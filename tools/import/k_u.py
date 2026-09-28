# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}
DV={'es':'Imagen de la promotora','fr':'Image du promoteur','de':'Visualisierung des Bauträgers','ru':'Визуализация застройщика','ar':'تصميم المطور','nl':'Impressie van de ontwikkelaar','pl':'Wizualizacja dewelopera','no':'Utviklerens visualisering','sv':'Byggherrens visualisering'}
def v(en,es,fr,de,ru,ar,nl,pl,no,sv):
    # "Developer visual of X" keeps the same lead-in in every locale.
    parts={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}
    T['Developer visual of '+en]={l:f'{DV[l]}: {p}' for l,p in parts.items()}

v("the scheme stepping down the slope above the old white village",
 "la promoción descendiendo la ladera sobre el antiguo pueblo blanco",
 "le programme descendant le coteau au-dessus du vieux village blanc",
 "die Anlage, die den Hang über dem alten weißen Dorf hinabstuft",
 "комплекс, спускающийся по склону над старым белым городком",
 "المجمّع متدرجاً على المنحدر فوق القرية البيضاء القديمة",
 "het project dat de helling boven het oude witte dorp afdaalt",
 "inwestycja schodząca zboczem nad starym białym miasteczkiem",
 "prosjektet som trapper seg ned hellingen over den gamle hvite landsbyen",
 "projektet som trappar ned sluttningen ovanför den gamla vita byn")

v("the long white block curving along the road, planted terraces above",
 "el largo bloque blanco curvándose junto a la carretera, con terrazas plantadas arriba",
 "le long bâtiment blanc épousant la courbe de la route, terrasses plantées au-dessus",
 "den langen weißen Baukörper entlang der Straße, darüber bepflanzte Terrassen",
 "длинный белый корпус, изгибающийся вдоль дороги, с озеленёнными террасами выше",
 "المبنى الأبيض الطويل ينحني مع الطريق، والتراسات المزروعة فوقه",
 "het lange witte blok dat met de weg meebuigt, met groene terrassen erboven",
 "długi biały budynek wygięty wzdłuż drogi, z obsadzonymi tarasami powyżej",
 "den lange hvite bygningskroppen som følger veien, med plantede terrasser over",
 "den långa vita huskroppen som följer vägen, med planterade terrasser ovanför")

v("the block at sunset, palms and bougainvillea at its foot",
 "el bloque al atardecer, con palmeras y buganvillas a sus pies",
 "le bâtiment au coucher du soleil, palmiers et bougainvilliers à ses pieds",
 "den Baukörper bei Sonnenuntergang, Palmen und Bougainvillea am Fuß",
 "корпус на закате, у подножия — пальмы и бугенвиллея",
 "المبنى عند الغروب، والنخيل والجهنمية عند قاعدته",
 "het blok bij zonsondergang, palmen en bougainville aan de voet",
 "budynek o zachodzie słońca, palmy i bugenwille u jego podnóża",
 "bygningen i solnedgang, palmer og bougainvillea ved foten",
 "huskroppen i solnedgång, palmer och bougainvillea vid foten")

v("the pool lit at dusk between the two wings",
 "la piscina iluminada al anochecer entre las dos alas",
 "la piscine éclairée au crépuscule entre les deux ailes",
 "den bei Dämmerung beleuchteten Pool zwischen den beiden Flügeln",
 "бассейн с подсветкой в сумерках между двумя крыльями",
 "المسبح مُضاءً عند الغسق بين الجناحين",
 "het zwembad verlicht in de schemering tussen de twee vleugels",
 "basen podświetlony o zmierzchu między dwoma skrzydłami",
 "bassenget opplyst i skumringen mellom de to fløyene",
 "poolen upplyst i skymningen mellan de två flyglarna")

