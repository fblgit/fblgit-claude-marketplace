# Vectors: adp-catalog

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-rebuild](../adp-rebuild/SKILL.md) reads them; they are run against the tools assembled from the fragments.

## Contract: a catalog tree, `adp_catalog.py build` and the check

```json fixture
{
 "fixture": "catalog-a",
 "files": {
  "kit/badge.js": "/* part:page.script.kit.badge */\n/**\n * Status badge\n * Kit.badge.render(el, {label, tone}) draws a small label coloured by a meaning token; an empty label draws nothing.\n *\n * @id        kit.badge\n * @kind      component\n * @group     Board kit\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   A small label coloured by a meaning token.\n * @tags      badge, status, label\n * @requires  none\n * @files     kit/badge.css, kit/samples/kit.json\n * @provides  Kit.badge.render\n * @config    Kit.badge.render(el, opts) | label, tone (ok warn danger)\n * @tokens    --ok --warn --danger --f-ui\n * @globals   none\n * @db        none\n * @preview   {\"render\": \"kit.badge\", \"samples\": [\"kit/samples/kit.json#badge\"]}\n * @samples   badge\n */\n(function (root) {\n  const Kit = root.Kit = root.Kit || {};\n  Kit.badge = {render(el, o) { el.className = 'kit-badge ' + (o.tone || 'ok'); el.textContent = o.label || ''; return {destroy() { el.textContent = ''; }}; }};\n})(window);\n/* /part:page.script.kit.badge */\n",
  "kit/badge.css": "/* part:page.style.kit.badge */\n.kit-badge { font: 600 12px var(--f-ui); padding: 0 6px; border-radius: 9px; }\n.kit-badge.ok { color: var(--ok); } .kit-badge.warn { color: var(--warn); } .kit-badge.danger { color: var(--danger); }\n/* /part:page.style.kit.badge */\n",
  "kit/viz/meter.js": "/* part:page.script.kit.viz.meter */\n/**\n * Meter\n * Kit.meter.draw(el, {value, max, label}) draws a bar that states its value in words, with a badge for the tone it falls in.\n *\n * @id        viz.meter\n * @kind      component\n * @group     Visualizations\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   A bar that states its value and range in words, with a status badge.\n * @tags      meter, bar, progress, value\n * @requires  kit.badge\n * @files     kit/viz/meter.css, kit/samples/viz.json\n * @provides  Kit.meter.draw\n * @config    Kit.meter.draw(el, opts) | value, max, label\n * @tokens    --panel --ink --accent --f-ui\n * @globals   none\n * @db        none\n * @preview   {\"render\": \"viz.meter\", \"samples\": [\"kit/samples/viz.json#meter\"]}\n * @samples   meter\n */\n(function (root) {\n  const Kit = root.Kit;\n  Kit.meter = {draw(el, o) { const p = Math.round(100 * o.value / o.max); el.innerHTML = '<div class=\"kit-meter\"><i style=\"width:' + p + '%\"></i></div><span></span>'; el.lastChild.textContent = o.label + ': ' + o.value + ' of ' + o.max; Kit.badge.render(el.appendChild(document.createElement('b')), {label: p + '%', tone: p < 50 ? 'danger' : p < 80 ? 'warn' : 'ok'}); }};\n})(window);\n/* /part:page.script.kit.viz.meter */\n",
  "kit/viz/meter.css": "/* part:page.style.kit.viz.meter */\n.kit-meter { background: var(--panel); height: 8px; } .kit-meter i { display: block; height: 100%; background: var(--accent); }\n/* /part:page.style.kit.viz.meter */\n",
  "kit/themes/paper.css": "/* part:page.style.kit.theme.paper */\n/**\n * Paper\n * Warm paper by day, ink-blue by night; one green accent.\n *\n * @id        theme.paper\n * @kind      theme\n * @group     Themes\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   Warm paper by day, ink-blue by night, one green accent.\n * @tags      palette, tokens, dark mode, paper\n * @requires  none\n * @files     kit/themes/paper.json\n * @provides  none\n * @tokens    none\n * @globals   none\n * @fonts     https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\n * @db        none\n */\n:root { --bg: #fbfaf7; --panel: #ffffff; --ink: #1d1b16; --accent: #2f5d50; --ok: #2e7d4f; --warn: #8a5200; --danger: #b3261e; --f-ui: \"Inter\", system-ui, sans-serif; }\n@media (prefers-color-scheme: dark) { :root:not([data-theme=\"light\"]) { --bg: #14130f; --panel: #1c1a15; --ink: #ece8dc; --accent: #7fb8a4; --ok: #7fc79a; --warn: #e0b060; --danger: #f08a80; } }\n:root[data-theme=\"dark\"] { --bg: #14130f; --panel: #1c1a15; --ink: #ece8dc; --accent: #7fb8a4; --ok: #7fc79a; --warn: #e0b060; --danger: #f08a80; }\n/* /part:page.style.kit.theme.paper */\n",
  "kit/themes/paper.json": "{\n \"id\": \"paper\",\n \"name\": \"Paper\",\n \"about\": \"Warm paper by day, ink-blue by night; one green accent.\",\n \"source\": \"an example for this skill\",\n \"fonts\": \"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\",\n \"light\": {\n  \"--bg\": \"#fbfaf7\",\n  \"--panel\": \"#ffffff\",\n  \"--ink\": \"#1d1b16\",\n  \"--accent\": \"#2f5d50\",\n  \"--ok\": \"#2e7d4f\",\n  \"--warn\": \"#8a5200\",\n  \"--danger\": \"#b3261e\",\n  \"--f-ui\": \"\\\"Inter\\\", system-ui, sans-serif\"\n },\n \"dark\": {\n  \"--bg\": \"#14130f\",\n  \"--panel\": \"#1c1a15\",\n  \"--ink\": \"#ece8dc\",\n  \"--accent\": \"#7fb8a4\",\n  \"--ok\": \"#7fc79a\",\n  \"--warn\": \"#e0b060\",\n  \"--danger\": \"#f08a80\"\n }\n}\n",
  "kit/guides/reading.md": "<!--\nReading this catalog\nWhat each folder of the catalog holds and how a page takes an entry.\n\n@id        guide.reading\n@kind      guide\n@group     Guides\n@status    stable\n@version   0.1.0\n@updated   2026-11-20\n@summary   What each folder of this catalog holds and how a page takes an entry.\n@tags      guide, catalog, folders\n@requires  none\n@files     none\n@provides  none\n@tokens    none\n@globals   none\n@db        none\n-->\n\n# Reading this catalog\n\nComponents in `kit/`, charts in `kit/viz/`, themes in `kit/themes/`, sample data in `kit/samples/`. Take an entry with `adp.py take`.\n",
  "kit/samples/kit.json": "{\n \"badge\": {\n  \"note\": \"Invented labels.\",\n  \"typical\": {\n   \"label\": \"Passed\",\n   \"tone\": \"ok\"\n  },\n  \"warning\": {\n   \"label\": \"Late by two days\",\n   \"tone\": \"warn\"\n  },\n  \"empty\": {\n   \"label\": \"\",\n   \"tone\": \"danger\"\n  }\n }\n}\n",
  "kit/samples/viz.json": "{\n \"meter\": {\n  \"note\": \"Invented figures.\",\n  \"half\": {\n   \"value\": 5,\n   \"max\": 10,\n   \"label\": \"Kiln loads\"\n  },\n  \"full\": {\n   \"value\": 10,\n   \"max\": 10,\n   \"label\": \"Kiln loads\"\n  },\n  \"zero\": {\n   \"value\": 0,\n   \"max\": 3,\n   \"label\": \"Glaze tests\"\n  }\n }\n}\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-orphan",
 "base": "catalog-a",
 "files": {
  "kit/stray.js": "/* a kit file no entry names */\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-bad-header",
 "base": "catalog-a",
 "files": {
  "kit/badge.js": "/* part:page.script.kit.badge */\n/**\n * Status badge\n * Kit.badge.render(el, {label, tone}) draws a small label coloured by a meaning token; an empty label draws nothing.\n *\n * @id        kit.badge\n * @kind      component\n * @group     Board kit\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @tags      badge, status, label\n * @requires  none\n * @files     kit/badge.css, kit/samples/kit.json\n * @provides  Kit.badge.render\n * @config    Kit.badge.render(el, opts) | label, tone (ok warn danger)\n * @tokens    --ok --warn --danger --f-ui\n * @globals   none\n * @db        none\n * @preview   {\"render\": \"kit.badge\", \"samples\": [\"kit/samples/kit.json#badge\"]}\n * @samples   badge\n */\n(function (root) {\n  const Kit = root.Kit = root.Kit || {};\n  Kit.badge = {render(el, o) { el.className = 'kit-badge ' + (o.tone || 'ok'); el.textContent = o.label || ''; return {destroy() { el.textContent = ''; }}; }};\n})(window);\n/* /part:page.script.kit.badge */\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-unowned-sample",
 "base": "catalog-a",
 "files": {
  "kit/samples/kit.json": "{\n \"badge\": {\n  \"typical\": {\n   \"label\": \"Passed\"\n  }\n },\n \"nobody\": {\n  \"x\": 1\n }\n}\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-missing-require",
 "base": "catalog-a",
 "files": {
  "kit/badge.js": null,
  "kit/badge.css": null
 }
}
```

```json vector
{
 "vector": "catalog-build",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-a}"
 ],
 "exit": 0,
 "stdout_text": [
  "wrote <tmp>/catalog-a/catalog.json: 4 entries, 9 files"
 ],
 "files_out": {
  "{catalog-a}/catalog.json": {
   "schema": "kit-catalog/2",
   "url": "",
   "ver": "",
   "built": "<time>",
   "entries": [
    {
     "id": "kit.badge",
     "kind": "component",
     "group": "Board kit",
     "name": "Status badge",
     "summary": "A small label coloured by a meaning token.",
     "tags": [
      "badge",
      "status",
      "label"
     ],
     "status": "new",
     "version": "0.1.0",
     "requires": [],
     "globals": [],
     "provides": [
      "Kit.badge.render"
     ],
     "main": "kit/badge.js",
     "files": [
      {
       "path": "kit/badge.js",
       "role": "script",
       "sha256": "18ba1a867d82bc9e28b399fdc6a9fc306f6b79252d5d88f7d9035e681fa040ab",
       "bytes": 1024
      },
      {
       "path": "kit/badge.css",
       "role": "style",
       "sha256": "e36fc8a443380c6dea1dfad9be19b7c67d72c6e735d471c546115c182d00478c",
       "bytes": 264
      },
      {
       "path": "kit/samples/kit.json",
       "role": "sample",
       "sha256": "754630b80636553bc207c5aa66fd12263e9e2c344e55372c7ad61ad827c32ce8",
       "bytes": 230
      }
     ],
     "hash": "04fb713a8c9d"
    },
    {
     "id": "guide.reading",
     "kind": "guide",
     "group": "Guides",
     "name": "Reading this catalog",
     "summary": "What each folder of this catalog holds and how a page takes an entry.",
     "tags": [
      "guide",
      "catalog",
      "folders"
     ],
     "status": "stable",
     "version": "0.1.0",
     "requires": [],
     "globals": [],
     "provides": [],
     "main": "kit/guides/reading.md",
     "files": [
      {
       "path": "kit/guides/reading.md",
       "role": "doc",
       "sha256": "233f053024286515d3f6b87f9d3ace3f33871beadbe420ede60a78e8cbb78ac4",
       "bytes": 588
      }
     ],
     "hash": "37bcfff649f0"
    },
    {
     "id": "theme.paper",
     "kind": "theme",
     "group": "Themes",
     "name": "Paper",
     "summary": "Warm paper by day, ink-blue by night, one green accent.",
     "tags": [
      "palette",
      "tokens",
      "dark mode",
      "paper"
     ],
     "status": "new",
     "version": "0.1.0",
     "requires": [],
     "globals": [],
     "provides": [],
     "fonts": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
     "main": "kit/themes/paper.css",
     "files": [
      {
       "path": "kit/themes/paper.css",
       "role": "style",
       "sha256": "d69784ce8672c5ac5019d6d99eecd8aa488f2ed1c396c50035b0ac3808f7ca80",
       "bytes": 1146
      },
      {
       "path": "kit/themes/paper.json",
       "role": "data",
       "sha256": "1ce5d350bb6973a1bc6c4e3488171b0e55d848493c432ff741af55e3b2089306",
       "bytes": 643
      }
     ],
     "hash": "de7027176d74"
    },
    {
     "id": "viz.meter",
     "kind": "component",
     "group": "Visualizations",
     "name": "Meter",
     "summary": "A bar that states its value and range in words, with a status badge.",
     "tags": [
      "meter",
      "bar",
      "progress",
      "value"
     ],
     "status": "new",
     "version": "0.1.0",
     "requires": [
      "kit.badge"
     ],
     "globals": [],
     "provides": [
      "Kit.meter.draw"
     ],
     "main": "kit/viz/meter.js",
     "files": [
      {
       "path": "kit/viz/meter.js",
       "role": "script",
       "sha256": "efcf7c5c57ca8affb49a053292d5a29e7c1dbdbf402fa99909a03ed8d13fd37f",
       "bytes": 1262
      },
      {
       "path": "kit/viz/meter.css",
       "role": "style",
       "sha256": "3cbbbd327ce9f7de9c0284e73cddb355107a1b5fb31369301aadf318613e1c33",
       "bytes": 201
      },
      {
       "path": "kit/samples/viz.json",
       "role": "sample",
       "sha256": "c8af2a4b0d09926a10a953d1a2ffb00ff111b694ff6b0d9f43f62be1b7e4ddcc",
       "bytes": 263
      }
     ],
     "hash": "c53c2c95d630"
    }
   ]
  }
 }
}
```

