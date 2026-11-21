---
name: adp-minimal-rebuild
description: "Build the ADP tools (adp.py, adp_catalog.py, adp.js) from the code fragments in the adp-minimal skills, and check the build: the fragment format, the assembler and its checks, the fixture and vector format, normalization, and the vector runner. Use when the user wants the ADP tools built from this plugin, asks how a fragment becomes part of a tool, or how a build is tested."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Building the ADP tools

The ADP (Artifacts Done Properly) tools are written in these skills. Each skill explains one topic and holds the code for it as **fragments**:
fenced blocks placed under the prose that explains them. The **assembler** collects the fragments and writes the three tools: the CLI
(`adp.py`), the catalog tool (`adp_catalog.py`) and the browser runtime (`adp.js`). The **vectors** (a command, its inputs and what it must
return), in the `vectors.md` beside each `SKILL.md`, then check the build.

## Fragments

A fragment is a fenced `python` or `js` block whose first lines are a header, written as comments (`#` in Python, `//` in JavaScript):

```text
# ---
# id: parts.manifest
# tool: adp.py
# section: parts
# order: 150
# needs: [parts.regions]
# tests: [manifest-dir, manifest-single]
# sha: 3f2a9c1d0b7e
# ---
def manifest(path): ...
```

| Field | Meaning |
|---|---|
| `id` | `<section>.<name>`, unique across the plugin |
| `tool` | the file the fragment goes into: `adp.py`, `adp_catalog.py` or `adp.js` |
| `section` | one of the tool's sections. Each section belongs to one skill and has a range of `order` values |
| `order` | the fragment's position in the tool; unique per tool, inside its section's range |
| `needs` | the fragments this one builds on: earlier fragments of the same tool |
| `tests` | the vectors that exercise the fragment |
| `sha` | the first 12 hex characters of the SHA-256 of the body (the lines under the header). The assembler writes it; never edit it by hand |

A block without the header is an illustration and is never assembled.

Each tool's first fragment is its **preamble**, in [adp-minimal](../adp-minimal/SKILL.md). Its header carries one more field, `sections`,
which lists the tool's sections as `name first-last skill`. A command registers itself where it is defined (`@cmd('check')` in `adp.py`), so
no fragment holds a list of commands.

| Tool | Sections, in order | Skills |
|---|---|---|
| `adp.py` | `core`, `parts`, `payloads`, `hosts`, `protocol`, `delta`, `packing`, `themes`, `kit`, `new`, `catalog`, `cli` | the skill named after each section; `core` and `cli` are in [adp-minimal](../adp-minimal/SKILL.md), `new` in [adp-minimal-new-artifact](../adp-minimal-new-artifact/SKILL.md) |
| `adp_catalog.py` | `core`, `authoring`, `catalog` | [adp-minimal](../adp-minimal/SKILL.md), [adp-minimal-kit-authoring](../adp-minimal-kit-authoring/SKILL.md), [adp-minimal-catalog](../adp-minimal-catalog/SKILL.md) |
| `adp.js` | `core`, `hosts`, `runtime`, `cli` | [adp-minimal](../adp-minimal/SKILL.md), [adp-minimal-hosts](../adp-minimal-hosts/SKILL.md), [adp-minimal-runtime](../adp-minimal-runtime/SKILL.md) |

The parts of `adp.js` that draw into the DOM (content painting, the "What changed" panel, anchors, the self-check) have no vectors: checking
them needs a browser.

## Fixtures and vectors

A **fixture** is a named file tree, written as a fenced block whose info string is `json fixture`. With `"base": "<fixture>"` it starts from that
fixture's files; its own files override them, and a file set to `null` is removed:

```json
{"fixture": "example", "files": {"index.html": "<!-- part:a --><p data-part=\"a\">A</p><!-- /part:a -->\n"}}
```

A file's value is its text. Three other forms build what text cannot: `{"link": "target"}` is a symbolic link to `target`, `{"fill": N}` is
a file of N bytes, and `{"base64": "..."}` is a file of those bytes. In a command, in `stdin` and in a fixture file written after it, `<pid>`
stands for the proposal id the last step printed.

A **vector** is a fenced block whose info string is `json vector`. It runs one command (or several `steps`) and states what must come back:

| Field | Meaning |
|---|---|
| `vector` | its name |
| `skip` | a reason. The vector is kept but not run, and no fragment has to name it |
| `run` | the command: first the tool (`adp.py`, `adp_catalog.py`, or `adp.js` for the browser runtime), then the arguments. `{name}` is the fixture `name` written to a fresh folder; `{out}` is an empty scratch folder; `{home}` is the vector's `ADP_HOME` |
| `stdin` | the text the command reads from standard input, with the same `{name}` placeholders; empty when absent |
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
default, and a UTF-8 locale. The parent environment is not inherited. `adp.py` reads `ADP_HOME` the same way (default `~/.adp`).

**Normalization** (applied to everything compared): the scratch root is replaced by `<tmp>`, and every UTC timestamp (`2026-11-20T12:13:27Z`) by
`<time>`; a proposal id (`p-<epoch ms>-<4 random>`) by `<pid>`; its change id (`d-<epoch ms>`) by `d-<ms>`; a random
version-4 UUID (a lease token) by `<uuid>`, a git commit id (40 hex characters) by `<commit>`, and the SHA-256 of the `adp.js` under test (whole, or its first 12 characters) by
`<adp.js sha>` and `<adp.js sha12>`, except the zero-prefixed ones (`00000000-...`) the vectors use as artifact ids. No other normalization is applied: key sets, list order, number versus string, and exit codes must match.

## The runner

```python
# snippet: vector-runner
import base64, glob, hashlib, json, os, pathlib, re, shutil, subprocess, sys, tempfile

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
    """tools: {'adp.py': path, 'adp_catalog.py': path, 'adp.js': path}. -> [{vector, ok, problems, observed}] for every vector (or those in only).
    A vector with a `skip` field is not run: its row carries `skip` and `ok: None`."""
    fixtures, vectors = blocks(skills_dir)
    results = []
    for _, _, vec in vectors:
        if only and vec['vector'] not in only: continue
        if vec.get('skip'): results.append({'vector': vec['vector'], 'skip': vec['skip'], 'ok': None, 'problems': [], 'observed': []}); continue
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
    js = hashlib.sha256(pathlib.Path(tools['adp.js']).read_bytes()).hexdigest()          # the runtime's own hash, which a page may quote

    def norm(s): return re.sub(r'\b[0-9a-f]{40}\b', '<commit>', UUID.sub('<uuid>', DID.sub('d-<ms>', PID.sub('<pid>', TIME.sub('<time>', s.replace(os.path.realpath(root), '<tmp>').replace(root, '<tmp>').replace(js, '<adp.js sha>').replace(js[:12], '<adp.js sha12>'))))))

    last = ['']                     # the proposal id the last step printed: a later step names it as <pid>

    def place(s):
        def sub(m):
            name = m.group(1)
            d = os.path.join(root, name)
            if not os.path.isdir(d):
                os.makedirs(d)
                for rel, content in tree(fixtures, name).items() if name not in ('out', 'home') else ():
                    p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
                    if isinstance(content, dict) and 'link' in content: os.symlink(content['link'], p); continue
                    data = content.replace('<pid>', last[0]).encode() if isinstance(content, str) else b'x' * content['fill'] if 'fill' in content else base64.b64decode(content['base64'])
                    with open(p, 'wb') as f: f.write(data)
            return d
        return re.sub(r'\{([a-z0-9-]+)\}', sub, s.replace('<pid>', last[0]))

    problems, observed = [], []
    for i, step in enumerate(vec.get('steps', [vec])):
        if 'run' in step:
            tool, *args = [place(a) for a in step['run']]
            name = step['run'][0]
            if name == 'adp.js': cmd = ['node', '-e', NODE, tools['adp.js'], *args]
            else: cmd = [sys.executable, '-I', tools[name], *args]
            env = {'ADP_HOME': os.path.join(root, 'home'), 'PATH': BIN, 'LANG': 'en_US.UTF-8'}      # hermetic: the parent environment is not inherited
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=root, env=env, timeout=60, input=place(step.get('stdin', '')))
            got = {'exit': r.returncode}
            last[:] = PID.findall(r.stdout)[-1:] or last
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

## The assembler

The assembler reads every `SKILL.md` under the skills folder, checks the fragments and writes the build:

| Check | A problem line is printed when |
|---|---|
| checksum | a fragment's `sha` is not the hash of its body. `seal` names the skills whose `sha` lines are rewritten instead |
| repeated | two fragments share an `id`, a position (`tool` and `order`) or a body; or one tool defines a top-level name twice |
| placement | a fragment's `section` is not declared by its tool, belongs to another skill, or its `order` is outside the section's range |
| missing link | a `needs` id is not an earlier fragment of the same tool, a `tests` name is not a vector, or a Python fragment calls a name its tool never defines |
| chain | a fragment's `needs` do not lead back to its tool's preamble |
| builds | `adp.py` or `adp_catalog.py` does not parse, or `node --check` rejects `adp.js` |
| coverage (`final` only) | a vector without a `skip` field is named by no fragment |

Each problem line starts with the fragment's `id` and its skill. The three files are written even when a check fails, so a fragment in progress
can be run. `adp.js` gets no name scan: `node --check` is its only build check.

```python
# snippet: assemble   (needs vector-runner above)
import ast, builtins, hashlib

