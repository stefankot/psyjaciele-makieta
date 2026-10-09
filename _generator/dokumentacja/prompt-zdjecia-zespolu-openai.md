# Prompt do osobnego wątku — ujednolicone zdjęcia zespołu (OpenAI)

Skopiuj wszystko poniżej linii do nowego wątku (z włączoną wtyczką OpenAI Images).

---

## ZADANIE

Przygotuj ujednolicone portrety 7 lekarek weterynarii kliniki „Psyjaciele” (Warszawa Gocław) do sekcji „Zespół” na stronie. Mają wyglądać tak, jakby wszystkie osoby stały obok siebie na jednej sesji: **ta sama odległość aparatu, ta sama wysokość głowy w kadrze, to samo światło, to samo tło, ta sama skala sylwetki**. Dla każdej osoby wygeneruj **3 wersje** (razem 21 zdjęć).

Narzędzie: `mcp__OpenAI_Images___Nano_Banana__generate_openai_image` (jakość `high`, rozmiar `1536x1024`, `reference_images` — do 4 bezwzględnych ścieżek PNG/JPEG/WebP). Jeśli narzędzie nie jest załadowane, załaduj je przez ToolSearch (`select:mcp__OpenAI_Images___Nano_Banana__generate_openai_image`). Używaj jako referencji **tylko** plików wskazanych niżej.

## KATALOG ZE ZDJĘCIAMI ZESPOŁU (źródła)

`/Users/milajovovich/Documents/Codex/2026-10-06/pracujesz-na-stronie-psyjacielevet-pl-masz-3/outputs/makieta/assets/`

Przed generowaniem obejrzyj pliki (Read), żeby sprawdzić, co jest na zdjęciu. Dla każdej osoby użyj jako referencji tożsamości 1–2 plików (zawsze najpierw wersja z kompletnymi ramionami, jeśli istnieje):

| Osoba | Specjalizacje | Pliki źródłowe (w katalogu `assets/`) |
|---|---|---|
| Magdalena Ostrowska | choroby wewnętrzne, nefrologia i urologia, anestezjologia | `3b64aaacd150-studio-arms-v2.png`, `3b64aaacd150.webp` |
| Aleksandra Podkowa | choroby wewnętrzne, stomatologia, ultrasonografia | `e48db60840a2-studio-arms-v2.png`, `e48db60840a2.webp` |
| Julia Chutkowska-Świetlik | choroby wewnętrzne | `557c244c36a9-studio-web.png`, `557c244c36a9.webp` |
| Małgorzata Tywoniuk | kardiologia | `d9e0817d66ec-studio-web.png`, `d9e0817d66ec.webp` |
| Katarzyna Krawulska | chirurgia tkanek miękkich | `5205d4b0e462-studio-web.png`, `5205d4b0e462.webp` |
| Olga Winnicka-Ziółkowska | ultrasonografia | `a6e997421073-studio-arms-v2.png`, `a6e997421073.webp` |
| Kinga Bielińska-Bielecka | okulistyka | `5be50d2b873b-studio-arms-v2.png`, `5be50d2b873b.avif` (AVIF nie podawaj jako referencji — użyj `5be50d2b873b-studio-web.png`) |

Pliki `*-studio-tonal-v3.png` to obecne czarno-białe wersje na stronie — mogą służyć tylko jako pomoc przy rozpoznaniu osoby, nie jako wzór jakości.

## JAK MAJĄ WYGLĄDAĆ (wszystkie 21 zdjęć)

**Układ kadru (identyczny w każdym zdjęciu):**
- Poziomy kadr 3:2 (1536×1024). Osoba **na środku**, od głowy do **połowy ud / bioder** — dolna krawędź kadru ucina sylwetkę poziomo, jak w referencji „zespół w rzędzie”. Nad głową zostaje ok. 10–12 % wysokości kadru wolnej przestrzeni.
- **Głowa zawsze tej samej wielkości**: od czubka głowy do brody ok. 26–28 % wysokości kadru; oczy na ok. 1/4 wysokości kadru od góry. Szerokość sylwetki (ramiona) ok. 40–45 % szerokości kadru, więc po bokach jest dużo wolnego tła (zdjęcia będą wstawiane w pasy 3:2 obok siebie).
- Aparat na wysokości oczu, obiektyw portretowy (ok. 85 mm), bez zniekształceń, ostra twarz, delikatnie miękkie tło.

