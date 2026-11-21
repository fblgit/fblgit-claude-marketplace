---
name: adp-minimal-parts
description: "Explains ADP parts and hashes, with the code that computes them: part markers (<!-- part:id -->, /* part:id */), the part id grammar, data-part and data-comment-target, nesting, the _rest bucket, the part hash and page hash rule, adp.py check, manifest, diff and diff-pages, and comment anchors that are part ids. Use when the user asks what a part is, how to mark one, why a hash changed, what deepest or elements mean in a diff, or how comments stay anchored."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Parts and hashes

Kit entries, comments, recorded changes, requests and merges all reference part ids.

A **part** is a region of the page with a stable id. Part hashes identify which parts changed.

The code blocks with a header are the fragments of `adp.py` this skill owns; [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) assembles
them. Their vectors are in [vectors.md](vectors.md).

## Markers

A part is the text between two comment markers, written in the comment syntax of the enclosing language (HTML, or CSS/JS):

```html
<!-- part:triage.keys-table -->
<section data-part="triage.keys-table" data-comment-target>
  <h2>Keys</h2> ...
</section>
<!-- /part:triage.keys-table -->
```

```css
/* part:page.style.table */  .keys { ... }  /* /part:page.style.table */
```

```js
/* part:page.script.sort */  function sortKeys() { ... }  /* /part:page.script.sort */
```

- **Id**: dot-separated segments, each `[a-z0-9][a-z0-9-]*` (`home`, `triage.keys-table`). Unique across the files of a page.
  Ids are immutable once published. To rename a part, remove it and add a part with a new id. Comment threads on the old id are kept
  but no longer placed on the page; to carry them over, map the old id to the new one in the `legacy` map (see Anchors).
- **Nesting**: parts may nest; markers must balance inside one file.
- **`data-part`**: the root element a part renders carries `data-part="<id>"`, and `data-comment-target` if people may comment on it. Mark chrome
  nobody should comment on with `data-uncommentable`. Style and script parts render no element, so they need no `data-part`.
- **`_rest`**: whatever sits outside every top-level part (the page skeleton). A change there still changes the page hash, but a diff cannot say
  where. Keep it small.

The grammar, as patterns. `ROOT` finds an element that carries `data-part`, and `TAG` an opening tag:

```python
# ---
# id: parts.markers
# tool: adp.py
# section: parts
# order: 100
# needs: [core.cli]
# sha: 315d6f9744ca
# ---
ID = r'[a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)*'
MARK = re.compile(r'(?:<!--|/\*)\s*(/?)part:(' + ID + r')\s*(?:-->|\*/)')
ROOT = re.compile(r'<[^<>]*data-part="(' + ID + r')"[^<>]*>')
TAG = re.compile(r'<[A-Za-z][A-Za-z0-9-]*')
REST = '_rest'
TEXT = ('.html', '.js', '.mjs', '.css')        # the files that may hold markers
```

A stack pairs each opening marker with its closing one. A part's region runs from the end of its opening marker to the start of its closing
marker, and its parent is the part open around it:

```python
# ---
# id: parts.parse
# tool: adp.py
# section: parts
# order: 110
# needs: [parts.markers]
# sha: c7d09fe1a5f6
# ---
def parse(text):
    """-> ({id: (start, end, parent id or '')}, problems)"""
    stack, parts, bad = [], {}, []
    for m in MARK.finditer(text):
        close, pid = m.groups()
        line = text.count('\n', 0, m.start()) + 1
        if not close:
            if pid in parts or pid in dict(stack): bad.append(f'line {line}: part {pid} opened twice')
            stack.append((pid, m.end()))
        elif not stack or stack[-1][0] != pid: bad.append(f'line {line}: /part:{pid} closes {stack[-1][0] if stack else "nothing"}')
        else:
            _, start = stack.pop()
            parts[pid] = (start, m.start(), stack[-1][0] if stack else '')
    return parts, bad + [f'part {p} never closed' for p, _ in stack]
```

Three things can be wrong with one file's markers: a part opened twice, a closing marker that does not match the last one opened, and a part
never closed. Across the files of a page, an id may be used once:

```python
# ---
# id: parts.problems
# tool: adp.py
# section: parts
# order: 115
# needs: [parts.parse]
# sha: a693e67acf1a
# ---
def problems(marked):
    """marked {path: text} -> (problems, {id: path})"""
    bad, ids = [], {}
    for f, text in marked.items():
        parts, found = parse(text)
        bad += [(f + ': ' if len(marked) > 1 else '') + p for p in found] + [f'part {p} in {ids[p]} and {f}' for p in parts if p in ids]
        ids.update(dict.fromkeys(parts, f))
    return bad, ids
```

