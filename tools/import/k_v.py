# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Seventy homes, <em>eight available</em>",
 "Setenta viviendas, <em>ocho disponibles</em>","Soixante-dix logements, <em>huit disponibles</em>",
 "Siebzig Wohnungen, <em>acht verfügbar</em>","Семьдесят квартир, <em>восемь доступны</em>",
 "سبعون مسكناً، <em>ثمانٍ متاحة</em>","Zeventig woningen, <em>acht beschikbaar</em>",
 "Siedemdziesiąt mieszkań, <em>osiem dostępnych</em>","Sytti boliger, <em>åtte ledige</em>","Sjuttio bostäder, <em>åtta lediga</em>")

a("A gated scheme on the slope above Benalmádena Pueblo, the old white village between the mountain and the sea.",
 "Una promoción cerrada en la ladera sobre Benalmádena Pueblo, el antiguo pueblo blanco entre la montaña y el mar.",
 "Un programme fermé sur le coteau au-dessus de Benalmádena Pueblo, le vieux village blanc entre la montagne et la mer.",
 "Eine geschlossene Anlage am Hang über Benalmádena Pueblo, dem alten weißen Dorf zwischen Berg und Meer.",
 "Закрытый комплекс на склоне над Бенальмадена-Пуэбло — старым белым городком между горой и морем.",
 "مجمّع مغلق على المنحدر فوق بينالمادينا بويبلو، القرية البيضاء القديمة بين الجبل والبحر.",
 "Een gesloten project op de helling boven Benalmádena Pueblo, het oude witte dorp tussen de berg en de zee.",
 "Zamknięta inwestycja na zboczu nad Benalmádena Pueblo, starym białym miasteczkiem między górą a morzem.",
 "Et portert prosjekt i hellingen over Benalmádena Pueblo, den gamle hvite landsbyen mellom fjellet og sjøen.",
 "Ett grindat projekt på sluttningen ovanför Benalmádena Pueblo, den gamla vita byn mellan berget och havet.")

a("Two and three bedrooms, 85 to 110 sqm built, every home facing south, with two parking spaces and a storeroom.",
 "Dos y tres dormitorios, de 85 a 110 m² construidos, todas las viviendas orientadas al sur, con dos plazas de garaje y trastero.",
 "Deux et trois chambres, de 85 à 110 m² construits, tous les logements orientés au sud, avec deux places de parking et un débarras.",
 "Zwei und drei Schlafzimmer, 85 bis 110 m² bebaut, alle Wohnungen nach Süden orientiert, mit zwei Stellplätzen und einem Abstellraum.",
 "Две и три спальни, от 85 до 110 м² застройки, все квартиры ориентированы на юг, с двумя машиноместами и кладовой.",
 "غرفتا نوم وثلاث، من 85 إلى 110 م² مبنية، وجميع المساكن موجّهة جنوباً، مع موقفي سيارات ومخزن.",
 "Twee en drie slaapkamers, 85 tot 110 m² bebouwd, alle woningen op het zuiden, met twee parkeerplaatsen en een berging.",
 "Dwie i trzy sypialnie, od 85 do 110 m² powierzchni zabudowy, wszystkie mieszkania od południa, z dwoma miejscami postojowymi i komórką.",
 "To og tre soverom, 85 til 110 m² bruksareal, alle boliger sørvendte, med to parkeringsplasser og bod.",
 "Två och tre sovrum, 85 till 110 m² byggyta, alla bostäder södervända, med två parkeringsplatser och förråd.")

a("Two and three bedrooms, every home facing south.",
 "Dos y tres dormitorios, todas las viviendas orientadas al sur.",
 "Deux et trois chambres, tous les logements orientés au sud.",
 "Zwei und drei Schlafzimmer, alle Wohnungen nach Süden orientiert.",
 "Две и три спальни, все квартиры ориентированы на юг.",
 "غرفتا نوم وثلاث، وجميع المساكن موجّهة جنوباً.",
 "Twee en drie slaapkamers, alle woningen op het zuiden.",
 "Dwie i trzy sypialnie, wszystkie mieszkania od południa.",
 "To og tre soverom, alle boliger sørvendte.",
 "Två och tre sovrum, alla bostäder södervända.")

a("Open, balanced layouts with terraces from 14.50 to 77.60 sqm.",
 "Distribuciones abiertas y equilibradas con terrazas de 14,50 a 77,60 m².",
 "Des plans ouverts et équilibrés avec des terrasses de 14,50 à 77,60 m².",
 "Offene, ausgewogene Grundrisse mit Terrassen von 14,50 bis 77,60 m².",
 "Открытые сбалансированные планировки с террасами от 14,50 до 77,60 м².",
 "مخططات مفتوحة ومتوازنة مع تراسات من 14.50 إلى 77.60 م².",
 "Open, evenwichtige indelingen met terrassen van 14,50 tot 77,60 m².",
 "Otwarte, wyważone układy z tarasami od 14,50 do 77,60 m².",
 "Åpne, balanserte planløsninger med terrasser fra 14,50 til 77,60 m².",
 "Öppna, balanserade planlösningar med terrasser från 14,50 till 77,60 m².")

