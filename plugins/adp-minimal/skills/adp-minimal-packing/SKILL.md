---
name: adp-minimal-packing
description: "Explains ADP pack formats and record transfer, with the code behind them: the publish arguments (adp.py files, --since, --batch, pins), the one-file page (adp.py files --host single, its loader shim, unpack), seed packs (adp-seed/2, adp.py seed), catalog packs (adp-catalog-pack/1), and record bundles moved between hosts with bundle, import-plan and import-ack. Use when the user asks how to publish only what changed, how to ship a page as one file, restore files from a pack, what seed.json is, or how to move a page's records from Claude to Sites and back."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Pack formats and record transfer

A page is many small files. Transferring them one at a time is slow, and a failure partway leaves a partial publish. ADP packs them into a few
files and unpacks them byte for byte. It defines four pack formats:

| Format | For | Made by | Unpacked by |
|---|---|---|---|
| **One-file page** | a tool that can publish only one file | `adp.py files DIR --host single` | `adp.py unpack PACK DEST` |
| **Seed packs** | the first database documents of a page | `adp.py new`, `adp.py seed` | the page, the first time an editor opens it |
| **Catalog packs** | a catalog's files carried as a few JSON files, where a channel limits the file count | a catalog's distribution | `adp.py unpack` |
| **Record bundle** | a page's records moving between hosts | `adp.py bundle` | `adp.py import-plan`, `import-ack` |

The code blocks with a header are the fragments of `adp.py` this skill owns; [adp-minimal-rebuild](../adp-minimal-rebuild/SKILL.md) assembles
them. Their vectors are in [vectors.md](vectors.md).

## Publishing: `files`, `--since`, `--batch`, `pins`

`adp.py files DIR` prints the arguments of the `Artifact` publish call: `file_path` (the page, `DIR/index.html`), `root` and `files`, every other
served file mapped to itself. A file the service does not serve (by extension) is listed in `skipped`. Entries of DIR itself that start with `.`
are never listed (a dotfile inside a folder is), and nor is a `__pycache__` folder. A page's own tool and a person edit the same files, so `files` also refreshes `seed.json` first when the folder has one: edits since the
seed was written change the hashes it carries.

```python
# ---
# id: packing.publish
# tool: adp.py
# section: packing
# order: 500
# needs: [core.io]
# sha: 1d7341832779
# ---
SERVED = set('.html .css .js .mjs .wasm .json .map .geojson .webmanifest .txt .md .csv .xml .svg .png .jpg .jpeg .gif .webp .avif .ico '
             '.woff .woff2 .ttf .otf .mp3 .wav .ogg .mp4 .webm .pdf'.split())
LIMIT = 250            # files per publish: the tool takes 255, and the page is one more


def files_in(d, tree=False):
    """The files under DIR, sorted, `/` separated, without entries that start with `.`; `tree` keeps them and skips only `__pycache__` folders."""
    out = []
    for root, dirs, names in os.walk(d):
        dirs[:] = sorted(x for x in dirs if (x != '__pycache__' if tree else not x.startswith('.')))
        out += [os.path.relpath(os.path.join(root, n), d).replace(os.sep, '/') for n in sorted(names) if tree or not n.startswith('.')]
    return out


def publish_args(d, only=None):
    """The Artifact publish arguments for DIR: the page, the root, and every other served file (of `only`, when given) mapped to itself."""
    fs = [p for p in files_in(d, True) if p != 'index.html' and not p.startswith('.') and (only is None or p in only)]
    out = {'file_path': os.path.join(d, 'index.html'), 'root': d, 'files': {p: p for p in fs if Path(p).suffix.lower() in SERVED}}
    if skipped := [p for p in fs if Path(p).suffix.lower() not in SERVED]: out['skipped'] = skipped
    return out


def kit_refs(out, d):
    """A page built from a catalog keeps its kit files as references: the roots of installed.json (the entries no other entry requires) are taken
    again, and each file is mapped to the catalog beside the local ones, a local file of the same path winning."""
    if not Path(d, 'installed.json').is_file(): return out
    ix = read_json(Path(d, 'installed.json'))
    ents = ix.get('entries', [])
    ids = [e['id'] for e in ents]
    needed = {r for e in ents for r in e.get('requires', [])}
    roots = [i for i in ix.get('take', []) if i in ids] or [i for i in ids if i not in needed]
    if not (ix.get('url') and roots): return out
    got, code = taken(ix['url'], roots)
    if code:
        if 'fetch' in got:
            got['fetch'].setdefault('then', 'run `adp.py catalog` again: it lists the reads for the whole kit (My Own Kit)')
            got.setdefault('next', 'adp.py catalog fetches your whole kit (My Own Kit)')
        out['kit_refs'] = got; return out
    for p, ref in got['files'].items(): out['files'].setdefault(p, ref)
    out['kit_refs'] = len(got['files'])
    return out
```

`--since MANIFEST.json` (a manifest, or `manifest/current` saved as an ArtifactData document) keeps only the files whose hash differs from the
manifest's `files`; a file the manifest has and DIR lacks maps to `null` (the publish removes it). `index.html` is always the `file_path`, so
`page_changed` says whether it differs, and a `note` when it does not.

A page built from a catalog (`installed.json`, which `new` writes) keeps its kit files as references: a full publish also maps the roots' files
to the catalog, a local file of the same path winning, and `kit_refs` counts them. When the catalog's index is not fetched, `kit_refs` carries the
`take` answer that says how to fetch it.

A publish takes at most 255 files. Over `--batch N` files (default 250) `files` prints `batches` instead of `files`, the local files `index.html`
loads first, in load order, and writes each batch to `DIR.adp/publish-K.json` (`--out` names another folder, made with its parents). Publish the page with the first batch and every other
batch to the same url, noting each version id the tool returns.

