# -*- coding: utf-8 -*-
# Olivar Residences, human translations in one pass.
# a(en, es, fr, de, ru, ar, nl, pl, no, sv)
#
# Tokens, expanded per locale as in k_cedro.py: €775000 -> "775.000 €" (nl "€ 775.000",
# fr/ru/pl/no/sv "775 000 €", ar "775,000 €"), #171.55 -> "171,55" (ar "171.55"), and
# [m2] -> m² (ru "м²", ar "م²").
#
# The 16 floorplan alts and the 12 unit-size strings are generated from a template per
# locale, so a figure is written once and the wording cannot drift between rows.
#
#   python3 tools/import/k_olivar.py <workdir>/tr_o.json <workdir>/todo.json
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


def a(en, *tr):
    assert len(tr) == 9, en[:60]
    if en not in TODO:
        return  # the translation memory already has it
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(en):
    a(en, *([en] * 9))


# ---------------------------------------------------------------- names
for s in ('Olivar Residences', 'Olivar', 'Olivar <em>Residences</em>', 'Ask about <em>Olivar Residences</em>'):
    same(s)
a('Hello Nueva Living, I would like information about Olivar Residences.',
  'Hola Nueva Living, me gustaría recibir información sobre Olivar Residences.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Olivar Residences.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Olivar Residences.',
  'Здравствуйте, Nueva Living, прошу прислать информацию о Olivar Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Olivar Residences.',
  'Goedendag Nueva Living, ik wil graag informatie over Olivar Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Olivar Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Olivar Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Olivar Residences.')
a('Ask about <em>Olivar Residences</em>',
  'Pregunte por <em>Olivar Residences</em>', 'Renseignez-vous sur <em>Olivar Residences</em>',
  'Fragen Sie nach <em>Olivar Residences</em>', 'Узнайте больше о <em>Olivar Residences</em>',
  'اسألوا عن <em>Olivar Residences</em>', 'Informeer naar <em>Olivar Residences</em>',
  'Zapytaj o <em>Olivar Residences</em>', 'Spør om <em>Olivar Residences</em>',
  'Fråga om <em>Olivar Residences</em>')

# ---------------------------------------------------------------- head
a('16 of 72 two- and three-bedroom apartments and duplex penthouses close to Estepona Golf, with garden homes on the ground floor, a communal pool and basement parking. No document we hold gives a delivery date. From EUR 330,000 plus VAT.',
  '16 de 72 apartamentos y áticos dúplex de dos y tres dormitorios cerca de Estepona Golf, con viviendas con jardín en planta baja, piscina comunitaria y aparcamiento en sótano. Ningún documento de que disponemos indica la fecha de entrega. Desde €330000 más IVA.',
  '16 appartements et penthouses duplex de deux et trois chambres sur 72, près d’Estepona Golf, avec des logements avec jardin au rez-de-chaussée, une piscine commune et un parking en sous-sol. Aucun document dont nous disposons n’indique la date de livraison. À partir de €330000 hors TVA.',
  '16 von 72 Wohnungen und Maisonette-Penthäusern mit zwei und drei Schlafzimmern in der Nähe von Estepona Golf, mit Gartenwohnungen im Erdgeschoss, Gemeinschaftspool und Tiefgaragenstellplätzen. Aus keinem der uns vorliegenden Dokumente geht ein Übergabetermin hervor. Ab €330000 zuzüglich MwSt.',
  '16 из 72 квартир и двухуровневых пентхаусов с двумя и тремя спальнями рядом с Estepona Golf, с квартирами с садом на первом этаже, общим бассейном и парковкой в подвале. Срок сдачи ни в одном из имеющихся у нас документов не указан. От €330000 без НДС.',
  '16 من أصل 72 شقة وبنتهاوس دوبلكس من غرفتي نوم وثلاث غرف نوم بالقرب من Estepona Golf، مع مساكن بحدائق في الطابق الأرضي ومسبح مشترك ومواقف في القبو. لا يذكر أي مستند لدينا موعد التسليم. ابتداءً من €330000 دون ضريبة القيمة المضافة.',
  '16 van de 72 appartementen en duplex penthouses met twee en drie slaapkamers dichtbij Estepona Golf, met tuinwoningen op de begane grond, een gemeenschappelijk zwembad en parkeren in de kelder. Geen enkel document waarover wij beschikken vermeldt een opleverdatum. Vanaf €330000 plus btw.',
  '16 z 72 mieszkań i dwupoziomowych penthouse’ów z dwiema i trzema sypialniami w pobliżu Estepona Golf, z mieszkaniami z ogrodem na parterze, wspólnym basenem i parkingiem w podziemiu. W żadnym z posiadanych przez nas dokumentów nie podano terminu odbioru. Od €330000 plus VAT.',
  '16 av 72 leiligheter og duplex-toppleiligheter med to og tre soverom nær Estepona Golf, med hageboliger i første etasje, felles basseng og parkering i kjelleren. Ingen av dokumentene vi har oppgir ferdigstillelsesdato. Fra €330000 pluss mva.',
  '16 av 72 lägenheter och duplex-takvåningar med två och tre sovrum nära Estepona Golf, med trädgårdsbostäder på bottenvåningen, gemensam pool och parkering i källaren. Ingen av de handlingar vi har anger något färdigställandedatum. Från €330000 plus moms.')

a('16 of 72 two- and three-bedroom apartments and duplex penthouses near Estepona Golf with terraces, garden homes, a communal pool and basement parking, from EUR 330,000 plus VAT.',
  '16 de 72 apartamentos y áticos dúplex de dos y tres dormitorios cerca de Estepona Golf con terrazas, viviendas con jardín, piscina comunitaria y aparcamiento en sótano, desde €330000 más IVA.',
  '16 appartements et penthouses duplex de deux et trois chambres sur 72, près d’Estepona Golf, avec terrasses, logements avec jardin, piscine commune et parking en sous-sol, à partir de €330000 hors TVA.',
  '16 von 72 Wohnungen und Maisonette-Penthäusern mit zwei und drei Schlafzimmern nahe Estepona Golf mit Terrassen, Gartenwohnungen, Gemeinschaftspool und Tiefgaragenstellplätzen, ab €330000 zuzüglich MwSt.',
  '16 из 72 квартир и двухуровневых пентхаусов с двумя и тремя спальнями рядом с Estepona Golf с террасами, квартирами с садом, общим бассейном и парковкой в подвале, от €330000 без НДС.',
  '16 من أصل 72 شقة وبنتهاوس دوبلكس من غرفتي نوم وثلاث غرف نوم بالقرب من Estepona Golf مع تراسات ومساكن بحدائق ومسبح مشترك ومواقف في القبو، ابتداءً من €330000 دون ضريبة القيمة المضافة.',
  '16 van de 72 appartementen en duplex penthouses met twee en drie slaapkamers nabij Estepona Golf met terrassen, tuinwoningen, een gemeenschappelijk zwembad en parkeren in de kelder, vanaf €330000 plus btw.',
  '16 z 72 mieszkań i dwupoziomowych penthouse’ów z dwiema i trzema sypialniami w pobliżu Estepona Golf, z tarasami, mieszkaniami z ogrodem, wspólnym basenem i parkingiem w podziemiu, od €330000 plus VAT.',
  '16 av 72 leiligheter og duplex-toppleiligheter med to og tre soverom nær Estepona Golf med terrasser, hageboliger, felles basseng og parkering i kjelleren, fra €330000 pluss mva.',
  '16 av 72 lägenheter och duplex-takvåningar med två och tre sovrum nära Estepona Golf med terrasser, trädgårdsbostäder, gemensam pool och parkering i källaren, från €330000 plus moms.')

a('Two- and three-bedroom apartments and duplex penthouses near Estepona Golf, from EUR 330,000 plus VAT.',
  'Apartamentos y áticos dúplex de dos y tres dormitorios cerca de Estepona Golf, desde €330000 más IVA.',
  'Appartements et penthouses duplex de deux et trois chambres près d’Estepona Golf, à partir de €330000 hors TVA.',
  'Wohnungen und Maisonette-Penthäuser mit zwei und drei Schlafzimmern nahe Estepona Golf, ab €330000 zuzüglich MwSt.',
  'Квартиры и двухуровневые пентхаусы с двумя и тремя спальнями рядом с Estepona Golf, от €330000 без НДС.',
  'شقق وبنتهاوس دوبلكس من غرفتي نوم وثلاث غرف نوم بالقرب من Estepona Golf، ابتداءً من €330000 دون ضريبة القيمة المضافة.',
  'Appartementen en duplex penthouses met twee en drie slaapkamers nabij Estepona Golf, vanaf €330000 plus btw.',
  'Mieszkania i dwupoziomowe penthouse’y z dwiema i trzema sypialniami w pobliżu Estepona Golf, od €330000 plus VAT.',
  'Leiligheter og duplex-toppleiligheter med to og tre soverom nær Estepona Golf, fra €330000 pluss mva.',
  'Lägenheter och duplex-takvåningar med två och tre sovrum nära Estepona Golf, från €330000 plus moms.')

a('16 of 72 homes listed',
  '16 de 72 viviendas a la venta', '16 logements annoncés sur 72', '16 von 72 Wohnungen gelistet',
  'В продаже 16 из 72 квартир', '16 مسكنًا معروضًا من أصل 72', '16 van de 72 woningen te koop',
  '16 z 72 mieszkań w ofercie', '16 av 72 boliger annonsert', '16 av 72 bostäder listade')
a('Near Estepona Golf', 'Junto a Estepona Golf', 'Près d’Estepona Golf', 'Nahe Estepona Golf',
  'Рядом с Estepona Golf', 'بالقرب من Estepona Golf', 'Nabij Estepona Golf', 'Przy Estepona Golf',
  'Nær Estepona Golf', 'Nära Estepona Golf')
a('Near Estepona Golf, Estepona', 'Junto a Estepona Golf, Estepona', 'Près d’Estepona Golf, Estepona',
  'Nahe Estepona Golf, Estepona', 'Рядом с Estepona Golf, Эстепона', 'بالقرب من Estepona Golf، إستيبونا',
  'Nabij Estepona Golf, Estepona', 'Przy Estepona Golf, Estepona', 'Nær Estepona Golf, Estepona',
  'Nära Estepona Golf, Estepona')
a('Near Estepona Golf, <em>Estepona</em>', 'Junto a Estepona Golf, <em>Estepona</em>', 'Près d’Estepona Golf, <em>Estepona</em>',
  'Nahe Estepona Golf, <em>Estepona</em>', 'Рядом с Estepona Golf, <em>Эстепона</em>', 'بالقرب من Estepona Golf، <em>إستيبونا</em>',
  'Nabij Estepona Golf, <em>Estepona</em>', 'Przy Estepona Golf, <em>Estepona</em>', 'Nær Estepona Golf, <em>Estepona</em>',
  'Nära Estepona Golf, <em>Estepona</em>')
a('From EUR 330,000 + VAT', 'Desde €330000 + IVA', 'À partir de €330000 + TVA', 'Ab €330000 + MwSt.',
  'От €330000 + НДС', 'ابتداءً من €330000 + ضريبة القيمة المضافة', 'Vanaf €330000 + btw', 'Od €330000 + VAT',
  'Fra €330000 + mva.', 'Från €330000 + moms')
a('EUR 330,000 + VAT', '€330000 + IVA', '€330000 + TVA', '€330000 + MwSt.', '€330000 + НДС',
  '€330000 + ضريبة القيمة المضافة', '€330000 + btw', '€330000 + VAT', '€330000 + mva.', '€330000 + moms')
a('EUR 330,000 - EUR 525,000 + VAT', '€330000 - €525000 + IVA', '€330000 - €525000 + TVA', '€330000 - €525000 + MwSt.',
  '€330000 - €525000 + НДС', '€330000 - €525000 + ضريبة القيمة المضافة', '€330000 - €525000 + btw',
  '€330000 - €525000 + VAT', '€330000 - €525000 + mva.', '€330000 - €525000 + moms')
a('16 of 72 two- and three-bedroom apartments and duplex penthouses with terraces, garden homes on the ground floor and a communal pool, near Estepona Golf.',
  '16 de 72 apartamentos y áticos dúplex de dos y tres dormitorios con terrazas, viviendas con jardín en planta baja y piscina comunitaria, junto a Estepona Golf.',
  '16 appartements et penthouses duplex de deux et trois chambres sur 72, avec terrasses, logements avec jardin au rez-de-chaussée et piscine commune, près d’Estepona Golf.',
  '16 von 72 Wohnungen und Maisonette-Penthäusern mit zwei und drei Schlafzimmern, mit Terrassen, Gartenwohnungen im Erdgeschoss und Gemeinschaftspool, nahe Estepona Golf.',
  '16 из 72 квартир и двухуровневых пентхаусов с двумя и тремя спальнями, с террасами, квартирами с садом на первом этаже и общим бассейном, рядом с Estepona Golf.',
  '16 من أصل 72 شقة وبنتهاوس دوبلكس من غرفتي نوم وثلاث غرف نوم مع تراسات ومساكن بحدائق في الطابق الأرضي ومسبح مشترك، بالقرب من Estepona Golf.',
  '16 van de 72 appartementen en duplex penthouses met twee en drie slaapkamers, met terrassen, tuinwoningen op de begane grond en een gemeenschappelijk zwembad, nabij Estepona Golf.',
  '16 z 72 mieszkań i dwupoziomowych penthouse’ów z dwiema i trzema sypialniami, z tarasami, mieszkaniami z ogrodem na parterze i wspólnym basenem, przy Estepona Golf.',
  '16 av 72 leiligheter og duplex-toppleiligheter med to og tre soverom, med terrasser, hageboliger i første etasje og felles basseng, nær Estepona Golf.',
  '16 av 72 lägenheter och duplex-takvåningar med två och tre sovrum, med terrasser, trädgårdsbostäder på bottenvåningen och gemensam pool, nära Estepona Golf.')

# ---------------------------------------------------------------- images and media
a('Computer-generated view of white apartment blocks with terraces on every level behind a communal pool, with palm trees and a mountain in the distance',
  'Vista generada por ordenador de bloques de apartamentos blancos con terrazas en cada nivel, tras una piscina comunitaria, con palmeras y una montaña al fondo',
  'Vue générée par ordinateur d’immeubles blancs avec des terrasses à chaque niveau derrière une piscine commune, avec des palmiers et une montagne au loin',
  'Computergenerierte Ansicht weißer Wohnblöcke mit Terrassen auf jeder Ebene hinter einem Gemeinschaftspool, mit Palmen und einem Berg im Hintergrund',
  'Компьютерная визуализация белых многоквартирных домов с террасами на каждом уровне за общим бассейном, с пальмами и горой вдали',
  'منظر مولَّد بالحاسوب لمبانٍ سكنية بيضاء بتراسات في كل طابق خلف مسبح مشترك، مع أشجار نخيل وجبل في البعيد',
  'Computergegenereerd beeld van witte appartementsblokken met terrassen op elke verdieping achter een gemeenschappelijk zwembad, met palmbomen en een berg in de verte',
  'Wygenerowany komputerowo widok białych budynków mieszkalnych z tarasami na każdej kondygnacji za wspólnym basenem, z palmami i górą w oddali',
  'Datagenerert bilde av hvite leilighetsbygg med terrasser i hver etasje bak et felles basseng, med palmer og et fjell i det fjerne',
  'Datorgenererad bild av vita flerbostadshus med terrasser på varje våning bakom en gemensam pool, med palmer och ett berg i fjärran')
a('Computer-generated aerial view of white apartment blocks with terraces and stepped roof terraces, set around lawns and stone retaining walls',
  'Vista aérea generada por ordenador de bloques de apartamentos blancos con terrazas y azoteas escalonadas, dispuestos alrededor de césped y muros de contención de piedra',
  'Vue aérienne générée par ordinateur d’immeubles blancs avec terrasses et toits-terrasses en gradins, répartis autour de pelouses et de murs de soutènement en pierre',
  'Computergenerierte Luftansicht weißer Wohnblöcke mit Terrassen und gestaffelten Dachterrassen, angeordnet um Rasenflächen und Stützmauern aus Stein',
  'Компьютерная визуализация белых многоквартирных домов с террасами и ступенчатыми кровельными террасами с высоты птичьего полёта, вокруг газонов и каменных подпорных стен',
  'منظر جوي مولَّد بالحاسوب لمبانٍ سكنية بيضاء بتراسات وأسطح متدرجة، تحيط بها مروج وجدران استنادية حجرية',
  'Computergegenereerd luchtbeeld van witte appartementsblokken met terrassen en getrapte dakterrassen, rond grasvelden en stenen keermuren',
  'Wygenerowany komputerowo widok z lotu ptaka na białe budynki mieszkalne z tarasami i schodkowymi tarasami dachowymi, rozmieszczone wokół trawników i kamiennych murów oporowych',
  'Datagenerert flyfoto av hvite leilighetsbygg med terrasser og trappede takterrasser, rundt plener og støttemurer i stein',
  'Datorgenererad flygbild av vita flerbostadshus med terrasser och trappstegsformade takterrasser, kring gräsmattor och stödmurar i sten')
a('Computer-generated balcony with a dining table and two chairs, with a view of the sea and a pool below',
  'Terraza generada por ordenador con una mesa de comedor y dos sillas, con vistas al mar y una piscina debajo',
  'Terrasse générée par ordinateur avec une table à manger et deux chaises, avec vue sur la mer et une piscine en contrebas',
  'Computergenerierter Balkon mit einem Esstisch und zwei Stühlen, mit Blick aufs Meer und einen Pool darunter',
  'Компьютерная визуализация балкона с обеденным столом и двумя стульями, с видом на море и бассейн внизу',
  'شرفة مولَّدة بالحاسوب مع طاولة طعام وكرسيين، مع إطلالة على البحر ومسبح في الأسفل',
  'Computergegenereerd balkon met een eettafel en twee stoelen, met uitzicht op zee en een zwembad beneden',
  'Wygenerowany komputerowo balkon ze stołem jadalnianym i dwoma krzesłami, z widokiem na morze i basen poniżej',
  'Datagenerert balkong med et spisebord og to stoler, med utsikt over havet og et basseng under',
  'Datorgenererad balkong med ett matbord och två stolar, med utsikt över havet och en pool nedanför')
a('Computer-generated roof terrace with a white pergola, lounge seating, a dining table and a view of the sea',
  'Azotea generada por ordenador con una pérgola blanca, zona de descanso, una mesa de comedor y vistas al mar',
  'Toit-terrasse généré par ordinateur avec une pergola blanche, un coin salon, une table à manger et vue sur la mer',
  'Computergenerierte Dachterrasse mit weißer Pergola, Loungemöbeln, einem Esstisch und Blick aufs Meer',
  'Компьютерная визуализация кровельной террасы с белой перголой, зоной отдыха, обеденным столом и видом на море',
  'سطح مولَّد بالحاسوب مع برغولا بيضاء ومقاعد جلوس وطاولة طعام وإطلالة على البحر',
  'Computergegenereerd dakterras met een witte pergola, loungezitplaatsen, een eettafel en uitzicht op zee',
  'Wygenerowany komputerowo taras dachowy z białą pergolą, strefą wypoczynku, stołem jadalnianym i widokiem na morze',
  'Datagenerert takterrasse med hvit pergola, loungemøbler, et spisebord og utsikt over havet',
  'Datorgenererad takterrass med vit pergola, loungemöbler, ett matbord och utsikt över havet')
a('Computer-generated views of the development and its interiors, and the floorplans of the 16 homes on the price list.',
  'Vistas generadas por ordenador de la promoción y sus interiores, y planos de las 16 viviendas de la lista de precios.',
  'Vues générées par ordinateur de la résidence et de ses intérieurs, et plans des 16 logements de la liste de prix.',
  'Computergenerierte Ansichten der Anlage und ihrer Innenräume sowie die Grundrisse der 16 Wohnungen der Preisliste.',
  'Компьютерные визуализации комплекса и его интерьеров и планировки 16 квартир из прайс-листа.',
  'مناظر مولَّدة بالحاسوب للمشروع وداخله، ومخططات المساكن الـ16 الواردة في قائمة الأسعار.',
  'Computergegenereerde beelden van het project en de interieurs, en de plattegronden van de 16 woningen op de prijslijst.',
  'Wygenerowane komputerowo widoki inwestycji i jej wnętrz oraz rzuty 16 mieszkań z cennika.',
  'Datagenererte bilder av prosjektet og interiørene, og plantegningene av de 16 boligene på prislisten.',
  'Datorgenererade bilder av projektet och dess interiörer samt planritningarna för de 16 bostäderna på prislistan.')
