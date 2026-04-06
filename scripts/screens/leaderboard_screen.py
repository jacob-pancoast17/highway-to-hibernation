import arcade
from scripts import constants as c
from scripts.firebase_leaderboard import get_top_scores


class LeaderboardScreen(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        self.scores = get_top_scores(10)

    def on_show_view(self):
        self.window.default_camera.use()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "LEADERBOARD",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.82,
            font_name="Edit Undo BRK",
            font_size=36,
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
            y_pos = c.WINDOW_HEIGHT * 0.68
            for i, entry in enumerate(self.scores, start=1):
                arcade.draw_text(
                    f"{i}. {entry['name']} - {entry['score']}",
                    x=c.WINDOW_WIDTH / 2,
                    y=y_pos,
                    font_name="Edit Undo BRK",
                    font_size=22,
                    anchor_x="center"
                )
                y_pos -= 35

        arcade.draw_text(
            "Press ESC to go back",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.08,
            font_name="Edit Undo BRK",
            font_size=16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)
