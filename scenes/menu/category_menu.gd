extends ScrollContainer

@export var growthtime = 10.0
@export var card_scale = 1
@export var card_current_scale = 1.3
@export var scroll_duration = 1.3

var card_current_index: int = 0
var card_x_positions: Array = []

# Ensure these paths accurately reflect your scene structure.
@onready var margin_r: int = $CenterContainer/MarginContainer.custom_constants["margin_right"]
@onready var card_space: int = $CenterContainer/MarginContainer/HBoxContainer.custom_constants["separation"]
@onready var card_nodes: Array = $CenterContainer/MarginContainer/HBoxContainer.get_children()

func _ready() -> void:
	# Initiating asynchronous setup
	start_async_init()

async func start_async_init() -> void:
	await get_tree().idle_frame

	# Corrected method name for accessing the horizontal scrollbar
	get_h_scroll_bar().modulate.a = 0
	
	for _card in card_nodes:
		var _card_pos_x: float = (margin_r + _card.rect_position.x) - ((rect_size.x - _card.rect_size.x) / 2)
		_card.rect_pivot_offset = _card.rect_size / 2
		card_x_positions.append(_card_pos_x)
		
	scroll_horizontal = card_x_positions[card_current_index]
	scroll()

func _process(delta: float) -> void:
	for _index in range(card_x_positions.size()):
		var _card_pos_x: float = card_x_positions[_index]
		var _swipe_length: float = card_nodes[_index].rect_size.x / 2 + card_space / 2
		var _swipe_current_length: float = abs(_card_pos_x - scroll_horizontal)
		var _card_scale: float = lerp(card_scale, card_current_scale, _swipe_current_length / _swipe_length) if _swipe_length != 0 else card_scale
		var _card_opacity: float = lerp(0.3, 1, _swipe_current_length / _swipe_length) if _swipe_length != 0 else 1
		
		card_nodes[_index].rect_scale = Vector2(_card_scale, _card_scale)
		card_nodes[_index].modulate.a = _card_opacity

		if _swipe_current_length < _swipe_length:
			card_current_index = _index

func scroll() -> void:
	var tween = create_tween()
	tween.tween_property(self, "scroll_horizontal", card_x_positions[card_current_index], scroll_duration, Tween.TRANS_BACK, Tween.EASE_OUT)
	
	for _index in range(card_nodes.size()):
		var _card_scale = card_current_scale if _index == card_current_index else card_scale
		tween.tween_property(card_nodes[_index], "rect_scale", Vector2(_card_scale, _card_scale), scroll_duration, Tween.TRANS_QUAD, Tween.EASE_OUT)
	
	tween.start()

func _on_ScrollContainer_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == BUTTON_LEFT:
		if event.pressed:
			stop_all_tweens()
		else:
			scroll()
