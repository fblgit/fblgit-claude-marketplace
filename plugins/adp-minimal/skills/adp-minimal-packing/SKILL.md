---
name: adp-minimal-packing
description: "Explains ADP packing and unpacking as fast, verified transport: the one-file page (adp.py files --host single, the shim, unpack), seed packs (adp-seed/2), catalog packs inside a skill zip, and record bundles moved between hosts with bundle, import-plan and import-ack. Use when the user asks how to ship a page as one file, restore files from a pack, what seed.json is, or how to move a page's records from Claude to Sites and back."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Packing and unpacking: moving a page faster

Pages, their records and the catalog all have to move: to a tool that publishes one file, into a fresh database, into a skill zip, or to another host.

A page is many small files. Publishing, copying and fetching them one by one is slow and fails halfway. ADP packs them into a few files, and unpacks
them byte for byte. There are four packings, for four jobs.

| Packing | For | Made by | Undone by |
|---|---|---|---|
| **One-file page** | a tool that can publish only one file | `adp.py files DIR --host single` | `adp.py unpack PACK DEST` |
| **Seed packs** | the first database documents of a page | `adp.py new`, `adp.py seed` | the page itself, on the first editor open |
| **Catalog packs** | the catalog inside a skill zip (a zip allows at most 200 files, and may not hold a zip) | the package build | `adp.py setup`, or `adp.py unpack` |
| **Record bundle** | a page's records moving between hosts | `adp.py bundle` | `adp.py import-plan`, `import-ack` |

## One-file page

```sh
$ADP files DIR --host single --out index.html          # --fragment for the Artifact tool: it adds doctype, html, head, body
$ADP unpack index.html RESTORED/                       # every file back, sha256 checked; DEST must be new or empty
```

Every file is embedded once, with its sha256, in a block of the packed `index.html`. A small **shim** (`assets/hosts/single/shim.js`) serves the page's
relative `<script src>`, `<link rel=stylesheet>` and `fetch()` from those blocks. It uses only inline scripts and styles, because the claude.ai sandbox
blocks `blob:` and `data:` stylesheets and `data:` scripts. Not supported: module scripts, relative images and CSS `url()`, and a page over 16 MB.

## Seed packs

`seed.json` is the index (`schema: adp-seed/2`, `version`, `by`, `at`, `docs`, `collections` counts, `packs` paths). Each `seed/pack-NNN.json` is:

```json
{ "schema": "adp-seed/2", "pack": 1, "of": 3,
  "docs": [ {"collection": "parts", "id": "home.lead", "data": {"title": "Lead", "hash": "0f1e2d3c4b5a"}},
            {"collection": "manifest", "id": "current", "data": {"schema": "adp/2", "version": 1}} ] }
```

A pack holds up to about 1.5 MB of JSON; documents are cut into packs in order, so `manifest/current` is the last document of the last pack. Extra
collections ride along: `adp.py seed DIR --data FILE` with `{collection, id, data}` documents puts them in the database on the first open. The files
are published with the page and never appear in the manifest.

## Catalog packs

The catalog is hundreds of files; a skill zip may hold 200. The build packs the catalog as `adp/catalog-pack-NN.json` (`{"schema": "adp-catalog-pack/1",
"files": {path: text}}`, split near 900 KB, text only), and `adp.py setup` unpacks them into `~/.adp/catalog`, never overwriting a file already there. A
published catalog ships the same way: its seed carries the kit folders as inbox proposals ([delta and inbox](../adp-minimal-delta/SKILL.md)), applied one at a time
on an editor's open.

## Moving records between hosts: bundle, plan, acknowledge

A bundle reuses the seed format and adds provenance (`source`: host, artifact, publication version, export time, author, bundle hash). The shell owns
bundles, classification and provenance; an adapter turns them into native reads and guarded writes; an agent runs the calls. Nothing syncs by itself.

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
- Planning uses the same classification as the loop: base is the last imported hash in `imports/<source>`, live the target, incoming the bundle. New
  creates, source-only changes replace, equal skips, target-only stays, competing changes **hold** (exit 2, no writes).
- It never deletes records. Source revisions are evidence, never guards for the target: fresh target revisions guard every write.
- `import-ack` reports *applied* only when the write result **and** the readback match; a lost response is *unknown*, to be read, not retried.
- The bundle carries records, not source files: publish the page with `adp.py files` and the host's own publication.

## Why this is faster

Fewer, larger transfers; each verified by hash; each resumable (seeding writes `manifest/current` last, a pack that is not served stops the run before
anything is written, an unchanged document leaves its file alone).

## Contract: `files`, `files --host single`, `unpack`, `seed`

