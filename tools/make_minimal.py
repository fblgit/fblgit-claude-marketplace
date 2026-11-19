#!/usr/bin/env python3
"""Refresh the copied pages of plugins/adp-minimal/, the Markdown-only ADP plugin of this marketplace.

The plugin carries no program: the pages written by hand stay as they are, and the pages below are copies of the ADP repository's own
documentation (the protocol guide, the architecture, the road skills ...) with a banner on top and their relative links turned into links to
that repository (or to the sibling copy). `--check` fails when a copy is not what this script would write, or when the plugin's version is not
ADP's version.

The sources are read from a checkout of https://github.com/fblgit/artifacts-done-properly: `--adp PATH`, else $ADP_REPO, else the folder
`artifacts-done-properly` beside this repository.

  python3 tools/make_minimal.py [--adp PATH]            write the copies
  python3 tools/make_minimal.py [--adp PATH] --check    verify them
"""
import json, os, posixpath, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # this repository: where the plugin is
ADP = os.environ.get('ADP_REPO') or os.path.join(os.path.dirname(ROOT), 'artifacts-done-properly')      # the ADP checkout: where the sources are
FULL = 'plugins/artifacts-done-properly'
MIN = 'plugins/adp-minimal'
REFS = f'{MIN}/skills/adp-minimal/references'
REPO = 'https://github.com/fblgit/artifacts-done-properly'
BLOB = f'{REPO}/blob/main/'

# source in the repository -> (page in references/, what it is)
COPIES = {
    f'{FULL}/skills/adp/catalog/kit/guides/artifact-dataplane.md': ('protocol.md', 'The protocol: parts, hashes, the ArtifactData layout, what every agent does'),
    'docs/architecture.md': ('architecture.md', 'The architecture: layout, parts and hashes, manifest and database, runtime, catalog'),
    'docs/catalog-header.md': ('catalog-header.md', 'The header every catalog entry carries'),
    'docs/themes.md': ('themes.md', 'Themes and tokens'),
    'docs/config.md': ('config.md', 'The switches of an ADP page'),
    'docs/host-adapters.md': ('host-adapters.md', 'Host adapters: the boundary between a page and its host'),
    'docs/claude-host-adapter.md': ('claude-host-adapter.md', 'The Claude host adapter'),
    f'{FULL}/skills/adp-new/SKILL.md': ('road-new.md', 'The road for a new artifact'),
    f'{FULL}/skills/adp-catalog/SKILL.md': ('road-catalog.md', 'The road for the catalog'),
    f'{FULL}/skills/adp-edit/SKILL.md': ('road-edit.md', 'The road for editing an artifact others also work on'),
    f'{FULL}/skills/adp-adopt/SKILL.md': ('road-adopt.md', 'The road for adopting an existing artifact'),
}
LINK = re.compile(r'(\]\()([^)\s]+)(\))')


def read(rel, base=None):
    with open(os.path.join(base or ADP, rel), encoding='utf-8') as f: return f.read()


def relink(text, src):
    """Relative links in a copied page: to the sibling copy when the target is copied too, else to the file in the repository."""
    sibling = {s: d for s, (d, _) in COPIES.items()}

    def fix(m):
        href = m.group(2)
        if re.match(r'(?:[a-z][a-z0-9+.-]*:|#)', href): return m.group(0)
        path, _, frag = href.partition('#')
        target = posixpath.normpath(posixpath.join(posixpath.dirname(src), path))
        if target in sibling: new = sibling[target]
        else: new = BLOB + target
        return f'{m.group(1)}{new}{"#" + frag if frag else ""}{m.group(3)}'
    return LINK.sub(fix, text)


def page(src, title):
    text = read(src)
    if text.startswith('---\n'): text = text.split('\n---\n', 1)[1].lstrip('\n')      # a road skill: its frontmatter is not part of the page
    banner = (f'> Copy of [`{src}`]({BLOB}{src}) in the ADP repository, written by `tools/make_minimal.py` of the marketplace: edit the source, not this page.\n'
              f'> This plugin ships documentation only. A command named here (`adp.py ...`) belongs to the full ADP install in the repository\n'
              f'> ({REPO}); `snippets.md` shows how to do the same by hand.\n\n')
    return banner + relink(text, src)


def expected():
    return {f'{REFS}/{dst}': page(src, title) for src, (dst, title) in COPIES.items()}


def main(argv):
    global ADP
    if '--adp' in argv: ADP = os.path.abspath(argv[argv.index('--adp') + 1])
    if not os.path.isdir(os.path.join(ADP, FULL)): sys.exit(f'no ADP checkout at {ADP}: pass --adp PATH or set ADP_REPO')
    want, bad = expected(), []
    for rel, text in want.items():
        path = os.path.join(ROOT, rel)
        have = read(rel, ROOT) if os.path.isfile(path) else None
        if have != text:
            bad.append(rel)
            if '--check' not in argv:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f: f.write(text)
    full = json.loads(read(f'{FULL}/.claude-plugin/plugin.json'))['version']
    mine = json.loads(read(f'{MIN}/.claude-plugin/plugin.json', ROOT))['version']
    if full != mine: bad.append(f'{MIN}/.claude-plugin/plugin.json: version {mine} is not ADP\'s {full}')
    if '--check' in argv:
        if bad: sys.exit('make_minimal --check failed:\n  ' + '\n  '.join(bad) + '\nrun: python3 tools/make_minimal.py')
        print('ok'); return 0
    print(f'{len([b for b in bad if b in want])} pages written' if bad else 'up to date'); return 0


if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
