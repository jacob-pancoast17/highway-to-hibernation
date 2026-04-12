''' Module representing the pause screen. '''
import arcade
from scripts import constants as c
from scripts.screens.settings_screen import Settings
from scripts.screens.leaderboard_screen import LeaderboardScreen

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
        self.initialize()

    def initialize(self):
        '''
        initialize is part of the pause screen's constructor, but has a special property.
        initialize only sets logic that is dependent on the size of the screen, which must
        be updated every time the user changes the resolution in settings.

        param:
            self
        returns:
            nothing
        '''
        self.pause_spr = arcade.Sprite(
            path_or_texture= "sprites/pause_graphic.png",
            scale = 1.25 * c.RESOLUTION_RATIO,
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
            font_size = 50 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.continue_text = arcade.Text(
            "Press 'ESC' to continue",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.1,
            font_size = 18 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.quit_text = arcade.Text(
            "Press 'Q' to quit",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.4,
            font_size = 18 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.reset_text = arcade.Text(
            "Press 'ENTER' to reset",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.8,
            font_size = 18 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.stats_text = arcade.Text(
            "Press 'S' for stats",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 3.4,
            font_size = 18 * c.RESOLUTION_RATIO,
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

    
        arcade.draw_text(
            "PAUSE",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 3 / 5,
            font_size = 50,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "Press 'ESC' to continue",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.1,
            font_size = 17,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        # TODO: Change to text objects, same in start_screen

        arcade.draw_text(
            "Press 'ENTER' to restart",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2.4,
            font_size = 17,
            anchor_x = 'center',
            anchor_y = 'center'
        )



        arcade.draw_text(
            "Press 'M' to return to main menu",
            font_name="Edit Undo BRK",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 2.8,
            font_size=17,
            anchor_x='center',
            anchor_y='center'
        )

        arcade.draw_text(
            "Press 'S' for stats",
            font_name="Edit Undo BRK",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 3.4,
            font_size=17,
            anchor_x='center',
            anchor_y='center'
        )

    def on_key_press(self, symbol, modifiers):
        print(symbol)
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
            self.game_view.initialize()
        if symbol == arcade.key.ENTER:
            self.window.show_view(self.game_view.__class__())
        if symbol == arcade.key.M:
            from scripts.screens.start_screen import StartScreen
            self.window.show_view(StartScreen())
        if symbol == arcade.key.L:
            self.window.show_view(LeaderboardScreen(self))
        
        elif symbol == arcade.key.F:
            self.window.show_view(Settings(self, True))
