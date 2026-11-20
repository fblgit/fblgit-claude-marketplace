---
name: adp-minimal-kit-authoring
description: "Explains how to build an ADP kit entry instead of hand-writing a one-off: look and take first, what makes an entry general (data and options, tokens only, ADP.* not window.claude, accessible, update and destroy), several samples per entry in a bundle, files, markers and header, build and check, publishing by proposal, versioning, and clearing stale developer notes from entries. Use when the user wants a reusable widget, layout, chart, pattern or theme, or asks how to add or update a catalog entry."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Building kits: general, with several samples

This is how the catalog grows, and why ADP pages get better over time instead of each starting from nothing.

Nothing reusable is written inside a page. When a page needs a widget, a layout, a chart, a pattern or a look, the answer is a **kit entry**: written once,
in the catalog, general enough that the next page takes it unchanged. Hand-writing it into one page, or copying a kit file by retyping it, is the thing
this rule abolishes.

## Decide

1. **Look first.** `adp.py suggest - --for "what you need"`, `kit list`, `kit show`. The catalog probably has it ([catalog](../adp-minimal-catalog/SKILL.md)).
2. **Take it** if it fits. A near miss is a reason to extend the entry (a new option, a new sample), not to fork it.
3. **Add it** only when nothing fits and at least a second page could use it. If only this page will ever want it, it is this page's copy or layout, a
   normal edit ([roads](../adp-minimal-roads/SKILL.md)).

## What makes an entry general

- It takes **data and options**, never a project's schema: `Kit.table.render(box, {columns, rows, group})`, not a "keys table". A component hard-wired
  to one board's kinds is the inventory's "high coupling": generalise it into props (`rowQuery`, `colQuery`, `linkField`) and let each board map its data.
- It draws with **tokens only** and lists them in `@tokens`; it hard-codes no colour, family or size.
- It reaches the record, the viewer and the host through `ADP.db`, `ADP.user`, `ADP.agent()`, `ADP.publish()`, `ADP.ask()`; never `window.claude`.
  Its header's `@db` says what it reads and writes.
- It is accessible by construction (roles, keyboard, a state described in words, not colour alone) and states its range or limits where it draws.
- It returns `{update(patch), destroy()}` (or the equivalent), so a page can change and remove it.
- It names its dependencies in `@requires` and its CDN needs in `@globals`; it does not reach for anything else.
- Its text, ids and sample data carry **no project names, paths or private figures**.

## Several samples

One sample proves one shape; several prove the entry is general. Give each entry samples that differ in **size and kind**: an empty state, a typical
one, a large one, a long label, a right-to-left or very narrow case, light and dark. Samples live in the folder's bundle, one key each:

```json
// kit/samples/viz.json  (excerpt)
{
  "sparkline": {
    "note": "Invented figures.",
    "line":  {"values": [3, 5, 4, 8, 9], "labels": ["Mon","Tue","Wed","Thu","Fri"], "unit": "kg"},
    "flat":  {"values": [4, 4, 4, 4]},
    "empty": {"values": []},
    "long":  {"values": [/* 200 points */], "caption": "A long caption that must wrap without moving the range text"}
  }
}
```

The header names the key it owns; every bundle key must be owned by some entry, and every `#key` named must exist ([catalog](../adp-minimal-catalog/SKILL.md)).

## Add the entry

1. **Files** under `kit/<folder>/`: the main file (script, or style for a theme), the style beside it, and the folder's sample bundle.
2. **Markers**: the script between `/* part:page.script.kit.<folder>.<name> */` ... `/* /part:... */`, the style between `page.style.kit...`.
3. **The header** in the main file: `@id` (`viz.sparkline`), `@kind`, `@group`, `@status new`, `@version 0.1.0`, `@updated`, `@summary`, `@tags`, `@requires`,
   `@files`, `@provides`, `@config` (one per public function), `@tokens`, `@globals`, `@db`, `@preview`, `@samples`. See [catalog](../adp-minimal-catalog/SKILL.md#the-header) and the
   example at the end of this page.
4. **Build and check:**

```sh
CAT="python3 -I <adp skill folder>/scripts/adp_catalog.py"
$CAT build      # catalog.json from the headers
$CAT            # every check must pass: sizes, hashes, orphans, headers, samples, runtime copy
```

5. **Publish by proposal**, not over the live catalog: the catalog changes through the inbox (`publish_catalog.py update --url URL` plans proposals whose
   `ifMatch` is the live sha of each changed file). Try anything on a scratch artifact first and never republish a catalog others use without asking.
6. **Use it**: from the page, `adp.py take - viz.sparkline`, link, mount ([kit](../adp-minimal-kit/SKILL.md)).

## Changing an entry later

Bump `@version`, set `@updated`, add one sentence to `@changed`, rebuild, recheck. A changed file changes its `sha256` and the entry `hash`, which is how a
page knows its copy is no longer the catalog's. Never change an id; add a new entry and mark the old one superseded in its `about`.

## Smells to clear when you find them

Entries and docs that carry a developer's task notes instead of what the thing is: a status line that records a developer's task state, a path on someone's machine, a
board or project name in a sample, a "copied byte for byte from" provenance note that no longer matches, a paragraph describing what a past session did.
Each is stale or irrelevant to a user: rewrite the header so it states what the entry does and how to mount it, put real provenance in `@source` (origin
only) and the newest change in `@changed` (one sentence), and run the catalog checks.

## Example: a kit entry (accessible tabs)

A catalog entry is a file with a header, plus the files it names. This is the shape of `kit.tabs`: markup contract, small API, tokens it
draws with. It is a trimmed excerpt, not the whole file.

**Use it on a page**

```html
<link rel="stylesheet" href="kit/tabs.css">
<script src="kit/tabs.js"></script>

<div class="kit-tabs" id="record-tabs">
  <div class="kit-tabs-list" role="tablist" aria-label="Record">
    <button role="tab" data-tab="overview">Overview</button>
    <button role="tab" data-tab="history">History</button>
  </div>
  <section data-tab-panel="overview">...</section>
  <section data-tab-panel="history">...</section>
</div>
<script>
  const tabs = Kit.tabs.mount(document.getElementById('record-tabs'), { hash: true, keys: true });
  // tabs.select('history'); tabs.current(); tabs.destroy();
</script>
```

**What the header promises** (`kit/tabs.js`): `@provides Kit.tabs.mount`; `@tokens --panel --sunk --ink --ink-2 --rule --shadow --accent
--f-ui --f-mono --seam?` (the page's theme must set the ones without a `?`); `@db none` (it touches no database); ids are bare tokens
(letters, digits, `. _ ~ -`), never `settings`, `sidebar`, `customize`, `upgrade`, `downloads` or `comment-...`, which the viewer keeps.

More kit examples (themes, layouts such as `app-shell`, `doc-shell` and `topbar`, patterns, visualisations, samples) are in the project
repository: https://github.com/fblgit/artifacts-done-properly, `plugins/artifacts-done-properly/skills/adp/catalog/kit/`.
