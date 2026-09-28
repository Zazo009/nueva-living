# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Eight of 46 apartments available in two gated blocks above Mijas Costa, with a communal pool, gardens and a chill-out terrace, parking and a storeroom with every home.",
 "Ocho de 46 apartamentos disponibles en dos bloques cerrados sobre Mijas Costa, con piscina comunitaria, jardines y terraza chill-out, y plaza de aparcamiento y trastero con cada vivienda.",
 "Huit des 46 appartements disponibles dans deux immeubles fermés au-dessus de Mijas Costa, avec piscine commune, jardins et terrasse chill-out, place de parking et débarras pour chaque logement.",
 "Acht von 46 Wohnungen verfügbar in zwei geschlossenen Gebäuden oberhalb von Mijas Costa, mit Gemeinschaftspool, Gärten und Chill-out-Terrasse sowie Stellplatz und Abstellraum zu jeder Wohnung.",
 "Восемь из 46 квартир доступны в двух закрытых корпусах над Михас-Костой, с общим бассейном, садами и зоной chill-out, а также парковочным местом и кладовой к каждой квартире.",
 "ثماني من 46 شقة متاحة في مبنيين مغلقين فوق ميخاس كوستا، مع مسبح مشترك وحدائق وتراس استرخاء، وموقف سيارة ومخزن مع كل منزل.",
 "Acht van de 46 appartementen beschikbaar in twee besloten blokken boven Mijas Costa, met gemeenschappelijk zwembad, tuinen en een chill-outterras, plus parkeerplaats en berging bij elke woning.",
 "Osiem z 46 apartamentów dostępnych w dwóch zamkniętych budynkach nad Mijas Costa, z basenem wspólnym, ogrodami i tarasem chill-out oraz miejscem postojowym i komórką przy każdym mieszkaniu.",
 "Åtte av 46 leiligheter tilgjengelige i to lukkede bygg over Mijas Costa, med fellesbasseng, hager og chill-out-terrasse, samt parkeringsplass og bod til hver bolig.",
 "Åtta av 46 lägenheter tillgängliga i två slutna hus ovanför Mijas Costa, med gemensam pool, trädgårdar och chill out-terrass, samt parkeringsplats och förråd till varje bostad.")
a("Eight of 46 new-build apartments available above Mijas Costa: two and three bedrooms, 97 to 137 sqm built, gardens to 81.80 sqm, from EUR 421,600 net of tax.",
 "Ocho de 46 apartamentos de obra nueva disponibles sobre Mijas Costa: dos y tres dormitorios, de 97 a 137 m² construidos, jardines hasta 81,80 m², desde 421.600 € más impuestos.",
 "Huit des 46 appartements neufs disponibles au-dessus de Mijas Costa : deux et trois chambres, de 97 à 137 m² construits, jardins jusqu'à 81,80 m², à partir de 421 600 € hors taxes.",
 "Acht von 46 Neubauwohnungen verfügbar oberhalb von Mijas Costa: zwei und drei Schlafzimmer, 97 bis 137 m² Wohnfläche, Gärten bis 81,80 m², ab 421.600 € zuzüglich Steuern.",
 "Восемь из 46 новых квартир над Михас-Костой: две и три спальни, от 97 до 137 м² построенной площади, сады до 81,80 м², от 421 600 € без учёта налогов.",
 "ثماني من 46 شقة جديدة متاحة فوق ميخاس كوستا: غرفتان وثلاث غرف نوم، من 97 إلى 137 م² مبنية، وحدائق حتى 81.80 م²، تبدأ من 421,600 € دون الضرائب.",
 "Acht van de 46 nieuwbouwappartementen beschikbaar boven Mijas Costa: twee en drie slaapkamers, 97 tot 137 m² bouwoppervlak, tuinen tot 81,80 m², vanaf € 421.600 exclusief belastingen.",
 "Osiem z 46 nowych apartamentów dostępnych nad Mijas Costa: dwie i trzy sypialnie, od 97 do 137 m² powierzchni zabudowanej, ogrody do 81,80 m², od 421 600 € bez podatków.",
 "Åtte av 46 nye leiligheter tilgjengelige over Mijas Costa: to og tre soverom, 97 til 137 m² bygget, hager opptil 81,80 m², fra 421 600 € eksklusive avgifter.",
 "Åtta av 46 nyproducerade lägenheter tillgängliga ovanför Mijas Costa: två och tre sovrum, 97 till 137 m² byggyta, trädgårdar upp till 81,80 m², från 421 600 € exklusive skatter.")