TOOLS = {'adp.py': 'scripts/adp.py', 'adp_catalog.py': 'scripts/adp_catalog.py', 'adp.js': 'assets/adp.js'}
FRAG = re.compile('^' + FENCE + r'(?:python|js)\n((?:#|//) ---\n.*?\n(?:#|//) ---)\n(.*?)\n' + FENCE + '$', re.S | re.M)


def header(text):
    """A fragment's header lines -> {key: value, or [values] for a bracketed list}. A line without a key continues the value above it."""
    h, key = {}, None
    for line in text.split('\n')[1:-1]:
        line = re.sub(r'^(#|//) ?', '', line)
        m = re.match(r'(\w+): *(.*)', line)
        if m: key = m.group(1); h[key] = m.group(2).strip()
        else: h[key] += ' ' + line.strip()
    return {k: [x.strip() for x in v[1:-1].split(',') if x.strip()] if v.startswith('[') else v for k, v in h.items()}


def assemble(skills_dir, out, final=False, seal=()):
    """Check every fragment under skills_dir and write the tools and the templates under out. -> ({tool: {lines, fragments, sha256}}, [problems])"""
    frags, bad = [], []
    say = lambda f, kind, msg: bad.append(f"{f['id']} ({f['skill']}): {kind}: {msg}")
    for skill in sorted(os.listdir(skills_dir)):
        path = os.path.join(skills_dir, skill, 'SKILL.md')
        if not os.path.isfile(path): continue
        text = old = pathlib.Path(path).read_text(encoding='utf-8')
        for m in reversed(list(FRAG.finditer(old))):
            f = {'needs': [], 'tests': [], **header(m.group(1)), 'body': m.group(2), 'skill': skill}
            f['order'], sha = int(f['order']), hashlib.sha256(f['body'].encode()).hexdigest()[:12]
            if f.get('sha') != sha and skill in seal: text = text[:m.start(1)] + re.sub(r'sha:.*', 'sha: ' + sha, m.group(1)) + text[m.end(1):]
            elif f.get('sha') != sha: say(f, 'checksum', f"sha says {f.get('sha')}, the body is {sha}")
            frags.append(f)
        if text != old: pathlib.Path(path).write_text(text, encoding='utf-8')
    fixtures, vectors = blocks(skills_dir)
    skipped = {v['vector']: v.get('skip') for _, _, v in vectors}
    frags.sort(key=lambda f: (f['tool'], f['order']))
    seen, report = {}, {}
    for f in frags:
        for what, key in (('id', f['id']), ('position', (f['tool'], f['order'])), ('body', f['body'])):
            if key in seen: say(f, 'repeated', f'same {what} as {seen[key]}')
            seen.setdefault(key, f['id'])
    for tool, rel in TOOLS.items():
        mine = [f for f in frags if f['tool'] == tool]
        entry, sections, earlier, rooted = mine[0], {}, set(), set()        # the preamble declares the tool's sections
        for s in entry['sections']:
            name, span, owner = s.split(); sections[name] = (*map(int, span.split('-')), owner)
        for f in mine:
            lo, hi, owner = sections.get(f['section'], (0, -1, None))
            if owner != f['skill'] or not lo <= f['order'] <= hi: say(f, 'placement', f"section {f['section']} is orders {lo}-{hi} of {owner}")
            for n in f['needs']:
                if n not in earlier: say(f, 'missing link', f'needs {n}, which is not an earlier fragment of {tool}')
            for t in f['tests']:
                if t not in skipped: say(f, 'missing link', f'tests {t}, which is not a vector')
            if f is entry or rooted & set(f['needs']): rooted.add(f['id'])
            else: say(f, 'chain', f"its needs do not lead back to {entry['id']}")
            earlier.add(f['id'])
        src, starts = '', []
        for f in mine: starts.append((src.count('\n') + 1, f)); src += f['body'] + '\n\n\n'
        src = src.rstrip('\n') + '\n'
        at = lambda line: [f for n, f in starts if n <= line][-1]
        path = os.path.join(out, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
        pathlib.Path(path).write_text(src, encoding='utf-8')
        report[tool] = {'lines': sum(f['body'].count('\n') + 1 for f in mine), 'fragments': len(mine), 'sha256': hashlib.sha256(src.encode()).hexdigest()[:12]}
        if tool.endswith('.js'):
            r = subprocess.run(['node', '--check', path], capture_output=True, text=True, env={'PATH': BIN})
            if r.returncode: say(at(int(re.search(r':(\d+)\n', r.stderr).group(1))), 'builds', r.stderr.strip().split('\n\n')[1].split('\n')[0])
            continue
        try: mod = ast.parse(src)
        except SyntaxError as e: say(at(e.lineno), 'builds', f'{e.msg}: {(e.text or "").strip()}'); continue
        nodes, top = list(ast.walk(mod)), set()
        known = set(dir(builtins)) | {n.id for n in nodes if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)} \
            | {n.name for n in nodes if isinstance(n, (ast.FunctionDef, ast.ClassDef))} | {n.arg for n in nodes if isinstance(n, ast.arg)} \
            | {(n.asname or n.name).split('.')[0] for n in nodes if isinstance(n, ast.alias)}
        for n in nodes:
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id not in known: say(at(n.lineno), 'missing link', f'calls {n.func.id}, which {tool} never defines')
        for n in mod.body:
            for name in [n.name] if isinstance(n, (ast.FunctionDef, ast.ClassDef)) else [t.id for t in getattr(n, 'targets', []) if isinstance(t, ast.Name)]:
                if name in top: say(at(n.lineno), 'repeated', f'{name} is already defined in {tool}')
                top.add(name)
    if final:
        named = {t for f in frags for t in f['tests']}
        bad += [f'{v}: coverage: no fragment names this vector' for v, skip in skipped.items() if not skip and v not in named]
    for name in fixtures:
        for rel, content in tree(fixtures, name).items() if name.startswith('template-') else ():
            p = os.path.join(out, 'templates', name[len('template-'):], rel); os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8', newline='') as fh: fh.write(content)
    return report, bad
