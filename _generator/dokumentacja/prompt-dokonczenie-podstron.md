# Prompt: dokończ makietę podstron przychodni „Psyjaciele”

Jesteś doświadczonym front-end developerem/typografem. Kończysz pracę nad statyczną makietą podstron przychodni weterynaryjnej „Psyjaciele” (Warszawa Gocław). Poprzedni model wyczerpał limit. Pracujesz **samodzielnie**: sam znajdź pliki, zbuduj, sprawdź zrzutami, popraw. Odpowiadaj po polsku, krótko, bez wstępu i podsumowania; struktura ponad prozą. Nie fabrykuj niczego (tekstów, liczb, API). Przy nietrywialnych twierdzeniach podaj „Pewność: wysoka/umiarkowana/niska”.

## 0. Zasada współpracy z właścicielem
- Kierunek należy do właściciela. Wydane polecenia są **zamknięte** — nie proponuj ich wycofania. Problem w kierunku zgłoś **raz**, krótko, z konkretnym powodem, i rób po jego myśli.
- Przy niejasności tylko krótkie pytanie. Przy usuwaniu elementów ozdobnych: najpierw pytanie, ze zrzutem, po jednym elemencie.
- **Strony głównej (`index.html` w korzeniu) nie ruszaj** bez zgody.

