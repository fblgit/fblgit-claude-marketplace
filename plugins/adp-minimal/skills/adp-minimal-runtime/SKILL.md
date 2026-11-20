---
name: adp-minimal-runtime
description: "Explains the ADP shell and the adp.js runtime: the shell's markup contract and ADP.page({view, expected, titles, legacy, all, reveal}), content as data, the What changed panel, comment anchors, the integrity verdict, the checks/latest self-check, first-open seeding, switches in config/current (edit.locked, look.theme), the public ADP surface, and the dev shim. Use when the user asks what adp.js does in the page, how seeding works, what a switch is, or what ADP.* offers page code."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The shell and the runtime

The runtime is what every ADP page shares in the browser: it keeps the page's record, seeds it on first open, shows what changed, and carries the host connection that the agent pane and the kits use.

The **shell** is the thin `index.html` of an adp/2 page. The **runtime** is `adp.js`, one script loaded before the page's own. Together they are the
part of ADP that lives in the page; they talk to the world only through the [host adapter](../adp-minimal-hosts/SKILL.md).

## The shell

```html
<meta name="adp:build" content="12">
<link rel="stylesheet" href="kit/themes/default.css">
<link rel="stylesheet" href="styles/page.css">
<header data-part="page.header"> ... <div id="wc"> What changed panel: #wcChanges #wcDecisions #wcIncoming </div></header>
<nav data-part="page.tabs"> ... </nav>
<main id="views"></main>
<script src="content.js"></script>
<script src="adp.js"></script>
<script src="kit/dom.js"></script>   <!-- taken kit scripts, requires first -->
<script src="parts/app.js"></script> <!-- the page's code, last -->
```

The page contract: `adp:build` and `window.ADP_CONTENT` load before the runtime; the parts `page.header`, `page.tabs` and `page.changes` exist; once
the views exist the page calls the runtime once:

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
| **Content as data** | `ADP.content(id)` returns `content/<id>.html` from the database, else from `ADP_CONTENT`; a live subscription repaints every `[data-part="<id>"]` when it changes. |
| **What changed** | Fills the panel from `changes/` (newest ten), active `decisions/`, and an Incoming list from `incoming/`. |
| **Comment anchors** | Registers part-id anchors: a click in comment mode composes on the nearest `[data-part]`; threads are placed on the matching element. |
| **Integrity at open** | Hashes the page, reads `manifest/current` and writes a verdict to `status/integrity`: `consistent`, `files_ahead`, `record_ahead` or `mixed`. |
| **Self-check** | After load, for an editor, writes `checks/latest`: missing parts, unmarked `[data-part]`, horizontal overflow, errors, anchor counts. Read it after every publish. |
| **Seeding** | On the first open by an editor with no `manifest/current`, expands `seed.json` and `seed/pack-*.json` into the database, `manifest/current` last (below). |
| **Settings** | `ADP.config` carries the switches in `config/current`. |

### Seeding

An agent publishes the page once, with `seed.json` and `seed/` beside it. The first editor to open it:

1. stops if `manifest/current` exists (already seeded);
2. fetches `seed.json` (schema `adp-seed/2`) and every pack in `packs`, before writing anything;
3. checks `manifest/current` again (another editor may have won);
4. writes the documents six at a time, with progress in `status/seed`;
5. writes `manifest/current` last, then `status/seed` `done`.

Because `manifest/current` is what agents read first and what step 1 tests, a run that stops halfway leaves no manifest and the next editor starts
again. Setting a document twice is harmless. A viewer who cannot edit never seeds.

### Settings (switches)

A switch is one `group.name` value (`edit.locked`, `look.theme`, `panel.changes`), stored in `config/current` only when it differs from the default.
Groups: `edit`, `parts`, `comments`, `panel`, `playground`, `look`, `links`, `log`. `adp.py config` shows them; its `set` subcommand (a switch name, then the value) changes one.
If `edit.locked` is true, stop and tell the user who locked it.

```js
ADP.config.get('look.mode');
ADP.config.on('look.mode', v => applyMode(v));
await ADP.config.set('panel.changes', false);
```

