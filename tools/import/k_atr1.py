# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 1 of 2.
# a(en, es, fr, de, ru, ar, nl, pl, no, sv)
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Eighty homes in eight blocks stepping up a hillside at Altos de los Monteros, Marbella, every one turned to the sea. Twelve of the twenty released are available, from EUR 540,000 before tax.",
 "Ochenta viviendas en ocho bloques que ascienden por una ladera en Altos de los Monteros, Marbella, todas orientadas al mar. Doce de las veinte puestas a la venta están disponibles, desde 540.000 EUR antes de impuestos.",
 "Quatre-vingts logements répartis en huit blocs qui gravissent un coteau à Altos de los Monteros, Marbella, tous orientés vers la mer. Douze des vingt mis en vente sont disponibles, à partir de 540 000 EUR hors taxes.",
 "Achtzig Wohnungen in acht Blöcken, die einen Hang in Altos de los Monteros, Marbella, hinaufsteigen, alle zum Meer ausgerichtet. Zwölf der zwanzig freigegebenen sind verfügbar, ab 540.000 EUR vor Steuern.",
 "Восемьдесят квартир в восьми корпусах, поднимающихся по склону в Альтос-де-лос-Монтерос, Марбелья, и все обращены к морю. Двенадцать из двадцати выведенных в продажу доступны, от 540 000 EUR без налогов.",
 "ثمانون مسكناً في ثمانية مبانٍ تتدرّج صعوداً على منحدر في ألتوس دي لوس مونتيروس بمربيّا، وكلها مطلّة على البحر. اثنا عشر من العشرين المطروحة متاحة، ابتداءً من 540,000 EUR قبل الضرائب.",
 "Tachtig woningen in acht blokken die een helling op klimmen in Altos de los Monteros, Marbella, alle op zee gericht. Twaalf van de twintig vrijgegeven woningen zijn beschikbaar, vanaf 540.000 EUR voor belasting.",
 "Osiemdziesiąt mieszkań w ośmiu budynkach wspinających się po zboczu w Altos de los Monteros w Marbelli, każde zwrócone ku morzu. Dwanaście z dwudziestu wprowadzonych do sprzedaży jest dostępnych, od 540 000 EUR przed podatkiem.",
 "Åtti boliger i åtte blokker som trapper seg oppover en skråning i Altos de los Monteros, Marbella, alle vendt mot sjøen. Tolv av de tjue som er lagt ut er ledige, fra 540 000 EUR før skatt.",
 "Åttio bostäder i åtta huskroppar som trappar uppför en sluttning i Altos de los Monteros, Marbella, samtliga vända mot havet. Tolv av de tjugo som släppts är lediga, från 540 000 EUR före skatt.")

a("New-build apartments and duplex penthouses at Altos de los Monteros, Marbella. Twelve of twenty released homes available from EUR 540,000 plus VAT, delivery Q2 2029.",
 "Apartamentos y áticos dúplex de obra nueva en Altos de los Monteros, Marbella. Doce de veinte viviendas disponibles desde 540.000 EUR más IVA, entrega T2 2029.",
 "Appartements et penthouses duplex neufs à Altos de los Monteros, Marbella. Douze logements sur vingt disponibles à partir de 540 000 EUR hors TVA, livraison T2 2029.",
 "Neubau-Wohnungen und Duplex-Penthäuser in Altos de los Monteros, Marbella. Zwölf von zwanzig Wohnungen verfügbar ab 540.000 EUR zzgl. MwSt., Fertigstellung Q2 2029.",
 "Новостройка: квартиры и двухуровневые пентхаусы в Альтос-де-лос-Монтерос, Марбелья. Доступно двенадцать из двадцати, от 540 000 EUR плюс НДС, сдача 2 кв. 2029.",
 "شقق وبنتهاوس دوبلكس جديدة في ألتوس دي لوس مونتيروس، مربيّا. اثنا عشر مسكناً من عشرين متاحة ابتداءً من 540,000 EUR زائد ضريبة القيمة المضافة، التسليم الربع الثاني 2029.",
 "Nieuwbouwappartementen en duplexpenthouses in Altos de los Monteros, Marbella. Twaalf van de twintig woningen beschikbaar vanaf 540.000 EUR exclusief btw, oplevering K2 2029.",
 "Nowe apartamenty i penthouse'y dwupoziomowe w Altos de los Monteros w Marbelli. Dwanaście z dwudziestu mieszkań dostępnych od 540 000 EUR plus VAT, odbiór II kw. 2029.",
 "Nye leiligheter og toppleiligheter over to plan i Altos de los Monteros, Marbella. Tolv av tjue boliger ledige fra 540 000 EUR pluss mva., ferdigstillelse K2 2029.",
 "Nyproducerade lägenheter och takvåningar i två plan i Altos de los Monteros, Marbella. Tolv av tjugo bostäder lediga från 540 000 EUR plus moms, färdigställande K2 2029.")

