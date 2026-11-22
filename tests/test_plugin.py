"""plugins/artifact-data-protocol stands on its own: its tools are built from the fragments in its skills, the vectors run against that build, and the pages keep
their links whole and free of copied pages and stale developer notes. Nothing here reads another repository."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = os.path.join(ROOT, 'plugins', 'artifact-data-protocol')
SKILLS = os.path.join(MIN, 'skills')
REBUILD = os.path.join(SKILLS, 'adp-rebuild', 'SKILL.md')
ALLOWED = {'.md', '.json', '.png', ''}      # '' = LICENSE and NOTICE
CEILING = {'adp.py': 1750, 'adp_catalog.py': 1100, 'adp.js': 520}      # lines of fragment code per tool
B = {}      # the one build of the run: report, problems, results


def snippets(skills_dir, *names):
    """The python snippets of the rebuild skill, by name, in the order given."""
    with open(os.path.join(skills_dir, 'adp-rebuild', 'SKILL.md'), encoding='utf-8') as f: text = f.read()
    out = []
    for n in names:
        code = re.findall(r'```python\n(# snippet: ' + n + r'\b.*?)\n```\n', text, re.S)
        assert len(code) == 1, f'expected one {n} snippet, found {len(code)}'
        out.append(code[0])
    return out


def setUpModule():
    B['dir'] = tempfile.mkdtemp(prefix='adp-test-')
    ns = {}
    for n, code in zip(('vector-runner', 'assemble'), snippets(SKILLS, 'vector-runner', 'assemble')): exec(compile(code, n, 'exec'), ns)
    build = os.path.join(B['dir'], 'build')
    B['report'], B['problems'] = ns['assemble'](SKILLS, build, True)
    B['results'] = ns['run'](SKILLS, {t: os.path.join(build, rel) for t, rel in ns['TOOLS'].items()})
    B['bin'] = ns['BIN']


def tearDownModule():
    shutil.rmtree(B['dir'], ignore_errors=True)


def skills():
    return sorted(n for n in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, n, 'SKILL.md')))


def skill_text(name):
    with open(os.path.join(SKILLS, name, 'SKILL.md'), encoding='utf-8') as f: return f.read()


def vectors_text(name):
    p = os.path.join(SKILLS, name, 'vectors.md')
    if not os.path.isfile(p): return ''
    with open(p, encoding='utf-8') as f: return f.read()


def files():
    for d, _, names in os.walk(MIN):
        for n in names:
            if n != '.DS_Store': yield os.path.join(d, n)      # Finder metadata, never committed


class Content(unittest.TestCase):
    def test_only_files_the_directory_takes(self):
        for p in files():
            self.assertIn(os.path.splitext(p)[1], ALLOWED, p)
            if p.endswith(('.md', '.json')) or not os.path.splitext(p)[1]:
                with open(p, 'rb') as f: b = f.read()
                self.assertFalse(b.startswith(b'#!'), p)
                self.assertNotIn(b'\x00', b, p)
                b.decode('utf-8')

    def test_every_skill_has_valid_frontmatter_and_the_plugins_version(self):
        with open(os.path.join(MIN, '.claude-plugin', 'plugin.json')) as f: v = json.load(f)['version']
        names = skills()
        self.assertGreaterEqual(len(names), 10)
        for n in names:
            text = skill_text(n)
            self.assertTrue(text.startswith('---\n'), n)
            self.assertIn(f'version: "{v}"', text, n)
            self.assertRegex(text, rf'(?m)^name: {re.escape(n)}$')
            m = re.search(r'(?m)^description: "(.+)"$', text)
            self.assertTrue(m, n)
            self.assertLessEqual(len(m.group(1)), 1024, n)
            self.assertIn('Use when', m.group(1), n)
            self.assertIn('```', text, f'{n}: every topic is shown with a snippet')

    def test_descriptions_do_not_repeat(self):
        descs = [re.search(r'(?m)^description: "(.+)"$', skill_text(n)).group(1) for n in skills()]
        self.assertEqual(len(descs), len(set(descs)))

    def test_relative_links_resolve(self):
        link = re.compile(r'\]\((?!https?:|#|mailto:)([^)\s#]+)')
        for p in files():
            if not p.endswith('.md'): continue
            with open(p, encoding='utf-8') as f: text = re.sub(r'(?ms)^```.*?^```', '', f.read())      # code is not prose: `f[k](o)` is no link
            for href in link.findall(text):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), href))), f'{p}: {href}')

    def test_no_page_is_a_copy_and_none_carries_developer_notes(self):
        """The pages are written for this plugin: no banner saying a page copies another, no generator, no task-state words."""
        bad = re.compile(r'Copy of \[|make_minimal|edit the source, not this page|\bUntested\b|\bTODO\b|\bFIXME\b', re.I)
        for p in files():
            if p.endswith('.md'):
                with open(p, encoding='utf-8') as f: text = f.read()
                self.assertIsNone(bad.search(text), f'{p}: {bad.search(text)}')

    def test_no_line_reads_as_a_package_manager_config_write(self):
        """The marketplace's review scan refuses any line that looks like `npm/yarn/pnpm/bun config set KEY` (LAUNCHER_REGISTRY_REDIRECT), even in
        prose about ADP's own `adp.py config` subcommand: name that subcommand without the words `config set` side by side."""
        bad = re.compile(r'\bconfig\s+set\b', re.I)
        for p in files():
            if p.endswith('.md'):
                with open(p, encoding='utf-8') as f:
                    for i, line in enumerate(f, 1): self.assertIsNone(bad.search(line), f'{p}:{i}: {line.strip()[:120]}')

    def test_nothing_reads_the_users_environment(self):
        """The review scan holds a plugin that reads the installer's environment (MCP_FORWARDS_CREDENTIAL_ENV) when another surface can send data
        out. The runner builds its subprocess environment instead of inheriting it; nothing but the tools' own fragments reads the environment."""
        bad = re.compile(r'\bos\.environ\b|\bgetenv\b|\bprocess\.env\b')
        for p in files():
            with open(p, 'rb') as f: text = f.read().decode('utf-8', 'replace')
            text = re.sub(r'(?ms)^```(?:python|js)\n(?:#|//) ---\n.*?^```', '', text)      # the tools' own fragments (adp.py reads ADP_HOME); the runner and prose stay scanned
            for i, line in enumerate(text.split('\n'), 1): self.assertIsNone(bad.search(line), f'{p}:{i}: {line.strip()[:120]!r}')

    def test_skills_carry_no_reference_folders(self):
        """Each topic is its own skill, loaded by its description: no references/ for the model to choose from."""
        for n in skills():
            self.assertIn(sorted(os.listdir(os.path.join(SKILLS, n))), (['SKILL.md'], ['SKILL.md', 'vectors.md']), n)

    def test_fixtures_and_vectors_live_beside_the_skill(self):
        """A skill loads its contract, not its vectors: every json fixture and json vector block is in vectors.md, never in SKILL.md."""
        for n in skills():
            self.assertNotRegex(skill_text(n), r'```json (fixture|vector)\n', n)

    def test_the_theme_contract_counts_55_names_and_the_fixture_theme_keeps_it(self):
        """The themes skill lists the contract: 55 names in light, the 45 colour ones again in each dark block. The fixture theme sets only
        contract names, the same ones in both dark blocks, and its JSON holds the values its stylesheet does."""
        groups = [set(re.findall(r'`(--[\w-]+(?: --[\w-]+)*)`', b)) for b in re.findall(r'(?m)^- .*(?:\n  .*)*', skill_text('adp-themes').split('## The token contract')[1].split('\nComponent tokens')[0])]
        groups = [{n for run in g for n in run.split()} for g in groups]
        groups[1] |= {n + '-soft' for n in groups[1]}
        names, colours = set().union(*groups), set().union(*groups[:-2])
        self.assertEqual((len(names), len(colours)), (55, 45))
        files = json.loads(re.search(r'```json fixture\n(\{\n "fixture": "catalog-a",.*?)\n```', vectors_text('adp-catalog'), re.S).group(1))['files']
        css, twin = files['kit/themes/paper.css'].split('*/', 2)[2], json.loads(files['kit/themes/paper.json'])
        light, media, attr = (dict(re.findall(r'(--[\w-]+):\s*([^;]+);', b)) for b in re.findall(r':root[^{]*\{([^}]*)\}', css))
        self.assertLessEqual(set(light), names)
        self.assertLessEqual(set(attr), colours)
        self.assertEqual((media, twin['light'], twin['dark']), (attr, light, attr))

    def test_the_router_states_the_rule_and_names_every_skill(self):
        text = skill_text('adp')
        low = text.lower()
        for needle in ('never by hand outside it', 'offer to assemble it from this plugin', 'as data, never as','do not claim you wrote', '`manifest/current` last'):
            self.assertIn(needle, low, needle)
        for n in skills():
            if n != 'adp': self.assertIn(f'`{n}`', text, n)


