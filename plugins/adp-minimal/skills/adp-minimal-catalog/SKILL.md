---
name: adp-minimal-catalog
description: "Explains the ADP catalog and how to check its consistency: the folder, catalog.json (kit-catalog/2) entries, files, roles and hashes, the header every entry carries and its tags, adp_catalog.py (check, build, headers, drift, inventory) and what it fails on, My Own Kit in ~/.adp/catalog, take by reference, why a catalog changes by proposal. Use when the user asks what catalog.json holds, how headers work, how to verify a catalog, or how to fetch and take entries."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The catalog, and how to check that it is consistent

The catalog is a published artifact whose files are kit entries, plus an index. A page takes entries from it by reference.

```
catalog/
  catalog.json     the index (schema kit-catalog/2): url, ver, built, entries[]
  index.html       the catalog page: browse, preview, take
  adp.js           the runtime, byte-identical to the one pages get
  content.js parts/ styles/   the catalog page's own parts
  kit/             the building blocks ([kit](../adp-minimal-kit/SKILL.md))
```

## The index

Each entry in `catalog.json`:

```json
{ "id": "kit.tabs", "kind": "component", "group": "Board kit", "name": "Accessible tabs",
  "status": "new", "version": "0.1.0", "requires": [], "globals": [], "provides": ["Kit.tabs.mount"],
  "main": "kit/tabs.js",
  "files": [ {"path": "kit/tabs.js",  "role": "script", "sha256": "7ea8a15b...", "bytes": 7550},
             {"path": "kit/tabs.css", "role": "style",  "sha256": "a00b73f4...", "bytes": 2713} ],
  "hash": "a090ff09e829" }
```

`kind` is `component`, `theme`, `template` or `guide`; the **id prefix** (`kit`, `layout`, `pattern`, `viz`, `theme`, `runtime`, `template`, `guide`) is
what `kit list --kind` filters on. File roles: `script`, `style`, `sample`, `data`, `template`, `doc`. The entry `hash` is the first 12 hex of the SHA-256
of the sorted `path=sha256` lines. A theme also carries `fonts`, and some entries `extends`.

## The header

The index is **built from the headers**; nothing else writes it. Every entry describes itself in one comment at the top of its main file: a `/** ... */`
block in `.js` and `.css`, a `<!-- ... -->` block in `.txt` templates and `.md` guides. The first line is the name, the first paragraph the `about` text,
further paragraphs are notes, then the tags:

```
/**
 * Data table
 * A table from rows and columns inside its own scroll frame, with numeric columns and group rows.
 *
 * @id        kit.table
 * @kind      component
 * @group     Board kit
 * @status    new
 * @version   0.1.0
 * @updated   2026-10-25
 * @summary   A table in its own scroll frame with a sticky head and numeric columns.
 * @tags      table, data, numbers
 * @requires  none
 * @files     kit/table.css, kit/samples/kit.json
 * @provides  Kit.table.render, Kit.table.fmt
 * @config    Kit.table.render(box, opts) | columns [{key, label, num}], rows, group
 * @tokens    --panel --ink --rule
 * @globals   none
 * @db        none
 * @preview   {"render": "kit.table", "samples": ["kit/samples/kit.json#table"]}
 * @samples   table
 */
```

| Tag | Required | Value |
|---|---|---|
| `@id` `@kind` `@group` `@status` `@version` `@updated` `@summary` `@tags` `@requires` `@files` `@globals` `@db` | always | `@status` is `new` or `stable`; `@version` is `major.minor.patch`; `@summary` at most 260 characters; `@requires` and `@files` are `none` or comma lists |
| `@provides` | in a `.js` main file | `none` or dotted JS names (`Kit.table.render`) |
| `@tokens` | when the entry has a style file | custom properties; a trailing `?` marks an optional one (`--seam?`) |
| `@config` | optional, repeats | `signature \| what it takes` |
| `@preview`, `@samples` | optional | where and with what the catalog previews it; the bundle keys it owns |
| `@fonts`, `@extends`, `@related`, `@optional`, `@source`, `@changed` | optional | theme font URL; the entry it extends; related ids; origin; the newest change |

No other tag is allowed. The **main file** is the template or guide file, otherwise the first script, otherwise the first style.

## The consistency checks

The catalog tool is `scripts/adp_catalog.py`, beside `adp.py`, standard library only:

```sh
CAT="python3 -I <adp skill folder>/scripts/adp_catalog.py"
$CAT                 # every catalog check: sizes, hashes, orphans, headers, index freshness, runtime copy
$CAT build           # write catalog.json from the headers (the check fails while it is out of date)
$CAT headers [FILES] # validate headers only; --report counts conformance per kind and per rule, exits 0
$CAT drift           # header drift against the sources
$CAT inventory       # list what the catalog holds
```

What it fails on:

- an entry file whose recorded `sha256` or `bytes` differ from the file; a file on disk that no entry lists (an orphan); an entry listing a missing file;
- a main file without a valid header, an unknown tag, a missing required tag, an `@id` that is not the entry listing the file;
- an index that does not match what `build` would write from the headers;
- `adp.js` in the catalog differing from the runtime's copy byte for byte;
- samples: a `#key` the bundle lacks, a bundle not in the entry's own `@files`, an entry listing a bundle but naming no key of it, a bundle key that no entry
  names or owns;

The theme rules ([themes](../adp-minimal-themes/SKILL.md): the same token names, JSON and CSS agreeing, fonts) are checked by the repository's own test suite, next to
this tool.

