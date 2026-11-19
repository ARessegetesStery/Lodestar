#!/usr/bin/env python3
"""Extract one task's full text from a plan into its own file, so a dispatched
implementer reads only its own task and never the whole plan.

Matches a heading of the form `### Task N:` and stops at the next `### Task `
or at the end of the file.

Usage: python task-brief.py PLAN_FILE N OUTFILE
"""

import os
import sys


def main():
    if len(sys.argv) != 4:
        sys.stderr.write("usage: task-brief.py PLAN_FILE N OUTFILE\n")
        return 2

    plan_path, task_num, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    if not os.path.isfile(plan_path):
        sys.stderr.write(f"task-brief: no such plan file: {plan_path}\n")
        return 1

    target_prefix = f"### Task {task_num}:"
    extracted = []
    inside = False

    with open(plan_path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith(target_prefix):
                inside = True
                extracted.append(line)
                continue
            if inside and line.startswith("### Task "):
                break
            if inside:
                extracted.append(line)

    if not extracted:
        sys.stderr.write(f"task-brief: no '### Task {task_num}:' heading found in {plan_path}\n")
        if os.path.exists(out_path):
            os.remove(out_path)
        return 1

    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.writelines(extracted)

    print(f"wrote {out_path}: {len(extracted)} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
