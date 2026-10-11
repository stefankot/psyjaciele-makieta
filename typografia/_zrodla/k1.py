# -*- coding: utf-8 -*-
"""Definicje 24 punktów kategorii 1 (CSS i HTML). Kod w polu `css` jest tym samym kodem, który steruje oknem „Po”."""
from texts import TA, TB, TC, QUOTE, QUOTE_SRC, VERSE, LIST

def P(t, cls=''):
    return '<p%s>%s</p>' % ((' class="%s"' % cls) if cls else '', t)

SHORT = ("Dobra strona zaczyna się od decyzji, których czytelnik nie zauważa. Nikt nie zatrzymuje się nad szerokością "
         "łamu ani nad odstępem między wierszami, a jednak to one decydują, czy tekst da się przeczytać do końca.")
SHORT2 = ("Pracownia drukowała około 40 tytułów rocznie. Nikt nie liczył, ile godzin kosztowało dopasowanie jednego "
          "wiersza, ale wszyscy zgadzali się, że warto.")

def canon_page(cls, H, t, e, f, s, caption, text=TA + ' ' + TB, drawing=True):
    """Strona z polem składu; liczby (w jednostkach szerokości strony) służą tylko do narysowania nakładki."""
    x0, y0, x1, y1 = s, t, 1 - e, H - f
    svg = ('<svg class="konstrukcja" viewBox="0 0 1 %.4f" preserveAspectRatio="none" aria-hidden="true">'
           '<path d="M0 0L1 %.4fM1 0L0 %.4f"/>'
           '<path d="M%.4f %.4fH%.4fV%.4fH%.4fZM%.4f %.4fL%.4f %.4fM%.4f %.4fL%.4f %.4f"/></svg>'
           % (H, H, H, x0, y0, x1, y1, x0, x0, y0, x1, y1, x1, y0, x0, y1))
    return ('<figure class="fig"><div class="strona %s"><div class="pole"><p>%s</p></div>%s</div>'
            '<figcaption>%s</figcaption></figure>' % (cls, text, svg if drawing else '', caption))

K1 = []
def add(**kw):
    kw.setdefault('base', ''); kw.setdefault('before', ''); kw.setdefault('css', '')
    kw.setdefault('stats', []); kw.setdefault('tools', []); kw.setdefault('note', '')
    kw.setdefault('wide', False); kw.setdefault('sup', 'pelne'); kw.setdefault('sample', '')
    K1.append(kw)

# ---------------------------------------------------------------------------------------------
add(id='P1-01', lvl='mikro', wide=True, stats=['chars'],
    why=("Zbyt długi wiersz gubi oko w drodze do następnego, zbyt krótki rwie rytm czytania. Tradycja książkowa zgadza się "
         "co do przedziału 45–75 znaków ze środkiem w okolicach 66; w CSS wystarczy ograniczyć szerokość bloku tekstu."),
    css=".tekst {\n  max-inline-size: min(64ch, 100%);\n}",
    html=P(TA) + P(TB),
    note=("Jednostka `ch` to szerokość cyfry „0”, nie przeciętnego znaku tekstu, więc liczba ch nie jest liczbą znaków w wierszu. "
          "W Source Serif 4 jeden ch mieści średnio ok. 1,04 znaku tekstu polskiego, dlatego zamiast 66ch użyto 64ch, co daje ok. 66 znaków "
          "(licznik w nagłówku okna pokazuje pomiar). Przy innym foncie wartość trzeba skalibrować od nowa."))

add(id='P1-02', lvl='mikro', stats=['lh'],
    why=("Ciasna interlinia zlewa wiersze, zbyt luźna rozrywa akapit na pasy. Dla kroju szeryfowego i miary około 66 znaków "
         "dobrze działa 1,4–1,5; im dłuższy wiersz, tym większa potrzebna interlinia."),
    before=".tekst { line-height: 1.1; }",
    css=(".tekst {\n  --lh: 1.5;               /* krój szeryfowy, miara ok. 60–70 znaków */\n"
         "  line-height: var(--lh);  /* bezwymiarowa: potomkowie o innym rozmiarze liczą od własnego */\n}"),
    html=P(SHORT) + P(SHORT2),
    note="Wartość bezwymiarowa jest dziedziczona jako mnożnik; `24px` zostałoby przekazane potomkom jako stała wysokość.")

