#!/usr/bin/env python3
"""Erzeugt das Mauszeiger-Theme „Neo11 Zeiger“ (Xcursor) aus SVG-Motiven.
Benötigt nur Python 3 und rsvg-convert. Aufruf: python3 zeiger/tools/generate_cursors.py"""
import io, math, os, pathlib, shutil, struct, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "Neo11-Zeiger"
SIZES = (24, 32, 48, 64, 96)
FILL = "url(#f)"

HEAD = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
<defs>
<linearGradient id="f" gradientUnits="userSpaceOnUse" x1="0" y1="3" x2="0" y2="29"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d2d2d2"/></linearGradient>
<filter id="s" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="1.1"/><feComponentTransfer><feFuncA type="linear" slope="1.25"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g filter="url(#s)">'''
TAIL = '</g></svg>'

def P(d, fill=FILL, rule=""):
    r = f' fill-rule="{rule}"' if rule else ""
    return f'<path d="{d}" fill="{fill}"{r} stroke="#3a3a3a" stroke-width=".35" stroke-linejoin="round"/>'

DART = "M5 3.5L25.5 15.2 15.6 16.9 9.9 27z"
def dart_small():
    return P(DART)

def badge(inner):
    return f'<g transform="translate(18.5 18.5)"><circle cx="5" cy="5" r="5.2" fill="{FILL}" stroke="#3a3a3a" stroke-width=".35"/>{inner}</g>'

def spinner(angle, cx=16, cy=16, r=10.5, scale=1.0):
    a = angle
    def quad(start):
        s = math.radians(start); e = math.radians(start + 90)
        x1, y1 = cx + r * math.cos(s), cy + r * math.sin(s)
        x2, y2 = cx + r * math.cos(e), cy + r * math.sin(e)
        return f"M{cx} {cy}L{x1:.2f} {y1:.2f}A{r} {r} 0 0 1 {x2:.2f} {y2:.2f}z"
    return P(quad(a) + quad(a + 180))

HAND = ("M11 15.6V5.6a2 2 0 0 1 4 0v7.2h.6V10.6a1.9 1.9 0 0 1 3.8 0v2.4h.6v-1.3a1.8 1.8 0 0 1 3.6 0v1.9h.5v-.7a1.7 1.7 0 0 1 3.4 0v6.8"
        "c0 4.6-3 7.9-7.6 7.9h-2c-2.5 0-4.2-1-5.5-3l-4.1-6.1a2 2 0 0 1 3.2-2.4z")
FIST = ("M9.5 13.5a1.9 1.9 0 0 1 3.4-1.2v-.6a1.9 1.9 0 0 1 3.8 0v.4a1.9 1.9 0 0 1 3.6.3v.3a1.8 1.8 0 0 1 3.5.6v6.4"
        "c0 4.6-3 7.9-7.6 7.9h-2c-2.5 0-4.2-1-5.5-3l-1.2-1.9z")

def ring_slash():
    return P("M16 4a12 12 0 1 1 0 24 12 12 0 0 1 0-24zM16 8a8 8 0 0 0-6.4 12.8L20.8 9.6A8 8 0 0 0 16 8zm6.4 3.2L11.2 22.4A8 8 0 0 0 22.4 11.2z", rule="evenodd")

def magnifier(minus=False):
    plus = "" if minus else '<rect x="12.2" y="7.2" width="1.8" height="7.6" rx=".6" fill="#3a3a3a"/>'
    return (P("M13 2.8a8.2 8.2 0 1 1 0 16.4 8.2 8.2 0 0 1 0-16.4zm0 2.8a5.4 5.4 0 1 0 0 10.8 5.4 5.4 0 0 0 0-10.8z", rule="evenodd")
            + P("M18.6 17.3l2.1-2.1 8 8a1.5 1.5 0 0 1 0 2.1l-.1.1a1.5 1.5 0 0 1-2.1 0z")
            + f'<rect x="9.3" y="10.1" width="7.6" height="1.8" rx=".6" fill="#3a3a3a"/>' + plus)

# name: (svg-body or list of frames, hotspot x, y in 32er-Raster, delay ms)
def cursors():
    c = {}
    c["default"] = (P(DART), 5, 3.5)
    c["help"] = (P(DART) + badge('<path d="M3.4 3.9a1.7 1.7 0 1 1 2.4 1.5c-.6.3-.9.7-.9 1.3v.2" fill="none" stroke="#3a3a3a" stroke-width="1.1" stroke-linecap="round"/><circle cx="4.9" cy="8.3" r=".6" fill="#3a3a3a"/>'), 5, 3.5)
    c["copy"] = (P(DART) + badge('<path d="M5 2.4v5.2M2.4 5h5.2" stroke="#3a3a3a" stroke-width="1.3" stroke-linecap="round"/>'), 5, 3.5)
    c["alias"] = (P(DART) + badge('<path d="M3 7.4C3 4.6 4.6 3.4 7 3.4M5.6 1.9L7.2 3.4 5.6 4.9" fill="none" stroke="#3a3a3a" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>'), 5, 3.5)
    c["context-menu"] = (P(DART) + '<g transform="translate(18 17)"><rect x="0" y="0" width="10" height="11" rx="1.4" fill="url(#f)" stroke="#3a3a3a" stroke-width=".35"/><path d="M2.2 3h5.6M2.2 5.5h5.6M2.2 8h5.6" stroke="#3a3a3a" stroke-width=".9" stroke-linecap="round"/></g>', 5, 3.5)
    c["wait"] = ([spinner(a) for a in range(0, 360, 30)], 16, 16, 60)
    c["progress"] = ([P(DART) + f'<g transform="translate(14.5 14.5) scale(.5)">{spinner(a)}</g>' for a in range(0, 360, 30)], 5, 3.5, 60)
    c["pointer"] = (P(HAND), 13, 3.6)
    c["grab"] = (P(HAND), 16, 12)
    c["grabbing"] = (P(FIST), 16, 14)
    c["text"] = (P("M11 3.5h3.6l1.4 1.2 1.4-1.2H21v2.6h-3.4v19.8H21v2.6h-3.6L16 27.3l-1.4 1.2H11v-2.6h3.4V6.1H11z"), 16, 16)
    c["vertical-text"] = (P("M3.5 21V17.4l1.2-1.4-1.2-1.4V11h2.6v3.4h19.8V11h2.6v3.6L27.3 16l1.2 1.4V21h-2.6v-3.4H6.1V21z"), 16, 16)
    c["crosshair"] = (P("M15 3h2v10h-2zM15 19h2v10h-2zM3 15h10v2H3zM19 15h10v2H19z"), 16, 16)
    c["cell"] = (P("M13.5 4h5v9.5H28v5h-9.5V28h-5v-9.5H4v-5h9.5z"), 16, 16)
    c["not-allowed"] = (ring_slash(), 16, 16)
    c["move"] = (P("M16 3l13 13-13 13L3 16z") + '<circle cx="16" cy="16" r="2" fill="#3a3a3a"/>', 16, 16)
    c["ns-resize"] = (P("M16 3.5l9.5 9.5h-19zM6.5 19h19L16 28.5z"), 16, 16)
    c["ew-resize"] = (P("M3.5 16l9.5-9.5v19zM19 6.5L28.5 16 19 25.5z"), 16, 16)
    c["nwse-resize"] = (P("M5 5h19L5 24zM27 8v19H8z"), 16, 16)
    c["nesw-resize"] = (P("M8 5h19v19zM5 8l19 19H5z"), 16, 16)
    c["zoom-in"] = (magnifier(False), 13, 11)
    c["zoom-out"] = (magnifier(True), 13, 11)
    return c

ALIASES = {
 "default": ["left_ptr", "arrow", "top_left_arrow", "left_arrow", "right_ptr", "draft_large", "draft_small"],
 "help": ["question_arrow", "whats_this", "left_ptr_help", "dnd-ask", "5c6cd98b3f3ebcb1f9c7f1c204630408", "d9ce0ab605698f320427677b458ad60b"],
 "copy": ["dnd-copy", "1081e37283d90000800003c07f3ef6bf", "6407b0e94181790501fd1e167b474872", "b66166c04f8c3109214a4fbd64a50fc8"],
 "alias": ["link", "dnd-link", "3085a0e285430894940527032f8b26df", "640fb0e74195791501fd1ed57b41487f", "a2a266d0498c3104214a47bd64ab0fc8"],
 "context-menu": [],
 "wait": ["watch", "0426c94ea35c87780ff01dc239897213"],
 "progress": ["left_ptr_watch", "half-busy", "00000000000000020006000e7e9ffc3f", "08e8e1c95fe2fc01f976f1e063a24ccd", "3ecb610c1bf2410f44200f48c40d3599"],
 "pointer": ["hand1", "hand2", "hand", "pointing_hand", "e29285e634086352946a0e7090d73106", "9d800788f1b08800ae810202380a0822"],
 "grab": ["openhand", "9141b49c8149039304290b508d208c40", "5aca4d189052212118709018842178c0"],
 "grabbing": ["closedhand", "dnd-none", "fcf21c00b30f7e3f83fe0dfd12e71cff", "208530c400c041818281048008011002"],
 "text": ["xterm", "ibeam"],
 "vertical-text": [],
 "crosshair": ["cross", "tcross", "cross_reverse", "diamond_cross", "target"],
 "cell": ["plus"],
 "not-allowed": ["no-drop", "forbidden", "circle", "crossed_circle", "dnd-no-drop", "03b6e0fcb3499374a867c041f52298f0"],
 "move": ["fleur", "all-scroll", "size_all", "dnd-move", "4498f0e0c1937ffe01fd06f973665830", "9081237383d90e509aa00f00170e968f"],
 "ns-resize": ["row-resize", "n-resize", "s-resize", "size_ver", "v_double_arrow", "sb_v_double_arrow", "top_side", "bottom_side", "split_v",
               "00008160000006810000408080010102", "2870a09082c103050810ffdffffe0204", "double_arrow", "up_arrow", "down_arrow"],
 "ew-resize": ["col-resize", "e-resize", "w-resize", "size_hor", "h_double_arrow", "sb_h_double_arrow", "left_side", "right_side", "split_h",
               "028006030e0e7ebffc7f7070c0600140", "14fef782d02440884392942c11205230"],
 "nwse-resize": ["nw-resize", "se-resize", "size_fdiag", "bd_double_arrow", "top_left_corner", "bottom_right_corner", "c7088f0f3e6c8088236ef8e1e3e70000"],
 "nesw-resize": ["ne-resize", "sw-resize", "size_bdiag", "fd_double_arrow", "top_right_corner", "bottom_left_corner", "fcf1c3c7cd4491d801f1e1c78f100000"],
 "zoom-in": [], "zoom-out": [],
}

def render(svg_text, px, tmp):
    src = tmp / "c.svg"; dst = tmp / "c.png"
    src.write_text(HEAD + svg_text + TAIL)
    subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px), str(src), "-o", str(dst)], check=True)
    return dst.read_bytes()

def png_to_argb(png):
    # minimaler PNG-Leser (8-bit RGBA, nicht interlaced) – rsvg-convert liefert genau das
    import zlib
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, w = 8, b"", 0
    while pos < len(png):
        ln = struct.unpack(">I", png[pos:pos+4])[0]; typ = png[pos+4:pos+8]; data = png[pos+8:pos+8+ln]
        if typ == b"IHDR":
            w, h, bd, ct = struct.unpack(">IIBB", data[:10]); assert bd == 8 and ct == 6
        elif typ == b"IDAT":
            idat += data
        pos += 12 + ln
    raw = zlib.decompress(idat); stride = w * 4; out = bytearray(); prev = bytearray(stride)
    i = 0
    for _ in range(h):
        f = raw[i]; line = bytearray(raw[i+1:i+1+stride]); i += 1 + stride
        for x in range(stride):
            a = line[x-4] if x >= 4 else 0; b = prev[x]; c = prev[x-4] if x >= 4 else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif f == 4:
                p = a + b - c; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line
        for x in range(0, stride, 4):
            r, g, bl, al = line[x:x+4]
            out += struct.pack("<I", (al << 24) | ((r * al // 255) << 16) | ((g * al // 255) << 8) | (bl * al // 255))
    return w, h, bytes(out)

def write_xcursor(path, images):
    # images: Liste (nominal, w, h, xhot, yhot, delay, pixels)
    ntoc = len(images)
    header = struct.pack("<4sIII", b"Xcur", 16, 0x10000, ntoc)
    pos = 16 + ntoc * 12; toc = b""; chunks = b""
    for nom, w, h, xh, yh, dl, px in images:
        chunk = struct.pack("<IIIIIIIII", 36, 0xfffd0002, nom, 1, w, h, xh, yh, dl) + px
        toc += struct.pack("<III", 0xfffd0002, nom, pos)
        pos += len(chunk); chunks += chunk
    path.write_bytes(header + toc + chunks)

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    cdir = OUT / "cursors"; cdir.mkdir(parents=True)
    tmp = pathlib.Path(tempfile.mkdtemp())
    for name, spec in cursors().items():
        body, hx, hy = spec[0], spec[1], spec[2]
        delay = spec[3] if len(spec) > 3 else 0
        frames = body if isinstance(body, list) else [body]
        images = []
        for px in SIZES:
            for fr in frames:
                w, h, pix = png_to_argb(render(fr, px, tmp))
                images.append((px, w, h, round(hx * px / 32), round(hy * px / 32), delay, pix))
        write_xcursor(cdir / name, images)
        for al in ALIASES.get(name, []):
            (cdir / al).symlink_to(name)
    shutil.rmtree(tmp)
    (OUT / "index.theme").write_text("[Icon Theme]\nName=Neo11 Zeiger\nComment=Silberne Mauszeiger passend zu Neo11 Silber\nInherits=breeze_cursors\n")
    (OUT / "cursor.theme").write_text("[Icon Theme]\nName=Neo11 Zeiger\nInherits=breeze_cursors\n")
    print(f"{len(cursors())} Zeiger, {sum(len(v) for v in ALIASES.values())} Aliasnamen erzeugt.")

if __name__ == "__main__":
    main()