A part's **own text** is its region without its child parts and without any marker. With no part named, it is the file outside every
top-level part, which is `_rest`:

```python
# ---
# id: parts.own
# tool: adp.py
# section: parts
# order: 120
# needs: [parts.parse]
# sha: 4cb02b59e253
# ---
def own(text, parts, p=''):
    s, e = parts[p][:2] if p else (0, len(text))
    out = []
    for cs, ce, parent in sorted(parts.values()):
        if parent == p: out.append(text[s:cs]); s = ce
    return MARK.sub('', ''.join(out) + text[s:e])
```

## Hashes

| Hash | Rule |
|---|---|
| **Part hash** | First 12 hex characters of the SHA-256 of the part's text between its markers (UTF-8), every whitespace run collapsed to one space, trimmed. A parent's text contains its children, so a change shows on the part and on every ancestor. |
| **`_rest`** | The same, over the text outside every top-level part, markers removed. In a folder, each file with markers has its own, named `_rest:<path>`. |
| **Page hash** | The same hash (without whitespace collapsing) over the sorted lines `<id>=<hash>` (every part and `_rest`), followed by the sorted lines `file:<path>=<first 12 hex of the file's SHA-256>`, joined with `\n`, no trailing newline. |

```python
# ---
# id: parts.hash
# tool: adp.py
# section: parts
# order: 130
# needs: [core.cli]
# sha: 686dc523b415
# ---
import hashlib


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def H(data):
    """First 12 hex characters of the SHA-256 of a text (as UTF-8) or of bytes."""
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()[:12]
```

Whitespace is collapsed everywhere in a part, including inside `<pre>` and string literals, so a whitespace-only change there does not change
the hash.

The page runtime (`adp.js`) and `adp.py` must agree on these hashes: on load, the page hashes itself and compares the result with
`manifest/current`. Both collapse `\s+`, but the two regex engines define `\s` differently. Python also matches U+001C to U+001F and U+0085;
JavaScript also matches U+FEFF. Text containing those characters hashes differently in the two, so keep them out of marked text.

## Reading a page

PAGE is one file. DIR is a page laid out at its published paths. In a DIR every file is hashed by its bytes except dotfiles, the root
`seed.json` and `seed/`, and the text files that hold markers (read as UTF-8, bad bytes replaced) are parsed one by one:

```python
# ---
# id: parts.load
# tool: adp.py
# section: parts
# order: 140
# needs: [parts.markers, parts.hash]
# tests: [parts-lenient-inputs]
# sha: a28b012e7747
# ---
def load(path):
    """PAGE or DIR -> (files {path: hash}, marked {path: text}). A PAGE has no files, and its text is under the path ''."""
    if os.path.isfile(path): return {}, {'': Path(path).read_text(encoding='utf-8')}
    files, marked = {}, {}
    for p in sorted(Path(path).rglob('*')):
        rel = p.relative_to(path).as_posix()
        if p.is_dir() or rel == 'seed.json' or rel.startswith(('seed/', '.')) or '/.' in rel: continue
        files[rel] = H(raw := p.read_bytes())
        if rel.endswith(TEXT) and MARK.search(text := raw.decode('utf-8', 'replace')): marked[rel] = text
    return files, marked
```

Every command below works on the page's **regions**: one row per part, and one per file for its `_rest`. A page whose markers are wrong has
no regions: the command stops with the problems on stderr and exit 1.

```python
# ---
# id: parts.regions
# tool: adp.py
# section: parts
# order: 150
# needs: [parts.load, parts.own, parts.problems]
# sha: d95b5bb76abb
# ---
def regions(path):
    """-> (files, [(id, file, text between the markers, own text, parent)])"""
    files, marked = load(path)
    rows, (bad, _) = [], problems(marked)
    if bad: sys.exit('adp check failed:\n  ' + '\n  '.join(bad))
    for f, text in marked.items():
        parts, _ = parse(text)
        rows += [(p, f, text[s:e], own(text, parts, p), parent) for p, (s, e, parent) in parts.items()]
        rest = own(text, parts)
        rows.append((f'{REST}:{f}' if f else REST, f, rest, rest, ''))
    return files, rows
```

## The manifest

