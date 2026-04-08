import arcade
from scripts import constants as c


class Settings(arcade.View):
    def __init__(self, previous_view):

        super().__init__()

        self.previous_view = previous_view

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.options = list(range(1))
        self.selected = self.options[0]

    def on_show_view(self):
        self.window.default_camera.use()

    def on_update(self, delta_time):
        '''
        Happens every frame
        '''

        self.time_elapsed += delta_time

        if self.time_elapsed > self.next_blink:

            self.next_blink += c.BLINK_RATE

            self.blink()

    def on_draw(self):
        self.clear()

        self.draw_settings()
        self.draw_volume()
        
        self.draw_escape()        

    def draw_settings(self):

        arcade.draw_text(
            "SETTINGS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.82,
            font_name="Edit Undo BRK",
            font_size=40,
            anchor_x="center")
    
    def draw_volume(self):

        if self.blinked:
        
            volume_title = arcade.Text(
                "VOLUME",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.70,
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK)
            
            arcade.draw_rect_filled(
                arcade.XYWH(c.WINDOW_WIDTH / 2,
                c.WINDOW_HEIGHT * 0.70,
                volume_title.content_width,
                volume_title.content_height),
                arcade.csscolor.WHITE
            )
            
            volume_title.draw()
        
        else:

            volume_title = arcade.Text(
                "VOLUME",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.70,
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)
            volume_title.draw()

    def draw_escape(self):

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

    def blink(self):

        if self.blinked == False:

            self.blinked = True

        else:
            self.blinked = False

        