---
name: adp-minimal-themes
description: "Theme system for ADP (Artifacts Done Properly) pages: a theme as tokens only (a CSS file with light, dark and data-theme blocks, a JSON twin and a Google Fonts URL), the 55-name token contract, layer themes, adp.py new --theme, link order after page.css, runtime switching with look.theme, and changing a page's theme later. Use when the user asks about tokens, dark mode, fonts, choosing or switching a theme, or building a custom palette."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Themes

A theme is a catalog entry that sets design tokens and nothing else. Every presentational choice a component makes is read from a token: color
and type, but also shape, density, surface and arrangement. Pages link a theme instead of defining their own look, and every kit stylesheet uses the
same token names, so swapping the theme takes a page from one look to another, including at run time, while its markup, part ids and behavior stay
the same.

## What a theme is

A catalog entry `theme.<id>` (kind `theme`, group `Themes`) with two files and one font URL:

| Part | Where | Holds |
|---|---|---|
| stylesheet | `kit/themes/<id>.css` | Tokens only, in three blocks: light on `:root`; dark under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...} }`; dark again under `:root[data-theme="dark"]` |
| data | `kit/themes/<id>.json` | `id`, `name`, `about`, `source`, `fonts`, `light`, `dark`, `aliases`, `scale`. Catalog previews and theme pickers read it instead of parsing the CSS |
| fonts | `fonts` in the JSON and in the catalog entry (the same URL) | One Google Fonts `css2` URL with `display=swap` that loads the first family of each font token. Display, UI and mono families are requested up to at least weight 700; `--f-hand` may be a system stack with no web font |

Abridged example; [the token contract](#the-token-contract) lists every name:

```css
/* kit/themes/mine.css: tokens only */
:root {
  --bg: #fbfaf7;  --panel: #ffffff;  --sunk: #f1efe9;
  --ink: #1d1b16; --ink-2: #4a463c;  --ink-3: #7a7466;
  --rule: #e2ded3; --rule-2: #cfc9ba;
  --accent: #2f5d50; --accent-ink: #ffffff;
  --ok: #2e7d4f; --warn: #b7791f; --danger: #b3261e;
  --f-display: "Fraunces", serif; --f-ui: "Inter", system-ui, sans-serif;
  --f-mono: ui-monospace, monospace; --f-hand: "Caveat", cursive;
  /* ...plus the rest of the contract: --info, --wait, every -soft tint, the highlights, kinds, drawing colors, sticky notes, depth, surface and type */
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #14130f; --panel: #1c1a15; /* ...every color token again */ } }
:root[data-theme="dark"] { --bg: #14130f; --panel: #1c1a15; /* ...the same values as the media block */ }
```

## The token contract

Every theme sets these 55 names in its light block, and the first 45 (all but the last two groups) again in each dark block:

- Surfaces and ink: `--bg --panel --sunk --ink --ink-2 --ink-3 --rule --rule-2 --accent --accent-ink --accent-soft`.
- Status colors: `--ok --warn --danger --info --wait`, each with a `-soft` tint.
- Highlights: `--seam` (the highlight line: current link, selected tab, focus outlines; kit files fall back to `--accent`), `--gold-leaf` (the
  decorative hairline under the top bar, the hero and the doc header; may be a gradient) and `--focus`. A theme with no separate highlight sets all three to its accent.
- Kinds: `--k-problem --k-solution --k-idea --k-question --k-decision --k-task`.
- Drawing colors: `--c-ink --c-blue --c-red --c-green --c-amber --c-violet`.
- Sticky notes and canvas: `--st-yellow --st-blue --st-pink --st-green --sticky-ink --canvas --dot`.
- Depth: `--shadow --outline`.
- Fonts (light block only): `--f-display --f-ui --f-mono --f-hand`.
- Surface and type (light block only): `--bg-image --bg-size --edge-w --text-size --leading --head-case`.

Component tokens go beyond the contract: a kit entry may read further tokens of its own (spacing, radius, placement such as a grid's areas or a
bar's direction). It declares each one in its header's `@tokens`, with `?` when the entry has a fallback, so a theme knows what it can set.

The list above is the contract. A catalog's default theme also sets every token that one of its kit entries declares as required (`@tokens`
without `?`), and every other theme in that catalog sets every name the default sets: in light, and in dark wherever the default's dark map
has it. A theme may set more. A theme with internal
names of its own aliases them to the contract names in a second `:root` block (`--f-ui: var(--f-body)`). A **layer theme** builds on another:
it names the base theme in `@requires`, is linked after it, sets only the tokens it changes, and sets no font token.

The catalog fixture of this plugin ships one theme, `theme.paper`. It sets only a few names: it exists to exercise the catalog tool,
which does not check the contract ([catalog](../adp-minimal-catalog/SKILL.md#the-consistency-checks)).

Each theme's stylesheet header lists the text/background pairs that reach 4.5:1 (WCAG AA) in light and dark, and any exception. These ratios are
stated by the theme's author; no tool here checks them.

## Applying a theme

**At creation**: `adp.py new TEMPLATE DIR --theme paper --catalog CATALOG`. `--theme` takes a short name or an entry id. Without it, the page
gets the catalog's `theme.default` when the catalog has one. An unknown name exits with an error that lists the available themes, and nothing is written. The theme is
added to the page's [take](../adp-minimal-kit/SKILL.md#how-an-entry-wires-into-a-page) list, so the
[publish object](../adp-minimal-new-artifact/SKILL.md#create-check-publish-seed) carries its files by reference, and `index.html` links the theme's
fonts before `page.css` and the theme stylesheet after it:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...">   <!-- the theme's fonts, the page's only font link -->
<link rel="stylesheet" href="styles/page.css">
<link rel="stylesheet" href="kit/themes/paper.css">                           <!-- tokens last: they override page.css's fallbacks -->
```

Because the theme comes after `page.css` and sets only tokens, it overrides the template's placeholder tokens and leaves the page's rules alone.
For a palette of your own, set the tokens in `page.css` and remove the theme's link.

`link_tags` writes those links. It places the theme's font URLs and the taken entries' stylesheets before `page.css`, theme stylesheets after it
and scripts before `parts/app.js`, and skips any file `index.html` already loads.

```python
# ---
# id: themes.link
# tool: adp.py
# section: themes
# order: 600
# needs: [core.cli]
# tests: [new-minimal]
# sha: 92be9093c7a7
# ---
PAGE_CSS = '<link rel="stylesheet" href="styles/page.css">\n'
APP_JS = '<script src="parts/app.js"></script>'


def link_tags(d, files, fonts=()):
    """Link taken files and theme fonts into DIR/index.html: fonts and entry styles, page.css, theme styles; scripts before parts/app.js."""
    p = Path(d, 'index.html'); html = p.read_text(encoding='utf-8')
    fresh = lambda xs, ext: [x for x in dict.fromkeys(xs) if x.endswith(ext) and f'"{x}"' not in html]
    css = fresh(files, '.css')
    link = lambda xs: ''.join(f'<link rel="stylesheet" href="{x}">\n' for x in xs)
    html = html.replace(PAGE_CSS, link(fresh(fonts, '') + [x for x in css if not x.startswith('kit/themes/')]) + PAGE_CSS
                        + link(x for x in css if x.startswith('kit/themes/')), 1)
    html = html.replace(APP_JS, ''.join(f'<script src="{x}"></script>\n' for x in fresh(files, '.js')) + APP_JS, 1)
    p.write_text(html, encoding='utf-8')
```

**At run time**: a page that has taken several themes and a theme picker from its catalog can switch themes while it is open. A light/dark/system
control sets `data-theme` on the root; the picker swaps the linked theme. A viewer's picks are kept in their browser. The page-wide choice is the
`look.theme` [switch](../adp-minimal-runtime/SKILL.md) in `config/current`: its options are the themes the page has installed, and its default is
the theme `--theme` linked. Changing `look.theme` clears viewers' own theme picks. Other pages offer only the theme they were built with. A page built from `minimal` links no theme until it takes one: its `styles/page.css` sets the colors and fonts it
uses, the contract's `--text-size`, `--leading` and `--edge-w`, and three page tokens of its own (`--space`, `--radius`, `--measure`), and
its rules read only tokens, so a theme linked after it changes the page's color, type, spacing, corners and width.

**Changing it later**: on a page with the theme picker, change `look.theme`. On any other page, take the new theme (`adp.py take CATALOG theme.<id>`),
replace both the theme `<link>` and the font `<link>` in `index.html`, publish, and record the change with `adp.py record` as in
[the six steps](../adp-minimal-protocol/SKILL.md#the-six-steps).

**Adding a theme** is a catalog change: [kit authoring](../adp-minimal-kit-authoring/SKILL.md).

## Why tokens only

A theme that only sets tokens cannot override component rules, so it cannot break a component: swapping themes changes how the page is
presented (color, type, shape, density, arrangement), never its markup or behavior. The reach of a theme is therefore set by the components:
whatever a component reads from a token, a theme can change. Components never hard-code a color, a font family or a layout value that a theme
should be able to change; a page that needs one more value defines its own token in `page.css`.

A theme is valid when it sets every name in the contract (light, and the color groups in dark), sets every name its catalog's default theme
sets, its CSS and JSON agree on the font tokens, and its font URL loads the first family of every font token, with display, UI and mono
families requested at weight 700 or more. `adp_catalog.py check` does not test these rules; check them when you add a theme.
