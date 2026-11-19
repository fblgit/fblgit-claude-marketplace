"""plugins/adp-minimal is documentation only. These tests keep it that way, keep its links whole, and (with a checkout of the ADP repository
beside this one, or at $ADP_REPO) keep its copied pages equal to their sources and run its code snippets against the real adp.py, so the hash
arithmetic on the page is the one the tool uses."""
import json
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = os.path.join(ROOT, 'plugins', 'adp-minimal')
SKILL = os.path.join(MIN, 'skills', 'adp-minimal')
ADP = os.environ.get('ADP_REPO') or os.path.join(os.path.dirname(ROOT), 'artifacts-done-properly')
HAVE_ADP = os.path.isdir(os.path.join(ADP, 'plugins', 'artifacts-done-properly'))
if HAVE_ADP:
    sys.path.insert(0, os.path.join(ADP, 'plugins', 'artifacts-done-properly', 'skills', 'adp', 'scripts'))
    import adp

ALLOWED = {'.md', '.json', '.png', ''}      # '' = LICENSE and NOTICE


def files():
    for d, _, names in os.walk(MIN):
        for n in names:
            yield os.path.join(d, n)


class Content(unittest.TestCase):
    def test_only_files_the_directory_takes(self):
        for p in files():
            self.assertIn(os.path.splitext(p)[1], ALLOWED, p)
            if p.endswith(('.md', '.json')) or not os.path.splitext(p)[1]:
                with open(p, 'rb') as f: b = f.read()
                self.assertFalse(b.startswith(b'#!'), p)
                self.assertNotIn(b'\x00', b, p)
                b.decode('utf-8')

    @unittest.skipUnless(HAVE_ADP, 'no ADP checkout')
    def test_copies_equal_their_sources_and_the_version_is_adps(self):
        r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'make_minimal.py'), '--adp', ADP, '--check'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)

    def test_skill_version_matches_the_plugin(self):
        with open(os.path.join(MIN, '.claude-plugin', 'plugin.json')) as f: v = json.load(f)['version']
        with open(os.path.join(SKILL, 'SKILL.md')) as f: text = f.read()
        self.assertIn(f'version: "{v}"', text)
        self.assertRegex(text, r'(?m)^name: adp-minimal$')
        self.assertRegex(text, r'(?m)^description: ".+"$')

    def test_relative_links_resolve(self):
        link = re.compile(r'\]\((?!https?:|#|mailto:)([^)\s#]+)')
        for p in files():
            if not p.endswith('.md'): continue
            with open(p, encoding='utf-8') as f: text = f.read()
            for href in link.findall(text):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), href))), f'{p}: {href}')

    def test_every_page_is_linked_from_the_skill(self):
        with open(os.path.join(SKILL, 'SKILL.md')) as f: text = f.read()
        with open(os.path.join(SKILL, 'references', 'concepts.md')) as f: text += f.read()
        for n in os.listdir(os.path.join(SKILL, 'references')):
            if n.endswith('.md'): self.assertIn(n, text, n)


@unittest.skipUnless(HAVE_ADP, 'no ADP checkout')
class Snippets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(SKILL, 'references', 'snippets.md'), encoding='utf-8') as f: text = f.read()
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


class Payloads(unittest.TestCase):
    def test_json_blocks_parse(self):
        with open(os.path.join(SKILL, 'references', 'payloads.md'), encoding='utf-8') as f: text = f.read()
        blocks = re.findall(r'```json\n(.*?)```', text, re.S)
        self.assertGreaterEqual(len(blocks), 6)
        for b in blocks: json.loads(b)

    def test_batches_fit_the_rules(self):
        with open(os.path.join(SKILL, 'references', 'payloads.md'), encoding='utf-8') as f: text = f.read()
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
