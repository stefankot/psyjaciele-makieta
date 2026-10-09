# generated: psyjaciele-podstrony
"""infografiki.py — infografiki wstawiane po nagłówku wskazanych sekcji (HTML + SVG, style w podstrony.css, klasy .info-*).

Teksty są skrótami zdań ze źródła tej samej sekcji (patrz komentarze); infografika jest dekoracją (aria-hidden), pełna treść zostaje w tekście.
inject(slug, html) → html. Wstawia po pierwszym </header> następującym po <h2 id="…">.
"""

ROW = 48   # wysokość wiersza infografiki „zbieżne linie” w px (wielokrotność 8)


RICE = ('<svg class="info-rice" viewBox="0 0 120 56" aria-hidden="true"><ellipse cx="60" cy="28" rx="50" ry="15" '
        'transform="rotate(-18 60 28)" fill="none" stroke="currentColor" stroke-width="3"/></svg>')
DROP = ('<svg class="info-rice" viewBox="0 0 120 68" aria-hidden="true"><path d="M60 4C46 22 38 32 38 40a22 22 0 0 0 44 0C82 32 74 22 60 4Z" '
        'fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="miter"/></svg>')


def stats(tiles):
    """Kafle z wielkimi liczbami. tiles: [(liczba lub None, podpis, styl 'ink'|'accent'|'line', ikona lub '')] — trzy kafle."""
    out = []
    for i, (num, label, style, icon) in enumerate(tiles):
        wide = ' is-wide' if num and len(num) > 2 else ''
        head = f'<span class="info-num">{num}</span>' if num else icon
        out.append(f'<div class="info-stat is-{style}{wide}">{head}<span class="info-label">{label}</span></div>')
    return '<figure class="info info-stats" aria-hidden="true">' + ''.join(out) + '</figure>'


def stats_czip():
    """„Jak działa czip”: 15-cyfrowy numer (ISO), brak baterii i sygnału, wielkość ziarna ryżu."""
    return stats([('15', 'cyfr w unikalnym numerze czipa (norma ISO)', 'ink', ''),
                  ('0', 'baterii i sygnałów — to nie GPS', 'accent', ''),
                  (None, 'wielkość ziarna ryżu', 'line', RICE)])


def stats_usg():
    """USG jamy brzusznej: 12 godzin bez jedzenia, 2–3 godziny bez kuwety (kot), woda bez ograniczeń."""
    return stats([('12', 'godzin bez jedzenia przed USG jamy brzusznej', 'ink', ''),
                  ('2–3', 'godziny przed badaniem zabierz kotu kuwetę — pęcherz ma być pełny', 'accent', ''),
                  (None, 'woda bez ograniczeń', 'line', DROP)])


def stats_lab():
    """Badania laboratoryjne: krew na czczo 8–12 godzin, kał z trzech dni, mocz świeży z porannej zbiórki."""
    return stats([('8–12', 'godzin od ostatniego posiłku do pobrania krwi; woda bez ograniczeń', 'ink', ''),
                  ('3', 'dni: próbki kału z trzech kolejnych dni zwiększają szansę wykrycia pasożytów', 'accent', ''),
                  (None, 'mocz najlepiej świeży, z porannej zbiórki', 'line', DROP)])


def stats_kontrolne():
    """Interna, „Badania kontrolne”: raz w roku u starszych, częściej u chorych przewlekle, krew i mocz wykrywają choroby przed objawami."""
    return stats([('1', 'raz w roku — minimum kontroli u zwierząt starszych', 'ink', ''),
                  (None, 'u zwierząt chorych przewlekle kontrole są częstsze', 'accent', ''),
                  (None, 'badania krwi i moczu wykrywają część chorób, zanim dadzą objawy', 'line', DROP)])


def steps(items):
    """Stopnie z rosnącymi kółkami (styl bloku range-scale). items: [(tytuł, podpis)] — cztery pozycje."""
    lis = ''.join(f'<li><span class="range-value">{t}</span><span class="range-cell">{c}</span></li>' for t, c in items)
    return f'<ol class="range-scale" aria-hidden="true" style="--cols-n:{len(items)}">{lis}</ol>'


def steps_paszport():
    """Pierwszy paszport: czip → szczepienie przeciw wściekliźnie → 21 dni oczekiwania → wyjazd (wizyta 3–4 tygodnie wcześniej)."""
    return steps([('Czip', 'najpierw oznakowanie'), ('Szczepienie', 'przeciw wściekliźnie'),
                  ('21 dni', 'oczekiwania na ważność szczepienia'), ('Wyjazd', 'wizytę zaplanuj 3–4 tygodnie wcześniej')])


