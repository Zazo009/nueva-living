# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 2 of 2.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Eighty homes, <em>eight blocks</em>",
 "Ochenta viviendas, <em>ocho bloques</em>","Quatre-vingts logements, <em>huit blocs</em>",
 "Achtzig Wohnungen, <em>acht Blöcke</em>","Восемьдесят квартир, <em>восемь корпусов</em>",
 "ثمانون مسكناً، <em>ثمانية مبانٍ</em>","Tachtig woningen, <em>acht blokken</em>",
 "Osiemdziesiąt mieszkań, <em>osiem budynków</em>","Åtti boliger, <em>åtte blokker</em>",
 "Åttio bostäder, <em>åtta huskroppar</em>")

a("Eight blocks of ten homes at Altos de los Monteros, on the hillside above Marbella's eastern coast.",
 "Ocho bloques de diez viviendas en Altos de los Monteros, en la ladera sobre la costa este de Marbella.",
 "Huit blocs de dix logements à Altos de los Monteros, sur le coteau qui domine la côte est de Marbella.",
 "Acht Blöcke mit je zehn Wohnungen in Altos de los Monteros, am Hang über der Ostküste von Marbella.",
 "Восемь корпусов по десять квартир в Альтос-де-лос-Монтерос, на склоне над восточным побережьем Марбельи.",
 "ثمانية مبانٍ من عشرة مساكن لكل منها في ألتوس دي لوس مونتيروس، على المنحدر فوق الساحل الشرقي لمربيّا.",
 "Acht blokken van tien woningen in Altos de los Monteros, op de helling boven de oostkust van Marbella.",
 "Osiem budynków po dziesięć mieszkań w Altos de los Monteros, na zboczu nad wschodnim wybrzeżem Marbelli.",
 "Åtte blokker med ti boliger hver i Altos de los Monteros, i skråningen over Marbellas østkyst.",
 "Åtta huskroppar med tio bostäder vardera i Altos de los Monteros, i sluttningen ovanför Marbellas östra kust.")

a("The blocks do not sit level with each other. Each one is set a step higher than the block to its south, so that no home looks into the roof of its neighbour and every one of the eighty is turned to the sea.",
 "Los bloques no están al mismo nivel. Cada uno se sitúa un escalón por encima del que tiene al sur, de modo que ninguna vivienda mira al tejado de la vecina y las ochenta quedan orientadas al mar.",
 "Les blocs ne sont pas de niveau entre eux. Chacun est implanté un cran plus haut que celui situé au sud, si bien qu'aucun logement ne donne sur le toit du voisin et que les quatre-vingts sont tournés vers la mer.",
 "Die Blöcke liegen nicht auf gleicher Höhe. Jeder steht eine Stufe höher als der südlich davon, sodass keine Wohnung auf das Dach der Nachbarwohnung blickt und alle achtzig zum Meer ausgerichtet sind.",
 "Корпуса стоят не на одном уровне. Каждый расположен на ступень выше того, что южнее, поэтому ни одна квартира не смотрит на крышу соседней, и все восемьдесят обращены к морю.",
 "المباني ليست على مستوى واحد. كل مبنى يقع درجة أعلى من المبنى الذي يقع جنوبه، فلا يطلّ أي مسكن على سطح جاره، وتكون المساكن الثمانون جميعها مطلّة على البحر.",
 "De blokken staan niet op gelijke hoogte. Elk blok ligt een trede hoger dan het blok ten zuiden ervan, zodat geen enkele woning op het dak van de buren uitkijkt en alle tachtig op zee gericht zijn.",
 "Budynki nie stoją na jednym poziomie. Każdy jest osadzony o stopień wyżej niż ten położony na południe od niego, dzięki czemu żadne mieszkanie nie patrzy na dach sąsiada, a wszystkie osiemdziesiąt zwrócone są ku morzu.",
 "Blokkene ligger ikke på samme nivå. Hver enkelt er satt et trinn høyere enn blokken sør for den, slik at ingen bolig ser inn på taket til naboen og alle åtti er vendt mot sjøen.",
 "Huskropparna ligger inte i nivå med varandra. Var och en är satt ett steg högre än den som ligger söder om den, så att ingen bostad tittar in i grannens tak och alla åttio är vända mot havet.")

