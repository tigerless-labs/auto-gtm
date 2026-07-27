import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "check_release_version.py"

README_TEMPLATE = """<h1 align="center">auto-gtm</h1>

<p align="center">
  <img src="https://img.shields.io/badge/release-v{version}-brightgreen.svg" alt="release" />
</p>

body text
"""


def write_repo(root, version, claude_version=None, codex_version=None, readme_version=None):
    (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (root / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    (root / "skills" / "demo").mkdir(parents=True, exist_ok=True)
    (root / "docs").mkdir(parents=True, exist_ok=True)

    (root / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "auto-gtm", "version": claude_version or version}) + "\n"
    )
    (root / ".codex-plugin" / "plugin.json").write_text(
        json.dumps({"name": "auto-gtm", "version": codex_version or version}) + "\n"
    )
    (root / "README.md").write_text(README_TEMPLATE.format(version=readme_version or version))
    (root / "skills" / "demo" / "SKILL.md").write_text("# demo\n")
    (root / "docs" / "note.md").write_text("note\n")


def git(root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=True,
        env={
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@example.com",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@example.com",
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "HOME": str(root),
        },
    )


def init_repo(root, version):
    write_repo(root, version)
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")


def run(root, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(root), *args],
        capture_output=True,
        text=True,
    )


class VersionConsistency(unittest.TestCase):
    def test_all_three_copies_agree_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_repo(root, "0.3.0")
            r = run(root, "--skip-bump-check")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_readme_badge_lagging_fails_and_names_every_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_repo(root, "0.3.0", readme_version="0.2.23")
            r = run(root, "--skip-bump-check")
            self.assertEqual(r.returncode, 1)
            out = r.stdout + r.stderr
            self.assertIn("README.md", out)
            self.assertIn("0.2.23", out)
            self.assertIn("0.3.0", out)

    def test_codex_manifest_out_of_sync_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_repo(root, "0.3.0", codex_version="0.2.24")
            r = run(root, "--skip-bump-check")
            self.assertEqual(r.returncode, 1)
            self.assertIn(".codex-plugin", r.stdout + r.stderr)

    def test_missing_badge_fails_rather_than_passing_silently(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_repo(root, "0.3.0")
            (root / "README.md").write_text("no badge here\n")
            r = run(root, "--skip-bump-check")
            self.assertEqual(r.returncode, 1)
            self.assertIn("README.md", r.stdout + r.stderr)

    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            write_repo(root, "0.3.0")
            (root / ".codex-plugin" / "plugin.json").unlink()
            r = run(root, "--skip-bump-check")
            self.assertEqual(r.returncode, 1)


class BumpRequirement(unittest.TestCase):
    def test_product_surface_change_without_bump_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            init_repo(root, "0.3.0")
            (root / "skills" / "demo" / "SKILL.md").write_text("# demo changed\n")
            r = run(root, "--base-ref", "main")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            out = r.stdout + r.stderr
            self.assertIn("skills/demo/SKILL.md", out)

    def test_product_surface_change_with_bump_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            init_repo(root, "0.3.0")
            (root / "skills" / "demo" / "SKILL.md").write_text("# demo changed\n")
            write_repo(root, "0.3.1")
            (root / "skills" / "demo" / "SKILL.md").write_text("# demo changed\n")
            r = run(root, "--base-ref", "main")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_docs_only_change_needs_no_bump(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            init_repo(root, "0.3.0")
            (root / "docs" / "note.md").write_text("note changed\n")
            r = run(root, "--base-ref", "main")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_command_change_requires_bump(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            init_repo(root, "0.3.0")
            (root / "commands").mkdir()
            (root / "commands" / "start.md").write_text("start\n")
            r = run(root, "--base-ref", "main")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("commands/start.md", r.stdout + r.stderr)

    def test_version_must_move_forward_not_backward(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            init_repo(root, "0.3.0")
            (root / "skills" / "demo" / "SKILL.md").write_text("# demo changed\n")
            write_repo(root, "0.2.9")
            (root / "skills" / "demo" / "SKILL.md").write_text("# demo changed\n")
            r = run(root, "--base-ref", "main")
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            out = r.stdout + r.stderr
            self.assertIn("0.2.9", out)
            self.assertIn("0.3.0", out)

    def test_unreachable_base_skips_bump_check_without_failing(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            init_repo(root, "0.3.0")
            r = run(root, "--base-ref", "origin/does-not-exist")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("skip", (r.stdout + r.stderr).lower())


if __name__ == "__main__":
    unittest.main()
