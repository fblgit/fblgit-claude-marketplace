---
name: adp-minimal-kit-authoring
description: "Explains how to build an ADP kit entry instead of hand-writing a one-off: look and take first, what makes an entry general (data and options, tokens only, ADP.* not window.claude, accessible, update and destroy), several samples per entry in a bundle, files, markers and header, build and check, publishing by proposal, and versioning. Use when the user wants a reusable widget, layout, chart, pattern or theme, or asks how to add or update a catalog entry."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Authoring kit entries

Reusable UI (a widget, layout, chart, pattern or theme) belongs in the catalog as a **kit entry**, not inline in a page. Write it once, generally
enough that the next page can take it unchanged. Pull entries into a page with `adp.py take`; don't copy kit files by hand.

## Decide

1. **Look first.** `adp.py suggest - --for "what you need"`, `kit list`, `kit show` ([catalog](../adp-minimal-catalog/SKILL.md)). Check before
   writing anything.
2. **Take it** if it fits. A near miss is a reason to extend the entry (a new option, a new sample), not to fork it.
3. **Add it** only when nothing fits and at least one other page could use it. If only this page needs it, edit the page directly (see
   [roads](../adp-minimal-roads/SKILL.md)).

## What makes an entry general

- It takes **data and options**, never a project's schema: `Kit.meter.draw(el, {value, max, label})`, not a "kiln loads bar". A component
  hard-wired to one dataset's types is too tightly coupled: generalise it into props (`rowQuery`, `colQuery`, `linkField`) and let each page map
  its data.
- It draws with **tokens only** and lists them in `@tokens`; it hard-codes no color, family or size.
- It reaches the record, the viewer and the host through `ADP.db`, `ADP.user`, `ADP.agent()`, `ADP.publish()`, `ADP.ask()`; never `window.claude`.
  Its header's `@db` says what it reads and writes.
- It is accessible by construction: ARIA roles, keyboard support, state conveyed in text and not by color alone. Charts state their range in
  words.
- An entry that keeps state or listeners returns a handle, at least `{destroy()}` and `update(patch)` when it can change in place, so a page
  can change and remove it (`Kit.badge.render` returns `{destroy}`). One that only draws, like `Kit.meter.draw`, is simply called again.
- It names its dependencies in `@requires` and its CDN scripts in `@globals`. It uses no other globals.
- Its text, ids and sample data carry **no project names, file paths or real data**.
- Its header describes what the entry does and how to mount it. No TODOs, task status, local paths or changelog prose: origin goes in
  `@source`, the latest change in `@changed`.

## Several samples

Give each entry samples that cover the edge cases, varying in **size and kind**: an empty state, a typical one, a large one, a long label, a
right-to-left or very narrow case, light and dark. Samples live in the folder's sample bundle, a JSON object with one top-level key per sample.
The bundle `kit/samples/viz.json` of the catalog fixture, where `viz.meter` owns the key `meter`:

```json
{
  "meter": {
    "note": "Invented figures.",
    "half": {"value": 5, "max": 10, "label": "Kiln loads"},
    "full": {"value": 10, "max": 10, "label": "Kiln loads"},
    "zero": {"value": 0, "max": 3, "label": "Glaze tests"}
  }
}
```

The entry's `@preview` is a JSON object naming its renderer and its samples as `bundle-path#key`
(`{"render": "viz.meter", "samples": ["kit/samples/viz.json#meter"]}`), and `@samples` lists the keys it owns. The check fails when a named key is missing from its bundle or a bundle key has no owner ([catalog](../adp-minimal-catalog/SKILL.md)).

## Add the entry

1. **Files** under `kit/<folder>/`: the main file (script, or style for a theme) and the style beside it; the folder's sample bundle is
   `kit/samples/<folder>.json` (`kit/samples/kit.json` for the `kit/` root), listed in the entry's own `@files`.
2. **Markers**: wrap the script in `/* part:page.script.kit.<name> */` ... `/* /part:page.script.kit.<name> */` and the style in
   `/* part:page.style.kit.<name> */` ... `/* /part:page.style.kit.<name> */`, the opening marker on the first line, before the header.
   `<name>` follows the folder's existing files: `kit/badge.js` uses `kit.badge`, `kit/viz/meter.js` uses `kit.viz.meter`, and
   `kit/themes/paper.css` uses `page.style.kit.theme.paper`.
