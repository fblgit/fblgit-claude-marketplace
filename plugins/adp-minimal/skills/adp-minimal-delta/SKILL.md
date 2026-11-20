---
name: adp-minimal-delta
description: "Explains the ADP delta and inbox: the base, live and incoming manifests; classification into new, ours, theirs, applied, retired and held, and the closure over parents and requires; the loop (export, classify, propose, ack) and the gate hook; local state in DIR.adp/; the incoming/<pid> proposal; applying and declining in Kit.inbox. Use when the user asks how ADP merges concurrent work, what held or theirs means, what a proposal is, or why propose or the gate refused."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The delta, the proposal and the inbox

An ADP page can be changed concurrently from the page itself (the inbox) and from agent sessions through `adp.py`. ADP does not let the last
publish win: it compares three states, sorts every part and file into a class, merges what does not conflict and holds the rest.

## The three states

| State | Meaning |
|---|---|
| **base** | the last state both sides agreed on: set to live by the first export and by every export that merges cleanly, and to the proposal's work by `ack --proposal` once the page applied it |
| **live** | the record and the published page, as the last export read them |
| **incoming** | the side being merged: the agent's local folder (**work**, below), or a proposal when the inbox classifies it |

**work** is the local folder `DIR` as committed to the `work` branch of the nested repository in `DIR.adp/repo`. When `adp.py` classifies, work
is the incoming side.

Each state is a manifest: `{parts: {id: hash}, files: {path: hash}}`, optionally with `parents`, `requires` and, on incoming, `retired {id: reason}`.
Every hash is the first 12 hex characters of a SHA-256.

## The classification

For each id, `b`, `l` and `i` are its hashes in base, live and incoming (`-` when absent):

| Class | Rule | Meaning |
|---|---|---|
| `new` | b `-`, l `-`, i present | only incoming has it |
| `ours` | i present, i != b, l = b | incoming changed it; live did not |
| `theirs` | i = b, l != b; or b `-`, l present, i `-` | live changed or added it; incoming did not |
| `applied` | l = i, l != b (including both absent) | live and incoming already agree |
| `retired` | b present, l present, i `-`, id in incoming's `retired` | incoming deletes it and gives a reason |
| `held` | any other change | both sides changed it differently, or incoming deletes it without a reason |
| (none) | b = l = i | unchanged; left out of the output |

Then a **closure**: an id classified `new`, `ours` or `retired` becomes `held` if it touches a held id, repeated until no id changes class. Two ids
touch when one is the other's parent (`parents`), or when one is a file in `requires[c]` and the other is `c` or a descendant `c.*`. `parents` and
`requires` are taken from all three manifests. The closure keeps a file from being proposed while a part it depends on is held.

One id, before the closure:

```python
def classify_id(key, b, l, i, retired):
    """key: the part id or file path; b, l, i: its hash in base, live and incoming, or None when absent; retired: incoming's retired map."""
    if b is None:
        if l is None:
            return 'new' if i is not None else None
        if i is None:
            return 'theirs'
        return 'applied' if i == l else 'held'
    if i is None:
        if l is None:
            return 'applied'
        return 'retired' if key in retired else 'held'
    if l == b:
        return 'ours' if i != b else None
    if i == b:
        return 'theirs'
    return 'applied' if i == l else 'held'
```

## Contract: `classify`, in `adp.py` and `adp.js`

`adp.py classify BASE.json LIVE.json INCOMING.json` and `ADP.classify(base, live, incoming)` in the page runtime (`adp.js`) implement the table and
the closure above.

Input: three manifests `{parts: {id: hash}, files: {path: hash}}`, optionally `parents {id: parent}` and `requires {component: [paths]}`, and on
incoming `retired {id: reason}` (a list of ids is also accepted). `adp.py` also accepts a manifest wrapped in `data`, as an ArtifactData document
stores it. Parts and files share one id space.

Output: `adp.py` prints one line of JSON and exits 0; `adp.js` returns the same object. It is `{new, ours, theirs, applied, held, retired}`, each a
list of ids except `held`, a list of `{id, base, live, incoming}` with `null` for an absent hash.

