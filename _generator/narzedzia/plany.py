# generated: psyjaciele-podstrony
"""plany.py — plany stron: sekwencja bloków, fakty, podziały tytułów (§10, §10A). Zero zdań treści — wszystko ze źródła.

Ręczne nadpisania (TITLE_SPLIT) są w jednym słowniku, z powodem.
"""
import bloki as B

PLANS = {}

# podział tytułów: 'h1' lub id sekcji → 'część romańska|część kursywą' (słowa nigdy nie są zmieniane)
TITLE_SPLIT = {
    # nazwiska lekarek: stały podział „lek. wet.” + imię i nazwisko (spójnie dla siedmiu profili)
    'zespol': {k: f'lek. wet.|{n}' for k, n in {
        'Magda': 'Magdalena Ostrowska', 'Ola': 'Aleksandra Podkowa', 'Julia': 'Julia Chutkowska-Świetlik',
        'Malgosia': 'Małgorzata Tywoniuk', 'Olga': 'Olga Winnicka-Ziółkowska', 'Kasia': 'Katarzyna Krawulska',
        'Kinga': 'Kinga Bielińska-Bielecka'}.items()},
}


def plan(slug):
    def deco(fn):
        PLANS[slug] = fn
        return fn
    return deco


def ph(P, pid, **kw):
    return B.photo_frame(P.ctx, pid, **kw)


# ============================================================================
# C · czipowanie
# ============================================================================
@plan('czipowanie-psow-i-kotow')
def _czipowanie(P):
    ctx = P.ctx
    P.hero([('Numer', '15-cyfrowy'), ('Standard', 'ISO'), ('Rejestr', 'Safe-Animal'), ('Od kiedy', 'od około 8. tygodnia życia')])
    P.toc()

    s = P.S('jak-dziala-czip')
    P.begin(s)
    P.chapter(s, B.ruled_list(ctx, s.nodes[0]), ph(P, 'czip-01-czip-diagram', role='aside rozdziału 01'), reverse=False)

    s = P.S('jak-wyglada-czipowanie')
    P.begin(s)
    ol, p = s.nodes
    it = P.chapter(s, B.step_list(ctx, ol, titles=False, cls='is-stacked') + f'<p>{p.decode_contents()}</p>',
                   ph(P, 'czip-02-aplikator', role='aside rozdziału 02'), reverse=True)
    it.inner += B.figure_band(ctx, 'czip-03-pas-zabieg')

    s = P.S('sam-czip-nie-wystarczy')
    P.begin(s)
    sub = s.subs[0]
    body = (B.callout(ctx, 'Ważne', s.nodes) +
            B.sub_chapter(ctx, sub, B.ruled_list(ctx, sub.nodes[0], 'is-checklist')))
    P.chapter(s, body, ph(P, 'czip-04-skaner', role='aside rozdziału 03'), reverse=False)

    s = P.S('co-zrobic-gdy-zwierze-sie-zgubi')
    P.begin(s)
    inner = (B.poster_header(ctx, 'nagle-przypadki', sec=s, kick='Pilne') +
             B.emergency_guide(ctx, s.nodes[0], s.id, None, untitled=True))
    P.add('alarm', inner, aria=s.id)

    s = P.S('czy-czipowanie-jest-obowiazkowe')
    P.begin(s)
    sub = s.subs[0]
    body = B.ruled_table(ctx, s.nodes[0], s.title) + B.sub_chapter(ctx, sub)
    P.chapter(s, body, ph(P, 'czip-05-pies-kot', role='aside rozdziału 05'), reverse=True)

    P.faq()
    P.related()
    P.booking()
    P.contact()


# ============================================================================
# Silnik planu automatycznego (reguły D1–D12): tabela/lista/podrozdziały → bloki; obrazy z manifestu
# ============================================================================
import re as _re
from strony import Item
from zrodlo import runin, table_rows
from obrazy import OBRAZY

URGENT = _re.compile(r'nie czekać|nie warto przeczekać|pilnie|stan nagły|natychmiast', _re.I)
CHECK = _re.compile(r'zabra|przygotow|co robić|dbać|pielęgn|zapobiegać|chronić|zmniejszyć|ułatwić', _re.I)


