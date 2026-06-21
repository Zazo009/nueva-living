import { readFileSync, writeFileSync } from 'node:fs';

const file = 'Liora_Living_SOLENNE_POLISHED.html';
let html = readFileSync(file, 'utf8');

function replaceRequired(label, pattern, replacement) {
  const next = html.replace(pattern, replacement);
  if (next === html) {
    throw new Error(`Could not replace ${label}`);
  }
  html = next;
}

replaceRequired(
  'nav monogram',
  /<img src="data:image\/png;base64,[^"]+" alt="Liora Living monogram" \/>/,
  '<img src="assets/liora/liora-monogram.svg" alt="Liora Living monogram" decoding="async" />',
);

replaceRequired(
  'hero logo',
  /<img class="hero-brand-logo" src="data:image\/png;base64,[^"]+" alt="Liora Living logo" \/>/,
  '<img class="hero-brand-logo" src="assets/liora/liora-logo-wordmark-light.svg" alt="Liora Living logo" decoding="async" />',
);

replaceRequired(
  'footer logo',
  /<img class="footer-liora-logo" src="data:image\/png;base64,[^"]+" alt="Liora Living logo" \/>/,
  '<img class="footer-liora-logo" src="assets/liora/liora-logo-wordmark-light.svg" alt="Liora Living logo" loading="lazy" decoding="async" />',
);

replaceRequired(
  'vbrand monogram background',
  /(\.vbrand::before\s*\{[\s\S]*?background-image:\s*)url\('data:image\/png;base64,[^']+'\);/,
  "$1url('assets/liora/liora-monogram.svg');",
);

if (!html.includes('assets/liora/liora-monogram.svg" type="image/svg+xml"')) {
  html = html.replace(
    '</title>',
    '</title>\n  <link rel="icon" href="assets/liora/liora-monogram.svg" type="image/svg+xml">',
  );
}

const logoCss = `
    /* ══════════════════════════════════════════════════════
       LIORA LIGHT LOGO PASS
       Refined external logo assets, no embedded PNG logo blobs.
    ══════════════════════════════════════════════════════ */
    .brand-logo-compact {
      gap: 11px;
    }

    .brand-logo-compact img {
      width: 34px;
      height: 34px;
      object-fit: contain;
      filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.18));
    }

    .brand-logo-word strong {
      font-family: Didot, 'Bodoni 72', 'Times New Roman', serif;
      font-size: 15px;
      font-weight: 400;
      letter-spacing: 0.30em;
      color: #f7efe1;
    }

    .brand-logo-word span {
      font-family: Avenir, 'Montserrat', sans-serif;
      font-size: 6.5px;
      font-weight: 400;
      letter-spacing: 0.50em;
      color: rgba(214, 183, 123, 0.92);
    }

    #nav.scrolled .brand-logo-compact img {
      width: 30px;
      height: 30px;
    }

    #nav.scrolled .brand-logo-word strong {
      font-size: 13px;
    }

    #nav.scrolled .brand-logo-word span {
      font-size: 6px;
    }

    .hero-brand-logo {
      width: clamp(230px, 23vw, 360px);
      max-width: 75vw;
      margin: 0 0 clamp(24px, 4vh, 42px) -10px;
      opacity: 0.96;
      filter: drop-shadow(0 14px 34px rgba(0, 0, 0, 0.24));
    }

    .footer-liora-logo {
      width: min(280px, 88vw);
      margin: 0 0 20px -10px;
      opacity: 0.95;
      filter: drop-shadow(0 12px 28px rgba(0, 0, 0, 0.20));
    }

    .vbrand::before {
      width: 22px;
      height: 22px;
      background-image: url('assets/liora/liora-monogram.svg');
      opacity: 0.88;
      filter: drop-shadow(0 2px 7px rgba(0, 0, 0, 0.28));
    }

    @media (max-width: 768px) {
      .brand-logo-compact {
        gap: 9px;
      }

      .brand-logo-compact img {
        width: 30px;
        height: 30px;
      }

      .brand-logo-word strong {
        font-size: 12px;
        letter-spacing: 0.24em;
      }

      .brand-logo-word span {
        font-size: 5.8px;
        letter-spacing: 0.38em;
      }

      .hero-brand-logo {
        width: min(270px, 72vw);
        margin-left: -4px;
      }

      .footer-liora-logo {
        width: min(250px, 84vw);
        margin-left: -4px;
      }

      .vbrand::before {
        width: 19px;
        height: 19px;
      }
    }
`;

if (!html.includes('LIORA LIGHT LOGO PASS')) {
  html = html.replace('  </style>', `${logoCss}\n  </style>`);
}

writeFileSync(file, html);
console.log('Integrated new Liora logo assets into HTML.');
