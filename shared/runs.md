# Runs

The machinery every Lodestar run shares when it dispatches subagents or outlasts the user's attention: `lodestar:sdd`, the `lodestar:campaign` autopilot, `lodestar:consolidate`, and the inline route out of `lodestar:design`. Each of these reads this file in full when its run starts; a skill that only names the model for a single dispatch reads Model selection. The rules live here once so that the skills cannot drift apart on them. Where a skill's own process differs, the skill says so in its own text, and its difference governs; where it says nothing, the rule here holds.

## Model selection

### The dispatch question

Before the first dispatch of a run, ask the user which applies: the tiering policy below; one model they name for every dispatch; or models they name per role -- implementer, reviewer, final reviewer. Skip the question only where the invocation already answers it, or, on a resume, the ledger records it. Models change faster than these rules do, and the user may know the current ones better than a policy written against an earlier generation of them. The question costs one exchange at the one moment the user is sure to be present; a wrong tier costs every dispatch of a run they are not there to watch.

Record the answer in the ledger's standing section, in the user's words, when the ledger is created. It binds every dispatch of the run, including the final review, wherever the skill names a tier; it survives compaction; and a resumed run reads it there rather than asking again. Whichever answer is given, the rule below on naming the model still holds: an answer of "the policy" is carried out by naming each tier's model on its dispatch, not by omitting the model. Where the answer fixes a role's model -- one model named for every dispatch, or one named for that role -- an escalation a skill makes by tier stays on that model, and a BLOCKED reasoning problem is re-dispatched to a fresh agent on it.

Each skill maps its own dispatches onto the three roles, so a per-role answer covers them.

### The tiering policy

Use the least powerful model that can carry each role. Cost and speed both follow from this, and the ceiling is rarely the bottleneck.

- **Mechanical implementation** -- a single file, a change with no derivation left in it: a fast, cheap model. This tier is narrower than it looks; see Turn count below.
- **Integration and judgment** -- multi-file coordination, matching an existing pattern, debugging: a standard model.
- **Architecture and design judgment**, and the final whole-branch review: the most capable model available.
- **Reviews** scale to the diff: size, complexity, and risk. A small mechanical diff does not need the top tier; a subtle concurrency change does.

**Name the model explicitly on every dispatch.** An omitted model inherits this session's, which is usually the most capable and most expensive one available, and that silently undoes everything above.

**Turn count beats token price.** Wall-clock and context cost both scale with a subagent's turns, and the cheapest models routinely take two to three times as many on multi-step work -- costing more in total than the tier that would have done it in one pass. Treat a mid tier as the floor for reviewers and for any implementer working from a prose description. Reserve the cheapest tier for work with no derivation left in it, which a plan or brief that describes the change rather than transcribing it makes uncommon by design: a task can read as thoroughly specified and still require the implementer to work out the code. The standard tier is the normal choice for implementation, not the exception.

## Dispatch cost

Every dispatch pays a fixed cost before it does any work -- its prompts, and the files it reads to get its bearings -- and a subagent left waiting past its prompt cache pays it again. The rules below keep both small against the work they buy, in every skill that dispatches.

**Dispatch fresh; resume a subagent only straight after it returns.** A resumed subagent reprocesses its entire transcript -- every file it read and every output it printed -- before its first new turn. That is cheap only while the transcript is still in the provider's prompt cache, which keeps a subagent's for about five minutes from the start of its last request, and the main session's far longer. Past that point the resume pays full price, where a fresh subagent reads only what the next piece of work needs, from the current files. So resume only to continue the exchange a return has just opened -- answering a NEEDS_CONTEXT, or a question the subagent asked -- and only before anything else is dispatched or run. Everything else, fix rounds and follow-up questions included, goes to a fresh subagent, which takes the earlier work from the brief and the report, with the findings in its dispatch.

**Give each dispatch enough work to carry that cost.** Where pieces of work are ready at the same time and lie in the files one subagent would read anyway, they go in one dispatch: every open finding in one fix, several small changes in one review. Work too small to be worth any dispatch is the controller's to do inline, where the skill lets the controller do that work at all. Batching never merges what a skill keeps apart: the gate between two tasks, the separation of implementer and reviewer, or two writers on one file.

**Keep long waits with the controller.** A subagent that waits on one command past its cache pays, on its next turn, to reload everything it holds, and a turn cannot start until the command returns. So subagents run only unit tests and assertions that finish well inside the cache, under about four minutes. Anything else -- a full suite, a whole-product build, a measurement, or any check that runs longer -- is a long check: the controller runs it, since its own cache lasts far longer. A long check the controller waits on in the foreground has no heartbeat to wake it (Long runs): run it under a time limit the command itself enforces, so that a hung run ends and reports instead of leaving the controller waiting on a notification that never comes; a run that hits the limit has failed. Every dispatch whose subagent runs checks carries the block below, pasted, so that a check that runs long anyway still wakes inside the cache:

---

**Waiting.** Never run a whole suite, a whole-product build, a measurement, or any check your brief or dispatch marks long; those are the controller's. Your context stays cached for about five minutes from the start of each of your turns, and a turn after a longer gap pays to reload all of it. So never wait on one command for more than four minutes: run anything that may take longer in the background, with its output going to a log, and wait on it with a bounded wait -- one that returns when the command ends or after four minutes, whichever comes first -- reading the log's tail between waits. Your system prompt tells you to wait for a background task's notification rather than check on it; for this work that instruction is OVERRIDDEN.

---

## Operating rules

Before the first implementer dispatch, assemble `<workspace>/operating-rules.md`: the agent contract from `${CLAUDE_PLUGIN_ROOT}/shared/agent-contract.md` -- the block between its horizontal rules only, not the file's opening paragraph, which addresses you -- followed by this project's own rules, its testing and environment conventions, the report contract below, the waiting block under Dispatch cost, and whatever the skill adds. The contract is the portable part; the project supplies the rest. Every implementer dispatch carries the operating rules' contents, pasted, and never merely referenced. Reviewers get their constraints from the review blocks and the attention lens the skill hands them instead -- in sdd, the plan's Global Constraints; the report contract in the operating rules is written for an implementer and does not apply to them.

Keep it live. When a task or a review surfaces a fact that binds more than the work it was found in -- a convention, an ordering requirement, a property of the build, how the test harness signals failure -- append it to `operating-rules.md` rather than only carrying it into the next dispatch. Threaded by hand it reaches one implementer; recorded here it reaches every later one without being asked for.

### Report contract

This block goes into the operating rules, pasted, with the report path filled in per dispatch:

---

**Reporting.** Write your full report to the report file named in your dispatch: what you implemented, what you verified with the exact command and its output, the files you created and modified, your self-review findings, and any concerns.

**Where the behaviour under test already exists** -- a port, a refactor, an invariant nobody had asserted -- run its test before you change anything and record the result; an unexpected red there is the most informative event in this workflow. Where the code does not exist yet, skip that run and say so: a missing symbol is not a demonstration that the test discriminates, and staging one costs a build cycle to learn nothing.

**What certifies a test is a deliberate small breakage:** a wrong constant, the wrong branch taken, a step left out, an empty return. Report one line per breakage -- what you broke, which tests went red, which stayed green. A test no breakage can turn red has not been shown to test anything, so a breakage nothing catches is a finding about your tests rather than a footnote, and saying so is more useful than reporting a pass.

**A failing check is never yours to resolve.** Do not delete it, loosen its tolerance, or redesign its fixture to make it pass. Investigate only far enough to say what the red means, then report it under your concerns and leave it failing: the effort spent explaining a failure away reliably exceeds the cost of escalating it, and a real defect talked away is the most expensive outcome this workflow has. Say which of the three it is -- a defect in the code this task owns, a defect in your own test, or a defect in code this task does NOT own. Name the third explicitly: nobody downstream can identify it from your diff, because it is not in it.

If your dispatch carries review findings, APPEND your fix report to the report file it names, after what is already there; never overwrite it or start a new one. Include the covering tests, the command run, and the output.

Then reply with ONLY the following, under fifteen lines, because the detail lives in the report file:

- **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- Files created and modified
- A one-line verification summary
- Your concerns, if any
- The report file path

**Escalating is always available and never counts against you.** Bad work is worse than no work. Stop and escalate when the task needs an architectural decision with several defensible answers; when you need to understand code beyond what you were given and cannot find it; when you have been reading file after file without making progress; or when finishing would mean restructuring something the task did not anticipate. If something is unclear before you start, ask then rather than guessing.

Use DONE_WITH_CONCERNS if you finished the work but have doubts about its correctness. Use BLOCKED if you cannot finish. Use NEEDS_CONTEXT if you need information you were not given. For those last two, put the specifics in the reply itself -- the controller acts on them directly. Never silently produce work you are unsure about.

---

### Implementer statuses

The four statuses route differently, unless the skill says otherwise:

- **DONE** -- dispatch the review the skill requires.
- **DONE_WITH_CONCERNS** -- read the concerns first. Correctness or scope concerns are addressed before review; observations are noted and review proceeds.
- **NEEDS_CONTEXT** -- supply what was missing and re-dispatch (Dispatch cost).
- **BLOCKED** -- assess. A context problem gets more context and the same model; a reasoning problem gets a more capable model; an oversized task gets broken up; a wrong plan escalates to the user. Never force the same model to retry unchanged.

## Workspace and ledger

