#!/usr/bin/env python3
"""Erzeugt das Icon-Theme „Neo11 Silber“. Aufruf: python3 tools/generate.py [Größe in %, Standard 90]"""
import math, os, sys, shutil, pathlib

PERCENT = float(sys.argv[1]) if len(sys.argv) > 1 else 90.0
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "Neo11-Silber"
G, D, M, W = "url(#g)", "#1c1c1c", "#8f8f8f", "#ffffff"

def svg(body):
    s = (PERCENT / 100.0) * 32 / 26          # Motive sind auf 26 px (3..29) gezeichnet
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="3" x2="0" y2="29"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#a9a9a9"/></linearGradient></defs>
<g transform="translate(16 16) scale({s:.4f}) translate(-16 -16)">
{body}
</g>
</svg>
'''

def st(d, w=2, c=D, extra=""):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'

def gear_path(cx=16, cy=16, ro=13, ri=10.3, teeth=8):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4) - math.pi / 2
        r = ro if (i % 4) in (1, 2) else ri
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{G}" stroke="{G}" stroke-width="1.2" stroke-linejoin="round"/>'

def star(cx, cy, r, c=D):
    pts = []
    for i in range(10):
        a = math.pi * i / 5 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{c}" stroke-linejoin="round"/>'

PAGE = f'<path d="M8 3h11l6 6v18a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" fill="{G}"/><path d="M19 3v6h6" fill="{D}" opacity=".25"/>'
TERM = f'<rect x="3" y="5.5" width="26" height="21" rx="3" fill="{G}"/>'

GLYPHS = {
 "terminal": TERM + st("M8 12l4 4-4 4", 2.2) + f'<rect x="14" y="18.9" width="9" height="2.2" rx="1.1" fill="{D}"/>',
 "terminal-cursor": TERM + st("M8 12l4 4-4 4", 2.2) + f'<rect x="14.5" y="12" width="4.5" height="8" rx="1" fill="{D}"/>',
 "code": PAGE + st("M13 14l-3.5 3.5 3.5 3.5", 2) + st("M19 14l3.5 3.5-3.5 3.5", 2),
 "gear": gear_path() + f'<circle cx="16" cy="16" r="4.6" fill="{D}"/>',
 "update": st("M26.5 16a10.5 10.5 0 1 1-3.1-7.4", 3, G) + f'<polygon points="25.5,3.5 26.3,11.5 18.5,10" fill="{G}" stroke="{G}" stroke-width="1" stroke-linejoin="round"/>' + st("M16 10v9.5", 2.6, G) + st("M12 15.5l4 4 4-4", 2.6, G),
 "help-book": f'<rect x="6" y="3" width="20" height="26" rx="2.5" fill="{G}"/><rect x="9" y="3" width="1.6" height="26" fill="{D}" opacity=".35"/>' + st("M14.2 12.5a3 3 0 1 1 4.3 2.7c-1 .5-1.8 1.2-1.8 2.3v.6", 2) + f'<circle cx="16.7" cy="21.6" r="1.25" fill="{D}"/>',
 "activity": f'<rect x="3" y="5" width="26" height="22" rx="3" fill="{G}"/>' + st("M6.5 18h4.5l2.5-7 3.5 11 2.5-7h6", 2),
 "bars": TERM + ''.join(f'<rect x="{x}" y="{23-h}" width="4" height="{h}" rx="1" fill="{D}"/>' for x, h in ((8.5, 6), (14, 12), (19.5, 9))),
 "layers": ''.join(f'<rect x="4" y="{y}" width="24" height="6.4" rx="3.2" fill="{c}"/><circle cx="23.8" cy="{y+3.2}" r="1.2" fill="{D}"/>' for y, c in ((4.5, G), (12.8, G), (21.1, M))),
 "restore": st("M6.3 12.5A10.5 10.5 0 1 1 7.6 22.6", 3, G) + f'<polygon points="2.8,8.6 10.2,10.4 4.6,15.8" fill="{G}" stroke="{G}" stroke-width="1" stroke-linejoin="round"/>' + st("M16 10v6.5l4.2 2.6", 2.4, G),
 "welcome": f'<path d="M6 4.5h20a3 3 0 0 1 3 3v12.5a3 3 0 0 1-3 3H14l-6 5v-5H6a3 3 0 0 1-3-3V7.5a3 3 0 0 1 3-3z" fill="{G}"/>' + star(16, 13.8, 5.4),
 "package": f'<path d="M4.5 10.5l11.5 5.6 11.5-5.6v12.6L16 29 4.5 23.1z" fill="{G}"/><path d="M4.5 10.5L16 4.6l11.5 5.9L16 16.1z" fill="{W}"/><path d="M16 16.1V29" stroke="{D}" stroke-width=".9" opacity=".4"/><path d="M10 7.5l11.5 5.8" stroke="{D}" stroke-width="1.6" opacity=".35"/>',
 "bag": f'<path d="M6.5 11h19l-1.4 15.8a2.3 2.3 0 0 1-2.3 2.1H10.2a2.3 2.3 0 0 1-2.3-2.1z" fill="{G}"/>' + st("M11.5 11V9a4.5 4.5 0 0 1 9 0v2", 2.4, G) + f'<circle cx="11.5" cy="14.5" r="1.2" fill="{D}"/><circle cx="20.5" cy="14.5" r="1.2" fill="{D}"/>',
 "cloud": f'<path d="M9.5 25a6.5 6.5 0 0 1-.9-12.9A8.5 8.5 0 0 1 24.4 11a7 7 0 0 1-.2 14z" fill="{G}"/>',
 "layout": f'<rect x="3" y="5" width="26" height="22" rx="3" fill="{G}"/><rect x="6" y="9.5" width="8" height="14" rx="1.2" fill="{D}" opacity=".55"/><rect x="16" y="9.5" width="10" height="6" rx="1.2" fill="{D}" opacity=".55"/><rect x="16" y="17.5" width="10" height="6" rx="1.2" fill="{D}" opacity=".55"/>',
 "globe": f'<circle cx="16" cy="16" r="12.8" fill="{G}"/><ellipse cx="16" cy="16" rx="5.4" ry="12.8" fill="none" stroke="{D}" stroke-width="1.5"/>' + st("M3.2 16h25.6M5.2 9.6h21.6M5.2 22.4h21.6", 1.5),
 "compass": f'<circle cx="16" cy="16" r="12.8" fill="{G}"/><circle cx="16" cy="16" r="10.2" fill="none" stroke="{D}" stroke-width="1" opacity=".35"/><polygon points="22,10 17.9,17.9 10,22 14.1,14.1" fill="{D}"/><circle cx="16" cy="16" r="1.6" fill="{W}"/>',
 "chip": ''.join(f'<rect x="{p}" y="3.5" width="2" height="4" rx=".8" fill="{G}"/><rect x="{p}" y="24.5" width="2" height="4" rx=".8" fill="{G}"/><rect x="3.5" y="{p}" width="4" height="2" rx=".8" fill="{G}"/><rect x="24.5" y="{p}" width="4" height="2" rx=".8" fill="{G}"/>' for p in (10.5, 15, 19.5)) + f'<rect x="7.5" y="7.5" width="17" height="17" rx="2.6" fill="{G}"/><rect x="12" y="12" width="8" height="8" rx="1.3" fill="{D}"/>',
 "gpu": f'<rect x="3" y="7.5" width="26" height="15" rx="2.2" fill="{G}"/><circle cx="12" cy="15" r="5" fill="{D}"/><circle cx="12" cy="15" r="1.7" fill="{G}"/>' + st("M20 11.5v7M23 11.5v7M26 11.5v7", 1.4) + f'<rect x="6" y="22.5" width="13" height="3.6" rx="1" fill="{M}"/>',
 "translate": f'<path d="M6 3.5h12a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3h-7l-4.5 3.5v-3.5H6a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3z" fill="{G}"/><path d="M15.5 13.5h10.5a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H25v3.2l-4-3.2h-5.5a3 3 0 0 1-3-3v-7a3 3 0 0 1 3-3z" fill="{M}"/>' + st("M8.5 14.5l3.5-8.5 3.5 8.5M9.9 11.6h4.2", 1.8),
 "tree": f'<rect x="11.5" y="3" width="9" height="6.5" rx="1.6" fill="{G}"/>' + ''.join(f'<rect x="{x}" y="22.5" width="8" height="6.5" rx="1.6" fill="{G}"/>' for x in (3, 12, 21)) + st("M16 9.5v6M7 15.5h18M7 15.5v7M16 15.5v7M25 15.5v7", 2, G),
 "play-circle": f'<circle cx="16" cy="16" r="12.8" fill="{G}"/><polygon points="13,10 23,16 13,22" fill="{D}" stroke="{D}" stroke-width="1.2" stroke-linejoin="round"/>',
 "play-rect": f'<rect x="3" y="6" width="26" height="20" rx="3" fill="{G}"/><polygon points="13.5,11 21,16 13.5,21" fill="{D}" stroke="{D}" stroke-width="1.2" stroke-linejoin="round"/>',
 "clapper": f'<rect x="4" y="13" width="24" height="15" rx="2.2" fill="{G}"/><path d="M4.3 8.3l22-4.3 1 5.2-22 4.3z" fill="{G}"/>' + st("M9 7.3l2.6 4.2M14.5 6.2l2.6 4.2M20 5.2l2.6 4.2", 1.8) + st("M8 18h16M8 22.5h10", 1.6),
 "camera": f'<rect x="3" y="9" width="18" height="14" rx="3" fill="{G}"/><polygon points="22,14 29,10 29,22 22,18" fill="{G}" stroke="{G}" stroke-width="1" stroke-linejoin="round"/><circle cx="8" cy="13" r="1.5" fill="{D}"/>',
 "webcam": f'<circle cx="16" cy="13" r="9.5" fill="{G}"/><circle cx="16" cy="13" r="4.3" fill="{D}"/><circle cx="17.3" cy="11.7" r="1.4" fill="{G}"/>' + st("M16 22.5v4.5M10.5 28h11", 2.6, G),
 "note": st("M12.5 22V9l12-2.8v13", 2.4, G) + f'<ellipse cx="9.7" cy="22.4" rx="3.6" ry="2.8" fill="{G}"/><ellipse cx="21.7" cy="19.6" rx="3.6" ry="2.8" fill="{G}"/>',
 "kernel": f'<polygon points="16,3 27.3,9.5 27.3,22.5 16,29 4.7,22.5 4.7,9.5" fill="{G}" stroke="{G}" stroke-width="1.5" stroke-linejoin="round"/><circle cx="16" cy="16" r="5.6" fill="{D}"/><circle cx="16" cy="16" r="2.2" fill="{G}"/>',
 "gauge": st("M4.5 22a11.5 11.5 0 0 1 23 0", 3.2, G) + st("M16 22l6.2-7.2", 2.4, G) + f'<circle cx="16" cy="22" r="2.8" fill="{G}"/>' + st("M8.3 13.8l1.6 1.4M16 10.4v2.1M23.7 13.8l-1.6 1.4", 1.8, G),
 "diff": f'<rect x="3" y="4.5" width="11.5" height="21" rx="2" fill="{G}"/><rect x="17.5" y="6.5" width="11.5" height="21" rx="2" fill="{M}"/>' + st("M7.5 16h17M10.5 13l-3 3 3 3M21.5 13l3 3-3 3", 2),
 "archive": f'<rect x="4" y="8" width="24" height="20" rx="2.5" fill="{G}"/><rect x="3" y="4" width="26" height="6" rx="2" fill="{W}"/><rect x="12" y="13.5" width="8" height="2.6" rx="1.3" fill="{D}"/>',
 "folder": f'<path d="M3 9a2.5 2.5 0 0 1 2.5-2.5h7l2.5 2.5h11.5A2.5 2.5 0 0 1 29 11.5v13a2.5 2.5 0 0 1-2.5 2.5h-21A2.5 2.5 0 0 1 3 24.5z" fill="{G}"/><rect x="3" y="12" width="26" height="1.4" fill="{D}" opacity=".35"/>',
 "pie": f'<circle cx="16" cy="16" r="12.8" fill="{G}"/><path d="M17.5 14.5V2.6a12.8 12.8 0 0 1 11.2 15.4z" fill="{M}" stroke="{D}" stroke-width="1"/><circle cx="16" cy="16" r="4.3" fill="{D}"/>',
 "image": f'<rect x="3" y="5" width="26" height="22" rx="3" fill="{G}"/><polygon points="6,24 13,14 18,20.5 21,17 26,24" fill="{D}" stroke="{D}" stroke-width="1" stroke-linejoin="round"/><circle cx="21.5" cy="11" r="2.6" fill="{D}"/>',
 "pen-page": PAGE + f'<path d="M11 25l1-4.2 8.5-8.5 3.2 3.2-8.5 8.5z" fill="{D}"/>',
 "text-page": PAGE + st("M10.5 14h11M10.5 18h11M10.5 22h7", 1.8),
 "calculator": f'<rect x="6" y="3" width="20" height="26" rx="3" fill="{G}"/><rect x="9" y="6" width="14" height="5" rx="1.2" fill="{D}"/>' + ''.join(f'<rect x="{x}" y="{y}" width="3.4" height="3.4" rx=".9" fill="{D}"/>' for y in (14, 18.8, 23.6) for x in (9.2, 14.3, 19.4)),
 "phone": f'<rect x="9" y="2.5" width="14" height="27" rx="3" fill="{G}"/><rect x="11" y="6" width="10" height="17" rx="1.2" fill="{D}"/><circle cx="16" cy="26" r="1.3" fill="{D}"/>',
 "info": f'<circle cx="16" cy="16" r="12.8" fill="{G}"/><circle cx="16" cy="9.8" r="1.9" fill="{D}"/><rect x="14.3" y="13.5" width="3.4" height="10" rx="1.7" fill="{D}"/>',
 "menu-edit": f'<rect x="3" y="4" width="21" height="24" rx="3" fill="{G}"/>' + ''.join(f'<circle cx="7.5" cy="{y}" r="1.2" fill="{D}"/><rect x="10.5" y="{y-0.8}" width="10" height="1.6" rx=".8" fill="{D}"/>' for y in (10, 15, 20)) + f'<path d="M19.5 29l1-4.2 7-7 3.2 3.2-7 7z" fill="{W}" stroke="{D}" stroke-width="1"/>',
 "wallet": f'<path d="M7 8.5l13.5-4.2 1.6 4.2z" fill="{M}"/><rect x="3" y="8" width="26" height="19" rx="3" fill="{G}"/><rect x="17" y="13.5" width="12" height="8" rx="2" fill="{D}" opacity=".55"/><circle cx="21.2" cy="17.5" r="1.6" fill="{G}"/>',
 "drive": f'<rect x="3" y="8" width="26" height="16" rx="3" fill="{G}"/><rect x="6" y="12" width="10" height="4" rx="1" fill="{D}"/><rect x="17" y="12" width="5" height="4" rx="1" fill="{D}" opacity=".5"/><circle cx="24.5" cy="19.5" r="1.3" fill="{D}"/>' + st("M6 20.5h9", 1.4),
 "smiley": f'<circle cx="16" cy="16" r="12.8" fill="{G}"/><circle cx="11.8" cy="13" r="1.7" fill="{D}"/><circle cx="20.2" cy="13" r="1.7" fill="{D}"/>' + st("M10.3 18.5a6.2 6.2 0 0 0 11.4 0", 2),
 "screenshot": st("M4 11V6.5A2.5 2.5 0 0 1 6.5 4H11M21 4h4.5A2.5 2.5 0 0 1 28 6.5V11M28 21v4.5a2.5 2.5 0 0 1-2.5 2.5H21M11 28H6.5A2.5 2.5 0 0 1 4 25.5V21", 3, G) + f'<circle cx="16" cy="16" r="5" fill="{G}"/><circle cx="16" cy="16" r="2.1" fill="{D}"/>',
 "key": f'<circle cx="10.5" cy="16" r="5.6" fill="none" stroke="{G}" stroke-width="3.4"/><rect x="15.5" y="14.3" width="13" height="3.4" rx="1.2" fill="{G}"/><rect x="21.5" y="17" width="2.8" height="4.2" rx=".8" fill="{G}"/><rect x="25.5" y="17" width="2.8" height="5.6" rx=".8" fill="{G}"/>',
 "mail": f'<rect x="3" y="7" width="26" height="18" rx="3" fill="{G}"/>' + st("M4.8 9.3l11.2 8.2 11.2-8.2", 1.9),
 "sliders-h": st("M5 9h22M5 16h22M5 23h22", 2.2, G) + ''.join(f'<circle cx="{x}" cy="{y}" r="3.1" fill="{W}" stroke="{D}" stroke-width="1.2"/>' for x, y in ((11, 9), (21, 16), (14.5, 23))),
 "sliders-v": st("M9 5v22M16 5v22M23 5v22", 2.2, G) + ''.join(f'<rect x="{x-3}" y="{y-2}" width="6" height="4" rx="1.2" fill="{W}" stroke="{D}" stroke-width="1.2"/>' for x, y in ((9, 19), (16, 10), (23, 15))),
 "knobs": f'<circle cx="10" cy="11.5" r="6.5" fill="{G}"/><circle cx="22" cy="20.5" r="6.5" fill="{G}"/>' + st("M10 11.5l-2.8-3.6M22 20.5l3.6-2.8", 1.9),
 "speaker": f'<polygon points="4,12 9.5,12 16,6.5 16,25.5 9.5,20 4,20" fill="{G}" stroke="{G}" stroke-width="1.2" stroke-linejoin="round"/>' + st("M20 12a5.5 5.5 0 0 1 0 8M23.5 8.5a10.5 10.5 0 0 1 0 15", 2.4, G),
 "nodes": st("M16 16L8 8M16 16l8-8M16 16v8.5", 2.2, G) + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{G}"/>' for x, y, r in ((8, 8, 3.6), (24, 8, 3.6), (16, 25, 3.6), (16, 16, 4.6))) + f'<circle cx="16" cy="16" r="1.8" fill="{D}"/>',
 "gamepad": f'<path d="M9.5 9.5h13a7 7 0 0 1 6.6 9.2l-1.5 4.7a3.5 3.5 0 0 1-5.8 1.4L18.6 22h-5.2l-3.2 2.8a3.5 3.5 0 0 1-5.8-1.4l-1.5-4.7A7 7 0 0 1 9.5 9.5z" fill="{G}"/>' + f'<rect x="8.6" y="12.2" width="2.4" height="7" rx=".8" fill="{D}"/><rect x="6.3" y="14.5" width="7" height="2.4" rx=".8" fill="{D}"/><circle cx="21.5" cy="13.6" r="1.4" fill="{D}"/><circle cx="24.5" cy="16.4" r="1.4" fill="{D}"/>',
 "remote": f'<rect x="3" y="4" width="26" height="18" rx="2.5" fill="{G}"/><rect x="13" y="22" width="6" height="3.6" fill="{G}"/><rect x="9" y="25.5" width="14" height="2.6" rx="1.3" fill="{G}"/>' + st("M9 10.5h12M18 7.5l3 3-3 3M23 15.5H11M14 12.5l-3 3 3 3", 1.8),
 "tiles": ''.join(f'<rect x="{3+i*9.35:.2f}" y="{3+j*9.35:.2f}" width="7.3" height="7.3" rx="2" fill="#e8e8e8"/>' for i in range(3) for j in range(3)),
}

APPS = {
 "Alacritty": "terminal", "utilities-terminal": "terminal", "org.kde.konsole": "terminal",
 "micro": "terminal-cursor", "gvim": "code", "vim": "code",
 "cachy-update-blue": "update", "assistant": "help-book",
 "btop": "bars", "utilities-system-monitor": "activity", "org.kde.plasma-systemmonitor": "activity",
 "btrfs-assistant": "layers", "LimineSnapperSync": "restore",
 "org.cachyos.hello": "welcome", "cachyos-pi": "package", "shelly": "bag",
 "Nextcloud": "cloud", "nextcloud": "cloud", "designer": "layout", "linguist": "translate",
 "firefox": "compass", "vivaldi": "globe", "internet-web-browser": "globe",
 "io.github.thetumultuousunicornofdarkness.cpu-x": "chip", "cpu-x": "chip",
 "preferences-system": "gear", "systemsettings": "gear", "nvidia-settings": "gpu",
 "hwloc": "tree", "mpv": "play-circle", "haruna": "play-rect", "vlc": "clapper",
 "qvidcap": "camera", "qv4l2": "webcam", "neonote": "note",
 "org.cachyos.KernelManager": "kernel", "org.cachyos.scx-manager": "gauge",
 "org.gnome.Meld": "diff", "ark": "archive", "org.kde.ark": "archive",
 "org.kde.dolphin": "folder", "system-file-manager": "folder", "filelight": "pie", "gwenview": "image",
 "kate": "pen-page", "kwrite": "text-page", "accessories-calculator": "calculator",
 "kdeconnect": "phone", "hwinfo": "info", "kmenuedit": "menu-edit", "kwalletmanager": "wallet",
 "partitionmanager": "drive", "preferences-desktop-emoticons": "smiley", "spectacle": "screenshot",
 "keepassxc": "key", "org.mozilla.Thunderbird": "mail", "thunderbird": "mail",
 "org.pulseaudio.pavucontrol": "sliders-h", "qasmixer": "sliders-v", "qashctl": "knobs", "qasconfig": "speaker",
 "qdbusviewer": "nodes", "steam": "gamepad", "hoptodesk": "remote",
}
PLACES = {"start-here": "tiles", "start-here-kde": "tiles", "start-here-kde-symbolic": "tiles", "start-here-kde-plasma": "tiles"}

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for sub, table in (("apps", APPS), ("places", PLACES)):
        d = OUT / "scalable" / sub
        d.mkdir(parents=True)
        for name, glyph in table.items():
            (d / f"{name}.svg").write_text(svg(GLYPHS[glyph]))
    (OUT / "index.theme").write_text(f"""[Icon Theme]
Name=Neo11 Silber
Comment=Weiß-silberne Programmsymbole passend zu Neo11Menu (Symbolgröße {PERCENT:.0f} %)
Inherits=breeze-dark,breeze,hicolor
Example=folder
DisplayDepth=32
Directories=scalable/apps,scalable/places

[scalable/apps]
Size=48
MinSize=8
MaxSize=512
Type=Scalable
Context=Applications

[scalable/places]
Size=48
MinSize=8
MaxSize=512
Type=Scalable
Context=Places
""")
    print(f"{len(APPS) + len(PLACES)} Symbole aus {len(GLYPHS)} Motiven erzeugt ({PERCENT:.0f} %).")

if __name__ == "__main__":
    main()
