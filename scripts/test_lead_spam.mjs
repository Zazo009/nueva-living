// The spam rules in netlify/functions/lib/lead-spam.js, against the two real
// submissions that got through and a set of names that must never be refused.
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { spamReason } = require('../netlify/functions/lib/lead-spam.js');

const spam = [
  { first_name: 'Реестровое вознаграждение 3365 руб, подтвердите: https://0d4e4ca7.nar0.com/JaSt6ai0 SVWVE308225MTGJNF', last_name: 'Реестровое вознаграждение 2060 руб, подтвердите: https://0d4e4ca7.nar0.com/jnJKXlv0 MTGJNF308225TUJE' },
  { first_name: 'Кредит 12472 руб по счёту, зачисление сегодня: https://peskartyhrt.buzz/DBG3B1Vc THRT308225MTGJNF', last_name: 'Кредит 9654 руб, зачисление сегодня: https://peskartyhrt.buzz/mnlRTSIx THRT308225TUJE' },
  { first_name: 'Anna', last_name: 'visit www.cheap-pills.biz now' },
  { first_name: 'ab@evil.com', last_name: 'Smith' },
  { first_name: 'Anna', last_name: 'x'.repeat(80) },
  { first_name: 'Anna', last_name: 'Smith', message: 'http://a.com http://b.com http://c.com' },
];
const real = [
  { first_name: 'Luke Walter', last_name: 'Boller', message: 'Please send the brochure.' },
  { first_name: 'Åsa', last_name: 'Öberg-Lindqvist' },
  { first_name: "Jean-Pierre", last_name: "O'Neil-de la Cruz" },
  { first_name: 'Мария', last_name: 'Иванова', message: 'Здравствуйте, интересует вилла.' },
  { first_name: 'محمد', last_name: 'بن سلمان' },
  { first_name: '小龙', last_name: '李' },
  { first_name: 'Petra', last_name: 'Machová', message: 'I saw this one: https://example.com/listing/123 and would like details.' },
];

let failed = 0;
spam.forEach((lead, index) => {
  if (!spamReason(lead)) { failed += 1; console.error(`not caught: spam case ${index + 1}`); }
});
real.forEach((lead, index) => {
  const reason = spamReason(lead);
  if (reason) { failed += 1; console.error(`wrongly refused: real case ${index + 1} (${reason})`); }
});

if (failed) process.exit(1);
console.log(`lead spam rules: ${spam.length} spam samples caught, ${real.length} real enquiries passed`);