a('All the photographs are computer-generated images, and the furniture and decoration in them are illustrative and not included. The floorplans are the developer’s plans: eleven are dated September 2023 and five September or December 2025. The areas on them are approximate and subject to the final project, and the room names on them are in Spanish. On the ground-floor plans the garden is marked as unlandscaped space, and for Portal 2 - 2B the sheet we hold shows only the lower level.',
  'Todas las fotografías son imágenes generadas por ordenador, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los del promotor: once llevan fecha de septiembre de 2023 y cinco de septiembre o diciembre de 2025. Las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo, y los nombres de las estancias están en español. En los planos de planta baja el jardín figura como espacio sin ajardinar, y de Portal 2 - 2B la hoja de que disponemos muestra solo la planta inferior.',
  'Toutes les photographies sont des images générées par ordinateur, et le mobilier et la décoration qui y figurent sont illustratifs et non inclus. Les plans sont ceux du promoteur : onze sont datés de septembre 2023 et cinq de septembre ou décembre 2025. Les surfaces qui y figurent sont approximatives et soumises au projet définitif, et les noms des pièces sont en espagnol. Sur les plans du rez-de-chaussée, le jardin est indiqué comme espace non aménagé, et pour Cage 2 - 2B la feuille dont nous disposons ne montre que le niveau inférieur.',
  'Alle Fotografien sind computergenerierte Bilder, und die darin gezeigten Möbel und die Dekoration sind illustrativ und nicht enthalten. Die Grundrisse stammen vom Bauträger: elf tragen das Datum September 2023, fünf September oder Dezember 2025. Die darauf angegebenen Flächen sind ungefähre Angaben und unterliegen dem endgültigen Projekt, und die Raumbezeichnungen sind auf Spanisch. In den Erdgeschossgrundrissen ist der Garten als nicht angelegte Fläche gekennzeichnet, und für Aufgang 2 - 2B zeigt das uns vorliegende Blatt nur die untere Ebene.',
  'Все фотографии — компьютерные визуализации, а мебель и декор на них носят иллюстративный характер и не включены в стоимость. Планировки — это планы застройщика: одиннадцать датированы сентябрём 2023 года, пять — сентябрём или декабрём 2025 года. Указанные на них площади приблизительны и зависят от окончательного проекта, а названия помещений даны на испанском языке. На планах первого этажа сад обозначен как необустроенная территория, а для Подъезд 2 - 2B имеющийся у нас лист показывает только нижний уровень.',
  'جميع الصور مولَّدة بالحاسوب، والأثاث والديكور الظاهران فيها توضيحيان وغير مشمولين. المخططات هي مخططات المطوّر: أحد عشر منها مؤرخ في سبتمبر 2023 وخمسة في سبتمبر أو ديسمبر 2025. المساحات المبينة عليها تقريبية وتخضع للمشروع النهائي، وأسماء الغرف عليها بالإسبانية. في مخططات الطابق الأرضي تظهر الحديقة كمساحة غير مهيأة بالنباتات، وبالنسبة إلى مدخل 2 - 2B تُظهر الورقة التي لدينا الطابق السفلي فقط.',
  'Alle foto’s zijn computergegenereerde beelden en het meubilair en de inrichting daarop zijn illustratief en niet inbegrepen. De plattegronden zijn die van de ontwikkelaar: elf zijn gedateerd september 2023 en vijf september of december 2025. De oppervlaktes erop zijn bij benadering en onder voorbehoud van het definitieve project, en de namen van de ruimtes zijn in het Spaans. Op de plattegronden van de begane grond staat de tuin aangegeven als niet-aangelegde ruimte, en voor Portiek 2 - 2B toont het blad waarover wij beschikken alleen het onderste niveau.',
  'Wszystkie zdjęcia to obrazy wygenerowane komputerowo, a meble i dekoracje na nich mają charakter poglądowy i nie są wliczone w cenę. Rzuty to plany dewelopera: jedenaście z nich nosi datę wrzesień 2023, pięć — wrzesień lub grudzień 2025. Podane na nich powierzchnie są przybliżone i podlegają projektowi ostatecznemu, a nazwy pomieszczeń są po hiszpańsku. Na rzutach parteru ogród oznaczono jako teren nieurządzony, a dla Klatka 2 - 2B posiadany przez nas arkusz pokazuje tylko poziom dolny.',
  'Alle fotografiene er datagenererte bilder, og møblene og dekorasjonen på dem er illustrative og følger ikke med. Plantegningene er utbyggerens: elleve er datert september 2023 og fem september eller desember 2025. Arealene på dem er omtrentlige og med forbehold om det endelige prosjektet, og romnavnene er på spansk. På plantegningene for første etasje er hagen merket som uopparbeidet areal, og for Oppgang 2 - 2B viser arket vi har bare det nedre nivået.',
  'Alla fotografier är datagenererade bilder, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens: elva är daterade september 2023 och fem september eller december 2025. Ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet, och rumsnamnen är på spanska. På planritningarna för bottenvåningen är trädgården markerad som ej anlagd yta, och för Port 2 - 2B visar bladet vi har bara det nedre planet.')
a('The blocks and the communal pool', 'Los bloques y la piscina comunitaria', 'Les immeubles et la piscine commune',
  'Die Wohnblöcke und der Gemeinschaftspool', 'Дома и общий бассейн', 'المباني والمسبح المشترك',
  'De blokken en het gemeenschappelijk zwembad', 'Budynki i wspólny basen', 'Byggene og det felles bassenget',
  'Husen och den gemensamma poolen')
a('The blocks and gardens from above', 'Los bloques y los jardines desde el aire', 'Les immeubles et les jardins vus du ciel',
  'Die Wohnblöcke und Gärten von oben', 'Дома и сады с высоты', 'المباني والحدائق من الأعلى',
  'De blokken en tuinen van bovenaf', 'Budynki i ogrody z lotu ptaka', 'Byggene og hagene ovenfra',
  'Husen och trädgårdarna uppifrån')
a('A roof terrace', 'Una azotea', 'Un toit-terrasse', 'Eine Dachterrasse', 'Кровельная терраса', 'سطح خاص',
  'Een dakterras', 'Taras dachowy', 'En takterrasse', 'En takterrass')
a('Computer-generated living and dining room with a sofa, a round dining table and a sliding glass door to a terrace with a view of the sea',
  'Salón-comedor generado por ordenador con un sofá, una mesa de comedor redonda y una puerta corredera de cristal a una terraza con vistas al mar',
  'Salon-salle à manger généré par ordinateur avec un canapé, une table à manger ronde et une porte coulissante vitrée donnant sur une terrasse avec vue sur la mer',
  'Computergeneriertes Wohn- und Esszimmer mit einem Sofa, einem runden Esstisch und einer gläsernen Schiebetür zu einer Terrasse mit Meerblick',
  'Компьютерная визуализация гостиной-столовой с диваном, круглым обеденным столом и стеклянной раздвижной дверью на террасу с видом на море',
  'غرفة معيشة وطعام مولَّدة بالحاسوب مع أريكة وطاولة طعام مستديرة وباب زجاجي منزلق نحو تراس بإطلالة على البحر',
  'Computergegenereerde woon- en eetkamer met een bank, een ronde eettafel en een glazen schuifdeur naar een terras met uitzicht op zee',
  'Wygenerowany komputerowo salon z jadalnią z sofą, okrągłym stołem jadalnianym i przesuwnymi szklanymi drzwiami na taras z widokiem na morze',
  'Datagenerert stue og spisestue med en sofa, et rundt spisebord og en glasskyvedør til en terrasse med utsikt over havet',
  'Datorgenererat vardagsrum och matplats med en soffa, ett runt matbord och en glasskjutdörr till en terrass med utsikt över havet')
a('Computer-generated white kitchen with an oven, an induction hob, a dishwasher and a tall fridge, beside the dining area',
  'Cocina blanca generada por ordenador con horno, placa de inducción, lavavajillas y un frigorífico alto, junto a la zona de comedor',
  'Cuisine blanche générée par ordinateur avec un four, une plaque à induction, un lave-vaisselle et un grand réfrigérateur, à côté du coin repas',
  'Computergenerierte weiße Küche mit Backofen, Induktionskochfeld, Geschirrspüler und einem hohen Kühlschrank, neben dem Essbereich',
  'Компьютерная визуализация белой кухни с духовым шкафом, индукционной варочной панелью, посудомоечной машиной и высоким холодильником рядом с обеденной зоной',
  'مطبخ أبيض مولَّد بالحاسوب مع فرن وموقد حثّي وغسالة أطباق وثلاجة طويلة، بجوار منطقة الطعام',
  'Computergegenereerde witte keuken met een oven, een inductiekookplaat, een vaatwasser en een hoge koelkast, naast de eethoek',
  'Wygenerowana komputerowo biała kuchnia z piekarnikiem, płytą indukcyjną, zmywarką i wysoką lodówką, obok jadalni',
  'Datagenerert hvitt kjøkken med ovn, induksjonstopp, oppvaskmaskin og et høyt kjøleskap, ved siden av spiseplassen',
  'Datorgenererat vitt kök med ugn, induktionshäll, diskmaskin och ett högt kylskåp, intill matplatsen')
a('Computer-generated bedroom with a double bed and a sliding glass door to a terrace with a view of the sea',
  'Dormitorio generado por ordenador con una cama doble y una puerta corredera de cristal a una terraza con vistas al mar',
  'Chambre générée par ordinateur avec un lit double et une porte coulissante vitrée donnant sur une terrasse avec vue sur la mer',
  'Computergeneriertes Schlafzimmer mit Doppelbett und einer gläsernen Schiebetür zu einer Terrasse mit Meerblick',
  'Компьютерная визуализация спальни с двуспальной кроватью и стеклянной раздвижной дверью на террасу с видом на море',
  'غرفة نوم مولَّدة بالحاسوب مع سرير مزدوج وباب زجاجي منزلق نحو تراس بإطلالة على البحر',
  'Computergegenereerde slaapkamer met een tweepersoonsbed en een glazen schuifdeur naar een terras met uitzicht op zee',
  'Wygenerowana komputerowo sypialnia z podwójnym łóżkiem i przesuwnymi szklanymi drzwiami na taras z widokiem na morze',
  'Datagenerert soverom med dobbeltseng og en glasskyvedør til en terrasse med utsikt over havet',
  'Datorgenererat sovrum med dubbelsäng och en glasskjutdörr till en terrass med utsikt över havet')

# floorplan alts, one template per locale
PL_PREFIX = {'es': 'Plano: ', 'fr': 'Plan : ', 'de': 'Grundriss: ', 'ru': 'Планировка: ', 'ar': 'مخطط: ',
             'nl': 'Plattegrond: ', 'pl': 'Rzut: ', 'no': 'Plantegning: ', 'sv': 'Planritning: '}
PORTAL = {'es': 'Portal', 'fr': 'Cage', 'de': 'Aufgang', 'ru': 'Подъезд', 'ar': 'مدخل', 'nl': 'Portiek',
          'pl': 'Klatka', 'no': 'Oppgang', 'sv': 'Port'}
REFS = ['1 - 0A', '1 - 0C', '1 - 0D', '1 - 2A', '2 - 0B', '2 - 1A', '2 - 2B', '3 - 0B', '3 - 0C', '3 - 2A',
        '4 - 1C', '4 - 1D', '4 - 2D', '5 - 2A', '5 - 2D', '6 - 1D']
for r in REFS:
    a(f'Floorplan of Portal {r}', *[f'{PL_PREFIX[l]}{PORTAL[l]} {r}' for l in LOCS])

# ---------------------------------------------------------------- overview
a('72 homes, <em>sixteen listed</em>', '72 viviendas, <em>dieciséis a la venta</em>', '72 logements, <em>seize annoncés</em>',
  '72 Wohnungen, <em>sechzehn gelistet</em>', '72 квартиры, <em>шестнадцать в продаже</em>', '72 مسكنًا، <em>ستة عشر منها معروضة</em>',
  '72 woningen, <em>zestien te koop</em>', '72 mieszkania, <em>szesnaście w ofercie</em>', '72 boliger, <em>seksten annonsert</em>',
  '72 bostäder, <em>sexton listade</em>')
a('This is a residential development of 72 homes close to Estepona Golf, in Estepona, with two- and three-bedroom apartments, ground-floor apartments with gardens and duplex penthouses. The brochure lists 108 garages and 72 storerooms in the basement, limited places for golf buggies, a communal pool, a coworking area and a chill-out terrace, and every home has an individual aerothermal system and a furnished, equipped kitchen.',
  'Es una promoción residencial de 72 viviendas cerca de Estepona Golf, en Estepona, con apartamentos de dos y tres dormitorios, apartamentos con jardín en planta baja y áticos dúplex. El folleto indica 108 garajes y 72 trasteros en el sótano, plazas limitadas para buggies de golf, una piscina comunitaria, una zona de coworking y una terraza chill out, y cada vivienda cuenta con un sistema individual de aerotermia y una cocina amueblada y equipada.',
  'Il s’agit d’une résidence de 72 logements près d’Estepona Golf, à Estepona, avec des appartements de deux et trois chambres, des appartements avec jardin au rez-de-chaussée et des penthouses duplex. La brochure mentionne 108 garages et 72 caves en sous-sol, des places limitées pour les voiturettes de golf, une piscine commune, un espace de coworking et une terrasse chill out, et chaque logement dispose d’un système aérothermique individuel et d’une cuisine meublée et équipée.',
  'Dies ist eine Wohnanlage mit 72 Wohnungen nahe Estepona Golf in Estepona, mit Wohnungen mit zwei und drei Schlafzimmern, Erdgeschosswohnungen mit Garten und Maisonette-Penthäusern. Die Broschüre nennt 108 Garagen und 72 Abstellräume im Untergeschoss, begrenzte Plätze für Golfbuggys, einen Gemeinschaftspool, einen Coworking-Bereich und eine Chill-out-Terrasse; jede Wohnung hat eine individuelle Luft-Wasser-Wärmepumpe und eine möblierte, ausgestattete Küche.',
  'Это жилой комплекс из 72 квартир рядом с Estepona Golf, в Эстепоне, с квартирами с двумя и тремя спальнями, квартирами с садом на первом этаже и двухуровневыми пентхаусами. В брошюре указаны 108 гаражей и 72 кладовые в подвале, ограниченное число мест для гольф-каров, общий бассейн, зона коворкинга и терраса для отдыха; в каждой квартире — индивидуальная аэротермальная система и кухня с мебелью и техникой.',
  'هذا مشروع سكني من 72 مسكنًا بالقرب من Estepona Golf في إستيبونا، يضم شققًا من غرفتي نوم وثلاث غرف نوم وشققًا بحدائق في الطابق الأرضي وبنتهاوس دوبلكس. يذكر الكتيّب 108 مرائب و72 مخزنًا في القبو وأماكن محدودة لعربات الغولف ومسبحًا مشتركًا ومنطقة عمل مشترك وتراس استرخاء، ولكل مسكن نظام حراري هوائي مستقل ومطبخ مجهز بالأثاث والأجهزة.',
  'Dit is een woonproject van 72 woningen dichtbij Estepona Golf, in Estepona, met appartementen met twee en drie slaapkamers, appartementen met tuin op de begane grond en duplex penthouses. De brochure noemt 108 garages en 72 bergingen in de kelder, beperkte plaatsen voor golfbuggy’s, een gemeenschappelijk zwembad, een coworkingruimte en een chill-outterras, en elke woning heeft een individueel aerothermisch systeem en een gemeubileerde, uitgeruste keuken.',
  'To inwestycja mieszkaniowa obejmująca 72 mieszkania w pobliżu Estepona Golf, w Esteponie, z mieszkaniami z dwiema i trzema sypialniami, mieszkaniami z ogrodem na parterze i dwupoziomowymi penthouse’ami. Broszura wymienia 108 garaży i 72 komórki lokatorskie w podziemiu, ograniczoną liczbę miejsc na meleksy golfowe, wspólny basen, strefę coworkingową i taras relaksacyjny, a każde mieszkanie ma indywidualny system aerotermalny oraz umeblowaną i wyposażoną kuchnię.',
  'Dette er et boligprosjekt med 72 boliger nær Estepona Golf, i Estepona, med leiligheter med to og tre soverom, leiligheter med hage i første etasje og duplex-toppleiligheter. Brosjyren oppgir 108 garasjeplasser og 72 bodplasser i kjelleren, begrenset antall plasser til golfbiler, et felles basseng, et coworking-område og en chill out-terrasse, og hver bolig har et eget aerotermisk system og et møblert og utstyrt kjøkken.',
  'Detta är ett bostadsprojekt med 72 bostäder nära Estepona Golf, i Estepona, med lägenheter med två och tre sovrum, trädgårdslägenheter på bottenvåningen och duplex-takvåningar. Broschyren anger 108 garage och 72 förråd i källaren, begränsat antal platser för golfbilar, en gemensam pool, ett coworking-område och en chill out-terrass, och varje bostad har ett eget aerotermiskt system och ett möblerat, utrustat kök.')
a('The sales portal marks the development as works started, while the brochure calls it a construction project and the plans we hold are marked basic-project or execution-project stage. None of the documents gives a completion date, so we ask for the licence, the state of the works and the contractual date before any reservation.',
  'El portal de ventas marca la promoción como obras iniciadas, mientras que el folleto la llama proyecto de construcción y los planos de que disponemos figuran en fase de proyecto básico o de ejecución. Ninguno de los documentos indica una fecha de finalización, así que pedimos la licencia, el estado de las obras y la fecha contractual antes de cualquier reserva.',
  'Le portail de vente indique que les travaux ont commencé, alors que la brochure parle d’un projet de construction et que les plans dont nous disposons sont au stade du projet de base ou du projet d’exécution. Aucun des documents ne donne de date d’achèvement ; nous demandons donc le permis, l’état des travaux et la date contractuelle avant toute réservation.',
  'Das Verkaufsportal kennzeichnet die Anlage als „Bauarbeiten begonnen“, während die Broschüre von einem Bauprojekt spricht und die uns vorliegenden Pläne dem Stand des Basis- oder des Ausführungsprojekts entsprechen. Keines der Dokumente nennt einen Fertigstellungstermin; deshalb fordern wir vor jeder Reservierung die Genehmigung, den Stand der Arbeiten und den vertraglichen Termin an.',
  'Портал продаж отмечает комплекс как «работы начаты», тогда как в брошюре он назван проектом строительства, а имеющиеся у нас планы относятся к стадии базового проекта или проекта исполнения. Ни один из документов не называет дату завершения, поэтому перед любым бронированием мы запрашиваем разрешение, ход работ и договорную дату.',
  'تشير بوابة المبيعات إلى أن الأعمال بدأت، بينما يصف الكتيّب المشروع بأنه مشروع بناء، والمخططات التي لدينا مصنفة في مرحلة المشروع الأساسي أو مشروع التنفيذ. لا يذكر أي مستند موعد الانتهاء، لذلك نطلب الرخصة وحالة الأعمال والتاريخ التعاقدي قبل أي حجز.',
  'Het verkoopportaal markeert het project als werken gestart, terwijl de brochure het een bouwproject noemt en de plattegronden waarover wij beschikken zijn aangeduid als basisproject of uitvoeringsproject. Geen van de documenten vermeldt een opleverdatum, dus we vragen vóór elke reservering om de vergunning, de stand van de werken en de contractuele datum.',
  'Portal sprzedażowy oznacza inwestycję jako „prace rozpoczęte”, podczas gdy broszura nazywa ją projektem budowlanym, a posiadane przez nas rzuty są na etapie projektu podstawowego lub wykonawczego. Żaden z dokumentów nie podaje terminu zakończenia, dlatego przed jakąkolwiek rezerwacją prosimy o pozwolenie, stan prac i termin umowny.',
  'Salgsportalen markerer prosjektet som byggestart, mens brosjyren kaller det et byggeprosjekt og plantegningene vi har er merket som grunnprosjekt eller utførelsesprosjekt. Ingen av dokumentene oppgir ferdigstillelsesdato, så vi ber om tillatelsen, byggets status og den kontraktsfestede datoen før en reservasjon.',
  'Försäljningsportalen markerar projektet som byggstartat, medan broschyren kallar det ett byggprojekt och de planritningar vi har är märkta som grundprojekt eller genomförandeprojekt. Inget av dokumenten anger något färdigställandedatum, så vi ber om bygglovet, arbetenas status och det avtalade datumet före varje reservation.')
a('72 homes', '72 viviendas', '72 logements', '72 Wohnungen', '72 квартиры', '72 مسكنًا', '72 woningen', '72 mieszkania', '72 boliger', '72 bostäder')
a('16 homes', '16 viviendas', '16 logements', '16 Wohnungen', '16 квартир', '16 مسكنًا', '16 woningen', '16 mieszkań', '16 boliger', '16 bostäder')

# ---------------------------------------------------------------- why
a('Apartments with terraces, garden homes and duplex penthouses on one development near a golf course, with a garage space and a storeroom listed for every home.',
  'Apartamentos con terrazas, viviendas con jardín y áticos dúplex en una misma promoción junto a un campo de golf, con una plaza de garaje y un trastero en la lista para cada vivienda.',
  'Appartements avec terrasses, logements avec jardin et penthouses duplex dans une même résidence près d’un golf, avec une place de garage et une cave indiquées pour chaque logement.',
  'Wohnungen mit Terrassen, Gartenwohnungen und Maisonette-Penthäuser in einer Anlage nahe einem Golfplatz, mit einem Garagenstellplatz und einem Abstellraum, die für jede Wohnung aufgeführt sind.',
  'Квартиры с террасами, квартиры с садом и двухуровневые пентхаусы в одном комплексе рядом с полем для гольфа; для каждой квартиры указаны место в гараже и кладовая.',
  'شقق بتراسات ومساكن بحدائق وبنتهاوس دوبلكس في مشروع واحد قرب ملعب غولف، مع مكان في المرآب ومخزن مدرجين لكل مسكن.',
  'Appartementen met terrassen, tuinwoningen en duplex penthouses in één project nabij een golfbaan, met voor elke woning een garageplaats en een berging op de lijst.',
  'Mieszkania z tarasami, mieszkania z ogrodem i dwupoziomowe penthouse’y w jednej inwestycji w pobliżu pola golfowego, z miejscem w garażu i komórką lokatorską wskazanymi dla każdego mieszkania.',
  'Leiligheter med terrasser, hageboliger og duplex-toppleiligheter i ett prosjekt nær en golfbane, med garasjeplass og bod oppgitt for hver bolig.',
  'Lägenheter med terrasser, trädgårdsbostäder och duplex-takvåningar i ett projekt nära en golfbana, med en garageplats och ett förråd angivna för varje bostad.')
