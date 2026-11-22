---
name: adp-delta
description: "Explains the ADP delta and inbox: the base, live and incoming manifests; classification into new, ours, theirs, applied, retired and held, and the closure over parents and requires; the loop (export, classify, propose, ack) and the gate hook; local state in DIR.adp/; the incoming/PID proposal; applying and declining in the page's inbox. Use when the user asks how ADP merges concurrent work, what held or theirs means, what a proposal is, or why propose or the gate refused."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The delta, the proposal and the inbox

An ADP page can be changed concurrently from the page itself (the inbox) and from agent sessions through `adp.py`. ADP does not let the last
publish win: it compares three states, sorts every part and file into a class, merges what does not conflict and holds the rest.

The code blocks with a header are the fragments of `adp.py` this skill owns; their vectors are in [vectors.md](vectors.md).

## The three states

| State | Meaning |
|---|---|
| **base** | the last state both sides agreed on: made equal to live by the first export and by every export that merges cleanly, and to the proposal's work by `ack --proposal` once the page applied it |
| **live** | the record and the published page, as the last export read them |
| **incoming** | the side being merged: the agent's local folder (**work**, below), or a proposal when the inbox classifies it |

**work** is the local folder `DIR`. When `adp.py` classifies, work is the incoming side.

Each state is a manifest: `{parts: {id: hash}, files: {path: hash}}`, optionally with `parents`, `requires` and, on incoming, `retired {id: reason}`.
Every hash is the first 12 hex characters of a SHA-256.

## The classification

For each id, `b`, `l` and `i` are its hashes in base, live and incoming (`-` when absent):

| Class | Rule | Meaning |
|---|---|---|
| `new` | b `-`, l `-`, i present | only incoming has it |
| `ours` | i present, i != b, l = b | incoming changed it; live did not |
| `theirs` | i = b, l != b; or b `-`, l present, i `-` | live changed or added it; incoming did not |
| `applied` | l = i, l != b (including both absent) | live and incoming already agree |
| `retired` | b present, l present, i `-`, id in incoming's `retired` | incoming deletes it and gives a reason |
| `held` | any other change | both sides changed it differently, or incoming deletes it without a reason |
| (none) | b = l = i | unchanged; left out of the output |

One id:

```python
# ---
# id: delta.classify-id
# tool: adp.py
# section: delta
# order: 400
# needs: [core.cli]
# sha: 93f923a75c1a
# ---
def classify_id(key, b, l, i, retired):
    """key: the part id or file path; b, l, i: its hash in base, live and incoming, or None when absent; retired: incoming's retired ids."""
    if b is None:
        if l is None:
            return 'new' if i is not None else None
        if i is None:
            return 'theirs'
        return 'applied' if i == l else 'held'
    if i is None:
        if l is None:
            return 'applied'
        return 'retired' if key in retired else 'held'
    if l == b:
        return 'ours' if i != b else None
    if i == b:
        return 'theirs'
    return 'applied' if i == l else 'held'
```

Then a **closure**: an id classified `new`, `ours` or `retired` becomes `held` if it touches a held id, repeated until no id changes class. Two ids
touch when one is the other's parent (`parents`), or when one is a file in `requires[c]` and the other is `c` or a descendant `c.*`. `parents` and
`requires` are taken from all three manifests. The closure keeps a file from being proposed while a part it depends on is held.

Parts and files share one id space, and every class lists its ids sorted, in `adp.py` and in `adp.js` (`ADP.classify`) alike. `held` lists
`{id, base, live, incoming}`, `null` for an absent hash. `adp.py classify BASE.json LIVE.json INCOMING.json` prints the result; a manifest
saved as an ArtifactData document (`{id, data, version}`) is read from its `data`, and `retired` may be a list of ids.

```python
# ---
# id: delta.classify
# tool: adp.py
# section: delta
# order: 410
# needs: [delta.classify-id, protocol.pins]
# tests: [classify-every-class, loop-refusals]
# sha: b4e34ed32639
# ---
CLASSES = ('new', 'ours', 'theirs', 'applied', 'held', 'retired')


def touches(x, y, parents, requires):
    under = lambda f, p: any(f in fs and (p == c or p.startswith(c + '.')) for c, fs in requires.items())
    return parents.get(x) == y or parents.get(y) == x or under(x, y) or under(y, x)


def classify(base, live, incoming):
    """Three manifests -> {new, ours, theirs, applied, held: [{id, base, live, incoming}], retired}"""
    ids = lambda m: {**(m.get('parts') or {}), **(m.get('files') or {})}
    links = lambda k: {x: v for m in (base, live, incoming) for x, v in (m.get(k) or {}).items()}
    bs, ls, js, retired, parents, requires = ids(base), ids(live), ids(incoming), incoming.get('retired') or {}, links('parents'), links('requires')
    out = {c: [] for c in CLASSES}
    for x in sorted({*bs, *ls, *js}):
        c = classify_id(x, bs.get(x), ls.get(x), js.get(x), retired)
        if c: out[c].append(x)
    moved = True
    while moved:
        moved = False
        for c in ('new', 'ours', 'retired'):
            for x in [x for x in out[c] if any(touches(x, y, parents, requires) for y in out['held'])]:
                out[c].remove(x); out['held'].append(x); moved = True
    out['held'] = [{'id': x, 'base': bs.get(x), 'live': ls.get(x), 'incoming': js.get(x)} for x in sorted(out['held'])]
    return out


@cmd('classify')
def classify_cmd(a):
    """classify BASE.json LIVE.json INCOMING.json    sort every part and file into new, ours, theirs, applied, held and retired"""
    if len(a) != 3: sys.exit(usage('classify'))
    emit(classify(*(unwrap(read_json(p)) for p in a[:3])))
```

