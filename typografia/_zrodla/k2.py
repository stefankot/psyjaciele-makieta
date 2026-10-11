# -*- coding: utf-8 -*-
"""Definicje 24 punktów kategorii 2. Pole `apply` to dokładnie ten kod, który uruchamia przycisk w oknie „Po”."""
from texts import RAW, TA, TB, TC

CDN = {
    'typograf': 'https://cdn.jsdelivr.net/npm/typograf@7.8.0/dist/typograf.all.min.js',
    'hyphenopoly': 'https://cdn.jsdelivr.net/npm/hyphenopoly@6.1.0/min/Hyphenopoly_Loader.js',
    'texlinebreak': 'https://cdn.jsdelivr.net/npm/tex-linebreak@0.9.0/dist/lib.js',
    'opentype': 'https://cdn.jsdelivr.net/npm/opentype.js@2.0.0/dist/opentype.min.js',
}
FONT_WOFF = 'https://cdn.jsdelivr.net/gh/adobe-fonts/source-serif@4.005R/WOFF/TTF/SourceSerif4-Regular.ttf.woff'
HYPH_DIR = 'https://cdn.jsdelivr.net/npm/hyphenopoly@6.1.0/min/'

# Inicjalizacja Hyphenopoly (loader nadpisuje window.Hyphenopoly, więc konfiguruje się po jego załadowaniu)
HYPH_INIT = r'''Hyphenopoly.config({
  require: { pl: 'FORCEHYPHENOPOLY' },            // zawsze własne wzorce, nie natywne
  paths: {
    maindir: '%s',
    patterndir: '%s',
  },
  setup: {
    CORScredentials: 'omit',                        // CDN odpowiada z Access-Control-Allow-Origin: *
    hide: 'none',
    selectors: { '.hyph': { minWordLength: 5, leftmin: 2, rightmin: 3 } },
  },
});''' % (HYPH_DIR, HYPH_DIR + 'patterns/')

HELPERS = r'''function mapText(el, fn) {                       // zmienia tylko węzły tekstowe, znaczniki zostają
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode()); ) n.nodeValue = fn(n.nodeValue);
}'''

def pp(t):
    return '<p>%s</p>' % t

K2 = []
def add(**kw):
    kw.setdefault('base', ''); kw.setdefault('css', ''); kw.setdefault('libs', [])
    kw.setdefault('note', ''); kw.setdefault('tools', []); kw.setdefault('marks', False)
    kw.setdefault('wide', False); kw.setdefault('sample', ''); kw.setdefault('uses_helper', False)
    K2.append(kw)

add(id='P2-01', lvl='mikro', cost='niski', libs=['typograf'], marks=True,
    why=("Jednoliterowy spójnik lub przyimek na końcu wiersza (a, i, o, u, w, z) jest polskim błędem składu; po takim wyrazie wstawiamy spację "
         "niełamliwą. Reguła nie pochodzi z książek, tylko z polskiej praktyki DTP."),
    base=".tekst { max-inline-size: min(100%, 24em); }",
    raw=pp(RAW['P2-01']),
    apply=r'''function (el) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');                                   // tylko reguły wybrane niżej
  tp.enableRule('common/nbsp/afterShortWord');
  tp.setSetting('common/nbsp/afterShortWord', 'lengthShortWord', 1);   // tylko wyrazy jednoliterowe
  el.innerHTML = tp.execute(el.innerHTML);
}''',
    note="Najlepiej zastosować w buildzie, wtedy przeglądarka nie dostaje ani biblioteki, ani przetwarzania. Dwuliterowe przyimki (do, na, po, za) są opcjonalne i poza pokazem.")

add(id='P2-02', lvl='mikro', cost='niski', libs=['typograf'], uses_helper=True,
    why=("Proste cudzysłowy z klawiatury i apostrofy nie są znakami typograficznymi. Polski skład używa „…” na zewnątrz i «…» wewnątrz (rozstrzygnięcie K-08), "
         "a apostrof zapisuje się jako ’."),
    raw=pp(RAW['P2-02']),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    apply=r'''function (el) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');
  tp.enableRule('common/punctuation/quote');         // "…" → „…”, wewnętrzne «…»
  tp.enableRule('common/punctuation/apostrophe');    // ' → ’ między literami
  el.innerHTML = tp.execute(el.innerHTML);
  mapText(el, s => s.replace(/(\p{L})'(?=\p{L})/gu, '$1\u2019'));   // apostrofy, których reguła nie złapała
}''',
    note="Typograf zamienił tylko pierwszy apostrof w „rock'n'rollu”; drugi domyka własny wyrażenie regularne. Przypadki nietypowe (cale, minuty łuku, ’80 jako rok) wymagają przeglądu ręcznego.")

