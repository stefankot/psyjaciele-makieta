# generated: psyjaciele-podstrony
"""typo.py — typografia tekstu z biblioteki typografia-www, stosowana w buildzie (jak nbsp.py, tylko szerzej).

Co robi (na tekście w <body>; pomija script, style, svg, title, code, pre, atrybuty, komentarze, fragmenty z data-notp):
  1. Reguły P2 z biblioteki: uruchamia oryginalne tp() z `typo-biblioteka.js` (kopia typografia-www/skill/typografia-tekst/typo.js,
     commit ce97dd3), więc jedno źródło prawdy: cudzysłowy „…” i «…», apostrof, półpauza we wtrąceniach (K-01), zakresy, wielokropek,
     ×, −, ½, °C, spójniki jednoliterowe, inicjały, grupowanie cyfr, czyszczenie spacji. Stan cudzysłowów jest osobny w każdym bloku.
  2. P2-12: ostatni wyraz (do 4 znaków) ostatniego akapitu/pozycji listy/podpisu przyklejony twardą spacją (bez „wdowy wyrazowej”).
  3. Uzupełnienia z katalogu biblioteki, których tp() nie robi (M-113: krótkie wyrażenia liczbowe łącz twardą spacją; M-59: grupy cyfr):
     liczba + jednostka (30 dni, 8. tygodnia), skrót + wyraz (ul. Celownicza, lek. wet. Aleksandra), ulica + numer, kod + miasto,
     numer telefonu w jednym kawałku.
  4. Normalizacja: pauza „—” (i półpauza) we wtrąceniach → twarda spacja + „–” ze spacją po (K-01). Samotne „—” (brak danych) zostaje.

Wyjątki celowe: grupowanie cyfr (P2-09) nie dotyka identyfikatorów (ISO 11784, NIP, REGON, KRS, adresy URL), bo to nie liczby do czytania.
Wymaga Node.js (tp() jest w JS). Idempotentne. Użycie jako moduł: fix(html) → html; jako skrypt: python3 typo.py plik.html […]
(nadpisuje pliki; na Home po ręcznych zmianach tekstu) albo `--raport plik.html` (tylko liczby, bez zapisu).
"""
import html as _html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r'(<!--.*?-->|<[^>]+>)', re.S)
OPEN = re.compile(r'<([a-zA-Z][a-zA-Z0-9:-]*)\b([^>]*)>', re.S)
CLOSE = re.compile(r'</([a-zA-Z][a-zA-Z0-9:-]*)\s*>')
SKIP = {'script', 'style', 'svg', 'title', 'noscript', 'textarea', 'option', 'select', 'head',
        'code', 'pre', 'kbd', 'samp', 'input', 'math'}
BLOCK = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'td', 'th', 'dd', 'dt', 'figcaption', 'blockquote', 'div'}
LAST = {'p', 'li', 'dd', 'figcaption', 'blockquote'}          # P2-12 (jak w typo.js)
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr', 'param'}

NBSP, THIN, NNBSP = ' ', ' ', ' '
PL_UP = 'A-ZĄĆĘŁŃÓŚŹŻ'
PL = 'A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ'
MASK_L, MASK_R = '', ''

# --- uzupełnienia (M-113, M-59) -------------------------------------------------
UNITS = (r'(?:dni|dzień|dnia|dniach|lat|lata|latach|rok|roku|tygodni|tygodnie|tygodnia|tygodniu|tydzień|'
         r'miesiąc|miesiące|miesiąca|miesięcy|godz\.|godzin|godziny|minut|minuty|min|zł|PLN|kg|g|mg|ml|cm|mm|m|km|szt\.|lok\.)')
NUM_UNIT = re.compile(r'(\d\.?) (?=' + UNITS + r'(?![' + PL + r'\d]))')
ABBR = re.compile(r'(?<![' + PL + r'])(ul|al|pl|os|lok|nr|tel|godz|ok|np|tzw|tj|prof|mgr|inż|św|lek|wet)\. (?=\S)')
STREET = re.compile(r'(?<=ul\.' + NBSP + r')((?:[' + PL_UP + r'][^\s\d,.;:]*[ ])*[' + PL_UP + r'][^\s\d,.;:]*) (?=\d)')
ZIP = re.compile(r'(?<![\d-])(\d{2}-\d{3}) (?=[' + PL_UP + r'])')
PHONE = re.compile(r'(?<![\d+])((?:\+\d{2} )?)(\d{3}) (\d{3}) (\d{3})(?!\d)')
DASH = re.compile(r'[ \t ]+[—–][ \t]+(?=\S)|[ \t ]+[—–][ \t]+$')   # „słowo — słowo” oraz pauza ze spacją na końcu węzła (dalej znacznik)
DASH_SP = re.compile(r'[ \t ]+[—–]$')                    # pauza bez spacji po niej na końcu węzła: tylko przed pauzą twarda spacja

# identyfikatory, których nie grupujemy (P2-09 dotyczy liczb do czytania)
ID_LABEL = re.compile(r'(\b(?:ISO|IEC|PN|EN|NIP|REGON|KRS|PESEL)\b[\s :.-]*)(\d{5,})')
ONLY_DIGITS = re.compile(r'^\s*\d{5,}\s*$')
LAST_WORD = re.compile(r'\s(\S{1,4})\s*$')


def _technical(t: str) -> bool:
    """Adresy w tekście (ze znakami zerowej szerokości, ukośnikami) zostają bez zmian."""
    return '​' in t or '://' in t or bool(re.search(r'\S/\S+/\S', t))