3. **The header** in the main file, with the tags of [the catalog's tag table](../adp-minimal-catalog/SKILL.md#the-header): the required ones
   always, `@provides` in a script, `@tokens` when the entry has a style, and the optional ones it needs. See the example at the end of this
   page.
4. **Build and check** with `adp_catalog.py` ([catalog](../adp-minimal-catalog/SKILL.md#the-consistency-checks)):

```sh
CAT="python3 -I adp_catalog.py"
$CAT build CATALOG_DIR     # catalog.json from the headers
$CAT CATALOG_DIR           # every check must pass: sizes, hashes, orphans, headers, samples, runtime copy
```

5. **Publish by proposal**, not over the live catalog. Catalog changes go through the [loop and the inbox](../adp-minimal-delta/SKILL.md):
   `adp.py export CATALOG_DIR --url URL` reads the live catalog, then `adp.py propose CATALOG_DIR --by NAME --summary S` writes the change as one
   proposal whose files are each guarded by an `ifMatch` on their live sha, and an editor previews and applies it from the catalog page. Try
   changes on a scratch artifact first, and never change a catalog others use without the owner's approval.
6. **Use it**: from the page, `adp.py take - <id>`, link, mount ([kit](../adp-minimal-kit/SKILL.md)).

## The header, as code

`adp_catalog.py` reads each entry's header with these fragments; the tag table in [the catalog's header section](../adp-minimal-catalog/SKILL.md#the-header)
is what they enforce. The vectors that run them are in [the catalog's vectors](../adp-minimal-catalog/vectors.md).

The vocabulary: the ids' prefixes and the allowed values, the tags that repeat, the ones every header carries, and the comma lists. `split_ref`
splits a sample reference, `bundle-path#key`, into its path and key.

```python
# ---
# id: authoring.rules
# tool: adp_catalog.py
# section: authoring
# order: 100
# needs: [core.catalog-tool]
# sha: 459346b5c4a6
# ---
KINDS = {'kit', 'layout', 'pattern', 'viz', 'theme', 'runtime', 'template', 'guide'}      # the first word of an @id
KIND = {'component', 'theme', 'template', 'guide'}                                         # @kind
STATUS = {'new', 'stable'}
GLOBALS = {'htm-preact', 'marked', 'dompurify'}      # the CDN scripts the catalog page can add
MANY = ('config', 'source', 'changed')               # these repeat; every other tag once
ALWAYS = ('id', 'kind', 'group', 'status', 'version', 'updated', 'summary', 'tags', 'requires', 'files', 'globals', 'db')
KNOWN = {*ALWAYS, *MANY, 'provides', 'tokens', 'preview', 'fonts', 'extends', 'related', 'optional', 'samples'}
LISTS = ('tags', 'requires', 'provides', 'globals', 'related', 'optional', 'files', 'samples')      # comma lists; `\,` is a comma in an item
ID = re.compile(r'[a-z0-9][a-z0-9-]*\.[a-z0-9][a-z0-9.-]*')
SEMVER = re.compile(r'\d+\.\d+\.\d+')
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
MEMBER = re.compile(r'[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*')
TOKEN = re.compile(r'--[A-Za-z0-9_<>-]+\??')         # a trailing ? marks an optional property
KEY = re.compile(r'[\w.-]+')                         # a sample's key inside its bundle
SUMMARY_MAX = 260


def split_ref(ref):
    """'kit/samples/viz.json#meter' -> ('kit/samples/viz.json', 'meter'); a path with no # is (path, None)."""
    path, sep, key = str(ref).partition('#')
    return (path, key) if sep else (path, None)
```

The header is the first `/** ... */` of a `.js` or `.css` file (and of their `.txt` copies), else the first `<!-- ... -->`; `*\/` inside it reads as
`*/`. Its first line is the name, the first paragraph after it the `about` text, and a line that does not start with `@` at its margin (an indented `@word` too) continues the tag above it.
`parse_header` shapes each tag the way the catalog page does: comma lists, `[signature, what]` pairs for `@config`, `{reads, writes, note}` for
`@db` (`reads a; b / writes c / note text`), `{board, file, what}` for `@source`, and the JSON of `@preview` (`null` when it is not JSON).

```python
# ---
# id: authoring.read
# tool: adp_catalog.py
# section: authoring
# order: 110
# needs: [authoring.rules]
# tests: [catalog-an-indented-at-line-continues-the-tag]
# sha: 232ba5cb329a
# ---
def comment_of(text, path):
    """The header comment of a file; None without one."""
    code = path.endswith(('.js', '.css', '.js.txt', '.css.txt'))
    m = re.search(r'/\*\*(.*?)\*/' if code else r'<!--(.*?)-->', text[:20000], re.S)
    return m.group(1).replace('*\\/', '*/') if m else None


def parse(comment):
    """-> (title, about, [(tag, value)])"""
    title, about, tags, done = '', [], [], False
    for raw in comment.split('\n'):
        line = re.sub(r'^\s*\*? ?', '', raw).rstrip()
        if m := re.match(r'@([A-Za-z]+)\s*(.*)$', line): tags.append([m.group(1), m.group(2).strip()])
        elif tags: tags[-1][1] = (tags[-1][1] + ' ' + line.strip()).strip() if line.strip() else tags[-1][1]
        elif not line.strip(): done = done or bool(about)
        elif not title: title = line.strip()
        elif not done: about.append(line.strip())
    return title, ' '.join(about), [tuple(t) for t in tags]


def split(v, spaces=False):
    """The items of a comma list (or a list of tokens separated by spaces too)."""
    return [x for x in (y.strip() for y in re.split(r'[,\s]+' if spaces else ',', v)) if x]


def blank(v):
    return v is None or str(v).strip().lower() in ('', 'none')


def pieces(v, sep):
    """The trimmed pieces of v between separators; a separator after a backslash is that character."""
    return [x.replace('\\' + sep, sep).strip() for x in re.split(r'(?<!\\)' + re.escape(sep), v)]


def refuse(constant):
    raise ValueError(constant)           # NaN and Infinity are not JSON: the page's JSON.parse refuses them


def shape(raw):
    h = {}
    for k, v in raw.items():
        if k in ('name', 'about'): h[k] = v
        elif k in LISTS: h[k] = [] if blank(v) else [x for x in pieces(v, ',') if x]
        elif k == 'tokens': h[k] = [] if blank(v) else v.split()
        elif k == 'config': h[k] = [[x.replace('\\|', '|').strip() for x in (re.split(r'\s+\|\s+', c, maxsplit=1) + [''])[:2]] for c in v if not blank(c)]
        elif k == 'source': h[k] = [{'board': a[0], 'file': a[1] if a[1:] else '', 'what': ' | '.join(a[2:])} for a in (pieces(s, '|') for s in v if not blank(s))]
        elif k == 'changed': h[k] = [x for x in v if not blank(x)]
        elif k == 'db':
            h[k] = {'reads': [], 'writes': [], 'note': ''}
            notes = []
            for part in [] if blank(v) else re.split(r'\s+/\s+', v):
                m = re.match(r'(reads|writes|note)\s+(.*)$', part.strip(), re.S)
                if m and m.group(1) == 'note': notes.append(m.group(2).strip())
                elif m: h[k][m.group(1)] += [x.strip() for x in m.group(2).split(';') if x.strip()]
                elif part.strip(): h[k].setdefault('unread', []).append(part.strip())
            h[k]['note'] = ' '.join(notes)
        elif k == 'preview' and not blank(v):
            try: h[k] = json.loads(v, parse_constant=refuse)
            except ValueError: h[k] = None
        elif k != 'preview': h[k] = '' if blank(v) else v
    return h


def parse_header(text, path):
    """The header of a file as a dict (tag names, plus name and about); {} when it has none."""
    c = comment_of(text or '', path.replace('\\', '/'))
    if c is None: return {}
    title, about, tags = parse(c)
    raw = {}
    for n, v in tags:
        if n in MANY: raw.setdefault(n, []).append(v)
        else: raw[n] = v
    return shape({**raw, 'name': title, 'about': about}) if title or raw else {}
```

`validate` returns `(rule, message)` for each broken rule of one header. `entry` is the catalog entry the file is the main file of, and `ids` the ids
of the catalog:

```python
# ---
# id: authoring.validate
# tool: adp_catalog.py
# section: authoring
# order: 200
# needs: [authoring.read]
# tests: [catalog-refuses-a-bad-header, catalog-header-rules]
# sha: 972e753e69b2
# ---
def validate(path, comment, entry, ids):
    """[(rule, message)] for one header."""
    title, about, tags = parse(comment)
    out, names, val = [], [n for n, _ in tags], {}
    for n, v in tags:
        if n not in KNOWN: out.append(('unknown-tag', f'@{n} is not a header tag'))
        elif n not in MANY and n in val: out.append(('duplicate-tag', f'@{n} appears twice'))
        else: val.setdefault(n, v)
    if not title: out.append(('title', 'the first line of the comment is the entry name'))
    if not about: out.append(('about', 'a paragraph after the name says what the entry is'))
    need = [*ALWAYS, *(['provides'] * path.endswith('.js')), *(['tokens'] * any(f.get('role') == 'style' for f in entry.get('files', [])))]
    out += [('missing-tag', f'@{n} is required') for n in need if n not in names or not val.get(n)]
    used = lambda n: val.get(n) and val[n] != 'none'
    bad = lambda xs: ', '.join(xs)
    if i := val.get('id'):
        if not ID.fullmatch(i) or i.split('.')[0] not in KINDS: out.append(('id', f'@id {i}: kind.name with kind one of {bad(sorted(KINDS))}'))
        if i != entry['id']: out.append(('id-mismatch', f'@id {i} but catalog.json lists this file under {entry["id"]}'))
    for n, ok, shown, want in (('status', val.get('status') in STATUS, val.get('status'), f'one of {bad(sorted(STATUS))}'),
                               ('version', SEMVER.fullmatch(val.get('version', '')), val.get('version'), 'major.minor.patch'),
                               ('updated', DATE.fullmatch(val.get('updated', '')), val.get('updated'), 'YYYY-MM-DD')):
        if val.get(n) and not ok: out.append((n, f'@{n} {shown}: {want}'))
    if len(val.get('summary', '')) > SUMMARY_MAX: out.append(('summary', f'@summary is {len(val["summary"])} characters, at most {SUMMARY_MAX}'))
    if val.get('kind') and val['kind'] not in KIND: out.append(('kind', f'@kind {val["kind"]}: one of {bad(sorted(KIND))}'))
    if val.get('files'):
        got = [] if val['files'] == 'none' else split(val['files'])
        want = [f['path'] for f in entry.get('files', []) if f['path'] != path]
        if len(got) != len(set(got)) or sorted(got) != sorted(want):
            out.append(('files', f'@files lists {bad(got) or "none"}; catalog.json lists the other files {bad(want) or "none"}'))
    if used('db') and (wrong := [s for s in re.split(r'\s+/\s+', val['db']) if not re.match(r'(reads|writes|note)\s+\S', s.strip())]):
        out.append(('db', f'@db: sections `reads a; b` / `writes c` / `note text`, keywords in lowercase; not: {wrong[0][:40]}'))
    if val.get('preview'):
        try: pv = json.loads(val['preview'])
        except ValueError: out.append(('preview', '@preview is not one line of JSON'))
        else:
            for s in (pv.get('samples') if isinstance(pv, dict) else None) or []:
                p, k = split_ref(s) if isinstance(s, str) else ('', None)
                if not p or (k is not None and not KEY.fullmatch(k)):
                    out.append(('preview', f'@preview samples: a path, or path#key with a key of letters, digits, . _ -; not: {str(s)[:40]}'))
    if val.get('samples') and (len(ss := split(val['samples'])) != len(set(ss)) or not all(KEY.fullmatch(s) for s in ss)):
        out.append(('samples', '@samples: a comma list of bundle keys (letters, digits, . _ -), no repeats'))
    if names.count('changed') > 1: out.append(('changed', '@changed appears once: the newest change'))
    if val.get('tags') and (len(ts := split(val['tags'])) != len(set(ts)) or any(t != t.lower() for t in ts)):
        out.append(('tags', '@tags: a comma list, lowercase, no repeats'))
    for n, fits, msg in (('requires', lambda x: x in ids, '@requires names no catalog entry:'), ('provides', MEMBER.fullmatch, '@provides: dotted names, comma separated; not:'),
                         ('tokens', TOKEN.fullmatch, '@tokens: custom properties like --ink (--ink? when optional); not:'),
                         ('globals', lambda x: x in GLOBALS, f'@globals: none or {bad(sorted(GLOBALS))}; not:')):
        if used(n) and (wrong := [x for x in split(val[n], spaces=n == 'tokens') if not fits(x)]): out.append((n, f'{msg} {bad(wrong)}'))
    for n, v in tags:
        if n == 'config' and ' | ' not in v: out.append(('config', f'@config {v[:40]}: "signature | what it takes"'))
        if n == 'source' and len(re.split(r'\s\|\s', v)) < 3: out.append(('source', f'@source {v[:40]}: "board | file | what"'))
    return out
```

The main file of an entry is the one named by its `main`, else the template or doc, else the first script, else the first style. `check_headers`
validates the header of each main file of the catalog's `catalog.json`, or of the files it is given. A file that is not a main file is `skipped`; a main
file listed but absent, or with no `@id` header, is `legacy`:

```python
# ---
# id: authoring.check
# tool: adp_catalog.py
# section: authoring
# order: 250
# needs: [authoring.validate]
# tests: [catalog-headers-command]
# sha: 01a962e53c26
# ---
def main_file(e):
    """The file that carries an entry's header."""
    if e.get('main'): return e['main']
    for roles in (('template', 'doc'), ('script',), ('style',)):
        for f in e.get('files', []):
            if f.get('role') in roles: return f['path']


def check_headers(root, files=None):
    """-> ([(path, state, [(rule, message)])], {main file: entry}); state is header, legacy or skipped"""
    cat = json.loads(Path(root, 'catalog.json').read_text(encoding='utf-8'))['entries']
    by_path, ids, results = {m: e for e in cat if (m := main_file(e))}, {e['id'] for e in cat}, []
    for p in sorted(by_path) if files is None else files:
        rel = p if files is None else os.path.relpath(os.path.abspath(p), root).replace(os.sep, '/')
        e, f = by_path.get(rel), Path(root, rel)
        if e is None: results.append((rel, 'skipped', []))
        elif not f.is_file(): results.append((rel, 'legacy', [('missing-file', f'catalog.json lists {rel} for {e["id"]} but the file is not there')]))
        elif (c := comment_of(f.read_text(encoding='utf-8'), rel)) is None or '@id' not in c: results.append((rel, 'legacy', [('legacy', 'no @id header')]))
        else: results.append((rel, 'header', validate(rel, c, e, ids)))
    return results, by_path
```

## Changing an entry later

Bump `@version`, fill `@updated`, replace `@changed` with one sentence describing the newest change, run `build` again, then the check. A changed file changes its
`sha256` and the entry `hash`, which is how a page knows its copy is no longer the catalog's. Never change an id: add a new entry, and say in
the old entry's description paragraph (the `about` text under its name) that it is superseded and by which id. `@status` takes only `new` or
`stable`.

## Example: an entry that requires another (`viz.meter`)

The catalog fixture `catalog-a` ([vectors](../adp-minimal-catalog/vectors.md)) is the complete example: every file, header and sample of four
entries. `viz.meter` shows an entry built on another:

```js
/* part:page.script.kit.viz.meter */
/**
 * Meter
 * Kit.meter.draw(el, {value, max, label}) draws a bar that states its value in words, with a badge for the tone it falls in.
 *
 * @id        viz.meter
 * @kind      component
 * @group     Visualizations
 * @status    new
 * @version   0.1.0
 * @updated   2026-11-20
 * @summary   A bar that states its value and range in words, with a status badge.
 * @tags      meter, bar, progress, value
 * @requires  kit.badge
 * @files     kit/viz/meter.css, kit/samples/viz.json
 * @provides  Kit.meter.draw
 * @config    Kit.meter.draw(el, opts) | value, max, label
 * @tokens    --panel --ink --accent --f-ui
 * @globals   none
 * @db        none
 * @preview   {"render": "viz.meter", "samples": ["kit/samples/viz.json#meter"]}
 * @samples   meter
 */
```

What the header promises: `take` brings `kit.badge` first (`@requires`); the page's theme sets the four `@tokens`; the entry touches no
database (`@db none`); the value is stated in text (`Kiln loads: 5 of 10`), not by the bar's length or the badge's color alone.
