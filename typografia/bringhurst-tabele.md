# Tabele Bringhursta uzupełnione (rekonstrukcja)

Uzupełnienie do [katalog.md](katalog.md). W PDF-ie Bringhursta (warstwa OCR) uszkodzone są: tabela liczby znaków w wierszu (s. 29), tabele proporcji stron i kolumn (s. 148–149) i pierwszy ciąg rozmiarów w s. 157. Poniżej odtworzono je z trzech źródeł. Żadna z tych tabel nie jest transkrypcją z oryginału; tam, gdzie liczby pochodzą z mojej wiedzy lub rachunku, jest to oznaczone.

Oznaczenia pochodzenia:
- **O** wartość i nazwa czytelne w OCR (zgodne z podpisami na s. 150–153);
- **R** obliczone z definicji (interwały muzyczne, stałe matematyczne, wymiary arkuszy);
- **W** wnioskowane z kontekstu lub z mojej wiedzy o książce; do sprawdzenia ze skanem.
- Pominięto: przykładowe formaty (kolumna „Sample sizes” na s. 148–149), bo to ilustracje, nie reguły.

## 1. Średnia liczba znaków w wierszu (B s. 29)

Jak czytać: wiersz = długość małego alfabetu (pt, A), kolumna = długość wiersza (pc, L). Wartość = liczba znaków ze spacjami i interpunkcją w wierszu średniej długości.

Pochodzenie komórek: **582** z 608 odczytano z OCR (po ułożeniu rozproszonych ciągów liczb do właściwych wierszy), **26** oznaczonych `*` uzupełniono proporcjonalnie z sąsiedniej komórki tego samego wiersza (błąd ±1). Cyfry w kilku komórkach OCR są pomylone; sprawdzono je przez monotoniczność wierszy i kolumn oraz zgodność z przybliżeniem poniżej.

Przybliżenie, którym można liczyć poza tabelą (dopasowane do czytelnych komórek: 71% trafień dokładnych, 97% w granicach ±1 znaku):

`znaków w wierszu ≈ L[pt] / (0,4325 + 0,032 · A[pt])`, gdzie L[pt] = 12 · L[pc].

Kontrola przykładu z książki (s. 27): A = 128 pt, wiersz 25 pc = 300 pt → wzór daje 66 znaków; w tabeli wiersz A = 130 ma 62 znaki dla 24 pc i 67 dla 26 pc, czyli ok. 65 dla 25 pc, co potwierdza zapis „roughly 65”.

