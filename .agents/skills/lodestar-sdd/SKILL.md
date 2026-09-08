---
name: lodestar-sdd
description: Use when an approved spec or plan is ready to execute through per-task subagents, or when a spec needs an implementation plan written from it.
---

# Lodestar: Spec-Driven Development

This is the Codex entry point for Lodestar's canonical SDD skill. Before acting, read and follow `../../../skills/sdd/SKILL.md` in full, along with any resources it directs you to read. That file is authoritative.

## Codex compatibility

The Lodestar repository root is three directories above this file. When the canonical skill refers to `/lodestar:<skill>`, use the matching Codex skill name: `$lodestar-<skill>`. When it refers to `${CLAUDE_PLUGIN_ROOT}`, substitute that repository root. Use Codex subagents and other native tools while preserving the canonical skill's constraints and outcomes.

The canonical helper commands use Bash. In a Codex environment without Bash, run the equivalent PowerShell helpers in this skill folder: `scripts/task-brief.ps1` for `task-brief`, and `scripts/review-package.ps1` for `review-package`. Their arguments and output contracts match the canonical helpers.
