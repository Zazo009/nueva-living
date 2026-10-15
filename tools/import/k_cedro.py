# -*- coding: utf-8 -*-
# Cedro Golf Villas, human translations in one pass.
# a(en, es, fr, de, ru, ar, nl, pl, no, sv)
#
# Two tokens are expanded per locale, so a figure is written once and takes
# its locale's own format: €775000 -> "775.000 €" (nl "€ 775.000", fr/ru/pl/no/sv
# "775 000 €", ar "775,000 €"), and #171.55 -> "171,55" (ar "171.55").
# [m2] is the area unit: m² everywhere but ru "м²" and ar "م²".
#
#   python3 tools/import/k_cedro.py <workdir>/tr_z.json <workdir>/todo.json
import json, re, sys

LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}
UNIT['ru'] = 'м²'
UNIT['ar'] = 'م²'


def money(n, loc):
    body = f'{n:,}'.replace(',', GROUP[loc])
    return f'€ {body}' if loc == 'nl' else f'{body} €'


def expand(s, loc):
    s = re.sub(r'€(\d+)', lambda m: money(int(m.group(1)), loc), s)
    s = re.sub(r'#(\d+)\.(\d+)', lambda m: m.group(1) + ('.' if loc == 'ar' else ',') + m.group(2), s)
    return s.replace('[m2]', UNIT[loc])


T = {}
TODO = json.load(open(sys.argv[2]))
TODO_LIST = list(TODO)


def a(en, *tr):
    assert len(tr) == 9, en[:60]
    if en not in TODO:
        return  # the translation memory already has it
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def force(en, *tr):
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    a(en, *([en] * 9))


# ---------------------------------------------------------------- names
for s in ('Cedro Golf Villas', 'Cedro', 'Cedro <em>Golf Villas</em>'):
    same(s)
a('Atalaya Golf, Estepona', 'Atalaya Golf, Estepona', 'Atalaya Golf, Estepona', 'Atalaya Golf, Estepona',
  'Atalaya Golf, Эстепона', 'Atalaya Golf، إستيبونا', 'Atalaya Golf, Estepona', 'Atalaya Golf, Estepona',
  'Atalaya Golf, Estepona', 'Atalaya Golf, Estepona')
a('Atalaya Golf, <em>Estepona</em>', 'Atalaya Golf, <em>Estepona</em>', 'Atalaya Golf, <em>Estepona</em>',
  'Atalaya Golf, <em>Estepona</em>', 'Atalaya Golf, <em>Эстепона</em>', 'Atalaya Golf، <em>إستيبونا</em>',
  'Atalaya Golf, <em>Estepona</em>', 'Atalaya Golf, <em>Estepona</em>', 'Atalaya Golf, <em>Estepona</em>',
  'Atalaya Golf, <em>Estepona</em>')

# ---------------------------------------------------------------- head
a('13 of 50 semi-detached homes available at Atalaya Golf, Estepona, next to the golf club, with three bedrooms, terraces and private gardens. From EUR 775,000. The delivery date is not stated in the documents we hold.',
  '13 de 50 viviendas pareadas disponibles en Atalaya Golf, Estepona, junto al club de golf, con tres dormitorios, terrazas y jardines privados. Desde €775000. Los documentos de que disponemos no indican la fecha de entrega.',
  '13 maisons jumelées sur 50 disponibles à Atalaya Golf, Estepona, à côté du club de golf, avec trois chambres, terrasses et jardins privés. À partir de €775000. Les documents dont nous disposons n’indiquent pas la date de livraison.',
  '13 von 50 Doppelhaushälften verfügbar in Atalaya Golf, Estepona, neben dem Golfclub, mit drei Schlafzimmern, Terrassen und privaten Gärten. Ab €775000. Der Übergabetermin geht aus den uns vorliegenden Unterlagen nicht hervor.',
  'Доступны 13 из 50 парных домов в Atalaya Golf, Эстепона, рядом с гольф-клубом, с тремя спальнями, террасами и частными садами. От €775000. Срок сдачи в имеющихся у нас документах не указан.',
  '13 منزلًا شبه منفصل متاحًا من أصل 50 في Atalaya Golf بإستيبونا، بجوار نادي الغولف، من ثلاث غرف نوم مع تراسات وحدائق خاصة. ابتداءً من €775000. موعد التسليم غير مذكور في المستندات المتوفرة لدينا.',
  '13 van de 50 halfvrijstaande woningen beschikbaar bij Atalaya Golf, Estepona, naast de golfclub, met drie slaapkamers, terrassen en privétuinen. Vanaf €775000. De opleverdatum staat niet in de documenten waarover wij beschikken.',
  '13 z 50 domów bliźniaczych dostępnych w Atalaya Golf w Esteponie, obok klubu golfowego, z trzema sypialniami, tarasami i prywatnymi ogrodami. Od €775000. W posiadanych przez nas dokumentach nie podano terminu odbioru.',
  '13 av 50 tomannsboliger ledige ved Atalaya Golf, Estepona, ved siden av golfklubben, med tre soverom, terrasser og private hager. Fra €775000. Ferdigstillelsesdato er ikke oppgitt i dokumentene vi har.',
  '13 av 50 parhus lediga vid Atalaya Golf, Estepona, intill golfklubben, med tre sovrum, terrasser och privata trädgårdar. Från €775000. Färdigställandedatum anges inte i de handlingar vi har.')

a('13 of 50 semi-detached homes with three bedrooms, terraces, private gardens and two communal pools at Atalaya Golf, Estepona, from EUR 775,000.',
  '13 de 50 viviendas pareadas de tres dormitorios, con terrazas, jardines privados y dos piscinas comunitarias en Atalaya Golf, Estepona, desde €775000.',
  '13 maisons jumelées sur 50 de trois chambres, avec terrasses, jardins privés et deux piscines communes à Atalaya Golf, Estepona, à partir de €775000.',
  '13 von 50 Doppelhaushälften mit drei Schlafzimmern, Terrassen, privaten Gärten und zwei Gemeinschaftspools in Atalaya Golf, Estepona, ab €775000.',
  '13 из 50 парных домов с тремя спальнями, террасами, частными садами и двумя общими бассейнами в Atalaya Golf, Эстепона, от €775000.',
  '13 منزلًا شبه منفصل من أصل 50 من ثلاث غرف نوم مع تراسات وحدائق خاصة ومسبحين مشتركين في Atalaya Golf بإستيبونا، ابتداءً من €775000.',
  '13 van de 50 halfvrijstaande woningen met drie slaapkamers, terrassen, privétuinen en twee gemeenschappelijke zwembaden bij Atalaya Golf, Estepona, vanaf €775000.',
  '13 z 50 domów bliźniaczych z trzema sypialniami, tarasami, prywatnymi ogrodami i dwoma wspólnymi basenami w Atalaya Golf w Esteponie, od €775000.',
  '13 av 50 tomannsboliger med tre soverom, terrasser, private hager og to felles basseng ved Atalaya Golf, Estepona, fra €775000.',
  '13 av 50 parhus med tre sovrum, terrasser, privata trädgårdar och två gemensamma pooler vid Atalaya Golf, Estepona, från €775000.')

a('Semi-detached homes with gardens next to the golf club at Atalaya Golf, Estepona, from EUR 775,000.',
  'Viviendas pareadas con jardín junto al club de golf en Atalaya Golf, Estepona, desde €775000.',
  'Maisons jumelées avec jardin à côté du club de golf à Atalaya Golf, Estepona, à partir de €775000.',
  'Doppelhaushälften mit Garten neben dem Golfclub in Atalaya Golf, Estepona, ab €775000.',
  'Парные дома с садом рядом с гольф-клубом в Atalaya Golf, Эстепона, от €775000.',
  'منازل شبه منفصلة مع حدائق بجوار نادي الغولف في Atalaya Golf بإستيبونا، ابتداءً من €775000.',
  'Halfvrijstaande woningen met tuin naast de golfclub bij Atalaya Golf, Estepona, vanaf €775000.',
  'Domy bliźniacze z ogrodem obok klubu golfowego w Atalaya Golf w Esteponie, od €775000.',
  'Tomannsboliger med hage ved siden av golfklubben ved Atalaya Golf, Estepona, fra €775000.',
  'Parhus med trädgård intill golfklubben vid Atalaya Golf, Estepona, från €775000.')

a('13 of 50 semi-detached homes with three bedrooms, terraces and private gardens next to the golf club at Atalaya Golf, Estepona.',
  '13 de 50 viviendas pareadas de tres dormitorios, con terrazas y jardines privados, junto al club de golf en Atalaya Golf, Estepona.',
  '13 maisons jumelées sur 50 de trois chambres, avec terrasses et jardins privés, à côté du club de golf à Atalaya Golf, Estepona.',
  '13 von 50 Doppelhaushälften mit drei Schlafzimmern, Terrassen und privaten Gärten neben dem Golfclub in Atalaya Golf, Estepona.',
  '13 из 50 парных домов с тремя спальнями, террасами и частными садами рядом с гольф-клубом в Atalaya Golf, Эстепона.',
  '13 منزلًا شبه منفصل من أصل 50 من ثلاث غرف نوم مع تراسات وحدائق خاصة بجوار نادي الغولف في Atalaya Golf بإستيبونا.',
  '13 van de 50 halfvrijstaande woningen met drie slaapkamers, terrassen en privétuinen naast de golfclub bij Atalaya Golf, Estepona.',
  '13 z 50 domów bliźniaczych z trzema sypialniami, tarasami i prywatnymi ogrodami obok klubu golfowego w Atalaya Golf w Esteponie.',
  '13 av 50 tomannsboliger med tre soverom, terrasser og private hager ved siden av golfklubben ved Atalaya Golf, Estepona.',
  '13 av 50 parhus med tre sovrum, terrasser och privata trädgårdar intill golfklubben vid Atalaya Golf, Estepona.')

