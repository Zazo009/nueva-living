# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Thirteen of thirty-six townhouses still available at El Higuerón, between Fuengirola and Benalmádena, each with a private pool on its roof solarium, two parking spaces and a storeroom, in a gated scheme with three communal pools, a gym and a spa.",
 "Trece de treinta y seis adosados todavía disponibles en El Higuerón, entre Fuengirola y Benalmádena, cada uno con piscina privada en el solárium, dos plazas de garaje y trastero, en una promoción cerrada con tres piscinas comunitarias, gimnasio y spa.",
 "Treize maisons de ville sur trente-six encore disponibles à El Higuerón, entre Fuengirola et Benalmádena, chacune avec piscine privative sur son solarium, deux places de parking et un débarras, dans un programme fermé avec trois piscines communes, une salle de sport et un spa.",
 "Dreizehn von sechsunddreißig Reihenhäusern sind in El Higuerón zwischen Fuengirola und Benalmádena noch verfügbar, jedes mit eigenem Pool auf dem Dachsolarium, zwei Stellplätzen und einem Abstellraum, in einer geschlossenen Anlage mit drei Gemeinschaftspools, Fitnessraum und Spa.",
 "Тринадцать из тридцати шести таунхаусов ещё доступны в Эль-Игероне, между Фуэнхиролой и Бенальмаденой: у каждого собственный бассейн на солярии, два машиноместа и кладовая, в закрытом комплексе с тремя общими бассейнами, спортзалом и спа.",
 "ثلاثة عشر منزلاً متلاصقاً من أصل ستة وثلاثين ما زالت متاحة في إل إيغيرون، بين فوينخيرولا وبينالمادينا، لكل منها مسبح خاص على السولاريوم وموقفا سيارات ومخزن، ضمن مجمّع مغلق بثلاثة مسابح مشتركة وصالة رياضة وسبا.",
 "Dertien van de zesendertig herenhuizen nog beschikbaar in El Higuerón, tussen Fuengirola en Benalmádena, elk met een eigen zwembad op het dakterras, twee parkeerplaatsen en een berging, in een gesloten project met drie gemeenschappelijke zwembaden, een fitnessruimte en een spa.",
 "Trzynaście z trzydziestu sześciu domów szeregowych wciąż dostępnych w El Higuerón, między Fuengirolą a Benalmádeną, każdy z prywatnym basenem na solarium, dwoma miejscami postojowymi i komórką, w zamkniętej inwestycji z trzema basenami wspólnymi, siłownią i spa.",
 "Tretten av trettiseks rekkehus er fortsatt ledige i El Higuerón, mellom Fuengirola og Benalmádena, hvert med eget basseng på solterrassen, to parkeringsplasser og bod, i et portert prosjekt med tre fellesbassenger, treningsrom og spa.",
 "Tretton av trettiosex radhus är fortfarande lediga i El Higuerón, mellan Fuengirola och Benalmádena, vart och ett med egen pool på solterrassen, två parkeringsplatser och förråd, i ett grindat projekt med tre gemensamma pooler, gym och spa.")

a("Thirteen new-build townhouses available at El Higuerón, Fuengirola: 170.30 to 187.49 sqm built, terraces from 80.61 sqm, a private rooftop pool on every home, three communal pools, gym and spa, BREEAM certified.",
 "Trece adosados de obra nueva disponibles en El Higuerón, Fuengirola: de 170,30 a 187,49 m² construidos, terrazas desde 80,61 m², piscina privada en cubierta en todas las viviendas, tres piscinas comunitarias, gimnasio y spa, con certificación BREEAM.",
 "Treize maisons de ville neuves disponibles à El Higuerón, Fuengirola : de 170,30 à 187,49 m² construits, terrasses à partir de 80,61 m², une piscine privative en toiture sur chaque logement, trois piscines communes, salle de sport et spa, certifié BREEAM.",
 "Dreizehn neue Reihenhäuser in El Higuerón, Fuengirola: 170,30 bis 187,49 m² bebaut, Terrassen ab 80,61 m², ein eigener Dachpool je Haus, drei Gemeinschaftspools, Fitnessraum und Spa, BREEAM-zertifiziert.",
 "Тринадцать новых таунхаусов в Эль-Игероне, Фуэнхирола: от 170,30 до 187,49 м² застройки, террасы от 80,61 м², собственный бассейн на крыше каждого дома, три общих бассейна, спортзал и спа, сертификация BREEAM.",
 "ثلاثة عشر منزلاً متلاصقاً جديداً متاحة في إل إيغيرون، فوينخيرولا: من 170.30 إلى 187.49 م² مبنية، وتراسات من 80.61 م²، ومسبح خاص على السطح في كل مسكن، وثلاثة مسابح مشتركة وصالة رياضة وسبا، بشهادة BREEAM.",
 "Dertien nieuwbouwherenhuizen beschikbaar in El Higuerón, Fuengirola: 170,30 tot 187,49 m² bebouwd, terrassen vanaf 80,61 m², een eigen dakzwembad bij elke woning, drie gemeenschappelijke zwembaden, fitnessruimte en spa, BREEAM-gecertificeerd.",
 "Trzynaście nowych domów szeregowych dostępnych w El Higuerón w Fuengiroli: od 170,30 do 187,49 m² powierzchni zabudowy, tarasy od 80,61 m², prywatny basen na dachu w każdym domu, trzy baseny wspólne, siłownia i spa, certyfikat BREEAM.",
 "Tretten nye rekkehus ledige i El Higuerón, Fuengirola: 170,30 til 187,49 m² bruksareal, terrasser fra 80,61 m², eget takbasseng i hver bolig, tre fellesbassenger, treningsrom og spa, BREEAM-sertifisert.",
 "Tretton nyproducerade radhus lediga i El Higuerón, Fuengirola: 170,30 till 187,49 m² byggyta, terrasser från 80,61 m², egen takpool i varje bostad, tre gemensamma pooler, gym och spa, BREEAM-certifierat.")