a('Buyers who want a new two- or three-bedroom home with a terrace, a garden or a roof terrace, near a golf course, from EUR 330,000 plus VAT.',
  'Compradores que buscan una vivienda nueva de dos o tres dormitorios con terraza, jardín o azotea, cerca de un campo de golf, desde €330000 más IVA.',
  'Acheteurs qui souhaitent un logement neuf de deux ou trois chambres avec terrasse, jardin ou toit-terrasse, près d’un golf, à partir de €330000 hors TVA.',
  'Käufer, die eine neue Wohnung mit zwei oder drei Schlafzimmern und Terrasse, Garten oder Dachterrasse nahe einem Golfplatz suchen, ab €330000 zuzüglich MwSt.',
  'Покупатели, которым нужна новая квартира с двумя или тремя спальнями, с террасой, садом или кровельной террасой рядом с полем для гольфа, от €330000 без НДС.',
  'المشترون الذين يريدون مسكنًا جديدًا من غرفتي نوم أو ثلاث غرف نوم مع تراس أو حديقة أو سطح خاص، قرب ملعب غولف، ابتداءً من €330000 دون ضريبة القيمة المضافة.',
  'Kopers die een nieuwe woning met twee of drie slaapkamers willen met een terras, een tuin of een dakterras, nabij een golfbaan, vanaf €330000 plus btw.',
  'Kupujący, którzy szukają nowego mieszkania z dwiema lub trzema sypialniami z tarasem, ogrodem lub tarasem dachowym, w pobliżu pola golfowego, od €330000 plus VAT.',
  'Kjøpere som vil ha en ny bolig med to eller tre soverom med terrasse, hage eller takterrasse, nær en golfbane, fra €330000 pluss mva.',
  'Köpare som vill ha en ny bostad med två eller tre sovrum med terrass, trädgård eller takterrass, nära en golfbana, från €330000 plus moms.')
a('Three kinds of home on one site: first-floor apartments from EUR 330,000, ground-floor apartments with gardens of 55 to 220 sqm, and duplex penthouses with a private roof terrace on the plans.',
  'Tres tipos de vivienda en un mismo recinto: apartamentos en primera planta desde €330000, apartamentos en planta baja con jardines de 55 a 220 [m2] y áticos dúplex con azotea privada según los planos.',
  'Trois types de logement sur un même site : appartements au premier étage à partir de €330000, appartements au rez-de-chaussée avec jardins de 55 à 220 [m2] et penthouses duplex avec toit-terrasse privé selon les plans.',
  'Drei Wohnungstypen in einer Anlage: Wohnungen im ersten Obergeschoss ab €330000, Erdgeschosswohnungen mit Gärten von 55 bis 220 [m2] und Maisonette-Penthäuser mit privater Dachterrasse laut Plänen.',
  'Три типа жилья на одной территории: квартиры на втором этаже от €330000, квартиры на первом этаже с садами от 55 до 220 [m2] и двухуровневые пентхаусы с частной кровельной террасой по планам.',
  'ثلاثة أنواع من المساكن في موقع واحد: شقق الطابق الأول ابتداءً من €330000، وشقق الطابق الأرضي بحدائق من 55 إلى 220 [m2]، وبنتهاوس دوبلكس بسطح خاص حسب المخططات.',
  'Drie soorten woningen op één terrein: appartementen op de eerste verdieping vanaf €330000, appartementen op de begane grond met tuinen van 55 tot 220 [m2] en duplex penthouses met een eigen dakterras volgens de plattegronden.',
  'Trzy rodzaje mieszkań na jednym terenie: mieszkania na pierwszym piętrze od €330000, mieszkania na parterze z ogrodami od 55 do 220 [m2] oraz dwupoziomowe penthouse’y z prywatnym tarasem dachowym według rzutów.',
  'Tre typer boliger på ett område: leiligheter i andre etasje fra €330000, leiligheter i første etasje med hager på 55 til 220 [m2] og duplex-toppleiligheter med privat takterrasse ifølge plantegningene.',
  'Tre typer av bostäder på ett område: lägenheter på första våningen från €330000, lägenheter på bottenvåningen med trädgårdar på 55 till 220 [m2] och duplex-takvåningar med privat takterrass enligt ritningarna.')
a('The brochure puts the development close to Estepona Golf and lists sea views, and the renders show the sea from the terraces. The documents give no distances, so we measure them with you on a visit.',
  'El folleto sitúa la promoción cerca de Estepona Golf y menciona vistas al mar, y las imágenes muestran el mar desde las terrazas. Los documentos no dan distancias, así que las medimos con usted en una visita.',
  'La brochure situe la résidence près d’Estepona Golf et mentionne une vue sur la mer, et les images montrent la mer depuis les terrasses. Les documents ne donnent aucune distance ; nous les mesurons avec vous lors d’une visite.',
  'Die Broschüre verortet die Anlage nahe Estepona Golf und nennt Meerblick, und die Visualisierungen zeigen das Meer von den Terrassen aus. Die Dokumente nennen keine Entfernungen; wir messen sie gemeinsam mit Ihnen bei einem Besuch.',
  'В брошюре комплекс расположен рядом с Estepona Golf и указан вид на море, а на визуализациях море видно с террас. В документах нет расстояний, поэтому мы измеряем их вместе с вами во время просмотра.',
  'يضع الكتيّب المشروع بالقرب من Estepona Golf ويذكر إطلالات على البحر، وتُظهر الصور البحر من التراسات. لا تذكر المستندات مسافات، لذلك نقيسها معكم خلال الزيارة.',
  'De brochure plaatst het project dichtbij Estepona Golf en noemt zeezicht, en de beelden tonen de zee vanaf de terrassen. De documenten vermelden geen afstanden, dus we meten ze samen met u tijdens een bezoek.',
  'Broszura umiejscawia inwestycję w pobliżu Estepona Golf i wymienia widok na morze, a wizualizacje pokazują morze z tarasów. Dokumenty nie podają odległości, więc mierzymy je razem z Państwem podczas wizyty.',
  'Brosjyren plasserer prosjektet nær Estepona Golf og nevner havutsikt, og bildene viser havet fra terrassene. Dokumentene oppgir ingen avstander, så vi måler dem på stedet under en visning.',
  'Broschyren placerar projektet nära Estepona Golf och nämner havsutsikt, och bilderna visar havet från terrasserna. Handlingarna anger inga avstånd, så vi mäter dem tillsammans med er vid ett besök.')
a('The sales portal, the brochure and the plans describe the stage of the project differently, and the built areas on the plans differ from the price list, so we confirm both in writing.',
  'El portal de ventas, el folleto y los planos describen de forma distinta la fase del proyecto, y las superficies construidas de los planos difieren de la lista de precios, así que confirmamos ambas cosas por escrito.',
  'Le portail de vente, la brochure et les plans décrivent différemment l’état d’avancement du projet, et les surfaces construites des plans diffèrent de la liste de prix ; nous confirmons donc les deux par écrit.',
  'Das Verkaufsportal, die Broschüre und die Pläne beschreiben den Projektstand unterschiedlich, und die bebauten Flächen in den Plänen weichen von der Preisliste ab; wir bestätigen daher beides schriftlich.',
  'Портал продаж, брошюра и планы по-разному описывают стадию проекта, а площади застройки на планах отличаются от прайс-листа, поэтому мы подтверждаем и то, и другое в письменном виде.',
  'تصف بوابة المبيعات والكتيّب والمخططات مرحلة المشروع بشكل مختلف، وتختلف المساحات المبنية في المخططات عن قائمة الأسعار، لذلك نؤكد الأمرين كتابةً.',
  'Het verkoopportaal, de brochure en de plattegronden beschrijven de projectfase verschillend, en de bebouwde oppervlaktes op de plattegronden wijken af van de prijslijst, dus we bevestigen beide schriftelijk.',
  'Portal sprzedażowy, broszura i rzuty opisują etap projektu w różny sposób, a powierzchnie zabudowy na rzutach różnią się od cennika, dlatego potwierdzamy jedno i drugie na piśmie.',
  'Salgsportalen, brosjyren og plantegningene beskriver prosjektets fase ulikt, og det bebygde arealet på plantegningene avviker fra prislisten, så vi bekrefter begge deler skriftlig.',
  'Försäljningsportalen, broschyren och planritningarna beskriver projektets fas olika, och byggytorna på planritningarna avviker från prislistan, så vi bekräftar båda skriftligen.')

# ---------------------------------------------------------------- architecture and specification
a('The renders show white apartment blocks with a terrace on every level, set around lawns and a communal pool. The plans show the living room, kitchen and dining area as one space opening onto a terrace, and the duplex penthouses with a staircase to a private roof terrace.',
  'Las imágenes muestran bloques de apartamentos blancos con una terraza en cada nivel, dispuestos alrededor de césped y una piscina comunitaria. Los planos muestran el salón, la cocina y el comedor como un único espacio que se abre a una terraza, y los áticos dúplex con una escalera a una azotea privada.',
  'Les images montrent des immeubles blancs avec une terrasse à chaque niveau, disposés autour de pelouses et d’une piscine commune. Les plans montrent le salon, la cuisine et la salle à manger en un seul espace ouvert sur une terrasse, et les penthouses duplex avec un escalier menant à un toit-terrasse privé.',
  'Die Visualisierungen zeigen weiße Wohnblöcke mit einer Terrasse auf jeder Ebene, angeordnet um Rasenflächen und einen Gemeinschaftspool. Die Pläne zeigen Wohnzimmer, Küche und Essbereich als einen Raum, der sich zu einer Terrasse öffnet, und die Maisonette-Penthäuser mit einer Treppe zu einer privaten Dachterrasse.',
  'На визуализациях — белые многоквартирные дома с террасой на каждом уровне, расположенные вокруг газонов и общего бассейна. На планах гостиная, кухня и столовая образуют единое пространство с выходом на террасу, а двухуровневые пентхаусы имеют лестницу на частную кровельную террасу.',
  'تُظهر الصور مبانيَ سكنية بيضاء بتراس في كل طابق، تحيط بها مروج ومسبح مشترك. وتُظهر المخططات غرفة المعيشة والمطبخ ومنطقة الطعام كمساحة واحدة تفتح على تراس، وبنتهاوس الدوبلكس بسلّم يؤدي إلى سطح خاص.',
  'De beelden tonen witte appartementsblokken met op elke verdieping een terras, rond grasvelden en een gemeenschappelijk zwembad. De plattegronden tonen woonkamer, keuken en eethoek als één ruimte die uitkomt op een terras, en de duplex penthouses met een trap naar een eigen dakterras.',
  'Wizualizacje pokazują białe budynki mieszkalne z tarasem na każdej kondygnacji, rozmieszczone wokół trawników i wspólnego basenu. Rzuty pokazują salon, kuchnię i jadalnię jako jedną przestrzeń otwartą na taras oraz dwupoziomowe penthouse’y ze schodami na prywatny taras dachowy.',
  'Bildene viser hvite leilighetsbygg med en terrasse i hver etasje, rundt plener og et felles basseng. Plantegningene viser stue, kjøkken og spiseplass som ett rom som åpner seg mot en terrasse, og duplex-toppleilighetene med en trapp til en privat takterrasse.',
  'Bilderna visar vita flerbostadshus med en terrass på varje våning, kring gräsmattor och en gemensam pool. Planritningarna visar vardagsrum, kök och matplats som ett rum som öppnar sig mot en terrass, och duplex-takvåningarna med en trappa till en privat takterrass.')
a('The brochure lists an aerothermal system, a furnished kitchen and a balcony or terrace for the homes, and sea views for the development.',
  'El folleto indica para las viviendas un sistema de aerotermia, una cocina amueblada y un balcón o terraza, y para la promoción vistas al mar.',
  'La brochure mentionne pour les logements un système aérothermique, une cuisine meublée et un balcon ou une terrasse, et pour la résidence une vue sur la mer.',
  'Die Broschüre nennt für die Wohnungen eine Luft-Wasser-Wärmepumpe, eine möblierte Küche und einen Balkon oder eine Terrasse und für die Anlage Meerblick.',
  'В брошюре для квартир указаны аэротермальная система, кухня с мебелью и балкон или терраса, а для комплекса — вид на море.',
  'يذكر الكتيّب للمساكن نظامًا حراريًا هوائيًا ومطبخًا مجهزًا بالأثاث وشرفة أو تراسًا، وللمشروع إطلالات على البحر.',
  'De brochure noemt voor de woningen een aerothermisch systeem, een gemeubileerde keuken en een balkon of terras, en voor het project zeezicht.',
  'Broszura wymienia dla mieszkań system aerotermalny, umeblowaną kuchnię i balkon lub taras, a dla inwestycji widok na morze.',
  'Brosjyren oppgir for boligene et aerotermisk system, et møblert kjøkken og en balkong eller terrasse, og for prosjektet havutsikt.',
  'Broschyren anger för bostäderna ett aerotermiskt system, ett möblerat kök och en balkong eller terrass, och för projektet havsutsikt.')
a('Brickwork rendered on the outside to the facade design, with internal thermal insulation and a plasterboard lining on a metal frame.',
  'Fábrica de ladrillo revestida al exterior según el diseño de la fachada, con aislamiento térmico interior y un trasdosado de yeso laminado sobre perfiles metálicos.',
  'Maçonnerie de briques revêtue à l’extérieur selon le dessin de la façade, avec isolation thermique intérieure et doublage en plaques de plâtre sur ossature métallique.',
  'Ziegelmauerwerk, außen nach dem Fassadendesign verkleidet, mit innenliegender Wärmedämmung und einer Gipskartonvorsatzschale auf Metallprofilen.',
  'Кирпичная кладка с наружной отделкой по дизайну фасада, внутренней теплоизоляцией и облицовкой гипсокартоном на металлическом каркасе.',
  'بناء من الطوب مكسوّ من الخارج وفق تصميم الواجهة، مع عزل حراري داخلي وتبطين من ألواح الجبس على هيكل معدني.',
  'Bakstenen metselwerk, aan de buitenzijde afgewerkt volgens het gevelontwerp, met thermische isolatie aan de binnenzijde en een voorzetwand van gipsplaten op een metalen frame.',
  'Mur z cegły z wykończeniem zewnętrznym zgodnym z projektem elewacji, z izolacją termiczną od wewnątrz i obudową z płyt gipsowo-kartonowych na stelażu metalowym.',
  'Teglmurverk kledd på utsiden etter fasadedesignet, med varmeisolasjon på innsiden og en gipsplatekledning på metallramme.',
  'Tegelmurverk med utvändig beklädnad enligt fasaddesignen, med invändig värmeisolering och en gipsskiva på metallstomme.')
a('Source: the developer’s quality specification, version V-0.2 dated 5 June 2024. It is provisional and may change with licensing requirements or the criteria of the project management, without compromising quality.',
  'Fuente: la memoria de calidades del promotor, versión V-0.2 de 5 de junio de 2024. Es provisional y puede cambiar por requisitos de la licencia o por criterio de la dirección facultativa, sin menoscabo de la calidad.',
  'Source : le descriptif de qualité du promoteur, version V-0.2 du 5 juin 2024. Il est provisoire et peut évoluer selon les exigences du permis ou l’appréciation de la maîtrise d’œuvre, sans nuire à la qualité.',
  'Quelle: die Bau- und Ausstattungsbeschreibung des Bauträgers, Version V-0.2 vom 5. Juni 2024. Sie ist vorläufig und kann sich aufgrund von Genehmigungsauflagen oder nach Ermessen der Bauleitung ändern, ohne die Qualität zu beeinträchtigen.',
  'Источник: описание качества отделки застройщика, версия V-0.2 от 5 июня 2024 года. Оно предварительное и может измениться по требованиям разрешения или по решению технического руководства без снижения качества.',
  'المصدر: مواصفات الجودة الخاصة بالمطوّر، النسخة V-0.2 بتاريخ 5 يونيو 2024. وهي مؤقتة وقد تتغير بسبب متطلبات الرخصة أو بتقدير إدارة المشروع دون الإخلال بالجودة.',
  'Bron: de kwaliteitsomschrijving van de ontwikkelaar, versie V-0.2 van 5 juni 2024. Deze is voorlopig en kan wijzigen door vergunningseisen of naar het oordeel van de projectleiding, zonder afbreuk te doen aan de kwaliteit.',
  'Źródło: opis jakości wykonania dewelopera, wersja V-0.2 z 5 czerwca 2024 r. Jest on wstępny i może ulec zmianie z powodu wymogów pozwolenia lub decyzji kierownictwa projektu, bez obniżenia jakości.',
  'Kilde: utbyggerens kvalitetsbeskrivelse, versjon V-0.2 datert 5. juni 2024. Den er foreløpig og kan endres på grunn av krav i tillatelsen eller etter prosjektledelsens skjønn, uten at kvaliteten svekkes.',
  'Källa: exploatörens kvalitetsbeskrivning, version V-0.2 daterad den 5 juni 2024. Den är preliminär och kan ändras på grund av krav i bygglovet eller efter projektledningens bedömning, utan att kvaliteten försämras.')
a('Stoneware ceramic flooring throughout with a matching skirting, first-quality ceramic tiling in the bathrooms and the kitchen, and smooth false ceilings where services run, with an accessible false ceiling in the bathroom for the air-conditioning unit.',
  'Pavimento cerámico de gres en toda la vivienda con rodapié a juego, alicatado cerámico de primera calidad en baños y cocina, y falsos techos lisos por donde discurren las instalaciones, con un falso techo registrable en el baño para la máquina de climatización.',
  'Carrelage en grès cérame dans tout le logement avec plinthes assorties, faïence de première qualité dans les salles de bain et la cuisine, et faux plafonds lisses là où passent les installations, avec un faux plafond démontable dans la salle de bain pour l’unité de climatisation.',
  'Keramischer Steinzeugboden in der gesamten Wohnung mit passender Sockelleiste, hochwertige Fliesen in Bädern und Küche sowie glatte abgehängte Decken dort, wo Installationen verlaufen, mit einer zugänglichen abgehängten Decke im Bad für das Klimagerät.',
  'Керамогранитные полы во всей квартире с подходящим плинтусом, керамическая плитка первого сорта в ванных комнатах и на кухне, гладкие подвесные потолки там, где проходят коммуникации, и съёмный подвесной потолок в ванной для климатического оборудования.',
  'أرضيات من الحجر الخزفي في كل المسكن مع قوائم سفلية متناسقة، وبلاط خزفي من الدرجة الأولى في الحمامات والمطبخ، وأسقف مستعارة ملساء حيث تمر التمديدات، مع سقف مستعار قابل للفتح في الحمام لوحدة التكييف.',
  'Keramische gresvloer in de hele woning met bijpassende plint, keramische tegels van eerste kwaliteit in de badkamers en de keuken, en gladde verlaagde plafonds waar installaties lopen, met een toegankelijk verlaagd plafond in de badkamer voor de airconditioning.',
  'Posadzki z gresu ceramicznego w całym mieszkaniu z pasującymi listwami przypodłogowymi, płytki ceramiczne pierwszej jakości w łazienkach i kuchni oraz gładkie sufity podwieszane tam, gdzie biegną instalacje, z rewizyjnym sufitem podwieszanym w łazience na urządzenie klimatyzacyjne.',
  'Keramisk gresgulv i hele boligen med matchende gulvlister, flis av førsteklasses kvalitet på bad og kjøkken, og glatte nedforede tak der installasjonene går, med et tilgjengelig nedforet tak på badet for klimaanlegget.',
  'Keramiskt stengodsgolv i hela bostaden med matchande golvlister, kakel av förstklassig kvalitet i badrum och kök, och släta undertak där installationerna går, med ett åtkomligt undertak i badrummet för klimatenheten.')
a('Smooth plastic paint in a soft colour on the interior walls and in white on the ceilings.',
  'Pintura plástica lisa de color suave en las paredes interiores y blanca en los techos.',
  'Peinture plastique lisse de teinte douce sur les murs intérieurs et blanche sur les plafonds.',
  'Glatte Kunststoffdispersionsfarbe in einem sanften Farbton an den Innenwänden und in Weiß an den Decken.',
  'Гладкая акриловая краска мягкого цвета на внутренних стенах и белая на потолках.',
  'دهان بلاستيكي أملس بلون هادئ على الجدران الداخلية وأبيض على الأسقف.',
  'Gladde kunststofverf in een zachte kleur op de binnenmuren en in wit op de plafonds.',
  'Gładka farba plastyczna w łagodnym kolorze na ścianach wewnętrznych i biała na sufitach.',
  'Glatt plastmaling i en myk farge på innvendige vegger og i hvitt i taket.',
  'Slät plastfärg i en mjuk kulör på innerväggarna och vit i taken.')
