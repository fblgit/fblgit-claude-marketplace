---
name: adp-minimal-new-artifact
description: "Explains how a new ADP artifact is created and why: adp.py new, the adp/2 file tree (index.html shell, adp.js, content.js, parts/, styles/, seed.json, seed/), why not a single file, templates (the minimal template this plugin ships, how templates stack, tiers), copy as data, check, publish, first-open seeding, what the artifact service serves. Use when the user asks how to start a new ADP page, what its files are for, or which template to start from."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Creating a new artifact

Run `adp.py new` rather than hand-writing a single `index.html`. It lays the page out as **adp/2** from a template, takes its kit entries from the
catalog, and prints the publish call for it. `adp.py` is built from this specification ([rebuild](../adp-minimal-rebuild/SKILL.md)).

## Why not one file

The artifact service already keeps a hash per file, a database per page and an anchor per element. adp/2 uses those units instead of rebuilding
them inside one document:

- a change touches only the file that holds it, so a publish sends only that file and a diff points at it;
- copy (the page's text content) lives in the database, so a wording fix is a data write, not a publish;
- the shell rarely changes, so concurrent publishes rarely conflict on it.

## The file tree

`adp.py new` writes this into a folder (DIR), at the paths it is published under:

```
DIR/
  index.html          the thin shell: header, "What changed" panel, tabs, an empty <main id="views">, script tags
  adp.js              the runtime, copied byte for byte
  content.js          window.ADP_CONTENT = {<part id>: {part, title, html}}: the baseline copy of every part
  parts/app.js        the page's code, one file per part family
  styles/page.css     the page's styles
  seed.json           index of the initial database documents
  seed/pack-001.json  the packed document bodies (excluded from the manifest)
```

Kit files (`kit/...`) are **not** copied into DIR. A template's `take` list names catalog entries. When a catalog is available, `new` adds them to
the publish call as by-reference entries and the artifact service copies them server-side; otherwise `new` prints the `take` step to run before
publishing. Kit files belong to the catalog, so they are excluded from the manifest.

## Templates

A template is a folder `templates/<name>/` beside `adp.py`: a `template.json` (`name`, `summary`, `use_when`, `design`, `capabilities`, `take`, and
optionally `base`, `drop` and `installed`) and the page's files. A template with a `base` starts from that template's files and overrides files of
the same name. A template file whose name has another extension before `.txt` is written without the `.txt` (`index.html.txt` becomes
`index.html`). `{{title}}`, `{{slug}}` and `{{catalog}}` are substituted in every file except `adp.js`, which is copied byte for byte.

This specification ships one template, **`minimal`**, as the fixture `template-minimal` in [vectors.md](vectors.md): the shell, its copy as data,
and a status list of what the runtime found on the host (connection, viewer, capabilities, integrity, seeding). It takes nothing from the catalog,
so a page built from it works with `adp.js` alone. Install it as `templates/minimal/` and start with `adp.py new minimal DIR`.

`--tier minimal` and `--tier default` select the `starter` and `default` templates where a catalog installs them; `--tier full` is refused.
`--theme NAME` (default `theme.default`) and `--layout ID` add a theme and layouts from the catalog; `--catalog` falls back to the catalog saved by
`adp.py catalog`. `--data FILE|DIR` seeds the page's own records; `--content FILE` builds views from a content file (`starter` template only).

## The shape of a part

Every view and its main sections are parts, in the markers of [parts and hashes](../adp-minimal-parts/SKILL.md). A part's copy is a
`content/<part id>` document with an `html` field. `content.js` carries the same copy as the fallback when the database is unavailable; the database
overrides it live, and the page's code repaints `[data-part]` elements when `content/` changes.

```js
// content.js
window.ADP_CONTENT = {
  "home.lead": {"part": "home.lead", "title": "Lead", "html": "<p>What this page is for.</p>"}
};
```

The tooling parses the object literal after `window.ADP_CONTENT =` as strict JSON: double-quoted keys, no trailing commas, no comments, and a
closing `;`.

## Create, check, publish, seed

```sh
ADP="python3 -I adp.py"
$ADP new minimal DIR --title "Release board" --by NAME
# adapt the look and copy: styles/page.css, parts/*.js, content.js (keep the token names, the markers and the selectors adp.js relies on)
$ADP check DIR                 # markers balance, ids valid and unique, every part has data-part
# publish with the object `new` printed (file_path, root, files, capabilities), plus a label and, the first time, an icon
```

`--by NAME` is recorded as the author of the seeded documents.

- Give each page its own `styles/page.css` and views; keep the structure.
- `adp.py files DIR` emits `batches` instead of `files` above 250 files: publish the page with the first batch, then send the rest to the same URL.
- **Seeding.** The first editor to open the published page writes the record into its database from `seed.json` and `seed/`, so no manual batch
  writes are needed. Until then there are no `parts/<id>` documents to [hold](../adp-minimal-protocol/SKILL.md) and no `manifest/current` to
  record against, so the [edit road](../adp-minimal-roads/SKILL.md) cannot start. Check with an ArtifactData `get` of `manifest/current` first: if
  it exists, write nothing. Only when nobody can open the page as an editor, `adp.py seed DIR --by NAME --batches` prints the same documents as
  batches. Details: [shell and runtime](../adp-minimal-runtime/SKILL.md).
- After publishing, give the user the URL and the next steps.

## What gets served

The artifact service serves a fixed set of extensions (`.html .css .js .mjs .json .geojson .webmanifest .wasm .map .txt .md .csv .xml .svg`,
common images, fonts, audio, video and `.pdf`); a publish that includes any other file is refused. `adp.py files DIR` maps every servable file to
itself and lists the rest under `skipped`. Store templates and other unserved files with a `.txt` suffix.

## The page's own code

The page's script reaches the database through the runtime, not the host: `ADP.ns('shared').doc('board/main')` and `.collection('cards')` give
handles under `ns/shared/`; `ADP.ns('users/<id>')` is per person. A handle has `get`, `set`, `update`, `delete` and `onSnapshot`.
`ADP.config.get('look.mode')` reads a [switch](../adp-minimal-runtime/SKILL.md) (a named page setting in `config/current`).

```js
const board = ADP.ns('shared').doc('board/main');
board.onSnapshot(s => render(s.exists ? s.data() : {cards: []}));
await board.update({title: 'Sprint 12'});
```

## Rules

- Part ids never change after publishing; add a new id instead.
- If the catalog already provides a part, take it instead of writing it ([catalog](../adp-minimal-catalog/SKILL.md)).

## Contract: `new`

`new` copies a template folder into DIR, fills in its title and slug, writes the seed, and prints one publish object. The vectors run it on the
`minimal` template (fixture `template-minimal`, installed as the only template): the output, the file tree the publish names, a tree that passes
`check`, the seed it writes, and the refusal of a non-empty DIR. Part counts and sizes in the `check` and `seed` output depend on that template.

| Command | Prints | Exit |
|---|---|---|
| `templates` | one block per template: name, what it is, `use when:` | 0 |
| `new (TEMPLATE \| --tier minimal\|default) DIR [--title T] [--slug S] [--by NAME] [--content FILE] [--data FILE\|DIR] [--theme NAME] [--layout ID] [--catalog URL\|-\|catalog.json]` | `{template, dir, title, slug, publish {file_path, root, files, capabilities}, take, design, next, ...}` | 0; 1 when DIR exists and is not empty; 2 `{error: "take failed", ...}` when a catalog is given that cannot be taken from |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `new`".