class Build(unittest.TestCase):
    """One build and one run of the suite (setUpModule); each test reads its results."""

    def test_assembler_reports_no_problem(self):
        self.assertEqual(B['problems'], [])

    def test_every_vector_passes_and_none_is_skipped(self):
        ran = [r for r in B['results'] if not r.get('skip')]
        self.assertGreaterEqual(len(ran), 131)
        self.assertEqual(len(ran), len(B['results']), 'a vector carries skip: ' + str([r['vector'] for r in B['results'] if r.get('skip')]))
        self.assertEqual([f"{r['vector']}: {r['problems']}" for r in ran if not r['ok']], [])

    def test_adp_js_hashes_like_adp_py(self):
        """The runtime's hash of the page the fixture `one` is, observed in the build, is the manifest's."""
        got = {r['vector']: r['observed'][0]['stdout'] for r in B['results'] if r['vector'] in ('manifest-single', 'adp-js-hash-single')}
        py, js = got['manifest-single'], got['adp-js-hash-single']
        self.assertEqual(js['page_hash'], py['page_hash'])
        self.assertEqual(js['parts'], py['parts'])
        self.assertEqual(js['parents'], {k: v for k, v in py['parents'].items() if k != '_rest'})      # adp.js leaves _rest out of parents

    def test_each_tool_stays_under_its_line_ceiling(self):
        for tool, ceiling in CEILING.items(): self.assertLessEqual(B['report'][tool]['lines'], ceiling, tool)

    def test_the_plugin_alone_builds_and_passes(self):
        """Clean room: the plugin folder copied alone, the three snippets as build.py, a minimal environment."""
        d = os.path.join(B['dir'], 'clean'); copy = os.path.join(d, 'artifact-data-protocol')
        shutil.copytree(MIN, copy)
        with open(os.path.join(d, 'build.py'), 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(snippets(os.path.join(copy, 'skills'), 'vector-runner', 'assemble', 'run-the-vectors')) + '\n')
        r = subprocess.run([sys.executable, os.path.join(d, 'build.py'), os.path.join(copy, 'skills'), os.path.join(d, 'build')], capture_output=True, text=True,
                           cwd=d, env={'PATH': B['bin'], 'LANG': 'en_US.UTF-8'}, timeout=900)
        self.assertEqual(r.returncode, 0, r.stdout[-2000:] + r.stderr[-2000:])
        self.assertRegex(r.stdout.strip().split('\n')[-1], r'^(\d+) of \1 vectors pass, 0 skipped$')

    def test_no_vector_is_left_unfilled(self):
        text = ''.join(vectors_text(n) for n in skills())
        for b in re.findall(r'```json vector\n(.*?)```', text, re.S):
            v = json.loads(b)
            for step in v.get('steps', [v]):
                for k in ('exit', 'stdout', 'stdout_text', 'stderr_text', 'files_out'):
                    if k in step: self.assertIsNotNone(step[k], f"{v['vector']}: {k}")

    def test_vector_names_are_unique_and_fixtures_exist(self):
        text = ''.join(vectors_text(n) for n in skills())
        names = [json.loads(b)['vector'] for b in re.findall(r'```json vector\n(.*?)```', text, re.S)]
        self.assertEqual(len(names), len(set(names)))
        fx = [json.loads(b) for b in re.findall(r'```json fixture\n(.*?)```', text, re.S)]
        fixtures = {f['fixture'] for f in fx}
        self.assertFalse(fixtures & {'out', 'home'}, '{out} and {home} are reserved')
        for f in fx:
            if 'base' in f: self.assertIn(f['base'], fixtures, f"base of {f['fixture']}")
        for b in re.findall(r'```json vector\n(.*?)```', text, re.S):
            v = json.loads(b)
            for step in v.get('steps', [v]):      # `{nothing}` is the one deliberately missing folder; placeholders are read in the inputs only, never in an expected output
                inputs = step.get('run', []) + list(step.get('files_out') or {}) + step.get('copy', []) + step.get('same_tree', [])
                for ref in re.findall(r'\{([a-z0-9-]+)\}', ' '.join(inputs)):
                    if ref not in ('out', 'home', 'nothing'): self.assertIn(ref, fixtures, f"{ref} in {v['vector']}")


class Payloads(unittest.TestCase):
    def test_json_blocks_parse(self):
        text = skill_text('adp-payloads')
        blocks = re.findall(r'```json\n(.*?)```', text, re.S)
        self.assertGreaterEqual(len(blocks), 6)
        for b in blocks: json.loads(b)

    def test_batches_fit_the_rules(self):
        text = skill_text('adp-payloads')
        for b in re.findall(r'```json\n(.*?)```', text, re.S):
            d = json.loads(b)
            writes = d.get('writes', [])
            self.assertLessEqual(len(writes), 50)
            for w in writes:
                if w['op'] == 'update': self.assertIn('if_version', w)
            if len(writes) > 1 and any(w['collection'] == 'manifest' for w in writes):
                self.assertEqual(writes[-1]['collection'], 'manifest')      # manifest/current goes last


if __name__ == '__main__':
    unittest.main()
