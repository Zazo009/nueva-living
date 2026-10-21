// The "bentley" layout of the signature template.
//
// Fifth page of the family, for AÍDA, furnished by Bentley Home. It follows the brochure's own look:
// cream pages, tiny wide-tracked capitals, hairline rules between the lines of a list, square photographs,
// and one spread in the muted green of the Bentley Home page. Nothing here is a logo: the wordmark is set
// in type.
//
// What it reads, beyond the standard record:
//   signature.*             copy that only this layout has (keys below)
//   availability.units      the priced residences, matched to the eight tiles by their number
//
// Lists the content may write as pairs ([value, label]) or as objects ({value, label} / {title, text});
// both are read.

const pair = (item) => (Array.isArray(item)
  ? item
  : [item?.value ?? item?.title ?? item?.name ?? '', item?.label ?? item?.text ?? '']);

const digits = (value = '') => Number(String(value).match(/\d+/)?.[0]) || 0;

const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'];

export function renderBentleyMain({ project, sourceProject, locale, faqs, projectMedia, helpers }) {
  const {
    esc, t, pictureTag, actionLink, ghostAction, whatsappHref,
    renderLocationCard, renderEnquiryForm, liveLocationMap,
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
  const chapterIds = ['idea', 'bentley', 'residences', 'pitlane', 'rooms', 'goldenmile', 'enquire'];
  const chapters = (s.chapters || []).map((label, index) => [chapterIds[index], label]).filter(([id]) => id);
  const enquireLabel = project.enquiry.headlineHtml.replace(/<[^>]+>/g, '');
  const paragraphs = (list = []) => list.map((text) => `<p>${esc(text)}</p>`).join('');
  const head = (block = {}, delay = 0) => `<div class="bn-head">
          <span class="bn-kicker" data-bn-in="up">${esc(block.kicker || '')}</span>
          <h2 data-bn-in="up" style="--d:${(delay + 0.08).toFixed(2)}s">${block.headlineHtml || ''}</h2>
          ${block.copy ? `<p data-bn-in="up" style="--d:${(delay + 0.16).toFixed(2)}s">${esc(block.copy)}</p>` : ''}
        </div>`;

  const units = project.availability?.units || [];
  // The price list names the eight residences by the garage they pair with: 0A to 0D below ground, 1A to 1D above.
  const REFERENCES = ['0A', '0B', '0C', '0D', '1A', '1B', '1C', '1D'];
  const codeOf = (reference = '') => (String(reference).match(/\b([01])\s*([A-D])\b/i) || []).slice(1).join('').toUpperCase();
  const unitFor = (code) => units.find((unit) => codeOf(unit.reference) === code);
  const eight = REFERENCES.map((code, index) => ({ number: index + 1, code, unit: unitFor(code) }));
  const collection = s.collection || {};

  // ---- Hero figures: a plain row, ruled like the brochure's contents page ----------
  const dials = facts.map(([value, label], index) => `<li class="bn-dial" data-bn-in="up" style="--d:${(0.1 * index).toFixed(2)}s"><strong>${esc(value)}</strong><span>${esc(label)}</span></li>`).join('\n        ');

  // ---- The house's codes: six panels that follow the light ----------------------
  const codes = (s.bentley?.items || []).map((item, index) => {
    const [title, text] = pair(item);
    return `<article class="bn-card bn-code" data-bn-in="up" style="--d:${(index % 3) * 0.1}s">
          <span class="bn-code-no" aria-hidden="true">${ROMAN[index] || index + 1}</span>
          <div class="bn-code-img">${figure(item.image, '(max-width: 900px) 100vw, 30vw')}</div>
          <h3>${esc(title)}</h3>
          <p>${esc(text)}</p>
        </article>`;
  }).join('\n        ');

  // ---- The two residences, one switch -------------------------------------------
  const types = s.types?.items || [];
  const typeTabs = types.map((type, index) => `<button type="button" role="tab" class="bn-switch-btn${index === 0 ? ' is-active' : ''}" data-bn-type="${index}" aria-selected="${index === 0 ? 'true' : 'false'}" aria-controls="bn-type-${index}">${esc(type.name)}</button>`).join('');
  const typePanels = types.map((type, index) => `<article class="bn-type${index === 0 ? ' is-active' : ''}" id="bn-type-${index}" data-bn-type-panel="${index}" role="tabpanel"${index === 0 ? '' : ' hidden'}>
          <figure class="bn-type-img">${figure(type.image, '(max-width: 900px) 100vw, 56vw')}</figure>
          <div class="bn-type-copy">
            <p class="bn-type-tag">${esc(type.tagline || '')}</p>
            <h3>${esc(type.name)}</h3>
            <p>${esc(type.text || '')}</p>
            <ul class="bn-type-facts">${(type.facts || []).map(pair).map(([value, label]) => `<li><strong>${esc(value)}</strong><span>${esc(label)}</span></li>`).join('')}</ul>
            <ol class="bn-levels">${(type.floors || []).map((floor, level) => {
    const [name, text] = pair(floor);
    return `<li><i aria-hidden="true">${String(level + 1).padStart(2, '0')}</i><div><h4>${esc(name)}</h4><p>${esc(text)}</p></div></li>`;
  }).join('')}</ol>
          </div>
        </article>`).join('\n        ');

  // The developer's commercial plans, as published, under the two residences.
  const planItems = (project.media?.items || []).filter((item) => /floor\s?plan/i.test(item.category || ''));
  const plansStrip = planItems.length ? `<div class="bn-plans">${planItems.map((item, index) => `<figure class="bn-plan" data-bn-in="up" style="--d:${(index % 4) * 0.08}s"><a href="${esc(item.src)}" target="_blank" rel="noopener" aria-label="${esc(item.alt || item.caption || '')}">${pictureTag(item, '', 'lazy', { sizes: '(max-width: 900px) 100vw, 30vw' })}</a><figcaption>${esc(item.caption || '')}</figcaption></figure>`).join('')}</div>` : '';

  // The developer's film, when the project has one.
  const film = project.media?.video;
  const filmBlock = film?.desktopSrc ? `<figure class="bn-film" data-bn-in="frame">
          <video controls playsinline preload="none" poster="${esc(film.poster || '')}" aria-label="${esc(film.alt || film.title || '')}">
            ${film.mobileSrc ? `<source src="${esc(film.mobileSrc)}" type="video/mp4" media="(max-width: 700px)">` : ''}
            <source src="${esc(film.desktopSrc)}" type="video/mp4">
          </video>
          <figcaption><strong>${esc(film.title || '')}</strong><span>${esc(film.caption || '')}</span></figcaption>
        </figure>` : '';

  // ---- The pit lane --------------------------------------------------------------
  const pit = s.pitlane || {};
  const pitItems = (pit.items || []).map((item, index) => {
    const [title, text] = pair(item);
    return `<li data-bn-in="up" style="--d:${index * 0.12}s"><i aria-hidden="true">${String(index + 1).padStart(2, '0')}</i><div><h3>${esc(title)}</h3><p>${esc(text)}</p></div></li>`;
  }).join('');

  // ---- The rooms, as a theatre: the picture stays, the words scroll past it -------
  const rooms = s.rooms || [];
  const stage = rooms.map((room, index) => `<figure class="bn-stage-img${index === 0 ? ' is-active' : ''}" data-bn-stage="${index}">${figure(room.image, '(max-width: 900px) 100vw, 62vw')}</figure>`).join('');
  const steps = rooms.map((room, index) => `<li class="bn-step${index === 0 ? ' is-active' : ''}" data-bn-step="${index}">
            <p class="bn-step-no" aria-hidden="true"><b>${String(index + 1).padStart(2, '0')}</b> / ${String(rooms.length).padStart(2, '0')}</p>
            <h3>${esc(room.title)}</h3>
            <p>${esc(room.text)}</p>
          </li>`).join('\n          ');

  // ---- Wellness and the Golden Mile ------------------------------------------------
  const wellness = s.wellness || {};
  const wellnessItems = (wellness.items || []).map((item, index) => {
    const [title, text] = pair(item);
    return `<article class="bn-card bn-spa" data-bn-in="up" style="--d:${(index % 2) * 0.1}s"><div class="bn-spa-img">${figure(item.image, '(max-width: 900px) 100vw, 40vw')}</div><h3>${esc(title)}</h3><p>${esc(text)}</p></article>`;
  }).join('\n        ');
  const hotspots = (s.hotspots?.items || []).map((item, index) => {
    const [title, text] = pair(item);
    return `<article class="bn-card bn-spot" data-bn-in="up" style="--d:${(index % 4) * 0.08}s"><span aria-hidden="true">${String(index + 1).padStart(2, '0')}</span><h3>${esc(title)}</h3><p>${esc(text)}</p></article>`;
  }).join('\n        ');
  const distances = (project.location?.distances || []).map(([label, value]) => `<li><span>${esc(label)}</span><strong>${esc(value)}</strong></li>`).join('');
  const extras = (s.setting?.extras || []).map((item) => `<li>${esc(Array.isArray(item) ? item.join(' · ') : item)}</li>`).join('');

  // ---- The eight residences: two keys lit ----------------------------------------------
  const keyTile = ({ number, code, unit }) => `<article class="bn-keyfob${unit ? ' is-listed' : ''}" data-bn-in="up" style="--d:${((number - 1) % 4) * 0.08}s">
          <p class="bn-keyfob-no" aria-hidden="true">${ROMAN[number - 1]}</p>
          <h3>${esc(unit ? unit.reference : `${collection.villasLabel || ''} ${code}`.trim())}</h3>
          ${unit
    ? `<p class="bn-keyfob-price">${esc(localizedUnitPrice(unit.price, locale))}</p>
          <p class="bn-keyfob-spec">${esc([localizedUnitBedrooms(unit.bedrooms, locale), localizedUnitSize(unit.size, locale)].filter(Boolean).join(' · '))}</p>
          <p class="bn-keyfob-state">${esc(collection.availableLabel || '')}</p>
          ${unit.floorplan ? `<a class="bn-keyfob-plan" href="${esc(unit.floorplan)}" target="_blank" rel="noopener">${esc(t('availability.floorplan', locale))}</a>` : ''}`
    : `<p class="bn-keyfob-spec">${esc(collection.soldNote || '')}</p>
          <p class="bn-keyfob-state">${esc(collection.soldLabel || '')}</p>`}
        </article>`;

  const credits = (s.team?.credits || []).map((credit, index) => {
    const [role, name, text] = Array.isArray(credit) ? credit : [credit.role, credit.name, credit.text];
    return `<article class="bn-credit" data-bn-in="up" style="--d:${(index % 3) * 0.08}s"><span>${esc(role)}</span><h3>${esc(name)}</h3><p>${esc(text)}</p></article>`;
  }).join('');

  return `
    <section class="bn-hero" id="top">
      <div class="bn-wrap bn-hero-grid">
        <div class="bn-hero-copy">
          <p class="bn-eyebrow">${esc(project.hero.eyebrow)} <span aria-hidden="true">·</span> ${esc(project.hero.location)}</p>
          <h1 class="bn-title"><span>${esc(project.name)}</span></h1>
          <p class="bn-by"><i aria-hidden="true"></i><span>${esc(s.hero?.tagline || '')}</span><i aria-hidden="true"></i></p>
          <p class="bn-lead">${esc(s.heroLead || project.description)}</p>
          <div class="bn-actions">
            ${actionLink(enquireLabel, '#enquire')}
            ${ghostAction(collection.kicker || t('cta.requestProjectMaterial', locale), '#goldenmile')}
          </div>
        </div>
        <figure class="bn-bezel">
          <div class="bn-bezel-img">${pictureTag(heroImage, 'bn-hero-img', '', { priority: true, sizes: '100vw' })}</div>
        </figure>
      </div>
      <ul class="bn-wrap bn-dials" aria-label="${esc(t('aria.projectKeyFacts', locale))}">
        ${dials}
      </ul>
    </section>

    <nav class="bn-bar" aria-label="${esc(t('aria.projectSections', locale))}">
      <div class="bn-wrap bn-bar-inner">
        <a class="bn-bar-brand" href="#top">${esc(project.name)}</a>
        <div class="bn-bar-links">
          ${chapters.map(([id, label], index) => `<a href="#${id}" data-chapter="${id}"><i>${String(index + 1).padStart(2, '0')}</i>${esc(label)}</a>`).join('\n          ')}
        </div>
        ${actionLink(enquireLabel, '#enquire', 'bn-bar-cta')}
      </div>
      <span class="bn-progress" data-bn-progress aria-hidden="true"></span>
    </nav>

    <section class="bn-section bn-idea" id="idea" data-no="01">
      <div class="bn-wrap bn-idea-grid">
        <div class="bn-idea-copy">
          <span class="bn-kicker" data-bn-in="up">${esc(s.concept?.kicker || '')}</span>
          <h2 data-bn-in="up" style="--d:.08s">${s.concept?.headlineHtml || ''}</h2>
          <div class="bn-prose" data-bn-in="up" style="--d:.16s">${paragraphs(s.concept?.copy)}</div>
          ${s.concept?.pullQuote ? `<blockquote class="bn-pull" data-bn-in="up" style="--d:.24s"><p>${esc(s.concept.pullQuote)}</p></blockquote>` : ''}
        </div>
        <figure class="bn-chrome" data-bn-in="frame">${figure(s.concept?.image || 'garden-duplex-pool', '(max-width: 900px) 100vw, 46vw')}</figure>
      </div>
    </section>

    ${filmBlock ? `<section class="bn-section bn-filmsec" id="film">
      <div class="bn-wrap">
        ${head(s.film)}
        ${filmBlock}
      </div>
    </section>` : ''}

    <section class="bn-section bn-bentley" id="bentley" data-no="02">
      <div class="bn-wrap">
        ${head(s.bentley)}
        <div class="bn-codes">
        ${codes}
        </div>
      </div>
    </section>

    <section class="bn-section bn-types" id="residences" data-no="03">
      <div class="bn-wrap">
        ${head(s.types)}
        <div class="bn-switch" role="tablist" data-bn-switch>${typeTabs}<span class="bn-switch-thumb" aria-hidden="true"></span></div>
        <div class="bn-type-stage">
        ${typePanels}
        </div>
        ${plansStrip}
      </div>
    </section>

    <section class="bn-section bn-pit" id="pitlane" data-no="04">
      <div class="bn-wrap bn-pit-grid">
        <div class="bn-pit-copy">
          <span class="bn-kicker" data-bn-in="up">${esc(pit.kicker || '')}</span>
          <h2 data-bn-in="up" style="--d:.08s">${pit.headlineHtml || ''}</h2>
          <p class="bn-pit-lead" data-bn-in="up" style="--d:.16s">${esc(pit.copy || '')}</p>
          <ol class="bn-pit-list">${pitItems}</ol>
          ${pit.note ? `<p class="bn-note" data-bn-in="up">${esc(pit.note)}</p>` : ''}
        </div>
        <div class="bn-pit-visual" data-bn-in="frame">
          ${pit.image ? `<figure class="bn-pit-img">${figure(pit.image, '(max-width: 900px) 100vw, 50vw')}</figure>` : ''}
        </div>
      </div>
    </section>

    <section class="bn-section bn-rooms" id="rooms" data-no="05">
      <div class="bn-wrap">
        ${head(s.roomsHead)}
      </div>
      <div class="bn-wrap bn-theatre" data-bn-theatre>
        <div class="bn-stage" data-bn-in="frame">${stage}</div>
        <ol class="bn-steps">
          ${steps}
        </ol>
      </div>
    </section>

    <section class="bn-section bn-wellness" id="wellness" data-no="06">
      <div class="bn-wrap">
        ${head(wellness)}
        <div class="bn-spa-grid">
        ${wellnessItems}
        </div>
      </div>
    </section>

    <section class="bn-section bn-golden" id="goldenmile" data-no="07">
      <div class="bn-wrap">
        ${head(s.hotspots)}
        <div class="bn-spots">
        ${hotspots}
        </div>
        <div class="bn-setting-grid">
          <div class="bn-head">
            <span class="bn-kicker" data-bn-in="up">${esc(s.setting?.kicker || '')}</span>
            <h2 data-bn-in="up" style="--d:.08s">${project.location.headlineHtml}</h2>
            <p data-bn-in="up" style="--d:.16s">${esc(project.location.copy)}</p>
          </div>
          <div data-bn-in="up" style="--d:.1s">
            <ul class="bn-distances">${distances}</ul>
            ${extras ? `<ul class="bn-extras">${extras}</ul>` : ''}
          </div>
        </div>
        <div class="bn-map" data-bn-in="up">${liveLocationMap ? renderLocationCard(project, locale) : ''}</div>
      </div>
      ${s.setting?.aerialImage ? `<figure class="bn-aerial" data-bn-in="frame">${figure(s.setting.aerialImage, '100vw')}</figure>` : ''}
    </section>

    <section class="bn-section bn-collection" id="collection">
      <div class="bn-wrap">
        ${head(collection)}
        <div class="bn-keyfobs">${eight.map(keyTile).join('\n        ')}</div>
        ${collection.priceNote ? `<p class="bn-note" data-bn-in="up">${esc(collection.priceNote)}</p>` : ''}
        ${project.availability?.sourceNote ? `<p class="bn-note" data-bn-in="up">${esc(project.availability.sourceNote)}</p>` : ''}
        <div class="bn-actions" data-bn-in="up">${actionLink(t('cta.requestProjectMaterial', locale), '#enquire')}${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</div>
      </div>
    </section>

    <section class="bn-section bn-team" id="team">
      <div class="bn-wrap">
        ${head(s.team)}
        <div class="bn-credits">${credits}</div>
      </div>
    </section>

    ${projectMedia.section ? `<div class="bn-gallery">${projectMedia.section}</div>` : ''}

    <section class="bn-section bn-faq" id="faq">
      <div class="bn-wrap bn-faq-wrap">
        <div class="bn-head">
          <span class="bn-kicker" data-bn-in="up">${esc(t('section.faq', locale))}</span>
          <h2 data-bn-in="up" style="--d:.08s">${t('faq.headlineHtml', locale)}</h2>
        </div>
        <div class="faq-list bn-faq-list">
          ${faqs.map(([question, answer], index) => `<details class="faq-item"${index === 0 ? ' open' : ''}>
            <summary>${esc(question)}<span class="faq-toggle-icon" aria-hidden="true"></span></summary>
            <p>${esc(answer)}</p>
          </details>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="bn-section bn-enquire" id="enquire" data-no="08">
      <div class="bn-wrap bn-enquire-wrap">
        <div class="bn-head bn-enquire-head">
          <span class="bn-kicker" data-bn-in="up">${esc(t('section.enquireLabel', locale))}</span>
          <h2 data-bn-in="up" style="--d:.08s">${project.enquiry.headlineHtml}</h2>
          <p data-bn-in="up" style="--d:.16s">${esc(project.enquiry.copy)}</p>
          <p class="bn-enquire-private">${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</p>
        </div>
        <div class="bn-enquire-form" data-bn-in="up">${renderEnquiryForm(project, locale)}</div>
      </div>
    </section>

    <section class="bn-fine">
      <div class="bn-wrap">
        <p>${esc(s.disclaimer?.renders || s.disclaimer || '')}</p>
        ${s.disclaimer?.independence ? `<p>${esc(s.disclaimer.independence)}</p>` : ''}
      </div>
    </section>
`;
}
