# ADP minimal

ADP (Artifacts Done Properly) as documentation. This is the **minimal ADP configuration**: enough to understand ADP and to do real work with it
by hand, with nothing to install or run. Every file is Markdown.

It holds the protocol, the catalog structure, the shell, the shim, the tokens, the conventions, payload examples, the host adapter, the
architecture, the four roads (new, catalog, edit, adopt), kit examples and code snippets you can adapt.

Install:

    /plugin install adp-minimal --marketplace fblgit/fblgit-claude-marketplace

Then ask Claude about ADP, or to build or edit an Artifact "the ADP way"; the `adp-minimal` skill loads on its own.

## What this is not

It has no `adp.py`, no catalog files and no templates. Without them the hashes, diffs and the ArtifactData batches are worked out by hand
(`snippets.md` has short, readable snippets for that), and the shared catalog is not available to copy from.

## The full installation

The complete ADP tools are in the project repository: https://github.com/fblgit/artifacts-done-properly. They are one Python 3 command line on the
standard library: no dependencies, no remote connections, nothing fetched at run time. The repository also holds the full catalog (the
kit examples in this plugin are a few of its entries), the templates and the page runtime.

    /plugin marketplace add fblgit/artifacts-done-properly
    /plugin install artifacts-done-properly@fblgit-adp

Licence: Apache-2.0.
