// Property page template (v2): the homes-and-prices panel, the gallery, the project bar and the
// quiet motion layer. The page's data and its words come from window.NUEVA_V2, written by
// scripts/lib/property_v2.mjs in the page's own language; prices are spelled the way that
// language spells them. Forms are left to liora-conversion.js, the menu to liora-property.js.
// Everything runs inside init() on the first frame, so nothing reads layout before the first paint.
(function () {
  function init() {
  var D = window.NUEVA_V2;
  if (!D) return;
  var $ = function (id) { return document.getElementById(id); };
  var P = D.price || { pre: '€', sep: ',', post: '' };
  var L = D.i18n || {};
  var eur = function (n) { return P.pre + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, P.sep) + P.post; };
  var parse = function (t) { var n = parseInt(String(t).replace(/[^\d]/g, ''), 10); return isNaN(n) ? null : n; };
  var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  document.documentElement.classList.add('js-motion');

  // phones show three lines of the introduction with "Read more"; the button goes when the text fits
  var ovText = $('v2-ov-text'), ovMore = document.querySelector('.v2 .ov-more');
  if (ovText && ovMore) {
    var ovFit = function () { if (!ovText.classList.contains('is-open')) ovText.classList.toggle('fits', ovText.scrollHeight <= ovText.clientHeight + 2); };
    ovFit();
    addEventListener('resize', ovFit);
    addEventListener('load', ovFit);
    ovMore.addEventListener('click', function () { ovText.classList.add('is-open'); ovMore.setAttribute('aria-expanded', 'true'); });
  }

  function countTo(el, to) {
    if (!el) return;
    var from = parse(el.textContent);
    if (still || from == null || to == null || from === to) { if (to != null) el.textContent = eur(to); return; }
    var t0 = performance.now(), dur = 420;
    (function step(t) { var k = Math.min(1, (t - t0) / dur); k = 1 - Math.pow(1 - k, 3); el.textContent = eur(from + (to - from) * k); if (k < 1) requestAnimationFrame(step); })(t0);
  }

  // hero: the name arrives word by word on wide screens; phones paint it at once
  var h1 = document.querySelector('.v2 .hero-title h1');
  if (h1 && !still && innerWidth > 760) { var wi = 0; h1.querySelectorAll('span').forEach(function (sp) { sp.innerHTML = sp.textContent.split(' ').map(function (w) { return '<span class="w" style="--i:' + (wi++) + '">' + w + '</span>'; }).join(' '); }); }
  var hi = document.querySelector('.v2 .hero-img'); if (hi) hi.style.setProperty('--focus', hi.style.objectPosition || '50% 50%');
  document.querySelectorAll('.v2 .scarcity i.on').forEach(function (d, k) { d.style.setProperty('--d', k); });

  // headings and cards below the fold reveal once; prices and tables never move
  if ('IntersectionObserver' in window && !still) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('rv-in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.v2 .sec > h2, .v2 .sec > .sec-sub, .v2 .view3-col, .v2 .steps li, .v2 .docs, .v2 .mosaic, .v2 .amen-top, .v2 .faq details, .v2 .kfacts > div, .v2 .fold, .v2 .res-type, .v2 .ov-text').forEach(function (el) {
      if (el.getBoundingClientRect().top > innerHeight) {
        // siblings that arrive together follow one another by 60 ms, at most five steps
        var k = el.parentNode ? Array.prototype.indexOf.call(el.parentNode.children, el) : 0;
        if (el.matches('.kfacts > div, .steps li, .res-type, .view3-col')) el.style.setProperty('--rv-d', Math.min(k, 5) * 60 + 'ms');
        el.classList.add('rv'); io.observe(el);
      }
    });
  }
  document.querySelectorAll('.v2 .mosaic img, .v2 .swipe img').forEach(function (im) {
    if (im.complete && im.naturalWidth) im.classList.add('ld');
    else { im.addEventListener('load', function () { im.classList.add('ld'); }, { once: true }); im.addEventListener('error', function () { im.classList.add('ld'); }, { once: true }); }
  });

  // homes and prices
  var table = $('units');
  var current = null;
  var ab = document.querySelector('#v2-actionbar .ab-primary'), abDefault = ab ? ab.innerHTML : '';
  function abUpdate() {
    if (!ab) return;
    var av = $('availability'), r = av && av.getBoundingClientRect();
    var inPrices = r && r.top < innerHeight * 0.6 && r.bottom > innerHeight * 0.4;
    var html = inPrices && current && current.price ? (L.askAbout || '').replace('{ref}', current.ref) + '<small>' + eur(current.price) + ' · ' + (L.plusVat || '') + '</small>' : abDefault;
    if (html === ab.innerHTML) return;
    ab.innerHTML = html;
    if (!still && ab.animate) ab.animate([{ opacity: .35, transform: 'translateY(8px) scale(.97)' }, { opacity: 1, transform: 'none' }], { duration: 300, easing: 'cubic-bezier(.22,.61,.36,1)' });
  }
  addEventListener('scroll', abUpdate, { passive: true });
  var byId = {}; (D.units || []).forEach(function (u) { byId[u.id] = u; });
  function stageRow(label, when, amountLabel, value) {
    return '<tr><th scope="row">' + label + (when ? '<small>' + when + '</small>' : '') + '</th><td class="pct">' + (amountLabel || '') + '</td><td>' + value + '</td></tr>';
  }
  var esc = function (s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };
  function select(id, flash) {
    var u = byId[id]; if (!u || !table) return;
    table.tBodies[0].querySelectorAll('tr').forEach(function (tr) { tr.setAttribute('aria-selected', tr.dataset.id === id ? 'true' : 'false'); });
    $('v2-p-title').textContent = u.title;
    $('v2-p-sub').textContent = u.sub;
    if (flash && !still) [$('v2-p-title'), $('v2-p-sub'), $('v2-c-plans')].forEach(function (el, k) {
      if (el && el.animate) el.animate([{ opacity: 0, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }], { duration: 320, delay: k * 50, easing: 'cubic-bezier(.22,.61,.36,1)', fill: 'backwards' });
    });
    var sched = $('v2-p-sched');
    if (sched) {
      var prev = Array.prototype.map.call(sched.querySelectorAll('td:last-child'), function (td) { return td.textContent; });
      var rows = '';
      if (D.stages && u.price) {
        var run = 0;
        D.stages.forEach(function (s) {
          var amt = s.fixed != null ? s.fixed : s.balance ? u.price - run : u.price * s.pct - (s.less || 0);
          run += amt;
          rows += stageRow(esc(s.label), esc(s.when), s.fixed != null ? '' : esc(s.amountLabel), eur(amt));
        });
        rows += stageRow('<b>' + esc(L.totalPrice) + '</b>', esc(L.vatOnStages), '100%', '<b>' + eur(run) + '</b>');
      } else {
        (D.stageLabels || D.stages || []).forEach(function (s) { rows += stageRow(esc(s.label), esc(s.when), esc(s.amountLabel), ''); });
      }
      sched.innerHTML = rows;
      if (!still && flash) sched.querySelectorAll('td:last-child').forEach(function (td, k) { var el = td.querySelector('b') || td; var to = parse(el.textContent); if (to != null && parse(prev[k]) != null) { el.textContent = prev[k]; countTo(el, to); } });
    }
    var has = u.price != null;
    var setv = function (elId, v) { var el = $(elId); if (!el) return; if (has && flash) countTo(el, v); else el.textContent = has ? eur(v) : (elId === 'v2-c-price' ? L.onRequest : '–'); };
    setv('v2-c-price', u.price); setv('v2-c-vat', u.price * D.vat); setv('v2-c-ajd', u.price * D.ajd); setv('v2-c-total', u.price * (1 + D.vat + D.ajd));
    current = u;
    abUpdate();
    var enq = $('v2-c-enquire'); if (enq) { enq.textContent = (L.askAbout || '').replace('{ref}', u.ref); enq.dataset.unit = u.ref; }
    // one link per level: a townhouse's living and bedroom levels are two plans
    var pl = $('v2-c-plans');
    if (pl) pl.innerHTML = (u.plans || []).map(function (p) { return '<a class="btn btn-ghost" href="' + esc(p.src) + '" target="_blank" rel="noopener">' + esc(L.floorPlan || '') + (p.label ? ' · ' + esc(p.label) : '') + '</a>'; }).join('');
  }
  // "Ask about 40C" picks the home in the enquiry form
  function nameHome() {
    if (!current) return;
    var sel = $('v2-f-unit'); if (sel) { sel.value = current.ref; compose(); }
  }
  // the CRM reads one message field: the chosen home, the purpose, the reply channel and the alert
  // request are written into it, in English, as the rest of the lead record is
  var form = $('projectForm'), msgField = $('v2-f-message');
  function compose() {
    if (!form || !msgField) return;
    var parts = [msgField.getAttribute('data-base') || ''];
    var sel = $('v2-f-unit'); if (sel && sel.value) parts.push('Home: ' + sel.value + '.');
    var use = form.querySelector('[name="purchase_purpose"]:checked'); if (use) parts.push('Purpose: ' + use.value + '.');
    var how = form.querySelector('[name="preferred_contact"]:checked'); if (how) parts.push('Reply by: ' + how.value + '.');
    var al = $('v2-f-alert'); if (al && al.checked) parts.push('Also alert me if availability or prices change.');
    msgField.value = parts.filter(Boolean).join(' ');
  }
  if (form) { form.addEventListener('change', compose); form.addEventListener('submit', compose, true); compose(); }
  var enqBtn = $('v2-c-enquire'); if (enqBtn) enqBtn.addEventListener('click', nameHome);
  if (ab) ab.addEventListener('click', function () { var av = $('availability'), r = av && av.getBoundingClientRect(); if (r && r.top < innerHeight * 0.6 && r.bottom > innerHeight * 0.4) nameHome(); });

  if (table) {
    var tbody = table.tBodies[0];
    tbody.addEventListener('click', function (e) { if (e.target.closest('a')) return; var tr = e.target.closest('tr'); if (tr) select(tr.dataset.id, true); });
    tbody.addEventListener('keydown', function (e) { if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('tr')) { e.preventDefault(); select(e.target.dataset.id, true); } });
    table.tHead.addEventListener('click', function (e) {
      var th = e.target.closest('th[data-sort]'); if (!th) return;
      var key = th.dataset.sort, dir = th.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
      table.tHead.querySelectorAll('th').forEach(function (x) { x.removeAttribute('aria-sort'); }); th.setAttribute('aria-sort', dir);
      var rows = Array.prototype.slice.call(tbody.rows);
      var before = new Map(); rows.forEach(function (r) { before.set(r, r.getBoundingClientRect().top); });
      rows.sort(function (a, b) {
        if (key === 'ref') { var c = a.cells[0].textContent.localeCompare(b.cells[0].textContent, undefined, { numeric: true }); return dir === 'ascending' ? c : -c; }
        var x = parseFloat(a.dataset[key]), y = parseFloat(b.dataset[key]);
        if (isNaN(x)) return 1; if (isNaN(y)) return -1; return dir === 'ascending' ? x - y : y - x;
      });
      rows.forEach(function (r) { tbody.appendChild(r); });
      if (!still && rows[0] && rows[0].animate) rows.forEach(function (r) {
        var dy = before.get(r) - r.getBoundingClientRect().top; if (!dy) return;
        r.animate([{ transform: 'translateY(' + dy + 'px)' }, { transform: 'none' }], { duration: 320, easing: 'cubic-bezier(.22,.61,.36,1)' });
      });
    });
    // phones list the first eight homes of the current filter and sort; "Show all" opens the rest
    var showAll = document.querySelector('.v2 .u-showall'), allOpen = false;
    var clip = function () {
      if (!showAll) return;
      var n = 0;
      Array.prototype.forEach.call(tbody.rows, function (r) {
        var out = r.classList.contains('is-out');
        if (!out) n++;
        r.classList.toggle('u-more', !allOpen && !out && n > 8 && r.getAttribute('aria-selected') !== 'true');
      });
      showAll.textContent = String(L.showAll || '').replace('{n}', n);
      showAll.classList.toggle('is-gone', allOpen || n <= 8);
    };
    if (showAll) showAll.addEventListener('click', function () { allOpen = true; clip(); });
    clip();
    table.tHead.addEventListener('click', clip);
    var uf = document.querySelector('.v2 .ufilter');
    if (uf) uf.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      uf.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      var want = b.dataset.beds;
      var back = 0;
      Array.prototype.forEach.call(tbody.rows, function (r) {
        var was = r.classList.contains('is-out'), out = want !== '' && r.dataset.beds !== want;
        r.classList.toggle('is-out', out);
        if (!out && !still && r.animate && back < 10) r.animate([{ opacity: 0, transform: 'translateY(6px)' }, { opacity: 1, transform: 'none' }], { duration: 280, delay: (back++) * 35, easing: 'cubic-bezier(.22,.61,.36,1)', fill: 'backwards' });
      });
      var cnt = b.querySelector('span'); if (cnt && !still && cnt.animate) cnt.animate([{ transform: 'scale(1.35)' }, { transform: 'none' }], { duration: 260, easing: 'cubic-bezier(.22,.61,.36,1)' });
      var sel = tbody.querySelector('tr[aria-selected="true"]');
      if (sel && sel.classList.contains('is-out')) { var vis = tbody.querySelector('tr:not(.is-out)'); if (vis) select(vis.dataset.id, true); }
      clip();
    });
    if (fine) {
      var tip = document.createElement('div'); tip.className = 'uthumb'; tip.setAttribute('aria-hidden', 'true'); tip.innerHTML = '<img alt="">';
      document.querySelector('.v2').appendChild(tip);
      var timg = tip.firstChild;
      tbody.addEventListener('mouseover', function (e) { var tr = e.target.closest('tr[data-thumb]'); if (!tr) { tip.classList.remove('on'); return; } if (timg.getAttribute('src') !== tr.dataset.thumb) timg.src = tr.dataset.thumb; tip.classList.add('on'); });
      tbody.addEventListener('mousemove', function (e) { tip.style.left = Math.min(e.clientX + 24, innerWidth - 260) + 'px'; tip.style.top = Math.min(e.clientY - 40, innerHeight - 200) + 'px'; });
      tbody.addEventListener('mouseleave', function () { tip.classList.remove('on'); });
    }
    var first = (D.units || []).filter(function (u) { return u.price != null; }).sort(function (a, b) { return a.price - b.price; })[0] || (D.units || [])[0];
    if (first) select(first.id, false);
  }

  // our view: one column at a time on phones
  var v3 = document.querySelector('.v2 [data-view3]');
  if (v3) {
    v3.setAttribute('data-js', '');
    var cols = v3.querySelectorAll('.view3-col'); if (cols[0]) cols[0].classList.add('is-on');
    v3.querySelector('.view3-tabs').addEventListener('click', function (e) {
      var b = e.target.closest('button[data-v]'); if (!b) return;
      v3.querySelectorAll('.view3-tabs button').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
      cols.forEach(function (c) { c.classList.toggle('is-on', c.id === b.dataset.v); });
    });
  }

  // tabs (specifications, layouts)
  document.querySelectorAll('.v2 .tabs').forEach(function (bar) {
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-tab]'); if (!b) return;
      bar.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); var p = $(x.dataset.tab); if (p) p.hidden = x !== b; });
    });
  });

  // the project bar docks under the site's top bar (CSS reads --nueva-header-h)
  var sn = document.querySelector('.site-nav');
  var hdr = $('v2bar'), hero = $('top'), bar = $('v2-actionbar'), contact = $('enquire'), lastY = scrollY;
  // translated pages carry <base href="../">, so their section links are written out in full
  // ("de/property-x.html#overview"); a link is in-page when it points at this very document
  function inPage(a) {
    if (!a || !a.hash || a.hash.length < 2 || a.pathname !== location.pathname) return null;
    try { return document.getElementById(decodeURIComponent(a.hash.slice(1))); } catch (err) { return null; }
  }
  function onScroll() {
    var y = scrollY;
    if (hdr && hero) hdr.classList.toggle('is-project', y > hero.offsetTop + hero.offsetHeight - 80);
    if (hdr) { if (innerWidth <= 760) hdr.classList.toggle('is-hidden', y > lastY && y > 120); else hdr.classList.remove('is-hidden'); }
    if (bar && contact) { var cr = contact.getBoundingClientRect(); bar.classList.toggle('is-hidden', cr.top < innerHeight * 0.7 && cr.bottom > 0); }
    if (bar && Math.abs(y - lastY) > 4) bar.classList.toggle('is-compact', y > lastY && y > 400);
    if (hdr) {
      var links = hdr.querySelectorAll('.hdr-proj a'), cur = null, off = (sn ? sn.getBoundingClientRect().height : 64) + 90;
      links.forEach(function (a) { var s = inPage(a); if (s && s.getBoundingClientRect().top < off) cur = a; });
      links.forEach(function (a) { a.classList.toggle('is-active', a === cur); });
    }
    lastY = y;
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.v2 a[href*="#"]'); var t = inPage(a); if (!t) return;
    e.preventDefault();
    scrollTo({ top: t.getBoundingClientRect().top + scrollY - ((sn ? sn.getBoundingClientRect().height : 64) + 64), behavior: still ? 'auto' : 'smooth' });
  });

  // gallery lightbox
  var rtl = document.documentElement.dir === 'rtl' ? -1 : 1;
  var G = D.gallery || [], lb = $('v2-lb'), img = $('v2-lb-img'), idx = 0, lastFocus = null;
  if (!lb || !img) return;
  function show(i) {
    if (!G.length) return; idx = (i + G.length) % G.length; var g = G[idx];
    if (!still && !lb.hidden && img.src) { img.classList.add('swap'); var nx = new Image(); nx.onload = function () { img.src = g.src; img.classList.remove('swap'); }; nx.src = g.src; } else img.src = g.src;
    img.alt = g.alt;
    [idx + 1, idx - 1].forEach(function (j) { var p = G[(j + G.length) % G.length]; if (p) (new Image()).src = p.src; });
    $('v2-lb-cap').textContent = g.caption;
    $('v2-lb-count').textContent = (L.imageOf || '{i} / {n}').replace('{i}', idx + 1).replace('{n}', G.length);
    lb.querySelectorAll('.lb-cats button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.cat === g.cat ? 'true' : 'false'); });
  }
  function zoomFrom(from) {
    var src = from && (from.querySelector('img') || (from.tagName === 'IMG' ? from : null));
    if (still || !src || !img.animate) return;
    var r0 = src.getBoundingClientRect();
    var go = function () {
      var r1 = img.getBoundingClientRect(); if (!r1.width || !r0.width) return;
      var k = r0.width / r1.width, dx = (r0.left + r0.width / 2) - (r1.left + r1.width / 2), dy = (r0.top + r0.height / 2) - (r1.top + r1.height / 2);
      img.animate([{ transform: 'translate(' + dx + 'px,' + dy + 'px) scale(' + k + ')', opacity: .5 }, { transform: 'none', opacity: 1 }], { duration: 380, easing: 'cubic-bezier(.22,.61,.36,1)' });
    };
    if (img.complete && img.naturalWidth) go(); else img.addEventListener('load', go, { once: true });
  }
  function open(i, from) { lastFocus = document.activeElement; lb.hidden = false; document.body.classList.add('v2-lb-open'); show(i); zoomFrom(from); lb.querySelector('.lb-close').focus(); document.body.style.overflow = 'hidden'; }
  function close() { lb.hidden = true; document.body.classList.remove('v2-lb-open'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }
  function firstOf(cat) { for (var i = 0; i < G.length; i++) if (G[i].cat === cat) return i; return 0; }
  document.addEventListener('click', function (e) {
    var o = e.target.closest('.v2 [data-open-gallery]'); if (o) { open(parseInt(o.getAttribute('data-open-gallery'), 10) || 0, o); return; }
    var c = e.target.closest('.v2 [data-open-cat]'); if (c) open(firstOf(c.getAttribute('data-open-cat')), c);
  });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
  lb.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
  lb.querySelector('.lb-cats').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) show(firstOf(b.dataset.cat)); });
  document.addEventListener('keydown', function (e) { if (lb.hidden) return; if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') show(idx + rtl); else if (e.key === 'ArrowLeft') show(idx - rtl); else if (e.key === 'Tab') { var f = [].slice.call(lb.querySelectorAll('button:not([hidden])')).filter(function (b) { return b.offsetParent; }); if (!f.length) return; var first = f[0], last = f[f.length - 1]; if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); } } });
  var tx = null;
  lb.addEventListener('touchstart', function (e) { tx = e.touches.length === 1 ? e.touches[0].clientX : null; if (tx !== null && !still) img.classList.add('drag'); }, { passive: true });
  lb.addEventListener('touchmove', function (e) {
    if (tx === null || still || e.touches.length !== 1) return;
    var dx = e.touches[0].clientX - tx;
    img.style.transform = 'translateX(' + dx + 'px)'; img.style.opacity = String(1 - Math.min(0.5, Math.abs(dx) / 700));
  }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (tx === null) return;
    var dx = e.changedTouches[0].clientX - tx; tx = null;
    img.classList.remove('drag'); img.style.transform = ''; img.style.opacity = '';
    if (Math.abs(dx) > 40) show(idx + (dx < 0 ? rtl : -rtl));
  });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { requestAnimationFrame(init); });
  else requestAnimationFrame(init);
})();
