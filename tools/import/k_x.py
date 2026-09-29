# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Playa del Ángel, Estepona","Playa del Ángel, Estepona","Playa del Ángel, Estepona","Playa del Ángel, Estepona","Плая-дель-Анхель, Эстепона","بلايا ديل أنخيل، إستيبونا","Playa del Ángel, Estepona","Playa del Ángel, Estepona","Playa del Ángel, Estepona","Playa del Ángel, Estepona")
a("Playa del Ángel","Playa del Ángel","Playa del Ángel","Playa del Ángel","Плая-дель-Анхель","بلايا ديل أنخيل","Playa del Ángel","Playa del Ángel","Playa del Ángel","Playa del Ángel")
a("Playa del <em>Ángel</em>","Playa del <em>Ángel</em>","Playa del <em>Ángel</em>","Playa del <em>Ángel</em>","Плая-дель-<em>Анхель</em>","بلايا ديل <em>أنخيل</em>","Playa del <em>Ángel</em>","Playa del <em>Ángel</em>","Playa del <em>Ángel</em>","Playa del <em>Ángel</em>")
a("Apartments, penthouses and villas","Apartamentos, áticos y villas","Appartements, penthouses et villas","Wohnungen, Penthäuser und Villen","Квартиры, пентхаусы и виллы","شقق وشقق بنتهاوس وفيلات","Appartementen, penthouses en villa's","Apartamenty, Penthouse'y i wille","Leiligheter, toppleiligheter og villaer","Lägenheter, takvåningar och villor")
a("Completion Q4 2027 - Q1 2028","Entrega T4 2027 - T1 2028","Livraison T4 2027 - T1 2028","Fertigstellung Q4 2027 - Q1 2028","Сдача 4 кв. 2027 - 1 кв. 2028","التسليم الربع الرابع 2027 - الربع الأول 2028","Oplevering K4 2027 - K1 2028","Odbiór IV kw. 2027 - I kw. 2028","Ferdigstilling K4 2027 - K1 2028","Färdigställande K4 2027 - K1 2028")
a("Not stated","No indicado","Non indiqué","Nicht angegeben","Не указано","غير محدد","Niet opgegeven","Nie podano","Ikke oppgitt","Ej angivet")
a("Licence Granted","Licencia concedida","Permis accordé","Baugenehmigung erteilt","Разрешение получено","تم منح الرخصة","Vergunning verleend","Pozwolenie wydane","Tillatelse gitt","Bygglov beviljat")
a("Approx. 50 min","Aprox. 50 min","Environ 50 min","Ca. 50 Min.","Ок. 50 мин","نحو 50 دقيقة","Ca. 50 min","Ok. 50 min","Ca. 50 min","Ca. 50 min")
a("Approx. 45 min","Aprox. 45 min","Environ 45 min","Ca. 45 Min.","Ок. 45 мин","نحو 45 دقيقة","Ca. 45 min","Ok. 45 min","Ca. 45 min","Ca. 45 min")

a("Four homes left of 48 on the Estepona beachfront: three apartments and one of the six seafront villas, in a gated scheme with a spa, a gym and a padel court.",
 "Quedan cuatro viviendas de 48 en primera línea de playa de Estepona: tres apartamentos y una de las seis villas frente al mar, en una promoción cerrada con spa, gimnasio y pista de pádel.",
 "Quatre logements restants sur 48 en front de mer à Estepona : trois appartements et l'une des six villas face à la mer, dans un programme fermé avec spa, salle de sport et terrain de padel.",
 "Vier von 48 Wohnungen an der Strandpromenade von Estepona sind noch frei: drei Wohnungen und eine der sechs Villen am Meer, in einer geschlossenen Anlage mit Spa, Fitnessraum und Padelplatz.",
 "Осталось четыре из 48 домов на первой линии в Эстепоне: три квартиры и одна из шести вилл у моря, в закрытом комплексе со спа, спортзалом и падел-кортом.",
 "أربعة مساكن متبقية من أصل 48 على واجهة إستيبونا البحرية: ثلاث شقق وواحدة من الفيلات الست المطلّة على البحر، ضمن مجمّع مغلق بسبا وصالة رياضة وملعب بادل.",
 "Nog vier van de 48 woningen aan de kustlijn van Estepona: drie appartementen en een van de zes villa's aan zee, in een gesloten project met spa, fitnessruimte en padelbaan.",
 "Zostały cztery z 48 domów przy plaży w Esteponie: trzy mieszkania i jedna z sześciu willi nad morzem, w zamkniętej inwestycji ze spa, siłownią i kortem do padla.",
 "Fire av 48 boliger igjen i strandkanten i Estepona: tre leiligheter og en av de seks villaene ved sjøen, i et portert prosjekt med spa, treningsrom og padelbane.",
 "Fyra av 48 bostäder kvar i strandkanten i Estepona: tre lägenheter och en av de sex villorna vid havet, i ett grindat projekt med spa, gym och padelbana.")