BREATH = ('<div class="breath-counter" role="group" aria-label="Licznik oddechów">'
          '<div class="bc-intro"><p class="kicker">Licznik oddechów w spoczynku</p>'
          '<p class="bc-how">Zwierzę ma spać lub spokojnie leżeć. Kliknij „Start”, a potem „Oddech” przy każdym oddechu (uniesienie i opadnięcie klatki). '
          'Po minucie pokażemy wynik.</p>'
          '<p class="bc-result" aria-live="polite" data-breath-result>Wynik pojawi się po 60 sekundach.</p></div>'
          '<div class="bc-panel"><p class="breath-time"><span data-breath-time>60</span> s</p><output aria-live="polite">0</output>'
          '<div class="breath-actions"><button type="button" class="button" data-breath-start data-label-again="Zacznij od nowa">Start</button>'
          '<button type="button" class="button" data-breath-tap>Oddech</button></div></div></div>')


def urgent_band(ctx, inner, kick='Pilne'):
    ctx.use('alert-band')
    nap = ctx.home.nap
    btn = f'<a class="button" href="tel:{nap["tel"]}">Zadzwoń: {nap["tel_disp"].replace(" ", B.NB)}</a>'
    return f'<div class="alert-band is-inverted" role="note"><span class="kicker">{kick}</span>{inner}{btn}</div>'


def table_html(P, n, title, directory=False):
    ctx = P.ctx
    head, rows = table_rows(n)
    h = [B.plain(x).strip().lower() for x in head]
    if directory:
        return B.ruled_table(ctx, n, title, 'is-directory')
    if h and (h[0] == '' or (len(h) >= 2 and (h[-2].startswith(('u psa', 'u psów'))))):
        return B.duo_cols(ctx, n, title)
    if h == ['gatunek', 'przykłady chorób'] or h[0] == 'gdzie':
        return B.duo_rows(ctx, n, title)
    if h[0] == 'etap' and len(h) == 3:
        return B.phase_timeline(ctx, n)
    if len(h) == 2 and h[1] == 'jak szybko':
        return B.triage_table(ctx, n, title)
    if h[0].startswith('ciśnienie skurczowe'):
        return B.range_scale(ctx, n, title)
    return B.ruled_table(ctx, n, title)


def nodes_html(P, nodes, title, wide, urgent=False, check=False, directory=False, chooser=False):
    ctx = P.ctx
    if urgent:
        inner = ''.join(f'<p>{n.decode_contents()}</p>' if n.name == 'p' else B._node_html(ctx, n) for n in nodes)
        return urgent_band(ctx, inner)
    out = []
    for n in nodes:
        if n.name in ('ul', 'ol') and getattr(P, '_owner', None) in getattr(P, 'h11', ()):
            out.append(B.emergency_guide(ctx, n, P._owner, None, untitled=True))
            continue
        if n.name == 'ul':
            items = n.find_all('li', recursive=False)
            labelled = len(items) >= 3 and all(runin(li)[0] for li in items)
            if chooser:
                out.append(B.chooser(ctx, n))
            elif labelled and not directory:
                out.append(B.key_values(ctx, n))
            else:
                out.append(B.ruled_list(ctx, n, 'is-checklist' if check else ''))
        elif n.name == 'ol':
            items = n.find_all('li', recursive=False)
            labelled = all(runin(li)[0] for li in items)
            out.append(B.step_list(ctx, n, titles=labelled, cls='' if (wide and len(items) <= 4) else 'is-stacked'))
        elif n.name == 'table':
            out.append(table_html(P, n, title, directory))
        else:
            out.append(B._node_html(ctx, n))
    return ''.join(out)


def sub_html(P, s, wide, directory=False):
    ctx = P.ctx
    t = B.plain(s.title)
    if URGENT.search(t):
        inner = ''.join(f'<p>{n.decode_contents()}</p>' if n.name == 'p' else B._node_html(ctx, n) for n in s.nodes)
        ctx.use('alert-band')
        nap = ctx.home.nap
        btn = f'<a class="button" href="tel:{nap["tel"]}">Zadzwoń: {nap["tel_disp"].replace(" ", B.NB)}</a>'
        return (f'<div class="alert-band is-inverted" role="note"><span class="kicker">Pilne</span>'
                f'<h3 id="{s.id}" class="alert-title">{s.title}</h3>{inner}{btn}</div>')
    P._owner = s.id
    extra = BREATH if s.id == 'jak-liczyc-oddechy-w-domu' else ''
    if extra:
        ctx.use('breath-counter')
    return B.sub_chapter(ctx, s, nodes_html(P, s.nodes, t, wide, False, bool(CHECK.search(t)), directory) + extra)


