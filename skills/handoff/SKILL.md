---
name: handoff
description: Use when work continues in another session or under another agent; drafts a self-contained prompt the user can hand to the next executor.
disable-model-invocation: true
---

# Handoff

## Purpose

Produce a prompt that stands alone. Its reader has zero context from this conversation and may be a different model. Everything the executor needs to act correctly has to be in the prompt, or reachable from a path named in it.

The work being handed off can be anything: a half-finished investigation, a stretch of inline edits, a process partway through. Assume no particular artifact exists, and name what does.

## Gather first

From this session, and from what is on disk:

- What is done and verified, against what is pending. Keep the two apart; do not let "written" pass as "verified".
- The decisions made, each with its one-line reason. Give particular weight to the ones the user made in conversation: those exist nowhere else, and losing them is how a continuation quietly re-opens a settled question.
- The path of every artifact the executor will need, whatever kind it is -- documents produced, working files, records of what has happened so far.
- The immediate next step.

## Prompt structure to produce

In this order:

1. **Context reload.** An ordered list of the files the executor must read first, by path, including the relevant project docs and project memory.
2. **The task.** What to do, the precise scope, and the explicit non-goals.
3. **Constraints.** The agent contract, pasted verbatim, plus any project rules that are stricter. It lives at `${CLAUDE_PLUGIN_ROOT}/shared/agent-contract.md` -- that placeholder resolves to this plugin's install directory, so it is not a path in the user's project. Paste the fenced block only, not the file's opening paragraph, which addresses you rather than the executor.
4. **Process.** Any procedure the executor should follow and where it is written down. Name a skill only where one actually applies; most handoffs do not need one.
5. **Success criteria.** Including the exact verification commands.
6. **Reporting expectations.** What the executor reports when it is done, and where that goes: the path of the file to write the full record to, and what the reply itself must carry -- what was done, what was verified and with which command, what remains, and any concerns. Name the destination. "Report back" with no path produces a message that disappears with the session.

## Writing rules for the produced prompt

- No conversation shorthand. No "as discussed", no "the file we talked about".
- Absolute dates only, never "yesterday" or "last session".
- Everything named by path.
- Assume the executor cannot see this session and cannot ask you a question.

## Delivery

Output the prompt in a single fenced block so the user can copy it whole. Then offer to write it to `docs/lodestar/handoff/YYYY-MM-DD-topic-handoff.md`. That is the default; a location or naming convention stated by the project or by the user overrides it.
