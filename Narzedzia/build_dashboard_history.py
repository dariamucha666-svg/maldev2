#!/usr/bin/env python3
"""Build history.json for the public lab dashboard from pipeline reports."""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPORTS = Path("/root/samples/reports")
OUT = Path("/var/www/ioc-dashboard/history.json")
WEB = Path("/root/android-pipeline/web/history.json")


def load_json(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def sha_of(name: str) -> str:
    return name.split(".")[0].lower()


def collect() -> dict:
    samples: list[dict] = []
    for path in sorted(REPORTS.glob("*.json")):
        if path.name == "iocs.json" or ".features" in path.name:
            continue
        data = load_json(path)
        if not data:
            continue
        cls = data.get("classification") if isinstance(data.get("classification"), dict) else {}
        f = data.get("file")
        digest = ""
        fname = path.stem
        if isinstance(f, dict):
            digest = (f.get("sha256") or "").lower()
            fname = f.get("name") or fname
        elif isinstance(f, str) and len(f) == 64 and f.isalnum():
            digest = f.lower()
        if not digest:
            digest = sha_of(path.name)
        at = str(data.get("analyzed_at") or "")
        samples.append(
            {
                "hash": digest,
                "name": fname,
                "analyzed_at": at,
                "day": at[:10],
                "role": cls.get("role") or data.get("role") or "unknown",
                "kind": "pe" if str(fname).lower().endswith((".exe", ".dll")) or "PE32" in str(f) else "apk",
            }
        )

    days: dict[str, dict] = {}
    for s in samples:
        day = s["day"] or "unknown"
        slot = days.setdefault(day, {"day": day, "count": 0, "roles": Counter(), "hashes": []})
        slot["count"] += 1
        slot["roles"][s["role"]] += 1
        slot["hashes"].append(s["hash"][:12])

    for p in sorted(REPORTS.glob("daily_summary_*.md")):
        m = re.search(r"(\d{8})", p.name)
        if not m:
            continue
        day = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:8]}"
        slot = days.setdefault(day, {"day": day, "count": 0, "roles": Counter(), "hashes": []})
        head = p.read_text(encoding="utf-8", errors="replace").splitlines()[:8]
        slot["summary"] = next((ln[2:].strip() for ln in head if ln.startswith("# ")), p.name)
        slot["source"] = p.name

    timeline = []
    for day, slot in sorted(days.items()):
        timeline.append(
            {
                "day": day,
                "count": slot["count"],
                "roles": dict(slot["roles"]),
                "hashes": slot["hashes"],
                "summary": slot.get("summary") or f"{slot['count']} analiz",
                "source": slot.get("source") or "",
            }
        )

    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "samples": samples,
        "timeline": timeline,
    }


def main() -> int:
    payload = collect()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    for dest in (OUT, WEB):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text + "\n", encoding="utf-8")
    print(f"history: {len(payload['samples'])} samples, {len(payload['timeline'])} days → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
