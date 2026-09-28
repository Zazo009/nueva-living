# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Ten apartments: seven with two bedrooms and three with three, across three blocks.",
 "Diez apartamentos: siete de dos dormitorios y tres de tres, repartidos en tres bloques.",
 "Dix appartements : sept de deux chambres et trois de trois, répartis sur trois immeubles.",
 "Zehn Wohnungen: sieben mit zwei und drei mit drei Schlafzimmern, verteilt auf drei Gebäude.",
 "Десять квартир: семь с двумя спальнями и три с тремя, в трёх корпусах.",
 "عشر شقق: سبع بغرفتي نوم وثلاث بثلاث غرف، موزعة على ثلاثة مبانٍ.",
 "Tien appartementen: zeven met twee slaapkamers en drie met drie, verdeeld over drie gebouwen.",
 "Dziesięć apartamentów: siedem z dwiema sypialniami i trzy z trzema, w trzech budynkach.",
 "Ti leiligheter: sju med to soverom og tre med tre, fordelt på tre bygg.",
 "Tio lägenheter: sju med två sovrum och tre med tre, fördelade på tre hus.")
a("What do they cost?","¿Cuánto cuestan?","Combien coûtent-ils ?","Was kosten sie?","Сколько они стоят?",
 "كم تكلف؟","Wat kosten ze?","Ile kosztują?","Hva koster de?","Vad kostar de?")
a("From EUR 376,000 to EUR 550,000, excluding VAT and the other purchase costs.",
 "De 376.000 € a 550.000 €, sin incluir el IVA ni los demás gastos de compra.",
 "De 376 000 € à 550 000 €, hors TVA et autres frais d'acquisition.",
 "Von 376.000 € bis 550.000 €, ohne Mehrwertsteuer und die übrigen Kaufnebenkosten.",
 "От 376 000 € до 550 000 €, без НДС и прочих расходов на покупку.",
 "من 376,000 € إلى 550,000 €، دون ضريبة القيمة المضافة وباقي تكاليف الشراء.",
 "Van € 376.000 tot € 550.000, exclusief btw en de overige aankoopkosten.",
 "Od 376 000 € do 550 000 €, bez VAT i pozostałych kosztów zakupu.",
 "Fra 376 000 € til 550 000 €, uten merverdiavgift og de øvrige kjøpsomkostningene.",
 "Från 376 000 € till 550 000 €, exklusive moms och övriga köpkostnader.")
a("How big are they?","¿Qué superficie tienen?","Quelle est leur surface ?","Wie groß sind sie?",
 "Какая у них площадь?","ما مساحتها؟","Hoe groot zijn ze?","Jak duże są?","Hvor store er de?","Hur stora är de?")
a("From 92.81 to 136.53 sqm built among the homes available now, with terraces from 15.32 to 36.74 sqm.",
 "De 92,81 a 136,53 m² construidos entre las viviendas disponibles ahora, con terrazas de 15,32 a 36,74 m².",
 "De 92,81 à 136,53 m² construits parmi les logements disponibles, avec des terrasses de 15,32 à 36,74 m².",
 "Von 92,81 bis 136,53 m² Wohnfläche bei den derzeit verfügbaren Wohnungen, mit Terrassen von 15,32 bis 36,74 m².",
 "От 92,81 до 136,53 м² построенной площади среди доступных сейчас квартир, с террасами от 15,32 до 36,74 м².",
 "من 92.81 إلى 136.53 م² مبنية بين المنازل المتاحة حالياً، مع شرفات من 15.32 إلى 36.74 م².",
 "Van 92,81 tot 136,53 m² bouwoppervlak bij de nu beschikbare woningen, met terrassen van 15,32 tot 36,74 m².",
 "Od 92,81 do 136,53 m² powierzchni zabudowanej wśród dostępnych obecnie mieszkań, z tarasami od 15,32 do 36,74 m².",
 "Fra 92,81 til 136,53 m² bygget blant boligene som er tilgjengelige nå, med terrasser fra 15,32 til 36,74 m².",
 "Från 92,81 till 136,53 m² byggyta bland de bostäder som är tillgängliga nu, med terrasser från 15,32 till 36,74 m².")
a("Completion is given as the third quarter of 2029.","La entrega está indicada para el tercer trimestre de 2029.",
 "La livraison est annoncée pour le troisième trimestre 2029.","Die Fertigstellung ist für das dritte Quartal 2029 angegeben.",
 "Срок сдачи указан как третий квартал 2029 года.","الإنجاز مذكور في الربع الثالث من عام 2029.",
 "De oplevering is opgegeven voor het derde kwartaal van 2029.","Zakończenie podano na trzeci kwartał 2029 roku.",
 "Ferdigstillelse er oppgitt til tredje kvartal 2029.","Färdigställandet anges till tredje kvartalet 2029.")
