> Copy of [`plugins/artifacts-done-properly/skills/adp/refs/sites.md`](https://github.com/fblgit/artifacts-done-properly/blob/main/plugins/artifacts-done-properly/skills/adp/refs/sites.md) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.
> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository
> (https://github.com/fblgit/artifacts-done-properly); `snippets.md` shows how to do the same by hand. Calls to Claude's own tools (`Artifact`, `ArtifactData`) are examples
> of what a Claude host offers: on another host, use that host's way to read and write the page.

# ADP on Sites (Claude and Codex)

Use the same ADP parts, catalog and export/hold/propose/publish/record/ack protocol
on either host. The agent's name does not choose the host. For Sites, load the
available Sites skill and use its source helper and native publication tools;
Artifact/ArtifactData calls in the roads describe the Claude host only.

## Source and assets

Keep the Site checkout in the project, for example `.adp/knowledgebase/`, unless
the user chose another path. Read `.openai/hosting.json` and the checkout's Git
remote before writing or pushing. The Site source repository and the ADP GitHub
project repository are separate: push reusable tooling to the project repository;
publish page source through Sites. A Site commit does not push a GitHub change.

Confirm the exact Site ID, URL and connection match the source checkout. Use the
authenticated Sites connection for private catalog reads; a public-looking URL
does not establish access. Follow `adp-catalog` to fetch, verify and materialize
catalog references. The builder requires local bytes for every selected file.

Prepare an asset directory containing `index.html` and its served files, separate
from the Site project output. After normal ADP checks and explicit seed preparation:

```sh
python3 -I <adp skill folder>/scripts/adp.py files ASSETS --host sites --out SITE_PROJECT
```

This writes only `SITE_PROJECT/dist/server/index.js`: selected assets (including
binary files) plus the canonical Sites API handler. GET/HEAD serve assets; API
requests retain the handler's authentication and revision checks. Hidden paths
are excluded; symlink assets, unresolved catalog references, output inside ASSETS
and delta/batch flags are refused. Existing hosting identity and migrations stay
in place. The result names the required `DB` binding and canonical SQL schema;
provision/apply migrations using the Sites workflow. Building does not deploy,
seed records or reconcile content. Keep page-specific compilation in the page.

## Publication and records

1. Read the latest deployed source and native records before editing. Feed verified
   source files/listing and normalized records to `ADP export`. Preserve raw reads;
   normalize native record `revision` to the shell's `version` for pins only.
2. Hold affected parts with guarded native writes; read back and ack. Edit, check,
   and propose with the existing commands. `export`/`propose` reconcile content;
   do not substitute custom copy reconciliation or a saved stale baseline.
3. Prepare seeds explicitly when needed, build the full asset snapshot, then use
   Sites packaging/deployment. Guard source publication with the current source
   revision. A record revision cannot guard a source deployment.
4. Verify deployed bytes. Record with the successful deployment ID as publication
   version, native record revisions as pins, and the source commit in the summary.
   Apply guarded native record writes with `manifest/current` last; read back each
   result before ack. Re-export and ack the applied proposal before another edit.

The shared shell uses `adp_sites_adapter.py` for native read/write plans and
receipt verification. Source publication and record writes are
sequential operations, not one transaction. If either outcome is unknown, inspect
the deployment or read back the records before retrying. Report partial success.
Building alone is never evidence that a page is published or its records persisted.
