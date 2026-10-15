import fs from 'node:fs';

// The "signature" project template.
//
// A project that sets `"template": "signature"` keeps the whole project record
// (cards, search, compare, CRM sync, schema, the enquiry form, the live map)
// but gets its own page body: a long, single-column editorial layout with its
// own palette, its own type and its own chapter navigation. It exists for the
// handful of projects that are sold on a name and an atmosphere, where the
// standard project page -- built for comparing many similar apartments -- would
// flatten them.
//
// What it reads, beyond the standard record:
//   signature.*   copy that only this template has (hero lead, the concept,
//                 the masterplan, wellness, the team, the disclaimers)
//   residences    the types, as the standard cards carry them; the size bars
//                 are drawn from the numbers in the ENGLISH meta values, so a
//                 translation can never change a bar
//   media         the gallery and the film, through the standard renderer
//
// Everything visible is either a string from the record (translated by the
// overlays like any other) or derived from numbers in it. Nothing here is
// typed prose.

const RANGE = /(\d[\d,.]*)\s*(?:-|–|to)\s*(\d[\d,.]*)/;

function numbers(value = '') {
  const match = String(value).match(RANGE);
  if (!match) return null;
  const read = (text) => Number(text.replace(/[,]/g, ''));
  const low = read(match[1]);
  const high = read(match[2]);
  return Number.isFinite(low) && Number.isFinite(high) ? [low, high] : null;
}

function metaValue(item, index) {
  const row = item?.meta?.[index];
  return Array.isArray(row) ? row[1] : '';
}

// The wordmark is the developer's own logotype, drawn as vector paths and
// inlined so it takes the colour of whatever it sits on. The words "Armani"
// stay in the heading as hidden text: the logo is a picture of them.
const armaniMark = fs.readFileSync(new URL('../../assets/liora/signature-logos/armani-mark.svg', import.meta.url), 'utf8')
  .replace(' xmlns="http://www.w3.org/2000/svg"', '')
  .replace('<svg ', '<svg class="sig-mark" aria-hidden="true" focusable="false" ')
  .trim();