add(id='P1-03', lvl='makro', wide=True, stats=['h8'], sample='guide8',
    tools=[dict(type='toggle', cls='show-grid', label='Pokaż siatkę 8 px')],
    why=("Jeśli wszystkie wysokości (interlinia, nagłówki, odstępy) są wielokrotnością jednej jednostki, wiersze sąsiednich kolumn "
         "leżą na wspólnych liniach, a układ zyskuje stały rytm pionowy."),
    base=".tekst { max-inline-size: min(100%, 64ch); }",
    before=(".tekst h3 { font-size: 1.35em; line-height: 1.2; margin: .9em 0 .35em; }\n"
            ".tekst p { line-height: 1.45; margin: 0 0 1.1em; }"),
    css=(".tekst { --u: 8px; }\n"
         ".tekst h3 {\n  font-size: 1.5em;\n  line-height: calc(var(--u) * 4);\n"
         "  margin: calc(var(--u) * 3) 0 var(--u);\n}\n"
         ".tekst p {\n  line-height: calc(var(--u) * 3);\n  margin: 0 0 calc(var(--u) * 3);\n}"),
    html="<h3>Rytm pionowy</h3>" + P(SHORT) + "<h3>Odstępy jako kroki</h3>" + P(SHORT2),
    note=("Wysokość całego bloku w oknie „Po” jest wielokrotnością 8 px; w oknie „Przed” zwykle nie jest. Zamiast zmiennej `--u` "
          "można pisać `1lh` (jedna interlinia), jeśli wystarcza wsparcie jednostki `lh` (Firefox od 120)."))

add(id='P1-04', lvl='mikro',
    why=("Rozmiary kroju powinny tworzyć skalę o stałej proporcji (np. 2:3 albo ciąg Fibonacciego), a poziomy hierarchii różnić się "
         "wyraźnie. Jedenaście niemal równych rozmiarów to brak decyzji, nie skala."),
    before=(".tekst h3 { font-size: 1.15em; }\n.tekst h4 { font-size: 1.1em; }\n.tekst h5 { font-size: 1.05em; }"),
    css=(".tekst {\n  --r: 1.5;                          /* proporcja skali (kwinta) */\n"
         "  --s0: 1em;\n  --s1: calc(var(--s0) * var(--r));\n  --s2: calc(var(--s1) * var(--r));\n}\n"
         ".tekst h5 { font-size: var(--s0); line-height: 24px; }\n"
         ".tekst h4 { font-size: var(--s1); line-height: 32px; }\n"
         ".tekst h3 { font-size: clamp(var(--s1), 1.2em + 1.2vw, var(--s2)); line-height: 40px; }"),
    html="<h3>Poziom pierwszy</h3><h4>Poziom drugi</h4><h5>Poziom trzeci</h5>" + P(SHORT2),
    note="`clamp()` pozwala nagłówkowi rosnąć płynnie między dwoma stopniami skali; tekst zasadniczy pozostaje na stałym rozmiarze.")

add(id='P1-05', lvl='mikro',
    why=("Zmiana kilku cech naraz (rozmiar, waga, kursywa, kolor, wersaliki) sprawia, że nagłówek krzyczy, a nie porządkuje. "
         "Rozstrzygnięcie K-07: jeden parametr na jedną różnicę, a wagę zmniejszamy, gdy rozmiar rośnie."),
    before=(".tekst h3 { font-size: 1.9em; font-weight: 800; font-style: italic; text-transform: uppercase; color: var(--accent); }\n"
            ".tekst h4 { font-size: 1.35em; font-weight: 800; font-style: italic; text-decoration: underline; }\n"
            ".tekst em { font-style: italic; font-weight: 700; color: var(--accent); text-transform: uppercase; }"),
    css=(".tekst h3 { font-size: 1.9em; font-weight: 350; line-height: 40px; }   /* duży = lekki */\n"
         ".tekst h4 { font-size: 1.35em; font-weight: 450; line-height: 32px; }\n"
         ".tekst h5 { font-size: 1em;   font-weight: 650; line-height: 24px; }   /* mały = cięższy */\n"
         ".tekst em { font-style: italic; }                                       /* tylko kursywa */"),
    html=("<h3>Szkic o dobrej stronie</h3><h4>Jak czytać skład</h4><h5>Uwagi na marginesie</h5>"
          + P("Nikt nie zatrzymuje się nad szerokością łamu, ale każdy czuje, kiedy tekst jest <em>naprawdę</em> czytelny. "
              "Wyróżnienie powinno szeptać, a nie krzyczeć.")),
    note="Krój Source Serif 4 jest zmienny, więc oś `wght` daje dowolne wagi pośrednie; przy kroju statycznym trzeba wybrać z dostępnych.")

add(id='P1-06', lvl='mikro',
    why=("Prawdziwe kapitaliki mają grubość kreski dopasowaną do tekstu, a pomniejszone wersaliki są zbyt jasne i ciasne. Wersaliki "
         "w tekście trzeba rozstrzelić, a akronimy złożyć kapitalikami, żeby nie świeciły w szarości strony."),
    before=(".tekst .etykieta, .tekst .akr { text-transform: uppercase; }\n.tekst .akr { font-size: .8em; }"),
    css=(".tekst .etykieta {\n  font-variant-caps: all-small-caps;     /* prawdziwe kapitaliki z fontu */\n"
         "  letter-spacing: .08em;                 /* wersaliki i kapitaliki wymagają spacjowania */\n"
         "  font-feature-settings: \"case\";         /* nawiasy i myślniki dopasowane do wersalików */\n"
         "  font-synthesis-small-caps: none;       /* zakaz udawania, gdy font nie ma kapitalików */\n}\n"
         ".tekst .akr {\n  font-variant-caps: all-small-caps;\n  letter-spacing: .06em;\n}"),
    html=(P("(Katalog nr 12 – wydanie drugie)", "etykieta") +
          P("Według <span class=\"akr\">ONZ</span> i <span class=\"akr\">UNESCO</span>, a także <span class=\"akr\">PKP</span>, "
            "zecer powinien wiedzieć, ile waży ołów.")),
    note="W oknie „Przed” kapitaliki są wersalikami pomniejszonymi o 20 %, bez rozstrzelenia. Krój bez funkcji `smcp` i `c2sc` nie nadaje się do tego zabiegu.")

