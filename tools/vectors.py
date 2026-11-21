#!/usr/bin/env python3
"""Assemble the tools of plugins/adp-minimal from its fragments, then run or re-record its vectors against that build.

The assembler and the runner are the snippets in plugins/adp-minimal/skills/adp-minimal-rebuild/SKILL.md (assemble, vector-runner), executed as
written there.

  python3 tools/vectors.py [--final] [--only NAME ...]      assemble, then run the vectors; prints problems, failures and the totals
  python3 tools/vectors.py --update --only NAME ...         write what the build returns into the expected fields of the named vectors
  python3 tools/vectors.py --seal SKILL ...                 rewrite the sha lines of those skills' fragments, assemble, and stop

--final adds the coverage check (every vector without `skip` is named by a fragment). --update only fills fields a vector already names
(exit, stdout, stdout_text, stderr_text, files_out); inputs are never changed, and a skipped vector is left as it is. Exit 1 on any problem
or failing vector.
"""
import argparse, json, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'plugins', 'adp-minimal', 'skills')
REBUILD = os.path.join(SKILLS, 'adp-minimal-rebuild', 'SKILL.md')


def load():
    """The vector-runner and assemble snippets of the rebuild skill, executed into one namespace."""
    with open(REBUILD, encoding='utf-8') as f: text = f.read()
    ns = {}
    for name in ('vector-runner', 'assemble'):
        code = re.findall(r'```python\n(# snippet: ' + name + r'\b.*?)\n```\n', text, re.S)
        if len(code) != 1: sys.exit(f'{REBUILD}: expected one {name} snippet, found {len(code)}')
        exec(compile(code[0], f'{REBUILD}:{name}', 'exec'), ns)
    return ns


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--update', action='store_true')
    ap.add_argument('--final', action='store_true')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--seal', nargs='*')
    a = ap.parse_args(argv)
    ns = load()
    with tempfile.TemporaryDirectory(prefix='adp-build-') as build:
        report, problems = ns['assemble'](SKILLS, build, a.final, a.seal or ())
        for tool, r in report.items(): print(f"{tool}: {r['lines']} lines, {r['fragments']} fragments, {r['sha256']}")
        print(*problems, sep='\n', end='\n' if problems else '')
        if a.seal is not None: return 1 if problems else 0
        results = {r['vector']: r for r in ns['run'](SKILLS, {t: os.path.join(build, p) for t, p in ns['TOOLS'].items()}, a.only)}
    ran = [r for r in results.values() if not r.get('skip')]
    if not a.update:
        for r in ran:
            if not r['ok']: print('FAIL ' + r['vector'], *r['problems'], sep='\n     ')
        print(f"{sum(r['ok'] for r in ran)} of {len(ran)} vectors pass, {len(results) - len(ran)} skipped")
        return 0 if not problems and all(r['ok'] for r in ran) else 1
    if not a.only: sys.exit('--update needs --only NAME ...: name the vectors to re-record')
    _, vectors = ns['blocks'](SKILLS)
    edits = {}
    for path, span, vec in vectors:
        r = results.get(vec['vector'])
        if not r or r['ok'] is not False: continue
        for step, got in zip(vec.get('steps', [vec]), r['observed']):
            for k in ('exit', 'stdout', 'stdout_text', 'stderr_text', 'files_out'):
                if k in step: step[k] = got.get(k)
        edits.setdefault(path, []).append((span, json.dumps(vec, indent=1, ensure_ascii=False) + '\n'))
    for path, spans in edits.items():
        with open(path, encoding='utf-8') as f: text = f.read()
        for (s, e), new in sorted(spans, reverse=True): text = text[:s] + new + text[e:]
        with open(path, 'w', encoding='utf-8') as f: f.write(text)
        print(f'updated {len(spans)} vector(s) in {os.path.relpath(path, ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
