---
name: adp-minimal-kit
description: "Reference for the ADP (Artifacts Done Properly) kit: the folders and id prefixes of kit entries (components, visualizations, layouts, patterns, themes, templates, guides), how an entry's files, part markers and sample bundle are laid out, and how a page takes an entry with adp.py take, links its files in dependency order, mounts it with its @config signature, styles it with theme tokens and persists through ADP.db. Use when the user asks what the kit contains, what an entry is, or how to load and mount one on a page."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The kit: structure, and how an entry wires into a page

The **kit** is the set of reusable entries that ADP (Artifacts Done Properly) pages take instead of rewriting. It lives in a catalog under
`kit/`. The examples below use the catalog that this plugin ships as a fixture (`catalog-a` in
[the catalog's vectors](../adp-minimal-catalog/vectors.md)): a component, a visualization that requires it, a theme and a guide.

```
kit/
  badge.js, badge.css        kit.badge       a component: a small label coloured by a status token
  viz/meter.js, meter.css    viz.meter       a visualization: a bar that states its value in words; requires kit.badge
  themes/paper.css, .json    theme.paper     a theme: tokens only, and its JSON twin
  guides/reading.md          guide.reading   a guide in Markdown
  samples/kit.json           the sample bundle of the kit/ root entries (key "badge")
  samples/viz.json           the sample bundle of kit/viz/ (key "meter")
```

A larger catalog uses the same layout with more folders: `layout/` (frames of a page or region), `patterns/` (recurring interactions built from
components, often reading or writing the [record](../adp-minimal-protocol/SKILL.md#the-record)) and `templates/` (starting pages).

## Prefixes and kinds

An entry's id prefix says which folder it lives in; the header's `@kind` says what the [catalog](../adp-minimal-catalog/SKILL.md#the-header)
does with it (`component`, `theme`, `template` or `guide`). `adp.py kit list` reports the prefix as `kind`, and `--kind viz` filters on it.

| Prefix | Folder | `@kind` | Example |
|---|---|---|---|
| `kit.` | `kit/` | `component` | `kit.badge` |
| `viz.` | `kit/viz/` | `component` | `viz.meter` |
| `layout.` | `kit/layout/` | `component` | |
| `pattern.` | `kit/patterns/` | `component` | |
| `theme.` | `kit/themes/` | `theme` | `theme.paper` |
| `template.` | `kit/templates/` | `template` | |
| `guide.` | `kit/guides/` | `guide` | `guide.reading` |
| `runtime.` | the catalog root | `component` | the catalog's copy of `adp.js` |

`kit list --kind` also accepts an `@kind` value. `adp.py kit list CATALOG` prints one JSON line per entry (`id`, `kind`, `name`, `summary`, `tags`);
CATALOG is the catalog URL, `-` for the
catalog saved by `adp.py catalog`, or a local `catalog.json`, which it reads with a warning ([catalog](../adp-minimal-catalog/SKILL.md#using-the-catalog)).

## One entry, as files

An entry is a **main file** carrying its [header](../adp-minimal-catalog/SKILL.md#the-header) plus the files the header's `@files` names:

```
kit/viz/meter.js       main file: /* part:page.script.kit.viz.meter */, then the header comment, then the code
kit/viz/meter.css      its style, between page.style.kit.viz.meter markers
kit/samples/viz.json   the sample bundle of kit/viz/; the entry owns the key "meter"
```

Kit files are parts too: their code sits between `part:page.script.<id>` and `part:page.style.<id>` markers, so tooling and diffs can attribute
every change to a specific part.

## How an entry wires into a page

1. **Take it.** `adp.py take CATALOG viz.meter --url CATALOG_URL` resolves `@requires` first and prints JSON: `entries` in dependency order
   (`kit.badge`, then `viz.meter`), a `files` map of `{"artifact": <catalog url>, "path": <file>}` references, their `sha256`, and under `samples`
   the `path#key` references of the entries you named. The sample bundles of the named entries are in `files`; those of entries pulled in by
   `@requires` are not. `take` writes nothing locally: pass `files` to the Artifact publish call and the host copies those files into the page's
   artifact server-side. A taken file is published with the page, but the page does not load it until step 2.
2. **Link it** in `index.html` in `entries` order: each taken `.css` as `<link>`, each `.js` as `<script src>`, all scripts before `parts/app.js`.
   Stylesheets go in this order: the entries' own, then `styles/page.css`, then the theme last. A global such as `Kit.meter` is defined only
   after its script has run.
3. **Mount it** from the page's code with the signature in the header's `@config` (`Kit.meter.draw(el, opts) | value, max, label`):

```html
<link rel="stylesheet" href="kit/badge.css">
<link rel="stylesheet" href="kit/viz/meter.css">
<link rel="stylesheet" href="styles/page.css">
<link rel="stylesheet" href="kit/themes/paper.css">
...
<div id="loads"></div>
<script src="content.js"></script>
<script src="adp.js"></script>
<script src="kit/badge.js"></script>
<script src="kit/viz/meter.js"></script>
<script src="parts/app.js"></script>   <!-- Kit.meter.draw(document.getElementById('loads'), {value: 5, max: 10, label: 'Kiln loads'}) -->
```

4. **Style it with tokens.** An entry colors and sizes itself only with tokens, and lists the ones it reads in `@tokens` (`viz.meter`:
   `--panel --ink --accent --f-ui`). The page's theme sets them, so switching the theme restyles every entry on the page
   ([themes](../adp-minimal-themes/SKILL.md)).
5. **Persist through the runtime.** An entry that reads or writes the record uses `ADP.db`, `ADP.user`, `ADP.agent()` and the other `ADP.*` APIs,
   never the host API (`window.claude`) directly ([host adapters](../adp-minimal-hosts/SKILL.md)). Its header's `@db` field lists the collections
   it reads and writes, or `none`.

An entry's function may return a handle (`Kit.badge.render` returns `{destroy}`; `Kit.meter.draw` returns nothing). The header's first
paragraph says what it returns; `@provides` names the functions.

## `take`

`take CATALOG ID... [--url URL] [--config C.json]` reads the catalog's index and resolves each id's `@requires` first. CATALOG is a catalog url (the index `adp.py catalog` fetched
into `ADP_HOME/catalog/`; when it is not there, `take` prints the `Artifact read` that fetches it and exits 2), `-` for the saved catalog (none saved: exit 1, `take: no saved catalog; ...`), or a
local `catalog.json` (a path that is no file exits 1), whose url is `--url`, else `links.catalog` of the `--config` document, else the index's own `url`; with none it exits 1 with `take: no catalog url. ...`. An unknown id exits 1 with `no entry ID in CATALOG`; no ids prints the usage line and exits 1; a cycle in `@requires` ends at the id already visited. A `files` ref carries the entry file's pinned `ver` when the index has one. It prints `catalog`, `entries` in dependency order, the `files` map, `sha256`, `samples` (the `@preview` refs of the keys the
named entries own in `@samples`, read from each entry's `main`, else its template, doc, script or style file; `fetch_headers` lists the `Artifact read` of main files not on disk yet) and, for themes, `fonts`. A sample bundle is in `files` only for a named entry, and not when the entry only borrows it for its preview.

```python
# ---
# id: kit.take
# tool: adp.py
# section: kit
# order: 620
# needs: [core.options, core.io, protocol.switches]
# tests: [take-with-its-requires, take-a-local-index-needs-a-url, take-unknown, take-fetches-missing-headers, take-url-from-config, take-index-quirks]
# sha: 17c1a45228d0
# ---
CAT_URL = re.compile(r'https://claude\.ai/(?:code/)?artifact/[A-Za-z0-9-]+/?')


def saved_catalog():
    p = Path(ADP_HOME, 'config.json')
    return read_json(p).get('catalog') if p.is_file() else None


def head_file(e):
    """The file that carries an entry's header (its `main`, else its template, script or style); None when it has none or it points outside the catalog."""
    m = header_lib().main_file(e)
    return m if m and not m.startswith('/') and '..' not in m.split('/') else None


def entry_head(root, e):
    """(the keys `@samples` names, the `@preview` sample refs) of an entry's header file; None when the file is not on disk."""
    main = head_file(e)
    if not main or not (root / main).is_file(): return None
    text = (root / main).read_text(encoding='utf-8', errors='replace')
    keys, view = re.search(r'@samples\s+(.+)', text), re.search(r'@preview\s+(\{.*\})', text)
    return [k.strip() for k in keys.group(1).split(',')] if keys else [], json.loads(view.group(1)).get('samples', []) if view else []


def taken(src, ids, url=None, config=None):
    """(result, exit code) of `take`: the entries `ids` need, in dependency order, and the files map that publishes them."""
    src = saved_catalog() or sys.exit('take: no saved catalog; adp.py catalog <url> saves one') if src == '-' else src
    live = bool(CAT_URL.fullmatch(src))
    idx = cat_dir(src) / 'catalog.json' if live else Path(src)
    url = src.rstrip('/') if live else url
    if not idx.is_file():
        if not live: sys.exit(f'take: {src} is neither a catalog url nor a catalog.json')
        return {'error': 'index not fetched', 'catalog': url, 'fetch': {'tool': 'Artifact', 'action': 'read', 'url': url,
                'path': 'catalog.json', 'out_dir': str(idx.parent)}}, 2
    cat = read_json(idx)
    url = url or (switches(unwrap(read_json(config))).get('links.catalog') if config else None) or cat.get('url')
    if not url: sys.exit('take: no catalog url. Pass the catalog url as CATALOG (then the index is the live one), or --url with a local index')
    by, order, seen = {e['id']: e for e in cat['entries']}, [], set()

    def visit(i):
        if i in seen: return
        if i not in by: sys.exit(f'no entry {i} in {src}')
        seen.add(i)
        for r in by[i].get('requires', []): visit(r)
        order.append(i)
    for i in ids: visit(i)
    named = [by[i] for i in ids if any(f.get('role') == 'sample' for f in by[i]['files'])]
    heads = {e['id']: entry_head(idx.parent, e) for e in named}
    own = {i: [r for r in h[1] if r.split('#')[-1] in h[0]] for i, h in heads.items() if h}
    idle = {i: {r.split('#')[0] for r in h[1]} - {r.split('#')[0] for r in own[i]} for i, h in heads.items() if h}   # a bundle borrowed for the preview only
    files = {f['path']: {'artifact': url, 'path': f['path'], **({'ver': f['ver']} if f.get('ver') else {})} for i in order for f in by[i]['files']
             if f.get('role') != 'sample' or (i in ids and f['path'] not in idle.get(i, ()))}
    out = {'catalog': {'url': url, 'index': str(idx.resolve()), 'live': live, 'ver': cat.get('ver') or None, 'built': cat.get('built')},
           'entries': order, 'files': files,
           'sha256': {f['path']: f['sha256'] for i in order for f in by[i]['files'] if f['path'] in files and f.get('sha256')}}
    if not live: out['catalog']['warning'] = ('a local index is a build, not the live catalog: a file it lists may be missing there. '
                                              'adp.py take <catalog url> ... reads the fetched live index')
    if any(own.values()): out['samples'] = {i: r for i, r in own.items() if r}
    if live and (want := [m for e in named if heads[e['id']] is None and (m := head_file(e))]):
        out['fetch_headers'] = [{'tool': 'Artifact', 'action': 'read', 'url': url, 'paths': want, 'out_dir': str(idx.parent), 'then': 'run the command again'}]
    if fonts := {i: by[i]['fonts'] for i in order if by[i].get('fonts')}: out['fonts'] = fonts
    return out, 0


@cmd('take')
def take(a):
    """take CATALOG ID ... [--url URL] [--config C.json]    the entries and their requires, as the files map that publishes them"""
    src, *ids = bare(a) or ['']
    if not ids: sys.exit('usage: adp.py take CATALOG ID ... [--url URL] [--config C.json]   CATALOG: the catalog url, - (saved), or a local catalog.json')
    out, code = taken(src, ids, opt(a, '--url'), opt(a, '--config'))
    emit(out); return code
```

## Layouts and tokens

A layout owns geometry and publishes it as a token of its own (a top bar writing its height to a custom property that the frames below read), so
layouts combine through those properties, not by overriding each other's CSS. Every token an entry reads is either in the
[token contract](../adp-minimal-themes/SKILL.md#the-token-contract) or declared in its `@tokens`, so any entry works with any theme that meets the
contract.

## Samples

An entry shows itself with sample data, kept in its folder's bundle (`kit/samples/<folder>.json`, `kit.json` for the `kit/` root; one JSON
object, one key per entry). The header names the bundle in `@files`, and the key in `@samples` and `@preview`:

```
 * @files     kit/viz/meter.css, kit/samples/viz.json
 * @preview   {"render": "viz.meter", "samples": ["kit/samples/viz.json#meter"]}
 * @samples   meter
```

Under its key, an entry keeps several samples (`viz.meter`: `half`, `full`, `zero`), covering the typical, the extreme and the empty case. Sample
data is invented, never taken from a real project.

## Where to look next

[catalog](../adp-minimal-catalog/SKILL.md) for the index and its checks, [themes](../adp-minimal-themes/SKILL.md) for tokens, and
[kit authoring](../adp-minimal-kit-authoring/SKILL.md) for adding an entry.
