''' Module representing the pause screen. '''
import arcade
from scripts import constants as c
from scripts.screens.stats_screen import StatsScreen

class Pause(arcade.View):
    '''
    Constructor calls arcade 'View' superclass constructor

    param:
        self
    returns:
        nothing
    '''
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.pause_spr = arcade.Sprite(
            path_or_texture= "sprites/pause_graphic.png",
            scale = 1.25,
            center_x = c.WINDOW_WIDTH / 2,
            center_y = c.WINDOW_HEIGHT / 2,
            angle = 180.0
        )
        self.sprites = arcade.SpriteList()
        self.sprites.append(self.pause_spr)

        self.pause_text = arcade.Text(
            "PAUSE",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 3 / 5,
            font_size = 50,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.continue_text = arcade.Text(
            "Press 'ESC' to continue",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.1,
            font_size = 18,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.quit_text = arcade.Text(
            "Press 'Q' to quit",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.4,
            font_size = 18,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.reset_text = arcade.Text(
            "Press 'ENTER' to reset",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.8,
            font_size = 18,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.stats_text = arcade.Text(
            "Press 'S' for stats",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 3.4,
            font_size = 18,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )


    def on_show_view(self):
        '''
        on_show_view defines events that happen when switching to the game over screen

        param:
            self
        returns:
            nothing
        '''
        # Reset view
        self.window.default_camera.use()


    def on_draw(self):
        '''
        on_draw redraws the pause screen

        param:
            self
        returns:
            nothing
        '''
        self.clear()
        self.sprites.draw()

        self.pause_text.draw()
        self.continue_text.draw()
        self.quit_text.draw()
        self.reset_text.draw()
        self.stats_text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        if symbol == arcade.key.Q:
            self.window.close()
        if symbol == arcade.key.ENTER:
            self.window.show_view(self.game_view.__class__())
        if symbol == arcade.key.S:
            self.window.show_view(StatsScreen(self))
