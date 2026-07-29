---
name: wrap-up
description: Use at the end of a session, before the user reviews or commits, for a short reflective summary of open uncertainties, blind spots, and unrequested changes.
disable-model-invocation: true
---

# Wrap-up

## Purpose

A short report that closes out a session. It surfaces what a completion summary hides: what is still uncertain, what the user is not accounting for, and what changed without being asked for.

This is a reflection, not a review. Do not re-derive the work, re-read the codebase, or diff the branch to find out what happened. Verifying the work is a separate job with separate instruments, and running it here turns a few seconds of reading into a full recheck. Fix nothing, start nothing, commit nothing.

## What to draw on

- **This session.** Sections 1 and 2 live here and nowhere else. No artifact records what you were unsure of, or what you noticed and did not raise.
- **The implementation log, where there is one.** If `lodestar:sdd` ran, read its ledger: `Temp/lodestar/<plan-basename>/progress.md`, unless the project's CLAUDE.md designates another scratch area, in which case it is under that. It holds what the conversation did not: deviations from the plan, decisions taken mid-task, findings deferred as minor, findings parked with a ruling, and the implementers' own stated concerns. Those are known-unresolved items the user has not been told about, which makes them sections 1 and 2 already written down.
- **Project memory**, for standing obligations this session's work touches.
- **Optionally `git status --porcelain`**, as a cross-check on section 3 only. It is a one-line-per-file list, not a diff. Reach for it when the session touched more than you can hold in mind. Never `git diff`.

Section 3 depends least on memory and most on having noticed at the time. A side-change goes unreported because it was never registered as a change, so give it a deliberate pass rather than a recollection.

## The report

Three sections, in this order:

**1. Unsure about** -- uncertainty inside the work delivered. Assumptions made without confirmation, paths written but not exercised, places where a plausible alternative reading of the request exists.

**2. You may be overlooking** -- consequences outside the work delivered. Downstream effects, decisions now pending, facts about the surrounding system that the user's current direction does not account for.

**3. Not explicitly asked for** -- changes made on your own initiative. Files touched beyond the stated scope, refactors folded into a task, dependencies added, defaults chosen where the request was silent.

## Shape

- Each section holds at most three items. Zero is a valid count, and `None` is a complete section.
- Most consequential first.
- Where more than three real items exist, give the three that matter most and close the section with a line saying how many were left out and where they are recorded. A cap that truncates silently reads exactly like having little to report.
- One line per item. No sub-bullets, no follow-on sentences.
- Name the file, path, or command wherever one applies.

Report only what is true. A section with one real item is finished at one item. Then stop -- the user will ask if they want more on any of it.

## Delivery

Report in the conversation. Where the invoker names a destination file, write the report there as well, opening with a line naming what it closes out and the absolute date.

Sections 1 and 2 cannot be reconstructed later, so where the user is not present to read the report as it is given, the conversation is the wrong medium for the only part of it that cannot be produced again.

A written report is the same report. The three-item cap is about what a reader can act on, not about what fits, and a file offers exactly the room the cap exists to refuse. Where a report already exists at that path, append a new dated one below it rather than overwriting -- a resumed or re-run job does not resolve the earlier run's uncertainties.