def _mask(t: str):
    saved = []

    def keep(m):
        saved.append(m.group(2))
        return m.group(1) + MASK_L + str(len(saved) - 1) + MASK_R

    if ONLY_DIGITS.match(t):
        saved.append(t)
        return MASK_L + '0' + MASK_R, saved
    return ID_LABEL.sub(keep, t), saved


def _unmask(t: str, saved):
    return re.sub(MASK_L + r'(\d+)' + MASK_R, lambda m: saved[int(m.group(1))], t)


def _supplements(t: str, stats: Counter) -> str:
    def sub(rx, rep, name, s):
        def one(m):
            r = rep(m) if callable(rep) else rep
            if r != m.group(0):          # liczymy tylko realne zmiany (idempotencja: drugi przebieg daje 0)
                stats[name] += 1
            return r
        return rx.sub(one, s)

    t = sub(DASH, NBSP + '– ', 'pauza → półpauza', t)
    t = sub(DASH_SP, NBSP + '–', 'pauza → półpauza', t)
    t = sub(ABBR, lambda m: m.group(1) + '.' + NBSP, 'skrót + wyraz', t)
    t = sub(NUM_UNIT, lambda m: m.group(1) + NBSP, 'liczba + jednostka', t)
    t = sub(STREET, lambda m: m.group(1) + NBSP, 'ulica + numer', t)
    t = sub(ZIP, lambda m: m.group(1) + NBSP, 'kod + miasto', t)
    t = sub(PHONE, lambda m: m.group(1).replace(' ', NBSP) + NBSP.join(m.group(2, 3, 4)), 'telefon', t)
    return t


def _enc(s: str) -> str:
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return s.replace(NBSP, '&nbsp;').replace(THIN, '&thinsp;').replace(NNBSP, '&#8239;')


def _tp_batch(items):
    try:
        r = subprocess.run(['node', str(HERE / 'typo_tp.js')], input=json.dumps(items, ensure_ascii=False),
                           capture_output=True, text=True, encoding='utf-8', check=True)
    except FileNotFoundError:
        raise SystemExit('typo.py: brak Node.js (tp() z biblioteki typografia-www jest w JS); zainstaluj Node albo pomiń typo.fix w build.py')
    return json.loads(r.stdout)


def process(html: str, stats: Counter | None = None) -> str:
    stats = stats if stats is not None else Counter()
    i = html.find('<body')
    head, body = (html[:i], html[i:]) if i >= 0 else ('', html)
    tokens = TOKEN.split(body)

    # przebieg 1: które węzły tekstowe wchodzą i w jakim bloku stoją
    stack = []                      # [nazwa, pomiń, klucz bloku]
    nblock = 0
    jobs = []                       # (indeks tokenu, klucz, tekst zamaskowany, maski, ostatnie dziecko bloku?)
    for n, tok in enumerate(tokens):
        if not tok:
            continue
        if tok.startswith('<!--'):
            continue
        if tok.startswith('<'):
            c = CLOSE.match(tok)
            if c:
                name = c.group(1).lower()
                for k in range(len(stack) - 1, -1, -1):
                    if stack[k][0] == name:
                        del stack[k:]
                        break
                continue
            o = OPEN.match(tok)
            if o and not tok.endswith('/>') and o.group(1).lower() not in VOID:
                name = o.group(1).lower()
                parent = stack[-1] if stack else ['', False, 'body']
                key = parent[2]
                if name in BLOCK:
                    nblock += 1
                    key = 'b%d' % nblock
                skip = parent[1] or name in SKIP or 'data-notp' in o.group(2)
                stack.append([name, skip, key])
            continue
        if not tok.strip() or (stack and stack[-1][1]) or any(s[1] for s in stack):
            continue
        text = _html.unescape(tok)
        if _technical(text):
            continue
        masked, saved = _mask(text)
        nxt = tokens[n + 1] if n + 1 < len(tokens) else ''
        cm = CLOSE.match(nxt) if nxt else None
        last = bool(stack and cm and stack[-1][0] in LAST and cm.group(1).lower() == stack[-1][0])
        jobs.append((n, stack[-1][2] if stack else 'body', masked, saved, text, last))

    done = _tp_batch([[j[1], j[2]] for j in jobs]) if jobs else []

    # przebieg 2: uzupełnienia, wdowa wyrazowa, zapis tylko tam, gdzie coś się zmieniło
    for (n, _key, _masked, saved, text, last), out in zip(jobs, done):
        new = _unmask(out, saved)
        if new != text:
            stats['tp() z biblioteki (węzły zmienione)'] += 1
        new = _supplements(new, stats)
        if last:
            w = LAST_WORD.sub(lambda m: NBSP + m.group(1), new)
            if w != new:
                stats['wdowa wyrazowa'] += 1
            new = w
        if new != text:
            tokens[n] = _enc(new)
    return head + ''.join(tokens)


def fix(html: str) -> str:
    return process(html)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--raport' in sys.argv
    total = Counter()
    for p in args:
        s = Path(p).read_text(encoding='utf-8')
        st = Counter()
        n = process(s, st)
        total.update(st)
        if n != s and not dry:
            Path(p).write_text(n, encoding='utf-8')
        print(('zmieniono ' if n != s else 'bez zmian ') + p + ('  ' + ', '.join(f'{k}: {v}' for k, v in sorted(st.items())) if st else ''))
    if len(args) > 1:
        print('RAZEM  ' + ', '.join(f'{k}: {v}' for k, v in sorted(total.items())))
