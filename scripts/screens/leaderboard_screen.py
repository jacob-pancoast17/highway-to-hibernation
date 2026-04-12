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

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

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

        leaderboard = arcade.Text(
            "LEADERBOARD",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.86,
            font_name="Edit Undo BRK",
            font_size=32,
            anchor_x="center"
        )

        leaderboard.draw()

        if not self.scores:
            no_score = arcade.Text(
                "No scores found",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.55,
                font_name="Edit Undo BRK",
                font_size=22,
                anchor_x="center"
            )

            no_score.draw()

        else:
            y_pos = c.WINDOW_HEIGHT * 0.76
            for i, entry in enumerate(self.scores, start=1):
                score = arcade.Text(
                    f"{i}. {entry['name']} - {entry['score']}",
                    x=c.WINDOW_WIDTH / 2,
                    y=y_pos,
                    font_name="Edit Undo BRK",
                    font_size=18,
                    anchor_x="center"
                )
                score.draw()
                y_pos -= 26

        self.draw_back()

    def on_key_press(self, symbol, modifiers):
        '''
        on_key_press detects when a key is pressed

        param:
            self
            symbol - key pressed
            modifiers - e.g. capslock or numlock
        returns:
            nothing
        '''
        if symbol == arcade.key.ENTER or symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

    def on_update(self, delta_time):
        '''
        Happens every frame

        param:
            self
            delta_time - time passed since last on_update
        return:
            nothing
        '''

        self.time_elapsed += delta_time

        if self.time_elapsed > self.next_blink:

            self.next_blink += c.BLINK_RATE

            self.blink()

    def draw_back(self):
        '''
        draw_back is a helper function used to draw the back button from the leaderboard
        screen

        param:
            self
        returns:
            nothing
        '''
        if self.blinked:

            back_text = arcade.Text(
                "BACK",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.08,
                font_size=30 * c.RESOLUTION_RATIO,
                font_name="Edit Undo BRK",
                anchor_x='center',
                anchor_y='center',
                color = arcade.csscolor.BLACK
            )

            arcade.draw_rect_filled(
                arcade.XYWH(back_text.x,
                back_text.y,
                back_text.content_width + (6 * c.RESOLUTION_RATIO),
                back_text.content_height),
                arcade.csscolor.WHITE)

        else:

            back_text = arcade.Text(
                "BACK",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.08,
                font_size=30 * c.RESOLUTION_RATIO,
                font_name="Edit Undo BRK",
                anchor_x='center',
                anchor_y='center'
            )

        back_text.draw()

    def blink(self):
        '''
        blink takes the variable blinked and changes it on or off depending on what the
        current value is

        param:
            self
        returns:
            nothing
        '''

        if self.blinked is False:

            self.blinked = True

        else:
            self.blinked = False
