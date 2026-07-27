# Reviewer prompts

Three blocks to paste when dispatching a review: one for a task, one for a fix round, one for the whole branch at the end. Each block is everything between its horizontal rules; this paragraph and the notes between blocks address you, not the reviewer.

Fill every `[BRACKETED]` slot before dispatching, except where a block marks one as omittable. `[GLOBAL CONSTRAINTS]` is the plan's Global Constraints section copied verbatim -- exact values, exact formats, and the stated relationships between components. It is the reviewer's attention lens, so a paraphrase weakens it.

Where the work was done inline rather than task by task, there is no plan behind it and no implementer report. Three parts of the task review block assume both, and all three come out for an inline review: the report line, the Global Constraints heading with its block, and the paragraph on not re-running the implementer's tests. Each is marked below. The block is otherwise unchanged.

Do not add "do not flag X" or "at most Minor" to any of them. Pre-judging a finding to spare yourself a fix round is the failure these reviews exist to catch; raise it, then adjudicate it.

## Task review

---

You are reviewing one piece of completed work -- a single task from a plan, or a change made in one sitting. Report two verdicts: whether the work does what was required of it, and whether its quality is acceptable. Both are required; a report missing either is incomplete.

**Read these first.**

- Requirements: `[BRIEF_FILE -- the task brief, or the spec itself where the work was done inline rather than task by task]`
- The implementer's report: `[REPORT_FILE, or omit this line for an inline review, where no implementer report exists]`
- The change under review: `[REVIEW_PACKAGE_FILE]`

The review package contains the status of the paths under review, a diffstat, a `git diff -U10` of modified files, and the full contents of new files. Nothing is committed in this repository, so the package is scoped by path rather than by commit range.

**These constraints bind the task. Check the work against them specifically.**

[GLOBAL CONSTRAINTS -- omit this heading and this block for an inline review, where there is no plan to take them from]

**What to check.**

- Requirements: everything the brief asked for is present, and nothing beyond it was added.
- Correctness: the code does what it claims, including its edge and error cases.
- Verification: the tests or checks the brief named exist and genuinely exercise the behaviour rather than asserting on mocks or restating the implementation. Test each one against a deliberate small breakage -- a wrong constant, the wrong branch taken, a step left out, an empty return -- and say so where no test would fail for any of them, because a test that cannot fail is not coverage. Warnings and stray output in the reported run are findings in their own right: a green summary hides a deprecation warning or a silently skipped test just as easily as it reports a pass.
- Quality: names say what things do, the structure follows the surrounding code, and there is no duplication or dead surface introduced.
- Scope: nothing was restructured or refactored beyond what the task called for.
- Where the change reaches them, and only then: whether it opens a security hole, whether existing callers or stored data still work, and whether a change to stored formats can be rolled out safely. Say nothing about these where the change does not touch them.

**Grade every finding.**

- **Critical** -- breaks correctness, or fails a stated requirement of the task.
- **Important** -- a real defect that should be fixed before the work is used.
- **Minor** -- cosmetic, stylistic, or a matter of preference.

**A defect the brief itself demanded is still a defect.** If the requirement you are checking against is the thing that is wrong, say so and grade it Important, labelled plan-mandated. A plan does not get to grade its own work, and the user decides which governs.

**Where you cannot tell.** Some requirements live in code the package does not show, or span several tasks. Do not crawl the codebase at large -- but reading outside the package is warranted to check one concrete risk you can name, one focused check per risk. A change to a shared signature, an API contract, or shared mutable state is exactly such a risk, so checking its call sites is a finding waiting to be made rather than something to defer. What you still cannot settle goes under "Cannot verify from the package" with what you would need; do not guess and do not assume the worst. The controller holds the cross-task context and resolves those.

**Do not re-run the implementer's tests.** Its report carries that evidence. Judge whether what it ran was the right thing and whether the output supports the claim. [Omit this paragraph for an inline review, where there is no report and the tests in the package are judged by reading them.]

**Stay read-only on the code under review.** Do not edit the files in the package. Writing scratch probes is expected and useful -- put them in the repository's designated scratch area, and never outside the repository.

**Report in this form.**

    ## Task review

    **Requirements:** MET | NOT MET
    - [if NOT MET, what is missing or wrong, one line each]

    **Quality:** APPROVED | CHANGES NEEDED

    **Findings**
    - [Critical|Important|Minor] path:line -- [what is wrong, and why it matters]

    **Cannot verify from the package**
    - [requirement, and what would be needed to check it]

    **Strengths:** [one or two lines, or omit]

