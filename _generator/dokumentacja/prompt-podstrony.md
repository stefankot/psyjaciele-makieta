# Prompt: wygeneruj podstrony serwisu Przychodni Weterynaryjnej „Psyjaciele”

> Wersja 1.0 · 8.10.2026 · język dokumentu i raportu: polski · przeznaczenie: agent z dostępem do plików i powłoki (przeglądarka lub Playwright mile widziane).
> Dokument jest samowystarczalny: nie wymaga żadnych wcześniejszych rozmów ani innych plików niż folder makiety opisany w §2.

---

## 0. Jak używać tego dokumentu

1. Wklej całość agentowi uruchomionemu z dostępem do folderu makiety (`MAKIETA`, §2). Agent wykonuje zadanie samodzielnie, od analizy po raport.
2. **Kolejność ważności przy konflikcie:** §3 Reguły twarde → §4 Pułapki techniczne → §6 Bloki ze strony głównej i §7 Nowe bloki → §8 Dobór bloków → §9 Obrazy → §10 Szkielety stron. Chęć „ładniejszego” efektu nigdy nie wygrywa z regułą twardą.
3. **Fakty o makiecie** (§2, §4–§6) opisują stan z 8.10.2026. Zanim zaczniesz budować, sprawdź je skryptami na plikach (Etap 1, §12). Gdy plik różni się od opisu — **wygrywa plik**, a różnicę wpisz do raportu. Dotyczy to zwłaszcza palet kolorów: autor zapowiedział, że mogą się jeszcze zmienić.
4. **Nie zadawaj pytań w trakcie pracy.** Decyzje podejmuj sam i zapisuj je w raporcie (§13). Zatrzymaj się wyłącznie przy czynności nieodwracalnej (usunięcie albo nadpisanie istniejącego pliku, którego nie utworzył Twój generator) — wtedy jej nie wykonuj, tylko opisz w raporcie.
5. Pracuj etapami (§12) i po każdym etapie zapisuj stan na dysku. Nie pisz, że coś sprawdziłeś, jeśli tego nie uruchomiłeś; czego nie dało się sprawdzić — wypisz w raporcie.
6. Słowniczek: **strona główna** (dalej *home*) = `index-min.html`; **blok** = powtarzalny element kompozycji (np. `poster-grid`, `bento`, `quote`); **sekcja** = `<section>` pełnej szerokości z własną paletą; **paleta** = zestaw zmiennych `--surface/--ink/--small-ink/--accent/…` ustawiany przez klasę sekcji; **placeholder** = widoczne miejsce na obraz, który autor wstawi później.

---

## 1. Zadanie

**Rola.** Jesteś starszym inżynierem front-end i projektantem layoutu redakcyjnego. Twoim zadaniem jest *wiernie rozszerzyć istniejący system wizualny* strony głównej na 17 podstron — nie stworzyć własny.

**Zamówienie autora strony (dosłownie, skrócone o zdania wstępne):**

> Podstrony muszą pasować do charakteru strony głównej graficznie, i muszą używać jak największej ilości bloków kompozycyjnych które są obecne. Dodaj też swoje nowe bloki. Lubię gdy strona ma ciekawą strukturę, nie tylko lany tekst w jednej kolumnie — możesz stosować elementy layoutu które są niestandardowe. Podstrony mają mieć zdjęcia/obrazki/ilustracje, więc niech model da w optymalnych miejscach placeholdery na obrazki, które potem wstawię.
>
> Używaj znaczników/klas jak w CSS ze strony głównej — palety mogą się jeszcze zmienić, dlatego chcę deklaracji globalnych.

**Co robisz:** na podstawie gotowych tekstów (17 plików, §2) generujesz 17 statycznych podstron HTML, które wyglądają i zachowują się jak część tej samej strony co home.

**Sześć celów — wszystkie obowiązkowe:**

1. **Wierność wizualna.** Ten sam język graficzny, te same klasy i znaczniki, ta sama typografia, siatka, palety i ruch co na home (R1, R2, §5).
2. **Maksimum bloków z home.** Każdy blok kompozycyjny ze strony głównej, który ma sens treściowo, ma pojawić się na podstronach (§6, macierz pokrycia w §8).
3. **Nowe bloki.** Projektujesz własne bloki (§7) i używasz ich na każdej stronie.
4. **Ciekawa struktura.** Zero „lanego tekstu w jednej kolumnie”: asymetryczne kompozycje, kolumny przyklejone do przewijania, taśmy, osie czasu, zestawienia — z zachowaniem czytelności (§7, §8, §10).
5. **Placeholdery obrazów** w optymalnych miejscach, z manifestem i gotowymi promptami do generowania (§9).
6. **Deklaracje globalne.** Kolory wyłącznie przez zmienne i klasy-palety z home; żadnych literałów koloru w nowym kodzie (R2). Zmiana palety na home ma zmieniać podstrony po przeładowaniu — bez edycji podstron.

**Co dostarczasz (szczegóły w §11):**

- 17 stron HTML w `WYJŚCIE` + `podstrony/index.html` (przegląd);
- `podstrony.css` i `podstrony.js` (jedyne nowe arkusz i skrypt, ładowane po plikach home);
- katalog bloków `_bloki.html` (każdy nowy blok w ≥ 3 paletach);
- manifest obrazów `_obrazy.json` + `_obrazy.md` (opis, proporcje, alt, prompty);
- generator (Python) i testy w `_narzedzia/`;
- raport końcowy `_raport.md` (§13).

**Kryteria sukcesu — każde sprawdzasz i raportujesz osobno (K1–K9):**

| # | Kryterium | Jak sprawdzić |
|---|---|---|
| K1 | Istnieje 17 stron + przegląd; wszystkie otwierają się z serwera podglądu i z podkatalogu (symulacja GitHub Pages); zero błędów w konsoli, zero 404 poza placeholderami | V5, V11 |
| K2 | Test inwersji palety nie wykrywa **nowych** wycieków koloru ponad bazę home | V3, Dodatek A |
| K3 | W nowym CSS/HTML/JS **zero literałów koloru** (hex, `rgb()`, `hsl()`, nazwane kolory) | V2 |
| K4 | Cały tekst z plików treści występuje na stronach dosłownie; nic nie dopisano poza białą listą UI (R4) | V1 |
| K5 | Każda strona spełnia minimum pokrycia z §8 (≥ 7 różnych typów bloków, w tym ≥ 3 z home i ≥ 3 nowe; ≥ 2 kompozycje asymetryczne; 3–7 placeholderów) | V12 |
| K6 | Brak poziomego przewijania i brak zepsutych układów przy 1440, 1024, 768 i 390 px | V7 |
| K7 | Każdy placeholder ma wpis w manifeście (opis, proporcje, alt, prompt) | V13 |
| K8 | Brak nieznanych klas (spoza home i `podstrony.css`) oraz kolizji nazw | V4, Dodatek B |
| K9 | Raport końcowy w formacie z §13, uczciwie wskazujący, czego nie sprawdzono | §13 |

---

## 2. Dane wejściowe i parametry

### 2.1 Parametry

| Parametr | Wartość domyślna | Uwagi |
|---|---|---|
| `MAKIETA` | `/Users/milajovovich/Documents/Codex/2026-10-06/pracujesz-na-stronie-psyjacielevet-pl-masz-3/outputs/makieta` | Korzeń projektu; wszystkie ścieżki w tym dokumencie są względem niego. Jeśli ścieżka nie istnieje, znajdź folder zawierający jednocześnie `index-min.html` i `minimal.css`. |
| `PODGLĄD` | `http://127.0.0.1:8765/` | Lokalny serwer podglądu (`python3 -m http.server 8765` w `MAKIETA` — według `README.md`). Jeśli nie działa, uruchom własny i zapisz to w raporcie. Adresy katalogów mogą dawać 404 → **każdy link do podstrony kończy się na `index.html`**. |
| `PODGLĄD_PUBLICZNY` | `https://stefankot.github.io/psyjaciele-makieta/` | GitHub Pages z tego samego folderu. Makieta może leżeć w podkatalogu domeny → **tylko ścieżki względne**, bez `<base>` i bez ścieżek zaczynających się od `/`. |
| `TREŚCI` | `MAKIETA/tresci-podstron/czyste/<slug>.html` | Jedyne źródło tekstu (17 plików). Pliki w `tresci-podstron/<slug>.html` zawierają oznaczenia zmian redakcyjnych i służą tylko do wglądu — **nie używaj ich jako źródła**. |
| `WYJŚCIE` | `MAKIETA/podstrony/` | Jedyny katalog, do którego zapisujesz (R3, R11). |
| `DOMENA` | `https://www.psyjacielevet.pl` | Do `canonical`, Open Graph i JSON-LD. |
| `ROBOTS` | `noindex,follow` | Tak jak na home (makieta nie jest jeszcze produkcją). Ustaw w jednym miejscu generatora, żeby dało się przełączyć jedną stałą. |

**Pliki, z których składa się home** (ładowane przez `index-min.html`, w tej kolejności): `minimal.css`, `typography-book.css`, `animacje.css`, `zespol-rejestr.css`, `zespol-stopka.css`, [JSON-LD], `social-promo.css`, `layout-editorial.css`, `design-tokens.css` (na końcu, nadpisuje tokeny); skrypty (`defer`): `pet-photos.js`, `minimal.js`, `illustration-motion.js`, `animacje.js`. **Pozostałe pliki CSS/JS leżące w korzeniu** (`paleta.css`, `geometria.css`, `siatka.css`, `uklad.css`, `poprawki.css`, `nowe-sekcje.css`, `section-headings.css`, `zdjecia.css`, `menu.js`, `motion.js`, `index-poprzedni.html`, `index-min.przed-zmianami-2026-10-08.html`) **są historyczne — nie ładuj ich i nie traktuj jako źródła prawdy**. Tokeny kolorów w `design-tokens.css` są generowane z `wordpress/theme-source/theme.json` — nie edytuj ich.

### 2.2 Lista stron

Archetypy (szczegóły w §8 i §10): **A** usługa kliniczna (objawy → przyczyny → diagnostyka → leczenie → pytania → umówienie), **B** badanie (przygotowanie → przebieg → wynik), **C** profilaktyka i dokumenty (kroki, terminy, przepisy), **D** hub usług, **E** zespół, **F** dokument prawny.

| # | `slug` (plik treści) | Plik wyjściowy (względem `WYJŚCIE`) | Arch. | Etykieta w okruszkach* | Ilustracja bazowa do page-hero** |
|---|---|---|---|---|---|
| 1 | `uslugi-weterynaryjne` | `uslugi-weterynaryjne/index.html` | D | Usługi | `assets/illustrations/sekcja-uslugi-c.png` |
| 2 | `choroby-wewnetrzne-u-psow-i-kotow` | `uslugi-weterynaryjne/choroby-wewnetrzne-u-psow-i-kotow/index.html` | A | Choroby wewnętrzne | `…/services/service-internal.png` |
| 3 | `diagnostyka-laboratoryjna-weterynaryjna` | `uslugi-weterynaryjne/diagnostyka-laboratoryjna-weterynaryjna/index.html` | B | Diagnostyka laboratoryjna | `…/services/service-laboratory.png` |
| 4 | `szczepienia-oraz-profilaktyka-przeciwpasozytnicza` | `uslugi-weterynaryjne/szczepienia-oraz-profilaktyka-przeciwpasozytnicza/index.html` | C | Szczepienia i profilaktyka | `…/services/service-prevention.png` |
| 5 | `chirurgia-weterynaryjna-tkanek-miekkich` | `uslugi-weterynaryjne/chirurgia-weterynaryjna-tkanek-miekkich/index.html` | A | Chirurgia tkanek miękkich | `…/services/service-surgery.png` |
| 6 | `kardiologia-weterynaryjna` | `uslugi-weterynaryjne/kardiologia-weterynaryjna/index.html` | A | Kardiologia | `…/services/service-cardiology.png` |
| 7 | `diagnostyka-obrazowa-psow-i-kotow` | `uslugi-weterynaryjne/diagnostyka-obrazowa-psow-i-kotow/index.html` | B | Diagnostyka obrazowa | `…/services/service-imaging.png` |
| 8 | `okulistyka-weterynaryjna` | `uslugi-weterynaryjne/okulistyka-weterynaryjna/index.html` | A | Okulistyka | `…/services/service-eyes.png` |
| 9 | `dermatologia-weterynaryjna` | `uslugi-weterynaryjne/dermatologia-weterynaryjna/index.html` | A | Dermatologia | `…/services/service-skin.png` |
| 10 | `stomatologia-weterynaryjna` | `uslugi-weterynaryjne/stomatologia-weterynaryjna/index.html` | A | Stomatologia | `…/services/service-dentistry.png` |
| 11 | `nefrologia-weterynaryjna` | `uslugi-weterynaryjne/nefrologia-weterynaryjna/index.html` | A | Nefrologia | `…/services/service-kidneys.png` |
| 12 | `urologia-weterynaryjna` | `uslugi-weterynaryjne/urologia-weterynaryjna/index.html` | A | Urologia | `…/services/service-urology.png` |
| 13 | `pomiar-cisnienia-psow-i-kotow` | `uslugi-weterynaryjne/pomiar-cisnienia-psow-i-kotow/index.html` | B | Pomiar ciśnienia | `…/services/service-pressure.png` |
| 14 | `wystawianie-paszportow-psom-i-kotom` | `uslugi-weterynaryjne/wystawianie-paszportow-psom-i-kotom/index.html` | C | Paszporty dla zwierząt | `…/services/service-passport.png` |
| 15 | `czipowanie-psow-i-kotow` | `uslugi-weterynaryjne/czipowanie-psow-i-kotow/index.html` | C | Czipowanie zwierząt | `…/services/service-microchip.png` |
| 16 | `zespol` | `zespol/index.html` | E | Zespół | `assets/illustrations/cropped-b14c1db0a053.svg` (maska) |
| 17 | `polityka-prywatnosci` | `polityka-prywatnosci/index.html` | F | Polityka prywatności | brak |

\* Etykiety z kolumny są wartościami domyślnymi; **wygrywa tekst tytułu kafla na home** (generator czyta `h3 > a` w `.bento .tile`, usuwa `&shy;` i dopasowuje po `href`).
\*\* `…/services/` = `assets/illustrations/services/`. Pliki bazowe `service-<nazwa>.png` (1254 px) są ilustracjami liniowymi z kanałem alfa (zweryfikowane). Mapowanie slug → ilustracja **weź z kafli na home** (po `href`), plik bazowy to nazwa bez sufiksu `-a/-b/-c`.

**Dodatkowo** tworzysz `podstrony/index.html` — przegląd dla autora (lista 17 stron z linkami, link do `_bloki.html`, `_obrazy.md`, `_raport.md`). To strona narzędziowa: `noindex`, ten sam nagłówek i stopka, bez wymogów pokrycia z §8.

Adresy produkcyjne (do `canonical`, `og:url`, JSON-LD): `DOMENA/uslugi-weterynaryjne/` (hub), `DOMENA/uslugi-weterynaryjne/<slug>/`, `DOMENA/zespol/`, `DOMENA/polityka-prywatnosci/`.

### 2.3 Stałe danych kontaktowych

Odczytaj je z home (JSON-LD, sekcja `#kontakt`, nagłówek, stopka) — **nie wpisuj z pamięci**. Stan na 8.10.2026, dla orientacji: Przychodnia Weterynaryjna Psyjaciele, ul. Celownicza 4 lok. U-3, 04-175 Warszawa (Gocław); wejście od tyłu budynku; przystanek Zajezdnia Ostrobramska; telefon `+48 537 821 345` (`tel:+48537821345`, zapis wyświetlany `537 821 345`); e-mail `kontakt@psyjacielevet.pl`; rezerwacja online `https://www.wettermin.pl/lecznice/warszawa/5555`; godziny: pn–pt 9:00–20:00, sob–nd 10:00–14:00; mapa `https://maps.app.goo.gl/dNSn5ba2SVkXwKQH6`; Facebook i Instagram z JSON-LD. Gdy treść podstrony i home się różnią, napisz o tym w raporcie („Uwagi do treści”) i **nie poprawiaj tekstu samodzielnie**.

### 2.4 Struktura plików źródłowych treści

Każdy plik `TREŚCI/<slug>.html` ma stały kształt:

```
<!-- title: …  -->                       → <title> i og:title
<!-- meta description: … -->             → meta description, og:description
<div class="content">
  <h1>…</h1>                             → jedyny h1 strony
  <p>lead…</p> [<p>drugi akapit wstępu</p>]
  <p class="cta-wizyta"><strong>Umów wizytę:</strong> … Wettermin … 537 821 345</p>   (brak na zespole i w polityce)
  <nav class="spis-tresci"><p><strong>Spis treści</strong></p><ol> li > a[href="#id"] (+ zagnieżdżone ul dla h3) </ol></nav>
  <h2 id="…">…</h2> / <h3 id="…">…</h3>  → treść: p, ul, ol, table (thead/tbody), linki
  … sekcja pytań: h2 „Najczęstsze pytania” + h3 (pytanie) + p (odpowiedź) …
  … zamknięcie: h2 „Jak umówić …” + ul: <strong>Online:</strong>, <strong>Telefonicznie:</strong>, <strong>Kto …:</strong>, <strong>Adres:</strong>, <strong>Godziny otwarcia:</strong>
</div>
```

Wyjątki: `diagnostyka-laboratoryjna` ma tabelę zaraz po leadzie (przed `cta-wizyta`); `uslugi-weterynaryjne` ma cztery tabele 3-kolumnowe z linkami; `zespol` ma tabelę 3-kolumnowej listy lekarek i siedem profili (h2 z `id`: `Magda`, `Ola`, `Julia`, `Malgosia`, `Olga`, `Kasia`, `Kinga` — te same kotwice, do których linkuje home); `polityka-prywatnosci` (~20 000 znaków) nie ma `cta-wizyta` ani sekcji „Jak umówić”, za to tabele i listy numerowane.

Linki w treści używają ścieżek produkcyjnych (`/uslugi-weterynaryjne/<slug>/`, `/zespol/#Magda`, `/#kontakt`…) — mapuj je według R5.

---

## 3. Reguły twarde (R1–R12)

Reguły R1 i R2 pochodzą wprost od autora strony i mają najwyższy priorytet.

### R1. Te same znaczniki, klasy i kontekst co na home

1. Źródłem prawdy o markupie jest `index-min.html`, o wyglądzie — jej arkusze. Każdy blok istniejący na home kopiujesz **co do tagu, zagnieżdżenia, nazw klas i atrybutów** (`data-palette`, `aria-*`, `role`), zmieniając wyłącznie treść. Żadnych synonimów (`.hero-section` zamiast `.hero`) ani dodatkowych opakowań, które zmieniają ścieżkę selektora.
2. Reguły CSS home są silnie związane z przodkami (`.services .bento .tile`, `.team .people .person`, `.reviews .quote`, `.emergency .emergency-guide`, `.arrival .arrival-details`, `#obserwuj-nas …`). Dlatego odtwarzasz też **kontekst**: `section.<klasa-palety>[data-palette][aria-labelledby] > div.wrap.section-stack > blok`.
3. **Nowe bloki:** nazwy w kebab-case, rzeczownik, bez przedrostków i bez BEM (`fact-strip`, nie `ps-fact-strip` ani `fact-strip__item`). Warianty jako dodatkowa klasa `is-<wariant>`, stany też `is-…` (jak na home: `is-open`, `is-compact`, `is-active`). Wewnątrz bloku używaj znaczników semantycznych (`dl`, `dt`, `dd`, `ol`, `li`, `summary`), a klas tylko tam, gdzie są konieczne. Sprawdź kolizje z nazwami home (Dodatek B).
4. **Nie edytujesz CSS ani HTML home.** Całe nowe CSS trafia do `podstrony/podstrony.css`, ładowanego jako ostatni arkusz; reguły dotyczące wyłącznie podstron zaczynasz od `body.subpage`.
5. Atrybut `style` służy tylko do właściwości własnych instancji, tak jak na home (`--art-ratio`, `--blob`, `--art`, `--icon`, `--ph-ratio`) — **nigdy do kolorów**. Wyjątek jak na home: `width/height/object-fit` i `filter:url(#id)` na `<img>` ilustracji barwionej filtrem (T1).

### R2. Kolory wyłącznie przez deklaracje globalne (palety mogą się zmienić)

1. **Paleta sekcji = klasa sekcji identyczna z home** (tabela w §5.4) **+ atrybut `data-palette`**. Obecność atrybutu włącza regułę ogólną `[data-palette]{…}`; jego wartość nie wpływa na CSS (kopiuj ją z home dla tej samej klasy, programowo). Użycie klasy sekcji wyłącznie jako *dostawcy palety* jest dozwolone i zamierzone (np. `class="reviews"` na sekcji bez cytatów).
2. Wewnątrz sekcji kolor wolno brać **tylko** z: `var(--surface)`, `var(--ink)`, `var(--small-ink)`, `var(--accent)`, `var(--hover-ink)`, `var(--hover-accent)`, `var(--card-surface)`, `var(--card-accent)`, a ponadto `currentColor`, `transparent`, `inherit` i `color-mix(in srgb, <zmienna z listy> N%, transparent)` do półprzezroczystości (tak robi home przy `.button:hover`).
3. Poza sekcjami (np. `sticky-cta`) wolno użyć zmiennych z `:root` (`--paper`, `--ink`, `--surface`) — to też deklaracje globalne.
4. Tokeny `--wp--preset--color--*` służą do *definiowania* palet w CSS home. W nowym kodzie nie używaj ich bezpośrednio.
5. **Zabronione** w nowym kodzie: `#hex`, `rgb()/rgba()/hsl()/hwb()/lab()/oklch()` z literalnymi liczbami, nazwane kolory (poza `transparent`, `currentColor`, `inherit`), kolor literalny w `filter`, `feFlood`, `stop-color`, `fill`, `stroke`, `box-shadow`, `text-shadow`, `outline`, gradientach. Na home nie ma cieni (poza dymkiem `.pet-name-tooltip`) — nie dodawaj ich wcale.
6. **Nowy blok jest bezbarwny.** Nie projektuj „zielonej karty” ani „brzoskwiniowej taśmy”: blok wylicza wszystko ze zmiennych sekcji, w której stoi, więc w każdej palecie wygląda poprawnie. Blok odwrócony (`alert-band.is-inverted`) używa `background: var(--ink); color: var(--surface)`. **Nie ustawiaj** `--ink: var(--surface)` na tym samym elemencie, na którym `--surface` jest zdefiniowane przez paletę (powstaje cykl i zmienna staje się nieważna) — rozwiązaniem jest bezpośrednie użycie `color:var(--surface)` i jawne `color:inherit` w dzieciach.
7. **Obrazy:** ilustracje liniowe barwisz filtrem SVG z `flood-color="var(--ink)"` osadzonym w tej samej sekcji (technika z home, §5.5), nigdy gotowym kolorowym plikiem. Zdjęcia są czarno-białe (CSS `grayscale`), a kolor pochodzi z tła ramki (`--accent`). Przezroczyste wycinki i ilustracje nie mają „wypalonego” koloru, który miałby się zmieniać z paletą.
8. **Nie ufaj etykietom `data-palette`** (`cream-salmon`, `sky`, `ivory`…) — bywają nieaktualne. O palecie decyduje klasa sekcji i jej definicja w CSS. Słownik „rola → klasy + etykieta” generator buduje **z home w czasie generowania** (nie z pamięci).
9. **Wyjątki dziedziczone z home** (stałe kolory w filtrach `<svg>` na końcu `<body>`, tło fotografii `#d4d4d4`, dymki, logo marki, `social-promo`) kopiujesz bez zmian, ale **nie dodajesz nowych**. Baza wycieków home jest mierzona testem z Dodatku A; podstrony nie mogą jej powiększyć.
10. **Test akceptacyjny:** po obróceniu barwy wszystkich tokenów kolorów o 137° żaden *nowy* element podstrony nie może zachować dawnego koloru (V3).