**Workspace.** Each run owns a directory holding every artifact for that run -- its ledger, operating rules, briefs, reports and review packages -- in the project's scratch area: `Temp/lodestar/<basename>/`, named after the document the run starts from, unless the project's instruction file or the user designates another scratch area. Never a single shared path that every run appends to; that file only grows and stops being readable. Confirm the directory is git-ignored before writing into it -- `git check-ignore <path>` -- since briefs, reports, and review packages otherwise land in the diff the owner has to commit. If it is not ignored, say so and settle the location before dispatching anything.

**Ledger.** Each run keeps one in its workspace: sdd's `progress.md`, the campaign's `ledger.md`, consolidation's `notes.md`, the inline route's `progress.md`. Conversation memory does not survive compaction, and a controller that has lost its place redoes work, or builds on work it has forgotten was retracted. The ledger is the recovery map: trust it over your own recollection. It opens with a standing section carrying what binds the whole run -- the documents it runs from, the answer to the dispatch question, and any hard rules; where these rules name the standing section, a ledger without one uses its head. Append to that section whenever the user issues a directive mid-run -- dated, in their words -- because those bind everything that follows and nothing else records them.

## Long runs

**Heartbeat.** While anything runs in the background -- a run or long check, an agent dispatched without waiting on it, a queue -- keep a recurring wake-up armed, with whatever scheduling the harness provides, at the period the run's governing document names, or every 45 minutes. A period the scheduler cannot express in one entry, such as 45 minutes in cron, takes several entries, registered as one. Between events the controller is idle, and only a notification wakes it; a run that hangs without exiting, or an agent that never hands back, sends none. Each firing does three things, briefly:

1. **Stall check.** For everything running, read its live output against its start time and any time limit it has. Anything with no progress since the previous firing, or past its limit, gets a look at what it is actually doing, not merely whether it is alive -- an idle process looks the same as a busy one to a liveness check. Stop it if it is past its limit or hung, and log the finding.
2. **Context refresh.** Re-read the ledger's standing section and its newest entries, and, if it has not happened since the last compaction, the re-read Compaction requires.
3. **Continue** with the next pending step that does not wait on the user's answer, and reply with one line on where the run stands.

Register the heartbeat in the ledger's standing section, and delete it when the run ends, stops for the user, or has nothing left running in the background. It dies with the session, and with anything that stops background tasks -- a harness restart or update, tasks stopped by hand -- without saying so. After any of these, check the scheduler and re-arm it if it is gone: a dead heartbeat looks exactly like a quiet run.

**Compaction.** The harness writes the compaction summary and keeps what it judges important; only the ledger keeps what the run needs, and a run that waits to be asked depends on the user remembering to, at the moment they are most likely to be leaving. So when the user says they are about to compact, or asks whether this is a good point to, or the context is close to full:

1. **Bring the ledger up to date** with everything the conversation holds that it does not: what is running, with its identifiers and where its output goes; what is next; any result not yet logged; and every directive and decision taken in conversation, in the user's words where they were the user's, dated.
2. **Say whether this is a good point.** It is not while a returned dispatch or a finished run is unlogged, or with an edit half made. Say what to finish first, finish it, and say when it is done.
3. **Give the resume instruction:** the one message to send after compacting, phrased as a continuation rather than a fresh invocation of the skill -- "continue the <skill or inline> run from <ledger path>" -- and what is left armed in the background.

Where the user raised it, wait for them. Where only the context did, carry on once the ledger is current: the harness compacts on its own, and an unattended run does not stop for it.

After a compaction, before anything else, re-read the ledger, the skill's own files, this file and the operating rules: a compaction keeps them only as a summary, the summary drops the rules that bind least often, which are the ones a long run eventually needs, and a controller resuming from it does not know what it dropped. A compaction is not a stop, and a continuation is not a resume: the session, its background work and its heartbeat survive it, so carry on from the ledger. Resuming, below, is for a run whose session ended; run after a compaction, it re-dispatches work that is still running and waits on questions for a user who has left.

## Resuming

A run whose session ended resumes from its ledger, and the skill says how it finds its place there; where it says nothing, its place is the first task the ledger does not record as complete. Three things the ledger cannot settle alone:

- **The baseline** is not a clean tree: the run's own output is expected in it -- that is the point of resuming. The baseline is the set of files the ledger accounts for, as the skill defines it; anything `git status --porcelain` shows beyond that set is unaccounted for: report it and let the user say whether it belongs before going on.
- **The stop.** If the previous run stopped, the user resolved whatever stopped it, if at all, in a conversation you cannot see: wait for them to state that resolution rather than inferring one from the ledger's account of the problem.
- **The last gate.** A gating result recorded just before the run halted is the one result least safe to take on trust: check it, as the skill says, before anything builds on it; where the skill says nothing, re-run it.
