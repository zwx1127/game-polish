# Godot integration: use gdx, do not duplicate it

**game-polish owns** the polish brief, acceptance criteria, baseline/candidate evidence, change scope, and review loop. **[gdx](https://github.com/zwx1127/gdx) owns** Godot project inspection, compilation checks, runtime lifecycle, method calls, state inspection, and capture. **The project owns** deterministic game-specific hooks and tests.

There is deliberately no separate Godot control daemon, transport, or screenshot adapter in this directory. The example's headless `smoke_test.gd` is a game-local regression test only.

## Prerequisites and safety

Install gdx through its documented distribution instructions and verify `gdx --help` / `gdx --version`. The commands below were checked against gdx's upstream CLI reference; this MVP does not bundle gdx. Do not claim an end-to-end gdx run until it has actually run on the selected machine.

Start with a private working copy of a project. `project inspect`, `project update --check`, `doctor`, and `script check-all` are inspection/check operations. `project update` **writes gdx add-ons into the project**; run it only when the user has authorized that project setup. Record/pin the gdx revision and Godot version in each experiment.

## Example workflow

Run these individually, inspect each structured result, and stop on failures. `$PROJECT` is the absolute `examples/neon-dash` directory and `$EVIDENCE` is a new experiment directory. Do not reuse a running daemon belonging to another task.

```sh
gdx --project "$PROJECT" --progress ndjson doctor
gdx --project "$PROJECT" project inspect
gdx --project "$PROJECT" project update --check
# Only if authorized setup is needed:
gdx --project "$PROJECT" project update
gdx --project "$PROJECT" script check-all
gdx --project "$PROJECT" daemon start --restart --width 960 --height 600
gdx --project "$PROJECT" call invoke --target / --method polish_replay --args-json '[180,7]'
gdx --project "$PROJECT" state get --target / --method gdx_state
gdx --project "$PROJECT" capture daemon --out "$EVIDENCE/frame-0180.png" --frames 10
gdx --project "$PROJECT" daemon stop
```

After daemon start, require health fields `rpc_ready`, `scene_loaded`, and `project_healthy` to be true. `--frames 10` waits ten frames before one screenshot, not a ten-image sequence. The capture path is returned in `capture`, while RPC/state data is in `result`.

Success stdout is one JSON object; validate its `ok` field, not only the process status. Progress NDJSON can appear on stderr before a final failure JSON object. Retain raw stdout/stderr as evidence. A failed capture, missing display, missing add-on, missing binary, or failed compile is a blocker, not a visual pass.

After editing `.gd`, gdx may return `daemon_scripts_stale`. Explicitly restart the daemon and replay from the same seed before comparing state/images; do not pretend scripts were hot reloaded. `capture record` runs a **fresh scene**, so it is not a recording of the current daemon's state.

The commands establish instrumented replay evidence, not human playtesting. Use actual input-based checks for controls, collision edge cases, menus, interruptions, and game feel. Headless checks provide no visual quality evidence. When gdx cannot provide a needed operation, document the gap and iterate gdx rather than adding a competing control path here.

## Source

- [gdx CLI reference](https://github.com/zwx1127/gdx/blob/main/docs/en/cli-reference.md)
- [gdx repository](https://github.com/zwx1127/gdx)
