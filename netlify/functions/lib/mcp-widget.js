// The view Claude and ChatGPT draw for the connector's results: development cards with photos,
// list prices and delivery, a map, filters that narrow the search, a detail view with the homes on
// the price list, and a form to ask an advisor.
//
// It is one self-contained HTML document, served by nueva-mcp.js as an MCP Apps resource
// (ui://nueva-living/view-<hash>.html). The host runs it in a sandboxed frame and talks to it with
// JSON-RPC over postMessage: it sends the tool result in, and the view can call the server's tools
// (a filter chip searches again, a card opens its details, the form sends an enquiry) and ask the
// host to open a link. ChatGPT also exposes `window.openai`; when it is there the view uses it.
//
// Loaded from elsewhere, all listed in the resource's CSP: Leaflet from this site's own vendored
// and protomaps-leaflet copies, photos and the base-map archive from this site, fonts from Google.
// No backticks in the script below: the document is a JavaScript string.
const I18N = require('./mcp-widget-i18n');


const STYLE = String.raw`
:root{--bg:#faf6ee;--card:#fffdf8;--ink:#2e2a24;--body:#5f574e;--muted:#7a7066;--rule:#e2d8c6;--gold:#896a3f;--gold-soft:#c7a36b;--chip:#f1e9da;--btn:#2f2417;--btn-ink:#faf6ee;--shadow:0 1px 2px rgba(47,36,23,.06),0 8px 24px rgba(47,36,23,.06)}
:root[data-theme=dark]{--bg:#1d1913;--card:#26211a;--ink:#f3ece0;--body:#d6ccbd;--muted:#a99d8c;--rule:#3b3328;--gold:#d6b27a;--gold-soft:#b8935c;--chip:#2f2920;--btn:#e8d5b0;--btn-ink:#1d1913;--shadow:none}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Montserrat,"Helvetica Neue",Arial,sans-serif}
body{padding:14px}
button,input,textarea{font:inherit;color:inherit}
.eyebrow{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);font-weight:600}
h1,h2,h3{font-family:"Cormorant Garamond",Georgia,serif;font-weight:600;margin:0;color:var(--ink);text-wrap:balance}
h1{font-size:24px;line-height:1.15}h2{font-size:21px;line-height:1.2}h3{font-size:19px;line-height:1.2}
.head{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.count{color:var(--muted);font-size:12.5px}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:999px;overflow:hidden}
.seg button{border:0;background:transparent;padding:6px 14px;font-size:12.5px;cursor:pointer;color:var(--body)}
.seg button[aria-pressed=true]{background:var(--btn);color:var(--btn-ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--rule);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:var(--shadow);min-width:0}
.ph{position:relative;aspect-ratio:16/10;background:var(--chip);overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover;display:block}
.badge{position:absolute;left:10px;top:10px;background:rgba(250,246,238,.92);color:#2f2417;font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;padding:4px 9px;border-radius:999px}
.cb{padding:12px 14px 14px;display:flex;flex-direction:column;gap:6px;flex:1}
.loc{color:var(--muted);font-size:12.5px}
.price{font-weight:600;font-size:15px}
.meta{display:flex;flex-wrap:wrap;gap:4px 12px;color:var(--body);font-size:12.5px}
.fit{color:var(--gold);font-size:12.5px;font-weight:600}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{background:var(--chip);color:var(--body);border-radius:999px;padding:3px 10px;font-size:11.5px;border:0}
button.chip{cursor:pointer;padding:6px 12px;font-size:12.5px;border:1px solid var(--rule)}
button.chip:hover{border-color:var(--gold-soft)}
.actions{display:flex;gap:8px;margin-top:auto;padding-top:8px;flex-wrap:wrap}
.btn{border:1px solid var(--btn);background:var(--btn);color:var(--btn-ink);border-radius:999px;padding:7px 14px;font-size:12.5px;font-weight:600;cursor:pointer}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--rule)}
.btn:disabled{opacity:.6;cursor:default}
.narrow{margin-top:14px}.narrow .eyebrow{display:block;margin-bottom:8px}
.note{color:var(--muted);font-size:11.5px;margin-top:12px}
#map,.minimap{height:360px;border-radius:14px;border:1px solid var(--rule);overflow:hidden;background:var(--chip)}
.minimap{height:220px}
.leaflet-container{font:inherit}
.pin{width:14px;height:14px;border-radius:50%;background:var(--gold);border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.35)}
.pop b{display:block;font-family:"Cormorant Garamond",Georgia,serif;font-size:16px}
.back{background:none;border:0;color:var(--gold);cursor:pointer;padding:0 0 10px;font-weight:600;font-size:12.5px}
.gallery{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;border-radius:14px;margin-bottom:12px}
.gallery img{height:220px;width:auto;max-width:88%;flex:0 0 auto;object-fit:cover;border-radius:12px;scroll-snap-align:start;background:var(--chip)}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin:12px 0}
.fact{background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:9px 12px}
.fact span{display:block;color:var(--muted);font-size:11px;letter-spacing:.06em;text-transform:uppercase}
.fact strong{font-size:14px}
.sec{margin-top:16px}.sec>.eyebrow{display:block;margin-bottom:8px}
.p{color:var(--body);margin:6px 0}
.tbl{overflow-x:auto;border:1px solid var(--rule);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{text-align:start;padding:7px 10px;border-bottom:1px solid var(--rule);vertical-align:top}
th{color:var(--muted);font-weight:600;font-size:11px;letter-spacing:.06em;text-transform:uppercase}
tr:last-child td{border-bottom:0}
td.num{white-space:nowrap;font-weight:600}
details{border:1px solid var(--rule);border-radius:12px;padding:8px 12px;background:var(--card)}
summary{cursor:pointer;font-weight:600;font-size:13px}
.dist{display:grid;grid-template-columns:1fr auto;gap:2px 16px;font-size:12.5px;color:var(--body)}
.form{display:grid;gap:10px;max-width:520px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
label.f{display:grid;gap:4px;font-size:12px;color:var(--muted)}
input[type=text],input[type=email],input[type=tel],textarea{border:1px solid var(--rule);background:var(--card);border-radius:10px;padding:9px 11px;width:100%}
textarea{min-height:80px;resize:vertical}
.consent{display:flex;gap:8px;align-items:flex-start;font-size:12.5px;color:var(--body)}
.msg{font-size:13px;padding:10px 12px;border-radius:10px;background:var(--chip)}
.empty{padding:18px;border:1px dashed var(--rule);border-radius:14px;color:var(--body)}
@media (max-width:480px){body{padding:10px}.row{grid-template-columns:1fr}.gallery img{height:180px}}
`;

