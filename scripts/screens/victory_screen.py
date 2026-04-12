''' Module representing the victory screen. '''
import arcade
from scripts import constants as c
from scripts.screens.leaderboard_screen import LeaderboardScreen


class Victory(arcade.View):
    '''
    Victory represents the game over view
    '''

    def __init__(self, score, previous_view):
        '''
        Constructor calls arcade 'View' superclass constructor
        
        param:
            self
        returns:
            nothing
        '''
        super().__init__()
        self.score = score
        self.previous_view = previous_view

        self.victory_text = arcade.Text(
            "VICTORY!",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 3 / 4,
            color = c.victory,
            font_size = 50,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.score_text = arcade.Text(
            f"SCORE: {self.score}",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 5 / 8,
            font_size = 30,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.play_again_text = arcade.Text(
            "Click to play again",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2,
            font_size = 18,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.quit_text = arcade.Text(
            "Press 'Q' to quit",
            x = c.WINDOW_WIDTH / 2,
            y = (c.WINDOW_HEIGHT / 2)-30,
            font_size = 18,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )
        self.stats_text = arcade.Text(
            "Press 'S' for stats",
            x=c.WINDOW_WIDTH / 2,
            y=(c.WINDOW_HEIGHT / 2) - 60,
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

        arcade.stop_sound(c.MAIN_THEME)

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
            "Press 'M' to return to main menu",
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

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        '''
        on_mouse_press detects when the mouse is pressed and
        changes the view to the game view again to restart

        param:
            self
            _x - cursor x pos
            _y - cursor y pos
            _button - button on mouse pressed
            _modifiers - shift, ctrl, numlock, etc.
        returns:
            nothing
        '''
        self.window.show_view(self.previous_view.__class__())

    def on_key_press(self, symbol, modifiers):
        '''
        on_key_press detects when the E key is pressed
        and closes the game window

        param:
            self
            symbol - key pressed
            modifiers - e.g. capslock or numlock
        returns:
            nothing
        '''
        if symbol == arcade.key.M:
            from scripts.screens.start_screen import StartScreen
            self.window.show_view(StartScreen())
        if symbol == arcade.key.S:
            self.window.show_view(LeaderboardScreen(self))
