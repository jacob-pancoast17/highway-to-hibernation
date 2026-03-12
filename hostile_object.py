import arcade
import constants as c
from game_over_screen import GameOver
from object import Object
import time

class Hostile(arcade.SpriteSolidColor):
    '''
    Constructor creates a hostile object which "is-an" object

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

    def try_move(self, window, player):
        if self.center_y < 0:
            temp = self.center_y
            self.center_y = c.WINDOW_HEIGHT - (c.TILE_HEIGHT / 2) - 5
            hit_list = arcade.check_for_collision(
                self, 
                player)
            if hit_list:
                window.show_view(GameOver())
                return False
            self.center_y = temp
        else:
            self.center_y -= c.VELOCITY_MULTIPLIER
            hit_list = arcade.check_for_collision(
                self, 
                player)
            if hit_list:
                window.show_view(GameOver())
                return False
            self.center_y += c.VELOCITY_MULTIPLIER
        return True


    def move(self):
        if self.center_y < 0:
            self.center_y = c.WINDOW_HEIGHT - (c.TILE_HEIGHT / 2) - 5
        else:
            self.center_y -= c.VELOCITY_MULTIPLIER
