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
        self.object_list = None

    def setup(self):
        self.object_list = arcade.SpriteList(
            use_spatial_hash=True
        )

        square = arcade.SpriteSolidColor(
            width = 100,
            height = 100,
            center_x = 600,
            center_y = 400,
            color = arcade.csscolor.BLACK,
            angle = 0
        )

        self.object_list.append(square) 

    '''
    on_draw redraws each frame

    param: self
    return: nothing
    '''
    def on_draw(self):
        # Reset window
        self.clear()

        self.object_list.draw()

    def run_window(self):
        self.setup()
        arcade.run()
