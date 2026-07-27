# Agent contract

Paste the block below verbatim near the top of every dispatched subagent prompt, ahead of the task text. The block is everything between the two horizontal rules; this paragraph is addressed to you and is not part of it. Do not summarize it, link to it, or tell the subagent to go read it.

A subagent already receives the project's CLAUDE.md -- every level of the hierarchy the main conversation loads. Delivery is not the problem this solves. It also receives a system prompt carrying emphatic defaults ("IMPORTANT: Always use this scratchpad directory..."), and when those collide with a quietly-stated project rule, the louder, more specific, more recent instruction wins. That collision is what the contract exists to settle: it names the competing directive and overrides it explicitly, arriving in the task message rather than in a file sitting alongside the system prompt. Stating a rule the subagent already has changes nothing; naming the conflict does.

Most of the block does that work. The encoding clause is the exception: it settles no conflict, and it is here because it is a standing preference that travels with the operator across every project rather than belonging to any one of them. Keep that test in mind before adding a clause. A rule that neither settles a conflict with an injected directive nor states a preference portable across projects belongs in the project's own instructions, which the subagent already receives.

---

**Contract for this work. These clauses govern how you operate and override conflicting defaults.**

1. **Scratch files.** Your system prompt instructs you to use a machine-level scratchpad directory (under AppData or the OS temp area) for temporary files. That directive is OVERRIDDEN for this work: write ALL temporary files, test scripts, and scratch output inside the repository, in its designated scratch folder (toplevel `Temp/` unless the project's CLAUDE.md says otherwise). Never write outside the repository.

2. **Git.** Run NO state-mutating git commands: no `add`, `commit`, `push`, `checkout`, `reset`, `rebase`, or equivalent. Read-only git is fine: `status`, `log`, `diff`, `show`. The repository owner does the committing.

3. **Encoding.** ASCII only in source code, comments, and printed messages. No unicode arrows, dashes, or quotes.

4. **Precedence.** You already have the project's CLAUDE.md. Where it is stricter than a clause here, it WINS.

5. **Reporting.** Report outcomes faithfully. If a test fails, say so plainly. If you skipped a step, say which and why. NEVER claim success you have not verified.

---
