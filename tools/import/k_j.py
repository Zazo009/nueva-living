# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Floors, areas and prices are transcribed from the seller's own availability list, read on 28 September 2026. Built areas are the developer's constructed figure and include a share of the common parts; the useful area of each home is smaller and is on its floorplan. The list gives no total for the scheme, so the number of homes is not stated here. Prices exclude VAT and the other purchase costs, which are set out in the buying guides.",
 "Plantas, superficies y precios están transcritos de la propia lista de disponibilidad del vendedor, consultada el 28 de septiembre de 2026. Las superficies son la construida del promotor e incluyen una parte proporcional de elementos comunes; la superficie útil de cada vivienda es menor y figura en su plano. La lista no indica un total para la promoción, por lo que aquí no se afirma el número de viviendas. Los precios no incluyen el IVA ni los demás gastos de compra, detallados en las guías de compra.",
 "Étages, surfaces et prix sont transcrits de la liste de disponibilité du vendeur, consultée le 28 septembre 2026. Les surfaces sont la surface construite du promoteur et incluent une quote-part des parties communes ; la surface utile de chaque logement est inférieure et figure sur son plan. La liste ne donne pas de total pour le programme, le nombre de logements n'est donc pas indiqué ici. Les prix s'entendent hors TVA et hors autres frais d'acquisition, détaillés dans les guides d'achat.",
 "Geschosse, Flächen und Preise sind aus der Verfügbarkeitsliste des Verkäufers übernommen, eingesehen am 28. September 2026. Die Flächen sind die Bauträger-Bruttofläche und enthalten einen Anteil am Gemeinschaftseigentum; die Nutzfläche jeder Wohnung ist kleiner und steht im Grundriss. Die Liste nennt keine Gesamtzahl für die Anlage, daher wird hier keine Anzahl der Wohnungen angegeben. Die Preise verstehen sich ohne Mehrwertsteuer und ohne die übrigen Kaufnebenkosten, die in den Kaufratgebern aufgeführt sind.",
 "Этажи, площади и цены перенесены из собственного списка наличия продавца, просмотренного 28 сентября 2026 года. Площади — построенная площадь застройщика и включают долю мест общего пользования; полезная площадь каждой квартиры меньше и указана на её плане. В списке нет общего числа квартир в комплексе, поэтому оно здесь не указывается. Цены не включают НДС и прочие расходы на покупку, которые описаны в руководствах покупателя.",
 "الطوابق والمساحات والأسعار منقولة عن قائمة التوافر الخاصة بالبائع، اطُّلع عليها في 28 سبتمبر 2026. المساحات هي المساحة المبنية للمطور وتشمل حصة من الأجزاء المشتركة، والمساحة المفيدة لكل منزل أقل وتظهر في مخططه. لا تذكر القائمة إجمالياً للمشروع، لذلك لا يُذكر عدد المنازل هنا. الأسعار لا تشمل ضريبة القيمة المضافة ولا باقي تكاليف الشراء الموضحة في أدلة الشراء.",
 "Verdiepingen, oppervlakten en prijzen zijn overgenomen uit de eigen beschikbaarheidslijst van de verkoper, geraadpleegd op 28 september 2026. De oppervlakten zijn de bouwoppervlakte van de ontwikkelaar en omvatten een aandeel in de gemeenschappelijke delen; de nuttige oppervlakte van elke woning is kleiner en staat op de plattegrond. De lijst geeft geen totaal voor het project, dus het aantal woningen wordt hier niet genoemd. Prijzen zijn exclusief btw en de overige aankoopkosten, die in de koopgidsen staan.",
 "Kondygnacje, powierzchnie i ceny przepisano z własnej listy dostępności sprzedającego, sprawdzonej 28 września 2026 roku. Powierzchnie to powierzchnia zabudowana dewelopera i obejmują udział w częściach wspólnych; powierzchnia użytkowa każdego mieszkania jest mniejsza i podana jest na jego rzucie. Lista nie podaje sumy dla inwestycji, dlatego liczby mieszkań tu nie wskazano. Ceny nie zawierają VAT ani pozostałych kosztów zakupu, opisanych w przewodnikach zakupowych.",
 "Etasjer, arealer og priser er hentet fra selgerens egen tilgjengelighetsliste, lest 28. september 2026. Arealene er utbyggerens bruttoareal og inkluderer en andel av fellesarealene; det nyttbare arealet i hver bolig er mindre og står på plantegningen. Listen oppgir ingen totalsum for prosjektet, så antall boliger oppgis ikke her. Prisene er uten merverdiavgift og de øvrige kjøpsomkostningene, som står i kjøpsguidene.",
 "Våningar, ytor och priser är hämtade från säljarens egen tillgänglighetslista, läst den 28 september 2026. Ytorna är utvecklarens byggyta och inkluderar en andel av de gemensamma delarna; varje bostads nyttiga yta är mindre och står på dess planritning. Listan anger ingen totalsumma för projektet, så antalet bostäder anges inte här. Priserna är exklusive moms och övriga köpkostnader, som beskrivs i köpguiderna.")

