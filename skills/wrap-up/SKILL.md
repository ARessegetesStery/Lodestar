---
name: wrap-up
description: Use at the end of a session, before the user reviews or commits, for a short reflective summary of open uncertainties, blind spots, unrequested changes, and the standing context a fresh session needs to review the work cold.
disable-model-invocation: false
---

# Wrap-up

## Purpose

A short report that closes out a session. It surfaces what a completion summary hides: what is still uncertain, what the user is not accounting for, and what changed without being asked for. It closes by handing all of that to a reader who was not here, since a run that finishes while the user is away is read the next morning by a fresh agent, and this file is what that agent has.

It is a complement, so it presumes its other half. Where no account of the work has been given -- what shipped, what was verified, and with what result -- give that first and this report after it. Delivered alone, a list of caveats leaves the reader assembling the thing being caveated, and a reader who cannot see the work reads an unqualified set of doubts as the whole of it.

This is a reflection, not a review. Do not re-derive the work, re-read the codebase, or diff the branch to find out what happened. Verifying the work is a separate job with separate instruments, and running it here turns a few seconds of reading into a full recheck. Fix nothing, start nothing, commit nothing.

## What to draw on

- **This session.** Sections 1 and 2 live here and nowhere else. No artifact records what you were unsure of, or what you noticed and did not raise.
- **The implementation log, where there is one.** If `lodestar:sdd` ran, read its ledger: `Temp/lodestar/<plan-basename>/progress.md`, unless the project's CLAUDE.md designates another scratch area, in which case it is under that. It holds what the conversation did not: deviations from the plan, decisions taken mid-task, findings deferred as minor, findings parked with a ruling, and the implementers' own stated concerns. Those are known-unresolved items the user has not been told about, which makes them sections 1 and 2 already written down.
- **Project memory**, for standing obligations this session's work touches.
- **Optionally `git status --porcelain`**, as a cross-check on section 3 and as the file list for section 5, with `git branch --show-current` for its branch name. Both are cheap -- a one-line-per-file list and a name, not a diff. Never `git diff`.

Section 3 depends least on memory and most on having noticed at the time. A side-change goes unreported because it was never registered as a change, so give it a deliberate pass rather than a recollection.

Section 5 is assembled from what you already hold -- the ledger's completion lines, the verification output already reported, the paths this session worked in, and what the conversation settled -- and not by reconstructing state from the repository. A cold session can read every file you would re-read; what it cannot recover is which written thing was verified and which was merely written, what was decided out loud, and what the run reported into a conversation that no longer exists.

## The report

Five sections, in this order:

**1. Unsure about** -- uncertainty inside the work delivered. Assumptions made without confirmation, paths written but not exercised, places where a plausible alternative reading of the request exists.

**2. You may be overlooking** -- consequences outside the work delivered. Downstream effects, decisions now pending, facts about the surrounding system that the user's current direction does not account for.

**3. Not explicitly asked for** -- changes made on your own initiative. Files touched beyond the stated scope, refactors folded into a task, dependencies added, defaults chosen where the request was silent.

**4. User-side action/verification** -- what the user must do to verify what this session implemented. Where the work produced a separate acceptance procedure, which contains the ordered steps someone follows to decide whether the work is done, name it by path and give its first step as a single item. Do not reproduce the full procedure here: it would spend the cap below on steps the reader cannot follow to the end, and they would open the document anyway.

**5. Picking this up cold** -- what a fresh agent needs in order to discuss this work with the user in a session holding none of this one's context. Four labelled entries, in this order:

- **What shipped.** The delivered work in a few lines, what verification returned -- the counts and measurements themselves, not a verdict on them -- and which reviews ran with what they concluded.
- **Where it lives.** The branch, what is committed and what is only in the working tree, and the changed files by path. Then the documents in reading order: the spec or plan the work ran from, and this report. Mark a scratch path for what it is.
- **Decisions.** The rulings this session took, each with its one-line reason. Weight the ones the user made in conversation, which exist in no file, and the ones taken mid-run against a finding: what was deferred, what was parked, and on what ground.
- **Where it stands.** What is done and verified, held apart from what is written but unexercised and what was never started. Close on what the work is waiting on, phrased as the user's next decision rather than an instruction to carry out.