a("Four of 48 new-build homes remaining on the Estepona seafront: apartments from EUR 3,500,000 and a beachfront villa at EUR 12,750,000, completion Q4 2027 to Q1 2028.",
 "Quedan cuatro de 48 viviendas de obra nueva en el frente marítimo de Estepona: apartamentos desde 3.500.000 € y una villa en primera línea por 12.750.000 €, entrega T4 2027 a T1 2028.",
 "Quatre logements neufs restants sur 48 en bord de mer à Estepona : appartements à partir de 3 500 000 € et une villa en front de mer à 12 750 000 €, livraison T4 2027 à T1 2028.",
 "Vier von 48 Neubauwohnungen an der Küste von Estepona verfügbar: Wohnungen ab 3.500.000 € und eine Villa in erster Strandlinie für 12.750.000 €, Fertigstellung Q4 2027 bis Q1 2028.",
 "Осталось четыре из 48 новых домов на побережье Эстепоны: квартиры от 3 500 000 € и вилла на первой линии за 12 750 000 €, сдача с 4 кв. 2027 по 1 кв. 2028.",
 "أربعة من أصل 48 مسكناً جديداً متبقية على واجهة إستيبونا البحرية: شقق ابتداءً من 3,500,000 € وفيلا على الشاطئ بـ 12,750,000 €، التسليم من الربع الرابع 2027 إلى الربع الأول 2028.",
 "Nog vier van de 48 nieuwbouwwoningen aan de kust van Estepona: appartementen vanaf € 3.500.000 en een villa aan het strand voor € 12.750.000, oplevering K4 2027 tot K1 2028.",
 "Zostały cztery z 48 nowych domów na nabrzeżu Estepony: mieszkania od 3 500 000 € i willa przy plaży za 12 750 000 €, odbiór od IV kw. 2027 do I kw. 2028.",
 "Fire av 48 nye boliger igjen ved sjøkanten i Estepona: leiligheter fra 3 500 000 € og en villa i strandkanten til 12 750 000 €, ferdigstilling K4 2027 til K1 2028.",
 "Fyra av 48 nybyggda bostäder kvar vid Esteponas strandkant: lägenheter från 3 500 000 € och en villa i strandkanten för 12 750 000 €, färdigställande K4 2027 till K1 2028.")

a("Four homes left of 48 on the Estepona beachfront, with a spa, a gym and a padel court.",
 "Quedan cuatro viviendas de 48 en primera línea de playa de Estepona, con spa, gimnasio y pista de pádel.",
 "Quatre logements restants sur 48 en front de mer à Estepona, avec spa, salle de sport et terrain de padel.",
 "Vier von 48 Wohnungen an der Strandpromenade von Estepona sind noch frei, mit Spa, Fitnessraum und Padelplatz.",
 "Осталось четыре из 48 домов на первой линии в Эстепоне: спа, спортзал и падел-корт.",
 "أربعة مساكن متبقية من أصل 48 على واجهة إستيبونا البحرية، مع سبا وصالة رياضة وملعب بادل.",
 "Nog vier van de 48 woningen aan de kustlijn van Estepona, met spa, fitnessruimte en padelbaan.",
 "Zostały cztery z 48 domów przy plaży w Esteponie, ze spa, siłownią i kortem do padla.",
 "Fire av 48 boliger igjen i strandkanten i Estepona, med spa, treningsrom og padelbane.",
 "Fyra av 48 bostäder kvar i strandkanten i Estepona, med spa, gym och padelbana.")

a("Forty-eight homes, <em>four left</em>","Cuarenta y ocho viviendas, <em>quedan cuatro</em>","Quarante-huit logements, <em>quatre restants</em>","Achtundvierzig Wohnungen, <em>vier frei</em>","Сорок восемь домов, <em>четыре свободны</em>","ثمانية وأربعون مسكناً، <em>أربعة متبقية</em>","Achtenveertig woningen, <em>vier over</em>","Czterdzieści osiem domów, <em>zostały cztery</em>","Førtiåtte boliger, <em>fire igjen</em>","Fyrtioåtta bostäder, <em>fyra kvar</em>")

