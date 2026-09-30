# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 5: location, FAQ, enquiry.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Altos de los Monteros, <em>above the coast</em>",
 "Altos de los Monteros, <em>sobre la costa</em>","Altos de los Monteros, <em>au-dessus de la côte</em>",
 "Altos de los Monteros, <em>über der Küste</em>","Альтос-де-лос-Монтерос, <em>над побережьем</em>",
 "ألتوس دي لوس مونتيروس، <em>فوق الساحل</em>","Altos de los Monteros, <em>boven de kust</em>",
 "Altos de los Monteros, <em>ponad wybrzeżem</em>","Altos de los Monteros, <em>over kysten</em>",
 "Altos de los Monteros, <em>ovanför kusten</em>")

a("On the hillside behind Los Monteros, east of Marbella town, with the sea in front and the Sierra Blanca foothills behind.",
 "En la ladera detrás de Los Monteros, al este del casco urbano de Marbella, con el mar delante y las estribaciones de Sierra Blanca detrás.",
 "Sur le coteau derrière Los Monteros, à l'est du centre de Marbella, la mer devant et les contreforts de la Sierra Blanca derrière.",
 "Am Hang hinter Los Monteros, östlich des Stadtkerns von Marbella, mit dem Meer davor und den Ausläufern der Sierra Blanca dahinter.",
 "На склоне за Лос-Монтерос, к востоку от центра Марбельи: море впереди, предгорья Сьерра-Бланка позади.",
 "على المنحدر خلف لوس مونتيروس، شرق مركز مربيّا، والبحر في المقدّمة وسفوح سييرا بلانكا في الخلف.",
 "Op de helling achter Los Monteros, ten oosten van het centrum van Marbella, met de zee ervoor en de uitlopers van de Sierra Blanca erachter.",
 "Na zboczu za Los Monteros, na wschód od centrum Marbelli, z morzem przed sobą i podnóżem Sierra Blanca za plecami.",
 "I skråningen bak Los Monteros, øst for Marbella sentrum, med sjøen foran og utløperne av Sierra Blanca bak.",
 "I sluttningen bakom Los Monteros, öster om Marbellas centrum, med havet framför och Sierra Blancas utlöpare bakom.")

a("Altos de los <em>Monteros</em>",
 "Altos de los <em>Monteros</em>","Altos de los <em>Monteros</em>","Altos de los <em>Monteros</em>",
 "Альтос-де-лос-<em>Монтерос</em>","ألتوس دي لوس <em>مونتيروس</em>","Altos de los <em>Monteros</em>",
 "Altos de los <em>Monteros</em>","Altos de los <em>Monteros</em>","Altos de los <em>Monteros</em>")

a("Altos de los Monteros",
 "Altos de los Monteros","Altos de los Monteros","Altos de los Monteros","Альтос-де-лос-Монтерос",
 "ألتوس دي لوس مونتيروس","Altos de los Monteros","Altos de los Monteros","Altos de los Monteros","Altos de los Monteros")

a("Los Monteros beach",
 "Playa de Los Monteros","Plage de Los Monteros","Strand Los Monteros","Пляж Лос-Монтерос","شاطئ لوس مونتيروس",
 "Strand Los Monteros","Plaża Los Monteros","Los Monteros-stranden","Los Monteros-stranden")

a("5 km","5 km","5 km","5 km","5 км","5 كم","5 km","5 km","5 km","5 km")
a("4 km","4 km","4 km","4 km","4 км","4 كم","4 km","4 km","4 km","4 km")
a("6.2 km","6,2 km","6,2 km","6,2 km","6,2 км","6.2 كم","6,2 km","6,2 km","6,2 km","6,2 km")

a("La Canada shopping centre",
 "Centro comercial La Cañada","Centre commercial La Cañada","Einkaufszentrum La Cañada",
 "Торговый центр La Cañada","مركز لا كانيادا التجاري","Winkelcentrum La Cañada",
 "Centrum handlowe La Cañada","Kjøpesenteret La Cañada","Köpcentrumet La Cañada")

