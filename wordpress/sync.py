#!/usr/bin/env python3
"""Repeatable, offline staging build and WPVibe synchronization plan.

No command publishes or changes WordPress. Generated files are disposable;
index-min.html, its assets and theme-source are the editable sources.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import urlsplit
import zipfile

from html_to_blocks import Compiler, Node, Parser, raw, walk

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ALLOWED_SITE = 'https://www.psyjacielevet.pl/mystaging02'
TITLES = {
    'poczatek': 'Hero — zdanie z ilustracją', 'onas': 'Założycielki — portrety i aureola',
    'uslugi': 'Usługi — siatka z separatorami', 'zapraszamy': 'Zaproszenie — zdjęcie i przyciski',
    'przychodnia': 'Przychodnia — ilustracja i trzy kolumny', 'zespol': 'Zespół — rejestr osób',
    'rekomendacje': 'Opinie — siatka cytatów', 'obserwuj-nas': 'Obserwuj nas — dwie połowy i logo',
    'nagle-przypadki': 'Nagłe przypadki — instrukcja i lecznice', 'przygotowanie': 'Przed wizytą — sześć wskazówek',
    'dojazd': 'Dojazd — adres, mapa i trzy kolumny', 'pytania': 'Częste pytania — sześć odpowiedzi',
    'kontakt': 'Kontakt — ilustracja i dane',
}


def read_json(path):
    return json.loads(Path(path).read_text())


def sha(data):
    # read_file cannot distinguish an absent final newline; code hashes normalize it.
    return hashlib.sha256(data if isinstance(data, bytes) else data.rstrip('\n').encode()).hexdigest()


def dump(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def config():
    cfg = read_json(HERE / 'sync-config.json')
    if cfg['site_url'].rstrip('/') != ALLOWED_SITE or cfg['home_page_id'] != 14:
        raise ValueError('This project synchronizes only mystaging02 home page 14.')
    if cfg['theme_slug'] != 'psyjaciele-staging':
        raise ValueError('Unexpected destination theme.')
    return cfg


def design_tokens(theme):
    values = []
    for item in theme['settings']['color']['palette']:
        values.append('--wp--preset--color--' + item['slug'] + ':' + item['color'])
    for item in theme['settings']['typography']['fontFamilies']:
        values.append('--wp--preset--font-family--' + item['slug'] + ':' + item['fontFamily'])
    for item in theme['settings']['typography']['fontSizes']:
        values.append('--wp--preset--font-size--' + item['slug'] + ':' + item['size'])
    values.extend(['--font-main:var(--wp--preset--font-family--satoshi)',
                   '--font-emphasis:var(--wp--preset--font-family--rialto-script)'])
    custom = theme['settings']['custom']['psyjaciele']
    for key, prop in [('gutter', '--gutter'), ('columnGap', '--gap'), ('sectionSpace', '--section-space'),
                      ('contentGap', '--content-gap'), ('groupGap', '--group-gap')]:
        values.append(prop + ':' + custom[key])
    values.append('--width:' + theme['settings']['layout']['wideSize'])
    return '/* Generated from wordpress/theme-source/theme.json; edit that source. */\n:root{' + ';'.join(values) + '}\n@media(min-width:701px) and (max-width:1000px){:root{--gap:24px;--group-gap:48px}}\n@media(max-width:700px){:root{--gap:16px;--gutter:24px;--section-space:64px;--group-gap:48px}}\n'


class Assets:
    def __init__(self, cfg):
        self.cfg = cfg
        self.media = read_json(HERE / 'media-map.json')
        self.remote = read_json(HERE / 'remote-assets.json')
        self.used = {}

    def url(self, name):
        p = (ROOT / name).resolve()
        if not p.is_relative_to(ROOT.resolve()) or not p.is_file():
            raise ValueError('Missing local asset: ' + name)
        row = self.media.get(name) or self.remote.get(name)
        if not row:
            raise ValueError('Upload/register new asset before build: ' + name)
        digest = sha(p.read_bytes())
        if row.get('sha256') != digest:
            raise ValueError('Asset changed since upload. Upload a new version and update media-map/remote-assets: ' + name)
        self.used[name] = {'url': row['url'], 'sha256': digest, **({'id': row['id']} if 'id' in row else {})}
        return row['url']

    def rewrite(self, text):
        # This one dynamic atlas expression cannot be found by a static URL regex.
        old = "`url(assets/${id < 64 ? 'pets-phone-atlas.png' : 'pets-phone-atlas-unique-v2.png'})`"
        if old in text:
            text = text.replace(old, "`url(${id < 64 ? '" + self.url('assets/pets-phone-atlas.png') + "' : '" + self.url('assets/pets-phone-atlas-unique-v2.png') + "'})`")
        text = re.sub(r'(?<![\w/-])assets/[a-zA-Z0-9_./-]+', lambda m: self.url(m[0]), text)
        if 'assets/${' in text:
            raise ValueError('Unresolved dynamic asset URL; add an explicit resolver.')
        text = text.replace('href="index-min.html"', 'href="' + self.cfg['site_url'] + '/"')
        text = re.sub(r'href="([^"#?:]+?)/index.html([^"]*)"',
                      lambda m: 'href="' + self.cfg['site_url'] + '/' + m[1] + '/' + m[2] + '"', text)
        # Keep all own-site links inside staging. External booking/social links stay intact.
        text = re.sub(r'https://www\.psyjacielevet\.pl/(?!mystaging02(?:/|["#?]|$))', self.cfg['site_url'] + '/', text)
        return text


def source_assets(head, tag, key):
    return [urlsplit(n.attrs[key]).path for n in walk(head)
            if n.tag == tag and key in n.attrs and not urlsplit(n.attrs[key]).scheme]


def block_structure(content):
    stack, count = [], 0
    for m in re.finditer(r'<!--\s*(/?)wp:([\w/-]+)(.*?)-->', content, re.S):
        closing, name, attrs = m.groups()
        if closing:
            if not stack or stack.pop() != name:
                raise ValueError('Unbalanced Gutenberg block: ' + name)
        else:
            count += 1
            if attrs.strip().rstrip('/').strip():
                json.loads(attrs.strip().rstrip('/').strip())
            if not attrs.strip().endswith('/'):
                stack.append(name)
    if stack:
        raise ValueError('Unclosed Gutenberg blocks: ' + str(stack))
    return count


def build_artifacts():
    cfg = config()
    parser = Parser()
    html_text = (ROOT / cfg['html']).read_text()
    parser.feed(html_text)
    nodes = list(walk(parser.root))
    head = next(n for n in nodes if n.tag == 'head')
    body = next(n for n in nodes if n.tag == 'body')
    main = next(n for n in nodes if n.tag == 'main')
    sections = [n for n in main.children if isinstance(n, Node) and n.tag == 'section']
    ids = [n.attrs.get('id') for n in nodes if n.attrs.get('id')]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate HTML ids.')
    if len(sections) != len(TITLES) or set(n.attrs['id'] for n in sections) != set(TITLES):
        raise ValueError('Unexpected home section set. Update the explicit section contract first.')
    if 'wp:' in html_text:
        raise ValueError('Local source must be HTML, not generated Gutenberg markup.')
    assets = Assets(cfg)
    compiler = Compiler(assets.rewrite, assets.media)
    files, manifest = {}, []
    base = HERE / 'theme-source'
    for p in sorted(base.rglob('*')):
        if p.is_file():
            files[str(p.relative_to(base))] = p.read_text()
    theme = json.loads(files['theme.json'])
    if 'Template: ' + cfg['parent_theme'] not in files['style.css']:
        raise ValueError('Parent theme mismatch.')
    css = source_assets(head, 'link', 'href')
    css = [n for n in css if n.endswith('.css')]
    scripts = source_assets(body, 'script', 'src')
    for name in css + scripts:
        if Path(name).name != name:
            raise ValueError('Styles/scripts must be root-relative source files: ' + name)
    tokens = design_tokens(theme)
    palette = {}
    for item in theme['settings']['color']['palette']:
        palette.setdefault(item['color'].lower(), item['slug'])
    for name in css:
        text = tokens if name == 'design-tokens.css' else (ROOT / name).read_text()
        text = assets.rewrite(text)
        # Preserve type-selector specificity when a native Group replaces figure.
        text = re.sub(r'\bfigure\b', ':is(figure,div):where(figure,.psy-figure)', text)
        if name != 'design-tokens.css':
            text = re.sub(r'#[a-fA-F0-9]{6}\b', lambda m: 'var(--wp--preset--color--' + palette[m[0].lower()] + ')' if m[0].lower() in palette else m[0], text)
        files['assets/css/' + name] = text
    for name in scripts:
        files['assets/js/' + name] = assets.rewrite((ROOT / name).read_text())
    # The generated enqueue list follows the actual local HTML, in the same order.
    enqueue = {'styles': [Path(n).stem for n in css] + ['wordpress'],
               'scripts': ['adapter'] + [Path(n).stem for n in scripts]}
    files['assets/enqueue.json'] = dump(enqueue)
    for i, section in enumerate(sections, 1):
        slug = section.attrs['id']
        content = compiler.convert(section)
        files[f'patterns/{i:02d}-{slug}.php'] = '<?php\n/**\n * Title: ' + TITLES[slug] + '\n * Slug: ' + cfg['theme_slug'] + '/' + slug + '\n * Categories: psyjaciele-sections\n * Inserter: true\n */\n?>\n' + content + '\n'
        manifest.append({'slug': slug, 'title': TITLES[slug], 'content': content})
    header = next(n for n in body.children if isinstance(n, Node) and n.tag == 'header')
    backdrop = next(n for n in body.children if isinstance(n, Node) and 'header-backdrop' in n.attrs.get('class', ''))
    footer = next(n for n in body.children if isinstance(n, Node) and n.tag == 'footer')
    filters = [n for n in body.children if isinstance(n, Node) and n.tag == 'svg']
    files['parts/home-header.html'] = compiler.block('html', {}, '<a class="skip" href="#main">Przejdź do treści</a>\n' + raw(backdrop)) + '\n\n' + compiler.convert(header) + '\n'
    files['parts/home-footer.html'] = compiler.convert(footer) + '\n\n' + '\n'.join(compiler.block('html', {}, assets.rewrite(raw(n))) for n in filters) + '\n'
    home = '\n\n'.join(s['content'] for s in manifest)
    files['content/home.html'] = home
    # Keep existing numbered markers during the theme-first/page-second transition.
    legacy = read_json(HERE / 'legacy-block-config.json')
    files['assets/block-config.json'] = dump({**legacy, **compiler.configs})
    files['sync-manifest.json'] = dump({'schema': 1, 'site_url': cfg['site_url'], 'page_id': cfg['home_page_id'],
                                       'source_sha256': sha(html_text), 'home_sha256': sha(home)})
    blocks = block_structure(home)
    for name, text in files.items():
        if name.endswith('.html') or name.startswith('patterns/'):
            block_structure(text)
    return cfg, files, home, {
        'sections': [{'slug': s['slug'], 'title': s['title']} for s in manifest],
        'blocks': dict(compiler.stats), 'home_blocks': blocks, 'stable_configs': len(compiler.configs),
        'graphic_fragments': compiler.fragments, 'assets': assets.used,
        'styles': enqueue['styles'], 'scripts': enqueue['scripts'],
    }, tokens


def hashes(files):
    return {name: sha(content) for name, content in sorted(files.items())}


def state_path(target='draft'):
    draft = HERE / 'draft-state.json'
    return draft if target == 'draft' and draft.exists() else HERE / 'sync-state.json'


def plan(cfg, files, home, state):
    if state.get('site_url') != cfg['site_url'] or state.get('theme_slug') != cfg['theme_slug']:
        raise ValueError('Remote snapshot belongs to another site or theme.')
    changed = [name for name, digest in hashes(files).items() if state.get('files', {}).get(name) != digest]
    remote_only = sorted(set(state.get('files', {})) - set(files))
    return {
        'schema': 1, 'site_url': cfg['site_url'], 'theme_slug': cfg['theme_slug'], 'page_id': cfg['home_page_id'],
        'baseline_provenance': state.get('provenance', 'Verified remote snapshot'),
        'expected_remote_files': {name: state.get('files', {}).get(name) for name in changed},
        'expected_remote_home_sha256': state.get('home_sha256'),
        'draft_files': [{'tool': 'write_file', 'path': name, 'source': 'theme/' + name, 'sha256': sha(files[name])} for name in changed],
        'remote_only_files': remote_only, 'delete_automatically': False,
        'home_changed': sha(home) != state.get('home_sha256'), 'home_payload': 'home-update.json',
        'live_operations_automatic': False,
        'sequence': ['Re-read changed remote files and page 14; stop on any baseline conflict.',
                     'Write changed theme files into the existing WPVibe draft.',
                     'Review the draft: it renders content/home.html without changing page 14.',
                     'After explicit approval, publish the draft theme on mystaging02.',
                     'Re-read page 14 and compare expected hash; update only its content via home-update.json.',
                     'Purge caches, verify the plain staging URL, then record fresh remote hashes.'],
    }


def write_output(out, cfg, files, home, report, tokens):
    out = out.resolve()
    if out == ROOT.resolve() or out in ROOT.resolve().parents:
        raise ValueError('Build output may not replace the HTML source.')
    if out.exists() and any(out.iterdir()) and not (out / 'build-manifest.json').exists():
        raise ValueError('Refusing to overwrite a folder not generated by this tool: ' + str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix='.psy-build-', dir=out.parent))
    try:
        for name, content in files.items():
            path = temp / 'theme' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        (temp / 'home-content.html').write_text(home)
        (temp / 'home-update.json').write_text(dump({'content': home}))
        state = read_json(state_path())
        (temp / 'sync-plan.json').write_text(dump(plan(cfg, files, home, state)))
        (temp / 'report.json').write_text(dump(report))
        (temp / 'build-manifest.json').write_text(dump({'schema': 1, 'site_url': cfg['site_url'],
            'theme_slug': cfg['theme_slug'], 'files': hashes(files), 'home_sha256': sha(home)}))
        with zipfile.ZipFile(temp / (cfg['theme_slug'] + '.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, content in sorted(files.items()):
                info = zipfile.ZipInfo(cfg['theme_slug'] + '/' + name, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, content.encode())
        if out.exists():
            shutil.rmtree(out)
        temp.rename(out)
        (ROOT / 'design-tokens.css').write_text(tokens)
    finally:
        if temp.exists():
            shutil.rmtree(temp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'check', 'plan', 'verify-remote'])
    parser.add_argument('--out', type=Path)
    parser.add_argument('--snapshot', type=Path, help='Fresh remote hashes for plan/verify-remote.')
    parser.add_argument('--target', choices=['draft', 'published'], default='draft', help='Compare to the last draft upload or published baseline.')
    args = parser.parse_args()
    cfg, files, home, report, tokens = build_artifacts()
    if args.command == 'build':
        out = args.out or (ROOT / cfg['output'])
        write_output(out, cfg, files, home, report, tokens)
        print(dump({'output': str(out.resolve()), 'theme_files': len(files), 'home_blocks': report['home_blocks'],
                    'sections': len(report['sections']), 'assets': len(report['assets'])}), end='')
    elif args.command == 'check':
        # A second independent compile catches order/state/import side effects.
        again = build_artifacts()
        if files != again[1] or home != again[2]:
            raise ValueError('Non-deterministic build.')
        print(dump({'ok': True, 'deterministic': True, 'sections': len(report['sections']),
                    'home_blocks': report['home_blocks'], 'assets': len(report['assets'])}), end='')
    elif args.command == 'plan':
        print(dump(plan(cfg, files, home, read_json(args.snapshot or state_path(args.target)))), end='')
    else:
        if not args.snapshot:
            parser.error('verify-remote requires --snapshot with fresh remote file and home hashes.')
        baseline = read_json(state_path(args.target))
        fresh = read_json(args.snapshot)
        if fresh.get('site_url') != cfg['site_url'] or fresh.get('theme_slug') != cfg['theme_slug']:
            raise ValueError('Wrong site in remote snapshot.')
        changes = plan(cfg, files, home, baseline)
        conflicts = [name for name in changes['expected_remote_files']
                     if baseline.get('files', {}).get(name) != fresh.get('files', {}).get(name)]
        if baseline.get('home_sha256') != fresh.get('home_sha256'):
            conflicts.append('page:14')
        if conflicts:
            raise ValueError('Remote edits detected; merge before sync: ' + ', '.join(conflicts))
        print(dump({'ok': True, 'remote_conflicts': []}), end='')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration) as exc:
        print('Sync blocked: ' + str(exc), file=sys.stderr)
        sys.exit(1)
