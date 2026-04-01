''' Module representing obstacle objects in the game. '''
import arcade
from scripts import constants as c

class Obstacle(arcade.Sprite):
    '''
    Constructor creates a obstacle object which "is-an" object

    param: 
        same as object parameters
    returns:
        nothing
    '''
    def __init__ (self, texture, column, row, speed = 0):
        super().__init__(path_or_texture=texture)
        
        self.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0
        self.speed = speed
