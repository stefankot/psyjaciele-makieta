# generated: psyjaciele-podstrony
"""nbsp.py — typografia polska: twarda spacja po jednoliterowych spójnikach i przyimkach (a, i, o, u, w, z) oraz przed pauzą;
adresy e-mail w tekście owijane w <span class="nohy"> (CSS wyłącza w nich dzielenie wyrazów: kontakt@psy-jacielevet.pl);
zwykła spacja przed strzałką linku (<span class="type-arrow …">) znika, a strzałka dostaje klasę is-after-text (odstęp robi margines, więc podkreślenie nie obejmuje spacji).

Żaden wiersz nie kończy się na „w”, „z”, „i” … ani nie zaczyna od „—”. Działa tylko na tekście w <body> (pomija skrypty, style, SVG,
atrybuty, komentarze). Idempotentne: zamienia wyłącznie zwykłą spację, istniejące &nbsp; zostają.
Użycie jako moduł: fix(html) → html; jako skrypt: python3 nbsp.py plik.html […] (nadpisuje pliki; na Home po ręcznych zmianach tekstu).
"""
import re
import sys

TOKEN = re.compile(r'(<!--.*?-->|<[^>]+>)', re.S)
SKIP = {'script', 'style', 'svg', 'title', 'noscript', 'textarea', 'option', 'head'}
# jednoliterowe słowo (nie część dłuższego), po nim zwykła spacja
ONE = re.compile(r'(?<![\wÀ-ſ])([aiouwzAIOUWZ]) ')
# spacja przed pauzą/półpauzą otoczoną spacjami
DASH = re.compile(r' ([—–])(?= )')
EMAIL = re.compile(r'(?<![\w.@-])([\w.+-]+@[\w-]+(?:\.[\w-]+)+)')
ARROW = re.compile(r'[ \t\r\n]+<span class="type-arrow ')
OLDMAIL = re.compile(r'<span class="nohy">(.*?)</span>', re.S)


def _fix_text(t: str) -> str:
    t = ONE.sub(r'\1&nbsp;', t)
    t = ONE.sub(r'\1&nbsp;', t)     # „w i z” — drugi przebieg łapie sąsiednie jednoliterówki
    t = DASH.sub(r'&nbsp;\1', t)
    return EMAIL.sub(r'<span class="nohy">\1</span>', t)


def fix(html: str) -> str:
    html = OLDMAIL.sub(r'\1', html)
    i = html.find('<body')
    head, body = (html[:i], html[i:]) if i >= 0 else ('', html)
    body = ARROW.sub('<span class="type-arrow is-after-text ', body)
    depth = {}
    out = []
    for tok in TOKEN.split(body):
        if not tok:
            continue
        if tok.startswith('<'):
            m = re.match(r'<(/?)([a-zA-Z][a-zA-Z0-9:-]*)', tok)
            if m and m.group(2).lower() in SKIP and not tok.endswith('/>'):
                name = m.group(2).lower()
                depth[name] = depth.get(name, 0) + (-1 if m.group(1) else 1)
            out.append(tok)
        elif any(v > 0 for v in depth.values()):
            out.append(tok)
        else:
            out.append(_fix_text(tok))
    return head + ''.join(out)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read()
        n = fix(s)
        if n != s:
            open(p, 'w', encoding='utf-8').write(n)
        print(('zmieniono ' if n != s else 'bez zmian ') + p, n.count('&nbsp;') - s.count('&nbsp;'))
