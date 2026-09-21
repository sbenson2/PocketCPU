#!/usr/bin/env python3
"""Validate the static site's metadata, local links, and published assets."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import re
import struct
import sys
import xml.etree.ElementTree as ET

SITE = 'https://sbenson2.github.io/PocketCPU/'
PAGES = ('index.html', 'guide.html', 'privacy.html', 'press.html')


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.ids = []
        self.title = ''
        self.in_title = False
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def local_target(root, source, raw):
    """Return a same-site file plus fragment, or None for an external link."""
    url = urlparse(raw)
    if raw.startswith(SITE):
        url = urlparse(raw[len(SITE):])
        parent = root
    elif url.scheme or url.netloc:
        if url.scheme not in ('https', 'mailto'):
            raise ValueError('unsupported URL scheme: ' + raw)
        return None
    else:
        if url.path.startswith('/'):
            raise ValueError('root-relative URL breaks the project Pages prefix: ' + raw)
        parent = source.parent
    path = (parent / unquote(url.path)).resolve() if url.path else source
    if path.is_dir():
        path /= 'index.html'
    if not path.is_relative_to(root):
        raise ValueError('link escapes the site: ' + raw)
    if not path.is_file():
        raise ValueError('missing target: ' + raw)
    return path, unquote(url.fragment)


def check(root):
    root = root.resolve()
    errors = []
    pages = {}
    for name in PAGES:
        path = root / name
        if not path.is_file():
            errors.append('missing page: ' + name)
        else:
            pages[path] = Page(path.read_text(encoding='utf-8'))
    for path, page in pages.items():
        def fail(message):
            errors.append(path.name + ': ' + message)
        if not any(tag == 'html' and attrs.get('lang') for tag, attrs in page.tags):
            fail('missing html lang')
        if not page.title.strip():
            fail('missing title')
        if not any(tag == 'meta' and attrs.get('name') == 'description' and attrs.get('content', '').strip() for tag, attrs in page.tags):
            fail('missing description')
        canonical = SITE + ('' if path.name == 'index.html' else path.name)
        if not any(tag == 'link' and attrs.get('rel') == 'canonical' and attrs.get('href') == canonical for tag, attrs in page.tags):
            fail('missing or incorrect canonical URL')
        if len(page.ids) != len(set(page.ids)):
            fail('duplicate id')
        if sum(tag == 'h1' for tag, _ in page.tags) != 1:
            fail('expected one main heading')
        for tag, attrs in page.tags:
            if tag in ('script', 'form', 'iframe') or any(key.startswith('on') for key in attrs):
                fail('unexpected interactive/embedded content: ' + tag)
            refs = [attrs[key] for key in ('src', 'href', 'action') if attrs.get(key)]
            if tag == 'meta' and attrs.get('property') in ('og:image', 'og:url'):
                refs.append(attrs.get('content', ''))
            for raw in refs:
                try:
                    target = local_target(root, path, raw)
                    if target:
                        dest, fragment = target
                        if fragment and (dest not in pages or fragment not in pages[dest].ids):
                            fail('missing fragment: ' + raw)
                    elif tag not in ('a',) and attrs.get('rel') != 'canonical':
                        fail('external asset: ' + raw)
                except ValueError as error:
                    fail(str(error))
            if tag == 'img':
                if 'alt' not in attrs:
                    fail('image missing alt attribute')
                try:
                    target = local_target(root, path, attrs.get('src', ''))
                    if target and target[0].suffix == '.png':
                        data = target[0].read_bytes()
                        if data[:8] != b'\x89PNG\r\n\x1a\n' or len(data) < 24:
                            raise ValueError('invalid PNG')
                        dimensions = struct.unpack('>II', data[16:24])
                        declared = (int(attrs.get('width', 0)), int(attrs.get('height', 0)))
                        if dimensions != declared:
                            fail('PNG width/height mismatch: ' + attrs['src'])
                except (ValueError, OSError) as error:
                    fail(str(error))
    css = root / 'styles.css'
    if css.is_file():
        text = css.read_text()
        if re.search(r'@import\b', text, re.I):
            errors.append('stylesheet imports are not allowed')
        for raw in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)', text, re.I):
            try:
                if local_target(root, css, raw.strip()) is None:
                    errors.append('external CSS asset: ' + raw)
            except ValueError as error:
                errors.append(str(error))
    try:
        sitemap = ET.parse(root / 'sitemap.xml')
        urls = {element.text for element in sitemap.iter() if element.tag.endswith('}loc')}
        expected = {SITE + ('' if name == 'index.html' else name) for name in PAGES}
        if urls != expected:
            errors.append('sitemap does not match published pages')
        if 'Sitemap: ' + SITE + 'sitemap.xml' not in (root / 'robots.txt').read_text():
            errors.append('robots.txt has the wrong sitemap')
    except (OSError, ET.ParseError) as error:
        errors.append(str(error))
    return errors


if __name__ == '__main__':
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1]).resolve()
    errors = check(root)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print('PocketCPU site integrity: 4 pages, local links, metadata, and assets verified')
