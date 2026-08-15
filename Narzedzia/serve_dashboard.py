#!/usr/bin/env python3
"""Static dashboard + live hash hunt (MalwareBazaar metadata only — no samples)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(os.environ.get("DASH_ROOT", "/var/www/ioc-dashboard"))
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
    if catalog.is_file():
        try:
            samples = json.loads(catalog.read_text()).get("samples") or {}
        except Exception:
            samples = {}
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
            payload = json.loads(iocs.read_text())
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
    return out


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in {"/api/hunt", "/hunt"}:
            q = urllib.parse.parse_qs(parsed.query).get("q", [""])[0]
            body = json.dumps(hunt(q), ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/api/iocs":
            self.path = "/iocs.json"
        return super().do_GET()

    def log_message(self, fmt: str, *args) -> None:
        if args and str(args[0]).startswith("GET /api/"):
            super().log_message(fmt, *args)


def main() -> None:
    host = os.environ.get("DASH_BIND", "0.0.0.0")
    port = int(os.environ.get("DASH_PORT", "8080"))
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"dashboard+hunt on {host}:{port} root={ROOT}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
