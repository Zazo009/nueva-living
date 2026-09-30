# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 6: investment and trust cards.
# scaffold.py never listed these -- it mirrors a sibling's overlay shape, and
# the sibling has no investment/trustDossier cards, so they were invisible.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Tax is not in the price","El precio no incluye impuestos","Le prix s'entend hors taxes","Der Preis enthält keine Steuern",
 "Налоги в цену не входят","السعر لا يشمل الضرائب","De prijs is exclusief belasting","Cena nie zawiera podatku",
 "Prisen er uten skatt","Priset är exklusive skatt")

a("The price list is quoted before tax. Ten per cent VAT and 1.20 per cent stamp duty add roughly sixty thousand euros to the cheapest apartment and a hundred and eighteen thousand to the penthouse, before notary and registry fees.",
 "La lista de precios se expresa antes de impuestos. El IVA del diez por ciento y el impuesto de actos jurídicos documentados del 1,20 por ciento suman unos sesenta mil euros al apartamento más barato y ciento dieciocho mil al ático, antes de notaría y registro.",
 "La liste de prix s'entend hors taxes. La TVA à dix pour cent et le droit de timbre à 1,20 pour cent ajoutent environ soixante mille euros à l'appartement le moins cher et cent dix-huit mille au penthouse, avant frais de notaire et d'enregistrement.",
 "Die Preisliste versteht sich ohne Steuern. Zehn Prozent Mehrwertsteuer und 1,20 Prozent Stempelsteuer kommen bei der günstigsten Wohnung auf rund sechzigtausend Euro und beim Penthouse auf hundertachtzehntausend, vor Notar- und Grundbuchkosten.",
 "Прайс-лист указан без налогов. НДС десять процентов и гербовый сбор 1,20 процента добавляют около шестидесяти тысяч евро к самой дешёвой квартире и сто восемнадцать тысяч к пентхаусу, до нотариуса и регистрации.",
 "قائمة الأسعار قبل الضريبة. تضيف ضريبة القيمة المضافة بنسبة عشرة بالمئة ورسم الدمغة بنسبة 1.20 بالمئة نحو ستين ألف يورو إلى أرخص شقة ومئة وثمانية عشر ألفاً إلى البنتهاوس، قبل أتعاب التوثيق والتسجيل.",
 "De prijslijst is exclusief belasting. Tien procent btw en 1,20 procent overdrachtsbelasting leggen ongeveer zestigduizend euro bij op het goedkoopste appartement en honderdachttienduizend op het penthouse, vóór notaris- en kadasterkosten.",
 "Cennik podano przed opodatkowaniem. Dziesięcioprocentowy VAT i 1,20-procentowy podatek od czynności cywilnoprawnych dokładają około sześćdziesięciu tysięcy euro do najtańszego apartamentu i sto osiemnaście tysięcy do penthouse'u, przed opłatami notarialnymi i wieczystoksięgowymi.",
 "Prislisten er oppgitt før skatt. Ti prosent merverdiavgift og 1,20 prosent dokumentavgift legger rundt seksti tusen euro på den rimeligste leiligheten og hundre og atten tusen på toppleiligheten, før notar- og tinglysingsgebyrer.",
 "Prislistan anges före skatt. Tio procents moms och 1,20 procents stämpelskatt lägger cirka sextiotusen euro på den billigaste lägenheten och hundraarton tusen på takvåningen, före notarie- och registreringsavgifter.")

a("Delivery is two and a half years out","La entrega está a dos años y medio","La livraison est dans deux ans et demi",
 "Die Übergabe liegt zweieinhalb Jahre entfernt","До сдачи два с половиной года","التسليم بعد عامين ونصف",
 "De oplevering ligt tweeënhalf jaar weg","Do odbioru dwa i pół roku","Overtakelsen er to og et halvt år fram","Tillträdet ligger två och ett halvt år bort")

a("The second quarter of 2029 is a long horizon. Ask what the contract says happens if it slips, and whether the date is contractual or indicative.",
 "El segundo trimestre de 2029 es un horizonte largo. Pregunte qué dice el contrato si se retrasa, y si la fecha es contractual o meramente orientativa.",
 "Le deuxième trimestre 2029 est un horizon lointain. Demandez ce que prévoit le contrat en cas de retard, et si la date est contractuelle ou seulement indicative.",
 "Das zweite Quartal 2029 ist ein weiter Horizont. Fragen Sie, was der Vertrag bei Verzug vorsieht und ob der Termin vertraglich bindend oder nur indikativ ist.",
 "Второй квартал 2029 года — далёкий горизонт. Спросите, что предусматривает договор при задержке и является ли дата договорной или лишь ориентировочной.",
 "الربع الثاني من 2029 أفق بعيد. اسأل عمّا ينصّ عليه العقد في حال التأخير، وهل التاريخ تعاقدي أم إرشادي فقط.",
 "Het tweede kwartaal van 2029 is een verre horizon. Vraag wat het contract bepaalt bij vertraging, en of de datum contractueel of slechts indicatief is.",
 "Drugi kwartał 2029 roku to odległy horyzont. Prosimy zapytać, co umowa przewiduje w razie opóźnienia i czy data jest umowna, czy tylko orientacyjna.",
 "Andre kvartal 2029 er en lang horisont. Spør hva kontrakten sier ved forsinkelse, og om datoen er kontraktfestet eller bare veiledende.",
 "Andra kvartalet 2029 är en lång horisont. Fråga vad avtalet säger vid försening, och om datumet är avtalat eller endast vägledande.")

