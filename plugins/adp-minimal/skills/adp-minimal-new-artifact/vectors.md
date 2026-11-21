# Vectors: adp-minimal-new-artifact

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are run against the tools assembled from the fragments.

## Contract: `new`

The template `new` builds from, installed as `templates/minimal/` beside the tool (files ending `.txt` are written without it):

```json fixture
{"fixture": "template-minimal", "files": {
 "template.json": "{\n \"name\": \"minimal\",\n \"summary\": \"The smallest adp/2 page: the shell, its copy as data, and a status list of what the runtime found (host, viewer, capabilities, integrity, seeding). Needs nothing from the catalog.\",\n \"use_when\": \"Starting a page from the specification alone, or checking a build of the tools and the runtime on a real host.\",\n \"design\": \"A token-only look with system fonts: the three theme blocks in styles/page.css. Keep the token names, the part markers and the What changed selectors adp.js fills (#wc, #wcN, #wcChanges, #wcDecisions, #wcIncoming); replace the Home section with the page's own views.\",\n \"capabilities\": {\"db\": {\"rules\": [{\"path\": \"\", \"read\": \"view\", \"write\": \"admin\"}, {\"path\": \"ns/shared\", \"read\": \"view\", \"write\": \"interact\"}, {\"path\": \"ns/users/{self}\", \"read\": \"view\", \"write\": \"interact\"}]}, \"user\": {}, \"comments\": {\"customAnchors\": true}, \"artifact\": {}},\n \"take\": []\n}\n",
 "index.html.txt": "<title>{{title}}</title>\n<meta name=\"adp:build\" content=\"1\">\n<link rel=\"stylesheet\" href=\"styles/page.css\">\n<!-- part:page.header -->\n<header data-part=\"page.header\" data-comment-target>\n<h1>{{title}}</h1>\n<!-- part:page.lead --><p data-part=\"page.lead\" data-comment-target></p><!-- /part:page.lead -->\n<!-- part:page.changes --><details id=\"wc\" data-part=\"page.changes\" data-comment-target hidden><summary>What changed <span id=\"wcN\"></span></summary><ol id=\"wcChanges\"></ol><ul id=\"wcDecisions\"></ul><ul id=\"wcIncoming\"></ul></details><!-- /part:page.changes -->\n</header>\n<!-- /part:page.header -->\n<!-- part:page.tabs --><nav data-part=\"page.tabs\" data-comment-target></nav><!-- /part:page.tabs -->\n<main id=\"views\">\n<!-- part:home --><section data-part=\"home\" data-comment-target>\n<!-- part:home.intro --><div data-part=\"home.intro\" data-comment-target></div><!-- /part:home.intro -->\n<!-- part:home.status --><dl id=\"status\" data-part=\"home.status\" data-comment-target></dl><!-- /part:home.status -->\n</section><!-- /part:home -->\n</main>\n<script src=\"content.js\"></script>\n<script src=\"adp.js\"></script>\n<script src=\"parts/app.js\"></script>\n",
 "content.js.txt": "/* part:page.script.content */\n/* The page's copy, by part id. The record's content/<id> documents override it live, with no republish. */\nwindow.ADP_CONTENT = {\n \"page.lead\": {\"part\": \"page.lead\", \"title\": \"Lead\", \"html\": \"A minimal ADP page. Replace this line with what the page is for.\"},\n \"home.intro\": {\"part\": \"home.intro\", \"title\": \"Introduction\", \"html\": \"<p>Every section of this page has a part id, its copy lives in the record, and every publish is recorded. The list below is what the runtime found on this host.</p>\"}\n};\n/* /part:page.script.content */\n",
 "parts/app.js.txt": "/* part:page.script.app */\n/* The page's code: paint the copy, list what the runtime found, register the page. Replace the Home section with the page's own views. */\n(function(){\n'use strict';\nconst A = window.ADP, COPY = new Set(Object.keys(window.ADP_CONTENT || {}));\nconst TITLES = {'page.header': 'Header', 'page.lead': 'Lead', 'page.changes': 'What changed', 'page.tabs': 'Views',\n  home: 'Home', 'home.intro': 'Introduction', 'home.status': 'Status'};\ndocument.querySelectorAll('[data-part]').forEach(el => { if (A && COPY.has(el.dataset.part)) el.innerHTML = A.content(el.dataset.part); });\nfunction status(){\n  const h = (A && A.host) || {}, u = (A && A.user) || {}, i = A && A.integrity, dl = document.getElementById('status');\n  const rows = [['runtime', A ? 'adp.js, build ' + A.build : 'not loaded'],\n    ['host', (h.id || 'static') + ' (' + (h.status || 'no provider') + ')'],\n    ['viewer', (u.id || 'anonymous') + (u.canEdit ? ', can edit' : ', read only')],\n    ['capabilities', ['records', 'comments', 'seedFiles', 'agent', 'publish', 'ask'].filter(k => h[k]).join(', ') || 'none'],\n    ['integrity', i ? i.verdict : 'not checked'],\n    ['seeded', A && A.seeded ? 'yes' : 'no']];\n  dl.textContent = '';\n  rows.forEach(([k, v]) => { const dt = document.createElement('dt'), dd = document.createElement('dd'); dt.textContent = k; dd.textContent = v; dl.append(dt, dd); });\n}\nstatus();\nif (A && A.config) A.config.ready.then(() => setTimeout(status, 300));\nif (A) A.page({view: () => 'home', expected: () => Object.keys(TITLES), titles: TITLES, legacy: {}, all: Object.keys(TITLES), reveal: () => Promise.resolve()});\n})();\n/* /part:page.script.app */\n",
 "styles/page.css.txt": "/* part:page.style */\n:root{--bg:#fafaf8;--panel:#fff;--ink:#1c1c1a;--ink-2:#55554f;--rule:#ddddd6;--accent:#2f5d50;--f-ui:system-ui,sans-serif;--f-mono:ui-monospace,monospace;--text-size:15px;--leading:1.5;--edge-w:1px;--space:16px;--radius:8px;--measure:760px;color-scheme:light}\n@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){--bg:#161614;--panel:#1e1e1b;--ink:#ecebe6;--ink-2:#b4b3ab;--rule:#34332e;--accent:#7cc4ad;color-scheme:dark}}\n:root[data-theme=\"dark\"]{--bg:#161614;--panel:#1e1e1b;--ink:#ecebe6;--ink-2:#b4b3ab;--rule:#34332e;--accent:#7cc4ad;color-scheme:dark}\nbody{margin:0 auto;max-width:var(--measure);padding:var(--space);background:var(--bg);color:var(--ink);font:var(--text-size)/var(--leading) var(--f-ui)}\nheader{border-bottom:var(--edge-w) solid var(--rule);padding-bottom:var(--space)}\nh1{margin:0}\n#views section{margin-top:var(--space);padding:var(--space);background:var(--panel);border:var(--edge-w) solid var(--rule);border-radius:var(--radius)}\ndl{display:grid;grid-template-columns:max-content 1fr;gap:calc(var(--space) / 4) var(--space)}\ndt{color:var(--ink-2)}\ndd{margin:0;font-family:var(--f-mono);overflow-wrap:anywhere}\na,summary{color:var(--accent)}\n/* /part:page.style */\n"}}
```