a("El Higuerón, Fuengirola","El Higuerón, Fuengirola","El Higuerón, Fuengirola","El Higuerón, Fuengirola",
 "Эль-Игерон, Фуэнхирола","إل إيغيرون، فوينخيرولا","El Higuerón, Fuengirola","El Higuerón, Fuengirola","El Higuerón, Fuengirola","El Higuerón, Fuengirola")

a("Thirteen of thirty-six townhouses still available at El Higuerón, each with a private pool on its roof solarium and views over the Mediterranean.",
 "Trece de treinta y seis adosados todavía disponibles en El Higuerón, cada uno con piscina privada en el solárium y vistas al Mediterráneo.",
 "Treize maisons de ville sur trente-six encore disponibles à El Higuerón, chacune avec piscine privative sur son solarium et vue sur la Méditerranée.",
 "Dreizehn von sechsunddreißig Reihenhäusern in El Higuerón sind noch verfügbar, jedes mit eigenem Pool auf dem Dachsolarium und Blick aufs Mittelmeer.",
 "Тринадцать из тридцати шести таунхаусов ещё доступны в Эль-Игероне: у каждого собственный бассейн на солярии и вид на Средиземное море.",
 "ثلاثة عشر منزلاً متلاصقاً من أصل ستة وثلاثين ما زالت متاحة في إل إيغيرون، لكل منها مسبح خاص على السولاريوم وإطلالة على البحر المتوسط.",
 "Dertien van de zesendertig herenhuizen nog beschikbaar in El Higuerón, elk met een eigen zwembad op het dakterras en uitzicht over de Middellandse Zee.",
 "Trzynaście z trzydziestu sześciu domów szeregowych wciąż dostępnych w El Higuerón, każdy z prywatnym basenem na solarium i widokiem na Morze Śródziemne.",
 "Tretten av trettiseks rekkehus er fortsatt ledige i El Higuerón, hvert med eget basseng på solterrassen og utsikt over Middelhavet.",
 "Tretton av trettiosex radhus är fortfarande lediga i El Higuerón, vart och ett med egen pool på solterrassen och utsikt över Medelhavet.")

a("The houses and the <em>roof terraces</em>","Las viviendas y las <em>azoteas</em>","Les maisons et les <em>toits-terrasses</em>","Die Häuser und die <em>Dachterrassen</em>",
 "Дома и <em>крыши-террасы</em>","المنازل و<em>تراسات السطح</em>","De huizen en de <em>dakterrassen</em>","Domy i <em>tarasy na dachu</em>","Husene og <em>takterrassene</em>","Husen och <em>takterrasserna</em>")