```json vector
{
 "vector": "catalog-build-then-check",
 "steps": [
  {
   "run": [
    "adp_catalog.py",
    "build",
    "{catalog-a}"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp_catalog.py",
    "{catalog-a}"
   ],
   "exit": 0,
   "stdout_text": [
    "OK: 4 entries, 9 entry files, 10 files in tree, 0 orphans, all sizes, sha256 and hashes match, 4 valid headers"
   ]
  }
 ]
}
```

```json fixture
{
 "fixture": "catalog-built",
 "base": "catalog-a",
 "files": {
  "catalog.json": "{\n \"schema\": \"kit-catalog/2\",\n \"url\": \"\",\n \"ver\": \"\",\n \"built\": \"2026-11-20T00:00:00Z\",\n \"entries\": [\n  {\n   \"id\": \"kit.badge\",\n   \"kind\": \"component\",\n   \"group\": \"Board kit\",\n   \"name\": \"Status badge\",\n   \"summary\": \"A small label coloured by a meaning token.\",\n   \"tags\": [\n    \"badge\",\n    \"status\",\n    \"label\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [\n    \"Kit.badge.render\"\n   ],\n   \"main\": \"kit/badge.js\",\n   \"files\": [\n    {\n     \"path\": \"kit/badge.js\",\n     \"role\": \"script\",\n     \"sha256\": \"18ba1a867d82bc9e28b399fdc6a9fc306f6b79252d5d88f7d9035e681fa040ab\",\n     \"bytes\": 1024\n    },\n    {\n     \"path\": \"kit/badge.css\",\n     \"role\": \"style\",\n     \"sha256\": \"e36fc8a443380c6dea1dfad9be19b7c67d72c6e735d471c546115c182d00478c\",\n     \"bytes\": 264\n    },\n    {\n     \"path\": \"kit/samples/kit.json\",\n     \"role\": \"sample\",\n     \"sha256\": \"754630b80636553bc207c5aa66fd12263e9e2c344e55372c7ad61ad827c32ce8\",\n     \"bytes\": 230\n    }\n   ],\n   \"hash\": \"04fb713a8c9d\"\n  },\n  {\n   \"id\": \"guide.reading\",\n   \"kind\": \"guide\",\n   \"group\": \"Guides\",\n   \"name\": \"Reading this catalog\",\n   \"summary\": \"What each folder of this catalog holds and how a page takes an entry.\",\n   \"tags\": [\n    \"guide\",\n    \"catalog\",\n    \"folders\"\n   ],\n   \"status\": \"stable\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [],\n   \"main\": \"kit/guides/reading.md\",\n   \"files\": [\n    {\n     \"path\": \"kit/guides/reading.md\",\n     \"role\": \"doc\",\n     \"sha256\": \"233f053024286515d3f6b87f9d3ace3f33871beadbe420ede60a78e8cbb78ac4\",\n     \"bytes\": 588\n    }\n   ],\n   \"hash\": \"37bcfff649f0\"\n  },\n  {\n   \"id\": \"theme.paper\",\n   \"kind\": \"theme\",\n   \"group\": \"Themes\",\n   \"name\": \"Paper\",\n   \"summary\": \"Warm paper by day, ink-blue by night, one green accent.\",\n   \"tags\": [\n    \"palette\",\n    \"tokens\",\n    \"dark mode\",\n    \"paper\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [],\n   \"fonts\": \"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\",\n   \"main\": \"kit/themes/paper.css\",\n   \"files\": [\n    {\n     \"path\": \"kit/themes/paper.css\",\n     \"role\": \"style\",\n     \"sha256\": \"d69784ce8672c5ac5019d6d99eecd8aa488f2ed1c396c50035b0ac3808f7ca80\",\n     \"bytes\": 1146\n    },\n    {\n     \"path\": \"kit/themes/paper.json\",\n     \"role\": \"data\",\n     \"sha256\": \"1ce5d350bb6973a1bc6c4e3488171b0e55d848493c432ff741af55e3b2089306\",\n     \"bytes\": 643\n    }\n   ],\n   \"hash\": \"de7027176d74\"\n  },\n  {\n   \"id\": \"viz.meter\",\n   \"kind\": \"component\",\n   \"group\": \"Visualizations\",\n   \"name\": \"Meter\",\n   \"summary\": \"A bar that states its value and range in words, with a status badge.\",\n   \"tags\": [\n    \"meter\",\n    \"bar\",\n    \"progress\",\n    \"value\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [\n    \"kit.badge\"\n   ],\n   \"globals\": [],\n   \"provides\": [\n    \"Kit.meter.draw\"\n   ],\n   \"main\": \"kit/viz/meter.js\",\n   \"files\": [\n    {\n     \"path\": \"kit/viz/meter.js\",\n     \"role\": \"script\",\n     \"sha256\": \"efcf7c5c57ca8affb49a053292d5a29e7c1dbdbf402fa99909a03ed8d13fd37f\",\n     \"bytes\": 1262\n    },\n    {\n     \"path\": \"kit/viz/meter.css\",\n     \"role\": \"style\",\n     \"sha256\": \"3cbbbd327ce9f7de9c0284e73cddb355107a1b5fb31369301aadf318613e1c33\",\n     \"bytes\": 201\n    },\n    {\n     \"path\": \"kit/samples/viz.json\",\n     \"role\": \"sample\",\n     \"sha256\": \"c8af2a4b0d09926a10a953d1a2ffb00ff111b694ff6b0d9f43f62be1b7e4ddcc\",\n     \"bytes\": 263\n    }\n   ],\n   \"hash\": \"c53c2c95d630\"\n  }\n ]\n}\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-stale",
 "base": "catalog-a",
 "files": {
  "catalog.json": "{\n \"schema\": \"kit-catalog/2\",\n \"url\": \"\",\n \"ver\": \"\",\n \"built\": \"2026-11-20T00:00:00Z\",\n \"entries\": [\n  {\n   \"id\": \"kit.badge\",\n   \"kind\": \"component\",\n   \"group\": \"Board kit\",\n   \"name\": \"Status badge\",\n   \"summary\": \"A small label coloured by a meaning token.\",\n   \"tags\": [\n    \"badge\",\n    \"status\",\n    \"label\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [\n    \"Kit.badge.render\"\n   ],\n   \"main\": \"kit/badge.js\",\n   \"files\": [\n    {\n     \"path\": \"kit/badge.js\",\n     \"role\": \"script\",\n     \"sha256\": \"18ba1a867d82bc9e28b399fdc6a9fc306f6b79252d5d88f7d9035e681fa040ab\",\n     \"bytes\": 1024\n    },\n    {\n     \"path\": \"kit/badge.css\",\n     \"role\": \"style\",\n     \"sha256\": \"e36fc8a443380c6dea1dfad9be19b7c67d72c6e735d471c546115c182d00478c\",\n     \"bytes\": 264\n    },\n    {\n     \"path\": \"kit/samples/kit.json\",\n     \"role\": \"sample\",\n     \"sha256\": \"754630b80636553bc207c5aa66fd12263e9e2c344e55372c7ad61ad827c32ce8\",\n     \"bytes\": 230\n    }\n   ],\n   \"hash\": \"04fb713a8c9d\"\n  },\n  {\n   \"id\": \"guide.reading\",\n   \"kind\": \"guide\",\n   \"group\": \"Guides\",\n   \"name\": \"Reading this catalog\",\n   \"summary\": \"What each folder of this catalog holds and how a page takes an entry.\",\n   \"tags\": [\n    \"guide\",\n    \"catalog\",\n    \"folders\"\n   ],\n   \"status\": \"stable\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [],\n   \"main\": \"kit/guides/reading.md\",\n   \"files\": [\n    {\n     \"path\": \"kit/guides/reading.md\",\n     \"role\": \"doc\",\n     \"sha256\": \"233f053024286515d3f6b87f9d3ace3f33871beadbe420ede60a78e8cbb78ac4\",\n     \"bytes\": 588\n    }\n   ],\n   \"hash\": \"37bcfff649f0\"\n  },\n  {\n   \"id\": \"theme.paper\",\n   \"kind\": \"theme\",\n   \"group\": \"Themes\",\n   \"name\": \"Paper\",\n   \"summary\": \"Warm paper by day, ink-blue by night, one green accent.\",\n   \"tags\": [\n    \"palette\",\n    \"tokens\",\n    \"dark mode\",\n    \"paper\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [],\n   \"fonts\": \"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\",\n   \"main\": \"kit/themes/paper.css\",\n   \"files\": [\n    {\n     \"path\": \"kit/themes/paper.css\",\n     \"role\": \"style\",\n     \"sha256\": \"d69784ce8672c5ac5019d6d99eecd8aa488f2ed1c396c50035b0ac3808f7ca80\",\n     \"bytes\": 1146\n    },\n    {\n     \"path\": \"kit/themes/paper.json\",\n     \"role\": \"data\",\n     \"sha256\": \"1ce5d350bb6973a1bc6c4e3488171b0e55d848493c432ff741af55e3b2089306\",\n     \"bytes\": 643\n    }\n   ],\n   \"hash\": \"de7027176d74\"\n  },\n  {\n   \"id\": \"viz.meter\",\n   \"kind\": \"component\",\n   \"group\": \"Visualizations\",\n   \"name\": \"Meter\",\n   \"summary\": \"A bar that states its value and range in words, with a status badge.\",\n   \"tags\": [\n    \"meter\",\n    \"bar\",\n    \"progress\",\n    \"value\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [\n    \"kit.badge\"\n   ],\n   \"globals\": [],\n   \"provides\": [\n    \"Kit.meter.draw\"\n   ],\n   \"main\": \"kit/viz/meter.js\",\n   \"files\": [\n    {\n     \"path\": \"kit/viz/meter.js\",\n     \"role\": \"script\",\n     \"sha256\": \"efcf7c5c57ca8affb49a053292d5a29e7c1dbdbf402fa99909a03ed8d13fd37f\",\n     \"bytes\": 1262\n    },\n    {\n     \"path\": \"kit/viz/meter.css\",\n     \"role\": \"style\",\n     \"sha256\": \"3cbbbd327ce9f7de9c0284e73cddb355107a1b5fb31369301aadf318613e1c33\",\n     \"bytes\": 201\n    },\n    {\n     \"path\": \"kit/samples/viz.json\",\n     \"role\": \"sample\",\n     \"sha256\": \"c8af2a4b0d09926a10a953d1a2ffb00ff111b694ff6b0d9f43f62be1b7e4ddcc\",\n     \"bytes\": 263\n    }\n   ],\n   \"hash\": \"c53c2c95d630\"\n  }\n ]\n}\n",
  "kit/badge.css": "/* part:page.style.kit.badge */\n.kit-badge { font: 600 12px var(--f-ui); padding: 0 8px; border-radius: 9px; }\n.kit-badge.ok { color: var(--ok); } .kit-badge.warn { color: var(--warn); } .kit-badge.danger { color: var(--danger); }\n/* /part:page.style.kit.badge */\n"
 }
}
```

```json vector
{
 "vector": "catalog-check-passes-a-built-tree",
 "run": [
  "adp_catalog.py",
  "{catalog-built}"
 ],
 "exit": 0,
 "stdout_text": [
  "OK: 4 entries, 9 entry files, 10 files in tree, 0 orphans, all sizes, sha256 and hashes match, 4 valid headers"
 ],
 "stderr_text": []
}
```