```json vector
{
 "vector": "templates",
 "run": [
  "adp.py",
  "templates"
 ],
 "exit": 0,
 "stdout_text": [
  "catalog    The minimal page, taking kit.badge from the catalog.",
  "           use when: Checking that `new` layers a template on a base, takes from a catalog and records what it took.",
  "minimal    The smallest adp/2 page: the shell, its copy as data, and a status list of what the runtime found (host, viewer, capabilities, integrity, seeding). Needs nothing from the catalog.",
  "           use when: Starting a page from the specification alone, or checking a build of the tools and the runtime on a real host."
 ]
}
```

```json vector
{
 "vector": "new-minimal",
 "steps": [
  {
   "run": [
    "adp.py",
    "new",
    "minimal",
    "{out}/kiln",
    "--title",
    "Kiln log",
    "--by",
    "agent-a"
   ],
   "exit": 0,
   "stdout": {
    "template": "minimal",
    "dir": "<tmp>/out/kiln",
    "title": "Kiln log",
    "slug": "kiln-log",
    "publish": {
     "file_path": "<tmp>/out/kiln/index.html",
     "root": "<tmp>/out/kiln",
     "files": {
      "adp.js": "adp.js",
      "content.js": "content.js",
      "seed.json": "seed.json",
      "parts/app.js": "parts/app.js",
      "seed/pack-001.json": "seed/pack-001.json",
      "styles/page.css": "styles/page.css"
     },
     "capabilities": {
      "db": {
       "rules": [
        {
         "path": "",
         "read": "view",
         "write": "admin"
        },
        {
         "path": "ns/shared",
         "read": "view",
         "write": "interact"
        },
        {
         "path": "ns/users/{self}",
         "read": "view",
         "write": "interact"
        }
       ]
      },
      "user": {},
      "comments": {
       "customAnchors": true
      },
      "artifact": {}
     }
    },
    "take": [],
    "design": "A token-only look with system fonts: the three theme blocks in styles/page.css. Keep the token names, the part markers and the What changed selectors adp.js fills (#wc, #wcN, #wcChanges, #wcDecisions, #wcIncoming); replace the Home section with the page's own views.",
    "next": [
     "adp.py check <tmp>/out/kiln",
     "Design it: read `design` above, take a theme and the layouts the content needs from the catalog, then write page.css and the views for this content (a script that emits them beats typing)",
     "Artifact publish with the `publish` arguments (first publish: add icon; label \"adp/2 start\")",
     "Open the page as an editor (you, or the owner): it expands seed.json and seed/ into its database on that first open and shows what ADP is while it does. Only when nobody can open it: adp.py seed <tmp>/out/kiln --batches prints the ArtifactData batches"
    ]
   }
  },
  {
   "run": [
    "adp.py",
    "check",
    "{out}/kiln"
   ],
   "exit": 0,
   "stdout_text": [
    "10 parts in 4 files, ok; 235 chars (5%) outside every part, hashed as _rest"
   ]
  },
  {
   "run": [
    "adp.py",
    "files",
    "{out}/kiln"
   ],
   "exit": 0,
   "stdout": {
    "file_path": "<tmp>/out/kiln/index.html",
    "root": "<tmp>/out/kiln",
    "files": {
     "adp.js": "adp.js",
     "content.js": "content.js",
     "seed.json": "seed.json",
     "parts/app.js": "parts/app.js",
     "seed/pack-001.json": "seed/pack-001.json",
     "styles/page.css": "styles/page.css"
    }
   }
  },
  {
   "run": [
    "adp.py",
    "seed",
    "{out}/kiln",
    "--by",
    "agent-a",
    "--dry-run"
   ],
   "exit": 0,
   "stdout": {
    "collections": {
     "parts": 10,
     "content": 2,
     "changes": 1,
     "agents": 1,
     "manifest": 1
    },
    "docs": 15,
    "batches": 1,
    "skipped_empty": [],
    "bytes": 5024
   }
  }
 ]
}
```