a("12 of 20 released homes available",
 "12 de 20 viviendas disponibles","12 logements disponibles sur 20","12 von 20 Wohnungen verfügbar",
 "12 из 20 доступно","12 من 20 مسكناً متاحة","12 van de 20 woningen beschikbaar",
 "12 z 20 mieszkań dostępnych","12 av 20 boliger ledige","12 av 20 bostäder lediga")

a("Altos de los Monteros, Marbella",
 "Altos de los Monteros, Marbella","Altos de los Monteros, Marbella","Altos de los Monteros, Marbella",
 "Альтос-де-лос-Монтерос, Марбелья","ألتوس دي لوس مونتيروس، مربيّا","Altos de los Monteros, Marbella",
 "Altos de los Monteros, Marbella","Altos de los Monteros, Marbella","Altos de los Monteros, Marbella")

a("Apartments and duplex penthouses",
 "Apartamentos y áticos dúplex","Appartements et penthouses duplex","Wohnungen und Duplex-Penthäuser",
 "Квартиры и двухуровневые пентхаусы","شقق وبنتهاوس دوبلكس","Appartementen en duplexpenthouses",
 "Apartamenty i penthouse'y dwupoziomowe","Leiligheter og toppleiligheter over to plan","Lägenheter och takvåningar i två plan")

a("Completion Q2 2029",
 "Entrega T2 2029","Livraison T2 2029","Fertigstellung Q2 2029","Сдача 2 кв. 2029",
 "الإنجاز الربع الثاني 2029","Oplevering K2 2029","Odbiór II kw. 2029","Ferdigstillelse K2 2029","Färdigställande K2 2029")

a("Eighty homes in eight blocks stepping up a Marbella hillside, each block above the one below it and every home turned to the sea.",
 "Ochenta viviendas en ocho bloques que ascienden por una ladera de Marbella, cada bloque por encima del anterior y todas las viviendas orientadas al mar.",
 "Quatre-vingts logements en huit blocs qui gravissent un coteau de Marbella, chaque bloc dominant le précédent et tous les logements tournés vers la mer.",
 "Achtzig Wohnungen in acht Blöcken, die einen Hang bei Marbella hinaufsteigen, jeder Block über dem darunterliegenden und jede Wohnung zum Meer ausgerichtet.",
 "Восемьдесят квартир в восьми корпусах, поднимающихся по склону в Марбелье: каждый корпус выше предыдущего, и все квартиры обращены к морю.",
 "ثمانون مسكناً في ثمانية مبانٍ تتدرّج على منحدر في مربيّا، كل مبنى فوق الذي تحته وكل مسكن مطلّ على البحر.",
 "Tachtig woningen in acht blokken die een helling bij Marbella op klimmen, elk blok boven het voorgaande en elke woning op zee gericht.",
 "Osiemdziesiąt mieszkań w ośmiu budynkach wspinających się po zboczu w Marbelli, każdy budynek powyżej poprzedniego, a każde mieszkanie zwrócone ku morzu.",
 "Åtti boliger i åtte blokker som trapper seg oppover en skråning i Marbella, hver blokk over den under, og hver bolig vendt mot sjøen.",
 "Åttio bostäder i åtta huskroppar som trappar uppför en sluttning i Marbella, varje huskropp ovanför den under, och varje bostad vänd mot havet.")

a("97.79-124.53 sqm",
 "97,79-124,53 m² construido","97,79-124,53 m² construit","97,79-124,53 m² bebaut","97,79-124,53 м² застройка",
 "97.79-124.53 م² مبنية","97,79-124,53 m² bebouwd","97,79-124,53 m² powierzchni zabudowy",
 "97,79-124,53 m² bruksareal","97,79-124,53 m² byggyta")

a("Q2 2029",
 "T2 2029","T2 2029","Q2 2029","2 кв. 2029","الربع الثاني 2029","K2 2029","II kw. 2029","K2 2029","K2 2029")

a("80 in 8 blocks",
 "80 en 8 bloques","80 en 8 blocs","80 in 8 Blöcken","80 в 8 корпусах","80 في 8 مبانٍ",
 "80 in 8 blokken","80 w 8 budynkach","80 i 8 blokker","80 i 8 huskroppar")

