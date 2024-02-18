extends AudioStreamPlayer

# Define variables to store the minimum and maximum delay before playing the music
var min_delay = 5
var max_delay = 15

func _ready():
	# Call the function to start playing the music
	play_music()

# Function to play the music
func play_music():
	# Set a random delay before playing the music
	var delay = randf_range(min_delay, max_delay)
	get_tree().create_timer(delay).timeout

	# Load the music resource
	var music = load("res://musics/lofi.mp3")

	# Set the music to loop
	stream = music
	autoplay = true

	# Start playing the music
	play()

# Function to handle the end of the music
func _on_finished():
	# If the music finishes, play it again
	play_music()
