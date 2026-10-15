# -*- coding: utf-8 -*-
"""Brezo Residences, part 2 of 2: residences, lifestyle, location, purchase terms, checks, availability, FAQ.

Same conventions as k_brezo.py (which carries the templates). Run after it:
    python3 tools/import/k_brezo_2.py <scratch dir>     (writes <scratch dir>/tr_b.json)
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


def find(hint):
    hits = [s for s in todo if s == hint] or [s for s in todo if s.startswith(hint)]
    assert len(hits) == 1, (hint, len(hits))
    return hits[0]


def a(hint, *tr):
    en = find(hint)
    assert len(tr) == 9, (hint, len(tr))
    T[en] = {l: expand(t, l) for l, t in zip(LOCS, tr)}


# ---------------------------------------------------------------- residences
a('Three kinds of home,',
  'Tres tipos de vivienda, <em>cinco a la venta</em>', 'Trois types de logement, <em>cinq annoncés</em>',
  'Drei Arten von Wohnungen, <em>fünf aufgeführt</em>', 'Три типа квартир, <em>пять в списке</em>',
  'ثلاثة أنواع من المساكن، <em>خمسة منها مدرجة</em>', 'Drie soorten woningen, <em>vijf op de lijst</em>',
  'Trzy rodzaje lokali, <em>pięć na liście</em>', 'Tre typer boliger, <em>fem oppført</em>', 'Tre typer av bostäder, <em>fem listade</em>')
a('The five listed homes fall into three groups',
  'Las cinco viviendas de la lista se dividen en tres grupos según su ubicación en el edificio. La tabla siguiente las recoge todas con sus precios.',
  'Les cinq logements listés se répartissent en trois groupes selon leur place dans l’immeuble. Le tableau ci-dessous les présente tous avec leurs prix.',
  'Die fünf aufgeführten Wohnungen gliedern sich nach ihrer Lage im Gebäude in drei Gruppen. Die folgende Tabelle listet alle mit ihren Preisen auf.',
  'Пять квартир из списка делятся на три группы по расположению в здании. В таблице ниже приведены все они с ценами.',
  'تنقسم المساكن الخمسة المدرجة إلى ثلاث مجموعات بحسب موقعها في المبنى. ويعرضها الجدول أدناه جميعًا مع أسعارها.',
  'De vijf woningen op de lijst vallen in drie groepen, naargelang hun plaats in het gebouw. De tabel hieronder toont ze allemaal met hun prijzen.',
  'Pięć lokali z listy dzieli się na trzy grupy według położenia w budynku. Poniższa tabela zawiera je wszystkie wraz z cenami.',
  'De fem oppførte boligene deles inn i tre grupper etter hvor de ligger i bygningen. Tabellen under viser alle med priser.',
  'De fem listade bostäderna delas in i tre grupper efter var de ligger i byggnaden. Tabellen nedan listar alla med deras priser.')
a('Ground floor, with a garden',
  'Planta baja, con jardín', 'Rez-de-chaussée, avec jardin', 'Erdgeschoss, mit Garten', 'Первый этаж, с садом',
  'الطابق الأرضي، بحديقة', 'Begane grond, met tuin', 'Parter, z ogrodem', 'Første etasje, med hage', 'Bottenvåning, med trädgård')
a('Homes 2 and 3 have two bedrooms',
  'Las viviendas 2 y 3 tienen dos dormitorios y dos baños, {N100.00} {U} construidos y {N74.10} {U} interiores, con una terraza cubierta de {N10.60} {U}, una terraza descubierta de {N8.10} {U} y un jardín de {N43.20} y {N44.20} {U}.',
  'Les logements 2 et 3 ont deux chambres et deux salles de bains, {N100.00} {U} construits et {N74.10} {U} intérieurs, avec une terrasse couverte de {N10.60} {U}, une terrasse découverte de {N8.10} {U} et un jardin de {N43.20} et {N44.20} {U}.',
  'Die Wohnungen 2 und 3 haben zwei Schlafzimmer und zwei Bäder, {N100.00} {U} bebaute Fläche und {N74.10} {U} Innenfläche, mit einer überdachten Terrasse von {N10.60} {U}, einer unüberdachten Terrasse von {N8.10} {U} und einem Garten von {N43.20} bzw. {N44.20} {U}.',
  'В квартирах 2 и 3 по две спальни и две ванные комнаты, {N100.00} {U} застроенной площади и {N74.10} {U} внутри, крытая терраса {N10.60} {U}, открытая терраса {N8.10} {U} и сад {N43.20} и {N44.20} {U}.',
  'للمسكنين 2 و3 غرفتا نوم وحمامان، و{N100.00} {U} مبنية و{N74.10} {U} داخلية، مع تراس مغطى بمساحة {N10.60} {U} وتراس مكشوف بمساحة {N8.10} {U} وحديقة بمساحة {N43.20} و{N44.20} {U}.',
  'Woningen 2 en 3 hebben twee slaapkamers en twee badkamers, {N100.00} {U} bebouwd en {N74.10} {U} binnen, met een overdekt terras van {N10.60} {U}, een onoverdekt terras van {N8.10} {U} en een tuin van {N43.20} en {N44.20} {U}.',
  'Lokale 2 i 3 mają dwie sypialnie i dwie łazienki, {N100.00} {U} zabudowy i {N74.10} {U} wnętrza, z tarasem zadaszonym o powierzchni {N10.60} {U}, tarasem odkrytym o powierzchni {N8.10} {U} i ogrodem o powierzchni {N43.20} i {N44.20} {U}.',
  'Bolig 2 og 3 har to soverom og to bad, {N100.00} {U} bygd og {N74.10} {U} innvendig, med en overbygd terrasse på {N10.60} {U}, en åpen terrasse på {N8.10} {U} og en hage på {N43.20} og {N44.20} {U}.',
  'Bostad 2 och 3 har två sovrum och två badrum, {N100.00} {U} byggyta och {N74.10} {U} inomhus, med en övertäckt terrass på {N10.60} {U}, en öppen terrass på {N8.10} {U} och en trädgård på {N43.20} respektive {N44.20} {U}.')
a('Home 15 has three bedrooms',
  'La vivienda 15 tiene tres dormitorios y dos baños, {N114.00} {U} construidos y {N82.60} {U} interiores, con una terraza cubierta de {N16.60} {U} y un jardín de {N14.90} {U}.',
  'Le logement 15 a trois chambres et deux salles de bains, {N114.00} {U} construits et {N82.60} {U} intérieurs, avec une terrasse couverte de {N16.60} {U} et un jardin de {N14.90} {U}.',
  'Die Wohnung 15 hat drei Schlafzimmer und zwei Bäder, {N114.00} {U} bebaute Fläche und {N82.60} {U} Innenfläche, mit einer überdachten Terrasse von {N16.60} {U} und einem Garten von {N14.90} {U}.',
  'В квартире 15 три спальни и две ванные комнаты, {N114.00} {U} застроенной площади и {N82.60} {U} внутри, крытая терраса {N16.60} {U} и сад {N14.90} {U}.',
  'للمسكن 15 ثلاث غرف نوم وحمامان، و{N114.00} {U} مبنية و{N82.60} {U} داخلية، مع تراس مغطى بمساحة {N16.60} {U} وحديقة بمساحة {N14.90} {U}.',
  'Woning 15 heeft drie slaapkamers en twee badkamers, {N114.00} {U} bebouwd en {N82.60} {U} binnen, met een overdekt terras van {N16.60} {U} en een tuin van {N14.90} {U}.',
  'Lokal 15 ma trzy sypialnie i dwie łazienki, {N114.00} {U} zabudowy i {N82.60} {U} wnętrza, z tarasem zadaszonym o powierzchni {N16.60} {U} i ogrodem o powierzchni {N14.90} {U}.',
  'Bolig 15 har tre soverom og to bad, {N114.00} {U} bygd og {N82.60} {U} innvendig, med en overbygd terrasse på {N16.60} {U} og en hage på {N14.90} {U}.',
  'Bostad 15 har tre sovrum och två badrum, {N114.00} {U} byggyta och {N82.60} {U} inomhus, med en övertäckt terrass på {N16.60} {U} och en trädgård på {N14.90} {U}.')
a('Prices are EUR 495,500',
  'Los precios son {E495500}, {E497500} y {E502000}.', 'Les prix sont de {E495500}, {E497500} et {E502000}.',
  'Die Preise betragen {E495500}, {E497500} und {E502000}.', 'Цены — {E495500}, {E497500} и {E502000}.',
  'الأسعار {E495500} و{E497500} و{E502000}.', 'De prijzen zijn {E495500}, {E497500} en {E502000}.',
  'Ceny wynoszą {E495500}, {E497500} i {E502000}.', 'Prisene er {E495500}, {E497500} og {E502000}.',
  'Priserna är {E495500}, {E497500} och {E502000}.')
a('Home 54 has two bedrooms',
  'La vivienda 54 tiene dos dormitorios y dos baños, {N103.00} {U} construidos y {N76.40} {U} interiores, con una terraza descubierta de {N16.70} {U}.',
  'Le logement 54 a deux chambres et deux salles de bains, {N103.00} {U} construits et {N76.40} {U} intérieurs, avec une terrasse découverte de {N16.70} {U}.',
  'Die Wohnung 54 hat zwei Schlafzimmer und zwei Bäder, {N103.00} {U} bebaute Fläche und {N76.40} {U} Innenfläche, mit einer unüberdachten Terrasse von {N16.70} {U}.',
  'В квартире 54 две спальни и две ванные комнаты, {N103.00} {U} застроенной площади и {N76.40} {U} внутри, открытая терраса {N16.70} {U}.',
  'للمسكن 54 غرفتا نوم وحمامان، و{N103.00} {U} مبنية و{N76.40} {U} داخلية، مع تراس مكشوف بمساحة {N16.70} {U}.',
  'Woning 54 heeft twee slaapkamers en twee badkamers, {N103.00} {U} bebouwd en {N76.40} {U} binnen, met een onoverdekt terras van {N16.70} {U}.',
  'Lokal 54 ma dwie sypialnie i dwie łazienki, {N103.00} {U} zabudowy i {N76.40} {U} wnętrza, z tarasem odkrytym o powierzchni {N16.70} {U}.',
  'Bolig 54 har to soverom og to bad, {N103.00} {U} bygd og {N76.40} {U} innvendig, med en åpen terrasse på {N16.70} {U}.',
  'Bostad 54 har två sovrum och två badrum, {N103.00} {U} byggyta och {N76.40} {U} inomhus, med en öppen terrass på {N16.70} {U}.')
a('The price is EUR 483,500',
  'El precio es de {E483500}.', 'Le prix est de {E483500}.', 'Der Preis beträgt {E483500}.', 'Цена — {E483500}.', 'السعر {E483500}.',
  'De prijs is {E483500}.', 'Cena wynosi {E483500}.', 'Prisen er {E483500}.', 'Priset är {E483500}.')
a('Home 57 has three bedrooms',
  'La vivienda 57 tiene tres dormitorios y dos baños, {N107.00} {U} construidos y {N77.50} {U} interiores, con una terraza descubierta de {N99.90} {U}.',
  'Le logement 57 a trois chambres et deux salles de bains, {N107.00} {U} construits et {N77.50} {U} intérieurs, avec une terrasse découverte de {N99.90} {U}.',
  'Die Wohnung 57 hat drei Schlafzimmer und zwei Bäder, {N107.00} {U} bebaute Fläche und {N77.50} {U} Innenfläche, mit einer unüberdachten Terrasse von {N99.90} {U}.',
  'В квартире 57 три спальни и две ванные комнаты, {N107.00} {U} застроенной площади и {N77.50} {U} внутри, открытая терраса {N99.90} {U}.',
  'للمسكن 57 ثلاث غرف نوم وحمامان، و{N107.00} {U} مبنية و{N77.50} {U} داخلية، مع تراس مكشوف بمساحة {N99.90} {U}.',
  'Woning 57 heeft drie slaapkamers en twee badkamers, {N107.00} {U} bebouwd en {N77.50} {U} binnen, met een onoverdekt terras van {N99.90} {U}.',
  'Lokal 57 ma trzy sypialnie i dwie łazienki, {N107.00} {U} zabudowy i {N77.50} {U} wnętrza, z tarasem odkrytym o powierzchni {N99.90} {U}.',
  'Bolig 57 har tre soverom og to bad, {N107.00} {U} bygd og {N77.50} {U} innvendig, med en åpen terrasse på {N99.90} {U}.',
  'Bostad 57 har tre sovrum och två badrum, {N107.00} {U} byggyta och {N77.50} {U} inomhus, med en öppen terrass på {N99.90} {U}.')
a('The price is EUR 749,000',
  'El precio es de {E749000}.', 'Le prix est de {E749000}.', 'Der Preis beträgt {E749000}.', 'Цена — {E749000}.', 'السعر {E749000}.',
  'De prijs is {E749000}.', 'Cena wynosi {E749000}.', 'Prisen er {E749000}.', 'Priset är {E749000}.')

# ---------------------------------------------------------------- lifestyle
a('Gardens, <em>a pool</em> and the beach nearby',
  'Jardines, <em>piscina</em> y la playa cerca', 'Des jardins, <em>une piscine</em> et la plage à proximité',
  'Gärten, <em>ein Pool</em> und der Strand in der Nähe', 'Сады, <em>бассейн</em> и пляж рядом',
  'حدائق، <em>ومسبح</em> والشاطئ قريب', 'Tuinen, <em>een zwembad</em> en het strand in de buurt',
  'Ogrody, <em>basen</em> i plaża w pobliżu', 'Hager, <em>et basseng</em> og stranden i nærheten', 'Trädgårdar, <em>en pool</em> och stranden nära')
a('Life here is outdoors',
  'La vida aquí transcurre al aire libre, entre un jardín o una terraza privados, la piscina compartida y la playa.',
  'La vie ici se passe en plein air, entre un jardin ou une terrasse privés, la piscine partagée et la plage.',
  'Das Leben hier spielt sich draußen ab, zwischen privatem Garten oder Terrasse, dem gemeinsamen Pool und dem Strand.',
  'Жизнь здесь проходит на открытом воздухе: между частным садом или террасой, общим бассейном и пляжем.',
  'الحياة هنا في الهواء الطلق، بين حديقة أو تراس خاص والمسبح المشترك والشاطئ.',
  'Het leven hier speelt zich buiten af, tussen een privétuin of terras, het gedeelde zwembad en het strand.',
  'Życie toczy się tu na świeżym powietrzu, między prywatnym ogrodem lub tarasem, wspólnym basenem a plażą.',
  'Livet her foregår utendørs, mellom en privat hage eller terrasse, det felles bassenget og stranden.',
  'Livet här tillbringas utomhus, mellan en privat trädgård eller terrass, den gemensamma poolen och stranden.')
a('The ground-floor homes have a private garden and the penthouses',
  'Las viviendas de planta baja tienen jardín privado y los áticos amplias terrazas, y cada vivienda de la lista tiene una terraza en su plano.',
  'Les logements du rez-de-chaussée ont un jardin privé et les penthouses de vastes terrasses, et chaque logement listé a une terrasse sur son plan.',
  'Die Erdgeschosswohnungen haben einen privaten Garten und die Penthäuser große Terrassen, und jede aufgeführte Wohnung hat in ihrem Grundriss eine Terrasse.',
  'У квартир на первом этаже есть частный сад, у пентхаусов — просторные террасы, а у каждой квартиры из списка на плане есть терраса.',
  'لمساكن الطابق الأرضي حديقة خاصة وللبنتهاوس تراسات واسعة، ولكل مسكن مدرج تراس في مخططه.',
  'De woningen op de begane grond hebben een privétuin en de penthouses ruime terrassen, en elke woning op de lijst heeft een terras op de plattegrond.',
  'Lokale na parterze mają prywatny ogród, a penthouse’y duże tarasy, a każdy lokal z listy ma na rzucie taras.',
  'Boligene i første etasje har privat hage og toppleilighetene store terrasser, og hver oppført bolig har en terrasse på plantegningen.',
  'Bostäderna på bottenvåningen har privat trädgård och takvåningarna stora terrasser, och varje listad bostad har en terrass på sin planritning.')
a('A sunny communal outdoor pool for adults, with salt',
  'Una amplia y soleada piscina comunitaria exterior para adultos, con cloración salina e iluminación nocturna.',
  'Une vaste piscine extérieure commune ensoleillée pour adultes, à électrolyse au sel et éclairage nocturne.',
  'Ein sonniger Gemeinschaftspool im Freien für Erwachsene, mit Salzelektrolyse und Nachtbeleuchtung.',
  'Просторный солнечный общий открытый бассейн для взрослых с солевым хлорированием и ночной подсветкой.',
  'مسبح خارجي مشترك واسع ومشمس للبالغين، بمعالجة بالكلور الملحي وإضاءة ليلية.',
  'Een zonnig gemeenschappelijk buitenzwembad voor volwassenen, met zoutelektrolyse en nachtverlichting.',
  'Duży, nasłoneczniony wspólny basen zewnętrzny dla dorosłych, z chlorowaniem solnym i oświetleniem nocnym.',
  'Et stort, solrikt felles utendørsbasseng for voksne, med saltklorering og nattbelysning.',
  'En stor, solig gemensam utomhuspool för vuxna, med saltklorering och nattbelysning.')
a('The gym and the social room',
  'El gimnasio y la sala social', 'La salle de sport et la salle commune', 'Der Fitnessraum und der Gemeinschaftsraum',
  'Тренажёрный зал и общая гостиная', 'الصالة الرياضية والقاعة الاجتماعية', 'De fitnessruimte en de gemeenschappelijke ruimte',
  'Siłownia i sala wspólna', 'Treningsrommet og fellesrommet', 'Gymmet och gemensamhetsrummet')
a('An equipped gym, and a social room',
  'Un gimnasio equipado y una sala social con cocina, aseos y wifi para comidas y reuniones compartidas.',
  'Une salle de sport équipée et une salle commune avec cuisine, sanitaires et wifi pour les repas et les rencontres partagés.',
  'Ein ausgestatteter Fitnessraum und ein Gemeinschaftsraum mit Küche, Toiletten und WLAN für gemeinsame Mahlzeiten und Zusammenkünfte.',
  'Оборудованный тренажёрный зал и общая гостиная с кухней, санузлами и Wi-Fi для совместных обедов и встреч.',
  'صالة رياضية مجهزة وقاعة اجتماعية بمطبخ ودورات مياه وواي فاي للوجبات واللقاءات المشتركة.',
  'Een uitgeruste fitnessruimte en een gemeenschappelijke ruimte met keuken, toiletten en wifi voor gedeelde maaltijden en bijeenkomsten.',
  'Wyposażona siłownia i sala wspólna z kuchnią, toaletami i Wi-Fi na wspólne posiłki i spotkania.',
  'Et utstyrt treningsrom og et fellesrom med kjøkken, toaletter og wifi for felles måltider og samlinger.',
  'Ett utrustat gym och ett gemensamhetsrum med kök, toaletter och wifi för gemensamma måltider och sammankomster.')
a('Every home has at least one parking space and a storage room, and the garage',
  'Cada vivienda tiene al menos una plaza de aparcamiento y un trastero, y el garaje cuenta con preinstalación para la recarga de coches eléctricos.',
  'Chaque logement dispose d’au moins une place de stationnement et d’une cave, et le garage a une pré-installation pour la recharge des voitures électriques.',
  'Jede Wohnung hat mindestens einen Stellplatz und einen Abstellraum, und die Garage hat eine Vorinstallation für das Laden von Elektroautos.',
  'У каждой квартиры есть как минимум одно парковочное место и кладовая, а в гараже предусмотрена подготовка под зарядку электромобилей.',
  'لكل مسكن موقف سيارات واحد على الأقل وغرفة تخزين، وفي المرآب تجهيز مسبق لشحن السيارات الكهربائية.',
  'Elke woning heeft minstens één parkeerplaats en een berging, en de garage heeft een voorbereiding voor het laden van elektrische auto’s.',
  'Każdy lokal ma co najmniej jedno miejsce postojowe i komórkę, a garaż jest przygotowany pod ładowanie samochodów elektrycznych.',
  'Hver bolig har minst én parkeringsplass og en bod, og garasjen har forberedelse for lading av elbiler.',
  'Varje bostad har minst en parkeringsplats och ett förråd, och garaget har förberedelse för laddning av elbilar.')

# ---------------------------------------------------------------- location
a('Cala de Mijas, <em>by the sea between',
  'Cala de Mijas, <em>junto al mar entre Fuengirola y La Cala</em>', 'Cala de Mijas, <em>au bord de la mer entre Fuengirola et La Cala</em>',
  'Cala de Mijas, <em>am Meer zwischen Fuengirola und La Cala</em>', 'Кала-де-Михас, <em>у моря между Фуэнхиролой и Ла-Калой</em>',
  'كالا دي ميهاس، <em>على البحر بين فوينخيرولا ولا كالا</em>', 'Cala de Mijas, <em>aan zee tussen Fuengirola en La Cala</em>',
  'Cala de Mijas, <em>nad morzem między Fuengirolą a La Calą</em>', 'Cala de Mijas, <em>ved sjøen mellom Fuengirola og La Cala</em>',
  'Cala de Mijas, <em>vid havet mellan Fuengirola och La Cala</em>')
a('The homes are at Cala de Mijas, on the coast',
  'Las viviendas están en Cala de Mijas, en la costa entre Fuengirola y La Cala. El folleto del promotor sitúa la playa a dos minutos a pie, el centro de Cala de Mijas a {N1.6} km, a tres minutos en coche, y la A-7 y la AP-7 muy cerca. Indica el Chaparral Golf Club a menos de dos kilómetros, con centros comerciales, supermercados, restaurantes, un centro de salud y farmacias en la zona, el aeropuerto de Málaga a menos de 25 minutos en coche y la estación María Zambrano a 40 minutos. Fuengirola está a unos diez minutos en coche, según el portal del promotor.',
  'Les logements sont à Cala de Mijas, sur la côte entre Fuengirola et La Cala. La brochure du promoteur place la plage à deux minutes à pied, le centre de Cala de Mijas à {N1.6} km, à trois minutes en voiture, et l’A-7 et l’AP-7 tout près. Elle indique le Chaparral Golf Club à moins de deux kilomètres, avec des centres commerciaux, des supermarchés, des restaurants, un centre de santé et des pharmacies dans le secteur, l’aéroport de Malaga à moins de 25 minutes en voiture et la gare María Zambrano à 40 minutes. Fuengirola est à environ dix minutes en voiture, selon le portail du promoteur.',
  'Die Wohnungen liegen in Cala de Mijas, an der Küste zwischen Fuengirola und La Cala. Die Broschüre des Bauträgers nennt den Strand zwei Gehminuten entfernt, das Zentrum von Cala de Mijas {N1.6} km entfernt, drei Autominuten, und die A-7 und die AP-7 ganz in der Nähe. Sie führt den Chaparral Golf Club in weniger als zwei Kilometern Entfernung an, dazu Einkaufszentren, Supermärkte, Restaurants, ein Gesundheitszentrum und Apotheken in der Umgebung, den Flughafen Malaga in unter 25 Autominuten und den Bahnhof María Zambrano in 40 Minuten. Fuengirola ist laut dem Portal des Bauträgers etwa zehn Autominuten entfernt.',
  'Квартиры находятся в Кала-де-Михас, на побережье между Фуэнхиролой и Ла-Калой. Брошюра застройщика указывает, что до пляжа две минуты пешком, до центра Кала-де-Михас {N1.6} км, три минуты на машине, а трассы A-7 и AP-7 совсем рядом. В ней упомянуты гольф-клуб Chaparral менее чем в двух километрах, торговые центры, супермаркеты, рестораны, медицинский центр и аптеки в округе, аэропорт Малаги менее чем в 25 минутах на машине и вокзал Мария Самбрано в 40 минутах. До Фуэнхиролы, по данным портала застройщика, около десяти минут на машине.',
  'تقع المساكن في كالا دي ميهاس، على الساحل بين فوينخيرولا ولا كالا. يضع كتيّب المطوّر الشاطئ على بُعد دقيقتين سيرًا، ووسط كالا دي ميهاس على بُعد {N1.6} كم، أي ثلاث دقائق بالسيارة، والطريقين A-7 وAP-7 على مقربة. ويذكر نادي تشابارال للغولف على بُعد أقل من كيلومترين، ومراكز تسوق وأسواقًا مركزية ومطاعم ومركزًا صحيًا وصيدليات في المنطقة، ومطار مالقة على بُعد أقل من 25 دقيقة بالسيارة ومحطة ماريا زامبرانو على بُعد 40 دقيقة. أما فوينخيرولا فعلى بُعد نحو عشر دقائق بالسيارة بحسب بوابة المطوّر.',
  'De woningen liggen in Cala de Mijas, aan de kust tussen Fuengirola en La Cala. De brochure van de ontwikkelaar plaatst het strand op twee minuten lopen, het centrum van Cala de Mijas op {N1.6} km, drie minuten rijden, en de A-7 en de AP-7 vlakbij. Ze noemt Chaparral Golf Club op minder dan twee kilometer, met winkelcentra, supermarkten, restaurants, een gezondheidscentrum en apotheken in de buurt, de luchthaven van Málaga op minder dan 25 minuten rijden en het station María Zambrano op 40 minuten. Fuengirola ligt volgens het portaal van de ontwikkelaar op ongeveer tien minuten rijden.',
  'Lokale znajdują się w Cala de Mijas, na wybrzeżu między Fuengirolą a La Calą. Broszura dewelopera podaje plażę dwie minuty spacerem, centrum Cala de Mijas w odległości {N1.6} km, trzy minuty samochodem, a A-7 i AP-7 tuż obok. Wymienia Chaparral Golf Club w odległości mniejszej niż dwa kilometry, a w okolicy centra handlowe, supermarkety, restauracje, ośrodek zdrowia i apteki, lotnisko w Maladze w mniej niż 25 minut samochodem i dworzec María Zambrano w 40 minut. Do Fuengiroli według portalu dewelopera jest około dziesięć minut samochodem.',
  'Boligene ligger i Cala de Mijas, på kysten mellom Fuengirola og La Cala. Utbyggerens brosjyre oppgir stranden to minutter å gå unna, sentrum av Cala de Mijas {N1.6} km unna, tre minutter med bil, og A-7 og AP-7 like ved. Den nevner Chaparral Golf Club under to kilometer unna, med kjøpesentre, supermarkeder, restauranter, et helsesenter og apotek i området, Málaga lufthavn på under 25 minutter med bil og stasjonen María Zambrano på 40 minutter. Fuengirola ligger omtrent ti minutter unna med bil, ifølge utbyggerens portal.',
  'Bostäderna ligger i Cala de Mijas, vid kusten mellan Fuengirola och La Cala. Exploatörens broschyr anger stranden två minuters promenad bort, centrala Cala de Mijas {N1.6} km bort, tre minuter med bil, och A-7 och AP-7 alldeles intill. Den nämner Chaparral Golf Club på under två kilometers avstånd, med köpcentrum, stormarknader, restauranger, en vårdcentral och apotek i området, Málagas flygplats på under 25 minuter med bil och stationen María Zambrano på 40 minuter. Fuengirola ligger ungefär tio minuter bort med bil, enligt exploatörens portal.')
a('Cala de Mijas, <em>Mijas Costa</em>',
  'Cala de Mijas, <em>Mijas Costa</em>', 'Cala de Mijas, <em>Mijas Costa</em>', 'Cala de Mijas, <em>Mijas Costa</em>',
  'Кала-де-Михас, <em>Михас-Коста</em>', 'كالا دي ميهاس، <em>ميخاس كوستا</em>', 'Cala de Mijas, <em>Mijas Costa</em>',
  'Cala de Mijas, <em>Mijas Costa</em>', 'Cala de Mijas, <em>Mijas Costa</em>', 'Cala de Mijas, <em>Mijas Costa</em>')
a('Cala de Mijas, Mijas Costa',
  'Cala de Mijas, Mijas Costa', 'Cala de Mijas, Mijas Costa', 'Cala de Mijas, Mijas Costa', 'Кала-де-Михас, Михас-Коста',
  'كالا دي ميهاس، ميخاس كوستا', 'Cala de Mijas, Mijas Costa', 'Cala de Mijas, Mijas Costa', 'Cala de Mijas, Mijas Costa', 'Cala de Mijas, Mijas Costa')
a('2 minutes on foot, as the developer says',
  'A 2 minutos a pie, según el promotor', 'À 2 minutes à pied, selon le promoteur', 'Zwei Gehminuten, laut Bauträger',
  '2 минуты пешком, по данным застройщика', 'دقيقتان سيرًا بحسب المطوّر', '2 minuten lopen, volgens de ontwikkelaar',
  '2 minuty spacerem, według dewelopera', '2 minutter å gå, ifølge utbyggeren', '2 minuters promenad, enligt exploatören')
a('1.6 km, about 3 minutes by car',
  '{N1.6} km, unos 3 minutos en coche', '{N1.6} km, environ 3 minutes en voiture', '{N1.6} km, etwa 3 Minuten mit dem Auto',
  '{N1.6} км, около 3 минут на машине', '{N1.6} كم، نحو 3 دقائق بالسيارة', '{N1.6} km, ongeveer 3 minuten met de auto',
  '{N1.6} km, około 3 minut samochodem', '{N1.6} km, omtrent 3 minutter med bil', '{N1.6} km, cirka 3 minuter med bil')
a('Chaparral Golf Club',
  'Chaparral Golf Club', 'Chaparral Golf Club', 'Chaparral Golf Club', 'Гольф-клуб Chaparral', 'نادي تشابارال للغولف',
  'Chaparral Golf Club', 'Chaparral Golf Club', 'Chaparral Golf Club', 'Chaparral Golf Club')
a('Under 25 minutes',
  'Menos de 25 minutos', 'Moins de 25 minutes', 'Unter 25 Minuten', 'Менее 25 минут', 'أقل من 25 دقيقة',
  'Minder dan 25 minuten', 'Poniżej 25 minut', 'Under 25 minutter', 'Under 25 minuter')

# ---------------------------------------------------------------- purchase and checks
a('The reservation is EUR 6,000 plus 10% VAT, EUR 6,600 in all.',
  'La reserva es de {E6000} más el 10% de IVA, es decir, {E6600} en total. Los documentos no indican si se descuenta del primer pago, así que lo preguntamos.',
  'La réservation est de {E6000} plus 10 % de TVA, soit {E6600} au total. Les documents n’indiquent pas si elle est déduite du premier versement ; nous posons la question.',
  'Die Reservierung beträgt {E6000} zuzüglich 10 % MwSt., insgesamt {E6600}. Die Unterlagen sagen nicht, ob sie von der ersten Rate abgezogen wird, deshalb fragen wir nach.',
  'Бронирование стоит {E6000} плюс НДС 10 %, всего {E6600}. В документах не сказано, засчитывается ли оно в первый платёж, поэтому мы это уточняем.',
  'الحجز {E6000} زائد ضريبة القيمة المضافة 10%، أي {E6600} إجمالًا. ولا تذكر الوثائق ما إذا كان يُخصم من الدفعة الأولى، لذلك نسأل عن ذلك.',
  'De reservering bedraagt {E6000} plus 10% btw, in totaal {E6600}. De documenten vermelden niet of ze van de eerste termijn wordt afgetrokken, dus vragen we het na.',
  'Rezerwacja wynosi {E6000} plus VAT 10%, łącznie {E6600}. Dokumenty nie mówią, czy jest odliczana od pierwszej raty, dlatego o to pytamy.',
  'Reservasjonen er {E6000} pluss 10 % mva., til sammen {E6600}. Dokumentene sier ikke om den trekkes fra første innbetaling, så vi spør om det.',
  'Reservationen är {E6000} plus 10 % moms, sammanlagt {E6600}. Dokumenten anger inte om den dras av från första delbetalningen, så vi frågar om det.')
a('30% plus VAT on signing the private purchase contract',
  'El 30% más IVA al firmar el contrato privado de compraventa y el 70% más IVA con la escritura ante notario.',
  '30 % hors TVA à la signature du contrat de vente privé et 70 % hors TVA à l’acte chez le notaire.',
  '30 % zuzüglich MwSt. bei Unterzeichnung des privaten Kaufvertrags und 70 % zuzüglich MwSt. bei der Beurkundung beim Notar.',
  '30 % плюс НДС при подписании предварительного договора купли-продажи и 70 % плюс НДС при оформлении сделки у нотариуса.',
  '30% زائد ضريبة القيمة المضافة عند توقيع عقد الشراء الخاص، و70% زائد الضريبة عند توقيع صك البيع أمام كاتب العدل.',
  '30% plus btw bij ondertekening van de onderhandse koopovereenkomst en 70% plus btw bij de akte bij de notaris.',
  '30% plus VAT przy podpisaniu umowy przedwstępnej i 70% plus VAT u notariusza, przy akcie notarialnym.',
  '30 % pluss mva. ved signering av den private kjøpekontrakten og 70 % pluss mva. ved skjøtet hos notarius.',
  '30 % plus moms vid undertecknandet av det privata köpeavtalet och 70 % plus moms vid lagfarten hos notarien.')
a('The prices do not include VAT. The developer gives 10% VAT',
  'Los precios no incluyen el IVA. El promotor indica el 10% de IVA en la reserva y da los demás pagos más IVA. Nueva Living confirma por escrito los impuestos y los gastos de compra.',
  'Les prix n’incluent pas la TVA. Le promoteur indique 10 % de TVA sur la réservation et donne les autres versements hors TVA. Nueva Living confirme par écrit les taxes et les frais d’achat.',
  'Die Preise verstehen sich zuzüglich MwSt. Der Bauträger gibt 10 % MwSt. auf die Reservierung an und nennt die übrigen Raten zuzüglich MwSt. Nueva Living bestätigt Steuern und Kaufnebenkosten schriftlich.',
  'Цены указаны без НДС. Застройщик называет НДС 10 % для бронирования, а остальные платежи указывает плюс НДС. Nueva Living письменно подтверждает налоги и расходы на покупку.',
  'الأسعار لا تشمل ضريبة القيمة المضافة. ويذكر المطوّر نسبة 10% على الحجز ويذكر الدفعات الأخرى زائد الضريبة. وتؤكد Nueva Living الضرائب ومصاريف الشراء كتابةً.',
  'De prijzen zijn exclusief btw. De ontwikkelaar vermeldt 10% btw op de reservering en noemt de overige termijnen plus btw. Nueva Living bevestigt de belastingen en aankoopkosten schriftelijk.',
  'Ceny nie obejmują VAT. Deweloper podaje VAT 10% przy rezerwacji, a pozostałe raty określa jako plus VAT. Nueva Living potwierdza na piśmie podatki i koszty zakupu.',
  'Prisene inkluderer ikke mva. Utbyggeren oppgir 10 % mva. på reservasjonen og angir de øvrige innbetalingene pluss mva. Nueva Living bekrefter skatter og kjøpskostnader skriftlig.',
  'Priserna inkluderar inte moms. Exploatören anger 10 % moms på reservationen och anger övriga betalningar plus moms. Nueva Living bekräftar skatter och köpkostnader skriftligen.')
a('The developer says every home has at least one parking space and a storage room. We confirm',
  'El promotor indica que cada vivienda tiene al menos una plaza de aparcamiento y un trastero. Confirmamos la plaza y el trastero de la vivienda que usted elija.',
  'Le promoteur indique que chaque logement dispose d’au moins une place de stationnement et d’une cave. Nous confirmons la place et la cave du logement que vous choisissez.',
  'Der Bauträger gibt an, dass jede Wohnung mindestens einen Stellplatz und einen Abstellraum hat. Wir bestätigen Stellplatz und Abstellraum der von Ihnen gewählten Wohnung.',
  'Застройщик сообщает, что у каждой квартиры есть как минимум одно парковочное место и кладовая. Мы подтверждаем место и кладовую той квартиры, которую вы выберете.',
  'يذكر المطوّر أن لكل مسكن موقف سيارات واحدًا على الأقل وغرفة تخزين. ونؤكد الموقف والغرفة الخاصين بالمسكن الذي تختارونه.',
  'De ontwikkelaar geeft aan dat elke woning minstens één parkeerplaats en een berging heeft. Wij bevestigen de plaats en de berging van de woning die u kiest.',
  'Deweloper podaje, że każdy lokal ma co najmniej jedno miejsce postojowe i komórkę. Potwierdzamy miejsce i komórkę wybranego przez Państwa lokalu.',
  'Utbyggeren oppgir at hver bolig har minst én parkeringsplass og en bod. Vi bekrefter plassen og boden for boligen dere velger.',
  'Exploatören anger att varje bostad har minst en parkeringsplats och ett förråd. Vi bekräftar platsen och förrådet för den bostad ni väljer.')
a('The documents we hold do not say whether the building licence',
  'Los documentos de que disponemos no indican si la licencia de obras está concedida ni en qué fase están las obras, y la memoria de calidades es provisional. Solicitamos la licencia, su estado y la fecha de inicio de las obras.',
  'Les documents dont nous disposons n’indiquent pas si le permis de construire est accordé ni à quel stade en sont les travaux, et le descriptif de qualité est provisoire. Nous demandons le permis, son état et la date de début des travaux.',
  'Die uns vorliegenden Unterlagen sagen nicht, ob die Baugenehmigung erteilt wurde oder in welchem Stadium die Bauarbeiten sind, und die Baubeschreibung ist vorläufig. Wir fordern die Genehmigung, ihren Stand und den Baubeginn an.',
  'В имеющихся у нас документах не сказано, получено ли разрешение на строительство и на какой стадии работы, а спецификация качества предварительная. Мы запрашиваем разрешение, его статус и дату начала работ.',
  'لا تذكر الوثائق التي بين أيدينا ما إذا كانت رخصة البناء قد مُنحت أو في أي مرحلة وصلت الأعمال، ومواصفات الجودة مؤقتة. نطلب الرخصة وحالتها وتاريخ بدء الأعمال.',
  'In de documenten waarover wij beschikken staat niet of de bouwvergunning is verleend of in welke fase de werken zijn, en de kwaliteitsspecificatie is voorlopig. Wij vragen de vergunning, de status ervan en de startdatum van de werken op.',
  'Dokumenty, którymi dysponujemy, nie mówią, czy pozwolenie na budowę zostało wydane ani na jakim etapie są prace, a specyfikacja jakości jest wstępna. Prosimy o pozwolenie, jego status i datę rozpoczęcia prac.',
  'Dokumentene vi har, sier ikke om byggetillatelsen er gitt eller hvilket stadium arbeidene har nådd, og kvalitetsspesifikasjonen er foreløpig. Vi ber om tillatelsen, status for den og startdatoen for arbeidene.',
  'De handlingar vi har anger inte om bygglovet har beviljats eller vilket stadium arbetena har nått, och kvalitetsspecifikationen är preliminär. Vi begär bygglovet, dess status och startdatum för arbetena.')
a('The plans give a built area that includes a share of the communal areas',
  'Los planos dan una superficie construida que incluye una parte de las zonas comunes y una segunda superficie construida, mayor, según el Decreto 218/2005: {N110.58} {U} frente a {N100.00} {U} en las viviendas 2 y 3. El portal del promotor da además otras cifras, {N85} {U} construidos para las viviendas 2 y 3. Para la vivienda 57 el plano da {N107.00} {U} construidos, {N77.50} interiores y una terraza de {N99.90} {U}, y el folleto {N109.00}, {N77.30} y {N97.20}, con el portal en 109, 77 y 97. Confirmamos qué cifras utiliza el contrato.',
  'Les plans donnent une surface construite qui inclut une part des parties communes et une seconde surface construite, plus grande, selon le décret 218/2005 : {N110.58} {U} contre {N100.00} {U} pour les logements 2 et 3. Le portail du promoteur donne encore d’autres chiffres, {N85} {U} construits pour les logements 2 et 3. Pour le logement 57, le plan donne {N107.00} {U} construits, {N77.50} intérieurs et une terrasse de {N99.90} {U}, et la brochure {N109.00}, {N77.30} et {N97.20}, avec le portail à 109, 77 et 97. Nous confirmons quels chiffres retient le contrat.',
  'Die Pläne geben eine bebaute Fläche an, die einen Anteil der Gemeinschaftsbereiche enthält, und eine zweite, größere bebaute Fläche nach dem Dekret 218/2005: {N110.58} {U} gegenüber {N100.00} {U} bei den Wohnungen 2 und 3. Das Portal des Bauträgers nennt noch andere Werte, {N85} {U} bebaute Fläche für die Wohnungen 2 und 3. Für die Wohnung 57 gibt der Plan {N107.00} {U} bebaut, {N77.50} Innenfläche und eine Terrasse von {N99.90} {U} an, die Broschüre {N109.00}, {N77.30} und {N97.20}, das Portal 109, 77 und 97. Wir klären, welche Werte der Vertrag verwendet.',
  'На планах указана застроенная площадь, включающая долю общих зон, и вторая, большая застроенная площадь по декрету 218/2005: {N110.58} {U} против {N100.00} {U} для квартир 2 и 3. На портале застройщика приведены и другие цифры: {N85} {U} застроенной площади для квартир 2 и 3. Для квартиры 57 на плане указаны {N107.00} {U} застроенной площади, {N77.50} внутри и терраса {N99.90} {U}, в брошюре — {N109.00}, {N77.30} и {N97.20}, на портале — 109, 77 и 97. Мы уточняем, какие цифры использует договор.',
  'تذكر المخططات مساحة مبنية تشمل حصة من المناطق المشتركة، ومساحة مبنية ثانية أكبر بموجب المرسوم 218/2005: {N110.58} {U} مقابل {N100.00} {U} للمسكنين 2 و3. وتذكر بوابة المطوّر أرقامًا أخرى، هي {N85} {U} مبنية للمسكنين 2 و3. وللمسكن 57 يذكر المخطط {N107.00} {U} مبنية و{N77.50} داخلية وتراسًا بمساحة {N99.90} {U}، ويذكر الكتيّب {N109.00} و{N77.30} و{N97.20}، وتذكر البوابة 109 و77 و97. نؤكد أي الأرقام يعتمدها العقد.',
  'De plattegronden geven een bebouwde oppervlakte die een deel van de gemeenschappelijke ruimten omvat en een tweede, grotere bebouwde oppervlakte volgens decreet 218/2005: {N110.58} {U} tegenover {N100.00} {U} bij de woningen 2 en 3. Het portaal van de ontwikkelaar geeft nog andere cijfers, {N85} {U} bebouwd voor de woningen 2 en 3. Voor woning 57 geeft de plattegrond {N107.00} {U} bebouwd, {N77.50} binnen en een terras van {N99.90} {U}, de brochure {N109.00}, {N77.30} en {N97.20}, en het portaal 109, 77 en 97. Wij bevestigen welke cijfers het contract hanteert.',
  'Rzuty podają powierzchnię zabudowy obejmującą część powierzchni wspólnych oraz drugą, większą powierzchnię zabudowy według dekretu 218/2005: {N110.58} {U} wobec {N100.00} {U} dla lokali 2 i 3. Portal dewelopera podaje jeszcze inne wartości, {N85} {U} zabudowy dla lokali 2 i 3. Dla lokalu 57 rzut podaje {N107.00} {U} zabudowy, {N77.50} wnętrza i taras o powierzchni {N99.90} {U}, broszura {N109.00}, {N77.30} i {N97.20}, a portal 109, 77 i 97. Potwierdzamy, które wartości przyjmuje umowa.',
  'Tegningene oppgir et bebygd areal som inkluderer en andel av fellesarealene, og et andre, større bebygd areal etter dekret 218/2005: {N110.58} {U} mot {N100.00} {U} for bolig 2 og 3. Utbyggerens portal oppgir enda andre tall, {N85} {U} bygd for bolig 2 og 3. For bolig 57 oppgir tegningen {N107.00} {U} bygd, {N77.50} innvendig og en terrasse på {N99.90} {U}, brosjyren {N109.00}, {N77.30} og {N97.20}, og portalen 109, 77 og 97. Vi bekrefter hvilke tall kontrakten bruker.',
  'Ritningarna anger en byggyta som inkluderar en andel av de gemensamma ytorna och en andra, större byggyta enligt dekret 218/2005: {N110.58} {U} mot {N100.00} {U} för bostad 2 och 3. Exploatörens portal anger ytterligare andra siffror, {N85} {U} byggyta för bostad 2 och 3. För bostad 57 anger ritningen {N107.00} {U} byggyta, {N77.50} inomhus och en terrass på {N99.90} {U}, broschyren {N109.00}, {N77.30} och {N97.20}, och portalen 109, 77 och 97. Vi bekräftar vilka siffror avtalet använder.')
a('The distances', 'Las distancias', 'Les distances', 'Die Entfernungen', 'Расстояния', 'المسافات', 'De afstanden', 'Avstandene', 'Avstandene', 'Avstånden')
a('The distances in the text are the developer’s own',
  'Las distancias del texto son las del propio promotor: dos minutos a pie hasta la playa, unos diez minutos en coche hasta Fuengirola y menos de 25 minutos hasta el aeropuerto de Málaga. Las cifras por carretera junto al mapa se miden desde un marcador aproximado de la parcela y difieren de ellas, así que confirmamos las distancias en una visita.',
  'Les distances du texte sont celles du promoteur : deux minutes à pied jusqu’à la plage, environ dix minutes en voiture jusqu’à Fuengirola et moins de 25 minutes jusqu’à l’aéroport de Malaga. Les chiffres routiers à côté de la carte sont mesurés depuis un repère approximatif de la parcelle et en diffèrent ; nous confirmons donc les distances lors d’une visite.',
  'Die Entfernungen im Text stammen vom Bauträger selbst: zwei Gehminuten zum Strand, etwa zehn Autominuten nach Fuengirola und unter 25 Minuten zum Flughafen Malaga. Die Straßenwerte neben der Karte sind von einer ungefähren Grundstücksmarkierung aus gemessen und weichen davon ab, deshalb bestätigen wir die Entfernungen bei einer Besichtigung.',
  'Расстояния в тексте — данные самого застройщика: две минуты пешком до пляжа, около десяти минут на машине до Фуэнхиролы и менее 25 минут до аэропорта Малаги. Дорожные цифры рядом с картой измерены от приблизительной отметки участка и отличаются от них, поэтому расстояния мы подтверждаем во время осмотра.',
  'المسافات المذكورة في النص هي مسافات المطوّر نفسه: دقيقتان سيرًا إلى الشاطئ، ونحو عشر دقائق بالسيارة إلى فوينخيرولا، وأقل من 25 دقيقة إلى مطار مالقة. أما أرقام الطرق بجانب الخريطة فتُقاس من علامة تقريبية للقطعة وتختلف عنها، لذلك نؤكد المسافات أثناء الزيارة.',
  'De afstanden in de tekst zijn die van de ontwikkelaar zelf: twee minuten lopen naar het strand, ongeveer tien minuten rijden naar Fuengirola en minder dan 25 minuten naar de luchthaven van Málaga. De wegcijfers naast de kaart zijn gemeten vanaf een bij benadering geplaatste markering van het perceel en wijken ervan af, dus bevestigen we de afstanden bij een bezichtiging.',
  'Odległości w tekście pochodzą od samego dewelopera: dwie minuty spacerem do plaży, około dziesięciu minut samochodem do Fuengiroli i mniej niż 25 minut do lotniska w Maladze. Drogowe wartości obok mapy są mierzone od przybliżonego znacznika działki i różnią się od nich, dlatego odległości potwierdzamy podczas wizyty.',
  'Avstandene i teksten er utbyggerens egne: to minutter å gå til stranden, omtrent ti minutter med bil til Fuengirola og under 25 minutter til Málaga lufthavn. Veitallene ved siden av kartet er målt fra en omtrentlig tomtemarkør og avviker fra dem, så vi bekrefter avstandene på en visning.',
  'Avstånden i texten är exploatörens egna: två minuters promenad till stranden, ungefär tio minuter med bil till Fuengirola och under 25 minuter till Málagas flygplats. Vägsiffrorna bredvid kartan mäts från en ungefärlig tomtmarkör och avviker från dem, så vi bekräftar avstånden vid ett besök.')
a('The developer’s portal lists home 2 with three bedrooms',
  'El portal del promotor da la vivienda 2 con tres dormitorios, mientras que su plano muestra dos dormitorios y dos baños, la misma distribución que la vivienda 3. Esta página muestra los dos dormitorios del plano y lo confirmamos por escrito.',
  'Le portail du promoteur indique le logement 2 avec trois chambres, alors que son plan montre deux chambres et deux salles de bains, la même distribution que le logement 3. Cette page montre les deux chambres du plan, et nous le confirmons par écrit.',
  'Das Portal des Bauträgers führt die Wohnung 2 mit drei Schlafzimmern auf, während ihr Plan zwei Schlafzimmer und zwei Bäder zeigt, derselbe Grundriss wie bei Wohnung 3. Diese Seite zeigt die zwei Schlafzimmer des Plans, und wir bestätigen das schriftlich.',
  'На портале застройщика квартира 2 указана с тремя спальнями, а на её плане две спальни и две ванные комнаты, такая же планировка, как у квартиры 3. На этой странице показаны две спальни по плану, и мы подтверждаем это письменно.',
  'تذكر بوابة المطوّر المسكن 2 بثلاث غرف نوم، بينما يُظهر مخططه غرفتي نوم وحمامين، وهو التوزيع نفسه للمسكن 3. وتعرض هذه الصفحة غرفتي النوم كما في المخطط، ونؤكد ذلك كتابةً.',
  'Het portaal van de ontwikkelaar vermeldt woning 2 met drie slaapkamers, terwijl de plattegrond twee slaapkamers en twee badkamers toont, dezelfde indeling als woning 3. Deze pagina toont de twee slaapkamers van de plattegrond en wij bevestigen dat schriftelijk.',
  'Portal dewelopera podaje lokal 2 z trzema sypialniami, podczas gdy jego rzut pokazuje dwie sypialnie i dwie łazienki, taki sam układ jak w lokalu 3. Ta strona pokazuje dwie sypialnie z rzutu, co potwierdzamy na piśmie.',
  'Utbyggerens portal oppfører bolig 2 med tre soverom, mens plantegningen viser to soverom og to bad, samme planløsning som bolig 3. Denne siden viser de to soverommene fra plantegningen, og vi bekrefter det skriftlig.',
  'Exploatörens portal listar bostad 2 med tre sovrum, medan dess planritning visar två sovrum och två badrum, samma planlösning som bostad 3. Den här sidan visar planritningens två sovrum, och vi bekräftar det skriftligen.')

# ---------------------------------------------------------------- availability
a('Five homes <em>currently listed</em>',
  'Cinco viviendas <em>a la venta ahora</em>', 'Cinq logements <em>actuellement listés</em>', 'Fünf Wohnungen <em>derzeit aufgeführt</em>',
  'Пять квартир <em>сейчас в списке</em>', 'خمسة مساكن <em>مدرجة حاليًا</em>', 'Vijf woningen <em>momenteel op de lijst</em>',
  'Pięć lokali <em>obecnie na liście</em>', 'Fem boliger <em>oppført nå</em>', 'Fem bostäder <em>listade just nu</em>')
a('Prices are those of the developer’s price list as of October 2026',
  'Los precios son los de la lista de precios del promotor a octubre de 2026 y se confirman antes de la reserva. Cinco de las 72 viviendas figuran con precio; los documentos del promotor no dicen que las otras 67 estén vendidas.',
  'Les prix sont ceux de la liste de prix du promoteur d’octobre 2026 et sont confirmés avant la réservation. Cinq des 72 logements sont listés ; les documents du promoteur ne disent pas que les 67 autres sont vendus.',
  'Die Preise sind die der Preisliste des Bauträgers vom Oktober 2026 und werden vor der Reservierung bestätigt. Fünf der 72 Wohnungen sind aufgeführt; die Unterlagen des Bauträgers sagen nicht, dass die übrigen 67 verkauft sind.',
  'Цены взяты из прайс-листа застройщика на октябрь 2026 года и подтверждаются до бронирования. В списке пять из 72 квартир; в документах застройщика не сказано, что остальные 67 проданы.',
  'الأسعار هي أسعار قائمة المطوّر في أكتوبر 2026 وتُؤكَّد قبل الحجز. خمسة من 72 مسكنًا مدرجة بالأسعار، ولا تذكر وثائق المطوّر أن المساكن الـ67 الأخرى مباعة.',
  'De prijzen zijn die van de prijslijst van de ontwikkelaar van oktober 2026 en worden vóór de reservering bevestigd. Vijf van de 72 woningen staan op de lijst; de documenten van de ontwikkelaar zeggen niet dat de overige 67 verkocht zijn.',
  'Ceny pochodzą z cennika dewelopera z października 2026 r. i są potwierdzane przed rezerwacją. Pięć z 72 lokali jest na liście; dokumenty dewelopera nie mówią, że pozostałe 67 są sprzedane.',
  'Prisene er de i utbyggerens prisliste fra oktober 2026 og bekreftes før reservasjon. Fem av de 72 boligene er oppført; utbyggerens dokumenter sier ikke at de øvrige 67 er solgt.',
  'Priserna är de i exploatörens prislista från oktober 2026 och bekräftas före reservation. Fem av de 72 bostäderna är listade; exploatörens dokument säger inte att de övriga 67 är sålda.')
a('Prices are transcribed from the developer’s price list as shown on its portal',
  'Los precios se han transcrito de la lista de precios del promotor tal como figura en su portal en octubre de 2026, y no incluyen el IVA. Las superficies son las del plano de cada vivienda: la superficie interior es la útil de la vivienda, la construida incluye una parte de las zonas comunes y la terraza es la cubierta y la descubierta juntas. El portal da otras superficies construidas e interiores para las mismas viviendas, y la vivienda 57 difiere entre su plano y el folleto; las diferencias se exponen en las comprobaciones de arriba.',
  'Les prix sont transcrits de la liste de prix du promoteur telle qu’elle figure sur son portail en octobre 2026, et s’entendent hors TVA. Les surfaces sont celles du plan de chaque logement : la surface intérieure est la surface utile du logement, la surface construite inclut une part des parties communes et la terrasse est la terrasse couverte et la terrasse découverte réunies. Le portail donne d’autres surfaces construites et intérieures pour les mêmes logements, et le logement 57 diffère entre son plan et la brochure ; les écarts sont exposés dans les vérifications ci-dessus.',
  'Die Preise sind aus der Preisliste des Bauträgers übernommen, wie sie im Oktober 2026 auf seinem Portal stand, und verstehen sich zuzüglich MwSt. Die Flächen sind die des Plans jeder Wohnung: Die Innenfläche ist die Nutzfläche der Wohnung, die bebaute Fläche enthält einen Anteil der Gemeinschaftsbereiche, und die Terrasse ist die überdachte und die unüberdachte Terrasse zusammen. Das Portal nennt für dieselben Wohnungen andere bebaute und Innenflächen, und die Wohnung 57 weicht zwischen ihrem Plan und der Broschüre ab; die Unterschiede sind in den Prüfpunkten oben dargestellt.',
  'Цены перенесены из прайс-листа застройщика в том виде, в каком он был размещён на его портале в октябре 2026 года, и указаны без НДС. Площади взяты с плана каждой квартиры: внутренняя площадь — это полезная площадь квартиры, застроенная площадь включает долю общих зон, а терраса — это крытая и открытая террасы вместе. Портал приводит для тех же квартир другие застроенные и внутренние площади, а квартира 57 отличается на плане и в брошюре; расхождения изложены в проверках выше.',
  'نُقلت الأسعار من قائمة أسعار المطوّر كما ظهرت على بوابته في أكتوبر 2026، وهي لا تشمل ضريبة القيمة المضافة. والمساحات هي مساحات مخطط كل مسكن: المساحة الداخلية هي المساحة الصالحة للاستخدام في المسكن، والمساحة المبنية تشمل حصة من المناطق المشتركة، والتراس هو التراس المغطى والمكشوف معًا. وتذكر البوابة مساحات مبنية وداخلية أخرى للمساكن نفسها، ويختلف المسكن 57 بين مخططه والكتيّب؛ وتُعرض الفروق في عمليات التحقق أعلاه.',
  'De prijzen zijn overgenomen uit de prijslijst van de ontwikkelaar zoals die in oktober 2026 op zijn portaal stond, en zijn exclusief btw. De oppervlakten zijn die van de plattegrond van elke woning: de binnenoppervlakte is de bruikbare oppervlakte van de woning, de bebouwde oppervlakte omvat een deel van de gemeenschappelijke ruimten en het terras is het overdekte en het onoverdekte terras samen. Het portaal geeft voor dezelfde woningen andere bebouwde en binnenoppervlakten, en woning 57 verschilt tussen de plattegrond en de brochure; de verschillen staan bij de controles hierboven.',
  'Ceny zostały przepisane z cennika dewelopera widocznego na jego portalu w październiku 2026 r. i nie obejmują VAT. Powierzchnie pochodzą z rzutu każdego lokalu: powierzchnia wnętrza to powierzchnia użytkowa lokalu, powierzchnia zabudowy obejmuje część powierzchni wspólnych, a taras to taras zadaszony i odkryty razem. Portal podaje dla tych samych lokali inne powierzchnie zabudowy i wnętrza, a lokal 57 różni się między rzutem a broszurą; różnice opisano w sprawdzanych kwestiach powyżej.',
  'Prisene er hentet fra utbyggerens prisliste slik den sto på portalen hans i oktober 2026, og inkluderer ikke mva. Arealene er de fra plantegningen for hver bolig: det innvendige arealet er boligens bruksareal, det bebygde arealet inkluderer en andel av fellesarealene, og terrassen er den overbygde og den åpne terrassen til sammen. Portalen oppgir andre bygde og innvendige arealer for de samme boligene, og bolig 57 avviker mellom plantegningen og brosjyren; forskjellene er satt opp under kontrollpunktene ovenfor.',
  'Priserna är hämtade från exploatörens prislista så som den stod på hans portal i oktober 2026, och inkluderar inte moms. Ytorna är de från planritningen för varje bostad: den inomhusytan är bostadens boyta, byggytan inkluderar en andel av de gemensamma ytorna och terrassen är den övertäckta och den öppna terrassen tillsammans. Portalen anger andra byggytor och inomhusytor för samma bostäder, och bostad 57 skiljer sig mellan sin planritning och broschyren; skillnaderna redovisas under kontrollpunkterna ovan.')

# ---------------------------------------------------------------- timeline, viewing, enquiry, FAQ
a('We confirm the reservation of EUR 6,000 plus VAT',
  'Confirmamos por escrito la reserva de {E6000} más IVA y el calendario de pagos, y después el contrato privado de compraventa.',
  'Nous confirmons par écrit la réservation de {E6000} hors TVA et l’échéancier de paiement, puis le contrat de vente privé.',
  'Wir bestätigen die Reservierung von {E6000} zuzüglich MwSt. und den Zahlungsplan schriftlich, dann folgt der private Kaufvertrag.',
  'Мы письменно подтверждаем бронирование {E6000} плюс НДС и график платежей, затем следует предварительный договор купли-продажи.',
  'نؤكد كتابةً الحجز بمبلغ {E6000} زائد ضريبة القيمة المضافة وجدول الدفعات، ثم عقد الشراء الخاص.',
  'Wij bevestigen de reservering van {E6000} plus btw en het betalingsschema schriftelijk, daarna volgt de onderhandse koopovereenkomst.',
  'Potwierdzamy na piśmie rezerwację {E6000} plus VAT i harmonogram płatności, a następnie umowę przedwstępną.',
  'Vi bekrefter reservasjonen på {E6000} pluss mva. og betalingsplanen skriftlig, deretter den private kjøpekontrakten.',
  'Vi bekräftar reservationen på {E6000} plus moms och betalningsplanen skriftligen, därefter det privata köpeavtalet.')
a('Visit the site and its surroundings with us.',
  'Visite con nosotros la parcela y sus alrededores.', 'Visitez avec nous le terrain et ses alentours.',
  'Besichtigen Sie mit uns das Grundstück und seine Umgebung.', 'Осмотрите участок и окрестности вместе с нами.',
  'زر معنا موقع المشروع ومحيطه.', 'Bezoek met ons het terrein en de omgeving.', 'Odwiedzą Państwo z nami teren i okolicę.',
  'Besøk tomten og omgivelsene sammen med oss.', 'Besök tomten och omgivningarna tillsammans med oss.')
a('We walk to the beach with you and time it.',
  'Caminamos con usted hasta la playa y cronometramos el trayecto.', 'Nous marchons avec vous jusqu’à la plage et chronométrons le trajet.',
  'Wir gehen mit Ihnen zum Strand und messen die Zeit.', 'Мы пройдём с вами до пляжа и засечём время.',
  'نمشي معكم إلى الشاطئ ونحتسب الوقت.', 'We lopen met u naar het strand en nemen de tijd op.', 'Przejdziemy z Państwem na plażę i zmierzymy czas.',
  'Vi går til stranden sammen med dere og tar tiden.', 'Vi går till stranden tillsammans med er och tar tid.')
a('Ask about <em>Brezo Residences</em>',
  'Pregunte por <em>Brezo Residences</em>', 'Renseignez-vous sur <em>Brezo Residences</em>', 'Fragen Sie nach <em>Brezo Residences</em>',
  'Узнайте о <em>Brezo Residences</em>', 'استفسر عن <em>Brezo Residences</em>', 'Vraag naar <em>Brezo Residences</em>',
  'Zapytanie o <em>Brezo Residences</em>', 'Spør om <em>Brezo Residences</em>', 'Fråga om <em>Brezo Residences</em>')
a('Hello Nueva Living, I would like information about Brezo Residences.',
  'Hola Nueva Living, me gustaría recibir información sobre Brezo Residences.',
  'Bonjour Nueva Living, je souhaiterais recevoir des informations sur Brezo Residences.',
  'Guten Tag Nueva Living, ich hätte gern Informationen zu Brezo Residences.',
  'Здравствуйте, Nueva Living! Хочу получить информацию о Brezo Residences.',
  'مرحبًا Nueva Living، أودّ الحصول على معلومات عن Brezo Residences.',
  'Hallo Nueva Living, ik ontvang graag informatie over Brezo Residences.',
  'Dzień dobry, Nueva Living, proszę o informacje o Brezo Residences.',
  'Hei Nueva Living, jeg vil gjerne ha informasjon om Brezo Residences.',
  'Hej Nueva Living, jag vill gärna ha information om Brezo Residences.')
a('The development has 72 homes with two, three and four bedrooms',
  'La promoción tiene 72 viviendas de dos, tres y cuatro dormitorios, y cinco figuran con precio: tres de dos dormitorios y dos de tres, de {E483500} a {E749000} más IVA.',
  'Le programme compte 72 logements de deux, trois et quatre chambres, et cinq sont listés avec un prix : trois de deux chambres et deux de trois, de {E483500} à {E749000} hors TVA.',
  'Die Anlage hat 72 Wohnungen mit zwei, drei und vier Schlafzimmern, und fünf sind mit Preis aufgeführt: drei mit zwei und zwei mit drei Schlafzimmern, von {E483500} bis {E749000} zuzüglich MwSt.',
  'В комплексе 72 квартиры с двумя, тремя и четырьмя спальнями, пять указаны с ценой: три с двумя спальнями и две с тремя, от {E483500} до {E749000} плюс НДС.',
  'يضم المشروع 72 مسكنًا بغرفتي نوم وثلاث وأربع غرف نوم، وخمسة منها مدرجة بالأسعار: ثلاثة بغرفتي نوم واثنان بثلاث غرف نوم، من {E483500} إلى {E749000} زائد ضريبة القيمة المضافة.',
  'Het project telt 72 woningen met twee, drie en vier slaapkamers, en vijf staan met een prijs op de lijst: drie met twee en twee met drie slaapkamers, van {E483500} tot {E749000} plus btw.',
  'Inwestycja liczy 72 lokale z dwiema, trzema i czterema sypialniami, a pięć jest na liście z ceną: trzy z dwiema i dwa z trzema sypialniami, od {E483500} do {E749000} plus VAT.',
  'Prosjektet har 72 boliger med to, tre og fire soverom, og fem er oppført med pris: tre med to og to med tre soverom, fra {E483500} til {E749000} pluss mva.',
  'Projektet har 72 bostäder med två, tre och fyra sovrum, och fem är listade med pris: tre med två och två med tre sovrum, från {E483500} till {E749000} plus moms.')
a('No. The prices exclude VAT, which the developer gives as 10%',
  'No. Los precios no incluyen el IVA, que el promotor cifra en el 10% en la reserva. Confirmamos por escrito los impuestos y los gastos de compra.',
  'Non. Les prix n’incluent pas la TVA, que le promoteur indique à 10 % sur la réservation. Nous confirmons par écrit les taxes et les frais d’achat.',
  'Nein. Die Preise verstehen sich zuzüglich MwSt., die der Bauträger bei der Reservierung mit 10 % angibt. Wir bestätigen Steuern und Kaufnebenkosten schriftlich.',
  'Нет. Цены указаны без НДС, который застройщик называет как 10 % для бронирования. Налоги и расходы на покупку мы письменно подтверждаем.',
  'لا. الأسعار لا تشمل ضريبة القيمة المضافة التي يذكرها المطوّر بنسبة 10% على الحجز. ونؤكد الضرائب ومصاريف الشراء كتابةً.',
  'Nee. De prijzen zijn exclusief btw, die de ontwikkelaar bij de reservering op 10% stelt. We bevestigen de belastingen en aankoopkosten schriftelijk.',
  'Nie. Ceny nie obejmują VAT, który deweloper określa na 10% przy rezerwacji. Podatki i koszty zakupu potwierdzamy na piśmie.',
  'Nei. Prisene inkluderer ikke mva., som utbyggeren setter til 10 % på reservasjonen. Vi bekrefter skatter og kjøpskostnader skriftlig.',
  'Nej. Priserna inkluderar inte moms, som exploatören anger till 10 % på reservationen. Vi bekräftar skatter och köpkostnader skriftligen.')
a('Yes. The developer says every home has at least one parking space',
  'Sí. El promotor indica que cada vivienda tiene al menos una plaza de aparcamiento y un trastero.',
  'Oui. Le promoteur indique que chaque logement dispose d’au moins une place de stationnement et d’une cave.',
  'Ja. Der Bauträger gibt an, dass jede Wohnung mindestens einen Stellplatz und einen Abstellraum hat.',
  'Да. Застройщик сообщает, что у каждой квартиры есть как минимум одно парковочное место и кладовая.',
  'نعم. يذكر المطوّر أن لكل مسكن موقف سيارات واحدًا على الأقل وغرفة تخزين.',
  'Ja. De ontwikkelaar geeft aan dat elke woning minstens één parkeerplaats en een berging heeft.',
  'Tak. Deweloper podaje, że każdy lokal ma co najmniej jedno miejsce postojowe i komórkę.',
  'Ja. Utbyggeren oppgir at hver bolig har minst én parkeringsplass og en bod.',
  'Ja. Exploatören anger att varje bostad har minst en parkeringsplats och ett förråd.')
a('None of the developer’s documents gives a completion date. We ask for the contractual date, the licence status',
  'Ninguno de los documentos del promotor da una fecha de finalización. Pedimos la fecha contractual, el estado de la licencia y la fase de las obras.',
  'Aucun des documents du promoteur ne donne de date d’achèvement. Nous demandons la date contractuelle, l’état du permis et l’avancement des travaux.',
  'Keine der Unterlagen des Bauträgers nennt ein Fertigstellungsdatum. Wir fragen das vertragliche Datum, den Stand der Genehmigung und den Baufortschritt an.',
  'Ни в одном из документов застройщика нет даты завершения строительства. Мы запрашиваем договорную дату, статус разрешения и стадию работ.',
  'لا تذكر أي من وثائق المطوّر موعد إنجاز. نطلب التاريخ التعاقدي وحالة الرخصة ومرحلة الأعمال.',
  'Geen van de documenten van de ontwikkelaar geeft een opleverdatum. We vragen naar de contractuele datum, de status van de vergunning en de stand van de werken.',
  'Żaden z dokumentów dewelopera nie podaje terminu ukończenia. Prosimy o termin wskazany w umowie, status pozwolenia i etap prac.',
  'Ingen av utbyggerens dokumenter oppgir en ferdigstillelsesdato. Vi ber om den kontraktsfestede datoen, status for tillatelsen og byggestadiet.',
  'Inget av exploatörens dokument anger ett slutdatum. Vi ber om det avtalade datumet, bygglovets status och byggstadiet.')
a('The reservation is EUR 6,000 plus 10% VAT. Then 30%',
  'La reserva es de {E6000} más el 10% de IVA. Luego, el 30% más IVA con el contrato privado y el 70% más IVA ante notario a la finalización.',
  'La réservation est de {E6000} plus 10 % de TVA. Ensuite, 30 % hors TVA au contrat privé et 70 % hors TVA chez le notaire à l’achèvement.',
  'Die Reservierung beträgt {E6000} zuzüglich 10 % MwSt. Dann 30 % zuzüglich MwSt. bei Unterzeichnung des privaten Kaufvertrags und 70 % zuzüglich MwSt. bei Fertigstellung beim Notar.',
  'Бронирование стоит {E6000} плюс НДС 10 %. Затем 30 % плюс НДС при подписании предварительного договора и 70 % плюс НДС у нотариуса при завершении сделки.',
  'الحجز {E6000} زائد ضريبة القيمة المضافة 10%. ثم 30% زائد الضريبة عند العقد الخاص، و70% زائد الضريبة أمام كاتب العدل عند الإتمام.',
  'De reservering bedraagt {E6000} plus 10% btw. Daarna 30% plus btw bij de onderhandse overeenkomst en 70% plus btw bij oplevering ten overstaan van de notaris.',
  'Rezerwacja wynosi {E6000} plus VAT 10%. Następnie 30% plus VAT przy umowie przedwstępnej i 70% plus VAT u notariusza, przy akcie notarialnym.',
  'Reservasjonen er {E6000} pluss 10 % mva. Deretter 30 % pluss mva. ved den private kontrakten og 70 % pluss mva. hos notarius ved overtakelse.',
  'Reservationen är {E6000} plus 10 % moms. Därefter 30 % plus moms vid det privata avtalet och 70 % plus moms hos notarien vid tillträdet.')

json.dump(T, open(f'{SP}/tr_b.json', 'w'), ensure_ascii=False, indent=1)
print('tr_b entries', len(T))
