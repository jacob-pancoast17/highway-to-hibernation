''' Module representing the stats screen. '''
import arcade
from scripts import constants as c
from scripts.stats_manager import load_stats


class StatsScreen(arcade.View):
    ''' StatsScreen represents the stats view '''

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
        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.back_text = None

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

    def on_key_press(self, symbol, modifiers):
        '''
        defines key presses

        param:
            self
            symbol - the key
            modifiers - any modifiers (e.g. capslock)
        return:
            nothing
        '''

        if symbol == arcade.key.ENTER or symbol == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

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
            font_size=24 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center'
        )

        high_score.draw()

        prev_score = arcade.Text(
            f"LAST SCORE: {self.stats['last_score']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.46,
            font_size=24 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center'
        )

        prev_score.draw()

        games_played = arcade.Text(
            f"GAMES PLAYED: {self.stats['games_played']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.34,
            font_size=24 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center'
        )

        games_played.draw()

        games_played.draw()

        self.draw_back()

    def draw_back(self):
        '''
        draw_back is a helper function used to draw the back button from the stats
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
