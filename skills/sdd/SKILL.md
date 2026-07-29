---
name: sdd
description: Use when an approved spec or plan is ready to execute through per-task subagents, or when a spec needs an implementation plan written from it; entry points for spec-in, plan-in, and plan-only.
disable-model-invocation: true
---

# Subagent-driven development

## Purpose

Execute a plan by dispatching a fresh implementer per task, reviewing each task as it lands, and reviewing the whole branch at the end.

Subagents inherit none of this session's context, so you construct exactly what each one needs. Everything you paste into a dispatch, and everything a subagent prints back, stays resident in your context for the rest of the session. Hand artifacts over as files.

## Entry points

- **Spec in hand.** Write the plan, self-review it, then run the execution loop. The self-review is the gate; do not wait for approval of the plan.
- **Plan in hand.** Skip planning. Run the execution loop against the given plan file.
- **Plan only.** Write the plan and stop, typically to hand it to another session or agent.

## Scale escape hatch

If while planning the work collapses to a few bounded edits, say so and recommend inline implementation. Do not run the loop on work that does not need it.

## Writing the plan

Write it to `docs/lodestar/plan/YYYY-MM-DD-topic-plan.md`. That is the default; a location or naming convention stated by the project or by the user overrides it.

Write the whole plan for a reader with zero conversation context: no shorthand, no relative dates, everything named by path.

**Scope check.** If the spec covers several independent subsystems, say so and recommend one plan per subsystem. Each plan should produce working, verifiable software on its own.

**Map the files first.** Before defining tasks, list the files to be created or modified and what each is responsible for. This is where decomposition is decided; the task boundaries follow from it. Prefer focused files with one responsibility. In an existing codebase, follow the established structure.

**Right-size the tasks.** A task is the smallest unit that carries its own verification and is worth a fresh reviewer's gate. Fold setup, configuration, scaffolding, and documentation into the task whose deliverable needs them. Split only where a reviewer could meaningfully reject one task while approving its neighbour.

### Plan header

- **Goal.** One or two sentences.
- **Spec.** The path to the spec, if there is one.
- **Architecture.** Two or three sentences on the approach.
- **Verification strategy.** How the work as a whole is checked, from the spec's testing section where one exists.
- **Global constraints.** The requirements that bind every task and that no single task states: exact values, exact formats, and the stated relationships between components -- "same layout as X", "matches Y". Take them from the spec's Architecture and Context sections, copied verbatim, since this is also what the reviewers get as their attention lens and a paraphrase weakens it. Every task's requirements implicitly include this section.

  Environmental facts an implementer can read off the project itself -- language version, dependency policy, platform -- do not belong here. They are already in the manifest and the surrounding code, and restating them adds a second place to go stale. Where the design turned one of them into a decision, it is a design decision and travels as one.

### Per task

Head each task `### Task N: <name>`, in exactly that form -- the task-brief script matches it to extract one task's text, and a task it cannot find cannot be dispatched.

- **Files.** Exact paths, marked create / modify / test. These paths are what scopes the task's review package, so they must be complete.
- **Interfaces.** *Consumes*: what this task uses from earlier tasks, with exact signatures. *Produces*: what later tasks rely on -- exact names, parameter and return types. An implementer sees only its own task, so without this block two capable subagents will pick two different names for the same thing.
- **The change**, described concretely: what to do, not a direction to head in.
- **Context** the implementer needs: docs to read, project conventions that apply, known gotchas.
- **Verification**: the exact commands or tests, written out, each one a check on something this task produces. A gate that turns on behaviour the task does not own cannot tell you whether the task succeeded.
- **Non-goals** wherever scope could bleed into a neighbouring task.

Sizing note: describe the change, do not transcribe it. Literal implementation code in the plan writes the work twice and pins implementers to the cheapest tier -- see Model selection.

### No placeholders

None of these belong in a plan: "TBD", "TODO", "implement later"; "add appropriate error handling", "handle edge cases"; "write tests for the above" with no statement of what they assert; "similar to Task N" instead of saying it again; references to types or functions no task defines.

