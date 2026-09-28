# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("The current price list, the floorplans and the specification.",
 "La lista de precios vigente, los planos y la memoria de calidades.",
 "La liste de prix en vigueur, les plans et le descriptif.",
 "Die aktuelle Preisliste, die Grundrisse und die Baubeschreibung.",
 "Действующий прайс-лист, планировки и спецификация.",
 "قائمة الأسعار الحالية والمخططات والمواصفات.",
 "De actuele prijslijst, de plattegronden en de bouwbeschrijving.",
 "Aktualny cennik, rzuty i standard wykończenia.",
 "Gjeldende prisliste, planløsningene og beskrivelsen.",
 "Aktuell prislista, planlösningarna och beskrivningen.")

a("The thirteen available houses with areas, orientation and price",
 "Las trece viviendas disponibles con superficies, orientación y precio",
 "Les treize maisons disponibles avec surfaces, orientation et prix",
 "Die dreizehn verfügbaren Häuser mit Flächen, Ausrichtung und Preis",
 "Тринадцать доступных домов с площадями, ориентацией и ценой",
 "المنازل الثلاثة عشر المتاحة مع المساحات والاتجاه والسعر",
 "De dertien beschikbare huizen met oppervlakten, oriëntatie en prijs",
 "Trzynaście dostępnych domów z powierzchniami, orientacją i ceną",
 "De tretten ledige husene med arealer, himmelretning og pris",
 "De tretton lediga husen med ytor, väderstreck och pris")

a("The plan for each house, level by level",
 "El plano de cada vivienda, planta por planta",
 "Le plan de chaque maison, niveau par niveau",
 "Der Plan für jedes Haus, Ebene für Ebene",
 "План каждого дома, уровень за уровнем",
 "مخطط كل منزل، مستوى بمستوى",
 "De plattegrond van elk huis, laag voor laag",
 "Rzut każdego domu, kondygnacja po kondygnacji",
 "Planen for hvert hus, plan for plan",
 "Ritningen för varje hus, plan för plan")

a("See the <em>show house</em>","Ver la <em>casa piloto</em>","Voir la <em>maison témoin</em>","Das <em>Musterhaus</em> sehen",
 "Посмотреть <em>шоу-хаус</em>","شاهد <em>المنزل النموذجي</em>","Bekijk de <em>modelwoning</em>","Zobacz <em>dom pokazowy</em>","Se <em>visningshuset</em>","Se <em>visningshuset</em>")

a("The show house is finished and furnished, so a visit shows the real thing rather than a drawing.",
 "La casa piloto está terminada y amueblada, así que la visita muestra la realidad y no un plano.",
 "La maison témoin est achevée et meublée : la visite montre la réalité, pas un plan.",
 "Das Musterhaus ist fertig und möbliert, ein Besuch zeigt also die Wirklichkeit statt einer Zeichnung.",
 "Шоу-хаус завершён и меблирован, так что визит показывает реальность, а не чертёж.",
 "المنزل النموذجي مكتمل ومفروش، فالزيارة تُظهر الواقع لا مجرد رسم.",
 "De modelwoning is af en gemeubileerd, dus een bezoek laat de werkelijkheid zien in plaats van een tekening.",
 "Dom pokazowy jest ukończony i umeblowany, więc wizyta pokazuje rzeczywistość, a nie rysunek.",
 "Visningshuset er ferdig og møblert, så et besøk viser det virkelige og ikke en tegning.",
 "Visningshuset är färdigt och möblerat, så ett besök visar verkligheten och inte en ritning.")

a("Walk the finished show house, including its roof solarium and pool.",
 "Recorrer la casa piloto terminada, incluidos su solárium y su piscina.",
 "Parcourir la maison témoin achevée, y compris son solarium et sa piscine.",
 "Das fertige Musterhaus ablaufen, samt Dachsolarium und Pool.",
 "Пройти по готовому шоу-хаусу, включая солярий и бассейн.",
 "التجوّل في المنزل النموذجي المكتمل، بما فيه السولاريوم والمسبح.",
 "De voltooide modelwoning doorlopen, inclusief het dakterras en het zwembad.",
 "Przejść przez ukończony dom pokazowy, łącznie z solarium i basenem.",
 "Gå gjennom det ferdige visningshuset, inkludert solterrassen og bassenget.",
 "Gå igenom det färdiga visningshuset, inklusive solterrassen och poolen.")

