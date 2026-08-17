#!/usr/bin/env bash
# Compact IoC export hook — safe to call from pipeline.sh / nightly.
# Wrapper for ioc_to_stix.py: STIX 2.1 (TLP) + CSV (SOC) + JSON (dashboard).
# Non-fatal: failure prints a warning and exits 0 (nie blokuje pipeline.sh).
#
# Env:
#   REPORTS_DIR     katalog raportow pipeline  (default: /root/samples/reports)
#   IOC_EXPORT_DIR  katalog wyjsciowy          (default: REPORTS_DIR/export)
#   IOC_TLP         amber|red|green|clear      (default: amber)
#   IOC_OBSERVED    1 = dolacz observed-data do STIX (default: 0)
#   IOC_PUBLIC_DIR  opcjonalnie: kopia ioc_export.json dla dashboardu (np. /var/www/ioc-dashboard)
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORTS_DIR="${REPORTS_DIR:-/root/samples/reports}"
IOC_EXPORT_DIR="${IOC_EXPORT_DIR:-$REPORTS_DIR/export}"
IOC_TLP="${IOC_TLP:-amber}"
IOC_OBSERVED="${IOC_OBSERVED:-0}"
IOC_PUBLIC_DIR="${IOC_PUBLIC_DIR:-}"
PYTHON="${PYTHON:-$(command -v python3)}"

if [[ ! -d "$REPORTS_DIR" ]]; then
  echo "ioc export: no reports dir at $REPORTS_DIR" >&2
  exit 0
fi
mkdir -p "$IOC_EXPORT_DIR"

args=(--reports "$REPORTS_DIR" --out "$IOC_EXPORT_DIR/ioc_export" --format all --tlp "$IOC_TLP")
if [[ "$IOC_OBSERVED" == "1" ]]; then
  args+=(--observed)
fi

if ! "$PYTHON" "$SCRIPT_DIR/ioc_to_stix.py" "${args[@]}" >/dev/null 2>&1; then
  echo "ioc export: FAILED (ioc_to_stix.py)" >&2
  exit 0
fi

if [[ -n "$IOC_PUBLIC_DIR" && -d "$IOC_PUBLIC_DIR" ]]; then
  cp -f "$IOC_EXPORT_DIR/ioc_export.json" "$IOC_PUBLIC_DIR/ioc_export.json" 2>/dev/null || true
  echo "ioc export: public copy -> $IOC_PUBLIC_DIR/ioc_export.json"
fi

echo "ioc export: $IOC_EXPORT_DIR/ioc_export.{stix,csv,json}"
