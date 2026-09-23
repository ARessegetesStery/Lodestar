---
name: lodestar-sdd
description: Use when an approved spec or plan is ready to execute through per-task subagents, or when a spec needs an implementation plan written from it.
---

# Lodestar: Spec-Driven Development

This is the Codex entry point for Lodestar's canonical SDD skill. Before acting, read and follow `../../../skills/sdd/SKILL.md` in full, along with any resources it directs you to read. That file is authoritative.

## Codex compatibility

The Lodestar repository root is three directories above this file. When the canonical skill refers to `/lodestar:<skill>`, use the matching Codex skill name: `$lodestar-<skill>`. When it refers to `${CLAUDE_PLUGIN_ROOT}`, substitute that repository root. Use Codex subagents and other native tools while preserving the canonical skill's constraints and outcomes.

The canonical helpers `task-brief` and `review-package` are bash scripts; run them exactly as the canonical skill gives them, with the repository root substituted. On Windows, run them with Git for Windows' bash: the `bash.exe` in the `bin` folder of the Git installation, beside the `cmd` folder that holds `git.exe` -- typically `C:\Program Files\Git\bin\bash.exe`. From PowerShell, a bare `bash` usually resolves to `C:\Windows\System32\bash.exe`, the WSL launcher, which fails outright where no Linux distribution is installed and otherwise runs the script inside Linux, where the Windows paths it is given do not resolve. Git for Windows' bash accepts Windows paths as given, and the helpers need Git installed in any case. From PowerShell, invoke it with the call operator: `& "C:\Program Files\Git\bin\bash.exe" "<repository root>\skills\sdd\scripts\task-brief" PLAN_FILE N OUTFILE`.