a("An AA energy rating, which the developer puts at about 89 per cent less energy than a conventional home.",
 "Calificación energética AA, que la promotora cifra en un ahorro de en torno al 89 % de energía frente a una vivienda convencional.",
 "Une classe énergétique AA, que le promoteur évalue à environ 89 % d'énergie en moins qu'un logement conventionnel.",
 "Eine Energieklasse AA, die der Bauträger mit rund 89 Prozent weniger Energie als bei einer konventionellen Wohnung angibt.",
 "Энергетический класс AA: застройщик оценивает это как примерно на 89 процентов меньше энергии, чем в обычном жилье.",
 "تصنيف طاقة AA، يقدّره المطور بتوفير نحو 89 بالمائة من الطاقة مقارنةً بمسكن تقليدي.",
 "Een energielabel AA, dat de ontwikkelaar becijfert op ongeveer 89 procent minder energie dan een conventionele woning.",
 "Klasa energetyczna AA, którą deweloper określa jako około 89 procent mniej energii niż w mieszkaniu konwencjonalnym.",
 "Energiklasse AA, som utvikleren oppgir til om lag 89 prosent lavere energibruk enn i en konvensjonell bolig.",
 "Energiklass AA, som byggherren anger till omkring 89 procent lägre energianvändning än i en konventionell bostad.")

a("A communal pool, a gym and a chill-out terrace.",
 "Piscina comunitaria, gimnasio y terraza chill-out.",
 "Une piscine commune, une salle de sport et une terrasse chill-out.",
 "Ein Gemeinschaftspool, ein Fitnessraum und eine Chill-out-Terrasse.",
 "Общий бассейн, спортзал и терраса чил-аут.",
 "مسبح مشترك وصالة رياضة وتراس استرخاء.",
 "Een gemeenschappelijk zwembad, een fitnessruimte en een chill-outterras.",
 "Basen wspólny, siłownia i taras chill-out.",
 "Et fellesbasseng, et treningsrom og en chill-out-terrasse.",
 "En gemensam pool, ett gym och en chill-out-terrass.")

a("8 of 70 homes <em>available</em>",
 "8 de 70 viviendas <em>disponibles</em>","8 logements sur 70 <em>disponibles</em>",
 "8 von 70 Wohnungen <em>verfügbar</em>","8 из 70 квартир <em>доступно</em>",
 "8 من 70 مسكناً <em>متاحة</em>","8 van de 70 woningen <em>beschikbaar</em>",
 "8 z 70 mieszkań <em>dostępnych</em>","8 av 70 boliger <em>ledige</em>","8 av 70 bostäder <em>lediga</em>")

a("Eight apartments are available, two of them on the ground floor. Nueva Living reconfirms price and availability before any viewing or reservation.",
 "Hay ocho apartamentos disponibles, dos de ellos en planta baja. Nueva Living vuelve a confirmar precio y disponibilidad antes de cualquier visita o reserva.",
 "Huit appartements sont disponibles, dont deux en rez-de-chaussée. Nueva Living reconfirme le prix et la disponibilité avant toute visite ou réservation.",
 "Acht Wohnungen sind verfügbar, zwei davon im Erdgeschoss. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung erneut.",
 "Доступны восемь квартир, две из них на первом этаже. Nueva Living заново подтверждает цену и наличие перед любым просмотром или бронированием.",
 "ثماني شقق متاحة، اثنتان منها في الطابق الأرضي. تعيد Nueva Living تأكيد السعر والتوافر قبل أي معاينة أو حجز.",
 "Er zijn acht appartementen beschikbaar, twee daarvan op de begane grond. Nueva Living bevestigt prijs en beschikbaarheid opnieuw voor elke bezichtiging of reservering.",
 "Dostępnych jest osiem mieszkań, dwa z nich na parterze. Nueva Living ponownie potwierdza cenę i dostępność przed każdą prezentacją lub rezerwacją.",
 "Åtte leiligheter er ledige, to av dem i første etasje. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning eller reservasjon.",
 "Åtta lägenheter är lediga, två av dem i bottenvåningen. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning eller reservation.")

a("Currently off-plan, with completion given as the last quarter of 2027. Nueva Living asks for the delivery date in writing and puts it in the contract.",
 "Actualmente sobre plano, con entrega prevista para el último trimestre de 2027. Nueva Living pide la fecha de entrega por escrito y la incorpora al contrato.",
 "Actuellement sur plan, avec une livraison annoncée au dernier trimestre 2027. Nueva Living demande la date de livraison par écrit et la fait inscrire au contrat.",
 "Derzeit vom Plan, die Fertigstellung ist für das letzte Quartal 2027 angegeben. Nueva Living verlangt den Liefertermin schriftlich und nimmt ihn in den Vertrag auf.",
 "На этапе строительства; сдача указана на последний квартал 2027 года. Nueva Living запрашивает срок сдачи в письменном виде и вносит его в договор.",
 "المشروع على المخطط حالياً، والتسليم محدد في الربع الأخير من 2027. تطلب Nueva Living تاريخ التسليم كتابةً وتدرجه في العقد.",
 "Momenteel op plan, met oplevering opgegeven voor het laatste kwartaal van 2027. Nueva Living vraagt de opleverdatum schriftelijk op en laat die in het contract opnemen.",
 "Obecnie na etapie planu, z odbiorem podanym na ostatni kwartał 2027 roku. Nueva Living prosi o datę odbioru na piśmie i wpisuje ją do umowy.",
 "For tiden på tegning, med ferdigstilling oppgitt til siste kvartal 2027. Nueva Living ber om overleveringsdatoen skriftlig og fører den inn i kontrakten.",
 "Just nu på ritning, med färdigställande angivet till sista kvartalet 2027. Nueva Living begär överlämningsdatumet skriftligt och för in det i avtalet.")