add(id='P2-03', lvl='mikro', cost='niski', uses_helper=True, marks=True,
    why=("Wtrącenie oddziela się półpauzą ze spacjami (rozstrzygnięcie K-01); dywiz („-”), dwa dywizy i pauza em w tym samym znaczeniu mają jeden kształt. "
         "Przed półpauzą stawiamy spację niełamliwą, żeby wiersz nie zaczynał się od myślnika."),
    raw=pp(RAW['P2-03'] + ' Słownik polsko-niemiecki zostaje bez zmian.'),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    apply=r'''function (el) {
  mapText(el, s => s.replace(/\s(?:-{1,2}|\u2014)\s/g, '\u00A0\u2013 '));   // „ - ”, „ -- ”, „ — ” → „ – ”
}''',
    note="Dywiz w złożeniach („polsko-niemiecki”) i znak minus przy liczbach nie mają spacji po obu stronach, więc wyrażenie ich nie dotyka. Pauza em w dialogach to osobna konwencja.")

add(id='P2-04', lvl='mikro', cost='niski', uses_helper=True,
    why=("Zakresy liczb (strony, lata, godziny) oddziela półpauza bez spacji, nie dywiz. Daty ISO, numery telefonów i identyfikatory trzeba pominąć."),
    raw=pp(RAW['P2-04']),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    apply=r'''function (el) {
  const ZAKRES = /(?<![\d-])(?!\d{2}-\d{3}(?!\d))(\d+)\s?[-\u2013\u2014]\s?(\d+)(?![\d-])/g;   // dwie liczby; bez trzeciego członu i kodów pocztowych
  mapText(el, s => s.replace(ZAKRES, '$1\u2013$2'));
}''',
    note="Wzorzec odrzuca ciągi z więcej niż dwiema liczbami (2026-10-11, 22-555-12-34) i kody pocztowe (00-950). Lookbehind (`(?<!…)`) działa od Safari 16.4; w starszych trzeba przepisać wzorzec.")

add(id='P2-05', lvl='mikro', cost='niski', libs=['typograf'], uses_helper=True,
    why=("Trzy kropki to jeden znak, wielokrotne znaki wykrzyknienia i zapytania to interpunkcja notacyjna, której Bringhurst odradza (5.2.8)."),
    raw=pp(RAW['P2-05']),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    apply=r'''function (el) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');
  tp.enableRule('common/punctuation/hellip');                // ... → …
  tp.enableRule('common/punctuation/delDoublePunctuation');  // ?? → ?
  el.innerHTML = tp.execute(el.innerHTML);
  mapText(el, s => s.replace(/!{2,}/g, '!'));   // wielokrotne wykrzykniki: własny wzór, tylko w tekście
}''',
    note="Zmiana „!!!” na „!” to decyzja redakcyjna, nie czysto typograficzna: odbiera autorowi ekspresję.")

add(id='P2-06', lvl='mikro', cost='niski', libs=['typograf'], uses_helper=True,
    why=("Znak × (nie litera x), minus (−, nie dywiz), ± i ≠ oraz ułamki ½ ¼ ¾ są osobnymi znakami z fontu, nie przybliżeniami z klawiatury."),
    raw=pp(RAW['P2-06']),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    apply=r'''function (el) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');
  ['common/number/times', 'common/number/mathSigns', 'common/number/fraction'].forEach(r => tp.enableRule(r));
  el.innerHTML = tp.execute(el.innerHTML);
  mapText(el, s => s.replace(/(^|\s)-(?=\d)/g, '$1\u2212'));   // minus przed liczbą, tylko w tekście
}''',
    note="Biała lista kontekstów jest konieczna: „x” w nazwach (np. „Windows x64”) nie jest znakiem mnożenia, a „1/2” w dacie nie jest ułamkiem.")

add(id='P2-07', lvl='mikro', cost='niski', libs=['typograf'], marks=True, uses_helper=True,
    why=("Stopień (°), prime (′ ″ dla minut, cali), znaki ©, ® i ™ mają własne kody w foncie; zwykły apostrof i cudzysłów są w tych miejscach błędne."),
    raw=pp(RAW['P2-07']),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    apply=r'''function (el) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');
  ['common/symbols/cf', 'common/symbols/copy'].forEach(r => tp.enableRule(r));   // 20 C → 20 °C, (c) → ©
  el.innerHTML = tp.execute(el.innerHTML);
  mapText(el, s => s.replace(/(\d)'(?=\d)/g, '$1\u2032')      // 5'2" → 5′2″ (tylko w tekście, nie w atrybutach)
                    .replace(/(\d)"/g, '$1\u2033'));
}''',
    note="Odróżnianie cali (″) od cudzysłowów prostych wymaga kontekstu liczbowego; wzorzec poprawnie obsługuje tylko zapis „liczba + znak”.")

