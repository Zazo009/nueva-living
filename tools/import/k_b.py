# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("The communal gym under a timber ceiling, running machines facing the garden",
 "El gimnasio comunitario bajo un techo de madera, con las cintas de correr mirando al jardín",
 "La salle de sport commune sous un plafond en bois, les tapis de course face au jardin",
 "Der Gemeinschaftsfitnessraum unter einer Holzdecke, die Laufbänder zum Garten hin",
 "Общий спортзал под деревянным потолком: беговые дорожки смотрят в сад",
 "صالة الرياضة المشتركة تحت سقف خشبي، وأجهزة الجري تواجه الحديقة",
 "De gemeenschappelijke fitnessruimte onder een houten plafond, de loopbanden naar de tuin gericht",
 "Wspólna siłownia pod drewnianym sufitem, z bieżniami zwróconymi ku ogrodowi",
 "Fellesgymmet under et tretak, med tredemøllene vendt mot hagen",
 "Det gemensamma gymmet under ett trätak, med löpbanden vända mot trädgården")

a("The spa, with loungers beside the heated indoor pool and planting through the glass",
 "El spa, con tumbonas junto a la piscina interior climatizada y vegetación al otro lado del vidrio",
 "Le spa, avec des transats au bord de la piscine intérieure chauffée et des plantations derrière la vitre",
 "Das Spa mit Liegen am beheizten Innenpool und Bepflanzung hinter dem Glas",
 "Спа: шезлонги у крытого бассейна с подогревом и зелень за стеклом",
 "السبا بمقاعد استلقاء بجانب المسبح الداخلي المُدفأ ونباتات خلف الزجاج",
 "De spa, met ligbedden naast het verwarmde binnenbad en beplanting achter het glas",
 "Spa z leżankami przy podgrzewanym basenie krytym i zielenią za szkłem",
 "Spaet, med solsenger ved det oppvarmede innendørsbassenget og beplantning bak glasset",
 "Spat, med solsängar vid den uppvärmda inomhuspoolen och plantering bakom glaset")

a("A long bar with stools and lounge seating under a timber ceiling, facing the sea",
 "Una barra larga con taburetes y zona de estar bajo un techo de madera, orientada al mar",
 "Un long bar avec tabourets et coin salon sous un plafond en bois, face à la mer",
 "Eine lange Bar mit Hockern und Sitzgruppe unter einer Holzdecke, zum Meer ausgerichtet",
 "Длинная барная стойка с табуретами и зоной отдыха под деревянным потолком, лицом к морю",
 "بار طويل بمقاعد عالية وجلسة استرخاء تحت سقف خشبي، يواجه البحر",
 "Een lange bar met krukken en loungezitjes onder een houten plafond, met zicht op zee",
 "Długi bar z hokerami i strefą wypoczynku pod drewnianym sufitem, zwrócony ku morzu",
 "En lang bar med krakker og loungesoner under et tretak, vendt mot sjøen",
 "En lång bar med barstolar och loungesittning under ett trätak, vänd mot havet")
a("The co-working lounge","La sala de coworking","Le salon de coworking","Die Coworking-Lounge","Коворкинг-лаундж","صالة العمل المشترك","De coworkinglounge","Salon coworkingowy","Coworking-loungen","Coworkingloungen")

a("One of the communal pools, sun loungers along a lawn below the terraces",
 "Una de las piscinas comunitarias, con tumbonas junto al césped bajo las terrazas",
 "L’une des piscines communes, des transats le long d’une pelouse en contrebas des terrasses",
 "Einer der Gemeinschaftspools, Liegen entlang einer Rasenfläche unterhalb der Terrassen",
 "Один из общих бассейнов: шезлонги вдоль газона под террасами",
 "أحد المسابح المشتركة، بأسرّة تشمّس على امتداد مسطح أخضر أسفل التراسات",
 "Een van de gemeenschappelijke zwembaden, ligbedden langs een gazon onder de terrassen",
 "Jeden z basenów wspólnych, leżaki wzdłuż trawnika poniżej tarasów",
 "Ett av fellesbassengene, solsenger langs en plen under terrassene",
 "En av de gemensamma poolerna, solsängar längs en gräsmatta under terrasserna")
a("A communal pool","Una piscina comunitaria","Une piscine commune","Ein Gemeinschaftspool","Общий бассейн","مسبح مشترك","Een gemeenschappelijk zwembad","Basen wspólny","Et fellesbasseng","En gemensam pool")

