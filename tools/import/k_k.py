# -*- coding: utf-8 -*-
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("How to think about <em>it</em>","Cómo <em>valorarlo</em>","Comment <em>l'évaluer</em>","Wie man <em>es einordnet</em>",
 "Как <em>это оценивать</em>","كيف <em>تقيّمه</em>","Hoe je het <em>beoordeelt</em>","Jak to <em>oceniać</em>",
 "Hvordan <em>vurdere det</em>","Hur man <em>bedömer det</em>")
a("Points worth weighing before you reserve, and the questions Nueva Living asks on your behalf.",
 "Puntos que conviene sopesar antes de reservar, y las preguntas que Nueva Living hace por usted.",
 "Des points à peser avant de réserver, et les questions que Nueva Living pose pour vous.",
 "Punkte, die vor einer Reservierung abzuwägen sind, und die Fragen, die Nueva Living für Sie stellt.",
 "О чём стоит подумать до бронирования и какие вопросы Nueva Living задаёт от вашего имени.",
 "نقاط تستحق التفكير قبل الحجز، والأسئلة التي تطرحها Nueva Living نيابةً عنك.",
 "Punten om te wegen voordat u reserveert, en de vragen die Nueva Living namens u stelt.",
 "Kwestie warte rozważenia przed rezerwacją oraz pytania, które Nueva Living zadaje w Państwa imieniu.",
 "Punkter verdt å veie før reservasjon, og spørsmålene Nueva Living stiller på dine vegne.",
 "Punkter värda att väga före reservation, och frågorna Nueva Living ställer för din räkning.")
a("Completion in 2029","Entrega en 2029","Livraison en 2029","Fertigstellung 2029","Сдача в 2029 году",
 "الإنجاز في 2029","Oplevering in 2029","Zakończenie w 2029","Ferdigstilling i 2029","Färdigställande 2029")
a("Three years out. The date belongs in the contract, not in a brochure.",
 "A tres años vista. La fecha debe estar en el contrato, no en un folleto.",
 "À trois ans. La date a sa place dans le contrat, pas dans une brochure.",
 "Drei Jahre hin. Der Termin gehört in den Vertrag, nicht in eine Broschüre.",
 "До неё три года. Дата должна быть в договоре, а не в буклете.",
 "على بعد ثلاث سنوات. التاريخ مكانه العقد لا الكتيّب.",
 "Drie jaar weg. De datum hoort in het contract, niet in een brochure.",
 "Za trzy lata. Data powinna znaleźć się w umowie, a nie w folderze.",
 "Tre år fram i tid. Datoen hører hjemme i kontrakten, ikke i en brosjyre.",
 "Tre år bort. Datumet hör hemma i avtalet, inte i en broschyr.")
a("Running costs","Costes de mantenimiento","Charges courantes","Laufende Kosten","Текущие расходы",
 "التكاليف الجارية","Vaste lasten","Koszty utrzymania","Løpende kostnader","Löpande kostnader")
a("A scheme with two pools, a gym and courts carries a community fee to match. Ask for the budget.",
 "Una promoción con dos piscinas, gimnasio y pistas conlleva una cuota de comunidad acorde. Pida el presupuesto.",
 "Un programme avec deux piscines, une salle de sport et des terrains implique des charges à l'avenant. Demandez le budget.",
 "Eine Anlage mit zwei Pools, Fitnessraum und Plätzen bringt ein entsprechendes Hausgeld mit sich. Fragen Sie nach dem Wirtschaftsplan.",
 "Комплекс с двумя бассейнами, залом и кортами предполагает соответствующий взнос на содержание. Запросите смету.",
 "مشروع بمسبحين وصالة رياضية وملاعب يحمل رسوم خدمات بما يوازيه. اطلب الميزانية.",
 "Een project met twee zwembaden, een fitnessruimte en banen brengt een bijpassende servicekost mee. Vraag om de begroting.",
 "Inwestycja z dwoma basenami, siłownią i kortami wiąże się z odpowiednim czynszem wspólnoty. Poproś o budżet.",
 "Et prosjekt med to bassenger, treningsrom og baner bærer en fellesutgift deretter. Be om budsjettet.",
 "Ett projekt med två pooler, gym och banor för med sig en samfällighetsavgift därefter. Be om budgeten.")
