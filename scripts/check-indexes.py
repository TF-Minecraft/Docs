#!/usr/bin/env python3
"""Check local Markdown links, section anchors, and project navigation."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt


class HTMLLinks(HTMLParser):
    """Collect explicit HTML links and anchors embedded in Markdown."""

    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        for key in ("id", "name"):
            if attrs.get(key):
                self.anchors.add(attrs[key])


def parse_markdown(text):
    """Resolve inline/reference links and GitHub-style heading anchors."""
    tokens = MarkdownIt("commonmark").parse(text)
    links, anchors = [], set()
    html = HTMLLinks()
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            children = tokens[index + 1].children or []
            title = "".join(t.content for t in children if t.type in ("text", "code_inline", "image"))
            base = "".join(
                char for char in title.lower()
                if char in "-_ " or not unicodedata.category(char).startswith(("P", "S", "C"))
            ).replace(" ", "-")
            anchor, count = base, 0
            while anchor in anchors:
                count += 1
                anchor = f"{base}-{count}"
            anchors.add(anchor)
        if token.type == "html_block":
            html.feed(token.content)
        for child in token.children or []:
            if child.type == "link_open":
                links.append(child.attrGet("href"))
            elif child.type == "image":
                links.append(child.attrGet("src"))
            elif child.type == "html_inline":
                html.feed(child.content)
    return links + html.links, anchors | html.anchors


def check(root):
    """Return broken links and navigation errors for a documentation tree."""
    root = root.resolve()
    pages = {
        file.resolve(): parse_markdown(file.read_text(encoding="utf-8"))
        for file in root.rglob("*.md") if ".git" not in file.parts
    }
    errors, checked = [], 0
    for file, (links, _) in pages.items():
        for link in links:
            target = urlsplit(link)
            if target.scheme or target.netloc:
                continue
            checked += 1
            path = (file.parent / unquote(target.path)).resolve() if target.path else file
            if not path.is_relative_to(root) or not path.exists():
                errors.append(f"{file.relative_to(root)}: missing local link {link}")
                continue
            if path.is_dir():
                path = next((path / name for name in ("README.md", "index.md") if (path / name).exists()), path)
            if target.fragment and path in pages:
                fragment = unquote(target.fragment)
                if fragment not in pages[path][1]:
                    errors.append(f"{file.relative_to(root)}: missing section {link}")

    home = root / "README.md"
    home_links = pages.get(home, ([], set()))[0]
    for index in sorted((root / "projects").glob("*/README.md")):
        name = index.parent.name
        links = pages[index][0]
        if f"https://github.com/TF-Minecraft/{name}" not in links:
            errors.append(f"{index.relative_to(root)}: missing canonical source repository link")
        if "../../README.md" not in links:
            errors.append(f"{index.relative_to(root)}: missing All projects link")
        if f"projects/{name}/README.md" not in home_links:
            errors.append(f"README.md: missing project entry for {name}")
    return errors, checked, len(pages)


if __name__ == "__main__":
    errors, checked, pages = check(Path(__file__).resolve().parents[1])
    if errors:
        sys.exit("\n".join(errors))
    print(f"Verified {checked} local links and anchors in {pages} Markdown pages, plus project navigation")