a("A second communal pool with parasols and loungers, the blocks stepping up behind",
 "Una segunda piscina comunitaria con sombrillas y tumbonas, y los bloques escalonándose detrás",
 "Une deuxième piscine commune avec parasols et transats, les bâtiments s’étageant derrière",
 "Ein zweiter Gemeinschaftspool mit Sonnenschirmen und Liegen, dahinter die gestaffelten Blöcke",
 "Второй общий бассейн с зонтами и шезлонгами, за ним уступами поднимаются корпуса",
 "مسبح مشترك ثانٍ بمظلات وأسرّة تشمّس، والمباني تتدرّج خلفه",
 "Een tweede gemeenschappelijk zwembad met parasols en ligbedden, de blokken trapsgewijs erachter",
 "Drugi basen wspólny z parasolami i leżakami, z budynkami wznoszącymi się schodkowo z tyłu",
 "Et annet fellesbasseng med parasoller og solsenger, byggene trapper seg opp bak",
 "En andra gemensam pool med parasoller och solsängar, husen trappar upp bakom")
a("The second pool","La segunda piscina","La deuxième piscine","Der zweite Pool","Второй бассейн","المسبح الثاني","Het tweede zwembad","Drugi basen","Det andre bassenget","Den andra poolen")

a("The scheme from the air, curved terraces stepping down the hillside above the coast",
 "La promoción desde el aire, con terrazas curvas descendiendo por la ladera sobre la costa",
 "Le programme vu du ciel, des terrasses courbes descendant le coteau au-dessus de la côte",
 "Die Anlage aus der Luft, geschwungene Terrassen, die den Hang über der Küste hinabtreten",
 "Комплекс с воздуха: изогнутые террасы спускаются по склону над побережьем",
 "المشروع من الجو، بتراسات منحنية تتدرّج على المنحدر فوق الساحل",
 "Het project vanuit de lucht, gebogen terrassen die de helling boven de kust af trappen",
 "Inwestycja z lotu ptaka, z łukowatymi tarasami schodzącymi po zboczu nad wybrzeżem",
 "Anlegget fra lufta, buede terrasser som trapper seg nedover skråningen over kysten",
 "Området från luften, svängda terrasser som trappar ned för sluttningen ovanför kusten")

a("An open living room and dining table with the terrace and the town through full-height glass",
 "Un salón abierto y mesa de comedor con la terraza y el pueblo al otro lado del vidrio de suelo a techo",
 "Un séjour ouvert et une table à manger avec la terrasse et le village derrière une baie toute hauteur",
 "Ein offener Wohnraum und Esstisch, dahinter Terrasse und Ort hinter raumhoher Verglasung",
 "Открытая гостиная и обеденный стол, за панорамным остеклением — терраса и посёлок",
 "غرفة معيشة مفتوحة وطاولة طعام، والتراس والبلدة خلف زجاج بارتفاع كامل",
 "Een open woonkamer en eettafel met het terras en het dorp achter vloer-tot-plafondglas",
 "Otwarty salon i stół jadalny z tarasem i miasteczkiem za przeszkleniem od podłogi do sufitu",
 "En åpen stue og spisebord med terrassen og stedet bak gulv-til-tak-glass",
 "Ett öppet vardagsrum och matbord med terrassen och orten bakom glas i full höjd")

a("A kitchen with a marble splashback and an oak panel, opening to a dining table",
 "Una cocina con frente de mármol y panel de roble, abierta a una mesa de comedor",
 "Une cuisine avec crédence en marbre et panneau en chêne, ouverte sur une table à manger",
 "Eine Küche mit Marmorrückwand und Eichenpaneel, offen zum Esstisch",
 "Кухня с мраморным фартуком и дубовой панелью, открытая к обеденному столу",
 "مطبخ بخلفية رخامية ولوح بلوط، مفتوح على طاولة طعام",
 "Een keuken met een marmeren achterwand en een eiken paneel, open naar een eettafel",
 "Kuchnia z marmurową ścianką i dębowym panelem, otwarta na stół jadalny",
 "Et kjøkken med marmorplate på veggen og eikepanel, åpent mot et spisebord",
 "Ett kök med marmorstänkskydd och ekpanel, öppet mot ett matbord")

a("A living room with a stone media wall, a pale sofa and the staircase behind",
 "Un salón con paramento de piedra para el televisor, sofá claro y la escalera al fondo",
 "Un séjour avec un mur TV en pierre, un canapé clair et l’escalier à l’arrière",
 "Ein Wohnzimmer mit steinerner Medienwand, hellem Sofa und der Treppe dahinter",
 "Гостиная с каменной стеной под телевизор, светлым диваном и лестницей позади",
 "غرفة معيشة بجدار حجري للشاشة وأريكة فاتحة والدرج خلفها",
 "Een woonkamer met een stenen tv-wand, een lichte bank en de trap erachter",
 "Salon z kamienną ścianą telewizyjną, jasną sofą i schodami w tle",
 "En stue med en mediavegg i stein, en lys sofa og trappa bak",
 "Ett vardagsrum med en mediavägg i sten, en ljus soffa och trappan bakom")