a("Photographs of the completed show house, with computer-generated images of the communal gym, spa and pools. Furniture and decoration are indicative and are not included in the sale.",
 "Fotografías de la casa piloto terminada, junto con imágenes generadas por ordenador del gimnasio, el spa y las piscinas comunitarios. El mobiliario y la decoración son orientativos y no están incluidos en la venta.",
 "Photographies de la maison témoin achevée, accompagnées d’images de synthèse de la salle de sport, du spa et des piscines communs. Le mobilier et la décoration sont indicatifs et ne sont pas compris dans la vente.",
 "Fotografien des fertigen Musterhauses, dazu computergenerierte Bilder des gemeinschaftlichen Fitnessraums, des Spas und der Pools. Möbel und Dekoration sind unverbindlich und im Kauf nicht enthalten.",
 "Фотографии готового шоу-хауса и компьютерная графика общего спортзала, спа и бассейнов. Мебель и декор показаны для примера и в стоимость не входят.",
 "صور للمنزل النموذجي المكتمل، مع صور مولّدة بالحاسوب لصالة الرياضة والسبا والمسابح المشتركة. الأثاث والديكور استرشاديان وغير مشمولين في البيع.",
 "Foto’s van de voltooide modelwoning, met computerbeelden van de gemeenschappelijke fitnessruimte, spa en zwembaden. Meubels en decoratie zijn indicatief en niet bij de verkoop inbegrepen.",
 "Zdjęcia ukończonego domu pokazowego oraz wizualizacje komputerowe wspólnej siłowni, spa i basenów. Meble i dekoracje mają charakter poglądowy i nie są objęte sprzedażą.",
 "Fotografier av det ferdige visningshuset, sammen med datagenererte bilder av det felles treningsrommet, spaet og bassengene. Møbler og dekor er veiledende og inngår ikke i salget.",
 "Fotografier av det färdiga visningshuset, tillsammans med datorgenererade bilder av det gemensamma gymmet, spat och poolerna. Möbler och inredning är vägledande och ingår inte i köpet.")

a("A private pool set into the timber deck of a roof solarium, under a white pergola",
 "Una piscina privada integrada en la tarima del solárium, bajo una pérgola blanca",
 "Une piscine privative encastrée dans la terrasse en bois du solarium, sous une pergola blanche",
 "Ein privater Pool, eingelassen in das Holzdeck eines Dachsolariums, unter einer weißen Pergola",
 "Собственный бассейн, встроенный в деревянный настил солярия под белой перголой",
 "مسبح خاص مدمج في السطح الخشبي للسولاريوم تحت بيرغولا بيضاء",
 "Een privézwembad verzonken in het houten dek van een dakterras, onder een witte pergola",
 "Prywatny basen wpuszczony w drewniany pokład solarium, pod białą pergolą",
 "Et privat basseng felt ned i tredekket på en solterrasse, under en hvit pergola",
 "En privat pool nedsänkt i solterrassens trädäck, under en vit pergola")
a("The rooftop pool","La piscina en la azotea","La piscine en toiture","Der Dachpool","Бассейн на крыше","مسبح السطح","Het dakzwembad","Basen na dachu","Takbassenget","Takpoolen")

a("The rooftop pool and a lounge seat under the pergola, with the sierra behind",
 "La piscina de la azotea y un asiento de descanso bajo la pérgola, con la sierra al fondo",
 "La piscine en toiture et une assise longue sous la pergola, la sierra en arrière-plan",
 "Der Dachpool und eine Liege unter der Pergola, dahinter die Sierra",
 "Бассейн на крыше и лежак под перголой, за ними сьерра",
 "مسبح السطح ومقعد استرخاء تحت البيرغولا، والجبال في الخلفية",
 "Het dakzwembad en een loungebank onder de pergola, met de sierra erachter",
 "Basen na dachu i siedzisko wypoczynkowe pod pergolą, z sierrą w tle",
 "Takbassenget og en loungeseng under pergolaen, med fjellene bak",
 "Takpoolen och en loungesits under pergolan, med bergen bakom")

a("A dining table on the roof solarium beside the pool, the sea on the horizon",
 "Una mesa de comedor en el solárium junto a la piscina, con el mar en el horizonte",
 "Une table à manger sur le solarium au bord de la piscine, la mer à l’horizon",
 "Ein Esstisch auf dem Dachsolarium neben dem Pool, das Meer am Horizont",
 "Обеденный стол на солярии у бассейна, море на горизонте",
 "طاولة طعام على السولاريوم بجانب المسبح، والبحر في الأفق",
 "Een eettafel op het dakterras naast het zwembad, de zee aan de horizon",
 "Stół jadalny na solarium przy basenie, z morzem na horyzoncie",
 "Et spisebord på solterrassen ved bassenget, sjøen i horisonten",
 "Ett matbord på solterrassen vid poolen, havet vid horisonten")

a("The rooftop pool looking out over the rooftops of the town to the sea",
 "La piscina de la azotea mirando por encima de los tejados del pueblo hacia el mar",
 "La piscine en toiture ouverte au-delà des toits du village vers la mer",
 "Der Dachpool mit Blick über die Dächer des Orts zum Meer",
 "Бассейн на крыше с видом поверх крыш посёлка на море",
 "مسبح السطح يطلّ فوق أسطح البلدة نحو البحر",
 "Het dakzwembad met uitzicht over de daken van het dorp naar de zee",
 "Basen na dachu z widokiem ponad dachami miasteczka ku morzu",
 "Takbassenget med utsikt over takene i stedet og ut mot sjøen",
 "Takpoolen med utsikt över ortens tak och ut mot havet")
