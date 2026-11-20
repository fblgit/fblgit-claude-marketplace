# Vectors: adp-minimal-new-artifact

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

## Contract: `new`

```json vector
{
 "vector": "templates",
 "run": [
  "adp.py",
  "templates"
 ],
 "exit": 0,
 "stdout_text": [
  "assistant  A page with Claude capabilities enabled out of the box: a Work with Claude pane (pick a block, say what you want, send it to a watching Claude Code session or ask now), a Requests view that follows every request, a line saying whether a session is watching, and every catalog theme with a switch in the header.",
  "           use when: Any shared artifact where people should be able to point at a part of the page and have Claude change it, answer about it or fix it, without leaving the page.",
  "default    The assistant plus every theme, the canvas, 3D and the most useful common kits, so you can build your own page or tune an existing one.",
  "           use when: Starting a page of your own, or reshaping an existing one, when you want the whole toolbox taken and at hand.",
  "starter    A blank adp/2 artifact that opens on a welcome view: shell, runtime, copy as data, one view, What changed panel.",
  "           use when: Any new artifact that will be revised, commented on or worked on by more than one agent."
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
    "--tier",
    "minimal",
    "{out}/kiln",
    "--title",
    "Kiln log",
    "--by",
    "agent-a"
   ],
   "exit": 0,
   "stdout": {
    "template": "starter",
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
    "take": [
     "kit.dom",
     "kit.tokens",
     "kit.vocab",
     "pattern.settings",
     "pattern.inbox",
     "pattern.namespaces"
    ],
    "design": "The scaffold's look is the catalog page's shell (a specimen book: proofing-paper greys, carmine accent, Bricolage Grotesque, Atkinson Hyperlegible Next, IBM Plex Mono). It is where a page starts, not its design: never let two pages built from it look the same. Keep the token names, the three theme blocks, the part markers and the selectors adp.js and the settings pattern rely on (.wc*, .gear, .settings-view). Take a theme (theme.*) and the layout.*, pattern.* and viz.* entries this content needs from the catalog by reference; write the rest of styles/page.css and the views for this content, with a short script that emits them from the content rather than by typing.",
    "next": [
     "adp.py check <tmp>/out/kiln",
     "Design it: read `design` above, take a theme and the layouts the content needs from the catalog, then write page.css and the views for this content (a script that emits them beats typing)",
     "Artifact publish with the `publish` arguments (first publish: add icon; label \"adp/2 start\")",
     "adp.py take <catalog url> kit.dom kit.tokens kit.vocab pattern.settings pattern.inbox pattern.namespaces, then publish those files to the same url",
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
    "19 parts in 4 files, ok; 5970 chars (26%) outside every part, hashed as _rest"
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
     "parts": 19,
     "content": 5,
     "changes": 1,
     "agents": 1,
     "manifest": 1
    },
    "docs": 27,
    "batches": 1,
    "skipped_empty": [],
    "bytes": 10903
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
  "--tier",
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
