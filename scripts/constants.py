''' Module providing constants for the game. '''
import os
import sys
import random
import arcade

def resource_path(relative_path):
    '''
    Gets absolute path to resource for pyinstaller
    '''
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Set window and grid information
ROW_COUNT = 15
COLUMN_COUNT = 15

TILE_SIZE = 30
WINDOW_WIDTH = TILE_SIZE * COLUMN_COUNT
WINDOW_HEIGHT = TILE_SIZE * ROW_COUNT
TITLE = "SEEKER"

# Generation details
LEVEL_SIZE = 100 # Should be >= 15
NUM_START_FOREST_ROWS = 3 # How many grassy rows at the beginning?
NUM_ENDING_FOREST_ROWS = 5 # how many grassy rows at the end?

# River
MIN_LILYPADS_PER_RIVER = 3
SMALLEST_LOG = 2
BIGGEST_LOG = 4
LOG_MOVING_LEFT = random.choice([True, False])

# Cars
TIME_BETWEEN_SPAWNS = 1.0

# SLOW = 2.0, MED = 1.5, FAST = 1.0
TIME_BETWEEN_FAST_LOG_SPAWNS = 1.0
TIME_BETWEEN_MED_LOG_SPAWNS = 1.5
TIME_BETWEEN_SLOW_LOG_SPAWNS = 2.0
MAX_LOG_WAIT_TIME = 4.0
UPPER_OBSTACLE_SPEED = 1.0 # Tiles per second
LOWER_OBSTACLE_SPEED = 0.2 # Tiles per second

# Player info
DIST_UNTIL_STAY_PUT = 3
VELOCITY_MULTIPLIER = TILE_SIZE
STARTING_X = 7
STARTING_Y = 0
ENDING_X = 7
ENDING_Y = LEVEL_SIZE - 1

DEATH_ANIMATION_LENGTH = 2.0
DEATH_ANIMATION_UPDATE_INTERVAL = 0.1


# Log Speed
LOG_SPEED_SLOW = 0.4
LOG_SPEED_MED = 0.3
LOG_SPEED_FAST= 0.2

# Colors
background = arcade.csscolor.SEA_GREEN
start_screen_background = arcade.csscolor.BLACK
game_over_background = arcade.csscolor.BLACK
brennas_favorite_color = arcade.csscolor.DARK_GREEN
blood_mwahaha = arcade.csscolor.RED
victory = arcade.csscolor.GOLD

# Sounds
VOLUME = 5
MIN_VOLUME = 0
MAX_VOLUME = 10

# Sound Effects
ADVENTURE_MUSIC = arcade.load_sound(resource_path("sfx/bear_adventure.mp3"))
WALK_SFX = arcade.load_sound(resource_path("sfx/footstep.mp3"))
DEATH_SFX = arcade.load_sound(resource_path("sfx/death.mp3"))
HUNNY_SFX = arcade.load_sound(resource_path("sfx/hunny_pickup.mp3"))
VICTORY_JINGLE = arcade.load_sound(resource_path("sfx/victory.wav"))
GAME_OVER_JINGLE = arcade.load_sound(resource_path("sfx/game_over.wav"))


# Music
MAIN_THEME = arcade.play_sound(ADVENTURE_MUSIC)
MAIN_THEME.pause()

# Settings
BLINK_RATE = 0.5
DEBUG = False
WINDOW = 'Windowed'
RESOLUTION = 450
RESOLUTION_RATIO = RESOLUTION / 450
SKIN = 'Grizzly'

BLINK_RATE = 0.5
CURRENT_MODE = 'Thirty'
CURRENT_OPTION = 'Play'
