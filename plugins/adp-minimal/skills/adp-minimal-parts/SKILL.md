---
name: adp-minimal-parts
description: "Explains ADP parts and hashes: part markers (<!-- part:id -->, /* part:id */), the part id grammar, data-part and data-comment-target, nesting, the _rest bucket, the part hash and page hash rule, reading adp.py diff and diff-pages output, and comment anchors that are part ids. Use when the user asks what a part is, how to mark one, why a hash changed, what deepest or elements mean in a diff, or how comments stay anchored."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Parts and hashes

Kit entries, comments, recorded changes, requests and merges all reference part ids.

A **part** is a region of the page with a stable id. Part hashes identify which parts changed.

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

## Hashes

| Hash | Rule |
|---|---|
| **Part hash** | First 12 hex characters of the SHA-256 of the part's text between its markers (UTF-8), every whitespace run collapsed to one space, trimmed. A parent's text contains its children, so a change shows on the part and on every ancestor. |
| **`_rest`** | The same, over the text outside every top-level part, markers removed. In a folder, each file with markers has its own, named `_rest:<path>`. |
| **Page hash** | The same hash (without whitespace collapsing) over the sorted lines `<id>=<hash>` (every part and `_rest`), followed by the sorted lines `file:<path>=<first 12 hex of the file's SHA-256>`, joined with `\n`, no trailing newline. |

Whitespace is collapsed everywhere in a part, including inside `<pre>` and string literals, so a whitespace-only change there does not change
the hash.

The page runtime (`adp.js`) and `adp.py` must agree on these hashes: on load, the page hashes itself and compares the result with
`manifest/current`. Both collapse `\s+`, but the two regex engines define `\s` differently. Python also matches U+001C to U+001F and U+0085;
JavaScript also matches U+FEFF. Text containing those characters hashes differently in the two, so keep them out of marked text.

```python
# the hash rule, for reference; adp.py check / manifest also validate and report
import hashlib, re

def H(s):
    return hashlib.sha256(s.encode()).hexdigest()[:12]

def part_hash(text_between_markers):
    return H(re.sub(r'\s+', ' ', text_between_markers).strip())

def page_hash(part_lines, file_lines):
    return H('\n'.join(sorted(part_lines) + sorted(file_lines)))
```

Complete, runnable versions are in [adp-minimal-snippets](../adp-minimal-snippets/SKILL.md). In practice you run `adp.py check DIR` (markers
balance, ids valid and unique, every part has its `data-part`) and `adp.py manifest DIR` (the hashes, as JSON).

## Reading a diff

`adp.py diff OLD.json NEW.json` (two manifests) and `adp.py diff-pages OLD NEW` (two pages or folders, plus the changed lines) report the deepest changed
parts first:

| Change | Shows as |
|---|---|
| a new element with its own markers | `added: [id]` |
| a new unmarked element inside a part | that part in `deepest`, `elements: {id: "+1"}` |
| a new unmarked element outside every part | `_rest` in `deepest` |
| a text or style edit | the part in `deepest`, no `elements` entry |
| `data-part="x"` with no markers | `check` fails |

Unmarked elements are allowed but produce coarse diffs; mark them before publishing. The `deepest` and `elements` fields are recorded in the
`changes/` summary.

## Anchors

A comment anchors to a part id (or `<part id>:<key>` for one record inside a part, where the key is the element's `data-part-key`). The page asks
the runtime to compose a comment on the nearest `[data-part]` ancestor; the runtime places existing threads on the matching element, and a
`reveal(id, key)` hook opens the view or modal that holds the part. Legacy threads anchored by CSS path are migrated to part ids through a
`legacy` map the page passes to `ADP.page`.

## Contract: `check`, `manifest`, `diff`, `diff-pages`

What a rebuilt `adp.py` must do, checked against the vectors ([adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) has the format and the
runner). PAGE is one file; DIR is a page laid out at its published paths.

**Loading.** A single file is read as text. In a DIR every file is hashed (`file:<path>` = first 12 hex of the SHA-256 of its bytes) except dotfiles, the
root `seed.json` and `seed/`; the text files with markers (`.html .js .mjs .css`) are parsed one by one. Markers must balance within a file, part ids are
unique across the DIR, and each parsed file's text outside its parts is the pseudo-part `_rest:<path>` (a single file: `_rest`).

| Command | Prints | Exit |
|---|---|---|
| `check PAGE\|DIR` | a summary line (`N parts in M files, ok; X chars (P%) outside every part, hashed as _rest`), then warnings indented two spaces (`warning: ... part roots without data-comment-target: ...`); on a problem `N parts` and one problem per line | 0, or 1 on any problem: a marker opened twice, a mismatched close marker, an unclosed marker, a part with no `data-part="<id>"` in the page (ids starting `page.style` or `page.script` exempt), a `data-part` with no markers |
| `manifest PAGE\|DIR` | JSON: `schema` (`adp/1` for a file, `adp/2` for a DIR), `page_hash`, `parts {id: hash}` (with the `_rest` entries), `files {path: hash}`, `parents {id: parent or ""}`, `elements {id: opening tags in its own text}`, and for a DIR `part_file {id: path}` | 0 |
| `diff OLD.json NEW.json` | JSON: `page_hash [old, new]`, `added`, `removed`, `changed` (every changed id, ancestors included), `deepest` (changed ids with no changed descendant), `elements {id: "+n" / "-n"}`, `files {path: [old, new]}` | 0 |
| `diff-pages OLD NEW` | the same as `diff` for two pages or two DIRs, plus `detail {deepest id: ["-old line", "+new line", ...]}` | 0 |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `check`, `manifest`, `diff`, `diff-pages`".
