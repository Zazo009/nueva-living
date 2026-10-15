# -*- coding: utf-8 -*-
"""Azahar Residences: the strings the translation memory did not have.

Keyed by the English string, as k_olmo.py is, so a change to the English copy cannot silently shift
a translation onto the wrong sentence. Tokens: {E363000} money, {N67.16} decimal number, {U} the area
unit. The unit sizes, the floorplan labels and the unit references are built from per-locale templates
at the bottom of the file.
    python3 tools/import/k_azahar.py <scratch dir>      (writes <dir>/tr_z.json, then run assemble.py)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {l: 'm²' for l in LOCS}; UNIT['ru'] = 'м²'; UNIT['ar'] = 'م²'
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


def a(en, *tr):
    assert len(tr) == 9, (en[:50], len(tr))
    assert en not in T, en[:50]
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    T[en] = {l: en for l in LOCS}


# identifiers: the invented name, the place and the developer's own home codes read the same everywhere
for s in ['Azahar Residences', 'Azahar', 'Azahar <em>Residences</em>', 'El Calvario, Estepona',
          '1-0-A0', '1-2-B2', '1-2-D2', '1-3-B3', '3-0-C0', '3-2-A2', '3-2-C2', '3-2-D2']:
    same(s)

# ---------------------------------------------------------------- the money line
a('From EUR 363,000 + VAT', 'Desde {E363000} + IVA', 'À partir de {E363000} + TVA', 'Ab {E363000} + MwSt.',
  'От {E363000} + НДС', 'ابتداءً من {E363000} + ضريبة القيمة المضافة', 'Vanaf {E363000} + btw', 'Od {E363000} + VAT',
  'Fra {E363000} + mva.', 'Från {E363000} + moms')
a('EUR 363,000 + VAT', '{E363000} + IVA', '{E363000} + TVA', '{E363000} + MwSt.', '{E363000} + НДС',
  '{E363000} + ضريبة القيمة المضافة', '{E363000} + btw', '{E363000} + VAT', '{E363000} + mva.', '{E363000} + moms')
a('EUR 363,000 - EUR 566,000 + VAT', '{E363000} - {E566000} + IVA', '{E363000} - {E566000} + TVA',
  '{E363000} - {E566000} + MwSt.', '{E363000} - {E566000} + НДС', '{E363000} - {E566000} + ضريبة القيمة المضافة',
  '{E363000} - {E566000} + btw', '{E363000} – {E566000} + VAT', '{E363000} - {E566000} + mva.', '{E363000} - {E566000} + moms')
a('EUR 363,000 - EUR 566,000', '{E363000} - {E566000}', '{E363000} - {E566000}', '{E363000} - {E566000}',
  '{E363000} - {E566000}', '{E363000} - {E566000}', '{E363000} - {E566000}', '{E363000} – {E566000}',
  '{E363000} - {E566000}', '{E363000} - {E566000}')
a('47.99 - 84.92 sqm', '{N47.99} - {N84.92} {U}', '{N47.99} - {N84.92} {U}', '{N47.99} - {N84.92} {U}',
  '{N47.99} - {N84.92} {U}', '{N47.99} - {N84.92} {U}', '{N47.99} - {N84.92} {U}', '{N47.99}–{N84.92} {U}',
  '{N47.99} - {N84.92} {U}', '{N47.99} - {N84.92} {U}')
a('64.77 - 113.52 sqm', '{N64.77} - {N113.52} {U}', '{N64.77} - {N113.52} {U}', '{N64.77} - {N113.52} {U}',
  '{N64.77} - {N113.52} {U}', '{N64.77} - {N113.52} {U}', '{N64.77} - {N113.52} {U}', '{N64.77}–{N113.52} {U}',
  '{N64.77} - {N113.52} {U}', '{N64.77} - {N113.52} {U}')
a('Built area', 'Superficie construida', 'Surface construite', 'Bebaute Fläche', 'Площадь застройки', 'المساحة المبنية',
  'Bebouwde oppervlakte', 'Powierzchnia zabudowy', 'Bebygd areal', 'Byggyta')

# ---------------------------------------------------------------- the descriptions
a('8 of 40 apartments with one to three bedrooms in a closed complex in El Calvario, Estepona, each with a garage space and a storage room, and a shared pool, gym and multipurpose room. The works have started and no delivery date is stated. From EUR 363,000 plus VAT.',
  '8 de 40 apartamentos de uno a tres dormitorios en un conjunto cerrado en El Calvario, Estepona, cada uno con plaza de garaje y trastero, y con piscina, gimnasio y sala polivalente comunitarios. Las obras han comenzado y no se indica fecha de entrega. Desde {E363000} más IVA.',
  '8 des 40 appartements d’une à trois chambres, dans une résidence fermée à El Calvario, Estepona, chacun avec une place de garage et une cave, et avec piscine, salle de sport et salle polyvalente communes. Les travaux ont commencé et aucune date de livraison n’est indiquée. À partir de {E363000} hors TVA.',
  '8 von 40 Wohnungen mit einem bis drei Schlafzimmern in einer geschlossenen Wohnanlage in El Calvario, Estepona, jeweils mit Garagenstellplatz und Abstellraum sowie gemeinsamem Pool, Fitnessraum und Mehrzweckraum. Die Bauarbeiten haben begonnen, ein Übergabetermin ist nicht angegeben. Ab {E363000} zuzüglich MwSt.',
  '8 из 40 квартир с одной–тремя спальнями в закрытом жилом комплексе в Эль-Кальварио, Эстепона: у каждой есть место в гараже и кладовая, а для всех жителей — бассейн, тренажёрный зал и многофункциональное помещение. Строительство начато, срок сдачи не указан. От {E363000} без НДС.',
  '8 من أصل 40 شقة بغرفة إلى ثلاث غرف نوم في مجمع سكني مغلق في إل كالفاريو، إستيبونا، لكل منها موقف في المرآب وغرفة تخزين، مع مسبح وصالة رياضية وقاعة متعددة الاستخدامات مشتركة. بدأت الأعمال ولم يُذكر موعد تسليم. ابتداءً من {E363000} دون ضريبة القيمة المضافة.',
  '8 van de 40 appartementen met één tot drie slaapkamers in een besloten complex in El Calvario, Estepona, elk met een garageplaats en een berging, en met een gedeeld zwembad, fitnessruimte en multifunctionele ruimte. De werken zijn gestart en er wordt geen opleveringsdatum genoemd. Vanaf {E363000} excl. btw.',
  '8 z 40 mieszkań z jedną do trzech sypialni w zamkniętym osiedlu w El Calvario w Esteponie, każde z miejscem garażowym i komórką lokatorską, a także ze wspólnym basenem, siłownią i salą wielofunkcyjną. Prace budowlane się rozpoczęły, a termin oddania nie jest podany. Od {E363000} plus VAT.',
  '8 av 40 leiligheter med ett til tre soverom i et lukket boligområde i El Calvario, Estepona, hver med garasjeplass og bod, og med felles basseng, treningsrom og flerbruksrom. Byggearbeidene er startet, og ingen overleveringsdato er oppgitt. Fra {E363000} pluss mva.',
  '8 av 40 lägenheter med ett till tre sovrum i ett slutet bostadsområde i El Calvario, Estepona, var och en med garageplats och förråd, samt gemensam pool, gemensamt gym och ett flexibelt rum. Byggarbetena har påbörjats och inget tillträdesdatum anges. Från {E363000} plus moms.')
a('8 of 40 one-, two- and three-bedroom apartments in a closed complex in Estepona, each with garage and storage, a pool, a gym and a multipurpose room, works started, from EUR 363,000 plus VAT.',
  '8 de 40 apartamentos de uno, dos y tres dormitorios en un conjunto cerrado en Estepona, cada uno con garaje y trastero, piscina, gimnasio y sala polivalente, obras iniciadas, desde {E363000} más IVA.',
  '8 des 40 appartements d’une, deux et trois chambres dans une résidence fermée à Estepona, chacun avec garage et cave, piscine, salle de sport et salle polyvalente, travaux commencés, à partir de {E363000} hors TVA.',
  '8 von 40 Wohnungen mit einem, zwei und drei Schlafzimmern in einer geschlossenen Wohnanlage in Estepona, jeweils mit Garage und Abstellraum, Pool, Fitnessraum und Mehrzweckraum, Bau begonnen, ab {E363000} zuzüglich MwSt.',
  '8 из 40 квартир с одной, двумя и тремя спальнями в закрытом комплексе в Эстепоне: у каждой гараж и кладовая, есть бассейн, тренажёрный зал и многофункциональное помещение, строительство начато, от {E363000} без НДС.',
  '8 من أصل 40 شقة بغرفة وغرفتين وثلاث غرف نوم في مجمع مغلق في إستيبونا، لكل منها مرآب وغرفة تخزين، مع مسبح وصالة رياضية وقاعة متعددة الاستخدامات، والأعمال بدأت، ابتداءً من {E363000} دون ضريبة القيمة المضافة.',
  '8 van de 40 appartementen met één, twee en drie slaapkamers in een besloten complex in Estepona, elk met garage en berging, een zwembad, een fitnessruimte en een multifunctionele ruimte, bouw gestart, vanaf {E363000} excl. btw.',
  '8 z 40 mieszkań z jedną, dwiema i trzema sypialniami w zamkniętym osiedlu w Esteponie, każde z garażem i komórką lokatorską, basen, siłownia i sala wielofunkcyjna, budowa rozpoczęta, od {E363000} plus VAT.',
  '8 av 40 leiligheter med ett, to og tre soverom i et lukket boligområde i Estepona, hver med garasje og bod, basseng, treningsrom og flerbruksrom, byggingen er startet, fra {E363000} pluss mva.',
  '8 av 40 lägenheter med ett, två och tre sovrum i ett slutet bostadsområde i Estepona, var och en med garage och förråd, pool, gym och ett flexibelt rum, byggstart gjord, från {E363000} plus moms.')
a('One-, two- and three-bedroom apartments in Estepona with garage and storage, from EUR 363,000 plus VAT.',
  'Apartamentos de uno, dos y tres dormitorios en Estepona con garaje y trastero, desde {E363000} más IVA.',
  'Appartements d’une, deux et trois chambres à Estepona avec garage et cave, à partir de {E363000} hors TVA.',
  'Wohnungen mit einem, zwei und drei Schlafzimmern in Estepona mit Garage und Abstellraum, ab {E363000} zuzüglich MwSt.',
  'Квартиры с одной, двумя и тремя спальнями в Эстепоне с гаражом и кладовой, от {E363000} без НДС.',
  'شقق بغرفة وغرفتين وثلاث غرف نوم في إستيبونا مع مرآب وغرفة تخزين، ابتداءً من {E363000} دون ضريبة القيمة المضافة.',
  'Appartementen met één, twee en drie slaapkamers in Estepona met garage en berging, vanaf {E363000} excl. btw.',
  'Mieszkania z jedną, dwiema i trzema sypialniami w Esteponie z garażem i komórką lokatorską, od {E363000} plus VAT.',
  'Leiligheter med ett, to og tre soverom i Estepona med garasje og bod, fra {E363000} pluss mva.',
  'Lägenheter med ett, två och tre sovrum i Estepona med garage och förråd, från {E363000} plus moms.')
a('8 of 40 one-, two- and three-bedroom apartments in a closed complex in Estepona, each with a garage space and a storage room, with a pool and a gym.',
  '8 de 40 apartamentos de uno, dos y tres dormitorios en un conjunto cerrado en Estepona, cada uno con plaza de garaje y trastero, con piscina y gimnasio.',
  '8 des 40 appartements d’une, deux et trois chambres dans une résidence fermée à Estepona, chacun avec une place de garage et une cave, avec piscine et salle de sport.',
  '8 von 40 Wohnungen mit einem, zwei und drei Schlafzimmern in einer geschlossenen Wohnanlage in Estepona, jeweils mit Garagenstellplatz und Abstellraum, mit Pool und Fitnessraum.',
  '8 из 40 квартир с одной, двумя и тремя спальнями в закрытом комплексе в Эстепоне: у каждой есть место в гараже и кладовая, в комплексе есть бассейн и тренажёрный зал.',
  '8 من أصل 40 شقة بغرفة وغرفتين وثلاث غرف نوم في مجمع مغلق في إستيبونا، لكل منها موقف في المرآب وغرفة تخزين، مع مسبح وصالة رياضية.',
  '8 van de 40 appartementen met één, twee en drie slaapkamers in een besloten complex in Estepona, elk met een garageplaats en een berging, met een zwembad en een fitnessruimte.',
  '8 z 40 mieszkań z jedną, dwiema i trzema sypialniami w zamkniętym osiedlu w Esteponie, każde z miejscem garażowym i komórką lokatorską, z basenem i siłownią.',
  '8 av 40 leiligheter med ett, to og tre soverom i et lukket boligområde i Estepona, hver med garasjeplass og bod, med basseng og treningsrom.',
  '8 av 40 lägenheter med ett, två och tre sovrum i ett slutet bostadsområde i Estepona, var och en med garageplats och förråd, med pool och gym.')

# ---------------------------------------------------------------- images
a('Computer-generated view of two apartment blocks with stepped terraces and pergolas above the communal pool',
  'Vista generada por ordenador de dos bloques de apartamentos con terrazas escalonadas y pérgolas sobre la piscina comunitaria',
  'Vue de synthèse de deux blocs d’appartements avec terrasses en gradins et pergolas au-dessus de la piscine commune',
  'Computergenerierte Ansicht von zwei Wohnblöcken mit gestaffelten Terrassen und Pergolen über dem Gemeinschaftspool',
  'Компьютерная визуализация двух жилых корпусов с террасами уступами и перголами над общим бассейном',
  'منظر مُولَّد بالحاسوب لمبنيين سكنيين بتراسات متدرجة وبرغولات فوق المسبح المشترك',
  'Computergegenereerd beeld van twee appartementsblokken met getrapte terrassen en pergola’s boven het gemeenschappelijke zwembad',
  'Komputerowa wizualizacja dwóch bloków mieszkalnych z tarasami schodkowymi i pergolami nad wspólnym basenem',
  'Datagenerert bilde av to leilighetsblokker med trappetrinnsterrasser og pergolaer over det felles bassenget',
  'Datorgenererad bild av två flerbostadshus med trappstegsformade terrasser och pergolor ovanför den gemensamma poolen')
a('Computer-generated view of an apartment block with bands of vertical slats and wide terraces, seen from the street',
  'Vista generada por ordenador de un bloque de apartamentos con bandas de lamas verticales y amplias terrazas, visto desde la calle',
  'Vue de synthèse d’un bloc d’appartements avec des bandeaux de lames verticales et de larges terrasses, vu depuis la rue',
  'Computergenerierte Ansicht eines Wohnblocks mit Bändern aus senkrechten Lamellen und breiten Terrassen, von der Straße aus gesehen',
  'Компьютерная визуализация жилого корпуса с поясами вертикальных реек и широкими террасами, вид с улицы',
  'منظر مُولَّد بالحاسوب لمبنى سكني بأشرطة من الشرائح العمودية وتراسات واسعة، من جهة الشارع',
  'Computergegenereerd beeld van een appartementsblok met banden van verticale latten en brede terrassen, gezien vanaf de straat',
  'Komputerowa wizualizacja bloku mieszkalnego z pasami pionowych listew i szerokimi tarasami, widok od strony ulicy',
  'Datagenerert bilde av en leilighetsblokk med bånd av vertikale lameller og brede terrasser, sett fra gaten',
  'Datorgenererad bild av ett flerbostadshus med band av lodräta lameller och breda terrasser, sett från gatan')
a('Computer-generated rooftop terrace with lounge seating, sunbeds, planting and a view over the town',
  'Terraza en la azotea generada por ordenador con zona de estar, tumbonas, plantas y vistas a la ciudad',
  'Vue de synthèse d’une terrasse sur le toit avec salon, bains de soleil, plantations et vue sur la ville',
  'Computergenerierte Dachterrasse mit Loungemöbeln, Sonnenliegen, Bepflanzung und Blick über die Stadt',
  'Компьютерная визуализация террасы на крыше с зоной отдыха, шезлонгами, зеленью и видом на город',
  'سطح مُولَّد بالحاسوب بمقاعد جلوس وكراسي تشمّس ونباتات وإطلالة على المدينة',
  'Computergegenereerd dakterras met loungeplekken, ligbedden, beplanting en uitzicht over de stad',
  'Komputerowa wizualizacja tarasu na dachu ze strefą wypoczynku, leżakami, zielenią i widokiem na miasto',
  'Datagenerert takterrasse med loungemøbler, solsenger, beplantning og utsikt over byen',
  'Datorgenererad takterrass med loungemöbler, solsängar, växter och utsikt över staden')
a('Computer-generated main bedroom with a double bed, a mural of palm shadows and a fitted wardrobe, with a bathroom beyond',
  'Dormitorio principal generado por ordenador con cama doble, un mural de sombras de palmeras y un armario empotrado, con un baño al fondo',
  'Vue de synthèse d’une chambre principale avec un lit double, une fresque d’ombres de palmiers et un placard intégré, et une salle de bains au fond',
  'Computergeneriertes Hauptschlafzimmer mit Doppelbett, einem Wandbild mit Palmenschatten und einem Einbauschrank, dahinter ein Bad',
  'Компьютерная визуализация главной спальни с двуспальной кроватью, панно с тенями пальм и встроенным шкафом, за которой видна ванная комната',
  'غرفة نوم رئيسية مُولَّدة بالحاسوب بسرير مزدوج وجدارية لظلال النخيل وخزانة مدمجة، ويظهر خلفها حمام',
  'Computergegenereerde hoofdslaapkamer met een tweepersoonsbed, een muurschildering met palmschaduwen en een inbouwkast, met een badkamer erachter',
  'Komputerowa wizualizacja sypialni głównej z podwójnym łóżkiem, muralem z cieniami palm i szafą w zabudowie, a za nią łazienka',
  'Datagenerert hovedsoverom med dobbeltseng, et veggbilde av palmeskygger og innebygd garderobeskap, med et bad innenfor',
  'Datorgenererat huvudsovrum med dubbelsäng, en väggmålning av palmskuggor och en inbyggd garderob, med ett badrum innanför')
a('The blocks above the communal pool', 'Los bloques sobre la piscina comunitaria', 'Les blocs au-dessus de la piscine commune',
  'Die Blöcke über dem Gemeinschaftspool', 'Корпуса над общим бассейном', 'المبنيان فوق المسبح المشترك',
  'De blokken boven het gemeenschappelijke zwembad', 'Bloki nad wspólnym basenem', 'Blokkene over det felles bassenget',
  'Husen ovanför den gemensamma poolen')
a('The facade on the street', 'La fachada a la calle', 'La façade sur la rue', 'Die Fassade zur Straße', 'Фасад со стороны улицы',
  'الواجهة المطلة على الشارع', 'De gevel aan de straat', 'Elewacja od strony ulicy', 'Fasaden mot gaten', 'Fasaden mot gatan')
a('Computer-generated view of the blocks on a street corner, with lawn and flowering shrubs in front',
  'Vista generada por ordenador de los bloques en una esquina de la calle, con césped y arbustos en flor delante',
  'Vue de synthèse des blocs à l’angle d’une rue, avec de la pelouse et des arbustes en fleurs au premier plan',
  'Computergenerierte Ansicht der Blöcke an einer Straßenecke, davor Rasen und blühende Sträucher',
  'Компьютерная визуализация корпусов на углу улицы, впереди газон и цветущие кусты',
  'منظر مُولَّد بالحاسوب للمبنيين عند ناصية شارع، وأمامهما عشب وشجيرات مزهرة',
  'Computergegenereerd beeld van de blokken op een straathoek, met gras en bloeiende struiken op de voorgrond',
  'Komputerowa wizualizacja bloków na rogu ulicy, z trawnikiem i kwitnącymi krzewami na pierwszym planie',
  'Datagenerert bilde av blokkene i et gatehjørne, med plen og blomstrende busker foran',
  'Datorgenererad bild av husen i ett gathörn, med gräsmatta och blommande buskar framför')
a('The corner from the roundabout', 'La esquina desde la rotonda', 'L’angle vu depuis le rond-point', 'Die Ecke vom Kreisverkehr aus',
  'Угол здания со стороны кольцевой развязки', 'الزاوية من جهة الدوّار', 'De hoek vanaf de rotonde', 'Narożnik od strony ronda',
  'Hjørnet sett fra rundkjøringen', 'Hörnet sett från rondellen')
a('Computer-generated view of a corner of the building with white walls and bands of vertical slats under a deep blue sky',
  'Vista generada por ordenador de una esquina del edificio con paredes blancas y bandas de lamas verticales bajo un cielo azul intenso',
  'Vue de synthèse d’un angle du bâtiment avec des murs blancs et des bandeaux de lames verticales sous un ciel d’un bleu profond',
  'Computergenerierte Ansicht einer Gebäudeecke mit weißen Wänden und Bändern aus senkrechten Lamellen unter tiefblauem Himmel',
  'Компьютерная визуализация угла здания с белыми стенами и поясами вертикальных реек под глубоким синим небом',
  'منظر مُولَّد بالحاسوب لزاوية المبنى بجدران بيضاء وأشرطة من الشرائح العمودية تحت سماء زرقاء داكنة',
  'Computergegenereerd beeld van een hoek van het gebouw met witte muren en banden van verticale latten onder een diepblauwe lucht',
  'Komputerowa wizualizacja narożnika budynku z białymi ścianami i pasami pionowych listew pod głęboko błękitnym niebem',
  'Datagenerert bilde av et hjørne av bygningen med hvite vegger og bånd av vertikale lameller under en dypblå himmel',
  'Datorgenererad bild av ett hörn av byggnaden med vita väggar och band av lodräta lameller under en djupblå himmel')
a('The corner facade', 'La fachada de la esquina', 'La façade d’angle', 'Die Eckfassade', 'Угловой фасад', 'الواجهة الزاوية',
  'De hoekgevel', 'Elewacja narożna', 'Hjørnefasaden', 'Hörnfasaden')
a('Computer-generated view of the blocks and a pedestrian entrance from the street, with a crossing and parked cars',
  'Vista generada por ordenador de los bloques y de una entrada peatonal desde la calle, con un paso de peatones y coches aparcados',
  'Vue de synthèse des blocs et d’une entrée piétonne depuis la rue, avec un passage piéton et des voitures en stationnement',
  'Computergenerierte Ansicht der Blöcke und eines Fußgängereingangs von der Straße aus, mit Zebrastreifen und geparkten Autos',
  'Компьютерная визуализация корпусов и пешеходного входа со стороны улицы, с пешеходным переходом и припаркованными автомобилями',
  'منظر مُولَّد بالحاسوب للمبنيين ومدخل للمشاة من جهة الشارع، مع ممر مشاة وسيارات متوقفة',
  'Computergegenereerd beeld van de blokken en een voetgangersingang vanaf de straat, met een zebrapad en geparkeerde auto’s',
  'Komputerowa wizualizacja bloków i wejścia dla pieszych od strony ulicy, z przejściem dla pieszych i zaparkowanymi samochodami',
  'Datagenerert bilde av blokkene og en gangadkomst fra gaten, med fotgjengerfelt og parkerte biler',
  'Datorgenererad bild av husen och en gångentré från gatan, med övergångsställe och parkerade bilar')
a('The entrance from the street', 'La entrada desde la calle', 'L’entrée depuis la rue', 'Der Eingang von der Straße',
  'Вход со стороны улицы', 'المدخل من جهة الشارع', 'De ingang vanaf de straat', 'Wejście od strony ulicy', 'Inngangen fra gaten', 'Entrén från gatan')
a('Aerial photograph of Estepona with the computer-generated building placed on the plot, and the sea beyond',
  'Fotografía aérea de Estepona con el edificio generado por ordenador situado en la parcela, y el mar al fondo',
  'Photographie aérienne d’Estepona avec le bâtiment de synthèse placé sur la parcelle, et la mer au loin',
  'Luftaufnahme von Estepona mit dem computergenerierten Gebäude auf dem Grundstück und dem Meer dahinter',
  'Аэрофотоснимок Эстепоны с компьютерной визуализацией здания на участке и морем на горизонте',
  'صورة جوية لإستيبونا مع المبنى المُولَّد بالحاسوب موضوعًا على القطعة، والبحر في الخلفية',
  'Luchtfoto van Estepona met het computergegenereerde gebouw op het perceel en de zee erachter',
  'Zdjęcie lotnicze Estepony z komputerową wizualizacją budynku umieszczoną na działce i morzem w tle',
  'Flyfoto av Estepona med den datagenererte bygningen plassert på tomten, og havet bak',
  'Flygfoto över Estepona med den datorgenererade byggnaden placerad på tomten, och havet bortom')
a('The plot in Estepona, with the sea beyond', 'La parcela en Estepona, con el mar al fondo', 'La parcelle à Estepona, avec la mer au loin',
  'Das Grundstück in Estepona, dahinter das Meer', 'Участок в Эстепоне, за ним море', 'القطعة في إستيبونا، والبحر خلفها',
  'Het perceel in Estepona, met de zee erachter', 'Działka w Esteponie, a za nią morze', 'Tomten i Estepona, med havet bak',
  'Tomten i Estepona, med havet bortom')
a('Computer-generated open-plan living room with a corner sofa, a slatted dining area and a kitchen with a breakfast bar',
  'Salón de planta abierta generado por ordenador con sofá rinconero, un comedor con paneles de lamas y una cocina con barra',
  'Vue de synthèse d’un séjour ouvert avec un canapé d’angle, un coin repas à lames de bois et une cuisine avec bar',
  'Computergenerierter offener Wohnbereich mit Ecksofa, einem Essbereich mit Lamellenwand und einer Küche mit Frühstückstheke',
  'Компьютерная визуализация гостиной в формате открытой планировки с угловым диваном, обеденной зоной с рейками и кухней с барной стойкой',
  'غرفة معيشة مفتوحة مُولَّدة بالحاسوب بأريكة زاوية ومنطقة طعام بشرائح خشبية ومطبخ ببار',
  'Computergegenereerde open woonkamer met een hoekbank, een eethoek met latten en een keuken met ontbijtbar',
  'Komputerowa wizualizacja otwartego salonu z narożną sofą, jadalnią z drewnianymi listwami i kuchnią z barkiem',
  'Datagenerert åpen stue med hjørnesofa, en spiseplass med lameller og et kjøkken med frokostbar',
  'Datorgenererat öppet vardagsrum med hörnsoffa, en matplats med lameller och ett kök med frukostbar')
a('Computer-generated kitchen with a breakfast bar and a living room opening onto a terrace with a pergola',
  'Cocina con barra generada por ordenador y un salón que se abre a una terraza con pérgola',
  'Vue de synthèse d’une cuisine avec bar et d’un séjour ouvrant sur une terrasse avec pergola',
  'Computergenerierte Küche mit Frühstückstheke und einem Wohnzimmer, das sich zu einer Terrasse mit Pergola öffnet',
  'Компьютерная визуализация кухни с барной стойкой и гостиной с выходом на террасу с перголой',
  'مطبخ مُولَّد بالحاسوب ببار وغرفة معيشة تفتح على تراس ببرغولا',
  'Computergegenereerde keuken met ontbijtbar en een woonkamer die uitkomt op een terras met pergola',
  'Komputerowa wizualizacja kuchni z barkiem i salonu z wyjściem na taras z pergolą',
  'Datagenerert kjøkken med frokostbar og en stue som åpner seg mot en terrasse med pergola',
  'Datorgenererat kök med frukostbar och ett vardagsrum som öppnar sig mot en terrass med pergola')
a('Kitchen, living room and terrace', 'Cocina, salón y terraza', 'Cuisine, séjour et terrasse', 'Küche, Wohnzimmer und Terrasse',
  'Кухня, гостиная и терраса', 'المطبخ وغرفة المعيشة والتراس', 'Keuken, woonkamer en terras', 'Kuchnia, salon i taras',
  'Kjøkken, stue og terrasse', 'Kök, vardagsrum och terrass')
a('Computer-generated bathroom with a wall-hung vanity, a backlit mirror and a walk-in shower beside a timber-effect tiled wall',
  'Baño generado por ordenador con mueble de lavabo suspendido, espejo retroiluminado y ducha a ras de suelo junto a una pared alicatada efecto madera',
  'Vue de synthèse d’une salle de bains avec un meuble vasque suspendu, un miroir rétroéclairé et une douche à l’italienne près d’un mur carrelé effet bois',
  'Computergeneriertes Bad mit wandhängendem Waschtischunterschrank, hinterleuchtetem Spiegel und einer bodengleichen Dusche neben einer Wand in Holzoptik',
  'Компьютерная визуализация ванной комнаты с подвесной тумбой под раковину, зеркалом с подсветкой и душем без поддона рядом со стеной с плиткой под дерево',
  'حمام مُولَّد بالحاسوب بخزانة مغسلة معلّقة ومرآة بإضاءة خلفية ودش مفتوح بجانب جدار مكسو ببلاط بمظهر الخشب',
  'Computergegenereerde badkamer met een zwevend wastafelmeubel, een verlichte spiegel en een inloopdouche naast een wand met tegels in houtlook',
  'Komputerowa wizualizacja łazienki z wiszącą szafką pod umywalkę, podświetlanym lustrem i prysznicem bez brodzika obok ściany z płytkami w kolorze drewna',
  'Datagenerert bad med veggmontert servantskap, et baklyst speil og en åpen dusj ved siden av en vegg med trelignende fliser',
  'Datorgenererat badrum med ett väggmonterat tvättställsskåp, en bakgrundsbelyst spegel och en duschhörna bredvid en vägg med kakel i träutförande')
a('Computer-generated gym with cardio machines, free weights, yoga mats and a seating area',
  'Gimnasio generado por ordenador con máquinas de cardio, pesas libres, esterillas de yoga y una zona de descanso',
  'Vue de synthèse d’une salle de sport avec appareils de cardio, poids libres, tapis de yoga et coin salon',
  'Computergenerierter Fitnessraum mit Cardiogeräten, Hanteln, Yogamatten und einer Sitzecke',
  'Компьютерная визуализация тренажёрного зала с кардиотренажёрами, свободными весами, ковриками для йоги и зоной отдыха',
  'صالة رياضية مُولَّدة بالحاسوب بأجهزة كارديو وأوزان حرة وبُسُط يوغا ومنطقة جلوس',
  'Computergegenereerde fitnessruimte met cardioapparaten, losse gewichten, yogamatten en een zithoek',
  'Komputerowa wizualizacja siłowni ze sprzętem cardio, ciężarkami, matami do jogi i strefą wypoczynku',
  'Datagenerert treningsrom med kondisjonsapparater, frie vekter, yogamatter og en sittegruppe',
  'Datorgenererat gym med konditionsmaskiner, fria vikter, yogamattor och en sittgrupp')
a('Computer-generated views of the blocks, the pool and the interiors, and the floorplans of the eight homes listed.',
  'Vistas generadas por ordenador de los bloques, la piscina y los interiores, y los planos de las ocho viviendas a la venta.',
  'Vues de synthèse des blocs, de la piscine et des intérieurs, et plans des huit logements annoncés.',
  'Computergenerierte Ansichten der Blöcke, des Pools und der Innenräume sowie die Grundrisse der acht gelisteten Wohnungen.',
  'Компьютерные визуализации корпусов, бассейна и интерьеров, а также планировки восьми квартир, находящихся в продаже.',
  'مناظر مُولَّدة بالحاسوب للمبنيين والمسبح والمساحات الداخلية، ومخططات المساكن الثمانية المعروضة.',
  'Computergegenereerde beelden van de blokken, het zwembad en de interieurs, en de plattegronden van de acht aangeboden woningen.',
  'Komputerowe wizualizacje bloków, basenu i wnętrz oraz rzuty ośmiu oferowanych mieszkań.',
  'Datagenererte bilder av blokkene, bassenget og interiørene, og plantegningene til de åtte annonserte boligene.',
  'Datorgenererade bilder av husen, poolen och interiörerna samt planritningarna för de åtta listade bostäderna.')
a('All the views are computer-generated, apart from the aerial view, which places the computer-generated building in a photograph, and the furniture and decoration in them are illustrative and not included. The floorplans are the developer’s sales plans: they are not contractual, the room names on them are in Spanish, and the areas on them differ slightly from the price list.',
  'Todas las vistas están generadas por ordenador, salvo la vista aérea, que sitúa el edificio generado por ordenador en una fotografía, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los planos de venta del promotor: no tienen carácter contractual, los nombres de las estancias están en español y las superficies que figuran difieren ligeramente de la lista de precios.',
  'Toutes les vues sont des images de synthèse, à l’exception de la vue aérienne, qui place le bâtiment de synthèse dans une photographie, et le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont les plans de vente du promoteur : ils n’ont pas valeur contractuelle, le nom des pièces y est en espagnol et les surfaces indiquées diffèrent légèrement de la liste de prix.',
  'Alle Ansichten sind computergeneriert, mit Ausnahme der Luftaufnahme, die das computergenerierte Gebäude in ein Foto setzt; die darin gezeigten Möbel und die Dekoration dienen der Veranschaulichung und sind nicht enthalten. Die Grundrisse sind die Verkaufspläne des Bauträgers: Sie sind nicht vertraglich bindend, die Raumbezeichnungen sind auf Spanisch, und die darin angegebenen Flächen weichen geringfügig von der Preisliste ab.',
  'Все изображения созданы на компьютере, за исключением аэрофотоснимка, на котором компьютерная визуализация здания помещена в фотографию; мебель и декор на них приведены для иллюстрации и в стоимость не входят. Планировки — это продажные планы застройщика: они не имеют договорной силы, названия помещений на них даны по-испански, а указанные площади незначительно отличаются от прайс-листа.',
  'جميع المناظر مُولَّدة بالحاسوب، باستثناء المنظر الجوي الذي يضع المبنى المُولَّد بالحاسوب داخل صورة فوتوغرافية، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات هي مخططات البيع الخاصة بالمطوّر: وهي غير ملزمة تعاقديًا، وأسماء الغرف عليها بالإسبانية، والمساحات المذكورة فيها تختلف قليلًا عن قائمة الأسعار.',
  'Alle beelden zijn computergegenereerd, met uitzondering van de luchtfoto, die het computergegenereerde gebouw in een foto plaatst; de meubels en de inrichting erop zijn illustratief en niet inbegrepen. De plattegronden zijn de verkoopplattegronden van de ontwikkelaar: ze zijn niet contractueel, de ruimtenamen erop zijn in het Spaans en de vermelde oppervlakten wijken licht af van de prijslijst.',
  'Wszystkie wizualizacje są wygenerowane komputerowo, z wyjątkiem zdjęcia lotniczego, które umieszcza komputerowy model budynku na fotografii; widoczne na nich meble i wystrój mają charakter poglądowy i nie są wliczone w cenę. Rzuty to plany sprzedażowe dewelopera: nie mają charakteru umownego, nazwy pomieszczeń są po hiszpańsku, a podane na nich powierzchnie nieznacznie różnią się od cennika.',
  'Alle bildene er datagenererte, bortsett fra flyfotoet, som plasserer den datagenererte bygningen i et fotografi, og møblene og innredningen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens salgstegninger: de er ikke kontraktsfestet, romnavnene på dem er på spansk, og arealene på dem avviker noe fra prislisten.',
  'Alla bilder är datorgenererade, förutom flygfotot, som placerar den datorgenererade byggnaden i ett fotografi, och möblerna och inredningen i dem är illustrativa och ingår inte. Planritningarna är exploatörens säljplaner: de är inte avtalsgrundande, rummens namn på dem är på spanska och ytorna på dem avviker något från prislistan.')

# ---------------------------------------------------------------- overview
a('Forty homes, <em>eight available</em>', 'Cuarenta viviendas, <em>ocho disponibles</em>', 'Quarante logements, <em>huit disponibles</em>',
  'Vierzig Wohnungen, <em>acht verfügbar</em>', 'Сорок квартир, <em>восемь в продаже</em>', 'أربعون مسكنًا، <em>ثمانية منها متاحة</em>',
  'Veertig woningen, <em>acht beschikbaar</em>', 'Czterdzieści mieszkań, <em>osiem dostępnych</em>', 'Førti boliger, <em>åtte ledige</em>',
  'Fyrtio bostäder, <em>åtta lediga</em>')
a('This is a closed residential complex of 40 apartments with one, two and three bedrooms, in the El Calvario residential area of Estepona, near the new sports zone, the old town and the coastal path. Eight homes are listed with a price: two on the ground floor with a private garden, four on the second floor with a terrace and a solarium, one two-bedroom home with a terrace and one one-bedroom home. Each has a garage space and a storage room.',
  'Es un conjunto residencial cerrado de 40 apartamentos de uno, dos y tres dormitorios, en la zona residencial de El Calvario, en Estepona, cerca de la nueva zona deportiva, del casco antiguo y de la senda litoral. Ocho viviendas figuran con precio: dos en planta baja con jardín privado, cuatro en la segunda planta con terraza y solárium, una de dos dormitorios con terraza y una de un dormitorio. Cada una tiene plaza de garaje y trastero.',
  'Il s’agit d’une résidence fermée de 40 appartements d’une, deux et trois chambres, dans le quartier résidentiel d’El Calvario à Estepona, près du nouveau pôle sportif, de la vieille ville et du sentier littoral. Huit logements sont annoncés avec un prix : deux au rez-de-chaussée avec jardin privatif, quatre au deuxième étage avec terrasse et solarium, un de deux chambres avec terrasse et un d’une chambre. Chacun dispose d’une place de garage et d’une cave.',
  'Es handelt sich um eine geschlossene Wohnanlage mit 40 Wohnungen mit einem, zwei und drei Schlafzimmern im Wohngebiet El Calvario in Estepona, nahe der neuen Sportzone, der Altstadt und dem Küstenweg. Acht Wohnungen sind mit Preis gelistet: zwei im Erdgeschoss mit privatem Garten, vier im zweiten Obergeschoss mit Terrasse und Solarium, eine Wohnung mit zwei Schlafzimmern und Terrasse und eine Wohnung mit einem Schlafzimmer. Jede hat einen Garagenstellplatz und einen Abstellraum.',
  'Это закрытый жилой комплекс из 40 квартир с одной, двумя и тремя спальнями в жилом районе Эль-Кальварио в Эстепоне, рядом с новой спортивной зоной, старым городом и прибрежной тропой. С ценой указаны восемь квартир: две на первом этаже с частным садом, четыре на третьем этаже с террасой и солярием, одна с двумя спальнями и террасой и одна с одной спальней. У каждой есть место в гараже и кладовая.',
  'هو مجمع سكني مغلق من 40 شقة بغرفة وغرفتين وثلاث غرف نوم، في المنطقة السكنية إل كالفاريو في إستيبونا، قرب المنطقة الرياضية الجديدة والبلدة القديمة والممشى الساحلي. ثمانية مساكن معروضة بسعر: اثنان في الطابق الأرضي بحديقة خاصة، وأربعة في الطابق الثاني بتراس وسولاريوم، وواحد بغرفتي نوم وتراس، وواحد بغرفة نوم واحدة. ولكل منها موقف في المرآب وغرفة تخزين.',
  'Dit is een besloten woonwijk met 40 appartementen met één, twee en drie slaapkamers, in de woonwijk El Calvario in Estepona, bij de nieuwe sportzone, de oude stad en het kustpad. Acht woningen staan met prijs vermeld: twee op de begane grond met een privétuin, vier op de tweede verdieping met een terras en een solarium, één met twee slaapkamers en een terras en één met één slaapkamer. Elke woning heeft een garageplaats en een berging.',
  'Jest to zamknięte osiedle mieszkaniowe z 40 mieszkaniami z jedną, dwiema i trzema sypialniami, w dzielnicy mieszkalnej El Calvario w Esteponie, w pobliżu nowej strefy sportowej, starego miasta i nadmorskiej ścieżki. Osiem mieszkań podano z ceną: dwa na parterze z prywatnym ogrodem, cztery na drugim piętrze z tarasem i solarium, jedno z dwiema sypialniami i tarasem oraz jedno z jedną sypialnią. Każde ma miejsce garażowe i komórkę lokatorską.',
  'Dette er et lukket boligområde med 40 leiligheter med ett, to og tre soverom, i boligområdet El Calvario i Estepona, nær den nye idrettssonen, gamlebyen og kyststien. Åtte boliger er annonsert med pris: to i første etasje med privat hage, fire i tredje etasje med terrasse og solterrasse, en med to soverom og terrasse og en med ett soverom. Hver har garasjeplass og bod.',
  'Det här är ett slutet bostadsområde med 40 lägenheter med ett, två och tre sovrum, i bostadsområdet El Calvario i Estepona, nära den nya idrottszonen, gamla stan och kustpromenaden. Åtta bostäder är listade med pris: två på bottenvåningen med privat trädgård, fyra på andra våningen med terrass och solterrass, en med två sovrum och terrass och en med ett sovrum. Varje bostad har garageplats och förråd.')
a('The shared areas are a salt-water pool, landscaped areas, a gym and a multipurpose room. The developer’s listing says the works have started, and none of the documents we hold gives a delivery date.',
  'Las zonas comunes son una piscina de agua salada, zonas ajardinadas, un gimnasio y una sala polivalente. El anuncio del promotor indica que las obras han comenzado, y ninguno de los documentos que tenemos da una fecha de entrega.',
  'Les parties communes comprennent une piscine à l’eau salée, des espaces paysagers, une salle de sport et une salle polyvalente. L’annonce du promoteur indique que les travaux ont commencé, et aucun des documents dont nous disposons ne donne de date de livraison.',
  'Die Gemeinschaftsbereiche sind ein Salzwasserpool, begrünte Flächen, ein Fitnessraum und ein Mehrzweckraum. Laut Angabe des Bauträgers haben die Bauarbeiten begonnen, und keines der uns vorliegenden Dokumente nennt einen Übergabetermin.',
  'В общих зонах есть бассейн с солёной водой, озеленённые территории, тренажёрный зал и многофункциональное помещение. В объявлении застройщика сказано, что строительство начато, а ни в одном из имеющихся у нас документов срок сдачи не указан.',
  'المرافق المشتركة هي مسبح بالمياه المالحة ومساحات مشجّرة وصالة رياضية وقاعة متعددة الاستخدامات. يذكر إعلان المطوّر أن الأعمال قد بدأت، ولا تذكر أي من الوثائق التي بحوزتنا موعد تسليم.',
  'De gedeelde ruimtes zijn een zoutwaterzwembad, aangelegde groene zones, een fitnessruimte en een multifunctionele ruimte. In de aankondiging van de ontwikkelaar staat dat de werken zijn gestart, en geen van de documenten die wij hebben noemt een opleveringsdatum.',
  'Części wspólne to basen ze słoną wodą, tereny zielone, siłownia i sala wielofunkcyjna. W ogłoszeniu dewelopera napisano, że prace budowlane się rozpoczęły, a żaden z posiadanych przez nas dokumentów nie podaje terminu oddania.',
  'Fellesarealene er et saltvannsbasseng, grønne områder, et treningsrom og et flerbruksrom. I utbyggerens annonse står det at byggearbeidene er startet, og ingen av dokumentene vi har oppgir en overleveringsdato.',
  'De gemensamma ytorna är en saltvattenpool, planterade ytor, ett gym och ett flexibelt rum. Exploatörens annons anger att byggarbetena har påbörjats, och inget av de dokument vi har anger ett tillträdesdatum.')
a('40 homes', '40 viviendas', '40 logements', '40 Wohnungen', '40 квартир', '40 مسكنًا', '40 woningen', '40 mieszkań', '40 boliger', '40 bostäder')
a('Terraces, gardens, solariums and a pool', 'Terrazas, jardines, solariums y una piscina', 'Terrasses, jardins, solariums et une piscine',
  'Terrassen, Gärten, Solarien und ein Pool', 'Террасы, сады, солярии и бассейн', 'التراسات والحدائق والسولاريوم ومسبح',
  'Terrassen, tuinen, solariums en een zwembad', 'Tarasy, ogrody, solaria i basen', 'Terrasser, hager, solterrasser og et basseng',
  'Terrasser, trädgårdar, solterrasser och en pool')

# ---------------------------------------------------------------- why
a('Apartments with a garage space and a storage room each, and a pool, a gym and a multipurpose room in a closed complex.',
  'Apartamentos con plaza de garaje y trastero cada uno, y con piscina, gimnasio y sala polivalente en un conjunto cerrado.',
  'Des appartements avec chacun une place de garage et une cave, et une piscine, une salle de sport et une salle polyvalente dans une résidence fermée.',
  'Wohnungen mit je einem Garagenstellplatz und einem Abstellraum sowie Pool, Fitnessraum und Mehrzweckraum in einer geschlossenen Wohnanlage.',
  'Квартиры, у каждой из которых есть место в гараже и кладовая, а в закрытом комплексе — бассейн, тренажёрный зал и многофункциональное помещение.',
  'شقق لكل منها موقف في المرآب وغرفة تخزين، مع مسبح وصالة رياضية وقاعة متعددة الاستخدامات في مجمع مغلق.',
  'Appartementen met elk een garageplaats en een berging, en een zwembad, een fitnessruimte en een multifunctionele ruimte in een besloten complex.',
  'Mieszkania, z których każde ma miejsce garażowe i komórkę lokatorską, oraz basen, siłownia i sala wielofunkcyjna w zamkniętym osiedlu.',
  'Leiligheter som hver har garasjeplass og bod, og basseng, treningsrom og flerbruksrom i et lukket boligområde.',
  'Lägenheter som var och en har garageplats och förråd, samt pool, gym och ett flexibelt rum i ett slutet bostadsområde.')
a('Buyers who want a new apartment in a residential area of Estepona, to live in or as a second home.',
  'Compradores que quieren un apartamento nuevo en una zona residencial de Estepona, para vivir o como segunda residencia.',
  'Acheteurs qui veulent un appartement neuf dans un quartier résidentiel d’Estepona, pour y vivre ou comme résidence secondaire.',
  'Käufer, die eine neue Wohnung in einem Wohngebiet von Estepona suchen, zum Selbstbewohnen oder als Zweitwohnsitz.',
  'Покупатели, которые хотят новую квартиру в жилом районе Эстепоны, для постоянного проживания или как вторую недвижимость.',
  'مشترون يريدون شقة جديدة في منطقة سكنية في إستيبونا، للسكن فيها أو كمنزل ثانٍ.',
  'Kopers die een nieuw appartement willen in een woonwijk van Estepona, om in te wonen of als tweede woning.',
  'Kupujący, którzy szukają nowego mieszkania w dzielnicy mieszkalnej Estepony, do zamieszkania lub jako drugi dom.',
  'Kjøpere som vil ha en ny leilighet i et boligområde i Estepona, til å bo i eller som feriebolig.',
  'Köpare som vill ha en ny lägenhet i ett bostadsområde i Estepona, att bo i eller som andra bostad.')
a('Gardens of 66 to 78 sqm on the two ground-floor homes, solariums of 44 to 66 sqm on four homes, and a garage space and a storage room with every home.',
  'Jardines de 66 a 78 {U} en las dos viviendas de planta baja, solariums de 44 a 66 {U} en cuatro viviendas, y plaza de garaje y trastero con cada vivienda.',
  'Des jardins de 66 à 78 {U} pour les deux logements du rez-de-chaussée, des solariums de 44 à 66 {U} pour quatre logements, et une place de garage et une cave avec chaque logement.',
  'Gärten von 66 bis 78 {U} bei den beiden Erdgeschosswohnungen, Solarien von 44 bis 66 {U} bei vier Wohnungen sowie bei jeder Wohnung ein Garagenstellplatz und ein Abstellraum.',
  'Сады от 66 до 78 {U} у двух квартир на первом этаже, солярии от 44 до 66 {U} у четырёх квартир, а к каждой квартире — место в гараже и кладовая.',
  'حدائق من 66 إلى 78 {U} في المسكنين الأرضيين، وسولاريوم من 44 إلى 66 {U} في أربعة مساكن، وموقف في المرآب وغرفة تخزين مع كل مسكن.',
  'Tuinen van 66 tot 78 {U} bij de twee woningen op de begane grond, solariums van 44 tot 66 {U} bij vier woningen, en bij elke woning een garageplaats en een berging.',
  'Ogrody od 66 do 78 {U} przy dwóch mieszkaniach na parterze, solaria od 44 do 66 {U} przy czterech mieszkaniach oraz miejsce garażowe i komórka lokatorska przy każdym mieszkaniu.',
  'Hager på 66 til 78 {U} ved de to boligene i første etasje, solterrasser på 44 til 66 {U} ved fire boliger, og garasjeplass og bod til hver bolig.',
  'Trädgårdar på 66 till 78 {U} vid de två bostäderna på bottenvåningen, solterrasser på 44 till 66 {U} vid fyra bostäder, samt garageplats och förråd till varje bostad.')
a('The old town is about 5 minutes away and the A-7 about 3 minutes, according to the developer’s dossier, in a quiet residential area next to the new sports zone.',
  'El casco antiguo está a unos 5 minutos y la A-7 a unos 3 minutos, según el dosier del promotor, en una zona residencial tranquila junto a la nueva zona deportiva.',
  'La vieille ville est à environ 5 minutes et l’A-7 à environ 3 minutes, selon le dossier du promoteur, dans un quartier résidentiel calme à côté du nouveau pôle sportif.',
  'Die Altstadt ist laut Dossier des Bauträgers etwa 5 Minuten entfernt und die A-7 etwa 3 Minuten, in einem ruhigen Wohngebiet neben der neuen Sportzone.',
  'Старый город находится примерно в 5 минутах, а трасса A-7 — примерно в 3 минутах, по данным досье застройщика, в тихом жилом районе рядом с новой спортивной зоной.',
  'تبعد البلدة القديمة نحو 5 دقائق والطريق A-7 نحو 3 دقائق، وفق ملف المطوّر، في منطقة سكنية هادئة بجوار المنطقة الرياضية الجديدة.',
  'De oude stad ligt volgens het dossier van de ontwikkelaar op ongeveer 5 minuten en de A-7 op ongeveer 3 minuten, in een rustige woonwijk naast de nieuwe sportzone.',
  'Stare miasto jest oddalone o około 5 minut, a autostrada A-7 o około 3 minuty, według dossier dewelopera, w spokojnej dzielnicy mieszkalnej obok nowej strefy sportowej.',
  'Gamlebyen ligger omtrent 5 minutter unna og A-7 omtrent 3 minutter, ifølge utbyggerens dossier, i et rolig boligområde ved siden av den nye idrettssonen.',
  'Gamla stan ligger ungefär 5 minuter bort och A-7 ungefär 3 minuter, enligt exploatörens dossier, i ett lugnt bostadsområde intill den nya idrottszonen.')
a('Why check the works', 'Por qué comprobar las obras', 'Pourquoi vérifier le chantier', 'Warum wir die Bauarbeiten prüfen',
  'Почему стоит проверить ход работ', 'لماذا نتحقق من الأعمال', 'Waarom de werken controleren', 'Dlaczego sprawdzić stan prac',
  'Hvorfor sjekke byggearbeidene', 'Varför kontrollera byggarbetena')
a('The listing says the works have started, but no document gives a delivery date, so we ask for the contractual date and the licence before any reservation.',
  'El anuncio indica que las obras han comenzado, pero ningún documento da una fecha de entrega, por lo que pedimos la fecha contractual y la licencia antes de cualquier reserva.',
  'L’annonce indique que les travaux ont commencé, mais aucun document ne donne de date de livraison ; nous demandons donc la date contractuelle et le permis avant toute réservation.',
  'Laut Angabe haben die Bauarbeiten begonnen, aber kein Dokument nennt einen Übergabetermin; wir fragen daher vor jeder Reservierung das vertragliche Datum und die Genehmigung an.',
  'В объявлении сказано, что строительство начато, но ни в одном документе нет срока сдачи, поэтому до любого бронирования мы запрашиваем договорную дату и разрешение.',
  'يذكر الإعلان أن الأعمال قد بدأت، لكن لا توجد وثيقة تذكر موعد تسليم، لذلك نطلب التاريخ التعاقدي والرخصة قبل أي حجز.',
  'In de aankondiging staat dat de werken zijn gestart, maar geen enkel document noemt een opleveringsdatum; daarom vragen wij vóór elke reservering de contractuele datum en de vergunning op.',
  'W ogłoszeniu napisano, że prace budowlane się rozpoczęły, ale żaden dokument nie podaje terminu oddania, dlatego przed każdą rezerwacją prosimy o termin umowny i pozwolenie.',
  'I annonsen står det at byggearbeidene er startet, men ingen dokumenter oppgir en overleveringsdato, så vi ber om den kontraktsfestede datoen og tillatelsen før enhver reservasjon.',
  'Annonsen anger att byggarbetena har påbörjats, men inget dokument anger ett tillträdesdatum, så vi ber om det avtalade datumet och bygglovet före varje reservation.')

# ---------------------------------------------------------------- architecture
a('Light facades, <em>wide terraces</em>', 'Fachadas claras, <em>amplias terrazas</em>', 'Façades claires, <em>larges terrasses</em>',
  'Helle Fassaden, <em>breite Terrassen</em>', 'Светлые фасады, <em>широкие террасы</em>', 'واجهات فاتحة، <em>وتراسات واسعة</em>',
  'Lichte gevels, <em>brede terrassen</em>', 'Jasne elewacje, <em>szerokie tarasy</em>', 'Lyse fasader, <em>brede terrasser</em>',
  'Ljusa fasader, <em>breda terrasser</em>')
a('The developer’s dossier describes a reformulated Mediterranean architecture with clean, modern lines, large windows and wide terraces conceived as an extension of the interior.',
  'El dosier del promotor describe una arquitectura mediterránea reformulada, de líneas modernas y depuradas, con grandes ventanales y amplias terrazas concebidas como una extensión del interior.',
  'Le dossier du promoteur décrit une architecture méditerranéenne revisitée, aux lignes modernes et épurées, avec de grandes baies vitrées et de larges terrasses conçues comme un prolongement de l’intérieur.',
  'Das Dossier des Bauträgers beschreibt eine neu interpretierte mediterrane Architektur mit klaren, modernen Linien, großen Fenstern und breiten Terrassen, die als Erweiterung des Innenraums gedacht sind.',
  'В досье застройщика описана переосмысленная средиземноморская архитектура с чистыми современными линиями, большими окнами и широкими террасами, задуманными как продолжение интерьера.',
  'يصف ملف المطوّر عمارة متوسطية مُعاد صياغتها بخطوط حديثة نقية ونوافذ كبيرة وتراسات واسعة مُصمَّمة كامتداد للمساحات الداخلية.',
  'Het dossier van de ontwikkelaar beschrijft een herziene mediterrane architectuur met zuivere, moderne lijnen, grote ramen en brede terrassen die zijn bedacht als een verlengstuk van het interieur.',
  'Dossier dewelopera opisuje na nowo ujętą architekturę śródziemnomorską o czystych, nowoczesnych liniach, z dużymi oknami i szerokimi tarasami pomyślanymi jako przedłużenie wnętrza.',
  'Utbyggerens dossier beskriver en omformulert middelhavsarkitektur med rene, moderne linjer, store vinduer og brede terrasser tenkt som en forlengelse av interiøret.',
  'Exploatörens dossier beskriver en omformulerad medelhavsarkitektur med rena, moderna linjer, stora fönster och breda terrasser tänkta som en förlängning av interiören.')
a('In the images the blocks have white walls with bands of vertical slats in a sand tone, terraces with glass balustrades and pergolas on the upper levels.',
  'En las imágenes, los bloques tienen paredes blancas con bandas de lamas verticales en tono arena, terrazas con barandillas de vidrio y pérgolas en los niveles superiores.',
  'Sur les images, les blocs ont des murs blancs avec des bandeaux de lames verticales de teinte sable, des terrasses à garde-corps en verre et des pergolas aux niveaux supérieurs.',
  'In den Bildern haben die Blöcke weiße Wände mit Bändern aus senkrechten Lamellen in Sandton, Terrassen mit Glasbrüstungen und Pergolen auf den oberen Ebenen.',
  'На изображениях корпуса имеют белые стены с поясами вертикальных реек песочного оттенка, террасы со стеклянными ограждениями и перголы на верхних уровнях.',
  'تظهر في الصور المبنيان بجدران بيضاء وأشرطة من الشرائح العمودية بلون رملي وتراسات بحواجز زجاجية وبرغولات في الطوابق العليا.',
  'Op de beelden hebben de blokken witte muren met banden van verticale latten in een zandtint, terrassen met glazen balustrades en pergola’s op de bovenste niveaus.',
  'Na wizualizacjach bloki mają białe ściany z pasami pionowych listew w piaskowym odcieniu, tarasy ze szklanymi balustradami i pergole na wyższych poziomach.',
  'På bildene har blokkene hvite vegger med bånd av vertikale lameller i en sandfarge, terrasser med glassrekkverk og pergolaer på de øvre nivåene.',
  'På bilderna har husen vita väggar med band av lodräta lameller i en sandton, terrasser med glasräcken och pergolor på de övre nivåerna.')
a('Reinforced concrete built to current regulations and the Technical Building Code, on a foundation designed from the geotechnical study.',
  'Hormigón armado conforme a la normativa vigente y al Código Técnico de la Edificación, sobre una cimentación proyectada a partir del estudio geotécnico.',
  'Béton armé conforme à la réglementation en vigueur et au Code technique du bâtiment, sur des fondations conçues d’après l’étude géotechnique.',
  'Stahlbeton nach geltenden Vorschriften und dem spanischen Bautechnikkodex, auf einem Fundament, das auf Grundlage des geotechnischen Gutachtens ausgelegt wurde.',
  'Железобетон в соответствии с действующими нормами и Техническим строительным кодексом, на фундаменте, рассчитанном по геотехническому исследованию.',
  'خرسانة مسلحة وفق الأنظمة السارية والمدونة التقنية للبناء، على أساسات مصممة بناءً على الدراسة الجيوتقنية.',
  'Gewapend beton volgens de geldende regelgeving en de Spaanse technische bouwcode, op een fundering die is ontworpen op basis van het geotechnisch onderzoek.',
  'Żelbet zgodny z obowiązującymi przepisami i hiszpańskim Kodeksem Technicznym Budownictwa, na fundamencie zaprojektowanym na podstawie badań geotechnicznych.',
  'Armert betong i samsvar med gjeldende regler og den spanske tekniske byggekoden, på et fundament utformet ut fra den geotekniske undersøkelsen.',
  'Armerad betong enligt gällande föreskrifter och den spanska tekniska byggnormen, på en grund utformad utifrån den geotekniska undersökningen.')
a('Multilayer brickwork with insulation and a self-supporting plasterboard lining, rendered and painted in smooth matt acrylic paint.',
  'Fábrica de ladrillo multicapa con aislamiento y trasdosado autoportante de yeso laminado, enfoscada y pintada con pintura acrílica lisa mate.',
  'Maçonnerie de brique multicouche avec isolation et doublage autoportant en plaques de plâtre, enduite et peinte à la peinture acrylique lisse mate.',
  'Mehrschichtiges Ziegelmauerwerk mit Dämmung und selbsttragender Gipskartonvorsatzschale, verputzt und mit glatter matter Acrylfarbe gestrichen.',
  'Многослойная кирпичная кладка с утеплителем и самонесущей облицовкой из гипсокартона, оштукатуренная и окрашенная гладкой матовой акриловой краской.',
  'بناء بالطوب متعدد الطبقات مع عزل وتبطين ذاتي الحمل من ألواح الجبس، ومكسو بالملاط ومطلي بدهان أكريليكي أملس مطفأ.',
  'Meerlaags metselwerk met isolatie en een zelfdragende gipsplaatbekleding, gepleisterd en geschilderd met gladde matte acrylverf.',
  'Wielowarstwowy mur z cegły z izolacją i samonośną okładziną z płyt gipsowo-kartonowych, otynkowany i pomalowany gładką matową farbą akrylową.',
  'Flerlags teglmurverk med isolasjon og en selvbærende gipsplatekledning, pusset og malt med glatt matt akrylmaling.',
  'Flerskiktat tegelmurverk med isolering och en självbärande gipsskiva på insidan, putsat och målat med slät matt akrylfärg.')
a('PVC frames with double glazing and an air chamber, and thermal PVC slat blinds with injected insulation.',
  'Carpintería de PVC con doble acristalamiento y cámara de aire, y persianas de lamas de PVC térmico con aislamiento inyectado.',
  'Menuiseries en PVC avec double vitrage et lame d’air, et volets à lames en PVC thermique avec isolation injectée.',
  'PVC-Rahmen mit Doppelverglasung und Luftkammer sowie Rollläden aus thermischem PVC mit eingespritzter Dämmung.',
  'Рамы из ПВХ с двойным остеклением и воздушной камерой и жалюзи из термического ПВХ с залитым утеплителем.',
  'إطارات من PVC بزجاج مزدوج وحجرة هواء، وستائر من شرائح PVC العازلة بعزل محقون.',
  'PVC-kozijnen met dubbele beglazing en een luchtkamer, en rolluiken van thermisch PVC met ingespoten isolatie.',
  'Stolarka z PVC z podwójnym szkleniem i komorą powietrzną oraz żaluzje z termicznego PVC z wtryskiwaną izolacją.',
  'PVC-rammer med dobbeltglass og luftkammer, og persienner av termisk PVC med injisert isolasjon.',
  'PVC-karmar med dubbelglas och luftspalt, och rullgardiner av termisk PVC med insprutad isolering.')
a('Inverted flat roofs, waterproofed and insulated, with gravel in the areas nobody walks on and non-slip ceramic flooring where they are walkable.',
  'Cubiertas planas invertidas, impermeabilizadas y aisladas, con grava en las zonas no transitables y solado cerámico antideslizante en las transitables.',
  'Toitures-terrasses inversées, étanchées et isolées, avec du gravier dans les zones non accessibles et un carrelage antidérapant dans les zones accessibles.',
  'Umkehrdächer als Flachdächer, abgedichtet und gedämmt, mit Kies in den nicht begehbaren Bereichen und rutschhemmendem Keramikbelag in den begehbaren.',
  'Инверсионные плоские кровли с гидроизоляцией и утеплением: гравий на неэксплуатируемых участках и нескользящая керамическая плитка на эксплуатируемых.',
  'أسقف مسطحة مقلوبة معزولة مائيًا وحراريًا، بالحصى في المناطق غير المخصصة للمشي وببلاط سيراميك مانع للانزلاق في المناطق المخصصة للمشي.',
  'Omgekeerde platte daken, waterdicht en geïsoleerd, met grind op de niet-begaanbare delen en antislip keramische vloeren op de begaanbare delen.',
  'Odwrócone dachy płaskie, hydroizolowane i ocieplone, ze żwirem w strefach niedostępnych i antypoślizgową płytką ceramiczną w strefach dostępnych.',
  'Omvendte flate tak, vanntettet og isolert, med grus i områdene der ingen går og sklisikre keramiske fliser der de er tilgjengelige.',
  'Omvända platta tak, tätade och isolerade, med grus på de ytor där ingen går och halkfria keramikplattor där de är beträdbara.')

# ---------------------------------------------------------------- quality specification
a('Source: the quality specification in the developer’s dossier, which is undated. It says that the images are an approximate representation, that the furniture shown is not included and that the project management may make changes for technical or legal reasons.',
  'Fuente: la memoria de calidades del dosier del promotor, que no lleva fecha. Indica que las imágenes son una representación aproximada, que el mobiliario mostrado no está incluido y que la dirección facultativa puede introducir cambios por razones técnicas o legales.',
  'Source : le descriptif de qualité du dossier du promoteur, qui n’est pas daté. Il précise que les images sont une représentation approximative, que le mobilier présenté n’est pas inclus et que la direction de projet peut apporter des modifications pour des raisons techniques ou légales.',
  'Quelle: die Baubeschreibung im Dossier des Bauträgers, die kein Datum trägt. Sie weist darauf hin, dass die Bilder eine ungefähre Darstellung sind, dass die gezeigten Möbel nicht enthalten sind und dass die Bauleitung aus technischen oder rechtlichen Gründen Änderungen vornehmen kann.',
  'Источник: спецификация качества в досье застройщика, которая не датирована. В ней сказано, что изображения дают приблизительное представление, что показанная мебель не входит в стоимость и что руководство проекта может вносить изменения по техническим или юридическим причинам.',
  'المصدر: مواصفات الجودة في ملف المطوّر، وهي غير مؤرخة. وتذكر أن الصور تمثيل تقريبي، وأن الأثاث الظاهر غير مشمول، وأن إدارة المشروع قد تُجري تغييرات لأسباب تقنية أو قانونية.',
  'Bron: de kwaliteitsspecificatie in het dossier van de ontwikkelaar, die niet is gedateerd. Daarin staat dat de beelden een benaderende weergave zijn, dat de getoonde meubels niet zijn inbegrepen en dat de bouwleiding om technische of juridische redenen wijzigingen kan aanbrengen.',
  'Źródło: specyfikacja jakości w dossier dewelopera, która nie jest datowana. Podano w niej, że wizualizacje są przybliżonym odwzorowaniem, że pokazane meble nie są wliczone w cenę, a kierownictwo projektu może wprowadzać zmiany z powodów technicznych lub prawnych.',
  'Kilde: kvalitetsspesifikasjonen i utbyggerens dossier, som ikke er datert. Den sier at bildene er en omtrentlig gjengivelse, at møblene som vises ikke er inkludert, og at prosjektledelsen kan gjøre endringer av tekniske eller juridiske grunner.',
  'Källa: kvalitetsbeskrivningen i exploatörens dossier, som inte är daterad. Den anger att bilderna är en ungefärlig återgivning, att de möbler som visas inte ingår och att projektledningen kan göra ändringar av tekniska eller juridiska skäl.')
a('Walls and partitions', 'Paredes y tabiques', 'Murs et cloisons', 'Wände und Trennwände', 'Стены и перегородки', 'الجدران والفواصل',
  'Wanden en scheidingswanden', 'Ściany i przegrody', 'Vegger og skillevegger', 'Väggar och mellanväggar')
a('Partitions inside the home in dry plasterboard on metal profiles with rock-wool insulation, and between homes and common areas in perforated solid brick lined with plasterboard and rock wool, with water-repellent plasterboard in the wet rooms.',
  'Tabiquería interior de la vivienda en yeso laminado en seco sobre perfilería metálica con aislamiento de lana de roca, y entre viviendas y zonas comunes en ladrillo macizo perforado trasdosado con yeso laminado y lana de roca, con yeso laminado hidrófugo en las zonas húmedas.',
  'Cloisons intérieures du logement en plaques de plâtre sur ossature métallique avec isolation en laine de roche, et entre logements et parties communes en brique pleine perforée doublée de plaques de plâtre et de laine de roche, avec des plaques de plâtre hydrofuges dans les pièces humides.',
  'Trennwände innerhalb der Wohnung in Trockenbau mit Gipskarton auf Metallprofilen und Steinwolldämmung, zwischen Wohnungen und Gemeinschaftsflächen aus gelochtem Vollziegel mit Gipskarton- und Steinwollvorsatzschale, in den Feuchträumen mit wasserabweisendem Gipskarton.',
  'Внутренние перегородки в квартире — сухой гипсокартон на металлическом каркасе с утеплителем из минеральной ваты, между квартирами и общими зонами — перфорированный полнотелый кирпич с облицовкой из гипсокартона и минеральной ваты, во влажных помещениях — влагостойкий гипсокартон.',
  'فواصل داخلية في المسكن من ألواح الجبس الجافة على هياكل معدنية مع عزل بالصوف الصخري، وبين المساكن والمناطق المشتركة من الطوب الكامل المثقب المبطَّن بألواح الجبس والصوف الصخري، مع ألواح جبس مقاومة للرطوبة في الغرف الرطبة.',
  'Binnenwanden in de woning van droogbouw met gipsplaten op metalen profielen met steenwolisolatie, tussen woningen en gemeenschappelijke ruimtes van geperforeerde volle baksteen met een bekleding van gipsplaten en steenwol, met waterafstotende gipsplaten in de natte ruimtes.',
  'Przegrody wewnątrz mieszkania wykonane w technologii suchej zabudowy z płyt gipsowo-kartonowych na profilach metalowych z izolacją z wełny skalnej, a między mieszkaniami i częściami wspólnymi z perforowanej cegły pełnej z okładziną z płyt gipsowo-kartonowych i wełny skalnej, z wodoodpornymi płytami w pomieszczeniach wilgotnych.',
  'Skillevegger inne i boligen i tørrbygg med gipsplater på metallprofiler med steinullisolasjon, og mellom boliger og fellesarealer i perforert massiv tegl med kledning av gipsplater og steinull, med fuktbestandige gipsplater i våtrommene.',
  'Mellanväggar inne i bostaden i torrbyggnad med gipsskivor på metallprofiler med stenullsisolering, och mellan bostäder och gemensamma ytor i perforerad massiv tegel med foder av gipsskivor och stenull, med fuktbeständiga gipsskivor i de våta rummen.')
a('Plasterboard false ceilings on suspended galvanised steel profiles with rock-wool insulation.',
  'Falsos techos de yeso laminado sobre perfilería de acero galvanizado suspendida, con aislamiento de lana de roca.',
  'Faux plafonds en plaques de plâtre sur ossature en acier galvanisé suspendue, avec isolation en laine de roche.',
  'Abgehängte Decken aus Gipskarton auf abgehängten verzinkten Stahlprofilen mit Steinwolldämmung.',
  'Подвесные потолки из гипсокартона на подвесном каркасе из оцинкованной стали с утеплителем из минеральной ваты.',
  'أسقف معلّقة من ألواح الجبس على هياكل فولاذية مجلفنة معلّقة مع عزل بالصوف الصخري.',
  'Verlaagde plafonds van gipsplaten op opgehangen verzinkte stalen profielen met steenwolisolatie.',
  'Sufity podwieszane z płyt gipsowo-kartonowych na podwieszanych profilach z ocynkowanej stali z izolacją z wełny skalnej.',
  'Nedforede himlinger i gipsplater på opphengte galvaniserte stålprofiler med steinullisolasjon.',
  'Undertak av gipsskivor på upphängda galvaniserade stålprofiler med stenullsisolering.')
a('Floors, doors and wardrobes', 'Suelos, puertas y armarios', 'Sols, portes et placards', 'Böden, Türen und Schränke',
  'Полы, двери и шкафы', 'الأرضيات والأبواب والخزائن', 'Vloeren, deuren en kasten', 'Podłogi, drzwi i szafy',
  'Gulv, dører og garderobeskap', 'Golv, dörrar och garderober')
a('Rectified porcelain stoneware floors with a 10 cm white skirting, and non-slip flooring on the terraces.',
  'Suelo de gres porcelánico rectificado con rodapié blanco de 10 cm, y pavimento antideslizante en las terrazas.',
  'Sols en grès cérame rectifié avec plinthe blanche de 10 cm, et revêtement antidérapant sur les terrasses.',
  'Böden aus rektifiziertem Feinsteinzeug mit 10 cm hoher weißer Sockelleiste und rutschhemmendem Belag auf den Terrassen.',
  'Полы из ректифицированного керамогранита с белым плинтусом высотой 10 см, а на террасах — нескользящее покрытие.',
  'أرضيات من البورسلان المصقول مع وزرة بيضاء بارتفاع 10 سم، وأرضية مانعة للانزلاق في التراسات.',
  'Vloeren van gerectificeerd porseleinen gres met een witte plint van 10 cm, en antislipvloeren op de terrassen.',
  'Podłogi z rektyfikowanego gresu porcelanowego z białą listwą przypodłogową o wysokości 10 cm oraz antypoślizgowa nawierzchnia na tarasach.',
  'Gulv i rektifisert porselensfliser med 10 cm hvit gulvlist, og sklisikkert gulv på terrassene.',
  'Golv av rektifierat porslinsgods med 10 cm hög vit golvlist, och halkfritt golv på terrasserna.')
a('An armoured front door with a three-point security lock and anti-pry hinges, white-lacquered interior doors, and built-in wardrobes with hinged or sliding white-lacquered doors, a suitcase shelf and a hanging rail, all with chrome fittings.',
  'Puerta de entrada blindada con cerradura de seguridad de tres puntos de anclaje y bisagras antipalanca, puertas interiores lacadas en blanco y armarios empotrados con puertas abatibles o correderas lacadas en blanco, balda maletero y barra de colgar, todo con herrajes cromados.',
  'Porte d’entrée blindée avec serrure de sécurité à trois points d’ancrage et paumelles anti-effraction, portes intérieures laquées blanc et placards intégrés avec portes battantes ou coulissantes laquées blanc, étagère à valises et barre de penderie, le tout avec une quincaillerie chromée.',
  'Gepanzerte Wohnungseingangstür mit Dreipunkt-Sicherheitsschloss und Aufbohrschutz-Bändern, weiß lackierte Innentüren sowie Einbauschränke mit weiß lackierten Dreh- oder Schiebetüren, Kofferablage und Kleiderstange, alles mit verchromten Beschlägen.',
  'Бронированная входная дверь с замком безопасности с тремя точками запирания и петлями с защитой от взлома, межкомнатные двери с белым лаковым покрытием и встроенные шкафы с распашными или раздвижными дверями с белым лаковым покрытием, полкой для чемоданов и штангой для одежды, вся фурнитура хромированная.',
  'باب دخول مصفّح بقفل أمان بثلاث نقاط تثبيت ومفصلات مضادة للكسر، وأبواب داخلية مطلية بالورنيش الأبيض، وخزائن مدمجة بأبواب مفصلية أو منزلقة مطلية بالورنيش الأبيض مع رف للحقائب وعمود تعليق، وكلها بإكسسوارات كرومية.',
  'Een gepantserde voordeur met een veiligheidsslot met drie sluitpunten en scharnieren met breekbeveiliging, wit gelakte binnendeuren en inbouwkasten met wit gelakte draai- of schuifdeuren, een koffertablet en een kledingstang, alles met verchroomd beslag.',
  'Drzwi wejściowe antywłamaniowe z zamkiem zabezpieczającym o trzech punktach ryglowania i zawiasami zabezpieczonymi przed wyważeniem, drzwi wewnętrzne lakierowane na biało oraz szafy w zabudowie z uchylnymi lub przesuwnymi drzwiami lakierowanymi na biało, z półką na walizki i drążkiem na ubrania, wszystko z chromowanym okuciem.',
  'Pansret inngangsdør med sikkerhetslås med tre låsepunkter og hengsler med brekkbeskyttelse, hvitlakkerte innvendige dører og innebygde garderobeskap med hvitlakkerte hengslede eller skyvbare dører, kofferthylle og kleshengerstang, alt med forkrommede beslag.',
  'Pansrad ytterdörr med säkerhetslås med tre låspunkter och gångjärn med påbrytningsskydd, vitlackerade innerdörrar och inbyggda garderober med vitlackerade svängda eller skjutbara dörrar, en resväskehylla och en klädstång, allt med förkromade beslag.')
a('A kitchen with large-capacity matt white base and wall units, a quartz-resin worktop, a single-bowl stainless-steel sink and a chrome single-lever tap.',
  'Cocina con muebles bajos y altos de gran capacidad en blanco mate, encimera de resina de cuarzo, fregadero de un seno en acero inoxidable y grifería monomando cromada.',
  'Cuisine avec meubles bas et hauts de grande capacité blanc mat, plan de travail en résine de quartz, évier à un bac en acier inoxydable et mitigeur chromé.',
  'Küche mit geräumigen matt weißen Unter- und Oberschränken, Arbeitsplatte aus Quarzharz, Einbecken-Edelstahlspüle und verchromter Einhebelarmatur.',
  'Кухня с вместительными матовыми белыми нижними и верхними шкафами, столешницей из кварцевой смолы, одночашевой мойкой из нержавеющей стали и хромированным однорычажным смесителем.',
  'مطبخ بخزائن سفلية وعلوية واسعة بلون أبيض مطفأ، وسطح عمل من راتنج الكوارتز، وحوض من الفولاذ المقاوم للصدأ بحوض واحد، وصنبور كرومي أحادي المقبض.',
  'Een keuken met ruime matwitte onder- en bovenkasten, een werkblad van kwartshars, een roestvrijstalen spoelbak met één bak en een verchroomde eengreepsmengkraan.',
  'Kuchnia z pojemnymi matowymi białymi szafkami dolnymi i górnymi, blatem z żywicy kwarcowej, jednokomorowym zlewozmywakiem ze stali nierdzewnej i chromowaną baterią jednouchwytową.',
  'Kjøkken med store matthvite over- og underskap, kvartsharpiksbenkeplate, en kum i rustfritt stål og et forkrommet énhåndsbatteri.',
  'Kök med rymliga matta vita över- och underskåp, en bänkskiva av kvartsharts, en diskho i rostfritt stål med ett fack och en förkromad enhandsblandare.')
a('An induction hob, an oven and an extractor hood are included.',
  'Se incluyen una placa de inducción, un horno y una campana extractora.',
  'Une plaque à induction, un four et une hotte aspirante sont inclus.',
  'Ein Induktionskochfeld, ein Backofen und eine Dunstabzugshaube sind enthalten.',
  'В комплект входят индукционная варочная панель, духовой шкаф и вытяжка.',
  'تشمل التجهيزات موقد حث وفرنًا وشفاطًا.',
  'Een inductiekookplaat, een oven en een afzuigkap zijn inbegrepen.',
  'W cenie jest płyta indukcyjna, piekarnik i okap.',
  'Induksjonstopp, ovn og avtrekksvifte er inkludert.',
  'Induktionshäll, ugn och spisfläkt ingår.')
a('Bathrooms partly tiled in ceramic or porcelain stoneware, with chrome single-lever taps and forced extraction.',
  'Baños alicatados parcialmente con gres cerámico o porcelánico, con grifería monomando cromada y extracción forzada.',
  'Salles de bains partiellement carrelées en grès cérame ou en grès porcelainé, avec mitigeurs chromés et extraction mécanique.',
  'Bäder teilweise mit Keramik- oder Feinsteinzeugfliesen verkleidet, mit verchromten Einhebelarmaturen und mechanischer Entlüftung.',
  'Ванные комнаты частично облицованы керамической плиткой или керамогранитом, с хромированными однорычажными смесителями и принудительной вытяжкой.',
  'حمامات مكسوة جزئيًا ببلاط سيراميك أو بورسلان، مع صنابير كرومية أحادية المقبض وتهوية قسرية.',
  'Badkamers gedeeltelijk betegeld met keramiek of porseleinen gres, met verchroomde eengreepsmengkranen en mechanische afzuiging.',
  'Łazienki częściowo wyłożone płytkami ceramicznymi lub gresem porcelanowym, z chromowanymi bateriami jednouchwytowymi i wentylacją mechaniczną.',
  'Bad delvis flislagt med keramikk eller porselensfliser, med forkrommede énhåndsbatterier og mekanisk avtrekk.',
  'Badrum delvis klädda med keramik eller porslinsgods, med förkromade enhandsblandare och mekanisk ventilation.')
a('The main bathrooms have a vanity with a single basin, an anti-mist backlit mirror, a toilet and an extra-flat shower tray; the secondary bathroom has a single-basin vanity with a mirror, a toilet and a bath.',
  'Los baños principales llevan mueble con lavabo de un seno, espejo antivaho retroiluminado, inodoro y plato de ducha extraplano; el baño secundario lleva mueble de lavabo de un seno con espejo, inodoro y bañera.',
  'Les salles de bains principales ont un meuble vasque à une vasque, un miroir antibuée rétroéclairé, des WC et un receveur de douche extraplat ; la salle de bains secondaire a un meuble vasque à une vasque avec miroir, des WC et une baignoire.',
  'Die Hauptbäder haben einen Waschtisch mit einem Becken, einen beschlagfreien hinterleuchteten Spiegel, ein WC und eine extraflache Duschwanne; das zweite Bad hat einen Waschtisch mit einem Becken und Spiegel, ein WC und eine Badewanne.',
  'В основных ванных комнатах — тумба с одной раковиной, зеркало с подсветкой и защитой от запотевания, унитаз и сверхплоский душевой поддон; во второй ванной комнате — тумба с одной раковиной и зеркалом, унитаз и ванна.',
  'تضم الحمامات الرئيسية خزانة مغسلة بحوض واحد ومرآة بإضاءة خلفية مضادة للضباب ومرحاضًا وحوض دش شديد الانبساط؛ أما الحمام الثانوي فيضم خزانة مغسلة بحوض واحد مع مرآة ومرحاضًا وحوض استحمام.',
  'De hoofdbadkamers hebben een wastafelmeubel met één wastafel, een verlichte antibeslagspiegel, een toilet en een extra vlakke douchebak; de tweede badkamer heeft een wastafelmeubel met één wastafel en een spiegel, een toilet en een bad.',
  'Łazienki główne mają szafkę z jedną umywalką, podświetlane lustro niepokrywające się parą, toaletę i bardzo płaski brodzik; łazienka dodatkowa ma szafkę z jedną umywalką i lustrem, toaletę i wannę.',
  'Hovedbadene har servantskap med én servant, et baklyst speil som ikke dugger, et toalett og en ekstra flat dusjkum; det andre badet har servantskap med én servant og speil, et toalett og et badekar.',
  'Huvudbadrummen har ett tvättställsskåp med ett handfat, en bakgrundsbelyst antidimspegel, en toalett och en extra låg duschbrunn; det andra badrummet har ett tvättställsskåp med ett handfat och en spegel, en toalett och ett badkar.')
a('Hot water from an individual aerothermal system, and individual hot-and-cold air conditioning by direct expansion, through ducts hidden in the false ceiling with grilles in the living room, bedrooms and kitchen.',
  'Agua caliente sanitaria mediante un sistema individual de aerotermia, y aire acondicionado individual de frío y calor por expansión directa, con conductos ocultos en el falso techo y rejillas en el salón, los dormitorios y la cocina.',
  'Eau chaude sanitaire par un système aérothermique individuel, et climatisation individuelle chaud-froid à détente directe, par des gaines cachées dans le faux plafond avec des grilles dans le séjour, les chambres et la cuisine.',
  'Warmwasser über ein individuelles Luft-Wasser-Wärmepumpensystem und individuelle Klimatisierung (Heizen und Kühlen) mit Direktverdampfung, über im Deckenhohlraum verborgene Kanäle mit Auslässen in Wohnzimmer, Schlafzimmern und Küche.',
  'Горячая вода от индивидуальной аэротермической системы и индивидуальное кондиционирование на тепло и холод с прямым расширением, через скрытые в подвесном потолке воздуховоды с решётками в гостиной, спальнях и кухне.',
  'الماء الساخن من نظام حراري هوائي فردي، وتكييف فردي للتبريد والتدفئة بالتمدد المباشر، عبر مجارٍ مخفية في السقف المعلّق مع فتحات في غرفة المعيشة وغرف النوم والمطبخ.',
  'Warm water via een individueel aerothermisch systeem en individuele airconditioning voor koelen en verwarmen met directe expansie, via kanalen verborgen in het verlaagde plafond met roosters in de woonkamer, de slaapkamers en de keuken.',
  'Ciepła woda z indywidualnego systemu aerotermicznego oraz indywidualna klimatyzacja chłodząco-grzewcza z bezpośrednim odparowaniem, z kanałami ukrytymi w suficie podwieszanym i kratkami w salonie, sypialniach i kuchni.',
  'Varmtvann fra et individuelt aerotermisk system og individuell klimaanlegg for kjøling og oppvarming med direkte ekspansjon, gjennom kanaler skjult i den nedforede himlingen med ventiler i stuen, soverommene og kjøkkenet.',
  'Varmvatten från ett individuellt aerotermiskt system och individuell luftkonditionering för värme och kyla med direktexpansion, genom kanaler dolda i undertaket med don i vardagsrummet, sovrummen och köket.')
a('A digital thermostat in the living room.', 'Un termostato digital en el salón.', 'Un thermostat numérique dans le séjour.',
  'Ein digitaler Thermostat im Wohnzimmer.', 'Цифровой термостат в гостиной.', 'ترموستات رقمي في غرفة المعيشة.',
  'Een digitale thermostaat in de woonkamer.', 'Cyfrowy termostat w salonie.', 'En digital termostat i stuen.', 'En digital termostat i vardagsrummet.')
a('LED spotlights in the bathrooms and kitchen, a power point, a TV point and LED lighting on the terraces, a water point on each terrace, and a colour video intercom.',
  'Focos LED en los baños y la cocina, toma de corriente, toma de TV e iluminación LED en las terrazas, toma de agua en cada terraza y videoportero automático a color.',
  'Spots LED dans les salles de bains et la cuisine, prise électrique, prise TV et éclairage LED sur les terrasses, point d’eau sur chaque terrasse et visiophone couleur.',
  'LED-Spots in den Bädern und in der Küche, Steckdose, TV-Anschluss und LED-Beleuchtung auf den Terrassen, ein Wasseranschluss auf jeder Terrasse und eine Farb-Videosprechanlage.',
  'Светодиодные светильники в ванных комнатах и на кухне, розетка, ТВ-розетка и светодиодное освещение на террасах, водопроводный кран на каждой террасе и цветной видеодомофон.',
  'كشافات LED في الحمامات والمطبخ، ومخرج كهرباء ومخرج تلفاز وإضاءة LED في التراسات، ونقطة مياه في كل تراس، وجهاز اتصال مرئي ملوّن.',
  'Led-spots in de badkamers en de keuken, een stopcontact, een tv-aansluiting en led-verlichting op de terrassen, een waterpunt op elk terras en een kleurenvideofoon.',
  'Oprawy LED w łazienkach i kuchni, gniazdo elektryczne, gniazdo TV i oświetlenie LED na tarasach, punkt poboru wody na każdym tarasie oraz kolorowy wideodomofon.',
  'LED-spotter på badene og kjøkkenet, strømuttak, TV-uttak og LED-belysning på terrassene, et vannuttak på hver terrasse og en fargevideoporttelefon.',
  'LED-spotlights i badrummen och köket, ett eluttag, ett tv-uttag och LED-belysning på terrasserna, ett vattenuttag på varje terrass och en färgvideotelefon.')
a('A digital network of integrated services with outlets in the living rooms, kitchens and bedrooms.',
  'Una red digital de servicios integrados con tomas en los salones, las cocinas y los dormitorios.',
  'Un réseau numérique de services intégrés avec des prises dans les séjours, les cuisines et les chambres.',
  'Ein digitales Netz integrierter Dienste mit Anschlüssen in Wohnzimmern, Küchen und Schlafzimmern.',
  'Цифровая сеть интегрированных услуг с розетками в гостиных, кухнях и спальнях.',
  'شبكة رقمية للخدمات المتكاملة مع مخارج في غرف المعيشة والمطابخ وغرف النوم.',
  'Een digitaal netwerk van geïntegreerde diensten met aansluitingen in de woonkamers, de keukens en de slaapkamers.',
  'Cyfrowa sieć usług zintegrowanych z gniazdami w salonach, kuchniach i sypialniach.',
  'Et digitalt nett av integrerte tjenester med uttak i stuene, kjøkkenene og soverommene.',
  'Ett digitalt nät av integrerade tjänster med uttag i vardagsrummen, köken och sovrummen.')
a('A garage with a remote-controlled door, a polished quartz-concrete floor, fire protection to the regulations and pre-installation for electric-car charging at the parking spaces.',
  'Garaje con puerta mecanizada con mando a distancia, pavimento de hormigón pulido al cuarzo, protección contra incendios según la normativa y preinstalación de carga para vehículos eléctricos en las plazas.',
  'Garage avec porte motorisée à télécommande, sol en béton poli au quartz, protection incendie conforme à la réglementation et pré-équipement pour la recharge de véhicules électriques aux places de stationnement.',
  'Garage mit ferngesteuertem Tor, poliertem Quarzbetonboden, Brandschutz nach den Vorschriften und Vorinstallation für das Laden von Elektrofahrzeugen an den Stellplätzen.',
  'Гараж с автоматическими воротами с дистанционным управлением, полом из бетона с кварцевой полировкой, противопожарной защитой по нормам и подготовкой к зарядке электромобилей на парковочных местах.',
  'مرآب بباب آلي يعمل بجهاز تحكم عن بُعد، وأرضية من الخرسانة المصقولة بالكوارتز، وحماية من الحريق وفق الأنظمة، وتجهيز مسبق لشحن السيارات الكهربائية في مواقف السيارات.',
  'Een garage met een afstandsbediende poort, een gepolijste kwartsbetonvloer, brandbeveiliging volgens de voorschriften en voorbereiding voor het opladen van elektrische auto’s bij de parkeerplaatsen.',
  'Garaż z bramą sterowaną pilotem, posadzką z betonu polerowanego kwarcem, ochroną przeciwpożarową zgodną z przepisami i przygotowaniem do ładowania pojazdów elektrycznych na miejscach parkingowych.',
  'Garasje med fjernstyrt port, polert kvartsbetonggulv, brannsikring i henhold til forskriftene og forberedelse for lading av elbil på parkeringsplassene.',
  'Garage med fjärrstyrd port, polerat kvartsbetonggolv, brandskydd enligt föreskrifterna och förberedelse för laddning av elbil vid parkeringsplatserna.')
a('Lifts that reach every floor and the garage floors directly, with automatic doors, overload detection, a telephone connection and room for 8 people.',
  'Ascensores con acceso desde todas las plantas y comunicados directamente con las plantas de garaje, con puertas automáticas, detección de sobrecarga, conexión telefónica y capacidad para 8 personas.',
  'Ascenseurs desservant tous les étages et reliés directement aux niveaux du garage, avec portes automatiques, détection de surcharge, liaison téléphonique et capacité de 8 personnes.',
  'Aufzüge, die alle Etagen und direkt die Garagengeschosse erreichen, mit automatischen Türen, Überlasterkennung, Telefonverbindung und Platz für 8 Personen.',
  'Лифты, обслуживающие все этажи и напрямую связанные с этажами гаража, с автоматическими дверями, датчиком перегрузки, телефонной связью и вместимостью 8 человек.',
  'مصاعد تصل إلى جميع الطوابق وإلى طوابق المرآب مباشرةً، بأبواب آلية وكشف للحمولة الزائدة واتصال هاتفي وسعة 8 أشخاص.',
  'Liften die alle verdiepingen en rechtstreeks de garageverdiepingen bereiken, met automatische deuren, overbelastingsdetectie, een telefoonverbinding en plaats voor 8 personen.',
  'Windy docierające na wszystkie piętra i bezpośrednio na poziomy garażowe, z automatycznymi drzwiami, wykrywaniem przeciążenia, łącznością telefoniczną i pojemnością 8 osób.',
  'Heiser som går til alle etasjer og direkte til garasjeetasjene, med automatiske dører, overlastdeteksjon, telefonforbindelse og plass til 8 personer.',
  'Hissar som når alla våningar och garageplanen direkt, med automatiska dörrar, överlastdetektering, telefonförbindelse och plats för 8 personer.')
a('A salt-chlorinated pool lined with gresite tiles and a solarium area, a multipurpose room and a gym area.',
  'Una piscina de cloración salina revestida de gresite con una zona de solárium, una sala polivalente y una zona de gimnasio.',
  'Une piscine à électrolyse au sel revêtue de gresite avec un espace solarium, une salle polyvalente et un espace salle de sport.',
  'Ein Pool mit Salzwasserchlorierung, mit Glasmosaik ausgekleidet, mit Solarium-Bereich, ein Mehrzweckraum und ein Fitnessbereich.',
  'Бассейн с хлорированием солью, облицованный мозаикой гресите, с зоной солярия, многофункциональное помещение и зона тренажёрного зала.',
  'مسبح بالكلورة الملحية مكسو ببلاط الغريسيت مع منطقة سولاريوم، وقاعة متعددة الاستخدامات ومنطقة للصالة الرياضية.',
  'Een zwembad met zoutchlorering, bekleed met gresite, met een solariumzone, een multifunctionele ruimte en een fitnessgedeelte.',
  'Basen z chlorowaniem solnym wyłożony mozaiką gresite ze strefą solarium, sala wielofunkcyjna i strefa siłowni.',
  'Et basseng med saltklorering kledd med gresite og en solterrasseområde, et flerbruksrom og et treningsområde.',
  'En pool med saltklorering klädd med gresite och en solterrassyta, ett flexibelt rum och en gymyta.')
a('Entrance halls lit by LED, presence detectors with timers on the lighting of entrances, stairs and landings, and landscaping of native, low-water planting with automatic drip irrigation.',
  'Portales iluminados con LED, detectores de presencia con temporizador en la iluminación de portales, escaleras y vestíbulos de planta, y zonas ajardinadas con vegetación autóctona de bajo consumo hídrico y riego por goteo automático.',
  'Halls d’entrée éclairés par LED, détecteurs de présence avec minuterie sur l’éclairage des entrées, des escaliers et des paliers, et espaces paysagers plantés d’espèces locales peu gourmandes en eau avec arrosage goutte à goutte automatique.',
  'LED-beleuchtete Eingangshallen, Präsenzmelder mit Zeitschaltung für die Beleuchtung von Eingängen, Treppenhäusern und Etagenfluren sowie Begrünung mit heimischen, wassersparenden Pflanzen und automatischer Tröpfchenbewässerung.',
  'Подъезды со светодиодным освещением, датчики присутствия с таймером в освещении входов, лестниц и этажных холлов, а также озеленение местными малотребовательными к воде растениями с автоматическим капельным поливом.',
  'مداخل مضاءة بتقنية LED، وكاشفات حضور بمؤقّت في إضاءة المداخل والسلالم وردهات الطوابق، ومساحات مشجّرة بنباتات محلية قليلة استهلاك المياه مع ريّ بالتنقيط آلي.',
  'Door led verlichte ingangshallen, aanwezigheidsdetectoren met timer op de verlichting van ingangen, trappen en overlopen, en een aanplant van inheemse, waterzuinige planten met automatische druppelirrigatie.',
  'Klatki schodowe oświetlone diodami LED, czujniki obecności z wyłącznikiem czasowym w oświetleniu wejść, schodów i korytarzy na piętrach oraz nasadzenia rodzimych roślin o niskim zużyciu wody z automatycznym nawadnianiem kropelkowym.',
  'LED-belyste inngangspartier, tilstedeværelsessensorer med tidsbryter på belysningen i innganger, trapper og repos, og grøntanlegg med stedegen, vannsparende beplantning med automatisk dryppvanning.',
  'LED-belysta entréhallar, närvarosensorer med timer på belysningen i entréer, trappor och våningsplan, och planteringar med inhemska, vattensnåla växter med automatisk droppbevattning.')

# ---------------------------------------------------------------- residences
a('Eight homes, <em>four kinds</em>', 'Ocho viviendas, <em>cuatro tipos</em>', 'Huit logements, <em>quatre types</em>',
  'Acht Wohnungen, <em>vier Typen</em>', 'Восемь квартир, <em>четыре типа</em>', 'ثمانية مساكن، <em>أربعة أنواع</em>',
  'Acht woningen, <em>vier soorten</em>', 'Osiem mieszkań, <em>cztery rodzaje</em>', 'Åtte boliger, <em>fire typer</em>',
  'Åtta bostäder, <em>fyra typer</em>')
a('The eight homes fall into four groups by floor and outdoor space. The table below lists each one with its price.',
  'Las ocho viviendas se dividen en cuatro grupos según la planta y el espacio exterior. La tabla siguiente recoge cada una con su precio.',
  'Les huit logements se répartissent en quatre groupes selon l’étage et l’espace extérieur. Le tableau ci-dessous présente chacun avec son prix.',
  'Die acht Wohnungen lassen sich nach Etage und Außenbereich in vier Gruppen einteilen. Die folgende Tabelle führt jede einzelne mit ihrem Preis auf.',
  'Восемь квартир делятся на четыре группы по этажу и открытому пространству. В таблице ниже указана каждая из них с ценой.',
  'تنقسم المساكن الثمانية إلى أربع مجموعات بحسب الطابق والمساحة الخارجية. ويعرض الجدول أدناه كل مسكن مع سعره.',
  'De acht woningen vallen naar verdieping en buitenruimte uiteen in vier groepen. In de tabel hieronder staat elke woning met haar prijs.',
  'Osiem mieszkań dzieli się na cztery grupy według piętra i przestrzeni zewnętrznej. W tabeli poniżej podano każde z nich wraz z ceną.',
  'De åtte boligene deles inn i fire grupper etter etasje og utendørsareal. Tabellen nedenfor viser hver av dem med pris.',
  'De åtta bostäderna delas in i fyra grupper efter våning och uteplats. Tabellen nedan listar var och en med sitt pris.')
a('Ground-floor homes with a garden', 'Viviendas de planta baja con jardín', 'Logements de rez-de-chaussée avec jardin',
  'Erdgeschosswohnungen mit Garten', 'Квартиры на первом этаже с садом', 'مساكن الطابق الأرضي بحديقة',
  'Woningen op de begane grond met tuin', 'Mieszkania na parterze z ogrodem', 'Boliger i første etasje med hage',
  'Bostäder på bottenvåningen med trädgård')
a('Two homes at ground level with two bedrooms, two bathrooms, a covered terrace and a private garden: 1-0-A0 with a garden of 78.11 sqm and one garage space, and 3-0-C0 with a garden of 66.23 sqm and two garage spaces. Each has a storage room.',
  'Dos viviendas en planta baja con dos dormitorios, dos baños, una terraza cubierta y un jardín privado: la 1-0-A0, con un jardín de {N78.11} {U} y una plaza de garaje, y la 3-0-C0, con un jardín de {N66.23} {U} y dos plazas de garaje. Cada una tiene trastero.',
  'Deux logements au rez-de-chaussée avec deux chambres, deux salles de bains, une terrasse couverte et un jardin privatif : le 1-0-A0, avec un jardin de {N78.11} {U} et une place de garage, et le 3-0-C0, avec un jardin de {N66.23} {U} et deux places de garage. Chacun dispose d’une cave.',
  'Zwei Erdgeschosswohnungen mit zwei Schlafzimmern, zwei Bädern, einer überdachten Terrasse und einem privaten Garten: 1-0-A0 mit einem Garten von {N78.11} {U} und einem Garagenstellplatz sowie 3-0-C0 mit einem Garten von {N66.23} {U} und zwei Garagenstellplätzen. Jede hat einen Abstellraum.',
  'Две квартиры на первом этаже с двумя спальнями, двумя ванными комнатами, крытой террасой и частным садом: 1-0-A0 с садом {N78.11} {U} и одним местом в гараже и 3-0-C0 с садом {N66.23} {U} и двумя местами в гараже. У каждой есть кладовая.',
  'مسكنان في الطابق الأرضي بغرفتي نوم وحمامين وتراس مغطى وحديقة خاصة: المسكن 1-0-A0 بحديقة مساحتها {N78.11} {U} وموقف واحد في المرآب، والمسكن 3-0-C0 بحديقة مساحتها {N66.23} {U} وموقفين في المرآب. ولكل منهما غرفة تخزين.',
  'Twee woningen op de begane grond met twee slaapkamers, twee badkamers, een overdekt terras en een privétuin: 1-0-A0 met een tuin van {N78.11} {U} en één garageplaats, en 3-0-C0 met een tuin van {N66.23} {U} en twee garageplaatsen. Elke woning heeft een berging.',
  'Dwa mieszkania na parterze z dwiema sypialniami, dwiema łazienkami, tarasem zadaszonym i prywatnym ogrodem: 1-0-A0 z ogrodem o powierzchni {N78.11} {U} i jednym miejscem garażowym oraz 3-0-C0 z ogrodem o powierzchni {N66.23} {U} i dwoma miejscami garażowymi. Każde ma komórkę lokatorską.',
  'To boliger i første etasje med to soverom, to bad, en overdekket terrasse og en privat hage: 1-0-A0 med en hage på {N78.11} {U} og én garasjeplass, og 3-0-C0 med en hage på {N66.23} {U} og to garasjeplasser. Hver har en bod.',
  'Två bostäder på bottenvåningen med två sovrum, två badrum, en övertäckt terrass och en privat trädgård: 1-0-A0 med en trädgård på {N78.11} {U} och en garageplats, och 3-0-C0 med en trädgård på {N66.23} {U} och två garageplatser. Var och en har ett förråd.')
a('Covered terraces of 20.04 and 23.99 sqm and uncovered terraces of 9.39 and 3.17 sqm.',
  'Terrazas cubiertas de {N20.04} y {N23.99} {U} y terrazas descubiertas de {N9.39} y {N3.17} {U}.',
  'Terrasses couvertes de {N20.04} et {N23.99} {U} et terrasses découvertes de {N9.39} et {N3.17} {U}.',
  'Überdachte Terrassen von {N20.04} und {N23.99} {U} und unüberdachte Terrassen von {N9.39} und {N3.17} {U}.',
  'Крытые террасы {N20.04} и {N23.99} {U} и открытые террасы {N9.39} и {N3.17} {U}.',
  'تراسات مغطاة بمساحة {N20.04} و{N23.99} {U} وتراسات مكشوفة بمساحة {N9.39} و{N3.17} {U}.',
  'Overdekte terrassen van {N20.04} en {N23.99} {U} en open terrassen van {N9.39} en {N3.17} {U}.',
  'Tarasy zadaszone o powierzchni {N20.04} i {N23.99} {U} oraz tarasy niezadaszone o powierzchni {N9.39} i {N3.17} {U}.',
  'Overdekkede terrasser på {N20.04} og {N23.99} {U} og åpne terrasser på {N9.39} og {N3.17} {U}.',
  'Övertäckta terrasser på {N20.04} och {N23.99} {U} och öppna terrasser på {N9.39} och {N3.17} {U}.')
a('The prices are EUR 389,000 and EUR 499,000.', 'Los precios son {E389000} y {E499000}.', 'Les prix sont de {E389000} et {E499000}.',
  'Die Preise betragen {E389000} und {E499000}.', 'Цены — {E389000} и {E499000}.', 'السعران هما {E389000} و{E499000}.',
  'De prijzen zijn {E389000} en {E499000}.', 'Ceny wynoszą {E389000} i {E499000}.', 'Prisene er {E389000} og {E499000}.',
  'Priserna är {E389000} och {E499000}.')
a('The plans give interior areas of 67.16 and 70.92 sqm against 67.22 and 71.11 sqm on the price list, and a garden of 66.16 sqm against 66.23 sqm for 3-0-C0.',
  'Los planos dan superficies interiores de {N67.16} y {N70.92} {U}, frente a {N67.22} y {N71.11} {U} en la lista de precios, y un jardín de {N66.16} {U} frente a {N66.23} {U} en la 3-0-C0.',
  'Les plans donnent des surfaces intérieures de {N67.16} et {N70.92} {U}, contre {N67.22} et {N71.11} {U} sur la liste de prix, et un jardin de {N66.16} {U} contre {N66.23} {U} pour le 3-0-C0.',
  'Die Pläne geben Innenflächen von {N67.16} und {N70.92} {U} an, die Preisliste {N67.22} und {N71.11} {U}, und für 3-0-C0 einen Garten von {N66.16} {U} gegenüber {N66.23} {U}.',
  'По планам внутренняя площадь составляет {N67.16} и {N70.92} {U}, а по прайс-листу — {N67.22} и {N71.11} {U}; сад у 3-0-C0 по плану {N66.16} {U}, по прайс-листу {N66.23} {U}.',
  'تعطي المخططات مساحات داخلية قدرها {N67.16} و{N70.92} {U} مقابل {N67.22} و{N71.11} {U} في قائمة الأسعار، وحديقة مساحتها {N66.16} {U} مقابل {N66.23} {U} للمسكن 3-0-C0.',
  'De plattegronden geven binnenoppervlakten van {N67.16} en {N70.92} {U}, tegen {N67.22} en {N71.11} {U} in de prijslijst, en een tuin van {N66.16} {U} tegen {N66.23} {U} voor 3-0-C0.',
  'Rzuty podają powierzchnie wewnętrzne {N67.16} i {N70.92} {U}, a cennik {N67.22} i {N71.11} {U}, oraz ogród o powierzchni {N66.16} {U} wobec {N66.23} {U} w cenniku dla 3-0-C0.',
  'Plantegningene oppgir innvendige arealer på {N67.16} og {N70.92} {U}, mot {N67.22} og {N71.11} {U} i prislisten, og en hage på {N66.16} {U} mot {N66.23} {U} for 3-0-C0.',
  'Planritningarna anger invändiga ytor på {N67.16} och {N70.92} {U}, mot {N67.22} och {N71.11} {U} i prislistan, och en trädgård på {N66.16} {U} mot {N66.23} {U} för 3-0-C0.')
a('A two-bedroom home with a terrace', 'Una vivienda de dos dormitorios con terraza', 'Un logement de deux chambres avec terrasse',
  'Eine Wohnung mit zwei Schlafzimmern und Terrasse', 'Квартира с двумя спальнями и террасой', 'مسكن بغرفتي نوم وتراس',
  'Een woning met twee slaapkamers en een terras', 'Mieszkanie z dwiema sypialniami i tarasem', 'En bolig med to soverom og terrasse',
  'En bostad med två sovrum och terrass')
a('Home 1-2-B2 is on the second floor, with two bedrooms, two bathrooms and an uncovered terrace of 22.38 sqm.',
  'La vivienda 1-2-B2 está en la segunda planta, con dos dormitorios, dos baños y una terraza descubierta de {N22.38} {U}.',
  'Le logement 1-2-B2 est au deuxième étage, avec deux chambres, deux salles de bains et une terrasse découverte de {N22.38} {U}.',
  'Die Wohnung 1-2-B2 liegt im zweiten Obergeschoss, mit zwei Schlafzimmern, zwei Bädern und einer unüberdachten Terrasse von {N22.38} {U}.',
  'Квартира 1-2-B2 расположена на третьем этаже, с двумя спальнями, двумя ванными комнатами и открытой террасой {N22.38} {U}.',
  'يقع المسكن 1-2-B2 في الطابق الثاني، وفيه غرفتا نوم وحمامان وتراس مكشوف مساحته {N22.38} {U}.',
  'Woning 1-2-B2 ligt op de tweede verdieping, met twee slaapkamers, twee badkamers en een open terras van {N22.38} {U}.',
  'Mieszkanie 1-2-B2 znajduje się na drugim piętrze, ma dwie sypialnie, dwie łazienki i taras niezadaszony o powierzchni {N22.38} {U}.',
  'Bolig 1-2-B2 ligger i tredje etasje, med to soverom, to bad og en åpen terrasse på {N22.38} {U}.',
  'Bostad 1-2-B2 ligger på andra våningen, med två sovrum, två badrum och en öppen terrass på {N22.38} {U}.')
a('It comes with one garage space and a storage room, at EUR 524,000.',
  'Incluye una plaza de garaje y un trastero, por {E524000}.', 'Elle comprend une place de garage et une cave, pour {E524000}.',
  'Sie umfasst einen Garagenstellplatz und einen Abstellraum und kostet {E524000}.', 'В цену входят одно место в гараже и кладовая, стоимость — {E524000}.',
  'يشمل موقفًا واحدًا في المرآب وغرفة تخزين، بسعر {E524000}.', 'Er hoort een garageplaats en een berging bij, voor {E524000}.',
  'W cenie jest jedno miejsce garażowe i komórka lokatorska; cena wynosi {E524000}.', 'Den har én garasjeplass og en bod, til {E524000}.',
  'Den har en garageplats och ett förråd, för {E524000}.')
a('The plan gives 72.80 sqm interior against 73.00 sqm on the price list, and a terrace of 23.62 sqm against 22.38 sqm.',
  'El plano da {N72.80} {U} interiores, frente a {N73.00} {U} en la lista de precios, y una terraza de {N23.62} {U} frente a {N22.38} {U}.',
  'Le plan donne {N72.80} {U} d’intérieur, contre {N73.00} {U} sur la liste de prix, et une terrasse de {N23.62} {U} contre {N22.38} {U}.',
  'Der Plan gibt {N72.80} {U} Innenfläche an, die Preisliste {N73.00} {U}, und eine Terrasse von {N23.62} {U} gegenüber {N22.38} {U}.',
  'По плану внутренняя площадь составляет {N72.80} {U}, по прайс-листу — {N73.00} {U}; терраса по плану {N23.62} {U}, по прайс-листу {N22.38} {U}.',
  'يعطي المخطط {N72.80} {U} مساحة داخلية مقابل {N73.00} {U} في قائمة الأسعار، وتراسًا مساحته {N23.62} {U} مقابل {N22.38} {U}.',
  'De plattegrond geeft {N72.80} {U} binnenoppervlak, tegen {N73.00} {U} in de prijslijst, en een terras van {N23.62} {U} tegen {N22.38} {U}.',
  'Rzut podaje {N72.80} {U} powierzchni wewnętrznej, a cennik {N73.00} {U}, oraz taras o powierzchni {N23.62} {U} wobec {N22.38} {U}.',
  'Plantegningen oppgir {N72.80} {U} innvendig areal, mot {N73.00} {U} i prislisten, og en terrasse på {N23.62} {U} mot {N22.38} {U}.',
  'Planritningen anger {N72.80} {U} invändig yta, mot {N73.00} {U} i prislistan, och en terrass på {N23.62} {U} mot {N22.38} {U}.')
a('Second-floor homes with a solarium', 'Viviendas de la segunda planta con solárium', 'Logements au deuxième étage avec solarium',
  'Wohnungen im zweiten Obergeschoss mit Solarium', 'Квартиры на третьем этаже с солярием', 'مساكن الطابق الثاني بسولاريوم',
  'Woningen op de tweede verdieping met solarium', 'Mieszkania na drugim piętrze z solarium', 'Boliger i tredje etasje med solterrasse',
  'Bostäder på andra våningen med solterrass')
a('Four homes on the second floor, each with an uncovered terrace and a solarium: 1-2-D2, 3-2-A2 and 3-2-C2 with two bedrooms and two bathrooms, and 3-2-D2 with three bedrooms and two bathrooms.',
  'Cuatro viviendas en la segunda planta, cada una con una terraza descubierta y un solárium: la 1-2-D2, la 3-2-A2 y la 3-2-C2, de dos dormitorios y dos baños, y la 3-2-D2, de tres dormitorios y dos baños.',
  'Quatre logements au deuxième étage, chacun avec une terrasse découverte et un solarium : les 1-2-D2, 3-2-A2 et 3-2-C2, de deux chambres et deux salles de bains, et le 3-2-D2, de trois chambres et deux salles de bains.',
  'Vier Wohnungen im zweiten Obergeschoss, jeweils mit einer unüberdachten Terrasse und einem Solarium: 1-2-D2, 3-2-A2 und 3-2-C2 mit zwei Schlafzimmern und zwei Bädern sowie 3-2-D2 mit drei Schlafzimmern und zwei Bädern.',
  'Четыре квартиры на третьем этаже, у каждой есть открытая терраса и солярий: 1-2-D2, 3-2-A2 и 3-2-C2 с двумя спальнями и двумя ванными комнатами и 3-2-D2 с тремя спальнями и двумя ванными комнатами.',
  'أربعة مساكن في الطابق الثاني، لكل منها تراس مكشوف وسولاريوم: المساكن 1-2-D2 و3-2-A2 و3-2-C2 بغرفتي نوم وحمامين، والمسكن 3-2-D2 بثلاث غرف نوم وحمامين.',
  'Vier woningen op de tweede verdieping, elk met een open terras en een solarium: 1-2-D2, 3-2-A2 en 3-2-C2 met twee slaapkamers en twee badkamers, en 3-2-D2 met drie slaapkamers en twee badkamers.',
  'Cztery mieszkania na drugim piętrze, każde z tarasem niezadaszonym i solarium: 1-2-D2, 3-2-A2 i 3-2-C2 z dwiema sypialniami i dwiema łazienkami oraz 3-2-D2 z trzema sypialniami i dwiema łazienkami.',
  'Fire boliger i tredje etasje, hver med en åpen terrasse og en solterrasse: 1-2-D2, 3-2-A2 og 3-2-C2 med to soverom og to bad, og 3-2-D2 med tre soverom og to bad.',
  'Fyra bostäder på andra våningen, var och en med en öppen terrass och en solterrass: 1-2-D2, 3-2-A2 och 3-2-C2 med två sovrum och två badrum, och 3-2-D2 med tre sovrum och två badrum.')
a('Terraces of 20.38 to 37.96 sqm and solariums of 44.06 to 65.87 sqm. Homes 3-2-A2 and 3-2-C2 have two garage spaces and 1-2-D2 and 3-2-D2 have one; each has a storage room.',
  'Terrazas de {N20.38} a {N37.96} {U} y solariums de {N44.06} a {N65.87} {U}. La 3-2-A2 y la 3-2-C2 tienen dos plazas de garaje y la 1-2-D2 y la 3-2-D2 una; cada una tiene trastero.',
  'Terrasses de {N20.38} à {N37.96} {U} et solariums de {N44.06} à {N65.87} {U}. Les 3-2-A2 et 3-2-C2 ont deux places de garage et les 1-2-D2 et 3-2-D2 une ; chacun dispose d’une cave.',
  'Terrassen von {N20.38} bis {N37.96} {U} und Solarien von {N44.06} bis {N65.87} {U}. 3-2-A2 und 3-2-C2 haben zwei Garagenstellplätze, 1-2-D2 und 3-2-D2 einen; jede hat einen Abstellraum.',
  'Террасы от {N20.38} до {N37.96} {U} и солярии от {N44.06} до {N65.87} {U}. У 3-2-A2 и 3-2-C2 по два места в гараже, у 1-2-D2 и 3-2-D2 — по одному; у каждой есть кладовая.',
  'تراسات من {N20.38} إلى {N37.96} {U} وسولاريوم من {N44.06} إلى {N65.87} {U}. للمسكنين 3-2-A2 و3-2-C2 موقفان في المرآب، وللمسكنين 1-2-D2 و3-2-D2 موقف واحد؛ ولكل منها غرفة تخزين.',
  'Terrassen van {N20.38} tot {N37.96} {U} en solariums van {N44.06} tot {N65.87} {U}. 3-2-A2 en 3-2-C2 hebben twee garageplaatsen en 1-2-D2 en 3-2-D2 één; elke woning heeft een berging.',
  'Tarasy od {N20.38} do {N37.96} {U} i solaria od {N44.06} do {N65.87} {U}. Mieszkania 3-2-A2 i 3-2-C2 mają po dwa miejsca garażowe, a 1-2-D2 i 3-2-D2 po jednym; każde ma komórkę lokatorską.',
  'Terrasser på {N20.38} til {N37.96} {U} og solterrasser på {N44.06} til {N65.87} {U}. 3-2-A2 og 3-2-C2 har to garasjeplasser, og 1-2-D2 og 3-2-D2 har én; hver har en bod.',
  'Terrasser på {N20.38} till {N37.96} {U} och solterrasser på {N44.06} till {N65.87} {U}. 3-2-A2 och 3-2-C2 har två garageplatser, och 1-2-D2 och 3-2-D2 har en; var och en har ett förråd.')
a('The prices run from EUR 550,000 to EUR 566,000.', 'Los precios van de {E550000} a {E566000}.', 'Les prix vont de {E550000} à {E566000}.',
  'Die Preise reichen von {E550000} bis {E566000}.', 'Цены — от {E550000} до {E566000}.', 'تتراوح الأسعار من {E550000} إلى {E566000}.',
  'De prijzen lopen van {E550000} tot {E566000}.', 'Ceny wahają się od {E550000} do {E566000}.', 'Prisene går fra {E550000} til {E566000}.',
  'Priserna går från {E550000} till {E566000}.')
a('The plans give interior areas of 66.61, 72.64, 65.82 and 84.75 sqm against 66.98, 72.98, 66.69 and 84.92 sqm on the price list, for 1-2-D2, 3-2-A2, 3-2-C2 and 3-2-D2 in that order.',
  'Los planos dan superficies interiores de {N66.61}, {N72.64}, {N65.82} y {N84.75} {U}, frente a {N66.98}, {N72.98}, {N66.69} y {N84.92} {U} en la lista de precios, para la 1-2-D2, la 3-2-A2, la 3-2-C2 y la 3-2-D2, por ese orden.',
  'Les plans donnent des surfaces intérieures de {N66.61}, {N72.64}, {N65.82} et {N84.75} {U}, contre {N66.98}, {N72.98}, {N66.69} et {N84.92} {U} sur la liste de prix, pour les 1-2-D2, 3-2-A2, 3-2-C2 et 3-2-D2, dans cet ordre.',
  'Die Pläne geben Innenflächen von {N66.61}, {N72.64}, {N65.82} und {N84.75} {U} an, die Preisliste {N66.98}, {N72.98}, {N66.69} und {N84.92} {U}, für 1-2-D2, 3-2-A2, 3-2-C2 und 3-2-D2 in dieser Reihenfolge.',
  'По планам внутренняя площадь составляет {N66.61}, {N72.64}, {N65.82} и {N84.75} {U}, по прайс-листу — {N66.98}, {N72.98}, {N66.69} и {N84.92} {U}, для 1-2-D2, 3-2-A2, 3-2-C2 и 3-2-D2 соответственно.',
  'تعطي المخططات مساحات داخلية قدرها {N66.61} و{N72.64} و{N65.82} و{N84.75} {U} مقابل {N66.98} و{N72.98} و{N66.69} و{N84.92} {U} في قائمة الأسعار، للمساكن 1-2-D2 و3-2-A2 و3-2-C2 و3-2-D2 بهذا الترتيب.',
  'De plattegronden geven binnenoppervlakten van {N66.61}, {N72.64}, {N65.82} en {N84.75} {U}, tegen {N66.98}, {N72.98}, {N66.69} en {N84.92} {U} in de prijslijst, voor 1-2-D2, 3-2-A2, 3-2-C2 en 3-2-D2 in die volgorde.',
  'Rzuty podają powierzchnie wewnętrzne {N66.61}, {N72.64}, {N65.82} i {N84.75} {U}, a cennik {N66.98}, {N72.98}, {N66.69} i {N84.92} {U}, odpowiednio dla 1-2-D2, 3-2-A2, 3-2-C2 i 3-2-D2.',
  'Plantegningene oppgir innvendige arealer på {N66.61}, {N72.64}, {N65.82} og {N84.75} {U}, mot {N66.98}, {N72.98}, {N66.69} og {N84.92} {U} i prislisten, for 1-2-D2, 3-2-A2, 3-2-C2 og 3-2-D2 i den rekkefølgen.',
  'Planritningarna anger invändiga ytor på {N66.61}, {N72.64}, {N65.82} och {N84.75} {U}, mot {N66.98}, {N72.98}, {N66.69} och {N84.92} {U} i prislistan, för 1-2-D2, 3-2-A2, 3-2-C2 och 3-2-D2 i den ordningen.')
a('In the same order the plans give terraces of 38.56, 35.97, 27.06 and 20.09 sqm against 37.96, 33.17, 26.22 and 20.38 sqm on the price list, and solariums of 64.32, 46.46, 66.23 and 58.33 sqm against 60.57, 44.06, 65.87 and 55.62 sqm.',
  'En el mismo orden, los planos dan terrazas de {N38.56}, {N35.97}, {N27.06} y {N20.09} {U}, frente a {N37.96}, {N33.17}, {N26.22} y {N20.38} {U} en la lista de precios, y solariums de {N64.32}, {N46.46}, {N66.23} y {N58.33} {U}, frente a {N60.57}, {N44.06}, {N65.87} y {N55.62} {U}.',
  'Dans le même ordre, les plans donnent des terrasses de {N38.56}, {N35.97}, {N27.06} et {N20.09} {U}, contre {N37.96}, {N33.17}, {N26.22} et {N20.38} {U} sur la liste de prix, et des solariums de {N64.32}, {N46.46}, {N66.23} et {N58.33} {U}, contre {N60.57}, {N44.06}, {N65.87} et {N55.62} {U}.',
  'In derselben Reihenfolge geben die Pläne Terrassen von {N38.56}, {N35.97}, {N27.06} und {N20.09} {U} an, die Preisliste {N37.96}, {N33.17}, {N26.22} und {N20.38} {U}, sowie Solarien von {N64.32}, {N46.46}, {N66.23} und {N58.33} {U} gegenüber {N60.57}, {N44.06}, {N65.87} und {N55.62} {U}.',
  'В том же порядке по планам террасы составляют {N38.56}, {N35.97}, {N27.06} и {N20.09} {U}, по прайс-листу — {N37.96}, {N33.17}, {N26.22} и {N20.38} {U}, а солярии по планам — {N64.32}, {N46.46}, {N66.23} и {N58.33} {U}, по прайс-листу — {N60.57}, {N44.06}, {N65.87} и {N55.62} {U}.',
  'وبالترتيب نفسه تعطي المخططات تراسات مساحتها {N38.56} و{N35.97} و{N27.06} و{N20.09} {U} مقابل {N37.96} و{N33.17} و{N26.22} و{N20.38} {U} في قائمة الأسعار، وسولاريوم مساحته {N64.32} و{N46.46} و{N66.23} و{N58.33} {U} مقابل {N60.57} و{N44.06} و{N65.87} و{N55.62} {U}.',
  'In dezelfde volgorde geven de plattegronden terrassen van {N38.56}, {N35.97}, {N27.06} en {N20.09} {U}, tegen {N37.96}, {N33.17}, {N26.22} en {N20.38} {U} in de prijslijst, en solariums van {N64.32}, {N46.46}, {N66.23} en {N58.33} {U}, tegen {N60.57}, {N44.06}, {N65.87} en {N55.62} {U}.',
  'W tej samej kolejności rzuty podają tarasy o powierzchni {N38.56}, {N35.97}, {N27.06} i {N20.09} {U}, a cennik {N37.96}, {N33.17}, {N26.22} i {N20.38} {U}, oraz solaria o powierzchni {N64.32}, {N46.46}, {N66.23} i {N58.33} {U} wobec {N60.57}, {N44.06}, {N65.87} i {N55.62} {U} w cenniku.',
  'I samme rekkefølge oppgir plantegningene terrasser på {N38.56}, {N35.97}, {N27.06} og {N20.09} {U}, mot {N37.96}, {N33.17}, {N26.22} og {N20.38} {U} i prislisten, og solterrasser på {N64.32}, {N46.46}, {N66.23} og {N58.33} {U}, mot {N60.57}, {N44.06}, {N65.87} og {N55.62} {U}.',
  'I samma ordning anger planritningarna terrasser på {N38.56}, {N35.97}, {N27.06} och {N20.09} {U}, mot {N37.96}, {N33.17}, {N26.22} och {N20.38} {U} i prislistan, och solterrasser på {N64.32}, {N46.46}, {N66.23} och {N58.33} {U}, mot {N60.57}, {N44.06}, {N65.87} och {N55.62} {U}.')
a('The one-bedroom home', 'La vivienda de un dormitorio', 'Le logement d’une chambre', 'Die Wohnung mit einem Schlafzimmer',
  'Квартира с одной спальней', 'المسكن بغرفة نوم واحدة', 'De woning met één slaapkamer', 'Mieszkanie z jedną sypialnią',
  'Boligen med ett soverom', 'Bostaden med ett sovrum')
a('Home 1-3-B3 is on the third floor, with one bedroom, one bathroom and an uncovered terrace of 36.15 sqm.',
  'La vivienda 1-3-B3 está en la tercera planta, con un dormitorio, un baño y una terraza descubierta de {N36.15} {U}.',
  'Le logement 1-3-B3 est au troisième étage, avec une chambre, une salle de bains et une terrasse découverte de {N36.15} {U}.',
  'Die Wohnung 1-3-B3 liegt im dritten Obergeschoss, mit einem Schlafzimmer, einem Bad und einer unüberdachten Terrasse von {N36.15} {U}.',
  'Квартира 1-3-B3 расположена на четвёртом этаже, с одной спальней, одной ванной комнатой и открытой террасой {N36.15} {U}.',
  'يقع المسكن 1-3-B3 في الطابق الثالث، وفيه غرفة نوم واحدة وحمام واحد وتراس مكشوف مساحته {N36.15} {U}.',
  'Woning 1-3-B3 ligt op de derde verdieping, met één slaapkamer, één badkamer en een open terras van {N36.15} {U}.',
  'Mieszkanie 1-3-B3 znajduje się na trzecim piętrze, ma jedną sypialnię, jedną łazienkę i taras niezadaszony o powierzchni {N36.15} {U}.',
  'Bolig 1-3-B3 ligger i fjerde etasje, med ett soverom, ett bad og en åpen terrasse på {N36.15} {U}.',
  'Bostad 1-3-B3 ligger på tredje våningen, med ett sovrum, ett badrum och en öppen terrass på {N36.15} {U}.')
a('It comes with one garage space and a storage room, at EUR 363,000.',
  'Incluye una plaza de garaje y un trastero, por {E363000}.', 'Il comprend une place de garage et une cave, pour {E363000}.',
  'Sie umfasst einen Garagenstellplatz und einen Abstellraum und kostet {E363000}.', 'В цену входят одно место в гараже и кладовая, стоимость — {E363000}.',
  'يشمل موقفًا واحدًا في المرآب وغرفة تخزين، بسعر {E363000}.', 'Er hoort een garageplaats en een berging bij, voor {E363000}.',
  'W cenie jest jedno miejsce garażowe i komórka lokatorska; cena wynosi {E363000}.', 'Den har én garasjeplass og en bod, til {E363000}.',
  'Den har en garageplats och ett förråd, för {E363000}.')
a('The plan gives 47.63 sqm interior against 47.99 sqm on the price list, and a terrace of 39.16 sqm against 36.15 sqm.',
  'El plano da {N47.63} {U} interiores, frente a {N47.99} {U} en la lista de precios, y una terraza de {N39.16} {U} frente a {N36.15} {U}.',
  'Le plan donne {N47.63} {U} d’intérieur, contre {N47.99} {U} sur la liste de prix, et une terrasse de {N39.16} {U} contre {N36.15} {U}.',
  'Der Plan gibt {N47.63} {U} Innenfläche an, die Preisliste {N47.99} {U}, und eine Terrasse von {N39.16} {U} gegenüber {N36.15} {U}.',
  'По плану внутренняя площадь составляет {N47.63} {U}, по прайс-листу — {N47.99} {U}; терраса по плану {N39.16} {U}, по прайс-листу {N36.15} {U}.',
  'يعطي المخطط {N47.63} {U} مساحة داخلية مقابل {N47.99} {U} في قائمة الأسعار، وتراسًا مساحته {N39.16} {U} مقابل {N36.15} {U}.',
  'De plattegrond geeft {N47.63} {U} binnenoppervlak, tegen {N47.99} {U} in de prijslijst, en een terras van {N39.16} {U} tegen {N36.15} {U}.',
  'Rzut podaje {N47.63} {U} powierzchni wewnętrznej, a cennik {N47.99} {U}, oraz taras o powierzchni {N39.16} {U} wobec {N36.15} {U}.',
  'Plantegningen oppgir {N47.63} {U} innvendig areal, mot {N47.99} {U} i prislisten, og en terrasse på {N39.16} {U} mot {N36.15} {U}.',
  'Planritningen anger {N47.63} {U} invändig yta, mot {N47.99} {U} i prislistan, och en terrass på {N39.16} {U} mot {N36.15} {U}.')

# ---------------------------------------------------------------- lifestyle
a('A pool, <em>a gym</em> and room to gather', 'Una piscina, <em>un gimnasio</em> y espacio para reunirse',
  'Une piscine, <em>une salle de sport</em> et de la place pour se retrouver', 'Ein Pool, <em>ein Fitnessraum</em> und Platz zum Zusammenkommen',
  'Бассейн, <em>тренажёрный зал</em> и место для встреч', 'مسبح، <em>وصالة رياضية</em> ومساحة للتجمّع',
  'Een zwembad, <em>een fitnessruimte</em> en ruimte om samen te komen', 'Basen, <em>siłownia</em> i miejsce na spotkania',
  'Et basseng, <em>et treningsrom</em> og plass til å samles', 'En pool, <em>ett gym</em> och plats att samlas')
a('The shared areas are planned around a pool, a gym and a multipurpose room, in a closed complex.',
  'Las zonas comunes se organizan en torno a una piscina, un gimnasio y una sala polivalente, en un conjunto cerrado.',
  'Les parties communes s’organisent autour d’une piscine, d’une salle de sport et d’une salle polyvalente, dans une résidence fermée.',
  'Die Gemeinschaftsbereiche sind um einen Pool, einen Fitnessraum und einen Mehrzweckraum angelegt, in einer geschlossenen Wohnanlage.',
  'Общие зоны организованы вокруг бассейна, тренажёрного зала и многофункционального помещения в закрытом комплексе.',
  'صُمّمت المرافق المشتركة حول مسبح وصالة رياضية وقاعة متعددة الاستخدامات، في مجمع مغلق.',
  'De gedeelde ruimtes zijn opgezet rond een zwembad, een fitnessruimte en een multifunctionele ruimte, in een besloten complex.',
  'Części wspólne zaplanowano wokół basenu, siłowni i sali wielofunkcyjnej, w zamkniętym osiedlu.',
  'Fellesarealene er planlagt rundt et basseng, et treningsrom og et flerbruksrom, i et lukket boligområde.',
  'De gemensamma ytorna är planerade kring en pool, ett gym och ett flexibelt rum, i ett slutet bostadsområde.')
a('A salt-chlorinated pool lined with gresite tiles, with a solarium area.',
  'Una piscina de cloración salina revestida de gresite, con una zona de solárium.',
  'Une piscine à électrolyse au sel revêtue de gresite, avec un espace solarium.',
  'Ein Pool mit Salzwasserchlorierung, mit Glasmosaik ausgekleidet, mit Solarium-Bereich.',
  'Бассейн с хлорированием солью, облицованный мозаикой гресите, с зоной солярия.',
  'مسبح بالكلورة الملحية مكسو ببلاط الغريسيت مع منطقة سولاريوم.',
  'Een zwembad met zoutchlorering, bekleed met gresite, met een solariumzone.',
  'Basen z chlorowaniem solnym wyłożony mozaiką gresite, ze strefą solarium.',
  'Et basseng med saltklorering kledd med gresite, med et solterrasseområde.',
  'En pool med saltklorering klädd med gresite, med en solterrassyta.')
a('An equipped gym for the residents.', 'Un gimnasio equipado para los residentes.', 'Une salle de sport équipée pour les résidents.',
  'Ein ausgestatteter Fitnessraum für die Bewohner.', 'Оборудованный тренажёрный зал для жителей.', 'صالة رياضية مجهّزة للسكان.',
  'Een uitgeruste fitnessruimte voor de bewoners.', 'Wyposażona siłownia dla mieszkańców.', 'Et utstyrt treningsrom for beboerne.',
  'Ett utrustat gym för de boende.')
a('The multipurpose room', 'La sala polivalente', 'La salle polyvalente', 'Der Mehrzweckraum', 'Многофункциональное помещение',
  'القاعة متعددة الاستخدامات', 'De multifunctionele ruimte', 'Sala wielofunkcyjna', 'Flerbruksrommet', 'Det flexibla rummet')
a('A room the developer describes as a space for different uses, as an extension of the home.',
  'Una sala que el promotor describe como un espacio para distintos usos, como una extensión de la vivienda.',
  'Une salle que le promoteur décrit comme un espace aux usages variés, en prolongement du logement.',
  'Ein Raum, den der Bauträger als Fläche für unterschiedliche Nutzungen beschreibt, als Erweiterung der Wohnung.',
  'Помещение, которое застройщик описывает как пространство для разных целей, как продолжение квартиры.',
  'قاعة يصفها المطوّر بأنها مساحة لاستخدامات مختلفة، كامتداد للمسكن.',
  'Een ruimte die de ontwikkelaar beschrijft als een plek voor verschillend gebruik, als een verlengstuk van de woning.',
  'Sala, którą deweloper opisuje jako przestrzeń o różnych zastosowaniach, będącą przedłużeniem mieszkania.',
  'Et rom utbyggeren beskriver som et rom til ulike bruksområder, som en forlengelse av boligen.',
  'Ett rum som exploatören beskriver som en yta för olika användningar, som en förlängning av bostaden.')
a('Green areas and privacy', 'Zonas verdes e intimidad', 'Espaces verts et intimité', 'Grünflächen und Privatsphäre',
  'Зелёные зоны и приватность', 'المساحات الخضراء والخصوصية', 'Groene zones en privacy', 'Tereny zielone i prywatność',
  'Grøntområder og privatliv', 'Grönytor och avskildhet')
a('Landscaped areas around the blocks, in a complex that the dossier presents as private and secure.',
  'Zonas ajardinadas alrededor de los bloques, en un conjunto que el dosier presenta como privado y seguro.',
  'Des espaces paysagers autour des blocs, dans une résidence que le dossier présente comme privée et sécurisée.',
  'Begrünte Flächen rund um die Blöcke, in einer Anlage, die das Dossier als privat und sicher darstellt.',
  'Озеленённые территории вокруг корпусов в комплексе, который в досье представлен как частный и безопасный.',
  'مساحات مشجّرة حول المبنيين، في مجمع يقدّمه الملف على أنه خاص وآمن.',
  'Aangelegde groene zones rond de blokken, in een complex dat het dossier presenteert als privé en veilig.',
  'Tereny zielone wokół bloków, w osiedlu, które dossier przedstawia jako prywatne i bezpieczne.',
  'Grønne områder rundt blokkene, i et boligområde som dossieret presenterer som privat og trygt.',
  'Planterade ytor runt husen, i ett område som dossiern presenterar som privat och tryggt.')

# ---------------------------------------------------------------- location
a('El Calvario, <em>in Estepona</em>', 'El Calvario, <em>en Estepona</em>', 'El Calvario, <em>à Estepona</em>', 'El Calvario, <em>in Estepona</em>',
  'Эль-Кальварио, <em>Эстепона</em>', 'إل كالفاريو، <em>في إستيبونا</em>', 'El Calvario, <em>in Estepona</em>', 'El Calvario, <em>w Esteponie</em>',
  'El Calvario, <em>i Estepona</em>', 'El Calvario, <em>i Estepona</em>')
a('The homes are in the El Calvario residential area of Estepona, a quiet and well-connected neighbourhood near the new sports zone, the old town, the coastal path and the Sierra Bermeja. The developer’s dossier gives the old town as 5 minutes away, the A-7 as 3 minutes, Puerto Banús as 20, Marbella as 30 and Málaga airport as an hour. The listing also names the hospital, the renewed port area and the schools as nearby.',
  'Las viviendas están en la zona residencial de El Calvario, en Estepona, un barrio tranquilo y bien comunicado cerca de la nueva zona deportiva, del casco antiguo, de la senda litoral y de Sierra Bermeja. El dosier del promotor sitúa el casco antiguo a 5 minutos, la A-7 a 3, Puerto Banús a 20, Marbella a 30 y el aeropuerto de Málaga a una hora. El anuncio nombra además el hospital, la zona portuaria renovada y los colegios como cercanos.',
  'Les logements se trouvent dans le quartier résidentiel d’El Calvario à Estepona, un secteur calme et bien desservi, près du nouveau pôle sportif, de la vieille ville, du sentier littoral et de la Sierra Bermeja. Le dossier du promoteur situe la vieille ville à 5 minutes, l’A-7 à 3, Puerto Banús à 20, Marbella à 30 et l’aéroport de Málaga à une heure. L’annonce cite aussi l’hôpital, la zone portuaire rénovée et les écoles comme proches.',
  'Die Wohnungen liegen im Wohngebiet El Calvario in Estepona, einem ruhigen und gut angebundenen Viertel nahe der neuen Sportzone, der Altstadt, dem Küstenweg und der Sierra Bermeja. Das Dossier des Bauträgers nennt die Altstadt in 5 Minuten, die A-7 in 3, Puerto Banús in 20, Marbella in 30 und den Flughafen Málaga in einer Stunde. Die Anzeige führt außerdem das Krankenhaus, das erneuerte Hafenviertel und die Schulen als nahe gelegen auf.',
  'Квартиры расположены в жилом районе Эль-Кальварио в Эстепоне — тихом и хорошо связанном с городом, рядом с новой спортивной зоной, старым городом, прибрежной тропой и горным хребтом Сьерра-Бермеха. По данным досье застройщика, до старого города 5 минут, до трассы A-7 — 3, до Пуэрто-Банус — 20, до Марбельи — 30, до аэропорта Малаги — час. В объявлении также указаны поблизости больница, обновлённая портовая зона и школы.',
  'تقع المساكن في المنطقة السكنية إل كالفاريو في إستيبونا، وهي حي هادئ وجيد الاتصال قرب المنطقة الرياضية الجديدة والبلدة القديمة والممشى الساحلي وسييرا برميخا. ويذكر ملف المطوّر أن البلدة القديمة على بُعد 5 دقائق، والطريق A-7 على بُعد 3 دقائق، وبويرتو بانوس 20 دقيقة، وماربيا 30 دقيقة، ومطار مالقة ساعة. ويذكر الإعلان أيضًا المستشفى ومنطقة الميناء المجددة والمدارس بين المعالم القريبة.',
  'De woningen liggen in de woonwijk El Calvario in Estepona, een rustige en goed bereikbare buurt bij de nieuwe sportzone, de oude stad, het kustpad en de Sierra Bermeja. Het dossier van de ontwikkelaar noemt de oude stad op 5 minuten, de A-7 op 3, Puerto Banús op 20, Marbella op 30 en de luchthaven van Málaga op een uur. De aankondiging noemt ook het ziekenhuis, het vernieuwde havengebied en de scholen als dichtbij.',
  'Mieszkania znajdują się w dzielnicy mieszkalnej El Calvario w Esteponie, spokojnej i dobrze skomunikowanej okolicy w pobliżu nowej strefy sportowej, starego miasta, nadmorskiej ścieżki i gór Sierra Bermeja. Dossier dewelopera podaje, że do starego miasta jest 5 minut, do A-7 3, do Puerto Banús 20, do Marbelli 30, a do lotniska w Maladze godzina. W ogłoszeniu jako pobliskie wymieniono też szpital, odnowioną strefę portową i szkoły.',
  'Boligene ligger i boligområdet El Calvario i Estepona, et rolig og godt forbundet nabolag nær den nye idrettssonen, gamlebyen, kyststien og Sierra Bermeja. Utbyggerens dossier oppgir gamlebyen 5 minutter unna, A-7 3, Puerto Banús 20, Marbella 30 og Málaga lufthavn en time. Annonsen nevner også sykehuset, det fornyede havneområdet og skolene som nære.',
  'Bostäderna ligger i bostadsområdet El Calvario i Estepona, ett lugnt och välförbundet område nära den nya idrottszonen, gamla stan, kustpromenaden och Sierra Bermeja. Exploatörens dossier anger gamla stan på 5 minuter, A-7 på 3, Puerto Banús på 20, Marbella på 30 och Málagas flygplats på en timme. Annonsen nämner också sjukhuset, det förnyade hamnområdet och skolorna som nära.')
a('El Calvario, <em>Estepona</em>', 'El Calvario, <em>Estepona</em>', 'El Calvario, <em>Estepona</em>', 'El Calvario, <em>Estepona</em>',
  'Эль-Кальварио, <em>Эстепона</em>', 'إل كالفاريو، <em>إستيبونا</em>', 'El Calvario, <em>Estepona</em>', 'El Calvario, <em>Estepona</em>',
  'El Calvario, <em>Estepona</em>', 'El Calvario, <em>Estepona</em>')
a('Mediterranean Highway (A-7)', 'Autovía del Mediterráneo (A-7)', 'Autoroute de la Méditerranée (A-7)', 'Mittelmeer-Autobahn (A-7)',
  'Средиземноморское шоссе (A-7)', 'الطريق السريع المتوسطي (A-7)', 'Middellandse Zeesnelweg (A-7)', 'Autostrada Śródziemnomorska (A-7)',
  'Middelhavsmotorveien (A-7)', 'Medelhavsmotorvägen (A-7)')
a('Approx. 1 hour', 'Aprox. 1 hora', 'Environ 1 heure', 'Ca. 1 Stunde', 'Около 1 часа', 'حوالي ساعة', 'Ca. 1 uur', 'Ok. 1 godzina',
  'Ca. 1 time', 'Ca 1 timme')

# ---------------------------------------------------------------- purchase
a('The terms are those of the developer’s payment schedule. We confirm the current amounts and dates in writing before you reserve.',
  'Las condiciones son las del calendario de pagos del promotor. Confirmamos por escrito los importes y fechas actuales antes de que reserve.',
  'Les conditions sont celles de l’échéancier de paiement du promoteur. Nous confirmons par écrit les montants et les dates en vigueur avant votre réservation.',
  'Die Bedingungen sind die des Zahlungsplans des Bauträgers. Wir bestätigen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.',
  'Условия определяются графиком платежей застройщика. Перед бронированием мы письменно подтверждаем актуальные суммы и даты.',
  'تخضع الشروط لجدول دفعات المطوّر. ونؤكد كتابةً المبالغ والتواريخ الحالية قبل أن تحجزوا.',
  'De voorwaarden zijn die van het betalingsschema van de ontwikkelaar. Wij bevestigen de actuele bedragen en data schriftelijk voordat u reserveert.',
  'Warunki są zgodne z harmonogramem płatności dewelopera. Przed rezerwacją potwierdzamy na piśmie aktualne kwoty i terminy.',
  'Vilkårene er de i utbyggerens betalingsplan. Vi bekrefter gjeldende beløp og datoer skriftlig før dere reserverer.',
  'Villkoren är de i exploatörens betalningsplan. Vi bekräftar gällande belopp och datum skriftligen innan ni reserverar.')
a('The reservation is EUR 6,000 plus VAT. The payment terms we hold do not say whether it is deducted from the first instalment, so we ask.',
  'La reserva es de {E6000} más IVA. Las condiciones de pago que tenemos no indican si se descuenta del primer pago, por lo que lo preguntamos.',
  'La réservation est de {E6000} hors TVA. Les conditions de paiement dont nous disposons ne précisent pas si elle est déduite du premier versement ; nous posons donc la question.',
  'Die Reservierung beträgt {E6000} zuzüglich MwSt. Die uns vorliegenden Zahlungsbedingungen sagen nicht, ob sie von der ersten Rate abgezogen wird, daher fragen wir nach.',
  'Бронирование стоит {E6000} плюс НДС. В имеющихся у нас условиях оплаты не сказано, засчитывается ли оно в первый платёж, поэтому мы это уточняем.',
  'الحجز {E6000} زائد ضريبة القيمة المضافة. ولا تذكر شروط الدفع التي بحوزتنا ما إذا كان يُخصم من الدفعة الأولى، لذلك نستفسر عن ذلك.',
  'De reservering bedraagt {E6000} plus btw. De betalingsvoorwaarden die wij hebben, vermelden niet of ze van de eerste termijn wordt afgetrokken, dus vragen wij het na.',
  'Rezerwacja kosztuje {E6000} plus VAT. Posiadane przez nas warunki płatności nie podają, czy jest ona odliczana od pierwszej raty, dlatego o to pytamy.',
  'Reservasjonen er {E6000} pluss mva. Betalingsvilkårene vi har sier ikke om den trekkes fra første delbetaling, så vi spør om det.',
  'Reservationen är {E6000} plus moms. De betalningsvillkor vi har anger inte om den dras av från första delbetalningen, så vi frågar om det.')
a('30% plus VAT on signing the purchase contract and 70% plus VAT on the deed at the notary.',
  'El 30% más IVA al firmar el contrato de compraventa y el 70% más IVA en la escritura ante notario.',
  '30 % hors TVA à la signature du contrat de vente et 70 % hors TVA à l’acte notarié.',
  '30 % zuzüglich MwSt. bei Unterzeichnung des Kaufvertrags und 70 % zuzüglich MwSt. bei der notariellen Beurkundung.',
  '30 % плюс НДС при подписании договора купли-продажи и 70 % плюс НДС при подписании нотариального акта.',
  '30% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء، و70% زائد الضريبة عند توقيع سند الملكية أمام كاتب العدل.',
  '30% plus btw bij het ondertekenen van de koopovereenkomst en 70% plus btw bij de notariële akte.',
  '30% plus VAT przy podpisaniu umowy sprzedaży i 70% plus VAT przy akcie notarialnym.',
  '30 % pluss mva ved signering av kjøpekontrakten og 70 % pluss mva ved skjøtet hos notarius.',
  '30 % plus moms vid undertecknandet av köpekontraktet och 70 % plus moms vid lagfarten hos notarien.')
a('The price list does not include VAT and does not give the rate. Nueva Living confirms the rate and the purchase costs in writing.',
  'La lista de precios no incluye el IVA y no indica el tipo. Nueva Living confirma por escrito el tipo y los gastos de compra.',
  'La liste de prix n’inclut pas la TVA et n’en indique pas le taux. Nueva Living confirme par écrit le taux et les frais d’achat.',
  'Die Preisliste enthält keine MwSt. und nennt den Satz nicht. Nueva Living bestätigt den Satz und die Kaufnebenkosten schriftlich.',
  'Прайс-лист не включает НДС и не указывает ставку. Nueva Living письменно подтверждает ставку и расходы на покупку.',
  'قائمة الأسعار لا تشمل ضريبة القيمة المضافة ولا تذكر نسبتها. وتؤكد Nueva Living النسبة ومصاريف الشراء كتابةً.',
  'De prijslijst bevat geen btw en geeft het tarief niet aan. Nueva Living bevestigt het tarief en de aankoopkosten schriftelijk.',
  'Cennik nie zawiera VAT i nie podaje stawki. Nueva Living potwierdza na piśmie stawkę i koszty zakupu.',
  'Prislisten inkluderer ikke mva. og oppgir ikke satsen. Nueva Living bekrefter satsen og kjøpskostnadene skriftlig.',
  'Prislistan inkluderar inte moms och anger inte momssatsen. Nueva Living bekräftar satsen och köpkostnaderna skriftligen.')
a('Each of the eight listed homes comes with a storage room and one or two garage spaces, as the price list shows. The furniture shown in the images is not included.',
  'Cada una de las ocho viviendas a la venta incluye un trastero y una o dos plazas de garaje, según la lista de precios. El mobiliario que aparece en las imágenes no está incluido.',
  'Chacun des huit logements annoncés comprend une cave et une ou deux places de garage, selon la liste de prix. Le mobilier présenté sur les images n’est pas inclus.',
  'Jede der acht gelisteten Wohnungen umfasst laut Preisliste einen Abstellraum und einen oder zwei Garagenstellplätze. Die auf den Bildern gezeigten Möbel sind nicht enthalten.',
  'Согласно прайс-листу, к каждой из восьми квартир в продаже прилагаются кладовая и одно или два места в гараже. Мебель, показанная на изображениях, в стоимость не входит.',
  'يشمل كل مسكن من المساكن الثمانية المعروضة غرفة تخزين وموقفًا أو موقفين في المرآب، كما تُظهر قائمة الأسعار. والأثاث الظاهر في الصور غير مشمول.',
  'Elk van de acht aangeboden woningen heeft volgens de prijslijst een berging en een of twee garageplaatsen. De meubels op de beelden zijn niet inbegrepen.',
  'Zgodnie z cennikiem każde z ośmiu oferowanych mieszkań ma komórkę lokatorską i jedno lub dwa miejsca garażowe. Meble widoczne na wizualizacjach nie są wliczone w cenę.',
  'Hver av de åtte annonserte boligene har ifølge prislisten en bod og én eller to garasjeplasser. Møblene som vises på bildene er ikke inkludert.',
  'Var och en av de åtta listade bostäderna har enligt prislistan ett förråd och en eller två garageplatser. Möblerna som visas på bilderna ingår inte.')

# ---------------------------------------------------------------- what we check
a('The listing marks the works as started. The documents we hold do not give the status of the building licence, so we ask for it and for the bank guarantee that covers amounts paid on account.',
  'El anuncio indica que las obras han comenzado. Los documentos que tenemos no dan el estado de la licencia de obras, por lo que la pedimos, junto con la garantía bancaria que cubre las cantidades entregadas a cuenta.',
  'L’annonce indique que les travaux ont commencé. Les documents dont nous disposons ne donnent pas l’état du permis de construire ; nous le demandons donc, ainsi que la garantie bancaire qui couvre les sommes versées en acompte.',
  'Laut Anzeige haben die Bauarbeiten begonnen. Die uns vorliegenden Dokumente nennen den Stand der Baugenehmigung nicht, daher fragen wir sie an, zusammen mit der Bankgarantie, die geleistete Anzahlungen absichert.',
  'В объявлении указано, что строительство начато. В имеющихся у нас документах не указан статус разрешения на строительство, поэтому мы запрашиваем его, а также банковскую гарантию, покрывающую суммы, внесённые авансом.',
  'يذكر الإعلان أن الأعمال قد بدأت. ولا تبيّن الوثائق التي بحوزتنا حالة رخصة البناء، لذلك نطلبها، مع الضمان المصرفي الذي يغطي المبالغ المدفوعة مقدمًا.',
  'In de aankondiging staat dat de werken zijn gestart. De documenten die wij hebben, geven de status van de bouwvergunning niet aan, dus vragen wij die op, samen met de bankgarantie die vooruitbetaalde bedragen dekt.',
  'W ogłoszeniu napisano, że prace budowlane się rozpoczęły. Posiadane przez nas dokumenty nie podają statusu pozwolenia na budowę, dlatego prosimy o nie oraz o gwarancję bankową obejmującą wpłacone zaliczki.',
  'I annonsen står det at byggearbeidene er startet. Dokumentene vi har oppgir ikke status for byggetillatelsen, så vi ber om den, og om bankgarantien som dekker beløp betalt på forhånd.',
  'Annonsen anger att byggarbetena har påbörjats. De dokument vi har anger inte bygglovets status, så vi ber om det och om bankgarantin som täcker belopp som betalats i förskott.')
a('No document we hold gives a delivery date, so we ask for the contractual date for the building you choose and put it in writing.',
  'Ningún documento que tenemos da una fecha de entrega, por lo que pedimos la fecha contractual del edificio que usted elija y la ponemos por escrito.',
  'Aucun document dont nous disposons ne donne de date de livraison ; nous demandons donc la date contractuelle pour l’immeuble que vous choisissez et la mettons par écrit.',
  'Kein uns vorliegendes Dokument nennt einen Übergabetermin, daher fragen wir das vertragliche Datum für das von Ihnen gewählte Gebäude an und halten es schriftlich fest.',
  'Ни в одном из имеющихся у нас документов не указан срок сдачи, поэтому мы запрашиваем договорную дату для выбранного вами корпуса и фиксируем её письменно.',
  'لا تذكر أي من الوثائق التي بحوزتنا موعد تسليم، لذلك نطلب التاريخ التعاقدي للمبنى الذي تختارونه ونثبّته كتابةً.',
  'Geen van de documenten die wij hebben noemt een opleveringsdatum, dus vragen wij de contractuele datum voor het gebouw dat u kiest op en leggen die schriftelijk vast.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu oddania, dlatego prosimy o termin umowny dla budynku, który Państwo wybiorą, i potwierdzamy go na piśmie.',
  'Ingen av dokumentene vi har oppgir en overleveringsdato, så vi ber om den kontraktsfestede datoen for bygget dere velger og får den skriftlig.',
  'Inget av de dokument vi har anger ett tillträdesdatum, så vi ber om det avtalade datumet för den byggnad ni väljer och får det skriftligen.')
a('The price list and the plans agree on the built area of every home but not on the interior area, the terraces or the solariums. For home 3-2-A2 the list gives a solarium of 44.06 sqm and a terrace of 33.17 sqm, and the plan gives 46.46 and 35.97 sqm. We confirm which figures the contract uses.',
  'La lista de precios y los planos coinciden en la superficie construida de cada vivienda, pero no en la superficie interior, las terrazas ni los solariums. Para la vivienda 3-2-A2, la lista da un solárium de {N44.06} {U} y una terraza de {N33.17} {U}, y el plano da {N46.46} y {N35.97} {U}. Confirmamos qué cifras utiliza el contrato.',
  'La liste de prix et les plans concordent sur la surface construite de chaque logement, mais pas sur la surface intérieure, les terrasses ni les solariums. Pour le logement 3-2-A2, la liste donne un solarium de {N44.06} {U} et une terrasse de {N33.17} {U}, et le plan donne {N46.46} et {N35.97} {U}. Nous confirmons quels chiffres le contrat retient.',
  'Preisliste und Pläne stimmen bei der bebauten Fläche jeder Wohnung überein, nicht aber bei Innenfläche, Terrassen und Solarien. Für die Wohnung 3-2-A2 nennt die Liste ein Solarium von {N44.06} {U} und eine Terrasse von {N33.17} {U}, der Plan {N46.46} und {N35.97} {U}. Wir klären, welche Zahlen der Vertrag verwendet.',
  'Прайс-лист и планы совпадают по застроенной площади каждой квартиры, но не по внутренней площади, террасам и солярием. Для квартиры 3-2-A2 в прайс-листе солярий {N44.06} {U} и терраса {N33.17} {U}, а на плане — {N46.46} и {N35.97} {U}. Мы уточняем, какие цифры использует договор.',
  'تتفق قائمة الأسعار والمخططات على المساحة المبنية لكل مسكن لكنها تختلف في المساحة الداخلية والتراسات والسولاريوم. فبالنسبة إلى المسكن 3-2-A2 تذكر القائمة سولاريوم بمساحة {N44.06} {U} وتراسًا بمساحة {N33.17} {U}، بينما يذكر المخطط {N46.46} و{N35.97} {U}. ونتحقق من الأرقام التي يعتمدها العقد.',
  'De prijslijst en de plattegronden komen overeen voor de bebouwde oppervlakte van elke woning, maar niet voor de binnenoppervlakte, de terrassen en de solariums. Voor woning 3-2-A2 geeft de lijst een solarium van {N44.06} {U} en een terras van {N33.17} {U}, en de plattegrond {N46.46} en {N35.97} {U}. Wij bevestigen welke cijfers het contract hanteert.',
  'Cennik i rzuty zgadzają się co do powierzchni zabudowy każdego mieszkania, ale nie co do powierzchni wewnętrznej, tarasów i solariów. Dla mieszkania 3-2-A2 cennik podaje solarium o powierzchni {N44.06} {U} i taras o powierzchni {N33.17} {U}, a rzut {N46.46} i {N35.97} {U}. Potwierdzamy, które wartości przyjmuje umowa.',
  'Prislisten og plantegningene stemmer overens om bebygd areal for hver bolig, men ikke om innvendig areal, terrassene og solterrassene. For bolig 3-2-A2 oppgir listen en solterrasse på {N44.06} {U} og en terrasse på {N33.17} {U}, og plantegningen {N46.46} og {N35.97} {U}. Vi bekrefter hvilke tall kontrakten bruker.',
  'Prislistan och planritningarna stämmer överens om den byggda ytan för varje bostad men inte om den invändiga ytan, terrasserna och solterrasserna. För bostad 3-2-A2 anger listan en solterrass på {N44.06} {U} och en terrass på {N33.17} {U}, och planritningen {N46.46} och {N35.97} {U}. Vi bekräftar vilka siffror avtalet använder.')
a('The distances', 'Las distancias', 'Les distances', 'Die Entfernungen', 'Расстояния', 'المسافات', 'De afstanden', 'Odległości', 'Avstandene', 'Avstånden')
a('The dossier gives the beach as 10 minutes away in its description of the area and the sea as 5 minutes by car on its location map. We ask what each figure measures.',
  'El dosier sitúa la playa a 10 minutos en su descripción de la zona y el mar a 5 minutos en coche en su mapa de ubicación. Preguntamos qué mide cada cifra.',
  'Le dossier situe la plage à 10 minutes dans sa description du quartier et la mer à 5 minutes en voiture sur sa carte de localisation. Nous demandons ce que mesure chaque chiffre.',
  'Das Dossier nennt den Strand in seiner Beschreibung der Umgebung in 10 Minuten Entfernung und das Meer auf seiner Lagekarte in 5 Minuten mit dem Auto. Wir fragen nach, was jede Angabe misst.',
  'В досье пляж в описании района находится в 10 минутах, а на карте расположения море — в 5 минутах на машине. Мы уточняем, что измеряет каждая из цифр.',
  'يذكر الملف أن الشاطئ على بُعد 10 دقائق في وصف المنطقة، وأن البحر على بُعد 5 دقائق بالسيارة في خريطة الموقع. ونستفسر عمّا يقيسه كل رقم.',
  'Het dossier noemt het strand op 10 minuten in zijn beschrijving van de omgeving en de zee op 5 minuten met de auto op zijn locatiekaart. Wij vragen na wat elk cijfer meet.',
  'Dossier podaje plażę w odległości 10 minut w opisie okolicy, a morze w odległości 5 minut samochodem na mapie lokalizacji. Pytamy, co mierzy każda z tych wartości.',
  'Dossieret oppgir stranden 10 minutter unna i beskrivelsen av området og havet 5 minutter unna med bil på kartet over beliggenheten. Vi spør hva hvert av tallene måler.',
  'Dossiern anger stranden på 10 minuters avstånd i beskrivningen av området och havet på 5 minuter med bil på sin lägeskarta. Vi frågar vad varje siffra mäter.')

# ---------------------------------------------------------------- availability
a('8 of 40 homes <em>currently available</em>', '8 de 40 viviendas <em>a la venta actualmente</em>', '8 logements sur 40 <em>actuellement annoncés</em>',
  '8 von 40 Wohnungen <em>derzeit verfügbar</em>', '8 из 40 квартир <em>сейчас в продаже</em>', '8 من أصل 40 مسكنًا <em>معروضة حاليًا</em>',
  '8 van de 40 woningen <em>momenteel beschikbaar</em>', '8 z 40 mieszkań <em>obecnie dostępnych</em>', '8 av 40 boliger <em>ledige nå</em>',
  '8 av 40 bostäder <em>lediga just nu</em>')
a('Eight apartments are listed: two on the ground floor with a garden, four on the second floor with a solarium, a two-bedroom home with a terrace and a one-bedroom home. Prices are those of the developer’s price list as of October 2026 and exclude VAT, and we confirm availability and price before any reservation.',
  'Figuran ocho apartamentos: dos en planta baja con jardín, cuatro en la segunda planta con solárium, una vivienda de dos dormitorios con terraza y una de un dormitorio. Los precios son los de la lista de precios del promotor a octubre de 2026 y no incluyen IVA; confirmamos la disponibilidad y el precio antes de cualquier reserva.',
  'Huit appartements sont annoncés : deux au rez-de-chaussée avec jardin, quatre au deuxième étage avec solarium, un logement de deux chambres avec terrasse et un d’une chambre. Les prix sont ceux de la liste de prix du promoteur à octobre 2026 et s’entendent hors TVA ; nous confirmons la disponibilité et le prix avant toute réservation.',
  'Acht Wohnungen sind gelistet: zwei im Erdgeschoss mit Garten, vier im zweiten Obergeschoss mit Solarium, eine Wohnung mit zwei Schlafzimmern und Terrasse und eine mit einem Schlafzimmer. Die Preise stammen aus der Preisliste des Bauträgers mit Stand Oktober 2026 und verstehen sich zuzüglich MwSt.; Verfügbarkeit und Preis bestätigen wir vor jeder Reservierung.',
  'В продаже восемь квартир: две на первом этаже с садом, четыре на третьем этаже с солярием, одна с двумя спальнями и террасой и одна с одной спальней. Цены взяты из прайс-листа застройщика по состоянию на октябрь 2026 года и не включают НДС; наличие и цену мы подтверждаем до любого бронирования.',
  'تُعرض ثماني شقق: اثنتان في الطابق الأرضي بحديقة، وأربع في الطابق الثاني بسولاريوم، ومسكن بغرفتي نوم وتراس، ومسكن بغرفة نوم واحدة. الأسعار وفق قائمة أسعار المطوّر حتى أكتوبر 2026 ولا تشمل ضريبة القيمة المضافة، ونؤكد التوفر والسعر قبل أي حجز.',
  'Acht appartementen staan vermeld: twee op de begane grond met een tuin, vier op de tweede verdieping met een solarium, een woning met twee slaapkamers en een terras en een woning met één slaapkamer. De prijzen zijn die van de prijslijst van de ontwikkelaar per oktober 2026 en zijn exclusief btw; wij bevestigen beschikbaarheid en prijs vóór elke reservering.',
  'Ogłoszono osiem mieszkań: dwa na parterze z ogrodem, cztery na drugim piętrze z solarium, jedno z dwiema sypialniami i tarasem oraz jedno z jedną sypialnią. Ceny pochodzą z cennika dewelopera według stanu na październik 2026 r. i nie zawierają VAT; dostępność i cenę potwierdzamy przed każdą rezerwacją.',
  'Åtte leiligheter er annonsert: to i første etasje med hage, fire i tredje etasje med solterrasse, en bolig med to soverom og terrasse og en med ett soverom. Prisene er de i utbyggerens prisliste per oktober 2026 og er eksklusive mva.; vi bekrefter tilgjengelighet og pris før enhver reservasjon.',
  'Åtta lägenheter är listade: två på bottenvåningen med trädgård, fyra på andra våningen med solterrass, en bostad med två sovrum och terrass och en med ett sovrum. Priserna är de i exploatörens prislista per oktober 2026 och är exklusive moms; vi bekräftar tillgänglighet och pris före varje reservation.')
a('Prices, bedrooms, areas, garage spaces and storage rooms are transcribed from the developer’s price list for the eight homes it lists as available out of 40, as of October 2026. The list is not dated, states that prices exclude VAT and says that availability is subject to confirmation. The built area includes a share of the communal areas, and the terrace shown is the covered and the uncovered terrace together. The developer’s sales plans match the list on the built area but differ slightly on the interior area, the terraces, the gardens and the solariums; both figures are given for each home type above.',
  'Los precios, los dormitorios, las superficies, las plazas de garaje y los trasteros están transcritos de la lista de precios del promotor para las ocho viviendas que figuran como disponibles de las 40, a octubre de 2026. La lista no lleva fecha, indica que los precios no incluyen IVA y señala que la disponibilidad está sujeta a confirmación. La superficie construida incluye una parte proporcional de zonas comunes; la terraza indicada es la cubierta y la descubierta juntas. Los planos de venta del promotor coinciden con la lista en la superficie construida pero difieren ligeramente en la superficie interior, las terrazas, los jardines y los solariums; arriba se dan ambas cifras para cada tipo de vivienda.',
  'Les prix, les chambres, les surfaces, les places de garage et les caves sont transcrits de la liste de prix du promoteur pour les huit logements qu’elle donne comme disponibles sur 40, à octobre 2026. La liste n’est pas datée, indique que les prix s’entendent hors TVA et précise que la disponibilité est à confirmer. La surface construite inclut une part des parties communes ; la terrasse indiquée est la terrasse couverte et la terrasse découverte ensemble. Les plans de vente du promoteur concordent avec la liste sur la surface construite mais diffèrent légèrement sur la surface intérieure, les terrasses, les jardins et les solariums ; les deux chiffres sont donnés ci-dessus pour chaque type de logement.',
  'Preise, Schlafzimmer, Flächen, Garagenstellplätze und Abstellräume sind der Preisliste des Bauträgers für die acht Wohnungen entnommen, die sie von 40 als verfügbar aufführt, mit Stand Oktober 2026. Die Liste trägt kein Datum, weist die Preise zuzüglich MwSt. aus und nennt die Verfügbarkeit freibleibend. Die bebaute Fläche enthält einen Anteil an Gemeinschaftsflächen; die angegebene Terrasse ist die überdachte und die unüberdachte Terrasse zusammen. Die Verkaufspläne des Bauträgers stimmen bei der bebauten Fläche mit der Liste überein, weichen aber bei Innenfläche, Terrassen, Gärten und Solarien geringfügig ab; oben sind für jeden Wohnungstyp beide Zahlen angegeben.',
  'Цены, количество спален, площади, места в гараже и кладовые перенесены из прайс-листа застройщика по восьми квартирам, которые в нём указаны как доступные из 40, по состоянию на октябрь 2026 года. Прайс-лист не датирован, в нём сказано, что цены не включают НДС, а наличие подлежит подтверждению. Застроенная площадь включает долю общих зон; указанная терраса — это крытая и открытая террасы вместе. Продажные планы застройщика совпадают с прайс-листом по застроенной площади, но немного расходятся по внутренней площади, террасам, садам и солярием; выше для каждого типа квартир приведены обе цифры.',
  'الأسعار وغرف النوم والمساحات ومواقف المرآب وغرف التخزين منقولة من قائمة أسعار المطوّر للمساكن الثمانية التي تدرجها متاحةً من أصل 40، حتى أكتوبر 2026. القائمة غير مؤرخة، وتنص على أن الأسعار لا تشمل ضريبة القيمة المضافة وعلى أن التوفر خاضع للتأكيد. وتشمل المساحة المبنية حصة من المناطق المشتركة، والتراس المذكور هو التراس المغطى والمكشوف معًا. وتتفق مخططات البيع الخاصة بالمطوّر مع القائمة في المساحة المبنية لكنها تختلف قليلًا في المساحة الداخلية والتراسات والحدائق والسولاريوم؛ وتُذكر أعلاه الأرقام من المصدرين لكل نوع من المساكن.',
  'Prijzen, slaapkamers, oppervlakten, garageplaatsen en bergingen zijn overgenomen uit de prijslijst van de ontwikkelaar voor de acht woningen die zij als beschikbaar noemt van de 40, per oktober 2026. De lijst is niet gedateerd, vermeldt dat de prijzen exclusief btw zijn en stelt dat de beschikbaarheid onder voorbehoud is. De bebouwde oppervlakte omvat een aandeel in de gemeenschappelijke ruimtes en het vermelde terras is het overdekte en het open terras samen. De verkoopplattegronden van de ontwikkelaar komen met de lijst overeen voor de bebouwde oppervlakte, maar wijken licht af voor de binnenoppervlakte, de terrassen, de tuinen en de solariums; hierboven staan voor elk woningtype beide cijfers.',
  'Ceny, liczba sypialni, powierzchnie, miejsca garażowe i komórki lokatorskie zostały przepisane z cennika dewelopera dla ośmiu mieszkań, które wymienia on jako dostępne z 40, według stanu na październik 2026 r. Cennik nie jest datowany, wskazuje, że ceny nie zawierają VAT, i zastrzega, że dostępność wymaga potwierdzenia. Powierzchnia zabudowy obejmuje udział w częściach wspólnych, a podany taras to taras zadaszony i niezadaszony łącznie. Plany sprzedażowe dewelopera zgadzają się z cennikiem co do powierzchni zabudowy, ale nieznacznie różnią się co do powierzchni wewnętrznej, tarasów, ogrodów i solariów; powyżej podano obie wartości dla każdego typu mieszkania.',
  'Priser, soverom, arealer, garasjeplasser og boder er hentet fra utbyggerens prisliste for de åtte boligene den oppgir som ledige av 40, per oktober 2026. Listen er ikke datert, oppgir at prisene er eksklusive mva. og sier at tilgjengeligheten er med forbehold. Bebygd areal inkluderer en andel av fellesarealene, og terrassen som er oppgitt er den overdekkede og den åpne terrassen til sammen. Utbyggerens salgstegninger stemmer med listen på bebygd areal, men avviker noe på innvendig areal, terrasser, hager og solterrasser; ovenfor er begge tallene oppgitt for hver boligtype.',
  'Priser, sovrum, ytor, garageplatser och förråd är hämtade från exploatörens prislista för de åtta bostäder den anger som lediga av 40, per oktober 2026. Listan är inte daterad, anger att priserna är exklusive moms och uppger att tillgängligheten är med förbehåll. Den byggda ytan inkluderar en andel av de gemensamma ytorna, och den angivna terrassen är den övertäckta och den öppna terrassen tillsammans. Exploatörens säljplaner stämmer med listan på den byggda ytan men avviker något på den invändiga ytan, terrasserna, trädgårdarna och solterrasserna; ovan anges båda siffrorna för varje bostadstyp.')

# ---------------------------------------------------------------- next steps
a('See the plot and the area with us, and the plans against the works.',
  'Vea la parcela y la zona con nosotros, y compare los planos con las obras.',
  'Visitez la parcelle et le quartier avec nous, et confrontez les plans aux travaux.',
  'Sehen Sie sich mit uns das Grundstück und die Umgebung an und vergleichen Sie die Pläne mit den Bauarbeiten.',
  'Посмотрите участок и район вместе с нами и сравните планы с ходом работ.',
  'شاهد القطعة والمنطقة معنا، وقارن المخططات بسير الأعمال.',
  'Bekijk het perceel en de omgeving samen met ons en leg de plattegronden naast de werken.',
  'Zobaczcie Państwo z nami działkę i okolicę oraz porównajcie rzuty ze stanem prac.',
  'Se tomten og området sammen med oss, og sammenlign plantegningene med byggearbeidene.',
  'Se tomten och området tillsammans med oss, och jämför planritningarna med byggarbetena.')
a('A reservation of EUR 6,000 plus VAT, then the purchase contract, and the deed at the notary.',
  'Una reserva de {E6000} más IVA, después el contrato de compraventa y la escritura ante notario.',
  'Une réservation de {E6000} hors TVA, puis le contrat de vente, et l’acte notarié.',
  'Eine Reservierung von {E6000} zuzüglich MwSt., dann der Kaufvertrag und die notarielle Beurkundung.',
  'Бронирование {E6000} плюс НДС, затем договор купли-продажи и нотариальный акт.',
  'حجز بمبلغ {E6000} زائد ضريبة القيمة المضافة، ثم عقد الشراء، ثم سند الملكية أمام كاتب العدل.',
  'Een reservering van {E6000} plus btw, daarna de koopovereenkomst en de notariële akte.',
  'Rezerwacja {E6000} plus VAT, następnie umowa sprzedaży i akt notarialny.',
  'En reservasjon på {E6000} pluss mva., deretter kjøpekontrakten og skjøtet hos notarius.',
  'En reservation på {E6000} plus moms, därefter köpekontraktet och lagfarten hos notarien.')
a('The homes are under construction, so a visit is about the location, the plans and the stage of the works.',
  'Las viviendas están en construcción, por lo que la visita trata de la ubicación, los planos y el estado de las obras.',
  'Les logements sont en construction ; la visite porte donc sur l’emplacement, les plans et l’état d’avancement des travaux.',
  'Die Wohnungen sind im Bau, daher geht es bei einer Besichtigung um die Lage, die Pläne und den Stand der Bauarbeiten.',
  'Квартиры строятся, поэтому просмотр посвящён расположению, планам и стадии работ.',
  'المساكن قيد الإنشاء، لذلك تتناول الزيارة الموقع والمخططات ومرحلة الأعمال.',
  'De woningen zijn in aanbouw, dus een bezoek gaat over de ligging, de plattegronden en de voortgang van de werken.',
  'Mieszkania są w budowie, dlatego wizyta dotyczy lokalizacji, rzutów i etapu prac.',
  'Boligene er under bygging, så en visning handler om beliggenheten, plantegningene og hvor langt byggearbeidene har kommet.',
  'Bostäderna är under uppförande, så ett besök handlar om läget, planritningarna och hur långt byggarbetena har kommit.')
a('See the plot and the stage the works have reached.', 'Vea la parcela y el estado de las obras.', 'Découvrez la parcelle et l’état d’avancement des travaux.',
  'Sehen Sie das Grundstück und den Stand der Bauarbeiten.', 'Посмотрите участок и стадию, которой достигли работы.',
  'شاهد القطعة والمرحلة التي بلغتها الأعمال.', 'Bekijk het perceel en de stand van de werken.', 'Zobaczcie Państwo działkę i etap, do którego doszły prace.',
  'Se tomten og hvor langt byggearbeidene har kommet.', 'Se tomten och hur långt byggarbetena har kommit.')
a('We walk to the old town with you and time it.', 'Caminamos con usted hasta el casco antiguo y medimos el tiempo.',
  'Nous allons à pied avec vous jusqu’à la vieille ville et chronométrons le trajet.', 'Wir gehen mit Ihnen zur Altstadt und stoppen die Zeit.',
  'Мы идём с вами пешком до старого города и засекаем время.', 'نمشي معكم إلى البلدة القديمة ونحسب الوقت.',
  'We lopen met u naar de oude stad en meten de tijd.', 'Idziemy z Państwem pieszo do starego miasta i mierzymy czas.',
  'Vi går med dere til gamlebyen og tar tiden.', 'Vi går med er till gamla stan och tar tiden.')
a('Licence, bank guarantee and the contract, before anything is signed.', 'Licencia, garantía bancaria y contrato, antes de firmar nada.',
  'Permis, garantie bancaire et contrat, avant toute signature.', 'Genehmigung, Bankgarantie und Vertrag, bevor etwas unterzeichnet wird.',
  'Разрешение, банковская гарантия и договор — до подписания чего-либо.', 'الرخصة والضمان المصرفي والعقد، قبل توقيع أي شيء.',
  'Vergunning, bankgarantie en contract, voordat er iets wordt ondertekend.', 'Pozwolenie, gwarancja bankowa i umowa — zanim cokolwiek zostanie podpisane.',
  'Tillatelse, bankgaranti og kontrakt, før noe undertegnes.', 'Bygglov, bankgaranti och avtal, innan något undertecknas.')
a('Ask about <em>Azahar Residences</em>', 'Pregunte por <em>Azahar Residences</em>', 'Renseignez-vous sur <em>Azahar Residences</em>',
  'Fragen Sie nach <em>Azahar Residences</em>', 'Узнайте больше об <em>Azahar Residences</em>', 'استفسر عن <em>Azahar Residences</em>',
  'Vraag naar <em>Azahar Residences</em>', 'Zapytaj o <em>Azahar Residences</em>', 'Spør om <em>Azahar Residences</em>', 'Fråga om <em>Azahar Residences</em>')
a('Hello Nueva Living, I would like information about Azahar Residences.',
  'Hola Nueva Living, me gustaría recibir información sobre Azahar Residences.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Azahar Residences.',
  'Guten Tag Nueva Living, ich hätte gerne Informationen zu Azahar Residences.',
  'Здравствуйте, Nueva Living, я хотел бы получить информацию об Azahar Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Azahar Residences.',
  'Hallo Nueva Living, ik wil graag informatie over Azahar Residences.',
  'Dzień dobry, Nueva Living, chciałbym otrzymać informacje o Azahar Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Azahar Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Azahar Residences.')

# ---------------------------------------------------------------- faq
a('The complex has 40 homes and eight are currently listed with a price: one one-bedroom home, six two-bedroom homes and one three-bedroom home, from EUR 363,000 to EUR 566,000 plus VAT.',
  'El conjunto tiene 40 viviendas y ocho figuran actualmente con precio: una de un dormitorio, seis de dos dormitorios y una de tres, de {E363000} a {E566000} más IVA.',
  'La résidence compte 40 logements et huit sont actuellement annoncés avec un prix : un d’une chambre, six de deux chambres et un de trois chambres, de {E363000} à {E566000} hors TVA.',
  'Die Anlage hat 40 Wohnungen, und acht sind derzeit mit Preis gelistet: eine mit einem, sechs mit zwei und eine mit drei Schlafzimmern, von {E363000} bis {E566000} zuzüglich MwSt.',
  'В комплексе 40 квартир, и восемь сейчас указаны с ценой: одна с одной спальней, шесть с двумя и одна с тремя, от {E363000} до {E566000} без НДС.',
  'يضم المجمع 40 مسكنًا وثمانية منها معروضة حاليًا بسعر: واحد بغرفة نوم، وستة بغرفتين، وواحد بثلاث غرف، من {E363000} إلى {E566000} دون ضريبة القيمة المضافة.',
  'Het complex telt 40 woningen en acht staan momenteel met prijs vermeld: één met één slaapkamer, zes met twee en één met drie, van {E363000} tot {E566000} excl. btw.',
  'Osiedle liczy 40 mieszkań, a osiem jest obecnie podanych z ceną: jedno z jedną sypialnią, sześć z dwiema i jedno z trzema, od {E363000} do {E566000} plus VAT.',
  'Boligområdet har 40 boliger, og åtte er for øyeblikket annonsert med pris: én med ett soverom, seks med to og én med tre, fra {E363000} til {E566000} pluss mva.',
  'Området har 40 bostäder och åtta är just nu listade med pris: en med ett sovrum, sex med två och en med tre, från {E363000} till {E566000} plus moms.')
a('No. The price list states that prices exclude VAT, and the payment terms add VAT to each instalment. The list does not give the rate, so we confirm it and the other purchase costs in writing.',
  'No. La lista de precios indica que los precios no incluyen IVA, y las condiciones de pago añaden el IVA a cada pago. La lista no indica el tipo, por lo que lo confirmamos por escrito, junto con los demás gastos de compra.',
  'Non. La liste de prix indique que les prix s’entendent hors TVA, et les conditions de paiement ajoutent la TVA à chaque versement. La liste n’en donne pas le taux ; nous le confirmons donc par écrit, ainsi que les autres frais d’achat.',
  'Nein. Laut Preisliste verstehen sich die Preise zuzüglich MwSt., und die Zahlungsbedingungen schlagen die MwSt. auf jede Rate auf. Die Liste nennt den Satz nicht, daher bestätigen wir ihn und die übrigen Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе сказано, что цены не включают НДС, а по условиям оплаты НДС добавляется к каждому платежу. Ставка в прайс-листе не указана, поэтому мы письменно подтверждаем её и остальные расходы на покупку.',
  'لا. تذكر قائمة الأسعار أن الأسعار لا تشمل ضريبة القيمة المضافة، وتضيف شروط الدفع الضريبة إلى كل دفعة. ولا تذكر القائمة النسبة، لذلك نؤكدها كتابةً مع باقي مصاريف الشراء.',
  'Nee. De prijslijst vermeldt dat de prijzen exclusief btw zijn en de betalingsvoorwaarden tellen btw bij elke termijn op. De lijst geeft het tarief niet aan, dus bevestigen wij dat en de overige aankoopkosten schriftelijk.',
  'Nie. Cennik wskazuje, że ceny nie zawierają VAT, a warunki płatności dodają VAT do każdej raty. Cennik nie podaje stawki, dlatego potwierdzamy ją i pozostałe koszty zakupu na piśmie.',
  'Nei. Prislisten oppgir at prisene er eksklusive mva., og betalingsvilkårene legger mva. til hver delbetaling. Listen oppgir ikke satsen, så vi bekrefter den og de øvrige kjøpskostnadene skriftlig.',
  'Nej. Prislistan anger att priserna är exklusive moms, och betalningsvillkoren lägger moms på varje delbetalning. Listan anger inte momssatsen, så vi bekräftar den och de övriga köpkostnaderna skriftligen.')
a('Is there parking and storage?', '¿Hay aparcamiento y trastero?', 'Y a-t-il un parking et une cave ?', 'Gibt es Stellplätze und Abstellräume?',
  'Есть ли парковка и кладовая?', 'هل توجد مواقف سيارات وغرفة تخزين؟', 'Is er parkeergelegenheid en een berging?',
  'Czy jest parking i komórka lokatorska?', 'Er det parkering og bod?', 'Finns det parkering och förråd?')
a('Yes. The price list gives each of the eight homes a storage room and one or two garage spaces, and the specification includes pre-installation for electric-car charging in the garage.',
  'Sí. La lista de precios asigna a cada una de las ocho viviendas un trastero y una o dos plazas de garaje, y la memoria de calidades incluye la preinstalación de carga para coche eléctrico en el garaje.',
  'Oui. La liste de prix attribue à chacun des huit logements une cave et une ou deux places de garage, et le descriptif prévoit le pré-équipement pour la recharge de véhicules électriques dans le garage.',
  'Ja. Laut Preisliste gehören zu jeder der acht Wohnungen ein Abstellraum und ein oder zwei Garagenstellplätze, und die Baubeschreibung umfasst die Vorinstallation für das Laden von Elektrofahrzeugen in der Garage.',
  'Да. Согласно прайс-листу, к каждой из восьми квартир прилагаются кладовая и одно или два места в гараже, а спецификация включает подготовку к зарядке электромобилей в гараже.',
  'نعم. تخصص قائمة الأسعار لكل مسكن من المساكن الثمانية غرفة تخزين وموقفًا أو موقفين في المرآب، وتشمل المواصفات تجهيزًا مسبقًا لشحن السيارات الكهربائية في المرآب.',
  'Ja. De prijslijst kent elk van de acht woningen een berging en een of twee garageplaatsen toe, en de specificatie omvat de voorbereiding voor het opladen van elektrische auto’s in de garage.',
  'Tak. Zgodnie z cennikiem każde z ośmiu mieszkań ma komórkę lokatorską i jedno lub dwa miejsca garażowe, a specyfikacja obejmuje przygotowanie do ładowania pojazdów elektrycznych w garażu.',
  'Ja. Prislisten gir hver av de åtte boligene en bod og én eller to garasjeplasser, og spesifikasjonen inkluderer forberedelse for lading av elbil i garasjen.',
  'Ja. Prislistan ger var och en av de åtta bostäderna ett förråd och en eller två garageplatser, och specifikationen inkluderar förberedelse för laddning av elbil i garaget.')
a('The listing says the works have started, but none of the documents we hold gives a delivery date. We ask for the contractual date and put it in writing.',
  'El anuncio indica que las obras han comenzado, pero ninguno de los documentos que tenemos da una fecha de entrega. Pedimos la fecha contractual y la ponemos por escrito.',
  'L’annonce indique que les travaux ont commencé, mais aucun des documents dont nous disposons ne donne de date de livraison. Nous demandons la date contractuelle et la mettons par écrit.',
  'Laut Anzeige haben die Bauarbeiten begonnen, aber keines der uns vorliegenden Dokumente nennt einen Übergabetermin. Wir fragen das vertragliche Datum an und halten es schriftlich fest.',
  'В объявлении сказано, что строительство начато, но ни в одном из имеющихся у нас документов не указан срок сдачи. Мы запрашиваем договорную дату и фиксируем её письменно.',
  'يذكر الإعلان أن الأعمال قد بدأت، لكن لا تذكر أي من الوثائق التي بحوزتنا موعد تسليم. نطلب التاريخ التعاقدي ونثبّته كتابةً.',
  'In de aankondiging staat dat de werken zijn gestart, maar geen van de documenten die wij hebben noemt een opleveringsdatum. Wij vragen de contractuele datum op en leggen die schriftelijk vast.',
  'W ogłoszeniu napisano, że prace budowlane się rozpoczęły, ale żaden z posiadanych przez nas dokumentów nie podaje terminu oddania. Prosimy o termin umowny i potwierdzamy go na piśmie.',
  'I annonsen står det at byggearbeidene er startet, men ingen av dokumentene vi har oppgir en overleveringsdato. Vi ber om den kontraktsfestede datoen og får den skriftlig.',
  'Annonsen anger att byggarbetena har påbörjats, men inget av de dokument vi har anger ett tillträdesdatum. Vi ber om det avtalade datumet och får det skriftligen.')
a('The reservation is EUR 6,000 plus VAT. Then 30% plus VAT on the purchase contract and 70% plus VAT on the deed at the notary.',
  'La reserva es de {E6000} más IVA. Luego, el 30% más IVA con el contrato de compraventa y el 70% más IVA con la escritura ante notario.',
  'La réservation est de {E6000} hors TVA. Ensuite, 30 % hors TVA au contrat de vente et 70 % hors TVA à l’acte notarié.',
  'Die Reservierung beträgt {E6000} zuzüglich MwSt. Dann 30 % zuzüglich MwSt. beim Kaufvertrag und 70 % zuzüglich MwSt. bei der notariellen Beurkundung.',
  'Бронирование стоит {E6000} плюс НДС. Затем 30 % плюс НДС при договоре купли-продажи и 70 % плюс НДС при нотариальном акте.',
  'الحجز {E6000} زائد ضريبة القيمة المضافة. ثم 30% زائد الضريبة عند عقد الشراء، و70% زائد الضريبة عند سند الملكية أمام كاتب العدل.',
  'De reservering bedraagt {E6000} plus btw. Daarna 30% plus btw bij de koopovereenkomst en 70% plus btw bij de notariële akte.',
  'Rezerwacja kosztuje {E6000} plus VAT. Następnie 30% plus VAT przy umowie sprzedaży i 70% plus VAT przy akcie notarialnym.',
  'Reservasjonen er {E6000} pluss mva. Deretter 30 % pluss mva. ved kjøpekontrakten og 70 % pluss mva. ved skjøtet hos notarius.',
  'Reservationen är {E6000} plus moms. Därefter 30 % plus moms vid köpekontraktet och 70 % plus moms vid lagfarten hos notarien.')

# ---------------------------------------------------------------- templates: unit sizes, plan labels
W = {  # built, interior, terrace, garden, solarium -- the forms sotavento-residences already uses
 'es': ('construidos', 'interiores', 'de terraza', 'de jardín', 'de solárium'),
 'fr': ('construits', 'intérieurs', 'de terrasse', 'de jardin', 'de solarium'),
 'de': ('bebaut', 'Innenfläche', 'Terrasse', 'Garten', 'Solarium'),
 'nl': ('bebouwd', 'binnen', 'terras', 'tuin', 'solarium'),
 'pl': ('zabudowy', 'wnętrza', 'tarasu', 'ogrodu', 'solarium'),
 'no': ('bebygd areal', 'innvendig', 'terrasse', 'hage', 'solterrasse'),
 'sv': ('byggyta', 'inomhus', 'terrass', 'trädgård', 'solterrass'),
}
AR_W = ('مبنية', 'داخلية', 'تراس', 'حديقة', 'سولاريوم')
RU_W = ('застроенной площади', 'внутри', 'терраса', 'сад', 'солярий')


def size_str(src, l):
    parts = [p.strip() for p in src.split(',')]
    out = []
    for p in parts:
        m = re.fullmatch(r'([\d.]+) sqm (built|interior|terrace|garden|solarium)', p)
        assert m, p
        n, kind = m.group(1), ['built', 'interior', 'terrace', 'garden', 'solarium'].index(m.group(2))
        v = num(n, l)
        if l == 'ru':
            out.append(f'{v} м² {RU_W[0]}' if kind == 0 else f'{v} м² {RU_W[1]}' if kind == 1 else f'{RU_W[kind]} {v} м²')
        elif l == 'ar':
            out.append(f'{v} م² {AR_W[kind]}')
        else:
            out.append(f'{v} m² {W[l][kind]}')
    return ('، ' if l == 'ar' else ', ').join(out)


SIZES = ['91.15 sqm built, 67.22 sqm interior, 29.43 sqm terrace, 78.11 sqm garden',
         '94.48 sqm built, 73.00 sqm interior, 22.38 sqm terrace',
         '89.99 sqm built, 66.98 sqm interior, 37.96 sqm terrace, 60.57 sqm solarium',
         '64.77 sqm built, 47.99 sqm interior, 36.15 sqm terrace',
         '95.02 sqm built, 71.11 sqm interior, 27.16 sqm terrace, 66.23 sqm garden',
         '97.42 sqm built, 72.98 sqm interior, 33.17 sqm terrace, 44.06 sqm solarium',
         '86.24 sqm built, 66.69 sqm interior, 26.22 sqm terrace, 65.87 sqm solarium',
         '113.52 sqm built, 84.92 sqm interior, 20.38 sqm terrace, 55.62 sqm solarium']
for s in SIZES:
    T[s] = {l: size_str(s, l) for l in LOCS}

FLOORPLAN = {'es': 'Plano de la vivienda {}', 'fr': 'Plan du logement {}', 'de': 'Grundriss der Wohnung {}', 'ru': 'Планировка квартиры {}',
             'ar': 'مخطط المسكن {}', 'nl': 'Plattegrond van woning {}', 'pl': 'Rzut mieszkania {}', 'no': 'Plantegning av bolig {}',
             'sv': 'Planritning för bostad {}'}
HOME = {'es': 'Vivienda {}', 'fr': 'Logement {}', 'de': 'Wohnung {}', 'ru': 'Квартира {}', 'ar': 'المسكن {}', 'nl': 'Woning {}',
        'pl': 'Mieszkanie {}', 'no': 'Bolig {}', 'sv': 'Bostad {}'}
for u in ['1-0-A0', '1-2-B2', '1-2-D2', '1-3-B3', '3-0-C0', '3-2-A2', '3-2-C2', '3-2-D2']:
    T[f'Floorplan of home {u}'] = {l: FLOORPLAN[l].format(u) for l in LOCS}
    T[f'Home {u}'] = {l: HOME[l].format(u) for l in LOCS}

json.dump(T, open(f'{SP}/tr_z.json', 'w'), ensure_ascii=False, indent=1)
print('entries', len(T))
