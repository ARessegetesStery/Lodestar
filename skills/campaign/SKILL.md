---
name: campaign
description: Use when the answer is not known in theory and has to be found by experiment; settles a self-contained charter with the user, runs the experiments unattended, and on the user's go-ahead closes with a report that lodestar:consolidate turns into production code.
disable-model-invocation: false
---

# Campaign

## Purpose

For work whose answer cannot be derived and has to be measured: which of several methods holds up, why something fails, whether an idea works at all. It is the second route out of `lodestar:brainstorming`, beside `lodestar:design`. Design suits work that is clear in theory: the spec fixes what to build, and execution conforms to it. A campaign suits work that is not: the charter fixes the question and the rules of the search, and the answer is the output.

A campaign runs in two phases. The **charter phase** is a discussion with the user that ends in a charter file. The **autopilot phase** runs the experiments from that file unattended, reports back, and on the user's go-ahead runs the closing pass to a closing package. `lodestar:consolidate` then takes the package and, with the user, decides what of the campaign's code is kept, and writes the spec that turns it into production code.

Everything the campaign builds is shaped by that successor: its code, its record and the rulings it takes on the user's behalf are all written for consolidation to decide on.

If the question turns out to be answerable in theory, say so and recommend `lodestar:design` instead. If the idea has not taken shape -- the question itself is still open -- recommend `lodestar:brainstorming`.

## Entry points

- **No charter.** Run the charter phase. It ends when the charter is written and cold-read, and the user has been asked about compacting.
- **A charter path.** Read `${CLAUDE_PLUGIN_ROOT}/skills/campaign/autopilot.md` in full, then run the autopilot phase from the charter. If the charter's ledger already exists, this is a resume: see Resuming in that file.

## Charter phase

### Investigate

Read enough to write a bar that can be checked: the code the question lives in, the records of earlier work on it, the measurements that already exist and the instruments that produced them. The bound is the same as `lodestar:design`'s: what the question references, plus the area it touches. Where the reading shows the question is already answered, or cannot be answered with what exists, say so before drafting anything.

### Settle the charter

The charter has the sections below. Work out what the reading settles, and batch everything else into one numbered message: never one question at a time, and only what the reading cannot settle. Prefer concrete options where the choice has a natural set.

