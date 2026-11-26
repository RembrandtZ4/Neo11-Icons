#!/usr/bin/env bash
# Installiert oder aktualisiert das Icon-Theme „Neo11 Silber“ für den aktuellen Benutzer.
#   ./install.sh        → mit der zuletzt gewählten Größe (Standard 90 %)
#   ./install.sh 75     → Motive füllen 75 % der Fläche; die Größe wird für spätere Updates gemerkt
set -e
cd "$(dirname "$(readlink -f "$0")")"

ZIEL="$HOME/.local/share/icons/Neo11-Silber"
MERKER="$HOME/.config/neo11-silber-groesse"

if [ "$(id -u)" -eq 0 ]; then
  echo "Bitte nicht als root bzw. mit sudo starten – das Theme wird für deinen Benutzer installiert."
  exit 1
fi

GROESSE="$1"
if [ -z "$GROESSE" ] && [ -f "$MERKER" ]; then
  GROESSE="$(cat "$MERKER")"
fi
GROESSE="${GROESSE:-90}"
if ! [[ "$GROESSE" =~ ^[0-9]+$ ]] || [ "$GROESSE" -lt 40 ] || [ "$GROESSE" -gt 100 ]; then
  echo "Bitte eine Größe zwischen 40 und 100 angeben, z. B. ./install.sh 75"
  exit 1
fi
mkdir -p "$HOME/.config"
echo "$GROESSE" > "$MERKER"

QUELLE="Neo11-Silber"
if [ "$GROESSE" != "90" ]; then
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  NEO11_OUT="$TMP/Neo11-Silber" python3 tools/generate.py "$GROESSE" >/dev/null
  QUELLE="$TMP/Neo11-Silber"
fi

rm -rf "$ZIEL"
mkdir -p "$HOME/.local/share/icons"
cp -r "$QUELLE" "$ZIEL"

# Symbol-Zwischenspeicher leeren, damit KDE die neuen Symbole sofort zeigt
rm -f "$HOME/.cache/icon-cache.kcache"
command -v kbuildsycoca6 >/dev/null 2>&1 && kbuildsycoca6 >/dev/null 2>&1 || true

echo "Fertig! „Neo11 Silber“ ist mit ${GROESSE} % installiert."
echo "Aktivieren: Systemeinstellungen ▸ Farben & Design ▸ Symbole ▸ „Neo11 Silber“"
echo "Taskleiste neu laden:  systemctl --user restart plasma-plasmashell"