### R3. Istniejące pliki są tylko do odczytu

Nie modyfikujesz ani nie usuwasz: `index-min.html`, `index.html`, żadnego pliku CSS/JS w korzeniu, `assets/**`, `tresci-podstron/**`, `wordpress/**`, folderów `uslugi-weterynaryjne/`, `zespol/`, `polityka-prywatnosci/` w korzeniu (to wcześniejsze statyczne kopie, na których home nadal się opiera), ani `README.md`. Zapisujesz wyłącznie w `WYJŚCIE`. Gdy potrzebujesz zmodyfikowanej kopii zasobu (np. inny kadr), umieść ją w `podstrony/assets/`. Propozycje zmian w plikach home trafiają do raportu, nie do plików.

### R4. Treść dosłownie

1. Tekst z `TREŚCI` kopiujesz **dosłownie, programowo** (generator czyta pliki; nie przepisujesz ręcznie). Nie skracasz, nie parafrazujesz, nie łączysz akapitów, nie zmieniasz kolejności w obrębie sekcji. Zachowujesz treść linków i ich cele. Wszystkie `h2/h3` zachowują poziom, tekst i `id` (kotwice ze spisu treści muszą działać).
2. **Zakaz dopisywania** zdań medycznych, cen, terminów, liczb, dat, nazwisk, statystyk, obietnic („szybko”, „bezboleśnie”) i opinii. Jeśli fragment treści wydaje się błędny lub ryzykowny — nie zmieniaj go; wypisz w raporcie w „Uwagach do treści”.
3. **Biała lista dodatków UI** (krótkie, neutralne, bez nowych twierdzeń; ≤ 4 słowa):
   etykiety struktury („Spis treści”, „Na skróty”, „Okruszki”, „Zobacz też”, „Kolejne usługi”, „Wróć do spisu”, „Pokaż odpowiedź”, „Krok 1”), kickery („Usługa”, „Ważne”, „Pilne”, „Pytania”, „Kontakt”), numeracja (01, 02…), strzałki `→`/`↗` w `.type-arrow`, etykiety przycisków powtarzające CTA z treści („Umów wizytę”, „Zadzwoń: 537 821 345”, „Wybierz termin online”), `aria-label`/`alt`/`title` opisowe, podpisy placeholderów (§9) oraz **stałe teksty z home pobrane programowo** (nagłówek, stopka, kafle usług, panel „Poza godzinami pracy”, opinie, sekcje rezerwacji i „Obserwuj nas”).
4. **Dozwolone przekształcenia** (bez zmiany słów): podział h1/h2 na `span.heading-roman` + `em`, z pozostawieniem pauzy lub dwukropka w `.visually-hidden` (§7 N1); pominięcie kropki lub dwukropka kończącego etykietę *run-in* („Rozmowa.” → `h4` „Rozmowa”), gdy etykieta staje się nagłówkiem; zamiana `td` pierwszej kolumny na `th scope="row"`; dekoracyjna strzałka w miejsce myślnika dzielącego warunek i rekomendację w bloku `chooser`.
5. **Dozwolone duplikaty** (identyczny tekst w drugim miejscu): lead w page-hero, `cta-wizyta` jako przyciski i jako `cta-band`, wpisy spisu treści, wartości `fact-strip` (muszą być *dosłownymi podciągami* tekstu strony), pytania i odpowiedzi w JSON-LD.
6. **Kolejność:** w obrębie sekcji — jak w źródle. Przeniesienia dozwolone tylko te: lead → page-hero; `cta-wizyta` → przyciski page-hero; `nav.spis-tresci` → `toc-index`; sekcja „Jak umówić…” → blok `contact`; „Najczęstsze pytania” → FAQ.
7. **Typografia polska:** spacja niełamliwa (`&nbsp;`) po jednoliterowych wyrazach (a, i, o, u, w, z), w „lek. wet.”, „ul.”, „lok.”, w numerach telefonu i między liczbą a jednostką; prawdziwe cudzysłowy „…”, pauza —, półpauza –, wielokropek …; żadnych ręcznych `<br>` w tytułach; `&shy;` tylko w tytułach kafli, tak jak na home. Źródła mają już poprawną typografię — nie psuj jej przy kopiowaniu.

### R5. Ścieżki i linki

1. Wszystkie ścieżki są **względne**. Dla każdej strony oblicz `ROOT` = ścieżka względna do `MAKIETA` (`podstrony/index.html` → `../`; `podstrony/zespol/index.html` i `podstrony/uslugi-weterynaryjne/index.html` → `../../`; strony usług `podstrony/uslugi-weterynaryjne/<slug>/index.html` → `../../../`). Zapisz go w `<body data-root="…">`.
2. `<link href>`, `<script src>`, `<img src>`, `<a href>`, `srcset`, `<source>` rozwiązują się względem dokumentu → **zawsze z prefiksem `ROOT`** (np. `../../../assets/…`). Zasoby i arkusze home ładuj z `ROOT` z dokładnie tymi samymi atrybutami (łącznie z `?v=…`), odczytanymi z `index-min.html`.
3. Własności `--art`, `--icon`, `--blob`, `--pet-atlas` ustawiane w `style` mają osobną regułę — patrz §4, pułapka 4.
4. **Mapowanie linków z treści** (wszystkie linki wewnętrzne kończą się na `index.html`; zero adresów katalogów):

| W treści | W wyniku |
|---|---|
| `/uslugi-weterynaryjne/<slug>/` | ścieżka względna do `…/uslugi-weterynaryjne/<slug>/index.html` |
| `/uslugi-weterynaryjne/` | ścieżka względna do huba |
| `/zespol/` i `/zespol/#Magda` itd. | `zespol/index.html` (+ ta sama kotwica) w nowych podstronach |
| `/polityka-prywatnosci/` | `polityka-prywatnosci/index.html` w nowych podstronach |
| `/#kontakt`, `/#przygotowanie`, `/#nagle-przypadki`, `/#uslugi`, `/#zespol`, `/#onas`, `/#dojazd`, `/#pytania` | `ROOT` + `index-min.html#…` |
| `/` | `ROOT` + `index-min.html` |
| zewnętrzne (Wettermin, mapy, Google, FB/IG, strony instytucji), `tel:`, `mailto:` | bez zmian; linki zewnętrzne dostają `<span class="type-arrow" aria-hidden="true">↗</span>`, wewnętrzne `→` (w przyciskach i linkach „akcji”) |

5. Nagłówek i stopka pochodzą z home: linki `#sekcja` zamieniasz na `ROOT` + `index-min.html#sekcja`; link marki → `ROOT` + `index-min.html`. W menu pozycje „Usługi” i „Zespół” kierują do nowych podstron (hub, zespół), a pozycji odpowiadającej bieżącej stronie nadajesz `aria-current="page"` (strony usług: `aria-current="true"` przy „Usługi”) — CSS home pokazuje wtedy kropkę „tu jesteś”.
6. Link w stopce do polityki prywatności oraz linki do profili lekarek kierują do **nowych** podstron (`podstrony/…`), pozostałe — do home.

### R6. Skrypty

1. **Nie ładuj `minimal.js`** — nie jest odporny na brak elementów (`.about`, `.portrait-halo`, `.portrait-circle`, `.booking-composition`), więc na podstronie zgłasza błąd i przerywa działanie.
2. Utwórz `podstrony/podstrony.js` (vanilla JS, `defer`, bez bibliotek). Przenosi z `minimal.js` **tylko** potrzebne zachowania, identyczne w działaniu: przełącznik menu (`aria-expanded`, `#menu.is-open`, `.menu-open` na nagłówku, etykiety „Otwórz menu”/„Zamknij menu”, zamknięcie po kliknięciu w link i klawiszem Escape); stan nagłówka (`is-compact` gdy `scrollY > 16`, `.header-backdrop.is-active`, `is-scrolling-down`, zmienna `--nav-ink` liczona z sekcji pod nagłówkiem); obrót `--blob-angle` dla `.portrait-blob`; obrót pierścieni `.social-promo-ring, .footer-logo-ring`; (jeśli użyjesz kompozycji `booking`) pływanie `.booking-pet` i `psyPetPhotos`. Dodaje też: korektę adresów w zmiennych własnych (§4, pkt 4), ładowarkę placeholderów (§9), otwieranie `details` z kotwicy, `sticky-cta`, podświetlanie w `rail-layout`.
3. Ładujesz z home bez zmian: `animacje.css`, `animacje.js`, `illustration-motion.js`, `pet-photos.js` (po sprawdzeniu, że nie zgłaszają błędów na podstronach; `pet-photos.js` zapisuje `url(assets/…)` — patrz pułapka 4).
4. **Zero nowych animacji przewijania** (reveal, parallax). Ruch pochodzi z warstwy home: rysowanie linii nad kolumnami (`.ruled-columns > div|article`, `.equipment-grid > div`), „wrzenie” ilustracji (`.section-illustration`), pasek postępu, dryf, kropki, strzałki. Nowe bloki korzystają z tej warstwy przez te same klasy (np. `ruled-columns`).
5. Bez zewnętrznych zasobów: żadnych CDN, fontów, analityki, bibliotek, iframe’ów.

### R7. Dostępność i SEO

1. Jedno `h1` na stronę (tytuł ze źródła). Landmarki: `header`, `nav#menu`, `main#main`, `footer`, link `a.skip` („Przejdź do treści”). Okruszki jako `nav[aria-label="Okruszki"] > ol`; bieżąca pozycja bez linku, z `aria-current="page"`.
2. `<title>` i `meta description` z komentarzy w pliku treści. `canonical` i `og:url` = `DOMENA` + adres produkcyjny strony. `robots` = `ROBOTS`. Open Graph i Twitter jak na home (`og:type=website`, `og:locale=pl_PL`, `og:site_name=Psyjaciele`, `twitter:card=summary`).
3. JSON-LD (`@graph`) na każdej stronie: `VeterinaryCare` (pełny węzeł skopiowany z home, z tym samym `@id` `…/#przychodnia`), `WebSite` (`…/#website`), `WebPage` (z `isPartOf`, `about`, `breadcrumb`), `BreadcrumbList`; na stronach usług dodatkowo `Service` (`provider` → `@id` przychodni, `areaServed`); gdy na stronie jest sekcja pytań — `FAQPage`, którego pytania i odpowiedzi są **identyczne** z widocznymi (V9). Na zespole możesz dodać węzły `Person` (imię i nazwisko, „lekarz weterynarii”, `knowsAbout` z listy „Obszary”) — tylko z faktów w treści.
4. Kontrast WCAG AA dla tekstu w każdej palecie (sprawdzaj obliczone kolory). Widoczny fokus (`:focus-visible` z home). Cele dotykowe ≥ 44 px. Obrazy treściowe mają `alt`; dekoracyjne `alt=""`. Tabele: `<th scope>`; przy układzie „kartowym” na telefonie nagłówek kolumny wraca jako `data-label` z tekstem dosłownie z `th`.
5. `lang="pl"`. Nagłówki tworzą poprawny konspekt (bez przeskoków poziomów w treści; poziomy wizualne ustawiasz klasami, nie zmianą tagu).

### R8. Bezpieczeństwo treści medycznych

1. Informacje pilne (np. „Kocur lub pies nie może oddać moczu — to stan nagły”, „Kiedy nie czekać na wolny termin”, objawy wymagające natychmiastowej pomocy, numer telefonu) **są widoczne bez żadnej interakcji**: nigdy w zamkniętym `details`, zakładce ani karuzeli.
2. Nie twórz narzędzi, które „diagnozują” lub „oceniają” (kalkulatory, suwaki ryzyka, quizy objawów). `range-scale` i `triage-table` są *wizualizacją tabeli ze źródła*, ze wszystkimi zastrzeżeniami z tekstu widocznymi obok.
3. Strony z treścią o stanach nagłych mają w zasięgu wzroku numer telefonu i odnośnik do panelu „Poza godzinami pracy” (z home).

### R9. Progresywne ulepszanie i wydajność

1. Bez JS treść jest w pełni czytelna (menu może pozostać zwinięte jak na home; `details` działają natywnie; `sticky-cta` jest statycznym blokiem lub ukryty bez szkody).
2. `prefers-reduced-motion: reduce` — żadnego ruchu poza tym, co home już wyłącza; nowe przejścia opakuj w `@media (prefers-reduced-motion: no-preference)`.
3. Obrazy: `loading="lazy"`, `decoding="async"`, `width`/`height` (lub `aspect-ratio`), pierwszy obraz nad zgięciem bez `lazy`. Jeden arkusz CSS i jeden skrypt dodane do home; bez dodatkowych zapytań blokujących.

### R10. Organizacja CSS

1. `podstrony.css` ma sekcje oznaczone komentarzami: *podstawy podstron* → *bloki w kolejności z §7* → *reguły responsywne*. Każdy blok: komentarz z krótkim opisem i listą wariantów.
2. Używaj tokenów geometrii z home: `--s1…--s7` (8/13/21/34/55/89/144 px), `--gap`, `--gutter`, `--section-space`, `--content-gap`, `--group-gap`, `--row-gap`, `--column-rule-width`, `--column-rule-gap`, `--cols`, `--width`. Narożniki proste (`border-radius: 0`), linie 1 px, **zero cieni**. Punkty graniczne: 1000 px i 700 px (+ 600 i 480 tam, gdzie home je ma). Właściwości logiczne (`inline-size`, `margin-inline`) jak na home.
3. Bez `!important`, chyba że naśladujesz mechanizm home (np. `--weight-text`). Bez preprocesorów i frameworków. Zagnieżdżanie CSS dozwolone tylko tam, gdzie home je stosuje.
4. Zmiennych własnych bloków używaj do geometrii (odstępy, proporcje), **nie do kolorów**.

### R11. Generator jest idempotentny i nie nadpisuje cudzych plików

1. Generator zapisuje wyłącznie w `WYJŚCIE` i oznacza każdy wygenerowany plik komentarzem `<!-- generated: psyjaciele-podstrony -->` (CSS/JS: komentarz na początku).
2. Jeśli `WYJŚCIE` istnieje i zawiera plik bez tego znacznika — **nie nadpisuj**; zapisz całość do `podstrony-v2/` i napisz o tym w raporcie.
3. Ponowne uruchomienie daje identyczne pliki (deterministyczna kolejność, brak znaczników czasu poza polem `data-generated` w `_raport.md`).

### R12. Autonomia i uczciwość

Nie pytaj — decyduj i raportuj. Gdy brakuje narzędzia (np. przeglądarki), wykonaj kontrole statyczne i oznacz w raporcie, czego nie zweryfikowano. Nie ukrywaj niedociągnięć: „zrobione, ale nie sprawdzone w przeglądarce” jest akceptowalnym raportem; „zrobione” bez sprawdzenia — nie.

---

## 4. Pułapki techniczne (zweryfikowane na makiecie)

Każdą z poniższych rzeczy sprawdziłem na plikach i w przeglądarce. Traktuj je jako listę znanych min; w Etapie 1 potwierdź je u siebie (jeśli któraś już nie obowiązuje, napisz to w raporcie).

