---
name: adp-minimal-kit
description: "Explains the ADP kit structure and how a piece wires into a page: components (kit.*), layouts, patterns, viz, themes, templates, guides and sample bundles; an entry's files and part markers; take, link and script order, mounting with the @config signature, drawing with tokens, persisting through ADP.db. Use when the user asks what the kit holds, which kind an entry is, or how to load and mount a component, layout, pattern or visualisation on a page."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The kit: structure, and how a piece wires into a page

The **kit** is the shared set of building blocks a page takes instead of writing. It lives in the catalog under `kit/`. The id prefix of an entry is its
kind of building block.

```
kit/
  <name>.css|js          components: dom, tokens, vocab, tabs, table, tooltip, store, md, mermaid, canvas ...   (kit.*)
  layout/                shells and frames: app-shell, doc-shell, explorer-shell, topbar, stack, carousel ...   (layout.*)
  patterns/              recurring page patterns: inbox, settings, namespaces, assist, decisions, gate ...      (pattern.*)
  viz/                   visualisations: bars, sparkline, timeline, tree, flow, topology, wheel, dial ...       (viz.*)
  themes/                <id>.css (tokens only) + <id>.json per theme                                           (theme.*)
  templates/             adp2-shell, doc, record, expiry-board, tester                                          (template.*)
  guides/                Markdown guides: the dataplane standard, the component inventory                       (guide.*)
  samples/               sample data, keyed in bundles: kit.json, layout.json, patterns.json, viz.json
```

(The catalog holds about 140 entries: roughly 53 patterns, 30 visualisations, 27 components, 14 themes, 9 layouts, 5 templates, 2 guides and the
runtime. `adp.py kit list - --kind pattern` is the live list.)

| Kind | What it is | Example |
|---|---|---|
| **Component** | One small, general widget or helper with a mount function | `kit.tabs`, `kit.table`, `kit.tooltip`, `kit.dom` |
| **Layout** | The frame of a page or region, wiring header, rail, scroll margins | `layout.topbar`, `layout.doc-shell`, `layout.app-shell` |
| **Pattern** | A recurring interaction built from components, often reading or writing the record | `pattern.inbox`, `pattern.settings`, `pattern.decisions`, `pattern.assist` |
| **Viz** | A chart or diagram that states its range and is keyboard-reachable | `viz.sparkline`, `viz.timeline`, `viz.tree`, `viz.topology` |
| **Theme** | Tokens and fonts only; see [themes](../adp-minimal-themes/SKILL.md) | `theme.default`, `theme.glaze` |
| **Template** | A starting page or shell | `template.adp2-shell`, `template.record` |
| **Guide** | Markdown a human or agent reads | `guide.artifact-dataplane` |

## One entry, as files

An entry is a **main file** carrying its [header](../adp-minimal-catalog/SKILL.md#the-header) plus the files the header names:

```
kit/viz/sparkline.js          main file: the header comment, then the code between /* part:page.script.kit.viz.sparkline */ markers
kit/viz/sparkline.css         style, markers page.style.kit.viz.sparkline
kit/samples/viz.json          the sample bundle (shared by every viz entry; the entry owns the key "sparkline")
```

Kit files are parts too: their code sits between `part:page.script.kit.*` and `part:page.style.kit.*` markers, so a restyle or fix names what it touched.

## How a piece wires into a page

1. **Take it** by reference, `requires` first (`adp.py take - viz.sparkline` brings `kit.tooltip` too). The server copies the files; they are served,
   not loaded.
2. **Link and load it** in `index.html` in dependency order: each taken `.css` as `<link>`, each `.js` as `<script src>`, before `parts/app.js`.
   Stylesheets order: the entries' own (in `entries` order), then `styles/page.css`, then the theme last. A global such as `Kit.sparkline` exists only
   after its script ran.
3. **Mount it** from the page's code with the signature in the header's `@config`:

```html
<link rel="stylesheet" href="kit/tooltip.css"><link rel="stylesheet" href="kit/viz/sparkline.css">
<script src="kit/tooltip.js"></script><script src="kit/viz/sparkline.js"></script>

<div id="trend"></div>
<script>
  const trend = Kit.sparkline.line(document.getElementById('trend'),
    {values: [3, 5, 4, 8, 9], labels: ['Mon','Tue','Wed','Thu','Fri'], unit: 'kg', caption: 'Kept per day'});
  // trend.update({values: [...]}); trend.destroy();
</script>
```

4. **Draw with the tokens.** Entries colour themselves only with theme tokens (`--panel --ink --rule --accent --f-ui ...`); the page's theme sets them. That
   is why one theme switch restyles every entry on the page.
5. **Persist through the runtime.** An entry that reads or writes the record takes `ADP.db`, `ADP.user`, `ADP.agent()` and friends, never
   `window.claude` ([host adapters](../adp-minimal-hosts/SKILL.md)). Its header's `@db` says which collections it reads and writes, in words.

## Layouts and the tokens contract

Layouts own geometry (`--kit-topbar-h` is set by the top bar and read by the doc shell's rail and scroll margins), so combine them through those
properties, not by overriding each other's CSS. Entries share one token vocabulary (`kit.tokens`, `Kit.tokens.contract(part)` lists the names a file
reads), which is what lets any entry sit on any theme.

## Samples

An entry shows itself with sample data, kept in a bundle (`kit/samples/<folder>.json`, one JSON object, one key per sample). The header names the key:

```
 * @files     kit/viz/sparkline.css, kit/samples/viz.json
 * @preview   {"render": "viz.sparkline", "samples": ["kit/samples/viz.json#sparkline"]}
 * @samples   sparkline
```

`adp.py take` hands out the bundle by reference and prints only the entry's own `path#key`. Samples are invented, general figures, not a project's data.

## Where to look next

[catalog](../adp-minimal-catalog/SKILL.md) for the index and its checks, [themes](../adp-minimal-themes/SKILL.md) for tokens, [kit authoring](../adp-minimal-kit-authoring/SKILL.md) for adding an entry,
[kit authoring](../adp-minimal-kit-authoring/SKILL.md) also has a worked header and mount.
