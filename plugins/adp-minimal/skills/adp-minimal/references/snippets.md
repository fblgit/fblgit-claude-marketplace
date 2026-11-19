# Snippets: the hash arithmetic by hand

These are short, readable examples of what the ADP tool (`adp.py`) computes: Python 3 and its standard library only, nothing downloaded.
They are **suggestions, not a program**: nothing here is wired together or run for you. Taken together they cover the core of working with
ADP (read a page's parts, hash it, compare it with the recorded manifest, build the pinned writes), so Claude can put them together into
a small script when the work needs one, adapt them to the page at hand, or use a single piece alone. Each has a mark, `snippet: <name>`, so it
can be referred to. The full tool, which also diffs, checks and prints the ArtifactData batches, is in the project repository
(https://github.com/fblgit/artifacts-done-properly).

The rules they follow are in [architecture](architecture.md) section 3 and [concepts](concepts.md).

## snippet: markers and part hashes

```python
# snippet: part-hashes
import hashlib, re

ID = r'[a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)*'
MARK = re.compile(r'(?:<!--|/\*)\s*(/?)part:(' + ID + r')\s*(?:-->|\*/)')
H = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]          # first 12 hex of the SHA-256 of the UTF-8 text
norm = lambda s: re.sub(r'\s+', ' ', s).strip()                    # every whitespace run -> one space, trimmed


def parse(text):
    """-> (parts {id: (start, end, parent)}, problems); parts nest and must balance within one file"""
    stack, parts, bad = [], {}, []
    for m in MARK.finditer(text):
        closing, pid = m.group(1) == '/', m.group(2)
        line = text.count('\n', 0, m.start()) + 1
        if not closing:
            if pid in parts or any(p == pid for p, _ in stack): bad.append(f'line {line}: part {pid} opened twice')
            stack.append((pid, m.end()))
        elif not stack or stack[-1][0] != pid:
            bad.append(f'line {line}: /part:{pid} closes {stack[-1][0] if stack else "nothing"}')
        else:
            _, start = stack.pop()
            parts[pid] = (start, m.start(), stack[-1][0] if stack else '')
    bad += [f'part {p} never closed' for p, _ in stack]
    return parts, bad


def own(text, parts, p):
    """A part's own text: its region minus its child parts ('' = the page minus every top-level part)."""
    s, e = (0, len(text)) if p == '' else parts[p][:2]
    out, i = [], s
    for cs, ce in sorted((cs, ce) for cs, ce, par in parts.values() if par == p and s <= cs < e):
        out.append(text[i:cs]); i = ce
    return MARK.sub('', ''.join(out) + text[i:e])


def part_hashes(text):
    """-> {part id: hash, '_rest': hash}; a parent's text includes its children; '_rest' is everything outside every part"""
    parts, bad = parse(text)
    if bad: raise ValueError('; '.join(bad))
    hashes = {p: H(norm(text[s:e])) for p, (s, e, _) in parts.items()}
    hashes['_rest'] = H(norm(own(text, parts, '')))
    return hashes
```

## snippet: page hash

```python
# snippet: page-hash   (needs part-hashes above)
import os

def file_hash(path):
    with open(path, 'rb') as f: return hashlib.sha256(f.read()).hexdigest()[:12]

def page_hash(parts, files):
    """parts {id: hash} (the '_rest' of each file named '_rest:<path>' in a directory), files {relative path: hash}"""
    lines = sorted(f'{p}={h}' for p, h in parts.items()) + sorted(f'file:{n}={h}' for n, h in files.items())
    return H('\n'.join(lines))
```

For a single file (adp/1) `files` is empty. For a folder (adp/2), hash every file except dotfiles, the root `seed.json` and `seed/`; parse the
`.html`, `.js`, `.mjs` and `.css` files that contain markers, and name each file's own `_rest` as `_rest:<path>`. Ids must be unique across the
folder.

## snippet: compare with the recorded manifest

```python
# snippet: diff-manifest
def diff(recorded, current):
    """recorded = manifest/current's parts, current = part_hashes(...): -> (added, removed, changed)"""
    added   = sorted(set(current) - set(recorded))
    removed = sorted(set(recorded) - set(current))
    changed = sorted(p for p in set(current) & set(recorded) if current[p] != recorded[p])
    return added, removed, changed
```

When `changed`, `added` and `removed` are all empty but the page hashes differ, a file changed outside the parts: compare the `files` maps.

## snippet: the next changes/ id

```python
# snippet: next-change
def next_change(existing_ids):
    """changes/ documents are append-only and zero-padded to six digits"""
    return '%06d' % (max((int(i) for i in existing_ids if i.isdigit()), default=0) + 1)
```

## snippet: a pinned write

```python
# snippet: pinned-write
def pinned(op, collection, doc_id, data, version=None):
    """One entry of an ArtifactData batch. An existing document needs the version you read; a new one is written with op 'set' and none."""
    w = {'op': op, 'collection': collection, 'doc_id': doc_id, 'data': data}
    if version is not None: w['if_version'] = version
    return w
```

Batches hold at most 50 writes; put `manifest/current` last. The shapes are in [payloads](payloads.md).

## Putting them together

The usual order, as a sketch (a recipe to follow, not code to run as is):

1. Read the page's source files; call `part_hashes(text)` for each file with markers, and `file_hash(path)` for each file.
2. Name each file's own `_rest` as `_rest:<path>`, then `page_hash(parts, files)`.
3. `diff(recorded['parts'], parts)` against `manifest/current.parts` to see what changed (or whether someone published without recording).
4. After the edit, repeat 1 to 3 to get the new hashes, and build the writes with `pinned(...)` and `next_change(...)` following
   [payloads](payloads.md); at most 50 per batch, `manifest/current` last.

Whatever is assembled from these is unchecked by the ADP tool: say so, and give the user what to verify.
