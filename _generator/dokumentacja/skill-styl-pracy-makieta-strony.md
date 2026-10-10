---
name: styl-pracy-makieta-strony
description: Wymagania, zasady, potrzeby i styl pracy właściciela przy budowie statycznych makiet stron (projekt „Psyjaciele” — przychodnia weterynaryjna Warszawa Gocław — i kolejne w tym samym stylu). Używaj na początku każdej pracy nad makietą strony HTML/CSS/JS, przy poprawkach z inspektora uwag („Uwagi do makiety”), zmianach układu, palet, ikon, obrazów (konwersja do AVIF), przy pisaniu promptów dla innych wątków (generowanie obrazów, tekstów) oraz przy każdej odpowiedzi po poprawkach (linki, weryfikacja, commit). Pisz po polsku, krótko, konkretnie.
---

# Styl pracy — makiety stron w stylu „Psyjaciele”

Skill zbiera wszystko, co właściciel powtarzał w trakcie budowy makiety. Zastosuj go domyślnie; łam tylko na wyraźne polecenie. Szczegóły bieżącego projektu: `README.md` makiety i pamięć projektu (`projekt-makieta-psyjaciele-srodowisko`).

## 1. Komunikacja
- Język polski, bez emoji, bez zbędnych wstępów. Krótkie podsumowanie: co zmieniłem, co zmierzyłem, czego nie sprawdzałem.
- **Zasada nadrzędna: po każdej poprawce podaj link, najlepiej z `#sekcja`** (np. `http://127.0.0.1:8766/uslugi-weterynaryjne/<slug>/index.html#<id>`); osobny link na każde zmienione miejsce.
- Mów prawdę o stanie: co jest lokalne, co wypchnięte (commit/push tylko na prośbę), co niesprawdzone (np. widok mobilny), co zawiodło (np. brak kredytów API).
- Gdy uwaga jest niejasna albo ma kilka sensownych interpretacji, który wybór zmienia wygląd: zapytaj krótko i konkretnie (2–3 pytania naraz). Gdy da się rozsądnie wybrać — wybierz, powiedz co wybrałeś.
- Nie przepraszaj długo, nie powtarzaj całej historii. Jeśli popełniłem błąd (np. usunąłem coś, o co nie proszono) — napraw i napisz jednym zdaniem.
- Zdjęcia/ilustracje referencyjne od właściciela: odtwórz **układ** dokładnie, kolorów nie zmieniaj, o ile o to nie prosił („nic nie pisałem o kolorze”).

## 2. Proces (zoptymalizowany)
1. **Wejście:** uwagi z inspektora (klawisz **I**; Markdown z selektorem, wymiarami, stylem, fragmentem HTML, adresem). Lista bywa kumulatywna — uwagi już zrobione pomijaj (napisz jednym zdaniem, że były). Uwaga „tylko do home” = tylko Home; w innym wypadku **stosuj regułę do wszystkich analogicznych miejsc na wszystkich podstronach** („ile mam powtarzać”).
2. **Zakres:** zacznij od zrozumienia reguły, nie pojedynczego elementu. Jedna zmiana w generatorze/CSS > ręczne poprawki w 17 plikach.
3. **Implementacja:** Home (`index.html`) edytuje się ręcznie; podstrony generuje `_generator/narzedzia/build.py` z Home + `_generator/tresci-podstron/`. Po zmianie CSS/JS podbij `CSS_V` / `JS_V` w `build.py` i wersje `?v=` w `index.html` (cache!).
4. **Weryfikacja punktowa** (właściciel prosił o oszczędność tokenów): `build.py` + `checks.py`, potem jeden pomiar w przeglądarce (`getBoundingClientRect`, `getComputedStyle`) i najwyżej jeden zrzut elementu. Pełny audyt wszystkich stron i szerokości tylko na koniec paczki albo na prośbę. Domyślne okno: 1710 px (jak u właściciela), dodatkowo 1440; mobilne (390) sprawdzaj, gdy zmiana dotyczy układu wąskiego albo gdy właściciel prosi.
5. **Odpowiedź:** co zmieniłem (po punktach uwag), liczby z pomiaru, linki. Pytania na końcu.
6. **Git:** commit/push wyłącznie na prośbę („wypchnij na githuba”); wiadomość commitu po polsku, z trailerem Co-Authored-By zgodnym z instrukcją sesji.

