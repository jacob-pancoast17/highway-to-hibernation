import arcade
from scripts import constants as c
from scripts.stats_manager import load_stats


class StatsScreen(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        self.stats = load_stats()

    def on_show_view(self):
        self.window.default_camera.use()

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "STATS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.82,
            font_name="Edit Undo BRK",
            font_size=40,
            anchor_x="center"
        )

        arcade.draw_text(
            f"High Score: {self.stats['high_score']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.66,
            font_name="Edit Undo BRK",
            font_size=24,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Last Score: {self.stats['last_score']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.58,
            font_name="Edit Undo BRK",
            font_size=24,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Games Played: {self.stats['games_played']}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.50,
            font_name="Edit Undo BRK",
            font_size=24,
            anchor_x="center"
        )

        arcade.draw_text(
            "Top 5 Scores",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.38,
            font_name="Edit Undo BRK",
            font_size=28,
            anchor_x="center"
        )

        y_pos = c.WINDOW_HEIGHT * 0.30
        for i, score in enumerate(self.stats["top_scores"], start=1):
            arcade.draw_text(
                f"{i}. {score}",
                x=c.WINDOW_WIDTH / 2,
                y=y_pos,
                font_name="Edit Undo BRK",
                font_size=20,
                anchor_x="center"
            )
            y_pos -= 30

        arcade.draw_text(
            "Press ESC to go back",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.08,
            font_name="Edit Undo BRK",
            font_size=16,
            anchor_x="center"
        )

    def on_key_press(self, key):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)