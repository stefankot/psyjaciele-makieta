"""Pure HTML → native Gutenberg compiler. Importing this module never writes files."""
from collections import Counter
from html.parser import HTMLParser
import hashlib
import html
import json
import re

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Node:
    def __init__(self, tag, attrs=(), start=''):
        self.tag, self.attrs, self.start = tag, dict(attrs), start
        self.children = []


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node('root')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.get_starttag_text())
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs, self.get_starttag_text()))

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                return

    def handle_data(self, text):
        self.stack[-1].children.append(text)

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')


def walk(node):
    if isinstance(node, Node):
        yield node
        for child in node.children:
            yield from walk(child)


def raw(node):
    if isinstance(node, str):
        return node
    if node.tag == 'root':
        return ''.join(raw(x) for x in node.children)
    opening = node.start or '<' + node.tag + '>'
    if node.tag in VOID or opening.endswith('/>'):
        return opening
    return opening + ''.join(raw(x) for x in node.children) + '</' + node.tag + '>'


def attrs_text(attrs):
    return ''.join(' ' + k + '="' + html.escape(str(v), quote=True) + '"'
                   for k, v in attrs.items() if v is not None)


class Compiler:
    def __init__(self, rewrite, media):
        self.rewrite, self.media = rewrite, media
        self.configs, self.stats, self.fragments = {}, Counter(), []

    def block(self, name, attrs, inner):
        self.stats[name] += 1
        # Block comment JSON must never terminate the HTML comment.
        info = json.dumps(attrs, ensure_ascii=False, separators=(',', ':'))
        info = info.replace('--', '\\u002d\\u002d').replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
        return '<!-- wp:' + name + (' ' + info if attrs else '') + ' -->\n' + inner + '\n<!-- /wp:' + name + ' -->'

    def marker(self, props):
        if not props:
            return ''
        encoded = json.dumps(props, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        key = 'psy-config-' + hashlib.sha256(encoded.encode()).hexdigest()[:12]
        if key in self.configs and self.configs[key] != props:
            raise ValueError('Configuration hash collision: ' + key)
        self.configs[key] = props
        return key

    def config(self, node):
        return self.marker({k: self.rewrite(str(v)) for k, v in node.attrs.items()
                            if k not in ['id', 'class'] and v is not None})

    def children(self, node):
        return '\n\n'.join(self.convert(x) for x in node.children if isinstance(x, Node) or x.strip())

    def convert(self, node):
        if isinstance(node, str):
            return node if node.strip() else ''
        tag, a = node.tag, node.attrs
        c = a.get('class', '')
        if tag == 'nav' and a.get('id') == 'menu':
            links = []
            for child in node.children:
                if isinstance(child, Node) and child.tag == 'a':
                    attrs = {'label': html.unescape(re.sub('<[^>]+>', '', raw(child))),
                             'url': self.rewrite(child.attrs.get('href', '#')),
                             'kind': 'custom', 'isTopLevelLink': True}
                    links.append('<!-- wp:navigation-link ' + json.dumps(attrs, ensure_ascii=False, separators=(',', ':')) + ' /-->')
            return self.block('navigation', {'className': c, 'anchor': 'menu', 'overlayMenu': 'never',
                              'ariaLabel': 'Nawigacja główna', 'layout': {'type': 'flex', 'orientation': 'horizontal'}}, '\n'.join(links))
        if tag == 'a' and not set(c.split()) & {'brand', 'person-card-link', 'button'}:
            return self.block('paragraph', {'className': 'psy-inline-link'},
                              '<p class="psy-inline-link">' + self.rewrite(raw(node)) + '</p>')
        if tag == 'span' and 'kicker' in c.split():
            tag = 'p'
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']:
            typ = 'paragraph' if tag == 'p' else 'heading'
            attr, classes = {}, []
            if typ == 'heading':
                classes.append('wp-block-heading')
                if tag != 'h2':
                    attr['level'] = int(tag[1])
            cname = ' '.join(x for x in [c, self.config(node)] if x)
            if cname:
                attr['className'] = cname
                classes.extend(cname.split())
            if a.get('id'):
                attr['anchor'] = a['id']
            ha = {'class': ' '.join(classes)} if classes else {}
            if a.get('id'):
                ha['id'] = a['id']
            return self.block(typ, attr, '<' + tag + attrs_text(ha) + '>' + self.rewrite(''.join(raw(x) for x in node.children)) + '</' + tag + '>')
        if tag == 'img':
            m = self.media.get(a['src'])
            if not m:
                raise ValueError('Image missing from Media Library: ' + a['src'])
            # Verify bytes against the uploaded version even for native image blocks.
            if self.rewrite(a['src']) != m['url']:
                raise ValueError('Image URL registry mismatch: ' + a['src'])
            marker = self.marker({'image': {k: self.rewrite(str(v)) for k, v in a.items()
                                           if k not in ['src', 'alt'] and v is not None}})
            cname = 'psy-image-inner ' + marker
            attr = {'id': m['id'], 'sizeSlug': 'full', 'linkDestination': 'none', 'className': cname}
            img = '<img src="' + html.escape(m['url'], quote=True) + '" alt="' + html.escape(a.get('alt', ''), quote=True) + '" class="wp-image-' + str(m['id']) + '"/>'
            return self.block('image', attr, '<figure class="wp-block-image size-full ' + cname + '">' + img + '</figure>')
        if tag in ['ul', 'ol']:
            attr = {'ordered': True} if tag == 'ol' else {}
            if c:
                attr['className'] = c
            if a.get('id'):
                attr['anchor'] = a['id']
            ha = {'class': 'wp-block-list' + (' ' + c if c else '')}
            if a.get('id'):
                ha['id'] = a['id']
            return self.block('list', attr, '<' + tag + attrs_text(ha) + '>' + self.children(node) + '</' + tag + '>')
        if tag == 'li':
            inner = ''.join(self.convert(x) if isinstance(x, Node) and x.tag in ['ul', 'ol', 'p', 'h4'] else self.rewrite(raw(x)) for x in node.children)
            return self.block('list-item', {}, '<li>' + inner + '</li>')
        if tag == 'blockquote':
            attr = {'className': 'is-style-plain' + (' ' + c if c else '')}
            return self.block('quote', attr, '<blockquote class="wp-block-quote ' + attr['className'] + '">' + self.children(node) + '</blockquote>')
        if tag == 'a' and 'button' in c.split():
            attr = {'className': c}
            link = '<a class="wp-block-button__link wp-element-button" href="' + html.escape(self.rewrite(a.get('href', '#')), quote=True) + '">' + self.rewrite(''.join(raw(x) for x in node.children)) + '</a>'
            btn = self.block('button', attr, '<div class="wp-block-button ' + c + '">' + link + '</div>')
            return self.block('buttons', {}, '<div class="wp-block-buttons">' + btn + '</div>')
        if tag in ['div', 'section', 'article', 'header', 'footer', 'main', 'aside', 'nav', 'figure']:
            attr, outtag = {'layout': {'type': 'default'}}, 'div' if tag == 'figure' else tag
            if outtag != 'div':
                attr['tagName'] = outtag
            cname = ' '.join(x for x in [c, 'psy-figure' if tag == 'figure' else '', self.config(node)] if x)
            if cname:
                attr['className'] = cname
            if a.get('id'):
                attr['anchor'] = a['id']
            ha = {'class': 'wp-block-group' + (' ' + cname if cname else '')}
            if a.get('id'):
                ha['id'] = a['id']
            return self.block('group', attr, '<' + outtag + attrs_text(ha) + '>' + self.children(node) + '</' + outtag + '>')
        self.fragments.append({'tag': tag, 'class': c, 'id': a.get('id', '')})
        return self.block('html', {}, self.rewrite(raw(node)))
