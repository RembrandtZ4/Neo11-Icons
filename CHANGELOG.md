# Änderungen

## 1.3.1 – 26.11.2026

- Mauszeiger: zusätzliche Verknüpfung in `~/.icons`, damit „Neo11 Zeiger“ in den Systemeinstellungen erscheint (KDE sucht Mauszeiger nicht in `~/.local/share/icons`)

## 1.3.0 – 26.11.2026

- Neu: Mauszeiger-Theme „Neo11 Zeiger“ – 22 eigene Zeiger im geometrischen Stil mit weichem Schatten, über 100 Aliasnamen für alle Programme, animiertes Warten und „Arbeitet im Hintergrund“, Größen 24–96 px
- Installation mit `./install-zeiger.sh`

## 1.2.0 – 26.11.2026

- Schutz für Original-Symbole: KDE kürzt fehlende Symbolnamen und landete dabei auf Silber-Symbolen (z. B. Lautstärke im Systemabschnitt → Musikdatei). `tools/protect.py` verweist bei der Installation für alle betroffenen Namen auf die Breeze-Originale
- „Arbeitsfläche anzeigen“ (user-desktop) nutzt wieder das Original; der Ordner „Schreibtisch“ bleibt silbern

## 1.1.2 – 26.11.2026

- `./install.sh <Prozent>` merkt sich die gewählte Symbolgröße für spätere Updates
- Eine eigene Größe verändert die Dateien im Repository nicht mehr – `git pull` bleibt ohne Konflikte

## 1.1.1 – 26.11.2026

- Neue Symbole „Programm ausführen“ und „Hilfe“ – damit zeigt auch die Vorschau in den Systemeinstellungen nur noch Neo11-Silber-Symbole
- install.sh leert den Symbol-Zwischenspeicher von KDE, damit neue Symbole sofort erscheinen

## 1.1.0 – 26.11.2026

- Ordner: Standard, Dokumente, Bilder, Musik, Videos, Downloads, Schreibtisch, Persönlicher Ordner, Cloud, Netzwerk
- Papierkorb leer und voll
- Laufwerke: Festplatte, SSD, USB-Stick, CD/DVD
- Dateitypen: Text, Bild, Musik, Video, PDF, Archiv, Skript, Programm, ISO-Abbild, Webseite, Office-Dokument, Tabelle, Präsentation, Unbekannt
- Insgesamt 81 Motive für 149 Symbolnamen

## 1.0.0 – 26.11.2026

- Erste Version: 54 eigene Silber-Motive für 64 Programm-Symbolnamen
- Startsymbole (start-here, start-here-kde …) zeigen die Neo11-Kacheln statt des Logos des Icon-Themes
- Symbolgröße 90 %, mit `./install.sh <Prozent>` änderbar
- Basis-Theme für alle übrigen Symbole: Breeze Dark
