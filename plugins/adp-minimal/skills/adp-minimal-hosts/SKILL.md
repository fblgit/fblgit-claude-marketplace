---
name: adp-minimal-hosts
description: "Reference for the ADP host adapter protocol (adp-host/1): installing a provider with window.ADP_HOST and connect(); the db, user and comments contract; the optional agent, publish and ask handles; why a failed provider never falls back to another host; the host-neutral surface components use (ADP.db, ADP.user, ADP.agent(), ADP.publish(), ADP.ask()) instead of window.claude; the Claude, ChatGPT Sites and OpenAI bridge adapters; the agent-host operations and the receipts that keep source, deployment and record revisions apart; and how to write and test a new adapter. Use when the user asks how ADP runs on a host other than claude.ai, what a component may rely on, how ChatGPT Sites differs from Claude, or how to add a host."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Host adapters

ADP runs on more than one host: the claude.ai viewer, ChatGPT Sites, and a local dev shim. The page, the kit and the record format are the same on
all of them. What differs is how a page reads and writes its records, who the viewer is, how comments anchor, and how a request reaches an agent. A
host adapter implements those four concerns so that components never reference a specific host.

## Two boundaries

1. **Browser runtime.** The page talks to a provider that supplies a record store, a viewer identity, anchored comments and three optional handles.
   This is `adp-host/1`.
2. **Agent host.** The agent reads the artifact source and pending feedback, proposes changes, publishes them with a version check, and verifies the
   result. `adp.py` makes no network calls: it emits the host's native calls for an authorized agent to run. See
   [packing](../adp-minimal-packing/SKILL.md) for moving records between hosts.

## Connecting a provider