# ---------------------------------------------------------------- image alts and gallery
G = [
 ('Computer-generated view of a white semi-detached house with a grey upper floor, a rooftop pergola and a lawn',
  'Vista generada por ordenador de una vivienda pareada blanca con planta superior gris, una pérgola en la azotea y césped',
  'Vue générée par ordinateur d’une maison jumelée blanche à l’étage gris, avec une pergola sur le toit et une pelouse',
  'Computergenerierte Ansicht einer weißen Doppelhaushälfte mit grauem Obergeschoss, einer Pergola auf dem Dach und Rasen',
  'Компьютерная визуализация белого парного дома с серым верхним этажом, перголой на крыше и газоном',
  'منظر مولَّد بالحاسوب لمنزل شبه منفصل أبيض بطابق علوي رمادي وبرغولا على السطح ومرج أخضر',
  'Computergegenereerde weergave van een witte halfvrijstaande woning met een grijze bovenverdieping, een pergola op het dak en een gazon',
  'Wizualizacja komputerowa białego domu bliźniaczego z szarym piętrem, pergolą na dachu i trawnikiem',
  'Datagenerert visning av en hvit tomannsbolig med grå overetasje, en pergola på taket og plen',
  'Datorgenererad bild av ett vitt parhus med grå övervåning, en pergola på taket och gräsmatta'),
 ('Computer-generated wider view of the white house with its upper floor, rooftop pergola, olive tree and lawn',
  'Vista más amplia, generada por ordenador, de la casa blanca con su planta superior, la pérgola de la azotea, un olivo y césped',
  'Vue plus large, générée par ordinateur, de la maison blanche avec son étage, la pergola du toit, un olivier et la pelouse',
  'Computergenerierte Weitwinkelansicht des weißen Hauses mit Obergeschoss, Dachpergola, Olivenbaum und Rasen',
  'Компьютерная визуализация белого дома с более широким охватом: верхний этаж, пергола на крыше, оливковое дерево и газон',
  'منظر أوسع مولَّد بالحاسوب للمنزل الأبيض بطابقه العلوي وبرغولا السطح وشجرة زيتون ومرج أخضر',
  'Bredere computergegenereerde weergave van het witte huis met bovenverdieping, pergola op het dak, olijfboom en gazon',
  'Szersze ujęcie komputerowe białego domu z piętrem, pergolą na dachu, drzewem oliwnym i trawnikiem',
  'Bredere datagenerert visning av det hvite huset med overetasje, pergola på taket, oliventre og plen',
  'Bredare datorgenererad bild av det vita huset med övervåning, pergola på taket, olivträd och gräsmatta'),
 ('Computer-generated garden with a timber deck, a round table and lounge seating, and the covered terrace behind',
  'Jardín generado por ordenador con una plataforma de madera, una mesa redonda y asientos de descanso, y la terraza cubierta detrás',
  'Jardin généré par ordinateur avec un deck en bois, une table ronde et des assises de détente, et la terrasse couverte derrière',
  'Computergenerierter Garten mit Holzdeck, rundem Tisch und Loungemöbeln, dahinter die überdachte Terrasse',
  'Компьютерная визуализация сада с деревянным настилом, круглым столом и местом для отдыха, а за ним крытая терраса',
  'حديقة مولَّدة بالحاسوب فيها منصة خشبية وطاولة مستديرة ومقاعد للاسترخاء، وخلفها التراس المغطى',
  'Computergegenereerde tuin met een houten vlonder, een ronde tafel en loungezitplaatsen, met erachter het overdekte terras',
  'Ogród w wizualizacji komputerowej z drewnianym podestem, okrągłym stołem i miejscami wypoczynkowymi oraz zadaszonym tarasem w tle',
  'Datagenerert hage med et tredekk, et rundt bord og loungemøbler, og den overbygde terrassen bak',
  'Datorgenererad trädgård med ett trädäck, ett runt bord och loungemöbler, och den övertäckta terrassen bakom'),
 ('Computer-generated covered terrace with a long dining table and a sofa, opening onto the lawn',
  'Terraza cubierta generada por ordenador con una mesa de comedor larga y un sofá, abierta al césped',
  'Terrasse couverte générée par ordinateur avec une longue table à manger et un canapé, ouverte sur la pelouse',
  'Computergenerierte überdachte Terrasse mit langem Esstisch und Sofa, zum Rasen hin geöffnet',
  'Компьютерная визуализация крытой террасы с длинным обеденным столом и диваном, выходящей на газон',
  'تراس مغطى مولَّد بالحاسوب فيه طاولة طعام طويلة وأريكة، ويُفتح على المرج',
  'Computergegenereerd overdekt terras met een lange eettafel en een bank, open naar het gazon',
  'Zadaszony taras w wizualizacji komputerowej z długim stołem jadalnianym i sofą, otwarty na trawnik',
  'Datagenerert overbygd terrasse med et langt spisebord og en sofa, åpen mot plenen',
  'Datorgenererad övertäckt terrass med ett långt matbord och en soffa, öppen mot gräsmattan'),
 ('Computer-generated front door set in timber-look cladding, with a paved path and planting',
  'Puerta de entrada generada por ordenador, enmarcada en un revestimiento de aspecto madera, con un camino pavimentado y vegetación',
  'Porte d’entrée générée par ordinateur, encadrée d’un revêtement aspect bois, avec un chemin dallé et des plantations',
  'Computergenerierte Haustür in einer Holzoptik-Verkleidung, mit gepflastertem Weg und Bepflanzung',
  'Компьютерная визуализация входной двери в обрамлении облицовки под дерево, с мощёной дорожкой и зеленью',
  'باب المدخل مولَّد بالحاسوب ضمن كسوة بمظهر الخشب، مع ممر مرصوف ونباتات',
  'Computergegenereerde voordeur in een bekleding met houtlook, met een bestraat pad en beplanting',
  'Drzwi wejściowe w wizualizacji komputerowej w okładzinie imitującej drewno, z brukowaną ścieżką i zielenią',
  'Datagenerert inngangsdør i en kledning med trelook, med en brolagt sti og beplantning',
  'Datorgenererad ytterdörr i en träliknande beklädnad, med en stenlagd gång och planteringar'),
 ('Computer-generated living room with a corner sofa, timber slat screens and sliding glass doors to the terrace',
  'Salón generado por ordenador con un sofá rinconero, celosías de lamas de madera y puertas correderas de vidrio a la terraza',
  'Salon généré par ordinateur avec un canapé d’angle, des claustras en lames de bois et des baies vitrées coulissantes vers la terrasse',
  'Computergeneriertes Wohnzimmer mit Ecksofa, Holzlamellen-Sichtschutz und gläsernen Schiebetüren zur Terrasse',
  'Компьютерная визуализация гостиной с угловым диваном, деревянными рейками-экранами и стеклянными раздвижными дверями на террасу',
  'غرفة معيشة مولَّدة بالحاسوب فيها أريكة زاوية وحواجز من ألواح الخشب وأبواب زجاجية منزلقة نحو التراس',
  'Computergegenereerde woonkamer met een hoekbank, houten lamellenschermen en glazen schuifdeuren naar het terras',
  'Salon w wizualizacji komputerowej z sofą narożną, drewnianymi listwowymi ekranami i szklanymi drzwiami przesuwnymi na taras',
  'Datagenerert stue med en hjørnesofa, skjermer av trelister og skyvedører i glass ut til terrassen',
  'Datorgenererat vardagsrum med en hörnsoffa, skärmar av träribbor och skjutdörrar i glas mot terrassen'),
 ('Computer-generated lower-level lounge with a corner sofa, a television, shelving, built-in wardrobes and stairs',
  'Sala del nivel inferior generada por ordenador con un sofá rinconero, un televisor, estanterías, armarios empotrados y una escalera',
  'Salon du niveau inférieur généré par ordinateur avec un canapé d’angle, un téléviseur, des étagères, des placards intégrés et un escalier',
  'Computergenerierter Aufenthaltsraum im Untergeschoss mit Ecksofa, Fernseher, Regalen, Einbauschränken und Treppe',
  'Компьютерная визуализация гостиной нижнего уровня с угловым диваном, телевизором, стеллажами, встроенными шкафами и лестницей',
  'صالة المستوى السفلي مولَّدة بالحاسوب فيها أريكة زاوية وتلفزيون ورفوف وخزائن مدمجة ودرج',
  'Computergegenereerde zitkamer op de onderste verdieping met een hoekbank, een televisie, planken, inbouwkasten en een trap',
  'Salon na niższym poziomie w wizualizacji komputerowej z sofą narożną, telewizorem, regałami, szafami wnękowymi i schodami',
  'Datagenerert oppholdsrom i underetasjen med en hjørnesofa, et TV-apparat, hyller, innebygde garderobeskap og trapp',
  'Datorgenererat vardagsrum på nedre plan med en hörnsoffa, en tv, hyllor, inbyggda garderober och en trappa'),
 ('Computer-generated bedroom with two single beds and a window with views of the hills',
  'Dormitorio generado por ordenador con dos camas individuales y una ventana con vistas a las colinas',
  'Chambre générée par ordinateur avec deux lits simples et une fenêtre donnant sur les collines',
  'Computergeneriertes Schlafzimmer mit zwei Einzelbetten und einem Fenster mit Blick auf die Hügel',
  'Компьютерная визуализация спальни с двумя односпальными кроватями и окном с видом на холмы',
  'غرفة نوم مولَّدة بالحاسوب فيها سريران مفردان ونافذة تطل على التلال',
  'Computergegenereerde slaapkamer met twee eenpersoonsbedden en een raam met uitzicht op de heuvels',
  'Sypialnia w wizualizacji komputerowej z dwoma pojedynczymi łóżkami i oknem z widokiem na wzgórza',
  'Datagenerert soverom med to enkeltsenger og et vindu med utsikt mot åsene',
  'Datorgenererat sovrum med två enkelsängar och ett fönster med utsikt över kullarna'),
 ('Computer-generated bathroom with a walk-in shower, a wall-hung basin and a toilet',
  'Baño generado por ordenador con una ducha a ras de suelo, un lavabo suspendido y un inodoro',
  'Salle de bains générée par ordinateur avec une douche à l’italienne, une vasque suspendue et des toilettes',
  'Computergeneriertes Badezimmer mit bodengleicher Dusche, Wandwaschbecken und WC',
  'Компьютерная визуализация ванной комнаты с душем без поддона, подвесной раковиной и унитазом',
  'حمّام مولَّد بالحاسوب فيه دش بمستوى الأرض وحوض معلّق ومرحاض',
  'Computergegenereerde badkamer met een inloopdouche, een hangende wastafel en een toilet',
  'Łazienka w wizualizacji komputerowej z prysznicem bez brodzika, umywalką wiszącą i toaletą',
  'Datagenerert bad med en åpen dusj, en veggmontert servant og et toalett',
  'Datorgenererat badrum med en duschplats i golvnivå, en väggmonterad handfat och en toalett'),
 ('Computer-generated communal pool beside a lawn with sun loungers, with hills in the distance',
  'Piscina comunitaria generada por ordenador junto a un césped con tumbonas, con colinas al fondo',
  'Piscine commune générée par ordinateur au bord d’une pelouse avec des transats, avec des collines au loin',
  'Computergenerierter Gemeinschaftspool neben einem Rasen mit Sonnenliegen, mit Hügeln in der Ferne',
  'Компьютерная визуализация общего бассейна рядом с газоном и шезлонгами, вдали холмы',
  'مسبح مشترك مولَّد بالحاسوب بجوار مرج فيه كراسي للاستلقاء، وتظهر التلال في البعيد',
  'Computergegenereerd gemeenschappelijk zwembad naast een gazon met ligbedden, met heuvels in de verte',
  'Wspólny basen w wizualizacji komputerowej obok trawnika z leżakami, ze wzgórzami w oddali',
  'Datagenerert felles basseng ved siden av en plen med solsenger, med åser i det fjerne',
  'Datorgenererad gemensam pool bredvid en gräsmatta med solstolar, med kullar i fjärran'),
 ('Computer-generated communal pool with a shallow entry, with white houses behind it',
  'Piscina comunitaria generada por ordenador con acceso de poca profundidad, con casas blancas detrás',
  'Piscine commune générée par ordinateur avec une entrée peu profonde, avec des maisons blanches derrière',
  'Computergenerierter Gemeinschaftspool mit flachem Einstieg und weißen Häusern dahinter',
  'Компьютерная визуализация общего бассейна с пологим входом, за ним белые дома',
  'مسبح مشترك مولَّد بالحاسوب بمدخل ضحل، وخلفه منازل بيضاء',
  'Computergegenereerd gemeenschappelijk zwembad met een ondiepe instap, met witte huizen erachter',
  'Wspólny basen w wizualizacji komputerowej z płytkim wejściem, a za nim białe domy',
  'Datagenerert felles basseng med grunn inngang, med hvite hus bak',
  'Datorgenererad gemensam pool med grund entré, med vita hus bakom'),
 ('Computer-generated aerial view of the white houses among greenery, with the coast and the sea on the horizon',
  'Vista aérea generada por ordenador de las casas blancas entre vegetación, con la costa y el mar en el horizonte',
  'Vue aérienne générée par ordinateur des maisons blanches au milieu de la verdure, avec la côte et la mer à l’horizon',
  'Computergenerierte Luftaufnahme der weißen Häuser im Grünen, mit Küste und Meer am Horizont',
  'Компьютерная аэросъёмка белых домов среди зелени, на горизонте побережье и море',
  'منظر جوي مولَّد بالحاسوب للمنازل البيضاء وسط الخضرة، وعلى الأفق الساحل والبحر',
  'Computergegenereerd luchtbeeld van de witte huizen tussen het groen, met de kust en de zee aan de horizon',
  'Widok z lotu ptaka w wizualizacji komputerowej na białe domy wśród zieleni, z wybrzeżem i morzem na horyzoncie',
  'Datagenerert flyfoto av de hvite husene mellom grøntarealer, med kysten og havet i horisonten',
  'Datorgenererad flygvy över de vita husen bland grönskan, med kusten och havet vid horisonten'),
 ('Computer-generated open-plan kitchen with a breakfast bar, a dining table and a sofa, looking out to the garden',
  'Cocina abierta generada por ordenador con una barra de desayuno, una mesa de comedor y un sofá, con vistas al jardín',
  'Cuisine ouverte générée par ordinateur avec un bar de petit-déjeuner, une table à manger et un canapé, donnant sur le jardin',
  'Computergenerierte offene Küche mit Frühstückstresen, Esstisch und Sofa, mit Blick in den Garten',
  'Компьютерная визуализация кухни открытой планировки с барной стойкой, обеденным столом и диваном, с видом на сад',
  'مطبخ مفتوح مولَّد بالحاسوب فيه كاونتر للفطور وطاولة طعام وأريكة، ويطل على الحديقة',
  'Computergegenereerde open keuken met een ontbijtbar, een eettafel en een bank, met uitzicht op de tuin',
  'Otwarta kuchnia w wizualizacji komputerowej z barkiem śniadaniowym, stołem jadalnianym i sofą, z widokiem na ogród',
  'Datagenerert åpen kjøkkenløsning med en frokostbar, et spisebord og en sofa, med utsikt mot hagen',
  'Datorgenererat öppet kök med en frukostbar, ett matbord och en soffa, med utsikt mot trädgården'),
 ('Computer-generated main bedroom with a double bed and a window to the landscape',
  'Dormitorio principal generado por ordenador con una cama de matrimonio y una ventana al paisaje',
  'Chambre principale générée par ordinateur avec un lit double et une fenêtre ouverte sur le paysage',
  'Computergeneriertes Hauptschlafzimmer mit Doppelbett und einem Fenster zur Landschaft',
  'Компьютерная визуализация главной спальни с двуспальной кроватью и окном с видом на окрестности',
  'غرفة النوم الرئيسية مولَّدة بالحاسوب فيها سرير مزدوج ونافذة تطل على المنظر الطبيعي',
  'Computergegenereerde hoofdslaapkamer met een tweepersoonsbed en een raam met uitzicht op het landschap',
  'Główna sypialnia w wizualizacji komputerowej z łóżkiem dwuosobowym i oknem na krajobraz',
  'Datagenerert hovedsoverom med en dobbeltseng og et vindu mot landskapet',
  'Datorgenererat huvudsovrum med en dubbelsäng och ett fönster mot landskapet'),
]
for g in G:
    a(*g)

CAPS = [
 ('The garden facade', 'La fachada al jardín', 'La façade côté jardin', 'Die Gartenfassade', 'Фасад со стороны сада', 'الواجهة المطلة على الحديقة', 'De gevel aan de tuinzijde', 'Elewacja od strony ogrodu', 'Fasaden mot hagen', 'Fasaden mot trädgården'),
 ('The house from the garden', 'La casa vista desde el jardín', 'La maison vue du jardin', 'Das Haus vom Garten aus', 'Дом со стороны сада', 'المنزل من الحديقة', 'Het huis vanuit de tuin', 'Dom widziany z ogrodu', 'Huset sett fra hagen', 'Huset sett från trädgården'),
 ('Deck and lawn', 'La plataforma de madera y el césped', 'Le deck et la pelouse', 'Holzdeck und Rasen', 'Настил и газон', 'المنصة الخشبية والمرج', 'Vlonder en gazon', 'Podest i trawnik', 'Tredekk og plen', 'Trädäck och gräsmatta'),
 ('The covered terrace', 'La terraza cubierta', 'La terrasse couverte', 'Die überdachte Terrasse', 'Крытая терраса', 'التراس المغطى', 'Het overdekte terras', 'Zadaszony taras', 'Den overbygde terrassen', 'Den övertäckta terrassen'),
 ('The entrance', 'La entrada', 'L’entrée', 'Der Eingang', 'Вход', 'المدخل', 'De entree', 'Wejście', 'Inngangen', 'Entrén'),
 ('Kitchen, dining and living room', 'Cocina, comedor y salón', 'Cuisine, salle à manger et salon', 'Küche, Essbereich und Wohnzimmer', 'Кухня, столовая и гостиная', 'المطبخ وغرفة الطعام وغرفة المعيشة', 'Keuken, eetkamer en woonkamer', 'Kuchnia, jadalnia i salon', 'Kjøkken, spisestue og stue', 'Kök, matplats och vardagsrum'),
 ('The lower level', 'El nivel inferior', 'Le niveau inférieur', 'Das Untergeschoss', 'Нижний уровень', 'المستوى السفلي', 'De onderste verdieping', 'Poziom niższy', 'Underetasjen', 'Nedre plan'),
 ('The communal pool and lawn', 'La piscina comunitaria y el césped', 'La piscine commune et la pelouse', 'Der Gemeinschaftspool und der Rasen', 'Общий бассейн и газон', 'المسبح المشترك والمرج', 'Het gemeenschappelijke zwembad en het gazon', 'Wspólny basen i trawnik', 'Fellesbassenget og plenen', 'Den gemensamma poolen och gräsmattan'),
 ('The development from above', 'La promoción vista desde arriba', 'Le programme vu d’en haut', 'Die Anlage von oben', 'Комплекс с высоты', 'المشروع من الأعلى', 'Het project van boven', 'Inwestycja z lotu ptaka', 'Prosjektet fra oven', 'Projektet uppifrån'),
]
for c in CAPS:
    a(*c)

# plans: alt and caption per home, built from the words an earlier project already uses
tm = json.load(open(sys.argv[3]))
FPL = tm['Floorplan of home 1']
CAPW = {'es': 'Vivienda', 'fr': 'Logement', 'de': 'Haus', 'ru': 'Дом', 'ar': 'المسكن', 'nl': 'Woning', 'pl': 'Lokal', 'no': 'Bolig', 'sv': 'Bostad'}
REFS = ['F1V15', 'F1V20', 'F1V23', 'F1V24', 'F1V35', 'F1V37', 'F1V38', 'F1V46', 'F2V19', 'F2V20', 'F2V42', 'F3V1', 'FIIIV7']
for r in REFS:
    en = f'Floorplan of home {r}'
    T[en] = {l: FPL[l].rsplit(' ', 1)[0] + ' ' + r for l in LOCS}
    en = f'Home {r}'
    T[en] = {l: f'{CAPW[l]} {r}' for l in LOCS}
    same(r)

# size strings, with the locale words an earlier project already uses
SZ = {
 'es': '{b} m² construidos, {t} m² de terraza, {g} m² de jardín',
 'fr': '{b} m² construits, {t} m² de terrasse, {g} m² de jardin',
 'de': '{b} m² bebaut, {t} m² Terrasse, {g} m² Garten',
 'ru': '{b} м² застроенной площади, терраса {t} м², сад {g} м²',
 'ar': '{b} م² مبنية، {t} م² تراس، {g} م² حديقة',
 'nl': '{b} m² bebouwd, {t} m² terras, {g} m² tuin',
 'pl': '{b} m² zabudowy, {t} m² tarasu, {g} m² ogrodu',
 'no': '{b} m² bygd, {t} m² terrasse, {g} m² hage',
 'sv': '{b} m² byggyta, {t} m² terrass, {g} m² trädgård',
}
for en in list(TODO):
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm terrace, ([\d.]+) sqm garden', en)
    if m:
        T[en] = {l: SZ[l].format(b=expand('#' + m.group(1), l), t=expand('#' + m.group(2), l), g=expand('#' + m.group(3), l)) for l in LOCS}

# ---------------------------------------------------------------- media
a('Computer-generated views of the homes, their interiors and the communal pool, and the floorplans of the 13 homes on the price list.',
  'Vistas generadas por ordenador de las viviendas, sus interiores y la piscina comunitaria, y los planos de las 13 viviendas de la lista de precios.',
  'Vues générées par ordinateur des maisons, de leurs intérieurs et de la piscine commune, et plans des 13 maisons de la liste de prix.',
  'Computergenerierte Ansichten der Häuser, ihrer Innenräume und des Gemeinschaftspools sowie die Grundrisse der 13 Häuser der Preisliste.',
  'Компьютерные визуализации домов, их интерьеров и общего бассейна, а также планировки 13 домов из прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمنازل وداخلها والمسبح المشترك، ومخططات المنازل الـ13 الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van de woningen, hun interieurs en het gemeenschappelijke zwembad, en de plattegronden van de 13 woningen op de prijslijst.',
  'Wizualizacje komputerowe domów, ich wnętrz i wspólnego basenu oraz rzuty 13 domów z cennika.',
  'Datagenererte bilder av boligene, interiørene og fellesbassenget, og plantegningene av de 13 boligene på prislisten.',
  'Datorgenererade bilder av bostäderna, deras interiörer och den gemensamma poolen, samt planritningarna för de 13 bostäderna på prislistan.')

a('All the photographs are computer-generated images, and the furniture and decoration in them are illustrative and not included. The floorplans are the developer’s project-stage plans, the areas on them are approximate and subject to the final project, and the room names on them are in Spanish. For home F1V37 the developer’s sheet we hold shows only the two lower levels.',
  'Todas las fotografías son imágenes generadas por ordenador, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los del promotor, en fase de proyecto, y las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo. Los nombres de las estancias en los planos están en español. De la vivienda F1V37, la hoja del promotor de que disponemos solo muestra los dos niveles inferiores.',
  'Toutes les photographies sont des images générées par ordinateur, et le mobilier et la décoration qui y figurent sont illustratifs et non inclus. Les plans sont ceux du promoteur, au stade du projet, et les surfaces qui y figurent sont approximatives et soumises au projet définitif. Les noms des pièces sur les plans sont en espagnol. Pour la maison F1V37, la feuille du promoteur dont nous disposons ne montre que les deux niveaux inférieurs.',
  'Alle Fotografien sind computergenerierte Bilder, und die darin gezeigte Möblierung und Dekoration ist illustrativ und nicht enthalten. Die Grundrisse sind die Pläne des Bauträgers im Projektstadium, die darauf angegebenen Flächen sind ungefähre Angaben und vorbehaltlich des endgültigen Projekts, und die Raumbezeichnungen auf den Plänen sind auf Spanisch. Vom Haus F1V37 zeigt das uns vorliegende Blatt des Bauträgers nur die beiden unteren Ebenen.',
  'Все фотографии являются компьютерными изображениями, а показанная на них мебель и отделка носят иллюстративный характер и в стоимость не входят. Планировки — это проектные планы застройщика, указанные на них площади приблизительны и зависят от окончательного проекта, а названия помещений на планах даны на испанском языке. По дому F1V37 у нас есть лист застройщика, на котором показаны только два нижних уровня.',
  'جميع الصور مولَّدة بالحاسوب، وما يظهر فيها من أثاث وديكور هو للتوضيح فقط وغير مشمول. المخططات هي مخططات المطوّر في مرحلة المشروع، والمساحات المبيَّنة عليها تقريبية وتخضع للمشروع النهائي، وأسماء الغرف عليها بالإسبانية. أما المسكن F1V37 فلا تُظهر ورقة المطوّر المتوفرة لدينا سوى المستويين السفليين.',
  'Alle foto’s zijn computergegenereerde beelden, en het meubilair en de inrichting die erop te zien zijn, zijn illustratief en niet inbegrepen. De plattegronden zijn de plannen van de ontwikkelaar in projectfase, de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project, en de namen van de ruimtes op de plannen staan in het Spaans. Van woning F1V37 toont het blad van de ontwikkelaar dat wij hebben alleen de twee onderste niveaus.',
  'Wszystkie zdjęcia to obrazy wygenerowane komputerowo, a pokazane na nich meble i wyposażenie mają charakter poglądowy i nie są wliczone w cenę. Rzuty to plany dewelopera na etapie projektu, podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu, a nazwy pomieszczeń na planach są po hiszpańsku. W przypadku domu F1V37 posiadany przez nas arkusz dewelopera pokazuje tylko dwa niższe poziomy.',
  'Alle fotografiene er datagenererte bilder, og møblene og dekorasjonen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens planer på prosjektstadiet, arealene på dem er omtrentlige og med forbehold om det endelige prosjektet, og romnavnene på tegningene er på spansk. For bolig F1V37 viser utbyggerens ark vi har bare de to nedre nivåene.',
  'Alla fotografier är datorgenererade bilder, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens projektplaner, ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet, och rumsnamnen på ritningarna är på spanska. För bostad F1V37 visar exploatörens ark som vi har bara de två nedre planen.')

