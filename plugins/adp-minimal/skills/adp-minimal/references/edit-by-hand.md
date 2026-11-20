# Editing a page by hand, without `adp.py`

[road-edit](road-edit.md) is written for the full ADP install: each step names an `adp.py` command. This plugin has none. This page says, step by step,
what you can do instead, and which steps have no stand-in. A snippet here is a suggestion to run or adapt, not a tool that is installed.

| Road step | By hand | Where |
|---|---|---|
| Export (read) | Read the page (the latest version is the only source), then read `manifest/current`, `parts/*` and `agents/` from the artifact's database. Keep the version each doc returned. | [payloads](payloads.md) 1 |
| Classify (new, ours, theirs, held, retired) | Compare, part by part, the hash you recorded when you last read with the hash in the live `manifest/current`. A part that changed upstream and that you also changed is held: stop and ask. | [snippets](snippets.md) "compare with the recorded manifest" |
| Hold | One pinned batch that sets `hold_until` (at most 2 hours ahead) on the parts you will touch, with `if_version` on every doc. A refused write means someone wrote first: read again. | [payloads](payloads.md) 2, "a pinned write" |
| Edit | Change the files. Keep every marker and `data-part`; add both for a new part; never reuse a retired id. | [protocol](protocol.md) |
| Check | Recompute the part hashes and the page hash and compare with what you mean to record. Nothing else checks your work: say so. | [snippets](snippets.md) "part hashes", "page hash" |
| Publish | Publish to the same URL with only the changed files and a label of at most 60 characters. On a conflict, merge onto the newer version; never force. | [payloads](payloads.md) 3 |
| Record | One pinned batch: the `changes/` entry (its id from "the next changes/ id"), the parts you touched, `manifest/current` last. At most 50 writes. | [payloads](payloads.md) 4, [snippets](snippets.md) |
| Wording-only change | Update `content/<part id>` with `if_version`, then record a change. | [payloads](payloads.md) 6 |

## No stand-in here

`seed`, `propose` and `ack` (the proposal flow), `work` (leases and claims on requests), `bundle`, `import-plan` and `import-ack` (moving a page between
hosts) and `log` do real bookkeeping that this plugin does not reproduce. Do not improvise them. Tell the user the step needs the full install
(https://github.com/fblgit/artifacts-done-properly) and, if the page has no `manifest/current` yet, that it was never seeded.

## Calls to Claude's tools

The `Artifact` and `ArtifactData` calls in these pages show what a Claude host offers. Another host has its own way to read a page, write its
database and publish; the order of the steps and the `if_version` pin stay the same.