a("Above the town","Sobre el pueblo","Au-dessus du village","Über dem Ort","Над посёлком","فوق البلدة","Boven het dorp","Ponad miasteczkiem","Over stedet","Ovanför orten")

a("A stainless outdoor kitchen and barbecue built into the roof terrace",
 "Una cocina exterior de acero inoxidable con barbacoa integrada en la azotea",
 "Une cuisine d’extérieur en inox avec barbecue intégrée au toit-terrasse",
 "Eine Außenküche aus Edelstahl mit Grill, in die Dachterrasse eingebaut",
 "Уличная кухня из нержавеющей стали с грилем, встроенная в крышу-террасу",
 "مطبخ خارجي من الفولاذ المقاوم للصدأ وشواية مدمجان في تراس السطح",
 "Een rvs-buitenkeuken met barbecue, ingebouwd in het dakterras",
 "Kuchnia zewnętrzna ze stali nierdzewnej z grillem, wbudowana w taras na dachu",
 "Et utekjøkken i rustfritt stål med grill, bygget inn i takterrassen",
 "Ett utekök i rostfritt stål med grill, inbyggt i takterrassen")
a("The outdoor kitchen","La cocina exterior","La cuisine d’extérieur","Die Außenküche","Уличная кухня","المطبخ الخارجي","De buitenkeuken","Kuchnia zewnętrzna","Utekjøkkenet","Uteköket")

a("A gas fire pit set into a low table between outdoor sofas",
 "Un brasero de gas integrado en una mesa baja entre sofás de exterior",
 "Un foyer à gaz encastré dans une table basse entre des canapés d’extérieur",
 "Eine Gasfeuerstelle in einem niedrigen Tisch zwischen Außensofas",
 "Газовый очаг, встроенный в низкий стол между уличными диванами",
 "موقد غاز مدمج في طاولة منخفضة بين أرائك خارجية",
 "Een gasvuurtafel verzonken in een lage tafel tussen buitenbanken",
 "Palenisko gazowe wpuszczone w niski stół między sofami ogrodowymi",
 "Et gassbålfat felt ned i et lavt bord mellom utesofaer",
 "En gaseldstad nedsänkt i ett lågt bord mellan utesoffor")
a("The fire pit","El brasero","Le foyer","Die Feuerstelle","Очаг","الموقد","De vuurtafel","Palenisko","Bålfatet","Eldstaden")

a("A round table and chairs on the roof terrace, the coast beyond the glass balustrade",
 "Una mesa redonda con sillas en la azotea, con la costa al otro lado de la barandilla de vidrio",
 "Une table ronde et des chaises sur le toit-terrasse, la côte au-delà du garde-corps vitré",
 "Ein runder Tisch mit Stühlen auf der Dachterrasse, dahinter die Küste hinter der Glasbrüstung",
 "Круглый стол со стульями на крыше-террасе, за стеклянным ограждением — побережье",
 "طاولة مستديرة وكراسي على تراس السطح، والساحل خلف الدرابزين الزجاجي",
 "Een ronde tafel met stoelen op het dakterras, de kust achter de glazen balustrade",
 "Okrągły stół z krzesłami na tarasie na dachu, wybrzeże za szklaną balustradą",
 "Et rundt bord med stoler på takterrassen, kysten bak glassrekkverket",
 "Ett runt bord med stolar på takterrassen, kusten bortom glasräcket")
a("The rooftop table","La mesa en la azotea","La table en toiture","Der Tisch auf dem Dach","Стол на крыше","طاولة السطح","De tafel op het dak","Stół na dachu","Bordet på taket","Bordet på taket")

a("The shaded end of the roof terrace, with the outdoor kitchen along one side",
 "El extremo en sombra de la azotea, con la cocina exterior a lo largo de un lateral",
 "L’extrémité ombragée du toit-terrasse, la cuisine d’extérieur le long d’un côté",
 "Das beschattete Ende der Dachterrasse, an einer Seite die Außenküche",
 "Затенённая часть крыши-террасы, вдоль одной стороны — уличная кухня",
 "الطرف المظلّل من تراس السطح، والمطبخ الخارجي على أحد جانبيه",
 "Het beschaduwde einde van het dakterras, met de buitenkeuken langs één zijde",
 "Zacieniony koniec tarasu na dachu, z kuchnią zewnętrzną wzdłuż jednego boku",
 "Den skyggelagte enden av takterrassen, med utekjøkkenet langs den ene siden",
 "Den skuggade änden av takterrassen, med uteköket längs ena sidan")
a("The shaded terrace","La terraza en sombra","La terrasse ombragée","Die beschattete Terrasse","Затенённая терраса","التراس المظلّل","Het beschaduwde terras","Zacieniony taras","Den skyggelagte terrassen","Den skuggade terrassen")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