a('An armoured white-lacquered front door with security fittings, an outside handle and an optical peephole, flat-panel lacquered interior doors, and modular wardrobes, hinged or sliding by home type, with a melamine interior, a luggage shelf and a hanging rail.',
  'Puerta de entrada blindada lacada en blanco con herrajes de seguridad, tirador exterior y mirilla óptica, puertas de paso lacadas de hoja plana y armarios modulares, abatibles o correderos según el tipo de vivienda, con interior de melamina, balda de maletero y barra de colgar.',
  'Porte d’entrée blindée laquée blanc avec quincaillerie de sécurité, poignée extérieure et judas optique, portes intérieures laquées à panneau plat et placards modulaires, battants ou coulissants selon le type de logement, avec intérieur en mélaminé, tablette à bagages et barre de penderie.',
  'Gepanzerte weiß lackierte Wohnungseingangstür mit Sicherheitsbeschlägen, Außengriff und optischem Türspion, lackierte Innentüren mit glattem Türblatt und modulare Einbauschränke, je nach Wohnungstyp mit Dreh- oder Schiebetüren, mit Melamin-Innenausstattung, Hutablage und Kleiderstange.',
  'Бронированная входная дверь, окрашенная в белый цвет, с защитной фурнитурой, наружной ручкой и оптическим глазком, окрашенные гладкие межкомнатные двери и модульные шкафы с распашными или раздвижными дверями в зависимости от типа квартиры, с меламиновой отделкой внутри, полкой для чемоданов и штангой для вешалок.',
  'باب دخول مصفّح مطلي بالأبيض بتجهيزات أمان ومقبض خارجي وعين سحرية بصرية، وأبواب داخلية مطلية بسطح أملس، وخزائن مجمّعة بأبواب مفصلية أو منزلقة بحسب نوع المسكن، بداخل من الميلامين ورف للحقائب وعمود لتعليق الملابس.',
  'Gepantserde wit gelakte voordeur met veiligheidsbeslag, een buitenhandgreep en een optische deurspion, gelakte vlakke binnendeuren en modulaire kasten, naar gelang van het woningtype met draai- of schuifdeuren, met een melamine binnenkant, een bagageplank en een kledingstang.',
  'Pancerne drzwi wejściowe lakierowane na biało z okuciami zabezpieczającymi, klamką zewnętrzną i wizjerem optycznym, lakierowane gładkie drzwi wewnętrzne oraz modułowe szafy z drzwiami uchylnymi lub przesuwnymi, zależnie od typu mieszkania, z melaminowanym wnętrzem, półką na walizki i drążkiem na wieszaki.',
  'Pansret hvitlakkert inngangsdør med sikkerhetsbeslag, utvendig håndtak og optisk dørspion, lakkerte innerdører med slett blad og modulære garderobeskap, med slagdører eller skyvedører avhengig av boligtype, med melamininteriør, bagasjehylle og kleshenger.',
  'Pansrad vitlackerad ytterdörr med säkerhetsbeslag, utvändigt handtag och optisk titthål, lackerade innerdörrar med slätt dörrblad och modulgarderober, med svängda eller skjutbara dörrar beroende på bostadstyp, med melaminyta invändigt, hatthylla och klädstång.')
a('A furnished kitchen with a compact-material worktop, a stainless-steel sink and a single-lever tap, laid out according to the home type.',
  'Cocina amueblada con encimera de material compacto, fregadero de acero inoxidable y grifería monomando, con distribución según el tipo de vivienda.',
  'Cuisine meublée avec plan de travail en matériau compact, évier en inox et mitigeur monocommande, agencée selon le type de logement.',
  'Möblierte Küche mit Arbeitsplatte aus Kompaktmaterial, Edelstahlspüle und Einhebelarmatur, je nach Wohnungstyp angeordnet.',
  'Кухня с мебелью, столешницей из компактного материала, мойкой из нержавеющей стали и однорычажным смесителем; планировка зависит от типа квартиры.',
  'مطبخ مجهز بالأثاث مع سطح عمل من مادة مضغوطة وحوض من الفولاذ المقاوم للصدأ وحنفية أحادية الذراع، بتوزيع يختلف بحسب نوع المسكن.',
  'Gemeubileerde keuken met een werkblad van compact materiaal, een roestvrijstalen spoelbak en een eengreepskraan, ingedeeld naar woningtype.',
  'Umeblowana kuchnia z blatem z materiału kompaktowego, zlewem ze stali nierdzewnej i baterią jednouchwytową, z układem zależnym od typu mieszkania.',
  'Møblert kjøkken med benkeplate i kompaktmateriale, en vask i rustfritt stål og en énhåndtaksarmatur, innredet etter boligtype.',
  'Möblerat kök med bänkskiva i kompaktmaterial, en diskho i rostfritt stål och en enhandsblandare, utformat efter bostadstyp.')
a('Appliances included: an electric oven, an induction hob, a pull-out extractor hood, a fridge and a dishwasher.',
  'Electrodomésticos incluidos: horno eléctrico, placa de inducción, campana extraíble, frigorífico y lavavajillas.',
  'Électroménager inclus : four électrique, plaque à induction, hotte escamotable, réfrigérateur et lave-vaisselle.',
  'Enthaltene Geräte: Elektrobackofen, Induktionskochfeld, ausziehbare Dunstabzugshaube, Kühlschrank und Geschirrspüler.',
  'Техника в комплекте: электрический духовой шкаф, индукционная варочная панель, выдвижная вытяжка, холодильник и посудомоечная машина.',
  'الأجهزة المشمولة: فرن كهربائي وموقد حثّي وشفاط قابل للسحب وثلاجة وغسالة أطباق.',
  'Inbegrepen apparaten: een elektrische oven, een inductiekookplaat, een uittrekbare afzuigkap, een koelkast en een vaatwasser.',
  'W cenie urządzenia: piekarnik elektryczny, płyta indukcyjna, wysuwany okap, lodówka i zmywarka.',
  'Apparater inkludert: elektrisk ovn, induksjonstopp, uttrekkbar kjøkkenvifte, kjøleskap og oppvaskmaskin.',
  'Apparater som ingår: elugn, induktionshäll, utdragbar köksfläkt, kylskåp och diskmaskin.')
a('White sanitaryware, extra-flat shower trays, a screen and a thermostatic shower tap in the main bathroom, single-lever taps in the second bathroom and at the basins, a vanity unit with a basin in the main bathroom, and mirrors in the bathrooms.',
  'Aparatos sanitarios blancos, platos de ducha extraplanos, mampara y grifería termostática en la ducha del baño principal, grifería monomando en el segundo baño y en los lavabos, mueble con lavabo en el baño principal y espejos en los baños.',
  'Appareils sanitaires blancs, receveurs de douche extraplats, paroi et mitigeur thermostatique dans la douche de la salle de bain principale, mitigeurs monocommande dans la seconde salle de bain et aux lavabos, meuble-vasque dans la salle de bain principale et miroirs dans les salles de bain.',
  'Weiße Sanitärobjekte, extraflache Duschwannen, eine Duschabtrennung und eine Thermostatarmatur in der Dusche des Hauptbads, Einhebelarmaturen im zweiten Bad und an den Waschbecken, ein Waschtischunterschrank im Hauptbad und Spiegel in den Bädern.',
  'Белая сантехника, сверхплоские душевые поддоны, душевое ограждение и термостатический смеситель в душе главной ванной, однорычажные смесители во второй ванной и у раковин, тумба с раковиной в главной ванной и зеркала в ванных комнатах.',
  'أدوات صحية بيضاء وقواعد دش شديدة الانبساط وحاجز دش وحنفية ثرموستاتية في دش الحمام الرئيسي، وحنفيات أحادية الذراع في الحمام الثاني وعند المغاسل، ووحدة مغسلة في الحمام الرئيسي ومرايا في الحمامات.',
  'Wit sanitair, extra platte douchebakken, een douchewand en een thermostatische doucheknop in de hoofdbadkamer, eengreepskranen in de tweede badkamer en bij de wastafels, een wastafelmeubel in de hoofdbadkamer en spiegels in de badkamers.',
  'Biała ceramika sanitarna, bardzo płaskie brodziki, kabina i bateria termostatyczna prysznica w łazience głównej, baterie jednouchwytowe w drugiej łazience i przy umywalkach, szafka z umywalką w łazience głównej oraz lustra w łazienkach.',
  'Hvitt sanitærutstyr, ekstra flate dusjkar, en dusjvegg og en termostatarmatur i dusjen på hovedbadet, énhåndtaksarmaturer på det andre badet og ved vaskene, en servantskap med vask på hovedbadet og speil på badene.',
  'Vitt sanitetsporslin, extra låga duschkar, en duschvägg och en termostatblandare i duschen i huvudbadrummet, enhandsblandare i det andra badrummet och vid handfaten, ett tvättställsskåp i huvudbadrummet och speglar i badrummen.')
a('Taps on the terraces of the ground-floor homes and the penthouses, depending on the type.',
  'Grifería en las terrazas de las viviendas de planta baja y de los áticos, según el tipo.',
  'Robinets sur les terrasses des logements du rez-de-chaussée et des penthouses, selon le type.',
  'Wasserhähne auf den Terrassen der Erdgeschosswohnungen und der Penthäuser, je nach Typ.',
  'Краны на террасах квартир первого этажа и пентхаусов, в зависимости от типа.',
  'حنفيات على تراسات مساكن الطابق الأرضي والبنتهاوس بحسب النوع.',
  'Kranen op de terrassen van de woningen op de begane grond en de penthouses, naargelang het type.',
  'Krany na tarasach mieszkań na parterze i penthouse’ów, zależnie od typu.',
  'Kraner på terrassene til boligene i første etasje og toppleilighetene, avhengig av typen.',
  'Kranar på terrasserna till bostäderna på bottenvåningen och takvåningarna, beroende på typ.')
a('An individual aerothermal system for hot water, and air conditioning by a heat pump for cooling and heating, through ducts with grilles in the living room and bedrooms, with an indoor and an outdoor unit.',
  'Un sistema individual de aerotermia para el agua caliente y aire acondicionado por bomba de calor para frío y calor, mediante conductos con rejillas en el salón y los dormitorios, con unidad interior y exterior.',
  'Un système aérothermique individuel pour l’eau chaude et une climatisation par pompe à chaleur pour le froid et le chaud, par gaines avec grilles dans le séjour et les chambres, avec une unité intérieure et une unité extérieure.',
  'Eine individuelle Luft-Wasser-Wärmepumpe für das Warmwasser und eine Klimaanlage mit Wärmepumpe zum Kühlen und Heizen über Kanäle mit Gittern in Wohnzimmer und Schlafzimmern, mit Innen- und Außengerät.',
  'Индивидуальная аэротермальная система для горячей воды и кондиционирование тепловым насосом на охлаждение и обогрев по воздуховодам с решётками в гостиной и спальнях, с внутренним и наружным блоками.',
  'نظام حراري هوائي مستقل للماء الساخن، وتكييف بمضخة حرارية للتبريد والتدفئة عبر مجارٍ بشبكات في غرفة المعيشة وغرف النوم، مع وحدة داخلية وأخرى خارجية.',
  'Een individueel aerothermisch systeem voor warm water en airconditioning met een warmtepomp voor koeling en verwarming, via kanalen met roosters in de woonkamer en de slaapkamers, met een binnen- en een buitenunit.',
  'Indywidualny system aerotermalny do ciepłej wody oraz klimatyzacja z pompą ciepła do chłodzenia i ogrzewania, kanałami z kratkami w salonie i sypialniach, z jednostką wewnętrzną i zewnętrzną.',
  'Et eget aerotermisk system for varmtvann og klimaanlegg med varmepumpe for kjøling og oppvarming, via kanaler med ventiler i stuen og soverommene, med en innendørs og en utendørs enhet.',
  'Ett eget aerotermiskt system för varmvatten och luftkonditionering med värmepump för kyla och värme, via kanaler med galler i vardagsrum och sovrum, med en inomhus- och en utomhusenhet.')
a('The development is shown with an energy rating of B for consumption and for emissions at project stage, which is informative and provisional.',
  'La promoción figura con una calificación energética B de consumo y de emisiones en fase de proyecto, que es meramente informativa y provisional.',
  'La résidence est présentée avec une classe énergétique B pour la consommation et pour les émissions au stade du projet, à titre informatif et provisoire.',
  'Die Anlage ist im Projektstadium mit der Energieeffizienzklasse B für Verbrauch und Emissionen ausgewiesen, rein informativ und vorläufig.',
  'Для комплекса на стадии проекта указан класс энергоэффективности B по потреблению и по выбросам; он носит информационный и предварительный характер.',
  'يظهر المشروع بتصنيف طاقة B للاستهلاك وللانبعاثات في مرحلة المشروع، وهو للعلم فقط ومؤقت.',
  'Het project wordt in de projectfase getoond met energielabel B voor verbruik en voor emissies, uitsluitend ter informatie en voorlopig.',
  'Inwestycja jest przedstawiona w fazie projektu z klasą energetyczną B dla zużycia i dla emisji, wyłącznie informacyjnie i wstępnie.',
  'Prosjektet er vist med energimerke B for forbruk og for utslipp på prosjektstadiet, kun til informasjon og foreløpig.',
  'Projektet redovisas på projektstadiet med energiklass B för förbrukning och för utsläpp, endast som information och preliminärt.')
a('An electrical installation to the low-voltage regulations, telecoms sockets in the living room, bedrooms, kitchen and terrace, an automatic video intercom at the entrances to the development and an intercom at each portal, and a photovoltaic contribution to the communal services.',
  'Instalación eléctrica conforme al Reglamento Electrotécnico de Baja Tensión, tomas de telecomunicaciones en el salón, los dormitorios, la cocina y la terraza, videoportero automático en los accesos a la urbanización y portero automático en cada portal, y aporte de energía fotovoltaica a los servicios comunitarios.',
  'Installation électrique conforme à la réglementation basse tension, prises de télécommunications dans le séjour, les chambres, la cuisine et sur la terrasse, visiophone automatique aux accès de la résidence et interphone dans chaque cage, et apport d’énergie photovoltaïque aux services communs.',
  'Elektroinstallation nach der Niederspannungsverordnung, Telekommunikationsanschlüsse in Wohnzimmer, Schlafzimmern, Küche und auf der Terrasse, eine automatische Videosprechanlage an den Zugängen zur Anlage und eine Sprechanlage an jedem Aufgang sowie ein Photovoltaikbeitrag für die Gemeinschaftsdienste.',
  'Электропроводка по нормам для низкого напряжения, телекоммуникационные розетки в гостиной, спальнях, на кухне и на террасе, автоматический видеодомофон на входах в комплекс и домофон в каждом подъезде, а также фотоэлектрическая энергия для общих служб.',
  'تمديدات كهربائية وفق لوائح الجهد المنخفض، ومآخذ اتصالات في غرفة المعيشة وغرف النوم والمطبخ والتراس، ونظام اتصال مرئي آلي عند مداخل المشروع ونظام اتصال داخلي عند كل مدخل، ومساهمة من الطاقة الكهروضوئية في الخدمات المشتركة.',
  'Elektrische installatie volgens de laagspanningsregelgeving, telecomaansluitingen in de woonkamer, de slaapkamers, de keuken en op het terras, een automatische video-intercom bij de toegangen tot het project en een intercom bij elke portiek, en een fotovoltaïsche bijdrage aan de gemeenschappelijke voorzieningen.',
  'Instalacja elektryczna zgodna z przepisami niskiego napięcia, gniazda telekomunikacyjne w salonie, sypialniach, kuchni i na tarasie, automatyczny wideodomofon przy wejściach na teren inwestycji i domofon na każdej klatce oraz energia fotowoltaiczna zasilająca części wspólne.',
  'Elektrisk installasjon etter lavspenningsforskriften, telekommunikasjonsuttak i stuen, soverommene, kjøkkenet og på terrassen, en automatisk videoport ved inngangene til prosjektet og en porttelefon ved hver oppgang, og et solcellebidrag til fellestjenestene.',
  'Elinstallation enligt lågspänningsreglerna, telekommunikationsuttag i vardagsrum, sovrum, kök och på terrassen, en automatisk videoporttelefon vid projektets entréer och en porttelefon vid varje port, samt ett solcellsbidrag till de gemensamma tjänsterna.')
a('Walls and sound', 'Paredes y aislamiento acústico', 'Murs et isolation phonique', 'Wände und Schallschutz',
  'Стены и звукоизоляция', 'الجدران والعزل الصوتي', 'Wanden en geluidsisolatie', 'Ściany i izolacja akustyczna',
  'Vegger og lydisolasjon', 'Väggar och ljudisolering')
a('Interior partitions of plasterboard on a metal frame with thermal and acoustic insulation, and walls between homes of brickwork with a plasterboard lining and thermal and acoustic insulation on both faces.',
  'Tabiquería interior de yeso laminado sobre estructura metálica con aislamiento térmico y acústico, y separaciones entre viviendas de fábrica con trasdosado de yeso laminado y aislamiento térmico y acústico en ambas caras.',
  'Cloisons intérieures en plaques de plâtre sur ossature métallique avec isolation thermique et acoustique, et murs entre logements en maçonnerie avec doublage en plaques de plâtre et isolation thermique et acoustique sur les deux faces.',
  'Innenwände aus Gipskarton auf Metallständern mit Wärme- und Schalldämmung sowie Wohnungstrennwände aus Mauerwerk mit Gipskarton-Vorsatzschale und Wärme- und Schalldämmung auf beiden Seiten.',
  'Внутренние перегородки из гипсокартона на металлическом каркасе с тепло- и звукоизоляцией, а стены между квартирами — кирпичная кладка с гипсокартонной облицовкой и тепло- и звукоизоляцией с обеих сторон.',
  'حواجز داخلية من ألواح الجبس على هيكل معدني مع عزل حراري وصوتي، وجدران فاصلة بين المساكن من الطوب مع تبطين بألواح الجبس وعزل حراري وصوتي على الوجهين.',
  'Binnenwanden van gipsplaat op een metalen frame met thermische en akoestische isolatie, en woningscheidende muren van metselwerk met een voorzetwand van gipsplaat en thermische en akoestische isolatie aan beide zijden.',
  'Przegrody wewnętrzne z płyt gipsowo-kartonowych na stelażu metalowym z izolacją termiczną i akustyczną oraz ściany między mieszkaniami z muru z obudową z płyt gipsowo-kartonowych i izolacją termiczną i akustyczną z obu stron.',
  'Innvendige skillevegger av gipsplater på metallramme med varme- og lydisolasjon, og vegger mellom boliger av murverk med gipsplatekledning og varme- og lydisolasjon på begge sider.',
  'Invändiga mellanväggar av gipsskivor på metallstomme med värme- och ljudisolering, och väggar mellan bostäder av murverk med gipsskiva och värme- och ljudisolering på båda sidor.')
a('A fully enclosed and fenced residential complex with low-energy lighting at the entrances, on the internal roads and in the gardens, and landscaped areas with lawns, trees and shrubs.',
  'Conjunto residencial totalmente cerrado y vallado, con iluminación de bajo consumo en los accesos, los viales interiores y los jardines, y zonas ajardinadas con césped, árboles y arbustos.',
  'Ensemble résidentiel entièrement clos et clôturé, avec un éclairage basse consommation aux accès, sur les voies intérieures et dans les jardins, et des espaces paysagers avec pelouses, arbres et arbustes.',
  'Eine vollständig umschlossene und eingezäunte Wohnanlage mit energiesparender Beleuchtung an den Zugängen, auf den Anlagenwegen und in den Gärten sowie angelegten Flächen mit Rasen, Bäumen und Sträuchern.',
  'Полностью закрытый и огороженный жилой комплекс с энергосберегающим освещением на входах, внутренних проездах и в садах, а также озеленённые территории с газонами, деревьями и кустарниками.',
  'مجمّع سكني مغلق ومسوّر بالكامل مع إضاءة منخفضة الاستهلاك عند المداخل وعلى الطرق الداخلية وفي الحدائق، ومساحات مزروعة بالمروج والأشجار والشجيرات.',
  'Een volledig omheind en afgesloten woonproject met energiezuinige verlichting bij de toegangen, op de interne wegen en in de tuinen, en aangelegde zones met gazon, bomen en struiken.',
  'W pełni ogrodzony i zamknięty zespół mieszkaniowy z energooszczędnym oświetleniem przy wejściach, na drogach wewnętrznych i w ogrodach oraz zagospodarowane tereny z trawnikami, drzewami i krzewami.',
  'Et fullstendig lukket og inngjerdet boligområde med lavenergibelysning ved inngangene, på de interne veiene og i hagene, og opparbeidede områder med plen, trær og busker.',
  'Ett helt slutet och inhägnat bostadsområde med lågenergibelysning vid entréerna, på de interna vägarna och i trädgårdarna, och anlagda ytor med gräsmattor, träd och buskar.')
