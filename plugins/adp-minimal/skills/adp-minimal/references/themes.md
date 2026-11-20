> Copy of [`docs/themes.md`](https://github.com/fblgit/artifacts-done-properly/blob/3f0062952f499370f88200d114e954bff82fe841/docs/themes.md) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.
> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository
> (https://github.com/fblgit/artifacts-done-properly); `snippets.md` shows how to do the same by hand. Calls to Claude's own tools (`Artifact`, `ArtifactData`) are examples
> of what a Claude host offers: on another host, use that host's way to read and write the page.

# Themes and the look of a page

How a theme is made, how a page wears one (at `adp.py new`, later, or switched by the viewer), how to change the rest of the look, and how to add a theme to the catalog. `ADP` means `python3 -I <adp skill folder>/scripts/adp.py`; CATALOG is as in `plugins/artifacts-done-properly/skills/adp-catalog/SKILL.md`.

## What a theme is

A theme is a catalog entry `theme.<id>` (kind `theme`, group `Themes`) with two files and one font url:

| Part | Where | What it holds |
|---|---|---|
| stylesheet | `kit/themes/<id>.css`, role `style` | Tokens only, in three blocks: light on `:root`; dark under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { … } }`; dark again under `:root[data-theme="dark"]`. The header follows `docs/catalog-header.md` and repeats the font url. |
| data | `kit/themes/<id>.json`, role `data` | `id`, `name`, `about`, `source`, `fonts`, `light`, `dark`, `aliases`, `scale`. The `light` and `dark` maps carry the same tokens as the css. The catalog previews, `kit.skins` (a `json` skin) and `pattern.playground` read this file. |
| fonts | `fonts` in the json and in the catalog entry (the same url) | One Google Fonts `css2` url with `display=swap` that loads the first family of each font token, at every weight from 400 to 800 the family ships (pages set headings at 700 to 800; a missing weight is drawn as synthesized bold). `--f-hand` alone may be a stack of system faces that ends in a generic, with no web font (`theme.default`). `adp.py new` and `adp.py take` read the url from the entry. Without it the page falls back to system fonts. |

Tokens use the kit contract names, so kit files draw in the theme without aliases: `--bg --panel --sunk --ink --ink-2 --ink-3 --rule --rule-2 --accent --accent-ink`, the meanings (`--ok --warn --danger …`) and the four font tokens `--f-display`, `--f-ui`, `--f-mono` and `--f-hand` (the canvas). `Kit.tokens.contract(part)` lists the names a kit file reads. A theme that keeps its own names maps them in a second `:root` block (`theme.adr-drafting-table` sets `--f-ui: var(--f-body)`).

A layer theme adds to another one: `theme.glaze-depth` requires `theme.glaze`, sets no font token and has the same `fonts` as Glaze.

### One convention

The viewer can switch themes at run time, so every theme sets the same names. The convention has one source, `theme.default`: it sets every token a kit entry's header declares as required (`@tokens` without a trailing `?`), and every other theme's json sets every name the default's json sets, in light, and in dark wherever the default's dark map has it (colours and shadows). A theme may set more; the default sets only what is shared. That is the surfaces and inks, the accent with `--seam`, `--gold-leaf` and `--focus`, five meanings (`--ok --warn --danger --info --wait`) each with a `-soft` tint, six `--k-*` kinds, the canvas (`--canvas --dot`, six `--c-*` pens, four `--st-*` stickies, `--sticky-ink`), `--shadow`, the four font tokens, and the feel the templates read (`--outline --edge-w --text-size --leading --head-case --bg-image --bg-size`). `--radius` and `--radius-lg` are not in it: the templates and the kit fall back to different corners in different places, so the default cannot state one value without changing its look; a theme that sets them gets its own corners everywhere.

`tests/test_fonts.py` checks every theme: the convention above, the json `fonts` equals the entry `fonts`, the url loads the first family of every font token in the css and the json at 700 or more for the display and UI families, and the css and json agree on the font tokens. It also checks that the catalog page's own fonts (`--cat-f-*`) never reach into a preview stage.

## Wear a theme

### At `adp.py new`

    ADP new TEMPLATE DIR --theme <id> --catalog CATALOG

`--theme` takes the short name (`default`, `glaze`) or the entry id (`theme.glaze`); a name the catalog index does not have exits with the names it has, before anything is written. Without `--theme` the page wears `theme.default`, when the index has it: both forms give the same page. The publish object carries the theme's files by reference, and `index.html` gets two tags: the theme's font link before `styles/page.css`, and `kit/themes/<id>.css` after it (a theme is tokens only, so it overrides the template's placeholder tokens and leaves the page's rules alone). A theme that requires another (Glaze depth) brings that one's stylesheet too. The template's own font link stays.

The `assistant` and `default` templates also take every theme of the catalog (`theme.*` in their `take` list is every theme the index has, so a new theme needs no template edit) and `kit.skins`; `--theme` picks the one the page opens with.

`theme.default` is the look every page starts with, stated in full: every token the templates' own stylesheets set (`styles/page.css`, and the assistant's `styles/canvas.css` for the Canvas view) has the same value in the theme, and the font link is the theme's (`tests/test_fonts.py` keeps them equal). The templates keep those inline tokens as the fallback for a page with no theme file linked (no catalog index at `new`), so both look the same. A linked theme wins over page.css: for a palette of your own, set the tokens in page.css and remove the theme's link.

### Later: switch the theme of an existing page

1. `ADP take CATALOG theme.<new>` prints the `files` map and `fonts` (`{"theme.<new>": "<url>"}`).
2. In `index.html`, replace the old `kit/themes/<old>.css` link with the new one, still after `styles/page.css`, and replace the old theme's font link with the printed url, still before it.
3. Merge the `files` map into the page's publish, run `ADP check DIR` and publish.

### At runtime: let the viewer choose

`kit.skins` holds several looks in one page: `Kit.skins.init({skins: [{name, json: 'kit/themes/<id>.json'}, …]})`. A `json` skin uses the json's tokens and links its `fonts` when it is chosen. A skin given as `href` (a stylesheet) or `tokens` takes its font url as `fonts`. `modes: []` leaves `data-theme` to a page that keeps light and dark itself. `pattern.playground` links the json's `fonts` when its stage wears a theme.

The assistant and default templates do this out of the box (`parts/app.js`). The choices are the themes the page has installed (`installed.json`), Default first. The page's theme is the Settings value `look.theme`, whose default is the theme `index.html` links; the viewer's own pick, from the round button in the header, is kept in their browser and wins; changing `look.theme` drops that pick. The linked theme is switched off under any other, and the other is worn from its json alone (`kit.skins` is started again with that one theme's tokens, scoped to `data-skin`), so a theme replaces the one before and no token of the last one lingers, whichever sets more. The theme last worn is kept in the browser with its tokens, so the next visit wears it before any file arrives.

### Light and dark

These are separate from the theme. The `look.mode` setting (`auto`, `light`, `dark`) sets `data-theme` on `<html>` (`docs/config.md`), and the assistant's header button overrides it for one viewer. Each theme answers through its three blocks.

## Change the rest of the UI

- `styles/page.css` is the page's own look. Keep the token names, the three theme blocks and the selectors `adp.js` and the settings pattern rely on (`.wc*`, `.gear`, `.settings-view`, `.muted`). Write the layout, type scale and surfaces for the page's content.
- Every font declaration in a page or kit stylesheet takes `var(--f-ui)`, `var(--f-display)`, `var(--f-mono)` or `var(--f-hand)`, or `inherit`. Never a family name. That way a theme's fonts reach every element (`tests/test_fonts.py`).
- Layouts, patterns and components come from the catalog: use `--layout ID` at `new`, or `ADP take` plus the tags in step 4 of `plugins/artifacts-done-properly/skills/adp-catalog/SKILL.md`.

## Add a theme to the catalog

1. Write `plugins/artifacts-done-properly/skills/adp/catalog/kit/themes/<id>.css` (the three blocks, contract names, the header with `@id theme.<id>`, `@kind theme`, `@group Themes`, `@files kit/themes/<id>.json`, `@fonts` with the font url (the tags are in `docs/catalog-header.md`), `@requires` (`none`, or the base theme for a layer) and `@preview` with `"render": "theme.<id>"`) and `<id>.json` (the same tokens in `light` and `dark`, plus `fonts`).
2. Run `python3 plugins/artifacts-done-properly/skills/adp/scripts/adp_catalog.py build`: it writes the entry into `plugins/artifacts-done-properly/skills/adp/catalog/catalog.json` from the header (the fields every entry has, `docs/architecture.md` section 7: both files with `sha256` and `bytes`, `fonts`, `requires`, the entry `hash`). Nothing is added to `catalog.json` by hand.
3. Set every token `theme.default` sets (section "One convention"); the test names what is missing. No template lists themes and no test pins a count: the assistant and default templates take `theme.*`.
4. For the catalog page's preview, register `P['theme.<id>']` in `plugins/artifacts-done-properly/skills/adp/catalog/parts/`. The list at the end of `previews-b8.js` gives a theme the shared preview, which also loads its fonts.
5. Run `python3 plugins/artifacts-done-properly/skills/adp/scripts/adp_catalog.py` (it checks the headers too) and `python3 -m unittest discover -s tests`.
6. Publishing the catalog artifact is the owner's step (`docs/RELEASING.md`, "Publish the catalog": the kit files wait in proposals that the catalog page applies itself when an editor opens it). Pages built against the live catalog get the new entry, and its `fonts`, only after that publish and Apply.
