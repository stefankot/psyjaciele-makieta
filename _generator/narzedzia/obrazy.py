# generated: psyjaciele-podstrony
"""obrazy.py — rejestr placeholderów obrazów (§9, §10A.2). Jedyne źródło prawdy dla _obrazy.json/.md i OBRAZY-PROMPTY.md.

Wpis: id → kind, ratio (CSS, np. '3/2'), title (podpis ramki, PL), opis (co ma być na obrazie), alt, zrodlo, subject (EN, do promptu).
Nie zawiera żadnych zdań treści medycznej — tylko opisy obrazów dla autora.
"""

SLUG = {
    'uslugi': 'uslugi-weterynaryjne', 'zespol': 'zespol', 'interna': 'choroby-wewnetrzne-u-psow-i-kotow',
    'lab': 'diagnostyka-laboratoryjna-weterynaryjna', 'szcz': 'szczepienia-oraz-profilaktyka-przeciwpasozytnicza',
    'chir': 'chirurgia-weterynaryjna-tkanek-miekkich', 'kard': 'kardiologia-weterynaryjna',
    'usg': 'diagnostyka-obrazowa-psow-i-kotow', 'oko': 'okulistyka-weterynaryjna', 'derm': 'dermatologia-weterynaryjna',
    'stom': 'stomatologia-weterynaryjna', 'nefr': 'nefrologia-weterynaryjna', 'uro': 'urologia-weterynaryjna',
    'cis': 'pomiar-cisnienia-psow-i-kotow', 'pasz': 'wystawianie-paszportow-psom-i-kotom', 'czip': 'czipowanie-psow-i-kotow',
}

REAL = 'prawdziwe zdjęcie z przychodni (za zgodą opiekunów)'
GEN = 'generowanie (image_gen) lub zdjęcie stockowe'
DRAW = 'generowanie (image_gen), rysunek liniowy'

