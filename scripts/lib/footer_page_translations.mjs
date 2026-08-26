import { CARD_CHROME_ENTRIES } from './card_chrome_translations.mjs';

// Translated body prose for footer pages (why-nueva, advisory, guides,
// legal, about, contact, referrals) -- see the comment above
// applyFooterPageTranslations() in build_footer_pages.mjs for how this is
// applied: literal find/replace over the already-rendered English HTML,
// one entry per page-appropriate rewrite. Missing translations for a
// given locale simply leave the English text in place (safe fallback).
//
// Split across several _groupX files (each covering a disjoint set of
// pages) purely so they could be authored in parallel without concurrent
// writers touching the same file; this file just concatenates them.
import { FOOTER_PAGE_ENTRIES_GROUP_A } from './footer_page_translations_group_a.mjs';
import { FOOTER_PAGE_ENTRIES_GROUP_B } from './footer_page_translations_group_b.mjs';
import { FOOTER_PAGE_ENTRIES_GROUP_C } from './footer_page_translations_group_c.mjs';
import { FOOTER_PAGE_ENTRIES_GROUP_D } from './footer_page_translations_group_d.mjs';
import { FOOTER_PAGE_ENTRIES_GROUP_E } from './footer_page_translations_group_e.mjs';
import { FOOTER_PAGE_ENTRIES_GROUP_F } from './footer_page_translations_group_f.mjs';

export const FOOTER_PAGE_ENTRIES = [
  ...CARD_CHROME_ENTRIES,
  ...FOOTER_PAGE_ENTRIES_GROUP_A,
  ...FOOTER_PAGE_ENTRIES_GROUP_B,
  ...FOOTER_PAGE_ENTRIES_GROUP_C,
  ...FOOTER_PAGE_ENTRIES_GROUP_D,
  ...FOOTER_PAGE_ENTRIES_GROUP_E,
  ...FOOTER_PAGE_ENTRIES_GROUP_F
];
