---
name: adp-minimal-payloads
description: "Example JSON for every ADP protocol write: manifest/current, a pinned hold batch, the publish call, the record batch with manifest/current last, a decision, a data-only change. Use when the user asks what an ArtifactData batch, a changes/ entry, a decision document or the publish arguments of an ADP page look like."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Payload examples

Example payloads for the steps of the [ADP protocol](../adp-minimal-protocol/SKILL.md). Field names and structure are normative; values are
illustrative. `URL` stands for the artifact's URL.

The examples carry each document inline as `data`. `adp.py hold` and `adp.py record` produce the same writes, but put each document in its own
file and pass `file_path` instead; their exact output is fixed by the test vectors in [vectors.md](../adp-minimal-protocol/vectors.md).

**Pins.** Every write to an existing document is *pinned*: it is a conditional write that carries `if_version`, the store's version of that
document as you last read it. ArtifactData refuses a write to an existing document without `if_version`, and refuses a pinned write whose
version is stale. A refusal means another writer got there first: read again and redo the step.

**Two kinds of version.** `if_version` is the store's integer revision of a single document, returned by every ArtifactData read. The `version`
*field* inside `manifest/current`, `parts/<id>` and `changes/<seq>` is the page's published version, stored verbatim as a string. They are
unrelated counters.

## The batch writer

Every command that prints a batch builds it with `Batch`. `put` writes a document's `data` to its own file,
`<collection, "/" as "~">__<doc_id>.json`, under the output folder and adds the entry `{op, collection, doc_id, file_path, if_version?}`: the
agent passes `file_path` to ArtifactData instead of pasting the document. `if_version` comes from the pins, a map of
`"<collection>/<doc_id>"` to the version read. A document the caller already wrote to a file is listed by that file: `put(..., path=FILE)`
writes nothing. An `update`, a `delete`, or a write to a document known to exist (`exists=True`) with no pin
is listed under `needs_pin`: read those documents, add their versions to the pins and run the command again, because the store refuses an
unpinned write to an existing document. `emit` prints the entries in batches of at most 50, with the `manifest` collection last, so
`manifest/current` is always in the last batch, and the folder as `docs_dir`.

```python
# ---
# id: payloads.batch
# tool: adp.py
# section: payloads
# order: 200
# needs: [core.io]
# sha: 17c7e105b1d5
# ---
class Batch:
    """The writes of one step: one file per document under OUT, listed in batches of at most 50 with manifest/current last."""
    def __init__(self, out, pins=None):
        self.out, self.pins, self.writes, self.unpinned = os.path.abspath(out), pins or {}, [], []

    def put(self, op, collection, doc_id, data=None, exists=False, path=None):
        entry = {'op': op, 'collection': collection, 'doc_id': doc_id}
        if path: entry['file_path'] = path
        elif op != 'delete':
            os.makedirs(self.out, exist_ok=True)
            entry['file_path'] = os.path.join(self.out, f"{collection.replace('/', '~')}__{doc_id}.json")
            Path(entry['file_path']).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        key = f'{collection}/{doc_id}'
        if key in self.pins: entry['if_version'] = self.pins[key]
        elif exists or op in ('update', 'delete'): self.unpinned.append(key)
        self.writes.append(entry)

    def emit(self, **extra):
        w = sorted(self.writes, key=lambda e: e['collection'] == 'manifest')
        out = {**extra, 'batches': [w[i:i + 50] for i in range(0, len(w), 50)], 'docs_dir': self.out}
        if self.unpinned: out['needs_pin'] = self.unpinned
        emit(out)
```

## Step 1: Read

Read the page with `Artifact`, always the latest published version, never a local copy from an earlier session. Then, with ArtifactData,
`get` `manifest/current` and `list` `parts`, `decisions`, `threads` and `agents`. Keep each document's store version for the pins below.

`manifest/current` (`adp/2`):

```json
{
  "schema": "adp/2", "version": "7", "page_hash": "a1b2c3d4e5f6",
  "parts": {"triage.keys-table": "0f1e2d3c4b5a", "triage.header": "5a4b3c2d1e0f", "_rest:index.html": "9c8d7e6f5a4b"},
  "elements": {"triage.keys-table": 14, "triage.header": 1, "_rest:index.html": 2},
  "files": {"index.html": "77aa88bb99cc", "parts/app.js": "11dd22ee33ff"},
  "part_file": {"triage.keys-table": "parts/app.js", "triage.header": "index.html", "_rest:index.html": "index.html"},
  "content": {},
  "at": "2026-11-19T10:00:00Z", "by": "agent-a"
}
```

`parts`, `elements` and `part_file` cover every part, including the `_rest:<file>` remainder of each file. `content` maps each
`content/<part id>` document to the hash of its `html`; it is `{}` when the page keeps no copy in the database.

Compute the page's manifest from the source you just read (`adp.py manifest`, [parts](../adp-minimal-parts/SKILL.md)). If its `page_hash` differs from
`manifest/current.page_hash`, someone published without recording. Record a `changes/` entry for the gap with `by: "unrecorded"` before going on.

## Step 2: Hold

One ArtifactData batch, every write pinned. `hold_until` is at most two hours ahead. It is a staleness hint, not a lock: the pin is what
serializes writers.

```json
{ "action": "batch", "url": "URL", "writes": [
  { "op": "update", "collection": "parts", "doc_id": "triage.keys-table", "if_version": 3,
    "data": { "holder": "agent-a", "hold_until": "2026-11-19T12:00:00Z" } },
  { "op": "update", "collection": "agents", "doc_id": "agent-a", "if_version": 5,
    "data": { "holds": ["triage.keys-table"], "last_seen": "2026-11-19T10:05:00Z" } }
] }
```

