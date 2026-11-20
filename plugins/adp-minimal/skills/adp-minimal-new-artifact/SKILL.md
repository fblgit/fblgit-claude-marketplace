---
name: adp-minimal-new-artifact
description: "Explains how a new ADP artifact is created and why: adp.py new, the adp/2 file tree (index.html shell, adp.js, content.js, parts/, styles/, seed.json, seed/), why not a single file, tiers and templates (starter, assistant, default), copy as data, check, publish, first-open seeding, what the artifact service serves. Use when the user asks how to start a new ADP page, what its files are for, or which tier to pick."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# How a new artifact is created, and its shape

A new artifact is never a single hand-written `index.html`. It is created by `adp.py new`, which lays the page out as **adp/2** and prints the one
publish call that goes with it.

## Why not one file

A single file cannot give per-file hashes, copy as data, or part-id comment anchors. The platform already keeps a hash per file, a database per
page and an anchor per element; adp/2 uses those units instead of rebuilding them inside one document. Concretely:

- a change touches only the file that holds it, so a publish sends only that file and a diff points at it;
- copy lives in the database, so a wording fix is a data write, not a publish;
- the shell is small enough that the shell itself almost never conflicts.

## The file tree

`adp.py new` writes this into a folder (DIR), at the paths it is published under:

```
DIR/
  index.html        the thin shell: header, What changed panel, tabs, an empty <main id="views">, script tags
  adp.js            the runtime (always the catalog's copy, byte for byte)
  content.js        window.ADP_CONTENT = {<part id>: {part, title, html}}: the baseline copy of every part
  parts/app.js      the page's code, one file per part family
  styles/page.css   the page's styles (the assistant tier adds styles/assist.css, canvas.css)
  seed.json         the first database documents, indexed ...
  seed/pack-001.json  ... and packed (never part of the manifest)
```

Kit files (`kit/...`) are **not** copied into DIR. A template's `take` list names catalog entries; `new` puts them in the publish call as
by-reference entries, and the server copies them across. They are the catalog's files, not yours, so they are not in the manifest.

## Tiers and templates

| Start | Command | You get |
|---|---|---|
| minimal | `adp.py new --tier minimal DIR` (= `new starter DIR`) | blank page, welcome view, settings view, `theme.default`, the What changed panel |
| assistant | `adp.py new assistant DIR --theme default --catalog CATALOG` | the starter plus the Work-with-Claude pane, requests, presence, the canvas and every catalog theme with a switch |
| default | `adp.py new --tier default DIR` | the assistant plus 3D and the common kits |

Templates stack: `default` is based on `assistant`, which is based on `starter`; each layer overrides files of the same name. Files in a template carry
a `.txt` suffix, which `new` drops (`index.html.txt` becomes `index.html`). `{{title}}` and `{{slug}}` are filled in everywhere except `adp.js`.

Default to the assistant when people and Claude use the page together. `--theme NAME` and `--layout ID` add a theme and layouts from the catalog;
`--data FILE|DIR` seeds the page's own records; `--content FILE` builds starter views from a content file.

## The shape of a part

Every view and its main sections are parts, in the markers of [parts and hashes](../adp-minimal-parts/SKILL.md). Copy is a `content/<part id>` document with an
`html` field, and `content.js` carries the same copy as the fallback when the database is unavailable; the database overrides it live. The page's code
repaints `[data-part]` elements when `content/` changes.

```js
// content.js
window.ADP_CONTENT = {
  "home.lead": {"part": "home.lead", "title": "Lead", "html": "<p>What this page is for.</p>"}
};
```

`content.js` is parsed as strict JSON by the tooling: leave no trailing commas.

## Create, check, publish, seed

```sh
ADP="python3 -I <adp skill folder>/scripts/adp.py"
$ADP new assistant DIR --title "Release board" --by my-session --theme default --catalog CATALOG
# change the look and copy: styles/page.css, parts/*.js, content.js (keep the token names, the markers, the selectors adp.js relies on)
$ADP check DIR                 # markers balance, ids valid and unique, every part has data-part
# publish with the object `new` printed (file_path, root, files, capabilities), plus a label and, the first time, an icon
```

- Two pages must not ship looking the same: write your own `styles/page.css` and views, keep the structure.
- Over 250 files the `files` map becomes `batches`: publish the page with the first and send the rest to the same URL.
- **Seeding.** The first editor to open the published page writes the record into its own database from `seed.json` and `seed/`; no agent runs
  batches for it. Until then there is no `manifest/current`, and the edit road cannot hold or record. Check with an ArtifactData `get` of
  `manifest/current` first: if it exists, write nothing. Only when nobody can open the page as an editor, `adp.py seed DIR --by NAME --batches`
  prints the same documents as batches. Details: [shell and runtime](../adp-minimal-runtime/SKILL.md).

## What gets served

The artifact service serves a fixed set of extensions (`.html .css .js .mjs .json .wasm .map .txt .md .csv .xml .svg`, common images, fonts, audio,
video and `.pdf`). `adp.py files DIR` maps every such file to itself and lists the rest under `skipped`; keep templates and other unserved files with a
`.txt` suffix and read them back without it.

## The page's own code

The page's script reaches the database through the runtime, not the host: `ADP.ns('shared').doc('board/main')` and `.collection('cards')` give handles
under `ns/shared/`; `ADP.ns('users/<id>')` is per person. A handle has `get`, `set`, `update`, `delete` and `onSnapshot`. `ADP.config.get('look.mode')`
reads a switch.

```js
const board = ADP.ns('shared').doc('board/main');
board.onSnapshot(s => render(s.exists ? s.data() : {cards: []}));
await board.update({title: 'Sprint 12'});
```

## Rules

- Part ids never change after publishing; add a new id instead.
- Never build by hand a part that a catalog entry already is: take it ([catalog](../adp-minimal-catalog/SKILL.md)).
- Hand the user the link and what to do next.

## Contract: `new`

`new` copies a **template folder** (shipped with the full plugin, with the catalog: not part of this plugin) into DIR, fills its title and slug,
writes the seed, and prints one publish object. The vectors pin what a rebuilt `new` must do with the starter template: the output, the file tree
the publish names, a tree that passes `check`, and the refusal of a non-empty DIR. They were taken with the starter template of ADP 2.2.0 (its part count and sizes show in `check` and `seed`): run them
with that template, not another.

| Command | Prints | Exit |
|---|---|---|
| `templates` | one block per template: name, what it is, `use when:` | 0 |
| `new (TEMPLATE \| --tier minimal\|default) DIR [--title T] [--slug S] [--by NAME] [--content FILE] [--data ...] [--theme NAME] [--layout ID] [--catalog C]` | `{template, dir, title, slug, publish {file_path, root, files, capabilities}, take, design, next, ...}` | 0; 1 when DIR exists and is not empty; 2 `{error: "take failed", ...}` when a catalog is given that cannot be taken from |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `new`".
