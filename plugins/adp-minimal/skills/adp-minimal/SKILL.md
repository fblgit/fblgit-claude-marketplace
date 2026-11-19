---
name: adp-minimal
description: "Reference for ADP (Artifacts Done Properly), the standard for shared Claude Artifacts and Sites pages: parts with stable ids and content hashes, the read, hold, publish, record protocol, the catalog structure, shell, shim, tokens and conventions, payload examples and code snippets. Use when the user asks what ADP is, wants a page built or edited the ADP way without the ADP tools, or asks about parts, part ids, page hashes, manifest/current, if_version, holds, kits or themes."
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# ADP minimal

This skill is documentation only; it has no scripts. It lets Claude explain ADP and follow it by hand. The full tools (`adp.py`, the catalog,
templates, the page runtime) are in https://github.com/fblgit/artifacts-done-properly; when the user wants them, say so and point there.

## How to use it

1. For the idea and the vocabulary, read [concepts](references/concepts.md).
2. To work on an artifact, follow the protocol in [protocol](references/protocol.md): read, hold, edit, check, publish, record. The exact
   calls and documents are in [payloads](references/payloads.md); the hash arithmetic you would normally run through `adp.py` is in
   [snippets](references/snippets.md) as short code you can run or adapt.
3. For a new page, read [road-new](references/road-new.md); for an edit, [road-edit](references/road-edit.md); to bring an existing page onto
   ADP, [road-adopt](references/road-adopt.md); for the catalog, [catalog structure](references/catalog-structure.md) and
   [road-catalog](references/road-catalog.md). The roads name `adp.py` commands: without the tool, do the step by hand as the snippets show.
4. For how a page looks and switches, read [themes](references/themes.md) and [config](references/config.md); for the boundary with a host,
   [host adapters](references/host-adapters.md) and [the Claude adapter](references/claude-host-adapter.md).
5. For worked examples, see a [kit entry](references/examples/kit-entry.md) and a [theme](references/examples/theme.md).

## Always

- Read the latest version of an artifact before touching it; a local copy from an earlier session may predate other people's work.
- Say what you did not verify. Without `adp.py`, nothing has checked your hashes: say so, and give the user what to check.
- Never invent a command. If a page says to run `adp.py`, and it is not installed, the command is not available here.
