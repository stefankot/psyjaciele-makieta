# generated: psyjaciele-podstrony
"""bloki_demo.py — _bloki.html: wszystkie nowe bloki N1–N27 w czterech paletach (soft-a, mid-c, paper, booking).

Teksty w przykładach są neutralnymi przykładami technicznymi (strona ma noindex i nie trafia do użytkowników).
Wyjątek: N23 doctor-strip pokazany tylko w palecie „team” — karty osób mają style tylko w kontekście .team (pułapka H9).
"""
import re
from types import SimpleNamespace as NS

from bs4 import BeautifulSoup

import bloki as B
import obrazy

ROLES = ['soft-a', 'mid-c', 'paper', 'booking']
ALARM_ROLES = ['soft-a', 'paper', 'mid-a', 'booking']


def soup(html):
    return BeautifulSoup(html, 'html.parser')


def tag(html):
    return soup(html).find()


def _register_demo():
    base = {'strona': 'demo', 'opis_pl': '', 'zrodlo': '', 'prompt_en': '', 'min_px': 0, 'czego_unikac_pl': '', 'obrobka': ''}
    for pid, kind, ratio, title in [('demo-foto', 'foto', '4/5', 'Przykładowe zdjęcie'), ('demo-foto2', 'foto', '3/2', 'Przykładowe zdjęcie'),
                                    ('demo-foto3', 'foto', '3/2', 'Przykładowe zdjęcie'), ('demo-pas', 'pas', '21/9', 'Przykładowy pas'),
                                    ('demo-diagram', 'diagram', '4/3', 'Przykładowy diagram'), ('demo-wycinek', 'wycinek', '1/1', 'Przykładowy wycinek')]:
        obrazy.OBRAZY[pid] = dict(base, id=pid, kind=kind, ratio=ratio, title=title, alt=title)


FAQ = NS(subs=[NS(id='pyt-a', title='Przykładowe pytanie pierwsze?', nodes=[tag('<p>Krótka odpowiedź na pytanie pierwsze, w dwóch zdaniach. Druga część zdania.</p>')]),
               NS(id='pyt-b', title='Przykładowe pytanie drugie?', nodes=[tag('<p>Odpowiedź na pytanie drugie.</p>')]),
               NS(id='pyt-c', title='Przykładowe pytanie trzecie?', nodes=[tag('<p>Odpowiedź na pytanie trzecie.</p>')])])


def wrap(home, role, inner, uid):
    cls = home.role_class[role]
    lab = home.label_for(cls)
    return (f'<section class="{cls}" data-palette="{lab}" aria-label="Paleta {role}"><div class="wrap section-stack">'
            f'<p class="bloki-label">{uid} · paleta: {role}</p>{inner}</div></section>')


