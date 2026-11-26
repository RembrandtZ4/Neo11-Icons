#!/usr/bin/env bash
# Installiert oder aktualisiert das Mauszeiger-Theme „Neo11 Zeiger“ für den aktuellen Benutzer.
set -e
cd "$(dirname "$(readlink -f "$0")")"
ZIEL="$HOME/.local/share/icons/Neo11-Zeiger"

if [ "$(id -u)" -eq 0 ]; then
  echo "Bitte nicht als root bzw. mit sudo starten – das Theme wird für deinen Benutzer installiert."
  exit 1
fi

rm -rf "$ZIEL"
mkdir -p "$HOME/.local/share/icons"
cp -a zeiger/Neo11-Zeiger "$ZIEL"

echo "Fertig! „Neo11 Zeiger“ ist installiert."
echo "Aktivieren: Systemeinstellungen ▸ Farben & Design ▸ Mauszeiger ▸ „Neo11 Zeiger“"