a("Currently off-plan, with completion given as the third quarter of 2029. Nueva Living asks for the delivery date in writing and puts it in the contract.",
 "Actualmente sobre plano, con entrega indicada para el tercer trimestre de 2029. Nueva Living pide la fecha de entrega por escrito y la lleva al contrato.",
 "Actuellement sur plan, avec une livraison annoncée au troisième trimestre 2029. Nueva Living demande la date de livraison par écrit et l'inscrit au contrat.",
 "Derzeit im Bauträgerverkauf, die Fertigstellung ist für das dritte Quartal 2029 angegeben. Nueva Living lässt sich den Übergabetermin schriftlich geben und nimmt ihn in den Vertrag auf.",
 "Сейчас на стадии проекта, срок сдачи указан как третий квартал 2029 года. Nueva Living запрашивает дату передачи письменно и вносит её в договор.",
 "المشروع حالياً على المخطط، والإنجاز مذكور في الربع الثالث من عام 2029. تطلب Nueva Living تاريخ التسليم كتابةً وتدرجه في العقد.",
 "Momenteel op plan, met oplevering opgegeven voor het derde kwartaal van 2029. Nueva Living vraagt de opleverdatum schriftelijk op en neemt die in het contract op.",
 "Obecnie na etapie przedsprzedaży, z terminem zakończenia podanym na trzeci kwartał 2029 roku. Nueva Living prosi o datę odbioru na piśmie i wpisuje ją do umowy.",
 "For tiden på tegnebrettet, med ferdigstillelse oppgitt til tredje kvartal 2029. Nueva Living ber om overtakelsesdatoen skriftlig og tar den inn i kontrakten.",
 "För närvarande på ritning, med färdigställande angivet till tredje kvartalet 2029. Nueva Living begär tillträdesdatumet skriftligt och för in det i avtalet.")

a("This project suits buyers who want a quiet, green setting in Mijas without giving up the beach or the motorway.",
 "Este proyecto encaja con quienes buscan un entorno tranquilo y verde en Mijas sin renunciar a la playa ni a la autopista.",
 "Ce programme convient aux acquéreurs qui cherchent un cadre calme et vert à Mijas sans renoncer à la plage ni à l'autoroute.",
 "Das Projekt passt zu Käufern, die eine ruhige, grüne Lage in Mijas suchen, ohne auf Strand oder Autobahn zu verzichten.",
 "Проект подходит покупателям, которым нужна тихая зелёная среда в Михасе без отказа от пляжа и автомагистрали.",
 "يناسب هذا المشروع من يبحث عن محيط هادئ وأخضر في ميخاس دون التخلي عن الشاطئ أو الطريق السريع.",
 "Dit project past bij kopers die een rustige, groene omgeving in Mijas willen zonder het strand of de snelweg op te geven.",
 "Ta inwestycja odpowiada osobom szukającym spokojnego, zielonego otoczenia w Mijas bez rezygnacji z plaży i autostrady.",
 "Prosjektet passer kjøpere som vil ha et rolig, grønt miljø i Mijas uten å gi slipp på stranden eller motorveien.",
 "Projektet passar köpare som vill ha en lugn, grön miljö i Mijas utan att ge upp stranden eller motorvägen.")
a("Buyers who want space and greenery within a few minutes of the coast.",
 "Compradores que buscan espacio y verde a pocos minutos de la costa.",
 "Des acquéreurs qui veulent de l'espace et de la verdure à quelques minutes de la côte.",
 "Käufer, die Platz und Grün wenige Minuten von der Küste entfernt suchen.",
 "Покупателям, которым нужны простор и зелень в нескольких минутах от побережья.",
 "من يبحث عن المساحة والخضرة على بعد دقائق من الساحل.",
 "Kopers die ruimte en groen willen op enkele minuten van de kust.",
 "Kupującym, którzy cenią przestrzeń i zieleń kilka minut od wybrzeża.",
 "Kjøpere som ønsker plass og grønt noen minutter fra kysten.",
 "Köpare som vill ha yta och grönska några minuter från kusten.")
