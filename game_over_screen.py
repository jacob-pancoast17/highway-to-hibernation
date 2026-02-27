import arcade
import constants as c
import game_view as GameView
import sys

class GameOver(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        # Set background color
        self.window.background_color = c.game_over_background

        # Reset view
        self.window.default_camera.use()

    def on_draw(self):
        # reset window
        self.clear()

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "GAME OVER",
            x = c.WIDTH / 2,
            y = c.HEIGHT * 3 / 4,
            font_size = 50,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "Click to play again",
            x = c.WIDTH / 2,
            y = c.HEIGHT / 2,
            font_size = 20,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "or press 'E' to exit the program.",
            x = c.WIDTH / 2,
            y = (c.HEIGHT / 2)-30,
            font_size = 20,
            anchor_x = 'center',
            anchor_y = 'center'
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView.GameView()
        self.window.show_view(game_view)
        self.windo.run_window()

    def on_key_press(self, symbol, modifier):
        if symbol == arcade.key.E:
            self.window.close()