/* Soléa, the chat on every page (build_dist.mjs injects this script).
 *
 * A round launcher at the bottom right opens a chat panel. Answers come from
 * /.netlify/functions/nueva-chat, which answers from the site's own catalogue and pages.
 *
 * Weight: the launcher is a 10 KB image. The 3D avatar (Three.js and a 480 KB model, about 1.4 MB
 * together, made in Kimi: assets/liora/solea/) is loaded only when someone opens the chat, so a
 * visitor who never opens it never downloads it. The avatar has four states: idle, thinking (while
 * the answer is fetched), talking (while it appears), happy (on opening).
 *
 * The conversation lives in sessionStorage, so it follows the visitor from page to page in one tab
 * and is gone when the tab closes. Nothing is stored on our side except what request_details sends
 * when the visitor asks to be contacted.
 */
(() => {
  if (window.__nuevaSolea) return;
  window.__nuevaSolea = true;

  const script = document.currentScript;
  const AVATAR_VERSION = script?.dataset.avatarVersion || '1';
  const AVATAR_URL = `/assets/liora/solea/sol-avatar.js?v=${AVATAR_VERSION}`;
  const MODEL_URL = `/assets/liora/solea/sol-nueva-living.glb?v=${AVATAR_VERSION}`;
    const LAUNCHER_URL = '/assets/liora/solea/sol-launcher.webp';
  const ENDPOINT = '/.netlify/functions/nueva-chat';
  const STORE = 'nueva-solea-v1';
  const WHATSAPP = '+46 70 757 67 09';
  const WHATSAPP_LINK = 'https://wa.me/46707576709';
  const NUDGE_KEY = 'nueva-solea-nudged';
  const HELLO_KEY = 'nueva-solea-hello';

  const T = {
    en: {
      wa: "WhatsApp an advisor", waHello: "Hello! I have been chatting with Soléa on nuevaliving.com.", waAsked: "I asked:", privacy: "Privacy", nudge: "Shall I show you the floor plans for {name}?", nudgeOther: "Any questions about {name}? I can help with prices, costs and the area.", pPlans: "Show me the floor plans for {name}", pCost: "What does {name} cost in total, with tax and costs?", pArea: "What is near {name}?", dismiss: "Dismiss", hello: ["Hi, I’m Soléa.", "Ask me what a home costs in total.", "Or which area would suit you.", "Questions? I’m here to help."],
      idle: 'Here to help', thinking: 'Looking it up…', happy: 'Hello!', talking: 'Answering…',
      welcome: 'Hola! I’m Soléa, Nueva Living’s guide. Ask me about developments, areas, buying costs or how a purchase works.',
      placeholder: 'Ask about a home, an area or costs…', send: 'Send', open: 'Chat with Soléa', close: 'Close chat',
      reset: 'New conversation', you: 'You', view: 'View',
      suggestions: ['4 bedrooms in Estepona under €1m', 'What tax do I pay on a new build?', 'How does the bank guarantee work?'],
      error: `I couldn’t answer just now. Try again in a moment, or write to us on WhatsApp ${WHATSAPP}.`,
      busy: `There have been many questions from here just now. Try again in a while, or write to us on WhatsApp ${WHATSAPP}.`,
      refusal: 'I can’t help with that one. Ask me anything about buying a new-build home on the Costa del Sol.',
      note: 'AI answers from what nuevaliving.com publishes. List prices; an advisor confirms them.',
    },
    es: {
      wa: "WhatsApp con un asesor", waHello: "¡Hola! He estado hablando con Soléa en nuevaliving.com.", waAsked: "Pregunté:", privacy: "Privacidad", nudge: "¿Le enseño los planos de {name}?", nudgeOther: "¿Tiene preguntas sobre {name}? Le ayudo con precios, costes y la zona.", pPlans: "Enséñeme los planos de {name}", pCost: "¿Cuánto cuesta {name} en total, con impuestos y gastos?", pArea: "¿Qué hay cerca de {name}?", dismiss: "Cerrar", hello: ["Hola, soy Soléa.", "Pregúnteme cuánto cuesta una vivienda en total.", "O qué zona le conviene.", "¿Preguntas? Estoy aquí para ayudarle."],
      idle: 'Aquí para ayudarle', thinking: 'Buscando…', happy: '¡Hola!', talking: 'Respondiendo…',
      welcome: '¡Hola! Soy Soléa, la guía de Nueva Living. Pregúnteme por promociones, zonas, costes de compra o cómo funciona una compra.',
      placeholder: 'Pregunte por una vivienda, una zona o los costes…', send: 'Enviar', open: 'Hablar con Soléa', close: 'Cerrar el chat',
      reset: 'Nueva conversación', you: 'Usted', view: 'Ver',
      suggestions: ['4 dormitorios en Estepona por menos de 1 M€', '¿Qué impuestos pago en una obra nueva?', '¿Cómo funciona el aval bancario?'],
      error: `No he podido responder ahora. Inténtelo de nuevo en un momento o escríbanos por WhatsApp al ${WHATSAPP}.`,
      busy: `Ha habido muchas preguntas desde aquí. Inténtelo más tarde o escríbanos por WhatsApp al ${WHATSAPP}.`,
      refusal: 'En eso no puedo ayudarle. Pregúnteme lo que quiera sobre comprar obra nueva en la Costa del Sol.',
      note: 'Respuestas de IA basadas en lo que publica nuevaliving.com. Precios de lista; un asesor los confirma.',
    },
    fr: {
      wa: "WhatsApp avec un conseiller", waHello: "Bonjour ! J’ai discuté avec Soléa sur nuevaliving.com.", waAsked: "J’ai demandé :", privacy: "Confidentialité", nudge: "Voulez-vous voir les plans de {name} ?", nudgeOther: "Des questions sur {name} ? Je peux vous aider sur les prix, les frais et le quartier.", pPlans: "Montrez-moi les plans de {name}", pCost: "Combien coûte {name} au total, taxes et frais compris ?", pArea: "Qu’y a-t-il près de {name} ?", dismiss: "Fermer", hello: ["Bonjour, je suis Soléa.", "Demandez-moi le coût total d’un logement.", "Ou quel quartier vous convient.", "Une question ? Je suis là pour vous aider."],
      idle: 'À votre écoute', thinking: 'Je cherche…', happy: 'Bonjour !', talking: 'Je réponds…',
      welcome: 'Hola ! Je suis Soléa, le guide de Nueva Living. Posez-moi vos questions sur les programmes, les quartiers, les frais d’achat ou le déroulement d’un achat.',
      placeholder: 'Un logement, un quartier, les frais…', send: 'Envoyer', open: 'Discuter avec Soléa', close: 'Fermer la discussion',
      reset: 'Nouvelle conversation', you: 'Vous', view: 'Voir',
      suggestions: ['4 chambres à Estepona pour moins d’1 M€', 'Quelles taxes sur un logement neuf ?', 'Comment fonctionne la garantie bancaire ?'],
      error: `Je n’ai pas pu répondre pour l’instant. Réessayez dans un moment ou écrivez-nous sur WhatsApp au ${WHATSAPP}.`,
      busy: `Beaucoup de questions viennent d’ici en ce moment. Réessayez plus tard ou écrivez-nous sur WhatsApp au ${WHATSAPP}.`,
      refusal: 'Je ne peux pas vous aider sur ce point. Demandez-moi tout ce qui concerne l’achat d’un logement neuf sur la Costa del Sol.',
      note: 'Réponses d’IA fondées sur ce que publie nuevaliving.com. Prix catalogue, confirmés par un conseiller.',
    },
    de: {
      wa: "WhatsApp an eine Beratung", waHello: "Hallo! Ich habe auf nuevaliving.com mit Soléa gechattet.", waAsked: "Meine Fragen:", privacy: "Datenschutz", nudge: "Soll ich Ihnen die Grundrisse von {name} zeigen?", nudgeOther: "Fragen zu {name}? Ich helfe bei Preisen, Kosten und der Lage.", pPlans: "Zeigen Sie mir die Grundrisse von {name}", pCost: "Was kostet {name} insgesamt, mit Steuern und Nebenkosten?", pArea: "Was gibt es in der Nähe von {name}?", dismiss: "Schließen", hello: ["Hallo, ich bin Soléa.", "Fragen Sie mich, was eine Wohnung insgesamt kostet.", "Oder welche Gegend zu Ihnen passt.", "Fragen? Ich helfe Ihnen gern."],
      idle: 'Für Sie da', thinking: 'Ich schaue nach…', happy: 'Hallo!', talking: 'Ich antworte…',
      welcome: 'Hola! Ich bin Soléa, die Begleiterin von Nueva Living. Fragen Sie mich nach Projekten, Lagen, Kaufnebenkosten oder dem Ablauf eines Kaufs.',
      placeholder: 'Fragen Sie nach Wohnung, Lage oder Kosten…', send: 'Senden', open: 'Mit Soléa chatten', close: 'Chat schließen',
      reset: 'Neues Gespräch', you: 'Sie', view: 'Ansehen',
      suggestions: ['4 Schlafzimmer in Estepona unter 1 Mio. €', 'Welche Steuern fallen beim Neubau an?', 'Wie funktioniert die Bankbürgschaft?'],
      error: `Ich konnte gerade nicht antworten. Versuchen Sie es gleich noch einmal oder schreiben Sie uns auf WhatsApp: ${WHATSAPP}.`,
      busy: `Von hier kamen gerade viele Fragen. Versuchen Sie es später noch einmal oder schreiben Sie uns auf WhatsApp: ${WHATSAPP}.`,
      refusal: 'Dabei kann ich nicht helfen. Fragen Sie mich alles zum Kauf eines Neubaus an der Costa del Sol.',
      note: 'KI-Antworten auf Grundlage dessen, was nuevaliving.com veröffentlicht. Listenpreise; eine Beraterin oder ein Berater bestätigt sie.',
    },
    ru: {
      wa: "WhatsApp консультанту", waHello: "Здравствуйте! Я общался с Солеей на nuevaliving.com.", waAsked: "Мои вопросы:", privacy: "Конфиденциальность", nudge: "Показать вам планировки {name}?", nudgeOther: "Есть вопросы о {name}? Помогу с ценами, расходами и районом.", pPlans: "Покажите планировки {name}", pCost: "Сколько стоит {name} в итоге, с налогами и расходами?", pArea: "Что находится рядом с {name}?", dismiss: "Закрыть", hello: ["Здравствуйте, я Солея.", "Спросите, сколько в итоге стоит жильё.", "Или какой район вам подойдёт.", "Есть вопросы? Я помогу."],
      idle: 'Готова помочь', thinking: 'Ищу…', happy: 'Здравствуйте!', talking: 'Отвечаю…',
      welcome: 'Hola! Я Солея, гид Nueva Living. Спрашивайте о жилых комплексах, районах, расходах на покупку и о том, как проходит сделка.',
      placeholder: 'Спросите о жилье, районе или расходах…', send: 'Отправить', open: 'Чат с Солеей', close: 'Закрыть чат',
      reset: 'Новый разговор', you: 'Вы', view: 'Смотреть',
      suggestions: ['4 спальни в Эстепоне до 1 млн €', 'Какие налоги при покупке новостройки?', 'Как работает банковская гарантия?'],
      error: `Сейчас не получилось ответить. Попробуйте через минуту или напишите нам в WhatsApp: ${WHATSAPP}.`,
      busy: `Отсюда только что пришло много вопросов. Попробуйте позже или напишите нам в WhatsApp: ${WHATSAPP}.`,
      refusal: 'С этим я помочь не могу. Спрашивайте обо всём, что связано с покупкой новостройки на Коста-дель-Соль.',
      note: 'Ответы ИИ на основе того, что опубликовано на nuevaliving.com. Цены по прайс-листу; их подтверждает консультант.',
    },
    ar: {
      wa: "واتساب مع مستشار", waHello: "مرحبًا! كنت أتحدث مع سوليا على nuevaliving.com.", waAsked: "سألت:", privacy: "الخصوصية", nudge: "هل أعرض عليك مخططات {name}؟", nudgeOther: "هل لديك أسئلة عن {name}؟ يمكنني المساعدة في الأسعار والتكاليف والمنطقة.", pPlans: "اعرض لي مخططات {name}", pCost: "كم تبلغ التكلفة الإجمالية لـ {name} مع الضرائب والتكاليف؟", pArea: "ما الذي يقع بالقرب من {name}؟", dismiss: "إغلاق", hello: ["مرحبًا، أنا سوليا.", "اسألني عن التكلفة الإجمالية للمنزل.", "أو عن المنطقة التي تناسبك.", "لديك سؤال؟ أنا هنا لمساعدتك."],
      idle: 'في خدمتك', thinking: 'أبحث…', happy: 'مرحبًا!', talking: 'أجيب…',
      welcome: 'أهلًا! أنا سوليا، دليل نويفا ليفينغ. اسألني عن المشاريع والمناطق وتكاليف الشراء وكيف تتم عملية الشراء.',
      placeholder: 'اسأل عن منزل أو منطقة أو التكاليف…', send: 'إرسال', open: 'تحدّث مع سوليا', close: 'إغلاق المحادثة',
      reset: 'محادثة جديدة', you: 'أنت', view: 'عرض',
      suggestions: ['4 غرف نوم في إستيبونا بأقل من مليون يورو', 'ما الضرائب على العقار الجديد؟', 'كيف يعمل الضمان البنكي؟'],
      error: `تعذّر الرد الآن. حاول مرة أخرى بعد قليل أو راسلنا عبر واتساب ${WHATSAPP}.`,
      busy: `وصلت أسئلة كثيرة من هنا للتو. حاول لاحقًا أو راسلنا عبر واتساب ${WHATSAPP}.`,
      refusal: 'لا أستطيع المساعدة في هذا. اسألني عن أي شيء يخص شراء منزل جديد على كوستا ديل سول.',
      note: 'إجابات بالذكاء الاصطناعي مما ينشره موقع nuevaliving.com. الأسعار أسعار القوائم ويؤكدها مستشار.',
    },
    nl: {
      wa: "WhatsApp met een adviseur", waHello: "Hallo! Ik heb op nuevaliving.com met Soléa gechat.", waAsked: "Mijn vragen:", privacy: "Privacy", nudge: "Zal ik u de plattegronden van {name} laten zien?", nudgeOther: "Vragen over {name}? Ik help met prijzen, kosten en de omgeving.", pPlans: "Laat me de plattegronden van {name} zien", pCost: "Wat kost {name} in totaal, met belasting en kosten?", pArea: "Wat is er in de buurt van {name}?", dismiss: "Sluiten", hello: ["Hallo, ik ben Soléa.", "Vraag mij wat een woning in totaal kost.", "Of welke omgeving bij u past.", "Vragen? Ik help u graag."],
      idle: 'Hier om te helpen', thinking: 'Even zoeken…', happy: 'Hallo!', talking: 'Ik antwoord…',
      welcome: 'Hola! Ik ben Soléa, de gids van Nueva Living. Vraag me naar projecten, gebieden, aankoopkosten of hoe een aankoop verloopt.',
      placeholder: 'Vraag naar een woning, een gebied of de kosten…', send: 'Versturen', open: 'Chat met Soléa', close: 'Chat sluiten',
      reset: 'Nieuw gesprek', you: 'U', view: 'Bekijken',
      suggestions: ['4 slaapkamers in Estepona onder € 1 mln', 'Welke belasting betaal ik op nieuwbouw?', 'Hoe werkt de bankgarantie?'],
      error: `Ik kon nu niet antwoorden. Probeer het zo opnieuw of stuur ons een WhatsApp: ${WHATSAPP}.`,
      busy: `Er kwamen net veel vragen van hier. Probeer het later opnieuw of stuur ons een WhatsApp: ${WHATSAPP}.`,
      refusal: 'Daar kan ik niet bij helpen. Vraag me alles over het kopen van nieuwbouw aan de Costa del Sol.',
      note: 'AI-antwoorden op basis van wat nuevaliving.com publiceert. Lijstprijzen; een adviseur bevestigt ze.',
    },
    pl: {
      wa: "WhatsApp z doradcą", waHello: "Dzień dobry! Rozmawiałem z Soléą na nuevaliving.com.", waAsked: "Moje pytania:", privacy: "Prywatność", nudge: "Pokazać rzuty mieszkań w {name}?", nudgeOther: "Pytania o {name}? Pomogę z cenami, kosztami i okolicą.", pPlans: "Proszę pokazać rzuty mieszkań w {name}", pCost: "Ile łącznie kosztuje {name}, z podatkami i kosztami?", pArea: "Co jest w pobliżu {name}?", dismiss: "Zamknij", hello: ["Dzień dobry, jestem Soléa.", "Proszę zapytać, ile łącznie kosztuje mieszkanie.", "Albo która okolica będzie odpowiednia.", "Pytania? Chętnie pomogę."],
      idle: 'Chętnie pomogę', thinking: 'Szukam…', happy: 'Dzień dobry!', talking: 'Odpowiadam…',
      welcome: 'Hola! Jestem Soléa, przewodniczka Nueva Living. Proszę pytać o inwestycje, okolice, koszty zakupu i o to, jak przebiega zakup.',
      placeholder: 'Proszę zapytać o mieszkanie, okolicę lub koszty…', send: 'Wyślij', open: 'Czat z Soléą', close: 'Zamknij czat',
      reset: 'Nowa rozmowa', you: 'Pan/Pani', view: 'Zobacz',
      suggestions: ['4 sypialnie w Esteponie do 1 mln €', 'Jakie podatki przy zakupie nowej nieruchomości?', 'Jak działa gwarancja bankowa?'],
      error: `Nie udało się teraz odpowiedzieć. Proszę spróbować za chwilę albo napisać do nas na WhatsAppie: ${WHATSAPP}.`,
      busy: `Z tego miejsca przyszło właśnie wiele pytań. Proszę spróbować później albo napisać do nas na WhatsAppie: ${WHATSAPP}.`,
      refusal: 'W tym nie mogę pomóc. Proszę pytać o wszystko, co dotyczy zakupu nowej nieruchomości na Costa del Sol.',
      note: 'Odpowiedzi AI na podstawie treści opublikowanych na nuevaliving.com. Ceny cennikowe potwierdza doradca.',
    },
    sv: {
      wa: "WhatsApp med en rådgivare", waHello: "Hej! Jag har chattat med Soléa på nuevaliving.com.", waAsked: "Jag frågade:", privacy: "Integritet", nudge: "Vill ni se planritningarna för {name}?", nudgeOther: "Frågor om {name}? Jag hjälper er gärna med priser, kostnader och området.", pPlans: "Visa planritningarna för {name}", pCost: "Vad kostar {name} totalt, med skatt och köpkostnader?", pArea: "Vad finns i närheten av {name}?", dismiss: "Stäng", hello: ["Hej, jag är Soléa.", "Fråga mig vad en bostad kostar totalt.", "Eller vilket område som passar er.", "Frågor? Jag hjälper er gärna."],
      idle: 'Här för att hjälpa', thinking: 'Jag letar…', happy: 'Hej!', talking: 'Jag svarar…',
      welcome: 'Hola! Jag är Soléa, Nueva Livings guide. Fråga mig gärna om projekt, områden, köpkostnader eller hur ett köp går till.',
      placeholder: 'Fråga om en bostad, ett område eller kostnader…', send: 'Skicka', open: 'Chatta med Soléa', close: 'Stäng chatten',
      reset: 'Ny konversation', you: 'Ni', view: 'Visa',
      suggestions: ['4 sovrum i Estepona under 1 miljon €', 'Vilken skatt betalar man på nyproduktion?', 'Hur fungerar bankgarantin?'],
      error: `Jag kunde inte svara just nu. Försök gärna igen om en stund, eller skriv till oss på WhatsApp ${WHATSAPP}.`,
      busy: `Det har kommit många frågor härifrån nyss. Försök gärna igen om en stund, eller skriv till oss på WhatsApp ${WHATSAPP}.`,
      refusal: 'Det kan jag tyvärr inte hjälpa till med. Fråga mig gärna om allt som gäller köp av nyproduktion på Costa del Sol.',
      note: 'AI-svar utifrån det nuevaliving.com publicerar. Listpriser; en rådgivare bekräftar dem.',
    },
    no: {
      wa: "WhatsApp med en rådgiver", waHello: "Hei! Jeg har chattet med Soléa på nuevaliving.com.", waAsked: "Jeg spurte:", privacy: "Personvern", nudge: "Vil du se plantegningene for {name}?", nudgeOther: "Spørsmål om {name}? Jeg hjelper deg med priser, kostnader og området.", pPlans: "Vis meg plantegningene for {name}", pCost: "Hva koster {name} totalt, med skatt og kjøpskostnader?", pArea: "Hva finnes i nærheten av {name}?", dismiss: "Lukk", hello: ["Hei, jeg er Soléa.", "Spør meg hva en bolig koster totalt.", "Eller hvilket område som passer deg.", "Spørsmål? Jeg hjelper deg gjerne."],
      idle: 'Her for å hjelpe', thinking: 'Jeg leter…', happy: 'Hei!', talking: 'Jeg svarer…',
      welcome: 'Hola! Jeg er Soléa, Nueva Livings guide. Spør meg om prosjekter, områder, kjøpskostnader eller hvordan et kjøp foregår.',
      placeholder: 'Spør om en bolig, et område eller kostnader…', send: 'Send', open: 'Chat med Soléa', close: 'Lukk chatten',
      reset: 'Ny samtale', you: 'Du', view: 'Se',
      suggestions: ['4 soverom i Estepona under 1 million €', 'Hvilken skatt betaler jeg på nybygg?', 'Hvordan fungerer bankgarantien?'],
      error: `Jeg fikk ikke svart akkurat nå. Prøv igjen om litt, eller skriv til oss på WhatsApp ${WHATSAPP}.`,
      busy: `Det har kommet mange spørsmål herfra nettopp. Prøv igjen om litt, eller skriv til oss på WhatsApp ${WHATSAPP}.`,
      refusal: 'Det kan jeg ikke hjelpe med. Spør meg gjerne om alt som gjelder kjøp av nybygg på Costa del Sol.',
      note: 'KI-svar ut fra det nuevaliving.com publiserer. Listepriser; en rådgiver bekrefter dem.',
    },
  };

  const lang = (document.documentElement.lang || 'en').slice(0, 2).toLowerCase();
  const t = T[lang] || T.en;
  const rtl = document.documentElement.dir === 'rtl' || lang === 'ar';
  const PRIVACY_URL = `/${lang === 'en' ? '' : `${lang}/`}privacy-policy.html#the-chat-assistant`;

  const CSS = `
.solea{--s-cream:#f4ead9;--s-ivory:#faf6ee;--s-gold:#a8834a;--s-engraving:#896a3f;--s-ink:#2f2417;--s-espresso:#4a3b28;--s-muted:#6b5a43;--s-sea:#7b97a4;--s-line:rgba(168,131,74,.28);--s-lift:var(--solea-lift,0px);font-family:"Montserrat",Arial,sans-serif;color:var(--s-ink)}
.solea *{box-sizing:border-box}
.solea-launcher{position:fixed;z-index:30050;right:max(20px,env(safe-area-inset-right));bottom:calc(max(20px,env(safe-area-inset-bottom)) + var(--s-lift));width:68px;height:68px;padding:0;border:1px solid var(--s-line);border-radius:50%;background:var(--s-ivory);box-shadow:0 12px 34px rgba(47,36,23,.22);cursor:pointer;display:grid;place-items:center;transition:transform .28s ease-out,box-shadow .18s ease-out,opacity .28s}
.solea-launcher:hover{transform:translateY(-3px);box-shadow:0 16px 40px rgba(47,36,23,.26)}
.solea-launcher:active{transform:scale(.96)}
.solea-launcher-face{position:relative;display:block;width:62px;height:62px}.solea-launcher-face img,.solea-launcher-face sol-avatar{position:absolute;inset:0;width:62px;height:62px;display:block}.solea-launcher.is-live .solea-launcher-face>img,.solea-face.is-live>img{opacity:0}
.solea-launcher::after{content:"";position:absolute;right:3px;bottom:5px;width:13px;height:13px;border:3px solid var(--s-ivory);border-radius:50%;background:var(--s-gold)}
.solea.is-open .solea-launcher{opacity:0;pointer-events:none;transform:scale(.8)}
.solea.is-waiting .solea-launcher,.solea.is-tucked .solea-launcher,.solea.is-tucked .solea-nudge{transform:translateY(calc(100% + 40px));opacity:0;pointer-events:none}
.solea button:focus-visible,.solea input:focus-visible,.solea a:focus-visible{outline:2px solid var(--s-sea);outline-offset:2px}
.solea-panel{position:fixed;z-index:30200;right:max(20px,env(safe-area-inset-right));bottom:calc(max(20px,env(safe-area-inset-bottom)) + var(--s-lift));width:min(390px,calc(100vw - 32px));height:min(620px,calc(100dvh - 40px - var(--s-lift)));display:flex;flex-direction:column;overflow:hidden;border:1px solid var(--s-line);border-radius:20px;background:var(--s-ivory);box-shadow:0 24px 70px rgba(47,36,23,.24)}
.solea-panel[hidden]{display:none}
.solea-head{display:flex;align-items:center;gap:12px;padding:12px 10px 12px 14px;border-bottom:1px solid var(--s-line);background:linear-gradient(180deg,var(--s-cream),var(--s-ivory))}
.solea-face{position:relative;flex:0 0 56px;width:56px;height:56px}
.solea-face img,.solea-face sol-avatar{position:absolute;inset:0;width:56px;height:56px;display:block}
.solea-id{flex:1;min-width:0}
.solea-name{display:block;font-family:"Cinzel",Georgia,serif;font-size:19px;letter-spacing:.04em;line-height:1.2;color:var(--s-espresso)}
.solea-status{display:block;margin-top:2px;font-size:11.5px;color:var(--s-muted)}
.solea-icon{display:grid;place-items:center;width:40px;height:40px;padding:0;border:0;border-radius:50%;background:transparent;color:var(--s-espresso);cursor:pointer}
.solea-icon:hover{background:var(--s-cream)}
.solea-icon svg{width:19px;height:19px}
.solea-log{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:16px 14px;display:flex;flex-direction:column;gap:10px}
.solea-msg{max-width:90%;padding:10px 13px;border-radius:4px 14px 14px 14px;background:var(--s-cream);font-size:14px;line-height:1.55;overflow-wrap:anywhere}
.solea-msg p{margin:0}.solea-msg p+p,.solea-msg ul+p,.solea-msg p+ul{margin-top:8px}
.solea-msg ul{margin:0;padding-inline-start:18px;list-style:disc}.solea-msg li{list-style:inherit}.solea-msg li+li{margin-top:3px}
.solea-msg a{color:var(--s-engraving);text-decoration:underline;text-underline-offset:2px}
.solea-msg.is-user{align-self:flex-end;border-radius:14px 4px 14px 14px;background:var(--s-espresso);color:var(--s-ivory);white-space:pre-wrap}
.solea-msg.is-note{background:transparent;padding:0 2px;font-size:11.5px;color:var(--s-muted)}
.solea-typing{display:inline-flex;gap:4px;padding:14px 16px}
.solea-typing i{width:6px;height:6px;border-radius:50%;background:var(--s-gold);animation:solea-dot 1.2s infinite ease-in-out}
.solea-typing i:nth-child(2){animation-delay:.15s}.solea-typing i:nth-child(3){animation-delay:.3s}
@keyframes solea-dot{0%,80%,100%{opacity:.25;transform:translateY(0)}40%{opacity:1;transform:translateY(-3px)}}
.solea-cards{display:flex;gap:8px;overflow-x:auto;padding:2px 2px 6px;scroll-snap-type:x mandatory;max-width:100%}
.solea-card{flex:0 0 200px;scroll-snap-align:start;display:flex;flex-direction:column;border:1px solid var(--s-line);border-radius:12px;background:#fff;color:var(--s-ink);text-decoration:none;overflow:hidden}
.solea-card img{width:100%;height:108px;object-fit:cover;display:block;background:var(--s-cream)}
.solea-card span{display:block;padding:0 10px}
.solea-card .c-name{padding-top:8px;font-size:13px;font-weight:600;line-height:1.3}
.solea-card .c-meta{font-size:11.5px;color:var(--s-muted);line-height:1.4}
.solea-card .c-from{padding-bottom:9px;font-size:12px;color:var(--s-engraving);font-weight:600}
.solea-chips{display:flex;flex-wrap:wrap;gap:6px}
.solea-chip{padding:7px 11px;border:1px solid var(--s-line);border-radius:999px;background:#fff;color:var(--s-espresso);font:inherit;font-size:12.5px;line-height:1.3;cursor:pointer;text-align:start}
.solea-chip:hover{border-color:var(--s-gold);background:var(--s-cream)}
.solea-form{display:flex;gap:8px;padding:10px 12px 12px;border-top:1px solid var(--s-line);background:var(--s-ivory)}
.solea-input{flex:1;min-width:0;min-height:44px;padding:10px 14px;border:1px solid var(--s-line);border-radius:999px;background:#fff;color:var(--s-ink);font:inherit;font-size:16px}
.solea-input::placeholder{color:#8d7c63}
.solea-send{flex:0 0 44px;width:44px;height:44px;padding:0;border:0;border-radius:50%;background:var(--s-espresso);color:var(--s-ivory);cursor:pointer;display:grid;place-items:center}
.solea-send:hover{background:var(--s-ink)}.solea-send:disabled{opacity:.45;cursor:default}
.solea-send svg{width:18px;height:18px}
.solea[dir=rtl] .solea-send svg{transform:scaleX(-1)}
.solea-sr{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.solea-nudge{position:fixed;z-index:30055;right:calc(max(20px,env(safe-area-inset-right)) + 80px);bottom:calc(max(20px,env(safe-area-inset-bottom)) + var(--s-lift) + 10px);max-width:min(270px,calc(100vw - 120px));display:flex;align-items:flex-start;gap:6px;padding:11px 10px 11px 14px;border:1px solid var(--s-line);border-radius:14px 14px 4px 14px;background:var(--s-ivory);box-shadow:0 12px 34px rgba(47,36,23,.18);font-size:13.5px;line-height:1.45;color:var(--s-ink);animation:solea-in .32s ease-out}
.solea-hello{position:fixed;z-index:30049;right:calc(max(20px,env(safe-area-inset-right)) + 82px);bottom:calc(max(20px,env(safe-area-inset-bottom)) + var(--s-lift) + 17px);max-width:min(300px,calc(100vw - 120px));padding:8px 15px 9px;text-wrap:balance;border:1px solid var(--s-line);border-radius:16px 16px 4px 16px;background:var(--s-ivory);box-shadow:0 10px 28px rgba(47,36,23,.16);font:inherit;font-size:13.5px;line-height:1.4;color:var(--s-espresso);text-align:start;cursor:pointer;transform-origin:100% 100%;transition:opacity .35s ease-out,transform .35s cubic-bezier(.2,1.4,.4,1)}
.solea-hello::after{content:"";position:absolute;right:-6px;bottom:9px;width:10px;height:10px;background:var(--s-ivory);border-right:1px solid var(--s-line);border-top:1px solid var(--s-line);transform:rotate(45deg)}
.solea-hello span{display:block;transition:opacity .25s,transform .25s}.solea-hello span.is-out{opacity:0;transform:translateY(-5px)}
.solea-hello-dots{display:inline-flex!important;gap:4px;padding:6px 2px}.solea-hello-dots i{width:5px;height:5px;border-radius:50%;background:var(--s-gold);animation:solea-dot 1.2s infinite ease-in-out}.solea-hello-dots i:nth-child(2){animation-delay:.15s}.solea-hello-dots i:nth-child(3){animation-delay:.3s}
.solea-hello.is-settled{animation:solea-hello-bob 5s 1.5s ease-in-out infinite}
@keyframes solea-hello-bob{0%,100%{translate:0 0}50%{translate:0 -3px}}
.solea-hello:hover{color:var(--s-ink);box-shadow:0 12px 32px rgba(47,36,23,.22)}.solea-hello:focus-visible{outline:2px solid var(--s-sea);outline-offset:3px}
.solea-hello.is-gone,.solea.is-open .solea-hello,.solea.is-waiting .solea-hello,.solea.is-tucked .solea-hello{opacity:0;transform:scale(.6) translateY(8px);pointer-events:none}
.solea[dir=rtl] .solea-hello{right:auto;left:calc(max(20px,env(safe-area-inset-left)) + 82px);border-radius:16px 16px 16px 4px;transform-origin:0 100%}.solea[dir=rtl] .solea-hello::after{right:auto;left:-6px;transform:rotate(-135deg)}
@media (max-width:520px){.solea-hello{right:calc(max(14px,env(safe-area-inset-right)) + 72px);bottom:calc(max(14px,env(safe-area-inset-bottom)) + var(--s-lift) + 13px);font-size:13px}.solea[dir=rtl] .solea-hello{left:calc(max(14px,env(safe-area-inset-left)) + 72px)}}
.solea-nudge button.n-text{all:unset;cursor:pointer;flex:1}
.solea-nudge button.n-text:focus-visible{outline:2px solid var(--s-sea);outline-offset:3px}
.solea-nudge .solea-icon{width:26px;height:26px;flex:0 0 26px}.solea-nudge .solea-icon svg{width:14px;height:14px}
.solea[dir=rtl] .solea-nudge{right:auto;left:calc(max(20px,env(safe-area-inset-left)) + 80px);border-radius:14px 14px 14px 4px}
.solea.is-open .solea-nudge{display:none}
@keyframes solea-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.solea-wa{color:#1f7a4d}
.solea-msg.is-note a{color:inherit}
@media (max-width:520px){.solea-nudge{right:calc(max(14px,env(safe-area-inset-right)) + 70px)}}
@media (max-width:520px){.solea-launcher{right:max(14px,env(safe-area-inset-right));bottom:calc(max(14px,env(safe-area-inset-bottom)) + var(--s-lift));width:60px;height:60px}.solea-launcher-face,.solea-launcher-face img,.solea-launcher-face sol-avatar{width:54px;height:54px}
.solea-panel{right:8px;left:8px;bottom:calc(8px + env(safe-area-inset-bottom));width:auto;height:calc(100dvh - 16px - env(safe-area-inset-bottom) - env(safe-area-inset-top));border-radius:18px}}
@media (prefers-reduced-motion:reduce){.solea-launcher,.solea-typing i,.solea-nudge,.solea-hello,.solea-hello span,.solea-hello-dots i{transition:none;animation:none}}
@media print{.solea{display:none}}`;

  const ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>';
  const ICON_RESET = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4h4"/></svg>';
  const ICON_WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M4.5 19.5l1.2-3.6A8 8 0 1 1 8.4 18.6Z"/><path d="M9.2 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4.1.5.4l.6 1.5c.1.2 0 .4-.1.6l-.5.6c.6 1.1 1.5 2 2.6 2.6l.6-.5c.2-.1.4-.2.6-.1l1.5.6c.3.1.4.3.4.5v.5c0 .3 0 .6-.5.8-.6.3-1.5.4-2.6-.1a9 9 0 0 1-4.4-4.4c-.5-1.1-.4-2 0-2.5Z"/></svg>';
  const ICON_SEND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m5 12 14-7-4 14-3-6-7-1Z"/></svg>';

  function el(tag, attrs = {}, children = []) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (value == null) continue;
      if (key === 'class') node.className = value;
      else if (key === 'text') node.textContent = value;
      else if (key === 'html') node.innerHTML = value;
      else node.setAttribute(key, value);
    }
    for (const child of [].concat(children)) if (child) node.append(child);
    return node;
  }

  function track(event, detail = {}) {
    try { window.dispatchEvent(new CustomEvent('nueva:track', { detail: { event, ...detail } })); } catch { /* never block the chat */ }
  }

  // --- answer rendering: a small, safe subset of markdown built as DOM nodes, never as HTML -----

  function safeHref(raw) {
    try {
      const url = new URL(raw, location.origin);
      if (url.protocol === 'mailto:') return url.href;
      if (url.protocol !== 'https:' && url.protocol !== 'http:') return null;
      if (/(^|\.)nuevaliving\.com$/.test(url.hostname) || url.hostname === location.hostname || url.hostname === 'wa.me') return url.href;
    } catch { /* not a link */ }
    return null;
  }

  function inline(text, parent) {
    const pattern = /\[([^\]]+)\]\(([^)\s]+)\)|\*\*([^*]+)\*\*|(https?:\/\/[^\s)]+)/g;
    let last = 0;
    let match;
    while ((match = pattern.exec(text))) {
      if (match.index > last) parent.append(text.slice(last, match.index));
      if (match[1]) {
        const href = safeHref(match[2]);
        parent.append(href ? link(href, match[1]) : match[1]);
      } else if (match[3]) {
        parent.append(el('strong', { text: match[3] }));
      } else {
        const href = safeHref(match[4]);
        parent.append(href ? link(href, match[4].replace(/^https?:\/\/(www\.)?/, '')) : match[4]);
      }
      last = pattern.lastIndex;
    }
    if (last < text.length) parent.append(text.slice(last));
  }

  function link(href, label) {
    const same = new URL(href).hostname === location.hostname || /nuevaliving\.com$/.test(new URL(href).hostname);
    return el('a', { href, text: label, ...(same ? {} : { target: '_blank', rel: 'noopener' }) });
  }

  function renderAnswer(text, bubble) {
    let list = null;
    for (const raw of String(text).split('\n')) {
      const line = raw.trim();
      if (!line) { list = null; continue; }
      const item = /^[-*•]\s+(.*)$/.exec(line) || /^\d+[.)]\s+(.*)$/.exec(line);
      if (item) {
        if (!list) { list = el('ul'); bubble.append(list); }
        const li = el('li');
        inline(item[1], li);
        list.append(li);
      } else {
        list = null;
        const p = el('p');
        inline(line.replace(/^#+\s*/, ''), p);
        bubble.append(p);
      }
    }
  }

  // --- state ---------------------------------------------------------------------------------

  let messages = [];
  try { messages = JSON.parse(sessionStorage.getItem(STORE) || '[]').filter((m) => m && m.role && typeof m.text === 'string'); } catch { messages = []; }
  function save() {
    try { sessionStorage.setItem(STORE, JSON.stringify(messages.slice(-30))); } catch { /* private mode */ }
  }

  let root; let panel; let launcher; let log; let input; let sendButton; let status; let face; let avatar = null;
  let busy = false;
  let talkTimer = 0;

  function setState(state) {
    status.textContent = t[state] || t.idle;
    if (avatar) avatar.setAttribute('state', state);
  }

  // The 3D avatar is two <sol-avatar> elements: one in the launcher, one in the panel's header.
  // The launcher's waits until the page has loaded and the browser is idle; opening the chat
  // fetches it at once. Visitors who ask to save data keep the still image in the launcher.
  let launcherAvatar = null;
  function makeAvatar(state) {
    const node = document.createElement('sol-avatar');
    node.setAttribute('model', MODEL_URL);
    node.setAttribute('poster', LAUNCHER_URL);
    node.setAttribute('framing', 'close');
    node.setAttribute('state', state);
    node.setAttribute('aria-hidden', 'true');
    return node;
  }

  function loadAvatar() {
    if (loadAvatar.promise) return loadAvatar.promise;
    if (!('WebGLRenderingContext' in window)) return (loadAvatar.promise = Promise.reject());
    loadAvatar.promise = import(AVATAR_URL).then(() => {
      launcherAvatar = makeAvatar('idle');
      // In the corner she rests and notices only a pointer that comes near (tools/solea).
      launcherAvatar.setAttribute('calm', '');
      launcherAvatar.setAttribute('follow-radius', '260');
      launcher.querySelector('.solea-launcher-face').append(launcherAvatar);
      launcherAvatar.addEventListener('ready', () => launcher.classList.add('is-live'), { once: true });
      avatar = makeAvatar('happy');
      face.append(avatar);
      avatar.addEventListener('ready', () => face.classList.add('is-live'), { once: true });
      if (!panel.hidden) launcherAvatar.pause?.();
    });
    loadAvatar.promise.catch(() => { /* the still image stays; the chat works without the 3D avatar */ });
    return loadAvatar.promise;
  }

  function loadAvatarWhenIdle() {
    if (navigator.connection?.saveData) return;
    const start = () => (window.requestIdleCallback ? requestIdleCallback(() => loadAvatar(), { timeout: 4000 }) : setTimeout(loadAvatar, 1500));
    if (document.readyState === 'complete') start();
    else addEventListener('load', start, { once: true });
  }

  function scrollDown() { log.scrollTop = log.scrollHeight; }

  function addBubble(role, text, cards) {
    const bubble = el('div', { class: `solea-msg${role === 'user' ? ' is-user' : ''}`, dir: 'auto' });
    bubble.append(el('span', { class: 'solea-sr', text: `${role === 'user' ? t.you : 'Soléa'}: ` }));
    if (role === 'user') bubble.append(text);
    else renderAnswer(text, bubble);
    log.append(bubble);
    if (cards && cards.length) log.append(renderCards(cards));
    scrollDown();
    return bubble;
  }

  function renderCards(cards) {
    const row = el('div', { class: 'solea-cards' });
    for (const card of cards) {
      const href = safeHref(card.url);
      if (!href) continue;
      const meta = [card.area, card.type, card.bedrooms ? `${card.bedrooms} 🛏` : null].filter(Boolean).join(' · ');
      row.append(el('a', { class: 'solea-card', href }, [
        card.image ? el('img', { src: card.image, alt: '', loading: 'lazy', decoding: 'async' }) : null,
        el('span', { class: 'c-name', text: card.name }),
        el('span', { class: 'c-meta', text: meta }),
        el('span', { class: 'c-from', text: card.from || '' }),
      ]));
    }
    return row;
  }

  // On a development's page Soléa knows which one the visitor is reading, and whether its page has
  // floor plans, so the suggestions and the nudge are about that development.
  function pageProject() {
    const name = document.querySelector('[data-project-name]')?.getAttribute('data-project-name');
    if (!name || !/property-/.test(location.pathname)) return null;
    return { name, plans: Boolean(document.querySelector('a[href$="floorplan.pdf"]')) };
  }

  function suggestionsHere() {
    const project = pageProject();
    if (!project) return t.suggestions;
    const fill = (template) => template.replace('{name}', project.name);
    return [project.plans ? fill(t.pPlans) : null, fill(t.pCost), fill(t.pArea)].filter(Boolean);
  }

  function renderSuggestions() {
    const chips = el('div', { class: 'solea-chips' });
    for (const question of suggestionsHere()) {
      chips.append(el('button', { type: 'button', class: 'solea-chip', text: question }));
    }
    chips.addEventListener('click', (event) => {
      const chip = event.target.closest('.solea-chip');
      if (!chip) return;
      chips.remove();
      ask(chip.textContent);
    });
    log.append(chips);
  }

  function renderAll() {
    log.textContent = '';
    addBubble('assistant', t.welcome);
    for (const m of messages) addBubble(m.role, m.text, m.cards);
    if (!messages.length) renderSuggestions();
    log.append(el('p', { class: 'solea-msg is-note' }, [`${t.note} `, el('a', { href: PRIVACY_URL, text: t.privacy })]));
    scrollDown();
  }

  // Takes out what looks like an e-mail address or a phone number before a question is logged.
  function anonymise(text) {
    return String(text)
      .replace(/[^\s@]+@[^\s@]+\.[^\s@]+/g, '[e-mail]')
      .replace(/\+?\d[\d\s().-]{6,}\d/g, '[phone]')
      .slice(0, 300);
  }

  // The anonymous question log (see the privacy policy): the question without contact details,
  // what was searched and read, and whether the site could answer. It goes to the CRM's own
  // measurement; the tracker keeps "message" away from Google and Meta.
  function logQuestion(text, meta, outcome) {
    const search = (meta?.searches || [])[0] || {};
    track('chat_question', {
      message: anonymise(text),
      language: lang,
      outcome,
      gap: Boolean(meta?.gap),
      found: meta?.found ?? null,
      pages: (meta?.pages || []).join(' '),
      tools: (meta?.tools || []).join(' '),
      search_location: search.location || null,
      search_budget_min: search.budget_min || null,
      search_budget_max: search.budget_max || null,
      search_bedrooms: search.bedrooms_min || null,
      search_type: search.property_type || null,
      search_stage: search.stage || null,
      search_features: (search.features || []).join(' ') || null,
      search_size_min: search.size_min || null,
      search_size_max: search.size_max || null,
      project: pageProject()?.name || null,
      turn: messages.filter((m) => m.role === 'user').length,
    });
  }

  async function ask(question) {
    const text = String(question || '').trim().slice(0, 1500);
    if (!text || busy) return;
    busy = true;
    sendButton.disabled = true;
    hideNudge(true);
    log.querySelector('.solea-chips')?.remove();
    log.querySelector('.is-note')?.remove();
    messages.push({ role: 'user', text });
    save();
    const asked = addBubble('user', text);
    const typing = el('div', { class: 'solea-msg solea-typing', 'aria-hidden': 'true' }, [el('i'), el('i'), el('i')]);
    log.append(typing);
    scrollDown();
    clearTimeout(talkTimer);
    setState('thinking');

    let answer = '';
    let cards = [];
    let failure = null;
    let done = null;
    let bubble = null;
    let frame = 0;
    // The answer is drawn as it arrives, at most once a frame.
    const draw = () => {
      frame = 0;
      if (!bubble) {
        typing.remove();
        bubble = el('div', { class: 'solea-msg', dir: 'auto' });
        log.append(bubble);
        setState('talking');
      }
      bubble.textContent = '';
      bubble.append(el('span', { class: 'solea-sr', text: 'Soléa: ' }));
      renderAnswer(answer, bubble);
      scrollDown();
    };
    try {
      const response = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          language: lang,
          page: location.pathname,
          messages: messages.map((m) => ({ role: m.role, text: m.text })),
        }),
      });
      if (response.status === 429) failure = t.busy;
      else if (!response.ok || !response.body) failure = t.error;
      else {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        for (;;) {
          const { value, done: finished } = await reader.read();
          if (finished) break;
          buffer += decoder.decode(value, { stream: true });
          let cut;
          while ((cut = buffer.indexOf('\n')) >= 0) {
            const line = buffer.slice(0, cut).trim();
            buffer = buffer.slice(cut + 1);
            if (!line) continue;
            let item;
            try { item = JSON.parse(line); } catch { continue; }
            if (item.type === 'text') {
              answer += item.text;
              if (!frame) frame = requestAnimationFrame(draw);
            } else if (item.type === 'done') done = item;
            else if (item.type === 'error') failure = t.error;
          }
        }
        if (!done && !failure) failure = t.error;
      }
    } catch {
      failure = t.error;
    }
    if (frame) { cancelAnimationFrame(frame); frame = 0; }
    if (done?.fallback === 'refusal') { answer = t.refusal; }
    else if (done?.fallback === 'rounds' && !answer.trim()) failure = t.error;
    if (failure && !answer.trim()) {
      typing.remove();
      messages.pop(); save(); asked.remove();
      addBubble('assistant', failure);
      logQuestion(text, null, failure === t.busy ? 'busy' : 'error');
      setState('idle');
      busy = false;
      sendButton.disabled = false;
      input.value = text;
      input.focus({ preventScroll: true });
      return;
    }
    if (!answer.trim()) answer = t.error;
    cards = Array.isArray(done?.cards) ? done.cards : [];
    draw();
    if (cards.length) { log.append(renderCards(cards)); scrollDown(); }
    messages.push({ role: 'assistant', text: answer, cards });
    save();
    logQuestion(text, done?.meta, done?.fallback || 'answered');
    if (done?.sent) track('chat_lead', { language: lang });
    clearTimeout(talkTimer);
    talkTimer = setTimeout(() => setState('idle'), 1800);
    busy = false;
    sendButton.disabled = false;
    input.focus({ preventScroll: true });
  }

  // --- the nudge: on a development's page, a small question beside the launcher -------------

  let nudge = null;
  function hideNudge(forGood) {
    nudge?.remove();
    nudge = null;
    if (forGood) { try { sessionStorage.setItem(NUDGE_KEY, '1'); } catch { /* ignore */ } }
  }

  // Only for someone reading the page: after 40 seconds, and once they have scrolled a fair way.
  function scheduleNudge() {
    const project = pageProject();
    if (!project) return;
    try { if (sessionStorage.getItem(NUDGE_KEY) || messages.length) return; } catch { return; }
    let timeUp = false;
    let read = false;
    const onScroll = () => {
      if (scrollY > Math.min(900, document.documentElement.scrollHeight * 0.25)) {
        read = true;
        removeEventListener('scroll', onScroll);
        if (timeUp) show();
      }
    };
    addEventListener('scroll', onScroll, { passive: true });
    setTimeout(() => { timeUp = true; if (read) show(); }, 40000);
    function show() {
      if (!panel.hidden || nudge) return;
      try { if (sessionStorage.getItem(NUDGE_KEY)) return; } catch { return; }
      const question = (project.plans ? t.nudge : t.nudgeOther).replace('{name}', project.name);
      const textButton = el('button', { type: 'button', class: 'n-text', text: question });
      const dismiss = el('button', { type: 'button', class: 'solea-icon', 'aria-label': t.dismiss, title: t.dismiss, html: ICON_CLOSE });
      nudge = el('div', { class: 'solea-nudge', role: 'status', dir: 'auto' }, [textButton, dismiss]);
      hideHello();
      root.append(nudge);
      launcherAvatar?.setAttribute('state', 'happy');
      setTimeout(() => launcherAvatar?.setAttribute('state', 'idle'), 2500);
      track('chat_nudge_shown', { language: lang, project: project.name });
      textButton.addEventListener('click', () => {
        hideNudge(true);
        open();
        track('chat_nudge_click', { language: lang, project: project.name });
        if (project.plans) ask(t.pPlans.replace('{name}', project.name));
      });
      dismiss.addEventListener('click', () => hideNudge(true));
    }
  }

  // --- the hello: a speech bubble beside the launcher, so it is plain she is there to help ----
  // On the visitor's first page she introduces herself in a few lines that turn over one after
  // another and settle on the last; on later pages only the last line shows. On a phone the
  // bubble leaves after a while so it does not sit over the text. It goes for good once the chat
  // has been opened, and steps aside for the nudge.
  let hello = null;
  function hideHello() { hello?.classList.add('is-gone'); }
  function sayHello() {
    if (messages.length || !panel.hidden) return;
    const lines = t.hello;
    let first = false;
    try { first = !sessionStorage.getItem(HELLO_KEY); sessionStorage.setItem(HELLO_KEY, '1'); } catch { /* ignore */ }
    const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const queue = first && !still ? lines.slice() : [lines[lines.length - 1]];
    const text = el('span');
    hello = el('button', { type: 'button', class: 'solea-hello is-gone', dir: 'auto', 'aria-label': t.open }, [text]);
    root.append(hello);
    hello.addEventListener('click', open);
    // Each line arrives as she would write it: three dots first, then the words.
    const say = (line, then) => {
      if (still) { text.textContent = line; then?.(); return; }
      text.classList.add('is-out');
      setTimeout(() => {
        text.className = 'solea-hello-dots';
        text.replaceChildren(el('i'), el('i'), el('i'));
        setTimeout(() => {
          text.className = 'is-out';
          text.textContent = line;
          requestAnimationFrame(() => text.classList.remove('is-out'));
          then?.();
        }, 750);
      }, 220);
    };
    requestAnimationFrame(() => requestAnimationFrame(() => hello.classList.remove('is-gone')));
    launcherAvatar?.setAttribute('state', 'happy');
    setTimeout(() => launcherAvatar?.getAttribute('state') === 'happy' && launcherAvatar.setAttribute('state', 'idle'), 2200);
    const next = () => {
      if (!queue.length) {
        hello.classList.add('is-settled');
        if (matchMedia('(max-width:520px)').matches) setTimeout(hideHello, 7000);
        return;
      }
      say(queue.shift(), () => setTimeout(next, 2700));
    };
    next();
  }

  // Soléa is not there when the visitor lands: she appears once they start scrolling, so the
  // first view of a page is the page. A visitor who has already chatted in this tab sees her at
  // once, and on a page too short to scroll she comes after a few seconds.
  function appearOnScroll() {
    if (messages.length) return;
    root.classList.add('is-waiting');
    const show = () => {
      root.classList.remove('is-waiting');
      removeEventListener('scroll', onScroll);
      loadAvatar();
      setTimeout(sayHello, 900);
    };
    const onScroll = () => { if (scrollY > 120) show(); };
    addEventListener('scroll', onScroll, { passive: true });
    setTimeout(() => {
      if (document.documentElement.scrollHeight <= innerHeight + 160) show();
    }, 4000);
  }

  // On a phone the launcher steps aside while the visitor scrolls down to read, and comes back
  // when they scroll up or stop, so it never sits over a form or a price list they are reading.
  function tuckOnScroll() {
    let last = scrollY;
    let timer = 0;
    addEventListener('scroll', () => {
      if (innerWidth > 760 || !panel.hidden) { root.classList.remove('is-tucked'); last = scrollY; return; }
      const y = scrollY;
      if (y > last + 6 && y > 160) root.classList.add('is-tucked');
      else if (y < last - 6) root.classList.remove('is-tucked');
      last = y;
      clearTimeout(timer);
      timer = setTimeout(() => root.classList.remove('is-tucked'), 1400);
    }, { passive: true });
  }

  // --- WhatsApp: the same conversation, handed to a person ------------------------------------

  function whatsappHref() {
    const asked = messages.filter((m) => m.role === 'user').slice(-3).map((m) => `- ${m.text.slice(0, 160)}`);
    const lines = [t.waHello, asked.length ? `${t.waAsked}\n${asked.join('\n')}` : '', location.href.split('#')[0]].filter(Boolean);
    return `${WHATSAPP_LINK}?text=${encodeURIComponent(lines.join('\n\n'))}`;
  }

  function open() {
    if (!panel.hidden) return;
    hideNudge(true);
    hideHello();
    root.classList.remove('is-waiting');
    panel.hidden = false;
    root.classList.add('is-open');
    launcher.setAttribute('aria-expanded', 'true');
    loadAvatar();
    launcherAvatar?.pause?.();
    setState('happy');
    clearTimeout(talkTimer);
    talkTimer = setTimeout(() => setState('idle'), 2500);
    scrollDown();
    requestAnimationFrame(() => input.focus({ preventScroll: true }));
    track('chat_open', { language: lang });
  }

  function close() {
    if (panel.hidden) return;
    panel.hidden = true;
    root.classList.remove('is-open');
    launcher.setAttribute('aria-expanded', 'false');
    launcherAvatar?.play?.();
    setState('idle');
    launcher.focus({ preventScroll: true });
  }

  function reset() {
    messages = [];
    save();
    renderAll();
    setState('happy');
    input.focus({ preventScroll: true });
  }

  // The property pages pin a booking bar to the bottom on phones; the launcher sits above it.
  // The current template's bar is #v2-actionbar; it slides away over the enquiry form, and the
  // launcher follows it down when it does.
  function liftAboveBars() {
    const bar = document.querySelector('.sticky-mobile-cta, #v2-actionbar');
    let lift = 0;
    if (bar && !bar.classList.contains('is-hidden')) {
      const style = getComputedStyle(bar);
      if (style.position === 'fixed' && style.display !== 'none' && style.visibility !== 'hidden') lift = bar.getBoundingClientRect().height;
    }
    root.style.setProperty('--solea-lift', `${Math.round(lift)}px`);
  }

  function build() {
    document.head.append(el('style', { 'data-solea': '', text: CSS }));
    root = el('div', { class: 'solea', dir: rtl ? 'rtl' : 'ltr', lang });
    launcher = el('button', { type: 'button', class: 'solea-launcher', 'aria-label': t.open, 'aria-expanded': 'false', 'aria-controls': 'solea-panel' }, [
      el('span', { class: 'solea-launcher-face' }, [el('img', { src: LAUNCHER_URL, alt: '', width: '60', height: '60', decoding: 'async' })]),
    ]);
    face = el('div', { class: 'solea-face', 'aria-hidden': 'true' }, [el('img', { src: LAUNCHER_URL, alt: '' })]);
    status = el('span', { class: 'solea-status', 'aria-live': 'polite', text: t.idle });
    log = el('div', { class: 'solea-log', role: 'log', 'aria-live': 'polite', 'aria-relevant': 'additions' });
    input = el('input', { class: 'solea-input', type: 'text', name: 'message', autocomplete: 'off', maxlength: '1500', placeholder: t.placeholder, 'aria-label': t.placeholder, enterkeyhint: 'send' });
    sendButton = el('button', { type: 'submit', class: 'solea-send', 'aria-label': t.send, html: ICON_SEND });
    const form = el('form', { class: 'solea-form' }, [input, sendButton]);
    panel = el('section', { id: 'solea-panel', class: 'solea-panel', role: 'dialog', 'aria-label': t.open, hidden: '' }, [
      el('header', { class: 'solea-head' }, [
        face,
        el('div', { class: 'solea-id' }, [el('span', { class: 'solea-name', text: 'Soléa' }), status]),
        el('a', { class: 'solea-icon solea-wa', 'data-wa': '', href: WHATSAPP_LINK, target: '_blank', rel: 'noopener', 'aria-label': t.wa, title: t.wa, html: ICON_WA }),
        el('button', { type: 'button', class: 'solea-icon', 'data-reset': '', 'aria-label': t.reset, title: t.reset, html: ICON_RESET }),
        el('button', { type: 'button', class: 'solea-icon', 'data-close': '', 'aria-label': t.close, title: t.close, html: ICON_CLOSE }),
      ]),
      log,
      form,
    ]);
    root.append(panel, launcher);
    document.body.append(root);

    launcher.addEventListener('click', open);
    panel.querySelector('[data-close]').addEventListener('click', close);
    panel.querySelector('[data-reset]').addEventListener('click', reset);
    // The link carries the visitor's last questions and the page, written when it is followed.
    const wa = panel.querySelector('[data-wa]');
    const fillWa = () => { wa.href = whatsappHref(); };
    wa.addEventListener('pointerdown', fillWa);
    wa.addEventListener('focus', fillWa);
    wa.addEventListener('click', () => { fillWa(); track('chat_whatsapp', { language: lang, turn: messages.filter((m) => m.role === 'user').length }); });
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const text = input.value;
      input.value = '';
      ask(text);
    });
    root.addEventListener('keydown', (event) => { if (event.key === 'Escape') close(); });
    // Warm the 3D avatar's download when the visitor reaches for the launcher.
    launcher.addEventListener('pointerenter', loadAvatar, { once: true });
    launcher.addEventListener('focus', loadAvatar, { once: true });
    loadAvatarWhenIdle();

    renderAll();
    appearOnScroll();
    scheduleNudge();
    tuckOnScroll();
    liftAboveBars();
    window.addEventListener('resize', liftAboveBars, { passive: true });
    const v2bar = document.getElementById('v2-actionbar');
    if (v2bar && 'MutationObserver' in window) new MutationObserver(liftAboveBars).observe(v2bar, { attributes: true, attributeFilter: ['class'] });
    // Anything on the site can open the chat: a link or button with data-solea-open.
    document.addEventListener('click', (event) => {
      const trigger = event.target.closest('[data-solea-open]');
      if (!trigger) return;
      event.preventDefault();
      open();
      const question = trigger.getAttribute('data-solea-open');
      if (question) ask(question);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build, { once: true });
  else build();
})();
