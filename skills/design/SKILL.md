---
name: design
description: Use when the intent is settled but the design is not; investigates the codebase and returns a concrete design, then writes it to a spec.
disable-model-invocation: true
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
- **Error and edge cases.** Walk them deliberately: invalid input, absent or malformed state, boundary values, failure of anything the code depends on, and concurrent or repeated invocation where those apply. Name the ones the tests cover and the ones they do not, with why. A short honest list beats a claim of full coverage.

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
3. **Architecture.** The shape of the solution, plus the decisions that were genuinely open -- ones where a reader could reasonably have expected the other answer -- each with the alternative considered and the reason for the choice.
4. **Components.** Each unit: what it does, its interface, what it depends on, and the files it lives in by path.
5. **Data flow.** How information moves between the components, and the states it passes through.
6. **Error handling.** The failure modes, what happens in each, and what surfaces to the user.
7. **Testing.** The testing decision written out concretely: coverage and level, framework and test paths, exact commands, the predicted outcome of each criterion with its numbers, and the error and edge cases both covered and deliberately not.
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

Where the recommendation is inline, say that the finished work still gets one review dispatch before the user reads it: the task review block from `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md`, with this spec standing in for a task brief and a package built over the files the change touched. Inline is the cheaper route, not the unreviewed one.

**Say whether the work owes a standalone report.** The wrap-up that closes an sdd run is four capped sections about the session, not a place findings go; work whose deliverable is knowledge rather than code -- an investigation, a measurement campaign, a stage gate someone decides against later -- owes a document that outlives the session and is read by someone who was never in it. Decide it here for the reason the testing decision is decided here: a report commissioned at the end gets fitted to whatever happened to be measured, where one named now makes the design produce what the report will have to state. Where a report is called for, say what question it answers and where it lives by path, and put that line in the spec -- a decision held only in this conversation does not reach a plan written in another session -- so an sdd run carries it as a task in the plan rather than prose after the last one. Where none is, say so: the spec and the code are the record.

Then stop. Do not invoke any other skill without the user's go-ahead.
