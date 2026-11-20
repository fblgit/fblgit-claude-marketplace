---
name: adp-minimal
description: "What ADP (Artifacts Done Properly) is and why: the standard for shared Claude Artifacts and Sites pages that several people and agents keep editing, its four pieces (parts, the record, the protocol, the kit), what it preserves, its vocabulary, and the rule that pages are built and changed through ADP, never by hand. Use when the user asks what ADP is, why it exists, how its pieces fit, or wants work done on a page and the ADP tools may not be installed."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# What ADP is

ADP (Artifacts Done Properly) is a standard for a Claude Artifact, or a Sites page, that more than one person or agent keeps working on. It is a set of
conventions plus one small runtime; it is not a service and not a UI framework. A page stays plain HTML, CSS and JavaScript.

This plugin explains ADP; each topic is its own skill (below). ADP itself (`adp.py`, the catalog, the templates, the runtime) is the full plugin:

    /plugin marketplace add fblgit/artifacts-done-properly
    /plugin install artifacts-done-properly@fblgit-adp

## The problem

A shared page is edited over many versions by sessions that cannot see each other. Without a standard:

- a session works from a stale copy and its publish overwrites someone else's change;
- a comment says "I'll fix it" and nobody does;
- a comment anchored to a CSS path loses its place the day the layout changes;
- the same table, tabs or chart is retyped, slightly differently, on every page.

## The answer, in four pieces

| Piece | What it is |
|---|---|
| **Parts** | Every piece of the page has a stable id and a content hash. Comments anchor to part ids, not to CSS paths. |
| **The record** | One database layout (manifest, parts, content, changes, decisions, agents ...) says what the page is and what changed. |
| **The protocol** | Read, hold, edit, check, publish, record. The only lock is the `if_version` pin on a write. |
| **The kit** | Shared, versioned building blocks (components, layouts, patterns, visualisations, themes) with a header, in a catalog. A page takes them; nobody retypes them. |

In one picture: a part, its recorded hash, and the write that is refused when someone got there first.

```html
<!-- part:triage.keys-table --> <section data-part="triage.keys-table">...</section> <!-- /part:triage.keys-table -->
```
```json
{"collection": "parts", "doc_id": "triage.keys-table", "if_version": 3, "data": {"hash": "1234567890ab", "holder": ""}}
```

## What ADP preserves

Not only the bytes. A page on ADP keeps its **intent** (decisions, quoted verbatim), its **feedback** (threads and requests), its **history**
(`changes/`), its **provenance** (who, when, from which version) and the safe way to evolve it (holds, proposals, classification). Open the page in a
new session, on another host, a month later: all of it is still there.

## The rule

`adp.py` is one Python 3 command on the standard library. It computes hashes and diffs, lays a page out, takes catalog entries, and **prints** the exact
`Artifact` / `ArtifactData` calls to make; an agent runs them. Nothing is retyped, so nothing is mistyped.

**A page is created, edited, themed and published through ADP, never by hand outside it.** A hand edit has no part ids, no hashes, no record and no
hold; it is the stale overwrite ADP exists to prevent. A reusable need becomes a kit entry (once, general, with several samples), not a one-off.

When the user wants work done on a page and `adp.py` is not available here:

- say so, and give the two install lines above;
- do not improvise a build, an edit or a publish, and do not claim you wrote, held or published anything;
- you may still **plan** the work in ADP terms: the road, the commands it would run, the part ids affected, the revision guards (`if_version`, or "not known:
  read it first"), and the order with `manifest/current` last. Label every payload as an example and say what you did not verify.

When the live tools are present (`Artifact`, `ArtifactData` and `adp.py`), follow the road and the protocol exactly.

## Vocabulary, and the skill that explains each

| Term | In a line | Skill |
|---|---|---|
| Part, hash, anchor | the text between two markers, with an id; its content hash; comments pinned to it | `adp-minimal-parts` |
| Snippets | the hash and diff arithmetic as runnable Python | `adp-minimal-snippets` |
| Protocol, record | read, hold, edit, check, publish, record; the documents ADP keeps | `adp-minimal-protocol` |
| Payloads | those documents and calls written out as JSON | `adp-minimal-payloads` |
| New artifact | `adp.py new`, the adp/2 file tree, tiers, seeding | `adp-minimal-new-artifact` |
| Shell, runtime | the thin `index.html` and `adp.js`, the one script every page loads | `adp-minimal-runtime` |
| Host adapter | the boundary between the page and its host; what components may rely on | `adp-minimal-hosts` |
| Road | a short procedure for one kind of job: new, catalog, edit, adopt | `adp-minimal-roads` |
| Delta, inbox | the classified difference of base, live and incoming; where proposals wait | `adp-minimal-delta` |
| Packing | one-file pages, seed packs, catalog packs, record bundles | `adp-minimal-packing` |
| Kit | components, layouts, patterns, viz, samples, and how they wire | `adp-minimal-kit` |
| Theme, tokens | the look as CSS custom properties every kit file draws with | `adp-minimal-themes` |
| Catalog | the index of kit entries, their headers and the consistency checks | `adp-minimal-catalog` |
| Kit authoring | adding a general entry with several samples, instead of a one-off | `adp-minimal-kit-authoring` |
| Rebuild | the tooling's contracts, vectors and the runner that proves a rebuilt `adp.py`, `adp.js` or catalog tool | `adp-minimal-rebuild` |

## Always

- Read the latest version of an artifact before touching it; a local copy from an earlier session may predate other people's work.
- Say what you did not verify. Hashes computed in your head, or with a snippet, were not checked by `adp.py`: say so.
- Never invent a command. If a page says to run `adp.py` and it is not installed, the command is not available here.
- Calls to `Artifact` and `ArtifactData` are the Claude host's; another host has its own, and the order of the steps and the `if_version` pin stay the same.
