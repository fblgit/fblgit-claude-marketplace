---
name: adp-minimal-runtime
description: "Reference for the ADP page shell and the adp.js runtime: the shell's markup contract and ADP.page(), content as data, the What changed panel, comment anchors, the integrity verdict, the checks/latest self-check, first-open seeding, switches in config/current (edit.locked, look.theme, look.mode) and the public ADP API. Use when the user asks what adp.js does in a page, how seeding works, what a switch is, or what ADP.* exposes to page code."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The shell and the runtime

The **shell** is the minimal `index.html` of an adp/2 page. The **runtime** is `adp.js`, a single script loaded before the page's own code.
Together they are the part of ADP that runs in the browser. All host I/O (records, comments, publishing) goes through the
[host adapter](../adp-minimal-hosts/SKILL.md).

## The shell

This is the `index.html` of the [`minimal` template](../adp-minimal-new-artifact/SKILL.md#templates), abridged; the commented lines are
added only when the page takes catalog entries:

```html
<meta name="adp:build" content="1">
<link rel="stylesheet" href="styles/page.css">
<!-- <link rel="stylesheet" href="kit/themes/<id>.css">   a taken theme: after page.css, so its tokens win -->
<!-- part:page.header -->
<header data-part="page.header" data-comment-target>
  <h1>Title</h1>
  <!-- part:page.changes --><details id="wc" data-part="page.changes" data-comment-target hidden>
    <summary>What changed <span id="wcN"></span></summary><ol id="wcChanges"></ol><ul id="wcDecisions"></ul><ul id="wcIncoming"></ul>
  </details><!-- /part:page.changes -->
</header>
<!-- /part:page.header -->
<!-- part:page.tabs --><nav data-part="page.tabs" data-comment-target></nav><!-- /part:page.tabs -->
<main id="views"> ... each view a part ... </main>
<script src="content.js"></script>
<script src="adp.js"></script>
<!-- <script src="kit/....js"></script>   taken kit scripts, dependencies first -->
<script src="parts/app.js"></script>   <!-- the page's own code, last -->
```

Every part sits between its markers and carries `data-part`; `data-comment-target` marks it as a place a comment can anchor. The page
contract:

- `<meta name="adp:build">` and `content.js` (which defines `window.ADP_CONTENT`) load before `adp.js`.
- The parts `page.header`, `page.tabs` and `page.changes` exist; the self-check reports any that are missing.
- After rendering its views, the page calls `ADP.page()` exactly once:

```js
ADP.page({
  view:     () => currentView,                    // the current view's id
  expected: view => ['home.lead', 'home.cards'],  // the part ids that view must render
  titles:   {'home.lead': 'Lead'},                // anchor labels
  legacy:   {},                                   // old CSS-path anchors -> part ids
  all:      ALL_PART_IDS,                         // every known part id
  reveal:   (id, key) => openViewHolding(id, key) // show the part (and the keyed record)
});
```

## What the runtime does

| Job | Behaviour |
|---|---|
| **Content as data** | `ADP.content(id)` returns the `html` field of `content/<id>` from the database, falling back to `ADP_CONTENT[id]`. A live subscription repaints every `[data-part="<id>"]` when the document changes. |
| **What changed** | Fills the panel with the ten most recent `changes/`, the active `decisions/`, and up to ten proposals from `incoming/`. The `panel.changes` switch controls who sees it. |
| **Comment anchors** | Registers part-id anchors: a click in comment mode composes on the nearest `[data-part]`; threads are placed on the matching element. |
| **Integrity at open** | Hashes the page, compares it with `manifest/current` and writes a verdict to `status/integrity`: `consistent`, `files_ahead`, `record_ahead` or `mixed`. Where the database rules refuse the write, the verdict is kept in `ADP.integrity`. |
| **Self-check** | For an editor, shortly after `ADP.page()` and again after DOM changes, writes `checks/latest`: missing parts, `[data-part]` ids not listed in `all`, horizontal overflow, script errors, failed loads and unhandled rejections, anchor counts. |
| **Seeding** | On the first open by an editor, when the host serves the page's files and `manifest/current` does not exist, expands `seed.json` and `seed/pack-*.json` into the database, `manifest/current` last ([Seeding](#seeding)). |
| **Settings** | `ADP.config` reads and writes the switches in `config/current`. |

Content as data paints the stored HTML as is, so `content/` must be writable only by the page's editors (the host's access rules), and
anything that writes it treats viewer input as text, never as markup.

After every publish, read `checks/latest`.

The runtime keeps a little state for the jobs below: the page's registration, the database once connected, the viewer, the live content
documents, and up to twenty distinct errors (script errors, failed loads, unhandled rejections), each of which schedules a self-check.

```js
// ---
// id: runtime.state
// tool: adp.js
// section: runtime
// order: 220
// needs: [hosts.connect, runtime.hash]
// tests: [runtime-an-editor-seeds-an-empty-record]
// sha: fad97fcc3a44
// ---
const meta = document.querySelector('meta[name="adp:build"]'), BUILD = meta ? meta.content : '';
const live = {}, errors = [], stats = {anchors: 'not started', threads: 0, placed: 0, unknown: []};
const user = {canEdit: false, id: '', can: () => Promise.resolve(null)};
let PAGE = null, db = null, canEdit = false, probe = '';
const pushErr = m => { m = String(m).slice(0, 300); if (errors.length < 20 && !errors.includes(m)) { errors.push(m); later(); } };
addEventListener('error', e => {
  const t = e.target;
  if (t && t !== window && (t.src || t.href)) pushErr('load failed: ' + String(t.src || t.href).split('/').slice(-2).join('/'));
  else pushErr((e.message || 'error') + (e.filename ? ' @ ' + e.filename.split('/').pop() + ':' + e.lineno : ''));
}, true);
addEventListener('unhandledrejection', e => { const r = e.reason; pushErr('unhandled: ' + (r && (r.code || r.message) || r)); });
const when = v => { const d = new Date(v); return isNaN(d) ? '' : d.toLocaleString('en-GB', {day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'}); };
const sel = id => '[data-part="' + id + '"]', $ = id => document.getElementById(id);
const mk = (tag, cls, txt) => { const n = document.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = String(txt); return n; };
```

`content.js` is the baseline; a `content/<part id>` document overrides it live. A part with neither is an error for the self-check:

```js
// ---
// id: runtime.content
// tool: adp.js
// section: runtime
// order: 230
// needs: [runtime.state]
// tests: [runtime-an-editor-seeds-an-empty-record]
// sha: 5f79724ad5e7
// ---
const baseline = () => window.ADP_CONTENT || {};
function content(id) {
  const d = live[id] || baseline()[id];
  if (!d || typeof d.html !== 'string') { pushErr('content missing: ' + id); return ''; }
  return d.html;
}
function paint(id) { const h = content(id); document.querySelectorAll(sel(id)).forEach(el => { if (el.innerHTML !== h) el.innerHTML = h; }); }
function watchContent() {
  db.collection('content').onSnapshot(snap => {
    const touched = snap.docChanges().map(c => {
      const id = c.doc.id, v = c.type === 'removed' ? null : c.doc.data();
      if (!ID.test(id)) return '';
      if (v && typeof v.html === 'string') live[id] = v; else delete live[id];
      return id;
    });
    touched.filter(Boolean).forEach(paint);
  }, e => pushErr('content snapshot: ' + (e && e.code)));
}
ADP.content = content;
```

