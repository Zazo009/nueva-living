// The "versace" layout of the signature template.
//
// Fourth page of the family, for Ocho de Oro, whose interiors are by Versace Home.
// Armani is an olive-and-ivory column, Design Hills is majolica, Tyrian is aubergine
// terraces. This one is black, gold and marble, edged with the Greek key (a plain
// meander drawn here as a repeating border, not anyone's logo), and it is organised
// around the three things the dossier is about: the house's hand in the rooms, the
// walk through them, and the eight villas themselves.
//
// What it reads, beyond the standard record:
//   signature.*             copy that only this layout has (see the keys below)
//   availability.units      the priced villas, matched to the eight tiles by their number
//
// Lists the content may write either as pairs ([value, label]) or as objects
// ({value, label} / {title, text}); both are read.

const pair = (item) => (Array.isArray(item)
  ? item
  : [item?.value ?? item?.title ?? item?.name ?? '', item?.label ?? item?.text ?? '']);

const digits = (value = '') => Number(String(value).match(/\d+/)?.[0]) || 0;

const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'];

export function renderVersaceMain({ project, sourceProject, locale, faqs, projectMedia, helpers }) {
  const {
    esc, t, pictureTag, actionLink, ghostAction, whatsappHref,
    renderLocationCard, renderEnquiryForm, liveLocationMap, responsiveThumb,
    localizedUnitBedrooms, localizedUnitPrice, localizedUnitSize
  } = helpers;
  const s = project.signature || {};
  const mediaByName = (name) => (project.media?.items || []).find((item) => item.src.includes(`/${name}.`));
  const figure = (name, sizes = '(max-width: 900px) 100vw, 50vw', loading = 'lazy') => {
    const image = mediaByName(name);
    return image ? pictureTag(image, '', loading, { sizes }) : '';
  };
  const heroImage = project.images.hero;
  const facts = (s.heroFacts || []).map(pair);
  const chapterIds = ['idea', 'versace', 'villa', 'rooms', 'wellness', 'collection', 'enquire'];
  const chapters = (s.chapters || []).map((label, index) => [chapterIds[index], label]).filter(([id]) => id);
  const enquireLabel = project.enquiry.headlineHtml.replace(/<[^>]+>/g, '');
  const paragraphs = (list = []) => list.map((text) => `<p>${esc(text)}</p>`).join('');
  const head = (block = {}, delay = 0) => `<div class="vs-head">
          <span class="vs-kicker" data-vs-in="up">${esc(block.kicker || '')}</span>
          <h2 data-vs-in="up" style="--d:${(delay + 0.08).toFixed(2)}s">${block.headlineHtml || ''}</h2>
          ${block.copy ? `<p data-vs-in="up" style="--d:${(delay + 0.16).toFixed(2)}s">${esc(block.copy)}</p>` : ''}
        </div>`;

  // ---- The eight villas, as eight keys: lit when they have a price ------------
  const units = project.availability?.units || [];
  const unitFor = (number) => units.find((unit) => digits(unit.reference) === number);
  const eight = Array.from({ length: 8 }, (_, index) => ({ number: index + 1, unit: unitFor(index + 1) }));
  const pricedCount = eight.filter((villa) => villa.unit).length;
  const collection = s.collection || {};
  const keys = eight.map((villa) => `<i class="${villa.unit ? 'is-lit' : ''}"></i>`).join('');

  // The unit table's own size strings come from the English price list; the area unit follows the language.
  const AREA_UNIT = { ru: 'м²', ar: 'م²' };
  const areaText = (value) => (AREA_UNIT[locale] ? String(value || '').replace(/m²/g, AREA_UNIT[locale]) : value);

  const villaTile = ({ number, unit }) => {
    const plan = unit?.floorplan || unit?.plan;
    return `<article class="vs-villa${unit ? ' is-listed' : ''}" data-vs-in="up" style="--d:${((number - 1) % 4) * 0.08}s">
          <p class="vs-villa-no" aria-hidden="true">${ROMAN[number - 1]}</p>
          <h3>${esc(`${collection.villasLabel || ''} ${number}`.trim())}</h3>
          ${unit
    ? `<p class="vs-villa-price">${esc(localizedUnitPrice(unit.price, locale))}</p>
          <p class="vs-villa-spec">${esc([localizedUnitBedrooms(unit.bedrooms, locale), areaText(localizedUnitSize(unit.size, locale))].filter(Boolean).join(' · '))}</p>
          <p class="vs-villa-state">${esc(collection.availableLabel || '')}</p>
          ${plan ? `<a class="vs-villa-plan" href="${esc(plan)}" target="_blank" rel="noopener">${esc(t('availability.floorplan', locale))}</a>` : ''}`
    : `<p class="vs-villa-spec">${esc(collection.soldNote || '')}</p>
          <p class="vs-villa-state">${esc(collection.soldLabel || '')}</p>`}
        </article>`;
  };

  // ---- The house's hand: a catalogue the reader turns through -----------------
  const touches = (s.versace?.items || []).map(pair).map(([title, text], index) => ({
    title, text, image: (s.versace.items[index] || {}).image || ''
  }));
  const touchStage = touches.map((touch, index) => `<figure class="vs-touch-img${index === 0 ? ' is-active' : ''}" data-vs-touch-img="${index}">${figure(touch.image, '(max-width: 900px) 100vw, 52vw', index === 0 ? 'lazy' : 'lazy')}</figure>`).join('');
  const touchList = touches.map((touch, index) => `<li>
            <button type="button" class="vs-touch${index === 0 ? ' is-active' : ''}" data-vs-touch="${index}" aria-pressed="${index === 0 ? 'true' : 'false'}">
              <i aria-hidden="true">${ROMAN[index] || index + 1}</i><span>${esc(touch.title)}</span>
            </button>
            <p class="vs-touch-text">${esc(touch.text)}</p>
          </li>`).join('\n          ');

  // ---- The villa ---------------------------------------------------------------
  const villaFacts = (s.villa?.facts || []).map(pair).map(([value, label]) => `<li data-vs-in="up"><strong>${esc(value)}</strong><span>${esc(label)}</span></li>`).join('');
  const floorCols = (s.villa?.floors || []).map((floor, index) => {
    const name = floor.name ?? floor[0] ?? '';
    const items = floor.items ?? floor[1] ?? [];
    return `<article class="vs-floor" data-vs-in="up" style="--d:${index * 0.1}s">
          <p class="vs-floor-no" aria-hidden="true">${ROMAN[index]}</p>
          <h3>${esc(name)}</h3>
          <ul>${items.map((item) => `<li>${esc(item)}</li>`).join('')}</ul>
        </article>`;
  }).join('');
  const plans = (s.villa?.plans || []).map((plan) => `<figure class="vs-plan" data-vs-in="up">
          <a href="${esc(plan.src)}" target="_blank" rel="noopener" aria-label="${esc(plan.alt || plan.label || '')}">${responsiveThumb ? responsiveThumb(plan.src, plan.alt || plan.label || '') : `<img src="${esc(plan.src)}" alt="${esc(plan.alt || '')}" loading="lazy">`}</a>
          <figcaption>${esc(plan.label || '')}</figcaption>
        </figure>`).join('');

  // ---- The rooms: one large view, a strip of the rest --------------------------
  const rooms = s.rooms || [];
  const slides = rooms.map((room, index) => `<article class="vs-slide${index === 0 ? ' is-active' : ''}" data-vs-slide="${index}"${index === 0 ? '' : ' aria-hidden="true"'}>
            <div class="vs-slide-img">${figure(room.image, '(max-width: 900px) 100vw, 66vw', index === 0 ? 'lazy' : 'lazy')}</div>
            <div class="vs-slide-copy"><p class="vs-slide-count" aria-hidden="true"><b data-vs-count>${String(index + 1).padStart(2, '0')}</b> / ${String(rooms.length).padStart(2, '0')}</p><h3>${esc(room.title)}</h3><p>${esc(room.text)}</p></div>
          </article>`).join('\n          ');
  const thumbs = rooms.map((room, index) => `<button type="button" class="vs-thumb${index === 0 ? ' is-active' : ''}" data-vs-thumb="${index}" aria-label="${esc(room.title)}" aria-pressed="${index === 0 ? 'true' : 'false'}">${figure(room.image, '120px')}</button>`).join('');

  // ---- Wellness and outdoors: two panels of four -----------------------------------
  const panel = (block = {}, tone) => `<div class="vs-panel vs-panel--${tone}">
        ${head(block)}
        <div class="vs-quad">
          ${(block.items || []).map((item, index) => {
    const [title, text] = pair(item);
    return `<article class="vs-quad-item" data-vs-in="up" style="--d:${(index % 2) * 0.1}s"><div class="vs-quad-img">${figure(item.image, '(max-width: 900px) 100vw, 40vw')}</div><h3>${esc(title)}</h3><p>${esc(text)}</p></article>`;
  }).join('\n          ')}
        </div>
      </div>`;

  const distances = (project.location?.distances || []).map(([label, value]) => `<li><span>${esc(label)}</span><strong>${esc(value)}</strong></li>`).join('');
  const extras = (s.setting?.extras || []).map((item) => `<li>${esc(Array.isArray(item) ? item.join(' · ') : item)}</li>`).join('');
  const credits = (s.team?.credits || []).map((credit, index) => {
    const [role, name, text] = Array.isArray(credit) ? credit : [credit.role, credit.name, credit.text];
    return `<article class="vs-credit" data-vs-in="up" style="--d:${(index % 3) * 0.08}s"><span>${esc(role)}</span><h3>${esc(name)}</h3><p>${esc(text)}</p></article>`;
  }).join('');

  return `
    <section class="vs-hero" id="top">
      <div class="vs-hero-media">${pictureTag(heroImage, 'vs-hero-img', '', { priority: true, sizes: '100vw' })}</div>
      <div class="vs-hero-veil" aria-hidden="true"></div>
      <div class="vs-wrap vs-hero-inner">
        <p class="vs-eyebrow">${esc(project.hero.eyebrow)} <span aria-hidden="true">·</span> ${esc(project.hero.location)}</p>
        <h1 class="vs-title">${esc(project.name)}</h1>
        <p class="vs-by"><span class="vs-greca vs-greca--short" aria-hidden="true"></span><span>${esc(s.hero?.tagline || '')}</span><span class="vs-greca vs-greca--short" aria-hidden="true"></span></p>
        <p class="vs-lead">${esc(s.heroLead || project.description)}</p>
        <div class="vs-hero-actions">
          ${actionLink(enquireLabel, '#enquire')}
          ${ghostAction(collection.kicker || t('cta.requestProjectMaterial', locale), '#collection')}
        </div>
      </div>
      <div class="vs-wrap vs-hero-base">
        <p class="vs-keys" role="img" aria-label="${esc(`${pricedCount} / 8`)}">${keys}</p>
        <ul class="vs-hero-facts" aria-label="${esc(t('aria.projectKeyFacts', locale))}">
          ${facts.map(([value, label]) => `<li><strong>${esc(value)}</strong><span>${esc(label)}</span></li>`).join('\n          ')}
        </ul>
      </div>
      <span class="vs-greca vs-greca--edge" aria-hidden="true"></span>
    </section>

    <nav class="vs-bar" aria-label="${esc(t('aria.projectSections', locale))}">
      <div class="vs-wrap vs-bar-inner">
        <a class="vs-bar-brand" href="#top">${esc(project.name)}</a>
        <div class="vs-bar-links">
          ${chapters.map(([id, label], index) => `<a href="#${id}" data-chapter="${id}"><i>${String(index + 1).padStart(2, '0')}</i>${esc(label)}</a>`).join('\n          ')}
        </div>
        ${actionLink(enquireLabel, '#enquire', 'vs-bar-cta')}
      </div>
      <span class="vs-progress" data-vs-progress aria-hidden="true"></span>
    </nav>

    <section class="vs-section vs-idea" id="idea" data-no="01">
      <div class="vs-wrap vs-idea-grid">
        <div class="vs-idea-copy">
          <span class="vs-kicker" data-vs-in="up">${esc(s.concept?.kicker || '')}</span>
          <h2 data-vs-in="up" style="--d:.08s">${s.concept?.headlineHtml || ''}</h2>
          <div class="vs-prose" data-vs-in="up" style="--d:.16s">${paragraphs(s.concept?.copy)}</div>
          ${s.concept?.pullQuote ? `<blockquote class="vs-pull" data-vs-in="up" style="--d:.24s"><p>${esc(s.concept.pullQuote)}</p></blockquote>` : ''}
        </div>
        <figure class="vs-framed" data-vs-in="frame">${figure(s.concept?.image || 'villa-exterior-pool', '(max-width: 900px) 100vw, 46vw')}</figure>
      </div>
    </section>

    <section class="vs-section vs-versace" id="versace" data-no="02">
      <span class="vs-greca vs-greca--edge vs-greca--top" aria-hidden="true"></span>
      <div class="vs-wrap">
        ${head(s.versace)}
        <div class="vs-touches" data-vs-touches>
          <div class="vs-touch-stage" data-vs-in="frame">${touchStage}</div>
          <ol class="vs-touch-list">
          ${touchList}
          </ol>
        </div>
      </div>
    </section>

    <section class="vs-section vs-villa-sec" id="villa" data-no="03">
      <div class="vs-wrap">
        ${head(s.villa)}
        <ul class="vs-facts">${villaFacts}</ul>
        <div class="vs-floors">${floorCols}</div>
        ${s.villa?.planNote ? `<p class="vs-note" data-vs-in="up">${esc(s.villa.planNote)}</p>` : ''}
        ${plans ? `<div class="vs-plans">${plans}</div>` : ''}
      </div>
    </section>

    <section class="vs-section vs-rooms" id="rooms" data-no="04">
      <span class="vs-greca vs-greca--edge vs-greca--top" aria-hidden="true"></span>
      <div class="vs-wrap">
        ${head({ kicker: s.roomsHead?.kicker || '', headlineHtml: s.roomsHead?.headlineHtml || '', copy: s.roomsHead?.copy || '' })}
        <div class="vs-viewer" data-vs-viewer>
          <div class="vs-slides" data-vs-in="frame">
          ${slides}
          </div>
          <div class="vs-viewer-nav">
            <button type="button" data-vs-prev aria-label="${esc(t('aria.previous', locale))}"><span aria-hidden="true"></span></button>
            <button type="button" data-vs-next aria-label="${esc(t('aria.next', locale))}"><span aria-hidden="true"></span></button>
          </div>
          <div class="vs-thumbs" data-vs-thumbs>${thumbs}</div>
        </div>
      </div>
    </section>

    <section class="vs-section vs-wellness" id="wellness" data-no="05">
      <div class="vs-wrap">
        ${panel(s.wellness, 'wellness')}
        ${panel(s.outdoors, 'outdoors')}
      </div>
    </section>

    <section class="vs-section vs-collection" id="collection" data-no="06">
      <span class="vs-greca vs-greca--edge vs-greca--top" aria-hidden="true"></span>
      <div class="vs-wrap">
        ${head(collection)}
        <figure class="vs-masterplan" data-vs-in="frame">${figure(s.setting?.masterplanImage || 'masterplan', '(max-width: 900px) 100vw, 80vw')}</figure>
        <div class="vs-villas">${eight.map(villaTile).join('\n        ')}</div>
        ${collection.priceNote ? `<p class="vs-note" data-vs-in="up">${esc(collection.priceNote)}</p>` : ''}
        ${project.availability?.sourceNote ? `<p class="vs-note" data-vs-in="up">${esc(project.availability.sourceNote)}</p>` : ''}
        <div class="vs-actions" data-vs-in="up">${actionLink(t('cta.requestProjectMaterial', locale), '#enquire')}${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</div>
      </div>
    </section>

    <section class="vs-section vs-setting" id="setting">
      <div class="vs-wrap">
        <div class="vs-setting-grid">
          <div class="vs-head">
            <span class="vs-kicker" data-vs-in="up">${esc(s.setting?.kicker || '')}</span>
            <h2 data-vs-in="up" style="--d:.08s">${project.location.headlineHtml}</h2>
            <p data-vs-in="up" style="--d:.16s">${esc(project.location.copy)}</p>
          </div>
          <div data-vs-in="up" style="--d:.1s">
            <ul class="vs-distances">${distances}</ul>
            ${extras ? `<ul class="vs-extras">${extras}</ul>` : ''}
          </div>
        </div>
        <div class="vs-map" data-vs-in="up">${liveLocationMap ? renderLocationCard(project, locale) : ''}</div>
      </div>
      ${s.setting?.aerialImage ? `<figure class="vs-aerial" data-vs-in="frame">${figure(s.setting.aerialImage, '100vw')}</figure>` : ''}
    </section>

    <section class="vs-section vs-team" id="team">
      <div class="vs-wrap">
        ${head(s.team)}
        <div class="vs-credits">${credits}</div>
      </div>
    </section>

    ${projectMedia.section ? `<div class="vs-gallery">${projectMedia.section}</div>` : ''}

    <section class="vs-section vs-faq" id="faq">
      <div class="vs-wrap vs-faq-wrap">
        <div class="vs-head">
          <span class="vs-kicker" data-vs-in="up">${esc(t('section.faq', locale))}</span>
          <h2 data-vs-in="up" style="--d:.08s">${t('faq.headlineHtml', locale)}</h2>
        </div>
        <div class="faq-list vs-faq-list">
          ${faqs.map(([question, answer], index) => `<details class="faq-item"${index === 0 ? ' open' : ''}>
            <summary>${esc(question)}<span class="faq-toggle-icon" aria-hidden="true"></span></summary>
            <p>${esc(answer)}</p>
          </details>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="vs-section vs-enquire" id="enquire" data-no="07">
      <span class="vs-greca vs-greca--edge vs-greca--top" aria-hidden="true"></span>
      <div class="vs-wrap vs-enquire-wrap">
        <div class="vs-head vs-enquire-head">
          <span class="vs-kicker" data-vs-in="up">${esc(t('section.enquireLabel', locale))}</span>
          <h2 data-vs-in="up" style="--d:.08s">${project.enquiry.headlineHtml}</h2>
          <p data-vs-in="up" style="--d:.16s">${esc(project.enquiry.copy)}</p>
          <p class="vs-enquire-private">${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</p>
        </div>
        <div class="vs-enquire-form" data-vs-in="up">${renderEnquiryForm(project, locale)}</div>
      </div>
    </section>

    <section class="vs-fine">
      <div class="vs-wrap">
        <p>${esc(s.disclaimer?.renders || s.disclaimer || '')}</p>
        ${s.disclaimer?.independence ? `<p>${esc(s.disclaimer.independence)}</p>` : ''}
      </div>
    </section>
`;
}
