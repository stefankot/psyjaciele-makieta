# -*- coding: utf-8 -*-
"""Tekst demo (własny, wymyślony) i pomocnicze funkcje składu polskiego."""
import re

NB = ' '

def plfix(s):
    """Skład polski dla tekstu statycznego: spójniki jednoliterowe, półpauza, jednostki."""
    s = re.sub(r'(?<![\wąćęłńóśźż])([aiouwzAIOUWZ])[ ](?=\S)', lambda m: m.group(1) + NB, s)
    s = s.replace(' - ', NB + '– ').replace(' – ', NB + '– ')
    s = re.sub(r'(\d) (zł|mm|cm|km|kg|r\.|tys\.|m)\b', lambda m: m.group(1) + NB + m.group(2), s)
    s = re.sub(r'\b(str\.|rozdz\.|s\.|ul\.|nr|ok\.|np\.|tj\.) (?=\S)', lambda m: m.group(1) + NB, s)
    return s

def plfix_html(h):
    parts = re.split(r'(<[^>]+>|<!--.*?-->)', h, flags=re.S)
    return ''.join(p if (p.startswith('<')) else plfix(p) for p in parts)

def own(label, html):
    return '<!-- tekst własny: %s -->\n%s' % (label, html)

# --- tekst demo -------------------------------------------------------------
TA = ("Dobra strona zaczyna się od decyzji, których czytelnik nie zauważa. Nikt nie zatrzymuje się nad szerokością "
      "łamu ani nad odstępem między wierszami, a jednak to one decydują, czy długi tekst da się przeczytać do końca. "
      "Dawny zecer wiedział o tym z doświadczenia: zbyt ciasna interlinia męczyła oczy po kilku stronach, a zbyt "
      "szeroka miara gubiła wzrok w drodze do następnego wiersza. Dzisiejsza przeglądarka wykonuje tę pracę za nas, "
      "ale tylko wtedy, gdy ją o to poprosimy.")

TB = ("Pracownia, o której tu mowa, istniała naprawdę tylko w wyobraźni autora. Zatrudniała trzech zecerów i jedną "
      "korektorkę, drukowała około 40 tytułów rocznie, a jej katalog z 1998 roku liczył 144 strony. Cena egzemplarza "
      "wynosiła 12,50 zł, nakład dochodził do 2 400 sztuk. Nikt nie liczył, ile godzin kosztowało dopasowanie "
      "jednego wiersza, ale wszyscy zgadzali się, że warto.")

TC = ("Rzecz w tym, że czytelnik nie czyta liter, tylko rytm. Gdy wiersz kończy się tam, gdzie kończy się myśl, oko "
      "odpoczywa. Gdy łamie się w pół słowa albo zostawia na końcu samotny przyimek, odpoczynek zamienia się w potknięcie.")

QUOTE = "„Typografia istnieje po to, żeby tekst dało się czytać, a nie po to, żeby ją podziwiano.”"
QUOTE_SRC = "z notatek pracowni"

VERSE = ["Ciche są litery w skrzyni,", "nim je ktoś ułoży w słowo;", "każda ma swoje miejsce", "i żadna nie mówi pierwsza."]

LIST = ["Wybierz krój do tekstu, nie do tematu.", "Ustal miarę i interlinię.", "Dopiero potem dobieraj nagłówki."]

# surowy tekst do punktów kategorii 2 (celowo z błędami składu)
RAW = {
 'P2-01': "W tej pracowni a także w sąsiedniej drukarni, o świcie i o zmierzchu, u zecera w skrzyni z ołowiu leżał zapas czcionek. W końcu nikt nie zapytał, a ile kosztuje wiersz.",
 'P2-02': "Korektorka powiedziała: \"Nie ma reguł bez wyjątków\", a zecer dodał: \"Każdy wyjątek to \"reguła\" pisana innym ołówkiem\". Mówili też o rock'n'rollu i o panu O'Brienie.",
 'P2-03': "Pracownia - choć niewielka - drukowała dużo. Autor -- co ciekawe -- nie lubił kursywy, a redaktor — z wzajemnością — nie lubił autora.",
 'P2-04': "Zob. str. 12-18, lata 1998-2004, godz. 9:00-17:30 oraz 2026-10-11 (data ISO), tel. 22-555-12-34, kod 00-950.",
 'P2-05': "Czekali... i czekali.... Koniec!!! Naprawdę?? Tak... Nikt nie wiedział, co dalej...",
 'P2-06': "Format 10 x 5 cm, tolerancja 50 +- 2 mm, warunek a != b, 1/2 szklanki mąki, 3/4 nakładu, temperatura -5 stopni.",
 'P2-07': "Temperatura 20 C, wzrost 5'2\", (c) 2026 Pracownia, nazwa(tm), znak towarowy(r).",
 'P2-08': "Zob. str. 12, rozdz. 5, ul. Kwiatowa 7, długość 6,2 mm, cena 12 zł, w 2026 r., nakład 2,4 tys. egz., § 5 ust. 2.",
 'P2-09': "Nakład wyniósł 1250000 egzemplarzy, budżet 12345678 zł, tel. 225551234 lub 601234567, kod 00-950.",
 'P2-10': "Według ONZ i UE oraz NATO, a także PKP i PAN, UNESCO wspiera nie tylko kulturę. Rozmawiali o USA, UK i PL.",
 'P2-11': "J. R. R. Tolkien, W. B. Yeats i M. Konopnicka pisali inaczej niż J. K. Rowling.",
 'P2-12': "Pracownia, o której tu mowa, istniała naprawdę tylko w wyobraźni autora i nikt jej nie zamknął, bo nikt jej nie otworzył, a mimo to",
 'P2-13': "Nieprzejednany przedstawiciel rozmaitości konstytucyjnych bezpardonowo odrzucił jednoznacznie sformułowaną propozycję, a pracownia zecerska przystąpiła do sporządzania sprawozdania.",
 'P2-14': TA,
 'P2-23': "Zecer  ,który pracował  tu od  lat ,  nie lubił podwójnych  spacji .  Tabulator\tteż mu przeszkadzał ( jak i spacja przed przecinkiem )  oraz  zbędne spacje .",
}
