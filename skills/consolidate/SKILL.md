---
name: consolidate
description: Use after lodestar:campaign, once its state is checkpointed; has the campaign's results reviewed cold and settles with the user whether they are ready to consolidate or need a chained campaign first, then takes the keep-or-discard ruling on each change and writes the spec that turns the kept ones into production code.
disable-model-invocation: false
---

# Consolidate

## Purpose

A campaign ends with its changes in the tree behind switches, a report that lists each change as a consolidation item with its evidence and a recommendation, and a set of rulings it took on the user's behalf. Consolidation turns that into production code. It has the campaign's results reviewed cold, takes the user's ruling on every item and every provisional ruling, and writes the spec that makes the kept items production code: switches removed or promoted to real options, interfaces cleaned, tests and documentation written, and the discarded items gone. It ends as `lodestar:design` does, with an approved spec and a recommendation of inline implementation or `lodestar:sdd`.

It runs in two stages. The first reviews the campaign's results and settles, with the user, whether they are ready to consolidate or raise a question that a chained campaign has to answer first. Only when they are ready does the second stage rule on the items and write the spec.

For work that came through a campaign, consolidation takes the place of design. The report is the settled intent, and the campaign's evidence stands in for design's investigation, so what is left to settle is which items to keep and what their production form is.

It is not a rewrite. Campaign code was written to the standard of the code around it so that consolidation has only to decide and to clean. Where an item's code needs more than interface cleanup before it can be kept, that is a finding about the campaign, and it goes to the user as one rather than being absorbed silently into the spec.

## Start

**Locate the campaign.** The report path is given, or found where the campaign skill's Layout puts reports (`${CLAUDE_PLUGIN_ROOT}/skills/campaign/SKILL.md`). From its header, take the charter, the ledger, and the starting commit.

**Check the checkpoint.** `git status --porcelain` must be empty, and `git log --format='%h %s' <starting commit>..HEAD` must show the campaign's code committed under the `exp:` prefix that `lodestar:commit-plan` gives a campaign. The checkpoint is HEAD: the campaign's close may span several commits -- its code under `exp:`, its records under the history's own prefixes -- and everything from the starting commit to HEAD is what consolidation decides on. If the tree is dirty, or no `exp:` commit is in the range, stop and ask the user to checkpoint first, with `/lodestar:commit-plan`; where the report's manifest is empty -- the campaign changed no code -- no `exp:` commit is expected. The checkpoint is what lets every review diff against a fixed state, lets a discarded item be removed by diff, keeps the experimental code in history for anyone reproducing the campaign's numbers, and lets `lodestar:sdd` start from the clean tree it requires. Name any commit in that range that touches files outside the manifest and the campaign's records (Layout, in the campaign skill), and ask whether it belongs.

**Follow the chain.** A report whose header names a campaign it continues is consolidated together with that one, and with whatever that one continues in turn. Give the whole chain the reading this skill gives one campaign: the range starts at the first campaign's starting commit, every report's items are presented, and where a later report covers an item an earlier one did, its recommendation supersedes. Consolidating one link alone would rule on code whose successors have since changed it. Every charter, report and ledger slot of the opening review takes each link's, in chain order; items are named `<report basename>:<item ID>`, since IDs repeat across links; and a ruling taken at an earlier link's readiness stage, which its successor's charter records, goes into the spec's Rulings section beside this session's.

**Check the ledger.** It is scratch, and exists only on the machine the campaign ran on. If it is absent, say so: the opening review then works from the report and the diff alone, and reports which checks that leaves it unable to make.

**Workspace.** `Temp/lodestar/<report-basename>/`, named after the report consolidation was invoked on, unless the project's instruction file (CLAUDE.md, AGENTS.md) designates another scratch area; it must be git-ignored (`git check-ignore <path>`). It holds the opening review's package and report, and `notes.md`: the dispatch answer, the readiness decision and every ruling, each verbatim and dated. They are kept there so they survive a compaction until the spec carries them into the tracked record.

