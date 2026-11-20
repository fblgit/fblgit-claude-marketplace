---
name: adp-minimal-catalog
description: "Reference for the ADP catalog: the catalog folder, catalog.json (kit-catalog/2) entries with their files, roles and hashes, the header each entry's main file carries and its tags, adp_catalog.py (check, build, headers, drift, inventory) and what it fails on, My Own Kit (the user's local copy of the catalog in ~/.adp/catalog), reading entries with kit, suggest and take, and why a published catalog changes by proposal. Use when the user asks what catalog.json holds, how headers work, how to verify a catalog, or how to fetch and take entries."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Catalog: format and consistency checks

The catalog is a published artifact that holds ADP's reusable kit entries and their index, `catalog.json`. Pages reference catalog files; they never copy them.

```
catalog/
  catalog.json     the index (schema kit-catalog/2): url, ver, built, entries[]
  index.html       the catalog page: browse, preview, take
  adp.js           the runtime, byte-identical to the one pages get
  content.js parts/ styles/   the catalog page's own parts
  kit/             the building blocks ([kit](../adp-minimal-kit/SKILL.md))
```

## The index

Each entry in `catalog.json`; this is `kit.badge` as `build` writes it from the fixture `catalog-a` ([vectors](vectors.md)):

```json
{ "id": "kit.badge", "kind": "component", "group": "Board kit", "name": "Status badge",
  "summary": "A small label coloured by a meaning token.", "tags": ["badge", "status", "label"],
  "status": "new", "version": "0.1.0", "requires": [], "globals": [], "provides": ["Kit.badge.render"],
  "main": "kit/badge.js",
  "files": [ {"path": "kit/badge.js",         "role": "script", "sha256": "18ba1a86...", "bytes": 1024},
             {"path": "kit/badge.css",        "role": "style",  "sha256": "e36fc8a4...", "bytes": 264},
             {"path": "kit/samples/kit.json", "role": "sample", "sha256": "754630b8...", "bytes": 230} ],
  "hash": "04fb713a8c9d" }
```

`kind` is `component`, `theme`, `template` or `guide`. The **id prefix** (`kit`, `layout`, `pattern`, `viz`, `theme`, `runtime`, `template`, `guide`) is a
separate classification. `kit list` and `suggest` report the id prefix in their `kind` output field, and their `--kind` filter matches it (`kit list --kind`
also accepts a `kind` value). File roles: `script`, `style`, `sample`, `data`, `template`, `doc`. The entry `hash` is the first 12 hex of the SHA-256
of the sorted `path=sha256` lines. A theme also carries `fonts`, and some entries `extends`.

## The header

The index is **built from the headers**; nothing else writes it. Every entry describes itself in one comment at the top of its main file, after the
opening part marker: a `/** ... */` block in `.js` and `.css`, a `<!-- ... -->` block in `.txt` templates and `.md` guides. The first line is the
name, the next line or paragraph the `about` text, further paragraphs are notes, then the tags. The header of `kit/badge.js` in `catalog-a`:

```
/* part:page.script.kit.badge */
/**
 * Status badge
 * Kit.badge.render(el, {label, tone}) draws a small label coloured by a meaning token; an empty label draws nothing.
 *
 * @id        kit.badge
 * @kind      component
 * @group     Board kit
 * @status    new
 * @version   0.1.0
 * @updated   2026-11-20
 * @summary   A small label coloured by a meaning token.
 * @tags      badge, status, label
 * @requires  none
 * @files     kit/badge.css, kit/samples/kit.json
 * @provides  Kit.badge.render
 * @config    Kit.badge.render(el, opts) | label, tone (ok warn danger)
 * @tokens    --ok --warn --danger --f-ui
 * @globals   none
 * @db        none
 * @preview   {"render": "kit.badge", "samples": ["kit/samples/kit.json#badge"]}
 * @samples   badge
 */
```