a("Mijas Costa","Mijas Costa","Mijas Costa","Mijas Costa","Михас-Коста","ميخاس كوستا","Mijas Costa","Mijas Costa","Mijas Costa","Mijas Costa")
a("Completion Q3 2027","Entrega T3 2027","Livraison T3 2027","Fertigstellung Q3 2027","Сдача 3 кв. 2027",
 "الإنجاز الربع الثالث 2027","Oplevering K3 2027","Zakończenie III kw. 2027","Ferdigstilling K3 2027","Färdigställande K3 2027")
a("Eight of 46 apartments in two gated blocks above Mijas Costa, with a communal pool, gardens and a chill-out terrace.",
 "Ocho de 46 apartamentos en dos bloques cerrados sobre Mijas Costa, con piscina comunitaria, jardines y terraza chill-out.",
 "Huit des 46 appartements dans deux immeubles fermés au-dessus de Mijas Costa, avec piscine commune, jardins et terrasse chill-out.",
 "Acht von 46 Wohnungen in zwei geschlossenen Gebäuden oberhalb von Mijas Costa, mit Gemeinschaftspool, Gärten und Chill-out-Terrasse.",
 "Восемь из 46 квартир в двух закрытых корпусах над Михас-Костой, с общим бассейном, садами и зоной chill-out.",
 "ثماني من 46 شقة في مبنيين مغلقين فوق ميخاس كوستا، مع مسبح مشترك وحدائق وتراس استرخاء.",
 "Acht van de 46 appartementen in twee besloten blokken boven Mijas Costa, met gemeenschappelijk zwembad, tuinen en een chill-outterras.",
 "Osiem z 46 apartamentów w dwóch zamkniętych budynkach nad Mijas Costa, z basenem wspólnym, ogrodami i tarasem chill-out.",
 "Åtte av 46 leiligheter i to lukkede bygg over Mijas Costa, med fellesbasseng, hager og chill-out-terrasse.",
 "Åtta av 46 lägenheter i två slutna hus ovanför Mijas Costa, med gemensam pool, trädgårdar och chill out-terrass.")
a("Developer visuals of the homes, the pool and the communal gardens.",
 "Imágenes del promotor de las viviendas, la piscina y los jardines comunes.",
 "Visuels du promoteur des logements, de la piscine et des jardins communs.",
 "Bauträger-Visualisierungen der Wohnungen, des Pools und der Gemeinschaftsgärten.",
 "Визуализации застройщика: квартиры, бассейн и общие сады.",
 "تصورات من المطور للمنازل والمسبح والحدائق المشتركة.",
 "Beelden van de ontwikkelaar van de woningen, het zwembad en de gemeenschappelijke tuinen.",
 "Wizualizacje dewelopera mieszkań, basenu i ogrodów wspólnych.",
 "Visualiseringer fra utbygger av boligene, bassenget og fellesehagene.",
 "Visualiseringar från utvecklaren av bostäderna, poolen och de gemensamma trädgårdarna.")
a("Developer visual of the two blocks and their pools on the wooded slope above the road",
 "Imagen del promotor de los dos bloques y sus piscinas en la ladera arbolada sobre la carretera",
 "Visuel du promoteur des deux immeubles et de leurs piscines sur le coteau boisé au-dessus de la route",
 "Bauträger-Visualisierung der beiden Gebäude und ihrer Pools am bewaldeten Hang über der Straße",
 "Визуализация застройщика: два корпуса и их бассейны на лесистом склоне над дорогой",
 "تصور من المطور للمبنيين ومسبحيهما على المنحدر المشجّر فوق الطريق",
 "Beeld van de ontwikkelaar van de twee blokken en hun zwembaden op de beboste helling boven de weg",
 "Wizualizacja dewelopera przedstawiająca dwa budynki i ich baseny na zalesionym zboczu nad drogą",
 "Visualisering fra utbygger av de to byggene og bassengene deres i den skogkledde skråningen over veien",
 "Visualisering från utvecklaren av de två husen och deras pooler i den skogbevuxna sluttningen ovanför vägen")
a("The two blocks from above","Los dos bloques desde el aire","Les deux immeubles vus d'en haut","Die beiden Gebäude von oben",
 "Два корпуса сверху","المبنيان من الأعلى","De twee blokken van bovenaf","Dwa budynki z góry","De to byggene ovenfra","De två husen uppifrån")
