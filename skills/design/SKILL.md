---
name: design
description: Use when the intent is settled but the design is not; investigates the codebase and returns a concrete design, then writes it to a spec.
disable-model-invocation: false
---

# Design

## Purpose

The user knows what they want built. The design they bring may be rough, vague, or only partly formed. Your job is to investigate the codebase and return something concrete enough to implement against.

Do not re-open the intent. Where the brief settles something, it is settled: ask nothing it already answers, and propose no alternatives to points the user has already decided. Where the brief is vague, prefer resolving it against what the code actually does over asking.

If the intent itself turns out to be unsettled -- the question is still what to build, or whether to -- say so and recommend `lodestar:brainstorming` instead of designing past it.

## Scope check

Do this before investigating in depth.

Split only when the brief spans several independent subsystems. Different modules of one subsystem are not a split; neither is a brief that is merely large. When it does split, say so immediately rather than designing all of it: name the independent pieces, how they relate, and what order they should be built in, then design the first piece through the rest of this skill. Each piece gets its own spec.

For the pieces not being designed now, offer `lodestar:handoff` to capture each as a self-contained prompt, so the decomposition survives this conversation.

## Investigate

- Read the code, docs, plans, and specs the brief references, plus the surrounding code the change will touch. Those references are the bound on the reading.
- Establish how the codebase already does this kind of thing. The design follows the existing pattern unless there is a reason to break it, and the reason gets stated in the design.
- Flag inconsistencies with the codebase or with existing plans and specs.
- Flag gaps: unaddressed cases, undefined behavior, missing verification.
- Flag simpler alternatives where one exists.

Where investigation shows the intent cannot work as stated -- it conflicts with something already in the codebase, or depends on something that is not there -- stop and say so plainly instead of designing around it. That is reporting a broken premise, not re-opening the intent.

Where code you are touching has a problem that affects this work -- a file grown too large, a tangled responsibility, an unclear boundary -- fold a targeted improvement into the design. Refactoring unrelated to the goal stays out.

## Shape the design

**Cut what the goal does not need.** Drop speculative features, unused configurability, and extension points nobody asked for. When you cut something the brief gestured at, say you cut it and why.

**Design in units that can be understood separately.** Each unit gets one clear purpose and a defined interface: what it does, how it is used, what it depends on. If a consumer has to read a unit's internals to use it, or if changing those internals would break consumers, the boundary needs work. A unit growing to cover several purposes is a signal to split it.

## Testing decision

This is the implementation's completion criterion. Settle it while the design is still moving, so the design can change in response; settled afterward, tests get fitted to whatever was built.

Work out and then present, as its own numbered section of the design:

- **What is covered.** Which behaviors get automated tests, and at which level -- unit at a named boundary, integration across a named seam, end-to-end through a named entry point.
- **What form.** The framework, where the tests live by path, and the exact command that runs them.
- **What passing means.** What a green run looks like, and what completion of the work therefore gates on.
- **Whether it will pass.** Predict each criterion's outcome before the work exists; where it turns on a quantity, put a number on it and show the number clears. A criterion you cannot predict, or whose outcome turns on something this work does not produce, is not a completion criterion for this work -- that is a design finding, not a gap to paper over. Spend the prediction where it can be wrong: a criterion that follows from the code being written at all -- a guard clause guards, an empty input returns empty -- is asserted, not predicted.
- **Whether it can fail.** For each criterion, name the configuration under which it goes RED, and run it once where the thing it checks already exists. A criterion never observed failing is not evidence: a green reading is equally consistent with the check being structurally unable to report the failure at all. Do not count a test-first red as that evidence: absent code fails on a missing symbol, which shows only that the check RUNS, and a wholly stubbed implementation routinely leaves part of a criterion set green. A red discriminates only against code that is PRESENT and wrong -- by a bad value or under a bad input; against absent code it shows nothing. No check is exempt: one authored alongside or after what it measures is green from birth, and telemetry has no red phase in its lifecycle at all. The falsifying configuration takes one of two shapes and the criterion decides which: where some input exhibits the failure, it is a one-line edit of an existing fixture or scene; where the property holds on EVERY legal input -- which is what an invariant is -- no input reds it, and the red is a deliberate break of the implementation, run once and reverted. Name which one in the spec so the next reader can re-run it.
- **Whether anything covers it at all.** Once per design, not per criterion: name the mechanism this work exists to install and the one break that disables it, then run the WHOLE suite against that break. The bullet above examines only criteria that already exist, so nothing in it can report that nothing anywhere covers the deliverable. A green suite is the finding, and names the gate this design still owes.
- **Error and edge cases.** Walk them deliberately: invalid input, absent or malformed state, boundary values, failure of anything the code depends on, and concurrent or repeated invocation where those apply. Name the ones the tests cover and the ones they do not, with why. A short honest list beats a claim of full coverage.
- **What only a person can check.** Name the part of acceptance that no command settles -- a judgement, a comparison, an operation the suite cannot perform on its own -- and write it as a procedure: what the person does, in what order, what they are looking for, and roughly how long it takes. A design that leaves this implicit ships a completion criterion nobody has agreed to perform, and the work then sits finished but unaccepted for as long as it takes someone to reconstruct what to run.

