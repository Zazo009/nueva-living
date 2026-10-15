// The "majolica" layout of the signature template.
//
// Same idea as signature_page.mjs -- a project sold on a name gets its own page
// body instead of the apartment-comparison page -- but a different page. Where
// the Armani layout is a calm olive-and-ivory editorial column, this one is
// built from the Design Hills brochure itself: the cover lockup, the navy of its
// price list, the blue-and-white of the majolica ceramics, the emerald of the
// living rooms, and sections that slide in from alternating sides.
//
// What it reads, beyond the standard record:
//   signature.*             copy that only this layout has
//   availability.units      the priced residences, one card each
//   signature.residences    the numbers behind each card, in the same order
//
// Everything visible is either a string from the record (translated by the
// overlays like any other) or derived from numbers in it. The block names, the
// stone swatches and the unit-to-block mapping are not prose: the names and
// swatches live in keys the overlays leave alone, and the mapping is read from
// the ENGLISH unit references so a translation can never move a unit.

import fs from 'node:fs';

const readMark = (name, className) => fs.readFileSync(new URL(`../../assets/liora/signature-logos/${name}.svg`, import.meta.url), 'utf8')
  .replace(' xmlns="http://www.w3.org/2000/svg"', '')
  .replace('<svg ', `<svg class="${className}" aria-hidden="true" focusable="false" `)
  .trim();

// The brochure's own lockup and the Dolce&Gabbana wordmark, as vector paths so
// they take the colour of whatever they sit on. The words stay in the markup as
// hidden text: the logos are pictures of them.
const titleMark = readMark('dhm-mark', 'mj-mark');
const dgMark = readMark('dg-mark', 'mj-dg');

const digits = (value = '') => Number(String(value).replace(/[^\d]/g, '')) || 0;