a("Two parking spaces and a storeroom with every apartment, three spaces and a storeroom with every penthouse, all at no extra cost. Tax is not included: VAT at 10 per cent and stamp duty at 1.20 per cent are added on top, along with notary and land registry fees.",
 "Dos plazas de garaje y un trastero con cada apartamento, y tres plazas y un trastero con cada ático, todo sin coste adicional. Los impuestos no están incluidos: se añaden el IVA del 10 por ciento y el impuesto de actos jurídicos documentados del 1,20 por ciento, además de los gastos de notaría y registro.",
 "Deux places de parking et un débarras avec chaque appartement, trois places et un débarras avec chaque penthouse, le tout sans supplément. Les taxes ne sont pas comprises : la TVA à 10 pour cent et le droit de timbre à 1,20 pour cent s'ajoutent, ainsi que les frais de notaire et d'enregistrement.",
 "Zwei Stellplätze und ein Abstellraum zu jeder Wohnung, drei Stellplätze und ein Abstellraum zu jedem Penthouse, alles ohne Aufpreis. Steuern sind nicht enthalten: 10 Prozent Mehrwertsteuer und 1,20 Prozent Stempelsteuer kommen hinzu, dazu Notar- und Grundbuchkosten.",
 "Два машиноместа и кладовая с каждой квартирой, три машиноместа и кладовая с каждым пентхаусом — всё без доплаты. Налоги не включены: сверху добавляются НДС 10 процентов и гербовый сбор 1,20 процента, а также расходы на нотариуса и регистрацию.",
 "موقفا سيارات ومخزن مع كل شقة، وثلاثة مواقف ومخزن مع كل بنتهاوس، جميعها دون تكلفة إضافية. الضرائب غير مشمولة: تُضاف ضريبة القيمة المضافة 10 بالمئة ورسم الدمغة 1.20 بالمئة، إلى جانب أتعاب التوثيق والتسجيل العقاري.",
 "Twee parkeerplaatsen en een berging bij elk appartement, drie plaatsen en een berging bij elk penthouse, alles zonder meerprijs. Belasting is niet inbegrepen: 10 procent btw en 1,20 procent overdrachtsbelasting komen erbij, samen met notaris- en kadasterkosten.",
 "Dwa miejsca postojowe i komórka przy każdym apartamencie, trzy miejsca i komórka przy każdym penthousie, wszystko bez dopłaty. Podatek nie jest wliczony: doliczany jest VAT w wysokości 10 procent i podatek od czynności cywilnoprawnych 1,20 procent, a także opłaty notarialne i wieczystoksięgowe.",
 "To parkeringsplasser og en bod til hver leilighet, tre plasser og en bod til hver toppleilighet, alt uten tillegg. Skatt er ikke inkludert: merverdiavgift på 10 prosent og dokumentavgift på 1,20 prosent kommer i tillegg, sammen med notar- og tinglysingsgebyrer.",
 "Två parkeringsplatser och ett förråd till varje lägenhet, tre platser och ett förråd till varje takvåning, allt utan extra kostnad. Skatt ingår inte: moms på 10 procent och stämpelskatt på 1,20 procent tillkommer, liksom notarie- och registreringsavgifter.")

a("When will the homes be delivered?",
 "¿Cuándo se entregarán las viviendas?","Quand les logements seront-ils livrés ?","Wann werden die Wohnungen übergeben?",
 "Когда будут переданы квартиры?","متى ستُسلَّم المساكن؟","Wanneer worden de woningen opgeleverd?",
 "Kiedy mieszkania zostaną oddane?","Når blir boligene overlevert?","När överlämnas bostäderna?")

