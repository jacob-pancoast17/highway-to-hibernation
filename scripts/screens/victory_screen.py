''' Module representing the victory screen. '''
import arcade
from scripts import constants as c


class Victory(arcade.View):
    ''' Victory represents the game over view '''
    # Constructor calls arcade 'View' superclass constructor
    # param: self
    # return: nothing

    def __init__(self, score, previous_view):
        super().__init__()
        self.score = score
        self.previous_view = previous_view


    # on_show_view defines events that happen when switching to the game over screen
    # param: self
    # return: nothing
    def on_show_view(self):
        # Set background color
        self.window.background_color = c.game_over_background

        # Reset view
        self.window.default_camera.use()


    # on_draw redraws the game over screen

    # param: self
    # return: nothing

    def on_draw(self):
        # reset window
        self.clear()

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "VICTORY!",
            font_name="Edit Undo BRK",
            color= c.victory,
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 3 / 4,
            font_size = 50,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        arcade.draw_text(
            f"SCORE: {self.score}",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 5 / 8,
            font_size = 30,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "Click to play again",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2,
            font_size = 20,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "or press 'Q' to quit",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = (c.WINDOW_HEIGHT / 2)-30,
            font_size = 20,
            anchor_x = 'center',
            anchor_y = 'center'
        )

    # on_mouse_press detects when the mouse is pressed and
    # changes the view to the game view again to restart

    # param: self
     #      _x - cursor x pos
     #      _y - cursor y pos
     #     _button - button on mouse pressed
     #     _modifiers - shift, ctrl, numlock, etc.
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(self.previous_view.__class__())


    # on_key_press detects when the E key is pressed
    # and closes the game window

    # param: self
     #      symbol - key pressed
     #      modifiers - e.g. capslock or numlock

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            self.window.close()
