# Evidence and decision loop

## A useful change card

Record this before a change, in the project’s existing tracker or a local pass note:

- **Player symptom:** what happened, scene and reproduction steps.
- **Evidence:** baseline revision, capture/log path, input sequence and relevant timestamp.
- **Hypothesis:** why this change should help; distinguish observation from inference.
- **Scope:** files/system affected and what will remain outside this pass.
- **Acceptance:** observable behavior, regression checks, and any human judgment needed.
- **Cost cap:** wall-time or iteration limit, approved paid spend if any.
- **Outcome:** kept, revised, reverted, or blocked; evidence and unresolved risks.

Do not turn every subjective judgment into a numeric score. If using a rating, label the rater and criteria; never aggregate it into an objective “commercial quality” score. A screenshot can establish layout, not controller feel. A short scripted run can establish startup, not campaign stability.

## Comparable captures

Use the same save state, scene, seed when supported, camera, resolution, input sequence, and approximate duration. Record variations that cannot be controlled. Put before and after evidence beside a plain explanation of what the viewer should compare. Label synthetic fixtures and edited mockups; neither is live gameplay evidence.

Measure performance on the actual target or label the computer/renderer limitations. Report frame-time distributions or spikes when available, not only average FPS. Cloud CPU/software-renderer results cannot establish target GPU performance. Keep audio levels and playback device consistent when evaluating mix changes.

Preserve original evidence. A capture is evidence only after it exists and has been inspected; a requested filename is not proof. Use relative paths or the host's supported attachment mechanism for delivery, not private cloud filesystem paths as public links. Redact secrets and private player data before sharing externally.

## Budgets and stopping

Record elapsed time, iteration count, tool/runtime usage that is actually exposed, and explicit paid expenses. Leave unknown costs unknown. Estimate future work as a range with assumptions; distinguish engineering effort from metered spend. Default to one small experiment if no broader budget has been agreed.

Stop or reassess when:

- The acceptance condition is met and regression checks are complete.
- The agreed time/iteration/spend cap is reached.
- Two attempts fail to produce an observable benefit: summarize alternatives rather than endlessly tuning.
- New work would change genre, balance philosophy, content scope, dependencies, engine version, or spending beyond authorization.
- The next judgment depends on human playtesting or unavailable hardware.

Do not silently extend the loop overnight. Future checks need the host's supported scheduling and user-approved scope. Save a checkpoint so another session can resume without repeating discovery.
