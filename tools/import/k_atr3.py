# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 3: source note, timeline, payment, why.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Every figure is transcribed from the seller's own price list dated 17 September 2026. Interior areas and terrace areas are the developer's. One cell is left blank rather than estimated: the seller has not issued a floorplan for apartment 71B. Prices exclude tax. VAT is charged at 10 per cent and stamp duty at 1.20 per cent, so the 540,000 euro apartment costs about 600,000 euros before notary and land registry fees, and the 1,050,000 euro penthouse about 1,168,000. Two parking spaces and a storeroom are included at no extra cost for an apartment, three spaces and a storeroom for a penthouse.",
 "Todas las cifras están transcritas de la lista de precios del propio vendedor con fecha 17 de septiembre de 2026. Las superficies interiores y de terraza son las del promotor. Una casilla se deja vacía en lugar de estimarla: el vendedor no ha emitido plano para el apartamento 71B. Los precios no incluyen impuestos. El IVA es del 10 por ciento y el impuesto de actos jurídicos documentados del 1,20 por ciento, de modo que el apartamento de 540.000 euros cuesta unos 600.000 euros antes de notaría y registro, y el ático de 1.050.000 euros unos 1.168.000. Dos plazas de garaje y un trastero se incluyen sin coste adicional en los apartamentos, y tres plazas y un trastero en los áticos.",
 "Tous les chiffres sont transcrits de la liste de prix du vendeur datée du 17 septembre 2026. Les surfaces intérieures et de terrasse sont celles du promoteur. Une case est laissée vide plutôt qu'estimée : le vendeur n'a pas établi de plan pour l'appartement 71B. Les prix s'entendent hors taxes. La TVA est de 10 pour cent et le droit de timbre de 1,20 pour cent, de sorte que l'appartement à 540 000 euros revient à environ 600 000 euros avant frais de notaire et d'enregistrement, et le penthouse à 1 050 000 euros à environ 1 168 000. Deux places de parking et un débarras sont inclus sans supplément pour un appartement, trois places et un débarras pour un penthouse.",
 "Alle Zahlen sind aus der Preisliste des Verkäufers vom 17. September 2026 übernommen. Innen- und Terrassenflächen stammen vom Bauträger. Ein Feld bleibt leer statt geschätzt: Für Wohnung 71B hat der Verkäufer keinen Grundriss herausgegeben. Die Preise verstehen sich ohne Steuern. Die Mehrwertsteuer beträgt 10 Prozent, die Stempelsteuer 1,20 Prozent, sodass die Wohnung für 540.000 Euro vor Notar- und Grundbuchkosten rund 600.000 Euro kostet und das Penthouse für 1.050.000 Euro rund 1.168.000. Zwei Stellplätze und ein Abstellraum sind bei einer Wohnung ohne Aufpreis enthalten, drei Stellplätze und ein Abstellraum beim Penthouse.",
 "Все цифры перенесены из прайс-листа самого продавца от 17 сентября 2026 года. Внутренние площади и площади террас — данные застройщика. Одна ячейка оставлена пустой, а не оценена: продавец не выпустил планировку квартиры 71B. Цены указаны без налогов. НДС составляет 10 процентов, гербовый сбор — 1,20 процента, поэтому квартира за 540 000 евро обходится примерно в 600 000 евро до нотариуса и регистрации, а пентхаус за 1 050 000 евро — примерно в 1 168 000. Два машиноместа и кладовая входят в цену квартиры без доплаты, три машиноместа и кладовая — в цену пентхауса.",
 "جميع الأرقام منقولة عن قائمة أسعار البائع نفسه المؤرخة 17 سبتمبر 2026. المساحات الداخلية ومساحات التراسات هي أرقام المطوّر. تُركت خانة واحدة فارغة بدل تقديرها: لم يصدر البائع مخططاً للشقة 71B. الأسعار لا تشمل الضرائب. ضريبة القيمة المضافة 10 بالمئة ورسم الدمغة 1.20 بالمئة، فتصبح الشقة بسعر 540,000 يورو نحو 600,000 يورو قبل أتعاب التوثيق والتسجيل، والبنتهاوس بسعر 1,050,000 يورو نحو 1,168,000. يشمل السعر موقفي سيارات ومخزناً للشقة، وثلاثة مواقف ومخزناً للبنتهاوس، دون تكلفة إضافية.",
 "Alle cijfers zijn overgenomen uit de eigen prijslijst van de verkoper van 17 september 2026. De binnen- en terrasoppervlakken zijn die van de ontwikkelaar. Eén cel blijft leeg in plaats van geschat: de verkoper heeft geen plattegrond uitgegeven voor appartement 71B. De prijzen zijn exclusief belasting. De btw bedraagt 10 procent en de overdrachtsbelasting 1,20 procent, zodat het appartement van 540.000 euro ongeveer 600.000 euro kost vóór notaris- en kadasterkosten, en het penthouse van 1.050.000 euro ongeveer 1.168.000. Twee parkeerplaatsen en een berging zijn zonder meerprijs inbegrepen bij een appartement, drie plaatsen en een berging bij een penthouse.",
 "Wszystkie liczby przepisano z własnego cennika sprzedającego z 17 września 2026 roku. Powierzchnie wewnętrzne i tarasów pochodzą od dewelopera. Jedna komórka pozostaje pusta zamiast szacowana: sprzedający nie wydał rzutu dla apartamentu 71B. Ceny nie zawierają podatku. VAT wynosi 10 procent, a podatek od czynności cywilnoprawnych 1,20 procent, więc apartament za 540 000 euro kosztuje około 600 000 euro przed opłatami notarialnymi i wpisem do księgi wieczystej, a penthouse za 1 050 000 euro około 1 168 000. Dwa miejsca postojowe i komórka są wliczone bez dopłaty w apartamencie, trzy miejsca i komórka w penthousie.",
 "Alle tall er hentet fra selgerens egen prisliste datert 17. september 2026. Innvendige arealer og terrassearealer er utbyggerens. Én celle står tom i stedet for anslått: selgeren har ikke utstedt plantegning for leilighet 71B. Prisene er uten skatt. Merverdiavgiften er 10 prosent og dokumentavgiften 1,20 prosent, slik at leiligheten til 540 000 euro koster rundt 600 000 euro før notar- og tinglysingsgebyrer, og toppleiligheten til 1 050 000 euro rundt 1 168 000. To parkeringsplasser og en bod er inkludert uten tillegg for en leilighet, tre plasser og en bod for en toppleilighet.",
 "Varje siffra är avskriven från säljarens egen prislista daterad 17 september 2026. Invändiga ytor och terrassytor är byggherrens. En cell lämnas tom i stället för uppskattad: säljaren har inte utfärdat någon planritning för lägenhet 71B. Priserna är exklusive skatt. Momsen är 10 procent och stämpelskatten 1,20 procent, så lägenheten för 540 000 euro kostar omkring 600 000 euro före notarie- och registreringsavgifter, och takvåningen för 1 050 000 euro omkring 1 168 000. Två parkeringsplatser och ett förråd ingår utan extra kostnad i en lägenhet, tre platser och ett förråd i en takvåning.")

