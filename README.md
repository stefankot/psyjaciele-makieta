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
│   design-tokens.css, layout-editorial.css, social-promo.css,
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
- `infografiki.py`: infografiki wstawiane po nagłówkach wskazanych sekcji (lista `PLAN`); style `.info-*` w `podstrony.css`. Skala ciśnienia to restyl istniejącego bloku `range-scale`.

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

## Nakładka palet (klawisz K)
- **K** na dowolnej stronie (lokalnie) włącza nakładkę: najedź na sekcję i kliknij — panel pokazuje 12 gotowych palet z kolorów strony, cztery własne kolory (tło, tekst, tekst mały, akcent), „Odwróć”, „Przywróć sekcję/wszystko” i „Kopiuj zmiany” (Markdown do rozmowy). Ponowne **K** lub **Esc** zamyka nakładkę.
- Zmiany to zmienne CSS sekcji ustawione inline (`--surface`, `--ink`, `--small-ink`, `--accent`, `--hover-ink`, `--hover-accent`); po odświeżeniu znikają. Kod: `_generator/narzedzia/paleta.js`, ładowany z `inspektor.js`.

## Komendy (z katalogu makiety)

```
python3 _generator/narzedzia/build.py     # buduje podstrony
python3 _generator/narzedzia/checks.py    # sprawdza treść i strukturę (17× OK)
python3 _generator/narzedzia/audit.py     # audyt przeglądarkowy (Playwright), serwer na :8765
```

Wymagania: `beautifulsoup4` (build, checks) i `playwright` (audit).

## Archiwum (`_archiwum/`)

`home-stare/` (index-min, index-poprzedni, przekierowanie), `layout-warianty/` (warianty układu),
`stare-podstrony-korzen/` i `stare-podstrony-wygenerowane/` (poprzednie wersje podstron),
`nieuzywane/` (CSS i JS nieładowane przez żadną stronę), `_to_delete/`, `README-stary.md`
oraz `kopia-przed-porzadkami-2026-10-08.tgz` (kopia całości bez `assets` sprzed porządków).
