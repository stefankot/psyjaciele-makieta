# Klasyfikacja zasad (Etap 2)

Stan: Etap 2, do akceptacji. Podstawa: [katalog.md](katalog.md) (288 zasad, Etap 1 zaakceptowany) i [bringhurst-tabele.md](bringhurst-tabele.md).

## 1. Metoda i legenda

- **Kategoria 1**: sam CSS i atrybuty HTML. **Kategoria 2**: własny JS, biblioteka z CDN, przetwarzanie w buildzie, subsetting fontów, uważność w HTML (znaki Unicode, `&nbsp;`). **Kategoria 3**: niemożliwe, bo web to nie druk (stały format, papier, rozkładówka, kontrola łamania stron, ręczna korekta optyczna).
- Zasady złożone z części różnej wykonalności są oznaczone **`1+2`**, **`1+3`** itd.; opis w kolumnie „Wdrożenie lub powód” mówi, co należy do której kategorii.
- **Punkt pokazu** to jedna przełączana zasada w Etapach 3–4 (ID `P1-nn` w kategorii 1, `P2-nn` w kategorii 2); jeden punkt może obejmować kilka zasad z katalogu. Zasady poza punktami są oznaczone „poza pokazem” z powodem.
- **Wsparcie**: wersje Chrome / Safari / Firefox, od których funkcja działa w pełni, wg MDN browser-compat-data v8.1.5 z 8.10.2026. Bieżące wersje stabilne w tym zbiorze: Chrome 155, Safari 27, Firefox 157. Poza danymi MDN sprawdziłem w Chromium 156 (Playwright, `CSS.supports`, czyli tylko rozpoznanie składni, nie wygląd) obsługę: `text-wrap: balance/pretty`, `hyphenate-limit-chars`, `initial-letter`, `text-box`, `font-size-adjust`, `subgrid`, `anchor-name`/`position-anchor`, `font-variant-caps`, `orphans`/`widows`, `width: 66ch`, jednostki `lh`/`rlh`/`cap`, `text-autospace`, `text-justify`; zgodnie z MDN brak: `hanging-punctuation`, `hyphenate-limit-lines`. Nie testowałem Safari i Firefoksa (brak tych silników w środowisku), więc ich kolumny pochodzą wyłącznie z MDN.
- **Do sprawdzenia** (nie rozstrzygnięte w tym etapie): polskie słowniki dzielenia w przeglądarkach (`hyphens: auto`; headless Chromium 156 nie dzielił polskiego tekstu przy `lang="pl"`), zachowanie `text-wrap: balance` przy większej liczbie wierszy, kopiowanie i wyszukiwanie tekstu z `&nbsp;` i `&shy;`, bundlowanie tex-linebreak z CDN. Z pamięci (nie testowane): nazwy opcji Hyphenopoly (`leftmin`, `rightmin`, `minWordLength`) i sposób działania tex-linebreak. Wagi „własnego kodu” w tabeli kategorii 2 to szacunki z projektu, nie pomiary.

## 2. Rozstrzygnięcia konfliktów

| ID | Wybrana wersja | Uzasadnienie | Dotyczy |
|---|---|---|---|
| K-01 | Wtrącenia: półpauza ze spacjami (B 5.2.1) | Książka Lupton opisuje pauzę bez spacji; półpauza ze spacjami jest zgodna z polskim zwyczajem DTP, a pauza zostaje dla dialogu. Do sprawdzenia: zgodność z normą polską (nie weryfikowano). Lupton (M-95) poza pokazem. | M-94, M-95, M-96 |
| K-02 | Wcięcie 1 em, bez odstępu między akapitami | Obie książki zgadzają się, że wcięcie i odstęp razem to nadmiar (Lupton s. 127) oraz że odstęp powinien być krokiem rytmu (Bringhurst 2.2.2). Wdrożono wcięcie; akapity blokowe (M-131) odrzucono w tekście ciągłym. | M-128 – M-132 |
| K-03 | Margines zewnętrzny szerszy od wewnętrznego (B) | Konstrukcja Bringhursta jest spójna i daje się policzyć (s : e = 1 : 2); Lupton podaje przykład, nie regułę. Wersja Lupton (A-21) poza pokazem. | A-20, A-21 |
| K-04 | Kontekstowo: pustka dla tekstu ciągłego (B), gęstość dla danych (L) | Oba stanowiska nie konkurują o to samo: pierwsze dotyczy strony tytułowej i tekstu, drugie układów informacyjnych. W pokazie bez osobnego punktu (efekt marginesów w P1-19 i tabel w P1-18). | A-54, A-55 |
| K-05 | Złoty podział jako jedna z równoprawnych opcji | Nie rozstrzygamy spór; przełącznik P1-20 pokazuje kanony obok siebie (2:3, ISO, złoty) z blokadą jednoczesnego wyboru. | A-06, A-07 |
| K-06 | Justowanie: limity Bringhursta 9.4.1 | Najnowsza reguła Bringhursta (9.4.1) dopuszcza korektę ±3% odstępów między znakami i ±2% szerokości glifów, a ogólny zakaz (2.4) dotyczy korekt automatycznych bez kontroli. W pokazie: korekta odstępu między wyrazami i znakami tylko w P2-14, bez skalowania glifów (font-stretch tylko na prawdziwej osi). Ręczny tracking Lupton tylko w nagłówkach (P1-09). | M-71 – M-73 |
| K-07 | Połączenie: jeden parametr na raz przy tytule (B), do trzech sygnałów na poziom (L) | Obie zasady mówią o różnych skalach: pierwsza o zmianie jednej cechy względem tekstu, druga o liczbie cech wyróżniających poziom hierarchii. | M-21, A-75 |
| K-08 | Cudzysłowy polskie: „…” z «…» wewnątrz | Zgodnie z locale `pl` w Typografie (left „«, right ”»). Zwyczaj polski dla interpunkcji: znaki poza cudzysłowem, jeśli nie należą do cytatu; do sprawdzenia w źródle polskim (książki tego nie omawiają). | M-103, M-104 |
| K-09 | Dominująca forma nagłówków (B 4.2.2) | Lupton opisuje mieszanie wyrównań jako zabieg ekspresyjny; w demo wybieramy jedną formę (asymetryczną), mieszanie poza pokazem (A-78). | A-73, A-78 |
| W-S | Terminologia: wdowa i sierota wg Bringhursta zgadza się z CSS | Wdowa (ostatni wiersz akapitu u góry strony) = CSS `widows`; sierota (pierwszy wiersz akapitu na dole) = CSS `orphans`. Bringhurst wymaga tylko dopełnienia wdowy (M-88); sierotę dopuszcza (M-89). W pokazie: `widows: 2`, `orphans: 1`. | M-88, M-89 |
| W-P | Reguły polskie spoza książek | Spójniki jednoliterowe niełamliwe (`lengthShortWord: 1`), półpauza w zakresach, cudzysłowy „…”, dzielenie wg polskich wzorców. Dwuliterowe przyimki (do, na, po, za…) opcjonalnie; poza pokazem. | M-114, M-63, M-83 |

## 3. Podsumowanie

- Zasad w katalogu: **288**. Według głównej kategorii: tylko kategoria 1: **205**; tylko kategoria 2: **37**; tylko kategoria 3: **25**; mieszane: **21** (1+2: 16, 1+3: 5).
- Zasady z częścią w kategorii 1: 226; w kategorii 2: 53; w kategorii 3: 30.
- Wchodzą do pokazu (w punktach P1 lub P2): **153** zasad (w tym 3 z kategorii 3 przez przybliżenie: A-44, A-48, A-49); **135** poza pokazem, z powodem w tabeli.
- Według poziomu, w pokazie / ogółem: mikro: 94 / 153; makro: 51 / 78; własne: 8 / 57.

## 4. Propozycja liczby punktów pokazu

**X = 24 punkty w kategorii 1 i 24 w kategorii 2** (48 przełączników).

- Kategoria 2 ma dokładnie 24 punkty do przełączenia na żywo; pozostałe elementy kategorii 2 (subsetting i poprawki fontów, Paged.js) są etapami builda albo nieodwracalnie przebudowują DOM, więc nie wchodzą do pokazu (powód w tabeli poniżej).
- **Kategoria 1 jest bogatsza**: ma ok. 41 kandydatów (24 wybranych plus 17 w rezerwie `R1-nn`). Zamiast przycinać ją bez śladu, wybrane 24 punkty to te o największym wpływie na czytelność; pozostałe 17 oznaczono „poza pokazem: nadwyżka K1” i opisano w sekcji 9. Jeśli wolisz asymetrię (np. 41 w kategorii 1 przy 24 w kategorii 2), wystarczy dopisać rezerwy do tablicy punktów.
- Wybrane punkty obejmują wszystkie poziomy: mikro (znak, wiersz, akapit), makro (kanon strony, marginesy, siatka, kolumny, rozkładówka jako przybliżenie, hierarchia) i własne (tabele i listy).

## 5. Klasyfikacja wszystkich zasad

