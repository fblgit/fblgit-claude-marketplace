---
name: adp-minimal-roads
description: "Explains the four ADP roads and which job each covers: new (adp.py new), catalog (catalog, suggest, kit, take), edit (export, hold, check, files, record, ack, propose, work) and adopt (markers on an existing page, then optional move to adp/2 with a parity proof). Use when the user asks which ADP procedure fits a job, how to adopt an existing artifact, or what the command sequence of a road is."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# The roads

Every job done with ADP (building a page, reusing or adding to the catalog, editing, bringing an existing page in) follows one of these.

A road is a short, complete procedure for one kind of job. There are four, and every job on a page is one of them. Each names `adp.py` commands; none
is done by hand. `ADP` below is `python3 -I <adp skill folder>/scripts/adp.py`.

| The user wants | Road |
|---|---|
| a new page, board, tracker, assistant or record | **new** |
| to find, take or add a component, theme, layout or pattern | **catalog** |
| to edit or publish a page others also work on, or answer its comments | **edit** |
| an existing page put on ADP | **adopt** |

Choose the host as well as the road. On Sites the same roads apply, with native Sites source and record calls in place of the Claude ones
([host adapters](../adp-minimal-hosts/SKILL.md)).

## New

Why: start on adp/2 so the page has parts, a record and a place for the catalog's pieces from the first minute. Detail in
[artifact layout](../adp-minimal-new-artifact/SKILL.md).

```sh
$ADP templates                                          # starter, assistant, default
$ADP new assistant DIR --title "Release board" --by me --theme default --catalog CATALOG
$ADP check DIR
# publish the object `new` printed; the first editor to open the page seeds its database
```

## Catalog

Why: the catalog already holds what you were about to write. Detail in [catalog](../adp-minimal-catalog/SKILL.md).

```sh
$ADP catalog CATALOG_URL                                # save it and fetch the index into ~/.adp/catalog (My Own Kit)
$ADP suggest - --for "sortable table with totals"       # ranked by tags, name, summary, provides
$ADP kit show kit.table                                 # header: about, files, requires, provides, tokens
$ADP kit describe kit.table                             # the mount signature and its sample
$ADP take - kit.table                                   # a files map of by-reference entries, requires first
```

Merge the printed `files` map into the page's publish, add a `<link>` for each taken `.css` and a `<script src>` for each taken `.js` in the order of
`entries` (requires first, before `parts/app.js`), then `ADP check DIR`. A taken file is served, not loaded: a global such as `Kit.table` exists only
after its script ran. Adding a *new* entry is the job of [kit authoring](../adp-minimal-kit-authoring/SKILL.md).

## Edit

Why: several agents change the page over many versions; the `if_version` pin is the only lock. The steps are the [protocol](../adp-minimal-protocol/SKILL.md):

```sh
$ADP export DIR --url URL                  # two-step: prints the reads, then builds DIR.adp/ with base, live and work
$ADP hold DIR triage.keys-table --by me --hours 2 --pins P.json
# edit in DIR: keep every marker and data-part
$ADP check DIR && $ADP manifest DIR
$ADP files DIR --since BEFORE.json         # only the changed files, for the publish
$ADP record OLD.json DIR --seq 8 --by me --summary "Keys table: sort" --pins P.json
$ADP ack DIR --result RESULT.json
```

By proposal (when you must not write the record directly): `ADP propose DIR --by me --summary S` writes an `incoming/<pid>` for an editor to apply
([delta and inbox](../adp-minimal-delta/SKILL.md)). `edit.locked` stops everything: tell the user who locked it. Work claimed from `requests/` goes through
`ADP work`, which prints one pinned write per step (`claim`, `progress`, `checkpoint`, `block`, `complete`) and never retries an unknown outcome blindly.

## Adopt

Why: a page without part ids has no stable anchors and its history lives only in versions. Adoption adds the part ids and the database **without
changing how the page looks or behaves**.

- **Step A, markers.** Read the latest version and save only what sits between `<body>` and `</body>` (the publish wraps it again). Wrap every view and
  main section in markers, add `data-part` and `data-comment-target`, `ADP check`, publish with a label and a `capabilities` that keeps what the page
  already declares plus `{path: "", read: "view", write: "admin"}` (and one rule per collection the page writes). Seed with
  `ADP seed DIR --by me --data FILE|DIR`. This alone gives part ids and comment anchors.
- **Step B, multi-file (optional).** Start a reference project with `ADP new starter REF`, move the page's copy and views into `index.html`, `content.js`,
  `styles/*`, `parts/*`, and **prove parity**: render old and new in a headless browser and compare every element's computed style and box in every view,
  state, width and theme in use. No parity proof, no publish.
- Never rename a published part id. Restyling is a separate change under the edit road.

## Which road when

A new need that is *reusable* starts on the catalog road: look, then take, and only then add. A need that is only this page's copy or layout is the
edit road. Nothing is built outside a road.