## 1. Gdzie jest praca
- Katalog roboczy (jeśli jest): `/home/claude/makieta`. Jeśli go nie ma — źródło prawdy to kopia na Macu: `/Users/milajovovich/Documents/Codex/2026-10-06/pracujesz-na-stronie-psyjacielevet-pl-masz-3/outputs/makieta` (w `device_bash`: `$HOME/mnt/makieta`). Skopiuj/wstaw ją do kontenera i pracuj tam.
- Generator statyczny: `podstrony/_narzedzia/` (`build.py`, `bloki.py`, `strony.py`, `plany.py`, `home.py`, `checks.py`, `audit.py`, `obrazy.py`). Arkusz: `podstrony/podstrony.css`, skrypt: `podstrony/podstrony.js`. Wersje cache: `CSS_V`, `JS_V` w `build.py` (podbijaj przy każdej zmianie CSS/JS).
- Teksty **dosłownie** ze źródeł `tresci-podstron/czyste/*.html` (nie zmieniaj treści; wyjątki poniżej).
- Wynik: 17 podstron w `podstrony/` (hub usług `uslugi-weterynaryjne/`, 14 usług, `zespol/`, `polityka-prywatnosci/`) + `podstrony/index.html` i `_bloki.html`.
- Budowa i kontrola:
  ```
  cd <makieta>
  python3 podstrony/_narzedzia/build.py
  python3 podstrony/_narzedzia/checks.py     # ma dać 17× OK
  (python3 -m http.server 8765 w korzeniu makiety, w tle)
  python3 podstrony/_narzedzia/audit.py      # Playwright, szerokości 1440,1280,1024,768,390; nie może zgłaszać flag
  ```
  Chromium+Playwright są w kontenerze (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`; nie uruchamiaj `playwright install`). Zrzuty: Playwright, przewiń stronę przed zrzutem (lazy-load obrazów), ignoruj artefakt sticky-nagłówka na zrzutach full-page.
- Synchronizacja na Maca, gdy właściciel każe „zapisz zmiany”: spakuj `podstrony/` do `.tgz` w `/mnt/user-data/outputs/`, `device_commit_files` do `…/makieta/_sync/podstrony-sync.tgz`, na Macu `device_bash` + Python: wypakuj pliki `podstrony/*` **zapisując bajty ręcznie** (`open(name,'wb')`; `extractall` nie nadpisał plików), potem `rm -rf _sync`, na końcu zweryfikuj (np. `grep CSS_V`). Prawo kasowania na Macu jest.

## 2. Siatka i rytm
- 12 kolumn, max 1280 px (`--width`), rynna `--gap` 32 px (24 px w 701–1000, 16 px ≤700), margines `--gutter: clamp(24px,4.2vw,55px)`. Rytm pionowy 8 px (`--s1..--s6`). Przy 1440: kolumna 77,33 px; 4 kol. = 405 px, 6 kol. = 624 px, 8 kol. = 843 px.
- **Wszystko rygorystycznie w siatce.** Tymczasowa nakładka siatki (blok `TEMP-GRID` w CSS, klawisz G lub `?siatka=1`) zostaje, dopóki właściciel nie każe jej usunąć.

## 3. Zasady wiążące (dosłowne polecenia właściciela — nie łamać)
**Hero**
- Po lewej tytuł Satoshi, duży, **jedną wielkością**, nie wersaliki, nie Rialto. Po prawej lead. Wszystko w siatce.
- Ilustracja po lewej, **pod tytułem**. Przyciski i informacja o otwarciu **pod tytułem**. Układ: `.poster-heading` 1/span 6, `.poster-copy` 7/span 6, `.hero-actions` 1/span 6, `.poster-art` 1/span 6; ≤1000 px jedna kolumna.
- Usunięte zdanie „Umów wizytę: wybierz termin online w Wettermin albo zadzwoń: 537 821 345” (powtarzało przyciski) — w hero i w `cta_band`. Nie przywracaj (checks.py je pomija).
- Hero każdej usługi używa ilustracji kafla z Home.

**Spis treści**
- Lewa szpalta na wszystkich stronach (poza zespołem — bez TOC), **4 kolumny**. Aktywna pozycja ma po lewej **strzałkę**. Podpunkty oddzielone kreskami i wcięte o ok. **20 px** w prawo.

**Artykuły i obrazy**
- Szerokość artykułów na podstronach **8 kolumn, po prawej** (kolumny 5–12).
- Zdjęcie zawsze w ciągu artykułu.
- **Zdjęcia i obrazki w tekście bez wyjątku: 4 lub 8 kolumn.**
- **Nigdy** układ „tytuł w treści po jednej stronie, treść po drugiej” — dozwolony wyłącznie w hero (zlecony jawnie).
- **Nigdy nie rozbijaj tytułu** na człony/linie wizualne (np. „Czy czipowanie / jest obowiązkowe” w dwóch krojach). Tytuł to **jeden napis Satoshi**, tylko większy.

**Rialto**
- Rialto **wyłącznie** w 2 największych rozmiarach zadeklarowanych w zmiennych globalnych (tak ma być na Home). **Nigdzie indziej — zakaz.** Obecnie na podstronach Rialto = 0 (zmienne `--font-emphasis`, `--wp--preset--font-family--rialto-script` nadpisane na Satoshi w `body.subpage`). Audyt liczy Rialto (ma być 0). Pytanie do zgłoszenia raz: czy Rialto ma wrócić na podstrony w tych 2 rozmiarach (55/89 px?), oraz że Home używa Rialto w rozmiarach płynnych (niezgodne z regułą; nie ruszać bez zgody).

**Baner „Praca w Psyjaciołach”**
- Wyśrodkowany, **8 kolumn**, na górze zdjęcie (21:9), potem przerwa **100 px**, potem tekst i **przycisk jako link na końcu linijki ostatniego akapitu** w bannerze (`.join-link`, strzałka maską). Karta ciemna `--ink`, promień `var(--s2)` (jedyny wyjątek od zakazu zaokrągleń). Na stronach usług baner jest na końcu sekcji FAQ; także na zespole.

**Reguły z wcześniejszych sesji**
- Znaczniki (strzałki, kółka z cyframi 1, 2, 3 w Satoshi 900) wiszą **poza akapitem**. Bez numeracji-ozdobnika.
- **Zero zaokrągleń i cieni** (wyjątek: baner pracy).
- Zdanie o obszarach Podkowa/Ostrowska usunięte (Home i zespół). Zespół bez TOC i bez „Którą lekarkę wybrać”; boczna lista „Lekarki” zostaje; układ profili — „zostawmy to na razie”.
- Profile lekarek: h2 „Lekarka weterynarii {imię}” (rozwinięty skrót „lek. wet.” — zlecone).
- Kontakt jako wiersze „etykieta | treść”. Etykiety usunięte, zostaje tylko „Pilne” (`h2[data-pre]::before`). Strzałka cofania na lewo od h1. Narzędzie recenzji `?uwagi=1` zostaje.
- Typografia: tytuły wymuszone na Satoshi 700, `--title-size: clamp(32px,3.6vw,48px)` na `main h2` (poza `.legal-prose h2`), h1 hero `clamp(40px,4.6vw,64px)`, lead 20/24/28 px (lh 32/32/40).

## 4. NOWE ZADANIE: tytuły wypełniają szeroką kolumnę (±25 %)
Polecenie właściciela: *„wielkość fontu w tytułach będzie się zmieniać +/-25% od rozmiaru bazowego, litery będą wypełniać całą dużą kolumnę (np. 6 kolumn)”.*

Wykonaj tak (to interpretacja — zgłoś ją w jednym zdaniu, nie pytaj):
1. **Rozmiar bazowy** = obecny token (h1 hero: `--hero-title`; h2: `--title-size`). Rozmiar każdego tytułu jest **dopasowany do jego treści**: tak dobrany, by najdłuższa linia po naturalnym łamaniu **wypełniała szerokość kolumny tytułu** (hero h1: 6 kolumn = `.poster-heading`; h2 w artykule: 8 kolumn), **ograniczony do przedziału 75 %–125 % rozmiaru bazowego** (clamp). Krótki tytuł rośnie do +25 %, długi maleje do −25 %; jeśli nie mieści się nawet przy −25 %, zostaje −25 % i łamie się naturalnie.
2. **Jeden rozmiar na tytuł** (nie zmieniaj kroju/rozmiaru wewnątrz tytułu), Satoshi 700, bez wersalików, bez rozbijania na człony. Łamanie tylko naturalne (word-wrap); zachowaj twarde spacje po jednoznakowych spójnikach (`nbsp_html`).
3. Implementacja: moduł `fitTitles` w `podstrony.js` — dla każdego `h1.page-hero`/`main h2` binarne wyszukiwanie `font-size` (krok zaokrąglony do 1 px), pomiar najdłuższej linii (Range/`getClientRects` albo `scrollWidth` przy `white-space: nowrap` na klonie), przeliczenie przy `resize` (debounce) i po załadowaniu fontów (`document.fonts.ready`). **Fallback bez JS = rozmiar bazowy.** Ustaw rozmiar przez zmienną `--fit` na elemencie; `line-height` ma pozostać wielokrotnością 8 px (`round(up, 1.06em, 8px)` lub liczone w JS).
4. Wyłączenia: ≤700 px (kolumna jedna — fit do szerokości kolumny nadal działa, ale przedział zawęź do 90–110 %), profile lekarek (26–32 px, bez zmian), `.legal-prose h2`, tytuły kafli. Nie wolno przy tym naruszyć reguły „jedna wielkość, Satoshi”.
5. Dodaj do `audit.py` sprawdzenie: rozmiar tytułu ∈ [0,75; 1,25]× baza i szerokość najdłuższej linii ≥ 90 % szerokości kolumny (dla tytułów, które się nie zmieściły przy −25 % — pomiń). Zrzuty kontrolne: hub, czipowanie, zespół, polityka przy 1440/1024/390.

## 5. Stan pracy i lista do zrobienia
Zrobione i zsynchronizowane na Maca (8.10.2026, `CSS_V=13`): hero Off→Grid, spis w szpalcie, kolumna 8 kol., baner pracy, Rialto→Satoshi, nakładka siatki, audyt osi (checks 17× OK, audit bez flag).

Do zrobienia (kolejność wg wpływu):
1. **Zadanie z sekcji 4** (fit tytułów) + aktualizacja audytu. Po wdrożeniu: build → checks → audit → zrzuty → podbić `CSS_V`/`JS_V`.
2. **Hub (`uslugi-weterynaryjne`)**: katalog usług jest w 2 kolumnach po 4 kol. (kafle 405 px, ilustracja pełna szerokość kafla; zgodne z regułą 4/8 kol.). Ostatnia poprawka: ilustracja nad tytułem we wszystkich kaflach. Do poprawienia: tytuły kafli 1 i 3 są mniejsze niż pozostałych (zbyt agresywne `font-size: inherit` w bloku „katalog usług (hub)” na końcu `podstrony.css`) — ujednolić z resztą. Rozważ powiadomienie właściciela (raz), że 14 kafli po 405 px daje bardzo długą stronę.
3. **Polityka prywatności**: po `.legal-section{padding:0}` obejrzeć zrzut (1440, 390) — tekst ma stać na osi kolumny 5, bez dużych odstępów.
4. **Ilustracje hero** `*-00-hero` dla huba, zespołu i polityki (obecnie placeholder 1:1). Z kontenera generowanie bywało zablokowane; dostępne narzędzia (deferred): `mcp__remote-devices__OpenAI_Images___Nano_Banana__*` (najpierw `image_tools_status`). Prompty: `podstrony/_obrazy.md`, `OBRAZY-PROMPTY.md`, `obrazy.py` (`zespol-03-atmosfera` ma ratio 21/9). Styl: liniowe ilustracje jak kafle Home.
5. Znane otwarte kwestie: wiszące znaczniki w mniejszych oknach; zespół — rail bez synchronizacji koloru (tylko `toc-rail` ją ma); sekcje full-bleed z Home (booking, social, reviews, about, doctors, after-hours) poza kolumną 8 kol., więc nie podlegają regule 4/8 — zgłoś raz.
6. Zaktualizuj `podstrony/_raport.md` (nowy układ: hero Off→Grid, spis w szpalcie, kolumna 8 kol., baner, Rialto→Satoshi, nakładka siatki, audyt osi, fit tytułów).
7. Na końcu: sync na Maca (sekcja 1) i krótki raport: co zrobione, jedno zdanie o interpretacji fit-tytułów, otwarte pytania (Rialto 55/89 px; Home).

## 6. Definicja ukończenia
`checks.py` 17× OK; `audit.py` bez flag (osie hero 1/7, artykuły na osi 5, obrazy 4 lub 8 kol., spis na osi 1, Rialto = 0, fit tytułów w przedziale); zrzuty 1440/1024/390 obejrzane dla huba, czipowania, zespołu, polityki; zmiany zsynchronizowane na Maca.