| # | Pułapka | Co robić |
|---|---|---|
| 1 | Serwer podglądu serwuje **tylko dokładne pliki**; adres katalogu (`…/zespol/`) kończy się 404. | Wszystkie linki wewnętrzne kończą się na `index.html`. Testuj `curl -I` na adresie katalogu, żeby wiedzieć, jak serwer się zachowuje. |
| 2 | Makieta jest publikowana w **podkatalogu** (GitHub Pages: `/psyjaciele-makieta/`). | Tylko ścieżki względne; bez `<base>`, bez adresów zaczynających się od `/`. Test V11 (serwer na katalogu nadrzędnym). |
| 3 | `minimal.js` rzuca wyjątek na podstronach (wymaga `.about`, `.portrait-halo`, `.portrait-circle`, `.booking-composition`). | Nie ładuj go; przenieś potrzebne funkcje do `podstrony.js` (R6). Aby przeczytać zminifikowany plik, sformatuj go (np. `npx prettier`) — nie zmieniaj oryginału. |
| 4 | **Adresy w zmiennych własnych** (`--art`, `--icon`, `--blob`, `--pet-atlas`). W Chromium `url()` w zmiennej rozwiązuje się względem **arkusza, który ją zużywa** (tu `minimal.css` w korzeniu), nie względem dokumentu; inne przeglądarki mogą się różnić. | (a) Ustawiaj je w `style` **dokładnie jak na home** (`url(assets/…)`, bez `ROOT`) — wtedy działają w Chromium. (b) `podstrony.js` przy starcie zamienia każdą taką wartość na bezwzględną: `new URL(ścieżka, new URL(document.body.dataset.root, location.href)).href` — to czyni zachowanie jednakowym wszędzie. (c) W `podstrony.css` **nie** zużywaj adresów przez `url(var(--x))` i nie pisz ścieżek do zasobów home bez przemyślenia (adres w `podstrony.css` liczy się od `podstrony/podstrony.css`; dozwolone `data:` lub jawne `../assets/…`). (d) Własności bezpośrednie (`mask-image: url()` w `style`) rozwiązują się względem dokumentu — tam użyj `ROOT`. |
| 5 | **Nagłówek jest `position: fixed`** i pływa nad treścią; jego wysokość zależy od szerokości (`--floating-header-height` ≈ 140 px > 1200 px, ≈ 205 px ≤ 1200; `--header-float-top`). `html { scroll-padding-top }` ≈ 144 px (110 px ≤ 700; 216 px ≤ 600). | Kotwice `#id` działają dzięki `scroll-padding-top`. Elementy `position: sticky` ustaw z `top: calc(var(--header-float-top) + var(--floating-header-height) + var(--s3))` (sprawdź aktualne zmienne). Pierwsza sekcja strony musi zostawić miejsce pod nagłówkiem — robi to `.hero` przez `padding-top` (§7 N1). |
| 6 | `.hero { height: 96svh; max-height: 96svh }` i `.hero > .wrap.grid { height: 100% … }` — hero home jest ekranowy. | Page-hero używa klasy `hero` (paleta + odstęp pod nagłówkiem), ale **nadpisuje** wysokość: `body.subpage .hero.page-hero { height: auto; max-height: none; min-height: 0 }`. Wewnętrzny kontener nazwij inaczej niż `.wrap.grid` (np. `.wrap.section-stack`), żeby nie uruchomić reguł `.hero > .wrap.grid`. |
| 7 | `main > section { overflow: clip }`. | Nic nie może wystawać poza sekcję (ujemne marginesy, wystające cienie są ucinane). `position: sticky` działa, bo `clip` nie tworzy kontenera przewijania — ale **nie** dawaj `overflow: hidden/auto/scroll` przodkom elementów przyklejonych. |
| 8 | **Globalna waga pisma:** `body :not(em, i, cite) { font-weight: var(--weight-text) !important }`, `--weight-text: 700`; `main .button` wymusza 900. | Hierarchię budujesz rozmiarem, wersalikami, Rialto i liniami. Wagę zmieniasz lokalnie **zmienną** `--weight-text`, nie `font-weight`. |
| 9 | Reguła ogólna **`[data-palette]`** ustawia kolory dzieci: `h1,h2,h3,.art,.icon` → `var(--ink)`; `p, cite, figcaption, dt, dd, td, address, .kicker…` → `var(--small-ink, var(--ink))`; `.portrait-circle, .halo-dot, .placeholder, .geometric-shape` → tło `var(--accent)`; `svg circle/ellipse/rect/polygon` → `fill: var(--accent)`; `.bento .tile::before` → tło `var(--accent)`. | Uwzględnij to w nowych blokach. W bloku odwróconym nadpisz kolory dzieci regułą o wyższej specyficzności (`body.subpage .alert-band.is-inverted :is(h3, p, dt, dd, li, a)` → `color: inherit`) i sprawdź **obliczone** kolory w przeglądarce. |
| 10 | Klasy-palety niosą **reguły kontekstowe**, np. `.emergency .poster-copy { min-height: clamp(560px,44vw,680px) }`, `.emergency .emergency-guide { margin-top: 112px }`, `.booking { padding: 0 … }`, `.services .bento …`, `#obserwuj-nas …`. | Wybierając klasę-paletę dla sekcji bez odpowiadającej jej zawartości, sprawdź w przeglądarce, czy żadna reguła kontekstowa nie zepsuła układu. Sekcje `emergency`, `booking`, `social-promo-section` mają własne, ciężkie kompozycje — używaj ich z odpowiednią zawartością (§6). |
| 11 | `section, footer { padding: var(--section-space) var(--gutter) }`, `main > section:not(.hero) > .wrap { padding-top: 0 }`, `.wrap { max-width: var(--width) }` (1280 px; 80vw od 2000 px). | Nie dodawaj własnych szerokości ani paddingów kontenerów sekcji. Odstępy między blokami w sekcji daje `.section-stack` (`gap: var(--group-gap)`). |
| 12 | **Strona główna nie ma `h1`.** Ogólny `h1 { font-size: var(--type-h1) }` ma 89 px, `h1 { --roman-heading-scale: var(--roman-h1-scale) }`; reguły `.hero-copy h1` nie mają zastosowania. Tytuły h1 podstron są długie (np. „Kardiologia weterynaryjna — badanie serca psów i kotów na Gocławiu”). | H1 podstrony wymaga własnego rozmiaru (np. `body.subpage .page-hero h1 { --mixed-title-size: clamp(40px, 5vw, 72px) }`) oraz składu mieszanego (§7 N1). Fakt braku `h1` na home zgłoś w raporcie. |
| 13 | Tytuły mieszane: `h1/h2:has(.heading-roman):has(em)`; rozmiar `--mixed-title-size: clamp(34px, 3.5vw, 48px)` (≤ 700 px: `clamp(20px, 5vw, 34px)`); `em` w nagłówku to Rialto Script (`--rialto-scale: 1.12`). | Składaj tytuły dokładnie jak home (§5.3). Nie ustawiaj `font-family` ręcznie. |
| 14 | `.button`: wypełnienie `var(--ink)`, tekst `var(--surface, var(--paper))`, `min-height: 55px`, wewnątrz `span.type-arrow` (→ wewnętrzne, ↗ zewnętrzne). | Nie stylizuj przycisków po swojemu. W blokach odwróconych zamień kolory zmiennymi (`background: var(--surface); color: var(--ink)`). Przycisk w nagłówku ma osobne reguły (`.header-grid > .button`). |
| 15 | `animacje.js` (działa na podstronach) dodaje `html.motion`, `rule-wait/rule-draw` do `.ruled-columns > div|article` i `.equipment-grid > div`, `is-boiling` do `.section-illustration` i `img.service-art`, pasek postępu, dryf `--drift`, kropkę „otwarte teraz” w nagłówku, zawija glify strzałek w `.type-arrow-glyph`, zaznacza pozycję menu przy linkach `#…`. | (a) Nowe bloki kolumnowe oparte na `.ruled-columns` dostają rysowanie linii za darmo. (b) `img.service-art` ma na home **stałe filtry kolorów** (`#service-light-ink`, `#service-hover-ink` w `<svg>` na końcu `<body>`); używaj tej klasy tylko w kopii kafli `bento` (hub) — i wtedy kopiuj też ten blok `<svg>` z home. (c) „Wrzenie” (`boil`) łączy się z własnym filtrem koloru tylko przy figurach z filtrem wbudowanym (§5.5); sprawdź w przeglądarce, że po włączeniu ruchu ilustracja nie traci koloru. |
| 16 | PNG ilustracji bywają dwojakie: **alfa-liniowe** (czarna kreska + przezroczystość: `service-<nazwa>.png`, `emergency-care-cole.png`, `sekcja-*-a/b/c.png`, `clinic-equipment-cole*.png`, `prepare-for-visit-cole.png`, `services-reception-*.png`) oraz z **białym wypełnieniem** (`*-first-frame.png`; `service-cardiology-b`, `service-internal-a`, `service-prevention-a`, `service-urology-a`). | Filtr „luminancja → alfa” z §5.5 działa dla obu rodzajów. Maska CSS (`mask-image`) działa tylko dla alfa-liniowych PNG i dla SVG. |
| 17 | Pliki SVG `cropped-*.svg`, `cole-*.svg` mają jednolite wypełnienie (`#030405`). | Nadają się na maskę (`span.art` z `--art`, jak w sekcji zespołu na home). Nie wstawiaj ich jako `<img>` — zostaną czarne. |
| 18 | Fonty: `Satoshi` (Regular, Medium, Bold, Black — `assets/fonts/*.woff2`) i `Rialto Script` (`assets/fonts/RialtoScript-Regular.otf`); `font-synthesis: none`. | Kopiuj z home linki `preload` (dwa Satoshi + Rialto). Nie używaj innych krojów ani pogrubiania/kursywy syntetycznej. |
| 19 | Kafle `bento` i karty `people` opierają się na `subgrid` (wspólne wiersze: tytuł / opis / ilustracja). | Nie zmieniaj struktury DOM kart i nie wkładaj wrapperów między `.tile` a jego dzieci. |
| 20 | Linie kolumn: `.ruled-columns > :is(div, article) { border-top: var(--column-rule-width) solid currentColor; padding-top: var(--column-rule-gap) }`; `.quote blockquote` bez linii. | Gdy nowy blok ma mieć taką linię i animację jej rysowania, użyj klasy `ruled-columns` na kontenerze i `div`/`article` jako dzieci. Linie wewnątrz komórek (tabele, listy) rób `border-top: 1px solid color-mix(in srgb, currentColor 25%, transparent)`. |
| 21 | Kafle usług na home wskazują **stare** statyczne podstrony (`uslugi-weterynaryjne/<slug>/index.html`). | W kopii kafli na hubie przemapuj `href` na nowe podstrony (R5). |
| 22 | Zdjęcia czarno-białe uzyskuje się w CSS (`filter: grayscale(1)`); studyjne tło zdjęć to jasna szarość (`#d4d4d4`, wyjątek dziedziczony). | Placeholdery zdjęć opisuj jako czarno-białe (§9). Nie dodawaj nowych szarości literalnych — tło ramki to `var(--accent)`. |
| 23 | `README.md` twierdzi, że animacje reagujące na scroll są wyłączone. | Nieaktualne: warstwa `animacje.css/js` jest aktywna. Wiarygodne jest to, co ładuje `index-min.html`. |
| 24 | Środowisko agenta może mieć ograniczony dostęp do sieci. | Wszystko, czego potrzebujesz, leży w `MAKIETA`; niczego nie pobieraj z zewnątrz. Narzędzia do testów (Playwright itp.) sprawdź lokalnie; jeśli ich brak, wykonaj kontrole statyczne i zaznacz to w raporcie. |

---

## 5. DNA wizualne strony głównej (to musi być widać na podstronach)

Jednym zdaniem: **płaskie, pełnoszerokie pola koloru; asymetryczne plakaty na siatce 12 kolumn; cienkie linie 1 px nad kolumnami tekstu; mały rozstrzelony kicker nad dużym tytułem w kursywie Rialto; narożniki proste, zero cieni; ilustracje liniowe w kolorze atramentu sekcji; czarno-białe zdjęcia; spokojny, „książkowy” tekst.**

### 5.1 Siatka i odstępy

| Element | Wartość |
|---|---|
| Siatka | `--cols: repeat(12, minmax(0, 1fr))`, kontener `.wrap` (`max-width: var(--width)` = 1280 px; od 2000 px `80vw`), wyśrodkowany |
| Marginesy / odstępy | `--gutter: clamp(24px, 4.2vw, 55px)` (24 px ≤ 700), `--gap: 32px` (24 px w 701–1000, 16 px ≤ 700), `--section-space: clamp(64px, 8vw, 104px)` (64 px ≤ 700), `--content-gap: 16px`, `--group-gap: 64px` (48 px ≤ 1000), `--row-gap: 64px` (48 px ≤ 1000) |
| Skala odstępów | `--s1…--s7` = 8, 13, 21, 34, 55, 89, 144 px (złoty podział) |
| Linie | `--column-rule-width: 1px`, `--column-rule-gap: var(--s3)`; linie ramek i kolumn w `currentColor`, linie pomocnicze `color-mix(in srgb, currentColor 25%, transparent)` |
| Narożniki, cienie | `* { border-radius: 0 }`; brak cieni; płaskie tła |
| Punkty graniczne | 1000 px i 700 px (+ 600 i 480 w kilku miejscach; nagłówek: 1200 i 1140 px) |
| Układ sekcji | `section > div.wrap.section-stack` (`display: grid; gap: var(--group-gap)`), wewnątrz bloki |

### 5.2 Typografia

- Krój: **Satoshi** (tekst i tytuły); **Rialto Script** wyłącznie w `em` wewnątrz nagłówków i w wybranych akcentach (cyfry spisu, „vs”).
- Tekst: 16/26 px; `body.book-type` włącza mikrotypografię z `typography-book.css`; długie teksty w `.book-prose` (łam 66ch, rytm akapitów, dzielenie wyrazów).
- Waga: wymuszona globalnie (`--weight-text: 700`) — hierarchia wynika z rozmiaru, **wersalików z rozstrzeleniem**, Rialto i linii, nie z wagi.
- Kicker: `.kicker` — 10/13 px, wersaliki, `letter-spacing: .12em`.
- Tytuły kolumn `h3` ≈ 26 px (24 px ≤ 700), `h4` ≈ 21 px, akapity w kolumnach do 38ch.
- Przyciski: `a.button` + `span.type-arrow` (`→` w obrębie serwisu, `↗` na zewnątrz); waga 900, `min-height: 55px`.

### 5.3 Wzorce tytułów (kopiuj dokładnie)

```html
<!-- (a) sam tytuł w kursywie Rialto — najczęstszy na home -->
<div class="poster-heading"><h2 id="…"><em>Nasze usługi</em></h2></div>

<!-- (b) kicker + tytuł -->
<div class="poster-heading"><span class="kicker">Przed wizytą</span><h2 id="…"><em>Jak do nas trafić</em></h2></div>

<!-- (c) tytuł mieszany: wersaliki (mały) nad Rialto (duży) -->
<h2 id="…"><span class="heading-roman">Przychodnię prowadzą<br>lekarki weterynarii</span><em>Ola i&nbsp;Magda</em></h2>
```

Tytuły z plików treści są długimi frazami (np. „Z jakimi objawami przyjść do internisty”). Reguła podziału (dla `h1` i `h2`): jeśli fraza ma ≤ 3 słowa lub ≤ 28 znaków → wzorzec (a), całość w `em`. W przeciwnym razie → wzorzec (c): `span.heading-roman` = początek frazy (do pierwszego myślnika/dwukropka/przecinka albo pierwsze 2–3 słowa), `em` = reszta (najważniejsze semantycznie końcowe słowa). **Nigdy nie zmieniaj ani nie pomijaj słów.** Pauza lub dwukropek między częściami zostaje w `<span class="visually-hidden">—</span>`, żeby czytnik ekranu odczytał nagłówek w całości. Generator dopuszcza ręczne nadpisanie podziału per tytuł (`split="Jak wygląda|konsultacja chirurgiczna"`).

### 5.4 Palety (zmienne sekcji) — dokumentacja, nie źródło prawdy

Paleta sekcji to pięć–osiem zmiennych ustawianych przez **klasę sekcji** w `minimal.css` (tokeny `--wp--preset--color--*` pochodzą z `design-tokens.css`). Stan z 8.10.2026 — **odczytaj aktualny z CSS skryptem**:

| Klasa sekcji | `--surface` (tło) | `--ink` (tytuły, linie, atrament ilustracji) | `--small-ink` (tekst) | `--accent` (ramki, placeholdery, plamy) | Dodatkowo |
|---|---|---|---|---|---|
| `hero` | green | peach | peach-light | green-soft | |
| `about` | peach-light | green | green-deep | peach | |
| `services` | sage | green | green-deep | sage-light | `--hover-ink`: blue |
| `booking` | green | peach | peach-light | orange | |
| `clinic` | paper | green | green-deep | peach-light | |
| `team` | peach | green | green-deep | peach-light | `--hover-ink`: green-deep, `--hover-accent`: paper |
| `reviews` | sage-light | green | green-deep | sage | |
| `emergency` | green | emergency-peach | peach-light | green-soft | |
| `arrival preparation` (także z `faq`) | paper | green | green-deep | sage-light | |
| `arrival` (bez `preparation`) | peach-light | green | green-deep | peach | |
| `contact` | blue | peach | peach-light | blue-deep | |
| `footer` (znacznik, nie klasa) | green | sage | sage-light | green-soft | |
| `social-promo-section` + `id="obserwuj-nas"` | peach (z reguły po `#id`) | green | green-deep | peach-light | `--social-promo-*` |

Dodatkowo: `.bento` i `.people` ustawiają `--surface: var(--card-surface)` (zamiana `surface` ↔ `accent`), a `.team .people .person` ma przezroczyste tło.

**Wnioski kompozycyjne:** (1) są 7 różnych powierzchni: zielona (hero, booking, emergency, stopka), papierowa (clinic, preparation/faq), jasna brzoskwiniowa (about, arrival), szałwiowa (services), jasna szałwiowa (reviews), brzoskwiniowa (team), niebieska (contact). (2) Na home sąsiednie sekcje **nigdy** nie mają tej samej powierzchni — podstrony trzymają tę samą zasadę. (3) Zielona i niebieska to pola „wysokiego kontrastu” — używaj ich oszczędnie w środku strony (hero na górze, kontakt na dole, pojedyncze pasy alarmowe).

Kolejność sekcji na home (rytm do naśladowania): `hero` (zielony) → `about` (jasna brzoskwinia) → `services` (szałwia) → `booking` (zielony) → `clinic` (papier) → `team` (brzoskwinia) → `reviews` (jasna szałwia) → `emergency` (zielony) → `preparation` (papier) → `arrival` (jasna brzoskwinia) → `faq` (papier) → `social-promo` (brzoskwinia) → `contact` (niebieski) → stopka (zielony).

### 5.5 Techniki obrazu (jedyne dozwolone)

**T1. Ilustracja liniowa w kolorze atramentu sekcji — filtr SVG osadzony w tej samej sekcji.** To technika z home (`#services-animation-ink` itd.). Filtr zamienia luminancję na przezroczystość (ciemna kreska → kryje, biel → znika), mnoży przez alfę źródła i wypełnia `var(--ink)`. Działa dla PNG alfa-liniowych i z białym wypełnieniem. `var(--ink)` w `flood-color` rozwiązuje się w kontekście elementu `<filter>`, dlatego **filtr musi leżeć wewnątrz sekcji (figury), której paleta ma go barwić**, i mieć unikalne `id` na stronie:

```html
<figure class="section-illustration poster-art" style="--art-ratio:1">
  <svg width="0" height="0" aria-hidden="true" style="position:absolute">
    <filter id="ink-hero" color-interpolation-filters="sRGB">
      <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -.2126 -.7152 -.0722 0 1"/>
      <feComposite in2="SourceGraphic" operator="in" result="lines"/>
      <feFlood flood-color="var(--ink)"/>
      <feComposite in2="lines" operator="in"/>
    </filter>
  </svg>
  <img src="ROOT/assets/illustrations/services/service-cardiology.png" alt="" width="1254" height="1254"
       decoding="async" style="width:100%;height:100%;object-fit:contain;filter:url(#ink-hero)">
</figure>
```

Generator numeruje identyfikatory (`ink-<strona>-<n>`). To jedyne miejsce, w którym w `style` pojawia się `filter` (jak na home).

**T2. Maska CSS dla SVG i PNG alfa-liniowych:** `span.art[aria-hidden="true"][style="--art:url(assets/…)"]` wewnątrz `figure.section-illustration` (jak sekcja zespołu na home); kolor to `currentColor`/`--ink` z reguł home. Adres w `--art` — jak w pułapce 4.

**T3. Zdjęcia:** `filter: grayscale(1)`; ramka z tłem `var(--accent)` i — tam, gdzie paleta jest jasna — `mix-blend-mode: multiply` na obrazie (kolor „przebija” przez jasne partie zdjęcia, jak druk na kolorowym papierze). W paletach ciemnych (`hero`, `booking`, `emergency`, `contact`, stopka) użyj wariantu `is-plain` (bez multiply).

**T4. Portret z plamą:** `div.portrait-blob[style="--blob:url(assets/shapes/shape-NN.svg)"] > img` (czarno-biały portret + obracany kształt; per-lekarka dostrojenia w `zespol-rejestr.css` działają **tylko** wewnątrz `.team .people .person`). Dostępne kształty: `shape-14/16/23/35.svg`.

**T5. Gotowe elementy kompozycji obrazu:** `figure.section-illustration.poster-art` (proporcja z `--art-ratio`), `.hero-art`, `.about-photo` (`portrait-circle` + `portrait-halo`), `.booking-photo` + `.booking-dog-foreground`, `.social-promo-photo`.

### 5.6 Ruch (korzystaj, nie dubluj)

Home ma warstwę `animacje.css/js` (aktywną): rysowanie linii nad kolumnami, „wrzenie” kreski ilustracji, kropka „otwarte teraz” przy godzinach w nagłówku, kropka „tu jesteś” w menu, strzałki przesuwające się przy najechaniu, gwiazdki ocen, pasek postępu przewijania, dryf ilustracji, podświetlenie kafli i kart przy najechaniu i na dotyku. Wszystko to masz „za darmo”, ładując `animacje.css` i `animacje.js`. Nowe bloki **nie dodają** własnych animacji wejścia; wolno dodać subtelne przejścia stanów (otwarcie `details`, najechanie), owinięte w `@media (prefers-reduced-motion: no-preference)`.

---

## 6. Katalog bloków ze strony głównej (do ponownego użycia)

Ta sekcja jest mapą. Aktualny markup bierzesz z `index-min.html` — **programowo** (parser HTML w generatorze), nie z pamięci. Skeletony poniżej pokazują kształt, żebyś wiedział, czego szukać; atrybuty pominięte w skrócie (`…`) kopiujesz z home.

### 6.1 Zestawienie

| Kod | Blok (klasy) | Gdzie na home | Zastosowanie na podstronach | Źródło markupu |
|---|---|---|---|---|
| H1 | **Nagłówek** `header.site-header[data-palette]` + `a.skip` + `div.header-backdrop` | globalnie | każda strona | kopia z home, linki przemapowane (R5) |
| H2 | **Stopka** `footer[data-palette]` (marka, zespół z portretami, nawigacja, kredyt) | globalnie | każda strona | kopia z home, linki przemapowane |
| H3 | **Hero** `section.hero` | początek | baza dla page-hero (N1) | wzorzec; własny kontener |
| H4 | **Plakat** `div.poster-grid` = `div.poster-copy` (`div.poster-heading` + `div.poster-bottom`) + `figure.section-illustration.poster-art` | 9 z 12 sekcji | page-hero; otwarcie wybranych rozdziałów (z ilustracją po prawej) | skeleton poniżej |
| H5 | **Kolumny szczegółów** `div.arrival-details.detail-columns.ruled-columns` (> `div` > `h3` + `div.detail-body` > `p`) | przygotowanie, dojazd, pytania | FAQ (gdy liczba pytań dzieli się przez 3), „Co zabrać”, równoległe krótkie wpisy | skeleton |
| H6 | **Siatka wyposażenia** `div.equipment-grid.detail-columns.ruled-columns` (> `div` > `h3` + `p`) | przychodnia | równoległe karty 3-kolumnowe (np. układy narządowe, rodzaje badań) | skeleton |
| H7 | **Kolumny kontaktu** `div.contact-columns.detail-columns.ruled-columns` (> `div.contact-column` > `h3` + `p`) | kontakt | zamknięcie każdej strony („Jak umówić…”) | skeleton |
| H8 | **Bento / kafel usługi** `div.bento.ruled-columns` > `article.tile` (`h3 > a`, `p.tile-description`, `img.service-art`) | usługi | **hub** (wszystkie kafle) | kopia kafli z home, `href` przemapowane |
| H9 | **Karty zespołu** `div.grid.people.ruled-columns` > `article.person` (`header > h3.person-name`, `ul.specializations`, `figure > div.portrait-blob > img`, `a.person-card-link`) | zespół, stopka | doctor-strip (N23), zespół | kopia kart z home (po `id` kotwicy) |
| H10 | **Opinie** `div.grid.quotes.ruled-columns` > `div.quote` > `blockquote` (`p` + `p.review-author`) + `div.review-source` | opinie | sekcja opinii na wybranych stronach | kopia z home (wybrane cytaty) |
| H11 | **Instrukcja kroków** `div.emergency-guide` (> `h3` + `ol.emergency-steps` > `li` > `h4` + `p`; `p.emergency-guide-source`) | nagłe przypadki | pilne i proceduralne listy z etykietami | skeleton; kontekst `.emergency` |
| H12 | **Panel „Poza godzinami pracy”** `div.after-hours.after-hours-panel[role=region]` (> `div.poster-heading` + `div.emergency-clinics` > `article` ×3 + `p`) | nagłe przypadki | strony z treścią o stanach nagłych | kopia z home (dane lecznic — **tylko** stąd) |
| H13 | **Rezerwacja (kompozycja)** `section.booking` (`div.booking-composition`: `booking-copy`, `booking-photo`, `booking-dog-foreground`, `booking-pets`) | zapraszamy | strony, na których można umówić się online | kopia sekcji z home; wymaga portu JS (pływające zwierzaki) |
| H14 | **Obserwuj nas** `section#obserwuj-nas.social-promo-section` | przed kontaktem | hub i zespół | kopia sekcji z home |
| H15 | **Założycielki** `section.about` (`figure.about-photo`: `portrait-halo`, `portrait-circle`, dymki `founder-hover`; `div.about-copy`) | o nas | zespół | kopia sekcji z home |
| H16 | **Kontakt (plakat + kolumny)** `section.contact` (`poster-grid` + H7) | kontakt | zamknięcie każdej strony | skeleton |
| H17 | **Przychodnia** `section.clinic` (`poster-grid` + H6) | przychodnia | wzorzec dla stron z „wyposażeniem”/etapami | skeleton |
| H18 | **Przygotowanie / pytania** `section.arrival.preparation[.faq]` (`poster-grid` + H5) | przygotowanie, pytania | „Jak się przygotować”, FAQ | skeleton |
| H19 | **Placeholder** `.placeholder` (obramowanie 1 px, tło `--accent`, `figcaption`) | CSS gotowe, w HTML nieużyte | wszystkie miejsca na obrazy (§9) | CSS home |
| H20 | **Elementy drobne** `a.button` + `span.type-arrow`, `span.kicker`, `span.heading-roman`, `span.icon[--icon]`, `hero-inline-pet` (dekoracyjne zdjęcie zwierzaka w tekście) | wszędzie | wszędzie | CSS home |

### 6.2 Skeletony kluczowych bloków

**Sekcja (szkielet każdej sekcji):**