# ---------------------------------------------------------------- overview
a('Fifty semi-detached homes, <em>thirteen listed</em>',
  'Cincuenta viviendas pareadas, <em>trece a la venta</em>',
  'Cinquante maisons jumelées, <em>treize annoncées</em>',
  'Fünfzig Doppelhaushälften, <em>dreizehn gelistet</em>',
  'Пятьдесят парных домов, <em>тринадцать в продаже</em>',
  'خمسون منزلًا شبه منفصل، <em>ثلاثة عشر منها معروضة</em>',
  'Vijftig halfvrijstaande woningen, <em>dertien vermeld</em>',
  'Pięćdziesiąt domów bliźniaczych, <em>trzynaście w ofercie</em>',
  'Femti tomannsboliger, <em>tretten annonsert</em>',
  'Femtio parhus, <em>tretton listade</em>')

a('This is a development of 50 contemporary semi-detached homes at Atalaya Golf in Estepona, next to the Atalaya Golf & Country Club and close to commercial areas, with Puerto Banús nearby. The developer’s page describes a large living room, an open kitchen supplied furnished and fitted with branded appliances, a terrace and a garden for every home.',
  'Se trata de una promoción de 50 viviendas pareadas contemporáneas en Atalaya Golf, en Estepona, junto al Atalaya Golf & Country Club y cerca de zonas comerciales, con Puerto Banús a poca distancia. La página del promotor describe un gran salón, una cocina abierta entregada amueblada y equipada con electrodomésticos de marca, y una terraza y un jardín en cada vivienda.',
  'Il s’agit d’un programme de 50 maisons jumelées contemporaines à Atalaya Golf, à Estepona, à côté de l’Atalaya Golf & Country Club et près des zones commerciales, avec Puerto Banús à proximité. La page du promoteur décrit un grand séjour, une cuisine ouverte livrée meublée et équipée d’électroménager de marque, ainsi qu’une terrasse et un jardin pour chaque maison.',
  'Es handelt sich um eine Anlage mit 50 zeitgenössischen Doppelhaushälften in Atalaya Golf in Estepona, neben dem Atalaya Golf & Country Club und in der Nähe von Einkaufsbereichen, mit Puerto Banús in der Nähe. Die Seite des Bauträgers beschreibt ein großes Wohnzimmer, eine offene Küche, die möbliert und mit Markengeräten ausgestattet geliefert wird, sowie eine Terrasse und einen Garten bei jedem Haus.',
  'Это комплекс из 50 современных парных домов в Atalaya Golf в Эстепоне, рядом с Atalaya Golf & Country Club и недалеко от торговых зон; Пуэрто-Банус находится поблизости. На странице застройщика описаны просторная гостиная, открытая кухня, которая поставляется меблированной и оснащённой техникой известных марок, а также терраса и сад у каждого дома.',
  'هذا مشروع من 50 منزلًا شبه منفصل بتصميم معاصر في Atalaya Golf بإستيبونا، بجوار Atalaya Golf & Country Club وقرب المناطق التجارية، وبويرتو بانوس قريب منه. تصف صفحة المطوّر غرفة معيشة واسعة ومطبخًا مفتوحًا يُسلَّم مفروشًا ومجهزًا بأجهزة من علامات معروفة، مع تراس وحديقة لكل منزل.',
  'Dit is een project van 50 eigentijdse halfvrijstaande woningen bij Atalaya Golf in Estepona, naast de Atalaya Golf & Country Club en dicht bij winkelgebieden, met Puerto Banús in de buurt. De pagina van de ontwikkelaar beschrijft een grote woonkamer, een open keuken die gemeubileerd en met merkapparatuur wordt geleverd, en een terras en een tuin bij elke woning.',
  'To inwestycja obejmująca 50 nowoczesnych domów bliźniaczych w Atalaya Golf w Esteponie, obok Atalaya Golf & Country Club i w pobliżu stref handlowych, z Puerto Banús w niewielkiej odległości. Strona dewelopera opisuje duży salon, otwartą kuchnię dostarczaną umeblowaną i wyposażoną w sprzęt znanych marek oraz taras i ogród przy każdym domu.',
  'Dette er et prosjekt med 50 moderne tomannsboliger ved Atalaya Golf i Estepona, ved siden av Atalaya Golf & Country Club og nær kommersielle områder, med Puerto Banús i nærheten. Utbyggerens side beskriver en stor stue, et åpent kjøkken som leveres møblert og utstyrt med merkevarehvitevarer, samt en terrasse og en hage til hver bolig.',
  'Detta är ett projekt med 50 moderna parhus vid Atalaya Golf i Estepona, intill Atalaya Golf & Country Club och nära kommersiella områden, med Puerto Banús i närheten. Exploatörens sida beskriver ett stort vardagsrum, ett öppet kök som levereras möblerat och utrustat med märkesvitvaror, samt en terrass och en trädgård till varje bostad.')

a('The communal gardens have two saltwater pools, one of them for children with a beach-style entry. The developer’s page calls the last homes “turnkey” in phase 1, while the plans we hold are project-stage plans with no delivery date, so we ask for the status of the works before any reservation.',
  'Los jardines comunitarios tienen dos piscinas de agua salada, una de ellas infantil y con acceso tipo playa. La página del promotor presenta las últimas viviendas de la fase 1 como «llave en mano», mientras que los planos de que disponemos son planos de proyecto, sin fecha de entrega, por lo que pedimos el estado de las obras antes de cualquier reserva.',
  'Les jardins communs comptent deux piscines à l’eau salée, dont une pour enfants avec un accès en pente douce de type plage. La page du promoteur présente les dernières maisons de la phase 1 comme « clés en main », alors que les plans dont nous disposons sont des plans de projet, sans date de livraison ; nous demandons donc l’état d’avancement des travaux avant toute réservation.',
  'Die Gemeinschaftsgärten haben zwei Salzwasserpools, einer davon für Kinder mit strandartigem Einstieg. Die Seite des Bauträgers nennt die letzten Häuser der Phase 1 „schlüsselfertig“, während die uns vorliegenden Pläne Projektpläne ohne Übergabetermin sind; wir fragen daher vor jeder Reservierung nach dem Stand der Bauarbeiten.',
  'В общих садах два бассейна с солёной водой, один из них детский, с пологим входом наподобие пляжа. На странице застройщика последние дома первой очереди названы «под ключ», тогда как имеющиеся у нас планы — проектные и без срока сдачи, поэтому перед любым бронированием мы запрашиваем состояние строительных работ.',
  'في الحدائق المشتركة مسبحان بالمياه المالحة، أحدهما للأطفال بمدخل على شكل شاطئ. تصف صفحة المطوّر آخر منازل المرحلة الأولى بأنها «جاهزة للسكن بمفتاحها»، بينما المخططات التي لدينا هي مخططات مرحلة المشروع وبلا موعد تسليم، لذلك نسأل عن حالة الأعمال قبل أي حجز.',
  'De gemeenschappelijke tuinen hebben twee zoutwaterzwembaden, waarvan één voor kinderen met een strandachtige instap. De pagina van de ontwikkelaar noemt de laatste woningen van fase 1 “turnkey”, terwijl de plannen waarover wij beschikken projectplannen zijn zonder opleverdatum; daarom vragen wij vóór elke reservering naar de stand van de werken.',
  'We wspólnych ogrodach znajdują się dwa baseny ze słoną wodą, w tym jeden dla dzieci z wejściem w stylu plaży. Strona dewelopera określa ostatnie domy w fazie 1 jako „pod klucz”, natomiast posiadane przez nas plany to plany projektowe bez terminu odbioru, dlatego przed każdą rezerwacją pytamy o stan robót.',
  'Fellesarealene har to saltvannsbasseng, ett av dem for barn med strandlignende inngang. Utbyggerens side kaller de siste boligene i fase 1 «nøkkelferdige», mens planene vi har er prosjektplaner uten overtakelsesdato, så vi spør om byggestatus før enhver reservasjon.',
  'De gemensamma trädgårdarna har två saltvattenpooler, varav en för barn med strandliknande entré. Exploatörens sida kallar de sista bostäderna i fas 1 ”nyckelfärdiga”, medan planerna vi har är projektplaner utan färdigställandedatum, så vi frågar efter byggstatus före varje bokning.')

a('50 homes', '50 viviendas', '50 maisons', '50 Häuser', '50 домов', '50 منزلًا', '50 woningen', '50 domów', '50 boliger', '50 bostäder')
# ---------------------------------------------------------------- why
a('Semi-detached homes with private gardens, a terrace on every plan and two communal pools, next to a golf club.',
  'Viviendas pareadas con jardín privado, una terraza en todos los planos y dos piscinas comunitarias, junto a un club de golf.',
  'Maisons jumelées avec jardin privé, une terrasse sur chaque plan et deux piscines communes, à côté d’un club de golf.',
  'Doppelhaushälften mit privaten Gärten, einer Terrasse auf jedem Grundriss und zwei Gemeinschaftspools, neben einem Golfclub.',
  'Парные дома с частными садами, террасой на каждой планировке и двумя общими бассейнами рядом с гольф-клубом.',
  'منازل شبه منفصلة بحدائق خاصة وتراس في كل مخطط ومسبحين مشتركين، بجوار نادي غولف.',
  'Halfvrijstaande woningen met privétuinen, een terras op elke plattegrond en twee gemeenschappelijke zwembaden, naast een golfclub.',
  'Domy bliźniacze z prywatnymi ogrodami, tarasem na każdym rzucie i dwoma wspólnymi basenami, obok klubu golfowego.',
  'Tomannsboliger med private hager, en terrasse på hver plantegning og to felles basseng, ved siden av en golfklubb.',
  'Parhus med privata trädgårdar, en terrass på varje planritning och två gemensamma pooler, intill en golfklubb.')

a('Families and second-home buyers who want an independent house with a garden rather than an apartment, close to a golf club.',
  'Familias y compradores de segunda residencia que buscan una casa independiente con jardín en lugar de un apartamento, cerca de un club de golf.',
  'Familles et acquéreurs de résidence secondaire qui souhaitent une maison indépendante avec jardin plutôt qu’un appartement, près d’un club de golf.',
  'Familien und Käufer eines Zweitwohnsitzes, die ein eigenständiges Haus mit Garten statt einer Wohnung suchen, in der Nähe eines Golfclubs.',
  'Семьи и покупатели второго жилья, которым нужен отдельный дом с садом, а не квартира, рядом с гольф-клубом.',
  'العائلات ومشترو المسكن الثاني الذين يريدون منزلًا مستقلًا بحديقة بدلًا من شقة، قرب نادي غولف.',
  'Gezinnen en kopers van een tweede woning die een zelfstandig huis met tuin willen in plaats van een appartement, dicht bij een golfclub.',
  'Rodziny i nabywcy drugiego domu, którzy szukają samodzielnego domu z ogrodem zamiast apartamentu, w pobliżu klubu golfowego.',
  'Familier og kjøpere av en andrebolig som ønsker et eget hus med hage i stedet for en leilighet, nær en golfklubb.',
  'Familjer och köpare av en andrabostad som vill ha ett eget hus med trädgård i stället för en lägenhet, nära en golfklubb.')

a('The homes are spread over a basement and two main floors, and ten of the 13 plans add a rooftop solarium. Gardens run from 11.74 to 160.30 sqm.',
  'Las viviendas se reparten en un sótano y dos plantas principales, y diez de los 13 planos añaden un solárium en la azotea. Los jardines van de #11.74 a #160.30 [m2].',
  'Les maisons se répartissent sur un sous-sol et deux niveaux principaux, et dix des 13 plans ajoutent un solarium sur le toit. Les jardins vont de #11.74 à #160.30 [m2].',
  'Die Häuser verteilen sich auf ein Untergeschoss und zwei Hauptgeschosse, und zehn der 13 Grundrisse haben zusätzlich ein Dach-Solarium. Die Gärten reichen von #11.74 bis #160.30 [m2].',
  'Дома расположены на цокольном этаже и двух основных этажах, а в десяти из 13 планировок есть ещё и солярий на крыше. Площадь садов — от #11.74 до #160.30 [m2].',
  'تتوزع المنازل على طابق سفلي وطابقين رئيسيين، وفي عشرة من المخططات الـ13 سوليريوم إضافي على السطح. وتتراوح مساحات الحدائق من #11.74 إلى #160.30 [m2].',
  'De woningen zijn verdeeld over een kelder en twee hoofdverdiepingen, en tien van de 13 plattegronden hebben daarbovenop een dakterras-solarium. De tuinen variëren van #11.74 tot #160.30 [m2].',
  'Domy rozkładają się na piwnicę i dwie główne kondygnacje, a dziesięć z 13 rzutów ma dodatkowo solarium na dachu. Ogrody mają od #11.74 do #160.30 [m2].',
  'Boligene er fordelt på en kjeller og to hovedetasjer, og ti av de 13 plantegningene har i tillegg en solterrasse på taket. Hagene varierer fra #11.74 til #160.30 [m2].',
  'Bostäderna fördelas på en källare och två huvudvåningar, och tio av de 13 planritningarna har dessutom en solterrass på taket. Trädgårdarna varierar från #11.74 till #160.30 [m2].')

a('The development is next to the Atalaya Golf & Country Club, close to commercial areas, and the developer’s page puts Puerto Banús within easy reach.',
  'La promoción está junto al Atalaya Golf & Country Club, cerca de zonas comerciales, y la página del promotor sitúa Puerto Banús a poca distancia.',
  'Le programme est à côté de l’Atalaya Golf & Country Club, près des zones commerciales, et la page du promoteur place Puerto Banús à proximité.',
  'Die Anlage liegt neben dem Atalaya Golf & Country Club, in der Nähe von Einkaufsbereichen, und die Seite des Bauträgers nennt Puerto Banús als leicht erreichbar.',
  'Комплекс находится рядом с Atalaya Golf & Country Club, недалеко от торговых зон, а на странице застройщика Пуэрто-Банус назван совсем рядом.',
  'يقع المشروع بجوار Atalaya Golf & Country Club وقرب المناطق التجارية، وتذكر صفحة المطوّر أن بويرتو بانوس قريب منه.',
  'Het project ligt naast de Atalaya Golf & Country Club, dicht bij winkelgebieden, en de pagina van de ontwikkelaar noemt Puerto Banús dichtbij.',
  'Inwestycja leży obok Atalaya Golf & Country Club, w pobliżu stref handlowych, a strona dewelopera podaje, że Puerto Banús jest niedaleko.',
  'Prosjektet ligger ved siden av Atalaya Golf & Country Club, nær kommersielle områder, og utbyggerens side oppgir at Puerto Banús er like i nærheten.',
  'Projektet ligger intill Atalaya Golf & Country Club, nära kommersiella områden, och exploatörens sida anger att Puerto Banús ligger nära.')

a('Why check the details', 'Por qué revisar los detalles', 'Pourquoi vérifier les détails', 'Warum die Details prüfen', 'Зачем проверять детали', 'لماذا نراجع التفاصيل', 'Waarom de details controleren', 'Dlaczego sprawdzamy szczegóły', 'Hvorfor sjekke detaljene', 'Varför kontrollera detaljerna')
a('The developer’s sources disagree on a few figures, including the bedroom count of two homes. We list them on this page and confirm each one in writing.',
  'Las fuentes del promotor no coinciden en algunas cifras, entre ellas el número de dormitorios de dos viviendas. Las indicamos en esta página y confirmamos cada una por escrito.',
  'Les sources du promoteur divergent sur quelques chiffres, dont le nombre de chambres de deux maisons. Nous les indiquons sur cette page et confirmons chacune par écrit.',
  'Die Quellen des Bauträgers widersprechen sich bei einigen Angaben, darunter die Zahl der Schlafzimmer bei zwei Häusern. Wir nennen sie auf dieser Seite und bestätigen jede schriftlich.',
  'Источники застройщика расходятся по нескольким показателям, включая число спален у двух домов. Мы указываем их на этой странице и подтверждаем каждый в письменном виде.',
  'تختلف مصادر المطوّر في بعض الأرقام، ومنها عدد غرف النوم في منزلين. نذكرها في هذه الصفحة ونؤكد كل رقم منها كتابةً.',
  'De bronnen van de ontwikkelaar verschillen op enkele punten, waaronder het aantal slaapkamers van twee woningen. Wij vermelden ze op deze pagina en bevestigen elk punt schriftelijk.',
  'Źródła dewelopera różnią się w kilku liczbach, w tym w liczbie sypialni w dwóch domach. Podajemy je na tej stronie i potwierdzamy każdą na piśmie.',
  'Utbyggerens kilder er uenige om noen tall, blant annet antall soverom i to boliger. Vi oppgir dem på denne siden og bekrefter hvert enkelt skriftlig.',
  'Exploatörens källor skiljer sig åt på några siffror, bland annat antalet sovrum i två bostäder. Vi anger dem på den här sidan och bekräftar var och en skriftligen.')

