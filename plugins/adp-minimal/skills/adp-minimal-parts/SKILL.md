---
name: adp-minimal-parts
description: "Explains ADP parts and hashes: part markers (<!-- part:id -->, /* part:id */), the part id grammar, data-part and data-comment-target, nesting, the _rest bucket, the part hash and page hash rule, reading adp.py diff and diff-pages output, and comment anchors that are part ids. Use when the user asks what a part is, how to mark one, why a hash changed, what deepest or elements mean in a diff, or how comments stay anchored."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Parts and hashes

Parts are what the rest of ADP stands on: kit entries, comments, recorded changes, requests and merges all point at part ids.

A **part** is a piece of the page with a stable id. Hashes say what changed. Together they replace "a copy that looks about right" with a check.

## Markers

A part is the text between two comment markers, written in the comment syntax of the spot:

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
  An id never changes once published; retire it and add a new one.
- **Nesting**: parts may nest; markers must balance inside one file.
- **`data-part`**: the root element a part renders carries `data-part="<id>"`, and `data-comment-target` if people may comment on it. Mark chrome
  nobody should comment on with `data-uncommentable`. Style and script parts render no element, so they need no `data-part`.
- **`_rest`**: whatever sits outside every top-level part (the page skeleton). A change there still changes the page hash, but a diff cannot say
  where. Keep it small.

## Hashes

| Hash | Rule |
|---|---|
| **Part hash** | First 12 hex characters of the SHA-256 of the part's text between its markers, every whitespace run collapsed to one space, trimmed. A parent's text contains its children, so a change shows on the part and on every ancestor. |
| **`_rest`** | The same, over the text outside every top-level part, markers removed. In a folder, each file with markers has its own, named `_rest:<path>`. |
| **Page hash** | The same hash over the sorted lines `<id>=<hash>` (every part and `_rest`), followed by the sorted lines `file:<path>=<first 12 hex of the file's SHA-256>`. |

The page runtime (`adp.js`) and `adp.py` compute these identically, because the page hashes itself when it opens and compares with `manifest/current`.

```python
# the whole rule, for reading (adp.py check / manifest do this and more)
import hashlib, re
H    = lambda s: hashlib.sha256(s.encode()).hexdigest()[:12]
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
part_hash = H(norm(text_between_the_markers))
```

[snippets](../adp-minimal-snippets/SKILL.md) has the complete, runnable versions. In practice you run `adp.py check DIR` (markers balance, ids valid and unique, every
part has its `data-part`) and `adp.py manifest DIR` (the hashes, as JSON).

## Reading a diff

`adp.py diff OLD.json NEW.json` (two manifests) and `adp.py diff-pages OLD NEW` (two pages or folders, plus the changed lines) report the deepest changed
parts first:

| Change | Shows as |
|---|---|
| a new piece with its own markers | `added: [id]` |
| a new unmarked piece inside a part | that part in `deepest`, `elements: {id: "+1"}` |
| a new unmarked piece outside every part | `_rest` in `deepest` |
| a text or style edit | the part in `deepest`, no `elements` entry |
| `data-part="x"` with no markers | `check` fails |

An unmarked new piece is legal but a smell: mark it before publishing. The `deepest` and `elements` go into the `changes/` summary.

## Anchors

A comment anchors to a part id (or `<part id>:<key>` for one record inside a part). The page asks the runtime to compose a comment on the nearest
`[data-part]` ancestor; the runtime places existing threads on the matching element, and a `reveal(id, key)` hook opens the view or modal that holds
the part. Old CSS-path threads are mapped to part ids once, in a `legacy` map the page passes to `ADP.page`.

## Contract: `check`, `manifest`, `diff`, `diff-pages`

What a rebuilt `adp.py` must do, pinned by vectors ([adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) has the format and the runner). PAGE is one
file; DIR is a page laid out at its published paths.

**Loading.** A single file is read as text. In a DIR every file is hashed (`file:<path>` = first 12 hex of the SHA-256 of its bytes) except dotfiles, the
root `seed.json` and `seed/`; the text files with markers (`.html .js .mjs .css`) are parsed one by one. Markers must balance within a file, part ids are
unique across the DIR, and each parsed file's text outside its parts is the pseudo-part `_rest:<path>` (a single file: `_rest`).

| Command | Prints | Exit |
|---|---|---|
| `check PAGE\|DIR` | a summary line (`N parts in M files, ok; X chars (P%) outside every part, hashed as _rest`), then warnings indented two spaces (`warning: ... part roots without data-comment-target: ...`); on a problem `N parts` and one problem per line | 0, or 1 on any problem: a marker opened twice, a close that does not match, never closed, a part with no `data-part="<id>"` in the page (ids starting `page.style` or `page.script` exempt), a `data-part` with no markers |
| `manifest PAGE\|DIR` | JSON: `schema` (`adp/1` for a file, `adp/2` for a DIR), `page_hash`, `parts {id: hash}` (with the `_rest` entries), `files {path: hash}`, `parents {id: parent or ""}`, `elements {id: opening tags in its own text}`, and for a DIR `part_file {id: path}` | 0 |
| `diff OLD.json NEW.json` | JSON: `page_hash [old, new]`, `added`, `removed`, `changed` (every changed id, ancestors included), `deepest` (changed ids with no changed descendant), `elements {id: "+n" / "-n"}`, `files {path: [old, new]}` | 0 |
| `diff-pages OLD NEW` | the same as `diff` for two pages or two DIRs, plus `detail {deepest id: ["-old line", "+new line", ...]}` | 0 |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `check`, `manifest`, `diff`, `diff-pages`".
