# layout-warianty — dwa warianty układu strony głównej

Pliki obok oryginałów. `index-min.html` i reszta makiety **nie zostały zmienione**.
Warianty ładują Twoje style i obrazki z folderu wyżej (`../`), więc zmiany w Twoim CSS widać w obu.

## Uruchomienie
```
cd makieta
python3 -m http.server 8765
```
- Średnia: http://127.0.0.1:8765/layout-warianty/index-srednia.html
- Odważna: http://127.0.0.1:8765/layout-warianty/index-odwazna.html

## Wspólne (layout-base.css, layout-header.js)
- Stały pasek nagłówka z tłem sekcji pod spodem (zamiast przezroczystego z mix-blend).
- Hero: dwa przyciski — „Umów wizytę” i „Zadzwoń”; na telefonie ikona słuchawki w pasku.
- Cały kafel usługi klikalny, widoczny fokus klawiatury, większy lead pod tytułami sekcji.
- Nagłówki sekcji (poster-grid) bez zmian.

## Średnia (layout-srednia.css)
Porządkuje: usługi w 4 kolumnach (ilustracja nad opisem), krótsza strona, czytelniejsze kolumny.

## Odważna (layout-odwazna.css, layout-status.js)
Średnia + hasło w hero jak plakat, chip „Otwarte teraz / Zamknięte” (liczony z godzin przyjęć),
dwa wyróżnione kafle usług, większe imiona zespołu, opinie z podpisami pismem, wielkie numery telefonów.

## Nagłówki sekcji (layout-naglowki.css) — wspólne dla obu wariantów
Charakter bez zmian: tytuł u góry, światło i ilustracja, tekst razem na dole.
- Lead pod tytułem: 16 → ok. 21 px na desktopie (tytuł ma 69 px).
- Szerokie ilustracje (Opinie, Przygotuj się, Częste pytania) nie wychodzą poza ekran — wcześniej na 1440 px ucinało ptaka.
- Mobile: tytuł → ilustracja → tekst (jak na desktopie), tytuły większe.
- Wyłączenie: usuń z `index-*.html` linijkę `<link ... layout-naglowki.css ...>`.

## Podgląd nagłówków: przed / po
http://127.0.0.1:8765/layout-warianty/naglowki-porownanie.html
Dwie działające ramki obok siebie (oryginał i wersja po zmianach), przełączniki: sekcja, ekran (desktop / laptop / tablet / telefon), wariant.

## Wersja „nowa” (index-nowa.html) — miks wg decyzji
http://127.0.0.1:8765/layout-warianty/index-nowa.html
Pliki: `layout-nowa.css`, `nowa-bar.css`, `nowa-readability.js`, `nowa-header.js`, `minimal-nowa.js`.
- **Rytm 8 px**: tokeny `--s1…s7` = 8/16/24/32/56/88/144, interlinie przez `round(…, 8px)`, 12 kolumn, odstęp 32 px. Min. 16 px tekstu na całej stronie.
- **Nawigacja**: desktop/tablet jak w oryginale (pełna szerokość, te same rozmiary), ale z podkładem w kolorze sekcji pod rozmyciem 16 px. Nowy stały pasek: telefon (≤ 700 px) oraz tryb większej czytelności (domyślna czcionka przeglądarki ≥ 18 px, „większy kontrast”; zoom strony nie jest wykrywany). Test: `?bar=1` / `?bar=0`.
- **Nagłówki sekcji**: lead 20/32 px na 4 kolumnach (≥ 1100 px), 6 kolumn na tablecie, pełna szerokość na telefonie; ilustracje jak w oryginale.
- **Hero**: tekst bez zmian + 2 przyciski + status „Otwarte teraz”.
- **#zapraszamy**: nowy tekst lekarek, bez Instagrama/Facebooka; na telefonie dwa kwadraty (tekst, pies). Kropki min. 50 px (`minimal-nowa.js` = kopia minimal.js z poprawką animacji kropek).
- **#uslugi** odważna, **#przychodnia** numeracja + listy, **#zespol** średnia, **#rekomendacje** odważna bez przesuniętych kolumn, **#obserwuj-nas** odwrócony przycisk, kot w kwadracie, logo 80 vw, **#kontakt** średnia.