a("Yes. Every home comes with a garage space and a storeroom.",
 "Sí. Cada vivienda incluye plaza de garaje y trastero.",
 "Oui. Chaque logement comprend une place de garage et un débarras.",
 "Ja. Zu jeder Wohnung gehören ein Garagenstellplatz und ein Abstellraum.",
 "Да. К каждой квартире прилагаются место в гараже и кладовая.",
 "نعم. كل منزل يشمل موقفاً في المرآب ومخزناً.",
 "Ja. Bij elke woning horen een garageplaats en een berging.",
 "Tak. Do każdego mieszkania należy miejsce w garażu i komórka lokatorska.",
 "Ja. Hver bolig har garasjeplass og bod.","Ja. Varje bostad har garageplats och förråd.")
a("What is there on site?","¿Qué hay en la promoción?","Qu'y a-t-il sur place ?","Was gibt es vor Ort?",
 "Что есть на территории?","ماذا يوجد في الموقع؟","Wat is er op het terrein?","Co jest na terenie?",
 "Hva finnes på området?","Vad finns på området?")
a("Two pools, a gym, beach padel and pickleball courts, a putting green, an outdoor calisthenics area, a walking trail, an events room and a coworking room.",
 "Dos piscinas, gimnasio, pistas de pádel playa y pickleball, putting green, zona de calistenia al aire libre, un sendero, sala de eventos y sala de coworking.",
 "Deux piscines, une salle de sport, des terrains de beach padel et de pickleball, un putting green, une aire de callisthénie en plein air, un sentier, une salle de réception et un espace de coworking.",
 "Zwei Pools, ein Fitnessraum, Beach-Padel- und Pickleball-Plätze, ein Putting Green, ein Calisthenics-Bereich im Freien, ein Wanderweg, ein Veranstaltungsraum und ein Coworking-Raum.",
 "Два бассейна, тренажёрный зал, корты для пляжного паделя и пиклбола, паттинг-грин, площадка для калистеники, тропа, зал для мероприятий и коворкинг.",
 "مسبحان وصالة رياضية وملاعب بادل شاطئي وبيكل بول وملعب بَتّ ومنطقة كاليسثينيكس في الهواء الطلق ومسار للمشي وقاعة مناسبات وغرفة عمل مشترك.",
 "Twee zwembaden, een fitnessruimte, beachpadel- en pickleballbanen, een puttinggreen, een calisthenicsplek in de open lucht, een wandelpad, een evenementenruimte en een coworkingruimte.",
 "Dwa baseny, siłownia, korty do padla plażowego i pickleballa, putting green, plenerowa strefa kalisteniki, ścieżka spacerowa, sala eventowa i sala coworkingowa.",
 "To bassenger, treningsrom, beachpadel- og pickleballbaner, en puttinggreen, et utendørs kalistenikkområde, en tursti, et selskapsrom og et coworking-rom.",
 "Två pooler, gym, beachpadel- och pickleballbanor, en puttinggreen, ett utomhusområde för kalistenik, en gångstig, en festlokal och ett coworking-rum.")
a("The availability list, the specification and the brochure.","La lista de disponibilidad, la memoria de calidades y el folleto.",
 "La liste de disponibilité, le descriptif technique et la brochure.","Die Verfügbarkeitsliste, die Baubeschreibung und die Broschüre.",
 "Список наличия, спецификация и буклет.","قائمة التوافر ومواصفات البناء والكتيّب.",
 "De beschikbaarheidslijst, het lastenboek en de brochure.","Lista dostępności, specyfikacja techniczna i folder.",
 "Tilgjengelighetslisten, beskrivelsen og brosjyren.","Tillgänglighetslistan, byggbeskrivningen och broschyren.")
a("We arrange the appointment and walk the plot with you.","Concertamos la cita y recorremos la parcela con usted.",
 "Nous organisons le rendez-vous et parcourons le terrain avec vous.","Wir vereinbaren den Termin und gehen das Grundstück mit Ihnen ab.",
 "Мы договариваемся о встрече и обходим участок вместе с вами.","نحدد الموعد ونتجول معك في الأرض.",
 "Wij maken de afspraak en lopen het terrein met u door.","Umawiamy wizytę i obchodzimy z Państwem działkę.",
 "Vi avtaler visningen og går tomten sammen med deg.","Vi bokar visningen och går tomten tillsammans med köparen.")
