#!/usr/bin/env python3
"""Review package for a repository where nothing is committed -- the owner commits
after their own review pass, so a commit-range diff is unavailable. Scoping is by
PATH instead: pass the paths the task declared.

Emits into one file, for the given paths: a status summary, a real `git diff -U10`
for tracked modified files, and the FULL CONTENTS of untracked (new) files, which
`git diff` does not show at all. A reviewer reads the whole thing in one call.

Usage: python review-package.py OUTFILE PATH [PATH...]
"""

import os
import subprocess
import sys


def run_git(args, cwd=None, check=True):
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("usage: review-package.py OUTFILE PATH [PATH...]\n")
        return 2

    out_path = sys.argv[1]
    paths = sys.argv[2:]

    try:
        root_proc = run_git(["rev-parse", "--show-toplevel"])
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr.decode("utf-8", errors="replace"))
        return exc.returncode or 1

    root = root_proc.stdout.decode("utf-8", errors="replace").strip()

    status_proc = run_git(["-C", root, "status", "--porcelain", "--", *paths], check=False)
    status_text = status_proc.stdout.decode("utf-8", errors="replace")

    if not status_text.strip():
        sys.stderr.write(f"review-package: NO CHANGES under the given paths, in repo {root}\n")
        sys.stderr.write("review-package: nothing to review -- check the paths and the working directory\n")
        if os.path.exists(out_path):
            os.remove(out_path)
        return 1

    diffstat_proc = run_git(["-C", root, "diff", "--stat", "--", *paths], check=False)
    diffstat_text = diffstat_proc.stdout.decode("utf-8", errors="replace")

    diff_proc = run_git(["-C", root, "diff", "-U10", "--", *paths], check=False)
    diff_text = diff_proc.stdout.decode("utf-8", errors="replace")

    untracked_proc = run_git(
        ["-C", root, "ls-files", "--others", "--exclude-standard", "-z", "--", *paths],
        check=False,
    )
    untracked_paths = [
        p.decode("utf-8", errors="replace")
        for p in untracked_proc.stdout.split(b"\0")
        if p
    ]

    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    chunks = [
        "# Review package (working tree; nothing is committed -- the owner commits after review)\n\n",
        "## Status of the paths under review\n",
        status_text,
        "" if status_text.endswith("\n") else "\n",
        "\n## Diffstat (tracked files only)\n",
        diffstat_text,
        "" if (not diffstat_text or diffstat_text.endswith("\n")) else "\n",
        "\n## Diff of tracked, modified files (-U10)\n",
        diff_text,
        "" if (not diff_text or diff_text.endswith("\n")) else "\n",
        "\n## Full contents of NEW (untracked) files\n",
    ]

    for rel_path in untracked_paths:
        full_path = os.path.join(root, rel_path)
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
        except OSError as exc:
            content = f"<could not read file: {exc}>\n"
        chunks.append(f"\n### NEW FILE: {rel_path}\n```\n")
        chunks.append(content)
        if content and not content.endswith("\n"):
            chunks.append("\n")
        chunks.append("```\n")

    data = "".join(chunks).encode("utf-8")
    with open(out_path, "wb") as fh:
        fh.write(data)

    print(f"wrote {out_path}: {len(data)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
