---
name: game-polish
description: Improve an existing playable game through bounded, evidence-backed polish passes using dot and its cloud computer. Use for game feel, clarity, presentation, accessibility, and release-readiness work, especially Godot projects.
---

# Game polish

Use the existing dot as the producer and its available computer as the workbench. This is a workflow and local evidence toolkit, not a new agent runtime. Preserve the game's identity. Commercial quality is an aspiration judged by the intended audience and target device, never a claim inferred from a passing smoke test or model score.

## Establish the pass

Read the project instructions and inspect the working tree before modifying anything. Preserve uncommitted user work. Confirm the runnable entry point, engine version, target platform/input, intended player experience, and allowed scope from available context. Ask only for missing decisions that materially affect the pass.

Set a bounded work window, maximum iterations, and an explicit stop condition. For recurring work, read [references/continuous-passes.md](references/continuous-passes.md). Use existing authorized resources; do not assume a subscription exposes API credit, unlimited compute, paid assets, or unattended runtime. If budget is unknown, begin with a small local baseline and one narrow change; ask before incurring charges or expanding scope. Read [references/evidence-loop.md](references/evidence-loop.md) for measurement and stop rules.

Establish a recoverable baseline in an authorized branch or isolated project copy. Record the revision, dirty state, engine version, startup command, device/display context, and evidence location. Inspect project scripts and plugins before running unfamiliar code. A separate project directory is not a security sandbox. Do not execute untrusted add-ons just because they are game assets.

## Observe before choosing

Run the actual game where possible, not just the editor or a headless import. Capture the first-play flow, core loop, and one failure/retry path. Record reproducible issues and distinguish observed failures from design hypotheses. For Godot, use gdx for engine control, runtime interaction, and capture; read [references/godot.md](references/godot.md). Keep goal selection, evaluation, and evidence ownership here. If gdx lacks a needed capability, identify the gap and propose a scoped gdx improvement rather than building duplicate control infrastructure.

For animation, sprite or asset-style work, read [references/animation-and-assets.md](references/animation-and-assets.md) before selecting the change and use continuous-frame evidence rather than a static-image substitute.

Choose the highest-value small intervention against the user's goal. Prioritize blocked play, confusing feedback, input/camera problems, and lost progress before decorative effects. Tie each change to a symptom, a test, and a predicted player benefit. Avoid adding a suite of effects simply to make the game look more elaborate.

## Change, compare, decide

Make a coherent, reversible patch. Parallel work is useful for independent critique, asset inspection, or tests; give code writers disjoint ownership to avoid conflicting edits. Use dot's existing delegation capabilities when available. Do not install an orchestration service, scheduler, remote-control endpoint, or new model API client for this workflow.

Re-run affected checks and repeat the baseline scenario under comparable conditions. Inspect the actual screenshots, video, audio, and runtime behavior relevant to the change. Include negative cases: rapid retry, repeated input, interrupted menus, pause/resume, and scene reload when affected. Do not treat the absence of an exception as evidence that a game feels better.

Keep, revise, or revert based on evidence. A model's critique is a hypothesis, not an independent player's verdict. If visual/audio interaction cannot be tested in the available computer, finish safe static work and clearly label the untested behavior rather than claiming polish is verified. Read [references/playtest.md](references/playtest.md) before making player-experience or release claims.

## Deliver the checkpoint

Return the changed files or local patch, a short before/after explanation, exact checks performed, evidence locations, known regressions, and next decision. Distinguish passed, failed, blocked, and not run. State actual effort and remaining uncertainty instead of invented dollar costs. Leave a reproducible next-pass entry point.

A successful pass can end with a useful diagnosis or a reverted experiment. Stop at the agreed limit, a serious regression, missing authorization, or insufficient evidence to select the next change. Do not publish, push, merge, upload private builds, purchase assets, recruit testers, or contact anyone merely because a polish pass was requested.

### Mandatory end-of-round report
Read [references/round-completion.md](references/round-completion.md) to reconcile source changes, interpret nested test results, verify rollback and deliver the report.
For every completed polish round, populate observations.json with the actual goal/problem,
changes, before/after evidence and viewing instructions, test results, known baseline errors,
limitations, rollback and unresolved items. Run `game-polish report RUN_DIR` after those
observations are saved; verify both report.html and report.md exist. Deliver the readable
report to the user alongside evidence. A pending template is not a completed narrative.
If the round was performed outside the CLI, create and deliver a sourced standalone report
and state that no automatic CLI run record exists. Never invent executed checks or scheduling.
