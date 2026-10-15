# -*- coding: utf-8 -*-
"""Acacia Residences: the strings the translation memory did not have.

Same shape as k_higueron.py, but each translation is keyed by the English text it
translates (an exact match, or a prefix that is unique in the to-do list) instead of by
position, so reordering the English does not shift a translation onto the wrong string.

Tokens expand per language:  {E470000} money   {N5} number with the locale's decimal mark
{U} m2   {KM} km   {P7} the percentage as this locale writes it ("7%", "7 %").
Run:  python3 tools/import/k_acacia.py <scratch dir>     (reads <dir>/todo.json, writes <dir>/tr_a.json)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
KM = {'ru': 'км', 'ar': 'كم'}
PCT = {'es': '{}%', 'fr': '{} %', 'de': '{} %', 'ru': '{} %', 'ar': '{}%', 'nl': '{}%', 'pl': '{}%', 'no': '{} %', 'sv': '{} %'}
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace(',', GROUP[l]).replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    text = text.replace('{P7}', PCT[l].format(7))
    return text.replace('{U}', UNIT[l]).replace('{KM}', KM.get(l, 'km'))


def find(hint):
    if hint in todo:
        return hint
    hits = [t for t in todo if t.startswith(hint)]
    assert len(hits) == 1, (hint, len(hits))
    return hits[0]


def a(hint, *tr):
    en = find(hint)
    assert len(tr) == 9, (hint, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(hint):
    en = find(hint)
    T[en] = {l: en for l in LOCS}

# ---------------------------------------------------------------- names, card, price strings
same('Acacia Residences')
same('Acacia')
same('Acacia <em>Residences</em>')
a('Ten finished two-bedroom apartments, ground-floor homes',
  "Diez apartamentos terminados de dos dormitorios, viviendas en planta baja y áticos dúplex en Nueva Andalucía, Marbella, cada uno con terraza, una plaza de aparcamiento subterráneo y un trastero, en un complejo con dos piscinas y un gimnasio. El edificio figura como terminado. Desde {E470000} más el {P7} de ITP.",
  "Dix appartements achevés de deux chambres, logements en rez-de-chaussée et penthouses duplex à Nueva Andalucía, Marbella, chacun avec une terrasse, une place de stationnement en sous-sol et un débarras, dans une résidence avec deux piscines et une salle de sport. L’immeuble est présenté comme achevé. À partir de {E470000} plus {P7} d’ITP.",
  "Zehn fertiggestellte Wohnungen mit zwei Schlafzimmern in Nueva Andalucía, Marbella – im Erdgeschoss, im ersten Obergeschoss und als Maisonette-Penthäuser –, jeweils mit Terrasse, einem Tiefgaragenstellplatz und einem Abstellraum, in einer Anlage mit zwei Pools und einem Fitnessraum. Das Gebäude ist als fertiggestellt aufgeführt. Ab {E470000} zuzüglich {P7} ITP.",
  "Десять готовых квартир с двумя спальнями в Нуэва-Андалусии, Марбелья: на первом и втором этажах и двухуровневые пентхаусы. У каждой есть терраса, подземное парковочное место и кладовая, а в комплексе — два бассейна и тренажёрный зал. Здание указано как завершённое. От {E470000} плюс {P7} ITP.",
  "عشر شقق جاهزة من غرفتي نوم في نويفا أندلوثيا بماربيا، في الطابق الأرضي والطابق الأول، إضافة إلى بنتهاوس دوبلكس، لكل منها تراس وموقف سيارات تحت الأرض ومخزن، ضمن مجمع يضم مسبحين وصالة رياضية. يُدرج المبنى على أنه مكتمل. ابتداءً من {E470000} زائد {P7} ضريبة ITP.",
  "Tien opgeleverde appartementen met twee slaapkamers in Nueva Andalucía, Marbella: woningen op de begane grond, op de eerste verdieping en duplexpenthouses, elk met een terras, een ondergrondse parkeerplaats en een berging, in een complex met twee zwembaden en een gym. Het gebouw staat vermeld als opgeleverd. Vanaf {E470000} plus {P7} ITP.",
  "Dziesięć ukończonych mieszkań z dwiema sypialniami w Nueva Andalucía, Marbella – na parterze, na pierwszym piętrze i w formie dwupoziomowych penthouse’ów – każde z tarasem, podziemnym miejscem parkingowym i komórką lokatorską, w kompleksie z dwoma basenami i siłownią. Budynek figuruje jako ukończony. Od {E470000} plus {P7} ITP.",
  "Ti ferdigstilte leiligheter med to soverom i Nueva Andalucía, Marbella – i første etasje, andre etasje og som toppleiligheter i to plan – hver med terrasse, en parkeringsplass under bakken og en bod, i et anlegg med to bassenger og et treningsrom. Bygget er oppført som ferdig. Fra {E470000} pluss {P7} ITP.",
  "Tio färdigställda lägenheter med två sovrum i Nueva Andalucía, Marbella – på bottenvåningen, på första våningen och som takvåningar i två plan – var och en med terrass, en parkeringsplats under jord och ett förråd, i ett område med två pooler och ett gym. Byggnaden anges som färdigställd. Från {E470000} plus {P7} ITP.")
a('Ten finished two-bedroom homes at Nueva Andalucía, Marbella, with terraces',
  "Diez viviendas terminadas de dos dormitorios en Nueva Andalucía, Marbella, con terrazas, una plaza de aparcamiento y un trastero cada una, dos piscinas y un gimnasio, desde {E470000} más el {P7} de ITP.",
  "Dix logements achevés de deux chambres à Nueva Andalucía, Marbella, avec terrasses, une place de stationnement et un débarras chacun, deux piscines et une salle de sport, à partir de {E470000} plus {P7} d’ITP.",
  "Zehn fertiggestellte Wohnungen mit zwei Schlafzimmern in Nueva Andalucía, Marbella, mit Terrassen, je einem Stellplatz und einem Abstellraum, zwei Pools und einem Fitnessraum, ab {E470000} zuzüglich {P7} ITP.",
  "Десять готовых квартир с двумя спальнями в Нуэва-Андалусии, Марбелья: террасы, по одному парковочному месту и кладовой у каждой, два бассейна и тренажёрный зал, от {E470000} плюс {P7} ITP.",
  "عشرة مساكن جاهزة من غرفتي نوم في نويفا أندلوثيا بماربيا، بتراسات وموقف سيارات ومخزن لكل مسكن، ومسبحان وصالة رياضية، ابتداءً من {E470000} زائد {P7} ضريبة ITP.",
  "Tien opgeleverde woningen met twee slaapkamers in Nueva Andalucía, Marbella, elk met terras, een parkeerplaats en een berging, twee zwembaden en een gym, vanaf {E470000} plus {P7} ITP.",
  "Dziesięć ukończonych lokali z dwiema sypialniami w Nueva Andalucía, Marbella, z tarasami, miejscem parkingowym i komórką lokatorską w każdym, dwoma basenami i siłownią, od {E470000} plus {P7} ITP.",
  "Ti ferdigstilte boliger med to soverom i Nueva Andalucía, Marbella, hver med terrasse, en parkeringsplass og en bod, to bassenger og et treningsrom, fra {E470000} pluss {P7} ITP.",
  "Tio färdigställda bostäder med två sovrum i Nueva Andalucía, Marbella, var och en med terrass, en parkeringsplats och ett förråd, två pooler och ett gym, från {E470000} plus {P7} ITP.")
a('Finished two-bedroom apartments and penthouses at Nueva Andalucía, Marbella, from',
  "Apartamentos y áticos terminados de dos dormitorios en Nueva Andalucía, Marbella, desde {E470000} más el {P7} de ITP.",
  "Appartements et penthouses achevés de deux chambres à Nueva Andalucía, Marbella, à partir de {E470000} plus {P7} d’ITP.",
  "Fertiggestellte Wohnungen und Penthäuser mit zwei Schlafzimmern in Nueva Andalucía, Marbella, ab {E470000} zuzüglich {P7} ITP.",
  "Готовые квартиры и пентхаусы с двумя спальнями в Нуэва-Андалусии, Марбелья, от {E470000} плюс {P7} ITP.",
  "شقق وبنتهاوس جاهزة من غرفتي نوم في نويفا أندلوثيا بماربيا، ابتداءً من {E470000} زائد {P7} ضريبة ITP.",
  "Opgeleverde appartementen en penthouses met twee slaapkamers in Nueva Andalucía, Marbella, vanaf {E470000} plus {P7} ITP.",
  "Ukończone apartamenty i penthouse’y z dwiema sypialniami w Nueva Andalucía, Marbella, od {E470000} plus {P7} ITP.",
  "Ferdigstilte leiligheter og toppleiligheter med to soverom i Nueva Andalucía, Marbella, fra {E470000} pluss {P7} ITP.",
  "Färdigställda lägenheter och takvåningar med två sovrum i Nueva Andalucía, Marbella, från {E470000} plus {P7} ITP.")
a('From EUR 470,000 + 7% ITP',
  "Desde {E470000} + {P7} ITP", "À partir de {E470000} + {P7} ITP", "Ab {E470000} + {P7} ITP", "От {E470000} + {P7} ITP",
  "ابتداءً من {E470000} + {P7} ITP", "Vanaf {E470000} + {P7} ITP", "Od {E470000} + {P7} ITP", "Fra {E470000} + {P7} ITP", "Från {E470000} + {P7} ITP")
a('EUR 470,000 + 7% ITP', *(["{E470000} + {P7} ITP"] * 9))
a('EUR 470,000 - EUR 600,000 + 7% ITP', *(["{E470000} - {E600000} + {P7} ITP"] * 9))
a('Ten finished two-bedroom apartments and penthouses at Nueva Andalucía, with terraces',
  "Diez apartamentos y áticos terminados de dos dormitorios en Nueva Andalucía, con terrazas de {N38} a {N65} {U}, una plaza de aparcamiento y un trastero cada uno, dos piscinas y un gimnasio.",
  "Dix appartements et penthouses achevés de deux chambres à Nueva Andalucía, avec des terrasses de {N38} à {N65} {U}, une place de stationnement et un débarras chacun, deux piscines et une salle de sport.",
  "Zehn fertiggestellte Wohnungen und Penthäuser mit zwei Schlafzimmern in Nueva Andalucía, mit Terrassen von {N38} bis {N65} {U}, je einem Stellplatz und einem Abstellraum, zwei Pools und einem Fitnessraum.",
  "Десять готовых квартир и пентхаусов с двумя спальнями в Нуэва-Андалусии: террасы от {N38} до {N65} {U}, по одному парковочному месту и кладовой у каждой, два бассейна и тренажёрный зал.",
  "عشر شقق وبنتهاوس جاهزة من غرفتي نوم في نويفا أندلوثيا، بتراسات من {N38} إلى {N65} {U}، وموقف سيارات ومخزن لكل منها، ومسبحان وصالة رياضية.",
  "Tien opgeleverde appartementen en penthouses met twee slaapkamers in Nueva Andalucía, met terrassen van {N38} tot {N65} {U}, elk met een parkeerplaats en een berging, twee zwembaden en een gym.",
  "Dziesięć ukończonych apartamentów i penthouse’ów z dwiema sypialniami w Nueva Andalucía, z tarasami od {N38} do {N65} {U}, miejscem parkingowym i komórką lokatorską w każdym, dwoma basenami i siłownią.",
  "Ti ferdigstilte leiligheter og toppleiligheter med to soverom i Nueva Andalucía, med terrasser på {N38} til {N65} {U}, en parkeringsplass og en bod hver, to bassenger og et treningsrom.",
  "Tio färdigställda lägenheter och takvåningar med två sovrum i Nueva Andalucía, med terrasser på {N38} till {N65} {U}, en parkeringsplats och ett förråd vardera, två pooler och ett gym.")

# ---------------------------------------------------------------- image alt text, captions and the media note
a('Photograph of white apartment blocks with curved-tile roofs',
  "Fotografía de bloques blancos de apartamentos con tejados de teja curva que ascienden por una ladera aterrazada sobre la piscina comunitaria",
  "Photographie de blocs d’appartements blancs aux toits de tuiles rondes qui montent sur une colline en terrasses au-dessus de la piscine commune",
  "Foto weißer Apartmentblöcke mit Hohlziegeldächern, die an einem terrassierten Hang oberhalb des Gemeinschaftspools ansteigen",
  "Фотография белых жилых блоков с черепичными крышами, поднимающихся по террасированному склону над общим бассейном",
  "صورة لمبانٍ سكنية بيضاء بأسقف من القرميد المقوّس تتدرج على سفح مدرّج فوق المسبح المشترك",
  "Foto van witte appartementenblokken met daken van gebogen dakpannen, die op een terrasvormige helling boven het gemeenschappelijke zwembad oplopen",
  "Zdjęcie białych bloków z dachami z dachówki łukowej, wznoszących się tarasowym zboczem nad basenem wspólnym",
  "Fotografi av hvite leilighetsbygg med tak av buede takstein som stiger opp en terrassert skråning over det felles bassenget",
  "Fotografi av vita lägenhetshus med tak av välvda tegelpannor som stiger uppför en terrasserad sluttning ovanför den gemensamma poolen")
a('Aerial photograph of the complex on its hillside',
  "Fotografía aérea del complejo en su ladera, con la costa y el mar a lo lejos",
  "Photographie aérienne de la résidence sur sa colline, avec la côte et la mer au loin",
  "Luftaufnahme der Anlage an ihrem Hang, in der Ferne die Küste und das Meer",
  "Фотография комплекса на склоне с высоты, вдали видны побережье и море",
  "صورة جوية للمجمع على سفحه، وفي البعيد الساحل والبحر",
  "Luchtfoto van het complex op zijn heuvel, met in de verte de kust en de zee",
  "Zdjęcie lotnicze kompleksu na zboczu, w oddali wybrzeże i morze",
  "Flyfoto av anlegget i skråningen, med kysten og havet i det fjerne",
  "Flygfoto över området i sluttningen, med kusten och havet i fjärran")
a('Photograph of a terrace under a timber pergola',
  "Fotografía de una terraza bajo una pérgola de madera con un sofá largo blanco, sillones y vistas a las colinas y a la costa",
  "Photographie d’une terrasse sous une pergola en bois avec un long canapé blanc, des fauteuils et une vue sur les collines et la côte",
  "Foto einer Terrasse unter einer Holzpergola mit einem langen weißen Sofa, Sesseln und Blick auf die Hügel und die Küste",
  "Фотография террасы под деревянной перголой с длинным белым диваном, креслами и видом на холмы и побережье",
  "صورة لتراس تحت برغولا خشبية بأريكة بيضاء طويلة ومقاعد وإطلالة على التلال والساحل",
  "Foto van een terras onder een houten pergola met een lange witte bank, fauteuils en uitzicht op de heuvels en de kust",
  "Zdjęcie tarasu pod drewnianą pergolą z długą białą sofą, fotelami i widokiem na wzgórza i wybrzeże",
  "Fotografi av en terrasse under en tre-pergola med en lang hvit sofa, lenestoler og utsikt over åsene og kysten",
  "Fotografi av en terrass under en pergola av trä med en lång vit soffa, fåtöljer och utsikt över kullarna och kusten")
a('Photograph of a bedroom with twin beds',
  "Fotografía de un dormitorio con dos camas individuales bajo un cabecero decorado con discos de fibra trenzada y grandes ventanales",
  "Photographie d’une chambre à lits jumeaux sous une tête de lit ornée de disques tressés, avec de grandes fenêtres",
  "Foto eines Schlafzimmers mit zwei Einzelbetten unter einem mit geflochtenen Scheiben dekorierten Kopfteil und großen Fenstern",
  "Фотография спальни с двумя односпальными кроватями под изголовьем, украшенным плетёными дисками, и высокими окнами",
  "صورة لغرفة نوم بسريرين منفردين تحت لوح رأس تزيّنه أقراص منسوجة، ونوافذ عالية",
  "Foto van een slaapkamer met twee eenpersoonsbedden onder een hoofdbord versierd met gevlochten schijven, en hoge ramen",
  "Zdjęcie sypialni z dwoma łóżkami pojedynczymi pod zagłówkiem ozdobionym plecionymi krążkami i z wysokimi oknami",
  "Fotografi av et soverom med to enkeltsenger under en hodegavl pyntet med flettede skiver, og høye vinduer",
  "Fotografi av ett sovrum med två enkelsängar under en sänggavel dekorerad med flätade skivor, och höga fönster")
a('Photographs of the finished complex and of furnished homes',
  "Fotografías del complejo terminado y de viviendas amuebladas, y los planos de los tres tipos de vivienda.",
  "Photographies de la résidence achevée et de logements meublés, et plans des trois types de logement.",
  "Fotos der fertiggestellten Anlage und möblierter Wohnungen sowie die Grundrisse der drei Wohnungstypen.",
  "Фотографии готового комплекса и меблированных квартир, а также планировки трёх типов жилья.",
  "صور للمجمع المكتمل ولمساكن مفروشة، ومخططات أنواع المساكن الثلاثة.",
  "Foto’s van het opgeleverde complex en van gemeubileerde woningen, en de plattegronden van de drie woningtypen.",
  "Zdjęcia ukończonego kompleksu i umeblowanych lokali oraz rzuty trzech typów lokali.",
  "Bilder av det ferdige anlegget og av møblerte boliger, og plantegningene for de tre boligtypene.",
  "Bilder av det färdiga området och av möblerade bostäder, och planritningarna för de tre bostadstyperna.")
a('All the pictures are photographs of the built complex',
  "Todas las imágenes son fotografías del complejo construido y de viviendas amuebladas. El mobiliario y la decoración no se mencionan en la lista de precios, y confirmamos qué está incluido. Los planos son los del promotor, fechados el 28 de febrero de 2023, y sus superficies difieren de las de la lista de precios, como explican las notas sobre las superficies. Los nombres de las estancias en los planos están en español.",
  "Toutes les images sont des photographies de la résidence construite et de logements meublés. Le mobilier et la décoration ne sont pas mentionnés dans la liste de prix, et nous confirmons ce qui est inclus. Les plans sont ceux du promoteur, datés du 28 février 2023, et leurs surfaces diffèrent de celles de la liste de prix, comme l’expliquent les notes sur les surfaces. Les noms des pièces sur les plans sont en espagnol.",
  "Alle Bilder sind Fotografien der gebauten Anlage und möblierter Wohnungen. Möblierung und Dekoration werden in der Preisliste nicht erwähnt, und wir bestätigen, was enthalten ist. Die Grundrisse stammen vom Bauträger und sind auf den 28. Februar 2023 datiert; ihre Flächen weichen von denen der Preisliste ab, wie die Hinweise zu den Flächen erläutern. Die Raumbezeichnungen in den Grundrissen sind auf Spanisch.",
  "Все изображения — фотографии построенного комплекса и меблированных квартир. Мебель и оформление в прайс-листе не упоминаются, и мы уточняем, что входит в стоимость. Планировки — это планы застройщика от 28 февраля 2023 года; указанные на них площади отличаются от площадей в прайс-листе, как объясняется в примечаниях о площадях. Названия помещений на планах даны по-испански.",
  "جميع الصور فوتوغرافية للمجمع المبني ولمساكن مفروشة. لا تذكر قائمة الأسعار الأثاث والتنسيق، ونؤكد ما هو مشمول. المخططات هي مخططات المطوّر المؤرخة في 28 فبراير 2023، وتختلف مساحاتها عن مساحات قائمة الأسعار كما توضح الملاحظات عن المساحات. أسماء الغرف على المخططات بالإسبانية.",
  "Alle beelden zijn foto’s van het gebouwde complex en van gemeubileerde woningen. Meubilair en decoratie worden in de prijslijst niet genoemd, en wij bevestigen wat is inbegrepen. De plattegronden zijn die van de ontwikkelaar, gedateerd 28 februari 2023, en de oppervlakten erop wijken af van die in de prijslijst, zoals de toelichting bij de oppervlakten uitlegt. De ruimtenamen op de plattegronden zijn in het Spaans.",
  "Wszystkie obrazy to zdjęcia ukończonego kompleksu i umeblowanych lokali. Meble i dekoracje nie są wymienione w cenniku, a my potwierdzamy, co jest w cenie. Rzuty pochodzą od dewelopera i są datowane na 28 lutego 2023 r.; podane na nich powierzchnie różnią się od powierzchni z cennika, jak wyjaśniają uwagi o powierzchniach. Nazwy pomieszczeń na rzutach są po hiszpańsku.",
  "Alle bildene er fotografier av det ferdige anlegget og av møblerte boliger. Møbler og dekor er ikke nevnt i prislisten, og vi bekrefter hva som er inkludert. Plantegningene er utbyggerens, datert 28. februar 2023, og arealene på dem avviker fra prislistens, slik merknadene om arealene forklarer. Romnavnene på plantegningene er på spansk.",
  "Alla bilder är fotografier av det färdiga området och av möblerade bostäder. Möbler och inredning nämns inte i prislistan, och vi bekräftar vad som ingår. Planritningarna är exploatörens, daterade den 28 februari 2023, och ytorna på dem skiljer sig från prislistans, vilket anteckningarna om ytorna förklarar. Rumsnamnen på planritningarna är på spanska.")

# ---------------------------------------------------------------- gallery alt text and captions
a('The complex and the coast',
  "El complejo y la costa", "La résidence et la côte", "Die Anlage und die Küste", "Комплекс и побережье", "المجمع والساحل",
  "Het complex en de kust", "Kompleks i wybrzeże", "Anlegget og kysten", "Området och kusten")
a('Photograph of two pools in landscaped gardens',
  "Fotografía de dos piscinas en jardines cuidados bajo un bloque blanco, con colinas arboladas al fondo",
  "Photographie de deux piscines dans des jardins paysagers au pied d’un bloc blanc, avec des collines boisées derrière",
  "Foto von zwei Pools in gepflegten Gärten unterhalb eines weißen Blocks, dahinter bewaldete Hügel",
  "Фотография двух бассейнов в благоустроенных садах под белым блоком, позади — поросшие лесом холмы",
  "صورة لمسبحين في حدائق منسّقة أسفل مبنى أبيض، وخلفهما تلال مكسوّة بالأشجار",
  "Foto van twee zwembaden in verzorgde tuinen onder een wit blok, met beboste heuvels erachter",
  "Zdjęcie dwóch basenów w zadbanych ogrodach pod białym blokiem, a za nimi zalesione wzgórza",
  "Fotografi av to bassenger i opparbeidede hager under et hvitt bygg, med skogkledde åser bak",
  "Fotografi av två pooler i anlagda trädgårdar under ett vitt hus, med skogsklädda kullar bakom")
a('The gardens and the two pools',
  "Los jardines y las dos piscinas", "Les jardins et les deux piscines", "Die Gärten und die beiden Pools", "Сады и два бассейна", "الحدائق والمسبحان",
  "De tuinen en de twee zwembaden", "Ogrody i dwa baseny", "Hagene og de to bassengene", "Trädgårdarna och de två poolerna")
a('Aerial photograph at night of a communal terrace',
  "Fotografía aérea nocturna de una terraza comunitaria con muros blancos curvos, caminos iluminados y palmeras",
  "Photographie aérienne de nuit d’une terrasse commune aux murs blancs incurvés, aux allées éclairées et aux palmiers",
  "Luftaufnahme bei Nacht einer Gemeinschaftsterrasse mit geschwungenen weißen Mauern, beleuchteten Wegen und Palmen",
  "Ночная фотография общей террасы с изогнутыми белыми стенами, освещёнными дорожками и пальмами, снятая с высоты",
  "صورة جوية ليلية لتراس مشترك بجدران بيضاء منحنية وممرات مضاءة ونخيل",
  "Luchtfoto bij nacht van een gemeenschappelijk terras met gebogen witte muren, verlichte paden en palmbomen",
  "Nocne zdjęcie lotnicze tarasu wspólnego z łukowymi białymi murami, oświetlonymi ścieżkami i palmami",
  "Flyfoto om natten av en felles terrasse med buede hvite murer, opplyste stier og palmer",
  "Flygfoto på natten över en gemensam terrass med böjda vita murar, upplysta stigar och palmer")
a('A communal terrace at night',
  "Una terraza comunitaria de noche", "Une terrasse commune la nuit", "Eine Gemeinschaftsterrasse bei Nacht", "Общая терраса ночью", "تراس مشترك في الليل",
  "Een gemeenschappelijk terras bij nacht", "Taras wspólny nocą", "En felles terrasse om natten", "En gemensam terrass på natten")
a('Photograph of the gym with weight machines',
  "Fotografía del gimnasio con máquinas de musculación, bicicletas estáticas y luminarias circulares en un techo oscuro",
  "Photographie de la salle de sport avec appareils de musculation, vélos d’appartement et luminaires circulaires sur un plafond sombre",
  "Foto des Fitnessraums mit Kraftgeräten, Spinningbikes und Ringleuchten an einer dunklen Decke",
  "Фотография тренажёрного зала с силовыми тренажёрами, велотренажёрами и кольцевыми светильниками на тёмном потолке",
  "صورة للصالة الرياضية بأجهزة القوة ودراجات التمارين ومصابيح حلقية على سقف داكن",
  "Foto van de gym met krachtapparaten, hometrainers en ringlampen aan een donker plafond",
  "Zdjęcie siłowni z maszynami do ćwiczeń siłowych, rowerami treningowymi i okrągłymi oprawami na ciemnym suficie",
  "Fotografi av treningsrommet med styrkemaskiner, spinningsykler og ringlamper i et mørkt tak",
  "Fotografi av gymmet med styrkemaskiner, motionscyklar och ringlampor i ett mörkt tak")
a('Photograph of a room with curved white walls',
  "Fotografía de una sala con paredes blancas curvas, luminarias circulares, pelotas de ejercicio y ventanas que dan a la vegetación",
  "Photographie d’une salle aux murs blancs incurvés, avec luminaires circulaires, ballons d’exercice et fenêtres donnant sur la végétation",
  "Foto eines Raums mit geschwungenen weißen Wänden, Ringleuchten, Gymnastikbällen und Fenstern zur Bepflanzung",
  "Фотография зала с изогнутыми белыми стенами, кольцевыми светильниками, фитнес-мячами и окнами, выходящими на зелень",
  "صورة لقاعة بجدران بيضاء منحنية ومصابيح حلقية وكرات تمارين ونوافذ تطل على النباتات",
  "Foto van een ruimte met gebogen witte muren, ringlampen, oefenballen en ramen op de beplanting",
  "Zdjęcie sali z łukowymi białymi ścianami, okrągłymi oprawami, piłkami do ćwiczeń i oknami wychodzącymi na zieleń",
  "Fotografi av et rom med buede hvite vegger, ringlamper, treningsballer og vinduer mot beplantningen",
  "Fotografi av ett rum med böjda vita väggar, ringlampor, träningsbollar och fönster mot grönskan")
a('An exercise room',
  "Una sala de ejercicio", "Une salle d’exercice", "Ein Übungsraum", "Зал для занятий", "قاعة تمارين",
  "Een oefenruimte", "Sala do ćwiczeń", "Et treningsrom", "Ett träningsrum")
a('Photograph of a covered open-air pavilion',
  "Fotografía de un pabellón abierto cubierto, con techo de caña, una parrilla de obra y un banco a lo largo de la pared",
  "Photographie d’un pavillon ouvert couvert, avec un toit de chaume, un gril maçonné et un banc le long du mur",
  "Foto eines überdachten offenen Pavillons mit Schilfdach, einem gemauerten Grill und einer Bank an der Wand",
  "Фотография крытого открытого павильона с тростниковой крышей, встроенным грилем и скамьёй вдоль стены",
  "صورة لجناح مفتوح مسقوف بسقف من القصب، مع شواية مبنية ومقعد ممتد على طول الجدار",
  "Foto van een overdekt open paviljoen met een rieten dak, een ingebouwde grill en een bank langs de muur",
  "Zdjęcie zadaszonego otwartego pawilonu z dachem z trzciny, wbudowanym grillem i ławką wzdłuż ściany",
  "Fotografi av en overbygd åpen paviljong med stråtak, en innmurt grill og en benk langs veggen",
  "Fotografi av en övertäckt öppen paviljong med vasstak, en inbyggd grill och en bänk längs väggen")
a('A covered pavilion with a grill',
  "Un pabellón cubierto con parrilla", "Un pavillon couvert avec un gril", "Ein überdachter Pavillon mit Grill", "Крытый павильон с грилем", "جناح مسقوف مع شواية",
  "Een overdekt paviljoen met een grill", "Zadaszony pawilon z grillem", "En overbygd paviljong med grill", "En övertäckt paviljong med grill")
a('Photograph of a living and dining room',
  "Fotografía de un salón comedor con mesa de comedor, sillones blancos y un sofá, que se abre a una terraza",
  "Photographie d’un séjour avec salle à manger, une table, des fauteuils blancs et un canapé, ouvert sur une terrasse",
  "Foto eines Wohn- und Essbereichs mit Esstisch, weißen Sesseln und einem Sofa, der sich zu einer Terrasse öffnet",
  "Фотография гостиной со столовой: обеденный стол, белые кресла и диван, выход на террасу",
  "صورة لغرفة معيشة وطعام بطاولة طعام ومقاعد بيضاء وأريكة، تنفتح على تراس",
  "Foto van een woon- en eetkamer met een eettafel, witte fauteuils en een bank, die uitkomt op een terras",
  "Zdjęcie salonu z jadalnią: stół, białe fotele i sofa, z wyjściem na taras",
  "Fotografi av en stue med spiseplass, spisebord, hvite lenestoler og en sofa, som åpner seg mot en terrasse",
  "Fotografi av ett vardagsrum med matplats, matbord, vita fåtöljer och en soffa, som öppnar sig mot en terrass")
a('Photograph of a white kitchen',
  "Fotografía de una cocina blanca con una columna de horno y microondas, una placa de inducción, una campana extractora y una puerta acristalada a la terraza",
  "Photographie d’une cuisine blanche avec une colonne four et micro-ondes, une plaque à induction, une hotte et une porte vitrée donnant sur la terrasse",
  "Foto einer weißen Küche mit Backofen-Mikrowellen-Hochschrank, Induktionskochfeld, Dunstabzugshaube und einer Glastür zur Terrasse",
  "Фотография белой кухни с колонной духовки и микроволновой печи, индукционной варочной панелью, вытяжкой и стеклянной дверью на террасу",
  "صورة لمطبخ أبيض بوحدة طويلة تضم فرنًا وميكروويف، وموقد حثّي وشفاط، وباب زجاجي يفتح على التراس",
  "Foto van een witte keuken met een hoge kast met oven en magnetron, een inductiekookplaat, een afzuigkap en een glazen deur naar het terras",
  "Zdjęcie białej kuchni z zabudową z piekarnikiem i mikrofalówką, płytą indukcyjną, okapem i przeszklonymi drzwiami na taras",
  "Fotografi av et hvitt kjøkken med et høyskap med ovn og mikrobølgeovn, en induksjonstopp, en ventilator og en glassdør til terrassen",
  "Fotografi av ett vitt kök med ett högskåp med ugn och mikrovågsugn, en induktionshäll, en köksfläkt och en glasdörr till terrassen")
a('Photograph of a double bedroom with a glazed door',
  "Fotografía de un dormitorio doble con una puerta acristalada a la terraza y un espejo de fibra trenzada sobre la cama",
  "Photographie d’une chambre double avec une porte vitrée donnant sur la terrasse et un miroir en fibres tressées au-dessus du lit",
  "Foto eines Doppelzimmers mit einer Glastür zur Terrasse und einem Spiegel aus Naturfaser über dem Bett",
  "Фотография спальни с двуспальной кроватью, стеклянной дверью на террасу и зеркалом в плетёной раме над кроватью",
  "صورة لغرفة نوم مزدوجة بباب زجاجي يفتح على التراس ومرآة بإطار منسوج فوق السرير",
  "Foto van een tweepersoonsslaapkamer met een glazen deur naar het terras en een spiegel van gevlochten vezels boven het bed",
  "Zdjęcie sypialni z podwójnym łóżkiem, przeszklonymi drzwiami na taras i lustrem w plecionej ramie nad łóżkiem",
  "Fotografi av et soverom med dobbeltseng, en glassdør til terrassen og et speil i flettet fiber over sengen",
  "Fotografi av ett sovrum med dubbelsäng, en glasdörr till terrassen och en spegel i flätad fiber ovanför sängen")
a('A bedroom opening to the terrace',
  "Un dormitorio que se abre a la terraza", "Une chambre ouverte sur la terrasse", "Ein Schlafzimmer mit Zugang zur Terrasse", "Спальня с выходом на террасу", "غرفة نوم تفتح على التراس",
  "Een slaapkamer die op het terras uitkomt", "Sypialnia z wyjściem na taras", "Et soverom som åpner seg mot terrassen", "Ett sovrum som öppnar sig mot terrassen")
a('Photograph of a second bedroom',
  "Fotografía de un segundo dormitorio con una cama individual, una manta azul y un escritorio de madera",
  "Photographie d’une deuxième chambre avec un lit simple, un plaid bleu et un bureau en bois",
  "Foto eines zweiten Schlafzimmers mit einem Einzelbett, einer blauen Decke und einem Holzschreibtisch",
  "Фотография второй спальни с односпальной кроватью, синим пледом и деревянным письменным столом",
  "صورة لغرفة نوم ثانية بسرير منفرد وغطاء أزرق ومكتب خشبي",
  "Foto van een tweede slaapkamer met een eenpersoonsbed, een blauwe plaid en een houten bureau",
  "Zdjęcie drugiej sypialni z łóżkiem pojedynczym, niebieskim pledem i drewnianym biurkiem",
  "Fotografi av et andre soverom med en enkeltseng, et blått pledd og et skrivebord i tre",
  "Fotografi av ett andra sovrum med en enkelsäng, en blå pläd och ett skrivbord i trä")
a('Photograph of a marble bathroom with a double vanity',
  "Fotografía de un baño de mármol con un mueble de lavabo doble, una ducha a ras de suelo y un inodoro",
  "Photographie d’une salle de bain en marbre avec un meuble double vasque, une douche à l’italienne et des toilettes",
  "Foto eines Marmorbads mit Doppelwaschtisch, ebenerdiger Dusche und Toilette",
  "Фотография мраморной ванной комнаты с двойной раковиной, душем без поддона и унитазом",
  "صورة لحمام من الرخام بمغسلة مزدوجة ودش على مستوى الأرض ومرحاض",
  "Foto van een marmeren badkamer met een dubbele wastafel, een inloopdouche en een toilet",
  "Zdjęcie marmurowej łazienki z podwójną umywalką, prysznicem bez brodzika i toaletą",
  "Fotografi av et marmorbad med dobbel servant, en dusj i gulvhøyde og et toalett",
  "Fotografi av ett badrum i marmor med dubbel handfat, en golvnära dusch och en toalett")
a('Photograph of a marble bathroom with a basin',
  "Fotografía de un baño de mármol con un lavabo, un inodoro y una bañera",
  "Photographie d’une salle de bain en marbre avec un lavabo, des toilettes et une baignoire",
  "Foto eines Marmorbads mit Waschbecken, Toilette und Badewanne",
  "Фотография мраморной ванной комнаты с раковиной, унитазом и ванной",
  "صورة لحمام من الرخام بمغسلة ومرحاض وحوض استحمام",
  "Foto van een marmeren badkamer met een wastafel, een toilet en een bad",
  "Zdjęcie marmurowej łazienki z umywalką, toaletą i wanną",
  "Fotografi av et marmorbad med en servant, et toalett og et badekar",
  "Fotografi av ett badrum i marmor med ett handfat, en toalett och ett badkar")
a('A terrace under a pergola',
  "Una terraza bajo una pérgola", "Une terrasse sous une pergola", "Eine Terrasse unter einer Pergola", "Терраса под перголой", "تراس تحت برغولا",
  "Een terras onder een pergola", "Taras pod pergolą", "En terrasse under en pergola", "En terrass under en pergola")
a('Photograph of a paved terrace with two wooden sun loungers',
  "Fotografía de una terraza pavimentada con dos tumbonas de madera y macetas con plantas",
  "Photographie d’une terrasse dallée avec deux bains de soleil en bois et des plantes en pot",
  "Foto einer gepflasterten Terrasse mit zwei hölzernen Sonnenliegen und Topfpflanzen",
  "Фотография вымощенной террасы с двумя деревянными шезлонгами и растениями в горшках",
  "صورة لتراس مرصوف بكرسيين خشبيين للاستلقاء تحت الشمس ونباتات في أصص",
  "Foto van een bestraat terras met twee houten ligbedden en planten in potten",
  "Zdjęcie wybrukowanego tarasu z dwoma drewnianymi leżakami i roślinami w donicach",
  "Fotografi av en flislagt terrasse med to solsenger i tre og planter i potter",
  "Fotografi av en stenlagd terrass med två solsängar i trä och krukväxter")
a('A terrace with sun loungers',
  "Una terraza con tumbonas", "Une terrasse avec des bains de soleil", "Eine Terrasse mit Sonnenliegen", "Терраса с шезлонгами", "تراس مع كراسي استلقاء",
  "Een terras met ligbedden", "Taras z leżakami", "En terrasse med solsenger", "En terrass med solsängar")
a('Photograph of a terrace with a laid dining table',
  "Fotografía de una terraza con una mesa de comedor puesta, un sofá y palmeras en macetas",
  "Photographie d’une terrasse avec une table dressée, un canapé et des palmiers en pot",
  "Foto einer Terrasse mit gedecktem Esstisch, einem Sofa und Palmen in Töpfen",
  "Фотография террасы с накрытым обеденным столом, диваном и пальмами в горшках",
  "صورة لتراس بطاولة طعام مجهّزة وأريكة ونخيل في أصص",
  "Foto van een terras met een gedekte eettafel, een bank en palmen in potten",
  "Zdjęcie tarasu z nakrytym stołem jadalnianym, sofą i palmami w donicach",
  "Fotografi av en terrasse med dekket spisebord, en sofa og palmer i potter",
  "Fotografi av en terrass med dukat matbord, en soffa och palmer i krukor")
a('A terrace for dining', "Una terraza para comer", "Une terrasse pour déjeuner", "Eine Terrasse zum Essen im Freien", "Терраса для трапез", "تراس لتناول الطعام",
  "Een terras om buiten te eten", "Taras do jedzenia na świeżym powietrzu", "En terrasse for måltider ute", "En terrass för måltider utomhus") if 'A terrace for dining' in todo else None

# ---------------------------------------------------------------- floorplan alt text and captions
a('Floorplan of the ground-floor home',
  "Plano de la vivienda de planta baja", "Plan du logement en rez-de-chaussée", "Grundriss der Erdgeschosswohnung", "Планировка квартиры на первом этаже", "مخطط المسكن في الطابق الأرضي",
  "Plattegrond van de woning op de begane grond", "Rzut lokalu na parterze", "Plantegning av boligen i første etasje", "Planritning för bostaden på bottenvåningen")
a('Ground-floor homes 6-0-1 and 7-0-1',
  "Viviendas de planta baja 6-0-1 y 7-0-1", "Logements en rez-de-chaussée 6-0-1 et 7-0-1", "Erdgeschosswohnungen 6-0-1 und 7-0-1", "Квартиры на первом этаже 6-0-1 и 7-0-1", "مساكن الطابق الأرضي 6-0-1 و7-0-1",
  "Woningen op de begane grond 6-0-1 en 7-0-1", "Lokale na parterze 6-0-1 i 7-0-1", "Boligene i første etasje 6-0-1 og 7-0-1", "Bostäderna på bottenvåningen 6-0-1 och 7-0-1")
a('Floorplan of the first-floor home',
  "Plano de la vivienda de primera planta", "Plan du logement au premier étage", "Grundriss der Wohnung im ersten Obergeschoss", "Планировка квартиры на втором этаже", "مخطط المسكن في الطابق الأول",
  "Plattegrond van de woning op de eerste verdieping", "Rzut lokalu na pierwszym piętrze", "Plantegning av boligen i andre etasje", "Planritning för bostaden på första våningen")
a('First-floor homes 3-1-3',
  "Viviendas de primera planta 3-1-3, 8-1-5, 10-1-3 y 10-1-5", "Logements au premier étage 3-1-3, 8-1-5, 10-1-3 et 10-1-5", "Wohnungen im ersten Obergeschoss 3-1-3, 8-1-5, 10-1-3 und 10-1-5",
  "Квартиры на втором этаже 3-1-3, 8-1-5, 10-1-3 и 10-1-5", "مساكن الطابق الأول 3-1-3 و8-1-5 و10-1-3 و10-1-5",
  "Woningen op de eerste verdieping 3-1-3, 8-1-5, 10-1-3 en 10-1-5", "Lokale na pierwszym piętrze 3-1-3, 8-1-5, 10-1-3 i 10-1-5",
  "Boligene i andre etasje 3-1-3, 8-1-5, 10-1-3 og 10-1-5", "Bostäderna på första våningen 3-1-3, 8-1-5, 10-1-3 och 10-1-5")
for blk in ('5', '10'):
    pent = 'Penthouse 5-AT-6' if blk == '5' else 'Penthouses 10-AT-8 and 10-AT-9'
    if blk == '5':
        cap = {'lower': ("Ático 5-AT-6, planta inferior", "Penthouse 5-AT-6, étage inférieur", "Penthouse 5-AT-6, unteres Geschoss", "Пентхаус 5-AT-6, нижний этаж", "البنتهاوس 5-AT-6، الطابق السفلي", "Penthouse 5-AT-6, onderste verdieping", "Penthouse 5-AT-6, dolne piętro", "Toppleilighet 5-AT-6, nedre etasje", "Takvåning 5-AT-6, nedre våningen"),
               'upper': ("Ático 5-AT-6, planta superior", "Penthouse 5-AT-6, étage supérieur", "Penthouse 5-AT-6, oberes Geschoss", "Пентхаус 5-AT-6, верхний этаж", "البنتهاوس 5-AT-6، الطابق العلوي", "Penthouse 5-AT-6, bovenste verdieping", "Penthouse 5-AT-6, górne piętro", "Toppleilighet 5-AT-6, øvre etasje", "Takvåning 5-AT-6, övre våningen")}
    else:
        cap = {'lower': ("Áticos 10-AT-8 y 10-AT-9, planta inferior", "Penthouses 10-AT-8 et 10-AT-9, étage inférieur", "Penthäuser 10-AT-8 und 10-AT-9, unteres Geschoss", "Пентхаусы 10-AT-8 и 10-AT-9, нижний этаж", "البنتهاوس 10-AT-8 و10-AT-9، الطابق السفلي", "Penthouses 10-AT-8 en 10-AT-9, onderste verdieping", "Penthouse’y 10-AT-8 i 10-AT-9, dolne piętro", "Toppleilighetene 10-AT-8 og 10-AT-9, nedre etasje", "Takvåningarna 10-AT-8 och 10-AT-9, nedre våningen"),
               'upper': ("Áticos 10-AT-8 y 10-AT-9, planta superior", "Penthouses 10-AT-8 et 10-AT-9, étage supérieur", "Penthäuser 10-AT-8 und 10-AT-9, oberes Geschoss", "Пентхаусы 10-AT-8 и 10-AT-9, верхний этаж", "البنتهاوس 10-AT-8 و10-AT-9، الطابق العلوي", "Penthouses 10-AT-8 en 10-AT-9, bovenste verdieping", "Penthouse’y 10-AT-8 i 10-AT-9, górne piętro", "Toppleilighetene 10-AT-8 og 10-AT-9, øvre etasje", "Takvåningarna 10-AT-8 och 10-AT-9, övre våningen")}
    ALT = {
        'lower': ("Plano de la planta inferior del ático dúplex del bloque {b}", "Plan de l’étage inférieur du penthouse duplex du bloc {b}", "Grundriss des unteren Geschosses des Maisonette-Penthauses in Block {b}", "Планировка нижнего этажа двухуровневого пентхауса в блоке {b}", "مخطط الطابق السفلي من البنتهاوس الدوبلكس في المبنى {b}", "Plattegrond van de onderste verdieping van het duplexpenthouse in blok {b}", "Rzut dolnego piętra penthouse’u dwupoziomowego w bloku {b}", "Plantegning av nedre etasje i duplex-toppleiligheten i hus {b}", "Planritning över nedre våningen i duplex-takvåningen i hus {b}"),
        'upper': ("Plano de la planta superior del ático dúplex del bloque {b}", "Plan de l’étage supérieur du penthouse duplex du bloc {b}", "Grundriss des oberen Geschosses des Maisonette-Penthauses in Block {b}", "Планировка верхнего этажа двухуровневого пентхауса в блоке {b}", "مخطط الطابق العلوي من البنتهاوس الدوبلكس في المبنى {b}", "Plattegrond van de bovenste verdieping van het duplexpenthouse in blok {b}", "Rzut górnego piętra penthouse’u dwupoziomowego w bloku {b}", "Plantegning av øvre etasje i duplex-toppleiligheten i hus {b}", "Planritning över övre våningen i duplex-takvåningen i hus {b}")}
    for lv in ('lower', 'upper'):
        a(f'Floorplan of the {lv} floor of the block {blk} duplex penthouse', *[t.format(b=blk) for t in ALT[lv]])
        a(f'{pent}, {lv} floor', *cap[lv])

# ---------------------------------------------------------------- overview, why, architecture
a('Ten homes, <em>finished and listed</em>',
  "Diez viviendas, <em>terminadas y a la venta</em>", "Dix logements, <em>achevés et en vente</em>", "Zehn Wohnungen, <em>fertig und gelistet</em>", "Десять квартир, <em>готовых и в продаже</em>", "عشرة مساكن، <em>مكتملة ومعروضة</em>",
  "Tien woningen, <em>opgeleverd en te koop</em>", "Dziesięć lokali, <em>ukończonych i dostępnych</em>", "Ti boliger, <em>ferdige og annonsert</em>", "Tio bostäder, <em>färdiga och listade</em>")
a('Acacia Residences is a finished residential complex',
  "Acacia Residences es un complejo residencial terminado en Nueva Andalucía, Marbella. El folleto del promotor describe 70 viviendas de dos y tres dormitorios, terrazas con vistas al Mediterráneo y a la montaña, y jardines cuidados con dos piscinas, un gimnasio y una zona de bienestar. Hoy se ofrecen diez viviendas de dos dormitorios: tres en planta baja, cuatro en primera planta y tres áticos dúplex.",
  "Acacia Residences est une résidence achevée à Nueva Andalucía, Marbella. La brochure du promoteur décrit 70 logements de deux et trois chambres, des terrasses avec vue sur la Méditerranée et la montagne, et des jardins paysagers avec deux piscines, une salle de sport et un espace bien-être. Dix logements de deux chambres sont aujourd’hui en vente : trois au rez-de-chaussée, quatre au premier étage et trois penthouses duplex.",
  "Acacia Residences ist eine fertiggestellte Wohnanlage in Nueva Andalucía, Marbella. Die Broschüre des Bauträgers beschreibt 70 Wohnungen mit zwei und drei Schlafzimmern, Terrassen mit Blick auf das Mittelmeer und die Berge sowie gepflegte Gärten mit zwei Pools, einem Fitnessraum und einem Wellnessbereich. Zum Verkauf stehen heute zehn Wohnungen mit zwei Schlafzimmern: drei im Erdgeschoss, vier im ersten Obergeschoss und drei Maisonette-Penthäuser.",
  "Acacia Residences — готовый жилой комплекс в Нуэва-Андалусии, Марбелья. В брошюре застройщика описаны 70 квартир с двумя и тремя спальнями, террасы с видом на Средиземное море и горы, а также благоустроенные сады с двумя бассейнами, тренажёрным залом и велнес-зоной. Сегодня в продаже десять квартир с двумя спальнями: три на первом этаже, четыре на втором и три двухуровневых пентхауса.",
  "Acacia Residences مجمع سكني مكتمل في نويفا أندلوثيا بماربيا. يصف كتيّب المطوّر 70 مسكنًا من غرفتي نوم وثلاث غرف، بتراسات تطل على البحر المتوسط والجبال، وحدائق منسّقة فيها مسبحان وصالة رياضية ومنطقة للعافية. يُعرض اليوم للبيع عشرة مساكن من غرفتي نوم: ثلاثة في الطابق الأرضي وأربعة في الطابق الأول وثلاثة بنتهاوس دوبلكس.",
  "Acacia Residences is een opgeleverd woningcomplex in Nueva Andalucía, Marbella. De brochure van de ontwikkelaar beschrijft 70 woningen met twee en drie slaapkamers, terrassen met uitzicht op de Middellandse Zee en de bergen, en verzorgde tuinen met twee zwembaden, een gym en een wellnessruimte. Vandaag staan tien woningen met twee slaapkamers te koop: drie op de begane grond, vier op de eerste verdieping en drie duplexpenthouses.",
  "Acacia Residences to ukończony kompleks mieszkaniowy w Nueva Andalucía, Marbella. Broszura dewelopera opisuje 70 lokali z dwiema i trzema sypialniami, tarasy z widokiem na Morze Śródziemne i góry oraz zadbane ogrody z dwoma basenami, siłownią i strefą wellness. Do sprzedaży jest dziś dziesięć lokali z dwiema sypialniami: trzy na parterze, cztery na pierwszym piętrze i trzy dwupoziomowe penthouse’y.",
  "Acacia Residences er et ferdigstilt boligkompleks i Nueva Andalucía, Marbella. Utbyggerens brosjyre beskriver 70 boliger med to og tre soverom, terrasser med utsikt mot Middelhavet og fjellene, og opparbeidede hager med to bassenger, et treningsrom og et velværeområde. Ti boliger med to soverom er til salgs i dag: tre i første etasje, fire i andre etasje og tre toppleiligheter i to plan.",
  "Acacia Residences är ett färdigställt bostadsområde i Nueva Andalucía, Marbella. Exploatörens broschyr beskriver 70 bostäder med två och tre sovrum, terrasser med utsikt över Medelhavet och bergen, samt anlagda trädgårdar med två pooler, ett gym och en wellnessavdelning. Tio bostäder med två sovrum är till salu i dag: tre på bottenvåningen, fyra på första våningen och tre takvåningar i två plan.")
a('Every listed home has two bedrooms and two bathrooms',
  "Todas las viviendas a la venta tienen dos dormitorios y dos baños, y los planos muestran además un aseo independiente. Cada una incluye una plaza de aparcamiento y un trastero. El portal del promotor llama al complejo edificio terminado; el folleto está fechado en 2023 y no da fecha de finalización.",
  "Chaque logement en vente compte deux chambres et deux salles de bain, et les plans montrent en plus des toilettes séparées. Chacun est livré avec une place de stationnement et un débarras. Le portail du promoteur qualifie la résidence d’immeuble achevé ; la brochure est datée de 2023 et ne donne aucune date d’achèvement.",
  "Jede angebotene Wohnung hat zwei Schlafzimmer und zwei Badezimmer, und die Grundrisse zeigen zusätzlich ein separates WC. Zu jeder gehören ein Stellplatz und ein Abstellraum. Das Portal des Bauträgers bezeichnet die Anlage als fertiggestelltes Gebäude; die Broschüre ist auf 2023 datiert und nennt keinen Fertigstellungstermin.",
  "В каждой квартире, выставленной на продажу, две спальни и две ванные комнаты, а на планах есть ещё и отдельный туалет. К каждой прилагаются одно парковочное место и одна кладовая. Портал застройщика называет комплекс завершённым зданием; брошюра датирована 2023 годом и не называет даты завершения.",
  "في كل مسكن معروض غرفتا نوم وحمامان، وتُظهر المخططات مرحاضًا منفصلًا أيضًا. ويأتي مع كل منها موقف سيارات واحد ومخزن واحد. تصف بوابة المطوّر المجمع بأنه مبنى مكتمل؛ والكتيّب مؤرخ في 2023 ولا يذكر تاريخًا للإتمام.",
  "Elke aangeboden woning heeft twee slaapkamers en twee badkamers, en de plattegronden tonen ook een apart toilet. Bij elke woning horen één parkeerplaats en één berging. Het portaal van de ontwikkelaar noemt het complex een opgeleverd gebouw; de brochure is gedateerd 2023 en noemt geen opleveringsdatum.",
  "Każdy oferowany lokal ma dwie sypialnie i dwie łazienki, a na rzutach widać także osobną toaletę. Do każdego należą jedno miejsce parkingowe i jedna komórka lokatorska. Portal dewelopera nazywa kompleks budynkiem ukończonym; broszura jest datowana na 2023 r. i nie podaje terminu ukończenia.",
  "Hver av boligene som er til salgs har to soverom og to bad, og plantegningene viser i tillegg et eget toalett. Til hver hører én parkeringsplass og én bod. Utbyggerens portal kaller anlegget en ferdig bygning; brosjyren er datert 2023 og oppgir ingen ferdigstillelsesdato.",
  "Varje bostad som är till salu har två sovrum och två badrum, och planritningarna visar dessutom en separat toalett. Till varje hör en parkeringsplats och ett förråd. Exploatörens portal kallar området en färdig byggnad; broschyren är daterad 2023 och anger inget färdigställandedatum.")
a('Finished two-bedroom homes with large terraces',
  "Viviendas terminadas de dos dormitorios con grandes terrazas, una plaza de aparcamiento y un trastero cada una, en una ladera de Nueva Andalucía.",
  "Des logements achevés de deux chambres avec de grandes terrasses, une place de stationnement et un débarras chacun, sur une colline de Nueva Andalucía.",
  "Fertiggestellte Wohnungen mit zwei Schlafzimmern, großen Terrassen, je einem Stellplatz und einem Abstellraum, an einem Hang in Nueva Andalucía.",
  "Готовые квартиры с двумя спальнями, большими террасами, парковочным местом и кладовой у каждой, на склоне холма в Нуэва-Андалусии.",
  "مساكن جاهزة من غرفتي نوم بتراسات واسعة وموقف سيارات ومخزن لكل منها، على سفح تل في نويفا أندلوثيا.",
  "Opgeleverde woningen met twee slaapkamers, grote terrassen, elk met een parkeerplaats en een berging, op een heuvel in Nueva Andalucía.",
  "Ukończone lokale z dwiema sypialniami, dużymi tarasami, miejscem parkingowym i komórką lokatorską w każdym, na zboczu wzgórza w Nueva Andalucía.",
  "Ferdigstilte boliger med to soverom, store terrasser, en parkeringsplass og en bod hver, i en skråning i Nueva Andalucía.",
  "Färdigställda bostäder med två sovrum, stora terrasser, en parkeringsplats och ett förråd vardera, i en sluttning i Nueva Andalucía.")
a('Buyers who want a finished two-bedroom home',
  "Compradores que quieren una vivienda terminada de dos dormitorios en Nueva Andalucía, con una gran terraza y piscinas, gimnasio y jardines comunes, en lugar de una vivienda aún por construir.",
  "Acheteurs qui veulent un logement achevé de deux chambres à Nueva Andalucía, avec une grande terrasse et des piscines, une salle de sport et des jardins communs, plutôt qu’un logement encore à construire.",
  "Käufer, die eine fertiggestellte Wohnung mit zwei Schlafzimmern in Nueva Andalucía mit großer Terrasse sowie gemeinsamen Pools, Fitnessraum und Gärten suchen, statt einer Wohnung, die erst noch gebaut werden muss.",
  "Покупатели, которым нужна готовая квартира с двумя спальнями в Нуэва-Андалусии с большой террасой, общими бассейнами, тренажёрным залом и садами, а не квартира, которую ещё предстоит построить.",
  "مشترون يريدون مسكنًا جاهزًا من غرفتي نوم في نويفا أندلوثيا، بتراس واسع ومسابح وصالة رياضية وحدائق مشتركة، بدلًا من مسكن لم يُبنَ بعد.",
  "Kopers die een afgeronde woning met twee slaapkamers in Nueva Andalucía willen, met een groot terras en gedeelde zwembaden, gym en tuinen, in plaats van een woning die nog gebouwd moet worden.",
  "Kupujący, którzy chcą ukończonego lokalu z dwiema sypialniami w Nueva Andalucía, z dużym tarasem oraz wspólnymi basenami, siłownią i ogrodami, a nie lokalu, który dopiero powstanie.",
  "Kjøpere som vil ha en ferdig bolig med to soverom i Nueva Andalucía, med stor terrasse og felles bassenger, treningsrom og hager, i stedet for en bolig som ennå skal bygges.",
  "Köpare som vill ha en färdig bostad med två sovrum i Nueva Andalucía, med stor terrass och gemensamma pooler, gym och trädgårdar, i stället för en bostad som ännu ska byggas.")
a('Terraces of 38.56 to 64.54 sqm on the price list',
  "Terrazas de {N38.56} a {N64.54} {U} según la lista de precios, una plaza de aparcamiento y un trastero con cada vivienda, y un complejo ya construido, de modo que puede ver las viviendas, las piscinas y el gimnasio antes de decidir.",
  "Des terrasses de {N38.56} à {N64.54} {U} selon la liste de prix, une place de stationnement et un débarras avec chaque logement, et une résidence déjà construite : vous pouvez voir les logements, les piscines et la salle de sport avant de décider.",
  "Terrassen von {N38.56} bis {N64.54} {U} laut Preisliste, zu jeder Wohnung ein Stellplatz und ein Abstellraum und eine bereits gebaute Anlage, sodass Sie die Wohnungen, die Pools und den Fitnessraum sehen können, bevor Sie sich entscheiden.",
  "Террасы от {N38.56} до {N64.54} {U} по прайс-листу, парковочное место и кладовая при каждой квартире и уже построенный комплекс: вы можете увидеть квартиры, бассейны и тренажёрный зал до принятия решения.",
  "تراسات من {N38.56} إلى {N64.54} {U} وفق قائمة الأسعار، وموقف سيارات ومخزن مع كل مسكن، ومجمع مبني بالفعل، فيمكنكم رؤية المساكن والمسابح والصالة الرياضية قبل أن تقرروا.",
  "Terrassen van {N38.56} tot {N64.54} {U} volgens de prijslijst, bij elke woning een parkeerplaats en een berging, en een complex dat al is gebouwd, zodat u de woningen, de zwembaden en de gym kunt zien voordat u beslist.",
  "Tarasy od {N38.56} do {N64.54} {U} według cennika, miejsce parkingowe i komórka lokatorska przy każdym lokalu oraz kompleks, który już stoi, więc mogą Państwo zobaczyć lokale, baseny i siłownię, zanim podejmą decyzję.",
  "Terrasser på {N38.56} til {N64.54} {U} ifølge prislisten, en parkeringsplass og en bod til hver bolig, og et anlegg som allerede er bygget, slik at du kan se boligene, bassengene og treningsrommet før du bestemmer deg.",
  "Terrasser på {N38.56} till {N64.54} {U} enligt prislistan, en parkeringsplats och ett förråd till varje bostad, och ett område som redan är byggt, så att ni kan se bostäderna, poolerna och gymmet innan ni bestämmer er.")
a('The brochure counts three golf courses within a few minutes, and Puerto',
  "El folleto cuenta tres campos de golf a pocos minutos, y Puerto Banús está a unos diez minutos en coche.",
  "La brochure compte trois parcours de golf à quelques minutes, et Puerto Banús est à environ dix minutes en voiture.",
  "Die Broschüre nennt drei Golfplätze in wenigen Minuten Entfernung, und Puerto Banús ist mit dem Auto etwa zehn Minuten entfernt.",
  "В брошюре указаны три поля для гольфа в нескольких минутах езды, а до Пуэрто-Бануса около десяти минут на машине.",
  "يذكر الكتيّب ثلاثة ملاعب غولف على بعد دقائق قليلة، وبويرتو بانوس على بعد نحو عشر دقائق بالسيارة.",
  "De brochure telt drie golfbanen op enkele minuten afstand, en Puerto Banús ligt ongeveer tien minuten met de auto.",
  "Broszura podaje trzy pola golfowe w odległości kilku minut, a do Puerto Banús jest około dziesięciu minut samochodem.",
  "Brosjyren oppgir tre golfbaner på få minutters avstand, og Puerto Banús ligger omtrent ti minutter unna med bil.",
  "Broschyren anger tre golfbanor på några minuters avstånd, och Puerto Banús ligger ungefär tio minuter bort med bil.")
a('What to check',
  "Qué comprobar", "Ce qu’il faut vérifier", "Was zu prüfen ist", "Что проверить", "ما يجب التحقق منه", "Waar op te letten", "Co sprawdzić", "Hva som bør sjekkes", "Vad som bör kontrolleras")
a('The price list adds 7% ITP rather than VAT',
  "La lista de precios añade el {P7} de ITP en lugar de IVA, y sus superficies difieren de las de los planos, así que confirmamos el impuesto y las superficies del contrato antes de cualquier reserva.",
  "La liste de prix ajoute {P7} d’ITP et non la TVA, et ses surfaces diffèrent de celles des plans ; nous confirmons donc la taxe et les surfaces du contrat avant toute réservation.",
  "Die Preisliste addiert {P7} ITP statt MwSt., und ihre Flächen weichen von denen der Grundrisse ab; deshalb bestätigen wir vor jeder Reservierung die Steuer und die Vertragsflächen.",
  "В прайс-листе к цене добавляется {P7} ITP, а не НДС, и его площади отличаются от площадей на планах, поэтому до любого бронирования мы уточняем налог и площади по договору.",
  "تضيف قائمة الأسعار {P7} ضريبة ITP بدلًا من ضريبة القيمة المضافة، وتختلف مساحاتها عن المساحات على المخططات، لذلك نؤكد الضريبة ومساحات العقد قبل أي حجز.",
  "De prijslijst telt {P7} ITP op in plaats van btw, en de oppervlakten wijken af van die op de plattegronden. Daarom bevestigen wij vóór elke reservering de belasting en de oppervlakten in het contract.",
  "Cennik dolicza {P7} ITP zamiast VAT, a jego powierzchnie różnią się od tych na rzutach, dlatego przed każdą rezerwacją potwierdzamy podatek i powierzchnie z umowy.",
  "Prislisten legger til {P7} ITP i stedet for mva., og arealene i den avviker fra dem på plantegningene, så vi bekrefter skatten og kontraktsarealene før en reservasjon.",
  "Prislistan lägger till {P7} ITP i stället för moms, och dess ytor skiljer sig från dem på planritningarna, så vi bekräftar skatten och avtalsytorna före varje reservation.")
a('White blocks, <em>terraces facing the view</em>',
  "Bloques blancos, <em>terrazas orientadas a la vista</em>", "Des blocs blancs, <em>des terrasses tournées vers la vue</em>", "Weiße Blöcke, <em>Terrassen zur Aussicht</em>", "Белые блоки, <em>террасы с видом</em>", "مبانٍ بيضاء، <em>وتراسات تواجه الإطلالة</em>",
  "Witte blokken, <em>terrassen op het uitzicht</em>", "Białe bloki, <em>tarasy zwrócone na widok</em>", "Hvite bygg, <em>terrasser mot utsikten</em>", "Vita hus, <em>terrasser mot utsikten</em>")
a('The homes are in white blocks with curved clay roof tiles',
  "Las viviendas están en bloques blancos con tejas curvas de barro, que ascienden por una ladera aterrazada sobre los jardines y las piscinas. El folleto da la orientación como sureste y suroeste, con terrazas que miran al Mediterráneo y a la montaña.",
  "Les logements se trouvent dans des blocs blancs aux tuiles rondes en terre cuite, qui montent sur une colline en terrasses au-dessus des jardins et des piscines. La brochure indique une orientation sud-est et sud-ouest, avec des terrasses ouvertes sur la Méditerranée et la montagne.",
  "Die Wohnungen liegen in weißen Blöcken mit gebogenen Tondachziegeln, die an einem terrassierten Hang oberhalb der Gärten und der Pools ansteigen. Die Broschüre nennt die Ausrichtung Südost und Südwest, mit Terrassen mit Blick auf das Mittelmeer und die Berge.",
  "Квартиры расположены в белых блоках с изогнутой глиняной черепицей, которые поднимаются по террасированному склону над садами и бассейнами. В брошюре ориентация указана как юго-восток и юго-запад, а террасы смотрят на Средиземное море и горы.",
  "تقع المساكن في مبانٍ بيضاء بقرميد طيني مقوّس، تتدرج على سفح مدرّج فوق الحدائق والمسابح. ويذكر الكتيّب أن الاتجاه جنوب شرقي وجنوب غربي، وأن التراسات تطل على البحر المتوسط والجبال.",
  "De woningen liggen in witte blokken met gebogen kleidakpannen, die op een terrasvormige helling boven de tuinen en de zwembaden oplopen. De brochure geeft als oriëntatie zuidoost en zuidwest, met terrassen met uitzicht op de Middellandse Zee en de bergen.",
  "Lokale znajdują się w białych blokach z łukową dachówką ceramiczną, wznoszących się tarasowym zboczem nad ogrodami i basenami. Broszura podaje orientację południowo-wschodnią i południowo-zachodnią, z tarasami z widokiem na Morze Śródziemne i góry.",
  "Boligene ligger i hvite bygg med buede takstein av leire, som stiger opp en terrassert skråning over hagene og bassengene. Brosjyren oppgir orienteringen som sørøst og sørvest, med terrasser som vender ut mot Middelhavet og fjellene.",
  "Bostäderna ligger i vita hus med välvda lertegelpannor, som stiger uppför en terrasserad sluttning ovanför trädgårdarna och poolerna. Broschyren anger väderstrecken som sydost och sydväst, med terrasser som vetter mot Medelhavet och bergen.")
a('The developer describes a private complex with 24-hour security',
  "El promotor describe un complejo privado con seguridad las 24 horas, y el portal menciona garajes subterráneos y trasteros.",
  "Le promoteur décrit une résidence privée avec sécurité 24 heures sur 24, et le portail mentionne des garages en sous-sol et des débarras.",
  "Der Bauträger beschreibt eine private Anlage mit 24-Stunden-Sicherheitsdienst, und das Portal nennt Tiefgaragen und Abstellräume.",
  "Застройщик описывает закрытый комплекс с круглосуточной охраной, а на портале указаны подземные гаражи и кладовые.",
  "يصف المطوّر مجمعًا خاصًا بحراسة على مدار الساعة، وتذكر البوابة مرائب تحت الأرض ومخازن.",
  "De ontwikkelaar beschrijft een privécomplex met bewaking de klok rond, en het portaal vermeldt ondergrondse garages en bergingen.",
  "Deweloper opisuje zamknięty kompleks z całodobową ochroną, a portal wymienia garaże podziemne i komórki lokatorskie.",
  "Utbyggeren beskriver et privat anlegg med sikkerhet døgnet rundt, og portalen nevner garasjer under bakken og boder.",
  "Exploatören beskriver ett privat område med säkerhet dygnet runt, och portalen nämner garage under jord och förråd.")
a('Roof', "Cubierta", "Toiture", "Dach", "Кровля", "السقف", "Dak", "Dach", "Tak", "Tak")
a('Curved Arab roof tile.', "Teja curva árabe.", "Tuile ronde de style arabe.", "Gebogene arabische Dachziegel.", "Изогнутая арабская черепица.", "قرميد عربي مقوّس.", "Gebogen Arabische dakpan.", "Łukowa dachówka w stylu arabskim.", "Buede arabiske takstein.", "Välvda arabiska takpannor.")
a('Exterior paint in RAL 9003',
  "Pintura exterior en RAL 9003, un blanco.", "Peinture extérieure RAL 9003, un blanc.", "Außenanstrich in RAL 9003, einem Weiß.", "Наружная краска RAL 9003 — белый цвет.", "طلاء خارجي بلون RAL 9003، وهو أبيض.",
  "Buitenverf in RAL 9003, een wit.", "Farba zewnętrzna RAL 9003, odcień bieli.", "Utvendig maling i RAL 9003, en hvitfarge.", "Utvändig färg i RAL 9003, en vit kulör.")
a('PVC frames with Climalit glazing.',
  "Carpintería de PVC con vidrios Climalit.", "Menuiseries en PVC avec vitrages Climalit.", "PVC-Rahmen mit Climalit-Verglasung.", "ПВХ-рамы со стеклопакетами Climalit.", "إطارات من PVC بزجاج Climalit.",
  "PVC-kozijnen met Climalit-beglazing.", "Ramy z PVC z szybami Climalit.", "PVC-karmer med Climalit-glass.", "PVC-karmar med Climalit-glas.")
a('The brochure says every home has a terrace',
  "El folleto dice que todas las viviendas tienen una terraza con vistas panorámicas al Mediterráneo y a la montaña.",
  "La brochure indique que chaque logement a une terrasse avec vue panoramique sur la Méditerranée et la montagne.",
  "Laut Broschüre hat jede Wohnung eine Terrasse mit Panoramablick auf das Mittelmeer und die Berge.",
  "В брошюре сказано, что у каждой квартиры есть терраса с панорамным видом на Средиземное море и горы.",
  "يذكر الكتيّب أن لكل مسكن تراسًا بإطلالة بانورامية على البحر المتوسط والجبال.",
  "De brochure zegt dat elke woning een terras heeft met panoramisch uitzicht op de Middellandse Zee en de bergen.",
  "Broszura podaje, że każdy lokal ma taras z panoramicznym widokiem na Morze Śródziemne i góry.",
  "Brosjyren sier at hver bolig har en terrasse med panoramautsikt over Middelhavet og fjellene.",
  "Broschyren säger att varje bostad har en terrass med panoramautsikt över Medelhavet och bergen.")

# ---------------------------------------------------------------- quality specification
a('Source: the developer’s quality specification',
  "Fuente: la memoria de calidades del promotor, que no lleva fecha y se repite en el folleto de 2023. Confirmamos que cada vivienda se ajusta a ella.",
  "Source : le descriptif technique du promoteur, qui ne porte aucune date et est repris dans la brochure de 2023. Nous confirmons que chaque logement y correspond.",
  "Quelle: die Baubeschreibung des Bauträgers, die kein Datum trägt und in der Broschüre von 2023 wiederholt wird. Wir bestätigen, dass jede Wohnung ihr entspricht.",
  "Источник: спецификация застройщика, на которой нет даты и которая повторена в брошюре 2023 года. Мы уточняем, что каждая квартира ей соответствует.",
  "المصدر: مواصفات البناء لدى المطوّر، وهي بلا تاريخ ومكرّرة في كتيّب 2023. نؤكد أن كل مسكن مطابق لها.",
  "Bron: het lastenboek van de ontwikkelaar, dat geen datum draagt en is herhaald in de brochure van 2023. Wij bevestigen dat elke woning ermee overeenkomt.",
  "Źródło: specyfikacja techniczna dewelopera, która nie ma daty i została powtórzona w broszurze z 2023 r. Potwierdzamy, że każdy lokal jej odpowiada.",
  "Kilde: utbyggerens beskrivelse av kvalitet og standard, som ikke har dato og er gjentatt i brosjyren fra 2023. Vi bekrefter at hver bolig samsvarer med den.",
  "Källa: exploatörens byggbeskrivning, som saknar datum och återges i broschyren från 2023. Vi bekräftar att varje bostad stämmer med den.")
a('Honed cream-ivory marble floors',
  "Suelos de mármol crema marfil con acabado apomazado, en piezas cuadradas, con rodapié del mismo mármol.",
  "Sols en marbre crème ivoire adouci, en carreaux carrés, avec plinthes dans le même marbre.",
  "Böden aus mattgeschliffenem Marmor Crema Marfil in quadratischen Platten, mit Sockelleisten aus demselben Marmor.",
  "Полы из матово отполированного мрамора «крема марфиль» квадратными плитами, плинтусы из того же мрамора.",
  "أرضيات من الرخام بلون العاج الكريمي بتشطيب مطفأ، بقطع مربعة، مع وزرات من الرخام نفسه.",
  "Vloeren van gezoet crème-ivoorkleurig marmer in vierkante stukken, met plinten van hetzelfde marmer.",
  "Podłogi z matowo szlifowanego marmuru w kolorze kremowej kości słoniowej, w kwadratowych płytach, z listwami przypodłogowymi z tego samego marmuru.",
  "Gulv i matt slipt marmor i kremhvit elfenbensfarge, i kvadratiske biter, med sokkel i samme marmor.",
  "Golv i mattslipad marmor i krämelfenbensfärg, i kvadratiska stycken, med golvlist i samma marmor.")
a('Walls and ceilings in plastic paint',
  "Paredes y techos con pintura plástica color RAL 9003.", "Murs et plafonds en peinture plastique, teinte RAL 9003.", "Wände und Decken mit Dispersionsfarbe, Farbton RAL 9003.",
  "Стены и потолки окрашены пластичной краской цвета RAL 9003.", "جدران وأسقف بطلاء بلاستيكي بلون RAL 9003.", "Wanden en plafonds met muurverf, kleur RAL 9003.",
  "Ściany i sufity pomalowane farbą plastyczną w kolorze RAL 9003.", "Vegger og tak med plastmaling, farge RAL 9003.", "Väggar och tak med plastfärg, kulör RAL 9003.")
a('PVC window frames with Climalit glazing.',
  "Ventanas con carpintería de PVC y vidrios Climalit.", "Fenêtres à menuiseries PVC avec vitrages Climalit.", "Fensterrahmen aus PVC mit Climalit-Verglasung.",
  "Оконные рамы из ПВХ со стеклопакетами Climalit.", "إطارات نوافذ من PVC بزجاج Climalit.", "PVC raamkozijnen met Climalit-beglazing.",
  "Ramy okienne z PVC z szybami Climalit.", "Vindusrammer i PVC med Climalit-glass.", "Fönsterkarmar i PVC med Climalit-glas.")
a('White-lacquered doors with black handles and fittings.',
  "Puertas lacadas en blanco con manillas y herrajes negros.", "Portes laquées blanc avec poignées et ferrures noires.", "Weiß lackierte Türen mit schwarzen Griffen und Beschlägen.",
  "Двери, лакированные в белый цвет, с чёрными ручками и фурнитурой.", "أبواب مطلية بالورنيش الأبيض بمقابض وإكسسوارات سوداء.", "Wit gelakte deuren met zwarte kruk en beslag.",
  "Drzwi lakierowane na biało z czarnymi klamkami i okuciami.", "Hvitlakkerte dører med svarte håndtak og beslag.", "Vitlackerade dörrar med svarta handtag och beslag.")
a('Polished cream-ivory marble on the walls',
  "Paredes revestidas de mármol crema marfil pulido, en piezas cuadradas.", "Murs revêtus de marbre crème ivoire poli, en carreaux carrés.", "Wandverkleidung aus poliertem Marmor Crema Marfil in quadratischen Platten.",
  "Стены облицованы полированным мрамором «крема марфиль» квадратными плитами.", "جدران مكسوّة برخام بلون العاج الكريمي المصقول، بقطع مربعة.", "Wanden bekleed met gepolijst crème-ivoorkleurig marmer in vierkante stukken.",
  "Ściany wykończone polerowanym marmurem w kolorze kremowej kości słoniowej, w kwadratowych płytach.", "Vegger kledd med polert marmor i kremhvit elfenbensfarge, i kvadratiske biter.", "Väggar klädda med polerad marmor i krämelfenbensfärg, i kvadratiska stycken.")
a('Roca “ONA” toilets with a low cistern',
  "Inodoros Roca «ONA» de tanque bajo, y lavabos, bañeras y grifería Grohe, con grifos de la serie Grohe Bauedge.",
  "Toilettes Roca « ONA » à réservoir bas, et lavabos, baignoires et robinetterie Grohe, la robinetterie de la série Grohe Bauedge.",
  "Roca-Toiletten „ONA“ mit niedrigem Spülkasten sowie Grohe-Waschtische, -Badewannen und -Armaturen, die Armaturen aus der Serie Grohe Bauedge.",
  "Унитазы Roca «ONA» с низким бачком, а также умывальники, ванны и смесители Grohe, смесители серии Grohe Bauedge.",
  "مراحيض Roca «ONA» بخزان منخفض، ومغاسل وأحواض استحمام وحنفيات Grohe، والحنفيات من سلسلة Grohe Bauedge.",
  "Roca ‘ONA’-toiletten met lage stortbak, en Grohe-wastafels, baden en kranen, de kranen uit de Grohe Bauedge-serie.",
  "Toalety Roca „ONA” z niskim zbiornikiem oraz umywalki, wanny i baterie Grohe, baterie z serii Grohe Bauedge.",
  "Roca «ONA»-toaletter med lav sisterne, og Grohe-servanter, badekar og kraner, kranene fra Grohe Bauedge-serien.",
  "Roca ”ONA”-toaletter med lågt spolkärl, samt Grohe-handfat, badkar och blandare, blandarna ur serien Grohe Bauedge.")
a('Porcelain worktops, white-lacquered wooden fronts',
  "Encimeras de porcelánico, frentes de madera lacada en blanco e interiores de melamina.", "Plans de travail en grès cérame, façades en bois laqué blanc et intérieurs en mélaminé.",
  "Arbeitsplatten aus Feinsteinzeug, weiß lackierte Holzfronten und Innenausstattung aus Melamin.", "Столешницы из керамогранита, фасады из белого лакированного дерева и внутренние поверхности из меламина.",
  "أسطح عمل من البورسلين، وواجهات خشبية مطلية بالورنيش الأبيض، وداخل من الميلامين.", "Werkbladen van porselein, wit gelakte houten fronten en binnenkanten van melamine.",
  "Blaty z gresu porcelanowego, fronty z drewna lakierowanego na biało i wnętrza z melaminy.", "Benkeplater i porselensfliser, hvitlakkerte fronter i tre og melamininnside.", "Bänkskivor i porslinsklinker, vitlackerade träfronter och insidor i melamin.")
a('Siemens appliances: an oven',
  "Electrodomésticos Siemens: horno, microondas, lavavajillas integrable, placa de inducción, lavadora integrable, frigorífico combi integrable y campana de 90 cm, con fregadero y grifo de acero inoxidable Teka.",
  "Électroménager Siemens : four, micro-ondes, lave-vaisselle intégrable, plaque à induction, lave-linge intégrable, réfrigérateur-congélateur combiné intégrable et hotte de 90 cm, avec évier et robinet en inox Teka.",
  "Siemens-Geräte: Backofen, Mikrowelle, integrierbarer Geschirrspüler, Induktionskochfeld, integrierbare Waschmaschine, integrierbare Kühl-Gefrier-Kombination und 90-cm-Dunstabzugshaube, dazu Edelstahlspüle und Armatur von Teka.",
  "Техника Siemens: духовой шкаф, микроволновая печь, встраиваемая посудомоечная машина, индукционная варочная панель, встраиваемая стиральная машина, встраиваемый холодильник с морозильной камерой и вытяжка 90 см, а также мойка и смеситель из нержавеющей стали Teka.",
  "أجهزة Siemens: فرن وميكروويف وغسالة أطباق مدمجة وموقد حثّي وغسالة ملابس مدمجة وثلاجة مدمجة بمجمّد وشفاط بعرض 90 سم، مع حوض وحنفية من الفولاذ المقاوم للصدأ من Teka.",
  "Siemens-apparatuur: een oven, een magnetron, een inbouwvaatwasser, een inductiekookplaat, een inbouwwasmachine, een inbouwkoel-vriescombinatie en een afzuigkap van 90 cm, met een roestvrijstalen spoelbak en kraan van Teka.",
  "Sprzęt Siemens: piekarnik, mikrofalówka, zmywarka do zabudowy, płyta indukcyjna, pralka do zabudowy, lodówko-zamrażarka do zabudowy i okap 90 cm, a do tego zlew i bateria ze stali nierdzewnej Teka.",
  "Siemens-hvitevarer: en stekeovn, en mikrobølgeovn, en integrert oppvaskmaskin, en induksjonstopp, en integrert vaskemaskin, et integrert kombiskap og en 90 cm ventilator, med oppvaskkum og kran i rustfritt stål fra Teka.",
  "Siemens-apparater: en ugn, en mikrovågsugn, en integrerad diskmaskin, en induktionshäll, en integrerad tvättmaskin, ett integrerat kyl-frys och en 90 cm köksfläkt, med en diskho och en blandare i rostfritt stål från Teka.")
a('Lighting and electrical',
  "Iluminación e instalación eléctrica", "Éclairage et électricité", "Beleuchtung und Elektrik", "Освещение и электрика", "الإضاءة والكهرباء", "Verlichting en elektra", "Oświetlenie i instalacja elektryczna", "Belysning og elektro", "Belysning och el")
a('LED lighting indoors, and on the terraces',
  "Iluminación LED en el interior y, en las terrazas, apliques de pared hechos con una teja pintada del color de la fachada y focos blancos de techo.",
  "Éclairage LED à l’intérieur et, sur les terrasses, des appliques fabriquées à partir d’une tuile peinte de la couleur de la façade, et des spots blancs au plafond.",
  "LED-Beleuchtung im Innenraum und auf den Terrassen Wandleuchten aus einem in der Fassadenfarbe lackierten Dachziegel sowie weiße Deckenspots.",
  "Светодиодное освещение внутри, а на террасах — настенные светильники из черепицы, окрашенной в цвет фасада, и белые потолочные споты.",
  "إضاءة LED في الداخل، وعلى التراسات إضاءات جدارية مصنوعة من قرميدة مطلية بلون الواجهة وكشّافات بيضاء في السقف.",
  "LED-verlichting binnen, en op de terrassen wandlampen gemaakt van een dakpan in de gevelkleur en witte plafondspots.",
  "Oświetlenie LED wewnątrz, a na tarasach kinkiety wykonane z dachówki pomalowanej na kolor elewacji oraz białe oprawy sufitowe.",
  "LED-belysning innendørs, og på terrassene vegglamper laget av en takstein malt i fasadefargen og hvite taklamper.",
  "LED-belysning inomhus, och på terrasserna vägglampor av en takpanna målad i fasadens kulör samt vita takspotlights.")
a('Bticino switches and sockets.',
  "Interruptores y enchufes Bticino.", "Interrupteurs et prises Bticino.", "Schalter und Steckdosen von Bticino.", "Выключатели и розетки Bticino.", "مفاتيح ومآخذ كهرباء من Bticino.",
  "Schakelaars en stopcontacten van Bticino.", "Włączniki i gniazdka Bticino.", "Brytere og stikkontakter fra Bticino.", "Strömbrytare och eluttag från Bticino.")
a('Climate-control equipment by Johnson Controls.',
  "Equipos de climatización de Johnson Controls.", "Équipements de climatisation Johnson Controls.", "Klimatechnik von Johnson Controls.", "Климатическое оборудование Johnson Controls.", "معدات تكييف من Johnson Controls.",
  "Klimaatregeling van Johnson Controls.", "Urządzenia klimatyzacyjne Johnson Controls.", "Klimaanlegg fra Johnson Controls.", "Klimatutrustning från Johnson Controls.")
a('The pools are lined with Reviglass',
  "Las piscinas están revestidas con Reviglass y el gimnasio tiene acabado de Mortex.", "Les piscines sont revêtues de Reviglass et la salle de sport est finie en Mortex.",
  "Die Pools sind mit Reviglass ausgekleidet, und der Fitnessraum ist mit Mortex ausgeführt.", "Бассейны облицованы Reviglass, а тренажёрный зал отделан Mortex.",
  "المسابح مكسوّة بمادة Reviglass، والصالة الرياضية مشطّبة بمادة Mortex.", "De zwembaden zijn bekleed met Reviglass en de gym is afgewerkt met Mortex.",
  "Baseny wyłożono Reviglass, a siłownię wykończono Mortexem.", "Bassengene er kledd med Reviglass, og treningsrommet er behandlet med Mortex.", "Poolerna är klädda med Reviglass och gymmet är utfört i Mortex.")

# ---------------------------------------------------------------- the three kinds of home
a('The ten homes fall into three groups by floor',
  "Las diez viviendas se reparten en tres grupos por planta. La tabla de abajo las lista todas con su precio.",
  "Les dix logements se répartissent en trois groupes selon l’étage. Le tableau ci-dessous les liste tous avec leur prix.",
  "Die zehn Wohnungen verteilen sich nach Geschoss auf drei Gruppen. Die Tabelle unten führt alle mit ihrem Preis auf.",
  "Десять квартир делятся на три группы по этажам. В таблице ниже перечислены все с ценами.",
  "تنقسم المساكن العشرة إلى ثلاث مجموعات بحسب الطابق. ويسردها الجدول أدناه جميعًا مع أسعارها.",
  "De tien woningen vallen naar verdieping uiteen in drie groepen. De tabel hieronder toont ze allemaal met hun prijs.",
  "Dziesięć lokali dzieli się na trzy grupy według piętra. Tabela poniżej wymienia wszystkie wraz z cenami.",
  "De ti boligene deler seg i tre grupper etter etasje. Tabellen nedenfor viser alle med pris.",
  "De tio bostäderna delas in i tre grupper efter våning. Tabellen nedan listar alla med pris.")
a('First-floor homes',
  "Viviendas en primera planta", "Logements au premier étage", "Wohnungen im ersten Obergeschoss", "Квартиры на втором этаже", "مساكن الطابق الأول",
  "Woningen op de eerste verdieping", "Lokale na pierwszym piętrze", "Boliger i andre etasje", "Bostäder på första våningen")
a('3 homes on the ground floor',
  "3 viviendas en planta baja con dos dormitorios y dos baños: la 6-0-1 y la 7-0-1 con {N104.05} {U} interiores y {N121.61} {U} construidos, y la 8-0-3 con {N113.24} {U} interiores y {N145.68} {U} construidos, según la lista de precios.",
  "3 logements au rez-de-chaussée de deux chambres et deux salles de bain : les 6-0-1 et 7-0-1 avec {N104.05} {U} intérieurs et {N121.61} {U} construits, et le 8-0-3 avec {N113.24} {U} intérieurs et {N145.68} {U} construits, selon la liste de prix.",
  "3 Wohnungen im Erdgeschoss mit zwei Schlafzimmern und zwei Badezimmern: 6-0-1 und 7-0-1 mit {N104.05} {U} Innenfläche und {N121.61} {U} bebauter Fläche sowie 8-0-3 mit {N113.24} {U} Innenfläche und {N145.68} {U} bebauter Fläche, wie in der Preisliste angegeben.",
  "3 квартиры на первом этаже с двумя спальнями и двумя ванными комнатами: 6-0-1 и 7-0-1 с внутренней площадью {N104.05} {U} и площадью застройки {N121.61} {U}, а также 8-0-3 с внутренней площадью {N113.24} {U} и площадью застройки {N145.68} {U} — по данным прайс-листа.",
  "3 مساكن في الطابق الأرضي من غرفتي نوم وحمامين: المسكنان 6-0-1 و7-0-1 بمساحة داخلية {N104.05} {U} ومساحة مبنية {N121.61} {U}، والمسكن 8-0-3 بمساحة داخلية {N113.24} {U} ومساحة مبنية {N145.68} {U}، وفق قائمة الأسعار.",
  "3 woningen op de begane grond met twee slaapkamers en twee badkamers: 6-0-1 en 7-0-1 met {N104.05} {U} binnenoppervlak en {N121.61} {U} bebouwde oppervlakte, en 8-0-3 met {N113.24} {U} binnenoppervlak en {N145.68} {U} bebouwde oppervlakte, zoals de prijslijst ze opgeeft.",
  "3 lokale na parterze z dwiema sypialniami i dwiema łazienkami: 6-0-1 i 7-0-1 o powierzchni wewnętrznej {N104.05} {U} i powierzchni zabudowy {N121.61} {U} oraz 8-0-3 o powierzchni wewnętrznej {N113.24} {U} i powierzchni zabudowy {N145.68} {U}, według cennika.",
  "3 boliger i første etasje med to soverom og to bad: 6-0-1 og 7-0-1 med {N104.05} {U} innvendig areal og {N121.61} {U} bebygd areal, og 8-0-3 med {N113.24} {U} innvendig areal og {N145.68} {U} bebygd areal, slik prislisten oppgir.",
  "3 bostäder på bottenvåningen med två sovrum och två badrum: 6-0-1 och 7-0-1 med {N104.05} {U} invändig yta och {N121.61} {U} byggyta, och 8-0-3 med {N113.24} {U} invändig yta och {N145.68} {U} byggyta, så som prislistan anger.")
a('Terraces of 49.55 sqm for the first two',
  "Terrazas de {N49.55} {U} para las dos primeras y de {N38.56} {U} para la 8-0-3. El plano que tenemos de esta planta muestra un salón, una cocina, dos dormitorios, dos baños, un aseo y tres terrazas, y cubre la 6-0-1 y la 7-0-1.",
  "Terrasses de {N49.55} {U} pour les deux premiers et de {N38.56} {U} pour le 8-0-3. Le plan dont nous disposons pour cet étage montre un séjour, une cuisine, deux chambres, deux salles de bain, des toilettes et trois terrasses, et couvre les 6-0-1 et 7-0-1.",
  "Terrassen mit {N49.55} {U} bei den ersten beiden und {N38.56} {U} bei 8-0-3. Der Grundriss, der uns für dieses Geschoss vorliegt, zeigt ein Wohnzimmer, eine Küche, zwei Schlafzimmer, zwei Badezimmer, ein WC und drei Terrassen und gilt für 6-0-1 und 7-0-1.",
  "Террасы — {N49.55} {U} у первых двух и {N38.56} {U} у 8-0-3. План этого этажа, который есть у нас, показывает гостиную, кухню, две спальни, две ванные комнаты, туалет и три террасы и относится к 6-0-1 и 7-0-1.",
  "التراسات {N49.55} {U} للمسكنين الأولين و{N38.56} {U} للمسكن 8-0-3. يُظهر المخطط الذي لدينا لهذا الطابق غرفة معيشة ومطبخًا وغرفتي نوم وحمامين ومرحاضًا وثلاثة تراسات، ويخص المسكنين 6-0-1 و7-0-1.",
  "Terrassen van {N49.55} {U} bij de eerste twee en {N38.56} {U} bij 8-0-3. De plattegrond die wij van deze verdieping hebben toont een woonkamer, een keuken, twee slaapkamers, twee badkamers, een toilet en drie terrassen, en geldt voor 6-0-1 en 7-0-1.",
  "Tarasy o powierzchni {N49.55} {U} przy dwóch pierwszych i {N38.56} {U} przy 8-0-3. Rzut tego piętra, który posiadamy, pokazuje salon, kuchnię, dwie sypialnie, dwie łazienki, toaletę i trzy tarasy i dotyczy 6-0-1 i 7-0-1.",
  "Terrasser på {N49.55} {U} for de to første og {N38.56} {U} for 8-0-3. Plantegningen vi har for denne etasjen viser en stue, et kjøkken, to soverom, to bad, et toalett og tre terrasser, og gjelder 6-0-1 og 7-0-1.",
  "Terrasser på {N49.55} {U} för de två första och {N38.56} {U} för 8-0-3. Planritningen vi har för den här våningen visar ett vardagsrum, ett kök, två sovrum, två badrum, en toalett och tre terrasser, och gäller 6-0-1 och 7-0-1.")
for lo, hi in (('470000', '570000'), ('540000', '599000'), ('500000', '600000')):
    a(f'Prices run from EUR {int(lo):,} to EUR {int(hi):,}.',
      f"Los precios van de {{E{lo}}} a {{E{hi}}}.", f"Les prix vont de {{E{lo}}} à {{E{hi}}}.", f"Die Preise reichen von {{E{lo}}} bis {{E{hi}}}.",
      f"Цены — от {{E{lo}}} до {{E{hi}}}.", f"تتراوح الأسعار من {{E{lo}}} إلى {{E{hi}}}.", f"De prijzen lopen van {{E{lo}}} tot {{E{hi}}}.",
      f"Ceny wahają się od {{E{lo}}} do {{E{hi}}}.", f"Prisene går fra {{E{lo}}} til {{E{hi}}}.", f"Priserna ligger mellan {{E{lo}}} och {{E{hi}}}.") if f'Prices run from EUR {int(lo):,} to EUR {int(hi):,}.' in todo else None
a('4 homes on the first floor',
  "4 viviendas en primera planta con dos dormitorios y dos baños, cada una con {N113.24} {U} interiores, {N145.68} {U} construidos y una terraza de {N38.56} {U} según la lista de precios.",
  "4 logements au premier étage de deux chambres et deux salles de bain, chacun avec {N113.24} {U} intérieurs, {N145.68} {U} construits et une terrasse de {N38.56} {U} selon la liste de prix.",
  "4 Wohnungen im ersten Obergeschoss mit zwei Schlafzimmern und zwei Badezimmern, jeweils mit {N113.24} {U} Innenfläche, {N145.68} {U} bebauter Fläche und einer Terrasse von {N38.56} {U} laut Preisliste.",
  "4 квартиры на втором этаже с двумя спальнями и двумя ванными комнатами: по прайс-листу у каждой внутренняя площадь {N113.24} {U}, площадь застройки {N145.68} {U} и терраса {N38.56} {U}.",
  "4 مساكن في الطابق الأول من غرفتي نوم وحمامين، لكل منها مساحة داخلية {N113.24} {U} ومساحة مبنية {N145.68} {U} وتراس {N38.56} {U} وفق قائمة الأسعار.",
  "4 woningen op de eerste verdieping met twee slaapkamers en twee badkamers, elk met {N113.24} {U} binnenoppervlak, {N145.68} {U} bebouwde oppervlakte en een terras van {N38.56} {U} volgens de prijslijst.",
  "4 lokale na pierwszym piętrze z dwiema sypialniami i dwiema łazienkami, każdy o powierzchni wewnętrznej {N113.24} {U}, powierzchni zabudowy {N145.68} {U} i z tarasem {N38.56} {U} według cennika.",
  "4 boliger i andre etasje med to soverom og to bad, hver med {N113.24} {U} innvendig areal, {N145.68} {U} bebygd areal og en terrasse på {N38.56} {U} ifølge prislisten.",
  "4 bostäder på första våningen med två sovrum och två badrum, var och en med {N113.24} {U} invändig yta, {N145.68} {U} byggyta och en terrass på {N38.56} {U} enligt prislistan.")
a('The plan shows a living and dining room of 31.70 sqm',
  "El plano muestra un salón comedor de {N31.70} {U}, una cocina de {N13.80} {U}, dormitorios de {N14.05} y {N14.27} {U}, dos baños y un aseo.",
  "Le plan montre un séjour-salle à manger de {N31.70} {U}, une cuisine de {N13.80} {U}, des chambres de {N14.05} et {N14.27} {U}, deux salles de bain et des toilettes.",
  "Der Grundriss zeigt einen Wohn- und Essbereich von {N31.70} {U}, eine Küche von {N13.80} {U}, Schlafzimmer von {N14.05} und {N14.27} {U}, zwei Badezimmer und ein WC.",
  "На плане — гостиная со столовой {N31.70} {U}, кухня {N13.80} {U}, спальни {N14.05} и {N14.27} {U}, две ванные комнаты и туалет.",
  "يُظهر المخطط غرفة معيشة وطعام بمساحة {N31.70} {U}، ومطبخًا بمساحة {N13.80} {U}، وغرفتي نوم بمساحة {N14.05} و{N14.27} {U}، وحمامين ومرحاضًا.",
  "De plattegrond toont een woon- en eetkamer van {N31.70} {U}, een keuken van {N13.80} {U}, slaapkamers van {N14.05} en {N14.27} {U}, twee badkamers en een toilet.",
  "Rzut pokazuje salon z jadalnią o powierzchni {N31.70} {U}, kuchnię {N13.80} {U}, sypialnie {N14.05} i {N14.27} {U}, dwie łazienki i toaletę.",
  "Plantegningen viser en stue med spiseplass på {N31.70} {U}, et kjøkken på {N13.80} {U}, soverom på {N14.05} og {N14.27} {U}, to bad og et toalett.",
  "Planritningen visar ett vardagsrum med matplats på {N31.70} {U}, ett kök på {N13.80} {U}, sovrum på {N14.05} och {N14.27} {U}, två badrum och en toalett.")
a('3 duplex penthouses with two bedrooms',
  "3 áticos dúplex con dos dormitorios y dos baños: el 5-AT-6 con {N102.38} {U} interiores, {N125.61} {U} construidos y {N63.86} {U} de terraza, y el 10-AT-8 y el 10-AT-9 con {N114.06} {U} interiores, {N146.73} {U} construidos y {N64.54} {U} de terraza, según la lista de precios.",
  "3 penthouses duplex de deux chambres et deux salles de bain : le 5-AT-6 avec {N102.38} {U} intérieurs, {N125.61} {U} construits et {N63.86} {U} de terrasse, et les 10-AT-8 et 10-AT-9 avec {N114.06} {U} intérieurs, {N146.73} {U} construits et {N64.54} {U} de terrasse, selon la liste de prix.",
  "3 Maisonette-Penthäuser mit zwei Schlafzimmern und zwei Badezimmern: 5-AT-6 mit {N102.38} {U} Innenfläche, {N125.61} {U} bebauter Fläche und {N63.86} {U} Terrasse sowie 10-AT-8 und 10-AT-9 mit {N114.06} {U} Innenfläche, {N146.73} {U} bebauter Fläche und {N64.54} {U} Terrasse, laut Preisliste.",
  "3 двухуровневых пентхауса с двумя спальнями и двумя ванными комнатами: 5-AT-6 с внутренней площадью {N102.38} {U}, площадью застройки {N125.61} {U} и террасой {N63.86} {U}, а также 10-AT-8 и 10-AT-9 с внутренней площадью {N114.06} {U}, площадью застройки {N146.73} {U} и террасой {N64.54} {U} — по прайс-листу.",
  "3 بنتهاوس دوبلكس من غرفتي نوم وحمامين: البنتهاوس 5-AT-6 بمساحة داخلية {N102.38} {U} ومساحة مبنية {N125.61} {U} وتراس {N63.86} {U}، والبنتهاوسان 10-AT-8 و10-AT-9 بمساحة داخلية {N114.06} {U} ومساحة مبنية {N146.73} {U} وتراس {N64.54} {U}، وفق قائمة الأسعار.",
  "3 duplexpenthouses met twee slaapkamers en twee badkamers: 5-AT-6 met {N102.38} {U} binnenoppervlak, {N125.61} {U} bebouwde oppervlakte en {N63.86} {U} terras, en 10-AT-8 en 10-AT-9 met {N114.06} {U} binnenoppervlak, {N146.73} {U} bebouwde oppervlakte en {N64.54} {U} terras, volgens de prijslijst.",
  "3 dwupoziomowe penthouse’y z dwiema sypialniami i dwiema łazienkami: 5-AT-6 o powierzchni wewnętrznej {N102.38} {U}, powierzchni zabudowy {N125.61} {U} i tarasie {N63.86} {U} oraz 10-AT-8 i 10-AT-9 o powierzchni wewnętrznej {N114.06} {U}, powierzchni zabudowy {N146.73} {U} i tarasie {N64.54} {U}, według cennika.",
  "3 toppleiligheter i to plan med to soverom og to bad: 5-AT-6 med {N102.38} {U} innvendig areal, {N125.61} {U} bebygd areal og {N63.86} {U} terrasse, og 10-AT-8 og 10-AT-9 med {N114.06} {U} innvendig areal, {N146.73} {U} bebygd areal og {N64.54} {U} terrasse, ifølge prislisten.",
  "3 takvåningar i två plan med två sovrum och två badrum: 5-AT-6 med {N102.38} {U} invändig yta, {N125.61} {U} byggyta och {N63.86} {U} terrass, och 10-AT-8 och 10-AT-9 med {N114.06} {U} invändig yta, {N146.73} {U} byggyta och {N64.54} {U} terrass, enligt prislistan.")
a('The plans put the living areas and the main bedroom',
  "Los planos sitúan las zonas de día y el dormitorio principal en la planta inferior, y un segundo dormitorio, un baño y una terraza en la planta superior.",
  "Les plans placent les pièces de vie et la chambre principale à l’étage inférieur, et une deuxième chambre, une salle de bain et une terrasse à l’étage supérieur.",
  "Die Grundrisse legen die Wohnbereiche und das Hauptschlafzimmer in das untere Geschoss, ein zweites Schlafzimmer, ein Badezimmer und eine Terrasse in das obere.",
  "По планам жилые зоны и главная спальня находятся на нижнем этаже, а вторая спальня, ванная комната и терраса — на верхнем.",
  "تضع المخططات مناطق المعيشة وغرفة النوم الرئيسية في الطابق السفلي، وغرفة نوم ثانية وحمامًا وتراسًا في الطابق العلوي.",
  "Volgens de plattegronden liggen de woonruimten en de hoofdslaapkamer op de onderste verdieping, en een tweede slaapkamer, een badkamer en een terras op de bovenste.",
  "Według rzutów strefy dzienne i główna sypialnia znajdują się na dolnym piętrze, a druga sypialnia, łazienka i taras na górnym.",
  "Plantegningene legger oppholdsrommene og hovedsoverommet i nedre etasje, og et andre soverom, et bad og en terrasse i øvre etasje.",
  "Planritningarna lägger vardagsutrymmena och huvudsovrummet på nedre våningen, och ett andra sovrum, ett badrum och en terrass på övre våningen.")

# ---------------------------------------------------------------- lifestyle
a('Pools, <em>a gym</em> and the golf nearby',
  "Piscinas, <em>un gimnasio</em> y el golf cerca", "Piscines, <em>une salle de sport</em> et le golf à proximité", "Pools, <em>ein Fitnessraum</em> und Golf in der Nähe", "Бассейны, <em>тренажёрный зал</em> и гольф рядом", "مسابح، <em>وصالة رياضية</em> وغولف قريب",
  "Zwembaden, <em>een gym</em> en golf in de buurt", "Baseny, <em>siłownia</em> i golf w pobliżu", "Bassenger, <em>et treningsrom</em> og golf like ved", "Pooler, <em>ett gym</em> och golf i närheten")
a('Life here is outdoors, between the terrace',
  "La vida aquí es al aire libre, entre la terraza, los jardines y las piscinas compartidas.", "La vie ici se passe en plein air, entre la terrasse, les jardins et les piscines communes.",
  "Das Leben hier spielt sich im Freien ab, zwischen Terrasse, Gärten und gemeinsamen Pools.", "Жизнь здесь проходит на открытом воздухе: между террасой, садами и общими бассейнами.",
  "الحياة هنا في الهواء الطلق، بين التراس والحدائق والمسابح المشتركة.", "Het leven speelt zich hier buiten af, tussen het terras, de tuinen en de gedeelde zwembaden.",
  "Życie toczy się tu na świeżym powietrzu, między tarasem, ogrodami i wspólnymi basenami.", "Livet her utspiller seg ute, mellom terrassen, hagene og de felles bassengene.",
  "Livet här utspelar sig utomhus, mellan terrassen, trädgårdarna och de gemensamma poolerna.")
a('Two pools and a solarium in landscaped gardens',
  "Dos piscinas y un solárium en jardines cuidados, tal como los enumera el folleto.", "Deux piscines et un solarium dans des jardins paysagers, comme les énumère la brochure.",
  "Zwei Pools und ein Solarium in gepflegten Gärten, wie die Broschüre sie aufführt.", "Два бассейна и солярий в благоустроенных садах — так их перечисляет брошюра.",
  "مسبحان وسولاريوم في حدائق منسّقة، كما يعددها الكتيّب.", "Twee zwembaden en een solarium in verzorgde tuinen, zoals de brochure ze opsomt.",
  "Dwa baseny i solarium w zadbanych ogrodach, tak jak wymienia je broszura.", "To bassenger og en solterrasse i opparbeidede hager, slik brosjyren lister dem.",
  "Två pooler och en solterrass i anlagda trädgårdar, så som broschyren listar dem.")
a('An equipped gym and a wellness area.',
  "Un gimnasio equipado y una zona de bienestar. El folleto menciona además un espacio Zen, y el portal enumera un spa.",
  "Une salle de sport équipée et un espace bien-être. La brochure mentionne aussi un espace zen, et le portail indique un spa.",
  "Ein ausgestatteter Fitnessraum und ein Wellnessbereich. Die Broschüre erwähnt außerdem einen Zen-Bereich, und das Portal nennt einen Spa.",
  "Оборудованный тренажёрный зал и велнес-зона. В брошюре также упомянуто дзен-пространство, а на портале указан спа.",
  "صالة رياضية مجهزة ومنطقة للعافية. ويذكر الكتيّب أيضًا مساحة زِن، وتذكر البوابة سبا.",
  "Een uitgeruste gym en een wellnessruimte. De brochure noemt ook een zenruimte, en het portaal vermeldt een spa.",
  "Wyposażona siłownia i strefa wellness. Broszura wspomina też strefę zen, a portal wymienia spa.",
  "Et utstyrt treningsrom og et velværeområde. Brosjyren nevner også et zen-rom, og portalen oppgir et spa.",
  "Ett utrustat gym och en wellnessavdelning. Broschyren nämner också ett zenrum, och portalen anger ett spa.")
a('Dining outdoors', "Comer al aire libre", "Déjeuner en plein air", "Essen im Freien", "Трапезы на воздухе", "تناول الطعام في الهواء الطلق", "Buiten eten", "Jedzenie na świeżym powietrzu", "Måltider ute", "Måltider utomhus")
a('The brochure lists a gastronomic area',
  "El folleto menciona un área gastronómica y muestra un pabellón abierto cubierto con parrilla y asientos.",
  "La brochure mentionne un espace gastronomique et montre un pavillon ouvert couvert avec un gril et des places assises.",
  "Die Broschüre nennt einen gastronomischen Bereich und zeigt einen überdachten offenen Pavillon mit Grill und Sitzgelegenheiten.",
  "В брошюре указана гастрономическая зона и показан крытый открытый павильон с грилем и местами для сидения.",
  "يذكر الكتيّب منطقة للطعام ويعرض جناحًا مفتوحًا مسقوفًا بشواية ومقاعد.",
  "De brochure vermeldt een gastronomische zone en toont een overdekt open paviljoen met een grill en zitplaatsen.",
  "Broszura wymienia strefę gastronomiczną i pokazuje zadaszony otwarty pawilon z grillem i miejscami do siedzenia.",
  "Brosjyren nevner et gastronomisk område og viser en overbygd åpen paviljong med grill og sitteplasser.",
  "Broschyren nämner ett gastronomiskt område och visar en övertäckt öppen paviljong med grill och sittplatser.")
a('The golf and the hills', "El golf y las colinas", "Le golf et les collines", "Golf und Hügel", "Гольф и холмы", "الغولف والتلال", "Golf en heuvels", "Golf i wzgórza", "Golf og åsene", "Golf och kullar")
a('The brochure counts three golf courses within a few minutes and names',
  "El folleto cuenta tres campos de golf a pocos minutos y cita pinares, eucaliptos y el lago de las Tortugas cerca para pasear.",
  "La brochure compte trois parcours de golf à quelques minutes et cite des pinèdes, des eucalyptus et le lac de las Tortugas à proximité pour la promenade.",
  "Die Broschüre nennt drei Golfplätze in wenigen Minuten Entfernung sowie Pinienwälder, Eukalyptus und den Lago de las Tortugas in der Nähe zum Spazierengehen.",
  "В брошюре указаны три поля для гольфа в нескольких минутах и упомянуты рядом сосновые рощи, эвкалипты и озеро Лас-Тортугас для прогулок.",
  "يذكر الكتيّب ثلاثة ملاعب غولف على بعد دقائق قليلة، ويسمّي غابات الصنوبر والأوكالبتوس وبحيرة لاس تورتوغاس القريبة للمشي.",
  "De brochure telt drie golfbanen op enkele minuten afstand en noemt in de buurt dennenbossen, eucalyptus en het Lago de las Tortugas om te wandelen.",
  "Broszura podaje trzy pola golfowe w odległości kilku minut i wymienia w pobliżu sosnowe lasy, eukaliptusy i jezioro Lago de las Tortugas do spacerów.",
  "Brosjyren oppgir tre golfbaner på få minutters avstand og nevner furuskog, eukalyptus og Lago de las Tortugas i nærheten til turer.",
  "Broschyren anger tre golfbanor på några minuters avstånd och nämner tallskog, eukalyptus och Lago de las Tortugas i närheten för promenader.")

# ---------------------------------------------------------------- location
a('Nueva Andalucía, <em>ten minutes from Puerto Banús</em>',
  "Nueva Andalucía, <em>a diez minutos de Puerto Banús</em>", "Nueva Andalucía, <em>à dix minutes de Puerto Banús</em>", "Nueva Andalucía, <em>zehn Minuten von Puerto Banús</em>",
  "Нуэва-Андалусия, <em>в десяти минутах от Пуэрто-Бануса</em>", "نويفا أندلوثيا، <em>على بعد عشر دقائق من بويرتو بانوس</em>", "Nueva Andalucía, <em>tien minuten van Puerto Banús</em>",
  "Nueva Andalucía, <em>dziesięć minut od Puerto Banús</em>", "Nueva Andalucía, <em>ti minutter fra Puerto Banús</em>", "Nueva Andalucía, <em>tio minuter från Puerto Banús</em>")
a('The portal places the complex in the heart of Nueva Andalucía',
  "El portal sitúa el complejo en el corazón de Nueva Andalucía, cerca de campos de golf, centros comerciales, restaurantes y colegios internacionales, y a pocos minutos en coche de Puerto Banús. Los tiempos y las distancias de abajo son los del mapa del folleto del promotor de 2023.",
  "Le portail situe la résidence au cœur de Nueva Andalucía, près de parcours de golf, de centres commerciaux, de restaurants et d’écoles internationales, et à quelques minutes en voiture de Puerto Banús. Les durées de trajet et les distances ci-dessous proviennent de la carte de la brochure du promoteur de 2023.",
  "Das Portal verortet die Anlage im Herzen von Nueva Andalucía, nahe Golfplätzen, Einkaufszentren, Restaurants und internationalen Schulen und nur wenige Autominuten von Puerto Banús entfernt. Die Fahrzeiten und Entfernungen unten stammen aus der Karte in der Broschüre des Bauträgers von 2023.",
  "Портал помещает комплекс в самое сердце Нуэва-Андалусии, рядом с полями для гольфа, торговыми центрами, ресторанами и международными школами, в нескольких минутах езды от Пуэрто-Бануса. Время в пути и расстояния ниже взяты с карты в брошюре застройщика 2023 года.",
  "تضع البوابة المجمع في قلب نويفا أندلوثيا، قرب ملاعب الغولف ومراكز التسوق والمطاعم والمدارس الدولية، وعلى بعد دقائق قليلة بالسيارة من بويرتو بانوس. أزمنة القيادة والمسافات أدناه مأخوذة من الخريطة الواردة في كتيّب المطوّر لعام 2023.",
  "Het portaal plaatst het complex in het hart van Nueva Andalucía, dicht bij golfbanen, winkelcentra, restaurants en internationale scholen, en op enkele autominuten van Puerto Banús. De reistijden en afstanden hieronder komen van de kaart in de brochure van de ontwikkelaar uit 2023.",
  "Portal umieszcza kompleks w sercu Nueva Andalucía, blisko pól golfowych, centrów handlowych, restauracji i szkół międzynarodowych oraz kilka minut jazdy samochodem od Puerto Banús. Czasy dojazdu i odległości poniżej pochodzą z mapy w broszurze dewelopera z 2023 r.",
  "Portalen plasserer anlegget i hjertet av Nueva Andalucía, nær golfbaner, kjøpesentre, restauranter og internasjonale skoler, og noen få minutter med bil fra Puerto Banús. Kjøretidene og avstandene nedenfor er fra kartet i utbyggerens brosjyre fra 2023.",
  "Portalen placerar området i hjärtat av Nueva Andalucía, nära golfbanor, köpcentrum, restauranter och internationella skolor, och några minuter med bil från Puerto Banús. Körtiderna och avstånden nedan kommer från kartan i exploatörens broschyr från 2023.")
same('nuevaAndalucia')
a('Puerto Banús beach', "Playa de Puerto Banús", "Plage de Puerto Banús", "Strand von Puerto Banús", "Пляж Пуэрто-Бануса", "شاطئ بويرتو بانوس", "Strand van Puerto Banús", "Plaża Puerto Banús", "Stranden i Puerto Banús", "Stranden i Puerto Banús")
a('Nueva Andalucía beach', "Playa de Nueva Andalucía", "Plage de Nueva Andalucía", "Strand von Nueva Andalucía", "Пляж Нуэва-Андалусии", "شاطئ نويفا أندلوثيا", "Strand van Nueva Andalucía", "Plaża Nueva Andalucía", "Stranden i Nueva Andalucía", "Stranden i Nueva Andalucía")
MIN = {'es': 'minutos', 'fr': 'minutes', 'de': 'Minuten', 'ru': 'минут', 'ar': 'دقيقة', 'nl': 'minuten', 'pl': 'minut', 'no': 'minutter', 'sv': 'minuter'}
for m, km in ((10, 5), (12, 6), (15, 8), (18, 10), (58, 70)):
    en = f'{m} minutes, {km} km'
    if en in todo:
        row = []
        for l in LOCS:
            word = 'دقائق' if (l == 'ar' and m == 10) else MIN[l]
            sep = '، ' if l == 'ar' else ', '
            row.append(f'{m} {word}{sep}{km} {KM.get(l, "km")}')
        a(en, *row)

# ---------------------------------------------------------------- how the purchase works
a('The terms are those of the developer’s price list and portal',
  "Las condiciones son las de la lista de precios y el portal del promotor. Confirmamos por escrito los importes y fechas actuales antes de que reserve.",
  "Les conditions sont celles de la liste de prix et du portail du promoteur. Nous confirmons par écrit les montants et dates actuels avant que vous ne réserviez.",
  "Die Bedingungen sind die der Preisliste und des Portals des Bauträgers. Wir bestätigen die aktuellen Beträge und Termine schriftlich, bevor Sie reservieren.",
  "Условия определяются прайс-листом и порталом застройщика. Перед бронированием мы письменно подтверждаем актуальные суммы и даты.",
  "الشروط هي شروط قائمة أسعار المطوّر وبوابته. ونؤكد كتابةً المبالغ والتواريخ الحالية قبل أن تحجزوا.",
  "De voorwaarden zijn die van de prijslijst en het portaal van de ontwikkelaar. We bevestigen de actuele bedragen en data schriftelijk voordat u reserveert.",
  "Warunki są takie, jak w cenniku i na portalu dewelopera. Przed rezerwacją potwierdzamy na piśmie aktualne kwoty i terminy.",
  "Vilkårene er de i utbyggerens prisliste og portal. Vi bekrefter gjeldende beløp og datoer skriftlig før du reserverer.",
  "Villkoren är de i exploatörens prislista och portal. Vi bekräftar gällande belopp och datum skriftligen innan ni reserverar.")
a('The portal gives EUR 4,900 on signing',
  "El portal indica {E4900} al firmar el contrato privado de compraventa y el resto al firmar la escritura.",
  "Le portail indique {E4900} à la signature du contrat de vente privé et le solde à la signature de l’acte.",
  "Das Portal nennt {E4900} bei Unterzeichnung des privaten Kaufvertrags und den Rest bei Unterzeichnung der Kaufurkunde.",
  "Портал указывает {E4900} при подписании предварительного договора купли-продажи и остаток при подписании нотариального акта.",
  "تذكر البوابة {E4900} عند توقيع عقد الشراء الخاص، والباقي عند توقيع سند الملكية.",
  "Het portaal geeft {E4900} bij ondertekening van de onderhandse koopovereenkomst en de rest bij ondertekening van de eigendomsakte.",
  "Portal podaje {E4900} przy podpisaniu umowy przedwstępnej, a resztę przy podpisaniu aktu notarialnego przeniesienia własności.",
  "Portalen oppgir {E4900} ved signering av den private kjøpekontrakten og resten ved signering av skjøtet.",
  "Portalen anger {E4900} vid undertecknandet av det privata köpeavtalet och resten vid undertecknandet av köpehandlingen.")
a('Tax', "Impuesto", "Taxe", "Steuer", "Налог", "الضريبة", "Belasting", "Podatek", "Skatt", "Skatt")
a('The price list does not add VAT.',
  "La lista de precios no añade IVA. Indica que los precios deben incrementarse con el {P7} de ITP, el impuesto de transmisiones patrimoniales. Nueva Living confirma por escrito el impuesto y los gastos de compra.",
  "La liste de prix n’ajoute pas la TVA. Elle indique que les prix doivent être majorés de {P7} d’ITP, l’impôt sur les transmissions patrimoniales. Nueva Living confirme par écrit l’impôt et les frais d’achat.",
  "Die Preisliste addiert keine MwSt. Sie gibt an, dass auf die Preise {P7} ITP aufzuschlagen sind, die Grunderwerbsteuer. Nueva Living bestätigt Steuer und Kaufnebenkosten schriftlich.",
  "Прайс-лист не добавляет НДС. В нём сказано, что к ценам нужно прибавить {P7} ITP — налог на передачу имущества. Nueva Living письменно подтверждает налог и расходы на покупку.",
  "لا تضيف قائمة الأسعار ضريبة القيمة المضافة. وتذكر أنه يجب زيادة الأسعار بنسبة {P7} ضريبة ITP، أي ضريبة نقل الملكية. وتؤكد Nueva Living الضريبة ومصاريف الشراء كتابةً.",
  "De prijslijst telt geen btw op. Ze vermeldt dat de prijzen met {P7} ITP moeten worden verhoogd, de overdrachtsbelasting. Nueva Living bevestigt de belasting en de aankoopkosten schriftelijk.",
  "Cennik nie dolicza VAT. Podaje, że ceny należy powiększyć o {P7} ITP, podatek od przeniesienia własności. Nueva Living potwierdza na piśmie podatek i koszty zakupu.",
  "Prislisten legger ikke til mva. Den oppgir at prisene må økes med {P7} ITP, skatten på eiendomsoverdragelse. Nueva Living bekrefter skatten og kjøpskostnadene skriftlig.",
  "Prislistan lägger inte till moms. Den anger att priserna ska ökas med {P7} ITP, överlåtelseskatten. Nueva Living bekräftar skatten och köpkostnaderna skriftligen.")
a('Each home comes with one parking space and one storage room, as the price list says',
  "Cada vivienda incluye una plaza de aparcamiento y un trastero, según la lista de precios, y el folleto dice que el aparcamiento es subterráneo. La lista de precios no menciona el mobiliario.",
  "Chaque logement comprend une place de stationnement et un débarras, selon la liste de prix, et la brochure précise que le stationnement est en sous-sol. La liste de prix ne mentionne pas le mobilier.",
  "Zu jeder Wohnung gehören laut Preisliste ein Stellplatz und ein Abstellraum, und laut Broschüre liegt der Stellplatz in der Tiefgarage. Die Preisliste erwähnt keine Möbel.",
  "К каждой квартире, согласно прайс-листу, прилагаются одно парковочное место и одна кладовая, а в брошюре сказано, что парковка подземная. Мебель в прайс-листе не упоминается.",
  "يأتي مع كل مسكن موقف سيارات واحد ومخزن واحد وفق قائمة الأسعار، ويذكر الكتيّب أن الموقف تحت الأرض. ولا تذكر قائمة الأسعار الأثاث.",
  "Bij elke woning horen volgens de prijslijst één parkeerplaats en één berging, en de brochure zegt dat de parkeerplaats ondergronds is. De prijslijst noemt geen meubilair.",
  "Do każdego lokalu należą według cennika jedno miejsce parkingowe i jedna komórka lokatorska, a broszura podaje, że parking jest podziemny. Cennik nie wspomina o meblach.",
  "Til hver bolig hører ifølge prislisten én parkeringsplass og én bod, og brosjyren sier at parkeringen er under bakken. Prislisten nevner ikke møbler.",
  "Till varje bostad hör enligt prislistan en parkeringsplats och ett förråd, och broschyren säger att parkeringen är under jord. Prislistan nämner inga möbler.")
a('The documents give no reservation amount',
  "Los documentos no dan importe ni condiciones de reserva. Los pedimos, y también cómo se custodia la reserva, antes de cualquier pago.",
  "Les documents ne donnent ni montant ni conditions de réservation. Nous les demandons, ainsi que la manière dont la réservation est conservée, avant tout paiement.",
  "Die Unterlagen nennen weder einen Reservierungsbetrag noch Bedingungen. Wir fragen beides ab, ebenso wie die Verwahrung der Reservierung, bevor eine Zahlung erfolgt.",
  "В документах нет ни суммы брони, ни её условий. Мы запрашиваем их, а также порядок хранения брони, до любого платежа.",
  "لا تذكر الوثائق مبلغ الحجز ولا شروطه. نطلبها، ونطلب كذلك كيفية حفظ مبلغ الحجز، قبل أي دفعة.",
  "De documenten geven geen reserveringsbedrag of voorwaarden. Wij vragen ze op, en ook hoe de reservering wordt bewaard, vóór er iets wordt betaald.",
  "Dokumenty nie podają kwoty ani warunków rezerwacji. Prosimy o nie, a także o informację, jak rezerwacja jest zabezpieczona, przed jakąkolwiek płatnością.",
  "Dokumentene oppgir verken reservasjonsbeløp eller vilkår. Vi ber om dem, og om hvordan reservasjonen forvares, før noen betaling.",
  "Dokumenten anger varken reservationsbelopp eller villkor. Vi ber om dem, och om hur reservationen förvaras, före varje betalning.")

# ---------------------------------------------------------------- what we check
a('Licences and completion', "Licencias y finalización", "Permis et achèvement", "Genehmigungen und Fertigstellung", "Разрешения и завершение", "الرخص والإتمام", "Vergunningen en oplevering", "Pozwolenia i ukończenie", "Tillatelser og ferdigstillelse", "Tillstånd och färdigställande")
a('The portal lists the complex as a finished building and the brochure is dated 2023',
  "El portal presenta el complejo como un edificio terminado y el folleto está fechado en 2023. Los planos llevan por título un proyecto de adecuación interior y de zonas comunes exteriores, con fecha 28 de febrero de 2023. Pedimos la licencia de primera ocupación y el certificado energético, y confirmamos que las viviendas son nuevas.",
  "Le portail présente la résidence comme un immeuble achevé et la brochure est datée de 2023. Les plans portent pour titre un projet d’aménagement intérieur et des parties communes extérieures, daté du 28 février 2023. Nous demandons la licence de première occupation et le certificat énergétique, et nous confirmons que les logements sont neufs.",
  "Das Portal führt die Anlage als fertiggestelltes Gebäude, und die Broschüre ist auf 2023 datiert. Die Grundrisse tragen den Titel eines Projekts zum Innenausbau und zu den äußeren Gemeinschaftsflächen und sind auf den 28. Februar 2023 datiert. Wir verlangen die Erstbezugsgenehmigung und den Energieausweis und bestätigen, dass die Wohnungen neu sind.",
  "Портал указывает комплекс как завершённое здание, а брошюра датирована 2023 годом. Планы озаглавлены как проект внутренней отделки и внешних общих зон и датированы 28 февраля 2023 года. Мы запрашиваем лицензию на первое заселение и энергетический сертификат и уточняем, что квартиры новые.",
  "تعرض البوابة المجمع بوصفه مبنى مكتملًا، والكتيّب مؤرخ في 2023. وعنوان المخططات مشروع تهيئة داخلية ومناطق مشتركة خارجية، وتاريخها 28 فبراير 2023. نطلب رخصة الإشغال الأول وشهادة الطاقة، ونتأكد من أن المساكن جديدة.",
  "Het portaal vermeldt het complex als een opgeleverd gebouw en de brochure is gedateerd 2023. De plattegronden dragen de titel van een project voor de inrichting van de interieurs en de buitenste gemeenschappelijke ruimten, gedateerd 28 februari 2023. Wij vragen de vergunning voor eerste ingebruikname en het energiecertificaat, en bevestigen dat de woningen nieuw zijn.",
  "Portal podaje kompleks jako budynek ukończony, a broszura jest datowana na 2023 r. Rzuty mają tytuł projektu adaptacji wnętrz i zewnętrznych części wspólnych i są datowane na 28 lutego 2023 r. Prosimy o pozwolenie na pierwsze zajęcie i świadectwo energetyczne oraz potwierdzamy, że lokale są nowe.",
  "Portalen oppfører anlegget som en ferdig bygning, og brosjyren er datert 2023. Plantegningene har tittelen et prosjekt for innredning og utvendige fellesarealer og er datert 28. februar 2023. Vi ber om brukstillatelse og energiattest, og bekrefter at boligene er nye.",
  "Portalen anger området som en färdig byggnad, och broschyren är daterad 2023. Planritningarna har rubriken ett projekt för inredning och yttre gemensamma ytor och är daterade den 28 februari 2023. Vi ber om slutbesked och energideklaration, och bekräftar att bostäderna är nya.")
a('The tax', "El impuesto", "La taxe", "Die Steuer", "Налог", "الضريبة", "De belasting", "Podatek", "Skatten", "Skatten")
a('The price list says prices must be increased by 7% ITP',
  "La lista de precios dice que los precios deben incrementarse con el {P7} de ITP y no menciona el IVA. Confirmamos por escrito qué impuesto se aplica a cada vivienda y el coste total.",
  "La liste de prix indique que les prix doivent être majorés de {P7} d’ITP et ne mentionne pas la TVA. Nous confirmons par écrit quelle taxe s’applique à chaque logement et le coût total.",
  "Die Preisliste gibt an, dass auf die Preise {P7} ITP aufzuschlagen sind, und erwähnt keine MwSt. Wir bestätigen schriftlich, welche Steuer für jede Wohnung gilt, und die Gesamtkosten.",
  "В прайс-листе сказано, что к ценам нужно прибавить {P7} ITP, а НДС не упомянут. Мы письменно подтверждаем, какой налог применяется к каждой квартире, и общую стоимость.",
  "تذكر قائمة الأسعار أنه يجب زيادة الأسعار بنسبة {P7} ضريبة ITP، ولا تذكر ضريبة القيمة المضافة. نؤكد كتابةً أي ضريبة تنطبق على كل مسكن والتكلفة الإجمالية.",
  "De prijslijst zegt dat de prijzen met {P7} ITP moeten worden verhoogd en noemt geen btw. Wij bevestigen schriftelijk welke belasting voor elke woning geldt en wat de totale kosten zijn.",
  "Cennik podaje, że ceny należy powiększyć o {P7} ITP, i nie wspomina o VAT. Potwierdzamy na piśmie, jaki podatek dotyczy każdego lokalu, oraz całkowity koszt.",
  "Prislisten sier at prisene må økes med {P7} ITP, og nevner ikke mva. Vi bekrefter skriftlig hvilke skatter som gjelder for hver bolig, og totalkostnaden.",
  "Prislistan säger att priserna ska ökas med {P7} ITP och nämner inte moms. Vi bekräftar skriftligen vilka skatter som gäller för varje bostad, och den totala kostnaden.")
a('For the first-floor homes the price list gives',
  "Para las viviendas de primera planta, la lista de precios da {N113.24} {U} interiores, {N145.68} {U} construidos y una terraza de {N38.56} {U}, y el plano da {N93.17} {U} útiles, {N113.13} {U} construidos y una terraza de {N39.14} {U}. Confirmamos qué cifras usa el contrato.",
  "Pour les logements du premier étage, la liste de prix indique {N113.24} {U} intérieurs, {N145.68} {U} construits et une terrasse de {N38.56} {U}, et le plan indique {N93.17} {U} utiles, {N113.13} {U} construits et une terrasse de {N39.14} {U}. Nous confirmons quels chiffres le contrat retient.",
  "Für die Wohnungen im ersten Obergeschoss nennt die Preisliste {N113.24} {U} Innenfläche, {N145.68} {U} bebaute Fläche und eine Terrasse von {N38.56} {U}, der Grundriss dagegen {N93.17} {U} Nutzfläche, {N113.13} {U} bebaute Fläche und eine Terrasse von {N39.14} {U}. Wir bestätigen, welche Zahlen der Vertrag verwendet.",
  "Для квартир на втором этаже прайс-лист указывает внутреннюю площадь {N113.24} {U}, площадь застройки {N145.68} {U} и террасу {N38.56} {U}, а план — полезную площадь {N93.17} {U}, площадь застройки {N113.13} {U} и террасу {N39.14} {U}. Мы уточняем, какие цифры используются в договоре.",
  "بالنسبة لمساكن الطابق الأول، تذكر قائمة الأسعار مساحة داخلية {N113.24} {U} ومساحة مبنية {N145.68} {U} وتراسًا {N38.56} {U}، بينما يذكر المخطط مساحة صافية {N93.17} {U} ومساحة مبنية {N113.13} {U} وتراسًا {N39.14} {U}. نؤكد أي الأرقام يعتمدها العقد.",
  "Voor de woningen op de eerste verdieping geeft de prijslijst {N113.24} {U} binnenoppervlak, {N145.68} {U} bebouwde oppervlakte en een terras van {N38.56} {U}, en de plattegrond {N93.17} {U} gebruiksoppervlak, {N113.13} {U} bebouwde oppervlakte en een terras van {N39.14} {U}. Wij bevestigen welke cijfers het contract hanteert.",
  "Dla lokali na pierwszym piętrze cennik podaje {N113.24} {U} powierzchni wewnętrznej, {N145.68} {U} powierzchni zabudowy i taras {N38.56} {U}, a rzut — {N93.17} {U} powierzchni użytkowej, {N113.13} {U} powierzchni zabudowy i taras {N39.14} {U}. Potwierdzamy, jakich liczb używa umowa.",
  "For boligene i andre etasje oppgir prislisten {N113.24} {U} innvendig areal, {N145.68} {U} bebygd areal og en terrasse på {N38.56} {U}, mens plantegningen oppgir {N93.17} {U} nyttbart areal, {N113.13} {U} bebygd areal og en terrasse på {N39.14} {U}. Vi bekrefter hvilke tall kontrakten bruker.",
  "För bostäderna på första våningen anger prislistan {N113.24} {U} invändig yta, {N145.68} {U} byggyta och en terrass på {N38.56} {U}, medan planritningen anger {N93.17} {U} boyta, {N113.13} {U} byggyta och en terrass på {N39.14} {U}. Vi bekräftar vilka siffror avtalet använder.")
a('The list of homes', "La lista de viviendas", "La liste des logements", "Die Liste der Wohnungen", "Список квартир", "قائمة المساكن", "De lijst met woningen", "Lista lokali", "Listen over boliger", "Listan över bostäder")
a('The portal lists ten homes and the price list file lists eleven',
  "El portal lista diez viviendas y el archivo de la lista de precios once, la adicional un ático en el bloque 8. El folleto cuenta 70 viviendas de dos y tres dormitorios, y solo se listan viviendas de dos dormitorios. Confirmamos qué hay disponible cuando nos lo pide.",
  "Le portail liste dix logements et le fichier de la liste de prix en liste onze, le logement en plus étant un penthouse du bloc 8. La brochure compte 70 logements de deux et trois chambres, et seuls des logements de deux chambres sont listés. Nous confirmons ce qui est disponible lorsque vous nous le demandez.",
  "Das Portal führt zehn Wohnungen, die Datei der Preisliste elf, die zusätzliche ist ein Penthouse in Block 8. Die Broschüre zählt 70 Wohnungen mit zwei und drei Schlafzimmern, aufgeführt sind nur Wohnungen mit zwei Schlafzimmern. Wir bestätigen, was verfügbar ist, wenn Sie danach fragen.",
  "На портале указаны десять квартир, а в файле прайс-листа — одиннадцать; лишняя — пентхаус в блоке 8. В брошюре насчитывается 70 квартир с двумя и тремя спальнями, а в продаже указаны только квартиры с двумя спальнями. Мы уточняем наличие по вашему запросу.",
  "تدرج البوابة عشرة مساكن، ويدرج ملف قائمة الأسعار أحد عشر مسكنًا، والمسكن الإضافي بنتهاوس في المبنى 8. ويحصي الكتيّب 70 مسكنًا من غرفتي نوم وثلاث غرف، ولا تُدرج إلا المساكن من غرفتي نوم. نؤكد المتاح عند طلبكم.",
  "Het portaal vermeldt tien woningen en het bestand met de prijslijst elf; de extra woning is een penthouse in blok 8. De brochure telt 70 woningen met twee en drie slaapkamers, en alleen woningen met twee slaapkamers staan vermeld. Wij bevestigen wat beschikbaar is wanneer u erom vraagt.",
  "Portal podaje dziesięć lokali, a plik cennika jedenaście; dodatkowy to penthouse w bloku 8. Broszura wymienia 70 lokali z dwiema i trzema sypialniami, a podane są tylko lokale z dwiema sypialniami. Potwierdzamy, co jest dostępne, gdy Państwo o to poproszą.",
  "Portalen oppfører ti boliger og prislistefilen elleve, den ekstra er en toppleilighet i hus 8. Brosjyren teller 70 boliger med to og tre soverom, og bare boliger med to soverom er oppført. Vi bekrefter hva som er tilgjengelig når du spør.",
  "Portalen listar tio bostäder och prislistefilen elva, den extra är en takvåning i hus 8. Broschyren räknar 70 bostäder med två och tre sovrum, och bara bostäder med två sovrum är listade. Vi bekräftar vad som är tillgängligt när ni frågar.")

# ---------------------------------------------------------------- availability
a('Ten homes <em>currently available</em>',
  "Diez viviendas <em>a la venta actualmente</em>", "Dix logements <em>actuellement annoncés</em>", "Zehn Wohnungen <em>derzeit gelistet</em>", "Десять квартир <em>сейчас в продаже</em>", "عشرة مساكن <em>معروضة حاليًا</em>",
  "Tien woningen <em>momenteel te koop</em>", "Dziesięć lokali <em>obecnie dostępnych</em>", "Ti boliger <em>annonsert nå</em>", "Tio bostäder <em>listade just nu</em>")
a('Homes are numbered by block, floor and door',
  "Las viviendas se numeran por bloque, planta y puerta: la vivienda 6-0-1 es el bloque 6, planta baja, puerta 1. Los precios son los de la lista de precios del promotor, a fecha de hoy, octubre de 2026, y no incluyen el {P7} de ITP; los confirmamos antes de cualquier reserva.",
  "Les logements sont numérotés par bloc, étage et porte : le logement 6-0-1 est le bloc 6, rez-de-chaussée, porte 1. Les prix sont ceux de la liste de prix du promoteur, à ce jour, octobre 2026, et n’incluent pas les {P7} d’ITP ; nous les confirmons avant toute réservation.",
  "Die Wohnungen sind nach Block, Geschoss und Tür nummeriert: Wohnung 6-0-1 ist Block 6, Erdgeschoss, Tür 1. Die Preise stammen aus der Preisliste des Bauträgers, Stand heute, Oktober 2026, und verstehen sich ohne die {P7} ITP; wir bestätigen sie vor jeder Reservierung.",
  "Квартиры нумеруются по блоку, этажу и двери: квартира 6-0-1 — это блок 6, первый этаж, дверь 1. Цены взяты из прайс-листа застройщика на сегодняшний день, октябрь 2026 года, и не включают {P7} ITP; мы подтверждаем их перед любым бронированием.",
  "تُرقَّم المساكن بحسب المبنى والطابق والباب: المسكن 6-0-1 هو المبنى 6، الطابق الأرضي، الباب 1. الأسعار هي أسعار قائمة المطوّر اليوم، أكتوبر 2026، ولا تشمل {P7} ضريبة ITP؛ ونؤكدها قبل أي حجز.",
  "De woningen zijn genummerd per blok, verdieping en deur: woning 6-0-1 is blok 6, begane grond, deur 1. De prijzen zijn die van de prijslijst van de ontwikkelaar, per vandaag, oktober 2026, en zijn exclusief de {P7} ITP; we bevestigen ze vóór elke reservering.",
  "Lokale są numerowane według bloku, piętra i drzwi: lokal 6-0-1 to blok 6, parter, drzwi 1. Ceny pochodzą z cennika dewelopera, na dziś, październik 2026 r., i nie zawierają {P7} ITP; potwierdzamy je przed każdą rezerwacją.",
  "Boligene er nummerert etter hus, etasje og dør: bolig 6-0-1 er hus 6, første etasje, dør 1. Prisene er de i utbyggerens prisliste, per i dag, oktober 2026, og er eksklusive {P7} ITP; vi bekrefter dem før en reservasjon.",
  "Bostäderna är numrerade efter hus, våning och dörr: bostad 6-0-1 är hus 6, bottenvåning, dörr 1. Priserna är de i exploatörens prislista, per i dag, oktober 2026, och är exklusive {P7} ITP; vi bekräftar dem före varje reservation.")
a('Prices, areas and terraces are transcribed from the developer’s price list',
  "Los precios, las superficies y las terrazas están transcritos de la lista de precios del promotor tal como la leemos en octubre de 2026; el archivo no lleva fecha. El portal lista diez viviendas como disponibles y el archivo de la lista de precios once. Esta página muestra las diez del portal y omite el ático 9 del bloque 8, que el archivo fija en {E590000}. La lista dice que los precios deben incrementarse con el {P7} de ITP y que la disponibilidad está sujeta a confirmación, y asigna a cada vivienda una plaza de aparcamiento y un trastero. La cifra interior de la lista de precios se acerca a la superficie construida de los planos, de modo que las dos fuentes difieren. Los planos, fechados el 28 de febrero de 2023, dan para las viviendas de planta baja {N86.45} {U} útiles, {N104.20} {U} construidos y {N51.95} {U} de terrazas; para las de primera planta {N93.17}, {N113.13} y {N39.14}; para el ático del bloque 5 {N83.11}, {N105.94} y {N65.05}; y para los áticos del bloque 10 {N85.77}, {N115.09} y {N63.45}. Solo se adjunta un plano cuando su hoja corresponde al tipo y la planta de la vivienda, por lo que la vivienda de planta baja 8-0-3 no tiene ninguno.",
  "Les prix, les surfaces et les terrasses sont transcrits de la liste de prix du promoteur telle que nous la lisons en octobre 2026 ; le fichier ne porte aucune date. Le portail liste dix logements comme disponibles et le fichier de la liste de prix en liste onze. Cette page présente les dix du portail et omet le penthouse 9 du bloc 8, que le fichier chiffre à {E590000}. La liste indique que les prix doivent être majorés de {P7} d’ITP et que la disponibilité est soumise à confirmation, et attribue à chaque logement une place de stationnement et un débarras. La surface intérieure de la liste de prix est proche de la surface construite des plans, si bien que les deux sources diffèrent. Les plans, datés du 28 février 2023, donnent pour les logements du rez-de-chaussée {N86.45} {U} utiles, {N104.20} {U} construits et {N51.95} {U} de terrasses ; pour ceux du premier étage {N93.17}, {N113.13} et {N39.14} ; pour le penthouse du bloc 5 {N83.11}, {N105.94} et {N65.05} ; et pour les penthouses du bloc 10 {N85.77}, {N115.09} et {N63.45}. Un plan n’est joint que lorsque sa feuille correspond au type et à l’étage du logement, de sorte que le logement du rez-de-chaussée 8-0-3 n’en a pas.",
  "Preise, Flächen und Terrassen sind der Preisliste des Bauträgers entnommen, wie wir sie im Oktober 2026 lesen; die Datei trägt kein Datum. Das Portal führt zehn Wohnungen als verfügbar, die Datei der Preisliste elf. Diese Seite zeigt die zehn des Portals und lässt das Penthouse 9 in Block 8 aus, das die Datei mit {E590000} beziffert. Die Liste gibt an, dass auf die Preise {P7} ITP aufzuschlagen sind und die Verfügbarkeit bestätigt werden muss, und ordnet jeder Wohnung einen Stellplatz und einen Abstellraum zu. Die Innenfläche der Preisliste liegt nahe an der bebauten Fläche der Grundrisse, die beiden Quellen weichen also voneinander ab. Die Grundrisse, datiert auf den 28. Februar 2023, nennen für die Erdgeschosswohnungen {N86.45} {U} Nutzfläche, {N104.20} {U} bebaute Fläche und {N51.95} {U} Terrassen, für die Wohnungen im ersten Obergeschoss {N93.17}, {N113.13} und {N39.14}, für das Penthouse in Block 5 {N83.11}, {N105.94} und {N65.05} und für die Penthäuser in Block 10 {N85.77}, {N115.09} und {N63.45}. Ein Grundriss wird nur beigefügt, wenn sein Blatt zu Typ und Geschoss der Wohnung passt; deshalb hat die Erdgeschosswohnung 8-0-3 keinen.",
  "Цены, площади и террасы переписаны из прайс-листа застройщика в том виде, как мы читаем его в октябре 2026 года; на файле нет даты. На портале десять квартир указаны как доступные, а в файле прайс-листа — одиннадцать. На этой странице показаны десять с портала; пентхаус 9 в блоке 8, который файл оценивает в {E590000}, опущен. В прайс-листе сказано, что к ценам нужно прибавить {P7} ITP и что наличие подлежит подтверждению, и за каждой квартирой закреплены одно парковочное место и одна кладовая. Внутренняя площадь в прайс-листе близка к площади застройки на планах, поэтому источники расходятся. Планы от 28 февраля 2023 года дают для квартир на первом этаже полезную площадь {N86.45} {U}, площадь застройки {N104.20} {U} и террасы {N51.95} {U}; для квартир на втором этаже — {N93.17}, {N113.13} и {N39.14}; для пентхауса в блоке 5 — {N83.11}, {N105.94} и {N65.05}; для пентхаусов в блоке 10 — {N85.77}, {N115.09} и {N63.45}. План прилагается только тогда, когда его лист соответствует типу и этажу квартиры, поэтому у квартиры 8-0-3 на первом этаже плана нет.",
  "الأسعار والمساحات والتراسات منقولة من قائمة أسعار المطوّر كما نقرؤها في أكتوبر 2026؛ والملف بلا تاريخ. تدرج البوابة عشرة مساكن على أنها متاحة، ويدرج ملف قائمة الأسعار أحد عشر. تعرض هذه الصفحة العشرة الواردة في البوابة وتستبعد البنتهاوس 9 في المبنى 8، الذي يسعّره الملف بـ {E590000}. تذكر القائمة أنه يجب زيادة الأسعار بنسبة {P7} ضريبة ITP وأن التوافر خاضع للتأكيد، وتمنح كل مسكن موقف سيارات واحدًا ومخزنًا واحدًا. والمساحة الداخلية في قائمة الأسعار قريبة من المساحة المبنية في المخططات، ولذلك يختلف المصدران. تذكر المخططات المؤرخة في 28 فبراير 2023 لمساكن الطابق الأرضي {N86.45} {U} مساحة صافية و{N104.20} {U} مساحة مبنية و{N51.95} {U} تراسات؛ ولمساكن الطابق الأول {N93.17} و{N113.13} و{N39.14}؛ وللبنتهاوس في المبنى 5 {N83.11} و{N105.94} و{N65.05}؛ وللبنتهاوس في المبنى 10 {N85.77} و{N115.09} و{N63.45}. لا يُرفق مخطط إلا حين تطابق ورقته نوع المسكن وطابقه، ولذلك لا مخطط للمسكن 8-0-3 في الطابق الأرضي.",
  "Prijzen, oppervlakten en terrassen zijn overgenomen uit de prijslijst van de ontwikkelaar zoals wij die in oktober 2026 lezen; het bestand draagt geen datum. Het portaal vermeldt tien woningen als beschikbaar en het bestand met de prijslijst elf. Deze pagina toont de tien van het portaal en laat penthouse 9 in blok 8 weg, dat het bestand op {E590000} stelt. De lijst zegt dat de prijzen met {P7} ITP moeten worden verhoogd en dat de beschikbaarheid onder voorbehoud van bevestiging is, en kent elke woning één parkeerplaats en één berging toe. Het binnenoppervlak in de prijslijst ligt dicht bij de bebouwde oppervlakte op de plattegronden, dus de twee bronnen verschillen. De plattegronden, gedateerd 28 februari 2023, geven voor de woningen op de begane grond {N86.45} {U} gebruiksoppervlak, {N104.20} {U} bebouwd en {N51.95} {U} terrassen; voor die op de eerste verdieping {N93.17}, {N113.13} en {N39.14}; voor het penthouse in blok 5 {N83.11}, {N105.94} en {N65.05}; en voor de penthouses in blok 10 {N85.77}, {N115.09} en {N63.45}. Een plattegrond wordt alleen toegevoegd als het blad past bij het type en de verdieping van de woning, daarom heeft woning 8-0-3 op de begane grond er geen.",
  "Ceny, powierzchnie i tarasy przepisano z cennika dewelopera w takiej postaci, w jakiej czytamy go w październiku 2026 r.; plik nie ma daty. Portal wymienia dziesięć lokali jako dostępne, a plik cennika jedenaście. Ta strona pokazuje dziesięć z portalu i pomija penthouse 9 w bloku 8, który plik wycenia na {E590000}. Cennik podaje, że ceny należy powiększyć o {P7} ITP i że dostępność wymaga potwierdzenia, oraz przypisuje każdemu lokalowi jedno miejsce parkingowe i jedną komórkę lokatorską. Powierzchnia wewnętrzna w cenniku jest bliska powierzchni zabudowy z rzutów, więc oba źródła się różnią. Rzuty z 28 lutego 2023 r. podają dla lokali na parterze {N86.45} {U} powierzchni użytkowej, {N104.20} {U} powierzchni zabudowy i {N51.95} {U} tarasów; dla lokali na pierwszym piętrze {N93.17}, {N113.13} i {N39.14}; dla penthouse’u w bloku 5 {N83.11}, {N105.94} i {N65.05}; a dla penthouse’ów w bloku 10 {N85.77}, {N115.09} i {N63.45}. Rzut jest dołączany tylko wtedy, gdy jego arkusz odpowiada typowi i piętru lokalu, dlatego lokal 8-0-3 na parterze go nie ma.",
  "Priser, arealer og terrasser er skrevet av fra utbyggerens prisliste slik vi leser den i oktober 2026; filen har ingen dato. Portalen oppfører ti boliger som tilgjengelige og prislistefilen elleve. Denne siden viser de ti fra portalen og utelater toppleilighet 9 i hus 8, som filen setter til {E590000}. Listen sier at prisene må økes med {P7} ITP og at tilgjengelighet er med forbehold om bekreftelse, og gir hver bolig én parkeringsplass og én bod. Det innvendige arealet i prislisten ligger nær det bebygde arealet på plantegningene, så de to kildene avviker. Plantegningene, datert 28. februar 2023, oppgir for boligene i første etasje {N86.45} {U} nyttbart areal, {N104.20} {U} bebygd areal og {N51.95} {U} terrasser; for boligene i andre etasje {N93.17}, {N113.13} og {N39.14}; for toppleiligheten i hus 5 {N83.11}, {N105.94} og {N65.05}; og for toppleilighetene i hus 10 {N85.77}, {N115.09} og {N63.45}. En plantegning legges bare ved når arket passer til boligens type og etasje, så bolig 8-0-3 i første etasje har ingen.",
  "Priser, ytor och terrasser är avskrivna från exploatörens prislista så som vi läser den i oktober 2026; filen saknar datum. Portalen listar tio bostäder som tillgängliga och prislistefilen elva. Den här sidan visar de tio från portalen och utelämnar takvåning 9 i hus 8, som filen prissätter till {E590000}. Listan säger att priserna ska ökas med {P7} ITP och att tillgängligheten är under förbehåll för bekräftelse, och ger varje bostad en parkeringsplats och ett förråd. Den invändiga ytan i prislistan ligger nära byggytan på planritningarna, så de två källorna skiljer sig åt. Planritningarna, daterade den 28 februari 2023, anger för bostäderna på bottenvåningen {N86.45} {U} boyta, {N104.20} {U} byggyta och {N51.95} {U} terrasser; för bostäderna på första våningen {N93.17}, {N113.13} och {N39.14}; för takvåningen i hus 5 {N83.11}, {N105.94} och {N65.05}; och för takvåningarna i hus 10 {N85.77}, {N115.09} och {N63.45}. En planritning bifogas bara när dess blad motsvarar bostadens typ och våning, så bostad 8-0-3 på bottenvåningen har ingen.")
# unit references are identifiers and stay as printed; the size row reuses the words the sibling overlays settled on
SIZE = {
    'es': '{b} m² construidos, {i} m² interiores, {t} m² de terraza', 'fr': '{b} m² construits, {i} m² intérieurs, {t} m² de terrasse',
    'de': '{b} m² bebaut, {i} m² Innenfläche, {t} m² Terrasse', 'ru': '{b} м² застроенной площади, {i} м² внутри, терраса {t} м²',
    'ar': '{b} م² مبنية، {i} م² داخلية، {t} م² تراس', 'nl': '{b} m² bebouwd, {i} m² binnen, {t} m² terras',
    'pl': '{b} m² zabudowy, {i} m² wnętrza, {t} m² tarasu', 'no': '{b} m² bygd, {i} m² innvendig, {t} m² terrasse',
    'sv': '{b} m² byggyta, {i} m² inomhus, {t} m² terrass'}
for en in todo:
    if re.fullmatch(r'Home [\d]+-(?:\d|AT)-\d+', en):
        same(en)
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm interior, ([\d.]+) sqm terrace', en)
    if m:
        T[en] = {l: SIZE[l].format(b=num(m.group(1), l), i=num(m.group(2), l), t=num(m.group(3), l)) for l in LOCS}

# ---------------------------------------------------------------- next steps, viewing, enquiry, FAQ
a('See this alongside the other Nueva Andalucía projects we hold.',
  "Véalo junto a los demás proyectos de Nueva Andalucía que tenemos.", "Voyez-le à côté des autres projets de Nueva Andalucía que nous proposons.", "Sehen Sie es neben den anderen Projekten in Nueva Andalucía, die wir betreuen.",
  "Посмотрите его рядом с другими проектами в Нуэва-Андалусии, которые у нас есть.", "شاهده إلى جانب مشاريع نويفا أندلوثيا الأخرى التي نعرضها.", "Zie het naast de andere projecten in Nueva Andalucía die wij aanbieden.",
  "Zobacz go obok innych projektów w Nueva Andalucía, które mamy w ofercie.", "Se det ved siden av de andre prosjektene i Nueva Andalucía vi har.", "Se det vid sidan av de andra projekten i Nueva Andalucía som vi har.")
a('See the homes, the terraces and the shared grounds with us.',
  "Vea las viviendas, las terrazas y las zonas comunes con nosotros.", "Visitez les logements, les terrasses et les espaces communs avec nous.", "Sehen Sie sich mit uns die Wohnungen, die Terrassen und die Gemeinschaftsflächen an.",
  "Осмотрите вместе с нами квартиры, террасы и общую территорию.", "شاهد المساكن والتراسات والمساحات المشتركة معنا.", "Bekijk de woningen, de terrassen en de gemeenschappelijke terreinen met ons.",
  "Wspólnie oglądamy lokale, tarasy i tereny wspólne.", "Se boligene, terrassene og fellesarealene sammen med oss.", "Se bostäderna, terrasserna och de gemensamma ytorna med oss.")
a('We confirm the reservation terms in writing, then the private purchase contract',
  "Confirmamos por escrito las condiciones de la reserva, luego el contrato privado de compraventa con {E4900}, y la escritura.",
  "Nous confirmons par écrit les conditions de réservation, puis le contrat de vente privé avec {E4900}, et l’acte.",
  "Wir bestätigen die Reservierungsbedingungen schriftlich, dann folgen der private Kaufvertrag mit {E4900} und die Kaufurkunde.",
  "Мы письменно подтверждаем условия бронирования, затем предварительный договор купли-продажи с платежом {E4900} и нотариальный акт.",
  "نؤكد كتابةً شروط الحجز، ثم عقد الشراء الخاص مع دفع {E4900}، ثم سند الملكية.",
  "Wij bevestigen de reserveringsvoorwaarden schriftelijk, daarna volgen de onderhandse koopovereenkomst met {E4900} en de eigendomsakte.",
  "Potwierdzamy na piśmie warunki rezerwacji, następnie umowa przedwstępna z kwotą {E4900} i akt notarialny.",
  "Vi bekrefter reservasjonsvilkårene skriftlig, deretter den private kjøpekontrakten med {E4900}, og skjøtet.",
  "Vi bekräftar reservationsvillkoren skriftligen, därefter det privata köpeavtalet med {E4900}, och köpehandlingen.")
a('The complex is built, so a visit is about',
  "El complejo está construido, así que la visita trata de las terrazas, las vistas y las zonas comunes.", "La résidence est construite : la visite porte donc sur les terrasses, les vues et les espaces communs.",
  "Die Anlage ist gebaut, bei einem Besuch geht es also um die Terrassen, die Aussicht und die Gemeinschaftsflächen.", "Комплекс построен, поэтому осмотр — это террасы, виды и общая территория.",
  "المجمع مبني، فالزيارة تدور حول التراسات والإطلالات والمساحات المشتركة.", "Het complex is gebouwd, dus een bezoek gaat over de terrassen, het uitzicht en de gemeenschappelijke terreinen.",
  "Kompleks jest zbudowany, więc wizyta dotyczy tarasów, widoków i terenów wspólnych.", "Anlegget er bygget, så et besøk handler om terrassene, utsikten og fellesarealene.",
  "Området är byggt, så ett besök handlar om terrasserna, utsikten och de gemensamma ytorna.")
a('Walk the terrace of the home you are considering',
  "Recorra la terraza de la vivienda que le interesa y vea las piscinas, el gimnasio y los jardines.", "Parcourez la terrasse du logement qui vous intéresse et visitez les piscines, la salle de sport et les jardins.",
  "Gehen Sie über die Terrasse der Wohnung, die Sie erwägen, und sehen Sie sich die Pools, den Fitnessraum und die Gärten an.", "Пройдитесь по террасе рассматриваемой квартиры и осмотрите бассейны, тренажёрный зал и сады.",
  "تجولوا على تراس المسكن الذي تفكرون فيه وشاهدوا المسابح والصالة الرياضية والحدائق.", "Loop over het terras van de woning die u overweegt en bekijk de zwembaden, de gym en de tuinen.",
  "Przejdziemy po tarasie lokalu, który Państwo rozważają, i zobaczymy baseny, siłownię i ogrody.", "Gå over terrassen til boligen du vurderer, og se bassengene, treningsrommet og hagene.",
  "Gå ut på terrassen i bostaden ni överväger och se poolerna, gymmet och trädgårdarna.")
a('We drive to Puerto Banús, the beaches and the golf with you',
  "Vamos en coche con usted a Puerto Banús, las playas y el golf, y lo cronometramos.", "Nous roulons avec vous jusqu’à Puerto Banús, aux plages et au golf, et nous chronométrons le trajet.",
  "Wir fahren mit Ihnen nach Puerto Banús, zu den Stränden und zum Golf und messen die Zeit.", "Мы вместе с вами едем до Пуэрто-Бануса, пляжей и гольфа и засекаем время.",
  "نقود معكم إلى بويرتو بانوس والشواطئ والغولف ونحتسب الوقت.", "Wij rijden met u naar Puerto Banús, de stranden en de golf en nemen de tijd op.",
  "Jedziemy z Państwem do Puerto Banús, na plaże i na golfa i mierzymy czas.", "Vi kjører med deg til Puerto Banús, strendene og golfbanene og tar tiden.",
  "Vi kör med er till Puerto Banús, stränderna och golfen och tar tid.")
a('Licence of first occupation, energy certificate, the tax and the deed',
  "Licencia de primera ocupación, certificado energético, el impuesto y la escritura, antes de firmar nada.", "Licence de première occupation, certificat énergétique, taxe et acte, avant toute signature.",
  "Erstbezugsgenehmigung, Energieausweis, Steuer und Kaufurkunde, bevor etwas unterschrieben wird.", "Лицензия на первое заселение, энергетический сертификат, налог и нотариальный акт — до подписания любых бумаг.",
  "رخصة الإشغال الأول وشهادة الطاقة والضريبة وسند الملكية، قبل توقيع أي شيء.", "Vergunning voor eerste ingebruikname, energiecertificaat, de belasting en de eigendomsakte, voordat er iets wordt ondertekend.",
  "Pozwolenie na pierwsze zajęcie, świadectwo energetyczne, podatek i akt notarialny, zanim cokolwiek zostanie podpisane.", "Brukstillatelse, energiattest, skatten og skjøtet, før noe signeres.",
  "Slutbesked, energideklaration, skatten och köpehandlingen, innan något undertecknas.")
# the enquiry block is the same sentence in every project, with only the name changed
_sot = json.load(open('content/liora-projects/sotavento-residences/project.json'))
for key in ('headlineHtml', 'message'):
    en = f"Ask about <em>Acacia Residences</em>" if key == 'headlineHtml' else 'Hello Nueva Living, I would like information about Acacia Residences.'
    if en in todo:
        T[en] = {l: _sot['i18n'][l]['enquiry'][key].replace('Sotavento Residences', 'Acacia Residences') for l in LOCS}
a('Ten two-bedroom homes are listed on the developer’s portal',
  "El portal del promotor lista diez viviendas de dos dormitorios: tres en planta baja, cuatro en primera planta y tres áticos dúplex, de {E470000} a {E600000} más el {P7} de ITP. El folleto cuenta 70 viviendas en el complejo.",
  "Le portail du promoteur liste dix logements de deux chambres : trois au rez-de-chaussée, quatre au premier étage et trois penthouses duplex, de {E470000} à {E600000} plus {P7} d’ITP. La brochure compte 70 logements dans la résidence.",
  "Das Portal des Bauträgers führt zehn Wohnungen mit zwei Schlafzimmern: drei im Erdgeschoss, vier im ersten Obergeschoss und drei Maisonette-Penthäuser, von {E470000} bis {E600000} zuzüglich {P7} ITP. Die Broschüre zählt 70 Wohnungen in der Anlage.",
  "На портале застройщика указаны десять квартир с двумя спальнями: три на первом этаже, четыре на втором и три двухуровневых пентхауса, от {E470000} до {E600000} плюс {P7} ITP. В брошюре в комплексе насчитывается 70 квартир.",
  "تدرج بوابة المطوّر عشرة مساكن من غرفتي نوم: ثلاثة في الطابق الأرضي وأربعة في الطابق الأول وثلاثة بنتهاوس دوبلكس، من {E470000} إلى {E600000} زائد {P7} ضريبة ITP. ويحصي الكتيّب 70 مسكنًا في المجمع.",
  "Het portaal van de ontwikkelaar vermeldt tien woningen met twee slaapkamers: drie op de begane grond, vier op de eerste verdieping en drie duplexpenthouses, van {E470000} tot {E600000} plus {P7} ITP. De brochure telt 70 woningen in het complex.",
  "Portal dewelopera podaje dziesięć lokali z dwiema sypialniami: trzy na parterze, cztery na pierwszym piętrze i trzy dwupoziomowe penthouse’y, od {E470000} do {E600000} plus {P7} ITP. Broszura wymienia w kompleksie 70 lokali.",
  "Utbyggerens portal oppfører ti boliger med to soverom: tre i første etasje, fire i andre etasje og tre toppleiligheter i to plan, fra {E470000} til {E600000} pluss {P7} ITP. Brosjyren teller 70 boliger i anlegget.",
  "Exploatörens portal listar tio bostäder med två sovrum: tre på bottenvåningen, fyra på första våningen och tre takvåningar i två plan, från {E470000} till {E600000} plus {P7} ITP. Broschyren räknar 70 bostäder i området.")
a('No tax is included.',
  "No se incluye ningún impuesto. La lista de precios no menciona el IVA y dice que los precios deben incrementarse con el {P7} de ITP. Confirmamos por escrito el impuesto y los gastos de compra.",
  "Aucune taxe n’est incluse. La liste de prix ne mentionne pas la TVA et indique que les prix doivent être majorés de {P7} d’ITP. Nous confirmons par écrit la taxe et les frais d’achat.",
  "Keine Steuer ist enthalten. Die Preisliste erwähnt keine MwSt. und gibt an, dass auf die Preise {P7} ITP aufzuschlagen sind. Wir bestätigen Steuer und Kaufnebenkosten schriftlich.",
  "Налоги не включены. В прайс-листе НДС не упомянут, а сказано, что к ценам нужно прибавить {P7} ITP. Мы письменно подтверждаем налог и расходы на покупку.",
  "لا تشمل الأسعار أي ضريبة. لا تذكر قائمة الأسعار ضريبة القيمة المضافة، وتذكر أنه يجب زيادة الأسعار بنسبة {P7} ضريبة ITP. نؤكد الضريبة ومصاريف الشراء كتابةً.",
  "Er is geen belasting inbegrepen. De prijslijst noemt geen btw en zegt dat de prijzen met {P7} ITP moeten worden verhoogd. Wij bevestigen de belasting en de aankoopkosten schriftelijk.",
  "Żaden podatek nie jest wliczony. Cennik nie wspomina o VAT i podaje, że ceny należy powiększyć o {P7} ITP. Potwierdzamy na piśmie podatek i koszty zakupu.",
  "Ingen skatter er inkludert. Prislisten nevner ikke mva. og sier at prisene må økes med {P7} ITP. Vi bekrefter skatten og kjøpskostnadene skriftlig.",
  "Inga skatter ingår. Prislistan nämner inte moms och säger att priserna ska ökas med {P7} ITP. Vi bekräftar skatten och köpkostnaderna skriftligen.")
a('Is the building finished?',
  "¿Está terminado el edificio?", "L’immeuble est-il achevé ?", "Ist das Gebäude fertiggestellt?", "Завершено ли здание?", "هل المبنى مكتمل؟", "Is het gebouw opgeleverd?", "Czy budynek jest ukończony?", "Er bygningen ferdig?", "Är byggnaden färdig?")
a('The portal lists it as a finished building',
  "El portal lo lista como edificio terminado y las fotografías lo muestran construido. Los documentos no dan fecha de finalización, así que pedimos la licencia de primera ocupación.",
  "Le portail le présente comme un immeuble achevé et les photographies le montrent construit. Les documents ne donnent aucune date d’achèvement ; nous demandons donc la licence de première occupation.",
  "Das Portal führt es als fertiggestelltes Gebäude, und die Fotos zeigen es gebaut. Die Unterlagen nennen keinen Fertigstellungstermin, deshalb verlangen wir die Erstbezugsgenehmigung.",
  "Портал указывает его как завершённое здание, а на фотографиях оно построено. В документах нет даты завершения, поэтому мы запрашиваем лицензию на первое заселение.",
  "تدرجه البوابة بوصفه مبنى مكتملًا، وتُظهره الصور مبنيًا. لا تذكر الوثائق تاريخًا للإتمام، لذلك نطلب رخصة الإشغال الأول.",
  "Het portaal vermeldt het als een opgeleverd gebouw en de foto’s tonen het gebouwd. De documenten noemen geen opleveringsdatum, daarom vragen wij de vergunning voor eerste ingebruikname.",
  "Portal podaje go jako budynek ukończony, a zdjęcia pokazują go jako zbudowany. Dokumenty nie podają terminu ukończenia, dlatego prosimy o pozwolenie na pierwsze zajęcie.",
  "Portalen fører den som en ferdig bygning, og bildene viser den bygget. Dokumentene oppgir ingen ferdigstillelsesdato, så vi ber om brukstillatelsen.",
  "Portalen anger den som en färdig byggnad, och bilderna visar den byggd. Dokumenten anger inget färdigställandedatum, så vi ber om slutbesked.")
a('Is there parking and storage?',
  "¿Hay aparcamiento y trastero?", "Y a-t-il un stationnement et un débarras ?", "Gibt es Stellplatz und Abstellraum?", "Есть ли парковка и кладовая?", "هل يوجد موقف سيارات ومخزن؟", "Is er parkeergelegenheid en een berging?", "Czy jest parking i komórka lokatorska?", "Er det parkering og bod?", "Finns det parkering och förråd?")
a('Yes. The price list gives each home one parking space',
  "Sí. La lista de precios asigna a cada vivienda una plaza de aparcamiento y un trastero, y el folleto dice que el aparcamiento es subterráneo.",
  "Oui. La liste de prix attribue à chaque logement une place de stationnement et un débarras, et la brochure précise que le stationnement est en sous-sol.",
  "Ja. Die Preisliste ordnet jeder Wohnung einen Stellplatz und einen Abstellraum zu, und laut Broschüre liegt der Stellplatz in der Tiefgarage.",
  "Да. В прайс-листе за каждой квартирой закреплены одно парковочное место и одна кладовая, а в брошюре сказано, что парковка подземная.",
  "نعم. تمنح قائمة الأسعار كل مسكن موقف سيارات واحدًا ومخزنًا واحدًا، ويذكر الكتيّب أن الموقف تحت الأرض.",
  "Ja. De prijslijst kent elke woning één parkeerplaats en één berging toe, en de brochure zegt dat de parkeerplaats ondergronds is.",
  "Tak. Cennik przypisuje każdemu lokalowi jedno miejsce parkingowe i jedną komórkę lokatorską, a broszura podaje, że parking jest podziemny.",
  "Ja. Prislisten gir hver bolig én parkeringsplass og én bod, og brosjyren sier at parkeringen er under bakken.",
  "Ja. Prislistan ger varje bostad en parkeringsplats och ett förråd, och broschyren säger att parkeringen är under jord.")
a('Two pools and a solarium, a gym, a wellness area',
  "Dos piscinas y un solárium, un gimnasio, una zona de bienestar y un área gastronómica en jardines cuidados, con seguridad las 24 horas, según el folleto.",
  "Deux piscines et un solarium, une salle de sport, un espace bien-être et un espace gastronomique dans des jardins paysagers, avec sécurité 24 heures sur 24, d’après la brochure.",
  "Zwei Pools und ein Solarium, ein Fitnessraum, ein Wellnessbereich und ein gastronomischer Bereich in gepflegten Gärten, mit 24-Stunden-Sicherheitsdienst, laut Broschüre.",
  "Два бассейна и солярий, тренажёрный зал, велнес-зона и гастрономическая зона в благоустроенных садах, круглосуточная охрана — по данным брошюры.",
  "مسبحان وسولاريوم وصالة رياضية ومنطقة للعافية ومنطقة للطعام في حدائق منسّقة، مع حراسة على مدار الساعة، وفق الكتيّب.",
  "Twee zwembaden en een solarium, een gym, een wellnessruimte en een gastronomische zone in verzorgde tuinen, met bewaking de klok rond, volgens de brochure.",
  "Dwa baseny i solarium, siłownia, strefa wellness i strefa gastronomiczna w zadbanych ogrodach, z całodobową ochroną, według broszury.",
  "To bassenger og en solterrasse, et treningsrom, et velværeområde og et gastronomisk område i opparbeidede hager, med sikkerhet døgnet rundt, ifølge brosjyren.",
  "Två pooler och en solterrass, ett gym, en wellnessavdelning och ett gastronomiskt område i anlagda trädgårdar, med säkerhet dygnet runt, enligt broschyren.")
if 'What is there on site?' in todo:
  a('What is there on site?',
  "¿Qué hay en el complejo?", "Qu’y a-t-il sur place ?", "Was gibt es in der Anlage?", "Что есть на территории?", "ما المتوفر في المجمع؟", "Wat is er in het complex?", "Co znajduje się na terenie kompleksu?", "Hva finnes i anlegget?", "Vad finns i området?")

out = f'{SP}/tr_a.json'
json.dump(T, open(out, 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries;', 'still unmatched todo:', len([t for t in todo if t not in T]))
for t in todo:
    if t not in T:
        print('  OPEN', t[:100])
