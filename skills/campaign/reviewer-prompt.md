# Campaign reviewer prompts

Three blocks to paste when dispatching a review during a campaign: one for an experimental change, one for claims about to be promoted, one for the closing report. Each block is everything between its horizontal rules; this paragraph and the notes between blocks address you, not the reviewer. A re-review after a fix round uses the re-review block in `${CLAUDE_PLUGIN_ROOT}/skills/sdd/reviewer-prompt.md`, with the experiment's brief entry standing in for the task brief, and with the Gating and Markers bullets of the implementation block below appended to its "Beyond the findings" paragraph: a fix that leaks into the off path would otherwise pass until the closing identity check.

Fill every `[BRACKETED]` slot before dispatching, except where a block marks one as omittable. Paste the ledger slices a block asks for into files in the workspace and hand over the paths; the reviewer greps the full ledger only where a block says so.

Do not add "do not flag X" or "at most Minor" to any of them. Pre-judging a finding to spare yourself a fix round is the failure these reviews exist to catch; raise it, then adjudicate it.

## Implementation review

---

You are reviewing one experimental change made during a research campaign. A later consolidation pass will keep or discard this change as written, and clean only its interface, so it has to be correct and it has to be written to the standard of the code around it. Report two verdicts: whether the change is correct and does what its brief says, and whether its quality is acceptable to keep. Both are required; a report missing either is incomplete.

**Read these first.**

- The brief: `[BRIEF_FILE -- the ledger entry that planned this experiment]`
- The charter: `[CHARTER_PATH]`. Read its Moves allowed section: what may change, what is off limits, and how experiments are gated.
- The implementer's report: `[REPORT_FILE, or omit this line where the change was made inline]`
- The manifest entry for this change: `[MANIFEST_ENTRY_FILE -- the ledger's manifest row or rows for it]`
- The change: `[REVIEW_PACKAGE_FILE]`. It holds the campaign's cumulative diff on the files this change touched, followed by this change's own diff against snapshots taken just before it. Review the second part; read the first to see what it sits among. A file this change created appears whole in the first part; review it there.

**What to check.**

- Brief: the change does what the brief says, and nothing beyond it.
- Correctness: including its edge and failure cases. Where it adds an instrument, the instrument does not change the computation it observes.
- Gating: the change is reachable only with its switch on, and with the switch off the code behaves exactly as it did before the change. Trace every edited line to its switch. A line that changes behaviour with the switch off is Critical, because every comparison against the starting code then measures the leak instead of the experiment. A change the manifest marks ordered kept has no switch by design: check instead that it is exactly what was ordered, and nothing more.
- Markers: every experimental block carries the campaign's marker comment, naming its switch.
- Manifest: the manifest entry matches the diff -- its files, its switch, and what it says the change does.
- Moves: nothing touches what the charter puts off limits; no configuration surface is added unless the charter permits it; no existing test is changed to make it pass.
- Quality: names say what things do, the structure follows the surrounding code, comments are at the surrounding density, and there is no duplication or dead surface. Hold it to the standard of code that will ship, because it may: consolidation cleans interfaces, it does not rewrite.
- Verification: the checks the implementer ran exercise the behaviour. Test each against a deliberate small breakage -- a wrong constant, the wrong branch taken, a step left out -- and say where none would go red.

**Grade every finding.**

- **Critical** -- breaks correctness, leaks through a switch that is off, or fails the brief.
- **Important** -- a real defect that should be fixed before any result measured on this code is trusted.
- **Minor** -- cosmetic, stylistic, or a matter of preference.

**Where you cannot tell** from the package, check one concrete risk you can name outside it, one focused check per risk. Do not crawl the codebase. List what you still cannot settle, and what you would need.

**Stay read-only on the code under review.** Scratch probes go in the repository's designated scratch area, never outside the repository.

**Report in this form.**

    ## Implementation review

    **Correct and as briefed:** YES | NO
    - [if NO, what is wrong or missing, one line each]

    **Quality:** APPROVED | CHANGES NEEDED

    **Switch-off identity, by reading:** HOLDS | BROKEN at [path:line]

    **Findings**
    - [Critical|Important|Minor] path:line -- [what is wrong, and why it matters]

    **Cannot verify from the package**
    - [what, and what would be needed to check it]

---

## Numbers review

Dispatch this before a claim is used for anything only a reviewed claim may ground. Batch claims that share runs into one dispatch.

---

You are reviewing claims made by a research campaign, before they are allowed to support recommendations. Establish whether the numbers are what the claims say they are, and whether the claims follow from them. A claim you pass will be acted on.

**Read these first.**

