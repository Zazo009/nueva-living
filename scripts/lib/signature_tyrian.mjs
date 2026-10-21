// The "tyrian" layout of the signature template.
//
// Third page of the family, and it is meant to read as its own house. Armani is a
// calm olive-and-ivory column; Design Hills is blue-and-white majolica sliding in
// from the sides. This one is built from the Tyrian brochure: the aubergine of its
// cover, the sand of its inner pages, the copper of its brand, the sweep of the
// terraces. Everything that moves does so the way a terrace does -- a slab
// sliding out from the building -- and the page's own centrepiece is the price list
// drawn as the building it is: four floors, west corner to east corner, every
// residence marked priced, reserved or sold.
//
// What it reads, beyond the standard record:
//   signature.*             copy that only this layout has
//   signature.grid          the whole building, floor by floor (English record is
//                           the source of the numbers and the statuses; the
//                           overlays only translate the words)
//   availability.units      the priced residences, one card each
//   signature.residences    the numbers behind each card, in the same order
//
// `signature.gridTypeNames` is deliberately never read: it maps unit numbers to the
// developer's own type names and is not for the page.

import fs from 'node:fs';

const readMark = (name, className) => fs.readFileSync(new URL(`../../assets/liora/signature-logos/${name}.svg`, import.meta.url), 'utf8')
  .replace(' xmlns="http://www.w3.org/2000/svg"', '')
  .replace('<svg ', `<svg class="${className}" aria-hidden="true" focusable="false" `)
  .trim();

const tyrianMark = readMark('tyrian-mark', 'ty-mark');

// One wave, used as the edge of a section. The path is a long, slow swell like the
// terrace edges in the brochure; `fill` is set by the class so the wave takes the
// colour of the section that follows it.
const wave = (tone, flip = false) => `<svg class="ty-wave ty-wave--${tone}${flip ? ' is-flip' : ''}" viewBox="0 0 1440 96" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 52C180 100 330 6 540 36S900 104 1100 58s240-34 340-6V96H0Z"/></svg>`;

const digits = (value = '') => Number(String(value).replace(/[^\d]/g, '')) || 0;