# (id, kind, ratio, tytuł PL, opis PL, alt PL, źródło, subject EN)
_ROWS = [
    # --- hub
    ('uslugi-01-recepcja', 'foto', '3/2', 'Recepcja przychodni', 'Wnętrze recepcji lub poczekalni: lada, krzesła, kocyk dla zwierząt; bez ludzi w kadrze.', 'Recepcja przychodni weterynaryjnej Psyjaciele', REAL, 'the reception area of a small veterinary clinic, empty counter, a chair and a folded blanket'),
    ('uslugi-02-gabinet', 'pas', '21/9', 'Gabinet zabiegowy', 'Szeroki kadr pustego gabinetu: stół, lampa, szafki. Jasne, spokojne światło.', 'Gabinet przychodni weterynaryjnej', REAL, 'a bright empty veterinary examination room, steel table, lamp and cabinets, wide view'),
    ('uslugi-03-mozaika-a', 'foto', '4/5', 'Pies na stole badań', 'Spokojny pies na stole, dłoń lekarki na jego grzbiecie; bez twarzy ludzi.', 'Pies spokojnie czeka na badanie', REAL, 'a calm medium-sized dog standing on an examination table, a veterinarian\'s hand resting on its back, no faces visible'),
    ('uslugi-03-mozaika-b', 'foto', '3/2', 'Kot w transporterze', 'Kot wyglądający z otwartego transportera z kocykiem.', 'Kot w transporterze w poczekalni', GEN, 'a cat peeking out of an open carrier lined with a blanket'),
    ('uslugi-03-mozaika-c', 'foto', '3/2', 'Dłonie przy książeczce zdrowia', 'Dłonie opiekuna trzymające książeczkę zdrowia zwierzęcia.', 'Książeczka zdrowia w dłoniach opiekuna', GEN, 'hands holding a pet health booklet over a table, no faces'),
    ('uslugi-04-kot-pies', 'wycinek', '1/1', 'Kot i pies obok siebie', 'Wycięty kot i pies siedzące obok siebie, białe tło, czarna kreska.', 'Kot i pies siedzą obok siebie', GEN, 'a calm grey cat and a small dog sitting side by side, seen from the front'),
    # --- zespół
    ('zespol-01-zespol-grupowe', 'pas', '21/9', 'Zespół przychodni', 'Zdjęcie grupowe lekarek w gabinecie lub przed budynkiem (prawdziwe, za zgodą).', 'Lekarki weterynarii przychodni Psyjaciele', REAL, 'a group of seven women veterinarians in white coats standing together in a bright clinic, wide group portrait'),
    ('zespol-02-gabinet', 'pas', '21/9', 'Gabinet', 'Wnętrze gabinetu przy oknie, bez ludzi.', 'Gabinet przychodni Psyjaciele', REAL, 'a quiet veterinary consulting room with a desk and a window'),
    ('zespol-03-atmosfera', 'foto', '21/9', 'Pies w gabinecie', 'Spokojny pies przy nogach lekarki; kadr bez twarzy.', 'Pies w przychodni', GEN, 'a dog sitting calmly next to a veterinarian\'s legs in a clinic, no faces, wide 21:9 composition'),
    # --- interna
    ('interna-01-badanie', 'foto', '4/5', 'Badanie psa stetoskopem', 'Lekarka osłuchuje spokojnego psa; kadr bez twarzy.', 'Lekarka osłuchuje psa', REAL, 'a veterinarian listening to a calm dog\'s chest with a stethoscope, face not visible'),
    ('interna-02-schemat-ukladow', 'diagram', '4/3', 'Schemat układów narządowych', 'Uproszczony zarys psa z naniesionymi układami (bez opisów).', 'Schemat układów narządowych psa', DRAW, 'simplified outline of a dog with faint organ systems indicated by line shapes, unlabeled'),
    ('interna-03-pas-gabinet', 'pas', '21/9', 'Gabinet internisty', 'Szeroki pas: stół, waga, szafka z dokumentami.', 'Gabinet konsultacyjny', REAL, 'a wide view of a veterinary consulting room with a table, scale and cabinet'),
    ('interna-04-kontrola', 'foto', '3/2', 'Kontrola kota', 'Kot na kolanach opiekuna podczas kontroli.', 'Kot podczas kontroli', GEN, 'a cat sitting on an owner\'s lap during a routine check, no faces'),
    # --- laboratorium
    ('lab-01-analizator', 'foto', '3/2', 'Analizator w gabinecie', 'Analizator laboratoryjny na blacie; bez wyświetlanych wyników.', 'Analizator laboratoryjny w przychodni', REAL, 'a tabletop laboratory analyzer on a clean counter, screen turned off'),
    ('lab-02-probki', 'wycinek', '1/1', 'Probówki z próbkami', 'Statyw z probówkami (bez etykiet z tekstem), białe tło, czarna kreska.', 'Probówki w statywie', GEN, 'a small rack with empty laboratory sample tubes, labels blank'),
    ('lab-03-pas-laboratorium', 'pas', '21/9', 'Stanowisko laboratoryjne', 'Pas: blat z mikroskopem i szkiełkami.', 'Stanowisko laboratoryjne w przychodni', REAL, 'a wide laboratory counter with a microscope and glass slides'),
    # --- szczepienia
    ('szcz-01-szczepienie', 'foto', '4/5', 'Szczepienie psa', 'Dłonie lekarki przygotowujące szczepienie, pies w tle; bez widocznej igły.', 'Szczepienie psa', REAL, 'gloved hands of a veterinarian preparing a vaccination for a calm dog in the background, no needle visible'),
    ('szcz-02-ksiazeczka', 'wycinek', '1/1', 'Książeczka szczepień', 'Zamknięta książeczka zdrowia zwierzęcia, białe tło, czarna kreska.', 'Książeczka szczepień zwierzęcia', GEN, 'a closed pet vaccination booklet, front cover with no text'),
    ('szcz-03-kalendarz', 'diagram', '4/3', 'Schemat osi czasu', 'Prosta pozioma oś z kilkoma punktami (bez dat i opisów).', 'Oś czasu szczepień', DRAW, 'a simple horizontal timeline with five small markers, no dates'),
    ('szcz-04-pas-pies-kot', 'pas', '21/9', 'Pies i kot', 'Szeroki pas: pies i kot siedzące obok siebie.', 'Pies i kot obok siebie', GEN, 'a dog and a cat sitting side by side, wide banner composition'),
    # --- chirurgia
    ('chir-01-sala-zabiegowa', 'pas', '21/9', 'Sala zabiegowa', 'Pusta, jasna sala zabiegowa; bez widocznych narzędzi w użyciu.', 'Sala zabiegowa przychodni', REAL, 'a bright empty surgical room with a table and lamp, no instruments in use'),
    ('chir-02-konsultacja', 'foto', '3/2', 'Konsultacja przed zabiegiem', 'Lekarka rozmawia z opiekunem przy psie; bez twarzy.', 'Konsultacja przed zabiegiem', REAL, 'a veterinarian talking with a pet owner next to a dog, faces not visible'),
    ('chir-03-opieka-po', 'foto', '4/5', 'Pies w kołnierzu', 'Pies w miękkim kołnierzu leżący na posłaniu.', 'Pies w kołnierzu po zabiegu', GEN, 'a dog resting on a bed wearing a soft recovery collar'),
    ('chir-04-rana-schemat', 'diagram', '4/3', 'Schemat opatrunku', 'Ogólny schemat linii opatrunku na łapie (bez ran).', 'Schemat opatrunku', DRAW, 'simplified line drawing of a dog\'s leg with a bandage wrap, no wound shown'),
    # --- kardiologia
    ('kard-01-serce-diagram', 'diagram', '4/3', 'Schemat budowy serca', 'Uproszczony przekrój czterech jam serca psa ze strzałkami przepływu krwi.', 'Schemat budowy serca psa', DRAW, 'simplified four-chamber heart of a dog in cross-section with unlabeled arrows showing blood flow'),
    ('kard-02-echo', 'foto', '3/2', 'Badanie echo serca', 'Głowica USG przy klatce piersiowej psa; ekran wyłączony lub poza kadrem.', 'Badanie echokardiograficzne psa', REAL, 'an ultrasound probe held against a calm dog\'s chest, screen not visible'),
    ('kard-03-ekg', 'wycinek', '1/1', 'Elektrody EKG', 'Zestaw elektrod EKG z kablami, białe tło, czarna kreska.', 'Elektrody EKG', GEN, 'a set of ECG electrode clips with cables, neatly arranged'),
    ('kard-04-pies-kot-a', 'foto', '4/5', 'Pies w gabinecie', 'Spokojny pies siedzący w gabinecie.', 'Pies w gabinecie kardiologicznym', GEN, 'a calm dog sitting in a veterinary room'),
    ('kard-04-pies-kot-b', 'foto', '3/2', 'Kot na stole', 'Kot spokojnie siedzący na stole badań.', 'Kot na stole badań', GEN, 'a cat sitting calmly on an examination table'),
    ('kard-04-pies-kot-c', 'foto', '3/2', 'Dłoń na grzbiecie', 'Dłoń lekarki głaszcząca zwierzę.', 'Dłoń lekarki na grzbiecie zwierzęcia', GEN, 'a veterinarian\'s hand gently stroking a pet\'s back'),
    ('kard-05-pas', 'pas', '21/9', 'Gabinet kardiologiczny', 'Szeroki pas: stół i aparat USG.', 'Gabinet kardiologiczny', REAL, 'wide view of a veterinary room with an examination table and an ultrasound machine'),
    # --- USG
    ('usg-01-aparat', 'foto', '4/5', 'Aparat USG', 'Aparat USG w gabinecie; ekran wyłączony.', 'Aparat USG w przychodni', REAL, 'a veterinary ultrasound machine in a consulting room, screen off'),
    ('usg-02-mapa-ciala', 'diagram', '4/3', 'Mapa ciała do USG', 'Zarys psa z bryłami okien badania (bez opisów).', 'Schemat okien badania USG', DRAW, 'simplified outline of a dog\'s body with soft rounded zones marking abdominal windows, unlabeled'),
    ('usg-03-badanie', 'foto', '3/2', 'Badanie USG jamy brzusznej', 'Głowica na wygolonym brzuchu psa; bez twarzy.', 'Badanie USG psa', REAL, 'an ultrasound probe on the shaved belly of a calm dog lying on its back, faces not visible'),
    ('usg-04-pas', 'pas', '21/9', 'Gabinet USG', 'Szeroki pas: stół badań i przyciemnione światło.', 'Gabinet badań USG', REAL, 'wide view of a dim ultrasound room with a table and machine'),
    # --- okulistyka
    ('oko-01-oko-diagram', 'diagram', '4/3', 'Schemat budowy oka', 'Uproszczony przekrój oka psa (bez opisów).', 'Schemat budowy oka psa', DRAW, 'simplified cross-section of a dog\'s eye showing cornea, lens and retina as plain shapes'),
    ('oko-02-badanie-lampa', 'foto', '3/2', 'Badanie lampą szczelinową', 'Lampa szczelinowa przy głowie psa; kadr bez twarzy ludzi.', 'Badanie oka lampą szczelinową', REAL, 'a slit lamp examination of a dog\'s eye, human faces not visible'),
    ('oko-03-oko-pies', 'foto', '4/5', 'Portret psa', 'Portret psa z widocznymi oczami, spokojny wyraz.', 'Portret psa z bliska', GEN, 'a close portrait of a calm dog looking toward the camera'),
    ('oko-04-pas-gabinet', 'pas', '21/9', 'Gabinet okulistyczny', 'Szeroki pas: gabinet z lampą szczelinową.', 'Gabinet okulistyczny', REAL, 'wide view of a veterinary room with a slit lamp on a table'),
    # --- dermatologia
    ('derm-01-badanie-skory', 'foto', '4/5', 'Badanie skóry psa', 'Dłonie rozchylające sierść na grzbiecie psa; bez widocznych zmian chorobowych.', 'Badanie skóry psa', REAL, 'hands parting the fur on a dog\'s back to look at healthy-looking skin, no lesions visible'),
    ('derm-02-pas-skora-siersc', 'pas', '21/9', 'Sierść z bliska', 'Szeroki makro-kadr sierści psa.', 'Sierść psa z bliska', GEN, 'wide macro view of a dog\'s fur texture'),
    ('derm-03-cytologia', 'foto', '3/2', 'Mikroskop i szkiełka', 'Mikroskop i szkiełka podstawowe na blacie.', 'Mikroskop i szkiełka', REAL, 'a microscope and glass slides on a clean counter'),
    ('derm-04-pielegnacja', 'wycinek', '1/1', 'Szczotka do sierści', 'Szczotka do sierści na białym tle, czarna kreska.', 'Szczotka do sierści', GEN, 'a pet grooming brush, simple object'),
    # --- stomatologia
    ('stom-01-jama-ustna-diagram', 'diagram', '4/3', 'Schemat zęba i dziąsła', 'Uproszczony przekrój zęba w dziąśle (bez opisów).', 'Schemat budowy zęba psa', DRAW, 'simplified cross-section of a dog tooth in the gum, unlabeled'),
    ('stom-02-zabieg', 'foto', '3/2', 'Stanowisko stomatologiczne', 'Stanowisko stomatologiczne w gabinecie; bez zwierzęcia.', 'Stanowisko stomatologiczne', REAL, 'a veterinary dental station with instruments laid out, no animal'),
    ('stom-03-mozaika-a', 'foto', '4/5', 'Pies z zabawką', 'Pies trzymający gumową zabawkę w pysku.', 'Pies z gumową zabawką', GEN, 'a dog holding a rubber toy in its mouth'),
    ('stom-03-mozaika-b', 'foto', '3/2', 'Szczoteczka', 'Szczoteczka i pasta dla zwierząt.', 'Szczoteczka do zębów dla zwierząt', GEN, 'a pet toothbrush and toothpaste on a plain surface'),
    ('stom-03-mozaika-c', 'foto', '3/2', 'Kot u lekarki', 'Kot siedzący spokojnie u lekarki.', 'Kot podczas wizyty', GEN, 'a cat sitting calmly with a veterinarian, face not visible'),
    ('stom-04-pies-szczotka', 'wycinek', '1/1', 'Pies ze szczoteczką', 'Siedzący pies obok szczoteczki.', 'Pies obok szczoteczki', GEN, 'a seated dog next to a toothbrush'),
    # --- nefrologia
    ('nefr-01-nerki-diagram', 'diagram', '4/3', 'Schemat nerek', 'Uproszczony schemat nerek i moczowodów (bez opisów).', 'Schemat nerek', DRAW, 'simplified line drawing of two kidneys with ureters, unlabeled'),
    ('nefr-02-kot-pije', 'foto', '4/5', 'Kot przy misce', 'Kot pijący wodę z miski.', 'Kot pije wodę', GEN, 'a cat drinking water from a bowl'),
    ('nefr-03-pas', 'pas', '21/9', 'Gabinet', 'Szeroki pas: gabinet konsultacyjny.', 'Gabinet konsultacyjny', REAL, 'wide view of a quiet veterinary consulting room'),
    ('nefr-04-badanie-krwi', 'foto', '3/2', 'Pobranie krwi', 'Dłonie przy łapie psa, probówka w tle; bez widocznej igły.', 'Pobranie krwi od psa', REAL, 'gloved hands holding a dog\'s paw with a sample tube nearby, no needle visible'),
    # --- urologia
    ('uro-01-uklad-moczowy-diagram', 'diagram', '4/3', 'Schemat układu moczowego', 'Uproszczony schemat dolnych dróg moczowych (bez opisów).', 'Schemat układu moczowego', DRAW, 'simplified line drawing of the lower urinary tract, unlabeled'),
    ('uro-02-kot-kuweta', 'foto', '3/2', 'Kot przy kuwecie', 'Czysta kuweta i kot obok.', 'Kot przy kuwecie', GEN, 'a cat next to a clean litter box'),
    ('uro-03-pas', 'pas', '21/9', 'Gabinet', 'Szeroki pas: gabinet konsultacyjny.', 'Gabinet konsultacyjny', REAL, 'wide view of a quiet veterinary consulting room'),
    ('uro-04-pies-spacer', 'wycinek', '1/1', 'Pies na spacerze', 'Pies na smyczy, białe tło, czarna kreska.', 'Pies na smyczy', GEN, 'a dog standing on a leash, side view'),
    # --- ciśnienie
    ('cis-01-mankiet-diagram', 'diagram', '4/3', 'Schemat mankietu', 'Łapa z założonym mankietem (bez opisów).', 'Schemat założenia mankietu', DRAW, 'simplified drawing of a dog\'s leg with a blood pressure cuff, unlabeled'),
    ('cis-02-pomiar-kot', 'foto', '4/5', 'Pomiar u kota', 'Kot z mankietem na łapie, trzymany delikatnie; bez twarzy.', 'Pomiar ciśnienia u kota', REAL, 'a cat with a small cuff on its paw held gently, faces not visible'),
    ('cis-03-pas-gabinet', 'pas', '21/9', 'Cichy gabinet', 'Szeroki pas: spokojny gabinet.', 'Spokojny gabinet', REAL, 'wide view of a quiet veterinary room with a small table'),
    ('cis-04-pomiar-pies', 'foto', '3/2', 'Pomiar u psa', 'Pies leżący spokojnie z mankietem; bez twarzy.', 'Pomiar ciśnienia u psa', REAL, 'a dog lying calmly with a cuff on its leg, faces not visible'),
    # --- paszporty
    ('pasz-01-paszport', 'wycinek', '1/1', 'Paszport zwierzęcia', 'Zamknięty paszport dla zwierzęcia (okładka bez tekstu), białe tło, czarna kreska.', 'Paszport dla zwierzęcia', GEN, 'a closed pet passport booklet, cover without text'),
    ('pasz-02-stempel', 'foto', '3/2', 'Stempel i dokumenty', 'Stempel i otwarty dokument na biurku; bez czytelnych danych.', 'Stempel i dokumenty', GEN, 'a stamp and a document on a desk, no readable text'),
    ('pasz-03-podroz', 'pas', '21/9', 'Podróż z psem', 'Szeroki pas: walizka i transporter.', 'Walizka i transporter', GEN, 'a suitcase and a pet carrier side by side, wide banner'),
    ('pasz-04-pies-kot-walizka', 'foto', '4/5', 'Pies obok walizki', 'Pies siedzący obok walizki.', 'Pies obok walizki', GEN, 'a dog sitting next to a suitcase'),
    # --- czipowanie
    ('czip-01-czip-diagram', 'diagram', '4/3', 'Schemat czipa', 'Uproszczony zarys czipa w skali obok ziarenka ryżu oraz miejsce wszczepienia po lewej stronie szyi (bez opisów).', 'Schemat czipa i miejsca wszczepienia', DRAW, 'simplified drawing of a microchip beside a grain of rice and the left side of a cat\'s neck marked by a small circle, unlabeled'),
    ('czip-02-aplikator', 'foto', '3/2', 'Aplikator czipa przy barku psa', 'Dłonie lekarki w rękawiczkach z aplikatorem przy karku spokojnego psa; igła niewidoczna.', 'Aplikator czipa przy barku psa', REAL, 'gloved hands of a veterinarian holding a microchip applicator near the scruff of a calm golden retriever, no needle visible'),
    ('czip-03-pas-zabieg', 'pas', '21/9', 'Gabinet zabiegowy', 'Szeroki pas: stół i lampa w gabinecie.', 'Gabinet, w którym wszczepiamy czipy', REAL, 'wide view of a bright veterinary room with a table and a lamp'),
    ('czip-04-skaner', 'foto', '4/5', 'Czytnik czipów', 'Czytnik czipów przy barku psa; ekran niewidoczny.', 'Odczyt czipa czytnikiem', REAL, 'a handheld microchip reader held near a dog\'s shoulder'),
    ('czip-05-pies-kot', 'wycinek', '1/1', 'Kot i pies w poczekalni', 'Spokojny szary kot i mały pies obok siebie, białe tło, czarna kreska.', 'Kot i pies siedzą obok siebie', GEN, 'a calm grey cat and a small dog sitting side by side, seen from the front'),
]

