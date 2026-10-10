# generated: psyjaciele-podstrony
"""osie.py — plan „osi kroków”: proces z listy w sekcji jako oś z kółkami i rysunkiem nad nią (wzór: szczepienia, „Kiedy szczepić szczenięta i kocięta”).

Każdy wpis OSIE: strona, id nagłówka, id rysunku, liczba kroków, hasła kroków (None = tytuły są już w liście), scenka do wygenerowania.
Oś pojawia się na stronie dopiero wtedy, gdy istnieje złożony rysunek assets/podstrony/<slug>/<id>.avif — bez niego sekcja zostaje bez zmian.

Kolejność pracy (z katalogu makiety):
  1. python3 _generator/narzedzia/osie.py prompt <id>          → prompt i referencje dla generate_openai_image (1536x1024, quality high)
  2. python3 _generator/narzedzia/os_czasu.py <id> <surowy.png> → składa oś z kółkami + scenkę, zapisuje PNG i AVIF w assets/podstrony/<slug>/
  3. python3 _generator/narzedzia/build.py && python3 _generator/narzedzia/checks.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ILU = 'assets/illustrations/services/'
WZOR = 'assets/podstrony/szczepienia-oraz-profilaktyka-przeciwpasozytnicza/szcz-03-kalendarz.png'

STYL = ('Monoline black ink illustration on a pure white background, in the exact style of the reference images: uniform hand-drawn '
        'black line of constant thickness, no grey, no shading, no gradients; a few deliberate solid black fills (droopy ear, nose, shoes); '
        'animals in human roles with deadpan faces; gentle humour in small details (a few short motion ticks). The first reference image '
        'shows the exact character design and line weight to match: the long-snouted dog with one black droopy ear, a closed eye drawn as '
        'a curved line with lashes, a ribbed knit sweater with small dashes, plain white trousers and black shoes, walking in profile to '
        'the right. The cat, when present, is the one from the references: pointed ears, long straight whiskers, half-closed sceptical '
        'eyes, white lab coat over a black turtleneck.\n\n'
        'Draw ONLY this small scene, strict side view, full-body, walking to the right, all feet resting on one invisible horizontal ground level: ')
KONIEC = ('\n\nDo NOT draw the horizontal line, the circles, any ground, floor, shadow or background. Keep the scene small: the figures about '
          'one third of the image height, centred, with wide empty white margins on all sides, and the same line weight relative to the '
          'figures as in the first reference. No text, no numbers, no letters, no shading, no grey, no colour.')

# poz = środek scenki na osi w jednostkach kółek (0 = pierwsze kółko, 1.5 = w połowie między drugim a trzecim); h = wymuszona wysokość scenki (px)
OSIE = [
    dict(slug='choroby-wewnetrzne-u-psow-i-kotow', hid='jak-wyglada-wizyta-u-internisty', id='interna-os-wizyta', n=4, hasla=None, poz=1.5,
         ref=['service-internal-a.png'],
         scena='the sweater dog walks on calmly with a thermometer sticking out of his mouth and a round ice bag tied on top of his head '
               'with a ribbon bow; one hand rests on his belly.'),
    dict(slug='kardiologia-weterynaryjna', hid='jak-wyglada-konsultacja-kardiologiczna', id='kard-os-konsultacja', n=4, hasla=None, poz=1.5,
         ref=['service-cardiology-b.png'],
         m=dict(typ='gora', scena='the sweater dog sits calmly on a simple stool in the right half of the picture, full body, with one small round '
                'electrode stuck on his chest. From the electrode leaves ONE single thin continuous black line (the same thickness as every other '
                'line in the drawing): it runs to the left, makes two sharp heartbeat spikes like an ECG trace, with one small heart outline '
                'floating above the spikes, reaches the far left side of the picture, then turns and runs perfectly straight down, vertically, '
                'all the way until it touches the bottom edge of the image.'),
         scena='the sweater dog walks while pressing the chest piece of a stethoscope against his own chest and listening with great '
               'concentration; one small heart outline floats above him with two short ticks.'),
    dict(slug='kardiologia-weterynaryjna', hid='jak-liczyc-oddechy-w-domu', id='kard-os-oddechy', n=4, poz=0.5,
         hasla=['Policz', 'Pełna minuta', 'Powtórz', 'Powyżej 30'], ref=['service-cardiology-b.png'],
         scena='the sweater dog tiptoes very carefully, carrying in both arms a curled-up sleeping cat; a stopwatch hangs from his neck on '
               'a string; three tiny puff curls rise from the sleeping cat\'s nose.'),
    dict(slug='stomatologia-weterynaryjna', hid='jak-wyglada-zabieg-stomatologiczny', id='stom-os-zabieg', n=4, hasla=None, poz=1.5,
         ref=['service-dentistry-a.png'],
         m=dict(typ='gora', scena='the sweater dog stands in the right half of the picture, full body, and squeezes an oversized toothpaste tube '
                'with both hands. The toothpaste comes out of the nozzle as ONE single thin continuous black line (the same thickness as every '
                'other line in the drawing, not a thick ribbon): it makes one playful loop in the air, travels to the far left side of the '
                'picture, then turns and runs perfectly straight down, vertically, all the way until it touches the bottom edge of the image.'),
         scena='the sweater dog marches carrying a giant toothbrush over his shoulder like a fishing rod, his mouth open in a wide grin '
               'showing a neat row of teeth, with two small four-point sparkles next to the teeth.'),
    dict(slug='chirurgia-weterynaryjna-tkanek-miekkich', hid='przygotowanie-w-dniu-zabiegu', id='chir-os-dzien-zabiegu', n=5, hasla=None, poz=2.5,
         ref=['service-surgery-b.png'],
         scena='the sweater dog walks carrying a pet carrier in one hand; the face of a grumpy cat looks out through the bars of the '
               'carrier door; a folded blanket is tucked under the dog\'s other arm.'),
    dict(slug='pomiar-cisnienia-psow-i-kotow', hid='jak-wyglada-pomiar', id='cisn-os-pomiar', n=4, poz=1.5,
         hasla=['Chwila spokoju', 'Mankiet i czujnik', 'Kilka pomiarów', 'Opiekun obok'], ref=['service-pressure-b.png'],
         scena='a cat in a plain turtleneck walks upright and calm, with a blood-pressure cuff wrapped around its raised tail; a thin tube '
               'runs from the cuff to a small round dial gauge that the cat carries in one hand and glances at sideways.'),
    dict(slug='pomiar-cisnienia-psow-i-kotow', hid='co-dzieje-sie-po-wykryciu-nadcisnienia', id='cisn-os-leczenie', n=4, poz=2.5,
         hasla=['Szukanie przyczyny', 'Dobór leku', 'Kontrolne pomiary', 'Stałe leczenie'], ref=['service-pressure-b.png'],
         scena='the sweater dog walks carrying an oversized two-part capsule pill under his arm like a baguette, and in the other hand a '
               'weekly pill organiser box drawn as a row of small empty compartments.'),
    dict(slug='wystawianie-paszportow-psom-i-kotom', hid='jak-przebiega-wizyta-w-sprawie-paszportu', id='pasz-os-wizyta', n=4, poz=1.5,
         hasla=['Odczyt czipa', 'Szczepienie', 'Wypełnienie paszportu', 'Kolejny termin'], ref=['service-passport-b.png'],
         scena='the cat vet in the lab coat walks holding an open blank booklet in one hand and a big rubber stamp raised high in the '
               'other, about to stamp it; a few short motion ticks around the stamp.'),
    dict(slug='wystawianie-paszportow-psom-i-kotom', hid='co-zabrac-na-wizyte', id='pasz-os-wyjazd', n=4, poz=2.55, ref=['service-passport-b.png'],
         # kroki stałe: te same cztery pozycje co dotychczasowe „stopnie” (infografiki.steps_paszport), bez listy źródłowej
         stale=[('Czip', 'najpierw oznakowanie'), ('Szczepienie', 'przeciw wściekliźnie'),
                ('21 dni', 'oczekiwania na ważność szczepienia'), ('Wyjazd', 'wizytę zaplanuj 3–4 tygodnie wcześniej')],
         scena='the sweater dog walks wearing a wide-brimmed sun hat, pulling a small wheeled suitcase behind him and holding a small '
               'closed blank booklet in his front hand.'),
    dict(slug='szczepienia-oraz-profilaktyka-przeciwpasozytnicza', hid='jak-przebiega-wizyta-szczepienna', id='szcz-os-wizyta', n=3, poz=0.5,
         hasla=['Rozmowa', 'Badanie i szczepionka', 'Wpis i termin'], ref=['service-prevention-a.png'],
         # 10.10: pierwsza wersja (oś jako smycz psa) odrzucona przez właściciela — „niepokojąca i niezrozumiała”; kreska nie może oplatać ani ciągnąć postaci
         m=dict(typ='dol', scena='ONE single thin continuous black line (the same thickness as every other line in the drawing) comes perfectly '
                'straight down, vertically, from the top edge of the image at the far left side of the picture; lower down it curves to the right, '
                'makes one small elegant handwriting flourish (a single loop, like the end of a signature) and ends exactly at the tip of a pen. '
                'The pen is held by the cat vet (pointed ears, long straight whiskers, half-closed sceptical eyes, white lab coat over a black '
                'turtleneck), who stands in the middle of the picture, full body, with a small open blank booklet in the other hand: the line is '
                'the ink of the pen. Next to the cat, on the right, stands the sweater dog, full body, proud with his chin up, one sleeve rolled '
                'up to show a small sticking plaster on his upper arm; his tail wags with three short motion ticks. The line does not touch or go '
                'around any character; it only ends at the pen tip.'),
         scena='the same dog in the knit sweater strides proudly with his chin up, one sweater sleeve rolled up to show a small sticking '
               'plaster on his upper arm, and in his raised front hand he carries a small closed blank booklet; his tail wags with three '
               'short motion ticks beside it.'),
    dict(slug='czipowanie-psow-i-kotow', hid='co-zrobic-po-czipowaniu', id='czip-os-po', n=4, poz=2.5, x0=697,   # x0: model dorysował kota z tyłu; zostaje sam pies
        
         hasla=['Zapisz numer', 'Sprawdź rejestrację', 'Poproś o odczyt', 'Dodaj adresówkę'], ref=['service-microchip-b.png'],
         scena='the sweater dog walks proudly, lifting with one finger a bone-shaped blank tag that dangles from his collar; in the other '
               'hand he holds a small notebook and a pencil.'),
    dict(slug='czipowanie-psow-i-kotow', hid='jak-wyglada-czipowanie', id='czip-os-czipowanie', n=4, poz=1.52, h=300,   # h: model narysował tę parę mniejszą niż pozostałe scenki
        
         hasla=['Sprawdzenie', 'Wszczepienie', 'Odczyt i wpis', 'Rejestracja'], ref=['service-microchip-b.png'],
         scena='the cat vet in the lab coat walks right behind the sweater dog and holds a handheld microchip reader (a flat paddle with '
               'a loop) to the back of the dog\'s neck; three short signal arcs come from the reader; the dog walks on unbothered.'),
    dict(slug='diagnostyka-obrazowa-psow-i-kotow', hid='jak-przebiega-badanie', id='usg-os-badanie', n=5, poz=1.06,   # kółko wypada pod kablem, między postaciami
        
         hasla=['Golenie i żel', 'Pozycja', 'Czas badania', 'Bez znieczulenia', 'Omówienie'], ref=['service-imaging-c.png'],
         scena='the sweater dog walks with his sweater pulled up a little to reveal a neat small square shaved patch on his round belly; '
               'he presses a handheld ultrasound probe against that patch, and its curly cable trails behind him.'),
    dict(slug='okulistyka-weterynaryjna', hid='jak-wyglada-badanie-okulistyczne', id='oko-os-badanie', n=4, hasla=None, poz=1.5,
         ref=['service-eyes-a.png'],
         scena='a cat in a plain turtleneck walks upright wearing an oversized round optometrist trial frame on its nose, one eye wide '
               'open and the other squinting, carrying a small dropper bottle in one hand.'),
    dict(slug='urologia-weterynaryjna', hid='jak-wyglada-diagnostyka', id='uro-os-diagnostyka', n=4, hasla=None, poz=1.5,
         ref=['service-urology-a.png'],
         scena='a cat in a plain turtleneck tiptoes very carefully, carrying a small lidded specimen cup with a blank label in both hands '
               'held out in front, eyes fixed on the cup; two short ticks around the cup.'),
]


def plik(o, ext='avif'):
    return f'assets/podstrony/{o["slug"]}/{o["id"]}.{ext}'


def gotowa(o):
    """Oś wchodzi na stronę tylko z gotowym rysunkiem."""
    return (ROOT / plik(o)).is_file()


def dla_strony(slug):
    return [o for o in OSIE if o['slug'] == slug and gotowa(o)]


def prompt(o):
    return STYL + o['scena'] + KONIEC

# --- wariant na komórkę (os_mobilna.py): scenka, z której wychodzi kreska przechodząca w pionową oś listy; wpis m=dict(typ, scena) ---
STYL_M = ('Monoline black ink illustration on a pure white background, in the exact style of the reference images: uniform hand-drawn '
          'black line of constant thickness, no grey, no shading, no gradients; a few deliberate solid black fills (droopy ear, nose, '
          'shoes); animals in human roles with deadpan faces; gentle humour in small details (a few short motion ticks). Characters '
          'exactly as in the references: the long-snouted dog with one black droopy ear, a closed eye drawn as a curved line with '
          'lashes, a ribbed knit sweater with small dashes, plain white trousers and black shoes; the cat with pointed ears, long '
          'straight whiskers, half-closed sceptical eyes, white lab coat over a black turtleneck.\n\nScene: ')
_UKLAD = '\n\nComposition: the figures fill most of the frame height and stand in the right two thirds of the picture. '
_ZASADY = 'The line never wraps around, ties or pulls any character. '
KONIEC_M = {
    'gora': (_UKLAD + 'The vertical part of the line is the leftmost element of the whole picture: nothing at all is drawn to the left of it. '
             + _ZASADY + 'Apart from the bottom end of this line, nothing touches the image edges. '),
    'dol': (_UKLAD + 'The vertical part of the line is the leftmost element of the whole picture and it touches the top edge: nothing at all is '
            'drawn to the left of it. ' + _ZASADY + 'Apart from the top end of this line, nothing touches the image edges. '),
}
BEZ = 'No ground line, no floor, no shadow, no background. No text, no numbers, no letters, no shading, no grey, no colour.'
_L = 'ONE single thin continuous black line (the same thickness as every other line in the drawing)'


def _trasa(skad):
    """Droga kreski w scenkach „gora”. Bez zdania o dwóch końcach model rysuje pionową kreskę przez całą wysokość kadru (dwie odrzucone próby)."""
    return (', travels to the far left side of the picture, then turns and runs perfectly straight down, vertically, all the way until it touches '
            f'the bottom edge of the image. The line has exactly two ends: one at {skad} and one at the bottom edge; it never continues upward '
            'above the turn.')


# scenki na komórkę dla pozostałych sekcji (10.10.2026); trzy pierwsze próbki mają wpis m= bezpośrednio w OSIE
M_SCENY = {
    # 10.10: właściciel odrzucił długopis na sznurku (interna) i nitkę z koca (chirurgia): kreska ma być czymś, co w scenie naprawdę jest linią
    'interna-os-wizyta': ('gora', 'the cat vet stands in the middle of the picture, full body, turned to the left, wearing a stethoscope with the two '
                          'earpieces in its ears, listening with a concentrated, sceptical face and one finger raised asking for silence. The '
                          f'stethoscope\'s long rubber tube is {_L}: from the Y-piece under the cat\'s chin it hangs down in front of the cat\'s chest, '
                          'makes one relaxed curl' + _trasa('the stethoscope\'s Y-piece') + ' On the right, behind the cat, the sweater dog sits on a '
                          'simple stool, full body, with a thermometer sticking out of his mouth, waiting.'),
    'kard-os-oddechy': ('gora', 'the sweater dog sleeps curled up on a big round cushion, eyes closed; behind the cushion the cat sits and watches him, '
                        f'holding a stopwatch. The dog\'s calm breath is drawn as {_L}: it starts a little in front of the dog\'s nose and makes three '
                        'soft, even waves like a breathing rhythm on its way to the left, then runs straight down at the far left to the bottom edge.'),
    'chir-os-dzien-zabiegu': ('gora', 'the sweater dog walks to the right, full body, carrying a pet carrier in his front hand, with the face of a grumpy '
                              'cat looking out through the bars of the carrier door, and holding the loop handle of a dog leash in his back hand. The '
                              f'leash is {_L}: from the loop handle in his hand it trails loosely behind him to the left, makes one relaxed curl'
                              + _trasa('the loop handle in the dog\'s hand') + ' The leash is slack and is not attached to any character.'),
    'cisn-os-pomiar': ('gora', 'the cat sits upright and perfectly calm on a simple stool, full body, facing right, eyes closed, with a blood-pressure '
                       'cuff wrapped around the upper arm that is on the left side of the picture, like a sleeve band. The cuff\'s rubber tube is '
                       f'{_L}: it leaves the cuff, makes one relaxed curl' + _trasa('the cuff') + ' On the right the sweater dog stands, full body, as '
                       'the caring owner, gently holding the cat\'s other hand.'),
    'cisn-os-leczenie': ('gora', 'the cat vet, full body, bends slightly forward and examines something through a big magnifying glass like a detective: '
                         f'under the magnifying glass begins {_L}, starting as a tiny spiral; from the spiral the line' + _trasa('the spiral')[1:]
                         + ' Behind the cat, on the right, the sweater dog stands and waits, holding a giant two-part capsule pill under his arm like '
                         'a baguette.'),
    'pasz-os-wizyta': ('gora', 'the cat vet stands, full body, holding an open blank booklet in one hand and a big rubber stamp raised high in the other. '
                       f'The booklet\'s ribbon bookmark is {_L}: it hangs out of the booklet, makes one playful curl' + _trasa('the booklet')
                       + ' On the right, next to the cat, the sweater dog stands with a small wheeled suitcase.'),
    'pasz-os-wyjazd': ('dol', f'{_L} comes perfectly straight down, vertically, from the top edge of the image at the far left side of the picture; lower '
                       'down it curves to the right, makes one loop like a flight path and ends exactly at the tail of a small paper airplane flying to '
                       'the right: the line is the trail of the airplane. The line has exactly two ends: one at the top edge and one at the airplane. '
                       'Below the airplane, in the right half, the sweater dog stands, full body, wearing a wide-brimmed sun hat, with a small wheeled '
                       'suitcase beside him, one arm still raised after throwing the airplane.'),
    'czip-os-po': ('gora', 'the sweater dog stands, full body, facing left, holding the receiver of an old-fashioned telephone to his ear with one hand '
                   f'and a small notebook in the other. The telephone\'s cord is {_L}: it hangs freely down from the bottom of the receiver, makes a few '
                   'small curly loops like a phone cord, then straightens' + _trasa('the receiver')),
    'czip-os-czipowanie': ('gora', 'the sweater dog stands, full body, facing right, and with one hand holds a handheld microchip reader (a flat paddle '
                           'with a round loop) behind his own shoulder, glancing back at it; three short signal arcs come from the reader. The reader\'s '
                           f'cable is {_L}: it leaves the bottom of the reader\'s handle, makes one relaxed curl' + _trasa('the reader')),
    'usg-os-badanie': ('gora', 'the sweater dog lies on his back on a simple examination table, full body, relaxed, his sweater pulled up a little to '
                       'show a neat small square shaved patch on his round belly. The cat vet stands behind the table and presses a handheld ultrasound '
                       f'probe onto that patch. The probe\'s cable is {_L}: it leaves the top of the probe, makes a few small curly loops'
                       + _trasa('the probe')),
    'oko-os-badanie': ('gora', 'the cat vet stands on the left, full body, holding up a small eye-drop bottle and squeezing it to test it, the tip '
                       f'pointing to the left: instead of a drop, {_L} comes out of the tip, makes one small loop in the air' + _trasa('the bottle\'s tip')
                       + ' On the right the sweater dog sits on a simple stool wearing an oversized round optometrist trial frame on his nose, one eye '
                       'wide open, watching.'),
    'uro-os-diagnostyka': ('gora', 'the sweater dog stands, full body, facing left, and tips a big water jug held high with both hands. The water pours '
                           f'out of the spout as {_L}: it arcs out to the left' + _trasa('the jug\'s spout') + ' On the right the cat, in a plain '
                           'turtleneck, stands holding out an empty glass in the wrong place and looks on, unimpressed.'),
}
for _o in OSIE:
    if _o['id'] in M_SCENY:
        _o['m'] = dict(typ=M_SCENY[_o['id']][0], scena=M_SCENY[_o['id']][1])


def plik_m(o, ext='avif'):
    return f'assets/podstrony/{o["slug"]}/{o["id"]}-m.{ext}'


def gotowa_m(o):
    return 'm' in o and (ROOT / plik_m(o)).is_file()


def prompt_m(o):
    return STYL_M + o['m']['scena'] + KONIEC_M[o['m']['typ']] + BEZ


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] in ('prompt', 'prompt-m'):
        o = next(x for x in OSIE if x['id'] == sys.argv[2])
        print(prompt(o) if sys.argv[1] == 'prompt' else prompt_m(o), '\n\nreference_images:', *[str(ROOT / WZOR)] + [str(ROOT / ILU / r) for r in o['ref']], sep='\n')
    else:
        for o in OSIE:
            print(('GOTOWA  ' if gotowa(o) else 'brak    ') + ('komórka  ' if gotowa_m(o) else '         ') + f'{o["id"]:22} {o["n"]} kroków  {o["slug"]}#{o["hid"]}')
