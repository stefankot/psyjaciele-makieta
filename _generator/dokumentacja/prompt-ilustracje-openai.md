# Prompt: wygeneruj brakujące ilustracje przychodni „Psyjaciele” (wtyczka OpenAI)

Jesteś ilustratorem i front-end developerem. W makiecie strony przychodni weterynaryjnej „Psyjaciele” (Warszawa Gocław) brakuje 22 ilustracji. Wygeneruj je przez wtyczkę obrazów OpenAI, tak by **świetnie pasowały klimatem i stylem do istniejących** (zestaw Cole i nowe ilustracje właściciela), wstaw je do makiety i podepnij filtr kolorystyczny. Odpowiadaj po polsku, krótko, bez wstępu i podsumowania. Nie fabrykuj niczego. Przy nietrywialnych twierdzeniach podaj „Pewność: wysoka/umiarkowana/niska”.

## 0. Zasady współpracy
- Kierunek należy do właściciela; wydane polecenia są zamknięte. Przy niejasności zadaj jedno krótkie pytanie.
- **Oszczędność tokenów (polecenie właściciela):** nie przeglądaj wielu stron i nie uruchamiaj pełnych audytów między zmianami. Weryfikuj punktowo: jeden pomiar i najwyżej jeden zrzut elementu.
- Generowanie jest płatne. **Najpierw 3 próbki** (patrz §5), pokaż je właścicielowi i dopiero po akceptacji generuj resztę.
- Strony głównej (`index.html` w korzeniu makiety) nie ruszaj bez zgody.

## 1. Gdzie jest praca
Makieta (praca bezpośrednio tam): `/Users/milajovovich/Documents/Codex/2026-10-06/pracujesz-na-stronie-psyjacielevet-pl-masz-3/outputs/makieta`. Przeczytaj `README.md` w korzeniu (struktura, komendy). Skrót:
- strona główna `index.html`; podstrony generowane w `uslugi-weterynaryjne/`, `zespol/`, `polityka-prywatnosci/`; styl i skrypt podstron: `podstrony.css`, `podstrony.js`; obrazy: `assets/`;
- generator: `_generator/narzedzia/` (`build.py`, `checks.py`), teksty źródłowe: `_generator/tresci-podstron/czyste/<slug>.html`, rejestr obrazów: `_generator/wyniki/_obrazy.json` (pole `plik` = docelowa ścieżka, `opis_pl`, `sekcja`, `ratio`, `prompt_en`);
- po każdej zmianie CSS/JS podbij `CSS_V` / `JS_V` w `build.py`; budowa i kontrola: `python3 _generator/narzedzia/build.py` i `python3 _generator/narzedzia/checks.py` (ma dać 17× OK). Wymaga `beautifulsoup4` (brak w systemie: zapytaj o zgodę na venv w katalogu tymczasowym);
- serwer podglądu: `python3 -m http.server 8766 --bind 127.0.0.1` w katalogu makiety (port 8765 może zajmować inny projekt). Nie otwieraj przez `file://` (blokada czcionek i masek).

## 2. Narzędzia obrazów
Narzędzia wtyczki są odroczone: załaduj je przez ToolSearch (`select:mcp__OpenAI_Images___Nano_Banana__image_tools_status,mcp__OpenAI_Images___Nano_Banana__generate_openai_image`). Najpierw `image_tools_status` (bez kosztu). Do generowania używaj **`generate_openai_image`**:
- `quality: "high"`, `transparent_background: false`;
- `size`: `1024x1024` dla 1:1, `1536x1024` dla 4:3;
- `reference_images`: maks. **4** ścieżki bezwzględne (PNG/JPEG/WebP; SVG odpada). **Właściciel wskazuje jako referencje wyłącznie pliki z §3.**
- Wynik zapisuje się na **Biurku** właściciela (`~/Desktop`), nazwa w formacie `<data ISO>-openai-<uuid>.png`. Ustal plik po czasie utworzenia tuż po wywołaniu. **Kopiuj, nie przenoś**; nie kasuj niczego z Biurka.

## 3. Referencje stylu (jedyne dozwolone do wysyłania)
Prefiks: `/Users/milajovovich/Documents/Codex/2026-10-06/pracujesz-na-stronie-psyjacielevet-pl-masz-3/outputs/makieta/assets/illustrations/`

- **Nowe, właściciela** (styl domowy; zwierzęta jak ludzie, groteskowo-łagodne): `services/service-internal-a.png`, `services/service-cardiology-b.png`, `services/service-eyes-a.png`, `services/service-dentistry-a.png`, `services/service-laboratory-b.png`, `services/service-imaging-c.png`, `services/service-microchip-b.png`, `services/service-passport-b.png`, `services/service-pressure-b.png`, `services/service-skin-a.png`, `services/service-surgery-b.png`, `services/service-urology-a.png`, `services/service-kidneys-b.png`, `services/service-prevention-a.png`
- **Cole** (nieco bardziej szczegółowy kontur, przedmioty i sprzęt): `clinic-equipment-cole-v2.png`, `clinic-equipment-cole.png`, `emergency-care-cole.png`, `prepare-for-visit-cole.png`, `services-reception-cole.png`, `services-reception-shouting-cat.png`

