---
name: adp-minimal-packing
description: "Reference for ADP pack formats and record transfer: the one-file page (adp.py files --host single, its loader shim, unpack), seed packs (adp-seed/2), catalog packs (adp-catalog-pack/1), and record bundles moved between hosts with bundle, import-plan and import-ack. Use when the user asks how to ship a page as one file, restore files from a pack, what seed.json is, or how to move a page's records from Claude to Sites and back."
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

## One-file page

```sh
$ADP files DIR --host single --out index.html          # --fragment for the Artifact tool: it adds doctype, html, head, body
$ADP unpack index.html RESTORED/                       # every file back, sha256 checked; DEST must be new or empty
```

Every file is embedded once, with its sha256, in a block of the packed `index.html`. A small loader script, the **shim**, serves the page's
relative `<script src>` and `<link rel=stylesheet>` from those blocks, and answers `GET` and `HEAD` `fetch()` calls for packed paths. It uses only
inline scripts and styles, because the claude.ai sandbox blocks `blob:` and `data:` stylesheets and `data:` scripts. Not supported: module scripts,
relative images and CSS `url()`, and a page over 16 MB.

### The packed page

**Files.** Every file under DIR, walked in sorted order (folders and names sorted, entries starting with `.` skipped), with `/` separators. A
symbolic link, or a path outside `[A-Za-z0-9._/@+-]+`, is refused. DIR must have an `index.html`.

**Blocks.** One per file, `index.html` included (its original bytes, before the rewriting below), in that order, joined with nothing between
them:

```html
<script type="application/adp-file" data-adp-file="PATH" data-type="MIME" data-enc="utf8|b64" data-sha256="64 HEX" data-bytes="N">BODY</script>
```

`data-enc` is `utf8`, and BODY the file's text, when the file is valid UTF-8 and contains no `\r`, no NUL, no `</script` and no `<!--` (case
insensitive); otherwise it is `b64` and BODY the standard base64 of the bytes, on one line, with `=` padding. `data-sha256` and `data-bytes` are of the file's bytes. MIME is
`text/javascript` (`.js`, `.mjs`), `text/css`, `application/json`, `text/html`, `image/svg+xml`, `text/plain` (`.txt`), else the platform's
guess, else `application/octet-stream`.

**Rewriting `index.html`.** When it has both a `<head ...>...</head>` and a `<body ...>...</body>`, their contents are used; otherwise (a
fragment, or only one of the two) the whole file is the body and HEAD is empty. Attributes are read as `name`, `name=value`, `name="value"` or
`name='value'`, names compared case-insensitively, quotes removed. In both HEAD and BODY:

- an empty `<script ...></script>` whose `src` (without `?` or `#` part) is exactly a packed path as listed above (no `./`, no `/` prefix, no
  other normalization), and is not `type=module`, becomes
  `<script>ADPPACK.js("PATH")</script>`; with a `defer` attribute it is removed from its place and appended after the body;
- a `<link ...>` whose `rel` is exactly `stylesheet` (case-insensitive) and whose `href`, matched the same way, names a packed file becomes `<script>ADPPACK.css("PATH")</script>`;
- everything else is kept as is. `PATH` is written as a JSON string.

The head's `<title>` (or `<title>Page</title>` when it has none) and every `<meta charset>` are taken out of the head. The page is then:

```
<!doctype html>\n<html ATTRS><head><meta charset="utf-8">TITLE BLOCKS SHIM HEAD</head><body ATTRS>BODY DEFERRED</body></html>\n
```

with nothing between the pieces. ATTRS is the original tag's attribute text exactly as written, leading whitespace included (`<html lang="en">`
stays `<html lang="en">`), and empty when the tag is absent. SHIM is `<script>`, the code block below as written (its lines joined with `\n`,
the indented line keeping its space), then `</script>`. `--fragment` writes only `TITLE BLOCKS SHIM HEAD BODY DEFERRED`, for a tool that adds the document skeleton
itself. A page over 16 × 1024 × 1024 bytes is refused. `bytes` in the output is the page's length in UTF-8.