## The public surface

`ADP.build`, `ADP.content(id)`, `ADP.page(cfg)`, `ADP.config`, `ADP.user` (`canEdit`, `id`, `can(name)`), `ADP.host` (which of `records`, `comments`,
`seedFiles`, `agent`, `publish`, `ask` exist), the handles `ADP.agent()`, `ADP.publish()`, `ADP.ask()` (promises of a handle or `null`), `ADP.ns(name)`,
`ADP.classify(base, live, incoming)`, `ADP.hash(text, files)`, and the getters `ADP.integrity`, `ADP.seeded`, `ADP.db`. Components take what they need from
this surface; they never reach for `window.claude` themselves ([host adapters](../adp-minimal-hosts/SKILL.md)).

## One runtime

`adp.js` is a catalog entry (`runtime.adp`). The copy in a page, the copy in the catalog and the copy in the skill are byte-identical; the catalog
check fails when they differ. A page never carries a modified runtime: a change to the runtime is a change to the catalog entry.

## The dev shim

`adp.py dev` serves a page offline with a stand-in for the claude.ai viewer (`window.claude`: `db`, `user`, `comments`, `publish`) that follows the
host's observable behaviour: pinned writes, merge-style `update`, a stale `ifMatch` publish rejected as `conflict`. It lets a page and its tests run
without a host. It is a stand-in, not the host: a live check still decides whether a page works there.

## Contract: the pure section of `adp.js`

`adp.js` re-implements the part hash of `adp.py` so the page can hash itself at open. A rebuilt runtime must expose, on `window.ADP`:

- `ADP.hash(text, files?)` → a promise of `{parts: {id: hash, _rest: hash}, parents: {id: parent or ""}, page_hash, bad: [problems]}`. Same marker
  pattern, `norm`, 12-hex SHA-256 (`crypto.subtle`), `_rest` (named just `_rest`, also in a DIR page) and page-hash lines as `adp.py manifest` on one
  file; `files {path: sha12}` join the page hash as `file:` lines. It does not count `elements`, and its `parents` leave out `_rest` (`adp.py`
  lists `_rest` with parent `""`).
- `ADP.classify(base, live, incoming)` → the classification of [adp-minimal-delta](../adp-minimal-delta/SKILL.md), vector `classify-in-adp-js`.

The vectors below hash the same file as `manifest-single` in [adp-minimal-parts](../adp-minimal-parts/SKILL.md): the parts and `page_hash` must equal
that manifest's.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: the pure section of `adp.js`".

## Contract: connecting, seeding and switches

Booted on a test host (the runner's `boot` and `config-set`), the runtime must:

| Situation | What it does |
|---|---|
| a valid `adp-host/1` provider | `ADP.host` = `{protocol, id, status: "connected", records, comments, seedFiles, agent, publish, ask}` |
| a provider with another protocol | `status: "failed"`, no records, nothing written; the page still renders statically |
| an editor opens a page whose store has no `manifest/current`, and the host serves files (`seedFiles`) | reads `seed.json`, fetches **every** pack before writing anything, writes each doc (six at a time), `manifest/current` alone and last, then `status/seed` (`{state: "done", from, version, by, opened_by, docs, packs, at}`), also `ADP.seeded` |
| a viewer opens it, or `manifest/current` exists, or the host does not serve files | writes nothing |
| a pack is missing | writes nothing (the tour shows why); the next editor's open tries again |
| `ADP.config.set(SWITCH, VALUE)` by an editor | checks the value against the switch's type, then `set config/current` (`schema: "adp-config/1", at, by, values, changed {SWITCH: {by, at}}`) and `set changes/d-<ms>` (`summary: "Set SWITCH = VALUE"`), unless `log.data-changes` is false; a value equal to the default is removed from `values` |
| a wrong value, an unknown switch, or a viewer | rejects with a message, writes nothing |

Content as data, the What changed panel, anchors, integrity and the self-check draw into the DOM: they are described above, not proven by vectors.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: connecting, seeding and switches".