def converge(src, target='Numer czipa', note='i opiekun'):
    """Wiele dróg prowadzi do jednego punktu. src: lista podpisów po lewej (skróty pozycji z listy w sekcji)."""
    n = len(src)
    h = n * ROW
    mid = h / 2
    paths = ''.join(f'<path d="M0 {ROW * i + ROW // 2} C55 {ROW * i + ROW // 2} 45 {mid:g} 100 {mid:g}"/>' for i in range(n))
    lis = ''.join(f'<li>{x}</li>' for x in src)
    return (f'<figure class="info info-converge" aria-hidden="true" style="--n:{n}">'
            f'<ul class="info-sources">{lis}</ul>'
            f'<svg class="info-lines" viewBox="0 0 100 {h}" preserveAspectRatio="none">{paths}</svg>'
            f'<div class="info-target"><span class="info-dot"></span><strong>{target}</strong><span>{note}</span></div>'
            '</figure>')


def converge_zgubi():
    return converge(['Baza z zarejestrowanym czipem', 'Okoliczne lecznice', 'Schroniska', 'Straż miejska', 'Sąsiedzi i lokalne grupy'])


def converge_interna():
    return converge(['Układ pokarmowy', 'Układ oddechowy', 'Układ hormonalny i nerki', 'Układ nerwowy', 'Układ moczowy'], 'Internista', 'jedna wizyta')


def converge_stomatologia():
    return converge(['Nieświeży zapach z pyska', 'Krwawiące dziąsła, osad na zębach', 'Ślinienie, pocieranie pyska łapą',
                     'Jedzenie jedną stroną', 'Złamany lub ruszający się ząb', 'Obrzęk pod okiem lub na żuchwie'], 'Wizyta', 'stomatologiczna')


def converge_urologia():
    return converge(['Częste oddawanie moczu w małych ilościach', 'Mocz poza kuwetą lub w domu', 'Krew w moczu',
                     'Ból i napinanie się przy oddawaniu', 'Częste lizanie okolic cewki', 'Apatia, brak apetytu, wymioty',
                     'Próby oddania moczu bez skutku'], 'Konsultacja', 'urologiczna')


def lanes():
    """„Sam czip nie wystarczy”: kto, co i gdzie (opiekun / lecznica / baza). Teksty to skróty zdań sekcji i kroków zabiegu."""
    def card(txt, lane, cls='', arrow=False):
        ar = '<span class="lane-arrow"></span>' if arrow else ''
        return f'<div class="lane-card {cls}" data-l="{lane}">{txt}{ar}</div>'
    e = '<div class="lane-cell"></div>'
    c = lambda inner, span='': f'<div class="lane-cell{span}">{inner}</div>'
    rows = [
        e + c(card('Wszczepia czip i wpisuje numer do książeczki lub paszportu', 'Lecznica', 'is-ink')) + e,
        e + c(card('Rejestruje zwierzę i dane opiekuna', 'Lecznica', 'is-accent', True)) + c(card('Safe-Animal', 'Baza')),
        c(card('Zapisuje numer czipa', 'Opiekun', 'is-accent')) + e + e,
        c(card('Sprawdza dane i aktualizuje je przy zmianie telefonu, adresu lub opiekuna', 'Opiekun', 'is-ink', True), ' is-span2') + c(card('Aktualne dane', 'Baza')),
    ]
    return ('<figure class="info info-lanes" aria-hidden="true">'
            '<div class="lane-head">Opiekun</div><div class="lane-head">Lecznica</div><div class="lane-head">Baza</div>'
            + ''.join(rows) + '</figure>')


def lanes_chirurgia():
    """Konsultacja chirurgiczna: dwa tory (lekarka, opiekun); kroki to tytuły czterech punktów listy w sekcji."""
    def card(txt, lane, cls='', arrow=False):
        ar = '<span class="lane-arrow"></span>' if arrow else ''
        return f'<div class="lane-card {cls}" data-l="{lane}">{txt}{ar}</div>'
    e = '<div class="lane-cell"></div>'
    c = lambda inner, span='': f'<div class="lane-cell{span}">{inner}</div>'
    rows = [
        c(card('Rozmowa i badanie', 'Lekarka', 'is-ink')) + e,
        c(card('Plan: możliwości leczenia, korzyści i ryzyko', 'Lekarka', 'is-accent', True)) + e,
        c(card('Termin i zalecenia: kiedy zabieg i jak przygotować zwierzę', 'Lekarka i opiekun', 'is-ink'), ' is-span2'),
        e + c(card('Opieka po zabiegu: zalecenia dla domu i termin kontroli', 'Opiekun', 'is-accent')),
    ]
    return ('<figure class="info info-lanes" aria-hidden="true" style="--lanes:2">'
            '<div class="lane-head">Lekarka</div><div class="lane-head">Opiekun</div>' + ''.join(rows) + '</figure>')