A pre-commit hook runs the header check on staged catalog files, so a catalog file can only be committed once its header is complete.

## Using the catalog

```sh
$ADP catalog CATALOG_URL      # save the url; prints the read for catalog.json, then reads (<=256 paths each) for every file missing or changed
$ADP catalog                  # again, until it prints complete: true
$ADP suggest - --for "kanban board" --n 3
$ADP kit list - --kind viz --tag timeline
$ADP take - viz.timeline layout.topbar --url CATALOG_URL
```

**My Own Kit**: the user's whole catalog lives in `~/.adp/catalog/`; `adp.py setup` puts the shipped copy there first, so fetching afterwards lists only
what differs. `take` returns a `files` map `{path: {artifact: <catalog url>, path}}` for the publish call, the entries taken in dependency order, and a
`sha256` map. A catalog **is not edited by publishing over it**: a published catalog changes by proposal ([delta and inbox](../adp-minimal-delta/SKILL.md)), and a
local `catalog.json` is a build, not the live catalog, so `take` warns and you do not publish from it. Never download the whole catalog to publish a copy
of it; clone the catalog artifact, or plan the packed publish with `publish_catalog.py`. A Sites catalog is read over authenticated HTTPS and
materialized with hash verification (`take ... --materialize DIR`).

## Contract: a catalog tree, `adp_catalog.py build` and the check

A catalog is a folder with a `kit/` in it. This example is a whole one, small enough to read: a component with three samples, a visualisation that
requires it, a theme (tokens and its JSON) and a guide. Its tree:

```
catalog-a/
  kit/badge.js              kit.badge     main file (header), role script
  kit/badge.css                           role style
  kit/viz/meter.js          viz.meter     main file, @requires kit.badge
  kit/viz/meter.css
  kit/themes/paper.css      theme.paper   main file (a theme's main file is its stylesheet), @fonts
  kit/themes/paper.json                   role data
  kit/guides/reading.md     guide.reading main file, header in <!-- -->
  kit/samples/kit.json      bundle: key "badge" (owned by kit.badge) holds three samples: typical, warning, empty
  kit/samples/viz.json      bundle: key "meter" (owned by viz.meter) holds three: half, full, zero
  catalog.json              written by build, never by hand
```

| Command | Does | Prints | Exit |
|---|---|---|---|
| `adp_catalog.py build CATALOG_DIR` | reads every header under `kit/`, writes `catalog.json` (`kit-catalog/2`: `schema`, `url`, `ver`, `built`, `entries`); each entry's `files` are its main file then its `@files`, each `{path, role, sha256, bytes}`, and `hash` the first 12 hex of the SHA-256 of the sorted `path=sha256` lines | `wrote <path>: N entries, M files` (or `unchanged ...`) | 0; 1 with each problem on stderr and nothing written: a kit file no entry names, a `@requires` that names no entry, a header rule broken, a sample key nobody owns |
| `adp_catalog.py CATALOG_DIR` | the check: the index equals what build would write, every file's size and sha256 match, no orphans, every header valid | `OK: N entries, M entry files, F files in tree, 0 orphans, all sizes, sha256 and hashes match, H valid headers`; or `FAIL: N problem(s)` and one problem per line (a sha256 that differs, the entry `hash` on disk against the one built ...) | 0; 1 on any problem |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: a catalog tree, `adp_catalog.py build` and the check".

## Contract: reading a catalog (`kit`, `suggest`, `take`)

These read a `catalog.json`: the fetched live one (by its url, or `-` for the saved one), or a local build, which they accept with a warning on
stderr (`a local index is a build, not the live catalog ...`).

| Command | Prints | Exit |
|---|---|---|
| `kit list CATALOG [--kind K] [--tag T]` | one JSON line per entry: `{id, kind, name, summary, tags}` (`kind` is the first word of the id) | 0 |
| `kit show ID CATALOG` | `{id, name, summary, about, tags, files, requires, provides, status, version, config: [[signature, options]], db}` | 0; 1 for an unknown id |
| `kit describe ID CATALOG` | how to wire it: `{id, needs, optional, provides, requires, files (code only), sample, sample_key, db}` | 0 |
| `suggest CATALOG --for "words" [--n 3] [--kind K]` | `[{id, kind, why, requires, takes}]` ranked by overlap with tags, name, summary, id, provides, about; no model call | 0 |
| `take CATALOG ID ... --url URL` | `{catalog {url, index, live, ver, built, warning?}, entries (with every @requires, in load order), files {path: {artifact, path}}, sha256, samples}`: references, never copies | 0; 1 for an unknown id, or a local index without `--url` |

`take` resolves `@requires` first: taking `viz.meter` takes `kit.badge` too, and its `files` are the publish `files` entries a page adds.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: reading a catalog (`kit`, `suggest`, `take`)".

## Contract: My Own Kit (`catalog`)

`catalog URL` saves the user's catalog url in `ADP_HOME/config.json` and keeps its files in `ADP_HOME/catalog/`. It never fetches: it prints the reads.

| State of `ADP_HOME/catalog/` | `catalog [URL]` prints |
|---|---|
| no `catalog.json` | `{catalog, index, fetched: false, fetch: {the Artifact read of catalog.json into it, then}}` |
| `catalog.json`, files missing | `{catalog, index, fetched: true, ver, built, entries, refresh, kit, files, missing, complete: false, reads: [Artifact reads, at most 256 paths each]}` |
| every file the index lists | the same with `missing: 0`, `complete: true` and no reads |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: My Own Kit (`catalog`)".
