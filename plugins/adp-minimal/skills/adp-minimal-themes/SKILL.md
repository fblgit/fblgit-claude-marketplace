---
name: adp-minimal-themes
description: "Explains ADP themes and how they wire: a theme as tokens only (css with light, dark and data-theme blocks, plus json and a Google Fonts url), the token contract and the one convention set by theme.default, layer themes, the shipped themes, adp.py new --theme, link order after page.css, viewer switching and look.theme, changing a page's theme later. Use when the user asks about tokens, dark mode, fonts, choosing or switching a theme, or making a palette."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Themes, and how they wire

Themes are catalog entries too, so a page's look is taken and switched like any other piece instead of being written into it.

A theme is the look of a page, expressed as **tokens** only. Every kit file draws with the same token names, so changing the theme restyles the
whole page, and a viewer can switch themes at run time.

## What a theme is

A catalog entry `theme.<id>` (kind `theme`, group `Themes`) with two files and one font URL:

| Part | Where | Holds |
|---|---|---|
| stylesheet | `kit/themes/<id>.css` | Tokens only, in three blocks: light on `:root`; dark under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...} }`; dark again under `:root[data-theme="dark"]` |
| data | `kit/themes/<id>.json` | `id`, `name`, `about`, `source`, `fonts`, `light`, `dark`, `aliases`, `scale`. The catalog preview, `kit.skins` and `pattern.playground` read it |
| fonts | `fonts` in the JSON and the entry (the same URL) | One Google Fonts `css2` URL with `display=swap` loading the first family of each font token at every weight 400 to 800 it ships |

```css
/* kit/themes/mine.css : tokens only */
:root {
  --bg: #fbfaf7;  --panel: #ffffff;  --sunk: #f1efe9;
  --ink: #1d1b16; --ink-2: #4a463c;  --ink-3: #7a7466;
  --rule: #e2ded3; --rule-2: #cfc9ba;
  --accent: #2f5d50; --accent-ink: #ffffff;
  --ok: #2e7d4f; --warn: #b7791f; --danger: #b3261e;
  --f-display: "Fraunces", serif; --f-ui: "Inter", system-ui, sans-serif;
  --f-mono: ui-monospace, monospace; --f-hand: "Caveat", cursive;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #14130f; --panel: #1c1a15; /* ...every token again */ } }
:root[data-theme="dark"] { --bg: #14130f; --panel: #1c1a15; /* ...the same values as above */ }
```

## The token contract

`--bg --panel --sunk --ink --ink-2 --ink-3 --rule --rule-2 --accent --accent-ink`; the meanings `--ok --warn --danger --info --wait`, each with a `-soft` tint;
`--seam --gold-leaf --focus`; the four font tokens `--f-display --f-ui --f-mono --f-hand`; and the feel tokens (`--outline --edge-w --text-size --leading
--head-case`). **One convention**: every theme sets the same names. `theme.default` is the reference: it sets every token a kit header declares as
required (`@tokens` without `?`), and every other theme sets every name the default sets, in light and, where the default's dark map has it, in dark. A
theme may set more. A theme that keeps its own names maps them in a second `:root` block (`--f-ui: var(--f-body)`). A **layer theme** adds to another
(`theme.glaze-depth` requires `theme.glaze` and sets no font token).

The catalog ships fourteen: `default`, `glaze`, `glaze-depth`, `classic`, `console`, `journal`, `kanban`, `longpage`, `manuscript`, `notebook`,
`blueprint`, `warroom`, `journey-whiteboard`, `adr-drafting-table`. Text pairs are 4.5:1 or more in both modes.

## How a page wears one

**At creation**: `adp.py new TEMPLATE DIR --theme glaze --catalog CATALOG`. `--theme` takes a short name or an entry id; an unknown name exits listing the
ones the catalog has, before anything is written. The publish object carries the theme's files by reference and `index.html` gets two tags:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...">   <!-- the theme's fonts, before page.css -->
<link rel="stylesheet" href="styles/page.css">
<link rel="stylesheet" href="kit/themes/glaze.css">                           <!-- tokens last: they win over page.css's fallbacks -->
```

The theme is linked after `styles/page.css` and holds tokens only, so it overrides the template's placeholder tokens and leaves the page's rules alone.
For a palette of your own, set the tokens in `page.css` and remove the theme's link.

**Assistant and default tiers** carry every catalog theme and `kit.skins`: the viewer switches in the header (`data-theme` on the root, three states:
system, light, dark, through `Kit.theme.create`), and an editor sets the page's theme in Settings (`look.theme`); `--theme` picks the one it opens with.

**Later**: switching an existing page's theme means replacing both its theme `<link>` and its font `<link>`, and recording the change.

**Adding a theme** is a catalog change: [kit authoring](../adp-minimal-kit-authoring/SKILL.md).

## Why tokens only

Because nothing else in a theme can break a component. Components never hard-code a colour or a family; a page that needs one more shade defines a
token on its own part. The contract is checkable: a theme that omits a required token, a JSON that disagrees with its CSS, or a font URL that does not
load the first family of every font token at weight 700 or more is a test failure in the ADP repository.