a("12 of 20 released",
 "12 de 20 puestas a la venta","12 sur 20 mis en vente","12 von 20 freigegeben","12 из 20 выведенных в продажу",
 "12 من 20 مطروحة","12 van de 20 vrijgegeven","12 z 20 wprowadzonych do sprzedaży",
 "12 av 20 lagt ut","12 av 20 släppta")

a("Developer visuals of the blocks, the terraces, the homes and the communal floor.",
 "Imágenes del promotor de los bloques, las terrazas, las viviendas y la planta comunitaria.",
 "Visuels du promoteur des blocs, des terrasses, des logements et de l'étage commun.",
 "Visualisierungen des Bauträgers von den Blöcken, den Terrassen, den Wohnungen und der Gemeinschaftsebene.",
 "Визуализации застройщика: корпуса, террасы, квартиры и общественный этаж.",
 "صور من المطوّر للمباني والتراسات والمساكن والطابق المشترك.",
 "Visuals van de ontwikkelaar van de blokken, de terrassen, de woningen en de gemeenschappelijke verdieping.",
 "Wizualizacje dewelopera budynków, tarasów, mieszkań i piętra wspólnego.",
 "Utbyggerens visualiseringer av blokkene, terrassene, boligene og fellesetasjen.",
 "Byggherrens visualiseringar av huskropparna, terrasserna, bostäderna och gemensamhetsplanet.")

a("A penthouse terrace with lounge seating and the coast beyond",
 "Una terraza de ático con zona de estar y la costa al fondo","Une terrasse de penthouse avec salon et la côte au loin",
 "Eine Penthouse-Terrasse mit Loungemöbeln und der Küste dahinter","Терраса пентхауса с лаунж-зоной и побережьем вдали",
 "تراس بنتهاوس بمقاعد استرخاء والساحل في الخلفية","Een penthouseterras met loungemeubels en de kust erachter",
 "Taras penthouse'u z wypoczynkiem i wybrzeżem w tle","En toppleilighetsterrasse med loungemøbler og kysten bak",
 "En takvåningsterrass med loungemöbler och kusten bortom")

a("A covered terrace looking down over the pines to the sea",
 "Una terraza cubierta que mira por encima de los pinos hacia el mar","Une terrasse couverte dominant les pins jusqu'à la mer",
 "Eine überdachte Terrasse mit Blick über die Pinien aufs Meer","Крытая терраса с видом поверх сосен на море",
 "تراس مغطّى يطلّ فوق أشجار الصنوبر على البحر","Een overdekt terras met uitzicht over de dennen naar zee",
 "Zadaszony taras z widokiem ponad sosnami na morze","En overbygd terrasse med utsikt over furutrærne til sjøen",
 "En täckt terrass med utsikt över tallarna mot havet")

a("A terrace sitting room under its overhang, the bay in the distance",
 "Un salón de terraza bajo el voladizo, con la bahía a lo lejos","Un salon de terrasse sous son avancée, la baie au loin",
 "Ein Terrassenwohnbereich unter der Auskragung, die Bucht in der Ferne","Гостиная зона на террасе под навесом, бухта вдали",
 "جلسة على التراس تحت البروز المعماري، والخليج في البعد","Een terraszitkamer onder de overstek, de baai in de verte",
 "Salon na tarasie pod nawisem, zatoka w oddali","En terrassestue under utspringet, bukta i det fjerne",
 "Ett terrassvardagsrum under utsprånget, viken i fjärran")

a("A terrace with a planted edge and the coastline below",
 "Una terraza con jardinera perimetral y la línea de costa abajo","Une terrasse bordée de plantations, le littoral en contrebas",
 "Eine Terrasse mit bepflanzter Kante und der Küste darunter","Терраса с озеленённым краем и береговой линией внизу",
 "تراس بحافة مزروعة وخط الساحل في الأسفل","Een terras met beplante rand en de kustlijn beneden",
 "Taras z obsadzoną krawędzią i linią brzegową poniżej","En terrasse med beplantet kant og kystlinjen nedenfor",
 "En terrass med planterad kant och kustlinjen nedanför")

a("A deep covered terrace running along the front of the home",
 "Una terraza cubierta y profunda que recorre el frente de la vivienda","Une terrasse couverte et profonde longeant la façade du logement",
 "Eine tiefe überdachte Terrasse entlang der Vorderseite der Wohnung","Глубокая крытая терраса вдоль всего фасада квартиры",
 "تراس مغطّى وعميق يمتد على واجهة المسكن","Een diep overdekt terras langs de voorzijde van de woning",
 "Głęboki zadaszony taras biegnący wzdłuż frontu mieszkania","En dyp overbygd terrasse langs hele fronten av boligen",
 "En djup täckt terrass längs bostadens hela framsida")