a("The building licence has been granted, which the developer confirmed in September 2026. The developer's own disclosure document, issued earlier, recorded the licence as applied for on 27 December 2024 with an expected grant date of 30 April 2026, and the build stage as design rather than construction. Completion is given as the second quarter of 2029. Nueva Living asks for the delivery date in writing and puts it in the contract.",
 "La licencia de obra está concedida, según confirmó el promotor en septiembre de 2026. El documento informativo del propio promotor, emitido antes, registraba la licencia como solicitada el 27 de diciembre de 2024 con fecha prevista de obtención el 30 de abril de 2026, y la fase de obra como proyecto y no construcción. La entrega se indica para el segundo trimestre de 2029. Nueva Living pide la fecha de entrega por escrito y la incorpora al contrato.",
 "Le permis de construire est accordé, ce que le promoteur a confirmé en septembre 2026. Le document d'information du promoteur, établi auparavant, mentionnait le permis comme demandé le 27 décembre 2024 avec une obtention prévue au 30 avril 2026, et le stade des travaux comme étude et non construction. La livraison est annoncée pour le deuxième trimestre 2029. Nueva Living demande la date de livraison par écrit et la fait inscrire au contrat.",
 "Die Baugenehmigung ist erteilt, was der Bauträger im September 2026 bestätigt hat. Das zuvor ausgegebene Informationsdokument des Bauträgers führte die Genehmigung noch als am 27. Dezember 2024 beantragt mit erwarteter Erteilung zum 30. April 2026 und die Bauphase als Planung statt Bau. Als Fertigstellung ist das zweite Quartal 2029 angegeben. Nueva Living lässt sich den Übergabetermin schriftlich geben und nimmt ihn in den Vertrag auf.",
 "Разрешение на строительство получено, что застройщик подтвердил в сентябре 2026 года. В более раннем информационном документе самого застройщика разрешение значилось как запрошенное 27 декабря 2024 года с ожидаемой датой выдачи 30 апреля 2026 года, а стадия — как проектирование, а не строительство. Сдача указана на второй квартал 2029 года. Nueva Living запрашивает дату передачи в письменном виде и вносит её в договор.",
 "رخصة البناء ممنوحة، وهو ما أكّده المطوّر في سبتمبر 2026. أما وثيقة الإفصاح الصادرة عن المطوّر قبل ذلك فكانت تسجّل الرخصة على أنها مُقدَّمة بتاريخ 27 ديسمبر 2024 مع تاريخ منح متوقّع في 30 أبريل 2026، ومرحلة العمل على أنها تصميم لا إنشاء. التسليم محدّد في الربع الثاني من 2029. تطلب Nueva Living تاريخ التسليم كتابةً وتُدرجه في العقد.",
 "De bouwvergunning is verleend, wat de ontwikkelaar in september 2026 heeft bevestigd. Het eerder uitgegeven informatiedocument van de ontwikkelaar vermeldde de vergunning nog als aangevraagd op 27 december 2024 met een verwachte verlening op 30 april 2026, en de bouwfase als ontwerp in plaats van bouw. De oplevering is opgegeven als het tweede kwartaal van 2029. Nueva Living vraagt de opleverdatum schriftelijk op en laat die in het contract opnemen.",
 "Pozwolenie na budowę zostało wydane, co deweloper potwierdził we wrześniu 2026 roku. Wcześniejszy dokument informacyjny samego dewelopera odnotowywał pozwolenie jako złożone 27 grudnia 2024 roku z przewidywaną datą uzyskania 30 kwietnia 2026 roku, a etap prac jako projekt, nie budowę. Odbiór wskazano na drugi kwartał 2029 roku. Nueva Living prosi o datę odbioru na piśmie i wpisuje ją do umowy.",
 "Byggetillatelsen er gitt, noe utbyggeren bekreftet i september 2026. Utbyggerens eget opplysningsdokument, utstedt tidligere, førte opp tillatelsen som søkt 27. desember 2024 med forventet innvilgelse 30. april 2026, og byggetrinnet som prosjektering og ikke bygging. Ferdigstillelse er oppgitt til andre kvartal 2029. Nueva Living ber om overtakelsesdatoen skriftlig og får den inn i kontrakten.",
 "Bygglovet är beviljat, vilket byggherren bekräftade i september 2026. Byggherrens eget informationsdokument, utfärdat tidigare, angav lovet som ansökt den 27 december 2024 med förväntat beviljande den 30 april 2026, och byggskedet som projektering och inte byggnation. Färdigställandet anges till andra kvartalet 2029. Nueva Living begär tillträdesdatumet skriftligt och skriver in det i avtalet.")

