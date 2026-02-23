import arcade
import constants as c

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(c.WIDTH, c.HEIGHT, c.TITLE)

        self.background_color = c.background

    '''
    on_draw draws each frame.

    param: self
    return: nothing
    '''
    def on_draw(self):
        self.clear()

    def run_window(self):
        self.setup()
        arcade.run()
