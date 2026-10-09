"""Regression checks for content preservation and safe repeatable synchronization."""
import importlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sync
from html_to_blocks import Compiler, Parser, walk


class SyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg, cls.files, cls.home, cls.report, cls.tokens = sync.build_artifacts()

    def test_repeat_build_is_byte_identical(self):
        self.assertEqual(self.files, sync.build_artifacts()[1])

    def test_import_has_no_write_side_effects(self):
        with patch.object(Path, 'write_text', side_effect=AssertionError('Import wrote files')):
            importlib.reload(sync)

    def test_original_testimonials_preserved(self):
        source = Parser(); source.feed((sync.ROOT / self.cfg['html']).read_text())
        output = Parser(); output.feed(self.home)
        # Core block comments/paragraph wrappers are permitted; quoted text is exact.
        def text(n):
            return ''.join(text(c) if hasattr(c, 'children') else c for c in n.children)
        def quotes(root):
            return [[(part.tag, ' '.join(text(part).split())) for part in walk(n)
                     if part.tag in ['p', 'cite']]
                    for n in walk(root) if n.tag == 'blockquote']
        a, b = quotes(source.root), quotes(output.root)
        self.assertEqual(len(a), 6)
        self.assertEqual(a, b)

    def test_native_headings_and_section_anchors_survive(self):
        source = Parser(); source.feed((sync.ROOT / self.cfg['html']).read_text())
        output = Parser(); output.feed(self.home)
        def text(n):
            return ''.join(text(c) if hasattr(c, 'children') else c for c in n.children)
        for tag in ['h2', 'h3', 'h4']:
            a = [' '.join(text(n).split()) for n in walk(source.root) if n.tag == tag]
            b = [' '.join(text(n).split()) for n in walk(output.root) if n.tag == tag]
            # Footer headings are compiled into a separate template part.
            self.assertEqual(a[:len(b)], b)
        self.assertEqual([n.attrs['id'] for n in walk(output.root) if n.tag == 'section'],
                         [s['slug'] for s in self.report['sections']])

    def test_configuration_ids_do_not_shift_when_another_node_is_added(self):
        c = Compiler(lambda s: s, {})
        before = c.marker({'aria-label': 'Magdalena Ostrowska'})
        c.marker({'aria-label': 'Nowy element przed portretem'})
        self.assertEqual(before, c.marker({'aria-label': 'Magdalena Ostrowska'}))

    def test_changed_media_is_rejected(self):
        assets = sync.Assets(self.cfg)
        name = next(iter(assets.media))
        assets.media[name]['sha256'] = 'not-the-uploaded-version'
        with self.assertRaisesRegex(ValueError, 'Asset changed'):
            assets.url(name)

    def test_unknown_destination_is_rejected(self):
        state = {'site_url': 'https://www.psyjacielevet.pl', 'theme_slug': self.cfg['theme_slug']}
        with self.assertRaisesRegex(ValueError, 'another site'):
            sync.plan(self.cfg, self.files, self.home, state)

    def test_existing_remote_content_never_deleted_by_plan(self):
        state = sync.read_json(sync.HERE / 'sync-state.json')
        state['files']['custom-user-file.php'] = '123'
        p = sync.plan(self.cfg, self.files, self.home, state)
        self.assertFalse(p['delete_automatically'])
        self.assertFalse(p['live_operations_automatic'])
        self.assertIn('custom-user-file.php', p['remote_only_files'])

    def test_build_does_not_replace_an_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp); (p / 'user.txt').write_text('keep me')
            with self.assertRaisesRegex(ValueError, 'not generated'):
                sync.write_output(p, self.cfg, self.files, self.home, self.report, self.tokens)
            self.assertEqual((p / 'user.txt').read_text(), 'keep me')

    def test_json_and_block_comments_are_balanced(self):
        for name, content in self.files.items():
            if name.endswith('.json'):
                json.loads(content)
            if name.endswith('.html') or name.startswith('patterns/'):
                self.assertGreater(sync.block_structure(content), 0)

    def test_figure_adapter_preserves_type_selector_specificity(self):
        css = self.files['assets/css/minimal.css']
        self.assertNotIn(':is(figure,.psy-figure)', css)
        self.assertIn(':is(figure,div):where(figure,.psy-figure)', css)


if __name__ == '__main__':
    unittest.main()
