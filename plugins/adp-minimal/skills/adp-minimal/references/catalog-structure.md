# Catalog structure

The catalog is a folder of files plus an index. Everything a page reuses comes from it, by reference, with a version and a hash.

    catalog/
      catalog.json        the index: schema, url, ver, built, entries[]
      index.html          the catalog page (browse, preview, take)
      adp.js              the page runtime (byte-identical to the one pages get)
      content.js  parts/  the catalog page's own parts
      styles/
      kit/                the shared building blocks
        <name>.css|js     components: each file one part of the kit (tabs.js, tabs.css, table.js ...)
        layout/           shells: app-shell, doc-shell, explorer-shell, topbar, stack ...
        themes/           one <id>.css (tokens only) and <id>.json per theme
        patterns/         recurring page patterns
        guides/           Markdown guides (the dataplane guide, the component inventory)
        samples/          sample data keyed in bundles
        templates/ viz/ ...

## An entry

`catalog.json` has `schema`, `url`, `ver`, `built` and `entries`. Each entry has `id` (`runtime.adp`, `kit.tabs`, `theme.default`,
`guide.component-inventory`), `kind` (`component`, `theme`, `guide` ...), `group`, `name`, `summary`, `tags`, `status`, `version`, `requires`,
`globals`, `provides`, `main` (the file that carries the header), `files` (each with `path`, `role`, `sha256` and `bytes`) and a `hash` of the
entry. Example (`kit.tabs`, shortened):

```json
{
  "id": "kit.tabs", "kind": "component", "group": "Board kit", "name": "Accessible tabs",
  "status": "new", "version": "0.1.0", "requires": [], "globals": [], "provides": ["Kit.tabs.mount"],
  "main": "kit/tabs.js",
  "files": [
    {"path": "kit/tabs.js",  "role": "script", "sha256": "7ea8a15b...", "bytes": 7550},
    {"path": "kit/tabs.css", "role": "style",  "sha256": "a00b73f4...", "bytes": 2713}
  ],
  "hash": "a090ff09e829"
}
```

The same facts are the *header* at the top of the entry's main file, in a comment (the real header of `kit/tabs.js`, shortened):

```
/**
 * Accessible tabs
 * Kit.tabs.mount(el, {tabs, label, hash, keys, initial, onChange}) wires [data-tab] buttons to [data-tab-panel] sections ...
 *
 * @id        kit.tabs
 * @kind      component
 * @group     Board kit
 * @status    new
 * @version   0.1.0
 * @summary   An ARIA tab set over the page's markup: arrow keys, Home and End, optional digit keys, and each tab a plain #anchor deep link.
 * @tags      tabs, tablist, aria, keyboard, hash, deep link, anchor
 * @requires  none
 * @files     kit/tabs.css, kit/samples/kit.json
 * @provides  Kit.tabs.mount
 * @tokens    --panel --sunk --ink --ink-2 --rule --shadow --accent --f-ui --f-mono --seam?
 * @globals   none
 * @db        none
 */
```

`@tokens` lists the theme tokens the entry draws with; a name ending in `?` is optional. The header grammar, the tag list and the checks are in
[catalog header](catalog-header.md). The index is built from the headers, so a header and the index cannot disagree without a check failing.

## Using an entry

A page takes the entries it needs (their `requires` come first). A taken file is served, not loaded: the page's `index.html` links each `.css` and
loads each `.js` in dependency order. Each file's `sha256` in the index says whether the copy you hold is the catalog's. The road for the catalog
is in [road-catalog](road-catalog.md).

Without the ADP tools (`adp.py catalog`, `adp.py take`), browse the full catalog in the repository
(https://github.com/fblgit/artifacts-done-properly, `plugins/artifacts-done-properly/skills/adp/catalog/`) and copy files by hand, keeping the
header intact. More kit entries than the examples in this plugin are there.