**Tło i światło (identyczne w każdym zdjęciu):**
- Jednolite, matowe, bardzo jasne neutralne szare tło studyjne (ok. `#DADDE1`), bez wzorów, bez podłogi, bez cieni rzucanych na ścianę, bez przejść i winiet, aby tło dało się łatwo zastąpić kolorem strony.
- Miękkie, duże, rozproszone światło z lekko lewej strony od aparatu (softbox) i delikatne światło wypełniające z prawej; naturalne, nieprzesadzone cienie na twarzy i ubraniu, zachowana faktura skóry (pory, drobne zmarszczki), bez wygładzania i bez „plastikowej” skóry, bez halo wokół włosów.
- Wykończenie fotografii redakcyjnej: **neutralna czerń i biel** (zgodnie z obecnym stylem strony), jasne, świetliste półtony, łagodnie podniesiona czerń, stonowany kontrast. Ciemne ubrania rozjaśnij do średniego grafitu z widocznymi fałdami i fakturą, ciemne włosy lekko podnieś z zachowaniem pojedynczych pasm.

**Osoba:**
- Dokładnie ta sama osoba co na zdjęciach źródłowych: twarz, wiek, rysy, proporcje, fryzura, okulary, biżuteria, strój (kroje i wzory), stetoskop i sprzęt. Bez makijażu „na nowo”, bez upiększania i zmiany rysów twarzy, bez zamiany twarzy.
- **Wolno zmienić** położenie sylwetki i twarzy (obrót ciała, przechylenie głowy, ułożenie rąk), jeśli dzięki temu zdjęcia lepiej do siebie pasują. Dokończ brakujące części ciała (ramiona, dłonie, łokcie), jeśli źródło jest obcięte.
- Wyraz twarzy: spokojny, życzliwy, naturalny uśmiech lub lekki uśmiech; kontakt wzrokowy z aparatem w wersjach A i C, spojrzenie w bok w wersji B.
- Jedna osoba na zdjęciu; bez zwierząt, bez rekwizytów w rękach poza elementami ubioru/sprzętu medycznego (stetoskop, okulary). Bez tekstu, bez logo, bez ramek.

**Trzy wersje każdej osoby (różnią się TYLKO pozą; wszystko inne identyczne):**
- **A — frontalnie:** ramiona ustawione prosto do aparatu, ręce swobodnie opuszczone lub splecione z przodu, głowa prosto, uśmiech.
- **B — półprofil:** tułów obrócony ok. 30° w prawo od aparatu, głowa zwrócona do aparatu lub lekko w bok, ręce skrzyżowane lub jedna dłoń w kieszeni.
- **C — swobodnie:** tułów obrócony ok. 20° w lewo, lekko przechylona głowa, ręce skrzyżowane na piersi; szeroki, naturalny uśmiech.
Nie odtwarzaj mechanicznie oryginalnej pozy — dopasuj pozę do zasad kadru powyżej, zachowując charakter osoby i jej strój.

## PROCEDURA (obowiązkowa)