add(id='P1-07', lvl='mikro',
    why=("Ligatury eliminują kolizję liter w sekwencjach typu „fi” i „fl”, w których zakrzywiony górny element jednej litery "
         "zderza się z kropką lub szyjką drugiej."),
    before=".tekst .duze { font-variant-ligatures: none; }",
    css=(".tekst .duze {\n  font-variant-ligatures: common-ligatures;   /* fi, fl, ff, ffi, ffl */\n}\n"
         ".tekst .rozstrzelone {\n  letter-spacing: .1em;\n  font-variant-ligatures: none;               /* rozstrzelone litery bez ligatur */\n}"),
    html=("<p class=\"duze\">filtr, flaga, oficyna, afisz, fleksja,<br><span lang=\"en\">office, affluent, baffle</span></p>"
          + P("Rozstrzelone: filtr, flaga", "rozstrzelone")),
    note=("Source Serif 4 ma ligatury standardowe (`liga`), ale nie ma dyskrecjonalnych (`dlig`), więc `discretionary-ligatures` "
          "w tym foncie nic nie zmieni. Przy niezerowym `letter-spacing` przeglądarki same wyłączają ligatury."))

add(id='P1-08', lvl='mikro',
    base=".tekst .proza { font-size: 1.25em; line-height: 32px; }\n.tekst .r { text-align: right; }",
    why=("Cyfry oldstyle wtapiają się w tekst, cyfry tabelaryczne ustawiają kolumny liczb jedna pod drugą, a prawdziwe ułamki "
         "i indeksy mają wagę kreski pasującą do reszty tekstu."),
    before=(".tekst .proza { font-variant-numeric: lining-nums proportional-nums; }\n"
            ".tekst .liczby { font-variant-numeric: lining-nums proportional-nums; }\n"
            ".tekst .sup, .tekst .sub { font-size: .75em; line-height: 0; vertical-align: super; }\n.tekst .sub { vertical-align: sub; }"),
    css=(".tekst .proza  { font-variant-numeric: oldstyle-nums proportional-nums; }  /* cyfry tekstowe */\n"
         ".tekst .liczby { font-variant-numeric: lining-nums tabular-nums; }        /* kolumna liczb */\n"
         ".tekst .u   { font-variant-numeric: diagonal-fractions; }                 /* 1/2 → ½ */\n"
         ".tekst .sup { font-variant-position: super; }\n.tekst .sub { font-variant-position: sub; }"),
    html=(P("W 1998 roku nakład wyniósł 2 400 egz., a cena 12,50 zł; <span class=\"u\">1/2</span> nakładu i "
            "<span class=\"u\">3/4</span> katalogu to druk zbiorczy. H<span class=\"sub\">2</span>O, m<span class=\"sup\">2</span>.", "proza") +
          "<table class=\"liczby\"><tr><td>1998</td><td class=\"r\">2 111</td></tr><tr><td>2004</td><td class=\"r\">1 888</td></tr>"
          "<tr><td>2010</td><td class=\"r\">12 100</td></tr></table>"),
    note=("Ułamki i indeksy wymagają w foncie funkcji `frac`, `sups`, `subs` (Source Serif 4 je ma); bez nich przeglądarka "
          "udaje je pomniejszeniem, co daje zbyt cienką kreskę. Dla tabeli z kolumną liczb różnica widoczna w prawej kolumnie."))

add(id='P1-09', lvl='mikro',
    why=("Kerning (podcinanie par liter) usuwa dziury w parach typu „AV” czy „To”; w dużych tytułach bywa potrzebny dodatkowy ujemny tracking. "
         "Odstęp międzywyrazowy decyduje o jednolitości koloru tekstu."),
    before=".tekst .naglowek { font-kerning: none; letter-spacing: 0; }",
    css=(".tekst .naglowek {\n  font-kerning: normal;\n  text-rendering: optimizeLegibility;\n"
         "  letter-spacing: -.01em;      /* duży rozmiar: lekkie zagęszczenie */\n  word-spacing: -.05em;\n}"),
    html=P("AVATAR To Wałęsa Tyrolka Yeti", "naglowek") + P(SHORT2),
    note=("Kerning optyczny (dopasowanie do kształtu liter bez tablicy fontu) jest niemożliwy w CSS (M-118, kategoria 3). W Chrome i Firefoksie "
          "`font-kerning: normal` jest zwykle włączone domyślnie; okno „Przed” wyłącza je jawnie."))