_DIM = {'foto': 1600, 'pas': 2400, 'wycinek': 1200, 'ilustracja': 1200, 'diagram': 1600, 'ikona': 256}
_RATIO_TXT = {'3/2': '3:2 landscape', '4/5': '4:5 portrait', '1/1': '1:1 square', '21/9': '21:9 wide panoramic banner',
              '4/3': '4:3 landscape', '16/9': '16:9 landscape'}
_AVOID = {
    'foto': 'twarze obcych osób, napisy, logotypy, krew, widoczny ból lub strach zwierzęcia, igły',
    'pas': 'twarze obcych osób, napisy, logotypy, zdjęcia sprzętu w użyciu',
    'wycinek': 'halo i rozmycie na krawędziach, cień, napisy, logotypy',
    'ilustracja': 'wypełnienia, gradienty, cieniowanie, napisy, drastyczność',
    'diagram': 'wypełnienia, gradienty, cieniowanie, napisy i numery, drastyczność',
    'ikona': 'detale poniżej 2 px, napisy',
}


def _prompt(kind, ratio, subject, fname, title):
    rt = _RATIO_TXT.get(ratio, ratio.replace('/', ':'))
    head = f'# {title}\nPlik: {fname}. Narzędzie: wbudowane image_gen.\n\n'
    if kind == 'foto':
        body = (f'Use case: photorealistic-natural. Asset type: website photograph, {rt}. Subject: {subject}. '
                'Casual smartphone snapshot with a retro 2010s Instagram-style filter: slightly faded warm film look, soft grain, gentle vignette, '
                'lifted blacks, faint warm light leak, slightly imperfect handheld framing. Palette: muted sage green, warm peach and apricot, '
                "deep forest green, cream; no harsh saturation. No text, no graphics, no logos, no people's faces.")
    elif kind == 'pas':
        body = (f'Use case: photorealistic-natural. Asset type: website photograph, {rt}. Subject: {subject}. '
                'Casual smartphone snapshot with a retro 2010s Instagram-style filter: slightly faded warm film look, soft grain, gentle vignette, '
                'lifted blacks, faint warm light leak. Palette: muted sage green, warm peach and apricot, deep forest green, cream. '
                "Wide horizontal composition: all key objects in a central horizontal band, plain wall and floor above and below (will be cropped to 21:9). "
                "No text, no graphics, no logos, no people's faces.")
    elif kind == 'wycinek':
        body = (f'Use case: stylized-concept. Asset type: website cutout illustration, {rt}. Subject: {subject}. '
                'Monoline black ink line art on pure white background (#FFFFFF), even stroke width, tiny solid-black accents only, '
                "in the clinic's existing line-illustration style (animals as deadpan humans). Composition within the middle 75 percent of the frame. "
                'No text, no numbers, no shading, no grey, no colour.')
    else:
        body = (f'Use case: scientific-educational illustration. Asset type: website {"icon" if kind == "ikona" else "diagram"}, {rt}. '
                f'Subject: {subject}. Monoline black ink line art on pure white background (#FFFFFF), no fill, even stroke width, '
                "consistent with the clinic's existing line illustrations. No text, no numbers, no gradients, no shading, no grey, no colour.")
    return head + body + '\n'