def is_grid(sec):
    return len(sec.subs) >= 3 and all(all(n.name == 'p' for n in s.nodes) for s in sec.subs)


def is_wide(sec, directory=False):
    if directory or is_grid(sec) or len(sec.subs) >= 4:
        return True
    for owner in [sec] + sec.subs:
        for n in owner.nodes:
            if n.name == 'table':
                h, r = table_rows(n)
                if len(h) >= 3 and len(r) >= 4:
                    return True
    return False


def body_for(P, sec, wide, directory=False, chooser=False):
    ctx = P.ctx
    title = B.plain(sec.title)
    urgent = bool(URGENT.search(title)) and not sec.subs
    check = bool(CHECK.search(title))
    P._owner = sec.id
    parts = [nodes_html(P, sec.nodes, title, wide, urgent, check, directory, chooser)]
    if sec.subs:
        if is_grid(sec):
            parts.append(B.equipment_grid(ctx, sec.subs, numbered=True, cols=3))
        else:
            parts += [sub_html(P, s, wide, directory) for s in sec.subs]
    return ''.join(parts)


def reviews_section(P, idx=(0, 1, 2)):
    ctx = P.ctx
    ctx.cur_sec = 'rekomendacje'
    ctx.use('quotes', 'poster-grid')
    inner = B.home_header_raw(ctx, 'rekomendacje') + B.quotes_block(ctx, list(idx))
    P.add('mid-b', inner, aria='section-title-6', kind='reviews')


def doctor_strip(P, keys):
    ctx = P.ctx
    ctx.cur_sec = 'kto-przyjmuje'
    ctx.use('doctor-strip')
    head = ('<header class="section-head">'
            '<h2 id="kto-przyjmuje"><em>Kto przyjmuje</em></h2></header>')
    P.add('mid-c', B.split_feature(ctx, head, B.people_cards(ctx, keys)), aria='kto-przyjmuje', kind='doctors')


def cta_section(P):
    ctx = P.ctx
    ctx.cur_sec = 'umow-telefon'
    P.add(None, '<h2 id="umow-telefon" class="visually-hidden">Umów wizytę</h2>' + B.cta_band(ctx, P.src.cta), aria='umow-telefon', kind='cta')


def after_hours_section(P):
    ctx = P.ctx
    P.add('mid-c', B.after_hours(ctx), aria='after-hours-title', kind='after-hours')


ART_IN_TIMELINE = {'szcz-03-kalendarz'}   # rysunek osi czasu stoi w infografice „Kiedy szczepić…” (infografiki.inject), nie w mozaice


def image_queue(slug):
    spec = [v for v in OBRAZY.values() if v['strona'] == slug and not v['id'].endswith('-00-hero') and v['id'] not in ART_IN_TIMELINE]
    spec.sort(key=lambda v: v['id'])
    spec = spec[:6]  # + ilustracja hero = max 7 placeholderów na stronę (V13)
    asides, bands, mosaic = [], [], []
    for v in spec:
        if v['kind'] == 'pas':
            bands.append(v['id'])
        elif _re.search(r'mozaika|pies-kot-[abc]$', v['id']):
            mosaic.append(v['id'])
        else:
            asides.append(v['id'])
    return asides, bands, mosaic


