''' Module representing the stats screen. '''
import arcade
from scripts import constants as c
from scripts.firebase_leaderboard import get_player_stats
from scripts.screens.start_screen import StartScreen


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

        self.player_name = ""
        self.stats_loaded = False
        self.stats = {
            "name": "",
            "high_score": 0,
            "last_score": 0,
            "games_played": 0
        }

        self.title_text = arcade.Text(
            "PERSONAL STATS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.78,
            font_size=40,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.prompt_text = arcade.Text(
            "ENTER YOUR INITIALS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.60,
            font_size=22,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.name_text = arcade.Text(
            "_ _ _",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.52,
            font_size=28,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.enter_text = arcade.Text(
            "Press ENTER to view stats",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.44,
            font_size=18,
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

        if not self.stats_loaded:
            self.prompt_text.draw()
            self.name_text.draw()
            self.enter_text.draw()
        else:
            arcade.draw_text(
                f"PLAYER: {self.stats['name']}",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.58,
                font_size=24,
                font_name="Edit Undo BRK",
                anchor_x='center'
            )

            arcade.draw_text(
                f"HIGH SCORE: {self.stats['high_score']}",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.48,
                font_size=24,
                font_name="Edit Undo BRK",
                anchor_x='center'
            )

            arcade.draw_text(
                f"LAST SCORE: {self.stats['last_score']}",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.38,
                font_size=24,
                font_name="Edit Undo BRK",
                anchor_x='center'
            )

            arcade.draw_text(
                f"GAMES PLAYED: {self.stats['games_played']}",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.28,
                font_size=24,
                font_name="Edit Undo BRK",
                anchor_x='center'
            )

        self.back_text.draw()

    def on_key_press(self, symbol, modifiers):
        '''
        on_key_press detects when a key is pressed

        param: self
           symbol - key pressed
           modifiers - e.g. capslock or numlock
        '''
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(StartScreen())

        elif not self.stats_loaded:
            if symbol == arcade.key.ENTER:
                name = self.player_name.strip()
                if not name:
                    name = "Player"

                self.stats = get_player_stats(name)
                self.stats_loaded = True

            elif symbol == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
                self.name_text.text = " ".join(self.player_name) if self.player_name else "_ _ _"

            else:
                if len(self.player_name) < 3 and 97 <= symbol <= 122:
                    self.player_name += chr(symbol).upper()
                    self.name_text.text = " ".join(self.player_name)
                elif len(self.player_name) < 3 and 65 <= symbol <= 90:
                    self.player_name += chr(symbol)
                    self.name_text.text = " ".join(self.player_name)
