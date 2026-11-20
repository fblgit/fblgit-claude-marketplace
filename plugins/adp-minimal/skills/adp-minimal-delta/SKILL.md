---
name: adp-minimal-delta
description: "Explains the ADP delta and inbox: base, live and incoming manifests; the classification into new, ours, theirs, applied, retired and held with its closure; the loop export, classify, propose, ack and the gate hook; local state in DIR.adp/; the incoming/<pid> proposal; Kit.inbox apply and decline. Use when the user asks how ADP merges concurrent work, what held or theirs means, what a proposal is, or why propose or the gate refused."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The delta, the proposal and the inbox

When two parties change the same page, ADP does not pick a winner and does not overwrite. It computes a **delta** from three states and sorts every part
and file into a class.

## The three states

| State | Meaning |
|---|---|
| **base** | the last state both sides agreed on (the last export or applied proposal) |
| **live** | the record and the published page now |
| **incoming** | the side being merged: an agent's local work, or a proposal |

Each is a manifest: `{parts: {id: hash}, files: {path: sha}}`, optionally `parents`, `requires` and, on incoming, `retired {id: reason}`.

## The classification

For each id, with `b`, `l`, `i` the hashes in base, live and incoming (`-` for absent):

| Class | Rule | Meaning |
|---|---|---|
| `new` | b `-`, l `-`, i present | only incoming has it |
| `ours` | i != b, l = b | incoming changed it, live did not |
| `theirs` | i = b, l != b (or b `-`, l present, i `-`) | live changed it, incoming did not |
| `applied` | l = i (or both removed) | both are already at the same state |
| `retired` | b present, i `-`, l present, id in `retired` | incoming deletes it, with a reason |
| `held` | any other combination | both changed it differently, or a deletion without a reason |
| none | b = l = i | unchanged |

Then a **closure**: `new`, `ours` and `retired` become `held` while anything they *touch* is held. Two ids touch when one is the other's parent, or when a
file listed under `requires[component]` meets that component's id or one of its dotted descendants. It repeats until nothing moves. This is what stops
a script from shipping while the part it depends on is in dispute.

```python
def classify(b, l, i, retired=()):           # b, l, i: a hash or None; retired: ids deleted with a reason
    if b == l == i: return 'none'
    if b is None and l is None: return 'new'
    if l == i: return 'applied'
    if i == b: return 'theirs'
    if i is None and b is not None and l is not None:      # incoming deletes what live still has
        return 'retired' if ID in retired else 'held'      # ID: the id being classified; no reason, no deletion
    if l == b: return 'ours'
    return 'held'
```

The same table is in the page runtime as
`ADP.classify(base, live, incoming)` and in `adp.py classify BASE.json LIVE.json INCOMING.json`.

## The loop

```
export (live -> local)  ->  classify  ->  propose (local -> live)  ->  ack  ->  gate
```

| Command | What it does |
|---|---|
| `adp.py export DIR --url URL` | Prints the reads (exit 2), then with the results stores live in `DIR.adp/incoming/`, commits it, classifies base/live/work, and merges live into work when nothing is held. |
| `adp.py classify BASE LIVE INCOMING` | Prints the classification of three manifests. |
| `adp.py propose DIR --by NAME --summary S [--retire ID --reason R]` | Builds an `incoming/<pid>` document and one batch. **Refuses** (exit 2) on a conflict with live, anything held, a deleted part or file without its own `--retire ID --reason R`, or no export. Prints `nothing` when work equals live. |
| `adp.py ack DIR [--result FILE] [--proposal PID]` | Folds a publish or batch result into the state; `--proposal PID` moves base once the page reports it `applied`. |
| `adp.py gate` | A PreToolUse hook decision: **deny** a write while held ids, unacknowledged proposals or pending replies exist, or when a write's `if_version` differs from the state's. Everything else is allowed with a note, so the host's own permission prompt still runs. |

Local state lives in `DIR.adp/` (a sibling folder: `state.json`, `incoming/`, `propose-<pid>.json`, `publish-N.json`, and a nested git repository with
branches `base`, `live`, `work`), in `~/.adp/` (the registry of artifacts, the config, the catalog) and in `<project>/.adp/` (`config.json`,
`log.jsonl`). The merge uses the base the loop names, not the one git would guess.

## A proposal

`incoming/<pid>` records who proposed what, against which base:

```json
{ "by": "agent-a", "at": "2026-11-19T10:00:00Z", "summary": "Keys table: sort",
  "base": {"version": 7, "page_hash": "a1b2c3d4e5f6"},
  "parts": [{"id": "triage.keys-table", "from": "0f1e2d3c4b5a", "to": "1234567890ab"}],
  "files": ["parts/app.js"], "classified": {"ours": ["triage.keys-table"]},
  "status": "new" }
```

A file over 200 KiB travels as `incoming/<pid>/chunks/<n>`. Statuses: `new`, `merged`, `held`, `applied`, `declined`.

