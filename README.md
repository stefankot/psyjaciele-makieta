# Makieta strony Psyjaciele (Warszawa Gocław)

Statyczna makieta bez budowania: otwieraj przez lokalny serwer, nie przez `file://`
(przeglądarka blokuje wtedy czcionki i maski SVG).

```
cd makieta
python3 -m http.server 8765
# http://127.0.0.1:8765/
```

## Struktura

```
makieta/
├── index.html                  strona główna (dawny layout-warianty/index-nowa.html)
├── uslugi-weterynaryjne/       hub usług + 14 podstron usług  (generowane)
├── zespol/                     zespół                          (generowane)
├── polityka-prywatnosci/       polityka prywatności            (generowane)
│
├── minimal.css, typography-book.css, animacje.css, section-headings.css,
│   design-tokens.css, palety-zestawy.css, layout-editorial.css, social-promo.css,
│   zespol-rejestr.css, zespol-stopka.css      style bazowe strony głównej
├── nowa-bar.css, layout-nowa.css              warstwa „nowa” (nagłówek, hero, układ sekcji)
├── podstrony.css, podstrony.js                style i skrypty wyłącznie podstron
├── minimal-nowa.js, nowa-header.js, nowa-readability.js, layout-status.js,
│   pet-photos.js, animacje.js, illustration-motion.js      skrypty strony głównej
├── assets/                     obrazy, czcionki, kształty (wspólne dla wszystkich stron)
│
├── _generator/                 wszystko, co buduje podstrony
│   ├── narzedzia/              build.py, checks.py, audit.py, … (Python + bs4)
│   ├── tresci-podstron/        źródła tekstów (czyste/<slug>.html)
│   ├── dokumentacja/           prompty i opisy zasad
│   └── wyniki/                 raporty, manifest obrazów, zrzuty, katalog podstron
├── wordpress/                  materiały do migracji (bez zmian)
└── _archiwum/                  stare wersje; nic stąd nie jest używane przez stronę
```

## Zasada źródeł

- **Strona główna** to `index.html`. Edytujesz ją ręcznie.
- **Podstrony** nie są edytowane ręcznie: powstają z `index.html` (nagłówek, rezerwacja, stopka)
  i z `_generator/tresci-podstron/czyste/*.html` (teksty). Zmiana w Home dociera do podstron po `build.py`.
- Wygląd podstron: `podstrony.css`; zachowanie: `podstrony.js`. Po zmianie podbij `CSS_V` / `JS_V`
  w `_generator/narzedzia/build.py`.

## Dodatki generatora
- `psy.py`: owija słowo „Psyjaciele” (i formy) w `<span class="psy">`; styl `.psy` (Rialto, 1,41 em) w `layout-nowa.css`. Ten sam skrypt na Home: `python3 _generator/narzedzia/psy.py index.html`.
- `nbsp.py`: twarda spacja po jednoliterowych spójnikach (a, i, o, u, w, z) i przed pauzą; adresy e-mail w tekście dostają `<span class="nohy">` (bez dzielenia wyrazów). Uruchamiany w `build.py`; na Home po ręcznych zmianach tekstu: `python3 _generator/narzedzia/nbsp.py index.html`.
- `infografiki.py`: infografiki wstawiane po nagłówkach wskazanych sekcji (lista `PLAN`); style `.info-*` w `podstrony.css`. Skala ciśnienia to restyl istniejącego bloku `range-scale`.
- `typo.py`: typografia z biblioteki `typografia-www` w buildzie (po `nbsp.py`, wymaga Node.js). Na Home po ręcznych zmianach tekstu: `python3 _generator/narzedzia/typo.py index.html` (`--raport` pokazuje tylko liczby, bez zapisu). Szczegóły w następnej sekcji.

