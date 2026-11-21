---
name: adp-minimal-roads
description: "Explains the four ADP roads and which job each covers: new (adp.py new), catalog (catalog, suggest, kit, take), edit (export, hold, check, files, record, ack, propose, work) and adopt (markers on an existing page, then optional move to adp/2 with a parity proof). Use when the user asks which ADP procedure fits a job, how to adopt an existing artifact, or what the command sequence of a road is."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The roads

A road is ADP's name for a fixed procedure that covers one kind of job. There are four. Every step in each is an `adp.py` command. `ADP` below is
`python3 -I adp.py`, the tool assembled from these skills ([rebuild](../adp-minimal-rebuild/SKILL.md)).

| The user wants | Road |
|---|---|
| a new page, board, tracker, assistant or record page | **new** |
| to find, take or add a component, theme, layout or pattern | **catalog** |
| to edit or publish a page others also work on, or answer its comments | **edit** |
| an existing page put on ADP | **adopt** |

On another host the same roads apply, using its native source and record calls instead of the Claude ones
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

Look in the catalog for an existing component before writing one. `ADP catalog` fetches nothing itself: it prints the reads that copy a published
catalog into `~/.adp/catalog`, the user's local copy of the kit ("My Own Kit"), which `suggest`, `kit` and `take` read. Run the reads and rerun it
until it prints `complete: true`. `CATALOG_URL` is the URL of a published catalog artifact. Details: [catalog](../adp-minimal-catalog/SKILL.md).

```sh
$ADP catalog CATALOG_URL                                # saves the URL, prints the reads; rerun until complete: true
$ADP suggest - --for "progress bar"                     # ranked by tags, name, summary, id, provides and about
$ADP kit show viz.meter                                 # header: about, files, requires, provides, tokens
$ADP kit describe viz.meter                             # the mount signature and its sample
$ADP take - viz.meter --url CATALOG_URL                 # a files map of by-reference entries, requires first
```

Merge the printed `files` map into the page's publish, add a `<link>` for each taken `.css` and a `<script src>` for each taken `.js` in the order of
`entries` (requires first, before `parts/app.js`), then `ADP check DIR`. `take` only adds files to the publish: a global such as `Kit.meter` exists
once its script has run. Adding a *new* entry is covered in [kit authoring](../adp-minimal-kit-authoring/SKILL.md).

## Edit

Several agents change the page across many versions, and the only lock is the `if_version` pin on each database write. The full steps are in the
[protocol](../adp-minimal-protocol/SKILL.md):

```sh
$ADP export DIR --url URL                  # exit 2 twice: run the printed reads each time, then rerun
$ADP manifest DIR > BEFORE.json            # right after the export, before editing: the baseline for --since
$ADP hold DIR triage.keys-table --by NAME --hours 2 --pins P.json --config C.json
# run the printed batch with ArtifactData; refused: read again and start over
# edit in DIR: keep every marker and data-part
$ADP check DIR
$ADP files DIR --since BEFORE.json         # only the changed files
# publish them to URL with a label (at most 60 characters); on a conflict, merge onto the newer version, never force
$ADP record OLD.json DIR --seq N --by NAME --summary "Keys table: sort" --version V --threads t-42 --pins P.json --config C.json
# run the printed batch(es) with ArtifactData and save the result as RESULT.json
$ADP ack DIR --result RESULT.json
# reply on each answered thread, naming V and the part ids
```

- After `export`: if `held` is above 0, stop and show both versions to the owner ([reading the result](../adp-minimal-delta/SKILL.md#reading-the-result)).
  If the page hash differs from `manifest/current.page_hash`, record that gap first. Record any new decision from the owner in `decisions/<slug>`
  before editing.
- `P.json` maps each doc you write to the version you read, e.g. `{"manifest/current": 4, "parts/home": 2}`. Once the hold's batch commits, a held
  part is one version higher; pin that version in `record`. If the output lists `needs_pin`, read those documents, add their versions and rerun.
- `C.json` is `config/current` as read; with it, `hold` and `record` refuse a locked page.
- `OLD.json` is the `manifest/current` doc as read.
- `N` is this change's sequence number, one above the last `changes/` entry; the record writes it as `changes/<NNNNNN>`.
- `V` is the version the publish returned.
- `RESULT.json` is the JSON the ArtifactData batch returned for the record write. A plain-text publish result is not accepted.
- After the record, read the page and `checks/latest` back before reporting success.

By proposal (when you must not write the record directly): `ADP propose DIR --by NAME --summary S` writes an `incoming/<pid>` for an editor to apply
([delta and inbox](../adp-minimal-delta/SKILL.md)). If `edit.locked` is true in `config/current`, make no edits and tell the user who set it; given
`--config C.json`, `hold` and `record` exit 2 with `{error: "locked", by, at, reason}`. Work claimed from `requests/` goes through `ADP work`, which
prints one pinned write per step (`claim`, `progress`, `checkpoint`, `block`, `complete`). Run the write and read the doc back. If the outcome is
unknown, read the doc and inspect it before writing again.

## Adopt

A page without part ids has no stable anchors, and its history lives only in versions. Adoption adds the part ids and the database **without
changing how the page looks or behaves**.

- **Step A, markers.** Read the latest version and save only what sits between `<body>` and `</body>` (the publish wraps it again). Wrap every view and
  main section in markers, add `data-part` and `data-comment-target`, and `ADP check`. Publish with a label and a `capabilities` that keeps what
  the page already declares plus `db: {rules: [{path: "", read: "view", write: "admin"}]}` and `user: {}` (and one rule per collection the page
  writes). Then write the first records: `ADP seed DIR --by NAME --version V --batches`, with `V` the version the publish returned (add
  `--data FILE|DIR` for the page's own data). A page without `adp.js` does not seed itself, so run the printed batches with ArtifactData,
  `manifest/current` last, and read the records back. Step A is enough for part ids and comment anchors.
- **Step B, multi-file (optional).** Start a scratch project with `ADP new minimal REF`, move the page's copy and views into `index.html`, `content.js`,
  `styles/*`, `parts/*`, and prove parity: render old and new in a headless browser and compare each element's computed style and box in every view
  and state, at the widths and themes in use. `adp.py` does not automate this comparison. Do not publish Step B until it passes.
- Never rename a published part id. Restyling is a separate change under the edit road.

## Which road when

A need that is *reusable* starts on the catalog road: search the catalog first and add a new entry only if nothing fits. A change to this page's own
copy or layout goes through the edit road.
