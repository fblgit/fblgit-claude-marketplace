---
name: adp-catalog
description: "Reference for the ADP catalog: the catalog folder, catalog.json (kit-catalog/2) entries with their files, roles and hashes, the header each entry's main file carries and its tags, adp_catalog.py (check, build, headers, drift, inventory) and what it fails on, My Own Kit (the user's local copy of the catalog in ~/.adp/catalog), reading entries with kit, suggest and take, and why a published catalog changes by proposal. Use when the user asks what catalog.json holds, how headers work, how to verify a catalog, or how to fetch and take entries."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Catalog: format and consistency checks

The catalog is a published artifact that holds ADP's reusable kit entries and their index, `catalog.json`. Pages reference catalog files; they never copy them.

```
catalog/
  catalog.json     the index (schema kit-catalog/2): url, ver, built, entries[]
  index.html       the catalog page: browse, preview, take
  adp.js           the runtime, byte-identical to the one pages get
  content.js parts/ styles/   the catalog page's own parts
  kit/             the building blocks ([kit](../adp-kit/SKILL.md))
```

## The index

Each entry in `catalog.json`; this is `kit.badge` as `build` writes it from the fixture `catalog-a` ([vectors](vectors.md)):

```json
{ "id": "kit.badge", "kind": "component", "group": "Board kit", "name": "Status badge",
  "summary": "A small label coloured by a meaning token.", "tags": ["badge", "status", "label"],
  "status": "new", "version": "0.1.0", "requires": [], "globals": [], "provides": ["Kit.badge.render"],
  "main": "kit/badge.js",
  "files": [ {"path": "kit/badge.js",         "role": "script", "sha256": "18ba1a86...", "bytes": 1024},
             {"path": "kit/badge.css",        "role": "style",  "sha256": "e36fc8a4...", "bytes": 264},
             {"path": "kit/samples/kit.json", "role": "sample", "sha256": "754630b8...", "bytes": 230} ],
  "hash": "04fb713a8c9d" }
```

`kind` is `component`, `theme`, `template` or `guide`. The **id prefix** (`kit`, `layout`, `pattern`, `viz`, `theme`, `runtime`, `template`, `guide`) is a
separate classification. `kit list` and `suggest` report the id prefix in their `kind` output field, and their `--kind` filter matches it (`kit list --kind`
also accepts a `kind` value). File roles: `script`, `style`, `sample`, `preview` (a file under `kit/previews/`: the entry's own preview script for the catalog page, which `take` leaves out), `data`, `template`, `doc`. The entry `hash` is the first 12 hex of the SHA-256
of the sorted `path=sha256` lines. A theme also carries `fonts`, and some entries `extends`.

## The header

The index is **built from the headers**; nothing else writes it. Every entry describes itself in one comment at the top of its main file, after the
opening part marker: a `/** ... */` block in `.js` and `.css`, a `<!-- ... -->` block in `.txt` templates and `.md` guides. The first line is the
name, the next line or paragraph the `about` text, further paragraphs are notes, then the tags. The header of `kit/badge.js` in `catalog-a`:

```
/* part:page.script.kit.badge */
/**
 * Status badge
 * Kit.badge.render(el, {label, tone}) draws a small label coloured by a meaning token; an empty label draws nothing.
 *
 * @id        kit.badge
 * @kind      component
 * @group     Board kit
 * @status    new
 * @version   0.1.0
 * @updated   2026-11-20
 * @summary   A small label coloured by a meaning token.
 * @tags      badge, status, label
 * @requires  none
 * @files     kit/badge.css, kit/samples/kit.json
 * @provides  Kit.badge.render
 * @config    Kit.badge.render(el, opts) | label, tone (ok warn danger)
 * @tokens    --ok --warn --danger --f-ui
 * @globals   none
 * @db        none
 * @preview   {"render": "kit.badge", "samples": ["kit/samples/kit.json#badge"]}
 * @samples   badge
 */
```

| Tag | Required | Value |
|---|---|---|
| `@id` `@kind` `@group` `@status` `@version` `@updated` `@summary` `@tags` `@requires` `@files` `@globals` `@db` | always | `@status` is `new` or `stable`; `@version` is `major.minor.patch`; `@summary` at most 260 characters; `@requires` and `@files` are `none` or comma lists |
| `@provides` | in a `.js` main file | `none` or dotted JS names (`Kit.badge.render`) |
| `@tokens` | when the entry has a style file | custom properties; a trailing `?` marks an optional one (`--seam?`) |
| `@config` | optional, repeats | `signature \| what it takes` |
| `@preview` | optional | the renderer and sample references the catalog page previews the entry with |
| `@samples` | optional | the sample-bundle keys this entry owns |
| `@fonts` | optional | a theme's font stylesheet URL |
| `@extends` | optional | the entry this one extends |
| `@related` | optional | ids of related entries |
| `@optional` | optional | ids of entries this one can work with but does not require; `take` does not pull them in |
| `@source` | optional, repeats | where the entry came from |
| `@changed` | optional, at most once | the most recent change |

No other tag is allowed. The **main file** is the template or guide file, otherwise the first script, otherwise the first style.

## The consistency checks

The catalog tool is `scripts/adp_catalog.py`, beside `adp.py`, standard library only:

```sh
CAT="python3 -I adp_catalog.py"
$CAT                 # every catalog check: sizes, hashes, orphans, headers, index freshness, runtime copy
$CAT build           # write catalog.json from the headers (the check fails while it is out of date)
$CAT headers [FILES] # validate headers only; --report counts conformance per kind and per rule, exits 0
$CAT drift           # read-only report of where an entry's header disagrees with catalog.json
$CAT inventory       # list what the catalog holds
```

What it fails on:

- an entry file whose recorded `sha256` or `bytes` differ from the file; a file on disk that no entry lists (an orphan); an entry listing a missing file;
- a main file without a valid header, an unknown tag, a missing required tag, an `@id` that differs from the id of the entry that lists the file;
- an index that does not match what `build` would write from the headers;
- more than 256 entries (their main files must fit one Artifact read);
- `adp.js` in the catalog differing from the runtime's copy byte for byte;
- samples: a `#key` the bundle lacks, a bundle not in the entry's own `@files`, an entry listing a bundle but naming no key of it, a bundle key that no entry
  names or owns.

`adp_catalog.py` does not check the theme rules ([themes](../adp-themes/SKILL.md): the same token names, JSON and CSS agreeing, fonts);
check them by hand when a theme is added or changed. Run `adp_catalog.py headers` on every changed main file and the full check before any
catalog change is proposed.

## Using the catalog

```sh
ADP="python3 -I adp.py"
$ADP catalog CATALOG_URL      # save the url; print the Artifact read call for catalog.json, then read calls (up to 256 paths each) for missing or changed files
$ADP catalog                  # make those reads, then run again until it prints complete: true
$ADP suggest - --for "progress bar" --n 3
$ADP kit list - --kind viz --tag meter
$ADP take - viz.meter --url CATALOG_URL
```

**My Own Kit** is the user's local copy of their catalog, in `~/.adp/catalog/` (`$ADP_HOME/catalog/`; a copy an earlier run fetched into
`~/.adp/catalogs/<artifact id>/` is used until `catalog/` has an index of its own). `catalog` prints the reads that copy into it only the files that are
missing or changed, and `kit` and `suggest` read from it. `take` returns a `files` map `{path: {artifact: <catalog url>, path}}` for the publish call, the entries taken
in dependency order, and a `sha256` map. A catalog **is not edited by publishing over it**: a published catalog changes by proposal
([delta and inbox](../adp-delta/SKILL.md)). A local `catalog.json` is a build, not the live catalog; `take` warns when given one, and you must not
publish from it. Never download the whole catalog to publish a copy of it: clone the catalog artifact instead.

## A catalog tree, `adp_catalog.py build` and the check

A catalog is a folder with a `kit/` in it. A minimal complete example: a component with three samples, a visualization that requires it, a theme (tokens
and its JSON) and a guide. Its tree:

```
catalog-a/
  kit/badge.js              kit.badge     main file (header), role script
  kit/badge.css                           role style
  kit/viz/meter.js          viz.meter     main file, @requires kit.badge
  kit/viz/meter.css
  kit/themes/paper.css      theme.paper   main file (a theme's main file is its stylesheet), @fonts
  kit/themes/paper.json                   role data
  kit/guides/reading.md     guide.reading main file, header in <!-- -->
  kit/samples/kit.json      bundle: key "badge" (owned by kit.badge) holds three samples: typical, warning, empty
  kit/samples/viz.json      bundle: key "meter" (owned by viz.meter) holds three: half, full, zero
  catalog.json              written by build, never by hand
```

| Command | Does | Prints | Exit |
|---|---|---|---|
| `adp_catalog.py build CATALOG_DIR` | reads every header under `kit/`, writes `catalog.json` (`kit-catalog/2`: `schema`, `url`, `ver`, `built`, `entries`); each entry's `files` are its main file then its `@files`, each `{path, role, sha256, bytes}`, and `hash` the first 12 hex of the SHA-256 of the sorted `path=sha256` lines | `wrote <path>: N entries, M files` (or `unchanged ...`) | 0; 1 on a problem (below) |
| `adp_catalog.py CATALOG_DIR` | the check: the index equals what build would write, every file's size and sha256 match, no orphans, every header valid | `OK: N entries, M entry files, F files in tree, 0 orphans, all sizes, sha256 and hashes match, H valid headers` on stdout; or `FAIL: N problem(s)` on stdout followed by one line per problem, indented two spaces, in the order below | 0; 1 on any problem |

The check's problem lines, in this order:

1. For each entry, for each of its files in index order: `ID: missing file PATH`, `ID: size PATH: file N != bytes N`,
   `ID: sha256 PATH: file HEX != entry HEX`; then `ID: hash H != computed H` (the hash recomputed from the sha256 values the entry records), or
   `ID: entry has no hash`.
2. `orphan: PATH is not referenced by any entry or page file`, for each such file in sorted path order.
3. `N entries: their main files do not fit one Artifact read (256 paths at most)`; then, for each entry with no file to carry a header,
   `ID: no script, style, template or doc file to carry its header`.
4. `header PATH: [RULE] MESSAGE` for each broken header rule.
5. `tree: ...` for each problem `build` would report from the tree (below); when there is none, `samples: ...` for each sample problem.
6. `catalog.json: ...` for each place the index on disk differs from the built one: a top-level field other than `built` and `entries` as
   `FIELD: on disk V, built V`; `ID: a header in the tree, no entry in catalog.json` and the reverse
   `ID: an entry in catalog.json without a header in the tree`; then per entry, its fields in sorted order: for `files`,
   `ID.files: PATH is built, not on disk`, `ID.files: PATH is on disk, not built`, `ID.files[PATH]: K, K differ` (the differing keys,
   sorted) and `ID.files: in a different order`; for any other field, `ID.FIELD: on disk, not part of the built index`,
   `ID.FIELD: missing on disk; built V` or `ID.FIELD: on disk V, built V`. When nothing else differs but the entries' order,
   `entries: in a different order`. A missing or unreadable index is the one line `catalog.json: missing or not JSON`. Values are printed as
   JSON with sorted keys, cut to 87 characters plus `...` when longer than 90
   (`catalog.json: kit.badge.hash: on disk "04fb713a8c9d", built "e95bca96c3bb"`).

`build` writes nothing and exits 1 when it finds a problem. It prints `N problem(s); catalog.json is not written:` on stderr, followed by one line
per problem, indented two spaces. It looks for tree problems first:

- `ID: @requires names no entry: ID, ID`;
- `PATH: no entry names it (add it to @files in the header of its entry)`, for a kit file no entry lists;
- `ID: @files names P, which is not in the tree` (and the other `@files` misuses: outside the folder, the main file itself, named twice,
  another entry's main file);
- `PATH: its header has @id I, which is the @id of PATH`.

Only when there is none does it report header problems as `ID: PATH: [RULE] MESSAGE` (`kit.badge: kit/badge.js: [missing-tag] @summary is
required`), then sample problems as `BUNDLE: the key K is named by no entry's @preview` and `BUNDLE: the key K is owned by no entry's @samples`.

Its fixtures and vectors are in [vectors.md](vectors.md).

## The index and the check, as code

The code blocks with a header are the fragments of `adp_catalog.py` this skill owns (the header rules are in
[kit-authoring](../adp-kit-authoring/SKILL.md#the-header-as-code)).

An entry's files are its main file, then its `@files`. Roles come from the extension (`kit/samples/` files are samples), and the entry `hash` is over the
sorted `path=sha256` lines. `old_index` is the `catalog.json` on disk, `{}` when it is missing or not JSON:

```python
# ---
# id: catalog.index
# tool: adp_catalog.py
# section: catalog
# order: 300
# needs: [authoring.check]
# tests: [catalog-build, catalog-build-then-check, catalog-preview-role-is-left-out-by-take]
# sha: 81aa07a33118
# ---
import datetime

SCHEMA = 'kit-catalog/2'
ROLES = (('.html.txt', 'template'), ('.js', 'script'), ('.css', 'style'), ('.md', 'doc'), ('.json', 'data'), ('.txt', 'template'))
CODE = ('.js', '.css', '.js.txt', '.css.txt')
PROSE = ('.md', '.txt')
SKIP_TOP = {'catalog.json', 'index.html'}            # top-level files that are never an entry's main file
READ_MAX = 256                                       # paths in one Artifact read: the main files of all entries are fetched in one call
HERE = Path(__file__).resolve().parent.parent        # the folder that holds scripts/; its catalog/ is the default catalog


def opt(a, name, default=None):
    return a[a.index(name) + 1] if name in a else default


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(root, path):
    try: return Path(root, path).read_text(encoding='utf-8', errors='replace')
    except OSError: return ''          # a file that cannot be read has no header: it is listed as a file no entry names


def role(path):
    for folder, r in (('kit/samples/', 'sample'), ('kit/previews/', 'preview')):       # a preview is an entry's own preview on the catalog page: take leaves it out
        if path.startswith(folder): return r
    return next((r for x, r in ROLES if path.lower().endswith(x)), 'data')


def entry_hash(files):
    return hashlib.sha256('\n'.join(sorted(f"{f['path']}={f['sha256']}" for f in files)).encode()).hexdigest()[:12]


def old_index(root):
    try: index = json.loads(Path(root, 'catalog.json').read_text(encoding='utf-8'))
    except (OSError, ValueError): return {}
    return index if isinstance(index, dict) else {}


def inside(path):
    """A @files path as the index writes it; None when it is not a path inside the catalog folder."""
    p = path.replace('\\', '/')
    while p.startswith('./'): p = p[2:]
    parts = p.split('/')
    return None if p.startswith('/') or ':' in parts[0] or any(x in ('', '.', '..') for x in parts) else p
```

`build_index` reads every header under `kit/` (a folder's files first, then its folders, each in name order; then the top of the folder) and returns the index with what is wrong in the tree. `url` and `ver` are kept
from the `catalog.json` on disk, and so is `built` when nothing else changed. What is wrong inside a header is `validate`'s, reported by `build` only
once the tree is sound:

```python
# ---
# id: catalog.build-index
# tool: adp_catalog.py
# section: catalog
# order: 310
# needs: [catalog.index]
# tests: [catalog-build, catalog-refuses-an-orphan, catalog-orphans-in-tree-order, catalog-refuses-a-missing-require, catalog-refuses-bad-files, catalog-lists-an-unreadable-file]
# sha: 730981e6b0cf
# ---
def build_index(root):
    """-> (the kit-catalog/2 index the headers build, [what is wrong with the tree])"""
    root, issues, heads, mains, built = os.path.abspath(root), [], {}, {}, []
    old = old_index(root)
    kit = []
    for d, dirs, names in os.walk(Path(root, 'kit')):      # a folder's files, then its folders, each in name order
        dirs[:] = sorted(x for x in dirs if not x.startswith('.') and x != '__pycache__')
        kit += [Path(d, n).relative_to(root).as_posix() for n in sorted(names) if not n.startswith('.')]
    top = sorted(n for n in os.listdir(root) if Path(root, n).is_file() and not n.startswith('.') and n not in SKIP_TOP)
    for p in kit + top:
        if not p.startswith('kit/samples/') and p.lower().endswith(CODE + PROSE) and (h := parse_header(read(root, p), p)).get('id'): heads[p] = h
    for p in sorted(heads):
        if heads[p]['id'] in mains: issues.append(f"{p}: its header has @id {heads[p]['id']}, which is the @id of {mains[heads[p]['id']]}; one file carries the header of an entry")
        else: mains[heads[p]['id']] = p
    named = set(heads)
    for i, cp in sorted(mains.items(), key=lambda x: x[1]):
        h, paths = heads[cp], [cp]
        for given in h.get('files', []):
            p = inside(given)
            if p is None: issues.append(f'{i}: @files names {given}, which is not a path inside the catalog folder')
            elif p == cp: issues.append(f'{i}: @files names {p}, the main file itself; name the other files only')
            elif p in paths: issues.append(f'{i}: @files names {p} twice')
            elif p in heads: issues.append(f"{i}: @files names {p}, which carries the header of {heads[p]['id']}; name that entry in @requires")
            elif not Path(root, p).is_file(): issues.append(f'{i}: @files names {p}, which is not in the tree')
            else: paths.append(p)
        named.update(paths)
        files = [{'path': p, 'role': role(p), 'sha256': sha256(Path(root, p)), 'bytes': Path(root, p).stat().st_size} for p in paths]
        e = {k: h.get(k, [] if k in LISTS else '') for k in ('kind', 'group', 'name', 'summary', 'tags', 'status', 'version', 'requires', 'globals', 'provides')}
        built.append({'id': i, **e, **{k: h[k] for k in ('fonts', 'extends') if h.get(k)}, 'main': cp, 'files': files, 'hash': entry_hash(files)})
    issues += [f"{e['id']}: @requires names no entry: {', '.join(bad)}" for e in built if (bad := [r for r in e['requires'] if r not in mains])]
    issues += [f'{p}: no entry names it (add it to @files in the header of its entry)' for p in kit if p not in named]
    same = old.get('schema') == SCHEMA and old.get('entries') == built and old.get('built')
    return {'schema': SCHEMA, 'url': old.get('url') or '', 'ver': old.get('ver') or '', 'built': old['built'] if same
            else datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'entries': built}, issues
```

The sample rules: a `@preview` reference `bundle#key` must name a key of a JSON-object bundle among the sample files of the entry's own `@files`; an entry
that lists a bundle names a key of it; every key of a bundle is named by some `@preview` and owned by some `@samples`. Each header is also validated
against the index just built:

```python
# ---
# id: catalog.samples
# tool: adp_catalog.py
# section: catalog
# order: 320
# needs: [catalog.build-index]
# tests: [catalog-refuses-a-bad-header, catalog-refuses-an-unowned-sample, catalog-refuses-bad-samples]
# sha: 1abfebd878b8
# ---
def header_issues(root, index):
    """[line] for every rule broken in the header of each entry's main file."""
    ids = {e['id'] for e in index['entries']}
    return [f"{e['id']}: {e['main']}: [{r}] {m}" for e in index['entries']
            for r, m in validate(e['main'], comment_of(read(root, e['main']), e['main']), e, ids)]


def sample_issues(root, index):
    """[line] for the sample bundles of the index."""
    root, out, refs, owned, cache, ents = os.path.abspath(root), [], [], {}, {}, index['entries']
    listed = {f['path'] for e in ents for f in e['files'] if f['role'] == 'sample'}
    own = {e['id']: {f['path'] for f in e['files'] if f['role'] == 'sample'} for e in ents}
    for e in ents:
        h = parse_header(read(root, e['main']), e['main'])
        owned[e['id']], pv = h.get('samples') or [], h.get('preview')
        for s in (pv.get('samples') if isinstance(pv, dict) else None) or []:
            p, k = split_ref(s) if isinstance(s, str) else ('', None)
            if p and k is not None: refs.append((e['id'], p, k))

    def bundle(p):
        if p not in cache:
            try: j = json.loads(Path(root, p).read_text(encoding='utf-8'))
            except (OSError, ValueError): j = None
            cache[p] = j if isinstance(j, dict) else None
        return cache[p]
    named = {}
    for i, p, k in refs:
        named.setdefault(p, set()).add(k)
        if p not in own[i]: out.append(f'{i}: @preview names {p}#{k}, but {p} is not a sample file in its @files')
        elif bundle(p) is None: out.append(f'{i}: @preview names {p}#{k}, but {p} is not a JSON object')
        elif k not in bundle(p): out.append(f'{i}: @preview names {p}#{k}, but {p} has no key {k}')
    for e in ents:
        mine = {p for i, p, _ in refs if i == e['id']}
        out += [f"{e['id']}: @files lists the sample bundle {f['path']}, but its @preview names no key of it"
                for f in e['files'] if f['role'] == 'sample' and f['path'] in named and f['path'] not in mine]
    live = [p for p in sorted(named) if bundle(p) is not None and p in listed]
    for p in live: out += [f"{p}: the key {k} is named by no entry's @preview" for k in sorted(set(bundle(p)) - named[p])]
    owners = {}
    for i, keys in owned.items():
        for k in keys:
            if mine := [p for p in sorted(own[i]) if p in named and bundle(p) is not None and k in bundle(p)]: owners.setdefault(mine[0], set()).add(k)
            else: out.append(f'{i}: @samples names {k}, which is a key of no sample bundle in its @files')
    for p in live: out += [f"{p}: the key {k} is owned by no entry's @samples" for k in sorted(set(bundle(p)) - owners.get(p, set()))]
    return out
```

`differences` is the check's last section: one line per place the index on disk differs from the one `build` would write (the `built` stamp
is not compared):

```python
# ---
# id: catalog.differences
# tool: adp_catalog.py
# section: catalog
# order: 330
# needs: [catalog.index]
# tests: [catalog-check-catches-a-file-edited-after-build, catalog-check-catches-a-stale-index]
# sha: 72dd960dc12b
# ---
def cut(v, n=90):
    s = json.dumps(v, ensure_ascii=False, sort_keys=True)
    return s if len(s) <= n else s[:n - 3] + '...'


def differences(old, new):
    """One line per place the index on disk (old) differs from the built one (new)."""
    if not old: return ['catalog.json: missing or not JSON']
    out = [f'{k}: on disk {cut(old.get(k))}, built {cut(new.get(k))}' for k in sorted((set(old) | set(new)) - {'built', 'entries'}) if old.get(k) != new.get(k)]
    oe, ne = ({e.get('id'): e for e in x.get('entries', []) if isinstance(e, dict)} for x in (old, new))
    out += [f'{i}: a header in the tree, no entry in catalog.json' for i in ne if i not in oe]
    out += [f'{i}: an entry in catalog.json without a header in the tree' for i in oe if i not in ne]
    for i, a in oe.items():
        if (b := ne.get(i)) is None: continue
        for k in sorted(set(a) | set(b)):
            if k == 'files' and isinstance(a[k], list):
                fa, fb = ({f.get('path'): f for f in x[k] if isinstance(f, dict)} for x in (a, b))
                out += [f'{i}.files: {p} is built, not on disk' for p in fb if p not in fa]
                for p in fa:
                    if p not in fb: out.append(f'{i}.files: {p} is on disk, not built')
                    elif fa[p] != fb[p]: out.append(f"{i}.files[{p}]: {', '.join(x for x in sorted(set(fa[p]) | set(fb[p])) if fa[p].get(x) != fb[p].get(x))} differ")
                if not set(fa) ^ set(fb) and list(fa) != list(fb): out.append(f'{i}.files: in a different order')
            elif k not in b: out.append(f'{i}.{k}: on disk, not part of the built index')
            elif k not in a: out.append(f'{i}.{k}: missing on disk; built {cut(b[k])}')
            elif a[k] != b[k]: out.append(f'{i}.{k}: on disk {cut(a[k])}, built {cut(b[k])}')
    return out or (['entries: in a different order'] if list(oe) != list(ne) else [])
```

The check, with the problem lines in the order the table above lists them. Only the catalog folder named `catalog` next to an `assets/adp.js` (the plugin's own
catalog) is also compared with that runtime:

```python
# ---
# id: catalog.check
# tool: adp_catalog.py
# section: catalog
# order: 400
# needs: [catalog.build-index, catalog.samples, catalog.differences]
# tests: [catalog-build-then-check, catalog-check-passes-a-built-tree, catalog-check-catches-a-file-edited-after-build, catalog-check-catches-a-stale-index]
# sha: 13749bc641a4
# ---
PAGE_FILES = {'index.html', 'catalog.json', 'content.js', 'adp.js', 'styles/catalog.css'}      # the catalog page's own files, never entries


def check_catalog(argv):
    """The catalog folder (default: ../catalog) against its catalog.json: 0 and one OK line, or 1 and each failure."""
    root = Path(argv[0]) if argv else HERE / 'catalog'
    cat = old_index(root)
    ents, errors, referenced, nfiles = cat.get('entries', []), [], set(), 0
    for e in ents:
        lines = []
        for f in e.get('files', []):
            nfiles += 1
            path, p = f['path'], root / f['path']
            referenced.add(path)
            if not p.is_file(): errors.append(f"{e.get('id', '?')}: missing file {path}"); continue
            if p.stat().st_size != f['bytes']: errors.append(f"{e.get('id', '?')}: size {path}: file {p.stat().st_size} != bytes {f['bytes']}")
            if sha256(p) != f['sha256']: errors.append(f"{e.get('id', '?')}: sha256 {path}: file {sha256(p)} != entry {f['sha256']}")
            lines.append(f"{path}={f['sha256']}")
        want = hashlib.sha256('\n'.join(sorted(lines)).encode()).hexdigest()[:12]
        if 'hash' not in e: errors.append(f"{e.get('id', '?')}: entry has no hash")
        elif e['hash'] != want: errors.append(f"{e.get('id', '?')}: hash {e['hash']} != computed {want}")
    tree = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    errors += [f'orphan: {p} is not referenced by any entry or page file' for p in sorted(tree) if p not in referenced and p not in PAGE_FILES and not p.startswith('parts/')]
    if len(ents) > READ_MAX: errors.append(f'{len(ents)} entries: their main files do not fit one Artifact read ({READ_MAX} paths at most)')
    errors += [f"{e.get('id', '?')}: no script, style, template or doc file to carry its header" for e in ents if not main_file(e)]
    results, _ = check_headers(root) if ents else ([], {})
    errors += [f'header {rel}: [{r}] {m}' for rel, _, issues in results for r, m in issues if r != 'missing-file']      # a missing file is reported above
    index, issues = build_index(root)
    errors += [f'tree: {i}' for i in issues] + ([] if issues else [f'samples: {i}' for i in sample_issues(root, index)]) + [f'catalog.json: {d}' for d in differences(cat, index)]
    runtime = root.parent / 'assets' / 'adp.js'
    if root.name == 'catalog' and runtime.is_file() and (root / 'adp.js').is_file() and runtime.read_bytes() != (root / 'adp.js').read_bytes():
        errors.append('runtime: the catalog adp.js and assets/adp.js differ; there is one runtime')
    if errors:
        print(f'FAIL: {len(errors)} problem(s)', *errors, sep='\n  ')
        return 1
    valid = sum(s == 'header' and not i for _, s, i in results)
    print(f"OK: {len(ents)} entries, {nfiles} entry files, {len(tree)} files in tree, 0 orphans, all sizes, sha256 and hashes match, {valid} valid headers")
    return 0
```

`build` writes nothing and exits 1 when the tree or a header has a problem; `headers [FILES...] [--report] [--root DIR]` validates the main files given
(other files are skipped), or every main file. `--report` counts, per id prefix, the headers that are ok, invalid or legacy, and per failed rule, and exits 0:

```python
# ---
# id: catalog.commands
# tool: adp_catalog.py
# section: catalog
# order: 410
# needs: [catalog.check]
# tests: [catalog-build, catalog-build-then-check, catalog-refuses-an-orphan, catalog-headers-command]
# sha: 2258cde6578a
# ---
import collections


def build(argv):
    """Write CATALOG_DIR/catalog.json entirely from the headers. A problem in a header or in the tree: list each one, write nothing, exit 1."""
    root = argv[0] if argv else str(HERE / 'catalog')
    if len(argv) > 1 or not os.path.isdir(os.path.join(root, 'kit')): sys.exit('usage: adp_catalog.py build [CATALOG_DIR]   (a folder with a kit/ in it)')
    index, issues = build_index(root)
    issues = issues or header_issues(os.path.abspath(root), index) + sample_issues(root, index)
    if issues:
        print(f'{len(issues)} problem(s); catalog.json is not written:', *issues, sep='\n  ', file=sys.stderr)
        return 1
    path, text = Path(root, 'catalog.json'), json.dumps(index, ensure_ascii=False, indent=1) + '\n'
    same = path.is_file() and path.read_text(encoding='utf-8') == text
    if not same: path.write_text(text, encoding='utf-8')
    print(f"{'unchanged' if same else 'wrote'} {path}: {len(index['entries'])} entries, {sum(len(e['files']) for e in index['entries'])} files")
    return 0


def headers(argv):
    """The headers of the main files given, or of every main file; --report counts per kind and rule instead."""
    root, files, report, a = str(HERE / 'catalog'), [], False, list(argv)
    while a:
        if (x := a.pop(0)) == '--root' and a: root = a.pop(0)
        elif x == '--report': report = True
        elif x.startswith('--'): sys.exit(f'unknown option {x}')
        else: files.append(x)
    results, by_path = check_headers(root, files or None)
    if report:
        kinds, rules = collections.defaultdict(collections.Counter), collections.Counter()
        for rel, state, issues in (r for r in results if r[1] != 'skipped'):
            kinds[by_path[rel]['id'].split('.')[0]]['legacy' if state == 'legacy' else 'invalid' if issues else 'header'] += 1
            rules.update(r for r, _ in issues)
        for k in sorted(kinds): print(f'{k:9s} header ok {kinds[k]["header"]:3d}   invalid {kinds[k]["invalid"]:3d}   legacy {kinds[k]["legacy"]:3d}')
        for r, n in rules.most_common(): print(f'  rule {r}: {n}')
        return 0
    bad = [(p, i) for p, _, i in results if i]
    for p, issues in bad: print(*(f'{p}: [{r}] {m}' for r, m in issues), sep='\n')
    if bad: print(f'{len(bad)} file(s) with problems', file=sys.stderr); return 1
    print(f"ok: {sum(s == 'header' for _, s, _ in results)} header(s) valid, {sum(s == 'skipped' for _, s, _ in results)} skipped")
    return 0
```

`drift [--catalog-dir D] [--field F,..] [--strict]` is a read-only report of where the header of each entry's main file disagrees with the entry in
`catalog.json`: one line per disagreement, a table of equal, differing and header-less entries per field, and the entries with no header. `-h` prints
the tolerances of each field; an unknown field or option is an argparse error (exit 2); a folder with no readable `catalog.json` prints the `FAIL` line of `check` and exits 1. The `about`, `tokens` and `db` fields are read from an
index that carries them (`about`, `needs.tokens`, `needs.db.note`); an index `build` wrote has none, so those fields differ for every entry that has a
header value, and the header is the only record:

```python
# ---
# id: catalog.drift
# tool: adp_catalog.py
# section: catalog
# order: 500
# needs: [catalog.commands]
# tests: [catalog-drift]
# sha: 08f0c3c826cc
# ---
import argparse

DRIFT_FIELDS = ['version', 'about', 'provides', 'tokens', 'db']


def squash(s):
    return re.sub(r'\s+', ' ', s or '').strip()


def short(v, n=80):
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[:n - 3] + '...'


def drift_compare(field, h, e):
    """(equal, header value, catalog value); h is the header of the main file, e the entry."""
    need = e.get('needs') or {}
    if field == 'version': return h['version'] == e.get('version'), h['version'], e.get('version')
    if field == 'provides': return h['provides'] == set(e.get('provides') or []), sorted(h['provides']), sorted(e.get('provides') or [])
    if field == 'tokens':
        c = {t for t in need.get('tokens') or [] if not t.endswith('-')}
        return h['tokens'] == c, sorted(h['tokens']), sorted(c)
    if field == 'about':
        a, b = ({w for w in re.findall(r'[a-z]{5,}', (x or '').lower())} for x in (e.get('about'), h['what']))
        share = len(a & b) / len(a) if a else 1.0
        return share >= 0.5, h['what'], '%s (share %.2f)' % (e.get('about', ''), share)
    note, d = squash((need.get('db') or {}).get('note')), h['db']
    return (d is None or d.lower().startswith('none')) if not note else bool(d) and note[:40].lower() in d.lower(), d, note


DRIFT_DOC = """Read-only report: where the header of each entry's main file disagrees with catalog.json.

adp_catalog.py drift [--catalog-dir CATALOG_DIR] [--field version,about,provides,tokens,db] [--strict]

One line per disagreement:  <entry id> <field>: header=<...> catalog=<...>   (values cut to 80 chars)
Then a summary table (equal / differ / no header per field) and the entries whose main file has no header.

Tolerances:
  version   exact string match (@version).
  provides  sets of names (@provides).
  about     share of the catalog about's words (5+ letters) found in the header's about paragraph >= 0.5.
  tokens    sets of css custom properties (@tokens, a trailing ? dropped) after leaving out wildcards (names ending in "-" or with a
            <placeholder>), which are listed separately as wildcards.
  db        the catalog needs.db.note, if any, must appear (first 40 chars, case-insensitive) in the header's @db text;
            no note matches an absent or "none" header text.
Exit code 0, except 1 with --strict when any version or provides disagreement exists, and 1 with the FAIL line `check` prints when the folder has no catalog.json."""


def drift(argv):
    ap = argparse.ArgumentParser(prog='adp_catalog.py drift', description=DRIFT_DOC, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--catalog-dir', default=str(HERE / 'catalog'))
    ap.add_argument('--field', default=','.join(DRIFT_FIELDS), help='comma list of: ' + ','.join(DRIFT_FIELDS))
    ap.add_argument('--strict', action='store_true', help='exit 1 if any version or provides disagreement')
    a = ap.parse_args(argv)
    root, fields = Path(a.catalog_dir), [f.strip() for f in a.field.split(',') if f.strip()]
    if (bad := [f for f in fields if f not in DRIFT_FIELDS]) or not fields: ap.error('unknown field: ' + ','.join(bad or ['(none)']))
    if not (index := old_index(root)): print('FAIL: 1 problem(s)', 'catalog.json: missing or not JSON', sep='\n  '); return 1
    ents = index.get('entries', [])
    lines, counts, nohdr, wild = [], {f: collections.Counter() for f in fields}, [], []
    for e in ents:
        main = main_file(e)
        c = comment_of(read(root, main), main) if main and Path(root, main).is_file() else None
        if c is None or '@id' not in c:
            nohdr.append(e['id'])
            for f in fields: counts[f]['no header'] += 1
            continue
        t = dict(parse(c)[2])
        toks = [x.rstrip('?') for x in split(t.get('tokens', ''), spaces=True) if x != 'none']
        star = [x for x in toks if x.endswith('-') or '<' in x]
        h = {'version': t.get('version'), 'provides': set(split(t.get('provides', ''))) - {'none'}, 'what': squash(parse(c)[1]),
             'tokens': set(toks) - set(star), 'db': squash(t.get('db')) or None}
        if star: wild.append((e['id'], sorted(set(star))))
        for f in fields:
            ok, hv, cv = drift_compare(f, h, e)
            counts[f]['equal' if ok else 'differ'] += 1
            if not ok:
                lines.append((f, f'{e["id"]} {f}: header={short(hv)} catalog={short(cv)}'))
    if lines: print(*(t for _, t in lines), sep='\n')
    print('\n%d entries; %d without a header in their main file' % (len(ents), len(nohdr)))
    print('%-10s %6s %6s %10s' % ('field', 'equal', 'differ', 'no header'))
    for f in fields: print('%-10s %6d %6d %10d' % (f, counts[f]['equal'], counts[f]['differ'], counts[f]['no header']))
    if nohdr: print('entries without a header: ' + ', '.join(nohdr))
    if wild: print('wildcard tokens (not compared): ' + '; '.join('%s %s' % (i, ' '.join(w)) for i, w in wild))
    return 1 if a.strict and any(f in ('version', 'provides') for f, _ in lines) else 0
```

`inventory [--root DIR]` prints one JSON (`adp-inventory/1`, the same on every run) of what every theme, catalog entry and page declares, reads and
hard-codes in its styles. `DIR` is the skill folder (default: the one above `scripts/`); its `catalog/` and `templates/` are read, and paths in the
output are relative to the folder that holds `DIR`. Tokens are CSS custom properties. Seven fragments build it: the CSS text readers, the script
lexer, the look classes, what one entry or page reads (`Unit`), a theme, and the inventory itself.

What is read. A `.css` file or `<style>`: every declaration, comments dropped; a `var()` inside a CSS string is not read. A `.js` file: every string and
template literal, joined across `+` and `${}` with `*` for the part computed at run time; comments and regex literals are dropped; a string with a tag
in it is markup (its reads are those of the whole string), any other is CSS. A `.html` file: `<style>`, `<script>` and attribute values; comments and
the text between tags are not read. A `.txt` file is read as the type before `.txt`. Values are printed with their spacing made uniform.

```python
# ---
# id: catalog.css-text
# tool: adp_catalog.py
# section: catalog
# order: 600
# needs: [catalog.drift]
# tests: [catalog-inventory]
# sha: 16b0108f61c9
# ---
import bisect

W = '\x00'                                              # the part of a string computed at run time; printed as *
NAME = re.compile(r'--[A-Za-z0-9_-]*[A-Za-z0-9_]')     # a name does not end in -: '--f-' is the start of one
IN_TEXT = re.compile(r'(?<![\w-])--[A-Za-z]([A-Za-z0-9_-]*[A-Za-z0-9_])?(?![\w<-])')       # a name in prose or data
NAMEW = re.compile(r'--[\w%s-]+' % W)                   # a name that may hold a run-time part
VAR = re.compile(r'(?<![\w-])var\(')
DECL = re.compile(r'\s*([-\w%s]+)\s*:(.*)' % W, re.S)
TAG = re.compile(r'<[A-Za-z][^<>]*>')
ATTR = re.compile(r'([\w:-]+)\s*=\s*("[^"]*"|\'[^\']*\')')


def norm(v):
    """A value as it is printed and counted: one space between parts and after a comma, none inside brackets, * for a run-time part."""
    return re.sub(r'\(\s+|\s+(?=\))', lambda m: m.group(0).strip(), re.sub(r'\s*,\s*', ', ', ' '.join(v.replace(W, '*').split())))


def wipe(chars, a, b):
    for k in range(a, b):
        if chars[k] != '\n': chars[k] = ' '


def skip_string(t, i):
    """The index after the string that opens at t[i] (it ends at the line's end when it never closes)."""
    j, n = i + 1, len(t)
    while j < n and t[j] != t[i] and t[j] != '\n': j += 2 if t[j] == '\\' else 1
    return min(j + 1, n)


def css_clean(t):
    """t with its comments blanked: the same length and the same lines."""
    out, i, n = list(t), 0, len(t)
    while i < n:
        if t[i] in '"\'': i = skip_string(t, i)
        elif t.startswith('/*', i):
            j = t.find('*/', i + 2)
            j = n if j < 0 else j + 2
            wipe(out, i, j)
            i = j
        else: i += 1
    return ''.join(out)


def close(t, i):
    """The index of the ) that closes the ( just before t[i]; len(t) when nothing closes it."""
    d, n = 1, len(t)
    while i < n:
        if t[i] in '"\'':
            i = skip_string(t, i)
            continue
        d += (t[i] == '(') - (t[i] == ')')
        if not d: return i
        i += 1
    return n


def split_top(v, seps):
    """v cut at every character of seps that is outside brackets and strings."""
    out, d, a, i, n = [], 0, 0, 0, len(v)
    while i < n:
        c = v[i]
        if c in '"\'':
            i = skip_string(v, i)
            continue
        if c in '([': d += 1
        elif c in ')]': d -= 1
        elif d <= 0 and c in seps:
            out.append(v[a:i])
            a = i + 1
        i += 1
    return out + [v[a:]]


def var_reads(t, off=0, depth=0):
    """[(name, fallback or None, depth, position)] for every var() of t; depth is how many fallbacks it sits inside."""
    out, i = [], 0
    while m := VAR.search(t, i):
        j = close(t, m.end())
        inner = t[m.end():j]
        head = split_top(inner, ',')[0]
        fb = inner[len(head) + 1:] if len(head) < len(inner) else None
        out.append((head.strip(), fb if fb is None else norm(fb), depth, off + m.start()))
        if fb: out += var_reads(fb, off + m.end() + len(head) + 1, depth + 1)
        i = j + 1
    return out


def css_decls(t):
    """[(rules, property, value, position)] for every declaration of t, comments already blanked; rules is the ((prelude, position), …)
    of the rules it sits in, outermost first."""
    out, stack, a, i, d, n = [], [], 0, 0, 0, len(t)

    def decl(b):
        if m := DECL.fullmatch(t[a:b]):
            p = m.group(1)
            out.append((tuple(stack), p if p.startswith('--') else p.lower(), m.group(2).strip(), a + m.start(1)))
    while i < n:
        c = t[i]
        if c in '"\'':
            i = skip_string(t, i)
            continue
        if c == '(': d += 1
        elif c == ')': d = max(0, d - 1)
        elif d == 0 and c in '{;}':
            if c == '{': stack.append((' '.join(t[a:i].split()), i))
            else:
                decl(i)
                if c == '}' and stack: stack.pop()
            a = i + 1
        i += 1
    decl(n)
    return out
```

A script is cut into tokens first: strings, template literals (with their `${}` parts), words, punctuation and regex literals; comments are dropped. `units`
then joins the strings of an expression across `+` and `${}`, which is what a name or a declaration built at run time looks like:

```python
# ---
# id: catalog.js-lexer
# tool: adp_catalog.py
# section: catalog
# order: 610
# needs: [catalog.css-text]
# tests: [catalog-inventory]
# sha: fae20ddb1018
# ---
WORD = re.compile(r'[A-Za-z_$][\w$]*|\d[\w.]*')
BEFORE_REGEX = {'return', 'typeof', 'case', 'in', 'of', 'delete', 'void', 'throw', 'new', 'else', 'do', 'instanceof', 'yield', 'await'}
OPERAND_ENDS, ARG_ENDS = set('+,;?:=|&<>)]}'), set(',)')


def unesc(s):
    """A script string with each escape made harmless, at the same length."""
    return re.sub(r'\\(.)', lambda m: ' ' + (' ' if m.group(1) in 'nrt' else m.group(1)), s, flags=re.S)


def js_lex(t, i=0, inner=False):
    """(tokens, end). A token is [kind, value, position]: s a string (its text), t a template literal (its parts: an s token, or ('x',
    tokens) for a ${}), w a word, p one punctuation character, r a regex literal. Comments are dropped. inner: stop after the } of a ${}."""
    toks, n, d = [], len(t), 0
    while i < n:
        c = t[i]
        if c.isspace(): i += 1
        elif t.startswith('//', i):
            j = t.find('\n', i)
            i = n if j < 0 else j
        elif t.startswith('/*', i):
            j = t.find('*/', i + 2)
            i = n if j < 0 else j + 2
        elif c in '"\'':
            j = skip_string(t, i)
            toks.append(['s', unesc(t[i + 1:j - 1]), i + 1])
            i = j
        elif c == '`':
            parts, j, a = [], i + 1, i + 1
            while j < n and t[j] != '`':
                if t[j] == '\\': j += 2
                elif t.startswith('${', j):
                    parts.append(['s', unesc(t[a:j]), a])
                    sub, j = js_lex(t, j + 2, True)
                    parts.append(('x', sub))
                    a = j
                else: j += 1
            parts.append(['s', unesc(t[a:j]), a])
            toks.append(['t', parts, i])
            i = j + 1
        elif c == '/' and (not toks or toks[-1][0] == 'p' and toks[-1][1] not in ')]' or toks[-1][0] == 'w' and toks[-1][1] in BEFORE_REGEX):
            j, cls = i + 1, False
            while j < n and t[j] != '\n' and (cls or t[j] != '/'):
                if t[j] == '\\': j += 1
                elif t[j] in '[]': cls = t[j] == '['
                j += 1
            toks.append(['r', '', i])
            i = j + 1
        elif m := WORD.match(t, i):
            toks.append(['w', m.group(0), i])
            i = m.end()
        else:
            if inner and c == '}' and d == 0: return toks, i + 1
            d += (c == '{') - (c == '}')
            toks.append(['p', c, i])
            i += 1
    return toks, n


def operand(toks, i, ends=OPERAND_ENDS):
    """The index where the operand that starts at toks[i] ends: the first character of ends outside brackets."""
    d = 0
    while i < len(toks):
        k, v = toks[i][0], toks[i][1]
        if k == 'p':
            if v in '([{': d += 1
            elif d == 0 and v in ends: break
            elif v in ')]}': d -= 1
        i += 1
    return i


def str_parts(tok):
    """A string or template token as ([(text, position)], [the token lists of its ${} parts]); each ${} is (W, position)."""
    if tok[0] == 's': return [(tok[1], tok[2])], []
    return [(p[1], p[2]) if p[0] == 's' else (W, tok[2]) for p in tok[1]], [p[1] for p in tok[1] if p[0] == 'x']


def units(toks):
    """Every string of a script as [(text, position), …], joined across + and ${}; the strings inside a run-time part come after it,
    on their own."""
    i, n = 0, len(toks)
    while i < n:
        if toks[i][0] not in 'st':
            i += 1
            continue
        out, subs = str_parts(toks[i])
        i += 1
        while i < n and toks[i][:2] == ['p', '+']:
            e = operand(toks, i + 1)
            op = toks[i + 1:e]
            if not op: break
            if len(op) == 1 and op[0][0] in 'st':
                a, b = str_parts(op[0])
                out, subs = out + a, subs + b
            else:
                out.append((W, op[0][2]))
                subs.append(op)
            i = e
        yield out
        for s in subs: yield from units(s)
```

`look` is what a declaration hard-codes, by class, each counted as `literal` (no `var()` in it), `token` (the value is one `var()`, counted under its
name) or `mixed` (anything else):

| Class | Counts |
|---|---|
| `radius` | `border-radius` and the four corner longhands |
| `case`, `tracking` | `text-transform`, `letter-spacing` |
| `family` | `font-family`, and the part of `font` after the size (the whole value when `font` is one word, such as `inherit`) |
| `edge` | `border-width` and its longhands, and the width of a border shorthand (`border`, `border-top`, `border-inline-start`, …): the length, else a `var()` written before the style keyword, else `none` for a shorthand that is only `none` or `hidden`; a shorthand with no width counts nothing |
| `shadow`, `ring` | `box-shadow`; `outline`, the whole value (`outline-color` and `outline-offset` are not counted) |
| `colour` | literal only, in a property that takes a colour (a custom property, any `*color`, `background`, border and outline shorthands, shadows, filters, `fill`, `stroke`): each hex, each `rgb()`/`hsl()`/`hwb()`/`lab()`/`lch()`/`oklab()`/`oklch()`/`color()` with no `var()` inside, and each named or system colour; in markup also the `fill`, `stroke`, `stop-color`, `flood-color` and `color` attributes. Not counted: `transparent`, `currentColor`, `inherit`, a colour in a CSS string or `url()`, a mask's `#000` (see `colour_strings` for scripts) |

```python
# ---
# id: catalog.look
# tool: adp_catalog.py
# section: catalog
# order: 620
# needs: [catalog.js-lexer]
# tests: [catalog-inventory]
# sha: 573804c4b69e
# ---
CLASSES = ('radius', 'case', 'tracking', 'family', 'edge', 'shadow', 'ring', 'colour')
WHOLE = {'text-transform': 'case', 'letter-spacing': 'tracking', 'font-family': 'family', 'box-shadow': 'shadow', 'outline': 'ring'}
SIDE = r'border(-(top|right|bottom|left|inline|block)(-(start|end))?)?'
RADIUS = re.compile(r'border(-(top|bottom|start|end)-(left|right|start|end))?-radius')
EDGE, BORDER = re.compile(SIDE + '-width'), re.compile(SIDE)
STYLES = {'none', 'hidden', 'dotted', 'dashed', 'solid', 'double', 'groove', 'ridge', 'inset', 'outset'}
MATH = r'(calc|min|max|clamp)\(.*\)'
LENGTH = re.compile(r'[+-]?(\d+\.?\d*|\.\d+)[a-z%]*|thin|medium|thick|' + MATH)
SIZE = re.compile(r'(\d+\.?\d*|\.\d+)([a-z]+|%)|(xx?-)?(small|large)|xxx-large|medium|larger|smaller|' + MATH)
PAINT = {'fill', 'stroke', 'stop-color', 'flood-color', 'color'}
TAKES_COLOUR = re.compile(r'--.*|.*color|background(-image)?|' + SIDE + r'|border-image(-source)?|outline|(box|text)-shadow|fill|stroke|'
                          r'text-decoration|column-rule|(backdrop-)?filter')
FUNC = re.compile(r'(?<![\w-])(rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(', re.I)
HEX = re.compile(r'#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])')
COLOUR_WORD = re.compile(r'(?<![\w#.-])[A-Za-z]+(?![\w(-])')
NAMED = set('''aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood cadetblue
chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey darkkhaki
darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen darkslateblue darkslategray darkslategrey darkturquoise
darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod
gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral
lightcyan lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey
lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen
mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive
olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple
rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey snow
springgreen steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen
canvas canvastext linktext visitedtext activetext buttonface buttontext buttonborder field fieldtext highlight highlighttext selecteditem
selecteditemtext mark marktext graytext accentcolor accentcolortext'''.split())


def colours(prop, v):
    """The literal colours in one value of a property that takes a colour: lower case, no spaces."""
    if not TAKES_COLOUR.fullmatch(prop): return []
    v = re.sub(r'"[^"]*"|\'[^\']*\'|url\([^)]*\)', ' ', v)
    out = []
    for m in FUNC.finditer(v):
        s = v[m.start():close(v, m.end()) + 1]
        if 'var(' not in s and '*' not in s: out.append(s.replace(' ', '').lower())
    return out + [m.group(0).lower() for m in HEX.finditer(v)] + [w.lower() for w in COLOUR_WORD.findall(v) if w.lower() in NAMED]


def bucket(v):
    """(literal, the value), (token, its name) when the value is one var(), else (mixed, the value)."""
    if 'var(' not in v and '*' not in v: return 'literal', v
    if v.startswith('var(') and close(v, 4) == len(v) - 1 and NAME.fullmatch(var_reads(v)[0][0]): return 'token', var_reads(v)[0][0]
    return 'mixed', v


def edge_of(c):
    """The width a border shorthand sets, from its parts; None when it sets none."""
    if w := [x for x in c if LENGTH.fullmatch(x)]: return w[0]
    if c[0].startswith('var(') and (len(c) == 1 or any(x in STYLES for x in c[1:])): return c[0]
    return 'none' if len(c) == 1 and c[0] in ('none', 'hidden') else None


def family_of(c):
    """The family a font shorthand sets, from its parts: what follows the size."""
    for i, x in enumerate(c):
        if SIZE.fullmatch(x.lower()) or len(split_top(x, '/')) > 1: return ' '.join(c[i + 1:]) or None
    return c[0] if len(c) == 1 else None


def look(prop, value):
    """[(class, bucket, key)]: what one declaration adds to the look."""
    v = norm(value.replace('!important', ''))
    out = [('colour', 'literal', c) for c in colours(prop, v)]
    if not v or prop.startswith('--'): return out
    cls, part = WHOLE.get(prop), v if prop == 'font-family' else v.lower()
    if RADIUS.fullmatch(prop): cls = 'radius'
    elif EDGE.fullmatch(prop): cls = 'edge'
    elif BORDER.fullmatch(prop): cls, part = 'edge', edge_of([x for x in split_top(v.lower(), ' ') if x])
    elif prop == 'font': cls, part = 'family', family_of([x for x in split_top(v, ' ') if x])
    if cls and part: out.append((cls,) + bucket(part))
    return out
```

A `Unit` is what one entry or page reads, sets and hard-codes over all its files. A `getPropertyValue('--x')` is a read and `setProperty('--x', …)` a write
(`removeProperty` is neither); a name that is not one string is built at run time and recorded in `dynamic` with a `*` pattern; a script string that is
only token names is `named`; a script string that is only a colour is a `colour_strings` row:

```python
# ---
# id: catalog.unit
# tool: adp_catalog.py
# section: catalog
# order: 630
# needs: [catalog.look]
# tests: [catalog-inventory]
# sha: c69b4335d7a8
# ---
CALLS = {'getPropertyValue': 'read', 'setProperty': 'set', 'removeProperty': None}


def kind_of(path):
    """The type a file is read as (.css, .js or .html; a .txt file: the type before .txt), None for any other."""
    kind = os.path.splitext(path[:-4] if path.endswith('.txt') else path)[1]
    return kind if kind in ('.css', '.js', '.html') else None


def line_of(t):
    """A function from a position in t to its line."""
    ends = [m.start() for m in re.finditer('\n', t)]
    return lambda p: bisect.bisect_left(ends, p) + 1


class Unit:
    """What one entry or page reads, sets and hard-codes."""

    def __init__(self):
        self.files, self.uses, self.dynamic, self.strings = [], {}, [], []
        self.sets, self.named = collections.Counter(), collections.Counter()
        self.look = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))

    def read(self, name, fb, depth, path):
        u = self.uses.setdefault(name, {'n': 0, 'bare': 0, 'in_fallback': 0, 'fallbacks': set(), 'files': collections.Counter()})
        u['n'] += 1
        u['bare'] += fb is None
        u['in_fallback'] += depth > 0
        u['files'][path] += 1
        if fb is not None: u['fallbacks'].add(fb)

    def built(self, how, name, path, line):
        p = norm(name)
        self.dynamic.append({'file': path, 'line': line, 'how': how, 'pattern': p if '*' in p else p + '*'})

    def text(self, t, path, line, css=False):
        """The var() reads of one piece of text; line(position) is the line in the file. css: a var() inside a css string is text."""
        quoted, i = [], 0
        while css and i < len(t):
            j = skip_string(t, i) if t[i] in '"\'' else i + 1
            quoted += [(i, j)] if j > i + 1 else []
            i = j
        for name, fb, depth, pos in var_reads(t):
            if any(a < pos < b for a, b in quoted): continue
            if NAME.fullmatch(name): self.read(name, fb, depth, path)
            else: self.built('read', name, path, line(pos))

    def css(self, t, path, line, reads=True):
        """A stylesheet or a declaration list: its reads, the custom properties it assigns and its look."""
        t = css_clean(t)
        if reads: self.text(t, path, line, True)
        for _rules, prop, value, pos in css_decls(t):
            if NAME.fullmatch(prop): self.sets[prop] += 1
            elif prop.startswith('--'): self.built('set', prop, path, line(pos))
            for cls, b, key in look(prop, value): self.look[cls][b][key] += 1

    def markup(self, t, path, line, whole=False):
        """Markup: <script> as script, <style> as css, each attribute value (style as declarations). whole (a script string, which may
        be a fragment of a tag): the reads are those of the whole text."""
        chars = list(t)
        for m in re.finditer(r'<!--.*?-->', t, re.S): wipe(chars, *m.span())
        t = ''.join(chars)
        if whole: self.text(t, path, line)
        for tag, scan in (('script', lambda s, at: self.script(js_lex(s)[0], path, at)), ('style', lambda s, at: self.css(s, path, at, not whole))):
            for m in re.finditer(r'<%s\b[^>]*>(.*?)</%s>' % (tag, tag), t, re.S | re.I):
                scan(m.group(1), lambda p, o=m.start(1): line(o + p))
                wipe(chars, m.start(1), m.end(1))
            t = ''.join(chars)
        for tag in TAG.finditer(t):
            for a in ATTR.finditer(tag.group(0)):
                v, at = a.group(2)[1:-1], lambda p, o=tag.start() + a.start(2) + 1: line(o + p)
                if a.group(1).lower() == 'style':
                    self.css(v, path, at, not whole)
                    continue
                if not whole: self.text(v, path, at)
                if a.group(1).lower() in PAINT:
                    for c in colours('fill', norm(v)): self.look['colour']['literal'][c] += 1

    def calls(self, toks, path, line):
        """The property calls of a script; the strings of a name are counted here and read no further."""
        for i, k in enumerate(toks):
            if k[0] == 't':
                for p in k[1]:
                    if p[0] == 'x': self.calls(p[1], path, line)
            elif k[0] == 'w' and k[1] in CALLS and toks[i + 1:i + 2] and toks[i + 1][1] == '(':
                arg, how = toks[i + 2:operand(toks, i + 2, ARG_ENDS)], CALLS[k[1]]
                parts = [''.join(s for s, _ in str_parts(a)[0]) if a[0] in 'st' else W for a in arg if a[:2] != ['p', '+']]
                name = re.sub(W + '+', W, ''.join(parts)).strip()
                if not name.startswith(('--', W)): continue                  # an ordinary property
                if how == 'set' and NAME.fullmatch(name): self.sets[name] += 1
                elif how and NAME.fullmatch(name): self.read(name, None, 0, path)
                elif how: self.built(how, name, path, line(k[2]))
                for a in arg:
                    if a[0] in 'st': a[0] = 'w'

    def script(self, toks, path, line):
        """A script: the property calls, then every string: token names, markup (a tag in it) or css."""
        self.calls(toks, path, line)
        for ps in units(toks):
            text, starts, o = ''.join(p[0] for p in ps), [], 0
            for s, pos in ps:
                starts.append((o, pos))
                o += len(s)

            def at(p, starts=starts):
                a, b = starts[bisect.bisect_right(starts, (p, float('inf'))) - 1]
                return line(b + p - a)
            names = text.replace(',', ' ').split()
            if names and all(NAMEW.fullmatch(x) for x in names):
                for x in names:
                    if NAME.fullmatch(x): self.named[x] += 1
                    else: self.built('name', x, path, at(0))
            elif re.search(r'<[A-Za-z/!]', text): self.markup(text, path, at, True)
            else:
                self.css(text, path, at)
                c = norm(text).lower().replace(' ', '')
                if colours('color', c) == [c] and c not in NAMED: self.strings.append({'file': path, 'line': at(0), 'value': c})

    def file(self, base, rel):
        """Scan one file by the type its name carries. False for a type that holds no styles."""
        kind = kind_of(rel)
        if not kind: return False
        t = Path(os.path.join(base, rel)).read_text(encoding='utf-8')
        line = line_of(t)
        if kind == '.css': self.css(t, rel, line)
        elif kind == '.js': self.script(js_lex(t)[0], rel, line)
        else: self.markup(t, rel, line)
        self.files.append(rel)
        return True

    def out(self):
        uses = {k: dict(u, fallbacks=sorted(u['fallbacks']), files=dict(u['files'])) for k, u in self.uses.items()}
        return {'files': sorted(self.files), 'uses': uses, 'sets': dict(self.sets), 'named': dict(self.named),
                'dynamic': sorted(self.dynamic, key=lambda d: (d['file'], d['line'], d['how'], d['pattern'])),
                'colour_strings': sorted(self.strings, key=lambda d: (d['file'], d['line'], d['value'])),
                'look': {c: {b: dict(v) for b, v in self.look[c].items()} for c in CLASSES if c in self.look}}
```

A theme is its stylesheet and its JSON. Per theme: `blocks` (each rule: `selector`, `scheme` of `light`, `dark-media`, `dark-attr` or `other`, `line`, `tokens`
counted, `color-scheme`, `other` declarations), `declares` (`{token: {light, dark}}`; light is every `:root` rule, dark the `[data-theme="dark"]` rule;
`dark_via` names the tokens with a dark value that a light-only value reads), `media_differs` (tokens whose `prefers-color-scheme` value is not the
`[data-theme="dark"]` one), `uses` (the tokens a value reads through `var()`: `by` and `declared`), `json` (the CSS against the JSON, light and dark:
`only_css`, `only_json`, `differ`; the JSON `scale` counts as light, and a token that follows another through `var()` or `dark_via` is compared by the
value it ends up with) and `convention` (the JSON against the tokens `theme.default`'s JSON sets: `missing`, `extra`):

```python
# ---
# id: catalog.theme
# tool: adp_catalog.py
# section: catalog
# order: 640
# needs: [catalog.unit]
# tests: [catalog-inventory]
# sha: b53a6e011b5e
# ---
def glob(pattern):
    """A name pattern (* for a run-time part, <word> for a placeholder) as a regex."""
    return re.compile(re.sub(r'\\\*|<[^>]*>', r'[\\w-]*', re.escape(pattern)))


def canon(v):
    return re.sub(r'\s*([,()/])\s*', r'\1', norm(v or '')).lower()


def scheme_of(rules):
    sel = rules[-1][0] if rules else ''
    if len(rules) == 1: return 'light' if sel == ':root' else 'dark-attr' if re.fullmatch(r':root\[data-theme=["\']?dark["\']?\]', sel) else 'other'
    dark = len(rules) == 2 and re.match(r'@media\b.*prefers-color-scheme\s*:\s*dark', rules[0][0]) and sel.startswith(':root')
    return 'dark-media' if dark else 'other'


def theme(base, css, data, ref):
    """One theme: its css rule by rule, what it declares and reads, the css against the json, the json against the convention ref.
    Returns it with the json as read."""
    t = css_clean(Path(os.path.join(base, css)).read_text(encoding='utf-8'))
    line, blocks, maps = line_of(t), {}, {'light': {}, 'dark-attr': {}, 'dark-media': {}, 'other': {}}
    for rules, prop, value, pos in css_decls(t):
        at = rules[-1][1] if rules else 0
        b = blocks.setdefault(at, {'selector': ' '.join(r[0] for r in rules), 'scheme': scheme_of(rules), 'line': line(at),
                                   'tokens': 0, 'color-scheme': None, 'other': []})
        if prop.startswith('--'):
            b['tokens'] += 1
            maps[b['scheme']][prop] = norm(value)
        elif prop == 'color-scheme': b['color-scheme'] = norm(value)
        else: b['other'].append({'property': prop, 'value': norm(value), 'line': line(pos)})
    light, dark = maps['light'], maps['dark-attr']
    reads = {k: sorted({r[0] for v in (light.get(k), dark.get(k)) if v for r in var_reads(v)}) for k in set(light) | set(dark)}

    def via(k, seen=()):
        """The tokens with a dark value that the light-only token k reads, directly or through another light-only token."""
        return sorted({d for r in reads[k] if r in reads and r not in seen for d in ([r] if r in dark else via(r, seen + (k,)))})
    declares = {k: dict({'light': light.get(k), 'dark': dark.get(k)}, **({'dark_via': via(k)} if k not in dark and via(k) else {}))
                for k in reads}
    uses = collections.defaultdict(lambda: set())
    for k, names in reads.items():
        for r in names: uses[r].add(k)
    j = json.loads(Path(os.path.join(base, data)).read_text(encoding='utf-8'))

    def end(m, alt, k, seen=()):
        """The value token k ends up with in map m (alt: the map behind it), following a value that is one var()."""
        v = m.get(k, alt.get(k))
        r = re.fullmatch(r'var\(\s*(--[\w-]+)\s*\)', v or '')
        go = r and r.group(1) not in seen and (r.group(1) in m or r.group(1) in alt)
        return end(m, alt, r.group(1), seen + (k,)) if go else canon(v)
    sides = {}
    for s, cm, calt, jm, jalt in (('light', light, {}, dict(j.get('scale', {}), **j['light']), {}), ('dark', dark, light, j['dark'], j['light'])):
        mine = set(cm) | {k for k in declares if s == 'dark' and 'dark_via' in declares[k]}      # a dark_via token needs no dark value of its own
        sides[s] = {'only_css': sorted(set(cm) - set(jm)), 'only_json': sorted(set(jm) - mine),
                    'differ': sorted(k for k in mine & set(jm) if canon(cm.get(k, calt.get(k))) != canon(jm[k]) and end(cm, calt, k) != end(jm, jalt, k))}
    conv = {s: {'missing': sorted(set(ref[s]) - set(j[s])), 'extra': sorted(set(j[s]) - set(ref[s]))} for s in ('light', 'dark')} if ref else None
    return {'files': {'css': css, 'json': data}, 'blocks': sorted(blocks.values(), key=lambda b: b['line']), 'declares': declares,
            'media_differs': sorted(k for k in set(dark) | set(maps['dark-media']) if dark.get(k) != maps['dark-media'].get(k)),
            'uses': {r: {'by': sorted(by), 'declared': r in reads} for r, by in uses.items()}, 'json': sides, 'convention': conv}, j
```

The `@tokens` tag of an entry's main file is what it declares: `required`, `optional` (a trailing `?`) and `patterns` (a `<placeholder>`); `declared`
returns it, and where `needs.tokens` of the index says otherwise (`header_only`, `needs_only`; only an index that carries `needs.tokens` can),
`(None, None)` for an entry with no `@tokens` tag:

```python
# ---
# id: catalog.declared
# tool: adp_catalog.py
# section: catalog
# order: 650
# needs: [catalog.theme]
# tests: [catalog-inventory]
# sha: 2f49961ef957
# ---
def declared(cat, e):
    """(what the @tokens tag of the entry's main file declares, where catalog.json needs.tokens says otherwise); (None, None) without the tag."""
    main = main_file(e)
    tags = parse(comment_of(Path(os.path.join(cat, main)).read_text(encoding='utf-8'), main) or '')[2] if main else []
    v = next((v for n, v in tags if n == 'tokens'), None)
    if v is None: return None, None
    toks = [] if v == 'none' else split(v, spaces=True)
    d = {'required': [], 'optional': [], 'patterns': []}
    for tok in toks: d['patterns' if '<' in tok else 'optional' if tok.endswith('?') else 'required'].append(tok.rstrip('?'))
    needs = set()                                       # needs.tokens is prose: "--a, --b-0..4 (optional)", "plus kit/vocab.css"
    for s in e.get('needs', {}).get('tokens', []):
        for m in re.finditer(r'(--[A-Za-z0-9_<\x3e-]+?)(\d+)\.\.(\d+)|--[A-Za-z0-9_<\x3e-]+', s):
            names = [m.group(1) + str(n) for n in range(int(m.group(2)), int(m.group(3)) + 1)] if m.group(1) else [m.group(0)]
            needs.update(n + ('?' if '(optional' in s else '') for n in names)
    differ = {'header_only': sorted(set(toks) - needs), 'needs_only': sorted(needs - set(toks))}
    return {k: sorted(x) for k, x in d.items()}, differ if differ['header_only'] or differ['needs_only'] else None
```

The inventory. `convention` is the token names `theme.default`'s JSON sets, light and dark: what every theme must set. Each other entry has its `kind`
(the id prefix), `files` (the ones scanned), `declares`, `needs_differ` (only when it exists), `uses` (`{token: {n, bare, in_fallback, fallbacks, files}}`:
`n` reads, `bare` with no fallback, `in_fallback` inside another `var()`'s fallback), `sets` (custom properties assigned, `{token: n}`), `named`
(script strings that are only token names; how each is used is not resolved), `dynamic` (`[{file, line, how, pattern}]`: a name built at run time,
`how` being `"read"`, `"set"` or `"name"`; a string that ends in `-`, such as `'--f-'`, is the start of a name), `colour_strings`, `undeclared` (read, but not in the
tag, not matched by its patterns and not written by the entry), `unused` (in the tag, but never read or named, and matched by no run-time pattern of the entry)
and `look`. `units` holds the same without `declares` for what is not an entry: `catalog.page` (the files of `catalog/` no entry lists) and
`base.<name>` (`templates/<name>/`). `coverage` accounts for every file: `files` = `scanned` + `theme` (the themes' CSS and JSON) + `unread`, which lists
`{file, why, names}` for the files that hold no styles (`why` is the role an entry lists it under, `index` for `catalog.json`, else `unlisted`; `names` is
every `--name` in the text), and `outside` lists `{file, copy_of, names}` for script, style and markup files elsewhere under `DIR` (`copy_of` is the
scanned file with the same bytes, else `null`). `tokens{name}` turns it round: the themes that define it (CSS and JSON, light and dark), whether
the convention has it, the entries that declare it, and `read`, `read_in_themes`, `"set"`, `named` and `dynamic` counts by entry or unit.

```python
# ---
# id: catalog.inventory
# tool: adp_catalog.py
# section: catalog
# order: 660
# needs: [catalog.declared]
# tests: [catalog-inventory]
# sha: 348c352336de
# ---
def inventory(root):
    root = os.path.abspath(root)
    base, cat, tpl = os.path.dirname(root), os.path.join(root, 'catalog'), os.path.join(root, 'templates')

    def rel(*p): return os.path.relpath(os.path.join(*p), base).replace(os.sep, '/')

    def paths(e, role=None): return [rel(cat, f['path']) for f in e['files'] if role in (None, f.get('role'))]
    entries = sorted(json.loads(Path(cat, 'catalog.json').read_text(encoding='utf-8'))['entries'], key=lambda e: e['id'])
    found = sorted(rel(d, f) for top in (cat, tpl) if os.path.isdir(top) for d, _, fs in os.walk(top) for f in fs)
    themes = [e for e in entries if e['id'].startswith('theme.')]
    themed, listed = {p for e in themes for p in paths(e)}, {p for e in entries for p in paths(e)}
    default = next((e for e in themes if e['id'] == 'theme.default'), None)
    ref = json.loads(Path(os.path.join(base, paths(default, 'data')[0])).read_text(encoding='utf-8')) if default else None
    out = {'schema': 'adp-inventory/1', 'themes': {}, 'entries': {}, 'units': {},
           'convention': {s: sorted(ref[s]) for s in ('light', 'dark')} if ref else None}
    data, scanned = {}, set()
    for e in themes: out['themes'][e['id']], data[e['id']] = theme(base, paths(e, 'style')[0], paths(e, 'data')[0], ref)

    def unit(files, extra):
        u = Unit()
        scanned.update(p for p in files if u.file(base, p))
        return dict(extra, **u.out())
    for e in entries:
        if e in themes: continue
        d, differ = declared(cat, e)
        x = unit(paths(e), {'kind': e['id'].split('.')[0], 'declares': d})
        if differ: x['needs_differ'] = differ
        known = d['required'] + d['optional'] if d else []
        pats, built = [glob(p) for p in (d['patterns'] if d else [])], [glob(y['pattern']) for y in x['dynamic']]
        x['undeclared'] = sorted(k for k in x['uses'] if k not in known and k not in x['sets'] and not any(p.fullmatch(k) for p in pats))
        x['unused'] = sorted(k for k in known if k not in x['uses'] and k not in x['named'] and not any(p.fullmatch(k) for p in built))
        out['entries'][e['id']] = x
    out['units']['catalog.page'] = unit([p for p in found if p.startswith(rel(cat) + '/') and p not in listed and p != rel(cat, 'catalog.json')], {})
    for name in sorted(os.listdir(tpl)) if os.path.isdir(tpl) else []:
        if os.path.isdir(os.path.join(tpl, name)): out['units']['base.' + name] = unit([p for p in found if p.startswith(rel(tpl, name) + '/')], {})
    role_of, same = collections.defaultdict(lambda: set()), {}
    for e in entries:
        for f in e['files']: role_of[rel(cat, f['path'])].add(f.get('role') or 'file')
    for p in sorted(scanned): same.setdefault(Path(os.path.join(base, p)).read_bytes(), p)

    def names(p): return sorted({m.group(0) for m in IN_TEXT.finditer(Path(os.path.join(base, p)).read_text(encoding='utf-8', errors='replace'))})
    unread = [{'file': p, 'why': 'index' if p == rel(cat, 'catalog.json') else '+'.join(sorted(role_of[p])) if p in role_of else 'unlisted',
               'names': names(p)} for p in found if p not in scanned and p not in themed]
    beyond = sorted(rel(d, f) for d, _, fs in os.walk(root) for f in fs if kind_of(f) and rel(d, f) not in found)
    outside = [{'file': p, 'copy_of': same.get(Path(os.path.join(base, p)).read_bytes()), 'names': names(p)} for p in beyond]
    out['coverage'] = {'files': len(found), 'scanned': len(scanned), 'theme': len(themed), 'unread': unread, 'outside': outside}
    tok = collections.defaultdict(lambda: {'themes': {'css': {'light': [], 'dark': []}, 'json': {'light': [], 'dark': []}},
                                           'convention': {'light': False, 'dark': False}, 'declared': {'required': [], 'optional': []},
                                           'read': {}, 'read_in_themes': {}, 'set': {}, 'named': {}, 'dynamic': []})
    for i, t in out['themes'].items():
        for k, v in t['declares'].items():
            for s in ('light', 'dark'):
                if v[s] is not None or s == 'dark' and 'dark_via' in v: tok[k]['themes']['css'][s].append(i)
        for s in ('light', 'dark'):
            for k in data[i][s]: tok[k]['themes']['json'][s].append(i)
            for k in ref[s] if i == 'theme.default' else []: tok[k]['convention'][s] = True
        for k, v in t['uses'].items(): tok[k]['read_in_themes'][i] = len(v['by'])
    for i, x in list(out['entries'].items()) + list(out['units'].items()):
        for s in ('required', 'optional'):
            for k in (x.get('declares') or {}).get(s, []): tok[k]['declared'][s].append(i)
        for k, u in x['uses'].items(): tok[k]['read'][i] = u['n']
        for field, into in (('sets', 'set'), ('named', 'named')):
            for k, n in x[field].items(): tok[k][into][i] = n
    for i, x in list(out['entries'].items()) + list(out['units'].items()):
        for y in x['dynamic']:
            if y['pattern'].replace('*', '').strip('-'):     # * and --* fit every name: they stay with their entry
                for k in [k for k in tok if glob(y['pattern']).fullmatch(k)]: tok[k]['dynamic'].append(dict(y, **{'in': i}))
    out['tokens'] = dict(tok)
    return out
```

The command prints the JSON with sorted keys, indented one space, and exits 0; a catalog or theme file it cannot read or parse is the one line
`FAIL: ...` on stderr and exit 1; an unknown option exits 1 with `unknown option X`:

```python
# ---
# id: catalog.inventory-command
# tool: adp_catalog.py
# section: catalog
# order: 670
# needs: [catalog.inventory]
# tests: [catalog-inventory]
# sha: 56317d0c394e
# ---
def inventory_main(argv):
    """inventory [--root DIR]: what every theme, entry and page declares, reads and hard-codes, as one JSON."""
    root, a = HERE, list(argv)
    while a:
        if (x := a.pop(0)) == '--root' and a: root = a.pop(0)
        else: sys.exit(f'unknown option {x}')
    try: out = inventory(root)
    except (OSError, ValueError, KeyError, IndexError) as e:
        print(f'FAIL: {e!r}', file=sys.stderr)
        return 1
    print(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False))
    return 0
```

The tool's entry point: the commands by name, and the check when the first argument is not one:

```python
# ---
# id: catalog.main
# tool: adp_catalog.py
# section: catalog
# order: 990
# needs: [catalog.inventory-command]
# tests: [catalog-build, catalog-check-passes-a-built-tree]
# sha: 0301fcff7aee
# ---
COMMANDS = {'build': build, 'headers': headers, 'inventory': inventory_main, 'drift': drift}


def main(argv):
    return COMMANDS[argv[0]](argv[1:]) if argv and argv[0] in COMMANDS else check_catalog(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
```

## Reading a catalog: `kit`, `suggest`, `take`

These read a `catalog.json`: the fetched live one (by its url, or `-` for the saved one), or a local build, which they accept with this line on
stderr, before any other:

```
warning: a local index is a build, not the live catalog: a file it lists may be missing there
```

Fields that live only in the main file's header (`about`, `status`, `version`, `config`, `db`) are read from the header on disk; `@db` is printed
as `{reads, writes, note}`, with empty lists and an empty note for `none`.

| Command | Prints | Exit |
|---|---|---|
| `kit list CATALOG [--kind K] [--tag T]` | one JSON line per entry, in index order: `{id, kind, name, summary, tags}` (`kind` here is the id prefix, not the entry's `kind` field). `--kind` matches the prefix or the entry's `kind`; `--tag` matches one tag exactly | 0 |
| `kit show ID CATALOG` | `{id, name, summary, about, tags, files, requires, provides}`, then `status`, `version`, `config: [[signature, options]]` and `db` when the header sets them | 0; 1 with `no entry ID in the catalog` on stderr for an unknown id |
| `kit describe ID CATALOG` | how to wire it: `{id, needs (its @globals), optional, provides, requires, files (every file but samples), sample (the bundle path), sample_key, db}` | 0; 1 as `show` |
| `suggest CATALOG --for "words" [--n 3] [--kind K]` | `[{id, kind, why, requires, takes}]` scored as below; no model call | 0 |
| `take CATALOG ID ... --url URL` | `{catalog {url, index, live, ver, built, warning?}, entries (with every @requires, in load order), files {path: {artifact, path}}, sha256, samples}`: references, never copies | 0; 1 for an unknown id, or a local index without `--url` |

**How `suggest` scores.** The words are the runs of `[a-z0-9]` in the lowercased `--for` text; each word longer than three letters that ends in
`s` adds itself without the `s`; the stop words `a an and or the of to in on for with between by is it as at my that this from` are removed.
For each entry (only those whose id prefix is `--kind`, when given), with the same word split applied to each field:

| Field | Counts | Weight |
|---|---|---|
| tags | each tag that contains a wanted word | 3 |
| name/summary | the name and summary joined by a space: each wanted word found | 1 |
| id | each wanted word found | 1 |
| provides | the names joined by spaces: each wanted word found | 2 |
| about | each wanted word found | 1 |

An entry scoring 0 is left out. The rest are grouped by id prefix; the groups are printed in prefix order, each sorted by score descending then
id, and cut to `--n` entries. `why` lists the hits, separated by `; `: `tags: ` and the matching tags in tag order, then for each other field
with a hit, in the table's order, its name, `: ` and the matched words sorted, comma-separated (`tags: bar, progress; name/summary: bar; about: bar`).
`takes` is the number of the entry's files that are not samples.

`take` resolves `@requires` first: taking `viz.meter` takes `kit.badge` too, and its `files` are the publish `files` entries a page adds.

Its fixtures and vectors are in [vectors.md](vectors.md).

## My Own Kit: `catalog`

`catalog URL` saves the user's catalog url in `ADP_HOME/config.json` and keeps its files in `ADP_HOME/catalog/`. It does not fetch anything; it prints
the Artifact `read` calls for you to run.

| State | `catalog [URL]` prints |
|---|---|
| no catalog url saved | `{catalog: null, next}` |
| no `catalog.json` in `ADP_HOME/catalog/` | `{catalog, index, fetched: false, fetch}`; `fetch` is the Artifact `read` call that saves `catalog.json` there. Run it, then run `catalog` again |
| `catalog.json`, files missing | `{catalog, index, fetched: true, ver, built, entries, refresh, kit, files, missing, complete: false, reads, calls, per_call, next}`; `reads` holds Artifact `read` calls of at most 256 paths each, `refresh` is the `read` that re-fetches `catalog.json` |
| every file the index lists | the same with `missing: 0`, `complete: true` and no `reads` |

Its fixtures and vectors are in [vectors.md](vectors.md).

### The code: `catalog`

The fragments of `adp.py` this skill owns. `catalog.reads` finds the files of My Own Kit that are missing or changed and plans the reads that bring
them: one `Artifact read` per folder group, at most 256 paths each, and a folder is not split while the call has room:

```python
# ---
# id: catalog.reads
# tool: adp.py
# section: catalog
# order: 700
# needs: [kit.take]
# tests: [catalog-fetch-into-my-own-kit, catalog-reads-an-older-folder]
# sha: a5c2e437fb3d
# ---
READ_MAX = 256                                       # paths in one Artifact read


def cat_dir(url):
    """Where the user's own kit sits on disk: ADP_HOME/catalog. A copy fetched into ADP_HOME/catalogs/<id>/ is used while the new folder has no index."""
    new, old = Path(ADP_HOME, 'catalog'), Path(ADP_HOME, 'catalogs', url.rstrip('/').rsplit('/', 1)[-1])
    return old if (old / 'catalog.json').is_file() and not (new / 'catalog.json').is_file() else new


def fetch_call(url):
    """The Artifact read that brings a catalog's live index to disk, where `take` and `catalog` find it."""
    return {'tool': 'Artifact', 'action': 'read', 'url': url, 'path': 'catalog.json', 'out_dir': str(cat_dir(url)),
            'then': 'run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)'}


def kit_missing(root, cat):
    """(every path the index lists, the ones not on disk under root or whose sha256 differs)"""
    want = {}
    for e in cat.get('entries', []):
        for f in e.get('files', []):
            if isinstance(f, dict) and f.get('path'): want.setdefault(f['path'], f.get('sha256'))
        if e.get('main'): want.setdefault(e['main'], None)
    want = {p: h for p, h in want.items() if not p.startswith('/') and '..' not in p.split('/')}
    return sorted(want), [p for p, h in sorted(want.items()) if not Path(root, p).is_file() or (h and hashlib.sha256(Path(root, p).read_bytes()).hexdigest() != h)]


def kit_reads(url, root, paths):
    calls, cur, folders = [], [], {}
    for p in sorted(paths): folders.setdefault(p.rpartition('/')[0], []).append(p)
    for group in folders.values():
        if cur and len(cur) + len(group) > READ_MAX: calls.append(cur); cur = []
        while len(group) > READ_MAX: calls.append(group[:READ_MAX]); group = group[READ_MAX:]
        cur += group
    return [{'tool': 'Artifact', 'action': 'read', 'url': url, 'paths': c, 'out_dir': str(root),
             'then': 'run `adp.py catalog` again: complete is true when every file is here'} for c in calls + [cur] * bool(cur)]
```

`catalog [URL]` is My Own Kit: with a URL it saves it in `ADP_HOME/config.json`; it then prints where the saved catalog stands (the table in
[My Own Kit](#my-own-kit-catalog)). It never fetches:

```python
# ---
# id: catalog.my-kit
# tool: adp.py
# section: catalog
# order: 710
# needs: [catalog.reads]
# tests: [catalog-fetch-into-my-own-kit, catalog-refuses-a-wrong-url]
# sha: eab3bceedd11
# ---
@cmd('catalog')
def catalog(a):
    """catalog [URL]    save the user's catalog url, then print the reads that keep a local copy of it complete (My Own Kit)"""
    if pos := bare(a):
        if not CAT_URL.fullmatch(pos[0]): sys.exit('catalog: use a Claude artifact URL')
        cfg = Path(ADP_HOME, 'config.json')
        os.makedirs(ADP_HOME, exist_ok=True)
        cfg.write_text(json.dumps({**(read_json(cfg) if cfg.is_file() else {}), 'catalog': pos[0].rstrip('/')}, indent=1))
    url = saved_catalog()
    if not url: return emit({'catalog': None, 'next': "adp.py catalog <url> saves the user's catalog (SKILL.md says how to find it); never assume one"})
    root = cat_dir(url)
    idx = root / 'catalog.json'
    out = {'catalog': url, 'index': str(idx), 'fetched': idx.is_file()}
    if not out['fetched']: return emit({**out, 'fetch': fetch_call(url)})
    cat = read_json(idx)
    every, bad = kit_missing(root, cat)
    out.update(ver=cat.get('ver') or None, built=cat.get('built'), entries=len(cat.get('entries', [])), refresh=fetch_call(url),
               kit=str(root), files=len(every), missing=len(bad), complete=not bad)
    if bad:
        reads = kit_reads(url, root, bad)
        out.update(reads=reads, calls=len(reads), per_call=[len(r['paths']) for r in reads], next='My Own Kit is not complete: make the reads, then run adp.py catalog again')
    emit(out)
```

`kit` and `suggest` read a catalog's index: `index_of` resolves CATALOG as `take` does (a url: the fetched index, `-`: the saved catalog, else a local
`catalog.json`, which comes with a warning), and `read_headers` reads the main-file header of each entry from where the catalog's files sit (the folder
of a local `catalog.json`, or My Own Kit). The tool stays offline: the main files not on disk come back as `Artifact read` calls. The header parser is
the one `adp_catalog.py` has:

```python
# ---
# id: catalog.read-index
# tool: adp.py
# section: catalog
# order: 720
# needs: [catalog.reads]
# tests: [kit-list, kit-show, suggest-by-words, kit-reads-a-url-catalog]
# sha: 596242836aaf
# ---
def header_lib():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adp_catalog
    return adp_catalog


def index_of(src):
    """(catalog dict, warning or None) for a CATALOG argument."""
    src = saved_catalog() or sys.exit('no saved catalog; adp.py catalog <url> saves one') if src == '-' else src
    if CAT_URL.fullmatch(src):
        idx = cat_dir(src) / 'catalog.json'
        if not idx.is_file():
            emit({'error': 'index not fetched', 'catalog': src.rstrip('/'), 'fetch': fetch_call(src.rstrip('/')), 'next': 'adp.py catalog fetches your whole kit (My Own Kit)'})
            sys.exit(2)
        return read_json(idx), None
    if not os.path.isfile(src): sys.exit(f'{src} is neither a catalog url nor a catalog.json')
    return read_json(src), 'a local index is a build, not the live catalog: a file it lists may be missing there'


def read_headers(src, entries):
    """({id: header}, main files not on disk, the reads that fetch them): [] when every header was read, or the catalog is local."""
    lib = header_lib()
    src = saved_catalog() if src == '-' else src
    url = src.rstrip('/') if CAT_URL.fullmatch(src) else None
    root = cat_dir(url) if url else Path(src).resolve().parent
    heads, want = {}, []
    for e in entries:
        m = lib.main_file(e)
        if not m or m.startswith('/') or '..' in m.split('/'): continue
        if Path(root, m).is_file(): heads[e['id']] = lib.parse_header(Path(root, m).read_text(encoding='utf-8', errors='replace'), m)
        else: want.append(m)
    return heads, want, [{'tool': 'Artifact', 'action': 'read', 'url': url, 'paths': want[i:i + READ_MAX], 'out_dir': str(root), 'then': 'run the command again'}
                         for i in range(0, len(want), READ_MAX)] if url else []
```

`suggest CATALOG --for "words" [--n 3] [--kind K]` scores the entries (the table above); `kit list|show|describe` prints one entry's
fields, the ones in its header read from the main file:

```python
# ---
# id: catalog.suggest
# tool: adp.py
# section: catalog
# order: 730
# needs: [catalog.read-index]
# tests: [suggest-by-words, suggest-options]
# sha: e3deb3c76169
# ---
WORD = re.compile(r'[a-z0-9]+')
STOP = {'a', 'an', 'and', 'or', 'the', 'of', 'to', 'in', 'on', 'for', 'with', 'between', 'by', 'is', 'it', 'as', 'at', 'my', 'that', 'this', 'from'}


@cmd('suggest')
def suggest(a):
    """suggest CATALOG --for "free words" [--n 3] [--kind K]    the entries that fit the words, best first, per kind; no model call"""
    pos, words, n, kind = bare(a), opt(a, '--for'), int(opt(a, '--n', 3)), opt(a, '--kind')
    if len(pos) != 1 or not words: sys.exit('usage: adp.py suggest CATALOG --for "free words" [--n 3] [--kind K]')
    cat, warn = index_of(pos[0])
    want = set(WORD.findall(words.lower()))
    want = (want | {w[:-1] for w in want if len(w) > 3 and w.endswith('s')}) - STOP
    pool = [e for e in cat['entries'] if not kind or e['id'].split('.')[0] == kind]
    heads, missing, calls = read_headers(pos[0], pool)      # the about text lives in each entry's main-file header
    groups = {}
    for e in pool:
        prefix = e['id'].split('.')[0]
        hit = [t for t in e.get('tags', []) if want & set(WORD.findall(t.lower()))]
        fields = {'name/summary': e.get('name', '') + ' ' + e.get('summary', ''), 'id': e['id'], 'provides': ' '.join(e.get('provides', [])),
                  'about': heads.get(e['id'], {}).get('about') or e.get('about') or e.get('details') or ''}
        seen = {f: want & set(WORD.findall(v.lower())) for f, v in fields.items()}
        score = 3 * len(hit) + len(seen['name/summary']) + len(seen['id']) + 2 * len(seen['provides']) + len(seen['about'])
        if score: groups.setdefault(prefix, []).append((score, e['id'], {'id': e['id'], 'kind': prefix, 'requires': e.get('requires', []),
            'why': '; '.join(([f"tags: {', '.join(hit)}"] if hit else []) + [f"{f}: {', '.join(sorted(w))}" for f, w in seen.items() if w]),
            'takes': len([f for f in e['files'] if f.get('role') not in ('sample', 'preview')])}))
    if warn: print('warning: ' + warn, file=sys.stderr)
    if missing:
        print(f'note: {len(missing)} main-file headers are not on disk, so their about text was not searched (tags, name, summary, id and provides were)'
              + ('; read them, then run the command again:\n' + ''.join(json.dumps(c) + '\n' for c in calls) if calls else ''), file=sys.stderr)
    emit([x[2] for k in sorted(groups) for x in sorted(groups[k], key=lambda t: (-t[0], t[1]))[:n]])
```

```python
# ---
# id: catalog.kit
# tool: adp.py
# section: catalog
# order: 740
# needs: [catalog.read-index]
# tests: [kit-list, kit-list-by-kind, kit-show, kit-show-unknown, kit-describe, kit-reads-a-url-catalog]
# sha: c6e0dd1fbc77
# ---
@cmd('kit')
def kit(a):
    """kit list [CATALOG] [--kind K] [--tag T] | show ID [CATALOG] | describe ID [CATALOG]    read the kit's entries"""
    pos = bare(a)
    sub = pos[0] if pos else ''
    if sub not in ('list', 'show', 'describe') or (sub != 'list' and len(pos) < 2):
        sys.exit('usage: adp.py kit list [CATALOG] [--kind K] [--tag T] | show ID [CATALOG] | describe ID [CATALOG]')
    src = pos[(sub != 'list') + 1] if len(pos) > (sub != 'list') + 1 else '-'
    cat, warn = index_of(src)
    if warn: print('warning: ' + warn, file=sys.stderr)
    kind, tag = opt(a, '--kind'), opt(a, '--tag')
    if sub == 'list':
        for e in cat['entries']:
            if kind and e['id'].split('.')[0] != kind and e.get('kind') != kind or tag and tag not in e.get('tags', []): continue
            emit({'id': e['id'], 'kind': e['id'].split('.')[0], 'name': e.get('name'), 'summary': e.get('summary'), 'tags': e.get('tags', [])})
        return 0
    e = next((x for x in cat['entries'] if x['id'] == pos[1]), None) or sys.exit(f'no entry {pos[1]} in the catalog')
    heads, missing, calls = read_headers(src, [e])
    h = heads.get(e['id'], {})      # about, db, config, source and changes live in the main-file header
    if missing and not calls: print('note: the main-file header is not on disk, so about and the header fields are missing', file=sys.stderr)      # a local catalog: no call to offer
    note = {'note': 'the main-file header is not on disk, so about and the header fields are missing; read it, then run the command again', 'fetch': calls} if calls else {}
    if sub == 'show':
        return emit({'id': e['id'], 'name': e.get('name'), 'summary': e.get('summary'), 'about': h.get('about') or e.get('details') or e.get('about') or '',
                     'tags': e.get('tags', []), 'files': [f['path'] for f in e['files']], 'requires': e.get('requires', []), 'provides': e.get('provides', []),
                     **{k: h[k] for k in ('status', 'version', 'config', 'db', 'source', 'changed') if h.get(k)}, **note})
    lib = header_lib()
    sample = [f['path'] for f in e['files'] if f.get('role') == 'sample']
    pv = h.get('preview')
    keys = [k for s in (pv.get('samples') if isinstance(pv, dict) else None) or [] if isinstance(s, str) and sample for p, k in [lib.split_ref(s)] if k is not None and p == sample[0]]
    emit({'id': e['id'], 'needs': e.get('globals', []), 'optional': e.get('optional') or h.get('optional', []), 'provides': e.get('provides', []),
          'requires': e.get('requires', []), 'files': [f['path'] for f in e['files'] if f.get('role') not in ('sample', 'preview')], 'sample': sample[0] if sample else None,
          **({'sample_key': keys[0]} if keys else {}), **({'db': h['db']} if h.get('db') else {}), **note})
```