a("What the area figure means","Qué significa la superficie indicada","Ce que signifie la surface annoncée",
 "Was die Flächenangabe bedeutet","Что означает указанная площадь","ماذا تعني المساحة المذكورة",
 "Wat de oppervlakte betekent","Co oznacza podana powierzchnia","Hva arealtallet betyr","Vad ytangivelsen betyder")
a("The built area includes a share of the common parts. Compare useful areas, not headline ones.",
 "La superficie construida incluye una parte proporcional de elementos comunes. Compare superficies útiles, no las de titular.",
 "La surface construite inclut une quote-part des parties communes. Comparez les surfaces utiles, pas celles affichées.",
 "Die Bruttofläche enthält einen Anteil am Gemeinschaftseigentum. Vergleichen Sie Nutzflächen, nicht Schlagzeilenflächen.",
 "Построенная площадь включает долю мест общего пользования. Сравнивайте полезные площади, а не заголовочные.",
 "المساحة المبنية تشمل حصة من الأجزاء المشتركة. قارن المساحات المفيدة لا المعلنة.",
 "De bouwoppervlakte omvat een aandeel in de gemeenschappelijke delen. Vergelijk nuttige oppervlakten, niet de genoemde.",
 "Powierzchnia zabudowana obejmuje udział w częściach wspólnych. Porównuj powierzchnie użytkowe, nie te z nagłówka.",
 "Bruttoarealet inkluderer en andel av fellesarealene. Sammenlign nyttbare arealer, ikke overskriftstallene.",
 "Byggytan inkluderar en andel av de gemensamma delarna. Jämför nyttiga ytor, inte rubrikytor.")
a("Early-phase choice","Elección en fase inicial","Le choix en début de programme","Auswahl in der frühen Phase",
 "Выбор на раннем этапе","الاختيار في المرحلة المبكرة","Keuze in een vroege fase","Wybór na wczesnym etapie",
 "Valg i tidlig fase","Val i tidigt skede")
a("Ten homes across three blocks means a real choice of aspect and floor, which narrows as it sells.",
 "Diez viviendas en tres bloques significan una elección real de orientación y planta, que se estrecha a medida que se vende.",
 "Dix logements répartis sur trois immeubles offrent un vrai choix d'exposition et d'étage, qui se réduit à mesure des ventes.",
 "Zehn Wohnungen in drei Gebäuden bedeuten eine echte Wahl bei Ausrichtung und Geschoss, die mit dem Verkauf schrumpft.",
 "Десять квартир в трёх корпусах дают реальный выбор ориентации и этажа, который сужается по мере продаж.",
 "عشرة منازل في ثلاثة مبانٍ تعني خياراً حقيقياً في الاتجاه والطابق، يضيق مع تقدم البيع.",
 "Tien woningen verdeeld over drie gebouwen geven een echte keuze in oriëntatie en verdieping, die kleiner wordt naarmate er verkocht wordt.",
 "Dziesięć mieszkań w trzech budynkach daje realny wybór ekspozycji i piętra, który zawęża się wraz ze sprzedażą.",
 "Ti boliger fordelt på tre bygg gir et reelt valg av retning og etasje, som snevres inn etter hvert som det selges.",
 "Tio bostäder i tre hus ger ett verkligt val av läge och våning, som krymper i takt med försäljningen.")
a("Before Nueva Living puts a scheme in front of you.","Antes de que Nueva Living le presente una promoción.",
 "Avant que Nueva Living ne vous présente un programme.","Bevor Nueva Living Ihnen eine Anlage vorstellt.",
 "Прежде чем Nueva Living предложит вам комплекс.","قبل أن تعرض Nueva Living أي مشروع عليك.",
 "Voordat Nueva Living u een project voorlegt.","Zanim Nueva Living przedstawi Państwu inwestycję.",
 "Før Nueva Living legger et prosjekt fram for deg.","Innan Nueva Living lägger fram ett projekt.")
