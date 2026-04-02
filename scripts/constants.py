''' Module providing constants for the game. '''
import arcade

# Set window and grid information
ROW_COUNT = 15
COLUMN_COUNT = 15

TILE_WIDTH = 30
TILE_HEIGHT = 30
TILE_SIZE = 30
MARGIN = 0
WINDOW_WIDTH = TILE_WIDTH * COLUMN_COUNT
WINDOW_HEIGHT = TILE_HEIGHT * ROW_COUNT
TITLE = "SEEKER"

# Generation details
LEVEL_SIZE = 30 # Should be >= 15
NUM_START_GRASSY_ROWS = 3 # How many grassy rows at the beginning?
NUM_ENDING_GRASSY_ROWS = 5 # how many grassy rows at the end?

## River
MIN_LILYPADS_PER_RIVER = 3
SMALLEST_LOG = 2
BIGGEST_LOG = 4

## Cars
TIME_BETWEEN_SPAWNS = 1.0
TIME_BETWEEN_LOG_SPAWNS = 2.0
UPPER_OBSTACLE_SPEED = 1.0 # Tiles per second
LOWER_OBSTACLE_SPEED = 0.2 # Tiles per second

# Player info
DIST_UNTIL_STAY_PUT = 3
VELOCITY_MULTIPLIER = TILE_HEIGHT
STARTING_X = 7
STARTING_Y = 0
ENDING_X = 7
ENDING_Y = LEVEL_SIZE - 1


## Log Speed
LOG_SPEED_SLOW = 0.5
LOG_SPEED_MED = 0.3
LOG_SPEED_FAST= 0.2

# Colors
background = arcade.csscolor.SEA_GREEN
start_screen_background = arcade.csscolor.BLACK
game_over_background = arcade.csscolor.BLACK
brennas_favorite_color = arcade.csscolor.DARK_GREEN
blood_mwahaha = arcade.csscolor.RED
victory = arcade.csscolor.GOLD

# Fonts
arcade.load_font("fonts/edit-undo.brk.ttf")