a("Twenty of eighty are released","Veinte de ochenta están a la venta","Vingt sur quatre-vingts sont mis en vente",
 "Zwanzig von achtzig sind freigegeben","Двадцать из восьмидесяти выведены в продажу","عشرون من ثمانين مطروحة",
 "Twintig van de tachtig zijn vrijgegeven","Dwadzieścia z osiemdziesięciu w sprzedaży","Tjue av åtti er lagt ut","Tjugo av åttio är släppta")

a("The remaining sixty homes will be priced later. Early buyers take the build risk; later buyers pay the later price. Which of those is the better side depends on the market, not on the brochure.",
 "Las sesenta viviendas restantes se pondrán a precio más adelante. Quien compra pronto asume el riesgo de obra; quien compra después paga el precio posterior. Cuál de las dos posiciones es mejor depende del mercado, no del folleto.",
 "Les soixante logements restants seront tarifés plus tard. Celui qui achète tôt prend le risque de chantier ; celui qui achète plus tard paie le prix plus tard. Savoir quel côté est le meilleur dépend du marché, pas de la brochure.",
 "Die übrigen sechzig Wohnungen werden später bepreist. Wer früh kauft, trägt das Baurisiko; wer später kauft, zahlt den späteren Preis. Welche Seite die bessere ist, entscheidet der Markt und nicht die Broschüre.",
 "Оставшиеся шестьдесят квартир получат цену позже. Кто покупает раньше, берёт на себя риск стройки; кто позже — платит более позднюю цену. Какая из сторон выгоднее, решает рынок, а не буклет.",
 "ستُسعَّر المساكن الستون المتبقية لاحقاً. من يشتري مبكراً يتحمّل مخاطر البناء، ومن يشتري لاحقاً يدفع السعر اللاحق. وأيّ الجانبين أفضل يحدّده السوق لا الكتيّب.",
 "De overige zestig woningen krijgen later een prijs. Wie vroeg koopt draagt het bouwrisico; wie later koopt betaalt de latere prijs. Welke van beide de betere kant is, bepaalt de markt en niet de brochure.",
 "Pozostałe sześćdziesiąt mieszkań zostanie wycenione później. Kto kupuje wcześnie, bierze na siebie ryzyko budowy; kto później, płaci późniejszą cenę. Która strona jest lepsza, rozstrzyga rynek, a nie folder.",
 "De resterende seksti boligene prises senere. Den som kjøper tidlig tar byggerisikoen; den som kjøper senere betaler den senere prisen. Hvilken side som er best, avgjøres av markedet og ikke av brosjyren.",
 "De återstående sextio bostäderna prissätts senare. Den som köper tidigt tar byggrisken; den som köper senare betalar det senare priset. Vilken sida som är bäst avgörs av marknaden, inte av broschyren.")

a("The middle instalments are date-driven","Los plazos intermedios van por fecha","Les échéances intermédiaires sont calées sur des dates",
 "Die mittleren Raten laufen nach Datum","Промежуточные платежи привязаны к датам","الأقساط الوسطى مرتبطة بتواريخ",
 "De tussentijdse termijnen lopen op datum","Raty środkowe są terminowe","De midtre avdragene styres av dato","De mellersta delbetalningarna styrs av datum")