The What changed panel (`#wc`) lists the ten latest `changes/` (a recorded version, a data change or the change id, with when, who, the
summary and up to twelve part ids), the active `decisions/`, and the ten latest proposals in `incoming/` with their status (a merged proposal is
recorded in the database, its files not yet published). It adds the Incoming list when the page's markup has none, and hides itself when the
database refuses the queries:

```js
// ---
// id: runtime.changes
// tool: adp.js
// section: runtime
// order: 240
// needs: [runtime.state]
// sha: e86d291beedb
// ---
function changesPanel() {
  const el = $('wc'); if (!el) return;
  el.hidden = hideChanges();
  const note = (box, t) => box.replaceChildren(mk('li', 'wc-empty', t));
  const partsOf = a => { const w = mk('div', 'wc-parts'); (Array.isArray(a) ? a : []).slice(0, 12).forEach(x => { const id = typeof x === 'string' ? x : x && x.id; if (id) w.append(mk('code', '', id)); }); return w.childNodes.length ? w : null; };
  const item = (top, text, parts) => { const li = mk('li'), p = partsOf(parts); li.append(...top, mk('p', '', text)); if (p) li.append(p); return li; };
  const head = (b, at, by) => { const h = mk('div', 'wc-h'); h.append(mk('b', '', b), mk('span', '', [when(at), by].filter(Boolean).join(' · '))); return h; };
  const feed = (q, box, empty, what, rows) => {
    note($(box), 'Loading…');
    q.onSnapshot(snap => { const docs = snap.docs.filter(d => d.exists), r = rows(docs); r.length ? $(box).replaceChildren(...r) : note($(box), empty); },
      () => note($(box), what + ' could not be read.'));
  };
  try {
    feed(db.collection('changes').orderBy('at', 'desc').limit(10), 'wcChanges', 'Nothing recorded yet.', 'Changes', docs => {
      $('wcN').textContent = docs.length ? String(docs.length) : '';
      return docs.map(d => { const c = d.data() || {};
        return item([head(c.version ? 'Version ' + c.version : Array.isArray(c.parts) && !c.parts.length ? 'Data change' : d.id, c.at, c.by)], c.summary || '', c.parts); });
    });
    feed(db.collection('decisions').where('status', '==', 'active'), 'wcDecisions', 'None recorded yet.', 'Decisions', docs => docs.map(d => {
      const c = d.data() || {}, li = mk('li'), p = partsOf(c.parts);
      li.append(mk('blockquote', '', c.quote || d.id), mk('div', 'wc-h', when(c.at))); if (p) li.append(p); return li;
    }));
    if (!$('wcIncoming')) { const s = mk('section'); s.append(mk('h3', '', 'Incoming'), Object.assign(mk('ol', 'wc-list'), {id: 'wcIncoming'})); (el.querySelector('.wc-body') || el).prepend(s); }
    const say = {new: 'arrived', merged: 'merged, not yet published', held: 'held', applied: 'applied', declined: 'declined'};
    feed(db.collection('incoming'), 'wcIncoming', 'Nothing proposed.', 'Incoming', docs => docs.map(d => ({pid: d.id, ...d.data()}))
      .sort((a, b) => String(b.at || '').localeCompare(String(a.at || ''))).slice(0, 10).map(c => {
        const st = c.status || 'new', why = st === 'held' && c.classified ? ': held on ' + (c.classified.held || []).map(x => x.id).join(', ')
          : st === 'declined' && c.decided ? ': ' + (c.decided.reason || '') : '';
        return item([head(say[st] || st, c.at, c.by)], (c.summary || c.pid) + why, (c.parts || []).map(x => x.id));
      }));
  } catch (e) { el.hidden = true; }
}
```

A comment anchors to `<part id>` or `<part id>:<data-part-key>`; an anchor in the page's `legacy` map (or starting with one of its keys) is read
as the part id it maps to. In comment mode a click composes on the nearest `[data-part]` outside `[data-uncommentable]`, labelled with the
part's title (a locked part says so); pointer presses there are swallowed, the hovered part is outlined, and threads are placed on the first
visible element that matches. `reveal` asks the page to show a part that is not on screen, then scrolls to it:

```js
// ---
// id: runtime.anchors
// tool: adp.js
// section: runtime
// order: 250
// needs: [runtime.state]
// sha: 2fc16d7357b1
// ---
let ctl = null, cmode = false, threads = [], hlEl = null;
const visible = el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
function parseAnchor(a) {
  const lg = PAGE && PAGE.legacy, leg = lg ? lg[a] || Object.keys(lg).filter(k => a.startsWith(k)).map(k => lg[k])[0] : null;
  const s = leg || a, i = s.indexOf(':'), pid = i < 0 ? s : s.slice(0, i), key = i < 0 ? '' : s.slice(i + 1);
  return ID.test(pid) ? {pid, key, legacy: !!leg} : null;
}
function resolveAnchor(a) {
  const p = parseAnchor(a); if (!p) return null;
  const els = [...document.querySelectorAll(sel(p.pid))].filter(visible);
  return (p.key && els.find(e => e.dataset.partKey === p.key)) || els[0] || null;
}
function placeThreads() {
  if (!ctl) return;
  const m = {}, unknown = [];
  threads.forEach(t => {
    const el = resolveAnchor(t.anchor);
    if (el) { const r = el.getBoundingClientRect(); m[t.id] = {x: Math.round(Math.max(r.left + 12, r.right - 16) + scrollX), y: Math.round(r.top + 14 + scrollY)}; }
    else if (!parseAnchor(t.anchor)) unknown.push(t.anchor.slice(0, 160));
  });
  try { ctl.placed(m); } catch (e) {}
  if (threads.length) Object.assign(stats, {threads: threads.length, placed: Object.keys(m).length, unknown: unknown.slice(0, 8)});
}
const target = n => { const el = n && n.closest ? n.closest('[data-part]') : null; return el && !el.closest('[data-uncommentable]') ? el : null; };
function label(el) {
  const t = PAGE && PAGE.titles ? PAGE.titles[el.dataset.part] : '', key = el.dataset.partKey;
  const s = ((t || el.getAttribute('aria-label') || el.dataset.part) + (key ? ', ' + key : '')).slice(0, 120);
  return partLocked(el.dataset.part) ? '\u{1F512} locked: ' + s : s;
}
function hl(el) { if (hlEl === el) return; if (hlEl) hlEl.classList.remove('adp-hl'); hlEl = el; if (el) el.classList.add('adp-hl'); }
async function anchors() {
  const cm = hostComments;
  if (!isFn(cm, 'customAnchors')) { stats.anchors = 'comments unavailable'; return later(); }
  document.head.append(mk('style', '', '.adp-cmode [data-part]{cursor:crosshair}.adp-hl{outline:2px solid var(--accent,#9A5406)!important;outline-offset:-2px}'));
  try {
    ctl = await cm.customAnchors({
      mode: on => { cmode = on; document.documentElement.classList.toggle('adp-cmode', on); if (!on) { threads = []; hl(null); } },
      threads: l => { threads = Array.isArray(l) ? l : []; placeThreads(); later(); },
      reveal: id => { revealThread(id); },
      composing: () => {}});
  } catch (e) { stats.anchors = 'not registered: ' + (e && e.code || e); return later(); }
  stats.anchors = 'registered';
  const swallow = e => { if (e.isTrusted && cmode && ctl && target(e.target)) { e.preventDefault(); e.stopPropagation(); } };
  ['pointerdown', 'mousedown', 'mouseup', 'dragstart'].forEach(t => document.addEventListener(t, swallow, true));
  document.addEventListener('click', e => {
    if (!cmode || !e.isTrusted) return; const el = target(e.target); if (!el) return;
    e.preventDefault(); e.stopPropagation();
    ctl.compose(el.dataset.part + (el.dataset.partKey ? ':' + el.dataset.partKey : ''), el, {label: label(el)}).catch(err => pushErr('compose: ' + (err && err.code)));
  }, true);
  document.addEventListener('pointermove', e => { if (cmode) hl(target(e.target)); }, true);
  placeThreads(); later();
}
async function revealThread(h) {
  const t = threads.find(x => x.id === h); if (!t) return;
  const p = parseAnchor(t.anchor); let el = resolveAnchor(t.anchor);
  if (el && p && p.key && el.dataset.partKey !== p.key) el = null;
  if (!el && p && PAGE && PAGE.reveal) { await PAGE.reveal(p.pid, p.key); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))); el = resolveAnchor(t.anchor); }
  if (el) el.scrollIntoView({block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
  placeThreads();
}
```

