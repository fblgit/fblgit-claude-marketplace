# Vectors: adp-minimal-parts

The fixtures and vectors of the contracts in [SKILL.md](SKILL.md). The runner in [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) reads them; they are checked against the real ADP tools.

## Contract: `check`, `manifest`, `diff`, `diff-pages`

```json fixture
{"fixture": "page-a", "files": {
 "index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hi</p><!-- /part:home.lead --></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
 "parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
 "styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n"}}
```

```json fixture
{"fixture": "page-a2", "files": {
 "index.html": "<header data-part=\"page.header\"><!-- part:page.header --><h1>Board</h1><!-- /part:page.header --></header>\n<!-- part:home --><section data-part=\"home\" data-comment-target><!-- part:home.lead --><p data-part=\"home.lead\" data-comment-target>Hello</p><!-- /part:home.lead --><p>new, unmarked</p></section><!-- /part:home -->\n<script src=\"parts/app.js\"></script>\n",
 "parts/app.js": "/* part:page.script.app */\nconsole.log(1);\n/* /part:page.script.app */\n",
 "styles/page.css": "/* part:page.style */ body { margin: 0 } /* /part:page.style */\n"}}
```

```json fixture
{"fixture": "one", "files": {"page.html": "<!doctype html><html><body>\n<!-- part:a.one -->\n<p data-part=\"a.one\">One <b>x</b></p>\n<!-- part:a.two -->  <p data-part=\"a.two\">Two</p>\n<!-- /part:a.two -->\n<!-- /part:a.one -->\noutside   text\n<script>\n/* part:page.script */ let x = 1; /* /part:page.script */\n</script></body></html>\n"}}
```

```json fixture
{"fixture": "bad", "files": {
 "unclosed.html": "<!-- part:x --><p data-part=\"x\">x</p>\n",
 "twice.html": "<!-- part:x --><!-- part:x --><p data-part=\"x\">x</p><!-- /part:x -->\n",
 "orphan.html": "<p data-part=\"y\">no markers</p>\n",
 "nodatapart.html": "<!-- part:z --><p>z</p><!-- /part:z -->\n"}}
```

```json fixture
{"fixture": "manifests", "files": {
 "old.json": "{\"page_hash\": \"aaaaaaaaaaaa\", \"parts\": {\"a\": \"111111111111\", \"a.b\": \"222222222222\", \"gone\": \"333333333333\"}, \"elements\": {\"a\": 2}, \"files\": {\"index.html\": \"999999999999\"}, \"parents\": {\"a\": \"\", \"a.b\": \"a\", \"gone\": \"\"}}",
 "new.json": "{\"page_hash\": \"bbbbbbbbbbbb\", \"parts\": {\"a\": \"444444444444\", \"a.b\": \"555555555555\", \"fresh\": \"666666666666\"}, \"elements\": {\"a\": 3}, \"files\": {\"index.html\": \"888888888888\"}, \"parents\": {\"a\": \"\", \"a.b\": \"a\", \"fresh\": \"\"}}"}}
```

```json vector
{
 "vector": "check-dir",
 "run": [
  "adp.py",
  "check",
  "{page-a}"
 ],
 "exit": 0,
 "stdout_text": [
  "5 parts in 3 files, ok; 78 chars (17%) outside every part, hashed as _rest",
  "  warning: 1 part roots without data-comment-target: page.header"
 ]
}
```

```json vector
{
 "vector": "check-single",
 "run": [
  "adp.py",
  "check",
  "{one}/page.html"
 ],
 "exit": 0,
 "stdout_text": [
  "3 parts, ok; 73 chars (26%) outside every part, hashed as _rest",
  "  warning: 2 part roots without data-comment-target: a.one, a.two"
 ]
}
```

```json vector
{
 "vector": "check-unclosed",
 "run": [
  "adp.py",
  "check",
  "{bad}/unclosed.html"
 ],
 "exit": 1,
 "stdout_text": [
  "0 parts",
  "  part x never closed",
  "  data-part=\"x\" has no part:x markers (a new piece nobody marked)",
  "  warning: 1 part roots without data-comment-target: x"
 ]
}
```

```json vector
{
 "vector": "check-opened-twice",
 "run": [
  "adp.py",
  "check",
  "{bad}/twice.html"
 ],
 "exit": 1,
 "stdout_text": [
  "1 parts",
  "  line 1: part x opened twice",
  "  part x never closed",
  "  warning: 1 part roots without data-comment-target: x"
 ]
}
```