```html
<section id="…" class="<klasa-palety>" data-palette="<etykieta z home>" aria-labelledby="<id-h2>">
  <div class="wrap section-stack">
    … bloki …
  </div>
</section>
```

**H4 Plakat:**

```html
<div class="poster-grid">
  <div class="poster-copy">
    <div class="poster-heading">
      <span class="kicker">Przed wizytą</span>
      <h2 id="…"><em>Przygotuj się na wizytę</em></h2>
    </div>
    <div class="poster-bottom">
      <p>…</p>
      <a class="button" href="…">Zadzwoń: 537 821 345 <span class="type-arrow" aria-hidden="true">→</span></a>
    </div>
  </div>
  <figure class="section-illustration poster-art" style="--art-ratio:1"> … ilustracja (T1/T2) … </figure>
</div>
```

`poster-copy` zajmuje kolumny 1–6, ilustracja 7–12; tytuł u góry, tekst i przycisk przy dolnej krawędzi (`min-height: var(--poster-intro-height)`); ≤ 700 px układ jednokolumnowy, ilustracja pod tekstem (`max-height: 360px`). `poster-bottom p` ma `max-inline-size: 36ch`.

**H5 Kolumny szczegółów (FAQ, przygotowanie):**

```html
<div class="arrival-details detail-columns ruled-columns">
  <div><h3>Jakie zwierzęta przyjmujecie?</h3><div class="detail-body"><p>Psy i&nbsp;koty.</p></div></div>
  <div> … </div>
</div>
```

Trzy kolumny ≥ 1001 px, dwie w 701–1000 px, jedna ≤ 700 px; wiersze wyrównane przez `subgrid`; `h3` ≈ 26 px; `p` do 38ch. Linia nad każdą kolumną rysuje się przy wejściu w okno (`animacje.js`).

**H6 Siatka wyposażenia:** `div.equipment-grid.detail-columns.ruled-columns > div > h3 + p` (trzy równe kolumny; wspólne wiersze tytuł/opis).

**H7 Kolumny kontaktu:**

```html
<div class="contact-columns detail-columns ruled-columns">
  <div class="contact-column"><h3>Adres</h3><p>…<br>…<br><a href="…">Pokaż w Google Maps <span class="type-arrow" aria-hidden="true">↗</span></a></p></div>
  <div class="contact-column"><h3>Kontakt</h3><p><a href="tel:+48537821345">+48 537 821 345</a><br><a href="mailto:…"><span>…</span></a> …</p></div>
  <div class="contact-column"> … </div>
</div>
```

**H8 Kafel usługi:**

```html
<div class="bento ruled-columns">
  <article class="tile">
    <h3><a aria-describedby="service-description-1" href="…">Choroby wew&shy;nętrzne</a></h3>
    <p class="tile-description" id="service-description-1">…</p>
    <img class="service-art" src="assets/illustrations/services/service-internal-a.png" alt="" width="800" height="800" loading="lazy" decoding="async">
  </article>
  … ×14 …
</div>
```

Cztery kolumny z 12 (`span 4`) w 3 rzędach; ≤ 1000 px po dwa; ≤ 700 px jeden. Zmień tylko `href`; dla każdego kafla zachowaj `id`/`aria-describedby` (unikalne na stronie).

**H9 Karta osoby:**

```html
<div class="grid people ruled-columns">
  <article class="person">
    <header><h3 class="person-name"><em>Magdalena</em> <span>Ostrowska</span></h3></header>
    <ul class="specializations"><li>choroby wewnętrzne</li> … </ul>
    <figure><div class="portrait-blob" style="--blob:url(assets/shapes/shape-16.svg)">
      <img loading="lazy" src="assets/3b64aaacd150-studio-tonal-v3.png" alt="Magdalena Ostrowska" width="1086" height="1448" decoding="async"></div></figure>
    <a class="person-card-link" href="…#Magda" aria-label="Magdalena Ostrowska — profil w zespole"></a>
  </article>
</div>
```

Portrety (tonalne PNG) i kształty: Magda `3b64aaacd150-studio-tonal-v3.png` (shape-16), Ola `e48db60840a2-…-v3` (shape-23), Julia `557c244c36a9-…-v3` (23), Małgosia `d9e0817d66ec-…-v3` (14), Kasia `5205d4b0e462-…-v3` (16), Olga `a6e997421073-…-v3` (23), Kinga `5be50d2b873b-studio-tonal-v4.png` (23). Dostrojenia obrazów w `zespol-rejestr.css` (`img[src*="<id>"]`) działają wyłącznie w `.team .people .person` — **karta musi leżeć w tym kontekście** (`section.team … div.people > article.person`). Specjalizacje na home: Magda — choroby wewnętrzne / nefrologia i urologia / anestezjologia; Ola — choroby wewnętrzne / stomatologia / ultrasonografia; Julia — choroby wewnętrzne; Małgosia — kardiologia; Kasia — chirurgia tkanek miękkich; Olga — ultrasonografia; Kinga — okulistyka (generator bierze je z home).

**H10 Opinia:** `div.quote > blockquote > p` + `p.review-author`; źródło: `div.review-source > span.icon[--icon:url(assets/min/icon-15.svg)] + p` (ocena i liczba opinii z home — kopiuj razem z datą „Dane z …”).

**H11 Instrukcja kroków:**

```html
<div class="emergency-guide" aria-labelledby="…">
  <h3 id="…">Co zrobić w nagłym przypadku?</h3>
  <ol class="emergency-steps">
    <li><h4>Zadzwoń do lecznicy</h4><p>…</p></li>
    …
  </ol>
</div>
```

Numery w kółkach pochodzą z licznika CSS na `h4::before`. Reguły kontekstowe w `.emergency …` — sprawdź w przeglądarce, że poza sekcją `emergency` blok wygląda poprawnie; w razie potrzeby powiel je w `podstrony.css` dla `body.subpage` (bez literałów koloru).

**H16 Kontakt (zamknięcie strony):**

```html
<section class="contact" data-palette="paper" id="kontakt" aria-labelledby="…">
  <div class="wrap section-stack">
    <div class="poster-grid">
      <div class="poster-copy"><div class="poster-heading"><h2 id="…"><em>Jak umówić czipowanie</em></h2></div>
        <div class="poster-bottom"><p>…</p></div></div>
      <figure class="section-illustration poster-art" style="--art-ratio:1.777777778"> … </figure>
    </div>
    <div class="contact-columns detail-columns ruled-columns"> … H7 … </div>
  </div>
</section>
```

### 6.3 Elementy, które kopiujesz z home programmatically (jedno źródło prawdy)

Generator czyta `index-min.html` i wyciąga: `<head>` (linki arkuszy z `?v=`, preloady, JSON-LD `VeterinaryCare`), nagłówek, stopkę, blok `<svg>` z filtrami na końcu `<body>` (tylko gdy strona używa kafli `bento`), sekcje H12–H15, wybrane cytaty (H10), dane NAP, mapowanie kafli (tytuł ↔ `href` ↔ ilustracja), słownik palet (klasa → `data-palette`). Wszystkie ścieżki i linki po wyciągnięciu przechodzą przez jedną funkcję `rewrite(html, page)` (R5). Dzięki temu zmiana na home (nowy numer telefonu, zmiana palety, nowy cytat) trafia na podstrony po ponownym uruchomieniu generatora.

---

## 7. Nowe bloki (N1–N27)

Wszystkie są **bezbarwne** (R2): kolor wyłącznie ze zmiennych sekcji. Zapisz je w `podstrony.css` i pokaż każdy w `_bloki.html` w ≥ 3 paletach (np. `hero`, `about`, `contact`). Poniżej: cel · markup · zasady CSS · responsywność/dostępność. Szczegóły geometrii dobierz w przeglądarce, trzymając się tokenów z §5.1.

**N1 `page-hero`** — wariant `hero` na górze każdej strony. `section.hero.page-hero[data-palette] > div.wrap.section-stack > div.poster-grid` (jak H4) + `dl.fact-strip` (N3). W `poster-heading`: `nav.breadcrumb` (N2), `span.kicker`, `h1` (skład mieszany wg §5.3: `span.heading-roman` + `visually-hidden` pauza + `em`). W `poster-bottom`: akapity wstępu (dosłownie), `p.cta-wizyta` (dosłownie) i `div.hero-actions` z przyciskami wyprowadzonymi z jego linków. Ilustracja: `figure.section-illustration.poster-art` z T1 (plik bazowy z tabeli §2.2). CSS: `body.subpage .hero.page-hero { height:auto; max-height:none; min-height:0 }`; własny rozmiar h1 (pułapka 12); `.visually-hidden` zdefiniuj (klip 1 px). Zachowaj `padding-top` z `.hero` (miejsce pod nagłówkiem).

**N2 `breadcrumb`** — `nav.breadcrumb[aria-label="Okruszki"] > ol > li`; ostatnia pozycja `aria-current="page"` bez linku; separator `li + li::before { content:"/" }`; 12 px, kapitaliki jak `.kicker`; kolor `currentColor`. Pozycje: Strona główna → Usługi (hub) → bieżąca (etykiety z §2.2). Na hubie, zespole i polityce: Strona główna → bieżąca.

**N3 `fact-strip`** — pasek 3–4 faktów pod plakatem: `dl.fact-strip > div > dt + dd`. `dt` = etykieta UI (≤ 2 słowa, kapitaliki 10 px), `dd` = wartość (21–34 px). Wartości muszą być **dosłownymi podciągami tekstu strony** (V1) — np. czipowanie: „15-cyfrowy”, „ISO”, „Safe-Animal”, „od około 8. tygodnia życia”; na stronach bez mocnych faktów użyj danych kontaktowych („537 821 345”, „9:00–20:00”, „Celownicza 4”). Komórki rozdzielone pionową linią 1 px (`border-inline-start`); ≤ 700 px 2×2.

**N4 `toc-index`** — spis treści na początku strony, w sekcji `clinic` (papier): `nav.toc-index[aria-labelledby] > p.kicker#toc-title + div.toc-grid.ruled-columns > div.toc-entry`. Wpis: `<em class="toc-number">01</em>` (Rialto) + link do `h2` + zagnieżdżona `ul` linków do jego `h3`. Wpisy i kolejność **identyczne z `nav.spis-tresci` w źródle**. Trzy kolumny (≥ 1001), dwie (701–1000), jedna (≤ 700). `div` jako dzieci → linie rysują się przez `animacje.js`.

**N5 `section-head`** — lekki nagłówek rozdziału: `header.section-head > span.kicker (numer 02) + h2 (wzorzec a/c z §5.3) + p.section-lead (tylko gdy rozdział zaczyna się akapitem)`. Używany w aside `split-feature` i nad szerokimi blokami; zamiast ciężkiego `poster-grid` w każdej sekcji.

**N6 `split-feature`** — kompozycja asymetryczna 4/7: `div.split-feature[.is-reversed] > div.split-aside + div.split-body`. Aside: kolumny 1–4, `position:sticky` (≥ 1001 px, `top` wg pułapki 5, `align-self:start`) — mieści `section-head` i opcjonalny placeholder; body: kolumny 6–12 (kolumna 5 pusta). `is-reversed` odbija układ. ≤ 1000 px: jedna kolumna, aside nad treścią, bez sticky. Główny „łamacz jednej kolumny” — używaj w większości rozdziałów.

**N7 `rail-layout`** — długie teksty z szyną nawigacji: `div.rail-layout > nav.rail-nav[aria-label="Rozdziały"] (p.kicker + ol > li > a) + div.rail-body`. Szyna sticky (≥ 1001 px), `podstrony.js` ustawia `aria-current="true"` na linku rozdziału w oknie (kropka „tu jesteś” jak w menu). ≤ 1000 px szyna jest zwykłą listą nad treścią. Użycie: polityka (szyna = spis treści), zespół (7 profili), choroby wewnętrzne (7 układów).

**N8 `ruled-list`** — `ul/ol.ruled-list`: bez punktorów domyślnych, wiersze oddzielone linią `color-mix(in srgb, currentColor 25%, transparent)`, znacznik `li::before` z kształtu CSS (pusty kwadrat 7 px z `currentColor`). Warianty: `is-numbered` (licznik CSS), `is-checklist` (ptaszek z borderów), `is-columns` (2 kolumny ≥ 701 px).

**N9 `ruled-table`** — `div.ruled-table[role="region"][tabindex="0"][aria-label] > table`. Nagłówki `th scope="col"` jako kicker; pierwsza kolumna `th scope="row"` (większa, 21 px); wiersze rozdzielone linią; bez zebry i ramek. ≤ 700 px: wiersze stają się blokami, `thead` ukryty wizualnie, komórki z `data-label` (tekst nagłówka dosłownie) w `td::before`. Warianty: `is-directory` (pierwsza kolumna to link + strzałka `→` na końcu wiersza; hub), `is-triage` (tabela „Objaw | Jak szybko”: druga kolumna jako wyróżniony „znacznik” z tekstu źródła; **bez** ocen własnych i bez kodowania kolorem).

**N10 `step-list`** — `ol.step-list > li`: duża cyfra Rialto (licznik CSS, `font-family: var(--font-emphasis)`), opcjonalnie tytuł (etykieta *run-in* → `h3`/`strong`) i tekst. ≥ 1001 px: do 4 kroków w rzędzie połączonych linią 1 px u góry; 5–6 kroków → 3 w rzędzie; ≤ 700 px pionowo z linią po lewej.

**N11 `phase-timeline`** — z tabeli „Etap | Kiedy | Co robimy” (szczepienia): `ol.phase-timeline > li > h3 (Etap) + p.phase-when (<span class="visually-hidden">Kiedy: </span>…) + p`. Oś pozioma z węzłami (kwadraty z `currentColor`) ≥ 1001 px, pionowa poniżej.

**N12 `duo`** — zestawienie dwóch stron: `div.duo > div.duo-head ×2 + (div.duo-row > p.duo-label + div.duo-cell ×2)…` z centralnym „vs” (`<em>` Rialto) — tylko dla tabel, w których nagłówki nazywają dwie strony (kardiologia „U psa | U kota”, nefrologia AKI | PChN, urologia „U psów | U kotów”). Wiersze wyrównane `subgrid`; ≤ 700 px strony jedna pod drugą z powtórzonym nagłówkiem. Zachowaj wszystkie komórki (także puste).

**N13 `range-scale`** — tabela ciśnienia (4 wiersze) jako segmentowa skala: `ol.range-scale > li` z podziałem na 4 równe segmenty, wypełnienie segmentu rośnie liniowo (`color-mix(in srgb, var(--ink) N%, transparent)` dla N = 10/25/45/70), etykiety (zakres, ocena, ryzyko) pod segmentem. Zastrzeżenie ze źródła widoczne obok. Tylko wizualizacja tabeli (R8).

**N14 `key-values`** — `dl.key-values > div > dt + dd` dla wierszy `<strong>Etykieta:</strong> wartość` (profile lekarek, „Jak umówić”); `dt` kicker, `dd` tekst; wiersze oddzielone linią.

**N15 `legal-prose`** — dokument prawny: `.book-prose` (66ch) + numeracja `h2` licznikiem CSS, `h3` mniejsze, listy numerowane z wcięciem, tabele jako `ruled-table`; w `rail-layout`. Zero placeholderów i ozdobników.

**N16 `alert-band`** — pas ostrzegawczy: `div.alert-band[role="note"][.is-inverted] > span.kicker (Pilne) + h3 + treść (p/ruled-list) + a.button (Zadzwoń…)`. Domyślnie ramka 1 px; `is-inverted` = `background:var(--ink); color:var(--surface)`, dzieci `color:inherit`, przycisk odwrócony. Treść pilna bywa w nim widoczna zawsze (R8). Jeśli pas stoi w sekcji `emergency`, nie odwracaj go.

**N17 `callout`** — `aside.callout > span.kicker (Ważne|Pamiętaj) + p`; lewa linia 3 px `currentColor`, tło `color-mix(in srgb, var(--ink) 6%, transparent)`.

**N18 `cta-band`** — powtórzone wezwanie w środku strony: `div.cta-band > p.cta-wizyta (dosłownie) + div.hero-actions`; duże odstępy, tytuł Rialto opcjonalnie „Umów wizytę” (UI).

**N19 `sticky-cta`** — pasek przy dolnej krawędzi ≤ 700 px, pojawia się po minięciu page-hero, znika przy sekcji `contact`/stopce (IntersectionObserver w `podstrony.js`): `div.sticky-cta > a.button (Umów wizytę) + a.button (Zadzwoń)`. Tło `var(--ink)` i tekst `var(--paper)` z `:root`, przyciski odwrócone; `padding-bottom` na `body` równy wysokości paska. Bez JS statyczny lub ukryty.

**N20 `faq-accordion`** — `div.faq-accordion > details.faq-item > summary > h3#id (pytanie) + div.faq-answer > p`. Linie 1 px, znacznik `+`/`−` z kształtu CSS, otwarcie animowane tylko w `no-preference`. `podstrony.js` otwiera `details` zawierający cel kotwicy z `location.hash`. Gdy liczba pytań dzieli się przez 3 i odpowiedzi są krótkie (≤ 380 znaków) — użyj zamiast tego H5 (kolumny z home).

**N21 `chooser`** — „którą usługę/lekarkę wybrać”: `ul.chooser > li > p`: zdanie ze źródła zostaje nietknięte, myślnik dzielący warunek i rekomendację zamieniony na dekoracyjną strzałkę `→` (`.type-arrow`); wiersze jako duże, klikalne pola z linkami ze źródła.

**N22 `related-tiles`** — „Zobacz też” (3–4 kafle powiązanych usług), wyglądem jak `tile` z `bento`, ale **bezbarwnie**: `div.related-tiles.ruled-columns > article > h3 > a + p + figure.section-illustration` z T1 (filtr osadzony w figurze). Tytuł i opis z kafla na home (programowo). Hover: `var(--hover-ink)` jeśli zdefiniowany, w przeciwnym razie `currentColor`.

**N23 `doctor-strip`** — lekarki prowadzące daną usługę: sekcja **`section.team`** z `div.grid.people.ruled-columns` zawierającym 1–3 kart `article.person` skopiowanych z home (H9) oraz `section-head`/akapit z listy „Kto przyjmuje” ze źródła. Karty tylko w kontekście `.team .people .person` (pułapka H9).

**N24 `photo-frame`** — placeholder obrazu (§9): `figure.placeholder.photo-frame[data-ph][data-kind][style="--ph-ratio:4/5"] > figcaption (tytuł + span opis)`. Warianty: `is-round`, `is-blob` (maska `--blob`), `is-plain` (bez multiply). Po wstawieniu pliku figura zachowuje proporcje i staje się obrazem czarno-białym (T3).

**N25 `figure-band`** — szeroki pas 21∶9 (pełna szerokość `.wrap`) z `photo-frame`, opcjonalnie nachodzący na niego `callout` (przesunięcie ujemnym `margin-block-start` — w granicach sekcji, pamiętaj o `overflow: clip`).

**N26 `figure-mosaic`** — 3 obrazy asymetrycznie: jeden duży (7 kolumn, 4∶5) i dwa małe (5 kolumn, 3∶2) w układzie `grid`; ≤ 700 px jedna kolumna.

**N27 `breath-counter`** *(opcjonalny, tylko kardiologia, sekcja „Jak liczyć oddechy w domu”)* — stoper 60 s + licznik kliknięć; po zakończeniu pokazuje **tylko liczbę** i zdanie ze źródła („zapisz wynik i pokaż lekarce” jeśli występuje w treści). Zero oceny, zero progów, zero kolorów stanu (R8).

**Własne bloki.** Możesz dodać kolejne, jeśli treść tego wymaga; zachowaj R1/R2/R10 i opisz w raporcie.

### Minimalny zestaw rdzeniowy (zrób najpierw)
N1–N6, N8–N10, N16, N17, N20, N24, N25 oraz kopie H4–H7, H12, H16. Reszta (N7, N11–N15, N18–N19, N21–N23, N26–N27, H8–H11, H13–H15) w Etapie 4–5.

---

## 7A. Specyfikacja szczegółowa nowych bloków (znaczniki, CSS, responsywność, a11y)

Zasady wspólne dla wszystkich reguł poniżej: (1) każdy selektor zaczyna się od `body.subpage`; (2) kolory wyłącznie `var(--ink)`, `var(--surface)`, `var(--small-ink)`, `var(--accent)`, `var(--hover-ink)`, `currentColor`, `color-mix(in srgb, <zmienna> N%, transparent)` — **zero literałów koloru** (R2); (3) odstępy i rozmiary z tokenów `--s1…--s7`, `--gap`, `--gutter`, `--content-gap`, `--column-rule-*`; (4) punkty graniczne 1000 / 700 px (jak home); (5) nazwę zmiennej kroju Rialto (w poniższych regułach `--font-emphasis`) **odczytaj z CSS home** (`grep -n "Rialto" minimal.css design-tokens.css`) i podstaw właściwą; (6) kod poniżej jest **szkicem punktu wyjścia** — dostrój geometrię w przeglądarce, ale nie zmieniaj struktury ani zasad kolorów.

### N1 `page-hero` (pełna specyfikacja)

```html
<section class="hero page-hero" id="poczatek" data-palette aria-labelledby="h1-id">
  <div class="wrap section-stack">
    <div class="poster-grid">
      <div class="poster-heading">
        <nav class="breadcrumb" aria-label="Okruszki">…</nav>
        <span class="kicker">Kardiologia</span>
        <h1 id="h1-id"><span class="heading-roman">Kardiologia weterynaryjna<span class="visually-hidden"> — </span></span><em>badanie serca psów i kotów na Gocławiu</em></h1>
      </div>
      <div class="poster-copy">
        <!-- akapity wstępu dosłownie, potem p.cta-wizyta dosłownie -->
        <div class="hero-actions"><a class="button" href="…">Umów wizytę <span class="type-arrow">→</span></a> <a class="button is-secondary" href="tel:…">Zadzwoń</a></div>
      </div>
      <figure class="section-illustration poster-art" style="--art-ratio:1">…T1…</figure>
    </div>
    <dl class="fact-strip">…</dl>
  </div>
</section>
```
Uwaga: `data-palette` bez wartości — paletę niesie **klasa** (`hero`); nie dodawaj `data-palette="…"` z nazwą, chyba że tak robi home (sprawdź w H1).

