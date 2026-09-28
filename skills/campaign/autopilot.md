# Campaign: autopilot phase

This file holds the autopilot phase of `lodestar:campaign`, read when the skill is invoked with a charter. It relies on `SKILL.md` beside it for the claim tiers, the decision rules and the layout, which the charter sets and consolidation relies on as well.

The user is present when the autopilot starts and very likely absent from then on. Everything that needs them is asked in one message at the start; after that, the run does not stop to ask.

## Start

Before anything is dispatched, check and ask, in one message:

- **The dispatch question** under Model selection in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/SKILL.md`, unless the invocation already answers it. This skill's roles map onto the question's: implementers to the implementer role; implementation reviews, numbers reviews and every re-review to the reviewer role; the closing review to the final-reviewer role.
- **The baseline.** `git status --porcelain` shows nothing but the charter itself, and HEAD is the commit the charter's Starting state names, or a later one whose only change since is the charter (Setup says why). If not, say what is outstanding.
- **The workspace.** It is git-ignored (`git check-ignore <path>`). If not, settle its location.
- **The pre-flight scan.** Read the charter once for anything that cannot be run as written: a bar with no inputs, contradictory moves, a run protocol that names something absent, a budget that cannot hold its own closing reservation. Put each finding beside the charter text it concerns and ask how it resolves. If the scan is clean, say nothing about it.

Wait for the answer. A resolution that changes the charter is appended to its Amendments section. Then run unattended to the end. A resume replaces this message with the resume check under Resuming.

## Setup

In this order, so that every run setup makes is inside the budget and in the registry.

**Workspace.** At its Layout location (`SKILL.md`). Everything for the run lives here: the ledger, the operating rules, briefs, implementer reports, review packages, snapshots, code states, analysis scripts and raw run output.

**Clock.** Read the time with `date`, and record the start, the deadline, and the closing time -- the deadline less the closing reservation -- in the ledger created next. Every later timestamp comes from `date` as well. Estimated times drift by hours over a long run, and the closing pass is the part that pays for the drift.

**Ledger.** Create `<workspace>/ledger.md` from `${CLAUDE_PLUGIN_ROOT}/skills/campaign/ledger-skeleton.md` (The ledger, below), with the charter path on its first line, and the dispatch answer, the start-message resolutions and the clock in its standing section.

**Baseline.** The campaign's changes are what consolidation later rules on, change by change, so they must be the only difference between the starting commit and the checkpoint the user commits at the end. Work already uncommitted when the run starts would be indistinguishable from the campaign's own, and would reach consolidation as changes nobody made and nobody measured; the charter is exempt only because it is the campaign's own record. Record HEAD at this point as the starting commit: every later diff, the identity check and the checkpoint are measured from it.

**Starting code.** Keep, in the workspace, a copy of what the starting commit runs as: its build, or where the project builds nothing, the code itself, exported with `git archive <starting commit>`. Once the first experiment lands, the starting code no longer exists in the working tree, and the red run and every identity check need it. No state-mutating git is needed to get it.

**Noise.** Run the starting code twice, in the identity check's configuration, and record everything that differs between the two runs; do the same with the test suite where its counts depend on data. That residual is what the identity check and the suite comparison accept later. Without it, run-to-run variation reads as a switch leaking into the off path.

**References.** Re-measure every reference number the bar compares against, on this machine and from the starting code. A reference imported from another machine, build or date is a different measurement, and a comparison against it measures the difference between environments as much as the experiment.

**Operating rules.** Assemble `<workspace>/operating-rules.md` as `lodestar:sdd` does under Setup, with the charter's run protocol beside the project's own rules, and three requirements added to the report contract for experiment work: the report names the experiment's switch; it states whether the switched-off path is identical to the starting code, and how that was established; and it proposes the manifest entry for its change, which the controller enters in the ledger. It is pasted into every implementer dispatch and kept live, as sdd's is.

**Suite baseline.** Where the project has a test suite, run it once on the starting code, with the command the charter names, and record the counts. The closing pass runs it again on the final code, and a failure that was already present at the start is otherwise indistinguishable from one the campaign caused.

**The red run.** Before the first experiment, run the bar on the configuration the charter predicts fails, and record the result against the prediction. It shows the bar can fail; it checks that the instruments work before anything depends on them; and it measures the cost of one run, which is what the closing reservation was sized from. If a run costs more than the charter assumed, move the closing time earlier to keep the reservation whole. The autopilot may move the closing time earlier, never later: a later closing time is a budget extension, which is the user's.

If the red run passes, the bar cannot fail as written, and changing the bar is the user's. Park that as a question on the bar (Decisions, in `SKILL.md`), and carry on only with work that does not depend on the bar's verdict -- instruments, and mechanism probes whose readings stand on their own -- and the report leads with it. Where one run of the bar is short, run the red run before sending the start message instead, once the baseline and workspace checks pass, with its output in the workspace and its registry row written when the ledger is created: a bar unable to fail then reaches the user while they are still present to change it.

## The ledger

The ledger is the run's recovery map and its record. Conversation memory does not survive compaction, and a controller that has lost its place redoes work, or builds on work it has forgotten was retracted. After a compaction, trust the ledger over recollection, and re-read this file and the operating rules: a compaction keeps them only as a summary, and the summary drops the rules that bind least often, which are the ones a long run eventually needs. The standing section carries a one-line current status, updated in place -- what is running, what is next, the newest result -- so that the user, arriving mid-run, can see where the run stands without reading the log.

It is also the main input of the reviewer who reads this campaign cold during consolidation, and its length is not a cost to minimize. An entry that says what was done without the code state, the inputs, the command, the output path and the numbers is an entry that reviewer cannot check. Every entry follows the rule for campaign files (Layout, in `SKILL.md`).

It has two kinds of section, and the difference is what keeps a long ledger navigable:

- **State sections** -- the standing section, the manifest, the claims, provisional rulings, parked questions, the hypothesis queue and the run registry -- hold the current state, and are updated in place.
- **The log** is append-only and dated. Every change to a state section happens through a log entry saying what changed and why, so the state can always be reconstructed from the log. An earlier entry is never edited: a correction is a new entry naming the one it corrects.

The skeleton at `${CLAUDE_PLUGIN_ROOT}/skills/campaign/ledger-skeleton.md` lays these out, with a heading form that lets a reader grep one entry out of a long file. When consulting the ledger mid-run, grep for the heading you need and read that slice, rather than re-reading the whole file.

## Experiments

**Written to be kept.** Every change the campaign makes to tracked code meets the standard of the code around it: its naming, its structure, its commenting, and its tests where the project tests that area. Consolidation decides what to keep and cleans interfaces -- removing switches, turning a kept switch into a real option, merging variants -- and that should be all it has to do. There is no final cleanup pass in a campaign, because code that would need one is code whose kept form was never the code measured.

**Gated.** Every experimental change sits behind a switch, off by default, and with every switch off the code behaves exactly as the starting commit does. Use the mechanism the charter names; where it names none, use the lightest one the project already has -- an environment variable read once, a compile-time definition -- and add no configuration surface unless the charter permits it: a configuration key is a schema decision, and schema decisions belong to consolidation. A change the charter or the user orders kept outright is the exception: it goes in unswitched, and it moves the baseline. Record it as a charter amendment, and from then on take the starting-code copy, the identity check, the noise and reference runs and the red run against the starting code plus that change. References measured before it are stale either way; re-basing says so, where a switch left on would hide it and leave consolidation one more switch to remove.

**Marked.** Every experimental block carries a comment naming the campaign and its switch, and every instrument a marker of its own. Consolidation finds every block by searching for the markers; a block without one is a change nobody can find to decide on.

**Identity.** After the first experiment lands, and again in the closing pass, show that the switched-off code reproduces the starting code -- re-based on any ordered-kept change (Gated): a short run of the starting code kept in the workspace and of the current code, every switch off, compared on everything but timing and the residual Setup's noise runs recorded, under whatever controls the run protocol names for making runs repeatable. A switch that leaks into the off path contaminates every comparison against the starting code. A failed identity check is therefore a Critical gating finding: it is fixed through the implementation review and the check re-run, and every claim measured on the leaking code drops to observation until it is re-measured.

**The manifest.** The manifest section of the ledger lists every change to tracked code: an ID; the switch, or `unswitched`; the files; what the change does, in a sentence; the experiment it belongs to; its status -- active, abandoned (switched off, recommended for removal), instrument, or ordered kept (unswitched by order of the charter or the user, who is named); and its known issues, the review findings consolidation will have to fix. It is consolidation's unit of decision. The checkpoint diff shows what changed, but not which edits belong together, nor which claim each keep-or-discard rests on.

**Code records.** Nothing is committed during the run, so the workspace keeps what a reviewer needs to see the exact code any run used. Each experiment takes the ID of its item in the hypothesis queue, and its records are named by it: its implementer report at `<workspace>/reports/<experiment ID>.md`, its review packages, and its snapshots. Before an experiment changes a file, copy the file to `<workspace>/snapshots/<experiment ID>/<repo-relative path>`; the experiment's own diff is then `git diff --no-index -U10` of the snapshot against the file, which its review needs, since a file in a campaign carries several experiments at once. Before each build, or each run where the project builds nothing, save `review-package` over the whole tree (`.`) to `<workspace>/states/<label>.md`. Each run then executes a frozen copy of its code state, kept in the workspace, so that nothing changed later can alter what a running or finished run executed, or what a re-run of it executes: where the project builds, the build, identified by a hash of the artifact; where it builds nothing, the starting-code export with that state's changes applied. A run's code state is the state file, the build configuration and the artifact hash, plus its switch settings -- or simply the starting commit before the first change. A change made only at build level, such as a compiler flag or a build option, leaves the tree diff untouched; it is an experiment with a manifest entry like any other.

Probes and analysis scripts live in the workspace. A script whose output the report cites is copied to wherever the project keeps such scripts, and cited there, because the workspace does not survive.

## The loop

The plan is a queue of hypotheses, re-planned after every result, not a list of tasks fixed in advance. Each iteration:

1. **Choose.** Take the next item from the queue, and say in the log why this one. The reasoning path between experiments is part of what the consolidation reviewer checks.
2. **Brief.** Before anything runs, append a brief entry: the hypothesis; the change, if any, and its switch; the measurement, on which inputs; the prediction, with a number or the exact observation expected; the result that would falsify it; which claims it would move; and the expected cost. A prediction written after the result cannot be wrong, so it cannot inform.
3. **Implement.** Bounded work whose context you already hold goes inline. Output-heavy, independent or parallelizable work is dispatched, with the operating rules pasted and the brief entry as the requirements. Name the model on every dispatch, per the start answer. Route an implementer's status as sdd does, with two differences for a run nobody is watching: a BLOCKED on a decision outside the charter's scope is parked (Decisions, in `SKILL.md`), and any other BLOCKED re-plans or drops the experiment, or re-dispatches on a more capable model where the dispatch answer leaves one. Nothing escalates to the user mid-run.
4. **Review the implementation** before any of its results rise above observation (Reviews, below).
5. **Run**, under the charter's run protocol. Register every run: label, timestamp, code state (Experiments), inputs, command, output path, exit status, wall time, and anything anomalous.
6. **Read.** Record the result against the prediction. A result that contradicts its prediction is the most informative event a campaign has: explain it in the next entry, before anything is built on top of it. Update the claims, and re-plan the queue.

**Spend measurement in proportion to confidence.** Offline probes and short runs to form and kill hypotheses; full-length runs to confirm one. A long run spent on an idea a short probe would have killed is budget the closing pass loses.

Within the charter's concurrency limits, run independent lanes side by side -- one experiment's runs while another's code is written or reviewed -- but never let two writers hold one file, and never put other work beside a run the run protocol says must run alone.

**Time limits.** Every run and every dispatched agent has a time limit, written in its registry row or its brief, and taken from the charter's run protocol where it sets one. At expiry, look at what the process is actually doing, not merely whether it is alive -- an idle process looks the same as a busy one to a liveness check -- then stop it and record what was found. A run that silently waits costs the budget the closing pass needs.

**Background tasks.** Every waiter, queue or watchdog the controller starts is registered in the ledger's standing section with what it waits for, and struck when it ends. Before starting or re-arming one, or re-dispatching on a notification, confirm from the process state that the previous one is gone and that its work did not in fact complete: a notification can be interim, and a re-armed waiter duplicates the queue it watches.

## Reviews

Three review blocks live in `${CLAUDE_PLUGIN_ROOT}/skills/campaign/reviewer-prompt.md`. Every reviewer is a fresh subagent, read-only on what it reviews; name its model per the start answer.

- **Implementation review**, after every experimental change -- or once over several landed together -- and before its results rise above observation. Build the package with `bash "${CLAUDE_PLUGIN_ROOT}/skills/sdd/scripts/review-package" OUTFILE PATH [PATH...]` over the experiment's files, run from the project's root, and append the snapshot diff of each file; a file the experiment created has no snapshot, and the package shows it whole. It returns the two verdicts sdd's task review does, correctness and quality, and holds quality to the surrounding code's standard, since the code may be kept as written.

  Critical and Important findings are fixed by the implementer, or inline by the controller where the fix is bounded, then re-reviewed on the findings alone, as `reviewer-prompt.md` describes. After two fix rounds, stop the fix loop. A correctness or gating finding still open makes the experiment's results ineligible for any tier above observation, which the log records, and the experiment is re-planned or dropped. A quality finding still open does not touch the evidence: it is recorded as a known issue on the manifest entry, and so is every Minor, since there is no cleanup pass to catch them later and consolidation is where they get fixed. A campaign does not need every experiment's code perfected to proceed, but it must know which of its evidence stands on code nobody has vouched for.
- **Numbers review**, to promote a claim to reviewed. Review a claim when it is about to be used for something only a reviewed claim may ground, not every observation as it lands, and batch claims that share runs. Each verdict is a claim entry in the log. SUPPORTED promotes the claim; SUPPORTED WITH CORRECTIONS promotes it in its corrected wording; NOT SUPPORTED leaves it at its tier, or demotes or retracts it where the numbers contradict it, with the retraction propagating as Claim tiers (`SKILL.md`) requires.
- **Closing review**, once, in the closing pass.

A reviewer's re-run is a run like any other, scheduled within the concurrency limits and registered. Where the charter's run protocol does not let reviewers launch it, the controller launches it in a slot the protocol allows -- between timed runs, for instance -- and hands the reviewer the output to compare. Where no such slot fits the budget, the claim is promoted without it, marked "not re-run" (Claim tiers, in `SKILL.md`).

## When the loop ends

The loop ends at the first of these:

- The question is answered: every outcome in the bar decided on reviewed claims, with only the concluding draws left for the closing pass.
- A stop condition the charter states is met.
- The queue is empty and re-planning finds no hypothesis left to test. Log why, and go to the closing pass with the question open.
- Everything left in the queue depends on a parked question.
- The closing time arrives. As it approaches, queue nothing that cannot finish before it; work still running at the closing time may finish if the reservation holds it.
- The environment fails in a way the run protocol cannot recover from. Record what failed, and spend what remains of the budget on the closing pass.

Nothing else ends it. A result that disappoints is a result: record it and re-plan. Continue without progress summaries or check-ins; they cost the user time they asked you to save.

## Closing pass

In this order, inside the reservation:

1. **Concluding draws** for the claims the report will conclude on, on the final code, under the charter's replication rule.
2. **The report** (below), drafted while the concluding draws run and completed once their numbers are in.
3. **Durable records** the project expects: its memory entry, and whatever documentation its own rules require for what the campaign changed. They include every trap that cost the run time, written where the charter's run protocol lives, so that the next campaign's charter inherits it instead of paying for it again. They are written before the closing review so that the review checks them too: a memory entry is read long after the report, and one that overstates a result misleads every session that loads it.
4. **The closing review.** Run `git status --porcelain` unscoped first: anything outside the manifest's files, the campaign's records (Layout, in `SKILL.md`) and the workspace is unaccounted for, and the dispatch says so. Then dispatch the closing review block, with a package built by `review-package` over the whole tree (`.`), so that a change the manifest omits is in front of the reviewer rather than hidden by the package's scope. Apply what it finds: corrections to the report and the durable records, and to the ledger by new entries. A Critical finding against code is fixed and goes through the implementation review like any other change, and the numbers the fix affects are re-run where the reservation allows; where it does not, the claims those numbers rest on are demoted, and the report's header says which results predate the fix. After a Critical finding, or any finding that changes the answer, the corrected report and records get a re-review on those findings alone, with the re-review block in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md`, the charter and the report standing in for the brief: a correction written under closing-time pressure is the text least likely to have been read twice. Record the review's outcome in the header.
5. **Identity** of the switched-off final code against the starting commit (Experiments). It runs after the closing review so that it checks the code the user will commit, whatever the review changed.
6. **The project's test suite**, where it has one, on the final code with every switch off, run with the command the charter names. The checkpoint the user commits must leave nothing broken for anyone who never turns a switch on. Record both results in the report's header, the suite's counts against the suite baseline. Where either fails and the reservation cannot hold the fix, the header states the failure -- for identity, the comparisons it voids; for the suite, the failing tests by name.
7. **The account.** Report in the conversation what the run delivered: the answer at its tier, the report path, and the closing review's outcome. The wrap-up presumes this account is given first.
8. **Wrap-up.** Follow `${CLAUDE_PLUGIN_ROOT}/skills/wrap-up/SKILL.md`, written to the wrap-up path (Layout, in `SKILL.md`). The run finished unattended, which is the condition under which that skill requires a written copy.