a("This project suits buyers who want the old village and the sea in the same view, at a price that starts below most of this coast.",
 "Esta promoción encaja con quienes quieren el pueblo antiguo y el mar en la misma vista, a un precio que parte por debajo de la mayoría de esta costa.",
 "Ce programme convient aux acheteurs qui veulent le vieux village et la mer dans la même vue, à un prix qui démarre en dessous de la plupart de cette côte.",
 "Dieses Projekt passt zu Käufern, die das alte Dorf und das Meer im selben Blick wollen, zu einem Preis, der unter dem Großteil dieser Küste beginnt.",
 "Проект подходит покупателям, которые хотят видеть старый городок и море в одном виде, по цене, которая начинается ниже, чем на большей части этого берега.",
 "يناسب هذا المشروع من يريد القرية القديمة والبحر في مشهد واحد، بسعر يبدأ دون معظم هذا الساحل.",
 "Dit project past bij kopers die het oude dorp en de zee in één blik willen, tegen een prijs die lager begint dan op het grootste deel van deze kust.",
 "Ta inwestycja odpowiada nabywcom, którzy chcą mieć stare miasteczko i morze w jednym widoku, w cenie zaczynającej się niżej niż na większości tego wybrzeża.",
 "Dette prosjektet passer for kjøpere som vil ha den gamle landsbyen og sjøen i samme utsikt, til en pris som starter lavere enn på størstedelen av denne kysten.",
 "Det här projektet passar köpare som vill ha den gamla byn och havet i samma utblick, till ett pris som börjar lägre än på större delen av den här kusten.")

a("Buyers who want a village setting rather than a beach strip, without giving up the sea view.",
 "Compradores que quieren un entorno de pueblo en lugar de un frente de playa, sin renunciar a las vistas al mar.",
 "Des acheteurs qui veulent un cadre de village plutôt qu'un front de mer, sans renoncer à la vue sur la mer.",
 "Käufer, die eine Dorflage statt einer Strandpromenade wollen, ohne auf den Meerblick zu verzichten.",
 "Покупатели, которым нужна деревенская среда, а не пляжная полоса, но без отказа от вида на море.",
 "مشترون يريدون محيط قرية بدلاً من شريط الشاطئ، دون التنازل عن مطل البحر.",
 "Kopers die een dorpse omgeving willen in plaats van een strandstrook, zonder het zeezicht op te geven.",
 "Nabywcy, którzy chcą otoczenia miasteczka, a nie pasa nadmorskiego, nie rezygnując z widoku na morze.",
 "Kjøpere som vil ha landsbyomgivelser i stedet for en strandstripe, uten å gi opp sjøutsikten.",
 "Köpare som vill ha en bymiljö i stället för en strandremsa, utan att ge upp havsutsikten.")

a("Every home faces south, and the energy rating is AA rather than the B or C that is usual here.",
 "Todas las viviendas están orientadas al sur y la calificación energética es AA, en lugar de la B o C habitual aquí.",
 "Tous les logements sont orientés au sud et la classe énergétique est AA, et non le B ou C habituel ici.",
 "Alle Wohnungen sind nach Süden orientiert, und die Energieklasse ist AA statt der hier üblichen B oder C.",
 "Все квартиры ориентированы на юг, а энергетический класс — AA, а не обычные здесь B или C.",
 "جميع المساكن موجّهة جنوباً، وتصنيف الطاقة AA بدلاً من B أو C المعتاد هنا.",
 "Alle woningen liggen op het zuiden en het energielabel is AA in plaats van de hier gebruikelijke B of C.",
 "Wszystkie mieszkania są od południa, a klasa energetyczna to AA, a nie zwykłe tu B lub C.",
 "Alle boliger er sørvendte, og energiklassen er AA i stedet for B eller C som er vanlig her.",
 "Alla bostäder är södervända, och energiklassen är AA i stället för B eller C som är vanligt här.")

a("Benalmádena Pueblo keeps the old town, the beaches and the motorway all within reach.",
 "Benalmádena Pueblo mantiene cerca el casco antiguo, las playas y la autovía.",
 "Benalmádena Pueblo garde à portée le vieux centre, les plages et l'autoroute.",
 "Benalmádena Pueblo hält Altstadt, Strände und Autobahn in Reichweite.",
 "В Бенальмадена-Пуэбло рядом и старый город, и пляжи, и автострада.",
 "تبقي بينالمادينا بويبلو البلدة القديمة والشواطئ والطريق السريع في متناول اليد.",
 "Benalmádena Pueblo houdt de oude kern, de stranden en de snelweg binnen bereik.",
 "Benalmádena Pueblo utrzymuje w zasięgu stare miasto, plaże i autostradę.",
 "Benalmádena Pueblo holder gamlebyen, strendene og motorveien innen rekkevidde.",
 "Benalmádena Pueblo håller gamla stan, stränderna och motorvägen inom räckhåll.")

a("Eight of the 70 remain and the seller's list changes, so it is worth confirming before you shortlist.",
 "Quedan ocho de las 70 y la lista del vendedor cambia, por lo que conviene confirmarla antes de hacer una preselección.",
 "Huit des 70 restent et la liste du vendeur évolue : il vaut donc la peine de la confirmer avant toute présélection.",
 "Acht der 70 sind noch da, und die Liste des Verkäufers ändert sich, daher lohnt sich eine Bestätigung vor der Vorauswahl.",
 "Из 70 осталось восемь, а список продавца меняется, поэтому его стоит подтвердить до составления короткого списка.",
 "بقيت ثمانٍ من أصل 70، وقائمة البائع تتغير، لذلك يُستحسن تأكيدها قبل الاختيار المبدئي.",
 "Acht van de 70 zijn over en de lijst van de verkoper verandert, dus een bevestiging voor de voorselectie is de moeite waard.",
 "Zostało osiem z 70, a lista sprzedającego się zmienia, dlatego warto ją potwierdzić przed sporządzeniem krótkiej listy.",
 "Åtte av de 70 står igjen, og selgerens liste endrer seg, så det er verdt å bekrefte den før en kortliste settes opp.",
 "Åtta av de 70 återstår och säljarens lista förändras, så den är värd att bekräfta innan en kortlista sätts samman.")