Not every change is usefully gated on a test. A configuration edit, a documentation change, or a throwaway probe may not be. Say so and say why rather than inventing a test to fill the section.

## Question policy

- Batch all open questions into one numbered message. Never ask one at a time.
- Ask only what investigation cannot settle.
- Prefer concrete options over open prompts where the choice has a natural option set.
- If the answers raise follow-ups, batch those too.

## Presentation

- Present the design in the conversation, before writing any file. The spec is written up from a design the user has already approved; it is not the vehicle for showing them one.
- Present it at once, organized into whatever sections the design naturally has. The eight-section structure below governs the written spec, not this conversation.
- Splitting a large presentation across several messages is a formatting choice, not an approval gate: no section-by-section sign-off.
- Wait for approval before writing anything. If the user asks for changes, revise and present again.

## Writing the spec

After the user approves the design, write it to `docs/lodestar/spec/YYYY-MM-DD-topic-spec.md`. A location or naming convention stated by the project or by the user overrides that default.

### Spec structure

These sections, in this order. Where one genuinely does not apply, keep the heading and say in a line why, so a reader can tell "considered and not applicable" from "forgotten".

1. **Goal.** What this builds and why, in a sentence or two.
2. **Context.** The state of the code today: the relevant files by path, the existing patterns this design follows, and the constraints the current code imposes.
3. **Architecture.** The shape of the solution, plus the decisions that were genuinely open (ones where a reader could reasonably have expected the other answer), with each the reason for the choice, and the alternative where there was a reasonable one. List those decisions most-expensive-to-reverse first. Expensive meaning a later change would propagate through interfaces, stored formats, or work already built on top, so a reviewer who stops early has read the ones that matter.
4. **Components.** Each unit: what it does, its interface, what it depends on, and the files it lives in by path.
5. **Data flow.** How information moves between the components, and the states it passes through.
6. **Error handling.** The failure modes, what happens in each, and what surfaces to the user.
7. **Testing.** The testing decision written out concretely: coverage and level, framework and test paths, exact commands, the predicted outcome of each criterion with its numbers, the falsifying configuration that turns each criterion red, the break that disables this work's central mechanism and what the whole suite did against it, the part of acceptance only a person can perform, and the error and edge cases both covered and deliberately not.
8. **Non-goals.** Adjacent work a reader would plausibly assume is included, stated as excluded, each with a one-line reason or the name of what owns it instead. Exclusions nobody would have expected are padding.

Write for a reader with no conversation context: no shorthand, absolute dates, everything named by path. Every claim about the current state -- what a file contains, what pattern exists, what constrains the work -- names the path where it can be checked, so the spec is reviewable against the repository rather than on trust.

### Keeping it tight

**Cap each section at 300 words.** Sections that enumerate -- Components, Error handling, Testing -- apply the cap per entry, since their length is set by how many units the design has.

Four things eat the budget without adding a constraint. A section that will not fit is almost always carrying one of them:

- **Defending a settled choice.** Which directory a file goes in, a naming convention, a default nobody would contest: state it. Writing a rejected alternative for it manufactures a decision that was never in doubt.
- **Restating an argument.** No-conversation-context means nothing is left implicit, not that each section stands alone. Establish a load-bearing claim once and cross-reference it after.
- **Narrating history.** No "an earlier draft said", no "this was previously X", no account of what a review changed. The reader is implementing from this document and cannot act on a version that no longer exists. One exception: a superseded value that still exists somewhere the reader may find it -- a number in a sibling document, a stale comment in the code -- earns one sentence saying not to use it and where it lives.
- **Explaining a rule twice.** If the second clause of a sentence restates the first, delete it.

### Self-review

Self-review the written spec once for:

- Placeholders and unresolved TODOs.
- Internal contradictions.
- Requirements ambiguous to a reader with no conversation context.
- Scope creep beyond what the user approved.

Fix what you find inline. Then dispatch one reviewer to read the spec cold, for those four checks plus the one you cannot perform on your own work: any claim about how the system will behave that rests on no number. A spec can be flawlessly self-consistent about a false premise, so consistency checking rewards it and the author is the worst-placed reader to catch it. Tell the reviewer to flag only what would cause a real problem later and to leave wording preferences alone. This is not a gate -- act on what comes back and carry on.

Name the model explicitly on this dispatch and on the review in Terminal state below; an omitted model inherits this session's. The tiering policy is under Model selection in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/SKILL.md`.

Then ask the user to review the file.

Never stage or commit the spec, or anything else. The project's rules govern committing.

## Terminal state

End with a one-line recommendation, with the reason in the same line: inline implementation, or `lodestar:sdd`.

- A bounded, mechanical change whose context you already hold favors inline.
- Multi-task, parallelizable, or output-heavy work favors sdd.

Where the recommendation is inline, say that two obligations still attach; inline is the cheaper route, not the unplanned or unreviewed one.

- **It begins with a written plan.** Before any code is touched, the implementing session writes an inline ledger -- the counterpart of sdd's plan phase -- at `Temp/lodestar/<spec-basename>/progress.md` (the same scratch convention as sdd's workspace; a location designated by the project's CLAUDE.md or the user overrides it), first line `# Inline ledger -- spec: <spec file path>`, and presents it for the user's review, waiting for their go-ahead before implementation starts. It states, dated: every ruling taken since the spec was written, in the user's words where it was theirs; what inline-with-dispatch means concretely for this work -- which work the main agent keeps and which is dispatched, each dispatch with its model named (tiering policy under Model selection in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/SKILL.md`); an ordered task list with its gates, kept current as tasks complete; and the disposition of every open question the spec carries -- ruled, pending, or deferred -- so none is decided silently by the implementation. It is working scratch, not a record: durable conclusions go to the project's own records, never only here.
- **The finished work still gets one review dispatch before the user reads it:** the task review block from `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md`, with this spec standing in for a task brief and a package built over the files the change touched.

**Say whether the work owes a standalone document.** The wrap-up that closes an sdd run is five sections about the session -- four of them capped, and the fifth a briefing for whoever picks the work up cold -- so it reports on the run, not on what the run produced. Work whose result has to outlive the session and be read by someone who was never in it owes a document of its own. Two kinds of work do:

- **Work whose deliverable contains knowledge besides code** -- an investigation, a measurement campaign, a stage gate someone decides against later. It owes a report: the comparisons, the numbers, and what they settle.
- **Work whose acceptance needs a person to perform it.** Where the testing decision's "What only a person can check" bullet runs past a few lines, that list is its own document: an acceptance procedure, the ordered steps someone follows to decide whether the work is done.

Decide it now, for the reason the testing decision is settled early: a document commissioned at the end gets fitted to whatever the work happened to produce, while one named in advance makes the work produce what the document will have to state.

Where one is owed, the spec carries a line of its own: what question the document answers, and the path it lives at. That line belongs in the spec and not only in this conversation, because a plan written in a later session reads the spec -- and an sdd run then carries the document as a task rather than as prose after the last one. Where none is owed, say so: the spec and the code are the record.

Then stop. Do not invoke any other skill without the user's go-ahead.
