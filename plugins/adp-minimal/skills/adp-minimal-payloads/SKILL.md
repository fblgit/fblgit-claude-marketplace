---
name: adp-minimal-payloads
description: "The ADP protocol's documents and calls written out as JSON: manifest/current, a pinned hold batch, the publish call, the record batch with manifest/current last, a decision, a data-only change. Use when the user asks what an ArtifactData batch, a changes/ entry, a decision document or the publish arguments of an ADP page look like."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Payload examples

The documents and calls of the protocol ([protocol](../adp-minimal-protocol/SKILL.md): the record and the six steps), written out; `adp.py` prints these for you. The field names are the layout's; the values are
made up. `URL` is the artifact's URL. Every write to an existing document carries `if_version`, the version you read; a refused write means someone
wrote first, so read again.

## 1. Read

An `Artifact` read of the page (the latest version is the only source). Then ArtifactData reads: `get` of `manifest/current`, and `list` of
`parts`, `decisions`, `threads` and `agents`. Keep each document's `version`.

`manifest/current` (adp/2):

```json
{
  "schema": "adp/2", "version": 7, "page_hash": "a1b2c3d4e5f6",
  "parts": {"triage.keys-table": "0f1e2d3c4b5a", "triage.header": "5a4b3c2d1e0f", "_rest:index.html": "9c8d7e6f5a4b"},
  "elements": {"triage.keys-table": 14},
  "files": {"index.html": "77aa88bb99cc", "parts/app.js": "11dd22ee33ff"},
  "part_file": {"triage.keys-table": "parts/app.js"},
  "at": "2026-11-19T10:00:00Z", "by": "agent-a"
}
```

Compute the page's own manifest from the source you just read ([snippets](../adp-minimal-snippets/SKILL.md)). If its `page_hash` differs from `manifest/current.page_hash`,
someone published without recording: record a `changes/` entry for the gap with `by: "unrecorded"`, then continue.

## 2. Hold

One ArtifactData batch, every entry pinned. `hold_until` is at most two hours ahead and only a staleness hint; the pin is the lock.

```json
{ "action": "batch", "url": "URL", "writes": [
  { "op": "update", "collection": "parts", "doc_id": "triage.keys-table", "if_version": 3,
    "data": { "holder": "agent-a", "hold_until": "2026-11-19T12:00:00Z" } },
  { "op": "update", "collection": "agents", "doc_id": "agent-a", "if_version": 5,
    "data": { "holds": ["triage.keys-table"], "last_seen": "2026-11-19T10:05:00Z" } }
] }
```

A document that does not exist yet is written with `set` and no `if_version`.

## 3. Publish

The Artifact tool, to the same URL, with a `label` of at most 60 characters. Pass `file_path` (the page) and `root` (the folder), and in `files`
every other file by its published path:

```json
{ "url": "URL", "file_path": "/work/page/index.html", "root": "/work/page",
  "files": { "parts/app.js": "parts/app.js", "styles/page.css": "styles/page.css" },
  "label": "Keys table: add sort" }
```

## 4. Record

One batch (at most 50 writes; split a larger one and put `manifest/current` last), every existing document pinned. Holders cleared, one new
`changes/` entry, `manifest/current` last.

```json
{ "action": "batch", "url": "URL", "writes": [
  { "op": "update", "collection": "parts", "doc_id": "triage.keys-table", "if_version": 4,
    "data": { "hash": "1234567890ab", "version": 8, "at": "2026-11-19T10:30:00Z", "by": "agent-a",
              "summary": "sortable columns", "holder": "", "hold_until": "" } },
  { "op": "set", "collection": "changes", "doc_id": "000008",
    "data": { "version": 8, "at": "2026-11-19T10:30:00Z", "by": "agent-a", "summary": "Keys table: add sort",
              "parts": [ { "id": "triage.keys-table", "from": "0f1e2d3c4b5a", "to": "1234567890ab" } ], "threads": ["t-42"] } },
  { "op": "update", "collection": "threads", "doc_id": "t-42", "if_version": 2,
    "data": { "status": "done", "holder": "", "done_in": 8 } },
  { "op": "update", "collection": "agents", "doc_id": "agent-a", "if_version": 6,
    "data": { "holds": [], "last_seen": "2026-11-19T10:31:00Z" } },
  { "op": "update", "collection": "manifest", "doc_id": "current", "if_version": 7,
    "data": { "version": 8, "page_hash": "ffeeddccbbaa", "at": "2026-11-19T10:30:00Z", "by": "agent-a",
              "parts": { "triage.keys-table": "1234567890ab" } } }
] }
```

`changes/` entries are append-only and zero-padded to six digits. A part added or removed has `from` or `to` equal to `""`.

## 5. A decision

An owner decision is written before acting on it, with the owner's words quoted verbatim:

```json
{ "op": "set", "collection": "decisions", "doc_id": "keep-table-compact",
  "data": { "quote": "Keep the table compact, no row icons.", "source": "comment t-42", "at": "2026-11-19T09:40:00Z",
            "parts": ["triage.keys-table"], "applied": "Removed row icons.", "status": "active" } }
```

## 6. A data-only change

A page's own record (for example `adrs/<id>`) follows the same protocol by document: hold it as `"adrs/<id>"` in `agents/<you>.holds`, write it
pinned, and list it under `data` in that publish's `changes/<seq>`:

```json
{ "version": 9, "at": "2026-11-19T11:00:00Z", "by": "agent-a", "summary": "ADR 12 accepted", "parts": [],
  "data": [ { "doc": "adrs/12", "from": 2, "to": 3 } ] }
```

`from` and `to` are the document's versions; `0` means created and `-1` deleted.
