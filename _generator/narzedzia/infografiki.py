# generated: psyjaciele-podstrony
"""infografiki.py — infografiki wstawiane po nagłówku wskazanych sekcji (HTML + SVG, style w podstrony.css, klasy .info-*).

Teksty są skrótami zdań ze źródła tej samej sekcji (patrz komentarze); infografika jest dekoracją (aria-hidden), pełna treść zostaje w tekście.
inject(slug, html) → html. Wstawia po pierwszym </header> następującym po <h2 id="…">.
"""

ROW = 48   # wysokość wiersza infografiki „zbieżne linie” w px (wielokrotność 8)


RICE = ('<svg class="info-rice" viewBox="0 0 120 56" aria-hidden="true"><ellipse cx="60" cy="28" rx="50" ry="15" '
        'transform="rotate(-18 60 28)" fill="none" stroke="currentColor" stroke-width="3"/></svg>')
DROP = ('<svg class="info-rice info-drop" viewBox="36 2 48 66" aria-hidden="true"><path d="M60 4C46 22 38 32 38 40a22 22 0 0 0 44 0C82 32 74 22 60 4Z" '
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
    """„Sam czip nie wystarczy”: cztery kroki po kolei (numer, kto, co) — zamiast torów z pustymi komórkami. Teksty to skróty zdań sekcji i kroków zabiegu."""
    steps = [
        ('Lecznica', 'Wszczepia czip i wpisuje jego numer do książeczki lub paszportu.', 'is-ink'),
        ('Lecznica', 'Rejestruje zwierzę i dane opiekuna w bazie, np. Safe-Animal.', 'is-ink'),
        ('Opiekun', 'Zapisuje numer czipa.', 'is-accent'),
        ('Opiekun', 'Sprawdza dane w bazie i aktualizuje je przy zmianie telefonu, adresu lub opiekuna.', 'is-accent'),
    ]
    cards = ''.join(f'<div class="step4 {cls}"><span class="s4-top"><span class="s4-num">{i}</span><span class="s4-who">{who}</span></span><p>{txt}</p></div>'
                    for i, (who, txt, cls) in enumerate(steps, 1))
    return f'<figure class="info info-steps4" aria-hidden="true">{cards}</figure>'


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


def road_czip():
    """Proces czipowania: 4 punkty poziomo (numer, kreska, tekst), po 2 z 8 kolumn artykułu. Teksty to kroki z listy w sekcji
    (lista zostaje w HTML jako źródło dla czytników, na desktopie ukryta; poniżej 1001 px widać listę)."""
    steps = ['Lekarka sprawdza czytnikiem, czy zwierzę nie ma już czipa.',
             'Wszczepia czip jednorazowym aplikatorem — trwa to kilka sekund i przypomina zastrzyk; nie wymaga znieczulenia.',
             'Odczytuje numer i wpisuje go do książeczki zdrowia lub paszportu.',
             'Rejestruje zwierzę i dane opiekuna w bazie Safe-Animal.']
    pts = ''.join(f'<div class="pt4"><span class="pt4-num">{i}</span><p>{t}</p></div>' for i, t in enumerate(steps, 1))
    return f'<figure class="info info-points4" aria-hidden="true">{pts}</figure>'


# (slug, id nagłówka) → fabryka
PLAN = {
    ('czipowanie-psow-i-kotow', 'jak-dziala-czip'): stats_czip,
    ('czipowanie-psow-i-kotow', 'co-zrobic-gdy-zwierze-sie-zgubi'): converge_zgubi,
    ('czipowanie-psow-i-kotow', 'sam-czip-nie-wystarczy-liczy-sie-rejestracja'): lanes,
    ('czipowanie-psow-i-kotow', 'jak-wyglada-czipowanie'): road_czip,
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


MOVE_ART = False

# nagłówki ostrzegawcze ze znakiem trójkąta (kreska 0,13 em, jak pismo obok)
WARN_H2 = {('dermatologia-weterynaryjna', 'dlaczego-nie-leczyc-skory-na-wlasna-reke')}
WARN_SIGN = ('<svg class="warn-sign" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 4.5 29 27.5H3Z"/><path d="M16 12v8M16 22.6v1.8"/></svg>')


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
    if fm and MOVE_ART:   # od 9.10.2026 rysunek zostaje w sekcji (poziomo, 8 kolumn), a baner to dwa kafle obok siebie
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
    for (ws, wid) in WARN_H2:
        if ws == slug:
            tag = f'<h2 id="{wid}">'
            if tag not in html:
                raise SystemExit(f'infografiki: brak nagłówka {wid} na stronie {slug}')
            html = html.replace(tag, f'<h2 id="{wid}" class="has-warn">{WARN_SIGN}', 1)
    if slug == 'czipowanie-psow-i-kotow':
        ol = '<ol class="step-list is-stacked" style="--steps:4">'
        if html.count(ol) != 1:
            raise SystemExit('infografiki: oczekiwano jednej listy kroków czipowania')
        html = html.replace(ol, '<ol class="step-list is-stacked is-road-source" style="--steps:4">', 1)
    if slug == 'szczepienia-oraz-profilaktyka-przeciwpasozytnicza':
        html = timeline_art(html, 'assets/podstrony/szczepienia-oraz-profilaktyka-przeciwpasozytnicza/szcz-03-kalendarz.png')
    return html


_TL_FILTER = ('<svg width="0" height="0" aria-hidden="true" style="position:absolute"><filter id="tl-ink" color-interpolation-filters="sRGB">'
              '<feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -.2126 -.7152 -.0722 0 1"/><feComposite in2="SourceGraphic" operator="in" result="lines"/>'
              '<feFlood flood-color="var(--ink)"/><feComposite in2="lines" operator="in"/></filter></svg>')


def timeline_art(html, img):
    """Oś czasu faz (5 kroków): rysunek z kółkami na górze (8 kol.), pod każdym kółkiem opis fazy; kolor kreski z filtra SVG (var(--ink))."""
    old = '<ol class="phase-timeline" style="--phases:5">'
    if old not in html:
        raise SystemExit('infografiki: brak osi czasu z 5 fazami')
    new = _TL_FILTER + f'<ol class="phase-timeline has-art" style="--phases:5;--tl-img:url({img})">'
    return html.replace(old, new, 1)