The self-check runs 1.5 s after the last trigger (`ADP.page()`, a DOM change, a resize, an error, a switch change). It sets `window.ADP_CHECK`
for anyone, starts the integrity check, and for an editor writes `checks/latest` (an `update`, else a `"set"`) when its body differs from the last
one written:

```js
// ---
// id: runtime.check
// tool: adp.js
// section: runtime
// order: 260
// needs: [runtime.content]
// sha: 8a860b5b57b5
// ---
let tCheck = 0, lastSent = '', sending = false;
const viewsSeen = {};
function later() { clearTimeout(tCheck); tCheck = setTimeout(selfCheck, 1500); }
async function selfCheck() {
  if (!PAGE) return;
  const view = PAGE.view(), missing = ['page.header', 'page.tabs', 'page.changes'].concat(PAGE.expected(view) || []).filter(id => !document.querySelector(sel(id)));
  const known = new Set(PAGE.all || []), unmarked = [...new Set([...document.querySelectorAll('[data-part]')].map(e => e.dataset.part))].filter(id => !known.has(id));
  const over = Math.max(0, document.documentElement.scrollWidth - innerWidth), ok = !missing.length && !unmarked.length && !over && !errors.length;
  viewsSeen[view] = {ok, missing, overflow_x: over, width: innerWidth};
  window.ADP_CHECK = {build: BUILD, view, ok, missing, unmarked, overflow_x: over, errors: errors.slice(), anchors: {...stats}, probe, integrity};
  integrityAt();
  if (!db || !canEdit || sending) return;
  const n = Object.keys(live).length, body = {build: BUILD, view, ok, missing, unmarked, overflow_x: over, width: innerWidth, errors: errors.slice(),
    content: {source: n ? 'db' : 'file', db_docs: n, file_docs: Object.keys(baseline()).length},
    locked: !!get('edit.locked'), config_at: cdoc ? cdoc.at : '', fetch_sibling: probe, anchors: {...stats}, views: viewsSeen, seeded,
    integrity: integrity ? {verdict: integrity.verdict, page_hash: integrity.page_hash, drift: integrity.drift, written: integrity.written} : null};
  const key = JSON.stringify(body); if (key === lastSent) return;
  sending = true;
  const ref = db.doc('checks/latest'), data = {at: new Date().toISOString(), ...body};
  try { await ref.update(data); lastSent = key; }
  catch (e) { try { await ref.set(data); lastSent = key; } catch (e2) { if (errors.length < 20) errors.push('check write: ' + (e2 && e2.code)); } }
  sending = false;
}
```

Integrity runs once per open. A part whose hash differs from `manifest/current` while its content document matches the baseline is
`files_ahead`; a content document that differs from the baseline is `record_ahead`; both is `mixed`. With no manifest the verdict is
`record_ahead` if content was edited, else `consistent`. Elements marked `data-adp-integrity` show the verdict, as `panel.checks` allows:

```js
// ---
// id: runtime.integrity
// tool: adp.js
// section: runtime
// order: 270
// needs: [runtime.check]
// sha: 6d2953ac7a26
// ---
let integrity = null, integrityRun = null;
function integrityAt() {
  if (integrityRun || !db) return;
  integrityRun = (async () => {
    const page = await hashText(document.documentElement.outerHTML);
    let rec = null;
    try { const s = await db.doc('manifest/current').get(); rec = s && s.exists ? s.data() || null : null; } catch (e) {}
    const mp = rec && (rec.parts || (rec.data && rec.data.parts)) || {}, b = baseline();
    const edited = Object.keys(live).filter(id => b[id] && live[id].html !== b[id].html);
    const ahead = Object.keys(page.parts).filter(id => id in mp && mp[id] !== page.parts[id] && !edited.includes(id));
    const v = !ahead.length && !edited.length ? 'consistent' : !edited.length ? 'files_ahead' : !ahead.length ? 'record_ahead' : 'mixed';
    integrity = {at: new Date().toISOString(), by: 'page', page_hash: page.page_hash, parts: page.parts,
      verdict: rec ? v : edited.length ? 'record_ahead' : 'consistent', drift: [...new Set(ahead.concat(edited))].sort(), written: false};
    if (window.ADP_CHECK) window.ADP_CHECK.integrity = integrity;
    try { const {written, ...d} = integrity; await db.doc('status/integrity').set(d); integrity.written = true; }
    catch (e) { integrity.write_error = String(e && e.code || e); }
    badge(); later();
  })().catch(e => pushErr('integrity: ' + (e && e.message || e)));
}
function badge() {
  const m = get('panel.checks'); if (!integrity || m === 'off' || (m === 'editors' && !canEdit)) return;
  document.querySelectorAll('[data-adp-integrity]').forEach(el => {
    el.textContent = integrity.verdict === 'consistent' ? 'Consistent' : integrity.verdict.replace('_', ' ') + ': ' + integrity.drift.slice(0, 6).join(', ');
    el.dataset.verdict = integrity.verdict; el.title = 'page ' + integrity.page_hash + (integrity.written ? ', recorded in status/integrity' : ', kept in memory');
  });
}
```