add(id='P1-10', lvl='mikro', stats=['lines', 'lastline'], sup='pelne',
    why=("Nagłówek, który łamie się na wiersz pełny i wiersz z jednym wyrazem, wygląda na nieskończony. `text-wrap: balance` "
         "wyrównuje długości wierszy, szczególnie ważne w tekście wyśrodkowanym."),
    before=".tekst h3, .tekst .srodek { text-wrap: wrap; }",
    css=".tekst h3, .tekst .srodek {\n  text-wrap: balance;\n}",
    html=("<h3 class=\"duzy\">Dobra strona zaczyna się od decyzji, których nikt nie zauważa</h3>"
          + P("Cisza w składzie to wiele małych decyzji, które razem dają spokojny tekst", "srodek")),
    base=".tekst h3 { font-size: 1.75em; line-height: 40px; }\n.tekst .srodek, .tekst h3 { text-align: center; }",
    note="Przeglądarki ograniczają równoważenie do kilku wierszy (Chrome 6, Firefox 10; do sprawdzenia w dokumentacji) – nadaje się do nagłówków, nie do akapitów.")

add(id='P1-11', lvl='mikro', sup='czesciowe', stats=['lines', 'lastline'],
    why=("Samotny krótki wyraz w ostatnim wierszu akapitu psuje kształt akapitu. `text-wrap: pretty` każe przeglądarce "
         "poświęcić trochę czasu, by zakończyć akapit sensowniej."),
    before=".tekst p { text-wrap: wrap; }",
    css=".tekst p {\n  text-wrap: pretty;\n}",
    base=".tekst { max-inline-size: min(100%, 25em); }",
    html=P("Każdy skład ma swoje potknięcia, a najczęstsze z nich zauważa się dopiero po wydrukowaniu całej strony wraz z kolumnami "
           "oraz marginesami tak, by nic nie przeszkadzało w czytaniu i wszystko się zgadzało zawsze."),
    note=("Chrome poprawia zakończenie akapitu, gdy ostatni wiersz ma jeden krótki wyraz; Firefox nie obsługuje właściwości (fallback: P2-12). "
          "Efekt zależy od szerokości kolumny i tekstu: w tym przykładzie kolumna ma stałe 25 em, a pod oknem podano zmierzone zakończenie. "
          "Na bardzo wąskich ekranach może zniknąć."))

add(id='P1-12', lvl='mikro', sup='czesciowe', stats=['hyph'],
    why=("W wąskiej kolumnie długie polskie wyrazy dają rwany rag albo wystające linie; dzielenie wyrazów skraca wiersze o puste końcówki. "
         "Dzielić powinno się według reguł języka, nie dowolnie."),
    before=".tekst { hyphens: manual; }",
    css=(".tekst {\n  hyphens: auto;                   /* wymaga lang=\"pl\" na <html> */\n"
         "  hyphenate-limit-chars: 6 3 3;    /* min. długość wyrazu, przed i po łączniku */\n"
         "  hyphenate-character: \"-\";\n}"),
    base=".tekst { max-inline-size: min(100%, 19em); text-align: left; }",
    html=P("Nieprzejednany przedstawiciel rozmaitości konstytucyjnych bezpardonowo odrzucił jednoznacznie sformułowaną propozycję "
           "nieprzewidywalnej delegacji."),
    note=("Strona ma `lang=\"pl\"`, ale przeglądarki wymagają słownika polskich wzorców. Pod oknem „Po” wykrywam w tej przeglądarce, "
          "czy dzielenie działa. W moim pierwszym teście Chromium 156 (headless) nie dzielił polskiego tekstu, a przy późniejszym uruchomieniu tej strony dzielił; "
          "przyczyny nie ustaliłem (możliwe, że słownik jest pobierany dopiero po pierwszym użyciu). Safari i Firefoksa nie sprawdzałem. "
          "Dla pewności zob. P2-13 (Hyphenopoly) lub wstawianie miękkich łączników (`&shy;`)."))

add(id='P1-13', lvl='mikro', sup='czesciowe',
    why=("Justowanie w wąskiej kolumnie rozciąga odstępy i tworzy „rzeki”; poniżej około 40 znaków lepszy jest tekst wyrównany do lewej. "
         "Kontener sam decyduje, czy justować."),
    tools=[dict(type='range', var='--w', min=18, max=62, value=26, unit='ch', label='Szerokość kolumny')],
    base=".col { container-type: inline-size; inline-size: min(var(--w, 26ch), 100%); }",
    before=".tekst { text-align: justify; hyphens: manual; }",
    css=(".tekst { text-align: left; hyphens: manual; }\n"
         "@container (min-width: 36ch) {\n  .tekst {\n    text-align: justify;\n    text-justify: inter-word;\n    hyphens: auto;\n  }\n}"),
    html="<div class=\"col\"><div class=\"tekst\">" + P(TA) + "</div></div>",
    note=("Suwak zmienia szerokość kolumny w obu oknach. W oknie „Po” justowanie włącza się dopiero, gdy kontener ma co najmniej 36ch "
          "(ok. 40 znaków przeciętnego tekstu). `text-justify` nie działa w Safari; `hyphens: auto` zależy od słownika (P1-12)."))

