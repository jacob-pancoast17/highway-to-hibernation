'''This module is used to create the screen used to display the leaderboard'''
import arcade
from scripts import constants as c
from scripts.firebase_leaderboard import get_top_scores


class LeaderboardScreen(arcade.View):
    '''
    LeaderboardScreen represents the leaderboard view
    '''

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
        self.scores = get_top_scores(10)

    def on_show_view(self):
        '''
        on_show_view defines events that happen when switching to the game over screen
        
        param:
            self
        returns:
            nothing
        '''
        self.window.default_camera.use()

    def on_draw(self):
        '''
        Render the screen every frame

        param:
            self
        returns:
            nothing
        '''
        
        self.clear()

        arcade.draw_text(
            "LEADERBOARD",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.86,
            font_name="Edit Undo BRK",
            font_size=32,
            anchor_x="center"
        )

        if not self.scores:
            arcade.draw_text(
                "No scores found",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.55,
                font_name="Edit Undo BRK",
                font_size=22,
                anchor_x="center"
            )
        else:
            y_pos = c.WINDOW_HEIGHT * 0.76
            for i, entry in enumerate(self.scores, start=1):
                arcade.draw_text(
                    f"{i}. {entry['name']} - {entry['score']}",
                    x=c.WINDOW_WIDTH / 2,
                    y=y_pos,
                    font_name="Edit Undo BRK",
                    font_size=18,
                    anchor_x="center"
                )
                y_pos -= 26


        arcade.draw_text(
            "Press 'ESC' for previous screen",
            font_name="Edit Undo BRK",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.15,
            font_size=17,
            anchor_x='center',
            anchor_y='center'
        )

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
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)
