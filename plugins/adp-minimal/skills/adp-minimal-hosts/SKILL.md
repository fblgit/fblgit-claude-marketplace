---
name: adp-minimal-hosts
description: "Explains the ADP host adapter framework (adp-host/1): window.ADP_HOST and connect(), the db, user and comments contract, the agent, publish and ask handles, failing closed, the common ground components reuse through ADP.db, ADP.user and ADP.agent() instead of window.claude, the Claude, Sites and OpenAI adapters, the agent-host contract and its receipts, and how to write a new adapter. Use when the user asks how ADP runs on another host, what a component may rely on, or how Sites differs from Claude."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Host adapters: the shell's boundary, and the common ground components reuse

ADP pages and kits are meant to be reused, including on hosts other than claude.ai. The host adapter is what makes that possible.

ADP runs on more than one host: the claude.ai viewer, ChatGPT Sites, a local emulator. The page, the kit and the record format are the same on all of
them. What differs is **how a page reads and writes its records, who the viewer is, how comments anchor, and how a request reaches an agent**. That is
the host adapter. It exists so that no component ever names a host.

## Two boundaries

1. **Browser runtime.** The page talks to a provider: a record store, an identity, anchored comments and three optional handles. This is `adp-host/1`.
2. **Agent host.** The agent reads source, finds feedback, proposes, publishes with a guard, verifies. `adp.py` stays offline: it prints native calls, an
   authorized agent runs them. See [packing](../adp-minimal-packing/SKILL.md) for moving records between hosts.

## Connecting a provider

A provider is installed before `adp.js` loads:

```html
<script src="adapters/claude.js"></script>
<script>window.ADP_HOST = ADPClaudeHost.create();</script>
<script src="adp.js"></script>
```

```js
window.ADP_HOST = {
  protocol: 'adp-host/1',
  async connect() {
    return {
      id: 'my-host',
      db: myDocumentStore,                                   // optional record store
      user: {canEdit: async () => false, id: async () => ''},// optional identity
      comments: myAnchoredComments,                          // optional anchored comments
      agent, publish, ask,                                   // optional handles
      seedFiles: false                                       // fetch local seed files?
    };
  }
};
```

- With no provider the runtime uses the built-in Claude bridge (`window.claude.use('db' | 'user' | 'comments')`). With neither, the page renders its static
  baseline and the switches' defaults.
- A malformed or failed provider **never falls back** to another host: that could write another backing store. `ADP.host.status` is `connected`,
  `connecting`, `failed` or, for no provider, `static`.
- `connect()` must settle; a provider must not switch identity or store mid-session.

## What a provider gives

| Part | Contract |
|---|---|
| `db` | The document API the runtime already uses: `doc(path)` with `get`, `set`, `update`, `onSnapshot`; `collection(path)` with `onSnapshot`, `where`, `orderBy`, `limit`; snapshots carrying `exists`, `data()`, `docs`, `docChanges()`. A store that cannot do this omits `db` instead of faking it. |
| `user` | `canEdit()` must resolve literal `true` to enable edit UI; `id()` is a display/audit name, not a credential; `can(name)` is the host's answer for a named right (`data.write`) or `null`. |
| `comments` | `customAnchors(callbacks)`: `mode`, `threads`, `reveal`, `composing`, plus `compose(anchor, el, {label})` and placement. Anchors are part ids; a failed capability disables anchoring, not the page. |
| `agent` | `{label, where?, canSend(), send({anchor\|threadId, text}), anchorFor(el)}`: hand a request to an agent. `canSend()` answers `available`, `queued`, `writers_only`, `no_session` or `off`. |
| `publish` | `{files(files, opts)}`: the immediate native file publish, `{version, shas}`. Absent where the host has none. |
| `ask` | `(messages, opts) => {text}`: an immediate model answer from the page. Separate from `agent`. |

## The common ground

Everything shared sits behind `ADP`, never behind the host:

```js
const db    = await ADP.db;                 // the record store, whichever host
const me    = ADP.user;                     // {canEdit, id, can(name)}
const agent = await ADP.agent();            // handle or null
if (agent && (await agent.canSend()) === 'available') await agent.send({anchor: 'home.lead', text: 'Tighten this'});
const pub   = await ADP.publish();          // handle or null
const ask   = await ADP.ask();              // handle or null
```

A component written this way runs on every host that supplies those pieces and degrades where it does not: `null` handle, no button. The kit's
`inbox`, `assist`, `assist-panel`, `request-card` and `presence` are written like this. `claude-lane`, `store.js` (the adp/1 board store), `tester` and the
catalog page still call `window.claude` directly and say so in their headers: that is the exception, not the pattern, and a new component must not copy
it.

## The hosts

| Host | How it connects | Notes |
|---|---|---|
| **Claude** (`adapters/claude.js`) | Wraps `window.claude.use('db'\|'user'\|'comments')`; `agent`, `publish`, `ask` map from `comments.sendToClaude`, `artifact.publish`, `sample`; `null` where the viewer did not grant the capability | Same records, hashes and classification as the built-in bridge. Without `window.claude`, `connect()` throws: fails closed. |
| **Sites** (`adapters/openai-sites.js` + a Worker) | Authenticated same-origin HTTP at `/api/adp/<artifact-id>`, polling at least 1 s; a Worker and a durable store (D1) answer | Server authorization is authoritative. A source commit is not a deployment; a deployment and a record write are not one transaction; Sites supplies its own `agent` and no `publish` or `ask`. |
| **OpenAI bridge** (`adapters/openai.js`) | An integration contract: a trusted integrator supplies `bridge.connect()` | Not a native browser SDK; it probes nothing and handles no credentials. |
| **Local** (`adp.py dev`) | The dev shim stands in for `window.claude` | For pages and tests offline. |

### Sites in one page

Same parts, same catalog, same protocol; native calls replace the Claude ones. Keep the Site source in the project and confirm the Site id, URL and
connection match the checkout. `adp.py files ASSETS --host sites --out SITE_PROJECT` writes the asset snapshot and the canonical API handler and names
the required `DB` binding and schema; it deploys nothing. Guard source publication with the source revision; pin record writes with the record
revisions; record with the deployment id as the publication version; read back before acknowledging. If any outcome is unknown, inspect the
deployment or read back the records before retrying, and report partial success as partial.

## The agent-host contract

Whatever the host, an agent adapter provides the same six things, and receipts keep three revisions apart (source commit, deployment version, record
revision):

| Operation | Semantics |
|---|---|
| Discover | host, artifact locator, profile, permissions, unsupported capabilities |
| Read | source and records, native version tokens, completeness |
| Propose | base / live / incoming classification, with holds, explicit retirement and provenance |
| Publish | expected native versions, the exact mutation set, an idempotency key if supported |
| Verify | read back the authoritative result; reconcile partial or unknown outcomes before retrying |
| Acknowledge | record *applied* only for verified operations; distinguish proposed, pending, applied, failed, unknown |

An exception or a timeout is not proof that nothing changed. A host without guarded publication is reported as such; a locally cached version is never
passed off as a server-side guard.

## Writing a new adapter

1. Implement `connect()` returning only what the host can really do; omit the rest.
2. Make `db` honest: initial snapshots, real subscriptions or documented polling, conditional writes that surface as `if_version` failures.
3. Never let the browser's identity be the authority; enforce access on the server.
4. Run the page's flow on it: a fresh and an existing artifact, anonymous and editor, a stale write rejected, concurrent writes, an interrupted publish,
   a missing capability, reopening in a new session with intent, feedback and history intact. Do not call a host supported before those pass.