```css
body.subpage .hero.page-hero { height:auto; max-height:none; min-height:0; }
body.subpage .hero.page-hero .poster-grid { display:grid; grid-template-columns:var(--cols); column-gap:var(--gap); row-gap:var(--s5); align-items:end; }
body.subpage .hero.page-hero .poster-heading { grid-column:1 / span 8; display:grid; gap:var(--s3); }
body.subpage .hero.page-hero .poster-art      { grid-column:9 / span 4; grid-row:1 / span 2; align-self:center; aspect-ratio:var(--art-ratio,1); }
body.subpage .hero.page-hero .poster-copy     { grid-column:1 / span 6; display:grid; gap:var(--content-gap); }
body.subpage .page-hero h1 { --mixed-title-size:clamp(40px,5vw,72px); }
body.subpage .hero-actions { display:flex; flex-wrap:wrap; gap:var(--s2); margin-block-start:var(--s2); }
@media (max-width:1000px){ body.subpage .hero.page-hero .poster-heading,
  body.subpage .hero.page-hero .poster-copy { grid-column:1 / -1; }
  body.subpage .hero.page-hero .poster-art { grid-column:1 / -1; grid-row:auto; max-width:320px; } }
.visually-hidden { position:absolute; width:1px; height:1px; margin:-1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
```
`.button.is-secondary`: **nie** wprowadzaj nowego koloru — wariant to ramka `1px solid currentColor`, tło przezroczyste, tekst `var(--ink)`. Wariant dla hubu/polityki: pomiń `poster-art` (`poster-heading` na 12 kolumn).

### N2 `breadcrumb`
```css
body.subpage .breadcrumb ol { display:flex; flex-wrap:wrap; gap:0 var(--s2); list-style:none; margin:0; padding:0; }
body.subpage .breadcrumb li { font-size:12px; letter-spacing:.12em; text-transform:uppercase; }
body.subpage .breadcrumb li + li::before { content:"/"; margin-inline-end:var(--s2); opacity:.6; }
body.subpage .breadcrumb a { text-decoration:none; }
body.subpage .breadcrumb a:hover { text-decoration:underline; text-underline-offset:.25em; }
```
Minimalny obszar dotyku linków 24 px (padding-block). Kolor dziedziczony (`color: inherit`) — działa w każdej palecie.

### N3 `fact-strip`
```css
body.subpage .fact-strip { display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); margin:0; border-top:var(--column-rule-width) solid currentColor; }
body.subpage .fact-strip > div { padding:var(--s3) var(--s3) var(--s3) 0; }
body.subpage .fact-strip > div + div { border-inline-start:1px solid color-mix(in srgb, currentColor 25%, transparent); padding-inline-start:var(--s3); }
body.subpage .fact-strip dt { font-size:10px; letter-spacing:.12em; text-transform:uppercase; margin:0 0 var(--s1); }
body.subpage .fact-strip dd { margin:0; font-size:clamp(21px,2.4vw,34px); line-height:1.1; }
@media (max-width:700px){ body.subpage .fact-strip { grid-template-columns:1fr 1fr; }
  body.subpage .fact-strip > div:nth-child(odd) { border-inline-start:0; padding-inline-start:0; } }
```
Reguła doboru faktów: bierz **krótkie, konkretne** frazy (liczba, nazwa standardu, zakres czasu, adres) z pierwszych dwóch rozdziałów strony; sprawdź programowo, że każdy `dd` jest podciągiem `tekst_strony` (po normalizacji białych znaków i spacji niełamliwych). Brak pewnych faktów → użyj NAP (telefon, godziny, ulica). `dt` to etykieta UI z białej listy R4 (np. „Standard”, „Od kiedy”, „Telefon”, „Godziny”, „Adres”, „Dla kogo”).

### N4 `toc-index` (dopowiedzenie)
Źródło spisu: `nav.spis-tresci` z pliku treści (lub — gdy go brak — nagłówki `h2`/`h3` strony; kolejność i brzmienie identyczne z nagłówkami). `a[href]` = `#id` nagłówka; `id` nagłówków generuj deterministycznie ze slugu tytułu (polskie znaki → ASCII; kolizje `-2`). Wpis jest `div.toc-entry` (nie `li`), aby `animacje.js` rysował linię nad nim.
```css
body.subpage .toc-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:var(--row-gap) var(--gap); }
body.subpage .toc-entry { display:grid; grid-template-columns:auto 1fr; column-gap:var(--s3); align-content:start; }
body.subpage .toc-number { font-family:var(--font-emphasis); font-style:normal; font-size:clamp(34px,4vw,55px); line-height:1; }
body.subpage .toc-entry ul { grid-column:2; list-style:none; margin:var(--s2) 0 0; padding:0; font-size:14px; }
body.subpage .toc-entry ul a { display:block; padding-block:3px; }
@media (max-width:1000px){ body.subpage .toc-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:700px){ body.subpage .toc-grid { grid-template-columns:1fr; } }
```
Gdy `h2` jest ≤ 4, użyj układu poziomego z jednym rzędem. Link `h2` ma `font-size:21px`, linki `h3` mniejsze; `aria-current` nie ustawiaj (to nie szyna).

### N5 `section-head`
```css
body.subpage .section-head { display:grid; gap:var(--s2); }
body.subpage .section-head .kicker { display:flex; align-items:baseline; gap:var(--s2); }
body.subpage .section-head .kicker::after { content:""; flex:1; border-top:1px solid color-mix(in srgb, currentColor 25%, transparent); }
body.subpage .section-lead { max-width:38ch; }
```
Numer rozdziału w kickerze to numeracja UI (01, 02…) — nie dopisuj słów.

### N6 `split-feature` (rama większości rozdziałów)
```css
body.subpage .split-feature { display:grid; grid-template-columns:var(--cols); column-gap:var(--gap); row-gap:var(--s5); align-items:start; }
body.subpage .split-aside { grid-column:1 / span 4; display:grid; gap:var(--s4); }
body.subpage .split-body  { grid-column:6 / span 7; display:grid; gap:var(--s4); min-width:0; }
body.subpage .split-feature.is-reversed .split-aside { grid-column:9 / span 4; grid-row:1; }
body.subpage .split-feature.is-reversed .split-body  { grid-column:1 / span 7; grid-row:1; }
@media (min-width:1001px){ body.subpage .split-aside { position:sticky; align-self:start;
  top:calc(var(--header-float-top) + var(--floating-header-height) + var(--s3)); } }
@media (max-width:1000px){ body.subpage .split-aside, body.subpage .split-body,
  body.subpage .split-feature.is-reversed > * { grid-column:1 / -1; grid-row:auto; } }
```
Zasady użycia: aside = `section-head` + (opcjonalnie) 1 placeholder (N24) lub `callout`; body = prozę `.book-prose`, listy, tabele, kroki. Nigdy dwa sąsiednie rozdziały w tej samej orientacji, jeśli oba mają aside z obrazem — przeplataj `is-reversed`. Jeśli aside jest wyższy niż okno, sticky wyłącz (`@media (max-height:700px){position:static}`).

### N8 `ruled-list`
```css
body.subpage .ruled-list { list-style:none; margin:0; padding:0; counter-reset:rl; }
body.subpage .ruled-list > li { position:relative; padding:var(--s2) 0 var(--s2) var(--s4); border-top:1px solid color-mix(in srgb, currentColor 25%, transparent); }
body.subpage .ruled-list > li:last-child { border-bottom:1px solid color-mix(in srgb, currentColor 25%, transparent); }
body.subpage .ruled-list > li::before { content:""; position:absolute; inset-inline-start:0; top:calc(var(--s2) + .55em); width:7px; height:7px; border:1px solid currentColor; }
body.subpage .ruled-list.is-numbered > li { counter-increment:rl; }
body.subpage .ruled-list.is-numbered > li::before { content:counter(rl, decimal-leading-zero); border:0; width:auto; height:auto; top:var(--s2); font-size:12px; letter-spacing:.12em; }
body.subpage .ruled-list.is-checklist > li::before { width:5px; height:10px; border-width:0 1px 1px 0; transform:rotate(40deg); top:calc(var(--s2) + .2em); inset-inline-start:3px; }
@media (min-width:701px){ body.subpage .ruled-list.is-columns { columns:2; column-gap:var(--gap); } body.subpage .ruled-list.is-columns > li { break-inside:avoid; } }
```
Zastosowanie: każda lista `ul/ol` ze źródła, która nie jest krokami (N10) ani profilem (N14). Lista pozycji ≥ 8 krótkich (≤ 6 słów) → `is-columns`. Lista „zabierz ze sobą / przygotuj” → `is-checklist`.

### N9 `ruled-table`
```html
<div class="ruled-table" role="region" tabindex="0" aria-label="Tytuł tabeli (dosłownie z najbliższego nagłówka)">
  <table><thead><tr><th scope="col">Objaw</th><th scope="col">Jak szybko</th></tr></thead>
  <tbody><tr><th scope="row">…</th><td data-label="Jak szybko">…</td></tr></tbody></table>
</div>
```
```css
body.subpage .ruled-table { overflow-x:auto; }
body.subpage .ruled-table table { width:100%; border-collapse:collapse; }
body.subpage .ruled-table th[scope=col] { text-align:start; font-size:10px; letter-spacing:.12em; text-transform:uppercase; padding:var(--s2) var(--s3) var(--s2) 0; border-bottom:var(--column-rule-width) solid currentColor; }
body.subpage .ruled-table th[scope=row] { text-align:start; font-size:21px; line-height:1.2; padding:var(--s3) var(--s3) var(--s3) 0; }
body.subpage .ruled-table td { padding:var(--s3) var(--s3) var(--s3) 0; vertical-align:top; }
body.subpage .ruled-table tbody tr { border-bottom:1px solid color-mix(in srgb, currentColor 25%, transparent); }
body.subpage .ruled-table:focus-visible { outline:2px solid currentColor; outline-offset:4px; }
@media (max-width:700px){
  body.subpage .ruled-table thead { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }
  body.subpage .ruled-table tr, body.subpage .ruled-table th, body.subpage .ruled-table td { display:block; }
  body.subpage .ruled-table td::before { content:attr(data-label); display:block; font-size:10px; letter-spacing:.12em; text-transform:uppercase; margin-bottom:2px; }
}
```
`is-directory` (hub): wiersz = `th[scope=row] > a` + opis + `td.row-go` ze `span.type-arrow`; cały wiersz klikalny przez `a::after{content:"";position:absolute;inset:0}` i `tr{position:relative}`. `is-triage`: druga kolumna w `td > strong` (dosłowny tekst), bez koloru stanu. Puste komórki zachowaj (`<td></td>` + `data-label`). Generator wykrywa liczbę kolumn i dodaje `data-label` z tekstu `th` odpowiedniej kolumny.

### N10 `step-list`
```css
body.subpage .step-list { list-style:none; margin:0; padding:0; counter-reset:st; display:grid; gap:var(--row-gap) var(--gap); grid-template-columns:repeat(var(--steps,3),minmax(0,1fr)); }
body.subpage .step-list > li { counter-increment:st; border-top:var(--column-rule-width) solid currentColor; padding-top:var(--column-rule-gap); display:grid; gap:var(--s2); align-content:start; }
body.subpage .step-list > li::before { content:counter(st); font-family:var(--font-emphasis); font-size:clamp(44px,5vw,72px); line-height:.9; }
body.subpage .step-list h3 { font-size:21px; }
@media (max-width:1000px){ body.subpage .step-list { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:700px){ body.subpage .step-list { grid-template-columns:1fr; } body.subpage .step-list > li { border-top:0; border-inline-start:1px solid currentColor; padding:0 0 0 var(--s3); } }
```
Generator ustawia inline `style="--steps:N"` dla N ≤ 4 (5–6 → `--steps:3`). Nagłówek kroku = etykieta *run-in* (tekst przed dwukropkiem/kropką, jeśli wyraźnie krótka etykieta ≤ 6 słów), reszta w `p`; brak etykiety → sam `p`. Kroki mogą mieć `ol.step-list` w `split-body` (wtedy `--steps:1` i układ pionowy z szeroką cyfrą po lewej: `grid-template-columns:auto 1fr`).

### N16 `alert-band` (pułapka odwrócenia palety)
```html
<div class="alert-band is-inverted" role="note"><span class="kicker">Pilne</span><h3>Kiedy nie czekać na wizytę</h3><ul class="ruled-list">…</ul><a class="button" href="tel:…">Zadzwoń <span class="type-arrow">→</span></a></div>
```
```css
body.subpage .alert-band { border:1px solid currentColor; padding:var(--s4); display:grid; gap:var(--s3); }
body.subpage .alert-band.is-inverted { background:var(--ink); color:var(--surface); border-color:var(--ink); }
body.subpage .alert-band.is-inverted :is(.kicker,h3,p,li,dt,dd,a:not(.button),strong) { color:inherit; }
body.subpage .alert-band.is-inverted .ruled-list > li { border-color:color-mix(in srgb, var(--surface) 35%, transparent); }
body.subpage .alert-band.is-inverted .button { background:var(--surface); color:var(--ink); }
```
Test w V-palet (Appendix A): kontrast tekstu `--surface` na `--ink` ≥ 4,5:1 w każdej z palet użytych na stronach; jeśli któraś paleta tego nie spełnia (np. `--ink` jasny), użyj wariantu bez inwersji (sama ramka).

### N17 `callout`
```css
body.subpage .callout { border-inline-start:3px solid currentColor; padding:var(--s3) var(--s4); background:color-mix(in srgb, var(--ink) 6%, transparent); display:grid; gap:var(--s1); max-width:56ch; }
```
Nie nadawaj `role`. Treść: dosłowny akapit ze źródła, który zaczyna się od „Ważne”, „Pamiętaj”, „Uwaga” lub jest wyróżnioną uwagą w źródle (blockquote/aside).

### N20 `faq-accordion`
```css
body.subpage .faq-accordion { display:grid; border-bottom:1px solid currentColor; }
body.subpage .faq-item { border-top:1px solid currentColor; }
body.subpage .faq-item > summary { list-style:none; cursor:pointer; display:flex; justify-content:space-between; align-items:baseline; gap:var(--s3); padding:var(--s3) 0; }
body.subpage .faq-item > summary::-webkit-details-marker { display:none; }
body.subpage .faq-item > summary h3 { font-size:clamp(18px,2vw,24px); margin:0; }
body.subpage .faq-item > summary::after { content:"+"; font-size:28px; line-height:1; flex:none; }
body.subpage .faq-item[open] > summary::after { content:"−"; }
body.subpage .faq-answer { padding:0 0 var(--s4); max-width:62ch; }
body.subpage .faq-item > summary:focus-visible { outline:2px solid currentColor; outline-offset:2px; }
```
Pierwsze pytanie zostaje otwarte tylko wtedy, gdy lista ma ≥ 6 pozycji. Pytania (`h3`) i odpowiedzi dosłownie; `FAQPage` JSON-LD tylko gdy strona ma ≥ 3 pytania i każda odpowiedź jest widoczna (R7). Cel kotwicy w zwiniętym `details` → `podstrony.js` ustawia `open`.

### N24 `photo-frame` (placeholder)
```html
<figure class="placeholder photo-frame" data-ph="czip-01" data-kind="photo" style="--ph-ratio:4/5">
  <figcaption><strong>Zdjęcie: lekarka skanuje czytnikiem bark psa</strong><span>Czarno-białe, 4∶5 · plik: assets/podstrony/czipowanie/czip-01.jpg</span></figcaption>
</figure>
```
```css
body.subpage .photo-frame { margin:0; aspect-ratio:var(--ph-ratio,4/5); position:relative; overflow:hidden; display:grid; place-items:center; text-align:center; padding:var(--s3);
  background:var(--accent); border:1px dashed currentColor; }
body.subpage .photo-frame figcaption { display:grid; gap:var(--s1); font-size:13px; max-width:28ch; }
body.subpage .photo-frame figcaption span { font-size:10px; letter-spacing:.12em; text-transform:uppercase; }
body.subpage .photo-frame > img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:grayscale(1); mix-blend-mode:multiply; }
body.subpage .photo-frame.is-plain > img { mix-blend-mode:normal; }
body.subpage .photo-frame.is-round { border-radius:0; clip-path:circle(50% at 50% 50%); }
body.subpage .photo-frame.is-blob { -webkit-mask:var(--blob) center/contain no-repeat; mask:var(--blob) center/contain no-repeat; border:0; }
body.subpage .photo-frame.has-image { border:0; display:block; padding:0; }
body.subpage .photo-frame.has-image figcaption { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); }
```
(Okrąg przez `clip-path` — to nie `border-radius`, więc zgodne z zasadą „zero zaokrągleń” home, który używa okręgów w `portrait-circle`.) Po wstawieniu pliku użytkownik dodaje `<img src="…" alt="…" width height loading="lazy" decoding="async">` jako pierwsze dziecko i klasę `has-image` — **opisz tę procedurę w komentarzu HTML pod każdym placeholderem** i w `OBRAZY.md` (§9). Plik nie istnieje → placeholder pozostaje widoczny; brak błędów 404 (nie dodawaj `<img>` z nieistniejącym `src`).

### N25 `figure-band`
```css
body.subpage .figure-band { position:relative; display:grid; }
body.subpage .figure-band .photo-frame { aspect-ratio:21/9; }
body.subpage .figure-band .callout { position:absolute; inset-inline-start:var(--s4); inset-block-end:calc(var(--s4) * -1); max-width:42ch; background:var(--surface); }
@media (max-width:700px){ body.subpage .figure-band .photo-frame { aspect-ratio:4/3; } body.subpage .figure-band .callout { position:static; } }
```
Dolny margines sekcji musi zrekompensować nachodzenie (`padding-block-end:var(--s4)` na kontenerze), bo `main>section{overflow:clip}` ucina wystające elementy.

### N26 `figure-mosaic`
```css
body.subpage .figure-mosaic { display:grid; grid-template-columns:var(--cols); gap:var(--gap); }
body.subpage .figure-mosaic > :nth-child(1) { grid-column:1 / span 7; grid-row:1 / span 2; --ph-ratio:4/5; }
body.subpage .figure-mosaic > :nth-child(2) { grid-column:8 / span 5; --ph-ratio:3/2; }
body.subpage .figure-mosaic > :nth-child(3) { grid-column:8 / span 5; --ph-ratio:3/2; }
@media (max-width:700px){ body.subpage .figure-mosaic > * { grid-column:1 / -1; grid-row:auto; } }
```
Wersja lustrzana `is-reversed` zamienia kolumny. Pokazuj mozaiki tylko na stronach z ≥ 5 placeholderami (§9).

### N7 `rail-layout`
```css
body.subpage .rail-layout { display:grid; grid-template-columns:var(--cols); column-gap:var(--gap); row-gap:var(--s5); }
body.subpage .rail-nav { grid-column:1 / span 3; }
body.subpage .rail-body { grid-column:5 / span 8; min-width:0; display:grid; gap:var(--group-gap); }
@media (min-width:1001px){ body.subpage .rail-nav { position:sticky; align-self:start; top:calc(var(--header-float-top) + var(--floating-header-height) + var(--s3)); } }
body.subpage .rail-nav ol { list-style:none; margin:var(--s2) 0 0; padding:0; font-size:14px; }
body.subpage .rail-nav a { display:block; padding:6px 0 6px var(--s3); position:relative; border-top:1px solid color-mix(in srgb, currentColor 25%, transparent); text-decoration:none; }
body.subpage .rail-nav a[aria-current="true"]::before { content:""; position:absolute; inset-inline-start:0; top:50%; width:7px; height:7px; background:currentColor; transform:translateY(-50%); }
@media (max-width:1000px){ body.subpage .rail-nav, body.subpage .rail-body { grid-column:1 / -1; } }
```
`podstrony.js`: `IntersectionObserver` (`rootMargin: "-30% 0px -60% 0px"`) ustawia `aria-current="true"` na linku, którego cel jest w oknie; brak JS → szyna działa jako zwykła lista linków.

### N11 `phase-timeline`
```css
body.subpage .phase-timeline { list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(var(--phases,4),minmax(0,1fr)); gap:var(--gap); position:relative; }
body.subpage .phase-timeline > li { position:relative; padding-top:var(--s4); border-top:1px solid currentColor; display:grid; gap:var(--s1); align-content:start; }
body.subpage .phase-timeline > li::before { content:""; position:absolute; top:-5px; inset-inline-start:0; width:9px; height:9px; background:currentColor; }
body.subpage .phase-when { font-family:var(--font-emphasis); font-size:clamp(21px,2.4vw,34px); line-height:1.1; }
@media (max-width:1000px){ body.subpage .phase-timeline { grid-template-columns:1fr; border-inline-start:1px solid currentColor; gap:var(--s4); }
  body.subpage .phase-timeline > li { border-top:0; padding:0 0 0 var(--s4); }
  body.subpage .phase-timeline > li::before { top:.4em; inset-inline-start:-5px; } }
```
Generator ustawia `--phases` = liczba wierszy (≤ 5; więcej → zwykły `ruled-table`).

### N12 `duo`
```css
body.subpage .duo { display:grid; grid-template-columns:minmax(0,1fr) auto minmax(0,1fr); column-gap:var(--gap); }
body.subpage .duo-head { font-size:clamp(21px,2.4vw,34px); border-bottom:var(--column-rule-width) solid currentColor; padding-bottom:var(--s2); }
body.subpage .duo-vs { font-family:var(--font-emphasis); font-style:normal; align-self:center; }
body.subpage .duo-row { grid-column:1 / -1; display:grid; grid-template-columns:subgrid; padding-block:var(--s3); border-bottom:1px solid color-mix(in srgb, currentColor 25%, transparent); }
body.subpage .duo-label { grid-column:1 / -1; font-size:10px; letter-spacing:.12em; text-transform:uppercase; }
body.subpage .duo-cell:nth-of-type(1){ grid-column:1; } body.subpage .duo-cell:nth-of-type(2){ grid-column:3; }
@media (max-width:700px){ body.subpage .duo, body.subpage .duo-row { grid-template-columns:1fr; } body.subpage .duo-cell:nth-of-type(n){ grid-column:1; } body.subpage .duo-cell::before { content:attr(data-side); display:block; font-size:10px; letter-spacing:.12em; text-transform:uppercase; } }
```
Każda `duo-cell` ma `data-side` = dosłowny nagłówek strony (np. „U psa”). Uwaga: nagłówek-wiersz `duo-head` ×2 + `span.duo-vs` w środku w jednym wierszu siatki.

