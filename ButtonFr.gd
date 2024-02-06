func _ready():
	self.connect("pressed", self, "_on_Button_pressed")

func _on_Button_pressed():
	print("The button has been pressed!")