a("The developer gives the second quarter of 2029. Nueva Living asks for that date in writing and for the contract to say what happens if it slips.",
 "El promotor indica el segundo trimestre de 2029. Nueva Living pide esa fecha por escrito y que el contrato recoja qué ocurre si se retrasa.",
 "Le promoteur annonce le deuxième trimestre 2029. Nueva Living demande cette date par écrit et que le contrat précise ce qui se passe en cas de retard.",
 "Der Bauträger nennt das zweite Quartal 2029. Nueva Living lässt sich diesen Termin schriftlich geben und fordert, dass der Vertrag regelt, was bei Verzug gilt.",
 "Застройщик называет второй квартал 2029 года. Nueva Living запрашивает эту дату письменно и требует, чтобы в договоре было прописано, что происходит при задержке.",
 "يحدّد المطوّر الربع الثاني من 2029. تطلب Nueva Living هذا التاريخ كتابةً وأن ينصّ العقد على ما يحدث في حال التأخير.",
 "De ontwikkelaar noemt het tweede kwartaal van 2029. Nueva Living vraagt die datum schriftelijk op en eist dat het contract vastlegt wat er gebeurt bij vertraging.",
 "Deweloper podaje drugi kwartał 2029 roku. Nueva Living prosi o tę datę na piśmie i o to, by umowa określała, co się stanie w razie opóźnienia.",
 "Utbyggeren oppgir andre kvartal 2029. Nueva Living ber om den datoen skriftlig og om at kontrakten sier hva som skjer ved forsinkelse.",
 "Byggherren anger andra kvartalet 2029. Nueva Living begär det datumet skriftligt och att avtalet anger vad som gäller vid försening.")

a("Has the building licence been granted?",
 "¿Está concedida la licencia de obra?","Le permis de construire est-il accordé ?","Ist die Baugenehmigung erteilt?",
 "Получено ли разрешение на строительство?","هل مُنحت رخصة البناء؟","Is de bouwvergunning verleend?",
 "Czy pozwolenie na budowę zostało wydane?","Er byggetillatelsen gitt?","Är bygglovet beviljat?")

a("Yes, confirmed by the developer in September 2026. The written disclosure document was issued before that and still records the licence as applied for on 27 December 2024, so we ask for the grant itself rather than rely on either.",
 "Sí, confirmado por el promotor en septiembre de 2026. El documento informativo escrito es anterior y todavía registra la licencia como solicitada el 27 de diciembre de 2024, así que pedimos la concesión en sí y no nos apoyamos en ninguno de los dos.",
 "Oui, confirmé par le promoteur en septembre 2026. Le document d'information écrit lui est antérieur et mentionne encore le permis comme demandé le 27 décembre 2024 ; nous réclamons donc l'arrêté lui-même plutôt que de nous fier à l'un ou à l'autre.",
 "Ja, vom Bauträger im September 2026 bestätigt. Das schriftliche Informationsdokument stammt aus der Zeit davor und führt die Genehmigung weiterhin als am 27. Dezember 2024 beantragt, deshalb verlangen wir die Genehmigung selbst und verlassen uns auf keines von beiden.",
 "Да, подтверждено застройщиком в сентябре 2026 года. Письменный информационный документ выпущен раньше и по-прежнему указывает разрешение как запрошенное 27 декабря 2024 года, поэтому мы запрашиваем сам акт, а не полагаемся ни на один из них.",
 "نعم، أكّده المطوّر في سبتمبر 2026. أما وثيقة الإفصاح المكتوبة فصدرت قبل ذلك وما زالت تسجّل الرخصة على أنها مُقدَّمة في 27 ديسمبر 2024، لذا نطلب قرار المنح نفسه بدل الاعتماد على أيّ منهما.",
 "Ja, in september 2026 door de ontwikkelaar bevestigd. Het schriftelijke informatiedocument dateert van daarvóór en vermeldt de vergunning nog als aangevraagd op 27 december 2024, dus vragen wij de verlening zelf op in plaats van op een van beide te vertrouwen.",
 "Tak, potwierdzone przez dewelopera we wrześniu 2026 roku. Pisemny dokument informacyjny powstał wcześniej i wciąż odnotowuje pozwolenie jako złożone 27 grudnia 2024 roku, dlatego prosimy o samą decyzję, a nie opieramy się na żadnym z nich.",
 "Ja, bekreftet av utbyggeren i september 2026. Det skriftlige opplysningsdokumentet er eldre og fører fortsatt opp tillatelsen som søkt 27. desember 2024, så vi ber om selve vedtaket i stedet for å stole på noen av dem.",
 "Ja, bekräftat av byggherren i september 2026. Det skriftliga informationsdokumentet är äldre och anger fortfarande lovet som ansökt den 27 december 2024, så vi begär själva beslutet i stället för att förlita oss på något av dem.")