The order of ids differs between the two. `adp.py` lists part ids sorted, then file paths sorted, in every class except `held`, which it sorts as one
list; `adp.js` sorts parts and files as one list in every class. A reimplementation keeps the order of the tool it replaces; one vector checks each.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `classify`, in `adp.py` and `adp.js`".

## Contract: the loop (`export`, `propose`, `ack`, `gate`)

```
export (live -> local)  ->  classify  ->  propose (local -> live)  ->  ack  ->  gate
```

| Command | Reads | Prints | Exit |
|---|---|---|---|
| `export DIR --url URL [--version V]` with no listing saved | nothing yet | `{reads: [one Artifact list call, save_to DIR.adp/listing.json], then}` | 2 |
| `export ... --files-listing F` (default `DIR.adp/listing.json`) with no records saved | the listing (JSON, or the list result as text) | `{reads, save_docs_to, docs_shape, then}`: an Artifact read of every listed path (except references to other artifacts) into `DIR.adp/incoming/files`, and one ArtifactData list per record collection | 2 |
| `export ... --files-listing F --docs D` (default `DIR.adp/docs.json`) | the listing, the files read, the dumped records `{collection: [{id, data, version}]}` | `{report: {new, ours, theirs, applied, held, retired}, merged, state, next}`; see below | 0 |
| `classify BASE LIVE INCOMING` | three manifests | the classification (see the contract above) | 0 |
| `propose DIR --by NAME --summary S [--retire ID --reason R ...]` | the state and DIR | `{proposal, doc, parts, files, chunks, next, batches, docs_dir}`: the batch sets the chunk documents, `incoming/<pid>`, then `changes/d-<ms>` | 0 |
| `propose`, work equals live | the state and DIR | `{"nothing": "work equals live", "report": {...}}` | 0 |
| `propose`, refused | the state and DIR | `{refused: [...]}`, one entry for each of: a merge conflict with live, held ids, a part or file deleted without `--retire ID --reason R`, a `--retire` without `--reason` | 2 |
| `propose` or `ack` before any export | nothing | `{error: "no export yet", next}` | 2 |
| `ack DIR [--result FILE]` (or the result on stdin) | a batch result `{results: [{collection, doc_id, version}]}` or a publish result `{shas, version}` | `{ack: [the docs or files taken], live, incoming: {held, unacked, pending_replies}}` | 0 |
| `ack DIR --proposal PID` | the proposal's status in the last export | as above; when the status is `applied`, base moves to the proposal's work; when `declined`, base is unchanged and the proposal is closed | 0; 1 (message on stderr) unless the status is `applied` or `declined` |
| `gate [--input HOOK.json]` (or stdin) | a PreToolUse hook input | `{hookSpecificOutput}`: `permissionDecision: "deny"` with `permissionDecisionReason`, or `additionalContext` only | 0 always |

**Exit codes.** 0 is success. 2 means the command stopped and printed, as JSON on stdout, what the caller does next: the reads to run (`export`),
the refusals (`propose`), or `no export yet`. 1 is a usage or input error, with the message on stderr.

**`export`.** The first export is the import: base and work start from live, and an empty or missing `DIR` is filled with the live files. When
nothing is held, live is merged into work with `git merge-tree`, every `theirs` file (and `content/<id>.html`, when `DIR` has `content/`) is
copied into `DIR`, and base moves to live. A git merge conflict adds the conflicting paths to `held` (hashes `null`) and the conflict lines to the
report as `merge_conflict`; `merged` is then `false`. `next` is one of `held: N; show both versions to the owner, nobody writes`,
`adp.py propose DIR --by NAME --summary S`, or `clean: nothing to send`.

**`propose`.** Each deleted part or file needs its own `--retire ID --reason R` pair, matched in order. The proposal id is `p-<ms>-<4 characters>`.
The document `DIR.adp/propose-<pid>.json` holds `by, at, summary, threads, base {version, page_hash, docs}, parts [{id, from, to, html, retired,
reason}], files [{path, ifMatch, contentType, content}], live_files, classified, status: "new", decided, applied`. A file whose content is over
200 KiB (as UTF-8 text, or base64 for a binary file) has no `content`; it is sent as `{path, n, of, content}` documents in the
`incoming/<pid>/chunks` collection, numbered across the whole proposal.