```json vector
{
 "vector": "catalog-check-catches-a-file-edited-after-build",
 "run": [
  "adp_catalog.py",
  "{catalog-stale}"
 ],
 "exit": 1,
 "stdout_text": [
  "FAIL: 3 problem(s)",
  "  kit.badge: sha256 kit/badge.css: file 67f45c9d03c24d44a67f81414d063629b3a7d2d8cfa11d48659955f3abbe3b6d != entry e36fc8a443380c6dea1dfad9be19b7c67d72c6e735d471c546115c182d00478c",
  "  catalog.json: kit.badge.files[kit/badge.css]: sha256 differ",
  "  catalog.json: kit.badge.hash: on disk \"04fb713a8c9d\", built \"e95bca96c3bb\""
 ],
 "stderr_text": []
}
```

```json vector
{
 "vector": "catalog-refuses-an-orphan",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-orphan}"
 ],
 "exit": 1,
 "files_out": {
  "{catalog-orphan}/catalog.json": null
 },
 "stderr_text": [
  "1 problem(s); catalog.json is not written:",
  "  kit/stray.js: no entry names it (add it to @files in the header of its entry)"
 ]
}
```

The fixture `catalog-unreadable` is a built catalog with one more file under `kit/` that cannot be read (a link to nothing). It has no header, so
`build` and the check list it as a file no entry names:

```json fixture
{
 "fixture": "catalog-unreadable",
 "base": "catalog-built",
 "files": {
  "kit/gone.js": {"link": "nowhere.js"}
 }
}
```

```json vector
{
 "vector": "catalog-lists-an-unreadable-file",
 "steps": [
  {
   "run": [
    "adp_catalog.py",
    "build",
    "{catalog-unreadable}"
   ],
   "exit": 1,
   "stderr_text": [
    "1 problem(s); catalog.json is not written:",
    "  kit/gone.js: no entry names it (add it to @files in the header of its entry)"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "{catalog-unreadable}"
   ],
   "exit": 1,
   "stdout_text": [
    "FAIL: 1 problem(s)",
    "  tree: kit/gone.js: no entry names it (add it to @files in the header of its entry)"
   ]
  }
 ]
}
```

A header line that starts with `@` but is indented continues the tag above it; it does not begin a tag:

```json fixture
{
 "fixture": "catalog-continued-tag",
 "files": {
  "kit/a.js": "/**\n * A\n * Draws a.\n *\n * @id        kit.a\n * @kind      component\n * @group     Board kit\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-21\n * @summary   Draws a.\n * @tags      a\n * @requires  none\n * @files     none\n * @provides  Kit.a\n * @globals   none\n * @db        none\n * @config    size\n *            @see next\n */\n"
 }
}
```

```json vector
{
 "vector": "catalog-an-indented-at-line-continues-the-tag",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-continued-tag}"
 ],
 "exit": 1,
 "stderr_text": [
  "1 problem(s); catalog.json is not written:",
  "  kit.a: kit/a.js: [config] @config size @see next: \"signature | what it takes\""
 ]
}
```

The header of the runtime itself is a catalog header like any other (`runtime.adp`, the file `adp.js` at the top of the catalog); the fixture holds the built `adp.js`:

```json fixture
{
 "fixture": "catalog-runtime",
 "files": {
  "kit/.keep": "",
  "adp.js": "{adp.js}"
 }
}
```

```json vector
{
 "vector": "catalog-accepts-the-runtime-header",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-runtime}"
 ],
 "exit": 0,
 "stdout_text": [
  "wrote <tmp>/catalog-runtime/catalog.json: 1 entries, 1 files"
 ],
 "stderr_text": []
}
```

```json vector
{
 "vector": "catalog-refuses-a-bad-header",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-bad-header}"
 ],
 "exit": 1,
 "stderr_text": [
  "1 problem(s); catalog.json is not written:",
  "  kit.badge: kit/badge.js: [missing-tag] @summary is required"
 ]
}
```

```json vector
{
 "vector": "catalog-refuses-an-unowned-sample",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-unowned-sample}"
 ],
 "exit": 1,
 "stderr_text": [
  "2 problem(s); catalog.json is not written:",
  "  kit/samples/kit.json: the key nobody is named by no entry's @preview",
  "  kit/samples/kit.json: the key nobody is owned by no entry's @samples"
 ]
}
```

```json vector
{
 "vector": "catalog-refuses-a-missing-require",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-missing-require}"
 ],
 "exit": 1,
 "stderr_text": [
  "2 problem(s); catalog.json is not written:",
  "  viz.meter: @requires names no entry: kit.badge",
  "  kit/samples/kit.json: no entry names it (add it to @files in the header of its entry)"
 ]
}
```

```json fixture
{
 "fixture": "catalog-bad-rules",
 "base": "catalog-a",
 "files": {
  "kit/badge.js": "/* part:page.script.kit.badge */\n/**\n * Status badge\n * Kit.badge.render(el, {label, tone}) draws a small label coloured by a meaning token; an empty label draws nothing.\n *\n * @id        kit.badge\n * @kind      widget\n * @group     Board kit\n * @status    wip\n * @version   1.0\n * @updated   yesterday\n * @summary   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n * @tags      Badge, badge, badge\n * @requires  none\n * @files     kit/badge.css, kit/samples/kit.json\n * @provides  1bad\n * @config    oops\n * @tokens    ink\n * @globals   jquery\n * @db        read x\n * @preview   not json\n * @bogus     one\n * @source    one | two\n * @changed   a\n * @changed   b\n * @status    new\n * @samples   badge, badge\n */\n(function (root) {\n  const Kit = root.Kit = root.Kit || {};\n  Kit.badge = {render(el, o) { el.className = 'kit-badge ' + (o.tone || 'ok'); el.textContent = o.label || ''; return {destroy() { el.textContent = ''; }}; }};\n})(window);\n/* /part:page.script.kit.badge */\n",
  "kit/viz/meter.js": "/* part:page.script.kit.viz.meter */\n/**\n * @id        viz.meter\n * @kind      component\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   A bar that states its value and range in words, with a status badge.\n * @tags      meter, bar, progress, value\n * @requires  kit.badge\n * @files     kit/viz/meter.css, kit/samples/viz.json\n * @provides  Kit.meter.draw\n * @config    Kit.meter.draw(el, opts) | value, max, label\n * @tokens    --panel --ink --accent --f-ui\n * @globals   none\n * @preview   {\"render\": \"viz.meter\", \"samples\": [\"kit/samples/viz.json#meter\"]}\n * @samples   meter\n */\n(function (root) {\n  const Kit = root.Kit;\n  Kit.meter = {draw(el, o) { const p = Math.round(100 * o.value / o.max); el.innerHTML = '<div class=\"kit-meter\"><i style=\"width:' + p + '%\"></i></div><span></span>'; el.lastChild.textContent = o.label + ': ' + o.value + ' of ' + o.max; Kit.badge.render(el.appendChild(document.createElement('b')), {label: p + '%', tone: p < 50 ? 'danger' : p < 80 ? 'warn' : 'ok'}); }};\n})(window);\n/* /part:page.script.kit.viz.meter */\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-bad-files",
 "base": "catalog-a",
 "files": {
  "kit/viz/meter.js": "/* part:page.script.kit.viz.meter */\n/**\n * Meter\n * Kit.meter.draw(el, {value, max, label}) draws a bar that states its value in words, with a badge for the tone it falls in.\n *\n * @id        viz.meter\n * @kind      component\n * @group     Visualizations\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   A bar that states its value and range in words, with a status badge.\n * @tags      meter, bar, progress, value\n * @requires  kit.badge\n * @files     kit/viz/meter.js, kit/viz/meter.css, kit/viz/meter.css, ../x.js, kit/nothing.css, kit/badge.js, kit/samples/viz.json\n * @provides  Kit.meter.draw\n * @config    Kit.meter.draw(el, opts) | value, max, label\n * @tokens    --panel --ink --accent --f-ui\n * @globals   none\n * @db        none\n * @preview   {\"render\": \"viz.meter\", \"samples\": [\"kit/samples/viz.json#meter\"]}\n * @samples   meter\n */\n(function (root) {\n  const Kit = root.Kit;\n  Kit.meter = {draw(el, o) { const p = Math.round(100 * o.value / o.max); el.innerHTML = '<div class=\"kit-meter\"><i style=\"width:' + p + '%\"></i></div><span></span>'; el.lastChild.textContent = o.label + ': ' + o.value + ' of ' + o.max; Kit.badge.render(el.appendChild(document.createElement('b')), {label: p + '%', tone: p < 50 ? 'danger' : p < 80 ? 'warn' : 'ok'}); }};\n})(window);\n/* /part:page.script.kit.viz.meter */\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-bad-samples",
 "base": "catalog-a",
 "files": {
  "kit/badge.js": "/* part:page.script.kit.badge */\n/**\n * Status badge\n * Kit.badge.render(el, {label, tone}) draws a small label coloured by a meaning token; an empty label draws nothing.\n *\n * @id        kit.badge\n * @kind      component\n * @group     Board kit\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   A small label coloured by a meaning token.\n * @tags      badge, status, label\n * @requires  none\n * @files     kit/badge.css, kit/samples/kit.json\n * @provides  Kit.badge.render\n * @config    Kit.badge.render(el, opts) | label, tone (ok warn danger)\n * @tokens    --ok --warn --danger --f-ui\n * @globals   none\n * @db        none\n * @preview   {\"render\": \"kit.badge\", \"samples\": [\"kit/samples/kit.json#missing\", \"kit/samples/viz.json#meter\", \"kit/other.json#x\"]}\n * @samples   badge, ghost\n */\n(function (root) {\n  const Kit = root.Kit = root.Kit || {};\n  Kit.badge = {render(el, o) { el.className = 'kit-badge ' + (o.tone || 'ok'); el.textContent = o.label || ''; return {destroy() { el.textContent = ''; }}; }};\n})(window);\n/* /part:page.script.kit.badge */\n",
  "kit/samples/viz.json": "{\n \"meter\": {\n  \"half\": {}\n },\n \"spare\": {\n  \"x\": 1\n }\n}\n"
 }
}
```

```json fixture
{
 "fixture": "catalog-stale-index",
 "base": "catalog-built",
 "files": {
  "catalog.json": "{\n \"schema\": \"kit-catalog/2\",\n \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000002\",\n \"ver\": \"\",\n \"built\": \"2026-11-20T00:00:00Z\",\n \"entries\": [\n  {\n   \"id\": \"kit.ghost\",\n   \"kind\": \"guide\",\n   \"group\": \"Guides\",\n   \"name\": \"Reading this catalog\",\n   \"summary\": \"What each folder of this catalog holds and how a page takes an entry.\",\n   \"tags\": [\n    \"guide\",\n    \"catalog\",\n    \"folders\"\n   ],\n   \"status\": \"stable\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [],\n   \"main\": \"kit/guides/reading.md\",\n   \"files\": [\n    {\n     \"path\": \"kit/guides/reading.md\",\n     \"role\": \"doc\",\n     \"sha256\": \"233f053024286515d3f6b87f9d3ace3f33871beadbe420ede60a78e8cbb78ac4\",\n     \"bytes\": 588\n    }\n   ],\n   \"hash\": \"37bcfff649f0\"\n  },\n  {\n   \"id\": \"kit.badge\",\n   \"kind\": \"component\",\n   \"name\": \"Status badge\",\n   \"summary\": \"A small label coloured by a meaning token.\",\n   \"tags\": [\n    \"badge\",\n    \"status\",\n    \"label\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [\n    \"Kit.badge.render\"\n   ],\n   \"main\": \"kit/badge.js\",\n   \"files\": [\n    {\n     \"path\": \"kit/samples/kit.json\",\n     \"role\": \"sample\",\n     \"sha256\": \"754630b80636553bc207c5aa66fd12263e9e2c344e55372c7ad61ad827c32ce8\",\n     \"bytes\": 230\n    },\n    {\n     \"path\": \"kit/badge.css\",\n     \"role\": \"style\",\n     \"sha256\": \"e36fc8a443380c6dea1dfad9be19b7c67d72c6e735d471c546115c182d00478c\",\n     \"bytes\": 264\n    },\n    {\n     \"path\": \"kit/badge.js\",\n     \"role\": \"script\",\n     \"sha256\": \"18ba1a867d82bc9e28b399fdc6a9fc306f6b79252d5d88f7d9035e681fa040ab\",\n     \"bytes\": 1024\n    }\n   ],\n   \"hash\": \"04fb713a8c9d\",\n   \"extra\": 1\n  },\n  {\n   \"id\": \"theme.paper\",\n   \"kind\": \"theme\",\n   \"group\": \"Themes\",\n   \"name\": \"Paper\",\n   \"summary\": \"Warm paper by day, ink-blue by night, one green accent.\",\n   \"tags\": [\n    \"palette\",\n    \"tokens\",\n    \"dark mode\",\n    \"paper\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.1.0\",\n   \"requires\": [],\n   \"globals\": [],\n   \"provides\": [],\n   \"fonts\": \"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\",\n   \"main\": \"kit/themes/paper.css\",\n   \"files\": [\n    {\n     \"path\": \"kit/themes/paper.css\",\n     \"role\": \"style\",\n     \"sha256\": \"d69784ce8672c5ac5019d6d99eecd8aa488f2ed1c396c50035b0ac3808f7ca80\",\n     \"bytes\": 1146\n    },\n    {\n     \"path\": \"kit/themes/paper.json\",\n     \"role\": \"data\",\n     \"sha256\": \"1ce5d350bb6973a1bc6c4e3488171b0e55d848493c432ff741af55e3b2089306\",\n     \"bytes\": 643\n    }\n   ]\n  },\n  {\n   \"id\": \"viz.meter\",\n   \"kind\": \"component\",\n   \"group\": \"Visualizations\",\n   \"name\": \"Meter\",\n   \"summary\": \"A bar that states its value and range in words, with a status badge.\",\n   \"tags\": [\n    \"meter\",\n    \"bar\",\n    \"progress\",\n    \"value\"\n   ],\n   \"status\": \"new\",\n   \"version\": \"0.2.0\",\n   \"requires\": [\n    \"kit.badge\"\n   ],\n   \"globals\": [],\n   \"provides\": [\n    \"Kit.meter.draw\"\n   ],\n   \"main\": \"kit/viz/meter.js\",\n   \"files\": [\n    {\n     \"path\": \"kit/viz/meter.js\",\n     \"role\": \"script\",\n     \"sha256\": \"efcf7c5c57ca8affb49a053292d5a29e7c1dbdbf402fa99909a03ed8d13fd37f\",\n     \"bytes\": 1262\n    },\n    {\n     \"path\": \"kit/viz/meter.css\",\n     \"role\": \"style\",\n     \"sha256\": \"3cbbbd327ce9f7de9c0284e73cddb355107a1b5fb31369301aadf318613e1c33\",\n     \"bytes\": 1\n    },\n    {\n     \"path\": \"kit/samples/viz.json\",\n     \"role\": \"sample\",\n     \"sha256\": \"c8af2a4b0d09926a10a953d1a2ffb00ff111b694ff6b0d9f43f62be1b7e4ddcc\",\n     \"bytes\": 263\n    }\n   ],\n   \"hash\": \"c53c2c95d630\"\n  }\n ]\n}\n",
  "kit/stray.js": "/* no entry */\n",
  "kit/themes/paper.json": null
 }
}
```

