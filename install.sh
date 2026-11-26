#!/usr/bin/env bash
# Installiert oder aktualisiert das Icon-Theme „Neo11 Silber“ für den aktuellen Benutzer.
set -e
cd "$(dirname "$(readlink -f "$0")")"

ZIEL="$HOME/.local/share/icons/Neo11-Silber"

if [ "$(id -u)" -eq 0 ]; then
  echo "Bitte nicht als root bzw. mit sudo starten – das Theme wird für deinen Benutzer installiert."
  exit 1
fi

# Optional: andere Symbolgröße, z. B. ./install.sh 80
if [ -n "$1" ]; then
  python3 tools/generate.py "$1"
fi

rm -rf "$ZIEL"
mkdir -p "$HOME/.local/share/icons"
cp -r Neo11-Silber "$ZIEL"
# Symbol-Zwischenspeicher leeren, damit KDE die neuen Symbole sofort zeigt
rm -f "$HOME/.cache/icon-cache.kcache"
command -v kbuildsycoca6 >/dev/null 2>&1 && kbuildsycoca6 >/dev/null 2>&1 || true

echo "Fertig! „Neo11 Silber“ ist installiert."
echo "Aktivieren: Systemeinstellungen ▸ Farben & Design ▸ Symbole ▸ „Neo11 Silber“"
echo "Taskleiste neu laden (falls alte Symbole bleiben):  systemctl --user restart plasma-plasmashell"