Pułapki, które już kosztowały czas: przejścia CSS opóźniają pomiary kolorów (wyłącz `transition` przed pomiarem); myszka nad elementem zmienia stan hover (odsuń kursor); zmienna `--i` jest już zajęta (licznik animacji) — własne zmienne prefiksuj; selektory specyficzności `html body.book-type…` przeważają luźniejsze; przy `display: contents` rodzic nie ma boxa (zrzut robić na dziecku); `:has()` i zagnieżdżony CSS działają — ale `getMatchedCSSRules` nie, użyj CDP `CSS.getMatchedStylesForNode`.

## 3. Układ i typografia
- Siatka 12 kolumn, max 1280 px, odstęp 32 px. Artykuł podstrony: kolumny 5–12 (8 kol.), po lewej sticky spis treści (4 kol.). Wszystko trzyma się siatki; zdjęcia i rysunki mają 4 lub 8 kolumn (pozostałe szerokości — wolna przestrzeń w kolorze tła).
- **Zdjęcie pionowe bez tekstu obok → poziomy kadr na 8 kolumn**; zdjęcie obok krótkiego tekstu (< ok. 320 znaków) → zdjęcie 8 kol., tekst pod nim; para zdjęcie + tekst 4+4 tylko gdy tekstu jest dużo; strony pary naprzemiennie.
- Bez zaokrągleń i cieni (radius 0), jeśli właściciel nie poprosił inaczej. Kreski/ramki płaskie, bez gradientów.
- Pismo: Satoshi (tytuły jednym rozmiarem, 700), Rialto tylko dla słów „Psyjaciele/psyjaciel…” (141 % rozmiaru, klasa `.psy`) i imion na kartach lekarek. Tekst główny 16/24, lead 20–28 px; **telefon (≤ 700 px): baza 14 px, wszystkie rozmiary i interlinie ×0,875 — robi to generator `mobile_skala.py` (mobile-skala*.css, nie edytuj ręcznie)**; interlinia na siatce 8 px. **Kapitaliki = wersaliki rozstrzelone (0,12 em, 16 px)** — rozstrzelenie tylko tam, nigdzie indziej.
- Tytuł hero jedną wielkością, bez „fit title”; strzałka powrotu do strony głównej (nie „wstecz”), środek kółka = środek wielkiej pierwszej litery.
- Odstępy z tokenów (`--s1…--s7`: 8/13–16/21/34/55/89/144); wiszące znaczniki list poza akapitem; światło (whitespace) jest decyzją właściciela — **nie skracaj apli, gdy prosi o światło**; tekst w kaflach/banerach zawsze na górze **i** na dole apli, jeśli tak ustalono.
- Komponenty: hero 2×2 (nagłówek | lead / przyciski+status | ilustracja do góry-lewej), infografiki zamiast opisowych list (kroki w rzędzie, osie czasu, porównania „vs” w kółku), baner pracy (zdjęcie siatki pacjentów + tytuł „Praca”), bloki alarmowe z ikoną (i) w prawym górnym rogu i padding pionowy 56 px.

## 4. Paleta kolorów (zmienne sekcji)
Każda sekcja ma cztery zmienne i nic poza nimi: `--surface` (tło), `--ink` (nagłówki, ilustracje, linie dzielące, przyciski), `--small-ink` (akapity, listy, komórki tabel, podpisy; = `--ink` przesunięty o 14 % w stronę czerni/bieli), `--accent` (tło kart i pasów, kształty). **Linie dzielące zawsze w `--ink`**, bez przezroczystości. Żadnych stałych kolorów z palety w komponentach, filtrach SVG, przyciskach. Zmiana koloru = zmiana palety, nie komponentu. Kontrast ≥ 3∶1 sprawdzaj dla co najmniej trzech palet. Nakładka palet: klawisz **K** (kliknij sekcję, wybierz paletę, „Kopiuj zmiany”). Kolory tylko na wyraźną prośbę.

