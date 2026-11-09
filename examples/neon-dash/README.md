# Neon Dash

An original, self-contained Godot 4 microgame distributed under the repository's MIT license. All art is drawn in code. No downloaded assets, packages, or editor import are needed. Tested with Godot **4.6.3**.

```sh
godot --path examples/neon-dash
```

Press Space to begin/restart, A/D or Left/Right to change lanes. Collect mint orbs. This is intentionally a tiny, bounded fixture, not proof the toolkit handles a full commercial game.

## Deterministic game test

```sh
godot --headless --path examples/neon-dash --script res://smoke_test.gd
```

The test performs the same 180-step, seed-7 replay twice and checks equal states, 300 points, zero misses, and exactly 180 simulation steps. It exits nonzero on failure. It does **not** test rendering, real player input, audio, pacing, wall-clock performance, or visual polish. In restricted CI, set `XDG_DATA_HOME`, `XDG_CACHE_HOME`, and `XDG_CONFIG_HOME` to writable directories.

## gdx-controlled evidence

See [the Godot integration contract](../../godot/README.md). The game exposes `polish_replay(frames, seed)` and `gdx_state()` for gdx's standard method invocation/state inspection. Replay leaves the simulation paused so captures correspond to a stable state. These game-specific hooks are not a second daemon, CLI, or RPC transport.

The drawing can be edited independently from the deterministic simulation. Compare images at the same resolution, frame count, seed, and engine version. A prettier screenshot does not establish better playability.