a("Two and three bedroom apartments, and duplex penthouses with a solarium.",
 "Apartamentos de dos y tres dormitorios, y áticos dúplex con solárium.",
 "Appartements de deux et trois chambres, et penthouses duplex avec solarium.",
 "Wohnungen mit zwei und drei Schlafzimmern sowie Duplex-Penthäuser mit Solarium.",
 "Квартиры с двумя и тремя спальнями и двухуровневые пентхаусы с солярием.",
 "شقق بغرفتي وثلاث غرف نوم، وبنتهاوس دوبلكس مع سولاريوم.",
 "Appartementen met twee en drie slaapkamers, en duplexpenthouses met solarium.",
 "Apartamenty dwu- i trzysypialniane oraz penthouse'y dwupoziomowe z solarium.",
 "Leiligheter med to og tre soverom, og toppleiligheter over to plan med solterrasse.",
 "Lägenheter med två och tre sovrum, och takvåningar i två plan med solterrass.")

a("Two and three bedrooms, 96.81 to 124.53 sqm of interior floor area.",
 "Dos y tres dormitorios, de 96,81 a 124,53 m² de superficie interior.",
 "Deux et trois chambres, de 96,81 à 124,53 m² de surface intérieure.",
 "Zwei und drei Schlafzimmer, 96,81 bis 124,53 m² Innenfläche.",
 "Две и три спальни, от 96,81 до 124,53 м² внутренней площади.",
 "غرفتان وثلاث غرف نوم، من 96.81 إلى 124.53 م² مساحة داخلية.",
 "Twee en drie slaapkamers, 96,81 tot 124,53 m² binnenoppervlak.",
 "Dwie i trzy sypialnie, od 96,81 do 124,53 m² powierzchni wewnętrznej.",
 "To og tre soverom, 96,81 til 124,53 m² innvendig areal.",
 "Två och tre sovrum, 96,81 till 124,53 m² invändig yta.")

a("Terraces from 22.09 to 67.18 sqm, covered, open or both.",
 "Terrazas de 22,09 a 67,18 m², cubiertas, abiertas o ambas.",
 "Terrasses de 22,09 à 67,18 m², couvertes, ouvertes ou les deux.",
 "Terrassen von 22,09 bis 67,18 m², überdacht, offen oder beides.",
 "Террасы от 22,09 до 67,18 м², крытые, открытые или и те и другие.",
 "تراسات من 22.09 إلى 67.18 م²، مغطّاة أو مفتوحة أو كلاهما.",
 "Terrassen van 22,09 tot 67,18 m², overdekt, open of beide.",
 "Tarasy od 22,09 do 67,18 m², zadaszone, otwarte lub jedno i drugie.",
 "Terrasser fra 22,09 til 67,18 m², overbygde, åpne eller begge deler.",
 "Terrasser från 22,09 till 67,18 m², täckta, öppna eller både och.")

a("Open-plan living and kitchen running out to the terrace.",
 "Salón y cocina en planta abierta que salen a la terraza.",
 "Séjour et cuisine ouverts prolongés par la terrasse.",
 "Offener Wohn- und Kochbereich, der auf die Terrasse übergeht.",
 "Объединённая гостиная с кухней, выходящая на террасу.",
 "صالة ومطبخ بتصميم مفتوح يمتدّان إلى التراس.",
 "Open woonkamer en keuken die doorlopen naar het terras.",
 "Otwarty salon z kuchnią przechodzący na taras.",
 "Åpen stue og kjøkken som går rett ut på terrassen.",
 "Öppen planlösning med vardagsrum och kök som går ut mot terrassen.")