## 5. Obrazy
- **Wszystkie obrazy na stronie konwertuj do AVIF, lokalnie** (`avifenc`): **ilustracje jakość 50, zdjęcia jakość 60, alfa 90, najwyższy wysiłek (`-s 0`)**, reszta parametrów bez zmian. Skrypt: `_generator/narzedzia/avif.py` (rozpoznaje użyte obrazy, WebP przechodzi przez PNG). Oryginały zostają obok (są referencją dla generowania i przy podmianach). Strona używa `.avif`; placeholdery próbują `.avif`, potem oryginału (`podstrony.js`).
- Ilustracje: czarna kreska na białym tle; na stronie kolor kreski = `--ink` sekcji (filtr SVG w obrębie sekcji), tło = kolor uzupełniający. Zdjęcia: kolorowe, wypełniają ramkę (`cover`, kadr przez `--ph-pos`). Brakujący obraz → placeholder z napisem, **co** ma w nim być (np. „Ilustracja zamiast zdjęcia: …”).
- Generowanie przez OpenAI: narzędzie wymaga kredytów (bez nich — powiedz od razu i zaproponuj istniejące zasoby). Do osobnych wątków pisz **samowystarczalne prompty ≤ 200 słów, ze ścieżkami absolutnymi** do plików projektu i do katalogów wyjściowych; generowanie partiami z pytaniem „czy kontynuować” po pierwszym obrazie.
- Obrazy cudzych praw i treści jednoznacznie seksualne: nie osadzaj.

## 6. Ikony
Jeden zestaw: **Iconoir** (MIT, `assets/icons/iconoir/`, generator `_generator/narzedzia/ikony.py` → `ikony.css`). Kreska ikony = grubość pisma obok (≈ 0,13 em; większe ramki dostają cieńszą kreskę w masce). Punktory list = `nav-arrow-right` (chevron-right); strzałki = `arrow-right` / `arrow-up-right`; (i) = `info-circle`; ostrzeżenie = `warning-triangle`; FAQ = `plus-circle`/`minus-circle`. Ikony pomocnicze, jeśli przyspieszają orientację (dojazd: `walking`/`bus`/`car`; kontakt: `map-pin`/`phone`/`clock`; przygotowanie…) — ale **bez ikony telefonu i maila w pasku nawigacji i w menu**, bez kropki statusu przy numerze w nagłówku. Pobieranie plików wymaga zgody (nazwa, źródło, rozmiar).

## 7. Narzędzia w makiecie
Klawisze (lokalnie): **I** inspektor uwag, **K** nakładka palet, **G** siatka. Serwer: `python3 -m http.server 8766` w katalogu makiety (Playwright MCP do pomiarów; venv z `bs4` w scratchpadzie). Komendy: `build.py` (uruchamia też `mobile_skala.py`), `checks.py`, `audit.py`, `avif.py`, `ikony.py`. Logo w nagłówku ma stałą grubość linii (obrys uzupełniany w `nowa-header.js` do wzorca z wysokości 100 px).

## 8. Lista kontrolna przed odpowiedzią
- Reguła zastosowana wszędzie, gdzie ma sens (nie tylko na stronie z uwagi)?
- `build.py` i `checks.py` bez błędów; wersje CSS/JS podbite?
- Jeden pomiar + (opcjonalnie) jeden zrzut; wynik w liczbach?
- Linki z `#sekcja`; jasno: lokalnie czy wypchnięte; co niesprawdzone?
- Pytania do właściciela tylko tam, gdzie wybór zmienia wygląd.
