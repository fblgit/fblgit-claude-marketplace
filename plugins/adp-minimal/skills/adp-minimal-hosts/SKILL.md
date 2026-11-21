---
name: adp-minimal-hosts
description: "Reference for the ADP host adapter protocol (adp-host/1): installing a provider with window.ADP_HOST and connect(); the db, user and comments contract; the optional agent, publish and ask handles; why a failed provider never falls back to another host; the host-neutral surface components use (ADP.db, ADP.user, ADP.agent(), ADP.publish(), ADP.ask()) instead of window.claude; the Claude and OpenAI bridge adapters; the agent-host operations and the receipts that keep source, deployment and record revisions apart; and how to write and test a new adapter. Use when the user asks how ADP runs on a host other than claude.ai, what a component may rely on, or how to add a host."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Host adapters

ADP runs on more than one host: the claude.ai viewer and any host whose adapter implements `adp-host/1`. The page, the kit and the record format are the same on
all of them. What differs is how a page reads and writes its records, who the viewer is, how comments anchor, and how a request reaches an agent. A
host adapter implements those four concerns so that components never reference a specific host.

## Two boundaries

1. **Browser runtime.** The page talks to a provider that supplies a record store, a viewer identity, anchored comments and three optional handles.
   This is `adp-host/1`.
2. **Agent host.** The agent reads the artifact source and pending feedback, proposes changes, publishes them with a version check, and verifies the
   result. `adp.py` makes no network calls: it emits the host's native calls for an authorized agent to run. See
   [packing](../adp-minimal-packing/SKILL.md) for moving records between hosts.

## Connecting a provider

On claude.ai a page needs no provider: `adp.js` connects through its built-in Claude bridge. A page for another host installs a provider before
`adp.js` loads, by setting `window.ADP_HOST` in a script placed before it:

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

`connectHost` in `adp.js` picks the provider: `window.ADP_HOST` when the page set it (even to a bad value), else the Claude bridge, else
`{id: 'static'}`. It refuses a connection without an id, a `db` without `doc` and `collection`, and a `user` without `canEdit` and `id`. The Claude
bridge wraps each `window.claude.use` handle in the neutral shape, and a handle the viewer did not grant becomes `null`. `attach` publishes
`ADP.host` and resolves the `agent`, `publish` and `ask` handles, turning on their flag in `ADP.host` once each proves valid.

```js
// ---
// id: hosts.connect
// tool: adp.js
// section: hosts
// order: 100
// needs: [core.runtime]
// tests: [runtime-an-invalid-provider-fails-closed, runtime-an-editor-seeds-an-empty-record]
// sha: 0c214dbb102e
// ---
const isFn = (o, k) => !!o && typeof o[k] === 'function', safely = (f, fallback) => Promise.resolve().then(f).catch(() => fallback);
const HANDLE_OK = {agent: o => isFn(o, 'canSend') && isFn(o, 'send'), publish: o => isFn(o, 'files'), ask: o => typeof o === 'function'};
const CLAUDE = {
  user: u => isFn(u, 'canEdit') ? Object.freeze({canEdit: () => u.canEdit(), id: () => isFn(u, 'id') ? u.id() : '', can: n => isFn(u, 'can') ? u.can(n) : null}) : null,
  agent: c => isFn(c, 'sendToClaude') && isFn(c, 'canSendToClaude') ? Object.freeze({label: 'Claude', where: 'Claude Code',
    canSend: () => Promise.resolve(c.canSendToClaude()), anchorFor: el => Promise.resolve(c.anchorFor(el)),
    send: async m => {
      m = m || {};
      const r = await c.sendToClaude(m.threadId ? {threadId: m.threadId, text: m.text} : {anchor: m.anchor, text: m.text});
      return {threadId: (r && r.threadId) || m.threadId || '', delivery: 'accepted'};
    }}) : null,
  publish: a => isFn(a, 'publish') ? Object.freeze({files: (files, opts) => Promise.resolve(a.publish(files, opts))}) : null,
  ask: s => typeof s === 'function' ? (messages, opts) => s(messages, opts) : null};
async function connectHost() {
  let c;
  if (Object.prototype.hasOwnProperty.call(window, 'ADP_HOST')) {           // an explicit provider never falls back to another host
    const p = window.ADP_HOST;
    if (!p || p.protocol !== 'adp-host/1' || !isFn(p, 'connect')) throw new Error('Invalid ADP_HOST provider');
    c = await p.connect();
  } else if (isFn(window.claude, 'use')) {
    const use = name => safely(() => window.claude.use(name), null), comments = use('comments');
    const [db, user] = await Promise.all([use('db'), use('user')]);
    c = {id: 'claude', db, user: CLAUDE.user(user), commentsReady: comments, seedFiles: true,
      agent: comments.then(CLAUDE.agent), publish: use('artifact').then(CLAUDE.publish), ask: use('sample').then(CLAUDE.ask)};
  } else return {id: 'static'};
  if (!c || typeof c.id !== 'string' || !c.id.trim()) throw new Error('Host connection needs an id');
  if (c.db && !(isFn(c.db, 'doc') && isFn(c.db, 'collection'))) throw new Error('Host database needs the document-store profile');
  if (c.user && !(isFn(c.user, 'canEdit') && isFn(c.user, 'id'))) throw new Error('Invalid host user capability');
  return c;
}
let host = Object.freeze({protocol: 'adp-host/1', id: '', status: 'connecting'}), hostComments = null;
const handles = {}, hostSet = o => { host = Object.freeze({...host, ...o}); };
function attach(c) {
  hostComments = c.comments || null;
  host = Object.freeze({protocol: 'adp-host/1', id: c.id, status: 'connected', records: !!c.db, comments: isFn(hostComments, 'customAnchors'),
    seedFiles: c.seedFiles === true, agent: false, publish: false, ask: false});
  for (const k of ['agent', 'publish', 'ask'])
    handles[k] = Promise.resolve(c[k]).then(o => HANDLE_OK[k](o) ? o : null, () => null).then(o => { if (o) hostSet({[k]: true}); return o; });
  (c.commentsReady ? c.commentsReady.then(cm => { hostComments = cm; hostSet({comments: isFn(cm, 'customAnchors')}); return anchors(); }) : anchors())
    .catch(() => pushErr('comments unavailable'));
}
```

