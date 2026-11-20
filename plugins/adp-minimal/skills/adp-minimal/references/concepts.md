# ADP concepts

ADP makes a shared Artifact safe to edit by several people and agents. It is a set of conventions, not a service.

## Parts and hashes

Every piece of the page is a *part* with a stable id. A part is the text between two comment markers, in the comment syntax of the spot:

    <!-- part:triage.keys-table -->  ...  <!-- /part:triage.keys-table -->
    /* part:page.style */           ...  /* /part:page.style */

An id is dot-separated segments, each `[a-z0-9][a-z0-9-]*`. Parts may nest. A part's *hash* is the first 12 hex characters of the SHA-256 of its
text with every whitespace run collapsed to one space (and trimmed); a parent's text includes its children, so a change shows on every ancestor.
Text outside every top-level part is hashed as the pseudo-part `_rest`. The *page hash* is the hash of the sorted `id=hash` lines plus
`file:<path>=<hash>` lines. Details: [architecture](architecture.md) section 3; code: [snippets](snippets.md).

## The protocol

Read the latest version, hold the parts you will touch, edit, check, publish to the same URL with a label, then record the change in the
database. The only lock is the `if_version` pin on a write: a refused write means someone wrote first. Full text: [protocol](protocol.md);
the documents and calls: [payloads](payloads.md).

## The vocabulary

- **Shell**: the thin `index.html` of an adp/2 artifact: a header with the What changed panel, tabs, an empty `<main id="views">` and the `<script>`
  tags. The page's content lives in files per part (`content.js`, `parts/*.js`, `styles/*.css`), not in the shell. See
  [architecture](architecture.md) section 2.
- **Runtime**: `adp.js`, one script loaded before the page's own, that renders What changed, anchors comments to part ids, checks page integrity
  against `manifest/current` and seeds the database on first open. [architecture](architecture.md) section 5.
- **Shim**: a small script that stands in for something the page expects. Two exist. The one-file shim (`assets/hosts/single/shim.js`)
  serves a page's relative `<script src>`, `<link>` and `fetch()` from files embedded in one `index.html`, each with its sha256, for tools
  that publish a single file. The dev shim stands in for the claude.ai viewer (`window.claude`: db, user, comments, publish) so a page runs
  offline. [architecture](architecture.md) section 2 and [host adapters](host-adapters.md).
- **Tokens**: the CSS custom properties a theme sets and every catalog file draws with: `--bg --panel --sunk --ink --ink-2 --ink-3 --rule --rule-2
  --accent --accent-ink`, the meanings (`--ok --warn --danger`) and the font tokens `--f-display --f-ui --f-mono --f-hand`. A theme sets the same
  names, so a viewer can switch themes at run time. [themes](themes.md).
- **Canonical forms**: what the tools compute identically so two parties agree: the part and page hash (the normalization above), and the set
  of database collections an export covers (`manifest`, `parts`, `content`, `changes`, `config`, `requests`, `presence`, `agents`,
  `decisions`, `incoming`). [architecture](architecture.md) sections 3 and 4.
- **Host adapter**: the boundary between a page and the system it runs in (the claude.ai viewer, Sites, a local emulator): the page calls the
  same names whatever the host. [host adapters](host-adapters.md), [Claude adapter](claude-host-adapter.md).
- **Kit and catalog**: shared, versioned building blocks with a header (id, kind, tokens it needs, files it provides) in a catalog of
  files. [catalog structure](catalog-structure.md), [catalog header](catalog-header.md).
- **Framework**: ADP is a convention plus a runtime, not a UI framework. A page is plain HTML, CSS and JavaScript; ADP adds the parts, the
  record and the integrity check around it.

## Conventions

- Keep every marker and every `data-part="<id>"`; add both for a new part; never reuse a retired id.
- A new owner decision is written under `decisions/` first, quoted verbatim.
- One publish, one `changes/` entry; at most 50 writes per ArtifactData batch, `manifest/current` last.
- A page renders fully when the database is unavailable (`use("db")` resolves `null`).
- Say what a command or a read did not confirm.
