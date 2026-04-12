''' Module representing platform objects in the game.'''
import arcade
from scripts import constants as c

class Platform(arcade.Sprite):
    '''
    A platform object is a derivative of the object clase which creates objects which
    the player can stand on to avoid touching anything hostile.
    '''

    def __init__ (self, texture, column, row, speed=0, static=True, left=None):
        '''
        Constructor creates a platform object which "is-an" object

        param: 
            same as object parameters
            window - a pyarcade window object, allows alterable screen
            player - player object
            static - a boolean if the object moves or not
        returns:
            nothing
        '''
        super().__init__(path_or_texture=texture)

        self.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0

        self.static = static
        self.speed = speed

        self.death_sound = None

        # If this platform item is a dynamic one...
        if self.static is False:
            # Start global timer
            self.timer = 0
            self.is_moving_left = left

            # Set the first time to move based on the speed
            self.next_move = self.speed

    def try_move(self, delta_time, player):
        '''
        try_move takes the elapsed time and tests if we can move
        the hostile object. If we can, move it

        param:
            self
            delta_time
            player
        returns:
            nothing
        '''
        #TODO: Delete object after moving off screen

        # Don't move static objects
        if self.static:

            return

        self.timer += delta_time

        # If the current timer exceeds the time to next move, then move

        if self.timer >= self.next_move:

            # Set the next move
            self.next_move += self.speed

            # Check if the player collides with platform object
            hit_list = arcade.check_for_collision(self,
                                                  player)
            # If moving right, increase x
            if not self.is_moving_left:
                self.center_x += c.VELOCITY_MULTIPLIER
                self.x += 1
                # if the player is colliding with log, and they aren't offscreen
                if hit_list:
                    player.center_x += c.VELOCITY_MULTIPLIER
                    player.x += 1
                    if player.x > c.COLUMN_COUNT - 1:
                        player.dead = True
                        player.death = 'Off Screen'
                        self.death_sound = arcade.play_sound(c.DEATH_SFX)
            # Otherwise, decrease x
            else:
                self.center_x -= c.VELOCITY_MULTIPLIER
                self.x -= 1
                if hit_list and player.x >= 0:
                    player.center_x -= c.VELOCITY_MULTIPLIER
                    player.x -= 1
                    if player.x < 0:
                        player.dead = True
                        player.death = 'Off Screen'
                        self.death_sound = arcade.play_sound(c.DEATH_SFX)

    def is_off_screen(self):
        '''
        Checks if the platform is off screen

        param:
            self
        returns:
            nothing
        '''

        if (self.center_x < c.TILE_WIDTH or
            self.center_x > c.WINDOW_WIDTH):
            self.speed = 0
            return True
        else:
            return False