a('An outdoor communal pool with night lighting and salt chlorination, a gastroteca space and multi-sport courts in the communal area, power pre-installed in the basements for electric-car charging according to regulations, and limited places for buggies.',
  'Piscina comunitaria exterior con iluminación nocturna y cloración salina, una zona gastroteca y pistas multideporte en la zona comunitaria, preinstalación de potencia en los sótanos para la carga de vehículos eléctricos según la normativa y plazas limitadas para buggies.',
  'Piscine commune extérieure avec éclairage nocturne et chloration au sel, un espace gastroteca et des terrains multisports dans la zone commune, une pré-installation de puissance dans les sous-sols pour la recharge des véhicules électriques conformément à la réglementation, et des places limitées pour les voiturettes.',
  'Ein Gemeinschaftspool im Freien mit Nachtbeleuchtung und Salzchlorung, ein Gastroteca-Bereich und Multisportplätze im Gemeinschaftsbereich, eine vorschriftsmäßige Leistungsvorinstallation in den Untergeschossen für das Laden von Elektrofahrzeugen und begrenzte Plätze für Buggys.',
  'Общий открытый бассейн с ночной подсветкой и солевой хлоринацией, пространство «гастротека» и многофункциональные спортивные площадки в общей зоне, предварительно подведённая мощность в подвалах для зарядки электромобилей в соответствии с нормами и ограниченное число мест для гольф-каров.',
  'مسبح مشترك خارجي بإضاءة ليلية وكلورة ملحية، ومساحة «غاستروتيكا» وملاعب متعددة الرياضات في المنطقة المشتركة، وتجهيز مسبق للقدرة الكهربائية في الأقبية لشحن السيارات الكهربائية وفق اللوائح، وأماكن محدودة لعربات الغولف.',
  'Een gemeenschappelijk buitenzwembad met nachtverlichting en zoutchlorering, een gastroteca-ruimte en multisportvelden in de gemeenschappelijke zone, een volgens de regelgeving voorbereide aansluiting in de kelders voor het laden van elektrische auto’s en beperkte plaatsen voor buggy’s.',
  'Wspólny basen zewnętrzny z oświetleniem nocnym i chlorowaniem solnym, przestrzeń gastroteca i boiska wielofunkcyjne w strefie wspólnej, wstępnie przygotowana moc w podziemiach do ładowania pojazdów elektrycznych zgodnie z przepisami oraz ograniczona liczba miejsc na meleksy.',
  'Et felles utendørsbasseng med nattbelysning og saltklorering, et gastroteca-område og flerbruksbaner i fellesområdet, forhåndsinstallert effekt i kjellerne til lading av elbiler i samsvar med regelverket, og et begrenset antall plasser til golfbiler.',
  'En gemensam utomhuspool med nattbelysning och saltklorering, en gastroteca-yta och multisportplaner i det gemensamma området, förinstallerad effekt i källarna för laddning av elbilar enligt reglerna och ett begränsat antal platser för golfbilar.')
a('The buyer can choose between finishing options for the general flooring, the bathroom tiling and flooring and the kitchen worktop, up to a deadline set by the progress of the works.',
  'El comprador puede elegir entre distintas opciones de acabado para el solado general, el alicatado y el solado de los baños y la encimera de la cocina, hasta una fecha límite que depende del avance de las obras.',
  'L’acheteur peut choisir entre plusieurs finitions pour le sol général, le carrelage mural et le sol des salles de bain et le plan de travail de la cuisine, jusqu’à une date limite fixée selon l’avancement des travaux.',
  'Der Käufer kann zwischen verschiedenen Ausführungen für den allgemeinen Bodenbelag, die Wand- und Bodenfliesen der Bäder und die Küchenarbeitsplatte wählen, bis zu einer Frist, die sich nach dem Baufortschritt richtet.',
  'Покупатель может выбрать варианты отделки общего напольного покрытия, плитки и пола в ванных комнатах и столешницы на кухне до срока, зависящего от хода строительных работ.',
  'يمكن للمشتري الاختيار بين خيارات تشطيب للأرضيات العامة وبلاط وأرضيات الحمامات وسطح عمل المطبخ، حتى موعد نهائي يحدده تقدم الأعمال.',
  'De koper kan kiezen uit verschillende afwerkingen voor de algemene vloer, de wandtegels en vloertegels in de badkamers en het keukenwerkblad, tot een uiterste datum die afhangt van de voortgang van de werken.',
  'Kupujący może wybrać spośród wariantów wykończenia ogólnej posadzki, płytek i posadzek w łazienkach oraz blatu kuchennego, do terminu zależnego od postępu prac.',
  'Kjøperen kan velge mellom ulike utførelser for det generelle gulvet, flis og gulv på badene og kjøkkenbenkeplaten, frem til en frist som avhenger av byggets fremdrift.',
  'Köparen kan välja mellan olika utföranden för det allmänna golvet, kakel och golv i badrummen och köksbänkskivan, fram till en tidsgräns som styrs av arbetenas framskridande.')

# ---------------------------------------------------------------- residences
a('The 16 listed homes fall into three groups: ground-floor apartments with gardens, first-floor apartments and duplex penthouses. The table below lists each one with its price.',
  'Las 16 viviendas a la venta se dividen en tres grupos: apartamentos con jardín en planta baja, apartamentos en primera planta y áticos dúplex. La tabla siguiente recoge cada una con su precio.',
  'Les 16 logements annoncés se répartissent en trois groupes : appartements avec jardin au rez-de-chaussée, appartements au premier étage et penthouses duplex. Le tableau ci-dessous les présente un à un avec leur prix.',
  'Die 16 gelisteten Wohnungen gliedern sich in drei Gruppen: Erdgeschosswohnungen mit Garten, Wohnungen im ersten Obergeschoss und Maisonette-Penthäuser. Die Tabelle unten führt jede einzelne mit ihrem Preis auf.',
  'Шестнадцать квартир в продаже делятся на три группы: квартиры с садом на первом этаже, квартиры на втором этаже и двухуровневые пентхаусы. В таблице ниже приведена каждая из них с ценой.',
  'تنقسم المساكن الـ16 المعروضة إلى ثلاث مجموعات: شقق بحدائق في الطابق الأرضي وشقق في الطابق الأول وبنتهاوس دوبلكس. ويورد الجدول أدناه كلًّا منها مع سعرها.',
  'De 16 woningen die te koop staan, vallen in drie groepen: appartementen met tuin op de begane grond, appartementen op de eerste verdieping en duplex penthouses. De tabel hieronder toont elk met zijn prijs.',
  'Szesnaście mieszkań w ofercie dzieli się na trzy grupy: mieszkania z ogrodem na parterze, mieszkania na pierwszym piętrze i dwupoziomowe penthouse’y. W tabeli poniżej wymieniono każde z nich wraz z ceną.',
  'De 16 annonserte boligene deler seg i tre grupper: leiligheter med hage i første etasje, leiligheter i andre etasje og duplex-toppleiligheter. Tabellen nedenfor viser hver av dem med pris.',
  'De 16 listade bostäderna delas in i tre grupper: lägenheter med trädgård på bottenvåningen, lägenheter på första våningen och duplex-takvåningar. Tabellen nedan visar var och en med pris.')
a('Ground-floor apartments with gardens', 'Apartamentos con jardín en planta baja', 'Appartements avec jardin au rez-de-chaussée',
  'Erdgeschosswohnungen mit Garten', 'Квартиры с садом на первом этаже', 'شقق بحدائق في الطابق الأرضي',
  'Appartementen met tuin op de begane grond', 'Mieszkania z ogrodem na parterze', 'Leiligheter med hage i første etasje',
  'Lägenheter med trädgård på bottenvåningen')
a('6 homes, five with two bedrooms and one with three, all with two bathrooms on the plans: 72.63 to 86.14 sqm interior, with a living, dining and kitchen area of 35.32 to 37.66 sqm.',
  '6 viviendas, cinco de dos dormitorios y una de tres, todas con dos baños según los planos: de #72.63 a #86.14 [m2] interiores, con un salón-comedor-cocina de #35.32 a #37.66 [m2].',
  '6 logements, cinq de deux chambres et un de trois, tous avec deux salles de bain selon les plans : de #72.63 à #86.14 [m2] intérieurs, avec un séjour-salle à manger-cuisine de #35.32 à #37.66 [m2].',
  '6 Wohnungen, fünf mit zwei und eine mit drei Schlafzimmern, laut Plänen alle mit zwei Bädern: #72.63 bis #86.14 [m2] Innenfläche, mit einem Wohn-, Ess- und Küchenbereich von #35.32 bis #37.66 [m2].',
  '6 квартир, пять с двумя спальнями и одна с тремя, по планам во всех две ванные комнаты: от #72.63 до #86.14 [m2] внутренней площади, с гостиной-столовой-кухней от #35.32 до #37.66 [m2].',
  '6 مساكن، خمسة منها من غرفتي نوم وواحد من ثلاث غرف نوم، وكلها بحمّامين حسب المخططات: من #72.63 إلى #86.14 [m2] داخلية، مع منطقة معيشة وطعام ومطبخ من #35.32 إلى #37.66 [m2].',
  '6 woningen, vijf met twee en één met drie slaapkamers, volgens de plattegronden allemaal met twee badkamers: #72.63 tot #86.14 [m2] binnenoppervlak, met een woon-, eet- en keukenruimte van #35.32 tot #37.66 [m2].',
  '6 mieszkań, pięć z dwiema sypialniami i jedno z trzema, według rzutów wszystkie z dwiema łazienkami: od #72.63 do #86.14 [m2] powierzchni wewnętrznej, z częścią dzienną z jadalnią i kuchnią od #35.32 do #37.66 [m2].',
  '6 boliger, fem med to soverom og én med tre, alle med to bad ifølge plantegningene: #72.63 til #86.14 [m2] innvendig, med et stue-, spise- og kjøkkenområde på #35.32 til #37.66 [m2].',
  '6 bostäder, fem med två sovrum och en med tre, alla med två badrum enligt ritningarna: #72.63 till #86.14 [m2] inomhus, med vardagsrum, matplats och kök på #35.32 till #37.66 [m2].')
a('Covered and uncovered terraces of 33.01 to 54.20 sqm together and private gardens of 55.40 to 220.12 sqm, which the plans mark as unlandscaped space.',
  'Terrazas cubiertas y descubiertas que suman de #33.01 a #54.20 [m2] y jardines privados de #55.40 a #220.12 [m2], que los planos marcan como espacio sin ajardinar.',
  'Terrasses couvertes et découvertes totalisant de #33.01 à #54.20 [m2] et jardins privatifs de #55.40 à #220.12 [m2], que les plans indiquent comme espace non aménagé.',
  'Überdachte und nicht überdachte Terrassen zusammen von #33.01 bis #54.20 [m2] und private Gärten von #55.40 bis #220.12 [m2], die in den Plänen als nicht angelegte Fläche gekennzeichnet sind.',
  'Крытые и открытые террасы общей площадью от #33.01 до #54.20 [m2] и частные сады от #55.40 до #220.12 [m2], которые на планах обозначены как необустроенная территория.',
  'تراسات مسقوفة ومكشوفة مجموعها من #33.01 إلى #54.20 [m2] وحدائق خاصة من #55.40 إلى #220.12 [m2]، تُظهرها المخططات كمساحة غير مهيأة بالنباتات.',
  'Overdekte en open terrassen van samen #33.01 tot #54.20 [m2] en privétuinen van #55.40 tot #220.12 [m2], die op de plattegronden als niet-aangelegde ruimte staan aangegeven.',
  'Tarasy zadaszone i odkryte łącznie od #33.01 do #54.20 [m2] oraz prywatne ogrody od #55.40 do #220.12 [m2], które na rzutach oznaczono jako teren nieurządzony.',
  'Overbygde og åpne terrasser på til sammen #33.01 til #54.20 [m2] og private hager på #55.40 til #220.12 [m2], som plantegningene markerer som uopparbeidet areal.',
  'Övertäckta och öppna terrasser på sammanlagt #33.01 till #54.20 [m2] och privata trädgårdar på #55.40 till #220.12 [m2], som planritningarna markerar som ej anlagd yta.')
a('First-floor apartments', 'Apartamentos en primera planta', 'Appartements au premier étage', 'Wohnungen im ersten Obergeschoss',
  'Квартиры на втором этаже', 'شقق في الطابق الأول', 'Appartementen op de eerste verdieping', 'Mieszkania na pierwszym piętrze',
  'Leiligheter i andre etasje', 'Lägenheter på första våningen')
a('4 homes with two bedrooms and two bathrooms: 72.63 to 78.46 sqm interior.',
  '4 viviendas de dos dormitorios y dos baños: de #72.63 a #78.46 [m2] interiores.',
  '4 logements de deux chambres et deux salles de bain : de #72.63 à #78.46 [m2] intérieurs.',
  '4 Wohnungen mit zwei Schlafzimmern und zwei Bädern: #72.63 bis #78.46 [m2] Innenfläche.',
  '4 квартиры с двумя спальнями и двумя ванными комнатами: от #72.63 до #78.46 [m2] внутренней площади.',
  '4 مساكن من غرفتي نوم وحمّامين: من #72.63 إلى #78.46 [m2] داخلية.',
  '4 woningen met twee slaapkamers en twee badkamers: #72.63 tot #78.46 [m2] binnenoppervlak.',
  '4 mieszkania z dwiema sypialniami i dwiema łazienkami: od #72.63 do #78.46 [m2] powierzchni wewnętrznej.',
  '4 boliger med to soverom og to bad: #72.63 til #78.46 [m2] innvendig.',
  '4 bostäder med två sovrum och två badrum: #72.63 till #78.46 [m2] inomhus.')
a('Covered and uncovered terraces of 21.72 to 29.84 sqm together.',
  'Terrazas cubiertas y descubiertas que suman de #21.72 a #29.84 [m2].',
  'Terrasses couvertes et découvertes totalisant de #21.72 à #29.84 [m2].',
  'Überdachte und nicht überdachte Terrassen zusammen von #21.72 bis #29.84 [m2].',
  'Крытые и открытые террасы общей площадью от #21.72 до #29.84 [m2].',
  'تراسات مسقوفة ومكشوفة مجموعها من #21.72 إلى #29.84 [m2].',
  'Overdekte en open terrassen van samen #21.72 tot #29.84 [m2].',
  'Tarasy zadaszone i odkryte łącznie od #21.72 do #29.84 [m2].',
  'Overbygde og åpne terrasser på til sammen #21.72 til #29.84 [m2].',
  'Övertäckta och öppna terrasser på sammanlagt #21.72 till #29.84 [m2].')
a('Duplex penthouses', 'Áticos dúplex', 'Penthouses duplex', 'Maisonette-Penthäuser', 'Двухуровневые пентхаусы',
  'بنتهاوس دوبلكس', 'Duplex penthouses', 'Dwupoziomowe penthouse’y', 'Duplex-toppleiligheter', 'Duplex-takvåningar')
a('6 homes: three with two bedrooms and 81.46 sqm interior, and three with three bedrooms and 84.99 to 88.12 sqm interior. The plans show two bathrooms in five of them; for Portal 2 - 2B the sheet shows only the lower level.',
  '6 viviendas: tres de dos dormitorios y #81.46 [m2] interiores, y tres de tres dormitorios y de #84.99 a #88.12 [m2] interiores. Los planos muestran dos baños en cinco de ellas; de Portal 2 - 2B la hoja muestra solo la planta inferior.',
  '6 logements : trois de deux chambres et #81.46 [m2] intérieurs, et trois de trois chambres et de #84.99 à #88.12 [m2] intérieurs. Les plans montrent deux salles de bain dans cinq d’entre eux ; pour Cage 2 - 2B, la feuille ne montre que le niveau inférieur.',
  '6 Wohnungen: drei mit zwei Schlafzimmern und #81.46 [m2] Innenfläche sowie drei mit drei Schlafzimmern und #84.99 bis #88.12 [m2] Innenfläche. Die Pläne zeigen bei fünf davon zwei Bäder; für Aufgang 2 - 2B zeigt das Blatt nur die untere Ebene.',
  '6 квартир: три с двумя спальнями и #81.46 [m2] внутренней площади и три с тремя спальнями и от #84.99 до #88.12 [m2] внутренней площади. По планам в пяти из них две ванные комнаты; для Подъезд 2 - 2B лист показывает только нижний уровень.',
  '6 مساكن: ثلاثة من غرفتي نوم بمساحة داخلية #81.46 [m2]، وثلاثة من ثلاث غرف نوم بمساحة داخلية من #84.99 إلى #88.12 [m2]. تُظهر المخططات حمّامين في خمسة منها؛ أما بالنسبة إلى مدخل 2 - 2B فتُظهر الورقة الطابق السفلي فقط.',
  '6 woningen: drie met twee slaapkamers en #81.46 [m2] binnenoppervlak en drie met drie slaapkamers en #84.99 tot #88.12 [m2] binnenoppervlak. De plattegronden tonen bij vijf ervan twee badkamers; voor Portiek 2 - 2B toont het blad alleen het onderste niveau.',
  '6 mieszkań: trzy z dwiema sypialniami i #81.46 [m2] powierzchni wewnętrznej oraz trzy z trzema sypialniami i od #84.99 do #88.12 [m2] powierzchni wewnętrznej. Rzuty pokazują dwie łazienki w pięciu z nich; dla Klatka 2 - 2B arkusz pokazuje tylko poziom dolny.',
  '6 boliger: tre med to soverom og #81.46 [m2] innvendig og tre med tre soverom og #84.99 til #88.12 [m2] innvendig. Plantegningene viser to bad i fem av dem; for Oppgang 2 - 2B viser arket bare det nedre nivået.',
  '6 bostäder: tre med två sovrum och #81.46 [m2] inomhus och tre med tre sovrum och #84.99 till #88.12 [m2] inomhus. Planritningarna visar två badrum i fem av dem; för Port 2 - 2B visar bladet bara det nedre planet.')
a('Terraces of 60.83 to 76.54 sqm in total. The plans show a staircase to a private roof terrace of 50.59 sqm on the two-bedroom type and 62.16 sqm on the three-bedroom type of Portals 1 and 3. For Portal 2 - 2B the sheet shows only the lower level, with an 18.86 sqm terrace.',
  'Terrazas de #60.83 a #76.54 [m2] en total. Los planos muestran una escalera a una azotea privada de #50.59 [m2] en el tipo de dos dormitorios y de #62.16 [m2] en el tipo de tres dormitorios de los portales 1 y 3. De Portal 2 - 2B la hoja muestra solo la planta inferior, con una terraza de #18.86 [m2].',
  'Terrasses de #60.83 à #76.54 [m2] au total. Les plans montrent un escalier vers un toit-terrasse privé de #50.59 [m2] pour le type à deux chambres et de #62.16 [m2] pour le type à trois chambres des cages 1 et 3. Pour Cage 2 - 2B, la feuille ne montre que le niveau inférieur, avec une terrasse de #18.86 [m2].',
  'Terrassen von insgesamt #60.83 bis #76.54 [m2]. Die Pläne zeigen eine Treppe zu einer privaten Dachterrasse von #50.59 [m2] beim Typ mit zwei Schlafzimmern und von #62.16 [m2] beim Typ mit drei Schlafzimmern der Aufgänge 1 und 3. Für Aufgang 2 - 2B zeigt das Blatt nur die untere Ebene mit einer Terrasse von #18.86 [m2].',
  'Террасы общей площадью от #60.83 до #76.54 [m2]. На планах показана лестница на частную кровельную террасу площадью #50.59 [m2] в типе с двумя спальнями и #62.16 [m2] в типе с тремя спальнями подъездов 1 и 3. Для Подъезд 2 - 2B лист показывает только нижний уровень с террасой #18.86 [m2].',
  'تراسات مجموعها من #60.83 إلى #76.54 [m2]. تُظهر المخططات سلّمًا يؤدي إلى سطح خاص مساحته #50.59 [m2] في نوع غرفتي النوم و#62.16 [m2] في نوع الثلاث غرف نوم في المدخلين 1 و3. أما بالنسبة إلى مدخل 2 - 2B فتُظهر الورقة الطابق السفلي فقط مع تراس مساحته #18.86 [m2].',
  'Terrassen van in totaal #60.83 tot #76.54 [m2]. De plattegronden tonen een trap naar een eigen dakterras van #50.59 [m2] bij het type met twee slaapkamers en van #62.16 [m2] bij het type met drie slaapkamers van portieken 1 en 3. Voor Portiek 2 - 2B toont het blad alleen het onderste niveau, met een terras van #18.86 [m2].',
  'Tarasy o łącznej powierzchni od #60.83 do #76.54 [m2]. Rzuty pokazują schody na prywatny taras dachowy o powierzchni #50.59 [m2] w typie z dwiema sypialniami i #62.16 [m2] w typie z trzema sypialniami na klatkach 1 i 3. Dla Klatka 2 - 2B arkusz pokazuje tylko poziom dolny z tarasem #18.86 [m2].',
  'Terrasser på til sammen #60.83 til #76.54 [m2]. Plantegningene viser en trapp til en privat takterrasse på #50.59 [m2] i typen med to soverom og #62.16 [m2] i typen med tre soverom i oppgang 1 og 3. For Oppgang 2 - 2B viser arket bare det nedre nivået, med en terrasse på #18.86 [m2].',
  'Terrasser på sammanlagt #60.83 till #76.54 [m2]. Planritningarna visar en trappa till en privat takterrass på #50.59 [m2] i typen med två sovrum och #62.16 [m2] i typen med tre sovrum i portarna 1 och 3. För Port 2 - 2B visar bladet bara det nedre planet, med en terrass på #18.86 [m2].')
# "Prices run from ..." by template
PRICE_T = {'es': 'Los precios van de {a} a {b}.', 'fr': 'Les prix vont de {a} à {b}.', 'de': 'Die Preise reichen von {a} bis {b}.',
           'ru': 'Цены — от {a} до {b}.', 'ar': 'تتراوح الأسعار من {a} إلى {b}.', 'nl': 'De prijzen lopen van {a} tot {b}.',
           'pl': 'Ceny wahają się od {a} do {b}.', 'no': 'Prisene går fra {a} til {b}.', 'sv': 'Priserna går från {a} till {b}.'}