a("How many homes are for sale?",
 "¿Cuántas viviendas están a la venta?","Combien de logements sont à vendre ?","Wie viele Wohnungen stehen zum Verkauf?",
 "Сколько квартир продаётся?","كم عدد المساكن المعروضة للبيع؟","Hoeveel woningen staan te koop?",
 "Ile mieszkań jest na sprzedaż?","Hvor mange boliger er til salgs?","Hur många bostäder är till salu?")

a("The scheme has eighty homes in eight blocks. Twenty have been released so far; twelve of those are available, seven are sold and one is reserved. The remaining sixty will be priced later.",
 "La promoción tiene ochenta viviendas en ocho bloques. Hasta ahora se han puesto a la venta veinte; de ellas, doce están disponibles, siete vendidas y una reservada. Las sesenta restantes se pondrán a precio más adelante.",
 "Le programme compte quatre-vingts logements en huit blocs. Vingt ont été mis en vente à ce jour ; douze sont disponibles, sept vendus et un réservé. Les soixante restants seront tarifés plus tard.",
 "Das Projekt umfasst achtzig Wohnungen in acht Blöcken. Zwanzig wurden bisher freigegeben; davon sind zwölf verfügbar, sieben verkauft und eine reserviert. Die übrigen sechzig werden später bepreist.",
 "В проекте восемьдесят квартир в восьми корпусах. На сегодня выведено в продажу двадцать: двенадцать доступны, семь проданы, одна забронирована. Оставшиеся шестьдесят получат цену позже.",
 "يضمّ المشروع ثمانين مسكناً في ثمانية مبانٍ. طُرح عشرون حتى الآن؛ منها اثنا عشر متاحة وسبعة مباعة وواحد محجوز. أما الستون الباقية فستُسعَّر لاحقاً.",
 "Het project telt tachtig woningen in acht blokken. Twintig zijn tot nu toe vrijgegeven; daarvan zijn er twaalf beschikbaar, zeven verkocht en één gereserveerd. De overige zestig krijgen later een prijs.",
 "Inwestycja liczy osiemdziesiąt mieszkań w ośmiu budynkach. Dotąd wprowadzono do sprzedaży dwadzieścia; z tego dwanaście jest dostępnych, siedem sprzedanych, a jedno zarezerwowane. Pozostałe sześćdziesiąt zostanie wycenione później.",
 "Prosjektet har åtti boliger i åtte blokker. Tjue er lagt ut så langt; av dem er tolv ledige, sju solgt og én reservert. De resterende seksti prises senere.",
 "Projektet har åttio bostäder i åtta huskroppar. Tjugo har släppts hittills; av dem är tolv lediga, sju sålda och en reserverad. De återstående sextio prissätts senare.")

a("How does the payment schedule work?",
 "¿Cómo funciona el calendario de pagos?","Comment fonctionne l'échéancier de paiement ?","Wie funktioniert der Zahlungsplan?",
 "Как устроен график платежей?","كيف يعمل جدول السداد؟","Hoe werkt het betalingsschema?",
 "Jak działa harmonogram płatności?","Hvordan fungerer betalingsplanen?","Hur fungerar betalningsplanen?")