export function renderSignatureMain({ project, sourceProject, locale, faqs, projectMedia, privateHref, helpers }) {
  const {
    esc, t, pictureTag, actionLink, ghostAction, whatsappHref,
    renderLocationCard, renderEnquiryForm, liveLocationMap
  } = helpers;
  const s = project.signature || {};
  const en = sourceProject.signature || {};
  const mediaByName = (name) => (project.media?.items || []).find((item) => item.src.includes(`/${name}.`));
  const figure = (name, className = '', sizes = '(max-width: 900px) 100vw, 60vw', loading = 'lazy') => {
    const image = mediaByName(name);
    return image ? pictureTag(image, className, loading, { sizes }) : '';
  };
  const heroImage = project.images.hero;
  const facts = s.heroFacts || [];
  const chapterIds = ['concept', 'masterplan', 'residences', 'interiors', 'wellness', 'setting', 'enquire'];
  const chapters = (s.chapters || []).map((label, index) => [chapterIds[index], label]).filter(([id]) => id);

  // Size bars: one shared scale across all three types, so the eye can compare.
  const englishTypes = sourceProject.residences?.items || [];
  const interiorRanges = englishTypes.map((item) => numbers(metaValue(item, 1)));
  const totalRanges = englishTypes.map((item) => numbers(metaValue(item, 2)));
  const scaleMax = Math.max(0, ...interiorRanges.concat(totalRanges).filter(Boolean).map((range) => range[1]));
  const bar = (range) => {
    if (!range || !scaleMax) return '';
    const left = (range[0] / scaleMax) * 100;
    const width = ((range[1] - range[0]) / scaleMax) * 100;
    return `<span class="sig-bar" aria-hidden="true"><i style="inset-inline-start:${left.toFixed(1)}%;width:${width.toFixed(1)}%"></i></span>`;
  };

  const typeCards = (project.residences?.items || []).map((item, index) => {
    const meta = item.meta || [];
    return `<article class="sig-type" data-sig-appear>
        <header>
          <span class="sig-type-index">${String.fromCharCode(65 + index)}</span>
          <h3>${esc(item.name)}</h3>
        </header>
        <dl class="sig-type-facts">
          <div><dt>${esc(meta[1]?.[0] || '')}</dt><dd>${esc(meta[1]?.[1] || '')}</dd>${bar(interiorRanges[index])}</div>
          <div><dt>${esc(meta[2]?.[0] || '')}</dt><dd>${esc(meta[2]?.[1] || '')}</dd>${bar(totalRanges[index])}</div>
          <div><dt>${esc(meta[0]?.[0] || '')}</dt><dd>${esc(meta[0]?.[1] || '')}</dd></div>
          <div><dt>${esc(s.residences?.pool || '')}</dt><dd>${esc(s.residences?.poolYes || '')}</dd></div>
        </dl>
      </article>`;
  }).join('\n      ');

  const onSale = Number(en.sales?.onSale) || 0;
  const sold = Number(en.sales?.sold) || 0;
  const dots = Array.from({ length: onSale }, (_, index) => `<i class="${index < sold ? 'is-sold' : ''}"></i>`).join('');

  const statItems = (s.masterplan?.stats || []).map(([value, label]) => `<div class="sig-stat"><strong data-sig-count>${esc(value)}</strong><span>${esc(label)}</span></div>`).join('');
  const amenityItems = (s.masterplan?.amenities || []).map((item) => `<li>${esc(item)}</li>`).join('');
  const salesRows = (s.sales?.rows || []).map(([label, value]) => `<div><dt>${esc(label)}</dt><dd>${esc(value)}</dd></div>`).join('');
  const materials = (s.interiors?.materials || []).map((label, index) => `<li data-material="${index}"><i aria-hidden="true"></i><span>${esc(label)}</span></li>`).join('');
  const wellnessItems = (s.wellness?.items || []).map(([title, body]) => `<article data-sig-appear><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`).join('');
  const teamCards = (s.team?.cards || []).map(([role, name, detail]) => `<article data-sig-appear><span>${esc(role)}</span><h3>${esc(name)}</h3><p>${esc(detail)}</p></article>`).join('');
  const distanceItems = (project.location?.distances || []).map(([label, value]) => `<li><span>${esc(label)}</span><strong>${esc(value)}</strong></li>`).join('');
  const paragraphs = (list = []) => list.map((text) => `<p>${esc(text)}</p>`).join('');

  const video = project.media?.video;
  const filmBlock = video?.desktopSrc ? `<figure class="sig-film" data-project-video-shell>
        <div class="sig-film-frame">
          <video playsinline muted loop preload="none" poster="${esc(video.poster || '')}" data-project-video
            data-video-desktop="${esc(video.desktopSrc)}" data-video-mobile="${esc(video.mobileSrc || video.desktopSrc)}"
            data-poster-desktop="${esc(video.poster || '')}" data-poster-mobile="${esc(video.mobilePoster || video.poster || '')}"
            aria-label="${esc(video.alt || project.name)}"></video>
          <button type="button" class="sig-film-play" data-project-video-play aria-label="${esc(t('media.playFilm', locale))}: ${esc(video.title || '')}">
            <span aria-hidden="true"></span><em>${esc(t('media.playFilm', locale))}</em>
          </button>
        </div>
        <figcaption><strong>${esc(video.title || '')}</strong><span>${esc(video.caption || '')}</span></figcaption>
      </figure>` : '';

  return `
    <section class="sig-hero" id="top">
      <div class="sig-hero-media">${pictureTag(heroImage, 'sig-hero-img', '', { priority: true, sizes: '100vw' })}</div>
      <div class="sig-hero-shade" aria-hidden="true"></div>
      <div class="sig-wrap sig-hero-inner">
        <p class="sig-eyebrow">${esc(project.hero.eyebrow)} <span aria-hidden="true">·</span> ${esc(project.hero.location)}</p>
        <h1 class="sig-title"><span class="sig-vh">Armani </span>${armaniMark}<span class="sig-title-sub">Residences Marbella</span></h1>
        <p class="sig-lead">${esc(s.lead || project.description)}</p>
        <div class="sig-hero-actions">
          ${actionLink(project.enquiry.headlineHtml.replace(/<[^>]+>/g, ''), '#enquire')}
          ${video?.desktopSrc ? ghostAction(t('media.playFilm', locale), '#film') : ghostAction(t('cta.requestProjectMaterial', locale), '#enquire')}
        </div>
      </div>
      <ul class="sig-hero-facts sig-wrap" aria-label="${esc(t('aria.projectKeyFacts', locale))}">
        ${facts.map(([value, label]) => `<li><strong>${esc(value)}</strong><span>${esc(label)}</span></li>`).join('\n        ')}
      </ul>
    </section>

    <nav class="sig-chapters" aria-label="${esc(t('aria.projectSections', locale))}" data-sig-chapters>
      <div class="sig-wrap sig-chapters-inner">
        <a class="sig-brand" href="#top" aria-label="${esc(project.name)}">${armaniMark}<small>Residences Marbella</small></a>
        <div class="sig-chapter-links">
        ${chapters.map(([id, label], index) => `<a href="#${id}" data-chapter="${id}"><i>${String(index + 1).padStart(2, '0')}</i>${esc(label)}</a>`).join('\n        ')}
        </div>
        ${actionLink(project.enquiry.headlineHtml.replace(/<[^>]+>/g, ''), '#enquire', 'sig-bar-cta')}
      </div>
    </nav>

    <section class="sig-section sig-concept" id="concept" data-no="01">
      <div class="sig-wrap sig-split">
        <div class="sig-concept-copy" data-sig-appear>
          <span class="sig-kicker">${esc(s.concept?.kicker || '')}</span>
          <blockquote class="sig-quote"><p>${esc(s.concept?.quote || '')}</p><footer>${esc(s.concept?.attribution || '')}</footer></blockquote>
          <div class="sig-prose">${paragraphs(s.concept?.paragraphs)}</div>
        </div>
        <figure class="sig-concept-figure" data-sig-appear>${figure('interior-study-with-folding-screen', '', '(max-width: 900px) 100vw, 40vw')}</figure>
      </div>
    </section>

    ${filmBlock ? `<section class="sig-section sig-film-section" id="film">
      <div class="sig-wrap">
        <div class="sig-head" data-sig-appear>
          <span class="sig-kicker">${esc(s.film?.kicker || '')}</span>
          <h2>${s.film?.headlineHtml || ''}</h2>
          <p>${esc(s.film?.copy || '')}</p>
        </div>
        ${filmBlock}
      </div>
    </section>` : ''}

    <section class="sig-section sig-masterplan" id="masterplan" data-no="02">
      <div class="sig-masterplan-media" data-sig-parallax>${figure('masterplan-aerial-nine-buildings', '', '100vw')}</div>
      <div class="sig-masterplan-shade" aria-hidden="true"></div>
      <div class="sig-wrap sig-masterplan-inner">
        <div class="sig-head" data-sig-appear>
          <span class="sig-kicker">${esc(s.masterplan?.kicker || '')}</span>
          <h2>${s.masterplan?.headlineHtml || ''}</h2>
          <p>${esc(s.masterplan?.copy || '')}</p>
        </div>
        <div class="sig-stats" data-sig-appear>${statItems}</div>
        <div class="sig-chips" data-sig-appear>
          <span>${esc(s.masterplan?.amenitiesLabel || '')}</span>
          <ul>${amenityItems}</ul>
        </div>
      </div>
    </section>

    <section class="sig-section sig-residences" id="residences" data-no="03">
      <div class="sig-wrap">
        <div class="sig-head" data-sig-appear>
          <span class="sig-kicker">${esc(s.residences?.kicker || '')}</span>
          <h2>${project.residences.headlineHtml}</h2>
          <p>${esc(project.residences.copy)}</p>
        </div>
        <div class="sig-types">
      ${typeCards}
        </div>
        <p class="sig-note" data-sig-appear>${esc(s.residences?.note || '')}</p>
      </div>
    </section>

    <section class="sig-section sig-sales" id="sales">
      <div class="sig-wrap sig-split sig-sales-grid">
        <div data-sig-appear>
          <span class="sig-kicker">${esc(s.sales?.kicker || '')}</span>
          <h2>${s.sales?.headlineHtml || ''}</h2>
          <p class="sig-sales-copy">${esc(project.availability.copy)}</p>
          <div class="sig-dots" role="img" aria-label="${esc(`${sold} / ${onSale}`)}">${dots}</div>
        </div>
        <div data-sig-appear>
          <dl class="sig-sales-rows">${salesRows}</dl>
          <p class="sig-note">${esc(s.sales?.note || '')}</p>
          <div class="sig-sales-actions">${actionLink(t('cta.requestProjectMaterial', locale), '#enquire')}${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</div>
        </div>
      </div>
    </section>

    <section class="sig-section sig-interiors" id="interiors" data-no="04">
      <div class="sig-wrap">
        <div class="sig-split sig-interiors-head">
          <div class="sig-head" data-sig-appear>
            <span class="sig-kicker">${esc(s.interiors?.kicker || '')}</span>
            <h2>${s.interiors?.headlineHtml || ''}</h2>
            <div class="sig-prose">${paragraphs(s.interiors?.copy)}</div>
            <ul class="sig-materials" aria-hidden="false">${materials}</ul>
          </div>
          <figure class="sig-interiors-lead" data-sig-appear>${figure('interior-bedroom-with-sea-view', '', '(max-width: 900px) 100vw, 55vw')}</figure>
        </div>
        <div class="sig-interiors-grid">
          <figure data-sig-appear>${figure('interior-bedroom-and-dressing-area', '', '(max-width: 900px) 100vw, 45vw')}</figure>
          <figure data-sig-appear>${figure('interior-bathroom-with-freestanding-bath', '', '(max-width: 900px) 50vw, 28vw')}</figure>
          <figure data-sig-appear>${figure('interior-study-with-folding-screen', '', '(max-width: 900px) 50vw, 28vw')}</figure>
        </div>
        <p class="sig-pull" data-sig-appear>${esc(s.interiors?.quote || '')}</p>
      </div>
    </section>

    <section class="sig-section sig-wellness" id="wellness" data-no="05">
      <div class="sig-wellness-hero">
        <div class="sig-wellness-media" data-sig-parallax>${figure('wellness-hydrothermal-pool', '', '100vw')}</div>
        <div class="sig-wellness-shade" aria-hidden="true"></div>
        <div class="sig-wrap sig-wellness-copy" data-sig-appear>
          <span class="sig-kicker">${esc(s.wellness?.kicker || '')}</span>
          <h2>${s.wellness?.headlineHtml || ''}</h2>
          <p>${esc(s.wellness?.copy || '')}</p>
          <strong class="sig-spa-figure">${esc(s.wellness?.spaTitle || '')}</strong>
        </div>
      </div>
      <div class="sig-wrap">
        <div class="sig-wellness-grid">${wellnessItems}</div>
        <div class="sig-strip" data-sig-strip>
          ${['wellness-spa-reception', 'wellness-spa-lounge', 'wellness-treatment-room', 'wellness-relaxation-room', 'wellness-fitness-studio'].map((name) => `<figure>${figure(name, '', '(max-width: 900px) 70vw, 30vw')}</figure>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="sig-section sig-team" id="team">
      <div class="sig-wrap">
        <div class="sig-head" data-sig-appear>
          <span class="sig-kicker">${esc(s.team?.kicker || '')}</span>
          <h2>${s.team?.headlineHtml || ''}</h2>
          <p>${esc(s.team?.copy || '')}</p>
        </div>
        <div class="sig-team-grid">${teamCards}</div>
      </div>
    </section>

    <section class="sig-section sig-setting" id="setting" data-no="06">
      <div class="sig-wrap">
        <div class="sig-split sig-setting-head">
          <div class="sig-head" data-sig-appear>
            <span class="sig-kicker">${esc(s.location?.kicker || '')}</span>
            <h2>${project.location.headlineHtml}</h2>
            <p>${esc(project.location.copy)}</p>
          </div>
          <ul class="sig-distances" data-sig-appear>${distanceItems}</ul>
        </div>
        <p class="sig-note" data-sig-appear>${esc(s.location?.note || '')}</p>
        <div class="sig-map" data-sig-appear>${liveLocationMap ? renderLocationCard(project, locale) : ''}</div>
        <figure class="sig-setting-aerial" data-sig-appear>${figure('sierra-blanca-and-coast-aerial', '', '100vw')}</figure>
      </div>
    </section>

    ${projectMedia.section ? `<div class="sig-gallery">${projectMedia.section}</div>` : ''}

    <section class="sig-section sig-faq" id="faq">
      <div class="sig-wrap sig-faq-wrap">
        <div class="sig-head" data-sig-appear>
          <span class="sig-kicker">${esc(t('section.faq', locale))}</span>
          <h2>${t('faq.headlineHtml', locale)}</h2>
        </div>
        <div class="faq-list sig-faq-list">
          ${faqs.map(([question, answer], index) => `<details class="faq-item"${index === 0 ? ' open' : ''}>
            <summary>${esc(question)}<span class="faq-toggle-icon" aria-hidden="true"></span></summary>
            <p>${esc(answer)}</p>
          </details>`).join('\n          ')}
        </div>
      </div>
    </section>

    <section class="sig-section sig-enquire" id="enquire" data-no="07">
      <div class="sig-wrap sig-enquire-wrap">
        <div class="sig-head sig-enquire-head" data-sig-appear>
          <span class="sig-kicker">${esc(t('section.enquireLabel', locale))}</span>
          <h2>${project.enquiry.headlineHtml}</h2>
          <p>${esc(project.enquiry.copy)}</p>
          <p class="sig-enquire-private">${ghostAction(t('cta.speakWithAdvisor', locale), whatsappHref(project))}</p>
        </div>
        <div class="sig-enquire-form">${renderEnquiryForm(project, locale)}</div>
      </div>
    </section>

    <section class="sig-fine">
      <div class="sig-wrap">
        <p>${esc(s.disclaimer?.renders || '')}</p>
        <p>${esc(s.disclaimer?.independence || '')}</p>
      </div>
    </section>
`;
}
