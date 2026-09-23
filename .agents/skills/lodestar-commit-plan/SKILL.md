---
name: lodestar-commit-plan
description: Use when the user asks how to commit the uncommitted working tree; decide whether it is one commit or several and return the git commands for the user to run, without running git itself.
---

# Lodestar: Commit plan

This is the Codex entry point for Lodestar's canonical commit-plan skill. Before acting, read and follow `../../../skills/commit-plan/SKILL.md` in full. That file is authoritative.

## Codex compatibility

The Lodestar repository root is three directories above this file. When the canonical skill refers to `/lodestar:<skill>`, use the matching Codex skill name: `$lodestar-<skill>`. When it refers to `${CLAUDE_PLUGIN_ROOT}`, substitute that repository root. Use Codex-native tools while preserving the canonical skill's constraints and outcomes.

The canonical skill is invoked only on the user's request; `agents/openai.yaml` in this folder disables implicit invocation to match.
