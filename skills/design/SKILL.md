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

Do this before investigating in depth, so that effort is not spent refining a design that needs to be split first.

If the brief spans several independent subsystems, say so immediately rather than designing all of it. Help the user decompose: name the independent pieces, how they relate, and what order they should be built in. Then design the first piece through the rest of this skill. Each piece gets its own spec. Only make the split when the brief involves large changes and indeed span multiple subsystems: do not split if they just cover different modules of the same subsystem.

For the pieces not being designed now, offer `lodestar:handoff` to capture each as a self-contained prompt, so the decomposition survives this conversation instead of living only in it.

## Investigate

- Read the code, docs, plans, and specs the brief references, plus the surrounding code the change will touch. Those references are the bound on the reading: enough to check the design against what is actually there.
- Establish how the codebase already does this kind of thing. The design follows the existing pattern unless there is a reason to break it, and the reason gets stated in the design.
- Flag inconsistencies with the codebase or with existing plans and specs.
- Flag gaps: unaddressed cases, undefined behavior, missing verification.
- Flag simpler alternatives where one exists.

Where investigation shows the intent cannot work as stated -- it conflicts with something already in the codebase, or depends on something that is not there -- stop and say so plainly instead of designing around it. This is not re-opening the intent; it is reporting that the premise does not hold, which the user needs before deciding what to do next.

Where code you are touching has a problem that affects this work -- a file that has grown too large, a tangled responsibility, an unclear boundary -- fold a targeted improvement into the design, the way a careful developer improves code they are already working in. Refactoring unrelated to the goal stays out.

## Shape the design

**Cut what the goal does not need.** Drop speculative features, unused configurability, and extension points nobody asked for, from every approach you propose and from the design you land on. When you cut something the brief gestured at, say you cut it and why, rather than dropping it silently.

**Design in units that can be understood separately.** Each unit gets one clear purpose and a defined interface. For each one you should be able to answer: what does it do, how is it used, and what does it depend on. If a consumer has to read a unit's internals to use it, or if changing those internals would break consumers, the boundary needs work. Smaller, focused files are also easier to implement against and to review, so a unit that is growing to cover several purposes is a signal to split it.

## Testing decision

This is the implementation's completion criterion: without it there is no explicit standard for whether the work passed or failed. Settle it while the design is still moving, so the design can change in response; settled afterward, tests get fitted to whatever was built.

Work out and then present, as its own numbered section of the design:

- **What is covered.** Which behaviors get automated tests, and at which level -- unit at a named boundary, integration across a named seam, end-to-end through a named entry point.
- **What form.** The framework, where the tests live by path, and the exact command that runs them.
- **What passing means.** What a green run looks like, and what completion of the work therefore gates on.
- **Whether it will pass.** Predict each criterion's outcome before the work exists; where it turns on a quantity, put a number on it and show the number clears. A criterion you cannot predict, or whose outcome turns on something this work does not produce, is not a completion criterion for this work -- and that is a design finding, not a gap to paper over.
- **Error and edge cases.** Walk them deliberately rather than asserting coverage in general terms: invalid input, absent or malformed state, boundary values, failure of anything the code depends on, and concurrent or repeated invocation where those apply. Name the ones the tests will cover, and name the ones they will not along with why. A short honest list beats a claim of full coverage.

Where the choice is genuinely open, present it as a decision with options. Where the project's conventions already settle it, state what they settle and move on.

Not every change is usefully gated on a test. A configuration edit, a documentation change, or a throwaway probe may not be. Where that is the case, say so and say why, rather than inventing a test to fill the section; the question gets answered on purpose either way.

## Question policy

- Batch all open questions into one numbered message. Never ask one at a time.
- Ask only what investigation cannot settle.
- Prefer concrete options over open prompts where the choice has a natural option set.
- If the answers raise follow-ups, batch those too.

## Presentation

- Present the design in the conversation, before writing any file. The spec is written up from a design the user has already approved; it is not the vehicle for showing them one.
- Present it at once, organized into whatever sections the design naturally has, each sized to its content. The eight-section structure below governs the written spec, not this conversation.
- Where the design is large, splitting the presentation across several messages is fine for readability. That is a formatting choice, not an approval gate: no section-by-section sign-off.
- Wait for approval before writing anything. If the user asks for changes, revise and present again.

## Writing the spec

After the user approves the design, write it to `docs/lodestar/spec/YYYY-MM-DD-topic-spec.md`. That is the default; a location or naming convention stated by the project or by the user overrides it.

### Spec structure

These sections, in this order. Size each to its content. Where one genuinely does not apply, keep the heading and say in a line why it does not, so a reader can tell the difference between "considered and not applicable" and "forgotten".

1. **Goal.** What this builds and why, in a sentence or two.
2. **Context.** The state of the code today: the relevant files by path, the existing patterns this design follows, and the constraints the current code imposes.
3. **Architecture.** The shape of the solution, plus the design decisions that were open, each with the alternative considered and the reason for the choice.
4. **Components.** Each unit: what it does, its interface, what it depends on, and the files it lives in by path.
5. **Data flow.** How information moves between the components, and the states it passes through.
6. **Error handling.** The failure modes, what happens in each, and what surfaces to the user.
7. **Testing.** The testing decision, written out concretely: what is covered and at what level, the framework and test paths, the exact commands, the predicted outcome of each criterion with the numbers behind it, and the error and edge cases -- both those covered and those deliberately not.
8. **Non-goals.** Adjacent work a reader would plausibly assume is included, stated as excluded, each with a one-line reason or the name of what owns it instead. Only things someone could reasonably have assumed; exclusions nobody would have expected are padding.

Write the whole spec for a reader with no conversation context: no shorthand, absolute dates, everything named by path.

The spec has to be reviewable against the code. Every claim it makes about the current state -- what a file contains, what pattern exists, what constrains the work -- names the path where that claim can be checked, so a reviewer can verify the design against the repository rather than take it on trust.

### Self-review

Then self-review the written spec once, checking for:

- Placeholders and unresolved TODOs.
- Internal contradictions.
- Requirements that are ambiguous to a reader with no conversation context.
- Scope creep beyond what the user approved.

Fix what you find inline. Then dispatch one reviewer to read the written spec cold, for those same four checks plus the one you cannot perform on your own work: any claim about how the system will behave that rests on no number. A spec can be flawlessly self-consistent about a false premise -- asserting it in three places reads as settling it -- so consistency checking rewards it, and the author is the worst-placed reader to catch that. Tell it to flag only what would cause a real problem later, and to leave wording preferences alone. This is not a gate -- act on what comes back and carry on.

Name the model explicitly on this dispatch and on the review in Terminal state below, since an omitted model inherits this session's; the tiering policy is under Model selection in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/SKILL.md`.

Then ask the user to review the file.

Never stage or commit the spec, or anything else. The project's rules govern committing.

## Terminal state

End with a one-line recommendation: inline implementation, or `lodestar:sdd`.

- A bounded, mechanical change whose context you already hold favors inline.
- Multi-task, parallelizable, or output-heavy work favors sdd.

Give the reason in the same line.

Where the recommendation is inline, say that the finished work still gets one review dispatch before the user reads it: the task review block from `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md`, with this spec standing in for a task brief and a package built over the files the change touched. Inline is the cheaper route, not the unreviewed one.

Then stop. Do not invoke any other skill without the user's go-ahead.