| A \ L (pc) | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 | 30 | 32 | 34 | 36 | 38 | 40 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **80** | 40 | 48 | 56 | 64 | 72 | 80 | 88 | 96 | 104 | 112 | 120 | 128 | 136 | 144 | 152 | 160 |
| **85** | 38 | 45 | 53 | 60 | 68 | 76 | 83 | 91 | 98 | 106 | 113 | 121 | 129 | 136 | 144 | 151 |
| **90** | 36 | 43 | 50 | 57 | 64 | 72 | 79 | 86 | 93 | 100 | 107 | 115 | 122 | 129 | 136 | 143 |
| **95** | 34 | 41 | 48 | 55 | 62 | 69 | 75 | 82 | 89 | 96 | 103 | 110 | 117 | 123 | 130 | 137 |
| **100** | 33 | 40 | 46 | 53 | 59 | 66 | 73 | 79 | 86 | 92 | 99 | 106 | 112 | 119 | 125 | 132 |
| **105** | 32 | 38 | 44 | 51 | 57 | 63 | 70 | 76 | 82 | 89 | 95 | 101 | 108 | 114 | 120 | 127 |
| **110** | 30 | 37 | 43 | 49 | 55 | 61 | 67 | 73 | 79 | 85 | 92 | 98 | 104 | 110 | 116 | 122 |
| **115** | 29 | 35 | 41 | 47 | 53 | 59 | 64 | 70 | 76 | 82 | 88 | 94 | 100 | 105 | 111 | 117 |
| **120** | 28 | 34 | 39 | 45 | 50 | 56 | 62 | 67 | 73 | 78 | 84 | 90 | 95 | 101 | 106 | 112 |
| **125** | 27 | 32 | 38 | 43 | 48 | 54 | 59 | 65 | 70 | 75 | 81 | 86 | 91 | 96* | 102* | 107* |
| **130** | 26 | 31 | 36 | 41 | 47 | 52 | 57 | 62 | 67 | 73 | 78 | 83 | 88 | 93 | 98* | 103* |
| **135** | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60* | 65* | 70 | 75 | 80 | 85 | 90 | 95 | 100 |
| **140** | 24 | 29 | 34 | 39 | 44 | 48 | 53 | 58 | 63 | 68 | 73 | 77 | 82 | 87 | 92 | 97 |
| **145** | 23 | 28 | 33 | 37 | 42 | 47 | 51 | 56 | 61 | 66 | 70 | 75 | 80 | 84 | 89 | 94 |
| **150** | 23 | 28 | 32 | 37 | 41 | 46 | 51 | 55 | 60 | 64 | 69 | 74 | 78 | 83 | 87 | 92 |
| **155** | 22 | 27 | 31 | 36 | 40 | 45 | 49 | 54 | 58 | 63 | 68* | 72 | 76 | 81 | 85 | 90 |
| **160** | 22 | 26 | 30 | 35 | 39 | 43 | 48 | 52 | 56 | 61 | 65 | 69 | 74 | 78 | 82 | 87 |
| **165** | 21 | 25 | 30 | 34 | 38 | 42 | 46 | 51 | 55 | 59 | 63 | 68 | 72 | 76 | 80 | 84 |
| **170** | 21 | 25 | 29 | 33 | 37* | 41* | 45 | 49 | 53 | 57 | 62 | 66 | 70 | 74 | 78 | 82* |
| **175** | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 52 | 56 | 60 | 64 | 68 | 72 | 76 | 80 |
| **180** | 20 | 23 | 27 | 31 | 35* | 39* | 43 | 47 | 51 | 55 | 59 | 62 | 66 | 70 | 74 | 78 |
| **185** | 19 | 23 | 27 | 30 | 34 | 38 | 42 | 46 | 49 | 53 | 57 | 61 | 65 | 68 | 72 | 76 |
| **190** | 19 | 22 | 26 | 30 | 33 | 37 | 41 | 44 | 48 | 52 | 56 | 59 | 63 | 67 | 70 | 74 |
| **195** | 18 | 22 | 25 | 29 | 32 | 36 | 40 | 43 | 47 | 50 | 54 | 58 | 61 | 65 | 68 | 72 |
| **200** | 18 | 21 | 25 | 28 | 32 | 35 | 39 | 42 | 46 | 49 | 53 | 56 | 60 | 63 | 67 | 70 |
| **210** | 17 | 20 | 23 | 27 | 30 | 33 | 37 | 40 | 43 | 47 | 50 | 53 | 57 | 60 | 63 | 67 |
| **220** | 16 | 19 | 22 | 25 | 29 | 32 | 35 | 38 | 41* | 45 | 48 | 51 | 54 | 57* | 60* | 64* |
| **230** | 15 | 18 | 21 | 24 | 27 | 30 | 33 | 36 | 40 | 43 | 46 | 49 | 52 | 55 | 58 | 61* |
| **240** | 15 | 17 | 20 | 23* | 26 | 29 | 32 | 35 | 38 | 41 | 44 | 46 | 49 | 52 | 55 | 58 |
| **250** | 14 | 17 | 20 | 22 | 25 | 28 | 31* | 34 | 36 | 39 | 42 | 45* | 48* | 51* | 54* | 57* |
| **260** | 14 | 16 | 19 | 22 | 24 | 27 | 30 | 32 | 35 | 38* | 41 | 43 | 46 | 49 | 51 | 54 |
| **270** | 13 | 16 | 18 | 21 | 23 | 26 | 29 | 31 | 34 | 36 | 39 | 42 | 44 | 47 | 49 | 52 |
| **280** | 13 | 15 | 18 | 20 | 23 | 25 | 28 | 30 | 33 | 35 | 38 | 40 | 43 | 45 | 48 | 50 |
| **290** | 12 | 15 | 17 | 20 | 22 | 24 | 27 | 29 | 32 | 34 | 37 | 39 | 41 | 44 | 46 | 49 |
| **300** | 12 | 14 | 17 | 19 | 21 | 24 | 26 | 28 | 31 | 33 | 35 | 38 | 40 | 42 | 45 | 47 |
| **320** | 11 | 13 | 16 | 18 | 20 | 22 | 25 | 27 | 29 | 31 | 34 | 36 | 38 | 40 | 43 | 45 |
| **340** | 10 | 13 | 15 | 17 | 19 | 21 | 23 | 25 | 27 | 29 | 32 | 34 | 36 | 38 | 40 | 42 |
| **360** | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 | 30 | 32 | 34 | 36 | 38 | 40 |

