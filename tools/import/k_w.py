# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}
DV={'es':'Imagen de la promotora','fr':'Image du promoteur','de':'Visualisierung des Bauträgers','ru':'Визуализация застройщика','ar':'تصميم المطور','nl':'Impressie van de ontwikkelaar','pl':'Wizualizacja dewelopera','no':'Utviklerens visualisering','sv':'Byggherrens visualisering'}
def v(en,es,fr,de,ru,ar,nl,pl,no,sv):
    parts={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}
    T['Developer visual of '+en]={l:f'{DV[l]}: {p}' for l,p in parts.items()}

v("the scheme seen from the water, the blocks set back behind the villas",
 "la promoción vista desde el agua, con los bloques retranqueados detrás de las villas",
 "le programme vu depuis l'eau, les immeubles en retrait derrière les villas",
 "die Anlage vom Wasser aus, die Baukörper hinter den Villen zurückgesetzt",
 "комплекс со стороны моря: корпуса отступают вглубь за виллами",
 "المجمّع من جهة الماء، والمباني متراجعة خلف الفيلات",
 "het project gezien vanaf het water, de blokken terugliggend achter de villa's",
 "inwestycja widziana od strony wody, budynki cofnięte za willami",
 "prosjektet sett fra sjøen, bygningene trukket tilbake bak villaene",
 "projektet sett från vattnet, huskropparna indragna bakom villorna")

v("the scheme lit at night above the beach",
 "la promoción iluminada de noche sobre la playa",
 "le programme éclairé la nuit au-dessus de la plage",
 "die nachts beleuchtete Anlage über dem Strand",
 "освещённый ночью комплекс над пляжем",
 "المجمّع مُضاءً ليلاً فوق الشاطئ",
 "het project 's nachts verlicht boven het strand",
 "inwestycja oświetlona nocą nad plażą",
 "prosjektet opplyst om natten over stranden",
 "projektet upplyst på natten ovanför stranden")

v("one of the three-storey blocks, planted terraces on every level",
 "uno de los bloques de tres plantas, con terrazas plantadas en todos los niveles",
 "l'un des immeubles de trois étages, terrasses plantées à chaque niveau",
 "einen der dreigeschossigen Baukörper mit bepflanzten Terrassen auf jeder Ebene",
 "один из трёхэтажных корпусов с озеленёнными террасами на каждом уровне",
 "أحد المباني المكوّنة من ثلاثة طوابق، بتراسات مزروعة في كل مستوى",
 "een van de blokken van drie lagen, met groene terrassen op elk niveau",
 "jeden z trzykondygnacyjnych budynków, z obsadzonymi tarasami na każdym poziomie",
 "en av bygningene i tre etasjer, med plantede terrasser på hvert nivå",
 "en av huskropparna i tre våningar, med planterade terrasser på varje plan")

v("the blocks rising behind the gardens and the pool",
 "los bloques elevándose detrás de los jardines y la piscina",
 "les immeubles s'élevant derrière les jardins et la piscine",
 "die Baukörper hinter den Gärten und dem Pool",
 "корпуса, поднимающиеся за садами и бассейном",
 "المباني ترتفع خلف الحدائق والمسبح",
 "de blokken die achter de tuinen en het zwembad oprijzen",
 "budynki wznoszące się za ogrodami i basenem",
 "bygningene som reiser seg bak hagene og bassenget",
 "huskropparna som reser sig bakom trädgårdarna och poolen")

v("a beachfront villa from its lawn, pool along the front",
 "una villa en primera línea de playa desde su césped, con la piscina en el frente",
 "une villa en front de mer depuis sa pelouse, la piscine sur le devant",
 "eine Villa in erster Strandlinie von ihrem Rasen aus, den Pool an der Front",
 "виллу на первой линии со стороны газона, бассейн вдоль фасада",
 "فيلا على الواجهة البحرية من مسطحها الأخضر، والمسبح على امتداد الواجهة",
 "een villa aan het strand vanaf het gazon, met het zwembad aan de voorzijde",
 "willę w pierwszej linii brzegowej od strony trawnika, z basenem wzdłuż frontu",
 "en villa i første rekke fra plenen, med bassenget langs fronten",
 "en villa i första strandlinjen från gräsmattan, med poolen längs framsidan")

