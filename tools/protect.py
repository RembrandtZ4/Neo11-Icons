#!/usr/bin/env python3
"""Schützt Original-Symbole vor ungewollter Übernahme.

KDE sucht ein fehlendes Symbol zuerst im aktiven Theme und kürzt den Namen dabei
schrittweise („audio-volume-low-symbolic“ → … → „audio“ → „audio-x-generic“).
Hat Neo11 Silber so einen gekürzten Namen, gewinnt es – obwohl das Basis-Theme
das exakte Symbol hätte. Dieses Skript legt für alle betroffenen Namen
Verknüpfungen auf die Originale ins Theme, damit der exakte Name zuerst gefunden wird.

Aufruf: python3 tools/protect.py <installiertes Neo11-Theme> [Basis-Theme …]
"""
import configparser, os, pathlib, sys

MEDIA_TYPES = {"text", "application", "image", "audio", "inode", "video", "message",
               "model", "multipart", "x-content", "x-epoc"}
EXTS = (".svg", ".svgz", ".png")


def fallback_chain(name):
    """Nachbau von KIconLoaderPrivate::findMatchingIcon (ohne den exakten Namen)."""
    out = []
    generic = name.endswith("-x-generic")
    symbolic = name.endswith("-symbolic")
    cur = name
    first = True
    while cur:
        if not first:
            out.append(cur)
        first = False
        if generic:
            break
        if symbolic:
            cur = cur[: -len("-symbolic")]
            out.append(cur)
        r = cur.rfind("-")
        if r > 1:
            cur = cur[:r]
            if cur.endswith("-x"):
                cur = cur[:-2]
            if symbolic:
                cur += "-symbolic"
        else:
            if cur in MEDIA_TYPES:
                cur += "-x-generic"
                generic = True
            else:
                break
    return out


def theme_dirs(theme_path):
    cp = configparser.ConfigParser(interpolation=None, strict=False)
    cp.optionxform = str
    cp.read(theme_path / "index.theme", encoding="utf-8")
    dirs = [d for d in cp.get("Icon Theme", "Directories", fallback="").split(",") if d]
    dirs += [d for d in cp.get("Icon Theme", "ScaledDirectories", fallback="").split(",") if d]
    return cp, dirs


def find_theme(name):
    for base in (pathlib.Path.home() / ".local/share/icons", pathlib.Path("/usr/share/icons")):
        p = base / name
        if (p / "index.theme").exists():
            return p
    return None


def main():
    ours = pathlib.Path(sys.argv[1])
    bases = sys.argv[2:] or ["breeze-dark", "breeze"]

    own_names = set()
    for f in ours.rglob("*"):
        if f.suffix in EXTS and not f.is_symlink():
            own_names.add(f.stem)

    cp_ours, our_dirs = theme_dirs(ours)
    added_dirs = {}
    seen = set(own_names)
    count = 0

    for base_name in bases:
        base = find_theme(base_name)
        if not base:
            continue
        cp_base, dirs = theme_dirs(base)
        for d in dirs:
            src_dir = base / d
            if not src_dir.is_dir() or not cp_base.has_section(d):
                continue
            for f in src_dir.iterdir():
                if f.suffix not in EXTS:
                    continue
                stem = f.stem
                if stem in own_names:
                    continue
                if not any(c in own_names for c in fallback_chain(stem)):
                    continue
                key = (stem, d)
                if key in seen:
                    continue
                seen.add(key)
                target_dir = ours / "schutz" / base_name / d
                target_dir.mkdir(parents=True, exist_ok=True)
                link = target_dir / f.name
                if not link.exists():
                    os.symlink(f.resolve(), link)
                    count += 1
                added_dirs[f"schutz/{base_name}/{d}"] = dict(cp_base.items(d))

    if added_dirs:
        for d, props in added_dirs.items():
            if not cp_ours.has_section(d):
                cp_ours.add_section(d)
                for k, v in props.items():
                    cp_ours.set(d, k, v)
        all_dirs = our_dirs + [d for d in added_dirs if d not in our_dirs]
        cp_ours.set("Icon Theme", "Directories", ",".join(all_dirs))
        if cp_ours.has_option("Icon Theme", "ScaledDirectories"):
            cp_ours.remove_option("Icon Theme", "ScaledDirectories")
        with open(ours / "index.theme", "w", encoding="utf-8") as fh:
            cp_ours.write(fh, space_around_delimiters=False)

    print(f"{count} Original-Symbole geschützt.")


if __name__ == "__main__":
    main()
