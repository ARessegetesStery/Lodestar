# Ledger skeleton

Copy everything between the two horizontal rules into `<workspace>/ledger.md` at setup, and fill the bracketed slots. The parenthesized lines are guidance: delete each one when its section gets its first content. This paragraph addresses the controller and is not part of the ledger.

---

# Campaign ledger -- charter: [CHARTER PATH]

Workspace: `[WORKSPACE PATH]` (scratch, git-ignored). This file is the run's recovery map across context compactions -- trust it over recollection -- and the record a cold reviewer reads during consolidation. Sections 1 to 7 hold the current state and are updated in place, each change through an entry in section 8. Section 8 is append-only: an earlier entry is never edited, and a correction is a new entry naming the one it corrects.

## 0. Resume checklist

1. Re-read the campaign skill's autopilot rules, `[AUTOPILOT.MD PATH]`, and `[WORKSPACE PATH]/operating-rules.md` in full. A compaction keeps them only as a summary.
2. Read section 1, and the charter's Amendments section.
3. Read sections 2 to 7 for the current state.
4. Read the newest entries of section 8. `grep -n '^### ' ledger.md` lists them.
5. Before launching anything, check what is still running, per the run protocol, and the background tasks section 1 registers.
6. On a resume, reconcile section 8 against the implementer reports, section 7 and the run outputs, and log any work that finished unlogged as recovered.

## 1. Standing section

- Current status: [one line, updated in place: what is running, what is next, the newest result].
- Background tasks: [every waiter, queue or watchdog the controller has started, with what it waits for; struck when it ends].
- Charter: `[CHARTER PATH]`. Starting commit, HEAD at setup: `[SHA]`. Starting code kept at: `[WORKSPACE PATH]/[PATH OF THE BUILD OR EXPORT]`, replaced by a re-based copy when an ordered-kept change lands.
- Clock, from `date`: start [TIME], deadline [TIME]. Closing pass: approved [DURATION], start [TIME], end [TIME].
- Dispatch: [the user's answer to the dispatch question, verbatim].
- Start-message resolutions: [each dated, verbatim].
- Directives mid-run: [each dated and verbatim, with the reading beside it and whether the user has ratified it].
- Operating rules: `[WORKSPACE PATH]/operating-rules.md`. Run protocol: [the charter section, or the project document's path].
- Suite baseline: [the counts, and the command that produced them; or: the project has no test suite].
- Noise residual: [what differs between two runs of the starting code, and between two suite runs where its counts depend on data].
- References: [each reference number the bar compares against, as re-measured at setup, with its run label].
- Red run: [its label, its result against the prediction, and the wall time of one run of the bar].

## 2. Manifest

| ID | Switch | Files | What it does | Experiment | Status | Known issues |
|----|--------|-------|--------------|------------|--------|--------------|

(Columns and statuses: The manifest, under Experiments in `autopilot.md`.)

## 3. Claims

| ID | Claim | Tier | Rests on (run labels) | Last moved in entry |
|----|-------|------|-----------------------|---------------------|

(Tiers: observation, indicative, reviewed, concluded, retracted. A claim reviewed without a re-run is marked "not re-run". A retracted claim stays in the table.)

## 4. Provisional rulings

| ID | Ruling | Alternatives set aside | Rests on (claim IDs) | Would be reversed by |
|----|--------|------------------------|----------------------|----------------------|

## 5. Parked questions

| ID | Question | Blocks | Parked in entry |
|----|----------|--------|-----------------|

## 6. Hypothesis queue

(In order. Each item: an ID, the hypothesis, the measurement that tests it, and its status -- queued, running, done in entry N, or dropped in entry N with the reason. An experiment takes its item's ID.)

## 7. Run registry

| Label | Started | Code state (state file, build configuration, artifact hash, switches) | Inputs | Command | Output path | Time limit | Exit | Wall | Anomalies |
|-------|---------|-----------------------------------------------------------------------|--------|---------|-------------|------------|------|------|-----------|

(State file: `states/<label>.md` in the workspace, or "starting commit" before the first change. Reviewers' re-runs are registered here too. If runs are registered by a script, name its registry file here instead.)

## 8. Log

(One heading per entry, in this form, so an entry can be found by grep. Kinds: setup, brief, implementation, review, run, reading, claim, retraction, ruling, parked, directive, amendment, correction, recovered, go-ahead, closing. A brief carries the fields of The loop's step 2 in `autopilot.md`. A claim entry names the evidence that moves the claim. A correction names the entry it corrects. A retraction lists everything that rested on the retracted claim. A recovered entry logs work a resume found finished but unlogged.)

### [YYYY-MM-DD HH:MM] entry [N] -- [kind]: [title]

---
