# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 7: lifestyle panels, project file, timeline.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Outside","En el exterior","À l'extérieur","Draußen","Снаружи","في الخارج","Buiten","Na zewnątrz","Ute","Ute")
a("Inside","En el interior","À l'intérieur","Drinnen","Внутри","في الداخل","Binnen","W środku","Inne","Inne")
a("Working","Para trabajar","Pour travailler","Zum Arbeiten","Для работы","للعمل","Werken","Do pracy","Til arbeid","För arbete")

a("An infinity pool on the terrace with the coast beyond the edge, a pool bar alongside it, and landscaped gardens between the blocks. The pools are salt chlorinated rather than chemically dosed.",
 "Una piscina infinita en la terraza con la costa al otro lado del borde, un bar de piscina al lado y jardines entre los bloques. Las piscinas llevan cloración salina en lugar de dosificación química.",
 "Une piscine à débordement sur la terrasse avec la côte au-delà du bord, un bar de piscine attenant et des jardins entre les blocs. Les bassins sont traités par électrolyse au sel plutôt que par dosage chimique.",
 "Ein Infinity-Pool auf der Terrasse mit der Küste jenseits der Kante, eine Poolbar daneben und Gartenanlagen zwischen den Blöcken. Die Becken werden mit Salzelektrolyse statt mit Chemie aufbereitet.",
 "Бассейн-инфинити на террасе с побережьем за краем, бар у бассейна рядом и озеленённые сады между корпусами. Бассейны на солевом хлорировании, а не на химической дозировке.",
 "مسبح لا متناهٍ على التراس والساحل خلف حافّته، وبار مسبح إلى جانبه، وحدائق منسّقة بين المباني. تُعالَج المسابح بالكلورة الملحية بدل الجرعات الكيميائية.",
 "Een infinityzwembad op het terras met de kust voorbij de rand, een poolbar ernaast en aangelegde tuinen tussen de blokken. De baden werken met zoutelektrolyse in plaats van chemische dosering.",
 "Basen infinity na tarasie z wybrzeżem za krawędzią, bar przy basenie obok i ogrody między budynkami. Baseny są chlorowane solą, a nie dozowane chemicznie.",
 "Et infinity-basseng på terrassen med kysten bak kanten, en poolbar ved siden av og opparbeidede hager mellom blokkene. Bassengene bruker saltklorering i stedet for kjemisk dosering.",
 "En infinitypool på terrassen med kusten bortom kanten, en poolbar bredvid och anlagda trädgårdar mellan huskropparna. Poolerna saltkloreras i stället för att doseras kemiskt.")

a("A heated indoor lap pool for swimming lengths, a spa with a Turkish bath, and a gym glazed to the hillside.",
 "Una piscina de nado climatizada y cubierta para hacer largos, un spa con baño turco y un gimnasio acristalado hacia la ladera.",
 "Un bassin de nage intérieur chauffé pour faire des longueurs, un spa avec hammam et une salle de sport vitrée vers le coteau.",
 "Ein beheizter Innen-Schwimmkanal für Bahnen, ein Spa mit Dampfbad und ein zum Hang verglaster Fitnessraum.",
 "Крытый подогреваемый бассейн для плавания дорожек, спа с турецкой баней и спортзал, застеклённый в сторону склона.",
 "مسبح داخلي مُدفأ للسباحة الطولية، وسبا بحمّام تركي، وصالة رياضة مزجّجة نحو المنحدر.",
 "Een verwarmd binnenbaanzwembad om baantjes te trekken, een spa met Turks bad en een naar de helling beglaasde fitnessruimte.",
 "Kryty podgrzewany basen pływacki do pokonywania długości, spa z łaźnią turecką i siłownia przeszklona w stronę zbocza.",
 "Et oppvarmet innendørs svømmebasseng for å ta lengder, et spa med tyrkisk bad og et treningsrom med glassvegg mot skråningen.",
 "En uppvärmd inomhusbassäng för att simma längder, ett spa med turkiskt bad och ett gym med glasvägg mot sluttningen.")

