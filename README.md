# Lodestar

A Claude Code plugin holding a small set of development-process skills: work out what to build, turn it into a spec -- or, where the answer has to be found by experiment, run a campaign and consolidate what it finds into one -- execute the spec through fresh-context subagents with review between them, and close out a session honestly.

## Compatibility

**Claude Code and Codex.** Claude Code loads the canonical skill files as a plugin. Codex discovers the corresponding entry points under `.agents/skills/`; each entry point loads the same canonical file and resolves `${CLAUDE_PLUGIN_ROOT}` against this repository. The original Claude Code files remain the source of truth. The SDD helpers are bash scripts on both hosts; on Windows, Codex runs them through Git for Windows' bash.

## The skills

In Claude Code, every skill but `commit-plan` carries `disable-model-invocation: false`, so each one can be reached by slash command -- `/lodestar:design` and so on -- or by the model loading it itself when the work at hand matches the skill's description. In Codex, use `$lodestar-design`, `$lodestar-sdd`, and the other `lodestar-*` names, or let Codex select them from their descriptions. `commit-plan` is a helper rather than a process step, so it runs only when you invoke it: `disable-model-invocation: true` in Claude Code, and `allow_implicit_invocation: false` in its Codex `agents/openai.yaml`. None of them chains into another without you saying so -- with one exception: `sdd` and `campaign` produce the `wrap-up` report themselves when a run completes, since they run unattended and that report cannot be reconstructed once the session is gone.

- **`/lodestar:brainstorming`** -- Explores an idea that has not taken shape yet and converges on a direction, without writing a spec.
- **`/lodestar:design`** -- Investigates the codebase against a settled intent, returns a concrete design, and writes it to a spec.
- **`/lodestar:campaign`** -- For a question only experiment can answer. Settles a self-contained charter with you -- the question, the bar, the moves allowed, the time budget, the decisions it may take alone -- then runs the experiments unattended from that charter to a report, with claims graded by the evidence behind them.
- **`/lodestar:consolidate`** -- Follows a checkpointed campaign. Has its results reviewed cold and settles with you whether they are ready to consolidate or need a chained campaign first; once ready, takes your keep-or-discard ruling on each change and each ruling the campaign took on your behalf, and writes the spec that turns the kept changes into production code.
- **`/lodestar:sdd`** -- Executes an approved spec or plan through per-task subagents, with a fresh reviewer after each task and a whole-branch review at the end. Also runs plan-only.
- **`/lodestar:handoff`** -- Drafts a self-contained prompt that a later session, or a different agent, can pick the work up from.
- **`/lodestar:wrap-up`** -- Reports what is still uncertain, what you may be overlooking, what changed without being asked, and the state a fresh session needs to review the work cold.
- **`/lodestar:commit-plan`** -- Decides whether the uncommitted working tree is one commit or several, and gives the commands for you to run: subject lines in the repository's own convention, no body, no attribution. Invoked only by you.

## Suggested workflow

```
           (optional) brainstorming           direction
                         |
          +--------------+--------------+
          |                             |
   clear in theory               needs experiment
          |                             |
          |                         campaign      charter, then unattended run to a report
          |                             |
          |                       commit-plan     exp: checkpoint
          |                             |
       design                     consolidate     rulings, spec
          |                             |
          +--------------+--------------+
                         |
                +--------+--------+
                |                 |
             inline              sdd   plan, per-task review, final review
                |                 |
                +--------+--------+
                         |
                      wrap-up          uncertainties, blind spots, side changes, continuation context
                         |
           (optional) handoff          prompt for the next session
```

1. **`brainstorming`**, when the question is still what to build or whether to. Skip it whenever the shape is already clear. It ends by recommending `design` or `campaign`, or dropping the idea.
2. **`design`**, once the intent is settled and the answer is clear in theory. It ends by recommending one of the two execution routes and then stops.
3. **`campaign`**, when the direction is set but whether or how it works has to be found by experiment. Invoked with nothing, it discusses the question with you and writes a charter that stands alone, then asks whether to compact before the run. Invoked with the charter, it runs unattended to a report, a wrap-up, and experimental code left in the tree behind switches that are off by default.
4. **`commit-plan`, then `consolidate`**, after a campaign. You commit the campaign's state as a checkpoint -- `commit-plan` gives its code the `exp:` prefix -- and `consolidate` has the results reviewed cold and asks whether they are ready. If they raised a new question instead, it sends you back to `campaign` for a chained campaign, and the chain is consolidated as a whole when it ends. Once ready, it takes your ruling on each change and writes the spec for the kept ones, recommending an execution route as `design` does.
5. **Inline or `sdd`.** A bounded, mechanical change whose context you already hold goes inline; multi-task, parallelizable, or output-heavy work goes to `sdd`. Either route gets one review dispatch before you read the result -- inline is the cheaper path, not the unreviewed one.
6. **`wrap-up`**, before you review or commit. It reports the complement of a completion summary: what a run leaves unresolved rather than what it produced. After the `sdd` route it runs on its own and lands in `docs/lodestar/wrap-up/`; after the inline route you invoke it. Its last section briefs a cold session -- what shipped, where it lives in git, the decisions taken, what is verified -- so the morning after an unattended run you can open a fresh agent on the file instead of reloading a stale conversation; a full standalone prompt is still `handoff`'s job.
7. **`handoff`**, when the work outlives the session. Also useful earlier, to park a second idea `brainstorming` set aside or a subsystem `design` decomposed out of scope.

