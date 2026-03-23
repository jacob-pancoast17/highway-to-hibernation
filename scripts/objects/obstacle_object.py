''' Module representing obstacle objects in the game. '''
import arcade
import constants as c

class Obstacle(arcade.Sprite):
    '''
    Constructor creates a obstacle object which "is-an" object

    param: 
        same as object parameters
    returns:
        nothing
    '''
    def __init__ (self, texture, column, row):
        super().__init__(path_or_texture=texture)

        self.center_x = (c.MARGIN + c.TILE_WIDTH) * column + c.MARGIN + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = (c.MARGIN + c.TILE_HEIGHT) * row + c.MARGIN + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0
