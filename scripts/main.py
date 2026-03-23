''' Main module to run the game. '''
import arcade
import constants as c
from screens.start_screen import StartScreen

# Create a new arcade window and run the start screen
window = arcade.Window(c.WINDOW_WIDTH, c.WINDOW_HEIGHT, c.TITLE)
start_view = StartScreen()
window.show_view(start_view)
arcade.run()
