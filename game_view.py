import arcade
import constants as c

'''
GameView represents a window object
'''
class GameView(arcade.Window):
    '''
    Constructor

    param: arcade window
    return: nothing
    '''
    def __init__(self):
        super().__init__(c.WIDTH, c.HEIGHT, c.TITLE)

        self.background_color = c.background

    '''
    on_draw redraws each frame

    param: self
    return: nothing
    '''
    def on_draw(self):
        self.clear()

    def run_window(self):
        self.setup()
        arcade.run()
