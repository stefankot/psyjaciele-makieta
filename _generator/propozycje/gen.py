import json
CL=json.load(open('/private/tmp/claude-501/-Users-milajovovich-Library-Application-Support-Claude-scratch-workspaces-e63bec1a-f736-4cb0-8f10-bcd724175181-03b99033-4a41-4f45-94ea-9bc6ae0c3185-scratch-2026-10-08-edfd5a/62db71fc-1f6b-4107-a48d-d8fc3ba31ede/scratchpad/shapes/clusters.json'))
def shape(i):
    c=CL[i]
    vb="%.2f %.2f %.2f %.2f"%(c['x0'],c['y0'],c['w'],c['h'])
    paths=''.join("%3Cpath d='"+d+"'/%3E" for d in c['paths'])
    return 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\''+vb+'\'%3E'+paths+'%3C/svg%3E")'
SH=[386,704,111,487,780,98,264]
P=[("Julia","Chutkowska-Świetlik",["choroby wewnętrzne"],"557c244c36a9","avif"),
("Aleksandra","Podkowa",["choroby wewnętrzne","stomatologia","ultrasonografia"],"e48db60840a2","avif"),
("Małgorzata","Tywoniuk",["kardiologia"],"d9e0817d66ec","avif"),
("Katarzyna","Krawulska",["chirurgia tkanek miękkich"],"5205d4b0e462","avif"),
("Magdalena","Ostrowska",["choroby wewnętrzne","nefrologia i urologia","anestezjologia"],"3b64aaacd150","avif"),
("Olga","Winnicka-Ziółkowska",["ultrasonografia"],"a6e997421073","avif"),
("Kinga","Bielińska-Bielecka",["okulistyka"],"5be50d2b873b","png")]
def img(p): return f"../../assets/{p[3]}-studio-tonal-v3.{p[4]}"
G="../../assets/zespol-grupa-v2.avif"
BIO='<span class="ph">Tu krótki opis lekarki: 2–3 zdania o specjalizacji i podejściu do pacjentów.</span>'
def spec(p,sep=' · '): return sep.join(p[2])
def name(p): return f'<b>{p[0]}</b> {p[1]}'
def sec(n,title,desc,body,cls=''):
    return f'<section class="opt {cls}"><header class="lab"><span>{n}</span><div><h3>{title}</h3><p>{desc}</p></div></header><div class="mock"><div class="inner"><h2>Zespół</h2>{body}</div></div></section>'