add(id='P2-08', lvl='mikro', cost='średni', libs=['typograf'], uses_helper=True, marks=True,
    why=("Liczba oddzielona od jednostki, skrót od numeru i paragraf od liczby tworzą jedną jednostkę znaczeniową; łamanie wiersza między nimi "
         "jest błędem składu."),
    raw=pp(RAW['P2-08'] + ' Zob. także poz. 7, nr 12 oraz 3 kg mąki.'),
    base=".tekst { max-inline-size: min(100%, 22em); }",
    apply=r'''function (el) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');
  ['common/nbsp/afterNumber', 'common/nbsp/afterSectionMark', 'common/nbsp/afterShortWord']
    .forEach(r => tp.enableRule(r));
  tp.setSetting('common/nbsp/afterShortWord', 'lengthShortWord', 1);
  el.innerHTML = tp.execute(el.innerHTML);
  const SKROTY = /\b(str|rozdz|ul|ust|pkt|poz|ok|np|tj|tys|mln)\.\s/g;                    // skrót + dalszy wyraz
  const JEDNOSTKI = /(\d)\s(mm|cm|km|kg|g|m|l|ml|tys\.|mln|zł|r\.)(?!\p{L})/gu;            // liczba + jednostka
  mapText(el, s => s.replace(SKROTY, '$1.\u00A0').replace(JEDNOSTKI, '$1\u00A0$2'));
}''',
    note="Typograf zna „zł”, „r.” i „§”, ale nie polskie skróty (str., rozdz., ul., tys.) ani jednostki metryczne; ich lista jest własna i trzeba ją utrzymywać.")

add(id='P2-09', lvl='mikro', cost='niski', libs=['typograf'], marks=True,
    why=("Duże liczby grupuje się po trzy cyfry cienką spacją niełamliwą, żeby oko wychwytywało rząd wielkości; numery telefonów dzieli się wg przyjętego wzoru."),
    raw=pp(RAW['P2-09']),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    apply=r'''function (el, ui) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');
  tp.enableRule('common/number/digitGrouping');               // grupy po 3 cyfry, U+202F
  el.innerHTML = tp.execute(el.innerHTML);
  const f = new Intl.NumberFormat('pl-PL');
  const v = n => f.format(n).replace(/\u00A0/g, '⍽').replace(/\u202F/g, '⸱');
  ui.say('Intl.NumberFormat("pl-PL"): 2400 → "' + v(2400) + '", 12400 → "' + v(12400) + '", 1250000 → "' + v(1250000) + '"');
}''',
    note=("Test w tej przeglądarce (komunikat pod oknem „Po”) rozstrzyga wątpliwość „czy `pl-PL` grupuje liczby czterocyfrowe”. Typograf grupuje od pięciu cyfr; "
          "numerów telefonów w układzie 2-3-2-2 nie rozpoznaje."))

add(id='P2-10', lvl='mikro', cost='średni',
    why=("Ciąg wersalików w tekście ciągłym jest zbyt ciężki; skróty (ONZ, NATO) składa się kapitalikami, a wyjątki stanowią m.in. kody krajów i inicjały."),
    raw=pp(RAW['P2-10']),
    base=".tekst { max-inline-size: min(100%, 30em); }",
    css=".tekst abbr.akr {\n  font-variant-caps: all-small-caps;\n  letter-spacing: .06em;\n}",
    apply=r'''function (el) {
  const WYJATKI = new Set(['PL', 'UK', 'US']);                          // kody krajów zostają wersalikami
  const SKROT = /(?<!\p{L})\p{Lu}{2,}(?!\p{L})/gu;                      // 2+ wielkie litery obok siebie
  el.innerHTML = el.innerHTML.replace(/(>|^)([^<]+)/g, (m, g, txt) =>   // tylko tekst między znacznikami
    g + txt.replace(SKROT, s => WYJATKI.has(s) ? s : '<abbr class="akr">' + s + '</abbr>'));
}''',
    note="Wersaliki w nagłówkach i podpisach trzeba pominąć (nie mają sensu jako akronimy). Sprzątanie: przywrócenie oryginalnego HTML (przycisk „Przywróć”).")

add(id='P2-11', lvl='mikro', cost='niski', uses_helper=True, marks=True,
    why=("Inicjały imion składa się z cienką spacją między literami i spacją niełamliwą przed nazwiskiem, żeby nazwisko nie zostało oderwane od inicjałów."),
    raw=pp(RAW['P2-11']),
    base=".tekst { max-inline-size: min(100%, 20em); }",
    apply=r'''function (el) {
  const INICJALY = /((?:\p{Lu}\.\s?)+)(?=\p{Lu}\p{Ll}+)/gu;            // „J. R. R. ” + nazwisko
  mapText(el, s => s.replace(INICJALY,
    m => m.replace(/\.\s?/g, '.\u202F').replace(/\u202F$/, '\u00A0')));  // cienka spacja wewnątrz, nbsp przed nazwiskiem
}''',
    note="Skróty typu „M. in.” albo „J. Kowalski” na początku zdania wymagają wyjątków. Użyto U+202F (wąska spacja niełamliwa); font Source Serif 4 ją zawiera (sprawdzone opentype.js).")