**Przed generowaniem obejrzyj co najmniej 6 z nich** (Read na pliku PNG) i opisz sobie styl własnymi słowami. Obserwacje (do potwierdzenia): czarna, jednolita linia o stałej grubości, bez szarości, cieniowania i gradientów; drobne, świadome pełne czernie (ucho, nos, buty, kółka); bohaterowie to zwierzęta w ludzkich rolach (pies w swetrze, kot lekarz w fartuchu ze stetoskopem), mina pozbawiona emocji, delikatny humor w detalu (zygzaki bólu, wąsy jak kreski); sprzęt narysowany prosto i „po ludzku”; duże białe marginesy; rysunek lekko odręczny, nie wektorowy-sterylny.
Dla każdego obrazu wybierz **4 referencje najbliższe tematycznie**: min. 2 z „nowych” i min. 1 z Cole. Do przedmiotów i schematów dołącz Cole (sprzęt), do postaci „nowe”.

## 4. Wymagania techniczne obrazu
- **Białe tło (#FFFFFF), czarna kreska (#000), nic więcej**: bez kolorów, szarości, cieni, tekstu, cyfr, logotypów, napisów na opakowaniach/okładkach/ekranach. Bez twarzy ludzi (zwierzęta mogą mieć miny).
- Stała grubość linii, spójna z referencjami; kompozycja w środkowych ~75% kadru, równe białe marginesy (obraz będzie przycinany do zawartości).
- Prompt do modelu pisz po angielsku, zaczynaj od opisu stylu („monoline black ink illustration on pure white background, in the exact style of the reference images: …”), potem temat, potem „no text, no numbers, no shading, no grey, no colour”.
- **Temat obrazu wymyśl sam**, najlepszy w kontekście: przeczytaj sekcję, przy której stoi obraz (tytuł + akapity, kolumna `sekcja` w rejestrze; tekst źródłowy `_generator/tresci-podstron/czyste/<slug>.html`, wynik w `uslugi-weterynaryjne/<slug>/index.html`), i narysuj coś, co **uzupełnia sens**, a nie powtarza go dosłownie (np. zamiast „schemat serca” scena z psem i uproszczonym sercem jak z referencji). Kolumna „Wskazówka” poniżej to tylko punkt wyjścia z rejestru. Bez drastyczności i bez ran.

## 5. Lista 22 ilustracji
Ścieżka zapisu = `assets/podstrony/<slug>/<id>.png` (w makiecie). **Wszystkie jako PNG** (dotychczasowe `.svg` diagramów zmieniasz na `.png`, patrz §6).

**Próbki (najpierw te 3, pokaż właścicielowi):** `uslugi-00-hero`, `czip-01-czip-diagram`, `lab-02-probki`.

| id | slug strony | proporcje / size | sekcja | wskazówka z rejestru |
|---|---|---|---|---|
| uslugi-00-hero | uslugi-weterynaryjne | 1:1 / 1024² | hero (ilustracja obok leadu) | hero huba usług, w stylu kafli usług z home |
| zespol-00-hero | zespol | 1:1 / 1024² | hero | hero zespołu: lekarki i zwierzęta |
| uslugi-04-kot-pies | uslugi-weterynaryjne | 1:1 | jak-wyglada-wizyta | kot i pies siedzące obok siebie |
| lab-02-probki | diagnostyka-laboratoryjna-weterynaryjna | 1:1 | jakie-badania-moga-byc-potrzebne… | statyw z probówkami (bez etykiet) |
| szcz-02-ksiazeczka | szczepienia-oraz-profilaktyka-przeciwpasozytnicza | 1:1 | profilaktyka-przeciwpasozytnicza… | książeczka zdrowia zwierzęcia |
| kard-03-ekg | kardiologia-weterynaryjna | 1:1 | badania-diagnostyczne… | elektrody EKG z kablami |
| derm-04-pielegnacja | dermatologia-weterynaryjna | 1:1 | leczenie-chorob-skory | szczotka do sierści |
| stom-04-pies-szczotka | stomatologia-weterynaryjna | 1:1 | jak-wyglada-zabieg-stomatologiczny | pies obok szczoteczki |
| uro-04-pies-spacer | urologia-weterynaryjna | 1:1 | leczenie-chorob-dolnych-drog-moczowych… | pies na smyczy |
| pasz-01-paszport | wystawianie-paszportow-psom-i-kotom | 1:1 | co-zawiera-paszport | zamknięty paszport (okładka bez tekstu) |
| czip-05-pies-kot | czipowanie-psow-i-kotow | 1:1 | czy-czipowanie-jest-obowiazkowe | spokojny kot i mały pies |
| interna-02-schemat-ukladow | choroby-wewnetrzne-u-psow-i-kotow | 4:3 / 1536×1024 | kiedy-nie-czekac-na-wolny-termin | zarys psa z układami |
| szcz-03-kalendarz | szczepienia-oraz-profilaktyka-przeciwpasozytnicza | 4:3 | profilaktyka-przeciwpasozytnicza… | oś z punktami (bez dat) |
| chir-04-rana-schemat | chirurgia-weterynaryjna-tkanek-miekkich | 4:3 | jakie-badania-wykonac-przed-operacja | opatrunek na łapie (bez ran) |
| kard-01-serce-diagram | kardiologia-weterynaryjna | 4:3 | objawy-ktore-moga-wskazywac-na-chorobe-serca | serce, przepływ krwi |
| usg-02-mapa-ciala | diagnostyka-obrazowa-psow-i-kotow | 4:3 | co-mozna-zbadac-za-pomoca-usg | zarys psa z oknami badania |
| oko-01-oko-diagram | okulistyka-weterynaryjna | 4:3 | kiedy-do-okulisty-a-kiedy-pilnie | przekrój oka |
| stom-01-jama-ustna-diagram | stomatologia-weterynaryjna | 4:3 | objawy-ktorych-nie-warto-przeczekac | ząb w dziąśle |
| nefr-01-nerki-diagram | nefrologia-weterynaryjna | 4:3 | objawy-problemow-nefrologicznych… | nerki i moczowody |
| uro-01-uklad-moczowy-diagram | urologia-weterynaryjna | 4:3 | objawy-chorob-dolnych-drog-moczowych | dolne drogi moczowe |
| cis-01-mankiet-diagram | pomiar-cisnienia-psow-i-kotow | 4:3 | kiedy-warto-zmierzyc-cisnienie | łapa z mankietem |
| czip-01-czip-diagram | czipowanie-psow-i-kotow | 4:3 | jak-dziala-czip | czip obok ziarna ryżu, miejsce wszczepienia |

Poza zakresem: 49 zdjęć (rodzaje `foto` i `pas`): to czarno-białe fotografie, nie ilustracje.

## 6. Po wygenerowaniu: wstawienie do makiety
1. Dla każdego obrazu: sprawdź wynik (białe tło, brak tekstu, jedna grubość linii, styl zgodny z referencjami); w razie wady jedna poprawka promptu, nie więcej niż 2 próby na obraz. Skopiuj plik z Biurka pod `assets/podstrony/<slug>/<id>.png`.
2. Zaktualizuj rejestr w `_generator/narzedzia/obrazy.py`: `EXT['diagram'] = 'png'`; wszystkie trzy rodzaje (`ilustracja`, `wycinek`, `diagram`) dostają obróbkę `ink-filter` zamiast `alpha`/`svg-mask`; w opisach i promptach zamień „przezroczyste tło” na „białe tło, czarna kreska”. `python3 _generator/narzedzia/build.py` przebuduje strony i manifest.
3. `podstrony.js` (`initPlaceholders`) podmienia ramkę `figure.placeholder[data-src]` na `<img>`, gdy plik istnieje. **Dodaj filtr**: ilustracje w tekście mają mieć **tło w kolorze uzupełniającym i kreskę kontrastową do tego tła**. Rób to tak, jak hero usług (`art_figure` w `_generator/narzedzia/bloki.py`: filtr SVG `feColorMatrix` luminancja→alfa, `feFlood flood-color="var(--ink)"`, `feComposite in`):
   - dla ramek `[data-kind="ilustracja"|"diagram"|"wycinek"]` wstrzyknij **per ramkę** (nie globalnie: `var(--ink)` musi się rozwiązać w palecie danej sekcji) ukryty `<svg><filter id="…unikalne…">` i ustaw `img { filter: url(#…) }`;
   - tło ramki: `var(--accent)` palety sekcji (kolor uzupełniający), kreska: `var(--ink)`; usuń wzór kreskowania placeholdera; `mix-blend-mode: normal`; `object-fit: contain`;
   - zmień regułę w `podstrony.css` (`.photo-frame[data-kind="diagram"].has-image > img … { filter: none }`);
   - **sprawdź kontrast** `--ink` względem `--accent` we wszystkich paletach sekcji (≥ 3:1); jeśli któraś para nie przechodzi, powiedz właścicielowi i zaproponuj `--surface` zamiast `--accent` dla tej palety.
4. Hero (`uslugi-00-hero`, `zespol-00-hero`): gdy plik istnieje, generator ma użyć `B.art_figure(...)` jak dla stron usług (`strony.py`, metoda `hero`, zamiast `hero-placeholder`), czyli kreska w kolorze `--ink` na tle sekcji (bez ramki). `podstrony.js` przycina ilustracje hero do zawartości (`heroArtAlign`), więc białe marginesy nie szkodzą.
5. Zasady wiążące makiety: ilustracje w tekście zajmują **4 lub 8 kolumn**; zero zaokrągleń i cieni; znaczniki wiszą poza akapitem; tytuły jednym krojem (Satoshi), bez rozbijania na człony.

## 7. Definicja ukończenia
22 pliki w `assets/podstrony/…`; `build.py` i `checks.py` bez błędów (17× OK); na jednej stronie wzorcowej (np. `czipowanie-psow-i-kotow`) zrzut elementu z ilustracją pokazuje tło `--accent` i kreskę `--ink`; krótki raport: co zrobione, ile prób na obraz, koszt (liczba wywołań), otwarte pytania.
