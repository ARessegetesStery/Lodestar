---
name: lodestar-handoff
description: Use when work continues in another session or under another agent; draft a self-contained prompt the user can hand to the next executor.
---

# Lodestar: Handoff

This is the Codex entry point for Lodestar's canonical handoff skill. Before acting, read and follow `../../../skills/handoff/SKILL.md` in full. That file is authoritative.

## Codex compatibility

The Lodestar repository root is three directories above this file. When the canonical skill refers to `/lodestar:<skill>`, use the matching Codex skill name: `$lodestar-<skill>`. When it refers to `${CLAUDE_PLUGIN_ROOT}`, substitute that repository root. When the canonical skill, or the agent contract it pastes into a prompt, refers to the project's CLAUDE.md, read the project's AGENTS.md in its place, and paste the contract with that substitution. Use Codex-native tools while preserving the canonical skill's constraints and outcomes.
