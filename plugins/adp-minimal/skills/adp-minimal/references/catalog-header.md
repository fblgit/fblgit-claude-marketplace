> Copy of [`docs/catalog-header.md`](https://github.com/fblgit/artifacts-done-properly/blob/3f0062952f499370f88200d114e954bff82fe841/docs/catalog-header.md) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.
> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository
> (https://github.com/fblgit/artifacts-done-properly); `snippets.md` shows how to do the same by hand. Calls to Claude's own tools (`Artifact`, `ArtifactData`) are examples
> of what a Claude host offers: on another host, use that host's way to read and write the page.

# Catalog entry header

Every catalog entry describes itself in one comment at the top of its main file. `catalog.json` is built from these headers, so the header is the only place the entry's facts are written.

## Main file

The file that carries the header:

- a template or guide: its file with role `template` or `doc`;
- everything else: the first file with role `script`, otherwise the first with role `style`.

Other files of the entry (a stylesheet beside its script, samples) have no header.

## Comment

- `.js` and `.css`: the first `/** ... */` block. Leading `*` on each line is ignored.
- anything else (`.txt` templates, `.md`): the first `<!-- ... -->` block.

Inside it, the first line is the entry name and the first paragraph after it is the `about` text. Further paragraphs before the first tag are notes (the API reference worth keeping next to the code); they are not read into the catalog. The tags follow. A tag line starts with `@name`; a line that does not start with `@` continues the tag above it.

```
/**
 * Data table
 * A table from rows and columns inside its own scroll frame, with numeric columns,
 * group rows with subtotals and signed figures.
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
 * @files     kit/table.css
 * @provides  Kit.table.render, Kit.table.fmt
 * @config    Kit.table.render(box, opts) | columns [{key, label, num}], rows, group
 * @config    markup | div.kit-table-box > table.kit-table
 * @tokens    --panel --ink --rule
 * @globals   none
 * @db        none
 */
```

## Tags

| Tag | Required | Value |
|---|---|---|
| `@id` | always | `kind.name`; kind is one of `kit`, `layout`, `pattern`, `viz`, `theme`, `runtime`, `template`, `guide`. Must be the entry that lists this file in `catalog.json`. |
| `@kind` | always | `component`, `theme`, `template` or `guide` |
| `@group` | always | the catalog group, for example `Board kit`, `Patterns` |
| `@status` | always | `new` or `stable` |
| `@version` | always | `major.minor.patch` |
| `@updated` | always | `YYYY-MM-DD`; drives "Latest entries" |
| `@summary` | always | one sentence, at most 260 characters |
| `@tags` | always | comma list, lowercase, no repeats |
| `@requires` | always | `none` or a comma list of entry ids |
| `@files` | always | `none` or a comma list of the entry's other files (every file except this main file); `adp_catalog.py build` reads them into the entry's `files` with role, sha256 and bytes |
| `@provides` | in a `.js` main file | `none` or a comma list of dotted JS names (`Kit.table.render`); methods of what it returns and CSS classes belong in the notes |
| `@config` | optional, repeats | `signature | what it takes`: what the page passes in |
| `@tokens` | when the entry has a style file | `none` or custom properties, comma or space separated; a trailing `?` marks an optional one (`--seam?`) |
| `@globals` | always | `none` or CDN scripts the page must load: `htm-preact`, `marked`, `dompurify` |
| `@db` | always | `none`, or the collections read and written, in words: sections `reads a; b` / `writes c` / `note text`, keywords in lowercase |
| `@preview` | optional | one line of JSON: `{"render": "<renderer>", "samples": [...], "uses": [...]}`; a sample is a path, or `path#key` for a key in a bundle (below) |
| `@samples` | optional | the bundle keys the entry owns (below) |
| `@fonts` | a theme's | the Google Fonts url its font tokens need; kept in the index |
| `@extends` | optional | the entry this one extends; kept in the index |
| `@related`, `@optional` | optional | comma lists of entry ids: related entries, and ones it works with but does not require |
| `@source` | optional, repeats | `board | file | what`: where the entry came from |
| `@changed` | optional, once | the newest change, in a sentence |

No other tag is allowed. `@config` and `@source` repeat; every other tag, `@changed` included, appears once.

## Samples are keys in a bundle

The sample data of the previews lives in four bundles, one JSON object each: `kit/samples/kit.json`, `layout.json`, `patterns.json` and `viz.json` (the folder of the entries that own the samples). A key is the name the sample had as a file (`confirm-sheet`, `viz-chips`). An entry lists the bundle it previews on in `@files` and names its sample in `@preview` as `path#key`:

```
 * @files     kit/patterns/confirm-sheet.css, kit/samples/patterns.json
 * @preview   {"render": "pattern.confirm-sheet", "samples": ["kit/samples/patterns.json#confirm-sheet"]}
```

An entry that previews on another folder's sample lists that bundle too (a theme lists `kit/samples/viz.json`). The check fails for a `#key` the bundle does not have, a bundle that is not in the entry's own `@files`, an entry that lists a bundle but names no key of it, and a bundle key that no entry's `@preview` names or no entry's `@samples` owns. A sample a template needs at run time (`kit/samples/expiry-board.json`, `tester.json`) stays its own file, named by plain path.

`@samples` (optional, a comma list of keys) names the samples an entry owns: `@samples confirm-sheet`. A theme that previews on `viz-chips` owns none and has no `@samples`; a sample used by several entries is owned by each of them. It is what `adp.py take` hands out: for an entry named on the command line, `take` puts its bundle in the files map by reference (the server copies the whole file) and prints only the entry's own refs under `samples` (`"viz.tree": ["kit/samples/viz.json#viz-tree"]`); an entry that owns no key in a bundle it previews on gets none, and an entry that comes in as a dependency brings no sample. Each key must be in a bundle of the entry's own `@files`, and every key of a bundle must be owned by some entry.

## Checking

`python3 plugins/artifacts-done-properly/skills/adp/scripts/adp_catalog.py build` writes `catalog.json` (schema `kit-catalog/2`) from the headers: the structure (id, kind, group, name, summary, tags, status, version, requires, globals, provides, main, files, hash); the check fails while it is out of date. `python3 plugins/artifacts-done-properly/skills/adp/scripts/adp_catalog.py headers [FILES...]` validates headers (`adp_catalog.py` alone runs them with the other catalog checks). A main file without a valid header fails, so a catalog file can only be committed once its header is complete. The pre-commit hook `catalog-headers` runs it on the staged files of `plugins/artifacts-done-properly/skills/adp/catalog/`. With no file arguments it checks every main file; `--report` counts conformance per kind and per rule and always exits 0.