### Seeding

An agent publishes the page once, with `seed.json` and `seed/` beside it. The first editor to open it, on a host that serves the page's files:

1. stops if `manifest/current` exists (already seeded);
2. reads `seed.json` (`adp-seed/2`, an index of packs; `adp-seed/1`, which held the documents inline, is still accepted) and fetches every
   pack before writing anything;
3. checks `manifest/current` again, in case a concurrent editor has seeded the page meanwhile;
4. writes the documents six at a time, recording progress in `status/seed` (`state: "seeding"`) every 25 documents;
5. writes `manifest/current` alone and last, then `status/seed` with `state: "done"`, and sets `ADP.seeded`.

While this runs, a first-open panel shows progress and a short introduction to ADP. If a pack is missing, the panel names it, the error is
recorded for the self-check, and nothing is written.

Agents read `manifest/current` first and step 1 tests it, so a run that stops partway leaves no manifest and the next editor's open starts over.
Step 3 narrows the race between two editors but does not close it; that is safe because seed writes are idempotent `"set"` writes of the same data.
Read-only viewers never seed.

The first-open panel walks through five short paragraphs on ADP while the bar fills, then offers Close (it closes itself after a minute):

```js
// ---
// id: runtime.tour
// tool: adp.js
// section: runtime
// order: 280
// needs: [runtime.state]
// sha: c3a3aac11d80
// ---
const TOUR = [
  ['Files are parts', 'Every file of this artifact is cut into named parts (a part:id marker around each). A part has a hash; the manifest lists them all. The agent published those files once, as one artifact.'],
  ['Copy is data', 'The text on the page is not in the files: it lives in content docs, one per part. Editing a sentence is a database write, not a republish.'],
  ['The database is the record', 'parts/, content/, changes/ and agents/ say what is live, who changed it and when; manifest/current is the truth the agents read first. That record is being written now, from the seed packs published beside the page.'],
  ['What changed, and Settings', 'The "What changed" panel in the header reads changes/ live. Settings (the gear) holds the switches, "Incoming", where an agent\'s proposal is applied or declined by an editor, and who may write where.'],
  ['From here', 'Agents export, edit and propose; an editor applies. Nothing lands on this page without a record, and every version stays readable.']];
const TOUR_CSS = '.adp-seed{position:fixed;inset:auto 16px 16px 16px;z-index:9999;max-width:560px;max-height:calc(100vh - 32px);overflow:auto;box-sizing:border-box;margin:0 auto;padding:16px 18px;border-radius:12px;background:var(--panel,#fff);color:var(--ink,#1c1917);border:1px solid var(--rule,#e7e5e4);box-shadow:0 12px 40px rgba(0,0,0,.18);font:14px/1.45 var(--f-ui,system-ui,sans-serif)}'
  + '.adp-seed h2{margin:0 0 4px;font-size:16px}.adp-seed p{margin:0 0 8px}.adp-seed .adp-sd-bar{height:6px;border-radius:3px;background:var(--sunk,#f5f5f4);overflow:hidden;margin:8px 0}.adp-seed .adp-sd-bar i{display:block;height:100%;width:0;background:var(--accent,#9A5406);transition:width .2s}'
  + '.adp-seed ol{margin:8px 0;padding-left:20px}.adp-seed li{margin:0 0 6px;opacity:.45;transition:opacity .3s}.adp-seed li.on{opacity:1}.adp-seed li b{display:block}.adp-seed .adp-sd-meta{font-size:12px;color:var(--ink-3,#78716c)}'
  + '.adp-seed button{margin-top:8px;padding:6px 12px;border-radius:8px;border:1px solid var(--rule,#e7e5e4);background:var(--panel,#fff);color:inherit;cursor:pointer}'
  + '@media(prefers-reduced-motion:reduce){.adp-seed li,.adp-seed .adp-sd-bar i{transition:none}}';
function tour(f) {
  if (!document.body) return {step() {}, progress() {}, done() {}, fail() {}};
  document.head.append(mk('style', '', TOUR_CSS));
  const box = mk('aside', 'adp-seed'), line = mk('p', '', 'Reading the seed…'), bar = mk('div', 'adp-sd-bar'), fill = mk('i'), ol = mk('ol'), n = (f.packs || []).length;
  Object.entries({role: 'status', 'aria-live': 'polite', 'aria-label': 'First open'}).forEach(([k, v]) => box.setAttribute(k, v));
  const lis = TOUR.map(([t, d]) => { const li = mk('li'); li.append(mk('b', '', t), document.createTextNode(d)); ol.append(li); return li; });
  bar.append(fill);
  box.append(mk('h2', '', 'First open: this page is writing its own record'), line, bar, ol,
    mk('p', 'adp-sd-meta', (f.by ? 'Seeded by ' + f.by + '. ' : '') + (f.docs ? f.docs + ' docs in ' + n + ' pack' + (n === 1 ? '' : 's') + '.' : '')));
  document.body.append(box);
  const t0 = Date.now(), counts = {}; let step = -1, closed = false;
  const light = i => { if (i === step || closed) return; step = i; lis.forEach((li, k) => li.classList.toggle('on', k <= i)); };
  const close = () => { if (!closed) { closed = true; box.remove(); } };
  const btn = () => { const b = mk('button', '', 'Close'); b.type = 'button'; b.addEventListener('click', close); box.append(b); b.focus(); };
  return {
    step(k, total, path) { light(0); line.textContent = 'Fetching pack ' + k + ' of ' + total + ' (' + path + ')'; },
    progress(done, total, x) {
      counts[x.collection] = (counts[x.collection] || 0) + 1; fill.style.width = Math.round(100 * done / total) + '%';
      light(done < total / 3 ? 1 : done < total ? 2 : 3);
      line.textContent = 'Writing ' + done + ' of ' + total + ': ' + Object.keys(counts).map(c => c + ' ' + counts[c]).join(' · ');
    },
    done(why) {
      light(4); fill.style.width = '100%';
      line.textContent = why || 'Done: the record is written (' + Math.round((Date.now() - t0) / 100) / 10 + ' s). Reload any other open view of this page.';
      btn(); setTimeout(close, 60000);
    },
    fail(why) { line.textContent = 'Seeding stopped: ' + why + '. Reload to try again; nothing is half-written as truth, manifest/current goes last.'; btn(); }};
}
```

The seed itself, step by step as listed above. A `seed.json` of another schema is an error for the self-check and writes nothing:

```js
// ---
// id: runtime.seed
// tool: adp.js
// section: runtime
// order: 290
// needs: [runtime.tour]
// tests: [runtime-an-editor-seeds-an-empty-record, runtime-a-viewer-seeds-nothing, runtime-a-written-record-is-not-seeded-again,
//   runtime-a-host-without-files-seeds-nothing, runtime-a-missing-pack-writes-nothing, runtime-seed-inline-and-unknown]
// sha: cf33dcd185b0
// ---
let seeded = null;
async function seedFromFile(d) {
  let t = null;
  try {
    const has = async () => { const c = await d.doc('manifest/current').get().catch(() => null); return !!(c && c.exists); };
    if (await has()) return;
    const r = await fetch('seed.json', {cache: 'no-store'}); if (!r.ok) return;
    const f = await r.json(), v1 = f && f.schema === 'adp-seed/1' && Array.isArray(f.docs);
    if (!v1 && !(f && f.schema === 'adp-seed/2' && Array.isArray(f.packs))) return pushErr('seed.json: not adp-seed/1 or adp-seed/2');
    const packs = Array.isArray(f.packs) ? f.packs : [];
    t = tour(f);
    let docs = v1 ? f.docs.slice() : [];
    for (let k = 0; k < packs.length; k++) {           // every pack first, then the writes: a missing pack stops before anything lands
      const path = String(packs[k]); t.step(k + 1, packs.length, path);
      const pr = await fetch(path, {cache: 'no-store'});
      if (!pr.ok) { t.fail('pack ' + path + ' is not published (' + pr.status + ')'); return pushErr('seed: ' + path + ' ' + pr.status); }
      const pk = await pr.json(); docs = docs.concat(Array.isArray(pk && pk.docs) ? pk.docs : []);
    }
    docs = docs.filter(x => x && typeof x.collection === 'string' && typeof x.id === 'string' && x.data && typeof x.data === 'object');
    if (await has()) return t.done('Another editor was first: the record is already written.');
    const isMan = x => x.collection === 'manifest' && x.id === 'current', rest = docs.filter(x => !isMan(x)), man = docs.find(isMan);
    const total = rest.length + (man ? 1 : 0), at0 = new Date().toISOString(), opened_by = user.id || 'editor'; let done = 0;
    const put = async x => {
      await d.doc(x.collection + '/' + x.id).set(x.data); done++; t.progress(done, total, x);
      if (done % 25 === 0) await d.doc('status/seed').set({state: 'seeding', done, total, from: 'seed.json', opened_by, at: at0}).catch(() => {});
    };
    for (let i = 0; i < rest.length; i += 6) await Promise.all(rest.slice(i, i + 6).map(put));   // six at a time; manifest/current alone, last
    if (man) await put(man);
    seeded = {state: 'done', from: 'seed.json', version: String(f.version || ''), by: f.by || '', opened_by, docs: docs.length,
      packs: packs.length, at: new Date().toISOString()};
    await d.doc('status/seed').set(seeded).catch(() => {});
    window.ADP_SEED = seeded; t.done();
  } catch (e) { const m = e && (e.code || e.message) || e; pushErr('seed: ' + m); if (t) t.fail(String(m)); }
}
```

### Settings (switches)

A switch is one `group.name` value (`edit.locked`, `look.theme`, `look.mode`, `panel.changes`). `config/current` stores a value only when it
differs from the default, and records in `changed` who last changed each switch and when.
Groups: `edit`, `parts`, `comments`, `panel`, `playground`, `look`, `links`, `log`. `adp.py config` shows them; its subcommand that sets a switch (the word set, a switch name, then the value) changes one.

`edit.locked` is advisory. The runtime shows a banner and disables controls marked `data-adp-edit`, and `adp.py hold` and `adp.py record` refuse
to run while it is on; changing switches from page code is not blocked. If `edit.locked` is true, do not write: tell the user who locked the page, from
`changed["edit.locked"].by` in `config/current`.

```js
ADP.config.get('look.mode');                    // 'auto', 'light' or 'dark'
ADP.config.on('look.mode', v => applyMode(v));
await ADP.config.set('panel.changes', 'off');   // 'everyone', 'editors' or 'off'
```

`ADP.config.define(group, {name: {type, default, label, help, options, level}})` registers switches; a type is `bool`, `enum`, `url` (`https://`
or empty), `list` (of strings), `datetime` or `text` (up to 2000 characters, the default type). Setting a switch checks the value, then rewrites
`config/current` from a fresh read (one retry) and logs `changes/d-<ms>`; `reset(name)` sets one switch back to its default and `reset()` clears
them all. Listeners run when `ready` resolves (the first read of `config/current`, or no database), and then on every change. The page's `db` handle
takes no version, so a write is unpinned and the last writer wins.

