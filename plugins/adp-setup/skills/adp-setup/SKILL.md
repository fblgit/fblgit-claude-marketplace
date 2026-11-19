---
name: adp-setup
description: "Guided install of ADP (Artifacts Done Properly), the standard and component catalog for claude.ai Artifacts. Use when the user asks to install, set up or get started with ADP."
license: MIT
---

# ADP setup

This skill holds no ADP code. It explains ADP and walks the user through installing the full plugin, which carries the scripts and the catalog.
The user runs each command themselves; do not run an install on their behalf.

## What ADP is

ADP (Artifacts Done Properly) is a standard and a shared component catalog for claude.ai Artifacts and Sites pages that people and several
agents keep editing. The full plugin gives Claude five skills: `adp` (the base skill, with the `adp.py` command line, templates and the catalog)
and the road skills `adp-new`, `adp-catalog`, `adp-edit` and `adp-adopt`. The full ADP plugin is open source (Apache-2.0); this setup skill is MIT:
https://github.com/fblgit/artifacts-done-properly

## Steps

Ask first whether ADP is already installed (does `/adp` exist?). If it is, stop: nothing to do except `/adp setup` if it was never run.

Check that Python 3 is available (`python3 --version`); ADP uses only the standard library. If it is missing, tell the user to install Python 3 from
python.org or their package manager, and wait.

Then ask the user to run, one at a time, and wait for each to finish:

1. `/plugin marketplace add fblgit/artifacts-done-properly`
2. `/plugin install artifacts-done-properly@fblgit-adp`
3. `/adp setup`

`/adp setup` asks for a scope (`user`, `project` or `local`), writes `~/.adp/config.json` and puts the shipped catalog in `~/.adp/catalog`.

When it finishes, confirm with the user that `/adp` answers, and point them to the README for the eight journeys:
https://github.com/fblgit/artifacts-done-properly#readme

For the Claude desktop app, `adp.skill` from the latest release is the install:
https://github.com/fblgit/artifacts-done-properly/releases/latest
