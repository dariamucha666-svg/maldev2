#!/bin/bash
set -euo pipefail

REALM="${REALM:-XMASK.LAB}"
DOMAIN="${DOMAIN:-XMASK}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:?ADMIN_PASSWORD not set}"
DNS_FORWARDER="${DNS_FORWARDER:-1.1.1.1}"

SHORT_HOST="$(hostname -s)"
FQDN="${SHORT_HOST}.$(echo "$REALM" | tr '[:upper:]' '[:lower:]')"

hostname "$FQDN"
grep -q "$FQDN" /etc/hosts || echo "127.0.0.1 $FQDN $SHORT_HOST" >> /etc/hosts

if [ ! -f /var/lib/samba/private/sam.ldb ]; then
  echo "[*] Provisioning domain $DOMAIN ($REALM) ..."
  rm -f /etc/samba/smb.conf
  samba-tool domain provision --realm="$REALM" --domain="$DOMAIN" --adminpass="$ADMIN_PASSWORD" --server-role=dc --dns-backend=SAMBA_INTERNAL --use-rfc2307 --option="dns forwarder = $DNS_FORWARDER"
  echo "[*] Provisioning done."
fi

echo "[*] Starting Samba AD DC ($FQDN) ..."
exec samba -F --no-process-group
