// Voice-over and ambience for the social cut, via Runway.
//
// Runway's only job in this campaign is the sound. The picture is the
// apartment's own photography, assembled by build_social_cut.mjs, and nothing
// here touches it.
//
// No music by decision: a generated ambience bed under a spoken recommendation,
// which also sidesteps needing a music licence.
//
// The script is written as a recommendation rather than a narration -- someone
// who has seen the apartment telling you it is worth your time -- and it makes
// no claim the project data does not support. No yield, no appreciation: the
// project's own investment note says Nueva Living does not promise either.
//
//   RUNWAYML_API_SECRET=... node scripts/tools/build_social_audio.mjs [--apply]

import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';

const API = 'https://api.dev.runwayml.com/v1';
const VERSION = '2024-11-06';
const SLUG = 'la-morelia-de-marbella';
const CUT = path.join('dist-social', SLUG, `${SLUG}-social-silent.mp4`);
const OUT = path.join('dist-social', SLUG);

const AMBIENCE = 'Quiet hillside terrace in southern Spain at midday: faint water '
  + 'movement in a small pool, a light breeze through palms, distant birdsong. '
  + 'No music, no voices, no traffic, no footsteps.';

// Same brand register as the site: formal address everywhere it exists,
// informal in Norwegian where the formal form is archaic.
const SCRIPT = {
  en: "Most of what we're shown on this coast is sold for 2029. This one is finished. Furnished, and you could be in it this month. Two bedrooms above Golf Valley, a plunge pool on the terrace, and the valley underneath it. Eight hundred and forty-five thousand euros. There is one of it, so if that is the shape of what you are after, say so early.",
  es: 'Casi todo lo que se nos enseña en esta costa se vende para 2029. Esta ya está terminada. Amueblada, y podría instalarse este mes. Dos dormitorios sobre Golf Valley, una piscina en la terraza y el valle debajo. Ochocientos cuarenta y cinco mil euros. Hay una sola, así que si encaja con lo que busca, dígalo pronto.',
  fr: "L'essentiel de ce qu'on nous montre sur cette côte se vend pour 2029. Celui-ci est terminé. Meublé, et vous pourriez y être ce mois-ci. Deux chambres au-dessus de Golf Valley, un bassin sur la terrasse, et la vallée en dessous. Huit cent quarante-cinq mille euros. Il n'y en a qu'un, alors si cela correspond à ce que vous cherchez, dites-le tôt.",
  de: 'Das meiste, was uns an dieser Küste gezeigt wird, ist für 2029 verkauft. Diese hier ist fertig. Möbliert, und Sie könnten noch diesen Monat einziehen. Zwei Schlafzimmer über dem Golf Valley, ein Tauchbecken auf der Terrasse und das Tal darunter. Achthundertfünfundvierzigtausend Euro. Es gibt sie einmal, also sagen Sie früh Bescheid, wenn das passt.',
  ru: 'Почти всё, что нам показывают на этом побережье, продаётся со сдачей в 2029 году. Эта уже готова. С мебелью, и въехать можно в этом месяце. Две спальни над Гольф-Вэлли, бассейн на террасе и долина внизу. Восемьсот сорок пять тысяч евро. Она одна, поэтому, если это то, что вы ищете, скажите заранее.',
  ar: 'معظم ما يُعرض علينا على هذا الساحل يُباع بتسليم عام 2029. أما هذه فجاهزة. مفروشة، ويمكنكم الانتقال إليها هذا الشهر. غرفتا نوم فوق غولف فالي، وحوض سباحة على التراس، والوادي تحته. ثمانمائة وخمسة وأربعون ألف يورو. إنها واحدة فقط، فإن كان هذا ما تبحثون عنه، فأخبرونا مبكراً.',
  nl: 'Het meeste wat ons aan deze kust wordt getoond, is verkocht voor 2029. Deze is af. Gemeubileerd, en u zou er deze maand in kunnen. Twee slaapkamers boven Golf Valley, een dompelbad op het terras en het dal eronder. Achthonderdvijfenveertigduizend euro. Er is er één, dus als dit past bij wat u zoekt, laat het vroeg weten.',
  pl: 'Większość tego, co pokazuje się na tym wybrzeżu, sprzedawana jest z odbiorem w 2029 roku. Ta jest gotowa. Umeblowana, i mogliby Państwo wprowadzić się w tym miesiącu. Dwie sypialnie nad Golf Valley, basen na tarasie i dolina poniżej. Osiemset czterdzieści pięć tysięcy euro. Jest jedna, więc jeśli to pasuje do Państwa poszukiwań, proszę powiedzieć wcześnie.',
  sv: 'Det mesta vi får se på den här kusten säljs med tillträde 2029. Den här är färdig. Möblerad, och ni skulle kunna flytta in den här månaden. Två sovrum ovanför Golf Valley, en pool på terrassen och dalen nedanför. Åttahundrafyrtiofemtusen euro. Det finns en, så säg till tidigt om det är formen på det ni söker.',
  no: 'Det meste vi får se på denne kysten selges med overtakelse i 2029. Denne er ferdig. Møblert, og du kunne flyttet inn denne måneden. To soverom over Golf Valley, et basseng på terrassen og dalen nedenfor. Åttehundreogførtifem tusen euro. Det finnes én, så si fra tidlig hvis det er formen på det du ser etter.'
};

