# Continuous improvement without silent degradation

Use the user's existing dot host to schedule passes. Do not create a new daemon or agent platform. Recording an interval and token budget in configuration does not schedule work or enforce a limit.

Before enabling repeated work, establish the requested interval, per-pass token budget, scope of allowed modifications, and notification/stop conditions. Verify the host can actually schedule and observe execution. Check whether it exposes usage and enforces a cap across the parent and delegated work. If it cannot, say so explicitly and ask whether a bounded time/iteration approximation is acceptable. Never report unknown token usage as zero or an estimated cap as a hard limit.

## One recurring pass

1. Check for user changes and incomplete prior work. Do not overlap writers or start a fresh pass while an earlier one is still running. If a run overruns the interval, skip or defer the next slot rather than accumulating simultaneous mutations.
2. Resume from the last accepted checkpoint, not simply the newest files. Preserve the original reference baseline too, so small regressions do not become invisible through repeated rebasing.
3. Select one reproducible problem and an acceptance condition. Reserve time/budget for verification and rollback instead of spending everything on implementation.
4. Make the reversible change, run the same relevant checks through the supported gdx workflow, and inspect comparable gameplay evidence.
5. Keep only changes with sufficient evidence and no unacceptable regression. A code-check pass does not override a visual or gameplay regression. Revert only the pass's own changes, preserving unrelated user edits.
6. Save the decision, source revision, evidence, observed usage or its absence, and next candidate. Notify according to the agreed policy, with material regressions or blockers surfaced promptly.

Stop on an unresolved crash, broken save behavior, lost control capability, missing permissions, exhausted budget, or repeated inconclusive experiments. Do not continue unattended with deteriorating evidence quality. When human feedback is necessary, checkpoint and wait for it rather than letting another model impersonate a player.

## Demonstrating progress in llm-game

Inspect the actual authorized llm-game checkout and run instructions; do not assume that a repository with this name is runnable or public. Record its exact revision and gdx version. Establish real baseline captures and reproducible scenarios before editing. Compare successive accepted checkpoints against both their immediate predecessor and the original baseline.

Maintain a short longitudinal record with pass ID, source checkpoint, player-facing hypothesis, verification results, visual/gameplay findings, measured cost if available, decision, and unresolved regressions. Track regressions separately from improvements so a long list of new features cannot hide broken behavior.

A credible demonstration includes an actual kept improvement, an actual comparison of runtime evidence, and clear accounting of failed or reverted attempts if they occurred. Do not manufacture a rejected experiment just to make the record look balanced. Multiple passing static checks, invented screenshots, a synthetic fixture, and model self-ratings do not demonstrate that llm-game is continuously improving. If the real project or gdx is unavailable, deliver the toolkit and mark the real-game demonstration blocked.