a("A gated scheme on a 33,346 sqm beachfront plot at Playa del Ángel, between Estepona and the New Golden Mile.",
 "Una promoción cerrada sobre una parcela de 33.346 m² en primera línea de playa en Playa del Ángel, entre Estepona y la Nueva Milla de Oro.",
 "Un programme fermé sur une parcelle de 33 346 m² en front de mer à Playa del Ángel, entre Estepona et la Nouvelle Mille d'Or.",
 "Eine geschlossene Anlage auf einem 33.346 m² großen Strandgrundstück an der Playa del Ángel, zwischen Estepona und der Neuen Goldenen Meile.",
 "Закрытый комплекс на участке 33 346 м² на первой линии в Плая-дель-Анхель, между Эстепоной и Новой Золотой милей.",
 "مجمّع مغلق على قطعة أرض بمساحة 33,346 م² على الواجهة البحرية في بلايا ديل أنخيل، بين إستيبونا والميل الذهبي الجديد.",
 "Een gesloten project op een strandperceel van 33.346 m² aan Playa del Ángel, tussen Estepona en de Nieuwe Gouden Mijl.",
 "Zamknięta inwestycja na działce 33 346 m² przy plaży w Playa del Ángel, między Esteponą a Nową Złotą Milą.",
 "Et portert prosjekt på en strandtomt på 33 346 m² ved Playa del Ángel, mellom Estepona og Den nye gylne mil.",
 "Ett grindat projekt på en strandtomt om 33 346 m² vid Playa del Ángel, mellan Estepona och Nya Golden Mile.")

a("Six seafront villas stand at the front. Behind them, five three-storey buildings hold 42 apartments and penthouses, every one turned to the sea. All vehicle circulation is underground.",
 "Seis villas frente al mar ocupan el frente. Detrás, cinco edificios de tres plantas albergan 42 apartamentos y áticos, todos orientados al mar. Toda la circulación de vehículos es subterránea.",
 "Six villas en front de mer occupent la première ligne. Derrière, cinq immeubles de trois étages abritent 42 appartements et penthouses, tous tournés vers la mer. Toute la circulation des véhicules est souterraine.",
 "Sechs Villen stehen in erster Reihe am Meer. Dahinter beherbergen fünf dreigeschossige Gebäude 42 Wohnungen und Penthäuser, alle zum Meer ausgerichtet. Der gesamte Fahrzeugverkehr verläuft unterirdisch.",
 "Шесть вилл стоят у самого моря. За ними в пяти трёхэтажных зданиях расположены 42 квартиры и пентхауса, все обращены к морю. Всё движение автомобилей — под землёй.",
 "ست فيلات تتصدّر الواجهة البحرية. خلفها خمسة مبانٍ من ثلاثة طوابق تضم 42 شقة وبنتهاوس، جميعها موجّهة نحو البحر. وحركة السيارات كلها تحت الأرض.",
 "Zes villa's aan zee staan vooraan. Daarachter bevatten vijf gebouwen van drie lagen 42 appartementen en penthouses, alle naar de zee gericht. Al het autoverkeer loopt ondergronds.",
 "Sześć willi stoi w pierwszej linii przy morzu. Za nimi pięć trzykondygnacyjnych budynków mieści 42 mieszkania i penthouse'y, wszystkie zwrócone ku morzu. Cały ruch samochodowy odbywa się pod ziemią.",
 "Seks villaer ligger i første rekke mot sjøen. Bak dem rommer fem bygninger i tre etasjer 42 leiligheter og toppleiligheter, alle vendt mot sjøen. All bilkjøring foregår under bakken.",
 "Sex villor ligger längst fram mot havet. Bakom dem rymmer fem trevåningshus 42 lägenheter och takvåningar, alla vända mot havet. All biltrafik går under mark.")

a("Three apartment types and two villa layouts.","Tres tipos de apartamento y dos distribuciones de villa.","Trois types d'appartements et deux plans de villa.","Drei Wohnungstypen und zwei Villengrundrisse.","Три типа квартир и две планировки вилл.","ثلاثة أنماط من الشقق ومخططان للفيلات.","Drie appartementstypes en twee villaplattegronden.","Trzy typy mieszkań i dwa układy willi.","Tre leilighetstyper og to villaplanløsninger.","Tre lägenhetstyper och två villaplanlösningar.")