const SCRIPT = String.raw`
(function () {
  var I18N = window.__I18N__;
  var state = { data: null, stack: [], view: 'list', lang: 'en', query: null };
  var root = document.getElementById('app');
  var openai = window.openai || null;

  /* ---------- host bridge (MCP Apps over postMessage; window.openai when present) ---------- */
  var pending = {}, nextId = 1;
  function post(msg) { try { window.parent.postMessage(msg, '*'); } catch (e) {} }
  function request(method, params) {
    return new Promise(function (resolve, reject) {
      var id = nextId++;
      pending[id] = { resolve: resolve, reject: reject };
      post({ jsonrpc: '2.0', id: id, method: method, params: params || {} });
      setTimeout(function () { if (pending[id]) { delete pending[id]; reject(new Error('timeout')); } }, 45000);
    });
  }
  function notify(method, params) { post({ jsonrpc: '2.0', method: method, params: params || {} }); }

  window.addEventListener('message', function (event) {
    var m = event.data;
    if (!m || m.jsonrpc !== '2.0') return;
    if (m.method) {
      if (m.method === 'ui/notifications/tool-result') receive(m.params);
      else if (m.method === 'ui/notifications/tool-input') state.query = (m.params && m.params.arguments) || state.query;
      else if (m.method === 'ui/notifications/host-context-changed') applyContext(m.params);
      if (m.id !== undefined && m.id !== null) post({ jsonrpc: '2.0', id: m.id, result: {} });
      return;
    }
    if (m.id !== undefined && pending[m.id]) {
      var p = pending[m.id]; delete pending[m.id];
      if (m.error) p.reject(new Error(m.error.message || 'error')); else p.resolve(m.result);
    }
  });

  function callTool(name, args) {
    if (openai && openai.callTool) {
      return Promise.resolve(openai.callTool(name, args)).then(function (r) { return (r && (r.structuredContent || r.result)) || r; });
    }
    return request('tools/call', { name: name, arguments: args }).then(function (r) {
      if (!r) throw new Error('empty');
      return r.structuredContent || JSON.parse(((r.content || [])[0] || {}).text || '{}');
    });
  }
  function openLink(url) {
    if (openai && openai.openExternal) { try { openai.openExternal({ href: url }); return; } catch (e) {} }
    request('ui/open-link', { url: url }).catch(function () { window.open(url, '_blank', 'noopener'); });
  }
  function applyContext(ctx) {
    if (!ctx) return;
    var theme = ctx.theme || (ctx.styles && ctx.styles.theme);
    if (theme) document.documentElement.setAttribute('data-theme', theme === 'dark' ? 'dark' : 'light');
  }
  var lastHeight = 0;
  function reportSize() {
    var h = Math.ceil(document.documentElement.getBoundingClientRect().height);
    if (Math.abs(h - lastHeight) < 2) return;
    lastHeight = h;
    notify('ui/notifications/size-changed', { width: Math.ceil(document.documentElement.clientWidth), height: h });
    if (openai && openai.notifyIntrinsicHeight) { try { openai.notifyIntrinsicHeight(h); } catch (e) {} }
  }
  if (window.ResizeObserver) new ResizeObserver(reportSize).observe(document.documentElement);

  function receive(result) {
    var data = result && (result.structuredContent || (result.content && result.content[0] && safeParse(result.content[0].text)));
    if (!data) return;
    state.stack = [];
    show(data);
  }
  function safeParse(text) { try { return JSON.parse(text); } catch (e) { return null; } }

  /* ---------- helpers ---------- */
  function t(key, vars) {
    var dict = I18N[state.lang] || I18N.en;
    var s = key.split('.').reduce(function (o, k) { return o && o[k]; }, dict);
    if (s == null) s = key.split('.').reduce(function (o, k) { return o && o[k]; }, I18N.en) || '';
    if (vars) Object.keys(vars).forEach(function (k) { s = s.split('{' + k + '}').join(vars[k]); });
    return s;
  }
  function esc(v) { return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function group(n, sep) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, sep); }
  function eur(n) {
    if (n == null) return '';
    var l = state.lang;
    if (l === 'en') return '€' + group(n, ',');
    if (l === 'nl') return '€ ' + group(n, '.');
    if (l === 'es' || l === 'de') return group(n, '.') + ' €';
    if (l === 'ar') return group(n, ',') + ' €';
    return group(n, ' ') + ' €';
  }
  function beds(b) { return !b ? '' : (b === '1' ? t('bed1') : t('beds', { b: b })); }
  function el(html) { var d = document.createElement('div'); d.innerHTML = html; return d.firstElementChild; }

  /* ---------- views ---------- */
  function show(data, push) {
    if (push && state.data) state.stack.push(state.data);
    state.data = data;
    state.lang = data.language || state.lang;
    if (data.query) state.query = data.query;
    document.documentElement.lang = state.lang;
    document.documentElement.dir = state.lang === 'ar' ? 'rtl' : 'ltr';
    if (data.kind === 'development') renderDetail(data);
    else if (data.kind === 'enquiry_form') renderForm(data);
    else if (data.kind === 'request' || data.sent !== undefined) renderSent(data);
    else renderSearch(data);
    window.scrollTo(0, 0);
    setTimeout(reportSize, 30);
  }
  function back() { var prev = state.stack.pop(); if (prev) { state.data = null; show(prev); } }

  function cardHtml(r) {
    var fit = r.homesMatching ? (r.homesMatching === 1 ? t('inBudget1', { p: eur(r.fromMatchingEur) }) : t('inBudget', { n: r.homesMatching, p: eur(r.fromMatchingEur) })) : '';
    var feats = (r.features || []).slice(0, 3).map(function (f) { return '<span class="chip">' + esc(t('feature.' + f)) + '</span>'; }).join('');
    return '<article class="card" data-slug="' + esc(r.slug) + '">'
      + '<div class="ph">' + (r.image ? '<img loading="lazy" alt="" src="' + esc(r.image) + '">' : '') + (r.stage ? '<span class="badge">' + esc(t('stage.' + r.stage)) + '</span>' : '') + '</div>'
      + '<div class="cb"><span class="loc">' + esc([r.location, r.type].filter(Boolean).join(' · ')) + '</span>'
      + '<h3>' + esc(r.name) + '</h3>'
      + '<div class="price">' + esc(r.from || '') + '</div>'
      + '<div class="meta">' + (r.bedrooms ? '<span>' + esc(beds(r.bedrooms)) + '</span>' : '') + (r.delivery ? '<span>' + esc(t('delivery')) + ': ' + esc(r.delivery) + '</span>' : '') + '</div>'
      + (fit ? '<div class="fit">' + esc(fit) + '</div>' : '')
      + (feats ? '<div class="chips">' + feats + '</div>' : '')
      + '<div class="actions"><button class="btn" data-act="details">' + esc(t('details')) + '</button><button class="btn ghost" data-act="page" data-url="' + esc(r.url) + '">' + esc(t('page')) + '</button></div>'
      + '</div></article>';
  }

  function refineChips(data) {
    var q = data.query || {};
    var chips = [];
    (data.refine || []).forEach(function (r) {
      (r.options || []).slice(0, 5).forEach(function (o) {
        var label = r.narrow_by === 'budget_max' ? t('upTo', { p: eur(o) })
          : r.narrow_by === 'property_type' ? t('only', { x: t('type.' + o) })
          : r.narrow_by === 'stage' ? t('stage.' + o)
          : String(o);
        var patch = {}; patch[r.narrow_by] = o;
        chips.push({ label: label, patch: patch });
      });
    });
    // Features the results share that the search did not ask for yet.
    var have = q.features || [];
    var counts = {};
    (data.results || []).forEach(function (r) { (r.features || []).forEach(function (f) { counts[f] = (counts[f] || 0) + 1; }); });
    ['sea_view', 'beach', 'golf', 'private_pool', 'gated', 'garden'].forEach(function (f) {
      if (have.indexOf(f) < 0 && counts[f] && counts[f] < (data.results || []).length) chips.push({ label: t('feature.' + f), patch: { features: have.concat([f]) } });
    });
    return chips.slice(0, 10);
  }

  function renderSearch(data) {
    var results = data.results || [];
    var chips = data.more_matches || results.length ? refineChips(data) : [];
    root.innerHTML = '<div class="head"><div><div class="eyebrow">' + esc(t('eyebrow')) + '</div><h1>' + esc(t('best')) + '</h1>'
      + (data.total ? '<div class="count">' + esc(t('of', { n: results.length, t: data.total })) + '</div>' : '') + '</div>'
      + (results.some(function (r) { return r.map; }) ? '<div class="seg" role="group"><button data-view="list" aria-pressed="' + (state.view === 'list') + '">' + esc(t('list')) + '</button><button data-view="map" aria-pressed="' + (state.view === 'map') + '">' + esc(t('map')) + '</button></div>' : '')
      + '</div>'
      + (results.length ? (state.view === 'map' ? '<div id="map"></div>' : '<div class="grid">' + results.map(cardHtml).join('') + '</div>')
        : '<div class="empty">' + esc(data.message || t('none')) + '</div>')
      + (chips.length ? '<div class="narrow"><span class="eyebrow">' + esc(t('narrow')) + '</span><div class="chips">' + chips.map(function (c, i) { return '<button class="chip" data-chip="' + i + '">' + esc(c.label) + '</button>'; }).join('') + '</div></div>' : '')
      + '<p class="note">' + esc(t('note')) + '</p>';
    root.querySelectorAll('[data-view]').forEach(function (b) { b.onclick = function () { state.view = b.getAttribute('data-view'); renderSearch(data); setTimeout(reportSize, 30); }; });
    root.querySelectorAll('[data-chip]').forEach(function (b) {
      b.onclick = function () {
        var c = chips[Number(b.getAttribute('data-chip'))];
        var q = Object.assign({}, data.query || {}, c.patch, { language: state.lang });
        b.disabled = true; b.textContent = t('loading');
        callTool('search_developments', q).then(function (r) { show(r); }).catch(function () { b.disabled = false; b.textContent = c.label; });
      };
    });
    bindCards(root);
    if (state.view === 'map' && results.length) drawMap(document.getElementById('map'), results);
  }

  function bindCards(scope) {
    scope.querySelectorAll('.card').forEach(function (card) {
      var slug = card.getAttribute('data-slug');
      var open = function () {
        var b = card.querySelector('[data-act=details]'); if (b) { b.disabled = true; b.textContent = t('loading'); }
        callTool('get_development', { slug: slug, language: state.lang }).then(function (r) { show(r, true); })
          .catch(function () { if (b) { b.disabled = false; b.textContent = t('details'); } });
      };
      var d = card.querySelector('[data-act=details]'); if (d) d.onclick = open;
      var img = card.querySelector('.ph'); if (img) { img.style.cursor = 'pointer'; img.onclick = open; }
      var p = card.querySelector('[data-act=page]'); if (p) p.onclick = function () { openLink(p.getAttribute('data-url')); };
    });
  }

  function renderDetail(d) {
    var rows = d.homes || [];
    var limit = 8;
    var feats = (d.features || []).map(function (f) { return '<span class="chip">' + esc(t('feature.' + f)) + '</span>'; }).join('');
    function table(n) {
      return '<div class="tbl"><table><thead><tr><th>' + esc(t('ref')) + '</th><th>' + esc(t('size')) + '</th><th>' + esc(t('price')) + '</th></tr></thead><tbody>'
        + rows.slice(0, n).map(function (h) { return '<tr><td>' + esc(h.ref) + (h.bedrooms ? '<br><span class="loc">' + esc(h.bedrooms) + '</span>' : '') + '</td><td>' + esc(h.size) + '</td><td class="num">' + esc(h.price) + '</td></tr>'; }).join('')
        + '</tbody></table></div>';
    }
    root.innerHTML = (state.stack.length ? '<button class="back" data-back>‹ ' + esc(t('back')) + '</button>' : '')
      + ((d.images || []).length ? '<div class="gallery">' + d.images.map(function (im) { return '<img loading="lazy" src="' + esc(im.url) + '" alt="' + esc(im.alt) + '">'; }).join('') + '</div>' : '')
      + '<div class="eyebrow">' + esc([d.area, d.type].filter(Boolean).join(' · ')) + '</div><h1>' + esc(d.name) + '</h1>'
      + '<div class="facts">'
      + '<div class="fact"><span>' + esc(t('price')) + '</span><strong>' + esc(d.priceRange || d.from) + '</strong></div>'
      + (d.bedrooms ? '<div class="fact"><span>' + esc(t('bedsLabel')) + '</span><strong>' + esc(d.bedrooms) + '</strong></div>' : '')
      + (d.delivery ? '<div class="fact"><span>' + esc(t('delivery')) + '</span><strong>' + esc(d.delivery) + '</strong></div>' : '')
      + (d.stage ? '<div class="fact"><span>' + esc(t('stageLabel')) + '</span><strong>' + esc(t('stage.' + d.stage)) + '</strong></div>' : '')
      + '</div>'
      + '<p class="p">' + esc(d.description || d.summary) + '</p>'
      + (feats ? '<div class="sec"><span class="eyebrow">' + esc(t('features')) + '</span><div class="chips">' + feats + '</div></div>' : '')
      + (rows.length ? '<div class="sec"><span class="eyebrow">' + esc(t('homes')) + (d.checked ? ' · ' + esc(t('checked', { d: d.checked })) : '') + '</span><div data-table>' + table(limit) + '</div>'
        + (rows.length > limit ? '<div class="actions"><button class="btn ghost" data-all>' + esc(t('showAll', { n: rows.length })) + '</button></div>' : '') + '</div>' : '')
      + (d.price_note ? '<div class="sec"><details><summary>' + esc(t('priceNote')) + '</summary><p class="p">' + esc(d.price_note) + '</p></details></div>' : '')
      + ((d.distances || []).length ? '<div class="sec"><span class="eyebrow">' + esc(t('distances')) + '</span><div class="dist">' + d.distances.map(function (r) { return '<span>' + esc(r[0]) + '</span><span>' + esc(r[1]) + '</span>'; }).join('') + '</div></div>' : '')
      + (d.map ? '<div class="sec"><div class="minimap" id="minimap"></div></div>' : '')
      + '<div class="actions" style="margin-top:14px"><button class="btn" data-ask>' + esc(t('ask')) + '</button><button class="btn ghost" data-page>' + esc(t('page')) + '</button></div>'
      + '<p class="note">' + esc(d.images_note || t('note')) + '</p>';
    var b = root.querySelector('[data-back]'); if (b) b.onclick = back;
    var all = root.querySelector('[data-all]'); if (all) all.onclick = function () { root.querySelector('[data-table]').innerHTML = table(rows.length); all.parentNode.remove(); setTimeout(reportSize, 30); };
    root.querySelector('[data-page]').onclick = function () { openLink(d.url); };
    root.querySelector('[data-ask]').onclick = function () { renderForm(d); };
    if (d.map) drawMap(document.getElementById('minimap'), [d], 13);
  }

  function renderForm(d) {
    if (state.data && state.data !== d) state.stack.push(state.data);
    state.data = { kind: 'form' };
    // Opened straight from request_details there is nothing to go back to, so no Back button.
    root.innerHTML = (state.stack.length ? '<button class="back" data-back>‹ ' + esc(t('back')) + '</button>' : '')
      + '<div class="eyebrow">' + esc(d.name) + '</div><h2>' + esc(t('formTitle')) + '</h2><p class="p">' + esc(t('formLead')) + '</p>'
      + '<div class="form"><div class="row"><label class="f">' + esc(t('first')) + '<input type="text" name="first_name" autocomplete="given-name" maxlength="60"></label>'
      + '<label class="f">' + esc(t('last')) + '<input type="text" name="last_name" autocomplete="family-name" maxlength="60"></label></div>'
      + '<div class="row"><label class="f">' + esc(t('email')) + '<input type="email" name="email" autocomplete="email" maxlength="120"></label>'
      + '<label class="f">' + esc(t('phone')) + '<input type="tel" name="phone" autocomplete="tel" maxlength="30"></label></div>'
      + '<label class="f">' + esc(t('message')) + '<textarea name="message" maxlength="1000"></textarea></label>'
      + '<label class="consent"><input type="checkbox" name="consent"><span>' + esc(t('consent')) + '</span></label>'
      + '<div class="actions"><button class="btn" type="button" data-send>' + esc(t('send')) + '</button></div><div data-out></div></div>';
    if (root.querySelector('[data-back]')) root.querySelector('[data-back]').onclick = back;
    // Not a <form>: hosts sandbox the view without allow-forms, which drops a submit event silently.
    var form = root.querySelector('.form');
    var field = function (n) { return form.querySelector('[name=' + n + ']'); };
    form.querySelector('[data-send]').onclick = function () {
      var v = function (n) { return (field(n).value || '').trim(); };
      var out = form.querySelector('[data-out]');
      if (!v('first_name') || !v('last_name') || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v('email')) || !field('consent').checked) {
        out.innerHTML = '<div class="msg">' + esc(t('required')) + '</div>'; setTimeout(reportSize, 30); return;
      }
      var btn = form.querySelector('[data-send]'); btn.disabled = true; btn.textContent = t('sending');
      // Straight to the server's enquiry route, not through a tool: only this click sends it.
      fetch('https://nuevaliving.com/mcp', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kind: 'enquiry', first_name: v('first_name'), last_name: v('last_name'), email: v('email'), phone: v('phone') || undefined,
          message: v('message') || undefined, slugs: d.slugs || [d.slug], consent: true, language: state.lang }) })
        .then(function (res) { return res.json(); })
        .then(function (r) {
          if (r && r.sent) { form.innerHTML = '<div class="msg">' + esc(t('sent')) + '</div>'; }
          else { out.innerHTML = '<div class="msg">' + esc(t('failed')) + '</div>'; btn.disabled = false; btn.textContent = t('send'); }
          setTimeout(reportSize, 30);
        })
        .catch(function () { out.innerHTML = '<div class="msg">' + esc(t('failed')) + '</div>'; btn.disabled = false; btn.textContent = t('send'); setTimeout(reportSize, 30); });
    };
    setTimeout(reportSize, 30);
  }

  function renderSent(data) {
    root.innerHTML = '<div class="eyebrow">' + esc(t('eyebrow')) + '</div><div class="msg" style="margin-top:8px">' + esc(data.sent ? t('sent') : (data.error || t('failed'))) + '</div>';
  }

  /* ---------- map ----------
     The site's own base map: the vendored Leaflet and protomaps-leaflet, drawing the self-hosted
     OpenStreetMap extract in the palette of the developments map. If the archive cannot be read the
     pins still stand on a plain ground. */
  var SITE = 'https://nuevaliving.com/assets/liora/';
  var BOUNDS = [[36.00, -5.75], [37.15, -3.80]];
  var PALETTE = { water: '#c8dbe0', earth: '#f7f3ec', beach: '#f3ead6', green: '#eceedf', greenDeep: '#e6e9d6', built: '#ece5d8',
    roadMinor: '#e8dfce', roadMajor: '#dccfb6', roadHighway: '#cdbc9a', placeLabel: '#5a4e3d', placeHalo: '#f7f3ec', seaLabel: '#7b97a4' };
  function loadScript(src) {
    return new Promise(function (resolve, reject) { var s = document.createElement('script'); s.src = src; s.onload = resolve; s.onerror = reject; document.head.appendChild(s); });
  }
  var libs = null;
  function loadLibraries() {
    if (libs) return libs;
    var css = document.createElement('link'); css.rel = 'stylesheet'; css.href = SITE + 'vendor/leaflet/leaflet.css'; document.head.appendChild(css);
    libs = loadScript(SITE + 'vendor/leaflet/leaflet.js').then(function () {
      return loadScript(SITE + 'vendor/protomaps-leaflet/protomaps-leaflet.js').catch(function () { return null; });
    });
    return libs;
  }
  function ramp(stops) {
    return function (z) {
      if (z <= stops[0][0]) return stops[0][1];
      for (var i = 1; i < stops.length; i += 1) {
        if (z <= stops[i][0]) { var a = stops[i - 1], b = stops[i]; return a[1] + (b[1] - a[1]) * ((z - a[0]) / (b[0] - a[0])); }
      }
      return stops[stops.length - 1][1];
    };
  }
  function basemap(lang) {
    var P = window.protomapsL;
    if (!P || !P.leafletLayer || !P.PmtilesSource) return null;
    try {
      var flavor = { background: PALETTE.water, earth: PALETTE.earth, water: PALETTE.water, park_a: PALETTE.green, park_b: PALETTE.green,
        wood_a: PALETTE.greenDeep, wood_b: PALETTE.greenDeep, scrub_a: PALETTE.green, scrub_b: PALETTE.green, hospital: PALETTE.earth,
        industrial: PALETTE.built, school: PALETTE.earth, zoo: PALETTE.green, beach: PALETTE.beach, sand: PALETTE.beach, glacier: PALETTE.earth,
        aerodrome: PALETTE.built, pedestrian: PALETTE.earth, pier: PALETTE.built, runway: PALETTE.built, buildings: PALETTE.built, major: PALETTE.roadMajor,
        landcover: { grassland: PALETTE.green, barren: PALETTE.earth, urban_area: PALETTE.earth, farmland: PALETTE.earth, glacier: PALETTE.earth, scrub: PALETTE.green, forest: PALETTE.greenDeep } };
      var road = function (kinds, color, stops) {
        return { dataLayer: 'roads', symbolizer: new P.LineSymbolizer({ color: color, width: ramp(stops), lineCap: 'round', lineJoin: 'round' }),
          filter: function (z, f) { return kinds.indexOf(f.props.kind) >= 0; } };
      };
      var paint = P.paintRules(flavor).filter(function (r) { return r.dataLayer !== 'roads' && r.dataLayer !== 'boundaries'; });
      paint.push(road(['minor_road'], PALETTE.roadMinor, [[12, 0], [13, 0.4], [14, 0.8], [16, 2]]));
      paint.push(road(['major_road'], PALETTE.roadMajor, [[8, 0], [10, 0.4], [12, 0.7], [14, 1.4], [16, 3]]));
      paint.push(road(['highway'], PALETTE.roadHighway, [[7, 0], [8, 0.5], [11, 0.9], [14, 2], [16, 4]]));
      var names = ['name:' + lang, 'name'];
      var labels = [
        { dataLayer: 'water', symbolizer: new P.CenteredTextSymbolizer({ labelProps: names, fill: PALETTE.seaLabel, fontFamily: 'Montserrat, Arial, sans-serif', fontStyle: 'italic', fontWeight: 400, fontSize: ramp([[8, 11], [12, 13]]), letterSpacing: 2 }),
          filter: function (z, f) { return f.geomType === P.GeomType.Point && ['sea', 'ocean', 'bay', 'strait'].indexOf(f.props.kind) >= 0; } },
        { dataLayer: 'places', minzoom: 8, symbolizer: new P.CenteredTextSymbolizer({ labelProps: names, fill: PALETTE.placeLabel, stroke: PALETTE.placeHalo, width: 2.5, fontFamily: 'Montserrat, Arial, sans-serif', fontWeight: 500,
            fontSize: function (z, f) { var d = f && f.props.kind_detail; return d === 'city' ? 15 : (d === 'town' ? 13.5 : 12); } }),
          filter: function (z, f) { if (f.props.kind !== 'locality') return false; var d = f.props.kind_detail; return d === 'city' || d === 'town' || (d === 'village' && z >= 11); } }
      ];
      return P.leafletLayer({ url: new P.PmtilesSource(SITE + 'tiles/costa-del-sol.pmtiles', false).p, paintRules: paint, labelRules: labels,
        backgroundColor: PALETTE.water, lang: lang, maxDataZoom: 14, bounds: BOUNDS,
        attribution: '&copy; OpenStreetMap contributors &middot; Protomaps' });
    } catch (e) { return null; }
  }
  function drawMap(node, items, zoom) {
    if (!node) return;
    loadLibraries().then(function () {
      var L = window.L;
      node.style.background = PALETTE.earth;
      var map = L.map(node, { scrollWheelZoom: false, maxBounds: [[35.6, -6.4], [37.5, -3.2]], minZoom: 8, maxZoom: 16 });
      var layer = basemap(state.lang);
      if (layer) layer.addTo(map);
      var icon = L.divIcon({ className: '', html: '<div class="pin"></div>', iconSize: [14, 14], iconAnchor: [7, 7] });
      var pts = [];
      items.forEach(function (r) {
        if (!r.map) return;
        var ll = [r.map.lat, r.map.lng]; pts.push(ll);
        var m = L.marker(ll, { icon: icon, title: r.name }).addTo(map);
        m.bindPopup('<div class="pop"><b>' + esc(r.name) + '</b>' + esc(r.from || '') + '</div>');
        if (r.slug && items.length > 1) m.on('dblclick', function () { callTool('get_development', { slug: r.slug, language: state.lang }).then(function (d) { show(d, true); }); });
      });
      if (pts.length === 1) map.setView(pts[0], zoom || 12);
      else if (pts.length) map.fitBounds(pts, { padding: [30, 30], maxZoom: 13 });
      else map.setView([36.5, -4.95], 9);
      setTimeout(function () { map.invalidateSize(); }, 60);
    }).catch(function () { node.remove(); setTimeout(reportSize, 30); });
  }

  /* ---------- start ---------- */
  if (openai) {
    if (openai.theme) applyContext({ theme: openai.theme });
    var first = openai.toolOutput;
    if (first) show(first);
    window.addEventListener('openai:set_globals', function (e) {
      var g = (e && e.detail && e.detail.globals) || {};
      if (g.theme) applyContext({ theme: g.theme });
      if (g.toolOutput && g.toolOutput !== state.data) { state.stack = []; show(g.toolOutput); }
    });
  }
  request('ui/initialize', { appInfo: { name: 'nueva-living-view', version: '1.0.0' }, appCapabilities: {}, protocolVersion: '2026-01-26' })
    .then(function (r) { applyContext(r && r.hostContext); notify('ui/notifications/initialized', {}); })
    .catch(function () {});
  root.innerHTML = '<p class="note">' + esc(t('loading')) + '</p>';
})();
`;

const WIDGET_HTML = '<!doctype html><html lang="en"><head><meta charset="utf-8">'
  + '<meta name="viewport" content="width=device-width, initial-scale=1">'
  + '<title>Nueva Living</title>'
  + '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
  + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Montserrat:wght@400;500;600&display=swap">'
  + '<style>' + STYLE + '</style></head><body><div id="app"></div>'
  + '<script>window.__I18N__=' + JSON.stringify(I18N).replace(/</g, '\\u003c') + ';</script>'
  + '<script>' + SCRIPT + '</script>'
  + '</body></html>';

module.exports = { WIDGET_HTML };
