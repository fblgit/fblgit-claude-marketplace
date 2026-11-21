# adp-setup

A guided install for ADP (Artifacts Done Properly). The plugin holds Markdown and JSON only; it explains ADP and has Claude walk you through the
full install, which you run yourself.

Install this guide:

    /plugin marketplace add fblgit/fblgit-claude-marketplace
    /plugin install adp-setup@fblgit-claude-marketplace

Then ask Claude to set up ADP; it will have you run:

    /plugin marketplace add fblgit/artifacts-done-properly
    /plugin install artifacts-done-properly@fblgit-adp
    /adp setup

The full plugin (scripts and catalog) is in https://github.com/fblgit/artifacts-done-properly. The full ADP plugin is Apache-2.0. This setup skill is MIT.