A document that does not exist yet, such as your first `agents/<you>`, is created with `"set"` and no `if_version`. If another writer creates
it first, your write is refused like a stale pin, because it now targets an existing document without `if_version`.

Steps 3 (edit) and 4 (check) work on local files and write nothing to the store.

## Step 5: Publish

Call the `Artifact` tool on the same URL with a `label` of at most 60 characters. Pass `file_path` (the page), `root` (the folder that holds
it) and, in `files`, only the files that changed since the recorded manifest (`adp.py files DIR --since MANIFEST.json`). A `null` removes a file.

```json
{ "url": "URL", "file_path": "/work/page/index.html", "root": "/work/page",
  "files": { "parts/app.js": "parts/app.js", "parts/legacy.js": null },
  "label": "Keys table: add sort" }
```

On a conflict, merge onto the newer version and publish again; never force.

## Step 6: Record

One batch, every existing document pinned, `manifest/current` last: the changed `parts/<id>`, with your own holds cleared, one new
`changes/<seq>` entry, the answered `threads/`, and your `agents/` entry with its holds cleared.

```json
{ "action": "batch", "url": "URL", "writes": [
  { "op": "update", "collection": "parts", "doc_id": "triage.keys-table", "if_version": 4,
    "data": { "hash": "1234567890ab", "version": "8", "at": "2026-11-19T10:30:00Z", "by": "agent-a",
              "summary": "Keys table: add sort", "holder": "", "hold_until": "", "file": "parts/app.js" } },
  { "op": "set", "collection": "changes", "doc_id": "000008",
    "data": { "version": "8", "at": "2026-11-19T10:30:00Z", "by": "agent-a", "summary": "Keys table: add sort",
              "parts": [ { "id": "triage.keys-table", "from": "0f1e2d3c4b5a", "to": "1234567890ab" } ], "threads": ["t-42"] } },
  { "op": "update", "collection": "threads", "doc_id": "t-42", "if_version": 2,
    "data": { "status": "done", "holder": "", "done_in": "8" } },
  { "op": "update", "collection": "agents", "doc_id": "agent-a", "if_version": 6,
    "data": { "holds": [], "last_seen": "2026-11-19T10:31:00Z" } },
  { "op": "set", "collection": "manifest", "doc_id": "current", "if_version": 7,
    "data": { "schema": "adp/2", "version": "8", "page_hash": "ffeeddccbbaa",
              "parts": { "triage.keys-table": "1234567890ab", "triage.header": "5a4b3c2d1e0f", "_rest:index.html": "9c8d7e6f5a4b" },
              "elements": { "triage.keys-table": 14, "triage.header": 1, "_rest:index.html": 2 },
              "files": { "index.html": "77aa88bb99cc", "parts/app.js": "44ee55ff66aa" },
              "part_file": { "triage.keys-table": "parts/app.js", "triage.header": "index.html", "_rest:index.html": "index.html" },
              "content": {}, "at": "2026-11-19T10:30:00Z", "by": "agent-a" } }
] }
```

- `holder: ""` and `hold_until: ""` mean the part is not held. They appear only on parts you held; a parent that changed only because a child
  changed is updated without them, so another agent's hold on it stays.
- `changes/` entries are append-only. A change that comes with a publish has the six-digit sequence id `record` writes; a data-only change has
  none to take, and uses `d-` followed by the time in milliseconds since the epoch (below).
- An added part is a `"set"` on `parts/<id>` and appears in `changes` with `from: ""`. A removed part is a `delete` and appears with `to: ""`.
- `manifest/current` is replaced whole with a pinned `"set"`, never `update`d: an `update` carrying only the changed parts would replace the
  page's whole `parts` map with them.

A batch holds at most 50 writes. `adp.py record` splits a larger record into several batches and keeps `manifest/current` in the last one.
Each batch is applied all or nothing ([the host's guarantee](../adp-minimal-hosts/SKILL.md#the-record-and-publish-guarantees)), but the batches
are not atomic as a group: if one is refused, none of its writes landed and `manifest/current` has not moved, so re-read and record the remainder.

## Other payloads

### A decision

A new decision from the page owner is written in step 3, before the edit that applies it, with the owner's exact words in `quote`. `applied`
records how it was implemented, in your words, never presented as the owner's.

```json
{ "op": "set", "collection": "decisions", "doc_id": "keep-table-compact",
  "data": { "quote": "Keep the table compact, no row icons.", "source": "comment t-42", "at": "2026-11-19T09:40:00Z",
            "parts": ["triage.keys-table"], "applied": "Removed row icons.", "status": "active" } }
```

### A data-only change

A change to records only, with no publish, is a `changes/d-<ms>` entry with an empty `version` and no part, listing each document it wrote
under `data`. Setting a switch with `adp.py config` writes one in the same batch as the pinned `config/current` update ([vectors](../adp-minimal-protocol/vectors.md),
`config-set-pinned`):

```json
{ "op": "set", "collection": "changes", "doc_id": "d-1763550000000",
  "data": { "version": "", "at": "2026-11-19T11:00:00Z", "by": "agent-a", "summary": "Set edit.locked = true",
            "parts": [], "threads": [], "data": [ { "doc": "config/current" } ] } }
```

Application data documents (for example `adrs/<id>`) follow the same pattern, and no command writes it for you: write each document pinned
with `if_version`, and in the same batch a `changes/d-<ms>` entry whose `data` lists `{doc: "adrs/<id>"}` for each. A `data` item may add
`from` and `to`, the document's store versions before and after the write (`from: 0` for a created document, `to: -1` for a deleted one).
The holds of [the protocol](../adp-minimal-protocol/SKILL.md) are on parts; there is no hold on a data document, so its pin is the only guard.
