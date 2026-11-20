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

- It takes **data and options**, never a project's schema: `Kit.meter.draw(el, {value, max, label})`, not a "kiln loads bar". A component
  hard-wired to one dataset's types is too tightly coupled: generalise it into props (`rowQuery`, `colQuery`, `linkField`) and let each page map
  its data.
- It draws with **tokens only** and lists them in `@tokens`; it hard-codes no color, family or size.
- It reaches the record, the viewer and the host through `ADP.db`, `ADP.user`, `ADP.agent()`, `ADP.publish()`, `ADP.ask()`; never `window.claude`.
  Its header's `@db` says what it reads and writes.
- It is accessible by construction: ARIA roles, keyboard support, state conveyed in text and not by color alone. Charts state their range in
  words.
- An entry that keeps state or listeners returns a handle, at least `{destroy()}` and `update(patch)` when it can change in place, so a page
  can change and remove it (`Kit.badge.render` returns `{destroy}`). One that only draws, like `Kit.meter.draw`, is simply called again.
- It names its dependencies in `@requires` and its CDN scripts in `@globals`. It uses no other globals.
- Its text, ids and sample data carry **no project names, file paths or real data**.
- Its header describes what the entry does and how to mount it. No TODOs, task status, local paths or changelog prose: origin goes in
  `@source`, the latest change in `@changed`.

## Several samples

Give each entry samples that cover the edge cases, varying in **size and kind**: an empty state, a typical one, a large one, a long label, a
right-to-left or very narrow case, light and dark. Samples live in the folder's sample bundle, a JSON object with one top-level key per sample.
The bundle `kit/samples/viz.json` of the catalog fixture, where `viz.meter` owns the key `meter`:

```json
{
  "meter": {
    "note": "Invented figures.",
    "half": {"value": 5, "max": 10, "label": "Kiln loads"},
    "full": {"value": 10, "max": 10, "label": "Kiln loads"},
    "zero": {"value": 0, "max": 3, "label": "Glaze tests"}
  }
}
```

The entry's `@preview` is a JSON object naming its renderer and its samples as `bundle-path#key`
(`{"render": "viz.meter", "samples": ["kit/samples/viz.json#meter"]}`), and `@samples` lists the keys it owns. The check fails when a named key is missing from its bundle or a bundle key has no owner ([catalog](../adp-minimal-catalog/SKILL.md)).

## Add the entry

1. **Files** under `kit/<folder>/`: the main file (script, or style for a theme) and the style beside it; the folder's sample bundle is
   `kit/samples/<folder>.json` (`kit/samples/kit.json` for the `kit/` root), listed in the entry's own `@files`.
2. **Markers**: wrap the script in `/* part:page.script.kit.<name> */` ... `/* /part:page.script.kit.<name> */` and the style in
   `/* part:page.style.kit.<name> */` ... `/* /part:page.style.kit.<name> */`, the opening marker on the first line, before the header.
   `<name>` follows the folder's existing files: `kit/badge.js` uses `kit.badge`, `kit/viz/meter.js` uses `kit.viz.meter`, and
   `kit/themes/paper.css` uses `page.style.kit.theme.paper`.
3. **The header** in the main file, with the tags of [the catalog's tag table](../adp-minimal-catalog/SKILL.md#the-header): the required ones
   always, `@provides` in a script, `@tokens` when the entry has a style, and the optional ones it needs. See the example at the end of this
   page.
4. **Build and check** with `adp_catalog.py` ([catalog](../adp-minimal-catalog/SKILL.md#the-consistency-checks)):

```sh
CAT="python3 -I adp_catalog.py"
$CAT build CATALOG_DIR     # catalog.json from the headers
$CAT CATALOG_DIR           # every check must pass: sizes, hashes, orphans, headers, samples, runtime copy
```

5. **Publish by proposal**, not over the live catalog. Catalog changes go through the [loop and the inbox](../adp-minimal-delta/SKILL.md):
   `adp.py export CATALOG_DIR --url URL` reads the live catalog, then `adp.py propose CATALOG_DIR --by NAME --summary S` writes the change as one
   proposal whose files are each guarded by an `ifMatch` on their live sha, and an editor previews and applies it from the catalog page. Try
   changes on a scratch artifact first, and never change a catalog others use without the owner's approval.
6. **Use it**: from the page, `adp.py take - <id>`, link, mount ([kit](../adp-minimal-kit/SKILL.md)).

## Changing an entry later

Bump `@version`, set `@updated`, replace `@changed` with one sentence describing the newest change, rebuild, recheck. A changed file changes its
`sha256` and the entry `hash`, which is how a page knows its copy is no longer the catalog's. Never change an id: add a new entry, and say in
the old entry's description paragraph (the `about` text under its name) that it is superseded and by which id. `@status` takes only `new` or
`stable`.

## Example: an entry that requires another (`viz.meter`)

The catalog fixture `catalog-a` ([vectors](../adp-minimal-catalog/vectors.md)) is the complete example: every file, header and sample of four
entries. `viz.meter` shows an entry built on another:

```js
/* part:page.script.kit.viz.meter */
/**
 * Meter
 * Kit.meter.draw(el, {value, max, label}) draws a bar that states its value in words, with a badge for the tone it falls in.
 *
 * @id        viz.meter
 * @kind      component
 * @group     Visualizations
 * @status    new
 * @version   0.1.0
 * @updated   2026-11-20
 * @summary   A bar that states its value and range in words, with a status badge.
 * @tags      meter, bar, progress, value
 * @requires  kit.badge
 * @files     kit/viz/meter.css, kit/samples/viz.json
 * @provides  Kit.meter.draw
 * @config    Kit.meter.draw(el, opts) | value, max, label
 * @tokens    --panel --ink --accent --f-ui
 * @globals   none
 * @db        none
 * @preview   {"render": "viz.meter", "samples": ["kit/samples/viz.json#meter"]}
 * @samples   meter
 */
```

What the header promises: `take` brings `kit.badge` first (`@requires`); the page's theme sets the four `@tokens`; the entry touches no
database (`@db none`); the value is stated in text (`Kiln loads: 5 of 10`), not by the bar's length or the badge's color alone.