export function renderTyrianMain({ project, sourceProject, locale, faqs, projectMedia, helpers }) {
  const {
    esc, t, pictureTag, actionLink, ghostAction, whatsappHref,
    renderLocationCard, renderEnquiryForm, liveLocationMap, floorplanThumb, responsiveThumb,
    localizedUnitFloor, localizedUnitBedrooms, localizedUnitPrice
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
  const chapterIds = ['idea', 'building', 'residences', 'interiors', 'amenities', 'setting', 'enquire'];
  const chapters = (s.chapters || []).map((label, index) => [chapterIds[index], label]).filter(([id]) => id);
  const enquireLabel = project.enquiry.headlineHtml.replace(/<[^>]+>/g, '');
  const paragraphs = (list = []) => list.map((text) => `<p>${esc(text)}</p>`).join('');

  // ---- The building: the price list drawn as the elevation it is --------------
  const grid = s.grid || {};
  const enGrid = en.grid || {};
  const labels = grid.labels || {};
  const units = project.availability?.units || [];
  // The price list's own strings ("First floor", "3 bedrooms", "EUR 4,550,000 + VAT") are
  // data, not overlay prose, so they go through the same formatters as every unit table.
  const unitPrice = (unit) => localizedUnitPrice(unit.price, locale);
  // Plan figures are stored as "275.27 sqm": the unit and the decimal mark follow the locale.
  const SIZE_UNIT = { ru: 'м²', ar: 'م²' };
  const figureText = (value) => (locale === 'en' || !value ? value : String(value).replace(/(\d+)\.(\d+)\s*sqm\b/g, (_, whole, part) => `${whole}${locale === 'ar' ? '.' : ','}${part} ${SIZE_UNIT[locale] || 'm²'}`).replace(/(\d+)\s*sqm\b/g, `$1 ${SIZE_UNIT[locale] || 'm²'}`));
  const unitIndexOf = (number) => units.findIndex((unit) => String(unit.reference).trim() === String(number));
  const floors = (enGrid.floors || []).map((floor, floorIndex) => {
    const translated = grid.floors?.[floorIndex] || {};
    const homes = (floor.homes || []).map((home, homeIndex) => {
      const unitIndex = home.status === 'available' ? unitIndexOf(home.number) : -1;
      return {
        number: home.number,
        status: home.status,
        type: translated.homes?.[homeIndex]?.type || home.type || '',
        price: unitIndex >= 0 ? unitPrice(units[unitIndex]) : '',
        unitIndex
      };
    });
    return { label: labels.floors?.[floorIndex] || translated.label || floor.label, homes };
  });
  const statusLabel = (status) => labels[status] || status;
  const counts = { available: 0, reserved: 0, sold: 0 };
  floors.forEach((floor) => floor.homes.forEach((home) => { if (counts[home.status] !== undefined) counts[home.status] += 1; }));
  const firstPriced = floors.flatMap((floor, floorIndex) => floor.homes.map((home) => ({ ...home, floorIndex }))).find((home) => home.status === 'available');

  const cell = (home, floorIndex) => `<li><button type="button" class="ty-cell" data-status="${home.status}" data-ty-home data-floor="${floorIndex}" data-number="${esc(home.number)}" data-type="${esc(home.type)}" data-price="${esc(home.price)}" data-unit="${home.unitIndex >= 0 ? home.unitIndex + 1 : ''}" aria-pressed="${firstPriced && firstPriced.number === home.number ? 'true' : 'false'}" aria-label="${esc(`${home.number}, ${statusLabel(home.status)}${home.price ? `, ${home.price}` : ''}`)}"><span>${esc(home.number)}</span></button></li>`;
  const floorRow = (floor, floorIndex) => {
    const priced = floor.homes.filter((home) => home.status === 'available').length;
    return `<div class="ty-floor" data-ty-floor-row="${floorIndex}" data-ty-in="slab" style="--d:${floorIndex * 0.1}s">
          <button type="button" class="ty-floor-tab" data-ty-floor="${floorIndex}" aria-pressed="false"><b>${esc(floor.label)}</b><i>${priced}</i></button>
          <ol class="ty-slab">${floor.homes.map((home) => cell(home, floorIndex)).join('')}</ol>
        </div>`;
  };

  // ---- Residences ---------------------------------------------------------------
  const unitCard = (unit, index) => {
    const fig = s.residences?.figures?.[index] || {};
    const thumb = floorplanThumb(unit.floorplan);
    const planAlt = t('availability.floorplanOf', locale, { reference: unit.reference });
    const rows = [
      [s.residences?.interior, fig.interior],
      [s.residences?.terrace, fig.terrace],
      [s.residences?.garage, fig.garage],
      [s.residences?.storage, fig.storage],
      [s.residences?.usable, fig.usable],
      [s.residences?.total, fig.total]
    ].filter(([label, value]) => label && value);
    return `<article class="ty-unit" id="unit-${index + 1}" data-ty-in="up" style="--d:${(index % 3) * 0.08}s">
          ${thumb ? `<a class="ty-unit-plan" href="${esc(unit.floorplan)}" target="_blank" rel="noopener" aria-label="${esc(planAlt)}">${responsiveThumb(thumb, planAlt)}</a>` : ''}
          <div class="ty-unit-body">
            <p class="ty-unit-no">${esc(unit.reference)}</p>
            <p class="ty-unit-floor">${esc(localizedUnitFloor(unit.floor || '', locale))}</p>
            <p class="ty-unit-lead">${esc(localizedUnitBedrooms(unit.bedrooms, locale))}${s.residences?.baths?.[index] ? ` · ${esc(s.residences.baths[index])}` : ''}</p>
            ${rows.length ? `<dl class="ty-unit-facts">${rows.map(([label, value], row) => `<div${row === rows.length - 1 ? ' class="is-total"' : ''}><dt>${esc(label)}</dt><dd>${esc(figureText(value))}</dd></div>`).join('')}</dl>` : ''}
            <p class="ty-unit-price">${esc(unitPrice(unit))}</p>
            ${unit.floorplan ? `<a class="ty-unit-link" href="${esc(unit.floorplan)}" target="_blank" rel="noopener">${esc(s.residences?.planLabel || '')}</a>` : ''}
          </div>
        </article>`;
  };
  const typologies = (s.residences?.typologies || []).map(([name, text], index) => `<article class="ty-type" data-ty-in="up" style="--d:${index * 0.08}s"><span aria-hidden="true">${String(index + 1).padStart(2, '0')}</span><h3>${esc(name)}</h3><p>${esc(text)}</p></article>`).join('');

  // ---- Concept, materials, interiors ----------------------------------------------
  const palette = (s.concept?.palette || []).map(([name, text], index) => `<article class="ty-material" data-ty-in="up" style="--d:${index * 0.1}s"><i aria-hidden="true" data-tone="${index}"></i><h3>${esc(name)}</h3><p>${esc(text)}</p></article>`).join('');
  const rooms = s.interiors?.rooms || [];
  const roomImages = ['living-room-and-sea-view', 'kitchen-island-and-sea-view', 'main-bedroom-and-dressing-room', 'master-bathroom'];
  const roomFigures = roomImages.map((name, index) => `<figure class="ty-room ty-room--${index + 1}" data-ty-in="slab" style="--d:${index * 0.08}s"><div>${figure(name, '(max-width: 900px) 100vw, 46vw')}</div><figcaption>${esc(rooms[index] || '')}</figcaption></figure>`).join('');
  const samples = (s.interiors?.materials || []).map(([name, origin, text], index) => {
    const swatch = en.interiors?.swatches?.[index];
    return `<article class="ty-sample" data-ty-in="up" style="--d:${(index % 2) * 0.1}s">
          <div class="ty-sample-img">${swatch ? pictureTag({ ...swatch, alt: '' }, '', 'lazy', { sizes: '(max-width: 900px) 100vw, 46vw' }) : ''}</div>
          <div class="ty-sample-copy"><h3>${esc(name)}</h3>${origin ? `<span>${esc(origin)}</span>` : ''}<p>${esc(text)}</p></div>
        </article>`;
  }).join('\n        ');

  // ---- Amenities: one row per kind, picture on one side and words on the other -----
  const clubRows = [
    { group: 0, images: ['indoor-pool-hall', 'sauna'] },
    { group: 1, images: ['gym'] },
    { group: 2, images: ['rooftop-pool-from-above'] },
    { group: 3, images: ['culinary-experience-room', 'childrens-playroom'] },
    { group: 4, images: ['reception-desk-in-the-entrance-lobby'] },
    { group: 5, images: ['entrance-canopy-and-garden'] }
  ];
  const clubMarkup = clubRows.map((row, index) => {
    const [title, ...items] = (s.club?.groups || [])[row.group] || [];
    const flip = index % 2 === 1;
    const media = row.images.map((name, position) => `<figure class="${position ? 'is-small' : 'is-main'}">${figure(name, position ? '(max-width: 900px) 50vw, 20vw' : '(max-width: 900px) 100vw, 42vw')}</figure>`).join('');
    return `<div class="ty-club-row${flip ? ' is-flip' : ''}">
          <div class="ty-club-media${row.images.length > 1 ? ' has-pair' : ''}" data-ty-in="slab">${media}</div>
          <div class="ty-club-text" data-ty-in="up" style="--d:.12s"><span aria-hidden="true">${String(index + 1).padStart(2, '0')}</span><h3>${esc(title || '')}</h3><ul>${items.map((item) => `<li>${esc(item)}</li>`).join('')}</ul></div>
        </div>`;
  }).join('\n        ');

  const teamCards = (s.team?.cards || []).map(([role, name, detail], index) => `<article class="ty-member" data-ty-in="up" style="--d:${(index % 3) * 0.08}s"><span>${esc(role)}</span><h3>${esc(name)}</h3><p>${esc(detail)}</p></article>`).join('');
  const distances = (project.location?.distances || []).map(([label, value]) => `<li><span>${esc(label)}</span><strong>${esc(value)}</strong></li>`).join('');
  const extras = (s.location?.extras || []).map(([label, value]) => `<li><span>${esc(label)}</span><strong>${esc(value)}</strong></li>`).join('');
  const grounds = (s.blocks?.grounds || []).map((item, index) => `<li><i aria-hidden="true">${String(index + 1).padStart(2, '0')}</i><span>${esc(item)}</span></li>`).join('');

  return `
    <section class="ty-hero" id="top">
      <div class="ty-hero-media" data-ty-parallax>${pictureTag(heroImage, 'ty-hero-img', '', { priority: true, sizes: '100vw' })}</div>
      <div class="ty-hero-veil" aria-hidden="true"></div>
      <div class="ty-wrap ty-hero-inner">
        <p class="ty-eyebrow">${esc(project.hero.eyebrow)} <span aria-hidden="true">·</span> ${esc(project.hero.location)}</p>
        <h1 class="ty-title"><span class="ty-vh">${esc(project.name)}</span>${tyrianMark}</h1>
        <p class="ty-lead">${esc(s.lead || project.description)}</p>
        <div class="ty-hero-actions">
          ${actionLink(enquireLabel, '#enquire')}
          ${ghostAction(s.blocks?.kicker || t('cta.requestProjectMaterial', locale), '#building')}
        </div>
      </div>
      <ul class="ty-hero-facts ty-wrap" aria-label="${esc(t('aria.projectKeyFacts', locale))}">
        ${facts.map(([value, label]) => `<li><strong>${esc(value)}</strong><span>${esc(label)}</span></li>`).join('\n        ')}
      </ul>
      <svg class="ty-curves" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true" focusable="false">
        <path class="c1" data-ty-drift="0.22" d="M0 150C220 70 470 190 720 120S1180 60 1440 140V220H0Z"/>
        <path class="c2" data-ty-drift="0.12" d="M0 176C260 118 500 214 760 160S1190 116 1440 168V220H0Z"/>
        <path class="c3" d="M0 198C300 162 560 224 820 192S1230 168 1440 196V220H0Z"/>
      </svg>
      <div class="ty-curtain" aria-hidden="true"></div>
    </section>

    <nav class="ty-bar" aria-label="${esc(t('aria.projectSections', locale))}" data-ty-chapters>
      <div class="ty-wrap ty-bar-inner">
        <a class="ty-bar-brand" href="#top" aria-label="${esc(project.name)}">${readMark('tyrian-mark', 'ty-mark')}</a>
        <div class="ty-bar-links">
          ${chapters.map(([id, label], index) => `<a href="#${id}" data-chapter="${id}"><i>${String(index + 1).padStart(2, '0')}</i>${esc(label)}</a>`).join('\n          ')}
        </div>
        ${actionLink(enquireLabel, '#enquire', 'ty-bar-cta')}
      </div>
      <span class="ty-progress" data-ty-progress aria-hidden="true"></span>
    </nav>

    <section class="ty-section ty-idea" id="idea" data-no="01">
      <div class="ty-wrap ty-idea-grid">
        <div class="ty-idea-copy">
          <span class="ty-kicker" data-ty-in="up">${esc(s.concept?.kicker || '')}</span>
          <h2 data-ty-in="up" style="--d:.08s">${s.concept?.headlineHtml || ''}</h2>
          <div class="ty-prose" data-ty-in="up" style="--d:.16s">${paragraphs(s.concept?.paragraphs)}</div>
        </div>
        <div class="ty-idea-media">
          <figure class="is-main" data-ty-in="slab">${figure('corner-of-the-terraces', '(max-width: 900px) 100vw, 40vw')}</figure>
          <figure class="is-sketch" data-ty-in="slab" style="--d:.2s">${figure('architects-sketch-of-the-terraces', '(max-width: 900px) 60vw, 20vw')}</figure>
        </div>
      </div>
      <blockquote class="ty-pull" data-ty-in="up"><p>${esc(s.concept?.pull || '')}</p></blockquote>
      <div class="ty-wrap ty-materials">
        <p class="ty-label" data-ty-in="up">${esc(s.concept?.paletteLabel || '')}</p>
        <div class="ty-materials-row">${palette}</div>
      </div>
      <figure class="ty-banner" data-ty-in="slab"><div data-ty-parallax>${figure('curved-terraces-and-entrance-court', '100vw')}</div></figure>
    </section>
    ${wave('plum', true)}

    <section class="ty-section ty-building" id="building" data-no="02">
      <div class="ty-wrap">
        <div class="ty-head">
          <span class="ty-kicker" data-ty-in="up">${esc(s.blocks?.kicker || '')}</span>
          <h2 data-ty-in="up" style="--d:.08s">${s.blocks?.headlineHtml || ''}</h2>
          <p data-ty-in="up" style="--d:.16s">${esc(s.blocks?.copy || '')}</p>
        </div>
        <div class="ty-legend" data-ty-in="up" aria-label="${esc(grid.listDate || '')}">
          <span><i data-status="available"></i>${esc(statusLabel('available'))} · ${counts.available}</span>
          <span><i data-status="reserved"></i>${esc(statusLabel('reserved'))} · ${counts.reserved}</span>
          <span><i data-status="sold"></i>${esc(statusLabel('sold'))} · ${counts.sold}</span>
          <em>${esc(grid.listDate || '')}</em>
        </div>
        <div class="ty-elevation" data-ty-elevation>
          <p class="ty-compass" aria-hidden="true"><span>${esc(labels.westCorner || '')}</span><span>${esc(labels.eastCorner || '')}</span></p>
          ${floors.map(floorRow).join('\n          ')}
        </div>
        <div class="ty-detail" data-ty-detail aria-live="polite">
          <p class="ty-detail-no" data-ty-d-number>${esc(firstPriced?.number || '')}</p>
          <p class="ty-detail-status" data-ty-d-status data-status="${esc(firstPriced?.status || 'available')}">${esc(statusLabel(firstPriced?.status || 'available'))}</p>
          <p class="ty-detail-type" data-ty-d-type>${esc(firstPriced?.type || '')}</p>
          <p class="ty-detail-price" data-ty-d-price>${esc(firstPriced?.price || '')}</p>
          <a class="ty-detail-link" href="#unit-${(firstPriced?.unitIndex ?? 0) + 1}" data-ty-d-link${firstPriced?.unitIndex >= 0 ? '' : ' hidden'}>${esc(s.residences?.kicker || '')}<span aria-hidden="true"></span></a>
        </div>
        <p class="ty-note" data-ty-in="up">${esc(labels.priceNote || '')}</p>
        <ol class="ty-grounds" data-ty-in="up"><li class="ty-grounds-label">${esc(s.blocks?.groundsLabel || '')}</li>${grounds}</ol>
      </div>
      <figure class="ty-band" data-ty-in="slab"><div data-ty-parallax>${figure('front-elevation-across-the-gardens', '100vw')}</div></figure>
    </section>
    ${wave('sand')}

    <section class="ty-section ty-residences" id="residences" data-no="03">
      <div class="ty-wrap">
        <div class="ty-head">
          <span class="ty-kicker" data-ty-in="up">${esc(s.residences?.kicker || '')}</span>
          <h2 data-ty-in="up" style="--d:.08s">${project.residences.headlineHtml}</h2>
          <p data-ty-in="up" style="--d:.16s">${esc(project.residences.copy)}</p>
        </div>
        <div class="ty-types" aria-label="${esc(s.residences?.typologiesLabel || '')}">${typologies}</div>
      </div>
      <div class="ty-rail-wrap">
        <div class="ty-rail" data-ty-rail tabindex="0" role="region" aria-label="${esc(s.residences?.selectLabel || '')}">
          ${units.map(unitCard).join('\n          ')}
        </div>
        <div class="ty-rail-nav">
          <button type="button" data-ty-prev aria-label="${esc(t('aria.previous', locale))}"><span aria-hidden="true"></span></button>
          <button type="button" data-ty-next aria-label="${esc(t('aria.next', locale))}"><span aria-hidden="true"></span></button>
        </div>
      </div>
      <div class="ty-wrap">
        <p class="ty-note" data-ty-in="up">${esc(s.residences?.noteTotal || '')}</p>
        <p class="ty-note" data-ty-in="up">${esc(s.residences?.noteVat || '')}</p>
        <p class="ty-note" data-ty-in="up">${esc(project.availability.sourceNote || '')}</p>
        <div class="ty-actions" data-ty-in="up">${actionLink(t('cta.requestProjectMaterial', locale), '#enquire')}${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</div>
      </div>
    </section>
    ${wave('plum', true)}

    <section class="ty-section ty-interiors" id="interiors" data-no="04">
      <div class="ty-wrap ty-interiors-head">
        <div class="ty-head">
          <span class="ty-kicker" data-ty-in="up">${esc(s.interiors?.kicker || '')}</span>
          <h2 data-ty-in="up" style="--d:.08s">${s.interiors?.headlineHtml || ''}</h2>
        </div>
        <div class="ty-prose" data-ty-in="up" style="--d:.16s">${paragraphs(s.interiors?.copy)}</div>
      </div>
      <div class="ty-rooms">${roomFigures}</div>
      <div class="ty-wrap">
        <p class="ty-label" data-ty-in="up">${esc(s.interiors?.materialsLabel || '')}</p>
      </div>
      <div class="ty-samples">
        ${samples}
      </div>
      <div class="ty-terraces">
        <figure data-ty-in="slab">${figure('terrace-with-fire-table', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-ty-in="slab" style="--d:.12s">${figure('terrace-lounge-and-pergola', '(max-width: 900px) 100vw, 50vw')}</figure>
      </div>
    </section>
    ${wave('sand')}

    <section class="ty-section ty-amenities" id="amenities" data-no="05">
      <div class="ty-amenities-hero">
        <figure data-ty-parallax>${figure('rooftop-infinity-pool-at-dusk', '100vw')}</figure>
        <div class="ty-amenities-veil" aria-hidden="true"></div>
        <div class="ty-wrap ty-amenities-copy">
          <span class="ty-kicker" data-ty-in="up">${esc(s.club?.kicker || '')}</span>
          <h2 data-ty-in="up" style="--d:.08s">${s.club?.headlineHtml || ''}</h2>
          <p data-ty-in="up" style="--d:.16s">${esc(s.club?.copy || '')}</p>
        </div>
      </div>
      <div class="ty-wrap ty-club-rows">
        ${clubMarkup}
      </div>
    </section>
    ${wave('plum', true)}

    <section class="ty-section ty-setting" id="setting" data-no="06">
      <div class="ty-wrap">
        <div class="ty-setting-grid">
          <div class="ty-head">
            <span class="ty-kicker" data-ty-in="up">${esc(s.location?.kicker || '')}</span>
            <h2 data-ty-in="up" style="--d:.08s">${project.location.headlineHtml}</h2>
            <p data-ty-in="up" style="--d:.16s">${esc(project.location.copy)}</p>
          </div>
          <div data-ty-in="up" style="--d:.1s">
            <ul class="ty-distances">${distances}</ul>
            ${extras ? `<p class="ty-label">${esc(s.location?.extrasLabel || '')}</p><ul class="ty-distances ty-distances-minor">${extras}</ul>` : ''}
          </div>
        </div>
        <p class="ty-note" data-ty-in="up">${esc(s.location?.note || '')}</p>
        <div class="ty-map" data-ty-in="up">${liveLocationMap ? renderLocationCard(project, locale) : ''}</div>
      </div>
      <figure class="ty-setting-aerial" data-ty-in="slab">${figure('aerial-view-of-the-building-and-the-beach', '100vw')}</figure>
      <div class="ty-duo">
        <figure data-ty-in="slab">${figure('aerial-view-towards-the-mountains', '(max-width: 900px) 100vw, 50vw')}</figure>
        <figure data-ty-in="slab" style="--d:.12s">${figure('site-plan-with-gardens-and-beach', '(max-width: 900px) 100vw, 50vw')}</figure>
      </div>
    </section>

    <section class="ty-section ty-team" id="team">
      <div class="ty-wrap">
        <div class="ty-head">
          <span class="ty-kicker" data-ty-in="up">${esc(s.team?.kicker || '')}</span>
          <h2 data-ty-in="up" style="--d:.08s">${s.team?.headlineHtml || ''}</h2>
          <p data-ty-in="up" style="--d:.16s">${esc(s.team?.copy || '')}</p>
        </div>
        <div class="ty-team-grid">${teamCards}</div>
      </div>
    </section>

    ${projectMedia.section ? `<div class="ty-gallery">${projectMedia.section}</div>` : ''}

    <section class="ty-section ty-faq" id="faq">
      <div class="ty-wrap ty-faq-wrap">
        <div class="ty-head">
          <span class="ty-kicker" data-ty-in="up">${esc(t('section.faq', locale))}</span>
          <h2 data-ty-in="up" style="--d:.08s">${t('faq.headlineHtml', locale)}</h2>
        </div>
        <div class="faq-list ty-faq-list">
          ${faqs.map(([question, answer], index) => `<details class="faq-item"${index === 0 ? ' open' : ''}>
            <summary>${esc(question)}<span class="faq-toggle-icon" aria-hidden="true"></span></summary>
            <p>${esc(answer)}</p>
          </details>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="ty-section ty-enquire" id="enquire" data-no="07">
      <div class="ty-wrap ty-enquire-wrap">
        <div class="ty-head ty-enquire-head">
          <span class="ty-kicker" data-ty-in="up">${esc(t('section.enquireLabel', locale))}</span>
          <h2 data-ty-in="up" style="--d:.08s">${project.enquiry.headlineHtml}</h2>
          <p data-ty-in="up" style="--d:.16s">${esc(project.enquiry.copy)}</p>
          <p class="ty-enquire-private">${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</p>
        </div>
        <div class="ty-enquire-form" data-ty-in="up">${renderEnquiryForm(project, locale)}</div>
      </div>
    </section>

    <section class="ty-fine">
      <div class="ty-wrap">
        <p>${esc(s.disclaimer?.renders || '')}</p>
        <p>${esc(s.disclaimer?.independence || '')}</p>
      </div>
    </section>
`;
}
