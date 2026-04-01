''' Module representing obstacle objects in the game. '''
import arcade
from scripts import constants as c

class Den(arcade.Sprite):
    '''
    A den object is a derivative of the object class, if the player touches it they win the game!
    '''

    def __init__ (self, texture, column, row):
        '''
        Constructor creates a den object (victory!)

        param: 
            self
            texture - the den texture
            column - x to spawn at
            row - y to spawn at
        returns:
            nothing
        '''
        super().__init__(path_or_texture=texture)

        self.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0