- The claims under review, with the ledger entries that made them: `[CLAIMS_FILE]`
- The run registry: `[REGISTRY_FILE]`. Each run's code state, inputs, command and output path.
- The charter: `[CHARTER_PATH]`. Its bar, and the scatter margin an effect has to clear to count.
- The run protocol: `[RUN_PROTOCOL -- the charter section, or the project document's path]`

**For each claim.**

- Re-derive every number it states from the raw output of the runs it cites, with your own script, written to the scratch area. Do not reuse the campaign's analysis scripts: a number reproduced by the script that produced it has not been checked.
- Re-run one run the claim rests on -- the cheapest that exercises it -- under the run protocol, and compare. Where the run protocol does not let you launch it, the dispatch hands you the output of a re-run the controller launched instead: compare that. If neither exists, say so rather than skipping it silently.
- Compare the runs the claim compares. They must differ only in what the claim says they differ in: check code state, switches, inputs, parameters, limits, defaults and environment. A difference nobody mentioned is the most common way a comparison ends up measuring something other than its subject.
- Check the reading: does the effect clear the charter's scatter margin; does the wording claim more than the numbers show; is there an explanation the campaign did not exclude.

**Stay read-only** on the code and on the campaign's own outputs. Your scripts and your re-run's output go in the scratch area.

**Report in this form.**

    ## Numbers review

    - [claim ID] -- SUPPORTED | SUPPORTED WITH CORRECTIONS | NOT SUPPORTED -- [one line]
      - Re-derived: [each number, as stated and as re-derived]
      - Re-run: [label, command, code state, output path, wall time, result against the original] | not re-run: [why]
      - Uncontrolled differences: none | [what]
      - Reading: agree | [the wording the numbers support]

---

## Closing review

Dispatch this once, in the closing pass, after the report is written.

---

You are reviewing the report that closes a research campaign. A consolidation pass will turn it into production code, and its owner will rule on its recommendations from what it says. Every recommendation and every conclusion must rest on evidence of the standing the report claims for it. You are the last check before that happens.

**Read these first.**

- The charter: `[CHARTER_PATH]`
- The report: `[REPORT_PATH]`
- The ledger: `[LEDGER_PATH]`. The full record: manifest, claims, rulings, run registry and log. It is long; grep its `### ` entry headings rather than reading it end to end.
- The campaign's change: `[REVIEW_PACKAGE_FILE]`. The whole working tree's diff against the starting commit, with every new file in full.
- Unaccounted files: `[the paths git status shows outside the manifest's files, the campaign's records and the workspace, or: none]`
- The durable records: `[the paths of the memory entry and documentation the closing pass wrote]`

**What to check.**

- Tiers: each claim's tier in the report matches the ledger; every conclusion is at the concluded tier, with its replication done as the charter requires; every recommendation rests on claims at reviewed or above, except a recommendation to discard, which may rest on indicative claims labelled as such.
- Numbers: re-derive, from the raw output, the numbers the conclusions and recommendations rest on, with your own script in the scratch area, and re-run one run under the run protocol, or compare the controller's re-run where the dispatch hands you one. Where a claim already passed a numbers review, check that the numbers the report states are still the reviewed ones.
- Retractions: nothing in the report rests on a retracted claim, or on a demoted one for a use its new tier does not allow.
- Manifest: every change in the diff belongs to one of the report's consolidation items, and every item's files and switch match the diff. Say for each unaccounted file whether it is campaign work the manifest omits. Every experimental block is marked. By reading, the switched-off code is the starting code, re-based on any ordered-kept change.
- Rulings and questions: every provisional ruling is labelled provisional and names what it rests on -- reviewed claims, or for a ruling that interprets the charter, the charter's text quoted; every parked question and every directive reading awaiting ratification is listed for the owner.
- The charter's letter: the code and the rulings match the charter's text, amendments included. A departure recorded anywhere other than as a provisional ruling or a parked question is a finding.
- Durable records: the memory entry and documentation the campaign wrote state nothing more strongly than the report does.
- Reproduction: the steps for each concluded claim are complete enough to run.
- Wording: nothing is written more strongly than its tier allows.

**Grade every finding.**

- **Critical** -- a conclusion or recommendation the evidence does not support, or a change that no consolidation item accounts for.
- **Important** -- a real defect in the report that would mislead consolidation.
- **Minor** -- wording.

**Stay read-only** on the code and the report. Scratch goes in the repository's designated scratch area, never outside the repository.

**Report in this form.**

    ## Closing review

    **Conclusions supported:** YES | NO
    - [if NO, one line each]

    **Findings**
    - [Critical|Important|Minor] [report section, or path:line] -- [what is wrong, and why it matters]

    **Re-derivation**
    - [number: as reported, as re-derived]
    - Re-run: [label, command, code state, output path, wall time, result] | not re-run: [why]

    **Cannot verify**
    - [what, and what would be needed to check it]

---