a("The entry price","El precio de entrada","Le prix d'entrée","Der Einstiegspreis","Цена входа","سعر الدخول","De instapprijs","Cena wejścia","Inngangsprisen","Ingångspriset")
a("From EUR 338,900, which is low for a south-facing new build with a sea view on this coast.",
 "Desde 338.900 €, una cifra baja para una obra nueva orientada al sur con vistas al mar en esta costa.",
 "À partir de 338 900 €, ce qui est bas pour un neuf orienté au sud avec vue sur la mer sur cette côte.",
 "Ab 338.900 €, was für einen nach Süden orientierten Neubau mit Meerblick an dieser Küste niedrig ist.",
 "От 338 900 € — невысоко для новостройки южной ориентации с видом на море на этом берегу.",
 "ابتداءً من 338,900 €، وهو منخفض لمبنى جديد موجّه جنوباً بمطل على البحر على هذا الساحل.",
 "Vanaf € 338.900, wat laag is voor een op het zuiden gerichte nieuwbouw met zeezicht aan deze kust.",
 "Od 338 900 €, co jest niską kwotą dla nowego budownictwa od południa z widokiem na morze na tym wybrzeżu.",
 "Fra 338 900 €, som er lavt for en sørvendt nybygg med sjøutsikt på denne kysten.",
 "Från 338 900 €, vilket är lågt för en södervänd nyproduktion med havsutsikt på den här kusten.")
a("The energy rating","La calificación energética","La classe énergétique","Die Energieklasse","Энергетический класс","تصنيف الطاقة","Het energielabel","Klasa energetyczna","Energiklassen","Energiklassen")
a("An AA rating is unusual here and shows up in the running costs, not the purchase price.",
 "Una calificación AA es poco habitual aquí y se nota en los gastos corrientes, no en el precio de compra.",
 "Une classe AA est peu courante ici et se voit dans les charges, pas dans le prix d'achat.",
 "Eine AA-Klasse ist hier unüblich und zeigt sich in den Betriebskosten, nicht im Kaufpreis.",
 "Класс AA здесь редкость, и он сказывается на текущих расходах, а не на цене покупки.",
 "تصنيف AA غير مألوف هنا، وأثره يظهر في التكاليف الجارية لا في سعر الشراء.",
 "Een AA-label is hier ongebruikelijk en komt terug in de vaste lasten, niet in de aankoopprijs.",
 "Klasa AA jest tu rzadka i widać ją w kosztach eksploatacji, a nie w cenie zakupu.",
 "Energiklasse AA er uvanlig her og viser seg i driftskostnadene, ikke i kjøpesummen.",
 "Energiklass AA är ovanligt här och syns i driftkostnaderna, inte i köpeskillingen.")
a("Two parking spaces","Dos plazas de garaje","Deux places de parking","Zwei Stellplätze","Два машиноместа","موقفا سيارات","Twee parkeerplaatsen","Dwa miejsca postojowe","To parkeringsplasser","Två parkeringsplatser")
a("Two rather than one, which matters for resale in a village where parking is tight.",
 "Dos en lugar de una, algo que cuenta en la reventa en un pueblo donde aparcar es difícil.",
 "Deux plutôt qu'une, ce qui compte à la revente dans un village où le stationnement est rare.",
 "Zwei statt einer, was beim Wiederverkauf in einem Dorf mit knappem Parkraum zählt.",
 "Два, а не одно — это важно при перепродаже в городке, где с парковкой туго.",
 "موقفان بدلاً من واحد، وهذا يهمّ عند إعادة البيع في قرية يشحّ فيها مكان الوقوف.",
 "Twee in plaats van één, wat telt bij doorverkoop in een dorp waar parkeren krap is.",
 "Dwa, a nie jedno, co ma znaczenie przy odsprzedaży w miasteczku, gdzie o miejsce do parkowania trudno.",
 "To i stedet for én, noe som betyr mye ved videresalg i en landsby der parkering er knapp.",
 "Två i stället för en, vilket betyder mycket vid vidareförsäljning i en by där parkering är ont om.")
a("Terrace size varies widely","El tamaño de la terraza varía mucho","La taille des terrasses varie fortement","Die Terrassengröße variiert stark","Размер террасы сильно разнится","مساحة التراس متباينة كثيراً","De terrasgrootte varieert sterk","Wielkość tarasu bardzo się różni","Terrassestørrelsen varierer mye","Terrassens storlek varierar kraftigt")
a("From 14.50 to 77.60 sqm. The terrace, not the interior, is what separates these homes.",
 "De 14,50 a 77,60 m². Lo que separa estas viviendas es la terraza, no el interior.",
 "De 14,50 à 77,60 m². Ce qui distingue ces logements, c'est la terrasse, pas l'intérieur.",
 "Von 14,50 bis 77,60 m². Was diese Wohnungen unterscheidet, ist die Terrasse, nicht der Innenraum.",
 "От 14,50 до 77,60 м². Эти квартиры различает терраса, а не интерьер.",
 "من 14.50 إلى 77.60 م². ما يفرّق بين هذه المساكن هو التراس لا الداخل.",
 "Van 14,50 tot 77,60 m². Wat deze woningen onderscheidt is het terras, niet het interieur.",
 "Od 14,50 do 77,60 m². To taras, a nie wnętrze, różni te mieszkania.",
 "Fra 14,50 til 77,60 m². Det som skiller disse boligene, er terrassen, ikke interiøret.",
 "Från 14,50 till 77,60 m². Det som skiljer dessa bostäder är terrassen, inte interiören.")