a("Two parking spaces and a storeroom with every apartment, included in the price.",
 "Dos plazas de garaje y un trastero con cada apartamento, incluidos en el precio.",
 "Deux places de parking et un débarras avec chaque appartement, inclus dans le prix.",
 "Zwei Stellplätze und ein Abstellraum zu jeder Wohnung, im Preis enthalten.",
 "Два машиноместа и кладовая с каждой квартирой, включены в цену.",
 "موقفا سيارات ومخزن مع كل شقة، مشمولة في السعر.",
 "Twee parkeerplaatsen en een berging bij elk appartement, inbegrepen in de prijs.",
 "Dwa miejsca postojowe i komórka lokatorska przy każdym apartamencie, wliczone w cenę.",
 "To parkeringsplasser og en bod til hver leilighet, inkludert i prisen.",
 "Två parkeringsplatser och ett förråd till varje lägenhet, inkluderade i priset.")

a("The duplex penthouses",
 "Los áticos dúplex","Les penthouses duplex","Die Duplex-Penthäuser","Двухуровневые пентхаусы",
 "البنتهاوس الدوبلكس","De duplexpenthouses","Penthouse'y dwupoziomowe","Toppleilighetene over to plan","Takvåningarna i två plan")

a("Three bedrooms and three bathrooms, 118.62 to 120.63 sqm of interior floor area.",
 "Tres dormitorios y tres baños, de 118,62 a 120,63 m² de superficie interior.",
 "Trois chambres et trois salles de bains, de 118,62 à 120,63 m² de surface intérieure.",
 "Drei Schlafzimmer und drei Bäder, 118,62 bis 120,63 m² Innenfläche.",
 "Три спальни и три ванные, от 118,62 до 120,63 м² внутренней площади.",
 "ثلاث غرف نوم وثلاثة حمّامات، من 118.62 إلى 120.63 م² مساحة داخلية.",
 "Drie slaapkamers en drie badkamers, 118,62 tot 120,63 m² binnenoppervlak.",
 "Trzy sypialnie i trzy łazienki, od 118,62 do 120,63 m² powierzchni wewnętrznej.",
 "Tre soverom og tre bad, 118,62 til 120,63 m² innvendig areal.",
 "Tre sovrum och tre badrum, 118,62 till 120,63 m² invändig yta.")

a("A private solarium of around 56 sqm on top of a covered terrace of around 29 sqm.",
 "Un solárium privado de unos 56 m² sobre una terraza cubierta de unos 29 m².",
 "Un solarium privatif d'environ 56 m² au-dessus d'une terrasse couverte d'environ 29 m².",
 "Ein privates Solarium von rund 56 m² über einer überdachten Terrasse von rund 29 m².",
 "Собственный солярий около 56 м² над крытой террасой около 29 м².",
 "سولاريوم خاص بمساحة نحو 56 م² فوق تراس مغطّى بمساحة نحو 29 م².",
 "Een privésolarium van circa 56 m² boven een overdekt terras van circa 29 m².",
 "Prywatne solarium o powierzchni około 56 m² nad zadaszonym tarasem około 29 m².",
 "En privat solterrasse på rundt 56 m² over en overbygd terrasse på rundt 29 m².",
 "En privat solterrass på cirka 56 m² ovanpå en täckt terrass på cirka 29 m².")

a("Total outdoor area of 83.81 to 85.19 sqm, larger than two thirds of the interior.",
 "Superficie exterior total de 83,81 a 85,19 m², mayor que dos tercios del interior.",
 "Surface extérieure totale de 83,81 à 85,19 m², soit plus des deux tiers de l'intérieur.",
 "Gesamte Außenfläche von 83,81 bis 85,19 m², mehr als zwei Drittel der Innenfläche.",
 "Общая площадь открытых пространств от 83,81 до 85,19 м², больше двух третей внутренней.",
 "إجمالي المساحة الخارجية من 83.81 إلى 85.19 م²، أي أكثر من ثلثي المساحة الداخلية.",
 "Totaal buitenoppervlak van 83,81 tot 85,19 m², meer dan twee derde van het binnenoppervlak.",
 "Łączna powierzchnia zewnętrzna od 83,81 do 85,19 m², czyli ponad dwie trzecie powierzchni wewnętrznej.",
 "Samlet uteareal på 83,81 til 85,19 m², mer enn to tredeler av det innvendige.",
 "Total utomhusyta på 83,81 till 85,19 m², mer än två tredjedelar av den invändiga.")