v("a villa and its private pool, palms behind",
 "una villa y su piscina privada, con palmeras detrás",
 "une villa et sa piscine privative, palmiers en arrière-plan",
 "eine Villa mit eigenem Pool, dahinter Palmen",
 "виллу с собственным бассейном, за ней пальмы",
 "فيلا ومسبحها الخاص، والنخيل خلفها",
 "een villa met eigen zwembad, palmen erachter",
 "willę i jej prywatny basen, palmy w tle",
 "en villa og dens private basseng, med palmer bak",
 "en villa och dess privata pool, med palmer bakom")

v("a villa living room open to the sea across a marble wall",
 "el salón de una villa abierto al mar frente a un paramento de mármol",
 "le séjour d'une villa ouvert sur la mer face à un mur de marbre",
 "das Wohnzimmer einer Villa, zum Meer hin offen, gegenüber einer Marmorwand",
 "гостиную виллы, открытую к морю, напротив мраморной стены",
 "غرفة معيشة فيلا مفتوحة على البحر مقابل جدار رخامي",
 "de woonkamer van een villa, open naar de zee tegenover een marmeren wand",
 "salon willi otwarty na morze naprzeciw marmurowej ściany",
 "stuen i en villa, åpen mot sjøen mot en marmorvegg",
 "vardagsrummet i en villa, öppet mot havet mitt emot en marmorvägg")

v("an apartment living and dining room glazed on two sides to the sea",
 "el salón comedor de un apartamento acristalado hacia el mar por dos lados",
 "le séjour et la salle à manger d'un appartement vitrés sur deux côtés vers la mer",
 "Wohn- und Essbereich einer Wohnung, an zwei Seiten zum Meer verglast",
 "гостиную-столовую квартиры, остеклённую к морю с двух сторон",
 "غرفة معيشة وطعام في شقة مزججة من جهتين نحو البحر",
 "de woon- en eetkamer van een appartement, aan twee zijden beglaasd naar de zee",
 "salon z jadalnią w mieszkaniu, przeszklony na morze z dwóch stron",
 "stue og spisestue i en leilighet, glassinnrammet mot sjøen på to sider",
 "vardagsrum och matplats i en lägenhet, glasade mot havet på två sidor")

v("a living room opening onto the terrace and the garden",
 "un salón que se abre a la terraza y al jardín",
 "un séjour ouvert sur la terrasse et le jardin",
 "ein Wohnzimmer, das sich zur Terrasse und zum Garten öffnet",
 "гостиную, открытую на террасу и в сад",
 "غرفة معيشة تنفتح على التراس والحديقة",
 "een woonkamer die uitkomt op het terras en de tuin",
 "salon otwierający się na taras i ogród",
 "en stue som åpner seg mot terrassen og hagen",
 "ett vardagsrum som öppnar sig mot terrassen och trädgården")

v("the kitchen with its island and breakfast stools",
 "la cocina con su isla y taburetes de desayuno",
 "la cuisine avec son îlot et ses tabourets de petit-déjeuner",
 "die Küche mit Kochinsel und Frühstückshockern",
 "кухню с островом и барными табуретами",
 "المطبخ بجزيرته ومقاعد الفطور",
 "de keuken met kookeiland en ontbijtkrukken",
 "kuchnię z wyspą i stołkami śniadaniowymi",
 "kjøkkenet med kjøkkenøy og frokostkrakker",
 "köket med köksö och frukostpallar")

v("a main bedroom with the terrace and the sea beyond",
 "un dormitorio principal con la terraza y el mar al fondo",
 "une chambre principale avec la terrasse et la mer au-delà",
 "ein Hauptschlafzimmer mit Terrasse und dahinter dem Meer",
 "главную спальню с террасой и морем за ней",
 "غرفة نوم رئيسية مع التراس والبحر خلفه",
 "een hoofdslaapkamer met het terras en daarachter de zee",
 "główną sypialnię z tarasem i morzem w tle",
 "et hovedsoverom med terrassen og sjøen bakenfor",
 "ett huvudsovrum med terrassen och havet bortom")