def auto(P, facts, kick='Usługa', directory_ids=(), before_faq=None, hero_kw=None, chooser_ids=(), alarm_ids=(), after_toc=None, alarm_extra=None,
         doctors=(), phone=False, quotes=False, social=False, booking=True, after_hours_after=None, h11=()):
    ctx, src = P.ctx, P.src
    P.h11 = set(h11)
    P.hero(facts, kick=kick, **(hero_kw or {}))
    P.toc()
    if after_toc:
        after_toc(P)
    # tabela wstępu (np. „Gdzie | Badania”)
    intro = [n for n in (src.intro_extra or []) if n.name == 'table']
    if intro:
        P.ctx.cur_sec = 'wstep'
        ctx.cur_title = 'Gdzie wykonujemy badania'
        body = ''.join(table_html(P, n, 'Gdzie wykonujemy badania') for n in intro)
        P.add(None, f'<div class="book-prose">{body}</div>', aria='toc-title')
    faq, contact = src.faq(), src.contact()
    secs = [s for s in src.secs if s is not faq and s is not contact]
    asides, bands, mosaic = image_queue(P.slug)
    pending_after = {}
    if bands:
        pending_after[1] = [('band', bands.pop(0))]
    if mosaic:
        pending_after.setdefault(2, []).append(('mosaic', mosaic[:]))
        mosaic.clear()
    if bands:
        pending_after.setdefault(3, []).append(('band', bands.pop(0)))
    for i, s in enumerate(secs):
        P.begin(s)
        if s.id in alarm_ids:
            inner = B.poster_header(ctx, 'nagle-przypadki', sec=s, kick='Pilne') + B.prose(ctx, s.nodes) + (alarm_extra(P) if alarm_extra else '')
            P.add('alarm', inner, aria=s.id)
            P.mark(s)
            if after_hours_after and s.id.startswith(after_hours_after):
                after_hours_section(P)
            continue
        d = s.id in directory_ids
        wide = is_wide(s, d)
        body = body_for(P, s, wide, d, s.id in chooser_ids)
        if wide:
            it = P.wide(s, body)
        else:
            aside = ph(P, asides.pop(0), role=f'aside rozdziału {P.num(s) or i + 1}') if asides else ''
            it = P.chapter(s, body, aside)
        P.mark(s)
        if after_hours_after and s.id.startswith(after_hours_after):
            after_hours_section(P)
        for kind, v in pending_after.pop(i, []) if i < len(secs) - 1 else []:
            it.inner += B.figure_band(ctx, v) if kind == 'band' else B.figure_mosaic(ctx, v)
    # obrazy, które nie znalazły miejsca
    left = [x for x in pending_after.values() for x in x]
    last = P.items[-1] if P.items else None
    for kind, v in left:
        last.inner += B.figure_band(ctx, v) if kind == 'band' else B.figure_mosaic(ctx, v)
    if asides:
        last.inner += B.figure_mosaic(ctx, asides)
        asides.clear()
    if before_faq:
        before_faq(P)
    if faq:
        P.faq(faq)
    if quotes:
        reviews_section(P)
    if doctors:
        doctor_strip(P, list(doctors))
    P.related()
    if phone:
        pass   # blok „Umów wizytę / Zadzwoń” usunięty (9.10.2026): powtarzał rezerwację i sekcję „Jak umówić”
    elif booking:
        P.booking()
    P.contact(contact)
    if social:   # „Obserwuj nas” na samym dole, pod „Jak umówić wizytę” (polecenie właściciela)
        P.items.append(Item('social', html=B.social_section(ctx), kind='social'))


FACTS = {
    'choroby-wewnetrzne-u-psow-i-kotow': [('Zakres', 'narządów i układów'), ('Rezerwacja online', 'Wettermin'), ('Adres', 'ul. Celownicza 4 lok. U-3')],
    'diagnostyka-laboratoryjna-weterynaryjna': [('Na miejscu', 'badanie moczu, badanie kału'), ('Zewnętrznie', 'laboratoriom zewnętrznym'), ('Rezerwacja online', 'Wettermin')],
    'szczepienia-oraz-profilaktyka-przeciwpasozytnicza': [('Pierwsza dawka', '6.–8. tydzień życia'), ('Kolejne dawki', 'co 2–4 tygodnie'), ('Wścieklizna', 'obowiązkowo')],
    'chirurgia-weterynaryjna-tkanek-miekkich': [('Lekarka', 'Katarzyna Krawulska'), ('Szwy', 'około 10–14 dni'), ('Terminy', 'telefonicznie')],
    'kardiologia-weterynaryjna': [('Lekarka', 'Małgorzata Tywoniuk'), ('Badania', 'ECHO i EKG'), ('Oddechy w domu', '30 oddechów na minutę'), ('Terminy', 'telefonicznie')],
    'diagnostyka-obrazowa-psow-i-kotow': [('Lekarka', 'Olga Winnicka-Ziółkowska'), ('USG ciąży', 'po około 3–4 tygodniach od krycia'), ('Badanie', 'bezbolesne'), ('Terminy', 'telefonicznie')],
    'okulistyka-weterynaryjna': [('Lekarka', 'Kinga Bielińska-Bielecka'), ('Choroby oczu', 'w ciągu godzin'), ('Terminy', 'telefonicznie')],
    'dermatologia-weterynaryjna': [('Lekarka', 'Magdalena Ostrowska'), ('Zakres', 'skóry i uszu'), ('Rezerwacja online', 'Wettermin')],
    'stomatologia-weterynaryjna': [('Lekarka', 'Aleksandra Podkowa'), ('Zakres', 'zębów i dziąseł'), ('Rezerwacja online', 'Wettermin')],
    'nefrologia-weterynaryjna': [('Lekarka', 'Magdalena Ostrowska'), ('Ostre uszkodzenie', 'AKI'), ('Przewlekła choroba', 'PChN')],
    'urologia-weterynaryjna': [('Lekarki', 'Magdalena Ostrowska i Aleksandra Podkowa'), ('Zakres', 'pęcherz i cewkę moczową'), ('Rezerwacja online', 'Wettermin')],
    'pomiar-cisnienia-psow-i-kotow': [('Lekarka', 'Magdalena Ostrowska'), ('Aparat wykorzystuje', 'metodę dopplerowską'), ('Badanie', 'bezbolesnym')],
    'wystawianie-paszportow-psom-i-kotom': [('Zwierzęta', 'psa, kota lub fretki'), ('Pierwsze szczepienie', 'po 21 dniach'), ('Zaplanuj wizytę', 'co najmniej 3–4 tygodnie przed wyjazdem'), ('Zmiany w przepisach', 'od 22 kwietnia 2026 r.')],
}

