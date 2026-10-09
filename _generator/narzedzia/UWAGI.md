<!-- generated: psyjaciele-podstrony -->
# Zaznaczanie elementów i komentarze

**Na podstronach** (`podstrony/…`): dopisz `?uwagi=1` do adresu, np.
`http://127.0.0.1:8765/podstrony/zespol/index.html?uwagi=1`. Panel zostaje włączony w tej karcie przeglądarki, dopóki nie wejdziesz na `?uwagi=0` albo nie klikniesz „Zamknij”.

**Na stronie głównej** (i wszędzie indziej na tym serwerze): utwórz zakładkę w przeglądarce, a w polu adresu wklej:

```
javascript:(function(){var s=document.createElement('script');s.src='http://127.0.0.1:8765/podstrony/_narzedzia/uwagi.js';document.body.appendChild(s)})()
```

**Użycie:** „Zaznacz element” → klikaj element na stronie (różowa ramka pokazuje, co wybierzesz) → wpisz komentarz → „Zapisz”. Numerowane pinezki pokazują zapisane uwagi (klik = edycja/usunięcie). „Kopiuj wszystko” kopiuje listę w Markdown (strona, selektor CSS, sekcja, fragment tekstu, szerokość okna, komentarz) — wklej ją do rozmowy. Uwagi zapisują się w przeglądarce (localStorage), więc przeżywają odświeżenie.
Szerokość okna jest w uwagach — jeśli poprawka dotyczy układu mobilnego, zmniejsz okno przed zaznaczeniem.