a("Compare what each terrace of houses faces, and how much sea each row keeps.",
 "Comparar hacia dónde mira cada terraza de viviendas y cuánto mar conserva cada hilera.",
 "Comparer l’exposition de chaque terrasse de maisons et la part de mer que garde chaque rangée.",
 "Vergleichen, wohin jede Häuserterrasse blickt und wie viel Meer jede Reihe behält.",
 "Сравнить, куда выходит каждый уступ домов и сколько моря остаётся у каждого ряда.",
 "مقارنة اتجاه كل مصطبة من المنازل، وكم يبقى لكل صف من إطلالة البحر.",
 "Vergelijken waar elk terras met huizen op uitkijkt, en hoeveel zee elke rij behoudt.",
 "Porównać, na co wychodzi każdy taras domów i ile morza zachowuje każdy rząd.",
 "Sammenligne hva hver husterrasse vender mot, og hvor mye sjø hver rad beholder.",
 "Jämföra vad varje husterrass vetter mot, och hur mycket hav varje rad behåller.")

a("See the garden and the storeroom that come with the specific house, which vary a good deal.",
 "Ver el jardín y el trastero que corresponden a la vivienda concreta, que varían bastante.",
 "Voir le jardin et le débarras attachés à la maison concernée, qui varient sensiblement.",
 "Den Garten und den Abstellraum des konkreten Hauses sehen, die sich deutlich unterscheiden.",
 "Увидеть сад и кладовую конкретного дома — они заметно различаются.",
 "رؤية الحديقة والمخزن الخاصّين بالمنزل المحدّد، وهما يتفاوتان كثيراً.",
 "Zien welke tuin en berging bij het betreffende huis horen, die nogal verschillen.",
 "Zobaczyć ogród i komórkę przypisane do konkretnego domu, bo znacznie się różnią.",
 "Se hagen og boden som følger det konkrete huset, som varierer en god del.",
 "Se trädgården och förrådet som hör till det aktuella huset, som varierar en hel del.")

a("El Higuerón, <em>Fuengirola</em>","El Higuerón, <em>Fuengirola</em>","El Higuerón, <em>Fuengirola</em>","El Higuerón, <em>Fuengirola</em>",
 "Эль-Игерон, <em>Фуэнхирола</em>","إل إيغيرون، <em>فوينخيرولا</em>","El Higuerón, <em>Fuengirola</em>","El Higuerón, <em>Fuengirola</em>","El Higuerón, <em>Fuengirola</em>","El Higuerón, <em>Fuengirola</em>")

a("A gated hillside scheme at El Higuerón, above Carvajal, between Fuengirola and Benalmádena and a few minutes from the A-7.",
 "Una promoción cerrada en ladera en El Higuerón, sobre Carvajal, entre Fuengirola y Benalmádena y a pocos minutos de la A-7.",
 "Un programme fermé à flanc de coteau à El Higuerón, au-dessus de Carvajal, entre Fuengirola et Benalmádena et à quelques minutes de l’A-7.",
 "Eine geschlossene Hanganlage in El Higuerón, über Carvajal, zwischen Fuengirola und Benalmádena und wenige Minuten von der A-7.",
 "Закрытый комплекс на склоне в Эль-Игероне, над Карвахалем, между Фуэнхиролой и Бенальмаденой, в нескольких минутах от A-7.",
 "مجمّع مغلق على منحدر في إل إيغيرون، فوق كارباخال، بين فوينخيرولا وبينالمادينا وعلى بُعد دقائق من الطريق A-7.",
 "Een gesloten hellingproject in El Higuerón, boven Carvajal, tussen Fuengirola en Benalmádena en op enkele minuten van de A-7.",
 "Zamknięta inwestycja na zboczu w El Higuerón, ponad Carvajal, między Fuengirolą a Benalmádeną, kilka minut od A-7.",
 "Et portert skråningsprosjekt i El Higuerón, over Carvajal, mellom Fuengirola og Benalmádena og noen minutter fra A-7.",
 "Ett grindat sluttningsprojekt i El Higuerón, ovanför Carvajal, mellan Fuengirola och Benalmádena och några minuter från A-7.")

