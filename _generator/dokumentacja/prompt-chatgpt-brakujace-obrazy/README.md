# Prompt dla ChatGPT: nowe zdjęcia całej strony (45 zdjęć, bez ilustracji)

Pomysł: seria wygląda jak „rolka zdjęć z telefonu osoby pracującej w przychodni” (przypadkowe, naturalne, lekko krzywe kadry, zwierzęta w trakcie ruchu, bez twarzy ludzi i bez napisów), bez żadnego filtra (decyzja właściciela 9.10.2026: filtr „Gocław Film” wyglądał sztampowo i został zdjęty ze wszystkich zdjęć). Kolory każdego zdjęcia są dobrane do tła sekcji, w której leży (SALMON, PEACH, SAGE, MIST, IVORY).

Zawartość folderu:
- `PROMPT.txt` — samowystarczalny prompt po angielsku (generator obrazów najlepiej rozumie angielski): koncepcja, filtr, tabela kolorów sekcji, zasady kadrowania i zakazy, sposób pracy oraz 45 pozycji pogrupowanych stronami (plik, kształt ramki na stronie, płótno, paleta sekcji, sekcja w której zdjęcie leży, pomysł na kadr).
- `referencje/PALETA-I-KADROWANIE.png` — jedyny załącznik: kolory sekcji z kodami, strefy bezpieczne kadrowania (3:2, pas 21:9, pion 4:5), (wzmianka o filtrze na obrazku jest nieaktualna — filtra nie stosujemy).

Stare zdjęcia nie są referencją (celowo): to wszystko zdjęcia z ChatGPT, które zastępujemy. Ilustracje (czarna kreska) zostają bez zmian i nie ma ich w prompcie; brakująca ilustracja `chir-03-opieka-po.png` (chirurgia) pozostaje do zrobienia osobno.

## Jak użyć
1. Nowy czat w ChatGPT z generowaniem obrazów. Wklej całą zawartość `PROMPT.txt`, dołącz `PALETA-I-KADROWANIE.png`.
2. ChatGPT odpowiada pięcioma linijkami (jak rozumie styl) i generuje zdjęcie 1. Sprawdź: brak twarzy ludzi, brak czytelnych napisów, naturalne łapy i sierść, kolory pasujące do palety sekcji, w pasach 21:9 ważne rzeczy w środkowym pasie. Odpisz `next` albo `redo N: …`.
3. Po ostatnim zdjęciu każdej strony ChatGPT wypisuje listę plików. Jeśli czat robi się zbyt długi, otwórz nowy, wklej prompt ponownie i dopisz na końcu: `START FROM ITEM 21` (numer, od którego kontynuujesz).
4. Zapisuj każdy obraz pod nazwą z promptu (ChatGPT podaje ją pod obrazem).

## Gdzie zapisać pliki
Do `assets/podstrony/<strona>/` pod **tymi samymi nazwami** co dotychczas (nadpisujesz stare):

| prefiks pliku | katalog w `assets/podstrony/` |
|---|---|
| `chir-` | `chirurgia-weterynaryjna-tkanek-miekkich/` |
| `interna-` | `choroby-wewnetrzne-u-psow-i-kotow/` |
| `czip-` | `czipowanie-psow-i-kotow/` |
| `derm-` | `dermatologia-weterynaryjna/` |
| `lab-` | `diagnostyka-laboratoryjna-weterynaryjna/` |
| `usg-` | `diagnostyka-obrazowa-psow-i-kotow/` |
| `kard-` | `kardiologia-weterynaryjna/` |
| `nefr-` | `nefrologia-weterynaryjna/` |
| `oko-` | `okulistyka-weterynaryjna/` |
| `cis-` | `pomiar-cisnienia-psow-i-kotow/` |
| `stom-` | `stomatologia-weterynaryjna/` |
| `szcz-` | `szczepienia-oraz-profilaktyka-przeciwpasozytnicza/` |
| `uro-` | `urologia-weterynaryjna/` |
| `pasz-` | `wystawianie-paszportow-psom-i-kotom/` |
| `uslugi-` | `uslugi-weterynaryjne/` |

Plik `derm-02-pas-skora-siersc-v2.jpg` ma w nazwie `-v2` (tak go oczekuje strona).

Potem z katalogu makiety:

```
python3 _generator/narzedzia/avif.py     # konwersja wszystkich użytych zdjęć do AVIF (jakość 60); nadpisuje stare .avif
python3 _generator/narzedzia/build.py    # przebudowa podstron
```

Na stronie odśwież twardo (Cmd+Shift+R), bo przeglądarka trzyma stare `.avif` pod tą samą nazwą.

## Czego prompt nie obejmuje
- Zdjęć na stronie głównej (zespół, założycielki, kolaż pacjentów, pies i kot w sekcjach rezerwacji i social) — to osobne kompozycje (wycinanki, kolaż); jeśli mają być wymienione, trzeba je opisać osobno.
- Ilustracji.


## Stan (9.10.2026)
Wszystkie 45 zdjęć wyrenderowano connectorem Nano Banana (surowe pliki: `_generator/wyniki/_nowe-zdjecia/raw/`), wstawiono przez `_generator/narzedzia/zdjecia_wstaw.py` (kadrowanie do slotu, domyślnie BEZ filtra; `--grade` włącza stary filtr). Kolaż pacjentów w banerze „Praca” zostaje oryginalny (kopie w `_archiwum/zdjecia-przed-wymiana-2026-10-09/join-pacjenci/`).