## Typografia (biblioteka typografia-www)
Biblioteka (prywatne repozytorium `typografia-www`) składa się z reguł CSS (P1-xx) i reguł znaków w treści (P2-xx). Wdrożenie w makiecie:
- **Treść (P2), w buildzie:** `typo.py` uruchamia oryginalne `tp()` z biblioteki (`typo-biblioteka.js` to kopia `skill/typografia-tekst/typo.js`, commit `ce97dd3`; aktualizacja = podmiana pliku): cudzysłowy „…” i «…», apostrof, półpauza we wtrąceniach (K-01), zakresy, wielokropek, ×, −, ½, °C, spójniki jednoliterowe, inicjały, grupowanie cyfr. Do tego P2-12 (ostatni krótki wyraz akapitu, listy, podpisu przyklejony twardą spacją) i uzupełnienia z katalogu (M-113, M-59): liczba + jednostka, skrót + wyraz (`ul.`, `lek. wet.`), ulica + numer, kod + miasto, numer telefonu w jednym kawałku.
- **CSS (P1):** większość reguł makieta ma już w `minimal.css` i `layout-nowa.css`. Luki uzupełnia `typografia-www.css` w `@layer typo` (każda reguła makiety wygrywa, więc plik niczego nie nadpisuje): `text-rendering`, wiszący cudzysłów, `quotes`, cyfry tabelaryczne w tabelach i numerach list. Link jest w `index.html`, podstrony dostają go z Home.
- **Wyjątki narzędzia:** grupowanie cyfr pomija identyfikatory (ISO, NIP, REGON, KRS, adresy URL); atrybuty, `<head>` (title, meta) i `aria-label`/`alt` nie są przetwarzane; samotne „—” (brak danych) zostaje.
- **Świadomie nie wdrożone (ustalenia makiety wygrywają):** Sentient jako krój tekstu (makieta: Satoshi), `html` 17/24 (makieta: 16/24), wcięcia akapitów i justowanie (strona z blokami, nie ciągły tekst), skala nagłówków h1–h6 (makieta: jeden rozmiar tytułów, 700), automatyczne spacjowanie akronimów (makieta: rozstrzelenie tylko w kapitalikach), klasy układu `.k23` `.kiso` `.roz` `.kol` (makieta ma własną siatkę 12 kolumn), `sup`/`sub`/`.frac` (w treści nie ma takich elementów; cechy OpenType Satoshi niezweryfikowane), spis treści i żywa pagina z `typo.js` (podstrony mają własny spis).
- **Niesprawdzone:** wygląd w przeglądarce (łamanie wierszy po dodaniu spacji twardych, szerokości kart na 390 px); `pomiar.py` i `audit.py` wymagają Playwrighta z przeglądarką, której w środowisku, w którym wdrażałem zmiany, nie było.

