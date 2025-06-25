import os
from html.parser import HTMLParser

SELF_CLOSING = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img',
    'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'
}

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.unmatched = False

    def handle_starttag(self, tag, attrs):
        if tag not in SELF_CLOSING:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        # self closing tags handled implicitly
        pass

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.unmatched = True

    def error(self, message):
        self.unmatched = True


def all_tags_closed(html: str) -> bool:
    parser = TagChecker()
    parser.feed(html)
    parser.close()
    return not parser.unmatched and len(parser.stack) == 0


def test_readme_html_tags_closed():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(root_dir, 'README.md'), encoding='utf-8') as f:
        content = f.read()
    assert all_tags_closed(content), 'Existem tags HTML não fechadas corretamente em README.md'