Each step stops when it is done and recommends the next. None of them advances without your go-ahead, save for the `sdd` and `campaign` wrap-ups noted above.

The long runs -- `sdd`, the `campaign` autopilot, `consolidate`, and the inline route out of `design` -- open by asking which models to dispatch: the tiering policy under Model selection in `skills/sdd/SKILL.md`, or models you name. Models change faster than the policy does, and the answer is recorded where a resumed run reads it rather than asking again.

## Supporting files

`shared/agent-contract.md` holds the subagent contract: the block pasted verbatim into every dispatched subagent prompt, and into the prompts `handoff` produces. It is the mechanism by which rules that must beat emphatic injected directives travel in the same channel as those directives. It sits outside `skills/` because several skills use it and none owns it.

Inside `sdd`, `skills/sdd/reviewer-prompt.md` carries the three review dispatch blocks -- task, fix round, whole branch -- and `skills/sdd/scripts/` holds two bash helpers: `review-package`, which builds a path-scoped review package from an uncommitted working tree, and `task-brief`, which extracts one task's text from a plan. Claude Code resolves these through `${CLAUDE_PLUGIN_ROOT}`. Codex entry points resolve the same references from the repository root and run the same bash scripts. On Windows the SDD entry point directs Codex to Git for Windows' `bash.exe` rather than a bare `bash`, which from PowerShell usually resolves to the WSL launcher.

Inside `campaign`, `SKILL.md` holds the charter phase and the definitions the charter sets -- claim tiers, decision rules, layout -- and `skills/campaign/autopilot.md` holds the autopilot phase, read only when the skill is invoked with a charter, so the discussion that writes a charter does not carry the autopilot's rules. `skills/campaign/ledger-skeleton.md` is the layout the autopilot copies into its ledger -- state sections updated in place, and an append-only dated log -- and `skills/campaign/reviewer-prompt.md` carries its three review blocks: an experimental change, claims about to be promoted, and the closing report. Its implementation reviews build their packages with `sdd`'s `review-package`, so the campaign entry point carries the same Windows note. Inside `consolidate`, `skills/consolidate/reviewer-prompt.md` carries the opening review block: a cold, read-only reading of the campaign's record that runs nothing.

## Install

From this repository, which doubles as a single-plugin marketplace:

```
/plugin marketplace add ARessegetesStery/Lodestar
/plugin install lodestar@arias-stery
```

Marketplace installs are cached, so after the source changes run `/plugin update lodestar` (or `/plugin marketplace update arias-stery`) to pick it up.

For iterating on the skills themselves, load the directory live instead, which skips the cache entirely:

```
claude --plugin-dir /path/to/Lodestar
```

## Use with Codex

Open this repository in Codex. Codex scans `.agents/skills` between the current working directory and the repository root, so the Lodestar skills are available automatically. Invoke a skill with `$lodestar-brainstorming`, `$lodestar-design`, `$lodestar-campaign`, `$lodestar-consolidate`, `$lodestar-sdd`, `$lodestar-handoff`, `$lodestar-wrap-up`, or `$lodestar-commit-plan`; Codex can also select any but `$lodestar-commit-plan` when its description matches the task.

The Codex entry points load the canonical files in `skills/`, so there is one set of process instructions for both hosts. The SDD helpers need bash, which Git for Windows provides wherever Git itself is installed.

The version is declared in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; a release bumps the two together.

## Maintenance principle

Rules are added only in response to an observed failure, never preemptively. A rule written for a problem nobody has hit yet costs attention on every run and earns nothing back. Before extending the toolkit, check that the addition answers a failure that actually happened.

Skills are project-independent. Anything that holds for one project -- its paths, tools, domain vocabulary, run procedures, model names -- belongs in that project's instruction file or documents, which a skill tells the agent to load, and never in the skill text. Where a skill names a default, such as `Temp/` or `docs/lodestar/`, the project overrides it. The test for a sentence: would it still be true of a project in another language and another domain? A rule learned on one project passes only once it has been restated so that it would.

## License

MIT. See `LICENSE`.
