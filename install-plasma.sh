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

for arg in "$@"; do
  case "$arg" in
    --aktivieren)
      plasma-apply-desktoptheme Neo11
      plasma-apply-colorscheme Neo11
      ;;
    --taskleiste-win11)
      # Wie Windows 11: Leiste 48 px hoch, Symbole 24 px, normaler Abstand zwischen den Symbolen
      busctl --user call org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell evaluateScript s '
        panels().forEach(function (p) {
          if (p.location == "bottom" || p.location == "top") { p.height = 48; }
          p.widgets().forEach(function (w) {
            if (w.type == "org.kde.plasma.icontasks" || w.type == "org.kde.plasma.taskmanager") {
              w.currentConfigGroup = ["General"];
              w.writeConfig("iconSpacing", 1);
              w.reloadConfig();
            }
          });
        });' >/dev/null && echo "Taskleiste: 48 px, Symbole 24 px (wie Windows 11)."
      ;;
  esac
done

# Plasma neu starten, damit die geänderten Grafiken sofort geladen werden
if pgrep -x plasmashell >/dev/null; then
  systemctl --user restart plasma-plasmashell.service 2>/dev/null \
    || { kquitapp6 plasmashell 2>/dev/null; sleep 1; (kstart plasmashell >/dev/null 2>&1 &); }
fi

echo "Fertig! „Neo11“ ist installiert."
echo "Aktivieren: Systemeinstellungen ▸ Farben & Design ▸ Plasma-Stil ▸ „Neo11“"
echo "            und ▸ Farben ▸ „Neo11“ – oder einfach: ./install-plasma.sh --aktivieren"
echo "Taskleiste wie Windows 11 (48 px, 24-px-Symbole): ./install-plasma.sh --taskleiste-win11"
