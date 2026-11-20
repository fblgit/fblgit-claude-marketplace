> Copy of [`docs/host-adapters.md`](https://github.com/fblgit/artifacts-done-properly/blob/3f0062952f499370f88200d114e954bff82fe841/docs/host-adapters.md) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.
> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository
> (https://github.com/fblgit/artifacts-done-properly); `snippets.md` shows how to do the same by hand. Calls to Claude's own tools (`Artifact`, `ArtifactData`) are examples
> of what a Claude host offers: on another host, use that host's way to read and write the page.

# Host adapters (experimental `adp-host/1`)

ADP preserves more than an artifact's bytes: named parts, intent, decisions,
feedback, provenance, proposals and safe evolution. A host supplies the local
storage, interaction and publishing mechanisms; it does not redefine those
records. This first seam keeps the existing `adp/2` records and hash/classification
rules unchanged. It is not a new wire protocol and not itself a migration tool (the records shell in
`docs/adp-export-import.md` moves a page's records between hosts), and it makes no
claim that every host supports the Claude experience.

## Two different boundaries

1. **Browser runtime:** rendering and reading/writing the artifact's record store,
   viewer hints, and optional anchored comments. Implemented below.
2. **Agent host:** reading source, finding feedback, proposing changes, guarded
   publication, and verifying the result. The contract below is a handoff design,
   partly implemented: the records shell (`adp.py bundle`, `import-plan`, `import-ack`)
   and the work planner (`adp.py work`) work for Claude and Sites, and `adp.py` stays
   offline: it prints the calls and an authorized agent runs them. Assist, inbox and
   the assistant template take the host's handles (below); `claude-lane`, `store.js`,
   the tester and the catalog page remain Claude-only.

## Browser connection

Install a provider **before** loading `adp.js`:

```js
window.ADP_HOST = {
  protocol: 'adp-host/1',
  async connect() {
    return {
      id: 'my-host',
      db: myDocumentStore,                 // optional; full profile below
      user: {canEdit: async () => false, id: async () => ''}, // optional
      comments: myAnchoredComments,        // optional
      seedFiles: false                     // opt-in fetch of local seed files
    };
  }
};
```

With no explicit provider, the existing Claude `use('db'|'user'|'comments')`
bridge remains the default. Without either provider, the page renders its static
baseline and configuration defaults. An explicit malformed or failed provider
**never falls back to Claude**: that could read or write another backing store.
`ADP.host` reports `protocol`, `id`, `status` (`connecting`, `connected`, `failed`),
and after connection the `records`, `comments`, and `seedFiles` flags. Flags report
available interfaces, not proof of durability, authority, transactions or delivery.
The static connection has `id: 'static'` and no capabilities.

`connect()` must settle and providers must return a stable artifact-scoped backing
store. A provider must not switch identities/stores mid-session; reload after an
explicit switch. No automatic data copying or identity migration occurs.

### Document-store compatibility profile

This is deliberately the existing document API, not a requirement that every
native document surface emulate a database. If supplied, `db` must implement:

- `doc(path)` with async `get`, `set(data)`, `update(data)` and
  `onSnapshot(next, error)`;
- `collection(path)` with `onSnapshot`, and chainable `where(field, '==', value)`,
  `orderBy(field, 'desc')`, `limit(number)`;
- document snapshots with `exists` and `data()`; collection snapshots with `docs`,
  whose items carry `id`, `exists` and `data()`, plus `docChanges()` entries
  with `type` and `doc` (and the operations needed by seed packs).

Consult `adp.js` and the seed-file format for the exact operations. Providers must
supply initial snapshots and report subscription failures. Polling is allowed if
it implements the same observable contract and documents its latency; a one-time
read must not masquerade as a live subscription. Unsupported stores should omit
`db` rather than returning a partially working facade. Top-level shape checks
cannot verify a backend implementation; conformance and deployment tests remain
its author's responsibility.

`seedFiles: true` opts into the existing local `seed.json` and referenced seed packs/content fetch flow.
Only enable it in a host that can fetch the packaged files. Legacy Claude retains
this behavior. Seeding is not a transaction or compare-and-set guarantee.

### Identity and permissions

`user.canEdit()` must return the boolean `true` to enable editing UI; other values
and failures mean false. `user.can(name)` is optional: `ADP.user.can(name)` resolves its answer for a named right (the kit asks `data.write`), or `null` when the host says nothing. `user.id()` is a host-local display/audit identifier, not
a portable authorization credential. Omitted identity means anonymous read-only
UI. Never trust the browser's identity/flags at a server boundary: enforce access
there. Existing integrity reporting can attempt a `status/integrity` write even
for a viewer; backend policy decides whether it lands. `checks/latest`, seeding
and configuration edits retain their existing editor gates. Current configuration
updates are read-modify-write and do **not** promise atomic concurrency.

### Comments

`comments.customAnchors(callbacks)` is optional and follows the current runtime
controller contract: callbacks `mode`, `threads`, `reveal`, `composing`; controller
`compose(anchor, element, {label})`, and placement operations used by `place()`.
Logical `data-part` IDs remain the anchors; host-native block IDs are separate
locators. A missing/failed comments capability disables anchoring, not the page.
Saving a request is not equivalent to waking an agent, delivering it, or having
it read. Delivery to an agent is the separate `agent` handle below, not part of `comments`.

### Agent, publish and ask (optional handles)

A provider may return `agent`, `publish` and `ask`, each a handle or a promise of one. A page reaches them with
`await ADP.agent()`, `await ADP.publish()` and `await ADP.ask()`: the handle, or `null` when the host gave none, its
shape is wrong or (on Claude) the viewer did not grant the capability. `ADP.host.agent`, `.publish` and `.ask` report
which exist. The accessors return promises because a host may bind a capability late; shared code never probes
`window.claude` for them.

| Handle | Shape | Meaning |
| --- | --- | --- |
| `agent` | `{label, where?, canSend(), send({anchor\|threadId, text}), anchorFor(el)}` | Hand a request to an agent. `label` is the name the UI shows ("Claude", "Codex"). `where` (optional) is the place a person starts the agent ("Claude Code"); the UI says "your agent" without it. `canSend()` answers `available` (a session is watching), `queued` (the host keeps it durably for an agent that picks it up later), `writers_only`, `no_session` or `off`. `send()` resolves `{threadId, delivery}`: `queued` (kept, read back), `accepted` (the native host took the handoff: **not** that the agent ran or finished it) or `unknown` (reconcile the same id before sending again) |
| `publish` | `{files(files, opts)}` | The immediate native file publish (`{version, shas}`). Absent where the host has none; asynchronous approval is not forced into it |
| `ask` | `(messages, opts) => {text, …}` | An immediate model answer from the page. Separate from `agent`: a queued agent answer is not browser sampling |

Claude maps these from `comments.sendToClaude`/`canSendToClaude`/`anchorFor`, `artifact.publish` and `sample` (the adapter
and the built-in default); a Sites adapter supplies its own `agent` and leaves `publish` and `ask` out. `ADP.claude(name)`
stays for pages that call it. The `comments` option of `Kit.assist` and `Kit.inbox` is gone (a Claude-shaped
object is no longer taken for an agent): pass `agent`, `artifact` (a publish handle) and `sample`, or take the
page's host defaults. A wake-up from the
inbox is sent only when `canSend()` answers `available`.

## Agent-host handoff contract (design, partly implemented)

Keep source/record authority explicit. A future adapter should provide these
operations and receipts, without naming in-session connector calls as a public SDK:

| Operation | Required semantics |
| --- | --- |
| Discover | Host and artifact locator, supported profile, permissions, unsupported capabilities |
| Read | Source + `adp/2` records, native version token(s), completeness and change cursor |
| Propose | Existing base/live/incoming classification; preserve holds, explicit retirement and provenance |
| Publish | Expected native version(s), exact mutation set and idempotency key if supported |
| Verify | Read back authoritative result; reconcile partial/unknown outcomes before retry |
| Acknowledge | Record applied only for verified operations; distinguish proposed/pending/applied/failed/unknown |

Receipts must distinguish source commit, deployment version and record revision;
these are not interchangeable. Include per-operation outcomes when a host can
partially apply a batch. An exception/timeout is not proof that nothing changed.
If a host lacks guarded publication, report that limit and require a safe explicit
workflow rather than pretending a local cached version is a server-side guard.
Never clear a hold, retire a part or acknowledge feedback merely because an API
returned success for a different operation.

### Host profiles and implementation handoff

- **Claude:** preserve `adp/2` schemas, existing content/config/manifest and
  incoming/changes/decisions records. Claude's adapter can replace the inline
  compatibility bridge with an explicit provider without changing logical IDs.
  Assist, inbox, the assistant template, publish/sample and request
  delivery now run through the host-neutral handles, which both the explicit adapter and the built-in default supply.
- **ChatGPT Sites:** a Worker and durable backend (for example D1) can implement
  the document-store facade. Server authentication, authorization, subscriptions
  or polling, conditional writes and backend provisioning are separate work.
  Site-scoped identity is not a cross-Site principal. A saved source commit does
  not prove deployment succeeded; deployment and database writes are not one
  atomic transaction. The included OpenAI bridge is wiring, not that backend.
- **ChatGPT Space text Pages:** native block IDs, guarded edits, comments and
  change cursors belong in an **agent-side document adapter**, not a fabricated
  `window` database. Map logical parts to native locators, detect stale writes,
  resync when history is incomplete, and reconcile partial patch batches.
- **Space visualizations:** bounded shared widget state is UI state, not ADP's
  authoritative record database. Sandbox network constraints rule out assuming
  arbitrary runtime fetches or subscriptions. Native spreadsheets/slides require
  their own document profile.

The unit harness validates no live host. Live runs on Claude and Sites are summarised in
`docs/claude-host-adapter.md` and `docs/openai-sites-transport.md`; no Space installation has been validated.
The release gates for each host are: fresh and existing artifact, anonymous and
editor access, stale version rejection, concurrent writes, interrupted/repeated
publish, readback/receipt reconciliation, missing capabilities, and reopening in
a new session with intent/feedback/history intact. Do not advertise a host as
fully supported until its live flow passes those gates.

## Capability references

Host guidance checked for this proposal (2026-11-16):
[Space overview](https://help.openai.com/en/articles/20001549-getting-started-with-space-in-chatgpt),
[Sites overview](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites),
[Site-hosted plugins](https://help.openai.com/en/articles/20001547-hosting-a-plugin-with-chatgpt-sites).
Detailed native editor/tool contracts are environment-specific, not a stable
public browser SDK; validate them again when implementing each native adapter.