# ---------------------------------------------------------------- architecture
a('Contemporary houses, <em>built in pairs</em>',
  'Casas contemporáneas, <em>construidas por parejas</em>',
  'Maisons contemporaines, <em>construites par deux</em>',
  'Zeitgenössische Häuser, <em>paarweise gebaut</em>',
  'Современные дома, <em>построенные парами</em>',
  'منازل معاصرة، <em>مبنية في أزواج</em>',
  'Eigentijdse huizen, <em>in paren gebouwd</em>',
  'Nowoczesne domy, <em>budowane parami</em>',
  'Moderne hus, <em>bygget i par</em>',
  'Moderna hus, <em>byggda i par</em>')

a('The developer describes the homes as contemporary semi-detached villas. The site model on the plans shows them built in pairs that share a party wall, and the renders show white houses with a grey upper floor and a pergola over the rooftop terrace.',
  'El promotor describe las viviendas como villas pareadas de estilo contemporáneo. La maqueta de implantación que aparece en los planos las muestra construidas por parejas que comparten una pared medianera, y las recreaciones muestran casas blancas con una planta superior gris y una pérgola sobre la terraza de la azotea.',
  'Le promoteur décrit les maisons comme des villas jumelées de style contemporain. La maquette d’implantation qui figure sur les plans les montre construites par deux, avec un mur mitoyen commun, et les images de synthèse montrent des maisons blanches à l’étage gris, avec une pergola au-dessus de la terrasse du toit.',
  'Der Bauträger beschreibt die Häuser als zeitgenössische Doppelhaushälften. Das Lagemodell auf den Plänen zeigt sie paarweise gebaut, mit einer gemeinsamen Trennwand, und die Visualisierungen zeigen weiße Häuser mit grauem Obergeschoss und einer Pergola über der Dachterrasse.',
  'Застройщик описывает дома как современные парные виллы. На макете застройки на планах они показаны парами с общей стеной, а на визуализациях — белые дома с серым верхним этажом и перголой над террасой на крыше.',
  'يصف المطوّر المنازل بأنها فيلات شبه منفصلة بتصميم معاصر. ويُظهر نموذج الموقع على المخططات أنها مبنية في أزواج تتشارك جدارًا فاصلًا، وتُظهر التصاميم منازل بيضاء بطابق علوي رمادي وبرغولا فوق تراس السطح.',
  'De ontwikkelaar beschrijft de woningen als eigentijdse halfvrijstaande villa’s. Het situatiemodel op de plannen toont ze in paren gebouwd die een scheidingsmuur delen, en de renders tonen witte huizen met een grijze bovenverdieping en een pergola boven het dakterras.',
  'Deweloper opisuje domy jako nowoczesne wille bliźniacze. Model sytuacyjny na planach pokazuje je zbudowane parami ze wspólną ścianą, a wizualizacje przedstawiają białe domy z szarym piętrem i pergolą nad tarasem na dachu.',
  'Utbyggeren beskriver boligene som moderne tomannsvillaer. Situasjonsmodellen på tegningene viser dem bygget i par med en felles skillevegg, og visualiseringene viser hvite hus med grå overetasje og en pergola over takterrassen.',
  'Exploatören beskriver bostäderna som moderna parvillor. Situationsmodellen på ritningarna visar dem byggda i par med en gemensam skiljevägg, och visualiseringarna visar vita hus med grå övervåning och en pergola över takterrassen.')

a('The plans show the living room and kitchen opening onto a covered terrace on one floor, the three bedrooms on another (the lower of the two main floors on F1V37 and F1V38), and a basement with a cellar room, a laundry and a bathroom.',
  'Los planos muestran el salón y la cocina abiertos a una terraza cubierta en una planta, los tres dormitorios en otra (la inferior de las dos plantas principales en F1V37 y F1V38) y un sótano con una bodega, un lavadero y un baño.',
  'Les plans montrent le séjour et la cuisine ouverts sur une terrasse couverte à un niveau, les trois chambres à un autre (le plus bas des deux niveaux principaux pour F1V37 et F1V38) et un sous-sol avec une cave, une buanderie et une salle de bains.',
  'Die Pläne zeigen Wohnzimmer und Küche mit Zugang zu einer überdachten Terrasse auf einer Ebene, die drei Schlafzimmer auf einer anderen (bei F1V37 und F1V38 auf der unteren der beiden Hauptebenen) sowie ein Untergeschoss mit Kellerraum, Waschküche und Bad.',
  'На планах гостиная и кухня с выходом на крытую террасу находятся на одном этаже, три спальни — на другом (у F1V37 и F1V38 это нижний из двух основных этажей), а в цоколе — подвальное помещение, прачечная и ванная комната.',
  'تُظهر المخططات غرفة المعيشة والمطبخ مفتوحين على تراس مغطى في طابق، وغرف النوم الثلاث في طابق آخر (وهو الأدنى من الطابقين الرئيسيين في F1V37 وF1V38)، وطابقًا سفليًا فيه غرفة قبو وغرفة غسيل وحمّام.',
  'De plannen tonen de woonkamer en keuken met een overdekt terras op één verdieping, de drie slaapkamers op een andere (de onderste van de twee hoofdverdiepingen bij F1V37 en F1V38), en een kelder met een kelderruimte, een wasruimte en een badkamer.',
  'Rzuty pokazują salon i kuchnię otwarte na zadaszony taras na jednej kondygnacji, trzy sypialnie na innej (w F1V37 i F1V38 na niższej z dwóch głównych kondygnacji) oraz piwnicę z pomieszczeniem piwnicznym, pralnią i łazienką.',
  'Plantegningene viser stuen og kjøkkenet med utgang til en overbygd terrasse i én etasje, de tre soverommene i en annen (den nederste av de to hovedetasjene i F1V37 og F1V38), og en kjeller med et kjellerrom, et vaskerom og et bad.',
  'Planritningarna visar vardagsrummet och köket med utgång till en övertäckt terrass på ett plan, de tre sovrummen på ett annat (det nedre av de två huvudplanen i F1V37 och F1V38), och en källare med ett förrådsrum, en tvättstuga och ett badrum.')

a('Semi-detached or terraced', 'Pareada o adosada', 'Jumelée ou en bande', 'Doppelhaushälfte oder Reihenhaus', 'Парный дом или таунхаус', 'شبه منفصل أم متلاصق', 'Halfvrijstaand of rijwoning', 'Bliźniak czy szeregowiec', 'Tomannsbolig eller rekkehus', 'Parhus eller radhus')
a('The developer’s page says semi-detached (“pareadas”), while its price table labels every home “Adosado”, the Spanish word for a terraced or attached house. The plans’ site model shows pairs of homes, so we call them semi-detached.',
  'La página del promotor dice «pareadas», mientras que su tabla de precios califica todas las viviendas de «adosado», el término español para una casa en hilera o adosada. La maqueta de implantación de los planos muestra parejas de viviendas, por eso las llamamos pareadas.',
  'La page du promoteur dit « pareadas » (jumelées), alors que son tableau de prix qualifie toutes les maisons d’« Adosado », le terme espagnol pour une maison en bande ou accolée. La maquette d’implantation des plans montre des maisons par deux, c’est pourquoi nous les disons jumelées.',
  'Die Seite des Bauträgers sagt „pareadas“ (Doppelhaushälften), während seine Preistabelle jedes Haus als „Adosado“ bezeichnet, das spanische Wort für ein Reihen- oder Anbauhaus. Das Lagemodell der Pläne zeigt Paare von Häusern, daher nennen wir sie Doppelhaushälften.',
  'На странице застройщика написано «pareadas» (парные), а в его таблице цен все дома обозначены как «Adosado» — по-испански это дом в ряду или пристроенный дом. На макете застройки на планах дома показаны парами, поэтому мы называем их парными.',
  'تقول صفحة المطوّر «pareadas» أي شبه منفصلة، بينما يصف جدول الأسعار كل المنازل بأنها «Adosado»، وهي الكلمة الإسبانية للمنزل المتلاصق ضمن صف. ويُظهر نموذج الموقع في المخططات أزواجًا من المنازل، لذلك نسميها شبه منفصلة.',
  'De pagina van de ontwikkelaar zegt “pareadas” (halfvrijstaand), terwijl de prijstabel elke woning “Adosado” noemt, het Spaanse woord voor een rij- of aaneengebouwd huis. Het situatiemodel van de plannen toont paren woningen, daarom noemen wij ze halfvrijstaand.',
  'Strona dewelopera podaje „pareadas” (bliźniaki), natomiast jego tabela cen opisuje każdy dom jako „Adosado”, czyli po hiszpańsku dom szeregowy lub przylegający. Model sytuacyjny na planach pokazuje domy w parach, dlatego nazywamy je bliźniakami.',
  'Utbyggerens side sier «pareadas» (tomannsbolig), mens pristabellen kaller hver bolig «Adosado», det spanske ordet for et rekkehus eller sammenbygd hus. Situasjonsmodellen på tegningene viser boliger i par, så vi kaller dem tomannsboliger.',
  'Exploatörens sida säger ”pareadas” (parhus), medan pristabellen kallar varje bostad ”Adosado”, det spanska ordet för ett radhus eller sammanbyggt hus. Situationsmodellen på ritningarna visar bostäder i par, så vi kallar dem parhus.')

a('A basement and two main floors on every plan, with a rooftop solarium on ten of the 13. Homes F1V35, F1V37 and F3V1 show no solarium on the sheets we hold.',
  'Un sótano y dos plantas principales en todos los planos, con un solárium en la azotea en diez de los 13. Las viviendas F1V35, F1V37 y F3V1 no muestran solárium en las hojas de que disponemos.',
  'Un sous-sol et deux niveaux principaux sur chaque plan, avec un solarium sur le toit pour dix des 13. Les maisons F1V35, F1V37 et F3V1 ne montrent pas de solarium sur les feuilles dont nous disposons.',
  'Auf jedem Grundriss ein Untergeschoss und zwei Hauptgeschosse, bei zehn der 13 mit einem Dach-Solarium. Bei den Häusern F1V35, F1V37 und F3V1 ist auf den uns vorliegenden Blättern kein Solarium zu sehen.',
  'На каждой планировке цоколь и два основных этажа, а у десяти из 13 ещё и солярий на крыше. На имеющихся у нас листах солярий не показан у домов F1V35, F1V37 и F3V1.',
  'في كل مخطط طابق سفلي وطابقان رئيسيان، مع سوليريوم على السطح في عشرة من الـ13. ولا يظهر سوليريوم للمنازل F1V35 وF1V37 وF3V1 في الأوراق المتوفرة لدينا.',
  'Op elke plattegrond een kelder en twee hoofdverdiepingen, met bij tien van de 13 een solarium op het dak. Bij de woningen F1V35, F1V37 en F3V1 is op de bladen die wij hebben geen solarium te zien.',
  'Na każdym rzucie piwnica i dwie główne kondygnacje, a w dziesięciu z 13 także solarium na dachu. W domach F1V35, F1V37 i F3V1 na posiadanych przez nas arkuszach nie ma solarium.',
  'En kjeller og to hovedetasjer på hver plantegning, med en solterrasse på taket på ti av de 13. Boligene F1V35, F1V37 og F3V1 viser ingen solterrasse på arkene vi har.',
  'En källare och två huvudvåningar på varje planritning, med en solterrass på taket på tio av de 13. Bostäderna F1V35, F1V37 och F3V1 visar ingen solterrass på arken vi har.')

a('Basement', 'Sótano', 'Sous-sol', 'Untergeschoss', 'Цокольный этаж', 'الطابق السفلي', 'Kelder', 'Piwnica', 'Kjeller', 'Källare')
a('Every plan shows a basement with a cellar room (“bodega”), a laundry and a bathroom. On F1V35 and F3V1 it also holds a garage for two cars.',
  'Todos los planos muestran un sótano con una bodega, un lavadero y un baño. En F1V35 y F3V1 también hay un garaje para dos coches.',
  'Chaque plan montre un sous-sol avec une cave (« bodega »), une buanderie et une salle de bains. Pour F1V35 et F3V1, il comprend aussi un garage pour deux voitures.',
  'Jeder Grundriss zeigt ein Untergeschoss mit einem Kellerraum („Bodega“), einer Waschküche und einem Bad. Bei F1V35 und F3V1 gibt es dort außerdem eine Garage für zwei Autos.',
  'На каждой планировке показан цоколь с подвальным помещением («bodega»), прачечной и ванной комнатой. У F1V35 и F3V1 там же находится гараж на два автомобиля.',
  'يُظهر كل مخطط طابقًا سفليًا فيه غرفة قبو («bodega») وغرفة غسيل وحمّام. وفي F1V35 وF3V1 يضم هذا الطابق أيضًا مرآبًا لسيارتين.',
  'Elke plattegrond toont een kelder met een kelderruimte (“bodega”), een wasruimte en een badkamer. Bij F1V35 en F3V1 bevindt zich daar ook een garage voor twee auto’s.',
  'Każdy rzut pokazuje piwnicę z pomieszczeniem piwnicznym („bodega”), pralnią i łazienką. W F1V35 i F3V1 mieści się tam także garaż na dwa samochody.',
  'Hver plantegning viser en kjeller med et kjellerrom («bodega»), et vaskerom og et bad. I F1V35 og F3V1 er det også en garasje for to biler der.',
  'Varje planritning visar en källare med ett förrådsrum (”bodega”), en tvättstuga och ett badrum. I F1V35 och F3V1 finns där också ett garage för två bilar.')

a('Extras on two plans', 'Extras en dos planos', 'Équipements sur deux plans', 'Extras auf zwei Plänen', 'Дополнения на двух планах', 'إضافات في مخططين', 'Extra’s op twee plannen', 'Dodatki na dwóch rzutach', 'Tillegg på to tegninger', 'Tillägg på två ritningar')
a('The plan of FIIIV7 shows a private pool of 12.2 sqm in the garden, and the plan of F3V1 shows a jacuzzi of 3.8 sqm on the terrace.',
  'El plano de FIIIV7 muestra una piscina privada de #12.2 [m2] en el jardín, y el de F3V1 un jacuzzi de #3.8 [m2] en la terraza.',
  'Le plan de FIIIV7 montre une piscine privée de #12.2 [m2] dans le jardin, et celui de F3V1 un jacuzzi de #3.8 [m2] sur la terrasse.',
  'Der Plan von FIIIV7 zeigt einen privaten Pool von #12.2 [m2] im Garten, der von F3V1 einen Whirlpool von #3.8 [m2] auf der Terrasse.',
  'На плане FIIIV7 показан частный бассейн площадью #12.2 [m2] в саду, а на плане F3V1 — джакузи площадью #3.8 [m2] на террасе.',
  'يُظهر مخطط FIIIV7 مسبحًا خاصًا بمساحة #12.2 [m2] في الحديقة، ويُظهر مخطط F3V1 جاكوزي بمساحة #3.8 [m2] على التراس.',
  'Het plan van FIIIV7 toont een privézwembad van #12.2 [m2] in de tuin, en dat van F3V1 een jacuzzi van #3.8 [m2] op het terras.',
  'Rzut FIIIV7 pokazuje prywatny basen o powierzchni #12.2 [m2] w ogrodzie, a rzut F3V1 jacuzzi o powierzchni #3.8 [m2] na tarasie.',
  'Plantegningen av FIIIV7 viser et privat basseng på #12.2 [m2] i hagen, og plantegningen av F3V1 viser en jacuzzi på #3.8 [m2] på terrassen.',
  'Planritningen för FIIIV7 visar en privat pool på #12.2 [m2] i trädgården, och planritningen för F3V1 visar en jacuzzi på #3.8 [m2] på terrassen.')

# ---------------------------------------------------------------- residences
a('Three groups of homes, <em>one development</em>',
  'Tres grupos de viviendas, <em>una sola promoción</em>', 'Trois groupes de maisons, <em>un seul programme</em>', 'Drei Gruppen von Häusern, <em>eine Anlage</em>',
  'Три группы домов, <em>один комплекс</em>', 'ثلاث مجموعات من المنازل، <em>مشروع واحد</em>', 'Drie groepen woningen, <em>één project</em>',
  'Trzy grupy domów, <em>jedna inwestycja</em>', 'Tre grupper boliger, <em>ett prosjekt</em>', 'Tre grupper av bostäder, <em>ett projekt</em>')
a('The 13 homes on the price list come from three groups of plans. The table below lists each one with its price.',
  'Las 13 viviendas de la lista de precios proceden de tres grupos de planos. La tabla siguiente recoge cada una con su precio.',
  'Les 13 maisons de la liste de prix relèvent de trois groupes de plans. Le tableau ci-dessous présente chacune avec son prix.',
  'Die 13 Häuser der Preisliste stammen aus drei Gruppen von Plänen. Die folgende Tabelle führt jedes mit seinem Preis auf.',
  'Тринадцать домов из прайс-листа относятся к трём группам планов. В таблице ниже указан каждый из них с ценой.',
  'تنتمي المنازل الـ13 الواردة في قائمة الأسعار إلى ثلاث مجموعات من المخططات. ويُدرج الجدول أدناه كل منزل مع سعره.',
  'De 13 woningen op de prijslijst komen uit drie groepen plannen. De onderstaande tabel toont elke woning met haar prijs.',
  'Trzynaście domów z cennika pochodzi z trzech grup planów. Poniższa tabela przedstawia każdy z nich wraz z ceną.',
  'De 13 boligene på prislisten kommer fra tre grupper av planer. Tabellen nedenfor viser hver enkelt med pris.',
  'De 13 bostäderna på prislistan kommer från tre grupper av planer. Tabellen nedan visar var och en med sitt pris.')