a("A main bedroom with a panelled headboard wall and terrace access",
 "Un dormitorio principal con pared de cabecero panelada y salida a la terraza",
 "Une chambre principale avec mur de tête de lit lambrissé et accès à la terrasse",
 "Ein Hauptschlafzimmer mit paneelierter Kopfwand und Terrassenzugang",
 "Главная спальня со стеной-изголовьем в панелях и выходом на террасу",
 "غرفة نوم رئيسية بجدار مكسوّ خلف السرير ومخرج إلى التراس",
 "Een hoofdslaapkamer met gelambriseerde hoofdeindwand en terrastoegang",
 "Sypialnia główna ze ścianą za wezgłowiem wykończoną panelami i wyjściem na taras",
 "Et hovedsoverom med panelvegg bak sengen og utgang til terrassen",
 "Ett huvudsovrum med panelklädd vägg bakom sängen och utgång till terrassen")

a("A second bedroom with twin beds and a sliding door to the terrace",
 "Un segundo dormitorio con dos camas individuales y puerta corredera a la terraza",
 "Une deuxième chambre avec lits jumeaux et baie coulissante vers la terrasse",
 "Ein zweites Schlafzimmer mit zwei Einzelbetten und Schiebetür zur Terrasse",
 "Вторая спальня с двумя кроватями и раздвижной дверью на террасу",
 "غرفة نوم ثانية بسريرين مفردين وباب منزلق إلى التراس",
 "Een tweede slaapkamer met twee eenpersoonsbedden en een schuifdeur naar het terras",
 "Druga sypialnia z dwoma łóżkami i drzwiami przesuwnymi na taras",
 "Et andre soverom med to enkeltsenger og skyvedør til terrassen",
 "Ett andra sovrum med två enkelsängar och skjutdörr till terrassen")

a("A bathroom with a walk-in shower and a countertop basin",
 "Un baño con ducha a ras de suelo y lavabo sobre encimera","Une salle de bains avec douche à l'italienne et vasque à poser",
 "Ein Bad mit bodengleicher Dusche und Aufsatzwaschbecken","Ванная с душем без поддона и накладной раковиной",
 "حمّام بدُش أرضي ومغسلة فوق سطح الرخام","Een badkamer met inloopdouche en opzetwastafel",
 "Łazienka z prysznicem bez brodzika i umywalką nablatową","Et bad med dusj i plan med gulvet og servant på benkeplate",
 "Ett badrum med golvdusch och tvättställ på bänkskiva")

a("The heated indoor lap pool with loungers at the far end",
 "La piscina de nado climatizada cubierta, con tumbonas al fondo","Le bassin de nage intérieur chauffé, avec des transats au fond",
 "Der beheizte Innen-Schwimmkanal mit Liegen am hinteren Ende","Крытый подогреваемый бассейн для плавания с лежаками в дальнем конце",
 "مسبح السباحة الداخلي المُدفأ مع كراسي استلقاء في نهايته","Het verwarmde binnenbaanzwembad met ligbedden aan het einde",
 "Kryty podgrzewany basen pływacki z leżakami na końcu","Det oppvarmede innendørs svømmebassenget med solsenger i enden",
 "Den uppvärmda inomhusbassängen för simning, med solsängar i bortre änden")

a("The gym, glazed along one side to the hillside",
 "El gimnasio, acristalado en un lateral hacia la ladera","La salle de sport, vitrée sur un côté vers le coteau",
 "Der Fitnessraum, auf einer Seite zum Hang verglast","Спортзал с остеклением вдоль одной стены в сторону склона",
 "صالة الرياضة، مزجّجة من جانب واحد نحو المنحدر","De fitnessruimte, aan één zijde beglaasd naar de helling",
 "Siłownia, przeszklona po jednej stronie w stronę zbocza","Treningsrommet, med glassvegg mot skråningen på den ene siden",
 "Gymmet, med glasvägg mot sluttningen längs ena sidan")

a("The social lounge and coworking room, opening to a terrace",
 "El salón social y la sala de coworking, abiertos a una terraza","Le salon commun et l'espace de coworking, ouverts sur une terrasse",
 "Der Gemeinschaftsraum und der Coworking-Bereich, zur Terrasse geöffnet",
 "Общая гостиная и коворкинг с выходом на террасу","الصالة الاجتماعية وغرفة العمل المشترك، مفتوحتان على تراس",
 "De gemeenschappelijke lounge en de coworkingruimte, met toegang tot een terras",
 "Salon wspólny i sala coworkingowa, otwarte na taras","Fellesstuen og coworking-rommet, med utgang til en terrasse",
 "Gemensamhetsrummet och coworkingrummet, med utgång till en terrass")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