v("the pool with loungers and parasols, the blocks behind",
 "la piscina con tumbonas y parasoles, con los bloques detrás",
 "la piscine avec bains de soleil et parasols, les bâtiments derrière",
 "den Pool mit Liegen und Sonnenschirmen, dahinter die Baukörper",
 "бассейн с шезлонгами и зонтами, позади — корпуса",
 "المسبح بمقاعد استلقاء ومظلات، والمباني خلفه",
 "het zwembad met ligbedden en parasols, de blokken erachter",
 "basen z leżakami i parasolami, budynki w tle",
 "bassenget med solsenger og parasoller, bygningene bak",
 "poolen med solstolar och parasoll, huskropparna bakom")

v("the chill-out lounge beneath the building, sofas facing the lawn",
 "el salón chill-out bajo el edificio, con sofás frente al césped",
 "le salon chill-out sous le bâtiment, canapés face à la pelouse",
 "die Chill-out-Lounge unter dem Gebäude, Sofas zum Rasen hin",
 "лаунж-зону под зданием, диваны обращены к газону",
 "صالة الاسترخاء تحت المبنى، والأرائك تطلّ على المساحة الخضراء",
 "de chill-outlounge onder het gebouw, banken naar het gazon",
 "strefa chill-out pod budynkiem, sofy zwrócone ku trawnikowi",
 "chill-out-loungen under bygningen, sofaer mot plenen",
 "chill-out-loungen under byggnaden, soffor mot gräsmattan")

v("the chill-out terrace, parasols and loungers on the lawn above the sea",
 "la terraza chill-out, con parasoles y tumbonas en el césped sobre el mar",
 "la terrasse chill-out, parasols et bains de soleil sur la pelouse au-dessus de la mer",
 "die Chill-out-Terrasse, Sonnenschirme und Liegen auf dem Rasen über dem Meer",
 "террасу чил-аут: зонты и шезлонги на газоне над морем",
 "تراس الاسترخاء، والمظلات ومقاعد الاستلقاء على العشب فوق البحر",
 "het chill-outterras, parasols en ligbedden op het gazon boven de zee",
 "taras chill-out, parasole i leżaki na trawniku nad morzem",
 "chill-out-terrassen, parasoller og solsenger på plenen over sjøen",
 "chill-out-terrassen, parasoll och solstolar på gräsmattan ovanför havet")

v("the gym, weights and machines under a long window",
 "el gimnasio, con pesas y máquinas bajo un ventanal alargado",
 "la salle de sport, poids et machines sous une longue fenêtre",
 "den Fitnessraum, Gewichte und Geräte unter einem langen Fenster",
 "спортзал: свободные веса и тренажёры под длинным окном",
 "صالة الرياضة، الأوزان والأجهزة تحت نافذة ممتدة",
 "de fitnessruimte, gewichten en toestellen onder een lang raam",
 "siłownię, ciężary i maszyny pod długim oknem",
 "treningsrommet, vekter og maskiner under et langt vindu",
 "gymmet, vikter och maskiner under ett långt fönster")

v("the gym beneath a timber-slat ceiling",
 "el gimnasio bajo un techo de lamas de madera",
 "la salle de sport sous un plafond à lames de bois",
 "den Fitnessraum unter einer Holzlattendecke",
 "спортзал под потолком из деревянных реек",
 "صالة الرياضة تحت سقف من شرائح الخشب",
 "de fitnessruimte onder een plafond van houten latten",
 "siłownię pod sufitem z drewnianych lameli",
 "treningsrommet under et tak av trespiler",
 "gymmet under ett tak av trälameller")

v("a terrace under a planted pergola, with a sofa and a dining table",
 "una terraza bajo una pérgola vegetal, con sofá y mesa de comedor",
 "une terrasse sous une pergola végétalisée, avec canapé et table à manger",
 "eine Terrasse unter einer bepflanzten Pergola, mit Sofa und Esstisch",
 "террасу под озеленённой перголой, с диваном и обеденным столом",
 "تراساً تحت عريشة مزروعة، مع أريكة وطاولة طعام",
 "een terras onder een groene pergola, met een bank en een eettafel",
 "taras pod obsadzoną pergolą, z sofą i stołem jadalnym",
 "en terrasse under en plantet pergola, med sofa og spisebord",
 "en terrass under en planterad pergola, med soffa och matbord")