a("Three parking spaces and a storeroom, included in the price.",
 "Tres plazas de garaje y un trastero, incluidos en el precio.",
 "Trois places de parking et un débarras, inclus dans le prix.",
 "Drei Stellplätze und ein Abstellraum, im Preis enthalten.",
 "Три машиноместа и кладовая, включены в цену.",
 "ثلاثة مواقف سيارات ومخزن، مشمولة في السعر.",
 "Drie parkeerplaatsen en een berging, inbegrepen in de prijs.",
 "Trzy miejsca postojowe i komórka lokatorska, wliczone w cenę.",
 "Tre parkeringsplasser og en bod, inkludert i prisen.",
 "Tre parkeringsplatser och ett förråd, inkluderade i priset.")

a("12 of the 20 released homes <em>available</em>",
 "12 de las 20 viviendas puestas a la venta <em>disponibles</em>",
 "12 des 20 logements mis en vente <em>disponibles</em>",
 "12 der 20 freigegebenen Wohnungen <em>verfügbar</em>",
 "12 из 20 выведенных в продажу квартир <em>доступны</em>",
 "12 من المساكن العشرين المطروحة <em>متاحة</em>",
 "12 van de 20 vrijgegeven woningen <em>beschikbaar</em>",
 "12 z 20 wprowadzonych do sprzedaży mieszkań <em>dostępnych</em>",
 "12 av de 20 boligene som er lagt ut er <em>ledige</em>",
 "12 av de 20 bostäder som släppts är <em>lediga</em>")

a("The seller has released twenty of the eighty homes so far. Twelve are available, seven are sold and one is reserved. Nueva Living reconfirms price and availability before any viewing or reservation.",
 "El vendedor ha puesto a la venta veinte de las ochenta viviendas hasta ahora. Doce están disponibles, siete vendidas y una reservada. Nueva Living reconfirma precio y disponibilidad antes de cualquier visita o reserva.",
 "Le vendeur a mis en vente vingt des quatre-vingts logements à ce jour. Douze sont disponibles, sept vendus et un réservé. Nueva Living reconfirme le prix et la disponibilité avant toute visite ou réservation.",
 "Der Verkäufer hat bislang zwanzig der achtzig Wohnungen freigegeben. Zwölf sind verfügbar, sieben verkauft und eine reserviert. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung erneut.",
 "На сегодня продавец вывел в продажу двадцать из восьмидесяти квартир. Двенадцать доступны, семь проданы, одна забронирована. Nueva Living заново подтверждает цену и наличие перед любым просмотром или бронированием.",
 "طرح البائع حتى الآن عشرين مسكناً من أصل ثمانين. اثنا عشر متاحة، وسبعة مباعة، وواحد محجوز. تعيد Nueva Living تأكيد السعر والتوافر قبل أي معاينة أو حجز.",
 "De verkoper heeft tot nu toe twintig van de tachtig woningen vrijgegeven. Twaalf zijn beschikbaar, zeven verkocht en één gereserveerd. Nueva Living bevestigt prijs en beschikbaarheid opnieuw vóór elke bezichtiging of reservering.",
 "Sprzedający wprowadził dotąd do sprzedaży dwadzieścia z osiemdziesięciu mieszkań. Dwanaście jest dostępnych, siedem sprzedanych, a jedno zarezerwowane. Nueva Living ponownie potwierdza cenę i dostępność przed każdą prezentacją lub rezerwacją.",
 "Selgeren har så langt lagt ut tjue av de åtti boligene. Tolv er ledige, sju er solgt og én er reservert. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning eller reservasjon.",
 "Säljaren har hittills släppt tjugo av de åttio bostäderna. Tolv är lediga, sju sålda och en reserverad. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning eller bokning.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