a("EUR 20,000 + VAT",
 "20.000 EUR + IVA","20 000 EUR + TVA","20.000 EUR + MwSt.","20 000 EUR + НДС","20,000 EUR + ضريبة القيمة المضافة",
 "20.000 EUR + btw","20 000 EUR + VAT","20 000 EUR + mva.","20 000 EUR + moms")

a("EUR 22,000 on signing",
 "22.000 EUR a la firma","22 000 EUR à la signature","22.000 EUR bei Unterzeichnung","22 000 EUR при подписании",
 "22,000 EUR عند التوقيع","22.000 EUR bij ondertekening","22 000 EUR przy podpisaniu","22 000 EUR ved signering","22 000 EUR vid undertecknandet")

a("60 days after reservation, less the reservation",
 "60 días después de la reserva, menos el importe de la reserva",
 "60 jours après la réservation, déduction faite de celle-ci",
 "60 Tage nach der Reservierung, abzüglich der Reservierungssumme",
 "Через 60 дней после бронирования, за вычетом суммы брони",
 "بعد 60 يوماً من الحجز، ناقص مبلغ الحجز",
 "60 dagen na de reservering, minus het reserveringsbedrag",
 "60 dni po rezerwacji, pomniejszone o kwotę rezerwacji",
 "60 dager etter reservasjonen, fratrukket reservasjonsbeløpet",
 "60 dagar efter bokningen, minus bokningsbeloppet")