```json fixture
{
 "fixture": "catalog-header-drift",
 "base": "catalog-built",
 "files": {
  "kit/badge.js": "/* part:page.script.kit.badge */\n/**\n * Status badge\n * Kit.badge.render(el, {label, tone}) draws a small label coloured by a meaning token; an empty label draws nothing.\n *\n * @id        nope.badge\n * @kind      component\n * @group     Board kit\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   A small label coloured by a meaning token.\n * @tags      badge, status, label\n * @requires  none\n * @files     kit/badge.css, kit/samples/kit.json\n * @provides  Kit.badge.render\n * @config    Kit.badge.render(el, opts) | label, tone (ok warn danger)\n * @tokens    --ok --warn --danger --f-ui\n * @globals   none\n * @db        none\n * @preview   {\"render\": \"kit.badge\", \"samples\": [\"kit/samples/kit.json#badge\"]}\n * @samples   badge\n */\n(function (root) {\n  const Kit = root.Kit = root.Kit || {};\n  Kit.badge = {render(el, o) { el.className = 'kit-badge ' + (o.tone || 'ok'); el.textContent = o.label || ''; return {destroy() { el.textContent = ''; }}; }};\n})(window);\n/* /part:page.script.kit.badge */\n",
  "kit/guides/reading.md": "Reading this catalog, with no header.\n",
  "kit/themes/paper.css": null
 }
}
```

```json vector
{
 "vector": "catalog-header-rules",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-bad-rules}"
 ],
 "exit": 1,
 "stderr_text": [
  "23 problem(s); catalog.json is not written:",
  "  kit.badge: kit/badge.js: [unknown-tag] @bogus is not a header tag",
  "  kit.badge: kit/badge.js: [duplicate-tag] @status appears twice",
  "  kit.badge: kit/badge.js: [status] @status wip: one of new, stable",
  "  kit.badge: kit/badge.js: [version] @version 1.0: major.minor.patch",
  "  kit.badge: kit/badge.js: [updated] @updated yesterday: YYYY-MM-DD",
  "  kit.badge: kit/badge.js: [summary] @summary is 300 characters, at most 260",
  "  kit.badge: kit/badge.js: [kind] @kind widget: one of component, guide, template, theme",
  "  kit.badge: kit/badge.js: [db] @db: sections `reads a; b` / `writes c` / `note text`, keywords in lowercase; not: read x",
  "  kit.badge: kit/badge.js: [preview] @preview is not one line of JSON",
  "  kit.badge: kit/badge.js: [samples] @samples: a comma list of bundle keys (letters, digits, . _ -), no repeats",
  "  kit.badge: kit/badge.js: [changed] @changed appears once: the newest change",
  "  kit.badge: kit/badge.js: [tags] @tags: a comma list, lowercase, no repeats",
  "  kit.badge: kit/badge.js: [provides] @provides: dotted names, comma separated; not: 1bad",
  "  kit.badge: kit/badge.js: [tokens] @tokens: custom properties like --ink (--ink? when optional); not: ink",
  "  kit.badge: kit/badge.js: [globals] @globals: none or dompurify, htm-preact, marked; not: jquery",
  "  kit.badge: kit/badge.js: [config] @config oops: \"signature | what it takes\"",
  "  kit.badge: kit/badge.js: [source] @source one | two: \"board | file | what\"",
  "  viz.meter: kit/viz/meter.js: [title] the first line of the comment is the entry name",
  "  viz.meter: kit/viz/meter.js: [about] a paragraph after the name says what the entry is",
  "  viz.meter: kit/viz/meter.js: [missing-tag] @group is required",
  "  viz.meter: kit/viz/meter.js: [missing-tag] @db is required",
  "  kit.badge: @samples names badge, which is a key of no sample bundle in its @files",
  "  kit.badge: @samples names badge, which is a key of no sample bundle in its @files"
 ]
}
```

```json vector
{
 "vector": "catalog-refuses-bad-files",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-bad-files}"
 ],
 "exit": 1,
 "stderr_text": [
  "5 problem(s); catalog.json is not written:",
  "  viz.meter: @files names kit/viz/meter.js, the main file itself; name the other files only",
  "  viz.meter: @files names kit/viz/meter.css twice",
  "  viz.meter: @files names ../x.js, which is not a path inside the catalog folder",
  "  viz.meter: @files names kit/nothing.css, which is not in the tree",
  "  viz.meter: @files names kit/badge.js, which carries the header of kit.badge; name that entry in @requires"
 ]
}
```

```json vector
{
 "vector": "catalog-refuses-bad-samples",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-bad-samples}"
 ],
 "exit": 1,
 "stderr_text": [
  "7 problem(s); catalog.json is not written:",
  "  kit.badge: @preview names kit/samples/kit.json#missing, but kit/samples/kit.json has no key missing",
  "  kit.badge: @preview names kit/samples/viz.json#meter, but kit/samples/viz.json is not a sample file in its @files",
  "  kit.badge: @preview names kit/other.json#x, but kit/other.json is not a sample file in its @files",
  "  kit/samples/kit.json: the key badge is named by no entry's @preview",
  "  kit/samples/viz.json: the key spare is named by no entry's @preview",
  "  kit.badge: @samples names ghost, which is a key of no sample bundle in its @files",
  "  kit/samples/viz.json: the key spare is owned by no entry's @samples"
 ]
}
```

```json vector
{
 "vector": "catalog-check-catches-a-stale-index",
 "run": [
  "adp_catalog.py",
  "{catalog-stale-index}"
 ],
 "exit": 1,
 "stdout_text": [
  "FAIL: 16 problem(s)",
  "  theme.paper: missing file kit/themes/paper.json",
  "  theme.paper: entry has no hash",
  "  viz.meter: size kit/viz/meter.css: file 201 != bytes 1",
  "  orphan: kit/stray.js is not referenced by any entry or page file",
  "  header kit/guides/reading.md: [id-mismatch] @id guide.reading but catalog.json lists this file under kit.ghost",
  "  tree: theme.paper: @files names kit/themes/paper.json, which is not in the tree",
  "  tree: kit/stray.js: no entry names it (add it to @files in the header of its entry)",
  "  catalog.json: guide.reading: a header in the tree, no entry in catalog.json",
  "  catalog.json: kit.ghost: an entry in catalog.json without a header in the tree",
  "  catalog.json: kit.badge.extra: on disk, not part of the built index",
  "  catalog.json: kit.badge.files: in a different order",
  "  catalog.json: kit.badge.group: missing on disk; built \"Board kit\"",
  "  catalog.json: theme.paper.files: kit/themes/paper.json is on disk, not built",
  "  catalog.json: theme.paper.hash: missing on disk; built \"347ce181b54c\"",
  "  catalog.json: viz.meter.files[kit/viz/meter.css]: bytes differ",
  "  catalog.json: viz.meter.version: on disk \"0.2.0\", built \"0.1.0\""
 ]
}
```