v("a terrace looking over the gardens and the communal pool",
 "una terraza con vistas a los jardines y a la piscina comunitaria",
 "une terrasse donnant sur les jardins et la piscine commune",
 "eine Terrasse mit Blick über die Gärten und den Gemeinschaftspool",
 "террасу с видом на сады и общий бассейн",
 "تراساً يطلّ على الحدائق والمسبح المشترك",
 "een terras met uitzicht over de tuinen en het gemeenschappelijke zwembad",
 "taras z widokiem na ogrody i basen wspólny",
 "en terrasse med utsikt over hagene og fellesbassenget",
 "en terrass med utsikt över trädgårdarna och den gemensamma poolen")

v("a terrace with a pool and loungers facing the Mediterranean",
 "una terraza con piscina y tumbonas frente al Mediterráneo",
 "une terrasse avec piscine et bains de soleil face à la Méditerranée",
 "eine Terrasse mit Pool und Liegen zum Mittelmeer",
 "террасу с бассейном и шезлонгами напротив Средиземного моря",
 "تراساً بمسبح ومقاعد استلقاء يواجه البحر المتوسط",
 "een terras met zwembad en ligbedden aan de Middellandse Zee",
 "taras z basenem i leżakami zwrócony ku Morzu Śródziemnemu",
 "en terrasse med basseng og solsenger mot Middelhavet",
 "en terrass med pool och solstolar mot Medelhavet")

v("the outdoor pool with parasols and daybeds",
 "la piscina exterior con parasoles y camas balinesas",
 "la piscine extérieure avec parasols et lits de repos",
 "den Außenpool mit Sonnenschirmen und Tagesbetten",
 "открытый бассейн с зонтами и лежаками",
 "المسبح الخارجي بالمظلات وأسرّة الاستلقاء",
 "het buitenzwembad met parasols en loungebedden",
 "basen zewnętrzny z parasolami i leżankami",
 "utendørsbassenget med parasoller og dagsenger",
 "utomhuspoolen med parasoll och dagbäddar")

v("the spa, a skylight above the heated pool",
 "el spa, con un lucernario sobre la piscina climatizada",
 "le spa, une verrière au-dessus de la piscine chauffée",
 "das Spa, ein Oberlicht über dem beheizten Pool",
 "спа со световым фонарём над подогреваемым бассейном",
 "السبا، وكوّة سقفية فوق المسبح المُدفأ",
 "de spa, met een daklicht boven het verwarmde zwembad",
 "spa ze świetlikiem nad podgrzewanym basenem",
 "spaet, med et takvindu over det oppvarmede bassenget",
 "spat, med ett takfönster över den uppvärmda poolen")

v("the indoor pool beneath its long skylight",
 "la piscina interior bajo su lucernario alargado",
 "la piscine intérieure sous sa longue verrière",
 "den Innenpool unter seinem langen Oberlicht",
 "крытый бассейн под длинным световым фонарём",
 "المسبح الداخلي تحت كوّته السقفية الممتدة",
 "het binnenzwembad onder het lange daklicht",
 "basen wewnętrzny pod długim świetlikiem",
 "innendørsbassenget under det lange takvinduet",
 "inomhuspoolen under det långa takfönstret")

v("the relaxation pool with loungers against green marble",
 "la piscina de relajación con tumbonas frente al mármol verde",
 "le bassin de relaxation avec bains de soleil devant le marbre vert",
 "das Ruhebecken mit Liegen vor grünem Marmor",
 "релакс-бассейн с шезлонгами на фоне зелёного мрамора",
 "مسبح الاسترخاء بمقاعد استلقاء أمام الرخام الأخضر",
 "het relaxbad met ligbedden tegen groen marmer",
 "basen relaksacyjny z leżakami na tle zielonego marmuru",
 "avslapningsbassenget med solsenger mot grønn marmor",
 "avkopplingspoolen med solstolar mot grön marmor")

v("the gym looking out over the gardens",
 "el gimnasio con vistas a los jardines",
 "la salle de sport donnant sur les jardins",
 "den Fitnessraum mit Blick über die Gärten",
 "спортзал с видом на сады",
 "صالة الرياضة المطلّة على الحدائق",
 "de fitnessruimte met uitzicht over de tuinen",
 "siłownię z widokiem na ogrody",
 "treningsrommet med utsikt over hagene",
 "gymmet med utsikt över trädgårdarna")

