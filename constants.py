import arcade

# Set how many rows and columns we will have
ROW_COUNT = 15
COLUMN_COUNT = 15


# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30


# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

WINDOW_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
WINDOW_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
TITLE = "Highway to Hibernation"

# Colors
background = arcade.csscolor.SEA_GREEN
start_screen_background = arcade.csscolor.BLACK
game_over_background = arcade.csscolor.BLACK