v("a terrace looking out over the coast to the sea",
 "una terraza con vistas sobre la costa hacia el mar",
 "une terrasse ouverte sur la côte et la mer",
 "eine Terrasse mit Blick über die Küste auf das Meer",
 "террасу с видом на побережье и море",
 "تراساً يطلّ على الساحل والبحر",
 "een terras met uitzicht over de kust naar de zee",
 "taras z widokiem na wybrzeże i morze",
 "en terrasse med utsikt over kysten og sjøen",
 "en terrass med utsikt över kusten och havet")

v("the living room with built-in shelving and a window to the sea",
 "el salón con estantería integrada y una ventana al mar",
 "le séjour avec étagères intégrées et une fenêtre sur la mer",
 "das Wohnzimmer mit Einbauregal und einem Fenster zum Meer",
 "гостиную со встроенными полками и окном к морю",
 "غرفة الجلوس برفوف مدمجة ونافذة تطلّ على البحر",
 "de woonkamer met ingebouwde schappen en een raam op de zee",
 "salon z wbudowanymi półkami i oknem na morze",
 "stuen med innebygde hyller og et vindu mot sjøen",
 "vardagsrummet med inbyggda hyllor och ett fönster mot havet")

v("the open kitchen and its island, the living room beyond",
 "la cocina abierta y su isla, con el salón al fondo",
 "la cuisine ouverte et son îlot, le séjour au fond",
 "die offene Küche mit Kochinsel, dahinter das Wohnzimmer",
 "открытую кухню с островом и гостиную за ней",
 "المطبخ المفتوح وجزيرته، وغرفة الجلوس خلفه",
 "de open keuken met kookeiland, de woonkamer erachter",
 "otwartą kuchnię z wyspą i salon w tle",
 "det åpne kjøkkenet med kjøkkenøy, stuen bak",
 "det öppna köket med köksö, vardagsrummet bakom")

v("the fitted kitchen with an island and breakfast stools",
 "la cocina equipada con isla y taburetes de desayuno",
 "la cuisine équipée avec îlot et tabourets de petit-déjeuner",
 "die Einbauküche mit Kochinsel und Frühstückshöckern",
 "оборудованную кухню с островом и барными табуретами",
 "المطبخ المجهز بجزيرة ومقاعد للفطور",
 "de ingerichte keuken met kookeiland en ontbijtkrukken",
 "wyposażoną kuchnię z wyspą i stołkami śniadaniowymi",
 "det innredede kjøkkenet med kjøkkenøy og frokostkrakker",
 "det inredda köket med köksö och frukostpallar")

v("the main bedroom, curtains drawn back to the light",
 "el dormitorio principal, con las cortinas descorridas a la luz",
 "la chambre principale, rideaux ouverts sur la lumière",
 "das Hauptschlafzimmer, die Vorhänge zum Licht zurückgezogen",
 "главную спальню с раздвинутыми шторами",
 "غرفة النوم الرئيسية، والستائر مفتوحة للنور",
 "de hoofdslaapkamer, met de gordijnen open naar het licht",
 "główną sypialnię z rozsuniętymi zasłonami",
 "hovedsoverommet, med gardinene trukket fra lyset",
 "huvudsovrummet, med gardinerna öppnade mot ljuset")

v("a twin bedroom with a palm mural and a sea view",
 "un dormitorio con dos camas, mural de palmeras y vistas al mar",
 "une chambre à deux lits, fresque de palmiers et vue sur la mer",
 "ein Zweibettzimmer mit Palmenwandbild und Meerblick",
 "спальню с двумя кроватями, росписью с пальмами и видом на море",
 "غرفة نوم بسريرين، مع جدارية نخيل ومطل على البحر",
 "een tweepersoonsslaapkamer met een palmenmuurschildering en zeezicht",
 "sypialnię z dwoma łóżkami, malowidłem z palmami i widokiem na morze",
 "et soverom med to senger, palmemaleri og sjøutsikt",
 "ett sovrum med två sängar, palmmålning och havsutsikt")