a("White volumes on <em>the village slope</em>",
 "Volúmenes blancos en <em>la ladera del pueblo</em>","Des volumes blancs sur <em>le coteau du village</em>",
 "Weiße Baukörper am <em>Dorfhang</em>","Белые объёмы на <em>склоне у городка</em>",
 "أحجام بيضاء على <em>منحدر القرية</em>","Witte volumes op <em>de dorpshelling</em>",
 "Białe bryły na <em>zboczu miasteczka</em>","Hvite volumer i <em>landsbyhellingen</em>","Vita volymer på <em>byns sluttning</em>")

a("Long low blocks that step down the hillside above the old village, following the contour rather than cutting across it.",
 "Bloques largos y bajos que descienden en terrazas la ladera sobre el pueblo antiguo, siguiendo la curva de nivel en lugar de cortarla.",
 "De longs bâtiments bas qui descendent le coteau au-dessus du vieux village en suivant la courbe de niveau plutôt qu'en la coupant.",
 "Lange, niedrige Baukörper, die den Hang über dem alten Dorf hinabstufen und der Höhenlinie folgen, statt sie zu durchschneiden.",
 "Длинные низкие корпуса спускаются уступами по склону над старым городком, следуя рельефу, а не рассекая его.",
 "مبانٍ منخفضة وممتدة تتدرج نزولاً على المنحدر فوق القرية القديمة، تتبع خط الأرض بدلاً من قطعه.",
 "Lange, lage blokken die de heuvel boven het oude dorp aftrappen en de hoogtelijn volgen in plaats van die te doorsnijden.",
 "Długie, niskie bryły schodzące tarasowo zboczem nad starym miasteczkiem, podążające za linią terenu, a nie przecinające jej.",
 "Lange, lave bygningskropper som trapper seg ned lia over den gamle landsbyen og følger terrenglinjen i stedet for å skjære gjennom den.",
 "Långa, låga huskroppar som trappar ned sluttningen ovanför den gamla byn och följer terränglinjen i stället för att skära genom den.")

a("Planted terraces on every level, with the mountain behind and the Mediterranean in front.",
 "Terrazas plantadas en todos los niveles, con la montaña detrás y el Mediterráneo delante.",
 "Des terrasses plantées à chaque niveau, la montagne derrière et la Méditerranée devant.",
 "Bepflanzte Terrassen auf jeder Ebene, hinten der Berg, vorn das Mittelmeer.",
 "Озеленённые террасы на каждом уровне: сзади гора, впереди Средиземное море.",
 "تراسات مزروعة في كل مستوى، والجبل خلفاً والبحر المتوسط أماماً.",
 "Groene terrassen op elk niveau, met de berg achter en de Middellandse Zee ervoor.",
 "Obsadzone tarasy na każdym poziomie, z górą z tyłu i Morzem Śródziemnym z przodu.",
 "Plantede terrasser på hvert nivå, med fjellet bak og Middelhavet foran.",
 "Planterade terrasser på varje nivå, med berget bakom och Medelhavet framför.")

a("Every home faces south.","Todas las viviendas están orientadas al sur.","Tous les logements sont orientés au sud.","Alle Wohnungen sind nach Süden orientiert.","Все квартиры ориентированы на юг.","جميع المساكن موجّهة جنوباً.","Alle woningen liggen op het zuiden.","Wszystkie mieszkania są od południa.","Alle boliger er sørvendte.","Alla bostäder är södervända.")
a("Terraces from 14.50 to 77.60 sqm.","Terrazas de 14,50 a 77,60 m².","Des terrasses de 14,50 à 77,60 m².","Terrassen von 14,50 bis 77,60 m².","Террасы от 14,50 до 77,60 м².","تراسات من 14.50 إلى 77.60 م².","Terrassen van 14,50 tot 77,60 m².","Tarasy od 14,50 do 77,60 m².","Terrasser fra 14,50 til 77,60 m².","Terrasser från 14,50 till 77,60 m².")
a("An AA rating, which the developer puts at about 89 per cent less energy than a conventional home.",
 "Calificación AA, que la promotora cifra en en torno al 89 % menos de energía que una vivienda convencional.",
 "Une classe AA, que le promoteur évalue à environ 89 % d'énergie en moins qu'un logement conventionnel.",
 "Klasse AA, die der Bauträger mit rund 89 Prozent weniger Energie als bei einer konventionellen Wohnung angibt.",
 "Класс AA: застройщик оценивает это как примерно на 89 процентов меньше энергии, чем в обычном жилье.",
 "تصنيف AA، يقدّره المطور بنحو 89 بالمائة طاقة أقل من مسكن تقليدي.",
 "Label AA, dat de ontwikkelaar becijfert op ongeveer 89 procent minder energie dan een conventionele woning.",
 "Klasa AA, którą deweloper określa jako około 89 procent mniej energii niż w mieszkaniu konwencjonalnym.",
 "Klasse AA, som utvikleren oppgir til om lag 89 prosent lavere energibruk enn i en konvensjonell bolig.",
 "Klass AA, som byggherren anger till omkring 89 procent lägre energianvändning än i en konventionell bostad.")

a("The village, <em>and the sea below it</em>",
 "El pueblo, <em>y el mar a sus pies</em>","Le village, <em>et la mer en dessous</em>",
 "Das Dorf, <em>und das Meer darunter</em>","Городок, <em>и море ниже</em>",
 "القرية، <em>والبحر تحتها</em>","Het dorp, <em>en de zee eronder</em>",
 "Miasteczko <em>i morze poniżej</em>","Landsbyen, <em>og sjøen nedenfor</em>","Byn, <em>och havet nedanför</em>")