```json vector
{
 "vector": "catalog-headers-command",
 "steps": [
  {
   "run": [
    "adp_catalog.py",
    "headers",
    "--root",
    "{catalog-built}"
   ],
   "exit": 0,
   "stdout_text": [
    "ok: 4 header(s) valid, 0 skipped"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "headers",
    "--root",
    "{catalog-header-drift}"
   ],
   "exit": 1,
   "stdout_text": [
    "kit/badge.js: [id] @id nope.badge: kind.name with kind one of guide, kit, layout, pattern, runtime, template, theme, viz",
    "kit/badge.js: [id-mismatch] @id nope.badge but catalog.json lists this file under kit.badge",
    "kit/guides/reading.md: [legacy] no @id header",
    "kit/themes/paper.css: [missing-file] catalog.json lists kit/themes/paper.css for theme.paper but the file is not there"
   ],
   "stderr_text": [
    "3 file(s) with problems"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "headers",
    "--root",
    "{catalog-header-drift}",
    "--report"
   ],
   "exit": 0,
   "stdout_text": [
    "guide     header ok   0   invalid   0   legacy   1",
    "kit       header ok   0   invalid   1   legacy   0",
    "theme     header ok   0   invalid   0   legacy   1",
    "viz       header ok   1   invalid   0   legacy   0",
    "  rule id: 1",
    "  rule id-mismatch: 1",
    "  rule legacy: 1",
    "  rule missing-file: 1"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "headers",
    "--root",
    "{catalog-built}",
    "{catalog-built}/kit/badge.js",
    "{catalog-built}/kit/badge.css"
   ],
   "exit": 0,
   "stdout_text": [
    "ok: 1 header(s) valid, 1 skipped"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "headers",
    "--bogus"
   ],
   "exit": 1,
   "stderr_text": [
    "unknown option --bogus"
   ]
  },
  {
   "run": [
    "adp_catalog.py"
   ],
   "exit": 1,
   "stdout_text": [],
   "stderr_text": [
    "usage: adp_catalog.py [CATALOG_DIR]   check a catalog folder (one with a kit/ in it) against its catalog.json",
    "       adp_catalog.py build [CATALOG_DIR] | headers [--root CATALOG_DIR] [--report] [FILE ...] | inventory [--root DIR] | drift [--catalog-dir CATALOG_DIR]"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "{catalog-orphan-order}/none"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp_catalog.py [CATALOG_DIR]   check a catalog folder (one with a kit/ in it) against its catalog.json",
    "       adp_catalog.py build [CATALOG_DIR] | headers [--root CATALOG_DIR] [--report] [FILE ...] | inventory [--root DIR] | drift [--catalog-dir CATALOG_DIR]"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "headers"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp_catalog.py headers [--root CATALOG_DIR] [--report] [FILE ...]   (a folder with a kit/ in it)"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "catalog-drift",
 "steps": [
  {
   "run": [
    "adp_catalog.py",
    "drift",
    "--catalog-dir",
    "{catalog-header-drift}"
   ],
   "exit": 0,
   "stdout_text": [
    "kit.badge tokens: header=[\"--danger\", \"--f-ui\", \"--ok\", \"--warn\"] catalog=[]",
    "viz.meter tokens: header=[\"--accent\", \"--f-ui\", \"--ink\", \"--panel\"] catalog=[]",
    "",
    "4 entries; 2 without a header in their main file",
    "field       equal differ  no header",
    "version         2      0          2",
    "about           2      0          2",
    "provides        2      0          2",
    "tokens          0      2          2",
    "db              2      0          2",
    "entries without a header: guide.reading, theme.paper"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "drift",
    "--catalog-dir",
    "{catalog-built}",
    "--field",
    "version,tokens",
    "--strict"
   ],
   "exit": 0,
   "stdout_text": [
    "kit.badge tokens: header=[\"--danger\", \"--f-ui\", \"--ok\", \"--warn\"] catalog=[]",
    "viz.meter tokens: header=[\"--accent\", \"--f-ui\", \"--ink\", \"--panel\"] catalog=[]",
    "",
    "4 entries; 0 without a header in their main file",
    "field       equal differ  no header",
    "version         4      0          0",
    "tokens          2      2          0"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "drift",
    "--catalog-dir",
    "{catalog-stale-index}",
    "--field",
    "version",
    "--strict"
   ],
   "exit": 1,
   "stdout_text": [
    "viz.meter version: header=0.1.0 catalog=0.2.0",
    "",
    "4 entries; 0 without a header in their main file",
    "field       equal differ  no header",
    "version         3      1          0"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "drift",
    "--field",
    "nope"
   ],
   "exit": 2,
   "stderr_text": [
    "usage: adp_catalog.py drift [-h] [--catalog-dir CATALOG_DIR] [--field FIELD]",
    "                            [--strict]",
    "adp_catalog.py drift: error: unknown field: nope"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "drift",
    "--catalog-dir",
    "{catalog-a}",
    "--strict"
   ],
   "exit": 1,
   "stdout_text": [
    "FAIL: 1 problem(s)",
    "  catalog.json: missing or not JSON"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "drift",
    "-h"
   ],
   "exit": 0,
   "stdout_text": [
    "usage: adp_catalog.py drift [-h] [--catalog-dir CATALOG_DIR] [--field FIELD]",
    "                            [--strict]",
    "",
    "Read-only report: where the header of each entry's main file disagrees with catalog.json.",
    "",
    "adp_catalog.py drift [--catalog-dir CATALOG_DIR] [--field version,about,provides,tokens,db] [--strict]",
    "",
    "One line per disagreement:  <entry id> <field>: header=<...> catalog=<...>   (values cut to 80 chars)",
    "Then a summary table (equal / differ / no header per field) and the entries whose main file has no header.",
    "",
    "Tolerances:",
    "  version   exact string match (@version).",
    "  provides  sets of names (@provides).",
    "  about     share of the catalog about's words (5+ letters) found in the header's about paragraph >= 0.5.",
    "  tokens    sets of css custom properties (@tokens, a trailing ? dropped) after leaving out wildcards (names ending in \"-\" or with a",
    "            <placeholder>), which are listed separately as wildcards.",
    "  db        the catalog needs.db.note, if any, must appear (first 40 chars, case-insensitive) in the header's @db text;",
    "            no note matches an absent or \"none\" header text.",
    "Exit code 0, except 1 with --strict when any version or provides disagreement exists, and 1 with the FAIL line `check` prints when the folder has no catalog.json.",
    "",
    "options:",
    "  -h, --help            show this help message and exit",
    "  --catalog-dir CATALOG_DIR",
    "  --field FIELD         comma list of: version,about,provides,tokens,db",
    "  --strict              exit 1 if any version or provides disagreement"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "drift",
    "--bogus"
   ],
   "exit": 2,
   "stderr_text": [
    "usage: adp_catalog.py drift [-h] [--catalog-dir CATALOG_DIR] [--field FIELD]",
    "                            [--strict]",
    "adp_catalog.py drift: error: unrecognized arguments: --bogus"
   ]
  }
 ]
}
```

```json fixture
{
 "fixture": "inv-catalog",
 "files": {
  "kit/badge.js": "/* part:page.script.kit.badge */\n/**\n * Status badge\n * Draws a small label coloured by a meaning token.\n *\n * @id        kit.badge\n * @kind      component\n * @group     Board kit\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   A small label coloured by a meaning token.\n * @tags      badge\n * @requires  none\n * @files     kit/badge.css\n * @provides  Kit.badge.render\n * @tokens    --ok --warn? --bg\n * @globals   none\n * @db        none\n */\nKit.badge = {render(el, o) { el.style.setProperty('--ok', o.c); }};\n/* /part:page.script.kit.badge */\n",
  "kit/badge.css": "/* part:page.style.kit.badge */\n.kit-badge { color: var(--ok); background: var(--ink, #eee); border-radius: 9px; }\n/* /part:page.style.kit.badge */\n",
  "kit/themes/default.css": "/* part:page.style.kit.theme.default */\n/**\n * Default\n * The tokens every theme sets.\n *\n * @id        theme.default\n * @kind      theme\n * @group     Themes\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   The tokens every theme sets, light and dark.\n * @tags      palette, tokens\n * @requires  none\n * @files     kit/themes/default.json\n * @provides  none\n * @tokens    none\n * @globals   none\n * @db        none\n */\n:root { --bg: #fff; --ink: #111; --accent: #2f5d50; --surface: var(--bg); }\n@media (prefers-color-scheme: dark) { :root:not([data-theme=\"light\"]) { --bg: #000; --ink: #eee; } }\n:root[data-theme=\"dark\"] { --bg: #000; --ink: #eee; --accent: #7fb8a4; }\n/* /part:page.style.kit.theme.default */\n",
  "kit/themes/default.json": "{\n \"id\": \"default\",\n \"name\": \"Default\",\n \"light\": {\n  \"--bg\": \"#fff\",\n  \"--ink\": \"#222\",\n  \"--accent\": \"#2f5d50\"\n },\n \"dark\": {\n  \"--bg\": \"#000\",\n  \"--ink\": \"#eee\",\n  \"--accent\": \"#7fb8a4\"\n }\n}\n",
  "index.html": "<style>.page { color: var(--ink); }</style>\n",
  "notes.txt": "Notes on --ink and --bg; the font is --f-ui.\n"
 }
}
```

```json fixture
{
 "fixture": "inv",
 "files": {
  "templates/minimal/index.html": "<!doctype html>\n<style>\n:root { --bg: #fff; }\nbody { background: var(--bg, #eee); color: var(--ink); border: 1px solid var(--line); border-radius: 4px; font: 14px/1.4 system-ui, sans-serif; box-shadow: 0 1px 2px rgba(0,0,0,.2); text-transform: uppercase; letter-spacing: .02em; outline: 2px solid red; }\n</style>\n<div style=\"width: var(--w); color: #ff0000\" fill=\"#abc\">x</div>\n<script>\n// a comment that names --ignored\nconst el = document.body, k = '--f-' + name, re = /var\\(--x\\)/;\nel.style.setProperty('--accent', '#123456');\ngetComputedStyle(el).getPropertyValue('--ink');\nel.style.setProperty('--dyn-' + i, 1);\nconst s = `.x { color: var(--panel); padding: ${n}px }`, names = '--ok --warn', c = '#888', m = '<i style=\"color:var(--ink)\"></i>';\n</script>\n",
  "assets/badge-copy.css": "/* part:page.style.kit.badge */\n.kit-badge { color: var(--ok); background: var(--ink, #eee); border-radius: 9px; }\n/* /part:page.style.kit.badge */\n",
  "assets/app.js": "document.body.style.color = 'var(--ink)';\n"
 }
}
```

