# Katalog zasad typograficznych (Etap 1)

Stan: Etap 1, do akceptacji. Źródła: Robert Bringhurst, *The Elements of Typographic Style* (wyd. 3., v3.0, 2004; skrót **B**) oraz Ellen Lupton, *Thinking with Type* (wyd. 2., 2010; skrót **L**). Liczba zasad: **288** (mikro 153, makro 78, własne 57).

## Legenda

- **ID** są stałe i będą używane w Etapach 2–4: `M-nn` mikro (znak, słowo, wiersz, akapit), `A-nn` makro (układ strony, rozkładówki, dokumentu), `W-nn` własne grupy.
- **Źródło B**: numer sekcji Bringhursta (pierwsza cyfra to rozdział, np. `2.1.2` to rozdz. 2) i numer strony **drukowanej** (strona początkowa sekcji lub miejsca, z którego pochodzi wartość). Plik PDF ma numer o 1 mniejszy niż druk (druk 26 = strona PDF 25). `B App.B` to dodatek B (słownik znaków).
- **Źródło L**: rozdział książki (`Letter` s. 10–83, `Text` s. 84–147, `Grid` s. 148–207, `App` s. 208–225) i numer strony; numeracja PDF zgadza się z drukiem.
- **Uwagi**: `KONFLIKT K-nn` odsyła do sekcji „Konflikty”; „Odpowiednik: …” to wskazówka na Etap 2, nie klasyfikacja.
- Zasady złożone z kilku parametrów zapisano w jednym wierszu tylko wtedy, gdy źródło podaje je jako jedną regułę; do klasyfikacji (Etap 2) wiersze będą rozbijane, jeśli części różnią się wykonalnością.
- Nazwy wdowa i sierota: Bringhurst (2.4.8) używa ich odwrotnie niż wiele poradników; wiersze o nich tak to oznaczają.

## Liczba zasad według poziomu i grupy

| Poziom | Grupa | Zasad |
|---|---|---:|
| mikro | Miara i długość wiersza | 6 |
| mikro | Interlinia i rytm pionowy | 9 |
| mikro | Skala rozmiarów | 8 |
| mikro | Dobór i zestawianie krojów | 17 |
| mikro | Kapitaliki i wersaliki | 7 |
| mikro | Ligatury | 6 |
| mikro | Cyfry | 6 |
| mikro | Liczby, daty i jednostki | 6 |
| mikro | Wyrównanie i justowanie | 13 |
| mikro | Dzielenie wyrazów | 9 |
| mikro | Wdowy i sieroty | 5 |
| mikro | Spacje i interpunkcja | 20 |
| mikro | Niełamliwość i spacje twarde | 3 |
| mikro | Kerning i odstępy międzyliterowe | 9 |
| mikro | Wyróżnienia i emfaza | 3 |
| mikro | Akapity i cytaty blokowe | 8 |
| mikro | Inicjały i otwarcie tekstu | 5 |
| mikro | Przypisy | 5 |
| mikro | Znaki, diakrytyki i język | 4 |
| mikro | Wielojęzyczność i alfabety | 4 |
| makro | Proporcje formatu i pola składu | 14 |
| makro | Kanony konstrukcji strony i marginesy | 11 |
| makro | Siatka modułowa i bazowa | 12 |
| makro | Kolumna główna i pomocnicze (marginalia) | 6 |
| makro | Rozkładówka i para stron | 4 |
| makro | Folio, żywa pagina i nawigacja | 6 |
| makro | Pusta przestrzeń | 3 |
| makro | Rytm dokumentu | 1 |
| makro | Elastyczność układu i zaokrąglenia | 3 |
| makro | Ilustracje, podpisy i relacja do kolumny | 3 |
| makro | Strona tytułowa, spisy i początki rozdziałów | 7 |
| makro | Hierarchia nagłówków i struktura układu | 8 |
| własne | Tabele i listy | 8 |
| własne | Kolor tekstu i druku | 5 |
| własne | Papier, technologia i format wydawniczy | 7 |
| własne | Tradycja kroju i historia | 6 |
| własne | Ekran i render | 8 |
| własne | Struktura HTML i dostępność | 5 |
| własne | Font jako artefakt | 11 |
| własne | Akcydens, ornament i tekst ekspresyjny | 5 |
| własne | Proces i redakcja | 2 |
| **razem** | | **288** |

## Katalog