a('Phase 1 homes', 'Viviendas de la fase 1', 'Maisons de la phase 1', 'Häuser der Phase 1', 'Дома первой очереди', 'منازل المرحلة 1', 'Woningen van fase 1', 'Domy fazy 1', 'Boliger i fase 1', 'Bostäder i fas 1')
a('Eight homes, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 and F1V46, with three bedrooms on the plans.',
  'Ocho viviendas, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 y F1V46, con tres dormitorios en los planos.',
  'Huit maisons, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 et F1V46, avec trois chambres sur les plans.',
  'Acht Häuser, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 und F1V46, mit drei Schlafzimmern auf den Plänen.',
  'Восемь домов — F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 и F1V46 — с тремя спальнями на планах.',
  'ثمانية منازل هي F1V15 وF1V20 وF1V23 وF1V24 وF1V35 وF1V37 وF1V38 وF1V46، بثلاث غرف نوم في المخططات.',
  'Acht woningen, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 en F1V46, met drie slaapkamers op de plannen.',
  'Osiem domów, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 i F1V46, z trzema sypialniami na rzutach.',
  'Åtte boliger, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 og F1V46, med tre soverom på tegningene.',
  'Åtta bostäder, F1V15, F1V20, F1V23, F1V24, F1V35, F1V37, F1V38 och F1V46, med tre sovrum på ritningarna.')
a('Built areas of 171.55 to 206.92 sqm, terraces of 41.46 to 107.22 sqm and gardens of 11.74 to 120.56 sqm.',
  'Superficies construidas de #171.55 a #206.92 [m2], terrazas de #41.46 a #107.22 [m2] y jardines de #11.74 a #120.56 [m2].',
  'Surfaces construites de #171.55 à #206.92 [m2], terrasses de #41.46 à #107.22 [m2] et jardins de #11.74 à #120.56 [m2].',
  'Bebaute Flächen von #171.55 bis #206.92 [m2], Terrassen von #41.46 bis #107.22 [m2] und Gärten von #11.74 bis #120.56 [m2].',
  'Площадь застройки — от #171.55 до #206.92 [m2], террасы — от #41.46 до #107.22 [m2], сады — от #11.74 до #120.56 [m2].',
  'مساحات مبنية من #171.55 إلى #206.92 [m2]، وتراسات من #41.46 إلى #107.22 [m2]، وحدائق من #11.74 إلى #120.56 [m2].',
  'Bebouwde oppervlakten van #171.55 tot #206.92 [m2], terrassen van #41.46 tot #107.22 [m2] en tuinen van #11.74 tot #120.56 [m2].',
  'Powierzchnie zabudowy od #171.55 do #206.92 [m2], tarasy od #41.46 do #107.22 [m2] i ogrody od #11.74 do #120.56 [m2].',
  'Bebygd areal på #171.55 til #206.92 [m2], terrasser på #41.46 til #107.22 [m2] og hager på #11.74 til #120.56 [m2].',
  'Byggytor på #171.55 till #206.92 [m2], terrasser på #41.46 till #107.22 [m2] och trädgårdar på #11.74 till #120.56 [m2].')
a('Prices run from EUR 800,000 to EUR 950,000.',
  'Los precios van de €800000 a €950000.', 'Les prix vont de €800000 à €950000.', 'Die Preise reichen von €800000 bis €950000.',
  'Цены — от €800000 до €950000.', 'تتراوح الأسعار من €800000 إلى €950000.', 'De prijzen lopen van €800000 tot €950000.',
  'Ceny wahają się od €800000 do €950000.', 'Prisene går fra €800000 til €950000.', 'Priserna går från €800000 till €950000.')
a('Phase 2 homes', 'Viviendas de la fase 2', 'Maisons de la phase 2', 'Häuser der Phase 2', 'Дома второй очереди', 'منازل المرحلة 2', 'Woningen van fase 2', 'Domy fazy 2', 'Boliger i fase 2', 'Bostäder i fas 2')
a('Three homes, F2V19, F2V20 and F2V42, with a basement, two main floors with three bedrooms and a rooftop solarium.',
  'Tres viviendas, F2V19, F2V20 y F2V42, con sótano, dos plantas principales con tres dormitorios y un solárium en la azotea.',
  'Trois maisons, F2V19, F2V20 et F2V42, avec un sous-sol, deux niveaux principaux comptant trois chambres et un solarium sur le toit.',
  'Drei Häuser, F2V19, F2V20 und F2V42, mit Untergeschoss, zwei Hauptgeschossen mit drei Schlafzimmern und einem Dach-Solarium.',
  'Три дома — F2V19, F2V20 и F2V42 — с цоколем, двумя основными этажами с тремя спальнями и солярием на крыше.',
  'ثلاثة منازل هي F2V19 وF2V20 وF2V42، بطابق سفلي وطابقين رئيسيين فيهما ثلاث غرف نوم وسوليريوم على السطح.',
  'Drie woningen, F2V19, F2V20 en F2V42, met een kelder, twee hoofdverdiepingen met drie slaapkamers en een solarium op het dak.',
  'Trzy domy, F2V19, F2V20 i F2V42, z piwnicą, dwiema głównymi kondygnacjami z trzema sypialniami i solarium na dachu.',
  'Tre boliger, F2V19, F2V20 og F2V42, med kjeller, to hovedetasjer med tre soverom og en solterrasse på taket.',
  'Tre bostäder, F2V19, F2V20 och F2V42, med källare, två huvudvåningar med tre sovrum och en solterrass på taket.')
a('Built areas of 176.66 to 181.87 sqm, terraces of 77.38 to 78.43 sqm and gardens of 131.09 to 149.00 sqm.',
  'Superficies construidas de #176.66 a #181.87 [m2], terrazas de #77.38 a #78.43 [m2] y jardines de #131.09 a #149.00 [m2].',
  'Surfaces construites de #176.66 à #181.87 [m2], terrasses de #77.38 à #78.43 [m2] et jardins de #131.09 à #149.00 [m2].',
  'Bebaute Flächen von #176.66 bis #181.87 [m2], Terrassen von #77.38 bis #78.43 [m2] und Gärten von #131.09 bis #149.00 [m2].',
  'Площадь застройки — от #176.66 до #181.87 [m2], террасы — от #77.38 до #78.43 [m2], сады — от #131.09 до #149.00 [m2].',
  'مساحات مبنية من #176.66 إلى #181.87 [m2]، وتراسات من #77.38 إلى #78.43 [m2]، وحدائق من #131.09 إلى #149.00 [m2].',
  'Bebouwde oppervlakten van #176.66 tot #181.87 [m2], terrassen van #77.38 tot #78.43 [m2] en tuinen van #131.09 tot #149.00 [m2].',
  'Powierzchnie zabudowy od #176.66 do #181.87 [m2], tarasy od #77.38 do #78.43 [m2] i ogrody od #131.09 do #149.00 [m2].',
  'Bebygd areal på #176.66 til #181.87 [m2], terrasser på #77.38 til #78.43 [m2] og hager på #131.09 til #149.00 [m2].',
  'Byggytor på #176.66 till #181.87 [m2], terrasser på #77.38 till #78.43 [m2] och trädgårdar på #131.09 till #149.00 [m2].')
a('Prices run from EUR 850,000 to EUR 900,000.',
  'Los precios van de €850000 a €900000.', 'Les prix vont de €850000 à €900000.', 'Die Preise reichen von €850000 bis €900000.',
  'Цены — от €850000 до €900000.', 'تتراوح الأسعار من €850000 إلى €900000.', 'De prijzen lopen van €850000 tot €900000.',
  'Ceny wahają się od €850000 do €900000.', 'Prisene går fra €850000 til €900000.', 'Priserna går från €850000 till €900000.')
a('Phase 3 homes', 'Viviendas de la fase 3', 'Maisons de la phase 3', 'Häuser der Phase 3', 'Дома третьей очереди', 'منازل المرحلة 3', 'Woningen van fase 3', 'Domy fazy 3', 'Boliger i fase 3', 'Bostäder i fas 3')
a('Two homes, F3V1 and FIIIV7, with three bedrooms on the plans, a basement with a cellar and a laundry, and larger terraces.',
  'Dos viviendas, F3V1 y FIIIV7, con tres dormitorios en los planos, un sótano con bodega y lavadero, y terrazas más amplias.',
  'Deux maisons, F3V1 et FIIIV7, avec trois chambres sur les plans, un sous-sol avec cave et buanderie, et de plus grandes terrasses.',
  'Zwei Häuser, F3V1 und FIIIV7, mit drei Schlafzimmern auf den Plänen, einem Untergeschoss mit Kellerraum und Waschküche sowie größeren Terrassen.',
  'Два дома — F3V1 и FIIIV7 — с тремя спальнями на планах, цоколем с подвальным помещением и прачечной и более просторными террасами.',
  'منزلان هما F3V1 وFIIIV7، بثلاث غرف نوم في المخططات، وطابق سفلي فيه غرفة قبو وغرفة غسيل، وتراسات أوسع.',
  'Twee woningen, F3V1 en FIIIV7, met drie slaapkamers op de plannen, een kelder met een kelderruimte en een wasruimte, en grotere terrassen.',
  'Dwa domy, F3V1 i FIIIV7, z trzema sypialniami na rzutach, piwnicą z pomieszczeniem piwnicznym i pralnią oraz większymi tarasami.',
  'To boliger, F3V1 og FIIIV7, med tre soverom på tegningene, en kjeller med kjellerrom og vaskerom, og større terrasser.',
  'Två bostäder, F3V1 och FIIIV7, med tre sovrum på ritningarna, en källare med förrådsrum och tvättstuga, och större terrasser.')
a('F3V1 has 186.00 sqm built, an 89.60 sqm terrace and a 107.80 sqm garden, and FIIIV7 has 198.00 sqm built, a 170.70 sqm terrace and a 160.30 sqm garden.',
  'F3V1 tiene #186.00 [m2] construidos, una terraza de #89.60 [m2] y un jardín de #107.80 [m2], y FIIIV7 tiene #198.00 [m2] construidos, una terraza de #170.70 [m2] y un jardín de #160.30 [m2].',
  'F3V1 compte #186.00 [m2] construits, une terrasse de #89.60 [m2] et un jardin de #107.80 [m2], et FIIIV7 compte #198.00 [m2] construits, une terrasse de #170.70 [m2] et un jardin de #160.30 [m2].',
  'F3V1 hat #186.00 [m2] bebaute Fläche, eine Terrasse von #89.60 [m2] und einen Garten von #107.80 [m2], FIIIV7 hat #198.00 [m2] bebaute Fläche, eine Terrasse von #170.70 [m2] und einen Garten von #160.30 [m2].',
  'У F3V1 площадь застройки #186.00 [m2], терраса #89.60 [m2] и сад #107.80 [m2], а у FIIIV7 — #198.00 [m2], терраса #170.70 [m2] и сад #160.30 [m2].',
  'مساحة F3V1 المبنية #186.00 [m2] وتراسه #89.60 [m2] وحديقته #107.80 [m2]، ومساحة FIIIV7 المبنية #198.00 [m2] وتراسه #170.70 [m2] وحديقته #160.30 [m2].',
  'F3V1 heeft #186.00 [m2] bebouwd, een terras van #89.60 [m2] en een tuin van #107.80 [m2], en FIIIV7 heeft #198.00 [m2] bebouwd, een terras van #170.70 [m2] en een tuin van #160.30 [m2].',
  'F3V1 ma #186.00 [m2] zabudowy, taras o powierzchni #89.60 [m2] i ogród o powierzchni #107.80 [m2], a FIIIV7 ma #198.00 [m2] zabudowy, taras o powierzchni #170.70 [m2] i ogród o powierzchni #160.30 [m2].',
  'F3V1 har #186.00 [m2] bebygd areal, en terrasse på #89.60 [m2] og en hage på #107.80 [m2], og FIIIV7 har #198.00 [m2] bebygd areal, en terrasse på #170.70 [m2] og en hage på #160.30 [m2].',
  'F3V1 har #186.00 [m2] byggyta, en terrass på #89.60 [m2] och en trädgård på #107.80 [m2], och FIIIV7 har #198.00 [m2] byggyta, en terrass på #170.70 [m2] och en trädgård på #160.30 [m2].')
a('Prices are EUR 775,000 for F3V1 and EUR 908,600 for FIIIV7.',
  'Los precios son €775000 para F3V1 y €908600 para FIIIV7.', 'Les prix sont de €775000 pour F3V1 et de €908600 pour FIIIV7.', 'Die Preise betragen €775000 für F3V1 und €908600 für FIIIV7.',
  'Цены — €775000 для F3V1 и €908600 для FIIIV7.', 'السعر €775000 لـF3V1 و€908600 لـFIIIV7.', 'De prijzen zijn €775000 voor F3V1 en €908600 voor FIIIV7.',
  'Ceny wynoszą €775000 dla F3V1 i €908600 dla FIIIV7.', 'Prisene er €775000 for F3V1 og €908600 for FIIIV7.', 'Priserna är €775000 för F3V1 och €908600 för FIIIV7.')

# ---------------------------------------------------------------- lifestyle
a('Gardens, <em>two pools</em> and the golf club next door',
  'Jardines, <em>dos piscinas</em> y el club de golf al lado', 'Des jardins, <em>deux piscines</em> et le club de golf voisin', 'Gärten, <em>zwei Pools</em> und der Golfclub nebenan',
  'Сады, <em>два бассейна</em> и гольф-клуб по соседству', 'حدائق، <em>ومسبحان</em>، ونادي الغولف المجاور', 'Tuinen, <em>twee zwembaden</em> en de golfclub ernaast',
  'Ogrody, <em>dwa baseny</em> i klub golfowy tuż obok', 'Hager, <em>to basseng</em> og golfklubben ved siden av', 'Trädgårdar, <em>två pooler</em> och golfklubben intill')
a('Life here is outdoors, between the private garden, the communal pools and the golf club.',
  'La vida aquí transcurre al aire libre, entre el jardín privado, las piscinas comunitarias y el club de golf.',
  'La vie ici se passe en plein air, entre le jardin privé, les piscines communes et le club de golf.',
  'Das Leben findet hier im Freien statt, zwischen privatem Garten, Gemeinschaftspools und Golfclub.',
  'Жизнь здесь проходит на свежем воздухе: между частным садом, общими бассейнами и гольф-клубом.',
  'الحياة هنا في الهواء الطلق، بين الحديقة الخاصة والمسبحين المشتركين ونادي الغولف.',
  'Het leven speelt zich hier buiten af, tussen de privétuin, de gemeenschappelijke zwembaden en de golfclub.',
  'Życie toczy się tu na świeżym powietrzu, między prywatnym ogrodem, wspólnymi basenami i klubem golfowym.',
  'Livet her foregår utendørs, mellom den private hagen, fellesbassengene og golfklubben.',
  'Livet här är utomhus, mellan den privata trädgården, de gemensamma poolerna och golfklubben.')
a('Every home has a terrace and a garden, on the developer’s own description and on every plan.',
  'Cada vivienda tiene una terraza y un jardín, según la descripción del propio promotor y en todos los planos.',
  'Chaque maison a une terrasse et un jardin, selon la description du promoteur lui-même et sur tous les plans.',
  'Jedes Haus hat eine Terrasse und einen Garten, nach der Beschreibung des Bauträgers selbst und auf jedem Grundriss.',
  'У каждого дома есть терраса и сад — так описывает застройщик, и это видно на каждой планировке.',
  'لكل منزل تراس وحديقة، بحسب وصف المطوّر نفسه وفي كل مخطط.',
  'Elke woning heeft een terras en een tuin, volgens de eigen beschrijving van de ontwikkelaar en op elke plattegrond.',
  'Każdy dom ma taras i ogród, zgodnie z opisem samego dewelopera i na każdym rzucie.',
  'Hver bolig har en terrasse og en hage, ifølge utbyggerens egen beskrivelse og på hver plantegning.',
  'Varje bostad har en terrass och en trädgård, enligt exploatörens egen beskrivning och på varje planritning.')
a('Two saltwater pools in the landscaped communal gardens, one of them for children with a beach-style entry.',
  'Dos piscinas de agua salada en los jardines comunitarios, una de ellas infantil y con acceso tipo playa.',
  'Deux piscines à l’eau salée dans les jardins communs paysagers, dont une pour enfants avec un accès de type plage.',
  'Zwei Salzwasserpools in den gepflegten Gemeinschaftsgärten, einer davon für Kinder mit strandartigem Einstieg.',
  'Два бассейна с солёной водой в благоустроенных общих садах, один из них детский, с пологим входом наподобие пляжа.',
  'مسبحان بالمياه المالحة في الحدائق المشتركة المنسّقة، أحدهما للأطفال بمدخل على شكل شاطئ.',
  'Twee zoutwaterzwembaden in de aangelegde gemeenschappelijke tuinen, waarvan één voor kinderen met een strandachtige instap.',
  'Dwa baseny ze słoną wodą w zagospodarowanych wspólnych ogrodach, w tym jeden dla dzieci z wejściem w stylu plaży.',
  'To saltvannsbasseng i de opparbeidede fellesarealene, ett av dem for barn med strandlignende inngang.',
  'Två saltvattenpooler i de anlagda gemensamma trädgårdarna, varav en för barn med strandliknande entré.')
