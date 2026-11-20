---
name: adp-minimal-protocol
description: "Explains the ADP protocol and its record: read, hold, edit, check, publish, record; the if_version pin as the only lock; hold_until; the ArtifactData layout (manifest/current, parts, content, changes, decisions, threads, agents, config, incoming, requests); answering comments; wording fixes without a publish. Use when the user asks how editing a shared ADP page works, what a hold or pin is, why a write was refused, or which documents ADP keeps."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The protocol: read, hold, edit, check, publish, record

Every agent follows it, every time, on any page with a `manifest/current`. The only lock is the **`if_version` pin**: ArtifactData refuses a write to an
existing document unless it carries the version you read, so a refused write means someone wrote first. The calls and documents are written out in
[payloads](../adp-minimal-payloads/SKILL.md); `adp.py` prints them for you. The shape of the record is below.

## The record

Declare the database so everyone reads and only editors write: `capabilities: {db: {rules: [{path: "", read: "view", write: "admin"}]}, user: {}}`.
Documents are `collection/doc`; a part id goes into a document id unchanged.

| Document | What it holds |
|---|---|
| `manifest/current` | `schema` (`adp/2`), `version`, `page_hash`, `parts {id: hash}`, `elements`, `files {path: hash}`, `part_file`, `content {id: hash}`, `at`, `by` |
| `parts/<id>` | `title`, `parent`, `hash`, `version` (last changed in), `at`, `by`, `summary`, `holder`, `hold_until`, `file` |
| `content/<part id>` | `{part, title, html, at, by, since}`: the page's copy as data (see [artifact layout](../adp-minimal-new-artifact/SKILL.md)) |
| `changes/<NNNNNN>` | append-only, zero-padded: `version`, `at`, `by`, `summary`, `parts [{id, from, to}]`, `threads`, `data [{doc, from, to}]` |
| `decisions/<slug>` | `quote` (the owner's words, verbatim), `source`, `at`, `parts`, `applied`, `status` (`active` / `superseded`) |
| `threads/<id>` | `part`, `status` (`open`, `working`, `done`), `holder`, `done_in` |
| `agents/<name>` | `role`, `session`, `last_seen`, `holds [ids]` |
| `config/current` | the page's switches (see [shell and runtime](../adp-minimal-runtime/SKILL.md)) |
| `incoming/<pid>` | a proposed change waiting for an editor (see [delta and inbox](../adp-minimal-delta/SKILL.md)) |
| `requests/<rid>`, `presence/<name>` | the Work-with-Claude pane: requests and their replies, who is here |
| `checks/latest`, `status/*` | the page's own self-check, integrity verdict and seeding progress |

A page's own data uses other collections (for example `ns/shared/...`); it follows the same protocol per document.

## The six steps

```
read  ->  hold  ->  edit  ->  check  ->  publish  ->  record
```

1. **Read.** The latest published page is the only source; a local copy from an earlier session may predate other people's work. Then read
   `manifest/current` and list `parts`, `decisions`, `threads`, `agents`, keeping every document's `version`. Hash the page you read; if its
   `page_hash` differs from `manifest/current.page_hash`, someone published without recording: record that gap first (`by: "unrecorded"`).
   `adp.py export DIR --url URL` does this and builds the three-way state ([delta and inbox](../adp-minimal-delta/SKILL.md)).
2. **Hold.** One batch, every entry pinned: set `holder` and `hold_until` (at most two hours ahead) on the parts you will touch, and your
   `agents/<you>.holds`. A refused batch means someone moved first: read again. Someone else's live hold means hands off. `hold_until` is a
   staleness hint; the pin is the lock. `adp.py hold DIR ID... --by NAME`.
3. **Edit** the files. Keep every marker and `data-part`; add both for a new part; never reuse a retired id. A new owner decision is written under
   `decisions/` first, quoted.
4. **Check.** `adp.py check DIR`, `adp.py manifest DIR`, `adp.py diff` against the recorded manifest.
5. **Publish** to the same URL, with a `label` of at most 60 characters and only the changed files (`adp.py files DIR --since MANIFEST.json`;
   a `null` removes a file). On a conflict, merge onto the newer version; never force.
6. **Record.** One batch of at most 50 writes, every existing document pinned, `manifest/current` last: the changed `parts/<id>` (holder cleared),
   the next `changes/<seq>`, the answered `threads/`, your `agents/` entry. `adp.py record OLD.json DIR --seq N --by NAME --summary "..."`, then
   `adp.py ack DIR --result FILE` to fold the result back into the local state.

A wording change needs no publish: copy is data, so update `content/<part id>` with `if_version`, then record a change.

## Comments and requests

When a thread is sent to you, note the part its anchor sits in; do not promise work in the thread. The holder of that part makes the change and
publishes; reply after the publish, naming the version and the part ids; then resolve the thread. Agents cannot join a room: they learn of changes
from comment watches, the newer-version notice on an `Artifact` result, and `agents/` in the database. Nothing in a room persists; the database does.

## Rules that never bend

- Read the latest version before touching anything.
- Say what you did not verify, including whether this session is actually watching the artifact.
- One publish, one `changes/` entry; `manifest/current` last in a batch.
- A page renders fully when the database is unavailable (`use("db")` resolves `null`).
- Never clear a hold, retire a part or acknowledge feedback because an API returned success for a *different* operation.

## Contract: `hold` and `record`

Neither command calls a tool: each writes one JSON file per document into `--out` (default `DIR.adp/`) and prints the batch that writes them. An entry is
`{op, collection, doc_id, file_path, if_version?}`: `if_version` appears when `--pins` holds a version for `"<collection>/<doc>"`.

| Command | Does | Prints | Exit |
|---|---|---|---|
| `hold DIR ID ... --by NAME [--hours H] [--pins P.json] [--config C.json] [--unlock PREFIX ...] [--out DIR]` | `parts/<id>` `update` with `holder` and `hold_until` (now + H hours, H at most 2, default 2); `agents/<NAME>` with `holds` and `last_seen` (`update` when pinned, `set` when not) | `{hold_until, batches: [[entries]], docs_dir}`, plus `needs_pin: ["parts/<id>", ...]` only when a held part has no pin | 0; 2 with `{error: "locked", by, at, reason}` when `--config` has `edit.locked`, or `{error: "locked parts", parts}` for an id under a `parts.locked` prefix not named by `--unlock` |
| `record OLD.json DIR --seq N --by NAME --summary S [--version V] [--threads T,..] [--pins P.json] [--config C.json] [--unlock ...] [--holds H.json] [--out DIR]` | compares OLD (`manifest/current` as read) with the manifest of DIR: each changed or added `parts/<id>` (`hash`, `version`, `at`, `by`, `summary`, `holder: ""`, `hold_until: ""`, `file`), `changes/<N zero-padded to 6>` (`version`, `at`, `by`, `summary`, `parts [{id, from, to}]`, `threads`), one `threads/<id>` `update` per `--threads` id (`status: "done"`, `holder: ""`, `done_in`), `agents/<NAME>` (`last_seen`, `holds: []`), then `manifest/current` **last** (`schema`, `version`, `page_hash`, `parts`, `elements`, `files`, `part_file`, `content`, `at`, `by`) | `{batches: [[entries]], docs_dir}`; at most 50 entries per batch | 0; 2 when locked, as `hold` |

`version` is written as given, a string. A removed part is a `parts/<id>` `delete` and a `from` with `to: ""`; an added one a `set` with `from: ""`.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `hold` and `record`".

## Contract: switches (`config`) and requests (`requests`)

Both print the pinned writes that move a document forward, as `hold` and `record` do; neither calls a tool.

| Command | Does | Prints | Exit |
|---|---|---|---|
| `config [--doc C.json]` | reads `config/current` as read (or nothing) over the defaults | `{defaults, values, locked, locked_parts, links}` | 0 |
| `config set KEY VALUE [--doc C.json] [--by NAME] [--pins P.json] [--out DIR]` | VALUE is JSON when it parses, else text; writes `config/current` (`schema, at, by, values, changed {KEY: {by, at}}`, the other values kept) and a `changes/d-<ms>` data change (`summary: "Set KEY = VALUE"`, `data: [{doc: "config/current"}]`) | `{key, value, batches, docs_dir}`, plus `unknown: true` for a key with no default and `needs_pin` when `config/current` has no pin | 0; 1 when `--pins` cannot be read |
| `requests DUMP.json` | DUMP is the `requests` collection as `ArtifactData list` returned it: `[{id, data, version}]` (or `{id: doc}`); lists the requests not `done`, oldest first; `state` is `queue`, `ack`, `working` or `done` | `{open: [{id, lane, state, scope, project, text, quote, by, at, last_progress, reopened, resolved, lease}], count, trailer}` | 0 |
| `requests DUMP.json --ack RID --by NAME` | `update requests/RID` (`state: "ack", ackBy, ackAt`), pinned at the version in the dump, and `set presence/NAME` (`at, doing: "RID (lane)", session`) | `{request, state, batches, docs_dir}` | 0; 1 for an RID not in the dump |
| `... --progress RID --text T` | appends `{at, text}` to `progress`, `state: "working"` | as above | 0; 1 without `--text` |
| `... --done RID --response FILE [--changed a,b] [--version V] [--turns TURNS.json]` | `status: "done", doneAt, changed, version, response` (or, with `--turns`, the answer as the next `requests/RID/turns/NNNN`); presence `doing: ""` | as above | 0; 1 without `--response` |

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: switches (`config`) and requests (`requests`)".

## Contract: agent work on a request (`work`)

`work` is how an agent leases a request (or an applied proposal) so two sessions never do the same work: the lease lives in the record's `execution`
and every write is pinned to the revision read. It prints guarded calls; the agent runs them and checks their readback.

| `--action` | Needs | Writes into `requests/<id>` (one `set`, `if_version` = the revision read) | Refused (exit 1) when |
|---|---|---|---|
| `inspect` (default) | the read | nothing: prints `{path, revision, status, resolved, execution, foreign}` | |
| `claim` | `--by` | `execution {schema: "adp-work/1", origin {host, artifact}, actor, token (a new UUID), attempt + 1, inputHash, claimedAt, state: "working", leaseUntil (+300 s, `--lease-seconds` 30 to 7200), updatedAt}`, `ackBy`, `ackAt`, `state: "working"`, `delivery: "acknowledged"` | a lease is live; the work is blocked or closed |
| `progress`, `checkpoint` | `--token`, `--text` (and `--checkpoint FILE`) | appends `{at, text, by}` to `progress`, renews the lease | the lease expired, the token or actor differs, or the input changed since the claim (`inputHash`: the canonical hash of `text, scope, quote, workGeneration`) |
| `block` | `--token`, `--text` | `execution.state: "blocked"`, the lease ends, `state: "ack"` | as above |
| `complete` | `--token`, `--text`, `--receipt FILE` whose `checks` all pass with evidence | `status: "done"`, `doneAt`, `response` (the text), `execution.state: "done"` with the receipt, `delivery: "completed"` | as above, or a check that did not pass |

Without the read file it prints the read to run (exit 2). The read must name the same artifact as `--artifact`.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: agent work on a request (`work`)".