a("A coworking room sharing its floor with a social lounge, for the weeks when the second home has to be an office as well.",
 "Una sala de coworking que comparte planta con un salón social, para las semanas en que la segunda residencia tiene que ser también oficina.",
 "Un espace de coworking partageant son étage avec un salon commun, pour les semaines où la résidence secondaire doit aussi servir de bureau.",
 "Ein Coworking-Raum, der sich die Ebene mit einem Gemeinschaftsraum teilt, für die Wochen, in denen der Zweitwohnsitz auch Büro sein muss.",
 "Коворкинг, делящий этаж с общей гостиной, — для тех недель, когда второй дом должен быть ещё и офисом.",
 "غرفة عمل مشترك تتقاسم الطابق مع صالة اجتماعية، للأسابيع التي يتعيّن فيها أن يكون المنزل الثاني مكتباً أيضاً.",
 "Een coworkingruimte die de verdieping deelt met een gemeenschappelijke lounge, voor de weken waarin het tweede huis ook kantoor moet zijn.",
 "Sala coworkingowa dzieląca piętro z salonem wspólnym, na tygodnie, gdy drugi dom musi być również biurem.",
 "Et coworking-rom som deler etasje med en fellesstue, for ukene da bolig nummer to også må være kontor.",
 "Ett coworkingrum som delar plan med ett gemensamhetsrum, för de veckor då andrabostaden också måste vara kontor.")

a("Price list","Lista de precios","Liste de prix","Preisliste","Прайс-лист","قائمة الأسعار","Prijslijst","Cennik","Prisliste","Prislista")

a("The seller's own list dated 17 September 2026, with every released home, its areas and its price before tax.",
 "La lista del propio vendedor con fecha 17 de septiembre de 2026, con cada vivienda puesta a la venta, sus superficies y su precio antes de impuestos.",
 "La liste du vendeur lui-même datée du 17 septembre 2026, avec chaque logement mis en vente, ses surfaces et son prix hors taxes.",
 "Die Liste des Verkäufers selbst vom 17. September 2026, mit jeder freigegebenen Wohnung, ihren Flächen und ihrem Preis vor Steuern.",
 "Список самого продавца от 17 сентября 2026 года: каждая выведенная в продажу квартира, её площади и цена без налогов.",
 "قائمة البائع نفسه المؤرخة 17 سبتمبر 2026، بكل مسكن مطروح ومساحاته وسعره قبل الضريبة.",
 "De eigen lijst van de verkoper van 17 september 2026, met elke vrijgegeven woning, haar oppervlakken en haar prijs voor belasting.",
 "Własna lista sprzedającego z 17 września 2026 roku, z każdym wprowadzonym do sprzedaży mieszkaniem, jego powierzchniami i ceną przed podatkiem.",
 "Selgerens egen liste datert 17. september 2026, med hver bolig som er lagt ut, arealene og prisen før skatt.",
 "Säljarens egen lista daterad 17 september 2026, med varje släppt bostad, dess ytor och dess pris före skatt.")

a("Quality specification","Memoria de calidades","Descriptif des prestations","Baubeschreibung",
 "Спецификация качества","مواصفات الجودة","Technische omschrijving","Standard wykończenia","Kvalitetsbeskrivelse","Kvalitetsbeskrivning")

