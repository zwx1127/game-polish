# game-polish

An evidence-first game-polishing skill and local toolkit for **your existing dot and cloud computer**. It is not another agent framework, model API client, scheduler, or Godot control service.

- **dot** investigates, edits, reviews evidence, and uses its existing scheduling capabilities when requested and verified.
- **game-polish** defines bounded experiments, saves check results, preserves evidence, and makes acceptance review explicit.
- **[gdx](https://github.com/zwx1127/gdx)** owns Godot inspection, runtime control, project method calls, state inspection, and capture.
- **Your game** owns replay hooks, invariants, and project-specific regression tests.

A successful command is not proof that a game became more enjoyable. Every pass needs a concrete hypothesis, comparable before/after evidence, regression coverage, and an explicit accept/reject/defer decision.

## Quick start

Requires Python 3.10+. The CLI has no runtime Python dependencies. Use it directly from this checkout:

```sh
PYTHONPATH=src python -m game_polish --help
PYTHONPATH=src python -m game_polish init /absolute/path/to/game
PYTHONPATH=src python -m game_polish validate --config /absolute/path/to/game/game-polish.json
PYTHONPATH=src python -m game_polish baseline --config /absolute/path/to/game/game-polish.json
```

`init` never overwrites an existing config. The final command creates a **plan only**. Review the configuration before executing any commands. The default check invokes `gdx script check-all`; gdx must already be installed and the project prepared according to its documented setup. Creating a config does not install gdx or modify Godot add-ons.

To expose the `game-polish` console command, optionally install this package in a virtual environment with `python -m pip install -e .`. Build tooling may need network access. Direct `PYTHONPATH=src` usage does not require installation.

Use [`skills/game-polish/SKILL.md`](skills/game-polish/SKILL.md) with your existing assistant. Skill discovery/installation depends on the host; this package does not silently install or start anything.

## One bounded pass

1. Establish scope and invariant behavior. Use an authorized private working copy and preserve the original baseline.
2. Capture a reproducible baseline through gdx, including game state, screenshots, engine/gdx versions, viewport, rendering backend, scenario, and seed where supported by the game.
3. Run baseline checks, then make one reversible change with a testable hypothesis.
4. Run the same checks and capture the same scenario after the change.
5. Review actual before/after evidence, affected gameplay invariants, and regression results. Accept, reject, or defer explicitly. Retain rejected experiments as evidence rather than silently promoting them.

```sh
PYTHONPATH=src python -m game_polish baseline --config /absolute/path/to/game/game-polish.json --execute
# Make the authorized, reversible change; substitute the actual returned baseline directory below.
PYTHONPATH=src python -m game_polish run --config /absolute/path/to/game/game-polish.json --baseline /absolute/path/to/game/.game-polish/runs/BASELINE_ID --execute
PYTHONPATH=src python -m game_polish report /absolute/path/to/game/.game-polish/runs/RUN_ID
```

`--check NAME` can select a subset of checks. Record the reduced coverage. Commands run as argv arrays without shell interpolation, with configurable timeouts, but **they execute trusted project code with your current permissions**. This CLI is not a sandbox. Review commands and authorization first.

For now `--baseline` requires the same absolute project root. Use one private working directory at baseline/candidate checkpoints, with a separately preserved baseline. If experiments use isolated baseline and candidate copies, save both runs without this flag and compare their evidence explicitly; the CLI does not assert cross-copy equivalence. Do not edit a manifest to bypass this check.

## Configuration and evidence

See the [configuration schema](schemas/game-polish.schema.json), [example project](examples/neon-dash), and [Godot/gdx workflow](godot/README.md).

A check contains `argv`, `timeout_seconds` (1–3600), and optional `expect_json_ok`. `{project_root}` and `{evidence_dir}` placeholders resolve to the current project and run directory. For gdx checks set `expect_json_ok: true`: both a zero process exit and one stdout JSON object containing `ok: true` are required. Other checks default to exit-status-only validation.

Each run gets a fresh `.game-polish/runs/<id>/` directory:

- `manifest.json`: actual execution status, command arguments, timing, source metadata, requested cycle/budget, and comparison scope.
- `config.snapshot.json`: configuration used for that run.
- `NAME.log` / `NAME.stderr.log`: stdout and stderr kept separately, including gdx progress/failure details.
- `observations.json`: a pending review template; record the hypothesis, changes, evidence, regressions, limitations, and decision.
- `evidence/`: destination for gdx captures and project evidence. The CLI does not automatically take screenshots.
- `report.md`: check summary and outstanding review checklist. Regenerating it does not evaluate observations or approve a change.
- Git revision/status/diff snapshots before and after execution, when available. Untracked file contents are not captured. Non-Git projects explicitly report unavailable source identity; preserve source hashes separately.

`passed` means configured checks passed. `no_check_regression` means matching baseline/candidate checks passed; it is **not** a claim that graphics, gameplay, accessibility, sound, or performance did not regress. gdx `ok: true` is only the generic protocol check: inspect command-specific health fields, capture paths, actual image pixels, and game-specific assertions too.

## Recurring cycles and token limits

The config can record requested parameters, for example:

```json
"cycle": {"interval_minutes": 60, "max_tokens": 20000}
```

These example values do not establish a schedule or budget. Both fields accept a positive integer or `null`.

- **Scheduling:** configure and verify it with the existing dot host. The CLI records `not_scheduled_by_cli` and prints a warning when an interval is configured. No background job is created by `init`, `validate`, `baseline`, or `run`.
- **Hard token cap:** unsupported by this CLI. It makes no model calls, cannot meter host/subagent usage, and records `tokens_used: null` / `enforcement: unsupported_by_cli`. A configured cap produces an explicit warning.
- **Required host behavior:** before starting a budget-constrained model cycle, verify that the host can measure and enforce the whole-cycle token limit. If it cannot, report the blocker. Do not replace it with time limits or iteration counts without the user's agreement, and never call those a hard token cap.
- **Continuous improvement:** maintain an accepted baseline and a chronological experiment ledger. Compare every candidate to the last accepted baseline; failed or inconclusive candidates must not become the next baseline automatically. Multiple evaluated passes are needed to support a continuing improvement claim.

See [continuous-pass guidance](skills/game-polish/references/continuous-passes.md) for the scheduling handoff and evidence gate.

## Verified scope and limitations

Current verification covers:

- Unit/integration tests for config validation, planning without execution, failures/timeouts, baseline comparisons, evidence placeholders, path containment, gdx JSON contracts, and explicit cycle/budget feedback.
- Compatibility with recorded stdout from **real gdx startup and screenshot capture** on llm-game; replaying these fixtures tests parsing, not a new game run.
- A real `gdx doctor` call through this CLI's execution function on the llm-game integration copy, with exit 0 and `ok: true`.

Separate real llm-game gdx testing established startup, state inspection, and a nonempty screenshot using Godot 4.6.3, GL compatibility/Mesa software rendering, and Dummy audio. It used gdx source `d08d7a4f2210cd435ccfff8d8f537e881c167ee1` plus a local **unpublished startup-timeout extension**, because the scene took longer than upstream's 30-second wait. This is not Forward+ visual parity, audio validation, hardware performance evidence, or proof of sustained improvement.

If using that extension, `daemon start --startup-timeout-secs 180` requires the patched gdx build; do not assume upstream supports it. Set the outer CLI check timeout above 180 seconds (for example 240) and retain health checks. Xvfb and the runtime must share the correct display/session. Extend gdx for missing engine operations rather than creating a second Godot controller here.

## Development

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
python -m compileall -q src
```

See [workflow](docs/WORKFLOW.md), [design](docs/DESIGN.md), and the [gdx integration contract](godot/README.md). Nothing here publishes, deploys, or merges a game change automatically.

## 每轮报告（2026-11-08 增强）

`baseline` 和 `run` 无论仅计划、检查通过或失败，结束时都自动生成 UTF-8
`report.md` 与可直接在浏览器打开的 `report.html`。它们描述真实命令结果，不将
“通过检查”冒充美术验收。初始观察尚未填写会明确显示待记录。

完成本轮打磨后，dot 应填写该轮 `observations.json` 的 `hypothesis`、`changes`、
`evidence`、`observations`、`regressions`、`limitations`、`rollback`、`decision`，
再运行 `game-polish report RUN_DIR`。该命令只重建两份报告，不重跑游戏、不改判定结果。
报告会纳入视觉证据的文件名/观看说明、旧错误、回退方式和未验证项；HTML 将所有记录
作为转义后的文本显示，不执行脚本或远程内容。证据路径是阅读位置，不代表已独立核验。

这不是后台 watcher 或自动调度：绕过此 CLI 的人工/dot 工作需要显式生成报告；宿主仍
负责每轮结束的调用、完整填写观察与向用户发送附件。CLI 不自动生成 Word/PDF，也不
强制 token 预算。正式用户报告可由 dot 从这份结构化记录生成并审核。
