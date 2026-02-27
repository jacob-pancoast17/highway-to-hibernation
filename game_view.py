import arcade
import constants as c
import game_over_screen as GameOver
from object import Object

'''
GameView represents a window object
'''
class GameView(arcade.View):
    '''
    Constructor

    param: arcade window
    return: nothing
    '''
    def __init__(self):
        super().__init__()

        self.background_color = c.background
        self.object_list = None

    def setup(self):
        self.object_list = arcade.SpriteList(
            use_spatial_hash=True
        )

        square = Object(size = 100, x = 400, y = 400, color = arcade.csscolor.BLACK)

        self.object_list.append(square.to_sprite()) 

    '''
    on_draw redraws each frame and each object

    param: self
    return: nothing
    '''
    def on_draw(self):
        # Reset window
        self.clear()

        self.object_list.draw()

    '''
    run_window sets up the window and runs it

    param: self
    return: nothing
    '''
    def run_window(self):
        self.setup()
        arcade.run()

    '''
    on_key_press detects when a key is pressed

    param: self
           symbol - key pressed
           modifiers - e.g. capslock or numlock
    '''
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            game_over = GameOver.GameOver()
            self.window.show_view(game_over)