OPTS = {
    'urologia-weterynaryjna': {'alarm_ids': {'kocur-lub-pies-nie-moze-oddac-moczu-to-stan-nagly'},
                               'after_hours_after': 'kocur-lub-pies'},
    'choroby-wewnetrzne-u-psow-i-kotow': {'quotes': True, 'after_hours_after': 'kiedy-nie-czekac'},
    'szczepienia-oraz-profilaktyka-przeciwpasozytnicza': {'quotes': True},
    'stomatologia-weterynaryjna': {'doctors': ['Ola']},
    'nefrologia-weterynaryjna': {'doctors': ['Magda'], 'after_hours_after': 'ostre-uszkodzenie'},
    'dermatologia-weterynaryjna': {'after_hours_after': 'objawy-z-ktorymi'},
    'kardiologia-weterynaryjna': {'doctors': ['Malgosia'], 'phone': True, 'h11': {'jak-wyglada-konsultacja-kardiologiczna'}},
    'okulistyka-weterynaryjna': {'doctors': ['Kinga'], 'phone': True, 'after_hours_after': 'kiedy-do-okulisty', 'h11': {'co-robic-do-czasu-wizyty'}},
    'chirurgia-weterynaryjna-tkanek-miekkich': {'doctors': ['Kasia'], 'phone': True, 'h11': {'jak-wyglada-konsultacja-chirurgiczna', 'przygotowanie-w-dniu-zabiegu'}},
    'diagnostyka-obrazowa-psow-i-kotow': {'doctors': ['Olga', 'Ola'], 'phone': True},
    'wystawianie-paszportow-psom-i-kotom': {'doctors': ['Magda']},
}

for _slug, _facts in FACTS.items():
    def _mk(slug=_slug, facts=_facts):
        @plan(slug)
        def _p(P):
            auto(P, facts, **OPTS.get(slug, {}))
        return _p
    _mk()


# ============================================================================
# Hub · uslugi-weterynaryjne
# ============================================================================
@plan('uslugi-weterynaryjne')
def _hub(P):
    ctx = P.ctx

    def skrot(P):
        P.ctx.cur_sec = 'uslugi-skrot'
        inner = ('<header class="section-head">'
                 '<h2 id="uslugi-skrot" class="visually-hidden">Usługi w skrócie</h2></header>' + B.bento(P.ctx))
        P.add('mid-a', inner, aria='uslugi-skrot')

    auto(P, [('Adres', 'ul. Celownicza 4 lok. U-3'), ('Dzielnica', 'Praga-Południe'), ('Rezerwacja online', 'Wettermin')],
         kick='Usługi', after_toc=skrot,
         directory_ids={'leczenie-i-profilaktyka', 'diagnostyka', 'konsultacje-specjalistyczne', 'dokumenty-i-oznakowanie'},
         chooser_ids={'nie-wiesz-ktora-usluge-wybrac'}, alarm_ids={'nagle-przypadki'}, quotes=True, social=True, booking=False,
         alarm_extra=lambda P: B.after_hours(P.ctx))


