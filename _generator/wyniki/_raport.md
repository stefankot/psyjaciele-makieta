<!-- generated: psyjaciele-podstrony -->
# Raport — podstrony Psyjaciół (stan z 8.10.2026, po porządkach)

## 1. Struktura (opis w `README.md` w korzeniu makiety)
- Strona główna: `index.html` (dawny `layout-warianty/index-nowa.html`; bez IG/FB w rezerwacji, nowy tekst rezerwacji).
- Podstrony (17) w korzeniu: `uslugi-weterynaryjne/` (hub + 14 usług), `zespol/`, `polityka-prywatnosci/`. Generowane z `index.html` + tekstów w `_generator/tresci-podstron/`.
- Style i skrypty podstron: `podstrony.css` (v36), `podstrony.js` (v14), obok stylów strony głównej.
- Generator: `_generator/narzedzia/` (`build.py`, `checks.py`, `audit.py`, …); wyniki: `_generator/wyniki/` (ten raport, rejestr obrazów, katalog podstron, zrzuty).
- Stare wersje: `_archiwum/` (nic nie skasowane; kopia `kopia-przed-porzadkami-2026-10-08.tgz`).

## 2. Układ — obowiązujące decyzje właściciela
- **Hero 2×2:** heading | lead; przyciski i informacja o otwarciu | ilustracja (kol. 7–12, do góry i lewej, przycięta do zawartości). Poniżej 1000 px jedna kolumna. Tytuł Satoshi 700 jedną wielkością (fitTitles usunięty).
- **Spis treści** jako lewa szpalta 4 kol., strzałka przy aktywnej pozycji, kreski nie szersze niż najdłuższa linia liter.
- **Artykuł** w kolumnach 5–12; zdjęcia i obrazki 4 lub 8 kol.; zdjęcie 4 kol. + tekst obok 4 kol. (tekst z kreską u góry), strony naprzemiennie.
- **Rezerwacja** w kolumnie artykułu, pionowo: tekst na górze, pies pod spodem (8 kol.), bez latających zdjęć zwierząt.
- **Baner pracy:** zdjęcie 300 px, pod nim kontener min. 300 px z tytułem na górze; tekst łamany równo.
- **Znaczniki:** strzałki/kółka wiszą poza akapitem; listy `ruled-list` mają kropki 10 px; FAQ: plus/minus w kółku; callout: trójkąt ostrzegawczy zamiast ramki.
- **Nagłówek strony:** dane kontaktowe zaczynają się na osi 7 (od 1440 px; 1440–1599 px bez strzałki przy „Umów wizytę”).
- **Rialto:** na podstronach 0 (tytuły Satoshi). Nakładka siatki (klawisz G, `?siatka=1`) zostaje do odwołania.

## 3. Zweryfikowane
- `build.py` + `checks.py`: 17× OK (po ostatniej zmianie).
- Wszystkie lokalne odnośniki i `url()` z 18 stron (Home + 17) wskazują istniejące pliki (poza celowymi placeholderami `assets/podstrony/…`).
- Punktowo na `czipowanie-psow-i-kotow` (1440 i 1710 px): hero 2×2, osie, rezerwacja, pary zdjęcie+tekst, tabela kontaktu (30 px od najdłuższej etykiety), baner pracy (300 + 300 px), spacing polityki prywatności.

## 4. Niesprawdzone / znane ograniczenia
- Pełny `audit.py` (17 stron × 5 szerokości) po porządkach i po przeniesieniu rezerwacji do kolumny **nie był uruchomiony** (oszczędność tokenów, polecenie właściciela); mogą wyjść flagi osi dla elementów rezerwacji.
- Pary zdjęcie+tekst, rezerwacja pionowa i hero 2×2 obejrzane tylko na stronie czipowania; zespół, hub i polityka sprawdzone punktowo.
- Pod `file://` przeglądarka blokuje czcionki i maski SVG (CORS); makietę otwieraj przez serwer (`python3 -m http.server`).
- Ilustracje: placeholdery nadal czekają na 22 brakujące rysunki i 49 zdjęć; prompt do generowania: `_generator/dokumentacja/prompt-ilustracje-openai.md`.
- Otwarte pytania do właściciela: czy Rialto ma wrócić na podstrony w 2 największych rozmiarach (55/89 px); Home używa Rialto w rozmiarach płynnych (niezgodne z regułą); sekcje full-bleed z Home (social, reviews, doctors, after-hours) stoją poza kolumną 8 kol., więc nie podlegają regule 4/8.
- Z wcześniejszych sesji: `--bake` nie jest zaimplementowane; plan stron to generyczny silnik (`plany.py`); `generuj_obrazy.py` nieprzetestowany.
