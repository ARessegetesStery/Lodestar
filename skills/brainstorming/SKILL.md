---
name: brainstorming
description: Use before design when the idea has not taken shape yet; explores the problem and converges on a direction, without writing a spec.
disable-model-invocation: false
---

# Brainstorming

## Purpose

For an idea that has not taken shape yet. Something should be built; what it is, is the open question. Once the direction is settled, `lodestar:design` takes it from there. This stage is optional, and skipping it is right whenever the shape is already clear.

The idea turning out not to be worth building is one of the outcomes, not the purpose.

## Focus the conversation

If what the user brought is really several ideas, say so and settle which one this conversation is about. A brainstorm spread across three ideas converges on none. The rest are not lost: name them, and offer `lodestar:handoff` to capture any worth keeping as a self-contained prompt, so they outlive this conversation instead of ending with it.

## Understand the background

Read enough of the project to discuss the idea concretely: what already exists in the area it would live in, what conventions govern that area, what has changed there recently. Stop when you could describe that area to someone else.

- This is orientation, not a survey of the codebase.
- Where the reading shows the project already does this, or rules it out, say so straight away. That is the cheapest outcome a brainstorm can have. Most of the time it will show neither, which is not a reason to keep reading.
- Read shallowly first, and go deeper only where the conversation lands. Depth spent before the idea has a shape is the kind that gets thrown away.

## State the problem

Before approaches can exist, the problem has to be stated. Work it out from the background where that settles it, and from the user where it does not:

- **Purpose.** What changes, and for whom, if this exists.
- **Constraints.** What it has to live within, and what it must not break.
- **Success.** What the finished thing would have to do for the user to call it done -- concrete enough to recognize.

An idea that cannot yet answer these does not need approaches proposed at it. It needs these answered first, and saying so is more useful than filling the gap with options.

## Converge

- Propose 2-3 approaches with a recommendation, but only where a choice is genuinely open. Do not manufacture alternatives for points the user has already settled.
- Say plainly when the idea does not look worth building, and why. Ending a brainstorm with "do not do this" is a complete result.

## Question policy

- Batch all open questions into one numbered message. Never ask one at a time.
- Ask only what the reading cannot settle.
- Prefer concrete options over open prompts where the choice has a natural option set.
- If the answers raise follow-ups, batch those too.

## Presentation

- Present the whole picture at once, as numbered sections sized to their content.
- No section-by-section approval rounds. The user reacts to it as a whole.

## Terminal state

End with where the thinking landed and a one-line recommendation: drop it, keep exploring, or take it to `lodestar:design`. The last is the right call as soon as the direction is concrete enough to implement against -- including when that turns out to be true early, in which case say so and stop rather than continuing to explore a question that is already answered.

This stage produces a direction, not artifacts. Write no spec, no code, and no files in the project unless the user asks. Then stop, and do not invoke another skill without the user's go-ahead.
