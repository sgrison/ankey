extends Sprite2D


@onready var prompt = $RichTextLabel
@onready var prompt_text = prompt.text # remove tags


func get_prompt() -> String:
	return prompt_text