a("A breakfast bar on the kitchen island under a curved pendant light",
 "Una barra de desayuno en la isla de la cocina bajo una lámpara colgante curva",
 "Un bar de petit-déjeuner sur l’îlot de cuisine sous une suspension incurvée",
 "Eine Frühstücksbar an der Kücheninsel unter einer geschwungenen Pendelleuchte",
 "Барная стойка для завтрака на кухонном острове под изогнутым светильником",
 "بار إفطار على جزيرة المطبخ تحت مصباح معلّق منحني",
 "Een ontbijtbar aan het keukeneiland onder een gebogen hanglamp",
 "Bar śniadaniowy przy wyspie kuchennej pod wygiętą lampą wiszącą",
 "En frokostbar på kjøkkenøya under en buet pendel",
 "En frukostbar vid köksön under en böjd pendel")

a("The main bedroom with a slatted oak headboard wall and a window onto the hillside",
 "El dormitorio principal con cabecero de listones de roble y una ventana a la ladera",
 "La chambre principale avec un mur de tête de lit en lattes de chêne et une fenêtre sur le coteau",
 "Das Hauptschlafzimmer mit einer Kopfwand aus Eichenlamellen und einem Fenster zum Hang",
 "Главная спальня со стеной-изголовьем из дубовых реек и окном на склон",
 "غرفة النوم الرئيسية بجدار مسند من شرائح البلوط ونافذة تطلّ على المنحدر",
 "De hoofdslaapkamer met een wand van eiken latten als hoofdeinde en een raam op de helling",
 "Sypialnia główna ze ścianą wezgłowia z dębowych listew i oknem na zbocze",
 "Hovedsoverommet med en hodegjerdevegg i eikespiler og et vindu mot skråningen",
 "Huvudsovrummet med en sänggavelvägg i ekspjälor och ett fönster mot sluttningen")

a("The main bathroom with a double basin on a timber vanity and a glass shower",
 "El baño principal con doble lavabo sobre mueble de madera y ducha de vidrio",
 "La salle de bains principale avec double vasque sur un meuble en bois et une douche vitrée",
 "Das Hauptbad mit Doppelwaschtisch auf Holzunterschrank und Glasdusche",
 "Главная ванная с двойной раковиной на деревянной тумбе и стеклянным душем",
 "الحمّام الرئيسي بحوضَي غسيل على وحدة خشبية ودشّ زجاجي",
 "De hoofdbadkamer met een dubbele wastafel op een houten meubel en een glazen douche",
 "Łazienka główna z podwójną umywalką na drewnianej szafce i szklaną kabiną prysznicową",
 "Hovedbadet med dobbel servant på treinnredning og glassdusj",
 "Huvudbadrummet med dubbla tvättställ på trästomme och glasdusch")

a("A second bedroom with wall lights either side of an upholstered headboard",
 "Un segundo dormitorio con apliques a ambos lados de un cabecero tapizado",
 "Une deuxième chambre avec des appliques de part et d’autre d’une tête de lit capitonnée",
 "Ein zweites Schlafzimmer mit Wandleuchten beidseits eines gepolsterten Kopfteils",
 "Вторая спальня с бра по обе стороны мягкого изголовья",
 "غرفة نوم ثانية بإضاءة جدارية على جانبَي مسند سرير منجّد",
 "Een tweede slaapkamer met wandlampen aan weerszijden van een beklede hoofdeinde",
 "Druga sypialnia z kinkietami po obu stronach tapicerowanego wezgłowia",
 "Et annet soverom med vegglamper på hver side av en polstret hodegjerde",
 "Ett andra sovrum med vägglampor på var sida om en klädd sänggavel")

a("A shower room with a corner glass enclosure and a long stone basin",
 "Un cuarto de ducha con mampara de vidrio en esquina y un lavabo alargado de piedra",
 "Une salle d’eau avec une paroi vitrée d’angle et une longue vasque en pierre",
 "Ein Duschbad mit gläserner Eckabtrennung und einem langen Steinwaschtisch",
 "Душевая с угловым стеклянным ограждением и длинной каменной раковиной",
 "غرفة دشّ بحاجز زجاجي ركني وحوض حجري ممتد",
 "Een doucheruimte met een glazen hoekwand en een lange stenen wastafel",
 "Łazienka z prysznicem w narożnej kabinie szklanej i długą kamienną umywalką",
 "Et dusjbad med glassvegg i hjørnet og en lang servant i stein",
 "Ett duschrum med glasvägg i hörnet och ett långt tvättställ i sten")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
