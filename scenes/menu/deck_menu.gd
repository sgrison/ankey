extends Control

var db: SQLite


func _ready():
	# Open the database
	db = SQLite.new()
	db.path = "res://data.db"
	db.open_db()
	
	# Fetch deck names from the database
	db.query("SELECT DeckName, DeckID FROM Decks")
	
	# Reference to the VBoxContainer inside the ScrollContainer
	var vbox = $CenterContainer/VBoxContainer 
	
	# Loop through the query results and create buttons
	for result in db.query_result:
		
		print(result)
		var button = Button.new()
		button.text = result["DeckName"]  # Assuming 'DeckName' is the column name
		button.set_meta("DeckID", result["DeckID"])
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL  # Make button expand to fill the container width
		button.connect("pressed", _on_Button_pressed.bind(button))
		vbox.add_child(button)


func _on_Button_pressed(button: Button):
	Global.selected_deck_name = button.text
	Global.selected_deck_id = button.get_meta("DeckID")
	get_tree().change_scene_to_file("res://scenes/menu/level_menu.tscn")