### N13 `range-scale`
```css
body.subpage .range-scale { list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:2px; }
body.subpage .range-scale > li { display:grid; gap:var(--s1); align-content:start; }
body.subpage .range-scale > li::before { content:""; height:var(--s4); background:color-mix(in srgb, var(--ink) var(--fill,10%), transparent); border:1px solid currentColor; }
body.subpage .range-scale > li:nth-child(1){--fill:10%} body.subpage .range-scale > li:nth-child(2){--fill:25%} body.subpage .range-scale > li:nth-child(3){--fill:45%} body.subpage .range-scale > li:nth-child(4){--fill:70%}
@media (max-width:700px){ body.subpage .range-scale { grid-template-columns:1fr; } }
```
Zawsze razem z `<table>` w `details` albo `visually-hidden` (wersja tabelaryczna dla czytników), plus zastrzeżenie ze źródła (R8).

### N14 `key-values`
```css
body.subpage .key-values { margin:0; display:grid; }
body.subpage .key-values > div { display:grid; grid-template-columns:minmax(120px,1fr) 3fr; gap:var(--s3); padding:var(--s2) 0; border-top:1px solid color-mix(in srgb, currentColor 25%, transparent); }
body.subpage .key-values dt { font-size:10px; letter-spacing:.12em; text-transform:uppercase; padding-top:.4em; }
body.subpage .key-values dd { margin:0; }
@media (max-width:700px){ body.subpage .key-values > div { grid-template-columns:1fr; gap:var(--s1); } }
```

### N15 `legal-prose`
```css
body.subpage .legal-prose { counter-reset:lp; max-width:66ch; }
body.subpage .legal-prose h2 { counter-increment:lp; font-size:clamp(21px,2.2vw,28px); margin-block:var(--s5) var(--s2); }
body.subpage .legal-prose h2::before { content:counter(lp) ". "; }
body.subpage .legal-prose ol, body.subpage .legal-prose ul { padding-inline-start:var(--s4); }
```
Jeśli nagłówki źródła już zawierają numerację, **nie** dodawaj licznika (usuń `::before`). Zero placeholderów.

### N18 `cta-band`
```css
body.subpage .cta-band { display:grid; grid-template-columns:var(--cols); gap:var(--gap); align-items:center; border-block:var(--column-rule-width) solid currentColor; padding-block:var(--s5); }
body.subpage .cta-band > p { grid-column:1 / span 7; font-size:clamp(21px,2.6vw,34px); line-height:1.2; }
body.subpage .cta-band .hero-actions { grid-column:9 / span 4; justify-content:flex-end; }
@media (max-width:1000px){ body.subpage .cta-band > * { grid-column:1 / -1; justify-content:flex-start; } }
```

### N19 `sticky-cta`
```css
body.subpage .sticky-cta { display:none; }
@media (max-width:700px){ body.subpage .sticky-cta { display:flex; gap:var(--s2); position:fixed; inset:auto 0 0 0; z-index:20; padding:var(--s2) var(--gutter); background:var(--ink-page, var(--wp--preset--color--green)); transform:translateY(110%); }
  body.subpage .sticky-cta.is-visible { transform:none; }
  body.subpage .sticky-cta .button { flex:1; background:var(--wp--preset--color--paper); color:var(--wp--preset--color--green); } }
@media (prefers-reduced-motion:no-preference){ body.subpage .sticky-cta { transition:transform .25s; } }
```
Pasek leży poza sekcjami (bezpośrednio w `body`), więc nie ma zmiennych sekcji — tu **jedyne** dopuszczalne użycie tokenów globalnych `--wp--preset--color--*` (zgodnie z R2.4: deklaracje globalne, nie literały). Wybierz parę zielony/papier, jak stopka i nagłówek home; sprawdź dokładne nazwy tokenów w `design-tokens.css`.

### N21 `chooser`
```css
body.subpage .chooser { list-style:none; margin:0; padding:0; display:grid; border-bottom:1px solid currentColor; }
body.subpage .chooser > li { border-top:1px solid currentColor; }
body.subpage .chooser > li > p { margin:0; padding:var(--s3) 0; display:flex; gap:var(--s3); align-items:baseline; font-size:clamp(18px,2vw,24px); }
body.subpage .chooser .type-arrow { flex:none; }
```
Zdanie ze źródła nie może zostać przepisane: generator dzieli je na `span` (warunek) + `span.type-arrow` + `span` (rekomendacja) tylko tam, gdzie oryginał ma myślnik/„→”; reszta zdania bez zmian.

### N22 `related-tiles`
```css
body.subpage .related-tiles { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:var(--gap); }
body.subpage .related-tiles > article { display:grid; grid-template-rows:subgrid; grid-row:span 3; gap:var(--s2); }
body.subpage .related-tiles h3 a { text-decoration:none; }
body.subpage .related-tiles h3 a::after { content:""; position:absolute; inset:0; }
body.subpage .related-tiles > article { position:relative; }
body.subpage .related-tiles > article:hover { color:var(--hover-ink, currentColor); }
```
Dobór kafli: z mapy powiązań `RELATED` w generatorze (patrz §10; maks. 4), tytuł i opis z kafla home dla tej usługi.

### N23 `doctor-strip`
Nie wymaga nowego CSS: ponownie użyj `section.team` + `.people` + `article.person` (H9). Dodaj `p.section-lead` nad kartami. Gdy usługę prowadzi jedna lekarka, `grid` kart zajmuje 4 kolumny i dopełnij 8 kolumn `split-feature`-owym aside z tekstem „Kto przyjmuje”.

### N27 `breath-counter` (opcjonalny)
```css
body.subpage .breath-counter { display:grid; gap:var(--s3); border:1px solid currentColor; padding:var(--s4); max-width:420px; }
body.subpage .breath-counter output { font-family:var(--font-emphasis); font-size:clamp(55px,8vw,89px); line-height:1; }
```
JS w `podstrony.js` (moduł `initBreathCounter`): `button` start/stop 60 s (`aria-live="polite"` na `output`), licznik kliknięć `button`; po 60 s wyświetla tylko liczbę. Zero progów i ocen (R8).

---

## 8. Dobór bloków do treści i rytm palet

### 8.1 Wzorzec treści → blok

| Wzorzec w źródle | Blok |
|---|---|
| Lead i `cta-wizyta` | N1 (page-hero) |
| `nav.spis-tresci` | N4 |
| `ul` zdań (objawy, zalecenia) | N8; pilne → N16 |
| `ul` z `<strong>Etykieta:</strong>` | N14 lub H5/H6 (3 kolumny: etykieta jako `h3`) |
| `ol` bez etykiet | N10 (bez tytułów) lub N8 `is-numbered` |
| `ol`/`ul` z etykietą *run-in* („Rozmowa. …”, „Rana: …”) | N10 z tytułami lub H11 (`emergency-guide`) |
| Pilna lista („to stan nagły”, „Kiedy nie czekać”) | N16 `is-inverted` + H12 |
| Tabela 2 kolumny z nazwanymi stronami | N12 |
| Tabela „Objaw / Jak szybko” | N9 `is-triage` |
| Tabela „Etap / Kiedy / Co robimy” | N11 |
| Tabela zakresów (ciśnienie) | N13 + N9 |
| Inna tabela (2–3 kolumny) | N9; w hubie `is-directory` |
| Sekcja pytań | H5 (liczba pytań podzielna przez 3, krótkie odpowiedzi) albo N20 |
| Zdanie-ostrzeżenie, „Pamiętaj” | N17 |
| Kilka równoległych krótkich akapitów z h3 (układy narządowe, rodzaje badań) | H6 / H5 lub N7 |
| „Kto przyjmuje” / lekarki | N23 |
| „Nie wiesz, którą wybrać?” | N21 |
| Zamknięcie „Jak umówić…” | H16 (H7 z wierszy listy: `<strong>` → `h3`) |
| Tekst prawny | N7 + N15 |

### 8.2 Rytm palet

1. Strona zaczyna się od `hero` (zielony), potem `clinic` (papier, spis treści), kończy `contact` (niebieski) i stopką (zielona).
2. Sąsiednie sekcje **nie mają tej samej powierzchni** (§5.4). Środek strony przeplataj: `about` → `services` → `team` → `reviews` → `arrival preparation faq` → `arrival`. Sekcja FAQ ma zwykle paletę `arrival preparation faq`.
3. Zieloną (`emergency`, `booking`) wstawiaj ≤ 2 razy na stronę, nie obok siebie.
4. Każda strona ma ≥ 4 różne palety; paletę wybiera generator ze słownika ról (jedno miejsce w kodzie), nie ręcznie w każdej sekcji.

### 8.3 Minimum pokrycia na stronę (V12)

- page-hero + toc-index (poza polityką i `podstrony/index.html`);
- ≥ 7 różnych typów bloków, w tym ≥ 3 z home (np. H4, H5/H6, H7, H16, H9–H13) i ≥ 3 nowe;
- ≥ 2 kompozycje asymetryczne (N6, N7, N25, N26…);
- 3–7 placeholderów (polityka: 0);
- ≥ 4 palety; `sticky-cta`; `related-tiles` (strony usług); zamknięcie H16.

### 8.4 Pokrycie globalne (macierz)

`booking` (H13) na ≥ 4 stronach, na których umawia się online (np. czipowanie, szczepienia, paszporty, ciśnienie, interna, stomatologia); `quotes` (H10) ≥ 3 (hub, interna, zespół, szczepienia); `after-hours` (H12) ≥ 4 (urologia, interna, okulistyka, nefrologia, dermatologia, hub); `emergency-guide` (H11) ≥ 3 (chirurgia, kardiologia, okulistyka, czipowanie); `bento` (H8) na hubie; `people` (H9) ≥ 5 stron (doctor-strip); `social-promo` (H14) hub + zespół; `about` (H15) zespół; `equipment-grid` (H6) ≥ 3 strony. Strony telefoniczne (kardiologia, okulistyka, chirurgia, USG) zamiast `booking` mają `cta-band` z numerem telefonu.

---

## 9. Obrazy i placeholdery

### 9.1 Zasady
Placeholder to widoczna ramka (`figure.placeholder.photo-frame`, N24) z opisem tego, co ma w niej być. Autor wstawi obrazy później — masz zrobić to **tak, by wstawienie pliku nie wymagało edycji HTML**.

Rodzaje (`data-kind`) i proporcje (`--ph-ratio`): `foto` (czarno-białe zdjęcie; 3/2, 4/5, 16/9), `pas` (21/9), `wycinek` (PNG z alfa, np. zwierzę/przedmiot; 4/5, 1/1), `ilustracja` (liniowa, alfa, barwiona T1; 1/1, 3/2), `diagram` (schemat, np. anatomia; 4/3), `ikona` (1/1, mała).

Rozmieszczenie (3–7 na stronę): (1) mozaika/pas po sekcji wyjaśniającej „jak to wygląda” (21/9 lub mozaika), (2) aside `split-feature` (4/5 lub 1/1) przy najważniejszym rozdziale, (3) diagram tam, gdzie tekst opisuje budowę/miejsce (kardiologia — serce, okulistyka — oko, USG — mapa ciała, ciśnienie — mankiet, czipowanie — miejsce wszczepienia), (4) „kto przyjmuje” — istniejące portrety z home (nie placeholder), (5) jeden obraz „atmosfery” (pies/kot w gabinecie). Zdjęcia sprzętu i personelu: zalecane prawdziwe zdjęcia przychodni; zdjęcia zabiegów — nie generuj fotorealistycznych (preferuj liniową ilustrację).

### 9.2 Znacznik
```html
<figure class="placeholder photo-frame" data-ph="czipowanie-02-aplikator" data-kind="foto"
        data-src="assets/podstrony/czipowanie-02-aplikator.jpg" data-alt="…" style="--ph-ratio:3/2">
  <figcaption>Aplikator czipa<span>Zdjęcie 3∶2, czarno-białe · plik: assets/podstrony/czipowanie-02-aplikator.jpg</span></figcaption>
</figure>
```
Rozszerzenia kanoniczne: `foto` → `.jpg`, `wycinek`/`ilustracja` → `.png`, `diagram` → `.svg`, `ikona` → `.svg`. `podstrony.js` próbuje załadować `data-src` (z `ROOT`); jeśli plik istnieje, podmienia zawartość figury na `<img>` (alt z `data-alt`, `width/height` z pliku). Tryb `--bake` generatora zamienia istniejące pliki na stałe `<img>` i usuwa próby ładowania. Kolory placeholdera: wyłącznie z palety (tło `--accent`, kreskowanie `repeating-linear-gradient` z `color-mix(in srgb, var(--ink) 12%, transparent)`).

### 9.3 Manifest
`_obrazy.json` i czytelny `_obrazy.md`: dla każdego placeholdera `id`, strona, sekcja, rola, rodzaj, proporcje, plik docelowy, min. rozmiar (np. 1600 px dłuższy bok), `opis_pl`, `czego_unikać`, `alt_pl`, `podpis_pl`, `prompt_en`, obróbka (zdjęcie → czarno-białe w CSS; wycinek → alfa), źródło zalecane (prawdziwe zdjęcie / generowanie). Prompty EN w konwencji istniejących `assets/*-prompt.md`:

```
# <Polski tytuł>
Plik: <nazwa>. Narzędzie: wbudowane image_gen.

Use case: photorealistic-natural. Asset type: website photograph, <proporcja>. Subject: … Grayscale black-and-white photographic rendering, flat very light neutral grey seamless backdrop (#d4d4d4), soft diffused studio light, low-contrast editorial look. Subject within the middle 60 percent of the frame. No text, no graphics, no logos, no people's faces.
```
(Wycinki: „true transparent alpha background, no halo, no drop shadow”; ilustracje: „monoline black line art on transparent background, no fill, consistent with the clinic’s existing line illustrations”.) Przed utworzeniem promptu przeczytaj 2 pliki z `assets/*-prompt.md`.

### 9.4 Zasoby istniejące
Hero: ilustracje z §2.2 (T1). Portrety lekarek: tonalne PNG z H9. Kształty `shape-14/16/23/35.svg`, ikony `assets/min/icon-*.svg`, wycięty pies `booking-dog-cutout-v1.png`, kot `follow-cat-grey-v1.png`. Nie podmieniaj niczego z `assets/`; nie zakładaj, że jakikolwiek z haszowanych plików `assets/*.webp` jest odpowiedni — sprawdź wzrokowo, zanim go zaproponujesz w manifeście jako „istniejący”.

---

## 10. Szkielety stron (sekwencja bloków; palety w nawiasach = klasy sekcji)

Szkielet jest obowiązkowy co do **sygnatury** (podkreślone elementy) i rytmu; drobne decyzje należą do Ciebie. Każda strona: `page-hero (hero)` + `toc-index (clinic)` na początku, `contact (contact)` na końcu (H16 z listy „Jak umówić”), stopka. Kompozycje 4/7 = `split-feature`.

| Strona | Sygnatura i szkielet środka |
|---|---|
| **Hub** (D) | **`bento` z home (services)** → 4 × `split-feature` + `ruled-table.is-directory` (about, team, reviews, arrival·preparation) → `chooser` („Nie wiesz, którą…”) → „Jak wygląda wizyta” `step-list` + `figure-mosaic` (clinic) → `alert-band` + H12 (emergency) → FAQ H5 (faq) → H10 (reviews) → H14 → contact |
| **Zespół** (E) | tabela lekarek jako `ruled-table.is-directory` z miniaturami portretów (team) → `chooser` „Którą lekarkę wybrać” → **`rail-layout` z 7 profilami** (kotwice `Magda, Ola, Julia, Malgosia, Olga, Kasia, Kinga`; każdy profil: `article.person` w `.team .people`, `key-values` z wierszy „Obszary/Wykształcenie…”, akapit, CTA) → H15 (about) → `callout` „Praca w Psyjaciołach” → FAQ → H10 → H14 → contact |
| **Polityka** (F) | page-hero (mały) → **`rail-layout` + `legal-prose`** (szyna = spis treści) z tabelami `ruled-table`; bez placeholderów i ozdobników; zamknięcie: stopka (brak `contact`) |
| **Choroby wewnętrzne** (A) | `split-feature` + `ruled-table` objawów (about) → **`rail-layout` 7 układów** (services; „Zakaźne” z tabelą, „Hormonalne/Moczowe” z `ruled-list`) → `alert-band.is-inverted` „Kiedy nie czekać” + H12 (team) → `step-list` wizyty (clinic) → `split-feature` „Badania kontrolne” → FAQ `faq-accordion` → H10 → H13 |
| **Dermatologia** (A) | `ruled-list` objawów + `callout` „Kiedy nie czekać” + H12 → `ruled-table` problemów skórnych (3 kolumny) → diagnostyka `ruled-list` + `figure-band` → leczenie `split-feature` → przygotowanie H5 → `alert`/`callout` „Dlaczego nie leczyć na własną rękę” → FAQ accordion → H13 |
| **Stomatologia** (A) | `ruled-list` objawów + `alert-band` → układ „Najczęstsze problemy” jako H6 (4 karty) → „Czym grozi brak leczenia” `ruled-list.is-checklist` → **`step-list` zabiegu** + „Po zabiegu” `callout` → profilaktyka `ruled-list` + `figure-mosaic` → FAQ (6 → H5) → H13 → doctor-strip (Ola) |
| **Nefrologia** (A) | objawy `ruled-list` → **`duo` AKI vs PChN** → dwa rozdziały `split-feature` (AKI z `alert-band`, PChN) → diagnostyka `ruled-table` → leczenie/życie z PChN `ruled-list` → „Jak chronić nerki” `callout` → H12 → FAQ accordion → doctor-strip (Magda) |
| **Urologia** (A) | **`alert-band.is-inverted` „stan nagły” jako pierwszy po spisie treści** + H12 → objawy `ruled-list` → **`duo` przyczyn (psy/koty)** + H6 (trzy przyczyny) → diagnostyka `step-list` → leczenie `ruled-list` → nawroty `ruled-list.is-checklist` → FAQ accordion → `related-tiles` (nefrologia) |
| **Kardiologia** (A) | **`duo` „U psa / U kota”** → `ruled-table` chorób (3 kolumny) → H6/`equipment-grid` badań (ECHO/EKG/ciśnienie) → H11 „Jak wygląda konsultacja” → `ruled-list` „Kiedy warto zbadać” → leczenie + opcjonalnie `breath-counter` → `doctor-strip` (Małgorzata) → FAQ accordion → `cta-band` telefon |
| **Okulistyka** (A) | **`ruled-table.is-triage`** (po leadzie) + `callout` telefon + H12 → „Co robić do czasu wizyty” H11 (untitled) → 5 chorób jako `split-feature` z `diagram` oka (placeholder) → badanie `step-list` → dbanie `ruled-list.is-checklist` → doctor-strip (Kinga) → FAQ accordion → `cta-band` |
| **Chirurgia** (A) | `step-list` konsultacji → „Dlaczego przygotowanie…” `ruled-list` + `ruled-table` badań → H11 „Przygotowanie w dniu zabiegu” (etykiety) → H11 „Jak dbać po operacji” + `duo` „Jak pielęgnować ranę / Kiedy skontaktować się” → FAQ accordion (5) → doctor-strip (Kasia) → `cta-band` |
| **Szczepienia** (C) | `ruled-table` gatunków → **`phase-timeline`** → `callout` wścieklizna → H6 przygotowanie/przebieg/po → profilaktyka: `ruled-table` + `split-feature` → FAQ (6 → H5) → H10 → H13 |
| **Paszporty** (C) | **`fact-strip` z datą** „22 kwietnia 2026 r.” → `ruled-list` zawartości + `ruled-table` warunków → `step-list` wizyty → `callout` zmian w przepisach → `ruled-table` „Dokąd” + `ruled-list` → FAQ accordion → H13 → doctor-strip (Magda) |
| **Czipowanie** (C) | **`fact-strip`** („15-cyfrowy”, „ISO”, „Safe-Animal”, „od około 8. tygodnia życia”) → `split-feature` „Jak działa czip” + `diagram` czipa → `step-list` zabiegu + `figure-band` → `callout` „liczy się rejestracja” + `ruled-list.is-checklist` → „gdy zwierzę się zgubi” `step-list`/H11 untitled → `duo`/`ruled-table` obowiązek + `callout` KROPiK → FAQ accordion (4) → H13 |
| **Ciśnienie** (B) | **`range-scale`** → `ruled-list` „Kiedy warto” → przygotowanie + `step-list` pomiaru (z `diagram` mankietu) → efekt białego fartucha `callout` → `ruled-table` narządów + `alert-band` → leczenie `step-list` → FAQ accordion → H13 |
| **USG** (B) | `ruled-list` wskazań + `callout` stan nagły → `ruled-table` „Co zbadać” + `diagram` mapa ciała → `callout` USG a RTG → `ruled-table` przygotowania → `step-list` przebiegu → FAQ accordion → doctor-strip (Olga, Ola) → `cta-band` |
| **Laboratorium** (B) | początkowa tabela „Gdzie / Badania” jako `duo` (na miejscu / zewnętrzne) → 5 badań na miejscu jako H6 (2 rzędy) → `ruled-table` zewnętrznych + `ruled-table` parametrów → `ruled-table` objawów → przygotowanie `ruled-list` → FAQ (6 → H5) → H13 |

---

## 11. Pliki, generator, szkielet dokumentu

### 11.1 Drzewo wyjściowe
```
podstrony/
  index.html  podstrony.css  podstrony.js
  _bloki.html  _obrazy.json  _obrazy.md  _raport.md
  _narzedzia/  (build.py, strony.py, bloki.py, home.py, checks.py, paleta-test.js, klasy.py)
  uslugi-weterynaryjne/index.html
  uslugi-weterynaryjne/<slug>/index.html   (×14)
  zespol/index.html   polityka-prywatnosci/index.html
```
Obrazy użytkownika: `assets/podstrony/<id>.<ext>` (katalog tworzy użytkownik; generator go nie tworzy w `assets/` – R3; w manifeście napisz, że trzeba go utworzyć).

