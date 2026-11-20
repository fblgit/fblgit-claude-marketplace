# ADP Minimal

Reference skills for [ADP (Artifacts Done Properly)](https://github.com/fblgit/artifacts-done-properly).

ADP is a framework and shared library for reusable claude.ai Artifacts. Reusable pieces of a page go into a catalog as kits, each with its
interface, its dependencies and examples, and the next page takes them by reference instead of rewriting them. Pages are built from templates
and carry their own record of changes and requests: a viewer files a request from the page, a Claude Code session claims it (`adp.py work`),
does the work and reports back on the page.
Every section of a page is a *part* with a stable id; comments and diffs are anchored to that id.

This plugin contains those reference skills and a specification of ADP's tools, with test vectors sufficient to reimplement them. It contains no
executable code, catalog or templates; those come with the full plugin, `artifacts-done-properly`. Install this one for the documentation alone, or to
port the tools to another runtime.

## Install

    /plugin marketplace add fblgit/fblgit-claude-marketplace
    /plugin install adp-minimal@fblgit-claude-marketplace

For the full plugin instead, from ADP's own marketplace:

    /plugin marketplace add fblgit/artifacts-done-properly
    /plugin install artifacts-done-properly@fblgit-adp

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
| `adp-minimal-roads` | step-by-step workflows: new page, catalog entry, edit, adopting an existing page |
| `adp-minimal-delta` | merging concurrent edits, proposals, the inbox |
| `adp-minimal-packing` | one-file pages, seed packs, moving records between hosts |
| `adp-minimal-kit` | components, layouts, patterns, charts and how a page uses them |
| `adp-minimal-themes` | color and font tokens, dark mode, switching themes |
| `adp-minimal-catalog` | the component catalog and how to validate it |
| `adp-minimal-kit-authoring` | writing a reusable component instead of a one-off |
| `adp-minimal-rebuild` | rebuilding `adp.py`, `adp.js` and the catalog tool, and testing the rebuild |

## Rebuilding the tools

Each command is specified in the skill that explains it, with test vectors (`vectors.md`) generated from the reference implementation.
`adp-minimal-rebuild` has the build order and a runner that checks a reimplementation against all of them. The marketplace repository's
`tools/vectors.py` and `tests/test_minimal.py` run these vectors against a local clone of `fblgit/artifacts-done-properly`.

## License

Apache-2.0.