a("Reserve with the checks done","Reservar con las comprobaciones hechas","Réserver une fois les vérifications faites",
 "Reservieren, wenn die Prüfungen erledigt sind","Бронировать после всех проверок","الحجز بعد إتمام الفحوصات",
 "Reserveren met de controles gedaan","Rezerwacja po wykonaniu sprawdzeń","Reservere når sjekkene er gjort","Reservera när kontrollerna är gjorda")
a("Licence, bank guarantee and a contractual date, before any money moves.",
 "Licencia, aval bancario y fecha contractual, antes de que se mueva ningún dinero.",
 "Permis, garantie bancaire et date contractuelle, avant tout mouvement d'argent.",
 "Genehmigung, Bankbürgschaft und ein vertraglicher Termin, bevor Geld fließt.",
 "Разрешение, банковская гарантия и договорная дата — до любых денежных переводов.",
 "الترخيص والضمان البنكي وتاريخ تعاقدي، قبل تحويل أي مبلغ.",
 "Vergunning, bankgarantie en een contractuele datum, voordat er geld wordt overgemaakt.",
 "Pozwolenie, gwarancja bankowa i umowna data, zanim pojawią się jakiekolwiek płatności.",
 "Tillatelse, bankgaranti og en kontraktfestet dato, før noen penger flyttes.",
 "Tillstånd, bankgaranti och ett avtalat datum, innan några pengar flyttas.")
a("Ask about <em>this scheme</em>","Pregunta por <em>esta promoción</em>","Renseignez-vous sur <em>ce programme</em>",
 "Fragen Sie zu <em>dieser Anlage</em>","Спросите об <em>этом комплексе</em>","اسأل عن <em>هذا المشروع</em>",
 "Vraag naar <em>dit project</em>","Zapytaj o <em>tę inwestycję</em>","Spør om <em>dette prosjektet</em>","Fråga om <em>det här projektet</em>")
a("Tell us what you are looking for and we will come back with the current list.",
 "Cuéntenos qué busca y le responderemos con la lista actual.",
 "Dites-nous ce que vous cherchez et nous reviendrons avec la liste actuelle.",
 "Sagen Sie uns, was Sie suchen, und wir melden uns mit der aktuellen Liste.",
 "Расскажите, что вы ищете, и мы вернёмся с актуальным списком.",
 "أخبرنا بما تبحث عنه وسنعود إليك بالقائمة الحالية.",
 "Vertel ons wat u zoekt en wij komen terug met de actuele lijst.",
 "Proszę napisać, czego Państwo szukają, a wrócimy z aktualną listą.",
 "Fortell hva du ser etter, så kommer vi tilbake med den aktuelle listen.",
 "Berätta vad som söks, så återkommer vi med den aktuella listan.")
a("I would like the current availability and prices for the Mijas Pinewood Residences.",
 "Me gustaría recibir la disponibilidad y los precios actuales de Mijas Pinewood Residences.",
 "Je souhaite recevoir la disponibilité et les prix actuels de Mijas Pinewood Residences.",
 "Ich hätte gern die aktuelle Verfügbarkeit und die Preise für Mijas Pinewood Residences.",
 "Хочу получить актуальное наличие и цены по Mijas Pinewood Residences.",
 "أرغب في معرفة التوافر والأسعار الحالية لمشروع Mijas Pinewood Residences.",
 "Ik ontvang graag de actuele beschikbaarheid en prijzen van Mijas Pinewood Residences.",
 "Chciałbym otrzymać aktualną dostępność i ceny dla Mijas Pinewood Residences.",
 "Jeg vil gjerne ha oppdatert tilgjengelighet og priser for Mijas Pinewood Residences.",
 "Jag vill gärna ha aktuell tillgänglighet och priser för Mijas Pinewood Residences.")
a("We reply to every enquiry ourselves.","Respondemos personalmente a cada consulta.","Nous répondons nous-mêmes à chaque demande.",
 "Wir beantworten jede Anfrage selbst.","Мы отвечаем на каждый запрос лично.","نردّ بأنفسنا على كل استفسار.",
 "Wij beantwoorden elke aanvraag zelf.","Na każde zapytanie odpowiadamy osobiście.",
 "Vi svarer selv på hver henvendelse.","Vi svarar själva på varje förfrågan.")
a("Thank you. We will come back to you with the current list.","Gracias. Te responderemos con la lista actual.",
 "Merci. Nous reviendrons vers vous avec la liste actuelle.","Vielen Dank. Wir melden uns mit der aktuellen Liste.",
 "Спасибо. Мы вернёмся к вам с актуальным списком.","شكراً لك. سنعود إليك بالقائمة الحالية.",
 "Dank u. Wij komen bij u terug met de actuele lijst.","Dziękujemy. Wrócimy z aktualną listą.",
 "Takk. Vi kommer tilbake med den aktuelle listen.","Tack. Vi återkommer med den aktuella listan.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