| ID | Kat. | Zasada (skrót) | Wdrożenie lub powód | Punkt pokazu / poza pokazem |
|---|:--:|---|---|---|
| M-01 | 1 | Akapit ciągły w jednej kolumnie, krój szeryfowy, rozmiar tekstowy: 45–75 znaków w wierszu (ze spacjami i … | max-inline-size w ch (45–75, cel 66) | P1-01 |
| M-02 | 1 | Tekst w kilku kolumnach: średnio 40–50 znaków w wierszu. | column-width ok. 40–50ch w układzie wielokolumnowym | P1-22 |
| M-03 | 1 | Wiersz średnio dłuższy niż 75–80 znaków jest za długi do czytania ciągłego, nawet przy dużej interlinii … | górny limit 75ch (min(66ch,100%)) | P1-01 |
| M-04 | 1 | Miara książkowa to ok. 30× rozmiar kroju; do przyjęcia jest 20–40×. | szerokość w em (ok. 30em ≈ 30× rozmiar) | P1-01 |
| M-05 | 1 | Dolne granice miary: tekst justowany nie krótszy niż ok. 40 znaków (poniżej 38–40 grozi „biały trądzik” … | justowanie tylko w kontenerze ≥ 40ch (@container), inaczej ragged | P1-13 |
| M-06 | 2 | Liczbę znaków w wierszu wylicza się z długości małego alfabetu danego kroju i rozmiaru (10 pt: roman … | liczenie znaków z długości alfabetu: canvas.measureText lub Range.getClientRects; narzędzie diagnostyczne | P2-16 |
| M-07 | 1 | Interlinię dobiera się do kroju, tekstu i miary: dłuższa miara, ciemniejszy krój, duży korpus (wysokość … | line-height jako funkcja miary i kroju (zmienna CSS) | P1-02 |
| M-08 | 1 | Typowa interlinia tekstu: 9/11, 10/12, 11/13, 12/15 (domyślnie ok. 120% rozmiaru). Interlinia ujemna … | line-height bezwymiarowe 1,2–1,5; ujemna tylko w nagłówkach | P1-02 |
| M-09 | 1+2 | Pionowa przestrzeń zmienia się w mierzonych odstępach: każde odstępstwo od tekstu głównego (nagłówek … | K1: odstępy w jednostce siatki (lh, rlh, --u); K2: wysokość obrazów i ramek dopełniana JS do wielokrotności | P1-03; P2-17 |
| M-10 | 1 | Nagłówki: przestrzeń nad i pod w sumie równa całkowitej liczbie linii tekstu (np. 13+13; 8+5; 26+13) … | margin nagłówków jako suma pełnych linii | P1-03 |
| M-11 | 1+2 | Blok o innej interlinii niż tekst (np. cytat 10/12 w tekście 11/13) domykaj elastycznymi odstępami przed … | K1: ta sama interlinia w cytacie i tekście; K2: dopełnianie dowolnego bloku do wielokrotności (ResizeObserver) | P1-03; P2-17 |
| M-12 | 3 | Linie tekstu na obu stronach kartki oraz na obu stronach rozkładówki leżą na wspólnych liniach … | Niemożliwe: brak dwustronnego druku i kartek. Przybliżenie: jedna siatka bazowa dla wszystkich kolumn i obu stron „rozkładówki” | poza pokazem: niemożliwe (patrz A-47, P1-23) |
| M-13 | 3 | Strona nie może dusić tekstu: 30–45 wierszy na stronie książki przy 60–66 znakach (300–500 słów) … | Niemożliwe: nie ma strony o stałej liczbie wierszy. Przybliżenie: miara i interlinia dobrane jak dla strony, kolumny przez @container | poza pokazem: niemożliwe (przybliżenie w P1-01, P1-02) |
| M-14 | 1+3 | Całe wiersze wersalików mogą mieć ciaśniejszą interlinię (brak ascenderów i descenderów), ale w stosach … | K1: osobny line-height dla bloków samych wersalików; K3: ręczna korekta linii bazowej w mieszanych stosach | P1-06 (część K1) |
| M-15 | 1 | Przy mieszaniu rozmiarów w jednym bloku interlinia „auto” daje nierówny efekt; ustaw interlinię jawnie i … | jawny line-height i korekta linii bazowej (vertical-align) | poza pokazem: dubluje P1-02 |
| M-16 | 1 | Nie składaj bez skali: ogranicz się do skromnego zestawu powiązanych rozmiarów; tradycyjna skala (6, 7 … | skala w zmiennych CSS, rozmiary z rem | P1-04 |
| M-17 | 1 | Skale rozmiarów wyprowadzone ze złotego podziału (każdy wyraz = suma dwóch poprzednich) … | alternatywne skale (Fibonacci, Le Corbusier) jako zestawy zmiennych | P1-04 |
| M-18 | 1 | Skala modułowa oparta na dwóch proporcjach (np. 1:φ i 1:2) jest bardziej elastyczna niż oparta na jednej. | skala z dwóch proporcji (calc) | P1-04 |
| M-19 | 1 | Rozmiar zależy od medium i kontekstu: w druku typowo 9–11 pt, 12 pt wygląda „koniowato”, podpisy ok. 7,5 … | clamp() zależnie od medium; domyślny rozmiar tekstu | P1-04 |
| M-20 | 1 | Hierarchia rozmiarów wymaga wyraźnego kontrastu; minimalne różnice rozmiaru wyglądają na niezdecydowane … | kontrast skali ≥ 1,25 między poziomami | P1-04 |
| M-21 | 1 | Zmieniaj jeden parametr na raz: tytuł najpierw jako ten sam krój w wadze i rozmiarze tekstu (kapitaliki … | nagłówek zmieniany o jeden parametr naraz (KONFLIKT K-07 rozstrzygnięty) | P1-05 |
| M-22 | 1 | Wraz ze wzrostem rozmiaru waga kroju lekko maleje, nie rośnie; duże tytuły w wadze lekkiej (light … | font-weight maleje wraz z rozmiarem (nagłówki light) | P1-05 |
| M-23 | 1 | Style optyczne: „display” od ok. 24 pt wzwyż (delikatne), „text” 9–14 pt, „caption” 6–8 pt z najgrubszą … | font-optical-sizing: auto, oś opsz w fontach zmiennych | poza pokazem: nadwyżka K1 (R1-01) |
| M-24 | 1 | Krój dobieraj do charakteru tekstu, zadania i kontekstu (nie dosłownie do tematu): dobry do długiego … | dobór font-family do tekstu | poza pokazem: decyzja projektowa, nieprzełączalna (realizowana doborem kroju demo) |
| M-25 | 2 | Krój musi zawierać to, czego tekst wymaga: kapitaliki, cyfry tekstowe, potrzebne wagi, pasujący krój … | sprawdzenie pokrycia glifów (opentype.js lub pomiar canvas) i subsetting w buildzie | P2-24 |
| M-26 | 1 | Krój skromny ustawiaj skromnie: jeden rozmiar, dobrze rozstawione wersaliki, dobrze dobrana interlinia … | zestaw deklaracji (jeden rozmiar, rozstaw wersalików, miara) | poza pokazem: postawa ogólna, nie pojedynczy efekt |
| M-27 | 1 | Spośród kilku popularnych krojów o różnych koncepcjach litery (Baskerville, Helvetica, Palatino, Times) … | wybór jednego kroju z kilku niezgodnych | poza pokazem: decyzja o doborze kroju |
| M-28 | 1 | Zacznij od jednej rodziny krojowej (roman, italic, kapitaliki, wagi); rozszerzona rodzina daje … | jedna rodzina w @font-face (family, weight, style) | poza pokazem: decyzja o doborze kroju |
| M-29 | 1 | Szanuj całość roman / italic / kapitaliki: nie łącz kursywy jednego kroju z romanem innego ani … | spójne roman/italic/kapitaliki z jednej rodziny | poza pokazem: decyzja o doborze kroju |
| M-30 | 1 | Hierarchia rodziny: roman → kapitaliki → italic → bold; odwrócenie tego porządku (bold wersaliki na tle … | hierarchia odmian roman → kapitaliki → italic → bold w stylach nagłówków | P1-05 |
| M-31 | 1 | Nie używaj odmiany, której nie potrzebujesz: bold i półbold do znaczników list, małych tytułów, haseł … | bold tylko w wybranych rolach | poza pokazem: dubluje P1-05 |
| M-32 | 1 | Bold dobieraj o strukturze zgodnej z krojem (rodzina projektowana z wagami albo pokrewna), nie z … | font-synthesis-weight: none, bold z rodziny | poza pokazem: nadwyżka K1 (R1-03) |
| M-33 | 1 | Kursywa nie jest pochylonym romanem: nie pochylaj mechanicznie (pseudokursywa); awaryjnie do ok. 10° … | font-synthesis-style: none, prawdziwy italic | poza pokazem: nadwyżka K1 (R1-03) |
| M-34 | 1 | Nie zniekształcaj liter: nie skaluj ich poziomo ani pionowo i nie ściskaj dla dopasowania tekstu; użyj … | font-stretch na prawdziwych osiach zamiast transform: scaleX | poza pokazem: nadwyżka K1 (R1-14) |
| M-35 | 1 | Kroje tytułowe i display wzmacniają strukturę kroju tekstu (kaligraficzny do kaligraficznego … | dobór kroju display do kroju tekstu | poza pokazem: decyzja o doborze kroju |
| M-36 | 1 | Parowanie szeryfowego i bezszeryfowego według struktury wewnętrznej (Meridien + Frutiger; Garamond + … | dobór pary szeryfowy/bezszeryfowy | poza pokazem: decyzja o doborze kroju |
| M-37 | 1 | Mieszaj kroje przez kontrast, nie mdłe podobieństwo: mało elementów o wyraźnie różnych rolach; unikaj … | kontrast zamiast mdłego podobieństwa krojów | poza pokazem: decyzja o doborze kroju |
| M-38 | 1 | Mieszając kroje w jednym wierszu wyrównaj ich wysokość x; mieszając w osobnych wierszach, różnicuj także … | font-size-adjust: from-font | poza pokazem: nadwyżka K1 (R1-02) |
| M-39 | 1 | Dwa kroje o tym samym rozmiarze nominalnym wyglądają na różnej wielkości (wysokość x, waga, szerokość) … | font-size-adjust: from-font | poza pokazem: nadwyżka K1 (R1-02) |
| M-40 | 1 | Nie mieszaj dwóch krojów w jednym wyrazie (łatana typografia = porażka); cały wyraz lub fragment w … | @font-face i unicode-range tak, by wyraz miał jeden font | poza pokazem: właściwość doboru fontów (P2-24 sprawdza pokrycie) |
| M-41 | 2 | Skrótowce w tekście bieżącym składaj spacjowanymi kapitalikami (AM, PM, CE, BC, NATO, 3:00 AM). | owijanie akronimów w abbr (TreeWalker), styl font-variant-caps: all-small-caps | P2-10 |
| M-42 | 2 | Wyjątki od kapitalików: dwuliterowe skróty geograficzne i skróty imion (JFK) zostają wersalikami … | lista wyjątków (dwuliterowe geograficzne, inicjały osób) | P2-10 |
| M-43 | 2 | Akronimy czytane jak słowa składaj małymi literami z wielką na początku (Unesco, Ascii); akronimy … | wymaga słownika wymowy; w pokazie krótka lista wyjątków | P2-10 |
| M-44 | 1 | Używaj prawdziwych kapitalików (inne proporcje, waga i szerokość), nie pomniejszonych wersalików … | font-variant-caps: small-caps i font-synthesis-small-caps: none | P1-06 |
| M-45 | 1 | Słowo lub krótka fraza wersalikami w tekście bieżącym wygląda ciężko; długi tekst złożony wyłącznie … | text-transform: uppercase tylko dla krótkich fraz | P1-06 |
| M-46 | 1 | Kapitaliki spacjowane przy prawdziwych kapitalikach do wyróżnień i nagłówków; spacjowane wersaliki w … | kapitaliki spacjowane w nagłówkach i wyróżnieniach | P1-06 |
| M-47 | 1 | Przy składzie wersalikami dopasuj położenie łączników, nawiasów i cudzysłowów do wysokości wersalików … | font-feature-settings: „case” | P1-06 |
| M-48 | 1 | Używaj ligatur wymaganych przez font i język: ff, fi, fl, ffi, ffl w kroju, który ich wymaga; w krojach … | font-variant-ligatures: common-ligatures | P1-07 |
| M-49 | 1 | Sprawdź, że oprogramowanie wstawia wszystkie pożądane ligatury i tylko je, i że ligatury zostają na … | kontrola jakości: ligatury w przeglądarce włączone domyślnie | poza pokazem: kontrola, nie reguła |
| M-50 | 1 | Ligatury dyskrecjonalne (Th, ct, st, sp) to osobny rejestr stylistyczny; nie mieszaj ich z podstawowymi … | font-variant-ligatures: discretionary-ligatures osobno | P1-07 |
| M-51 | 1 | Tekst spacjowany nie ma ligatur nieistotnych (wyłącz ligatury przy letterspacingu). | spec CSS wyłącza ligatury przy letter-spacing ≠ 0 | P1-07 |
| M-52 | 1 | Jeśli rezygnujesz z ligatur, wybierz kroje o niekolidującym f (Aldus, Sabon, Palatino, Trump Mediaeval) … | font-variant-ligatures: none dla fontów bez potrzeby | P1-07 |
| M-53 | 1 | Ligatury leksykalne (æ, œ) są wymagane przez język lub cytat z dawnego tekstu; ligatury typograficzne … | lang i font-variant-ligatures dla tureckiego | poza pokazem: dotyczy języka tureckiego |
| M-54 | 1 | Cyfry tytułowe (lining) stosuj z wersalikami; cyfry tekstowe (old-style, text figures) we wszystkich … | font-variant-numeric: oldstyle-nums w tekście, lining-nums przy wersalikach | P1-08 |
| M-55 | 1 | W tabelach i kolumnach liczbowych cyfry tabelaryczne (równa szerokość); w tekście bieżącym cyfry … | tabular-nums w tabelach, proportional-nums w tekście | P1-08 |
| M-56 | 1 | Cyfry w tekście wymagają kerningu między sobą i względem półpauzy; cyfry nie są pomijane w tablicach … | font-kerning: normal; reszta w tablicy fontu | P1-09 |
| M-57 | 1 | Znaki walut i działań dopasuj do stylu cyfr (mniejsze przy cyfrach tekstowych). | dobór fontu z dopasowanymi znakami walut | poza pokazem: cecha fontu |
| M-58 | 1 | Wykładniki, liczniki ułamków i indeksy dolne (H₂O, mianowniki) składaj prawdziwymi znakami „superior” i … | font-variant-position: sub/super i elementy sup/sub | P1-08 |
| M-59 | 1+2 | Cyfry w parach nie wymagają spacjowania; ciągi trzech i więcej cyfr (telefony, numery seryjne, daty) … | K1: letter-spacing dla ciągów cyfr (znacznik); K2: automatyczne wykrywanie ciągów | P2-09 |
| M-60 | 2 | Separator dziesiętny w Europie to przecinek, a tysiące grupuje się spacją (10 000 000); zapis 10,001 bez … | Intl.NumberFormat pl / regex, twarda cienka spacja | P2-09 |
| M-61 | 1+2 | Ułamki: gotowe znaki (¼ ½ ¾) lub ułamek zbudowany z licznika superior, ułamkowej kreski (solidus) i … | K1: font-variant-numeric: diagonal-fractions; K2: zamiana 1/2 → ½ znakiem | P1-08; P2-06 |
| M-62 | 2 | Znak wymiaru: × (nie litera x) w „26 × 42 cm”, „2 × 4”; znak minus − i znaki działań z jednego fontu … | regex x → ×, minus → − | P2-06 |
| M-63 | 2 | Zakres liczb (3–6 listopada, 4:30–5:00, 25–30 mm): półpauza ciasno, bez spacji (lub kreska ok. 1/3 em) … | regex zakresów cyfr → półpauza | P2-04 |
| M-64 | 2 | Bez apostrofu w liczbowych liczbach mnogich (lata 1930., dwójki 2 × 4s); bez kropki po jednostkach … | apostrof w liczbach mnogich i kropki po jednostkach | poza pokazem: reguła angielska, nie dotyczy polskiego |
| M-65 | 2 | Prime (′ ″) tylko dla stóp, cali, minut i sekund łuku; nie używaj ich jako cudzysłowów ani apostrofów … | regex ′ ″ ° (przy jednostkach) | P2-07 |
| M-66 | 1 | Ustaw tekst ragged right, gdy to pasuje do tekstu i strony; w wąskich kolumnach (wielokolumnowość) … | text-align: left (ragged) / justify | P1-13 |
| M-67 | 1 | „Twardy rag”: stałe odstępy, brak minimalnej długości wiersza, brak letterspacingu i dzielenia poza tym … | „twardy rag”: hyphens: manual, bez letter-spacing | P1-13 |
| M-68 | 1+2 | Dobry rag wygląda przyjemnie nierówno, bez wierszy skrajnie długich lub krótkich i z minimum dzieleń … | K1: text-wrap: pretty; K2: detektor złego ragu | P1-11; P2-22 |
| M-69 | 1 | Tekst wyrównany do prawej (ragged left) tylko w krótkich blokach (notki, pull quote, podpisy, sąsiednie … | text-align: right tylko w marginaliach i podpisach | P1-22 |
| M-70 | 1 | Tekst wyśrodkowany: łam wiersze „dla sensu” (fraza w wierszu), z różnicą długości wierszy; używaj do … | text-wrap: balance, <wbr>/<br> dla sensu | P1-10 |
| M-71 | 2 | Justowanie: najlepszy silnik liczy podział paragrafami, nie wiersz po wierszu; mikroregulacja odstępu … | algorytm Knutha–Plassa po stronie klienta (tex-linebreak) | P2-14 |
| M-72 | 1 | Żadne oprogramowanie nie powinno automatycznie ściskać, rozciągać ani spacjować tekstu, żeby go … | zakaz scaleX/letter-spacing ujemnego dla dopasowania (rozstrzygnięte w K-06) | poza pokazem: zakaz, ujęty w P2-14 i P1-13 |
| M-73 | 1 | W tekście justowanym unikaj dziur i rzek: wąska kolumna, długie wyrazy i zbyt mała miara dają luki … | @container: justuj tylko dla miary ≥ 40ch | P1-13 |
| M-74 | 1+2 | Hanging punctuation: cudzysłowy otwierające i znaki na początku wiersza wiszą w marginesie, aby krawędź … | K1: hanging-punctuation (tylko Safari); K2: fallback JS (Chrome, Firefox) | P1-14; P2-15 |
| M-75 | 1 | Poezja składa się flush left, bo łamania wersów są elementem formy; wyśrodkowanie poezji tylko wyjątkowo. | text-align: left i white-space: pre-line dla wersów | P1-16 |
| M-76 | 1 | Jedna spacja po kropce, dwukropku i innych znakach (nie dwie); en space między zdaniami tylko w … | HTML zwija białe znaki; nic do wdrożenia | poza pokazem: zachowanie domyślne |
| M-77 | 1 | Spacja nie służy do wcięć, centrowania ani pozycjonowania (używaj tabulatorów i wcięć). | wcięcia przez CSS, nie spacje | poza pokazem: praktyka kodowania |
| M-78 | 1 | Odstęp międzywyrazowy dostosuj do rozmiaru i kroju: typowo M/4 (ok. ¼ em); justowany: minimum M/5 … | word-spacing w em (domyślnie spacja fontu) | P1-09 |
| M-79 | 1 | Przy dzieleniu zostaw w pierwszym wierszu co najmniej 2 znaki, przenieś co najmniej 3 (fi-nally, nie … | hyphens: auto, hyphenate-limit-chars: 5 2 3 | P1-12 |
| M-80 | 1+2 | Ostatni wiersz akapitu nie może być końcówką dzielonego słowa ani wyrazem krótszym niż 4 litery. | K1: text-wrap: pretty (przybliżenie); K2: wiązanie ostatnich wyrazów nbsp | P1-11; P2-12 |
| M-81 | 2 | Nie więcej niż 3 kolejne wiersze zakończone dzieleniem. | brak CSS (hyphenate-limit-lines tylko w Safari preview); własny JS po pomiarze wierszy | poza pokazem: wysoki koszt, brak uniwersalnego algorytmu |
| M-82 | 1 | Nazwy własne dziel tylko w ostateczności, chyba że występują tak często jak rzeczowniki pospolite. | hyphens: none dla znaczników z nazwami | poza pokazem: nadwyżka K1 (R1-17) |
| M-83 | 1+2 | Dziel według reguł języka tekstu, także przy pojedynczych cytowanych wyrazach obcych. | K1: lang=pl + hyphens: auto; K2: słownik polski przez Hyphenopoly | P1-12; P2-13 |
| M-84 | 2 | Nie zaczynaj więcej niż dwóch kolejnych wierszy tym samym słowem. | samo wykrycie powtórzeń (JS); poprawa ręczna | poza pokazem: brak algorytmu naprawczego, niski zysk |
| M-85 | 1 | Unikaj dzielenia wyrazów tam, gdzie tekst jest przerwany (ilustracja, mapa, pull quote, ramka). | hyphens: none w pull quote i podpisach | poza pokazem: nadwyżka K1 (R1-17) |
| M-86 | 1 | W tekście ragged i wyśrodkowanym wyłącz automatyczne dzielenie; zastąp je dzieleniem warunkowym (&shy;) … | hyphens: manual i &shy; | P1-13 |
| M-87 | 1 | Do dzielenia ręcznego używaj łącznika warunkowego, nie twardego: twardy łącznik wstawiony w miejscu … | &shy; zamiast twardego łącznika | P1-13 |
| M-88 | 1+3 | Nigdy nie zaczynaj strony ostatnim wierszem wielowierszowego akapitu („wdowa” u Bringhursta: ma … | K1: widows: 2 w układzie kolumnowym; K3: w przewijanym tekście brak stron | P1-22 (część K1) |
| M-89 | 1+3 | Samotny pierwszy wiersz akapitu na dole strony („sierota” u Bringhursta: ma przyszłość, więc „nie trapi … | K1: orphans: 2 w układzie kolumnowym; K3: w przewijanym tekście brak stron | P1-22 (część K1) |
| M-90 | 3 | Wyrównuj głębokość rozkładówki przez przenoszenie pojedynczych wierszy z poprzednich lub do następnych … | Niemożliwe: brak rozkładówek i stron. Przybliżenie: column-fill: balance wyrównuje kolumny | poza pokazem: niemożliwe (przybliżenie w P1-22) |
| M-91 | 3 | Pozostawiony na ostatniej stronie rozdziału kilkuwierszowy ogon: rozciągnij kilka poprzednich … | Niemożliwe: brak ostatniej strony rozdziału. Przybliżenie: brak (treść przepływa) | poza pokazem: niemożliwe |
| M-92 | 1 | Nie zostawiaj nagłówka podrzędnego na dole strony oderwanego od tekstu (sierota nagłówka). | break-after: avoid(-column) przy nagłówkach w kolumnach | P1-22 |
| M-93 | 2 | Inicjały osobowe: zbędna lub minimalna (cienka, włosowa) spacja po wewnętrznych kropkach (W. B. Yeats) … | regex inicjałów, cienka spacja i nbsp przed nazwiskiem | P2-11 |
| M-94 | 2 | Wtrącenie oznaczaj półpauzą (en dash) ze zwykłą spacją po obu stronach, nie zwartą pauzą em ani … | półpauza ze spacjami we wtrąceniach (wersja wybrana, K-01) | P2-03 |
| M-95 | 2 | Wtrącenie oznaczaj pauzą em bez spacji wokół; pauza oznacza silne przerwanie wypowiedzi. | wersja odrzucona w K-01 | poza pokazem: odrzucona (K-01) |
| M-96 | 2 | Nie używaj podwójnego łącznika (--) ani łącznika zamiast pauzy/półpauzy; półpauza nie zastępuje łącznika … | -- i „ - ” → półpauza | P2-03 |
| M-97 | 2 | Pauza dialogowa: pauza z cienką spacją (M/5) lub spacją na początku wypowiedzi zamiast cudzysłowów. | pauza dialogowa | poza pokazem: rzadki kontekst, brak dialogu w demo |
| M-98 | 2 | Trzy-em (––) jako znak powtórzenia nazwiska w bibliografii. | znak powtórzenia w bibliografii | poza pokazem: rzadka konwencja |
| M-99 | 1 | Ukośnik (virgule) w słowach i datach, z odpowiednim kerningiem; ułamkowa kreska pod kątem ok. 45° tylko … | ukośnik z fontu; kerning w foncie | poza pokazem: cecha fontu |
| M-100 | 2 | Wielokropek jednym znakiem lub trzema kropkami dopasowanymi do kroju (flush, z cienkimi spacjami, nieco … | ... → … (Typograf) | P2-05 |
| M-101 | 2 | Interpunkcja jest notacją, nie ekspresją: nie składaj wielokrotnych !!!/???, nie powtarzaj kresek; kilka … | !!! → !, ?? → ? | P2-05 |
| M-102 | 1 | Nawiasy okrągłe i kwadratowe są pionowe nawet w italic i dobrane do kroju (nie nabrzmiałe ukośne), z … | @font-face z unicode-range dla nawiasów w roman | poza pokazem: nadwyżka K1 (R1-12) |
| M-103 | 1+2 | Cudzysłowy typograficzne (otwierające i zamykające), nie proste; apostrof to znak zamykającego … | K2: cudzysłowy i apostrof (Typograf pl); K1: <q> i quotes | P2-02; poza pokazem: nadwyżka K1 (R1-13) |
| M-104 | 1+2 | Postać i liczba cudzysłowów zależą od języka: odwrócone przecinki w krajach angielskich, dolne i górne … | K2: „…” i «…» (Typograf pl); K1: quotes dla <q> | P2-02; poza pokazem: nadwyżka K1 (R1-13) |
| M-105 | 2 | Pozycja cudzysłowu względem innej interpunkcji jest spójna (amerykańsko: przecinek i kropka wewnątrz … | pozycja cudzysłowu względem przecinka | poza pokazem: konwencja redakcyjna, zależna od języka |
| M-106 | 2 | Usuń zbędną interpunkcję: kropki po jednostkach i w skrótach pisanych kapitalikami, zbędne łączniki … | usuwanie zbędnych kropek i łączników | poza pokazem: wymaga rozumienia tekstu |
| M-107 | 1 | Znaki analfabetyczne (nawiasy, gwiazdka, §, ¶, #, ampersand, kropka) dobieraj z tego samego kroju; jeśli … | dobór znaków analfabetycznych (unicode-range) | poza pokazem: decyzja o foncie |
| M-108 | 1 | W nagłówkach i tytułach używaj najlepszego dostępnego ampersandu (często z italic). | ampersand italic przez unicode-range | poza pokazem: nadwyżka K1 (R1-12) |
| M-109 | 1 | Midpoint (·) jako separator w poziomej linii i znacznik listy (bullet • wiszący); znak inskrypcyjny w … | content: „·”, list-style, ::marker | P1-18 |
| M-110 | 1+2 | © na linii bazowej (nie superskrypt); ® i ™ jako superskrypty; § podwojony (§§) dla liczby mnogiej. | K1: sup dla ® ™; K2: (c)(r)(tm) → ©®™ | P2-07 |
| M-111 | 1 | Do mocniejszego odstępu w linii (podtytuł od tekstu, elementy papieru firmowego) użyj en space; do … | encje &ensp; &thinsp; &hairsp; | poza pokazem: znaki wprowadzane w tekście (P2-11) |
| M-112 | 3 | Łącznik (hyphen) ma szerokość ok. 1/4 em (czasem 1/5 em w krojach ekonomicznych), a jego kształt i … | Niemożliwe: kształt i szerokość łącznika to cecha fontu. Przybliżenie: wybór fontu o odpowiednim łączniku | poza pokazem: niemożliwe |
| M-113 | 2 | Krótkie wyrażenia liczbowe i matematyczne łącz twardą spacją (6,2 mm; 3 in.; 4 × 4; strona 3; rozdział … | nbsp: liczby z jednostkami, str. 3, rozdz. 5, § | P2-08 |
| M-114 | 2 | Polska reguła: jednoliterowe spójniki i przyimki (a, i, o, u, w, z) nie kończą wiersza (twarda spacja po … | nbsp po jednoliterowych spójnikach (Typograf lengthShortWord = 1) | P2-01 |
| M-115 | 1 | Nie stosuj kropek wiodących (dot leaders) ani gigantycznych luk w spisach i listach; sparuj tytuł z … | układ siatki dla spisów i list, bez kropek wiodących | poza pokazem: nadwyżka K1 (R1-08) |
| M-116 | 1 | Kerninguj spójnie i skromnie albo wcale; zbyt mało jest lepsze niż zbyt dużo, niespójne gorsze niż żadne. | font-kerning: normal | P1-09 |
| M-117 | 3 | Kerning dostosowany do języka (apostrofy: en ’d ’m ’s; fr. ’a ’e; niem. „T), bez kolizji z diakrytykami … | Niemożliwe: tablice kerningu języka siedzą w foncie. Przybliżenie: lang i font z kerningiem pl | poza pokazem: niemożliwe |
| M-118 | 1+3 | Kerning metryczny (tablica fontu) do tekstu, optyczny do nagłówków i krojów bez tablicy; różnice … | K1: text-rendering: optimizeLegibility, font-kerning; K3: kerning optyczny | P1-09 (część K1) |
| M-119 | 3 | Nie rozbudowuj tablicy kerningu, by ratować źle dopasowane znaki (oo, oe); popraw sidebearings; tablica … | Niemożliwe: sidebearings to edycja fontu. Przybliżenie: wybór poprawnie rozstawionego kroju | poza pokazem: niemożliwe |
| M-120 | 1 | Spacjuj wersaliki i kapitaliki w ciągu (akronimy, tytuły) o 5–10% rozmiaru; w tytułach więcej (20–25% … | letter-spacing 0,05–0,1em dla kapitalików i wersalików | P1-06 |
| M-121 | 1 | Nie spacjuj małych liter bez powodu; wyjątki: bezszeryfowe pogrubione zwężone w nagłówkach (ok. 10%) … | brak spacjowania małych liter; wyjątki w klasach | P1-06 |
| M-122 | 1 | Tracking w tekście ciągłym tylko w małych przyrostach; ujemny rzadko i oszczędnie przy krótkim wierszu … | letter-spacing dla tekstu jasnego na ciemnym | poza pokazem: nadwyżka K1 (R1-16) |
| M-123 | 1 | Duże rozmiary: tracking ciaśniej, odstęp międzywyrazowy zmniejszony (ok. 80%); wersaliki i kapitaliki … | word-spacing i letter-spacing zmniejszone w dużych rozmiarach | P1-09 |
| M-124 | 1 | Nie spacjuj tekstu w tak ciasnym ujęciu, że litery się dotykają (tight tracking = type crime). | zakaz ciasnego trackingu | poza pokazem: zakaz ujęty w P1-09 |
| M-125 | 1 | Jedno wyróżnienie = jeden sygnał (kursywa jest standardem; alternatywy: bold, kapitaliki, kolor); nie … | em i strong jako jedyny sygnał | P1-05 |
| M-126 | 2 | Przy wyróżnieniu pogrubieniem interpunkcję zostaw w kroju bazowym; przy kursywie interpunkcja też … | owijanie interpunkcji w kroju bazowym (JS) | poza pokazem: niski zysk |
| M-127 | 1 | Podkreślenie jest rzadko używane w formalnej typografii (zastępuje je kursywa); w druku nie podkreślaj … | text-decoration-skip-ink, text-underline-offset | poza pokazem: nadwyżka K1 (R1-11) |
| M-128 | 1 | Pierwszy akapit po tytule lub nagłówku bez wcięcia; wcięcie sygnalizuje przerwę, której na początku nie … | :is(h1..h6,hr,figure) + p { text-indent: 0 } | P1-15 |
| M-129 | 1 | Kolejne akapity w tekście ciągłym: wcięcie co najmniej 1 en (typowo 1 em lub 1 interlinia; do 3 em) … | text-indent: 1em dla kolejnych akapitów | P1-15 |
| M-130 | 1 | Akapit oznaczaj wcięciem albo odstępem, nie obiema rzeczami naraz; odstęp ma być precyzyjnym przyrostem … | wcięcie albo odstęp, nie oba (K-02) | P1-15 |
| M-131 | 1 | Akapity blokowe (bez wcięcia, biała linia): krótkie dokumenty biznesowe; w długich tekstach „bezduszne”. | akapity blokowe (margin) w tekście ciągłym | poza pokazem: odrzucone w K-02 |
| M-132 | 1 | Alternatywy dla wcięcia: znak akapitu (pilcrow, kwadracik, bullet) w biegu tekstu (oszczędne, ale … | pilcrow ::before, akapit wiszący | poza pokazem: nadwyżka K1 (R1-15) |
| M-133 | 1 | Cytat blokowy wyróżnij jednym środkiem (zmiana kroju na italic, zmniejszenie rozmiaru lub wcięcie) … | blockquote: italic lub mniejszy rozmiar lub wcięcie | P1-16 |
| M-134 | 1 | Cytat wierszowany wcinaj lub wyśrodkuj na najdłuższym wersie (zachowaj ragged right); wcięcie = (miara − … | width: fit-content; margin-inline: auto; text-align: left | P1-16 |
| M-135 | 1+2 | Jeśli tekst otwiera cytat, zachowaj cudzysłów otwierający (także przy inicjale). | cudzysłów otwierający jako wiszący | P1-14; P2-15 |
| M-136 | 1 | Oznacz każdy początek i wznowienie tekstu (po nagłówku wystarczy brak wcięcia; w pozostałych miejscach … | ::first-line w kapitalikach | P1-17 |
| M-137 | 1 | Inicjał: podniesiony (elevated) na linii bazowej pierwszego wiersza, wcięty (drop cap) w blok N wierszy … | initial-letter z fallbackiem float | P1-17 |
| M-138 | 1 | Inicjały A, I, O mogą być słowem: odstęp inicjału od reszty wyrazu nie może wprowadzać w błąd (np. … | odstęp inicjału A/I/O | P1-17 |
| M-139 | 1 | Obszar wcięty pod inicjał jest prostokątny, co przy literze o ukośnych bokach (A) wygląda niezgrabnie … | shape-outside, initial-letter-align | P1-17 |
| M-140 | 1 | Wcięcie, sinkage i rozmiar inicjału można związać proporcją (złoty podział: 38,2% miary, inicjał 61,8% … | rozmiar inicjału w jednostce cap | P1-17 |
| M-141 | 1+2 | Forma przypisów: boczne (najlepiej widoczne), dolne (krótkie, rzadkie), końcowe (dowolnej długości) … | K1: przypisy boczne (anchor positioning, float); K2: rozmieszczenie bez kolizji | P1-22; P2-18 |
| M-142 | 1 | Rozmiary: dolne 8–9 pt, końcowe 9–10 pt, boczne do rozmiaru tekstu głównego. | font-size przypisów 8–9 pt, bocznych do tekstu | P1-22 |
| M-143 | 1+2 | Odsyłacz w tekście jako superskrypt (liczba o zredukowanym rozmiarze, w razie potrzeby półbold i z … | K1: sup, wiszący numer; K2: autonumeracja | P2-18 (część K2); poza pokazem: nadwyżka K1 (R1-04) |
| M-144 | 1 | Przypisy boczne mogą nie mieć wskaźników albo mieć stały znak (*). | przypisy boczne bez wskaźników | P1-22 |
| M-145 | 1 | Przypisy końcowe jednoznacznie: razem na końcu publikacji, numeracja ciągła; przy numeracji w … | przypisy końcowe: kotwice i licznik CSS | poza pokazem: struktura dokumentu |
| M-146 | 2 | Pełne diakrytyki i znaki nazw własnych oraz wyrazów obcych (ą ę ł ń ó ś ź ż i inne); font musi mieć … | sprawdzenie pokrycia (opentype.js), subsetting | P2-24 |
| M-147 | 1 | Tekst składa się z abstrakcyjnych znaków (f+f+i), a ligatury i alternatywy są glifami wybieranymi w … | znaki zamiast glifów w tekście (U+FB01 itd. niepożądane) | poza pokazem: zasada kodowania |
| M-148 | 1+3 | Język tekstu steruje zasadami składu: cudzysłowami, dzieleniem, kerningiem apostrofów i odstępami przy  … | K1: lang i selektory :lang(); K3: kompromisowy sidebearing znaków | poza pokazem: dubluje P1-12 i P2-02 |
| M-149 | 2 | W tekście bieżącym nie używaj znaków bez funkcji typograficznej (ukośnik wsteczny, pionowa kreska pipe … | lint znaków bez funkcji typograficznej | P2-23 |
| M-150 | 1 | Mieszając alfabety (łaciński, grecki, cyrylica, hebrajski), dobierz kroje o zbliżonym kolorze i … | fonty grecki i cyrylicy przez unicode-range | poza pokazem: demo jest po polsku |
| M-151 | 1 | Alfabety w jednym tekście dopasuj optycznie, nie matematycznie: różnice wysokości x i rozciągłości (np. … | font-size-adjust przy mieszaniu alfabetów | poza pokazem: nadwyżka K1 (R1-02) |
| M-152 | 1 | Pełny font tekstowy zamiast fontu „pi” dla fragmentów greckich i podobnych; matching punctuation i … | font-family z pełnym fontem | poza pokazem: decyzja o doborze kroju |
| M-153 | 3 | W nowych ortografiach nie dodawaj zbędnych znaków; dodawaj tylko wizualnie rozróżnialne; unikaj … | Niemożliwe: dotyczy projektowania ortografii i fontu, nie składu. Przybliżenie: brak | poza pokazem: niemożliwe, nie dotyczy polskiego |
| A-01 | 1 | Proporcje strony wybieraj spośród satysfakcjonujących kanonów (muzyczne, z figur geometrycznych, złoty … | aspect-ratio dla „strony” demonstracyjnej | P1-19 |
| A-02 | 1 | Proporcja strony odpowiada treści, rozmiarowi i ambicji: zwykłe książki od 5:9 (1:1,8) do 4:5 (1:1,25) … | wybór proporcji z kanonu (aspect-ratio) | P1-20 |
| A-03 | 1 | Kanon proporcji muzycznych jako lista kontrolna: 1:2 (oktawa), 8:15, 9:16, 3:5, 5:8, 1:√2, 2:3 (kwinta) … | lista kanonów jako warianty aspect-ratio | P1-20 |
| A-04 | 1 | Strony 2:3 i 3:4 (kwinta, kwarta) to ulubione kształty średniowiecza; po złożeniu arkusza odtwarzają się … | aspect-ratio: 2 / 3 (i 3 / 4) | P1-19 |
| A-05 | 1 | Proporcja 1:√2 (ISO) odtwarza się przy każdym złożeniu, ale sama w sobie jest najmniej „muzyczna” … | aspect-ratio: 1.414 z polem o innym kształcie | P1-20 |
| A-06 | 1 | Złoty podział (1:1,618; 38,2% / 61,8%; a:b = b:(a+b)) jako proporcja strony lub pola składu; po odjęciu … | aspect-ratio: 1.618 i pole złotego podziału | P1-20 |
| A-07 | 1 | Złoty podział nie jest bardziej uzasadnioną podstawą proporcji niż inne metody (standardowy papier … | uwaga sceptyczna; odzwierciedlona w przełączniku jako jedna z alternatyw (K-05) | poza pokazem: stanowisko, nie reguła |
| A-08 | 1 | Ilustracje współdecydują o formacie: strona nieco głębsza niż typowa ilustracja (miejsce na podpis) … | aspect-ratio dla ilustracji, miejsce na podpis | poza pokazem: nadwyżka K1 (R1-09) |
| A-09 | 1 | Proporcje stron i kolumn mają skojarzenia historyczne: długa linia egipska to nacisk na pisanie, nie … | proporcje wg epoki: warianty aspect-ratio | poza pokazem: dubluje P1-20 |
| A-10 | 1 | Pole składu równoważ i kontrastuj z kształtem strony: proporcje strony i pola mają różnić się wyraźnie i … | różne proporcje strony i pola składu | P1-20 |
| A-11 | 1 | Tekst do czytania ciągłego ustawiaj w kolumnie wyraźnie wyższej niż szerokiej; bardzo wąskie i długie … | pole wyższe niż szerokie (aspect-ratio) | P1-20 |
| A-12 | 1 | Idealny kwadrat tekstu na kwadratowej stronie z równymi marginesami nie ma punktów orientacyjnych; buduj … | brak kwadratu w kwadracie: marginesy nierówne | P1-20 |
| A-13 | 1 | Pole składu umieszczaj wyżej i ku grzbietowi, nie na środku strony. | padding: góra mniejsza niż dół, grzbiet mniejszy niż zewnętrzny | P1-19 |
| A-14 | 1 | Wysokość pola składu jako całkowita liczba linii powiązana z marginesem grzbietowym (λ = s/3 → 27 linii … | block-size: calc(N * 1lh) | P1-19 |
| A-15 | 1 | Kanon średniowieczny (Tschichold 1955 wg Villarda de Honnecourt): strona 2:3, pole 2:3, s = w/9, t = … | marginesy w % szerokości: s = 1/9, t = 1/6 (w), e = 2/9, f = 1/3 (w) | P1-19 |
| A-16 | 1 | Aldus 1499: strona 2:3, pole 1:1,7 (wysoki pentagon), s = t = w/9, e = 2s. | wariant Aldusa: pole 1:1,7, marginesy 1/9, 2/9 | P1-19 |
| A-17 | 1 | Froissart 1559: strona złotego podziału, pole 1:1,87 (wysoki heksagon), s = w/9, t = s, e = 2s; kolumna … | wariant Froissarta: strona złotego podziału, pole 1:1,87 | P1-20 |
| A-18 | 1 | Pole złotego podziału na stronie ISO (1:√2): s = t = w/9, e = f = 2s (marginesy 1:2 spinają pole i … | wariant ISO + złote pole, marginesy 1:2 | P1-20 |
| A-19 | 1 | Pole 1:2 (podwójny kwadrat) na stronie 1:√2: s = w/12, f = 2t = h/9, e = w/3; szeroki margines … | pole 1:2 na stronie 1:√2, e = w/3 | P1-20 |
| A-20 | 1 | Margines zewnętrzny szerszy od wewnętrznego (tradycja kodeksów: e = 2s); wyjątek: książka poezji z polem … | margines zewnętrzny szerszy (KONFLIKT K-03 rozstrzygnięty) | P1-19 |
| A-21 | 1 | Marginesy wewnętrzne rozkładówki szersze od zewnętrznych dają więcej otwartej przestrzeni przy grzbiecie … | marginesy wewnętrzne szersze | poza pokazem: odrzucona (K-03) |
| A-22 | 1 | Marginesy mają trzy zadania: spiąć pole składu ze stroną (i strony sąsiednie) siłą proporcji, oprawić … | marginesy jako stosunek do szerokości kontenera | P1-19 |
| A-23 | 1 | Marginesy ustawiaj swobodnymi proporcjami, nie okrągłymi jednostkami; najpierw ustaw pole składu w … | marginesy w % i proporcjach, nie w px | P1-19 |
| A-24 | 1 | Równe marginesy dookoła są ekonomiczne, ale mało interesujące; strona o polu kwadratowym i marginesach … | marginesy równe (stan „przed” w P1-19) | poza pokazem: antywzorzec, pokazany jako stan wyłączony P1-19 |
| A-25 | 1 | Układ planuj od zewnątrz do wewnątrz (format i marginesy, kolumna to reszta) albo od wewnątrz (marginesy … | sposób pracy (od zewnątrz/ od wewnątrz) | poza pokazem: metoda, nie efekt |
| A-26 | 1 | Siatka jest regulatorem proporcji i programem: maksimum stałych, maksimum zmienności; elastyczny … | grid-template-columns, gap, strefy | P1-21 |
| A-27 | 1 | Siatka kolumnowa: im więcej kolumn, tym większa elastyczność; element zajmuje jedną lub kilka kolumn … | kolumny grid, elementy spanujące | P1-21 |
| A-28 | 1 | Siatka z linią zawieszenia (hang line, datum): pozioma linia, od której „wiszą” kolumny; górna strefa … | grid-template-rows, wspólna linia (subgrid) | P1-21 |
| A-29 | 1 | Siatka modułowa: kolumny i wiersze o spójnych podziałach; moduły rządzą rozmieszczeniem i kadrowaniem … | siatka modułowa grid-template-columns/rows | P1-21 |
| A-30 | 1 | Siatka bazowa: rozmiar i interlinia tekstu jako liczby całkowite (bez „auto”); liczbę modułów w pionie … | rlh i zmienna --u; nakładka siatki bazowej | P1-03 |
| A-31 | 1 | Style nagłówków, podtytułów i podpisów dobieraj z wielokrotności jednostki siatki bazowej (np. 18/24 … | line-height jako wielokrotność jednostki w stylach nagłówków | P1-03 |
| A-32 | 1 | Układaj elementy względem siatki bazowej, ale jej nie forsuj: czasem układ działa lepiej po nadpisaniu … | przełącznik widoczności nakładki siatki | P1-21 |
| A-33 | 1 | Prawdziwa siatka pozwala komponentom „łamać siatkę” przez przekroczenie kilku kolumn; białe płaszczyzny … | grid-column: 1 / -1 łamie siatkę | P1-21 |
| A-34 | 1 | Skala modułowa do podziału strony: pola, kolumny i marginesy w jednostkach z jednej skali (np. strona 52 … | skala modułowa dla podziałów siatki | P1-21 |
| A-35 | 1 | Dwa bloki tekstu różnych rozmiarów zestawione obok siebie wyrównaj na wspólnej linii bazowej (np. 14/18 … | align-items: last baseline, text-box-trim | poza pokazem: nadwyżka K1 (R1-10) |
| A-36 | 1 | Obrazy dopasowuj do modułów kolumn (zajmują jedną, dwie lub trzy strefy) i kadruj do modułu; tekst nie … | aspect-ratio i object-fit w modułach | poza pokazem: nadwyżka K1 (R1-09) |
| A-37 | 1 | Zaczynaj od siatki i szkieletu stron (wireframe), dopiero potem kroje, hierarchia i style nawigacji. | sposób pracy (siatka przed krojami) | poza pokazem: metoda |
| A-38 | 1 | Kolumna boczna na notatki (sidenotes) w marginesie zewnętrznym: może być bardzo wąska rynna (6–7 pt przy … | przypisy boczne w kolumnie marginesu (anchor positioning lub float) | P1-22 |
| A-39 | 1 | Marginalia składaj krótkim wierszem ragged (nawet 12–15 znaków); na stronie lewej flush right, by … | text-align w marginaliach | P1-22 |
| A-40 | 1 | Wiele kolumn, gdy tekst przekracza 500 słów na stronę, gdy elementów jest wiele lub gdy ilustracje … | column-count/width, column-fill: balance | P1-22 |
| A-41 | 1 | Rynny między kolumnami w stosunku do miary (g = m/20, w/75, s/4); różnica rozmiaru i kroju zapobiega … | column-gap w proporcji do miary | P1-22 |
| A-42 | 1 | Przy wielu językach każdy język dostaje strefę proporcjonalną do tekstury pisma; teksty równoległe obok … | strefy dla wielu języków | poza pokazem: demo jednojęzyczne |
| A-43 | 1 | Siatka pięciokolumnowa: tekst główny w czterech kolumnach, mniejsze teksty w jednej; pull quote w ramce … | siatka pięciokolumnowa 4 + 1 | P1-21 |
| A-44 | 3 | Książki i czasopisma projektuj jako rozkładówki: jednostką projektu jest para stron, a nie pojedyncza … | Niemożliwe: pojedyncza strona/rozkładówka nie istnieje w przewijanym dokumencie. Przybliżenie: dwie „strony” obok siebie w kontenerze | P1-23 (przybliżenie) |
| A-45 | 1 | Rozkładówka jest symetryczna poziomo (kierunek przewracania) i asymetryczna pionowo (pole składu wyżej i … | dwa kontenery z lustrzanymi marginesami | P1-23 |
| A-46 | 3 | Rozkładówki ciągłego tekstu mają równą głębokość; nie powinny różnić się od sąsiednich o więcej niż … | Niemożliwe: brak przepływu na strony. Przybliżenie: column-fill: balance | poza pokazem: niemożliwe (P1-22) |
| A-47 | 3 | Wiersze na obu stronach rozkładówki i obu stronach kartki pokrywają się; skład sprawdza się pod światło … | Niemożliwe: brak kartki i światła. Przybliżenie: wspólna siatka bazowa obu stron | poza pokazem: niemożliwe (P1-03, P1-23) |
| A-48 | 3 | Folio (numer strony) w dokumentach dłuższych niż dwie strony; miejsca: (1) góra, przy zewnętrznej … | Niemożliwe: nie ma numeru strony. Przybliżenie: numer sekcji w marginesie (JS) | P2-20 (przybliżenie) |
| A-49 | 3 | Folio w rozmiarze tekstu i blisko pola składu; dalej znika, wzmocnione rozprasza. | Niemożliwe: j.w. Przybliżenie: sticky w rozmiarze tekstu przy polu | P2-20 (przybliżenie) |
| A-50 | 2 | Żywa pagina jest niezbędna w antologiach i opracowaniach, zbędna w tekstach o jednym głosie lub jednym … | IntersectionObserver aktualizuje bieżącą żywą paginę | P2-20 |
| A-51 | 1 | Nagłówki marginesowe (shoulderheads) wyróżniają bez powiększania. | nagłówki w kolumnie marginesu | P1-22 |
| A-52 | 1 | Wprowadź projekt do marginesów: wiszące numery, wcięcia, folia, żywe paginy, notki boczne wiążą stronę z … | grid z kolumną marginesu, numery wiszące | P1-22 |
| A-53 | 2 | Elementy nawigacji dokumentu (numery stron, nagłówki, spis treści, indeks, przypisy, abstrakt) … | generowanie spisu treści z nagłówków | P2-21 |
| A-54 | 1 | Pusta przestrzeń nadaje równowagę (poise): strona tytułowa z kilkoma liniami i wyważoną pustką; niektóre … | pustka wynika z marginesów; nie ma osobnej reguły (K-04) | poza pokazem: efekt zbiorczy P1-19 |
| A-55 | 1 | Gęstość informacji zamiast pustki: jedna dobrze zorganizowana, gęsta powierzchnia bywa lepsza niż wiele … | gęstość informacji w tabelach (K-04) | poza pokazem: odrzucone dla tekstu, stosowane w P1-18 |
| A-56 | 1 | Sama pustka na początku rozdziału nie daje poczucia celebracji, a brak pustki nie jest ubóstwem (wąskie … | układ początku rozdziału | poza pokazem: dubluje P1-17 |
| A-57 | 1+2 | Wszystkie odstępstwa od tekstu (nagłówki, cytaty, przypisy, ilustracje) są synkopami wobec stałego rytmu … | rytm z P1-03; obrazy z P2-17 | P1-03; P2-17 |
| A-58 | 1 | Projekt strony ma być na tyle giętki, by dać tekstowi „zamieszkalny dom”: tekstura tekstu ma … | płynny układ zamiast stałej wysokości | poza pokazem: zasada architektury CSS |
| A-59 | 1 | Nie wyrównuj głębokości stron zmianą interlinii (justowanie pionowe) ani rozpychaniem odstępów między … | brak justowania pionowego (align-content nie rozciąga) | poza pokazem: zakaz |
| A-60 | 1 | Niezgodności między miarą optyczną a arytmetyczną (zaokrąglenia, centrowanie, łączenie proporcji) … | jednostki względne (rem, ch) | poza pokazem: zasada architektury CSS |
| A-61 | 1 | Widoczne relacje między tekstem a innymi elementami (zdjęcia, podpisy, tabele, diagramy, przypisy) … | figure / figcaption i odstęp | poza pokazem: nadwyżka K1 (R1-09) |
| A-62 | 1 | Podpis blisko ilustracji, gdy jest niezbędny do zrozumienia obrazu; gdy tylko dokumentacyjny, bliskość … | figcaption przy obrazie | poza pokazem: nadwyżka K1 (R1-09) |
| A-63 | 1 | W sieci reguły, ramki, nakładki i bloki koloru łączą obraz z podpisem w jedną całość. | ramka i blok koloru łączą obraz z podpisem | poza pokazem: nadwyżka K1 (R1-09) |
| A-64 | 1 | Strona tytułowa wyraża godność tekstu: kilka linii u góry i u dołu, wyważona pustka między nimi; nie … | układ strony tytułowej (grid, pustka) | poza pokazem: nadwyżka K1 (R1-08) |
| A-65 | 1 | Tytuły nie przytłaczają tekstu: wystarczą spacjowane kapitaliki w rozmiarze i wadze tekstu; większe … | tytuł w wadze i rozmiarze tekstu, kapitaliki spacjowane | P1-05 |
| A-66 | 1 | Wyśrodkowanie jest tradycyjną formą stron tytułowych, zaproszeń, certyfikatów i tytułów. | text-align: center i text-wrap: balance | P1-10 |
| A-67 | 1 | Początek rozdziału kształtuj tak, by przyczyniał się do całości projektu: renesans bez dodatkowej pustej … | początek rozdziału | poza pokazem: dubluje P1-17 i P1-05 |
| A-68 | 1 | Spis treści: dwie kolumny (tytuł, numer) zestawione blisko siebie, bez dot leaders i dużych luk; pełny … | spis treści w dwóch kolumnach grid | poza pokazem: nadwyżka K1 (R1-08) |
| A-69 | 3 | Przed tekstem półtytuł (half-title); po tekście pusta karta lub strona; dedykacja nie wciśnięta na … | Niemożliwe: brak kart i sygnatur. Przybliżenie: brak | poza pokazem: niemożliwe |
| A-70 | 3 | Zrównoważ front i back matter z tekstem (spis, listy ilustracji, podziękowania, przedmowa wobec … | Niemożliwe: brak objętości stronicowej. Przybliżenie: proporcjonalne sekcje | poza pokazem: niemożliwe |
| A-71 | 1 | Każda warstwa tekstu (tytuł rozdziału, nagłówki, cytaty, przypisy, listy) ma własną tożsamość … | osobny styl dla każdej warstwy (@layer) | P1-24 |
| A-72 | 1 | Używaj tylu poziomów nagłówków, ile potrzeba, nie więcej i nie mniej; poziomy oznaczaj A–F. | poziomy h1–h6 i liczniki; generator K2 w P2-21 | P1-24 |
| A-73 | 1 | Wybierz dominującą formę nagłówków: symetryczną (crossheads) albo asymetryczną (sideheads); losowe … | dominująca forma nagłówków (K-09) | P1-24 |
| A-74 | 1 | Nagłówek jednowierszowy wyrównany do prawej wymaga dużego rozmiaru lub wagi; nagłówki można wynieść w … | nagłówek w prawo wymaga wagi lub wielkości | P1-24 |
| A-75 | 1 | Każdy poziom hierarchii sygnalizują jeden lub kilka sygnałów: przestrzenne (wcięcie, interlinia … | do trzech sygnałów na poziom (K-07) | P1-24 |
| A-76 | 1 | Redundancja sygnałów bywa pożądana (wcięcie + łamanie wiersza), ale zbyt wiele sygnałów (wcięcie + … | redundancja sygnałów w mierze | P1-24 |
| A-77 | 1 | Hierarchia jest relacyjna: nagłówek, podtytuły i tekst odróżniają się wzajemnie; wyraźny kontrast skali … | kontrast skali i relacje poziomów | P1-04 |
| A-78 | 1 | Mieszanie wyrównań (flush left, flush right, justowanie, wyśrodkowanie) tworzy dynamiczne układy; w … | mieszanie wyrównań w nagłówkach | poza pokazem: odrzucona w K-09 |
| W-01 | 1 | Tabele redaguj i składaj jak tekst do czytania: nagłówki kolumn poziomo, litery nie za małe ani zbyt … | table: nagłówki poziomo, minimum linii | P1-18 |
| W-02 | 1 | Linie, tła i dzielniki biegną wzdłuż głównego kierunku czytania (w listach i indeksach pionowo, w … | linie w kierunku czytania, bez ramki zewnętrznej | P1-18 |
| W-03 | 1 | Listy porządkuj pozycją i punktowaniem (numery lub myślniki wiszące w marginesie, numery wyróżnione … | list-style-position: outside, ::marker | P1-18 |
| W-04 | 1+2 | Liczby w kolumnach wyrównuj do prawej lub do separatora dziesiętnego; odnośniki do liczb wieszaj po … | K1: tabular-nums i text-align: right; K2: wyrównanie do przecinka | P1-18; P2-19 |
| W-05 | 1 | Wyrównania w tabelach: pary (spis treści) — lewa kolumna flush right, prawa flush left; tabele finansowe … | wyrównania kolumn w tabelach | P1-18 |
| W-06 | 1 | Linie i ramki mają oświetlać relacje danych, a nie zamykać każdą komórkę w „więzieniu danych”; strukturę … | bez „więzienia danych”, linie pod nagłówkiem | P1-18 |
| W-07 | 1 | Zamiast gęstych linii użyj bladego tła łączącego długie wiersze; liczby można zastąpić kropkami do … | tło zebra zamiast linii | P1-18 |
| W-08 | 1 | Tabela jest strukturą danych (kolumny i wiersze), nie narzędziem układu strony; układ musi mieć sens po … | semantyka table w HTML | poza pokazem: właściwość kodu |
| W-09 | 3 | „Kolor” strony to gęstość czerni, zależna od kroju, odstępów liter, wyrazów i linii (wszystkie … | Niemożliwe: równość „koloru” ocenia oko po wydruku. Przybliżenie: detektor ragu i pomiar gęstości | poza pokazem: niemożliwe (P2-22 przybliża) |
| W-10 | 1 | Drugi kolor (czerwień) służy fleuronom, inicjałom, wersalom i żywej paginie. | drugi kolor akcentu | poza pokazem: nadwyżka K1 (R1-05) |
| W-11 | 1 | Duże litery o lekkim kolorze uzyskaj kolorem lub rastrem (tint, screening), a nie ciężarem kroju. | lekki kolor dużych liter | poza pokazem: nadwyżka K1 (R1-05) |
| W-12 | 1 | Odcień czerni dobieraj do papieru (czerwieńsza na kremowym, bliższa niebieskiej na szarym lub białym) … | czerń tekstu dobrana do tła (zmienne, light-dark) | poza pokazem: nadwyżka K1 (R1-05) |
| W-13 | 1 | Ostry czarny tekst na białym tle czyta się z ekranu równie sprawnie jak z papieru. | kontrast tekstu do tła | poza pokazem: nadwyżka K1 (R1-05) |
| W-14 | 3 | Krój dobieraj do technologii, dla której powstał (letterpress, offset, ekran): cienkie kreski w offsecie … | Niemożliwe: letterpress/offset to technologia druku. Przybliżenie: text-rendering i dobór fontu | poza pokazem: niemożliwe |
| W-15 | 3 | Krój dobieraj do końcowych warunków druku i rozdzielczości: delikatne kroje przepadają, a mocne szeryfy … | Niemożliwe: rozdzielczość druku. Przybliżenie: mocne kroje dla ekranu | poza pokazem: niemożliwe |
| W-16 | 3 | Krój i papier dobieraj do siebie: renesansowe i barokowe kroje do papieru szorstkiego, neoklasyczne do … | Niemożliwe: papier. Przybliżenie: kolor tła strony | poza pokazem: niemożliwe |
| W-17 | 3 | Marginesy oblicza się po wyborze oprawy; zmiana formatu o 1/8 cala niszczy dokładnie wymierzoną stronę. | Niemożliwe: oprawa i trim. Przybliżenie: brak | poza pokazem: niemożliwe |
| W-18 | 3 | Sprawdzaj skład na każdym etapie (odbitka, film, płyta): kolor, ostrość i spójność liter; kontroluj … | Niemożliwe: etapy druku. Przybliżenie: automatyczne kontrole w buildzie | poza pokazem: niemożliwe |
| W-19 | 3 | Format publikacji wynika z arkusza: 2:3 i 3:4 (średniowieczne arkusze, USA), 1:√2 (ISO); wymiary spoza … | Niemożliwe: arkusz papieru. Przybliżenie: aspect-ratio (P1-20) | poza pokazem: niemożliwe (przybliżenie w P1-20) |
| W-20 | 3 | Węższe strony wymagają miękkiego grzbietu; przy małych rozmiarach nadają się tylko do tekstu o wąskiej … | Niemożliwe: grzbiet. Przybliżenie: brak | poza pokazem: niemożliwe |
| W-21 | 1 | Dobieraj krój o skojarzeniach historycznych zgodnych z tekstem (renesans do renesansu); unikaj … | dobór kroju do epoki tekstu | poza pokazem: decyzja o doborze kroju |
| W-22 | 1 | Pozwól krojowi mówić jego idiomem: krój renesansowy żąda renesansowych proporcji strony i marginesów … | idiom epoki: proporcje i marginesy | poza pokazem: dubluje P1-19 i P1-20 |
| W-23 | 1 | Krój dobieraj według pochodzenia i charakteru (kraj, epoka, wyznanie, płeć projektanta), nie według … | dobór kroju wg pochodzenia | poza pokazem: decyzja o doborze kroju |
| W-24 | 1 | Cechy stylów: renesans — oś humanistyczna, umiarkowany kontrast, mała wysokość x; neoklasycyzm — oś … | cechy stylów epok | poza pokazem: wiedza o krojach, nie efekt |
| W-25 | 1 | Klasyfikacja krojów: humanistyczne (old style), przejściowe, nowoczesne (Bodoni, Didot), egipskie … | klasyfikacja krojów | poza pokazem: wiedza o krojach |
| W-26 | 3 | Subtelna, niemal niedostrzegalna wariacja glifów (alternatywy kontekstowe wbudowane w font) ożywia … | Niemożliwe: losowa wariacja glifów nie ma natywnego odpowiednika. Przybliżenie: font-variant-alternates i calt | poza pokazem: niemożliwe |
| W-27 | 1 | Jeśli tekst czyta się z ekranu, projektuj dla ekranu: rozmiar, miara, interlinia, kształt wirtualnej … | projekt pod ekran | poza pokazem: zasada ogólna realizowana w całym demo |
| W-28 | 1 | Dobre kroje ekranowe: niski kontrast, duży korpus (wysokość x), otwarte kontrzłobki, mocne zakończenia … | kroje ekranowe o dużym x-height | poza pokazem: decyzja o doborze kroju |
| W-29 | 3 | Jeśli font źle wygląda w niskiej rozdzielczości, sprawdź hinting; silny antyaliasing rozmywa bardzo małe … | Niemożliwe: hinting jest w foncie, silnik renderuje po swojemu. Przybliżenie: text-rendering | poza pokazem: niemożliwe |
| W-30 | 1 | Bitmapowy font pikselowy używaj w rozmiarze rdzeniowym lub w jego całkowitych wielokrotnościach (9 → 18 … | fonty pikselowe w wielokrotnościach rozmiaru | poza pokazem: demo bez fontu pikselowego |
| W-31 | 1 | @font-face wolno używać tylko dla krojów licencjonowanych do osadzania w sieci. | licencja przy @font-face | poza pokazem: kwestia prawna |
| W-32 | 1 | Na ekranie przypisy, indeksy i nadpisy giną; zastępują je odsyłacze hipertekstu; wszystkie podteksty … | przypisy jako odsyłacze lub popover | poza pokazem: UX, nie typografia |
| W-33 | 1 | Czytelnik w sieci skanuje, a nie czyta; ikony nie zastępują tekstu, bo wymagają objaśnienia w wielu … | tekst zamiast ikon | poza pokazem: UX |
| W-34 | 1 | W sieci myśl w stylach systemowo i globalnie: formę i treść oddziel (arkusze stylów), by treść można … | oddzielenie treści od stylu (@layer) | poza pokazem: architektura demo |
| W-35 | 1 | Style nazywaj strukturalnie (tytuł, podtytuł, podpis), nie wizualnie; w HTML em, strong i p są … | semantyczne style, jeden h1 | poza pokazem: właściwość kodu |
| W-36 | 1 | Źródło HTML czytane liniowo ma sens i jest zbliżone do kolejności wizualnej; kotwica „przejdź do treści” … | kolejność źródła i skip link | poza pokazem: właściwość kodu |
| W-37 | 1 | Nie używaj tabel do układu strony; układ liniowy ułatwia czytniki ekranu, urządzenia mobilne i … | brak tabel układu | poza pokazem: właściwość kodu |
| W-38 | 1 | Ten sam HTML może mieć różne arkusze stylów dla różnych urządzeń (układ komputerowy i mobilny). | jeden HTML, różne arkusze | poza pokazem: architektura |
| W-39 | 1 | Mikrodane (tytuł strony, słowa kluczowe, teksty alt) umożliwiają przeszukiwanie, indeksowanie i … | mikrodane | poza pokazem: SEO, nie wygląd |
| W-40 | 1 | Przed modyfikacją fontu sprawdź licencję (EULA); bez zgody nie zmieniaj i nie dystrybuuj; legalnym … | licencja fontu | poza pokazem: kwestia prawna |
| W-41 | 2 | Nie poprawiaj w foncie tego, co nie jest zepsute; poprawki wykonaj raz, na stałe, w foncie, nie ręcznie … | poprawka fontu w buildzie (fonttools) | poza pokazem: etap budowania, nieprzełączalny |
| W-42 | 2 | Stale potrzebne glify (cyfry tekstowe, ligatury ff, ffi, ffl, fj, pionowe nawiasy w italic) trzymaj w … | scalenie glifów w foncie bazowym (fonttools) | poza pokazem: etap budowania |
| W-43 | 2 | Brakujące glify (litery wschodnioeuropejskie itp.) dorób; opisz je nazwą PostScript i numerem Unicode. | dorobienie glifów (fonttools) | poza pokazem: etap budowania |
| W-44 | 2 | Napraw wadliwe glify pomocnicze (znaki + ± × = • – — © @) zbyt duże, jasne, wysoko lub nisko osadzone, i … | naprawa glifów pomocniczych (fonttools) | poza pokazem: etap budowania |
| W-45 | 2 | Tablicę kerningu sprawdzaj plikiem testowym (nazwy własne, diakrytyki, cudzysłowy, nawiasy, ułamki) … | plik testowy kerningu (hb-shape) | poza pokazem: etap budowania |
| W-46 | 2 | Odstęp po f przed spacją nie może mieć 1/8–1/4 em (błąd kerningu w wielu fontach); spacja słowna … | poprawa kerningu spacji (fonttools) | poza pokazem: etap budowania |
| W-47 | 1 | Funkcje OpenType działają tylko, gdy oprogramowanie je obsługuje; sprawdź, co font faktycznie zawiera … | font-feature-settings i obsługa funkcji | poza pokazem: dubluje P1-06–P1-08 |
| W-48 | 1 | Rodzina fontu: nazwy rodziny i stylów zgodne, aby roman, italic i bold były powiązane i przełączały się … | @font-face: jedna rodzina i style | poza pokazem: decyzja o doborze kroju |
| W-49 | 1 | Darmowe fonty bywają źle rozstawione i niekompletne; wiele jest pirackich; niektóre darmowe są rzetelne … | informacja o fontach darmowych | poza pokazem: informacja |
| W-50 | 1 | Dobry font to nie tylko kształty liter, lecz także poprawne wyrównanie glifów, spójne rozmiary, dokładne … | jakość fontu | poza pokazem: informacja |
| W-51 | 1 | Ornamenty (fleurony, linie dekoracyjne) flagują początki tekstu i rozdzielają bloki; w wcięciach … | ::before z ozdobnikiem | poza pokazem: nadwyżka K1 (R1-06) |
| W-52 | 1 | Ornament wynika ze struktury (echo struktury): moduły ornamentu składają się w większe formy według … | ornament z siatki | poza pokazem: nadwyżka K1 (R1-06) |
| W-53 | 1 | Tekst pionowy: obróć linię zamiast układać litery jedna pod drugą; stos wersalików jest stabilniejszy … | writing-mode i text-orientation | poza pokazem: nadwyżka K1 (R1-07) |
| W-54 | 1 | Odstępy, rozmiar i położenie liter mogą wyrażać znaczenie słowa (ekspresja przestrzenna) w tytułach … | ekspresja przestrzenna | poza pokazem: nie jest regułą normatywną |
| W-55 | 1 | Logotypy, nazwy marek i prośby autorów o szczególne traktowanie liter nie zmieniają zasad składu … | tekst bez wyjątków dla logotypów | poza pokazem: stanowisko |
| W-56 | 2 | Przed składem oczyść tekst: usuń podwójne spacje, zamień proste cudzysłowy na typograficzne, a podwójne … | czyszczenie tekstu (Typograf common/space) | P2-23 |
| W-57 | 1 | Brak silnej koncepcji maskują ozdobniki (gradienty, cienie, przezroczystość); pomysł prowadzi decyzje o … | ograniczenie dekoracji strony (bez gradientów, cieni) | poza pokazem: wymóg dla strony zasady.html |

## 6. Punkty pokazu: kategoria 1 (CSS i HTML)

| ID | Punkt | Zasady | Technika | Wsparcie (Chrome / Safari / Firefox) | Fallback | Uwagi |
|---|---|---|---|---|---|---|
| P1-01 | Miara w znakach (66 ch) | M-01, M-03, M-04 | `max-inline-size: min(66ch, 100%)` | ch: 27 / 7 / 1 | `max-width` w em (ok. 30em) | Najprostszy punkt; łączy się z P1-02. |
| P1-02 | Interlinia zależna od miary i kroju | M-07, M-08 | `line-height` bezwymiarowe; wartość ze zmiennej CSS rosnąca z miarą | wszystkie | n/d | Ujemna tylko w nagłówkach. |
| P1-03 | Rytm pionowy na siatce 8 px | M-09, M-10, M-11, A-30, A-31, A-57 | `--u: 8px`; `line-height: calc(var(--u) * 3)`; odstępy `calc(var(--u) * n)`; `lh`, `rlh` | lh: 109 / 16.4 / 120; rlh: 111 / 16.4 / 120 | same zmienne `--u` (działają wszędzie) | Nakładka siatki: `repeating-linear-gradient` lub SVG; zakaz gradientów dotyczy strony zasady.html, nie nakładki. |
| P1-04 | Skala rozmiarów i kontrast poziomów | M-16, M-17, M-18, M-19, M-20, A-77 | zmienne CSS + `clamp()` | clamp: 79 / 13.1 / 75 | stałe rozmiary w rem | Skale: Fibonacci, Le Corbusier, dwie proporcje. |
| P1-05 | Jeden parametr na raz i waga przy rozmiarze | M-21, M-22, M-30, M-125, A-65 | `font-weight` malejące z rozmiarem; `em`/`strong` jako jedyny sygnał; hierarchia odmian | wszystkie | n/d | Rozstrzygnięcie K-07. |
| P1-06 | Prawdziwe kapitaliki, spacjowanie wersalików | M-14, M-44, M-45, M-46, M-47, M-120, M-121 | `font-variant-caps: small-caps / all-small-caps`; `font-synthesis-small-caps: none`; `letter-spacing: .05–.1em`; `font-feature-settings: "case"` | font-variant-caps: 52 / 9.1 / 34; font-synthesis-small-caps: 97 / 16.4 / 111 | `font-feature-settings: "smcp","c2sc"`; bez fontu z kapitalikami zwykłe litery (nie fałszować) | Wymaga fontu z kapitalikami. |
| P1-07 | Ligatury | M-48, M-50, M-51, M-52 | `font-variant-ligatures: common-ligatures | discretionary-ligatures | none` | 34 / 9.1 / 34 | `font-feature-settings: "liga","dlig"` | Przy `letter-spacing ≠ 0` ligatury wyłączane z mocy specyfikacji. |
| P1-08 | Cyfry tekstowe i tabelaryczne, ułamki, indeksy | M-54, M-55, M-58, M-61 | `font-variant-numeric: oldstyle-nums | lining-nums | tabular-nums | diagonal-fractions`; `font-variant-position: sub | super` | numeric: 52 / 9.1 / 34; position: 117 / 9.1 / 34 | `font-feature-settings: "onum","tnum","frac","sups"`; element `sup` | Wymaga fontu z odpowiednimi funkcjami. |
| P1-09 | Kerning i odstęp międzywyrazowy | M-56, M-78, M-116, M-118, M-123 | `font-kerning: normal`; `text-rendering: optimizeLegibility`; `word-spacing`, `letter-spacing` w nagłówkach | font-kerning: 33 / 9 / 32 | n/d | Kerning optyczny: niedostępny (K3, M-118). |
| P1-10 | Balans wierszy nagłówków i tekstu wyśrodkowanego | M-70, A-66 | `text-wrap: balance` | 114 / 17.5 / 121 | ręczne `<br>` i miara w ch; bez wsparcia zwykłe łamanie | Limit wierszy: kilka (Chrome 6, Firefox 10; do sprawdzenia). |
| P1-11 | Ładne łamanie akapitu | M-68, M-80 | `text-wrap: pretty` | 117 / 26 / brak | P2-12 (wiązanie ostatnich wyrazów) | Firefox: brak wsparcia. |
| P1-12 | Dzielenie wyrazów w przeglądarce | M-79, M-83 | `hyphens: auto` + `lang="pl"`; `hyphenate-limit-chars: 5 2 3`; `hyphenate-character` | hyphens: 88 (55 macOS) / 17 / 6; limit-chars: 109 / preview / 137 | P2-13 (Hyphenopoly) lub `&shy;` | Słownik polski w przeglądarce: do sprawdzenia (headless Chromium 156 nie dzielił polskiego tekstu). |
| P1-13 | Ragged czy justowanie, dzielenie warunkowe | M-05, M-66, M-67, M-73, M-86, M-87 | `text-align: left | justify`; `text-justify: inter-word`; `hyphens: manual`; `&shy;`; `@container (min-width: 40ch)` | text-justify: 145 / brak / 55; @container: 105 / 16 / 110 | justowanie tylko w szerokim kontenerze; domyślnie left | Twardy rag: `hyphens: manual`, bez `letter-spacing`. |
| P1-14 | Wiszące znaki interpunkcyjne | M-74, M-135 | `hanging-punctuation: first last` | brak / 26.5 (częściowo od 10) / brak | P2-15 (JS) lub `text-indent` ujemny w klasie | Tylko Safari; Chrome i Firefox nie wspierają. |
| P1-15 | Wcięcia akapitów | M-128, M-129, M-130 | `:is(h1,h2,h3,h4,h5,h6,hr,figure) + p { text-indent: 0 }`; `p + p { text-indent: 1em }`; bez odstępu (K-02) | :is(): 88 / 14 / 78 | lista selektorów bez `:is()` | Rozstrzygnięcie K-02. |
| P1-16 | Cytaty blokowe i wierszowane | M-75, M-133, M-134 | `blockquote` (italic lub rozmiar lub wcięcie); wiersze: `width: fit-content; margin-inline: auto; text-align: left` | fit-content: 46 / 11 / 94; margin-inline: 87 / 14.1 / 66 | `display: table` zamiast fit-content | Cytat w rytmie siatki (P1-03). |
| P1-17 | Inicjał i otwarcie akapitu | M-136, M-137, M-138, M-139, M-140 | `initial-letter` (+ `::first-letter`), `::first-line` w kapitalikach; `shape-outside`; jednostka `cap` | initial-letter: 110 / 9 (-webkit-) / brak; shape-outside: 37 / 10.1 / 62; cap: 118 / 17.2 / 97 | `float: left` i `font-size` na `::first-letter` | Firefox bez `initial-letter`. |
| P1-18 | Tabele i listy | M-109, W-01, W-02, W-03, W-04, W-05, W-06, W-07 | `font-variant-numeric: tabular-nums`; `text-align: right`; `::marker`; `list-style-position: outside`; zebra `:nth-child`; brak ramek | ::marker: 86 / 11.1 (część.) / 68 | numery ręcznie wiszące (`position`) | Dane: gęstość (K-04). |
| P1-19 | Kanon strony i marginesy (Villard, Aldus) | A-01, A-04, A-13, A-14, A-15, A-16, A-20, A-22, A-23 | `aspect-ratio: 2 / 3`; marginesy w % szerokości (np. s = 11,11%, t = 16,67%, e = 22,22%, f = 33,33%) | aspect-ratio: 88 / 15 / 89 | `padding-top` w % (hack) lub stała wysokość | Procenty marginesów liczone od szerokości kontenera; nakładka kanonu. |
| P1-20 | Proporcje strony i pola składu (złoty podział, ISO) | A-02, A-03, A-05, A-06, A-10, A-11, A-12, A-17, A-18, A-19 | `aspect-ratio` strony i pola; marginesy 1/9 i 2/9 w %; przełącznik kanonu | aspect-ratio: 88 / 15 / 89 | j.w. | Alternatywa wobec P1-19: blokada jednoczesnego wyboru. |
| P1-21 | Siatka kolumnowa i modułowa z nakładką | A-26, A-27, A-28, A-29, A-32, A-33, A-34, A-43 | `display: grid`; `grid-template-columns/rows`; `subgrid`; `grid-column: 1 / -1` | grid: 57 / 10.1 / 52; subgrid: 117 / 16 / 71 | grid bez `subgrid` (ręczne wyrównanie) | Nakładka: SVG lub pseudoelement. |
| P1-22 | Kolumny, marginalia i przypisy boczne | M-02, M-69, M-88, M-89, M-92, M-141, M-142, M-144, A-38, A-39, A-40, A-41, A-51, A-52 | `column-width`, `column-gap`, `column-rule`; `break-inside/after: avoid`; `widows: 2`; przypisy boczne: `anchor-name` + `position-anchor` + `position-area` | multicol: 50 / 9 / 52; break: 50 / 10 / 65; widows/orphans: 25 / 1.3 / brak; anchor: 125–151 / 26–27 / 147–151 | przypisy: `float` + ujemny margines (Tufte); K2 w P2-18 | Anchor positioning pełne w bieżących wersjach (Chrome 155, Safari 27, Firefox 157). |
| P1-23 | Rozkładówka (przybliżenie) | A-44, A-45 | dwa kontenery obok siebie (grid), lustrzane marginesy `margin-inline`, `@container` ≥ szerokość dwóch stron | grid, container queries | jedna strona poniżej progu | Przybliżenie, nie rozkładówka (patrz K3: A-44, A-46, A-47). |
| P1-24 | Hierarchia nagłówków | A-71, A-72, A-73, A-74, A-75, A-76 | h1–h6, `@layer`, zmienne; do trzech sygnałów na poziom; jedna dominująca forma nagłówków | @layer: 99 / 15.4 / 97 | style bez `@layer` | Rozstrzygnięcia K-07 i K-09. |

## 7. Punkty pokazu: kategoria 2 (JS, biblioteki, build)

| ID | Punkt | Zasady | Rozwiązanie i wymagania | Waga | Poziom kosztu | Koszt i ryzyka (wydajność, dostępność, regresje) | Kiedy się opłaca |
|---|---|---|---|---|:--:|---|---|
| P2-01 | Spójniki jednoliterowe niełamliwe | M-114 | Typograf `common/nbsp/afterShortWord` z `lengthShortWord: 1` albo regex; przejście po węzłach tekstowych | Typograf 7.8.0 (64 kB min, ok. 20 kB gz) lub własny kod ok. 0,3 kB | niski | Waga ok. 0 przy własnym kodzie. Dostępność: U+00A0 czytane jak spacja. Regresje: przy wąskich kolumnach dłuższe niełamliwe ciągi; kopiowanie wkleja nbsp. | Zawsze; najlepiej w buildzie (zero kosztu w przeglądarce). W CMS: skrypt po stronie serwera. |
| P2-02 | Cudzysłowy typograficzne i apostrof | M-103, M-104 | Typograf `common/punctuation/quote` z locale `pl` (zewnętrzne „…”, wewnętrzne «…») i `common/punctuation/apostrophe` | Typograf 7.8.0 | niski | Zagnieżdżone cudzysłowy i apostrofy w skrótach wymagają testu; cudzysłowy w atrybutach HTML nie mogą być ruszane (Typograf pomija znaczniki). | Zawsze; w buildzie. |
| P2-03 | Pauza we wtrąceniach i półpauza | M-94, M-96 | własne regexy (Typograf nie ma reguły myślnika dla pl): „ - ”, „ -- ”, „ — ” → „ – ”; rozstrzygnięcie K-01 | własny kod ok. 0,2 kB | niski | Nie ruszać łączników w złożeniach (polsko-niemiecki) i znaków minus; ryzyko fałszywych trafień w kodzie i adresach. | Zawsze, razem z P2-04. |
| P2-04 | Półpauza w zakresach | M-63 | regex `\d+\s?[-–—]\s?\d+` → półpauza bez spacji, z wyłączeniem dat ISO i numerów | własny kod ok. 0,3 kB | niski | Fałszywe trafienia: daty 2026-10-11, numery telefonów, identyfikatory; potrzebna lista wyjątków. | Zawsze, jako reguła redakcyjna w buildzie. |
| P2-05 | Wielokropek i interpunkcja notacyjna | M-100, M-101 | Typograf `common/punctuation/hellip`, `delDoublePunctuation`; własne !!! → ! | Typograf 7.8.0 | niski | Zmiana intencji autora (ekspresja) — Bringhurst 5.2.8 uzasadnia. | Zawsze. |
| P2-06 | Znaki ×, −, ±, ≠ i ułamki ½ ¼ ¾ | M-61, M-62 | Typograf `common/number/times`, `mathSigns`, `fraction` | Typograf 7.8.0 | niski | Fałszywe trafienia: „x” w innym znaczeniu, daty 1/2; potrzebna biała lista kontekstów. | Zawsze. |
| P2-07 | Stopień, prime i znaki prawne | M-65, M-110 | Typograf `common/symbols/cf`, `common/symbols/copy`; prime (′ ″) własny regex | Typograf 7.8.0 | niski | Odróżnianie cali od cudzysłowów prostych. | Gdy tekst ma jednostki lub znaki prawne. |
| P2-08 | Twarde spacje: liczby, jednostki, skróty | M-113 | Typograf `common/nbsp/afterNumber`, `afterSectionMark`; własna lista polskich skrótów (str., rozdz., ul., r., tys., zł) | Typograf 7.8.0 + lista ok. 0,5 kB | średni | Kompletność listy skrótów; konflikt z wąskimi kolumnami (niełamliwe ciągi). | Zawsze; lista skrótów utrzymywana w repozytorium. |
| P2-09 | Grupowanie cyfr i numery telefonów | M-59, M-60 | `Intl.NumberFormat("pl-PL")` lub Typograf `common/number/digitGrouping`; wzorzec numerów 3-3-3; twarda cienka spacja | Intl (C24 / S10 / F29) lub Typograf | niski | `pl-PL` w Intl nie grupuje liczb czterocyfrowych (do sprawdzenia); trzeba własnych reguł. | Przy danych liczbowych, cenach, telefonach. |
| P2-10 | Akronimy w kapitalikach | M-41, M-42, M-43 | TreeWalker po węzłach tekstu + regex wersalików (≥ 2 litery) → `<abbr>`; `font-variant-caps: all-small-caps` | własny kod ok. 0,6 kB; font z kapitalikami | średni | Wyjątki (dwuliterowe geograficzne, inicjały osób), wersalikowe nagłówki; dodatkowe węzły DOM; sprzątanie przez przywrócenie oryginalnego HTML. | Gdy tekst ma wiele skrótów (np. NATO, UE) i font z kapitalikami. |
| P2-11 | Inicjały osobowe | M-93 | regex `([A-ZŁŚŻ])\.\s?([A-ZŁŚŻ])\.` → cienka spacja + nbsp przed nazwiskiem | własny kod ok. 0,2 kB | niski | Skróty typu „M. in.” — wyjątki. | Gdy tekst zawiera nazwiska i inicjały. |
| P2-12 | Wdowy wyrazowe w ostatnim wierszu | M-80 | nbsp między ostatnimi wyrazami akapitu, gdy ostatni wyraz < 4 litery | własny kod ok. 0,2 kB | niski | Przy bardzo wąskich kolumnach może powodować wystawanie; nakłada się na `text-wrap: pretty`. | Gdy brak `text-wrap: pretty` (Firefox). |
| P2-13 | Dzielenie wyrazów wg słownika polskiego (Hyphenopoly) | M-83 | Hyphenopoly 6.1.0: `Hyphenopoly_Loader.js` (3,2 kB), `Hyphenopoly.js` (9,3 kB), `patterns/pl.wasm` (16,5 kB); `leftmin: 2`, `rightmin: 3`, `minWordLength: 5` | razem ok. 14,6 kB gz; loader `async` | średni | Wstawia &shy; w DOM (kopiowanie, wyszukiwanie, czytniki ekranu: do sprawdzenia); FOUT bez ukrycia do czasu załadowania; nie ogranicza liczby kolejnych dzieleń; przywracanie tekstu z kopii. | Długi, justowany tekst ciągły, gdy słownik przeglądarki zawodzi (np. Chrome bez pobranego słownika). |
| P2-14 | Justowanie paragrafowe Knutha–Plassa | M-71 | tex-linebreak 0.9.0 (`dist/lib.js`, 16,7 kB); wzorce dzielenia w pakiecie tylko en-us, polskie trzeba dostarczyć (np. z Hyphenopoly) | tex-linebreak 0.9.0 (+ wzorce pl) | wysoki | Mierzy tekst i ustawia odstępy w każdym wierszu; słaba obsługa złożonego inline; przeliczanie przy resize; nie działa z P2-13 bez wspólnego silnika; do sprawdzenia: bundlowanie (UMD z CDN). | Rzadko: jedna justowana kolumna o stałej szerokości; rozstrzygnięcie K-06. |
| P2-15 | Wiszące znaki: zamiennik JS | M-74, M-135 | pomiar szerokości glifu (`canvas.measureText`), pierwszy znak w `span` z ujemnym `margin-inline-start`; aktualizacja po `document.fonts.ready` | własny kod ok. 0,5 kB | średni | Tylko akapity zaczynające się od cudzysłowu lub nawiasu; przy zmianie fontu trzeba przeliczać. | Gdy wymagane na Chrome i Firefox (brak `hanging-punctuation`). |
| P2-16 | Miernik miary (znaki w wierszu) | M-06 | `Range.getClientRects` + `Intl.Segmenter`/długość tekstu; nakładka z liczbą znaków; wzór z długości alfabetu (`canvas.measureText`) | własny kod ok. 0,8 kB | niski | Narzędzie diagnostyczne, nie zmienia typografii; zależy od rozpoznania linii. | QA w trakcie projektowania. |
| P2-17 | Przyciąganie do siatki bazowej (obrazy, ramki) | M-09, M-11, A-57 | `ResizeObserver` dopełnia wysokość do wielokrotności jednostki (`margin-block-end`) | własny kod ok. 0,6 kB | średni | Pętle layoutu, zmiana wysokości po załadowaniu obrazów (CLS); zapobiegać `aspect-ratio`. | Gdy w tekście są obrazy lub ramki o dowolnej wysokości. |
| P2-18 | Przypisy: numeracja i rozmieszczenie bez kolizji | M-141, M-143 | JS numeruje odsyłacze, układa przypisy boczne w kolumnie marginesu tak, by się nie zachodziły; alternatywa CSS: anchor positioning z `position-try-fallbacks` | własny kod ok. 1 kB | średni | Kolizje między przypisami wymagają JS; dostępność: `role="note"`, powiązanie `aria-describedby`; na wąskich ekranach zwijanie do popovera. | Gdy przypisów boczne jest wiele i leżą blisko siebie. |
| P2-19 | Wyrównanie do separatora dziesiętnego | W-04 | JS dzieli liczby w komórce na część całkowitą i ułamkową (spany) i wyrównuje je; alternatywa K1: stała liczba miejsc + `tabular-nums` | własny kod ok. 0,5 kB | średni | Brak natywnego `text-align` do znaku; dostępność: tekst się nie zmienia, spany tylko stylistyczne. | Tabele z liczbami o różnej liczbie miejsc po przecinku. |
| P2-20 | Bieżąca żywa pagina i numer sekcji (przybliżenie folio) | A-48, A-49, A-50 | `IntersectionObserver` + `position: sticky`; K3: brak numeru strony | własny kod ok. 0,4 kB | niski | Duplikat tekstu: `aria-hidden`; alternatywa K1: scroll-driven animations (Chrome 115, Safari 26, Firefox preview). | Długie dokumenty z podziałem na sekcje. |
| P2-21 | Spis treści generowany z nagłówków | A-53 | JS buduje listę z `h2`–`h3` o `id`; numeracja; progresywne ulepszenie | własny kod ok. 0,5 kB | niski | Bez JS brak spisu (lepiej w buildzie); powiązanie z A-68. | Zawsze jako krok build lub CMS. |
| P2-22 | Detektor złego ragu | M-68 | `Range.getClientRects` → szerokości wierszy; wykrywanie klina i trampoliny (≥ 4 kolejne wiersze rosnące lub malejące) | własny kod ok. 0,8 kB | średni | Narzędzie QA; parametry progów dobiera się empirycznie. | Przy przeglądzie składu tekstu ragged. |
| P2-23 | Czyszczenie tekstu przed składem | M-149, W-56 | Typograf `common/space/*` (podwójne spacje, spacje przed interpunkcją), `common/html/*`; lint znaków bez funkcji typograficznej | Typograf 7.8.0 | niski | Nie stosować w `<pre>`, `<code>`; dostosować do tekstu źródłowego. | Zawsze w buildzie. |
| P2-24 | Pokrycie glifów (diagnostyka fontu) | M-25, M-146 | opentype.js 2.0.0 (`dist/opentype.min.js`, 245 kB min) i `charToGlyphIndex` dla polskich liter i znaków typograficznych; w buildzie subsetting (pyftsubset, subset-font 2.9.0) | opentype.js 2.0.0 | średni | Duża waga biblioteki jak na jedno sprawdzenie; lepiej w buildzie; wymaga dostępu do pliku fontu. | QA przy zmianie fontu; nie w produkcji. |

Elementy kategorii 2 poza pokazem: **subsetting i poprawki fontów** (W-41 – W-46; pyftsubset, glyphhanger 6.0.0, subset-font 2.9.0): to etap builda, efekt jest wagowy, a nie przełączalny na żywo. **Paged.js 0.4.3** (folio i żywa pagina na prawdziwych stronach, wdowy i sieroty): ok. 5,9 MB w pakiecie, nieodwracalnie przebudowuje DOM, nie da się wyłączyć bez przeładowania i koliduje z pozostałymi skryptami. **Wykrywanie powtórzeń na początkach wierszy** (M-84): brak algorytmu naprawczego. **Ograniczenie kolejnych dzieleń** (M-81): wysoki koszt, brak uniwersalnego CSS (`hyphenate-limit-lines` tylko Safari preview).

## 8. Kategoria 3: niemożliwe w sieci i najbliższe przybliżenia

| ID | Zasada (skrót) | Dlaczego niemożliwe i najbliższe przybliżenie |
|---|---|---|
| M-12 | Linie tekstu na obu stronach kartki oraz na obu stronach rozkładówki leżą na wspólnych … | Niemożliwe: brak dwustronnego druku i kartek. Przybliżenie: jedna siatka bazowa dla wszystkich kolumn i obu stron „rozkładówki” |
| M-13 | Strona nie może dusić tekstu: 30–45 wierszy na stronie książki przy 60–66 znakach … | Niemożliwe: nie ma strony o stałej liczbie wierszy. Przybliżenie: miara i interlinia dobrane jak dla strony, kolumny przez @container |
| M-14 | Całe wiersze wersalików mogą mieć ciaśniejszą interlinię (brak ascenderów i descenderów) … | K1: osobny line-height dla bloków samych wersalików; K3: ręczna korekta linii bazowej w mieszanych stosach |
| M-88 | Nigdy nie zaczynaj strony ostatnim wierszem wielowierszowego akapitu („wdowa” u … | K1: widows: 2 w układzie kolumnowym; K3: w przewijanym tekście brak stron |
| M-89 | Samotny pierwszy wiersz akapitu na dole strony („sierota” u Bringhursta: ma przyszłość … | K1: orphans: 2 w układzie kolumnowym; K3: w przewijanym tekście brak stron |
| M-90 | Wyrównuj głębokość rozkładówki przez przenoszenie pojedynczych wierszy z poprzednich lub … | Niemożliwe: brak rozkładówek i stron. Przybliżenie: column-fill: balance wyrównuje kolumny |
| M-91 | Pozostawiony na ostatniej stronie rozdziału kilkuwierszowy ogon: rozciągnij kilka … | Niemożliwe: brak ostatniej strony rozdziału. Przybliżenie: brak (treść przepływa) |
| M-112 | Łącznik (hyphen) ma szerokość ok. 1/4 em (czasem 1/5 em w krojach ekonomicznych), a jego … | Niemożliwe: kształt i szerokość łącznika to cecha fontu. Przybliżenie: wybór fontu o odpowiednim łączniku |
| M-117 | Kerning dostosowany do języka (apostrofy: en ’d ’m ’s; fr. ’a ’e; niem. „T), bez kolizji … | Niemożliwe: tablice kerningu języka siedzą w foncie. Przybliżenie: lang i font z kerningiem pl |
| M-118 | Kerning metryczny (tablica fontu) do tekstu, optyczny do nagłówków i krojów bez tablicy … | K1: text-rendering: optimizeLegibility, font-kerning; K3: kerning optyczny |
| M-119 | Nie rozbudowuj tablicy kerningu, by ratować źle dopasowane znaki (oo, oe); popraw … | Niemożliwe: sidebearings to edycja fontu. Przybliżenie: wybór poprawnie rozstawionego kroju |
| M-148 | Język tekstu steruje zasadami składu: cudzysłowami, dzieleniem, kerningiem apostrofów i … | K1: lang i selektory :lang(); K3: kompromisowy sidebearing znaków |
| M-153 | W nowych ortografiach nie dodawaj zbędnych znaków; dodawaj tylko wizualnie rozróżnialne … | Niemożliwe: dotyczy projektowania ortografii i fontu, nie składu. Przybliżenie: brak |
| A-44 | Książki i czasopisma projektuj jako rozkładówki: jednostką projektu jest para stron, a … | Niemożliwe: pojedyncza strona/rozkładówka nie istnieje w przewijanym dokumencie. Przybliżenie: dwie „strony” obok siebie w kontenerze |
| A-46 | Rozkładówki ciągłego tekstu mają równą głębokość; nie powinny różnić się od sąsiednich o … | Niemożliwe: brak przepływu na strony. Przybliżenie: column-fill: balance |
| A-47 | Wiersze na obu stronach rozkładówki i obu stronach kartki pokrywają się; skład sprawdza … | Niemożliwe: brak kartki i światła. Przybliżenie: wspólna siatka bazowa obu stron |
| A-48 | Folio (numer strony) w dokumentach dłuższych niż dwie strony; miejsca: (1) góra, przy … | Niemożliwe: nie ma numeru strony. Przybliżenie: numer sekcji w marginesie (JS) |
| A-49 | Folio w rozmiarze tekstu i blisko pola składu; dalej znika, wzmocnione rozprasza. | Niemożliwe: j.w. Przybliżenie: sticky w rozmiarze tekstu przy polu |
| A-69 | Przed tekstem półtytuł (half-title); po tekście pusta karta lub strona; dedykacja nie … | Niemożliwe: brak kart i sygnatur. Przybliżenie: brak |
| A-70 | Zrównoważ front i back matter z tekstem (spis, listy ilustracji, podziękowania, przedmowa … | Niemożliwe: brak objętości stronicowej. Przybliżenie: proporcjonalne sekcje |
| W-09 | „Kolor” strony to gęstość czerni, zależna od kroju, odstępów liter, wyrazów i linii … | Niemożliwe: równość „koloru” ocenia oko po wydruku. Przybliżenie: detektor ragu i pomiar gęstości |
| W-14 | Krój dobieraj do technologii, dla której powstał (letterpress, offset, ekran): cienkie … | Niemożliwe: letterpress/offset to technologia druku. Przybliżenie: text-rendering i dobór fontu |
| W-15 | Krój dobieraj do końcowych warunków druku i rozdzielczości: delikatne kroje przepadają, a … | Niemożliwe: rozdzielczość druku. Przybliżenie: mocne kroje dla ekranu |
| W-16 | Krój i papier dobieraj do siebie: renesansowe i barokowe kroje do papieru szorstkiego … | Niemożliwe: papier. Przybliżenie: kolor tła strony |
| W-17 | Marginesy oblicza się po wyborze oprawy; zmiana formatu o 1/8 cala niszczy dokładnie … | Niemożliwe: oprawa i trim. Przybliżenie: brak |
| W-18 | Sprawdzaj skład na każdym etapie (odbitka, film, płyta): kolor, ostrość i spójność liter … | Niemożliwe: etapy druku. Przybliżenie: automatyczne kontrole w buildzie |
| W-19 | Format publikacji wynika z arkusza: 2:3 i 3:4 (średniowieczne arkusze, USA), 1:√2 (ISO) … | Niemożliwe: arkusz papieru. Przybliżenie: aspect-ratio (P1-20) |
| W-20 | Węższe strony wymagają miękkiego grzbietu; przy małych rozmiarach nadają się tylko do … | Niemożliwe: grzbiet. Przybliżenie: brak |
| W-26 | Subtelna, niemal niedostrzegalna wariacja glifów (alternatywy kontekstowe wbudowane w … | Niemożliwe: losowa wariacja glifów nie ma natywnego odpowiednika. Przybliżenie: font-variant-alternates i calt |
| W-29 | Jeśli font źle wygląda w niskiej rozdzielczości, sprawdź hinting; silny antyaliasing … | Niemożliwe: hinting jest w foncie, silnik renderuje po swojemu. Przybliżenie: text-rendering |

Przybliżenia nie są tym samym co druk: rozkładówka (P1-23) to dwa kontenery obok siebie bez grzbietu i kartki; folio (P2-20) to numer sekcji, a nie strony; wdowy i sieroty działają tylko w kolumnach (P1-22).

## 9. Rezerwa kategorii 1 (poza pokazem: nadwyżka K1)

| ID | Punkt | Zasady | Technika | Wsparcie | Uwagi |
|---|---|---|---|---|---|
| R1-01 | Rozmiar optyczny (`opsz`) | M-23 | `font-optical-sizing: auto` | font-optical-sizing: 79 / 13.1 / 62 | Wymaga fontu zmiennego z osią opsz. |
| R1-02 | Dopasowanie wysokości x przy mieszaniu krojów | M-38, M-39, M-151 | `font-size-adjust: from-font` | font-size-adjust: 127 / 16.4 / 3 (wartość dla Firefoksa wg MDN, do sprawdzenia); from-font: 127 / 17 / 118 | Wymaga dwóch krojów w demo. |
| R1-03 | Brak sztucznych odmian | M-32, M-33 | `font-synthesis-weight: none; font-synthesis-style: none` | 97 / 16.4 / 111 | Efekt widać tylko przy fontach bez prawdziwych odmian. |
| R1-04 | Przypisy: superskrypt i wiszący numer | M-143 | `font-variant-position: super`; numer wiszący w liście przypisów | 117 / 9.1 / 34 | Dubluje części P1-08 i P1-22. |
| R1-05 | Kolor i kontrast tekstu, czerń do tła | W-10, W-11, W-12, W-13 | zmienne, `color-scheme`, `light-dark()` | light-dark: 123 / 17.5 / 120 | Niezwiązane z typografią znaków; dotyczy strony. |
| R1-06 | Ornament i midpoint | W-51, W-52 | `::before { content }` | wszystkie | Efekt dekoracyjny. |
| R1-07 | Tekst pionowy | W-53 | `writing-mode: vertical-rl; text-orientation: sideways` | 48 / 10.1 / 41 | Rzadki w tekście łacińskim. |
| R1-08 | Strona tytułowa i spis treści w CSS | M-115, A-64, A-68 | grid, pustka, dwie kolumny (tytuł, numer) | wszystkie | Dubluje P1-19 i P2-21. |
| R1-09 | Obrazy, podpisy i moduły | A-08, A-36, A-61, A-62, A-63 | `aspect-ratio`, `object-fit`, `figure`/`figcaption` | aspect-ratio: 88 / 15 / 89; object-fit: 32 / 10 / 36 | Demo bez obrazów. |
| R1-10 | Linia bazowa i obcięcie pola tekstu | A-35 | `text-box: trim-both cap alphabetic`; `align-items: last baseline` | text-box: 133 / 18.2 / 154 | Nowe: Firefox dopiero od wersji 154. |
| R1-11 | Podkreślenia linków | M-127 | `text-decoration-skip-ink`, `text-underline-offset` | 64 / 15.4 / 70 | Detal. |
| R1-12 | Nawiasy i ampersand z innego kroju | M-102, M-108 | `@font-face` z `unicode-range` | unicode-range: 1 / 3.1 / 36 | Wymaga dwóch krojów. |
| R1-13 | Cudzysłowy przez `<q>` i `quotes` | M-103, M-104 | `quotes: "„" "”" "«" "»"` | quotes: 11 / 9 / 1.5 | K1 odpowiednik P2-02. |
| R1-14 | Brak zniekształcania liter | M-34 | `font-stretch` na prawdziwej osi zamiast `transform: scaleX` | font-stretch: 60 / 11 / 9 | Reguła negatywna. |
| R1-15 | Akapit blokowy i znak akapitu | M-132 | `margin`, `::before { content: "¶" }` | wszystkie | Alternatywa dla wcięcia, odrzucona w K-02. |
| R1-16 | Tracking jasnego tekstu na ciemnym | M-122 | `letter-spacing` + ciemne tło | wszystkie | Wymaga ciemnego motywu. |
| R1-17 | Selektywne wyłączanie dzielenia | M-82, M-85 | `hyphens: none` dla nazw i podpisów | wszystkie z `hyphens` | Dubluje P1-12. |

## 10. Zasady poza pokazem według powodu

- **30** zasad: Nadwyżka kategorii 1 ponad X = 24 (rezerwa R1-nn, do włączenia na życzenie)
- **24** zasad: Dotyczy kodu, builda lub prawa, nie wyglądu tekstu
- **22** zasad: Niemożliwe w sieci (kategoria 3), przybliżenia w sekcji 8
- **18** zasad: Decyzja o doborze kroju lub cecha fontu, nie przełącznik
- **12** zasad: Dubluje inny punkt lub wynika z niego
- **12** zasad: Poza zakresem demo (inny język, rzadki kontekst, niski zysk, brak algorytmu)
- **11** zasad: Metoda, postawa lub informacja, nie pojedyncza reguła do przełączenia
- **6** zasad: Odrzucone lub rozstrzygnięte w konflikcie (sekcja 2)
