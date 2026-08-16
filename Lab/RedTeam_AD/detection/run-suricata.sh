#!/bin/bash
# Uruchom Suricate na bridge'u labnet (dynamicznie wykrywa interfejs).
# Uwaga: trzymaj w trwalym terminalu/screen — proces zostaje na pierwszym planie.
set -euo pipefail
NET_ID=$(docker network inspect redteam-ad_labnet --format '{{.Id}}' | cut -c1-12)
IFACE="br-${NET_ID}"
RULES=/etc/suricata/rules/local.rules
LOGDIR=/var/log/suricata
mkdir -p "$LOGDIR"
echo "[*] Labnet bridge: $IFACE"
echo "[*] Reguly: $RULES"
exec suricata -i "$IFACE" -S "$RULES" -l "$LOGDIR"