add(id='P1-14', lvl='mikro', sup='ograniczone', stats=['hang'], sample='guide',
    why=("Cudzysłów lub nawias otwierający na początku akapitu przesuwa wizualnie krawędź tekstu do środka; kiedy znak „wisi” w marginesie, "
         "lewa krawędź liter pozostaje prosta."),
    css=(".tekst p {\n  hanging-punctuation: first;\n}\n"
         "@supports not (hanging-punctuation: first) {\n  .tekst p.zacyt { text-indent: -.42em; }   /* zamiennik; precyzyjnie: P2-15 */\n}"),
    html=(P("„Typografia istnieje po to, żeby tekst dało się czytać” – mówił zecer – „a nie po to, żeby ją podziwiano.”", "zacyt") +
          P("(Nawias otwierający także może wisieć w marginesie.)", "zacyt") + P("Zwykły akapit zaczyna się od litery.")),
    note=("`hanging-punctuation` działa tylko w Safari (od 10). W pozostałych przeglądarkach „Po” używa ujemnego wcięcia w klasie `.zacyt`. "
          "Pionowa linia w oknach to krawędź pola składu; znak wiszący powinien ją przekraczać."))

add(id='P1-15', lvl='mikro',
    why=("Wcięcie albo odstęp: nie oba naraz (rozstrzygnięcie K-02). W tekście ciągłym wcięcie o szerokości jednego em oznacza początek "
         "akapitu, a pierwszy akapit po nagłówku wcięcia nie potrzebuje."),
    before=".tekst p { margin: 0 0 1em; text-indent: 0; }",
    css=(".tekst p { margin: 0; }\n"
         ".tekst :is(h3, h4, h5, hr, figure) + p { text-indent: 0; }   /* po nagłówku bez wcięcia */\n"
         ".tekst p + p { text-indent: 1em; }                           /* kolejne akapity z wcięciem */"),
    html="<h3>Wcięcie zamiast odstępu</h3>" + P(SHORT) + P(SHORT2) + P(TC),
    note="Odstęp między akapitami jest wielokrotnością interlinii (P1-03), jeśli już trzeba go użyć (np. w tekstach internetowych); wcięcie i odstęp razem to nadmiar.")

add(id='P1-16', lvl='mikro',
    why=("Cytat blokowy odróżnia się od tekstu jednym sygnałem (kursywa albo wcięcie albo rozmiar), a wiersze wierszowane są "
         "ustawione jako blok na osi strony, ale wyrównane do lewej, a nie wyśrodkowane linia po linii."),
    before=(".tekst blockquote { margin: 1em 2.5em; padding-left: 1em; border-left: 4px solid var(--accent); font-size: 1.15em; font-weight: 700; font-style: italic; }\n"
            ".tekst .wiersz { text-align: center; }"),
    css=(".tekst blockquote { margin: 24px 0 24px 2em; font-style: italic; }   /* jeden sygnał + wcięcie */\n"
         ".tekst blockquote footer { font-style: normal; font-size: .9em; }\n"
         ".tekst .wiersz {\n  width: fit-content;\n  margin: 24px auto;\n  text-align: left;       /* blok na osi, wiersze do lewej */\n}"),
    html=(P(SHORT2) +
          "<blockquote><p>%s</p><footer>%s</footer></blockquote>" % (QUOTE, QUOTE_SRC) +
          "<div class=\"wiersz\"><p>%s</p></div>" % '<br>'.join(VERSE)),
    note="`fit-content` nie jest potrzebne przy wcięciu, ale pozwala wycentrować najdłuższy wiersz; fallback: `display: table`.")

add(id='P1-17', lvl='mikro', sup='czesciowe',
    why=("Inicjał i kapitaliki w pierwszym wierszu oznaczają początek rozdziału; zajmują wysokość kilku wierszy i leżą na wspólnej linii bazowej."),
    css=(".tekst p:first-of-type::first-letter {\n  -webkit-initial-letter: 3;   /* Safari */\n  initial-letter: 3;           /* Chrome 110+ */\n"
         "  margin-inline-end: .12em;\n  font-weight: 600;\n}\n"
         ".tekst p:first-of-type::first-line {\n  font-variant-caps: all-small-caps;\n  letter-spacing: .06em;\n}\n"
         "@supports not ((initial-letter: 3) or (-webkit-initial-letter: 3)) {\n  .tekst p:first-of-type::first-letter {\n"
         "    float: left;\n    font-size: 3.1em;\n    line-height: .85;\n    padding-inline-end: .1em;\n  }\n}"),
    html=P(TA) + P(SHORT2),
    note="Firefox nie obsługuje `initial-letter`; wtedy działa zamiennik z `float` (mniej dokładny, bo nie dopasowuje się do linii bazowych).")

