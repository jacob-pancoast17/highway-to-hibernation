''' Module representing the player and movement'''
import arcade
import constants as c
from objects.hostile_object import Hostile
from objects.obstacle_object import Obstacle
import time

class Player(arcade.Sprite):
    '''Player class: holds all information about the player, including position and sprite'''
    def __init__(self, row, column):
        # For now just makes cubes
        # Right now this also ignores the angle parameter
        super().__init__(path_or_texture="sprites/bear_2.png",
            scale = 1.25)
        
        self.center_x = (c.MARGIN + c.TILE_WIDTH) * column + c.MARGIN + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = (c.MARGIN + c.TILE_HEIGHT) * row + c.MARGIN + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 180.0
    
    def try_move(self, key, world, window):
        
        # Try to move
        self.move(key)

        # Do not let the user move outside the window
        if (self.center_y >= c.WINDOW_HEIGHT or
            self.center_y <= 0 or 
            self.center_x <= 0 or
            self.center_x >= c.WINDOW_WIDTH):
            
            self.move_back(key)
            return False

        # Obtain information about the next row
        next_cell = world.get_row(self.y)[self.x]
        next_platform = world.get_platform(self.y)[self.x]


        # If the next cell is a platform, we can move
        if next_platform is not None:

            return True
        
        # Otherwise, figure out what we are colliding with
        if (next_cell is not None and
            arcade.check_for_collision(self, next_cell)):

            # Define the type of hit
            self.hit(next_cell, window)

            # If this line is reached, the hit type was obstacle
            self.move_back(key)

            # return False
            return False
        # return True
        return True
                    
    def hit(self, next_cell, window):
        
        if isinstance(next_cell, Obstacle):

            return
        
        elif isinstance(next_cell, Hostile):

            from screens.game_over_screen import GameOver
            window.show_view(GameOver())
        
    def move(self, key):

        if (key == arcade.key.UP):
            #print("UP")
            self.center_y += c.VELOCITY_MULTIPLIER
            self.y += 1
            self.angle = 180

        elif (key == arcade.key.DOWN):
            #print("DOWN")
            self.center_y -= c.VELOCITY_MULTIPLIER
            self.y -= 1
            self.angle = 0

        elif (key == arcade.key.LEFT):
            #print("LEFT")
            self.center_x -= c.VELOCITY_MULTIPLIER
            self.x -= 1
            self.angle = 90

        elif (key == arcade.key.RIGHT):
            #print("RIGHT")
            self.center_x += c.VELOCITY_MULTIPLIER
            self.x += 1
            self.angle = -90
    
    def move_back(self, key):

        # If up, move back down
        if (key == arcade.key.UP):

            self.center_y -= c.VELOCITY_MULTIPLIER
            self.y -= 1
            self.angle = 180
            
        # If down, move back up
        elif (key == arcade.key.DOWN):            

            self.center_y += c.VELOCITY_MULTIPLIER
            self.y += 1
            self.angle = 0

        # If left, move back right
        elif (key == arcade.key.LEFT):
            
            self.center_x += c.VELOCITY_MULTIPLIER
            self.x += 1
            self.angle = 90
            
        # If right, move back left
        elif (key == arcade.key.RIGHT):

            self.center_x -= c.VELOCITY_MULTIPLIER
            self.x -= 1
            self.angle = -90