---

## Re-review of a fix round

Dispatch this after a fix round. The package is regenerated over the same paths, so it shows the whole task again rather than only the fix -- which is why this block scopes the review by findings instead of by diff.

---

You are re-reviewing a fix. A previous review raised the findings below; the implementer has since amended the work. Your job is to verdict each finding, not to review the task again.

**Read these first.**

- Requirements: `[BRIEF_FILE, or the plan and spec paths when the fix wave followed the final review rather than one task]`
- The implementer's report, including its appended fix report: `[REPORT_FILE, or omit this line if the fix wave produced no per-task report]`
- The current state of the change: `[REVIEW_PACKAGE_FILE]`

**The open findings.**

[FINDINGS LIST, VERBATIM FROM THE PREVIOUS REVIEW]

**For each finding**, return ADDRESSED or NOT ADDRESSED, with the path and line where you verified it. ADDRESSED means the defect is gone, not that an attempt was made.

**Beyond the findings**, report only breakage the fix itself introduced, graded Critical or Important. The package shows the entire task, so you will see code that was already reviewed and accepted -- do not re-litigate it. Anything else you notice goes in the last section as an observation; it will be recorded, and it will not reopen this task.

**Report in this form.**

    ## Re-review

    - [finding, abbreviated] -- ADDRESSED | NOT ADDRESSED (path:line) -- [one line]

    **New breakage introduced by the fix:** none | [Critical|Important] path:line -- [what]

    **Verdict:** all findings addressed | [N] still open

    **Observations (not blocking):**
    - [anything else noticed, or omit]

---

## Final whole-branch review

Dispatch this once, after the last task, on the most capable model available. Its value is the defects that per-task reviews structurally cannot see, so the block leads with those rather than repeating the task rubric.

---

You are reviewing a completed body of work as a whole. Every task in it has already passed its own review, so the defects worth your attention are the ones no single-task review could have seen: the ones that live between tasks, or in the aggregate.

**Read these first.**

- The plan every task was built from: `[PLAN_FILE]`
- The specification it implements, which governs on any conflict with the plan: `[SPEC_FILE, or omit this line if there is none]`
- The complete change: `[REVIEW_PACKAGE_FILE]`
- The running record, including findings deferred or parked during execution: `[LEDGER_FILE]`

**These constraints bind the whole body of work.**

[GLOBAL CONSTRAINTS]

**Look first for what per-task review cannot catch.**

- Interfaces that each task got right on its own but that do not line up with each other -- a name, signature, or type that drifted between the task that produced it and the task that consumed it.
- The same logic written twice in two different tasks, neither of which could see the other.
- A requirement of the spec that no single task owned, and that therefore no task review could have missed.
- Scaffolding, shims, or temporary paths from an early task that a later task superseded and left behind.
- Constraints that hold within each task but drift across the whole: naming, formats, error handling, structure.
- Whether the work as assembled actually does what the spec set out to do, as opposed to satisfying each task in turn.
- Where the work reaches them: security holes opened across task boundaries, existing callers or stored data broken by the combination, and whether a change to stored formats can be rolled out safely. Say nothing about these where the work does not touch them.

**Then re-examine what execution set aside.** The ledger lists findings recorded as Minor and deferred, and findings parked at the fix cap with a ruling. For each, say whether you agree. A deferred Minor that is really Important, or a parked ruling that does not hold up now that the whole is visible, is worth more than a fresh finding -- it means something already got through.

**Grade every finding.**

- **Critical** -- breaks correctness, or fails a stated requirement of the spec.
- **Important** -- a real defect that should be fixed before this work is used.
- **Minor** -- cosmetic, stylistic, or a matter of preference.

**On verification.** The per-task reports carry what was run and its output. Do not re-run them. If you believe the assembled work needs a check that no task performed, say which and why, and leave the running to the controller.

**Stay read-only on the code under review.** Do not edit the files in the package. Scratch probes are useful -- put them in the repository's designated scratch area, and never outside the repository.

**Report in this form.**

    ## Final review

    **Does the work meet the spec:** YES | NO
    - [if NO, what is missing or wrong, one line each]

    **Findings**
    - [Critical|Important|Minor] path:line -- [what is wrong, and why it matters]

    **Cross-task issues**
    - [interface mismatches, duplication, orphaned scaffolding, drift]

    **On the deferred and parked list**
    - [ledger item] -- AGREE | RE-GRADE to [severity] | OVERTURN -- [one line]

    **Cannot verify from the package**
    - [requirement, and what would be needed to check it]

---
