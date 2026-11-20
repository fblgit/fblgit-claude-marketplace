---
name: adp-minimal-roads
description: "Explains the four ADP roads and which job each covers: new (adp.py new), catalog (catalog, suggest, kit, take), edit (export, hold, check, files, record, ack, propose, work) and adopt (markers on an existing page, then optional move to adp/2 with a parity proof). Use when the user asks which ADP procedure fits a job, how to adopt an existing artifact, or what the command sequence of a road is."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The roads

A road is ADP's name for a fixed procedure that covers one kind of job. There are four. Every step in each is an `adp.py` command. `ADP` below is
`python3 -I adp.py`, a build of the tool that passes the vectors ([rebuild](../adp-minimal-rebuild/SKILL.md)).

| The user wants | Road |
|---|---|
| a new page, board, tracker, assistant or record page | **new** |
| to find, take or add a component, theme, layout or pattern | **catalog** |
| to edit or publish a page others also work on, or answer its comments | **edit** |
| an existing page put on ADP | **adopt** |

On Sites the same roads apply, using native Sites source and record calls instead of the Claude ones
([host adapters](../adp-minimal-hosts/SKILL.md)).

## New

Starting on adp/2 gives the page parts, a record and slots for catalog entries from the start. Details: [artifact layout](../adp-minimal-new-artifact/SKILL.md).

```sh
$ADP templates                                          # the installed templates: minimal, and any a catalog adds
$ADP new minimal DIR --title "Release board" --by NAME
$ADP check DIR
# publish the object `new` printed; the first editor to open the page seeds its database
```

## Catalog

Look in the catalog for an existing component before writing one. `ADP catalog` fetches it into `~/.adp/catalog`, the user's local copy of the kit
("My Own Kit"), which `suggest`, `kit` and `take` read. Details: [catalog](../adp-minimal-catalog/SKILL.md).

```sh
$ADP catalog CATALOG_URL                                # saves the URL, prints the reads that fetch the index and files
$ADP suggest - --for "sortable table with totals"       # ranked by tags, name, summary, id, provides and about
$ADP kit show kit.table                                 # header: about, files, requires, provides, tokens
$ADP kit describe kit.table                             # the mount signature and its sample
$ADP take - kit.table                                   # a files map of by-reference entries, requires first
```

Merge the printed `files` map into the page's publish, add a `<link>` for each taken `.css` and a `<script src>` for each taken `.js` in the order of
`entries` (requires first, before `parts/app.js`), then `ADP check DIR`. `take` only adds files to the publish: a global such as `Kit.table` exists
once its script has run. Adding a *new* entry is covered in [kit authoring](../adp-minimal-kit-authoring/SKILL.md).

## Edit

Several agents change the page across many versions, and the only lock is the `if_version` pin on each database write. The full steps are in the
[protocol](../adp-minimal-protocol/SKILL.md):

```sh
$ADP export DIR --url URL                  # first run prints the reads (exit 2); rerun with --files-listing F.json --docs D.json
$ADP manifest DIR > BEFORE.json            # right after the export, before editing: the baseline for --since
$ADP hold DIR triage.keys-table --by NAME --hours 2 --pins P.json
# edit in DIR: keep every marker and data-part
$ADP check DIR
$ADP files DIR --since BEFORE.json         # only the changed files, for the publish
$ADP record OLD.json DIR --seq N --by NAME --summary "Keys table: sort" --pins P.json
$ADP ack DIR --result RESULT.json
```

- `P.json` maps each doc you write to the version you read, e.g. `{"manifest/current": 4, "parts/home": 2}`. Once the hold's batch commits, a held
  part is one version higher; pin that version in `record`.
- `OLD.json` is the `manifest/current` doc as read.
- `N` is this change's sequence number; the record writes it as `changes/<NNNNNN>`.
- `RESULT.json` is the JSON the ArtifactData batch returned for the record write. A plain-text publish result is not accepted.

By proposal (when you must not write the record directly): `ADP propose DIR --by NAME --summary S` writes an `incoming/<pid>` for an editor to apply
([delta and inbox](../adp-minimal-delta/SKILL.md)). If `edit.locked` is true in `config/current`, make no edits and tell the user who set it; given
`--config C.json`, `hold` and `record` exit 2 with `{error: "locked", by, at, reason}`. Work claimed from `requests/` goes through `ADP work`, which
prints one pinned write per step (`claim`, `progress`, `checkpoint`, `block`, `complete`). Run the write and read the doc back. If the outcome is
unknown, read the doc and inspect it before writing again.

## Adopt

A page without part ids has no stable anchors, and its history lives only in versions. Adoption adds the part ids and the database **without
changing how the page looks or behaves**.

- **Step A, markers.** Read the latest version and save only what sits between `<body>` and `</body>` (the publish wraps it again). Wrap every view and
  main section in markers, add `data-part` and `data-comment-target`, `ADP check`, publish with a label and a `capabilities` that keeps what the page
  already declares plus `{path: "", read: "view", write: "admin"}` (and one rule per collection the page writes). Seed with
  `ADP seed DIR --by NAME --data FILE|DIR`. Step A is enough for part ids and comment anchors.
- **Step B, multi-file (optional).** Start a reference project with `ADP new minimal REF`, move the page's copy and views into `index.html`, `content.js`,
  `styles/*`, `parts/*`, and prove parity: render old and new in a headless browser and compare each element's computed style and box in every view
  and state, at the widths and themes in use. `adp.py` does not automate this comparison. Do not publish Step B until it passes.
- Never rename a published part id. Restyling is a separate change under the edit road.

## Which road when

A need that is *reusable* starts on the catalog road: search the catalog first and add a new entry only if nothing fits. A change to this page's own
copy or layout goes through the edit road.
