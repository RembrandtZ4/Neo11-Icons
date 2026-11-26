#!/usr/bin/env bash
# Installiert oder aktualisiert den Plasma-Stil und das Farbschema „Neo11“.
set -e
cd "$(dirname "$(readlink -f "$0")")"
if [ "$(id -u)" -eq 0 ]; then
  echo "Bitte nicht als root bzw. mit sudo starten."
  exit 1
fi
mkdir -p "$HOME/.local/share/plasma/desktoptheme" "$HOME/.local/share/color-schemes"
rm -rf "$HOME/.local/share/plasma/desktoptheme/Neo11"
cp -r plasma/desktoptheme/Neo11 "$HOME/.local/share/plasma/desktoptheme/Neo11"
cp plasma/color-schemes/Neo11.colors "$HOME/.local/share/color-schemes/Neo11.colors"
rm -f "$HOME"/.cache/plasma_theme_*.kcache "$HOME"/.cache/plasma-svgelements* 2>/dev/null || true

if [ "$1" = "--aktivieren" ]; then
  plasma-apply-desktoptheme Neo11
  plasma-apply-colorscheme Neo11
fi

echo "Fertig! „Neo11“ ist installiert."
echo "Aktivieren: Systemeinstellungen ▸ Farben & Design ▸ Plasma-Stil ▸ „Neo11“"
echo "            und ▸ Farben ▸ „Neo11“ – oder einfach: ./install-plasma.sh --aktivieren"