export function renderMajolicaMain({ project, sourceProject, locale, faqs, projectMedia, helpers }) {
  const {
    esc, t, pictureTag, actionLink, ghostAction, whatsappHref,
    renderLocationCard, renderEnquiryForm, liveLocationMap, floorplanThumb, responsiveThumb
  } = helpers;
  const s = project.signature || {};
  const en = sourceProject.signature || {};
  const mediaByName = (name) => (project.media?.items || []).find((item) => item.src.includes(`/${name}.`));
  const figure = (name, sizes = '(max-width: 900px) 100vw, 50vw', loading = 'lazy') => {
    const image = mediaByName(name);
    return image ? pictureTag(image, '', loading, { sizes }) : '';
  };
  const heroImage = project.images.hero;
  const facts = s.heroFacts || [];
  const chapterIds = ['concept', 'blocks', 'residences', 'interiors', 'club', 'setting', 'enquire'];
  const chapters = (s.chapters || []).map((label, index) => [chapterIds[index], label]).filter(([id]) => id);
  const enquireLabel = project.enquiry.headlineHtml.replace(/<[^>]+>/g, '');

  // ---- Units, grouped by block --------------------------------------------
  const units = project.availability?.units || [];
  const englishUnits = sourceProject.availability?.units || [];
  const blockOf = (index) => Number(String(englishUnits[index]?.reference || '').match(/Block\s+(\d)/)?.[1]) || 0;
  const blockNames = en.blocks?.names || [];

  const unitCard = (unit, index) => {
    const fig = s.residences?.figures?.[index] || {};
    const thumb = floorplanThumb(unit.floorplan);
    const planAlt = t('availability.floorplanOf', locale, { reference: unit.reference });
    const rows = [
      [s.residences?.interior, fig.interior],
      [s.residences?.common, fig.common],
      [s.residences?.terrace, fig.terrace],
      [s.residences?.garden, fig.garden],
      [s.residences?.solarium, fig.solarium],
      [s.residences?.total, fig.total]
    ].filter(([label, value]) => label && value);
    return `<article class="mj-unit" id="unit-${index + 1}" data-block="${blockOf(index)}" data-mj-in="up" style="--d:${(index % 3) * 0.08}s">
          ${thumb ? `<a class="mj-unit-plan" href="${esc(unit.floorplan)}" target="_blank" rel="noopener" aria-label="${esc(planAlt)}">${responsiveThumb(thumb, planAlt)}</a>` : ''}
          <div class="mj-unit-body">
            <p class="mj-unit-ref">${esc(unit.reference)}</p>
            <p class="mj-unit-price">${esc(unit.price)}</p>
            <p class="mj-unit-lead">${esc(unit.bedrooms)} · ${esc(s.residences?.baths?.[index] || '')}</p>
            <dl class="mj-unit-facts">${rows.map(([label, value], row) => `<div${row === rows.length - 1 ? ' class="is-total"' : ''}><dt>${esc(label)}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl>
            ${unit.floorplan ? `<a class="mj-unit-link" href="${esc(unit.floorplan)}" target="_blank" rel="noopener">${esc(s.residences?.planLabel || '')}</a>` : ''}
          </div>
        </article>`;
  };

  const blockPanel = (name, blockNumber) => {
    const indexes = englishUnits.map((_, index) => index).filter((index) => blockOf(index) === blockNumber);
    const cheapest = indexes.reduce((best, index) => (best === null || digits(englishUnits[index].price) < digits(englishUnits[best].price) ? index : best), null);
    const body = indexes.length
      ? `<ul class="mj-block-units">${indexes.map((index) => `<li><a href="#unit-${index + 1}"><span>${esc(units[index].reference)}</span><strong>${esc(units[index].price)}</strong></a></li>`).join('')}</ul>`
      : `<p class="mj-block-empty">${esc(s.blocks?.notPriced || '')}</p>`;
    return `<div class="mj-panel" role="tabpanel" id="mj-panel-${blockNumber}" aria-labelledby="mj-tab-${blockNumber}" data-mj-panel="${blockNumber}">
          <div class="mj-panel-head">
            <span class="mj-panel-no" aria-hidden="true">${blockNumber}</span>
            <div>
              <h3>${esc(name)}</h3>
              <p>${indexes.length ? `<span class="mj-count-label">${esc(s.blocks?.unitsLabel || '')}:</span> <strong>${indexes.length}</strong>${cheapest !== null ? ` · ${esc(s.blocks?.fromLabel || '')} ${esc(units[cheapest].price)}` : ''}` : esc(s.blocks?.notPriced || '')}</p>
            </div>
          </div>
          ${indexes.length ? body : ''}
        </div>`;
  };

  const blockTabs = blockNames.map((name, index) => `<button type="button" class="mj-tab" role="tab" id="mj-tab-${index + 1}" aria-controls="mj-panel-${index + 1}" aria-selected="${index === 0 ? 'true' : 'false'}" data-mj-tab="${index + 1}"><small>${esc(s.blocks?.blockLabel || '')} ${index + 1}</small><span>${esc(name)}</span></button>`).join('');
  const blockPanels = blockNames.map((name, index) => blockPanel(name, index + 1)).join('\n        ');
  const marqueeItems = blockNames.map((name) => `<span>${esc(name)}</span><i></i>`).join('');

  const typologies = (s.residences?.typologies || []).map(([name, text], index) => `<article class="mj-typology" data-mj-in="up" style="--d:${index * 0.1}s"><h3>${esc(name)}</h3><p>${esc(text)}</p></article>`).join('');
  const palette = (s.concept?.palette || []).map(([name, text], index) => `<article class="mj-swatch" data-tone="${index}" data-mj-in="${index % 2 ? 'right' : 'left'}" style="--d:${index * 0.12}s"><i aria-hidden="true"></i><h3>${esc(name)}</h3><p>${esc(text)}</p></article>`).join('');
  const stones = (s.interiors?.materials || []).map(([name, origin, text], index) => {
    const swatch = en.interiors?.swatches?.[index];
    return `<article class="mj-stone" data-mj-in="${index % 2 ? 'right' : 'left'}" style="--d:${(index % 2) * 0.1}s">
          <div class="mj-stone-img">${swatch ? pictureTag({ ...swatch, alt: '' }, '', 'lazy', { sizes: '(max-width: 900px) 100vw, 100vw' }) : ''}</div>
          <div class="mj-stone-copy"><h3>${esc(name)}</h3>${origin ? `<span>${esc(origin)}</span>` : ''}<p>${esc(text)}</p></div>
        </article>`;
  }).join('\n        ');
  // The club is told as rows of picture and text, one row per kind of amenity,
  // the picture sliding in from one side and the words from the other. The
  // groups are in the record's order; the rows pair two small ones together.
  const clubRows = [
    { groups: [0], images: ['pool-club-cabanas-and-umbrellas', 'pool-with-majolica-floats'] },
    { groups: [1], images: ['restaurant-with-a-teal-bar', 'private-dining-room-in-gold'] },
    { groups: [2], images: ['gym-in-white-panda-marble'] },
    { groups: [3], images: ['majolica-terrace-from-above'] },
    { groups: [4, 5], images: ['long-table-under-the-pergola'] },
    { groups: [6], images: ['facade-above-the-water-promenade', 'beach-club-entrance'] },
    { groups: [7], images: ['lobby-in-white-panda-marble'] }
  ];
  const clubGroup = ([title, ...items]) => `<article class="mj-group"><h3>${esc(title)}</h3><ul>${items.map((item) => `<li>${esc(item)}</li>`).join('')}</ul></article>`;
  const clubMarkup = clubRows.map((row, index) => {
    const flip = index % 2 === 1;
    const media = row.images.map((name, position) => `<figure class="${position ? 'is-small' : 'is-main'}">${figure(name, position ? '(max-width: 900px) 60vw, 24vw' : '(max-width: 900px) 100vw, 46vw')}</figure>`).join('');
    return `<div class="mj-club-row${flip ? ' is-flip' : ''}">
          <div class="mj-club-media${row.images.length > 1 ? ' has-pair' : ''}" data-mj-in="${flip ? 'right' : 'left'}">${media}</div>
          <div class="mj-club-text" data-mj-in="${flip ? 'left' : 'right'}" style="--d:.1s">${row.groups.map((g) => clubGroup((s.club?.groups || [])[g] || [])).join('')}</div>
        </div>`;
  }).join('\n        ');
  const teamCards = (s.team?.cards || []).map(([role, name, detail], index) => `<article class="mj-member" data-mj-in="${index % 2 ? 'right' : 'left'}" style="--d:${(index % 2) * 0.1}s"><span>${esc(role)}</span><h3>${esc(name)}</h3><p>${esc(detail)}</p></article>`).join('');
  const distances = (project.location?.distances || []).map(([label, value]) => `<li><span>${esc(label)}</span><strong>${esc(value)}</strong></li>`).join('');
  const extras = (s.location?.extras || []).map(([label, value]) => `<li><span>${esc(label)}</span><strong>${esc(value)}</strong></li>`).join('');
  const grounds = (s.blocks?.grounds || []).map((item) => `<li>${esc(item)}</li>`).join('');
  const paragraphs = (list = []) => list.map((text) => `<p>${esc(text)}</p>`).join('');

  return `
    <section class="mj-hero" id="top">
      <div class="mj-hero-media" data-mj-parallax>${pictureTag(heroImage, 'mj-hero-img', '', { priority: true, sizes: '100vw' })}</div>
      <div class="mj-hero-veil" aria-hidden="true"></div>
      <div class="mj-wrap mj-hero-inner">
        <p class="mj-eyebrow">${esc(project.hero.eyebrow)} <span aria-hidden="true">·</span> ${esc(project.hero.location)}</p>
        <h1 class="mj-title"><span class="mj-vh">Design Hills Marbella</span>${titleMark}</h1>
        <p class="mj-by"><span>${esc(s.by || '')}</span><span class="mj-vh">Dolce&amp;Gabbana</span>${dgMark}</p>
        <p class="mj-lead">${esc(s.lead || project.description)}</p>
        <div class="mj-hero-actions">
          ${actionLink(enquireLabel, '#enquire')}
          ${ghostAction(t('cta.requestProjectMaterial', locale), '#residences')}
        </div>
      </div>
      <ul class="mj-hero-facts mj-wrap" aria-label="${esc(t('aria.projectKeyFacts', locale))}">
        ${facts.map(([value, label]) => `<li><strong>${esc(value)}</strong><span>${esc(label)}</span></li>`).join('\n        ')}
      </ul>
      <div class="mj-ribbon" aria-hidden="true"></div>
      <div class="mj-curtain" aria-hidden="true"></div>
    </section>

    <nav class="mj-bar" aria-label="${esc(t('aria.projectSections', locale))}" data-mj-chapters>
      <div class="mj-wrap mj-bar-inner">
        <a class="mj-bar-brand" href="#top" aria-label="${esc(project.name)}">${readMark('dhm-mark', 'mj-mark')}</a>
        <div class="mj-bar-links">
          ${chapters.map(([id, label], index) => `<a href="#${id}" data-chapter="${id}"><i>${String(index + 1).padStart(2, '0')}</i>${esc(label)}</a>`).join('\n          ')}
        </div>
        ${actionLink(enquireLabel, '#enquire', 'mj-bar-cta')}
      </div>
      <span class="mj-progress" data-mj-progress aria-hidden="true"></span>
    </nav>

    <section class="mj-section mj-hills" id="concept" data-no="01">
      <div class="mj-wrap mj-hills-grid">
        <div class="mj-hills-copy">
          <span class="mj-kicker" data-mj-in="left">${esc(s.concept?.kicker || '')}</span>
          <h2 data-mj-in="left" style="--d:.08s">${s.concept?.headlineHtml || ''}</h2>
          <div class="mj-prose" data-mj-in="left" style="--d:.16s">${paragraphs(s.concept?.paragraphs)}</div>
        </div>
        <div class="mj-hills-collage" data-mj-in="wipe">
          <figure class="is-main">${figure('terrace-dining-at-sunset', '(max-width: 900px) 100vw, 46vw')}</figure>
          <figure class="is-small">${figure('sunken-lounge-at-dusk', '(max-width: 900px) 60vw, 24vw')}</figure>
        </div>
      </div>
      <blockquote class="mj-pull" data-mj-in="up"><p>${esc(s.concept?.pull || '')}</p></blockquote>
      <div class="mj-wrap mj-palette">
        <p class="mj-palette-label" data-mj-in="up">${esc(s.concept?.paletteLabel || '')}</p>
        <div class="mj-palette-row">${palette}</div>
      </div>
    </section>

    <div class="mj-marquee" aria-hidden="true">
      <div class="mj-marquee-track">${marqueeItems}${marqueeItems}${marqueeItems}${marqueeItems}</div>
    </div>

    <section class="mj-section mj-blocks" id="blocks" data-no="02">
      <div class="mj-wrap">
        <div class="mj-head">
          <span class="mj-kicker" data-mj-in="left">${esc(s.blocks?.kicker || '')}</span>
          <h2 data-mj-in="left" style="--d:.08s">${s.blocks?.headlineHtml || ''}</h2>
          <p data-mj-in="left" style="--d:.16s">${esc(s.blocks?.copy || '')}</p>
        </div>
        <div class="mj-tabs" role="tablist" aria-label="${esc(s.blocks?.kicker || '')}" data-mj-in="up">${blockTabs}</div>
        <div class="mj-panels" data-mj-panels>
        ${blockPanels}
        </div>
        <div class="mj-grounds" data-mj-in="up"><span>${esc(s.blocks?.groundsLabel || '')}</span><ul>${grounds}</ul></div>
      </div>
      <figure class="mj-blocks-aerial" data-mj-in="wipe">${figure('aerial-night-over-the-coast', '100vw')}</figure>
      <div class="mj-duo">
        <figure data-mj-in="left">${figure('terraced-facade-at-sunset', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="right">${figure('pool-club-and-terraces-by-day', '(max-width: 900px) 100vw, 50vw')}</figure>
      </div>
    </section>

    <figure class="mj-band" aria-hidden="true">
      <div data-mj-parallax>${figure('roof-terrace-with-the-sea-beyond', '100vw')}</div>
      <div class="mj-band-text">${[0, 1, 2, 3].map(() => `<span>${esc(project.name)}</span>`).join('')}</div>
    </figure>

    <section class="mj-section mj-residences" id="residences" data-no="03">
      <div class="mj-wrap">
        <div class="mj-head">
          <span class="mj-kicker" data-mj-in="left">${esc(s.residences?.kicker || '')}</span>
          <h2 data-mj-in="left" style="--d:.08s">${project.residences.headlineHtml}</h2>
          <p data-mj-in="left" style="--d:.16s">${esc(project.residences.copy)}</p>
        </div>
        <div class="mj-typologies" aria-label="${esc(s.residences?.typologiesLabel || '')}">${typologies}</div>
      </div>
      <div class="mj-rail-wrap">
        <div class="mj-rail" data-mj-rail tabindex="0" role="region" aria-label="${esc(s.residences?.selectLabel || '')}">
          ${units.map(unitCard).join('\n          ')}
        </div>
        <div class="mj-rail-nav" data-mj-rail-nav>
          <button type="button" data-mj-prev aria-label="${esc(t('aria.previous', locale))}"><span aria-hidden="true"></span></button>
          <button type="button" data-mj-next aria-label="${esc(t('aria.next', locale))}"><span aria-hidden="true"></span></button>
        </div>
      </div>
      <div class="mj-wrap">
        <p class="mj-note" data-mj-in="up">${esc(s.residences?.noteTotal || '')}</p>
        <p class="mj-note" data-mj-in="up">${esc(s.residences?.noteVat || '')}</p>
        <p class="mj-note" data-mj-in="up">${esc(project.availability.sourceNote || '')}</p>
        <div class="mj-actions" data-mj-in="up">${actionLink(t('cta.requestProjectMaterial', locale), '#enquire')}${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</div>
      </div>
    </section>

    <div class="mj-seam" aria-hidden="true"></div>

    <section class="mj-section mj-interiors" id="interiors" data-no="04">
      <div class="mj-wrap mj-interiors-grid">
        <div class="mj-interiors-copy">
          <span class="mj-kicker" data-mj-in="left">${esc(s.interiors?.kicker || '')}</span>
          <h2 data-mj-in="left" style="--d:.08s">${s.interiors?.headlineHtml || ''}</h2>
          <div class="mj-prose" data-mj-in="left" style="--d:.16s">${paragraphs(s.interiors?.copy)}</div>
        </div>
        <figure class="mj-interiors-lead" data-mj-in="wipe">${figure('kitchen-in-majolica-blue', '(max-width: 900px) 100vw, 48vw')}</figure>
      </div>
      <div class="mj-mosaic">
        <figure data-mj-in="left">${figure('living-room-in-emerald-green', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="right">${figure('dining-room-in-blue-sodalite', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="left">${figure('master-bedroom-with-sea-view', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="right">${figure('master-bathroom-in-sodalite', '(max-width: 900px) 100vw, 50vw')}</figure>
      </div>
      <div class="mj-mosaic mj-mosaic-wide">
        <figure data-mj-in="left">${figure('living-room-in-leopard-print', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="right">${figure('living-room-in-zebra-print', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="left">${figure('living-room-and-sodalite-bar', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="right">${figure('living-room-in-green-marble', '(max-width: 900px) 100vw, 50vw')}</figure>
      </div>
      <div class="mj-wrap">
        <p class="mj-palette-label" data-mj-in="up">${esc(s.interiors?.materialsLabel || '')}</p>
      </div>
      <div class="mj-stones">
        ${stones}
      </div>
    </section>

    <section class="mj-section mj-club" id="club" data-no="05">
      <div class="mj-club-hero">
        <figure data-mj-parallax>${figure('gold-bar-and-chandelier', '100vw')}</figure>
        <div class="mj-club-veil" aria-hidden="true"></div>
        <div class="mj-wrap mj-club-copy">
          <span class="mj-kicker" data-mj-in="left">${esc(s.club?.kicker || '')}</span>
          <h2 data-mj-in="left" style="--d:.08s">${s.club?.headlineHtml || ''}</h2>
          <p data-mj-in="left" style="--d:.16s">${esc(s.club?.copy || '')}</p>
        </div>
      </div>
      <div class="mj-wrap mj-club-rows">
        ${clubMarkup}
      </div>
    </section>

    <div class="mj-seam" aria-hidden="true"></div>

    <section class="mj-section mj-setting" id="setting" data-no="06">
      <div class="mj-wrap">
        <div class="mj-setting-grid">
          <div class="mj-head">
            <span class="mj-kicker" data-mj-in="left">${esc(s.location?.kicker || '')}</span>
            <h2 data-mj-in="left" style="--d:.08s">${project.location.headlineHtml}</h2>
            <p data-mj-in="left" style="--d:.16s">${esc(project.location.copy)}</p>
          </div>
          <div data-mj-in="right">
            <ul class="mj-distances">${distances}</ul>
            ${extras ? `<p class="mj-palette-label">${esc(s.location?.extrasLabel || '')}</p><ul class="mj-distances mj-distances-minor">${extras}</ul>` : ''}
          </div>
        </div>
        <p class="mj-note" data-mj-in="up">${esc(s.location?.note || '')}</p>
        <div class="mj-map" data-mj-in="up">${liveLocationMap ? renderLocationCard(project, locale) : ''}</div>
      </div>
      <figure class="mj-setting-aerial" data-mj-in="wipe">${figure('marbella-and-the-sierra-blanca', '100vw')}</figure>
      <div class="mj-duo">
        <figure data-mj-in="left">${figure('golden-mile-coast-and-pier', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-mj-in="right">${figure('master-suite-lounge-and-terrace', '(max-width: 900px) 100vw, 50vw')}</figure>
      </div>
    </section>

    <section class="mj-section mj-team" id="team">
      <div class="mj-wrap">
        <div class="mj-head">
          <span class="mj-kicker" data-mj-in="left">${esc(s.team?.kicker || '')}</span>
          <h2 data-mj-in="left" style="--d:.08s">${s.team?.headlineHtml || ''}</h2>
          <p data-mj-in="left" style="--d:.16s">${esc(s.team?.copy || '')}</p>
        </div>
        <div class="mj-team-grid">${teamCards}</div>
      </div>
    </section>

    ${projectMedia.section ? `<div class="mj-gallery">${projectMedia.section}</div>` : ''}

    <section class="mj-section mj-faq" id="faq">
      <div class="mj-wrap mj-faq-wrap">
        <div class="mj-head">
          <span class="mj-kicker" data-mj-in="left">${esc(t('section.faq', locale))}</span>
          <h2 data-mj-in="left" style="--d:.08s">${t('faq.headlineHtml', locale)}</h2>
        </div>
        <div class="faq-list mj-faq-list">
          ${faqs.map(([question, answer], index) => `<details class="faq-item"${index === 0 ? ' open' : ''}>
            <summary>${esc(question)}<span class="faq-toggle-icon" aria-hidden="true"></span></summary>
            <p>${esc(answer)}</p>
          </details>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="mj-section mj-enquire" id="enquire" data-no="07">
      <div class="mj-wrap mj-enquire-wrap">
        <div class="mj-head mj-enquire-head">
          <span class="mj-kicker" data-mj-in="left">${esc(t('section.enquireLabel', locale))}</span>
          <h2 data-mj-in="left" style="--d:.08s">${project.enquiry.headlineHtml}</h2>
          <p data-mj-in="left" style="--d:.16s">${esc(project.enquiry.copy)}</p>
          <p class="mj-enquire-private">${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</p>
        </div>
        <div class="mj-enquire-form" data-mj-in="right">${renderEnquiryForm(project, locale)}</div>
      </div>
    </section>

    <section class="mj-fine">
      <div class="mj-wrap">
        <p>${esc(s.disclaimer?.renders || '')}</p>
        <p>${esc(s.disclaimer?.independence || '')}</p>
      </div>
    </section>
`;
}
