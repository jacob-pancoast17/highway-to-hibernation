import arcade
import constants as c

class Hostile(arcade.Sprite):
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
    def __init__ (self, texture, column, row, speed=0, static=True, left=None):
        super().__init__(path_or_texture=texture)
        
        self.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0

        self.static = static
        self.speed = speed

        # If this hostile item is a dynamic one...
        if self.static == False:
            # Start global timer
            self.timer = 0
            self.is_moving_left = left
        
            # Set the first time to move based on the speed
            self.next_move = self.speed

    def try_move(self, delta_time, window, player):
        #TODO: Delete object after moving off screen

        # Don't move static objects
        if self.static:

            return

        self.timer += delta_time

        # If the current timer exceeds the time to next move, then move
        if self.timer >= self.next_move:

            # Set the next move
            self.next_move += self.speed

            # If moving right, increase x
            if not self.is_moving_left:
                self.center_x += c.VELOCITY_MULTIPLIER
                self.x += 1
            # Otherwise, decrease x
            else:
                self.center_x -= c.VELOCITY_MULTIPLIER
                self.x -= 1

            hit_list = arcade.check_for_collision(self,
                                                  player)
            if hit_list:

                from screens.game_over_screen import GameOver
                window.show_view(GameOver())

    def is_off_screen(self):
        
        if (self.center_x < c.TILE_WIDTH or
            self.center_x > c.WINDOW_WIDTH):
            self.speed = 0
            return True
        else:
            return False