extends Button

# Example: custom initialization or signal connection
func _ready():
	connect("pressed", _on_pressed)

func _on_pressed():
	print("Button pressed:", text)
