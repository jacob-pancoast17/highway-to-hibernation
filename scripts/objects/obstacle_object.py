''' Module representing obstacle objects in the game.'''
import arcade
from scripts import constants as c

class Obstacle(arcade.Sprite):
    '''
    An obstacle is a derivitative of the object class which the player cannot move through
    but does not kill them when they touch it
    '''

    def __init__ (self, texture, column, row, speed=0, left=False):
        '''
        Constructor creates a obstacle object which "is-an" object

        param: 
            same as object parameters
        returns:
            nothing
        '''
        super().__init__(path_or_texture=texture)

        self.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0