## What a provider supplies

| Part | Contract |
|---|---|
| `db` | The document API the runtime already uses: `doc(path)` with `get()`, `set()`, `update()`, `onSnapshot()`; `collection(path)` with `onSnapshot`, `where`, `orderBy`, `limit`; snapshots carrying `exists`, `data()`, `docs`, `docChanges()`. If the store cannot implement all of it, omit `db`; do not return a partial implementation. |
| `user` | `canEdit()` must resolve to the boolean `true` to enable editing UI. `id()` is a display and audit name, not a credential. `can(name)` resolves the host's decision for a named permission (the kit asks `data.write`), or `null` when the host has none. |
| `comments` | `customAnchors(callbacks)`: callbacks `mode`, `threads`, `reveal`, `composing`; the controller provides `compose(anchor, el, {label})` and placement. Anchors are part ids. If the comments capability fails, anchoring is disabled and the page keeps working. |
| `agent` | `{label, where?, canSend(), send({anchor\|threadId, text}), anchorFor(el)}`: hands a request to an agent. `canSend()` resolves to `available`, `queued`, `writers_only`, `no_session` or `off`. |
| `publish` | `{files(files, opts)}`: publishes files (`[{path, ifMatch?, contentType, content}]`) through the host's native API with the [guarded publish](#the-record-and-publish-guarantees) rule, and resolves to `{version, shas}`. Omitted where the host has no such API. |
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
the related control. A kit entry that must call `window.claude` directly says so in its header; new entries use `ADP.*`.

## The hosts

| Host | How it connects | Notes |
|---|---|---|
| **Claude** (built into `adp.js`) | Wraps `window.claude.use('db'\|'user'\|'comments')`. `agent`, `publish` and `ask` map from `comments.sendToClaude`, `artifact.publish` and `sample`, and are `null` where the viewer did not grant the capability. | The reference host: the protocol's guarantees are those of `ArtifactData` and `Artifact`. |
| **OpenAI bridge** (`adapters/openai.js`) | An integration contract: the integrating application supplies `bridge.connect()`. | Not a native browser SDK. It does not discover tools, install a plugin or deploy a page. |

### Deploying to another host

Same parts, same catalog, same protocol; the host's native source and record operations replace the Claude ones. Keep the host's project source
with the page and confirm its id and URL match the checkout. `adp.py files` prints the page's files; it deploys nothing. Then:

1. Publish the source through the host's tools, guarded by the expected source revision.
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

### The record and publish guarantees

ADP's concurrency rests on these guarantees, not on holds. On Claude, `ArtifactData` and `Artifact` provide them; any other host's agent adapter
must provide the same before it can run the [protocol](../adp-minimal-protocol/SKILL.md):

| Guarantee | Requirement |
|---|---|
| Versions on read | Every document read returns the store's integer revision of that document, the value a later write passes as `if_version`. |
| Conditional writes | A write to an existing document carries `if_version` and is refused when the document has changed since that revision, or when `if_version` is missing. A create (`"set"` with no `if_version`) is refused when the document already exists. |
| Atomic batches | A batch is applied all or nothing: if any write in it is refused, none is applied. The result names every document written and its new revision: `{results: [{collection, doc_id, version}]}`. Separate batches are not atomic as a group. |
| Guarded publish | Each published file can carry `ifMatch`, the SHA-256 of the file as read; the publish is refused with `conflict` when any such file has changed. The result carries the new version and each file's SHA-256: `{version, shas}`. |