```json vector
{
 "vector": "catalog-inventory",
 "steps": [
  {
   "run": [
    "adp_catalog.py",
    "build",
    "{inv-catalog}"
   ],
   "exit": 0
  },
  {
   "copy": [
    "{inv-catalog}",
    "{inv}/catalog"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "inventory",
    "--root",
    "{inv}"
   ],
   "exit": 0,
   "stdout": {
    "convention": {
     "dark": [
      "--accent",
      "--bg",
      "--ink"
     ],
     "light": [
      "--accent",
      "--bg",
      "--ink"
     ]
    },
    "coverage": {
     "files": 8,
     "outside": [
      {
       "copy_of": null,
       "file": "inv/assets/app.js",
       "names": [
        "--ink"
       ]
      },
      {
       "copy_of": "inv/catalog/kit/badge.css",
       "file": "inv/assets/badge-copy.css",
       "names": [
        "--ink",
        "--ok"
       ]
      }
     ],
     "scanned": 4,
     "theme": 2,
     "unread": [
      {
       "file": "inv/catalog/catalog.json",
       "names": [],
       "why": "index"
      },
      {
       "file": "inv/catalog/notes.txt",
       "names": [
        "--bg",
        "--f-ui",
        "--ink"
       ],
       "why": "unlisted"
      }
     ]
    },
    "entries": {
     "kit.badge": {
      "colour_strings": [],
      "declares": {
       "optional": [
        "--warn"
       ],
       "patterns": [],
       "required": [
        "--bg",
        "--ok"
       ]
      },
      "dynamic": [],
      "files": [
       "inv/catalog/kit/badge.css",
       "inv/catalog/kit/badge.js"
      ],
      "kind": "kit",
      "look": {
       "colour": {
        "literal": {
         "#eee": 1
        }
       },
       "radius": {
        "literal": {
         "9px": 1
        }
       }
      },
      "named": {},
      "needs_differ": {
       "header_only": [
        "--bg",
        "--ok",
        "--warn?"
       ],
       "needs_only": []
      },
      "sets": {
       "--ok": 1
      },
      "undeclared": [
       "--ink"
      ],
      "unused": [
       "--bg",
       "--warn"
      ],
      "uses": {
       "--ink": {
        "bare": 0,
        "fallbacks": [
         "#eee"
        ],
        "files": {
         "inv/catalog/kit/badge.css": 1
        },
        "in_fallback": 0,
        "n": 1
       },
       "--ok": {
        "bare": 1,
        "fallbacks": [],
        "files": {
         "inv/catalog/kit/badge.css": 1
        },
        "in_fallback": 0,
        "n": 1
       }
      }
     }
    },
    "schema": "adp-inventory/1",
    "themes": {
     "theme.default": {
      "blocks": [
       {
        "color-scheme": null,
        "line": 21,
        "other": [],
        "scheme": "light",
        "selector": ":root",
        "tokens": 4
       },
       {
        "color-scheme": null,
        "line": 22,
        "other": [],
        "scheme": "dark-media",
        "selector": "@media (prefers-color-scheme: dark) :root:not([data-theme=\"light\"])",
        "tokens": 2
       },
       {
        "color-scheme": null,
        "line": 23,
        "other": [],
        "scheme": "dark-attr",
        "selector": ":root[data-theme=\"dark\"]",
        "tokens": 3
       }
      ],
      "convention": {
       "dark": {
        "extra": [],
        "missing": []
       },
       "light": {
        "extra": [],
        "missing": []
       }
      },
      "declares": {
       "--accent": {
        "dark": "#7fb8a4",
        "light": "#2f5d50"
       },
       "--bg": {
        "dark": "#000",
        "light": "#fff"
       },
       "--ink": {
        "dark": "#eee",
        "light": "#111"
       },
       "--surface": {
        "dark": null,
        "dark_via": [
         "--bg"
        ],
        "light": "var(--bg)"
       }
      },
      "files": {
       "css": "inv/catalog/kit/themes/default.css",
       "json": "inv/catalog/kit/themes/default.json"
      },
      "json": {
       "dark": {
        "differ": [],
        "only_css": [],
        "only_json": []
       },
       "light": {
        "differ": [
         "--ink"
        ],
        "only_css": [
         "--surface"
        ],
        "only_json": []
       }
      },
      "media_differs": [
       "--accent"
      ],
      "uses": {
       "--bg": {
        "by": [
         "--surface"
        ],
        "declared": true
       }
      }
     }
    },
    "tokens": {
     "--accent": {
      "convention": {
       "dark": true,
       "light": true
      },
      "declared": {
       "optional": [],
       "required": []
      },
      "dynamic": [],
      "named": {},
      "read": {},
      "read_in_themes": {},
      "set": {
       "base.minimal": 1
      },
      "themes": {
       "css": {
        "dark": [
         "theme.default"
        ],
        "light": [
         "theme.default"
        ]
       },
       "json": {
        "dark": [
         "theme.default"
        ],
        "light": [
         "theme.default"
        ]
       }
      }
     },
     "--bg": {
      "convention": {
       "dark": true,
       "light": true
      },
      "declared": {
       "optional": [],
       "required": [
        "kit.badge"
       ]
      },
      "dynamic": [],
      "named": {},
      "read": {
       "base.minimal": 1
      },
      "read_in_themes": {
       "theme.default": 1
      },
      "set": {
       "base.minimal": 1
      },
      "themes": {
       "css": {
        "dark": [
         "theme.default"
        ],
        "light": [
         "theme.default"
        ]
       },
       "json": {
        "dark": [
         "theme.default"
        ],
        "light": [
         "theme.default"
        ]
       }
      }
     },
     "--ink": {
      "convention": {
       "dark": true,
       "light": true
      },
      "declared": {
       "optional": [],
       "required": []
      },
      "dynamic": [],
      "named": {},
      "read": {
       "base.minimal": 3,
       "catalog.page": 1,
       "kit.badge": 1
      },
      "read_in_themes": {},
      "set": {},
      "themes": {
       "css": {
        "dark": [
         "theme.default"
        ],
        "light": [
         "theme.default"
        ]
       },
       "json": {
        "dark": [
         "theme.default"
        ],
        "light": [
         "theme.default"
        ]
       }
      }
     },
     "--line": {
      "convention": {
       "dark": false,
       "light": false
      },
      "declared": {
       "optional": [],
       "required": []
      },
      "dynamic": [],
      "named": {},
      "read": {
       "base.minimal": 1
      },
      "read_in_themes": {},
      "set": {},
      "themes": {
       "css": {
        "dark": [],
        "light": []
       },
       "json": {
        "dark": [],
        "light": []
       }
      }
     },
     "--ok": {
      "convention": {
       "dark": false,
       "light": false
      },
      "declared": {
       "optional": [],
       "required": [
        "kit.badge"
       ]
      },
      "dynamic": [],
      "named": {
       "base.minimal": 1
      },
      "read": {
       "kit.badge": 1
      },
      "read_in_themes": {},
      "set": {
       "kit.badge": 1
      },
      "themes": {
       "css": {
        "dark": [],
        "light": []
       },
       "json": {
        "dark": [],
        "light": []
       }
      }
     },
     "--panel": {
      "convention": {
       "dark": false,
       "light": false
      },
      "declared": {
       "optional": [],
       "required": []
      },
      "dynamic": [],
      "named": {},
      "read": {
       "base.minimal": 1
      },
      "read_in_themes": {},
      "set": {},
      "themes": {
       "css": {
        "dark": [],
        "light": []
       },
       "json": {
        "dark": [],
        "light": []
       }
      }
     },
     "--surface": {
      "convention": {
       "dark": false,
       "light": false
      },
      "declared": {
       "optional": [],
       "required": []
      },
      "dynamic": [],
      "named": {},
      "read": {},
      "read_in_themes": {},
      "set": {},
      "themes": {
       "css": {
        "dark": [
         "theme.default"
        ],
        "light": [
         "theme.default"
        ]
       },
       "json": {
        "dark": [],
        "light": []
       }
      }
     },
     "--w": {
      "convention": {
       "dark": false,
       "light": false
      },
      "declared": {
       "optional": [],
       "required": []
      },
      "dynamic": [],
      "named": {},
      "read": {
       "base.minimal": 1
      },
      "read_in_themes": {},
      "set": {},
      "themes": {
       "css": {
        "dark": [],
        "light": []
       },
       "json": {
        "dark": [],
        "light": []
       }
      }
     },
     "--warn": {
      "convention": {
       "dark": false,
       "light": false
      },
      "declared": {
       "optional": [
        "kit.badge"
       ],
       "required": []
      },
      "dynamic": [],
      "named": {
       "base.minimal": 1
      },
      "read": {},
      "read_in_themes": {},
      "set": {},
      "themes": {
       "css": {
        "dark": [],
        "light": []
       },
       "json": {
        "dark": [],
        "light": []
       }
      }
     }
    },
    "units": {
     "base.minimal": {
      "colour_strings": [
       {
        "file": "inv/templates/minimal/index.html",
        "line": 10,
        "value": "#123456"
       },
       {
        "file": "inv/templates/minimal/index.html",
        "line": 13,
        "value": "#888"
       }
      ],
      "dynamic": [
       {
        "file": "inv/templates/minimal/index.html",
        "how": "name",
        "line": 9,
        "pattern": "--f-*"
       },
       {
        "file": "inv/templates/minimal/index.html",
        "how": "set",
        "line": 12,
        "pattern": "--dyn-*"
       }
      ],
      "files": [
       "inv/templates/minimal/index.html"
      ],
      "look": {
       "case": {
        "literal": {
         "uppercase": 1
        }
       },
       "colour": {
        "literal": {
         "#abc": 1,
         "#eee": 1,
         "#ff0000": 1,
         "#fff": 1,
         "red": 1,
         "rgba(0,0,0,.2)": 1
        }
       },
       "edge": {
        "literal": {
         "1px": 1
        }
       },
       "family": {
        "literal": {
         "system-ui, sans-serif": 1
        }
       },
       "radius": {
        "literal": {
         "4px": 1
        }
       },
       "ring": {
        "literal": {
         "2px solid red": 1
        }
       },
       "shadow": {
        "literal": {
         "0 1px 2px rgba(0, 0, 0, .2)": 1
        }
       },
       "tracking": {
        "literal": {
         ".02em": 1
        }
       }
      },
      "named": {
       "--ok": 1,
       "--warn": 1
      },
      "sets": {
       "--accent": 1,
       "--bg": 1
      },
      "uses": {
       "--bg": {
        "bare": 0,
        "fallbacks": [
         "#eee"
        ],
        "files": {
         "inv/templates/minimal/index.html": 1
        },
        "in_fallback": 0,
        "n": 1
       },
       "--ink": {
        "bare": 3,
        "fallbacks": [],
        "files": {
         "inv/templates/minimal/index.html": 3
        },
        "in_fallback": 0,
        "n": 3
       },
       "--line": {
        "bare": 1,
        "fallbacks": [],
        "files": {
         "inv/templates/minimal/index.html": 1
        },
        "in_fallback": 0,
        "n": 1
       },
       "--panel": {
        "bare": 1,
        "fallbacks": [],
        "files": {
         "inv/templates/minimal/index.html": 1
        },
        "in_fallback": 0,
        "n": 1
       },
       "--w": {
        "bare": 1,
        "fallbacks": [],
        "files": {
         "inv/templates/minimal/index.html": 1
        },
        "in_fallback": 0,
        "n": 1
       }
      }
     },
     "catalog.page": {
      "colour_strings": [],
      "dynamic": [],
      "files": [
       "inv/catalog/index.html"
      ],
      "look": {},
      "named": {},
      "sets": {},
      "uses": {
       "--ink": {
        "bare": 1,
        "fallbacks": [],
        "files": {
         "inv/catalog/index.html": 1
        },
        "in_fallback": 0,
        "n": 1
       }
      }
     }
    }
   },
   "stderr_text": []
  },
  {
   "run": [
    "adp_catalog.py",
    "inventory",
    "--bogus"
   ],
   "exit": 1,
   "stderr_text": [
    "unknown option --bogus"
   ]
  },
  {
   "run": [
    "adp_catalog.py",
    "inventory",
    "--root",
    "{nothing}"
   ],
   "exit": 1,
   "stderr_text": [
    "FAIL: FileNotFoundError(2, 'No such file or directory')"
   ]
  }
 ]
}
```

## Contract: reading a catalog (`kit`, `suggest`, `take`)

```json vector
{
 "vector": "kit-list",
 "run": [
  "adp.py",
  "kit",
  "list",
  "{catalog-built}/catalog.json"
 ],
 "exit": 0,
 "stdout_text": [
  "{\"id\":\"kit.badge\",\"kind\":\"kit\",\"name\":\"Status badge\",\"summary\":\"A small label coloured by a meaning token.\",\"tags\":[\"badge\",\"status\",\"label\"]}",
  "{\"id\":\"guide.reading\",\"kind\":\"guide\",\"name\":\"Reading this catalog\",\"summary\":\"What each folder of this catalog holds and how a page takes an entry.\",\"tags\":[\"guide\",\"catalog\",\"folders\"]}",
  "{\"id\":\"theme.paper\",\"kind\":\"theme\",\"name\":\"Paper\",\"summary\":\"Warm paper by day, ink-blue by night, one green accent.\",\"tags\":[\"palette\",\"tokens\",\"dark mode\",\"paper\"]}",
  "{\"id\":\"viz.meter\",\"kind\":\"viz\",\"name\":\"Meter\",\"summary\":\"A bar that states its value and range in words, with a status badge.\",\"tags\":[\"meter\",\"bar\",\"progress\",\"value\"]}"
 ],
 "stderr_text": [
  "warning: a local index is a build, not the live catalog: a file it lists may be missing there"
 ]
}
```

```json vector
{
 "vector": "kit-list-by-kind",
 "run": [
  "adp.py",
  "kit",
  "list",
  "{catalog-built}/catalog.json",
  "--kind",
  "viz"
 ],
 "exit": 0,
 "stdout_text": [
  "{\"id\":\"viz.meter\",\"kind\":\"viz\",\"name\":\"Meter\",\"summary\":\"A bar that states its value and range in words, with a status badge.\",\"tags\":[\"meter\",\"bar\",\"progress\",\"value\"]}"
 ]
}
```

```json vector
{
 "vector": "kit-show",
 "run": [
  "adp.py",
  "kit",
  "show",
  "viz.meter",
  "{catalog-built}/catalog.json"
 ],
 "exit": 0,
 "stdout": {
  "id": "viz.meter",
  "name": "Meter",
  "summary": "A bar that states its value and range in words, with a status badge.",
  "about": "Kit.meter.draw(el, {value, max, label}) draws a bar that states its value in words, with a badge for the tone it falls in.",
  "tags": [
   "meter",
   "bar",
   "progress",
   "value"
  ],
  "files": [
   "kit/viz/meter.js",
   "kit/viz/meter.css",
   "kit/samples/viz.json"
  ],
  "requires": [
   "kit.badge"
  ],
  "provides": [
   "Kit.meter.draw"
  ],
  "status": "new",
  "version": "0.1.0",
  "config": [
   [
    "Kit.meter.draw(el, opts)",
    "value, max, label"
   ]
  ],
  "db": {
   "reads": [],
   "writes": [],
   "note": ""
  }
 }
}
```

```json vector
{
 "vector": "kit-show-unknown",
 "run": [
  "adp.py",
  "kit",
  "show",
  "viz.nope",
  "{catalog-built}/catalog.json"
 ],
 "exit": 1,
 "stdout_text": [],
 "stderr_text": [
  "warning: a local index is a build, not the live catalog: a file it lists may be missing there",
  "no entry viz.nope in the catalog"
 ]
}
```

```json vector
{
 "vector": "kit-describe",
 "run": [
  "adp.py",
  "kit",
  "describe",
  "kit.badge",
  "{catalog-built}/catalog.json"
 ],
 "exit": 0,
 "stdout": {
  "id": "kit.badge",
  "needs": [],
  "optional": [],
  "provides": [
   "Kit.badge.render"
  ],
  "requires": [],
  "files": [
   "kit/badge.js",
   "kit/badge.css"
  ],
  "sample": "kit/samples/kit.json",
  "sample_key": "badge",
  "db": {
   "reads": [],
   "writes": [],
   "note": ""
  }
 }
}
```

```json vector
{
 "vector": "suggest-by-words",
 "run": [
  "adp.py",
  "suggest",
  "{catalog-built}/catalog.json",
  "--for",
  "progress bar"
 ],
 "exit": 0,
 "stdout": [
  {
   "id": "viz.meter",
   "kind": "viz",
   "why": "tags: bar, progress; name/summary: bar; about: bar",
   "requires": [
    "kit.badge"
   ],
   "takes": 2
  }
 ]
}
```

```json vector
{
 "vector": "take-with-its-requires",
 "run": [
  "adp.py",
  "take",
  "{catalog-built}/catalog.json",
  "viz.meter",
  "--url",
  "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002"
 ],
 "exit": 0,
 "stdout": {
  "catalog": {
   "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
   "index": "<tmp>/catalog-built/catalog.json",
   "live": false,
   "ver": null,
   "built": "<time>",
   "warning": "a local index is a build, not the live catalog: a file it lists may be missing there. adp.py take <catalog url> ... reads the fetched live index"
  },
  "entries": [
   "kit.badge",
   "viz.meter"
  ],
  "files": {
   "kit/badge.js": {
    "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
    "path": "kit/badge.js"
   },
   "kit/badge.css": {
    "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
    "path": "kit/badge.css"
   },
   "kit/viz/meter.js": {
    "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
    "path": "kit/viz/meter.js"
   },
   "kit/viz/meter.css": {
    "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
    "path": "kit/viz/meter.css"
   },
   "kit/samples/viz.json": {
    "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
    "path": "kit/samples/viz.json"
   }
  },
  "sha256": {
   "kit/badge.js": "18ba1a867d82bc9e28b399fdc6a9fc306f6b79252d5d88f7d9035e681fa040ab",
   "kit/badge.css": "e36fc8a443380c6dea1dfad9be19b7c67d72c6e735d471c546115c182d00478c",
   "kit/viz/meter.js": "efcf7c5c57ca8affb49a053292d5a29e7c1dbdbf402fa99909a03ed8d13fd37f",
   "kit/viz/meter.css": "3cbbbd327ce9f7de9c0284e73cddb355107a1b5fb31369301aadf318613e1c33",
   "kit/samples/viz.json": "c8af2a4b0d09926a10a953d1a2ffb00ff111b694ff6b0d9f43f62be1b7e4ddcc"
  },
  "samples": {
   "viz.meter": [
    "kit/samples/viz.json#meter"
   ]
  }
 }
}
```

