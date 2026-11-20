# Vectors: adp-minimal-catalog

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

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