a("Thirteen of the thirty-six houses: two three-bedroom and eleven four-bedroom. Twenty-three are sold or reserved.",
 "Trece de las treinta y seis viviendas: dos de tres dormitorios y once de cuatro. Veintitrés están vendidas o reservadas.",
 "Treize des trente-six maisons : deux de trois chambres et onze de quatre. Vingt-trois sont vendues ou réservées.",
 "Dreizehn der sechsunddreißig Häuser: zwei mit drei und elf mit vier Schlafzimmern. Dreiundzwanzig sind verkauft oder reserviert.",
 "Тринадцать из тридцати шести домов: два с тремя спальнями и одиннадцать с четырьмя. Двадцать три проданы или забронированы.",
 "ثلاثة عشر من المنازل الستة والثلاثين: اثنان بثلاث غرف نوم وأحد عشر بأربع. وثلاثة وعشرون مباعة أو محجوزة.",
 "Dertien van de zesendertig huizen: twee met drie slaapkamers en elf met vier. Drieëntwintig zijn verkocht of gereserveerd.",
 "Trzynaście z trzydziestu sześciu domów: dwa trzypokojowe i jedenaście czteropokojowych. Dwadzieścia trzy są sprzedane lub zarezerwowane.",
 "Tretten av de trettiseks husene: to med tre soverom og elleve med fire. Tjuetre er solgt eller reservert.",
 "Tretton av de trettiosex husen: två med tre sovrum och elva med fyra. Tjugotre är sålda eller reserverade.")

a("Does every house have its own pool?","¿Todas las viviendas tienen piscina propia?","Chaque maison a-t-elle sa propre piscine ?","Hat jedes Haus einen eigenen Pool?",
 "У каждого дома есть свой бассейн?","هل لكل منزل مسبحه الخاص؟","Heeft elk huis een eigen zwembad?","Czy każdy dom ma własny basen?","Har hvert hus sitt eget basseng?","Har varje hus en egen pool?")

a("Yes. Every house in the scheme has a private pool on its roof solarium, with a sun terrace around it.",
 "Sí. Todas las viviendas de la promoción cuentan con piscina privada en su solárium, con terraza de sol alrededor.",
 "Oui. Chaque maison du programme dispose d’une piscine privative sur son solarium, entourée d’une terrasse de bains de soleil.",
 "Ja. Jedes Haus der Anlage hat einen eigenen Pool auf seinem Dachsolarium, umgeben von einer Sonnenterrasse.",
 "Да. У каждого дома комплекса собственный бассейн на солярии с солнечной террасой вокруг.",
 "نعم. لكل منزل في المشروع مسبح خاص على سولاريومه، تحيط به تراس للتشمّس.",
 "Ja. Elk huis in het project heeft een eigen zwembad op het dakterras, met een zonneterras eromheen.",
 "Tak. Każdy dom w inwestycji ma prywatny basen na swoim solarium, z tarasem słonecznym dookoła.",
 "Ja. Hvert hus i prosjektet har eget basseng på solterrassen, med soldekk rundt.",
 "Ja. Varje hus i projektet har egen pool på solterrassen, med soldäck runt om.")

a("The house, its garden, its rooftop pool, two parking spaces and a storeroom. Prices exclude the 10% IVA.",
 "La vivienda, su jardín, su piscina en la azotea, dos plazas de garaje y un trastero. Los precios no incluyen el 10% de IVA.",
 "La maison, son jardin, sa piscine en toiture, deux places de parking et un débarras. Les prix s’entendent hors TVA de 10%.",
 "Das Haus, sein Garten, sein Dachpool, zwei Stellplätze und ein Abstellraum. Die Preise verstehen sich ohne 10% MwSt.",
 "Дом, его сад, бассейн на крыше, два машиноместа и кладовая. Цены не включают 10% НДС.",
 "المنزل وحديقته ومسبحه على السطح وموقفا سيارات ومخزن. ولا تشمل الأسعار ضريبة القيمة المضافة 10%.",
 "Het huis, de tuin, het dakzwembad, twee parkeerplaatsen en een berging. De prijzen zijn exclusief 10% btw.",
 "Dom, jego ogród, basen na dachu, dwa miejsca postojowe i komórka. Ceny nie obejmują 10% VAT.",
 "Huset, hagen, takbassenget, to parkeringsplasser og bod. Prisene er eksklusive 10% mva.",
 "Huset, trädgården, takpoolen, två parkeringsplatser och förråd. Priserna är exklusive 10% moms.")

