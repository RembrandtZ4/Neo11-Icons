#!/usr/bin/env bash
# Installiert oder aktualisiert den Plasma-Stil, das Farbschema und die Fensterdekoration „Neo11“.
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
# Fensterdekoration (Titelleiste mit Knöpfen) – Fluent-round-dark mit silbernem statt rotem Schließen-Knopf
mkdir -p "$HOME/.local/share/aurorae/themes/Neo11"
cp -rT plasma/aurorae/Neo11 "$HOME/.local/share/aurorae/themes/Neo11"
DEKO_AKTIV="$(kreadconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme 2>/dev/null)"

fenster_neo11() {
  kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kwin.aurorae
  kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme __aurorae__svg__Neo11
  # Knöpfe wie Windows 11: links nur das App-Symbol (Fenstermenü), rechts Minimieren, Maximieren, Schließen
  kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnLeft M
  kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnRight IAX
  busctl --user call org.kde.KWin /KWin org.kde.KWin reconfigure >/dev/null 2>&1 || true
  echo "Fensterdekoration: Neo11 (Schließen-Knopf silbern)."
}
WAR_AKTIV="$(kreadconfig6 --file plasmarc --group Theme --key name 2>/dev/null)"

rm -f "$HOME/.config/neo11-symbolrand"   # früherer Versuch (--symbolrand), wirkt in Plasma 6 nicht
# Zwischenspeicher der Grafiken leeren (Plasma 6: ksvg-elements, Plasma 5: plasma-svgelements)
rm -f "$HOME"/.cache/ksvg-elements* "$HOME"/.cache/plasma_theme_*.kcache "$HOME"/.cache/plasma-svgelements* 2>/dev/null || true

# Ist die Dekoration schon aktiv, KWin die neuen Grafiken laden lassen
if [ "$DEKO_AKTIV" = "__aurorae__svg__Neo11" ]; then
  busctl --user call org.kde.KWin /KWin org.kde.KWin reconfigure >/dev/null 2>&1 || true
fi

for arg in "$@"; do
  case "$arg" in
    --aktivieren)
      plasma-apply-desktoptheme Neo11
      plasma-apply-colorscheme Neo11
      fenster_neo11
      ;;
    --fenster)
      fenster_neo11
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
  local alt neu
  alt="$(pgrep -x plasmashell | head -1)"
  systemctl --user reset-failed plasma-plasmashell.service 2>/dev/null || true
  setsid -f plasmashell --replace >/dev/null 2>&1
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    sleep 1
    neu="$(pgrep -x plasmashell | head -1)"
    if [ -n "$neu" ] && [ "$neu" != "$alt" ]; then
      echo "Plasma wurde neu gestartet."
      return 0
    fi
  done
  if pgrep -x plasmashell >/dev/null; then
    echo "Plasma läuft, wurde aber evtl. nicht neu geladen – bitte ab- und wieder anmelden."
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
echo "Nur die Fensterdekoration einschalten: ./install-plasma.sh --fenster"
echo "Taskleiste wie Windows 11 (48 px hoch): ./install-plasma.sh --taskleiste-win11"
echo "Symbole in der Taskleiste kleiner: im Ordner Neo11-Icons ./install.sh 75   (Größe in Prozent)"