const apply = process.argv.includes('--apply');
const chars = Object.values(SCRIPT).reduce((n, s) => n + s.length, 0);

console.log(`  cut       ${CUT}`);
console.log(`  ambience  1 x 25s`);
console.log(`  voice     ${Object.keys(SCRIPT).length} languages, ${chars} characters total`);
console.log(`  music     none, by decision\n`);
for (const [loc, text] of Object.entries(SCRIPT)) {
  console.log(`  ${loc}  ${text.length.toString().padStart(4)} chars  ${text.slice(0, 62)}…`);
}

if (!apply) {
  console.log('\n  Dry run. Re-run with --apply to call the API.');
  process.exit(0);
}
if (!existsSync(CUT)) {
  console.error(`\n  ${CUT} is missing. Run build_social_cut.mjs first.`);
  process.exit(1);
}
const secret = process.env.RUNWAYML_API_SECRET;
if (!secret) {
  console.error('\n  RUNWAYML_API_SECRET is not set. Set it in your shell; it is never read from a file here.');
  process.exit(1);
}
const headers = { Authorization: `Bearer ${secret}`, 'X-Runway-Version': VERSION, 'Content-Type': 'application/json' };

async function run(endpoint, body, label) {
  const created = await fetch(`${API}/${endpoint}`, { method: 'POST', headers, body: JSON.stringify(body) });
  if (!created.ok) {
    console.error(`  ${label}: create failed ${created.status} ${(await created.text()).slice(0, 240)}`);
    process.exit(1);
  }
  const { id } = await created.json();
  process.stdout.write(`  ${label}: ${id} `);
  for (let i = 0; i < 90; i += 1) {
    await new Promise((r) => setTimeout(r, 4000));
    const res = await fetch(`${API}/tasks/${id}`, { headers });
    const task = await res.json();
    if (task.status === 'SUCCEEDED') { console.log('ok'); return Array.isArray(task.output) ? task.output[0] : task.output; }
    if (['FAILED', 'CANCELLED', 'CANCELED'].includes(task.status)) {
      console.error(`\n  ${label}: ${task.status} ${JSON.stringify(task.failure || {}).slice(0, 200)}`);
      process.exit(1);
    }
    process.stdout.write('.');
  }
  console.error(`\n  ${label}: timed out`); process.exit(1);
}

async function download(url, file) {
  const res = await fetch(url);
  if (!res.ok) { console.error(`  download failed ${res.status}`); process.exit(1); }
  writeFileSync(file, Buffer.from(await res.arrayBuffer()));
}

mkdirSync(OUT, { recursive: true });
const sfxFile = path.join(OUT, 'ambience.mp3');
if (!existsSync(sfxFile)) {
  await download(await run('sound_effect', { model: 'seed_audio', promptText: AMBIENCE, duration: 25 }, 'ambience'), sfxFile);
}

for (const [loc, text] of Object.entries(SCRIPT)) {
  const voFile = path.join(OUT, `vo-${loc}.mp3`);
  const outFile = path.join(OUT, `${SLUG}-social-${loc}.mp4`);
  if (existsSync(outFile)) { console.log(`  ${loc}: exists, skipping`); continue; }
  if (!existsSync(voFile)) {
    await download(await run('text_to_speech', { model: 'eleven_multilingual_v2', promptText: text }, `vo-${loc}`), voFile);
  }
  // Ambience sits well under the voice; the voice carries the message.
  execFileSync('ffmpeg', ['-v', 'error', '-i', CUT, '-i', voFile, '-i', sfxFile,
    '-filter_complex', '[1:a]volume=1.0[v];[2:a]volume=0.18[a];[v][a]amix=inputs=2:duration=first[mix]',
    '-map', '0:v', '-map', '[mix]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
    '-shortest', '-movflags', '+faststart', '-y', outFile]);
  console.log(`  ${loc}: ${outFile}`);
}