O=[]
rows=''.join(f'<li class="{"on" if i==4 else ""}"><span class="n">{i+1:02d}</span><span class="nm"><em>{p[0]}</em> {p[1]}</span><span class="sp">{spec(p)}</span><i class="ar"></i></li>' for i,p in enumerate(P))
O.append(sec(1,'Indeks','Duża typograficzna lista z liniami; po najechaniu po prawej pojawia się portret osoby (tu: Magdalena). Bez zdjęcia grupowego.',f'<div class="g1"><ul>{rows}</ul><figure><div class="pb"><img src="{img(P[4])}"></div><figcaption>{name(P[4])}</figcaption></figure></div>'))
cards=''.join(f'<li style="--o:{[0,40,8,48,0,40,8][i]}px"><div class="pb"><img src="{img(p)}"></div><b>{p[0]}</b><span>{p[1]}</span><small>{spec(p,"<br>")}</small></li>' for i,p in enumerate(P))
O.append(sec(2,'Rząd portretów w fali','Siedem równych kolumn, portrety na jednolitym tle; naprzemienne przesunięcie w pionie daje rytm. Imię, nazwisko, specjalizacje pod spodem.',f'<ul class="g2">{cards}</ul>'))
tabs=''.join(f'<span class="{"on" if i==5 else ""}">{p[0]}</span>' for i,p in enumerate(P))
O.append(sec(3,'Zdjęcie grupowe z kartą wybranej osoby','Zdjęcie 8 kolumn z ramką na wskazanej osobie; po prawej karta z portretem, specjalizacją i opisem. Pod zdjęciem zakładki z imionami.',f'<div class="g3"><div class="l"><figure class="gp"><img src="{G}"><i class="hs"></i></figure><div class="tabs">{tabs}</div></div><aside><div class="pb"><img src="{img(P[5])}"></div><h4>{name(P[5])}</h4><p class="s">{spec(P[5])}</p><p>{BIO}</p><a class="lnk">Poznaj lekarkę <i class="ar"></i></a></aside></div>'))
thumbs=''.join(f'<span class="{"on" if i==1 else ""}"><img src="{img(p)}"></span>' for i,p in enumerate(P))
O.append(sec(4,'Scena: jedna osoba duża','Jeden duży portret (5 kol.) i obok imię, specjalizacje, opis; pod spodem rząd miniatur do przełączania. Najspokojniejszy układ, najwięcej miejsca na tekst.',f'<div class="g4"><div class="pb"><img src="{img(P[1])}"></div><div class="tx"><h4><em>{P[1][0]}</em> {P[1][1]}</h4><p class="s">{spec(P[1])}</p><p>{BIO}</p><a class="lnk">Poznaj lekarkę <i class="ar"></i></a><div class="th">{thumbs}</div></div></div>'))
win=''.join(f'<li><div class="w" style="--sh:{shape(SH[i])}"><img src="{img(p)}"></div><b>{p[0]}</b> <span>{p[1]}</span><small>{spec(p)}</small></li>' for i,p in enumerate(P))
O.append(sec(5,'Okna z biblioteki kształtów (równe, w cegiełkę)','Siedem okien tej samej wielkości w kształtach z Twojego pliku, ułożonych jak cegły: 4 w górnym rzędzie, 3 pod nimi między nimi. Opisy pod oknami.',f'<ul class="g5">{win}</ul>'))
L=''.join(f'<li><b>{p[0]}</b> {p[1]}<small>{spec(p)}</small></li>' for p in P[:4]); R=''.join(f'<li><b>{p[0]}</b> {p[1]}<small>{spec(p)}</small></li>' for p in P[4:])
O.append(sec(6,'Zdjęcie w łuku, podpisy po bokach','Zdjęcie grupowe wycięte w łuk; po lewej cztery osoby z tylnego rzędu, po prawej trzy z siedzących.',f'<div class="g6"><ol class="a"><li class="t">Stoją od lewej</li>{L}</ol><figure><img src="{G}"></figure><ol class="b"><li class="t">Siedzą od lewej</li>{R}</ol></div>'))
O.append(sec(7,'Podpis jak w gazecie','Zdjęcie na całą szerokość bez znaczników; pod nim ciągły podpis „Stoją od lewej: …”, nazwiska wytłuszczone, specjalizacje w nawiasach. Minimum elementów.',f'<figure class="g7"><img src="{G}"><figcaption><p><span class="k">Stoją od lewej</span>'+', '.join(f'<b>{p[0]} {p[1]}</b> <i>({spec(p,", ")})</i>' for p in P[:4])+f'.</p><p><span class="k">Siedzą od lewej</span>'+', '.join(f'<b>{p[0]} {p[1]}</b> <i>({spec(p,", ")})</i>' for p in P[4:])+'.</p></figcaption></figure>'))
cardsb=''.join(f'<li class="c{i%3}"><img src="{img(p)}"><div><b>{p[0]}</b> {p[1]}<small>{spec(p)}</small></div></li>' for i,p in enumerate(P))
O.append(sec(8,'Bento z kafelkiem tytułowym','Siatka 4 × 2: pierwszy kafel to tytuł z ilustracją (kot i mysz), siedem kafli z portretami w trzech odcieniach palety. Podpis na dole kafla.',f'<ul class="g8"><li class="tt"><img src="../../assets/illustrations/zespol-header-first-frame.avif"><span>Poznaj osoby, które opiekują się Twoim <em>psyjacielem</em>.</span></li>{cardsb}</ul>'))
strips=''.join(f'<li class="{"open" if i==1 else ""}"><img src="{img(p)}"><div class="v"><b>{p[0]}</b></div><div class="d"><h4>{name(p)}</h4><p>{spec(p)}</p></div></li>' for i,p in enumerate(P))
O.append(sec(9,'Pasy: harmonijka pozioma','Siedem pionowych pasów z portretami; najechany pas rozszerza się i pokazuje imię, nazwisko i specjalizacje (można tu spróbować najeżdżać). Zwarte, bardzo graficzne.',f'<ul class="g9">{strips}</ul>'))
items=''.join(f'<li><div class="th"><img src="{img(p)}"></div><div><h4>{name(p)}</h4><p class="s">{spec(p)}</p><p>{BIO}</p></div><i class="ar"></i></li>' for p in P)
O.append(sec(10,'Dwie kolumny: zdjęcie przyklejone, lista przewijana','Po lewej zdjęcie grupowe przyklejone do ekranu (pionowy kadr), po prawej przewijana lista z miniaturą, opisem i strzałką; opis ma miejsce na 2–3 zdania.',f'<div class="g10"><figure><img src="{G}"></figure><ul>{items}</ul></div>'))
css=open('zespol-10-ukladow.css').read()
html='<!doctype html><html lang="pl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Zespół — 10 układów</title><style>'+css+'</style><body><div class="top"><h1>Sekcja „Zespół” na home — 10 układów (desktop)</h1><p>Schematy w kolorach i fontach strony (paleta cream). Opisy lekarek to miejsca na tekst. Dane z istniejących zasobów: zdjęcie zbiorcze, portrety tonalne, ilustracja, kształty z Shapes.svg.</p></div>'+''.join(O)+'<div style="height:60px"></div></body></html>'
open('zespol-10-ukladow.html','w').write(html)
print(len(html))