a("Ten per cent at twelve months and ten per cent at eighteen months are counted from the private contract, not from construction progress. You pay them whether or not the build is on schedule.",
 "El diez por ciento a los doce meses y el diez por ciento a los dieciocho se cuentan desde el contrato privado, no desde el avance de obra. Se pagan vaya la obra en plazo o no.",
 "Les dix pour cent à douze mois et les dix pour cent à dix-huit mois sont comptés à partir du contrat privé, non de l'avancement des travaux. Vous les réglez que le chantier soit à l'heure ou non.",
 "Die zehn Prozent nach zwölf Monaten und die zehn Prozent nach achtzehn Monaten zählen ab dem privaten Kaufvertrag, nicht ab dem Baufortschritt. Sie werden fällig, ob der Bau im Plan liegt oder nicht.",
 "Десять процентов через двенадцать месяцев и десять через восемнадцать отсчитываются от частного договора, а не от хода строительства. Вы платите их независимо от того, идёт ли стройка по графику.",
 "تُحتسب نسبة العشرة بالمئة عند اثني عشر شهراً والعشرة بالمئة عند ثمانية عشر شهراً من تاريخ العقد الخاص لا من تقدّم البناء. وتدفعها سواء سار البناء وفق الجدول أم لا.",
 "De tien procent na twaalf maanden en de tien procent na achttien maanden tellen vanaf het onderhandse contract, niet vanaf de bouwvoortgang. U betaalt ze of de bouw nu op schema ligt of niet.",
 "Dziesięć procent po dwunastu miesiącach i dziesięć po osiemnastu liczy się od umowy przedwstępnej, a nie od postępu budowy. Płaci się je niezależnie od tego, czy budowa idzie zgodnie z harmonogramem.",
 "De ti prosentene etter tolv måneder og de ti etter atten regnes fra den private kontrakten, ikke fra byggefremdriften. Du betaler dem enten byggingen er i rute eller ikke.",
 "De tio procenten efter tolv månader och de tio efter arton räknas från det privata avtalet, inte från byggets framdrift. Ni betalar dem oavsett om bygget håller tidplanen eller inte.")

a("The licence","La licencia","Le permis","Die Genehmigung","Разрешение","الرخصة","De vergunning","Pozwolenie","Tillatelsen","Bygglovet")

a("Granted, confirmed by the developer in September 2026. The written disclosure document predates that and still records it as applied for, so we ask for the grant in writing.",
 "Concedida, según confirmó el promotor en septiembre de 2026. El documento informativo escrito es anterior y todavía la registra como solicitada, así que pedimos la concesión por escrito.",
 "Accordé, confirmé par le promoteur en septembre 2026. Le document d'information écrit lui est antérieur et le mentionne encore comme demandé ; nous réclamons donc l'arrêté par écrit.",
 "Erteilt, vom Bauträger im September 2026 bestätigt. Das schriftliche Informationsdokument stammt aus der Zeit davor und führt sie weiterhin als beantragt, deshalb verlangen wir die Erteilung schriftlich.",
 "Получено, подтверждено застройщиком в сентябре 2026 года. Письменный информационный документ старше и по-прежнему указывает его как запрошенное, поэтому мы запрашиваем сам акт в письменном виде.",
 "ممنوحة، أكّدها المطوّر في سبتمبر 2026. وثيقة الإفصاح المكتوبة أقدم من ذلك وما زالت تسجّلها على أنها مُقدَّمة، لذا نطلب قرار المنح كتابةً.",
 "Verleend, in september 2026 door de ontwikkelaar bevestigd. Het schriftelijke informatiedocument is ouder en vermeldt haar nog als aangevraagd, dus vragen wij de verlening schriftelijk op.",
 "Wydane, potwierdzone przez dewelopera we wrześniu 2026 roku. Pisemny dokument informacyjny jest starszy i wciąż odnotowuje je jako złożone, dlatego prosimy o decyzję na piśmie.",
 "Gitt, bekreftet av utbyggeren i september 2026. Det skriftlige opplysningsdokumentet er eldre og fører den fortsatt opp som søkt, så vi ber om vedtaket skriftlig.",
 "Beviljat, bekräftat av byggherren i september 2026. Det skriftliga informationsdokumentet är äldre och anger det fortfarande som ansökt, så vi begär beslutet skriftligt.")

a("Your money","Su dinero","Votre argent","Ihr Geld","Ваши деньги","أموالك","Uw geld","Państwa pieniądze","Pengene dine","Era pengar")

a("The developer states that amounts paid on account are covered by bank guarantee. We ask to see the guarantee itself, not the statement.",
 "El promotor declara que las cantidades entregadas a cuenta están cubiertas por aval bancario. Pedimos ver el aval en sí, no la declaración.",
 "Le promoteur déclare que les sommes versées d'avance sont couvertes par une garantie bancaire. Nous demandons à voir la garantie elle-même, pas la déclaration.",
 "Der Bauträger erklärt, dass Anzahlungen durch eine Bankbürgschaft gedeckt sind. Wir lassen uns die Bürgschaft selbst zeigen, nicht die Erklärung.",
 "Застройщик заявляет, что внесённые суммы покрыты банковской гарантией. Мы просим показать саму гарантию, а не заявление.",
 "يذكر المطوّر أن المبالغ المدفوعة على الحساب مغطّاة بكفالة مصرفية. ونحن نطلب رؤية الكفالة نفسها لا التصريح بها.",
 "De ontwikkelaar verklaart dat voorschotten door een bankgarantie zijn gedekt. Wij vragen de garantie zelf te zien, niet de verklaring.",
 "Deweloper oświadcza, że wpłacone kwoty są objęte gwarancją bankową. Prosimy o wgląd w samą gwarancję, a nie w oświadczenie.",
 "Utbyggeren oppgir at innbetalte beløp er dekket av bankgaranti. Vi ber om å se selve garantien, ikke påstanden.",
 "Byggherren uppger att inbetalda belopp täcks av bankgaranti. Vi ber att få se själva garantin, inte påståendet.")

