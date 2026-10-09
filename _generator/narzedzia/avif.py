#!/usr/bin/env python3
"""avif.py — konwersja obrazów użytych na stronie do AVIF (lokalnie, avifenc).
Ilustracje: jakość 50, zdjęcia: jakość 60 (kanał alfa 90). Oryginały zostają obok (są wejściem dla narzędzi generujących ilustracje).
Użycie (z katalogu makiety):  python3 _generator/narzedzia/avif.py [--dry]
Potem pliki .avif są podpinane w HTML/CSS/JS przez avif_podmien.py (lub ręcznie)."""
import glob, os, re, subprocess, sys

DRY = '--dry' in sys.argv
PHOTO_NAMES = re.compile(r'(studio-|booking-dog|follow-cat|ola-magda|pets-phone-atlas|join-pacjenci)')
SRC_GLOBS = ['index.html', 'uslugi-weterynaryjne/**/index.html', 'zespol/index.html', 'polityka-prywatnosci/index.html', '*.css', '*.js']
PAT = re.compile(r'assets/[A-Za-z0-9_\-./%]+?\.(?:png|jpe?g|webp)\b', re.I)


def used():
    refs = set()
    for g in SRC_GLOBS:
        for f in glob.glob(g, recursive=True):
            refs |= set(PAT.findall(open(f, encoding='utf8').read()))
    # nazwy bez prefiksu assets/ (np. w pet-photos.js)
    for f in glob.glob('*.js') + glob.glob('*.css'):
        t = open(f, encoding='utf8').read()
        for m in re.findall(r"['\"`(/]([A-Za-z0-9_\-]+\.(?:png|jpe?g|webp))\b", t):
            refs |= set(glob.glob('assets/**/' + m, recursive=True))
    # odwołania do .avif (po podmianie w kodzie) liczą się jako użycie oryginału o tej samej nazwie
    avif_pat = re.compile(r'assets/[A-Za-z0-9_\-./%]+?\.avif\b', re.I)
    for g in SRC_GLOBS:
        for f in glob.glob(g, recursive=True):
            for a in avif_pat.findall(open(f, encoding='utf8').read()):
                for ext in ('png', 'jpg', 'jpeg', 'webp'):
                    o = re.sub(r'\.avif$', '.' + ext, a, flags=re.I)
                    if os.path.exists(o):
                        refs.add(o)
    for f in glob.glob('*.js') + glob.glob('*.css'):
        for m in re.findall(r"['\"`(/]([A-Za-z0-9_\-]+)\.avif\b", open(f, encoding='utf8').read()):
            for ext in ('png', 'jpg', 'jpeg', 'webp'):
                refs |= set(glob.glob('assets/**/' + m + '.' + ext, recursive=True))
    return sorted(r for r in refs if os.path.exists(r))


def kind(path):
    if re.search(r'\.jpe?g$', path, re.I) or PHOTO_NAMES.search(os.path.basename(path)):
        return 'zdjęcie', 60
    return 'ilustracja', 50


def main():
    tot_in = tot_out = 0
    for p in used():
        k, q = kind(p)
        out = re.sub(r'\.(png|jpe?g|webp)$', '.avif', p, flags=re.I)
        if not DRY:
            src, tmp = p, None
            if p.lower().endswith('.webp'):   # avifenc nie czyta WebP — przez tymczasowy PNG
                tmp = out + '.tmp.png'
                subprocess.run(['magick', p, tmp], check=True)
                src = tmp
            subprocess.run(['avifenc', '-q', str(q), '--qalpha', '90', '-s', '0', '-j', 'all', src, out], check=True, capture_output=True)
            if tmp:
                os.remove(tmp)
        a, b = os.path.getsize(p), (os.path.getsize(out) if os.path.exists(out) else 0)
        tot_in += a; tot_out += b
        print(f'{k:10} q{q}  {a // 1024:6} KB → {b // 1024:6} KB  {p}')
    print(f'RAZEM: {tot_in // 1024} KB → {tot_out // 1024} KB')


if __name__ == '__main__':
    main()