a('An open kitchen supplied furnished and fitted with branded appliances, on the developer’s own description.',
  'Una cocina abierta entregada amueblada y equipada con electrodomésticos de marca, según la descripción del propio promotor.',
  'Une cuisine ouverte livrée meublée et équipée d’électroménager de marque, selon la description du promoteur lui-même.',
  'Eine offene Küche, die möbliert und mit Markengeräten ausgestattet geliefert wird, nach der Beschreibung des Bauträgers selbst.',
  'Открытая кухня, которая поставляется меблированной и оснащённой техникой известных марок, — так её описывает застройщик.',
  'مطبخ مفتوح يُسلَّم مفروشًا ومجهزًا بأجهزة من علامات معروفة، بحسب وصف المطوّر نفسه.',
  'Een open keuken die gemeubileerd en met merkapparatuur wordt geleverd, volgens de eigen beschrijving van de ontwikkelaar.',
  'Otwarta kuchnia dostarczana umeblowana i wyposażona w sprzęt znanych marek, zgodnie z opisem samego dewelopera.',
  'Et åpent kjøkken som leveres møblert og utstyrt med merkevarehvitevarer, ifølge utbyggerens egen beskrivelse.',
  'Ett öppet kök som levereras möblerat och utrustat med märkesvitvaror, enligt exploatörens egen beskrivning.')
a('The development is next to the Atalaya Golf & Country Club.',
  'La promoción está junto al Atalaya Golf & Country Club.', 'Le programme est à côté de l’Atalaya Golf & Country Club.', 'Die Anlage liegt neben dem Atalaya Golf & Country Club.',
  'Комплекс находится рядом с Atalaya Golf & Country Club.', 'يقع المشروع بجوار Atalaya Golf & Country Club.', 'Het project ligt naast de Atalaya Golf & Country Club.',
  'Inwestycja leży obok Atalaya Golf & Country Club.', 'Prosjektet ligger ved siden av Atalaya Golf & Country Club.', 'Projektet ligger intill Atalaya Golf & Country Club.')

# ---------------------------------------------------------------- location
a('The homes are next to the Atalaya Golf & Country Club in Estepona, close to commercial areas, with Puerto Banús nearby, on the developer’s own description. The homes are described as facing views and the sun until sunset.',
  'Las viviendas están junto al Atalaya Golf & Country Club, en Estepona, cerca de zonas comerciales y con Puerto Banús a poca distancia, según la descripción del propio promotor. Se describen con buenas vistas y orientación para disfrutar del sol hasta el atardecer.',
  'Les maisons sont à côté de l’Atalaya Golf & Country Club, à Estepona, près des zones commerciales et avec Puerto Banús à proximité, selon la description du promoteur lui-même. Elles sont décrites comme bénéficiant de belles vues et d’une orientation permettant de profiter du soleil jusqu’au coucher.',
  'Die Häuser liegen neben dem Atalaya Golf & Country Club in Estepona, in der Nähe von Einkaufsbereichen und mit Puerto Banús in der Nähe, nach der Beschreibung des Bauträgers selbst. Sie werden mit Ausblick und einer Ausrichtung beschrieben, die Sonne bis zum Sonnenuntergang bietet.',
  'Дома находятся рядом с Atalaya Golf & Country Club в Эстепоне, недалеко от торговых зон, а Пуэрто-Банус расположен поблизости — так описывает застройщик. Дома описаны как имеющие хороший вид и ориентацию, позволяющую наслаждаться солнцем до заката.',
  'تقع المنازل بجوار Atalaya Golf & Country Club في إستيبونا، وقرب المناطق التجارية، وبويرتو بانوس قريب منها، بحسب وصف المطوّر نفسه. وتُوصف بأن لها إطلالات جيدة واتجاهًا يتيح التمتع بالشمس حتى الغروب.',
  'De woningen liggen naast de Atalaya Golf & Country Club in Estepona, dicht bij winkelgebieden en met Puerto Banús in de buurt, volgens de eigen beschrijving van de ontwikkelaar. Ze worden beschreven met mooi uitzicht en een ligging waarmee je tot zonsondergang van de zon geniet.',
  'Domy leżą obok Atalaya Golf & Country Club w Esteponie, w pobliżu stref handlowych i z Puerto Banús w niewielkiej odległości, zgodnie z opisem samego dewelopera. Opisano je jako mające dobre widoki i usytuowanie pozwalające cieszyć się słońcem do zachodu.',
  'Boligene ligger ved siden av Atalaya Golf & Country Club i Estepona, nær kommersielle områder og med Puerto Banús i nærheten, ifølge utbyggerens egen beskrivelse. De beskrives med god utsikt og en orientering som gir sol helt til solnedgang.',
  'Bostäderna ligger intill Atalaya Golf & Country Club i Estepona, nära kommersiella områden och med Puerto Banús i närheten, enligt exploatörens egen beskrivning. De beskrivs med fin utsikt och ett läge som ger sol ända till solnedgången.')

# ---------------------------------------------------------------- investment
a('The documents we hold give prices but no payment schedule, so the terms below are what we confirm with the developer in writing before you reserve.',
  'Los documentos de que disponemos recogen precios pero no un calendario de pagos, por lo que las condiciones siguientes son las que confirmamos por escrito con el promotor antes de que usted reserve.',
  'Les documents dont nous disposons indiquent des prix mais pas d’échéancier de paiement ; les conditions ci-dessous sont donc celles que nous confirmons par écrit avec le promoteur avant votre réservation.',
  'Die uns vorliegenden Unterlagen nennen Preise, aber keinen Zahlungsplan; die folgenden Bedingungen bestätigen wir daher schriftlich mit dem Bauträger, bevor Sie reservieren.',
  'В имеющихся у нас документах указаны цены, но нет графика платежей, поэтому перечисленные ниже условия мы подтверждаем у застройщика в письменном виде до того, как вы забронируете дом.',
  'تتضمن المستندات المتوفرة لدينا الأسعار دون جدول للدفعات، لذلك فإن الشروط أدناه هي ما نؤكده كتابةً مع المطوّر قبل أن تحجزوا.',
  'De documenten waarover wij beschikken noemen prijzen maar geen betalingsschema; de onderstaande voorwaarden bevestigen wij daarom schriftelijk bij de ontwikkelaar voordat u reserveert.',
  'Posiadane przez nas dokumenty podają ceny, ale nie harmonogram płatności, dlatego poniższe warunki potwierdzamy z deweloperem na piśmie, zanim Państwo dokonają rezerwacji.',
  'Dokumentene vi har oppgir priser, men ingen betalingsplan, så vilkårene nedenfor er det vi bekrefter skriftlig med utbyggeren før De reserverer.',
  'Handlingarna vi har anger priser men ingen betalningsplan, så villkoren nedan är det vi bekräftar skriftligen med exploatören innan ni bokar.')
a('The documents do not state a reservation amount. We ask for it and for the contract terms before you commit.',
  'Los documentos no indican el importe de la reserva. Lo pedimos, junto con las condiciones del contrato, antes de que usted se comprometa.',
  'Les documents n’indiquent pas le montant de la réservation. Nous le demandons, ainsi que les conditions du contrat, avant que vous ne vous engagiez.',
  'Die Unterlagen nennen keinen Reservierungsbetrag. Wir fragen ihn und die Vertragsbedingungen ab, bevor Sie sich verpflichten.',
  'В документах не указана сумма бронирования. Мы запрашиваем её и условия договора до того, как вы примете на себя обязательства.',
  'لا تذكر المستندات مبلغ الحجز. نسأل عنه وعن شروط العقد قبل أن تلتزموا.',
  'De documenten noemen geen reserveringsbedrag. Wij vragen ernaar, en naar de contractvoorwaarden, voordat u zich verbindt.',
  'W dokumentach nie podano kwoty rezerwacji. Pytamy o nią oraz o warunki umowy, zanim Państwo podejmą zobowiązanie.',
  'Dokumentene oppgir ikke noe reservasjonsbeløp. Vi ber om det og om kontraktsvilkårene før De forplikter Dem.',
  'Handlingarna anger inget bokningsbelopp. Vi frågar efter det och efter avtalsvillkoren innan ni binder er.')
a('No payment schedule is given. We ask for the instalments and their dates in writing.',
  'No se indica ningún calendario de pagos. Pedimos por escrito los plazos y sus fechas.',
  'Aucun échéancier de paiement n’est indiqué. Nous demandons par écrit les échéances et leurs dates.',
  'Ein Zahlungsplan ist nicht angegeben. Wir fragen die Raten und ihre Termine schriftlich ab.',
  'График платежей не указан. Мы запрашиваем в письменном виде суммы траншей и сроки.',
  'لا يُذكر أي جدول للدفعات. نطلب كتابةً الدفعات ومواعيدها.',
  'Er wordt geen betalingsschema vermeld. Wij vragen de termijnen en hun data schriftelijk op.',
  'Nie podano harmonogramu płatności. Prosimy na piśmie o raty i ich terminy.',
  'Ingen betalingsplan er oppgitt. Vi ber skriftlig om terminene og datoene for dem.',
  'Ingen betalningsplan anges. Vi begär avbetalningarna och deras datum skriftligen.')
a('VAT and taxes', 'IVA e impuestos', 'TVA et taxes', 'MwSt. und Steuern', 'НДС и налоги', 'ضريبة القيمة المضافة والضرائب', 'Btw en belastingen', 'VAT i podatki', 'Mva. og skatter', 'Moms och skatter')
a('The price list does not say whether its prices include VAT. We confirm the taxes and purchase costs in writing.',
  'La lista de precios no indica si sus precios incluyen el IVA. Confirmamos por escrito los impuestos y los gastos de compra.',
  'La liste de prix n’indique pas si ses prix incluent la TVA. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Die Preisliste sagt nicht, ob ihre Preise die MwSt. enthalten. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'В прайс-листе не сказано, включён ли в цены НДС. Мы подтверждаем налоги и расходы на покупку в письменном виде.',
  'لا تبيّن قائمة الأسعار ما إذا كانت أسعارها تشمل ضريبة القيمة المضافة. نؤكد الضرائب وتكاليف الشراء كتابةً.',
  'De prijslijst zegt niet of de prijzen btw bevatten. Wij bevestigen de belastingen en de aankoopkosten schriftelijk.',
  'Cennik nie podaje, czy ceny zawierają VAT. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Prislisten sier ikke om prisene inkluderer mva. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan anger inte om priserna inkluderar moms. Vi bekräftar skatter och köpkostnader skriftligen.')
a('The documents do not mention a guarantee on advance payments. We ask for the bank guarantee and the policy before any payment.',
  'Los documentos no mencionan una garantía sobre los pagos anticipados. Pedimos el aval bancario y la póliza antes de cualquier pago.',
  'Les documents ne mentionnent pas de garantie sur les paiements anticipés. Nous demandons la garantie bancaire et la police avant tout paiement.',
  'Die Unterlagen erwähnen keine Absicherung von Anzahlungen. Wir fragen vor jeder Zahlung nach der Bankbürgschaft und der Police.',
  'В документах не упоминается гарантия на авансовые платежи. Мы запрашиваем банковскую гарантию и полис до любого платежа.',
  'لا تذكر المستندات ضمانًا للدفعات المسبقة. نطلب الكفالة المصرفية ووثيقة التأمين قبل أي دفعة.',
  'De documenten vermelden geen waarborg voor vooruitbetalingen. Wij vragen de bankgarantie en de polis op vóór elke betaling.',
  'Dokumenty nie wspominają o gwarancji dla zaliczek. Przed jakąkolwiek płatnością prosimy o gwarancję bankową i polisę.',
  'Dokumentene nevner ingen garanti for forskuddsbetalinger. Vi ber om bankgarantien og polisen før enhver betaling.',
  'Handlingarna nämner ingen garanti för förskottsbetalningar. Vi begär bankgarantin och försäkringsbrevet före varje betalning.')

# ---------------------------------------------------------------- trust
a('Build status and delivery', 'Estado de la obra y entrega', 'État d’avancement et livraison', 'Baustand und Übergabe', 'Состояние стройки и сдача', 'حالة البناء والتسليم', 'Bouwstatus en oplevering', 'Stan budowy i odbiór', 'Byggestatus og overtakelse', 'Byggstatus och tillträde')
a('The developer’s page calls the phase 1 villas “turnkey”, but the plans are project-stage plans, the images are computer-generated, and no document gives a delivery date. We ask for the licence, the state of the works and the contractual date.',
  'La página del promotor presenta las villas de la fase 1 como «llave en mano», pero los planos son de proyecto, las imágenes están generadas por ordenador y ningún documento indica una fecha de entrega. Pedimos la licencia, el estado de las obras y la fecha contractual.',
  'La page du promoteur présente les villas de la phase 1 comme « clés en main », mais les plans sont des plans de projet, les images sont générées par ordinateur et aucun document n’indique de date de livraison. Nous demandons le permis, l’état d’avancement des travaux et la date contractuelle.',
  'Die Seite des Bauträgers nennt die Villen der Phase 1 „schlüsselfertig“, aber die Pläne sind Projektpläne, die Bilder sind computergeneriert, und kein Dokument nennt einen Übergabetermin. Wir fragen nach der Genehmigung, dem Stand der Arbeiten und dem vertraglichen Termin.',
  'На странице застройщика виллы первой очереди названы «под ключ», но планы проектные, изображения компьютерные, а срок сдачи не указан ни в одном документе. Мы запрашиваем разрешение, состояние работ и договорной срок.',
  'تصف صفحة المطوّر فيلات المرحلة الأولى بأنها «جاهزة للسكن بمفتاحها»، لكن المخططات هي مخططات مرحلة المشروع والصور مولَّدة بالحاسوب، ولا يذكر أي مستند موعد تسليم. نطلب الرخصة وحالة الأعمال والموعد التعاقدي.',
  'De pagina van de ontwikkelaar noemt de villa’s van fase 1 “turnkey”, maar de plannen zijn projectplannen, de beelden zijn computergegenereerd en geen enkel document noemt een opleverdatum. Wij vragen de vergunning, de stand van de werken en de contractuele datum op.',
  'Strona dewelopera określa wille fazy 1 jako „pod klucz”, ale plany są projektowe, obrazy generowane komputerowo, a żaden dokument nie podaje terminu odbioru. Prosimy o pozwolenie, stan robót i termin umowny.',
  'Utbyggerens side kaller villaene i fase 1 «nøkkelferdige», men planene er prosjektplaner, bildene er datagenererte, og ingen dokumenter oppgir en overtakelsesdato. Vi ber om tillatelsen, byggestatus og den kontraktfestede datoen.',
  'Exploatörens sida kallar villorna i fas 1 ”nyckelfärdiga”, men planerna är projektplaner, bilderna är datorgenererade och inget dokument anger ett tillträdesdatum. Vi begär bygglovet, byggstatusen och det avtalade datumet.')
a('The page text says semi-detached and the price table says “Adosado”. The plans’ site model shows homes built in pairs. We confirm the plot and the party walls of the home you choose.',
  'El texto de la página dice pareadas y la tabla de precios dice «adosado». La maqueta de implantación de los planos muestra viviendas construidas por parejas. Confirmamos la parcela y las paredes medianeras de la vivienda que usted elija.',
  'Le texte de la page dit jumelées et le tableau de prix dit « Adosado ». La maquette d’implantation des plans montre des maisons construites par deux. Nous confirmons la parcelle et les murs mitoyens de la maison que vous choisissez.',
  'Der Seitentext sagt Doppelhaushälften und die Preistabelle „Adosado“. Das Lagemodell der Pläne zeigt paarweise gebaute Häuser. Wir bestätigen Grundstück und Trennwände des Hauses, für das Sie sich entscheiden.',
  'В тексте страницы сказано «парные», а в таблице цен — «Adosado». На макете застройки на планах дома показаны парами. Мы подтверждаем участок и общие стены выбранного вами дома.',
  'يقول نص الصفحة شبه منفصلة ويقول جدول الأسعار «Adosado». ويُظهر نموذج الموقع في المخططات منازل مبنية في أزواج. نؤكد القطعة والجدران المشتركة للمنزل الذي تختارونه.',
  'De paginatekst zegt halfvrijstaand en de prijstabel zegt “Adosado”. Het situatiemodel van de plannen toont woningen die in paren zijn gebouwd. Wij bevestigen het perceel en de scheidingsmuren van de woning die u kiest.',
  'Tekst strony mówi o bliźniakach, a tabela cen o „Adosado”. Model sytuacyjny na planach pokazuje domy budowane parami. Potwierdzamy działkę i ściany wspólne wybranego przez Państwa domu.',
  'Sidens tekst sier tomannsbolig og pristabellen sier «Adosado». Situasjonsmodellen på tegningene viser boliger bygget i par. Vi bekrefter tomten og skilleveggene til boligen De velger.',
  'Sidans text säger parhus och pristabellen säger ”Adosado”. Situationsmodellen på ritningarna visar bostäder byggda i par. Vi bekräftar tomten och skiljeväggarna för den bostad ni väljer.')
