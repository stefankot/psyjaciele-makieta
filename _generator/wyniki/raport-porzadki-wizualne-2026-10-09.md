# Raport: porządki wizualne makiety (9.10.2026)

Zakres: Home, hub usług, 14 podstron usług, zespół, polityka prywatności (18 stron) × 1710, 1440, 1280, 1000, 390 px = 90 pomiarów przed i po.
Narzędzie: `_generator/narzedzia/pomiar.py` + `pomiar_analiza.py` (Playwright, Chrome). Serwer: `http://127.0.0.1:8766/`.
Wykluczone z reguł (świadomie): ilustracje w sekcjach Home, ilustracje hero, pełnoszerokie tła sekcji i zdjęcia „booking”/„social-promo”, menu rozwijane, nakładki (K, I), nagłówek strony na desktopie (pełna szerokość wg `nowa-bar.css`).

## Wynik pomiaru (przed → po)

| Kategoria | przed | po |
|---|---|---|
| Poziome przewijanie (strona × szerokość) | 2 | 0 |
| Odpowiedzi 404 | 100 | 0 |
| Wpisy w konsoli (błędy/ostrzeżenia) | 104 | 0 |
| Tekst poza własnym boxem lub oknem | 7 | 0 |
| Kontrast poniżej progu (bez fałszywych alarmów) | 16 | 0 |
| Odstępy i interlinie poza rytmem 8 px | 553 | 1 (padding-left 215 px = margines siatki w „booking”) |
| Bloki poza siatką 12 kol. @1710 / 1440 / 1280 | 50 / 50 / 50 | 0 / 0 / 0 |
| Bloki poza siatką @1000 | 108 | 3 (miara tekstu: lista, kolumna kontaktu) |
| Bloki poza siatką @390 | 55 | 0 (poza ilustracjami kafli Home, celowo wychodzącymi poza ekran) |
| Jednoliterowy spójnik na końcu wiersza (pomiar bezpośredni) | 633 (heurystyka) | 0 |
| Krótki ostatni wiersz w akapitach ≥ 3 wierszy @1440 / @390 | 59 / 132 | 29 / 43 |
| Pauza na początku wiersza (pomiar bezpośredni) | — | 1 widoczna (zespół @390) + 6 w ukrytej liście kroków |

## Problem → miejsce → poprawka

Adres bazowy: `http://127.0.0.1:8766/`. Wszystko lokalnie, bez commitu.