These apply to the agent's record and publish calls. The browser `db` handle above takes no version argument, so writes made from the page
(seeding, switches, requests, and the inbox's Apply) are not pinned: an editor's Apply and an agent's `record` on the same page are not
guarded against each other by the store. Until `db` carries a version, run one of them at a time on a page.

## The Claude adapter in `adp.py`

`adp.py` makes no calls. A host adapter in `HOSTS` turns its plans into the host's calls, which the agent runs, and parses what the calls
return. An adapter has four functions. `raw` is what the agent saves: `[{call, result}]`, the call printed by `adp.py` and the text it returned.

| Function | Does |
|---|---|
| `read_calls(artifact, collections)` | one `ArtifactData list` call per collection |
| `parse_reads(raw)` | `{docs: [{collection, id, data, revision}], covered, complete, warnings}`; a listing with a `next_cursor` is incomplete, and so is no result at all (`warnings: ["no read results"]`) |
| `write_calls(artifact, ops)` | `ops` are `{op, collection, id, data, guard}`, `op` being `create` (a `"set"` with no pin) or `replace` (pinned to `guard`). Atomic `ArtifactData batch` calls of at most 50 writes and 900 KB, each with its `keys` |
| `parse_receipt(raw)` | one `{collection, id, outcome, revision, error}` per key: `applied` when the batch result names the document, `rejected` when it reports that nothing was written, else `unknown` |

```python
# ---
# id: hosts.claude
# tool: adp.py
# section: hosts
# order: 250
# needs: [core.io]
# tests: [bundle-from-raw-reads, move-through-the-raw-adapter]
# sha: 6a83d54d8106
# ---
from types import SimpleNamespace


def claude_read_calls(artifact, collections):
    return [{'tool': 'ArtifactData', 'args': {'action': 'list', 'url': artifact, 'collection': c, 'query': {'limit': 1000}}, 'collection': c}
            for c in collections]


def claude_parse_reads(raw):
    docs, covered, warnings = [], set(), []
    for r in raw:
        c, text = r['call']['collection'], r['result']
        covered.add(c)
        for line in text.splitlines():
            if line.startswith('{"id":'):
                d = json.loads(line)
                docs.append({'collection': c, 'id': d['id'], 'data': d['data'], 'revision': d.get('version')})
        if 'next_cursor' in text: warnings.append(f'{c}: more pages (next_cursor)')
    return {'docs': docs, 'covered': sorted(covered), 'complete': bool(raw) and not warnings, 'warnings': warnings or ([] if raw else ['no read results'])}


def claude_write_calls(artifact, ops):
    calls, cur, size = [], [], 0
    for o in ops:
        w = {'op': 'set', 'collection': o['collection'], 'doc_id': o['id'], 'data': o['data']}
        if o['op'] == 'replace': w['if_version'] = o['guard']
        n = len(json.dumps(w, ensure_ascii=False).encode())
        if cur and (len(cur) == 50 or size + n > 900_000): calls.append(cur); cur, size = [], 0
        cur.append(w); size += n
    if cur: calls.append(cur)
    return [{'tool': 'ArtifactData', 'args': {'action': 'batch', 'url': artifact, 'writes': c}, 'atomic': True,
             'keys': [f"{w['collection']}/{w['doc_id']}" for w in c]} for c in calls]


def claude_parse_receipt(raw):
    out = []
    for r in raw:
        text = r['result']
        done = {f'{c}/{i}': int(v) for c, i, v in re.findall(r'- \w+ "([^"]+)"/"([^"]+)" \(version (\d+)\)', text)}
        bad = re.search(r'db (?:batch )?write failed[^\n]*|nothing was written[^\n]*', text)
        for k in r['call']['keys']:
            c, i = k.rsplit('/', 1)
            out.append({'collection': c, 'id': i, 'revision': done.get(k), 'error': bad.group(0) if bad and k not in done else None,
                        'outcome': 'applied' if k in done else 'rejected' if bad else 'unknown'})
    return out


HOSTS = {'claude': SimpleNamespace(read_calls=claude_read_calls, parse_reads=claude_parse_reads, write_calls=claude_write_calls,
                                   parse_receipt=claude_parse_receipt)}
```

## Writing a new adapter

1. Implement `connect()` to return only the capabilities the host supports; omit the rest.
2. Implement `db` fully: initial snapshots, and live subscriptions or documented polling. Implement the agent side with every
   [record and publish guarantee](#the-record-and-publish-guarantees).
3. Do not trust identity reported by the browser; enforce access control on the server.
4. Run the page's flow on the new host: a fresh and an existing artifact, anonymous and editor access, a stale write rejected, concurrent writes, an
   interrupted publish, a missing capability, and reopening in a new session with the recorded intent, feedback and change history intact. Do not
   call a host supported until all of these pass.