a("Benalmádena Pueblo is the white village above the coast, with the beaches a short drive down the hill.",
 "Benalmádena Pueblo es el pueblo blanco sobre la costa, con las playas a pocos minutos en coche bajando la ladera.",
 "Benalmádena Pueblo est le village blanc au-dessus de la côte, les plages à quelques minutes en descendant la colline.",
 "Benalmádena Pueblo ist das weiße Dorf über der Küste, die Strände sind eine kurze Fahrt den Hang hinunter entfernt.",
 "Бенальмадена-Пуэбло — белый городок над побережьем; до пляжей — короткая дорога вниз по склону.",
 "بينالمادينا بويبلو هي القرية البيضاء فوق الساحل، والشواطئ على مسافة قصيرة بالسيارة نزولاً.",
 "Benalmádena Pueblo is het witte dorp boven de kust, met de stranden op een korte rit de heuvel af.",
 "Benalmádena Pueblo to białe miasteczko nad wybrzeżem, a plaże są kilka minut jazdy w dół zbocza.",
 "Benalmádena Pueblo er den hvite landsbyen over kysten, med strendene en kort kjøretur nedover lia.",
 "Benalmádena Pueblo är den vita byn ovanför kusten, med stränderna en kort bilfärd nedåt sluttningen.")

a("A communal pool with loungers and parasols, lit in the evening.",
 "Piscina comunitaria con tumbonas y parasoles, iluminada por la noche.",
 "Une piscine commune avec bains de soleil et parasols, éclairée le soir.",
 "Ein Gemeinschaftspool mit Liegen und Sonnenschirmen, abends beleuchtet.",
 "Общий бассейн с шезлонгами и зонтами, вечером с подсветкой.",
 "مسبح مشترك بمقاعد استلقاء ومظلات، مُضاء في المساء.",
 "Een gemeenschappelijk zwembad met ligbedden en parasols, 's avonds verlicht.",
 "Basen wspólny z leżakami i parasolami, podświetlany wieczorem.",
 "Et fellesbasseng med solsenger og parasoller, opplyst om kvelden.",
 "En gemensam pool med solstolar och parasoll, upplyst på kvällen.")
a("A fully equipped gym under a timber-slat ceiling.",
 "Gimnasio totalmente equipado bajo un techo de lamas de madera.",
 "Une salle de sport entièrement équipée sous un plafond à lames de bois.",
 "Ein voll ausgestatteter Fitnessraum unter einer Holzlattendecke.",
 "Полностью оснащённый спортзал под потолком из деревянных реек.",
 "صالة رياضة كاملة التجهيز تحت سقف من شرائح الخشب.",
 "Een volledig uitgeruste fitnessruimte onder een plafond van houten latten.",
 "W pełni wyposażona siłownia pod sufitem z drewnianych lameli.",
 "Et fullt utstyrt treningsrom under et tak av trespiler.",
 "Ett fullt utrustat gym under ett tak av trälameller.")
a("Sofas and parasols on a lawn looking out over the coast.",
 "Sofás y parasoles en un césped con vistas sobre la costa.",
 "Canapés et parasols sur une pelouse ouverte sur la côte.",
 "Sofas und Sonnenschirme auf einem Rasen mit Blick über die Küste.",
 "Диваны и зонты на газоне с видом на побережье.",
 "أرائك ومظلات على مساحة خضراء تطلّ على الساحل.",
 "Banken en parasols op een gazon met uitzicht over de kust.",
 "Sofy i parasole na trawniku z widokiem na wybrzeże.",
 "Sofaer og parasoller på en plen med utsikt over kysten.",
 "Soffor och parasoll på en gräsmatta med utsikt över kusten.")

a("Dossier","Dosier","Dossier","Dossier","Досье","الملف التعريفي","Dossier","Dossier","Dossier","Dossier")
a("The developer's own dossier.","El dosier de la propia promotora.","Le dossier du promoteur lui-même.","Das Dossier des Bauträgers selbst.","Собственное досье застройщика.","الملف التعريفي الخاص بالمطور.","Het eigen dossier van de ontwikkelaar.","Własny dossier dewelopera.","Utviklerens eget dossier.","Byggherrens eget dossier.")

a("Which homes carry the large terraces, and what that does to the price.",
 "Qué viviendas tienen las terrazas grandes y cómo repercute eso en el precio.",
 "Quels logements possèdent les grandes terrasses, et ce que cela change au prix.",
 "Welche Wohnungen die großen Terrassen haben und was das mit dem Preis macht.",
 "В каких квартирах большие террасы и как это сказывается на цене.",
 "أيّ المساكن تحمل التراسات الكبيرة، وما أثر ذلك في السعر.",
 "Welke woningen de grote terrassen hebben, en wat dat met de prijs doet.",
 "Które mieszkania mają duże tarasy i jak wpływa to na cenę.",
 "Hvilke boliger som har de store terrassene, og hva det gjør med prisen.",
 "Vilka bostäder som har de stora terrasserna, och vad det gör med priset.")
a("How much of the sea each level actually sees over the village.",
 "Cuánto mar ve realmente cada nivel por encima del pueblo.",
 "Quelle part de mer chaque niveau voit réellement au-dessus du village.",
 "Wie viel Meer jede Ebene über dem Dorf tatsächlich sieht.",
 "Сколько моря реально видно с каждого уровня над городком.",
 "مقدار ما يراه كل مستوى من البحر فعلياً فوق القرية.",
 "Hoeveel zee elk niveau werkelijk ziet over het dorp heen.",
 "Ile morza faktycznie widzi każdy poziom ponad miasteczkiem.",
 "Hvor mye av sjøen hvert nivå faktisk ser over landsbyen.",
 "Hur mycket av havet varje nivå faktiskt ser över byn.")