```python
# ---
# id: packing.files
# tool: adp.py
# section: packing
# order: 510
# needs: [packing.publish, parts.manifest]
# tests: [files-publish-args, files-since-a-manifest, files-in-batches-then-pins, files-removals-and-kit-references]
# sha: 2b491b8ee3b1
# ---
def page_deps(d):
    """The local files index.html loads, in load order and once each."""
    page = Path(d, 'index.html')
    refs = re.findall(r'(?:src|href)="([^"]+)"', page.read_text(encoding='utf-8')) if page.is_file() else []
    return list(dict.fromkeys(r for r in refs if not re.match(r'(?:[a-z]+:|#|//)', r) and Path(d, r).is_file()))


def batched(out, d, n, where):
    """Over n files, `files` becomes `batches` (what index.html loads first, in load order), each also written to where/publish-K.json."""
    m = out['files']
    if len(m) <= n: return out
    deps = [p for p in page_deps(d) if p in m]
    order = deps + [p for p in m if p not in deps]
    batches = [{p: m[p] for p in order[i:i + n]} for i in range(0, len(order), n)]
    Path(where).mkdir(parents=True, exist_ok=True)
    for k, b in enumerate(batches, 1): Path(where, f'publish-{k}.json').write_text(json.dumps(b))
    del out['files']
    return {**out, 'batches': batches, 'batch_files': [str(Path(where, f'publish-{k}.json').resolve()) for k in range(1, len(batches) + 1)],
            'note': f'{len(m)} files: publish the page with batches[0] (new artifact: add capabilities, icon), then each other batch to the same url; '
                    'every publish passes file_path and root, the tool refuses files without them; note every version id, then adp.py pins'}


@cmd('files')
def files_cmd(a):
    """files DIR [--since MANIFEST.json] [--batch N] [--out DIR]    the publish arguments of DIR; --host single --out FILE [--fragment]: DIR packed into one page"""
    if not bare(a): sys.exit(usage('files'))
    d, host = bare(a)[0], opt(a, '--host', 'claude')
    if host not in ('claude', 'single'): sys.exit(f'files: --host is claude or single, not {host}')
    if host == 'single': return emit(pack_page(d, opt(a, '--out'), '--fragment' in a))
    fresh = Path(d, 'seed.json').is_file() and seed_file(d)['written']
    if not (since := opt(a, '--since')): out = kit_refs(publish_args(d), d)
    else:
        old = read_json(since)
        had, have = old.get('data', old)['files'], manifest(d)['files']
        changed = {p for p, h in have.items() if had.get(p) != h} | ({'seed.json', *seed_read(d)[0]['packs']} if fresh else set())
        out = publish_args(d, changed)
        out['files'].update({p: None for p in had if p not in have})
        out['page_changed'] = had.get('index.html') != have.get('index.html')
        if not out['page_changed']: out['note'] = 'index.html is unchanged: publish with url and the changed files, still passing file_path (the tool requires it; the page is re-sent as is)'
    emit(batched(out, d, int(opt(a, '--batch', LIMIT)), opt(a, '--out', d.rstrip('/') + '.adp')))
```

`pins publish-1.json=VERSION_ID ...` turns the version ids into `{path: version id}` and writes it to `--out` (default `DIR.adp/vermap.json`, beside
the first batch). A catalog's distribution references each file at the version that holds it.

```python
# ---
# id: packing.pins
# tool: adp.py
# section: packing
# order: 520
# needs: [core.io]
# tests: [files-in-batches-then-pins]
# sha: 265d59de873d
# ---
@cmd('pins')
def pins_cmd(a):
    """pins publish-1.json=VERSION_ID ... [--out vermap.json]    the version each published file went up in"""
    pairs = [x.rsplit('=', 1) for x in bare(a) if '=' in x]
    if not pairs: sys.exit('usage: adp.py pins publish-1.json=VERSION_ID ... [--out vermap.json]')
    vermap = {p: ver for f, ver in pairs for p in read_json(f)}
    out = Path(opt(a, '--out') or Path(pairs[0][0]).resolve().parent / 'vermap.json')
    out.write_text(json.dumps(vermap, sort_keys=True))
    emit({'pinned': len(vermap), 'vermap': str(out.resolve()), 'next': f'reference each file in catalog.json at the version {out} gives it, then publish catalog.json to the same url'})
```

## One-file page

```sh
$ADP files DIR --host single --out index.html          # --fragment for the Artifact tool: it adds doctype, html, head, body
$ADP unpack index.html RESTORED/                       # every file back, sha256 checked; DEST is a new or empty folder
```

Every file is embedded once, with its sha256, in a block of the packed `index.html`. A small loader script, the **shim**, serves the page's
relative `<script src>` and `<link rel=stylesheet>` from those blocks, and answers `GET` and `HEAD` `fetch()` calls for packed paths. It uses only
inline scripts and styles, because the claude.ai sandbox blocks `blob:` and `data:` stylesheets and `data:` scripts. Not supported: module scripts,
relative images and CSS `url()`, and a page over 16 MB.

### The packed page

**Files.** Every file under DIR, walked in sorted order (folders and names sorted, entries starting with `.` skipped), with `/` separators. They
are regular files (no symlinks) with paths inside `[A-Za-z0-9._/@+-]+`, and DIR has an `index.html`; otherwise `files --host single` exits 1.

**Blocks.** One per file, `index.html` included (its original bytes, before the rewriting below), in that order, joined with nothing between
them:

```html
<script type="application/adp-file" data-adp-file="PATH" data-type="MIME" data-enc="utf8|b64" data-sha256="64 HEX" data-bytes="N">BODY</script>
```

`data-enc` is `utf8`, and BODY the file's text, when the file is valid UTF-8 and contains no `\r`, no NUL, no `</script` and no `<!--` (case
insensitive); otherwise it is `b64` and BODY the standard base64 of the bytes, on one line, with `=` padding. `data-sha256` and `data-bytes` are of the file's bytes. MIME is
`text/javascript` (`.js`, `.mjs`), `text/css`, `application/json`, `text/html`, `image/svg+xml`, `text/plain` (`.txt`), else the platform's
guess, else `application/octet-stream`.

```python
# ---
# id: packing.block
# tool: adp.py
# section: packing
# order: 530
# needs: [core.io]
# sha: ec020810405b
# ---
import base64, hashlib, mimetypes

SAFE = re.compile(r'[A-Za-z0-9._/@+-]+')      # the characters a packed path may use
PAGE_LIMIT = 16 * 1024 * 1024                  # bytes of a packed page
MIME = {'.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.html': 'text/html',
        '.svg': 'image/svg+xml', '.txt': 'text/plain'}


def block(path, data):
    """One file as a block: its text when that is safe inside a script element, else base64."""
    try: text = data.decode()
    except UnicodeDecodeError: text = None
    if text is None or re.search(r'\r|\x00|</script|<!--', text, re.I): enc, body = 'b64', base64.b64encode(data).decode()
    else: enc, body = 'utf8', text
    mime = MIME.get(Path(path).suffix.lower()) or mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return (f'<script type="application/adp-file" data-adp-file="{path}" data-type="{mime}" data-enc="{enc}" '
            f'data-sha256="{hashlib.sha256(data).hexdigest()}" data-bytes="{len(data)}">{body}</script>')
```

**Rewriting `index.html`.** When it has both a `<head ...>...</head>` and a `<body ...>...</body>`, their contents are used; otherwise (a
fragment, or only one of the two) the whole file is the body and HEAD is empty. Attributes are read as `name`, `name=value`, `name="value"` or
`name='value'`, names compared case-insensitively, quotes removed. In both HEAD and BODY:

- an empty `<script ...>` element (nothing but whitespace before its `</script>`) whose `src` (without `?` or `#` part) is exactly a packed path as listed above (no `./`, no `/` prefix, no
  other normalization), and is not `type=module`, becomes
  `<script>ADPPACK.js("PATH")</script>`; with a `defer` attribute it is removed from its place and appended after the body;
