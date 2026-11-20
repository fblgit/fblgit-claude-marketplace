---
name: adp-minimal-runtime
description: "Reference for the ADP page shell and the adp.js runtime: the shell's markup contract and ADP.page(), content as data, the What changed panel, comment anchors, the integrity verdict, the checks/latest self-check, first-open seeding, switches in config/current (edit.locked, look.theme, look.mode), the public ADP API, and the adp.py dev shim. Use when the user asks what adp.js does in a page, how seeding works, what a switch is, or what ADP.* exposes to page code."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The shell and the runtime

The **shell** is the minimal `index.html` of an adp/2 page. The **runtime** is `adp.js`, a single script loaded before the page's own code.
Together they are the part of ADP that runs in the browser. All host I/O (records, comments, publishing) goes through the
[host adapter](../adp-minimal-hosts/SKILL.md).

## The shell

```html
<meta name="adp:build" content="12">
<link rel="stylesheet" href="kit/themes/default.css">
<link rel="stylesheet" href="styles/page.css">
<header data-part="page.header">
  ...
  <details id="wc" data-part="page.changes"> What changed panel: #wcN #wcChanges #wcDecisions #wcIncoming </details>
</header>
<nav data-part="page.tabs"> ... </nav>
<main id="views"></main>
<script src="content.js"></script>
<script src="adp.js"></script>
<script src="kit/dom.js"></script>   <!-- kit scripts added with `adp.py take`, dependencies first -->
<script src="parts/app.js"></script> <!-- the page's own code, last -->
```

The page contract:

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

After every publish, read `checks/latest`.

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
Step 3 narrows the race between two editors but does not close it; that is safe because seed writes are idempotent `set`s of the same data.
Read-only viewers never seed.

### Settings (switches)

A switch is one `group.name` value (`edit.locked`, `look.theme`, `look.mode`, `panel.changes`). `config/current` stores a value only when it
differs from the default, and records in `changed` who last changed each switch and when.
Groups: `edit`, `parts`, `comments`, `panel`, `playground`, `look`, `links`, `log`. `adp.py config` shows them; its `set` subcommand (a switch name, then the value) changes one.

`edit.locked` is advisory. The runtime shows a banner and disables controls marked `data-adp-edit`, and `adp.py hold` and `adp.py record` refuse
to run while it is on; changing switches from page code is not blocked. If `edit.locked` is true, do not write: tell the user who locked the page, from
`changed["edit.locked"].by` in `config/current`.

```js
ADP.config.get('look.mode');                    // 'auto', 'light' or 'dark'
ADP.config.on('look.mode', v => applyMode(v));
await ADP.config.set('panel.changes', 'off');   // 'everyone', 'editors' or 'off'
```

## The public API

| Member | What it is |
|---|---|
| `ADP.build` | The `adp:build` number, as a string. |
| `ADP.content(id)` | The current HTML of a part ([Content as data](#what-the-runtime-does)). |
| `ADP.page(cfg)` | Registers the page ([The shell](#the-shell)). |
| `ADP.config` | The switches: `get`, `on`, `set`, `reset`, `all`, `define`, the `ready` promise and the `doc` getter. |
| `ADP.user` | `canEdit`, `id`, and `can(name)`: a promise of the host's answer for a named right, or `null`. |
| `ADP.host` | The connection: `protocol`, `id`, `status`, and booleans for `records`, `comments`, `seedFiles`, `agent`, `publish`, `ask`. |
| `ADP.agent()`, `ADP.publish()`, `ADP.ask()` | Each returns a promise of the host's handle, or `null` when the host has none. |
| `ADP.claude(name)` | A promise of `window.claude.use(name)` when the connected host is Claude, else `null`. |
| `ADP.ns(name)` | `doc` and `collection` scoped to `ns/<name>/`; throws when there is no database. |
| `ADP.classify(base, live, incoming)` | The three-way classification ([contract](#contract-the-pure-section-of-adpjs)). |
| `ADP.hash(text, files?)` | The part hash ([contract](#contract-the-pure-section-of-adpjs)). |
| `ADP.integrity`, `ADP.seeded`, `ADP.db` | Getters: the integrity result, the seed record, the database handle (`null` when there is none). |

Components must use this API and must not access `window.claude` directly ([host adapters](../adp-minimal-hosts/SKILL.md)).

## One runtime

`adp.js` is a catalog entry (`runtime.adp`). The copy in a page, the copy in the catalog and the copy in the skill are byte-identical; the catalog
check fails when they differ. Pages must not modify `adp.js`; a runtime change is a change to the catalog entry.

## The dev shim

`adp.py dev serve` serves a page locally with a stand-in for the claude.ai viewer's `window.claude` (`db`, `user`, `comments`,
`artifact.publish`). It reproduces the host's observable behavior: `update` merges into an existing document, a publish whose `ifMatch` no
longer matches the file is rejected with `conflict`, and `adp.py dev send` applies ArtifactData batches all or nothing, refusing a
[pinned write](../adp-minimal-protocol/SKILL.md) whose `if_version` is stale. The shim's user can always edit. Passing under the shim does not
guarantee the page works on claude.ai; verify on the live host.

## Contract: the pure section of `adp.js`

`adp.js` reimplements the part hash of `adp.py` so the page can hash itself at open. A conforming implementation must expose, on `window.ADP`:

- `ADP.hash(text, files?)` → a promise of `{parts: {id: hash, _rest: hash}, parents: {id: parent or ""}, page_hash, bad: [problems]}`. It uses
  the same marker pattern, whitespace normalization (`norm`), 12-hex SHA-256 (`crypto.subtle`) and page-hash lines as `adp.py manifest` on a
  single file; `files` (`{path: sha12}`) are added to the page hash as `file:` lines. It differs from `adp.py manifest` in three ways: the text
  outside every part is always the key `_rest` (for a directory page `adp.py` uses `_rest:<path>`); there is no `elements` field; and `parents`
  has no `_rest` entry (`adp.py` lists it with parent `""`).
- `ADP.classify(base, live, incoming)` → the classification of [adp-minimal-delta](../adp-minimal-delta/SKILL.md), vector `classify-in-adp-js`.

The vectors for this contract hash the same file as `manifest-single` in [adp-minimal-parts](../adp-minimal-parts/SKILL.md): their `parts` and
`page_hash` must equal that manifest's.

Fixtures and vectors: [vectors.md](vectors.md#contract-the-pure-section-of-adpjs).

## Contract: connecting, seeding and switches

Booted on a test host by the [runner](../adp-minimal-rebuild/SKILL.md#the-runner), the runtime must:

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
