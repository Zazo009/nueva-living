# -*- coding: utf-8 -*-
"""Golfside Hill Residences (east Marbella): the strings the translation memory did not have.

Same shape as k_higueron.py: a(i, hint, es, fr, de, ru, ar, nl, pl, no, sv). The row is found by
hint, the start of the English string, which must match exactly one string in todo.json; i is the
index scaffold.py printed when the row was written and is kept only as a reading aid, because the
indices shift whenever the translation memory learns one of the strings. Tokens expand per language:  {E1300100} money,  {N173.98} a
figure with the locale's decimal mark,  {U} the area unit (m2, ru м², ar م²).

The unit size rows are built by size() from the same numbers as the English, with one word per
measure for the whole table (the size-label guard holds a project to that). The availability floor
labels are left to assemble.py, which writes them from FLOOR_PARTS.

    python3 tools/import/k_golfside_hill_residences.py <workdir>
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}
UNIT['ru'] = 'м²'
UNIT['ar'] = 'م²'
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


def find(hint):
    if hint in todo:
        return hint
    hits = [s for s in todo if s.startswith(hint)]
    assert len(hits) == 1, (hint, len(hits))
    return hits[0]


def a(i, hint, *tr):
    en = find(hint)
    assert len(tr) == 9, (i, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    assert en in todo, en
    T[en] = {l: en for l in LOCS}


# ---------------------------------------------------------------- unit sizes
W = {   # built, usable, terraces, terraces and solarium, garden -- the words la-resina-hillside-residences uses
    'es': ('construido', 'superficie útil', 'terrazas', 'terrazas y solárium', 'jardín'),
    'fr': ('construit', 'surface utile', 'terrasses', 'terrasses et solarium', 'jardin'),
    'de': ('bebaut', 'Wohnfläche', 'Terrassen', 'Terrassen und Solarium', 'Garten'),
    'ru': ('застройка', 'полезная площадь', 'террасы', 'террасы и солярий', 'сад'),
    'ar': ('مبنية', 'مساحة صافية', 'تراسات', 'تراسات وسولاريوم', 'حديقة'),
    'nl': ('bebouwd', 'nuttige oppervlakte', 'terrassen', 'terrassen en solarium', 'tuin'),
    'pl': ('powierzchnia zabudowy', 'powierzchnia użytkowa', 'tarasy', 'tarasy i solarium', 'ogród'),
    'no': ('bygget', 'nyttbart areal', 'terrasser', 'terrasser og solterrasse', 'hage'),
    'sv': ('byggyta', 'nyttoyta', 'terrasser', 'terrasser och solterrass', 'trädgård'),
}


def size(i, built, usable, terr, garden=None, solarium=True):
    en = find(f'{built} sqm built, {usable} sqm usable, {terr} sqm terraces')
    out = {}
    for l in LOCS:
        b, u, t, ts, g = W[l]
        parts = [f'{num(built, l)} {UNIT[l]} {b}', f'{num(usable, l)} {UNIT[l]} {u}', f'{num(terr, l)} {UNIT[l]} {ts if solarium else t}']
        if garden:
            parts.append(f'{num(garden, l)} {UNIT[l]} {g}')
        out[l] = ', '.join(parts)
    T[en] = out


size(60, '173.98', '139.52', '134.11')
size(62, '243.20', '196.58', '183.50')
size(66, '220.94', '180.62', '149.29', '201.96', solarium=False)
size(69, '178.33', '142.86', '134.11')
size(72, '264.44', '213.48', '220.63', '37.79')
size(79, '220.94', '180.62', '144.44', '195.51', solarium=False)

for en in ('Golfside Hill Residences', 'Golfside Hill', 'Golfside Hill <em>Residences</em>',
           '19-1-A', '19-1-B', '19-1-C', '20-0-A', '20-1-A', '22-0-B', '23-0-A', '24-0-A', '28-0-A'):
    same(en)

# ---------------------------------------------------------------- top of page
a(3, 'Nine homes still available',
  'Nueve viviendas aún disponibles en una fase de un conjunto cerrado junto a un campo de golf, en el este de Marbella: dos apartamentos con jardín, cuatro áticos con solárium en la cubierta y tres villas pareadas, de tres o cuatro dormitorios y de {N173.98} a {N264.44} {U} construidos, todas con piscina privada en los planos.',
  "Neuf logements encore disponibles dans une phase d'un ensemble fermé voisin d'un golf, dans l'est de Marbella : deux appartements avec jardin, quatre penthouses avec solarium sur le toit et trois villas jumelées, de trois ou quatre chambres et de {N173.98} à {N264.44} {U} construits, chacun dessiné avec une piscine privée.",
  'Neun noch verfügbare Wohneinheiten in einem Bauabschnitt einer geschlossenen Wohnanlage an einem Golfplatz im Osten von Marbella: zwei Gartenwohnungen, vier Penthäuser mit Dachsolarium und drei Doppelhaushälften mit drei oder vier Schlafzimmern und {N173.98} bis {N264.44} {U} bebauter Fläche, jede in den Plänen mit eigenem Pool.',
  'Девять ещё доступных объектов в одной из очередей закрытого комплекса рядом с гольф-полем на востоке Марбельи: две квартиры с садом, четыре пентхауса с солярием на крыше и три парных дома, с тремя или четырьмя спальнями и площадью застройки от {N173.98} до {N264.44} {U}, у каждого на плане собственный бассейн.',
  'تسعة مساكن لا تزال متاحة في مرحلة من مجمع مسوّر بجوار ملعب للغولف شرق ماربيا: شقتان بحديقة، وأربع شقق بنتهاوس مع سولاريوم على السطح، وثلاث فلل شبه منفصلة، بثلاث أو أربع غرف نوم ومساحة مبنية من {N173.98} إلى {N264.44} {U}، ولكل منها مسبح خاص في المخططات.',
  "Negen nog beschikbare woningen in een fase van een omheind complex naast een golfbaan in het oosten van Marbella: twee tuinappartementen, vier penthouses met een solarium op het dak en drie halfvrijstaande villa's, met drie of vier slaapkamers en {N173.98} tot {N264.44} {U} bebouwd, elk op tekening met een privézwembad.",
  "Dziewięć wciąż dostępnych nieruchomości w jednym z etapów zamkniętego osiedla przy polu golfowym we wschodniej Marbelli: dwa mieszkania z ogrodem, cztery penthouse'y z solarium na dachu i trzy domy bliźniacze, z trzema lub czterema sypialniami i powierzchnią zabudowy od {N173.98} do {N264.44} {U}, każda z prywatnym basenem na rzucie.",
  'Ni boliger som fortsatt er tilgjengelige i ett byggetrinn av et inngjerdet anlegg ved en golfbane øst i Marbella: to hageleiligheter, fire toppleiligheter med solterrasse på taket og tre tomannsvillaer, med tre eller fire soverom og {N173.98} til {N264.44} {U} bebygd areal, alle tegnet med privat basseng.',
  'Nio bostäder som fortfarande är lediga i en etapp av en inhägnad anläggning intill en golfbana i östra Marbella: två trädgårdslägenheter, fyra takvåningar med solterrass på taket och tre parhus, med tre eller fyra sovrum och {N173.98} till {N264.44} {U} byggyta, alla ritade med egen pool.')
a(4, 'Nine homes beside a golf course',
  'Nueve viviendas junto a un campo de golf, en el este de Marbella: apartamentos con jardín, áticos con solárium y villas pareadas, de 174 a 264 {U} construidos, con piscina privada.',
  "Neuf logements près d'un golf, est de Marbella : appartements avec jardin, penthouses avec solarium sur le toit et villas jumelées, de 174 à 264 {U} construits, piscines privées.",
  'Neun Einheiten an einem Golfplatz in Ost-Marbella: Gartenwohnungen, Penthäuser mit Dachsolarium und Doppelhaushälften, 174 bis 264 {U} bebaut, eigene Pools.',
  'Девять объектов у гольф-поля на востоке Марбельи: квартиры с садом, пентхаусы с солярием на крыше и парные дома, от 174 до 264 {U} застройки, собственные бассейны.',
  'تسعة مساكن بجوار ملعب للغولف شرق ماربيا: شقق بحديقة، وبنتهاوس مع سولاريوم على السطح، وفلل شبه منفصلة، من 174 إلى 264 {U} مبنية، مع مسابح خاصة.',
  "Negen woningen naast een golfbaan in oost-Marbella: tuinappartementen, penthouses met solarium op het dak en halfvrijstaande villa's, 174 tot 264 {U} bebouwd, privézwembaden.",
  "Dziewięć nieruchomości przy polu golfowym we wschodniej Marbelli: mieszkania z ogrodem, penthouse'y z solarium na dachu i domy bliźniacze, od 174 do 264 {U} zabudowy, prywatne baseny.",
  'Ni boliger ved en golfbane øst i Marbella: hageleiligheter, toppleiligheter med solterrasse på taket og tomannsvillaer, 174 til 264 {U} bebygd areal, private bassenger.',
  'Nio bostäder intill en golfbana i östra Marbella: trädgårdslägenheter, takvåningar med solterrass på taket och parhus, 174 till 264 {U} byggyta, egna pooler.')
a(5, 'Garden apartments, penthouses',
  'Apartamentos con jardín, áticos y villas pareadas junto a un campo de golf, en el este de Marbella. Desde {E1300100} + IVA.',
  "Appartements avec jardin, penthouses et villas jumelées près d'un golf, dans l'est de Marbella. À partir de {E1300100} + TVA.",
  'Gartenwohnungen, Penthäuser und Doppelhaushälften an einem Golfplatz im Osten von Marbella. Ab {E1300100} zzgl. MwSt.',
  'Квартиры с садом, пентхаусы и парные дома рядом с гольф-полем на востоке Марбельи. От {E1300100} + НДС.',
  'شقق بحديقة وبنتهاوس وفلل شبه منفصلة بجوار ملعب للغولف شرق ماربيا. ابتداءً من {E1300100} + ضريبة القيمة المضافة.',
  "Tuinappartementen, penthouses en halfvrijstaande villa's naast een golfbaan in het oosten van Marbella. Vanaf {E1300100} + btw.",
  "Mieszkania z ogrodem, penthouse'y i domy bliźniacze przy polu golfowym we wschodniej Marbelli. Od {E1300100} + VAT.",
  'Hageleiligheter, toppleiligheter og tomannsvillaer ved en golfbane øst i Marbella. Fra {E1300100} + mva.',
  'Trädgårdslägenheter, takvåningar och parhus intill en golfbana i östra Marbella. Från {E1300100} + IVA (spansk moms).')
a(6, 'Nine homes available /',
  'Nueve viviendas disponibles / en construcción', 'Neuf logements disponibles / en construction', 'Neun Wohneinheiten verfügbar / im Bau',
  'Девять объектов в продаже / строится', 'تسعة مساكن متاحة / قيد الإنشاء', 'Negen woningen beschikbaar / in aanbouw',
  'Dziewięć nieruchomości dostępnych / w budowie', 'Ni boliger tilgjengelige / under bygging', 'Nio bostäder lediga / under uppförande')
a(8, 'Nine apartments, penthouses',
  'Nueve apartamentos, áticos y villas pareadas junto a un campo de golf, en el este de Marbella, con jardines, soláriums en la cubierta y piscinas privadas.',
  "Neuf appartements, penthouses et villas jumelées près d'un golf, dans l'est de Marbella, avec jardins, solariums sur le toit et piscines privées.",
  'Neun Wohnungen, Penthäuser und Doppelhaushälften an einem Golfplatz im Osten von Marbella, mit Gärten, Dachsolarien und eigenen Pools.',
  'Девять квартир, пентхаусов и парных домов рядом с гольф-полем на востоке Марбельи, с садами, соляриями на крыше и собственными бассейнами.',
  'تسع وحدات بين شقق وبنتهاوس وفلل شبه منفصلة بجوار ملعب للغولف شرق ماربيا، مع حدائق وسولاريوم على الأسطح ومسابح خاصة.',
  "Negen appartementen, penthouses en halfvrijstaande villa's naast een golfbaan in het oosten van Marbella, met tuinen, solariums op het dak en privézwembaden.",
  "Dziewięć mieszkań, penthouse'ów i domów bliźniaczych przy polu golfowym we wschodniej Marbelli, z ogrodami, solariami na dachach i prywatnymi basenami.",
  'Ni leiligheter, toppleiligheter og tomannsvillaer ved en golfbane øst i Marbella, med hager, solterrasser på taket og private bassenger.',
  'Nio lägenheter, takvåningar och parhus intill en golfbana i östra Marbella, med trädgårdar, solterrasser på taket och egna pooler.')
a(9, '2-4 bathrooms and a guest WC',
  '2-4 baños y un aseo', '2-4 salles de bain et un WC invités', '2-4 Badezimmer und ein Gäste-WC', '2-4 ванные комнаты и гостевой санузел',
  '2-4 حمامات وحمام للضيوف', '2-4 badkamers en een gastentoilet', '2-4 łazienki i toaleta dla gości', '2-4 bad og et gjestetoalett', '2-4 badrum och en gästtoalett')

# ---------------------------------------------------------------- images
a(10, 'The wider scheme from the air',
  'El conjunto completo desde el aire, bloques blancos entre palmeras, entre el campo de golf y el mar',
  "L'ensemble vu du ciel, des immeubles blancs parmi les palmiers, entre le golf et la mer",
  'Die gesamte Anlage aus der Luft, weiße Baukörper zwischen Palmen, zwischen Golfplatz und Meer',
  'Весь комплекс с высоты: белые корпуса среди пальм между гольф-полем и морем',
  'المجمع بأكمله من الجو، مبانٍ بيضاء بين أشجار النخيل بين ملعب الغولف والبحر',
  'Het hele complex vanuit de lucht, witte blokken tussen palmen, tussen de golfbaan en de zee',
  'Całe osiedle z lotu ptaka, białe budynki wśród palm między polem golfowym a morzem',
  'Hele anlegget sett ovenfra, hvite bygg blant palmer mellom golfbanen og havet',
  'Hela anläggningen från ovan, vita huskroppar bland palmer mellan golfbanan och havet')
a(11, 'Two-storey apartment blocks',
  'Bloques de apartamentos de dos plantas con terrazas amplias junto al vial de acceso',
  "Immeubles de deux niveaux aux terrasses profondes le long de la voie d'accès",
  'Zweigeschossige Wohnblöcke mit tiefen Terrassen an der Zufahrtsstraße',
  'Двухэтажные корпуса с квартирами и глубокими террасами вдоль подъездной дороги',
  'مبانٍ سكنية من طابقين بتراسات عميقة بجانب طريق الدخول',
  'Appartementsblokken van twee verdiepingen met diepe terrassen langs de toegangsweg',
  'Dwukondygnacyjne budynki z mieszkaniami i głębokimi tarasami przy drodze dojazdowej',
  'Leilighetsbygg i to etasjer med dype terrasser langs adkomstveien',
  'Lägenhetshus i två plan med djupa terrasser längs tillfartsvägen')
a(12, 'A communal pool with cabanas',
  'Una piscina comunitaria con cabañas y tumbonas delante de los bloques de apartamentos',
  'Une piscine commune avec cabanas et transats devant les immeubles',
  'Ein Gemeinschaftspool mit Cabanas und Liegen vor den Wohnblöcken',
  'Общий бассейн с шатрами и шезлонгами перед жилыми корпусами',
  'مسبح مشترك مع أكشاك ظليلة وكراسي استلقاء أمام المباني السكنية',
  "Een gemeenschappelijk zwembad met cabana's en ligbedden voor de appartementsblokken",
  'Basen wspólny z altanami i leżakami przed budynkami mieszkalnymi',
  'Et fellesbasseng med paviljonger og solsenger foran leilighetsbyggene',
  'En gemensam pool med paviljonger och solstolar framför lägenhetshusen')
a(13, 'A roof solarium with a private pool',
  'Un solárium en la cubierta con piscina privada y mesa de comedor, con vistas al mar',
  'Un solarium sur le toit avec piscine privée et table à manger, face à la mer',
  'Ein Dachsolarium mit eigenem Pool und Esstisch, mit Blick aufs Meer',
  'Солярий на крыше с собственным бассейном и обеденным столом, с видом на море',
  'سولاريوم على السطح مع مسبح خاص وطاولة طعام، مطل على البحر',
  'Een solarium op het dak met privézwembad en eettafel, met uitzicht op zee',
  'Solarium na dachu z prywatnym basenem i stołem jadalnym, z widokiem na morze',
  'En solterrasse på taket med privat basseng og spisebord, med utsikt mot havet',
  'En solterrass på taket med egen pool och matbord, med utsikt mot havet')
a(14, 'Computer-generated images',
  'Imágenes virtuales de las viviendas, las terrazas y las zonas comunes del conjunto. Ilustran el proyecto y no son los edificios terminados; el mobiliario y la decoración son orientativos y no están incluidos en la venta.',
  "Images de synthèse des logements, des terrasses et des parties communes de l'ensemble. Elles illustrent le projet et ne montrent pas les bâtiments achevés ; le mobilier et la décoration sont indicatifs et ne sont pas inclus dans la vente.",
  'Visualisierungen der Wohneinheiten, der Terrassen und der Gemeinschaftsflächen der gesamten Anlage. Sie veranschaulichen das Projekt und zeigen nicht die fertigen Gebäude; Möblierung und Dekoration sind beispielhaft und nicht Teil des Kaufs.',
  'Визуализации домов, террас и общих зон всего комплекса. Они иллюстрируют проект и не показывают готовые здания; мебель и декор показаны для примера и в продажу не входят.',
  'صور تخيلية للمساكن والتراسات والمرافق المشتركة في المجمع. وهي توضح المشروع ولا تمثل المباني المكتملة، والأثاث والديكور للتوضيح فقط وغير مشمولين في البيع.',
  'Impressies van de woningen, de terrassen en de gemeenschappelijke ruimtes van het hele complex. Ze illustreren het project en tonen niet de afgewerkte gebouwen; meubilair en decoratie zijn ter illustratie en horen niet bij de verkoop.',
  'Wizualizacje nieruchomości, tarasów i części wspólnych całego osiedla. Ilustrują projekt i nie przedstawiają gotowych budynków; meble i dekoracje mają charakter poglądowy i nie wchodzą w skład sprzedaży.',
  'Illustrasjoner av boligene, terrassene og fellesarealene i hele anlegget. De illustrerer prosjektet og viser ikke de ferdige byggene; møbler og innredning er ment som eksempler og inngår ikke i kjøpet.',
  'Illustrationer av bostäderna, terrasserna och de gemensamma ytorna i hela anläggningen. De illustrerar projektet och visar inte de färdiga byggnaderna; möbler och inredning är exempel och ingår inte i köpet.')
a(15, 'The gated entrance',
  'La entrada con cancela bajo una larga marquesina blanca, con el mar al fondo',
  "L'entrée fermée sous un long auvent blanc, avec la mer au loin",
  'Die Toreinfahrt unter einem langen weißen Vordach, dahinter das Meer',
  'Въезд с воротами под длинным белым навесом, вдали море',
  'المدخل ذو البوابة تحت مظلة بيضاء طويلة، والبحر في الخلفية',
  'De afgesloten entree onder een lange witte overkapping, met de zee in de verte',
  'Wjazd z bramą pod długim białym zadaszeniem, w oddali morze',
  'Inngangen med port under et langt hvitt tak, med havet i bakgrunnen',
  'Entrén med grindar under ett långt vitt skärmtak, med havet i fjärran')
a(16, 'The apartment blocks',
  'Los bloques de apartamentos', 'Les immeubles', 'Die Wohnblöcke', 'Жилые корпуса', 'المباني السكنية', 'De appartementsblokken',
  'Budynki mieszkalne', 'Leilighetsbyggene', 'Lägenhetshusen')
a(17, 'An internal street',
  'Una calle interior entre las viviendas, con palmeras, muros de piedra y el mar al final',
  'Une rue intérieure entre les logements, avec palmiers, murs de pierre et la mer au bout',
  'Eine interne Straße zwischen den Häusern mit Palmen, Steinmauern und dem Meer am Ende',
  'Внутренняя улица между домами: пальмы, каменные стены и море в конце',
  'شارع داخلي بين المساكن، مع أشجار النخيل وجدران حجرية والبحر في نهايته',
  'Een interne straat tussen de woningen, met palmen, natuurstenen muren en de zee aan het eind',
  'Wewnętrzna uliczka między domami, z palmami, kamiennymi murami i morzem na końcu',
  'En intern gate mellom boligene, med palmer, steinmurer og havet i enden',
  'En inre gata mellan bostäderna, med palmer, stenmurar och havet längst bort')
a(18, 'Towards the sea',
  'Hacia el mar', 'Vers la mer', 'Richtung Meer', 'К морю', 'نحو البحر', 'Richting zee', 'W stronę morza', 'Mot havet', 'Mot havet')
a(19, 'An apartment block above',
  'Un bloque de apartamentos sobre taludes plantados de gramíneas y lavanda',
  'Un immeuble au-dessus de talus plantés de graminées et de lavande',
  'Ein Wohnblock über bepflanzten Böschungen mit Gräsern und Lavendel',
  'Жилой корпус над склонами, засаженными злаками и лавандой',
  'مبنى سكني فوق منحدرات مزروعة بالأعشاب والخزامى',
  'Een appartementsblok boven beplante taluds met grassen en lavendel',
  'Budynek mieszkalny nad skarpami obsadzonymi trawami i lawendą',
  'Et leilighetsbygg over beplantede skråninger med gress og lavendel',
  'Ett lägenhetshus ovanför planterade slänter med gräs och lavendel')
a(20, 'A block with a wide',
  'Un bloque con una amplia terraza en la primera planta y las colinas detrás',
  'Un immeuble avec une large terrasse au premier étage et les collines derrière',
  'Ein Baukörper mit breiter Terrasse im ersten Obergeschoss, dahinter die Hügel',
  'Корпус с широкой террасой на втором этаже, за ним холмы',
  'مبنى بتراس واسع في الطابق الأول والتلال خلفه',
  'Een blok met een breed terras op de eerste verdieping en de heuvels erachter',
  'Budynek z szerokim tarasem na pierwszym piętrze i wzgórzami w tle',
  'Et bygg med en bred terrasse i andre etasje og åsene bak',
  'Ett hus med en bred terrass på första våningen och kullarna bakom')
a(21, 'The hills behind',
  'Las colinas detrás', 'Les collines derrière', 'Die Hügel dahinter', 'Холмы позади', 'التلال في الخلف', 'De heuvels erachter',
  'Wzgórza w tle', 'Åsene bak', 'Kullarna bakom')
a(22, 'A semi-detached villa at dusk',
  'Una villa pareada al anochecer, con la terraza y la piscina privada iluminadas',
  'Une villa jumelée au crépuscule, terrasse et piscine privée éclairées',
  'Eine Doppelhaushälfte in der Abenddämmerung, Terrasse und eigener Pool beleuchtet',
  'Парный дом в сумерках, с освещёнными террасой и собственным бассейном',
  'فيلا شبه منفصلة عند الغسق، مع إضاءة التراس والمسبح الخاص',
  'Een halfvrijstaande villa in de schemering, met verlicht terras en privézwembad',
  'Dom bliźniaczy o zmierzchu, z oświetlonym tarasem i prywatnym basenem',
  'En tomannsvilla i skumringen, med opplyst terrasse og privat basseng',
  'Ett parhus i skymningen, med upplyst terrass och egen pool')
a(23, 'A villa at dusk',
  'Una villa al anochecer', 'Une villa au crépuscule', 'Eine Villa in der Dämmerung', 'Вилла в сумерках', 'فيلا عند الغسق',
  'Een villa in de schemering', 'Willa o zmierzchu', 'En villa i skumringen', 'En villa i skymningen')
a(24, 'An infinity-edge communal pool',
  'Una piscina comunitaria desbordante con vistas a la costa',
  'Une piscine commune à débordement face à la côte',
  'Ein Gemeinschafts-Infinitypool mit Blick über die Küste',
  'Общий бассейн с эффектом бесконечности и видом на побережье',
  'مسبح مشترك لا متناهي الحافة يطل على الساحل',
  'Een gemeenschappelijk infinityzwembad met uitzicht over de kust',
  'Basen wspólny typu infinity z widokiem na wybrzeże',
  'Et felles infinitybasseng med utsikt over kysten',
  'En gemensam infinitypool med utsikt över kusten')
a(25, "The residents' gym",
  'El gimnasio de los residentes, abierto a una terraza junto a la piscina',
  'La salle de sport des résidents, ouverte sur une terrasse au bord de la piscine',
  'Der Fitnessraum der Bewohner, offen zu einer Poolterrasse',
  'Спортзал для жителей с выходом на террасу у бассейна',
  'صالة الرياضة للسكان، تنفتح على تراس بجانب المسبح',
  'De fitnessruimte voor bewoners, die uitkomt op een terras aan het zwembad',
  'Siłownia dla mieszkańców z wyjściem na taras przy basenie',
  'Treningsrommet for beboerne, åpent mot en bassengterrasse',
  'Gymmet för dem som bor här, öppet mot en poolterrass')
a(26, 'A ground-floor terrace with sofas',
  'Una terraza en planta baja con sofás junto a una piscina privada',
  "Une terrasse en rez-de-chaussée avec canapés au bord d'une piscine privée",
  'Eine Terrasse im Erdgeschoss mit Sofas neben einem eigenen Pool',
  'Терраса на первом этаже с диванами у собственного бассейна',
  'تراس في الطابق الأرضي مع أرائك بجانب مسبح خاص',
  'Een terras op de begane grond met banken naast een privézwembad',
  'Taras na parterze z sofami obok prywatnego basenu',
  'En terrasse i første etasje med sofaer ved et privat basseng',
  'En terrass på bottenvåningen med soffor intill en egen pool')
a(27, 'A garden terrace',
  'Una terraza con jardín', 'Une terrasse sur jardin', 'Eine Gartenterrasse', 'Терраса с садом', 'تراس بحديقة', 'Een tuinterras',
  'Taras z ogrodem', 'En hageterrasse', 'En trädgårdsterrass')
a(28, 'A covered terrace under a pergola',
  'Una terraza cubierta bajo una pérgola, con sofás y las montañas al fondo',
  'Une terrasse couverte sous une pergola, avec canapés et les montagnes au loin',
  'Eine überdachte Terrasse unter einer Pergola mit Sofas und den Bergen in der Ferne',
  'Крытая терраса под перголой с диванами и видом на горы',
  'تراس مسقوف تحت عريشة، مع أرائك والجبال في الأفق',
  'Een overdekt terras onder een pergola, met banken en de bergen in de verte',
  'Zadaszony taras pod pergolą, z sofami i górami w oddali',
  'En overbygd terrasse under en pergola, med sofaer og fjellene i bakgrunnen',
  'En överbyggd terrass under en pergola, med soffor och bergen i fjärran')
a(29, 'A roof solarium',
  'Un solárium en la cubierta', 'Un solarium sur le toit', 'Ein Dachsolarium', 'Солярий на крыше', 'سولاريوم على السطح',
  'Een solarium op het dak', 'Solarium na dachu', 'En solterrasse på taket', 'En solterrass på taket')
a(30, 'The view from a roof solarium',
  'La vista desde un solárium en la cubierta, sobre el conjunto hasta el mar',
  "La vue depuis un solarium sur le toit, par-dessus l'ensemble jusqu'à la mer",
  'Der Blick von einem Dachsolarium über die Anlage bis zum Meer',
  'Вид с солярия на крыше на комплекс и море',
  'الإطلالة من سولاريوم على السطح فوق المجمع حتى البحر',
  'Het uitzicht vanaf een solarium op het dak over het complex naar zee',
  'Widok z solarium na dachu ponad osiedlem aż po morze',
  'Utsikten fra en solterrasse på taket over anlegget mot havet',
  'Utsikten från en solterrass på taket över anläggningen mot havet')
a(31, 'The view from the roof',
  'La vista desde la cubierta', 'La vue depuis le toit', 'Der Blick vom Dach', 'Вид с крыши', 'الإطلالة من السطح',
  'Het uitzicht vanaf het dak', 'Widok z dachu', 'Utsikten fra taket', 'Utsikten från taket')
a(32, 'A villa roof terrace with an outdoor kitchen',
  'Una terraza en la cubierta de una villa con cocina exterior, que el folleto incluye entre los extras opcionales',
  "Un toit-terrasse de villa avec cuisine d'extérieur, que la brochure présente comme une option",
  'Eine Dachterrasse einer Villa mit Außenküche, die in der Broschüre als Sonderausstattung aufgeführt ist',
  'Терраса на крыше виллы с летней кухней, которую буклет относит к дополнительным опциям',
  'تراس على سطح فيلا مع مطبخ خارجي، يدرجه الكتيب ضمن الإضافات الاختيارية',
  'Een dakterras van een villa met buitenkeuken, die de brochure als optie vermeldt',
  'Taras na dachu willi z kuchnią zewnętrzną, którą broszura wymienia jako dodatkową opcję',
  'En takterrasse på en villa med utekjøkken, som brosjyren oppgir som tilvalg',
  'En takterrass på en villa med utekök, som broschyren anger som tillval')
a(33, 'A villa roof terrace',
  'La terraza en la cubierta de una villa', "Le toit-terrasse d'une villa", 'Die Dachterrasse einer Villa', 'Терраса на крыше виллы',
  'تراس على سطح فيلا', 'Het dakterras van een villa', 'Taras na dachu willi', 'Takterrassen på en villa', 'Takterrassen på en villa')
a(34, 'The living room, with sofas',
  'El salón, con sofás y puertas correderas a la terraza',
  'Le séjour, avec canapés et baies coulissantes ouvrant sur la terrasse',
  'Der Wohnraum mit Sofas und Schiebetüren zur Terrasse',
  'Гостиная с диванами и раздвижными дверями на террасу',
  'صالة المعيشة، مع أرائك وأبواب منزلقة إلى التراس',
  'De woonkamer, met banken en schuifpuien naar het terras',
  'Salon z sofami i przesuwnymi drzwiami na taras',
  'Stuen, med sofaer og skyvedører ut til terrassen',
  'Vardagsrummet, med soffor och skjutdörrar ut mot terrassen')
a(35, 'The main bedroom, with a sliding',
  'El dormitorio principal, con un ventanal corredero a la terraza',
  'La chambre principale, avec une baie coulissante sur la terrasse',
  'Das Hauptschlafzimmer mit Schiebefenster zur Terrasse',
  'Главная спальня с раздвижным окном на террасу',
  'غرفة النوم الرئيسية، مع نافذة منزلقة على التراس',
  'De hoofdslaapkamer, met een schuifraam naar het terras',
  'Sypialnia główna z przesuwnym oknem na taras',
  'Hovedsoverommet, med skyvevindu ut mot terrassen',
  'Huvudsovrummet, med ett skjutfönster mot terrassen')

# ---------------------------------------------------------------- overview and residences
a(36, 'Nine homes, <em>',
  'Nueve viviendas, <em>tres tipos</em>', 'Neuf logements, <em>trois types</em>', 'Neun Einheiten, <em>drei Typen</em>',
  'Девять объектов, <em>три типа</em>', 'تسعة مساكن، <em>ثلاثة أنواع</em>', 'Negen woningen, <em>drie typen</em>',
  'Dziewięć nieruchomości, <em>trzy typy</em>', 'Ni boliger, <em>tre typer</em>', 'Nio bostäder, <em>tre typer</em>')
a(37, 'Golfside Hill Residences is one phase',
  'Golfside Hill Residences es una fase de un conjunto cerrado más amplio, en una zona elevada junto a un campo de golf, en el este de Marbella, con edificaciones blancas de poca altura y el mar enfrente. Nueve de sus viviendas están disponibles: dos apartamentos con jardín en planta baja, cuatro áticos en primera planta con solárium en la cubierta y tres villas pareadas de tres niveles.',
  "Golfside Hill Residences est une phase d'un ensemble fermé plus vaste, sur une hauteur voisine d'un golf, dans l'est de Marbella, avec des bâtiments blancs de faible hauteur et la mer en face. Neuf de ses logements sont disponibles : deux appartements avec jardin en rez-de-chaussée, quatre penthouses au premier étage avec solarium sur le toit et trois villas jumelées sur trois niveaux.",
  'Golfside Hill Residences ist ein Bauabschnitt einer größeren geschlossenen Wohnanlage auf erhöhtem Gelände an einem Golfplatz im Osten von Marbella, mit niedrigen weißen Baukörpern und dem Meer davor. Neun der Einheiten sind verfügbar: zwei Gartenwohnungen im Erdgeschoss, vier Penthäuser im ersten Obergeschoss mit Dachsolarium und drei Doppelhaushälften auf drei Ebenen.',
  'Golfside Hill Residences — одна из очередей большого закрытого комплекса на возвышенности рядом с гольф-полем на востоке Марбельи: невысокие белые корпуса и море впереди. В продаже девять объектов: две квартиры с садом на первом этаже, четыре пентхауса на втором этаже с солярием на крыше и три трёхуровневых парных дома.',
  'Golfside Hill Residences مرحلة من مجمع مسوّر أكبر على أرض مرتفعة بجوار ملعب للغولف شرق ماربيا، بمبانٍ بيضاء منخفضة والبحر أمامها. تسعة من مساكنها متاحة: شقتان بحديقة في الطابق الأرضي، وأربع شقق بنتهاوس في الطابق الأول مع سولاريوم على السطح، وثلاث فلل شبه منفصلة من ثلاثة مستويات.',
  "Golfside Hill Residences is een fase van een groter omheind complex op een hoger gelegen terrein naast een golfbaan in het oosten van Marbella, met lage witte bouwblokken en de zee ervoor. Negen woningen zijn beschikbaar: twee tuinappartementen op de begane grond, vier penthouses op de eerste verdieping met een solarium op het dak en drie halfvrijstaande villa's op drie niveaus.",
  "Golfside Hill Residences to jeden z etapów większego zamkniętego osiedla na wzniesieniu przy polu golfowym we wschodniej Marbelli, z niskimi białymi budynkami i morzem przed nimi. Dostępnych jest dziewięć nieruchomości: dwa mieszkania z ogrodem na parterze, cztery penthouse'y na pierwszym piętrze z solarium na dachu i trzy trzypoziomowe domy bliźniacze.",
  'Golfside Hill Residences er ett byggetrinn i et større inngjerdet anlegg på høyereliggende grunn ved en golfbane øst i Marbella, med lave hvite bygg og havet foran. Ni av boligene er tilgjengelige: to hageleiligheter i første etasje, fire toppleiligheter i andre etasje med solterrasse på taket og tre tomannsvillaer i tre plan.',
  'Golfside Hill Residences är en etapp i en större inhägnad anläggning på en höjd intill en golfbana i östra Marbella, med låga vita huskroppar och havet framför. Nio av bostäderna är lediga: två trädgårdslägenheter på bottenvåningen, fyra takvåningar på första våningen med solterrass på taket och tre parhus i tre plan.')
a(38, 'The available homes run from',
  'Las viviendas disponibles tienen de {N173.98} a {N264.44} {U} construidos, con {N139.52} a {N213.48} {U} útiles interiores, y tres o cuatro dormitorios. Sus terrazas suman de {N134.11} a {N220.63} {U}, contando el solárium y la piscina cuando los hay. Las nueve están orientadas al suroeste.',
  "Les logements disponibles vont de {N173.98} à {N264.44} {U} construits, avec {N139.52} à {N213.48} {U} de surface utile intérieure, et comptent trois ou quatre chambres. Leurs terrasses vont de {N134.11} à {N220.63} {U}, solarium et piscine compris lorsqu'il y en a. Les neuf sont orientés au sud-ouest.",
  'Die verfügbaren Einheiten haben {N173.98} bis {N264.44} {U} bebaute Fläche bei {N139.52} bis {N213.48} {U} Nutzfläche innen und drei oder vier Schlafzimmer. Ihre Terrassen umfassen {N134.11} bis {N220.63} {U}, Solarium und Pool eingerechnet, wo vorhanden. Alle neun sind nach Südwesten ausgerichtet.',
  'Площадь застройки доступных объектов — от {N173.98} до {N264.44} {U}, полезная площадь внутри — от {N139.52} до {N213.48} {U}, спален три или четыре. Террасы — от {N134.11} до {N220.63} {U}, включая солярий и бассейн, если они есть. Все девять ориентированы на юго-запад.',
  'تتراوح المساحة المبنية للمساكن المتاحة بين {N173.98} و{N264.44} {U}، والمساحة الداخلية الصافية بين {N139.52} و{N213.48} {U}، وفيها ثلاث أو أربع غرف نوم. وتتراوح تراساتها بين {N134.11} و{N220.63} {U}، بما في ذلك السولاريوم والمسبح حيث يوجدان. والمساكن التسعة كلها موجهة نحو الجنوب الغربي.',
  'De beschikbare woningen meten {N173.98} tot {N264.44} {U} bebouwd, met {N139.52} tot {N213.48} {U} nuttige binnenoppervlakte, en hebben drie of vier slaapkamers. Hun terrassen meten {N134.11} tot {N220.63} {U}, inclusief solarium en zwembad waar die er zijn. Alle negen liggen op het zuidwesten.',
  'Dostępne nieruchomości mają od {N173.98} do {N264.44} {U} powierzchni zabudowy i od {N139.52} do {N213.48} {U} powierzchni użytkowej wewnątrz oraz trzy lub cztery sypialnie. Ich tarasy mają od {N134.11} do {N220.63} {U}, wliczając solarium i basen tam, gdzie są. Wszystkie dziewięć ma ekspozycję południowo-zachodnią.',
  'De tilgjengelige boligene har fra {N173.98} til {N264.44} {U} bebygd areal og {N139.52} til {N213.48} {U} innvendig nyttbart areal, med tre eller fire soverom. Terrassene er på {N134.11} til {N220.63} {U}, solterrasse og basseng medregnet der de finnes. Alle ni vender mot sørvest.',
  'De lediga bostäderna har {N173.98} till {N264.44} {U} byggyta och {N139.52} till {N213.48} {U} invändig nyttoyta, med tre eller fyra sovrum. Terrasserna är på {N134.11} till {N220.63} {U}, solterrass och pool inräknade där de finns. Alla nio vetter mot sydväst.')
a(39, 'Residents share the communal areas of the whole',
  'Los residentes comparten las zonas comunes de todo el conjunto: el folleto enumera cuatro piscinas exteriores y una cubierta, un spa con sauna y baño turco, gimnasio, zona de coworking, cafetería, servicio de conserjería y un centro de bicicletas eléctricas. Cada vivienda lleva dos plazas de garaje y un trastero, con precio aparte.',
  "Les résidents partagent les parties communes de tout l'ensemble : la brochure cite quatre piscines extérieures et une piscine couverte, un spa avec sauna et hammam, une salle de sport, un espace de coworking, un café, un service de conciergerie et un centre de vélos électriques. Chaque logement s'accompagne de deux places de parking et d'un débarras, facturés à part.",
  'Die Bewohner teilen die Gemeinschaftsbereiche der gesamten Anlage: Die Broschüre nennt vier Außenpools und ein Hallenbad, ein Spa mit Sauna und türkischem Bad, einen Fitnessraum, einen Coworking-Bereich, ein Café, einen Concierge-Service und eine E-Bike-Station. Zu jeder Einheit gehören zwei Stellplätze und ein Abstellraum, die gesondert berechnet werden.',
  'Жители пользуются общими зонами всего комплекса: в буклете перечислены четыре открытых бассейна и крытый бассейн, спа с сауной и турецкой баней, спортзал, коворкинг, кафе, консьерж-сервис и центр электровелосипедов. К каждому объекту прилагаются два парковочных места и кладовая, они оплачиваются отдельно.',
  'يتشارك السكان المرافق المشتركة للمجمع بأكمله: يذكر الكتيب أربعة مسابح خارجية ومسبحًا داخليًا، وسبا مع ساونا وحمام تركي، وصالة رياضة، ومساحة عمل مشتركة، ومقهى، وخدمة كونسيرج، ومركزًا للدراجات الكهربائية. ويأتي مع كل مسكن موقفا سيارات ومخزن بسعر منفصل.',
  'Bewoners delen de gemeenschappelijke voorzieningen van het hele complex: de brochure noemt vier buitenzwembaden en een binnenzwembad, een spa met sauna en Turks bad, een fitnessruimte, een coworkingruimte, een koffiebar, een conciërgeservice en een e-bikecentrum. Bij elke woning horen twee parkeerplaatsen en een berging, apart geprijsd.',
  'Mieszkańcy korzystają z części wspólnych całego osiedla: broszura wymienia cztery baseny zewnętrzne i basen kryty, spa z sauną i łaźnią turecką, siłownię, strefę coworkingu, kawiarnię, usługę concierge i centrum rowerów elektrycznych. Do każdej nieruchomości przypisane są dwa miejsca postojowe i komórka lokatorska, wyceniane osobno.',
  'Beboerne deler fellesarealene i hele anlegget: brosjyren nevner fire utendørsbassenger og et innendørsbasseng, et spa med badstue og tyrkisk bad, treningsrom, et coworking-område, en kafé, en concierge-tjeneste og et senter for elsykler. Til hver bolig hører to parkeringsplasser og en bod, priset separat.',
  'De som bor här delar de gemensamma ytorna i hela anläggningen: broschyren nämner fyra utomhuspooler och en inomhuspool, ett spa med bastu och turkiskt bad, ett gym, en coworkingyta, ett kafé, en conciergeservice och en elcykelcentral. Till varje bostad hör två parkeringsplatser och ett förråd, prissatta separat.')
a(40, 'Three ways <em>',
  'Tres formas <em>de vivir aquí</em>', "Trois façons <em>d'habiter ici</em>", 'Drei Arten, <em>hier zu wohnen</em>',
  'Три формата <em>жизни здесь</em>', 'ثلاث طرق <em>للعيش هنا</em>', 'Drie manieren <em>om hier te wonen</em>',
  'Trzy sposoby <em>na życie tutaj</em>', 'Tre måter <em>å bo her på</em>', 'Tre sätt <em>att bo här</em>')
a(41, 'Two garden apartments, four penthouses and three semi-detached villas. The table',
  'Dos apartamentos con jardín, cuatro áticos y tres villas pareadas. La tabla siguiente sigue la lista del portal del promotor y sus planos de vivienda.',
  'Deux appartements avec jardin, quatre penthouses et trois villas jumelées. Le tableau ci-dessous suit la liste du portail du promoteur et ses plans de logement.',
  'Zwei Gartenwohnungen, vier Penthäuser und drei Doppelhaushälften. Die Tabelle unten folgt der Portalliste des Bauträgers und seinen Grundrissen.',
  'Две квартиры с садом, четыре пентхауса и три парных дома. Таблица ниже составлена по списку на портале застройщика и его поэтажным планам.',
  'شقتان بحديقة، وأربع شقق بنتهاوس، وثلاث فلل شبه منفصلة. يتبع الجدول أدناه قائمة بوابة المطور ومخططات وحداته.',
  "Twee tuinappartementen, vier penthouses en drie halfvrijstaande villa's. De tabel hieronder volgt de lijst op het portaal van de ontwikkelaar en zijn woningplattegronden.",
  "Dwa mieszkania z ogrodem, cztery penthouse'y i trzy domy bliźniacze. Poniższa tabela odpowiada liście z portalu dewelopera i jego rzutom.",
  'To hageleiligheter, fire toppleiligheter og tre tomannsvillaer. Tabellen nedenfor følger listen i utbyggerens portal og plantegningene.',
  'Två trädgårdslägenheter, fyra takvåningar och tre parhus. Tabellen nedan följer listan i exploatörens portal och ritningarna.')
a(42, 'The garden apartments',
  'Los apartamentos con jardín', 'Les appartements avec jardin', 'Die Gartenwohnungen', 'Квартиры с садом', 'الشقق ذات الحديقة',
  'De tuinappartementen', 'Mieszkania z ogrodem', 'Hageleilighetene', 'Trädgårdslägenheterna')
a(43, 'Four bedrooms, three bathrooms and a guest WC, on the ground',
  'Cuatro dormitorios, tres baños y un aseo, en la planta baja de los bloques 20 y 28.',
  'Quatre chambres, trois salles de bain et un WC invités, au rez-de-chaussée des blocs 20 et 28.',
  'Vier Schlafzimmer, drei Badezimmer und ein Gäste-WC, im Erdgeschoss der Blöcke 20 und 28.',
  'Четыре спальни, три ванные комнаты и гостевой санузел, на первом этаже корпусов 20 и 28.',
  'أربع غرف نوم وثلاثة حمامات وحمام للضيوف، في الطابق الأرضي من المبنيين 20 و28.',
  'Vier slaapkamers, drie badkamers en een gastentoilet, op de begane grond van blok 20 en 28.',
  'Cztery sypialnie, trzy łazienki i toaleta dla gości, na parterze budynków 20 i 28.',
  'Fire soverom, tre bad og et gjestetoalett, i første etasje i hus 20 og 28.',
  'Fyra sovrum, tre badrum och en gästtoalett, på bottenvåningen i hus 20 och 28.')
a(44, '180.62 sqm of usable interior',
  '{N180.62} {U} útiles interiores, con {N144.44} a {N149.29} {U} de terraza cubierta y descubierta.',
  '{N180.62} {U} de surface utile intérieure, avec {N144.44} à {N149.29} {U} de terrasse couverte et ouverte.',
  '{N180.62} {U} Nutzfläche innen, dazu {N144.44} bis {N149.29} {U} überdachte und offene Terrasse.',
  '{N180.62} {U} полезной площади внутри и от {N144.44} до {N149.29} {U} крытой и открытой террасы.',
  '{N180.62} {U} مساحة داخلية صافية، مع {N144.44} إلى {N149.29} {U} من التراس المسقوف والمكشوف.',
  '{N180.62} {U} nuttige binnenoppervlakte, met {N144.44} tot {N149.29} {U} overdekt en open terras.',
  '{N180.62} {U} powierzchni użytkowej wewnątrz oraz od {N144.44} do {N149.29} {U} tarasu zadaszonego i otwartego.',
  '{N180.62} {U} innvendig nyttbart areal, med {N144.44} til {N149.29} {U} overbygd og åpen terrasse.',
  '{N180.62} {U} invändig nyttoyta, med {N144.44} till {N149.29} {U} överbyggd och öppen terrass.')
a(45, 'A private garden of 195.51',
  'Un jardín privado de {N195.51} a {N201.96} {U} y una piscina privada de {N11.80} {U}.',
  'Un jardin privé de {N195.51} à {N201.96} {U} et une piscine privée de {N11.80} {U}.',
  'Ein eigener Garten von {N195.51} bis {N201.96} {U} und ein eigener Pool von {N11.80} {U}.',
  'Собственный сад от {N195.51} до {N201.96} {U} и собственный бассейн {N11.80} {U}.',
  'حديقة خاصة من {N195.51} إلى {N201.96} {U} ومسبح خاص بمساحة {N11.80} {U}.',
  'Een privétuin van {N195.51} tot {N201.96} {U} en een privézwembad van {N11.80} {U}.',
  'Prywatny ogród o powierzchni od {N195.51} do {N201.96} {U} i prywatny basen o powierzchni {N11.80} {U}.',
  'En privat hage på {N195.51} til {N201.96} {U} og et privat basseng på {N11.80} {U}.',
  'En egen trädgård på {N195.51} till {N201.96} {U} och en egen pool på {N11.80} {U}.')
a(46, 'A separate room of 16.15',
  'Una estancia independiente de {N16.15} {U} junto a un patio ajardinado, dibujada como gimnasio.',
  'Une pièce indépendante de {N16.15} {U} donnant sur un jardin intérieur, dessinée comme salle de sport.',
  'Ein separater Raum von {N16.15} {U} an einem Innengarten, im Plan als Fitnessraum eingezeichnet.',
  'Отдельное помещение {N16.15} {U} у внутреннего сада, на плане обозначенное как спортзал.',
  'غرفة مستقلة بمساحة {N16.15} {U} تطل على حديقة داخلية، مرسومة في المخطط كصالة رياضة.',
  'Een aparte ruimte van {N16.15} {U} aan een binnentuin, op tekening als fitnessruimte.',
  'Osobne pomieszczenie o powierzchni {N16.15} {U} przy wewnętrznym ogrodzie, oznaczone na rzucie jako siłownia.',
  'Et separat rom på {N16.15} {U} ved en indre hage, tegnet som treningsrom.',
  'Ett separat rum på {N16.15} {U} vid en inre trädgård, ritat som gym.')
a(47, 'Three or four bedrooms, two to four',
  'Tres o cuatro dormitorios, de dos a cuatro baños y un aseo, en la primera planta de los bloques 19 y 20.',
  'Trois ou quatre chambres, deux à quatre salles de bain et un WC invités, au premier étage des blocs 19 et 20.',
  'Drei oder vier Schlafzimmer, zwei bis vier Badezimmer und ein Gäste-WC, im ersten Obergeschoss der Blöcke 19 und 20.',
  'Три или четыре спальни, от двух до четырёх ванных комнат и гостевой санузел, на втором этаже корпусов 19 и 20.',
  'ثلاث أو أربع غرف نوم، ومن حمامين إلى أربعة حمامات، وحمام للضيوف، في الطابق الأول من المبنيين 19 و20.',
  'Drie of vier slaapkamers, twee tot vier badkamers en een gastentoilet, op de eerste verdieping van blok 19 en 20.',
  'Trzy lub cztery sypialnie, od dwóch do czterech łazienek i toaleta dla gości, na pierwszym piętrze budynków 19 i 20.',
  'Tre eller fire soverom, to til fire bad og et gjestetoalett, i andre etasje i hus 19 og 20.',
  'Tre eller fyra sovrum, två till fyra badrum och en gästtoalett, på första våningen i hus 19 och 20.')
a(48, '139.52 to 196.58',
  'De {N139.52} a {N196.58} {U} útiles interiores, con terrazas cubiertas y descubiertas junto al salón.',
  'De {N139.52} à {N196.58} {U} de surface utile intérieure, avec des terrasses couvertes et ouvertes dans le prolongement du séjour.',
  '{N139.52} bis {N196.58} {U} Nutzfläche innen, mit überdachten und offenen Terrassen am Wohnraum.',
  'От {N139.52} до {N196.58} {U} полезной площади внутри, с крытыми и открытыми террасами при гостиной.',
  'من {N139.52} إلى {N196.58} {U} مساحة داخلية صافية، مع تراسات مسقوفة ومكشوفة متصلة بصالة المعيشة.',
  '{N139.52} tot {N196.58} {U} nuttige binnenoppervlakte, met overdekte en open terrassen aan de woonkamer.',
  'Od {N139.52} do {N196.58} {U} powierzchni użytkowej wewnątrz, z tarasami zadaszonymi i otwartymi przy salonie.',
  '{N139.52} til {N196.58} {U} innvendig nyttbart areal, med overbygde og åpne terrasser ut fra stuen.',
  '{N139.52} till {N196.58} {U} invändig nyttoyta, med överbyggda och öppna terrasser i anslutning till vardagsrummet.')
a(49, 'A roof solarium of 60.30',
  'Un solárium en la cubierta de {N60.30} a {N96.08} {U}, con acceso por una escalera interior, dibujado con una piscina de {N11.60} a {N15.55} {U}.',
  'Un solarium sur le toit de {N60.30} à {N96.08} {U}, accessible par un escalier intérieur, dessiné avec une piscine de {N11.60} à {N15.55} {U}.',
  'Ein Dachsolarium von {N60.30} bis {N96.08} {U} über eine Innentreppe, im Plan mit einem Pool von {N11.60} bis {N15.55} {U}.',
  'Солярий на крыше площадью от {N60.30} до {N96.08} {U} с выходом по внутренней лестнице, на плане — с бассейном от {N11.60} до {N15.55} {U}.',
  'سولاريوم على السطح من {N60.30} إلى {N96.08} {U} يُصعد إليه بدرج داخلي، مرسوم مع مسبح من {N11.60} إلى {N15.55} {U}.',
  'Een solarium op het dak van {N60.30} tot {N96.08} {U}, bereikbaar via een binnentrap, op tekening met een zwembad van {N11.60} tot {N15.55} {U}.',
  'Solarium na dachu o powierzchni od {N60.30} do {N96.08} {U}, dostępne wewnętrznymi schodami, na rzucie z basenem od {N11.60} do {N15.55} {U}.',
  'En solterrasse på taket på {N60.30} til {N96.08} {U}, med adkomst via en innvendig trapp, tegnet med et basseng på {N11.60} til {N15.55} {U}.',
  'En solterrass på taket på {N60.30} till {N96.08} {U}, som nås via en invändig trappa, ritad med en pool på {N11.60} till {N15.55} {U}.')
a(50, 'The brochure lists the solarium with pool',
  'El folleto incluye el solárium con piscina entre los extras opcionales, así que confirmamos por escrito qué incluye el precio.',
  'La brochure range le solarium avec piscine parmi les options, nous confirmons donc par écrit ce que comprend le prix.',
  'Die Broschüre führt das Solarium mit Pool unter den Sonderausstattungen auf; deshalb bestätigen wir schriftlich, was im Preis enthalten ist.',
  'Буклет относит солярий с бассейном к дополнительным опциям, поэтому мы письменно подтверждаем, что входит в цену.',
  'يدرج الكتيب السولاريوم مع المسبح ضمن الإضافات الاختيارية، لذلك نؤكد كتابيًا ما يشمله السعر.',
  'De brochure noemt het solarium met zwembad bij de opties, dus wij bevestigen schriftelijk wat de prijs omvat.',
  'Broszura wymienia solarium z basenem wśród opcji dodatkowych, dlatego na piśmie potwierdzamy, co obejmuje cena.',
  'Brosjyren oppgir solterrassen med basseng som tilvalg, så vi bekrefter skriftlig hva prisen omfatter.',
  'Broschyren anger solterrassen med pool som tillval, så vi bekräftar skriftligt vad priset omfattar.')
a(51, 'The semi-detached villas',
  'Las villas pareadas', 'Les villas jumelées', 'Die Doppelhaushälften', 'Парные дома', 'الفلل شبه المنفصلة',
  "De halfvrijstaande villa's", 'Domy bliźniacze', 'Tomannsvillaene', 'Parhusen')
a(52, 'Four bedrooms, three bathrooms and a guest WC over',
  'Cuatro dormitorios, tres baños y un aseo repartidos entre planta baja, primera planta y un solárium en la cubierta de {N90.81} {U}.',
  'Quatre chambres, trois salles de bain et un WC invités répartis sur un rez-de-chaussée, un premier étage et un solarium sur le toit de {N90.81} {U}.',
  'Vier Schlafzimmer, drei Badezimmer und ein Gäste-WC auf Erdgeschoss, erstem Obergeschoss und einem Dachsolarium von {N90.81} {U}.',
  'Четыре спальни, три ванные комнаты и гостевой санузел на первом и втором этажах, плюс солярий на крыше площадью {N90.81} {U}.',
  'أربع غرف نوم وثلاثة حمامات وحمام للضيوف موزعة على طابق أرضي وطابق أول وسولاريوم على السطح بمساحة {N90.81} {U}.',
  'Vier slaapkamers, drie badkamers en een gastentoilet over een begane grond, een eerste verdieping en een solarium op het dak van {N90.81} {U}.',
  'Cztery sypialnie, trzy łazienki i toaleta dla gości na parterze i pierwszym piętrze oraz solarium na dachu o powierzchni {N90.81} {U}.',
  'Fire soverom, tre bad og et gjestetoalett fordelt på første etasje, andre etasje og en solterrasse på taket på {N90.81} {U}.',
  'Fyra sovrum, tre badrum och en gästtoalett fördelade på bottenvåning, första våning och en solterrass på taket på {N90.81} {U}.')
a(53, 'The living room, the kitchen and one bedroom',
  'El salón, la cocina y un dormitorio en planta baja, abiertos a la terraza, a una piscina privada de {N15.00} {U} y al jardín.',
  'Le séjour, la cuisine et une chambre au rez-de-chaussée, ouverts sur la terrasse, une piscine privée de {N15.00} {U} et le jardin.',
  'Wohnraum, Küche und ein Schlafzimmer im Erdgeschoss, offen zur Terrasse, zu einem eigenen Pool von {N15.00} {U} und zum Garten.',
  'Гостиная, кухня и одна спальня на первом этаже с выходом на террасу, к собственному бассейну {N15.00} {U} и в сад.',
  'صالة المعيشة والمطبخ وغرفة نوم في الطابق الأرضي، تنفتح على التراس ومسبح خاص بمساحة {N15.00} {U} والحديقة.',
  'De woonkamer, de keuken en één slaapkamer op de begane grond, met toegang tot het terras, een privézwembad van {N15.00} {U} en de tuin.',
  'Salon, kuchnia i jedna sypialnia na parterze, z wyjściem na taras, do prywatnego basenu o powierzchni {N15.00} {U} i do ogrodu.',
  'Stue, kjøkken og ett soverom i første etasje, med utgang til terrassen, et privat basseng på {N15.00} {U} og hagen.',
  'Vardagsrum, kök och ett sovrum på bottenvåningen, med utgång till terrassen, en egen pool på {N15.00} {U} och trädgården.')
a(54, 'Three more bedrooms',
  'Otros tres dormitorios y dos baños en la primera planta, con terrazas propias.',
  'Trois autres chambres et deux salles de bain au premier étage, avec leurs propres terrasses.',
  'Drei weitere Schlafzimmer und zwei Badezimmer im ersten Obergeschoss, mit eigenen Terrassen.',
  'Ещё три спальни и две ванные комнаты на втором этаже, со своими террасами.',
  'ثلاث غرف نوم أخرى وحمامان في الطابق الأول، مع تراسات خاصة بها.',
  'Nog drie slaapkamers en twee badkamers op de eerste verdieping, met eigen terrassen.',
  'Kolejne trzy sypialnie i dwie łazienki na pierwszym piętrze, z własnymi tarasami.',
  'Ytterligere tre soverom og to bad i andre etasje, med egne terrasser.',
  'Ytterligare tre sovrum och två badrum på första våningen, med egna terrasser.')
a(55, '213.48 sqm of usable',
  '{N213.48} {U} útiles interiores y {N220.63} {U} de terrazas, solárium y piscina.',
  '{N213.48} {U} de surface utile intérieure et {N220.63} {U} de terrasses, solarium et piscine.',
  '{N213.48} {U} Nutzfläche innen und {N220.63} {U} Terrassen, Solarium und Pool.',
  '{N213.48} {U} полезной площади внутри и {N220.63} {U} террас, солярия и бассейна.',
  '{N213.48} {U} مساحة داخلية صافية و{N220.63} {U} من التراسات والسولاريوم والمسبح.',
  '{N213.48} {U} nuttige binnenoppervlakte en {N220.63} {U} aan terrassen, solarium en zwembad.',
  '{N213.48} {U} powierzchni użytkowej wewnątrz i {N220.63} {U} tarasów, solarium i basenu.',
  '{N213.48} {U} innvendig nyttbart areal og {N220.63} {U} terrasser, solterrasse og basseng.',
  '{N213.48} {U} invändig nyttoyta och {N220.63} {U} terrasser, solterrass och pool.')

# ---------------------------------------------------------------- availability
a(56, 'Nine homes are available',
  'Hay nueve viviendas disponibles: dos apartamentos con jardín, cuatro áticos y tres villas pareadas. Cada una lleva dos plazas de garaje y un trastero, con precio aparte. Nueva Living reconfirma precio y disponibilidad antes de cualquier visita o reserva.',
  "Neuf logements sont disponibles : deux appartements avec jardin, quatre penthouses et trois villas jumelées. Chacun s'accompagne de deux places de parking et d'un débarras, facturés à part. Nueva Living reconfirme le prix et la disponibilité avant toute visite ou réservation.",
  'Neun Einheiten sind verfügbar: zwei Gartenwohnungen, vier Penthäuser und drei Doppelhaushälften. Zu jeder gehören zwei Stellplätze und ein Abstellraum, die gesondert berechnet werden. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung erneut.',
  'В продаже девять объектов: две квартиры с садом, четыре пентхауса и три парных дома. К каждому прилагаются два парковочных места и кладовая, оплачиваемые отдельно. Nueva Living заново подтверждает цену и наличие перед любым просмотром или бронированием.',
  'تتوفر تسعة مساكن: شقتان بحديقة، وأربع شقق بنتهاوس، وثلاث فلل شبه منفصلة. ويأتي مع كل منها موقفا سيارات ومخزن بسعر منفصل. تعيد Nueva Living تأكيد السعر والتوفر قبل أي معاينة أو حجز.',
  "Er zijn negen woningen beschikbaar: twee tuinappartementen, vier penthouses en drie halfvrijstaande villa's. Bij elke woning horen twee parkeerplaatsen en een berging, apart geprijsd. Nueva Living bevestigt prijs en beschikbaarheid opnieuw vóór elke bezichtiging of reservering.",
  "Dostępnych jest dziewięć nieruchomości: dwa mieszkania z ogrodem, cztery penthouse'y i trzy domy bliźniacze. Do każdej przypisane są dwa miejsca postojowe i komórka lokatorska, wyceniane osobno. Nueva Living ponownie potwierdza cenę i dostępność przed każdą wizytą lub rezerwacją.",
  'Ni boliger er tilgjengelige: to hageleiligheter, fire toppleiligheter og tre tomannsvillaer. Til hver hører to parkeringsplasser og en bod, priset separat. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning eller reservasjon.',
  'Nio bostäder är lediga: två trädgårdslägenheter, fyra takvåningar och tre parhus. Till varje bostad hör två parkeringsplatser och ett förråd, prissatta separat. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning eller bokning.')
a(57, 'Availability and prices as listed',
  'Disponibilidad y precios según el portal para agentes del promotor a 13 de noviembre de 2026, que se reconfirman antes de la reserva; el portal indica que su lista es solo informativa. Los precios son de la vivienda sola y no incluyen el IVA ni los gastos de compra. El portal asigna a cada vivienda dos plazas de garaje y un trastero por {E34000} más, con lo que los totales van de {E1334100} a {E2250000}. Las superficies construidas incluyen la parte proporcional de zonas comunes de cada vivienda, tal como las dan el portal y los planos, y las cifras de terraza cuentan el solárium y la piscina privada. El número de dormitorios y baños sigue los planos de vivienda del promotor: el portal cuenta el aseo como baño en unas viviendas y no en otras, y atribuye a las villas cinco baños donde los planos muestran tres y un aseo. El folleto redondea las villas a 265 {U} con 235 {U} de terraza; el portal y los planos dan {N264.44} y {N220.63} {U}. Nueva Living reconfirma precio, estado y condiciones antes de cualquier reserva.',
  "Disponibilité et prix tels qu'indiqués sur le portail agents du promoteur au 13 novembre 2026, reconfirmés avant réservation ; le portail précise que sa liste est purement informative. Les prix s'entendent pour le logement seul, hors TVA et hors frais d'acquisition. Le portail associe à chaque logement deux places de parking et un débarras pour {E34000} de plus, ce qui porte les totaux de {E1334100} à {E2250000}. Les surfaces construites incluent la quote-part des parties communes de chaque logement, telles que les donnent le portail et les plans, et les surfaces de terrasse comprennent le solarium et la piscine privée. Le nombre de chambres et de salles de bain suit les plans de logement du promoteur : le portail compte le WC invités comme salle de bain pour certains logements et pas pour d'autres, et attribue aux villas cinq salles de bain là où les plans en montrent trois et un WC invités. La brochure arrondit les villas à 265 {U} avec 235 {U} de terrasse ; le portail et les plans donnent {N264.44} et {N220.63} {U}. Nueva Living reconfirme le prix, le statut et les conditions avant toute réservation.",
  'Verfügbarkeit und Preise laut Maklerportal des Bauträgers am 13. November 2026, vor der Reservierung erneut bestätigt; das Portal bezeichnet seine Liste als rein informativ. Die Preise gelten für die Einheit allein, zuzüglich MwSt. und Erwerbsnebenkosten. Das Portal ordnet jeder Einheit zwei Stellplätze und einen Abstellraum für {E34000} mehr zu, womit die Gesamtpreise bei {E1334100} bis {E2250000} liegen. Die bebauten Flächen enthalten den Anteil jeder Einheit an den Gemeinschaftsflächen, so wie Portal und Pläne sie angeben, und die Terrassenflächen rechnen Solarium und eigenen Pool mit ein. Schlafzimmer und Badezimmer folgen den Grundrissen des Bauträgers: Das Portal zählt das Gäste-WC bei manchen Einheiten als Badezimmer und bei anderen nicht und gibt den Villen fünf Badezimmer, wo die Pläne drei und ein Gäste-WC zeigen. Die Broschüre rundet die Villen auf 265 {U} mit 235 {U} Terrasse; Portal und Pläne nennen {N264.44} und {N220.63} {U}. Nueva Living bestätigt Preis, Status und Konditionen erneut vor jeder Reservierung.',
  'Наличие и цены — по порталу для агентов застройщика на 13 ноября 2026 года, с повторной проверкой перед бронированием; портал помечает свой список как справочный. Цены указаны только за сам объект, без НДС и расходов на оформление. Портал относит к каждому объекту два парковочных места и кладовую за дополнительные {E34000}, так что итоговые суммы составляют от {E1334100} до {E2250000}. Площадь застройки включает долю общих зон каждого объекта, как её указывают и портал, и планы, а площадь террас включает солярий и собственный бассейн. Число спален и ванных комнат взято с поэтажных планов застройщика: портал в одних случаях считает гостевой санузел ванной комнатой, а в других нет, и даёт виллам пять ванных комнат там, где на планах три и гостевой санузел. Буклет округляет виллы до 265 {U} с 235 {U} террас; портал и планы дают {N264.44} и {N220.63} {U}. Nueva Living заново подтверждает цену, статус и условия перед любым бронированием.',
  'التوفر والأسعار كما وردت في بوابة الوكلاء لدى المطور في 13 نوفمبر 2026، ويُعاد تأكيدها قبل الحجز؛ وتصف البوابة قائمتها بأنها للعلم فقط. الأسعار للمسكن وحده ولا تشمل ضريبة القيمة المضافة ولا مصاريف التملك. وتُدرج البوابة مع كل مسكن موقفي سيارات ومخزنًا مقابل {E34000} إضافية، فيصبح الإجمالي من {E1334100} إلى {E2250000}. تشمل المساحات المبنية حصة كل مسكن من المرافق المشتركة، كما تذكرها البوابة والمخططات، وتشمل أرقام التراسات السولاريوم والمسبح الخاص. يتبع عدد غرف النوم والحمامات مخططات الوحدات لدى المطور: فالبوابة تحتسب حمام الضيوف حمامًا في بعض المساكن دون غيرها، وتنسب إلى الفلل خمسة حمامات حيث تُظهر المخططات ثلاثة وحمامًا للضيوف. ويقرّب الكتيب مساحة الفلل إلى 265 {U} مع 235 {U} من التراسات، بينما تذكر البوابة والمخططات {N264.44} و{N220.63} {U}. تعيد Nueva Living تأكيد السعر والحالة والشروط قبل أي حجز.',
  "Beschikbaarheid en prijzen zoals vermeld op het agentenportaal van de ontwikkelaar op 13 november 2026, opnieuw bevestigd vóór reservering; het portaal noemt zijn lijst uitsluitend informatief. De prijzen gelden voor de woning alleen, exclusief btw en aankoopkosten. Het portaal koppelt aan elke woning twee parkeerplaatsen en een berging voor {E34000} extra, waarmee de totalen op {E1334100} tot {E2250000} komen. De bebouwde oppervlaktes omvatten het aandeel van elke woning in de gemeenschappelijke ruimtes, zoals portaal en plattegronden ze geven, en de terrasoppervlaktes tellen het solarium en het privézwembad mee. Het aantal slaap- en badkamers volgt de woningplattegronden van de ontwikkelaar: het portaal telt het gastentoilet bij sommige woningen als badkamer en bij andere niet, en geeft de villa's vijf badkamers waar de plattegronden er drie en een gastentoilet tonen. De brochure rondt de villa's af op 265 {U} met 235 {U} terras; portaal en plattegronden geven {N264.44} en {N220.63} {U}. Nueva Living bevestigt prijs, status en voorwaarden opnieuw vóór elke reservering.",
  'Dostępność i ceny według portalu dla agentów dewelopera z 13 listopada 2026 roku, ponownie potwierdzane przed rezerwacją; portal zaznacza, że jego lista ma charakter wyłącznie informacyjny. Ceny dotyczą samej nieruchomości i nie zawierają podatku VAT ani kosztów nabycia. Portal przypisuje do każdej nieruchomości dwa miejsca postojowe i komórkę lokatorską za dodatkowe {E34000}, co daje łącznie od {E1334100} do {E2250000}. Powierzchnie zabudowy obejmują udział każdej nieruchomości w częściach wspólnych, tak jak podają je portal i rzuty, a powierzchnie tarasów obejmują solarium i prywatny basen. Liczba sypialni i łazienek odpowiada rzutom dewelopera: portal w jednych przypadkach liczy toaletę dla gości jako łazienkę, a w innych nie, i przypisuje willom pięć łazienek tam, gdzie rzuty pokazują trzy i toaletę dla gości. Broszura zaokrągla wille do 265 {U} z 235 {U} tarasów; portal i rzuty podają {N264.44} i {N220.63} {U}. Nueva Living ponownie potwierdza cenę, status i warunki przed każdą rezerwacją.',
  'Tilgjengelighet og priser slik de står i utbyggerens meglerportal per 13. november 2026, bekreftet på nytt før reservasjon; portalen merker listen som kun veiledende. Prisene gjelder boligen alene og er eksklusive mva og kjøpsomkostninger. Portalen knytter to parkeringsplasser og en bod til hver bolig for {E34000} ekstra, slik at totalbeløpene blir {E1334100} til {E2250000}. Det bebygde arealet omfatter boligens andel av fellesarealene, slik både portalen og tegningene oppgir det, og terrassearealene regner med solterrassen og det private bassenget. Antall soverom og bad følger utbyggerens plantegninger: portalen regner gjestetoalettet som bad for noen boliger og ikke for andre, og gir villaene fem bad der tegningene viser tre og et gjestetoalett. Brosjyren runder villaene av til 265 {U} med 235 {U} terrasse; portalen og tegningene oppgir {N264.44} og {N220.63} {U}. Nueva Living bekrefter pris, status og vilkår på nytt før enhver reservasjon.',
  'Tillgänglighet och priser enligt exploatörens mäklarportal den 13 november 2026, bekräftade på nytt före bokning; portalen anger att listan endast är informativ. Priserna gäller bostaden ensam och är exklusive IVA (spansk moms) och köpkostnader. Portalen knyter två parkeringsplatser och ett förråd till varje bostad för {E34000} extra, vilket ger totalbelopp på {E1334100} till {E2250000}. Byggytorna inkluderar bostadens andel av de gemensamma ytorna, så som både portalen och ritningarna anger dem, och terrassytorna räknar in solterrassen och den egna poolen. Antalet sovrum och badrum följer exploatörens planritningar: portalen räknar gästtoaletten som badrum för vissa bostäder men inte för andra, och ger villorna fem badrum där ritningarna visar tre och en gästtoalett. Broschyren avrundar villorna till 265 {U} med 235 {U} terrass; portalen och ritningarna anger {N264.44} och {N220.63} {U}. Nueva Living bekräftar pris, status och villkor på nytt före varje bokning.')
a(80, "The developer's portal lists construction",
  'El portal del promotor indica que la obra ha comenzado, y ninguno de sus documentos da fecha de entrega ni calendario de pagos. Nueva Living pide ambos por escrito, junto con la licencia de obra, antes de que se mueva dinero alguno, y no dará una fecha que no podamos enseñarle.',
  "Le portail du promoteur indique que le chantier a commencé, et aucun de ses documents ne donne de date de livraison ni d'échéancier. Nueva Living demande les deux par écrit, avec le permis de construire, avant tout versement, et n'annoncera pas une date que nous ne pouvons pas vous montrer.",
  'Laut Portal des Bauträgers hat der Bau begonnen, doch keines seiner Dokumente nennt einen Fertigstellungstermin oder einen Zahlungsplan. Nueva Living fordert beides schriftlich an, zusammen mit der Baugenehmigung, bevor Geld fließt, und nennt Ihnen keinen Termin, den wir Ihnen nicht zeigen können.',
  'На портале застройщика указано, что строительство началось, но ни в одном из его документов нет ни срока сдачи, ни графика платежей. Nueva Living запрашивает и то и другое письменно, вместе с разрешением на строительство, до любого платежа, и не называет срок, который мы не можем вам показать.',
  'تشير بوابة المطور إلى أن البناء قد بدأ، ولا تذكر أي من وثائقه تاريخ تسليم أو جدول دفعات. تطلب Nueva Living الاثنين كتابيًا، مع رخصة البناء، قبل دفع أي مبلغ، ولن نذكر لكم تاريخًا لا نستطيع أن نُريكم إياه.',
  'Volgens het portaal van de ontwikkelaar is de bouw begonnen, en geen van zijn documenten noemt een opleverdatum of een betalingsschema. Nueva Living vraagt beide schriftelijk op, samen met de bouwvergunning, voordat er geld overgaat, en noemt geen datum die wij u niet kunnen laten zien.',
  'Portal dewelopera podaje, że budowa się rozpoczęła, ale żaden z jego dokumentów nie zawiera terminu oddania ani harmonogramu płatności. Nueva Living występuje o jedno i drugie na piśmie, razem z pozwoleniem na budowę, zanim wpłacone zostaną jakiekolwiek pieniądze, i nie poda Państwu terminu, którego nie możemy pokazać.',
  'Utbyggerens portal oppgir at byggingen har startet, og ingen av dokumentene oppgir en overtakelsesdato eller en betalingsplan. Nueva Living ber om begge deler skriftlig, sammen med byggetillatelsen, før det betales noe, og vi oppgir ingen dato vi ikke kan dokumentere.',
  'Exploatörens portal anger att bygget har startat, och inget av dokumenten anger ett tillträdesdatum eller en betalningsplan. Nueva Living begär båda skriftligt, tillsammans med bygglovet, innan några pengar betalas, och vi anger inget datum som vi inte kan visa er.')

# ---------------------------------------------------------------- why, investment, trust
a(81, 'Nine homes in one phase',
  'Nueve viviendas en una fase de un conjunto cerrado más amplio: apartamentos con jardín, áticos con solárium en la cubierta y villas pareadas.',
  "Neuf logements dans une phase d'un ensemble fermé plus vaste : appartements avec jardin, penthouses avec solarium sur le toit et villas jumelées.",
  'Neun Einheiten in einem Bauabschnitt einer größeren geschlossenen Wohnanlage: Gartenwohnungen, Penthäuser mit Dachsolarium und Doppelhaushälften.',
  'Девять объектов в одной из очередей большого закрытого комплекса: квартиры с садом, пентхаусы с солярием на крыше и парные дома.',
  'تسعة مساكن في مرحلة من مجمع مسوّر أكبر: شقق بحديقة، وبنتهاوس مع سولاريوم على السطح، وفلل شبه منفصلة.',
  "Negen woningen in een fase van een groter omheind complex: tuinappartementen, penthouses met een solarium op het dak en halfvrijstaande villa's.",
  "Dziewięć nieruchomości w jednym z etapów większego zamkniętego osiedla: mieszkania z ogrodem, penthouse'y z solarium na dachu i domy bliźniacze.",
  'Ni boliger i ett byggetrinn av et større inngjerdet anlegg: hageleiligheter, toppleiligheter med solterrasse på taket og tomannsvillaer.',
  'Nio bostäder i en etapp av en större inhägnad anläggning: trädgårdslägenheter, takvåningar med solterrass på taket och parhus.')
a(82, 'Buyers who want a pool of their own',
  'Compradores que quieren piscina propia y un campo de golf al lado, con las instalaciones de un resort compartidas en todo el conjunto.',
  "Les acquéreurs qui veulent leur propre piscine et un golf à côté, avec les équipements d'un resort partagés dans tout l'ensemble.",
  'Käufer, die einen eigenen Pool und einen Golfplatz nebenan möchten, mit den Einrichtungen eines Resorts für die gesamte Anlage.',
  'Покупателям, которым нужен собственный бассейн и гольф-поле по соседству, а также инфраструктура курорта, общая для всего комплекса.',
  'المشترون الذين يريدون مسبحًا خاصًا بهم وملعب غولف بجوارهم، مع مرافق منتجع مشتركة على مستوى المجمع.',
  'Kopers die een eigen zwembad en een golfbaan naast de deur willen, met de voorzieningen van een resort die het hele complex deelt.',
  'Dla kupujących, którzy chcą mieć własny basen i pole golfowe obok, a do tego infrastrukturę resortu wspólną dla całego osiedla.',
  'Kjøpere som vil ha sitt eget basseng og en golfbane rett ved, med resortfasiliteter som deles i hele anlegget.',
  'Köpare som vill ha en egen pool och en golfbana alldeles intill, med en resorts faciliteter som delas i hela anläggningen.')
a(83, 'Every available home adds',
  'Cada vivienda disponible suma a sus terrazas un espacio exterior privado: jardín y piscina en planta baja, solárium en la cubierta.',
  'Chaque logement disponible ajoute à ses terrasses un espace extérieur privé : jardin et piscine au rez-de-chaussée, solarium sur le toit.',
  'Jede verfügbare Einheit ergänzt ihre Terrassen um privaten Außenraum: Garten und Pool im Erdgeschoss, ein Solarium auf dem Dach.',
  'У каждого доступного объекта помимо террас есть своё открытое пространство: сад и бассейн на первом этаже, солярий на крыше.',
  'يضيف كل مسكن متاح إلى تراساته مساحة خارجية خاصة: حديقة ومسبحًا في الطابق الأرضي، وسولاريوم على السطح.',
  'Elke beschikbare woning heeft naast de terrassen eigen buitenruimte: een tuin en zwembad op de begane grond, een solarium op het dak.',
  'Każda dostępna nieruchomość ma oprócz tarasów własną przestrzeń na zewnątrz: ogród i basen na parterze, solarium na dachu.',
  'Hver tilgjengelige bolig har privat uteareal i tillegg til terrassene: hage og basseng i første etasje, solterrasse på taket.',
  'Varje ledig bostad har egen utomhusyta utöver terrasserna: trädgård och pool på bottenvåningen, solterrass på taket.')
a(84, 'The scheme lies on the east side',
  'El conjunto está en el lado este de Marbella; según las cifras del folleto, el centro queda a entre 5 y 9 minutos y el aeropuerto de Málaga a unos 35.',
  "L'ensemble se trouve à l'est de Marbella ; selon les chiffres de la brochure, le centre-ville est à 5 à 9 minutes et l'aéroport de Malaga à environ 35.",
  'Die Anlage liegt im Osten von Marbella; nach den Angaben der Broschüre ist das Zentrum 5 bis 9 Minuten entfernt und der Flughafen Málaga etwa 35.',
  'Комплекс находится в восточной части Марбельи; по данным буклета, до центра города 5–9 минут, до аэропорта Малаги — около 35.',
  'يقع المجمع في الجانب الشرقي من ماربيا؛ ووفق أرقام الكتيب يبعد وسط المدينة من 5 إلى 9 دقائق ومطار مالقة نحو 35 دقيقة.',
  'Het complex ligt aan de oostkant van Marbella; volgens de brochure is het centrum 5 tot 9 minuten weg en de luchthaven van Malaga ongeveer 35.',
  'Osiedle leży we wschodniej części Marbelli; według broszury do centrum jest od 5 do 9 minut, a na lotnisko w Maladze około 35.',
  'Anlegget ligger på østsiden av Marbella; ifølge brosjyren er det 5 til 9 minutter til sentrum og rundt 35 til Málaga lufthavn.',
  'Anläggningen ligger på Marbellas östra sida; enligt broschyren är det 5 till 9 minuter till centrum och omkring 35 till Málagas flygplats.')
a(85, 'An <em>east Marbella',
  'Una dirección en el <em>este de Marbella</em>', "Une adresse dans <em>l'est de Marbella</em>", 'Eine Adresse im <em>Osten von Marbella</em>',
  'Адрес на <em>востоке Марбельи</em>', 'عنوان في <em>شرق ماربيا</em>', 'Een adres in <em>oost-Marbella</em>',
  'Adres we <em>wschodniej Marbelli</em>', 'En adresse <em>øst i Marbella</em>', 'En adress i <em>östra Marbella</em>')
a(86, 'Construction has started and nine homes',
  'La obra ha comenzado y quedan nueve viviendas en la lista del portal, así que la elección entre jardín, ático y villa ya es limitada.',
  'Le chantier a commencé et il reste neuf logements sur la liste du portail : le choix entre jardin, penthouse et villa est déjà restreint.',
  'Der Bau hat begonnen und auf der Portalliste stehen noch neun Einheiten, die Wahl zwischen Garten, Penthouse und Villa ist also bereits begrenzt.',
  'Строительство началось, и в списке портала осталось девять объектов, поэтому выбор между садом, пентхаусом и виллой уже невелик.',
  'بدأ البناء ولم يبقَ في قائمة البوابة سوى تسعة مساكن، لذا فالاختيار بين الحديقة والبنتهاوس والفيلا محدود بالفعل.',
  'De bouw is begonnen en er staan nog negen woningen op de portaallijst, dus de keuze tussen tuin, penthouse en villa is al beperkt.',
  "Budowa się rozpoczęła, a na liście portalu zostało dziewięć nieruchomości, więc wybór między ogrodem, penthouse'em a willą jest już ograniczony.",
  'Byggingen har startet, og det står ni boliger igjen på portallisten, så valget mellom hage, toppleilighet og villa er allerede begrenset.',
  'Bygget har startat och nio bostäder återstår på portallistan, så valet mellan trädgård, takvåning och villa är redan begränsat.')
a(87, 'The brochure describes the area',
  'El folleto describe la zona como un barrio residencial privado en torno al campo de golf vecino, cerca del mar.',
  'La brochure présente le secteur comme un quartier résidentiel privé autour du golf voisin, près de la mer.',
  'Die Broschüre beschreibt die Gegend als privates Wohnviertel rund um den benachbarten Golfplatz, nahe am Meer.',
  'Буклет описывает этот район как закрытый жилой квартал вокруг соседнего гольф-поля недалеко от моря.',
  'يصف الكتيب المنطقة بأنها حي سكني خاص حول ملعب الغولف المجاور، قريب من البحر.',
  'De brochure beschrijft de omgeving als een privé-woonwijk rond de naburige golfbaan, dicht bij zee.',
  'Broszura opisuje okolicę jako prywatną dzielnicę mieszkaniową wokół sąsiedniego pola golfowego, blisko morza.',
  'Brosjyren beskriver området som et privat boligområde rundt den nærliggende golfbanen, nær havet.',
  'Broschyren beskriver området som ett privat bostadsområde runt den närliggande golfbanan, nära havet.')
a(88, 'That the home, its terraces',
  'Que la vivienda, sus terrazas, su jardín o solárium, su piscina y las dos plazas de garaje y el trastero están inscritos tal como se describen.',
  'Que le logement, ses terrasses, son jardin ou son solarium, sa piscine ainsi que les deux places de parking et le débarras sont inscrits tels que décrits.',
  'Dass die Einheit, ihre Terrassen, ihr Garten oder Solarium, ihr Pool sowie die zwei Stellplätze und der Abstellraum wie beschrieben eingetragen sind.',
  'Что объект, его террасы, сад или солярий, бассейн, а также два парковочных места и кладовая зарегистрированы так, как описано.',
  'أن المسكن وتراساته وحديقته أو السولاريوم ومسبحه، وموقفي السيارات والمخزن، مسجلة كما هو موصوف.',
  'Dat de woning, de terrassen, de tuin of het solarium, het zwembad en de twee parkeerplaatsen en de berging zijn ingeschreven zoals beschreven.',
  'Że nieruchomość, jej tarasy, ogród lub solarium, basen oraz dwa miejsca postojowe i komórka lokatorska są wpisane do rejestru zgodnie z opisem.',
  'At boligen, terrassene, hagen eller solterrassen, bassenget og de to parkeringsplassene og boden er tinglyst slik de er beskrevet.',
  'Att bostaden, terrasserna, trädgården eller solterrassen, poolen samt de två parkeringsplatserna och förrådet är registrerade som beskrivet.')
a(89, 'The developer has not published one for this phase',
  'El promotor no la ha publicado para esta fase; la pedimos por escrito y la incluimos en el contrato.',
  "Le promoteur n'en a pas publié pour cette phase ; nous la demandons par écrit et l'inscrivons au contrat.",
  'Der Bauträger hat für diesen Bauabschnitt keinen veröffentlicht; wir fordern ihn schriftlich an und nehmen ihn in den Vertrag auf.',
  'Застройщик не опубликовал его для этой очереди; мы запрашиваем его письменно и вносим в договор.',
  'لم ينشر المطور تاريخًا لهذه المرحلة؛ نطلبه كتابيًا وندرجه في العقد.',
  'De ontwikkelaar heeft er voor deze fase geen gepubliceerd; wij vragen die schriftelijk op en nemen die op in het contract.',
  'Deweloper nie opublikował go dla tego etapu; występujemy o niego na piśmie i wpisujemy go do umowy.',
  'Utbyggeren har ikke publisert noen for dette byggetrinnet; vi ber om den skriftlig og tar den inn i kontrakten.',
  'Exploatören har inte publicerat något för den här etappen; vi begär det skriftligt och för in det i avtalet.')

# ---------------------------------------------------------------- architecture
a(90, 'White blocks, <em>',
  'Bloques blancos, <em>terrazas amplias</em>', 'Volumes blancs, <em>terrasses profondes</em>', 'Weiße Baukörper, <em>tiefe Terrassen</em>',
  'Белые корпуса, <em>глубокие террасы</em>', 'مبانٍ بيضاء، <em>وتراسات عميقة</em>', 'Witte blokken, <em>diepe terrassen</em>',
  'Białe bryły, <em>głębokie tarasy</em>', 'Hvite bygg, <em>dype terrasser</em>', 'Vita huskroppar, <em>djupa terrasser</em>')
a(91, 'The brochure describes a contemporary',
  'El folleto describe una relectura contemporánea de la arquitectura mediterránea: edificios blancos con grandes pérgolas para el sol y la sombra, patios que aportan luz y ventilación cruzada, y bloques encajados en la pendiente para que cada vivienda mire al mar o al campo de golf.',
  "La brochure décrit une relecture contemporaine de l'architecture méditerranéenne : des bâtiments blancs avec de grandes pergolas pour le soleil et l'ombre, des patios qui apportent lumière et ventilation traversante, et des volumes intégrés à la pente pour que chaque logement regarde vers la mer ou le golf.",
  'Die Broschüre beschreibt eine zeitgenössische Interpretation mediterraner Architektur: weiße Gebäude mit großen Pergolen für Sonne und Schatten, Innenhöfe für Licht und Querlüftung und Baukörper, die so in den Hang gesetzt sind, dass jede Einheit zum Meer oder zum Golfplatz blickt.',
  'Буклет описывает современное прочтение средиземноморской архитектуры: белые здания с большими перголами для солнца и тени, внутренние дворики для света и сквозного проветривания и корпуса, вписанные в склон так, чтобы каждый дом смотрел на море или на гольф-поле.',
  'يصف الكتيب قراءة معاصرة للعمارة المتوسطية: مبانٍ بيضاء بعرائش كبيرة للشمس والظل، وأفنية تُدخل الضوء والتهوية المتقاطعة، ومبانٍ مدمجة في المنحدر بحيث يطل كل مسكن على البحر أو ملعب الغولف.',
  "De brochure beschrijft een eigentijdse lezing van mediterrane architectuur: witte gebouwen met grote pergola's voor zon en schaduw, patio's die licht en dwarsventilatie binnenbrengen, en blokken die zo in de helling liggen dat elke woning uitkijkt op zee of op de golfbaan.",
  'Broszura opisuje współczesne odczytanie architektury śródziemnomorskiej: białe budynki z dużymi pergolami dającymi słońce i cień, patia doprowadzające światło i zapewniające wentylację skrośną oraz bryły wpisane w zbocze tak, by każda nieruchomość wychodziła na morze lub pole golfowe.',
  'Brosjyren beskriver en moderne tolkning av middelhavsarkitektur: hvite bygg med store pergolaer for sol og skygge, gårdsrom som slipper inn lys og gir krysslufting, og bygg lagt inn i skråningen slik at hver bolig ser mot havet eller golfbanen.',
  'Broschyren beskriver en modern tolkning av medelhavsarkitektur: vita byggnader med stora pergolor för sol och skugga, gårdar som släpper in ljus och ger tvärdrag, och huskroppar inpassade i sluttningen så att varje bostad blickar mot havet eller golfbanan.')
a(92, 'Two-storey blocks of garden apartments',
  'Bloques de dos plantas con apartamentos con jardín y áticos, y villas pareadas de tres niveles, todos orientados al suroeste.',
  'Des immeubles de deux niveaux avec appartements avec jardin et penthouses, et des villas jumelées sur trois niveaux, tous orientés au sud-ouest.',
  'Zweigeschossige Blöcke mit Gartenwohnungen und Penthäusern sowie Doppelhaushälften auf drei Ebenen, alle nach Südwesten ausgerichtet.',
  'Двухэтажные корпуса с квартирами с садом и пентхаусами и трёхуровневые парные дома, все с ориентацией на юго-запад.',
  'مبانٍ من طابقين تضم شققًا بحديقة وبنتهاوس، وفلل شبه منفصلة من ثلاثة مستويات، وكلها موجهة نحو الجنوب الغربي.',
  "Blokken van twee verdiepingen met tuinappartementen en penthouses, en halfvrijstaande villa's op drie niveaus, alle op het zuidwesten.",
  "Dwukondygnacyjne budynki z mieszkaniami z ogrodem i penthouse'ami oraz trzypoziomowe domy bliźniacze, wszystkie z ekspozycją południowo-zachodnią.",
  'Bygg i to etasjer med hageleiligheter og toppleiligheter, og tomannsvillaer i tre plan, alle vendt mot sørvest.',
  'Hus i två plan med trädgårdslägenheter och takvåningar, samt parhus i tre plan, alla vända mot sydväst.')
a(93, 'From 134.11 to 220.63 sqm including',
  'De {N134.11} a {N220.63} {U} incluidos solárium y piscina, todas con toma de agua, enchufe y pavimento porcelánico antideslizante.',
  'De {N134.11} à {N220.63} {U} solarium et piscine compris, toutes avec point d\'eau, prise électrique et carrelage en grès cérame antidérapant.',
  '{N134.11} bis {N220.63} {U} einschließlich Solarium und Pool, jeweils mit Wasseranschluss, Steckdose und rutschfestem Feinsteinzeug.',
  'От {N134.11} до {N220.63} {U} с учётом солярия и бассейна, на каждой — точка водоснабжения, розетка и нескользкий керамогранит.',
  'من {N134.11} إلى {N220.63} {U} بما في ذلك السولاريوم والمسبح، وفي كل منها نقطة مياه ومقبس كهربائي وأرضية بورسلان مانعة للانزلاق.',
  'Van {N134.11} tot {N220.63} {U} inclusief solarium en zwembad, elk met een waterpunt, een stopcontact en antislip-keramische tegels.',
  'Od {N134.11} do {N220.63} {U} łącznie z solarium i basenem, każdy z punktem wody, gniazdkiem elektrycznym i antypoślizgową płytką gresową.',
  'Fra {N134.11} til {N220.63} {U} inkludert solterrasse og basseng, hver med vannpost, stikkontakt og sklisikre porselensfliser.',
  'Från {N134.11} till {N220.63} {U} inklusive solterrass och pool, var och en med vattenuttag, eluttag och halkfritt klinkergolv.')
a(94, 'A private pool of 11.80',
  'Una piscina privada de {N11.80} a {N15.55} {U} en el plano de cada vivienda disponible, en el jardín o en la cubierta.',
  'Une piscine privée de {N11.80} à {N15.55} {U} sur le plan de chaque logement disponible, dans le jardin ou sur le toit.',
  'Ein eigener Pool von {N11.80} bis {N15.55} {U} im Plan jeder verfügbaren Einheit, im Garten oder auf dem Dach.',
  'Собственный бассейн от {N11.80} до {N15.55} {U} на плане каждого доступного объекта — в саду или на крыше.',
  'مسبح خاص من {N11.80} إلى {N15.55} {U} في مخطط كل مسكن متاح، في الحديقة أو على السطح.',
  'Een privézwembad van {N11.80} tot {N15.55} {U} op de tekening van elke beschikbare woning, in de tuin of op het dak.',
  'Prywatny basen o powierzchni od {N11.80} do {N15.55} {U} na rzucie każdej dostępnej nieruchomości, w ogrodzie lub na dachu.',
  'Et privat basseng på {N11.80} til {N15.55} {U} på tegningen av hver tilgjengelige bolig, i hagen eller på taket.',
  'En egen pool på {N11.80} till {N15.55} {U} på ritningen till varje ledig bostad, i trädgården eller på taket.')
a(95, 'Large-format porcelain floors',
  'Suelos porcelánicos de gran formato, cocina amueblada con placa de inducción, horno, microondas, lavavajillas, frigorífico y lavadora-secadora, y encimeras de Silestone.',
  'Sols en grès cérame grand format, cuisine équipée avec plaque à induction, four, micro-ondes, lave-vaisselle, réfrigérateur et lave-linge séchant, et plans de travail en Silestone.',
  'Großformatige Feinsteinzeugböden, eine Einbauküche mit Induktionskochfeld, Backofen, Mikrowelle, Geschirrspüler, Kühlschrank und Waschtrockner sowie Arbeitsplatten aus Silestone.',
  'Крупноформатный керамогранит на полу, встроенная кухня с индукционной варочной панелью, духовкой, микроволновой печью, посудомоечной машиной, холодильником и стирально-сушильной машиной, столешницы Silestone.',
  'أرضيات بورسلان كبيرة الحجم، ومطبخ مجهز بموقد حثي وفرن وميكروويف وغسالة صحون وثلاجة وغسالة مجففة، وأسطح عمل من Silestone.',
  'Keramische vloeren in groot formaat, een ingerichte keuken met inductiekookplaat, oven, magnetron, vaatwasser, koelkast en was-droogcombinatie, en werkbladen van Silestone.',
  'Wielkoformatowe płytki gresowe na podłogach, zabudowana kuchnia z płytą indukcyjną, piekarnikiem, mikrofalówką, zmywarką, lodówką i pralko-suszarką oraz blaty Silestone.',
  'Storformat porselensfliser på gulvene, et innredet kjøkken med induksjonstopp, stekeovn, mikrobølgeovn, oppvaskmaskin, kjøleskap og vaske-tørkemaskin, og benkeplater i Silestone.',
  'Storformatigt klinker på golven, ett inrett kök med induktionshäll, ugn, mikrovågsugn, diskmaskin, kylskåp och kombinerad tvätt- och torkmaskin, samt bänkskivor i Silestone.')
a(96, 'Comfort',
  'Confort', 'Confort', 'Komfort', 'Комфорт', 'الراحة', 'Comfort', 'Komfort', 'Komfort', 'Komfort')
a(97, 'Underfloor heating and ducted',
  'Suelo radiante y aire acondicionado por conductos alimentados por aerotermia, control por zonas y domótica en la zona de día.',
  'Plancher chauffant et climatisation gainable alimentés par aérothermie, régulation par zones et domotique dans les pièces de jour.',
  'Fußbodenheizung und Kanal-Klimaanlage über eine Luftwärmepumpe, Zonensteuerung und Hausautomation im Wohnbereich.',
  'Тёплые полы и канальное кондиционирование от аэротермической системы, зональное управление и система «умный дом» в дневной зоне.',
  'تدفئة أرضية وتكييف بالقنوات من نظام حراري هوائي، مع تحكم حسب المناطق وأتمتة منزلية في منطقة المعيشة.',
  'Vloerverwarming en kanaalairconditioning via een luchtwarmtepomp, zoneregeling en domotica in het woongedeelte.',
  'Ogrzewanie podłogowe i klimatyzacja kanałowa zasilane aerotermią, sterowanie strefowe i automatyka domowa w strefie dziennej.',
  'Gulvvarme og kanalbasert klimaanlegg fra et aerotermisk system, sonestyring og hjemmeautomasjon i oppholdsdelen.',
  'Golvvärme och kanaliserad luftkonditionering från ett aerotermiskt system, zonstyrning och hemautomation i vardagsdelen.')
a(98, 'Solar panels in support',
  'Placas solares de apoyo, doble acristalamiento con rotura de puente térmico y persianas motorizadas en los dormitorios; los planos llevan la calificación A.',
  'Panneaux solaires en appoint, double vitrage à rupture de pont thermique et volets motorisés dans les chambres ; les plans affichent la classe A.',
  'Solarmodule zur Unterstützung, Doppelverglasung mit thermischer Trennung und motorisierte Rollläden in den Schlafzimmern; die Pläne tragen die Energieklasse A.',
  'Солнечные панели в качестве поддержки, двойное остекление с терморазрывом и моторизованные жалюзи в спальнях; на планах указан энергокласс A.',
  'ألواح شمسية داعمة، وزجاج مزدوج بفاصل حراري، وستائر آلية في غرف النوم؛ وتحمل المخططات تصنيف الطاقة A.',
  'Zonnepanelen ter ondersteuning, dubbele beglazing met thermische onderbreking en gemotoriseerde rolluiken in de slaapkamers; de plattegronden vermelden energielabel A.',
  'Panele słoneczne jako wsparcie, podwójne szyby w ramach z przekładką termiczną i zmotoryzowane rolety w sypialniach; rzuty podają klasę energetyczną A.',
  'Solcellepaneler som tilskudd, doble vinduer med kuldebrobryter og motoriserte persienner på soverommene; tegningene oppgir energiklasse A.',
  'Solpaneler som stöd, dubbelglas med bruten köldbrygga och motoriserade persienner i sovrummen; ritningarna anger energiklass A.')

# ---------------------------------------------------------------- lifestyle, viewing, location
a(99, 'Golf and sea, <em>',
  'Golf y mar, <em>este de Marbella</em>', 'Golf et mer, <em>est de Marbella</em>', 'Golf und Meer, <em>Ost-Marbella</em>',
  'Гольф и море, <em>восток Марбельи</em>', 'الغولف والبحر، <em>شرق ماربيا</em>', 'Golf en zee, <em>oost-Marbella</em>',
  'Golf i morze, <em>wschodnia Marbella</em>', 'Golf og hav, <em>øst i Marbella</em>', 'Golf och hav, <em>östra Marbella</em>')
a(100, 'A private residential area',
  'Una zona residencial privada en torno al campo de golf vecino, en el lado este de Marbella, cerca del mar, con el centro a pocos minutos hacia el oeste.',
  "Un quartier résidentiel privé autour du golf voisin, à l'est de Marbella, près de la mer, avec le centre-ville à quelques minutes à l'ouest.",
  'Ein privates Wohngebiet rund um den benachbarten Golfplatz im Osten von Marbella, nahe am Meer, mit dem Zentrum wenige Minuten westlich.',
  'Закрытый жилой район вокруг соседнего гольф-поля в восточной части Марбельи, недалеко от моря; центр города — в нескольких минутах к западу.',
  'منطقة سكنية خاصة حول ملعب الغولف المجاور في الجانب الشرقي من ماربيا، قريبة من البحر، ووسط المدينة على بعد دقائق قليلة إلى الغرب.',
  'Een privé-woonwijk rond de naburige golfbaan aan de oostkant van Marbella, dicht bij zee, met het centrum enkele minuten naar het westen.',
  'Prywatna dzielnica mieszkaniowa wokół sąsiedniego pola golfowego we wschodniej części Marbelli, blisko morza, z centrum kilka minut na zachód.',
  'Et privat boligområde rundt den nærliggende golfbanen på østsiden av Marbella, nær havet, med sentrum noen minutter mot vest.',
  'Ett privat bostadsområde runt den närliggande golfbanan på Marbellas östra sida, nära havet, med centrum några minuter västerut.')
a(101, 'The neighbouring golf course runs',
  'El campo de golf vecino discurre junto al conjunto, y el mapa del folleto sitúa cerca Río Real, Los Monteros y Marbella Golf.',
  "Le golf voisin longe l'ensemble, et la carte de la brochure situe Río Real, Los Monteros et Marbella Golf à proximité.",
  'Der benachbarte Golfplatz verläuft entlang der Anlage, und die Karte der Broschüre zeigt Río Real, Los Monteros und Marbella Golf in der Nähe.',
  'Соседнее гольф-поле проходит вдоль комплекса, а на карте в буклете поблизости отмечены Рио-Реаль, Лос-Монтерос и Marbella Golf.',
  'يمتد ملعب الغولف المجاور بمحاذاة المجمع، وتُظهر خريطة الكتيب ملاعب ريو ريال ولوس مونتيروس وماربيا غولف على مقربة.',
  'De naburige golfbaan loopt langs het complex, en de kaart in de brochure toont Río Real, Los Monteros en Marbella Golf in de buurt.',
  'Sąsiednie pole golfowe biegnie wzdłuż osiedla, a mapa w broszurze pokazuje w pobliżu Río Real, Los Monteros i Marbella Golf.',
  'Den nærliggende golfbanen ligger langs anlegget, og kartet i brosjyren viser Río Real, Los Monteros og Marbella Golf i nærheten.',
  'Den närliggande golfbanan löper längs anläggningen, och kartan i broschyren visar Río Real, Los Monteros och Marbella Golf i närheten.')
a(102, 'The centre of Marbella is 5 to 9',
  'El centro de Marbella queda a entre 5 y 9 minutos según las dos cifras del folleto, que sitúa las playas del este de Marbella a poca distancia a pie.',
  "Le centre de Marbella est à 5 à 9 minutes selon les deux chiffres de la brochure, qui place les plages de l'est de Marbella à distance de marche.",
  'Das Zentrum von Marbella ist nach den zwei Angaben der Broschüre 5 bis 9 Minuten entfernt, und sie verortet die Strände im Osten von Marbella in Gehweite.',
  'До центра Марбельи 5–9 минут по двум цифрам из буклета, а пляжи восточной Марбельи, по его словам, в пешей доступности.',
  'يبعد وسط ماربيا من 5 إلى 9 دقائق وفق الرقمين الواردين في الكتيب، الذي يضع شواطئ شرق ماربيا على مسافة قريبة سيرًا على الأقدام.',
  'Het centrum van Marbella ligt volgens de twee cijfers in de brochure op 5 tot 9 minuten, en de brochure plaatst de stranden van oost-Marbella op loopafstand.',
  'Do centrum Marbelli jest od 5 do 9 minut według dwóch liczb z broszury, która umieszcza plaże wschodniej Marbelli w zasięgu spaceru.',
  'Marbella sentrum ligger 5 til 9 minutter unna etter brosjyrens to tall, og brosjyren plasserer strendene øst i Marbella i gangavstand.',
  'Marbellas centrum ligger 5 till 9 minuter bort enligt broschyrens två uppgifter, och broschyren placerar stränderna i östra Marbella på gångavstånd.')
a(103, 'Puerto Banús is about 17',
  'Puerto Banús queda a unos 17 minutos, el aeropuerto de Málaga a unos 35 y la ciudad de Málaga a unos 47, según las cifras del folleto.',
  "Puerto Banús est à environ 17 minutes, l'aéroport de Malaga à environ 35 et la ville de Malaga à environ 47, selon les chiffres de la brochure.",
  'Puerto Banús ist etwa 17 Minuten entfernt, der Flughafen Málaga etwa 35 und die Stadt Málaga etwa 47, nach den Angaben der Broschüre.',
  'До Пуэрто-Бануса около 17 минут, до аэропорта Малаги около 35, до самой Малаги около 47 — по данным буклета.',
  'يبعد بويرتو بانوس نحو 17 دقيقة، ومطار مالقة نحو 35 دقيقة، ومدينة مالقة نحو 47 دقيقة، وفق أرقام الكتيب.',
  'Puerto Banús ligt op ongeveer 17 minuten, de luchthaven van Malaga op ongeveer 35 en de stad Malaga op ongeveer 47, volgens de brochure.',
  'Do Puerto Banús jest około 17 minut, na lotnisko w Maladze około 35, a do samej Malagi około 47, według broszury.',
  'Puerto Banús ligger rundt 17 minutter unna, Málaga lufthavn rundt 35 og selve Málaga rundt 47, ifølge brosjyren.',
  'Puerto Banús ligger omkring 17 minuter bort, Málagas flygplats omkring 35 och staden Málaga omkring 47, enligt broschyren.')
a(104, 'Construction has started, so a visit',
  'La obra ya ha comenzado, así que una visita muestra la parcela, la pendiente y las vistas que tendrá cada vivienda sobre el campo de golf y el mar.',
  'Le chantier a commencé : une visite montre la parcelle, la pente et la vue que chaque logement aura sur le golf et la mer.',
  'Der Bau hat begonnen; ein Besuch zeigt das Grundstück, den Hang und den Ausblick, den jede Einheit über den Golfplatz und das Meer haben wird.',
  'Строительство уже идёт, поэтому на месте видно участок, склон и вид, который будет у каждого объекта на гольф-поле и море.',
  'بدأ البناء، لذا تُظهر الزيارة قطعة الأرض والمنحدر والإطلالة التي سيحظى بها كل مسكن على ملعب الغولف والبحر.',
  'De bouw is begonnen, dus een bezoek laat het perceel, de helling en het uitzicht zien dat elke woning op de golfbaan en de zee krijgt.',
  'Budowa już trwa, więc wizyta pokazuje działkę, zbocze i widok, jaki każda nieruchomość będzie mieć na pole golfowe i morze.',
  'Byggingen har startet, så et besøk viser tomten, skråningen og utsikten hver bolig får over golfbanen og havet.',
  'Bygget har startat, så ett besök visar tomten, sluttningen och den utsikt varje bostad får över golfbanan och havet.')
a(105, 'See where the blocks and the villas',
  'Vea dónde se sitúan los bloques y las villas en la pendiente y qué hay entre ellos y el mar.',
  'Voyez où se placent les immeubles et les villas sur la pente et ce qui les sépare de la mer.',
  'Sehen Sie, wo die Blöcke und die Villen am Hang liegen und was zwischen ihnen und dem Meer liegt.',
  'Посмотрите, где на склоне стоят корпуса и виллы и что находится между ними и морем.',
  'شاهدوا موقع المباني والفلل على المنحدر وما يفصلها عن البحر.',
  "Bekijk waar de blokken en de villa's op de helling staan en wat er tussen hen en de zee ligt.",
  'Proszę zobaczyć, gdzie na zboczu stoją budynki i wille i co znajduje się między nimi a morzem.',
  'Se hvor byggene og villaene ligger i skråningen og hva som ligger mellom dem og havet.',
  'Se var husen och villorna ligger i sluttningen och vad som finns mellan dem och havet.')
a(106, 'Compare the view from a garden',
  'Compare las vistas desde un jardín, una terraza de primera planta y un solárium en la cubierta.',
  'Comparez la vue depuis un jardin, une terrasse au premier étage et un solarium sur le toit.',
  'Vergleichen Sie den Blick aus einem Garten, von einer Terrasse im ersten Obergeschoss und von einem Dachsolarium.',
  'Сравните вид из сада, с террасы второго этажа и с солярия на крыше.',
  'قارنوا الإطلالة من حديقة ومن تراس في الطابق الأول ومن سولاريوم على السطح.',
  'Vergelijk het uitzicht vanuit een tuin, vanaf een terras op de eerste verdieping en vanaf een solarium op het dak.',
  'Proszę porównać widok z ogrodu, z tarasu na pierwszym piętrze i z solarium na dachu.',
  'Sammenlign utsikten fra en hage, en terrasse i andre etasje og en solterrasse på taket.',
  'Jämför utsikten från en trädgård, en terrass på första våningen och en solterrass på taket.')
a(107, "See which of the scheme's shared",
  'Compruebe cuáles de las piscinas, el spa, el gimnasio y las salas de coworking compartidos del conjunto están abiertos, y a qué distancia quedan de esta fase.',
  "Vérifiez lesquels des piscines, du spa, de la salle de sport et des espaces de coworking partagés de l'ensemble sont ouverts, et à quelle distance ils se trouvent de cette phase.",
  'Prüfen Sie, welche der gemeinsamen Pools, das Spa, der Fitnessraum und die Coworking-Räume der Anlage bereits geöffnet sind und wie weit sie von diesem Bauabschnitt entfernt liegen.',
  'Узнайте, какие из общих бассейнов, спа, спортзала и коворкингов комплекса уже работают и как далеко они от этой очереди.',
  'تحققوا من أي من المسابح والسبا وصالة الرياضة وغرف العمل المشترك في المجمع مفتوحة، ومن بُعدها عن هذه المرحلة.',
  'Bekijk welke gedeelde zwembaden, spa, fitnessruimte en coworkingruimtes van het complex open zijn, en hoe ver ze van deze fase liggen.',
  'Proszę sprawdzić, które ze wspólnych basenów, spa, siłowni i sal coworkingowych osiedla są już otwarte i jak daleko są od tego etapu.',
  'Se hvilke av anleggets felles bassenger, spa, treningsrom og coworking-rom som er åpne, og hvor langt de ligger fra dette byggetrinnet.',
  'Se vilka av anläggningens gemensamma pooler, spa, gym och coworkingrum som är öppna, och hur långt de ligger från den här etappen.')
a(108, 'East <em>Marbella',
  'Este de <em>Marbella</em>', 'Est de <em>Marbella</em>', 'Östliches <em>Marbella</em>', 'Восточная <em>Марбелья</em>',
  'شرق <em>ماربيا</em>', 'Oost-<em>Marbella</em>', 'Wschodnia <em>Marbella</em>', 'Østre <em>Marbella</em>',
  'Östra <em>Marbella</em>')
a(109, 'One phase of a larger gated scheme on the east side',
  'Una fase de un conjunto cerrado más amplio en el lado este de Marbella, junto al campo de golf vecino y cerca del mar. El promotor solo da tiempos en coche, y la posición en el mapa es aproximada.',
  "Une phase d'un ensemble fermé plus vaste à l'est de Marbella, près du golf voisin et de la mer. Le promoteur ne donne que des temps de trajet en voiture, et la position sur la carte est approximative.",
  'Ein Bauabschnitt einer größeren geschlossenen Wohnanlage im Osten von Marbella, am benachbarten Golfplatz und nahe am Meer. Der Bauträger nennt nur Fahrzeiten, und die Position auf der Karte ist ungefähr.',
  'Одна из очередей большого закрытого комплекса в восточной части Марбельи, рядом с соседним гольф-полем и недалеко от моря. Застройщик указывает только время в пути на машине, а положение на карте приблизительное.',
  'مرحلة من مجمع مسوّر أكبر في الجانب الشرقي من ماربيا، بجوار ملعب الغولف المجاور وقريبًا من البحر. يذكر المطور أوقات القيادة فقط، والموقع على الخريطة تقريبي.',
  'Een fase van een groter omheind complex aan de oostkant van Marbella, naast de naburige golfbaan en dicht bij zee. De ontwikkelaar geeft alleen rijtijden, en de positie op de kaart is bij benadering.',
  'Jeden z etapów większego zamkniętego osiedla we wschodniej części Marbelli, przy sąsiednim polu golfowym i blisko morza. Deweloper podaje tylko czasy dojazdu samochodem, a położenie na mapie jest przybliżone.',
  'Ett byggetrinn i et større inngjerdet anlegg på østsiden av Marbella, ved den nærliggende golfbanen og nær havet. Utbyggeren oppgir bare kjøretider, og plasseringen på kartet er omtrentlig.',
  'En etapp i en större inhägnad anläggning på Marbellas östra sida, intill den närliggande golfbanan och nära havet. Exploatören anger bara körtider, och placeringen på kartan är ungefärlig.')
a(110, 'Approx. 5 to 9 minutes',
  'Aprox. 5 a 9 minutos', 'Env. 5 à 9 minutes', 'Ca. 5 bis 9 Minuten', 'Ок. 5–9 минут', 'حوالي 5 إلى 9 دقائق', 'Ca. 5 tot 9 minuten',
  'Ok. 5–9 minut', 'Ca. 5 til 9 minutter', 'Ca 5 till 9 minuter')
a(111, 'Approx. 17 minutes',
  'Aprox. 17 minutos', 'Env. 17 minutes', 'Ca. 17 Minuten', 'Ок. 17 минут', 'حوالي 17 دقيقة', 'Ca. 17 minuten', 'Ok. 17 minut',
  'Ca. 17 minutter', 'Ca 17 minuter')
a(112, 'Approx. 47 minutes',
  'Aprox. 47 minutos', 'Env. 47 minutes', 'Ca. 47 Minuten', 'Ок. 47 минут', 'حوالي 47 دقيقة', 'Ca. 47 minuten', 'Ok. 47 minut',
  'Ca. 47 minutter', 'Ca 47 minuter')

# ---------------------------------------------------------------- faq
a(113, 'From €1,300,100',
  'De {E1300100} a {E2216000}, sin IVA ni gastos de compra. Cada vivienda lleva dos plazas de garaje y un trastero por {E34000} más.',
  "De {E1300100} à {E2216000}, hors TVA et frais d'acquisition. Chaque logement s'accompagne de deux places de parking et d'un débarras pour {E34000} de plus.",
  'Von {E1300100} bis {E2216000}, zuzüglich MwSt. und Erwerbsnebenkosten. Zu jeder Einheit gehören zwei Stellplätze und ein Abstellraum für {E34000} mehr.',
  'От {E1300100} до {E2216000}, без НДС и расходов на оформление. К каждому объекту прилагаются два парковочных места и кладовая за дополнительные {E34000}.',
  'من {E1300100} إلى {E2216000}، دون ضريبة القيمة المضافة ومصاريف التملك. ويأتي مع كل مسكن موقفا سيارات ومخزن مقابل {E34000} إضافية.',
  'Van {E1300100} tot {E2216000}, exclusief btw en aankoopkosten. Bij elke woning horen twee parkeerplaatsen en een berging voor {E34000} extra.',
  'Od {E1300100} do {E2216000}, bez podatku VAT i kosztów nabycia. Do każdej nieruchomości przypisane są dwa miejsca postojowe i komórka lokatorska za dodatkowe {E34000}.',
  'Fra {E1300100} til {E2216000}, eksklusive mva og kjøpsomkostninger. Til hver bolig hører to parkeringsplasser og en bod for {E34000} ekstra.',
  'Från {E1300100} till {E2216000}, exklusive IVA (spansk moms) och köpkostnader. Till varje bostad hör två parkeringsplatser och ett förråd för {E34000} extra.')
a(114, 'Nine: two ground-floor',
  'Nueve: dos apartamentos con jardín en planta baja, cuatro áticos y tres villas pareadas.',
  'Neuf : deux appartements avec jardin en rez-de-chaussée, quatre penthouses et trois villas jumelées.',
  'Neun: zwei Gartenwohnungen im Erdgeschoss, vier Penthäuser und drei Doppelhaushälften.',
  'Девять: две квартиры с садом на первом этаже, четыре пентхауса и три парных дома.',
  'تسعة: شقتان بحديقة في الطابق الأرضي، وأربع شقق بنتهاوس، وثلاث فلل شبه منفصلة.',
  "Negen: twee tuinappartementen op de begane grond, vier penthouses en drie halfvrijstaande villa's.",
  "Dziewięć: dwa mieszkania z ogrodem na parterze, cztery penthouse'y i trzy domy bliźniacze.",
  'Ni: to hageleiligheter i første etasje, fire toppleiligheter og tre tomannsvillaer.',
  'Nio: två trädgårdslägenheter på bottenvåningen, fyra takvåningar och tre parhus.')
a(115, 'From 173.98 to 264.44 sqm built',
  'De {N173.98} a {N264.44} {U} construidos, con {N139.52} a {N213.48} {U} útiles interiores y {N134.11} a {N220.63} {U} de terrazas, solárium y piscina.',
  'De {N173.98} à {N264.44} {U} construits, avec {N139.52} à {N213.48} {U} de surface utile intérieure et {N134.11} à {N220.63} {U} de terrasses, solarium et piscine.',
  '{N173.98} bis {N264.44} {U} bebaute Fläche, mit {N139.52} bis {N213.48} {U} Nutzfläche innen und {N134.11} bis {N220.63} {U} Terrassen, Solarium und Pool.',
  'От {N173.98} до {N264.44} {U} площади застройки, с {N139.52}–{N213.48} {U} полезной площади внутри и {N134.11}–{N220.63} {U} террас, солярия и бассейна.',
  'من {N173.98} إلى {N264.44} {U} مساحة مبنية، مع {N139.52} إلى {N213.48} {U} مساحة داخلية صافية و{N134.11} إلى {N220.63} {U} من التراسات والسولاريوم والمسبح.',
  'Van {N173.98} tot {N264.44} {U} bebouwd, met {N139.52} tot {N213.48} {U} nuttige binnenoppervlakte en {N134.11} tot {N220.63} {U} aan terrassen, solarium en zwembad.',
  'Od {N173.98} do {N264.44} {U} powierzchni zabudowy, z {N139.52}–{N213.48} {U} powierzchni użytkowej wewnątrz i {N134.11}–{N220.63} {U} tarasów, solarium i basenu.',
  'Fra {N173.98} til {N264.44} {U} bebygd areal, med {N139.52} til {N213.48} {U} innvendig nyttbart areal og {N134.11} til {N220.63} {U} terrasser, solterrasse og basseng.',
  'Från {N173.98} till {N264.44} {U} byggyta, med {N139.52} till {N213.48} {U} invändig nyttoyta och {N134.11} till {N220.63} {U} terrasser, solterrass och pool.')
a(116, 'Do the homes have a private pool?',
  '¿Tienen las viviendas piscina privada?', 'Les logements ont-ils une piscine privée ?', 'Haben die Einheiten einen eigenen Pool?',
  'Есть ли у объектов собственный бассейн?', 'هل للمساكن مسبح خاص؟', 'Hebben de woningen een privézwembad?',
  'Czy nieruchomości mają prywatny basen?', 'Har boligene privat basseng?', 'Har bostäderna egen pool?')
a(117, 'The drawings show one on every',
  'Los planos muestran una en cada vivienda disponible: {N11.80} {U} en los apartamentos con jardín, {N15.00} {U} en las villas y de {N11.60} a {N15.55} {U} en la cubierta de los áticos. El folleto incluye el solárium con piscina de los áticos entre los extras opcionales, así que confirmamos por escrito qué incluye el precio.',
  'Les plans en montrent une sur chaque logement disponible : {N11.80} {U} dans les appartements avec jardin, {N15.00} {U} dans les villas et {N11.60} à {N15.55} {U} sur le toit des penthouses. La brochure range le solarium avec piscine des penthouses parmi les options, nous confirmons donc par écrit ce que comprend le prix.',
  'Die Pläne zeigen bei jeder verfügbaren Einheit einen: {N11.80} {U} bei den Gartenwohnungen, {N15.00} {U} bei den Villen und {N11.60} bis {N15.55} {U} auf den Dächern der Penthäuser. Die Broschüre führt das Solarium mit Pool der Penthäuser unter den Sonderausstattungen auf; deshalb bestätigen wir schriftlich, was im Preis enthalten ist.',
  'На планах он есть у каждого доступного объекта: {N11.80} {U} у квартир с садом, {N15.00} {U} у вилл и от {N11.60} до {N15.55} {U} на крышах пентхаусов. Буклет относит солярий с бассейном у пентхаусов к дополнительным опциям, поэтому мы письменно подтверждаем, что входит в цену.',
  'تُظهر المخططات مسبحًا في كل مسكن متاح: {N11.80} {U} في الشقق ذات الحديقة، و{N15.00} {U} في الفلل، ومن {N11.60} إلى {N15.55} {U} على أسطح البنتهاوس. ويدرج الكتيب سولاريوم البنتهاوس مع المسبح ضمن الإضافات الاختيارية، لذلك نؤكد كتابيًا ما يشمله السعر.',
  "De plattegronden tonen er een bij elke beschikbare woning: {N11.80} {U} bij de tuinappartementen, {N15.00} {U} bij de villa's en {N11.60} tot {N15.55} {U} op het dak van de penthouses. De brochure noemt het solarium met zwembad van de penthouses bij de opties, dus wij bevestigen schriftelijk wat de prijs omvat.",
  "Rzuty pokazują go przy każdej dostępnej nieruchomości: {N11.80} {U} w mieszkaniach z ogrodem, {N15.00} {U} w willach i od {N11.60} do {N15.55} {U} na dachach penthouse'ów. Broszura wymienia solarium z basenem w penthouse'ach wśród opcji dodatkowych, dlatego na piśmie potwierdzamy, co obejmuje cena.",
  'Tegningene viser ett ved hver tilgjengelige bolig: {N11.80} {U} i hageleilighetene, {N15.00} {U} i villaene og {N11.60} til {N15.55} {U} på taket av toppleilighetene. Brosjyren oppgir toppleilighetenes solterrasse med basseng som tilvalg, så vi bekrefter skriftlig hva prisen omfatter.',
  'Ritningarna visar en till varje ledig bostad: {N11.80} {U} i trädgårdslägenheterna, {N15.00} {U} i villorna och {N11.60} till {N15.55} {U} på takvåningarnas tak. Broschyren anger takvåningarnas solterrass med pool som tillval, så vi bekräftar skriftligt vad priset omfattar.')
a(118, 'Two parking spaces and a storage room come with each home on',
  'En la lista del promotor, cada vivienda lleva dos plazas de garaje y un trastero, por {E34000} además del precio indicado.',
  "Sur la liste du promoteur, chaque logement s'accompagne de deux places de parking et d'un débarras, pour {E34000} en plus du prix indiqué.",
  'Laut Liste des Bauträgers gehören zu jeder Einheit zwei Stellplätze und ein Abstellraum, für {E34000} zusätzlich zum genannten Preis.',
  'По списку застройщика к каждому объекту прилагаются два парковочных места и кладовая — за {E34000} сверх указанной цены.',
  'وفق قائمة المطور، يأتي مع كل مسكن موقفا سيارات ومخزن مقابل {E34000} فوق السعر المذكور.',
  'Op de lijst van de ontwikkelaar horen bij elke woning twee parkeerplaatsen en een berging, voor {E34000} bovenop de genoemde prijs.',
  'Według listy dewelopera do każdej nieruchomości przypisane są dwa miejsca postojowe i komórka lokatorska, za {E34000} ponad podaną cenę.',
  'På utbyggerens liste hører to parkeringsplasser og en bod til hver bolig, for {E34000} i tillegg til oppgitt pris.',
  'På exploatörens lista hör två parkeringsplatser och ett förråd till varje bostad, för {E34000} utöver det angivna priset.')
a(119, 'What does the wider scheme offer?',
  '¿Qué ofrece el conjunto completo?', "Qu'offre l'ensemble dans sa totalité ?", 'Was bietet die gesamte Anlage?',
  'Что предлагает комплекс в целом?', 'ماذا يقدم المجمع بأكمله؟', 'Wat biedt het hele complex?', 'Co oferuje całe osiedle?',
  'Hva tilbyr anlegget som helhet?', 'Vad erbjuder anläggningen som helhet?')
a(120, 'Residents share the communal areas of every phase',
  'Los residentes comparten las zonas comunes de todas las fases: el folleto enumera cuatro piscinas exteriores y una cubierta, un spa con sauna y baño turco, gimnasio, zona de coworking, cafetería, conserjería 24 horas y un centro de bicicletas eléctricas. Las cuotas de comunidad no están publicadas; las solicitamos.',
  "Les résidents partagent les parties communes de toutes les phases : la brochure cite quatre piscines extérieures et une piscine couverte, un spa avec sauna et hammam, une salle de sport, un espace de coworking, un café, une conciergerie 24 h/24 et un centre de vélos électriques. Les charges de copropriété ne sont pas publiées ; nous les demandons.",
  'Die Bewohner teilen die Gemeinschaftsbereiche aller Bauabschnitte: Die Broschüre nennt vier Außenpools und ein Hallenbad, ein Spa mit Sauna und türkischem Bad, einen Fitnessraum, einen Coworking-Bereich, ein Café, einen 24-Stunden-Concierge und eine E-Bike-Station. Die Gemeinschaftskosten sind nicht veröffentlicht; wir fordern sie an.',
  'Жители пользуются общими зонами всех очередей: в буклете перечислены четыре открытых бассейна и крытый бассейн, спа с сауной и турецкой баней, спортзал, коворкинг, кафе, круглосуточный консьерж и центр электровелосипедов. Размер взносов в сообщество не опубликован; мы его запрашиваем.',
  'يتشارك السكان المرافق المشتركة لجميع المراحل: يذكر الكتيب أربعة مسابح خارجية ومسبحًا داخليًا، وسبا مع ساونا وحمام تركي، وصالة رياضة، ومساحة عمل مشتركة، ومقهى، وخدمة كونسيرج على مدار الساعة، ومركزًا للدراجات الكهربائية. رسوم المجمع غير منشورة، ونحن نطلبها.',
  'Bewoners delen de gemeenschappelijke voorzieningen van alle fasen: de brochure noemt vier buitenzwembaden en een binnenzwembad, een spa met sauna en Turks bad, een fitnessruimte, een coworkingruimte, een koffiebar, een conciërge die 24 uur per dag beschikbaar is en een e-bikecentrum. De servicekosten zijn niet gepubliceerd; wij vragen ze op.',
  'Mieszkańcy korzystają z części wspólnych wszystkich etapów: broszura wymienia cztery baseny zewnętrzne i basen kryty, spa z sauną i łaźnią turecką, siłownię, strefę coworkingu, kawiarnię, całodobową usługę concierge i centrum rowerów elektrycznych. Opłaty wspólnotowe nie zostały opublikowane; występujemy o nie.',
  'Beboerne deler fellesarealene i alle byggetrinn: brosjyren nevner fire utendørsbassenger og et innendørsbasseng, et spa med badstue og tyrkisk bad, treningsrom, et coworking-område, en kafé, døgnåpen concierge og et senter for elsykler. Fellesutgiftene er ikke publisert; vi ber om dem.',
  'De som bor här delar de gemensamma ytorna i alla etapper: broschyren nämner fyra utomhuspooler och en inomhuspool, ett spa med bastu och turkiskt bad, ett gym, en coworkingyta, ett kafé, en concierge dygnet runt och en elcykelcentral. Samfällighetsavgifterna är inte publicerade; vi begär dem.')
a(121, 'The developer has not published a date for this phase',
  'El promotor no ha publicado una fecha para esta fase. La obra ha comenzado, y pedimos la fecha por escrito antes de cualquier reserva.',
  "Le promoteur n'a pas publié de date pour cette phase. Le chantier a commencé, et nous demandons la date par écrit avant toute réservation.",
  'Der Bauträger hat für diesen Bauabschnitt keinen Termin veröffentlicht. Der Bau hat begonnen, und wir fordern den Termin vor jeder Reservierung schriftlich an.',
  'Застройщик не опубликовал срок для этой очереди. Строительство началось, и мы запрашиваем срок письменно до любого бронирования.',
  'لم ينشر المطور تاريخًا لهذه المرحلة. بدأ البناء، ونطلب التاريخ كتابيًا قبل أي حجز.',
  'De ontwikkelaar heeft voor deze fase geen datum gepubliceerd. De bouw is begonnen, en wij vragen de datum schriftelijk op vóór elke reservering.',
  'Deweloper nie opublikował terminu dla tego etapu. Budowa się rozpoczęła, a o termin występujemy na piśmie przed każdą rezerwacją.',
  'Utbyggeren har ikke publisert en dato for dette byggetrinnet. Byggingen har startet, og vi ber om datoen skriftlig før enhver reservasjon.',
  'Exploatören har inte publicerat något datum för den här etappen. Bygget har startat, och vi begär datumet skriftligt före varje bokning.')

# ---------------------------------------------------------------- enquiry and seo
# The enquiry lines are the sibling's own sentences with the name swapped, so the form reads the
# same on every project page.
sib = json.load(open('content/liora-projects/la-resina-hillside-residences/project.json'))
for hint, key in (('I would like to receive the latest', 'message'), ('Project context:', 'note')):
    en = find(hint)
    T[en] = {l: sib['i18n'][l]['enquiry'][key].replace('La Resina Hillside Residences', 'Golfside Hill Residences') for l in LOCS}
    for l in LOCS:
        assert 'Golfside Hill Residences' in T[en][l], (en, l)
a(124, 'Golfside Hill Residences - Marbella',
  'Golfside Hill Residences - Marbella', 'Golfside Hill Residences - Marbella', 'Golfside Hill Residences - Marbella',
  'Golfside Hill Residences - Марбелья', 'Golfside Hill Residences - ماربيا', 'Golfside Hill Residences - Marbella',
  'Golfside Hill Residences - Marbella', 'Golfside Hill Residences - Marbella', 'Golfside Hill Residences - Marbella')
a(125, 'Golfside Hill Residences: Nine',
  'Golfside Hill Residences: nueve viviendas, Marbella', 'Golfside Hill Residences : neuf logements, Marbella',
  'Golfside Hill Residences: neun Wohneinheiten, Marbella', 'Golfside Hill Residences: девять объектов, Марбелья',
  'Golfside Hill Residences: تسعة مساكن، ماربيا', 'Golfside Hill Residences: negen woningen, Marbella',
  'Golfside Hill Residences: dziewięć nieruchomości, Marbella', 'Golfside Hill Residences: ni boliger, Marbella',
  'Golfside Hill Residences: nio bostäder, Marbella')
a(126, 'Nine Homes, Marbella',
  'Nueve viviendas, Marbella', 'Neuf logements, Marbella', 'Neun Wohneinheiten, Marbella', 'Девять объектов, Марбелья',
  'تسعة مساكن، ماربيا', 'Negen woningen, Marbella', 'Dziewięć nieruchomości, Marbella', 'Ni boliger, Marbella', 'Nio bostäder, Marbella')

# ---------------------------------------------------------------- strings the TM or mech would get wrong here
# The card's built-area range: assemble's Norwegian word for "built" is a usable-area word, so it is
# written here with the one the size column uses.
T['173.98 - 264.44 sqm built'] = {l: f"{num('173.98', l)} - {num('264.44', l)} {UNIT[l]} {W[l][0]}" for l in LOCS}
# German: the settled word for penthouses is Penthäuser.
T['Apartments, Penthouses & Villas'] = {
    'es': 'Apartamentos, áticos y villas', 'fr': 'Appartements, penthouses et villas', 'de': 'Wohnungen, Penthäuser und Villen',
    'ru': 'Апартаменты, пентхаусы и виллы', 'ar': 'شقق وبنتهاوس وفلل', 'nl': 'Appartementen, penthouses en villa’s',
    'pl': 'Apartamenty, penthouse’y i wille', 'no': 'Leiligheter, toppleiligheter og villaer', 'sv': 'Lägenheter, takvåningar och villor'}

# Norwegian: the memory's wording for these four addresses the reader as "du"; the brief for this
# batch asks for formal address, and the site's own guard forbids "dere", so they are written
# without a pronoun for the reader. The other eight languages keep the memory's wording.
tm = json.load(open(f'{SP}/tm.json'))
for en, no in (
        ('What Nueva Living verifies before you commit.', 'Hva Nueva Living kontrollerer før noe avtales.'),
        ('The developer has not published them for this release. We confirm them in writing before you commit.',
         'Utbyggeren har ikke publisert dem for dette salgstrinnet. Vi bekrefter dem skriftlig før noe avtales.'),
        ('Share your details and we will send you the current project information.',
         'Legg igjen kontaktopplysningene, så sender vi gjeldende prosjektinformasjon.'),
        ('Thank you. We have received your enquiry and will be in touch.', 'Takk. Vi har mottatt henvendelsen og tar kontakt.'),
        ('We arrange the visit and walk the slope and the communal areas with you.',
         'Vi ordner visningen og går gjennom skråningen og fellesarealene på stedet.')):
    T[en] = dict(tm[en])
    T[en]['no'] = no

# The villa rows: tools/import/floor_parts.json has drifted from scripts/lib/unit_floor_parts.mjs
# for "semi-detached villa" in ru, pl and sv, and the page copy above uses the FLOOR_PARTS words,
# so these three labels are written from FLOOR_PARTS and FLOOR_PREFIXES directly.
SEMI = {'es': 'Villa pareada', 'fr': 'Villa jumelée', 'de': 'Doppelhaushälfte', 'ru': 'Парный дом', 'ar': 'فيلا شبه منفصلة',
        'nl': 'Halfvrijstaande villa', 'pl': 'Dom bliźniaczy', 'sv': 'Parhus', 'no': 'Tomannsvilla'}
BLOCK = {'es': 'Bloque', 'fr': 'Bloc', 'de': 'Block', 'ru': 'Блок', 'ar': 'مبنى', 'nl': 'Blok', 'pl': 'Blok', 'sv': 'Hus', 'no': 'Hus'}
for en in todo:
    m = re.fullmatch(r'Semi-Detached Villa, Block (\d+)', en)
    if m:
        T[en] = {l: f'{SEMI[l]}, {BLOCK[l]} {m.group(1)}' for l in LOCS}

# The remaining floor labels ("First Floor, Block 19") are plain FLOOR_PARTS phrases that
# assemble.py writes itself.
FLOOR = re.compile(r'(Ground|First) Floor, Block \d+')
missing = [(i, s) for i, s in enumerate(todo) if s not in T and not FLOOR.fullmatch(s)]
assert not missing, missing
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries to', f'{SP}/tr_a.json')