add(id='P2-12', lvl='mikro', cost='niski', marks=True,
    why=("Ostatni wiersz akapitu z jednym krótkim wyrazem (spójnikiem lub zaimkiem) wygląda jak błąd. Wiążąc dwa ostatnie wyrazy, wymuszamy "
         "przeniesienie krótkiego wyrazu razem z poprzednim."),
    base=".tekst { max-inline-size: min(100%, 22em); }",
    raw=''.join(pp(t) for t in [
        "Pracownia, o której tu mowa, istniała naprawdę tylko w wyobraźni autora i nikt jej nie zamknął, bo nikt jej nie otworzył, a mimo to",
        "Zecer sprawdzał ostatni wiersz każdego akapitu, bo to właśnie tam skład zdradza pośpiech i brak uwagi, i nic nie dawało mu spokoju, więc",
        "Dobra strona zaczyna się od decyzji, których czytelnik nie zauważa, a kończy na tym, że wszystko leży tak, jak powinno leżeć u nas",
        "Nikt nie liczył godzin dopasowywania jednego wiersza, ale wszyscy zgadzali się, że warto było je poświęcić na to, co tu"]),
    stats=['widowwords'],
    apply=r'''function (el) {
  el.querySelectorAll('p').forEach(p => {
    const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
    let last = null;
    for (let n; (n = w.nextNode()); ) last = n;
    if (last) last.nodeValue = last.nodeValue.replace(/\s(\S{1,4})\s*$/, '\u00A0$1');   // ostatni wyraz ≤ 4 znaki
  });
}''',
    note="Przy bardzo wąskich kolumnach niełamliwy ciąg może wystawać. `text-wrap: pretty` (P1-11) robi to natywnie, ale nie działa w Firefoksie.")

add(id='P2-13', lvl='mikro', cost='średni', libs=['hyphenopoly'], wide=False, stats=['softhyph', 'hyphlines'],
    why=("Justowany tekst w wąskiej kolumnie bez dzielenia wyrazów rozciąga odstępy; polskie wyrazy są długie. Hyphenopoly dostarcza wzorce polskie "
         "niezależnie od słownika przeglądarki (P1-12)."),
    base=".tekst { max-inline-size: min(100%, 19em); text-align: justify; }",
    raw=pp(TC + ' Nieprzejednany przedstawiciel rozmaitości konstytucyjnych bezpardonowo odrzucił jednoznacznie sformułowaną propozycję.'),
    apply=r'''async function (el) {
  const h = await Hyphenopoly.hyphenators.pl;                 // funkcja dzieląca (wzorce pl.wasm)
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode()); ) n.nodeValue = h(n.nodeValue, '.hyph');   // wstawia U+00AD w środku wyrazów
}''',
    note=("Miękkie łączniki trafiają do DOM, więc kopiowanie i wyszukiwanie mogą zachowywać się inaczej (do sprawdzenia w przeglądarkach docelowych). "
          "Sprzątanie: przywrócenie oryginalnego HTML."))

add(id='P2-14', lvl='mikro', cost='wysoki', libs=['hyphenopoly', 'texlinebreak'], stats=['lines'],
    why=("Algorytm Knutha–Plassa wybiera podział na wiersze dla całego akapitu naraz, nie wiersz po wierszu, więc justowanie ma równiejsze odstępy niż przeglądarka. "
         "Rozstrzygnięcie K-06: korekta tylko odstępów międzywyrazowych, bez skalowania glifów."),
    base=".tekst { max-inline-size: min(100%, 19em); text-align: justify; hyphens: manual; }",
    raw=pp(TA),
    apply=r'''async function (el) {
  await document.fonts.ready;                                       // pomiar tylko po załadowaniu kroju
  const h = await Hyphenopoly.hyphenators.pl;
  const hyphenate = w => h(w, '.hyph').split('\u00AD');             // sylaby dla tex-linebreak
  const ps = [...el.querySelectorAll('p')];
  const { justifyContent, unjustifyContent } = texLineBreak_lib;
  justifyContent(ps, hyphenate);
  let szer = el.clientWidth;
  const ro = new ResizeObserver(() => {                             // po zmianie szerokości: układ od nowa
    if (el.clientWidth === szer) return;
    szer = el.clientWidth;
    ps.forEach(unjustifyContent);
    justifyContent(ps, hyphenate);
  });
  ro.observe(el);
  return () => { ro.disconnect(); ps.forEach(unjustifyContent); };
}''',
    note=("Wzorce dzielenia dostarczone z tex-linebreak 0.9.0 są tylko angielskie, dlatego użyto sylab z Hyphenopoly. Biblioteka mierzy tekst, ustawia odstępy na wiersz i nie radzi sobie ze złożonym "
          "inline (obrazy, kod). Skopiowany tekst może zawierać wstawione łączniki i znaki podziału: do sprawdzenia."))