## The inbox

`Kit.inbox` (`pattern.inbox`) is the page side. It lists proposals; an editor **applies** one, which publishes its files with an `ifMatch` each through the
`ADP.publish()` handle and records the real version in `changes/`, or **declines** it with a reason. An editor can also wake the agent through the `agent`
handle, only when `canSend()` answers `available`. A catalog itself changes this way: its seed carries kit files as proposals, and its page mounts the
inbox with `autoApply`.

## Reading the result

- `theirs` only: take it, nothing to do.
- `ours` only: propose it.
- `held`: stop. Both sides changed it; the owner (or the holder) decides. Never resolve a hold by overwriting.
- `retired`: a deletion with a reason, recorded in `changes/`.

Related: [protocol](../adp-minimal-protocol/SKILL.md) for holds and pins, [packing](../adp-minimal-packing/SKILL.md) for moving a whole record between hosts.

## Contract: `classify`, in `adp.py` and `adp.js`

`adp.py classify BASE.json LIVE.json INCOMING.json` and `ADP.classify(base, live, incoming)` in the runtime implement the same table and closure
(above). Input: three manifests `{parts: {id: hash}, files: {path: sha}}`, optionally `parents {id: parent}`, `requires {component: [paths]}`, and on
incoming `retired {id: reason}`; a manifest may be wrapped in `data`. Parts and files are classified as one id space.

Output (one line of JSON from `adp.py`, the same object from `adp.js`): `{new, ours, theirs, applied, held, retired}`; each a list of ids except
`held`, a list of `{id, base, live, incoming}` (an absent hash is `null`). Exit 0. **Order differs, on purpose of neither**: `adp.py` lists the part ids
sorted, then the file paths sorted; `adp.js` sorts parts and files as one list. A rebuild keeps each tool's order (the two vectors pin both).

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `classify`, in `adp.py` and `adp.js`".

`same` is unchanged; `mine` is ours; `theirs` is theirs; `both` is held (changed differently); `agree` is applied (both at the same hash); `old` is retired
(deleted with a reason); `dropped` is held (deleted without one); `p.c` is held, and so `p`, its parent, which incoming changed, is held by the closure;
`fresh` is new; `livenew` is theirs; `index.html` is ours.

## Contract: the loop (`export`, `propose`, `ack`, `gate`)

`export` and `propose` keep their state beside the folder, in `DIR.adp/`; the registry of managed urls is `ADP_HOME/artifacts.json`. The nested git
repository (`DIR.adp/repo`, branches `base`, `live`, `work`) is how the tool merges; its commit ids depend on the clock and are never printed.

| Command | Reads | Prints | Exit |
|---|---|---|---|
| `export DIR --url URL` | nothing yet | `{reads: [the Artifact list call, save_to DIR.adp/listing.json], then}` | 2 |
| `export ... --files-listing F` | the listing (JSON, or the list result as text) | `{reads: [the Artifact read of every listed path into DIR.adp/incoming/files, one ArtifactData list per collection], save_docs_to, docs_shape, then}` | 2 |
| `export ... --files-listing F --docs D` | the listing, the files read, the dumped records `{collection: [{id, data, version}]}` | `{report: {new, ours, theirs, applied, held, retired}, merged, state, next}`; the first export is the import (base := live); when nothing is held, live is merged into work and every `theirs` file is copied into DIR | 0 |
| `propose DIR --by NAME --summary S [--retire ID --reason R ...]` | the state and DIR | `{proposal, doc, parts, files, chunks, next, batches, docs_dir}`: one `set incoming/<pid>` (the doc `DIR.adp/propose-<pid>.json`: `by, at, summary, base {version, page_hash, docs}, parts [{id, from, to, html, retired, reason}], files [{path, ifMatch, contentType, content}], live_files, classified, status: "new"`) and one `set changes/d-<ms>` | 0; 2 `{refused: [...]}` on held, a conflict, a deletion without `--retire`; 2 `{error: "no export yet"}` |
| `ack DIR --result FILE` | a batch result `{results: [{collection, doc_id, version}]}` or a publish result `{shas, version}` | `{ack: [the docs or files taken], live, incoming: {held, unacked, pending_replies}}` | 0 |
| `ack DIR --proposal PID` | the proposal's status in the last export | as above, base moved to the proposal's work when `applied` | 1 unless the last export shows it `applied` or `declined` |
| `gate --input HOOK.json` (or stdin) | a PreToolUse hook input | `{hookSpecificOutput}`: `permissionDecision: "deny"` with the reason, or `additionalContext` only (the host's own prompt still runs) | 0 always |

The gate denies a write to a managed url while the inbox holds `held` or `unacked` ids (and `pending_replies`, unless every write answers a request);
and a write whose `if_version` differs from the version the last export read. Reads, other urls and other tools pass with a note.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: the loop (`export`, `propose`, `ack`, `gate`)".