| Tag | Required | Value |
|---|---|---|
| `@id` `@kind` `@group` `@status` `@version` `@updated` `@summary` `@tags` `@requires` `@files` `@globals` `@db` | always | `@status` is `new` or `stable`; `@version` is `major.minor.patch`; `@summary` at most 260 characters; `@requires` and `@files` are `none` or comma lists |
| `@provides` | in a `.js` main file | `none` or dotted JS names (`Kit.badge.render`) |
| `@tokens` | when the entry has a style file | custom properties; a trailing `?` marks an optional one (`--seam?`) |
| `@config` | optional, repeats | `signature \| what it takes` |
| `@preview` | optional | the renderer and sample references the catalog page previews the entry with |
| `@samples` | optional | the sample-bundle keys this entry owns |
| `@fonts` | optional | a theme's font stylesheet URL |
| `@extends` | optional | the entry this one extends |
| `@related` | optional | ids of related entries |
| `@optional` | optional | ids of entries this one can work with but does not require; `take` does not pull them in |
| `@source` | optional, repeats | where the entry came from |
| `@changed` | optional, at most once | the most recent change |

No other tag is allowed. The **main file** is the template or guide file, otherwise the first script, otherwise the first style.

## The consistency checks

The catalog tool is `scripts/adp_catalog.py`, beside `adp.py`, standard library only:

```sh
CAT="python3 -I adp_catalog.py"
$CAT                 # every catalog check: sizes, hashes, orphans, headers, index freshness, runtime copy
$CAT build           # write catalog.json from the headers (the check fails while it is out of date)
$CAT headers [FILES] # validate headers only; --report counts conformance per kind and per rule, exits 0
$CAT drift           # read-only report of where an entry's header disagrees with catalog.json
$CAT inventory       # list what the catalog holds
```

What it fails on:

- an entry file whose recorded `sha256` or `bytes` differ from the file; a file on disk that no entry lists (an orphan); an entry listing a missing file;
- a main file without a valid header, an unknown tag, a missing required tag, an `@id` that differs from the id of the entry that lists the file;
- an index that does not match what `build` would write from the headers;
- more than 256 entries (their main files must fit one Artifact read);
- `adp.js` in the catalog differing from the runtime's copy byte for byte;
- samples: a `#key` the bundle lacks, a bundle not in the entry's own `@files`, an entry listing a bundle but naming no key of it, a bundle key that no entry
  names or owns.

`adp_catalog.py` does not check the theme rules ([themes](../adp-minimal-themes/SKILL.md): the same token names, JSON and CSS agreeing, fonts);
check them by hand when a theme is added or changed. Run `adp_catalog.py headers` on every changed main file and the full check before any
catalog change is proposed.

## Using the catalog

```sh
ADP="python3 -I adp.py"
$ADP catalog CATALOG_URL      # save the url; print the Artifact read call for catalog.json, then read calls (up to 256 paths each) for missing or changed files
$ADP catalog                  # make those reads, then run again until it prints complete: true
$ADP suggest - --for "progress bar" --n 3
$ADP kit list - --kind viz --tag meter
$ADP take - viz.meter --url CATALOG_URL
```

**My Own Kit** is the user's local copy of their catalog, in `~/.adp/catalog/` (`$ADP_HOME/catalog/`; a Sites catalog goes to
`~/.adp/catalogs/<host>/`). `catalog` prints the reads that copy into it only the files that are missing or changed, and `kit`, `suggest` and
`take` read from it. `take` returns a `files` map `{path: {artifact: <catalog url>, path}}` for the publish call, the entries taken
in dependency order, and a `sha256` map. A catalog **is not edited by publishing over it**: a published catalog changes by proposal
([delta and inbox](../adp-minimal-delta/SKILL.md)). A local `catalog.json` is a build, not the live catalog; `take` warns when given one, and you must not
publish from it. Never download the whole catalog to publish a copy of it: clone the catalog artifact instead. A catalog on ChatGPT Sites ([hosts](../adp-minimal-hosts/SKILL.md)) is read over
authenticated HTTPS and materialized with hash verification (`take ... --materialize DIR`).

## Contract: a catalog tree, `adp_catalog.py build` and the check

