# Close a round with recoverable evidence

Read before completing a polish round, including a reverted or blocked experiment.

## Reconcile source and outputs

Inspect the final changed-file list against the pre-pass snapshot. Editor/import runs can rewrite project settings and tracked import sidecars; review those separately from authored changes. Preserve capture-time settings in evidence. After relevant processes stop, restore unintended normalization only from a verified pre-pass copy, never from a guessed version. Preserve repository-required UID files and user changes.

Archive test/capture outputs that were written inside the project before cleaning generated files. Remove only known generated outputs with a verified copy when appropriate; do not blanket-clean the user's working tree. Check that the patch contains every needed native/binary resource and no unrelated edits. Test forward application on a copy of the baseline and reverse application on a copy of the candidate. Document the required base revision/hashes and stop rather than force-apply to mismatched user files.

## Interpret results at the correct level

Transport success is not test success. A gdx `test run` can have top-level `ok: true` while the invoked game's return value contains `ok: false`. Inspect the documented nested return value (the verified runtime used `result.result`), assertions/counts and failure arrays. Preserve raw stdout/stderr, process exit and timeout separately. If a project's test framework does not expose an unambiguous result, label it inconclusive instead of counting a pass. The CLI `expect_json_ok` option checks only top-level JSON: it does not replace this nested review.

Distinguish new failures from reproduced baseline failures. Report full totals and the pre-existing failure explicitly; do not silently remove a failing check or call the whole suite green. A corrected test must have a reason, such as circular phase equivalence, rather than a weakened assertion to conceal a regression.

## Produce and deliver the report

Populate `observations.json` with the goal/problem, actual changes, before/after evidence filenames and how to watch them, observations, known regressions/old errors, limitations, rollback and decision. Put test totals and their source logs in the observations when not represented by the command-level manifest. Refresh `game-polish report RUN_DIR` and inspect both `report.html` and `report.md`. Their existence alone does not mean the observations are complete.

For work outside the CLI, do not fabricate a run manifest or executed baseline. Produce a sourced standalone report through the host's document workflow and state that the work was performed directly. Give the report and evidence as accessible attachments/links, not cloud-only filesystem paths. Verify persistence and attachment IDs before announcing delivery. If an upload is uncertain, check its outcome before retrying.

Each report must separate what changed, what was verified, what remains unverified and how to revert. Link the previous accepted checkpoint and original baseline for repeated work. Saving a report or a skill does not schedule another round, install the skill into every host, or guarantee the host will invoke it. End with the actual checkpoint and next unresolved decision, not an unsupported promise of continuous improvement.