## The loop

```
adp.py export: live to local  ->  classify  ->  adp.py propose: local to live  ->  ack  ->  gate
```

The loop keeps its state beside the folder, in `DIR.adp/`: `state.json`, `listing.json` and `docs.json` (the reads), `incoming/files/` (the live
files), `incoming/content/` (the live copy, one `<id>.html` per `content` doc), `propose-<pid>.json` and its batch folder, and a git repository, `DIR.adp/repo`, with branches `base`, `live` and `work`. Each holds a
state as a tree: the files under `files/`, each part's hash as `db/parts/<id>.json`, and each part's copy as `content/<id>.html`. `$ADP_HOME/artifacts.json` (default `~/.adp`) maps each
exported url to `{dir, name}`, so the gate and the ack hook find the state of the artifact a call writes to.

```python
# ---
# id: delta.state
# tool: adp.py
# section: delta
# order: 420
# needs: [delta.classify, core.io]
# sha: 80b6c816965e
# ---
import base64, hashlib, random, shutil, subprocess, time

INBOX = ('held', 'unacked', 'pending_replies')        # state['incoming'] also keeps `proposed` and `acked`
LOOP_READS = ('manifest', 'parts', 'content', 'changes', 'config', 'requests', 'presence', 'agents', 'decisions', 'incoming')


def adp_dir(d):
    return d.rstrip('/') + '.adp'


def loop_state(d):
    p = os.path.join(adp_dir(d), 'state.json')
    return read_json(p) if os.path.isfile(p) else {}


def save_loop(d, st):
    Path(adp_dir(d), 'state.json').write_text(json.dumps(st, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')


def registry():
    p = os.path.join(ADP_HOME, 'artifacts.json')
    return read_json(p) if os.path.isfile(p) else {}


def managed(url):
    """The folder the registry, {url: {dir, name}}, gives for a url; None when ADP does not manage it."""
    return (registry().get(url) or {}).get('dir')


def exported(d):
    """The state of the last export, or None after printing that there is none (the caller exits 2)."""
    st = loop_state(d)
    if not st: emit({'error': 'no export yet', 'next': f'adp.py export {d} --url URL'})
    return st or None


def hook_input(a, name):
    """The JSON in the file after option `name` (not JSON: exit 1), else on stdin (not JSON: ValueError)."""
    if not opt(a, name): return json.loads(sys.stdin.read() or '{}')
    try: return read_json(opt(a, name))
    except ValueError as e: sys.exit(f'{name}: {opt(a, name)} is not JSON: {e}')
```

`commit_tree` makes a branch's tree exactly the given files and commits it. `merge3` merges live into work over the `base` branch, never the
merge base git would compute, and returns the merged tree and its conflict lines (none when clean). Commit ids depend on the clock and are never printed.

```python
# ---
# id: delta.repo
# tool: adp.py
# section: delta
# order: 430
# needs: [delta.state, parts.markers]
# sha: a16fb9f13b23
# ---
GIT_ENV = {'PATH': os.pathsep.join(filter(None, [os.path.dirname(shutil.which('git') or ''), os.defpath])), 'LANG': 'C',
           'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1'}     # git gets these and nothing else of the caller's environment


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, '-c', 'user.name=adp', '-c', 'user.email=adp@localhost', '-c', 'commit.gpgsign=false', *args],
                          capture_output=True, text=True, env=GIT_ENV)


def loop_repo(d):
    repo = os.path.join(adp_dir(d), 'repo')
    if not os.path.isdir(os.path.join(repo, '.git')):
        os.makedirs(repo, exist_ok=True)
        git(repo, 'init', '-q', '-b', 'base'); git(repo, 'commit', '-q', '--allow-empty', '-m', 'root')
        git(repo, 'branch', 'live'); git(repo, 'branch', 'work')
    return repo


def loop_tree(folder, m, content):
    """A state as a tree: the files of `m` read from `folder`, each part's hash, and each part's copy {id: html}."""
    tree = {'files/' + p: Path(folder, p).read_bytes() for p in m['files'] if Path(folder, p).is_file()}
    tree.update({f'db/parts/{p}.json': json.dumps({'hash': h}).encode() for p, h in m['parts'].items() if not p.startswith(REST)})
    tree.update({f'content/{k}.html': h.encode() for k, h in content.items()})
    return tree


def commit_tree(repo, branch, tree, msg):
    git(repo, 'checkout', '-q', '-f', branch); git(repo, 'rm', '-q', '-r', '--ignore-unmatch', '.')
    for p, b in tree.items():
        Path(repo, p).parent.mkdir(parents=True, exist_ok=True); Path(repo, p).write_bytes(b)
    git(repo, 'add', '-A'); git(repo, 'commit', '-q', '--allow-empty', '-m', msg)
    return git(repo, 'rev-parse', 'HEAD').stdout.strip()


def merge3(repo):
    """-> (the merged tree, its conflict lines: [] when clean)"""
    r = git(repo, 'merge-tree', '--write-tree', '--merge-base=base', 'work', 'live')
    lines = r.stdout.splitlines()
    return (lines[0] if lines else ''), [] if r.returncode == 0 else [x for x in lines if x.startswith('CONFLICT')] or [r.stderr.strip() or 'merge failed']
```