| ID | Poziom | Grupa | Zasada | Źródło | Uwagi |
|---|---|---|---|---|---|
| M-01 | mikro | Miara i długość wiersza | Akapit ciągły w jednej kolumnie, krój szeryfowy, rozmiar tekstowy: 45–75 znaków w wierszu (ze spacjami i interpunkcją); 66 znaków to uznana wartość idealna. | B 2.1.2, s. 26 |  |
| M-02 | mikro | Miara i długość wiersza | Tekst w kilku kolumnach: średnio 40–50 znaków w wierszu. | B 2.1.2, s. 26 |  |
| M-03 | mikro | Miara i długość wiersza | Wiersz średnio dłuższy niż 75–80 znaków jest za długi do czytania ciągłego, nawet przy dużej interlinii; 85–90 znaków dopuszcza się tylko w tekście nieciągłym (bibliografie, przypisy). | B 2.1.2, s. 26–27 |  |
| M-04 | mikro | Miara i długość wiersza | Miara książkowa to ok. 30× rozmiar kroju; do przyjęcia jest 20–40×. | B 2.1.2, s. 27 | Przykład z książki: 10 pt, miara 300 pt, ok. 65 znaków |
| M-05 | mikro | Miara i długość wiersza | Dolne granice miary: tekst justowany nie krótszy niż ok. 40 znaków (poniżej 38–40 grozi „biały trądzik” spacji i seria dzieleń); tekst ragged nie krótszy niż ok. 30; krótkie notki marginesowe mogą mieć 12–15 znaków. | B 2.1.2, s. 27; L·Text s. 112 | L: justowanie w zbyt wąskiej kolumnie daje dziury |
| M-06 | mikro | Miara i długość wiersza | Liczbę znaków w wierszu wylicza się z długości małego alfabetu danego kroju i rozmiaru (10 pt: roman zwykle 120–140 pt, italic ok. 100 pt, bold do 160 pt); ta sama miara w pt daje różną liczbę znaków w różnych krojach. | B 2.1.2, s. 27; tabela na s. 29 | Odpowiednik webowy: miara w ch. Tabela odtworzona w bringhurst-tabele.md (§1), nie jako transkrypcja |
| M-07 | mikro | Interlinia i rytm pionowy | Interlinię dobiera się do kroju, tekstu i miary: dłuższa miara, ciemniejszy krój, duży korpus (wysokość x), krój bezszeryfowy, częste wersaliki, indeksy lub wzory wymagają większej interlinii; niemiecki tekst nieco większej niż łaciński. | B 2.2.1, s. 36–37 |  |
| M-08 | mikro | Interlinia i rytm pionowy | Typowa interlinia tekstu: 9/11, 10/12, 11/13, 12/15 (domyślnie ok. 120% rozmiaru). Interlinia ujemna (np. 18/15) tylko w krótkich nagłówkach lub reklamie, bez kolizji kresek; w tekście ciągłym praktycznie nigdy; skład „solid” (1:1) wytrzymuje niewiele krojów. | B 2.2.1, s. 36–37; L·Text s. 108 |  |
| M-09 | mikro | Interlinia i rytm pionowy | Pionowa przestrzeń zmienia się w mierzonych odstępach: każde odstępstwo od tekstu głównego (nagłówek, cytat, przypis, ilustracja) zajmuje całkowitą wielokrotność interlinii, żeby tekst wracał „w fazie” (przy 11/13: 26, 39, 52, 65 pt). | B 2.2.2, s. 37 | Podstawa rytmu pionowego |
| M-10 | mikro | Interlinia i rytm pionowy | Nagłówki: przestrzeń nad i pod w sumie równa całkowitej liczbie linii tekstu (np. 13+13; 8+5; 26+13), także asymetrycznie. | B 2.2.2, s. 37 |  |
| M-11 | mikro | Interlinia i rytm pionowy | Blok o innej interlinii niż tekst (np. cytat 10/12 w tekście 11/13) domykaj elastycznymi odstępami przed i po tak, by wysokość bloku z odstępami była wielokrotnością interlinii tekstu. | B 2.3.3, s. 40 | Przykład z książki: 5 linii 10/12 = 60 pt → 78 pt, odstępy po 9 pt |
| M-12 | mikro | Interlinia i rytm pionowy | Linie tekstu na obu stronach kartki oraz na obu stronach rozkładówki leżą na wspólnych liniach (register). | B 2.2.2, s. 37 | Dotyczy druku dwustronnego |
| M-13 | mikro | Interlinia i rytm pionowy | Strona nie może dusić tekstu: 30–45 wierszy na stronie książki przy 60–66 znakach (300–500 słów); powyżej 500 słów rozważ kolumny (dwie kolumny wygodnie 750 słów); im dłuższy wiersz, tym więcej interlinii. | B 2.2.3, s. 39 |  |
| M-14 | mikro | Interlinia i rytm pionowy | Całe wiersze wersalików mogą mieć ciaśniejszą interlinię (brak ascenderów i descenderów), ale w stosach mieszanych (wersaliki nad małymi literami) odstępy wyglądają nierówno i wymagają korekty linii bazowej. | L·Letter s. 52–53 |  |
| M-15 | mikro | Interlinia i rytm pionowy | Przy mieszaniu rozmiarów w jednym bloku interlinia „auto” daje nierówny efekt; ustaw interlinię jawnie i skoryguj linię bazową. | L·Text s. 108 |  |
| M-16 | mikro | Skala rozmiarów | Nie składaj bez skali: ogranicz się do skromnego zestawu powiązanych rozmiarów; tradycyjna skala (6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 21, 24, 36, 48, 60, 72 pt) działa jak skala diatoniczna. | B 3.1.1, s. 45 |  |
| M-17 | mikro | Skala rozmiarów | Skale rozmiarów wyprowadzone ze złotego podziału (każdy wyraz = suma dwóch poprzednich): 3·5·8·13·21·34·55·89; 6·10·16·26·42·68·110 (podwojony poprzedni); 4·7·11·18·29·47·76; splot dwóch ciągów 6·8·10·13·16·21·26·34·42·55·68; skala Le Corbusiera 4·5·6½·8·10½·13·17·21·27½·34·44½·55·72. | B 8.2, s. 157–158 | Pierwszy ciąg (a) odtworzony rachunkiem z tekstu (b = 2a), por. bringhurst-tabele.md §2 |
| M-18 | mikro | Skala rozmiarów | Skala modułowa oparta na dwóch proporcjach (np. 1:φ i 1:2) jest bardziej elastyczna niż oparta na jednej. | B 8.6.1, s. 166 |  |
| M-19 | mikro | Skala rozmiarów | Rozmiar zależy od medium i kontekstu: w druku typowo 9–11 pt, 12 pt wygląda „koniowato”, podpisy ok. 7,5 pt; ten sam rozmiar bywa za duży na papierze i za mały na dużym ekranie. | L·Letter s. 39, 42; L·App s. 218 | L s. 218 ostrzega też przed rozmiarami za małymi |
| M-20 | mikro | Skala rozmiarów | Hierarchia rozmiarów wymaga wyraźnego kontrastu; minimalne różnice rozmiaru wyglądają na niezdecydowane i przypadkowe. | L·Letter s. 42 |  |
| M-21 | mikro | Skala rozmiarów | Zmieniaj jeden parametr na raz: tytuł najpierw jako ten sam krój w wadze i rozmiarze tekstu (kapitaliki spacjowane, wersaliki spacjowane, kursywa lub bold), dopiero potem większy rozmiar. | B 3.5.1, s. 60 | KONFLIKT K-07 |
| M-22 | mikro | Skala rozmiarów | Wraz ze wzrostem rozmiaru waga kroju lekko maleje, nie rośnie; duże tytuły w wadze lekkiej (light, kontur, inline), nie w bold. | B 3.5.1, s. 60; 4.1.2, s. 61–62 |  |
| M-23 | mikro | Skala rozmiarów | Style optyczne: „display” od ok. 24 pt wzwyż (delikatne), „text” 9–14 pt, „caption” 6–8 pt z najgrubszą kreską; mechaniczne skalowanie jednego rysunku daje za grube lub za cienkie detale. | L·Letter s. 41 | Odpowiednik: oś opsz |
| M-24 | mikro | Dobór i zestawianie krojów | Krój dobieraj do charakteru tekstu, zadania i kontekstu (nie dosłownie do tematu): dobry do długiego czytania, spokojny, z pokryciem potrzebnych glifów. | B 1.2.4, s. 22; 6.2.1, s. 95; 6.4.1, s. 99 |  |
| M-25 | mikro | Dobór i zestawianie krojów | Krój musi zawierać to, czego tekst wymaga: kapitaliki, cyfry tekstowe, potrzebne wagi, pasujący krój bezszeryfowy, alfabety (łaciński rozszerzony, grecki, cyrylica, fonetyka). Jeden krój z kompletem części jest lepszy niż pięćdziesiąt bez nich. | B 6.2.2, s. 95; 3.2.1, s. 47; 6.8.1, s. 117 |  |
| M-26 | mikro | Dobór i zestawianie krojów | Krój skromny ustawiaj skromnie: jeden rozmiar, dobrze rozstawione wersaliki, dobrze dobrana interlinia, optymalna miara, starannie proporcjonowana strona; używaj mniej, niż jest dostępne. | B 6.2.3, s. 96 |  |
| M-27 | mikro | Dobór i zestawianie krojów | Spośród kilku popularnych krojów o różnych koncepcjach litery (Baskerville, Helvetica, Palatino, Times) wybierz jeden; nie łącz ich ze sobą. | B 6.2.3, s. 96–98 |  |
| M-28 | mikro | Dobór i zestawianie krojów | Zacznij od jednej rodziny krojowej (roman, italic, kapitaliki, wagi); rozszerzona rodzina daje różnorodność w jednej kulturze typograficznej. | B 6.5.1, s. 102 |  |
| M-29 | mikro | Dobór i zestawianie krojów | Szanuj całość roman / italic / kapitaliki: nie łącz kursywy jednego kroju z romanem innego ani kapitalików z wersalikami innego kroju. | B 6.5.2, s. 103 |  |
| M-30 | mikro | Dobór i zestawianie krojów | Hierarchia rodziny: roman → kapitaliki → italic → bold; odwrócenie tego porządku (bold wersaliki na tle romana) męczy czytelnika; przejścia między odmianami wzdłuż linii hierarchii. | B 3.4.1, s. 53–55 |  |
| M-31 | mikro | Dobór i zestawianie krojów | Nie używaj odmiany, której nie potrzebujesz: bold i półbold do znaczników list, małych tytułów, haseł słownika, tekstu jasnego na ciemnym; nie rozsypuj ich po tekście. | B 3.4.2, s. 55–56; 6.5.3, s. 103 |  |
| M-32 | mikro | Dobór i zestawianie krojów | Bold dobieraj o strukturze zgodnej z krojem (rodzina projektowana z wagami albo pokrewna), nie z dopisanej wstecznie wagi starej antykwy; waga półbold i bold musi mieć własny italic. | B 6.5.3, s. 103–105; L·Letter s. 48 |  |
| M-33 | mikro | Dobór i zestawianie krojów | Kursywa nie jest pochylonym romanem: nie pochylaj mechanicznie (pseudokursywa); awaryjnie do ok. 10°; italic może być niepochylony, a pochylenie nie jest jego cechą definiującą. | B 3.4.3, s. 56–59; L·Letter s. 48 | Odpowiednik: font-synthesis |
| M-34 | mikro | Dobór i zestawianie krojów | Nie zniekształcaj liter: nie skaluj ich poziomo ani pionowo i nie ściskaj dla dopasowania tekstu; użyj odmiany condensed lub extended. | B 2.1.9, s. 35; L·Letter s. 38 |  |
| M-35 | mikro | Dobór i zestawianie krojów | Kroje tytułowe i display wzmacniają strukturę kroju tekstu (kaligraficzny do kaligraficznego; geometryczny kontrastowy do baskerville’owskiego), nie przeczą jej. | B 6.5.4, s. 105 |  |
| M-36 | mikro | Dobór i zestawianie krojów | Parowanie szeryfowego i bezszeryfowego według struktury wewnętrznej (Meridien + Frutiger; Garamond + Syntax; Futura + antykwa z Bodoniego), nie według nazwy. | B 6.5.5, s. 105–106 |  |
| M-37 | mikro | Dobór i zestawianie krojów | Mieszaj kroje przez kontrast, nie mdłe podobieństwo: mało elementów o wyraźnie różnych rolach; unikaj wag zbliżonych w jednej rodzinie i dwóch podobnych krojów obok siebie. | L·Letter s. 54 |  |
| M-38 | mikro | Dobór i zestawianie krojów | Mieszając kroje w jednym wierszu wyrównaj ich wysokość x; mieszając w osobnych wierszach, różnicuj także skalę. Dopasowanie ma być optyczne, nie matematyczne. | L·Letter s. 54; B 6.6.3, s. 112 | Odpowiednik: font-size-adjust |
| M-39 | mikro | Dobór i zestawianie krojów | Dwa kroje o tym samym rozmiarze nominalnym wyglądają na różnej wielkości (wysokość x, waga, szerokość): porównuj wizualnie. | L·Letter s. 39 |  |
| M-40 | mikro | Dobór i zestawianie krojów | Nie mieszaj dwóch krojów w jednym wyrazie (łatana typografia = porażka); cały wyraz lub fragment w jednym foncie. | B 6.7.4, s. 116 |  |
| M-41 | mikro | Kapitaliki i wersaliki | Skrótowce w tekście bieżącym składaj spacjowanymi kapitalikami (AM, PM, CE, BC, NATO, 3:00 AM). | B 3.2.2, s. 48 |  |
| M-42 | mikro | Kapitaliki i wersaliki | Wyjątki od kapitalików: dwuliterowe skróty geograficzne i skróty imion (JFK) zostają wersalikami; spójność przy mieszaniu długich i krótkich skrótów; kapitaliki w krojach o małej wysokości x, wersaliki w krojach o dużej. | B 3.2.2, s. 48 |  |
| M-43 | mikro | Kapitaliki i wersaliki | Akronimy czytane jak słowa składaj małymi literami z wielką na początku (Unesco, Ascii); akronimy czytane literowo wersalikami (CD, TV, USA). | B 3.2.3, s. 49 | Decyzja według mowy |
| M-44 | mikro | Kapitaliki i wersaliki | Używaj prawdziwych kapitalików (inne proporcje, waga i szerokość), nie pomniejszonych wersalików; pseudokapitaliki wyglądają „chudo i zagłodzone”. W kroju bez kapitalików nie udawaj ich. | B 3.2.2, s. 48; L·Letter s. 52 | Odpowiednik: font-synthesis-small-caps |
| M-45 | mikro | Kapitaliki i wersaliki | Słowo lub krótka fraza wersalikami w tekście bieżącym wygląda ciężko; długi tekst złożony wyłącznie wersalikami jest nieczytelny. | L·Letter s. 52 |  |
| M-46 | mikro | Kapitaliki i wersaliki | Kapitaliki spacjowane przy prawdziwych kapitalikach do wyróżnień i nagłówków; spacjowane wersaliki w nagłówkach zamiast bold; w pełnych kapitalikach (bez mieszania z wersalikami) linia nie ma wystających elementów. | B 3.5.1, s. 60; L·Letter s. 52 |  |
| M-47 | mikro | Kapitaliki i wersaliki | Przy składzie wersalikami dopasuj położenie łączników, nawiasów i cudzysłowów do wysokości wersalików (OpenType „case”). | L·Letter s. 80 | Odpowiednik: font-feature-settings „case” |
| M-48 | mikro | Ligatury | Używaj ligatur wymaganych przez font i język: ff, fi, fl, ffi, ffl w kroju, który ich wymaga; w krojach z rodziną f nachodzącą na kolejną literę brak ligatur daje kolizje. | B 3.3.1, s. 50 |  |
| M-49 | mikro | Ligatury | Sprawdź, że oprogramowanie wstawia wszystkie pożądane ligatury i tylko je, i że ligatury zostają na miejscu po justowaniu lub spacjowaniu. | B 3.3.1, s. 51–52 |  |
| M-50 | mikro | Ligatury | Ligatury dyskrecjonalne (Th, ct, st, sp) to osobny rejestr stylistyczny; nie mieszaj ich z podstawowymi (fi, fl) w jednym przełączniku. | B 3.3.1, s. 51 |  |
| M-51 | mikro | Ligatury | Tekst spacjowany nie ma ligatur nieistotnych (wyłącz ligatury przy letterspacingu). | B 2.1.7, s. 31 |  |
| M-52 | mikro | Ligatury | Jeśli rezygnujesz z ligatur, wybierz kroje o niekolidującym f (Aldus, Sabon, Palatino, Trump Mediaeval) lub bezszeryfowe bez ligatur. | B 3.3.2, s. 52–53 |  |
| M-53 | mikro | Ligatury | Ligatury leksykalne (æ, œ) są wymagane przez język lub cytat z dawnego tekstu; ligatury typograficzne (fi, fl) są stylistyczne; w tureckim fi nie łączy się, bo i i ı to różne litery. | B 3.3.1, s. 50–51; B App.B, s. 309, 312 |  |
| M-54 | mikro | Cyfry | Cyfry tytułowe (lining) stosuj z wersalikami; cyfry tekstowe (old-style, text figures) we wszystkich pozostałych sytuacjach, także w kapitalikach; lining w tekście bieżącym to „analfabetyzm” typograficzny. | B 3.2.1, s. 46–48; L·Letter s. 56 | Wyjątek wg B: pełne wersaliki |
| M-55 | mikro | Cyfry | W tabelach i kolumnach liczbowych cyfry tabelaryczne (równa szerokość); w tekście bieżącym cyfry proporcjonalne. | B 4.4.3, s. 71; L·Letter s. 56–57 |  |
| M-56 | mikro | Cyfry | Cyfry w tekście wymagają kerningu między sobą i względem półpauzy; cyfry nie są pomijane w tablicach kerningu. | B 2.1.8, s. 33 |  |
| M-57 | mikro | Cyfry | Znaki walut i działań dopasuj do stylu cyfr (mniejsze przy cyfrach tekstowych). | L·Letter s. 56 |  |
| M-58 | mikro | Cyfry | Wykładniki, liczniki ułamków i indeksy dolne (H₂O, mianowniki) składaj prawdziwymi znakami „superior” i „inferior”, nie pomniejszonymi cyframi, jeśli font je ma. | B App.B, s. 309 | Odpowiednik: font-variant-position |
| M-59 | mikro | Cyfry | Cyfry w parach nie wymagają spacjowania; ciągi trzech i więcej cyfr (telefony, numery seryjne, daty) wymagają „powietrza” (grupowanie, letterspacing). | B 2.1.6, s. 30 |  |
| M-60 | mikro | Liczby, daty i jednostki | Separator dziesiętny w Europie to przecinek, a tysiące grupuje się spacją (10 000 000); zapis 10,001 bez kontekstu jest niejednoznaczny. | B App.B, s. 305 | Dla pl: przecinek dziesiętny, spacja tysięcy |
| M-61 | mikro | Liczby, daty i jednostki | Ułamki: gotowe znaki (¼ ½ ¾) lub ułamek zbudowany z licznika superior, ułamkowej kreski (solidus) i mianownika inferior; poziome ułamki ukośnikiem (virgule). | B App.B, s. 310, 317; B 5.2.5, s. 81 | Odpowiednik: font-variant-numeric: diagonal-fractions |
| M-62 | mikro | Liczby, daty i jednostki | Znak wymiaru: × (nie litera x) w „26 × 42 cm”, „2 × 4”; znak minus − i znaki działań z jednego fontu technicznego. | B 5.2.6, s. 82; B App.B, s. 302, 307 |  |
| M-63 | mikro | Liczby, daty i jednostki | Zakres liczb (3–6 listopada, 4:30–5:00, 25–30 mm): półpauza ciasno, bez spacji (lub kreska ok. 1/3 em); w prozie lepiej „od 25 grudnia do 3 stycznia” niż pauza między złożonymi wyrażeniami. | B 5.2.2, s. 80–81; L·App s. 211 |  |
| M-64 | mikro | Liczby, daty i jednostki | Bez apostrofu w liczbowych liczbach mnogich (lata 1930., dwójki 2 × 4s); bez kropki po jednostkach metrycznych (5,2 m, 520 cm). | B 5.4.3–5.4.4, s. 87–88 |  |
| M-65 | mikro | Liczby, daty i jednostki | Prime (′ ″) tylko dla stóp, cali, minut i sekund łuku; nie używaj ich jako cudzysłowów ani apostrofów; znak stopnia (°) to nie ordinal ani pierścień. | L·Letter s. 58–59; L·App s. 211; B App.B, s. 306, 316 |  |
| M-66 | mikro | Wyrównanie i justowanie | Ustaw tekst ragged right, gdy to pasuje do tekstu i strony; w wąskich kolumnach (wielokolumnowość) ragged lżejszy i unika dzieleń; kroje bezszeryfowe często lepiej wyglądają ragged; kroje monospace zawsze. | B 2.1.3, s. 27–28 |  |
| M-67 | mikro | Wyrównanie i justowanie | „Twardy rag”: stałe odstępy, brak minimalnej długości wiersza, brak letterspacingu i dzielenia poza tym, co tkwi w tekście; unikaj „ładnie poplisowanej” prawej krawędzi. | B 2.1.3, s. 28 | Odpowiednik: text-wrap (pretty, balance) wygładza rag, czyli działa przeciwnie do twardego ragu |
| M-68 | mikro | Wyrównanie i justowanie | Dobry rag wygląda przyjemnie nierówno, bez wierszy skrajnie długich lub krótkich i z minimum dzieleń; zły rag tworzy regularne kształty (klin, półksiężyc, trampolinę) lub jest zbyt równy; interpunkcja na końcu wierszy osłabia prawą krawędź. | L·Text s. 113 |  |
| M-69 | mikro | Wyrównanie i justowanie | Tekst wyrównany do prawej (ragged left) tylko w krótkich blokach (notki, pull quote, podpisy, sąsiednie marginalia); w dłuższym tekście utrudnia czytanie. | L·Text s. 113; B 1.2.5, s. 23–24 | L: obiegowa opinia o trudności czytania (możliwy mit); B: ragged left akcentuje koniec wiersza |
| M-70 | mikro | Wyrównanie i justowanie | Tekst wyśrodkowany: łam wiersze „dla sensu” (fraza w wierszu), z różnicą długości wierszy; używaj do tytułów, zaproszeń, stron tytułowych; zły: losowe łamania i kształt grobowca. | L·Text s. 112, 114 |  |
| M-71 | mikro | Wyrównanie i justowanie | Justowanie: najlepszy silnik liczy podział paragrafami, nie wiersz po wierszu; mikroregulacja odstępu między znakami ±3% i szerokości glifów ±2%, przy czym elastyczność znaków to ok. 1/5 elastyczności spacji międzywyrazowych. | B 9.4.1, s. 190–191 | KONFLIKT K-06 |
| M-72 | mikro | Wyrównanie i justowanie | Żadne oprogramowanie nie powinno automatycznie ściskać, rozciągać ani spacjować tekstu, żeby go dopasować; problemy z dopasowaniem rozwiązuj projektem, nie kosztem czytelnika. | B 2.4 (wstęp), s. 42 | KONFLIKT K-06 |
| M-73 | mikro | Wyrównanie i justowanie | W tekście justowanym unikaj dziur i rzek: wąska kolumna, długie wyrazy i zbyt mała miara dają luki; tracking dodatni lub ujemny stosuje się oszczędnie jako środek pomocniczy. | L·Text s. 90, 112; B 2.1.3, s. 27 | KONFLIKT K-06 |
| M-74 | mikro | Wyrównanie i justowanie | Hanging punctuation: cudzysłowy otwierające i znaki na początku wiersza wiszą w marginesie, aby krawędź bloku była czysta; wiszące łączniki na końcu wiersza w prawym marginesie. | L·Letter s. 58; B 5.1.4, s. 78–79; 4.1.5, s. 64 | Odpowiednik: hanging-punctuation |
| M-75 | mikro | Wyrównanie i justowanie | Poezja składa się flush left, bo łamania wersów są elementem formy; wyśrodkowanie poezji tylko wyjątkowo. | L·Text s. 115; B 2.3.4, s. 41 |  |
| M-76 | mikro | Wyrównanie i justowanie | Jedna spacja po kropce, dwukropku i innych znakach (nie dwie); en space między zdaniami tylko w tekstach, gdzie zdania zaczynają się małą literą. | B 2.1.4, s. 28; L·App s. 210–211 |  |
| M-77 | mikro | Wyrównanie i justowanie | Spacja nie służy do wcięć, centrowania ani pozycjonowania (używaj tabulatorów i wcięć). | L·App s. 210, 213 | HTML ignoruje podwójne spacje |
| M-78 | mikro | Wyrównanie i justowanie | Odstęp międzywyrazowy dostosuj do rozmiaru i kroju: typowo M/4 (ok. ¼ em); justowany: minimum M/5, średnio M/4, maksimum M/2 (lepiej M/3); kroje luźne i małe rozmiary M/3 średnio, M/4 minimum; w dużych rozmiarach ciaśniej (np. 80% w nagłówkach). | B 2.1.1, s. 25–26; L·Text s. 103 |  |
| M-79 | mikro | Dzielenie wyrazów | Przy dzieleniu zostaw w pierwszym wierszu co najmniej 2 znaki, przenieś co najmniej 3 (fi-nally, nie final-ly). | B 2.4.1, s. 42 | Odpowiednik: hyphenate-limit-chars |
| M-80 | mikro | Dzielenie wyrazów | Ostatni wiersz akapitu nie może być końcówką dzielonego słowa ani wyrazem krótszym niż 4 litery. | B 2.4.2, s. 42 |  |
| M-81 | mikro | Dzielenie wyrazów | Nie więcej niż 3 kolejne wiersze zakończone dzieleniem. | B 2.4.3, s. 43 | Odpowiednik: hyphenate-limit-lines |
| M-82 | mikro | Dzielenie wyrazów | Nazwy własne dziel tylko w ostateczności, chyba że występują tak często jak rzeczowniki pospolite. | B 2.4.4, s. 43 |  |
| M-83 | mikro | Dzielenie wyrazów | Dziel według reguł języka tekstu, także przy pojedynczych cytowanych wyrazach obcych. | B 2.4.5, s. 43 | lang / hyphens |
| M-84 | mikro | Dzielenie wyrazów | Nie zaczynaj więcej niż dwóch kolejnych wierszy tym samym słowem. | B 2.4.7, s. 43 |  |
| M-85 | mikro | Dzielenie wyrazów | Unikaj dzielenia wyrazów tam, gdzie tekst jest przerwany (ilustracja, mapa, pull quote, ramka). | B 2.4.10, s. 44 |  |
| M-86 | mikro | Dzielenie wyrazów | W tekście ragged i wyśrodkowanym wyłącz automatyczne dzielenie; zastąp je dzieleniem warunkowym (&shy;) i tylko gdy nieuniknione. | L·App s. 210; B 2.1.3, s. 28 | Odpowiednik: hyphens: manual |
| M-87 | mikro | Dzielenie wyrazów | Do dzielenia ręcznego używaj łącznika warunkowego, nie twardego: twardy łącznik wstawiony w miejscu podziału zostaje w środku wiersza po zmianie łamania, a warunkowy znika. | L·App s. 210 | Odpowiednik: &shy; |
| M-88 | mikro | Wdowy i sieroty | Nigdy nie zaczynaj strony ostatnim wierszem wielowierszowego akapitu („wdowa” u Bringhursta: ma przeszłość, ale nie ma przyszłości); dopełnij ją jeszcze jednym wierszem poprzedniego (min. 2 wiersze akapitu u góry). | B 2.4.8, s. 43–44 | Odpowiednik: widows. Terminologia Bringhursta odwrotna do wielu poradników |
| M-89 | mikro | Wdowy i sieroty | Samotny pierwszy wiersz akapitu na dole strony („sierota” u Bringhursta: ma przyszłość, więc „nie trapi typografa”) jest dopuszczalny; ostrzejsza praktyka (min. 2 wiersze na dole) to konwencja poradników, nie tej książki. | B 2.4.8, s. 43–44 | Odpowiednik: orphans. Do rozstrzygnięcia w Etapie 2 |
| M-90 | mikro | Wdowy i sieroty | Wyrównuj głębokość rozkładówki przez przenoszenie pojedynczych wierszy z poprzednich lub do następnych rozkładówek, nie przez dodatkową interlinię ani rozpychanie spacji; rozkładówka ciągłego tekstu nie powinna być dłuższa lub krótsza niż o jeden wiersz. | B 2.4.9, s. 44 |  |
| M-91 | mikro | Wdowy i sieroty | Pozostawiony na ostatniej stronie rozdziału kilkuwierszowy ogon: rozciągnij kilka poprzednich rozkładówek o linię lub skróć sześć o linię, nie zmieniaj interlinii ani odstępów między akapitami. | B 8.8.3, s. 178 | Zgodne z B 2.4.9 |
| M-92 | mikro | Wdowy i sieroty | Nie zostawiaj nagłówka podrzędnego na dole strony oderwanego od tekstu (sierota nagłówka). | B 8.8.3, s. 178 |  |
| M-93 | mikro | Spacje i interpunkcja | Inicjały osobowe: zbędna lub minimalna (cienka, włosowa) spacja po wewnętrznych kropkach (W. B. Yeats), zwykła spacja po ostatniej kropce. | B 2.1.5, s. 30 |  |
| M-94 | mikro | Spacje i interpunkcja | Wtrącenie oznaczaj półpauzą (en dash) ze zwykłą spacją po obu stronach, nie zwartą pauzą em ani łącznikiem ze spacjami; pauza em jest za długa dla dobrych krojów tekstowych (wiktoriański zwyczaj). | B 5.2.1, s. 80 | KONFLIKT K-01 |
| M-95 | mikro | Spacje i interpunkcja | Wtrącenie oznaczaj pauzą em bez spacji wokół; pauza oznacza silne przerwanie wypowiedzi. | L·App s. 210–211 | KONFLIKT K-01 |
| M-96 | mikro | Spacje i interpunkcja | Nie używaj podwójnego łącznika (--) ani łącznika zamiast pauzy/półpauzy; półpauza nie zastępuje łącznika w wyrazach złożonych (second–best). | B 5.2.1, s. 80; L·App s. 211 |  |
| M-97 | mikro | Spacje i interpunkcja | Pauza dialogowa: pauza z cienką spacją (M/5) lub spacją na początku wypowiedzi zamiast cudzysłowów. | B 5.2.3, s. 81 | Zwyczaj europejski |
| M-98 | mikro | Spacje i interpunkcja | Trzy-em (––) jako znak powtórzenia nazwiska w bibliografii. | B 5.2.4, s. 81 | Rzadka konwencja |
| M-99 | mikro | Spacje i interpunkcja | Ukośnik (virgule) w słowach i datach, z odpowiednim kerningiem; ułamkowa kreska pod kątem ok. 45° tylko do ułamków. | B 5.2.5, s. 81–82 |  |
| M-100 | mikro | Spacje i interpunkcja | Wielokropek jednym znakiem lub trzema kropkami dopasowanymi do kroju (flush, z cienkimi spacjami, nieco więcej w małych rozmiarach); po zdaniu kropka plus wielokropek (angielski); wokół wielokropka zwykła spacja. | B 5.2.7, s. 82–83; L·App s. 210–211 | Książki zgodne co do wyboru (flush, rozstrzelone lub ze spacjami); Chicago Manual (M/3) odrzucony przez B |
| M-101 | mikro | Spacje i interpunkcja | Interpunkcja jest notacją, nie ekspresją: nie składaj wielokrotnych !!!/???, nie powtarzaj kresek; kilka łączników ze skanu zamień na jedną pauzę. | B 5.2.8, s. 83–84 |  |
| M-102 | mikro | Spacje i interpunkcja | Nawiasy okrągłe i kwadratowe są pionowe nawet w italic i dobrane do kroju (nie nabrzmiałe ukośne), z odpowiednią spacją; w italic dodaj odstęp, gdy trzeba. | B 5.3.1–5.3.2, s. 84–85 |  |
| M-103 | mikro | Spacje i interpunkcja | Cudzysłowy typograficzne (otwierające i zamykające), nie proste; apostrof to znak zamykającego pojedynczego cudzysłowu (’), nie prosty; automatyczne „smart quotes” psują apostrof wiodący (’tis). | L·Letter s. 58–59; L·App s. 210–211; B 5.5.2, s. 90 |  |
| M-104 | mikro | Spacje i interpunkcja | Postać i liczba cudzysłowów zależą od języka: odwrócone przecinki w krajach angielskich, dolne i górne („…”) i »…« po niemiecku, «…» po francusku i włosku (z cienkimi spacjami do tekstu); brytyjskie pojedyncze w podwójnych kontra amerykańskie podwójne w pojedynczych; minimalizuj użycie cudzysłowów. | B 5.4.1, s. 86–87 | KONFLIKT K-08 (zależnie od języka). Polskich cudzysłowów książki nie omawiają |
| M-105 | mikro | Spacje i interpunkcja | Pozycja cudzysłowu względem innej interpunkcji jest spójna (amerykańsko: przecinek i kropka wewnątrz; brytyjsko: poza, chyba że należą do cytatu); kerning cudzysłowu nad kropką tylko w dużych rozmiarach. | B 5.4.2, s. 87 |  |
| M-106 | mikro | Spacje i interpunkcja | Usuń zbędną interpunkcję: kropki po jednostkach i w skrótach pisanych kapitalikami, zbędne łączniki (postmodern); zachowaj interpunkcję potrzebną do sensu (twenty one-night stands, Douglas-fir). | B 5.4.4–5.4.5, s. 88–89 |  |
| M-107 | mikro | Spacje i interpunkcja | Znaki analfabetyczne (nawiasy, gwiazdka, §, ¶, #, ampersand, kropka) dobieraj z tego samego kroju; jeśli pożyczasz znak z innego fontu, wybierz ten, który pasuje do epoki, wagi i stylu kroju; sprawdź zwłaszcza nawiasy kwadratowe i okrągłe, gwiazdkę, pilcrow, §, #. | B 5.1.2, s. 76–77 |  |
| M-108 | mikro | Spacje i interpunkcja | W nagłówkach i tytułach używaj najlepszego dostępnego ampersandu (często z italic). | B 5.1.3, s. 78 |  |
| M-109 | mikro | Spacje i interpunkcja | Midpoint (·) jako separator w poziomej linii i znacznik listy (bullet • wiszący); znak inskrypcyjny w adresach i sygnaturach. | B 5.1.1, s. 75; B App.B, s. 304, 313 |  |
| M-110 | mikro | Spacje i interpunkcja | © na linii bazowej (nie superskrypt); ® i ™ jako superskrypty; § podwojony (§§) dla liczby mnogiej. | B App.B, s. 305, 317–318 |  |
| M-111 | mikro | Spacje i interpunkcja | Do mocniejszego odstępu w linii (podtytuł od tekstu, elementy papieru firmowego) użyj en space; do inicjałów osobowych i guillemetów cienkiej lub włosowej spacji; spacje stałe (em, en, cienka, figurowa) mają określone, różne funkcje. | L·App s. 210; B 2.1.5, s. 30; 2.4.6, s. 43 |  |
| M-112 | mikro | Spacje i interpunkcja | Łącznik (hyphen) ma szerokość ok. 1/4 em (czasem 1/5 em w krojach ekonomicznych), a jego kształt i pochylenie pasują do kroju; krótki, tępy i idealnie poziomy łącznik jak z Helvetiki w kroju renesansowym jest wadą. | B 5.1.4, s. 78–79 |  |
| M-113 | mikro | Niełamliwość i spacje twarde | Krótkie wyrażenia liczbowe i matematyczne łącz twardą spacją (6,2 mm; 3 in.; 4 × 4; strona 3; rozdział 5); w długich równaniach łam przy znaku równości lub innej logicznej pauzie. | B 2.4.6, s. 43 |  |
| M-114 | mikro | Niełamliwość i spacje twarde | Polska reguła: jednoliterowe spójniki i przyimki (a, i, o, u, w, z) nie kończą wiersza (twarda spacja po nich); półpauza w zakresach; cudzysłowy „…”; dzielenie wg polskich reguł. | Poza książkami: wymóg zadania; zasada ogólna B 2.4.6, s. 43 | Nie występuje w żadnej z książek; dodane z wymagań zadania |
| M-115 | mikro | Niełamliwość i spacje twarde | Nie stosuj kropek wiodących (dot leaders) ani gigantycznych luk w spisach i listach; sparuj tytuł z numerem w jednej strukturze (kolumny wyrównane do siebie). | B 2.1.10, s. 35 |  |
| M-116 | mikro | Kerning i odstępy międzyliterowe | Kerninguj spójnie i skromnie albo wcale; zbyt mało jest lepsze niż zbyt dużo, niespójne gorsze niż żadne. | B 2.1.8, s. 32 |  |
| M-117 | mikro | Kerning i odstępy międzyliterowe | Kerning dostosowany do języka (apostrofy: en ’d ’m ’s; fr. ’a ’e; niem. „T), bez kolizji z diakrytykami i kolejnych ciasnych kernów (L’Anse); kerning odstępu międzywyrazowego przy A, T, V, W, Y, cudzysłowach, apostrofie, 1, 3, 5. | B 2.1.8, s. 32–34; 10.3.6, s. 206 |  |
| M-118 | mikro | Kerning i odstępy międzyliterowe | Kerning metryczny (tablica fontu) do tekstu, optyczny do nagłówków i krojów bez tablicy; różnice widoczne przy dużych rozmiarach (H/a, T/a, T/o). | L·Text s. 102–103 | Odpowiednik: font-kerning |
| M-119 | mikro | Kerning i odstępy międzyliterowe | Nie rozbudowuj tablicy kerningu, by ratować źle dopasowane znaki (oo, oe); popraw sidebearings; tablica kerningu służy parom problemowym (To, Va, 7A), nie ratowaniu pospolitych par. | B 10.3.4, s. 202 |  |
| M-120 | mikro | Kerning i odstępy międzyliterowe | Spacjuj wersaliki i kapitaliki w ciągu (akronimy, tytuły) o 5–10% rozmiaru; w tytułach więcej (20–25% przy spacji międzyliterowej M/5–M/4); ważny jest balans (LA, AVA ciasno; NN, HIH szerzej), nie ilość. | B 2.1.6, s. 30–31; L·Text s. 105 |  |
| M-121 | mikro | Kerning i odstępy międzyliterowe | Nie spacjuj małych liter bez powodu; wyjątki: bezszeryfowe pogrubione zwężone w nagłówkach (ok. 10%), akronimy i adresy www/e-mail, w których litery liczą się osobno. | B 2.1.7, s. 31–32; L·Text s. 105 |  |
| M-122 | mikro | Kerning i odstępy międzyliterowe | Tracking w tekście ciągłym tylko w małych przyrostach; ujemny rzadko i oszczędnie przy krótkim wierszu; białe litery na ciemnym tle czytelniejsze z dodatnim trackingiem (np. +25). | L·Text s. 104 |  |
| M-123 | mikro | Kerning i odstępy międzyliterowe | Duże rozmiary: tracking ciaśniej, odstęp międzywyrazowy zmniejszony (ok. 80%); wersaliki i kapitaliki mogą mieć luźniejszy tracking. | L·Text s. 103, 105 |  |
| M-124 | mikro | Kerning i odstępy międzyliterowe | Nie spacjuj tekstu w tak ciasnym ujęciu, że litery się dotykają (tight tracking = type crime). | L·Text s. 104 |  |
| M-125 | mikro | Wyróżnienia i emfaza | Jedno wyróżnienie = jeden sygnał (kursywa jest standardem; alternatywy: bold, kapitaliki, kolor); nie składaj bold + italic + podkreślenie + wersaliki. | L·Text s. 132 |  |
| M-126 | mikro | Wyróżnienia i emfaza | Przy wyróżnieniu pogrubieniem interpunkcję zostaw w kroju bazowym; przy kursywie interpunkcja też kursywą; przy kapitalikach sprawdź tylko spacjowanie. | B 3.5.2, s. 60 |  |
| M-127 | mikro | Wyróżnienia i emfaza | Podkreślenie jest rzadko używane w formalnej typografii (zastępuje je kursywa); w druku nie podkreślaj tekstu. | L·App s. 214 | Linki w web |
| M-128 | mikro | Akapity i cytaty blokowe | Pierwszy akapit po tytule lub nagłówku bez wcięcia; wcięcie sygnalizuje przerwę, której na początku nie ma. | B 2.3.1, s. 39; L·Text s. 126 |  |
| M-129 | mikro | Akapity i cytaty blokowe | Kolejne akapity w tekście ciągłym: wcięcie co najmniej 1 en (typowo 1 em lub 1 interlinia; do 3 em); wcięcie > 3 em szkodzi. | B 2.3.2, s. 39–40; L·Text s. 126 |  |
| M-130 | mikro | Akapity i cytaty blokowe | Akapit oznaczaj wcięciem albo odstępem, nie obiema rzeczami naraz; odstęp ma być precyzyjnym przyrostem, nie pełną pustą linią (w druku odstęp rytmiczny). | L·Text s. 126–127; B 2.3.2, s. 40 | KONFLIKT K-02 |
| M-131 | mikro | Akapity i cytaty blokowe | Akapity blokowe (bez wcięcia, biała linia): krótkie dokumenty biznesowe; w długich tekstach „bezduszne”. | B 2.3.2, s. 40 | KONFLIKT K-02 |
| M-132 | mikro | Akapity i cytaty blokowe | Alternatywy dla wcięcia: znak akapitu (pilcrow, kwadracik, bullet) w biegu tekstu (oszczędne, ale utrudnia korekty), akapity wiszące (outdent) z dużymi literami marginalnymi, linie spadające (drop lines); ornamenty w wcięciach rzadko się sprawdzają. | B 2.3.2, s. 39–40; L·Text s. 126–129 |  |
| M-133 | mikro | Akapity i cytaty blokowe | Cytat blokowy wyróżnij jednym środkiem (zmiana kroju na italic, zmniejszenie rozmiaru lub wcięcie); odstęp przed i po bloku (biała linia lub półlinia). | B 2.3.3, s. 40 |  |
| M-134 | mikro | Akapity i cytaty blokowe | Cytat wierszowany wcinaj lub wyśrodkuj na najdłuższym wersie (zachowaj ragged right); wcięcie = (miara − szerokość najdłuższego wersu)/2. | B 2.3.4, s. 41–42 |  |
| M-135 | mikro | Akapity i cytaty blokowe | Jeśli tekst otwiera cytat, zachowaj cudzysłów otwierający (także przy inicjale). | B 4.1.5, s. 64 |  |
| M-136 | mikro | Inicjały i otwarcie tekstu | Oznacz każdy początek i wznowienie tekstu (po nagłówku wystarczy brak wcięcia; w pozostałych miejscach inicjał, fleuron, pierwsze słowa kapitalikami lub bold). | B 4.1.4, s. 63 |  |
| M-137 | mikro | Inicjały i otwarcie tekstu | Inicjał: podniesiony (elevated) na linii bazowej pierwszego wiersza, wcięty (drop cap) w blok N wierszy lub wiszący w marginesie; pierwsze słowa po inicjale kapitalikami, wersalikami lub bold jako most do tekstu. | B 4.1.4, s. 63; L·Text s. 124–125 | Odpowiednik: initial-letter, ::first-letter, ::first-line |
| M-138 | mikro | Inicjały i otwarcie tekstu | Inicjały A, I, O mogą być słowem: odstęp inicjału od reszty wyrazu nie może wprowadzać w błąd (np. Ahead). | B 4.1.4, s. 63 |  |
| M-139 | mikro | Inicjały i otwarcie tekstu | Obszar wcięty pod inicjał jest prostokątny, co przy literze o ukośnych bokach (A) wygląda niezgrabnie; skoryguj kształtem lub zawinięciem tekstu wokół litery; rozmiar i tracking inicjału dopasuj do tekstu. | L·Text s. 125 |  |
| M-140 | mikro | Inicjały i otwarcie tekstu | Wcięcie, sinkage i rozmiar inicjału można związać proporcją (złoty podział: 38,2% miary, inicjał 61,8% wcięcia). | B 8.2, s. 160 |  |
| M-141 | mikro | Przypisy | Forma przypisów: boczne (najlepiej widoczne), dolne (krótkie, rzadkie), końcowe (dowolnej długości); przypis dolny nie może przechodzić na drugą stronę. | B 4.3.1, s. 68 |  |
| M-142 | mikro | Przypisy | Rozmiary: dolne 8–9 pt, końcowe 9–10 pt, boczne do rozmiaru tekstu głównego. | B 4.3.1, s. 68 |  |
| M-143 | mikro | Przypisy | Odsyłacz w tekście jako superskrypt (liczba o zredukowanym rozmiarze, w razie potrzeby półbold i z większym odstępem); w samym przypisie liczba pełnowymiarowa, wisząca, bez kropki; numery zamiast symboli (* † ‡ § ‖ ¶); przy przecinkach nie kerninguj wysokiego indeksu. | B 4.3.2–4.3.3, s. 68–69 | Odpowiednik: font-variant-position: super |
| M-144 | mikro | Przypisy | Przypisy boczne mogą nie mieć wskaźników albo mieć stały znak (*). | B 4.3.2, s. 68 |  |
| M-145 | mikro | Przypisy | Przypisy końcowe jednoznacznie: razem na końcu publikacji, numeracja ciągła; przy numeracji w rozdziałach żywa pagina wskazuje zakres. | B 4.3.4, s. 69 |  |
| M-146 | mikro | Znaki, diakrytyki i język | Pełne diakrytyki i znaki nazw własnych oraz wyrazów obcych (ą ę ł ń ó ś ź ż i inne); font musi mieć pokrycie, a kodowanie poprawne. | B 5.5.1, s. 89–90; 9.1, s. 179 |  |
| M-147 | mikro | Znaki, diakrytyki i język | Tekst składa się z abstrakcyjnych znaków (f+f+i), a ligatury i alternatywy są glifami wybieranymi w składzie; Unicode nie zawiera kapitalików ani cyfr tekstowych. | B 9.3.1, s. 185; L·Letter s. 81 |  |
| M-148 | mikro | Znaki, diakrytyki i język | Język tekstu steruje zasadami składu: cudzysłowami, dzieleniem, kerningiem apostrofów i odstępami przy ; : ? !; kompromis między ciasnym zwyczajem angielskim a szerokim francuskim to większy lewy sidebearing tych znaków i wewnętrzne sidebearingi cudzysłowów francuskich i nawiasów. | B 2.1.8, s. 34; 10.3.4, s. 202; 2.4.5, s. 43 |  |
| M-149 | mikro | Znaki, diakrytyki i język | W tekście bieżącym nie używaj znaków bez funkcji typograficznej (ukośnik wsteczny, pionowa kreska pipe, daszek ASCII, @ poza adresami, proste cudzysłowy i apostrofy) ani zastępników (angielska litera x zamiast ×). | B App.B, s. 303, 308, 316; L·Letter s. 58 |  |
| M-150 | mikro | Wielojęzyczność i alfabety | Mieszając alfabety (łaciński, grecki, cyrylica, hebrajski), dobierz kroje o zbliżonym kolorze i rozmiarze; wybierz najpierw font dla najtrudniejszego alfabetu. | B 6.6.1–6.6.2, s. 106–111 |  |
| M-151 | mikro | Wielojęzyczność i alfabety | Alfabety w jednym tekście dopasuj optycznie, nie matematycznie: różnice wysokości x i rozciągłości (np. grecki 11 → 10,5 pt) koryguj małymi zmianami rozmiaru. | B 6.6.3, s. 112–113 | Odpowiednik: font-size-adjust |
| M-152 | mikro | Wielojęzyczność i alfabety | Pełny font tekstowy zamiast fontu „pi” dla fragmentów greckich i podobnych; matching punctuation i diakrytyki. | B 6.6.1, s. 110 |  |
| M-153 | mikro | Wielojęzyczność i alfabety | W nowych ortografiach nie dodawaj zbędnych znaków; dodawaj tylko wizualnie rozróżnialne; unikaj kapryśnej redefinicji znanych liter; przygotuj specjalne znaki od początku. | B 6.7.1–6.7.4, s. 114–117 | Rzadko dotyczy polskiego |
| A-01 | makro | Proporcje formatu i pola składu | Proporcje strony wybieraj spośród satysfakcjonujących kanonów (muzyczne, z figur geometrycznych, złoty podział, ISO), nie z dostępnych rozmiarów handlowych ani dowolnie. | B 8.3.1, s. 160; 8.1, s. 143–144 |  |
| A-02 | makro | Proporcje formatu i pola składu | Proporcja strony odpowiada treści, rozmiarowi i ambicji: zwykłe książki od 5:9 (1:1,8) do 4:5 (1:1,25); strony szersze niż 1:√2 tylko gdy są mapy, tabele, notatki boczne, szerokie ilustracje lub wiele kolumn. | B 8.3.2, s. 161 |  |
| A-03 | makro | Proporcje formatu i pola składu | Kanon proporcji muzycznych jako lista kontrolna: 1:2 (oktawa), 8:15, 9:16, 3:5, 5:8, 1:√2, 2:3 (kwinta), 3:4 (kwarta), 4:5, 5:6, 8:9, 1:1. | B 8.1, s. 146–149 | Pełne tabele s. 148–149 odtworzone w bringhurst-tabele.md (§3–4), nie jako transkrypcja |
| A-04 | makro | Proporcje formatu i pola składu | Strony 2:3 i 3:4 (kwinta, kwarta) to ulubione kształty średniowiecza; po złożeniu arkusza odtwarzają się wzajemnie (40×60 → 30×40 → 20×30). | B 8.1, s. 147; 8.3.3, s. 162 |  |
| A-05 | makro | Proporcje formatu i pola składu | Proporcja 1:√2 (ISO) odtwarza się przy każdym złożeniu, ale sama w sobie jest najmniej „muzyczna”: wymaga pola składu o innym kształcie dla kontrastu. | B 8.1, s. 153–154 |  |
| A-06 | makro | Proporcje formatu i pola składu | Złoty podział (1:1,618; 38,2% / 61,8%; a:b = b:(a+b)) jako proporcja strony lub pola składu; po odjęciu kwadratu zostaje kolejny złoty prostokąt; złote prostokąty można „zawiesić” na stronie dowolnego formatu. | B 8.2, s. 155–160; L·Grid s. 176–177 | KONFLIKT K-05 |
| A-07 | makro | Proporcje formatu i pola składu | Złoty podział nie jest bardziej uzasadnioną podstawą proporcji niż inne metody (standardowy papier, połówki, kwadraty, liczby całkowite). | L·Grid s. 176 | KONFLIKT K-05 |
| A-08 | makro | Proporcje formatu i pola składu | Ilustracje współdecydują o formacie: strona nieco głębsza niż typowa ilustracja (miejsce na podpis); zdjęcia kwadratowe → 1:1,16; krajobrazowe 4×5 → 1:0,87; 35 mm → 1:0,83. | B 8.3.2, s. 161 |  |
| A-09 | makro | Proporcje formatu i pola składu | Proporcje stron i kolumn mają skojarzenia historyczne: długa linia egipska to nacisk na pisanie, nie czytanie; renesans 1:1,4–1:2; neoklasycyzm szerszy, ok. 1:1,3. | B 8.3.3, s. 161–162 |  |
| A-10 | makro | Proporcje formatu i pola składu | Pole składu równoważ i kontrastuj z kształtem strony: proporcje strony i pola mają różnić się wyraźnie i celowo (np. strona 1:1,62, pole 1:1,8); identyczne proporcje to „unison”, dopuszczalny, gdy zamierzony. | B 8.4.2, s. 163–164 |  |
| A-11 | makro | Proporcje formatu i pola składu | Tekst do czytania ciągłego ustawiaj w kolumnie wyraźnie wyższej niż szerokiej; bardzo wąskie i długie kolumny kojarzą się z prasą. | B 8.4.1, s. 163 |  |
| A-12 | makro | Proporcje formatu i pola składu | Idealny kwadrat tekstu na kwadratowej stronie z równymi marginesami nie ma punktów orientacyjnych; buduj nierówność (jedne przestrzenie wąskie, inne szerokie). | B 8.4.2, s. 163 |  |
| A-13 | makro | Proporcje formatu i pola składu | Pole składu umieszczaj wyżej i ku grzbietowi, nie na środku strony. | B 8.4.2, s. 164 |  |
| A-14 | makro | Proporcje formatu i pola składu | Wysokość pola składu jako całkowita liczba linii powiązana z marginesem grzbietowym (λ = s/3 → 27 linii; λ = s/4 → 36 linii). | B 8.7, s. 173 |  |
| A-15 | makro | Kanony konstrukcji strony i marginesy | Kanon średniowieczny (Tschichold 1955 wg Villarda de Honnecourt): strona 2:3, pole 2:3, s = w/9, t = h/9, e = 2s, f = 2t (marginesy s:t:e:f = 2:3:4:6); głębokość pola równa szerokości strony; przekątne przecinają się w 1/3 pola i strony. | B 8.7, s. 173 | Kanon Van de Graafa nie występuje w żadnej z książek; ta konstrukcja jest tam opisana pod innym nazwiskiem. Oznaczenie „t:e:f” z OCR |
| A-16 | makro | Kanony konstrukcji strony i marginesy | Aldus 1499: strona 2:3, pole 1:1,7 (wysoki pentagon), s = t = w/9, e = 2s. | B 8.7, s. 171 |  |
| A-17 | makro | Kanony konstrukcji strony i marginesy | Froissart 1559: strona złotego podziału, pole 1:1,87 (wysoki heksagon), s = w/9, t = s, e = 2s; kolumna boczna n = s, rynna ok. w/75; tekst 14 pt, notki boczne 12 pt italic. | B 8.7, s. 172 |  |
| A-18 | makro | Kanony konstrukcji strony i marginesy | Pole złotego podziału na stronie ISO (1:√2): s = t = w/9, e = f = 2s (marginesy 1:2 spinają pole i stronę); folio w górnym zewnętrznym marginesie lub pod dolnym narożnikiem pola; przy s = t = w/8 e = f = φs. | B 8.7, s. 175 |  |
| A-19 | makro | Kanony konstrukcji strony i marginesy | Pole 1:2 (podwójny kwadrat) na stronie 1:√2: s = w/12, f = 2t = h/9, e = w/3; szeroki margines zewnętrzny zostawiony na notatki. | B 8.7, s. 176 |  |
| A-20 | makro | Kanony konstrukcji strony i marginesy | Margines zewnętrzny szerszy od wewnętrznego (tradycja kodeksów: e = 2s); wyjątek: książka poezji z polem wyśrodkowanym (s = e = w/5, t = s/2). | B 8.7, s. 171–175 | KONFLIKT K-03 |
| A-21 | makro | Kanony konstrukcji strony i marginesy | Marginesy wewnętrzne rozkładówki szersze od zewnętrznych dają więcej otwartej przestrzeni przy grzbiecie (układ symetryczny); albo asymetrycznie: lewy margines zawsze szerszy niż prawy. | L·Grid s. 179 | KONFLIKT K-03 |
| A-22 | makro | Kanony konstrukcji strony i marginesy | Marginesy mają trzy zadania: spiąć pole składu ze stroną (i strony sąsiednie) siłą proporcji, oprawić pole zgodnie z jego formą, chronić je (miejsce na kciuki); to mniej więcej połowa charakteru strony. | B 8.5.1, s. 165 |  |
| A-23 | makro | Kanony konstrukcji strony i marginesy | Marginesy ustawiaj swobodnymi proporcjami, nie okrągłymi jednostkami; najpierw ustaw pole składu w przyrostach typograficznych, potem skoryguj marginesy. | B 8.8.2, s. 177–178 |  |
| A-24 | makro | Kanony konstrukcji strony i marginesy | Równe marginesy dookoła są ekonomiczne, ale mało interesujące; strona o polu kwadratowym i marginesach zmiennych. | L·Grid s. 178 |  |
| A-25 | makro | Kanony konstrukcji strony i marginesy | Układ planuj od zewnątrz do wewnątrz (format i marginesy, kolumna to reszta) albo od wewnątrz (marginesy zero, prowadnice i ramki na pustej stronie). | L·Grid s. 178 |  |
| A-26 | makro | Siatka modułowa i bazowa | Siatka jest regulatorem proporcji i programem: maksimum stałych, maksimum zmienności; elastyczny szkielet reagujący na treść i ramę (strona, ekran, okno), nie sztywna formuła. | L·Grid s. 151, 165 |  |
| A-27 | makro | Siatka modułowa i bazowa | Siatka kolumnowa: im więcej kolumn, tym większa elastyczność; element zajmuje jedną lub kilka kolumn; nie wszystko musi być wypełnione; strefy dla rodzajów treści. | L·Grid s. 180 |  |
| A-28 | makro | Siatka modułowa i bazowa | Siatka z linią zawieszenia (hang line, datum): pozioma linia, od której „wiszą” kolumny; górna strefa dla obrazów i podpisów. | L·Grid s. 181 |  |
| A-29 | makro | Siatka modułowa i bazowa | Siatka modułowa: kolumny i wiersze o spójnych podziałach; moduły rządzą rozmieszczeniem i kadrowaniem tekstu i obrazów (4 × 4, 6 × 6). | L·Grid s. 194–195 |  |
| A-30 | makro | Siatka modułowa i bazowa | Siatka bazowa: rozmiar i interlinia tekstu jako liczby całkowite (bez „auto”); liczbę modułów w pionie dobierz tak, by dzieliła liczbę linii w kolumnie (42 linie = 7 × 6); resztę pochłaniają marginesy górny i dolny. | L·Grid s. 198 |  |
| A-31 | makro | Siatka modułowa i bazowa | Style nagłówków, podtytułów i podpisów dobieraj z wielokrotności jednostki siatki bazowej (np. 18/24, 14/18, 8/12 przy bazie 12); w CSS line-height w podobnych przyrostach. | L·Grid s. 198–199; B 2.2.2, s. 37 |  |
| A-32 | makro | Siatka modułowa i bazowa | Układaj elementy względem siatki bazowej, ale jej nie forsuj: czasem układ działa lepiej po nadpisaniu siatki; pokazuj siatkę przy sprawdzaniu, wyłącz, gdy przeszkadza. | L·Grid s. 198 |  |
| A-33 | makro | Siatka modułowa i bazowa | Prawdziwa siatka pozwala komponentom „łamać siatkę” przez przekroczenie kilku kolumn; białe płaszczyzny podkreślają strukturę; siatka jako obraz tła pomaga kontrolować wyrównania. | L·Grid s. 191 |  |
| A-34 | makro | Siatka modułowa i bazowa | Skala modułowa do podziału strony: pola, kolumny i marginesy w jednostkach z jednej skali (np. strona 52 × 55 pc, marginesy 5, 5, 5 i 8 pc, pole kwadratowe 42 pc); skala oparta na dwóch proporcjach jest elastyczniejsza. | B 8.6.1, s. 166–169 |  |
| A-35 | makro | Siatka modułowa i bazowa | Dwa bloki tekstu różnych rozmiarów zestawione obok siebie wyrównaj na wspólnej linii bazowej (np. 14/18 obok 7/9); linie bazowe i wysokości x wyznaczają rzeczywiste krawędzie tekstu. | L·Letter s. 37 |  |
| A-36 | makro | Siatka modułowa i bazowa | Obrazy dopasowuj do modułów kolumn (zajmują jedną, dwie lub trzy strefy) i kadruj do modułu; tekst nie owija bloków zakotwiczonych w środku strony. | L·Grid s. 163, 167 |  |
| A-37 | makro | Siatka modułowa i bazowa | Zaczynaj od siatki i szkieletu stron (wireframe), dopiero potem kroje, hierarchia i style nawigacji. | L·Grid s. 192 |  |
| A-38 | makro | Kolumna główna i pomocnicze (marginalia) | Kolumna boczna na notatki (sidenotes) w marginesie zewnętrznym: może być bardzo wąska rynna (6–7 pt przy miarze 33,5 pc), jeśli różni się rozmiarem i krojem od tekstu głównego; zostaw szeroki margines zewnętrzny (e = w/3) na notatki. | B 8.7, s. 172, 176 |  |
| A-39 | makro | Kolumna główna i pomocnicze (marginalia) | Marginalia składaj krótkim wierszem ragged (nawet 12–15 znaków); na stronie lewej flush right, by przylegały do tekstu. | B 2.1.2, s. 27; 1.2.5, s. 23; L·Text s. 113, 115 |  |
| A-40 | makro | Kolumna główna i pomocnicze (marginalia) | Wiele kolumn, gdy tekst przekracza 500 słów na stronę, gdy elementów jest wiele lub gdy ilustracje towarzyszą tekstowi; kolumny prozy ciągłej jednakowej głębokości; różna głębokość dla krótkich tekstów i stron o więcej niż dwóch kolumnach. | B 2.2.3, s. 39; 2.2.2, s. 37; 2.4.9, s. 44 |  |
| A-41 | makro | Kolumna główna i pomocnicze (marginalia) | Rynny między kolumnami w stosunku do miary (g = m/20, w/75, s/4); różnica rozmiaru i kroju zapobiega pomyłkom nawet przy małej rynnie. | B 8.7, s. 172, 175–176 |  |
| A-42 | makro | Kolumna główna i pomocnicze (marginalia) | Przy wielu językach każdy język dostaje strefę proporcjonalną do tekstury pisma; teksty równoległe obok siebie (równość) lub plecami do siebie (odrębność). | B 1.2.3, s. 21–22; L·Grid s. 155 |  |
| A-43 | makro | Kolumna główna i pomocnicze (marginalia) | Siatka pięciokolumnowa: tekst główny w czterech kolumnach, mniejsze teksty w jednej; pull quote w ramce na dwie kolumny. | L·Grid s. 183, 187 |  |
| A-44 | makro | Rozkładówka i para stron | Książki i czasopisma projektuj jako rozkładówki: jednostką projektu jest para stron, a nie pojedyncza strona. | L·Grid s. 179 |  |
| A-45 | makro | Rozkładówka i para stron | Rozkładówka jest symetryczna poziomo (kierunek przewracania) i asymetryczna pionowo (pole składu wyżej i ku grzbietowi). | B 8.4.2, s. 164 |  |
| A-46 | makro | Rozkładówka i para stron | Rozkładówki ciągłego tekstu mają równą głębokość; nie powinny różnić się od sąsiednich o więcej niż jeden wiersz. | B 2.4.9, s. 44 |  |
| A-47 | makro | Rozkładówka i para stron | Wiersze na obu stronach rozkładówki i obu stronach kartki pokrywają się; skład sprawdza się pod światło (druk). | B 2.2.2, s. 37 |  |
| A-48 | makro | Folio, żywa pagina i nawigacja | Folio (numer strony) w dokumentach dłuższych niż dwie strony; miejsca: (1) góra, przy zewnętrznej krawędzi pola (z żywą paginą), (2) dół, przy zewnętrznej krawędzi, (3) górna ćwiartka zewnętrznego marginesu, (4) środek dołu (neoklasyczne, gorsze do nawigacji); nie w marginesie wewnętrznym. | B 8.5.3, s. 165 |  |
| A-49 | makro | Folio, żywa pagina i nawigacja | Folio w rozmiarze tekstu i blisko pola składu; dalej znika, wzmocnione rozprasza. | B 8.5.3, s. 166 |  |
| A-50 | makro | Folio, żywa pagina i nawigacja | Żywa pagina jest niezbędna w antologiach i opracowaniach, zbędna w tekstach o jednym głosie lub jednym temacie; wyróżnij ją od tekstu (spacjowane kapitaliki w rozmiarze tekstu lub drugi kolor). | B 8.5.4, s. 166; 1.2.2, s. 20 |  |
| A-51 | makro | Folio, żywa pagina i nawigacja | Nagłówki marginesowe (shoulderheads) wyróżniają bez powiększania. | B 4.2.1, s. 65 |  |
| A-52 | makro | Folio, żywa pagina i nawigacja | Wprowadź projekt do marginesów: wiszące numery, wcięcia, folia, żywe paginy, notki boczne wiążą stronę z polem; marginesy są interfejsem książki. | B 8.5.2, s. 165; L·Grid s. 153, 185 |  |
| A-53 | makro | Folio, żywa pagina i nawigacja | Elementy nawigacji dokumentu (numery stron, nagłówki, spis treści, indeks, przypisy, abstrakt) wyprowadzają czytelnika z jednokierunkowego strumienia. | L·Text s. 92 |  |
| A-54 | makro | Pusta przestrzeń | Pusta przestrzeń nadaje równowagę (poise): strona tytułowa z kilkoma liniami i wyważoną pustką; niektóre przestrzenie wąskie, inne szerokie, by dać orientację. | B 4.1.1, s. 61; 8.4.2, s. 163 | KONFLIKT K-04 |
| A-55 | makro | Pusta przestrzeń | Gęstość informacji zamiast pustki: jedna dobrze zorganizowana, gęsta powierzchnia bywa lepsza niż wiele rzadkich stron; „density is the new white space”. | L·Text s. 99; L·App s. 218 | KONFLIKT K-04 |
| A-56 | makro | Pusta przestrzeń | Sama pustka na początku rozdziału nie daje poczucia celebracji, a brak pustki nie jest ubóstwem (wąskie domy w górskich miasteczkach). | B 4.1.3, s. 62 |  |
| A-57 | makro | Rytm dokumentu | Wszystkie odstępstwa od tekstu (nagłówki, cytaty, przypisy, ilustracje) są synkopami wobec stałego rytmu linii i wracają „w fazie”; rytm dokumentu to powtarzalna interlinia, sinkage i moduł. | B 2.2.2, s. 37; 8.7, s. 173 |  |
| A-58 | makro | Elastyczność układu i zaokrąglenia | Projekt strony ma być na tyle giętki, by dać tekstowi „zamieszkalny dom”: tekstura tekstu ma pierwszeństwo przed czystością proporcji pojedynczej strony; sztywny układ o niezmiennej głębokości strony jest nieodpowiedni dla długiego dokumentu. | B 8.8.3, s. 178 |  |
| A-59 | makro | Elastyczność układu i zaokrąglenia | Nie wyrównuj głębokości stron zmianą interlinii (justowanie pionowe) ani rozpychaniem odstępów między akapitami; zmieniaj głębokość rozkładówek o jeden wiersz albo przeproporcjonuj element nietekstowy (ilustrację, sinkage). | B 8.8.3, s. 178; 2.4.9, s. 44 |  |
| A-60 | makro | Elastyczność układu i zaokrąglenia | Niezgodności między miarą optyczną a arytmetyczną (zaokrąglenia, centrowanie, łączenie proporcji) traktuj jako okazje do poprawy; sprawdzaj obliczenia na szkicu i szkic obliczeniami. | B 8.8.1, s. 177 |  |
| A-61 | makro | Ilustracje, podpisy i relacja do kolumny | Widoczne relacje między tekstem a innymi elementami (zdjęcia, podpisy, tabele, diagramy, przypisy) odzwierciedlają ich relacje rzeczywiste: notatki w marginesie, na dole, na końcu; zdjęcia w tekście lub w osobnej sekcji; podpisy blisko lub osobno. | B 1.2.3, s. 21–22 |  |
| A-62 | makro | Ilustracje, podpisy i relacja do kolumny | Podpis blisko ilustracji, gdy jest niezbędny do zrozumienia obrazu; gdy tylko dokumentacyjny, bliskość można poświęcić. | L·Text s. 130 |  |
| A-63 | makro | Ilustracje, podpisy i relacja do kolumny | W sieci reguły, ramki, nakładki i bloki koloru łączą obraz z podpisem w jedną całość. | L·Text s. 131 |  |
| A-64 | makro | Strona tytułowa, spisy i początki rozdziałów | Strona tytułowa wyraża godność tekstu: kilka linii u góry i u dołu, wyważona pustka między nimi; nie wrzucaj dużych gotowych liter w środek. | B 4.1.1, s. 61 |  |
| A-65 | makro | Strona tytułowa, spisy i początki rozdziałów | Tytuły nie przytłaczają tekstu: wystarczą spacjowane kapitaliki w rozmiarze i wadze tekstu; większe tytuły w wersji lekkiej, inline lub rastrowanej, nie ciężkiej. | B 4.1.2, s. 61–62 |  |
| A-66 | makro | Strona tytułowa, spisy i początki rozdziałów | Wyśrodkowanie jest tradycyjną formą stron tytułowych, zaproszeń, certyfikatów i tytułów. | L·Text s. 112, 114 |  |
| A-67 | makro | Strona tytułowa, spisy i początki rozdziałów | Początek rozdziału kształtuj tak, by przyczyniał się do całości projektu: renesans bez dodatkowej pustej przestrzeni; w nowoczesnych książkach 1/3 strony pustej nie wystarcza do uczczenia początku. | B 4.1.3, s. 62 |  |
| A-68 | makro | Strona tytułowa, spisy i początki rozdziałów | Spis treści: dwie kolumny (tytuł, numer) zestawione blisko siebie, bez dot leaders i dużych luk; pełny spis na osobnej stronie, nie na stronie praw autorskich. | B 2.1.10, s. 35; 4.5.2, s. 73 |  |
| A-69 | makro | Strona tytułowa, spisy i początki rozdziałów | Przed tekstem półtytuł (half-title); po tekście pusta karta lub strona; dedykacja nie wciśnięta na stronę praw autorskich; objętość w wielokrotnościach sygnatur (16 stron). | B 4.5.1–4.5.3, s. 72–73 |  |
| A-70 | makro | Strona tytułowa, spisy i początki rozdziałów | Zrównoważ front i back matter z tekstem (spis, listy ilustracji, podziękowania, przedmowa wobec dodatków, przypisów, bibliografii, indeksu, kolofonu); stos pustych kart na końcu świadczy o niedbałości. | B 4.5.3, s. 73 |  |
| A-71 | makro | Hierarchia nagłówków i struktura układu | Każda warstwa tekstu (tytuł rozdziału, nagłówki, cytaty, przypisy, listy) ma własną tożsamość typograficzną: spójną, odrębną i zwykle harmonijną z pozostałymi. | B 1.2.2, s. 20 |  |
| A-72 | makro | Hierarchia nagłówków i struktura układu | Używaj tylu poziomów nagłówków, ile potrzeba, nie więcej i nie mniej; poziomy oznaczaj A–F. | B 4.2.1–4.2.2, s. 65 |  |
| A-73 | makro | Hierarchia nagłówków i struktura układu | Wybierz dominującą formę nagłówków: symetryczną (crossheads) albo asymetryczną (sideheads); losowe mieszanie daje chaos; obca forma trafia na szczyt lub dół hierarchii. | B 4.2.1–4.2.2, s. 65 | KONFLIKT K-09 |
| A-74 | makro | Hierarchia nagłówków i struktura układu | Nagłówek jednowierszowy wyrównany do prawej wymaga dużego rozmiaru lub wagi; nagłówki można wynieść w całości do marginesu, żeby wyróżnić je bez powiększania. | B 4.2.1, s. 65 |  |
| A-75 | makro | Hierarchia nagłówków i struktura układu | Każdy poziom hierarchii sygnalizują jeden lub kilka sygnałów: przestrzenne (wcięcie, interlinia, położenie) lub graficzne (rozmiar, krój, kolor), stosowane spójnie; do trzech sygnałów na poziom. | L·Text s. 132 | KONFLIKT K-07 |
| A-76 | makro | Hierarchia nagłówków i struktura układu | Redundancja sygnałów bywa pożądana (wcięcie + łamanie wiersza), ale zbyt wiele sygnałów (wcięcie + odstęp między akapitami; bold + italic + podkreślenie) rozmywa kształt tekstu. | L·Text s. 127, 132 |  |
| A-77 | makro | Hierarchia nagłówków i struktura układu | Hierarchia jest relacyjna: nagłówek, podtytuły i tekst odróżniają się wzajemnie; wyraźny kontrast skali buduje hierarchię i głębię. | L·Text s. 133; L·Letter s. 42 |  |
| A-78 | makro | Hierarchia nagłówków i struktura układu | Mieszanie wyrównań (flush left, flush right, justowanie, wyśrodkowanie) tworzy dynamiczne układy; w projektach ekspresyjnych dopuszczalne. | L·Text s. 116–117 | KONFLIKT K-09 |
| W-01 | własne | Tabele i listy | Tabele redaguj i składaj jak tekst do czytania: nagłówki kolumn poziomo, litery nie za małe ani zbyt zwężone, minimum „mebli” (linie, ramki, kropki) i maksimum informacji. | B 4.4.1, s. 70 |  |
| W-02 | własne | Tabele i listy | Linie, tła i dzielniki biegną wzdłuż głównego kierunku czytania (w listach i indeksach pionowo, w pozostałych tabelach poziomo); brak linii na krawędzi tabeli; w tabeli wystarczająca ilość białej przestrzeni między kolumnami. | B 4.4.1, s. 70–71 |  |
| W-03 | własne | Tabele i listy | Listy porządkuj pozycją i punktowaniem (numery lub myślniki wiszące w marginesie, numery wyróżnione krojem), bez nadmiaru interpunkcji; kropki wiodące w tabelach rzadko korzystne. | B 4.4.2, s. 71 |  |
| W-04 | własne | Tabele i listy | Liczby w kolumnach wyrównuj do prawej lub do separatora dziesiętnego; odnośniki do liczb wieszaj po prawej, by nie zaburzały wyrównania. | B 4.4.3, s. 71–72 |  |
| W-05 | własne | Tabele i listy | Wyrównania w tabelach: pary (spis treści) — lewa kolumna flush right, prawa flush left; tabele finansowe — słowa po lewej, liczby w prawo lub dziesiętnie; unikaj wielu różnych wyrównań naraz. | B 4.4.4, s. 72 |  |
| W-06 | własne | Tabele i listy | Linie i ramki mają oświetlać relacje danych, a nie zamykać każdą komórkę w „więzieniu danych”; strukturę wyrażaj wyrównaniem samej typografii. | L·Grid s. 204 |  |
| W-07 | własne | Tabele i listy | Zamiast gęstych linii użyj bladego tła łączącego długie wiersze; liczby można zastąpić kropkami do porównań wzrokowych. | L·Grid s. 206 |  |
| W-08 | własne | Tabele i listy | Tabela jest strukturą danych (kolumny i wiersze), nie narzędziem układu strony; układ musi mieć sens po linearyzacji. | L·Grid s. 170–171 |  |
| W-09 | własne | Kolor tekstu i druku | „Kolor” strony to gęstość czerni, zależna od kroju, odstępów liter, wyrazów i linii (wszystkie współzależne); po spełnieniu wymogów czytelności dąż do równości koloru. | B 2.1 (wstęp), s. 25 |  |
| W-10 | własne | Kolor tekstu i druku | Drugi kolor (czerwień) służy fleuronom, inicjałom, wersalom i żywej paginie. | B 4.1.4, s. 63; 8.5.4, s. 166 |  |
| W-11 | własne | Kolor tekstu i druku | Duże litery o lekkim kolorze uzyskaj kolorem lub rastrem (tint, screening), a nie ciężarem kroju. | B 4.1.2, s. 62 |  |
| W-12 | własne | Kolor tekstu i druku | Odcień czerni dobieraj do papieru (czerwieńsza na kremowym, bliższa niebieskiej na szarym lub białym); farba tekstu na papierze powlekanym ma być mniej błyszcząca niż papier. | B 9.5.3, s. 195 |  |
| W-13 | własne | Kolor tekstu i druku | Ostry czarny tekst na białym tle czyta się z ekranu równie sprawnie jak z papieru. | L·Text s. 98 |  |
| W-14 | własne | Papier, technologia i format wydawniczy | Krój dobieraj do technologii, dla której powstał (letterpress, offset, ekran): cienkie kreski w offsecie chudną, w letterpressie pogrubiają. | B 6.1.1–6.1.2, s. 93 |  |
| W-15 | własne | Papier, technologia i format wydawniczy | Krój dobieraj do końcowych warunków druku i rozdzielczości: delikatne kroje przepadają, a mocne szeryfy, otwarte kontrzłobki i łagodne modelowanie przeżywają. | B 6.1.3, s. 94 |  |
| W-16 | własne | Papier, technologia i format wydawniczy | Krój i papier dobieraj do siebie: renesansowe i barokowe kroje do papieru szorstkiego, neoklasyczne do gładkiego; Futura i Helvetica znoszą oba. | B 6.1.4, s. 94–95 |  |
| W-17 | własne | Papier, technologia i format wydawniczy | Marginesy oblicza się po wyborze oprawy; zmiana formatu o 1/8 cala niszczy dokładnie wymierzoną stronę. | B 9.5.3, s. 195 |  |
| W-18 | własne | Papier, technologia i format wydawniczy | Sprawdzaj skład na każdym etapie (odbitka, film, płyta): kolor, ostrość i spójność liter; kontroluj siatkę (spójna interlinia, wyrównanie kolumn, pole składu nietrapezowe). | B 9.5.2, s. 194 |  |
| W-19 | własne | Papier, technologia i format wydawniczy | Format publikacji wynika z arkusza: 2:3 i 3:4 (średniowieczne arkusze, USA), 1:√2 (ISO); wymiary spoza standardu bywają nieekonomiczne, ale „organiczny” kształt strony wpływa na czytelnika. | B 8.1, s. 143–144; 8.3.1, s. 160 |  |
| W-20 | własne | Papier, technologia i format wydawniczy | Węższe strony wymagają miękkiego grzbietu; przy małych rozmiarach nadają się tylko do tekstu o wąskiej miarze. | B 8.3.2, s. 161 |  |
| W-21 | własne | Tradycja kroju i historia | Dobieraj krój o skojarzeniach historycznych zgodnych z tekstem (renesans do renesansu); unikaj anachronizmów (barokowy krój do tekstu renesansowego, neoklasyczny do XVII-wiecznej Francji). | B 6.3.1, s. 98–99 |  |
| W-22 | własne | Tradycja kroju i historia | Pozwól krojowi mówić jego idiomem: krój renesansowy żąda renesansowych proporcji strony i marginesów, braku bolda, dużych inicjałów, rozdzielenia romana i italica; krój neoklasyczny — neoklasycznej strony. | B 6.3.2, s. 99 |  |
| W-23 | własne | Tradycja kroju i historia | Krój dobieraj według pochodzenia i charakteru (kraj, epoka, wyznanie, płeć projektanta), nie według przypadkowego skojarzenia nazwy. | B 6.4.1, s. 99–102 |  |
| W-24 | własne | Tradycja kroju i historia | Cechy stylów: renesans — oś humanistyczna, umiarkowany kontrast, mała wysokość x; neoklasycyzm — oś pionowa, pochylenie italica 14–16°; romantyzm — wzmocniony kontrast i oś pionowa; pozwalają sprawdzić zgodność kroju z epoką. | B 7.2, s. 122–133 | Rozdz. 7 czytany wyrywkowo (listy cech) |
| W-25 | własne | Tradycja kroju i historia | Klasyfikacja krojów: humanistyczne (old style), przejściowe, nowoczesne (Bodoni, Didot), egipskie (slab), bezszeryfowe humanistyczne, przejściowe i geometryczne. | L·Letter s. 46 |  |
| W-26 | własne | Tradycja kroju i historia | Subtelna, niemal niedostrzegalna wariacja glifów (alternatywy kontekstowe wbudowane w font) ożywia stronę; mechaniczna powtarzalność daje „sterylną jednakowość”. | B 9.3.2, s. 188–190 |  |
| W-27 | własne | Ekran i render | Jeśli tekst czyta się z ekranu, projektuj dla ekranu: rozmiar, miara, interlinia, kształt wirtualnej strony, nagłówki, ilustracje, listy; wybór kroju może należeć do czytelnika. | B 9.5.1, s. 192–193 |  |
| W-28 | własne | Ekran i render | Dobre kroje ekranowe: niski kontrast, duży korpus (wysokość x), otwarte kontrzłobki, mocne zakończenia, szeryfy płytowe lub brak szeryfów; Verdana i Georgia (duży x-height, otwarte formy, luźne odstępy). | B 9.5.1, s. 193; L·Letter s. 72 |  |
| W-29 | własne | Ekran i render | Jeśli font źle wygląda w niskiej rozdzielczości, sprawdź hinting; silny antyaliasing rozmywa bardzo małe litery. | B 10.4.1, s. 207; L·Letter s. 73 |  |
| W-30 | własne | Ekran i render | Bitmapowy font pikselowy używaj w rozmiarze rdzeniowym lub w jego całkowitych wielokrotnościach (9 → 18 → 27 → 36). | L·Letter s. 74 |  |
| W-31 | własne | Ekran i render | @font-face wolno używać tylko dla krojów licencjonowanych do osadzania w sieci. | L·Letter s. 72, 82 |  |
| W-32 | własne | Ekran i render | Na ekranie przypisy, indeksy i nadpisy giną; zastępują je odsyłacze hipertekstu; wszystkie podteksty mają wtedy ten sam rozmiar. | B 9.5.1, s. 193 |  |
| W-33 | własne | Ekran i render | Czytelnik w sieci skanuje, a nie czyta; ikony nie zastępują tekstu, bo wymagają objaśnienia w wielu językach. | L·Text s. 97–99 |  |
| W-34 | własne | Ekran i render | W sieci myśl w stylach systemowo i globalnie: formę i treść oddziel (arkusze stylów), by treść można było przekształcać na różne urządzenia. | L·Text s. 98–99 |  |
| W-35 | własne | Struktura HTML i dostępność | Style nazywaj strukturalnie (tytuł, podtytuł, podpis), nie wizualnie; w HTML em, strong i p są strukturalne, i, b i br wizualne; jeden h1 w dokumencie; poziomy h1–h6 stosuj strukturalnie, nawet gdy wyglądają tak samo. | L·Text s. 135 |  |
| W-36 | własne | Struktura HTML i dostępność | Źródło HTML czytane liniowo ma sens i jest zbliżone do kolejności wizualnej; kotwica „przejdź do treści” przed powtarzaną nawigacją; teksty alternatywne obrazów. | L·Text s. 136–137 |  |
| W-37 | własne | Struktura HTML i dostępność | Nie używaj tabel do układu strony; układ liniowy ułatwia czytniki ekranu, urządzenia mobilne i przeglądarki tekstowe. | L·Grid s. 170–171; L·Text s. 136 |  |
| W-38 | własne | Struktura HTML i dostępność | Ten sam HTML może mieć różne arkusze stylów dla różnych urządzeń (układ komputerowy i mobilny). | L·Text s. 135 |  |
| W-39 | własne | Struktura HTML i dostępność | Mikrodane (tytuł strony, słowa kluczowe, teksty alt) umożliwiają przeszukiwanie, indeksowanie i oznaczanie treści. | L·Text s. 93 |  |
| W-40 | własne | Font jako artefakt | Przed modyfikacją fontu sprawdź licencję (EULA); bez zgody nie zmieniaj i nie dystrybuuj; legalnym obejściem jest nadpisanie kerningu zewnętrznym narzędziem. | B 10.1.1, s. 198; L·Letter s. 82 |  |
| W-41 | własne | Font jako artefakt | Nie poprawiaj w foncie tego, co nie jest zepsute; poprawki wykonaj raz, na stałe, w foncie, nie ręcznie w każdej linii. | B 10.2.1–10.2.2, s. 199 |  |
| W-42 | własne | Font jako artefakt | Stale potrzebne glify (cyfry tekstowe, ligatury ff, ffi, ffl, fj, pionowe nawiasy w italic) trzymaj w foncie bazowym, nie w osobnym foncie „expert”. | B 10.3.2, s. 201 |  |
| W-43 | własne | Font jako artefakt | Brakujące glify (litery wschodnioeuropejskie itp.) dorób; opisz je nazwą PostScript i numerem Unicode. | B 10.3.3, s. 201–202 |  |
| W-44 | własne | Font jako artefakt | Napraw wadliwe glify pomocnicze (znaki + ± × = • – — © @) zbyt duże, jasne, wysoko lub nisko osadzone, i diakrytyki źle narysowane lub osadzone. | B 10.3.1, s. 200 |  |
| W-45 | własne | Font jako artefakt | Tablicę kerningu sprawdzaj plikiem testowym (nazwy własne, diakrytyki, cudzysłowy, nawiasy, ułamki); pary typu Tp, f(, Ttanuu, y = j(x) zdarzają się w prawdziwych tekstach. | B 10.3.5, s. 203–206 |  |
| W-46 | własne | Font jako artefakt | Odstęp po f przed spacją nie może mieć 1/8–1/4 em (błąd kerningu w wielu fontach); spacja słowna kernowana tylko ułamkiem względem f. | B 10.3.6, s. 206–207 |  |
| W-47 | własne | Font jako artefakt | Funkcje OpenType działają tylko, gdy oprogramowanie je obsługuje; sprawdź, co font faktycznie zawiera (małe kapitaliki, cyfry, ligatury, alternatywy). | B 9.2, s. 183–184; L·Letter s. 80 |  |
| W-48 | własne | Font jako artefakt | Rodzina fontu: nazwy rodziny i stylów zgodne, aby roman, italic i bold były powiązane i przełączały się razem. | B 10.5, s. 208 |  |
| W-49 | własne | Font jako artefakt | Darmowe fonty bywają źle rozstawione i niekompletne; wiele jest pirackich; niektóre darmowe są rzetelne (OFL). | L·Letter s. 82 |  |
| W-50 | własne | Font jako artefakt | Dobry font to nie tylko kształty liter, lecz także poprawne wyrównanie glifów, spójne rozmiary, dokładne szerokości i czuły kerning. | B 9.6.2, s. 197 |  |
| W-51 | własne | Akcydens, ornament i tekst ekspresyjny | Ornamenty (fleurony, linie dekoracyjne) flagują początki tekstu i rozdzielają bloki; w wcięciach akapitów rzadko się sprawdzają. | B 4.1.4, s. 63; 2.3.2, s. 40; L·Letter s. 60 |  |
| W-52 | własne | Akcydens, ornament i tekst ekspresyjny | Ornament wynika ze struktury (echo struktury): moduły ornamentu składają się w większe formy według siatki. | L·Letter s. 60–63 |  |
| W-53 | własne | Akcydens, ornament i tekst ekspresyjny | Tekst pionowy: obróć linię zamiast układać litery jedna pod drugą; stos wersalików jest stabilniejszy niż małych liter i najlepiej wyśrodkowany; na grzbietach książek tekst od góry do dołu (USA). | L·Text s. 120 |  |
| W-54 | własne | Akcydens, ornament i tekst ekspresyjny | Odstępy, rozmiar i położenie liter mogą wyrażać znaczenie słowa (ekspresja przestrzenna) w tytułach, logotypach i plakatach. | L·Text s. 106 |  |
| W-55 | własne | Akcydens, ornament i tekst ekspresyjny | Logotypy, nazwy marek i prośby autorów o szczególne traktowanie liter nie zmieniają zasad składu: typografia traktuje wszystkie teksty jednakowo (akronimy i nazwy składaj według mowy, nie według życzenia właściciela). | B 3.2.3, s. 49 |  |
| W-56 | własne | Proces i redakcja | Przed składem oczyść tekst: usuń podwójne spacje, zamień proste cudzysłowy na typograficzne, a podwójne łączniki na pauzy; spacje nie służą do wcięć. | L·App s. 210, 213, 215 |  |
| W-57 | własne | Proces i redakcja | Brak silnej koncepcji maskują ozdobniki (gradienty, cienie, przezroczystość); pomysł prowadzi decyzje o kolorze, układzie, kroju i formacie. | L·App s. 218–219 |  |

## Konflikty (obie strony zostawione, bez rozstrzygnięcia)

| ID | Temat | Stanowiska | Wiersze |
|---|---|---|---|
| K-01 | Wtrącenia: półpauza ze spacjami czy pauza bez spacji | Bringhurst 5.2.1: półpauza ze zwykłą spacją po obu stronach; pauza em „wiktoriańsko” za długa. Lupton (dodatek, s. 210–211): pauza em, bez spacji wokół. | M-94, M-95 |
| K-02 | Odstęp między akapitami | Bringhurst 2.3.2: akapit blokowy rozdzielony pełną białą linią (w długich tekstach „bezduszny”); 2.2.2 wymaga odstępów będących wielokrotnością interlinii. Lupton s. 126–127: pełna pusta linia daje zbyt otwarty efekt i marnuje miejsce; stosuj precyzyjny przyrost (space after); wcięcie i odstęp razem to „type crime”. | M-130, M-131 |
| K-03 | Marginesy wewnętrzne a zewnętrzne | Bringhurst 8.7 (kanon średniowieczny, Aldus, Froissart, ISO): margines wewnętrzny (s) mniejszy od zewnętrznego (e = 2s) jako tradycja. Lupton s. 179: w przykładzie rozkładówki marginesy wewnętrzne szersze od zewnętrznych, by dać przestrzeń przy grzbiecie. | A-20, A-21 |
| K-04 | Pusta przestrzeń a gęstość | Bringhurst 4.1.1, 8.4.2: spokój i „poise” bierze się z białej przestrzeni. Lupton s. 99, 218: biała przestrzeń to modernistyczny mit; gęstość informacji (Tufte) bywa lepsza niż rzadkie strony. | A-54, A-55 |
| K-05 | Złoty podział jako podstawa proporcji | Bringhurst 8.2: złoty podział jako wyróżniona, „organiczna” proporcja strony i pola (obok innych kanonów). Lupton s. 176: nie jest bardziej uzasadniony niż inne metody (papier standardowy, połówki, kwadraty, liczby całkowite). | A-06, A-07 |
| K-06 | Dopasowywanie wierszy justowanych | Bringhurst 2.4 (wstęp): żadne oprogramowanie nie powinno automatycznie ściskać, rozciągać ani spacjować tekstu w celu dopasowania. Bringhurst 9.4.1: najlepsza justyfikacja koryguje odstępy między znakami (±3%) i szerokość glifów (±2%). Lupton s. 112: ujemny tracking pomaga zmieścić znaki, dodatni wyrównuje zbyt luźne wiersze. | M-71, M-72, M-73 |
| K-07 | Ile sygnałów na jedną zmianę | Bringhurst 3.5.1: zmieniaj jeden parametr na raz. Lupton s. 132: do trzech sygnałów na poziom lub przerwę w dokumencie. | M-21, A-75 |
| K-08 | Cudzysłowy zależne od języka | Bringhurst 5.4.1–5.4.2: brytyjskie pojedyncze w podwójnych vs amerykańskie podwójne w pojedynczych; pozycja interpunkcji wewnątrz lub na zewnątrz zależy od tradycji. Książki nie omawiają polskich cudzysłowów „…” (wymóg zadania). | M-104 |
| K-09 | Mieszanie form wyrównania i nagłówków | Bringhurst 4.2.2: wybierz dominującą formę nagłówków (symetryczną lub asymetryczną); losowe mieszanie prowadzi do chaosu. Lupton s. 116–117: łączenie różnych wyrównań daje dynamiczne i zaskakujące układy. | A-73, A-78 |

Do Etapu 2 trafiają także zagadnienia, które nie są konfliktem między książkami, ale wymagają decyzji: terminologia wdowa/sierota (M, grupa „Wdowy i sieroty”), polskie reguły niełamliwości i cudzysłowów (spoza książek).

## Pominięte jako ogólniki lub niesprawdzalne na stronie

- B 1.1.1–1.1.3, 1.2.1, 1.2.6, 1.3: zasady nadrzędne (typografia honoruje treść, czytaj tekst przed projektowaniem, dbaj o szczegóły, służ czytelnikowi) bez sprawdzalnego kryterium.
- B 2.4.11: „porzuć każdą zasadę, która nie służy tekstowi”; B 8.8.1: „improwizuj i licz” (zachowano tylko część o zaokrągleniach, A grupa „Elastyczność układu”).
- B 9.6.1–9.6.2, 10.2.3, 10.2.4: o pielęgnowaniu rzemiosła i hierarchii priorytetów (tekst, litery, projektant, odlewnia).
- B rozdz. 7 (poza listą cech stylów): historia stylów i technologii składu; B rozdz. 11 (kroje, s. 209–287): przegląd krojów; B dodatki A, C–E: tablice znaków, słownik pojęć, projektanci, odlewnie.
- B 6.7 (nowe ortografie): zachowano jako pojedynczy wiersz; nie dotyczy polskiego.
- Zasady procesowe, nieweryfikowalne na stronie (przebieg redakcji, korekta, dostarczanie tekstu autorom): L s. 212–217; zachowano tylko oczyszczanie tekstu przed składem (W, „Proces i redakcja”).
- L s. 10–35 (historia pisma i krojów), s. 64–71 (lettering, logotypy), s. 76–79 (projektowanie fontów), s. 87–101 (esej o tekście, autorstwie i liniowości; zachowano tylko wnioski o ekranie), s. 106–107 i 118–119, 144–147, 202–203, 206 (ćwiczenia), s. 212–217 (korekta, symbole redakcyjne), s. 219 (rady ogólne), s. 220–224 (bibliografia, indeks).

## Grupy dodane ponad przykłady z polecenia

Po drugim przejściu („czego te tematy nie obejmują?”) dopisano:
- **mikro**: Liczby, daty i jednostki; Niełamliwość i spacje twarde; Kerning i odstępy międzyliterowe; Wyróżnienia i emfaza; Akapity i cytaty blokowe; Znaki, diakrytyki i język; Wielojęzyczność i alfabety.
- **makro**: Elastyczność układu i zaokrąglenia.
- **własne**: Ekran i render; Struktura HTML i dostępność; Font jako artefakt; Proces i redakcja.

Przykłady z polecenia „kanony konstrukcji strony” i „stosunki marginesów” zapisano w jednej grupie („Kanony konstrukcji strony i marginesy”), a „symetrię i asymetrię” w grupach „Rozkładówka i para stron” i „Kanony…”, bo źródła podają je łącznie.

## Zakres odczytu i ograniczenia

- Oba PDF mają warstwę tekstową. Lupton (InDesign): tekst czysty. Bringhurst: warstwa pochodzi z OCR (Paper Capture), więc zdarzają się błędy w znakach specjalnych, ułamkach i diakrytykach oraz uszkodzone tabele liczbowe.
- Nieczytelne w Bringhurście: tabela liczby znaków w wierszu (s. 29), tabele proporcji stron i kolumn (s. 148–149), pierwszy ciąg rozmiarów (s. 157), wzory na s. 182. Trzy pierwsze odtworzono w osobnym pliku [bringhurst-tabele.md](bringhurst-tabele.md) z oznaczeniem pochodzenia każdej wartości (OCR, obliczenie, wnioskowanie); to rekonstrukcja, nie transkrypcja. Wzorów z s. 182 nie odtwarzano.
- Bringhurst, przeczytane w całości lub w całości istotnych fragmentów: rozdz. 1–6 (s. 17–118), rozdz. 8 (s. 143–178), rozdz. 9 i 10 (s. 179–208), dodatek B (s. 301–320). Rozdz. 7 (s. 119–142) przejrzany wyrywkowo: listy cech stylów (s. 122–136). Rozdz. 11 (s. 209–287), dodatki A, C, D, E (s. 288–300, 321–356), bibliografia i indeks: nie czytane szczegółowo.
- Lupton, przeczytane: s. 36–63 (Letter bez historii), s. 72–83, s. 84–147 (Text), s. 148–207 (Grid; powtarzający się tekst próbny pominięto), s. 208–219 (Appendix). Pominięte lub tylko przejrzane: s. 10–35, 64–71, 76–79 (zob. wyżej).
- Kanon strony Van de Graafa (podany w poleceniu) nie występuje w żadnej z książek; Bringhurst na s. 173 opisuje identyczną konstrukcję 2:3 z marginesami s = w/9, t = h/9, e = 2s, f = 2t jako układ Tschicholda (1955) wg Villarda de Honnecourt (A, grupa „Kanony konstrukcji strony i marginesy”). Nie przypisano go więc Van de Graafowi.
- Zasady są parafrazami z książek, z numerami stron; w cudzysłowach stoją tylko krótkie terminy i określenia autorów (np. „type crime”, „poise”). Zasada o spójnikach jednoliterowych, polskie cudzysłowy i półpauza w zakresach wynikają z wymagań zadania, nie z książek (zaznaczone w odpowiednich wierszach).
- Nie sprawdzano zgodności przeglądarek ani wykonalności w CSS; wzmianki „Odpowiednik: …” to jedynie podpowiedzi na Etap 2.