a("Four types across the five blocks: duplex ground floor, middle floor, duplex penthouse and prime duplex penthouse.",
 "Cuatro tipologías en los cinco bloques: dúplex en planta baja, planta intermedia, ático dúplex y ático dúplex prime.",
 "Quatre typologies dans les cinq immeubles : duplex en rez-de-chaussée, étage intermédiaire, penthouse duplex et penthouse duplex prime.",
 "Vier Typen in den fünf Baukörpern: Maisonette im Erdgeschoss, Mittelgeschoss, Duplex-Penthouse und Prime-Duplex-Penthouse.",
 "Четыре типа в пяти корпусах: дуплекс на первом этаже, средний этаж, дуплекс-пентхаус и премиальный дуплекс-пентхаус.",
 "أربعة أنماط في المباني الخمسة: دوبلكس في الطابق الأرضي، وطابق متوسط، وبنتهاوس دوبلكس، وبنتهاوس دوبلكس بريم.",
 "Vier types in de vijf blokken: duplex op de begane grond, tussenverdieping, duplexpenthouse en prime duplexpenthouse.",
 "Cztery typy w pięciu budynkach: dupleks na parterze, piętro pośrednie, penthouse dwupoziomowy i penthouse dwupoziomowy prime.",
 "Fire typer i de fem bygningene: duplex i første etasje, mellometasje, duplex-toppleilighet og prime duplex-toppleilighet.",
 "Fyra typer i de fem huskropparna: duplex på bottenvåningen, mellanvåning, duplex-takvåning och prime duplex-takvåning.")

a("Two to five bedrooms, each home oriented to the sea.","De dos a cinco dormitorios, con todas las viviendas orientadas al mar.","De deux à cinq chambres, chaque logement orienté vers la mer.","Zwei bis fünf Schlafzimmer, jede Wohnung zum Meer ausgerichtet.","От двух до пяти спален, каждая квартира обращена к морю.","من غرفتَي نوم إلى خمس، وكل مسكن موجّه نحو البحر.","Twee tot vijf slaapkamers, elke woning op de zee gericht.","Od dwóch do pięciu sypialni, każde mieszkanie zwrócone ku morzu.","To til fem soverom, hver bolig vendt mot sjøen.","Två till fem sovrum, varje bostad vänd mot havet.")
a("Open-plan living rooms that run out onto deep terraces.","Salones diáfanos que se prolongan en terrazas profundas.","Des séjours ouverts qui se prolongent sur de vastes terrasses.","Offene Wohnräume, die sich auf tiefe Terrassen fortsetzen.","Гостиные открытой планировки, переходящие в глубокие террасы.","غرف معيشة مفتوحة تمتد إلى تراسات عميقة.","Open woonkamers die overgaan in diepe terrassen.","Otwarte salony przechodzące w głębokie tarasy.","Åpne stuer som går ut på dype terrasser.","Öppna vardagsrum som fortsätter ut på djupa terrasser.")
a("Ground-floor homes are screened from the communal areas for privacy.","Las viviendas en planta baja quedan resguardadas de las zonas comunes para preservar la intimidad.","Les logements en rez-de-chaussée sont protégés des parties communes pour préserver l'intimité.","Die Erdgeschosswohnungen sind zur Wahrung der Privatsphäre von den Gemeinschaftsflächen abgeschirmt.","Квартиры на первом этаже отгорожены от общих зон ради приватности.","المساكن في الطابق الأرضي محجوبة عن المساحات المشتركة حفاظاً على الخصوصية.","De woningen op de begane grond zijn afgeschermd van de gemeenschappelijke ruimten voor privacy.","Mieszkania na parterze są osłonięte od stref wspólnych dla zachowania prywatności.","Boligene i første etasje er skjermet fra fellesarealene av hensyn til privatlivet.","Bostäderna på bottenvåningen är avskärmade från de gemensamma ytorna för avskildhet.")
a("Six villas on the seafront, in two layouts across three floors with a lift.","Seis villas en primera línea, en dos distribuciones sobre tres plantas con ascensor.","Six villas en front de mer, en deux plans sur trois niveaux avec ascenseur.","Sechs Villen in erster Strandlinie, in zwei Grundrissen über drei Ebenen mit Aufzug.","Шесть вилл на первой линии, в двух планировках на трёх уровнях с лифтом.","ست فيلات على الواجهة البحرية، بمخططين على ثلاثة طوابق مع مصعد.","Zes villa's aan zee, in twee plattegronden over drie verdiepingen met lift.","Sześć willi w pierwszej linii, w dwóch układach na trzech kondygnacjach z windą.","Seks villaer i strandkanten, i to planløsninger over tre etasjer med heis.","Sex villor i strandkanten, i två planlösningar över tre plan med hiss.")
a("Private pool, garden and landscaped roof.","Piscina privada, jardín y cubierta ajardinada.","Piscine privative, jardin et toiture végétalisée.","Eigener Pool, Garten und begrüntes Dach.","Собственный бассейн, сад и озеленённая кровля.","مسبح خاص وحديقة وسطح مزروع.","Privézwembad, tuin en groen dak.","Prywatny basen, ogród i zazieleniony dach.","Privat basseng, hage og beplantet tak.","Privat pool, trädgård och planterat tak.")
a("A basement with an indoor pool, spa, sauna, hammam, cinema room, gym and parking for three cars.","Un sótano con piscina interior, spa, sauna, hammam, sala de cine, gimnasio y aparcamiento para tres coches.","Un sous-sol avec piscine intérieure, spa, sauna, hammam, salle de cinéma, salle de sport et parking pour trois voitures.","Ein Untergeschoss mit Innenpool, Spa, Sauna, Hammam, Kinoraum, Fitnessraum und Stellplätzen für drei Autos.","Цокольный этаж с крытым бассейном, спа, сауной, хаммамом, кинозалом, спортзалом и парковкой на три машины.","طابق سفلي بمسبح داخلي وسبا وساونا وحمّام وغرفة سينما وصالة رياضة ومواقف لثلاث سيارات.","Een kelderverdieping met binnenzwembad, spa, sauna, hammam, bioscoopruimte, fitnessruimte en parkeerplaats voor drie auto's.","Podziemna kondygnacja z basenem wewnętrznym, spa, sauną, hammamem, salą kinową, siłownią i miejscem dla trzech samochodów.","En kjelleretasje med innendørsbasseng, spa, badstue, hammam, kinorom, treningsrom og parkering til tre biler.","Ett källarplan med inomhuspool, spa, bastu, hammam, biosalong, gym och plats för tre bilar.")
a("Direct private access to the communal spa.","Acceso privado directo al spa comunitario.","Accès privatif direct au spa commun.","Direkter privater Zugang zum Gemeinschafts-Spa.","Прямой приватный выход в общий спа.","دخول خاص مباشر إلى السبا المشترك.","Directe privétoegang tot de gemeenschappelijke spa.","Bezpośrednie prywatne wejście do spa wspólnego.","Direkte privat adkomst til fellesspaet.","Direkt privat entré till det gemensamma spat.")