```js
// ---
// id: runtime.config
// tool: adp.js
// section: runtime
// order: 300
// needs: [runtime.state]
// tests: [runtime-config-set, runtime-config-set-the-default-removes-it, runtime-config-set-a-wrong-value, runtime-config-set-an-unknown-switch,
//   runtime-config-set-by-a-viewer, runtime-config-set-checks-each-type, runtime-config-define-a-bare-switch]
// sha: fc87b88df1c0
// ---
const REG = {}, lis = {}, SEG = /^[a-z0-9][a-z0-9-]*$/;
let vals = {}, changed = {}, cdoc = null, isReady = false, resolveReady;
const readyP = new Promise(r => { resolveReady = r; });
function define(group, defs) {
  if (!SEG.test(group)) throw new Error('bad config group: ' + group);
  Object.entries(defs || {}).forEach(([n, d]) => {
    if (!SEG.test(n)) throw new Error('bad config name: ' + n);
    d = d || {};
    REG[group + '.' + n] = {...d, group, name: n, type: d.type || 'text', level: d.level || 'page',
      default: 'default' in d ? d.default : d.type === 'bool' ? false : d.type === 'list' ? [] : ''};
  });
  if (isReady) effects();
}
const get = k => k in vals ? vals[k] : REG[k] ? REG[k].default : undefined;
function all() {
  const o = {};
  Object.entries(REG).forEach(([k, d]) => { (o[d.group] = o[d.group] || {})[d.name] = {...d, value: get(k), changed: changed[k] || null}; });
  return o;
}
const fire = (k, only) => (only ? [only] : (lis[k] || []).concat(lis['*'] || [])).forEach(fn => {
  try { fn(get(k), k); } catch (e) { pushErr('config listener: ' + (e && e.message)); } });
function on(k, fn) {
  (lis[k] = lis[k] || []).push(fn);
  if (isReady) Promise.resolve().then(() => fire(k, fn));
  return () => { lis[k] = (lis[k] || []).filter(f => f !== fn); };
}
function checkValue(k, v) {
  const d = REG[k]; if (!d) throw new Error('Unknown setting ' + k);
  const ok = {bool: () => typeof v === 'boolean', enum: () => (d.options || []).includes(v), url: () => typeof v === 'string' && (v === '' || v.startsWith('https://')),
    list: () => Array.isArray(v) && v.every(x => typeof x === 'string'), datetime: () => typeof v === 'string' && (v === '' || !isNaN(Date.parse(v)))}[d.type];
  if (!(ok ? ok() : typeof v === 'string' && v.length <= 2000))
    throw new Error(k + ' needs ' + (d.type === 'enum' ? 'one of ' + (d.options || []).join(', ') : d.type === 'url' ? 'an https:// address or empty'
      : d.type === 'text' ? 'text up to 2000 characters' : 'a ' + d.type + ' value'));
}
async function save(edit, summary) {
  await readyP;
  if (!db) throw new Error('Settings cannot be saved here: this page has no database.');
  if (!canEdit) throw new Error('Settings cannot be saved: you cannot edit this artifact.');
  const ref = db.doc('config/current'); let err;
  for (let i = 0; i < 2; i++) {
    try {
      const snap = await ref.get(), cur = snap && snap.exists ? snap.data() || {} : {}, by = user.id || 'page', at = new Date().toISOString();
      const values = {...cur.values}, ch = {...cur.changed}; edit(values, ch, {by, at});
      await ref.set({schema: 'adp-config/1', at, by, values, changed: ch});
      if (get('log.data-changes') !== false)
        await db.doc('changes/d-' + Date.now()).set({version: '', at, by, summary, parts: [], threads: [], data: [{doc: 'config/current'}]}).catch(() => {});
      return;
    } catch (e) { err = e; }
  }
  throw err;
}
function set(k, v) {
  try { checkValue(k, v); } catch (e) { return Promise.reject(e); }
  const same = JSON.stringify(v) === JSON.stringify(REG[k].default);
  return save((values, ch, m) => { if (same) delete values[k]; else values[k] = v; ch[k] = {by: m.by, at: m.at}; }, 'Set ' + k + ' = ' + JSON.stringify(v));
}
function reset(k) {
  if (k !== undefined) return REG[k] ? set(k, REG[k].default) : Promise.reject(new Error('Unknown setting ' + k));
  return save((values, ch) => { Object.keys(values).forEach(x => delete values[x]); Object.keys(ch).forEach(x => delete ch[x]); }, 'Reset all settings');
}
function ready() { if (isReady) return; isReady = true; effects(); Object.keys(lis).forEach(k => lis[k].forEach(fn => fire(k, fn))); resolveReady(); }
function watchConfig() {
  const ref = db.doc('config/current');
  const take = snap => {
    const first = !isReady, old = vals;
    cdoc = snap && snap.exists ? snap.data() || null : null;
    vals = cdoc && cdoc.values && typeof cdoc.values === 'object' ? cdoc.values : {};
    changed = cdoc && cdoc.changed && typeof cdoc.changed === 'object' ? cdoc.changed : {};
    if (first) return ready();
    effects(); later();
    new Set([...Object.keys(old), ...Object.keys(vals)]).forEach(k => { if (JSON.stringify(old[k]) !== JSON.stringify(vals[k])) fire(k); });
  };
  try { ref.onSnapshot(take, e => { pushErr('config snapshot: ' + (e && e.code)); ready(); }); }
  catch (e) { ref.get().then(take, () => ready()); }
}
const config = Object.freeze({define, get, all, on, set, reset, ready: readyP, get doc() { return cdoc; }});
```

The built-in switches, and what the page wears from them: `data-adp-locked`, `data-adp-theme`, `data-adp-density` and `data-theme` on `<html>`, the
What changed panel hidden by `panel.changes`, and a banner while `edit.locked` is on that says who paused editing, until when and why.
`look.theme` offers only the theme `index.html` links (`kit/themes/<name>.css`, else `default`); a page with a theme switch defines it again with
the themes it installs.

```js
// ---
// id: runtime.switches
// tool: adp.js
// section: runtime
// order: 310
// needs: [runtime.config]
// tests: [runtime-config-set, runtime-config-set-checks-each-type]
// sha: dffe27f9a88e
// ---
let lockEl = null;
const partLocked = id => (get('parts.locked') || []).some(p => id === p || id.startsWith(p + '.'));
const hideChanges = () => { const m = get('panel.changes'); return m === 'off' || (m === 'editors' && !canEdit); };
function panels() {
  document.querySelectorAll(sel('page.changes')).forEach(el => {
    if (hideChanges()) { el.hidden = true; el.dataset.adpHid = '1'; } else if (el.dataset.adpHid) { el.hidden = false; delete el.dataset.adpHid; }
  });
}
function effects() {
  const h = document.documentElement, lk = !!get('edit.locked'), attr = (n, v) => v ? h.setAttribute(n, v) : h.removeAttribute(n), md = get('look.mode');
  h.toggleAttribute('data-adp-locked', lk);
  attr('data-adp-theme', get('look.theme')); attr('data-adp-density', get('look.density')); attr('data-theme', md === 'light' || md === 'dark' ? md : '');
  panels();
  if (!lk) { if (lockEl) lockEl.remove(); lockEl = null; return; }
  if (!document.body) return addEventListener('DOMContentLoaded', effects, {once: true});
  const by = (changed['edit.locked'] || {}).by, until = when(get('edit.until')), why = get('edit.reason');
  if (!lockEl) { lockEl = mk('div', 'adp-lock'); lockEl.setAttribute('role', 'status'); }
  lockEl.textContent = 'Editing is paused' + (by ? ' by ' + by : '') + (until ? ' until ' + until : '') + (why ? ': ' + why : '');
  if (document.body.firstChild !== lockEl) document.body.prepend(lockEl);
}
(document.head || document.documentElement).append(mk('style', '', 'html[data-adp-locked] [data-adp-edit]{pointer-events:none;opacity:.55}'
  + '.adp-lock{padding:8px 16px;background:var(--accent-soft,#fef3c7);color:var(--ink,#1c1917);border-bottom:2px solid var(--warn,#b45309);font:13px/1.4 var(--f-ui,system-ui,sans-serif)}'));
const RESERVED = 'Reserved: stored and shown, nothing reads it yet.', WHO = ['everyone', 'editors', 'off'];
const BUILT = (() => { const l = [...document.querySelectorAll('link[rel="stylesheet"][href^="kit/themes/"]')].pop(); return l ? l.getAttribute('href').slice(11, -4) : 'default'; })();
define('edit', {locked: {type: 'bool', label: 'Pause editing', help: 'Turns off pointer events on controls marked data-adp-edit (CSS only) and shows a banner; ADP.config.set ignores it.'},
  until: {type: 'datetime', label: 'Paused until', help: 'Shown in the banner; nothing lifts the freeze by itself.'}, reason: {type: 'text', label: 'Reason'},
  'require-hold': {type: 'bool', label: 'Require a hold', help: 'Only adp.py record --holds checks it: it refuses changed parts that already existed and that nobody holds (deepest parts only; hold_until is not checked).'}});
define('parts', {locked: {type: 'list', label: 'Locked parts', help: 'Part-id prefixes that are frozen.'}});
define('comments', {enabled: {type: 'bool', default: true, label: 'Comment mode', help: RESERVED}});
define('panel', {changes: {type: 'enum', options: WHO, default: 'everyone', label: 'What changed panel'}, checks: {type: 'enum', options: WHO, default: 'editors', label: 'Integrity badge'}});
define('playground', {enabled: {type: 'bool', default: true, label: 'Playground'}});
define('look', {theme: {type: 'enum', options: [BUILT], default: BUILT, label: 'Theme', help: 'The theme everyone sees. A page with a theme switch offers the themes it has installed and wears the chosen one; any other page offers only the theme it was built with. Also set as data-adp-theme on the page.'},
  mode: {type: 'enum', options: ['auto', 'light', 'dark'], default: 'auto', label: 'Colour mode'},
  density: {type: 'enum', options: ['comfortable', 'compact'], default: 'comfortable', label: 'Density', help: 'Sets data-adp-density on the page for your own CSS; the kit does not read it.'}});
define('links', {catalog: {type: 'url', label: 'Catalog', help: RESERVED}, board: {type: 'url', label: 'Board', help: RESERVED}, repo: {type: 'url', label: 'Repository', help: RESERVED}});
define('log', {'data-changes': {type: 'bool', default: true, label: 'Log data changes'}});
```

