''' Hostile object class, which is an object that can kill the player on contact.'''
import arcade
from scripts import constants as c

class Hostile(arcade.Sprite):
    '''
    A hostile object is a deriviative of the object class that can "kill"
    the player if they touch it
    '''

    def __init__ (self, texture, column, row, speed=0, static=True, left=None):
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
        super().__init__(path_or_texture=texture)

        self.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 0

        self.static = static
        self.speed = speed

        # Set movement values for moving hostiles
        if not self.static:
            self.timer = 0
            self.is_moving_left = True
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

            # If moving right, increase x
            if not self.is_moving_left:
                self.center_x += c.VELOCITY_MULTIPLIER
                self.x += 1
            # Otherwise, decrease x
            else:
                self.center_x -= c.VELOCITY_MULTIPLIER
                self.x -= 1

            hit_list = arcade.check_for_collision(self, player)
            if hit_list:
                self.move_back()
                player.dead = True
                player.death = 'Mauled'
                self.death_sound = arcade.play_sound(c.DEATH_SFX)

    def move_back(self):
        '''
        move_back takes a key and moves the hostile back
        '''

        if self.is_moving_left is True:

            self.x += 1
            self.center_x += c.VELOCITY_MULTIPLIER

        else:

            self.x -= 1
            self.center_x -= c.VELOCITY_MULTIPLIER

    def is_off_screen(self):
        '''
        is_off_screen checks if the hostile object has moved off the screen, and
        should be deleted
        '''

        if (self.center_x < c.TILE_WIDTH or
            self.center_x > c.WINDOW_WIDTH):
            self.speed = 0
            return True
        else:
            return False