a("After 12 Months",
 "A los 12 meses","Au bout de 12 mois","Nach 12 Monaten","Через 12 месяцев","بعد 12 شهراً",
 "Na 12 maanden","Po 12 miesiącach","Etter 12 måneder","Efter 12 månader")

a("After 18 Months",
 "A los 18 meses","Au bout de 18 mois","Nach 18 Monaten","Через 18 месяцев","بعد 18 شهراً",
 "Na 18 maanden","Po 18 miesiącach","Etter 18 måneder","Efter 18 månader")

a("Measured from the private contract, not a build milestone",
 "Contado desde el contrato privado, no desde un hito de obra",
 "Compté à partir du contrat privé, non d'une étape de chantier",
 "Gerechnet ab dem privaten Kaufvertrag, nicht ab einem Bauabschnitt",
 "Отсчитывается от частного договора, а не от этапа строительства",
 "يُحتسب من تاريخ العقد الخاص لا من مرحلة إنشائية",
 "Gerekend vanaf het onderhandse contract, niet vanaf een bouwfase",
 "Liczone od umowy przedwstępnej, nie od etapu budowy",
 "Regnet fra den private kontrakten, ikke fra et byggetrinn",
 "Räknat från det privata avtalet, inte från en byggetapp")

a("Paid at notary signing on delivery of keys",
 "Se paga en la firma ante notario, con la entrega de llaves",
 "Réglé à la signature notariée, à la remise des clés",
 "Zahlbar bei der notariellen Beurkundung mit der Schlüsselübergabe",
 "Оплачивается при подписании у нотариуса, при передаче ключей",
 "يُدفع عند التوقيع لدى الموثّق مع تسليم المفاتيح",
 "Te voldoen bij de notariële akte, bij de sleuteloverdracht",
 "Płatne przy akcie notarialnym, przy wydaniu kluczy",
 "Betales ved signering hos notaren, ved nøkkeloverlevering",
 "Betalas vid undertecknandet hos notarien, vid nyckelöverlämningen")

