''' Module providing constants for the game. '''
import arcade

# Set how many rows and columns we will have
ROW_COUNT = 15
COLUMN_COUNT = 15


# This sets the WIDTH and HEIGHT of each grid location
TILE_WIDTH = 30
TILE_HEIGHT = 30
TILE_SIZE = 30

# Modifiers
TIME_BETWEEN_SPAWNS = 1.0
UPPER_OBSTACLE_SPEED = 1.0 # Tiles per second
LOWER_OBSTACLE_SPEED = 0.2 # Tiles per second

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 0

# Player info
VELOCITY_MULTIPLIER = TILE_HEIGHT + MARGIN
STARTING_X = 7
STARTING_Y = 0

WINDOW_WIDTH = (TILE_WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
WINDOW_HEIGHT = (TILE_HEIGHT + MARGIN) * ROW_COUNT + MARGIN
TITLE = "Highway to Hibernation"

MIN_LILYPADS_PER_RIVER = 3

# Colors
background = arcade.csscolor.SEA_GREEN
start_screen_background = arcade.csscolor.BLACK
game_over_background = arcade.csscolor.BLACK
brennas_favorite_color = arcade.csscolor.DARK_GREEN
blood_mwahaha = arcade.csscolor.RED

# Fonts
arcade.load_font("fonts/edit-undo.brk.ttf")
