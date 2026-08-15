#!/usr/bin/env python3
"""Static dashboard + live hash hunt (MalwareBazaar metadata only — no samples)."""
from __future__ import annotations

import gzip
import json
import os
import re
import sys
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from sliver_sessions import get_snapshot as sliver_snapshot
except ImportError:  # pragma: no cover - dashboard still serves IoC without Sliver
    sliver_snapshot = None

ROOT = Path(os.environ.get("DASH_ROOT", "/var/www/ioc-dashboard"))
JOBS = ROOT / "jobs"
SAMPLES = Path(os.environ.get("SAMPLES_ROOT", "/root/samples"))
RAW = SAMPLES / "raw"
QUAR = SAMPLES / "quarantine"
REPORTS = SAMPLES / "reports"
PIPELINE = Path("/root/android-pipeline/bin/pipeline.sh")
HASH_RE = re.compile(r"^[a-fA-F0-9]{64}$")
_JSON_CACHE: dict[str, tuple[float, int, object]] = {}
_HUNT_CACHE: dict[str, tuple[float, dict]] = {}
_HUNT_TTL = 60.0
_SAMPLE_IDX: dict = {"ts": 0.0, "map": {}}
_FILE_LOCK = threading.Lock()
MB_URL = "https://mb-api.abuse.ch/api/v1/"
MB_KEY_FILES = (
    Path("/root/.mb_api_key"),
    Path("/root/android-pipeline/config/secrets.env"),
)
TAG_MAP = {
    "lumma": "LummaStealer",
    "stealc": "StealC",
    "vidar": "Vidar",
    "redline": "RedLineStealer",
    "tesla": "AgentTesla",
    "formbook": "Formbook",
    "xloader": "XLoader",
    "nanocore": "NanoCore",
    "asyncrat": "AsyncRAT",
    "remcos": "RemcosRAT",
    "quasar": "QuasarRAT",
    "anatsa": "Anatsa",
    "hook": "Hook",
    "ermac": "Ermac",
    "sms": "Android",
    "nfc": "Android",
    "xmrig": "XMRig",
    "lockbit": "LockBit",
    "akira": "Akira",
    "nsis": "NSIS",
    "electron": "Electron",
    "chrome": "Chrome",
    "receita": "Chrome",
}


def read_json_cached(path: Path):
    try:
        st = path.stat()
    except OSError:
        return None
    key = str(path)
    with _FILE_LOCK:
        hit = _JSON_CACHE.get(key)
        if hit and hit[0] == st.st_mtime and hit[1] == st.st_size:
            return hit[2]
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    with _FILE_LOCK:
        _JSON_CACHE[key] = (st.st_mtime, st.st_size, data)
    return data


def sample_index() -> dict[str, Path]:
    now = time.time()
    if _SAMPLE_IDX["map"] and now - _SAMPLE_IDX["ts"] < 30:
        return _SAMPLE_IDX["map"]
    mapping: dict[str, Path] = {}
    skip = {".zip", ".json", ".log", ".md", ".txt"}
    for folder in (RAW, QUAR):
        if not folder.is_dir():
            continue
        try:
            names = list(folder.iterdir())
        except OSError:
            continue
        for path in names:
            if not path.is_file() or path.suffix.lower() in skip:
                continue
            low = path.name.lower()
            for token in HASH_RE.findall(low):
                mapping.setdefault(token, path)
            stem = path.stem.lower()
            if len(stem) >= 12:
                mapping.setdefault(stem, path)
    _SAMPLE_IDX["ts"] = now
    _SAMPLE_IDX["map"] = mapping
    return mapping


