---
name: adp-minimal-new-artifact
description: "Explains how a new ADP artifact is created and why: adp.py new, the adp/2 file tree (index.html shell, adp.js, content.js, parts/, styles/, seed.json, seed/), why not a single file, templates (the minimal template this plugin ships, how templates stack, tiers), copy as data, check, publish, first-open seeding, what the artifact service serves. Use when the user asks how to start a new ADP page, what its files are for, or which template to start from."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Creating a new artifact

Run `adp.py new` rather than hand-writing a single `index.html`. It lays the page out as **adp/2** from a template, takes its kit entries from the
catalog, and prints the publish call for it.

## Why not one file

The artifact service already keeps a hash per file, a database per page and an anchor per element. adp/2 uses those units instead of rebuilding
them inside one document:

- a change touches only the file that holds it, so a publish sends only that file and a diff points at it;
- copy (the page's text content) lives in the database, so a wording fix is a data write, not a publish;
- the shell rarely changes, so concurrent publishes rarely conflict on it.

## The file tree

`adp.py new` writes this into a folder (DIR), at the paths it is published under:

```
DIR/
  index.html          the thin shell: header, "What changed" panel, tabs, an empty <main id="views">, script tags
  adp.js              the runtime, copied byte for byte
  content.js          window.ADP_CONTENT = {<part id>: {part, title, html}}: the baseline copy of every part
  parts/app.js        the page's code, one file per part family
  styles/page.css     the page's styles
  seed.json           index of the initial database documents
  seed/pack-001.json  the packed document bodies (excluded from the manifest)
```

Kit files (`kit/...`) are **not** copied into DIR. A template's `take` list names catalog entries. When a catalog is available, `new` adds them to
the publish call as by-reference entries and the artifact service copies them server-side; otherwise `new` prints the `take` step to run before
publishing. Kit files belong to the catalog, so they are excluded from the manifest.

## Templates

A template is a folder `templates/<name>/` beside `adp.py`: a `template.json` (`name`, `summary`, `use_when`, `design`, `capabilities`, `take`, and
optionally `base`, `drop` and `installed`) and the page's files. A template with a `base` starts from that template's files and overrides files of
the same name. A template file whose name has another extension before `.txt` is written without the `.txt` (`index.html.txt` becomes
`index.html`). `{{title}}`, `{{slug}}` and `{{catalog}}` are substituted in every file except `adp.js`, which is copied byte for byte.

This plugin ships one template, **`minimal`**, as the fixture `template-minimal` in [vectors.md](vectors.md): the shell, its copy as data,
and a status list of what the runtime found on the host (connection, viewer, capabilities, integrity, seeding). It takes nothing from the catalog,
so a page built from it works with `adp.js` alone. Install it as `templates/minimal/` and start with `adp.py new minimal DIR`.

`installed: true` makes `new` write `installed.json` in DIR: `schema`, the catalog `url` (`--url`, else the catalog url of this run, else the index's own), `ver`, `built`, the `take` list and `entries` (id, name, kind,
group, summary, version, requires, in dependency order), the record of what the page took that the page's catalog tab lists.

`templates` lists them, one block each. `new` copies the chain of templates (base first, each layer overriding the one before) into DIR; a DIR that
exists and is not empty exits 1 with `DIR exists and is not empty`, a base that leads back into the chain with `template NAME: base loop (...)`, and a name that is no template with `no template NAME: ` and the names there are:

```python
# ---
# id: new.templates
# tool: adp.py
# section: new
# order: 650
# needs: [core.options, core.io]
# tests: [templates, new-ways-restored]
# sha: 68f8894d8133
# ---
TPL = HERE / 'templates'


def tmeta(name):
    if not (TPL / name / 'template.json').is_file(): sys.exit(f'no template {name}: ' + ', '.join(sorted(p.name for p in TPL.iterdir() if (p / 'template.json').is_file())))
    return read_json(TPL / name / 'template.json')


def chain(name):
    """The template and every template under it, base first; a base that leads back to a template of the chain exits 1."""
    out = []
    while name:
        if name in out: sys.exit(f'template {name}: base loop ({" -> ".join(out + [name])})')
        out.append(name); name = tmeta(name).get('base')
    return out[::-1]


def expand(take, ids):
    """`kind.*` in a take list is every entry of that kind the index has, in its order (none without an index)."""
    return [x for t in take for x in ([i for i in ids if i.startswith(t[:-1])] if t.endswith('.*') else [t])]


def layered(name):
    """{page path: source file} of a template and its bases, base first; `drop` removes paths. A `.txt` suffix is dropped when the name has another extension."""
    meta, files = tmeta(name), {}
    if meta.get('base'): files = layered(meta['base'])
    for f in sorted(x for x in (TPL / name).rglob('*') if x.is_file() and x.name != 'template.json'):
        rel = f.relative_to(TPL / name).as_posix()
        files[rel[:-4] if rel.endswith('.txt') and Path(rel[:-4]).suffix else rel] = f
    for p in meta.get('drop', []): files.pop(p, None)
    return files


@cmd('templates')
def templates(a):
    """templates    the templates `new` can start from, and when to use each"""
    names = sorted(p.name for p in TPL.iterdir() if (p / 'template.json').is_file())
    w = max(map(len, names)) + 4
    for n in names:
        m = tmeta(n)
        print(f"{n:<{w}}{m['summary']}\n{'':<{w}}use when: {m['use_when']}")
```

`{{catalog}}` is the `--catalog` value when it is a catalog URL, else the URL saved by `adp.py catalog` (also when `--catalog` is a local `catalog.json`), else the text
`none saved yet: python3 adp.py catalog <url> saves the owner's catalog url`.

The options of `new`:

- `--title T` (default `Untitled artifact`) and `--slug S` (default: the title in lowercase kebab, cut at 40 characters, `artifact` when the title has no letter or digit); a slug that is not lowercase kebab exits 1 with `--slug: lowercase kebab, e.g. status-pill`.
- `--tier T` names the template to start from instead of TEMPLATE: `--tier minimal DIR`. `--tier full` exits 1 with `tier full is not available yet`.
- `--summary S` and `--role R` go to the seed, as in `seed`.
- `--url URL` is the catalog url when `--catalog` is a local `catalog.json`.
- `--by NAME` (default `adp`) names the author of the seed, as in `seed`.
- `--data FILE|DIR` adds the page's own records to the seed, as `seed --data` does ([packing](../adp-minimal-packing/SKILL.md)).
- `--catalog URL|-|catalog.json` names the catalog the page takes entries from; omitted or `-`, the catalog saved by `adp.py catalog`.
- `--theme NAME` (repeatable) takes a theme: a short name (`paper`) or an id (`theme.paper`). When the catalog's index is on disk and has no
  such theme, it exits 1 with `--theme NAME: the catalog has no such theme. It has: ` and the short names, and writes nothing. Without
  `--theme`, the page takes `theme.default` when the index has it.
- `--layout ID` (repeatable) takes a catalog entry by id.

The page's take list is the template's `take` (`kind.*` stands for every entry of that kind in the index), then the themes, then the `--layout` ids, without repeats; it is printed as `take`. With a catalog,
`new` runs `take` on that list, merges its `files` into `publish.files`, and links the themes and `--layout` entries in `index.html` as
[themes](../adp-minimal-themes/SKILL.md#applying-a-theme) describes. A `take` failure prints its error (`{error, catalog, reason}` for one the take itself raised) and exits 2, before anything is
written. Without a catalog, `next` says to take the list later.

Besides `{{title}}`, `{{slug}}` and `{{catalog}}`, every template file may carry the info placeholders: `{{adp_version}}` (the skill's version), `{{adp_sha}}` and `{{adp_sha12}}`
(the sha256 of `adp.js`, whole and first 12 characters), `{{adp_catalog}}` and `{{adp_components}}` (one `<tr>` of id, version and hash for each entry the page takes, or `none taken`).

```python
# ---
# id: new.new
# tool: adp.py
# section: new
# order: 660
# needs: [new.templates, themes.link, kit.take, packing.seed]
# tests: [new-minimal, new-from-a-catalog, new-refuses-a-non-empty-folder, new-full-tier-is-not-available, new-refuses-a-bad-slug, new-refuses-an-unknown-theme]
# sha: 72d3bf97384e
# ---
import hashlib, html
@cmd('new')
def new(a):
    """new TEMPLATE DIR [--tier T] [--title T] [--slug S] [--by NAME] [--data FILE|DIR] [--summary S] [--role R] [--theme NAME] [--layout ID] [--catalog URL|-|catalog.json] [--url URL]    start a page"""
    pos = bare(a)
    if '--tier' in a:
        tier = opt(a, '--tier')
        if tier == 'full': sys.exit('tier full is not available yet')
        if not (TPL / tier / 'template.json').is_file(): sys.exit(f'tier {tier}: no template of that name')
        pos = [tier] + pos
    if len(pos) != 2: sys.exit('usage: adp.py new TEMPLATE|--tier T DIR [--title T] [--slug S] [--by NAME] [--data FILE|DIR] [--theme NAME] [--layout ID] [--catalog URL|-|catalog.json]')
    name, d = pos
    if Path(d).is_dir() and any(Path(d).iterdir()): sys.exit(f'{d} exists and is not empty')
    layers, d = chain(name), Path(d)
    meta = tmeta(name)
    title = opt(a, '--title', 'Untitled artifact')
    slug = opt(a, '--slug') or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:40] or 'artifact'
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', slug): sys.exit('--slug: lowercase kebab, e.g. status-pill')
    every = lambda flag: [a[i + 1] for i, x in enumerate(a) if x == flag]
    src = opt(a, '--catalog')
    if src in (None, '-'): src = saved_catalog()
    live = bool(src and CAT_URL.fullmatch(src))
    index = cat_dir(src) / 'catalog.json' if live else Path(src or '')
    index = read_json(index) if index.is_file() else {}
    ids = [e['id'] for e in index.get('entries', [])]
    themes = ['theme.' + t.removeprefix('theme.') for t in every('--theme')]
    have = [i[6:] for i in ids if i.startswith('theme.')]
    if have and (bad := [t for t in themes if t[6:] not in have]):
        sys.exit(f'--theme {bad[0][6:]}: the catalog has no such theme. It has: ' + ', '.join(have))
    themes = themes or [i for i in ids if i == 'theme.default']
    tk = list(dict.fromkeys(expand(meta.get('take', []), ids) + themes + every('--layout')))
    got = None
    if src and (index or opt(a, '--catalog')) and tk:
        try: got, code = taken(src, tk, opt(a, '--url'))
        except SystemExit as e: got, code = {'error': 'take failed', 'catalog': src, 'reason': str(e.code)}, 2
        if code: emit(got); return 2
    cat = (src if live else saved_catalog()) or 'none saved yet: python3 adp.py catalog <url> saves the owner\'s catalog url'
    by, skill = {e['id']: e for e in index.get('entries', [])}, HERE / 'SKILL.md'
    ver = re.search(r'^  version: "?([^"\s]+)', skill.read_text(encoding='utf-8') if skill.is_file() else '', re.M)
    cell = lambda v: '<td>' + html.escape(str(v or '')) + '</td>'
    info = {'title': title, 'slug': slug, 'catalog': cat, 'adp_catalog': html.escape(cat),
            'adp_version': html.escape(ver[1] if ver else 'unknown'),
            'adp_components': ''.join('<tr>' + cell(i) + cell(by.get(i, {}).get('version')) + cell(by.get(i, {}).get('hash')) + '</tr>'
                                      for i in (got['entries'] if got else tk)) or '<tr><td colspan="3">none taken</td></tr>'}
    info['adp_sha'] = hashlib.sha256((HERE / 'assets' / 'adp.js').read_bytes()).hexdigest(); info['adp_sha12'] = info['adp_sha'][:12]
    sub = lambda s: re.sub(r'\{\{(\w+)\}\}', lambda m: info.get(m[1], m[0]), s)
    files = layered(name); files['adp.js'] = HERE / 'assets' / 'adp.js'
    for rel, f in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_bytes(f.read_bytes()) if rel == 'adp.js' else (d / rel).write_text(sub(f.read_text(encoding='utf-8')), encoding='utf-8')
    if got and (asked := themes + every('--layout')):
        link, _ = taken(src, asked, opt(a, '--url'))
        link_tags(d, link['files'], list(link.get('fonts', {}).values()))
    if any(tmeta(n).get('installed') for n in layers):      # the My catalog tab lists this file; `files` takes the same entries again
        by = {e['id']: e for e in index.get('entries', [])}
        keep = ('id', 'name', 'kind', 'group', 'summary', 'version', 'requires')
        (d / 'installed.json').write_text(json.dumps({'schema': 'installed/1', 'url': opt(a, '--url') or (cat if CAT_URL.fullmatch(cat) else '') or index.get('url') or '',
            'ver': index.get('ver') or '', 'built': index.get('built') or '', 'take': tk,
            'entries': [{k: by[i][k] for k in keep if k in by[i]} if i in by else {'id': i} for i in (got['entries'] if got else tk)]},
            ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    seed_file(str(d), opt(a, '--by', 'adp'), data=data_docs(every('--data')), role=opt(a, '--role'), summary=opt(a, '--summary'))
    design = next((m['design'] for m in (tmeta(n) for n in reversed(layers)) if m.get('design')), '')
    out = {'template': name, 'dir': str(d), 'title': title, 'slug': slug,
           'publish': dict(publish_args(str(d)), capabilities=meta.get('capabilities', {})), 'take': tk, 'design': design}
    if got: out['publish']['files'].update(got['files']); out['catalog'] = got['catalog']; out['entries'] = got['entries']
    out['next'] = [f'adp.py check {d}',
                   'Design it: read `design` above, take a theme and the layouts the content needs from the catalog, then write page.css and the views for this content (a script that emits them beats typing)',
                   'Artifact publish with the `publish` arguments (first publish: add icon; label "adp/2 start")'
                   + ('; its files already carry the kit entries' if got else ''),
                   *([f'adp.py take {src or "<catalog url>"} ' + ' '.join(tk) + ', then publish those files to the same url'] if tk and not got else []),
                   'Open the page as an editor (you, or the owner): it expands seed.json and seed/ into its database on that first open and shows what ADP is while it does. '
                   f'Only when nobody can open it: adp.py seed {d} --batches prints the ArtifactData batches']
    emit(out)
```

## The shape of a part

Every view and its main sections are parts, in the markers of [parts and hashes](../adp-minimal-parts/SKILL.md). A part's copy is a
`content/<part id>` document with an `html` field. `content.js` carries the same copy as the fallback when the database is unavailable; the database
overrides it live, and the page's code repaints `[data-part]` elements when `content/` changes.

```js
// content.js
window.ADP_CONTENT = {
  "home.lead": {"part": "home.lead", "title": "Lead", "html": "<p>What this page is for.</p>"}
};
```

The tooling parses the object literal after `window.ADP_CONTENT =` as strict JSON: double-quoted keys, no trailing commas, no comments, and a
closing `;`.

## Create, check, publish, seed

```sh
ADP="python3 -I adp.py"
$ADP new minimal DIR --title "Release board" --by NAME
# adapt the look and copy: styles/page.css, parts/*.js, content.js (keep the token names, the markers and the selectors adp.js relies on)
$ADP check DIR                 # markers balance, ids valid and unique, every part has data-part
# publish with the object `new` printed (file_path, root, files, capabilities), plus a label and, the first time, an icon
```

`--by NAME` is recorded as the author of the seeded documents.

- Give each page its own `styles/page.css` and views; keep the structure.
- `adp.py files DIR` emits `batches` instead of `files` above 250 files: publish the page with the first batch, then send the rest to the same URL.
- **Seeding.** The first editor to open the published page writes the record into its database from `seed.json` and `seed/`, so no manual batch
  writes are needed. Until then there are no `parts/<id>` documents to [hold](../adp-minimal-protocol/SKILL.md) and no `manifest/current` to
  record against, so the [edit road](../adp-minimal-roads/SKILL.md) cannot start. Check with an ArtifactData `get` of `manifest/current` first: if
  it exists, write nothing. Only when nobody can open the page as an editor, `adp.py seed DIR --by NAME --batches` prints the same documents as
  batches. Details: [shell and runtime](../adp-minimal-runtime/SKILL.md).
- After publishing, give the user the URL and the next steps.

## What gets served

The artifact service serves a fixed set of extensions (`.html .css .js .mjs .json .geojson .webmanifest .wasm .map .txt .md .csv .xml .svg`,
common images, fonts, audio, video and `.pdf`); a publish that includes any other file is refused. `adp.py files DIR` maps every servable file to
itself and lists the rest under `skipped`. Store templates and other unserved files with a `.txt` suffix.

## The page's own code

The page's script reaches the database through the runtime, not the host: `ADP.ns('shared').doc('board/main')` and `.collection('cards')` give
handles under `ns/shared/`; `ADP.ns('users/<id>')` is per person. A handle has `get()`, `set()`, `update()`, `delete()` and `onSnapshot()`.
`ADP.config.get('look.mode')` reads a [switch](../adp-minimal-runtime/SKILL.md) (a named page setting in `config/current`).

```js
const board = ADP.ns('shared').doc('board/main');
board.onSnapshot(s => render(s.exists ? s.data() : {cards: []}));
await board.update({title: 'Sprint 12'});
```

## Rules

- Part ids never change after publishing; add a new id instead.
- If the catalog already provides a part, take it instead of writing it ([catalog](../adp-minimal-catalog/SKILL.md)).

## The `new` command

`new` copies a template folder into DIR, fills in its title and slug, writes the seed, and prints one publish object. The vectors run it on the
`minimal` template (fixture `template-minimal`, installed as the only template): the output, the file tree the publish names, a tree that passes
`check`, the seed it writes, a page taken from a catalog (themes, layouts, `installed.json`) and the refusals of a non-empty DIR, a bad slug, an unknown theme and
`--tier full`. Part counts and sizes in the `check` and `seed` output depend on that template.

| Command | Prints | Exit |
|---|---|---|
| `templates` | one block per template: name, what it is, `use when:` | 0 |
| `new TEMPLATE DIR [--title T] [--slug S] [--by NAME] [--data FILE\|DIR] [--theme NAME] [--layout ID] [--catalog URL\|-\|catalog.json]` | `{template, dir, title, slug, publish {file_path, root, files, capabilities}, take, design, next}`, plus `catalog` and `entries` when a catalog was taken from | 0; 1 when DIR exists and is not empty, on a bad slug, an unknown theme or `--tier full`; 2 with the `take` error (`index not fetched` and the read to make) when a catalog is given that cannot be taken from |

Its fixtures and vectors are in [vectors.md](vectors.md).