1. **Question.** What the campaign must answer, in a sentence or two, and why it is being asked now.
2. **Starting state.** The commit the campaign starts from; what is already known, each item with the path where it is recorded; the reference numbers the bar compares against, with where and how they were measured. A campaign that continues one whose result raised a new question instead of something to consolidate starts from that campaign's checkpoint, and names its report here; the two are then consolidated together.
3. **Bar.** The pass and fail criteria of each outcome the campaign can reach, each one a measurement on named inputs with a number, or a pass/fail observation defined precisely enough that two readers would agree on it. Name the configuration that should fail each criterion -- normally the starting code -- and predict that it does: the autopilot runs it first, and a bar never seen failing is not evidence (the reasoning is the testing decision's in `${CLAUDE_PLUGIN_ROOT}/skills/design/SKILL.md`). List separately what is reported beside the bar but does not gate it. A criterion may also be a rule that derives its target from an earlier result in the same campaign -- the second question's target set by the first's answer. Applying the rule is then not a change to the bar: the autopilot records the value it derives as a provisional ruling, and runs the derived criterion on the starting code, as the red run was, before measuring anything against it. Name, too, any stop condition: a result on which the campaign ends early, whatever time is left.
4. **Replication.** A draw is one run of a configuration from a fresh start. Where results vary from draw to draw, the concluded tier (Claim tiers, below) needs two draws; name the scatter margin an effect has to clear to count, in the bar's units. A pass/fail criterion has no margin: it is replicated when it passes on every draw, and the report gives the pass counts, since a pass on three draws of three can still fail the fourth. Where the method is deterministic, say so and show how inspection establishes it -- which sources of run-to-run variation exist, and why none of them is active -- and the concluded tier then needs one draw.
5. **Moves allowed.** What the autopilot may change -- files, subsystems, parameters, instruments -- and what is off limits. How experiments are gated in this project: the mechanism that keeps every experimental change off by default. Where the charter names none, the autopilot uses the lightest mechanism the project already has, such as an environment variable read once or a compile-time definition, and adds no configuration key unless this section permits one (the full gating rules are under Experiments in `autopilot.md`). Whether it may add configuration surface, touch shared components, or change existing tests; changing a test to make it pass is never among the moves.
6. **Decision scope.** Which decisions the autopilot takes alone, and which it parks for the user (Decisions, below). Changing the bar -- beyond applying a rule the bar itself states -- extending the budget, and anything section 5 puts off limits are always the user's; say what else is.
7. **Budget.** Wall-clock time for the experiments, as a duration from the autopilot's start. The closing pass -- concluding draws, the closing review, and the durable records -- is outside it: the loop's end presents its plan and an estimate sized from measured costs (Go-ahead, in `autopilot.md`), since a closing time guessed before any run is the usual reason a campaign ends without its concluding draws.
8. **Run protocol.** How experiments are run in this project: concurrency limits, isolation between runs, the provenance to record per run, the environment settings that make runs comparable, the traps known to cost time, and the command that runs the project's test suite where it has one -- the tier of it the setup and closing pass run, where the suite has tiers. Say too whether reviewers may re-run what they review, and which runs: a run that takes hours, or has to run alone for clean timing, may not be a reviewer's to launch, and the autopilot then launches it itself in a slot the protocol allows. Where the project keeps this in a document, name it and add only what this campaign needs beyond it; where it keeps none, write it out here.
9. **Deliverables.** The report path, the ledger path, and the durable records the project expects beyond them -- memory, documentation -- written once, for the campaign as a whole. Defaults, and the rule for durable records, under Layout.
10. **Starting hypotheses.** What the discussion suspects, each with the measurement that would test it and the predicted result. These are a queue, not findings; the autopilot may reorder, drop and add to them.

Present the charter in the conversation as a whole before writing it. Wait for approval; if the user asks for changes, revise and present again.

### Write it to stand alone

A context compaction, or a fresh session, very likely separates this conversation from the autopilot. The charter is then the only channel between them, so it has to carry everything the autopilot needs, and nothing it needs can be left in this conversation's context. Beyond the rule every campaign file follows (Layout):

- The user's directives in their own words, dated.
- Every claim about the current state named by path, and dated.

End the file with an empty **Amendments** section. The autopilot appends to it, dated, whenever the charter changes mid-run; the original text is never rewritten, so the charter always shows both what was asked and what it became.

Write it to the charter path (Layout). Self-review it once for placeholders, contradictions, and anything a reader with no context would have to ask about, and fix what you find.

### Cold read

Dispatch one reviewer to read the charter cold: that file, and only the paths it names. Ask it for every point at which it would have to ask the author a question before it could run this campaign unattended; every criterion that rests on no number or cannot fail; and every move or decision whose scope a reasonable reader could take two ways. This is the charter's one test of standing alone, and its author is the reader least able to perform it. It is not a gate: fix what comes back and carry on. Name the model on the dispatch; the tiering policy is under Model selection in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/SKILL.md`.

### Hand over

Ask the user to review the file. Then tell them the charter is written to stand alone, and ask them to judge whether this conversation's context should be compacted, or a fresh session started, before the autopilot begins with `/lodestar:campaign <charter path>`. The discussion that produced the charter is now the largest thing in context, and the one thing the autopilot does not need. Tell them too that the charter may be committed before the autopilot starts or left uncommitted: the start check accepts either, and nothing else in the tree may be outstanding.

Tell them too that the run stops at the loop's end for their go-ahead before the closing pass.

Then stop. If the user tells you to start without compacting, start the autopilot phase exactly as if newly invoked with the charter path: read the charter back from the file, not from recollection, so that the run is governed by what the file says.

## Autopilot phase

The autopilot's rules are in `${CLAUDE_PLUGIN_ROOT}/skills/campaign/autopilot.md`, read in full when the skill is invoked with a charter. The charter phase does not read that file; this outline is here so that the charter is written knowing the run it sets up.

1. **Start.** One message while the user is still present: the dispatch question, the baseline check, the workspace, and a pre-flight scan of the charter. Nothing else is asked until the loop ends.
2. **Setup.** The workspace; the clock, which turns the charter's budget into a deadline; the ledger; a copy of the starting code, kept for comparison; runs that measure its noise and re-measure the bar's references here; the operating rules every implementer receives; the suite baseline; and the red run, which shows the bar can fail.
3. **The loop.** A queue of hypotheses, re-planned after every result. Each experiment is chosen, briefed with a prediction written before it runs, implemented behind a switch, reviewed, run and read. Claims climb the tiers through numbers reviews, and decisions follow the rules below. The loop ends when the question is answered on reviewed claims, when a stop condition the charter states is met, when the queue is empty and re-planning finds nothing left to test, when everything left depends on a parked question, at the deadline, or when the environment fails.
4. **Go-ahead.** The results, parked questions, and the closing pass's plan and estimate, reported in the conversation; the user chooses more experiments or the close.
5. **Closing pass.** Inside the approved estimate: the concluding draws, the report (drafted while they run), the project's durable records, the closing review, the identity check and the test suite on the final code, the account, and the wrap-up.
6. **Finish.** The user checkpoints the campaign's state with `/lodestar:commit-plan`, which gives its code the `exp:` prefix, and then runs `/lodestar:consolidate` on the report.

A resume re-enters from the ledger, with a resume check in place of the start message.

## Claim tiers

Every claim the campaign makes about the question has an ID in the ledger's claims table, and one of these tiers:

- **Observation** -- a number was seen in a run. It says what happened, not what it means.
- **Indicative** -- a reading of one or more observations, from one draw, with its scatter unknown, on code that has passed its implementation review.
- **Reviewed** -- survived a numbers review (Reviews, in `autopilot.md`): its numbers re-derived from the raw output, one run it rests on re-run, and the compared runs shown to differ only in what the claim says they differ in. Where no re-run fits the run protocol and the budget, the claim is promoted on the rest alone and marked "not re-run" wherever its tier is shown, so that consolidation can see which reviewed claims were never reproduced.
- **Concluded** -- reviewed, and replicated on the final code under the charter's replication rule: two draws of every configuration it compares, each clearing the scatter margin or, for a pass/fail criterion, passing; or one draw where the charter establishes determinism. Two draws check that a result was not a lucky draw; they do not estimate scatter, which is why the margin is the charter's to set.
- **Retracted** -- withdrawn by a dated log entry saying why. Nothing is deleted.

What a claim may be used for depends on its tier, and this is what makes the tiers worth keeping:

- An indicative claim may steer exploration: which hypothesis to test next, which configuration to try.
- Only a reviewed claim may ground a recommendation in the report, or a provisional ruling.
- Only a concluded claim may appear among the report's conclusions.

One exception runs the other way: a recommendation to discard an abandoned experiment may rest on indicative claims, labelled as such. Discarding is cheap to reverse -- the code stays in the checkpoint -- while keeping is what ships, so the evidence bar sits on keeping. Requiring a numbers review for every idea the campaign dropped would spend the budget on the ideas that mattered least.

The failure this guards against is a claim that runs ahead of its evidence and steers several experiments before a review catches it. The review arrives either way; the tier makes the claim's standing visible at every point it is used, so that what rested on it can be found when it moves.

That is why a retraction propagates. When a claim is retracted or demoted, the same log entry lists everything that rested on it -- provisional rulings, recommendations, later claims, queued experiments -- and each of those is re-marked in its own section.

Promote a claim only through a log entry naming the evidence. Never write a claim more strongly than its tier allows: "X fixes Y" is concluded language, and said of an indicative claim it is false.

Replication is the expensive part, so the concluding draws are normally run in the closing pass, on the final code, for the claims the report will conclude on. Run them earlier only when the answer is already in hand.

## Decisions

**Within scope.** Take the decision and record it as a provisional ruling: an ID, the decision, the alternatives set aside, the reviewed claims it rests on, and the result that would reverse it. It governs the rest of the run; consolidation is where the user ratifies or rejects it. Choosing the next hypothesis, the shape of an experiment, and which items to recommend keeping are not rulings: they are the work, and the log records them. A reading that departs from the charter's letter is not the work, even when it is taken in the middle of implementing: it is a provisional ruling, or a parked question where it is outside scope. Recorded as the work, it is a departure the user never sees. A ruling that interprets the charter rests on the charter's text, quoted, in place of claims.

**Outside scope.** Park it in the parked questions section, with what it blocks, and carry on with work that does not depend on it. Stop only when everything left depends on a parked question, and then end the loop. Never take a parked decision because it would unblock the run, and never stop the run to ask it: the user is not there to answer, and the go-ahead at the loop's end delivers it.

**Directives mid-run.** When the user does speak during the run, record the directive in the ledger's standing section, verbatim and dated, with your reading of it beside it, marked as awaiting their ratification. The reading governs until they correct it. A directive that changes any charter section -- the bar, the replication rule, the scope, the budget, the moves -- is also appended to the charter's Amendments section, dated, with the claims, predictions and queue items it voids. A changed bar is run on the starting code, as the red run was, before anything is measured against it. A reading silently widened into a new target is how a run ends up answering a question nobody asked.

## Layout

Defaults, each overridden by a location the project or the user states:

- Charter: `docs/lodestar/campaign/YYYY-MM-DD-topic-charter.md`, tracked.
- Report: `docs/lodestar/campaign/YYYY-MM-DD-topic-report.md`, tracked.
- Workspace and ledger: `Temp/lodestar/<charter-basename>/ledger.md`, scratch and git-ignored.
- Wrap-up: `docs/lodestar/wrap-up/YYYY-MM-DD-topic-wrap-up.md`, tracked.

**The campaign's records** are its charter, report and wrap-up, the durable records its closing pass writes, and every script the report cites, copied to where the project keeps scripts. They are tracked, and they are not the campaign's code: the checks that look for changes outside the manifest set them aside.

**The durable records** are written once, in the closing pass, for the campaign as a whole: its memory entry, and the documentation the project's own rules require for what the campaign changed. No experiment gets a record or a memory entry of its own. The report accounts for every experiment, with the ledger as the depth behind it; and a result written up before the closing pass can still be demoted or retracted, after which a separate record of it goes on stating what the campaign no longer claims. Where the project's rules ask for a record or a memory entry per task, the whole campaign is the task.

**Every file the campaign writes** -- charter, ledger, report, records -- is written for a reader with no conversation context: no conversation shorthand, no "as discussed" and no "as above"; absolute dates and times; everything named by path, and names to search for rather than line numbers; no paragraph broken across lines.

The ledger is scratch, so consolidation's cold reviewer can read it only on the machine the campaign ran on. The report is written to stand without it for that reason; the ledger is the depth behind it.
