''' Module representing the game over screen. '''
import arcade
from scripts import constants as c
from scripts.screens.stats_screen import StatsScreen


class GameOver(arcade.View):
    ''' GameOver represents the game over view '''

    def __init__(self, previous_view):
        '''
        Constructor calls arcade 'View' superclass constructor
        
        param:
            self
        returns:
            nothing
        '''
        super().__init__()
        self.previous_view = previous_view

    def on_show_view(self):
        '''
        on_show_view defines events that happen when switching to the game over screen
        
        param:
            self
        returns:
            nothing
        '''
        # Set background color
        self.window.background_color = c.game_over_background

        # Reset view
        self.window.default_camera.use()

    def on_draw(self):
        '''
        on_draw redraws the game over screen

        param:
            self
        returns:
            nothing
        '''
        # reset window
        self.clear()

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "YOU ARE DEAD",
            font_name="Edit Undo BRK",
            color= c.blood_mwahaha,
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 3 / 4,
            font_size = 50,
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

        arcade.draw_text(
            "Press 'S' for stats",
            font_name="Edit Undo BRK",
            x=c.WINDOW_WIDTH / 2,
            y=(c.WINDOW_HEIGHT / 2) - 60,
            font_size=20,
            anchor_x='center',
            anchor_y='center'
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
        if symbol == arcade.key.S:
            self.window.show_view(StatsScreen(self))