EXT = {'foto': 'jpg', 'pas': 'jpg', 'wycinek': 'png', 'ilustracja': 'png', 'diagram': 'png', 'ikona': 'svg'}
OBRAZY = {}
for (_id, _kind, _ratio, _title, _opis, _alt, _zr, _subj) in _ROWS:
    _pre = _id.split('-')[0]
    _slug = SLUG[_pre]
    _fn = f'{_id}.{EXT[_kind]}'
    OBRAZY[_id] = {
        'id': _id, 'strona': _slug, 'kind': _kind, 'ratio': _ratio, 'title': _title, 'opis_pl': _opis, 'alt': _alt,
        'zrodlo': _zr, 'prompt_en': _prompt(_kind, _ratio, _subj, _fn, _title), 'min_px': _DIM[_kind],
        'czego_unikac_pl': _AVOID[_kind],
        'obrobka': {'foto': 'kolor-retro', 'pas': 'kolor-retro', 'wycinek': 'ink-filter', 'ilustracja': 'ink-filter', 'diagram': 'ink-filter'}[_kind],
        'plik': f'assets/podstrony/{_slug}/{_fn}',
    }
    # diagram/ilustracja bez wypełnień → tylko przezroczyste PNG/SVG


# ----------------------------------------------------------------------------
# ilustracje hero (jedna na stronę) — zastępują odrzucone pliki z assets/illustrations/services/*.png
# ----------------------------------------------------------------------------
_HERO_SUBJ = {
    'uslugi': 'a dog and a cat sitting calmly side by side beside a small stethoscope',
    'zespol': 'a row of animal veterinarians in white coats like a staff photo, with a small dog patient in a sweater on a stool in front',
    'interna': 'a dog being gently examined with a stethoscope', 'lab': 'a test tube rack and a microscope next to a sleeping cat',
    'szcz': 'a dog and a cat with a small syringe and a vaccination booklet', 'chir': 'a calm cat resting under a soft blanket on a surgical table',
    'kard': 'a dog with a simple heart shape drawn over its chest', 'usg': 'an ultrasound probe above a lying dog',
    'oko': 'a cat with large attentive eyes and a magnifying lens', 'derm': 'a dog scratching its ear, a small comb beside it',
    'stom': 'a dog showing its teeth next to a toothbrush', 'nefr': 'a cat sitting beside a simple kidney shape',
    'uro': 'a dog and a cat beside a water bowl and a small drop', 'cis': 'a cat wearing a small blood-pressure cuff on its leg',
    'pasz': 'a dog sitting beside an open pet passport booklet', 'czip': 'a small cat with a tiny microchip capsule drawn beside it',
}
_SLUG_REV = {v: k for k, v in SLUG.items()}
_STYLE_REFS = ('assets/illustrations/services/service-internal-a.png, assets/illustrations/services/service-cardiology-b.png, '
               'assets/illustrations/services/service-eyes-a.png, assets/illustrations/services/service-dentistry-a.png')
