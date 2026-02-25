import arcade
import constants as c
import game_view as GameView
import screen as Screen

# Create a GameView and run it
window = arcade.Window(c.WIDTH, c.HEIGHT, c.TITLE)
start_view = Screen.StartScreen()
window.show_view(start_view)
arcade.run()

# GameView.GameView()
# window.show_view(start_view)
# start_view.run_window()