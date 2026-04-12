''' Module representing the stats screen. '''
import arcade
from scripts import constants as c
from scripts.stats_manager import load_stats


class StatsScreen(arcade.View):
    ''' StatsScreen represents the stats view '''

    def __init__(self):
        '''
        Constructor calls arcade 'View' superclass constructor
        
        param:
            self
        returns:
            nothing
        '''
        super().__init__()

        self.stats = load_stats()

        self.title_text = arcade.Text(
            "PERSONAL STATS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.78,
            font_size=40,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.back_text = arcade.Text(
            "Press ESC to go back",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.08,
            font_size=16,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

    def on_show_view(self):
        '''
        on_show_view defines events that happen when switching to the stats screen
        
        param:
            self
        returns:
            nothing
        '''
        self.window.default_camera.use()

    def on_draw(self):
        '''
        on_draw redraws the stats screen

        param:
            self
        returns:
            nothing
        '''
        self.clear()

        self.title_text.draw()

        high_score = arcade.Text(
            f"HIGH SCORE: {self.stats['high_score']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.58,
            font_size=24,
            font_name="Edit Undo BRK",
            anchor_x='center'
        )

        high_score.draw()

        prev_score = arcade.Text(
            f"LAST SCORE: {self.stats['last_score']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.46,
            font_size=24,
            font_name="Edit Undo BRK",
            anchor_x='center'
        )

        prev_score.draw()

        games_played = arcade.Text(
            f"GAMES PLAYED: {self.stats['games_played']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.34,
            font_size=24,
            font_name="Edit Undo BRK",
            anchor_x='center'
        )

        games_played.draw()

        self.back_text.draw()

    def on_key_press(self, symbol, modifiers):
        '''
        on_key_press detects when a key is pressed

        param: self
        symbol - key pressed
        modifiers - e.g. capslock or numlock
        '''
        if symbol == arcade.key.ESCAPE:
            from scripts.screens.start_screen import StartScreen
            self.window.show_view(StartScreen())
