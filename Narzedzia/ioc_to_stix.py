#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agregator IoC z raportow pipeline -> STIX 2.1 / CSV (SOC) / JSON (dashboard).

Czyta katalog raportow (te same pliki co build_dashboard_history.py):
  - *.json raporty probek (file.sha256, analyzed_at, strings_ioc, classification)
  - iocs.json (agregat z rola/rodzina)
Deduplikuje po SHA256 probek i po (typ, wartosc) IoC.

Uzycie:
  python3 ioc_to_stix.py --reports DIR [--out PREFIX] [--format all|stix|csv|json]
                         [--tlp amber|red|green|clear] [--observed]
  PIPELINE_REPORTS=/root/samples/reports python3 ioc_to_stix.py
"""
from __future__ import annotations

import argparse, csv, datetime, hashlib, ipaddress, json, os, re, sys, uuid
from pathlib import Path

REPORTS = Path(os.environ.get("PIPELINE_REPORTS", "reports"))

TLP_IDS = {
    "red": "marking-definition--5e57c739-391a-4eb3-b6be-7d15ca92d5ed",
    "amber": "marking-definition--f88d31f6-486f-4971-8dda-618100589f7d",
    "green": "marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da",
    "clear": "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
}

IP_RE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")
URL_RE = re.compile(r"^https?://[A-Za-z0-9./_?=&:%+~#@-]+$", re.I)
DOM_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}(\.[a-z0-9][a-z0-9-]{0,62})+$", re.I)
HASH_RE = re.compile(r"^[0-9a-f]{64}$")

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_json(path):
    try:
        d = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        return d if isinstance(d, dict) else None
    except Exception:
        return None

def valid_ip(s):
    if not IP_RE.match(s):
        return False
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False

def clean_iocs(iocs: dict) -> dict:
    """Waliduje i normalizuje slownik IoC z raportu."""
    out = {"ips": [], "urls": [], "domains": [], "sha256": []}
    if not isinstance(iocs, dict):
        return out
    for v in (iocs.get("ips") or []):
        if valid_ip(str(v)):
            out["ips"].append(str(v))
    for v in (iocs.get("urls") or []):
        s = str(v).strip()
        if URL_RE.match(s):
            out["urls"].append(s)
    for v in (iocs.get("domains") or []):
        s = str(v).strip().lower().rstrip(".")
        if DOM_RE.match(s) and not valid_ip(s):
            out["domains"].append(s)
    for v in (iocs.get("sha256") or []):
        s = str(v).strip().lower()
        if HASH_RE.match(s):
            out["sha256"].append(s)
    for k in out:
        out[k] = sorted(set(out[k]))
    return out

def collect(reports_dir: Path) -> dict:
    """Zwraca: samples (lista dictow), iocs (dict type->{value: meta}), hashes."""
    samples = []
    if not reports_dir.is_dir():
        print("brak katalogu raportow: %s" % reports_dir)
        return {"samples": [], "iocs": {"ips": {}, "urls": {}, "domains": {}, "sha256": {}}}
    for path in sorted(reports_dir.glob("*.json")):
        if path.name == "iocs.json" or ".features" in path.name:
            continue
        data = load_json(path)
        if not data:
            continue
        f = data.get("file") or {}
        sha = (f.get("sha256") or "").lower() if isinstance(f, dict) else ""
        if not sha:
            continue
        samples.append({
            "sha256": sha,
            "name": (f.get("name") or path.stem) if isinstance(f, dict) else path.stem,
            "analyzed_at": str(data.get("analyzed_at") or ""),
            "role": ((data.get("classification") or {}).get("role") or data.get("role") or "unknown"),
            "family": ((data.get("classification") or {}).get("family") or ""),
            "iocs": clean_iocs(data.get("strings_ioc")),
        })

    # dopelnienie z iocs.json (agregat z rola/rodzina)
    agg_path = reports_dir / "iocs.json"
    agg = load_json(agg_path) if agg_path.exists() else None
    if agg and isinstance(agg.get("samples"), list):
        known = {s["sha256"] for s in samples}
        for e in agg["samples"]:
            sha = str(e.get("sha256") or "").lower()
            if not sha or sha in known:
                continue
            samples.append({
                "sha256": sha,
                "name": str(e.get("name") or sha[:12]),
                "analyzed_at": str(e.get("analyzed_at") or ""),
                "role": str(e.get("role") or "unknown"),
                "family": str(e.get("family") or ""),
                "iocs": clean_iocs(e.get("iocs")),
            })

    # dedupe po sha256 (pierwszy wygrywa)
    seen = set()
    uniq = []
    for s in samples:
        if s["sha256"] in seen:
            continue
        seen.add(s["sha256"])
        uniq.append(s)

    iocs = {"ips": {}, "urls": {}, "domains": {}, "sha256": {}}
    for s in uniq:
        for t in iocs:
            for v in s["iocs"].get(t, []):
                meta = iocs[t].setdefault(v, {"first_seen": s["analyzed_at"] or utc_now(),
                                              "last_seen": s["analyzed_at"] or utc_now(),
                                              "roles": set(), "families": set(), "samples": set()})
                if s["analyzed_at"]:
                    if s["analyzed_at"] < meta["first_seen"]:
                        meta["first_seen"] = s["analyzed_at"]
                    if s["analyzed_at"] > meta["last_seen"]:
                        meta["last_seen"] = s["analyzed_at"]
                meta["roles"].add(s["role"])
                if s["family"]:
                    meta["families"].add(s["family"])
                meta["samples"].add(s["sha256"][:12])
    return {"samples": uniq, "iocs": iocs}

# ---------------------------------------------------------------- STIX 2.1
def stix_pattern(t, v):
    if t == "ips":
        return "[ipv4-addr:value = '%s']" % v
    if t == "domains":
        return "[domain-name:value = '%s']" % v
    if t == "urls":
        return "[url:value = '%s']" % v
    if t == "sha256":
        return "[file:hashes.'SHA-256' = '%s']" % v

def stix_type_of(t):
    return {"ips": "ipv4-addr", "domains": "domain-name", "urls": "url", "sha256": "file"}[t]

def build_stix(data: dict, tlp: str, identity_name: str, with_observed: bool) -> dict:
    ident_id = "identity--" + str(uuid.uuid5(uuid.NAMESPACE_URL, identity_name))
    mark_id = TLP_IDS[tlp]
    objects = [
        {
            "type": "identity", "spec_version": "2.1", "id": ident_id,
            "name": identity_name, "identity_class": "organization",
            "description": "XMask lab — pipeline analizy malware",
        },
        {
            "type": "marking-definition", "spec_version": "2.1", "id": mark_id,
            "name": "TLP:" + tlp.upper(), "definition_type": "tlp",
            "definition": {"tlp": tlp},
        },
    ]
    label_default = "malicious"
    for t, bucket in data["iocs"].items():
        for v, meta in sorted(bucket.items()):
            iid = "indicator--" + str(uuid.uuid5(uuid.NAMESPACE_URL, "ioc:" + t + ":" + v))
            objects.append({
                "type": "indicator", "spec_version": "2.1", "id": iid,
                "name": stix_type_of(t) + ": " + v,
                "description": "IoC z pipeline XMask (role: %s; probki: %s)"
                               % (", ".join(sorted(meta["roles"])), ", ".join(sorted(meta["samples"]))),
                "pattern": stix_pattern(t, v),
                "pattern_type": "stix",
                "valid_from": meta["first_seen"] or utc_now(),
                "created_by_ref": ident_id,
                "object_marking_refs": [mark_id],
                "labels": [label_default] + sorted(meta["roles"]),
                "x_xmask": {"last_seen": meta["last_seen"],
                            "families": sorted(meta["families"]),
                            "samples": sorted(meta["samples"])},
            })
    if with_observed:
        for s in data["samples"]:
            oid = "observed-data--" + str(uuid.uuid5(uuid.NAMESPACE_URL, "obs:" + s["sha256"]))
            objects.append({
                "type": "observed-data", "spec_version": "2.1", "id": oid,
                "created_by_ref": ident_id,
                "object_marking_refs": [mark_id],
                "first_observed": s["analyzed_at"] or utc_now(),
                "last_observed": s["analyzed_at"] or utc_now(),
                "number_observed": 1,
                "labels": [s["role"]],
                "objects": {"0": {"type": "file", "hashes": {"SHA-256": s["sha256"]},
                                  "name": s["name"]}},
            })
    return {"type": "bundle", "id": "bundle--" + str(uuid.uuid4()), "spec_version": "2.1", "objects": objects}

# ---------------------------------------------------------------- JSON (dashboard)
def build_json(data: dict) -> dict:
    rows = []
    for t, bucket in data["iocs"].items():
        for v, meta in sorted(bucket.items()):
            rows.append({
                "type": stix_type_of(t), "value": v,
                "first_seen": meta["first_seen"], "last_seen": meta["last_seen"],
                "roles": sorted(meta["roles"]), "families": sorted(meta["families"]),
                "samples": sorted(meta["samples"]),
            })
    return {"generated": utc_now(), "samples": len(data["samples"]), "count": len(rows), "iocs": rows}

def build_csv(data: dict):
    lines = [["indicator_type", "value", "sha256", "role", "family", "first_seen", "source"]]
    for t, bucket in data["iocs"].items():
        for v, meta in sorted(bucket.items()):
            for s12 in sorted(meta["samples"]):
                lines.append([stix_type_of(t), v, s12,
                              ",".join(sorted(meta["roles"])),
                              ",".join(sorted(meta["families"])),
                              meta["first_seen"], "pipeline"])
    return lines

def main():
    ap = argparse.ArgumentParser(description="Agregator IoC -> STIX/CSV/JSON")
    ap.add_argument("--reports", default=str(REPORTS), help="katalog z raportami *.json")
    ap.add_argument("--out", default="ioc_export", help="prefix plikow wyjsciowych")
    ap.add_argument("--format", choices=["all", "stix", "csv", "json"], default="all")
    ap.add_argument("--tlp", choices=list(TLP_IDS), default="amber")
    ap.add_argument("--identity", default="XMask Lab")
    ap.add_argument("--observed", action="store_true", help="dodaj observed-data do STIX")
    a = ap.parse_args()

    data = collect(Path(a.reports))
    print("[*] probki: %d | IoC: IP=%d URL=%d DOM=%d HASH=%d" % (
        len(data["samples"]), len(data["iocs"]["ips"]), len(data["iocs"]["urls"]),
        len(data["iocs"]["domains"]), len(data["iocs"]["sha256"])))

    fmts = ["stix", "csv", "json"] if a.format == "all" else [a.format]
    for f in fmts:
        dest = Path(a.out + "." + f)
        if f == "stix":
            bundle = build_stix(data, a.tlp, a.identity, a.observed)
            dest.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        elif f == "json":
            dest.write_text(json.dumps(build_json(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        elif f == "csv":
            with open(dest, "w", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerows(build_csv(data))
        print("[*] %s -> %s" % (f, dest))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
