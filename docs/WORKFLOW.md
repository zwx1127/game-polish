# A polish pass with dot

`game-polish` complements an existing dot and its cloud computer. The Python CLI records reproducible checks and evidence; the skill tells dot how to make bounded design decisions. Neither replaces the game engine, a real player, or the host's permissions and execution controls. No separate agent server or paid model API is required by this package. Using a host assistant may still have plan limits or costs.

## Start with a playable slice

Give dot a local project and a concrete outcome, for example:

> Use the game-polish skill on this Godot project. Improve the clarity of damage and retry without changing the movement mechanics. Work locally for one bounded pass. Show before/after evidence and keep publication out of scope.

Dot should identify the engine version and current baseline, capture the relevant behavior, choose a small change, repeat the checks, and return evidence and a patch. If the project is not runnable, the first useful result may be a diagnosis rather than visual polish. If it cannot interact with the game, it should say so before treating the pass as verified.

## Local evidence toolkit

From the package checkout, with Python available:

```sh
PYTHONPATH=src python -m game_polish --help
PYTHONPATH=src python -m game_polish init /absolute/path/to/game
PYTHONPATH=src python -m game_polish validate --config /absolute/path/to/game/game-polish.json
PYTHONPATH=src python -m game_polish baseline --config /absolute/path/to/game/game-polish.json
```

The last command plans checks; it does not execute them. Inspect the generated configuration and commands before adding `--execute`. Configured commands run code with the current process's permissions. This tool is not a sandbox and a timeout is not a security boundary.

After recording an executed baseline, make the authorized change and run the same checks:

```sh
PYTHONPATH=src python -m game_polish baseline --config /absolute/path/to/game/game-polish.json --execute
PYTHONPATH=src python -m game_polish run --config /absolute/path/to/game/game-polish.json --baseline /absolute/path/to/game/.game-polish/runs/BASELINE_ID --execute
PYTHONPATH=src python -m game_polish report /absolute/path/to/game/.game-polish/runs/RUN_ID
```

Replace IDs with actual run directories returned by the CLI. A baseline referenced for comparison must be a passed baseline. Use `--check NAME` to select checks; record that this reduces coverage. Read current `--help` when using a newer package version rather than assuming flags are unchanged.

Each run keeps a manifest, configuration snapshot, observations, report, evidence directory, and execution logs under `.game-polish/runs/`. Configuration specifies goals, constraints, check argument arrays and timeouts, required evidence, and acceptance criteria. Argument arrays are preferable to shell strings; they do not make the invoked program trustworthy. Placeholders `{project_root}` and `{evidence_dir}` let checks write into the correct run context.

The default gdx check sets `expect_json_ok: true`, requiring both a successful process exit and a stdout JSON object with `ok: true`. Other command checks without this option establish only exit-status success. Separate stdout and stderr logs preserve diagnostics. Git source records are best-effort and do not capture untracked file contents; preserve those separately when needed to reproduce a pass.

A passing automated check is not a passed design review. Fill observations with actual findings and retain media evidence separately. Do not mark planned checks as executed or write a fabricated human playtest result. Read the report's distinction between execution status and review state.

## Repeated passes and token budgets

Configuration can record `cycle.interval_minutes` and `cycle.max_tokens`. These are requested parameters, not a scheduler or token limiter. The existing dot host must supply scheduling, usage measurement, and enforcement. The CLI records unknown usage as unknown and does not call models. If the host cannot enforce a hard token cap, disclose that gap; use a bounded scope/time/iteration allowance only if the user accepts it as an approximation. Do not label that approximation a hard token budget.

Use the skill’s `references/continuous-passes.md` for safe recurring operation and longitudinal evidence. A real `llm-game` demonstration requires runnable project access, working gdx control, captured baseline/after behavior, and multiple evaluated passes. Tests with simulated commands establish harness behavior only, not improvement to llm-game.

## Useful checkpoints

- **Baseline:** relevant scenario can be reproduced; capture and runtime context exist.
- **Experiment:** one clear hypothesis and reversible change; no broad redesign hidden in a polish pass.
- **Verification:** comparable before/after evidence plus affected regression checks.
- **Human review:** a person evaluates feel, comprehension, and enjoyment when those claims matter.
- **Handoff:** exact patch, what passed, what was not tested, remaining risks, and next action.

Keep the scope proportional to the project. A ten-minute prototype needs a different evidence bar from a shipped game with save compatibility and multiple platforms. Commercial readiness requires explicit criteria and evidence beyond this package's automated checks.