for lo, hi in ((400000, 525000), (330000, 354000), (425000, 514000)):
    a(f'Prices run from EUR {lo:,} to EUR {hi:,}.', *[PRICE_T[l].format(a=f'€{lo}', b=f'€{hi}') for l in LOCS])

# ---------------------------------------------------------------- lifestyle, location
a('Every listed home has a terrace on the plans, the ground-floor homes have a garden, and the duplex penthouses add a roof terrace reached by a staircase.',
  'Todas las viviendas a la venta tienen terraza en los planos, las de planta baja tienen jardín y los áticos dúplex añaden una azotea a la que se accede por una escalera.',
  'Tous les logements annoncés ont une terrasse sur les plans, ceux du rez-de-chaussée ont un jardin et les penthouses duplex ajoutent un toit-terrasse accessible par un escalier.',
  'Jede gelistete Wohnung hat laut Plänen eine Terrasse, die Erdgeschosswohnungen haben einen Garten, und die Maisonette-Penthäuser bieten zusätzlich eine über eine Treppe erreichbare Dachterrasse.',
  'У каждой квартиры в продаже по планам есть терраса, у квартир на первом этаже — сад, а двухуровневые пентхаусы дополнительно имеют кровельную террасу, на которую ведёт лестница.',
  'لكل مسكن معروض تراس حسب المخططات، ولمساكن الطابق الأرضي حديقة، وتضيف بنتهاوس الدوبلكس سطحًا يُصعد إليه بسلّم.',
  'Elke woning die te koop staat heeft volgens de plattegronden een terras, de woningen op de begane grond hebben een tuin en de duplex penthouses hebben bovendien een dakterras dat via een trap bereikbaar is.',
  'Każde mieszkanie w ofercie ma według rzutów taras, mieszkania na parterze mają ogród, a dwupoziomowe penthouse’y mają dodatkowo taras dachowy, na który prowadzą schody.',
  'Hver annonserte bolig har terrasse ifølge plantegningene, boligene i første etasje har hage, og duplex-toppleilighetene har i tillegg en takterrasse via en trapp.',
  'Varje listad bostad har en terrass enligt ritningarna, bostäderna på bottenvåningen har trädgård, och duplex-takvåningarna har dessutom en takterrass som nås via en trappa.')
a('An outdoor communal pool with night lighting and salt chlorination, in landscaped gardens with lawns, trees and shrubs.',
  'Una piscina comunitaria exterior con iluminación nocturna y cloración salina, en jardines con césped, árboles y arbustos.',
  'Une piscine commune extérieure avec éclairage nocturne et chloration au sel, dans des jardins paysagers avec pelouses, arbres et arbustes.',
  'Ein Gemeinschaftspool im Freien mit Nachtbeleuchtung und Salzchlorung, in angelegten Gärten mit Rasen, Bäumen und Sträuchern.',
  'Общий открытый бассейн с ночной подсветкой и солевой хлоринацией в озеленённых садах с газонами, деревьями и кустарниками.',
  'مسبح مشترك خارجي بإضاءة ليلية وكلورة ملحية، في حدائق مزروعة بالمروج والأشجار والشجيرات.',
  'Een gemeenschappelijk buitenzwembad met nachtverlichting en zoutchlorering, in aangelegde tuinen met gazon, bomen en struiken.',
  'Wspólny basen zewnętrzny z oświetleniem nocnym i chlorowaniem solnym w zagospodarowanych ogrodach z trawnikami, drzewami i krzewami.',
  'Et felles utendørsbasseng med nattbelysning og saltklorering, i opparbeidede hager med plen, trær og busker.',
  'En gemensam utomhuspool med nattbelysning och saltklorering, i anlagda trädgårdar med gräsmattor, träd och buskar.')
a('The price list gives each home a basement garage space, two for the three-bedroom homes, and a storeroom, with a buggy space for three homes. Power is pre-installed for electric-car charging.',
  'La lista de precios asigna a cada vivienda una plaza de garaje en el sótano, dos a las de tres dormitorios, y un trastero, con una plaza de buggy para tres viviendas. Hay preinstalación de potencia para la carga de coches eléctricos.',
  'La liste de prix attribue à chaque logement une place de garage en sous-sol, deux pour ceux de trois chambres, et une cave, avec une place pour voiturette de golf pour trois logements. La puissance est pré-installée pour la recharge des voitures électriques.',
  'Die Preisliste weist jeder Wohnung einen Garagenstellplatz im Untergeschoss zu, den Wohnungen mit drei Schlafzimmern zwei, dazu einen Abstellraum, und drei Wohnungen zusätzlich einen Buggy-Platz. Für das Laden von Elektroautos ist die Leistung vorinstalliert.',
  'В прайс-листе каждой квартире закреплено место в подвальном гараже (две для квартир с тремя спальнями) и кладовая, а трём квартирам — ещё и место для гольф-кара. Для зарядки электромобилей заранее подведена мощность.',
  'تخصص قائمة الأسعار لكل مسكن مكانًا في مرآب القبو، ومكانين للمساكن من ثلاث غرف نوم، ومخزنًا، مع مكان لعربة غولف لثلاثة مساكن. والقدرة الكهربائية مجهزة مسبقًا لشحن السيارات الكهربائية.',
  'De prijslijst wijst elke woning een garageplaats in de kelder toe, twee voor de woningen met drie slaapkamers, en een berging, met een buggyplaats voor drie woningen. Voor het laden van elektrische auto’s is het vermogen voorbereid.',
  'Cennik przypisuje każdemu mieszkaniu miejsce w garażu podziemnym, dwa w mieszkaniach z trzema sypialniami, oraz komórkę lokatorską, a trzem mieszkaniom także miejsce na meleks. Moc jest wstępnie przygotowana do ładowania samochodów elektrycznych.',
  'Prislisten gir hver bolig en garasjeplass i kjelleren, to for boligene med tre soverom, og en bod, med en plass til golfbil for tre boliger. Effekt er forhåndsinstallert for lading av elbiler.',
  'Prislistan ger varje bostad en garageplats i källaren, två för bostäderna med tre sovrum, och ett förråd, med en plats för golfbil för tre bostäder. Effekt är förinstallerad för laddning av elbilar.')
a('The brochure says the development is close to Estepona Golf and has buggy parking in the basement for golf players.',
  'El folleto indica que la promoción está cerca de Estepona Golf y que cuenta con aparcamiento para buggies en el sótano para quienes juegan al golf.',
  'La brochure indique que la résidence est proche d’Estepona Golf et dispose, en sous-sol, d’un parking pour voiturettes destiné aux golfeurs.',
  'Laut Broschüre liegt die Anlage nahe Estepona Golf und bietet im Untergeschoss Buggy-Stellplätze für Golfspieler.',
  'В брошюре сказано, что комплекс находится рядом с Estepona Golf и что в подвале есть парковка для гольф-каров для любителей гольфа.',
  'يذكر الكتيّب أن المشروع قريب من Estepona Golf وأن فيه مواقف لعربات الغولف في القبو للاعبي الغولف.',
  'Volgens de brochure ligt het project dichtbij Estepona Golf en is er in de kelder buggyparkeren voor golfers.',
  'Broszura podaje, że inwestycja leży w pobliżu Estepona Golf i ma w podziemiu parking na meleksy dla golfistów.',
  'Brosjyren oppgir at prosjektet ligger nær Estepona Golf og har parkering for golfbiler i kjelleren for golfspillere.',
  'Broschyren anger att projektet ligger nära Estepona Golf och har parkering för golfbilar i källaren för golfspelare.')
a('Close to Estepona Golf, <em>with sea views</em>',
  'Junto a Estepona Golf, <em>con vistas al mar</em>', 'Près d’Estepona Golf, <em>avec vue sur la mer</em>',
  'Nahe Estepona Golf, <em>mit Meerblick</em>', 'Рядом с Estepona Golf, <em>с видом на море</em>',
  'بالقرب من Estepona Golf، <em>بإطلالات على البحر</em>', 'Dichtbij Estepona Golf, <em>met zeezicht</em>',
  'Przy Estepona Golf, <em>z widokiem na morze</em>', 'Nær Estepona Golf, <em>med havutsikt</em>',
  'Nära Estepona Golf, <em>med havsutsikt</em>')
a('The development is in Estepona, close to Estepona Golf, and the brochure lists sea views among its features. The renders show the sea from the terraces and the roof terraces. The documents give no distances to the beach, the town centre or the airport, so we do not state any here.',
  'La promoción está en Estepona, cerca de Estepona Golf, y el folleto incluye las vistas al mar entre sus características. Las imágenes muestran el mar desde las terrazas y las azoteas. Los documentos no dan distancias a la playa, al centro de la ciudad ni al aeropuerto, así que no indicamos ninguna aquí.',
  'La résidence se trouve à Estepona, près d’Estepona Golf, et la brochure cite la vue sur la mer parmi ses atouts. Les images montrent la mer depuis les terrasses et les toits-terrasses. Les documents ne donnent aucune distance jusqu’à la plage, au centre-ville ou à l’aéroport ; nous n’en indiquons donc aucune ici.',
  'Die Anlage liegt in Estepona nahe Estepona Golf, und die Broschüre nennt Meerblick unter ihren Merkmalen. Die Visualisierungen zeigen das Meer von den Terrassen und Dachterrassen aus. Die Dokumente nennen keine Entfernungen zum Strand, zum Stadtzentrum oder zum Flughafen, daher geben wir hier keine an.',
  'Комплекс находится в Эстепоне, рядом с Estepona Golf, а в брошюре вид на море указан среди его особенностей. На визуализациях море видно с террас и кровельных террас. В документах нет расстояний до пляжа, центра города и аэропорта, поэтому мы их здесь не указываем.',
  'يقع المشروع في إستيبونا بالقرب من Estepona Golf، ويورد الكتيّب الإطلالات على البحر ضمن ميزاته. وتُظهر الصور البحر من التراسات والأسطح. لا تذكر المستندات مسافات إلى الشاطئ أو مركز المدينة أو المطار، لذلك لا نذكر أي مسافة هنا.',
  'Het project ligt in Estepona, dichtbij Estepona Golf, en de brochure noemt zeezicht onder de kenmerken. De beelden tonen de zee vanaf de terrassen en de dakterrassen. De documenten vermelden geen afstanden tot het strand, het centrum of de luchthaven, dus we noemen er hier geen.',
  'Inwestycja leży w Esteponie, w pobliżu Estepona Golf, a broszura wymienia widok na morze wśród jej cech. Wizualizacje pokazują morze z tarasów i tarasów dachowych. Dokumenty nie podają odległości do plaży, centrum miasta ani lotniska, więc nie podajemy ich tutaj.',
  'Prosjektet ligger i Estepona, nær Estepona Golf, og brosjyren nevner havutsikt blant egenskapene. Bildene viser havet fra terrassene og takterrassene. Dokumentene oppgir ingen avstander til stranden, sentrum eller flyplassen, så vi oppgir ingen her.',
  'Projektet ligger i Estepona, nära Estepona Golf, och broschyren nämner havsutsikt bland egenskaperna. Bilderna visar havet från terrasserna och takterrasserna. Handlingarna anger inga avstånd till stranden, centrum eller flygplatsen, så vi anger inga här.')

# ---------------------------------------------------------------- investment and checks
a('The reservation is EUR 6,000 plus 10% VAT.',
  'La reserva es de €6000 más el 10% de IVA.', 'La réservation est de €6000 plus 10 % de TVA.',
  'Die Reservierung beträgt €6000 zuzüglich 10 % MwSt.', 'Бронирование стоит €6000 плюс НДС 10 %.',
  'الحجز €6000 زائد ضريبة القيمة المضافة 10%.', 'De reservering bedraagt €6000 plus 10% btw.',
  'Rezerwacja wynosi €6000 plus 10% VAT.', 'Reservasjonen er €6000 pluss 10 % mva.',
  'Reservationen är €6000 plus 10 % moms.')
a('30% plus VAT on signing the purchase contract and 70% plus VAT on completion at the notary. The terms do not say whether the reservation is deducted, so we confirm that in writing.',
  'El 30% más IVA al firmar el contrato de compraventa y el 70% más IVA a la finalización ante notario. Las condiciones no indican si se descuenta la reserva, así que lo confirmamos por escrito.',
  '30 % hors TVA à la signature du contrat de vente et 70 % hors TVA à l’achèvement chez le notaire. Les conditions n’indiquent pas si la réservation est déduite ; nous le confirmons donc par écrit.',
  '30 % zuzüglich MwSt. bei Unterzeichnung des Kaufvertrags und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar. Aus den Bedingungen geht nicht hervor, ob die Reservierung abgezogen wird; wir bestätigen dies schriftlich.',
  '30 % плюс НДС при подписании договора купли-продажи и 70 % плюс НДС при завершении сделки у нотариуса. В условиях не сказано, засчитывается ли бронь, поэтому мы уточняем это в письменном виде.',
  '30% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء و70% زائد الضريبة عند الإتمام أمام كاتب العدل. لا تذكر الشروط ما إذا كان الحجز يُخصم، لذلك نؤكد ذلك كتابةً.',
  '30% plus btw bij ondertekening van de koopovereenkomst en 70% plus btw bij oplevering ten overstaan van de notaris. De voorwaarden vermelden niet of de reservering wordt afgetrokken, dus dat bevestigen we schriftelijk.',
  '30% plus VAT przy podpisaniu umowy sprzedaży i 70% plus VAT u notariusza, przy akcie notarialnym. Warunki nie mówią, czy rezerwacja jest odliczana, dlatego potwierdzamy to na piśmie.',
  '30 % pluss mva. ved signering av kjøpekontrakten og 70 % pluss mva. ved overtakelse hos notarius. Vilkårene oppgir ikke om reservasjonen trekkes fra, så vi bekrefter det skriftlig.',
  '30 % plus moms vid undertecknandet av köpeavtalet och 70 % plus moms vid tillträdet hos notarien. Villkoren anger inte om reservationen dras av, så vi bekräftar det skriftligen.')
a('The price list states its prices without VAT, and the payment terms give VAT at 10%. Nueva Living confirms the taxes and purchase costs in writing.',
  'La lista de precios indica sus precios sin IVA, y las condiciones de pago fijan el IVA en el 10%. Nueva Living confirma por escrito los impuestos y los gastos de compra.',
  'La liste de prix indique ses prix hors TVA, et les conditions de paiement fixent la TVA à 10 %. Nueva Living confirme par écrit les taxes et les frais d’achat.',
  'Die Preisliste weist ihre Preise ohne MwSt. aus, und die Zahlungsbedingungen geben die MwSt. mit 10 % an. Nueva Living bestätigt Steuern und Kaufnebenkosten schriftlich.',
  'В прайс-листе цены указаны без НДС, а в условиях оплаты НДС составляет 10 %. Nueva Living подтверждает налоги и расходы на покупку в письменном виде.',
  'تذكر قائمة الأسعار أسعارها دون ضريبة القيمة المضافة، وتحدد شروط الدفع الضريبة بنسبة 10%. وتؤكد Nueva Living الضرائب وتكاليف الشراء كتابةً.',
  'De prijslijst vermeldt haar prijzen zonder btw en de betalingsvoorwaarden geven de btw op 10%. Nueva Living bevestigt de belastingen en aankoopkosten schriftelijk.',
  'Cennik podaje ceny bez VAT, a warunki płatności określają VAT na 10%. Nueva Living potwierdza podatki i koszty zakupu na piśmie.',
  'Prislisten oppgir prisene uten mva., og betalingsvilkårene oppgir mva. til 10 %. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan anger priserna utan moms, och betalningsvillkoren anger momsen till 10 %. Nueva Living bekräftar skatter och köpkostnader skriftligen.')
a('Works and licence', 'Obras y licencia', 'Travaux et permis', 'Bauarbeiten und Genehmigung', 'Работы и разрешение',
  'الأعمال والرخصة', 'Werken en vergunning', 'Prace i pozwolenie', 'Byggearbeider og tillatelse', 'Arbeten och bygglov')
a('The sales portal marks the development as works started, the brochure calls it a construction project, and the plans are marked basic-project stage (eleven sheets, September 2023) or execution-project stage (five sheets, September and December 2025). We ask for the licence, the state of the works and the start date.',
  'El portal de ventas marca la promoción como obras iniciadas, el folleto la llama proyecto de construcción y los planos figuran en fase de proyecto básico (once hojas, septiembre de 2023) o de proyecto de ejecución (cinco hojas, septiembre y diciembre de 2025). Pedimos la licencia, el estado de las obras y la fecha de inicio.',
  'Le portail de vente indique que les travaux ont commencé, la brochure parle d’un projet de construction, et les plans sont au stade du projet de base (onze feuilles, septembre 2023) ou du projet d’exécution (cinq feuilles, septembre et décembre 2025). Nous demandons le permis, l’état des travaux et la date de début.',
  'Das Verkaufsportal kennzeichnet die Anlage als „Bauarbeiten begonnen“, die Broschüre spricht von einem Bauprojekt, und die Pläne sind dem Stand des Basisprojekts (elf Blätter, September 2023) oder des Ausführungsprojekts (fünf Blätter, September und Dezember 2025) zugeordnet. Wir fordern die Genehmigung, den Stand der Arbeiten und den Baubeginn an.',
  'Портал продаж отмечает комплекс как «работы начаты», в брошюре он назван проектом строительства, а планы относятся к стадии базового проекта (одиннадцать листов, сентябрь 2023 года) или проекта исполнения (пять листов, сентябрь и декабрь 2025 года). Мы запрашиваем разрешение, ход работ и дату начала.',
  'تشير بوابة المبيعات إلى أن الأعمال بدأت، ويصف الكتيّب المشروع بأنه مشروع بناء، والمخططات مصنفة في مرحلة المشروع الأساسي (أحد عشر لوحًا، سبتمبر 2023) أو مشروع التنفيذ (خمسة ألواح، سبتمبر وديسمبر 2025). نطلب الرخصة وحالة الأعمال وتاريخ البدء.',
  'Het verkoopportaal markeert het project als werken gestart, de brochure noemt het een bouwproject, en de plattegronden zijn aangeduid als basisproject (elf bladen, september 2023) of uitvoeringsproject (vijf bladen, september en december 2025). We vragen om de vergunning, de stand van de werken en de startdatum.',
  'Portal sprzedażowy oznacza inwestycję jako „prace rozpoczęte”, broszura nazywa ją projektem budowlanym, a rzuty są na etapie projektu podstawowego (jedenaście arkuszy, wrzesień 2023) lub projektu wykonawczego (pięć arkuszy, wrzesień i grudzień 2025). Prosimy o pozwolenie, stan prac i datę rozpoczęcia.',
  'Salgsportalen markerer prosjektet som byggestart, brosjyren kaller det et byggeprosjekt, og plantegningene er merket som grunnprosjekt (elleve ark, september 2023) eller utførelsesprosjekt (fem ark, september og desember 2025). Vi ber om tillatelsen, byggets status og startdatoen.',
  'Försäljningsportalen markerar projektet som byggstartat, broschyren kallar det ett byggprojekt, och planritningarna är märkta som grundprojekt (elva blad, september 2023) eller genomförandeprojekt (fem blad, september och december 2025). Vi ber om bygglovet, arbetenas status och startdatumet.')
a('None of the documents we hold states a completion date, so none is shown on this page. We ask for the contractual date in writing.',
  'Ninguno de los documentos de que disponemos indica una fecha de finalización, así que no se muestra ninguna en esta página. Pedimos la fecha contractual por escrito.',
  'Aucun des documents dont nous disposons n’indique de date d’achèvement ; aucune n’est donc affichée sur cette page. Nous demandons la date contractuelle par écrit.',
  'In keinem der uns vorliegenden Dokumente ist ein Fertigstellungstermin genannt, deshalb wird auf dieser Seite keiner angezeigt. Wir fordern den vertraglichen Termin schriftlich an.',
  'Ни в одном из имеющихся у нас документов не указана дата завершения, поэтому на этой странице она не приводится. Мы запрашиваем договорную дату в письменном виде.',
  'لا يذكر أي مستند لدينا موعد الانتهاء، لذلك لا يظهر أي موعد في هذه الصفحة. نطلب التاريخ التعاقدي كتابةً.',
  'Geen van de documenten waarover wij beschikken vermeldt een opleverdatum, dus er wordt er op deze pagina geen getoond. We vragen de contractuele datum schriftelijk op.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu zakończenia, dlatego na tej stronie go nie wskazujemy. Prosimy o termin umowny na piśmie.',
  'Ingen av dokumentene vi har oppgir en ferdigstillelsesdato, så ingen vises på denne siden. Vi ber om den kontraktsfestede datoen skriftlig.',
  'Ingen av de handlingar vi har anger något färdigställandedatum, så inget visas på den här sidan. Vi ber om det avtalade datumet skriftligen.')