```json vector
{
 "vector": "new-refuses-a-non-empty-folder",
 "run": [
  "adp.py",
  "new",
  "minimal",
  "{page-a}"
 ],
 "exit": 1,
 "stderr_text": [
  "<tmp>/page-a exists and is not empty"
 ]
}
```

```json vector
{
 "vector": "new-full-tier-is-not-available",
 "run": [
  "adp.py",
  "new",
  "--tier",
  "full",
  "{out}/x"
 ],
 "exit": 1,
 "stderr_text": [
  "tier full is not available yet"
 ]
}
```

```json fixture
{"fixture": "template-catalog", "files": {"template.json": "{\n \"name\": \"catalog\",\n \"summary\": \"The minimal page, taking kit.badge from the catalog.\",\n \"use_when\": \"Checking that `new` layers a template on a base, takes from a catalog and records what it took.\",\n \"base\": \"minimal\",\n \"take\": [\n  \"kit.badge\"\n ],\n \"installed\": true,\n \"drop\": [\n  \"styles/page.css\"\n ]\n}\n", "notes.md.txt": "# {{title}} ({{slug}})\n", "info.txt.txt": "{{adp_version}}\n{{adp_sha12}}\n{{adp_sha}}\n{{adp_catalog}}\n{{adp_components}}\n"}}
```

The fixture `template-catalog` is a second template: it starts from `minimal`, adds a file, adds `info.txt` with the five info placeholders, drops one, takes `kit.badge` and records what it took.