a('Bedrooms and bathrooms', 'Dormitorios y baños', 'Chambres et salles de bains', 'Schlafzimmer und Bäder', 'Спальни и ванные комнаты', 'غرف النوم والحمّامات', 'Slaapkamers en badkamers', 'Sypialnie i łazienki', 'Soverom og bad', 'Sovrum och badrum')
a('The price table lists four bedrooms for F1V23 and F2V42, while their plans show three bedrooms and a basement cellar room. The page text says two or three bathrooms, the table says four, and the plans show three bathrooms and a toilet.',
  'La tabla de precios indica cuatro dormitorios para F1V23 y F2V42, mientras que sus planos muestran tres dormitorios y una bodega en el sótano. El texto de la página habla de dos o tres baños, la tabla de cuatro, y los planos muestran tres baños y un aseo.',
  'Le tableau de prix indique quatre chambres pour F1V23 et F2V42, alors que leurs plans montrent trois chambres et une cave au sous-sol. Le texte de la page parle de deux ou trois salles de bains, le tableau de quatre, et les plans montrent trois salles de bains et des toilettes.',
  'Die Preistabelle nennt vier Schlafzimmer für F1V23 und F2V42, während ihre Pläne drei Schlafzimmer und einen Kellerraum im Untergeschoss zeigen. Der Seitentext spricht von zwei oder drei Bädern, die Tabelle von vier, und die Pläne zeigen drei Bäder und ein WC.',
  'В таблице цен для F1V23 и F2V42 указаны четыре спальни, тогда как на их планах три спальни и подвальное помещение в цоколе. В тексте страницы говорится о двух или трёх ванных комнатах, в таблице — о четырёх, а на планах три ванные комнаты и туалет.',
  'يذكر جدول الأسعار أربع غرف نوم للمنزلين F1V23 وF2V42، بينما تُظهر مخططاتهما ثلاث غرف نوم وغرفة قبو في الطابق السفلي. ويتحدث نص الصفحة عن حمّامين أو ثلاثة، والجدول عن أربعة، وتُظهر المخططات ثلاثة حمّامات ومرحاضًا.',
  'De prijstabel noemt vier slaapkamers voor F1V23 en F2V42, terwijl hun plannen drie slaapkamers en een kelderruimte in de kelder tonen. De paginatekst spreekt van twee of drie badkamers, de tabel van vier, en de plannen tonen drie badkamers en een toilet.',
  'Tabela cen podaje cztery sypialnie dla F1V23 i F2V42, podczas gdy ich rzuty pokazują trzy sypialnie i pomieszczenie piwniczne w suterenie. Tekst strony mówi o dwóch lub trzech łazienkach, tabela o czterech, a rzuty pokazują trzy łazienki i toaletę.',
  'Pristabellen oppgir fire soverom for F1V23 og F2V42, mens tegningene deres viser tre soverom og et kjellerrom i kjelleren. Sidens tekst nevner to eller tre bad, tabellen fire, og tegningene viser tre bad og et toalett.',
  'Pristabellen anger fyra sovrum för F1V23 och F2V42, medan deras ritningar visar tre sovrum och ett förrådsrum i källaren. Sidans text nämner två eller tre badrum, tabellen fyra, och ritningarna visar tre badrum och en toalett.')
a('The built areas in the price table match the plans except for F1V24 and F3V1. We confirm which figure each contract uses.',
  'Las superficies construidas de la tabla de precios coinciden con las de los planos, salvo en F1V24 y F3V1. Confirmamos qué cifra usa cada contrato.',
  'Les surfaces construites du tableau de prix correspondent à celles des plans, sauf pour F1V24 et F3V1. Nous confirmons quel chiffre retient chaque contrat.',
  'Die bebauten Flächen der Preistabelle stimmen mit den Plänen überein, außer bei F1V24 und F3V1. Wir bestätigen, welche Zahl der jeweilige Vertrag verwendet.',
  'Площади застройки в таблице цен совпадают с планами, кроме F1V24 и F3V1. Мы уточняем, какая цифра используется в каждом договоре.',
  'تطابق المساحات المبنية في جدول الأسعار ما في المخططات باستثناء F1V24 وF3V1. نؤكد أي رقم يعتمده كل عقد.',
  'De bebouwde oppervlakten in de prijstabel komen overeen met de plannen, behalve bij F1V24 en F3V1. Wij bevestigen welk cijfer elk contract hanteert.',
  'Powierzchnie zabudowy w tabeli cen zgadzają się z rzutami, z wyjątkiem F1V24 i F3V1. Potwierdzamy, jaką wartość przyjmuje każda umowa.',
  'Byggearealene i pristabellen stemmer med tegningene, bortsett fra F1V24 og F3V1. Vi bekrefter hvilket tall hver kontrakt bruker.',
  'Byggytorna i pristabellen stämmer med ritningarna, utom för F1V24 och F3V1. Vi bekräftar vilket tal varje avtal använder.')

# ---------------------------------------------------------------- availability
a('13 homes <em>currently listed</em>',
  '13 viviendas <em>a la venta ahora</em>', '13 maisons <em>actuellement annoncées</em>', '13 Häuser <em>aktuell gelistet</em>',
  '13 домов <em>сейчас в продаже</em>', '13 منزلًا <em>معروضة حاليًا</em>', '13 woningen <em>momenteel vermeld</em>',
  '13 domów <em>obecnie w ofercie</em>', '13 boliger <em>for tiden annonsert</em>', '13 bostäder <em>listade just nu</em>')
a('Prices are those of the developer’s list as of October 2026 and are confirmed before reservation. The 13 homes below are semi-detached houses with three bedrooms on the plans.',
  'Los precios son los de la lista del promotor a octubre de 2026 y se confirman antes de la reserva. Las 13 viviendas siguientes son casas pareadas con tres dormitorios según los planos.',
  'Les prix sont ceux de la liste du promoteur à octobre 2026 et sont confirmés avant la réservation. Les 13 maisons ci-dessous sont des maisons jumelées de trois chambres d’après les plans.',
  'Die Preise sind die der Liste des Bauträgers mit Stand Oktober 2026 und werden vor der Reservierung bestätigt. Die folgenden 13 Häuser sind Doppelhaushälften mit drei Schlafzimmern laut Plänen.',
  'Цены взяты из списка застройщика на октябрь 2026 года и подтверждаются перед бронированием. Тринадцать домов ниже — парные дома с тремя спальнями согласно планам.',
  'الأسعار هي أسعار قائمة المطوّر حتى أكتوبر 2026 وتُؤكَّد قبل الحجز. المنازل الـ13 أدناه منازل شبه منفصلة بثلاث غرف نوم بحسب المخططات.',
  'De prijzen zijn die van de lijst van de ontwikkelaar per oktober 2026 en worden vóór de reservering bevestigd. De 13 woningen hieronder zijn halfvrijstaande woningen met volgens de plannen drie slaapkamers.',
  'Ceny pochodzą z listy dewelopera na październik 2026 r. i są potwierdzane przed rezerwacją. Poniższe 13 domów to domy bliźniacze z trzema sypialniami według rzutów.',
  'Prisene er de fra utbyggerens liste per oktober 2026 og bekreftes før reservasjon. De 13 boligene nedenfor er tomannsboliger med tre soverom ifølge tegningene.',
  'Priserna är de i exploatörens lista per oktober 2026 och bekräftas före bokning. De 13 bostäderna nedan är parhus med tre sovrum enligt ritningarna.')
a('Prices and areas are transcribed from the developer’s portal listing of October 2026, which shows 13 of the 50 homes, all marked available, and does not say whether VAT is included. The terrace and garden areas are the listing’s figures; on the plans the exterior area is larger because it also counts the entrance and vehicle access (for F1V20, 179.41 sqm on the plan against 130.55 sqm of terrace and garden in the listing). Two figures differ between documents. F1V24: 180.60 sqm built in the listing, 184.55 sqm on its plan. F3V1: 186.00 sqm built and 107.80 sqm of garden in the listing, against 198.9 sqm built including a share of the communal areas and 61.1 sqm of garden on its plan. The listing gives four bedrooms for F1V23 and F2V42; their plans show three bedrooms and a cellar room, so the table above says three. For F1V37 only the lower two levels of the plan were supplied.',
  'Los precios y las superficies están transcritos del listado del portal del promotor de octubre de 2026, que muestra 13 de las 50 viviendas, todas marcadas como disponibles, y no indica si el IVA está incluido. Las superficies de terraza y jardín son las del listado; en los planos la superficie exterior es mayor porque incluye también la entrada y el acceso de vehículos (para F1V20, #179.41 [m2] en el plano frente a #130.55 [m2] de terraza y jardín en el listado). Dos cifras difieren entre documentos. F1V24: #180.60 [m2] construidos en el listado y #184.55 [m2] en su plano. F3V1: #186.00 [m2] construidos y #107.80 [m2] de jardín en el listado, frente a #198.9 [m2] construidos con una parte de las zonas comunes y #61.1 [m2] de jardín en su plano. El listado indica cuatro dormitorios para F1V23 y F2V42; sus planos muestran tres dormitorios y una bodega, por lo que la tabla anterior indica tres. De F1V37 solo se facilitaron los dos niveles inferiores del plano.',
  'Les prix et les surfaces sont transcrits du listing du portail du promoteur d’octobre 2026, qui présente 13 des 50 maisons, toutes indiquées comme disponibles, et ne dit pas si la TVA est comprise. Les surfaces de terrasse et de jardin sont celles du listing ; sur les plans, la surface extérieure est plus grande car elle compte aussi l’entrée et l’accès des véhicules (pour F1V20, #179.41 [m2] sur le plan contre #130.55 [m2] de terrasse et de jardin dans le listing). Deux chiffres diffèrent d’un document à l’autre. F1V24 : #180.60 [m2] construits dans le listing, #184.55 [m2] sur son plan. F3V1 : #186.00 [m2] construits et #107.80 [m2] de jardin dans le listing, contre #198.9 [m2] construits avec une part des parties communes et #61.1 [m2] de jardin sur son plan. Le listing indique quatre chambres pour F1V23 et F2V42 ; leurs plans montrent trois chambres et une cave, c’est pourquoi le tableau ci-dessus indique trois. Pour F1V37, seuls les deux niveaux inférieurs du plan ont été fournis.',
  'Preise und Flächen sind der Portalliste des Bauträgers von Oktober 2026 entnommen, die 13 der 50 Häuser zeigt, alle als verfügbar gekennzeichnet, und nicht angibt, ob die MwSt. enthalten ist. Die Terrassen- und Gartenflächen sind die Werte der Liste; auf den Plänen ist die Außenfläche größer, weil sie auch den Eingang und die Fahrzeugzufahrt umfasst (bei F1V20 #179.41 [m2] auf dem Plan gegenüber #130.55 [m2] Terrasse und Garten in der Liste). Zwei Angaben weichen zwischen den Dokumenten ab. F1V24: #180.60 [m2] bebaut in der Liste, #184.55 [m2] auf dem Plan. F3V1: #186.00 [m2] bebaut und #107.80 [m2] Garten in der Liste, gegenüber #198.9 [m2] bebaut einschließlich eines Anteils an den Gemeinschaftsflächen und #61.1 [m2] Garten auf dem Plan. Die Liste nennt vier Schlafzimmer für F1V23 und F2V42; ihre Pläne zeigen drei Schlafzimmer und einen Kellerraum, daher nennt die Tabelle oben drei. Von F1V37 wurden nur die beiden unteren Ebenen des Plans geliefert.',
  'Цены и площади перенесены из списка на портале застройщика за октябрь 2026 года, в котором показаны 13 из 50 домов, все отмечены как доступные; о том, включён ли НДС, там не сказано. Площади террас и садов — данные списка; на планах внешняя площадь больше, потому что включает вход и подъезд для автомобилей (для F1V20 — #179.41 [m2] на плане против #130.55 [m2] террасы и сада в списке). Две цифры расходятся между документами. F1V24: #180.60 [m2] площади застройки в списке и #184.55 [m2] на плане. F3V1: #186.00 [m2] площади застройки и #107.80 [m2] сада в списке против #198.9 [m2] застройки с долей общих зон и #61.1 [m2] сада на плане. В списке для F1V23 и F2V42 указаны четыре спальни; на их планах три спальни и подвальное помещение, поэтому в таблице выше указаны три. По F1V37 предоставлены только два нижних уровня плана.',
  'الأسعار والمساحات منقولة من قائمة بوابة المطوّر لشهر أكتوبر 2026، وهي تعرض 13 منزلًا من أصل 50، كلها موسومة بأنها متاحة، ولا تبيّن ما إذا كانت ضريبة القيمة المضافة مشمولة. مساحات التراس والحديقة هي أرقام القائمة؛ وفي المخططات تكون المساحة الخارجية أكبر لأنها تشمل أيضًا المدخل ومسار السيارات (في F1V20 بلغت #179.41 [m2] في المخطط مقابل #130.55 [m2] للتراس والحديقة في القائمة). ويختلف رقمان بين المستندات. F1V24: #180.60 [m2] مبنية في القائمة و#184.55 [m2] في مخططه. F3V1: #186.00 [m2] مبنية و#107.80 [m2] حديقة في القائمة، مقابل #198.9 [m2] مبنية تشمل حصة من المناطق المشتركة و#61.1 [m2] حديقة في مخططه. وتذكر القائمة أربع غرف نوم لـF1V23 وF2V42؛ بينما تُظهر مخططاتهما ثلاث غرف نوم وغرفة قبو، لذلك يذكر الجدول أعلاه ثلاثًا. أما F1V37 فلم يُزوَّد منه سوى المستويين السفليين من المخطط.',
  'Prijzen en oppervlakten zijn overgenomen uit de portaallijst van de ontwikkelaar van oktober 2026, die 13 van de 50 woningen toont, alle als beschikbaar aangemerkt, en niet zegt of btw is inbegrepen. De terras- en tuinoppervlakten zijn de cijfers van de lijst; op de plannen is de buitenoppervlakte groter omdat die ook de entree en de toegang voor voertuigen meetelt (voor F1V20 #179.41 [m2] op het plan tegenover #130.55 [m2] terras en tuin in de lijst). Twee cijfers verschillen tussen de documenten. F1V24: #180.60 [m2] bebouwd in de lijst, #184.55 [m2] op het plan. F3V1: #186.00 [m2] bebouwd en #107.80 [m2] tuin in de lijst, tegenover #198.9 [m2] bebouwd inclusief een aandeel in de gemeenschappelijke delen en #61.1 [m2] tuin op het plan. De lijst noemt vier slaapkamers voor F1V23 en F2V42; hun plannen tonen drie slaapkamers en een kelderruimte, daarom noemt de tabel hierboven er drie. Van F1V37 zijn alleen de twee onderste niveaus van het plan geleverd.',
  'Ceny i powierzchnie są przepisane z listy z portalu dewelopera z października 2026 r., która pokazuje 13 z 50 domów, wszystkie oznaczone jako dostępne, i nie podaje, czy VAT jest wliczony. Powierzchnie tarasów i ogrodów pochodzą z listy; na rzutach powierzchnia zewnętrzna jest większa, bo obejmuje także wejście i dojazd dla pojazdów (dla F1V20 #179.41 [m2] na rzucie wobec #130.55 [m2] tarasu i ogrodu na liście). Dwie wartości różnią się między dokumentami. F1V24: #180.60 [m2] zabudowy na liście, #184.55 [m2] na rzucie. F3V1: #186.00 [m2] zabudowy i #107.80 [m2] ogrodu na liście, wobec #198.9 [m2] zabudowy wraz z udziałem w częściach wspólnych i #61.1 [m2] ogrodu na rzucie. Lista podaje cztery sypialnie dla F1V23 i F2V42; ich rzuty pokazują trzy sypialnie i pomieszczenie piwniczne, dlatego tabela powyżej podaje trzy. Dla F1V37 dostarczono tylko dwa niższe poziomy rzutu.',
  'Prisene og arealene er overført fra utbyggerens portalliste fra oktober 2026, som viser 13 av de 50 boligene, alle merket som ledige, og ikke sier om mva. er inkludert. Terrasse- og hageareal er listens tall; på tegningene er utearealet større fordi det også teller inngangen og kjøreadkomsten (for F1V20 #179.41 [m2] på tegningen mot #130.55 [m2] terrasse og hage i listen). To tall avviker mellom dokumentene. F1V24: #180.60 [m2] bebygd areal i listen, #184.55 [m2] på tegningen. F3V1: #186.00 [m2] bebygd areal og #107.80 [m2] hage i listen, mot #198.9 [m2] bebygd areal inkludert en andel av fellesarealene og #61.1 [m2] hage på tegningen. Listen oppgir fire soverom for F1V23 og F2V42; tegningene deres viser tre soverom og et kjellerrom, så tabellen over oppgir tre. For F1V37 ble bare de to nedre nivåene av tegningen levert.',
  'Priser och ytor är överförda från exploatörens portallista från oktober 2026, som visar 13 av de 50 bostäderna, alla markerade som lediga, och inte anger om moms ingår. Terrass- och trädgårdsytorna är listans siffror; på ritningarna är utomhusytan större eftersom den också räknar entrén och infarten för fordon (för F1V20 #179.41 [m2] på ritningen mot #130.55 [m2] terrass och trädgård i listan). Två siffror skiljer sig mellan dokumenten. F1V24: #180.60 [m2] byggyta i listan, #184.55 [m2] på ritningen. F3V1: #186.00 [m2] byggyta och #107.80 [m2] trädgård i listan, mot #198.9 [m2] byggyta inklusive en andel av de gemensamma ytorna och #61.1 [m2] trädgård på ritningen. Listan anger fyra sovrum för F1V23 och F2V42; deras ritningar visar tre sovrum och ett förrådsrum, så tabellen ovan anger tre. För F1V37 levererades bara de två nedre planen av ritningen.')