a("Developer visual of the communal pool at dusk, loungers and parasols along its edge",
 "Imagen del promotor de la piscina comunitaria al atardecer, con tumbonas y sombrillas en el borde",
 "Visuel du promoteur de la piscine commune au crépuscule, transats et parasols le long du bord",
 "Bauträger-Visualisierung des Gemeinschaftspools in der Dämmerung, mit Liegen und Sonnenschirmen am Rand",
 "Визуализация застройщика: общий бассейн в сумерках, шезлонги и зонты вдоль края",
 "تصور من المطور للمسبح المشترك عند الغسق مع كراسي التشمس والمظلات على حافته",
 "Beeld van de ontwikkelaar van het gemeenschappelijke zwembad in de schemering, met ligbedden en parasols langs de rand",
 "Wizualizacja dewelopera przedstawiająca basen wspólny o zmierzchu, z leżakami i parasolami przy brzegu",
 "Visualisering fra utbygger av fellesbassenget i skumringen, med solsenger og parasoller langs kanten",
 "Visualisering från utvecklaren av den gemensamma poolen i skymningen, med solsängar och parasoll längs kanten")
a("Developer visual of the planted balconies above the pool, the sea beyond",
 "Imagen del promotor de las terrazas ajardinadas sobre la piscina, con el mar al fondo",
 "Visuel du promoteur des balcons plantés au-dessus de la piscine, la mer au fond",
 "Bauträger-Visualisierung der bepflanzten Balkone über dem Pool, dahinter das Meer",
 "Визуализация застройщика: озеленённые балконы над бассейном, за ними море",
 "تصور من المطور للشرفات المزروعة فوق المسبح والبحر في الخلفية",
 "Beeld van de ontwikkelaar van de beplante balkons boven het zwembad, met de zee erachter",
 "Wizualizacja dewelopera przedstawiająca obsadzone zielenią balkony nad basenem, z morzem w tle",
 "Visualisering fra utbygger av de beplantede balkongene over bassenget, med havet bak",
 "Visualisering från utvecklaren av de planterade balkongerna ovanför poolen, med havet bakom")
a("Balconies over the pool","Terrazas sobre la piscina","Balcons au-dessus de la piscine","Balkone über dem Pool",
 "Балконы над бассейном","شرفات فوق المسبح","Balkons boven het zwembad","Balkony nad basenem","Balkonger over bassenget","Balkonger ovanför poolen")
a("Developer visual of a block lit at dusk, seen from the parking approach",
 "Imagen del promotor de un bloque iluminado al atardecer, visto desde el acceso al aparcamiento",
 "Visuel du promoteur d'un immeuble éclairé au crépuscule, vu depuis l'accès au parking",
 "Bauträger-Visualisierung eines beleuchteten Gebäudes in der Dämmerung, von der Parkplatzzufahrt aus",
 "Визуализация застройщика: подсвеченный корпус в сумерках со стороны въезда на парковку",
 "تصور من المطور لمبنى مضاء عند الغسق من مدخل المواقف",
 "Beeld van de ontwikkelaar van een verlicht blok in de schemering, gezien vanaf de parkeeroprit",
 "Wizualizacja dewelopera przedstawiająca oświetlony budynek o zmierzchu, widziany od strony wjazdu na parking",
 "Visualisering fra utbygger av et opplyst bygg i skumringen, sett fra parkeringsadkomsten",
 "Visualisering från utvecklaren av ett upplyst hus i skymningen, sett från parkeringsinfarten")
a("The approach at dusk","El acceso al atardecer","L'accès au crépuscule","Die Zufahrt in der Dämmerung",
 "Подъезд в сумерках","المدخل عند الغسق","De oprit in de schemering","Wjazd o zmierzchu","Adkomsten i skumringen","Infarten i skymningen")
a("Developer visual of a terrace with a table and chairs, looking over the rooftops to the sea",
 "Imagen del promotor de una terraza con mesa y sillas, con vistas sobre los tejados hasta el mar",
 "Visuel du promoteur d'une terrasse avec table et chaises, avec vue par-dessus les toits jusqu'à la mer",
 "Bauträger-Visualisierung einer Terrasse mit Tisch und Stühlen, mit Blick über die Dächer zum Meer",
 "Визуализация застройщика: терраса со столом и стульями, вид поверх крыш на море",
 "تصور من المطور لتراس بطاولة وكراسي بإطلالة فوق الأسطح إلى البحر",
 "Beeld van de ontwikkelaar van een terras met tafel en stoelen, met uitzicht over de daken naar de zee",
 "Wizualizacja dewelopera przedstawiająca taras ze stołem i krzesłami, z widokiem ponad dachami na morze",
 "Visualisering fra utbygger av en terrasse med bord og stoler, med utsikt over takene mot havet",
 "Visualisering från utvecklaren av en terrass med bord och stolar, med utsikt över taken mot havet")
a("A terrace and the sea","Una terraza y el mar","Une terrasse et la mer","Eine Terrasse und das Meer",
 "Терраса и море","تراس والبحر","Een terras en de zee","Taras i morze","En terrasse og havet","En terrass och havet")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
