# Godot workbench

## gdx owns control

Use the existing [gdx project](https://github.com/zwx1127/gdx) for Godot launch, interaction, state inspection, and captures. Inspect the installed `gdx --help` and supported command help before invoking it; do not invent missing verbs. The starter check uses `gdx --project PROJECT script check-all`. `game-polish` owns goals, experiment selection, evidence records, and acceptance decisions, not a second runtime-control layer.

If gdx lacks input, capture, or state capabilities required for the pass, record the exact missing capability. A scoped gdx enhancement is preferable to building an alternative controller in game-polish. Continue independent static checks while reporting the gap. Ordinary direct Godot validation may supplement gdx when appropriate; it should not silently replace its ownership of control.

## Baseline and compatibility

Inspect `project.godot`, project instructions, export presets, add-ons, autoloads, input actions, and the main scene. Use the project's Godot major/minor version and renderer when known. Godot 3 and 4 projects are not interchangeable. Do not upgrade the engine or mass-resave scenes to solve a narrow polish issue without assessing and authorizing that scope.

Work in an isolated copy or recoverable branch. Godot's import/editor run can write `.godot` and plugin-generated data. Preserve tracked source and user work. Keep generated import caches out of authored patches unless the repository specifically requires otherwise. Treat `.uid` files according to the project's Godot version and repository conventions; do not delete them indiscriminately.

Disable or inspect unfamiliar editor plugins before launch when feasible. Project code, editor plugins, and `@tool` scripts may execute during editor/import operations. Headless does not mean sandboxed or safe to run untrusted code.

## Checks have different meanings

Use the installed gdx help and the package's `godot/README.md` for supported commands. At minimum inspect the project and run `gdx --project PROJECT script check-all`; for runtime evidence use gdx's daemon, calls/state, and capture operations. Validate structured `ok` results, not only exit codes. After daemon start require `rpc_ready`, `scene_loaded`, and `project_healthy`. Record raw stdout/stderr. Restart stale scripts before replaying from the same state. A failed capture or missing gdx is a blocker, not a visual pass.

A game-local headless regression test can supplement gdx. It is not a replacement engine controller or screenshot path. Use the project's documented test command and a wall-clock timeout. Do not create a second Godot runner here.

Use the project's own test framework if present. Do not claim headless startup proves rendered output, sound, controller behavior, performance, or absence of gameplay bugs. On a cloud computer with a usable display, launch the normal renderer and inspect an actual gameplay capture. If no GUI/audio/GPU or interaction mechanism is available, document exactly which checks remain blocked.

## Practical polish targets

- Input: use existing Input Map actions; test pressed/released/held semantics, buffering and interruption. Avoid making controls frame-rate dependent.
- Camera: test smoothing, bounds, lookahead, and effects with real movement. Camera shake should respect pause, reduced-motion choices, and UI independence.
- Feedback: tie animation, particles, sound, hit flash, and screen cues to real state transitions. Prevent repeated triggers or effects surviving a reset.
- Timing: changes to time scale, hit stop, and tweens must recover after pause, death, scene changes, and rapid repeated events. Physics and UI clocks may need different treatment.
- UI: use anchors/containers and the project's stretch settings; inspect narrow/wide windows, text overflow, focus order, and keyboard/controller navigation where supported.
- Resources: maintain scene/resource paths and UIDs; check exported resources rather than relying only on editor discovery.

Keep art direction and mechanics consistent with the existing game. A small audio envelope, clearer damage cue, or readable retry screen may be a better pass than rewriting the movement controller.

## Exports and artifacts

Export templates must match the engine version. Verify the requested preset and platform dependencies before exporting. A successful local export does not authorize distribution or storefront upload. Do not modify signing credentials, publish builds, or send crash/analytics data without appropriate authorization. Report absent export templates or unavailable target hardware as limits, not failed gameplay.


## Record the actual renderer and preserve capture logs

A configured Forward+ project can automatically fall back to Compatibility, and a usable GUI can still be software-rendered. Record the backend/device reported by the actual capture process, not just project.godot or a doctor check. Keep unsupported target-renderer/performance claims out of the result.

Where installed `capture record --help` exposes `--logs-dir`, request a per-round log directory and retain the returned `artifacts.stdout_log` and `artifacts.stderr_log` with the recording. Inspect those raw logs for fallback and errors; do not infer a backend from the option itself. Older builds may not expose this option: use available retained runtime logs, or a same-environment probe explicitly labeled as a probe, not the exact recording log. Report the remaining uncertainty. Never pass an unverified flag to an older build.

A shell and the connected desktop can have different display/socket access. A failed headless shell launch is not proof that the desktop cannot capture. Check the supported desktop environment before declaring capture unavailable, while retaining gdx as the controller. Do not bypass permissions or build a second renderer-control service. Runtime logs may contain project-private output; review before external sharing.

Validate the recorded media dimensions with a media inspector when available. The gdx recording result's `resolution` may echo requested dimensions rather than the encoded size; project viewport overrides were observed in a real capture. Keep requested and measured dimensions separate and disclose an unverified size when no inspector is available.