add(id='P2-15', lvl='mikro', cost='średni', stats=['hangjs'], sample='guide',
    why=("Cudzysłów lub nawias otwierający na początku akapitu powinien wisieć w marginesie (M-74); Chrome i Firefox nie mają `hanging-punctuation`, więc robi to skrypt."),
    raw=''.join(pp(t) for t in ["„Typografia istnieje po to, żeby tekst dało się czytać” – mówił zecer – „a nie po to, żeby ją podziwiano.”",
                                "(Nawias otwierający także może wisieć w marginesie.)",
                                "«Cudzysłów francuski» wewnątrz polskiego tekstu.", "Zwykły akapit zaczyna się od litery."]),
    apply=r'''async function (el) {
  await document.fonts.ready;
  const ctx = document.createElement('canvas').getContext('2d');
  el.querySelectorAll('p').forEach(p => {
    const t = p.firstChild;
    const m = t && t.nodeType === 3 && /^[„"«(\[‚]/.exec(t.nodeValue);   // znak otwierający
    if (!m) return;
    const cs = getComputedStyle(p);
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const s = document.createElement('span');
    s.textContent = m[0];
    s.style.marginInlineStart = -ctx.measureText(m[0]).width + 'px';   // szerokość znaku wystaje w margines
    t.nodeValue = t.nodeValue.slice(1);
    p.prepend(s);
  });
}''',
    note="Zmiana kroju wymaga ponownego pomiaru. Skrypt obsługuje tylko akapity zaczynające się znakiem otwierającym; wiszące znaki na końcu wiersza (`last`) wymagałyby pomiaru każdego wiersza.")

add(id='P2-16', lvl='mikro', cost='niski', stats=[], sample='',
    why=("Miarę ocenia się liczbą znaków w wierszu, a nie szerokością w pikselach; licznik pozwala skontrolować, czy akapit mieści się w przedziale 45–75."),
    base=".tekst { position: relative; padding-inline-end: 28px; }",
    raw=pp(TA) + pp(TB),
    css=".tekst .cnt {\n  position: absolute;\n  right: 4px;\n  font: 600 11px/24px var(--mono);\n  color: var(--accent);\n}",
    apply=r'''function (el, ui) {
  const draw = () => {
    el.querySelectorAll('.cnt').forEach(n => n.remove());
    const baza = el.getBoundingClientRect().top;
    const liczby = [];
    el.querySelectorAll('p').forEach(p => {
      const wiersze = [];                                           // { y, n } : pozycja pionowa i liczba znaków
      const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
      for (let t; (t = w.nextNode()); ) {
        const r = document.createRange();
        for (let i = 0; i < t.length; i++) {
          r.setStart(t, i); r.setEnd(t, i + 1);
          const b = r.getClientRects()[0];
          if (!b) continue;
          const o = wiersze[wiersze.length - 1];
          if (o && Math.abs(o.y - b.top) < 4) o.n++; else wiersze.push({ y: b.top, n: 1 });
        }
      }
      wiersze.forEach((o, i) => {
        const s = document.createElement('span');
        s.className = 'cnt'; s.textContent = o.n; s.style.top = (o.y - baza) + 'px';
        el.append(s);
        if (i < wiersze.length - 1) liczby.push(o.n);               // ostatni wiersz akapitu pomijamy
      });
    });
    const sr = Math.round(liczby.reduce((a, b) => a + b, 0) / liczby.length);
    ui.say('znaków w wierszu: średnio ' + sr + ', zakres ' + Math.min(...liczby) + '\u2013' + Math.max(...liczby));
  };
  document.fonts.ready.then(draw);
  const ro = new ResizeObserver(draw);
  ro.observe(el);
  return () => ro.disconnect();
}''',
    note="Liczone są znaki wraz ze spacjami i interpunkcją (jak w zasadzie M-01). Narzędzie diagnostyczne: nie zmienia typografii, tylko ją mierzy.")

add(id='P2-17', lvl='makro', cost='średni', stats=[], wide=True,
    tools=[dict(type='toggle', cls='show-grid', label='Pokaż siatkę 8 px')],
    why=("Obrazy i ramki o dowolnej wysokości przesuwają kolejne wiersze względem siatki bazowej. Dopełnienie wysokości do wielokrotności interlinii przywraca rytm."),
    base=(".tekst { max-inline-size: min(100%, 64ch); }\n.tekst .obr { margin: 0 0 16px; border: 1px solid var(--ink); background: var(--tint); display: grid; place-items: center; font-size: .85em; }"),
    raw=(pp(TC) + '<figure class="obr" style="height:83px">ilustracja 83 px</figure>' + pp("Akapit po obrazie, który nie mieści się w całych wierszach.")
         + '<figure class="obr" style="height:117px">ilustracja 117 px</figure>' + pp("Drugi akapit po obrazie.")),
    apply=r'''function (el, ui) {
  const U = 24;                                                      // krok rytmu = interlinia
  const dopasuj = () => {
    el.querySelectorAll('figure').forEach(f => {
      f.style.marginBlockEnd = '0px';
      const h = f.getBoundingClientRect().height;
      f.style.marginBlockEnd = (Math.ceil(h / U) * U - h) + 'px';    // dopełnienie do wielokrotności U
    });
    const baza = el.getBoundingClientRect().top;
    const dp = [...el.querySelectorAll('figure + p')].map(p => Math.round((p.getBoundingClientRect().top - baza) % U));
    ui.say('przesunięcie akapitów po obrazach względem siatki: ' + dp.join(' px, ') + ' px');
  };
  let szer = el.clientWidth;
  const ro = new ResizeObserver(() => { if (el.clientWidth !== szer) { szer = el.clientWidth; dopasuj(); } });
  ro.observe(el);
  document.fonts.ready.then(dopasuj);
  return () => ro.disconnect();
}''',
    note="Przesunięcie 0 px oznacza, że wiersz po obrazie leży na tej samej linii bazowej co wiersze przed nim. Drugi pomiar (okno „Przed”) widoczny jest pod nim.")

