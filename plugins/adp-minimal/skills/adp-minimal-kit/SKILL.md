---
name: adp-minimal-kit
description: "Reference for the ADP (Artifacts Done Properly) kit: the kinds of entry (components kit.*, layouts, patterns, visualizations, themes, templates, guides) and their sample bundles; how an entry's files and part markers are laid out; how to take an entry with adp.py take, link its files in dependency order, mount it with its @config signature, style it with theme tokens and persist through ADP.db. Use when the user asks what the kit contains, what kind an entry is, or how to load and mount a component, layout, pattern or visualization on a page."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The kit: structure, and how an entry wires into a page

The **kit** is the set of reusable entries that ADP (Artifacts Done Properly) pages take instead of reimplementing. It lives in the catalog under
`kit/`. An entry's id prefix (`kit.`, `layout.`, `pattern.`, `viz.`, `theme.`, `template.`, `guide.`) gives its kind.

```
kit/
  <name>.css|js          components: dom, tokens, vocab, tabs, table, tooltip, store, md, mermaid, canvas ...   (kit.*)
  layout/                shells and frames: app-shell, doc-shell, explorer-shell, topbar, stack, carousel ...   (layout.*)
  patterns/              recurring page patterns: inbox, settings, namespaces, assist, decisions, gate ...      (pattern.*)
  viz/                   visualizations: bars, sparkline, timeline, tree, flow, topology, wheel, dial ...       (viz.*)
  themes/                <id>.css (tokens only) + <id>.json per theme                                           (theme.*)
  templates/             adp2-shell, doc, record, expiry-board, tester                                          (template.*)
  guides/                Markdown guides: the dataplane standard, the component inventory                       (guide.*)
  samples/               sample data, keyed in bundles: kit.json, layout.json, patterns.json, viz.json ...
```

`adp.py kit list` prints one JSON line per entry; `--kind pattern` or `--tag timeline` filters it. Its optional CATALOG argument is the catalog URL,
`-` for the catalog saved by `adp.py catalog` (the default), or a local `catalog.json`.

| Kind | What it is | Example |
|---|---|---|
| **Component** | One small, general widget or helper with a mount function | `kit.tabs`, `kit.table`, `kit.tooltip`, `kit.dom` |
| **Layout** | The frame of a page or region: header, rail, scroll margins | `layout.topbar`, `layout.doc-shell`, `layout.app-shell` |
| **Pattern** | A recurring interaction built from components, often reading or writing the page's [record](../adp-minimal-protocol/SKILL.md#the-record) | `pattern.inbox`, `pattern.settings`, `pattern.decisions`, `pattern.assist` |
| **Viz** | A chart or diagram; labels its value range and is keyboard-accessible | `viz.sparkline`, `viz.timeline`, `viz.tree`, `viz.topology` |
| **Theme** | Tokens and fonts only; see [themes](../adp-minimal-themes/SKILL.md) | `theme.default`, `theme.glaze` |
| **Template** | A starting page or shell | `template.adp2-shell`, `template.record` |
| **Guide** | Reference documentation in Markdown | `guide.artifact-dataplane` |

## One entry, as files

An entry is a **main file** carrying its [header](../adp-minimal-catalog/SKILL.md#the-header) plus the files the header names:

```
kit/viz/sparkline.js          main file: the header comment, then the code between /* part:page.script.kit.viz.sparkline */ markers
kit/viz/sparkline.css         style, markers page.style.kit.viz.sparkline
kit/samples/viz.json          the sample bundle (shared by every viz entry; the entry owns the key "sparkline")
```

Kit files are parts too: their code sits between `part:page.script.kit.*` and `part:page.style.kit.*` markers, so tooling and diffs can attribute
every change to a specific part.

## How an entry wires into a page

1. **Take it.** `adp.py take CATALOG viz.sparkline` resolves `requires` first (here `kit.tooltip`) and prints JSON: `entries` in dependency order
   and a `files` map of `{"artifact": <catalog url>, "path": <file>}` references. It writes nothing locally; pass `files` to the Artifact publish
   call and the host copies those files into the page's artifact server-side. (A Sites-hosted catalog is the exception: it needs
   `--materialize DIR`, which copies the fetched files into DIR after checking their SHA-256.) A taken file is published with the page, but the
   page does not load it until step 2.
2. **Link it** in `index.html` in `entries` order: each taken `.css` as `<link>`, each `.js` as `<script src>`, all scripts before `parts/app.js`.
   Stylesheets go in this order: the entries' own, then `styles/page.css`, then the theme last. A global such as `Kit.sparkline` is defined only
   after its script has run.
3. **Mount it** from the page's code with the signature in the header's `@config`:

```html
<link rel="stylesheet" href="kit/tooltip.css"><link rel="stylesheet" href="kit/viz/sparkline.css">
<script src="kit/tooltip.js"></script><script src="kit/viz/sparkline.js"></script>

<div id="trend"></div>
<script>
  const trend = Kit.sparkline.line(document.getElementById('trend'),
    {values: [3, 5, 4, 8, 9], labels: ['Mon','Tue','Wed','Thu','Fri'], unit: 'orders', caption: 'Orders per day'});
  // trend.update({values: [...]}); trend.destroy();
</script>
```

4. **Style it with tokens.** Entries color themselves only with theme tokens (`--panel --ink --rule --accent --f-ui ...`), which the page's theme
   sets, so switching the theme restyles every entry on the page.
5. **Persist through the runtime.** An entry that reads or writes the record uses `ADP.db`, `ADP.user`, `ADP.agent()` and the other `ADP.*` APIs,
   never the host API (`window.claude`) directly ([host adapters](../adp-minimal-hosts/SKILL.md)). Its header's `@db` field lists the collections it
   reads and writes, or `none`.

## Layouts and the tokens contract

Layouts own geometry (`layout.topbar` writes its height to `--kit-topbar-h`; the doc shell's rail and scroll margins read it), so combine layouts
through those properties, not by overriding each other's CSS. All entries read one token vocabulary (`kit.tokens`; `Kit.tokens.contract(part)`
lists the names a file reads), so any entry works with any theme.

## Samples

An entry shows itself with sample data, kept in a bundle (`kit/samples/<folder>.json`, one JSON object, one key per sample). The header names the key:

```
 * @files     kit/viz/sparkline.css, kit/samples/viz.json
 * @preview   {"render": "viz.sparkline", "samples": ["kit/samples/viz.json#sparkline"]}
 * @samples   sparkline
```

`adp.py take` includes the bundle in its `files` map and lists, under `samples`, only the `path#key` references the entry owns. Sample data is
synthetic, never taken from a real project.

## Where to look next

[catalog](../adp-minimal-catalog/SKILL.md) for the index and its checks, [themes](../adp-minimal-themes/SKILL.md) for tokens, and
[kit authoring](../adp-minimal-kit-authoring/SKILL.md) for adding an entry, with a worked header and mount example.
