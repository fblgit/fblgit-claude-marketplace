# Privacy

Artifact Data Protocol is a set of skills: text and code that Claude reads on your machine. It has no server, no account and no analytics, and its
author receives nothing from your use of it.

## What the plugin does with data

- **It collects nothing.** No skill, script or page in this plugin sends data to the author or to any third party.
- **The command-line tools work offline.** `adp.py` and `adp_catalog.py`, once assembled from the skills, read and write files in the folders
  you give them and print the calls for Claude to make. They open no network connection. `adp.py` runs `git` locally, in a folder beside
  the page, to keep the history of an edit.
- **Local files.** The tools keep their own settings and your copy of the catalog in `~/.adp` (or the folder named by `ADP_HOME`). The only
  other environment variable they read is `ADP_PACK`, a size in bytes.
- **The page runtime.** `adp.js` runs inside a page you publish. It loads the files published with that page and reads and writes that page's
  own records through the host the page runs on. It contacts no other service.

## What goes to claude.ai

When you ask Claude to publish or update a page, Claude sends the page's files and records to claude.ai with its own tools, under your
account. That data is then held by Anthropic under the terms and privacy policy you accepted for Claude; this plugin adds nothing to it and
receives none of it. A published page is private to you until you share it.

## Contact

Questions and reports: <https://github.com/fblgit/fblgit-claude-marketplace/issues>.