```json vector
{
 "vector": "take-a-local-index-needs-a-url",
 "run": [
  "adp.py",
  "take",
  "{catalog-built}/catalog.json",
  "viz.meter"
 ],
 "exit": 1,
 "stderr_text": [
  "take: no catalog url. Pass the catalog url as CATALOG (then the index is the live one), or --url with a local index"
 ]
}
```

```json vector
{
 "vector": "take-unknown",
 "run": [
  "adp.py",
  "take",
  "{catalog-built}/catalog.json",
  "viz.nope",
  "--url",
  "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002"
 ],
 "exit": 1,
 "stderr_text": [
  "no entry viz.nope in <tmp>/catalog-built/catalog.json"
 ]
}
```

The fixture `catalog-quirks` is a local index whose `kit.a` file carries a pinned `ver`, whose `kit.a` and `kit.b` require each other, and whose `viz.c` names no `main`: its header is found through its script. `take` publishes the pin, ends the cycle, reads the header (a `@preview` may continue on the next lines) and refuses a missing saved catalog, a missing index and missing ids with one line.

```json fixture
{
 "fixture": "catalog-quirks",
 "files": {
  "catalog.json": "{\n \"entries\": [\n  {\n   \"id\": \"kit.a\",\n   \"kind\": \"component\",\n   \"requires\": [\n    \"kit.b\"\n   ],\n   \"files\": [\n    {\n     \"path\": \"kit/a.js\",\n     \"role\": \"script\",\n     \"ver\": \"v7\"\n    }\n   ]\n  },\n  {\n   \"id\": \"kit.b\",\n   \"kind\": \"component\",\n   \"requires\": [\n    \"kit.a\"\n   ],\n   \"files\": [\n    {\n     \"path\": \"kit/b.js\",\n     \"role\": \"script\"\n    }\n   ]\n  },\n  {\n   \"id\": \"viz.c\",\n   \"kind\": \"component\",\n   \"requires\": [],\n   \"files\": [\n    {\n     \"path\": \"kit/c.js\",\n     \"role\": \"script\"\n    },\n    {\n     \"path\": \"kit/samples/c.json\",\n     \"role\": \"sample\"\n    }\n   ]\n  }\n ]\n}\n",
  "kit/c.js": "/**\n * C\n * Draws c.\n *\n * @id        viz.c\n * @preview   {\"render\": \"viz.c\",\n *            \"samples\": [\"kit/samples/c.json#c\"]}\n * @samples   c\n */\n"
 }
}
```

```json vector
{
 "vector": "take-index-quirks",
 "steps": [
  {
   "run": [
    "adp.py",
    "take",
    "{catalog-quirks}/catalog.json",
    "kit.a",
    "viz.c",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002"
   ],
   "exit": 0,
   "stdout": {
    "catalog": {
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "index": "<tmp>/catalog-quirks/catalog.json",
     "live": false,
     "ver": null,
     "built": null,
     "warning": "a local index is a build, not the live catalog: a file it lists may be missing there. adp.py take <catalog url> ... reads the fetched live index"
    },
    "entries": [
     "kit.b",
     "kit.a",
     "viz.c"
    ],
    "files": {
     "kit/b.js": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/b.js"
     },
     "kit/a.js": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/a.js",
      "ver": "v7"
     },
     "kit/c.js": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/c.js"
     },
     "kit/samples/c.json": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/samples/c.json"
     }
    },
    "sha256": {},
    "samples": {
     "viz.c": [
      "kit/samples/c.json#c"
     ]
    }
   }
  },
  {
   "run": [
    "adp.py",
    "take",
    "-",
    "kit.a"
   ],
   "exit": 1,
   "stderr_text": [
    "take: no saved catalog; adp.py catalog <url> saves one"
   ]
  },
  {
   "run": [
    "adp.py",
    "take",
    "{catalog-quirks}/none.json",
    "kit.a"
   ],
   "exit": 1,
   "stderr_text": [
    "take: <tmp>/catalog-quirks/none.json is neither a catalog url nor a catalog.json"
   ]
  },
  {
   "run": [
    "adp.py",
    "take",
    "{catalog-quirks}/catalog.json"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py take CATALOG ID ... [--url URL] [--config C.json]   CATALOG: the catalog url, - (saved), or a local catalog.json"
   ]
  },
  {
   "run": [
    "adp.py",
    "take"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py take CATALOG ID ... [--url URL] [--config C.json]   CATALOG: the catalog url, - (saved), or a local catalog.json"
   ]
  }
 ]
}
```

## Contract: My Own Kit (`catalog`)

```json fixture
{"fixture": "catalog-index-only", "base": "catalog-built", "files": {"kit/badge.js": null, "kit/badge.css": null, "kit/viz/meter.js": null, "kit/viz/meter.css": null,
 "kit/themes/paper.css": null, "kit/themes/paper.json": null, "kit/guides/reading.md": null, "kit/samples/kit.json": null, "kit/samples/viz.json": null}}
```

```json vector
{
 "vector": "catalog-fetch-into-my-own-kit",
 "steps": [
  {
   "run": [
    "adp.py",
    "catalog",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c"
   ],
   "exit": 0,
   "stdout": {
    "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
    "index": "<tmp>/home/catalog/catalog.json",
    "fetched": false,
    "fetch": {
     "tool": "Artifact",
     "action": "read",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
     "path": "catalog.json",
     "out_dir": "<tmp>/home/catalog",
     "then": "run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)"
    }
   },
   "files_out": {
    "{home}/config.json": {
     "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c"
    }
   }
  },
  {
   "copy": [
    "{catalog-index-only}",
    "{home}/catalog"
   ]
  },
  {
   "run": [
    "adp.py",
    "catalog"
   ],
   "exit": 0,
   "stdout": {
    "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
    "index": "<tmp>/home/catalog/catalog.json",
    "fetched": true,
    "ver": null,
    "built": "<time>",
    "entries": 4,
    "refresh": {
     "tool": "Artifact",
     "action": "read",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
     "path": "catalog.json",
     "out_dir": "<tmp>/home/catalog",
     "then": "run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)"
    },
    "kit": "<tmp>/home/catalog",
    "files": 9,
    "missing": 9,
    "complete": false,
    "reads": [
     {
      "tool": "Artifact",
      "action": "read",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
      "paths": [
       "kit/badge.css",
       "kit/badge.js",
       "kit/guides/reading.md",
       "kit/samples/kit.json",
       "kit/samples/viz.json",
       "kit/themes/paper.css",
       "kit/themes/paper.json",
       "kit/viz/meter.css",
       "kit/viz/meter.js"
      ],
      "out_dir": "<tmp>/home/catalog",
      "then": "run `adp.py catalog` again: complete is true when every file is here"
     }
    ],
    "calls": 1,
    "per_call": [
     9
    ],
    "next": "My Own Kit is not complete: make the reads, then run adp.py catalog again"
   }
  },
  {
   "copy": [
    "{catalog-built}",
    "{home}/catalog"
   ]
  },
  {
   "run": [
    "adp.py",
    "catalog"
   ],
   "exit": 0,
   "stdout": {
    "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
    "index": "<tmp>/home/catalog/catalog.json",
    "fetched": true,
    "ver": null,
    "built": "<time>",
    "entries": 4,
    "refresh": {
     "tool": "Artifact",
     "action": "read",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
     "path": "catalog.json",
     "out_dir": "<tmp>/home/catalog",
     "then": "run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)"
    },
    "kit": "<tmp>/home/catalog",
    "files": 9,
    "missing": 0,
    "complete": true
   }
  }
 ]
}
```

```json vector
{
 "vector": "catalog-refuses-a-wrong-url",
 "steps": [
  {
   "run": [
    "adp.py",
    "catalog"
   ],
   "exit": 0,
   "stdout": {
    "catalog": null,
    "next": "adp.py catalog <url> saves the user's catalog (SKILL.md says how to find it); never assume one"
   }
  },
  {
   "run": [
    "adp.py",
    "catalog",
    "https://example.com/catalog"
   ],
   "exit": 1,
   "stderr_text": [
    "catalog: use a Claude artifact URL"
   ],
   "files_out": {
    "{home}/config.json": null
   }
  },
  {
   "run": [
    "adp.py",
    "catalog",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c?x=1"
   ],
   "exit": 1,
   "stderr_text": [
    "catalog: use a Claude artifact URL"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "kit-reads-a-url-catalog",
 "steps": [
  {
   "run": [
    "adp.py",
    "kit",
    "list",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c"
   ],
   "exit": 2,
   "stdout": {
    "error": "index not fetched",
    "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
    "fetch": {
     "tool": "Artifact",
     "action": "read",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
     "path": "catalog.json",
     "out_dir": "<tmp>/home/catalog",
     "then": "run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)"
    },
    "next": "adp.py catalog fetches your whole kit (My Own Kit)"
   }
  },
  {
   "run": [
    "adp.py",
    "catalog",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c/"
   ],
   "exit": 0
  },
  {
   "copy": [
    "{catalog-index-only}",
    "{home}/catalog"
   ]
  },
  {
   "run": [
    "adp.py",
    "kit",
    "show",
    "viz.meter",
    "-"
   ],
   "exit": 0,
   "stdout": {
    "id": "viz.meter",
    "name": "Meter",
    "summary": "A bar that states its value and range in words, with a status badge.",
    "about": "",
    "tags": [
     "meter",
     "bar",
     "progress",
     "value"
    ],
    "files": [
     "kit/viz/meter.js",
     "kit/viz/meter.css",
     "kit/samples/viz.json"
    ],
    "requires": [
     "kit.badge"
    ],
    "provides": [
     "Kit.meter.draw"
    ],
    "note": "the main-file header is not on disk, so about and the header fields are missing; read it, then run the command again",
    "fetch": [
     {
      "tool": "Artifact",
      "action": "read",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
      "paths": [
       "kit/viz/meter.js"
      ],
      "out_dir": "<tmp>/home/catalog",
      "then": "run the command again"
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "kit",
    "describe",
    "kit.badge",
    "-"
   ],
   "exit": 0,
   "stdout": {
    "id": "kit.badge",
    "needs": [],
    "optional": [],
    "provides": [
     "Kit.badge.render"
    ],
    "requires": [],
    "files": [
     "kit/badge.js",
     "kit/badge.css"
    ],
    "sample": "kit/samples/kit.json",
    "note": "the main-file header is not on disk, so about and the header fields are missing; read it, then run the command again",
    "fetch": [
     {
      "tool": "Artifact",
      "action": "read",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
      "paths": [
       "kit/badge.js"
      ],
      "out_dir": "<tmp>/home/catalog",
      "then": "run the command again"
     }
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "suggest",
    "-",
    "--for",
    "progress bar"
   ],
   "exit": 0,
   "stdout": [
    {
     "id": "viz.meter",
     "kind": "viz",
     "requires": [
      "kit.badge"
     ],
     "why": "tags: bar, progress; name/summary: bar",
     "takes": 2
    }
   ],
   "stderr_text": [
    "note: 4 main-file headers are not on disk, so their about text was not searched (tags, name, summary, id and provides were); read them, then run the command again:",
    "{\"tool\": \"Artifact\", \"action\": \"read\", \"url\": \"https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c\", \"paths\": [\"kit/badge.js\", \"kit/guides/reading.md\", \"kit/themes/paper.css\", \"kit/viz/meter.js\"], \"out_dir\": \"<tmp>/home/catalog\", \"then\": \"run the command again\"}"
   ]
  },
  {
   "copy": [
    "{catalog-built}",
    "{home}/catalog"
   ]
  },
  {
   "run": [
    "adp.py",
    "kit",
    "list",
    "-",
    "--tag",
    "meter"
   ],
   "exit": 0,
   "stdout_text": [
    "{\"id\":\"viz.meter\",\"kind\":\"viz\",\"name\":\"Meter\",\"summary\":\"A bar that states its value and range in words, with a status badge.\",\"tags\":[\"meter\",\"bar\",\"progress\",\"value\"]}"
   ]
  },
  {
   "run": [
    "adp.py",
    "suggest",
    "-",
    "--for",
    "progress bar",
    "--n",
    "1"
   ],
   "exit": 0,
   "stdout": [
    {
     "id": "viz.meter",
     "kind": "viz",
     "requires": [
      "kit.badge"
     ],
     "why": "tags: bar, progress; name/summary: bar; about: bar",
     "takes": 2
    }
   ],
   "stderr_text": []
  }
 ]
}
```

