> Copy of [`plugins/artifacts-done-properly/skills/adp/catalog/kit/guides/artifact-dataplane.md`](https://github.com/fblgit/artifacts-done-properly/blob/main/plugins/artifacts-done-properly/skills/adp/catalog/kit/guides/artifact-dataplane.md) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.
> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository
> (https://github.com/fblgit/artifacts-done-properly); `snippets.md` shows how to do the same by hand.

<!--
Artifact dataplane (ADP)
The standard for an artifact more than one agent works on: part ids, per-part hashes, comment anchors that are part ids, the ArtifactData layout, the read, hold, publish, record protocol, and the adp/2 layout. Read it before building, editing or publishing such an artifact. This catalog follows it.

Provides (no global): the protocol.

@id        guide.artifact-dataplane
@kind      guide
@group     Guides
@status    stable
@version   0.1.1
@updated   2026-11-13
@summary   The standard every shared artifact follows: part ids, hashes, the db layout, the read, hold, publish, record protocol, and the adp/2 layout.
@tags      adp, standard, protocol, guide, db, hashes, parts, adp/2
@requires  none
@files     none
@provides  none
@tokens    none
@globals   none
@db        none
@source    ADP | the artifact dataplane standard | reduced to the standard itself
@preview   {"render": "guide", "samples": ["kit/guides/artifact-dataplane.md"]}
@changed   Copied byte for byte from SKILL.md at commit f1098e86 (before: c2f889b8). That commit adds reveal(id, key) for keyed anchors and records the page’s own data by doc under changes/<seq>.data.
-->

# Artifact dataplane (adp/1, adp/2)

A shared artifact is edited by several agents and sessions over many versions. Without a standard, a stale copy overwrites other versions, comment replies promise work nobody does, and comment anchors that are CSS paths drift whenever the layout changes.

The dataplane fixes that with four things: **stable part ids** in the source, **per-part hashes** that say what changed, **anchors that are part ids**, and **one ArtifactData layout** written under a version-pinned protocol.

adp/1 is the protocol on a single `index.html`. adp/2 (section 7) is the multi-file, data-first layout on the same protocol. **New artifacts start on adp/2.**

## 1. Parts: stable ids in the source

Every addressable piece of the page is a **part**.

- **Id.** Dot-separated lowercase kebab: `<view>.<section>[.<piece>]`, for example `home`, `triage.keys-table`. An id never changes once published. Retire it and add a new one.
- **Source markers** around each part, in the comment syntax the spot allows. Parts may nest and markers must balance:
  `<!-- part:triage.keys-table -->` ... `<!-- /part:triage.keys-table -->`, or `/* part:triage.keys-table */` ... `/* /part:triage.keys-table */`
- **DOM.** The root element a part renders carries `data-part="<id>" data-comment-target` and a heading (or `aria-label`) inside it. `data-part` is for tools (`check`, the page self-check). `data-comment-target` is what the comment shell honours: a comment-mode click anywhere inside the element anchors to that element. Mark chrome nobody should comment on with `data-uncommentable`.
- **Styles and shared code are parts too.** Mark each style block and shared script as a part (`page.style`, `page.style.<area>`, `page.script`), so a restyle names what it touched. They render no element and need no `data-part`; `check` exempts those two prefixes.
- **`_rest`.** Everything outside every part hashes as the pseudo-part `_rest`. A change there still changes `page_hash` but the diff cannot say where. Keep `_rest` to the page skeleton (a few percent); `check` reports its size.

## 2. Hashes: what changed

`adp.py` (stdlib Python, run with `python3 -I`) computes:

- **Part hash**: sha256 of the part's source between its markers, whitespace runs collapsed, first 12 hex. A parent's hash covers its children, so a change shows on the part and on every ancestor. The diff reports the deepest changed parts.
- **page_hash**: sha256 of the sorted `id=hash` lines, plus the hash of each supporting file.
- **Element counts**: per part, the opening tags in its own text (children excluded), so a diff can tell a new piece from an edit.

```
python3 -I adp.py check      page.html     # balanced markers, valid unique ids, data-part per part, no unmarked data-part, size of _rest
python3 -I adp.py manifest   page.html > manifest.json
python3 -I adp.py diff       old-manifest.json new-manifest.json   # added / removed / changed, deepest, own elements +/-
python3 -I adp.py diff-pages old.html new.html                     # the same, plus the changed lines in each deepest part
```

| change | shows as |
|---|---|
| new piece with its own markers | `added: [id]` |
| new unmarked piece inside a part | that part in `deepest`, `elements: {id: "+1"}` |
| new unmarked piece outside every part | `_rest` in `deepest`, `elements: {_rest: "+1"}` |
| text or style edit, no new element | the part in `deepest`, no `elements` entry |
| `data-part="x"` with no markers | `check` fails |

An unmarked new piece is legal but a smell: mark it before publishing. Put the `deepest` and `elements` of `diff-pages` into the `changes/` summary.

## 3. The ArtifactData layout

Declare `db` with read for all and writes for admins only: `capabilities: {db: {rules: [{path: "", read: "view", write: "admin"}]}, user: {}}`. Add `{path: "ns/users/{self}", write: "interact"}` only if the page keeps per-viewer state. Docs are `collection/doc`; part ids go into doc ids unchanged.

Every doc read returns its `version` and `updatedAt`. ArtifactData refuses a write to an existing doc that does not carry `if_version` (the version you read). That pin is the concurrency control: a refused write means someone wrote first.

| doc | fields |
|---|---|
| `manifest/current` | `schema` (`adp/1` or `adp/2`), `version`, `page_hash`, `parts: {id: hash}`, `elements: {id: count}`, `files: {path: hash}`, `at`, `by` |
| `parts/<id>` | `title`, `parent`, `hash`, `version` (last changed in), `at`, `by`, `summary`, `holder`, `hold_until` |
| `changes/<NNNNNN>` | append-only, zero-padded: `version`, `at`, `by`, `summary`, `parts: [{id, from, to}]` (hash `""` = added or removed), `threads: [ids answered]`, `data: [{doc, from, to}]` |
| `decisions/<slug>` | `quote` (the owner's words, verbatim), `source`, `at`, `parts`, `applied` (how it was implemented, never presented as the owner's words), `status` (`active` or `superseded`), `superseded_by` |
| `threads/<thread id>` | `part`, `status` (`open`, `working`, `done`), `holder`, `done_in`, `note` |
| `agents/<name>` | `role`, `session`, `last_seen`, `holds: [ids]` |
| `content/<part id>` | adp/2: `{part, title, html, at, by, since}` |
| `checks/latest` | adp/2: the page's self-check (section 7) |

Nothing else goes in these collections. A page that needs data of its own uses other collections.

**The page's own data** (records such as `adrs/<id>`) follows the same protocol by doc: hold it as `"<collection>/<doc>"` in `agents/<you>.holds`, write it pinned, and list it under `data` in that publish's `changes/<seq>` (`from` and `to` are the doc's versions; `0` = created, `-1` = deleted). A data-only change is a `changes/` entry with `parts: []`.

Do not let one-doc-per-event grow without bound: roll old `changes/` entries into `changes/archive-<n>` once there are a few hundred.

## 4. Protocol (every agent, every time)

1. **Read.** `Artifact` read (the latest version is the only source, never a local copy from an earlier session), then ArtifactData get `manifest/current` and list `parts`, `decisions`, `threads`, `agents`. Keep each doc's `version`. Run `adp.py manifest` on the source you just read. If its `page_hash` differs from `manifest/current.page_hash`, someone published without recording: diff, record a `changes/` entry for the gap (`by: "unrecorded"`), then continue.
2. **Hold.** One batch, every entry pinned with `if_version`: set `holder` and `hold_until` (at most 2 h) on the parts you will touch, and `agents/<you>.holds`. A refused batch means someone moved first: read again. Someone else's live hold means hands off. `hold_until` is a staleness hint; the pin is the lock.
3. **Edit.** Keep every marker and `data-part`; add both for any new part; never reuse a retired id. Read the active `decisions/` before acting on an owner decision. A new owner decision is written there first, quoted.
4. **Before publishing.** `adp.py check` passes, then `adp.py manifest` and `adp.py diff` against `manifest/current`.
5. **Publish** to the same URL with a `label` (at most 60 characters, the change in a few words). Then record it in one ArtifactData batch (at most 50 writes; split a larger one and put `manifest/current` last), every existing doc pinned: `manifest/current`; the changed `parts/<id>` (holder cleared); the next `changes/<seq>`; the answered `threads/` entries; `agents/<you>` (holds cleared, `last_seen`).
6. **Comments.** When a thread is sent to Claude, record `threads/<id>` with the part its anchor sits in. Do not promise in the thread. The holder of that part does the work and replies after the publish, naming the version and part ids. Then resolve the thread.
7. **Awareness.** Agents cannot join a `room`. They learn of changes from the comment watch, the newer-version notice of an `Artifact` result, and `agents/` in the db. Nothing in a room persists: the db is the record.

## 5. On the page

- Render a small **What changed** panel from `changes/` (the latest 10, newest first) and the active `decisions/`. The page must render fully when `use("db")` resolves `null`.
- `preflight.js` at the artifact root (at most 8 KiB, an ES module whose default export is a function) runs against open pages on each publish. Whether it runs was not confirmed: prefer the page self-check in section 7.

## 6. Adopting an existing artifact

**On adp/1.** Markers plus `data-part data-comment-target` on every view and its main sections, then `adp.py check`, then publish with `db` declared, then seed (an adp/1 page has no loader, so write these yourself in ArtifactData batches; an adp/2 page expands its own `seed.json` on the first editor open) `manifest/current`, `parts/*`, `changes/000001` (summary "adp/1 adopted"), `decisions/*` (the owner decisions so far, quoted) and `threads/*` (open threads). Tell the owner in one line.

**Moving to adp/2.**
1. Split the page into files: the shell, `adp.js`, `content.js`, `styles/*`, `parts/*`.
2. Move copy into `content/*`.
3. Declare `comments: {customAnchors: true}` and map the old CSS-path threads in `legacy`.
4. Prove parity: render old and new in a headless browser and compare every element's computed style and box, in every view and state, at the widths and themes in use. Mutate the new build once to show the comparison catches a difference.
5. Publish with a label. Record in pinned batches; retire the old part ids (delete their `parts/` docs and list them as removed in `changes/`).
6. Ask the owner to open the page and enter comment mode once, then read `checks/latest`.

## 7. adp/2: the multi-file layout

adp/1 rebuilds inside one `index.html` what the platform gives per file, per doc and per anchor. adp/2 uses those units.

- **Files as parts.** A thin `index.html` shell (header, What-changed panel, an empty main, script tags), `adp.js` (the runtime), `content.js` (baseline copy), `styles/*.css` and `parts/*.js`, one file per part family. The platform keeps a sha256 per file (`Artifact` read with `path` returns it). A files-publish keeps the files it omits and `null` removes one. `<script src>` and `fetch()` of a sibling file both work.
- **`adp.py` on a directory.** `check DIR`, `manifest DIR` and `diff-pages OLD_DIR NEW_DIR` take the artifact laid out at its published paths. Markers balance within each file, a part's `data-part` root may sit in any file, and each file's leftover text hashes as `_rest:<path>`. The directory must hold **every** published file, images included, or `page_hash` will not match `manifest/current`.
- **Content as data.** Copy lives as `content/<part id>` docs. `content.js` is the same copy as the fallback when `use("db")` is `null`; the db overrides it live with `onSnapshot`. A wording fix is an ArtifactData `str_replace` on `content/<id>` field `html` with `if_version`: no republish, no page read. Copy still inline in a template is not data until it is moved there.
- **Anchors are part ids.** Declare `comments: {customAnchors: true}` in the **full** form (`composer_only` allows only CSS-path anchors). The page hit-tests, then calls `compose(<part id>, el, {label: <part title>})`; reports pin positions with `placed()`; and implements `reveal(id, key)` to switch to the view or modal that holds the part (`key` is the anchor's `data-part-key`, empty when none: open that record, not the one on screen). The thread list reaches the page only while the viewer is in comment mode, so a load-time check sees 0 threads. Old CSS-path threads need a page-side `LEGACY {anchor string: part id}` map; unmatched ones show in `checks/latest.anchors.unknown`.
- **Page self-check.** After load, when `user.canEdit()`, the page writes `checks/latest`: `{build, at, view, width, ok, missing, unmarked, overflow_x, errors, content: {source, db_docs, file_docs}, anchors: {threads, placed, unknown}, locked, config_at, fetch_sibling, views, seeded, integrity}`. `missing` lists the parts the build names that have no `[data-part]` element; `unmarked` lists `[data-part]` elements nobody marked. Read it after every publish once someone has opened the page.
- **The shared runtime** is the catalog's `adp.js` (entry `runtime.adp`). Take it by reference; the shell template is `adp2-shell`. The page contract: a `<meta name="adp:build" content="<n>">` and `window.ADP_CONTENT` (from `content.js`) load before the runtime; the `page.header`, `page.tabs` and `page.changes` parts exist, and the What-changed panel uses the shell's markup (`#wc`, `#wcChanges`, ...). Once the views exist the page calls `ADP.page({view, expected, titles, legacy, all, reveal})`:
  - `view()`: the current view;
  - `expected(view)`: the part ids that view must render;
  - `titles {id: title}`: the anchor labels;
  - `legacy {css anchor: part id}`;
  - `all`: every known part id;
  - `reveal(id, key)`: show the part, and for a keyed anchor the record `key`.

  The runtime provides `ADP.content(id)`, live repaint of `[data-part]` from `content/`, the changes and decisions panel, customAnchors, error capture, and `checks/latest`.

## 8. What has been tested

Tested on claude.ai Artifacts, runtime contract 0.2.90.

- **Exercised:** files as parts with per-file hashes, content as db docs with live repaint, the page self-check, the customAnchors mechanism, and the server-side `files: {artifact}` copy between artifacts.
- **Not exercised:** the live mapping of old CSS-path threads, and page-side `artifact.publish(files)` compare-and-set per file.
- **Untested on other hosts:** `customAnchors`, db `rules`, `if_version` and the server-side `files: {artifact}` copy. Check each before relying on it there.