- a `<link ...>` whose `rel` is exactly `stylesheet` (case-insensitive) and whose `href`, matched the same way, names a packed file becomes `<script>ADPPACK.css("PATH")</script>`;
- everything else is kept as is. `PATH` is written as a JSON string.

The head's `<title>` (or `<title>Page</title>` when it has none) and every `<meta charset>` are taken out of the head. The page is then:

```
<!doctype html>\n<html ATTRS><head><meta charset="utf-8">TITLE BLOCKS SHIM HEAD</head><body ATTRS>BODY DEFERRED</body></html>\n
```

with nothing between the pieces. ATTRS is the original tag's attribute text exactly as written, leading whitespace included (`<html lang="en">`
stays `<html lang="en">`), and empty when the tag is absent. SHIM is `<script>`, the `SHIM` code below, then `</script>`. `--fragment` writes only
`TITLE BLOCKS SHIM HEAD BODY DEFERRED`, for a tool that adds the document skeleton itself. `bytes` in the output is the page's length in UTF-8.

**The shim.** It indexes the blocks by path, and installs `window.ADPPACK` (`css(path)` and `js(path)` insert a `<style>` or `<script>` with
the file's text before the calling script; `js` appends `//# sourceURL=PATH`) and a `fetch` that answers `GET` and `HEAD` for a packed path
relative to the page with status 200 and the block's `data-type`, passing every other call to the original:

```python
# ---
# id: packing.shim
# tool: adp.py
# section: packing
# order: 535
# needs: [core.io]
# sha: 81e77e56200a
# ---
SHIM = r'''(function(){var B={};document.querySelectorAll('script[data-adp-file]').forEach(function(s){B[s.getAttribute('data-adp-file')]=s});
function raw(p){var s=B[p];if(!s)throw new Error('adp-pack: no file '+p);if(s.dataset.enc==='utf8')return new TextEncoder().encode(s.textContent);var b=atob(s.textContent),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
function text(p){var s=B[p];return s.dataset.enc==='utf8'?s.textContent:new TextDecoder().decode(raw(p))}
function put(tag,p,t){var e=document.createElement(tag);e.textContent=t;var c=document.currentScript;c.parentNode.insertBefore(e,c)}
window.ADPPACK={files:B,css:function(p){put('style',p,text(p))},js:function(p){put('script',p,text(p)+'\n//# sourceURL='+p)}};
var f=window.fetch,base=new URL('.',document.baseURI).href;
window.fetch=function(u,o){var a=String(u&&u.url||u),m=((o&&o.method)||(u&&u.method)||'GET').toUpperCase();
 try{a=new URL(a,document.baseURI).href}catch(e){}
 var p=a.indexOf(base)===0?a.slice(base.length).split(/[?#]/)[0]:null;
 if(p&&B[p]&&(m==='GET'||m==='HEAD'))return Promise.resolve(new Response(m==='HEAD'?null:raw(p),{status:200,headers:{'content-type':B[p].dataset.type}}));
 return f.apply(this,arguments)}})()'''
```

```python
# ---
# id: packing.pack
# tool: adp.py
# section: packing
# order: 540
# needs: [packing.publish, packing.block, packing.shim]
# tests: [pack-and-unpack-round-trip, pack-refusals-and-catalog-pack]
# sha: 1d6457aeae7c
# ---
FLAGS.add('--fragment')
ATTR = re.compile(r'([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]*)))?')


def attrs(text):
    return {m[1].lower(): m[2] or m[3] or m[4] or '' for m in ATTR.finditer(text)}


def pack_page(d, out, fragment):
    """DIR -> one page that serves every file from its blocks; written to out. Returns the summary."""
    paths = files_in(d)
    if 'index.html' not in paths: sys.exit('files --host single: the folder needs an index.html')
    for p in paths:
        if Path(d, p).is_symlink(): sys.exit(f'files --host single: {Path(d, p)} is a symlink, and symlinks are not packed')
        if not SAFE.fullmatch(p): sys.exit(f'files --host single: {p} has an unsupported name (use A-Z a-z 0-9 . _ / @ + -)')
    html = Path(d, 'index.html').read_bytes().decode()
    head, body = re.search(r'<head\b[^>]*>(.*?)</head>', html, re.S | re.I), re.search(r'<body\b([^>]*)>(.*)</body>', html, re.S | re.I)
    both = head and body
    head, body = (head[1], body[2]) if both else ('', html)
    deferred = []

    def script(m):
        at = attrs(m[1])
        p = re.split(r'[?#]', at.get('src', ''))[0]
        if p not in paths or at.get('type', '').lower() == 'module': return m[0]
        call = f'<script>ADPPACK.js({json.dumps(p)})</script>'
        if 'defer' not in at: return call
        deferred.append(call)
        return ''

    def link(m):
        at = attrs(m[1])
        p = re.split(r'[?#]', at.get('href', ''))[0]
        return f'<script>ADPPACK.css({json.dumps(p)})</script>' if at.get('rel', '').lower() == 'stylesheet' and p in paths else m[0]

    def swap(s): return re.sub(r'<link\b([^>]*)>', link, re.sub(r'<script\b([^>]*)>\s*</script\b[^>]*>', script, s, flags=re.I), flags=re.I)

    head, body = swap(head), swap(body)
    title = re.search(r'<title\b[^>]*>.*?</title>', head, re.S | re.I)
    head = re.sub(r'<meta\b([^>]*)>', lambda m: '' if 'charset' in attrs(m[1]) else m[0], head.replace(title[0], '') if title else head, flags=re.I)
    blocks = ''.join(block(p, Path(d, p).read_bytes()) for p in paths)
    inner = f'{title[0] if title else "<title>Page</title>"}{blocks}<script>{SHIM}</script>{head}'
    tail = body + ''.join(deferred)
    if fragment: page = inner + tail
    else:
        tag = lambda name: (re.search(rf'<{name}\b([^>]*)>', html, re.I) or [0, ''])[1] if both else ''
        page = f'<!doctype html>\n<html{tag("html")}><head><meta charset="utf-8">{inner}</head><body{tag("body")}>{tail}</body></html>\n'
    size = len(page.encode())
    if size > PAGE_LIMIT: sys.exit(f'files --host single: the packed page is {size} bytes, over the 16 MB page limit')
    if out: Path(out).write_bytes(page.encode())
    return {'host': 'single', 'out': out, 'files': len(paths), 'bytes': size, 'fragment': fragment}
```

**Unpacking** refuses a DEST that is not empty, reads every block, decodes it, and refuses the whole pack (nothing written) when a hash or length
differs, a path is unsafe (absolute, with a `..` segment, or outside the characters above) or the file holds no block. A `catalog-pack-NN.json`
unpacks the same way, its schema checked; there an entry with an absolute or `..` path, or whose text is not a string, is dropped and the others are
written, and a pack with no files writes nothing and exits 0.

```python
# ---
# id: packing.unpack
# tool: adp.py
# section: packing
# order: 545
# needs: [packing.block]
# tests: [pack-and-unpack-round-trip, pack-refusals-and-catalog-pack, unpack-refuses-a-non-empty-folder, files-and-unpack-edges]
# sha: 2033fdcf8d6c
# ---
BLOCK = re.compile(r'<script type="application/adp-file" data-adp-file="([^"]+)" data-type="[^"]*" data-enc="(\w+)" '
                   r'data-sha256="(\w+)" data-bytes="(\d+)">(.*?)</script>', re.S)


def read_pack(text):
    """{path: bytes} of a packed page, or of a catalog pack (`{schema: adp-catalog-pack/1, files: {path: text}}`); a bad pack stops the run."""
    if text.lstrip().startswith('{'):
        pack = json.loads(text)
        if not isinstance(pack, dict) or pack.get('schema') != 'adp-catalog-pack/1' or not isinstance(pack.get('files'), dict): sys.exit('unpack: not an ADP pack')
        return {p: t.encode() for p, t in pack['files'].items() if isinstance(t, str) and not p.startswith('/') and '..' not in p.split('/')}
    out = {}
    for p, enc, sha, n, body in BLOCK.findall(text):
        out[p] = data = base64.b64decode(body) if enc == 'b64' else body.encode()
        if hashlib.sha256(data).hexdigest() != sha or len(data) != int(n): sys.exit(f'unpack: {p} does not match its sha256')
    if bad := [p for p in out if not SAFE.fullmatch(p) or p.startswith('/') or '..' in p.split('/')]: sys.exit(f'unpack: unsafe path {bad[0]}')
    return out or sys.exit('unpack: no packed files found')


@cmd('unpack')
def unpack_cmd(a):
    """unpack PACK DEST    write every file of a packed page, or of a catalog pack, under an empty DEST"""
    if len(a) != 2: sys.exit(usage('unpack'))
    if Path(a[1]).is_dir() and any(Path(a[1]).iterdir()): sys.exit(f'unpack: {a[1]} is not empty')
    try: files = read_pack(Path(a[0]).read_bytes().decode())
    except (OSError, ValueError) as e: sys.exit(f'unpack: {e}')
    for p, data in files.items():
        Path(a[1], p).parent.mkdir(parents=True, exist_ok=True)
        Path(a[1], p).write_bytes(data)
    emit({'dest': a[1], 'files': len(files), 'bytes': sum(map(len, files.values()))})
```

## Seed packs

`seed.json` is the index (`schema: adp-seed/2`, `version`, `by`, `at`, `docs`, `collections` counts, `packs` paths; `overrides`, `[]` when none; `role` and `summary` when given). Each
`seed/pack-NNN.json` is:

```json
{ "schema": "adp-seed/2", "pack": 1, "of": 3,
  "docs": [ {"collection": "parts", "id": "home.lead", "data": {"title": "Lead", "hash": "0f1e2d3c4b5a"}},
            {"collection": "manifest", "id": "current", "data": {"schema": "adp/2", "version": 1}} ] }
```

Documents are cut into packs in order, so `manifest/current` is the last document of the last pack. A new pack starts when the next document would
take the current one past 1,500,000 bytes of UTF-8 JSON (`ADP_PACK` sets another size; a larger document gets a pack of its own). The seed files are published with the page and
never appear in the manifest.

```python
# ---
# id: packing.seed-packs
# tool: adp.py
# section: packing
# order: 550
# needs: [core.io]
# tests: [seed-reads-an-adp-seed-1-and-prints-batches]
# sha: e3e7003af7fe
# ---
PACK = int(os.environ.get('ADP_PACK', 1_500_000))        # bytes of UTF-8 JSON per seed pack


def tally(docs):
    out = {}
    for c, _, _ in docs: out[c] = out.get(c, 0) + 1
    return out


def write_seed(d, docs, **head):
    """DIR/seed/pack-NNN.json (the docs, cut at PACK bytes, in order) and the index DIR/seed.json; returns the index."""
    packs, cur, size = [], [], 0
    for c, i, x in docs:
        doc = {'collection': c, 'id': i, 'data': x}
        n = len(json.dumps(doc, ensure_ascii=False).encode())
        if cur and size + n > PACK: packs.append(cur); cur, size = [], 0
        cur.append(doc); size += n
    packs.append(cur)
    Path(d, 'seed').mkdir(parents=True, exist_ok=True)
    for f in Path(d, 'seed').glob('pack-*.json'): f.unlink()
    names = [f'seed/pack-{k:03d}.json' for k in range(1, len(packs) + 1)]
    for k, (name, pk) in enumerate(zip(names, packs), 1):
        Path(d, name).write_text(json.dumps({'schema': 'adp-seed/2', 'pack': k, 'of': len(packs), 'docs': pk}, ensure_ascii=False), encoding='utf-8')
    idx = {'schema': 'adp-seed/2', **head, 'docs': len(docs), 'collections': tally(docs), 'packs': names}
    Path(d, 'seed.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding='utf-8')
    return idx


def seed_read(d):
    """-> (index, [(collection, id, data)]) of the seed in DIR; ({}, []) when there is none. An `adp-seed/1` index holds its documents inline."""
    if not Path(d, 'seed.json').is_file(): return {}, []
    idx = read_json(Path(d, 'seed.json'))
    docs = list(idx['docs']) if isinstance(idx.get('docs'), list) else []
    docs += [x for f in idx.get('packs', []) if Path(d, f).is_file() for x in read_json(Path(d, f)).get('docs') or []]
    return idx, [(x['collection'], x['id'], x['data']) for x in docs if isinstance(x, dict) and isinstance(x.get('data'), dict)]
```

`adp.py seed DIR` writes the first documents of a page: `parts/<id>` for every part except `_rest`, `content/<id>` for each non-empty copy in
`content.js`, `changes/000001`, `agents/<NAME>` and, last, `manifest/current`. `--data FILE|DIR` (repeatable) adds the page's own documents to
the first open too: a FILE holds a list, or `{docs: [...]}`, of `{collection, id, data}` (`doc_id` and `file_path` are the names an `ArtifactData` write uses
for `id` and `data`); a DIR holds `collection/id.json`, nested collections as folders (`requests/r1/turns/t1.json`), or the flat `collection__id.json` a
batch folder holds (`/` written `~`). A `--data` document of a generated collection merges into the generated one, its fields winning; the seed's
index keeps it as `overrides`. Run again, `seed` keeps the earlier `--by`, `--version`, `--role`, `--summary` and `--data` documents, reads an
`adp-seed/1` seed (its documents inline in the index) and writes it as `adp-seed/2`, skips a pack the index names that is gone, and leaves the files as they are when no document changed. A
page without `adp.js` does not seed itself: `--batches` prints the same documents as `ArtifactData` batches, and `--dry-run` counts them and writes
nothing. `--at TIME` stamps the documents and the index with TIME instead of now (`bundle` takes it too, for `exportedAt`).

```python
# ---
# id: packing.seed-docs
# tool: adp.py
# section: packing
# order: 560
# needs: [packing.seed-packs, protocol.manifest-doc]
# tests: [seed-keeps-what-it-was-given]
# sha: d896b16fcc90
# ---
GENERATED = ('parts', 'content', 'changes', 'agents', 'manifest')


def data_docs(sources):
    """--data FILE|DIR ... -> [(collection, id, data)]."""
    out = []
    for s in sources:
        if not os.path.exists(s): sys.exit(f'--data: no file or directory {s}')
        if os.path.isdir(s):
            for p in (p for p in files_in(s, True) if p.endswith('.json')):
                segs = p[:-5].split('__', 1) if '/' not in p and '__' in p else p[:-5].split('/')
                if len(segs) % 2: sys.exit(f'--data {s}: {p} is not collection/id.json')
                out.append(('/'.join(segs[:-1]).replace('~', '/'), segs[-1], read_json(Path(s, p))))
        else:
            f = read_json(s)
            docs = f.get('docs') if isinstance(f, dict) else f
            if not isinstance(docs, list): sys.exit(f'--data {s}: a list of docs or {{docs: [...]}}')
            for x in docs:
                c, i = x.get('collection'), x.get('id', x.get('doc_id'))
                data = x['data'] if 'data' in x else read_json(x['file_path']) if x.get('file_path') else None
                if not (isinstance(c, str) and isinstance(i, str) and isinstance(data, dict)): sys.exit(f'--data {s}: a doc needs collection, id and data (an object)')
                out.append((c, i, data))
    if bad := [c for c, i, x in out if not (isinstance(i, str) and isinstance(x, dict))]: sys.exit(f'--data: a doc of {bad[0]} needs an id and a data object')
    return out


def seed_docs(d, by, version, at, role, summary):
    """The documents a record starts with, manifest/current last -> ([(collection, id, data)], the parts whose copy is empty and has no document)."""
    m, copy = manifest(d), content_of(d)
    real = sorted(p for p in m['parts'] if not p.startswith(REST))
    empty = [k for k, v in copy.items() if not v.get('html')]
    docs = [('parts', p, {'title': copy.get(p, {}).get('title', p), 'parent': m['parents'][p], 'hash': m['parts'][p], 'version': version,
                          'at': at, 'by': by, 'summary': 'added in the first build', 'holder': '', 'hold_until': '', 'file': m['part_file'][p]})
            for p in real]
    docs += [('content', k, dict(v, at=at, by=by, since=version)) for k, v in copy.items() if k not in empty]
    return docs + [('changes', '000001', {'version': version, 'at': at, 'by': by, 'summary': summary or 'adp/2 adopted: first build',
                                          'parts': [{'id': p, 'from': '', 'to': m['parts'][p]} for p in real], 'threads': []}),
                   ('agents', agent_id(by), {'role': role, 'session': '', 'last_seen': at, 'holds': []}),
                   ('manifest', 'current', manifest_doc(m, d, version, by, at))], empty
```

`seed_file` is what `new` calls: it writes the seed and says what it holds.

```python
# ---
# id: packing.seed-file
# tool: adp.py
# section: packing
# order: 570
# needs: [packing.seed-docs]
# tests: [seed-keeps-what-it-was-given, seed-reads-an-adp-seed-1-and-prints-batches]
# sha: 85c0e86eee20
# ---
def seed_all(d, by, version, data, role, summary, at=None):
    """Every document the seed of DIR holds now, with the settings and the extra documents an earlier seed had -> (docs, empty, old index, old docs, settings)."""
    old, had = seed_read(d)
    head = {'version': version or old.get('version', '1'), 'by': by or old.get('by', 'adp'), 'role': role or old.get('role', ''),
            'summary': summary or old.get('summary', '')}
    extra = {(c, i): x for c, i, x in had if c not in GENERATED}
    over = {(x['collection'], x['id']): x['data'] for x in old.get('overrides', [])}
    for c, i, x in data or []: (over if c in GENERATED else extra)[(c, i)] = x
    docs, empty = seed_docs(d, head['by'], head['version'], at or now(), head['role'], head['summary'])
    head['overrides'] = [{'collection': c, 'id': i, 'data': x} for (c, i), x in over.items()]
    docs = [(c, i, {**x, **over.pop((c, i), {})}) for c, i, x in docs]
    return [(c, i, x) for (c, i), x in {**extra, **over}.items()] + docs, empty, old, had, head


def seed_file(d, by=None, version=None, data=None, role=None, summary=None, at=None):
    """Write DIR/seed.json and DIR/seed/ unless no document changed (`at` aside) -> {seed, written, docs, collections, packs, bytes, skipped_empty}."""
    docs, empty, old, had, head = seed_all(d, by, version, data, role, summary, at)
    strip = lambda ds: [(c, i, {k: v for k, v in x.items() if k not in ('at', 'last_seen')}) for c, i, x in ds]
    written = old.get('schema') != 'adp-seed/2' or strip(docs) != strip(had)
    idx = write_seed(d, docs, at=docs[-1][2]['at'], **{k: v for k, v in head.items() if v or k == 'overrides'}) if written else old
    return {'seed': str(Path(d, 'seed.json')), 'written': written, 'docs': idx['docs'], 'collections': idx['collections'], 'packs': idx['packs'],
            'bytes': sum(Path(d, p).stat().st_size for p in idx['packs']), 'skipped_empty': empty}
```

```python
# ---
# id: packing.seed
# tool: adp.py
# section: packing
# order: 580
# needs: [packing.seed-file, payloads.batch]
# tests: [seed-dry-run, seed-files, seed-keeps-what-it-was-given, seed-reads-an-adp-seed-1-and-prints-batches, seed-tolerates-a-missing-pack-and-refuses-bad-data]
# sha: 5a1e75edfd44
# ---
FLAGS.add('--batches')


@cmd('seed')
def seed_cmd(a):
    """seed DIR [--by NAME] [--version V] [--data FILE|DIR]... [--summary S] [--role R] [--at TIME] [--batches] [--dry-run]    the first records of a page, as seed.json and seed/"""
    if not bare(a): sys.exit(usage('seed'))
    d, data = bare(a)[0], data_docs([a[i + 1] for i, x in enumerate(a) if x == '--data'])
    if not os.path.isdir(d): sys.exit(f'seed: {d} is not a directory (adp.py new makes one)')
    args = (d, opt(a, '--by'), opt(a, '--version'), data, opt(a, '--role'), opt(a, '--summary'), opt(a, '--at'))
    if '--dry-run' in a or '--batches' in a:
        docs, empty = seed_all(*args)[:2]
        if '--dry-run' in a:
            return emit({'collections': tally(docs), 'docs': len(docs), 'batches': -(-len(docs) // 50), 'skipped_empty': empty,
                         'bytes': sum(len(json.dumps(x, ensure_ascii=False).encode()) for _, _, x in docs)})
        b = Batch(opt(a, '--out', d.rstrip('/') + '.adp'))
        for c, i, x in docs: b.put('set', c, i, x)
        return b.emit(**({'skipped_empty': empty} if empty else {}))
    emit({**seed_file(*args), 'next': 'publish DIR (seed.json and seed/ go up with the files) and open the page once as an editor: it expands the packs into its database'})
```

## Catalog packs

A catalog is hundreds of files. Where a channel limits how many files it carries, the catalog travels as `catalog-pack-NN.json` files:
`{"schema": "adp-catalog-pack/1", "files": {path: text}}`, UTF-8 text only, a new pack starting when the next file would take the current one
past 921,600 characters of text. `adp.py unpack PACK DEST` writes one pack's files into an empty DEST. A published catalog ships its kit the same
way as a page ships its records: its seed carries the kit folders as inbox proposals ([delta and inbox](../adp-minimal-delta/SKILL.md)), applied
one at a time when an editor opens the page.

## Moving records between hosts: bundle, plan, acknowledge

A bundle reuses the seed format and adds provenance (`source`: host, artifact, publication version, export time, author, bundle id) and the
store's `revisions`. The shell builds bundles, classifies records and records provenance. A host adapter ([hosts](../adp-minimal-hosts/SKILL.md#the-claude-adapter-in-adppy))
translates its plans into the host's read and conditional-write calls, which the agent executes. There is no automatic sync.

```sh
$ADP bundle --host claude --artifact SOURCE                 # prints the reads; save the results as source-reads.json
$ADP bundle source-reads.json bundle-dir --host claude --artifact SOURCE --version V --raw
$ADP import-plan bundle-dir --host sites --artifact TARGET  # prints the target reads
$ADP import-plan bundle-dir target-reads.json --host sites --artifact TARGET --raw --out plan.json
# run the plan's calls in order, saving [{call, result}] as results.json
$ADP import-ack plan.json results.json --host sites --raw
```

- It covers `manifest`, `parts`, `content`, `changes`, `decisions`, `config`, `agents`, `incoming`, `requests` and each request's `turns`
  (`requests/<id>/turns`, read as one more collection); not presence, status, or the shell's own `imports` records. The reads of the first command
  name the nine collections, and `--collections C,...` adds more: a bundle holds what the saved reads returned. With `--raw` the saved results must
  be complete and cover every collection asked for, or `bundle` refuses; once the `requests` are read it exits 2 with the reads of their `turns`, to
  append to the same file.
- Planning uses the three-way classification of [the delta](../adp-minimal-delta/SKILL.md#the-classification): base is the last imported hash in
  `imports/<source>`, live is the target, incoming is the bundle. New records are created, source-only changes replace, equal records are skipped,
  target-only changes stay. Conflicting changes are **held**: not written, and the plan exits 2 with no calls. A replace the target gave no revision
  for is held too. `--only C,...` plans just those collections (the plan and the acknowledged import record it). `--base BUNDLE` names the bundle
  this one was derived from, the common ancestor of a return trip; an import already recorded for the source wins over it.
- It never deletes records. Source revisions are kept for provenance only; every write is conditioned on a revision from a fresh read of the target.
- `import-ack` reports *applied* only when the write result matches. A write with no receipt is *unknown*: it is not recorded, and the next
  `import-plan`, from a fresh read, classifies it again.
- The bundle carries records, not source files: publish the page with `adp.py files` and the host's own publication.

Records are compared by `chash`: `sha256:` over the document's sorted, compact JSON. The bundle's id is `b-` and the first 12 hex of the `chash` of its documents.

```python
# ---
# id: packing.bundle
# tool: adp.py
# section: packing
# order: 590
# needs: [packing.seed-packs, hosts.claude, protocol.pins]
# tests: [bundle-asks-for-its-reads, bundle-refuses-an-incomplete-raw-read, bundle-from-raw-reads, move-records-to-an-empty-artifact]
# sha: ebc04ce7e0d2
# ---
BUNDLED = ('manifest', 'parts', 'content', 'changes', 'decisions', 'config', 'agents', 'incoming', 'requests')
SKIP = ('status', 'presence', 'imports')       # never exported: written by the page, transient, or the shell's own record
FLAGS.add('--raw')


def chash(x):
    return 'sha256:' + hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def adapter(a, side=''):
    """The host adapter --host names and, for a command that reads or writes a host (`side`: source or target), the --artifact."""
    host = HOSTS.get(opt(a, '--host')) or sys.exit('--host names the adapter: ' + ', '.join(HOSTS))
    if side and not opt(a, '--artifact'): sys.exit(f'--artifact names the {side} artifact')
    return host, opt(a, '--artifact')


def read_set(a, path, need=(), then='read them again before planning'):
    """The documents a saved read holds -> ({collection/id: {collection, id, data, revision}}, {collection/id: revision} of the snapshots that say `exists: false`,
    the collections the read covered, None when unknown). A document with no object `data` is skipped. With --raw the file is the host's results: a read that is incomplete, or leaves a collection of `need` uncovered, is refused (`then` ends the message)."""
    f, cov = read_json(path), None
    if '--raw' in a:
        f = adapter(a)[0].parse_reads(f)
        if not f['complete']: sys.exit(f'{path}: the read is incomplete ({"; ".join(f["warnings"]) or "no detail"}): read again before planning')
        cov = f['covered']
        if miss := [c for c in need if c not in cov]: sys.exit(f'{path}: the read does not cover {", ".join(miss)}: {then}')
    docs, gone = {}, {}
    for x in (f.get('docs') if isinstance(f, dict) else f) or []:
        if isinstance(x.get('collection'), str) and isinstance(x.get('id'), str):
            if x.get('exists') is False: gone[f"{x['collection']}/{x['id']}"] = x.get('revision')
            elif isinstance(x.get('data'), dict): docs[f"{x['collection']}/{x['id']}"] = x
    return docs, gone, cov


def read_docs(a, path, need=()):
    return read_set(a, path, need)[0]


@cmd('bundle')
def bundle_cmd(a):
    """bundle [DOCS.json OUT_DIR] --host H --artifact SRC [--version V] [--by NAME] [--collections C,...] [--at TIME] [--raw]    the reads to run, or the bundle of the records they returned"""
    pos, (ad, art) = bare(a), adapter(a, 'source')
    want = [*BUNDLED, *filter(None, opt(a, '--collections', '').split(','))]
    if not pos: emit({'reads': ad.read_calls(art, want)}); return 2
    if len(pos) == 1: sys.exit(usage('bundle'))
    docs, _, cov = read_set(a, pos[0], want, 'a bundle from it would silently drop them; read them again')
    if cov is not None and (more := sorted({f"requests/{x['id']}/turns" for x in docs.values() if x['collection'] == 'requests'} - set(cov))):
        print('append the results of these reads to the same file and run bundle again', file=sys.stderr)
        emit({'reads': ad.read_calls(art, more)}); return 2
    got = sorted((x for x in docs.values() if x['collection'].split('/')[0] not in SKIP), key=lambda x: (x['collection'], x['id']))
    docs = [(x['collection'], x['id'], x['data']) for x in got]
    src = {'id': 'b-' + chash(docs)[7:19], 'host': opt(a, '--host'), 'artifact': art, 'version': opt(a, '--version', ''), 'exportedAt': opt(a, '--at') or now(), 'by': opt(a, '--by', 'adp')}
    write_seed(pos[1], docs, version=src['version'] or '1', by=src['by'], at=src['exportedAt'], overrides=[], source=src,
               revisions={f"{x['collection']}/{x['id']}": x['revision'] for x in got if x.get('revision') is not None})
    emit({'bundle': src['id'], 'docs': len(docs), 'dir': pos[1]})
```

`import-plan` reads the bundle and the target's fresh read and prints the plan: one op per record (`new` creates, `ours` replaces pinned to the
target's revision, `applied` and `theirs` skip, `held` holds), `manifest/current` last. `calls` appears only when nothing holds; `order` carries the rule that `manifest/current` is written last, and appears whenever the plan writes it. Each
write op (`create`, `replace`) carries `op`, `collection`, `id` and `data`, held plans included; `baseHash`, `liveHash` and `incomingHash` are its three states. `import-ack` takes the receipts of those calls and prints what was applied, what failed and the calls that record
the import: `imports/<source>` with the hash and revision of every confirmed record, and a `changes/d-<ms>` entry.

```python
# ---
# id: packing.import
# tool: adp.py
# section: packing
# order: 595
# needs: [packing.bundle, delta.classify]
# tests: [move-records-to-an-empty-artifact, move-holds-a-record-the-target-changed, move-ack-a-partial-import, move-return-trip-with-a-base-and-a-selection, move-through-the-raw-adapter, move-absent-snapshots-and-option-first-ack]
# sha: 4616600dc962
# ---
import time


def bundle_of(path, base=False):
    """(index, documents) of a bundle folder (a `--base` one need not carry `source`); any other folder is refused."""
    idx, docs = seed_read(path)
    if idx.get('schema') != 'adp-seed/2' or not (base or idx.get('source')): sys.exit(f"{'--base ' * base}{path} is not a bundle (adp.py bundle writes one)")
    return idx, docs


@cmd('import-plan')
def import_plan(a):
    """import-plan BUNDLE [TARGET.json] --host H --artifact DST [--only C,...] [--base BUNDLE] [--out PLAN.json] [--raw]    the target's reads, or the plan that imports the bundle into it"""
    pos, (ad, art) = bare(a), adapter(a, 'target')
    if not pos: sys.exit(usage('import-plan'))
    idx, docs = bundle_of(pos[0])
    only = [c for c in opt(a, '--only', '').split(',') if c]
    if only: docs = [x for x in docs if x[0].split('/')[0] in only]
    pid = re.sub(r'[^A-Za-z0-9_.~:@+-]+', '-', f"{idx['source']['host']}-{idx['source']['artifact']}")[:120]
    need = sorted({c for c, _, _ in docs} | {'imports'})
    if len(pos) < 2: emit({'reads': ad.read_calls(art, need)}); return 2
    live, gone, _ = read_set(a, pos[1], need)
    prior = live.get(f'imports/{pid}')
    base = prior['data']['records'] if prior else {}
    if opt(a, '--base'): base = {**{f'{c}/{i}': {'hash': chash(x)} for c, i, x in bundle_of(opt(a, '--base'), True)[1]}, **base}
    inc = {f'{c}/{i}': x for c, i, x in sorted(docs, key=lambda d: (d[:2] == ('manifest', 'current'), d[:2]))}
    states = [{'parts': m, 'files': {}} for m in ({k: v['hash'] for k, v in base.items()}, {k: chash(v['data']) for k, v in live.items()}, {k: chash(x) for k, x in inc.items()})]
    cls = classify(*states)
    kind = {k: c for c in ('new', 'ours', 'theirs', 'applied') for k in cls[c]} | {h['id']: 'held' for h in cls['held']}
    ops = [{'key': k, 'class': kind.get(k, 'applied'), 'baseHash': base.get(k, {}).get('hash'), 'liveHash': states[1]['parts'].get(k),
            'incomingHash': states[2]['parts'][k], 'guard': live[k].get('revision') if k in live else gone.get(k)} for k in inc]
    for o in ops:
        o['action'] = {'new': 'create', 'ours': 'replace', 'held': 'hold'}.get(o['class'], 'skip')
        if o['action'] == 'replace' and o['guard'] is None: o['action'], o['why'] = 'hold', 'target has no revision to guard the write with'
        elif o['action'] == 'hold': o['why'] = 'both sides changed, or the target differs and no import was recorded'
        if o['action'] in ('create', 'replace'): o.update(op=o['action'], collection=o['key'].split('/')[0], id=o['key'].split('/', 1)[1], data=inc[o['key']])
    held = [o['key'] for o in ops if o['action'] == 'hold']
    plan = {'schema': 'adp-import-plan/1', 'bundle': {'id': idx['source']['id'], 'schema': idx['schema'], 'docs': len(docs), 'source': idx['source']},
            'target': {'host': opt(a, '--host'), 'artifact': art, 'readAt': now()}, 'only': only, 'ops': ops, 'held': held,
            'counts': {n: sum(o['action'] == n for o in ops) for n in ('create', 'replace', 'skip', 'hold')},
            'provenance': {'collection': 'imports', 'id': pid, 'exists': bool(prior), 'guard': prior.get('revision') if prior else gone.get(f'imports/{pid}'), 'records': base}}
    writes = [o for o in ops if o['action'] in ('create', 'replace')]
    if any(o['key'] == 'manifest/current' for o in writes):
        plan['order'] = {'last': 'manifest/current', 'rule': 'run the calls in order; if an earlier call is rejected or unknown, do not run the call that writes manifest/current'}
    if not held: plan['calls'] = ad.write_calls(art, writes)
    if opt(a, '--out'): Path(opt(a, '--out')).write_text(json.dumps(plan, indent=1))
    emit(plan)
    return 2 if held else 0


@cmd('import-ack')
def import_ack(a):
    """import-ack PLAN.json RECEIPTS.json --host H [--by NAME] [--raw]    record the confirmed writes of an import"""
    pos = bare(a)
    if len(pos) != 2: sys.exit(usage('import-ack'))
    ad, p, res = adapter(a)[0], read_json(pos[0]), read_json(pos[1])
    if '--raw' in a: res = ad.parse_receipt(res)
    got = {f"{r['collection']}/{r['id']}": r for r in res}
    prov, src = p['provenance'], p['bundle']['source']
    records, done, failed = dict(prov['records']), [], []
    for o in p['ops']:
        r = got.get(o['key'], {})
        if o['action'] == 'skip' and o['class'] == 'applied': records[o['key']] = {'hash': o['incomingHash'], 'revision': None}
        elif o['action'] in ('create', 'replace') and r.get('outcome') == 'applied':
            records[o['key']] = {'hash': o['incomingHash'], 'revision': r.get('revision')}; done.append(o['key'])
        elif o['action'] in ('create', 'replace'): failed.append({'key': o['key'], 'outcome': r.get('outcome', 'unknown'), 'error': r.get('error')})
    at = now()
    ops = [{'op': 'replace' if prov['exists'] else 'create', 'collection': 'imports', 'id': prov['id'], 'guard': prov['guard'],
            'data': {'schema': 'adp-import/1', 'source': src, 'bundle': src['id'], 'at': at, 'target': p['target'], 'records': records, **({'only': p['only']} if p['only'] else {})}}]
    if done:
        ops.append({'op': 'create', 'collection': 'changes', 'id': f'd-{int(time.time() * 1000)}', 'guard': None,
                    'data': {'version': '', 'at': at, 'by': opt(a, '--by', 'adp'), 'parts': [], 'threads': [],
                             'summary': f"Imported {len(done)} records from {src['host']}:{src['artifact']} (bundle {src['id']})",
                             'data': [{'doc': k} for k in done + [f"imports/{prov['id']}"]]}})
    partial = ['manifest/current was applied while another record failed: the import is partial, do not trust the artifact as synced'] * ('manifest/current' in done and bool(failed))
    emit({'applied': len(done), 'failed': failed, 'warnings': partial, 'record': ad.write_calls(p['target']['artifact'], ops)})
    return 2 if failed else 0
```

## The commands

| Command | Does | Prints | Exit |
|---|---|---|---|
| `files DIR [--since MANIFEST.json] [--batch N] [--out DIR]` | the publish arguments, as above | `{file_path, root, files}`, plus `skipped` and `kit_refs`; with `--since`, `page_changed`; over N files (default 250) `batches`, `batch_files` and `note` instead of `files` | 0 |
| `pins publish-K.json=VERSION_ID ... [--out vermap.json]` | the version map of a batched publish | `{pinned, vermap, next}`; no `KEY=VERSION` argument prints the usage line | 0; 1 for no argument |
| `files DIR --host single --out FILE [--fragment]` | packs DIR into one page | `{host: "single", out, files, bytes, fragment}` | 0; 1 for no `index.html`, a symlink or an unsupported name (each refusal names its cause) or a page over 16 MB |
| `unpack PACK DEST` | writes every file back, byte for byte, sha256 checked | `{dest, files, bytes}` | 0; 1 for a DEST that is not empty, a mismatch, an unsafe path or no blocks, with nothing written |
| `seed DIR [--by NAME] [--version V] [--data FILE\|DIR]... [--summary S] [--role R] [--at TIME] [--batches] [--dry-run]` | writes `DIR/seed.json` and `DIR/seed/pack-NNN.json` | `{seed, written, docs, collections, packs, bytes, skipped_empty, next}`; `--dry-run`: `{collections, docs, batches, skipped_empty, bytes}` and nothing written; `--batches`: `{batches, docs_dir}` and `skipped_empty` when a copy is empty, the same documents as ArtifactData batches | 0 |

The packed page's layout is [specified above](#the-packed-page), so its `bytes` is fixed for a folder whose files all have a listed extension (the
MIME of any other file is the platform's guess). The vectors check the size and the round trip: unpacking returns every file byte for byte.

Its fixtures and vectors are in [vectors.md](vectors.md).

| Command | Prints | Exit |
|---|---|---|
| `bundle --host H --artifact SRC [--collections C,...]` | `{reads: [one list call per collection]}` | 2 |
| `bundle DOCS.json OUT_DIR --host H --artifact SRC [--version V] [--by NAME] [--collections C,...] [--at TIME] [--raw]` | `{bundle, docs, dir}`; writes `OUT_DIR/seed.json` (`source {id, host, artifact, version, exportedAt, by}`, `revisions`) and the packs, sorted by collection then id; with `--raw`, `{reads}` and exit 2 while the `turns` of the requests are unread (stderr says to append their results to the same file) | 0; 1 for an incomplete or short `--raw` read, an unknown host or no artifact |
| `import-plan BUNDLE --host H --artifact DST` | `{reads}` of the target's collections and `imports` | 2 |
| `import-plan BUNDLE TARGET.json --host H --artifact DST [--only C,...] [--base BUNDLE] [--out PLAN.json]` | `adp-import-plan/1`: `bundle {id, schema, docs, source}`, `target`, `only`, `ops` (a held op says `why`), `held`, `counts`, `provenance`, `order` when `manifest/current` is written, and `calls` when nothing holds | 0; 2 when a record is held; 1 for a folder that is not a bundle or a short `--raw` read |
| `import-ack PLAN.json RECEIPTS.json --host H [--by NAME] [--raw]` | `{applied, failed, warnings, record}`; a partial import that applied `manifest/current` is warned | 0; 2 when a record failed |

Base is the hash the last import recorded for that record. A record that differs on the target with no recorded import is held: conflicts are never
resolved automatically.

Exit 2 means either that more input is needed or that something was not written. Without a reads file, `bundle` and `import-plan` print the `reads` to
run and exit 2: run them and call again with their results. `import-plan` exits 2 when a record is held, and `import-ack` when a record failed.
`TARGET.json` and `DOCS.json` are `{docs: [{collection, id, data, revision}]}`; a record the target read as absent may be written `{collection, id, exists: false, revision}`, and
its revision then guards the create (a doc with no object `data` is otherwise skipped); with `--raw` they are the host's results, `[{call, result}]`, and
the adapter parses them: a raw read that is incomplete (more pages than one) or that does not cover the collections needed is refused with exit 1, so
a record the read did not show is never taken for absent.

Its fixtures and vectors are in [vectors.md](vectors.md).

## Integrity and resumption

Every packed file carries its sha256, checked on unpack. Seeding writes `manifest/current` last, and a pack that is not served stops the run before
anything is written. Re-seeding unchanged documents leaves the seed files as they are.
