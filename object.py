''' Module representing objects (cubes) in the game. '''
import arcade
import constants as c

class Object():
    '''
    Constructor

    param:
        size, the box's length and width
        x, x position on the window
        y, y position on the window
        color, arcade.csscolor color type
        angle, the angle of the box
    returns:
        nothing
    '''
    def __init__(self, size, row, column, color):
        # For now just makes cubes
        # Right now this also ignores the angle parameter
        self.obj = arcade.SpriteSolidColor(
            width = size,
            height = size,
            center_x = (c.MARGIN + c.TILE_WIDTH) * row + c.MARGIN + c.TILE_WIDTH // 2,
            center_y = (c.MARGIN + c.TILE_HEIGHT) * column + c.MARGIN + c.TILE_HEIGHT // 2,
            color = color,
            angle = 0
        )

        self.curr_x = row
        self.curr_y = column

    '''
    to_sprite returns the object as a sprite to be drawn

    param:
        nothing
    returns:
        sprite version of the object
    '''
    def to_sprite(self):
        return self.obj
