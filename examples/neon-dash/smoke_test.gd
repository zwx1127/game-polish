extends SceneTree
## Example's own CI unit/smoke test, not a Godot control adapter.
## Screenshot capture and runtime control belong to gdx.
func _initialize() -> void:
	call_deferred("run_test")

func run_test() -> void:
	var packed = load("res://main.tscn")
	if not packed is PackedScene:
		printerr("SMOKE_FAIL: scene did not load")
		quit(1)
		return
	var game = packed.instantiate()
	root.add_child(game)
	var first: Dictionary = game.polish_replay(180, 7)
	var second: Dictionary = game.polish_replay(180, 7)
	var passed: bool = first == second and first.get("score") == 300 and first.get("misses") == 0 and first.get("tick") == 180
	print(JSON.stringify({"test": "neon_dash_replay", "passed": passed, "state": first, "repeat_equal": first == second, "visual_evidence": false}))
	game.free()
	quit(0 if passed else 1)
