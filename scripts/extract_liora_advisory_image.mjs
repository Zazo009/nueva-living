import { readFileSync, writeFileSync } from 'node:fs';

const html = readFileSync('Liora_Living_SOLENNE_POLISHED.html', 'utf8');
const match = html.match(/<img src="data:image\/jpeg;base64,([^"]+)" alt="Solenne Benahavís new development exterior arrival"/);

if (!match) {
  throw new Error('Could not find embedded Solenne image to use as advisory fallback.');
}

writeFileSync('assets/liora/advisory-property.jpg', Buffer.from(match[1], 'base64'));
console.log('Wrote assets/liora/advisory-property.jpg');