a('The price list gives a built area that includes a share of the communal areas, and for 13 of the 16 homes the plan gives a different figure. The interior areas and the terraces agree. We confirm which figure the contract uses.',
  'La lista de precios da una superficie construida que incluye una parte de las zonas comunes, y para 13 de las 16 viviendas el plano da una cifra distinta. Las superficies interiores y las terrazas coinciden. Confirmamos qué cifra utiliza el contrato.',
  'La liste de prix donne une surface construite incluant une quote-part des parties communes, et pour 13 des 16 logements le plan donne un chiffre différent. Les surfaces intérieures et les terrasses concordent. Nous confirmons quel chiffre le contrat retient.',
  'Die Preisliste nennt eine bebaute Fläche einschließlich eines Anteils an den Gemeinschaftsflächen, und für 13 der 16 Wohnungen nennt der Plan eine andere Zahl. Die Innenflächen und die Terrassen stimmen überein. Wir bestätigen, welche Zahl der Vertrag verwendet.',
  'В прайс-листе указана площадь застройки, включающая долю общих зон, а для 13 из 16 квартир на плане приведена другая цифра. Внутренние площади и террасы совпадают. Мы уточняем, какая цифра используется в договоре.',
  'تذكر قائمة الأسعار مساحة مبنية تشمل حصة من المناطق المشتركة، وفي 13 من المساكن الـ16 يذكر المخطط رقمًا مختلفًا. أما المساحات الداخلية والتراسات فمتطابقة. نؤكد أي رقم يعتمده العقد.',
  'De prijslijst geeft een bebouwde oppervlakte inclusief een aandeel in de gemeenschappelijke delen, en voor 13 van de 16 woningen geeft de plattegrond een ander cijfer. De binnenoppervlaktes en de terrassen komen overeen. We bevestigen welk cijfer het contract hanteert.',
  'Cennik podaje powierzchnię zabudowy wraz z udziałem w częściach wspólnych, a dla 13 z 16 mieszkań rzut podaje inną wartość. Powierzchnie wewnętrzne i tarasy są zgodne. Potwierdzamy, której wartości używa umowa.',
  'Prislisten oppgir et bebygd areal som inkluderer en andel av fellesarealene, og for 13 av de 16 boligene oppgir plantegningen et annet tall. De innvendige arealene og terrassene stemmer overens. Vi bekrefter hvilket tall kontrakten bruker.',
  'Prislistan anger en byggyta som omfattar en andel av de gemensamma ytorna, och för 13 av de 16 bostäderna anger planritningen ett annat tal. De invändiga ytorna och terrasserna stämmer överens. Vi bekräftar vilket tal avtalet använder.')
a('The quality specification is version V-0.2 of 5 June 2024 and is marked provisional, and the energy rating of B is a project-stage rating. We ask for the final specification and certificate.',
  'La memoria de calidades es la versión V-0.2 del 5 de junio de 2024 y está marcada como provisional, y la calificación energética B es una calificación en fase de proyecto. Pedimos la memoria definitiva y el certificado.',
  'Le descriptif de qualité est la version V-0.2 du 5 juin 2024 et il est marqué comme provisoire, et la classe énergétique B est une classe au stade du projet. Nous demandons le descriptif définitif et le certificat.',
  'Die Bau- und Ausstattungsbeschreibung ist die Version V-0.2 vom 5. Juni 2024 und als vorläufig gekennzeichnet, und die Energieeffizienzklasse B ist eine Einstufung im Projektstadium. Wir fordern die endgültige Beschreibung und den Energieausweis an.',
  'Описание качества — версия V-0.2 от 5 июня 2024 года, оно помечено как предварительное, а класс энергоэффективности B — оценка на стадии проекта. Мы запрашиваем окончательное описание и сертификат.',
  'مواصفات الجودة هي النسخة V-0.2 بتاريخ 5 يونيو 2024 وهي مصنفة كمؤقتة، وتصنيف الطاقة B هو تصنيف في مرحلة المشروع. نطلب المواصفات النهائية والشهادة.',
  'De kwaliteitsomschrijving is versie V-0.2 van 5 juni 2024 en als voorlopig aangeduid, en het energielabel B is een label in de projectfase. We vragen om de definitieve omschrijving en het certificaat.',
  'Opis jakości wykonania to wersja V-0.2 z 5 czerwca 2024 r., oznaczona jako wstępna, a klasa energetyczna B to klasa na etapie projektu. Prosimy o ostateczny opis i świadectwo.',
  'Kvalitetsbeskrivelsen er versjon V-0.2 av 5. juni 2024 og er merket som foreløpig, og energimerke B er et merke på prosjektstadiet. Vi ber om den endelige beskrivelsen og sertifikatet.',
  'Kvalitetsbeskrivningen är version V-0.2 av den 5 juni 2024 och är markerad som preliminär, och energiklass B är en klass på projektstadiet. Vi ber om den slutliga beskrivningen och intyget.')

# ---------------------------------------------------------------- availability
a('16 homes <em>currently listed</em>', '16 viviendas <em>a la venta actualmente</em>', '16 logements <em>actuellement annoncés</em>',
  '16 Wohnungen <em>derzeit gelistet</em>', '16 квартир <em>сейчас в продаже</em>', '16 مسكنًا <em>معروضة حاليًا</em>',
  '16 woningen <em>momenteel te koop</em>', '16 mieszkań <em>obecnie w ofercie</em>', '16 boliger <em>annonsert nå</em>',
  '16 bostäder <em>listade just nu</em>')
a('Prices are those of the developer’s list as of October 2026 and are confirmed before reservation. The homes are listed by portal, floor and door: ground-floor apartments with gardens, first-floor apartments and duplex penthouses.',
  'Los precios son los de la lista del promotor a octubre de 2026 y se confirman antes de la reserva. Las viviendas se enumeran por portal, planta y puerta: apartamentos con jardín en planta baja, apartamentos en primera planta y áticos dúplex.',
  'Les prix sont ceux de la liste du promoteur à octobre 2026 et sont confirmés avant la réservation. Les logements sont classés par cage, étage et porte : appartements avec jardin au rez-de-chaussée, appartements au premier étage et penthouses duplex.',
  'Die Preise sind die der Liste des Bauträgers vom Oktober 2026 und werden vor der Reservierung bestätigt. Die Wohnungen sind nach Aufgang, Etage und Tür aufgeführt: Erdgeschosswohnungen mit Garten, Wohnungen im ersten Obergeschoss und Maisonette-Penthäuser.',
  'Цены приведены по списку застройщика на октябрь 2026 года и подтверждаются перед бронированием. Квартиры перечислены по подъезду, этажу и двери: квартиры с садом на первом этаже, квартиры на втором этаже и двухуровневые пентхаусы.',
  'الأسعار هي أسعار قائمة المطوّر حتى أكتوبر 2026 وتُؤكَّد قبل الحجز. تُدرج المساكن بحسب المدخل والطابق والباب: شقق بحدائق في الطابق الأرضي وشقق في الطابق الأول وبنتهاوس دوبلكس.',
  'De prijzen zijn die van de lijst van de ontwikkelaar per oktober 2026 en worden vóór de reservering bevestigd. De woningen staan per portiek, verdieping en deur: appartementen met tuin op de begane grond, appartementen op de eerste verdieping en duplex penthouses.',
  'Ceny pochodzą z listy dewelopera z października 2026 r. i są potwierdzane przed rezerwacją. Mieszkania wymieniono według klatki, piętra i drzwi: mieszkania z ogrodem na parterze, mieszkania na pierwszym piętrze i dwupoziomowe penthouse’y.',
  'Prisene er de fra utbyggerens liste per oktober 2026 og bekreftes før reservasjon. Boligene er oppført etter oppgang, etasje og dør: leiligheter med hage i første etasje, leiligheter i andre etasje og duplex-toppleiligheter.',
  'Priserna är de från exploatörens lista per oktober 2026 och bekräftas före reservation. Bostäderna är uppförda efter port, våning och dörr: lägenheter med trädgård på bottenvåningen, lägenheter på första våningen och duplex-takvåningar.')
a('Prices and interior areas are transcribed from the developer’s price list of October 2026, which shows 16 of the development’s 72 homes and states its prices without VAT. The terrace is the covered and the uncovered terrace together; for the ground-floor homes the list’s uncovered terrace figure includes the garden, which we show separately from the plans (Portal 3 - 0C: 13.37 sqm of uncovered terrace and 220.12 sqm of garden on the plan, 233.49 sqm of uncovered terrace on the list). The list also gives a built area including a share of the communal areas, which we do not print because 13 of the 16 plans give a different figure (Portal 1 - 0A: 156.16 sqm on the plan, 124.78 sqm on the list; Portal 3 - 2A: 133.63 sqm on the plan, 131.72 sqm on the list). The brochure says two-bedroom homes start at 81.46 sqm useful, while the list has two-bedroom homes of 72.63 and 78.46 sqm; we use the list. The list gives each home one garage space and a storeroom, the four three-bedroom homes two garage spaces, and three of them a buggy space. The brochure calls a communal room a coworking area and the portal calls it a social club.',
  'Los precios y las superficies interiores se han transcrito de la lista de precios del promotor de octubre de 2026, que recoge 16 de las 72 viviendas de la promoción y da sus precios sin IVA. La terraza es la terraza cubierta y la descubierta juntas; en las viviendas de planta baja, la cifra de terraza descubierta de la lista incluye el jardín, que mostramos por separado a partir de los planos (Portal 3 - 0C: #13.37 [m2] de terraza descubierta y #220.12 [m2] de jardín en el plano, #233.49 [m2] de terraza descubierta en la lista). La lista también da una superficie construida con parte de las zonas comunes, que no publicamos porque 13 de los 16 planos dan una cifra distinta (Portal 1 - 0A: #156.16 [m2] en el plano, #124.78 [m2] en la lista; Portal 3 - 2A: #133.63 [m2] en el plano, #131.72 [m2] en la lista). El folleto dice que las viviendas de dos dormitorios parten de #81.46 [m2] útiles, mientras que la lista tiene viviendas de dos dormitorios de #72.63 y #78.46 [m2]; usamos la lista. La lista asigna a cada vivienda una plaza de garaje y un trastero, a las cuatro viviendas de tres dormitorios dos plazas de garaje y a tres de ellas una plaza de buggy. El folleto llama zona coworking a una sala comunitaria y el portal la llama club social.',
  'Les prix et les surfaces intérieures sont repris de la liste de prix du promoteur d’octobre 2026, qui présente 16 des 72 logements de la résidence et indique ses prix hors TVA. La terrasse est la terrasse couverte et la terrasse découverte réunies ; pour les logements du rez-de-chaussée, le chiffre de terrasse découverte de la liste inclut le jardin, que nous indiquons séparément d’après les plans (Cage 3 - 0C : #13.37 [m2] de terrasse découverte et #220.12 [m2] de jardin sur le plan, #233.49 [m2] de terrasse découverte sur la liste). La liste donne aussi une surface construite incluant une quote-part des parties communes, que nous ne publions pas car 13 des 16 plans donnent un chiffre différent (Cage 1 - 0A : #156.16 [m2] sur le plan, #124.78 [m2] sur la liste ; Cage 3 - 2A : #133.63 [m2] sur le plan, #131.72 [m2] sur la liste). La brochure indique que les logements de deux chambres commencent à #81.46 [m2] utiles, alors que la liste compte des logements de deux chambres de #72.63 et #78.46 [m2] ; nous retenons la liste. La liste attribue à chaque logement une place de garage et une cave, aux quatre logements de trois chambres deux places de garage, et à trois d’entre eux une place pour voiturette. La brochure appelle espace de coworking une salle commune que le portail appelle club social.',
  'Preise und Innenflächen sind der Preisliste des Bauträgers vom Oktober 2026 entnommen, die 16 der 72 Wohnungen der Anlage zeigt und ihre Preise ohne MwSt. nennt. Die Terrasse ist die überdachte und die nicht überdachte Terrasse zusammen; bei den Erdgeschosswohnungen enthält die Angabe der nicht überdachten Terrasse in der Liste den Garten, den wir anhand der Pläne getrennt ausweisen (Aufgang 3 - 0C: #13.37 [m2] nicht überdachte Terrasse und #220.12 [m2] Garten laut Plan, #233.49 [m2] nicht überdachte Terrasse laut Liste). Die Liste nennt außerdem eine bebaute Fläche einschließlich eines Anteils an den Gemeinschaftsflächen, die wir nicht abdrucken, weil 13 der 16 Pläne eine andere Zahl nennen (Aufgang 1 - 0A: #156.16 [m2] laut Plan, #124.78 [m2] laut Liste; Aufgang 3 - 2A: #133.63 [m2] laut Plan, #131.72 [m2] laut Liste). Die Broschüre nennt für Wohnungen mit zwei Schlafzimmern ab #81.46 [m2] Nutzfläche, während die Liste Wohnungen mit zwei Schlafzimmern von #72.63 und #78.46 [m2] führt; wir folgen der Liste. Die Liste weist jeder Wohnung einen Garagenstellplatz und einen Abstellraum zu, den vier Wohnungen mit drei Schlafzimmern zwei Garagenstellplätze und dreien davon einen Buggy-Platz. Die Broschüre nennt einen Gemeinschaftsraum Coworking-Bereich, das Portal nennt ihn Social Club.',
  'Цены и внутренние площади взяты из прайс-листа застройщика от октября 2026 года, в котором указаны 16 из 72 квартир комплекса и цены без НДС. Терраса — это крытая и открытая террасы вместе; у квартир на первом этаже указанная в списке площадь открытой террасы включает сад, который мы показываем отдельно по планам (Подъезд 3 - 0C: #13.37 [m2] открытой террасы и #220.12 [m2] сада по плану, #233.49 [m2] открытой террасы по списку). В списке также указана площадь застройки с долей общих зон, которую мы не публикуем, потому что для 13 из 16 планов приведена другая цифра (Подъезд 1 - 0A: #156.16 [m2] по плану, #124.78 [m2] по списку; Подъезд 3 - 2A: #133.63 [m2] по плану, #131.72 [m2] по списку). В брошюре указано, что квартиры с двумя спальнями начинаются от #81.46 [m2] полезной площади, тогда как в списке есть квартиры с двумя спальнями площадью #72.63 и #78.46 [m2]; мы ориентируемся на список. Список закрепляет за каждой квартирой место в гараже и кладовую, за четырьмя квартирами с тремя спальнями — два места в гараже, а за тремя из них — ещё и место для гольф-кара. В брошюре общее помещение названо зоной коворкинга, а на портале — клубом.',
  'الأسعار والمساحات الداخلية منقولة من قائمة أسعار المطوّر لشهر أكتوبر 2026، التي تعرض 16 من مساكن المشروع الـ72 وتذكر أسعارها دون ضريبة القيمة المضافة. التراس هو التراس المسقوف والمكشوف معًا؛ وفي مساكن الطابق الأرضي يشمل رقم التراس المكشوف في القائمة الحديقة، ونعرضها منفصلة اعتمادًا على المخططات (مدخل 3 - 0C: #13.37 [m2] تراس مكشوف و#220.12 [m2] حديقة في المخطط، و#233.49 [m2] تراس مكشوف في القائمة). وتذكر القائمة أيضًا مساحة مبنية تشمل حصة من المناطق المشتركة، لا ننشرها لأن 13 من المخططات الـ16 تذكر رقمًا مختلفًا (مدخل 1 - 0A: #156.16 [m2] في المخطط و#124.78 [m2] في القائمة؛ مدخل 3 - 2A: #133.63 [m2] في المخطط و#131.72 [m2] في القائمة). ويذكر الكتيّب أن مساكن غرفتي النوم تبدأ من #81.46 [m2] مساحة صافية، بينما تضم القائمة مساكن من غرفتي نوم بمساحة #72.63 و#78.46 [m2]؛ ونعتمد القائمة. وتخصص القائمة لكل مسكن مكانًا في المرآب ومخزنًا، وللمساكن الأربعة من ثلاث غرف نوم مكانين في المرآب، ولثلاثة منها مكانًا لعربة غولف. ويسمي الكتيّب قاعة مشتركة منطقة عمل مشترك وتسميها البوابة نادٍ اجتماعيًا.',
  'De prijzen en binnenoppervlaktes zijn overgenomen uit de prijslijst van de ontwikkelaar van oktober 2026, die 16 van de 72 woningen van het project toont en haar prijzen zonder btw vermeldt. Het terras is het overdekte en het open terras samen; bij de woningen op de begane grond omvat het cijfer voor het open terras in de lijst de tuin, die wij aan de hand van de plattegronden apart tonen (Portiek 3 - 0C: #13.37 [m2] open terras en #220.12 [m2] tuin volgens de plattegrond, #233.49 [m2] open terras volgens de lijst). De lijst geeft ook een bebouwde oppervlakte inclusief een aandeel in de gemeenschappelijke delen, die wij niet publiceren omdat 13 van de 16 plattegronden een ander cijfer geven (Portiek 1 - 0A: #156.16 [m2] volgens de plattegrond, #124.78 [m2] volgens de lijst; Portiek 3 - 2A: #133.63 [m2] volgens de plattegrond, #131.72 [m2] volgens de lijst). De brochure zegt dat woningen met twee slaapkamers beginnen bij #81.46 [m2] bruikbaar, terwijl de lijst woningen met twee slaapkamers van #72.63 en #78.46 [m2] heeft; wij volgen de lijst. De lijst wijst elke woning een garageplaats en een berging toe, de vier woningen met drie slaapkamers twee garageplaatsen en drie daarvan een buggyplaats. De brochure noemt een gemeenschappelijke ruimte een coworkingruimte en het portaal noemt die een sociale club.',
  'Ceny i powierzchnie wewnętrzne przepisano z cennika dewelopera z października 2026 r., który pokazuje 16 z 72 mieszkań inwestycji i podaje ceny bez VAT. Taras to taras zadaszony i odkryty łącznie; w mieszkaniach na parterze podana w cenniku powierzchnia tarasu odkrytego obejmuje ogród, który pokazujemy osobno na podstawie rzutów (Klatka 3 - 0C: #13.37 [m2] tarasu odkrytego i #220.12 [m2] ogrodu według rzutu, #233.49 [m2] tarasu odkrytego według cennika). Cennik podaje też powierzchnię zabudowy z udziałem w częściach wspólnych, której nie publikujemy, ponieważ 13 z 16 rzutów podaje inną wartość (Klatka 1 - 0A: #156.16 [m2] według rzutu, #124.78 [m2] według cennika; Klatka 3 - 2A: #133.63 [m2] według rzutu, #131.72 [m2] według cennika). Broszura podaje, że mieszkania z dwiema sypialniami zaczynają się od #81.46 [m2] powierzchni użytkowej, podczas gdy cennik zawiera mieszkania z dwiema sypialniami o powierzchni #72.63 i #78.46 [m2]; opieramy się na cenniku. Cennik przypisuje każdemu mieszkaniu miejsce w garażu i komórkę lokatorską, czterem mieszkaniom z trzema sypialniami dwa miejsca w garażu, a trzem z nich także miejsce na meleks. Broszura nazywa wspólne pomieszczenie strefą coworkingową, a portal — klubem towarzyskim.',
  'Prisene og de innvendige arealene er hentet fra utbyggerens prisliste fra oktober 2026, som viser 16 av prosjektets 72 boliger og oppgir prisene uten mva. Terrassen er den overbygde og den åpne terrassen til sammen; for boligene i første etasje inkluderer listens tall for åpen terrasse hagen, som vi viser separat ut fra plantegningene (Oppgang 3 - 0C: #13.37 [m2] åpen terrasse og #220.12 [m2] hage ifølge plantegningen, #233.49 [m2] åpen terrasse ifølge listen). Listen oppgir også et bebygd areal som inkluderer en andel av fellesarealene, som vi ikke publiserer fordi 13 av de 16 plantegningene oppgir et annet tall (Oppgang 1 - 0A: #156.16 [m2] ifølge plantegningen, #124.78 [m2] ifølge listen; Oppgang 3 - 2A: #133.63 [m2] ifølge plantegningen, #131.72 [m2] ifølge listen). Brosjyren sier at boliger med to soverom starter på #81.46 [m2] nyttbart, mens listen har boliger med to soverom på #72.63 og #78.46 [m2]; vi bruker listen. Listen gir hver bolig en garasjeplass og en bod, de fire boligene med tre soverom to garasjeplasser og tre av dem en plass til golfbil. Brosjyren kaller et felles rom et coworking-område, og portalen kaller det en sosial klubb.',
  'Priser och invändiga ytor är hämtade ur exploatörens prislista från oktober 2026, som visar 16 av projektets 72 bostäder och anger priserna utan moms. Terrassen är den övertäckta och den öppna terrassen tillsammans; för bostäderna på bottenvåningen omfattar listans siffra för öppen terrass trädgården, som vi redovisar separat utifrån ritningarna (Port 3 - 0C: #13.37 [m2] öppen terrass och #220.12 [m2] trädgård enligt ritningen, #233.49 [m2] öppen terrass enligt listan). Listan anger också en byggyta som omfattar en andel av de gemensamma ytorna, som vi inte publicerar eftersom 13 av de 16 ritningarna anger ett annat tal (Port 1 - 0A: #156.16 [m2] enligt ritningen, #124.78 [m2] enligt listan; Port 3 - 2A: #133.63 [m2] enligt ritningen, #131.72 [m2] enligt listan). Broschyren säger att bostäder med två sovrum börjar på #81.46 [m2] nyttjandeyta, medan listan har bostäder med två sovrum på #72.63 och #78.46 [m2]; vi utgår från listan. Listan ger varje bostad en garageplats och ett förråd, de fyra bostäderna med tre sovrum två garageplatser och tre av dem en plats för golfbil. Broschyren kallar ett gemensamt rum ett coworking-område, och portalen kallar det en social klubb.')

# ---------------------------------------------------------------- units
a('Duplex penthouse', 'Ático dúplex', 'Penthouse duplex', 'Maisonette-Penthaus', 'Двухуровневый пентхаус',
  'بنتهاوس دوبلكس', 'Duplex penthouse', 'Penthouse dwupoziomowy', 'Duplex-toppleilighet', 'Duplex-takvåning')
