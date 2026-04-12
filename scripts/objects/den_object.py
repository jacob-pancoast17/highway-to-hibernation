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

        self.center_x = c.TILE_SIZE * column + c.TILE_SIZE // 2
        self.x = column
        self.center_y = c.TILE_SIZE * row + c.TILE_SIZE // 2
        self.y = row
        self.angle = 0

        self.update_resolution(self.x, self.y)

    def update_resolution(self, x_on_screen, y_on_screen):
        '''
        initialize updates all of a den object's sizes based on the current
        resolution

        param:
            self
        returns:
            nothing
        '''
        # Update the current resolution
        self.scale = c.RESOLUTION_RATIO

        # Update the current position
        self.center_x = c.TILE_SIZE * x_on_screen + c.TILE_SIZE // 2
        self.center_y = c.TILE_SIZE * y_on_screen + c.TILE_SIZE // 2