a("That the building licence is granted before any money moves.",
 "Que la licencia de obra esté concedida antes de que se mueva ningún dinero.",
 "Que le permis de construire soit accordé avant tout mouvement d'argent.",
 "Dass die Baugenehmigung erteilt ist, bevor Geld fließt.",
 "Что разрешение на строительство получено до любых денежных переводов.",
 "أن يكون ترخيص البناء ممنوحاً قبل تحويل أي مبلغ.",
 "Dat de bouwvergunning is verleend voordat er geld wordt overgemaakt.",
 "Że pozwolenie na budowę zostało wydane, zanim pojawią się jakiekolwiek płatności.",
 "At byggetillatelsen er gitt før noen penger flyttes.",
 "Att bygglovet är beviljat innan några pengar flyttas.")
a("The bank guarantee","El aval bancario","La garantie bancaire","Die Bankbürgschaft","Банковская гарантия",
 "الضمان البنكي","De bankgarantie","Gwarancja bankowa","Bankgarantien","Bankgarantin")
a("That every payment is covered by a bank guarantee or insurance policy, as the law requires.",
 "Que cada pago esté cubierto por un aval bancario o una póliza de seguro, como exige la ley.",
 "Que chaque versement soit couvert par une garantie bancaire ou une police d'assurance, comme la loi l'exige.",
 "Dass jede Zahlung durch eine Bankbürgschaft oder Versicherungspolice gedeckt ist, wie das Gesetz es verlangt.",
 "Что каждый платёж покрыт банковской гарантией или страховым полисом, как требует закон.",
 "أن تكون كل دفعة مغطاة بضمان بنكي أو وثيقة تأمين، كما يقتضي القانون.",
 "Dat elke betaling is gedekt door een bankgarantie of verzekeringspolis, zoals de wet vereist.",
 "Że każda wpłata jest objęta gwarancją bankową lub polisą ubezpieczeniową, zgodnie z wymogiem prawa.",
 "At hver innbetaling er dekket av bankgaranti eller forsikringspolise, slik loven krever.",
 "Att varje betalning täcks av bankgaranti eller försäkring, som lagen kräver.")
a("The specification","La memoria de calidades","Le descriptif technique","Die Baubeschreibung",
 "Спецификация","مواصفات البناء","Het lastenboek","Specyfikacja techniczna","Beskrivelsen","Byggbeskrivningen")
a("That what is promised in the brochure is what is written in the specification.",
 "Que lo prometido en el folleto sea lo que figura en la memoria de calidades.",
 "Que ce qui est promis dans la brochure soit ce qui figure au descriptif technique.",
 "Dass das in der Broschüre Versprochene in der Baubeschreibung steht.",
 "Что обещанное в буклете записано в спецификации.",
 "أن يكون ما وُعد به في الكتيّب هو ما كُتب في مواصفات البناء.",
 "Dat wat in de brochure wordt beloofd, ook in het lastenboek staat.",
 "Że to, co obiecano w folderze, znajduje się w specyfikacji technicznej.",
 "At det som loves i brosjyren, står i beskrivelsen.",
 "Att det som utlovas i broschyren står i byggbeskrivningen.")
a("The date","La fecha","La date","Der Termin","Дата","التاريخ","De datum","Data","Datoen","Datumet")
a("That the completion date is contractual rather than indicative.",
 "Que la fecha de entrega sea contractual y no orientativa.",
 "Que la date de livraison soit contractuelle et non indicative.",
 "Dass der Fertigstellungstermin vertraglich und nicht unverbindlich ist.",
 "Что срок сдачи является договорным, а не ориентировочным.",
 "أن يكون تاريخ الإنجاز تعاقدياً لا إرشادياً.",
 "Dat de opleverdatum contractueel is en niet indicatief.",
 "Że termin zakończenia jest umowny, a nie orientacyjny.",
 "At ferdigstillelsesdatoen er kontraktfestet og ikke veiledende.",
 "Att färdigställandedatumet är avtalat och inte vägledande.")
json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