def fixtures(ctx, sfx):
    """→ [(kod, nazwa, role, html)]; każde id z sufiksem palety, żeby uniknąć duplikatów."""
    home = ctx.home
    s = sfx
    nap = home.nap
    cta = tag(f'<p>Umów wizytę <a href="{nap["wettermin"]}">online</a> lub zadzwoń: <a href="tel:{nap["tel"]}">{nap["tel_disp"]}</a>.</p>')
    out = []

    def add(code, name, html, roles=None):
        out.append((code, name, roles or ROLES, html))

    # N1 + N2 + N3
    hero = B.page_hero(ctx, None,
                       None, 'Przykładowa usługa weterynaryjna dla psów i kotów',
                       [tag('<p>Akapit wstępny w tym przykładzie ma kilka zdań, żeby pokazać szerokość kolumny i rytm tekstu.</p>')],
                       cta, '', B.fact_strip(ctx, [('Czas', '30 minut'), ('Dla kogo', 'psy i koty'), ('Rezerwacja', 'online')],
                                             '30 minut psy i koty online'), hid=f'h1-demo-{s}', no_art=True, back=('uslugi-weterynaryjne/index.html', 'Wróć do usług'))
    add('N1', 'page-hero (+ strzałka powrotu, N3 fact-strip)', re.sub(r'^<section[^>]*><div class="wrap section-stack">|</div></section>$', '', hero))
    # N4
    toc = [{'id': f'a-{s}', 'text': 'Pierwszy rozdział', 'subs': []}, {'id': f'b-{s}', 'text': 'Drugi rozdział', 'subs': [{'id': f'b1-{s}', 'text': 'Podrozdział'}]},
           {'id': f'c-{s}', 'text': 'Trzeci rozdział', 'subs': []}]
    add('N4', 'toc-index', B.toc_index(ctx, toc).replace('id="toc-title"', f'id="toc-title-{s}"').replace('aria-labelledby="toc-title"', f'aria-labelledby="toc-title-{s}"'))
    # N5 + N6
    sec = NS(id=f'rozdzial-{s}', title='Jak wygląda przykładowe badanie', nodes=[])
    head = B.section_head(ctx, 2, sec, 'Zdanie wprowadzające do rozdziału.', 2)
    body = ('<div class="sub-chapter"><h3 id="sub1-%s">Pierwszy podrozdział</h3><p>Akapit przykładowy, który pokazuje szerokość kolumny treści w układzie z nagłówkiem po boku.</p></div>'
            '<div class="sub-chapter"><h3 id="sub2-%s">Drugi podrozdział</h3><p>Drugi akapit przykładowy.</p></div>') % (s, s)
    add('N5/N6', 'section-head + split-feature', B.split_feature(ctx, head + B.photo_frame(ctx, 'demo-foto', role='demo'), body))
    add('N6r', 'split-feature (is-reversed)', B.split_feature(ctx, head.replace(f'rozdzial-{s}', f'rozdzial-r-{s}'), body.replace(f'sub1-{s}', f'sub1r-{s}').replace(f'sub2-{s}', f'sub2r-{s}'), reverse=True))
    # N7
    add('N7', 'rail-layout', B.rail_layout(ctx, [(f'r1-{s}', 'Pierwszy'), (f'r2-{s}', 'Drugi'), (f'r3-{s}', 'Trzeci')],
                                          f'<section id="r1-{s}"><h3>Pierwszy</h3><p>Treść pierwszego rozdziału.</p></section>'
                                          f'<section id="r2-{s}"><h3>Drugi</h3><p>Treść drugiego rozdziału.</p></section>'
                                          f'<section id="r3-{s}"><h3>Trzeci</h3><p>Treść trzeciego rozdziału.</p></section>'))
    # N8
    add('N8', 'ruled-list (+ is-numbered, is-checklist)',
        B.ruled_list(ctx, tag('<ul><li>Pierwszy punkt listy</li><li>Drugi punkt listy</li><li>Trzeci punkt listy</li></ul>')) +
        B.ruled_list(ctx, tag('<ol><li>Krok pierwszy</li><li>Krok drugi</li><li>Krok trzeci</li></ol>')) +
        B.ruled_list(ctx, tag('<ul><li>Zabierz książeczkę</li><li>Zapisz objawy</li></ul>'), 'is-checklist'))
    # N9
    tbl = tag('<table><thead><tr><th>Objaw</th><th>Jak szybko</th></tr></thead><tbody><tr><td>Pierwszy objaw</td><td>tego samego dnia</td></tr>'
              '<tr><td>Drugi objaw</td><td>w ciągu kilku dni</td></tr><tr><td>Trzeci objaw</td><td>wizyta planowa</td></tr></tbody></table>')
    tbl3 = tag('<table><thead><tr><th>Badanie</th><th>Po co</th><th>Kiedy</th></tr></thead><tbody><tr><td>Pierwsze</td><td>Opis celu</td><td>Raz w roku</td></tr>'
               '<tr><td>Drugie</td><td>Opis celu</td><td>Przy objawach</td></tr></tbody></table>')
    add('N9', 'ruled-table (+ is-triage, is-directory)', B.ruled_table(ctx, tbl3, 'Badania') + B.triage_table(ctx, tbl, 'Pilność') + B.ruled_table(ctx, tbl3, 'Katalog', 'is-directory'))
    # N10
    add('N10', 'step-list', B.step_list(ctx, tag('<ol><li><strong>Rozmowa.</strong> Opis pierwszego kroku w jednym zdaniu.</li>'
                                                '<li><strong>Badanie.</strong> Opis drugiego kroku.</li><li><strong>Zalecenia.</strong> Opis trzeciego kroku.</li></ol>')))
    # N11
    ph = tag('<table><thead><tr><th>Etap</th><th>Kiedy</th><th>Co się dzieje</th></tr></thead><tbody><tr><td>Pierwszy</td><td>dzień 1</td><td>Opis etapu.</td></tr>'
             '<tr><td>Drugi</td><td>tydzień 2</td><td>Opis etapu.</td></tr><tr><td>Trzeci</td><td>miesiąc 3</td><td>Opis etapu.</td></tr></tbody></table>')
    add('N11', 'phase-timeline', B.phase_timeline(ctx, ph))
    # N12
    d1 = tag('<table><thead><tr><th>Cecha</th><th>U psa</th><th>U kota</th></tr></thead><tbody><tr><td>Pierwsza</td><td>opis dla psa</td><td>opis dla kota</td></tr>'
             '<tr><td>Druga</td><td>opis dla psa</td><td>opis dla kota</td></tr></tbody></table>')
    d2 = tag('<table><thead><tr><th>Gdzie</th><th>Badania</th></tr></thead><tbody><tr><td>W gabinecie</td><td>pierwsze, drugie</td></tr><tr><td>W laboratorium</td><td>trzecie, czwarte</td></tr></tbody></table>')
    add('N12', 'duo (kolumny i wiersze)', B.duo_cols(ctx, d1, 'Porównanie') + B.duo_rows(ctx, d2, 'Gdzie'))
    # N13
    rs = tag('<table><thead><tr><th>Zakres</th><th>Opis</th></tr></thead><tbody><tr><td>niski</td><td>opis zakresu</td></tr><tr><td>środkowy</td><td>opis zakresu</td></tr><tr><td>wysoki</td><td>opis zakresu</td></tr></tbody></table>')
    add('N13', 'range-scale', B.range_scale(ctx, rs, 'Zakresy'))
    # N14
    add('N14', 'key-values', B.key_values(ctx, tag('<ul><li><strong>Czas.</strong> około 30 minut</li><li><strong>Przygotowanie.</strong> opis przygotowania</li><li><strong>Koszt.</strong> zależy od zakresu</li></ul>')))
    # N15
    add('N15', 'legal-prose', f'<div class="legal-prose"><h2>Przykładowy paragraf</h2><p>Treść przykładowego paragrafu w układzie dokumentu prawnego.</p>'
                              '<ol><li>Pierwszy punkt</li><li>Drugi punkt</li></ol><h3>Podpunkt</h3><p>Dalsza treść.</p></div>')
    # N16
    add('N16', 'alert-band', B.alert_band(ctx, 3, 'Przykładowy alarm', None, '<p>Krótka instrukcja do wykonania od razu.</p>') +
        B.alert_band(ctx, 3, 'Wersja bez telefonu', None, '<p>Bez przycisku.</p>', kick='Uwaga', inverted=False, phone=False), ALARM_ROLES)
    # N17
    add('N17', 'callout', B.callout(ctx, 'Ważne', ['Jedno ważne zdanie do zapamiętania.']))
    # N18
    add('N18', 'cta-band', B.cta_band(ctx, cta))
    # N19
    add('N19', 'sticky-cta (≤ 700 px; tu statycznie)', f'<div class="bloki-static-sticky">{B.sticky_cta(ctx)}</div>')
    # N20
    fq = B.faq_accordion(ctx, FAQ, open_first=True)
    for k in ('pyt-a', 'pyt-b', 'pyt-c'):
        fq = fq.replace(f'id="{k}"', f'id="{k}-{s}"')
    add('N20', 'faq-accordion', fq)
    # N21
    add('N21', 'chooser', B.chooser(ctx, tag('<ul><li>Jeśli pierwszy warunek — pierwsza rekomendacja.</li><li>Jeśli drugi warunek — druga rekomendacja.</li></ul>')))
    # N22
    add('N22', 'related-tiles', B.related_tiles(ctx, ['kardiologia-weterynaryjna', 'okulistyka-weterynaryjna', 'stomatologia-weterynaryjna']))
    # N23 — tylko team
    add('N23', 'doctor-strip', B.section_head(ctx, None, NS(id=f'ds-{s}', title='Lekarki prowadzące', nodes=[]), None, 2) + B.people_cards(ctx, ['Kinga']), ['mid-c'])
    # N24
    add('N24', 'photo-frame (foto, wycinek, diagram)', '<div class="bloki-row">' + B.photo_frame(ctx, 'demo-foto') + B.photo_frame(ctx, 'demo-wycinek', 'is-plain') +
        B.photo_frame(ctx, 'demo-diagram') + '</div>')
    # N25
    add('N25', 'figure-band (+ callout)', B.figure_band(ctx, 'demo-pas', B.callout(ctx, 'Ważne', ['Zdanie nałożone na pas.'])))
    # N26
    add('N26', 'figure-mosaic', B.figure_mosaic(ctx, ['demo-foto', 'demo-foto2', 'demo-foto3']))
    # N27
    from plany import BREATH
    add('N27', 'breath-counter', BREATH)
    return out