for _pre, _slug in SLUG.items():
    _id = f'{_pre}-00-hero'
    _fn = f'{_id}.png'
    _subj = _HERO_SUBJ[_pre]
    _p = _prompt('ilustracja', '1/1', _subj, _fn, 'Ilustracja hero')
    _p += ('\nStyle references (attach all as image inputs and match their line weight, proportions, calm mood and level of detail; '
           f'do NOT copy their subjects): {_STYLE_REFS}.\nReject any result that looks generic, glossy, 3D, cartoon-mascot or stock-vector.\n')
    OBRAZY[_id] = {
        'id': _id, 'strona': _slug, 'kind': 'ilustracja', 'ratio': '1/1', 'title': 'Ilustracja hero strony',
        'opis_pl': 'Jednolinijowa ilustracja hero w stylu istniejących ilustracji usług z home (service-*-a/b/c.png). Do wygenerowania z referencjami stylu.',
        'alt': '', 'zrodlo': 'generowanie (image_gen / NanoBanana) z referencjami stylu z home',
        'prompt_en': _p, 'min_px': _DIM['ilustracja'], 'czego_unikac_pl': _AVOID['ilustracja'], 'obrobka': 'ink-filter',
        'plik': f'assets/podstrony/{_slug}/{_fn}',
    }
HERO_ID = {slug: f'{pre}-00-hero' for pre, slug in SLUG.items()}
