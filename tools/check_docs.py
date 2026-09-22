#!/usr/bin/env python3
"""Check repository-local Markdown destinations."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT = Path(__file__).resolve().parents[1]
errors = []
links = 0
for page in ROOT.rglob('*.md'):
    text = page.read_text()
    text = re.sub(r'^```[^\n]*\n.*?^```[^\n]*$|^~~~[^\n]*\n.*?^~~~[^\n]*$', '', text, flags=re.M | re.S)
    urls = re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)\)', text)
    urls += re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', text, flags=re.M)
    urls += re.findall(r'(?:src|href)=["\x27]([^"\x27]+)["\x27]', text)
    for url in urls:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        target = (page.parent / unquote(parts.path)).resolve()
        links += 1
        if not target.is_relative_to(ROOT) or not target.exists():
            errors.append(f'{page.relative_to(ROOT)}: missing {url}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Checked {links} local links.')
