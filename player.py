import arcade
import constants as c
from hostile_object import Hostile
from obstacle_object import Obstacle

class Player(arcade.SpriteSolidColor):
    def __init__(self, size, row, column, color):
        # For now just makes cubes
        # Right now this also ignores the angle parameter
        super().__init__(width = size,
            height = size,
            color = color)
        
        self.center_x = (c.MARGIN + c.TILE_WIDTH) * column + c.MARGIN + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = (c.MARGIN + c.TILE_HEIGHT) * row + c.MARGIN + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0
    
    def try_move(self, key, world, window):
        
        if key == arcade.key.UP:
            
            # Do not let the user move above the window
            if self.center_y >= c.WINDOW_HEIGHT - c.TILE_HEIGHT:
                return
            
            self.move(arcade.key.UP)
            next_row = world.get_row(self.y)
            next_cell = next_row[self.x]
            if next_cell is not None:
                hit_list = arcade.check_for_collision(self,
                                                  next_row[self.x])
                if hit_list: 
                    if self.hit(next_cell, window) == True:
                        self.move(arcade.key.DOWN)
                    
        
        elif key == arcade.key.DOWN:

            if self.center_y <= c.TILE_HEIGHT:
                return
            
            self.move(arcade.key.DOWN)
            next_row = world.get_row(self.y)
            next_cell = next_row[self.x]
            if next_cell is not None:
                hit_list = arcade.check_for_collision(self,
                                                  next_row[self.x])
                if hit_list: 
                    if self.hit(next_cell, window) == True:
                        self.move(arcade.key.UP)
        
        elif key == arcade.key.LEFT:
            if self.center_x <= c.TILE_HEIGHT:
                return False
            
            self.move(arcade.key.LEFT)
            row = world.get_row(self.y)
            next_cell = row[self.x]
            if next_cell is not None:
                hit_list = arcade.check_for_collision(self,
                                                  row[self.x])
                if hit_list: 
                    if self.hit(next_cell, window) == True:
                        self.move(arcade.key.RIGHT)
                
            return True
        
        elif key == arcade.key.RIGHT:
            if self.center_x >= c.WINDOW_WIDTH - c.TILE_HEIGHT:
                return False
            
            self.move(arcade.key.RIGHT)
            row = world.get_row(self.y)
            next_cell = row[self.x]
            if next_cell is not None:
                hit_list = arcade.check_for_collision(self,
                                                  row[self.x])
                if hit_list: 
                    if self.hit(next_cell, window) == True:
                        self.move(arcade.key.LEFT)
        
    def hit(self, next_cell, window):
        
        if isinstance(next_cell, Obstacle):

            return True
        
        elif isinstance(next_cell, Hostile):

            from game_over_screen import GameOver
            window.show_view(GameOver())

    
    def move(self, key):

        if (key == arcade.key.UP and
            self.center_y < c.WINDOW_HEIGHT - c.TILE_HEIGHT):
            #print("UP")
            self.center_y += c.VELOCITY_MULTIPLIER
            self.y += 1

        elif (key == arcade.key.DOWN and
              self.center_y > c.TILE_HEIGHT):
            #print("DOWN")
            self.center_y -= c.VELOCITY_MULTIPLIER
            self.y -= 1

        elif (key == arcade.key.LEFT and
              self.center_x > c.TILE_HEIGHT):
            #print("LEFT")
            print(self.center_x)
            self.center_x -= c.VELOCITY_MULTIPLIER
            self.x -= 1

        elif (key == arcade.key.RIGHT and
              self.center_x < c.WINDOW_WIDTH - c.TILE_HEIGHT):
            #print("RIGHT")
            self.center_x += c.VELOCITY_MULTIPLIER
            self.x += 1

        print(f"[{self.x}, {self.y}]")