# Example: a kit entry (accessible tabs)

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

**Write your own entry** by putting the same header at the top of the main file, naming the other files in `@files`, and listing the
tokens you draw with. See [catalog header](../catalog-header.md).

More kit examples (themes, layouts such as `app-shell`, `doc-shell` and `topbar`, patterns, visualisations, samples) are in the project
repository: https://github.com/fblgit/artifacts-done-properly, `plugins/artifacts-done-properly/skills/adp/catalog/kit/`.
