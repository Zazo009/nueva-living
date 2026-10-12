# -*- coding: utf-8 -*-
"""Brisamar Residences: the 166 strings the translation memory did not have.

Same shape as k_selwo.py and k_higueron.py. Floorplan captions, unit sizes and unit references are
templates; the prose is written by hand. Tokens:  {E549000}  {N77.32}  {U} (m2).
Run:  python3 tools/import/k_brisamar.py <scratch dir>     (writes <scratch dir>/tr_a.json)
"""
import json, re, sys
SP = sys.argv[1]
LOCS = ['es', 'fr', 'de', 'ru', 'ar', 'nl', 'pl', 'no', 'sv']
todo = list(json.load(open(f'{SP}/todo.json')))
GROUP = {'es': '.', 'fr': ' ', 'de': '.', 'ru': ' ', 'ar': ',', 'nl': '.', 'pl': ' ', 'no': ' ', 'sv': ' '}
UNIT = {'es': 'm²', 'fr': 'm²', 'de': 'm²', 'ru': 'м²', 'ar': 'م²', 'nl': 'm²', 'pl': 'm²', 'no': 'm²', 'sv': 'm²'}
T = {}


def money(n, l):
    body = f'{n:,}'.replace(',', GROUP[l])
    return f'€ {body}' if l == 'nl' else f'{body} €'


def num(s, l):
    return s.replace('.', '.' if l == 'ar' else ',')


def expand(text, l):
    text = re.sub(r'\{E(\d+)\}', lambda m: money(int(m.group(1)), l), text)
    text = re.sub(r'\{N([\d.]+)\}', lambda m: num(m.group(1), l), text)
    return text.replace('{U}', UNIT[l])


