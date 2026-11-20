# Example: a theme (tokens only)

A theme is a catalog entry `theme.<id>` with a stylesheet that sets tokens in three blocks, and a JSON file with the same values. Full rules:
[themes](../themes.md).

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
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #14130f; --panel: #1c1a15; --sunk: #100f0b; --ink: #ece8dc; /* ...every token again... */
  }
}
:root[data-theme="dark"] {
  --bg: #14130f; --panel: #1c1a15; --sunk: #100f0b; --ink: #ece8dc; /* ...the same values as the block above... */
}
```

Every theme sets the same token names, so a viewer can switch themes at run time. The values above are illustrative; the catalog's
`theme.default` is the reference for which names are required.

More themes are in the project repository, `plugins/artifacts-done-properly/skills/adp/catalog/kit/themes/`.