a("The houses are under construction and the show house is complete and furnished, but the developer publishes no completion date. We ask for a date in writing and put it in the contract rather than quoting one.",
 "Las viviendas están en obra y la casa piloto está terminada y amueblada, pero la promotora no publica fecha de entrega. Pedimos la fecha por escrito y la llevamos al contrato en lugar de citar ninguna.",
 "Les maisons sont en chantier et la maison témoin est achevée et meublée, mais le promoteur ne publie aucune date de livraison. Nous demandons la date par écrit et l’inscrivons au contrat plutôt que d’en avancer une.",
 "Die Häuser sind im Bau und das Musterhaus ist fertig und möbliert, doch der Bauträger veröffentlicht kein Fertigstellungsdatum. Wir lassen uns das Datum schriftlich geben und nehmen es in den Vertrag auf, statt eines zu nennen.",
 "Дома строятся, шоу-хаус завершён и меблирован, но застройщик не публикует дату сдачи. Мы запрашиваем её письменно и вносим в договор, а не называем сами.",
 "المنازل قيد الإنشاء والمنزل النموذجي مكتمل ومفروش، لكن الشركة المطوّرة لا تنشر تاريخ تسليم. نطلب التاريخ كتابةً وندرجه في العقد بدل ذكر تاريخ من عندنا.",
 "De huizen zijn in aanbouw en de modelwoning is af en gemeubileerd, maar de ontwikkelaar publiceert geen opleverdatum. Wij vragen de datum schriftelijk op en leggen die vast in het contract in plaats van er een te noemen.",
 "Domy są w budowie, a dom pokazowy jest ukończony i umeblowany, ale deweloper nie podaje daty odbioru. Prosimy o datę na piśmie i wpisujemy ją do umowy, zamiast podawać własną.",
 "Husene er under bygging og visningshuset er ferdig og møblert, men utbygger publiserer ingen ferdigstillelsesdato. Vi ber om datoen skriftlig og tar den inn i kontrakten i stedet for å oppgi en.",
 "Husen är under byggnation och visningshuset är färdigt och möblerat, men byggherren publicerar inget färdigställandedatum. Vi begär datumet skriftligt och för in det i avtalet i stället för att ange ett.")

a("Three communal pools, a gym, a spa with an indoor pool and a relaxation room, a co-working lounge, and more than 100,000 sqm of Mediterranean gardens.",
 "Tres piscinas comunitarias, gimnasio, spa con piscina cubierta y sala de relax, sala de coworking y más de 100.000 m² de jardín mediterráneo.",
 "Trois piscines communes, une salle de sport, un spa avec piscine intérieure et salle de relaxation, un salon de coworking, et plus de 100 000 m² de jardins méditerranéens.",
 "Drei Gemeinschaftspools, ein Fitnessraum, ein Spa mit Hallenbad und Ruheraum, eine Coworking-Lounge und über 100.000 m² mediterrane Gärten.",
 "Три общих бассейна, спортзал, спа с крытым бассейном и комнатой отдыха, коворкинг-лаундж и более 100 000 м² средиземноморских садов.",
 "ثلاثة مسابح مشتركة، وصالة رياضة، وسبا بمسبح داخلي وغرفة استرخاء، وصالة عمل مشترك، وأكثر من 100,000 م² من الحدائق المتوسطية.",
 "Drie gemeenschappelijke zwembaden, een fitnessruimte, een spa met binnenbad en relaxruimte, een coworkinglounge, en meer dan 100.000 m² mediterrane tuinen.",
 "Trzy baseny wspólne, siłownia, spa z basenem krytym i salą relaksu, salon coworkingowy oraz ponad 100 000 m² ogrodów śródziemnomorskich.",
 "Tre fellesbassenger, treningsrom, spa med innendørsbasseng og relaksrom, coworking-lounge, og mer enn 100 000 m² middelhavshager.",
 "Tre gemensamma pooler, gym, spa med inomhuspool och avkopplingsrum, coworkinglounge, och mer än 100 000 m² medelhavsträdgårdar.")

a("Which way do the houses face?","¿Hacia dónde miran las viviendas?","Quelle est l’orientation des maisons ?","In welche Richtung blicken die Häuser?",
 "Куда обращены дома?","إلى أي اتجاه تتّجه المنازل؟","Op welke richting liggen de huizen?","W którą stronę zwrócone są domy?","Hvilken vei vender husene?","Åt vilket håll vetter husen?")