### Plan self-review

Read the plan once against the spec:

1. **Coverage.** Point to a task for each requirement in the spec. Add tasks for any gap.
2. **Placeholders.** Scan for the patterns above.
3. **Interface consistency.** Do the names, signatures, and types used in later tasks match what earlier tasks produce?

Fix what you find inline. Then dispatch one reviewer to read the plan cold, with the spec where there is one, and report back on three things: whether an engineer could follow each task without getting stuck, whether any spec requirement has no task, and whether any task's verification could fail for a reason that task does not control. This is not a gate -- you act on what comes back and carry on -- but you wrote the plan, so you are the worst judge of whether its descriptions are followable, and these plans describe the work rather than contain it.

Then proceed to execution.

## Model selection

Use the least powerful model that can carry each role. Cost and speed both follow from this, and the ceiling is rarely the bottleneck.

- **Mechanical implementation** -- a single file, a change with no derivation left in it: a fast, cheap model. This tier is narrower than it looks; see Turn count below.
- **Integration and judgment** -- multi-file coordination, matching an existing pattern, debugging: a standard model.
- **Architecture and design judgment**, and the final whole-branch review: the most capable model available. The final review is the one dispatch that should never quietly take the session default.
- **Reviews** scale to the diff: size, complexity, and risk. A small mechanical diff does not need the top tier; a subtle concurrency change does.
- **A task still failing after three fix rounds** goes to a model at least one tier above the one that got stuck, as the fix loop below specifies.

**Name the model explicitly on every dispatch.** An omitted model inherits this session's, which is usually the most capable and most expensive one available, and that silently undoes everything above.

**Turn count beats token price.** Wall-clock and context cost both scale with how many turns a subagent takes, and the cheapest models routinely take two to three times the turns on multi-step work -- costing more in total than the tier that would have done it in one pass. Treat a mid tier as the floor for reviewers, and for any implementer working from a prose description rather than from literal code. Reserve the cheapest tier for work with no derivation left in it: a single-file mechanical fix, or the rare task whose text already contains what to write. Because the plan format above describes changes rather than transcribing them, that second case is uncommon by design -- a task can read as thoroughly specified and still require the implementer to work out the code. The standard tier is therefore the normal choice for implementation, not the exception.

## Setup

**Workspace.** Each plan owns a directory holding every artifact for that plan: the ledger, the operating rules, task briefs, reports, and review packages. Use the repo's designated scratch area -- `Temp/lodestar/<plan-basename>/` unless the project's CLAUDE.md designates elsewhere. Never a single shared path that every run appends to; that file only grows and stops being readable. If a directory already exists for this same plan from an earlier run, move it to `<scratch>/lodestar/archive/<plan-basename>/` -- inside the same scratch area, never outside it -- and start clean rather than appending.

Confirm the directory is git-ignored before writing into it -- `git check-ignore <path>` -- since briefs, reports, and review packages otherwise land in the diff the owner has to commit. If it is not ignored, say so and settle the location before dispatching anything.

**Ledger.** `<workspace>/progress.md`, with its identity on the first line: `# SDD ledger -- plan: <plan file path>`.

Look for one at that path before creating it. If its first line names this plan, the run is being resumed: every task carrying a `complete` line is done, so do not re-dispatch it, and pick up at the first task without one. A task whose last entry is a fix round is mid-loop; resume at the next round. A ledger naming a different plan belongs to another run -- leave it alone and start your own.

Two things about resuming that the ledger cannot supply. If the previous run stopped, the user resolved whatever stopped it in a conversation you cannot see, so wait for them to state that resolution rather than inferring one from the ledger's account of the problem. And where the run stopped at or just after a task whose verification gates the work that follows, re-run that verification before continuing: a gate recorded as passed by a run that then halted is the one result least safe to take on trust.