```json vector
{
 "vector": "check-data-part-without-markers",
 "run": [
  "adp.py",
  "check",
  "{bad}/orphan.html"
 ],
 "exit": 1,
 "stdout_text": [
  "0 parts",
  "  data-part=\"y\" has no part:y markers (a new piece nobody marked)",
  "  warning: 1 part roots without data-comment-target: y"
 ]
}
```

```json vector
{
 "vector": "check-part-without-data-part",
 "run": [
  "adp.py",
  "check",
  "{bad}/nodatapart.html"
 ],
 "exit": 1,
 "stdout_text": [
  "1 parts",
  "  part z: no data-part=\"z\" in the page"
 ]
}
```

```json vector
{
 "vector": "manifest-dir",
 "run": [
  "adp.py",
  "manifest",
  "{page-a}"
 ],
 "exit": 0,
 "stdout": {
  "schema": "adp/2",
  "page_hash": "7f4556515dd9",
  "parts": {
   "_rest:index.html": "ee2d7cd8fa75",
   "_rest:parts/app.js": "e3b0c44298fc",
   "_rest:styles/page.css": "e3b0c44298fc",
   "home": "081b78b8f894",
   "home.lead": "c6a82a517ff8",
   "page.header": "0d957e9aee8d",
   "page.script.app": "35c146f76e12",
   "page.style": "997faceca260"
  },
  "files": {
   "index.html": "bd002c3d502b",
   "parts/app.js": "574c60bebc47",
   "styles/page.css": "56ee869c6a7b"
  },
  "parents": {
   "_rest:index.html": "",
   "_rest:parts/app.js": "",
   "_rest:styles/page.css": "",
   "home": "",
   "home.lead": "home",
   "page.header": "",
   "page.script.app": "",
   "page.style": ""
  },
  "elements": {
   "_rest:index.html": 2,
   "_rest:parts/app.js": 0,
   "_rest:styles/page.css": 0,
   "home": 1,
   "home.lead": 1,
   "page.header": 1,
   "page.script.app": 0,
   "page.style": 0
  },
  "part_file": {
   "_rest:index.html": "index.html",
   "_rest:parts/app.js": "parts/app.js",
   "_rest:styles/page.css": "styles/page.css",
   "home": "index.html",
   "home.lead": "index.html",
   "page.header": "index.html",
   "page.script.app": "parts/app.js",
   "page.style": "styles/page.css"
  }
 }
}
```

```json vector
{
 "vector": "manifest-single",
 "run": [
  "adp.py",
  "manifest",
  "{one}/page.html"
 ],
 "exit": 0,
 "stdout": {
  "schema": "adp/1",
  "page_hash": "0eaae72148c3",
  "parts": {
   "_rest": "67ea429e991b",
   "a.one": "6193e96bef72",
   "a.two": "f67648d6310e",
   "page.script": "aad7378dfeb8"
  },
  "files": {},
  "parents": {
   "a.one": "",
   "a.two": "a.one",
   "page.script": "",
   "_rest": ""
  },
  "elements": {
   "_rest": 3,
   "a.one": 2,
   "a.two": 1,
   "page.script": 0
  }
 }
}
```

```json vector
{
 "vector": "diff-manifests",
 "run": [
  "adp.py",
  "diff",
  "{manifests}/old.json",
  "{manifests}/new.json"
 ],
 "exit": 0,
 "stdout": {
  "page_hash": [
   "aaaaaaaaaaaa",
   "bbbbbbbbbbbb"
  ],
  "added": [
   "fresh"
  ],
  "removed": [
   "gone"
  ],
  "changed": [
   "a.b",
   "a"
  ],
  "deepest": [
   "a.b",
   "fresh",
   "gone"
  ],
  "elements": {
   "a": "+1"
  },
  "files": {
   "index.html": [
    "999999999999",
    "888888888888"
   ]
  }
 }
}
```

```json vector
{
 "vector": "diff-pages-dir",
 "run": [
  "adp.py",
  "diff-pages",
  "{page-a}",
  "{page-a2}"
 ],
 "exit": 0,
 "stdout": {
  "page_hash": [
   "7f4556515dd9",
   "c125279381ff"
  ],
  "added": [],
  "removed": [],
  "changed": [
   "home.lead",
   "home"
  ],
  "deepest": [
   "home.lead"
  ],
  "elements": {
   "home": "+1"
  },
  "files": {
   "index.html": [
    "bd002c3d502b",
    "a56efc30baaf"
   ]
  },
  "detail": {
   "home.lead": [
    "-Hi",
    "+Hello"
   ]
  }
 }
}
```
