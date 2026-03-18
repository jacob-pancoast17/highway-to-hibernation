''' Module representing obstacle objects in the game. '''
import arcade
import constants as c

class Obstacle(arcade.SpriteSolidColor):
    '''
    Constructor creates a obstacle object which "is-an" object

    param: 
        same as object parameters
    returns:
        nothing
    '''
    def __init__ (self, size, column, row, color):
        super().__init__(width = size,
            height = size,
            color = color)
        
        self.center_x = (c.MARGIN + c.TILE_WIDTH) * column + c.MARGIN + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = (c.MARGIN + c.TILE_HEIGHT) * row + c.MARGIN + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0
    