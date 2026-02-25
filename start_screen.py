import arcade
import constants as c
import game_view as GameView

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        # Set background color
        self.window.background_color == c.start_screen_background

        # Reset view
        self.window.default_camera.use()

    def on_draw(self):
        # Reset window
        self.clear()

        arcade.draw_text("Highway to Hibernation", 
                         x = c.WIDTH / 2, 
                         y = c.HEIGHT * 3 / 4,
                         font_size = 50,
                         anchor_x = "center",
                         anchor_y = "center")
        
        arcade.draw_text("Click to begin",
                         x = c.WIDTH / 2,
                         y = c.HEIGHT / 2,
                         font_size = 20,
                         anchor_x = "center",
                         anchor_y = "center")
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView.GameView()
        self.window.show_view(game_view)
        game_view.run_window()
