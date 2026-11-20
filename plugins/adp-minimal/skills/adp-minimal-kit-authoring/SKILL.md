---
name: adp-minimal-kit-authoring
description: "Explains how to build an ADP kit entry instead of hand-writing a one-off: look and take first, what makes an entry general (data and options, tokens only, ADP.* not window.claude, accessible, update and destroy), several samples per entry in a bundle, files, markers and header, build and check, publishing by proposal, and versioning. Use when the user wants a reusable widget, layout, chart, pattern or theme, or asks how to add or update a catalog entry."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Authoring kit entries

Reusable UI (a widget, layout, chart, pattern or theme) belongs in the catalog as a **kit entry**, not inline in a page. Write it once, generally
enough that the next page can take it unchanged. Pull entries into a page with `adp.py take`; don't copy kit files by hand.

## Decide

1. **Look first.** `adp.py suggest - --for "what you need"`, `kit list`, `kit show` ([catalog](../adp-minimal-catalog/SKILL.md)). Check before
   writing anything.
2. **Take it** if it fits. A near miss is a reason to extend the entry (a new option, a new sample), not to fork it.
3. **Add it** only when nothing fits and at least one other page could use it. If only this page needs it, edit the page directly (see
   [roads](../adp-minimal-roads/SKILL.md)).

## What makes an entry general

- It takes **data and options**, never a project's schema: `Kit.table.render(box, {columns, rows, group})`, not a "keys table". A component
  hard-wired to one dataset's types is too tightly coupled: generalise it into props (`rowQuery`, `colQuery`, `linkField`) and let each page map
  its data.
- It draws with **tokens only** and lists them in `@tokens`; it hard-codes no color, family or size.
- It reaches the record, the viewer and the host through `ADP.db`, `ADP.user`, `ADP.agent()`, `ADP.publish()`, `ADP.ask()`; never `window.claude`.
  Its header's `@db` says what it reads and writes.
- It is accessible by construction: ARIA roles, keyboard support, state conveyed in text and not by color alone. Charts state their range in
  words.
- It returns `{update(patch), destroy()}` (or the equivalent), so a page can change and remove it.
- It names its dependencies in `@requires` and its CDN scripts in `@globals`. It uses no other globals.
- Its text, ids and sample data carry **no project names, file paths or real data**.
- Its header describes what the entry does and how to mount it. No TODOs, task status, local paths or changelog prose: origin goes in
  `@source`, the latest change in `@changed`.

## Several samples

Give each entry samples that cover the edge cases, varying in **size and kind**: an empty state, a typical one, a large one, a long label, a
right-to-left or very narrow case, light and dark. Samples live in the folder's sample bundle, a JSON object with one top-level key per sample.
An illustrative bundle for a sparkline entry:

```json
{
  "sparkline": {
    "line":  {"values": [3, 5, 4, 8, 9], "labels": ["Mon","Tue","Wed","Thu","Fri"], "unit": "kg"},
    "flat":  {"values": [4, 4, 4, 4]},
    "empty": {"values": []},
    "long":  {"values": [3, 5, 4, 8, 9, 7, 6, 8], "caption": "A long caption that must wrap without moving the range text"}
  }
}
```

The entry's `@preview` names its samples as `bundle-path#key` (for example `kit/samples/viz.json#sparkline`), and `@samples` lists the keys it
owns. The check fails when a named key is missing from its bundle or a bundle key has no owner ([catalog](../adp-minimal-catalog/SKILL.md)).

## Add the entry

1. **Files** under `kit/<folder>/`: the main file (script, or style for a theme), the style beside it, and the folder's sample bundle.
2. **Markers**: wrap the script in `/* part:page.script.kit.<name> */` ... `/* /part:page.script.kit.<name> */` and the style in
   `/* part:page.style.kit.<name> */` ... `/* /part:page.style.kit.<name> */`. Follow the folder's existing files: `kit/viz/` and
   `kit/templates/` put the folder in the id (`page.script.kit.viz.sparkline`); `kit/layout/` and `kit/patterns/` do not
   (`page.script.kit.app-shell`).
3. **The header** in the main file: `@id` (`viz.sparkline`), `@kind`, `@group`, `@status new`, `@version 0.1.0`, `@updated`, `@summary`, `@tags`,
   `@requires`, `@files`, `@provides`, `@config` (one per public function), `@tokens`, `@globals`, `@db`, `@preview`, `@samples`. See
   [catalog](../adp-minimal-catalog/SKILL.md#the-header) and the example at the end of this page.
4. **Build and check** with `adp_catalog.py` ([catalog](../adp-minimal-catalog/SKILL.md#the-consistency-checks)):

```sh
CAT="python3 -I adp_catalog.py"
$CAT build      # catalog.json from the headers
$CAT            # every check must pass: sizes, hashes, orphans, headers, samples, runtime copy
```

5. **Publish by proposal**, not over the live catalog. Catalog changes go through the [inbox](../adp-minimal-delta/SKILL.md):
   `publish_catalog.py update --url URL` writes one proposal per changed kit folder, each file guarded by an `ifMatch` on its live sha, and an
   editor applies them from the page. Try changes on a scratch artifact first, and never republish a catalog others use without the owner's
   approval.
6. **Use it**: from the page, `adp.py take - viz.sparkline`, link, mount ([kit](../adp-minimal-kit/SKILL.md)).

## Changing an entry later

Bump `@version`, set `@updated`, replace `@changed` with one sentence describing the newest change, rebuild, recheck. A changed file changes its
`sha256` and the entry `hash`, which is how a page knows its copy is no longer the catalog's. Never change an id: add a new entry, and say in
the old entry's description paragraph (the `about` text under its name) that it is superseded and by which id. `@status` takes only `new` or
`stable`.

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
--f-ui --f-mono --seam?` (the page's theme must set the ones without a `?`); `@db none` (it touches no database). Tab ids are bare tokens
(letters, digits, `. _ ~ -`). The ids `settings`, `sidebar`, `customize`, `upgrade`, `downloads` and any id starting with `comment-` are
reserved by the host viewer.
