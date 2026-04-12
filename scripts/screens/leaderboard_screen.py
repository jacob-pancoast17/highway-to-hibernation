import arcade
from scripts import constants as c
from scripts.firebase_leaderboard import get_top_scores


class LeaderboardScreen(arcade.View):
    def __init__(self, previous_view):
        super().__init__()

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.previous_view = previous_view
        self.scores = get_top_scores(10)

    def on_show_view(self):
        self.window.default_camera.use()

    def on_draw(self):
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

        self.draw_back()

    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.ENTER or key == arcade.key.ESCAPE:
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