add(id='P2-18', lvl='makro', cost='średni', wide=True,
    why=("Przypisy boczne czyta się bez przewracania strony, ale gdy kilka odsyłaczy leży blisko siebie, notatki zachodzą na siebie. Skrypt układa je jedna pod drugą."),
    base=(".tekst { position: relative; padding-inline-end: 36%; }\n"
          ".tekst .przypis { font-style: italic; font-size: .9em; }\n"
          ".tekst .przypis::before { content: \" [przypis: \"; }\n.tekst .przypis::after { content: \"]\"; }"),
    css=".tekst .nota {\n  position: absolute;\n  inset-inline-end: 0;\n  inline-size: 32%;\n  font-size: .85em;\n  line-height: 24px;\n}\n.tekst .nr { font-size: .75em; line-height: 0; vertical-align: super; }",
    raw=(pp("Pierwsze zdanie zawiera odsyłacz<span class=\"przypis\">Przypis pierwszy, dość długi, by zająć kilka wierszy w marginesie i zepchnąć następny.</span>, "
            "a zaraz po nim drugi<span class=\"przypis\">Przypis drugi zaczyna się w tym samym miejscu, co pierwszy.</span> oraz trzeci<span class=\"przypis\">Trzeci krótki.</span>.")
         + pp(TC)),
    apply=r'''function (el) {
  const nr = [];
  el.querySelectorAll('.przypis').forEach((span, i) => {
    const sup = document.createElement('sup');
    sup.className = 'nr'; sup.textContent = i + 1;
    const nota = document.createElement('aside');
    nota.className = 'nota'; nota.id = el.closest('.pt').id + '-n' + (i + 1);
    nota.setAttribute('role', 'note');
    nota.innerHTML = '<b>' + (i + 1) + '</b> ' + span.innerHTML;
    sup.setAttribute('aria-describedby', nota.id);                 // powiązanie dla czytników ekranu
    span.replaceWith(sup);
    el.append(nota);
    nr.push({ sup, nota });
  });
  const uloz = () => {
    let dol = 0;
    const baza = el.getBoundingClientRect().top;
    nr.forEach(({ sup, nota }) => {
      const gora = Math.max(sup.getBoundingClientRect().top - baza, dol + 8);   // nie zachodzi na poprzednią
      nota.style.top = gora + 'px';
      dol = gora + nota.offsetHeight;
    });
  };
  document.fonts.ready.then(uloz);
  const ro = new ResizeObserver(uloz);
  ro.observe(el);
  return () => ro.disconnect();
}''',
    note=("Alternatywa bez JS: anchor positioning z `position-try-fallbacks` (P1-22), ale bez gwarancji braku zachodzenia notatek. W oknie „Przed” przypisy stoją w tekście w nawiasach. "
          "Na bardzo wąskich ekranach należałoby je zwinąć do okna zależnego od kliknięcia."))

add(id='P2-19', lvl='własne', cost='średni', stats=[],
    why=("W tabeli liczb o różnej liczbie miejsc po przecinku wyrównanie do prawej nie ustawia przecinków jeden pod drugim. Trzeba wyrównać do separatora dziesiętnego."),
    base=(".tekst table { border-collapse: collapse; font-variant-numeric: lining-nums tabular-nums; }\n.tekst td { padding: 4px 24px 4px 0; }\n"
          ".tekst .liczba { text-align: right; }"),
    css=".tekst .u { display: inline-block; min-inline-size: var(--u, 0); text-align: left; }",
    raw=('<table><thead><tr><th>Pozycja</th><th class="liczba">Wartość</th></tr></thead><tbody>'
         '<tr><td>Nakład</td><td class="liczba">2 400</td></tr><tr><td>Cena</td><td class="liczba">12,5</td></tr>'
         '<tr><td>Rabat</td><td class="liczba">3,25</td></tr><tr><td>Waga</td><td class="liczba">118</td></tr>'
         '<tr><td>Tolerancja</td><td class="liczba">0,075</td></tr></tbody></table>'),
    apply=r'''function (el) {
  el.querySelectorAll('td.liczba').forEach(td => {
    const [c, u = ''] = td.textContent.trim().split(',');
    td.innerHTML = '<span class="c">' + c + '</span><span class="u">' + (u ? ',' + u : '') + '</span>';
  });
  const szer = Math.max(...[...el.querySelectorAll('.u')].map(s => s.getBoundingClientRect().width));
  el.style.setProperty('--u', szer + 'px');                         // wspólna szerokość części ułamkowej
}''',
    note="Dostępność: tekst komórki się nie zmienia, spany są tylko stylistyczne. Alternatywa w CSS: stała liczba miejsc po przecinku i `tabular-nums`.")