### 11.2 Generator
Python 3, bez zależności (stdlib `html.parser`; `bs4`/`lxml` dozwolone, jeśli są). Podział: `home.py` (wyciąganie fragmentów i słownika palet z home, `rewrite()` linków), `bloki.py` (funkcje renderujące bloki: wejście = węzły ze źródła, wyjście = HTML), `strony.py` (specyfikacje 17 stron: sekwencja sekcji, klasa-paleta jako rola, podziały tytułów, fakty, placeholdery), `build.py` (CLI: `--only <slug>`, `--check`, `--bake`, `--dry-run`). Tekst pochodzi wyłącznie ze źródła przez węzły; w `strony.py` nie ma ani jednego zdania treści poza etykietami UI z białej listy.

### 11.3 Szkielet dokumentu
```html
<!doctype html><html lang="pl"><head><!-- generated: psyjaciele-podstrony -->
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>…z komentarza title…</title><meta name="description" content="…">
<meta name="robots" content="noindex,follow"><link rel="canonical" href="DOMENA/…/">
<meta property="og:type" content="website"> … og:locale, og:site_name, og:title, og:description, og:url, twitter:*
<link rel="preload" as="font" …> ×3 (jak home, z ROOT)
<link rel="stylesheet" href="ROOTminimal.css?v=…"> … (ta sama kolejność co home) … <link rel="stylesheet" href="ROOTdesign-tokens.css">
<link rel="stylesheet" href="ROOTpodstrony/podstrony.css">
<script type="application/ld+json">{ "@graph": [ … ] }</script></head>
<body class="book-type subpage" data-root="ROOT" data-page="<slug>">
<a class="skip" href="#main">Przejdź do treści</a><div class="header-backdrop" aria-hidden="true"></div>
<header class="site-header" data-palette="…"> … </header>
<main id="main"> … sekcje … </main>
<footer data-palette="…"> … </footer>
[<svg …filtry z home… />]  <div class="sticky-cta">…</div>
<script src="ROOTpet-photos.js?v=…" defer></script> <script src="ROOTillustration-motion.js?v=…" defer></script>
<script src="ROOTanimacje.js?v=…" defer></script> <script src="ROOTpodstrony/podstrony.js" defer></script>
</body></html>
```
`ROOT` = prefiks z R5; adresy, wersje `?v=` i kolejność kopiuj z home.

---

## 12. Proces i weryfikacja

### 12.1 Etapy (po każdym zapisz stan)
1. **Rozpoznanie** — odczytaj home i arkusze, zweryfikuj fakty z §2/§4/§5.4 skryptem (palety, klasy, ścieżki, pliki z §2.2), uruchom baseline testu z Dodatku A na home i zapisz `_narzedzia/baseline.json`; uruchom Dodatek B.
2. **Fundament** — `podstrony.css` (podstawy + bloki rdzeniowe), `podstrony.js`, `_bloki.html` (każdy blok × ≥ 3 palety), sprawdź wizualnie.
3. **Generator + 3 strony pilotażowe** (czipowanie, kardiologia, polityka) — pełna weryfikacja V1–V14; poprawki systemowe w blokach, nie w pojedynczych stronach.
4. **Pozostałe strony** wg priorytetu: hub, zespół, urologia, interna, okulistyka, reszta.
5. **Bloki dodatkowe** (reszta macierzy §8.4), manifest obrazów, `index.html` przeglądu.
6. **Weryfikacja końcowa**, naprawa, raport.

### 12.2 Weryfikacje (V1–V14)
V1 diff tekstu: tekst każdej strony (po odjęciu UI z białej listy) = tekst źródła; dozwolone duplikaty wg R4.5; `fact-strip` ⊂ tekst. V2 skan literałów koloru w `podstrony.css/js` i w wygenerowanym HTML (w tym `style`, atrybuty SVG; wyjątek: skopiowany blok `<svg>` z home). V3 test inwersji palety (Dodatek A) — brak nowych wycieków. V4 nieznane klasy i kolizje (Dodatek B). V5 linki: każdy `href`/`src` istnieje, kotwice `#id` istnieją, brak adresów katalogów i ścieżek zaczynających się od `/`. V6 a11y: jeden h1, konspekt, kontrast AA w każdej palecie, fokus, `alt`. V7 zrzuty 1440/1024/768/390 px każdej strony + brak poziomego przewijania + brak nakładania. V8 wydajność: rozmiar HTML/CSS/JS, brak blokujących zapytań, brak CLS od obrazów. V9 JSON-LD: poprawny JSON; `FAQPage` identyczny z widocznymi pytaniami. V10 `prefers-reduced-motion`. V11 symulacja GitHub Pages: serwer na katalogu nadrzędnym względem `MAKIETA`, otwórz strony pod `/<folder>/podstrony/…`, zero 404 (poza placeholderami). V12 macierz pokrycia z §8.3–8.4 jako tabela w raporcie. V13 manifest obrazów kompletny (każdy `data-ph` ma wpis). V14 bez JS: treść czytelna, urgentne informacje widoczne.

---

## 13. Raport końcowy (`_raport.md` + podsumowanie w odpowiedzi)
Sekcje: (1) co dostarczono (pliki, liczby), (2) wyniki K1–K9 i V1–V14 (zaliczone / niesprawdzone + powód), (3) macierz pokrycia stron × bloków i palet, (4) decyzje projektowe i odstępstwa od promptu z uzasadnieniem, (5) różnice między opisem w prompcie a stanem plików, (6) uwagi do treści (błędy, niespójności, brak `h1` na home, rozbieżne dane), (7) lista placeholderów (liczba, link do manifestu), (8) jak zmienić paletę/treść i przegenerować, (9) znane ograniczenia i propozycje zmian w plikach home (nie wykonane, R3).

---

## 10A. Szkielety — uzupełnienie: algorytm palet, placeholdery per strona, przykład kompletny

### 10A.1 Algorytm doboru palet (jedno miejsce w generatorze)
Słownik **ról** → klasy sekcji (budowany programowo z `minimal.css`, nie wpisany ręcznie; poniżej stan z 8.10.2026):

| Rola w generatorze | Klasy sekcji | Powierzchnia |
|---|---|---|
| `top` | `hero` | zielona |
| `toc` | `clinic` | papier |
| `soft-a` | `about` | jasna brzoskwinia |
| `soft-b` | `arrival` | jasna brzoskwinia |
| `mid-a` | `services` | szałwia |
| `mid-b` | `reviews` | jasna szałwia |
| `mid-c` | `team` | brzoskwinia |
| `paper` | `arrival preparation` (+ `faq`) | papier |
| `alarm` | `emergency` | zielona |
| `booking` | `booking` | zielona |
| `end` | `contact` | niebieska |

Algorytm: (1) kolejne sekcje bloków dostają role z listy kolejności `[soft-a, mid-a, mid-c, mid-b, paper, soft-b]` (cyklicznie), (2) jeśli powierzchnia roli = powierzchnia sąsiada (poprzedniej **lub** następnej sekcji, w tym `toc` = papier i `contact`), przeskocz do następnej roli, (3) sekcje wymagające z natury konkretnej palety (patrz niżej) wymuszają rolę i resztę przesuwają, (4) `alarm` i `booking` ≤ 2 razy łącznie (nie obok siebie), (5) FAQ → zawsze `paper` (klasa `faq`), po nim nie może stać `toc`/`paper`. Powierzchnie liczy się **z CSS home** (rozwiąż `--surface` klasy), nie z tabeli.

Wymuszone role: `H12 after-hours` → w sekcji `team` albo `emergency` (jak na home, wg treści); `H11 emergency-guide` → `emergency`; `H13 booking` → `booking`; `doctor-strip` → `team`; `H10 quotes` → `reviews`; `H14 social-promo` → `social-promo-section#obserwuj-nas`; `H15 about` → `about`; `bento/H8` → `services`; `H6/equipment-grid` → `clinic` (jak na home) lub `services`.

### 10A.2 Placeholdery — minimalny zestaw per strona (id = `<skrót>-NN-<rola>`)

Rozmieszczenie jest zadaniem, nie sugestią: umieść **co najmniej** poniższe; możesz dodać do 7. `ph` = `photo-frame`; „aside” = w `split-aside`.

| Strona (skrót) | Placeholdery (rodzaj · proporcje · miejsce) |
|---|---|
| hub `uslugi` | `uslugi-01-recepcja` foto 3/2 aside „o nas”; `uslugi-02-gabinet` pas 21/9 pod bento; `uslugi-03-mozaika-a/b/c` foto 4/5 + 2×3/2 (mozaika „Jak wygląda wizyta”); `uslugi-04-kot-pies` wycinek 1/1 przy FAQ |
| `zespol` | `zespol-01-zespol-grupowe` pas 21/9 po tabeli lekarek; `zespol-02-gabinet` foto 3/2 aside rail; `zespol-03-atmosfera` foto 4/5 przy „Praca w Psyjaciołach” (portrety lekarek: z home, **nie** placeholdery) |
| `interna` | `interna-01-badanie` foto 4/5 aside objawów; `interna-02-schemat-ukladow` diagram 4/3 w szynie; `interna-03-pas-gabinet` pas 21/9 po krokach wizyty; `interna-04-kontrola` foto 3/2 |
| `lab` | `lab-01-analizator` foto 3/2 aside; `lab-02-probki` wycinek 1/1; `lab-03-pas-laboratorium` pas 21/9 nad tabelą zewnętrznych |
| `szczepienia` | `szcz-01-szczepienie` foto 4/5 aside; `szcz-02-ksiazeczka` wycinek 1/1 przy przebiegu; `szcz-03-kalendarz` diagram 4/3 nad osią; `szcz-04-pas-pies-kot` pas 21/9 |
| `chirurgia` | `chir-01-sala-zabiegowa` pas 21/9; `chir-02-konsultacja` foto 3/2 aside; `chir-03-opieka-po` foto 4/5; `chir-04-rana-schemat` diagram 4/3 (obok `duo`) |
| `kardiologia` | `kard-01-serce-diagram` diagram 4/3 (budowa serca, aside); `kard-02-echo` foto 3/2; `kard-03-ekg` wycinek 1/1; `kard-04-pies-kot` mozaika 7+5 (3 foto); `kard-05-pas` pas 21/9 |
| `obrazowa` | `usg-01-aparat` foto 4/5 aside; `usg-02-mapa-ciala` diagram 4/3; `usg-03-badanie` foto 3/2; `usg-04-pas` pas 21/9 |
| `okulistyka` | `oko-01-oko-diagram` diagram 4/3 (budowa oka); `oko-02-badanie-lampa` foto 3/2; `oko-03-oko-pies` foto 4/5; `oko-04-pas-gabinet` pas 21/9 |
| `dermatologia` | `derm-01-badanie-skory` foto 4/5 aside; `derm-02-pas-skora-siersc` pas 21/9; `derm-03-cytologia` foto 3/2; `derm-04-pielegnacja` wycinek 1/1 |
| `stomatologia` | `stom-01-jama-ustna-diagram` diagram 4/3; `stom-02-zabieg` foto 3/2; `stom-03-mozaika` 3 foto (7+5); `stom-04-pies-szczotka` wycinek 1/1 |
| `nefrologia` | `nefr-01-nerki-diagram` diagram 4/3 (aside); `nefr-02-kot-pije` foto 4/5; `nefr-03-pas` pas 21/9; `nefr-04-badanie-krwi` foto 3/2 |
| `urologia` | `uro-01-uklad-moczowy-diagram` diagram 4/3; `uro-02-kot-kuweta` foto 3/2; `uro-03-pas` pas 21/9; `uro-04-pies-spacer` wycinek 1/1 |
| `cisnienie` | `cis-01-mankiet-diagram` diagram 4/3 (przy `step-list` pomiaru); `cis-02-pomiar-kot` foto 4/5 aside; `cis-03-pas-gabinet` pas 21/9; `cis-04-pomiar-pies` foto 3/2 |
| `paszporty` | `pasz-01-paszport` wycinek 1/1 (aside); `pasz-02-stempel` foto 3/2; `pasz-03-podroz` pas 21/9; `pasz-04-pies-kot-walizka` foto 4/5 |
| `czipowanie` | `czip-01-czip-diagram` diagram 4/3 (aside „Jak działa czip”); `czip-02-aplikator` foto 3/2; `czip-03-pas-zabieg` pas 21/9; `czip-04-skaner` foto 4/5; `czip-05-pies-kot` wycinek 1/1 |
| `polityka` | brak |

Dla każdego: `data-kind`, `--ph-ratio`, `data-src` zgodne z §9.2; w `_obrazy.md` wpis z promptem EN. Wycinki i ilustracje przewidziane do barwienia T1 → `data-kind="ilustracja"`.

### 10A.3 Przykład kompletny: `czipowanie-psow-i-kotow` (wzór dla pozostałych stron)

| # | Sekcja (klasa/paleta) | Zawartość | Placeholdery |
|---|---|---|---|
| 1 | `hero page-hero` (zielona) | breadcrumb „Strona główna / Usługi / Czipowanie zwierząt”; kicker „Czipowanie”; h1 mieszany; wstęp; `p.cta-wizyta`; przyciski; `poster-art` = `service-microchip.png` (T1); `fact-strip`: „15-cyfrowy” / „ISO” / „Safe-Animal” / „od około 8. tygodnia życia” (dt: „Numer”, „Standard”, „Rejestr”, „Od kiedy”) | — |
| 2 | `clinic` (papier) | `toc-index` z nagłówków źródła | — |
| 3 | `about` (jasna brzoskwinia) | `split-feature`: aside = `section-head` + diagram; body = „Jak działa czip” (`book-prose`) + `callout` „liczy się rejestracja” | `czip-01-czip-diagram` |
| 4 | `services` (szałwia) | `split-feature.is-reversed`: body = `step-list` zabiegu (3–4 kroki, `--steps`), aside = foto; pod spodem `figure-band` | `czip-02-aplikator`, `czip-03-pas-zabieg` |
| 5 | `arrival` (jasna brzoskwinia) | `split-feature`: „co przynieść” `ruled-list.is-checklist` + aside skaner | `czip-04-skaner` |
| 6 | `emergency` (zielona) | „Gdy zwierzę się zgubi” — H11 `is-untitled` (kroki 1–3) + zdanie o kontakcie z kliniką | — |
| 7 | `reviews` (jasna szałwia) | obowiązek i rejestracja: `ruled-table` (Kto / Co / Gdzie) + `callout` KROPiK | `czip-05-pies-kot` |
| 8 | `arrival preparation faq` (papier) | `faq-accordion` (4 pytania; <6 → akordeon, nie H5) | — |
| 9 | `booking` (zielona) | H13 z kopii home (nagłówek UI „Umów wizytę”) | — |
| 10 | `contact` (niebieska) | H16 z „Jak umówić” (dane z NAP) | — |
| 11 | `footer` (zielona) | stopka z home | — |

Sąsiedztwo powierzchni: zielona → papier → jasna brzoskwinia → szałwia → jasna brzoskwinia → zielona → jasna szałwia → papier → zielona → niebieska → zielona. Zielona występuje mid-page 2 razy (6, 9), nie obok siebie. `sticky-cta` na ≤ 700 px; `related-tiles` (Szczepienia, Paszporty) dodaj **w sekcji 8** pod akordeonem lub jako sekcję `mid-c` przed `booking`, jeśli sąsiedztwo palet na to pozwala.

Typy bloków na tej stronie: page-hero, fact-strip, breadcrumb, toc-index, split-feature (×3), callout (×2), step-list, figure-band, ruled-list.is-checklist, H11, ruled-table, faq-accordion, related-tiles, H13, H16, photo-frame (×5), sticky-cta — czyli ≥ 7 typów, ≥ 3 z home (H11, H13, H16), ≥ 3 nowe.

---

## 8A. Reguły decyzyjne (deterministyczne — generator ma je zaimplementować, nie zgadywać)

**D1. Rozbiór pliku treści.** Parsuj `czyste/<slug>.html` (np. `html.parser`/BeautifulSoup lub własny tokenizer). Pomiń elementy techniczne (`head`, `script`, `style`, komentarze). Zbuduj drzewo: `title`, `h1`, wstęp (akapity przed pierwszym `h2`, w tym `p.cta-wizyta`), sekcje `h2` → podsekcje `h3` → bloki (`p`, `ul/ol`, `table`, `blockquote`, `details`…). Zachowaj inline (`strong`, `em`, `a`, `br`) bez zmian. Zapisz wszystko do pośredniego JSON (`_ast/<slug>.json`) — to ułatwia debugowanie i testy V1.

**D2. Etykieta *run-in*.** Akapit `p` zaczynający się od `<strong>Tekst:</strong>` lub `<strong>Tekst.</strong>` (≤ 6 słów) → etykieta; seria ≥ 3 takich akapitów pod rząd → `key-values` (gdy etykiety są krótkimi kategoriami: Obszary, Wykształcenie…) albo `step-list` (gdy tekst sąsiaduje z listą kroków/„Krok n”, „Etap n”, „Najpierw/Potem”) albo `H6` (gdy to 3–4 równoległe czynniki/karty). Pojedynczy run-in w środku prozy → zostaje w akapicie (nic nie zmieniaj).

**D3. Lista.** `ol` zawsze → `step-list`, jeśli elementy opisują czynności w kolejności (czasowniki w trybie rozkazującym/bezokolicznik/„Najpierw…”), inaczej `ruled-list.is-numbered`. `ul` ≤ 3 pozycji → zostaje listą w prozie (`ruled-list` bez `is-columns`); `ul` 4–7 → `ruled-list`; `ul` ≥ 8 krótkich pozycji → `is-columns`; `ul` z frazą „zabierz/przygotuj/przynieś” w nagłówku → `is-checklist`.

**D4. Tabela.** (a) 2 kolumny, nagłówek zawiera „Objaw” i „Kiedy/Jak szybko/Pilność” → `ruled-table.is-triage`; (b) nagłówki nazywają dwie strony (psy/koty, AKI/PChN) → `duo`; (c) „Etap | Kiedy | …” z ≤ 5 wierszami → `phase-timeline`; (d) 4 wiersze ciśnienia (zakres/ocena/ryzyko) → `range-scale` **plus** tabela w `details`; (e) pozostałe → `ruled-table`. W razie wątpliwości zawsze `ruled-table` (bezpieczny wariant).

**D5. FAQ.** Sekcja o nagłówku zawierającym „Pytania” / „FAQ” / „Najczęstsze pytania” i `h3` jako pytaniami: `n % 3 == 0` **i** każda odpowiedź ≤ 380 znaków → H5 (kolumny z home, `ruled-columns`); w przeciwnym razie `faq-accordion`. Jeśli odpowiedzi zawierają listy/tabele, zawsze akordeon.

**D6. Emergency-guide.** Sekcja „Co robić…/Pierwsza pomoc/Do czasu wizyty/Gdy zwierzę się zgubi” z listą 3 kroków → H11. Jeśli sekcja nie ma własnego tytułu poza nagłówkiem `h2` (czyli h2 stoi tuż nad krokami), użyj wariantu `is-untitled` (jak na home: bez dodatkowego `h3` nad krokami; tytuł `h2` zostaje w `poster-heading`). Przy ≠ 3 krokach użyj `step-list` (H11 jest zaprojektowany pod 3 kolumny).

**D7. Pilne.** Sekcje o nagłówkach z „Kiedy nie czekać”, „Stan nagły”, „Pilne”, „natychmiast” → `alert-band` (+ H12 pod spodem, jeśli treść wspomina o klinikach całodobowych/po godzinach). Pierwsze zdanie pozostaje pierwszym zdaniem; telefon i przycisk to UI dodany do sekcji (z NAP).

**D8. Ostrzeżenia i uwagi.** `blockquote`, akapit zaczynający się od „Ważne/Uwaga/Pamiętaj/Zapamiętaj” lub oznaczony w źródle jako uwaga → `callout`. Nie twórz calloutów z własnych podsumowań.

**D9. Wybór `split-feature` vs. pełna szerokość.** Rozdział z `h2` + ≥ 2 akapity prozy lub proza + lista → `split-feature` (aside: nagłówek; body: treść), naprzemiennie `is-reversed`. Rozdział z samą tabelą/akordeonem/mozaiką → pełna szerokość w `.wrap` z `section-head` powyżej. Maks. 2 rozdziały pod rząd w tej samej orientacji.

**D10. Podział długich rozdziałów.** Rozdział > 700 słów → rozbij na dwie sekcje o różnych paletach na granicy `h3` (bez zmiany treści), chyba że `rail-layout`.

**D11. Wstęp i CTA.** Akapit(y) przed pierwszym `h2` → `poster-copy` page-hero. `p.cta-wizyta` w źródle występuje 1–3 razy: pierwszy trafia do hero, kolejne → `cta-band`, ostatni → sekcja `contact`/`booking` (nie duplikuj dosłownego tekstu w więcej niż 2 miejscach: pozostałe wystąpienia zostają w treści jako zwykłe akapity).

**D12. Linki.** Każdy `href` z treści przechodzi przez `rewrite()` wg R5; brak mapowania → zostaw jak w źródle i wpisz do `_raport-linkow.md`. Zewnętrzne linki: `rel="noopener"` + `↗`.

### Tabela decyzyjna pułapek treści medycznych (R8) — co wolno wizualizować
Wolno: układ, hierarchia, ikonografia neutralna, kolejność kroków **ze źródła**. Nie wolno: kolory „zdrowe/chore”, ikony „OK/ostrzeżenie” przy wynikach, progów nieobecnych w źródle, liczników zmieniających sens (poza `breath-counter` bez oceny), skracania zastrzeżeń („nie zastępuje konsultacji…”) — zastrzeżenie musi stać **obok** zwizualizowanej tabeli (`range-scale`, `is-triage`).

---

## 9A. Playbook placeholderów i obrazów — uzupełnienie

**Kolejność kroków generatora:** (1) przejdź plan strony (§10, §10A.2), (2) dla każdego slotu utwórz rekord `{id, strona, sekcja, rola, rodzaj, ratio, wariant}` i `figure` N24, (3) po zbudowaniu wszystkich stron wygeneruj `_obrazy.json` (źródło prawdy) i z niego `_obrazy.md` (czytelna lista) oraz `OBRAZY-PROMPTY.md` (same prompty EN do kopiowania), (4) policz placeholdery per strona (V12/V13: 3–7), (5) sprawdź unikalność `data-ph` w całej makiecie.