## The public API

| Member | What it is |
|---|---|
| `ADP.build` | The `adp:build` number, as a string. |
| `ADP.content(id)` | The current HTML of a part ([Content as data](#what-the-runtime-does)). |
| `ADP.page(cfg)` | Registers the page ([The shell](#the-shell)). |
| `ADP.config` | The switches: `get()`, `on()`, `set()`, `reset()`, `all()`, `define()`, the `ready` promise and the `doc` getter. |
| `ADP.user` | `canEdit`, `id`, and `can(name)`: a promise of the host's answer for a named right, or `null`. |
| `ADP.host` | The connection: `protocol`, `id`, `status`, and booleans for `records`, `comments`, `seedFiles`, `agent`, `publish`, `ask`. |
| `ADP.agent()`, `ADP.publish()`, `ADP.ask()` | Each returns a promise of the host's handle, or `null` when the host has none. |
| `ADP.claude(name)` | A promise of `window.claude.use(name)` when the connected host is Claude, else `null`. |
| `ADP.ns(name)` | `doc` and `collection` scoped to `ns/<name>/`; throws when there is no database. |
| `ADP.classify(base, live, incoming)` | The three-way classification ([details](#hashing-and-classifying-in-adpjs)). |
| `ADP.hash(text, files?)` | The part hash ([details](#hashing-and-classifying-in-adpjs)). |
| `ADP.integrity`, `ADP.seeded`, `ADP.db` | Getters: the integrity result, the seed record, the database handle (`null` when there is none). |

Components must use this API and must not access `window.claude` directly ([host adapters](../adp-minimal-hosts/SKILL.md)).
`window.ADP_CHECK` holds the last self-check and `window.ADP_SEED` the seed record, for a reader without the API.

Boot connects the host. A failed connection leaves the page static, with `ADP.host.status` `failed` and the error kept for the self-check. On
success it learns the viewer, seeds (an editor, on a host that serves files) before anything reads the record, then starts the panel, content
and switches, and probes that a sibling file (`content.js`) is served, for the self-check. DOM changes and resizes re-place threads and schedule a
self-check.

```js
// ---
// id: runtime.boot
// tool: adp.js
// section: runtime
// order: 320
// needs: [runtime.seed, runtime.switches, runtime.integrity, runtime.anchors, runtime.changes, runtime.classify]
// tests: [runtime-an-editor-seeds-an-empty-record, runtime-an-invalid-provider-fails-closed, runtime-config-set]
// sha: e76c166fec74
// ---
let tPlace = 0;
new MutationObserver(() => { cancelAnimationFrame(tPlace); tPlace = requestAnimationFrame(() => { placeThreads(); panels(); later(); }); })
  .observe(document.documentElement, {childList: true, subtree: true});
addEventListener('resize', () => { placeThreads(); later(); });
(async () => {
  let c;
  try { c = await connectHost(); }
  catch (e) { host = Object.freeze({protocol: 'adp-host/1', id: '', status: 'failed'}); pushErr('host connection failed: ' + (e && e.message || e)); return ready(); }
  attach(c);
  const d = c.db || null, u = c.user || null;
  canEdit = user.canEdit = u ? await safely(() => u.canEdit(), false).then(v => v === true) : false;
  user.id = u ? String(await safely(() => u.id(), '') || '') : '';
  user.can = n => isFn(u, 'can') ? safely(() => u.can(n), null) : Promise.resolve(null);
  if (d && canEdit && host.seedFiles) await seedFromFile(d);
  db = d;
  if (db) { changesPanel(); watchContent(); watchConfig(); } else ready();
  if (db && canEdit && host.seedFiles) {
    try { const r = await fetch('content.js', {cache: 'no-store'}); probe = (r.ok ? 'ok ' : 'http ') + r.status + ', ' + (r.headers.get('content-type') || '?') + ', ' + (await r.text()).length + ' chars'; }
    catch (e) { probe = 'failed: ' + (e && e.message || e); }
  }
  later();
})().catch(e => {
  db = null; canEdit = user.canEdit = false; user.can = () => Promise.resolve(null);
  host = Object.freeze({protocol: 'adp-host/1', id: host.id, status: 'failed'});
  pushErr('host initialization failed: ' + (e && e.message || e)); ready();
});
const handle = k => readyP.then(() => handles[k] || null).catch(() => null);
Object.defineProperties(ADP, Object.fromEntries(Object.entries({host: () => host, integrity: () => integrity, seeded: () => seeded, db: () => db})
  .map(([k, g]) => [k, {get: g, enumerable: true}])));
Object.freeze(Object.assign(ADP, {build: BUILD, page: cfg => { PAGE = cfg; later(); }, config, user,
  ns: name => { if (!db) throw new Error('ADP.ns needs a database'); const b = 'ns/' + name + '/'; return {doc: p => db.doc(b + p), collection: p => db.collection(b + p)}; },
  claude: name => readyP.then(() => host.id === 'claude' && isFn(window.claude, 'use') ? window.claude.use(name) : null).catch(() => null),
  agent: () => handle('agent'), publish: () => handle('publish'), ask: () => handle('ask')}));
```

## One runtime

`adp.js` is a catalog entry (`runtime.adp`): it opens with the header comment of the entry, the first lines of the file. The copy in a page, the copy in the catalog and the assembled `adp.js` are byte-identical; the catalog
check fails when they differ. Pages must not modify `adp.js`; a runtime change is a change to the catalog entry.

## Hashing and classifying in `adp.js`

The code blocks with a header are the fragments of `adp.js` this skill owns; [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) assembles
them after the host connection of [adp-minimal-hosts](../adp-minimal-hosts/SKILL.md).

`adp.js` computes the part hash of [adp-minimal-parts](../adp-minimal-parts/SKILL.md) so the page can hash itself at open.
`ADP.hash(text, files?)` returns a promise of `{parts: {id: hash, _rest: hash}, parents: {id: parent or ""}, page_hash, bad: [problems]}`, with
the same marker pattern, `norm`, 12-hex SHA-256 and page-hash lines as `adp.py manifest` on a single file; `files` (`{path: sha12}`) join the page
hash as `file:` lines. Three differences from `adp.py manifest`: the text outside every part is always `_rest` (a directory page has
`_rest:<path>` there); there is no `elements` field; and `parents` has no `_rest` entry. Problems carry no line number.

```js
// ---
// id: runtime.hash
// tool: adp.js
// section: runtime
// order: 200
// needs: [core.runtime]
// tests: [adp-js-hash-single, adp-js-hash-shell, adp-js-hash-problems]
// sha: c1cf5842e30b
// ---
const PART = '[a-z0-9][a-z0-9-]*(?:\\.[a-z0-9][a-z0-9-]*)*', REST = '_rest';
const MARK = new RegExp('(?:<!--|/\\*)\\s*(/?)part:(' + PART + ')\\s*(?:-->|\\*/)', 'g'), ID = new RegExp('^' + PART + '$');
const norm = s => s.replace(/\s+/g, ' ').trim();
async function H(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 12);
}
function markers(text) {               // -> {parts: {id: [start, end, parent]}, bad}
  const stack = [], parts = {}, bad = [], top = () => stack.length ? stack[stack.length - 1][0] : '';
  for (const m of text.matchAll(MARK)) {
    const pid = m[2];
    if (!m[1]) { if (parts[pid] || stack.some(x => x[0] === pid)) bad.push('part ' + pid + ' opened twice'); stack.push([pid, m.index + m[0].length]); }
    else if (top() !== pid) bad.push('/part:' + pid + ' closes ' + (top() || 'nothing'));
    else { const [, start] = stack.pop(); parts[pid] = [start, m.index, top()]; }
  }
  return {parts, bad: bad.concat(stack.map(x => 'part ' + x[0] + ' never closed'))};
}
function restOf(text, parts) {         // the text outside every top-level part, markers removed
  let out = '', i = 0;
  Object.values(parts).filter(p => p[2] === '').sort((a, b) => a[0] - b[0]).forEach(([s, e]) => { out += text.slice(i, s); i = e; });
  return (out + text.slice(i)).replace(MARK, '');
}
async function hashText(text, files) {
  const {parts, bad} = markers(text), hp = {}, parents = {};
  for (const id in parts) { hp[id] = await H(norm(text.slice(parts[id][0], parts[id][1]))); parents[id] = parts[id][2]; }
  hp[REST] = await H(norm(restOf(text, parts)));
  const lines = Object.keys(hp).map(k => k + '=' + hp[k]).sort().concat(Object.keys(files || {}).map(k => 'file:' + k + '=' + files[k]).sort());
  return {parts: hp, parents, page_hash: await H(lines.join('\n')), bad};
}
ADP.hash = hashText;
```

`ADP.classify(base, live, incoming)` is the classification of [adp-minimal-delta](../adp-minimal-delta/SKILL.md), line for line: the same
classes, the same closure over `parents` and `requires` merged from the three manifests, every list sorted by id.

```js
// ---
// id: runtime.classify
// tool: adp.js
// section: runtime
// order: 210
// needs: [core.runtime]
// tests: [classify-in-adp-js]
// sha: 365e766403bf
// ---
const CLASSES = ['new', 'ours', 'theirs', 'applied', 'held', 'retired'], has = (m, x) => Object.prototype.hasOwnProperty.call(m, x), own = (m, x) => has(m, x) ? m[x] : null;
function classifyId(b, l, i, retired) {
  if (b === null) return l === null ? (i === null ? null : 'new') : i === null ? 'theirs' : i === l ? 'applied' : 'held';
  if (i === null) return l === null ? 'applied' : retired ? 'retired' : 'held';
  if (l === b) return i === b ? null : 'ours';
  return i === b ? 'theirs' : i === l ? 'applied' : 'held';
}
function classify(base, live, incoming) {
  const ms = [base, live, incoming].map(m => m || {}), merged = k => Object.assign({}, ...ms.map(m => m[k]));
  const [B, L, I] = ms.map(m => ({...m.parts, ...m.files})), parents = merged('parents'), requires = merged('requires');
  const r = ms[2].retired || {}, retired = x => Array.isArray(r) ? r.includes(x) : has(r, x);
  const under = (f, p) => Object.entries(requires).some(([c, fs]) => (fs || []).includes(f) && (p === c || p.startsWith(c + '.')));
  const touches = (x, y) => own(parents, x) === y || own(parents, y) === x || under(x, y) || under(y, x);
  const ids = [...new Set([B, L, I].flatMap(Object.keys))].sort(), cls = {}, out = {};
  ids.forEach(x => { cls[x] = classifyId(own(B, x), own(L, x), own(I, x), retired(x)); });
  for (let moved = true; moved;) {
    moved = false;
    ids.forEach(x => { if (['new', 'ours', 'retired'].includes(cls[x]) && ids.some(y => cls[y] === 'held' && touches(x, y))) { cls[x] = 'held'; moved = true; } });
  }
  CLASSES.forEach(c => { out[c] = []; });
  ids.forEach(x => { if (cls[x]) out[cls[x]].push(cls[x] === 'held' ? {id: x, base: own(B, x), live: own(L, x), incoming: own(I, x)} : x); });
  return out;
}
ADP.classify = classify;
```

Fixtures and vectors: [vectors.md](vectors.md#contract-the-pure-section-of-adpjs). They hash the same file as `manifest-single` in
[adp-minimal-parts](../adp-minimal-parts/SKILL.md): their `parts` and `page_hash` equal that manifest's.

## Connecting, seeding and switches

Booted on a test host by the [runner](../adp-minimal-rebuild/SKILL.md#the-runner), the runtime does this:

| Situation | What it does |
|---|---|
| a valid `adp-host/1` provider | `ADP.host` = `{protocol, id, status: "connected", records, comments, seedFiles, agent, publish, ask}` |
| a provider with another protocol | `status: "failed"`, no records, nothing written; the page still renders statically |
| an editor opens a page whose store has no `manifest/current`, and the host serves files (`seedFiles`) | reads `seed.json`, fetches **every** pack before writing anything, writes each doc (six at a time), `manifest/current` alone and last, then `status/seed` (`{state: "done", from, version, by, opened_by, docs, packs, at}`), and sets `ADP.seeded` |
| a viewer opens it, or `manifest/current` exists, or the host does not serve files | writes nothing |
| a pack is missing | writes nothing; the first-open panel names the missing pack; the next editor's open tries again |
| `ADP.config.set(SWITCH, VALUE)` by an editor | checks the value against the switch's type, then `set config/current` (`schema: "adp-config/1", at, by, values, changed {SWITCH: {by, at}}`) and `set changes/d-<ms>` (`summary: "Set SWITCH = VALUE"`), unless `log.data-changes` is false; a value equal to the default is removed from `values` |
| a wrong value, an unknown switch, or a viewer | rejects with a message, writes nothing |

Content as data, the What changed panel, comment anchors, integrity and the self-check render into the DOM; they are specified above and not
covered by vectors.

Fixtures and vectors: [vectors.md](vectors.md#contract-connecting-seeding-and-switches).