Conversation memory does not survive compaction, and a controller that has lost its place will re-dispatch work that was already done. The ledger is the recovery map: trust it over your own recollection. It opens with a standing section carrying the plan and spec paths, which governs on a plan-versus-spec conflict, the execution mode, and any hard rules for the run. Append to that section whenever the user issues a directive mid-run -- dated, in their words -- because those bind every later task and nothing else records them.

Below that section, before the first dispatch, write the **task list**: one line per task in the plan, `Task N: <name> -- <one-line summary of what it delivers>`. Progress lines append underneath it. Without it the ledger records only what is finished, so a controller reading it after compaction can see where the run stopped but not how much is left or what it consists of, and it would have to re-read the plan to find out.

**Establish the baseline.** Nothing is committed during a run, so the working tree is the only record of what has been done, and every task's scope check compares against it. What counts as a clean start depends on which kind of run this is, which is why this comes after the ledger lookup rather than before it.

On a **fresh run**, `git status --porcelain` should come back empty. If it does not, stop and tell the user what is outstanding rather than starting. Work that was already uncommitted is indistinguishable from work a task produced, and it will read as scope bleed on every task that follows.

On a **resumed run**, the tree is expected to carry the completed tasks' output -- that is the point of resuming. The baseline is the set of files the ledger records against completed tasks. Anything `git status` shows beyond that set is unaccounted for: report it and let the user say whether it belongs before going on.

A clean tree is not a working one. Run the plan's verification strategy once before Task 1 and record the result in the ledger. A failure that was already there makes every later failure ambiguous, and the first task to touch that area burns fix rounds on someone else's bug. Report a red baseline and let the user decide whether to proceed past it.

**Operating rules.** Before the first dispatch, assemble `<workspace>/operating-rules.md`: the agent contract from `${CLAUDE_PLUGIN_ROOT}/shared/agent-contract.md` -- the fenced block only, not the file's opening paragraph, which addresses you -- followed by this project's own rules, its testing and environment conventions, and the report contract below. The contract is the portable part; the project supplies the rest. Every implementer dispatch carries this file's contents, pasted, and never merely referenced. Reviewers get their constraints from the review blocks and the plan's Global Constraints instead; the report contract in this file is written for an implementer and does not apply to them.

**Pre-flight scan.** Before dispatching Task 1, read the plan once for tasks that contradict each other or the global constraints, and for anything the plan mandates that a reviewer would treat as a defect. Present everything found as one batched question, each finding beside the plan text that mandates it, asking which governs. If the scan is clean, proceed without comment.

## Execution loop

### Dispatch

- Extract the task text with `bash "${CLAUDE_PLUGIN_ROOT}/skills/sdd/scripts/task-brief" PLAN_FILE N OUTFILE`, and give the implementer that path. Never make an implementer read the whole plan.
- The dispatch prompt contains: the operating rules pasted verbatim; one line on where this task fits; the brief path, introduced as its requirements, with exact values to be used verbatim; interfaces and decisions from earlier tasks that the brief cannot know; your resolution of any ambiguity you noticed in the brief; and the report-file path.
- A dispatch describes one task, not the session's history. Do not paste accumulated prior-task summaries into later dispatches.
- If an earlier task parked a finding in the area this task touches, carry a pointer to that ledger entry.
- Parallel dispatch is fine where the tasks' declared file sets are disjoint, and two implementers must never hold the same file. Disjoint files are necessary and not sufficient: two tasks whose difficulty shares one underlying cause get solved two different ways by two implementers who cannot see each other, and the divergence surfaces only at the final review. Judge conservatively -- a declared list is a claim about what a task will touch, not a guarantee, and tasks working the same area routinely reach further than their list says. Dispatch serially where you suspect a shared root cause, where the sets merely look disjoint, or where either task's boundary is soft. A serial run costs a delay; a wrong call puts two implementers in one file with no commit boundary between them and no way to separate the results.
- Record the implementer's identity and the model you dispatched it on; fix rounds 1 to 3 resume the one, and rounds 4 and 5 escalate a tier above the other.

### Report contract

This block goes into the operating rules, pasted, with the report path filled in per dispatch:

---

**Reporting.** Write your full report to the report file named in your dispatch: what you implemented, what you verified with the exact command and its output, the files you created and modified, your self-review findings, and any concerns.

For each test the task named as its verification, record that you watched it fail before the code existed -- the command, the failing output, and why that failure was the expected one -- and then the passing run afterwards. A test that has never failed has not been shown to test anything.

Before reporting, check your tests against a deliberate small breakage: a wrong constant, the wrong branch taken, a step left out, an empty return. If none of your tests would fail for any of those, they do not cover the behaviour they claim to, and saying so is more useful than reporting a pass. If a reviewer later sends you findings, APPEND your fix report to that same file -- never start a new one -- including the covering tests, the command run, and the output.

Then reply with ONLY the following, under fifteen lines, because the detail lives in the report file:

- **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- Files created and modified
- A one-line verification summary
- Your concerns, if any
- The report file path

**Escalating is always available and never counts against you.** Bad work is worse than no work. Stop and escalate when the task needs an architectural decision with several defensible answers; when you need to understand code beyond what you were given and cannot find it; when you have been reading file after file without making progress; or when finishing would mean restructuring something the task did not anticipate. If something is unclear before you start, ask then rather than guessing.

Use DONE_WITH_CONCERNS if you finished the work but have doubts about its correctness. Use BLOCKED if you cannot finish. Use NEEDS_CONTEXT if you need information you were not given. For those last two, put the specifics in the reply itself -- the controller acts on them directly. Never silently produce work you are unsure about.

---

Reports live at `<workspace>/task-N-report.md`. The four statuses route differently:

- **DONE** -- build the review package and dispatch the reviewer.
- **DONE_WITH_CONCERNS** -- read the concerns first. Correctness or scope concerns are addressed before review; observations are noted and review proceeds.
- **NEEDS_CONTEXT** -- supply what was missing and re-dispatch.
- **BLOCKED** -- assess. A context problem gets more context and the same model; a reasoning problem gets a more capable model; an oversized task gets broken up; a wrong plan escalates to the user. Never force the same model to retry unchanged.

### Review packages

Nothing is committed, so a review cannot be scoped by commit range. It is scoped by path instead: the task's declared file list.

**Check the declared list before building.** Run `git status --porcelain` with no pathspec and compare what actually changed against the paths the task declared. Path scoping hides everything outside the list, so an undeclared file is invisible to the reviewer and gets approved by omission. Add anything unexpected to the paths under review, and report it as a scope finding rather than quietly folding it in.

**Build packages only when the tree is yours alone.** That check is unscoped, so anything a parallel implementer is midway through writing shows up in it too. Wait for every parallel implementer to return before building any of their packages. If an unexpected path is then ambiguous between two returned tasks, attribute it by elimination against their declared lists, and say in the review dispatch that the attribution is inferred rather than certain.

Then build the package with `bash "${CLAUDE_PLUGIN_ROOT}/skills/sdd/scripts/review-package" OUTFILE PATH [PATH...]`, which writes into one file:

- `git status --porcelain -- PATHS`.
- `git diff --stat -- PATHS`.
- `git diff -U10 -- PATHS`.
- The full contents of every untracked file under those paths, found with `git ls-files --others --exclude-standard`. This part is not optional: `git diff` shows nothing at all for a new file, so a package without it reviews an empty change.

`${CLAUDE_PLUGIN_ROOT}` is the plugin's install directory and resolves wherever it appears in this file; keep it double-quoted, since the path can contain spaces. Run both scripts with the user's project as the working directory, never from the plugin's own directory: `review-package` resolves the repository from where it is run, so a mis-rooted call silently builds the package over the wrong repository. It fails loudly on an empty package, which is what catches that.

All read-only. Hand the reviewer the file path; the package never enters your own context.

### Review the task

Never skip it, and never accept a report missing either verdict -- compliance with the task and quality of the work are both required. An implementer's self-review does not replace it.