a("The full written specification dated 24 March 2025, from the foundations to the appliances.",
 "La memoria completa por escrito con fecha 24 de marzo de 2025, desde la cimentación hasta los electrodomésticos.",
 "Le descriptif écrit complet daté du 24 mars 2025, des fondations jusqu'à l'électroménager.",
 "Die vollständige schriftliche Beschreibung vom 24. März 2025, vom Fundament bis zu den Geräten.",
 "Полная письменная спецификация от 24 марта 2025 года — от фундамента до бытовой техники.",
 "المواصفات المكتوبة الكاملة بتاريخ 24 مارس 2025، من الأساسات إلى الأجهزة.",
 "De volledige schriftelijke omschrijving van 24 maart 2025, van de fundering tot de apparatuur.",
 "Pełny opis pisemny z 24 marca 2025 roku, od fundamentów po sprzęt AGD.",
 "Den fullstendige skriftlige beskrivelsen datert 24. mars 2025, fra fundamentet til hvitevarene.",
 "Den fullständiga skriftliga beskrivningen daterad 24 mars 2025, från grunden till vitvarorna.")

a("Payment schedule","Calendario de pagos","Échéancier de paiement","Zahlungsplan","График платежей",
 "جدول السداد","Betalingsschema","Harmonogram płatności","Betalingsplan","Betalningsplan")

a("The developer's five-stage schedule with the reservation figure and the VAT on each instalment.",
 "El calendario de cinco fases del promotor, con el importe de reserva y el IVA de cada plazo.",
 "L'échéancier en cinq étapes du promoteur, avec le montant de la réservation et la TVA sur chaque versement.",
 "Der fünfstufige Zahlungsplan des Bauträgers mit dem Reservierungsbetrag und der Mehrwertsteuer je Rate.",
 "Пятиэтапный график застройщика с суммой брони и НДС по каждому платежу.",
 "جدول المطوّر ذو المراحل الخمس مع مبلغ الحجز وضريبة القيمة المضافة على كل قسط.",
 "Het vijfstappenschema van de ontwikkelaar met het reserveringsbedrag en de btw per termijn.",
 "Pięcioetapowy harmonogram dewelopera z kwotą rezerwacji i VAT-em od każdej raty.",
 "Utbyggerens femtrinnsplan med reservasjonsbeløpet og merverdiavgiften på hvert avdrag.",
 "Byggherrens femstegsplan med bokningsbeloppet och momsen på varje delbetalning.")

a("Floorplans","Planos","Plans","Grundrisse","Планировки","المخططات","Plattegronden","Rzuty","Plantegninger","Planritningar")

a("Eleven of the twelve available homes, in English and Spanish. The seller has not issued one for 71B.",
 "Once de las doce viviendas disponibles, en inglés y español. El vendedor no ha emitido el del 71B.",
 "Onze des douze logements disponibles, en anglais et en espagnol. Le vendeur n'a pas fourni celui du 71B.",
 "Elf der zwölf verfügbaren Wohnungen, auf Englisch und Spanisch. Für 71B hat der Verkäufer keinen herausgegeben.",
 "Одиннадцать из двенадцати доступных квартир, на английском и испанском. Для 71B продавец ничего не выпустил.",
 "أحد عشر من المساكن الاثني عشر المتاحة، بالإنجليزية والإسبانية. ولم يصدر البائع مخططاً للوحدة 71B.",
 "Elf van de twaalf beschikbare woningen, in het Engels en Spaans. Voor 71B heeft de verkoper er geen uitgegeven.",
 "Jedenaście z dwunastu dostępnych mieszkań, po angielsku i hiszpańsku. Dla 71B sprzedający nie wydał żadnego.",
 "Elleve av de tolv ledige boligene, på engelsk og spansk. For 71B har selgeren ikke utstedt noen.",
 "Elva av de tolv lediga bostäderna, på engelska och spanska. För 71B har säljaren inte utfärdat någon.")

a("You tell us what you are after","Usted nos dice qué busca","Vous nous dites ce que vous cherchez","Sie sagen uns, was Sie suchen",
 "Вы говорите, что ищете","تخبرنا بما تبحث عنه","U vertelt ons wat u zoekt","Mówią nam Państwo, czego szukają",
 "Du forteller oss hva du er ute etter","Ni berättar vad ni söker")

