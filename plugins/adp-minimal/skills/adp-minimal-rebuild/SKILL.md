---
name: adp-minimal-rebuild
description: "Reimplement the ADP CLI (adp.py), browser runtime (adp.js) and catalog tool (adp_catalog.py) from their specs, and check the result against the conformance suite: build order, fixture and vector format, normalization rules, and the vector runner. Use when the user wants these tools built from the specification, or asks how a build is tested."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Reimplementing the ADP tooling

The ADP (Artifacts Done Properly) skills specify the tooling well enough to build it: each command's contract is in the skill that documents it, and
its **vectors** (inputs paired with the exact expected output) are in the `vectors.md` next to that skill's `SKILL.md`, read only when building.
Together the vectors form the **conformance suite**. An implementation is conformant only if it passes every vector.

The vectors are golden outputs recorded from a conforming implementation, not hand-written.

## Scope

| Reimplement | Contract in (vectors in its `vectors.md`) | Verified by vectors |
|---|---|---|
| hashing, `check`, `manifest`, `diff`, `diff-pages` | [adp-minimal-parts](../adp-minimal-parts/SKILL.md) | yes |
| `classify` (and `ADP.classify`); the loop: `export`, `propose`, `ack`, `gate` | [adp-minimal-delta](../adp-minimal-delta/SKILL.md) | yes |
| `hold`, `record`, `config` (show, and its `set` subcommand), `requests`, `work` | [adp-minimal-protocol](../adp-minimal-protocol/SKILL.md) | yes |
| `files`, `--since`, `--batch` and `pins`, `files --host single`, `unpack`, `seed`; `bundle`, `import-plan`, `import-ack` (with the Claude adapter) | [adp-minimal-packing](../adp-minimal-packing/SKILL.md) | yes |
| `templates`, `new` (with the `minimal` template: write the fixture `template-minimal` to `templates/minimal/` beside the build before running the vectors) | [adp-minimal-new-artifact](../adp-minimal-new-artifact/SKILL.md) | yes |
| `adp.js`: `ADP.hash`, connecting an `adp-host/1` provider, seeding, `ADP.config` | [adp-minimal-runtime](../adp-minimal-runtime/SKILL.md) | yes |
| `adp_catalog.py build` and the check; `kit`, `suggest`, `take`, `catalog` (including My Own Kit, the user's local copy of the catalog at `~/.adp/catalog`, which `catalog` fetches into and `kit`, `suggest` and `take` read) | [adp-minimal-catalog](../adp-minimal-catalog/SKILL.md) | yes |
| `adp.js` parts that draw into the DOM: content painting, the "What changed" panel, anchors, the integrity badge, the self-check | [adp-minimal-runtime](../adp-minimal-runtime/SKILL.md) | no: spec only; requires a browser test harness |
| the Sites adapter, `files --host sites`; `dev serve` (the local emulator); `setup`, `init`, `projects`, `log`; `source-drift` | none | out of scope (deployment, installation and repository tooling) |

## Build order

1. **The hash core** (one stdlib Python file, `adp.py`): the id grammar, the marker pattern, `norm`, `H`, parsing with a stack, a part's own text (its region minus its child parts) and `_rest`.
2. **`manifest`**, then **`check`**, then **`diff`** and **`diff-pages`**: all read a page or a folder through the same loader.
3. **`classify`**: the table and the closure, over three manifests.
4. **`files`** (publish arguments), **`files --host single`** and **`unpack`** (the one-file pack, round trip byte for byte).
5. **`seed`**: `seed.json` and `seed/pack-NNN.json`, `manifest/current` last.
6. **`hold`** and **`record`**: the [pinned batches](../adp-minimal-protocol/SKILL.md), one document per file.
7. **`config`** (show and `set`), **`requests`**, **`work`**: the same [pinned batches](../adp-minimal-protocol/SKILL.md), for switches, requests and leases.
8. **The loop**: `export` (the nested git repository with `base`, `live`, `work`; `git merge-tree` for the three-way merge), `propose`, `ack`, `gate`.
9. **`bundle`**, **`import-plan`**, **`import-ack`**, then each supported host adapter (`adp_claude_adapter.py` first).
10. **`adp.js`**: the pure section (`H`, `norm`, markers, `_rest`, `classify`, exposed as `ADP.hash` and `ADP.classify`), then connecting a host,
    seeding and `ADP.config`; then the DOM-facing parts (spec only, see [adp-minimal-runtime](../adp-minimal-runtime/SKILL.md)).
11. **`adp_catalog.py`**: `build` (the index from the headers) and the check (sizes, hashes, orphans, headers, samples); then `kit`, `suggest`,
    `take`, `catalog` in `adp.py`.
12. **`new`** last: it copies a template and calls `seed` and `take`.

After each step, run that step's vectors (`run(..., only={...})`); at the end, run the full suite.

## Fixtures and vectors

A **fixture** is a named file tree, written as a fenced block whose info string is `json fixture`. With `"base": "<fixture>"` it starts from that
fixture's files; its own files override them, and a file set to `null` is removed:

```json
{"fixture": "example", "files": {"index.html": "<!-- part:a --><p data-part=\"a\">A</p><!-- /part:a -->\n"}}
```

A **vector** is a fenced block whose info string is `json vector`. It runs one command (or several `steps`) and states what must come back:

| Field | Meaning |
|---|---|
| `vector` | its name |
| `run` | the command: first the tool (`adp.py`, `adp_catalog.py`, or `adp.js` for the browser runtime), then the arguments. `{name}` is the fixture `name` written to a fresh folder; `{out}` is an empty scratch folder; `{home}` is the vector's `ADP_HOME` |
| `exit` | the exit code |
| `stdout` | the JSON printed, after normalization; or `stdout_text`, the text printed, as a list of lines |
| `stderr_text` | the text written to stderr, as a list of lines; used to assert error messages |
| `files_out` | `{path: content}` the command must have written (`{out}/...`, `{name}/...`), JSON compared as JSON; a `*` in the path matches a name that holds an id |
| `steps` | several of the above in order, sharing the folders; `same_tree: [a, b]` then requires two folders to be equal byte for byte, and `copy: [src, dst]` replaces folder dst with a copy of src (a change made between two runs) |

For `adp.js` the "command" is a call into the runtime, loaded in Node with a stub DOM: `["adp.js", "hash", FILE]` prints `ADP.hash(text of FILE)`, and
`["adp.js", "classify", BASE, LIVE, INCOMING]` prints `ADP.classify` of three JSON files. Two more boot the runtime on a test host (an `adp-host/1`
provider with an in-memory document store, `fetch` serving the page folder DIR, the user `agent-a` who can edit, or `viewer-1` who cannot when the last
argument is `viewer`); STATE.json is `{docs: {"collection/id": data}, provider?: "invalid", seedFiles?: false}`:

- `["adp.js", "boot", DIR, STATE]` prints `{host, seeded, writes: ["set collection/id", ...] in call order, docs: [the paths in the store]}`;
- `["adp.js", "config-set", DIR, STATE, SWITCH, VALUE_JSON]` boots, calls `ADP.config.set(SWITCH, VALUE)` and prints `{host, seeded, result: "ok" or
  "error: <message>", value: ADP.config.get(SWITCH), writes, config: config/current, changes: the changes/d-<ms> docs}`.

**Isolation.** Each vector runs in a fresh scratch folder (also the working directory) with an environment built for it, not inherited: `ADP_HOME`
set to `<scratch>/home` (so tests never read or write the user's `~/.adp`), a `PATH` of the folders that hold `node` and `git` plus the system
default, and a UTF-8 locale. The parent environment is not inherited. A reimplemented `adp.py` reads `ADP_HOME` the same way (default `~/.adp`).

**Normalization** (applied to everything compared): the scratch root is replaced by `<tmp>`, and every UTC timestamp (`2026-11-20T12:13:27Z`) by
`<time>`; a proposal id (`p-<epoch ms>-<4 random>`) by `<pid>`; its change id (`d-<epoch ms>`) by `d-<ms>`; a random
version-4 UUID (a lease token) by `<uuid>`, except the zero-prefixed ones (`00000000-...`) the vectors use as artifact ids. No other normalization is applied: key sets, list order, number versus string, and exit codes must match.

## The runner

```python
# snippet: vector-runner
import glob, json, os, pathlib, re, shutil, subprocess, sys, tempfile

FENCE = '`' * 3      # three backticks, built so this block does not end itself
BLOCK = re.compile(FENCE + r'json (fixture|vector)\n(.*?)' + FENCE, re.S)
TIME = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z')
BIN = os.pathsep.join(dict.fromkeys([os.path.dirname(w) for w in map(shutil.which, ('node', 'git')) if w] + os.defpath.split(os.pathsep)))   # node, git
PID = re.compile(r'(?<![A-Za-z0-9])p-\d{13}-[a-z2-9]{4}\b')     # a proposal id: p-<epoch ms>-<4 random>
DID = re.compile(r'(?<![A-Za-z0-9])d-\d{13}\b')                  # its changes/ entry: d-<epoch ms>
UUID = re.compile(r'(?<![0-9a-f-])(?!00000000-)[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b')   # a random lease token
NODE = r'''
const fs = require('fs'), path = require('path'), vm = require('vm');
const stub = () => new Proxy(function () {}, {get: (t, k) => k === Symbol.toPrimitive ? (() => '') : k === 'then' ? undefined : stub(),
  apply: () => stub(), construct: () => stub()});
const win = {setTimeout, clearTimeout, console, crypto: globalThis.crypto, TextEncoder, Promise, document: stub(), location: {href: 'about:blank'},
  MutationObserver: function () { return stub(); }, ResizeObserver: function () { return stub(); }, requestAnimationFrame: () => 0,
  cancelAnimationFrame() {}, navigator: {userAgent: 'node'}, addEventListener() {}, removeEventListener() {}};
win.window = win;
const [op, ...a] = process.argv.slice(2), read = p => fs.readFileSync(p, 'utf8'), writes = [], docs = {};
if (op === 'boot' || op === 'config-set') {          // a host: an in-memory document store, the page folder served by fetch, an editor or a viewer
  const st = JSON.parse(read(a[1])), viewer = a[a.length - 1] === 'viewer', subs = [];
  Object.assign(docs, st.docs || {});
  const clone = d => JSON.parse(JSON.stringify(d)), snap = (p, d) => ({id: p.split('/').pop(), exists: d !== undefined, data: () => d === undefined ? undefined : clone(d)});
  const doc = p => ({get: async () => snap(p, docs[p]),
    set: async d => { writes.push('set ' + p); docs[p] = clone(d); subs.forEach(f => f(p)); },
    update: async d => { if (!(p in docs)) throw Object.assign(new Error('not-found'), {code: 'not-found'}); writes.push('update ' + p); docs[p] = Object.assign({}, docs[p], clone(d)); subs.forEach(f => f(p)); },
    onSnapshot: cb => { subs.push(q => { if (q === p) cb(snap(p, docs[p])); }); Promise.resolve().then(() => cb(snap(p, docs[p]))); return () => {}; }});
  const coll = c => { const q = {orderBy: () => q, limit: () => q, onSnapshot: cb => {
    const ks = Object.keys(docs).filter(k => k.startsWith(c + '/') && !k.slice(c.length + 1).includes('/')).sort();
    Promise.resolve().then(() => cb({docs: ks.map(k => snap(k, docs[k])), docChanges: () => ks.map(k => ({type: 'added', doc: snap(k, docs[k])}))})); return () => {}; }}; return q; };
  win.ADP_HOST = st.provider === 'invalid' ? {protocol: 'adp-host/0'} : {protocol: 'adp-host/1', connect: async () => ({id: 'test', seedFiles: st.seedFiles !== false,
    db: {doc, collection: coll}, user: {canEdit: () => !viewer, id: () => viewer ? 'viewer-1' : 'agent-a'}})};
  win.fetch = async p => { const f = path.join(a[0], String(p)), ok = fs.existsSync(f), t = ok ? read(f) : '';
    return {ok, status: ok ? 200 : 404, json: async () => JSON.parse(t), text: async () => t, headers: {get: () => 'text/plain'}}; };
}
vm.runInContext(read(process.argv[1]), vm.createContext(win));
const settle = () => new Promise(r => setTimeout(r, 50));
(async () => {
  let out;
  if (op === 'hash') out = await win.ADP.hash(read(a[0]));
  else if (op === 'classify') out = win.ADP.classify(...a.map(p => JSON.parse(read(p))));
  else {
    await win.ADP.config.ready; await settle();
    out = {host: win.ADP.host, seeded: win.ADP.seeded};
    if (op === 'boot') Object.assign(out, {writes: writes.slice(), docs: Object.keys(docs).sort()});
    else { writes.length = 0; let r = 'ok';
      try { await win.ADP.config.set(a[2], JSON.parse(a[3])); } catch (e) { r = 'error: ' + e.message; }
      await settle();
      Object.assign(out, {result: r, value: win.ADP.config.get(a[2]), writes, config: docs['config/current'] || null,
        changes: Object.keys(docs).filter(k => k.startsWith('changes/d-')).map(k => docs[k])}); }
  }
  process.stdout.write(JSON.stringify(out)); process.exit(0);
})().catch(e => { process.stderr.write(String(e)); process.exit(1); });
'''


def blocks(skills_dir):
    """Every fixture and vector in the vectors.md files under skills_dir -> ({fixture: files}, [(path, (start, end), vector)])."""
    fixtures, vectors = {}, []
    for name in sorted(os.listdir(skills_dir)):
        path = os.path.join(skills_dir, name, 'vectors.md')
        if not os.path.isfile(path): continue
        with open(path, encoding='utf-8') as f: text = f.read()
        for m in BLOCK.finditer(text):
            data = json.loads(m.group(2))
            if m.group(1) == 'fixture': fixtures[data['fixture']] = data
            else: vectors.append((path, m.span(2), data))
    return fixtures, vectors


def run(skills_dir, tools, only=None):
    """tools: {'adp.py': path, 'adp_catalog.py': path, 'adp.js': path}. -> [{vector, ok, problems, observed}] for every vector (or those in only)."""
    fixtures, vectors = blocks(skills_dir)
    results = []
    for _, _, vec in vectors:
        if only and vec['vector'] not in only: continue
        root = tempfile.mkdtemp(prefix='adpv-')
        try:
            results.append(one(vec, fixtures, tools, root))
        finally:
            shutil.rmtree(root, ignore_errors=True)
    return results


def tree(fixtures, name):
    """A fixture's files: its base's (recursively), then its own; a file set to null is removed."""
    f = fixtures.get(name)
    if f is None: return {}
    files = dict(tree(fixtures, f['base'])) if f.get('base') else {}
    for rel, content in f['files'].items():
        if content is None: files.pop(rel, None)
        else: files[rel] = content
    return files


def one(vec, fixtures, tools, root):
    def norm(s): return UUID.sub('<uuid>', DID.sub('d-<ms>', PID.sub('<pid>', TIME.sub('<time>', s.replace(os.path.realpath(root), '<tmp>').replace(root, '<tmp>')))))

    def place(s):
        def sub(m):
            name = m.group(1)
            d = os.path.join(root, name)
            if not os.path.isdir(d):
                os.makedirs(d)
                for rel, content in tree(fixtures, name).items() if name not in ('out', 'home') else ():
                    p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, 'w', encoding='utf-8', newline='') as f: f.write(content)
            return d
        return re.sub(r'\{([a-z0-9-]+)\}', sub, s)

    problems, observed = [], []
    for i, step in enumerate(vec.get('steps', [vec])):
        if 'run' in step:
            tool, *args = [place(a) for a in step['run']]
            name = step['run'][0]
            if name == 'adp.js': cmd = ['node', '-e', NODE, tools['adp.js'], *args]
            else: cmd = [sys.executable, '-I', tools[name], *args]
            env = {'ADP_HOME': os.path.join(root, 'home'), 'PATH': BIN, 'LANG': 'en_US.UTF-8'}      # hermetic: the parent environment is not inherited
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=root, env=env, timeout=60)
            got = {'exit': r.returncode}
            out = norm(r.stdout)
            if 'stdout' in step:
                try: got['stdout'] = json.loads(out)
                except ValueError: got['stdout'] = out
            if 'stdout_text' in step: got['stdout_text'] = out.rstrip('\n').split('\n') if out else []
            err = norm(r.stderr)
            if 'stderr_text' in step: got['stderr_text'] = err.rstrip('\n').split('\n') if err else []
            for rel in step.get('files_out', {}):
                p = place(rel)
                if '*' in p: p = (sorted(glob.glob(p)) + [p])[0]       # a name that holds an id: the one file that matches
                if not os.path.isfile(p): got.setdefault('files_out', {})[rel] = None; continue
                with open(p, encoding='utf-8') as f: text = norm(f.read())
                got.setdefault('files_out', {})[rel] = json.loads(text) if p.endswith('.json') else text
            for k in ('exit', 'stdout', 'stdout_text', 'stderr_text', 'files_out'):
                if k in step and step[k] != got.get(k): problems.append(f'step {i}: {k} differs: expected {step[k]!r}, got {got.get(k)!r}; stderr: {norm(r.stderr)[-400:]}')
            observed.append(got)
        if 'copy' in step:                                              # a change between runs: dst becomes a copy of src
            src, dst = (place(x) for x in step['copy'])
            shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
            observed.append({'copy': step['copy']})
        if 'same_tree' in step:
            a, b = (place(x) for x in step['same_tree'])
            for d, _, names in os.walk(a):
                for n in names:
                    pa = os.path.join(d, n); pb = os.path.join(b, os.path.relpath(pa, a))
                    if not os.path.isfile(pb) or pathlib.Path(pa).read_bytes() != pathlib.Path(pb).read_bytes(): problems.append(f'step {i}: {os.path.relpath(pa, a)} differs')
            observed.append({'same_tree': step['same_tree']})
    return {'vector': vec['vector'], 'ok': not problems, 'problems': problems, 'observed': observed}
```

Run it against a rebuild:

```python
# snippet: run-the-vectors   (needs vector-runner above)
results = run('<this plugin>/skills', {'adp.py': 'my/adp.py', 'adp_catalog.py': 'my/adp_catalog.py', 'adp.js': 'my/adp.js'})
for r in results:
    print('ok  ' if r['ok'] else 'FAIL', r['vector'], *r['problems'], sep='\n    ' if r['problems'] else ' ')
print(sum(r['ok'] for r in results), 'of', len(results), 'vectors pass')
```

It needs Python 3 and, for the `adp.js` vectors, Node 18 or later.

## Rules

- Implement strictly against the contracts and vectors.
- One file per tool, standard library only, no network access at runtime.
- A vector that fails is a bug in the reimplementation, never a reason to edit the vector.
- Report which scope-table rows the reimplementation covers; everything else is unimplemented.
