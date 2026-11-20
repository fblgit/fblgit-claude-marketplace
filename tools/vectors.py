#!/usr/bin/env python3
"""Run or refresh the vectors of plugins/adp-minimal against the real ADP tools.

The runner is the one in plugins/adp-minimal/skills/adp-minimal-rebuild/SKILL.md (snippet: vector-runner), executed as written there, so the code a
reader rebuilds against is the code that checks the vectors here.

  python3 tools/vectors.py [--adp PATH] [--only NAME ...]            run every vector; exit 1 when one fails
  python3 tools/vectors.py [--adp PATH] --update [--only NAME ...]   write what the real tools return into the vectors' expected fields

--update only fills fields a vector already names (exit, stdout, stdout_text, stderr_text, files_out); a vector's inputs are never changed. The ADP checkout is
--adp PATH, else $ADP_REPO, else the folder artifacts-done-properly beside this repository.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'plugins', 'adp-minimal', 'skills')
RUNNER = os.path.join(SKILLS, 'adp-minimal-rebuild', 'SKILL.md')


def load_runner():
    with open(RUNNER, encoding='utf-8') as f: text = f.read()
    code = [b for b in re.findall(r'```python\n(.*?)\n```\n', text, re.S) if b.startswith('# snippet: vector-runner')]
    if len(code) != 1: sys.exit(f'{RUNNER}: expected one vector-runner snippet, found {len(code)}')
    ns = {}
    exec(compile(code[0], RUNNER, 'exec'), ns)
    return ns


def tools_of(adp):
    s = os.path.join(adp, 'plugins', 'artifacts-done-properly', 'skills', 'adp')
    t = {'adp.py': os.path.join(s, 'scripts', 'adp.py'), 'adp_catalog.py': os.path.join(s, 'scripts', 'adp_catalog.py'),
         'adp.js': os.path.join(s, 'assets', 'adp.js')}
    for k, p in t.items():
        if not os.path.isfile(p): sys.exit(f'{k} not found at {p}')
    return t


def dump(vec):
    return json.dumps(vec, indent=1, ensure_ascii=False) + '\n'


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--adp', default=os.environ.get('ADP_REPO') or os.path.join(os.path.dirname(ROOT), 'artifacts-done-properly'))
    ap.add_argument('--update', action='store_true')
    ap.add_argument('--only', nargs='*')
    a = ap.parse_args(argv)
    ns, tools = load_runner(), tools_of(a.adp)
    results = {r['vector']: r for r in ns['run'](SKILLS, tools, a.only)}
    if not a.update:
        for r in results.values():
            print(('ok   ' if r['ok'] else 'FAIL ') + r['vector'])
            for p in r['problems']: print('     ' + p)
        print(f"{sum(r['ok'] for r in results.values())} of {len(results)} vectors pass")
        return 0 if all(r['ok'] for r in results.values()) else 1
    _, vectors = ns['blocks'](SKILLS)
    edits = {}
    for path, span, vec in vectors:
        r = results.get(vec['vector'])
        if not r or r['ok']: continue
        steps = vec.get('steps', [vec])
        for step, got in zip(steps, r['observed']):
            for k in ('exit', 'stdout', 'stdout_text', 'stderr_text', 'files_out'):
                if k in step: step[k] = got.get(k)
        edits.setdefault(path, []).append((span, dump(vec)))
    for path, spans in edits.items():
        with open(path, encoding='utf-8') as f: text = f.read()
        for (s, e), new in sorted(spans, reverse=True): text = text[:s] + new + text[e:]
        with open(path, 'w', encoding='utf-8') as f: f.write(text)
        print(f'updated {len(spans)} vector(s) in {os.path.relpath(path, ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