```json vector
{
 "vector": "new-refuses-a-bad-slug",
 "run": [
  "adp.py",
  "new",
  "minimal",
  "{out}/x",
  "--slug",
  "Bad_Slug"
 ],
 "exit": 1,
 "stderr_text": [
  "--slug: lowercase kebab, e.g. status-pill"
 ]
}
```

```json vector
{
 "vector": "new-refuses-an-unknown-theme",
 "run": [
  "adp.py",
  "new",
  "minimal",
  "{out}/x",
  "--catalog",
  "{catalog-built}/catalog.json",
  "--url",
  "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
  "--theme",
  "nope"
 ],
 "exit": 1,
 "stderr_text": [
  "--theme nope: the catalog has no such theme. It has: paper"
 ]
}
```

```json vector
{
 "vector": "new-from-a-catalog",
 "run": [
  "adp.py",
  "new",
  "catalog",
  "{out}/p",
  "--title",
  "Kiln log",
  "--catalog",
  "{catalog-built}/catalog.json",
  "--url",
  "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
  "--theme",
  "paper",
  "--layout",
  "viz.meter",
  "--by",
  "agent-a"
 ],
 "exit": 0,
 "stdout": {
  "template": "catalog",
  "dir": "<tmp>/out/p",
  "title": "Kiln log",
  "slug": "kiln-log",
  "publish": {
   "file_path": "<tmp>/out/p/index.html",
   "root": "<tmp>/out/p",
   "files": {
    "adp.js": "adp.js",
    "content.js": "content.js",
    "info.txt": "info.txt",
    "installed.json": "installed.json",
    "notes.md": "notes.md",
    "seed.json": "seed.json",
    "parts/app.js": "parts/app.js",
    "seed/pack-001.json": "seed/pack-001.json",
    "kit/badge.js": {
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "path": "kit/badge.js"
    },
    "kit/badge.css": {
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "path": "kit/badge.css"
    },
    "kit/samples/kit.json": {
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "path": "kit/samples/kit.json"
    },
    "kit/themes/paper.css": {
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "path": "kit/themes/paper.css"
    },
    "kit/themes/paper.json": {
     "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "path": "kit/themes/paper.json"
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
   "capabilities": {}
  },
  "take": [
   "kit.badge",
   "theme.paper",
   "viz.meter"
  ],
  "design": "A token-only look with system fonts: the three theme blocks in styles/page.css. Keep the token names, the part markers and the What changed selectors adp.js fills (#wc, #wcN, #wcChanges, #wcDecisions, #wcIncoming); replace the Home section with the page's own views.",
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
   "theme.paper",
   "viz.meter"
  ],
  "next": [
   "adp.py check <tmp>/out/p",
   "Design it: read `design` above, take a theme and the layouts the content needs from the catalog, then write page.css and the views for this content (a script that emits them beats typing)",
   "Artifact publish with the `publish` arguments (first publish: add icon; label \"adp/2 start\"); its files already carry the kit entries",
   "Open the page as an editor (you, or the owner): it expands seed.json and seed/ into its database on that first open and shows what ADP is while it does. Only when nobody can open it: adp.py seed <tmp>/out/p --batches prints the ArtifactData batches"
  ]
 },
 "files_out": {
  "{out}/p/index.html": "<title>Kiln log</title>\n<meta name=\"adp:build\" content=\"1\">\n<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap\">\n<link rel=\"stylesheet\" href=\"kit/badge.css\">\n<link rel=\"stylesheet\" href=\"kit/viz/meter.css\">\n<link rel=\"stylesheet\" href=\"styles/page.css\">\n<link rel=\"stylesheet\" href=\"kit/themes/paper.css\">\n<!-- part:page.header -->\n<header data-part=\"page.header\" data-comment-target>\n<h1>Kiln log</h1>\n<!-- part:page.lead --><p data-part=\"page.lead\" data-comment-target></p><!-- /part:page.lead -->\n<!-- part:page.changes --><details id=\"wc\" data-part=\"page.changes\" data-comment-target hidden><summary>What changed <span id=\"wcN\"></span></summary><ol id=\"wcChanges\"></ol><ul id=\"wcDecisions\"></ul><ul id=\"wcIncoming\"></ul></details><!-- /part:page.changes -->\n</header>\n<!-- /part:page.header -->\n<!-- part:page.tabs --><nav data-part=\"page.tabs\" data-comment-target></nav><!-- /part:page.tabs -->\n<main id=\"views\">\n<!-- part:home --><section data-part=\"home\" data-comment-target>\n<!-- part:home.intro --><div data-part=\"home.intro\" data-comment-target></div><!-- /part:home.intro -->\n<!-- part:home.status --><dl id=\"status\" data-part=\"home.status\" data-comment-target></dl><!-- /part:home.status -->\n</section><!-- /part:home -->\n</main>\n<script src=\"content.js\"></script>\n<script src=\"adp.js\"></script>\n<script src=\"kit/badge.js\"></script>\n<script src=\"kit/viz/meter.js\"></script>\n<script src=\"parts/app.js\"></script>\n",
  "{out}/p/installed.json": {
   "schema": "installed/1",
   "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
   "ver": "",
   "built": "<time>",
   "take": [
    "kit.badge",
    "theme.paper",
    "viz.meter"
   ],
   "entries": [
    {
     "id": "kit.badge",
     "name": "Status badge",
     "kind": "component",
     "group": "Board kit",
     "summary": "A small label coloured by a meaning token.",
     "version": "0.1.0",
     "requires": []
    },
    {
     "id": "theme.paper",
     "name": "Paper",
     "kind": "theme",
     "group": "Themes",
     "summary": "Warm paper by day, ink-blue by night, one green accent.",
     "version": "0.1.0",
     "requires": []
    },
    {
     "id": "viz.meter",
     "name": "Meter",
     "kind": "component",
     "group": "Visualizations",
     "summary": "A bar that states its value and range in words, with a status badge.",
     "version": "0.1.0",
     "requires": [
      "kit.badge"
     ]
    }
   ]
  },
  "{out}/p/notes.md": "# Kiln log (kiln-log)\n",
  "{out}/p/info.txt": "unknown\n<adp.js sha12>\n<adp.js sha>\nnone saved yet: python3 adp.py catalog &lt;url&gt; saves the owner&#x27;s catalog url\n<tr><td>kit.badge</td><td>0.1.0</td><td>04fb713a8c9d</td></tr><tr><td>theme.paper</td><td>0.1.0</td><td>de7027176d74</td></tr><tr><td>viz.meter</td><td>0.1.0</td><td>c53c2c95d630</td></tr>\n"
 }
}
```

