extends Control


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_button_fr_pressed():
	print('fr')
	get_tree().change_scene_to_file('res://scenes/menu/LevelSelection.tscn')


func _on_button_jp_pressed():
	print('jp')
	get_tree().change_scene_to_file('res://scenes/menu/LevelSelection.tscn')


func _on_button_en_pressed():
	print('en')
	get_tree().change_scene_to_file('res://scenes/menu/LevelSelection.tscn')