add(id='P1-18', lvl='własne',
    why=("Tabelę składa się jak tekst: nagłówki poziomo, minimum linii, cyfry tabelaryczne wyrównane do prawej; "
         "numer na liście wisi poza kolumną tekstu. Dane są gęste, więc zwykła interlinia i drobne ramki wystarczą."),
    before=(".tekst table { border: 1px solid var(--ink); }\n.tekst th, .tekst td { border: 1px solid var(--ink); padding: 4px 8px; text-align: center; }\n"
            ".tekst th { text-transform: uppercase; font-weight: 800; }\n.tekst ol { list-style-position: inside; }"),
    css=(".tekst table {\n  border-collapse: collapse;\n  inline-size: 100%;\n  font-variant-numeric: lining-nums tabular-nums;\n}\n"
         ".tekst th, .tekst td { padding: 4px 8px 4px 0; text-align: left; }   /* 4 + 24 + 4 = 32 px */\n"
         ".tekst th { font-weight: 600; border-block-end: 1px solid currentColor; }\n"
         ".tekst .r { text-align: right; }                                      /* liczby do prawej */\n"
         ".tekst tbody tr:nth-child(even) { background: var(--tint); }        /* zebra zamiast ramek */\n"
         ".tekst ol { padding-inline-start: 2em; list-style-position: outside; }\n"
         ".tekst li::marker { font-variant-numeric: tabular-nums; color: var(--soft); }"),
    html=("<table><thead><tr><th>Tytuł</th><th class=\"r\">Rok</th><th class=\"r\">Nakład</th><th class=\"r\">Cena</th></tr></thead><tbody>"
          "<tr><td>Szkic o dobrej stronie</td><td class=\"r\">1998</td><td class=\"r\">2 400</td><td class=\"r\">12,50 zł</td></tr>"
          "<tr><td>Zecer przy skrzyni</td><td class=\"r\">2004</td><td class=\"r\">1 800</td><td class=\"r\">9,90 zł</td></tr>"
          "<tr><td>Miara i rytm</td><td class=\"r\">2011</td><td class=\"r\">12 000</td><td class=\"r\">24,00 zł</td></tr></tbody></table>"
          "<ol style=\"margin-top:24px\">" + ''.join('<li>%s</li>' % x for x in LIST) + "</ol>"),
    note=("Zebra jest opcjonalna (obie książki zalecają minimum „mebli”); w rozstrzygnięciu K-04 dla danych liczy się gęstość, więc w tabeli nie ma "
          "dodatkowego powietrza. `::marker` w Safari obsługuje tylko część właściwości."))

# ----- makro: kanony --------------------------------------------------------------------------
add(id='P1-19', lvl='makro', wide=True,
    tools=[dict(type='toggle', cls='show-canon', label='Pokaż konstrukcję (przekątne, pole składu)')],
    why=("Marginesy robią około połowy charakteru strony: spinają pole składu ze stroną i zostawiają miejsce na kciuk. Kanon średniowieczny (Villard) i "
         "Aldusa dają proporcje, które można policzyć i powtórzyć w procentach szerokości."),
    base=".fig { inline-size: min(100%, 280px); }",
    before=".pole { margin: 8%; }",
    css=(".villard, .aldus { aspect-ratio: 2 / 3; }\n"
         "/* margines: góra  zewn.  dół  wewn. (strona prawa) */\n"
         ".villard .pole { margin: 16.667% 22.222% 33.333% 11.111%; }   /* s : t : e : f = 2 : 3 : 4 : 6 */\n"
         ".aldus   .pole { margin: 11.111% 22.222% 25.556% 11.111%; }   /* pole 1 : 1,7 */"),
    before_html='<div class="strony">' + canon_page('rowne', 1.5, .08, .08, .08, .08, 'równe marginesy 8 %', drawing=False) + '</div>',
    after_html=('<div class="strony">' + canon_page('villard', 1.5, 0.166667, 0.222222, 0.333333, 0.111111, 'Villard: 2:3, pole 2:3') +
                canon_page('aldus', 1.5, 0.111111, 0.222222, 0.255556, 0.111111, 'Aldus: 2:3, pole 1:1,7') + '</div>'),
    note=("Procenty `margin` odnoszą się do szerokości kontenera, także dla góry i dołu, dlatego konstrukcja daje się zapisać wprost. "
          "Okno „Przed” nie ma `aspect-ratio`, więc strona ma wysokość tekstu; to ilustruje „dowolny” format. Kanon Van de Graafa nie występuje w żadnej z książek, "
          "opisana konstrukcja jest przypisana Tschicholdowi i Villardowi (zob. katalog)."))
K1[-1]['before_html'] = '<div class="strony">' + canon_page('rowne', 1.5, .08, .08, .08, .08, 'równe marginesy 8 %, format dowolny', drawing=False) + '</div>'