## Inspektor uwag (do zbierania poprawek)
- Klawisz **I** na dowolnej stronie (lokalnie: localhost, 127.0.0.1, file://) włącza inspektor; kliknięcie elementu otwiera okienko uwagi, **Kopiuj wszystko** daje Markdown
  (selektor, wymiary i kolumna w siatce, styl, fragment HTML, szerokość okna) do wklejenia w rozmowie. Ponowne **I** wyłącza. Na stronie publicznej: `?uwagi=1`.
- Kod: `inspektor.js` (skrót, ładowany ze strony głównej i podstron) i `_generator/narzedzia/uwagi.js` (narzędzie).

## Zmienne palety sekcji
Każda sekcja (`.hero`, `.about`, `.services`, … w `minimal.css`) ma cztery zmienne; nic w sekcji nie powinno mieć na stałe wpisanego koloru z palety:
- `--surface` — tło sekcji,
- `--ink` — nagłówki, tytuły, ilustracje (filtry SVG), przyciski,
- `--small-ink` — akapity, listy, komórki tabel, podpisy; zawsze `color-mix(--ink, 86%, czarny/biały)` (niezauważalnie ciemniejszy/jaśniejszy),
- `--accent` — tło kart, pasów i kształty (elementy graficzne); linie dzielące są w kolorze `--ink` (nie `--accent`).
Pomocniczo: `--hover-ink`, `--hover-accent`. Globalna reguła w końcu `layout-nowa.css` ustawia kolor tekstu z tych zmiennych (wyjątki: bloki odwrócone, przyciski, menu, panel „poza godzinami”).

## Zestawy palet (cała strona)
Strona ma trzy komplety palet; domyślny to „szlachetna”, pozostałe włącza atrybut `html[data-paleta]`:
- **szlachetna** (domyślna, bez atrybutu) — palety w `minimal.css`, `social-promo.css`, `podstrony.css`, tokeny w `design-tokens.css` (źródło: `wordpress/theme-source/theme.json`); zieleń hero `#124e36`.
- **poprzednia** (`?paleta=poprzednia`) — palety sprzed 11.10.2026: zielone ściany, brzoskwinia, szałwia, kobalt (zieleń `#124e2c`). Dwie różnice względem oryginału: blok rezerwacji na podstronach ma czytelny tekst (w oryginale zielony na zielonym), a sekcja z banerem „Praca” ma kolor sekcji Opinie (w oryginale zlewała się z „O nas”).
- **fac** (`?paleta=fac`) — oparta na stronie Feminist Art Coalition: krem `#FAF5EA`, głęboka zieleń `#0E433A` (tu zieleń hero), mięta `#4FAB72`, koral `#FF9575` oraz ich tinty. Cztery kolory odczytane z wyliczonych stylów dwóch podstron serwisu (nie z arkusza CSS); pozostałe odcienie są dobrane do nich.
Definicje zestawów (komplet reguł palet sekcji + kolory marki: zieleń, pomarańcz, „szampan”, „piasek”, papier) są w jednym pliku: **`palety-zestawy.css`**. Nowy zestaw = nowy blok z tymi samymi selektorami; każda reguła deklaruje wszystkie zmienne sekcji (inaczej zostałaby wartość z zestawu domyślnego). Kolory marki w pasku telefonu, cookies i nagłówku czytają tokeny `--wp--preset--color--*`, więc zmieniają się razem z zestawem.
Wybór: nakładka K (u góry panelu) albo `?paleta=…` w adresie (`?paleta=szlachetna` wraca do domyślnego); wybór pamięta `localStorage` („psyjaciele-paleta”), a ustawia go skrypt w `<head>` (`nowa-readability.js`), więc kolory nie mrugają. Generator (`home.py::_set_surfaces`) czyta tła ról ze wszystkich zestawów i dba, żeby na podstronach sąsiednie sekcje nie miały tego samego tła w żadnym z nich.

## Nakładka palet (klawisz K)
- **K** na dowolnej stronie (lokalnie albo z `?uwagi=1`) włącza nakładkę. U góry panelu jest **wybór zestawu palet** całej strony (podgląd siedmiu kolorów każdego zestawu); wybór zeruje ręczne zmiany sekcji.
- Najedź na sekcję i kliknij — panel pokazuje palety sekcji aktywnego zestawu (czytane z CSS, więc zawsze zgodne z zestawem), 12 klasycznych zestawień z mody (szmaragd i szampan, granat i wielbłąd, burgund i róż, czerń i kość słoniowa…), cztery własne kolory (tło, tekst, tekst mały, akcent), „Odwróć”, „Przywróć sekcję/wszystko” i „Kopiuj zmiany” (Markdown do rozmowy, z nazwą zestawu). Ponowne **K** lub **Esc** zamyka nakładkę.
- Zmiany sekcji to zmienne CSS ustawione inline (`--surface`, `--ink`, `--small-ink`, `--accent`, `--hover-ink`, `--hover-accent`); po odświeżeniu znikają (zestaw zostaje). Kod: `_generator/narzedzia/paleta.js`, ładowany z `inspektor.js`.

## Zespół (Home #zespol i „Kto przyjmuje” na podstronach)
Karty osób: kwadratowa komórka na 4 kolumnach w kolorze akcentowym sekcji (Home: 3 w rzędzie; podstrony: 2 w rzędzie w kolumnie artykułu; poniżej 560 px jedna). Hover/fokus pokazuje linie wokół sylwetki:
- `team-echo.js`: z kanału alfa zdjęcia liczone jest pole odległości od sylwetki, a canvas rysuje cienkie linie konturu (3 px, co 15 px) przesuwane w pętli na zewnątrz (11 px/s); parametry na górze pliku (`STROKE_PX`, `GAP_PX`, `SPEED_PX`, `FADE_IN_PX`); kolor linii = `--team-overlay-ink` (domyślnie `--accent` karty); pętla działa tylko przy hoverze. Bez JS, przy `prefers-reduced-motion` i na dotyku karta jest bez linii (statycznej nakładki nie ma).

## Komendy (z katalogu makiety)

```
python3 _generator/narzedzia/build.py     # buduje podstrony
python3 _generator/narzedzia/checks.py    # sprawdza treść i strukturę (17× OK)
python3 _generator/narzedzia/audit.py     # audyt przeglądarkowy (Playwright), serwer na :8765
python3 _generator/narzedzia/pomiar.py    # pomiar geometrii wszystkich stron (siatka, rytm 8 px, nakładanie, kontrast, sierotki, kotwice); serwer na :8766
python3 _generator/narzedzia/pomiar_analiza.py siatka|rytm|przepelnienia|kontrast|sieroty|nakladanie|puste|meta [szerokości]
```

Wymagania: `beautifulsoup4` (build, checks) i `playwright` (audit).

## Archiwum (`_archiwum/`)

`home-stare/` (index-min, index-poprzedni, przekierowanie), `layout-warianty/` (warianty układu),
`stare-podstrony-korzen/` i `stare-podstrony-wygenerowane/` (poprzednie wersje podstron),
`nieuzywane/` (CSS i JS nieładowane przez żadną stronę), `_to_delete/`, `README-stary.md`
oraz `kopia-przed-porzadkami-2026-10-08.tgz` (kopia całości bez `assets` sprzed porządków).
