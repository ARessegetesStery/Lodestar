---
name: handoff
description: Use when work continues in another session or under another agent; drafts a self-contained prompt the user can hand to the next executor.
disable-model-invocation: false
---

# Handoff

## Purpose

Produce a prompt that stands alone. Its reader has zero context from this conversation and may be a different model. Everything the executor needs to act correctly has to be in the prompt, or reachable from a path named in it.

The work being handed off can be anything: a half-finished investigation, a stretch of inline edits, a process partway through, or a body of work that has been decided on but not started. Assume no particular artifact exists, and name what does.

## Gather first

A handoff either continues work already underway or kicks off work that has only been decided on. Which one it is changes what has to be gathered.

For a continuation:

- What is done and verified, against what is pending. Keep the two apart; do not let "written" pass as "verified".

For a kickoff, where nothing is done yet:

- The state of the thing being changed, and why the work is being taken up now. Gather only the few facts that motivate the task and bound its scope. The rest is the executor's to read.

For both:

- The decisions made, each with its one-line reason. Give particular weight to the ones the user made in conversation: those exist nowhere else, and losing them is how a continuation quietly re-opens a settled question.
- What is still open, gathered separately from what is settled. A decision the executor has to make is not a gap in the handoff; leaving it indistinguishable from a settled one is.
- The path of every artifact the executor will need, whatever kind it is -- documents produced, working files, records of what has happened so far.
- The immediate next step.

## What to leave out

Anything reachable from a file in the context reload list. That list is a pointer, not a summary to be expanded.

This is the main way a handoff grows without getting better: the reading list and the task description end up doing the same job, and the content that exists nowhere else gets diluted by content the executor was about to read anyway. The division that prevents it -- the context reload list carries everything a file can carry, and the rest of the prompt carries only what no file carries: the decisions taken in conversation, the scope, the non-goals, the open questions, and the next step.

Project rules are the common case of getting this wrong. The executor already receives the project's CLAUDE.md, at every level of the hierarchy the main conversation loads. Restating its rules changes nothing.

## Prompt structure to produce

In this order:

1. **Context reload.** An ordered list of the files the executor must read first, by path, including the relevant project docs and project memory. Say what each one is for, in a clause.
2. **The task.** What to do, the precise scope, and the explicit non-goals. Where a non-goal contradicts something the executor is being sent to read -- an audit that ranks it urgent, a document that calls it a gap -- say so, and say the decision supersedes it. Otherwise the executor helpfully undoes it.
3. **Decisions and open questions.** The settled decisions with their reasons, and separately the questions the executor has to answer. Mark which is which.
4. **Constraints.** The agent contract, pasted verbatim. It lives at `${CLAUDE_PLUGIN_ROOT}/shared/agent-contract.md` -- that placeholder resolves to this plugin's install directory, so it is not a path in the user's project. Paste the fenced block only, not the file's opening paragraph, which addresses you rather than the executor. Add a project rule alongside it only where an injected default points the other way and you can name the directive it conflicts with. If you cannot name the conflict, the rule does not belong here.
5. **Process.** Any procedure the executor should follow and where it is written down. Name a skill only where one actually applies; most handoffs do not need one.
6. **Success criteria.** Including the exact verification commands.
7. **Reporting expectations.** What the executor reports when it is done, and where that goes: the path of the file to write the full record to, and what the reply itself must carry -- what was done, what was verified and with which command, what remains, and any concerns. Name the destination. "Report back" with no path produces a message that disappears with the session.

## Writing rules for the produced prompt

- No conversation shorthand. No "as discussed", no "the file we talked about".
- Absolute dates only, never "yesterday" or "last session".
- Everything named by path.
- Anchor on names, not line numbers. A handoff is read later by definition, and line numbers decay fastest in exactly the files the work is about to change. Name the function, class, or a string to search for. Give a line number only as a secondary hint, marked approximate.
- Date every claim about current state, so a stale one can be recognized as stale rather than trusted.
- Assume the executor cannot see this session and cannot ask you a question.

## Delivery

Write the prompt to `docs/lodestar/handoff/YYYY-MM-DD-topic-handoff.md`. That is the default; a location or naming convention stated by the project or by the user overrides it. Then give the user the path and what to run against it.

Show the prompt in the conversation as well only when it is short enough to be read there. A long one belongs on disk, where the user can review it in an editor and hand over a path rather than a wall of text -- and pasting it into the conversation stops working as soon as the prompt itself contains a fenced block.