Uwagi: wiersz A = 80 pt wynosi dokładnie L[pt]/3 (40, 48, 56 … 160 znaków). Wiersze 240, 250 odczytane z OCR niepewnie (uszkodzone cyfry); wartości w kolumnie 32–40 pc wiersza 250 uzupełnione.

## 2. Ciągi rozmiarów ze złotego podziału (B s. 157)

Tekst na s. 157 podaje: ciąg (b) = 6 · 10 · 16 · 26 · 42 · 68 · 110, ciąg (c) = 4 · 7 · 11 · 18 · 29 · 47 · 76, splot (a) i (b) jako (d) = 6 · 8 · 10 · 13 · 16 · 21 · 26 · 34 · 42 · 55 · 68 oraz zdanie, że ciąg (b) powstaje z (a) przez podwojenie. Stąd:

- **(a) = (b) / 2 = 3 · 5 · 8 · 13 · 21 · 34 · 55 · 89 …** (R; jest to ciąg Fibonacciego; w splocie (d) występują z niego już tylko wyrazy od 8 wzwyż, bo mniejsze rozmiary są bezużyteczne).

Nie wiem, czy w oryginale ciąg (a) zaczyna się od 3 i 5, czy od 8; wartości od 8 wzwyż są pewne.

## 3. Proporcje stron (B s. 148)

Proporcja zapisana jako 1 : x, gdzie x = wysokość / szerokość strony. Litery I (oraz l w tabeli kolumn) nie występują, tak jak w oryginale. Kolejność według x malejąco.

| 1 : x | Litera | Nazwa lub interwał | Pochodzenie |
|---:|:--:|---|:--:|
| 2.000 | A | Double Square (oktawa, 1 : 2) | O |
| 1.924 | B | Tall Octagon | O |
| 1.875 |  | 8 : 15, septyma wielka | R |
| 1.866 | C | Tall Hexagon | O |
| 1.848 | D | Octagon | O |
| 1.800 |  | 5 : 9, septyma mała (czysta) | W |
| 1.778 |  | 9 : 16, septyma mała | R |
| 1.732 | E | Hexagon, 1 : √3 | O |
| 1.701 | F | Tall Pentagon | O |
| 1.667 |  | 3 : 5, seksta wielka | R |
| 1.647 |  | Legal sheet (8½ × 14 cala) | R |
| 1.618 | G | Golden Section, 1 : φ | O |
| 1.600 |  | 5 : 8, seksta mała | R |
| 1.539 | H | Pentagon | O |
| 1.500 |  | 2 : 3, kwinta | R |
| 1.414 | Z | ISO, 1 : √2 (tryton równomiernie temperowany) | O |
| 1.400 |  | 5 : 7 | W |
| 1.376 | J | Short Pentagon | O |
| 1.333 |  | 3 : 4, kwarta | R |
| 1.307 | K | Tall Half Octagon | O |
| 1.294 |  | Letter sheet (8½ × 11 cala) | R |
| 1.250 |  | 4 : 5, tercja wielka | R |
| 1.207 | L | Half Octagon | O |
| 1.200 |  | 5 : 6, tercja mała | R |
| 1.176 | M | Truncated Pentagon | O |
| 1.167 |  | 6 : 7 | W |
| 1.156 |  | π : e (≈ ratio z natury) | W |
| 1.155 | N | Turned Hexagon | O |
| 1.125 |  | 8 : 9, sekunda wielka | R |
| 1.082 | O | Tall Cross Octagon | O |
| 1.067 |  | 15 : 16, sekunda mała | R |
| 1.051 | P | Turned Pentagon | O |
| 1.000 | Q | Square (pryma, 1 : 1) | O |
| 0.951 | R | Broad Pentagon | O |
| 0.924 | S | Broad Cross Octagon | O |
| 0.889 |  | 9 : 8, sekunda wielka (odwrócona) | R |
| 0.866 | T | Broad Hexagon | O |
| 0.829 | U | Full Cross Octagon | O |
| 0.800 |  | 5 : 4, tercja wielka (odwrócona) | R |
| 0.773 |  | Landscape letter (11 × 8½ cala, odwrócony) | R |