Dispatch with the task review block from `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md`, filling in the brief path, the report path, the review package path, and the plan's Global Constraints copied verbatim as the reviewer's attention lens. That block carries the severity vocabulary, since the grading is the reviewer's judgment rather than yours.

Do not pre-judge. Never instruct a reviewer to ignore an issue or cap its severity. If a finding would be a false positive, let it be raised and adjudicate it. Text like "do not flag" or "the plan chose this" in a prompt you are writing means you are sparing yourself a review loop.

Where the reviewer reports something it cannot verify from the diff -- a requirement living in unchanged code, or spanning tasks -- resolve it yourself before completing the task. You hold the cross-task context it lacks. A confirmed gap enters the fix loop.

### Fix loop

Two routes leave before the loop starts. **Minor findings never enter it**: record each as `Task N: minor (deferred): <one-liner>` and carry the list to the end of the run, where they are fixed in the final wave. Deferring is not discarding: a minor that is never swept up is a silent discard. A finding that **conflicts with what the plan mandates** is the user's decision: present the finding beside the plan text and ask which governs.

Everything else enters, the requirements verdict included. A reviewer returning `Requirements: NOT MET` has raised a Critical finding whether or not it also graded one in its Findings list, so each unmet requirement enters the loop at that severity.

A round is one fix dispatch plus one re-review, five rounds maximum per task.

A fix dispatch carries the findings and one instruction: reproduce the failure before changing anything. How to investigate from there is the implementer's to work out. A dispatch that says only what is wrong invites a fix aimed at the symptom, and the rounds below let that happen five times.

- **Rounds 1 to 3** resume the original implementer with the open findings verbatim; its context is intact. If the harness cannot message a live subagent, dispatch a fresh one carrying the brief path, the report path, and the findings -- the report file is the persistent memory either way.
- **Rounds 4 and 5** dispatch a fresh implementer one tier up, told that a prior implementer attempted the task and that the report file holds what was tried. A loop surviving three resumes usually means the implementer cannot see its own problem.

Every round, the implementer re-runs the verification covering the amended code and appends its fix report. Confirm that report names the covering tests, the command, and the output before re-reviewing. A fix dispatch is an implementer like any other, so the quiet-tree rule governs its package too: where two tasks are in fix rounds at once, wait for both before building either package.

The re-review regenerates the package over the same paths, so it sees the whole task again rather than only the fix. It is scoped by the prompt instead: dispatch the re-review block from `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md`, carrying the open findings verbatim. New Critical or Important breakage joins the open findings; anything else it notices goes to the ledger as a deferred minor and never extends the loop.

Append after each round: `Task N: fix round R/5 (impl: <model>, review: <model>): X addressed, Y open. <one-liners>`.

Never fix findings yourself. Controller fixes skip review and cost you the context you are protecting.

**At the cap**, stop dispatching and adjudicate each open finding. A finding that is wrong or contestable is parked with a ruling: `Task N: parked: <finding>. <why the code stands>`. A finding that is real but nothing builds on is parked the same way. A finding that is real and load-bearing -- a later task depends on it, or it exposes a plan defect -- stops the run: append `Task N: blocked: <reason>` and report to the user with the finding, the plan text it collides with, and the fix history. A requirement still unmet at the cap is not among the things you can park -- the task has not done what was asked of it, whatever else depends on that -- so it stops the run the same way: append `Task N: blocked: requirement not met` naming the requirement, and report as above. Adjudicate only at the cap; doing it earlier to end a loop is pre-judging under another name, and every adjudication is a ledger entry.

### Complete the task

Append `Task N: complete (impl: <model>, review: <model>): <one-line summary>`. Name the models actually dispatched, not the tier the plan called for; where fix rounds escalated, name the model that finished the task. The summary carries the files touched -- the actual set, including anything the scope check added -- and the review outcome, noting any parked findings. Model selection is a judgment made per dispatch and nothing else records it, so without this the run leaves no evidence of which tier produced which code -- which is what a resumed run escalates from, and what the final review and the user need to know when deciding how far to trust a task. The final review's package is built from these lines. Never start the next task while a Critical or Important finding is neither fixed nor parked with a ruling at the cap.