add(id='P1-20', lvl='makro', wide=True,
    tools=[dict(type='toggle', cls='show-canon', label='Pokaż konstrukcję (przekątne, pole składu)')],
    why=("Strona i pole składu powinny się różnić proporcją wyraźnie, a nie przypadkiem (A-10). ISO 1:√2 jest praktyczne, ale mało „muzyczne”, "
         "więc potrzebuje pola o innym kształcie (np. złotego podziału); strona złotego podziału pasuje do pola 1:1,87 (Froissart)."),
    base=".fig { inline-size: min(100%, 280px); }",
    before=".pole { margin: 10%; }",
    css=(".iso, .zloty { }\n.iso   { aspect-ratio: 1 / 1.4142; }   /* ISO 216, 1:√2 */\n.zloty { aspect-ratio: 1 / 1.618; }    /* złoty podział */\n"
         "/* margines: góra  zewn.  dół  wewn. */\n"
         ".iso   .pole { margin: 11.111% 22.222% 22.222% 11.111%; }   /* pole złotego podziału, s = t = w/9, e = f = 2s */\n"
         ".zloty .pole { margin: 11.111% 22.222% 26.02% 11.111%; }    /* Froissart: pole 1 : 1,87 */"),
    before_html='<div class="strony">' + canon_page('rowne iso0', 1.4142, .1, .1, .1, .1, 'ISO, równe marginesy 10 %') + '</div>',
    after_html=('<div class="strony">' + canon_page('iso', 1.4142, 0.111111, 0.222222, 0.222222, 0.111111, 'ISO + pole 1:1,62') +
                canon_page('zloty', 1.618, 0.111111, 0.222222, 0.2602, 0.111111, 'Złoty podział + pole 1:1,87') + '</div>'),
    note=("Spór K-05: złoty podział jest tu jednym z kanonów obok ISO i 2:3, nie wyróżnioną regułą. Przełącznik wyboru jednego kanonu "
          "(z blokadą kolizji z P1-19) pojawi się dopiero w pokazie (Etap 4)."))
# before for P1-20 needs aspect ratio of ISO: add class rowne iso0
K1[-1]['css'] = K1[-1]['css'].replace(".iso, .zloty { }\n", "")
K1[-1]['before'] = ".iso0 { aspect-ratio: 1 / 1.4142; }\n.pole { margin: 10%; }"

add(id='P1-21', lvl='makro', wide=True, sample='kolumny',
    tools=[dict(type='toggle', cls='show-cols', label='Pokaż siatkę 12 kolumn')],
    why=("Siatka kolumnowa jest regulatorem proporcji: elementy zajmują jedną lub kilka kolumn, a krawędzie tekstu, obrazów i podpisów "
         "powtarzają się. Podsiatka pozwala komponentowi dziedziczyć linie rodzica."),
    base=".siatka { display: grid; grid-template-columns: repeat(12, 1fr); column-gap: 16px; }",
    before=(".siatka > * { margin: 0 0 24px; }\n.siatka > h4 { grid-column: 1 / 8; }\n.siatka > .glowny { grid-column: 1 / 8; max-inline-size: 91%; }\n"
            ".siatka > .bok { grid-column: 8 / -1; margin-inline-start: 3%; }\n.siatka > .rys { grid-column: 1 / 7; }"),
    css=(".siatka > h4     { grid-column: 1 / 9; }\n.siatka > .glowny { grid-column: 1 / 9; }\n"
         ".siatka > .bok    { grid-column: 9 / -1; grid-row: 2; font-size: .85em; line-height: 24px; }\n"
         ".siatka > .rys {\n  grid-column: 1 / 9;\n  display: grid;\n  grid-template-columns: subgrid;   /* dziedziczy 8 kolumn rodzica */\n}\n"
         ".rys .ramka      { grid-column: 1 / 5; }\n.rys figcaption { grid-column: 5 / 9; }"),
    html=("<div class=\"siatka\"><h4>Rozdział trzeci</h4>" + "<p class=\"glowny\">" + SHORT + "</p>" +
          "<aside class=\"bok\">Notatka boczna zaczyna się w tej samej kolumnie co każda następna.</aside>"
          "<figure class=\"rys\"><div class=\"ramka\">obraz</div><figcaption>Podpis zaczyna się w piątej kolumnie siatki, nie „mniej więcej tu”.</figcaption></figure>"
          "<p class=\"glowny\">" + SHORT2 + "</p></div>"),
    note=("Nakładka kolumn to osobny element, nie część strony; w kodzie powyżej jest tylko siatka. Okno „Przed” ma szerokości w procentach, które nie pasują do kolumn. "
          "`subgrid`: Chrome 117, Safari 16, Firefox 71; bez niego trzeba ręcznie powielić szerokości kolumn."))