**What shipped** looks like a repetition of the account this report is the complement of, and in the conversation it is one. In the file it is the only copy. A run that finished while the user was asleep gave that account to a conversation nobody returns to -- stale, out of cache, and expensive to reload for what is usually one question -- so the file is where the next session starts, and a file opening with three sections of caveats and no statement of what was done makes its reader rebuild the work from a diff before it can read a word of the report. Keep it to the ledger's own completion lines and the verification numbers already reported. This is carrying a small thing forward, not re-deriving it.

Separate what will still be there from what may not. The spec, the plan, and this report are in the repository. An `sdd` workspace under the scratch area is gitignored, local to one machine, and moved aside the moment the same plan runs again, so name it as a bonus rather than a dependency -- and where a claim in this report rests on something inside it, put the substance of the claim in the report rather than a path to where it was found.

This is a briefing, not a dispatch prompt. Its reader is most likely about to go through an uncommitted working tree with the user and answer questions about it, not to resume implementation, so name what the work is waiting on and stop there. Where the work does continue under another agent, close the section with a line recommending `lodestar:handoff`, which produces the self-contained prompt -- scope, non-goals, constraints, verification commands, reporting expectations -- that this section is deliberately not. Writing that prompt out here trades a report the user can read in a minute for a second copy of a document `handoff` already owns, and the two then drift.

## Shape

Sections 1 through 4:

- Each holds at most three items, and the cap governs these sections rather than whatever report precedes them. Zero is a valid count, one is a finished section, and `None` is complete.
- Most consequential first.
- Name the work by what it is, not by its label elsewhere: "the retry path in the uploader" rather than "Task 4", "resuming an upload after a dropped connection" rather than "the third requirement". The reader has not read the spec or the plan.
- Where more than three real items exist, give the three that matter most and close the section with a line saying how many were left out and where they are recorded. A cap that truncates silently reads exactly like having little to report.
- One line per item. No sub-bullets, no follow-on sentences.

Section 5 is the four labelled entries, in the order given, and it is the long part of this report. Expect it to run about as long as sections 1 through 4 together, often longer. That is the right shape and not a lapse of restraint: those four are capped at what a reader can act on in one sitting, this one is sized by what a cold session cannot work without, and the two are different quantities -- a session left to guess at a branch name or at a decision already settled costs more than the line would have.

What shipped and Where it stands run to a few lines each; Where it lives and Decisions run to as many lines as there are real paths and real rulings. Enumeration is what earns the length -- one more path, one more ruling, one more file. Prose is not: elaborating an entry, restating a section above, or arguing a decision past its one line. Where the decisions run past what a reader will hold, give the ones a cold session could get wrong and name where the rest are recorded.

Name the file, path, or command wherever one applies.

Report only what is true, then stop -- the user will ask if they want more on any of it.

## Delivery

Report in the conversation. Where the invoker names a destination file, write the report there as well, opening with a line naming what it closes out and the absolute date.

Where the user is not present to read the report as it is given, the conversation is the wrong medium for sections 1 and 2 -- the only part of it that cannot be produced again.

Write section 5 for the file, whichever medium the report lands in, and write it in full there even where the conversation has just covered the same ground. The test is whether a session that has read nothing else could open this file and discuss the work with the user: no conversation shorthand, absolute dates rather than "today" or "last session", everything named by path, and names to search for rather than line numbers, which decay fastest in exactly the files this work just changed.

A written report is the same report. The item cap is about what a reader can act on, not about what fits, and a file offers exactly the room the cap exists to refuse. Where a report already exists at that path, append a new dated one below it rather than overwriting -- a resumed or re-run job does not resolve the earlier run's uncertainties, and its section 5 is the state the next run starts from.