a("The communal side is unusually broad for a scheme this size: two pools, a gym, padel, pickleball, a putting green and a coworking room.",
 "Las zonas comunes son inusualmente amplias para una promoción de este tamaño: dos piscinas, gimnasio, pádel, pickleball, putting green y sala de coworking.",
 "Les espaces communs sont inhabituellement vastes pour un programme de cette taille : deux piscines, une salle de sport, du padel, du pickleball, un putting green et un espace de coworking.",
 "Die Gemeinschaftsbereiche sind für eine Anlage dieser Größe ungewöhnlich umfangreich: zwei Pools, ein Fitnessraum, Padel, Pickleball, ein Putting Green und ein Coworking-Raum.",
 "Общие зоны необычно обширны для комплекса такого размера: два бассейна, тренажёрный зал, падел, пиклбол, паттинг-грин и коворкинг.",
 "المساحات المشتركة واسعة بشكل غير معتاد لمشروع بهذا الحجم: مسبحان وصالة رياضية وبادل وبيكل بول وملعب بَتّ وغرفة عمل مشترك.",
 "De gemeenschappelijke voorzieningen zijn ongewoon ruim voor een project van deze omvang: twee zwembaden, een fitnessruimte, padel, pickleball, een puttinggreen en een coworkingruimte.",
 "Część wspólna jest nietypowo rozbudowana jak na inwestycję tej wielkości: dwa baseny, siłownia, padel, pickleball, putting green i sala coworkingowa.",
 "Fellesarealene er uvanlig omfattende for et prosjekt av denne størrelsen: to bassenger, treningsrom, padel, pickleball, en puttinggreen og et coworking-rom.",
 "De gemensamma ytorna är ovanligt omfattande för ett projekt av den här storleken: två pooler, gym, padel, pickleball, en puttinggreen och ett coworking-rum.")
a("Mijas between La Cala and Fuengirola keeps the beaches and the A-7 close while staying above the coast road.",
 "Mijas, entre La Cala y Fuengirola, mantiene cerca las playas y la A-7 sin estar en la carretera de la costa.",
 "Mijas, entre La Cala et Fuengirola, garde les plages et l'A-7 à proximité tout en restant au-dessus de la route côtière.",
 "Mijas zwischen La Cala und Fuengirola hält Strände und die A-7 nah und liegt dabei oberhalb der Küstenstraße.",
 "Михас между Ла-Калой и Фуэнхиролой держит пляжи и A-7 рядом, оставаясь выше прибрежной дороги.",
 "ميخاس بين لا كالا وفوينخيرولا تُبقي الشواطئ وطريق A-7 قريبين مع البقاء فوق طريق الساحل.",
 "Mijas tussen La Cala en Fuengirola houdt de stranden en de A-7 dichtbij en ligt toch boven de kustweg.",
 "Mijas między La Cala a Fuengirolą utrzymuje plaże i A-7 blisko, pozostając powyżej drogi nadmorskiej.",
 "Mijas mellom La Cala og Fuengirola holder strendene og A-7 nær, men ligger over kystveien.",
 "Mijas mellan La Cala och Fuengirola håller stränderna och A-7 nära men ligger ovanför kustvägen.")
a("Ten homes are listed today and the seller's list changes, so it is worth confirming before you shortlist.",
 "Hoy figuran diez viviendas y la lista del vendedor cambia, así que conviene confirmarla antes de preseleccionar.",
 "Dix logements figurent aujourd'hui sur la liste du vendeur, qui évolue : mieux vaut la confirmer avant de présélectionner.",
 "Heute sind zehn Wohnungen gelistet, und die Liste des Verkäufers ändert sich, daher lohnt sich eine Bestätigung vor der Auswahl.",
 "Сегодня в списке десять квартир, а список продавца меняется, поэтому стоит уточнить его перед отбором.",
 "عشرة منازل مدرجة اليوم وقائمة البائع تتغير، لذا يُستحسن تأكيدها قبل الاختيار.",
 "Vandaag staan er tien woningen op de lijst van de verkoper, die verandert, dus het loont die te bevestigen voordat u selecteert.",
 "Dziś na liście sprzedającego jest dziesięć mieszkań, a lista się zmienia, więc warto ją potwierdzić przed wyborem.",
 "I dag er ti boliger oppført, og selgerens liste endrer seg, så det lønner seg å bekrefte før du velger ut.",
 "I dag listas tio bostäder och säljarens lista ändras, så det är värt att bekräfta innan urvalet görs.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