add(id='P2-20', lvl='makro', cost='niski', stats=[], wide=True,
    why=("W długim dokumencie bieżąca „żywa pagina” (nazwa sekcji lub numer) orientuje czytelnika; w sieci nie ma numerów stron, więc przybliżeniem jest numer sekcji (A-48, A-49: kategoria 3)."),
    base=".tekst { max-block-size: 192px; max-inline-size: min(100%, 64ch); overflow: auto; }",
    css=(".tekst .zywa {\n  position: sticky;\n  top: 0;\n  background: var(--panel);\n  border-block-end: 1px solid var(--ink);\n  font-variant-caps: all-small-caps;\n  letter-spacing: .08em;\n}"),
    raw=''.join('<h3>%s</h3>%s' % (h, pp(t)) for h, t in [
        ('Miara', TC), ('Interlinia', TB), ('Kapitaliki', TC), ('Ligatury', TB)]),
    apply=r'''function (el) {
  const zywa = document.createElement('div');
  zywa.className = 'zywa';
  zywa.setAttribute('aria-hidden', 'true');                        // duplikat treści nagłówka
  el.prepend(zywa);
  const h = [...el.querySelectorAll('h3')];
  const ustaw = i => { zywa.textContent = '§ ' + (i + 1) + ' · ' + h[i].textContent; };
  ustaw(0);
  const io = new IntersectionObserver(wpisy => {
    wpisy.forEach(e => { if (e.isIntersecting) ustaw(h.indexOf(e.target)); });
  }, { root: el, rootMargin: '0px 0px -80% 0px' });               // górne 20 % okna przewijania
  h.forEach(x => io.observe(x));
  return () => io.disconnect();
}''',
    note="Przewiń okno „Po”, żeby zobaczyć zmianę. Alternatywa bez JS: scroll-driven animations (Chrome 115, Safari 26, Firefox: za flagą/preview; do sprawdzenia).")

add(id='P2-21', lvl='makro', cost='niski', stats=[], wide=True, base=".tekst { max-inline-size: min(100%, 64ch); }",
    why=("Spis treści generowany z nagłówków nie rozjeżdża się z treścią i daje czytelnikowi plan dokumentu; powinien powstawać w buildzie, a w przeglądarce jest tylko ulepszeniem."),
    css=".tekst nav ol { margin: 0 0 24px; padding-inline-start: 2em; list-style-position: outside; }",
    raw=''.join('<h3>%s</h3>%s' % (h, pp(t)) for h, t in [
        ('Miara', "Wiersz nie powinien być za długi."), ('Interlinia', "Wiersze nie powinny się zlewać."), ('Kapitaliki', "Skróty składamy kapitalikami.")]),
    apply=r'''function (el) {
  const nav = document.createElement('nav');
  nav.setAttribute('aria-label', 'Spis treści');
  const ol = document.createElement('ol');
  [...el.querySelectorAll('h3')].forEach((h, i) => {
    h.id = el.closest('.pt').id + '-r' + (i + 1);                  // unikalne id w całej stronie
    const li = document.createElement('li');
    li.innerHTML = '<a href="#' + h.id + '">' + h.textContent + '</a>';
    ol.append(li);
  });
  nav.append(ol);
  el.prepend(nav);
}''',
    note="Bez JS spisu nie ma, dlatego w produkcji generuje się go w buildzie lub w CMS. Powiązanie z numeracją nagłówków (A-68) pominięto.")

