import arcade
import constants as c
from game_over_screen import GameOver
import random
import time

class Hostile(arcade.SpriteSolidColor):
    '''
    Constructor creates a hostile object which "is-an" object

    param: 
        same as object parameters
        window - a pyarcade window object, allows alterable screen
        player - player object
        static - a boolean if the object moves or not
    returns:
        nothing
    '''
    def __init__ (self, size, color, row, column=0, static=True, left=None):
        super().__init__(width = size,
            height = size,
            color = color)
        
        self.center_x = (c.MARGIN + c.TILE_WIDTH) * column + c.MARGIN + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = (c.MARGIN + c.TILE_HEIGHT) * row + c.MARGIN + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0

        self.static = static
        self.is_moving_left = left

        # If this hostile item is a dynamic one...
        if self.static == False:
            # Start global timer
            self.timer = 0

            # Choose a velocity depending on it's direction
            if self.is_moving_left == False:
                self.speed = random.uniform(0.1, 1.0)
                
            if self.is_moving_left == True:
                self.speed = random.uniform(-0.1, -1.0)

                self.center_x = (c.MARGIN + c.TILE_WIDTH) * 14 + c.MARGIN + c.TILE_WIDTH // 2
                self.x = 14
        
            # Set the first time to move based on the speed
            self.next_move = self.speed

    def try_move(self, delta_time, window, player):

        if self.static:

            return

        self.timer += delta_time

        if self.timer >= self.next_move:

            self.next_move += self.speed

            # if (self.center_x >= c.WINDOW_WIDTH - c.TILE_WIDTH or
            #     self.center_x <= c.TILE_WIDTH):
                
            #     print("BYE")

            self.move(self.is_moving_left)
            hit_list = arcade.check_for_collision(self,
                                                  player)
            if hit_list:

                from game_over_screen import GameOver
                window.show_view(GameOver())
            
            # if self.center_y < 0:
            #     temp = self.center_y
            #     self.center_y = c.WINDOW_HEIGHT - (c.TILE_HEIGHT / 2) - 5
            #     hit_list = arcade.check_for_collision(
            #         self, 
            #         player)
            #     if hit_list:
            #         window.show_view(GameOver())
            #         return False
            #     self.center_y = temp
            # else:
            #     self.center_y -= c.VELOCITY_MULTIPLIER
            #     hit_list = arcade.check_for_collision(
            #         self, 
            #         player)
            #     if hit_list:
            #         window.show_view(GameOver())
            #         return False
            #     self.center_y += c.VELOCITY_MULTIPLIER
            # return True


    def move(self, is_moving_left):

        if is_moving_left:
            self.center_x += c.VELOCITY_MULTIPLIER
            self.x += 1
        else:
            self.center_x -= c.VELOCITY_MULTIPLIER
            self.x -= 1