v("the padel court","la pista de pádel","le terrain de padel","den Padelplatz","падел-корт","ملعب البادل","de padelbaan","kort do padla","padelbanen","padelbanan")

a("The beach and the coastal promenade beside the scheme at sunset",
 "La playa y el paseo marítimo junto a la promoción al atardecer",
 "La plage et la promenade du littoral à côté du programme au coucher du soleil",
 "Der Strand und die Küstenpromenade neben der Anlage bei Sonnenuntergang",
 "Пляж и приморский променад рядом с комплексом на закате",
 "الشاطئ والممشى الساحلي بجوار المجمّع عند الغروب",
 "Het strand en de kustpromenade naast het project bij zonsondergang",
 "Plaża i promenada nadmorska obok inwestycji o zachodzie słońca",
 "Stranden og kystpromenaden ved siden av prosjektet i solnedgang",
 "Stranden och strandpromenaden intill projektet i solnedgång")

a("The scheme from the sea","La promoción desde el mar","Le programme depuis la mer","Die Anlage vom Meer aus","Комплекс со стороны моря","المجمّع من البحر","Het project vanaf zee","Inwestycja od strony morza","Prosjektet fra sjøen","Projektet från havet")
a("The scheme at night","La promoción de noche","Le programme la nuit","Die Anlage bei Nacht","Комплекс ночью","المجمّع ليلاً","Het project bij nacht","Inwestycja nocą","Prosjektet om natten","Projektet på natten")
a("One of the blocks","Uno de los bloques","L'un des immeubles","Einer der Baukörper","Один из корпусов","أحد المباني","Een van de blokken","Jeden z budynków","En av bygningene","En av huskropparna")
a("The blocks above the gardens","Los bloques sobre los jardines","Les immeubles au-dessus des jardins","Die Baukörper über den Gärten","Корпуса над садами","المباني فوق الحدائق","De blokken boven de tuinen","Budynki nad ogrodami","Bygningene over hagene","Huskropparna ovanför trädgårdarna")
a("A villa and its pool","Una villa y su piscina","Une villa et sa piscine","Eine Villa und ihr Pool","Вилла и её бассейн","فيلا ومسبحها","Een villa en haar zwembad","Willa i jej basen","En villa og bassenget","En villa och dess pool")
a("A villa living room","El salón de una villa","Le séjour d'une villa","Das Wohnzimmer einer Villa","Гостиная виллы","غرفة معيشة في فيلا","De woonkamer van een villa","Salon willi","Stuen i en villa","Vardagsrummet i en villa")
a("A terrace above the gardens","Una terraza sobre los jardines","Une terrasse au-dessus des jardins","Eine Terrasse über den Gärten","Терраса над садами","تراس فوق الحدائق","Een terras boven de tuinen","Taras nad ogrodami","En terrasse over hagene","En terrass ovanför trädgårdarna")
a("The relaxation pool","La piscina de relajación","Le bassin de relaxation","Das Ruhebecken","Релакс-бассейн","مسبح الاسترخاء","Het relaxbad","Basen relaksacyjny","Avslapningsbassenget","Avkopplingspoolen")
a("The beach beside the scheme","La playa junto a la promoción","La plage à côté du programme","Der Strand neben der Anlage","Пляж рядом с комплексом","الشاطئ بجوار المجمّع","Het strand naast het project","Plaża obok inwestycji","Stranden ved prosjektet","Stranden intill projektet")
a("Developer visuals of the blocks, the villas, the homes and the spa.",
 "Imágenes de la promotora de los bloques, las villas, las viviendas y el spa.",
 "Images du promoteur des immeubles, des villas, des logements et du spa.",
 "Visualisierungen des Bauträgers von den Baukörpern, den Villen, den Wohnungen und dem Spa.",
 "Визуализации застройщика: корпуса, виллы, квартиры и спа.",
 "تصاميم المطور للمباني والفيلات والمساكن والسبا.",
 "Impressies van de ontwikkelaar van de blokken, de villa's, de woningen en de spa.",
 "Wizualizacje dewelopera budynków, willi, mieszkań i spa.",
 "Utviklerens visualiseringer av bygningene, villaene, boligene og spaet.",
 "Byggherrens visualiseringar av huskropparna, villorna, bostäderna och spat.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