If the budget ends before the pass does, the report's header says which steps did not run. That is consolidation's cue to rely less on the report's own verdicts, and it is worth more than a report that reads as finished when it is not.

## The report

The report is to consolidation what a spec is to sdd. Consolidation turns it into production code without the campaign's context, and the user rules on it from what it says, so it carries its evidence rather than pointing at a scratch file that may be gone. It has no length cap. It is not the wrap-up, whose caps serve a different reader.

Sections, in order:

0. **Header.** The charter and ledger paths, the ledger marked as scratch; the report of the campaign this one continues, if any; the dates; the starting commit and the final code state; the ordered-kept changes the baseline was re-based on, if any; the closing review's outcome, or that it did not run; the identity and test-suite results; any closing step that did not run.
1. **Answer.** The question and the campaign's answer, at the tier it reached. Qualitative first -- saying plainly when the result is null, partial or negative -- then the numbers.
2. **Bar.** The bar as amended, with each amendment's date; the outcome of each criterion, with its numbers; the red run's result.
3. **Claims.** Every claim: ID, statement, tier -- marked "not re-run" where it was reviewed without one -- and the runs it rests on. Retracted claims stay, with the reason.
4. **Consolidation items.** One per manifest entry, or per group of entries that only make sense together: what it does; its switch and files; the claims it rests on, with their tiers; the recommendation -- keep, keep with changes, or discard -- and why; what its production form would need, such as a configuration key, a default, a merge with another item, or a home other than where the experiment put it; the items it was only ever measured together with; and its known issues.
5. **Provisional rulings.** Each with the claims it rests on and the result that would reverse it.
6. **For the user.** Parked questions, with what each one blocked; directive readings awaiting ratification.
7. **Reproduction.** For each concluded claim, how to reproduce it: code state, switches, inputs, commands, and where the raw output lives, marked scratch or tracked.
8. **Not done.** Hypotheses not tested and queue items not run, each with why.