add(id='P1-22', lvl='makro', wide=True, sup='czesciowe',
    why=("Tekst w kilku kolumnach ma wiersze 40–50 znaków; przypisy boczne w marginesie pozwalają czytać notatkę bez przewracania strony. "
         "Przypisy łączy z tekstem kotwica, a nie licznik pikseli."),
    base=".art { container-type: inline-size; position: relative; }",
    before=".nota { display: block; margin: 8px 0 0; font-size: .85em; }",
    css=(".tekst .kolumny {\n  column-width: 18em;\n  column-gap: 2em;\n  column-rule: 1px solid currentColor;\n  widows: 2;\n  orphans: 2;\n}\n"
         ".tekst .kolumny blockquote { break-inside: avoid; }\n"
         ".tekst .nota { display: block; font-size: .85em; line-height: 24px; }\n"
         "@container (min-width: 720px) {\n  .tekst .tresc { margin-inline-end: 30%; }                /* miejsce na margines */\n"
         "  .tekst .odsylacz { anchor-name: --przyp; }\n"
         "  .tekst .nota {\n    position: absolute;\n    position-anchor: --przyp;\n    top: anchor(top);               /* w jednej linii z odsyłaczem */\n"
         "    left: calc(100% - 28%);\n    inline-size: 26%;\n  }\n}"),
    html=("<div class=\"art\"><div class=\"tekst\"><div class=\"tresc\"><div class=\"kolumny\"><p>" + TA + "</p><p>" + TB + "</p></div>"
          "<p>Przypisy boczne<sup class=\"odsylacz\">1</sup> stoją w wysokości odsyłacza.</p>"
          "<aside class=\"nota\"><b>1</b> Przypis w marginesie, kotwiczony do odsyłacza.</aside></div></div></div>"),
    note=("Widows/orphans: Chrome 25, Safari 1,3, brak w Firefoksie; zasada „wdowy” z Bringhursta (M-88) działa tylko w układzie kolumnowym – w przewijanym tekście "
          "nie ma stron (K3). Anchor positioning: Chrome 125, Safari 26, Firefox 147 (do sprawdzenia przy starszych wersjach). Poniżej 720 px przypis przechodzi pod akapit."))
K1[-1]['stack_inner'] = True

add(id='P1-23', lvl='makro', wide=True,
    why=("Strony sąsiednie są jednostką projektu: marginesy zewnętrzne szersze od wewnętrznych, a lustro (strona lewa i prawa) powtarza układ. "
         "W przewijanym dokumencie można to tylko przybliżyć dwoma kontenerami obok siebie."),
    before=".rozkladowka .karta { padding: 8%; }\n.rozkladowka .karta + .karta { margin-top: 24px; }",
    css=(".rozkladowka { display: grid; grid-template-columns: 1fr; gap: 24px; }\n"
         "@container (min-width: 640px) {            /* poniżej progu: jedna strona */\n"
         "  .rozkladowka { grid-template-columns: 1fr 1fr; gap: 0; }\n"
         "  .karta.lewa   { padding: 8% 11.111% 12% 22.222%; }   /* zewnętrzny po lewej, wewnętrzny przy grzbiecie */\n"
         "  .karta.prawa  { padding: 8% 22.222% 12% 11.111%; border-inline-start: 1px solid var(--ink); }\n}"),
    html=("<div class=\"rozkladowka\"><section class=\"karta lewa\"><p>" + SHORT + "</p></section>"
          "<section class=\"karta prawa\"><p>" + SHORT2 + "</p></section></div>"),
    note=("To przybliżenie, nie rozkładówka: nie ma grzbietu, kartki ani równego wysokością przepływu na obie strony (A-44, A-46, A-47: kategoria 3). "
          "Okno „Po” przełącza się na dwie strony dopiero przy kontenerze szerokości co najmniej 640 px."))

add(id='P1-24', lvl='makro', wide=True, base=".tekst { max-inline-size: min(100%, 64ch); }",
    why=("Każdy poziom nagłówków ma mieć nie więcej niż trzy sygnały odróżniające (K-07) i jedną dominującą formę (K-09); warstwy `@layer` "
         "porządkują kaskadę, żeby ogólne style nie przebijały szczegółowych przez specyficzność."),
    before=(".tekst h3 { font-size: 1.6em; font-weight: 800; font-style: italic; text-transform: uppercase; text-align: center; color: var(--accent); }\n"
            ".tekst h4 { font-size: 1.3em; font-weight: 800; text-align: right; text-decoration: underline; }\n"
            ".tekst h5 { font-size: 1.1em; font-weight: 800; text-transform: uppercase; text-align: center; }"),
    css=("@layer baza, naglowki;\n"
         "@layer baza      { .tekst h3, .tekst h4, .tekst h5 { text-align: left; margin: 0 0 8px; } }\n"
         "@layer naglowki {\n  .tekst h3 { font-size: 1.9em; font-weight: 350; line-height: 40px; }        /* rozmiar + waga */\n"
         "  .tekst h4 { font-size: 1.35em; font-weight: 450; line-height: 32px; }\n"
         "  .tekst h5 { font-size: 1em; font-weight: 650; font-variant-caps: all-small-caps; letter-spacing: .08em; }\n}"),
    html="<h3>Rozdział</h3><h4>Podrozdział</h4><h5>Śródtytuł</h5>" + P(SHORT2) + "<h4>Drugi podrozdział</h4>" + P(TC),
    note="Mieszanie wyrównań w jednym dokumencie (A-78) jest poza pokazem; w demo wybrano jedną formę (asymetryczną, do lewej). `@layer`: Chrome 99, Safari 15,4, Firefox 97.")

assert len(K1) == 24, len(K1)