# ============================================================================
# Zespół
# ============================================================================
def _portrait(ctx, key):
    raw = ctx.home.people_raw[key]
    m = _re.search(r'<figure>.*?</figure>', raw, _re.S)
    return ctx.rw.fragment(m.group(0)) if m else ''


@plan('zespol')
def _zespol(P):
    ctx, src = P.ctx, P.src
    P.hero([('Lekarki', 'siedem lekarek weterynarii'), ('Zwierzęta', 'psy i koty'), ('Rezerwacja online', 'Wettermin')], kick='Zespół')
    # bez spisu treści: tabela lekarek poniżej jest indeksem strony (spis tylko powielałby nazwiska)
    # tabela wstępu → katalog lekarek
    tbl = next(n for n in src.intro_extra if n.name == 'table')
    ps = [n for n in src.intro_extra if n.name == 'p']
    ctx.cur_sec = 'wstep'
    ctx.cur_title = 'Lekarki i dziedziny'
    body = B.ruled_table(ctx, tbl, 'Lekarki i dziedziny', 'is-directory') + ''.join(f'<p>{n.decode_contents()}</p>' for n in ps)
    P.add(None, f'<div class="stack">{body}</div>', aria=None)
    # sekcja „Którą lekarkę wybrać” usunięta na polecenie użytkownika (8.10.2026)
    P.mark(src.by_id['ktora-lekarke-wybrac'])
    # profile
    keys = [x.id for x in src.secs if x.id in ctx.home.people_raw]
    profiles = []
    for i, k in enumerate(keys):
        sec = src.by_id[k]
        P.begin(sec)
        name = B.plain(sec.title).replace('lek. wet.', '').strip()   # „lek. wet.” rozwinięte: lekarka weterynarii (polecenie użytkownika)
        head = (f'<header class="section-head"><h2 id="{sec.id}"><span class="kapitaliki">Lekarka weterynarii</span> '
                f'{B.nbsp_html(name)}</h2></header>')
        body = nodes_html(P, sec.nodes, B.plain(sec.title), False)
        rev = ' is-reversed' if i % 2 else ''
        profiles.append(f'<article class="profile{rev}" aria-labelledby="{sec.id}"><div class="profile-portrait">{_portrait(ctx, k)}</div>'
                        f'<div class="profile-main">{head}<div class="profile-body">{body}</div></div></article>')
        P.mark(sec)
    ctx.cur_sec = keys[0]
    rail = B.rail_layout(ctx, [(k, B.plain(src.by_id[k].title).replace('lek. wet.', '').strip()) for k in keys], ''.join(profiles), label='Lekarki')
    P.add(None, rail, aria=keys[0], kind='rail')
    P.items.append(Item('soft-a', html=B.about_section(ctx), kind='about'))
    s = src.by_id['praca-w-psyjaciolach']
    P.begin(s)
    ctx.cur_sec = s.id
    P.add(None, B.join_banner(ctx, s.title, s.nodes, B.join_art_dog(ctx), 'mailto:kontakt@psyjacielevet.pl', hid=s.id, forced=ctx.title_split(s.id)), aria=s.id)
    P.mark(s)
    P.faq()
    reviews_section(P, (0, 1, 2))
    P.contact()
    P.items.append(Item('social', html=B.social_section(ctx), kind='social'))


# ============================================================================
# Polityka prywatności
# ============================================================================
@plan('polityka-prywatnosci')
def _polityka(P):
    ctx, src = P.ctx, P.src
    P.hero([], kick='Informacje prawne', no_art=True)
    parts = []
    for sec in src.secs:
        P.begin(sec)
        inner = f'<h2 id="{sec.id}">{sec.title}</h2>' + B.prose_nodes(ctx, sec.nodes)
        for sub in sec.subs:
            inner += f'<h3 id="{sub.id}">{sub.title}</h3>' + B.prose_nodes(ctx, sub.nodes)
        parts.append(f'<section class="legal-section" aria-labelledby="{sec.id}">{inner}</section>')
        P.mark(sec)
    ctx.use('legal-prose')
    body = f'<div class="legal-prose">{"".join(parts)}</div>'
    ctx.cur_sec = src.secs[0].id
    rail = B.rail_layout(ctx, [(e['id'], e['text']) for e in src.toc], body, label='Spis treści')
    P.add(None, rail, aria=src.secs[0].id, kind='rail')