a("Twenty thousand euros plus VAT on reservation, 20 per cent plus VAT at the private contract sixty days later, 10 per cent at twelve months, 10 per cent at eighteen months, and the remaining 60 per cent at the notary on delivery. The developer states the deferral is interest-free and that payments on account are secured by bank guarantee.",
 "Veinte mil euros más IVA en la reserva, un 20 por ciento más IVA en el contrato privado sesenta días después, un 10 por ciento a los doce meses, un 10 por ciento a los dieciocho, y el 60 por ciento restante ante notario en la entrega. El promotor declara que el aplazamiento no devenga intereses y que las cantidades a cuenta están cubiertas por aval bancario.",
 "Vingt mille euros hors TVA à la réservation, 20 pour cent hors TVA au contrat privé soixante jours plus tard, 10 pour cent à douze mois, 10 pour cent à dix-huit mois, et les 60 pour cent restants chez le notaire à la livraison. Le promoteur déclare que le différé est sans intérêt et que les sommes versées sont couvertes par une garantie bancaire.",
 "Zwanzigtausend Euro zuzüglich Mehrwertsteuer bei der Reservierung, 20 Prozent zuzüglich Mehrwertsteuer beim privaten Kaufvertrag sechzig Tage später, 10 Prozent nach zwölf Monaten, 10 Prozent nach achtzehn Monaten und die verbleibenden 60 Prozent beim Notar zur Übergabe. Der Bauträger erklärt, die Stundung sei zinsfrei und die Anzahlungen seien durch eine Bankbürgschaft gesichert.",
 "Двадцать тысяч евро плюс НДС при бронировании, 20 процентов плюс НДС при частном договоре через шестьдесят дней, 10 процентов через двенадцать месяцев, 10 процентов через восемнадцать и оставшиеся 60 процентов у нотариуса при передаче. Застройщик заявляет, что рассрочка беспроцентная, а внесённые суммы обеспечены банковской гарантией.",
 "عشرون ألف يورو زائد ضريبة القيمة المضافة عند الحجز، و20 بالمئة زائد الضريبة عند العقد الخاص بعد ستين يوماً، و10 بالمئة عند اثني عشر شهراً، و10 بالمئة عند ثمانية عشر شهراً، والـ60 بالمئة الباقية لدى الموثّق عند التسليم. يذكر المطوّر أن التأجيل بلا فائدة وأن المبالغ على الحساب مضمونة بكفالة مصرفية.",
 "Twintigduizend euro plus btw bij reservering, 20 procent plus btw bij het onderhandse contract zestig dagen later, 10 procent na twaalf maanden, 10 procent na achttien maanden en de resterende 60 procent bij de notaris bij oplevering. De ontwikkelaar verklaart dat het uitstel renteloos is en dat voorschotten door een bankgarantie zijn gedekt.",
 "Dwadzieścia tysięcy euro plus VAT przy rezerwacji, 20 procent plus VAT przy umowie przedwstępnej sześćdziesiąt dni później, 10 procent po dwunastu miesiącach, 10 procent po osiemnastu i pozostałe 60 procent u notariusza przy odbiorze. Deweloper oświadcza, że odroczenie jest nieoprocentowane, a wpłaty zabezpieczone gwarancją bankową.",
 "Tjue tusen euro pluss mva. ved reservasjon, 20 prosent pluss mva. ved den private kontrakten seksti dager senere, 10 prosent etter tolv måneder, 10 prosent etter atten måneder, og de resterende 60 prosent hos notaren ved overtakelse. Utbyggeren oppgir at utsettelsen er rentefri og at innbetalinger er sikret med bankgaranti.",
 "Tjugotusen euro plus moms vid bokning, 20 procent plus moms vid det privata avtalet sextio dagar senare, 10 procent efter tolv månader, 10 procent efter arton månader och återstående 60 procent hos notarien vid tillträdet. Byggherren uppger att uppskovet är räntefritt och att inbetalningarna är säkrade med bankgaranti.")

a("Do all the homes have sea views?",
 "¿Todas las viviendas tienen vistas al mar?","Tous les logements ont-ils vue sur la mer ?","Haben alle Wohnungen Meerblick?",
 "У всех ли квартир вид на море?","هل تتمتع كل المساكن بإطلالة على البحر؟","Hebben alle woningen zeezicht?",
 "Czy wszystkie mieszkania mają widok na morze?","Har alle boligene sjøutsikt?","Har alla bostäder havsutsikt?")