```json vector
{
 "vector": "suggest-options",
 "steps": [
  {
   "run": [
    "adp.py",
    "suggest",
    "{catalog-built}/catalog.json",
    "--for",
    "bars of values",
    "--kind",
    "viz",
    "--n",
    "1"
   ],
   "exit": 0,
   "stdout": [
    {
     "id": "viz.meter",
     "kind": "viz",
     "requires": [
      "kit.badge"
     ],
     "why": "tags: bar, value; name/summary: bar, value; about: bar, value",
     "takes": 2
    }
   ],
   "stderr_text": [
    "warning: a local index is a build, not the live catalog: a file it lists may be missing there"
   ]
  },
  {
   "run": [
    "adp.py",
    "suggest",
    "{catalog-built}/catalog.json",
    "--for",
    "the status of a label",
    "--n",
    "2"
   ],
   "exit": 0,
   "stdout": [
    {
     "id": "kit.badge",
     "kind": "kit",
     "requires": [],
     "why": "tags: status, label; name/summary: label, status; about: label",
     "takes": 2
    },
    {
     "id": "viz.meter",
     "kind": "viz",
     "requires": [
      "kit.badge"
     ],
     "why": "name/summary: status; about: label",
     "takes": 2
    }
   ],
   "stderr_text": [
    "warning: a local index is a build, not the live catalog: a file it lists may be missing there"
   ]
  },
  {
   "run": [
    "adp.py",
    "suggest",
    "{catalog-built}/catalog.json",
    "--for",
    "zzz"
   ],
   "exit": 0,
   "stdout": []
  },
  {
   "run": [
    "adp.py",
    "suggest",
    "{catalog-built}/catalog.json"
   ],
   "exit": 1,
   "stderr_text": [
    "usage: adp.py suggest CATALOG --for \"free words\" [--n 3] [--kind K]"
   ]
  }
 ]
}
```

```json vector
{
 "vector": "catalog-reads-an-older-folder",
 "steps": [
  {
   "run": [
    "adp.py",
    "catalog",
    "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c"
   ],
   "exit": 0
  },
  {
   "copy": [
    "{catalog-built}",
    "{home}/catalogs/00000000-0000-4000-8000-00000000000c"
   ]
  },
  {
   "run": [
    "adp.py",
    "catalog"
   ],
   "exit": 0,
   "stdout": {
    "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
    "index": "<tmp>/home/catalogs/00000000-0000-4000-8000-00000000000c/catalog.json",
    "fetched": true,
    "ver": null,
    "built": "<time>",
    "entries": 4,
    "refresh": {
     "tool": "Artifact",
     "action": "read",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
     "path": "catalog.json",
     "out_dir": "<tmp>/home/catalogs/00000000-0000-4000-8000-00000000000c",
     "then": "run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)"
    },
    "kit": "<tmp>/home/catalogs/00000000-0000-4000-8000-00000000000c",
    "files": 9,
    "missing": 0,
    "complete": true
   }
  },
  {
   "run": [
    "adp.py",
    "kit",
    "describe",
    "kit.badge",
    "-"
   ],
   "exit": 0,
   "stdout": {
    "id": "kit.badge",
    "needs": [],
    "optional": [],
    "provides": [
     "Kit.badge.render"
    ],
    "requires": [],
    "files": [
     "kit/badge.js",
     "kit/badge.css"
    ],
    "sample": "kit/samples/kit.json",
    "sample_key": "badge",
    "db": {
     "reads": [],
     "writes": [],
     "note": ""
    }
   }
  },
  {
   "copy": [
    "{catalog-index-only}",
    "{home}/catalog"
   ]
  },
  {
   "run": [
    "adp.py",
    "catalog"
   ],
   "exit": 0,
   "stdout": {
    "catalog": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
    "index": "<tmp>/home/catalog/catalog.json",
    "fetched": true,
    "ver": null,
    "built": "<time>",
    "entries": 4,
    "refresh": {
     "tool": "Artifact",
     "action": "read",
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
     "path": "catalog.json",
     "out_dir": "<tmp>/home/catalog",
     "then": "run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)"
    },
    "kit": "<tmp>/home/catalog",
    "files": 9,
    "missing": 9,
    "complete": false,
    "reads": [
     {
      "tool": "Artifact",
      "action": "read",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-00000000000c",
      "paths": [
       "kit/badge.css",
       "kit/badge.js",
       "kit/guides/reading.md",
       "kit/samples/kit.json",
       "kit/samples/viz.json",
       "kit/themes/paper.css",
       "kit/themes/paper.json",
       "kit/viz/meter.css",
       "kit/viz/meter.js"
      ],
      "out_dir": "<tmp>/home/catalog",
      "then": "run `adp.py catalog` again: complete is true when every file is here"
     }
    ],
    "calls": 1,
    "per_call": [
     9
    ],
    "next": "My Own Kit is not complete: make the reads, then run adp.py catalog again"
   }
  }
 ]
}
```

```json fixture
{
 "fixture": "catalog-orphan-order",
 "base": "catalog-a",
 "files": {
  "kit/b.js": "/* a kit file no entry names */\n",
  "kit/a/x.js": "/* another one, in a folder that sorts first */\n"
 }
}
```

```json vector
{
 "vector": "catalog-orphans-in-tree-order",
 "run": [
  "adp_catalog.py",
  "build",
  "{catalog-orphan-order}"
 ],
 "exit": 1,
 "stderr_text": [
  "2 problem(s); catalog.json is not written:",
  "  kit/b.js: no entry names it (add it to @files in the header of its entry)",
  "  kit/a/x.js: no entry names it (add it to @files in the header of its entry)"
 ]
}
```

A file under `kit/previews/` is an entry's own preview for the catalog page: `build` gives it the role `preview`, and `take`, `kit describe` and the `takes` count of `suggest` leave it out (`kit show` lists every file of the entry).

```json fixture
{
 "fixture": "catalog-preview",
 "files": {
  "kit/p.js": "/**\n * P\n * Draws p.\n *\n * @id        kit.p\n * @kind      component\n * @group     Board kit\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-22\n * @summary   Draws p.\n * @tags      p\n * @requires  none\n * @files     kit/previews/p.js\n * @provides  Kit.p\n * @globals   none\n * @db        none\n */\n",
  "kit/previews/p.js": "// the catalog page's preview of kit.p\n",
  "welcome.html": "<!doctype html><title>About</title>\n"
 }
}
```

```json vector
{
 "vector": "catalog-preview-role-is-left-out-by-take",
 "steps": [
  {
   "run": [
    "adp_catalog.py",
    "build",
    "{catalog-preview}"
   ],
   "exit": 0,
   "files_out": {
    "{catalog-preview}/catalog.json": {
     "schema": "kit-catalog/2",
     "url": "",
     "ver": "",
     "built": "<time>",
     "entries": [
      {
       "id": "kit.p",
       "kind": "component",
       "group": "Board kit",
       "name": "P",
       "summary": "Draws p.",
       "tags": [
        "p"
       ],
       "status": "new",
       "version": "0.1.0",
       "requires": [],
       "globals": [],
       "provides": [
        "Kit.p"
       ],
       "main": "kit/p.js",
       "files": [
        {
         "path": "kit/p.js",
         "role": "script",
         "sha256": "f69a1683bcf4dbc1c59543bf2ced6d08b5b9409638ee4f3f4852173abe75a02c",
         "bytes": 307
        },
        {
         "path": "kit/previews/p.js",
         "role": "preview",
         "sha256": "6f4f586155230ed2cf8ed2f65d4c89b8734092f1fe60518d33c4d81fdc42fe8c",
         "bytes": 39
        }
       ],
       "hash": "0e0da6c00b38"
      }
     ]
    }
   }
  },
  {
   "run": [
    "adp_catalog.py",
    "{catalog-preview}"
   ],
   "exit": 0,
   "stdout_text": [
    "OK: 1 entries, 2 entry files, 4 files in tree, 0 orphans, all sizes, sha256 and hashes match, 1 valid headers"
   ]
  },
  {
   "run": [
    "adp.py",
    "take",
    "{catalog-preview}/catalog.json",
    "kit.p",
    "--url",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002"
   ],
   "exit": 0,
   "stdout": {
    "catalog": {
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "index": "<tmp>/catalog-preview/catalog.json",
     "live": false,
     "ver": null,
     "built": "<time>",
     "warning": "a local index is a build, not the live catalog: a file it lists may be missing there. adp.py take <catalog url> ... reads the fetched live index"
    },
    "entries": [
     "kit.p"
    ],
    "files": {
     "kit/p.js": {
      "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "path": "kit/p.js"
     }
    },
    "sha256": {
     "kit/p.js": "f69a1683bcf4dbc1c59543bf2ced6d08b5b9409638ee4f3f4852173abe75a02c"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "kit",
    "describe",
    "kit.p",
    "{catalog-preview}/catalog.json"
   ],
   "exit": 0,
   "stdout": {
    "id": "kit.p",
    "needs": [],
    "optional": [],
    "provides": [
     "Kit.p"
    ],
    "requires": [],
    "files": [
     "kit/p.js"
    ],
    "sample": null,
    "db": {
     "reads": [],
     "writes": [],
     "note": ""
    }
   }
  },
  {
   "run": [
    "adp.py",
    "suggest",
    "{catalog-preview}/catalog.json",
    "--for",
    "draws p"
   ],
   "exit": 0,
   "stdout": [
    {
     "id": "kit.p",
     "kind": "kit",
     "requires": [],
     "why": "tags: p; name/summary: draws, p; id: p; provides: p; about: draws, p",
     "takes": 1
    }
   ]
  }
 ]
}
```

The fixture `catalog-bad-theme` is `catalog-a` with a theme whose stylesheet has no `:root[data-theme="dark"]` block and whose JSON has no `dark`. `build` indexes it; the check names both.

```json fixture
{
 "fixture": "catalog-bad-theme",
 "base": "catalog-a",
 "files": {
  "kit/themes/paper.css": "/* part:page.style.kit.theme.paper */\n/**\n * Paper\n * Warm paper by day, ink-blue by night; one green accent.\n *\n * @id        theme.paper\n * @kind      theme\n * @group     Themes\n * @status    new\n * @version   0.1.0\n * @updated   2026-11-20\n * @summary   Warm paper by day, ink-blue by night, one green accent.\n * @tags      palette, tokens, dark mode, paper\n * @requires  none\n * @files     kit/themes/paper.json\n * @provides  none\n * @tokens    none\n * @globals   none\n * @fonts     https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\n * @db        none\n */\n:root { --bg: #fbfaf7; --panel: #ffffff; --ink: #1d1b16; --accent: #2f5d50; --ok: #2e7d4f; --warn: #8a5200; --danger: #b3261e; --f-ui: \"Inter\", system-ui, sans-serif; }\n@media (prefers-color-scheme: dark) { :root:not([data-theme=\"light\"]) { --bg: #14130f; --panel: #1c1a15; --ink: #ece8dc; --accent: #7fb8a4; --ok: #7fc79a; --warn: #e0b060; --danger: #f08a80; } }\n/* /part:page.style.kit.theme.paper */\n",
  "kit/themes/paper.json": "{\n \"id\": \"paper\",\n \"name\": \"Paper\",\n \"about\": \"Warm paper by day, ink-blue by night; one green accent.\",\n \"source\": \"an example for this skill\",\n \"fonts\": \"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\",\n \"light\": {\n  \"--bg\": \"#fbfaf7\",\n  \"--panel\": \"#ffffff\",\n  \"--ink\": \"#1d1b16\",\n  \"--accent\": \"#2f5d50\",\n  \"--ok\": \"#2e7d4f\",\n  \"--warn\": \"#8a5200\",\n  \"--danger\": \"#b3261e\",\n  \"--f-ui\": \"\\\"Inter\\\", system-ui, sans-serif\"\n }\n}\n"
 }
}
```

```json vector
{
 "vector": "catalog-check-theme-shape",
 "steps": [
  {
   "run": [
    "adp_catalog.py",
    "build",
    "{catalog-bad-theme}"
   ],
   "exit": 0
  },
  {
   "run": [
    "adp_catalog.py",
    "{catalog-bad-theme}"
   ],
   "exit": 1,
   "stdout_text": [
    "FAIL: 2 problem(s)",
    "  theme.paper: theme: no :root[data-theme=\"dark\"] block",
    "  theme.paper: theme: its JSON lacks light, dark or the entry's fonts url"
   ]
  }
 ]
}
```