1. Wygeneruj **tylko 1 zdjęcie**: Magdalena Ostrowska, wersja A. Zapisz je (kopia — patrz „Zapis”) i **zatrzymaj się**. Pokaż zdjęcie i zapytaj: „Czy kontynuować? Czy coś zmienić w kadrze/świetle/skali?”. Nie generuj nic dalej bez odpowiedzi.
2. Po akceptacji **to zaakceptowane zdjęcie staje się wzorcem** („kotwica stylu”). Do każdego kolejnego zdjęcia dołączaj je w `reference_images` (jako ostatnią, trzecią lub czwartą referencję) z dopiskiem w prompcie: „Image N is the STYLE ANCHOR: match its camera distance, head size, head position in frame, crop line, background colour, lighting and tonal finish exactly; do NOT copy its person.” Pozostałe referencje to źródła tożsamości danej osoby.
3. Dalej w kolejności: Magdalena B, C → Aleksandra A, B, C → Julia → Małgorzata → Katarzyna → Olga → Kinga. **Po każdej osobie (3 zdjęcia) zapytaj, czy kontynuować.** Jeśli użytkownik zauważy odchylenie od wzorca, popraw i wygeneruj ponownie przed przejściem dalej.
4. Po każdym zdjęciu sprawdź (Read): czy głowa ma ten sam rozmiar co na kotwicy (±5 %), czy linia cięcia na dole jest w tym samym miejscu, czy tło i światło zgadzają się, czy twarz jest rozpoznawalnie tą samą osobą. Jeśli nie — wygeneruj ponownie (max 2 poprawki), potem opisz problem.

## SZABLON PROMPTU DLA NARZĘDZIA (po angielsku; podstaw dane osoby i wersji)

```
Use case: identity-preserve, consistent team portrait series.
Image 1 (and Image 2 if provided) are IDENTITY REFERENCES of one real veterinary doctor: {IMIE NAZWISKO}. Keep the exact same person: face, facial proportions, age, skin texture with natural pores, eyes, expression character, hairstyle and hair colour, glasses/jewelry/stethoscope and clothing design exactly as in the references. No beautification, no reshaping of features, no face swap.
{Image N is the STYLE ANCHOR (omit for the very first image): match its camera distance, head size, head position in the frame, crop line, background colour, lighting and tonal finish exactly; do NOT copy its person.}
Create a premium editorial studio portrait, landscape 3:2 (1536x1024). Subject centered, framed from the top of the head to mid-thigh, with the bottom edge of the frame cutting the body horizontally. Head height (crown to chin) about 27% of the frame height, eyes about one quarter down from the top, about 10-12% empty space above the head, shoulders about 40-45% of the frame width, lots of empty background on both sides. Camera at eye level, 85mm portrait lens look, no distortion.
Background: perfectly plain matte very light neutral grey studio backdrop (~#DADDE1), no floor, no pattern, no cast shadow on the wall, no vignette, no gradient.
Lighting: large soft diffused key light slightly from the left, gentle fill from the right, natural restrained shadows, real skin and fabric texture, no halos, no plastic skin.
Finish: pure neutral black-and-white, luminous bright midtones, gently lifted blacks, restrained contrast; dark clothing lightened to medium charcoal with visible folds, dark hair slightly lifted with individual strands visible.
Pose {A|B|C}: {OPIS POZY Z SEKCJI "Trzy wersje"}. Calm, friendly, natural expression. You may adjust body and head position to fit this pose; complete any missing arms/hands naturally.
Exactly one person. No animals, no props other than her clothing and medical gear, no text, no logo, no frame, no watermark.
```

## ZAPIS

Narzędzie zapisuje pliki na Biurku (`~/Desktop/<data>-openai-<id>.png`). Każde zaakceptowane zdjęcie **skopiuj** (nie przenoś) do katalogu:

`/Users/milajovovich/Documents/Codex/2026-10-06/pracujesz-na-stronie-psyjacielevet-pl-masz-3/outputs/makieta/assets/zespol-nowe/`

pod nazwą `<id-osoby>-<A|B|C>.png`, gdzie `<id-osoby>` to prefiks pliku źródłowego z tabeli (np. `3b64aaacd150-A.png`). Nie nadpisuj niczego w `assets/` poza tym podkatalogiem. Na końcu każdego etapu wypisz listę zapisanych plików i ich ścieżki.

## NA KONIEC

Po wszystkich 21 zdjęciach przygotuj plik `assets/zespol-nowe/README.md`: tabela osoba → trzy pliki → uwagi (np. które wersje najlepiej pasują do siebie jako rząd 3 osób). Nic nie edytuj w `index.html` — podmianę zdjęć na stronie wykona wątek z makietą.