a("The figures","Las cifras","Les chiffres","Die Zahlen","Цифры","الأرقام","De cijfers","Liczby","Tallene","Siffrorna")

a("Areas and prices are transcribed from the price list of 17 September 2026. Where the seller has issued nothing, such as the floorplan for 71B, the table says so.",
 "Las superficies y los precios están transcritos de la lista de precios del 17 de septiembre de 2026. Cuando el vendedor no ha emitido nada, como el plano del 71B, la tabla lo indica.",
 "Les surfaces et les prix sont transcrits de la liste de prix du 17 septembre 2026. Lorsque le vendeur n'a rien fourni, comme le plan du 71B, le tableau le précise.",
 "Flächen und Preise sind aus der Preisliste vom 17. September 2026 übernommen. Wo der Verkäufer nichts herausgegeben hat, etwa den Grundriss für 71B, sagt die Tabelle das.",
 "Площади и цены перенесены из прайс-листа от 17 сентября 2026 года. Там, где продавец ничего не выпустил, например планировку 71B, таблица так и говорит.",
 "المساحات والأسعار منقولة عن قائمة أسعار 17 سبتمبر 2026. وحيث لم يصدر البائع شيئاً، كمخطط 71B، يذكر الجدول ذلك.",
 "Oppervlakken en prijzen zijn overgenomen uit de prijslijst van 17 september 2026. Waar de verkoper niets heeft uitgegeven, zoals de plattegrond voor 71B, zegt de tabel dat.",
 "Powierzchnie i ceny przepisano z cennika z 17 września 2026 roku. Tam, gdzie sprzedający niczego nie wydał, jak rzut dla 71B, tabela to odnotowuje.",
 "Arealer og priser er hentet fra prislisten av 17. september 2026. Der selgeren ikke har utstedt noe, som plantegningen for 71B, sier tabellen det.",
 "Ytor och priser är avskrivna från prislistan av den 17 september 2026. Där säljaren inte utfärdat något, som planritningen för 71B, säger tabellen det.")

a("How long the price holds","Cuánto dura el precio","Combien de temps le prix tient","Wie lange der Preis gilt",
 "Как долго держится цена","كم يبقى السعر ساريا","Hoelang de prijs geldt","Jak długo obowiązuje cena","Hvor lenge prisen gjelder","Hur länge priset gäller")

a("The price list and the disclosure document both say two days. The explanatory note on price and payment says eleven. We ask the seller which governs before you rely on either.",
 "La lista de precios y el documento informativo dicen dos días. La nota explicativa sobre precio y forma de pago dice once. Preguntamos al vendedor cuál prevalece antes de que usted se apoye en ninguno.",
 "La liste de prix et le document d'information indiquent deux jours. La note explicative sur le prix et le paiement en indique onze. Nous demandons au vendeur lequel fait foi avant que vous ne vous y fiiez.",
 "Preisliste und Informationsdokument nennen zwei Tage. Die Erläuterung zu Preis und Zahlung nennt elf. Wir fragen beim Verkäufer nach, was gilt, bevor Sie sich darauf verlassen.",
 "Прайс-лист и информационный документ говорят о двух днях. Пояснительная записка о цене и оплате — об одиннадцати. Мы уточняем у продавца, что имеет силу, прежде чем вы будете на это полагаться.",
 "قائمة الأسعار ووثيقة الإفصاح تذكران يومين. والمذكّرة التوضيحية للسعر والدفع تذكر أحد عشر. نسأل البائع أيّهما المعتمد قبل أن تعتمد عليه.",
 "De prijslijst en het informatiedocument noemen twee dagen. De toelichting op prijs en betaling noemt er elf. Wij vragen de verkoper wat geldt voordat u erop afgaat.",
 "Cennik i dokument informacyjny podają dwa dni. Nota wyjaśniająca dotycząca ceny i płatności podaje jedenaście. Pytamy sprzedającego, co obowiązuje, zanim Państwo się na tym oprą.",
 "Prislisten og opplysningsdokumentet sier to dager. Forklaringsnotatet om pris og betaling sier elleve. Vi spør selgeren hva som gjelder før du legger det til grunn.",
 "Prislistan och informationsdokumentet säger två dagar. Den förklarande noten om pris och betalning säger elva. Vi frågar säljaren vad som gäller innan ni förlitar er på det.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
