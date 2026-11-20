---
name: adp-minimal-snippets
description: "Reference Python for what adp.py computes: part markers, part hashes, the page hash, the diff against the recorded manifest, the next changes/ id and a pinned ArtifactData write. Use when the user wants to see or verify how an ADP hash or diff is computed, or asks for the code behind a rule."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Snippets: reference implementations

Short versions of what the ADP tool (`adp.py`) computes, in Python 3 with the standard library only. They are for reading and for checking a
build; use `adp.py` for real checks. Each snippet starts with a `# snippet: <name>` comment so other documents can refer to it.

The rules they implement are in [parts and hashes](../adp-minimal-parts/SKILL.md) and the [protocol](../adp-minimal-protocol/SKILL.md).

## snippet: markers and part hashes

```python
# snippet: part-hashes
import hashlib
import re

ID = r'[a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)*'
MARK = re.compile(r'(?:<!--|/\*)\s*(/?)part:(' + ID + r')\s*(?:-->|\*/)')


def sha12(text):
    """First 12 hex digits of SHA-256 over the UTF-8 text (adp.py calls this H)."""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def norm(text):
    """Collapse every whitespace run to one space and trim."""
    return re.sub(r'\s+', ' ', text).strip()


def parse(text):
    """Return (parts, problems).

    parts maps each id to (start, end, parent_id); parent_id is '' for a top-level part.
    Parts may nest and must balance within one file.
    """
    stack, parts, bad = [], {}, []
    for m in MARK.finditer(text):
        closing, pid = m.group(1) == '/', m.group(2)
        line = text.count('\n', 0, m.start()) + 1
        if not closing:
            if pid in parts or any(p == pid for p, _ in stack):
                bad.append(f'line {line}: part {pid} opened twice')
            stack.append((pid, m.end()))
        elif not stack or stack[-1][0] != pid:
            bad.append(f'line {line}: /part:{pid} closes {stack[-1][0] if stack else "nothing"}')
        else:
            _, start = stack.pop()
            parts[pid] = (start, m.start(), stack[-1][0] if stack else '')
    bad += [f'part {p} never closed' for p, _ in stack]
    return parts, bad


def own(text, parts, p):
    """Return a part's own text: its region minus its child parts.

    p == '' selects the page root: the whole file minus its top-level parts.
    """
    s, e = (0, len(text)) if p == '' else parts[p][:2]
    out, i = [], s
    for cs, ce in sorted((cs, ce) for cs, ce, par in parts.values() if par == p and s <= cs < e):
        out.append(text[i:cs])
        i = ce
    return MARK.sub('', ''.join(out) + text[i:e])


def part_hashes(text):
    """Return {part_id: hash, '_rest': hash}.

    A parent's hash covers its children's text; '_rest' covers the text outside every part.
    """
    parts, bad = parse(text)
    if bad:
        raise ValueError('; '.join(bad))
    hashes = {p: sha12(norm(text[s:e])) for p, (s, e, _) in parts.items()}
    hashes['_rest'] = sha12(norm(own(text, parts, '')))
    return hashes
```

## snippet: page hash

```python
# snippet: page-hash   (needs part-hashes above)
def file_hash(path):
    """First 12 hex digits of SHA-256 over the file's bytes."""
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def page_hash(parts, files):
    """parts: {part_id: hash}; in a folder page, each file's '_rest' is keyed '_rest:<path>'.

    files: {relative_path: file_hash}; empty for a single-file page.
    """
    lines = sorted(f'{p}={v}' for p, v in parts.items()) + sorted(f'file:{n}={v}' for n, v in files.items())
    return sha12('\n'.join(lines))
```

A single-file page (schema adp/1) has an empty `files` map. For a folder page (schema adp/2), hash every file except dotfiles, the root
`seed.json` and `seed/`; parse the `.html`, `.js`, `.mjs` and `.css` files that contain markers, and key each file's `_rest` as `_rest:<path>`.
Part ids must be unique across the folder.

## snippet: compare with the recorded manifest

```python
# snippet: diff-manifest
def diff(recorded, current):
    """Return (added, removed, changed) part ids.

    recorded: the parts map of manifest/current; current: the output of part_hashes().
    """
    added = sorted(set(current) - set(recorded))
    removed = sorted(set(recorded) - set(current))
    changed = sorted(p for p in set(current) & set(recorded) if current[p] != recorded[p])
    return added, removed, changed
```

If the part diff is empty but the page hash differs, a file without parts was added, removed or changed (an asset, or a file with no markers).
Compare the `files` maps.

## snippet: the next changes/ id

```python
# snippet: next-change
def next_change(existing_ids):
    """Return the next changes/ id: the highest numeric id + 1, zero-padded to six digits. changes/ is append-only."""
    return '%06d' % (max((int(i) for i in existing_ids if i.isdigit()), default=0) + 1)
```

## snippet: a pinned write

A pin is the `if_version` precondition on a write; see the [protocol](../adp-minimal-protocol/SKILL.md).

```python
# snippet: pinned-write
def pinned(op, collection, doc_id, data, version=None):
    """Build one ArtifactData batch write.

    For an existing document, pass the version you read as `version`. For a new document, use op 'set' and omit `version`.
    """
    w = {'op': op, 'collection': collection, 'doc_id': doc_id, 'data': data}
    if version is not None:
        w['if_version'] = version
    return w
```

A batch holds at most 50 writes. Split a larger record across batches and put `manifest/current` last: until it is written, its `page_hash`
still names the previous page, so a record that stops partway shows up on the next read as a publish without a record. The shapes are in
[payloads](../adp-minimal-payloads/SKILL.md).

## Putting them together

Typical sequence:

1. Read the page's source files. Call `part_hashes(text)` for each file with markers and, for a folder page, `file_hash(path)` for every file.
2. Key each file's `_rest` as `_rest:<path>`, then call `page_hash(parts, files)`.
3. Call `diff(recorded['parts'], parts)` against `manifest/current.parts` to see what changed, or whether someone published without recording.
4. After the edit, repeat steps 1 to 3 for the new hashes, then build the writes with `pinned(...)` and `next_change(...)` as shown in
   [payloads](../adp-minimal-payloads/SKILL.md).