**Ask the dispatch question** under Model selection in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/SKILL.md`, unless the invocation already answers it. This skill's roles map onto the question's: the opening review to the final-reviewer role, and the spec's cold review to the reviewer role. Record the answer in the workspace's `notes.md`.

Raise everything this section turns up in one message.

## Opening review

Dispatch one reviewer with the opening review block from `${CLAUDE_PLUGIN_ROOT}/skills/consolidate/reviewer-prompt.md`. It reads the charter, the report, the ledger and the checkpoint diff, inspects the code, and checks the results by reasoning. It runs nothing: no build, no test, no measurement.

This is not a repeat of the campaign's closing review, and the difference is who framed it. Every review inside the campaign saw a package the campaign's own orchestrator chose and built. This reviewer answers to no one who ran the campaign, and reads the record whole. What it is placed to catch is framing: a recommendation resting on a claim below the tier the report gives it, a provisional ruling presented as settled, two runs compared across code states, a mechanism the code does not implement, items that were only ever measured together. All of that is visible from the record by reading, so the review costs one dispatch rather than a measurement pass.

Build its package from the checkpoint: `git diff --stat <starting commit> HEAD` followed by `git diff -U10 <starting commit> HEAD`, written into one file in the workspace. Hand the reviewer the path; the package never enters your own context.

Where the review cannot settle something without running it, it names the run that would. Offer those runs to the user beside the items they bear on, and run one only if the user asks.

## Readiness

Before any item is ruled on, present the results in one message:

- **The answer** as the campaign reached it and as the opening review reads it: which conclusions the record supports, at which tier, and where the reviewer's reading differs from the report's.
- **The questions the results raise**: the report's parked questions and untested hypotheses, the questions the opening review raises, and the runs it named that reading cannot settle.
- **The readiness verdict**, the opening review's and your own: consolidate now, or continue with a chained campaign first -- and for the latter, the question that campaign would take.

The user decides. A campaign is ready when the items worth keeping stand on reviewed evidence and no open question could change which of them to keep. One whose result mostly raised a new question is not ready, however solid its numbers: consolidating first would rule on code the next campaign may yet change.

**Consolidate:** go on to Rulings.

**Chain:** stop here, and record the decision and the question in the workspace's `notes.md`. No item is ruled on now; the chain is consolidated as a whole when it ends (Follow the chain). Recommend `/lodestar:campaign` with no charter. Its charter starts from this checkpoint, names this report as the campaign it continues, and carries into its starting state, in substance, what the opening review found: the review's file is scratch, and the charter has to stand without it. A provisional ruling or parked question the user wants settled to steer the next campaign may be ruled on now, and enters that charter as a directive.

## Rulings

Present everything the user has to rule on in one numbered message:

- **Every consolidation item.** What it does, in a sentence the user can follow without the report open; the tier of the claims it rests on; the campaign's recommendation; the opening review's verdict, and its view where that differs from the campaign's; the items it was only ever measured together with; and the choice -- keep, keep with changes, discard, or defer. An item the user ordered kept during the campaign is presented as kept, for confirmation: its production form is still this session's to settle. A deferred item is removed with the discarded ones, and stays recoverable from the checkpoint; say so beside the choice.
- **Every provisional ruling**, to ratify or reject.
- **Every parked question and directive reading** the report lists.

Where keeping some items and not others would leave a combination the campaign never measured, say so beside the choice. The equivalence gate (The production design, below) will measure the kept set, but the user should know before ruling that its result is not yet in the record.

An item ruled "keep with changes" has its changes settled with the user now, so the spec states them as requirements rather than leaving them open for the implementation to decide.

Record every ruling verbatim and dated in the workspace's `notes.md` (Start); the spec's Rulings section carries them into the tracked record. If the answers raise follow-ups, batch those too.

## The production design

Work out the production form of the kept set, and present it in the conversation before writing anything, as `lodestar:design` does: wait for approval, and revise if the user asks.

- **Each kept item.** Where it lives, and what becomes of its switch: removed, with the behaviour always on; or promoted to a real option, with its name, its default and its validation. Its interface, cleaned to the codebase's conventions. What it merges with.
- **Each discarded or deferred item.** Its removal: every block, marker and file, found through the campaign's markers and the manifest. A discarded item leaves nothing behind. A deferred one leaves nothing behind either; the spec's Non-goals names the checkpoint commit it can be recovered from.
- **Instruments.** Removed, unless the user ruled one kept; a kept instrument is a feature, and is designed as one.
- **Residue.** No campaign marker survives in the source, and no switch survives that was not promoted.
- **The testing decision**, as in the Testing decision section of `${CLAUDE_PLUGIN_ROOT}/skills/design/SKILL.md`, with one criterion always among them: **the equivalence gate.** On the bar's inputs, the production code runs beside the checkpoint's configuration -- built from an export of the checkpoint (`git archive`), with exactly the kept switches on -- on one machine, and the two agree within the charter's scatter margin under its replication rule (two draws, or one where the charter established determinism), or, for a pass/fail criterion, both pass on every draw. Running the two side by side, rather than against the campaign's recorded number, keeps a difference of machine, build or date out of the verdict. Its failing configuration is the starting code, which the campaign's red run already records failing; it needs no re-run. Nothing else checks that the production form of an experiment still does what was measured: the interface cleanup changes code, the kept set may be a combination never measured together, and a test suite checks the behaviour it was written for, not the effect the campaign found. Where the kept set was never measured as a set, or rests on a result that reached only the reviewed tier, the prediction says so. Where nothing is kept, the gate reduces to identity: the production code reproduces the starting code.

The rest of design's discipline applies unchanged: cut what the goal does not need, design in units with clear interfaces, and flag gaps and simpler alternatives.

## The spec

Write it to `docs/lodestar/spec/YYYY-MM-DD-topic-consolidation-spec.md`, unless the project or the user states another location, following the Spec structure, Keeping it tight, and Self-review sections of `${CLAUDE_PLUGIN_ROOT}/skills/design/SKILL.md`, including the one cold review dispatch its self-review ends with. Two additions to that structure:

- The Context section also names the report and the charter by path, the starting commit, and the checkpoint commit.
- A ninth section, **Rulings**, after Non-goals, carries every ruling taken in this session, verbatim and dated, one entry per item and per provisional ruling. It is an enumerating section, so the word cap applies per entry: rulings are the one part of the spec that exists nowhere else, and a cap on the whole would force them into paraphrase. The Non-goals section lists the deferred items, each with the ruling that deferred it.

The report stays as the campaign left it: it records what the campaign found, and the spec records what was decided about it. Where the two disagree, the spec governs, and says why at the point where they differ.

Say, as design does, whether the work owes a standalone document. It usually owes the project's own documentation of the behaviour that now ships.

Then ask the user to review the file.

Never stage or commit anything. The project's rules govern committing.

## Terminal state

Where the readiness decision chose a chained campaign, the session has already ended there, with its recommendation of `lodestar:campaign`. Otherwise, end with a one-line recommendation, with the reason in the same line: inline implementation, or `lodestar:sdd` against the spec. Design's criteria for the choice apply, and so do the two obligations design's Terminal state attaches to the inline route. The equivalence gate is a measurement, output-heavy and the result every other task waits on, which usually tips the choice to sdd. Say that sdd starts from a clean tree, so the spec has to be committed before it runs.

Then stop. Do not invoke any other skill without the user's go-ahead.
