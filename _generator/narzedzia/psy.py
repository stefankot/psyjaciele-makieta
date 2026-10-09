# generated: psyjaciele-podstrony
"""psy.py — owija słowo „Psyjaciele” (i formy: Psyjaciół, Psyjaciołach, psyjaciel, psyjaciela …) w <span class="psy">.

Krój Rialto, rozmiar i grubość kreski ustawia CSS (.psy w layout-nowa.css). Pomija: <head>, skrypty, style, SVG, atrybuty,
adresy i e-maile (psyjacielevet). Idempotentne: istniejące znaczniki są najpierw zdejmowane.
Użycie jako moduł: wrap(html) → html; jako skrypt: python3 psy.py plik.html […] (nadpisuje pliki).
"""
import re
import sys

TOKEN = re.compile(r'(<!--.*?-->|<[^>]+>)', re.S)
SKIP = {'script', 'style', 'svg', 'title', 'noscript', 'textarea', 'option', 'head'}
WORD = re.compile(r'(?<![\w@/.#=%-])([Pp]syjaci[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]*)')
OLD = re.compile(r'<span class="psy">(.*?)</span>', re.S)


def _word(m):
    w = m.group(1)
    if w.lower().endswith('vet'):
        return w
    return f'<span class="psy">{w}</span>'


def wrap(html: str) -> str:
    html = OLD.sub(r'\1', html)
    i = html.find('<body')
    head, body = (html[:i], html[i:]) if i >= 0 else ('', html)
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
            out.append(WORD.sub(_word, tok))
    return head + ''.join(out)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read()
        n = wrap(s)
        if n != s:
            open(p, 'w', encoding='utf-8').write(n)
        print(('zmieniono ' if n != s else 'bez zmian ') + p, n.count('class="psy"'))
