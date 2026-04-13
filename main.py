''' Main module to run the game. '''
import arcade
import sys
import os
from scripts import constants as c
from scripts.screens.start_screen import StartScreen

def resource_path(relative_path):
    '''
    Gets absolute path to resource for pyinstaller
    '''
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load the game font
arcade.load_font(resource_path("fonts/edit-undo.brk.ttf"))

# Create a new arcade window and run the start screen
window = arcade.Window(c.WINDOW_WIDTH, c.WINDOW_HEIGHT, c.TITLE)

# Start the game view
start_view = StartScreen()
window.main_menu_view = start_view
window.show_view(start_view)
arcade.run()


