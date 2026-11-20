# ADP minimal

A Claude Artifact that several people and agents keep editing breaks in familiar ways: someone publishes over a newer version, a comment loses
its place when the layout changes, the same table gets rewritten on every page. ADP (Artifacts Done Properly) is a set of conventions that
prevents this: every piece of the page has a stable id, every change is recorded, and a write is refused if someone else got there first.

This plugin teaches ADP. Ask Claude how any part of it works and the guide for that topic loads, with short examples. It is Markdown only and
installs nothing. For readers who want to go further, it also describes ADP's tools precisely enough to rebuild them, with tests to prove the
rebuild matches.

Install:

    /plugin install adp-minimal --marketplace fblgit/fblgit-claude-marketplace

Then ask Claude how any part of ADP works. Each topic is its own skill, so only the one the question needs loads:

| Skill | Explains |
|---|---|
| `adp-minimal` | what ADP is, its pieces, the rule (never by hand), and which skill covers what |
| `adp-minimal-parts` | part markers, ids, hashes, diffs, anchors |
| `adp-minimal-snippets` | the hash and diff arithmetic as runnable Python |
| `adp-minimal-protocol` | read, hold, edit, check, publish, record; the record's documents |
| `adp-minimal-payloads` | those documents and calls as JSON |
| `adp-minimal-new-artifact` | how a new artifact is created, its file tree and tiers |
| `adp-minimal-runtime` | the shell, `adp.js`, seeding, switches |
| `adp-minimal-hosts` | host adapters and the common ground components reuse |
| `adp-minimal-roads` | the four roads: new, catalog, edit, adopt |
| `adp-minimal-delta` | base, live, incoming; classification; proposals and the inbox |
| `adp-minimal-packing` | one-file pages, seed and catalog packs, record bundles |
| `adp-minimal-kit` | components, layouts, patterns, viz, samples, and how they wire |
| `adp-minimal-themes` | tokens, theme files, wiring and switching a theme |
| `adp-minimal-catalog` | catalog.json, headers, consistency checks, taking entries |
| `adp-minimal-kit-authoring` | building a general entry with several samples |
| `adp-minimal-rebuild` | rebuilding `adp.py`, `adp.js` and the catalog tool from the contracts, and the runner that proves the rebuild |

## What this is not

It does not ship ADP's tooling, its catalog or its templates, and it does not build or edit pages by hand: ADP's rule is that a page is made and
changed through ADP, never by hand. The tooling can be rebuilt from `adp-minimal-rebuild`, and is ADP's only once every vector passes; the catalog
and the templates are not specified here. To do the work with the real tools, install the full plugin (one Python 3 command on the standard library; no dependencies, no remote
connections, nothing fetched at run time):

    /plugin marketplace add fblgit/artifacts-done-properly
    /plugin install artifacts-done-properly@fblgit-adp

Source and full catalog: https://github.com/fblgit/artifacts-done-properly

Licence: Apache-2.0.