```json vector
{
 "vector": "take-fetches-missing-headers",
 "steps": [
  {
   "copy": [
    "{catalog-index-only}",
    "{home}/catalog"
   ]
  },
  {
   "run": [
    "adp.py",
    "take",
    "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
    "viz.meter"
   ],
   "exit": 0,
   "stdout": {
    "catalog": {
     "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
     "index": "<tmp>/home/catalog/catalog.json",
     "live": true,
     "ver": null,
     "built": "<time>"
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
    "fetch_headers": [
     {
      "tool": "Artifact",
      "action": "read",
      "url": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
      "paths": [
       "kit/viz/meter.js"
      ],
      "out_dir": "<tmp>/home/catalog",
      "then": "run the command again"
     }
    ]
   }
  }
 ]
}
```

The fixture `config-links` is a page configuration that sets `links.catalog`, the url `take` uses for a local index.

```json fixture
{"fixture": "config-links", "files": {"c.json": "{\"values\": {\"links.catalog\": \"https://claude.ai/artifact/00000000-0000-4000-8000-000000000002\"}}"}}
```

```json vector
{
 "vector": "take-url-from-config",
 "run": [
  "adp.py",
  "take",
  "{catalog-built}/catalog.json",
  "kit.badge",
  "--config",
  "{config-links}/c.json"
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
   "kit.badge"
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
   "kit/samples/kit.json": {
    "artifact": "https://claude.ai/artifact/00000000-0000-4000-8000-000000000002",
    "path": "kit/samples/kit.json"
   }
  },
  "sha256": {
   "kit/badge.js": "18ba1a867d82bc9e28b399fdc6a9fc306f6b79252d5d88f7d9035e681fa040ab",
   "kit/badge.css": "e36fc8a443380c6dea1dfad9be19b7c67d72c6e735d471c546115c182d00478c",
   "kit/samples/kit.json": "754630b80636553bc207c5aa66fd12263e9e2c344e55372c7ad61ad827c32ce8"
  },
  "samples": {
   "kit.badge": [
    "kit/samples/kit.json#badge"
   ]
  }
 }
}
```