v("a bathroom with a walk-in shower and timber walls",
 "un baño con ducha de obra y paredes de madera",
 "une salle de bains avec douche à l'italienne et murs en bois",
 "ein Badezimmer mit begehbarer Dusche und Holzwänden",
 "ванную с душевой без поддона и деревянными стенами",
 "حماماً بدوش مستوٍ وجدران خشبية",
 "een badkamer met inloopdouche en houten wanden",
 "łazienkę z prysznicem bez brodzika i drewnianymi ścianami",
 "et bad med dusjsone uten kant og trevegger",
 "ett badrum med duschplats utan kant och träväggar")

v("the second bathroom with a bath",
 "el segundo baño con bañera",
 "la seconde salle de bains avec baignoire",
 "das zweite Badezimmer mit Badewanne",
 "вторую ванную с ванной",
 "الحمام الثاني بحوض استحمام",
 "de tweede badkamer met bad",
 "drugą łazienkę z wanną",
 "det andre badet med badekar",
 "det andra badrummet med badkar")

a("The scheme above the village","La promoción sobre el pueblo","Le programme au-dessus du village","Die Anlage über dem Dorf","Комплекс над городком","المجمّع فوق القرية","Het project boven het dorp","Inwestycja nad miasteczkiem","Prosjektet over landsbyen","Projektet ovanför byn")
a("The block from the road","El bloque desde la carretera","Le bâtiment depuis la route","Der Baukörper von der Straße","Корпус со стороны дороги","المبنى من الطريق","Het blok vanaf de weg","Budynek od strony drogi","Bygningen fra veien","Huskroppen från vägen")
a("The block at sunset","El bloque al atardecer","Le bâtiment au coucher du soleil","Der Baukörper bei Sonnenuntergang","Корпус на закате","المبنى عند الغروب","Het blok bij zonsondergang","Budynek o zachodzie słońca","Bygningen i solnedgang","Huskroppen i solnedgång")
a("The chill-out lounge","El salón chill-out","Le salon chill-out","Die Chill-out-Lounge","Лаунж-зона чил-аут","صالة الاسترخاء","De chill-outlounge","Strefa chill-out","Chill-out-loungen","Chill-out-loungen")
a("The chill-out terrace","La terraza chill-out","La terrasse chill-out","Die Chill-out-Terrasse","Терраса чил-аут","تراس الاسترخاء","Het chill-outterras","Taras chill-out","Chill-out-terrassen","Chill-out-terrassen")
a("The gym, looking back","El gimnasio, mirando hacia atrás","La salle de sport, vue en retour","Der Fitnessraum, Blick zurück","Спортзал, взгляд обратно","صالة الرياضة من الجهة المقابلة","De fitnessruimte, terugkijkend","Siłownia od drugiej strony","Treningsrommet, sett tilbake","Gymmet, sett bakåt")
a("A pergola terrace","Una terraza con pérgola","Une terrasse avec pergola","Eine Terrasse mit Pergola","Терраса с перголой","تراس بعريشة","Een terras met pergola","Taras z pergolą","En terrasse med pergola","En terrass med pergola")
a("A terrace and the coast","Una terraza y la costa","Une terrasse et la côte","Eine Terrasse und die Küste","Терраса и побережье","تراس والساحل","Een terras en de kust","Taras i wybrzeże","En terrasse og kysten","En terrass och kusten")
a("Kitchen and living room","Cocina y salón","Cuisine et séjour","Küche und Wohnzimmer","Кухня и гостиная","المطبخ وغرفة الجلوس","Keuken en woonkamer","Kuchnia i salon","Kjøkken og stue","Kök och vardagsrum")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
