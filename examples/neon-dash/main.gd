extends Node2D
## Original vector-only microgame, no external assets or licenses.
## Left/right or A/D change lanes. Space starts/restarts. Collect mint orbs.
const LANES := [310.0, 480.0, 650.0]
const SPEED := 3.0
var lane := 1
var score := 0
var misses := 0
var tick := 0
var playing := false
var automated := false
var run_seed := 7
var items: Array[Dictionary] = []
var rng := RandomNumberGenerator.new()
var flash := 0
var font := ThemeDB.fallback_font

func _ready() -> void:
	rng.seed = run_seed
	queue_redraw()

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo: return
	if event.keycode == KEY_SPACE:
		_reset(run_seed)
		playing = true
	if event.keycode in [KEY_LEFT, KEY_A]: lane = maxi(0, lane - 1)
	if event.keycode in [KEY_RIGHT, KEY_D]: lane = mini(2, lane + 1)

func _physics_process(_delta: float) -> void:
	if playing and not automated: _advance()

func _reset(value: int) -> void:
	automated = false
	run_seed = value
	rng.seed = value
	lane = 1
	score = 0
	misses = 0
	tick = 0
	flash = 0
	items.clear()

func polish_begin(value: int) -> void:
	_reset(value)
	automated = true
	playing = true

func polish_step(_frame: int, _value: int) -> void:
	# Deterministic controller follows the closest orb, exercising collection.
	if not items.is_empty(): lane = items[0]["lane"]
	_advance()

func _advance() -> void:
	tick += 1
	flash = maxi(0, flash - 1)
	if tick % 30 == 1:
		items.append({"lane": rng.randi_range(0, 2), "y": 112.0})
	for item in items: item["y"] += SPEED
	for index in range(items.size() - 1, -1, -1):
		var item := items[index]
		if item["y"] >= 470.0:
			if item["lane"] == lane:
				score += 100
				flash = 12
			else: misses += 1
			items.remove_at(index)
	queue_redraw()

func polish_snapshot() -> Dictionary:
	return {"tick": tick, "lane": lane, "score": score, "misses": misses, "active_orbs": items.size(), "playing": playing}

func _draw() -> void:
	draw_rect(Rect2(0, 0, 960, 600), Color("090e20"))
	for x in range(0, 961, 40): draw_line(Vector2(x, 108), Vector2(x, 525), Color("111c35"), 1)
	for y in range(108, 526, 40): draw_line(Vector2(180, y), Vector2(780, y), Color("111c35"), 1)
	draw_string(font, Vector2(44, 51), "NEON / DASH", HORIZONTAL_ALIGNMENT_LEFT, -1, 29, Color("e4eeff"))
	draw_string(font, Vector2(44, 77), "A SMALL GAME. A REPEATABLE POLISH LOOP.", HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color("7794be"))
	draw_string(font, Vector2(736, 48), "%04d" % score, HORIZONTAL_ALIGNMENT_LEFT, -1, 31, Color("80ffd7"))
	draw_string(font, Vector2(736, 73), "POINTS  /  %d MISSED" % misses, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color("7794be"))
	for x in LANES:
		draw_line(Vector2(x, 110), Vector2(x, 510), Color("283653"), 2)
		draw_circle(Vector2(x, 485), 23, Color("14233d"))
	for item in items:
		var pos := Vector2(LANES[item["lane"]], item["y"])
		draw_circle(pos, 22, Color(0.35, 1, 0.8, 0.08))
		draw_circle(pos, 11, Color("80ffd7"))
		draw_circle(pos + Vector2(-3, -3), 3, Color("e5fff5"))
	var player := Vector2(LANES[lane], 485)
	if flash > 0: draw_circle(player, 28 + flash * 2, Color(0.5, 1, 0.83, float(flash) / 24.0))
	draw_colored_polygon(PackedVector2Array([player + Vector2(0,-21), player + Vector2(19,16), player + Vector2(0,8), player + Vector2(-19,16)]), Color("a7b5ff"))
	draw_line(Vector2(44, 543), Vector2(916, 543), Color("283653"), 1)
	draw_string(font, Vector2(44, 573), "A / D  OR  ARROW KEYS    •    COLLECT THE MINT ORBS", HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color("9ab0cf"))
	draw_string(font, Vector2(750, 573), "SPACE TO RESTART", HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color("9ab0cf"))
	if not playing:
		draw_rect(Rect2(226, 232, 508, 119), Color("101c34"))
		draw_string(font, Vector2(305, 279), "FIND YOUR RHYTHM", HORIZONTAL_ALIGNMENT_LEFT, -1, 28, Color("e4eeff"))
		draw_string(font, Vector2(345, 316), "PRESS SPACE TO BEGIN", HORIZONTAL_ALIGNMENT_LEFT, -1, 17, Color("80ffd7"))


func gdx_state() -> Dictionary:
	return polish_snapshot()

func polish_replay(frames: int = 180, value: int = 7) -> Dictionary:
	# Called by gdx's RPC, not a second control server. State is paused after replay.
	if frames < 1 or frames > 36000:
		return {"error": "frames must be in [1, 36000]"}
	polish_begin(value)
	for step in range(1, frames + 1): polish_step(step, value)
	return polish_snapshot()
