#!/usr/bin/env python3
"""Check that relative links in the documentation entry points exist."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
indexes = [root / "README.md", root / "MAINTAINING.md", root / "PIPELINES.md"]
indexes.extend(sorted((root / "projects").glob("*/README.md")))
errors = []
checked = 0
for index in indexes:
    for match in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", index.read_text()):
        target = urlsplit(match[1].strip("<>"))
        if target.scheme or target.netloc or not target.path:
            continue
        path = (index.parent / unquote(target.path)).resolve()
        checked += 1
        if not path.is_relative_to(root) or not path.exists():
            errors.append(f"{index.relative_to(root)}: missing local link {match[1]}")
if errors:
    sys.exit("\n".join(errors))
print(f"Verified {checked} relative links in {len(indexes)} documentation indexes")