a("Sixty per cent falls due only at the notary, which is a lighter schedule during construction than most schemes on this coast ask for. The two middle instalments run on fixed dates from the private contract rather than on build milestones. The developer states that payments made on account are secured by bank guarantee, and that the deferral carries no interest. Nueva Living confirms both in the reservation agreement before you commit.",
 "El sesenta por ciento no vence hasta el notario, lo que supone menos desembolso durante la obra que el que piden la mayoría de las promociones de esta costa. Los dos plazos intermedios corren en fechas fijas desde el contrato privado y no según hitos de obra. El promotor declara que las cantidades entregadas a cuenta están cubiertas por aval bancario y que el aplazamiento no devenga intereses. Nueva Living confirma ambos extremos en el documento de reserva antes de que usted se comprometa.",
 "Soixante pour cent ne sont exigibles qu'au notaire, ce qui représente un effort moindre pendant le chantier que ce que demandent la plupart des programmes de cette côte. Les deux échéances intermédiaires courent à dates fixes depuis le contrat privé et non selon l'avancement des travaux. Le promoteur déclare que les sommes versées sont couvertes par une garantie bancaire et que le différé ne porte pas intérêt. Nueva Living vérifie ces deux points dans le document de réservation avant tout engagement.",
 "Sechzig Prozent werden erst beim Notar fällig, was während der Bauzeit weniger bindet als bei den meisten Projekten an dieser Küste. Die beiden mittleren Raten laufen zu festen Terminen ab dem privaten Kaufvertrag, nicht nach Baufortschritt. Der Bauträger erklärt, dass geleistete Anzahlungen durch eine Bankbürgschaft gesichert sind und die Stundung zinsfrei ist. Nueva Living lässt sich beides in der Reservierungsvereinbarung bestätigen, bevor Sie sich binden.",
 "Шестьдесят процентов подлежат оплате только у нотариуса — это меньшая нагрузка во время стройки, чем требует большинство проектов на этом побережье. Два промежуточных платежа привязаны к фиксированным датам от частного договора, а не к этапам строительства. Застройщик заявляет, что внесённые суммы обеспечены банковской гарантией и что рассрочка беспроцентная. Nueva Living подтверждает и то и другое в соглашении о бронировании, прежде чем вы возьмёте на себя обязательства.",
 "لا تُستحقّ نسبة الستين بالمئة إلا عند الموثّق، وهو التزام أخفّ أثناء البناء ممّا تطلبه معظم المشاريع على هذا الساحل. القسطان الأوسطان يسريان في تواريخ ثابتة من العقد الخاص لا وفق مراحل البناء. يذكر المطوّر أن المبالغ المدفوعة على الحساب مضمونة بكفالة مصرفية وأن التأجيل بلا فائدة. تتحقّق Nueva Living من الأمرين في اتفاق الحجز قبل أن تلتزم.",
 "Zestig procent is pas bij de notaris verschuldigd, wat tijdens de bouw minder vastlegt dan de meeste projecten aan deze kust vragen. De twee tussentijdse termijnen lopen op vaste data vanaf het onderhandse contract en niet op bouwfasen. De ontwikkelaar verklaart dat betaalde voorschotten door een bankgarantie zijn gedekt en dat het uitstel renteloos is. Nueva Living bevestigt beide in de reserveringsovereenkomst voordat u zich vastlegt.",
 "Sześćdziesiąt procent staje się wymagalne dopiero u notariusza, co w trakcie budowy angażuje mniej kapitału niż wymaga większość inwestycji na tym wybrzeżu. Dwie środkowe raty biegną w stałych terminach od umowy przedwstępnej, a nie według etapów budowy. Deweloper oświadcza, że wpłacone kwoty są zabezpieczone gwarancją bankową, a odroczenie jest nieoprocentowane. Nueva Living potwierdza jedno i drugie w umowie rezerwacyjnej, zanim Państwo się zobowiążą.",
 "Seksti prosent forfaller først hos notaren, noe som binder mindre kapital under byggingen enn de fleste prosjektene på denne kysten krever. De to midtre avdragene løper på faste datoer fra den private kontrakten, ikke etter byggetrinn. Utbyggeren oppgir at innbetalte beløp er sikret med bankgaranti, og at utsettelsen er rentefri. Nueva Living bekrefter begge deler i reservasjonsavtalen før du forplikter deg.",
 "Sextio procent förfaller först hos notarien, vilket binder mindre kapital under byggtiden än vad de flesta projekt på den här kusten kräver. De två mellersta delbetalningarna löper på fasta datum från det privata avtalet, inte efter byggetapper. Byggherren uppger att inbetalda belopp är säkrade med bankgaranti och att uppskovet är räntefritt. Nueva Living bekräftar båda delarna i bokningsavtalet innan ni binder er.")