SIZE_T = {
    'es': ('{i} m² interiores', '{t} m² de terraza', '{g} m² de jardín', ', '),
    'fr': ('{i} m² intérieurs', '{t} m² de terrasse', '{g} m² de jardin', ', '),
    'de': ('{i} m² Innenfläche', '{t} m² Terrasse', '{g} m² Garten', ', '),
    'ru': ('{i} м² внутри', 'терраса {t} м²', 'сад {g} м²', ', '),
    'ar': ('{i} م² داخلية', '{t} م² تراس', '{g} م² حديقة', '، '),
    'nl': ('{i} m² binnen', '{t} m² terras', '{g} m² tuin', ', '),
    'pl': ('{i} m² wnętrza', '{t} m² tarasu', '{g} m² ogrodu', ', '),
    'no': ('{i} m² innvendig', '{t} m² terrasse', '{g} m² hage', ', '),
    'sv': ('{i} m² inomhus', '{t} m² terrass', '{g} m² trädgård', ', '),
}
UNITS = [('86.14', '54.20', '55.40'), ('72.63', '45.22', '84.40'), ('78.46', '33.01', '109.52'), ('88.12', '76.54', None),
         ('72.63', '45.22', '139.26'), ('78.46', '21.72', None), ('84.99', '70.77', None), ('72.63', '45.22', '165.41'),
         ('72.63', '45.22', '220.12'), ('88.12', '76.54', None), ('72.63', '29.84', None), ('78.46', '21.72', None),
         ('81.46', '60.83', None)]
for i, t, g in UNITS:
    en = f'{i} sqm interior, {t} sqm terrace' + (f', {g} sqm garden' if g else '')
    row = []
    for l in LOCS:
        si, st, sg, sep = SIZE_T[l]
        dec = (lambda x: x) if l == 'ar' else (lambda x: x.replace('.', ','))
        parts = [si.format(i=dec(i)), st.format(t=dec(t))] + ([sg.format(g=dec(g))] if g else [])
        row.append(sep.join(parts))
    # these are already localised; bypass the token expander
    if en in TODO:
        T[en] = dict(zip(LOCS, row))

# ---------------------------------------------------------------- timeline, viewing, faq
a('See the site and the area with us, and the plans against the state of the works.',
  'Vea la parcela y la zona con nosotros, y los planos frente al estado de las obras.',
  'Découvrez le site et le quartier avec nous, et comparez les plans à l’état des travaux.',
  'Sehen Sie sich das Grundstück und die Umgebung mit uns an und vergleichen Sie die Pläne mit dem Stand der Bauarbeiten.',
  'Осмотрите участок и окрестности вместе с нами и сопоставьте планы с ходом работ.',
  'عاينوا الموقع والمنطقة معنا، وقارنوا المخططات بحالة الأعمال.',
  'Bekijk het terrein en de omgeving met ons en leg de plattegronden naast de stand van de werken.',
  'Zobaczą Państwo teren i okolicę razem z nami oraz porównają rzuty ze stanem prac.',
  'Se tomten og området sammen med oss, og se plantegningene opp mot byggets status.',
  'Se tomten och området tillsammans med oss, och se ritningarna mot arbetenas status.')
a('A reservation of EUR 6,000 plus VAT, then the purchase contract, with the advance payments under the developer’s guarantee policy.',
  'Una reserva de €6000 más IVA y después el contrato de compraventa, con los pagos a cuenta bajo la póliza de garantía del promotor.',
  'Une réservation de €6000 hors TVA, puis le contrat de vente, avec les acomptes couverts par la police de garantie du promoteur.',
  'Eine Reservierung von €6000 zuzüglich MwSt., dann der Kaufvertrag, mit Anzahlungen, die über die Garantiepolice des Bauträgers abgesichert sind.',
  'Бронирование €6000 плюс НДС, затем договор купли-продажи, при этом авансовые платежи покрываются гарантийным полисом застройщика.',
  'حجز بقيمة €6000 زائد ضريبة القيمة المضافة، ثم عقد الشراء، مع الدفعات المقدمة بموجب وثيقة ضمان المطوّر.',
  'Een reservering van €6000 plus btw, daarna de koopovereenkomst, met de vooruitbetalingen onder de garantiepolis van de ontwikkelaar.',
  'Rezerwacja €6000 plus VAT, następnie umowa sprzedaży, z zaliczkami objętymi polisą gwarancyjną dewelopera.',
  'En reservasjon på €6000 pluss mva., deretter kjøpekontrakten, med forskuddsbetalingene dekket av utbyggerens garantipolise.',
  'En reservation på €6000 plus moms, därefter köpeavtalet, med förskottsbetalningarna under exploatörens garantipolicy.')
a('The sales portal says works have started but the documents do not say how far, so a visit is about the site, the plans and the state of the build.',
  'El portal de ventas dice que las obras han comenzado, pero los documentos no indican su grado de avance, así que la visita trata de la parcela, los planos y el estado de la obra.',
  'Le portail de vente indique que les travaux ont commencé, mais les documents ne disent pas où ils en sont ; la visite porte donc sur le site, les plans et l’état du chantier.',
  'Das Verkaufsportal gibt an, dass die Bauarbeiten begonnen haben, die Dokumente nennen aber keinen Fortschritt; ein Besuch gilt daher dem Grundstück, den Plänen und dem Stand des Baus.',
  'Портал продаж сообщает, что работы начаты, но в документах не сказано, как далеко они продвинулись, поэтому просмотр посвящён участку, планам и состоянию стройки.',
  'تذكر بوابة المبيعات أن الأعمال بدأت، لكن المستندات لا تبين مدى تقدمها، لذلك تتناول الزيارة الموقع والمخططات وحالة البناء.',
  'Het verkoopportaal zegt dat de werken zijn gestart, maar de documenten vermelden niet hoe ver ze zijn, dus een bezoek gaat over het terrein, de plattegronden en de stand van de bouw.',
  'Portal sprzedażowy podaje, że prace się rozpoczęły, ale dokumenty nie mówią, jak daleko zaawansowano, więc wizyta dotyczy terenu, rzutów i stanu budowy.',
  'Salgsportalen sier at byggearbeidene har startet, men dokumentene sier ikke hvor langt de har kommet, så en visning handler om tomten, plantegningene og byggets status.',
  'Försäljningsportalen säger att arbetena har startat, men handlingarna anger inte hur långt de har kommit, så ett besök handlar om tomten, ritningarna och byggets status.')
a('Walk the site near Estepona Golf and see where each garden and terrace sits.',
  'Recorra la parcela junto a Estepona Golf y vea dónde está cada jardín y cada terraza.',
  'Parcourez le site près d’Estepona Golf et voyez où se trouve chaque jardin et chaque terrasse.',
  'Gehen Sie über das Grundstück nahe Estepona Golf und sehen Sie, wo jeder Garten und jede Terrasse liegt.',
  'Пройдитесь по участку рядом с Estepona Golf и посмотрите, где расположен каждый сад и каждая терраса.',
  'تجولوا في الموقع بالقرب من Estepona Golf وانظروا أين تقع كل حديقة وكل تراس.',
  'Loop over het terrein nabij Estepona Golf en zie waar elke tuin en elk terras ligt.',
  'Przejdą Państwo po terenie przy Estepona Golf i zobaczą, gdzie leży każdy ogród i każdy taras.',
  'Gå over tomten nær Estepona Golf og se hvor hver hage og terrasse ligger.',
  'Gå över tomten nära Estepona Golf och se var varje trädgård och terrass ligger.')
a('The development has 72 homes. The developer’s price list shows 16 of them with a price, from EUR 330,000 to EUR 525,000 plus VAT: 6 ground-floor apartments with gardens, 4 first-floor apartments and 6 duplex penthouses, with two or three bedrooms.',
  'La promoción tiene 72 viviendas. La lista de precios del promotor muestra 16 de ellas con precio, de €330000 a €525000 más IVA: 6 apartamentos con jardín en planta baja, 4 apartamentos en primera planta y 6 áticos dúplex, de dos o tres dormitorios.',
  'La résidence compte 72 logements. La liste de prix du promoteur en présente 16 avec un prix, de €330000 à €525000 hors TVA : 6 appartements avec jardin au rez-de-chaussée, 4 appartements au premier étage et 6 penthouses duplex, de deux ou trois chambres.',
  'Die Anlage hat 72 Wohnungen. Die Preisliste des Bauträgers nennt für 16 davon einen Preis, von €330000 bis €525000 zuzüglich MwSt.: 6 Erdgeschosswohnungen mit Garten, 4 Wohnungen im ersten Obergeschoss und 6 Maisonette-Penthäuser mit zwei oder drei Schlafzimmern.',
  'В комплексе 72 квартиры. В прайс-листе застройщика цена указана для 16 из них — от €330000 до €525000 без НДС: 6 квартир с садом на первом этаже, 4 квартиры на втором этаже и 6 двухуровневых пентхаусов с двумя или тремя спальнями.',
  'يضم المشروع 72 مسكنًا. وتعرض قائمة أسعار المطوّر 16 منها بأسعارها، من €330000 إلى €525000 دون ضريبة القيمة المضافة: 6 شقق بحدائق في الطابق الأرضي و4 شقق في الطابق الأول و6 بنتهاوس دوبلكس من غرفتي نوم أو ثلاث غرف نوم.',
  'Het project telt 72 woningen. De prijslijst van de ontwikkelaar toont er 16 met een prijs, van €330000 tot €525000 plus btw: 6 appartementen met tuin op de begane grond, 4 appartementen op de eerste verdieping en 6 duplex penthouses, met twee of drie slaapkamers.',
  'Inwestycja liczy 72 mieszkania. Cennik dewelopera podaje cenę dla 16 z nich, od €330000 do €525000 plus VAT: 6 mieszkań z ogrodem na parterze, 4 mieszkania na pierwszym piętrze i 6 dwupoziomowych penthouse’ów z dwiema lub trzema sypialniami.',
  'Prosjektet har 72 boliger. Utbyggerens prisliste viser 16 av dem med pris, fra €330000 til €525000 pluss mva.: 6 leiligheter med hage i første etasje, 4 leiligheter i andre etasje og 6 duplex-toppleiligheter, med to eller tre soverom.',
  'Projektet har 72 bostäder. Exploatörens prislista visar 16 av dem med pris, från €330000 till €525000 plus moms: 6 lägenheter med trädgård på bottenvåningen, 4 lägenheter på första våningen och 6 duplex-takvåningar, med två eller tre sovrum.')
a('No. The price list states its prices without VAT, and the payment terms give VAT at 10%. We confirm the taxes and purchase costs in writing.',
  'No. La lista de precios indica sus precios sin IVA, y las condiciones de pago fijan el IVA en el 10%. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. La liste de prix indique ses prix hors TVA, et les conditions de paiement fixent la TVA à 10 %. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Die Preisliste weist ihre Preise ohne MwSt. aus, und die Zahlungsbedingungen geben die MwSt. mit 10 % an. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. В прайс-листе цены указаны без НДС, а в условиях оплаты НДС составляет 10 %. Мы подтверждаем налоги и расходы на покупку в письменном виде.',
  'لا. تذكر قائمة الأسعار أسعارها دون ضريبة القيمة المضافة، وتحدد شروط الدفع الضريبة بنسبة 10%. ونؤكد الضرائب وتكاليف الشراء كتابةً.',
  'Nee. De prijslijst vermeldt haar prijzen zonder btw en de betalingsvoorwaarden geven de btw op 10%. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Nie. Cennik podaje ceny bez VAT, a warunki płatności określają VAT na 10%. Potwierdzamy podatki i koszty zakupu na piśmie.',
  'Nei. Prislisten oppgir prisene uten mva., og betalingsvilkårene oppgir mva. til 10 %. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Prislistan anger priserna utan moms, och betalningsvillkoren anger momsen till 10 %. Vi bekräftar skatter och köpkostnader skriftligen.')
a('The price list gives each home a basement garage space, two for the three-bedroom homes, and a storeroom, and three homes also have a buggy space. We confirm in writing that they are included in the price.',
  'La lista de precios asigna a cada vivienda una plaza de garaje en el sótano, dos a las de tres dormitorios, y un trastero, y tres viviendas tienen además una plaza de buggy. Confirmamos por escrito que están incluidos en el precio.',
  'La liste de prix attribue à chaque logement une place de garage en sous-sol, deux pour ceux de trois chambres, et une cave, et trois logements ont en plus une place pour voiturette. Nous confirmons par écrit qu’ils sont inclus dans le prix.',
  'Die Preisliste weist jeder Wohnung einen Garagenstellplatz im Untergeschoss zu, den Wohnungen mit drei Schlafzimmern zwei, dazu einen Abstellraum, und drei Wohnungen haben zusätzlich einen Buggy-Platz. Wir bestätigen schriftlich, dass sie im Preis enthalten sind.',
  'В прайс-листе каждой квартире закреплено место в подвальном гараже (две для квартир с тремя спальнями) и кладовая, а у трёх квартир есть ещё и место для гольф-кара. Мы письменно подтверждаем, что они включены в цену.',
  'تخصص قائمة الأسعار لكل مسكن مكانًا في مرآب القبو، ومكانين للمساكن من ثلاث غرف نوم، ومخزنًا، ولثلاثة مساكن مكانًا لعربة غولف أيضًا. ونؤكد كتابةً أنها مشمولة في السعر.',
  'De prijslijst wijst elke woning een garageplaats in de kelder toe, twee voor de woningen met drie slaapkamers, en een berging, en drie woningen hebben bovendien een buggyplaats. We bevestigen schriftelijk dat ze in de prijs zijn inbegrepen.',
  'Cennik przypisuje każdemu mieszkaniu miejsce w garażu podziemnym, dwa w mieszkaniach z trzema sypialniami, oraz komórkę lokatorską, a trzy mieszkania mają też miejsce na meleks. Potwierdzamy na piśmie, że są wliczone w cenę.',
  'Prislisten gir hver bolig en garasjeplass i kjelleren, to for boligene med tre soverom, og en bod, og tre boliger har i tillegg en plass til golfbil. Vi bekrefter skriftlig at de er inkludert i prisen.',
  'Prislistan ger varje bostad en garageplats i källaren, två för bostäderna med tre sovrum, och ett förråd, och tre bostäder har dessutom en plats för golfbil. Vi bekräftar skriftligen att de ingår i priset.')
a('Are the gardens landscaped?', '¿Están ajardinados los jardines?', 'Les jardins sont-ils aménagés ?', 'Sind die Gärten angelegt?',
  'Обустроены ли сады?', 'هل الحدائق مهيأة بالنباتات؟', 'Zijn de tuinen aangelegd?', 'Czy ogrody są urządzone?',
  'Er hagene opparbeidet?', 'Är trädgårdarna anlagda?')
a('The ground-floor plans mark the garden as unlandscaped space, and the quality specification describes landscaping only for the communal areas. We ask what is delivered in each private garden.',
  'Los planos de planta baja marcan el jardín como espacio sin ajardinar, y la memoria de calidades describe el ajardinamiento solo para las zonas comunes. Preguntamos qué se entrega en cada jardín privado.',
  'Les plans du rez-de-chaussée indiquent le jardin comme espace non aménagé, et le descriptif de qualité ne décrit l’aménagement paysager que pour les parties communes. Nous demandons ce qui est livré dans chaque jardin privatif.',
  'Die Erdgeschossgrundrisse kennzeichnen den Garten als nicht angelegte Fläche, und die Bau- und Ausstattungsbeschreibung nennt eine Begrünung nur für die Gemeinschaftsflächen. Wir fragen nach, was in jedem privaten Garten übergeben wird.',
  'На планах первого этажа сад обозначен как необустроенная территория, а в описании качества озеленение указано только для общих зон. Мы уточняем, что передаётся в каждом частном саду.',
  'تُظهر مخططات الطابق الأرضي الحديقة كمساحة غير مهيأة بالنباتات، ولا تصف مواصفات الجودة التشجير إلا للمناطق المشتركة. نستفسر عما يُسلَّم في كل حديقة خاصة.',
  'De plattegronden van de begane grond geven de tuin aan als niet-aangelegde ruimte, en de kwaliteitsomschrijving beschrijft beplanting alleen voor de gemeenschappelijke zones. We vragen wat er in elke privétuin wordt opgeleverd.',
  'Rzuty parteru oznaczają ogród jako teren nieurządzony, a opis jakości wykonania opisuje zagospodarowanie zieleni tylko dla części wspólnych. Pytamy, co jest przekazywane w każdym ogrodzie prywatnym.',
  'Plantegningene for første etasje merker hagen som uopparbeidet areal, og kvalitetsbeskrivelsen omtaler opparbeiding bare for fellesarealene. Vi spør hva som leveres i hver private hage.',
  'Planritningarna för bottenvåningen markerar trädgården som ej anlagd yta, och kvalitetsbeskrivningen omtalar anläggning endast för de gemensamma ytorna. Vi frågar vad som lämnas över i varje privat trädgård.')
a('No document we hold gives a completion date. The sales portal says works have started and the brochure calls it a construction project, so we ask for the licence, the state of the works and the contractual date.',
  'Ningún documento de que disponemos da una fecha de finalización. El portal de ventas dice que las obras han comenzado y el folleto lo llama proyecto de construcción, así que pedimos la licencia, el estado de las obras y la fecha contractual.',
  'Aucun document dont nous disposons ne donne de date d’achèvement. Le portail de vente indique que les travaux ont commencé et la brochure parle d’un projet de construction ; nous demandons donc le permis, l’état des travaux et la date contractuelle.',
  'Kein uns vorliegendes Dokument nennt einen Fertigstellungstermin. Das Verkaufsportal gibt an, dass die Bauarbeiten begonnen haben, und die Broschüre spricht von einem Bauprojekt; deshalb fordern wir die Genehmigung, den Stand der Arbeiten und den vertraglichen Termin an.',
  'Ни в одном из имеющихся у нас документов нет даты завершения. Портал продаж сообщает, что работы начаты, а в брошюре комплекс назван проектом строительства, поэтому мы запрашиваем разрешение, ход работ и договорную дату.',
  'لا يذكر أي مستند لدينا موعد الانتهاء. تشير بوابة المبيعات إلى أن الأعمال بدأت ويصف الكتيّب المشروع بأنه مشروع بناء، لذلك نطلب الرخصة وحالة الأعمال والتاريخ التعاقدي.',
  'Geen enkel document waarover wij beschikken geeft een opleverdatum. Het verkoopportaal zegt dat de werken zijn gestart en de brochure noemt het een bouwproject, dus we vragen om de vergunning, de stand van de werken en de contractuele datum.',
  'Żaden z posiadanych przez nas dokumentów nie podaje terminu zakończenia. Portal sprzedażowy podaje, że prace się rozpoczęły, a broszura nazywa inwestycję projektem budowlanym, dlatego prosimy o pozwolenie, stan prac i termin umowny.',
  'Ingen av dokumentene vi har oppgir en ferdigstillelsesdato. Salgsportalen sier at byggearbeidene har startet, og brosjyren kaller det et byggeprosjekt, så vi ber om tillatelsen, byggets status og den kontraktsfestede datoen.',
  'Ingen av de handlingar vi har anger något färdigställandedatum. Försäljningsportalen säger att arbetena har startat och broschyren kallar det ett byggprojekt, så vi ber om bygglovet, arbetenas status och det avtalade datumet.')
a('The reservation is EUR 6,000 plus 10% VAT. Then 30% plus VAT on the purchase contract and 70% plus VAT at the notary on completion.',
  'La reserva es de €6000 más el 10% de IVA. Luego, el 30% más IVA con el contrato de compraventa y el 70% más IVA ante notario a la finalización.',
  'La réservation est de €6000 plus 10 % de TVA. Ensuite, 30 % hors TVA au contrat de vente et 70 % hors TVA chez le notaire à l’achèvement.',
  'Die Reservierung beträgt €6000 zuzüglich 10 % MwSt. Dann 30 % zuzüglich MwSt. beim Kaufvertrag und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar.',
  'Бронирование стоит €6000 плюс НДС 10 %. Затем 30 % плюс НДС по договору купли-продажи и 70 % плюс НДС у нотариуса при завершении.',
  'الحجز €6000 زائد ضريبة القيمة المضافة 10%. ثم 30% زائد الضريبة عند عقد الشراء و70% زائد الضريبة أمام كاتب العدل عند الإتمام.',
  'De reservering bedraagt €6000 plus 10% btw. Daarna 30% plus btw bij de koopovereenkomst en 70% plus btw bij oplevering ten overstaan van de notaris.',
  'Rezerwacja wynosi €6000 plus 10% VAT. Następnie 30% plus VAT przy umowie sprzedaży i 70% plus VAT u notariusza, przy akcie notarialnym.',
  'Reservasjonen er €6000 pluss 10 % mva. Deretter 30 % pluss mva. ved kjøpekontrakten og 70 % pluss mva. hos notarius ved overtakelse.',
  'Reservationen är €6000 plus 10 % moms. Därefter 30 % plus moms vid köpeavtalet och 70 % plus moms hos notarien vid tillträdet.')

json.dump(T, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('translations', len(T), 'of', len(TODO))
missing = [k for k in TODO if k not in T]
print('missing', len(missing))
for k in missing: print('  ', repr(k[:120]))
