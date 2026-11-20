# ADP Minimal

Skills that explain [ADP (Artifacts Done Properly)](https://github.com/fblgit/artifacts-done-properly) to Claude.

ADP is a standard for claude.ai Artifacts that more than one person or agent edits over time. Each part of a page gets an id and a content hash,
each change is recorded, and a write made against an old version is refused.

This plugin is the documentation only. It has no tools, no component catalog and no page templates; those come with the full plugin,
`artifacts-done-properly`. Use this one when you want Claude to explain ADP or plan work in it, or to rebuild ADP's tools from a written spec.

## Install

    /plugin marketplace add fblgit/fblgit-claude-marketplace
    /plugin install adp-minimal@fblgit-claude-marketplace

For the full plugin instead:

    /plugin install artifacts-done-properly@fblgit-claude-marketplace

## Skills

Each topic is its own skill, so Claude loads only the one a question needs.

| Skill | Covers |
|---|---|
| `adp-minimal` | what ADP is, and which skill covers what |
| `adp-minimal-parts` | part markers, ids, hashes, diffs, comment anchors |
| `adp-minimal-snippets` | the hash and diff rules as runnable Python |
| `adp-minimal-protocol` | how an edit is made: read, hold, edit, check, publish, record |
| `adp-minimal-payloads` | the records and tool calls as JSON |
| `adp-minimal-new-artifact` | creating a page: its files and templates |
| `adp-minimal-runtime` | `adp.js`, the script every page loads |
| `adp-minimal-hosts` | running ADP pages on hosts other than Claude |
| `adp-minimal-roads` | the procedure for each kind of job: new page, catalog, edit, adopt |
| `adp-minimal-delta` | merging concurrent edits, proposals, the inbox |
| `adp-minimal-packing` | one-file pages, seed packs, moving records between hosts |
| `adp-minimal-kit` | components, layouts, patterns, charts and how a page uses them |
| `adp-minimal-themes` | colour and font tokens, dark mode, switching themes |
| `adp-minimal-catalog` | the component catalog and how to check it |
| `adp-minimal-kit-authoring` | writing a reusable component instead of a one-off |
| `adp-minimal-rebuild` | rebuilding `adp.py`, `adp.js` and the catalog tool, and testing the rebuild |

## Rebuilding the tools

Each command is specified in the skill that explains it, with test cases (`vectors.md`) whose expected output comes from running the real tools.
`adp-minimal-rebuild` has the build order and a runner that checks a rebuilt tool against all of them. In this repository, `tools/vectors.py` and
`tests/test_minimal.py` run the same test cases against an ADP checkout.

Licence: Apache-2.0.