a("A hillside site handled as a piece of engineering rather than a view, and a payment schedule that leaves most of the money until the keys.",
 "Una parcela en ladera resuelta como un problema de ingeniería y no como una vista, y un calendario de pagos que deja la mayor parte del dinero para la entrega de llaves.",
 "Un terrain en pente traité comme un problème d'ingénierie plutôt que comme une vue, et un échéancier qui laisse l'essentiel du prix à la remise des clés.",
 "Ein Hanggrundstück, das als Ingenieuraufgabe und nicht als Aussicht behandelt wurde, und ein Zahlungsplan, der den größten Teil des Geldes bis zur Schlüsselübergabe stehen lässt.",
 "Склон, решённый как инженерная задача, а не как вид, и график платежей, оставляющий большую часть суммы до передачи ключей.",
 "موقع على منحدر عولج بوصفه مسألة هندسية لا مجرّد إطلالة، وجدول سداد يترك معظم المبلغ حتى تسليم المفاتيح.",
 "Een hellend terrein dat als ingenieursopgave is aangepakt in plaats van als uitzicht, en een betalingsschema dat het grootste deel van het geld tot de sleuteloverdracht laat staan.",
 "Działka na zboczu potraktowana jako zadanie inżynierskie, a nie jako widok, oraz harmonogram płatności, który zostawia większość kwoty na moment wydania kluczy.",
 "En tomt i skråning håndtert som en ingeniøroppgave snarere enn en utsikt, og en betalingsplan som lar mesteparten av pengene stå til nøkkeloverleveringen.",
 "En sluttande tomt som hanterats som en ingenjörsuppgift snarare än som en utsikt, och en betalningsplan som låter merparten av pengarna stå till nyckelöverlämningen.")

a("Every one of the eighty homes faces the sea, because the blocks step rather than sit level.",
 "Las ochenta viviendas miran al mar, porque los bloques se escalonan en lugar de estar al mismo nivel.",
 "Les quatre-vingts logements font face à la mer, parce que les blocs sont échelonnés et non de niveau.",
 "Alle achtzig Wohnungen sind zum Meer ausgerichtet, weil die Blöcke gestaffelt stehen statt auf gleicher Höhe.",
 "Все восемьдесят квартир обращены к морю, потому что корпуса стоят уступами, а не на одном уровне.",
 "كل المساكن الثمانين مطلّة على البحر، لأن المباني متدرّجة لا على مستوى واحد.",
 "Alle tachtig woningen kijken uit op zee, doordat de blokken getrapt staan in plaats van op gelijke hoogte.",
 "Wszystkie osiemdziesiąt mieszkań jest zwróconych ku morzu, ponieważ budynki są uskokowe, a nie na jednym poziomie.",
 "Alle de åtti boligene vender mot sjøen, fordi blokkene er trappet og ikke ligger på samme nivå.",
 "Alla åttio bostäder vetter mot havet, eftersom huskropparna trappar i stället för att ligga i nivå.")

