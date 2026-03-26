''' Module providing constants for the game. '''
import arcade

# Set window and grid information
ROW_COUNT = 15
COLUMN_COUNT = 15

TILE_WIDTH = 30
TILE_HEIGHT = 30
TILE_SIZE = 30

WINDOW_WIDTH = TILE_WIDTH * COLUMN_COUNT
WINDOW_HEIGHT = TILE_HEIGHT * ROW_COUNT
TITLE = "SEEKER"

# Player info
VELOCITY_MULTIPLIER = TILE_HEIGHT
STARTING_X = 7
STARTING_Y = 0

# Generation details
## River
MIN_LILYPADS_PER_RIVER = 3
SMALLEST_LOG = 1
BIGGEST_LOG = 4

## Cars
TIME_BETWEEN_SPAWNS = 1.0
UPPER_OBSTACLE_SPEED = 1.0 # Tiles per second
LOWER_OBSTACLE_SPEED = 0.2 # Tiles per second

# Colors
background = arcade.csscolor.SEA_GREEN
start_screen_background = arcade.csscolor.BLACK
game_over_background = arcade.csscolor.BLACK
brennas_favorite_color = arcade.csscolor.DARK_GREEN
blood_mwahaha = arcade.csscolor.RED

# Fonts
arcade.load_font("fonts/edit-undo.brk.ttf")