**Pola rekordu manifestu:** `id`, `strona` (slug), `sekcja` (id sekcji), `rola` (np. „aside rozdziału 02”), `rodzaj` (`foto|pas|wycinek|ilustracja|diagram|ikona`), `proporcje`, `plik` (ścieżka docelowa), `min_px` (dłuższy bok: foto 1600, pas 2400, wycinek 1200, diagram 1600 jako SVG/PNG), `opis_pl` (co ma być na obrazie — konkretnie, 1–2 zdania), `czego_unikac_pl` (np. twarze obcych osób, napisy, logotypy, krew, dyskomfort zwierzęcia), `alt_pl` (opis dla czytnika; pusty `alt=""` dla czysto dekoracyjnych), `podpis_pl` (opcjonalnie; nie wymyślaj faktów), `prompt_en`, `obrobka` (`bw-css` | `alpha-ink-T1` | `svg-mask`), `zrodlo` (`prawdziwe zdjęcie` zalecane dla wnętrz/zespołu/sprzętu; `generowanie` dla zwierząt/schematów), `status` (`placeholder` | `gotowe`).

**Zasady treści obrazów (etyka i wiarygodność):** obrazy medyczne (USG, EKG, zmiany skórne, zęby) — preferuj prawdziwe zdjęcia z kliniki za zgodą opiekunów; generowane obrazy nie mogą udawać konkretnych wyników badań. Schematy anatomiczne — prosty monoline, bez zbędnej drastyczności. Zwierzęta spokojne, w komfortowej pozie, bez widocznego bólu, z poszanowaniem dobrostanu.

**Przykłady promptów EN (wzorzec do powielania; zachowaj format z `assets/*-prompt.md`):**

```
# Aplikator czipa przy barku psa
Plik: czip-02-aplikator.jpg. Narzędzie: wbudowane image_gen.

Use case: photorealistic-natural. Asset type: website photograph, 3:2 landscape. Subject: gloved hands of a veterinarian holding a microchip applicator near the scruff of a calm golden retriever, no needle visible. Grayscale black-and-white photographic rendering, flat very light neutral grey seamless backdrop (#d4d4d4), soft diffused studio light, low-contrast editorial look. Subject within the middle 60 percent of the frame. No text, no graphics, no logos, no people's faces.
```
```
# Schemat budowy serca (kardiologia)
Plik: kard-01-serce-diagram.svg. Narzędzie: wbudowane image_gen.

Use case: scientific-educational illustration. Asset type: website diagram, 4:3. Subject: simplified four-chamber heart of a dog in cross-section with unlabeled arrows showing blood flow. Monoline black line art on transparent background, no fill, even stroke width, consistent with the clinic's existing line illustrations. No text, no numbers, no gradients, no shading.
```
```
# Kot i pies w poczekalni (wycinek)
Plik: czip-05-pies-kot.png. Narzędzie: wbudowane image_gen.

Use case: stylized-concept. Asset type: website cutout, 1:1. Subject: a calm grey cat and a small dog sitting side by side, seen from the front. True transparent alpha background, no halo, no drop shadow. Grayscale black-and-white photographic rendering, soft diffused studio light. Subject within the middle 70 percent of the frame. No text, no logos.
```
Zasady: pliki obrazów zapisuj w `assets/podstrony/<slug>/` (użytkownik sam je dodaje; generator tylko podaje ścieżki); `OBRAZY.md` zawiera krótką procedurę: (1) wgraj plik pod wskazaną nazwą, (2) odśwież stronę — `podstrony.js` podmieni placeholder, (3) opcjonalnie uruchom `python3 generuj-podstrony.py --bake` (stałe `<img>`).

**Zachowanie `podstrony.js` dla placeholderów (moduł `initPlaceholders`):** dla każdego `figure.placeholder[data-src]` wykonaj `fetch(url, {method:"HEAD"})` (lub `new Image()` z `onload/onerror`, jeśli serwer nie obsługuje HEAD); przy sukcesie utwórz `<img>` z `alt=data-alt`, `loading="lazy"`, `decoding="async"`, `width/height` z `naturalWidth/Height`, dodaj klasę `has-image`; przy niepowodzeniu nic nie rób (cichy). Nie loguj błędów w konsoli (K1: zero błędów w konsoli — dla 404 użyj `new Image()`, który nie loguje do konsoli zasobów jako błędu skryptu; w razie hałasu w sieci wyłącz próby w trybie `--bake`).

---

## 11A. Architektura generatora i `podstrony.js` — uzupełnienie

### 11A.1 Moduły i kontrakty
- `home.py` — `load_home()` zwraca obiekt z: `head_links` (kolejność `<link>` i `<script>` z home), `header_html`, `footer_html`, `after_hours_html`, `booking_html`, `social_promo_html`, `bento_tiles` (lista: slug, tytuł, opis, ilustracja), `quotes` (6), `people` (karty `article.person` per imię), `nap` (adres, telefon, godziny, e-mail), `jsonld_vet` (VeterinaryCare), `palette_roles` (rola → klasa → powierzchnia, liczone z CSS), `svg_filters_block` (blok `<svg>` filtrów z końca `<body>`). `rewrite(html, depth)` przepisuje `href`/`src`/`srcset`/`poster`/`data-src` i adresy w `style` na ścieżki względne dla danej głębokości (`depth` = liczba katalogów w ścieżce wyjściowej); tablica mapowań R5 jest tam jedyną prawdą.
- `bloki.py` — czyste funkcje `render_<blok>(dane, ctx) -> str` (bez I/O); `ctx` niesie `depth`, licznik `ink_filter_id`, rejestr placeholderów. Każda funkcja zwraca HTML zgodny z §6/§7/§7A; dodaj `assert` na brakujące dane (nigdy cichy fallback, który gubi treść).
- `strony.py` — dla każdego sluga: `PAGE = {slug, out, archetype, crumb, hero_art, fact_strip:[(dt,dd)], sections:[{role, blocks:[…]}], placeholders:[…], related:[slugi]}`; sekcje wynikają z reguł D1–D12 (§8A) + wymuszeń z §10/§10A; ręczne nadpisania w jednym słowniku `OVERRIDES[slug]` (z komentarzem, dlaczego).
- `build.py` — CLI: `python3 build.py [--only slug] [--bake] [--out podstrony] [--check]`; kroki: load_home → parse treści → plan → render → zapis (z markerem `<!-- generated: psyjaciele-podstrony -->`; odmowa nadpisania pliku bez markera) → manifest → `_bloki.html` → `index.html` przeglądu → `_raport.md` (część automatyczna).
- `checks.py` — implementacje V1, V2, V4, V5, V6 (statyczne): zwraca kody wyjścia ≠ 0 przy błędzie.
- `klasy.py` (Dodatek B), `paleta-test.js` (Dodatek A), `baseline.json`.

### 11A.2 `podstrony.js` — lista funkcji (IIFE, `"use strict"`, każdy moduł w `try/catch`, bez zależności)
1. `initRoot()` — wylicza `ROOT_URL = new URL(document.body.dataset.root, location.href)`; udostępnia `abs(path)`.
2. `fixCustomPropertyUrls()` — dla elementów z `style` zawierającym `url(assets/…)` w zmiennych `--art|--icon|--blob|--pet-atlas` przepisuje na adresy bezwzględne (pułapka 4); wywołaj **przed** `animacje.js` (skrypt ładowany później, `defer` w kolejności dokumentu).
3. `initMenu()` — przełącznik `.menu-toggle` ↔ `nav#menu` (`aria-expanded`, `Esc` zamyka, klik w link zamyka), kopiuj semantykę z `minimal.js` (zapisaną w `minimal.pretty.js` lub własnym sformatowaniu — nie zmieniaj oryginału).
4. `initHeaderState()` — klasy `is-compact`, `is-scrolling-down`, `.header-backdrop.is-active`, zmienna `--nav-ink` zgodnie z sekcją pod nagłówkiem (odczytaj, jak robi to `minimal.js`); `requestAnimationFrame` + `passive` listener.
5. `initBlobAngle()` — `--blob-angle` (obrót kształtów) tak jak na home; wyłączone w `prefers-reduced-motion`.
6. `initFooterRing()` — obrót pierścienia w stopce (jak home).
7. `initBookingPets()` *(opcjonalnie)* — jeśli jest `.booking-composition`, uruchom animację psa/kota z home; w przeciwnym razie nic.
8. `initRail()` — N7 (`IntersectionObserver`).
9. `initFaqHash()` — otwiera `details` dla `location.hash` oraz po `hashchange`.
10. `initPlaceholders()` — §9A.
11. `initStickyCta()` — pokazuje `.sticky-cta` po minięciu `.page-hero`, ukrywa w `section.contact`/`footer` (IntersectionObserver); ustawia `--sticky-cta-h` na `body` (padding-bottom).
12. `initBreathCounter()` — opcjonalnie.
13. `initTocActive()` *(opcjonalnie)* — zaznacza w `toc-index` rozdział w oknie (jak N7).
Moduły nie dotykają stylów inline poza zmiennymi własnymi; żadnych `alert/confirm`.

### 11A.3 Szkielet `podstrony.css` (kolejność sekcji pliku)
`/* 0. Tokens-free helpers (.visually-hidden, .skip) */` → `/* 1. Subpage base (body.subpage …) */` → `/* 2. Page-hero, breadcrumb, fact-strip */` → `/* 3. Layouts: split-feature, rail-layout, figure-* */` → `/* 4. Content blocks: ruled-list/table, step-list, phase-timeline, duo, range-scale, key-values, legal-prose, chooser, related-tiles */` → `/* 5. Signals: alert-band, callout, cta-band, sticky-cta, breath-counter */` → `/* 6. FAQ accordion */` → `/* 7. Placeholders */` → `/* 8. Print */` (ukryj `.sticky-cta`, nagłówek; `details` otwarte). Każdy blok opatrz komentarzem `/* Nxx name — tylko zmienne sekcji */` (R10).

---

## 12A. Procedury weryfikacji (jak wykonać V1–V14)

| V | Procedura | Kryterium zaliczenia |
|---|---|---|
| V1 | Wyciągnij tekst widoczny z wygenerowanej strony i ze źródła; usuń UI z białej listy R4; znormalizuj białe znaki, `&nbsp;`, cudzysłowy; porównaj sekwencje zdań (`difflib`) — raport per strona. Osobno sprawdź, że każdy `dd` w `fact-strip` jest podciągiem tekstu strony. | 0 zdań brakujących/zmienionych; duplikaty tylko wg R4.5. |
| V2 | `grep -E '#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|\b(red|blue|green|black|white|grey|gray|orange|yellow|pink|purple)\b'` w `podstrony.css`, `podstrony.js`, w HTML po usunięciu skopiowanego `<svg>`. | 0 trafień (poza komentarzami; usuń je). |
| V3 | Dodatek A w przeglądarce na: home (baseline), `_bloki.html`, 3 stronach pilotażowych, potem wszystkich. | Brak wycieków ponad baseline. |
| V4 | Dodatek B. | 0 nieznanych klas/kolizji. |
| V5 | Parser linków: każdy lokalny `href`/`src` istnieje na dysku (wyjątek: pliki placeholderów); `curl -I` kilku losowych URL-i z serwera podglądu → 200. | 0 martwych linków. |
| V6 | Statycznie: HTML poprawny (`html5lib`/`tidy` jeśli jest), unikalne `id`, `aria-labelledby`/`href="#"` wskazują istniejące `id`, jeden `h1`, hierarchia `h2→h3` bez przeskoków, każdy `img` ma `alt`. | 0 błędów. |
| V7 | Playwright (Chromium z `/opt/pw-browsers` lub lokalny): zrzuty 1440/1024/768/390 px dla 17 stron; `document.documentElement.scrollWidth <= innerWidth`; brak nakładania (`getBoundingClientRect` sprawdzenie kolizji między `.split-aside` a `.split-body`); obejrzyj zrzuty. Gdy Playwright niedostępny → wykonaj tylko statyczne kontrole i zaznacz. | Brak przewijania poziomego, układ czytelny. |
| V8 | Konsola: zero `error`/`warning` na 17 stronach (poza 404 placeholderów, o ile występują). | 0. |
| V9 | Klawiatura: Tab przez nagłówek, menu, akordeon (`Enter/Space`), `rail-nav`; widoczny fokus; skip-link działa. | Zaliczone. |
| V10 | `prefers-reduced-motion: reduce` (emulacja): brak animacji wejścia nowych bloków, `animacje.js` respektuje ustawienie. | Zaliczone. |
| V11 | Symulacja podkatalogu: skopiuj/zlinkuj `MAKIETA` jako `/tmp/sym/psyjaciele-makieta` i uruchom serwer w `/tmp/sym`; otwórz wszystkie strony pod `/psyjaciele-makieta/…`; sprawdź, czy wszystkie zasoby = 200 (`read_network_requests`/Playwright `response`). | 0 błędów 404/ścieżek. |
| V12 | Skrypt zliczający na stronę: typy bloków (po klasach), liczba z home / nowych, asymetrie (`split-feature|rail-layout|figure-mosaic|figure-band`), palety (`section` klasy), placeholdery. | Spełnia §8.3. |
| V13 | Manifest ↔ HTML: każdy `data-ph` ma wpis, każdy wpis ma figurę; pola obowiązkowe niepuste; prompt EN zawiera „No text”. | 1:1. |
| V14 | JSON-LD: parsuje się, `@id` spójne, `BreadcrumbList` zgodny z okruszkami, `FAQPage` tylko gdy widoczne Q&A, `VeterinaryCare` skopiowany z home, brak `Review`/`AggregateRating` wymyślonych. | Poprawne. |

Dodatkowo (zalecane): `Lighthouse` a11y/SEO jeśli dostępny; kontrast `--small-ink` na `--surface` ≥ 4,5:1 dla każdej palety użytej na podstronach (liczony z CSS, nie z oka) — wynik dopisz do raportu.

### Błędy, których nie wolno popełnić (lista kontrolna przed zamknięciem etapu)
(1) Zmieniony plik poza `podstrony/`; (2) literał koloru w nowym kodzie; (3) nowa klasa o nazwie z home, ale z innym znaczeniem; (4) link bez `index.html`; (5) `<base>` lub ścieżka od `/`; (6) `minimal.js` załadowany na podstronie; (7) tekst dopisany spoza białej listy; (8) ocena/próg medyczny spoza źródła; (9) `h1` ≠ 1 na stronie; (10) placeholder bez wpisu w manifeście; (11) `overflow:hidden/auto` na przodku sticky; (12) animacja wejścia nowego bloku bez `no-preference`.

---

## Dodatek A. Test inwersji palety (V3)

Idea: obróć barwę wszystkich tokenów `--wp--preset--color--*` i porównaj kolory obliczone przed i po. Element, którego kolor się **nie zmienił**, ma literał (wyciek). Uruchom na home (zapisz bazę), potem na każdej podstronie; „nowy wyciek” = rodzaj (`właściwość|kolor|sygnatura`) nieobecny w bazie.

```js
// Uruchom w kontekście strony (konsola DevTools / page.evaluate). Zwraca listę rodzajów wycieków.
async function paletteTest(deg = 137) {
  const snap = () => {
    const out = new Map();
    const sig = (el) => { let e = el; while (e && !(e.classList && e.classList.length)) e = e.parentElement;
      return (e ? e.tagName.toLowerCase() + '.' + [...e.classList].filter(c => !/^(is-|rule-|will-)/.test(c)).join('.') : '?'); };
    const rgba = (c) => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : null; };
    let n = 0;
    for (const el of document.querySelectorAll('body *')) {
      n++;
      if (el.closest('defs,filter,script,style')) continue;
      const cs = getComputedStyle(el), props = [['color', cs.color], ['background-color', cs.backgroundColor]];
      for (const s of ['Top', 'Right', 'Bottom', 'Left'])
        if (parseFloat(cs['border' + s + 'Width']) > 0 && cs['border' + s + 'Style'] !== 'none') props.push(['border-' + s, cs['border' + s + 'Color']]);
      if (parseFloat(cs.outlineWidth) > 0 && cs.outlineStyle !== 'none') props.push(['outline', cs.outlineColor]);
      if (cs.textDecorationLine !== 'none') props.push(['text-decoration', cs.textDecorationColor]);
      if (parseFloat(cs.columnRuleWidth) > 0 && cs.columnRuleStyle !== 'none') props.push(['column-rule', cs.columnRuleColor]);
      if (el instanceof SVGElement && el.tagName.toLowerCase() !== 'svg') {
        if (cs.fill !== 'none') props.push(['fill', cs.fill]);
        if (cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0) props.push(['stroke', cs.stroke]);
      }
      props.forEach(([p, v], i) => { const a = rgba(v); if (!a || a.length > 3 && a[a.length - 1] === 0 && /^rgba/.test(v)) return;
        out.set(sig(el) + '|' + p + '|' + n, v); });
    }
    return out;
  };
  const hex2hsl = (h) => { const n = parseInt(h.slice(1), 16), r = (n >> 16) / 255, g = (n >> 8 & 255) / 255, b = (n & 255) / 255;
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
    let hh = 0, s = 0; if (d) { s = d / (1 - Math.abs(2 * l - 1)); hh = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; hh *= 60; }
    return [(hh + 360) % 360, s, l]; };
  const hsl2hex = ([h, s, l]) => { const c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = l - c / 2;
    const [r, g, b] = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
    return '#' + [r, g, b].map(v => Math.round((v + m) * 255).toString(16).padStart(2, '0')).join(''); };
  const tokens = {};
  for (const sh of document.styleSheets) { let rules; try { rules = sh.cssRules; } catch { continue; }
    const walk = (list) => { for (const r of list) { if (r.selectorText === ':root')
        for (const p of r.style) if (p.startsWith('--wp--preset--color--')) { const v = r.style.getPropertyValue(p).trim(); if (/^#[0-9a-f]{6}$/i.test(v)) tokens[p] = v; }
      if (r.cssRules) walk(r.cssRules); } }; walk(rules); }
  const style = document.createElement('style'); style.id = 'paleta-test';
  const before = snap();
  style.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}:root{' +
    Object.entries(tokens).map(([k, v]) => { const [h, s, l] = hex2hsl(v); return k + ':' + hsl2hex([(h + deg) % 360, s, l]); }).join(';') + '}';
  document.head.appendChild(style);
  await new Promise(r => setTimeout(r, 250));           // nie używaj requestAnimationFrame: w ukrytej karcie nie odpala
  const after = snap(); style.remove();
  const leaks = {};
  for (const [k, v] of before) if (after.get(k) === v) { const [s, p] = k.split('|'); const key = p + '|' + v + '|' + s; leaks[key] = (leaks[key] || 0) + 1; }
  return { tokens: Object.keys(tokens).length, elements: before.size, leaks };
}
// przykład: paletteTest().then(r => console.log(JSON.stringify(r, null, 1)))
```

Baza home (8.10.2026, pierwsza wersja testu): ~1065 elementów, 22 tokeny, 17 rodzajów wycieków (migawka `--nav-ink` nagłówka z JS, szare tła zdjęć `#d4d4d4`/`#d8d8d8`, dymki, logo marki). Twój skrypt może liczyć nieco inaczej — **porównuj zawsze z własną bazą z tego samego skryptu**. Test nie widzi stałych kolorów wewnątrz `<filter>`; sprawdza je skan V2.

## Dodatek B. Lista dozwolonych klas i kolizje (V4)

```python
import re, glob, sys, pathlib
M = pathlib.Path(sys.argv[1])                                   # MAKIETA
home_css = ['minimal','typography-book','animacje','zespol-rejestr','zespol-stopka','social-promo','layout-editorial','design-tokens']
css_txt = ''.join((M/f'{n}.css').read_text(encoding='utf-8') for n in home_css)
css_txt = re.sub(r'/\*.*?\*/', '', css_txt, flags=re.S)
home_html = (M/'index-min.html').read_text(encoding='utf-8')
js_txt = ''.join((M/f).read_text(encoding='utf-8') for f in ['minimal.js','animacje.js','illustration-motion.js','pet-photos.js'])
cls_css  = set(re.findall(r'\.([A-Za-z_][\w-]*)', re.sub(r'url\([^)]*\)|"[^"]*"|\'[^\']*\'', '', css_txt)))
cls_html = {c for m in re.findall(r'class="([^"]*)"', home_html) for c in m.split()}
cls_js   = set(re.findall(r'[\'"`.]((?:is|has|will|rule|menu)-[\w-]+)', js_txt))
HOME = cls_css | cls_html | cls_js
new_css = pathlib.Path(sys.argv[2]).read_text(encoding='utf-8')                # podstrony.css
new_css = re.sub(r'/\*.*?\*/', '', new_css, flags=re.S)
DEFINED = set(re.findall(r'\.([A-Za-z_][\w-]*)', re.sub(r'url\([^)]*\)|"[^"]*"', '', new_css)))
used = set()
for f in glob.glob(str(pathlib.Path(sys.argv[3])/'**/*.html'), recursive=True):   # WYJŚCIE
    used |= {c for m in re.findall(r'class="([^"]*)"', pathlib.Path(f).read_text(encoding='utf-8')) for c in m.split()}
print('NIEZNANE (użyte, nieznane home ani podstrony.css):', sorted(used - HOME - DEFINED))
print('KOLIZJE (zdefiniowane w podstrony.css, a istniejące na home):', sorted((DEFINED & HOME) - {'subpage','visually-hidden'}))
```
Uruchom: `python3 klasy.py MAKIETA podstrony/podstrony.css podstrony`. Kolizje wolno zostawić tylko, gdy świadomie rozszerzasz klasę home przez `body.subpage …` — wypisz je w raporcie.

## Dodatek C. Lista kontrolna przed oddaniem

- [ ] 17 stron + `index.html` przeglądu + `_bloki.html` + `_obrazy.*` + `_raport.md` w `podstrony/`.
- [ ] Żaden plik poza `podstrony/` nie został zmieniony (porównaj sumy kontrolne korzenia przed/po).
- [ ] V2: zero literałów koloru; V3: zero nowych wycieków; V4: zero nieznanych klas.
- [ ] Każda strona: jeden `h1`, spis treści na początku, działające kotwice, `canonical` produkcyjny, JSON-LD poprawny.
- [ ] Pilne informacje widoczne bez interakcji; numer telefonu w zasięgu wzroku.
- [ ] Nie ma ani jednego zdania medycznego spoza `TREŚCI`.
- [ ] Raport wskazuje, czego nie sprawdzono.
