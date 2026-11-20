# Vectors: adp-minimal-new-artifact

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

## Contract: `new`

The template `new` builds from, installed as `templates/minimal/` beside the tool (files ending `.txt` are written without it):

```json fixture
{"fixture": "template-minimal", "files": {
 "template.json": "{\n \"name\": \"minimal\",\n \"summary\": \"The smallest adp/2 page: the shell, its copy as data, and a status list of what the runtime found (host, viewer, capabilities, integrity, seeding). Needs nothing from the catalog.\",\n \"use_when\": \"Starting a page from the specification alone, or checking a build of the tools and the runtime on a real host.\",\n \"design\": \"A token-only look with system fonts: the three theme blocks in styles/page.css. Keep the token names, the part markers and the What changed selectors adp.js fills (#wc, #wcN, #wcChanges, #wcDecisions, #wcIncoming); replace the Home section with the page's own views.\",\n \"capabilities\": {\"db\": {\"rules\": [{\"path\": \"\", \"read\": \"view\", \"write\": \"admin\"}, {\"path\": \"ns/shared\", \"read\": \"view\", \"write\": \"interact\"}, {\"path\": \"ns/users/{self}\", \"read\": \"view\", \"write\": \"interact\"}]}, \"user\": {}, \"comments\": {\"customAnchors\": true}, \"artifact\": {}},\n \"take\": []\n}\n",
 "index.html.txt": "<title>{{title}}</title>\n<meta name=\"adp:build\" content=\"1\">\n<link rel=\"stylesheet\" href=\"styles/page.css\">\n<!-- part:page.header -->\n<header data-part=\"page.header\" data-comment-target>\n<h1>{{title}}</h1>\n<!-- part:page.lead --><p data-part=\"page.lead\" data-comment-target></p><!-- /part:page.lead -->\n<!-- part:page.changes --><details id=\"wc\" data-part=\"page.changes\" data-comment-target hidden><summary>What changed <span id=\"wcN\"></span></summary><ol id=\"wcChanges\"></ol><ul id=\"wcDecisions\"></ul><ul id=\"wcIncoming\"></ul></details><!-- /part:page.changes -->\n</header>\n<!-- /part:page.header -->\n<!-- part:page.tabs --><nav data-part=\"page.tabs\" data-comment-target></nav><!-- /part:page.tabs -->\n<main id=\"views\">\n<!-- part:home --><section data-part=\"home\" data-comment-target>\n<!-- part:home.intro --><div data-part=\"home.intro\" data-comment-target></div><!-- /part:home.intro -->\n<!-- part:home.status --><dl id=\"status\" data-part=\"home.status\" data-comment-target></dl><!-- /part:home.status -->\n</section><!-- /part:home -->\n</main>\n<script src=\"content.js\"></script>\n<script src=\"adp.js\"></script>\n<script src=\"parts/app.js\"></script>\n",
 "content.js.txt": "/* part:page.script.content */\n/* The page's copy, by part id. The record's content/<id> documents override it live, with no republish. */\nwindow.ADP_CONTENT = {\n \"page.lead\": {\"part\": \"page.lead\", \"title\": \"Lead\", \"html\": \"A minimal ADP page. Replace this line with what the page is for.\"},\n \"home.intro\": {\"part\": \"home.intro\", \"title\": \"Introduction\", \"html\": \"<p>Every section of this page has a part id, its copy lives in the record, and every publish is recorded. The list below is what the runtime found on this host.</p>\"}\n};\n/* /part:page.script.content */\n",
 "parts/app.js.txt": "/* part:page.script.app */\n/* The page's code: paint the copy, list what the runtime found, register the page. Replace the Home section with the page's own views. */\n(function(){\n'use strict';\nconst A = window.ADP, COPY = new Set(Object.keys(window.ADP_CONTENT || {}));\nconst TITLES = {'page.header': 'Header', 'page.lead': 'Lead', 'page.changes': 'What changed', 'page.tabs': 'Views',\n  home: 'Home', 'home.intro': 'Introduction', 'home.status': 'Status'};\ndocument.querySelectorAll('[data-part]').forEach(el => { if (A && COPY.has(el.dataset.part)) el.innerHTML = A.content(el.dataset.part); });\nfunction status(){\n  const h = (A && A.host) || {}, u = (A && A.user) || {}, i = A && A.integrity, dl = document.getElementById('status');\n  const rows = [['runtime', A ? 'adp.js, build ' + A.build : 'not loaded'],\n    ['host', (h.id || 'static') + ' (' + (h.status || 'no provider') + ')'],\n    ['viewer', (u.id || 'anonymous') + (u.canEdit ? ', can edit' : ', read only')],\n    ['capabilities', ['records', 'comments', 'seedFiles', 'agent', 'publish', 'ask'].filter(k => h[k]).join(', ') || 'none'],\n    ['integrity', i ? i.verdict : 'not checked'],\n    ['seeded', A && A.seeded ? 'yes' : 'no']];\n  dl.textContent = '';\n  rows.forEach(([k, v]) => { const dt = document.createElement('dt'), dd = document.createElement('dd'); dt.textContent = k; dd.textContent = v; dl.append(dt, dd); });\n}\nstatus();\nif (A && A.config) A.config.ready.then(() => setTimeout(status, 300));\nif (A) A.page({view: () => 'home', expected: () => Object.keys(TITLES), titles: TITLES, legacy: {}, all: Object.keys(TITLES), reveal: () => Promise.resolve()});\n})();\n/* /part:page.script.app */\n",
 "styles/page.css.txt": "/* part:page.style */\n:root{--bg:#fafaf8;--panel:#fff;--ink:#1c1c1a;--ink-2:#55554f;--rule:#ddddd6;--accent:#2f5d50;--f-ui:system-ui,sans-serif;--f-mono:ui-monospace,monospace;--space:16px;color-scheme:light}\n@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){--bg:#161614;--panel:#1e1e1b;--ink:#ecebe6;--ink-2:#b4b3ab;--rule:#34332e;--accent:#7cc4ad;color-scheme:dark}}\n:root[data-theme=\"dark\"]{--bg:#161614;--panel:#1e1e1b;--ink:#ecebe6;--ink-2:#b4b3ab;--rule:#34332e;--accent:#7cc4ad;color-scheme:dark}\nbody{margin:0 auto;max-width:760px;padding:var(--space);background:var(--bg);color:var(--ink);font:15px/1.5 var(--f-ui)}\nheader{border-bottom:1px solid var(--rule);padding-bottom:var(--space)}\nh1{margin:0}\n#views section{margin-top:var(--space);padding:var(--space);background:var(--panel);border:1px solid var(--rule);border-radius:8px}\ndl{display:grid;grid-template-columns:max-content 1fr;gap:4px 16px}\ndt{color:var(--ink-2)}\ndd{margin:0;font-family:var(--f-mono);overflow-wrap:anywhere}\na,summary{color:var(--accent)}\n/* /part:page.style */\n"}}
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