# ---------------------------------------------------------------- timeline and viewing
a('The plans of the homes that interest you and the price list.',
  'Los planos de las viviendas que le interesen y la lista de precios.', 'Les plans des maisons qui vous intéressent et la liste de prix.', 'Die Pläne der Häuser, die Sie interessieren, und die Preisliste.',
  'Планировки интересующих вас домов и прайс-лист.', 'مخططات المنازل التي تهمكم وقائمة الأسعار.', 'De plattegronden van de woningen die u interesseren en de prijslijst.',
  'Rzuty interesujących Państwa domów i cennik.', 'Plantegningene av boligene som interesserer Dem, og prislisten.', 'Planritningarna för de bostäder som intresserar er och prislistan.')
a('We confirm the reservation terms and the payment guarantee in writing before you commit.',
  'Confirmamos por escrito las condiciones de reserva y la garantía de los pagos antes de que usted se comprometa.',
  'Nous confirmons par écrit les conditions de réservation et la garantie des paiements avant que vous ne vous engagiez.',
  'Wir bestätigen die Reservierungsbedingungen und die Zahlungsabsicherung schriftlich, bevor Sie sich verpflichten.',
  'Мы подтверждаем в письменном виде условия бронирования и гарантию платежей до того, как вы примете на себя обязательства.',
  'نؤكد كتابةً شروط الحجز وضمان الدفعات قبل أن تلتزموا.',
  'Wij bevestigen de reserveringsvoorwaarden en de betalingswaarborg schriftelijk voordat u zich verbindt.',
  'Warunki rezerwacji i gwarancję płatności potwierdzamy na piśmie, zanim Państwo podejmą zobowiązanie.',
  'Vi bekrefter reservasjonsvilkårene og betalingsgarantien skriftlig før De forplikter Dem.',
  'Vi bekräftar bokningsvillkoren och betalningsgarantin skriftligen innan ni binder er.')
a('The documents do not say how far the works have gone, so a visit is about the site, the plans and the state of the build.',
  'Los documentos no indican cuánto han avanzado las obras, así que la visita trata del terreno, los planos y el estado de la construcción.',
  'Les documents n’indiquent pas où en sont les travaux ; la visite porte donc sur le site, les plans et l’état de la construction.',
  'Die Unterlagen sagen nicht, wie weit die Arbeiten sind; bei einem Besuch geht es daher um das Gelände, die Pläne und den Stand des Baus.',
  'В документах не сказано, как далеко продвинулись работы, поэтому визит посвящён участку, планам и состоянию стройки.',
  'لا تبيّن المستندات مدى تقدم الأعمال، لذلك تتناول الزيارة الموقع والمخططات وحالة البناء.',
  'De documenten zeggen niet hoe ver de werken zijn, dus een bezoek gaat over het terrein, de plannen en de stand van de bouw.',
  'Dokumenty nie podają, jak daleko zaszły roboty, dlatego wizyta dotyczy terenu, rzutów i stanu budowy.',
  'Dokumentene sier ikke hvor langt arbeidene har kommet, så et besøk handler om tomten, tegningene og byggestatusen.',
  'Handlingarna anger inte hur långt arbetena har kommit, så ett besök handlar om platsen, ritningarna och byggstatusen.')
a('Walk the development next to the golf club and see where each garden sits.',
  'Recorra la promoción junto al club de golf y vea dónde está cada jardín.', 'Parcourez le programme à côté du club de golf et voyez où se trouve chaque jardin.',
  'Gehen Sie die Anlage neben dem Golfclub ab und sehen Sie, wo jeder Garten liegt.', 'Пройдитесь по комплексу рядом с гольф-клубом и посмотрите, где расположен каждый сад.',
  'تجولوا في المشروع المجاور لنادي الغولف وشاهدوا موقع كل حديقة.', 'Loop door het project naast de golfclub en zie waar elke tuin ligt.',
  'Przejdźcie Państwo po inwestycji obok klubu golfowego i zobaczcie, gdzie leży każdy ogród.', 'Gå gjennom prosjektet ved siden av golfklubben og se hvor hver hage ligger.',
  'Gå igenom projektet intill golfklubben och se var varje trädgård ligger.')
a('Nearby', 'En los alrededores', 'À proximité', 'In der Umgebung', 'По соседству', 'في المحيط', 'In de omgeving', 'W okolicy', 'I nærheten', 'I närheten')
a('We take you to the golf club and to Puerto Banús and time the drive.',
  'Le llevamos al club de golf y a Puerto Banús y cronometramos el trayecto.', 'Nous vous conduisons au club de golf et à Puerto Banús et chronométrons le trajet.',
  'Wir fahren mit Ihnen zum Golfclub und nach Puerto Banús und stoppen die Fahrzeit.', 'Мы отвезём вас к гольф-клубу и в Пуэрто-Банус и засечём время в пути.',
  'نرافقكم إلى نادي الغولف وإلى بويرتو بانوس ونحتسب مدة الرحلة.', 'Wij rijden met u naar de golfclub en naar Puerto Banús en nemen de rijtijd op.',
  'Zawieziemy Państwa do klubu golfowego i do Puerto Banús i zmierzymy czas przejazdu.', 'Vi kjører med Dem til golfklubben og til Puerto Banús og tar tiden.',
  'Vi kör med er till golfklubben och till Puerto Banús och tar tid på resan.')

# ---------------------------------------------------------------- enquiry
a('Ask about <em>Cedro Golf Villas</em>', 'Pregunte por <em>Cedro Golf Villas</em>', 'Renseignez-vous sur <em>Cedro Golf Villas</em>', 'Fragen Sie nach <em>Cedro Golf Villas</em>',
  'Узнайте о <em>Cedro Golf Villas</em>', 'استفسروا عن <em>Cedro Golf Villas</em>', 'Vraag naar <em>Cedro Golf Villas</em>',
  'Zapytaj o <em>Cedro Golf Villas</em>', 'Spør om <em>Cedro Golf Villas</em>', 'Fråga om <em>Cedro Golf Villas</em>')
a('Hello Nueva Living, I would like information about Cedro Golf Villas.',
  'Hola Nueva Living, me gustaría recibir información sobre Cedro Golf Villas.', 'Bonjour Nueva Living, je souhaiterais des informations sur Cedro Golf Villas.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Cedro Golf Villas.', 'Здравствуйте, Nueva Living! Я хотел бы получить информацию о Cedro Golf Villas.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Cedro Golf Villas.', 'Hallo Nueva Living, ik wil graag informatie over Cedro Golf Villas.',
  'Dzień dobry, Nueva Living, chciałbym uzyskać informacje o Cedro Golf Villas.', 'Hei Nueva Living, jeg vil gjerne ha informasjon om Cedro Golf Villas.',
  'Hej Nueva Living, jag skulle vilja få information om Cedro Golf Villas.')

# ---------------------------------------------------------------- faq
a('The development has 50 semi-detached homes. The developer lists 13 of them with a price and marks all 13 available, from EUR 775,000 to EUR 950,000.',
  'La promoción tiene 50 viviendas pareadas. El promotor incluye 13 de ellas con precio y las marca todas como disponibles, de €775000 a €950000.',
  'Le programme compte 50 maisons jumelées. Le promoteur en annonce 13 avec un prix et les indique toutes comme disponibles, de €775000 à €950000.',
  'Die Anlage hat 50 Doppelhaushälften. Der Bauträger listet 13 davon mit Preis und kennzeichnet alle 13 als verfügbar, von €775000 bis €950000.',
  'В комплексе 50 парных домов. Застройщик указывает 13 из них с ценой и отмечает все 13 как доступные: от €775000 до €950000.',
  'يضم المشروع 50 منزلًا شبه منفصل. يعرض المطوّر 13 منها بسعر ويصفها كلها بأنها متاحة، من €775000 إلى €950000.',
  'Het project heeft 50 halfvrijstaande woningen. De ontwikkelaar vermeldt er 13 met een prijs en markeert alle 13 als beschikbaar, van €775000 tot €950000.',
  'Inwestycja liczy 50 domów bliźniaczych. Deweloper podaje 13 z nich z ceną i oznacza wszystkie 13 jako dostępne, od €775000 do €950000.',
  'Prosjektet har 50 tomannsboliger. Utbyggeren oppgir 13 av dem med pris og merker alle 13 som ledige, fra €775000 til €950000.',
  'Projektet har 50 parhus. Exploatören listar 13 av dem med pris och markerar alla 13 som lediga, från €775000 till €950000.')
a('Are the homes semi-detached or terraced?', '¿Las viviendas son pareadas o adosadas?', 'Les maisons sont-elles jumelées ou en bande ?', 'Sind die Häuser Doppelhaushälften oder Reihenhäuser?',
  'Дома парные или таунхаусы?', 'هل المنازل شبه منفصلة أم متلاصقة؟', 'Zijn de woningen halfvrijstaand of rijwoningen?', 'Czy domy to bliźniaki, czy szeregowce?', 'Er boligene tomannsboliger eller rekkehus?', 'Är bostäderna parhus eller radhus?')
a('The developer’s page says semi-detached and its price table says “Adosado”, which means terraced or attached. The plans show the homes built in pairs, so we call them semi-detached and confirm the party walls of your plot.',
  'La página del promotor dice pareadas y su tabla de precios dice «adosado», que significa en hilera o adosado. Los planos muestran las viviendas construidas por parejas, por eso las llamamos pareadas y confirmamos las paredes medianeras de su parcela.',
  'La page du promoteur dit jumelées et son tableau de prix dit « Adosado », ce qui signifie en bande ou accolé. Les plans montrent les maisons construites par deux, c’est pourquoi nous les disons jumelées et confirmons les murs mitoyens de votre parcelle.',
  'Die Seite des Bauträgers sagt Doppelhaushälften und seine Preistabelle „Adosado“, was Reihen- oder Anbauhaus bedeutet. Die Pläne zeigen die Häuser paarweise gebaut, daher nennen wir sie Doppelhaushälften und bestätigen die Trennwände Ihres Grundstücks.',
  'На странице застройщика написано «парные», а в таблице цен — «Adosado», что означает дом в ряду или пристроенный дом. На планах дома показаны парами, поэтому мы называем их парными и подтверждаем общие стены вашего участка.',
  'تقول صفحة المطوّر شبه منفصلة ويقول جدول الأسعار «Adosado»، أي متلاصق ضمن صف. وتُظهر المخططات المنازل مبنية في أزواج، لذلك نسميها شبه منفصلة ونؤكد الجدران المشتركة في قطعتكم.',
  'De pagina van de ontwikkelaar zegt halfvrijstaand en de prijstabel zegt “Adosado”, wat rij- of aaneengebouwd huis betekent. De plannen tonen de woningen in paren gebouwd, daarom noemen wij ze halfvrijstaand en bevestigen wij de scheidingsmuren van uw perceel.',
  'Strona dewelopera mówi o bliźniakach, a tabela cen o „Adosado”, co oznacza dom szeregowy lub przylegający. Rzuty pokazują domy budowane parami, dlatego nazywamy je bliźniakami i potwierdzamy ściany wspólne Państwa działki.',
  'Utbyggerens side sier tomannsbolig og pristabellen sier «Adosado», som betyr rekkehus eller sammenbygd hus. Tegningene viser boligene bygget i par, så vi kaller dem tomannsboliger og bekrefter skilleveggene på tomten Deres.',
  'Exploatörens sida säger parhus och pristabellen säger ”Adosado”, vilket betyder radhus eller sammanbyggt hus. Ritningarna visar bostäderna byggda i par, så vi kallar dem parhus och bekräftar skiljeväggarna på er tomt.')
a('How many bedrooms do they have?', '¿Cuántos dormitorios tienen?', 'Combien de chambres comptent-elles ?', 'Wie viele Schlafzimmer haben sie?', 'Сколько в них спален?', 'كم غرفة نوم فيها؟', 'Hoeveel slaapkamers hebben ze?', 'Ile mają sypialni?', 'Hvor mange soverom har de?', 'Hur många sovrum har de?')
a('The plans of all 13 homes show three bedrooms on one floor and a cellar room in the basement. The price table lists four bedrooms for F1V23 and F2V42, which we check with the developer.',
  'Los planos de las 13 viviendas muestran tres dormitorios en una misma planta y una bodega en el sótano. La tabla de precios indica cuatro dormitorios para F1V23 y F2V42, algo que comprobamos con el promotor.',
  'Les plans des 13 maisons montrent trois chambres sur un même niveau et une cave au sous-sol. Le tableau de prix indique quatre chambres pour F1V23 et F2V42, ce que nous vérifions auprès du promoteur.',
  'Die Pläne aller 13 Häuser zeigen drei Schlafzimmer auf einer Ebene und einen Kellerraum im Untergeschoss. Die Preistabelle nennt vier Schlafzimmer für F1V23 und F2V42, was wir beim Bauträger prüfen.',
  'На планах всех 13 домов показаны три спальни на одном этаже и подвальное помещение в цоколе. В таблице цен для F1V23 и F2V42 указаны четыре спальни; мы уточняем это у застройщика.',
  'تُظهر مخططات المنازل الـ13 كلها ثلاث غرف نوم في طابق واحد وغرفة قبو في الطابق السفلي. ويذكر جدول الأسعار أربع غرف نوم للمنزلين F1V23 وF2V42، ونتحقق من ذلك لدى المطوّر.',
  'De plannen van alle 13 woningen tonen drie slaapkamers op één verdieping en een kelderruimte in de kelder. De prijstabel noemt vier slaapkamers voor F1V23 en F2V42, wat wij bij de ontwikkelaar nagaan.',
  'Rzuty wszystkich 13 domów pokazują trzy sypialnie na jednej kondygnacji i pomieszczenie piwniczne w piwnicy. Tabela cen podaje cztery sypialnie dla F1V23 i F2V42, co weryfikujemy u dewelopera.',
  'Plantegningene av alle 13 boligene viser tre soverom i én etasje og et kjellerrom i kjelleren. Pristabellen oppgir fire soverom for F1V23 og F2V42, noe vi sjekker med utbyggeren.',
  'Planritningarna för alla 13 bostäder visar tre sovrum på ett plan och ett förrådsrum i källaren. Pristabellen anger fyra sovrum för F1V23 och F2V42, vilket vi kontrollerar med exploatören.')
a('The price list does not say. We confirm the taxes and purchase costs in writing.',
  'La lista de precios no lo indica. Confirmamos por escrito los impuestos y los gastos de compra.', 'La liste de prix ne le dit pas. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Die Preisliste sagt es nicht. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.', 'В прайс-листе об этом не сказано. Мы подтверждаем налоги и расходы на покупку в письменном виде.',
  'لا تبيّن قائمة الأسعار ذلك. نؤكد الضرائب وتكاليف الشراء كتابةً.', 'De prijslijst zegt het niet. Wij bevestigen de belastingen en de aankoopkosten schriftelijk.',
  'Cennik tego nie podaje. Podatki i koszty zakupu potwierdzamy na piśmie.', 'Prislisten sier det ikke. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan anger det inte. Vi bekräftar skatter och köpkostnader skriftligen.')
a('No document we hold gives a delivery date. The developer’s page calls the phase 1 villas turnkey, and we ask for the licence, the state of the works and the contractual date.',
  'Ningún documento de que disponemos indica una fecha de entrega. La página del promotor presenta las villas de la fase 1 como llave en mano, y pedimos la licencia, el estado de las obras y la fecha contractual.',
  'Aucun document dont nous disposons n’indique de date de livraison. La page du promoteur présente les villas de la phase 1 comme clés en main, et nous demandons le permis, l’état d’avancement des travaux et la date contractuelle.',
  'Kein uns vorliegendes Dokument nennt einen Übergabetermin. Die Seite des Bauträgers nennt die Villen der Phase 1 schlüsselfertig, und wir fragen nach der Genehmigung, dem Stand der Arbeiten und dem vertraglichen Termin.',
  'Ни в одном из имеющихся у нас документов срок сдачи не указан. На странице застройщика виллы первой очереди названы «под ключ», и мы запрашиваем разрешение, состояние работ и договорной срок.',
  'لا يذكر أي مستند متوفر لدينا موعد تسليم. تصف صفحة المطوّر فيلات المرحلة الأولى بأنها جاهزة بمفتاحها، ونطلب الرخصة وحالة الأعمال والموعد التعاقدي.',
  'Geen enkel document waarover wij beschikken noemt een opleverdatum. De pagina van de ontwikkelaar noemt de villa’s van fase 1 turnkey, en wij vragen de vergunning, de stand van de werken en de contractuele datum op.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu odbioru. Strona dewelopera określa wille fazy 1 jako pod klucz, a my prosimy o pozwolenie, stan robót i termin umowny.',
  'Ingen av dokumentene vi har oppgir en overtakelsesdato. Utbyggerens side kaller villaene i fase 1 nøkkelferdige, og vi ber om tillatelsen, byggestatus og den kontraktfestede datoen.',
  'Inget av dokumenten vi har anger ett tillträdesdatum. Exploatörens sida kallar villorna i fas 1 nyckelfärdiga, och vi begär bygglovet, byggstatusen och det avtalade datumet.')

# The mechanical "N of M homes available" says "apartments" in some languages; these are houses.
force('13 of 50 homes available',
  '13 de 50 viviendas disponibles', '13 maisons disponibles sur 50', '13 von 50 Häusern verfügbar',
  '13 из 50 домов доступно', '13 من 50 منزلًا متاحًا', '13 van de 50 woningen beschikbaar',
  '13 z 50 domów dostępnych', '13 av 50 boliger ledige', '13 av 50 bostäder lediga')

# ---------------------------------------------------------------- write
missing = [s for s in TODO if s not in T]
if missing:
    print('MISSING', len(missing))
    for s in missing[:40]:
        print('  ', repr(s[:100]))
    sys.exit(1)
json.dump(T, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
