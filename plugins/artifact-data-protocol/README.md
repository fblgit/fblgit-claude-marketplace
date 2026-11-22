# Artifact Data Protocol

Build claude.ai Artifacts that are meant to last. ADP (Artifacts Done Properly, and the Artifact Data Protocol behind it) gives a page a
shared component catalog, sections that can be edited one at a time, and a record of every change. This plugin teaches Claude how ADP works
and carries the source of its tools.

## The problem it solves

An Artifact is easy to make and hard to keep. Three things go wrong once a page is shared or edited again:

| What goes wrong | What ADP does about it |
|---|---|
| Every page rebuilds its own cards, tables and charts | Reusable pieces live in a **catalog**. A page takes them by reference, with their version. |
| A second session publishes from a stale copy and wipes newer work | Every section is a **part** with a stable id and a hash. A session **holds** the parts it edits, and every write is pinned to the version it read. |
| Nobody can say what changed, or why | The page keeps its own **record**: each publish, each decision, each request from a viewer. |

## What you get

- **15 skills**, one per topic, so Claude loads only what a question needs.
- **Three tools, as source in the skills**: `adp.py` (the command line), `adp_catalog.py` (the catalog checker) and `adp.js` (the script every
  page loads). Each skill holds the code for its topic next to the text that explains it.
- **147 test vectors** with their fixtures. They run every command and check its exact output.
- **A minimal page template** to start from.

The tools work offline. `adp.py` computes hashes and diffs, lays out a page and prints the exact `Artifact` and `ArtifactData` calls; Claude
makes those calls. Nothing is sent anywhere unless you ask Claude to publish.

## Install

    /plugin marketplace add fblgit/fblgit-claude-marketplace
    /plugin install artifact-data-protocol@fblgit-claude-marketplace

Requirements: Python 3 for the tools, and Node.js and git to run the full test suite. No third-party packages.

## First use

Ask Claude for what you want, in your own words:

- "Make me a project tracker as an artifact that my team can comment on."
- "Add a progress chart to this page from the catalog."
- "Someone left a request on the page. Do it and record the change."
- "What changed on this artifact since last week?"

The first time, Claude offers to assemble the tools from the skills and tells you how many vectors pass. After that it follows one of four
**roads**: a new page, a catalog entry, an edit, or adopting a page you already have.

## How a page is built

    catalog (kits, themes, templates)
           |  taken by reference
           v
    page = shell + parts (stable ids, hashes) + adp.js
           |  read -> hold -> edit -> check -> publish -> record
           v
    record (manifest, parts, changes, requests, decisions)

A viewer files a request from the page. A Claude Code session claims it, does the work and reports back on the page. Two sessions editing
the same page each hold their own parts; where both changed the same part, ADP stops and shows both versions instead of picking one.

## Skills

| Skill | Covers |
|---|---|
| `adp` | what ADP is, and which skill covers what |
| `adp-roads` | step-by-step workflows: new page, catalog entry, edit, adopting an existing page |
| `adp-new-artifact` | creating a page: its files and templates |
| `adp-parts` | part markers, ids, hashes, diffs, comment anchors |
| `adp-protocol` | how an edit is made: read, hold, edit, check, publish, record |
| `adp-payloads` | the records and tool calls as JSON |
| `adp-delta` | merging concurrent edits, proposals, the inbox |
| `adp-runtime` | `adp.js`, the script every page loads |
| `adp-hosts` | running ADP pages on hosts other than Claude |
| `adp-packing` | one-file pages, seed packs, moving records between hosts |
| `adp-catalog` | the component catalog and how to validate it |
| `adp-kit` | components, layouts, patterns, charts and how a page uses them |
| `adp-kit-authoring` | writing a reusable component instead of a one-off |
| `adp-themes` | design tokens (color, type, shape, density, arrangement), dark mode, switching themes |
| `adp-rebuild` | assembling the three tools from the skills and running the vectors |

## Build and check the tools yourself

`adp-rebuild` holds an assembler and a test runner. Save its three snippets as `build.py`, then:

    python3 build.py SKILLS_DIR BUILD_DIR

It writes `adp.py`, `adp_catalog.py`, `adp.js` and the templates into `BUILD_DIR`, runs every vector against them and ends with a line such
as `147 of 147 vectors pass, 0 skipped`. A changed fragment fails its checksum, and a vector that no fragment names fails the build.

## Related plugins

- **artifacts-done-properly**: the full ADP distribution, with its catalog of ready components and themes.
- **adp-setup**: a guided install of the full distribution.

## Privacy and license

The plugin collects nothing; see [PRIVACY.md](PRIVACY.md). Apache-2.0, see [LICENSE](LICENSE).
