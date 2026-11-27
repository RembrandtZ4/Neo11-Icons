#!/usr/bin/env bash
# Installiert oder aktualisiert den Plasma-Stil und das Farbschema „Neo11“.
set -e
cd "$(dirname "$(readlink -f "$0")")"
if [ "$(id -u)" -eq 0 ]; then
  echo "Bitte nicht als root bzw. mit sudo starten."
  exit 1
fi
mkdir -p "$HOME/.local/share/plasma/desktoptheme" "$HOME/.local/share/color-schemes"
# Ordner nicht erst löschen (sonst fällt ein laufendes Plasma kurz auf Breeze zurück), sondern überschreiben
mkdir -p "$HOME/.local/share/plasma/desktoptheme/Neo11"
cp -rT plasma/desktoptheme/Neo11 "$HOME/.local/share/plasma/desktoptheme/Neo11"
# Reste eines kurzzeitigen Versuchs mit metadata.json entfernen (damit erkannte Plasma den Stil nicht)
rm -f "$HOME/.local/share/plasma/desktoptheme/Neo11/metadata.json" "$HOME/.local/share/plasma/desktoptheme/Neo11/plasmarc"
cp plasma/color-schemes/Neo11.colors "$HOME/.local/share/color-schemes/Neo11.colors"
WAR_AKTIV="$(kreadconfig6 --file plasmarc --group Theme --key name 2>/dev/null)"

# Rand um die Taskleisten-Symbole (Pixel) – wird gemerkt: ./install-plasma.sh --symbolrand 4
RAND_DATEI="$HOME/.config/neo11-symbolrand"
RAND="$(cat "$RAND_DATEI" 2>/dev/null || echo 4)"
prev=""
for arg in "$@"; do
  if [ "$prev" = "--symbolrand" ]; then RAND="$arg"; fi
  case "$arg" in --symbolrand=*) RAND="${arg#*=}";; esac
  prev="$arg"
done
if ! [[ "$RAND" =~ ^[0-9]+$ ]] || [ "$RAND" -gt 16 ]; then
  echo "Symbolrand muss eine Zahl von 0 bis 16 sein."; exit 1
fi
echo "$RAND" > "$RAND_DATEI"
python3 - "$HOME/.local/share/plasma/desktoptheme/Neo11/widgets/tasks.svgz" "$RAND" <<'PY'
import gzip, re, sys
path, rand = sys.argv[1], sys.argv[2]
s = gzip.open(path, "rt", encoding="utf-8").read()
s = re.sub(r'(<rect id="[a-z]+-hint-(?:top|bottom|left|right)-margin" x="-200" y="-200" )width="[\d.]+" height="[\d.]+"',
           r'\g<1>width="%s" height="%s"' % (rand, rand), s)
s = re.sub(r'(<rect\s+id="thick-hint-(?:top|bottom|left|right)-margin"[^>]*?)width="[\d.]+"\s+height="[\d.]+"',
           r'\g<1>width="%s"\n     height="%s"' % (rand, rand), s, flags=re.S)
with gzip.open(path, "wt", encoding="utf-8") as f:
    f.write(s)
PY
echo "Rand um die Taskleisten-Symbole: ${RAND} px"
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

# Plasma neu starten, damit die geänderten Grafiken sofort geladen werden.
# Erst über systemd (Standard bei Plasma 6); klappt das nicht, Plasma direkt ersetzen.
neustart_plasma() {
  if systemctl --user --quiet is-active plasma-plasmashell.service 2>/dev/null; then
    systemctl --user restart plasma-plasmashell.service && sleep 3
  fi
  if ! pgrep -x plasmashell >/dev/null; then
    setsid -f plasmashell --replace >/dev/null 2>&1
    sleep 3
  fi
  if pgrep -x plasmashell >/dev/null; then
    echo "Plasma wurde neu gestartet."
  else
    echo "Plasma läuft nicht – bitte Alt+F2 drücken, „plasmashell“ eingeben und Enter."
  fi
}
if pgrep -x plasmashell >/dev/null; then
  neustart_plasma
  if pgrep -x systemsettings >/dev/null; then
    echo "Hinweis: Die Systemeinstellungen sind geöffnet – bitte schließen, sonst stellen sie den alten Stil wieder ein."
  fi
  if [ "$WAR_AKTIV" = "Neo11" ]; then
    plasma-apply-desktoptheme Neo11 >/dev/null 2>&1 || true
  fi
fi

echo "Fertig! „Neo11“ ist installiert."
echo "Aktivieren: Systemeinstellungen ▸ Farben & Design ▸ Plasma-Stil ▸ „Neo11“"
echo "            und ▸ Farben ▸ „Neo11“ – oder einfach: ./install-plasma.sh --aktivieren"
echo "Taskleiste wie Windows 11 (48 px hoch): ./install-plasma.sh --taskleiste-win11"
echo "Symbole in der Taskleiste größer/kleiner: ./install-plasma.sh --symbolrand 4   (mehr Rand = kleinere Symbole)"
