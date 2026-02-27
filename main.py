import arcade
import constants as c
import game_view as GameView
import start_screen as Screen
import time

# Create a GameView and run it
window = arcade.Window(c.WINDOW_WIDTH, c.WINDOW_HEIGHT, c.TITLE)
start_view = Screen.StartScreen()
window.show_view(start_view)
arcade.run()
