''' Module representing the game over screen. '''
import arcade
import constants as c


class GameOver(arcade.View):
    ''' GameOver represents the game over view '''
    # Constructor calls arcade 'View' superclass constructor
    # param: self
    # return: nothing

    def __init__(self):
        super().__init__()


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
            "GAME OVER",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 3 / 4,
            font_size = 50,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "Click to play again",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2,
            font_size = 20,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "or press 'E' to exit the program.",
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
        from game_view import GameView
        self.window.show_view(GameView())


    # on_key_press detects when the E key is pressed
    # and closes the game window

    # param: self
     #      symbol - key pressed
     #      modifiers - e.g. capslock or numlock

    def on_key_press(self, symbol):
        if symbol == arcade.key.E:
            self.window.close()