a("South or south-west. The four terraces step down the hillside so that each row looks over the one below towards the sea.",
 "Al sur o al suroeste. Las cuatro terrazas descienden por la ladera para que cada hilera mire por encima de la inferior hacia el mar.",
 "Au sud ou au sud-ouest. Les quatre terrasses descendent le coteau afin que chaque rangée domine celle du dessous vers la mer.",
 "Nach Süden oder Südwesten. Die vier Terrassen treten den Hang hinab, sodass jede Reihe über die darunterliegende zum Meer blickt.",
 "На юг или юго-запад. Четыре уступа спускаются по склону так, что каждый ряд смотрит поверх нижнего в сторону моря.",
 "جنوباً أو جنوباً غربياً. وتتدرّج المصاطب الأربع على المنحدر بحيث يطلّ كل صف فوق الذي تحته نحو البحر.",
 "Op het zuiden of zuidwesten. De vier terrassen trappen de helling af zodat elke rij over de onderliggende heen naar de zee kijkt.",
 "Na południe lub południowy zachód. Cztery tarasy schodzą po zboczu tak, by każdy rząd patrzył ponad tym poniżej w stronę morza.",
 "Mot sør eller sørvest. De fire terrassene trapper seg nedover skråningen slik at hver rad ser over den under mot sjøen.",
 "Mot söder eller sydväst. De fyra terrasserna trappar ned för sluttningen så att varje rad ser över den nedanför mot havet.")

a("The price list, the floorplans and the specification.",
 "La lista de precios, los planos y la memoria de calidades.",
 "La liste de prix, les plans et le descriptif.",
 "Die Preisliste, die Grundrisse und die Baubeschreibung.",
 "Прайс-лист, планировки и спецификация.",
 "قائمة الأسعار والمخططات والمواصفات.",
 "De prijslijst, de plattegronden en de bouwbeschrijving.",
 "Cennik, rzuty i standard wykończenia.",
 "Prislisten, planløsningene og beskrivelsen.",
 "Prislistan, planlösningarna och beskrivningen.")

a("See the show house","Ver la casa piloto","Voir la maison témoin","Das Musterhaus sehen","Посмотреть шоу-хаус","شاهد المنزل النموذجي","Bekijk de modelwoning","Zobacz dom pokazowy","Se visningshuset","Se visningshuset")

a("We arrange the visit and walk the finished house and its roof terrace with you.",
 "Organizamos la visita y recorremos con usted la casa terminada y su azotea.",
 "Nous organisons la visite et parcourons avec vous la maison achevée et son toit-terrasse.",
 "Wir organisieren den Besuch und gehen mit Ihnen das fertige Haus und seine Dachterrasse ab.",
 "Мы организуем визит и вместе пройдём по готовому дому и его крыше-террасе.",
 "ننظّم الزيارة ونتجوّل معك في المنزل المكتمل وتراس سطحه.",
 "Wij regelen het bezoek en lopen samen met u het voltooide huis en het dakterras door.",
 "Organizujemy wizytę i przechodzimy z Państwem przez ukończony dom i jego taras na dachu.",
 "Vi arrangerer besøket og går gjennom det ferdige huset og takterrassen sammen med deg.",
 "Vi ordnar besöket och går igenom det färdiga huset och dess takterrass tillsammans med dig.")

a("I would like to receive the latest project information for the Higueron Rooftop Villas.",
 "Me gustaría recibir la información más reciente del proyecto Higueron Rooftop Villas.",
 "Je souhaite recevoir les dernières informations sur le projet Higueron Rooftop Villas.",
 "Ich möchte die aktuellen Projektinformationen zu den Higueron Rooftop Villas erhalten.",
 "Хочу получить актуальную информацию по проекту Higueron Rooftop Villas.",
 "أرغب في تلقّي أحدث معلومات المشروع الخاصة بـ Higueron Rooftop Villas.",
 "Ik ontvang graag de meest recente projectinformatie over de Higueron Rooftop Villas.",
 "Chciałbym otrzymać najnowsze informacje o projekcie Higueron Rooftop Villas.",
 "Jeg vil gjerne motta den nyeste prosjektinformasjonen om Higueron Rooftop Villas.",
 "Jag vill gärna få den senaste projektinformationen om Higueron Rooftop Villas.")

a("Project context: Higueron Rooftop Villas.",
 "Proyecto de referencia: Higueron Rooftop Villas.",
 "Projet concerné : Higueron Rooftop Villas.",
 "Projektbezug: Higueron Rooftop Villas.",
 "Проект: Higueron Rooftop Villas.",
 "سياق المشروع: Higueron Rooftop Villas.",
 "Projectcontext: Higueron Rooftop Villas.",
 "Kontekst projektu: Higueron Rooftop Villas.",
 "Prosjektkontekst: Higueron Rooftop Villas.",
 "Projektsammanhang: Higueron Rooftop Villas.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