# (slug, id nagłówka) → fabryka
PLAN = {
    ('czipowanie-psow-i-kotow', 'jak-dziala-czip'): stats_czip,
    ('czipowanie-psow-i-kotow', 'co-zrobic-gdy-zwierze-sie-zgubi'): converge_zgubi,
    ('czipowanie-psow-i-kotow', 'sam-czip-nie-wystarczy-liczy-sie-rejestracja'): lanes,
    ('diagnostyka-obrazowa-psow-i-kotow', 'jak-przygotowac-psa-lub-kota-do-badania-usg'): stats_usg,
    ('diagnostyka-laboratoryjna-weterynaryjna', 'jak-przygotowac-zwierze-do-badan'): stats_lab,
    ('wystawianie-paszportow-psom-i-kotom', 'co-zabrac-na-wizyte'): steps_paszport,
    ('choroby-wewnetrzne-u-psow-i-kotow', 'z-jakimi-objawami-przyjsc-do-internisty'): converge_interna,
    ('choroby-wewnetrzne-u-psow-i-kotow', 'badania-kontrolne'): stats_kontrolne,
    ('stomatologia-weterynaryjna', 'objawy-ktorych-nie-warto-przeczekac'): converge_stomatologia,
    ('urologia-weterynaryjna', 'objawy-chorob-dolnych-drog-moczowych'): converge_urologia,
    ('chirurgia-weterynaryjna-tkanek-miekkich', 'jak-wyglada-konsultacja-chirurgiczna'): lanes_chirurgia,
}



# --- baner „W nagłym przypadku zadzwoń” (okulistyka): kafle w różnych kolorach, tekst u góry i na dole, ikona ---
import re
from pathlib import Path

_ICON = Path(__file__).resolve().parents[2] / 'assets' / 'icons' / 'emergency.svg'
_EMERGENCY_P = re.compile(r'<p>W nagłym przypadku zadzwoń: <a href="(tel:[^"]+)">([^<]+)</a>\. (Gdy mamy zamknięte, jedź do lecznicy całodobowej\.)</p>')


def _icon():
    """Ikona „emergency” (Annisa, Noun Project): bez dopisków <text> z pliku, kadr przycięty do rysunku, kolor = currentColor."""
    svg = _ICON.read_text(encoding='utf-8')
    svg = re.sub(r'<\?xml.*?\?>|<!--.*?-->|<!DOCTYPE[^>]*>|<text\b.*?</text>', '', svg, flags=re.S).strip()
    svg = re.sub(r'viewBox="[^"]*"', 'viewBox="10 8 80 82"', svg, count=1)
    return svg.replace('<svg ', '<svg class="ab-icon" fill="currentColor" aria-hidden="true" focusable="false" data-credit="Annisa, Noun Project" ', 1)


def alert_banner(html, root='../../', slug=''):
    m = _EMERGENCY_P.search(html)
    if not m:
        return html
    tel, num, closed = m.group(1), m.group(2), m.group(3)
    # ilustracja sekcji (ramka zdjęcia w kolumnie bocznej) przechodzi do kafla baneru
    sec = html.rfind('<section', 0, m.start())
    art = ''
    fm = None
    for fm in re.finditer(r'<figure class="placeholder photo-frame[^"]*"[^>]*>.*?</figure>(?:<!--.*?-->)?', html[sec:m.start()], flags=re.S):
        pass
    if fm:
        art = fm.group(0)
        a, b = sec + fm.start(), sec + fm.end()
        html = html[:a] + html[b:]
        m = _EMERGENCY_P.search(html)
    cap = re.search(r'<figcaption><strong>([^<]+)</strong>', art)
    top = {'okulistyka-weterynaryjna': 'Okulistyka'}.get(slug, 'Nagły przypadek')
    # kafel z ilustracją też ma tekst u góry (nazwa dziedziny) i na dole (podpis rysunku z ramki)
    tile_art = (f'<div class="ab-tile ab-art"><span class="ab-top">{top}</span>{art}'
                f'<span class="ab-cap">{cap.group(1) if cap else ""}</span></div>') if art else ''
    arrow = '<span class="ab-arrow" aria-hidden="true"></span>'
    # dwa kafle-linki: cały kafel „zadzwoń” uruchamia telefon, cały kafel „lecznice” prowadzi do kontaktów lecznic całodobowych
    banner = (f'<div class="alert-banner{" has-art" if art else ""}" role="group" aria-label="Nagły przypadek">{tile_art}'
              f'<a class="ab-tile ab-call" href="{tel}"><span class="ab-top">W nagłym przypadku zadzwoń:</span>'
              f'<span class="ab-phone">{num}</span></a>'
              f'<a class="ab-tile ab-closed" href="{root}index.html#after-hours-title"><span class="ab-top">{closed}</span>'
              f'<span class="ab-foot">{_icon()}<span class="ab-more">Zobacz lecznice całodobowe {arrow}</span></span></a></div>')
    return html[:m.start()] + banner + html[m.end():]


def inject(slug, html):
    html = alert_banner(html, '../' if slug in ('uslugi-weterynaryjne', 'zespol', 'polityka-prywatnosci') else '../../', slug)
    for (s, hid), fn in PLAN.items():
        if s != slug:
            continue
        i = html.find(f'<h2 id="{hid}"')
        if i < 0:
            raise SystemExit(f'infografiki: brak nagłówka {hid} na stronie {slug}')
        j = html.find('</header>', i)
        k = j + len('</header>')
        html = html[:k] + fn() + html[k:]
    return html
