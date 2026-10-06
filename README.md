# Psyjaciele — statyczna makieta

Aktualna makieta strony głównej Przychodni Weterynaryjnej Psyjaciele. HTML, CSS i JavaScript oraz lokalne ilustracje, zdjęcia i fonty. Repozytorium nie jest połączone z publikacją produkcyjnej strony WordPress.

## Uruchomienie

W katalogu repozytorium:

```sh
python3 -m http.server 8765
```

Otwórz `http://127.0.0.1:8765/`. Plik `index.html` przekierowuje do aktualnego `index-min.html`.

## Aktualne pliki

- `index-min.html` — strona główna, teksty, metadane i przypisania palet.
- `minimal.css` — siatka 12 kolumn, zestawy kolorów, układ responsywny i pływający header.
- `minimal.js` — menu, aureola założycielek, pomiar headera i lazy load animowanej ilustracji.
- `motion.js` — animacje GSAP reagujące na przewijanie.
- `assets/` — lokalne zasoby, biblioteki GSAP/ScrollTrigger, oryginalne ilustracje i statyczne pierwsze klatki.

Podstrony usług, zespołu i polityki prywatności są wcześniejszymi statycznymi kopiami. Bieżące prace projektowe obejmują stronę główną. `index-poprzedni.html` zachowuje wcześniejszą wersję do porównania.

## Stan makiety

Hero mieści się w 96% wysokości okna. Każda sekcja ma ilustrację, a układ korzysta ze wspólnej siatki i zmiennych CSS. Nagłówki i kafle mają animacje wejścia; ilustracje reagują na scroll. Przy ograniczeniu ruchu nowe animacje są wyłączane. Animowana ilustracja hero ładuje się dopiero w widocznym obszarze i odtwarza się raz.

Makieta zawiera teksty robocze i miejsca na przyszłe zdjęcia. Strona główna ma `noindex,follow`; przed ewentualną publikacją trzeba potwierdzić aktualność treści biznesowych i zmienić ustawienie indeksowania. Samo umieszczenie kodu na GitHub nie publikuje witryny ani nie zmienia WordPressa.

Prawa do zdjęć, ilustracji, fontów i bibliotek pozostają przy ich właścicielach. Nagłówki licencyjne bibliotek zachowano w plikach.