a("The developer designs for it: each block is set a step above the one to its south so that none looks into its neighbour's roof. Which view a particular home has still depends on its block and floor, and that is worth checking on site.",
 "El promotor lo ha proyectado así: cada bloque se sitúa un escalón por encima del que tiene al sur, de modo que ninguno mira al tejado del vecino. Qué vista tiene cada vivienda depende de su bloque y su planta, y eso conviene comprobarlo sobre el terreno.",
 "Le promoteur l'a conçu ainsi : chaque bloc est implanté un cran plus haut que celui au sud, de sorte qu'aucun ne donne sur le toit du voisin. La vue propre à un logement dépend toutefois de son bloc et de son étage, ce qu'il vaut mieux vérifier sur place.",
 "Der Bauträger plant es so: Jeder Block steht eine Stufe höher als der südlich davon, sodass keiner auf das Dach des Nachbarn blickt. Welche Aussicht eine bestimmte Wohnung hat, hängt dennoch von Block und Geschoss ab, und das prüft man am besten vor Ort.",
 "Застройщик закладывает это в проект: каждый корпус стоит на ступень выше того, что южнее, поэтому ни один не смотрит на крышу соседа. Какой вид у конкретной квартиры, всё же зависит от корпуса и этажа, и это стоит проверить на месте.",
 "صمّم المطوّر المشروع على هذا الأساس: كل مبنى يقع درجة أعلى من المبنى الواقع جنوبه، فلا يطلّ أي منها على سطح جاره. لكن الإطلالة الفعلية لمسكن بعينه تبقى رهن مبناه وطابقه، وهو ما يستحقّ التحقّق منه في الموقع.",
 "De ontwikkelaar ontwerpt daarop: elk blok ligt een trede hoger dan het blok ten zuiden ervan, zodat geen enkel blok op het dak van de buren uitkijkt. Welk uitzicht een bepaalde woning heeft, hangt nog altijd af van blok en verdieping, en dat is ter plaatse het controleren waard.",
 "Deweloper tak to zaprojektował: każdy budynek jest osadzony o stopień wyżej niż ten na południe od niego, więc żaden nie patrzy na dach sąsiada. To, jaki widok ma konkretne mieszkanie, zależy jednak od budynku i piętra, a to warto sprawdzić na miejscu.",
 "Utbyggeren har prosjektert for det: hver blokk er satt et trinn høyere enn blokken sør for den, slik at ingen ser inn på naboens tak. Hvilken utsikt en bestemt bolig har, avhenger likevel av blokk og etasje, og det er verdt å sjekke på stedet.",
 "Byggherren projekterar för det: varje huskropp är satt ett steg högre än den söder om den, så att ingen tittar in i grannens tak. Vilken utsikt en viss bostad har beror ändå på huskropp och våningsplan, och det är värt att kontrollera på plats.")

a("How long do the prices hold?",
 "¿Cuánto tiempo se mantienen los precios?","Combien de temps les prix restent-ils valables ?","Wie lange gelten die Preise?",
 "Как долго действуют цены?","كم تبقى الأسعار سارية؟","Hoelang blijven de prijzen geldig?",
 "Jak długo obowiązują ceny?","Hvor lenge gjelder prisene?","Hur länge gäller priserna?")