a("Which block, which floor, how many bedrooms, and what you want the terrace to do.",
 "Qué bloque, qué planta, cuántos dormitorios y qué quiere que la terraza le dé.",
 "Quel bloc, quel étage, combien de chambres, et ce que vous attendez de la terrasse.",
 "Welcher Block, welches Geschoss, wie viele Schlafzimmer und was die Terrasse leisten soll.",
 "Какой корпус, какой этаж, сколько спален и что вы хотите от террасы.",
 "أي مبنى وأي طابق وكم غرفة نوم وما الذي تريده من التراس.",
 "Welk blok, welke verdieping, hoeveel slaapkamers en wat het terras moet kunnen.",
 "Który budynek, które piętro, ile sypialni i czego Państwo oczekują od tarasu.",
 "Hvilken blokk, hvilken etasje, hvor mange soverom, og hva du vil at terrassen skal gjøre.",
 "Vilken huskropp, vilket våningsplan, hur många sovrum och vad ni vill att terrassen ska göra.")

a("We come back with the current list","Le respondemos con la lista actual","Nous revenons avec la liste actuelle",
 "Wir melden uns mit der aktuellen Liste","Мы возвращаемся с актуальным списком","نعود إليك بالقائمة الحالية",
 "Wij komen terug met de actuele lijst","Wracamy z aktualną listą","Vi kommer tilbake med den aktuelle listen","Vi återkommer med den aktuella listan")

a("Reconfirmed with the seller, with the tax added so you see the real number.",
 "Reconfirmada con el vendedor y con los impuestos sumados, para que vea la cifra real.",
 "Reconfirmée auprès du vendeur, taxes comprises, pour que vous voyiez le vrai chiffre.",
 "Beim Verkäufer bestätigt und mit aufgeschlagenen Steuern, damit Sie die echte Zahl sehen.",
 "Подтверждённым у продавца и с добавленными налогами, чтобы вы видели настоящую цифру.",
 "بعد إعادة تأكيدها مع البائع ومع إضافة الضرائب لترى الرقم الحقيقي.",
 "Opnieuw bevestigd bij de verkoper en met belasting erbij, zodat u het echte bedrag ziet.",
 "Potwierdzoną ponownie u sprzedającego i z doliczonym podatkiem, aby widzieli Państwo prawdziwą kwotę.",
 "Bekreftet på nytt med selgeren, med skatten lagt til så du ser det reelle tallet.",
 "Bekräftad på nytt med säljaren, med skatten pålagd så att ni ser den verkliga siffran.")

a("We walk the site with you","Recorremos la promoción con usted","Nous parcourons le site avec vous","Wir gehen das Gelände mit Ihnen ab",
 "Мы обходим площадку вместе с вами","نتجوّل في الموقع معك","Wij lopen het terrein met u door",
 "Obchodzimy z Państwem teren","Vi går over tomta sammen med deg","Vi går platsen tillsammans med er")

a("And ask the questions about the licence, the guarantee and the delivery date in front of you.",
 "Y hacemos delante de usted las preguntas sobre la licencia, el aval y la fecha de entrega.",
 "Et posons devant vous les questions sur le permis, la garantie et la date de livraison.",
 "Und stellen in Ihrem Beisein die Fragen zu Genehmigung, Bürgschaft und Übergabetermin.",
 "И задаём вопросы о разрешении, гарантии и дате передачи в вашем присутствии.",
 "ونطرح أمامك الأسئلة عن الرخصة والكفالة وتاريخ التسليم.",
 "En stellen in uw bijzijn de vragen over de vergunning, de garantie en de opleverdatum.",
 "I zadajemy w Państwa obecności pytania o pozwolenie, gwarancję i datę odbioru.",
 "Og stiller spørsmålene om tillatelsen, garantien og overtakelsesdatoen mens du hører på.",
 "Och ställer frågorna om bygglovet, garantin och tillträdesdatumet inför er.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
