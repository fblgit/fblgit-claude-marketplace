> Copy of [`docs/claude-host-adapter.md`](https://github.com/fblgit/artifacts-done-properly/blob/3f0062952f499370f88200d114e954bff82fe841/docs/claude-host-adapter.md) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.
> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository
> (https://github.com/fblgit/artifacts-done-properly); `snippets.md` shows how to do the same by hand. Calls to Claude's own tools (`Artifact`, `ArtifactData`) are examples
> of what a Claude host offers: on another host, use that host's way to read and write the page.

# Claude host adapter (`adp-host/1`)

`plugins/artifacts-done-properly/skills/adp/assets/adapters/claude.js` is an explicit `adp-host/1` provider over the claude.ai
viewer's `window.claude.use('db'|'user'|'comments')`. It does what the runtime's built-in
Claude default does (same capabilities, same `claude` host id, seed files on), so existing
`adp/2` records, part ids, hashes and classification are untouched. The default is
unchanged: pages with no `ADP_HOST` still use the built-in bridge. The adapter is opt-in:

```html
<script src="adapters/claude.js"></script>
<script>window.ADP_HOST = ADPClaudeHost.create();</script>
<script src="adp.js"></script>
```

Without `window.claude` the adapter's `connect()` throws: `ADP.host.status` is `failed`,
not `static`. It never falls back to another host.

## Verified, and how

| Behaviour | Evidence |
| --- | --- |
| Adapter and built-in default give the same `ADP.host` (except `comments`), `ADP.db`, `ADP.ns`, `ADP.user` and `claude.use` calls | `tests/test_host_connection.py` (Node, fake `window.claude`, real `adp.js`) |
| Slow or never-settling `comments` does not hold `connect()` or page startup | same, plus adapter unit test |
| `user`: `canEdit` stays the viewer's own answer (the runtime still requires literal `true`); `id()` falls back to `''` when the page did not declare the `user` capability, so a missing `id()` does not fail the host | adapter unit test, `test_a_claude_user_without_id_still_connects` |
| `agent`, `publish` and `ask` are mapped from `comments.sendToClaude`, `artifact.publish` and `sample`, forward only what the native call takes, and are `null` when the viewer did not grant the capability | adapter contract test |
| Missing `window.claude` fails closed | both |

The rows above run against fakes. Separately, on 2026-11-16 a private disposable page loaded the real
`adp.js` with this adapter in one live claude.ai viewer (owner, editor): `ADP.host` reported
`{id: "claude", status: "connected", records: true, comments: true, seedFiles: true}`, `canEdit` was
`true`, the part was painted from `content/intro`, and it repainted about a second after an agent
(ArtifactData) edit. Not exercised live: whether the comment anchors registered, a reader or logged-out
session with the adapter, and a reload from a fresh tab. A first synthetic seed-pack was moved Claude to OpenAI
Site to Claude by two agents, before any shell existed. Later runs used the shared records
shell (`adp.py bundle`, `import-plan`, `import-ack`; see `docs/adp-export-import.md`) with this repo's
Claude and Sites adapters. Applying is still done by an agent running the printed calls, and no automatic
cross-host sync exists.

Live runs after that, in the owner's browser, on the assistant probe (the built-in default connection, runtime `de7c6796d072`) and the spec page (this adapter, `ADP.host` `claude`, connected, Agent yes, Publish yes, Ask no because that page does not declare `sample`). Each is in the records of those artifacts, not only in the code: a request sent through `ADP.agent()` (one request doc, change logged after the send returned, comment received by the agent); a reply on that request (turn stored, request reopened, comment headed `Reply 1`); `ADP.ask()` (conversation `c-…`, user message `0001`, answer `0002` 12 s later); `ADP.publish()` through the inbox's Apply (new artifact version, the new file listed, proposal `applied`, exactly one change entry); a native work claim with `adp.py work` (claim, reclaim after the lease expired, completion, each a pinned batch read back); the page's own `update` with `null` (key kept as `null`, `workGeneration` bumped); the page hashing its own `adp.js` against the stamp in its info panel (match, 45,066 bytes); and the integrity run's `files_ahead` drift on the script-painted parts. The probe reloaded itself to a newly published version while the owner had it open (seen for the null and runtime-hash self-tests). Not observed live: the agent, publish and ask calls through `adapters/claude.js` as the explicit provider (only the built-in default ran them), a reader or logged-out viewer on the assistant, racing claimants, and the rendered panel and labels beyond one screenshot of an Ask answer.

## Not supported by the contract (gaps, proposals)

The adapter stays inside `adp-host/1` as written. These Claude behaviours cannot be
expressed by it today; the proposals are for the contract owners and are **not** applied.

1. **`artifact.publish`** (files map, `ifMatch`, `null` delete, all-or-nothing, `{version, shas}`,
   `conflict` rejection with paths): **now the optional `publish.files(files, opts)` handle** (`ADP.publish()`), used by
   the inbox Apply. Still Claude-only: the tester template and docs-to-files call `claude.use('artifact')` directly.
   A per-path receipt beyond `{version, shas}` is not in the contract.
2. **Request delivery** (`comments.canSendToClaude`, `sendToClaude`, `anchorFor`): **now the optional `agent` handle**
   (`ADP.agent()`: `label`, `canSend`, `send` → `{threadId, delivery}`, `anchorFor`), used by `Kit.assist` and
   `Kit.inbox`; `sample` is the separate `ask` handle. `claude-lane` still reaches the comments handle through
   `kit/store.js` and stays Claude-only. See `docs/host-adapters.md`.
3. **Late-bound capabilities.** `connect()` must settle but Claude's `comments` can be slow; the runtime
   solves this with an internal field of the built-in default (`commentsReady`). The adapter uses a lazy wrapper, so
   `ADP.host.comments` is `true` even if the viewer later grants none (anchoring then reports
   `not registered: unavailable`). *Proposal:* let `comments` be a promise, or add a settled-later status.
4. **Db profile is narrower than use.** The kit's assist pattern calls `doc.delete()`; the contract profile
   lists only `get/set/update/onSnapshot` plus queries. The live 0.2.96 types also give `doc.collection`,
   `collection.add`, `query.get` and `doc.acquire` (a lease: `{holder, ttlMs, data}` to `{acquired, version,
   expiresAt, holder}`). Nothing in this repo calls `acquire`. *Proposal:* list the exact operations and run
   one conformance suite against the dev shim.
5. **Kit and `window.claude`.** `store.js` (the adp/1 board store), `claude-lane.js`, `tester.js` and the catalog page's `parts/catalog.js` still call `window.claude` directly and are Claude-only by design; they say so. `inbox.js`, `assist.js`, `assist-panel.js`, `request-card.js`, `presence.js` and the assistant template no longer do: they take `ADP.db`, `ADP.user` (with `can(name)`), `ADP.agent()`, `ADP.publish()` and `ADP.ask()`, so with an explicit non-Claude provider and `window.claude` both present they stay on the provider. *Proposal:* move `claude-lane` onto `pattern.assist` and retire it.
6. **No record version token.** Agent writes pin `if_version` per doc and publishes carry an artifact version;
   the contract's receipt says only "native version(s)". *Proposal:* name `source` and `record` tokens.
   Claude has no separate deployment version.
7. **No host attribution.** Records carry `by = user.id` only, so a later session on another host cannot
   tell which host wrote a change. *Proposal:* an additive `host` field (schema decision, not a bug fix).

Three behaviour changes sit in the shared runtime on the existing Claude path, not in this adapter (the third is `user` being wrapped, above):
`canEdit` now requires literal `true` (it accepted any truthy value; the live type is `Promise<boolean>`,
so the strict check matches the contract, though no live call was observed), and `anchors()` starts only
after `db` and `user` resolve (before, in parallel).

## Test interfaces against the live types

Two sources, in decreasing weight. **Observed live** (2026-11-16, one claude.ai viewer, runtime contract
0.2.96, a private disposable probe page with synthetic data; it exercised the viewer's own `window.claude`,
not `adapters/claude.js` itself): and the platform's type definitions for that contract. Differences in
`plugins/artifacts-done-properly/skills/adp/scripts/adp_dev.js` / `adp_dev.py`, the stand-in the tests and `adp.py dev` use:

- Observed, matches: `canEdit()` resolves a boolean; `canSendToClaude()` resolves `available`; `set` resolves
  `undefined`; snapshots carry `data/exists/id/metadata`; `update` merges; a missing doc reads
  `exists: false`; a stale `ifMatch` publish rejects `conflict` with `paths: [{path, expected, actual}]`.
- Observed, still missing from the dev stand-in because the behaviour was not measured, only the names or
  the uncontended shape: the top-level db path methods `get/set/update/delete/query/subscribe/unsubscribe/
  acquire` (the types list only `doc`/`collection`); `comments.create/delete/reply/resolve`;
  `user.profiles/search`; `doc.acquire`, which resolved `{acquired, expiresAt, holder, version}` uncontended
  (contention is unmeasured, so it is not faked).
- Fixed in the stand-in to match what was measured (`plugins/artifacts-done-properly/skills/adp/scripts/adp_dev.*`): a publish conflict's `live` is
  the current version id and it carries `changed: []`; `update` removes a field for a bare
  `{__delete__: true}` and refuses the marker with other keys (`invalid_argument`); `orderBy` puts `null`
  lowest and a missing field last in both directions; `user.isOwner()` and `user.me()` with the live key
  set. Checked by `tests/test_dev.py` (marker, conflict) and a throwaway run of the real shim file for the
  ordering and `user` additions, which is not in the suite.
- Observed, snapshot behaviour a host or fake must tolerate: a local write fires the listener with
  `hasPendingWrites: true`, then an empty-changes snapshot (`fromCache: true`), then a `modified` change for
  the doc it just added, then a settled snapshot; after a reload the first snapshot is `fromCache: true` and may
  hold documents deleted since, which later `removed` changes correct.
  **Stand-in, modelled (query `onSnapshot` only), one case:** a document newly `set` through the stand-in produces
  exactly the five snapshots of **run A**, recorded live on a collection that already held two documents
  (`+existing`, `+new` pending, empty cache echo, `~new` from cache, settled empty), and a reload produces the persisted result first (`fromCache`, stale documents included) and then the
  corrected one with `removed`/`added`. The persisted result is the page's `localStorage`, standing in for the
  viewer's cache, keyed by the artifact: the server sends a store identity (a hash of the folder it serves) with
  the shim, so another artifact on the same localhost origin never sees it; without an identity nothing is kept. `tests/test_dev.py` runs the real shim in Node and asserts both traces.
  **Replayed, not modelled:** the full six-snapshot reload recorded live (stale cache, pending echo, `-stale +added`,
  `-b`, empty, `+b ~a`, which includes another client's churn) is fed to the real `adp.js` content watcher through
  the host contract; the part texts follow it (stale removed, `b` dropped and back). A mutation that ignores
  `removed` fails that check.
  **Recorded later, contradicts the stand-in's flags (spec page, owner's viewer, 2026-11-16):** the same write
  against an **empty** collection (run B) gave four snapshots and `fromCache` false throughout
  (`none` size 0, `+new` pending, `none` pending, `~new` settled, no trailing empty snapshot inside 3 s). The
  trace pressed again straight after (run C) first replayed the earlier probe, already deleted, `fromCache` true,
  then `+new` cache and pending, then `-stale` as a server correction, `none` pending, `~new` settled. The
  stand-in's echo and acknowledgement flags match A only, so for an empty collection it is wrong. Run D, the
  controlled measurement (one document, `keep-1`, written to the collection first, then the trace pressed
  once): `+C-probe` size 1 `fromCache` true, `+new` size 2 cache and pending, `-C-probe +keep-1` size 2 pending
  (not cache), `none` pending, `~new` settled. It **refutes** "a non-empty collection gives cache-flagged echo
  rows": D's collection was not empty and its rows after the correction were all `fromCache` false. What D and
  C share with the earlier reload recording is that the first snapshot of a new listener is the viewer's last
  cached result for the query (it holds documents deleted since and lacks `keep-1`, added since), corrected by
  the server's answer one snapshot later. A's `fromCache` rows 3 and 4 remain unexplained. Four samples, one
  per shape, so none of it is modelled beyond run A and the reload.
  **Not modelled, not measured:** updates, deletes, document-level `onSnapshot` (settled only), concurrent
  writers, the extra pending/echo steps a reload shows around the first write, and query listeners the viewer
  already has open when a write lands. The stand-in's persisted result is not the viewer's cache: it survives
  only as long as the page's `localStorage` does.
  Consumers: `adp.js` is checked as above. The assistant template and the preview kit also apply each
  `docChanges` entry by document id (read, not run against these traces). Nothing shipped reads
  `hasPendingWrites` or `fromCache`; a page that shows a "saving" state from them, or counts notifications per
  write, is not covered by these traces.
- Observed, errors: `db.doc()` with an odd segment count throws synchronously with no `code`; an invalid query
  operator rejects `invalid_argument`. Not observed: the stand-in's `invalid_argument` from publish; the types
  do not list it as a publish code.
- Observed, a second signed-in account the owner shared the artifact with (stated view-only; its level was
  not independently confirmed): `use('db')` resolved, but `use('user')`, `use('comments')` and
  `use('artifact')` resolved `null`, and reads worked. All seven write attempts (set, update, delete, add,
  `acquire`, a nested `ns/` update) rejected `invalid_argument` ("The request was malformed or exceeds a
  limit"); the owner then read the fixtures back unchanged, no new docs. A refusal is therefore
  indistinguishable from a malformed request or a missing document: there is no permission-specific code.
  Not tested: the Contributor level, an unauthenticated session, a lost write response.
- Observed, `doc.update` (browser and ArtifactData agree): nested objects merge recursively
  (`{a:{x:1,y:2}}` + `{a:{y:9,z:3}}` gives `{a:{x:1,y:9,z:3}}`); arrays and scalars replace; an explicit
  `null` is stored as `null`; `{a:{__delete__:true}}` removes `a`; a dotted key such as `'a.x'` is stored as a
  literal key, not a path; updating a missing document rejects `invalid_argument`; `set` drops an `undefined`
  field. `orderBy('n')` also returned a document with no `n`, so a fake must not assume Firestore's exclusion.
- Observed, a reload's first snapshot is `fromCache: true` and can still hold documents deleted since;
  `removed` changes correct it a moment later. `adp.js` handles `removed` for `content/` (line 141); the other
  listeners were not checked.
- Observed, timing: the db capability took 1.3 s to resolve cold and 4 ms warm; `use()` of an unknown name resolved `null` at once.
- The fakes in `tests/test_host_connection.py` are shape stubs (`doc()`/`collection()` entry points and
  canned snapshots), deliberately not behavioural, and do not reproduce the snapshot sequence above.

## Claude-only handles in shared code

`db` and `user` reach the kit through `ADP.db` and `ADP.user`, so an explicit host (Sites included) is honoured.
Claude's `artifact.publish`, `comments.sendToClaude` / `canSendToClaude` / `anchorFor` and `sample` reach shared
code as the host-neutral `agent`, `publish` and `ask` handles (`ADP.agent()`, `ADP.publish()`, `ADP.ask()`; see
`docs/host-adapters.md`): `Kit.assist`, `Kit.inbox` and the assistant template use them, and the Claude adapter and
built-in default are the only places those Claude names are mapped. `ADP.claude(name)` stays for pages that already
call it: it waits for the connection and calls `window.claude.use(name)` **only when the connected host's id is
`claude`**; on any other host it resolves `null` without touching `window.claude`. On a
non-Claude host without a publish handle the inbox disables Apply and says "Apply publishes this page's files, which only a Claude host can
do; this host does not provide it." (it used to blame the page: "does not declare"). The assistant panel already
says "This page cannot reach a session." and "Ask now is not available on this page."

Live evidence for these handles is under "Verified, and how" (send, reply, ask and publish on the probe). Not run: the assistant template or the inbox on a Sites page by this author; that is the Sites owner's.

**Outside this surface:** `kit/store.js` is the adp/1 board store. It connects only through `window.claude.use('db')`
and `('user')` and says "Open this page on claude.ai" when that is absent, so a board built on it is Claude-only; it
is not part of the adp/2 host contract and is left unchanged. `kit/templates/tester.js` is a Claude capability tester
and is Claude-only by design, as are `claude-lane.js` and the catalog page's `parts/catalog.js`.

## Agent side

`plugins/artifacts-done-properly/skills/adp/scripts/adp_claude_adapter.py` is the Claude half of the shared records shell. It prints ArtifactData
`list` calls to read, one atomic `batch` (at most 50 writes, 1 MiB) to write, and parses the result text the agent
saves, wrapped as `[{call, result}]`. Observed live and relied on: a collection `list` shows each doc's native
`version`; a batch result names every committed doc with its new version; a refused batch starts "db batch
write failed (version_mismatch)", says nothing was written and names the first stale entry; an update that
rewrites the same text still bumps the version. Documented by the tool but not triggered here: a `set` over an
existing doc is refused unless pinned, which is what makes an unpinned create safe. A batch is all or nothing,
so `parse_receipt` never reports part of one as applied. The adapter needs no
separate readback: the batch result is the authority. Claude's page files are not part of the shell (use
`adp.py files` plus a publish).

`adp.py work --host claude` (the work planner, `plugins/artifacts-done-properly/skills/adp/scripts/adp_work.py`) prints one guarded `set` for a request claim, progress, checkpoint, block or completion. On a Claude artifact its claim, a reclaim after the lease expired and a completion with a receipt were each executed as one pinned `ArtifactData` batch and read back. Put a large planned document in a file and reference it with `file_path` in the batch rather than pasting it.

Mapped to the contract's
operations by reading the existing `adp-edit` protocol: Discover/Read = `Artifact read` + ArtifactData reads
(each carries `version`); Propose = `adp.py propose` (`incoming/`); Publish = `Artifact publish` to the same
url plus pinned ArtifactData writes; Verify = re-read; Acknowledge = `adp.py record`.

Observed live through ArtifactData on the probe artifact (same run, synthetic records at `content/intro`,
`decisions/keep-intent`, `ns/host-check/context/current`, which is collection `ns/host-check/context`, doc
`current`): a 3-write `batch` reported "committed atomically" with per-doc `version` 1; an `update` pinned
`if_version: 1` committed and returned version 2 (top-level fields merge, unknown fields survive, an array
field is replaced whole); a second write pinned to version 1 was refused `version_mismatch` naming version 2,
and wrote nothing; read-back matched. These versions are Claude doc revisions and are not tokens for another
host. Not observed: partial batch failure, a lost write response, or the rendered page reflecting the edit.
