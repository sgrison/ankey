extends Control

var db: SQLite


func _ready():
	# Open the database
	db = SQLite.new()
	db.path = "res://data.db"
	db.open_db()
	
	# Fetch deck names from the database
	var selected_deck_name = Global.selected_deck_name
	var selected_deck_id = Global.selected_deck_id
	print(selected_deck_name)
	print(selected_deck_id)
	
	# Fetch deck names from the database
	db.query_with_bindings("SELECT LevelName FROM Levels WHERE DeckID = ?", [selected_deck_id])
	
	# Reference to the VBoxContainer inside the ScrollContainer
	var vbox = $CenterContainer/VBoxContainer 
	
	# Loop through the query results and create buttons
	for result in db.query_result:
		var button = Button.new()
		button.text = result["LevelName"]  # Assuming 'DeckName' is the column name
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL  # Make button expand to fill the container width
		button.connect("pressed", _on_Button_pressed.bind(button))
		vbox.add_child(button)


func _on_Button_pressed(button: Button):
	print()