Kontrola z podpisami: litery A–U i Z zgadzają się z wartościami z podpisów na s. 150–153 (np. E 1,732; F 1,701; K 1,307; N 1,155; T 0,866; Z 1,414).

## 4. Proporcje kolumn (B s. 149)

| 1 : x | Litera | Nazwa lub interwał | Pochodzenie |
|---:|:--:|---|:--:|
| 4.000 | a | Quadruple Square (dwie oktawy) | O |
| 3.873 |  | 1 : √15 | R |
| 3.750 |  | 4 : 15, major 14th (czternasta wielka) | R |
| 3.600 |  | 5 : 18, minor 14th (czternasta mała) | R |
| 3.556 |  | 9 : 32 | R |
| 3.464 |  | 1 : √12 | R |
| 3.414 | b | Octagon Wing | O |
| 3.333 |  | 3 : 10, major 13th (tredecyma wielka) | R |
| 3.236 |  | 1 : 2φ | R |
| 3.200 |  | 5 : 16, minor 13th (tredecyma mała) | R |
| 3.162 |  | 1 : √10 | R |
| 3.142 |  | 1 : π | R |
| 3.078 | c | Double Pentagon (litera c niepewna) | W |
| 3.000 | d | Triple Square (duodecyma) | O |
| 2.993 | e | Wide Octagon Wing | O |
| 2.828 | z | Double ISO, 1 : 2√2 | O |
| 2.753 | f | Pentagon Wing | O |
| 2.718 |  | 1 : e | R |
| 2.667 |  | 3 : 8, undecyma | R |
| 2.646 |  | 1 : √7 | R |
| 2.618 | g | Extended Section, 1 : φ² | O |
| 2.613 | h | Tall Octagon Column | O |
| 2.514 | i | Mid Octagon Column | O |
| 2.500 |  | 2 : 5, major 10th (decyma wielka) | R |
| 2.414 | j | Short Octagon Column | O |
| 2.400 |  | 5 : 12, minor 10th (decyma mała) | R |
| 2.309 | k | Hexagon Wing | O |
| 2.252 | m | Double Truncated Pentagon | O |
| 2.250 |  | 4 : 9, major 9th (nona wielka) | R |
| 2.236 |  | 1 : √5 | R |
| 2.200 |  | 5 : 11 | R |
| 2.133 |  | 15 : 32, minor 9th (nona mała) | R |
| 2.000 | A | Double Square (oktawa) | O |

## 5. Czego nie odtworzono

- Kolumn „Sample sizes” (przykładowe formaty w calach i piccach) w obu tabelach proporcji.
- Wzorów na krzywe sklejane na s. 182 (nie dotyczą żadnej zasady z katalogu).
- Dokładnych cyfr kilku komórek tabeli z punktu 1, które oznaczono `*`.