**`gate`.** It denies a write to a managed url (an `Artifact` publish, or an `ArtifactData` call that is not get, list, query or read) while the
state lists `held` or `unacked` ids, or `pending_replies` unless every write in the call targets `requests` or `presence`. It also denies a write
whose `if_version` differs from the version the last export read for that document. In every other case, including other tools, reads, unmanaged
urls and input that is not JSON, it returns no decision, only `additionalContext`, so the host's normal permission flow applies. `unacked` lists the
proposals this folder sent that the last export shows `applied` or `declined` and that `ack --proposal` has not taken; `pending_replies` lists the
`requests` whose status is not `done` and whose state is not `ack`, `seen` or `working`.

**Local state.** The loop keeps its state beside the folder, in `DIR.adp/`: `state.json`, `listing.json`, `docs.json`, `incoming/`,
`propose-<pid>.json`, `publish-N.json` (written by `adp.py files`), and the nested git repository `DIR.adp/repo` with branches `base`, `live`
and `work`. The three-way merge passes the `base` branch as the merge base; it never uses the one git would compute. Commit ids depend on the clock
and are never printed. Outside the folder: `$ADP_HOME` (default `~/.adp`) holds the registry of managed urls (`artifacts.json`), the config and the
catalog; `<project>/.adp/` holds `config.json` and `log.jsonl`.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: the loop (`export`, `propose`, `ack`, `gate`)".

## A proposal

`incoming/<pid>` records who proposed what, against which base:

```json
{ "by": "agent-a", "at": "2026-11-19T10:00:00Z", "summary": "Keys table: sort", "threads": [],
  "base": {"version": "7", "page_hash": "a1b2c3d4e5f6", "docs": {"manifest/current": 7, "parts/triage.keys-table": 3}},
  "parts": [{"id": "triage.keys-table", "from": "0f1e2d3c4b5a", "to": "9c8b7a6f5e4d", "html": "", "retired": false, "reason": ""}],
  "files": [{"path": "parts/app.js", "ifMatch": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df",
             "contentType": "text/javascript", "content": "..."}],
  "live_files": {"parts/app.js": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df"},
  "classified": {"new": [], "ours": ["triage.keys-table", "parts/app.js"], "theirs": [], "applied": [], "held": [], "retired": []},
  "status": "new", "decided": {"by": "", "at": "", "reason": ""}, "applied": {"version": "", "at": ""} }
```

Statuses: `new` (written by `propose`), `merged` (the inbox classified it with nothing held; not yet published), `held` (the inbox found a conflict,
or Apply hit a publish conflict), `applied` (the inbox published it), `declined` (an editor declined it, with a reason).

## The inbox

The inbox is the page side of the loop: `Kit.inbox.mount(root, opts)`, the catalog entry `pattern.inbox`. It lists the open proposals and classifies
each new one with `ADP.classify`. For each held item, a user with edit rights picks Keep live or Take the proposal; Apply stays disabled until every
held item is picked. Apply publishes the proposal's files through the `artifact` handle (default `ADP.publish()`) with an `ifMatch` per file, then
writes `manifest/current`, `parts/<id>`, `content/<id>` and `changes/<seq>` with the resulting version, and sets the proposal `applied`. Decline
asks for a reason and records it.

After a publish conflict, a hold found on open, or a Decline, the inbox notifies the watching agent session through the `agent` handle, only when
`canSend()` returns `available`. A successful Apply sends nothing.

The published catalog ships its own kit files the same way: they are seeded as one proposal per kit folder, and the catalog page mounts the inbox
with `autoApply: true`, which applies every proposal that classifies as `merged`. See [catalog](../adp-minimal-catalog/SKILL.md).

## Reading the result

- `theirs`: when nothing is held, `export` has already merged it and copied it into `DIR`. No action.
- `ours`: run `propose`.
- `held`: stop. Both sides changed it, and a person decides: an editor picks a side in the inbox, or the owner chooses after you show both versions,
  or the part's holder (the session named in its `holder` field; see [protocol](../adp-minimal-protocol/SKILL.md)) settles it. Never resolve a hold
  by overwriting.
- `retired`: a deletion with a reason. `propose` sends it, and Apply records it in `changes/`.

Related: [protocol](../adp-minimal-protocol/SKILL.md) for holds and pins, [packing](../adp-minimal-packing/SKILL.md) for moving a whole record
between hosts.
