# Psyjaciele — HTML i WordPress z jednego źródła

Ten projekt obsługuje wyłącznie **https://www.psyjacielevet.pl/mystaging02** i treść strony głównej **ID 14**. Motyw potomny: `psyjaciele-staging`, rodzic: Twenty Twenty-Five. Globalne style są dostępne także na innych podstronach stagingu. Produkcja nie jest celem synchronizacji.

## Gdzie wprowadzać zmiany

- **Treść, kolejność sekcji, linki, nagłówek i stopka:** `../index-min.html`. To jedyne źródło treści home.
- **Układ i animacje:** lokalne CSS i JS wskazane w `index-min.html`. Kolejność ich ładowania jest odczytywana z HTML.
- **Wspólna paleta, fonty, typografia edytora, szerokości i odstępy:** `theme-source/theme.json`. Lokalny `../design-tokens.css` jest generowany z tego pliku. Kolory komponentów używają tych samych zmiennych palety co WordPress.
- **Wyjątki dotyczące opakowań bloków WordPressa:** `theme-source/assets/css/wordpress.css` i `theme-source/functions.php`. Nie umieszczać tutaj kopii treści strony.
- **Zdjęcia:** lokalny katalog `../assets/`, przypisania WordPress w `media-map.json`. Fonty i pozostałe zasoby wersjonowane: `remote-assets.json`.

Nie edytować `../../wordpress-staging/generated/`: wynik zostanie odtworzony przy następnym zbudowaniu. Nie zmieniać osobno wygenerowanych wzorców, nagłówka ani stopki.

## Najprostsze przygotowanie aktualizacji

Dwuklik na **Synchronizuj.command** przygotowuje paczkę i sprawdza ją. Można też uruchomić w katalogu `makieta`:

```sh
python3 wordpress/sync.py check
python3 -m unittest discover -s wordpress -p test_sync.py
python3 wordpress/sync.py build
```

To są polecenia lokalne. **Nie wysyłają plików, nie zmieniają WordPressa i nie publikują strony.** Nie wymagają dodatkowych bibliotek; potrzebny Python 3.9 lub nowszy.

Wynik: `../../wordpress-staging/generated/`:

| Plik | Zastosowanie |
| --- | --- |
| `theme/` | kompletny motyw potomny, gotowy do porównania z WP |
| `psyjaciele-staging.zip` | powtarzalna paczka motywu |
| `home-content.html` | treść home jako natywne bloki |
| `home-update.json` | ładunek aktualizujący tylko treść strony 14 |
| `sync-plan.json` | lista zmienionych plików, wymagane hashe i kolejność działań |
| `build-manifest.json` | hashe nowej wersji |
| `report.json` | sekcje, bloki, obrazy i kolejność zasobów |

## Synchronizacja przez WPVibe

1. Potwierdzić przez `site_info` adres **mystaging02**, aktywny motyw, jego rodzica i istniejący szkic. Gdy ktoś zmienił motyw, zatrzymać aktualizację i uzgodnić źródła.
2. Odczytać z WPVibe pliki wymienione w `sync-plan.json` i surową treść strony 14 przez REST. Porównać z `sync-state.json`. Każda niezależna zmiana w WP wymaga połączenia zmian przed synchronizacją. Nie aktualizować bazowego stanu po samym zbudowaniu paczki.
3. Wysłać przez `write_file`/`edit_file` **tylko różniące się pliki do szkicu**, najpierw zasoby, konfigurację i `content/home.html`, następnie części i wzorce, na końcu `functions.php`. Nie usuwać plików występujących tylko na serwerze.
4. Obejrzeć podgląd szkicu. W szkicu `content/home.html` zastępuje renderowaną treść home, dzięki czemu podgląd nowego HTML nie wymaga zmiany opublikowanej strony 14. Natywna kontrola Gutenberg: dopisać `&psy_validate=1` do adresu podglądu. Raport pojawia się na ekranie; niczego nie zapisuje.
5. **Po osobnym zatwierdzeniu publikacji** opublikować szkic motywu na mystaging02. Ponownie sprawdzić hash surowej treści strony 14 i dopiero wtedy przesłać `home-update.json` do `PUT /wp/v2/pages/14`. Nie przesyłać statusu, tytułu ani pozostałych stron. Przejście jest zgodne ze starymi identyfikatorami konfiguracji.
6. Wyczyścić cache, sprawdzić zwykły adres stagingu na komputerze i telefonie oraz zapisać nowy `sync-state.json` z rzeczywistymi hashami plików i treści home. Zachować poprzednią treść strony i pliki w `snapshots/`.

Plan względem świeżego zestawu hashy:

```sh
python3 wordpress/sync.py verify-remote --snapshot fresh-remote.json
python3 wordpress/sync.py plan --snapshot fresh-remote.json
```

Format snapshotu jest taki jak `sync-state.json`: `site_url`, `theme_slug`, `files` (ścieżka → SHA-256), `home_sha256`. Dla tekstu hashe ignorują wyłącznie końcowe znaki nowej linii; obrazy porównywane są bajtowo. Snapshot trzeba pozyskać przez dostępne narzędzia WPVibe; generator nie zawiera poświadczeń ani własnego klienta sieciowego.

## Co zabezpiecza powtarzalność

Konwersja nie zapisuje niczego przy imporcie. Identyfikatory konfiguracji zależą od zawartości, a nie numeru elementu; dodanie sekcji lub zdjęcia nie przesuwa ustawień innych elementów. Wszystkie 12 sekcji powstają równocześnie jako treść home i wzorce do ponownego użycia. Teksty, nagłówki, listy, cytaty, obrazy i przyciski pozostają standardowymi blokami; SVG i funkcjonalne linki portretów pozostają małymi fragmentami HTML.

Zmiana lokalnego obrazu blokuje kompilację, dopóki nowa wersja nie zostanie wysłana do WP i jej URL/hash zapisany w mapie. Nowe zasoby też wymagają rejestracji. Linki prowadzące do własnej witryny są kierowane na staging; rezerwacja i media społecznościowe zachowują adresy zewnętrzne.

Wszystkie aktualizacje motywu nadrzędnego pozostają możliwe. Podstrony korzystające z całych sekcji powinny mieć szablon **Psyjaciele — uniwersalne sekcje**. Zmiany wykonane ręcznie w WP nie są automatycznie przenoszone do lokalnego HTML; zostaną wykryte jako konflikt podczas kolejnej synchronizacji.

## Stan i ograniczenia

7.10.2026: lokalny generator i szkic są przygotowane do ponownego sprawdzenia; nowa wersja nie została opublikowana. Stan `sync-state.json` opisuje dotychczasową opublikowaną treść i pliki odczytane przed aktualizacją szkicu. Przy ponownej aktualizacji tego samego szkicu użyć dodatkowego `draft-state.json` opisującego już wysłane pliki.

Dawne `build.py`, `convert.py` i `prepare_globals.py` w katalogu migracji są bezpiecznymi przekierowaniami do tego generatora. Ich historyczne wersje leżą w `legacy-tools-archive` i są wyłącznie materiałem archiwalnym. Poprzednia paczka i zdjęcia kontrolne pozostały zachowane.
