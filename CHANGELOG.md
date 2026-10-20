# Changelog

Versions follow the `[x.y.z]` tags in the commit subjects; 0.1.0 is the untagged first commit, and two commits carry `[0.1.5]`. Dates are commit dates.

## 1.0.1 -- 2026-10-19

- **Heartbeat on a chained timer** (`shared/runs.md`): the heartbeat is a background `sleep` for the period, re-armed at each firing, instead of a scheduled job, which can stay listed yet never fire. Where the harness caps a background command's run time, the sleep gets a timeout longer than the period.
- **Confirm it fires**: after arming, and after every compaction or restart, the sleep is confirmed running from the process state, and any wake-up checks the last logged firing against the period, re-arming an overdue heartbeat.
- Manifest description no longer calls the set minimalistic.

## 1.0.0 -- 2026-10-19

- **Shared run rules** (`shared/runs.md`): model selection, dispatch cost, the operating rules and report contract, implementer status routing, the workspace and ledger, and resuming moved out of `sdd` into one file that `sdd`, the campaign autopilot, `consolidate` and the inline route out of `design` each read at the start of a run. The workspace, ledger and resume rules, previously restated in several skills, are stated there once; each skill keeps only where it differs. The inline route's implementer dispatches now carry the operating rules, as every other dispatch does.
- **Long runs** (`shared/runs.md`): one heartbeat rule for `sdd`, the campaign autopilot, `consolidate` and the inline route out of `design`. A recurring wake-up, every 45 minutes unless the run's document names another period, stays armed while anything runs in the background. It checks for stalls, refreshes the controller's context from the ledger, and is re-armed after anything that silently stops background tasks. The campaign autopilot's heartbeat now points here instead of defining its own.
- **Foreground long checks** (`shared/runs.md`): a long check the controller waits on in the foreground runs under a time limit the command enforces itself, since no heartbeat can wake a controller blocked on it; one in the background is watched by the heartbeat instead.
- **Compaction** (same section): when the user is about to compact, the run brings its ledger up to date, says whether this is a good point, and gives the one message to continue with; after the compaction it re-reads its rules and carries on from the ledger rather than through a resume procedure. `consolidate` gains a resume path for a session that ended.
- **Fresh run after a completed one** (`sdd`): the ledger records `Run complete`; an existing workspace is archived only when its ledger says so, so a resume keeps its ledger.
- **Attention list** (`design`, `campaign`, `consolidate`): a design, charter or spec is presented led by the decisions the user did not state or confirm and the judgement calls that could go the other way, and the file review leads with the same list.
- **Experiment lane** (`consolidate`): a bounded way to settle a question a few runs can answer inside consolidation, under the campaign's rules for code, runs and evidence, with a question, a settling result and a time budget the user sets; the spec carries its result. `commit-plan` gives the lane's code the `exp:` prefix.
- **Scratch listing** (`consolidate`): the consolidation spec ends with a step that lists the scratch the consolidation made redundant, with sizes and what deleting each entry loses. It lists only and deletes nothing.
- **Codex support removed.** The `.agents/` entry points are gone, and the README claims Claude Code only.
- Added this changelog.

## 0.9.0 -- 2026-10-10

- Dispatch cost (`sdd`, used by every skill): dispatch fresh subagents and resume one only straight after it returns; batch work to carry the cost of each dispatch; long checks belong to the controller, and subagents never wait past their prompt cache.

## 0.8.4 -- 2026-10-04

- `campaign`: a heartbeat, a recurring wake-up at the period the charter's run protocol names, checks for stalled runs and agents and refreshes the controller's context.

## 0.8.3 -- 2026-09-30

- `commit-plan`: commands for a Unix shell (bash, zsh, fish) are chained with `&&`, so a failed commit stops the run instead of sweeping its files into the next one.

## 0.8.2 -- 2026-09-29

- `campaign`: the run stops at the loop's end, reports the results, and asks whether to keep experimenting or close. The time budget covers only the experiments, and the closing pass's plan and estimate are presented for approval.

## 0.8.1 -- 2026-09-28

- `campaign`: durable records -- memory entry and documentation -- are written once, for the campaign as a whole, in the closing pass.

## 0.8.0 -- 2026-09-27

- New `campaign` skill: settles a self-contained charter with the user, runs experiments unattended with graded claims, and closes with a report.
- New `consolidate` skill: reviews a campaign's results cold, takes the keep-or-discard rulings, and writes the spec that turns kept changes into production code.
- The dispatch question: long runs ask which models to dispatch before the first dispatch.
- `commit-plan` gives campaign code the `exp:` prefix.

## 0.7.1 -- 2026-09-25

- `commit-plan`: subjects kept to roughly 50 characters, never more than 60.

## 0.7.0 -- 2026-09-23

- New `commit-plan` skill: groups the uncommitted tree into commits and gives the commands for the user to run.
- PowerShell copies of the `sdd` helper scripts removed; the bash scripts serve every platform.

## 0.6.0 -- 2026-09-08

- Codex entry points under `.agents/skills/`, with PowerShell copies of the `sdd` helper scripts (Codex support removed in 1.0.0).

## 0.5.1 -- 2026-09-03

- Written documents have no maximum line length or hard wrapping: one paragraph is one line.

## 0.5.0 -- 2026-09-02

- `design`: the testing decision names the part of acceptance only a person can check, written as a procedure; `wrap-up` carries it to the user.

## 0.4.2 -- 2026-09-02

- `wrap-up`: sections 1 to 4 name the work by what it is rather than by its task label.

## 0.4.1 -- 2026-08-27

- `design`, `sdd`: a red discriminates only against code that is present and wrong.

## 0.4.0 -- 2026-08-26

- `design`, `sdd`: a test-first red on absent code no longer counts as evidence that a test can fail; implementers run existing behaviour's tests before changing it, and never explain a failing check away.

## 0.3.2 -- 2026-08-26

- `design`: the inline route begins with a written plan.

## 0.3.1 -- 2026-08-24

- `design`, `sdd`: every testing criterion names the configuration that turns it red, and a check never seen failing is not evidence.

## 0.3.0 -- 2026-08-21

- Model invocation enabled: skills can be loaded by the model when the work matches their description, as well as by slash command.

## 0.2.1 -- 2026-08-19

- `wrap-up`: a fifth section briefs a fresh session that reads the work cold.

## 0.2.0 -- 2026-08-10

- `design` decides whether the work owes a standalone document.

## 0.1.9 -- 2026-08-03

- `sdd`: reports suite counts rather than a verdict, and what shipped, before the wrap-up.

## 0.1.8 -- 2026-07-29

- `wrap-up`: a section on what the user should do to verify the work.

## 0.1.7 -- 2026-07-29

- `design`: limits on spec length.

## 0.1.6 -- 2026-07-29

- `design`: split a brief into several specs only when it spans several subsystems.

## 0.1.5 -- 2026-07-29

- `sdd`: larger task granularity, and dispatching with only the context each task needs.

## 0.1.4 -- 2026-07-28

- `design`: the spec's cold review flags claims about behaviour that rest on no number. `sdd`: the plan's cold review checks whether a task's verification could fail for a reason that task does not control.

## 0.1.3 -- 2026-07-28

- `sdd` ends with a report and the `wrap-up`.

## 0.1.2 -- 2026-07-28

- `sdd`: richer task log in the ledger.

## 0.1.1 -- 2026-07-28

- `handoff`: trimmed output.

## 0.1.0 -- 2026-07-27

- First release: `brainstorming`, `design`, `sdd`, `handoff`, `wrap-up`, and the shared agent contract.
