"""Regression tests for check-indexes.py."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("check_indexes", Path(__file__).with_name("check-indexes.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class LinkChecks(unittest.TestCase):
    def test_reference_links_and_nested_badge_links(self):
        links, _ = checker.parse_markdown("[manual][ref]\n\n[ref]: guide.md\n\n[![badge](badge.svg)](policy.md#rules)")
        self.assertEqual(links, ["guide.md", "policy.md#rules", "badge.svg"])

    def test_examples_in_code_are_not_links(self):
        links, _ = checker.parse_markdown("```md\n[example](missing.md)\n```\n\n`[example](missing.md)`")
        self.assertEqual(links, [])

    def test_duplicate_formatted_headings_and_html_anchors(self):
        _, anchors = checker.parse_markdown('# **Build** `JAR`\n\n# Build JAR\n\n<a id="custom"></a>')
        self.assertEqual(anchors, {"build-jar", "build-jar-1", "custom"})

    def test_nested_pages_anchors_spaces_and_case(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guides").mkdir()
            (root / "README.md").write_text("[good](guides/A%20Guide.md#setup)\n[bad](guides/a%20guide.md)")
            (root / "guides/A Guide.md").write_text("# Setup\n[broken section](#absent)\n[escape](../../outside.md)")
            errors, _, pages = checker.check(root)
            self.assertEqual(pages, 2)
            self.assertEqual(len(errors), 3)
            self.assertTrue(any("missing section #absent" in error for error in errors))

    def test_project_navigation_requires_both_directions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "projects/Example"
            project.mkdir(parents=True)
            (root / "README.md").write_text("# Projects")
            (project / "README.md").write_text("# Example")
            errors, _, _ = checker.check(root)
            self.assertEqual(len(errors), 3)
            (root / "README.md").write_text("[Example](projects/Example/README.md)")
            (project / "README.md").write_text("[Source](https://github.com/TF-Minecraft/Example) · [All projects](../../README.md)")
            self.assertEqual(checker.check(root)[0], [])


if __name__ == "__main__":
    unittest.main()
