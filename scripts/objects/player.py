''' Module representing the player and movement'''
import arcade
from scripts import constants as c
from scripts.objects.den_object import Den
from scripts.objects.hostile_object import Hostile
from scripts.objects.obstacle_object import Obstacle
from scripts.screens.victory_screen import Victory

class Player(arcade.Sprite):
    '''
    Player class: holds all information about the player, including position and sprite
    '''

    def __init__(self, row, column, tex_eng):
        '''
        Constructor creates a player

        param: 
            self
            row
            column
            texture engine to access sprites
        returns:
            nothing
        '''

        # Access the bear sprite
        super().__init__(path_or_texture=tex_eng.bear)

        # Access the death textures
        self.drowning_textures = tex_eng.drowning
        self.mauled_texture = tex_eng.mauled

        # Define all coordinates
        self.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
        self.x = column
        self.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2
        self.y = row
        self.angle = 180.0
        self.cur_texture_index = 0

        # Define some starting properties of the player
        self.death_timer = 0
        self.death_sound = None
        self.death = None
        self.next_death_anim = c.DEATH_ANIMATION_UPDATE_INTERVAL
        self.dead = False
        self.score = 0
        self.achieve_victory = None

    def try_move(self, key, world, window):
        '''
        try_move takes a key, the world, and the window, and tries to move the player
        in the direction of the key. If the player can move, move them. If they can't,
        do not move them. If they hit a hostile object, move to the game over screen.

        param:
            self
            key - keyboard key
            world
            window
        returns:
            boolean - if they move or not
        '''

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
            river_collided = self.hit(next_cell, window)

            # If this line is reached, the hit type was obstacle
            if not river_collided:
                self.move_back(key)

            return False

        return True

    def hit(self, next_cell, window):
        '''
        hit takes the next cell and the window, and determines what type of cell it is.
        If it's an obstacle, do not move. If it's a hostile object, move to the game over screen

        param:
            self
            next_cell - cell you are trying to move into
            window - current view
        returns:
            boolean - check is player touched something that can kill them
        '''

        if isinstance(next_cell, Obstacle):

            return False

        elif isinstance(next_cell, Hostile):

            self.dead = True

            self.death_sound = arcade.play_sound(c.DEATH_SFX)

            if next_cell.static is True:

                self.death = 'Drown'
                return True

            else:

                self.death = 'Mauled'
                return False

        elif isinstance(next_cell, Den):

            window.show_view(Victory(self.score, window.current_view))
            self.achieve_victory = arcade.play_sound(c.VICTORY_JINGLE)
            return False

    def move(self, key):
        '''
        move takes a key and moves the player in the direction of the key, 
        without checking if the move is valid

        param:
            self
            key - keyboard key
        returns:
            nothing
        '''

        if key == arcade.key.UP:
            #print("UP")
            self.center_y += c.VELOCITY_MULTIPLIER
            self.y += 1
            self.angle = 180

        elif key == arcade.key.DOWN:
            #print("DOWN")
            self.center_y -= c.VELOCITY_MULTIPLIER
            self.y -= 1
            self.angle = 0

        elif key == arcade.key.LEFT:
            #print("LEFT")
            self.center_x -= c.VELOCITY_MULTIPLIER
            self.x -= 1
            self.angle = 90

        elif key == arcade.key.RIGHT:
            #print("RIGHT")
            self.center_x += c.VELOCITY_MULTIPLIER
            self.x += 1
            self.angle = -90

    def move_back(self, key):
        '''
        move_back takes a key and moves the player back in the opposite direction of the key,
        without checking if the move is valid. This is used when the player tries to move into
        an invalid space, and we want to move them back to where they were.

        param:
            self
            key - keyboard key used
        returns:
            nothing
        '''

        # If up, move back down
        if key == arcade.key.UP:

            self.center_y -= c.VELOCITY_MULTIPLIER
            self.y -= 1
            self.angle = 180

        # If down, move back up
        elif key == arcade.key.DOWN:

            self.center_y += c.VELOCITY_MULTIPLIER
            self.y += 1
            self.angle = 0

        # If left, move back right
        elif key == arcade.key.LEFT:

            self.center_x += c.VELOCITY_MULTIPLIER
            self.x += 1
            self.angle = 90

        # If right, move back left
        elif key == arcade.key.RIGHT:

            self.center_x -= c.VELOCITY_MULTIPLIER
            self.x -= 1
            self.angle = -90

    def die(self, delta_time):
        '''
        die is a helper function which is used when a player dies to determine which death
        animation is used based on how they die.

        param:
            self
            delta_time
        returns:
            nothing
        '''

        self.death_timer += delta_time

        if self.death == 'Drown':

            if self.death_timer > self.next_death_anim:

                self.next_death_anim += c.DEATH_ANIMATION_UPDATE_INTERVAL

                self.texture = self.drowning_textures[self.cur_texture_index]

                self.cur_texture_index += 1

                if self.cur_texture_index > 8:

                    self.cur_texture_index = 0

        elif self.death == 'Mauled':

            self.texture = self.mauled_texture
