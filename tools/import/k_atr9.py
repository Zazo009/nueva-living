# -*- coding: utf-8 -*-
# Altos Terrace Residences, part 9: prices move.
# The seller's own documents disagreed on how long a quoted price holds -- two
# days in the price list and the disclosure document, eleven in the explanatory
# note. That contradiction is dropped in favour of the thing a buyer can act
# on: the price is indicative, the seller can revise it, and on a release with
# sixty homes still unpriced it is likelier to rise than fall.
import json, sys
T={}
def a(en,es,fr,de,ru,ar,nl,pl,no,sv): T[en]={'es':es,'fr':fr,'de':de,'ru':ru,'ar':ar,'nl':nl,'pl':pl,'no':no,'sv':sv}

a("Prices can move","Los precios pueden cambiar","Les prix peuvent évoluer","Preise können sich ändern",
 "Цены могут измениться","الأسعار قابلة للتغيّر","Prijzen kunnen veranderen","Ceny mogą się zmienić",
 "Prisene kan endre seg","Priserna kan ändras")

a("The seller's prices are indicative and can be revised. With sixty of the eighty homes still unpriced, they are likelier to rise than fall. We reconfirm the figure with the seller before you reserve.",
 "Los precios del vendedor son orientativos y pueden revisarse. Con sesenta de las ochenta viviendas todavía sin precio, es más probable que suban a que bajen. Reconfirmamos la cifra con el vendedor antes de que usted reserve.",
 "Les prix du vendeur sont indicatifs et peuvent être révisés. Soixante des quatre-vingts logements n'étant pas encore tarifés, ils ont plus de chances de monter que de baisser. Nous reconfirmons le montant auprès du vendeur avant votre réservation.",
 "Die Preise des Verkäufers sind indikativ und können angepasst werden. Da sechzig der achtzig Wohnungen noch nicht bepreist sind, steigen sie eher, als dass sie fallen. Wir bestätigen die Zahl beim Verkäufer, bevor Sie reservieren.",
 "Цены продавца носят ориентировочный характер и могут быть пересмотрены. Поскольку шестьдесят из восьмидесяти квартир ещё без цены, они скорее вырастут, чем снизятся. Мы подтверждаем сумму у продавца до вашего бронирования.",
 "أسعار البائع إرشادية وقابلة للمراجعة. ومع بقاء ستين من المساكن الثمانين بلا تسعير، فاحتمال ارتفاعها أكبر من انخفاضها. نعيد تأكيد الرقم مع البائع قبل أن تحجز.",
 "De prijzen van de verkoper zijn indicatief en kunnen worden herzien. Nu zestig van de tachtig woningen nog geen prijs hebben, stijgen ze eerder dan dat ze dalen. Wij bevestigen het bedrag bij de verkoper voordat u reserveert.",
 "Ceny sprzedającego są orientacyjne i mogą zostać zmienione. Skoro sześćdziesiąt z osiemdziesięciu mieszkań wciąż nie ma ceny, prędzej wzrosną, niż spadną. Potwierdzamy kwotę u sprzedającego, zanim Państwo zarezerwują.",
 "Selgerens priser er veiledende og kan bli justert. Med seksti av de åtti boligene fortsatt uten pris er det mer sannsynlig at de stiger enn at de faller. Vi bekrefter beløpet med selgeren før du reserverer.",
 "Säljarens priser är vägledande och kan revideras. Med sextio av de åttio bostäderna ännu oprissatta är det mer sannolikt att de stiger än att de faller. Vi bekräftar summan med säljaren innan ni bokar.")

a("Can the prices change?","¿Pueden cambiar los precios?","Les prix peuvent-ils changer ?","Können sich die Preise ändern?",
 "Могут ли цены измениться?","هل يمكن أن تتغيّر الأسعار؟","Kunnen de prijzen veranderen?","Czy ceny mogą się zmienić?",
 "Kan prisene endre seg?","Kan priserna ändras?")

a("Yes. The prices published here are indicative and the seller can revise them at any point before a reservation is signed. With sixty of the eighty homes still to be priced, a revision upward is the likelier direction. Nueva Living reconfirms the figure with the seller before you commit to anything.",
 "Sí. Los precios publicados aquí son orientativos y el vendedor puede revisarlos en cualquier momento antes de firmar una reserva. Con sesenta de las ochenta viviendas todavía por poner a precio, lo más probable es que la revisión sea al alza. Nueva Living reconfirma la cifra con el vendedor antes de que usted se comprometa a nada.",
 "Oui. Les prix publiés ici sont indicatifs et le vendeur peut les réviser à tout moment avant la signature d'une réservation. Soixante des quatre-vingts logements restant à tarifer, une révision à la hausse est le sens le plus probable. Nueva Living reconfirme le montant auprès du vendeur avant tout engagement de votre part.",
 "Ja. Die hier veröffentlichten Preise sind indikativ, und der Verkäufer kann sie jederzeit vor Unterzeichnung einer Reservierung anpassen. Da sechzig der achtzig Wohnungen noch zu bepreisen sind, ist eine Anpassung nach oben die wahrscheinlichere Richtung. Nueva Living bestätigt die Zahl beim Verkäufer, bevor Sie sich zu irgendetwas verpflichten.",
 "Да. Опубликованные здесь цены ориентировочны, и продавец может пересмотреть их в любой момент до подписания брони. Поскольку шестьдесят из восьмидесяти квартир ещё предстоит оценить, пересмотр вверх — более вероятное направление. Nueva Living подтверждает сумму у продавца, прежде чем вы возьмёте на себя какие-либо обязательства.",
 "نعم. الأسعار المنشورة هنا إرشادية، وللبائع أن يراجعها في أي وقت قبل توقيع الحجز. ومع بقاء ستين من المساكن الثمانين دون تسعير، فالمراجعة صعوداً هي الاتجاه الأرجح. تعيد Nueva Living تأكيد الرقم مع البائع قبل أن تلتزم بأي شيء.",
 "Ja. De hier gepubliceerde prijzen zijn indicatief en de verkoper kan ze op elk moment vóór het tekenen van een reservering herzien. Nu zestig van de tachtig woningen nog geprijsd moeten worden, is een herziening naar boven de waarschijnlijkste richting. Nueva Living bevestigt het bedrag bij de verkoper voordat u zich ergens aan verbindt.",
 "Tak. Ceny publikowane tutaj są orientacyjne, a sprzedający może je zmienić w każdej chwili przed podpisaniem rezerwacji. Skoro sześćdziesiąt z osiemdziesięciu mieszkań pozostaje do wyceny, zmiana w górę jest bardziej prawdopodobnym kierunkiem. Nueva Living potwierdza kwotę u sprzedającego, zanim Państwo się do czegokolwiek zobowiążą.",
 "Ja. Prisene som er publisert her er veiledende, og selgeren kan justere dem når som helst før en reservasjon signeres. Med seksti av de åtti boligene igjen å prise er en justering oppover den mest sannsynlige retningen. Nueva Living bekrefter beløpet med selgeren før du forplikter deg til noe.",
 "Ja. Priserna som publiceras här är vägledande, och säljaren kan revidera dem när som helst innan en bokning skrivs på. Med sextio av de åttio bostäderna kvar att prissätta är en revidering uppåt den mer sannolika riktningen. Nueva Living bekräftar summan med säljaren innan ni binder er till något.")

json.dump(T, open(sys.argv[1],'w'), ensure_ascii=False, indent=1); print(len(T))