A catalog is a folder with a `kit/` in it. A minimal complete example: a component with three samples, a visualization that requires it, a theme (tokens
and its JSON) and a guide. Its tree:

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
| `adp_catalog.py build CATALOG_DIR` | reads every header under `kit/`, writes `catalog.json` (`kit-catalog/2`: `schema`, `url`, `ver`, `built`, `entries`); each entry's `files` are its main file then its `@files`, each `{path, role, sha256, bytes}`, and `hash` the first 12 hex of the SHA-256 of the sorted `path=sha256` lines | `wrote <path>: N entries, M files` (or `unchanged ...`) | 0; 1 on a problem (below) |
| `adp_catalog.py CATALOG_DIR` | the check: the index equals what build would write, every file's size and sha256 match, no orphans, every header valid | `OK: N entries, M entry files, F files in tree, 0 orphans, all sizes, sha256 and hashes match, H valid headers`; or `FAIL: N problem(s)` followed by one indented line per problem, such as `kit.badge: sha256 kit/badge.js: file <hex> != entry <hex>`, `kit.badge: hash <hash> != computed <hash>` or `orphan: kit/old.js is not referenced by any entry or page file` | 0; 1 on any problem |

`build` exits 1, prints each problem on stderr and writes nothing when:

- a kit file is not named by any entry;
- a `@requires` names no entry;
- a header rule is broken;
- a sample key has no owner.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: a catalog tree, `adp_catalog.py build` and the check".

## Contract: reading a catalog (`kit`, `suggest`, `take`)

These read a `catalog.json`: the fetched live one (by its url, or `-` for the saved one), or a local build, which they accept with a warning on
stderr (`a local index is a build, not the live catalog ...`).

| Command | Prints | Exit |
|---|---|---|
| `kit list CATALOG [--kind K] [--tag T]` | one JSON line per entry: `{id, kind, name, summary, tags}` (`kind` here is the id prefix, not the entry's `kind` field) | 0 |
| `kit show ID CATALOG` | `{id, name, summary, about, tags, files, requires, provides, status, version, config: [[signature, options]], db}` | 0; 1 for an unknown id |
| `kit describe ID CATALOG` | how to wire it: `{id, needs, optional, provides, requires, files (code only), sample, sample_key, db}` | 0 |
| `suggest CATALOG --for "words" [--n 3] [--kind K]` | `[{id, kind, why, requires, takes}]` ranked by overlap with tags, name, summary, id, provides, about; no model call | 0 |
| `take CATALOG ID ... --url URL` | `{catalog {url, index, live, ver, built, warning?}, entries (with every @requires, in load order), files {path: {artifact, path}}, sha256, samples}`: references, never copies | 0; 1 for an unknown id, or a local index without `--url` |

`take` resolves `@requires` first: taking `viz.meter` takes `kit.badge` too, and its `files` are the publish `files` entries a page adds.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: reading a catalog (`kit`, `suggest`, `take`)".

## Contract: My Own Kit (`catalog`)

`catalog URL` saves the user's catalog url in `ADP_HOME/config.json` and keeps its files in `ADP_HOME/catalog/`. It does not fetch anything; it prints
the Artifact `read` calls for you to run.

| State | `catalog [URL]` prints |
|---|---|
| no catalog url saved | `{catalog: null, next}` |
| no `catalog.json` in `ADP_HOME/catalog/` | `{catalog, index, fetched: false, fetch}`; `fetch` is the Artifact `read` call that saves `catalog.json` there (for a Sites catalog, an authenticated HTTPS GET plan). Run it, then run `catalog` again |
| `catalog.json`, files missing | `{catalog, index, fetched: true, ver, built, entries, refresh, kit, files, missing, complete: false, reads, calls, per_call, next}`; `reads` holds Artifact `read` calls of at most 256 paths each, `refresh` is the `read` that re-fetches `catalog.json` |
| every file the index lists | the same with `missing: 0`, `complete: true` and no `reads` |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: My Own Kit (`catalog`)".
