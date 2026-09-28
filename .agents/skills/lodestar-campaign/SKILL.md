---
name: lodestar-campaign
description: Use when the answer is not known in theory and has to be found by experiment; settle a self-contained charter with the user, then run the experiments unattended to a report for consolidation.
---

# Lodestar: Campaign

This is the Codex entry point for Lodestar's canonical campaign skill. Before acting, read and follow `../../../skills/campaign/SKILL.md` in full, along with any resources it directs you to read. That file is authoritative.

## Codex compatibility

The Lodestar repository root is three directories above this file. When the canonical skill refers to `/lodestar:<skill>`, use the matching Codex skill name: `$lodestar-<skill>`. When it refers to `${CLAUDE_PLUGIN_ROOT}`, substitute that repository root. When the canonical skill, or the agent contract it pastes into a prompt, refers to the project's CLAUDE.md, read the project's AGENTS.md in its place, and paste the contract with that substitution. Use Codex subagents and other native tools while preserving the canonical skill's constraints and outcomes.

The canonical skill builds its implementation review packages with the SDD helper `review-package`, a bash script; run it exactly as the canonical skill gives it, with the repository root substituted. On Windows, run it with Git for Windows' bash: the `bash.exe` in the `bin` folder of the Git installation, beside the `cmd` folder that holds `git.exe` -- typically `C:\Program Files\Git\bin\bash.exe`. From PowerShell, a bare `bash` usually resolves to `C:\Windows\System32\bash.exe`, the WSL launcher, which fails outright where no Linux distribution is installed and otherwise runs the script inside Linux, where the Windows paths it is given do not resolve. From PowerShell, invoke it with the call operator: `& "C:\Program Files\Git\bin\bash.exe" "<repository root>\skills\sdd\scripts\review-package" OUTFILE PATH`.
