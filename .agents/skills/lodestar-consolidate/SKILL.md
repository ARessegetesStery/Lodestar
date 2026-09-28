---
name: lodestar-consolidate
description: Use after lodestar-campaign, once its state is checkpointed; have the campaign's results reviewed cold, settle whether they are ready or need a chained campaign first, then take the user's keep-or-discard ruling on each change, and write the spec that turns the kept ones into production code.
---

# Lodestar: Consolidate

This is the Codex entry point for Lodestar's canonical consolidate skill. Before acting, read and follow `../../../skills/consolidate/SKILL.md` in full, along with any resources it directs you to read. That file is authoritative.

## Codex compatibility

The Lodestar repository root is three directories above this file. When the canonical skill refers to `/lodestar:<skill>`, use the matching Codex skill name: `$lodestar-<skill>`. When it refers to `${CLAUDE_PLUGIN_ROOT}`, substitute that repository root. When the canonical skill, or the agent contract it pastes into a prompt, refers to the project's CLAUDE.md, read the project's AGENTS.md in its place, and paste the contract with that substitution. Use Codex subagents and other native tools while preserving the canonical skill's constraints and outcomes.
