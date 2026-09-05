import { DEFAULT_LOCALE } from './i18n.mjs';

// Month names and the date shapes each locale writes them in. These lived in
// build_property_pages.mjs, which meant any other builder that needed to write
// a human date either duplicated the table or wrote an ISO string at the
// reader -- the guide byline did the latter until it was moved here.

export const MONTH_NAMES = {
  January: { en: 'January', es: 'enero', fr: 'janvier', de: 'Januar', ru: 'января', ar: 'يناير', nl: 'januari', pl: 'stycznia', sv: 'januari', no: 'januar' },
  February: { en: 'February', es: 'febrero', fr: 'février', de: 'Februar', ru: 'февраля', ar: 'فبراير', nl: 'februari', pl: 'lutego', sv: 'februari', no: 'februar' },
  March: { en: 'March', es: 'marzo', fr: 'mars', de: 'März', ru: 'марта', ar: 'مارس', nl: 'maart', pl: 'marca', sv: 'mars', no: 'mars' },
  April: { en: 'April', es: 'abril', fr: 'avril', de: 'April', ru: 'апреля', ar: 'أبريل', nl: 'april', pl: 'kwietnia', sv: 'april', no: 'april' },
  May: { en: 'May', es: 'mayo', fr: 'mai', de: 'Mai', ru: 'мая', ar: 'مايو', nl: 'mei', pl: 'maja', sv: 'maj', no: 'mai' },
  June: { en: 'June', es: 'junio', fr: 'juin', de: 'Juni', ru: 'июня', ar: 'يونيو', nl: 'juni', pl: 'czerwca', sv: 'juni', no: 'juni' },
  July: { en: 'July', es: 'julio', fr: 'juillet', de: 'Juli', ru: 'июля', ar: 'يوليو', nl: 'juli', pl: 'lipca', sv: 'juli', no: 'juli' },
  August: { en: 'August', es: 'agosto', fr: 'août', de: 'August', ru: 'августа', ar: 'أغسطس', nl: 'augustus', pl: 'sierpnia', sv: 'augusti', no: 'august' },
  September: { en: 'September', es: 'septiembre', fr: 'septembre', de: 'September', ru: 'сентября', ar: 'سبتمبر', nl: 'september', pl: 'września', sv: 'september', no: 'september' },
  October: { en: 'October', es: 'octubre', fr: 'octobre', de: 'Oktober', ru: 'октября', ar: 'أكتوبر', nl: 'oktober', pl: 'października', sv: 'oktober', no: 'oktober' },
  November: { en: 'November', es: 'noviembre', fr: 'novembre', de: 'November', ru: 'ноября', ar: 'نوفمبر', nl: 'november', pl: 'listopada', sv: 'november', no: 'november' },
  December: { en: 'December', es: 'diciembre', fr: 'décembre', de: 'Dezember', ru: 'декабря', ar: 'ديسمبر', nl: 'december', pl: 'grudnia', sv: 'december', no: 'desember' }
};

// The nominative month, for the languages whose table above is genitive
// because it is written for "15 August 2026". Only these two decline it.
export const BARE_MONTH_NAMES = {
  January: { ru: 'январь', pl: 'styczeń' },
  February: { ru: 'февраль', pl: 'luty' },
  March: { ru: 'март', pl: 'marzec' },
  April: { ru: 'апрель', pl: 'kwiecień' },
  May: { ru: 'май', pl: 'maj' },
  June: { ru: 'июнь', pl: 'czerwiec' },
  July: { ru: 'июль', pl: 'lipiec' },
  August: { ru: 'август', pl: 'sierpień' },
  September: { ru: 'сентябрь', pl: 'wrzesień' },
  October: { ru: 'октябрь', pl: 'październik' },
  November: { ru: 'ноябрь', pl: 'listopad' },
  December: { ru: 'декабрь', pl: 'grudzień' }
};

export function localizeMonthDate(value, locale) {
  if (!value || locale === DEFAULT_LOCALE) return value;
  const match = /^(?:(\d{1,2})\s+)?([A-Z][a-z]+)\s+(\d{4})$/.exec(value.trim());
  if (!match) return value.replace(/[A-Z][a-z]+/, (month) => MONTH_NAMES[month]?.[locale] || month);
  const [, day, monthName, year] = match;
  const month = MONTH_NAMES[monthName]?.[locale] || monthName;
  if (!day) {
    // A month standing on its own, with no day in front of it. Russian and
    // Polish decline the month after a day ("15 августа"), so the table above
    // holds the genitive; on its own the month is nominative. Spanish joins a
    // bare month to its year with "de".
    const bare = BARE_MONTH_NAMES[monthName]?.[locale] || month;
    return locale === 'es' ? `${bare} de ${year}` : `${bare} ${year}`;
  }
  if (locale === 'es') return `${day} de ${month} de ${year}`;
  if (locale === 'de') return `${day}. ${month} ${year}`;
  return `${day} ${month} ${year}`;
}