a("4 of 48 homes <em>available</em>","4 de 48 viviendas <em>disponibles</em>","4 logements sur 48 <em>disponibles</em>","4 von 48 Wohnungen <em>verfügbar</em>","4 из 48 домов <em>доступно</em>","4 من 48 مسكناً <em>متاحة</em>","4 van de 48 woningen <em>beschikbaar</em>","4 z 48 domów <em>dostępne</em>","4 av 48 boliger <em>ledige</em>","4 av 48 bostäder <em>lediga</em>")

a("Three apartments and one of the six seafront villas remain. Nueva Living reconfirms price and availability before any viewing or reservation.",
 "Quedan tres apartamentos y una de las seis villas frente al mar. Nueva Living vuelve a confirmar precio y disponibilidad antes de cualquier visita o reserva.",
 "Il reste trois appartements et l'une des six villas face à la mer. Nueva Living reconfirme le prix et la disponibilité avant toute visite ou réservation.",
 "Drei Wohnungen und eine der sechs Villen am Meer sind noch frei. Nueva Living bestätigt Preis und Verfügbarkeit vor jeder Besichtigung oder Reservierung erneut.",
 "Остаются три квартиры и одна из шести вилл у моря. Nueva Living заново подтверждает цену и наличие перед любым просмотром или бронированием.",
 "تبقّى ثلاث شقق وواحدة من الفيلات الست المطلّة على البحر. تعيد Nueva Living تأكيد السعر والتوافر قبل أي معاينة أو حجز.",
 "Er resteren drie appartementen en een van de zes villa's aan zee. Nueva Living bevestigt prijs en beschikbaarheid opnieuw voor elke bezichtiging of reservering.",
 "Pozostają trzy mieszkania i jedna z sześciu willi nad morzem. Nueva Living ponownie potwierdza cenę i dostępność przed każdą prezentacją lub rezerwacją.",
 "Det er igjen tre leiligheter og en av de seks villaene ved sjøen. Nueva Living bekrefter pris og tilgjengelighet på nytt før enhver visning eller reservasjon.",
 "Kvar finns tre lägenheter och en av de sex villorna vid havet. Nueva Living bekräftar pris och tillgänglighet på nytt före varje visning eller reservation.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