## Continuous execution

Run the plan to the end without checking in. Progress summaries and "shall I continue?" prompts cost the user time they asked you to save.

Once the first task is dispatched, five things stop the run, and nothing else: the user asked for a review gate; a review finding conflicts with what the plan mandates, which is theirs to resolve and not yours; an implementer reports that the plan itself is wrong; a finding survives the fix cap and is either load-bearing or an unmet requirement; or continuing would build later tasks on something known to be wrong. In each case, stop and report what happened rather than working around it.

Record why in the ledger. Add it to project memory only where the stop ends the session rather than being resolved inside it: the workspace is scratch and does not survive, so a later session that does not know this plan exists would otherwise have no way to learn the work was left mid-flight. A stop the user resolves in the same conversation stays in the ledger alone -- a memory entry for it is stale the moment the run continues.

## Final review

Build the package from the union of the files the ledger records as touched, not from the plan's declared lists. The two differ by every file a task changed without declaring, and those are the files nobody planned for -- the last set that should be dropped from the last review. Dispatch the final whole-branch review block from `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md` on the most capable model available, giving it the plan, the spec where one exists, the package, and the ledger.

Then dispatch **one** fix subagent carrying the complete list: the final review's own findings, every deferred minor from the ledger, and every parked finding the review overturned or re-graded upward. A ruling the final review rejected is a finding again, and nothing else would carry it back. Not one fixer per finding -- each separate fixer rebuilds context and re-runs suites. Then run one re-review of that fix, over a package scoped to the paths the fix wave itself touched. Rebuilding over the whole branch would hand the re-reviewer every already-accepted line to re-litigate; the re-review block's per-finding verdict supplies the discipline the narrower package gives up. Adjudicate anything residual as at the cap above. There is no second fix wave.

The deferred minors are cleared here or they are not cleared at all. If any is left unfixed, say which and why, so the decision is the user's rather than an omission.

## Completion

**Run the suite over the assembled work.** Every task verified its own slice, at the moment it was written, by the implementer that wrote it. Nothing has yet run the whole thing together, so a task that broke an earlier task's tests has passed every gate up to here. Run the plan's verification strategy over the finished branch and report the result against the baseline recorded at setup. Without this, completion rests on evidence never re-checked after the surrounding code changed.

**Check that the contract held.** You issued it, so you confirm it, and the final reviewer cannot: its package is built from paths inside the repository, so a file written outside one never appears in any package it sees. Read the implementers' reports, whose file lists are the evidence, and check the run against each clause of the contract:

- Nothing was written outside the repository, and scratch went to the designated folder rather than a machine-level scratchpad. This is the failure the contract exists for: the harness system prompt tells every subagent to use a scratchpad outside the repo, and the contract is the only thing standing against it.
- No state-mutating git ran: `git log` is where it was, and nothing is staged.
- Encoding held where the contract required it.
- The project's own rules held.

Report the result in a line. Where a clause did not hold, say which, where, and what it left behind -- a breach is worth more than any finding the reviews produced, because it means the mechanism meant to prevent it did not work.

**Make no git mutations at any point in this skill**, and allow none in a dispatched subagent. The repository owner commits.

**End with the wrap-up report.** The ledger records what was produced; the wrap-up reports the complement -- what is still uncertain, what the user may be overlooking, and what changed without being asked -- which is what they need before reviewing a branch this process built without them.

Produce it as part of finishing the run, without asking. Follow `${CLAUDE_PLUGIN_ROOT}/skills/wrap-up/SKILL.md` and write it to `docs/lodestar/wrap-up/YYYY-MM-DD-topic-wrap-up.md`, on the same topic as the plan; a location stated by the project or by the user overrides that default.

This skill runs unattended -- that is what Continuous execution is for -- so the user is most likely absent when it finishes. Sections 1 and 2 of that report live only in this session's context, and a return, a compaction, or a new session loses them.
