# Lodestar

A Claude Code plugin holding a small set of development-process skills: work out what to build, turn it into a spec, execute the spec through fresh-context subagents with review between them, and close out a session honestly.

## Compatibility

**Claude Code only.** The skills are built on Claude Code plugin conventions -- `SKILL.md` frontmatter, `disable-model-invocation`, and `${CLAUDE_PLUGIN_ROOT}` path resolution -- and no other agent harness is supported or tested. The two helper scripts under `skills/sdd/scripts/` are bash, so a bash-capable shell has to be available; on Windows the one shipped with Git for Windows is enough.

## The skills

Every skill carries `disable-model-invocation: true` and is therefore invoked by slash command only -- `/lodestar:design` and so on. The model cannot load one on its own, and none of them chains into another without you saying so -- with one exception: `sdd` produces the `wrap-up` report itself when a run completes, since it runs unattended and that report cannot be reconstructed once the session is gone. Work where this process is not explicitly asked for falls to whatever other skills are installed.

- **`/lodestar:brainstorming`** -- Explores an idea that has not taken shape yet and converges on a direction, without writing a spec.
- **`/lodestar:design`** -- Investigates the codebase against a settled intent, returns a concrete design, and writes it to a spec.
- **`/lodestar:sdd`** -- Executes an approved spec or plan through per-task subagents, with a fresh reviewer after each task and a whole-branch review at the end. Also runs plan-only.
- **`/lodestar:handoff`** -- Drafts a self-contained prompt that a later session, or a different agent, can pick the work up from.
- **`/lodestar:wrap-up`** -- Reports what is still uncertain, what you may be overlooking, and what changed without being asked.

## Suggested workflow

```
  (optional) brainstorming     direction
                 |
              design           spec
                 |
        +--------+--------+
        |                 |
     inline              sdd   plan, per-task review, final review
        |                 |
        +--------+--------+
                 |
              wrap-up          uncertainties, blind spots, side changes
                 |
   (optional) handoff          prompt for the next session
```

1. **`brainstorming`**, when the question is still what to build or whether to. Skip it whenever the shape is already clear.
2. **`design`**, once the intent is settled. It ends by recommending one of the two execution routes and then stops.
3. **Inline or `sdd`.** A bounded, mechanical change whose context you already hold goes inline; multi-task, parallelizable, or output-heavy work goes to `sdd`. Either route gets one review dispatch before you read the result -- inline is the cheaper path, not the unreviewed one.
4. **`wrap-up`**, before you review or commit. It reports the complement of a completion summary: what a run leaves unresolved rather than what it produced. After the `sdd` route it runs on its own and lands in `docs/lodestar/wrap-up/`; after the inline route you invoke it.
5. **`handoff`**, when the work outlives the session. Also useful earlier, to park a second idea `brainstorming` set aside or a subsystem `design` decomposed out of scope.

Each step stops when it is done and recommends the next. None of them advances without your go-ahead, save for the `sdd` wrap-up noted above.

## Supporting files

`shared/agent-contract.md` holds the subagent contract: the block pasted verbatim into every dispatched subagent prompt, and into the prompts `handoff` produces. It is the mechanism by which rules that must beat emphatic injected directives travel in the same channel as those directives. It sits outside `skills/` because two skills use it and neither owns it.

Inside `sdd`, `skills/sdd/reviewer-prompt.md` carries the three review dispatch blocks -- task, fix round, whole branch -- and `skills/sdd/scripts/` holds two bash helpers: `review-package`, which builds a path-scoped review package from an uncommitted working tree, and `task-brief`, which extracts one task's text from a plan. Skills reference all of these through `${CLAUDE_PLUGIN_ROOT}`, which Claude Code substitutes with the plugin's install directory.

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

The version is declared in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`; a release bumps the two together.

## Maintenance principle

Rules are added only in response to an observed failure, never preemptively. A rule written for a problem nobody has hit yet costs attention on every run and earns nothing back. Before extending the toolkit, check that the addition answers a failure that actually happened.

## License

MIT. See `LICENSE`.