a("The community fee, and what the AA rating saves against it.",
 "La cuota de comunidad y cuánto ahorra frente a ella la calificación AA.",
 "Les charges de copropriété, et ce que la classe AA permet d'économiser en regard.",
 "Das Hausgeld und was die AA-Klasse dagegen einspart.",
 "Размер взносов в сообщество и что на его фоне экономит класс AA.",
 "رسم المجمّع، وما يوفّره تصنيف AA إزاءه.",
 "De servicekosten, en wat het AA-label daartegenover bespaart.",
 "Opłata na wspólnotę i ile w jej zestawieniu oszczędza klasa AA.",
 "Fellesutgiftene, og hva energiklasse AA sparer mot dem.",
 "Avgiften till samfälligheten, och vad energiklass AA sparar mot den.")

a("Benalmádena Pueblo, <em>above the coast</em>",
 "Benalmádena Pueblo, <em>sobre la costa</em>","Benalmádena Pueblo, <em>au-dessus de la côte</em>",
 "Benalmádena Pueblo, <em>über der Küste</em>","Бенальмадена-Пуэбло, <em>над побережьем</em>",
 "بينالمادينا بويبلو، <em>فوق الساحل</em>","Benalmádena Pueblo, <em>boven de kust</em>",
 "Benalmádena Pueblo, <em>nad wybrzeżem</em>","Benalmádena Pueblo, <em>over kysten</em>","Benalmádena Pueblo, <em>ovanför kusten</em>")

a("A gated scheme of 70 homes on the slope above Benalmádena Pueblo, with the old town, the beaches and the motorway all a short drive away.",
 "Una promoción cerrada de 70 viviendas en la ladera sobre Benalmádena Pueblo, con el casco antiguo, las playas y la autovía a pocos minutos en coche.",
 "Un programme fermé de 70 logements sur le coteau au-dessus de Benalmádena Pueblo, avec le vieux centre, les plages et l'autoroute à quelques minutes en voiture.",
 "Eine geschlossene Anlage mit 70 Wohnungen am Hang über Benalmádena Pueblo, Altstadt, Strände und Autobahn jeweils eine kurze Fahrt entfernt.",
 "Закрытый комплекс из 70 квартир на склоне над Бенальмадена-Пуэбло: старый город, пляжи и автострада — в нескольких минутах езды.",
 "مجمّع مغلق من 70 مسكناً على المنحدر فوق بينالمادينا بويبلو، والبلدة القديمة والشواطئ والطريق السريع على مسافة قصيرة بالسيارة.",
 "Een gesloten project van 70 woningen op de helling boven Benalmádena Pueblo, met de oude kern, de stranden en de snelweg op een korte rit.",
 "Zamknięta inwestycja z 70 mieszkaniami na zboczu nad Benalmádena Pueblo, ze starym miastem, plażami i autostradą w kilka minut jazdy.",
 "Et portert prosjekt med 70 boliger i hellingen over Benalmádena Pueblo, med gamlebyen, strendene og motorveien en kort kjøretur unna.",
 "Ett grindat projekt med 70 bostäder på sluttningen ovanför Benalmádena Pueblo, med gamla stan, stränderna och motorvägen en kort bilfärd bort.")

a("Benalmádena <em>Pueblo</em>","Benalmádena <em>Pueblo</em>","Benalmádena <em>Pueblo</em>","Benalmádena <em>Pueblo</em>","Бенальмадена-<em>Пуэбло</em>","بينالمادينا <em>بويبلو</em>","Benalmádena <em>Pueblo</em>","Benalmádena <em>Pueblo</em>","Benalmádena <em>Pueblo</em>","Benalmádena <em>Pueblo</em>")
a("Benalmádena beaches","Playas de Benalmádena","Plages de Benalmádena","Strände von Benalmádena","Пляжи Бенальмадены","شواطئ بينالمادينا","Stranden van Benalmádena","Plaże Benalmádeny","Strendene i Benalmádena","Benalmádenas stränder")
a("Approx. 15 min","Aprox. 15 min","Environ 15 min","Ca. 15 Min.","Ок. 15 мин","نحو 15 دقيقة","Ca. 15 min","Ok. 15 min","Ca. 15 min","Ca. 15 min")

a("Eight of the 70 apartments: five with two bedrooms and three with three.",
 "Ocho de los 70 apartamentos: cinco de dos dormitorios y tres de tres.",
 "Huit des 70 appartements : cinq de deux chambres et trois de trois.",
 "Acht der 70 Wohnungen: fünf mit zwei und drei mit drei Schlafzimmern.",
 "Восемь из 70 квартир: пять с двумя спальнями и три с тремя.",
 "ثمانٍ من الشقق الـ 70: خمس بغرفتي نوم وثلاث بثلاث غرف.",
 "Acht van de 70 appartementen: vijf met twee en drie met drie slaapkamers.",
 "Osiem z 70 mieszkań: pięć dwusypialnianych i trzy trzysypialniane.",
 "Åtte av de 70 leilighetene: fem med to soverom og tre med tre.",
 "Åtta av de 70 lägenheterna: fem med två sovrum och tre med tre.")