Install the provider before `adp.js` loads:

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
      db: myDocumentStore,                                    // optional record store
      user: {canEdit: async () => false, id: async () => ''}, // optional identity
      comments: myAnchoredComments,                           // optional anchored comments
      agent, publish, ask,                                    // optional handles
      seedFiles: false                                        // opt in to fetching local seed files
    };
  }
};
```

- With no provider, the runtime uses the built-in Claude bridge (`window.claude.use('db' | 'user' | 'comments')`). With neither, the page renders its
  static content and the default value of each [switch](../adp-minimal-runtime/SKILL.md) (a named page setting stored in `config/current`).
- A malformed or failed provider **never falls back** to another host: falling back could send writes to a different store than the one the page was
  opened against. `ADP.host.status` is `connecting`, `connected` or `failed`; with no provider and no Claude bridge, `ADP.host.id` is `static` and
  no capability is available.
- `connect()` must settle, and a provider must not switch identity or store mid-session.

## What a provider supplies

| Part | Contract |
|---|---|
| `db` | The document API the runtime already uses: `doc(path)` with `get`, `set`, `update`, `onSnapshot`; `collection(path)` with `onSnapshot`, `where`, `orderBy`, `limit`; snapshots carrying `exists`, `data()`, `docs`, `docChanges()`. If the store cannot implement all of it, omit `db`; do not return a partial implementation. |
| `user` | `canEdit()` must resolve to the boolean `true` to enable editing UI. `id()` is a display and audit name, not a credential. `can(name)` resolves the host's decision for a named permission (the kit asks `data.write`), or `null` when the host has none. |
| `comments` | `customAnchors(callbacks)`: callbacks `mode`, `threads`, `reveal`, `composing`; the controller provides `compose(anchor, el, {label})` and placement. Anchors are part ids. If the comments capability fails, anchoring is disabled and the page keeps working. |
| `agent` | `{label, where?, canSend(), send({anchor\|threadId, text}), anchorFor(el)}`: hands a request to an agent. `canSend()` resolves to `available`, `queued`, `writers_only`, `no_session` or `off`. |
| `publish` | `{files(files, opts)}`: publishes files through the host's native API and resolves to `{version, shas}`. Omitted where the host has no such API. |
| `ask` | `(messages, opts) => {text}`: returns a model answer to the page directly. It is separate from `agent`, which hands work to an agent session. |

## The host-neutral surface

Components use host features only through the `ADP` global:

```js
const db    = ADP.db;                       // the record store, or null until the host connects or if it has none
const me    = ADP.user;                     // {canEdit, id, can(name)}
const agent = await ADP.agent();            // handle or null
if (agent && (await agent.canSend()) === 'available') await agent.send({anchor: 'home.lead', text: 'Tighten this'});
const pub   = await ADP.publish();          // handle or null
const ask   = await ADP.ask();              // handle or null
```

A component written this way runs on every host that supplies those handles. Where a host lacks one, the handle is `null` and the component hides
the related control. The kit's `inbox`, `assist`, `assist-panel`, `request-card` and `presence` follow this rule. `claude-lane`, `store.js` (the adp/1
board store), `tester` and the catalog page still call `window.claude` directly and say so in their headers. They are known exceptions; new
components must use `ADP.*`.

## The hosts

| Host | How it connects | Notes |
|---|---|---|
| **Claude** (`adapters/claude.js`) | Wraps `window.claude.use('db'\|'user'\|'comments')`. `agent`, `publish` and `ask` map from `comments.sendToClaude`, `artifact.publish` and `sample`, and are `null` where the viewer did not grant the capability. | Same records, hashes and classification as the built-in bridge. Without `window.claude`, `connect()` throws and `ADP.host.status` is `failed`. |
| **ChatGPT Sites** (`adapters/openai-sites.js` + a Worker) | Authenticated same-origin HTTP at `/api/adp/<artifact-id>`, answered by a Worker backed by a D1 database. Polls every 2 s by default; the interval cannot be set below 1 s. | The server is the authority for every access decision. Committing source does not deploy it, and a deployment is not atomic with record writes, so each step is verified separately. The adapter supplies its own `agent` and no `publish` or `ask`. |
| **OpenAI bridge** (`adapters/openai.js`) | An integration contract: the integrating application supplies `bridge.connect()`. | Not a native browser SDK. It does not discover tools, install a plugin or deploy a Site. |
| **Local** (`adp.py dev`) | The dev shim stands in for `window.claude`. | For running pages and tests offline. |

### Deploying to ChatGPT Sites

Same parts, same catalog, same protocol; native Sites operations replace the Claude ones. Keep the Site source in the project and confirm the Site ID
and URL match the checkout. `adp.py files ASSETS --host sites --out SITE_PROJECT` writes the asset snapshot and the API handler, and names the
required `DB` binding and schema; it deploys nothing. Then:

1. Publish the source through the native Sites tools, guarded by the expected source revision.
2. Read the deployed files back.
3. Write the records, each guarded by its **pin**: the record revision read earlier, passed as `if_version` so a stale write is refused (see
   [the protocol](../adp-minimal-protocol/SKILL.md)). Use the deployment ID as the publication version.
4. Read the records back before reporting success.

These are sequential operations, not one transaction. If any outcome is unknown, inspect the deployment or read the records back before retrying,
and report which steps succeeded and which did not.

## The agent-host contract

On any host, an agent adapter implements six operations. Each operation's **receipt** (the result the adapter reports for it) records three separate
identifiers: the source commit, the deployment version and the record revision.

| Operation | Semantics |
|---|---|
| Discover | Host, artifact locator, profile, permissions, unsupported capabilities |
| Read | Source and records, native version tokens, completeness |
| Propose | Base / live / incoming classification; preserve **holds** (an agent's time-limited claim on the parts it will edit), explicit **retirement** (a part id removed and never reused) and provenance. See [the protocol](../adp-minimal-protocol/SKILL.md). |
| Publish | Expected native versions, the exact mutation set, an idempotency key if the host supports one |
| Verify | Read back the authoritative result; reconcile partial or unknown outcomes before retrying |
| Acknowledge | Record *applied* only for verified operations; distinguish proposed, pending, applied, failed and unknown |

An exception or a timeout is not proof that nothing changed. If a host has no guarded publication, report that limitation; a locally cached version
must not be used as a concurrency check.

## Writing a new adapter

1. Implement `connect()` to return only the capabilities the host supports; omit the rest.
2. Implement `db` fully: initial snapshots, live subscriptions or documented polling, and conditional writes that fail with `if_version` errors when
   the version is stale.
3. Do not trust identity reported by the browser; enforce access control on the server.
4. Run the page's flow on the new host: a fresh and an existing artifact, anonymous and editor access, a stale write rejected, concurrent writes, an
   interrupted publish, a missing capability, and reopening in a new session with the recorded intent, feedback and change history intact. Do not
   call a host supported until all of these pass.