`adp.py manifest PAGE|DIR` prints the page's hashes. `manifest/current` in the record is this document. A PAGE has no files of its own;
`--file NAME=PATH ...` names the assets published beside it, so that they count in its page hash. `diff-pages` takes the same option.

| Field | Holds |
|---|---|
| `schema` | `adp/1` for a PAGE, `adp/2` for a DIR |
| `page_hash` | the page hash |
| `parts` | `{id: hash}`, with the `_rest` entries |
| `files` | `{path: hash}`; empty for a PAGE |
| `parents` | `{id: parent id, or ""}` |
| `elements` | `{id: the opening tags in its own text}` |
| `part_file` | `{id: path}`; a DIR only |

```python
# ---
# id: parts.manifest
# tool: adp.py
# section: parts
# order: 160
# needs: [parts.regions, core.io]
# tests: [manifest-dir, manifest-single, check-and-manifest-refusals]
# sha: f5f7d6afb0e7
# ---
def assets(a):
    """The `--file NAME=PATH ...` of a command -> {name: path}"""
    return dict(x.split('=', 1) for x in a[a.index('--file') + 1:]) if '--file' in a else {}


def manifest(path, extra={}):
    files, rows = regions(path)
    files = {**files, **{name: H(Path(p).read_bytes()) for name, p in extra.items()}}
    parts = {p: H(norm(whole)) for p, _, whole, _, _ in rows}
    lines = sorted(f'{p}={h}' for p, h in parts.items()) + sorted(f'file:{f}={h}' for f, h in files.items())
    m = {'schema': 'adp/2' if os.path.isdir(path) else 'adp/1', 'page_hash': H('\n'.join(lines)), 'parts': parts, 'files': files,
         'parents': {p: parent for p, _, _, _, parent in rows}, 'elements': {p: len(TAG.findall(mine)) for p, _, _, mine, _ in rows}}
    if os.path.isdir(path): m['part_file'] = {p: f for p, f, _, _, _ in rows}
    return m


@cmd('manifest')
def manifest_cmd(a):
    """manifest PAGE|DIR [--file NAME=PATH ...]    the page's hashes, as JSON"""
    emit(manifest(a[0], assets(a)))
```

## Checking a page

`adp.py check PAGE|DIR` reports the marker problems above, a part with no `data-part="<id>"` element in the page (ids starting `page.style`
or `page.script` render none and are exempt), and an element whose `data-part` has no markers.

It prints a summary line, then one line per problem, then a warning that lists the part roots nobody can comment on. Exit 1 on a problem.

```text
5 parts in 3 files, ok; 78 chars (17%) outside every part, hashed as _rest
  warning: 1 part roots without data-comment-target: page.header
```

```python
# ---
# id: parts.check
# tool: adp.py
# section: parts
# order: 170
# needs: [parts.regions]
# tests: [check-dir, check-single, check-unclosed, check-opened-twice, check-data-part-without-markers, check-part-without-data-part,
#   check-and-manifest-refusals]
# sha: fdade488c605
# ---
@cmd('check')
def check(a):
    """check PAGE|DIR    the markers balance, and parts and data-part elements match"""
    if not a: print('usage: adp.py ' + check.__doc__.split('\n')[0], file=sys.stderr); return 2
    _, marked = load(a[0])
    bad, ids = problems(marked)
    roots = {m.group(1): m.group(0) for m in ROOT.finditer('\n'.join(marked.values()))}
    bad += [f'part {p}: no data-part="{p}" in the page' for p in ids if p not in roots and not p.startswith(('page.style', 'page.script'))]
    bad += [f'data-part="{p}" has no part:{p} markers (a new piece nobody marked)' for p in sorted(set(roots) - set(ids))]
    rest, size = (sum(len(norm(f(t))) for t in marked.values()) for f in (lambda t: own(t, parse(t)[0]), str))
    print(f'{len(ids)} parts' + (f' in {len(marked)} files' if len(marked) > 1 else '')
          + ('' if bad else f', ok; {rest} chars ({rest / max(size, 1):.0%}) outside every part, hashed as {REST}'))
    for b in bad: print('  ' + b)
    quiet = sorted(p for p, tag in roots.items() if 'data-comment-target' not in tag)
    if quiet: print(f'  warning: {len(quiet)} part roots without data-comment-target: ' + ', '.join(quiet))
    return 1 if bad else 0
```

## Reading a diff

`adp.py diff OLD.json NEW.json` compares two manifests. `adp.py diff-pages OLD NEW` compares two pages or folders and adds the changed lines.
Both report the deepest changed parts first:

| Change | Shows as |
|---|---|
| a new element with its own markers | `added: [id]` |
| a new unmarked element inside a part | that part in `deepest`, `elements: {id: "+1"}` |
| a new unmarked element outside every part | `_rest` in `deepest` |
| a text or style edit | the part in `deepest`, no `elements` entry |
| `data-part="x"` with no markers | `check` fails |

Unmarked elements are allowed but produce coarse diffs; mark them before publishing. The `deepest` and `elements` fields are recorded in the
`changes/` summary.

The fields, from the two manifests' `parts`, `parents`, `elements` and `files` (`parents` of both, the new one winning for an id in both):

- `page_hash`: `[old, new]`.
- `added` and `removed`: the ids only in the new or only in the old manifest, sorted.
- `changed`: the ids in both whose hash differs, sorted by depth (the number of `.` in the id) descending, then by id. An ancestor of a changed
  part has a different hash too, so it is listed after it.
- `deepest`: each changed id that is not the parent of an added, removed or changed id, plus every added and removed id; sorted, without
  repeats.
- `elements`: for each changed id present in both `elements` maps with a different count, the new count minus the old, signed (`"+1"`, `"-2"`).
- `files`: each file of the new manifest whose hash differs, as `[old hash, new hash]`, the old hash `""` for a new file. A removed file is
  not listed.

```python
# ---
# id: parts.diff
# tool: adp.py
# section: parts
# order: 180
# needs: [parts.manifest]
# tests: [diff-manifests]
# sha: f3a7273753d0
# ---
def diff(old, new):
    op, np = old.get('parts', {}), new.get('parts', {})
    oe, ne, of = old.get('elements', {}), new.get('elements', {}), old.get('files', {})
    added, removed = sorted(set(np) - set(op)), sorted(set(op) - set(np))
    changed = sorted((p for p in np if p in op and op[p] != np[p]), key=lambda p: (-p.count('.'), p))
    parents = {**old.get('parents', {}), **new.get('parents', {})}
    inner = {parents.get(p) for p in [*added, *removed, *changed]}
    return {'page_hash': [old.get('page_hash'), new.get('page_hash')], 'added': added, 'removed': removed, 'changed': changed,
            'deepest': sorted({p for p in changed if p not in inner} | {*added, *removed}),
            'elements': {p: f'{ne[p] - oe[p]:+d}' for p in changed if p in oe and p in ne and ne[p] != oe[p]},
            'files': {f: [of.get(f, ''), h] for f, h in new.get('files', {}).items() if of.get(f) != h}}


@cmd('diff')
def diff_cmd(a):
    """diff OLD.json NEW.json    what changed between two manifests"""
    emit(diff(read_json(a[0]), read_json(a[1])))
```

If the part diff is empty but the page hash differs, a file without parts was added, removed or changed: read `files`.

`diff-pages` adds `detail {deepest id: ["-old line", "+new line", ...]}`. A line is a tag or the text between two tags, from the part's own
text, cut at 120 characters; a part shows at most 12 lines, then a count of the rest.

```python
# ---
# id: parts.diff-pages
# tool: adp.py
# section: parts
# order: 190
# needs: [parts.diff]
# tests: [diff-pages-dir]
# sha: dcbaa290cb2c
# ---
import difflib


@cmd('diff-pages')
def diff_pages(a):
    """diff-pages OLD NEW [--file NAME=PATH ...]    diff two pages or folders, with the changed lines of each deepest part"""
    d = diff(manifest(a[0], assets(a)), manifest(a[1], assets(a)))
    old, new = ({p: [t for t in map(norm, re.split(r'(?<=>)|(?=<)', mine)) if t] for p, _, _, mine, _ in regions(x)[1]} for x in a[:2])
    d['detail'] = {}
    for p in d['deepest']:
        lines = [l[:120] for l in difflib.unified_diff(old.get(p, []), new.get(p, []), lineterm='', n=0) if l[0] in '+-'][2:]
        d['detail'][p] = lines[:12] + [f'… {len(lines) - 12} more'] * (len(lines) > 12)
    emit(d)
```

## Anchors

A comment anchors to a part id (or `<part id>:<key>` for one record inside a part, where the key is the element's `data-part-key`). The page asks
the runtime to compose a comment on the nearest `[data-part]` ancestor; the runtime places existing threads on the matching element, and a
`reveal(id, key)` hook opens the view or modal that holds the part. Legacy threads anchored by CSS path are migrated to part ids through a
`legacy` map the page passes to `ADP.page`.