def a(i, hint, *tr):
    en = todo[i]
    assert en.startswith(hint), (i, hint, en[:50])
    assert len(tr) == 9, (i, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


def same(i, hint):
    a(i, hint, *([todo[i]] * 9))


# ---------------------------------------------------------------- templates
HOME = {'es': 'Vivienda', 'fr': 'Logement', 'de': 'Wohnung', 'ru': 'Квартира', 'ar': 'المسكن', 'nl': 'Woning',
        'pl': 'Lokal', 'no': 'Bolig', 'sv': 'Bostad'}
PLANOF = {'es': 'Plano de la vivienda', 'fr': 'Plan du logement', 'de': 'Grundriss der Wohnung', 'ru': 'Планировка квартиры',
          'ar': 'مخطط المسكن', 'nl': 'Plattegrond van woning', 'pl': 'Rzut lokalu', 'no': 'Plantegning av bolig',
          'sv': 'Planritning för bostad'}
COMMA = {l: (', ' if l != 'ar' else '، ') for l in LOCS}
# floor parts in phrase position, exactly as the other apartment projects write them
LV = {
    'ground floor': ['planta baja', 'rez-de-chaussée', 'Erdgeschoss', 'первый этаж', 'الطابق الأرضي', 'begane grond', 'parter', 'første etasje', 'bottenvåning'],
    'garden': ['jardín', 'jardin', 'Garten', 'сад', 'حديقة', 'tuin', 'ogród', 'hage', 'trädgård'],
    'first floor': ['primera planta', 'premier étage', 'erstes Obergeschoss', 'второй этаж', 'الطابق الأول', 'eerste verdieping', 'pierwsze piętro', 'andre etasje', 'första våningen'],
    'second floor': ['segunda planta', 'deuxième étage', 'zweites Obergeschoss', 'третий этаж', 'الطابق الثاني', 'tweede verdieping', 'drugie piętro', 'tredje etasje', 'andra våningen'],
    'third floor': ['tercera planta', 'troisième étage', 'drittes Obergeschoss', 'четвёртый этаж', 'الطابق الثالث', 'derde verdieping', 'trzecie piętro', 'fjerde etasje', 'tredje våningen'],
    'fourth floor': ['cuarta planta', 'quatrième étage', 'viertes Obergeschoss', 'пятый этаж', 'الطابق الرابع', 'vierde verdieping', 'czwarte piętro', 'femte etasje', 'fjärde våningen'],
    'solarium': ['solárium', 'solarium', 'Solarium', 'солярий', 'سولاريوم', 'solarium', 'solarium', 'solterrasse', 'solterrass'],
    'penthouse': ['ático', 'penthouse', 'Penthouse', 'пентхаус', 'بنتهاوس', 'penthouse', 'penthouse', 'toppleilighet', 'takvåning'],
}
SIZE = {   # built, terrace, then garden / solarium -- the wording the other apartment and villa projects use
    'es': ('{b} {U} construidos', '{t} {U} de terraza', {'garden': '{x} {U} de jardín', 'solarium': '{x} {U} de solárium'}),
    'fr': ('{b} {U} construits', '{t} {U} de terrasse', {'garden': '{x} {U} de jardin', 'solarium': '{x} {U} de solarium'}),
    'de': ('{b} {U} bebaut', '{t} {U} Terrasse', {'garden': '{x} {U} Garten', 'solarium': '{x} {U} Solarium'}),
    'ru': ('{b} {U} застроенной площади', 'терраса {t} {U}', {'garden': 'сад {x} {U}', 'solarium': 'солярий {x} {U}'}),
    'ar': ('{b} {U} مبنية', '{t} {U} تراس', {'garden': '{x} {U} حديقة', 'solarium': '{x} {U} سولاريوم'}),
    'nl': ('{b} {U} bebouwd', '{t} {U} terras', {'garden': '{x} {U} tuin', 'solarium': '{x} {U} solarium'}),
    'pl': ('{b} {U} zabudowy', '{t} {U} tarasu', {'garden': '{x} {U} ogrodu', 'solarium': '{x} {U} solarium'}),
    'no': ('{b} {U} bygd', '{t} {U} terrasse', {'garden': '{x} {U} hage', 'solarium': '{x} {U} solterrasse'}),
    'sv': ('{b} {U} byggyta', '{t} {U} terrass', {'garden': '{x} {U} trädgård', 'solarium': '{x} {U} solterrass'}),
}
for en in todo:
    m = re.fullmatch(r'(\d\.?\d*[A-Z]?)', en)
    if re.fullmatch(r'\d[A-D]', en):
        T[en] = {l: en for l in LOCS}
        continue
    m = re.fullmatch(r'Floorplan of home (\d[A-D]), (.+)', en)
    if m:
        T[en] = {l: f'{PLANOF[l]} {m.group(1)}{COMMA[l]}{LV[m.group(2)][i]}' for i, l in enumerate(LOCS)}
        continue
    m = re.fullmatch(r'Home (\d[A-D]), (.+)', en)
    if m:
        T[en] = {l: f'{HOME[l]} {m.group(1)}{COMMA[l]}{LV[m.group(2)][i]}' for i, l in enumerate(LOCS)}
        continue
    m = re.fullmatch(r'([\d.]+) sqm built, ([\d.]+) sqm terrace(?:, ([\d.]+) sqm (garden|solarium))?', en)
    if m:
        out = {}
        for l in LOCS:
            b, t, extra = SIZE[l]
            parts = [b.format(b='{N%s}' % m.group(1), U='{U}'), t.format(t='{N%s}' % m.group(2), U='{U}')]
            if m.group(3):
                parts.append(extra[m.group(4)].format(x='{N%s}' % m.group(3), U='{U}'))
            out[l] = expand((COMMA[l]).join(parts), l)
        T[en] = out

# ---------------------------------------------------------------- names, card, hero
same(0, 'Brisamar Residences')
same(1, 'Brisamar')
same(2, 'Brisamar <em>')
a(3, '22 three-bedroom homes in one building',
  '22 viviendas de tres dormitorios en un solo edificio cerca del centro de Estepona: cuatro viviendas en planta baja con jardín y piscina privados, terrazas en todas las plantas superiores y viviendas con solárium y piscina privados en la cubierta. Nueve figuran con precio, desde {E549000}.',
  '22 logements de trois chambres dans un seul immeuble près du centre d’Estepona : quatre logements en rez-de-chaussée avec jardin et piscine privés, des terrasses à chaque étage et des logements avec solarium et piscine privés sur le toit. Neuf sont listés, à partir de {E549000}.',
  '22 Wohnungen mit drei Schlafzimmern in einem Gebäude nahe dem Zentrum von Estepona: vier Erdgeschosswohnungen mit privatem Garten und Pool, Terrassen auf jeder Obergeschossebene und Wohnungen mit privatem Dachsolarium und Pool. Neun sind aufgeführt, ab {E549000}.',
  '22 квартиры с тремя спальнями в одном здании недалеко от центра Эстепоны: четыре квартиры на первом этаже с частным садом и бассейном, террасы на каждом верхнем этаже и квартиры с частным солярием и бассейном на крыше. В списке девять, от {E549000}.',
  '22 مسكناً بثلاث غرف نوم في مبنى واحد قرب وسط إستيبونا: أربعة مساكن في الطابق الأرضي بحديقة ومسبح خاصين، وتراسات في كل طابق علوي، ومساكن بسولاريوم ومسبح خاصين على السطح. تسعة منها مدرجة بالأسعار، ابتداءً من {E549000}.',
  '22 woningen met drie slaapkamers in één gebouw nabij het centrum van Estepona: vier woningen op de begane grond met privétuin en privézwembad, terrassen op elke bovenverdieping en woningen met een privésolarium en zwembad op het dak. Negen staan op de lijst, vanaf {E549000}.',
  '22 lokale z trzema sypialniami w jednym budynku w pobliżu centrum Estepony: cztery lokale na parterze z prywatnym ogrodem i basenem, tarasy na każdym piętrze oraz lokale z prywatnym solarium i basenem na dachu. Dziewięć jest na liście, od {E549000}.',
  '22 boliger med tre soverom i én bygning nær sentrum av Estepona: fire boliger i første etasje med privat hage og basseng, terrasser i alle etasjene over og boliger med privat solterrasse og basseng på taket. Ni er oppført, fra {E549000}.',
  '22 bostäder med tre sovrum i en byggnad nära centrala Estepona: fyra bostäder på bottenvåningen med privat trädgård och pool, terrasser på varje våning ovanför och bostäder med privat solterrass och pool på taket. Nio är listade, från {E549000}.')
a(4, 'Nine of 22 three-bedroom homes listed',
  'Nueve de 22 viviendas de tres dormitorios, cerca del centro de Estepona, desde {E549000}: jardines y piscinas privadas en planta baja, solárium en la cubierta, garaje y trastero incluidos.',
  'Neuf logements de trois chambres sur 22, près du centre d’Estepona, à partir de {E549000} : jardins et piscines privés au rez-de-chaussée, solariums sur le toit, parking et débarras inclus.',
  'Neun von 22 Wohnungen mit drei Schlafzimmern nahe dem Zentrum von Estepona ab {E549000}: Gärten und private Pools im Erdgeschoss, Dachsolarien darüber, Stellplatz und Abstellraum inklusive.',
  'Девять из 22 квартир с тремя спальнями недалеко от центра Эстепоны, от {E549000}: сады и частные бассейны на первом этаже, солярии на крыше, парковка и кладовая включены.',
  'تسعة من 22 مسكناً بثلاث غرف نوم قرب وسط إستيبونا، ابتداءً من {E549000}: حدائق ومسابح خاصة في الطابق الأرضي، وسولاريوم على السطح، والموقف والمخزن مشمولان.',
  'Negen van de 22 woningen met drie slaapkamers nabij het centrum van Estepona, vanaf {E549000}: tuinen en privézwembaden op de begane grond, solariums op het dak, parkeerplaats en berging inbegrepen.',
  'Dziewięć z 22 lokali z trzema sypialniami w pobliżu centrum Estepony, od {E549000}: ogrody i prywatne baseny na parterze, solaria na dachu, miejsce parkingowe i komórka w cenie.',
  'Ni av 22 boliger med tre soverom nær sentrum av Estepona, fra {E549000}: hager og private basseng i første etasje, solterrasser på taket, parkeringsplass og bod inkludert.',
  'Nio av 22 bostäder med tre sovrum nära centrala Estepona, från {E549000}: trädgårdar och privata pooler på bottenvåningen, solterrasser på taket, parkeringsplats och förråd ingår.')
a(5, 'Three-bedroom homes near the centre',
  'Viviendas de tres dormitorios cerca del centro de Estepona, con jardines, terrazas y solárium en la cubierta, desde {E549000}.',
  'Logements de trois chambres près du centre d’Estepona, avec jardins, terrasses et solariums sur le toit, à partir de {E549000}.',
  'Wohnungen mit drei Schlafzimmern nahe dem Zentrum von Estepona, mit Gärten, Terrassen und Dachsolarien, ab {E549000}.',
  'Квартиры с тремя спальнями недалеко от центра Эстепоны, с садами, террасами и солярием на крыше, от {E549000}.',
  'مساكن بثلاث غرف نوم قرب وسط إستيبونا، بحدائق وتراسات وسولاريوم على السطح، ابتداءً من {E549000}.',
  'Woningen met drie slaapkamers nabij het centrum van Estepona, met tuinen, terrassen en solariums op het dak, vanaf {E549000}.',
  'Lokale z trzema sypialniami w pobliżu centrum Estepony, z ogrodami, tarasami i solariami na dachu, od {E549000}.',
  'Boliger med tre soverom nær sentrum av Estepona, med hager, terrasser og solterrasser på taket, fra {E549000}.',
  'Bostäder med tre sovrum nära centrala Estepona, med trädgårdar, terrasser och solterrasser på taket, från {E549000}.')
a(6, '22 three-bedroom homes in one building',
  '22 viviendas de tres dormitorios en un edificio cerca del centro de Estepona, con jardines y piscinas privadas en planta baja y solárium en la cubierta.',
  '22 logements de trois chambres dans un immeuble près du centre d’Estepona, avec jardins et piscines privés au rez-de-chaussée et solariums sur le toit.',
  '22 Wohnungen mit drei Schlafzimmern in einem Gebäude nahe dem Zentrum von Estepona, mit Gärten und privaten Pools im Erdgeschoss und Solarien auf dem Dach.',
  '22 квартиры с тремя спальнями в одном здании недалеко от центра Эстепоны, с садами и частными бассейнами на первом этаже и солярием на крыше.',
  '22 مسكناً بثلاث غرف نوم في مبنى واحد قرب وسط إستيبونا، بحدائق ومسابح خاصة في الطابق الأرضي وسولاريوم على السطح.',
  '22 woningen met drie slaapkamers in één gebouw nabij het centrum van Estepona, met tuinen en privézwembaden op de begane grond en solariums op het dak.',
  '22 lokale z trzema sypialniami w jednym budynku w pobliżu centrum Estepony, z ogrodami i prywatnymi basenami na parterze oraz solariami na dachu.',
  '22 boliger med tre soverom i én bygning nær sentrum av Estepona, med hager og private basseng i første etasje og solterrasser på taket.',
  '22 bostäder med tre sovrum i en byggnad nära centrala Estepona, med trädgårdar och privata pooler på bottenvåningen och solterrasser på taket.')
a(7, 'Terrace and solarium', 'Terraza y solárium', 'Terrasse et solarium', 'Terrasse und Solarium', 'Терраса и солярий',
  'التراس والسولاريوم', 'Terras en solarium', 'Taras i solarium', 'Terrasse og solterrasse', 'Terrass och solterrass')
am = json.load(open('content/i18n/amenities.json'))
assert todo[8].startswith('Parking space and storage room included')
T[todo[8]] = {l: am[todo[8]][l] for l in LOCS}

# ---------------------------------------------------------------- image alts and captions
a(9, 'Computer-generated view of a building on a street corner',
  'Vista generada por ordenador de un edificio en una esquina, con losas de balcón blancas y curvas, terrazas con plantas y una pérgola en la cubierta',
  'Vue générée par ordinateur d’un immeuble en angle de rue, avec des dalles de balcon blanches et courbes, des terrasses plantées et une pergola sur le toit',
  'Computergenerierte Ansicht eines Gebäudes an einer Straßenecke mit geschwungenen weißen Balkonplatten, bepflanzten Terrassen und einer Pergola auf dem Dach',
  'Компьютерная визуализация здания на углу улицы с изогнутыми белыми плитами балконов, озеленёнными террасами и перголой на крыше',
  'منظر مولَّد بالحاسوب لمبنى على ناصية شارع بألواح شرفات بيضاء منحنية وتراسات مزروعة وبرغولا على السطح',
  'Computergegenereerd beeld van een gebouw op een straathoek met gebogen witte balkonplaten, beplante terrassen en een pergola op het dak',
  'Wygenerowany komputerowo widok budynku na rogu ulicy z zaokrąglonymi białymi płytami balkonowymi, obsadzonymi roślinami tarasami i pergolą na dachu',
  'Datagenerert bilde av en bygning på et gatehjørne med buede hvite balkongplater, beplantede terrasser og en pergola på taket',
  'Datorgenererad vy av en byggnad på ett gathörn med välvda vita balkongplattor, planterade terrasser och en pergola på taket')
a(10, 'Computer-generated aerial view of the building beside a roundabout',
  'Vista aérea generada por ordenador del edificio junto a una rotonda, con la ciudad de Estepona y el mar al fondo',
  'Vue aérienne générée par ordinateur de l’immeuble à côté d’un rond-point, avec la ville d’Estepona et la mer à l’arrière-plan',
  'Computergenerierte Luftansicht des Gebäudes neben einem Kreisverkehr, dahinter die Stadt Estepona und das Meer',
  'Компьютерная визуализация здания с высоты птичьего полёта рядом с кольцевой развязкой; позади город Эстепона и море',
  'منظر جوي مولَّد بالحاسوب للمبنى بجانب دوّار، وخلفه مدينة إستيبونا والبحر',
  'Computergegenereerd luchtbeeld van het gebouw naast een rotonde, met de stad Estepona en de zee erachter',
  'Wygenerowany komputerowo widok z lotu ptaka na budynek obok ronda, a za nim miasto Estepona i morze',
  'Datagenerert flyfoto av bygningen ved siden av en rundkjøring, med byen Estepona og havet bak',
  'Datorgenererad flygvy av byggnaden bredvid en rondell, med staden Estepona och havet bakom')
a(11, 'Computer-generated living room with a television',
  'Salón generado por ordenador con televisor, sillón, sofá y cocina abierta, y puertas correderas al jardín',
  'Séjour généré par ordinateur avec téléviseur, fauteuil, canapé et cuisine ouverte, et baies coulissantes sur le jardin',
  'Computergeneriertes Wohnzimmer mit Fernseher, Sessel, Sofa und offener Küche sowie Schiebetüren zum Garten',
  'Компьютерная визуализация гостиной с телевизором, креслом, диваном и открытой кухней, с раздвижными дверями в сад',
  'غرفة معيشة مولَّدة بالحاسوب فيها تلفاز ومقعد وأريكة ومطبخ مفتوح، وأبواب منزلقة إلى الحديقة',
  'Computergegenereerde woonkamer met een televisie, een fauteuil, een bank en een open keuken, en schuifdeuren naar de tuin',
  'Wygenerowany komputerowo salon z telewizorem, fotelem, sofą i otwartą kuchnią oraz rozsuwanymi drzwiami do ogrodu',
  'Datagenerert stue med TV, lenestol, sofa og åpent kjøkken, og skyvedører til hagen',
  'Datorgenererat vardagsrum med tv, fåtölj, soffa och öppet kök, samt skjutdörrar till trädgården')
a(12, 'Computer-generated bedroom with a double bed',
  'Dormitorio generado por ordenador con cama de matrimonio, pared de listones de madera y puertas correderas de cristal a la terraza',
  'Chambre générée par ordinateur avec lit double, mur à lattes de bois et portes vitrées coulissantes sur la terrasse',
  'Computergeneriertes Schlafzimmer mit Doppelbett, Holzlattenwand und gläsernen Schiebetüren zur Terrasse',
  'Компьютерная визуализация спальни с двуспальной кроватью, стеной из деревянных реек и стеклянными раздвижными дверями на террасу',
  'غرفة نوم مولَّدة بالحاسوب فيها سرير مزدوج وجدار من ألواح خشبية وأبواب زجاجية منزلقة إلى التراس',
  'Computergegenereerde slaapkamer met een tweepersoonsbed, een wand van houten latten en glazen schuifdeuren naar het terras',
  'Wygenerowana komputerowo sypialnia z łóżkiem dwuosobowym, ścianą z drewnianych listew i przesuwnymi szklanymi drzwiami na taras',
  'Datagenerert soverom med dobbeltseng, en vegg av trelister og skyvedører i glass til terrassen',
  'Datorgenererat sovrum med dubbelsäng, en vägg av träläkt och glasskjutdörrar till terrassen')
a(13, 'Computer-generated views of the building and its interiors',
  'Vistas del edificio y de sus interiores generadas por ordenador, y planos de las nueve viviendas de la lista.',
  'Vues générées par ordinateur de l’immeuble et de ses intérieurs, et plans des neuf logements de la liste.',
  'Computergenerierte Ansichten des Gebäudes und seiner Innenräume sowie die Grundrisse der neun aufgeführten Wohnungen.',
  'Компьютерные визуализации здания и интерьеров и планировки девяти квартир из списка.',
  'مناظر مولَّدة بالحاسوب للمبنى وداخله، ومخططات المساكن التسعة المدرجة.',
  'Computergegenereerde beelden van het gebouw en de interieurs, en de plattegronden van de negen woningen op de lijst.',
  'Wygenerowane komputerowo widoki budynku i jego wnętrz oraz rzuty dziewięciu lokali z listy.',
  'Datagenererte bilder av bygningen og interiørene, og plantegninger av de ni boligene på listen.',
  'Datorgenererade vyer av byggnaden och dess interiörer, och planritningar över de nio bostäderna på listan.')
a(14, 'All the images are computer-generated illustrations',
  'Todas las imágenes son ilustraciones generadas por ordenador y no fotografías del edificio terminado, y el mobiliario y la decoración que aparecen son ilustrativos y no están incluidos. Los planos son los del promotor, en fase de proyecto, y las superficies que figuran en ellos son aproximadas y están sujetas al proyecto definitivo. Los nombres de las estancias en los planos están en inglés.',
  'Toutes les images sont des illustrations générées par ordinateur et non des photographies du bâtiment achevé ; le mobilier et la décoration qui y figurent sont illustratifs et ne sont pas inclus. Les plans sont ceux du promoteur au stade du projet, et les surfaces qui y figurent sont approximatives et soumises au projet définitif. Les noms des pièces sur les plans sont en anglais.',
  'Alle Bilder sind computergenerierte Illustrationen und keine Fotos des fertigen Gebäudes; Möblierung und Dekoration darauf sind illustrativ und nicht enthalten. Die Grundrisse sind die Pläne des Bauträgers im Projektstadium, die darin angegebenen Flächen sind ungefähre Werte und vorbehaltlich des endgültigen Projekts. Die Raumbezeichnungen in den Plänen sind auf Englisch.',
  'Все изображения — компьютерные иллюстрации, а не фотографии готового здания; мебель и декор на них носят иллюстративный характер и не входят в стоимость. Планировки — проектные планы застройщика, указанные на них площади приблизительны и зависят от окончательного проекта. Названия помещений на планах даны на английском языке.',
  'جميع الصور رسوم توضيحية مولَّدة بالحاسوب وليست صوراً فوتوغرافية للمبنى بعد اكتماله، والأثاث والديكور الظاهران فيها للتوضيح فقط وغير مشمولين. المخططات هي مخططات المطوّر في مرحلة المشروع، والمساحات الواردة فيها تقريبية وتخضع للمشروع النهائي. أسماء الغرف في المخططات بالإنجليزية.',
  'Alle beelden zijn computergegenereerde illustraties en geen foto’s van het opgeleverde gebouw; het meubilair en de inrichting daarop zijn illustratief en niet inbegrepen. De plattegronden zijn de plannen van de ontwikkelaar in projectfase en de oppervlakten erop zijn bij benadering en onder voorbehoud van het definitieve project. De ruimtenamen op de plattegronden zijn in het Engels.',
  'Wszystkie obrazy to ilustracje wygenerowane komputerowo, a nie zdjęcia ukończonego budynku; meble i wyposażenie na nich mają charakter poglądowy i nie są wliczone. Rzuty to plany dewelopera z etapu projektu, a podane na nich powierzchnie są przybliżone i zależą od ostatecznego projektu. Nazwy pomieszczeń na rzutach są po angielsku.',
  'Alle bildene er datagenererte illustrasjoner og ikke fotografier av den ferdige bygningen, og møblene og dekorasjonen på dem er illustrative og ikke inkludert. Plantegningene er utbyggerens prosjektplaner, og arealene på dem er omtrentlige og med forbehold om det endelige prosjektet. Romnavnene på plantegningene er på engelsk.',
  'Alla bilder är datorgenererade illustrationer och inte fotografier av den färdiga byggnaden, och möblerna och inredningen på dem är illustrativa och ingår inte. Planritningarna är exploatörens projektplaner, och ytorna på dem är ungefärliga och med förbehåll för det slutliga projektet. Rumsnamnen på ritningarna är på engelska.')
a(15, 'The corner of the building', 'La esquina del edificio', 'L’angle de l’immeuble', 'Die Gebäudeecke', 'Угол здания',
  'ناصية المبنى', 'De hoek van het gebouw', 'Narożnik budynku', 'Hjørnet av bygningen', 'Byggnadens hörn')
a(16, 'The building from the air', 'El edificio desde el aire', 'L’immeuble vu du ciel', 'Das Gebäude aus der Luft', 'Здание с высоты птичьего полёта',
  'المبنى من الجو', 'Het gebouw vanuit de lucht', 'Budynek z lotu ptaka', 'Bygningen fra luften', 'Byggnaden från luften')
a(17, 'Computer-generated aerial view of the building lit at dusk',
  'Vista aérea generada por ordenador del edificio iluminado al anochecer, con la ciudad y el mar al fondo',
  'Vue aérienne générée par ordinateur de l’immeuble éclairé au crépuscule, avec la ville et la mer au loin',
  'Computergenerierte Luftansicht des beleuchteten Gebäudes in der Abenddämmerung, dahinter die Stadt und das Meer',
  'Компьютерная визуализация освещённого здания в сумерках с высоты птичьего полёта; вдали город и море',
  'منظر جوي مولَّد بالحاسوب للمبنى مضاءً عند الغسق، وخلفه المدينة والبحر',
  'Computergegenereerd luchtbeeld van het verlichte gebouw bij schemering, met de stad en de zee in de verte',
  'Wygenerowany komputerowo widok z lotu ptaka na oświetlony budynek o zmierzchu, a w oddali miasto i morze',
  'Datagenerert flyfoto av den opplyste bygningen i skumringen, med byen og havet i bakgrunnen',
  'Datorgenererad flygvy av den upplysta byggnaden i skymningen, med staden och havet bortom')
a(18, 'Computer-generated view of a ground-floor terrace',
  'Vista generada por ordenador de una terraza en planta baja con césped, dos tumbonas y una piscina pequeña, con colinas al fondo',
  'Vue générée par ordinateur d’une terrasse en rez-de-chaussée avec pelouse, deux bains de soleil et un petit bassin, avec des collines au loin',
  'Computergenerierte Ansicht einer Erdgeschossterrasse mit Rasen, zwei Sonnenliegen und einem kleinen Pool, dahinter Hügel',
  'Компьютерная визуализация террасы на первом этаже с газоном, двумя шезлонгами и небольшим бассейном; вдали холмы',
  'منظر مولَّد بالحاسوب لتراس في الطابق الأرضي فيه عشب ومقعدان للتشمس ومسبح صغير، وتلال في الأفق',
  'Computergegenereerd beeld van een terras op de begane grond met gazon, twee ligbedden en een klein zwembad, met heuvels in de verte',
  'Wygenerowany komputerowo widok tarasu na parterze z trawnikiem, dwoma leżakami i małym basenem, a w oddali wzgórza',
  'Datagenerert bilde av en terrasse i første etasje med plen, to solsenger og et lite basseng, med åser i det fjerne',
  'Datorgenererad vy av en terrass på bottenvåningen med gräsmatta, två solstolar och en liten pool, med kullar i fjärran')
a(19, 'A ground-floor garden and pool', 'Un jardín y una piscina en planta baja', 'Un jardin et une piscine au rez-de-chaussée',
  'Ein Erdgeschossgarten mit Pool', 'Сад и бассейн на первом этаже', 'حديقة ومسبح في الطابق الأرضي',
  'Een tuin en zwembad op de begane grond', 'Ogród i basen na parterze', 'En hage og et basseng i første etasje', 'En trädgård och en pool på bottenvåningen')
a(20, 'Computer-generated view of a covered terrace under a white pergola',
  'Vista generada por ordenador de una terraza cubierta bajo una pérgola blanca, con sillones y vistas al mar',
  'Vue générée par ordinateur d’une terrasse couverte sous une pergola blanche, avec fauteuils et vue sur la mer',
  'Computergenerierte Ansicht einer überdachten Terrasse unter einer weißen Pergola mit Loungesesseln und Meerblick',
  'Компьютерная визуализация крытой террасы под белой перголой с креслами и видом на море',
  'منظر مولَّد بالحاسوب لتراس مغطى تحت برغولا بيضاء فيه مقاعد استرخاء وإطلالة على البحر',
  'Computergegenereerd beeld van een overdekt terras onder een witte pergola met loungestoelen en uitzicht op zee',
  'Wygenerowany komputerowo widok zadaszonego tarasu pod białą pergolą z fotelami i widokiem na morze',
  'Datagenerert bilde av en overbygd terrasse under en hvit pergola med loungestoler og utsikt over havet',
  'Datorgenererad vy av en övertäckt terrass under en vit pergola med loungestolar och havsutsikt')
a(21, 'Computer-generated view from above of a rooftop terrace',
  'Vista cenital generada por ordenador de una terraza en la cubierta con tumbonas y una piscina, sobre las terrazas de los balcones inferiores',
  'Vue plongeante générée par ordinateur d’une terrasse sur le toit avec bains de soleil et une piscine, au-dessus des terrasses des balcons inférieurs',
  'Computergenerierte Ansicht von oben auf eine Dachterrasse mit Sonnenliegen und einem Pool, über den Balkonterrassen darunter',
  'Компьютерная визуализация террасы на крыше с шезлонгами и бассейном вид сверху, над террасами балконов нижних этажей',
  'منظر علوي مولَّد بالحاسوب لتراس على السطح فيه مقاعد للتشمس ومسبح، فوق تراسات الشرفات في الأسفل',
  'Computergegenereerd beeld van bovenaf van een dakterras met ligbedden en een zwembad, boven de balkonterrassen eronder',
  'Wygenerowany komputerowo widok z góry na taras na dachu z leżakami i basenem, nad tarasami balkonowymi poniżej',
  'Datagenerert bilde ovenfra av en takterrasse med solsenger og et basseng, over balkongterrassene under',
  'Datorgenererad vy uppifrån av en takterrass med solstolar och en pool, ovanför balkongterrasserna under')
a(22, 'A rooftop terrace and pool', 'Una terraza y una piscina en la cubierta', 'Une terrasse et une piscine sur le toit',
  'Eine Dachterrasse mit Pool', 'Терраса и бассейн на крыше', 'تراس ومسبح على السطح',
  'Een dakterras met zwembad', 'Taras i basen na dachu', 'En takterrasse med basseng', 'En takterrass med pool')
a(23, 'Computer-generated living and dining room with a sofa',
  'Salón-comedor generado por ordenador con sofá, cocina abierta y puertas de cristal al jardín',
  'Séjour-salle à manger généré par ordinateur avec canapé, cuisine ouverte et portes vitrées sur le jardin',
  'Computergeneriertes Wohn- und Esszimmer mit Sofa, offener Küche und Glastüren zum Garten',
  'Компьютерная визуализация гостиной-столовой с диваном, открытой кухней и стеклянными дверями в сад',
  'غرفة معيشة وطعام مولَّدة بالحاسوب فيها أريكة ومطبخ مفتوح وأبواب زجاجية إلى الحديقة',
  'Computergegenereerde woon- en eetkamer met een bank, een open keuken en glazen deuren naar de tuin',
  'Wygenerowany komputerowo salon z jadalnią, sofą, otwartą kuchnią i szklanymi drzwiami do ogrodu',
  'Datagenerert stue og spisestue med sofa, åpent kjøkken og glassdører til hagen',
  'Datorgenererat vardagsrum och matplats med soffa, öppet kök och glasdörrar till trädgården')
a(24, 'Computer-generated bedroom with two single beds',
  'Dormitorio generado por ordenador con dos camas individuales, armario empotrado y puerta corredera de cristal',
  'Chambre générée par ordinateur avec deux lits simples, un placard intégré et une porte vitrée coulissante',
  'Computergeneriertes Schlafzimmer mit zwei Einzelbetten, Einbauschrank und gläserner Schiebetür',
  'Компьютерная визуализация спальни с двумя односпальными кроватями, встроенным шкафом и стеклянной раздвижной дверью',
  'غرفة نوم مولَّدة بالحاسوب فيها سريران مفردان وخزانة مدمجة وباب زجاجي منزلق',
  'Computergegenereerde slaapkamer met twee eenpersoonsbedden, een inbouwkast en een glazen schuifdeur',
  'Wygenerowana komputerowo sypialnia z dwoma łóżkami pojedynczymi, szafą we wnęce i przesuwnymi szklanymi drzwiami',
  'Datagenerert soverom med to enkeltsenger, innebygd garderobeskap og en skyvedør i glass',
  'Datorgenererat sovrum med två enkelsängar, en inbyggd garderob och en glasskjutdörr')
a(25, 'Computer-generated bathroom with a wall-hung vanity',
  'Baño generado por ordenador con mueble de lavabo suspendido, inodoro y ducha a ras de suelo',
  'Salle de bains générée par ordinateur avec meuble-vasque suspendu, WC et douche à l’italienne',
  'Computergeneriertes Badezimmer mit wandhängendem Waschtisch, WC und bodengleicher Dusche',
  'Компьютерная визуализация ванной комнаты с подвесной тумбой с раковиной, унитазом и душевой без поддона',
  'حمام مولَّد بالحاسوب فيه خزانة مغسلة معلّقة على الجدار ومرحاض ودش مفتوح',
  'Computergegenereerde badkamer met een zwevend wastafelmeubel, een toilet en een inloopdouche',
  'Wygenerowana komputerowo łazienka z wiszącą szafką z umywalką, toaletą i prysznicem walk-in',
  'Datagenerert bad med en veggmontert servantskap, et toalett og en dusj uten kar',
  'Datorgenererat badrum med en väggmonterad tvättställsskåp, en toalett och en inbyggd dusch')

# ---------------------------------------------------------------- overview, why, architecture
a(52, 'Twenty-two homes', 'Veintidós viviendas, <em>nueve en la lista</em>', 'Vingt-deux logements, <em>neuf listés</em>',
  'Zweiundzwanzig Wohnungen, <em>neun aufgeführt</em>', 'Двадцать две квартиры, <em>девять в списке</em>',
  'اثنان وعشرون مسكناً، <em>تسعة منها مدرجة</em>', 'Tweeëntwintig woningen, <em>negen op de lijst</em>',
  'Dwadzieścia dwa lokale, <em>dziewięć na liście</em>', 'Tjueto boliger, <em>ni oppført</em>', 'Tjugotvå bostäder, <em>nio listade</em>')
a(53, 'This is one residential building',
  'Se trata de un edificio residencial de 22 viviendas cerca del centro de Estepona. Tiene planta baja, cuatro plantas superiores y una planta de áticos, con dos sótanos para garaje y trasteros. Todas las viviendas tienen tres dormitorios, un salón-comedor con cocina y dos baños, y el dormitorio principal cuenta con baño propio.',
  'Il s’agit d’un immeuble résidentiel de 22 logements près du centre d’Estepona. Il compte un rez-de-chaussée, quatre étages et un niveau de penthouses, avec deux niveaux de sous-sol pour les parkings et les débarras. Chaque logement a trois chambres, un séjour-salle à manger avec cuisine et deux salles de bain, la chambre principale ayant sa propre salle de bain.',
  'Es handelt sich um ein Wohngebäude mit 22 Wohnungen nahe dem Zentrum von Estepona. Es hat ein Erdgeschoss, vier Obergeschosse und eine Penthouse-Ebene sowie zwei Untergeschosse für Stellplätze und Abstellräume. Jede Wohnung hat drei Schlafzimmer, ein Wohn- und Esszimmer mit Küche und zwei Badezimmer; das Hauptschlafzimmer hat ein eigenes Bad.',
  'Это жилой дом на 22 квартиры недалеко от центра Эстепоны. В нём первый этаж, четыре верхних этажа и уровень пентхаусов, а также два подземных уровня под парковку и кладовые. В каждой квартире три спальни, гостиная-столовая с кухней и две ванные комнаты, а у главной спальни своя ванная.',
  'هذا مبنى سكني من 22 مسكناً قرب وسط إستيبونا. فيه طابق أرضي وأربعة طوابق علوية وطابق للبنتهاوس، وطابقان سفليان للمواقف والمخازن. لكل مسكن ثلاث غرف نوم وغرفة معيشة وطعام مع مطبخ وحمامان، ولغرفة النوم الرئيسية حمام خاص بها.',
  'Het is een woongebouw met 22 woningen nabij het centrum van Estepona, met een begane grond, vier bovenverdiepingen en een penthouseniveau, en twee kelderverdiepingen voor parkeerplaatsen en bergingen. Elke woning heeft drie slaapkamers, een woon- en eetkamer met keuken en twee badkamers; de hoofdslaapkamer heeft een eigen badkamer.',
  'To budynek mieszkalny z 22 lokalami w pobliżu centrum Estepony. Ma parter, cztery piętra i poziom penthouse’ów oraz dwa poziomy podziemne z miejscami parkingowymi i komórkami. Każdy lokal ma trzy sypialnie, salon z jadalnią i kuchnią oraz dwie łazienki, a główna sypialnia ma własną łazienkę.',
  'Dette er en boligbygning med 22 boliger nær sentrum av Estepona. Den har første etasje, fire etasjer over og et toppleilighetsnivå, med to kjelleretasjer for parkering og boder. Hver bolig har tre soverom, stue og spisestue med kjøkken og to bad, og hovedsoverommet har eget bad.',
  'Det här är en bostadsbyggnad med 22 bostäder nära centrala Estepona. Den har bottenvåning, fyra våningar ovanför och en takvåningsnivå, med två källarplan för parkering och förråd. Varje bostad har tre sovrum, vardagsrum och matplats med kök samt två badrum, och huvudsovrummet har eget badrum.')
a(54, 'The four ground-floor homes have a terrace',
  'Las cuatro viviendas de planta baja tienen terraza, jardín privado y piscina privada, y cada planta superior tiene cuatro viviendas con grandes terrazas. Algunas de las viviendas superiores tienen un solárium privado en la cubierta con su propia piscina, y en la cubierta hay además una piscina comunitaria, un solárium y servicios. Nueve viviendas figuran con precio; los documentos del promotor no indican una fecha de entrega.',
  'Les quatre logements du rez-de-chaussée ont une terrasse, un jardin privé et une piscine privée, et chaque étage compte quatre logements dotés de grandes terrasses. Certains des logements supérieurs disposent d’un solarium privé sur le toit avec sa propre piscine, et le toit abrite aussi une piscine commune, un solarium et des services. Neuf logements sont listés avec un prix ; les documents du promoteur n’indiquent pas de date de livraison.',
  'Die vier Erdgeschosswohnungen haben eine Terrasse, einen privaten Garten und einen privaten Pool, und jedes Obergeschoss hat vier Wohnungen mit großen Terrassen. Einige der oberen Wohnungen haben ein privates Dachsolarium mit eigenem Pool, und auf dem Dach gibt es außerdem einen Gemeinschaftspool, ein Solarium und Servicebereiche. Neun Wohnungen sind mit Preis aufgeführt; die Unterlagen des Bauträgers nennen keinen Fertigstellungstermin.',
  'У четырёх квартир на первом этаже есть терраса, частный сад и частный бассейн, а на каждом верхнем этаже по четыре квартиры с большими террасами. У некоторых верхних квартир есть частный солярий на крыше со своим бассейном, а на крыше также расположены общий бассейн, солярий и служебные помещения. Девять квартир указаны с ценой; в документах застройщика срок сдачи не назван.',
  'للمساكن الأربعة في الطابق الأرضي تراس وحديقة ومسبح خاصان، ولكل طابق علوي أربعة مساكن بتراسات واسعة. ولبعض المساكن العلوية سولاريوم خاص على السطح مع مسبحه الخاص، كما يضم السطح مسبحاً مشتركاً وسولاريوم ومرافق خدمية. تسعة مساكن مدرجة بالأسعار، ولا تذكر وثائق المطوّر موعداً للتسليم.',
  'De vier woningen op de begane grond hebben een terras, een privétuin en een privézwembad, en elke bovenverdieping heeft vier woningen met grote terrassen. Enkele van de bovenste woningen hebben een privésolarium op het dak met een eigen zwembad, en op het dak liggen ook een gemeenschappelijk zwembad, een solarium en voorzieningen. Negen woningen staan met prijs op de lijst; in de documenten van de ontwikkelaar staat geen opleverdatum.',
  'Cztery lokale na parterze mają taras, prywatny ogród i prywatny basen, a każde piętro ma cztery lokale z dużymi tarasami. Niektóre lokale na górze mają prywatne solarium na dachu z własnym basenem, a na dachu jest także wspólny basen, solarium i zaplecze. Dziewięć lokali ma podaną cenę; w dokumentach dewelopera nie ma terminu oddania.',
  'De fire boligene i første etasje har terrasse, privat hage og privat basseng, og hver etasje over har fire boliger med store terrasser. Noen av de øverste boligene har en privat solterrasse på taket med eget basseng, og på taket er det også et felles basseng, en solterrasse og servicearealer. Ni boliger er oppført med pris; utbyggerens dokumenter oppgir ingen overleveringsdato.',
  'De fyra bostäderna på bottenvåningen har terrass, privat trädgård och privat pool, och varje våning ovanför har fyra bostäder med stora terrasser. Några av de översta bostäderna har en privat solterrass på taket med egen pool, och på taket finns också en gemensam pool, en solterrass och serviceutrymmen. Nio bostäder är listade med pris; exploatörens handlingar anger inget tillträdesdatum.')
a(55, '22 homes', '22 viviendas', '22 logements', '22 Wohnungen', '22 квартиры', '22 مسكناً', '22 woningen', '22 lokale', '22 boliger', '22 bostäder')
a(56, 'Three-bedroom homes near the centre of Estepona, each with',
  'Viviendas de tres dormitorios cerca del centro de Estepona, cada una con plaza de garaje y trastero en el sótano.',
  'Logements de trois chambres près du centre d’Estepona, chacun avec une place de parking et un débarras au sous-sol.',
  'Wohnungen mit drei Schlafzimmern nahe dem Zentrum von Estepona, jeweils mit Stellplatz und Abstellraum im Untergeschoss.',
  'Квартиры с тремя спальнями недалеко от центра Эстепоны, в каждой — парковочное место и кладовая в подземном уровне.',
  'مساكن بثلاث غرف نوم قرب وسط إستيبونا، لكل منها موقف سيارة ومخزن في الطابق السفلي.',
  'Woningen met drie slaapkamers nabij het centrum van Estepona, elk met een parkeerplaats en een berging in de kelder.',
  'Lokale z trzema sypialniami w pobliżu centrum Estepony, każdy z miejscem parkingowym i komórką w podziemiu.',
  'Boliger med tre soverom nær sentrum av Estepona, hver med en parkeringsplass og en bod i kjelleren.',
  'Bostäder med tre sovrum nära centrala Estepona, var och en med en parkeringsplats och ett förråd i källaren.')
a(57, 'Buyers who want a new three-bedroom home',
  'Compradores que buscan una vivienda nueva de tres dormitorios cerca del centro, del puerto deportivo y de la playa, desde una vivienda en planta baja con jardín hasta un ático con solárium en la cubierta.',
  'Acheteurs qui veulent un logement neuf de trois chambres près du centre, du port de plaisance et de la plage, du logement en rez-de-chaussée avec jardin au penthouse avec solarium sur le toit.',
  'Käufer, die eine neue Wohnung mit drei Schlafzimmern nahe dem Zentrum, dem Yachthafen und dem Strand suchen, von der Erdgeschosswohnung mit Garten bis zum Penthouse mit Dachsolarium.',
  'Покупателям, которые ищут новую квартиру с тремя спальнями недалеко от центра, порта и пляжа: от квартиры на первом этаже с садом до пентхауса с солярием на крыше.',
  'للمشترين الذين يبحثون عن مسكن جديد بثلاث غرف نوم قرب الوسط والمرسى والشاطئ، من مسكن في الطابق الأرضي بحديقة إلى بنتهاوس بسولاريوم على السطح.',
  'Kopers die een nieuwe woning met drie slaapkamers zoeken nabij het centrum, de jachthaven en het strand, van een woning op de begane grond met tuin tot een penthouse met dakterras-solarium.',
  'Dla kupujących, którzy szukają nowego lokalu z trzema sypialniami blisko centrum, portu jachtowego i plaży, od lokalu na parterze z ogrodem po penthouse z solarium na dachu.',
  'Kjøpere som vil ha en ny bolig med tre soverom nær sentrum, småbåthavnen og stranden, fra en bolig i første etasje med hage til en toppleilighet med solterrasse på taket.',
  'Köpare som vill ha en ny bostad med tre sovrum nära centrum, småbåtshamnen och stranden, från en bostad på bottenvåningen med trädgård till en takvåning med solterrass på taket.')
a(58, 'One building of 22 homes with terraces on every level',
  'Un edificio de 22 viviendas con terrazas en todas las plantas, jardines y piscinas privados en planta baja, solárium privados con piscina en la cubierta y una piscina comunitaria en lo alto.',
  'Un immeuble de 22 logements avec des terrasses à chaque niveau, des jardins et des piscines privés au rez-de-chaussée, des solariums privés avec piscine sur le toit et une piscine commune en toiture.',
  'Ein Gebäude mit 22 Wohnungen und Terrassen auf jeder Ebene, privaten Gärten und Pools im Erdgeschoss, privaten Dachsolarien mit Pool darüber und einem Gemeinschaftspool auf dem Dach.',
  'Один дом на 22 квартиры с террасами на каждом уровне, частными садами и бассейнами на первом этаже, частными сол$ариями с бассейнами выше и общим бассейном на крыше.',
  'مبنى واحد من 22 مسكناً بتراسات في كل طابق، وحدائق ومسابح خاصة في الطابق الأرضي، وسولاريوم خاص بمسابح في الأعلى، ومسبح مشترك على السطح.',
  'Eén gebouw met 22 woningen met terrassen op elk niveau, privétuinen en privézwembaden op de begane grond, privésolariums met zwembad erboven en een gemeenschappelijk zwembad op het dak.',
  'Jeden budynek z 22 lokalami, z tarasami na każdym poziomie, prywatnymi ogrodami i basenami na parterze, prywatnymi solariami z basenem wyżej i wspólnym basenem na dachu.',
  'Én bygning med 22 boliger med terrasser i alle etasjer, private hager og basseng i første etasje, private solterrasser med basseng høyere opp og et felles basseng på taket.',
  'En byggnad med 22 bostäder med terrasser på varje plan, privata trädgårdar och pooler på bottenvåningen, privata solterrasser med pool högre upp och en gemensam pool på taket.')
T[todo[58]]['ru'] = T[todo[58]]['ru'].replace('сол$ариями', 'солярием')
T[todo[58]]['ru'] = T[todo[58]]['ru'].replace('частными солярием', 'частными соляриями')
a(59, 'The developer’s brochure puts the Estepona marina',
  'El folleto del promotor sitúa el puerto deportivo de Estepona y la playa de La Rada a menos de diez minutos, con la A-7 y la AP-7 muy cerca.',
  'La brochure du promoteur place le port de plaisance d’Estepona et la plage de La Rada à moins de dix minutes, avec l’A-7 et l’AP-7 tout près.',
  'Laut Prospekt des Bauträgers sind der Yachthafen von Estepona und der Strand La Rada in weniger als zehn Minuten erreichbar, die A-7 und die AP-7 liegen in der Nähe.',
  'По данным брошюры застройщика, порт Эстепоны и пляж Ла-Рада находятся менее чем в десяти минутах, а автомагистрали A-7 и AP-7 рядом.',
  'يضع كتيّب المطوّر مرسى إستيبونا وشاطئ لا رادا على بعد أقل من عشر دقائق، مع قرب الطريقين A-7 وAP-7.',
  'Volgens de brochure van de ontwikkelaar liggen de jachthaven van Estepona en het strand van La Rada op minder dan tien minuten, met de A-7 en de AP-7 dichtbij.',
  'Według broszury dewelopera port jachtowy w Esteponie i plaża La Rada są oddalone o mniej niż dziesięć minut, a autostrady A-7 i AP-7 są w pobliżu.',
  'Utbyggerens brosjyre oppgir at småbåthavnen i Estepona og La Rada-stranden ligger under ti minutter unna, med A-7 og AP-7 like i nærheten.',
  'Exploatörens broschyr anger att Esteponas småbåtshamn och stranden La Rada ligger under tio minuter bort, med A-7 och AP-7 i närheten.')
a(60, 'Why check the details', 'Por qué comprobar los detalles', 'Pourquoi vérifier les détails', 'Warum die Einzelheiten prüfen',
  'Почему стоит проверить детали', 'لماذا يجب التحقق من التفاصيل', 'Waarom de details checken', 'Dlaczego warto sprawdzić szczegóły',
  'Hvorfor sjekke detaljene', 'Varför ni bör kontrollera detaljerna')
a(61, 'The documents give no completion date',
  'Los documentos no indican fecha de entrega, calendario de pagos ni si el IVA está incluido, así que confirmamos los tres puntos con el promotor antes de cualquier reserva.',
  'Les documents n’indiquent ni date de livraison, ni échéancier de paiement, ni régime de TVA ; nous confirmons ces trois points avec le promoteur avant toute réservation.',
  'Die Unterlagen nennen weder einen Fertigstellungstermin noch einen Zahlungsplan noch die MwSt.-Regelung; wir klären alle drei Punkte vor jeder Reservierung mit dem Bauträger.',
  'В документах нет ни срока сдачи, ни графика платежей, ни сведений о НДС, поэтому перед любым бронированием мы уточняем все три пункта у застройщика.',
  'لا تذكر الوثائق موعد التسليم ولا جدول الدفعات ولا وضع ضريبة القيمة المضافة، لذا نؤكد هذه النقاط الثلاث مع المطوّر قبل أي حجز.',
  'In de documenten staan geen opleverdatum, geen betalingsschema en geen btw-regeling; wij bevestigen alle drie bij de ontwikkelaar vóór elke reservering.',
  'W dokumentach nie ma terminu oddania, harmonogramu płatności ani informacji o VAT, dlatego przed każdą rezerwacją potwierdzamy wszystkie trzy kwestie u dewelopera.',
  'Dokumentene oppgir verken overleveringsdato, betalingsplan eller mva.-forhold, så vi bekrefter alle tre med utbyggeren før en eventuell reservasjon.',
  'Handlingarna anger varken tillträdesdatum, betalningsplan eller momsförhållande, så vi bekräftar alla tre med exploatören före varje reservation.')
a(62, 'Curved white lines', 'Líneas blancas curvas, <em>terrazas con plantas</em>', 'Lignes blanches courbes, <em>terrasses plantées</em>',
  'Geschwungene weiße Linien, <em>bepflanzte Terrassen</em>', 'Изогнутые белые линии, <em>озеленённые террасы</em>',
  'خطوط بيضاء منحنية، <em>وتراسات مزروعة</em>', 'Gebogen witte lijnen, <em>beplante terrassen</em>',
  'Zaokrąglone białe linie, <em>obsadzone roślinami tarasy</em>', 'Buede hvite linjer, <em>beplantede terrasser</em>', 'Välvda vita linjer, <em>planterade terrasser</em>')
a(63, 'In the developer’s computer-generated images',
  'En las imágenes generadas por ordenador del promotor, el edificio tiene losas de balcón blancas y curvas, terrazas con plantas en todas las plantas y una pérgola en la cubierta, con un diseño contemporáneo que busca aprovechar al máximo la luz natural.',
  'Dans les images générées par ordinateur du promoteur, l’immeuble présente des dalles de balcon blanches et courbes, des terrasses plantées à chaque niveau et une pergola sur le toit, dans un dessin contemporain qui cherche à faire entrer le plus de lumière naturelle possible.',
  'In den computergenerierten Bildern des Bauträgers hat das Gebäude geschwungene weiße Balkonplatten, bepflanzte Terrassen auf jeder Ebene und eine Pergola auf dem Dach, in einem zeitgenössischen Entwurf, der möglichst viel Tageslicht hereinholen soll.',
  'На компьютерных изображениях застройщика у здания изогнутые белые плиты балконов, озеленённые террасы на каждом уровне и пергола на крыше; современный проект рассчитан на максимум естественного света.',
  'في الصور المولَّدة بالحاسوب لدى المطوّر، للمبنى ألواح شرفات بيضاء منحنية وتراسات مزروعة في كل طابق وبرغولا على السطح، بتصميم معاصر يسعى إلى إدخال أكبر قدر من الضوء الطبيعي.',
  'Op de computergegenereerde beelden van de ontwikkelaar heeft het gebouw gebogen witte balkonplaten, beplante terrassen op elk niveau en een pergola op het dak, in een eigentijds ontwerp dat zoveel mogelijk daglicht binnenlaat.',
  'Na wygenerowanych komputerowo obrazach dewelopera budynek ma zaokrąglone białe płyty balkonowe, obsadzone roślinami tarasy na każdym poziomie i pergolę na dachu, w nowoczesnym projekcie, który ma wpuszczać jak najwięcej światła dziennego.',
  'På utbyggerens datagenererte bilder har bygningen buede hvite balkongplater, beplantede terrasser i hver etasje og en pergola på taket, i en moderne utforming som skal slippe inn så mye dagslys som mulig.',
  'På exploatörens datorgenererade bilder har byggnaden välvda vita balkongplattor, planterade terrasser på varje plan och en pergola på taket, i en modern utformning som ska släppa in så mycket dagsljus som möjligt.')
a(64, 'The homes have large glazed doors',
  'Las viviendas tienen grandes puertas acristaladas a las terrazas, y la carpintería del salón-comedor va empotrada en el suelo para que la estancia continúe en la terraza.',
  'Les logements ont de grandes portes vitrées donnant sur les terrasses, et le châssis du séjour-salle à manger est encastré dans le sol pour que la pièce se prolonge sur la terrasse.',
  'Die Wohnungen haben große verglaste Türen zu den Terrassen, und der Rahmen im Wohn- und Esszimmer ist in den Boden eingelassen, sodass der Raum in die Terrasse übergeht.',
  'В квартирах большие остеклённые двери на террасы, а профиль остекления в гостиной-столовой скрыт в полу, так что комната плавно переходит в террасу.',
  'للمساكن أبواب زجاجية كبيرة إلى التراسات، وإطار الزجاج في غرفة المعيشة والطعام مخفي في الأرضية ليمتد الفضاء إلى التراس.',
  'De woningen hebben grote glazen deuren naar de terrassen, en het kozijnprofiel in de woon- en eetkamer is in de vloer verzonken, zodat de ruimte doorloopt in het terras.',
  'Lokale mają duże przeszklone drzwi na tarasy, a profil przeszklenia w salonie z jadalnią jest ukryty w podłodze, dzięki czemu pomieszczenie płynnie przechodzi w taras.',
  'Boligene har store glassdører til terrassene, og glassprofilen i stue og spisestue er skjult i gulvet slik at rommet går sømløst over i terrassen.',
  'Bostäderna har stora glasdörrar till terrasserna, och glasprofilen i vardagsrummet och matplatsen är dold i golvet så att rummet går över i terrassen.')
a(65, 'Reinforced concrete built to the Spanish', 'Hormigón armado conforme al Código Técnico de la Edificación.',
  'Béton armé conforme au Code technique du bâtiment espagnol.', 'Stahlbeton gemäß dem spanischen Technischen Baugesetzbuch (CTE).',
  'Железобетон по требованиям испанского технического строительного кодекса.', 'خرسانة مسلحة وفق الكود الفني الإسباني للبناء.',
  'Gewapend beton volgens de Spaanse technische bouwcode.', 'Armert betong i samsvar med den spanske tekniske byggekoden.',
  'Betong armert i samsvar med den spanske tekniske byggekoden.', 'Armerad betong enligt den spanska tekniska byggkoden.')
T[todo[65]]['pl'] = 'Żelbet zgodny z hiszpańskim kodeksem technicznym budownictwa.'
a(66, 'Multilayer: outer brickwork',
  'Multicapa: fábrica de ladrillo exterior, aislamiento interior, cámara de aire y trasdosado interior, con acabado de mortero exterior.',
  'Multicouche : maçonnerie de brique extérieure, isolation intérieure, lame d’air et doublage intérieur, avec une finition en enduit de mortier extérieur.',
  'Mehrschichtig: äußeres Ziegelmauerwerk, Innendämmung, Luftschicht und Innenverkleidung, mit einem Außenputz aus Mörtel.',
  'Многослойный фасад: наружная кирпичная кладка, внутренняя теплоизоляция, воздушная прослойка и внутренняя облицовка, отделка наружной цементной штукатуркой.',
  'متعددة الطبقات: بناء طوب خارجي وعزل داخلي وفراغ هوائي وبطانة داخلية، مع إنهاء بلاستر إسمنتي خارجي.',
  'Meerlaags: buitenmetselwerk, binnenisolatie, een luchtspouw en een binnenbekleding, afgewerkt met een buitenpleister van mortel.',
  'Wielowarstwowa: zewnętrzny mur z cegły, izolacja od wewnątrz, pustka powietrzna i wewnętrzna okładzina, wykończona tynkiem zaprawowym zewnętrznym.',
  'Flerlags: yttermur av murstein, innvendig isolasjon, luftspalte og innvendig kledning, med et ytre mørtelpuss som finish.',
  'Flerskiktad: yttre tegelmur, invändig isolering, luftspalt och invändig beklädnad, med ett yttre murbruksputs som ytskikt.')
a(67, 'Lacquered aluminium frames with a thermal break and double glazing',
  'Marcos de aluminio lacado con rotura de puente térmico y doble acristalamiento, y persianas motorizadas en los dormitorios.',
  'Cadres en aluminium laqué à rupture de pont thermique et double vitrage, et volets motorisés dans les chambres.',
  'Lackierte Aluminiumrahmen mit thermischer Trennung und Doppelverglasung sowie motorisierte Rollläden in den Schlafzimmern.',
  'Окрашенные алюминиевые рамы с терморазрывом и двойное остекление, моторизованные ставни в спальнях.',
  'إطارات ألمنيوم مطلية بقاطع حراري وزجاج مزدوج، ومصاريع كهربائية في غرف النوم.',
  'Gelakte aluminium kozijnen met thermische onderbreking en dubbele beglazing, en gemotoriseerde rolluiken in de slaapkamers.',
  'Lakierowane ramy aluminiowe z przerwą termiczną i podwójne szyby oraz elektryczne rolety w sypialniach.',
  'Lakkerte aluminiumsrammer med termisk brudd og dobbeltglass, og motoriserte skodder på soverommene.',
  'Lackerade aluminiumkarmar med termisk brytning och dubbelglas, och motoriserade rullgardiner i sovrummen.')
a(68, 'Large-format non-slip porcelain paving',
  'Pavimento de gres porcelánico antideslizante de gran formato, con iluminación LED.',
  'Revêtement en grès cérame antidérapant grand format, avec éclairage LED.',
  'Rutschhemmender großformatiger Feinsteinzeugbelag mit LED-Beleuchtung.',
  'Крупноформатный нескользящий керамогранит, светодиодное освещение.',
  'أرضية من البورسلين الكبير غير الزلق، مع إضاءة LED.',
  'Antislip porseleinen tegels in groot formaat, met LED-verlichting.',
  'Wielkoformatowa antypoślizgowa płytka gresowa z oświetleniem LED.',
  'Sklisikre porselensfliser i stort format, med LED-belysning.',
  'Halkfria porslinsplattor i stort format, med LED-belysning.')

# ---------------------------------------------------------------- quality specification
a(69, 'Source: the developer’s quality specification',
  'Fuente: la memoria de calidades del promotor para esta promoción, que no lleva versión ni fecha. Indica que la dirección facultativa puede modificar los materiales siempre que no se reduzca la calidad, y que la información no es contractual.',
  'Source : le descriptif de qualité du promoteur pour ce programme, qui ne porte ni version ni date. Il précise que la direction des travaux peut modifier les matériaux tant que la qualité n’est pas réduite, et que l’information n’est pas contractuelle.',
  'Quelle: die Baubeschreibung des Bauträgers für dieses Projekt, die weder Version noch Datum trägt. Sie besagt, dass die Bauleitung die Materialien ändern darf, solange die Qualität nicht gemindert wird, und dass die Angaben nicht vertraglich bindend sind.',
  'Источник: спецификация качества застройщика для этого комплекса, без номера версии и даты. В ней сказано, что руководство проекта может менять материалы, если качество не снижается, и что сведения не носят договорного характера.',
  'المصدر: مواصفات الجودة الخاصة بالمطوّر لهذا المشروع، وهي بلا رقم إصدار أو تاريخ. تنص على أن إدارة المشروع قد تغيّر المواد ما دامت الجودة لا تنخفض، وأن المعلومات غير ملزمة تعاقدياً.',
  'Bron: het lastenboek van de ontwikkelaar voor dit project, zonder versienummer of datum. Daarin staat dat de projectleiding de materialen mag wijzigen zolang de kwaliteit niet daalt, en dat de informatie niet contractueel is.',
  'Źródło: specyfikacja jakości dewelopera dla tej inwestycji, bez numeru wersji i daty. Zastrzega ona, że kierownictwo projektu może zmieniać materiały, o ile nie obniża to jakości, i że informacje nie mają charakteru umownego.',
  'Kilde: utbyggerens kvalitetsbeskrivelse for dette prosjektet, uten versjonsnummer og dato. Den sier at prosjektledelsen kan endre materialene så lenge kvaliteten ikke reduseres, og at opplysningene ikke er kontraktsfestet.',
  'Källa: exploatörens kvalitetsbeskrivning för det här projektet, utan versionsnummer och datum. Den anger att projektledningen får ändra materialen så länge kvaliteten inte försämras, och att uppgifterna inte är avtalsbundna.')
a(70, 'Structure, facade and roofs', 'Estructura, fachada y cubiertas', 'Structure, façade et toitures', 'Konstruktion, Fassade und Dächer',
  'Конструкция, фасад и кровля', 'الهيكل والواجهة والأسقف', 'Structuur, gevel en daken', 'Konstrukcja, elewacja i dachy', 'Konstruksjon, fasade og tak', 'Konstruktion, fasad och tak')
a(71, 'A reinforced-concrete structure',
  'Una estructura de hormigón armado, con cimentación diseñada según el estudio geotécnico, y una fachada multicapa de fábrica de ladrillo exterior, aislamiento interior, cámara de aire y trasdosado interior, con acabado de mortero exterior.',
  'Une structure en béton armé, avec des fondations conçues d’après l’étude géotechnique, et une façade multicouche en maçonnerie de brique extérieure, isolation intérieure, lame d’air et doublage intérieur, avec une finition en enduit de mortier extérieur.',
  'Eine Stahlbetonkonstruktion mit Fundamenten nach dem geotechnischen Gutachten und eine mehrschichtige Fassade aus äußerem Ziegelmauerwerk, Innendämmung, Luftschicht und Innenverkleidung, mit Außenputz aus Mörtel.',
  'Железобетонный каркас с фундаментом по результатам геотехнических изысканий и многослойный фасад из наружной кирпичной кладки, внутренней теплоизоляции, воздушной прослойки и внутренней облицовки с отделкой наружной цементной штукатуркой.',
  'هيكل من الخرسانة المسلحة بأساسات مصممة وفق الدراسة الجيوتقنية، وواجهة متعددة الطبقات من بناء طوب خارجي وعزل داخلي وفراغ هوائي وبطانة داخلية، بإنهاء من بلاستر إسمنتي خارجي.',
  'Een gewapend-betonnen draagstructuur met funderingen volgens het geotechnisch onderzoek en een meerlaagse gevel van buitenmetselwerk, binnenisolatie, een luchtspouw en een binnenbekleding, afgewerkt met een buitenpleister van mortel.',
  'Konstrukcja żelbetowa z fundamentami zaprojektowanymi na podstawie badań geotechnicznych oraz wielowarstwowa elewacja z zewnętrznego muru z cegły, izolacji od wewnątrz, pustki powietrznej i wewnętrznej okładziny, wykończona tynkiem zaprawowym zewnętrznym.',
  'En armert betongkonstruksjon med fundamenter prosjektert etter den geotekniske undersøkelsen, og en flerlags fasade av ytre murstein, innvendig isolasjon, luftspalte og innvendig kledning, med ytre mørtelpuss som finish.',
  'En stomme av armerad betong med grundläggning utformad efter den geotekniska undersökningen, och en flerskiktad fasad av yttre tegelmur, invändig isolering, luftspalt och invändig beklädnad, med yttre murbruksputs som ytskikt.')
a(72, 'Flat inverted roofs',
  'Cubiertas planas invertidas, impermeabilizadas y aisladas con planchas rígidas, con acabado de grava donde no hay acceso y de solado cerámico antideslizante donde sí lo hay.',
  'Toitures-terrasses inversées, étanchées et isolées par des panneaux rigides, avec une finition en gravier là où il n’y a pas d’accès et en carrelage céramique antidérapant là où il y en a.',
  'Flache Umkehrdächer, abgedichtet und mit Hartschaumplatten gedämmt, mit Kiesschüttung auf nicht begehbaren Flächen und rutschhemmendem Keramikbelag auf begehbaren.',
  'Плоские инверсионные кровли с гидроизоляцией и утеплением жёсткими плитами; в местах без доступа — гравийная отсыпка, в доступных зонах — нескользящая керамическая плитка.',
  'أسقف مسطحة معكوسة معزولة مائياً وحرارياً بألواح صلبة، بتشطيب من الحصى حيث لا يوجد وصول وببلاط خزفي غير زلق حيث يوجد.',
  'Platte omgekeerde daken, waterdicht en geïsoleerd met harde isolatieplaten, afgewerkt met grind waar geen toegang is en met antislip keramische tegels waar die er wel is.',
  'Płaskie dachy odwrócone, zaizolowane przeciwwilgociowo i cieplnie sztywnymi płytami, wykończone żwirem tam, gdzie nie ma dostępu, i antypoślizgową płytką ceramiczną tam, gdzie jest.',
  'Flate omvendte tak, fuktisolert og isolert med harde plater, med grus som finish der det ikke er adkomst og sklisikre keramiske fliser der det er.',
  'Platta omvända tak, fuktisolerade och isolerade med hårda skivor, med grus som ytskikt där åtkomst saknas och halkfria keramikplattor där åtkomst finns.')
a(73, 'Windows and insulation', 'Ventanas y aislamiento', 'Fenêtres et isolation', 'Fenster und Dämmung',
  'Окна и изоляция', 'النوافذ والعزل', 'Ramen en isolatie', 'Okna i izolacja', 'Vinduer og isolasjon', 'Fönster och isolering')
a(74, 'Lacquered aluminium frames with a thermal break, opening',
  'Marcos de aluminio lacado con rotura de puente térmico, abatibles, oscilobatientes o correderas según su ubicación, con doble acristalamiento de cámara de aire deshidratado elegido según la orientación, y persianas motorizadas en los dormitorios accionadas con pulsador.',
  'Cadres en aluminium laqué à rupture de pont thermique, ouvrants à la française, oscillo-battants ou coulissants selon l’emplacement, avec double vitrage à lame d’air déshydratée choisi selon l’orientation, et volets motorisés dans les chambres commandés par bouton-poussoir.',
  'Lackierte Aluminiumrahmen mit thermischer Trennung, je nach Lage Dreh-, Dreh-Kipp- oder Schiebeelemente, mit Doppelverglasung mit entfeuchteter Luftkammer je nach Ausrichtung sowie motorisierte Rollläden in den Schlafzimmern mit Tastersteuerung.',
  'Окрашенные алюминиевые рамы с терморазрывом, поворотные, поворотно-откидные или раздвижные в зависимости от места, с двойным остеклением с осушенной воздушной камерой, подобранным по ориентации, и моторизованные ставни в спальнях с управлением кнопкой.',
  'إطارات ألمنيوم مطلية بقاطع حراري، تفتح بالدوران أو بالدوران والإمالة أو بالانزلاق بحسب الموقع، مع زجاج مزدوج بحجرة هواء مجففة يُختار بحسب الاتجاه، ومصاريع كهربائية في غرف النوم تُشغَّل بزر.',
  'Gelakte aluminium kozijnen met thermische onderbreking, draaiend, draai-kiep of schuivend naargelang de plek, met dubbele beglazing met gedroogde luchtkamer gekozen naar oriëntatie, en gemotoriseerde rolluiken in de slaapkamers met drukknopbediening.',
  'Lakierowane ramy aluminiowe z przerwą termiczną, otwierane, uchylno-rozwierane lub przesuwne zależnie od miejsca, z podwójnymi szybami z osuszoną komorą powietrzną dobranymi do orientacji oraz elektryczne rolety w sypialniach sterowane przyciskiem.',
  'Lakkerte aluminiumsrammer med termisk brudd, side-, sidehengslede/tilt- eller skyvevinduer etter plassering, med dobbeltglass med tørket luftkammer valgt etter himmelretning, og motoriserte skodder på soverommene betjent med trykknapp.',
  'Lackerade aluminiumkarmar med termisk brytning, sidohängda, kipp- eller skjutbara efter läge, med dubbelglas med avfuktad luftspalt valt efter väderstreck, och motoriserade rullgardiner i sovrummen med tryckknappsstyrning.')
a(75, 'Dry plasterboard partitions',
  'Tabiquería seca de placas de yeso laminado sobre perfilería metálica con aislamiento térmico y acústico de lana mineral, placas hidrófugas en zonas húmedas, y separaciones entre viviendas y zonas comunes de ladrillo perforado con trasdosado aislante.',
  'Cloisons sèches en plaques de plâtre sur ossature métallique avec isolation thermique et acoustique en laine minérale, plaques hydrofuges dans les pièces d’eau, et séparations entre logements et parties communes en brique perforée avec un doublage isolant.',
  'Trockenbauwände aus Gipskartonplatten auf Metallprofilen mit Wärme- und Schalldämmung aus Mineralwolle, feuchtigkeitsbeständige Platten in Nassbereichen und Trennwände zwischen Wohnungen und Gemeinschaftsbereichen aus Lochziegel mit gedämmter Vorsatzschale.',
  'Сухие перегородки из гипсокартона на металлическом каркасе с тепло- и звукоизоляцией из минеральной ваты, влагостойкие плиты во влажных зонах, а между квартирами и местами общего пользования — стены из пустотелого кирпича с утеплённой облицовкой.',
  'حواجز جافة من ألواح الجبس على هيكل معدني مع عزل حراري وصوتي من الصوف الصخري، وألواح مقاومة للرطوبة في المناطق الرطبة، وجدران فاصلة بين المساكن والمناطق المشتركة من الطوب المثقب مع بطانة معزولة.',
  'Droge scheidingswanden van gipsplaten op een metalen frame met thermische en akoestische isolatie van minerale wol, vochtbestendige platen in natte ruimtes, en scheidingen tussen woningen en gemeenschappelijke ruimtes van geperforeerde baksteen met een geïsoleerde voorzetwand.',
  'Suche przegrody z płyt gipsowo-kartonowych na stelażu metalowym z izolacją cieplną i akustyczną z wełny mineralnej, płyty wodoodporne w pomieszczeniach mokrych oraz ściany między lokalami a częściami wspólnymi z cegły dziurawki z izolowaną okładziną.',
  'Tørre skillevegger av gipsplater på stålprofiler med varme- og lydisolasjon av mineralull, fuktbestandige plater i våtrom, og skiller mellom boliger og fellesarealer av hullmurstein med isolert kledning.',
  'Torra mellanväggar av gipsskivor på stålreglar med värme- och ljudisolering av mineralull, fuktbeständiga skivor i våtutrymmen, och väggar mellan bostäder och gemensamma ytor av hålsten med isolerad beklädnad.')
a(76, 'A reinforced security front door',
  'Puerta de entrada blindada con cerradura de tres puntos, puertas de paso lacadas de hoja lisa con herrajes de acero inoxidable o cromo mate, y armarios modulares empotrados totalmente forrados, con cajoneras, balda y barra de colgar.',
  'Porte d’entrée blindée à serrure trois points, portes intérieures planes laquées avec quincaillerie en acier inoxydable ou chrome mat, et placards modulaires encastrés entièrement aménagés, avec tiroirs, tablette et barre de penderie.',
  'Eine einbruchhemmende Wohnungseingangstür mit Dreipunktverriegelung, lackierte glatte Innentüren mit Beschlägen aus Edelstahl oder Mattchrom und vollständig ausgekleidete modulare Einbauschränke mit Schubladen, Ablage und Kleiderstange.',
  'Бронированная входная дверь с трёхточечным замком, окрашенные гладкие межкомнатные двери с фурнитурой из нержавеющей стали или матового хрома и встроенные модульные шкафы с полной внутренней отделкой, ящиками, полкой и штангой.',
  'باب دخول مصفّح بقفل ثلاثي النقاط، وأبواب داخلية ملساء مطلية بإكسسوارات من الفولاذ المقاوم للصدأ أو الكروم غير اللامع، وخزائن مدمجة مبطّنة بالكامل بأدراج ورف وعمود تعليق.',
  'Een pantserdeur als voordeur met driepuntssluiting, gelakte vlakke binnendeuren met beslag van roestvrij staal of matchroom, en volledig afgewerkte modulaire inbouwkasten met lades, een hoedenplank en een kledingstang.',
  'Pancerne drzwi wejściowe z zamkiem trzypunktowym, lakierowane gładkie drzwi wewnętrzne z okuciami ze stali nierdzewnej lub matowego chromu oraz zabudowane szafy modułowe w pełni wyłożone od środka, z szufladami, półką i drążkiem.',
  'En pansret inngangsdør med trepunktslås, lakkerte plane innerdører med beslag i rustfritt stål eller matt krom, og innebygde moduler-garderobeskap fullt kledd inni, med skuffer, hylle og klesstang.',
  'En pansardörr med trepunktslås, lackerade släta innerdörrar med beslag i rostfritt stål eller matt krom, och inbyggda modulgarderober helt klädda invändigt, med lådor, hylla och klädstång.')
T[todo[76]]['no'] = 'En pansret inngangsdør med trepunktslås, lakkerte plane innerdører med beslag i rustfritt stål eller matt krom, og innebygde modulgarderober fullt kledd innvendig, med skuffer, hylle og klesstang.'
a(77, 'Large-format rectified porcelain stoneware throughout',
  'Gres porcelánico rectificado de gran formato en toda la vivienda, gres rectificado antideslizante en las terrazas, porcelánico en suelos y paredes de los baños, y techos de placa de yeso laminado con aislamiento de lana mineral.',
  'Grès cérame rectifié grand format dans tout le logement, grès rectifié antidérapant sur les terrasses, grès cérame au sol et aux murs des salles de bain, et plafonds en plaques de plâtre avec isolation en laine minérale.',
  'Großformatiges rektifiziertes Feinsteinzeug in der gesamten Wohnung, rutschhemmendes rektifiziertes Feinsteinzeug auf den Terrassen, Feinsteinzeug auf Böden und Wänden der Bäder sowie Gipskartondecken mit Mineralwolldämmung.',
  'Крупноформатный ректифицированный керамогранит во всей квартире, нескользящий ректифицированный керамогранит на террасах, керамогранит на полу и стенах ванных комнат и гипсокартонные потолки с изоляцией из минеральной ваты.',
  'بورسلين مصقول كبير الحجم في كامل المسكن، وبورسلين مصقول غير زلق على التراسات، وبورسلين على أرضيات الحمامات وجدرانها، وأسقف من ألواح الجبس بعزل من الصوف الصخري.',
  'Groot formaat gerectificeerd porseleinen tegelwerk in de hele woning, antislip gerectificeerd porselein op de terrassen, porselein op de vloeren en wanden van de badkamers, en plafonds van gipsplaten met isolatie van minerale wol.',
  'Wielkoformatowy rektyfikowany gres w całym lokalu, antypoślizgowy rektyfikowany gres na tarasach, gres na podłogach i ścianach łazienek oraz sufity z płyt gipsowo-kartonowych z izolacją z wełny mineralnej.',
  'Rektifisert porselensflis i stort format i hele boligen, sklisikker rektifisert porselensflis på terrassene, porselensflis på gulv og vegger på badene, og himlinger av gipsplater med mineralullisolasjon.',
  'Rektifierat porslinsgods i stort format i hela bostaden, halkfritt rektifierat porslinsgods på terrasserna, porslinsgods på golv och väggar i badrummen, och innertak av gipsskivor med mineralullsisolering.')
a(78, 'A fully fitted kitchen with laminate',
  'Cocina completamente amueblada con muebles altos y bajos laminados, encimera de material porcelánico de alta resistencia de unos 12 mm de grosor o similar, fregadero de acero inoxidable bajo encimera y grifo monomando cromado.',
  'Cuisine entièrement équipée avec meubles hauts et bas stratifiés, plan de travail en matériau porcelainique haute résistance d’environ 12 mm d’épaisseur ou similaire, évier en inox sous plan et mitigeur chromé.',
  'Eine vollständig eingerichtete Küche mit laminierten Ober- und Unterschränken, einer Arbeitsplatte aus hochbelastbarem Porzellanmaterial von etwa 12 mm Stärke oder gleichwertig, einem unterbauten Edelstahlspülbecken und einer verchromten Einhebelarmatur.',
  'Полностью оборудованная кухня с верхними и нижними шкафами с ламинированной отделкой, столешницей из высокопрочного керамического материала толщиной около 12 мм или аналогичной, врезной мойкой из нержавеющей стали и хромированным однорычажным смесителем.',
  'مطبخ مجهّز بالكامل بخزائن علوية وسفلية بتشطيب لاميناتي، وسطح عمل من مادة بورسلين عالية التحمل بسماكة نحو 12 ملم أو ما يماثلها، وحوض من الفولاذ المقاوم للصدأ مدمج تحت السطح وحنفية كروم بذراع واحدة.',
  'Een volledig ingerichte keuken met laminaat boven- en onderkasten, een werkblad van zeer sterk porseleinmateriaal van ongeveer 12 mm dik of gelijkwaardig, een onderbouwspoelbak van roestvrij staal en een verchroomde eengreepskraan.',
  'W pełni wyposażona kuchnia z laminowanymi szafkami górnymi i dolnymi, blatem z wysoce wytrzymałego materiału porcelanowego o grubości około 12 mm lub podobnego, zlewozmywakiem ze stali nierdzewnej montowanym pod blatem i chromowaną baterią jednouchwytową.',
  'Et fullt utstyrt kjøkken med laminerte over- og underskap, en benkeplate av svært slitesterkt porselensmateriale på omtrent 12 mm eller tilsvarende, en underlimt vask i rustfritt stål og en forkrommet énhåndsblander.',
  'Ett helt utrustat kök med laminerade över- och underskåp, en bänkskiva av mycket slitstarkt porslinsmaterial på cirka 12 mm eller motsvarande, en underlimmad diskho i rostfritt stål och en förkromad enhandsblandare.')
a(79, 'Appliances included',
  'Electrodomésticos incluidos: horno eléctrico, microondas, placa de inducción, campana extractora, lavavajillas integrable, frigorífico y lavadora.',
  'Électroménager inclus : four électrique, micro-ondes, plaque à induction, hotte aspirante, lave-vaisselle intégrable, réfrigérateur et lave-linge.',
  'Geräte inklusive: Elektrobackofen, Mikrowelle, Induktionskochfeld, Dunstabzugshaube, integrierter Geschirrspüler, Kühlschrank und Waschmaschine.',
  'Бытовая техника входит в комплект: электрическая духовка, микроволновая печь, индукционная варочная панель, вытяжка, встраиваемая посудомоечная машина, холодильник и стиральная машина.',
  'الأجهزة مشمولة: فرن كهربائي وميكروويف وموقد حثي وشفاط وغسالة صحون مدمجة وثلاجة وغسالة ملابس.',
  'Apparatuur inbegrepen: een elektrische oven, een magnetron, een inductiekookplaat, een afzuigkap, een inbouwvaatwasser, een koelkast en een wasmachine.',
  'W cenie sprzęt AGD: piekarnik elektryczny, kuchenka mikrofalowa, płyta indukcyjna, okap, zmywarka do zabudowy, lodówka i pralka.',
  'Hvitevarer inkludert: en elektrisk ovn, en mikrobølgeovn, en induksjonstopp, en kjøkkenvifte, en integrert oppvaskmaskin, et kjøleskap og en vaskemaskin.',
  'Vitvaror ingår: en elugn, en mikrovågsugn, en induktionshäll, en köksfläkt, en integrerad diskmaskin, ett kylskåp och en tvättmaskin.')
a(80, 'Washbasins set into the countertop',
  'Lavabos integrados en la encimera con mueble suspendido, platos de ducha de perfil bajo con mampara de cristal, grifería de ducha termostática cromada con barra deslizante y rociador de mano, e inodoros con cisterna empotrada, doble descarga y asiento amortiguado.',
  'Vasques intégrées au plan avec meuble suspendu, receveurs de douche extra-plats avec paroi en verre, mitigeurs de douche thermostatiques chromés avec barre coulissante et douchette, et WC à réservoir encastré, double chasse et abattant amortisseur.',
  'In die Arbeitsplatte integrierte Waschbecken mit wandhängendem Unterschrank, flache Duschtassen mit Glasabtrennung, verchromte Thermostat-Duscharmaturen mit Gleitstange und Handbrause sowie WCs mit Unterputzspülkasten, Zweimengenspülung und Soft-Close-Sitz.',
  'Умывальники, встроенные в столешницу, с подвесными тумбами, низкие душевые поддоны со стеклянными ограждениями, хромированные термостатические душевые смесители со скользящей штангой и ручной лейкой, а также унитазы со скрытым бачком, двойным смывом и сиденьем с плавным закрытием.',
  'مغاسل مدمجة في سطح الخزانة مع خزائن معلّقة، وأحواض دش منخفضة بحواجز زجاجية، وخلاطات دش ثرموستاتية بلون الكروم مع عمود منزلق ورشاش يدوي، ومراحيض بخزان مخفي وتصريف مزدوج ومقعد هادئ الإغلاق.',
  'Wastafels ingebouwd in het blad met zwevende onderkasten, lage douchebakken met glazen afscheiding, verchroomde thermostatische douchekranen met glijstang en handdouche, en toiletten met verborgen stortbak, dubbele spoeling en soft-closezitting.',
  'Umywalki wpuszczone w blat z wiszącymi szafkami, niskie brodziki z szklanymi parawanami, chromowane termostatyczne baterie prysznicowe z drążkiem przesuwnym i słuchawką oraz toalety z ukrytą spłuczką, dwudzielnym spłukiwaniem i deską wolnoopadającą.',
  'Servanter innfelt i benkeplaten med veggmonterte skap, flate dusjkar med glassvegger, forkrommede termostatiske dusjblandere med glidestang og håndsdusj, og toaletter med innebygd sisterne, tosidig spyling og mykt lukkende sete.',
  'Handfat infällda i bänkskivan med väggmonterade underskåp, låga duschkar med glasväggar, förkromade termostatiska duschblandare med glidstång och handdusch, och toaletter med dold spolcistern, tvåmängdsspolning och mjukstängande sits.')
a(81, 'Climate, hot water and electrics', 'Climatización, agua caliente y electricidad', 'Climatisation, eau chaude et électricité',
  'Klima, Warmwasser und Elektrik', 'Климат, горячая вода и электрика', 'التكييف والماء الساخن والكهرباء',
  'Klimaat, warm water en elektra', 'Klimatyzacja, ciepła woda i elektryka', 'Klima, varmtvann og elektrisk', 'Klimat, varmvatten och el')
a(82, 'Ducted air conditioning for cooling and heating',
  'Aire acondicionado por conductos para frío y calor, zonificado por estancias, agua caliente mediante aerotermia, suelo radiante eléctrico en los baños y un sistema de ventilación con renovación continua del aire.',
  'Climatisation gainable pour le froid et le chaud, par zones de pièces, eau chaude par système aérothermique, plancher chauffant électrique dans les salles de bain et système de ventilation à renouvellement d’air continu.',
  'Kanalklimaanlage zum Kühlen und Heizen, nach Räumen zoniert, Warmwasser über ein Aerothermiesystem, elektrische Fußbodenheizung in den Bädern und ein Lüftungssystem mit kontinuierlichem Luftaustausch.',
  'Канальный кондиционер для охлаждения и обогрева с зонированием по комнатам, горячая вода от аэротермальной системы, электрический тёплый пол в ванных комнатах и система вентиляции с постоянным обновлением воздуха.',
  'تكييف بالمجاري للتبريد والتدفئة مقسّم بحسب الغرف، وماء ساخن من نظام الطاقة الهوائية الحرارية، وتدفئة كهربائية تحت أرضية الحمامات، ونظام تهوية بتجديد مستمر للهواء.',
  'Kanaalairconditioning voor koelen en verwarmen, per ruimte gezoneerd, warm water via een aerothermisch systeem, elektrische vloerverwarming in de badkamers en een ventilatiesysteem met continue luchtverversing.',
  'Klimatyzacja kanałowa do chłodzenia i ogrzewania, strefowana według pomieszczeń, ciepła woda z systemu aerotermalnego, elektryczne ogrzewanie podłogowe w łazienkach i system wentylacji z ciągłą wymianą powietrza.',
  'Kanalbasert klimaanlegg for kjøling og oppvarming, soneinndelt etter rom, varmtvann fra et aerotermisk system, elektrisk gulvvarme på badene og et ventilasjonssystem med kontinuerlig luftfornyelse.',
  'Kanalburen luftkonditionering för kyla och värme, zonindelad per rum, varmvatten från ett aerotermiskt system, elektrisk golvvärme i badrummen och ett ventilationssystem med kontinuerlig luftväxling.')
a(83, 'Recessed LED lighting in the kitchen',
  'Iluminación LED empotrada en cocinas, pasillos y baños, iluminación LED en las terrazas, tomas de TV, radio y teléfono en salones, cocinas y dormitorios, videoportero en color, y puntos de agua en las terrazas de solárium y en los jardines de planta baja.',
  'Éclairage LED encastré dans les cuisines, couloirs et salles de bain, éclairage LED sur les terrasses, prises TV, radio et téléphone dans les séjours, cuisines et chambres, interphone vidéo couleur, et points d’eau sur les terrasses solarium et dans les jardins du rez-de-chaussée.',
  'Eingelassene LED-Beleuchtung in Küchen, Fluren und Bädern, LED-Beleuchtung auf den Terrassen, TV-, Radio- und Telefonanschlüsse in Wohnzimmern, Küchen und Schlafzimmern, eine Farb-Videosprechanlage sowie Wasseranschlüsse auf den Solarium-Terrassen und in den Erdgeschossgärten.',
  'Встроенное светодиодное освещение на кухнях, в коридорах и ванных комнатах, светодиодное освещение на террасах, розетки для ТВ, радио и телефона в гостиных, на кухнях и в спальнях, цветной видеодомофон, а также точки подключения воды на террасах-солярии и в садах первого этажа.',
  'إضاءة LED مدمجة في المطابخ والممرات والحمامات، وإضاءة LED على التراسات، ومخارج للتلفاز والراديو والهاتف في غرف المعيشة والمطابخ وغرف النوم، وجهاز اتصال مرئي ملوّن، ونقاط مياه في تراسات السولاريوم وحدائق الطابق الأرضي.',
  'Inbouw-LED-verlichting in keukens, gangen en badkamers, LED-verlichting op de terrassen, tv-, radio- en telefoonaansluitingen in woonkamers, keukens en slaapkamers, een kleurenvideofoon en wateraansluitingen op de solariumterrassen en in de tuinen op de begane grond.',
  'Wpuszczane oświetlenie LED w kuchniach, korytarzach i łazienkach, oświetlenie LED na tarasach, gniazda TV, radiowe i telefoniczne w salonach, kuchniach i sypialniach, kolorowy wideodomofon oraz punkty poboru wody na tarasach solarium i w ogrodach na parterze.',
  'Innfelt LED-belysning på kjøkken, i ganger og på bad, LED-belysning på terrassene, TV-, radio- og telefonuttak i stuer, kjøkken og soverom, en fargevideoporttelefon og vannuttak på solterrassene og i hagene i første etasje.',
  'Infälld LED-belysning i kök, hallar och badrum, LED-belysning på terrasserna, uttag för tv, radio och telefon i vardagsrum, kök och sovrum, en färgvideotelefon och vattenuttag på solterrasserna och i trädgårdarna på bottenvåningen.')
a(84, 'Building and garage', 'Edificio y garaje', 'Immeuble et parking', 'Gebäude und Garage',
  'Здание и паркинг', 'المبنى والمواقف', 'Gebouw en garage', 'Budynek i garaż', 'Bygning og garasje', 'Byggnad och garage')
a(85, 'A communal pool is planned',
  'Se proyecta una piscina comunitaria en la terraza de la cubierta, con aseo y cuarto de instalaciones. Los portales tienen pavimento de piedra, cerámica o piedra artificial e iluminación LED con detectores de presencia.',
  'Une piscine commune est prévue sur le toit-terrasse, avec des sanitaires et un local technique. Les halls d’entrée sont revêtus de pierre, de céramique ou de pierre reconstituée et éclairés par LED avec détecteurs de présence.',
  'Auf der Dachterrasse ist ein Gemeinschaftspool geplant, mit Toiletten und einem Technikraum. Die Eingangshallen haben Böden aus Stein, Keramik oder Kunststein und LED-Beleuchtung mit Präsenzmeldern.',
  'На крыше-террасе планируется общий бассейн с санузлом и техническим помещением. Вестибюли отделаны камнем, керамикой или искусственным камнем и освещены светодиодными светильниками с датчиками присутствия.',
  'يُخطَّط لمسبح مشترك على تراس السطح مع دورة مياه وغرفة للتجهيزات. وأرضيات مداخل المبنى من الحجر أو الخزف أو الحجر الصناعي، وإضاءتها LED بكاشفات حضور.',
  'Op het dakterras is een gemeenschappelijk zwembad gepland, met een toilet en een technische ruimte. De entreehallen hebben een vloer van steen, keramiek of kunststeen en LED-verlichting met aanwezigheidsmelders.',
  'Na tarasie dachowym planowany jest wspólny basen z toaletą i pomieszczeniem technicznym. Hole wejściowe mają posadzki z kamienia, ceramiki lub kamienia sztucznego i oświetlenie LED z czujnikami obecności.',
  'Et felles basseng er planlagt på takterrassen, med toalett og teknisk rom. Inngangspartiene har gulv av stein, keramikk eller kunststein og LED-belysning med tilstedeværelsesdetektorer.',
  'En gemensam pool planeras på takterrassen, med toalett och teknikrum. Entréhallarna har golv av sten, keramik eller konststen och LED-belysning med närvarodetektorer.')
a(86, 'Lifts serve every floor',
  'Los ascensores sirven a todas las plantas y comunican directamente con las plantas de garaje, con puertas automáticas, detección de sobrecarga y conexión telefónica. El suelo del garaje es de hormigón pulido.',
  'Les ascenseurs desservent tous les étages et relient directement les niveaux de parking, avec portes automatiques, détection de surcharge et liaison téléphonique. Le sol du parking est en béton poli.',
  'Aufzüge bedienen alle Etagen und verbinden direkt mit den Garagenebenen, mit automatischen Türen, Überlasterkennung und Telefonanbindung. Der Garagenboden besteht aus poliertem Beton.',
  'Лифты обслуживают все этажи и напрямую соединены с уровнями паркинга, оснащены автоматическими дверями, датчиком перегрузки и телефонной связью. Пол паркинга — полированный бетон.',
  'تخدم المصاعد جميع الطوابق وتتصل مباشرة بطوابق المواقف، بأبواب أوتوماتيكية وكشف للحمل الزائد واتصال هاتفي. أرضية المواقف من الخرسانة المصقولة.',
  'Liften bedienen alle verdiepingen en verbinden rechtstreeks met de garageniveaus, met automatische deuren, overbelastingsdetectie en een telefoonverbinding. De garagevloer is van gepolijst beton.',
  'Windy obsługują wszystkie piętra i łączą się bezpośrednio z poziomami garażu, mają automatyczne drzwi, czujnik przeciążenia i łączność telefoniczną. Posadzka garażu jest z polerowanego betonu.',
  'Heiser betjener alle etasjer og forbinder direkte med garasjenivåene, med automatiske dører, overlastdeteksjon og telefonforbindelse. Garasjegulvet er av polert betong.',
  'Hissar går till alla våningar och ansluter direkt till garagenivåerna, med automatiska dörrar, överlastdetektering och telefonförbindelse. Garagegolvet är av polerad betong.')

# ---------------------------------------------------------------- residences
a(87, 'Four kinds of home', 'Cuatro tipos de vivienda, <em>un solo edificio</em>', 'Quatre types de logement, <em>un seul immeuble</em>',
  'Vier Wohnungstypen, <em>ein Gebäude</em>', 'Четыре типа квартир, <em>одно здание</em>', 'أربعة أنواع من المساكن، <em>في مبنى واحد</em>',
  'Vier soorten woningen, <em>één gebouw</em>', 'Cztery rodzaje lokali, <em>jeden budynek</em>', 'Fire typer boliger, <em>én bygning</em>', 'Fyra typer av bostäder, <em>en byggnad</em>')
a(88, 'The nine listed homes fall into four groups',
  'Las nueve viviendas de la lista se dividen en cuatro grupos según su posición en el edificio. La tabla siguiente las incluye todas con sus precios.',
  'Les neuf logements listés se répartissent en quatre groupes selon leur place dans l’immeuble. Le tableau ci-dessous les présente tous avec leurs prix.',
  'Die neun aufgeführten Wohnungen gliedern sich nach ihrer Lage im Gebäude in vier Gruppen. Die Tabelle unten führt alle mit ihren Preisen auf.',
  'Девять квартир из списка делятся на четыре группы по расположению в здании. В таблице ниже приведены все они с ценами.',
  'تنقسم المساكن التسعة المدرجة إلى أربع مجموعات بحسب موقعها في المبنى. ويضم الجدول أدناه جميعها مع أسعارها.',
  'De negen woningen op de lijst vallen in vier groepen naar hun plek in het gebouw. De tabel hieronder toont ze allemaal met hun prijzen.',
  'Dziewięć lokali z listy dzieli się na cztery grupy według położenia w budynku. Poniższa tabela zawiera wszystkie wraz z cenami.',
  'De ni oppførte boligene deles i fire grupper etter plasseringen i bygningen. Tabellen under viser alle med priser.',
  'De nio listade bostäderna delas in i fyra grupper efter läget i byggnaden. Tabellen nedan visar alla med priser.')
a(89, 'Ground floor, with garden and pool', 'Planta baja, con jardín y piscina', 'Rez-de-chaussée, avec jardin et piscine',
  'Erdgeschoss, mit Garten und Pool', 'Первый этаж, с садом и бассейном', 'الطابق الأرضي، بحديقة ومسبح',
  'Begane grond, met tuin en zwembad', 'Parter, z ogrodem i basenem', 'Første etasje, med hage og basseng', 'Bottenvåning, med trädgård och pool')
a(90, 'Four homes on the ground floor have a terrace',
  'Cuatro viviendas de planta baja tienen terraza, jardín privado y una piscina privada de 10 {U} según los planos; una de ellas, la 0D, figura en la lista.',
  'Quatre logements du rez-de-chaussée ont une terrasse, un jardin privé et une piscine privée de 10 {U} d’après les plans ; l’un d’eux, le 0D, est listé.',
  'Vier Erdgeschosswohnungen haben eine Terrasse, einen privaten Garten und laut Plänen einen privaten Pool von 10 {U}; eine davon, die 0D, ist aufgeführt.',
  'У четырёх квартир на первом этаже есть терраса, частный сад и, согласно планам, частный бассейн площадью 10 {U}; одна из них, 0D, есть в списке.',
  'في الطابق الأرضي أربعة مساكن لها تراس وحديقة خاصة ومسبح خاص مساحته 10 {U} بحسب المخططات؛ أحدها، 0D، مدرج في القائمة.',
  'Vier woningen op de begane grond hebben een terras, een privétuin en volgens de plattegronden een privézwembad van 10 {U}; een ervan, 0D, staat op de lijst.',
  'Cztery lokale na parterze mają taras, prywatny ogród i według rzutów prywatny basen o powierzchni 10 {U}; jeden z nich, 0D, jest na liście.',
  'Fire boliger i første etasje har terrasse, privat hage og ifølge tegningene et privat basseng på 10 {U}; én av dem, 0D, er oppført.',
  'Fyra bostäder på bottenvåningen har terrass, privat trädgård och enligt ritningarna en privat pool på 10 {U}; en av dem, 0D, är listad.')
a(91, 'Home 0D has three bedrooms',
  'La vivienda 0D tiene tres dormitorios y dos baños, {N77.32} {U} construidos, una terraza cubierta de {N11.42} {U} y un jardín de {N92.24} {U}.',
  'Le logement 0D a trois chambres et deux salles de bain, {N77.32} {U} construits, une terrasse couverte de {N11.42} {U} et un jardin de {N92.24} {U}.',
  'Die Wohnung 0D hat drei Schlafzimmer und zwei Badezimmer, {N77.32} {U} bebaut, eine überdachte Terrasse von {N11.42} {U} und einen Garten von {N92.24} {U}.',
  'В квартире 0D три спальни и две ванные комнаты, {N77.32} {U} застроенной площади, крытая терраса {N11.42} {U} и сад {N92.24} {U}.',
  'للمسكن 0D ثلاث غرف نوم وحمامان، و{N77.32} {U} مبنية، وتراس مغطى مساحته {N11.42} {U}، وحديقة مساحتها {N92.24} {U}.',
  'Woning 0D heeft drie slaapkamers en twee badkamers, {N77.32} {U} bebouwd, een overdekt terras van {N11.42} {U} en een tuin van {N92.24} {U}.',
  'Lokal 0D ma trzy sypialnie i dwie łazienki, {N77.32} {U} powierzchni zabudowy, zadaszony taras o powierzchni {N11.42} {U} i ogród o powierzchni {N92.24} {U}.',
  'Bolig 0D har tre soverom og to bad, {N77.32} {U} bygd, en overbygd terrasse på {N11.42} {U} og en hage på {N92.24} {U}.',
  'Bostad 0D har tre sovrum och två badrum, {N77.32} {U} byggyta, en övertäckt terrass på {N11.42} {U} och en trädgård på {N92.24} {U}.')
a(92, 'The price is EUR 650,000', 'El precio es de {E650000}.', 'Le prix est de {E650000}.', 'Der Preis beträgt {E650000}.',
  'Цена — {E650000}.', 'السعر {E650000}.', 'De prijs is {E650000}.', 'Cena wynosi {E650000}.', 'Prisen er {E650000}.', 'Priset är {E650000}.')
a(93, 'First to fourth floors', 'De la primera a la cuarta planta', 'Du premier au quatrième étage', 'Erstes bis viertes Obergeschoss',
  'Со второго по пятый этаж', 'من الطابق الأول إلى الرابع', 'Eerste tot vierde verdieping', 'Od pierwszego do czwartego piętra',
  'Andre til femte etasje', 'Första till fjärde våningen')
a(94, 'Five homes with three bedrooms and two bathrooms',
  'Cinco viviendas de tres dormitorios y dos baños: 1C, 2D, 3B, 4B y 4C, de {N81.17} a {N89.11} {U} construidos.',
  'Cinq logements de trois chambres et deux salles de bain : 1C, 2D, 3B, 4B et 4C, de {N81.17} à {N89.11} {U} construits.',
  'Fünf Wohnungen mit drei Schlafzimmern und zwei Badezimmern: 1C, 2D, 3B, 4B und 4C, mit {N81.17} bis {N89.11} {U} bebaut.',
  'Пять квартир с тремя спальнями и двумя ванными комнатами: 1C, 2D, 3B, 4B и 4C, от {N81.17} до {N89.11} {U} застроенной площади.',
  'خمسة مساكن بثلاث غرف نوم وحمامين: 1C وD2 وB3 وB4 وC4، بمساحة مبنية من {N81.17} إلى {N89.11} {U}.',
  'Vijf woningen met drie slaapkamers en twee badkamers: 1C, 2D, 3B, 4B en 4C, van {N81.17} tot {N89.11} {U} bebouwd.',
  'Pięć lokali z trzema sypialniami i dwiema łazienkami: 1C, 2D, 3B, 4B i 4C, o powierzchni zabudowy od {N81.17} do {N89.11} {U}.',
  'Fem boliger med tre soverom og to bad: 1C, 2D, 3B, 4B og 4C, fra {N81.17} til {N89.11} {U} bygd.',
  'Fem bostäder med tre sovrum och två badrum: 1C, 2D, 3B, 4B och 4C, från {N81.17} till {N89.11} {U} byggyta.')
T[todo[94]]['ar'] = 'خمسة مساكن بثلاث غرف نوم وحمامين: 1C و2D و3B و4B و4C، بمساحة مبنية من ' + num('81.17', 'ar') + ' إلى ' + num('89.11', 'ar') + ' ' + UNIT['ar'] + '.'
a(95, 'Terraces of 11.42 to 17.85 sqm', 'Terrazas de {N11.42} a {N17.85} {U}.', 'Terrasses de {N11.42} à {N17.85} {U}.',
  'Terrassen von {N11.42} bis {N17.85} {U}.', 'Террасы от {N11.42} до {N17.85} {U}.', 'تراسات من {N11.42} إلى {N17.85} {U}.',
  'Terrassen van {N11.42} tot {N17.85} {U}.', 'Tarasy od {N11.42} do {N17.85} {U}.', 'Terrasser på {N11.42} til {N17.85} {U}.', 'Terrasser på {N11.42} till {N17.85} {U}.')
a(96, 'Prices run from EUR 549,000 to EUR 665,000',
  'Los precios van de {E549000} a {E665000}.', 'Les prix vont de {E549000} à {E665000}.', 'Die Preise reichen von {E549000} bis {E665000}.',
  'Цены — от {E549000} до {E665000}.', 'تتراوح الأسعار من {E549000} إلى {E665000}.', 'De prijzen lopen van {E549000} tot {E665000}.',
  'Ceny wahają się od {E549000} do {E665000}.', 'Prisene går fra {E549000} til {E665000}.', 'Priserna går från {E549000} till {E665000}.')
a(97, 'Fourth floor, with a private solarium', 'Cuarta planta, con solárium privado', 'Quatrième étage, avec solarium privé',
  'Viertes Obergeschoss, mit privatem Solarium', 'Пятый этаж, с частным солярием', 'الطابق الرابع، بسولاريوم خاص',
  'Vierde verdieping, met privésolarium', 'Czwarte piętro, z prywatnym solarium', 'Femte etasje, med privat solterrasse', 'Fjärde våningen, med privat solterrass')
a(98, 'Homes 4A and 4D have a private solarium',
  'Las viviendas 4A y 4D tienen un solárium privado en la planta superior, al que se accede desde el interior de la vivienda, y una piscina de {N8.94} y {N7.37} {U} según los planos.',
  'Les logements 4A et 4D ont un solarium privé à l’étage supérieur, accessible depuis l’intérieur du logement, et une piscine de {N8.94} et {N7.37} {U} d’après les plans.',
  'Die Wohnungen 4A und 4D haben ein privates Solarium auf der Ebene darüber, vom Inneren der Wohnung aus erreichbar, und laut Plänen einen Pool von {N8.94} bzw. {N7.37} {U}.',
  'У квартир 4A и 4D есть частный солярий на уровне выше, куда можно подняться из квартиры, и, согласно планам, бассейн площадью {N8.94} и {N7.37} {U}.',
  'للمسكنين 4A و4D سولاريوم خاص في الطابق الأعلى يُدخل إليه من داخل المسكن، ومسبح مساحته {N8.94} و{N7.37} {U} بحسب المخططات.',
  'De woningen 4A en 4D hebben een privésolarium op het niveau erboven, bereikbaar vanuit de woning, en volgens de plattegronden een zwembad van {N8.94} en {N7.37} {U}.',
  'Lokale 4A i 4D mają prywatne solarium na poziomie wyżej, dostępne z wnętrza lokalu, oraz według rzutów basen o powierzchni {N8.94} i {N7.37} {U}.',
  'Bolig 4A og 4D har en privat solterrasse i etasjen over, nådd fra innsiden av boligen, og ifølge tegningene et basseng på {N8.94} og {N7.37} {U}.',
  'Bostad 4A och 4D har en privat solterrass på våningen ovanför, nådd inifrån bostaden, och enligt ritningarna en pool på {N8.94} och {N7.37} {U}.')
a(99, '4A has 101.15 sqm built',
  '4A tiene {N101.15} {U} construidos, una terraza de {N20.31} {U} y un solárium de {N19.66} {U}; 4D tiene {N81.17} {U} construidos, una terraza de {N11.42} {U} y un solárium de {N31.65} {U}.',
  '4A compte {N101.15} {U} construits, une terrasse de {N20.31} {U} et un solarium de {N19.66} {U} ; 4D compte {N81.17} {U} construits, une terrasse de {N11.42} {U} et un solarium de {N31.65} {U}.',
  '4A hat {N101.15} {U} bebaut, eine Terrasse von {N20.31} {U} und ein Solarium von {N19.66} {U}; 4D hat {N81.17} {U} bebaut, eine Terrasse von {N11.42} {U} und ein Solarium von {N31.65} {U}.',
  'У 4A {N101.15} {U} застроенной площади, терраса {N20.31} {U} и солярий {N19.66} {U}; у 4D {N81.17} {U} застроенной площади, терраса {N11.42} {U} и солярий {N31.65} {U}.',
  'مساحة 4A المبنية {N101.15} {U} وتراسها {N20.31} {U} وسولاريومها {N19.66} {U}؛ ومساحة 4D المبنية {N81.17} {U} وتراسها {N11.42} {U} وسولاريومها {N31.65} {U}.',
  '4A heeft {N101.15} {U} bebouwd, een terras van {N20.31} {U} en een solarium van {N19.66} {U}; 4D heeft {N81.17} {U} bebouwd, een terras van {N11.42} {U} en een solarium van {N31.65} {U}.',
  '4A ma {N101.15} {U} powierzchni zabudowy, taras o powierzchni {N20.31} {U} i solarium o powierzchni {N19.66} {U}; 4D ma {N81.17} {U} powierzchni zabudowy, taras o powierzchni {N11.42} {U} i solarium o powierzchni {N31.65} {U}.',
  '4A har {N101.15} {U} bygd, en terrasse på {N20.31} {U} og en solterrasse på {N19.66} {U}; 4D har {N81.17} {U} bygd, en terrasse på {N11.42} {U} og en solterrasse på {N31.65} {U}.',
  '4A har {N101.15} {U} byggyta, en terrass på {N20.31} {U} och en solterrass på {N19.66} {U}; 4D har {N81.17} {U} byggyta, en terrass på {N11.42} {U} och en solterrass på {N31.65} {U}.')
a(100, 'Prices are EUR 815,000 and EUR 860,000', 'Los precios son {E815000} y {E860000}.', 'Les prix sont de {E815000} et {E860000}.',
  'Die Preise betragen {E815000} und {E860000}.', 'Цены — {E815000} и {E860000}.', 'السعران {E815000} و{E860000}.',
  'De prijzen zijn {E815000} en {E860000}.', 'Ceny wynoszą {E815000} i {E860000}.', 'Prisene er {E815000} og {E860000}.', 'Priserna är {E815000} och {E860000}.')
a(101, 'Home 5A has three bedrooms',
  'La vivienda 5A tiene tres dormitorios y dos baños, {N95.09} {U} construidos y una terraza de {N17.56} {U} en la quinta planta.',
  'Le logement 5A a trois chambres et deux salles de bain, {N95.09} {U} construits et une terrasse de {N17.56} {U} au cinquième étage.',
  'Die Wohnung 5A hat drei Schlafzimmer und zwei Badezimmer, {N95.09} {U} bebaut und eine Terrasse von {N17.56} {U} im fünften Obergeschoss.',
  'В квартире 5A три спальни и две ванные комнаты, {N95.09} {U} застроенной площади и терраса {N17.56} {U} на шестом этаже.',
  'للمسكن 5A ثلاث غرف نوم وحمامان، و{N95.09} {U} مبنية، وتراس مساحته {N17.56} {U} في الطابق الخامس.',
  'Woning 5A heeft drie slaapkamers en twee badkamers, {N95.09} {U} bebouwd en een terras van {N17.56} {U} op de vijfde verdieping.',
  'Lokal 5A ma trzy sypialnie i dwie łazienki, {N95.09} {U} powierzchni zabudowy i taras o powierzchni {N17.56} {U} na piątym piętrze.',
  'Bolig 5A har tre soverom og to bad, {N95.09} {U} bygd og en terrasse på {N17.56} {U} i sjette etasje.',
  'Bostad 5A har tre sovrum och två badrum, {N95.09} {U} byggyta och en terrass på {N17.56} {U} på femte våningen.')
a(102, 'A private rooftop solarium of 66.04 sqm',
  'Un solárium privado en la cubierta, justo encima, de {N66.04} {U}, con una piscina de {N15.48} {U} según los planos.',
  'Un solarium privé sur le toit, juste au-dessus, de {N66.04} {U}, avec une piscine de {N15.48} {U} d’après les plans.',
  'Ein privates Dachsolarium von {N66.04} {U} darüber hat laut Plänen einen Pool von {N15.48} {U}.',
  'Частный солярий на крыше площадью {N66.04} {U} над квартирой, согласно планам, включает бассейн площадью {N15.48} {U}.',
  'فوقه سولاريوم خاص على السطح مساحته {N66.04} {U} فيه مسبح مساحته {N15.48} {U} بحسب المخططات.',
  'Een privésolarium op het dak van {N66.04} {U} erboven heeft volgens de plattegronden een zwembad van {N15.48} {U}.',
  'Prywatne solarium na dachu o powierzchni {N66.04} {U} nad lokalem ma według rzutów basen o powierzchni {N15.48} {U}.',
  'En privat solterrasse på taket på {N66.04} {U} over boligen har ifølge tegningene et basseng på {N15.48} {U}.',
  'En privat solterrass på taket på {N66.04} {U} ovanför bostaden har enligt ritningarna en pool på {N15.48} {U}.')
a(103, 'The price is EUR 1,050,000', 'El precio es de {E1050000}.', 'Le prix est de {E1050000}.', 'Der Preis beträgt {E1050000}.',
  'Цена — {E1050000}.', 'السعر {E1050000}.', 'De prijs is {E1050000}.', 'Cena wynosi {E1050000}.', 'Prisen er {E1050000}.', 'Priset är {E1050000}.')

# ---------------------------------------------------------------- lifestyle, location
a(104, 'Gardens, terraces', 'Jardines, terrazas <em>y la cubierta</em>', 'Jardins, terrasses <em>et le toit</em>', 'Gärten, Terrassen <em>und das Dach</em>',
  'Сады, террасы <em>и крыша</em>', 'حدائق وتراسات <em>والسطح</em>', 'Tuinen, terrassen <em>en het dak</em>', 'Ogrody, tarasy <em>i dach</em>',
  'Hager, terrasser <em>og taket</em>', 'Trädgårdar, terrasser <em>och taket</em>')
a(105, 'Every home has outdoor space', 'Todas las viviendas tienen espacio exterior, desde un jardín en planta baja hasta un solárium en la cubierta.',
  'Chaque logement dispose d’un espace extérieur, du jardin du rez-de-chaussée au solarium sur le toit.',
  'Jede Wohnung hat Außenbereich, vom Garten im Erdgeschoss bis zum Dachsolarium.',
  'У каждой квартиры есть открытое пространство: от сада на первом этаже до солярия на крыше.',
  'لكل مسكن مساحة خارجية، من حديقة في الطابق الأرضي إلى سولاريوم على السطح.',
  'Elke woning heeft buitenruimte, van een tuin op de begane grond tot een solarium op het dak.',
  'Każdy lokal ma przestrzeń na zewnątrz, od ogrodu na parterze po solarium na dachu.',
  'Alle boliger har uteplass, fra en hage i første etasje til en solterrasse på taket.',
  'Alla bostäder har utomhusyta, från en trädgård på bottenvåningen till en solterrass på taket.')
a(106, 'The ground floor', 'La planta baja', 'Le rez-de-chaussée', 'Das Erdgeschoss', 'Первый этаж', 'الطابق الأرضي', 'De begane grond', 'Parter', 'Første etasje', 'Bottenvåningen')
a(107, 'The ground-floor homes have a terrace',
  'Las viviendas de planta baja tienen terraza, jardín privado y piscina privada.',
  'Les logements du rez-de-chaussée ont une terrasse, un jardin privé et une piscine privée.',
  'Die Erdgeschosswohnungen haben eine Terrasse, einen privaten Garten und einen privaten Pool.',
  'У квартир на первом этаже есть терраса, частный сад и частный бассейн.',
  'للمساكن في الطابق الأرضي تراس وحديقة ومسبح خاصان.',
  'De woningen op de begane grond hebben een terras, een privétuin en een privézwembad.',
  'Lokale na parterze mają taras, prywatny ogród i prywatny basen.',
  'Boligene i første etasje har terrasse, privat hage og privat basseng.',
  'Bostäderna på bottenvåningen har terrass, privat trädgård och privat pool.')
a(108, 'The roof has a communal pool',
  'La cubierta tiene una piscina comunitaria, un solárium y servicios, y las viviendas con solárium privado tienen su propia piscina.',
  'Le toit accueille une piscine commune, un solarium et des services, et les logements avec solarium privé ont leur propre piscine.',
  'Auf dem Dach gibt es einen Gemeinschaftspool, ein Solarium und Servicebereiche, und die Wohnungen mit privatem Solarium haben einen eigenen Pool.',
  'На крыше есть общий бассейн, солярий и служебные помещения, а у квартир с частным солярием — собственный бассейн.',
  'على السطح مسبح مشترك وسولاريوم ومرافق خدمية، وللمساكن ذات السولاريوم الخاص مسبحها الخاص.',
  'Op het dak liggen een gemeenschappelijk zwembad, een solarium en voorzieningen, en de woningen met een privésolarium hebben een eigen zwembad.',
  'Na dachu jest wspólny basen, solarium i zaplecze, a lokale z prywatnym solarium mają własny basen.',
  'På taket er det et felles basseng, en solterrasse og servicearealer, og boligene med privat solterrasse har eget basseng.',
  'På taket finns en gemensam pool, en solterrass och serviceutrymmen, och bostäderna med privat solterrass har egen pool.')
a(109, 'Every home includes a parking space',
  'Todas las viviendas incluyen una plaza de garaje y un trastero en los sótanos, a los que se llega en ascensor.',
  'Chaque logement comprend une place de parking et un débarras aux niveaux de sous-sol, desservis par ascenseur.',
  'Jede Wohnung hat einen Stellplatz und einen Abstellraum in den Untergeschossen, die per Aufzug erreichbar sind.',
  'В каждую квартиру входят парковочное место и кладовая на подземных уровнях, куда можно спуститься на лифте.',
  'يشمل كل مسكن موقف سيارة ومخزناً في الطابقين السفليين، ويُصل إليهما بالمصعد.',
  'Elke woning omvat een parkeerplaats en een berging op de kelderniveaus, bereikbaar met de lift.',
  'Każdy lokal obejmuje miejsce parkingowe i komórkę na poziomach podziemnych, dostępne windą.',
  'Hver bolig inkluderer en parkeringsplass og en bod i kjelleretasjene, nådd med heis.',
  'Varje bostad inkluderar en parkeringsplats och ett förråd på källarplanen, nåbara med hiss.')
a(110, 'The climate', 'El clima', 'Le climat', 'Das Klima', 'Климат', 'المناخ', 'Het klimaat', 'Klimat', 'Klimaet', 'Klimatet')
a(111, 'The brochure counts more than 300 days',
  'El folleto cuenta más de 300 días de sol al año en la Costa del Sol.',
  'La brochure compte plus de 300 jours de soleil par an sur la Costa del Sol.',
  'Der Prospekt nennt mehr als 300 Sonnentage im Jahr an der Costa del Sol.',
  'В брошюре сказано, что на Коста-дель-Соль более 300 солнечных дней в году.',
  'يذكر الكتيّب أكثر من 300 يوم مشمس في السنة على كوستا ديل سول.',
  'De brochure telt meer dan 300 zonnedagen per jaar aan de Costa del Sol.',
  'Broszura podaje ponad 300 słonecznych dni w roku na Costa del Sol.',
  'Brosjyren oppgir mer enn 300 soldager i året på Costa del Sol.',
  'Broschyren anger mer än 300 soldagar om året på Costa del Sol.')
a(112, 'Estepona, <em>under ten minutes',
  'Estepona, <em>a menos de diez minutos del puerto deportivo y de la playa</em>', 'Estepona, <em>à moins de dix minutes du port de plaisance et de la plage</em>',
  'Estepona, <em>weniger als zehn Minuten vom Yachthafen und vom Strand</em>', 'Эстепона, <em>менее десяти минут до порта и пляжа</em>',
  'إستيبونا، <em>على بعد أقل من عشر دقائق من المرسى والشاطئ</em>', 'Estepona, <em>op minder dan tien minuten van de jachthaven en het strand</em>',
  'Estepona, <em>mniej niż dziesięć minut od portu jachtowego i plaży</em>', 'Estepona, <em>under ti minutter fra småbåthavnen og stranden</em>',
  'Estepona, <em>under tio minuter från småbåtshamnen och stranden</em>')
a(113, 'The building is in one of Estepona’s residential areas',
  'El edificio está en una de las zonas residenciales de Estepona, cerca del casco histórico y de la A-7 y la AP-7. El folleto del promotor sitúa el puerto deportivo de Estepona y la playa de La Rada a menos de diez minutos, con comercios, supermercados, colegios e instalaciones deportivas cerca, y acceso directo a Málaga y a su aeropuerto.',
  'L’immeuble se trouve dans l’un des quartiers résidentiels d’Estepona, près du centre historique et de l’A-7 et de l’AP-7. La brochure du promoteur place le port de plaisance d’Estepona et la plage de La Rada à moins de dix minutes, avec commerces, supermarchés, écoles et équipements sportifs à proximité, et un accès direct à Málaga et à son aéroport.',
  'Das Gebäude liegt in einem der Wohngebiete von Estepona, nahe der historischen Altstadt sowie der A-7 und der AP-7. Laut Prospekt des Bauträgers sind der Yachthafen von Estepona und der Strand La Rada in weniger als zehn Minuten erreichbar; Geschäfte, Supermärkte, Schulen und Sportanlagen sind in der Nähe, und es gibt eine direkte Verbindung nach Málaga und zu seinem Flughafen.',
  'Здание находится в одном из жилых районов Эстепоны, недалеко от исторического центра и автомагистралей A-7 и AP-7. По данным брошюры застройщика, порт Эстепоны и пляж Ла-Рада расположены менее чем в десяти минутах; рядом магазины, супермаркеты, школы и спортивные объекты, а также прямой выезд на Малагу и её аэропорт.',
  'يقع المبنى في أحد الأحياء السكنية في إستيبونا، قرب المركز التاريخي والطريقين A-7 وAP-7. ويضع كتيّب المطوّر مرسى إستيبونا وشاطئ لا رادا على بعد أقل من عشر دقائق، مع متاجر وسوبرماركت ومدارس ومرافق رياضية قريبة، ووصول مباشر إلى مالقة ومطارها.',
  'Het gebouw ligt in een van de woonwijken van Estepona, dicht bij het historische centrum en bij de A-7 en de AP-7. Volgens de brochure van de ontwikkelaar liggen de jachthaven van Estepona en het strand van La Rada op minder dan tien minuten, met winkels, supermarkten, scholen en sportvoorzieningen in de buurt en een directe verbinding met Málaga en de luchthaven.',
  'Budynek stoi w jednej z dzielnic mieszkalnych Estepony, blisko historycznego centrum oraz autostrad A-7 i AP-7. Według broszury dewelopera port jachtowy w Esteponie i plaża La Rada są oddalone o mniej niż dziesięć minut, w pobliżu są sklepy, supermarkety, szkoły i obiekty sportowe, a do Malagi i jej lotniska jest bezpośredni dojazd.',
  'Bygningen ligger i et av boligområdene i Estepona, nær det historiske sentrum og A-7 og AP-7. Utbyggerens brosjyre oppgir at småbåthavnen i Estepona og La Rada-stranden ligger under ti minutter unna, med butikker, supermarkeder, skoler og idrettsanlegg i nærheten og direkte tilgang til Málaga og flyplassen.',
  'Byggnaden ligger i ett av Esteponas bostadsområden, nära det historiska centrumet och A-7 och AP-7. Exploatörens broschyr anger att Esteponas småbåtshamn och stranden La Rada ligger under tio minuter bort, med butiker, snabbköp, skolor och idrottsanläggningar i närheten och direkt förbindelse till Málaga och dess flygplats.')
a(114, 'Estepona, <em>near the centre', 'Estepona, <em>cerca del centro</em>', 'Estepona, <em>près du centre</em>', 'Estepona, <em>nahe dem Zentrum</em>',
  'Эстепона, <em>недалеко от центра</em>', 'إستيبونا، <em>قرب الوسط</em>', 'Estepona, <em>nabij het centrum</em>', 'Estepona, <em>blisko centrum</em>',
  'Estepona, <em>nær sentrum</em>', 'Estepona, <em>nära centrum</em>')
a(115, 'Estepona, near the centre', 'Estepona, cerca del centro', 'Estepona, près du centre', 'Estepona, nahe dem Zentrum',
  'Эстепона, недалеко от центра', 'إستيبونا، قرب الوسط', 'Estepona, nabij het centrum', 'Estepona, blisko centrum', 'Estepona, nær sentrum', 'Estepona, nära centrum')
a(116, 'Estepona marina', 'Puerto deportivo de Estepona', 'Port de plaisance d’Estepona', 'Yachthafen von Estepona', 'Порт Эстепоны',
  'مرسى إستيبونا', 'Jachthaven van Estepona', 'Port jachtowy w Esteponie', 'Småbåthavnen i Estepona', 'Esteponas småbåtshamn')
a(117, 'La Rada beach', 'Playa de La Rada', 'Plage de La Rada', 'Strand La Rada', 'Пляж Ла-Рада', 'شاطئ لا رادا', 'Strand van La Rada', 'Plaża La Rada', 'La Rada-stranden', 'Stranden La Rada')

# ---------------------------------------------------------------- investment, trust dossier, availability
a(118, 'The documents we hold do not set out',
  'Los documentos de que disponemos no recogen las condiciones del promotor, así que las confirmamos por escrito antes de que reserve.',
  'Les documents dont nous disposons ne précisent pas les conditions du promoteur ; nous les confirmons par écrit avant que vous ne réserviez.',
  'Die uns vorliegenden Unterlagen enthalten die Bedingungen des Bauträgers nicht; wir bestätigen sie Ihnen schriftlich, bevor Sie reservieren.',
  'В имеющихся у нас документах условий застройщика нет, поэтому мы подтверждаем их письменно до того, как вы забронируете.',
  'لا تتضمن الوثائق التي بين أيدينا شروط المطوّر، لذا نؤكدها لكم كتابةً قبل أن تحجزوا.',
  'In de documenten waarover wij beschikken staan de voorwaarden van de ontwikkelaar niet; wij bevestigen ze schriftelijk voordat u reserveert.',
  'Dokumenty, którymi dysponujemy, nie zawierają warunków dewelopera, dlatego potwierdzamy je Państwu na piśmie przed rezerwacją.',
  'Dokumentene vi har, oppgir ikke utbyggerens vilkår, så vi bekrefter dem skriftlig før en eventuell reservasjon.',
  'De handlingar vi har anger inte exploatörens villkor, så vi bekräftar dem skriftligt innan ni reserverar.')
a(119, 'Reservation and payment schedule', 'Reserva y calendario de pagos', 'Réservation et échéancier de paiement', 'Reservierung und Zahlungsplan',
  'Бронирование и график платежей', 'الحجز وجدول الدفعات', 'Reservering en betalingsschema', 'Rezerwacja i harmonogram płatności',
  'Reservasjon og betalingsplan', 'Reservation och betalningsplan')
a(120, 'The documents we hold give no reservation amount',
  'Los documentos de que disponemos no indican el importe de la reserva ni el calendario de pagos. Obtenemos las condiciones del promotor y se las enviamos por escrito antes de que reserve.',
  'Les documents dont nous disposons n’indiquent ni le montant de la réservation ni l’échéancier de paiement. Nous obtenons les conditions du promoteur et vous les envoyons par écrit avant que vous ne réserviez.',
  'Die uns vorliegenden Unterlagen nennen weder einen Reservierungsbetrag noch einen Zahlungsplan. Wir holen die Bedingungen des Bauträgers ein und senden sie Ihnen schriftlich, bevor Sie reservieren.',
  'В имеющихся у нас документах нет ни суммы бронирования, ни графика платежей. Мы получаем условия застройщика и присылаем их вам письменно до того, как вы забронируете.',
  'لا تذكر الوثائق التي بين أيدينا مبلغ الحجز ولا جدول الدفعات. نحصل على شروط المطوّر ونرسلها إليكم كتابةً قبل أن تحجزوا.',
  'In de documenten waarover wij beschikken staan geen reserveringsbedrag en geen betalingsschema. Wij vragen de voorwaarden van de ontwikkelaar op en sturen ze u schriftelijk toe voordat u reserveert.',
  'Dokumenty, którymi dysponujemy, nie podają kwoty rezerwacji ani harmonogramu płatności. Uzyskujemy warunki dewelopera i przesyłamy je Państwu na piśmie przed rezerwacją.',
  'Dokumentene vi har, oppgir verken reservasjonsbeløp eller betalingsplan. Vi innhenter utbyggerens vilkår og sender dem skriftlig før en eventuell reservasjon.',
  'De handlingar vi har anger varken något reservationsbelopp eller någon betalningsplan. Vi inhämtar exploatörens villkor och skickar dem skriftligt till er innan ni reserverar.')
a(121, 'VAT and taxes', 'IVA e impuestos', 'TVA et taxes', 'MwSt. und Steuern', 'НДС и налоги', 'ضريبة القيمة المضافة والضرائب', 'Btw en belastingen', 'VAT i podatki', 'Mva. og skatter', 'Moms och skatter')
a(122, 'The price list does not say whether VAT is included. Nueva Living',
  'La lista de precios no indica si el IVA está incluido. Nueva Living confirma por escrito los impuestos y los gastos de compra.',
  'La liste de prix n’indique pas si la TVA est incluse. Nueva Living confirme par écrit les taxes et les frais d’achat.',
  'Die Preisliste sagt nicht, ob die MwSt. enthalten ist. Nueva Living bestätigt die Steuern und Kaufnebenkosten schriftlich.',
  'В прайс-листе не указано, включён ли НДС. Nueva Living письменно подтверждает налоги и расходы на покупку.',
  'لا تذكر قائمة الأسعار ما إذا كانت ضريبة القيمة المضافة مشمولة. وتؤكد Nueva Living الضرائب وتكاليف الشراء كتابةً.',
  'De prijslijst vermeldt niet of btw is inbegrepen. Nueva Living bevestigt de belastingen en aankoopkosten schriftelijk.',
  'Cennik nie podaje, czy VAT jest wliczony. Nueva Living potwierdza na piśmie podatki i koszty zakupu.',
  'Prislisten oppgir ikke om mva. er inkludert. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.',
  'Prislistan anger inte om moms ingår. Nueva Living bekräftar skatter och köpkostnader skriftligt.')
a(123, 'The brochure says every home includes a parking space',
  'El folleto indica que todas las viviendas incluyen una plaza de garaje y un trastero en los sótanos. Confirmamos la plaza y el trastero de la vivienda que elija.',
  'La brochure indique que chaque logement comprend une place de parking et un débarras aux niveaux de sous-sol. Nous confirmons la place et le débarras du logement que vous choisissez.',
  'Laut Prospekt hat jede Wohnung einen Stellplatz und einen Abstellraum in den Untergeschossen. Wir bestätigen Stellplatz und Abstellraum der von Ihnen gewählten Wohnung.',
  'В брошюре сказано, что в каждую квартиру входят парковочное место и кладовая на подземных уровнях. Мы подтверждаем место и кладовую выбранной вами квартиры.',
  'يذكر الكتيّب أن كل مسكن يشمل موقف سيارة ومخزناً في الطابقين السفليين. نؤكد الموقف والمخزن الخاصين بالمسكن الذي تختارونه.',
  'Volgens de brochure omvat elke woning een parkeerplaats en een berging op de kelderniveaus. Wij bevestigen de plaats en de berging van de woning die u kiest.',
  'Według broszury każdy lokal obejmuje miejsce parkingowe i komórkę na poziomach podziemnych. Potwierdzamy miejsce i komórkę wybranego przez Państwa lokalu.',
  'Brosjyren sier at hver bolig inkluderer en parkeringsplass og en bod i kjelleretasjene. Vi bekrefter plassen og boden til boligen som velges.',
  'Broschyren anger att varje bostad inkluderar en parkeringsplats och ett förråd på källarplanen. Vi bekräftar platsen och förrådet för den bostad ni väljer.')
a(124, 'The quality specification says the materials may be changed',
  'La memoria de calidades indica que la dirección facultativa puede modificar los materiales y que no es contractual. Solicitamos la memoria de calidades definitiva.',
  'Le descriptif de qualité indique que la direction des travaux peut modifier les matériaux et qu’il n’est pas contractuel. Nous demandons le descriptif définitif.',
  'Die Baubeschreibung besagt, dass die Bauleitung die Materialien ändern darf und dass sie nicht vertraglich bindend ist. Wir fordern die endgültige Baubeschreibung an.',
  'В спецификации качества сказано, что руководство проекта может менять материалы и что она не носит договорного характера. Мы запрашиваем окончательную спецификацию.',
  'تنص مواصفات الجودة على أن إدارة المشروع قد تغيّر المواد وأنها غير ملزمة تعاقدياً. نطلب المواصفات النهائية.',
  'Het lastenboek stelt dat de projectleiding de materialen mag wijzigen en dat het niet contractueel is. Wij vragen het definitieve lastenboek op.',
  'Specyfikacja jakości zastrzega, że kierownictwo projektu może zmieniać materiały i że nie ma charakteru umownego. Prosimy o ostateczną specyfikację.',
  'Kvalitetsbeskrivelsen sier at prosjektledelsen kan endre materialene, og at den ikke er kontraktsfestet. Vi ber om den endelige beskrivelsen.',
  'Kvalitetsbeskrivningen anger att projektledningen får ändra materialen och att den inte är avtalsbunden. Vi begär den slutliga beskrivningen.')
a(125, 'The documents we hold do not say whether the building licence',
  'Los documentos de que disponemos no indican si la licencia de obras está concedida ni si las obras han empezado, y la memoria de calidades está redactada en futuro. Solicitamos la licencia, su estado y la fecha de inicio de las obras.',
  'Les documents dont nous disposons n’indiquent pas si le permis de construire est accordé ni si les travaux ont commencé, et le descriptif de qualité est rédigé au futur. Nous demandons le permis, son état et la date de début des travaux.',
  'Die uns vorliegenden Unterlagen sagen nicht, ob die Baugenehmigung erteilt wurde oder ob die Bauarbeiten begonnen haben, und die Baubeschreibung ist im Futur verfasst. Wir fordern die Genehmigung, ihren Stand und den Baubeginn an.',
  'В имеющихся у нас документах не сказано, получено ли разрешение на строительство и начаты ли работы, а спецификация качества написана в будущем времени. Мы запрашиваем разрешение, его статус и дату начала работ.',
  'لا تذكر الوثائق التي بين أيدينا ما إذا كانت رخصة البناء قد مُنحت أو ما إذا بدأت الأعمال، ومواصفات الجودة مكتوبة بصيغة المستقبل. نطلب الرخصة وحالتها وتاريخ بدء الأعمال.',
  'In de documenten waarover wij beschikken staat niet of de bouwvergunning is verleend of dat de werken zijn gestart, en het lastenboek is in de toekomende tijd geschreven. Wij vragen de vergunning, de status ervan en de startdatum van de werken op.',
  'Dokumenty, którymi dysponujemy, nie mówią, czy pozwolenie na budowę zostało wydane ani czy prace się rozpoczęły, a specyfikacja jakości jest napisana w czasie przyszłym. Prosimy o pozwolenie, jego status i datę rozpoczęcia prac.',
  'Dokumentene vi har, sier ikke om byggetillatelsen er gitt eller om arbeidene har startet, og kvalitetsbeskrivelsen er skrevet i futurum. Vi ber om tillatelsen, status for den og startdatoen for arbeidene.',
  'De handlingar vi har anger inte om bygglovet har beviljats eller om arbetena har påbörjats, och kvalitetsbeskrivningen är skriven i futurum. Vi begär bygglovet, dess status och startdatum för arbetena.')
a(126, 'None of the developer’s documents gives a completion date',
  'Ninguno de los documentos del promotor indica una fecha de entrega, así que solicitamos la fecha contractual antes de cualquier reserva.',
  'Aucun des documents du promoteur n’indique de date de livraison ; nous demandons la date contractuelle avant toute réservation.',
  'Keines der Dokumente des Bauträgers nennt einen Fertigstellungstermin; wir fordern vor jeder Reservierung den vertraglichen Termin an.',
  'Ни в одном из документов застройщика не указан срок сдачи, поэтому перед любым бронированием мы запрашиваем договорную дату.',
  'لا تذكر أي من وثائق المطوّر موعداً للتسليم، لذا نطلب الموعد التعاقدي قبل أي حجز.',
  'In geen van de documenten van de ontwikkelaar staat een opleverdatum; wij vragen de contractuele datum op vóór elke reservering.',
  'W żadnym z dokumentów dewelopera nie ma terminu oddania, dlatego przed każdą rezerwacją prosimy o termin umowny.',
  'Ingen av utbyggerens dokumenter oppgir en overleveringsdato, så vi ber om den kontraktsfestede datoen før en eventuell reservasjon.',
  'Inget av exploatörens dokument anger ett tillträdesdatum, så vi begär det avtalade datumet före varje reservation.')
a(127, 'The price list gives the built area of each home',
  'La lista de precios da la superficie construida de cada vivienda y una cifra de terraza; en las viviendas 4A, 4D y 5A esa cifra es la terraza y el solárium juntos. Los planos dan además una superficie útil y una superficie construida mayor según el Decreto 218/2005: {N83.82} y {N103.15} {U} para la vivienda 1C, frente a {N87.13} {U} en la lista de precios. Confirmamos qué cifra utiliza el contrato.',
  'La liste de prix donne la surface construite de chaque logement et un chiffre de terrasse ; pour les logements 4A, 4D et 5A, ce chiffre réunit la terrasse et le solarium. Les plans donnent aussi une surface utile et une surface construite plus grande selon le décret 218/2005 : {N83.82} et {N103.15} {U} pour le logement 1C, contre {N87.13} {U} sur la liste de prix. Nous confirmons quel chiffre retient le contrat.',
  'Die Preisliste nennt die bebaute Fläche jeder Wohnung und einen Terrassenwert; bei den Wohnungen 4A, 4D und 5A umfasst dieser Wert Terrasse und Solarium zusammen. Die Pläne geben außerdem eine Nutzfläche und eine größere bebaute Fläche nach dem Dekret 218/2005 an: {N83.82} und {N103.15} {U} für die Wohnung 1C gegenüber {N87.13} {U} in der Preisliste. Wir klären, welcher Wert im Vertrag gilt.',
  'В прайс-листе указана застроенная площадь каждой квартиры и площадь террасы; для квартир 4A, 4D и 5A это терраса и солярий вместе. На планах также указаны полезная площадь и большая застроенная площадь по декрету 218/2005: {N83.82} и {N103.15} {U} для квартиры 1C против {N87.13} {U} в прайс-листе. Мы уточняем, какая цифра используется в договоре.',
  'تذكر قائمة الأسعار المساحة المبنية لكل مسكن ورقماً للتراس؛ وفي المساكن 4A و4D و5A يجمع هذا الرقم التراس والسولاريوم معاً. وتذكر المخططات أيضاً مساحة صالحة للاستخدام ومساحة مبنية أكبر بموجب المرسوم 218/2005: {N83.82} و{N103.15} {U} للمسكن 1C مقابل {N87.13} {U} في قائمة الأسعار. نؤكد أي رقم يعتمده العقد.',
  'De prijslijst geeft de bebouwde oppervlakte van elke woning en een terrascijfer; bij de woningen 4A, 4D en 5A is dat cijfer het terras en het solarium samen. De plattegronden geven daarnaast een bruikbare oppervlakte en een grotere bebouwde oppervlakte volgens decreet 218/2005: {N83.82} en {N103.15} {U} voor woning 1C, tegenover {N87.13} {U} in de prijslijst. Wij bevestigen welk cijfer het contract hanteert.',
  'Cennik podaje powierzchnię zabudowy każdego lokalu i wartość tarasu; w lokalach 4A, 4D i 5A jest to taras razem z solarium. Rzuty podają też powierzchnię użytkową i większą powierzchnię zabudowy według dekretu 218/2005: {N83.82} i {N103.15} {U} dla lokalu 1C wobec {N87.13} {U} w cenniku. Potwierdzamy, którą wartość przyjmuje umowa.',
  'Prislisten oppgir bygd areal for hver bolig og et terrassetall; for boligene 4A, 4D og 5A er tallet terrassen og solterrassen til sammen. Tegningene oppgir i tillegg et bruksareal og et større bygd areal etter dekret 218/2005: {N83.82} og {N103.15} {U} for bolig 1C mot {N87.13} {U} i prislisten. Vi bekrefter hvilket tall kontrakten bruker.',
  'Prislistan anger byggytan för varje bostad och en terrassiffra; för bostäderna 4A, 4D och 5A är siffran terrassen och solterrassen tillsammans. Ritningarna anger dessutom en boyta och en större byggyta enligt dekret 218/2005: {N83.82} och {N103.15} {U} för bostad 1C mot {N87.13} {U} i prislistan. Vi bekräftar vilken siffra avtalet använder.')
a(128, 'Prices and VAT', 'Precios e IVA', 'Prix et TVA', 'Preise und MwSt.', 'Цены и НДС', 'الأسعار وضريبة القيمة المضافة', 'Prijzen en btw', 'Ceny i VAT', 'Priser og mva.', 'Priser och moms')
a(129, 'The price list gives amounts in euros',
  'La lista de precios da los importes en euros y no indica si el IVA está incluido ni cuál es el calendario de pagos. Confirmamos ambos puntos por escrito.',
  'La liste de prix donne les montants en euros et n’indique ni si la TVA est incluse, ni l’échéancier de paiement. Nous confirmons les deux par écrit.',
  'Die Preisliste nennt Beträge in Euro und sagt weder, ob die MwSt. enthalten ist, noch, wie der Zahlungsplan aussieht. Wir bestätigen beides schriftlich.',
  'В прайс-листе суммы указаны в евро, но не сказано, включён ли НДС и каков график платежей. Мы письменно подтверждаем и то и другое.',
  'تذكر قائمة الأسعار المبالغ باليورو ولا تذكر ما إذا كانت ضريبة القيمة المضافة مشمولة ولا ما هو جدول الدفعات. نؤكد الأمرين كتابةً.',
  'De prijslijst geeft bedragen in euro en vermeldt niet of btw is inbegrepen of wat het betalingsschema is. Wij bevestigen beide schriftelijk.',
  'Cennik podaje kwoty w euro i nie mówi, czy VAT jest wliczony ani jaki jest harmonogram płatności. Potwierdzamy oba punkty na piśmie.',
  'Prislisten oppgir beløp i euro og sier ikke om mva. er inkludert eller hva betalingsplanen er. Vi bekrefter begge deler skriftlig.',
  'Prislistan anger belopp i euro och säger inte om moms ingår eller hur betalningsplanen ser ut. Vi bekräftar båda skriftligt.')
a(130, 'Nine homes <em>currently listed', 'Nueve viviendas <em>actualmente en la lista</em>', 'Neuf logements <em>actuellement listés</em>',
  'Neun Wohnungen <em>derzeit aufgeführt</em>', 'Девять квартир <em>сейчас в списке</em>', 'تسعة مساكن <em>مدرجة حالياً</em>',
  'Negen woningen <em>momenteel op de lijst</em>', 'Dziewięć lokali <em>obecnie na liście</em>', 'Ni boliger <em>oppført nå</em>', 'Nio bostäder <em>listade just nu</em>')
a(131, 'Prices are those of the developer’s price list as of October 2026',
  'Los precios son los de la lista de precios del promotor a octubre de 2026 y se confirman antes de la reserva. Nueve de las 22 viviendas figuran en la lista, todas con tres dormitorios y dos baños; los documentos del promotor no dicen que las otras 13 estén vendidas.',
  'Les prix sont ceux de la liste de prix du promoteur à octobre 2026 et sont confirmés avant la réservation. Neuf des 22 logements sont listés, tous avec trois chambres et deux salles de bain ; les documents du promoteur ne disent pas que les 13 autres sont vendus.',
  'Die Preise stammen aus der Preisliste des Bauträgers mit Stand Oktober 2026 und werden vor der Reservierung bestätigt. Neun der 22 Wohnungen sind aufgeführt, alle mit drei Schlafzimmern und zwei Badezimmern; die Unterlagen des Bauträgers sagen nicht, dass die übrigen 13 verkauft sind.',
  'Цены взяты из прайс-листа застройщика на октябрь 2026 года и подтверждаются перед бронированием. В списке девять из 22 квартир, все с тремя спальнями и двумя ванными комнатами; в документах застройщика не сказано, что остальные 13 проданы.',
  'الأسعار هي أسعار قائمة المطوّر في أكتوبر 2026 وتُؤكَّد قبل الحجز. تسعة من المساكن الاثنين والعشرين مدرجة، وكلها بثلاث غرف نوم وحمامين؛ ولا تذكر وثائق المطوّر أن الثلاثة عشر الباقية مباعة.',
  'De prijzen komen uit de prijslijst van de ontwikkelaar per oktober 2026 en worden vóór de reservering bevestigd. Negen van de 22 woningen staan op de lijst, allemaal met drie slaapkamers en twee badkamers; de documenten van de ontwikkelaar zeggen niet dat de andere 13 verkocht zijn.',
  'Ceny pochodzą z cennika dewelopera z października 2026 r. i są potwierdzane przed rezerwacją. Dziewięć z 22 lokali jest na liście, wszystkie z trzema sypialniami i dwiema łazienkami; dokumenty dewelopera nie mówią, że pozostałe 13 jest sprzedanych.',
  'Prisene er fra utbyggerens prisliste per oktober 2026 og bekreftes før reservasjon. Ni av de 22 boligene er oppført, alle med tre soverom og to bad; utbyggerens dokumenter sier ikke at de øvrige 13 er solgt.',
  'Priserna kommer från exploatörens prislista per oktober 2026 och bekräftas före reservation. Nio av de 22 bostäderna är listade, alla med tre sovrum och två badrum; exploatörens handlingar säger inte att de övriga 13 är sålda.')
a(132, 'Prices, built areas and terraces are transcribed',
  'Los precios, las superficies construidas y las terrazas se han transcrito de la lista de precios del promotor tal como figura en su portal en octubre de 2026. La lista no indica si el IVA está incluido. Para las viviendas 4A, 4D y 5A la lista da la terraza y el solárium privado como una sola cifra ({N39.97}, {N43.07} y {N83.60} {U}); la tabla los muestra por separado, como hacen los planos. Los planos dan además una superficie útil y una superficie construida según el Decreto 218/2005, que difieren de la superficie construida de la lista.',
  'Les prix, surfaces construites et terrasses sont transcrits de la liste de prix du promoteur telle qu’elle figure sur son portail en octobre 2026. La liste n’indique pas si la TVA est incluse. Pour les logements 4A, 4D et 5A, la liste donne la terrasse et le solarium privé en un seul chiffre ({N39.97}, {N43.07} et {N83.60} {U}) ; le tableau les présente séparément, comme les plans. Les plans donnent aussi une surface utile et une surface construite selon le décret 218/2005, qui diffèrent de la surface construite de la liste.',
  'Preise, bebaute Flächen und Terrassen sind aus der Preisliste des Bauträgers übernommen, wie sie im Oktober 2026 auf seinem Portal stand. Die Liste sagt nicht, ob die MwSt. enthalten ist. Für die Wohnungen 4A, 4D und 5A nennt die Liste Terrasse und privates Solarium als einen Wert ({N39.97}, {N43.07} und {N83.60} {U}); die Tabelle zeigt sie getrennt, wie die Pläne. Die Pläne geben außerdem eine Nutzfläche und eine bebaute Fläche nach dem Dekret 218/2005 an, die von der bebauten Fläche der Liste abweichen.',
  'Цены, застроенные площади и террасы перенесены из прайс-листа застройщика в том виде, в каком он был размещён на его портале в октябре 2026 года. В списке не указано, включён ли НДС. Для квартир 4A, 4D и 5A в прайс-листе терраса и частный солярий даны одной цифрой ({N39.97}, {N43.07} и {N83.60} {U}); в таблице они показаны отдельно, как на планах. На планах также указаны полезная площадь и застроенная площадь по декрету 218/2005, отличающиеся от застроенной площади в прайс-листе.',
  'نُقلت الأسعار والمساحات المبنية والتراسات من قائمة أسعار المطوّر كما ظهرت على بوابته في أكتوبر 2026. ولا تذكر القائمة ما إذا كانت ضريبة القيمة المضافة مشمولة. وفي المساكن 4A و4D و5A تعطي القائمة التراس والسولاريوم الخاص رقماً واحداً ({N39.97} و{N43.07} و{N83.60} {U})؛ ويعرضهما الجدول منفصلين كما تفعل المخططات. وتذكر المخططات أيضاً مساحة صالحة للاستخدام ومساحة مبنية بموجب المرسوم 218/2005 تختلفان عن المساحة المبنية في القائمة.',
  'De prijzen, bebouwde oppervlakten en terrassen zijn overgenomen uit de prijslijst van de ontwikkelaar zoals die in oktober 2026 op zijn portaal stond. De lijst vermeldt niet of btw is inbegrepen. Voor de woningen 4A, 4D en 5A geeft de lijst het terras en het privésolarium als één cijfer ({N39.97}, {N43.07} en {N83.60} {U}); de tabel toont ze apart, zoals de plattegronden. De plattegronden geven daarnaast een bruikbare oppervlakte en een bebouwde oppervlakte volgens decreet 218/2005, die afwijken van de bebouwde oppervlakte op de lijst.',
  'Ceny, powierzchnie zabudowy i tarasy zostały przepisane z cennika dewelopera widocznego na jego portalu w październiku 2026 r. Cennik nie podaje, czy VAT jest wliczony. Dla lokali 4A, 4D i 5A cennik podaje taras i prywatne solarium jako jedną wartość ({N39.97}, {N43.07} i {N83.60} {U}); tabela pokazuje je osobno, tak jak rzuty. Rzuty podają też powierzchnię użytkową i powierzchnię zabudowy według dekretu 218/2005, które różnią się od powierzchni zabudowy z cennika.',
  'Priser, bygde arealer og terrasser er hentet fra utbyggerens prisliste slik den sto på portalen hans i oktober 2026. Listen oppgir ikke om mva. er inkludert. For boligene 4A, 4D og 5A oppgir listen terrassen og den private solterrassen som ett tall ({N39.97}, {N43.07} og {N83.60} {U}); tabellen viser dem hver for seg, slik tegningene gjør. Tegningene oppgir i tillegg et bruksareal og et bygd areal etter dekret 218/2005, som avviker fra det bygde arealet i listen.',
  'Priser, byggytor och terrasser är hämtade från exploatörens prislista så som den stod på hans portal i oktober 2026. Listan anger inte om moms ingår. För bostäderna 4A, 4D och 5A anger listan terrassen och den privata solterrassen som en siffra ({N39.97}, {N43.07} och {N83.60} {U}); tabellen visar dem var för sig, som ritningarna gör. Ritningarna anger dessutom en boyta och en byggyta enligt dekret 218/2005, som avviker från byggytan i listan.')

# ---------------------------------------------------------------- timeline, viewing, enquiry, FAQ
a(152, 'See the area with us, and the plans against the stage',
  'Conozca la zona con nosotros y compare los planos con el estado de las obras.',
  'Découvrez le quartier avec nous et comparez les plans à l’état d’avancement des travaux.',
  'Sehen Sie sich mit uns die Umgebung an und vergleichen Sie die Pläne mit dem Stand der Bauarbeiten.',
  'Осмотрите район вместе с нами и сверьте планы с ходом работ.',
  'تعرّفوا على المنطقة معنا وقارنوا المخططات بمرحلة الأعمال.',
  'Bekijk de omgeving met ons en leg de plattegronden naast de stand van de werken.',
  'Zobaczą Państwo okolicę razem z nami i porównają rzuty ze stanem prac.',
  'Se området sammen med oss, og sammenlign tegningene med hvor langt arbeidene har kommet.',
  'Se området tillsammans med oss och jämför ritningarna med hur långt arbetena har kommit.')
a(153, 'We confirm the reservation terms',
  'Confirmamos por escrito las condiciones de reserva y el calendario de pagos, y después el contrato privado de compraventa.',
  'Nous confirmons par écrit les conditions de réservation et l’échéancier de paiement, puis le contrat d’achat privé.',
  'Wir bestätigen die Reservierungsbedingungen und den Zahlungsplan schriftlich, danach folgt der private Kaufvertrag.',
  'Мы письменно подтверждаем условия бронирования и график платежей, затем следует частный договор купли-продажи.',
  'نؤكد كتابةً شروط الحجز وجدول الدفعات، ثم يأتي عقد الشراء الخاص.',
  'Wij bevestigen de reserveringsvoorwaarden en het betalingsschema schriftelijk, daarna volgt het onderhandse koopcontract.',
  'Potwierdzamy na piśmie warunki rezerwacji i harmonogram płatności, a następnie następuje prywatna umowa kupna.',
  'Vi bekrefter reservasjonsvilkårene og betalingsplanen skriftlig, deretter følger den private kjøpskontrakten.',
  'Vi bekräftar reservationsvillkoren och betalningsplanen skriftligt, därefter följer det privata köpeavtalet.')
a(154, 'See the <em>area and the plans', 'Conozca <em>la zona y los planos</em>', 'Découvrez <em>le quartier et les plans</em>',
  'Sehen Sie sich <em>die Umgebung und die Pläne</em> an', 'Осмотрите <em>район и планы</em>', 'تعرّفوا على <em>المنطقة والمخططات</em>',
  'Bekijk <em>de omgeving en de plattegronden</em>', 'Zobacz <em>okolicę i rzuty</em>', 'Se <em>området og tegningene</em>', 'Se <em>området och ritningarna</em>')
T[todo[154]]['pl'] = 'Zobaczą Państwo <em>okolicę i rzuty</em>'
a(155, 'A visit is about the location',
  'Una visita trata de la ubicación, los planos y el estado de las obras.',
  'Une visite porte sur l’emplacement, les plans et l’état d’avancement des travaux.',
  'Bei einem Besuch geht es um die Lage, die Pläne und den Stand der Bauarbeiten.',
  'Визит посвящён расположению, планам и ходу работ.',
  'تدور الزيارة حول الموقع والمخططات ومرحلة الأعمال.',
  'Bij een bezoek gaat het om de ligging, de plattegronden en de stand van de werken.',
  'Wizyta dotyczy lokalizacji, rzutów i stanu prac.',
  'Et besøk handler om beliggenheten, tegningene og hvor langt arbeidene har kommet.',
  'Ett besök handlar om läget, ritningarna och hur långt arbetena har kommit.')
a(156, 'Visit the plot and its surroundings',
  'Visite la parcela y sus alrededores con nosotros.',
  'Visitez le terrain et ses environs avec nous.',
  'Besuchen Sie mit uns das Grundstück und seine Umgebung.',
  'Посетите участок и его окрестности вместе с нами.',
  'زوروا القطعة ومحيطها معنا.',
  'Bezoek met ons het perceel en de omgeving.',
  'Odwiedzą Państwo działkę i jej otoczenie razem z nami.',
  'Besøk tomten og omgivelsene sammen med oss.',
  'Besök tomten och omgivningarna tillsammans med oss.')
a(157, 'We drive to the marina and La Rada beach',
  'Vamos en coche con usted hasta el puerto deportivo y la playa de La Rada y cronometramos el trayecto.',
  'Nous nous rendons avec vous en voiture au port de plaisance et à la plage de La Rada, et chronométrons le trajet.',
  'Wir fahren mit Ihnen zum Yachthafen und zum Strand La Rada und messen die Zeit.',
  'Мы едем с вами на машине в порт и на пляж Ла-Рада и засекаем время.',
  'نقودكم بالسيارة إلى المرسى وشاطئ لا رادا ونحسب مدة الطريق.',
  'Wij rijden met u naar de jachthaven en het strand van La Rada en nemen de tijd op.',
  'Jedziemy z Państwem samochodem do portu jachtowego i na plażę La Rada i mierzymy czas.',
  'Vi kjører til småbåthavnen og La Rada-stranden og tar tiden.',
  'Vi kör till småbåtshamnen och stranden La Rada och tar tiden.')
a(158, 'Licence, completion date and the contract',
  'Licencia, fecha de entrega y contrato, antes de firmar nada.',
  'Permis, date de livraison et contrat, avant toute signature.',
  'Genehmigung, Fertigstellungstermin und Vertrag, bevor etwas unterschrieben wird.',
  'Разрешение, срок сдачи и договор — до подписания чего-либо.',
  'الرخصة وموعد التسليم والعقد، قبل توقيع أي شيء.',
  'Vergunning, opleverdatum en contract, voordat er iets wordt getekend.',
  'Pozwolenie, termin oddania i umowa — zanim cokolwiek zostanie podpisane.',
  'Tillatelse, overleveringsdato og kontrakt, før noe signeres.',
  'Bygglov, tillträdesdatum och avtal, innan något skrivs under.')
a(159, 'Ask about <em>Brisamar', 'Pregunte por <em>Brisamar Residences</em>', 'Renseignez-vous sur <em>Brisamar Residences</em>',
  'Fragen Sie nach <em>Brisamar Residences</em>', 'Узнайте о <em>Brisamar Residences</em>', 'استفسروا عن <em>Brisamar Residences</em>',
  'Vraag naar <em>Brisamar Residences</em>', 'Zapytaj o <em>Brisamar Residences</em>', 'Spør om <em>Brisamar Residences</em>', 'Fråga om <em>Brisamar Residences</em>')
T[todo[159]]['pl'] = 'Zapytaj o <em>Brisamar Residences</em>'
a(160, 'Hello Nueva Living, I would like information about Brisamar',
  'Hola Nueva Living, me gustaría recibir información sobre Brisamar Residences.', 'Bonjour Nueva Living, je souhaiterais des informations sur Brisamar Residences.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Brisamar Residences.', 'Здравствуйте, Nueva Living, мне нужна информация о Brisamar Residences.',
  'مرحباً Nueva Living، أودّ الحصول على معلومات عن Brisamar Residences.', 'Hallo Nueva Living, ik wil graag informatie over Brisamar Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Brisamar Residences.', 'Hei Nueva Living, jeg vil gjerne ha informasjon om Brisamar Residences.',
  'Hej Nueva Living, jag vill gärna få information om Brisamar Residences.')
a(161, 'The building has 22 homes with three bedrooms',
  'El edificio tiene 22 viviendas de tres dormitorios y dos baños, y nueve figuran con precio: de {E549000} a {E1050000}.',
  'L’immeuble compte 22 logements de trois chambres et deux salles de bain, et neuf sont listés avec un prix : de {E549000} à {E1050000}.',
  'Das Gebäude hat 22 Wohnungen mit drei Schlafzimmern und zwei Badezimmern, neun davon sind mit Preis aufgeführt: von {E549000} bis {E1050000}.',
  'В здании 22 квартиры с тремя спальнями и двумя ванными комнатами, девять из них указаны с ценой: от {E549000} до {E1050000}.',
  'في المبنى 22 مسكناً بثلاث غرف نوم وحمامين، وتسعة منها مدرجة بالأسعار: من {E549000} إلى {E1050000}.',
  'Het gebouw heeft 22 woningen met drie slaapkamers en twee badkamers, en negen staan met prijs op de lijst: van {E549000} tot {E1050000}.',
  'Budynek ma 22 lokale z trzema sypialniami i dwiema łazienkami, a dziewięć ma podaną cenę: od {E549000} do {E1050000}.',
  'Bygningen har 22 boliger med tre soverom og to bad, og ni er oppført med pris: fra {E549000} til {E1050000}.',
  'Byggnaden har 22 bostäder med tre sovrum och två badrum, och nio är listade med pris: från {E549000} till {E1050000}.')
a(162, 'The price list does not say. We confirm',
  'La lista de precios no lo indica. Confirmamos por escrito los impuestos y los gastos de compra antes de que reserve.',
  'La liste de prix ne le précise pas. Nous confirmons par écrit les taxes et les frais d’achat avant que vous ne réserviez.',
  'Die Preisliste sagt dazu nichts. Wir bestätigen die Steuern und Kaufnebenkosten schriftlich, bevor Sie reservieren.',
  'В прайс-листе об этом не сказано. Мы письменно подтверждаем налоги и расходы на покупку до того, как вы забронируете.',
  'لا تذكر قائمة الأسعار ذلك. نؤكد الضرائب وتكاليف الشراء كتابةً قبل أن تحجزوا.',
  'De prijslijst zegt dat niet. Wij bevestigen de belastingen en aankoopkosten schriftelijk voordat u reserveert.',
  'Cennik tego nie podaje. Podatki i koszty zakupu potwierdzamy na piśmie przed rezerwacją.',
  'Prislisten sier ikke noe om det. Vi bekrefter skatter og kjøpskostnader skriftlig før en eventuell reservasjon.',
  'Prislistan säger inget om det. Vi bekräftar skatter och köpkostnader skriftligt innan ni reserverar.')
a(163, 'Yes. The brochure says every home includes',
  'Sí. El folleto indica que todas las viviendas incluyen una plaza de garaje y un trastero en los sótanos.',
  'Oui. La brochure indique que chaque logement comprend une place de parking et un débarras aux niveaux de sous-sol.',
  'Ja. Laut Prospekt hat jede Wohnung einen Stellplatz und einen Abstellraum in den Untergeschossen.',
  'Да. В брошюре сказано, что в каждую квартиру входят парковочное место и кладовая на подземных уровнях.',
  'نعم. يذكر الكتيّب أن كل مسكن يشمل موقف سيارة ومخزناً في الطابقين السفليين.',
  'Ja. Volgens de brochure omvat elke woning een parkeerplaats en een berging op de kelderniveaus.',
  'Tak. Według broszury każdy lokal obejmuje miejsce parkingowe i komórkę na poziomach podziemnych.',
  'Ja. Brosjyren sier at hver bolig inkluderer en parkeringsplass og en bod i kjelleretasjene.',
  'Ja. Broschyren anger att varje bostad inkluderar en parkeringsplats och ett förråd på källarplanen.')
a(164, 'None of the developer’s documents gives a completion date. We ask',
  'Ninguno de los documentos del promotor indica una fecha de entrega. Solicitamos la fecha contractual y el estado de las obras.',
  'Aucun des documents du promoteur n’indique de date de livraison. Nous demandons la date contractuelle et l’état d’avancement des travaux.',
  'Keines der Dokumente des Bauträgers nennt einen Fertigstellungstermin. Wir fordern den vertraglichen Termin und den Stand der Bauarbeiten an.',
  'Ни в одном из документов застройщика не указан срок сдачи. Мы запрашиваем договорную дату и сведения о ходе работ.',
  'لا تذكر أي من وثائق المطوّر موعداً للتسليم. نطلب الموعد التعاقدي ومرحلة الأعمال.',
  'In geen van de documenten van de ontwikkelaar staat een opleverdatum. Wij vragen de contractuele datum en de stand van de werken op.',
  'W żadnym z dokumentów dewelopera nie ma terminu oddania. Prosimy o termin umowny i informację o stanie prac.',
  'Ingen av utbyggerens dokumenter oppgir en overleveringsdato. Vi ber om den kontraktsfestede datoen og status for arbeidene.',
  'Inget av exploatörens dokument anger ett tillträdesdatum. Vi begär det avtalade datumet och status för arbetena.')
a(165, 'The documents we hold do not give one',
  'Los documentos de que disponemos no lo indican. Se lo preguntamos al promotor y se lo confirmamos por escrito antes de que reserve.',
  'Les documents dont nous disposons ne l’indiquent pas. Nous interrogeons le promoteur et vous le confirmons par écrit avant que vous ne réserviez.',
  'Die uns vorliegenden Unterlagen nennen keinen. Wir fragen den Bauträger und bestätigen Ihnen den Plan schriftlich, bevor Sie reservieren.',
  'В имеющихся у нас документах его нет. Мы спрашиваем у застройщика и подтверждаем график письменно до того, как вы забронируете.',
  'لا تذكره الوثائق التي بين أيدينا. نسأل المطوّر ونؤكده لكم كتابةً قبل أن تحجزوا.',
  'In de documenten waarover wij beschikken staat er geen. Wij vragen het de ontwikkelaar en bevestigen het schriftelijk voordat u reserveert.',
  'Dokumenty, którymi dysponujemy, go nie podają. Pytamy dewelopera i potwierdzamy go Państwu na piśmie przed rezerwacją.',
  'Dokumentene vi har, oppgir ingen. Vi spør utbyggeren og bekrefter den skriftlig før en eventuell reservasjon.',
  'De handlingar vi har anger ingen. Vi frågar exploatören och bekräftar den skriftligt innan ni reserverar.')

# ---------------------------------------------------------------- anything left in the todo
missing = [en for en in todo if en not in T and en not in ('Fourth floor & solarium', 'Penthouse & solarium')]
if missing:
    print('MISSING', len(missing))
    for en in missing:
        print('  ', repr(en[:90]))
    sys.exit(1)
json.dump(T, open(f'{SP}/tr_a.json', 'w'), ensure_ascii=False, indent=1)
print('wrote', len(T), 'entries')