CSS = '''
.bloki-label { font-size: 16px; line-height: 24px; letter-spacing: .08em; text-transform: uppercase; margin: 0 0 24px; border-bottom: 1px solid currentColor; padding-bottom: 8px; }
.bloki-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px; align-items: start; }
@media (max-width: 700px) { .bloki-row { grid-template-columns: 1fr; } }
.bloki-static-sticky .sticky-cta { display: flex; position: static; transform: none; gap: 16px; padding: 16px; max-width: 416px; background: var(--ink); color: var(--surface); }
.bloki-static-sticky .sticky-cta .button { flex: 1; background: var(--surface); color: var(--ink); border-color: var(--surface); min-height: 56px; }
'''


def render(home, pages, root, build):
    """Zwraca pełny dokument _bloki.html. `build` — moduł build (head/header/footer/skrypty)."""
    import home as H
    import strony
    _register_demo()
    rw = H.Rewriter(pages, 'index')
    src = strony.Src('kardiologia-weterynaryjna', root, H.Rewriter(pages, 'kardiologia-weterynaryjna'))
    ctx = B.Ctx(home, rw, src, 'bloki', {})
    ctx.cur_sec = ''
    allfx = []
    for i, role_set in enumerate(ROLES):
        allfx.append((role_set, fixtures(ctx, f'p{i}')))
    # grupowanie po bloku: dla każdego bloku → kolejno palety
    codes = [(c, n) for c, n, _r, _h in allfx[0][1]]
    secs = []
    toc = []
    for idx, (code, name) in enumerate(codes):
        parts = []
        for pi, (_rs, fx) in enumerate(allfx):
            c, n, roles, html = fx[idx]
            role = ROLES[pi]
            if role not in roles:
                continue
            parts.append(wrap(home, role, html, f'{c} {n}'))
        # sąsiednie sekcje muszą się różnić powierzchnią; ROLES są różne z założenia
        bid = f'blok-{code.lower().replace("/", "-")}'
        toc.append(f'<li><a href="#{bid}">{code} — {n}</a></li>')
        secs.append(f'<div id="{bid}">{"".join(parts)}</div>')
    intro = ('<section class="about" data-palette="%s" aria-label="Wstęp"><div class="wrap section-stack"><h1 id="tytul-strony"><em>Bloki podstron</em></h1>'
             '<p>Katalog nowych bloków N1–N27 w czterech paletach z home (soft-a, mid-c, paper, booking). Strona techniczna, noindex. '
             'N23 pokazany tylko w palecie team.</p><nav aria-label="Spis bloków"><ol class="ruled-list">%s</ol></nav></div></section>') % (home.label_for('about'), ''.join(toc))
    main = intro + ''.join(secs)

    class _P:
        slug = 'index'
        rw = None
    P = _P()
    P.rw = rw
    head = build.simple_head(home, rw, 'Bloki podstron — katalog', 'Katalog nowych bloków podstron w czterech paletach.')
    svg = rw.fragment(home.svg_filters_raw)
    return f'''<!doctype html>
<html lang="pl"><head>
{head}
<style>{CSS}</style>
</head>
<body class="book-type subpage" data-root="{rw.root}" data-page="bloki">
<a class="skip" href="#main">Przejdź do treści</a>
<div class="header-backdrop" aria-hidden="true"></div>{build.header_html(home, P)}
<main id="main">
{main}
</main>
{rw.fragment(home.footer_raw, frag_to_home=True)}
{svg}
{build.body_scripts(home, rw)}
</body></html>
'''