add(id='P2-22', lvl='mikro', cost='średni', stats=[],
    why=("Prawy brzeg tekstu wyrównanego do lewej ma mieć falisty, nieregularny kształt; ciągi kolejno wydłużających się lub skracających się wierszy tworzą klin lub „schody”, "
         "które oko odbiera jako skazę."),
    base=".tekst { position: relative; max-inline-size: min(100%, 17em); }",
    css=".tekst .kr { position: absolute; inline-size: 6px; background: var(--accent); }",
    raw=pp(TA) + pp(TB),
    apply=r'''function (el, ui) {
  const skanuj = () => {
    el.querySelectorAll('.kr').forEach(n => n.remove());
    const b0 = el.getBoundingClientRect();
    let kliny = 0;
    el.querySelectorAll('p').forEach(p => {
      const r = document.createRange();
      r.selectNodeContents(p);
      const wiersze = [];                                           // jeden wpis na wiersz: góra, wysokość i prawy brzeg
      [...r.getClientRects()].forEach(b => {
        const w = wiersze.find(x => Math.abs(x.top - b.top) < 4);
        if (w) w.right = Math.max(w.right, b.right); else wiersze.push({ top: b.top, h: b.height, right: b.right });
      });
      const d = wiersze.map(x => x.right).slice(0, -1);              // ostatni wiersz akapitu pomijamy
      for (let i = 0, bieg = 1, znak = 0; i < d.length; i++) {
        const z = i ? Math.sign(Math.round(d[i] - d[i - 1])) : 0;
        if (z && z === znak) bieg++; else { bieg = z ? 2 : 1; znak = z; }
        if (bieg >= 4 && (i + 1 === d.length || Math.sign(Math.round(d[i + 1] - d[i])) !== znak)) {
          kliny++;                                                    // klin: ≥ 4 kolejne wiersze w jednym kierunku
          for (let k = i - bieg + 1; k <= i; k++) {
            const m = document.createElement('i');
            m.className = 'kr';
            m.style.top = (wiersze[k].top - b0.top) + 'px'; m.style.height = wiersze[k].h + 'px';
            m.style.left = (wiersze[k].right - b0.left + 4) + 'px';
            el.append(m);
          }
        }
      }
    });
    ui.say('wykryte kliny (≥ 4 wiersze o monotonicznej długości): ' + kliny);
  };
  document.fonts.ready.then(skanuj);
  const ro = new ResizeObserver(skanuj);
  ro.observe(el);
  return () => ro.disconnect();
}''',
    note="Progi (cztery wiersze, tolerancja 1 px) dobrano empirycznie i nie są zaczerpnięte z książek; zmiana szerokości okna zmienia wynik. Narzędzie QA, nie korekta.")

add(id='P2-23', lvl='własne', cost='niski', libs=['typograf'], uses_helper=True, marks=True,
    why=("Zanim zacznie się składać, tekst trzeba oczyścić: podwójne spacje, tabulatory, spacje przed przecinkiem i kropką lub w nawiasie to ślady kopiowania, "
         "nie zamierzony skład."),
    base=".tekst { max-inline-size: min(100%, 30em); } .tekst .raw-space { white-space: pre-wrap; }",
    raw='<p class="raw-space">%s</p>' % RAW['P2-23'],
    apply=r'''function (el) {
  const tp = new Typograf({ locale: ['pl'] });
  tp.disableRule('*');
  ['common/space/delRepeatSpace', 'common/space/replaceTab', 'common/space/delBeforePunctuation',
   'common/space/delBeforeDot', 'common/space/afterComma', 'common/space/bracket']
    .forEach(r => tp.enableRule(r));
  el.innerHTML = tp.execute(el.innerHTML);
  mapText(el, s => s.replace(/\s+([.,;:!?])/g, '$1'));           // spacja przed znakiem na końcu akapitu
}''',
    note="Nie stosować w `<pre>` ani `<code>`. Reguła Typografa nie usuwa spacji przed kropką na samym końcu akapitu, dlatego dopisano wyrażenie regularne. W oknie „Przed” użyto `white-space: pre-wrap`, żeby podwójne spacje były widoczne.")

add(id='P2-24', lvl='własne', cost='średni', libs=['opentype'], stats=[], wide=True,
    why=("Zanim wybierze się font, trzeba sprawdzić, czy ma polskie litery i znaki typograficzne; brakujący glif zostanie zastąpiony znakiem z innego kroju, "
         "który zepsuje kolor strony."),
    raw=''.join(pp(t) for t in ["ąćęłńóśźż ĄĆĘŁŃÓŚŹŻ",
                                "„ ” « » ‚ ’ – — … × − ± ≠ ′ ″ ° © ® ™ ½ ¼ ¾ § ¶ №",
                                "⁂ ☞ ǆ"]),
    base=".tekst .pokrycie { border-collapse: collapse; font-variant-numeric: tabular-nums; } .tekst .pokrycie td { padding: 0 16px 0 0; }",
    css=".tekst .brak { color: var(--accent); font-weight: 700; }",
    apply=r'''async function (el, ui) {
  const buf = await (await fetch('%s')).arrayBuffer();
  const font = opentype.parse(buf);                                 // Source Serif 4 Regular, WOFF
  const znaki = [...new Set(el.textContent.replace(/\s/g, ''))];
  const wiersze = znaki.map(c => {
    const ok = font.charToGlyphIndex(c) > 0;
    return '<tr' + (ok ? '' : ' class="brak"') + '><td>' + c + '</td><td>U+' +
           c.codePointAt(0).toString(16).toUpperCase().padStart(4, '0') + '</td><td>' + (ok ? 'jest' : 'BRAK') + '</td></tr>';
  });
  el.innerHTML = '<table class="pokrycie">' + wiersze.join('') + '</table>';
  const brak = znaki.filter(c => font.charToGlyphIndex(c) === 0);
  ui.say('znaków: ' + znaki.length + ', brakuje: ' + brak.length + (brak.length ? ' (' + brak.join(' ') + ')' : ''));
}''' % FONT_WOFF,
    note="Biblioteka waży 245 kB (min) i parsuje cały plik fontu, więc nadaje się do QA przy zmianie kroju, nie do produkcji. Subsetting (pyftsubset, subset-font) działa w buildzie i jest poza pokazem.")

assert len(K2) == 24, len(K2)