a("From EUR 338,900 to EUR 570,400, excluding VAT and the other purchase costs.",
 "De 338.900 € a 570.400 €, sin incluir el IVA ni los demás gastos de compra.",
 "De 338 900 € à 570 400 €, hors TVA et autres frais d'acquisition.",
 "Von 338.900 € bis 570.400 €, ohne MwSt. und die übrigen Kaufnebenkosten.",
 "От 338 900 € до 570 400 €, без НДС и прочих расходов на покупку.",
 "من 338,900 € إلى 570,400 €، دون ضريبة القيمة المضافة وسائر تكاليف الشراء.",
 "Van € 338.900 tot € 570.400, exclusief btw en de overige aankoopkosten.",
 "Od 338 900 € do 570 400 €, bez VAT i pozostałych kosztów zakupu.",
 "Fra 338 900 € til 570 400 €, uten mva og de øvrige kjøpsomkostningene.",
 "Från 338 900 € till 570 400 €, exklusive moms och övriga köpkostnader.")
a("From 85 to 110 sqm built, with terraces from 14.50 to 77.60 sqm.",
 "De 85 a 110 m² construidos, con terrazas de 14,50 a 77,60 m².",
 "De 85 à 110 m² construits, avec des terrasses de 14,50 à 77,60 m².",
 "Von 85 bis 110 m² bebaut, mit Terrassen von 14,50 bis 77,60 m².",
 "От 85 до 110 м² застройки, с террасами от 14,50 до 77,60 м².",
 "من 85 إلى 110 م² مبنية، مع تراسات من 14.50 إلى 77.60 م².",
 "Van 85 tot 110 m² bebouwd, met terrassen van 14,50 tot 77,60 m².",
 "Od 85 do 110 m² powierzchni zabudowy, z tarasami od 14,50 do 77,60 m².",
 "Fra 85 til 110 m² bruksareal, med terrasser fra 14,50 til 77,60 m².",
 "Från 85 till 110 m² byggyta, med terrasser från 14,50 till 77,60 m².")
a("Completion is given as the last quarter of 2027.",
 "La entrega está prevista para el último trimestre de 2027.",
 "La livraison est annoncée au dernier trimestre 2027.",
 "Die Fertigstellung ist für das letzte Quartal 2027 angegeben.",
 "Сдача указана на 4 кв. 2027 года.",
 "التسليم محدد في الربع الأخير من 2027.",
 "De oplevering is opgegeven voor het laatste kwartaal van 2027.",
 "Odbiór podano na IV kw. 2027 roku.",
 "Ferdigstilling er oppgitt til siste kvartal 2027.",
 "Färdigställandet anges till sista kvartalet 2027.")
a("Yes. Every home comes with two parking spaces and a storeroom.",
 "Sí. Cada vivienda incluye dos plazas de garaje y un trastero.",
 "Oui. Chaque logement comprend deux places de parking et un débarras.",
 "Ja. Zu jeder Wohnung gehören zwei Stellplätze und ein Abstellraum.",
 "Да. К каждой квартире прилагаются два машиноместа и кладовая.",
 "نعم. كل مسكن يشمل موقفي سيارات ومخزناً.",
 "Ja. Bij elke woning horen twee parkeerplaatsen en een berging.",
 "Tak. Do każdego mieszkania należą dwa miejsca postojowe i komórka.",
 "Ja. Til hver bolig hører to parkeringsplasser og bod.",
 "Ja. Till varje bostad hör två parkeringsplatser och förråd.")
a("A communal pool, a gym and a chill-out terrace, in a gated scheme.",
 "Piscina comunitaria, gimnasio y terraza chill-out, en una promoción cerrada.",
 "Une piscine commune, une salle de sport et une terrasse chill-out, dans un programme fermé.",
 "Ein Gemeinschaftspool, ein Fitnessraum und eine Chill-out-Terrasse, in einer geschlossenen Anlage.",
 "Общий бассейн, спортзал и терраса чил-аут в закрытом комплексе.",
 "مسبح مشترك وصالة رياضة وتراس استرخاء، داخل مجمّع مغلق.",
 "Een gemeenschappelijk zwembad, een fitnessruimte en een chill-outterras, in een gesloten project.",
 "Basen wspólny, siłownia i taras chill-out w zamkniętej inwestycji.",
 "Et fellesbasseng, et treningsrom og en chill-out-terrasse, i et portert prosjekt.",
 "En gemensam pool, ett gym och en chill-out-terrass, i ett grindat projekt.")

a("The availability list, the specification and the dossier.",
 "La lista de disponibilidad, la memoria de calidades y el dosier.",
 "La liste des disponibilités, le descriptif technique et le dossier.",
 "Die Verfügbarkeitsliste, die Baubeschreibung und das Dossier.",
 "Список наличия, спецификация и досье.",
 "قائمة التوافر ومواصفات التشطيب والملف التعريفي.",
 "De beschikbaarheidslijst, het bestek en het dossier.",
 "Lista dostępności, specyfikacja wykończenia i dossier.",
 "Tilgjengelighetslisten, kravspesifikasjonen og dossieret.",
 "Tillgänglighetslistan, kravspecifikationen och dossiern.")

a("I would like the current availability and prices for the Benalmadena Village Residences.",
 "Me gustaría recibir la disponibilidad y los precios actuales de Benalmadena Village Residences.",
 "Je souhaite recevoir les disponibilités et les prix actuels de Benalmadena Village Residences.",
 "Ich möchte die aktuelle Verfügbarkeit und die Preise von Benalmadena Village Residences erhalten.",
 "Хотелось бы получить текущее наличие и цены по Benalmadena Village Residences.",
 "أودّ الحصول على التوافر والأسعار الحالية لمشروع Benalmadena Village Residences.",
 "Ik ontvang graag de actuele beschikbaarheid en prijzen van Benalmadena Village Residences.",
 "Chciałbym otrzymać aktualną dostępność i ceny dla Benalmadena Village Residences.",
 "Jeg ønsker gjeldende tilgjengelighet og priser for Benalmadena Village Residences.",
 "Jag vill gärna få aktuell tillgänglighet och priser för Benalmadena Village Residences.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
