#!/usr/bin/env python3
"""Fail the build when the shipped surface changed without a version bump,
or when the version's three copies disagree."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

CLAUDE_MANIFEST = ".claude-plugin/plugin.json"
CODEX_MANIFEST = ".codex-plugin/plugin.json"
README = "README.md"

PRODUCT_SURFACE_PREFIXES = (
    "skills/",
    "commands/",
    ".claude-plugin/",
    ".codex-plugin/",
)

BADGE_PATTERN = re.compile(r"badge/release-v(\d+\.\d+\.\d+)-")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


class VersionProblem(Exception):
    pass


def read_manifest_version(repo_root, relative_path):
    path = repo_root / relative_path
    if not path.is_file():
        raise VersionProblem(f"{relative_path} is missing — every host manifest must ship a version")
    try:
        version = json.loads(path.read_text(encoding="utf-8"))["version"]
    except (json.JSONDecodeError, KeyError) as exc:
        raise VersionProblem(f"{relative_path} has no readable `version` field ({exc})") from exc
    if not SEMVER_PATTERN.match(str(version)):
        raise VersionProblem(f"{relative_path} version {version!r} is not MAJOR.MINOR.PATCH")
    return str(version)


def read_readme_badge_version(repo_root):
    path = repo_root / README
    if not path.is_file():
        raise VersionProblem(f"{README} is missing")
    match = BADGE_PATTERN.search(path.read_text(encoding="utf-8"))
    if not match:
        raise VersionProblem(
            f"{README} has no `release-vX.Y.Z` badge — the badge is one of the version's copies "
            "and must stay present so it can be checked"
        )
    return match.group(1)


def collect_version_copies(repo_root):
    return {
        CLAUDE_MANIFEST: read_manifest_version(repo_root, CLAUDE_MANIFEST),
        CODEX_MANIFEST: read_manifest_version(repo_root, CODEX_MANIFEST),
        README: read_readme_badge_version(repo_root),
    }


def assert_copies_agree(copies):
    distinct = set(copies.values())
    if len(distinct) > 1:
        lines = [f"  {location} → {version}" for location, version in copies.items()]
        raise VersionProblem(
            "version copies disagree — one fact, three places, all must match:\n" + "\n".join(lines)
        )
    return distinct.pop()


def git_output(repo_root, *args):
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def base_version(repo_root, base_ref):
    blob = git_output(repo_root, "show", f"{base_ref}:{CLAUDE_MANIFEST}")
    if blob is None:
        return None
    try:
        return str(json.loads(blob)["version"])
    except (json.JSONDecodeError, KeyError):
        return None


def changed_files(repo_root, base_ref):
    committed = git_output(repo_root, "diff", "--name-only", f"{base_ref}...HEAD")
    if committed is None:
        return None
    uncommitted = git_output(repo_root, "status", "--porcelain", "--untracked-files=all") or ""
    names = set(filter(None, committed.splitlines()))
    for line in uncommitted.splitlines():
        entry = line[3:].strip()
        if entry:
            names.add(entry.split(" -> ")[-1])
    return sorted(names)


def product_surface_changes(names):
    return [name for name in names if name.startswith(PRODUCT_SURFACE_PREFIXES)]


def as_tuple(version):
    return tuple(int(part) for part in version.split("."))


def assert_bump(repo_root, base_ref, current):
    previous = base_version(repo_root, base_ref)
    names = changed_files(repo_root, base_ref)
    if previous is None or names is None:
        print(f"bump check skipped — base ref {base_ref!r} is unreachable from here")
        return

    touched = product_surface_changes(names)
    if not touched:
        print(f"bump check passed — no shipped-surface change against {base_ref}")
        return

    listing = "\n".join(f"  {name}" for name in touched)
    if current == previous:
        raise VersionProblem(
            f"shipped surface changed but version stayed {current} — hosts key their update check "
            f"on this number, so an unchanged version ships stale content to everyone who already "
            f"installed it.\nchanged:\n{listing}"
        )
    if as_tuple(current) < as_tuple(previous):
        raise VersionProblem(
            f"version moved backward: {previous} → {current}.\nchanged:\n{listing}"
        )
    print(f"bump check passed — {previous} → {current} for {len(touched)} shipped file(s)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--skip-bump-check", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    try:
        copies = collect_version_copies(repo_root)
        current = assert_copies_agree(copies)
        print(f"version copies agree — {current}")
        if not args.skip_bump_check:
            assert_bump(repo_root, args.base_ref, current)
    except VersionProblem as problem:
        print(f"release guard failed: {problem}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
