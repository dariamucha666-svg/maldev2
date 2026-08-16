#!/bin/bash
set -euo pipefail
# Konta domeny do lancucha atakow AD. Hasla z env (poza vaultem).

mkuser() {
  local u="$1" p="$2"
  if samba-tool user show "$u" >/dev/null 2>&1; then
    echo "[i] $u juz istnieje - pomijam"
  else
    samba-tool user create "$u" "$p" --given-name="$u" --surname="Lab"
    samba-tool user setexpiry "$u" --noexpiry
    echo "[+] $u utworzony"
  fi
}

mkuser alice      "${ALICE_PASSWORD:-}"
mkuser bob        "${BOB_PASSWORD:-}"
mkuser carol      "${CAROL_PASSWORD:-}"
mkuser svc_sql    "${SVC_SQL_PASSWORD:-}"
mkuser svc_backup "${SVC_BACKUP_PASSWORD:-}"
mkuser asrep_user "${ASREP_PASSWORD:-}"

add_spn() {
  local u="$1" spn="$2"
  if samba-tool spn list "$u" 2>/dev/null | grep -qF "$spn"; then
    echo "[i] SPN $spn juz jest na $u"
  else
    samba-tool spn add "$spn" "$u"
    echo "[+] SPN $spn -> $u"
  fi
}
add_spn svc_sql    "MSSQLSvc/dc01.xmask.lab:1433"
add_spn svc_backup "backup/dc01.xmask.lab"

# AS-REP roastable: UF_DONT_REQUIRE_PREAUTH(0x400000) + UF_NORMAL_ACCOUNT(0x200) = 4194816
ldbmodify -H /var/lib/samba/private/sam.ldb <<EOF
dn: CN=asrep_user,CN=Users,DC=xmask,DC=lab
changetype: modify
replace: userAccountControl
userAccountControl: 4194816
EOF
echo "[+] asrep_user: no-preauth (AS-REP roastable)"

# Poluzuj polityke hasel (ulatwia spray w labie)
samba-tool domain passwordsettings set --min-pwd-length=7 --complexity=off --history-length=0 || true

echo "[OK] Konta gotowe."