a("The seller's documents disagree. The price list and the disclosure document both say two days from download; the explanatory note on price and payment terms says eleven. Nueva Living asks the seller which one governs before you rely on either.",
 "Los documentos del vendedor no coinciden. La lista de precios y el documento informativo dicen dos días desde la descarga; la nota explicativa sobre precio y forma de pago dice once. Nueva Living pregunta al vendedor cuál prevalece antes de que usted se apoye en ninguno.",
 "Les documents du vendeur se contredisent. La liste de prix et le document d'information indiquent deux jours à compter du téléchargement ; la note explicative sur le prix et les modalités de paiement en indique onze. Nueva Living demande au vendeur lequel fait foi avant que vous ne vous y fiiez.",
 "Die Unterlagen des Verkäufers widersprechen sich. Preisliste und Informationsdokument nennen beide zwei Tage ab dem Herunterladen; die Erläuterung zu Preis und Zahlungsbedingungen nennt elf. Nueva Living fragt beim Verkäufer nach, welche Angabe gilt, bevor Sie sich auf eine davon verlassen.",
 "Документы продавца противоречат друг другу. Прайс-лист и информационный документ говорят о двух днях с момента скачивания; пояснительная записка о цене и условиях оплаты — об одиннадцати. Nueva Living уточняет у продавца, какой срок имеет силу, прежде чем вы будете на него полагаться.",
 "وثائق البائع متعارضة. قائمة الأسعار ووثيقة الإفصاح تذكران يومين من تاريخ التنزيل؛ أما المذكّرة التوضيحية للسعر وشروط الدفع فتذكر أحد عشر يوماً. تسأل Nueva Living البائع أيّهما المعتمد قبل أن تعتمد أنت على أيّ منهما.",
 "De documenten van de verkoper spreken elkaar tegen. De prijslijst en het informatiedocument noemen beide twee dagen na het downloaden; de toelichting op prijs en betalingsvoorwaarden noemt elf. Nueva Living vraagt de verkoper welke geldt voordat u op een van beide afgaat.",
 "Dokumenty sprzedającego są rozbieżne. Cennik i dokument informacyjny podają dwa dni od pobrania; nota wyjaśniająca dotycząca ceny i warunków płatności podaje jedenaście. Nueva Living pyta sprzedającego, która wersja obowiązuje, zanim Państwo się na którejkolwiek oprą.",
 "Selgerens dokumenter er uenige. Prislisten og opplysningsdokumentet sier begge to dager fra nedlasting; forklaringsnotatet om pris og betalingsvilkår sier elleve. Nueva Living spør selgeren hvilken som gjelder før du legger noen av dem til grunn.",
 "Säljarens dokument säger olika saker. Prislistan och informationsdokumentet anger båda två dagar från nedladdningen; den förklarande noten om pris och betalningsvillkor anger elva. Nueva Living frågar säljaren vilken som gäller innan ni förlitar er på någon av dem.")

a("Tell us what you are looking for and we will come back with the current list and the full cost including tax.",
 "Cuéntenos qué busca y le responderemos con la lista actual y el coste completo con impuestos incluidos.",
 "Dites-nous ce que vous cherchez et nous reviendrons vers vous avec la liste actuelle et le coût complet, taxes comprises.",
 "Sagen Sie uns, was Sie suchen, und wir melden uns mit der aktuellen Liste und den Gesamtkosten einschließlich Steuern.",
 "Расскажите, что вы ищете, и мы вернёмся с актуальным списком и полной стоимостью с учётом налогов.",
 "أخبرنا بما تبحث عنه وسنعود إليك بالقائمة الحالية والتكلفة الكاملة شاملة الضرائب.",
 "Vertel ons wat u zoekt en wij komen terug met de actuele lijst en de volledige kosten inclusief belasting.",
 "Prosimy powiedzieć, czego Państwo szukają, a wrócimy z aktualną listą i pełnym kosztem wraz z podatkiem.",
 "Fortell oss hva du ser etter, så kommer vi tilbake med den aktuelle listen og den fulle kostnaden inkludert skatt.",
 "Berätta vad ni söker så återkommer vi med den aktuella listan och den fulla kostnaden inklusive skatt.")

a("I would like the current availability and prices for Altos Terrace Residences.",
 "Me gustaría conocer la disponibilidad y los precios actuales de Altos Terrace Residences.",
 "Je souhaite connaître la disponibilité et les prix actuels d'Altos Terrace Residences.",
 "Ich hätte gern die aktuelle Verfügbarkeit und die Preise für Altos Terrace Residences.",
 "Хотел(а) бы узнать актуальное наличие и цены по Altos Terrace Residences.",
 "أودّ معرفة التوافر والأسعار الحالية لمشروع Altos Terrace Residences.",
 "Ik ontvang graag de actuele beschikbaarheid en prijzen van Altos Terrace Residences.",
 "Chciałbym poznać aktualną dostępność i ceny w Altos Terrace Residences.",
 "Jeg vil gjerne ha oppdatert tilgjengelighet og priser for Altos Terrace Residences.",
 "Jag vill gärna ha aktuell tillgänglighet och priser för Altos Terrace Residences.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
