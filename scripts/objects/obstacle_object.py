''' Module representing obstacle objects in the game.'''
import arcade
from scripts import constants as c

class Obstacle(arcade.Sprite):
    '''
    An obstacle is a derivitative of the object class which the player cannot move through
    but does not kill them when they touch it
    '''

    def __init__ (self, texture, column, row, not_tree):
        '''
        Constructor creates a obstacle object which "is-an" object

        param: 
            same as object parameters
        returns:
            nothing
        '''
        super().__init__(path_or_texture=texture)

        self.center_x = c.TILE_SIZE * column + c.TILE_SIZE // 2
        self.x = column
        self.center_y = c.TILE_SIZE * row + c.TILE_SIZE // 2
        self.y = row
        self.angle = 0

        self.update_resolution(self.x, self.y, not_tree)
    
    def update_resolution(self, curr_x_on_screen, curr_y_on_screen, not_tree):
        '''
        Updates the current resolution
        
        param:
            self
            curr_x_on_screen
            curr_y_on_screen
        return:
            nothing
        '''

        if not_tree:
            # Update resolution
            self.scale = c.RESOLUTION_RATIO

            # Update the current position
            self.center_x = c.TILE_SIZE * curr_x_on_screen + c.TILE_SIZE // 2
            self.center_y = c.TILE_SIZE * curr_y_on_screen + c.TILE_SIZE // 2

        else:
            # Update resolution
            self.scale = c.RESOLUTION_RATIO

            # Update the current position
            self.center_x = c.TILE_SIZE * curr_x_on_screen + c.TILE_SIZE // 2
            self.center_y = c.TILE_SIZE * curr_y_on_screen + c.TILE_SIZE