| # | Problem | Miejsce | Poprawka |
|---|---|---|---|
| 1 | Zespół na Home: osoby bez komórek, trzy kolumny po 427 px bez odstępu (poza siatką); tło „akcentowe” niewidoczne, bo `.person` zamienia `--surface` i `--accent` | `index.html#zespol` | Trzy osoby w rzędzie, kwadrat 4 kolumny (405,3 px, odstęp 32 px, x = 80 / 517,3 / 954,7) w kolorze akcentowym; nakładka linii na hoverze i fokusie dynamiczny kontur sylwetki (`team-echo.js`, kolor `--team-overlay-ink`, domyślnie `--accent`); podpisy od lewej krawędzi komórki; poniżej 560 px jedna osoba w rzędzie |
| 2 | Strzałki w linkach za nisko (uwaga z inspektora): środek strzałki na linii bazowej, ok. 5 px niżej niż środek liter | `index.html#pytania`, też `#dojazd`, `#nagle-przypadki` (Wyznacz trasę) | Pusty `.type-arrow-glyph` w ikonie tworzył wewnętrzny wiersz tekstu i przesuwał linię bazową ikony; `display:none` w `ikony.py` (reguła na wszystkie ikony-strzałki); środek strzałki 5,3–6,2 px nad linią bazową |
| 3 | `/favicon.ico` → 404 na każdej stronie | wszystkie strony | `<link rel="icon" href="data:,">` w `index.html` i `build.py` |
| 4 | 20 żądań 404 przy sondowaniu 10 brakujących obrazów (placeholdery) | [nefrologia](http://127.0.0.1:8766/uslugi-weterynaryjne/nefrologia-weterynaryjna/index.html#przewlekla-choroba-nerek-pchn), [ciśnienie](http://127.0.0.1:8766/uslugi-weterynaryjne/pomiar-cisnienia-psow-i-kotow/index.html#jak-przygotowac-zwierze-do-pomiaru), [paszporty](http://127.0.0.1:8766/uslugi-weterynaryjne/wystawianie-paszportow-psom-i-kotom/index.html#jak-przebiega-wizyta-w-sprawie-paszportu), [dermatologia](http://127.0.0.1:8766/uslugi-weterynaryjne/dermatologia-weterynaryjna/index.html#najczestsze-problemy-skorne-psow-i-kotow), [urologia](http://127.0.0.1:8766/uslugi-weterynaryjne/urologia-weterynaryjna/index.html#jak-wyglada-diagnostyka), [chirurgia](http://127.0.0.1:8766/uslugi-weterynaryjne/chirurgia-weterynaryjna-tkanek-miekkich/index.html#dlaczego-przygotowanie-zwierzecia-do-zabiegu-jest-wazne) | `bloki.py` sprawdza plik na dysku: jest → `data-src` (AVIF, jeśli istnieje), brak → `data-brak` bez sondowania; `podstrony.js` nie próbuje nieistniejących. Po dodaniu pliku trzeba uruchomić `build.py` |
| 5 | Poziome przewijanie przy 390 px: status w bloku alarmowym jako przedłużenie przycisku wystawał (483 > 390) | [choroby wewnętrzne](http://127.0.0.1:8766/uslugi-weterynaryjne/choroby-wewnetrzne-u-psow-i-kotow/index.html#kiedy-nie-czekac-na-wolny-termin), [dermatologia](http://127.0.0.1:8766/uslugi-weterynaryjne/dermatologia-weterynaryjna/index.html#objawy-z-ktorymi-warto-przyjsc), [stomatologia](http://127.0.0.1:8766/uslugi-weterynaryjne/stomatologia-weterynaryjna/index.html#objawy-ktorych-nie-warto-przeczekac) | `podstrony.css`: ≤ 700 px status pod przyciskiem (jak w hero) |
| 6 | Poziome przewijanie 403 > 390: imię „Aleksandra” (Rialto) ucięte w połowie szerokości | [USG](http://127.0.0.1:8766/uslugi-weterynaryjne/diagnostyka-obrazowa-psow-i-kotow/index.html#kto-przyjmuje) i inne „Kto przyjmuje” | `layout-nowa.css`: ≤ 560 px jedna osoba w rzędzie (Home i podstrony) |
| 7 | Tytuł z długim słowem wychodzi 15 px poza kolumnę (357 > 342) | [szczepienia](http://127.0.0.1:8766/uslugi-weterynaryjne/szczepienia-oraz-profilaktyka-przeciwpasozytnicza/index.html#tytul-strony) | ≤ 700 px: `hyphens:auto` dla h1/h2, tylko słowa ≥ 14 liter |
| 8 | Sierotki: 633 jednoliterowych spójników (a, i, o, u, w, z) na końcu wiersza | wszystkie strony | Nowy `nbsp.py` (w `build.py`, jednorazowo na `index.html`): twarda spacja po spójniku i przed pauzą |
| 9 | Osierocone ostatnie wiersze | wszystkie strony | `text-wrap: pretty` (akapity, listy, podpisy), `balance` (h3, h4, th, summary); krótki ostatni wiersz 59 → 29 (1440), 132 → 43 (390) |
| 10 | Kontrast 1,09∶1: opis w panelu „Poza godzinami pracy” (jasny tekst na jasnym tle, bo globalna reguła `--small-ink` przebijała kolor panelu) | `index.html#nagle-przypadki` | `layout-nowa.css`: opis i h3 w nagłówku panelu w `--surface` |
| 11 | Ta sama relacja miała różne odstępy: nagłówek → tabela 32 / 64 / 88 px, podrozdział po bloku 88 / 64 / 32 px (stary styl Home `gap: 88px` działał też na podstronach przez klasy palety) | [kardiologia](http://127.0.0.1:8766/uslugi-weterynaryjne/kardiologia-weterynaryjna/index.html#najczestsze-choroby-serca-u-psow), [interna](http://127.0.0.1:8766/uslugi-weterynaryjne/choroby-wewnetrzne-u-psow-i-kotow/index.html#czym-zajmuje-sie-interna), [szczepienia](http://127.0.0.1:8766/uslugi-weterynaryjne/szczepienia-oraz-profilaktyka-przeciwpasozytnicza/index.html#szczepienia-psow-i-kotow), [hub](http://127.0.0.1:8766/uslugi-weterynaryjne/index.html#leczenie-i-profilaktyka) | `podstrony.css`: stos sekcji `--group-gap` (64 / 48 / 32 wg szerokości); nagłówek → tabela/akapit i podrozdział po bloku = 32 px; po poprawce jedna wartość na każdą parę |
| 12 | Interlinie i odstępy poza 8 px (553 miejsc): stopka h2 24,8; kafle usług 24,8 i 44,6; tytuły sekcji Home 51,8–77,8 (inline z `fitTitles()`); hero lead 25,6; specjalizacje 6 px | stopka każdej strony, `index.html#uslugi`, `#onas`, [hero interny](http://127.0.0.1:8766/uslugi-weterynaryjne/choroby-wewnetrzne-u-psow-i-kotow/index.html#poczatek) | Reguły z `round()` w `layout-nowa.css` i `podstrony.css`; `!important` przebija inline z `minimal-nowa.js` |
| 13 | „Kolejne usługi”: 3 kafle po 260 px poza siatką, czwarty osierocony | `#zobacz-tez` na 14 podstronach, np. [kardiologia](http://127.0.0.1:8766/uslugi-weterynaryjne/kardiologia-weterynaryjna/index.html#zobacz-tez) | Dwie kolumny po 4 kolumny siatki (405,3 px; x = 517,3 / 954,7) |
| 14 | Tabele, listy i h2 na polityce 745 px (66ch) zamiast 8 kolumn | [polityka](http://127.0.0.1:8766/polityka-prywatnosci/index.html#postanowienia-ogolne) | `.legal-prose` bez `max-inline-size`; miarę tekstu trzyma akapit |
| 15 | Zepsuta kotwica: „Otwarte teraz” na polityce → `#kontakt` (nie ma na stronie), bo `layout-status.js` nadpisywał adres z generatora; to samo w trybie „zamknięte” (`#after-hours-title` jest na 7 z 18 stron) | [polityka](http://127.0.0.1:8766/polityka-prywatnosci/index.html#poczatek) | `layout-status.js`: cel musi istnieć, inaczej adres z generatora (`../index.html#kontakt`) |
| 16 | Hub usług przy 390: ilustracje kafli 234 px w kolumnie 164 px, ucięte i nachodzące na sąsiednią kolumnę | [hub](http://127.0.0.1:8766/uslugi-weterynaryjne/index.html#uslugi-skrot) | `podstrony.css`: rysunek na 100 % kolumny |
| 17 | Kafle usług i kolumny „Przychodnia” przy 1000 px z odstępem 32 px zamiast rynny 24 px | `index.html#uslugi`, `#przychodnia` | `column-gap: var(--gap)` |
| 18 | „O nas”: opis 474 px (42ch) poza siatką | `index.html#onas` | 6 kolumn, szerokość i oś portretu (≥ 1001 px) |
| 19 | Zdjęcia profili 200 px poza siatką | [zespół](http://127.0.0.1:8766/zespol/index.html#Magda) | 3 kolumny (212 px przy 1000), 6 kolumn (163 px przy 390) |
| 20 | Podpisy pod portretami wcięte o 16–24 px od krawędzi kolumny | Home `#zespol`, „Kto przyjmuje” na podstronach | `padding-inline: 0` |
| 21 | Dzielenie wyrazów (na Twoją prośbę „rozszerz”): było wyłączone wszędzie (`p{hyphens:manual}` przesłaniało `.book-prose`) | wszystkie strony | `hyphens:auto` w akapitach, listach, podpisach (słowa ≥ 7 liter, min. 3 litery przed/po, najwyżej 2 kolejne wiersze); bez tabel, `.psy`, e-maili (`<span class="nohy">`), telefonów |
| 22 | Nagłówek podstron różnił się od Home po prawej (dane kontaktowe przesunięte na oś 7, strzałka „Umów wizytę” ukryta przy 1440–1599 px, inne odstępy) | wszystkie podstrony, np. [kardiologia](http://127.0.0.1:8766/uslugi-weterynaryjne/kardiologia-weterynaryjna/index.html#poczatek) | `podstrony.css`: usunięte nadpisania nagłówka; pomiar pozycji elementów nagłówka Home vs podstrona: 0 różnic przy 1710, 1440, 1280, 1000, 390 px; nagłówek zostaje pełnej szerokości |
| 23 | Podpisy opinii na podstronach pismem Satoshi, na Home Rialto (uwaga z inspektora) | [zespół](http://127.0.0.1:8766/zespol/index.html#section-title-6), [hub](http://127.0.0.1:8766/uslugi-weterynaryjne/index.html#section-title-6), interna, szczepienia | `podstrony.css`: `.review-author` w Rialto (na podstronach token `--font-emphasis` to Satoshi) |
| 24 | Hub usług: ilustracje kafli bez filtra koloru (czarne linie, białe tło), tytuły w rzędzie na różnej wysokości (kafle 1 i 3 miały proporcję 1∶1) | [hub](http://127.0.0.1:8766/uslugi-weterynaryjne/index.html#uslugi-skrot) | generator wstawia definicje filtrów `service-light-ink`, `service-hover-ink`, `thick-2` z Home; jedna proporcja 1,2∶1; tytuły na jednej linii we wszystkich rzędach |
| 25 | Podkreślenie linku obejmowało spację przed strzałką | [Home #pytania](http://127.0.0.1:8766/index.html#pytania), „Wyznacz trasę” w [#nagle-przypadki](http://127.0.0.1:8766/index.html#nagle-przypadki) | `nbsp.py` usuwa spację przed strzałką (klasa `is-after-text`), odstęp robi margines 0,5 em; strzałka dalej 5,3–6,2 px nad linią bazową |
| 26 | Stopka: nawigacja inna niż w rozwijanym menu, tekst pod logo szeroki, lista zespołu z awatarami | [Home](http://127.0.0.1:8766/index.html#kontakt) i wszystkie podstrony | trzy kolumny linków (Usługi, Zespół, Na stronie + Śledź nas) skopiowane z menu na kolumnach 7–12 (po 2 kolumny, 186,7 px); logo i tekst pod logo na 4 kolumnach (405,3 px; poniżej 1000 px logo 4 z 12, tekst 8); lista zespołu usunięta; tekst marki 16/24 px z odstępem 56 od logo; nagłówki kolumn Rialto także na podstronach; stopka Home = stopka podstrony (0 różnic) |
| 27 | „Kto przyjmuje” na podstronach: komórki niewidoczne (zamienione `--surface`/`--accent`) | [USG](http://127.0.0.1:8766/uslugi-weterynaryjne/diagnostyka-obrazowa-psow-i-kotow/index.html#kto-przyjmuje) | te same komórki co na Home: 2 w rzędzie (2 × 4 kolumny, 405,3 px), akcent sekcji, ta sama nakładka hover |
| 28 | Hover kart zespołu: dynamiczny obrys sylwetki (prośba) | [Home #zespol](http://127.0.0.1:8766/index.html#zespol), „Kto przyjmuje” | nowy `team-echo.js`: pole odległości z kanału alfa zdjęcia + canvas; linie 3 px co 15 px w pętli na zewnątrz, 11 px/s (po uwadze: 2× wolniej i rzadziej); kolor `--accent`; 60 fps (121 klatek w 2 s przy DPR 1 i 2); statyczna nakładka SVG usunięta |

## Czego nie sprawdzałem

- Safari i Firefox: `round()`, `text-wrap: pretty`, `hyphenate-limit-*` są w nich nowsze lub częściowe; w starszych zostają stare wartości.
- Szerokości inne niż 1710, 1440, 1280, 1000, 390; 320 px i układ poziomy telefonu.
- Menu rozwijane, nakładki K i I, stany hover/fokus poza kartami zespołu, animacje startowe Home.
- Kontrast dla palet z nakładki K i dla tekstu na zdjęciach/ilustracjach; sprawdzone tylko bieżące palety sekcji.
- Pozycja ikon poza strzałkami w linkach (pomiar pikselowy tylko strzałek).
- Linki zewnętrzne (Wettermin, Google, Facebook itd.), jakość i waga obrazów.

## Decyzje właściciela uwzględnione
Kolor nakładki `--accent`; nagłówek pełnej szerokości, na podstronach jak na Home; logo w stopce 4 kolumny; ilustracje kafli na telefonie, puste komórki tabel i dzielenie wyrazów bez zmian (zostaje włączone); komórki „Kto przyjmuje” jak na Home; spacja przed strzałką poza podkreśleniem; „Nagłe przypadki” dodane do stopki (kolumna „Na stronie”, po „Opinie”); animacja hovera 2× wolniejsza i linie co 15 px; statyczna nakładka (SVG) usunięta; nagłówki kolumn stopki w Rialto także na podstronach; zdjęcia z Home (zespół, założycielki, pies i kot) zostają, kolaż pacjentów bez zmian.

## Pytania do właściciela (otwarte)
1. Kolaż pacjentów (baner „Praca”) zostawiam bez zmian, bo nie wymieniłeś go na liście zostających. Wymienić go na nowy?
2. Klucz Gemini do generowania 45 zdjęć nadal czeka na restart connectora (patrz wcześniejsza wiadomość).