def mb_key() -> str:
    env = os.environ.get("MB_API_KEY", "").strip()
    if env:
        return env
    for path in MB_KEY_FILES:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.name.endswith(".env"):
            for line in text.splitlines():
                if line.startswith("MB_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        else:
            return text.strip()
    return ""


def mb_post(fields: dict) -> dict:
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(MB_URL, data=data, method="POST")
    key = mb_key()
    if key:
        req.add_header("Auth-Key", key)
    req.add_header("User-Agent", "xmask-lab-dashboard/1.0")
    with urllib.request.urlopen(req, timeout=18) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def slim(row: dict) -> dict:
    sha = row.get("sha256_hash") or row.get("sha256") or ""
    return {
        "sha256": sha,
        "md5": row.get("md5_hash") or row.get("md5") or "",
        "signature": row.get("signature") or row.get("tags") or "",
        "file_type": row.get("file_type") or row.get("file_type_mime") or "",
        "first_seen": row.get("first_seen") or "",
        "file_name": row.get("file_name") or "",
        "tags": row.get("tags") or [],
        "local": False,
    }


def local_hits(q: str) -> list[dict]:
    q = q.lower().strip()
    hits = []
    catalog = ROOT / "catalog.json"
    iocs = ROOT / "iocs.json"
    samples = {}
    cat = read_json_cached(catalog) if catalog.is_file() else None
    if isinstance(cat, dict):
        samples = cat.get("samples") or {}
    for digest, meta in samples.items():
        blob = " ".join(
            [digest, meta.get("title") or "", meta.get("family") or "", meta.get("role") or "", " ".join(meta.get("aka") or [])]
        ).lower()
        if q in blob or digest.startswith(q) or q.startswith(digest[:12]):
            hits.append(
                {
                    "sha256": digest,
                    "signature": meta.get("family") or "",
                    "file_type": meta.get("kind") or "",
                    "first_seen": "korpus",
                    "file_name": meta.get("title") or "",
                    "tags": [meta.get("role") or ""],
                    "local": True,
                    "title": meta.get("title"),
                    "verdict": meta.get("verdict"),
                }
            )
    if iocs.is_file() and q.isalnum() and len(q) >= 8:
        try:
            payload = read_json_cached(iocs) or {}
            for ioc in payload.get("iocs") or []:
                h = (ioc.get("hash") or "").lower()
                if h.startswith(q) and not any(x["sha256"] == h for x in hits):
                    hits.append(
                        {
                            "sha256": h,
                            "signature": ioc.get("family") or "",
                            "file_type": ioc.get("kind") or "",
                            "first_seen": ioc.get("date") or "",
                            "file_name": ioc.get("name") or "",
                            "tags": ioc.get("tags") or [],
                            "local": True,
                        }
                    )
        except Exception:
            pass
    return hits[:20]


def hunt(q: str) -> dict:
    q = (q or "").strip()
    out = {"query": q, "local": [], "remote": [], "error": ""}
    if not q:
        out["error"] = "puste zapytanie"
        return out
    key = q.lower()
    now = time.time()
    cached = _HUNT_CACHE.get(key)
    if cached and now - cached[0] < _HUNT_TTL:
        return cached[1]
    out["local"] = local_hits(q)
    compact = q.replace(" ", "")
    try:
        if all(c in "0123456789abcdefABCDEF" for c in compact) and len(compact) >= 32:
            payload = mb_post({"query": "get_info", "hash": compact})
            rows = payload.get("data") or []
            if isinstance(rows, dict):
                rows = [rows]
            out["remote"] = [slim(r) for r in rows][:15]
            out["source"] = "malwarebazaar:get_info"
        else:
            tag = TAG_MAP.get(q.lower(), q)
            payload = mb_post({"query": "get_taginfo", "tag": tag, "limit": "12"})
            if payload.get("query_status") not in {"ok", "success"}:
                payload = mb_post({"query": "get_siginfo", "signature": tag, "limit": "12"})
            rows = payload.get("data") or []
            out["remote"] = [slim(r) for r in rows][:12]
            out["source"] = "malwarebazaar:tag/sig"
            out["tag"] = tag
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        out["error"] = f"MalwareBazaar: {exc}"
    _HUNT_CACHE[key] = (now, out)
    if len(_HUNT_CACHE) > 64:
        oldest = sorted(_HUNT_CACHE, key=lambda k: _HUNT_CACHE[k][0])[:16]
        for stale in oldest:
            _HUNT_CACHE.pop(stale, None)
    return out


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def job_path(digest: str) -> Path:
    JOBS.mkdir(parents=True, exist_ok=True)
    return JOBS / f"{digest.lower()}.json"


def report_exists(digest: str) -> bool:
    return (REPORTS / f"{digest}.json").is_file() or (REPORTS / digest / f"{digest}.json").is_file()


def sample_on_disk(digest: str) -> Path | None:
    digest = digest.lower()
    idx = sample_index()
    hit = idx.get(digest)
    if hit:
        return hit
    for key, path in idx.items():
        if digest in key or key.startswith(digest[:12]):
            return path
    return None


def read_job(digest: str) -> dict:
    digest = digest.lower()
    path = job_path(digest)
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    state = "done" if report_exists(digest) else ("added" if sample_on_disk(digest) else "idle")
    return {
        "hash": digest,
        "state": state,
        "added": sample_on_disk(digest) is not None or report_exists(digest),
        "analyzed": report_exists(digest),
        "message": "już w raportach" if report_exists(digest) else "",
        "updated": utc_now(),
        "report": report_summary(digest),
    }


def write_job(digest: str, **fields) -> dict:
    data = read_job(digest)
    data.update(fields)
    data["hash"] = digest.lower()
    data["updated"] = utc_now()
    job_path(digest).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data


def _clean_strings(items) -> list[str]:
    out = []
    for raw in items or []:
        s = str(raw).strip()
        if 4 <= len(s) <= 48 and re.match(r"^[A-Za-z0-9_./:-]+$", s):
            out.append(s)
        if len(out) >= 8:
            break
    return out


def report_summary(digest: str) -> dict:
    for path in (REPORTS / f"{digest}.json", REPORTS / digest / f"{digest}.json"):
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        cls = data.get("classification") if isinstance(data.get("classification"), dict) else {}
        return {
            "role": cls.get("role") or data.get("kind") or "",
            "family": cls.get("family") or "",
            "analyzed_at": data.get("analyzed_at") or "",
            "tags": data.get("tags") or [],
            "urls": [str(u) for u in (data.get("urls") or [])[:6] if isinstance(u, str) and len(u) < 120],
            "suspicious": _clean_strings(data.get("suspicious_strings")),
        }
    return {}


def enqueue(digest: str, action: str) -> dict:
    digest = digest.lower().strip()
    if not HASH_RE.match(digest):
        return {"error": "podaj pełny SHA256 (64 znaki hex)", "hash": digest}
    if action not in {"add", "analyze", "re"}:
        return {"error": "nieznana akcja", "hash": digest}
    current = read_job(digest)
    if current.get("state") in {"queued", "downloading", "analyzing"}:
        return current
    if action == "add" and sample_on_disk(digest):
        return write_job(digest, state="added", added=True, message="już leży w próbkach")
    if action in {"analyze", "re"} and report_exists(digest) and action != "analyze":
        return write_job(
            digest,
            state="done",
            added=True,
            analyzed=True,
            message="raport już jest — otwórz reverse engineering",
            report=report_summary(digest),
        )
    write_job(digest, state="queued", message="w kolejce", action=action)
    log = JOBS / f"{digest}.log"
    subprocess.Popen(
        ["/usr/bin/python3", str(Path(__file__).resolve()), "--job", digest, action],
        stdout=open(log, "ab"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    return read_job(digest)


def download_sample(digest: str) -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    QUAR.mkdir(parents=True, exist_ok=True)
    existing = sample_on_disk(digest)
    if existing:
        return existing
    dest_zip = QUAR / f"{digest}.zip"
    if not dest_zip.is_file() or dest_zip.stat().st_size < 32:
        data = urllib.parse.urlencode({"query": "get_file", "sha256_hash": digest}).encode()
        req = urllib.request.Request(MB_URL, data=data, method="POST")
        key = mb_key()
        if key:
            req.add_header("Auth-Key", key)
        with urllib.request.urlopen(req, timeout=90) as resp:
            dest_zip.write_bytes(resp.read())
    head = dest_zip.read_bytes()[:16]
    if head.startswith(b"MZ"):
        out = QUAR / f"{digest}.exe"
        shutil.copy2(dest_zip, out)
        return out
    if not head.startswith(b"PK"):
        raise RuntimeError(f"odpowiedź MalwareBazaar to nie ZIP (start={head[:8]!r})")
    seven = shutil.which("7z") or shutil.which("7zz")
    if not seven:
        raise RuntimeError("brak 7z — ZIP z Bazaar jest AES, Python go nie otworzy")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        proc = subprocess.run(
            [seven, "x", f"-pinfected", f"-o{tmp_path}", "-y", str(dest_zip)],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"7z nie rozpakował ZIP: {(proc.stderr or proc.stdout)[-300:]}")
        files = [p for p in tmp_path.rglob("*") if p.is_file()]
        if not files:
            raise RuntimeError("ZIP pusty po rozpakowaniu")
        prefer = {".apk", ".xapk", ".exe", ".dll", ".msi", ".jar", ".dex"}
        ranked = [p for p in files if p.suffix.lower() in prefer] or files
        picked = max(ranked, key=lambda p: p.stat().st_size)
        ext = picked.suffix.lower() or ".bin"
        extracted = QUAR / f"{digest}{ext}"
        shutil.copy2(picked, extracted)
        if ext == ".apk":
            shutil.copy2(picked, RAW / f"{digest}.apk")
    _SAMPLE_IDX["ts"] = 0
    return extracted


def run_pipeline(sample: Path) -> None:
    if not PIPELINE.is_file():
        raise RuntimeError("brak pipeline.sh")
    env = os.environ.copy()
    env.setdefault("HOME", "/root")
    env.setdefault("USER", "root")
    env.setdefault("PIPELINE_HOME", "/root/android-pipeline")
    secrets = Path("/root/android-pipeline/config/secrets.env")
    if secrets.is_file():
        for line in secrets.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"'))
    env["FORCE"] = "1"
    proc = subprocess.run(
        ["/bin/bash", str(PIPELINE), str(sample)],
        env=env,
        capture_output=True,
        text=True,
        timeout=900,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "")[-800:]
        raise RuntimeError(f"pipeline exit {proc.returncode}: {tail}")
    src = SAMPLES / "reports" / "iocs.json"
    if src.is_file():
        shutil.copy2(src, ROOT / "iocs.json")
    hist = Path("/root/obsidian-vault/Narzedzia/build_dashboard_history.py")
    if hist.is_file():
        subprocess.run(["/usr/bin/python3", str(hist)], check=False)


def run_job(digest: str, action: str) -> None:
    digest = digest.lower()
    try:
        write_job(digest, state="downloading", message="pobieram z MalwareBazaar…")
        sample = download_sample(digest)
        write_job(digest, state="added", added=True, message=f"zapisano {sample.name}")
        if action == "add":
            return
        write_job(digest, state="analyzing", message="pipeline (static, bez detonacji)…")
        run_pipeline(sample)
        write_job(
            digest,
            state="done",
            added=True,
            analyzed=True,
            message="analiza skończona",
            report=report_summary(digest),
        )
    except Exception as exc:  # noqa: BLE001
        write_job(digest, state="error", message=str(exc)[:500])


def boot_payload() -> dict:
    iocs_raw = read_json_cached(ROOT / "iocs.json") or {}
    if isinstance(iocs_raw, list):
        items = iocs_raw
        generated = ""
    else:
        items = iocs_raw.get("iocs") or []
        generated = iocs_raw.get("generated") or ""
    catalog = read_json_cached(ROOT / "catalog.json") or {"samples": {}}
    history = read_json_cached(ROOT / "history.json") or {"timeline": [], "samples": []}
    sliver = {
        "ok": False,
        "counts": {
            "sessions": 0,
            "sessions_live": 0,
            "beacons": 0,
            "beacons_live": 0,
            "jobs": 0,
        },
    }
    if sliver_snapshot is not None:
        snap = sliver_snapshot()
        sliver = {
            "ok": bool(snap.get("ok")),
            "generated": snap.get("generated") or "",
            "server": snap.get("server") or {},
            "counts": snap.get("counts") or sliver["counts"],
            "error": snap.get("error") or "",
        }
    return {
        "generated": generated or utc_now(),
        "count": len(items),
        "iocs": items,
        "catalog": catalog,
        "history": history,
        "sliver": sliver,
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send(self, body: bytes, content_type: str, code: int = 200, cache: str = "no-store") -> None:
        accept = self.headers.get("Accept-Encoding", "")
        headers = {
            "Content-Type": content_type,
            "Cache-Control": cache,
        }
        payload = body
        if "gzip" in accept and len(body) > 256:
            payload = gzip.compress(body, compresslevel=5)
            headers["Content-Encoding"] = "gzip"
            headers["Vary"] = "Accept-Encoding"
        headers["Content-Length"] = str(len(payload))
        self.send_response(code)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def _json(self, payload: dict, code: int = 200, cache: str = "no-store") -> None:
        self._send(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode(), "application/json; charset=utf-8", code, cache)

    def _safe_file(self, rel: str) -> Path | None:
        candidate = (ROOT / rel.lstrip("/")).resolve()
        if candidate == ROOT or ROOT in candidate.parents:
            return candidate if candidate.is_file() else None
        return None

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if parsed.path in {"/api/boot", "/boot.json"}:
            self._json(boot_payload(), cache="public, max-age=8")
            return
        if parsed.path in {"/api/hunt", "/hunt"}:
            self._json(hunt(qs.get("q", [""])[0]))
            return
        if parsed.path == "/api/job":
            digest = (qs.get("hash", [""])[0] or "").lower()
            if not HASH_RE.match(digest):
                self._json({"error": "podaj pełny SHA256"}, 400)
                return
            self._json(read_job(digest))
            return
        if parsed.path == "/api/jobs":
            raw = qs.get("hashes", [""])[0]
            hashes = [h.lower() for h in raw.split(",") if HASH_RE.match(h.strip())]
            self._json({h: read_job(h) for h in hashes})
            return
        if parsed.path in {"/api/sliver/sessions", "/api/sliver", "/api/sessions"}:
            if sliver_snapshot is None:
                self._json(
                    {
                        "ok": False,
                        "error": "brak sliver_sessions.py / sliver-py",
                        "sessions": [],
                        "beacons": [],
                        "jobs": [],
                        "counts": {
                            "sessions": 0,
                            "sessions_live": 0,
                            "beacons": 0,
                            "beacons_live": 0,
                            "jobs": 0,
                        },
                    },
                    503,
                )
                return
            self._json(sliver_snapshot(), cache="public, max-age=5")
            return
        if parsed.path == "/api/iocs":
            parsed = parsed._replace(path="/iocs.json")
        if parsed.path in {"/", "/index.html"}:
            path = ROOT / "index.html"
            if path.is_file():
                self._send(path.read_bytes(), "text/html; charset=utf-8", cache="public, max-age=30")
                return
        if parsed.path.endswith(".json"):
            path = self._safe_file(parsed.path)
            if path:
                self._send(path.read_bytes(), "application/json; charset=utf-8", cache="public, max-age=15")
                return
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/job":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length") or 0)
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json({"error": "zły JSON"}, 400)
            return
        digest = str(payload.get("hash") or "").strip()
        action = str(payload.get("action") or "analyze").strip()
        self._json(enqueue(digest, action))

    def log_message(self, fmt: str, *args) -> None:
        if args and str(args[0]).startswith("GET /api/"):
            super().log_message(fmt, *args)


def main() -> None:
    host = os.environ.get("DASH_BIND", "0.0.0.0")
    port = int(os.environ.get("DASH_PORT", "8080"))
    httpd = ThreadingHTTPServer((host, port), Handler)
    if sliver_snapshot is not None:
        try:
            sliver_snapshot()
        except Exception:
            pass
    print(f"dashboard+hunt on {host}:{port} root={ROOT}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--job":
        run_job(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "analyze")
    else:
        main()