**The shim.** It indexes the blocks by path, and installs `window.ADPPACK` (`css(path)` and `js(path)` insert a `<style>` or `<script>` with
the file's text before the calling script; `js` appends `//# sourceURL=PATH`) and a `fetch` that answers `GET` and `HEAD` for a packed path
relative to the page with status 200 and the block's `data-type`, passing every other call to the original:

```js
(function(){var B={};document.querySelectorAll('script[data-adp-file]').forEach(function(s){B[s.getAttribute('data-adp-file')]=s});
function raw(p){var s=B[p];if(!s)throw new Error('adp-pack: no file '+p);if(s.dataset.enc==='utf8')return new TextEncoder().encode(s.textContent);var b=atob(s.textContent),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u}
function text(p){var s=B[p];return s.dataset.enc==='utf8'?s.textContent:new TextDecoder().decode(raw(p))}
function put(tag,p,t){var e=document.createElement(tag);e.textContent=t;var c=document.currentScript;c.parentNode.insertBefore(e,c)}
window.ADPPACK={files:B,css:function(p){put('style',p,text(p))},js:function(p){put('script',p,text(p)+'\n//# sourceURL='+p)}};
var f=window.fetch,base=new URL('.',document.baseURI).href;
window.fetch=function(u,o){var a=String(u&&u.url||u),m=((o&&o.method)||(u&&u.method)||'GET').toUpperCase();
 try{a=new URL(a,document.baseURI).href}catch(e){}
 var p=a.indexOf(base)===0?a.slice(base.length).split(/[?#]/)[0]:null;
 if(p&&B[p]&&(m==='GET'||m==='HEAD'))return Promise.resolve(new Response(m==='HEAD'?null:raw(p),{status:200,headers:{'content-type':B[p].dataset.type}}));
 return f.apply(this,arguments)}})()
```

**Unpacking** reads every block, decodes it, and refuses the whole pack (nothing written) when a hash or length differs or a path is unsafe
(absolute, `..`, or outside the character set above).

## Seed packs

`seed.json` is the index (`schema: adp-seed/2`, `version`, `by`, `at`, `docs`, `collections` counts, `packs` paths). Each `seed/pack-NNN.json` is:

```json
{ "schema": "adp-seed/2", "pack": 1, "of": 3,
  "docs": [ {"collection": "parts", "id": "home.lead", "data": {"title": "Lead", "hash": "0f1e2d3c4b5a"}},
            {"collection": "manifest", "id": "current", "data": {"schema": "adp/2", "version": 1}} ] }
```

Documents are cut into packs in order, so `manifest/current` is the last document of the last pack. A new pack starts when the next document would
take the current one past 1,500,000 bytes of UTF-8 JSON (a larger document gets a pack of its own). Additional collections can be seeded: `adp.py seed DIR --data FILE`, with `{collection, id, data}` documents, writes them to the database on the
first open too. The seed files are published with the page and never appear in the manifest.

## Catalog packs

A catalog is hundreds of files. Where a channel limits how many files it carries, the catalog travels as `catalog-pack-NN.json` files:
`{"schema": "adp-catalog-pack/1", "files": {path: text}}`, UTF-8 text only, a new pack starting when the next file would take the current one
past 921,600 characters of text. `adp.py unpack PACK DEST` writes one pack's files into an empty DEST; a path that is absolute or contains `..`
is skipped. A published catalog ships its kit the same way as a page ships its records: its seed carries the kit folders as inbox proposals
([delta and inbox](../adp-minimal-delta/SKILL.md)), applied one at a time when an editor opens the page.

## Moving records between hosts: bundle, plan, acknowledge

A bundle reuses the seed format and adds provenance (`source`: host, artifact, publication version, export time, author, bundle hash). The shell builds
bundles, classifies records and records provenance. A host adapter translates its plans into the host's read and conditional-write calls, which the
agent executes. There is no automatic sync.

```sh
$ADP bundle --host claude --artifact SOURCE                 # prints the reads; save the results as source-reads.json
$ADP bundle source-reads.json bundle-dir --host claude --artifact SOURCE --version V --raw
$ADP import-plan bundle-dir --host sites --artifact TARGET  # prints the target reads
$ADP import-plan bundle-dir target-reads.json --host sites --artifact TARGET --raw --out plan.json
# run the plan's calls in order, saving [{call, result, readback}] as results.json
$ADP import-ack plan.json results.json --host sites --raw
```

- It covers `manifest`, `parts`, `content`, `changes`, `decisions`, `config`, `agents`, `incoming`, `requests` and each request's `turns`; not presence,
  status, or the shell's own `imports` records.
- Planning uses the three-way classification of [the delta](../adp-minimal-delta/SKILL.md#the-classification): base is the last imported hash in
  `imports/<source>`, live is the target, incoming is the bundle. New records are created, source-only changes replace, equal records are skipped,
  target-only changes stay. Conflicting changes are **held**: not written, and the plan exits 2 with no calls.
- It never deletes records. Source revisions are kept for provenance only; every write is conditioned on a revision from a fresh read of the target.
- `import-ack` reports *applied* only when the write result **and** the readback match. A write with no receipt is *unknown*: it is not recorded, and
  the next `import-plan`, from a fresh read, classifies it again.
- The bundle carries records, not source files: publish the page with `adp.py files` and the host's own publication.

## Integrity and resumption

Every packed file carries its sha256, checked on unpack. Seeding writes `manifest/current` last, and a pack that is not served stops the run before
anything is written. Re-seeding unchanged documents leaves the seed files as they are.

## Contract: `files`, `files --host single`, `unpack`, `seed`

| Command | Does | Prints | Exit |
|---|---|---|---|
| `files DIR [--since MANIFEST.json] [--batch N] [--out DIR]` | the publish arguments: every served file of DIR mapped to itself, `index.html` as `file_path`; `--since` keeps only files whose hash differs from MANIFEST's `files` (a removed file maps to `null`) | `{file_path, root, files}`, plus `skipped` for files the service does not serve; with `--since`, `page_changed: true` when `index.html` itself changed (it is the `file_path`, never in `files`); over N files (default 250) `batches` instead of `files` | 0 |
| `files DIR --host single --out FILE [--fragment]` | packs DIR into one HTML page: every file embedded once with its sha256, served by the one-file shim | `{host: "single", out, files, bytes, fragment}` | 0 |
| `unpack PACK DEST` | writes every file of a packed page (or a `catalog-pack-NN.json`) back, byte for byte, sha256 checked; DEST must be new or empty | `{dest, files, bytes}` | 0; 1, with the reason on stderr and nothing written, when DEST is not empty or a hash does not match |
| `seed DIR --by NAME [--version V] [--data FILE\|DIR ...] [--summary S] [--role R] [--batches] [--dry-run]` | writes `DIR/seed.json` and `DIR/seed/pack-NNN.json` (`adp-seed/2`): `parts/<id>` for every part except `_rest`, `content/<id>` for non-empty copy, `changes/000001`, `agents/<NAME>`, then `manifest/current` last | `{seed, written, docs, collections, packs, bytes, skipped_empty, next}`; `--dry-run`: `{collections, docs, batches, skipped_empty, bytes}` and nothing written; `--batches`: the same documents as ArtifactData batches | 0 |

The packed page's layout is [specified above](#the-packed-page), so its `bytes` is fixed for a folder whose files all have a listed extension (the
MIME of any other file is the platform's guess). The vectors check the size and the round trip: unpacking returns every file byte for byte.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `files`, `files --host single`, `unpack`, `seed`".

## Contract: moving records (`bundle`, `import-plan`, `import-ack`)

Records move between two artifacts (on one host or two) as a bundle: an `adp-seed/2` seed with `source` and `revisions` added. The shell is
host-neutral; a **host adapter** module (`adp_<host>_adapter.py`: `read_calls`, `parse_reads`, `write_calls`, `parse_receipt`) turns its plans into the
host's calls and parses what they return. A [rebuild](../adp-minimal-rebuild/SKILL.md) needs the shell plus one adapter per supported host. Files are never moved this way: publish them
with `files`.

| Command | Prints | Exit |
|---|---|---|
| `bundle --host H --artifact SRC` | `{reads: [one list call per collection: manifest, parts, content, changes, decisions, config, agents, incoming, requests]}` | 2 |
| `bundle DOCS.json OUT_DIR --host H --artifact SRC [--version V] [--by NAME] [--raw]` | `{bundle: "b-<12 hex of the records' hash>", docs, dir}`; writes `OUT_DIR/seed.json` (`source {id, host, artifact, version, exportedAt, by}`, `revisions`) and the packs, sorted by collection then id, without `status`, `presence`, `imports` | 0; 1 when a `--raw` read is incomplete or misses a collection |
| `import-plan BUNDLE --host H --artifact DST` | `{reads}` of the target's collections | 2 |
| `import-plan BUNDLE TARGET.json --host H --artifact DST [--out PLAN.json] [--base OLD_BUNDLE] [--only c,..]` | `adp-import-plan/1`: per record, the loop's three-way classification of (base, live, incoming) over canonical hashes (`sha256:` of the sorted JSON): `new` creates, `ours` replaces (pinned to the target's revision), `applied`/`theirs` skip, anything else is **held**; `manifest/current` last; `calls` only when nothing holds | 0; 2 with `held` and no `calls` |
| `import-ack PLAN.json RECEIPTS.json --host H [--raw]` | `{applied, failed, warnings, record}`: `record` writes `imports/<host-artifact>` (`adp-import/1`, only confirmed records) and a `changes/d-<ms>`; a partial import that applied `manifest/current` is warned | 0; 2 when a record failed |

Base is the hash the last import recorded for that record (or, with `--base`, the bundle this one came back from). A record that differs on the target
with no recorded import is held: conflicts are never resolved automatically.

Exit 2 means either that more input is needed or that something was not written. Without a reads file, `bundle` and `import-plan` print the `reads` to run and exit 2: run them and call again with
their results. `bundle` also exits 2, with a note on stderr, when the reads cover `requests` but not each request's `turns`: append the results of the
printed reads to the same file and run it again. With a reads file, `import-plan` exits 2 when a record is held, and `import-ack` when a record failed.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: moving records (`bundle`, `import-plan`, `import-ack`)".

## Contract: publishing in batches (`files --batch`, `pins`)

A publish takes at most 255 files. Over `--batch N` files (default 250), `files` prints `batches` instead of `files` (the page stays `file_path`; every
batch is also written to `DIR.adp/publish-K.json`) and a `note`; the agent publishes the page with the first batch and every other batch to the same url, noting
each version id the tool returns. `pins publish-K.json=VERSION_ID ... [--out vermap.json]` turns those into `{path: version id}` (default
`DIR.adp/vermap.json`), the map a catalog's distribution uses to reference each file at the version that holds it. No tool in this specification
reads it.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: publishing in batches (`files --batch`, `pins`)".