### `adp.py export DIR`

`adp.py export DIR --url URL [--files-listing F] [--docs D] [--version V]` reads live in three passes. With no listing saved (default
`DIR.adp/listing.json`) it prints `{reads, then}`: one `Artifact` list call and where to save its result. With the listing but no records (default
`DIR.adp/docs.json`) it prints `{reads, save_docs_to, docs_shape, then}`: an `Artifact` read of every listed file into `DIR.adp/incoming/files`,
and one `ArtifactData` list per record collection, to be saved as `{collection: [{id, data, version}]}`. Both exit 2: run the reads, then the
command in `then`.

The listing is read as JSON (`{files: [...]}` or a list, with `sha256` or `sha`) or as the list result the tool prints (`- "path"  type  N bytes`
rows; a text with no row exits 1). The seed (`seed.json`, `seed/`) and references to other artifacts (rows with `artifact`, kept in the state
as `refs`) are left out: they are not part of the page, and work leaves them out too. The records file may list each collection's documents
(`{id or doc_id, data or the fields inline, version}`, an id read after its last `/`) or map them by id. The Artifact tool returns `index.html`
inside its own document skeleton; export strips it before hashing, so live compares with the folder.

The page's copy is its `content` docs on live, and on work `DIR/content/<id>.html`, else the `html` of each entry in `DIR/content.js`.

```python
# ---
# id: delta.listing
# tool: adp.py
# section: delta
# order: 440
# needs: [delta.state, parts.manifest, protocol.manifest-doc]
# sha: 3bf494cab51a
# ---
LIST_ROW = re.compile(r'^- "(.+?)"\s+\S+\s+(\d+) bytes', re.M)
SKELETON = re.compile(rb'^<!doctype html><html><head><meta charset=utf8>.*?</style></head><body>\n?(.*?)\n?</body></html>\s*$', re.S | re.I)


def read_listing(path):
    """-> [{path, sha256 ('' when the listing is text), bytes, ref: {artifact, ver} or None}], the seed left out"""
    text = Path(path).read_text(encoding='utf-8')
    if text.lstrip()[:1] in '{[':
        rows = json.loads(text); rows = rows.get('files', rows) if isinstance(rows, dict) else rows
    else:
        rows = [{'path': p, 'bytes': int(n)} for p, n in LIST_ROW.findall(text)]
        if not rows: sys.exit(f'{path}: no file rows (- "path"  type  N bytes) and not JSON: save the Artifact list result as it came')
    return [{'path': x['path'], 'sha256': x.get('sha256') or x.get('sha') or '', 'bytes': x.get('bytes') or x.get('size') or 0,
             'ref': {'artifact': x['artifact'], 'ver': x.get('ver', '')} if x.get('artifact') else None}
            for x in rows if x['path'] != 'seed.json' and not x['path'].startswith('seed/')]


def bare_page(b):
    m = SKELETON.match(b)
    return m.group(1) if m else b


def loop_docs(path):
    """{coll: [{id or doc_id, data or its fields inline, version}]} or {coll: {id: doc}} -> {coll: {id: {data, version}}}"""
    out = {}
    for c, xs in read_json(path).items():
        for k, x in xs.items() if isinstance(xs, dict) else ((x.get('id') or x.get('doc_id') or '', x) for x in xs):
            data = x['data'] if isinstance(x.get('data'), dict) else {f: v for f, v in x.items() if f not in ('id', 'doc_id', 'version')}
            out.setdefault(c, {})[str(k).split('/')[-1]] = {'data': data, 'version': x.get('version')}
    return out


def work_of(d, refs):
    """DIR -> (its manifest without the references and content/, its copy {part id: html})"""
    m, out = manifest(d), lambda f: f in refs or f.startswith('content/')
    m = {'parts': {p: h for p, h in m['parts'].items() if not out(m['part_file'].get(p, ''))},
         'files': {f: h for f, h in m['files'].items() if not out(f)}, 'parents': m['parents']}
    copy = {p.stem: p.read_text(encoding='utf-8') for p in sorted(Path(d, 'content').glob('*.html'))}
    return m, copy or {k: v.get('html', '') for k, v in content_of(d).items()}


def live_copy(ad):
    """The live copy, {part id: html}, as the last export saved the content docs."""
    return {p.stem: p.read_text(encoding='utf-8') for p in sorted(Path(ad, 'incoming', 'content').glob('*.html'))}
```

With both reads saved, export classifies work against base and live and prints `{report, merged, state, next}`; it exits 0.

- **The first export is the import.** Base and work start from live, and a `DIR` that is missing or holds only dotfiles is filled with the live files. A `theirs` file that was not saved under `incoming/files` is not copied.
- **Nothing held:** git merges live into work over base. Clean: the merge is committed on `work`, every `theirs` file is copied into `DIR`, the
  merged copy into `DIR/content/` when that folder exists, base moves to live, and `merged` is `true`. A conflict (two edits of one copy)
  adds `merge_conflict` with git's lines and holds each conflicting path.
- **Something held:** `DIR` and base stay as they are, and `merged` is `false`.
- `next` is `held: N; show both versions to the owner, nobody writes`, `adp.py propose DIR --by NAME --summary S`, or `clean: nothing to send`.