a("Sixty per cent of the price falls at the notary, so less capital is committed during the build than most schemes here require.",
 "El sesenta por ciento del precio se paga ante notario, por lo que se compromete menos capital durante la obra que en la mayoría de las promociones de la zona.",
 "Soixante pour cent du prix se règlent chez le notaire, ce qui immobilise moins de capital pendant le chantier que la plupart des programmes du secteur.",
 "Sechzig Prozent des Preises fallen beim Notar an, sodass während der Bauzeit weniger Kapital gebunden ist als bei den meisten Projekten hier.",
 "Шестьдесят процентов цены платятся у нотариуса, поэтому во время стройки задействовано меньше капитала, чем требует большинство местных проектов.",
 "ستون بالمئة من السعر تُدفع لدى الموثّق، فيُرتبط رأس مال أقل أثناء البناء ممّا تتطلّبه معظم المشاريع هنا.",
 "Zestig procent van de prijs valt bij de notaris, waardoor er tijdens de bouw minder kapitaal vastligt dan de meeste projecten hier vragen.",
 "Sześćdziesiąt procent ceny przypada na akt notarialny, więc w trakcie budowy angażuje się mniej kapitału niż wymaga większość tutejszych inwestycji.",
 "Seksti prosent av prisen forfaller hos notaren, så mindre kapital er bundet under byggingen enn de fleste prosjektene her krever.",
 "Sextio procent av priset faller hos notarien, så mindre kapital binds under byggtiden än vad de flesta projekt här kräver.")

a("Two parking spaces and a storeroom come with every apartment at no extra cost, which is unusual at this price.",
 "Cada apartamento incluye dos plazas de garaje y un trastero sin coste adicional, algo poco habitual en este rango de precio.",
 "Chaque appartement comprend deux places de parking et un débarras sans supplément, ce qui est rare dans cette gamme de prix.",
 "Zu jeder Wohnung gehören zwei Stellplätze und ein Abstellraum ohne Aufpreis, was in dieser Preisklasse ungewöhnlich ist.",
 "К каждой квартире идут два машиноместа и кладовая без доплаты, что необычно для этой цены.",
 "تأتي كل شقة بموقفي سيارات ومخزن دون تكلفة إضافية، وهو أمر غير معتاد في هذه الفئة السعرية.",
 "Bij elk appartement horen twee parkeerplaatsen en een berging zonder meerprijs, wat in deze prijsklasse ongebruikelijk is.",
 "Do każdego apartamentu należą dwa miejsca postojowe i komórka bez dopłaty, co jest nietypowe w tym przedziale cenowym.",
 "Hver leilighet får to parkeringsplasser og en bod uten tillegg, noe som er uvanlig i dette prissjiktet.",
 "Varje lägenhet får två parkeringsplatser och ett förråd utan extra kostnad, vilket är ovanligt i den här prisklassen.")

a("Payments on account are secured by bank guarantee, as Spanish law requires of off-plan sales.",
 "Las cantidades entregadas a cuenta están garantizadas mediante aval bancario, como exige la ley española en la venta sobre plano.",
 "Les sommes versées d'avance sont couvertes par une garantie bancaire, comme la loi espagnole l'impose pour la vente sur plan.",
 "Anzahlungen sind durch eine Bankbürgschaft gesichert, wie es das spanische Recht beim Kauf vom Plan verlangt.",
 "Внесённые суммы обеспечены банковской гарантией, как того требует испанский закон при продаже на стадии строительства.",
 "المبالغ المدفوعة على الحساب مضمونة بكفالة مصرفية، وفق ما يفرضه القانون الإسباني على البيع على الخريطة.",
 "Aanbetalingen zijn gedekt door een bankgarantie, zoals de Spaanse wet bij koop op plan voorschrijft.",
 "Wpłacone zaliczki są zabezpieczone gwarancją bankową, czego prawo hiszpańskie wymaga przy sprzedaży z planu.",
 "Innbetalte beløp er sikret med bankgaranti, slik spansk lov krever ved kjøp på tegning.",
 "Inbetalda belopp är säkrade med bankgaranti, vilket spansk lag kräver vid köp på ritning.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