| Command | Does | Prints | Exit |
|---|---|---|---|
| `files DIR [--since MANIFEST.json] [--batch N] [--out DIR]` | the publish arguments: every served file of DIR mapped to itself, `index.html` as `file_path`; `--since` keeps only files whose hash differs from MANIFEST's `files` (a removed file maps to `null`) | `{file_path, root, files}`, plus `skipped` for files the service does not serve; with `--since`, `page_changed: true` when `index.html` itself changed (it is the `file_path`, never in `files`); over N files (default 250) `batches` instead of `files` | 0 |
| `files DIR --host single --out FILE [--fragment]` | packs DIR into one HTML page: every file embedded once with its sha256, served by the one-file shim | `{host: "single", out, files, bytes, fragment}` | 0 |
| `unpack PACK DEST` | writes every file of a packed page (or a `catalog-pack-NN.json`) back, byte for byte, sha256 checked; DEST must be new or empty | `{dest, files, bytes}` | 0; 1, with the reason on stderr and nothing written, when DEST is not empty or a hash does not match |
| `seed DIR --by NAME [--version V] [--data FILE\|DIR ...] [--summary S] [--role R] [--batches] [--dry-run]` | writes `DIR/seed.json` and `DIR/seed/pack-NNN.json` (`adp-seed/2`): `parts/<id>` for every part except `_rest`, `content/<id>` for non-empty copy, `changes/000001`, `agents/<NAME>`, then `manifest/current` last | `{seed, written, docs, collections, packs, bytes, skipped_empty, next}`; `--dry-run`: `{collections, docs, batches, skipped_empty, bytes}` and nothing written; `--batches`: the same documents as ArtifactData batches | 0 |

The pack's exact bytes are the shim's and are not pinned here: the vector pins the round trip instead, which is what a rebuild must keep.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: `files`, `files --host single`, `unpack`, `seed`".

## Contract: moving records (`bundle`, `import-plan`, `import-ack`)

Records move between two artifacts (on one host or two) as a bundle: an `adp-seed/2` seed with `source` and `revisions` added. The shell is
host-neutral; a **host adapter** module (`adp_<host>_adapter.py`: `read_calls`, `parse_reads`, `write_calls`, `parse_receipt`) turns its plans into the
host's calls and parses what they return. A rebuild needs the shell and one adapter per host it serves. Files are never moved this way: publish them
with `files`.

| Command | Prints | Exit |
|---|---|---|
| `bundle --host H --artifact SRC` | `{reads: [one list call per collection: manifest, parts, content, changes, decisions, config, agents, incoming, requests]}` | 2 |
| `bundle DOCS.json OUT_DIR --host H --artifact SRC [--version V] [--by NAME] [--raw]` | `{bundle: "b-<12 hex of the records' hash>", docs, dir}`; writes `OUT_DIR/seed.json` (`source {id, host, artifact, version, exportedAt, by}`, `revisions`) and the packs, sorted by collection then id, without `status`, `presence`, `imports` | 0; 1 when a `--raw` read is incomplete or misses a collection |
| `import-plan BUNDLE --host H --artifact DST` | `{reads}` of the target's collections | 2 |
| `import-plan BUNDLE TARGET.json --host H --artifact DST [--out PLAN.json] [--base OLD_BUNDLE] [--only c,..]` | `adp-import-plan/1`: per record `classify3(base, live, incoming)` over canonical hashes (`sha256:` of the sorted JSON): `new` creates, `ours` replaces (pinned to the target's revision), `applied`/`theirs` skip, the rest **holds**; `manifest/current` last; `calls` only when nothing holds | 0; 2 with `held` and no `calls` |
| `import-ack PLAN.json RECEIPTS.json --host H [--raw]` | `{applied, failed, warnings, record}`: `record` writes `imports/<host-artifact>` (`adp-import/1`, only confirmed records) and a `changes/d-<ms>`; a partial import that applied `manifest/current` is warned | 0; 2 when a record failed |

Base is the hash the last import recorded for that record (or, with `--base`, the bundle this one came back from). A record that differs on the target
with no recorded import is held: the shell never guesses which side wins.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: moving records (`bundle`, `import-plan`, `import-ack`)".

## Contract: publishing in batches (`files --batch`, `pins`)

A publish takes at most 255 files. Over `--batch N` files (default 250), `files` prints `batches` instead of `files` (the page stays `file_path`; every
batch is also written to `DIR.adp/publish-K.json`) and a `note`; the agent publishes the page with the first batch and every other batch to the same url, noting
each version id the tool returns. `pins publish-K.json=VERSION_ID ... [--out vermap.json]` turns those into `{path: version id}` (default
`DIR.adp/vermap.json`), the map a catalog uses to reference each file at the version that holds it.

Its fixtures and vectors are in [vectors.md](vectors.md), under "Contract: publishing in batches (`files --batch`, `pins`)".