The state keeps what the next steps need: the live version and manifest, each record's version (the pins the gate checks), each file's SHA-256
(the `ifMatch` of a proposal), the references, each copy as work first had it (`src_copy`), the held ids, the proposals this folder sent and their status, and the `requests` still waiting for a reply.
It also keeps `schema: adp-state/1`, the folder's `name`, `capabilities`, `exported_at`, `catalog {url, vermap}` and the `commits` of live and work.
Beside it, in `incoming/`, export writes what it read: `files.json` (the listing's rows, `[{path, sha256, bytes, ref}]`), `live-manifest.json`, `report.json`, and each
record but the copy as `db/<collection>/<id>.json`.

```python
# ---
# id: delta.export
# tool: adp.py
# section: delta
# order: 450
# needs: [delta.repo, delta.listing, parts.manifest]
# tests: [loop-export-asks-for-its-reads, loop-the-first-export-is-the-import, loop-theirs-lands-in-the-folder, loop-both-sides-changed-is-held, loop-export-reads-every-input-shape, loop-content-merges-over-base, loop-refusals, loop-import-and-unsaved-reads]
# sha: 2ec086a54c1f
# ---
CONFLICT = re.compile(r'CONFLICT \([^)]*\): (?:Merge conflict in )?(\S+)')


@cmd('export')
def loop_export(a):
    """export DIR --url URL [--files-listing F] [--docs D] [--version V]    read live, merge it into work, take what only live changed"""
    if len(bare(a)) != 1 or not opt(a, '--url'): sys.exit(usage('export'))
    d, url = bare(a)[0], opt(a, '--url').rstrip('/')
    ad = adp_dir(d); inc, cc = os.path.join(ad, 'incoming', 'files'), os.path.join(ad, 'incoming', 'content')
    fl, dd = opt(a, '--files-listing', os.path.join(ad, 'listing.json')), opt(a, '--docs', os.path.join(ad, 'docs.json'))
    then = f'adp.py export {d} --url {url} --files-listing {fl}'
    if not os.path.isfile(fl):
        emit({'reads': [{'tool': 'Artifact', 'action': 'list', 'scope': 'files', 'url': url, 'save_to': os.path.abspath(fl),
                         'save': 'the result as the tool returned it, text or JSON'}], 'then': then}); return 2
    rows = read_listing(fl)
    listed, refs = {x['path']: x['sha256'] for x in rows if not x['ref']}, {x['path']: x['ref'] for x in rows if x['ref']}
    if not os.path.isfile(dd):
        emit({'reads': [{'tool': 'Artifact', 'action': 'read', 'url': url, 'paths': sorted(listed), 'out_dir': os.path.abspath(inc)}]
              + [{'tool': 'ArtifactData', 'action': 'list', 'url': url, 'collection': c} for c in LOOP_READS],
              'save_docs_to': os.path.abspath(dd), 'docs_shape': '{collection: [{id, data, version}, ...]}', 'then': f'{then} --docs {dd}'}); return 2
    docs = loop_docs(dd)
    if Path(inc, 'index.html').is_file(): Path(inc, 'index.html').write_bytes(bare_page(Path(inc, 'index.html').read_bytes()))
    files = {p: hashlib.sha256(Path(inc, p).read_bytes()).hexdigest() if Path(inc, p).is_file() else sha for p, sha in listed.items()}
    for sub in ('content', 'db'): shutil.rmtree(os.path.join(ad, 'incoming', sub), ignore_errors=True)
    os.makedirs(cc); save = lambda p, s: (p.parent.mkdir(parents=True, exist_ok=True), p.write_text(s, encoding='utf-8'))
    save(Path(ad, 'incoming', 'files.json'), json.dumps(rows, indent=1))
    for c, xs in docs.items():                          # each record as read: content as the copy, the rest under incoming/db/
        for k, x in xs.items():
            save(*((Path(cc, k + '.html'), x['data'].get('html', '')) if c == 'content' else
                   (Path(ad, 'incoming', 'db', c, k + '.json'), json.dumps(x['data'], ensure_ascii=False, indent=1))))
    m = docs.get('manifest', {}).get('current', {}).get('data', {})
    live = {'parts': m.get('parts', {}), 'parents': m.get('parents', {}), 'files': {p: s[:12] for p, s in files.items()}}
    save(Path(ad, 'incoming', 'live-manifest.json'), json.dumps({**live, 'page_hash': m.get('page_hash', '')}, indent=1))
    prev = loop_state(d)
    version = opt(a, '--version') or m.get('version') or prev.get('live', {}).get('version', '')
    base, repo, lc = prev.get('base') or {'version': version, 'manifest': live}, loop_repo(d), live_copy(ad)
    lsha = commit_tree(repo, 'live', loop_tree(inc, live, lc), f'live {version}')
    if not prev:
        git(repo, 'branch', '-f', 'work', 'live'); git(repo, 'branch', '-f', 'base', 'live')
        if not load(d)[0]: shutil.copytree(inc, d, dirs_exist_ok=True)
    work, wc = work_of(d, refs)
    commit_tree(repo, 'work', loop_tree(d, work, {**lc, **wc}), 'work')
    rep = classify(base['manifest'], live, work)
    merged = not rep['held']
    if merged:
        tree, conflicts = merge3(repo)
        if conflicts:
            rep['merge_conflict'], merged = conflicts, False
            rep['held'] += [{'id': x, 'base': None, 'live': None, 'incoming': None} for x in CONFLICT.findall('\n'.join(conflicts))]
        else:
            git(repo, 'reset', '-q', '--hard', git(repo, 'commit-tree', tree, '-p', 'work', '-p', 'live', '-m', f'merge live {version}').stdout.strip())
            for x in (x for x in rep['theirs'] if x in live['files'] and Path(inc, x).is_file()):
                Path(d, x).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(Path(inc, x), Path(d, x))
            if Path(d, 'content').is_dir():                               # the merged copy, when the folder keeps one
                for c in Path(repo, 'content').glob('*.html'): shutil.copyfile(c, Path(d, 'content', c.name))
            git(repo, 'branch', '-f', 'base', 'live'); base = {'version': version, 'manifest': live}
    save(Path(ad, 'incoming', 'report.json'), json.dumps(rep, indent=1))
    data = lambda c: {k: x['data'] for k, x in docs.get(c, {}).items()}
    status = {k: [x.get('status'), (x.get('applied') or {}).get('version', '')] for k, x in data('incoming').items()}
    proposed, acked = prev.get('incoming', {}).get('proposed', {}), prev.get('incoming', {}).get('acked', [])
    name = prev.get('name') or re.sub(r'[^a-z0-9]+', '-', os.path.basename(os.path.abspath(d)).lower()).strip('-')[:40] or 'artifact'
    st = {'schema': 'adp-state/1', 'name': name, 'capabilities': prev.get('capabilities') or {}, 'exported_at': now(),
          'catalog': prev.get('catalog') or {'url': (read_json(cfg) if (cfg := Path(ADP_HOME, 'config.json')).is_file() else {}).get('catalog') or '', 'vermap': {}},
          'commits': {'live': lsha, 'work': git(repo, 'rev-parse', 'work').stdout.strip()},
          'url': url, 'live': {'version': version, 'at': now()}, 'live_manifest': live, 'page_hash': m.get('page_hash', ''), 'base': base,
          'files': files, 'refs': refs, 'status': status,
          'docs': {f'{c}/{k}': x['version'] for c, xs in docs.items() for k, x in xs.items() if isinstance(x['version'], int)},
          'src_copy': {**{k: H(h) for k, h in wc.items()}, **prev.get('src_copy', {})},
          'incoming': {'held': [h['id'] for h in rep['held']],
                       'unacked': sorted(k for k in proposed if k not in acked and status.get(k, [''])[0] in ('applied', 'declined')),
                       'pending_replies': sorted(k for k, x in data('requests').items()
                                                 if x.get('status') != 'done' and x.get('state') not in ('ack', 'seen', 'working')),
                       'proposed': proposed, 'acked': acked}}
    save_loop(d, st)
    reg = {**registry(), url: {'dir': os.path.abspath(d), 'name': name}}
    os.makedirs(ADP_HOME, exist_ok=True); Path(ADP_HOME, 'artifacts.json').write_text(json.dumps(reg, indent=1, sort_keys=True))
    nxt = (f'held: {len(rep["held"])}; show both versions to the owner, nobody writes' if rep['held'] else
           f'adp.py propose {d} --by NAME --summary S' if rep['new'] + rep['ours'] + rep['retired'] else 'clean: nothing to send')
    emit({'report': rep, 'merged': merged, 'state': os.path.abspath(os.path.join(ad, 'state.json')), 'next': nxt})
```

### `propose`

`adp.py propose DIR --by NAME --summary S [--retire ID --reason R ...]` classifies work against the base and live of the last export run
and merges it with live. Before any export it prints `{error: "no export yet", next}` and exits 2. Each deleted part or file needs its own
`--retire ID --reason R` pair, matched in order. A `state.json` without `live_manifest` takes the live manifest from `incoming/live-manifest.json`.

- **Refused:** it prints `{refused: [...]}` and exits 2, listing every reason that applies: `merge conflict with live` (git's lines), `held` (the
  held ids), `deleted without --retire ID --reason R`, and `--retire needs --reason` (a `--retire` with no reason after it).
- **Work equals live:** it prints `{"nothing": "work equals live", "report": {...}}`.
- **Otherwise** it writes the proposal `DIR.adp/propose-<pid>.json` (see [A proposal](#a-proposal)) and prints the batch that sends it, with
  `{proposal, doc, parts, files, chunks, next}`: the chunk documents, `incoming/<pid>`, then `changes/d-<ms>`. The proposal id is
  `p-<ms>-<4 characters>`. A binary file is sent base64 (`encoding: "base64"`). A file whose content is over 200 KiB has no `content`; it is sent as
  `{path, n, of, content}` documents in `incoming/<pid>/chunks`, numbered across the whole proposal.
- A part's copy edited since the export (`src_copy`) and different from live is also sent, as a part with `kind: "content"`.

```python
# ---
# id: delta.propose
# tool: adp.py
# section: delta
# order: 460
# needs: [delta.export, payloads.batch]
# tests: [loop-ours-is-proposed-and-acknowledged, loop-propose-with-nothing-changed, loop-both-sides-changed-is-held, loop-propose-before-any-export, loop-retire-chunk-and-ack, loop-empty-applied-version-and-older-state]
# sha: 0d00ca6dccf7
# ---
CHUNK = 200 * 1024
CTYPE = {'.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
         '.svg': 'image/svg+xml', '.md': 'text/markdown', '.txt': 'text/plain', '.csv': 'text/csv'}


@cmd('propose')
def loop_propose(a):
    """propose DIR --by NAME --summary S [--retire ID --reason R ...]  (every deleted part id needs its own --retire ID --reason R pair, paired in order)    write work as a proposal, incoming/<pid>, for an editor to apply"""
    by, summary = opt(a, '--by'), opt(a, '--summary')
    if len(bare(a)) != 1 or not by or not summary: sys.exit(usage('propose'))
    d = bare(a)[0]; ad, st, every = adp_dir(d), exported(d), lambda k: [a[i + 1] for i, x in enumerate(a) if x == k]
    if not st: return 2
    retire = dict(zip(every('--retire'), every('--reason') + [''] * len(every('--retire'))))
    (work, wc), lc = work_of(d, st.get('refs', {})), live_copy(ad)
    live = st.get('live_manifest') or (read_json(p) if os.path.isfile(p := os.path.join(ad, 'incoming', 'live-manifest.json')) else st['base']['manifest'])
    work['retired'] = retired = {k: v for k, v in retire.items() if v}
    repo = loop_repo(d); wsha = commit_tree(repo, 'work', loop_tree(d, work, {**lc, **wc}), f'propose: {summary}')
    _, conflicts = merge3(repo)
    rep = classify(st['base']['manifest'], live, work)
    gone, bare_ids = [h['id'] for h in rep['held'] if h['incoming'] is None], [k for k, v in retire.items() if not v]
    refused = ([{'error': 'merge conflict with live', 'detail': conflicts}] * bool(conflicts) + [{'error': 'held', 'held': rep['held']}] * bool(rep['held'])
               + [{'error': 'deleted without --retire ID --reason R', 'ids': gone}] * bool(gone) + [{'error': '--retire needs --reason', 'ids': bare_ids}] * bool(bare_ids))
    if refused:
        emit({'refused': refused}); return 2
    send = sorted(rep['new'] + rep['ours'] + rep['retired'])
    parts = [{'id': x, 'from': live['parts'].get(x), 'to': work['parts'].get(x), 'html': wc.get(x, ''), 'retired': x in retired, 'reason': retired.get(x, '')}
             for x in send if x in work['parts'] or x in live['parts']]
    parts += [{'id': k, 'kind': 'content', 'from': H(lc[k]) if k in lc else None, 'to': H(h), 'html': h, 'retired': False, 'reason': ''}
              for k, h in sorted(wc.items()) if lc.get(k) != h and (k in lc or 'content.js' in send) and st.get('src_copy', {}).get(k) != H(h)]
    if not send and not parts: return emit({'nothing': 'work equals live', 'report': rep})
    ms, at = int(time.time() * 1000), now()
    pid = f'p-{ms}-' + ''.join(random.choices('abcdefghijkmnpqrstuvwxyz23456789', k=4))
    files, chunks = [], []
    for x in (x for x in send if x in work['files'] or x in live['files']):
        e = {'path': x, 'ifMatch': st['files'].get(x), 'contentType': CTYPE.get(os.path.splitext(x)[1].lower(), 'application/octet-stream')}
        files.append(e)
        if x not in work['files']: e.update(content=None, reason=retired.get(x, '')); continue
        b = Path(d, x).read_bytes()
        try: text = b.decode('utf-8')
        except UnicodeDecodeError: text, e['encoding'] = base64.b64encode(b).decode(), 'base64'
        if len(text.encode()) <= CHUNK: e['content'] = text; continue
        pieces = [text[i:i + CHUNK // 2] for i in range(0, len(text), CHUNK // 2)]
        chunks += [{'path': x, 'n': n, 'of': len(pieces), 'content': c} for n, c in enumerate(pieces)]
    doc = {'by': by, 'at': at, 'summary': summary, 'threads': [], 'base': {'version': st['live']['version'], 'page_hash': st.get('page_hash', live.get('page_hash', '')), 'docs': st['docs']},
           'parts': parts, 'files': files, 'live_files': st['files'], 'classified': rep, 'status': 'new',
           'decided': {'by': '', 'at': '', 'reason': ''}, 'applied': {'version': '', 'at': ''}}
    p = os.path.abspath(os.path.join(ad, f'propose-{pid}.json'))
    Path(p).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
    batch = Batch(os.path.join(ad, f'propose-{pid}'))
    for n, c in enumerate(chunks): batch.put('set', f'incoming/{pid}/chunks', str(n), c)
    batch.put('set', 'incoming', pid, path=p)
    batch.put('set', 'changes', f'd-{ms}', {'version': '', 'at': at, 'by': by, 'summary': f'Proposal {pid}: {summary}', 'parts': [], 'threads': [],
                                            'data': [{'doc': f'incoming/{pid}'}]})
    st['incoming']['proposed'][pid] = {'work': wsha, 'manifest': {k: work[k] for k in ('parts', 'files', 'parents')}, 'src_copy': {k: H(h) for k, h in wc.items()}}
    st['incoming']['held'] = []                   # a deletion the export held is retired here
    save_loop(d, st)
    batch.emit(proposal=pid, doc=p, parts=len(parts), files=len(files), chunks=len(chunks),
               next='run the ArtifactData batch, then adp.py ack with its result; an editor applies it on the page')
```

### `ack`

`adp.py ack DIR [--result FILE]` takes what a write returned (from `--result`, or stdin): a batch result (`{results}`, `{writes}` or a list
of `{collection, doc_id or id, version}`) updates each record's version, and a publish result `{shas, version}` (or `version_id`, `versionId`)
the files' SHA-256 and the live version. Input that is not JSON exits 1. As a PostToolUse hook (stdin holds `tool_input`, or `--hook`) it reads
the call's `tool_response` (content blocks or text) and finds DIR by the call's url; an unmanaged url prints `{ack: null, note}`. Before any
export it exits 2 as `propose` does. `ack DIR --proposal PID` takes the proposal's status from the last export (the state's table, else the exported record under `incoming/db/incoming/`): `applied` moves base to this
folder's proposal and its copy, and `declined` leaves base as it is; either way the proposal is closed. Any other status exits 1 with `<pid>: status <status> in the last export read; ack it once applied or declined` on stderr.
It prints `{ack: [what it took], live: {version, at}, incoming: {held, unacked, pending_replies}}`.

```python
# ---
# id: delta.ack
# tool: adp.py
# section: delta
# order: 470
# needs: [delta.state]
# tests: [loop-ours-is-proposed-and-acknowledged, loop-retire-chunk-and-ack, loop-empty-applied-version-and-older-state]
# sha: 9ee2e68e3b62
# ---
FLAGS.add('--hook')


@cmd('ack')
def loop_ack(a):
    """ack DIR [--result FILE] [--proposal PID] [--hook]    take the versions a write returned, or a proposal the page applied or declined"""
    pid, src = opt(a, '--proposal'), opt(a, '--result')
    try: raw = {} if not src and (pid or sys.stdin.isatty()) else hook_input(a, '--result')
    except ValueError as e: sys.exit(f'ack: the result is not JSON: {e}')
    if isinstance(raw, dict) and 'tool_input' in raw or '--hook' in a:       # a PostToolUse hook input: the call and what it returned
        res = raw.get('tool_response') or raw.get('tool_result') or {}
        if isinstance(res, list): res = next((x['text'] for x in res if isinstance(x, dict) and x.get('text')), '{}')
        if isinstance(res, str):
            try: res = json.loads(res)
            except ValueError: res = {}
        d = managed(((raw.get('tool_input') or {}).get('url') or '').rstrip('/'))
        if not d: return emit({'ack': None, 'note': 'not an artifact ADP manages'})
    elif len(bare(a)) == 1: d, res = bare(a)[0], raw
    else: sys.exit(usage('ack'))
    st, done = exported(d), []
    if not st: return 2
    writes = res if isinstance(res, list) else res.get('results') or res.get('writes') or []
    res = res if isinstance(res, dict) else {}
    for w in writes:
        k = f"{w.get('collection')}/{w.get('doc_id') or w.get('id')}"
        if isinstance(w.get('version'), int): st['docs'][k] = w['version']; done.append(k)
    if res.get('shas'):
        st['files'].update(res['shas']); done.append('files')
        st['live']['version'] = str(res.get('version') or res.get('version_id') or res.get('versionId') or st['live']['version'])
    if pid:
        rec = Path(adp_dir(d), 'incoming', 'db', 'incoming', pid + '.json')       # a state without the export's status table: the record as exported
        status, version = st.get('status', {}).get(pid) or ([(r := read_json(rec)).get('status'), (r.get('applied') or {}).get('version', '')] if rec.is_file() else [None, ''])
        if status not in ('applied', 'declined'): sys.exit(f'{pid}: status {status or "unknown"} in the last export read; ack it once applied or declined')
        inc = st['incoming']; prop = inc['proposed'].get(pid)
        if status == 'applied' and prop:                  # this folder's own proposal: its work is the new base
            git(loop_repo(d), 'branch', '-f', 'base', prop['work'])
            st['base'], st['src_copy'] = {'version': version, 'manifest': prop['manifest']}, prop['src_copy']
            if version: st['live']['version'] = version
        inc['unacked'] = [x for x in inc['unacked'] if x != pid]
        inc['acked'] = sorted({*inc['acked'], pid}); done.append(f'incoming/{pid} {status}')
    save_loop(d, st)
    emit({'ack': done, 'live': st['live'], 'incoming': {k: st['incoming'][k] for k in INBOX}})
```

### `gate`

`adp.py gate [--input HOOK.json]` (or the hook input on stdin) is a PreToolUse hook. It denies a write to a managed url (an `Artifact` publish, which is also
what an `Artifact` call without an action does, or an `ArtifactData` call that is not get, list, query or read) while the state lists `held` or `unacked` ids, or `pending_replies` unless every
write in the call targets `requests` or `presence`. It also denies a write whose `if_version` differs from the version the last export read for
that document. `unacked` lists the proposals this folder sent that the last export shows `applied` or `declined` and that `ack --proposal` has not
taken; `pending_replies` lists the `requests` whose status is not `done` and whose state is not `ack`, `seen` or `working`.

In every other case (other tools, reads, calls without a url, unmanaged urls, stdin that is not JSON) it gives no decision, only `additionalContext`, so the host's
normal permission flow applies, and exits 0. An `--input` file that is not JSON exits 1 with `--input: FILE is not JSON: ...`.

```python
# ---
# id: delta.gate
# tool: adp.py
# section: delta
# order: 480
# needs: [delta.state]
# tests: [loop-gate-decisions, loop-both-sides-changed-is-held, loop-ours-is-proposed-and-acknowledged, loop-retire-chunk-and-ack]
# sha: 957b736f83c7
# ---
def gate_says(why, deny=False):
    out = {'permissionDecision': 'deny', 'permissionDecisionReason': why} if deny else {'additionalContext': why}
    emit({'hookSpecificOutput': {'hookEventName': 'PreToolUse', **out}})


@cmd('gate')
def loop_gate(a):
    """gate [--input HOOK.json]    PreToolUse hook: deny a write to a managed artifact while its inbox is not clear or its pins are stale"""
    try: raw = hook_input(a, '--input')
    except ValueError: return gate_says('adp: the hook input is not JSON, so there is nothing to gate')
    tool, ti = raw.get('tool_name', ''), raw.get('tool_input') or {}
    url = (ti.get('url') or '').rstrip('/')
    act = ti.get('action') or ('publish' if tool.endswith('Artifact') else '')       # an Artifact call names no action only to publish
    if not url or tool.endswith('Artifact') and act != 'publish' or act in ('get', 'list', 'query', 'read'):
        return gate_says('adp: not a write onto an existing artifact')
    d = managed(url); st = loop_state(d) if d else {}
    if not st: return gate_says('adp: no state for this url, an artifact ADP does not manage')
    writes = ti.get('writes') or ([ti] if ti.get('collection') else [])
    answering = bool(writes) and all(str(w.get('collection', '')).split('/')[0] in ('requests', 'presence') for w in writes)
    block = {k: st['incoming'][k] for k in INBOX if st['incoming'][k] and (k != 'pending_replies' or not answering)}
    if block:
        return gate_says('adp: the inbox has ' + '; '.join(f'{k}: {", ".join(v)}' for k, v in block.items())
                         + f'. Run adp.py export {d} --url {url} and resolve them first', True)
    keys = [(f"{w.get('collection')}/{w.get('doc_id')}", w['if_version']) for w in writes if 'if_version' in w]
    stale = [f'{k} pinned at {v}, read at {st["docs"][k]}' for k, v in keys if k in st['docs'] and v != st['docs'][k]]
    if stale: return gate_says('adp: a batch not derived from the last export: ' + '; '.join(stale) + '. Re-export, then rebuild it', True)
    gate_says('adp: inbox clear')
```

## A proposal

`incoming/<pid>` records who proposed what, against which base:

```json
{ "by": "agent-a", "at": "2026-11-19T10:00:00Z", "summary": "Keys table: sort", "threads": [],
  "base": {"version": "7", "page_hash": "a1b2c3d4e5f6", "docs": {"manifest/current": 7, "parts/triage.keys-table": 3}},
  "parts": [{"id": "triage.keys-table", "from": "0f1e2d3c4b5a", "to": "9c8b7a6f5e4d", "html": "", "retired": false, "reason": ""}],
  "files": [{"path": "parts/app.js", "ifMatch": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df",
             "contentType": "text/javascript", "content": "..."}],
  "live_files": {"parts/app.js": "574c60bebc47c67f6767237cf4f4adeb285bafdcc2b9b6ec046ab7a65a3f92df"},
  "classified": {"new": [], "ours": ["parts/app.js", "triage.keys-table"], "theirs": [], "applied": [], "held": [], "retired": []},
  "status": "new", "decided": {"by": "", "at": "", "reason": ""}, "applied": {"version": "", "at": ""} }
```

A part's `html` is `DIR/content/<id>.html` when the folder has one. A retired part has `to: null`, `retired: true` and its reason; a retired file
has `content: null` and its reason. `live_files` and each `ifMatch` are the SHA-256 the last export read.

Statuses: `new` (written by `propose`), `merged` (the inbox classified it with nothing held; not yet published), `held` (the inbox found a conflict,
or Apply hit a publish conflict), `applied` (the inbox published it), `declined` (an editor declined it, with a reason).

## The inbox

The inbox is the page side of the loop: a component the page takes from its catalog. This section is what any inbox must do. It lists the open
proposals and classifies each new one with `ADP.classify`. For each held item, a user with edit rights picks Keep live or Take the proposal; Apply
stays disabled until every held item is picked. Apply publishes the proposal's files through `ADP.publish()` with an `ifMatch` per file, then
writes `manifest/current`, `parts/<id>`, `content/<id>` and `changes/<seq>` with the resulting version, and sets the proposal `applied`. Decline
asks for a reason and records it. When a proposal states a `sha256` for a file (a catalog's kit pack does; `adp.py propose` states none), Apply
refuses a file whose delivered text does not match it.

A proposal carries code: its files are published as they are. Treat a proposal as untrusted until an editor has read it: grant no viewer
write access to `incoming/` in the page's access rules, and have an editor preview every file of a proposal, held or not, before Apply. An agent
never applies a proposal it did not write without that preview.

After a publish conflict, a hold found on open, or a Decline, the inbox notifies the watching agent session through the `agent` handle, only when
`canSend()` returns `available`. A successful Apply sends nothing.

A published catalog ships its own kit files the same way: they are seeded as one proposal per kit folder, and the catalog page runs its inbox in
an auto-apply mode that applies every proposal that classifies as `merged`. A kit change proposed to the catalog later is applied the
same way while an editor has the page open; a held, failed or declined proposal is left for a person. Auto-apply skips the preview, so it is only
for a catalog, whose `incoming/` only its editors can write. Never enable it on a page where anyone else can write `incoming/`. See
[catalog](../adp-catalog/SKILL.md).

## Reading the result

- `theirs`: when nothing is held, `adp.py export DIR` has already copied it into `DIR`. No action.
- `ours`: run `propose`.
- `held`: stop. Both sides changed it, and a person decides: an editor picks a side in the inbox, or the owner chooses after you show both versions,
  or the part's holder (the session named in its `holder` field; see [protocol](../adp-protocol/SKILL.md)) settles it. Never resolve a hold
  by overwriting.
- `retired`: a deletion with a reason. `propose` sends it, and Apply records it in `changes/`.

Related: [protocol](../adp-protocol/SKILL.md) for holds and pins, [packing](../adp-packing/SKILL.md) for moving a whole record
between hosts.