It follows the rule for campaign files (Layout, in `SKILL.md`).

## Finish

After the wrap-up, give the user the next two steps:

- Checkpoint the campaign's state with `/lodestar:commit-plan`. It gives a campaign's code the `exp:` prefix, by which consolidation confirms the checkpoint. The campaign itself commits nothing.
- Then `/lodestar:consolidate <report path>`, in a fresh session.

Make no git mutations at any point in this phase, and allow none in a dispatched subagent. The repository owner commits.

## Resuming

A charter whose ledger already exists is a resume. The ledger's first line names its charter; if it names a different one, the workspace belongs to another run. Leave it alone and ask where this run's workspace should be.

Work through the ledger's resume checklist before launching anything. Then take the start message's place with a resume check, asked in one message while the user is present:

- **The baseline** is not a clean tree: the campaign's own changes are expected in it. It is the manifest's files, the campaign's records (Layout, in `SKILL.md`) and the workspace. Anything `git status --porcelain` shows beyond that set is unaccounted for: report it and let the user say whether it belongs.
- **The clock.** The deadline recorded at setup stands unless the user moves it, and a move is a charter amendment. If the closing time has already passed, say so and ask whether to go straight to the closing pass or extend the budget. If the deadline itself has passed, the question is theirs to settle before anything runs.
- **The stop.** Whatever stopped the previous run was resolved, if at all, in a conversation you cannot see: wait for the user to state the resolution, as sdd's Setup requires of a resume.

The dispatch answer in the standing section still binds; do not ask it again. Skip what setup already did: the ledger exists and must not be recreated from the skeleton, and the starting code, the noise and reference runs, the suite baseline and the red run are already recorded.

Before re-entering, reconcile the log against the implementer reports, the run registry and the run outputs. Work that finished after the last log entry is logged as recovered, not redone: an interruption routinely lands between a run's completion and its entry, and a log taken at its word re-runs what is already done. A gating result recorded just before the halt is checked before anything builds on it; re-run it only if its outputs are incomplete, since outputs can settle in minutes what a repeated run spends hours on.

Then re-enter at the loop, with the first queue item that is not done, or, if the closing time has passed, at the first closing step the log does not record as done.