```

The build is laid out as the tools expect it: `scripts/adp.py`, `scripts/adp_catalog.py`, `assets/adp.js` and `templates/<name>/` (each
`template-<name>` fixture, which is what `adp.py new` copies).

## Build and check

Save the three blocks (`vector-runner`, `assemble`, then this one) in that order as `build.py`, and run `python3 build.py SKILLS_DIR BUILD_DIR`:

```python
# snippet: run-the-vectors   (needs vector-runner and assemble above)
skills, build = sys.argv[1:3]
report, problems = assemble(skills, build, final=True)
print(json.dumps(report), *problems, sep='\n')
results = run(skills, {tool: os.path.join(build, rel) for tool, rel in TOOLS.items()})
ran = [r for r in results if not r.get('skip')]
for r in ran:
    if not r['ok']: print('FAIL ' + r['vector'], *r['problems'], sep='\n    ')
print(f"{sum(r['ok'] for r in ran)} of {len(ran)} vectors pass, {len(results) - len(ran)} skipped")
sys.exit(1 if problems or not all(r['ok'] for r in ran) else 0)
```

It prints one line per tool (its lines, fragments and checksum), any assembler problem, each failing vector, and the totals. It needs
Python 3.9 or later and Node 18 or later.

## Rules

- A tool changes only through its fragments: edit the fragment in its skill, seal it, assemble, run its vectors.
- One file per tool, standard library only, no network access at runtime.
- A fragment holds what a road step or a vector needs. A refusal is written only when a vector asserts it.
- When a vector fails, the fragment is wrong. A vector's expected output is recorded from the build only after a reviewer has read the change.
