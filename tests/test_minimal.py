"""plugins/adp-minimal is documentation only. These tests keep it that way, keep its links whole, keep it free of copied pages and of stale developer notes, and
(with a checkout of the ADP repository beside this one, or at $ADP_REPO) run its code snippets against the real adp.py, so the hash arithmetic on the page is the one the tool uses."""
import json
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = os.path.join(ROOT, 'plugins', 'adp-minimal')
SKILLS = os.path.join(MIN, 'skills')
ADP = os.environ.get('ADP_REPO') or os.path.join(os.path.dirname(ROOT), 'artifacts-done-properly')
HAVE_ADP = os.path.isdir(os.path.join(ADP, 'plugins', 'artifacts-done-properly'))
SKIP_VECTORS = os.environ.get('ADP_SKIP_VECTORS') == '1'      # the only way to not check the vectors: a missing checkout fails, it does not skip
if HAVE_ADP:
    sys.path.insert(0, os.path.join(ADP, 'plugins', 'artifacts-done-properly', 'skills', 'adp', 'scripts'))
    import adp

ALLOWED = {'.md', '.json', '.png', ''}      # '' = LICENSE and NOTICE


def skills():
    return sorted(n for n in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, n, 'SKILL.md')))


def skill_text(name):
    with open(os.path.join(SKILLS, name, 'SKILL.md'), encoding='utf-8') as f: return f.read()


def vectors_text(name):
    p = os.path.join(SKILLS, name, 'vectors.md')
    if not os.path.isfile(p): return ''
    with open(p, encoding='utf-8') as f: return f.read()


def need_adp():
    if not HAVE_ADP:
        raise AssertionError(f'no ADP checkout at {ADP}: clone https://github.com/fblgit/artifacts-done-properly there or set ADP_REPO '
                             '(ADP_SKIP_VECTORS=1 skips these checks on purpose)')


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
            with open(p, encoding='utf-8') as f: text = f.read()
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

    def test_skills_carry_no_reference_folders(self):
        """Each topic is its own skill, loaded by its description: no references/ for the model to choose from."""
        for n in skills():
            self.assertIn(sorted(os.listdir(os.path.join(SKILLS, n))), (['SKILL.md'], ['SKILL.md', 'vectors.md']), n)

    def test_fixtures_and_vectors_live_beside_the_skill(self):
        """A skill loads its contract, not its vectors: every json fixture and json vector block is in vectors.md, never in SKILL.md."""
        for n in skills():
            self.assertNotRegex(skill_text(n), r'```json (fixture|vector)\n', n)

    def test_the_router_states_the_rule_and_names_every_skill(self):
        text = skill_text('adp-minimal')
        low = text.lower()
        for needle in ('never by hand outside it', '/plugin install artifacts-done-properly@fblgit-adp', 'do not claim you wrote', '`manifest/current` last'):
            self.assertIn(needle, low, needle)
        for n in skills():
            if n != 'adp-minimal': self.assertIn(f'`{n}`', text, n)


@unittest.skipIf(SKIP_VECTORS, 'ADP_SKIP_VECTORS=1')
class Snippets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        need_adp()
        text = skill_text('adp-minimal-snippets')
        blocks = re.findall(r'```python\n(.*?)```', text, re.S)
        cls.ns = {}
        for b in blocks: exec(compile(b, 'snippets.md', 'exec'), cls.ns)      # in order: later snippets use the earlier ones

    PAGE = ('<!doctype html><html><body>\n<!-- part:a.one -->\n<p data-part="a.one">One <b>x</b></p>\n'
            '<!-- part:a.two -->  <p data-part="a.two">Two</p>\n<!-- /part:a.two -->\n<!-- /part:a.one -->\n'
            'outside   text\n<script>\n/* part:page.script */ let x = 1; /* /part:page.script */\n</script></body></html>\n')

    def test_part_hashes_are_the_tools(self):
        want = adp.manifest(self.PAGE, {})['parts']
        self.assertEqual(self.ns['part_hashes'](self.PAGE), want)

    def test_page_hash_is_the_tools(self):
        m = adp.manifest(self.PAGE, {})
        self.assertEqual(self.ns['page_hash'](self.ns['part_hashes'](self.PAGE), {}), m['page_hash'])

    def test_problems_are_refused(self):
        for bad in ('<!-- part:a.x -->', '<!-- /part:a.x -->', '<!-- part:a.x --><!-- part:a.x --><!-- /part:a.x -->'):
            with self.assertRaises(ValueError): self.ns['part_hashes'](bad)

    def test_diff_and_ids(self):
        a, r, c = self.ns['diff']({'p': '1', 'q': '2', 'r': '3'}, {'p': '1', 'q': '9', 's': '4'})
        self.assertEqual((a, r, c), (['s'], ['r'], ['q']))
        self.assertEqual(self.ns['next_change'](['000001', '000007', 'archive-1']), '000008')
        self.assertEqual(self.ns['pinned']('update', 'parts', 'a.one', {'x': 1}, 3)['if_version'], 3)
        self.assertNotIn('if_version', self.ns['pinned']('set', 'parts', 'a.one', {}))


@unittest.skipIf(SKIP_VECTORS, 'ADP_SKIP_VECTORS=1')
class Vectors(unittest.TestCase):
    """Every fixture and vector in the skills, through the runner written in adp-minimal-rebuild, against the real ADP tools."""

    def test_every_vector_passes_on_the_real_tools(self):
        need_adp()
        sys.path.insert(0, os.path.join(ROOT, 'tools'))
        import vectors
        results = vectors.load_runner()['run'](SKILLS, vectors.tools_of(ADP))
        self.assertGreaterEqual(len(results), 10)
        failed = [f"{r['vector']}: {r['problems']}" for r in results if not r['ok']]
        self.assertEqual(failed, [])

    def test_adp_js_hashes_like_adp_py(self):
        """The runtime's hash of a page must be the manifest's: the two vectors that hash the same file agree."""
        text = ''.join(vectors_text(n) for n in skills())
        v = {json.loads(b)['vector']: json.loads(b) for b in re.findall(r'```json vector\n(.*?)```', text, re.S)}
        py, js = v['manifest-single']['stdout'], v['adp-js-hash-single']['stdout']
        self.assertEqual(js['page_hash'], py['page_hash'])
        self.assertEqual(js['parts'], py['parts'])
        self.assertEqual(js['parents'], {k: v for k, v in py['parents'].items() if k != '_rest'})      # adp.js leaves _rest out of parents

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
            for step in v.get('steps', [v]):      # placeholders are read in the inputs only, never in an expected output
                inputs = step.get('run', []) + list(step.get('files_out') or {}) + step.get('copy', []) + step.get('same_tree', [])
                for ref in re.findall(r'\{([a-z0-9-]+)\}', ' '.join(inputs)):
                    if ref not in ('out', 'home'): self.assertIn(ref, fixtures, f"{ref} in {v['vector']}")


class Payloads(unittest.TestCase):
    def test_json_blocks_parse(self):
        text = skill_text('adp-minimal-payloads')
        blocks = re.findall(r'```json\n(.*?)```', text, re.S)
        self.assertGreaterEqual(len(blocks), 6)
        for b in blocks: json.loads(b)

    def test_batches_fit_the_rules(self):
        text = skill_text('adp-minimal-payloads')
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
