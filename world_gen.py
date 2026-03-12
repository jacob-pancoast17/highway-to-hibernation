import arcade
import constants as c
from hostile_object import Hostile
from noise import pnoise1
import numpy as np
from obstacle_object import Obstacle
import random

'''
The WorldGen class is the engine that generates
the world pseudo-randomly
'''
class WorldGen():
    
    def __init__(self):
        '''
        Constructor

        param: 
            self
        return: 
            nothing
        '''
        # Set a random seed for the perlin noise function
        self.seed = random.random() * 1000

        # Fill a numpy vector with 15 zeros (this represents
        # each row on the current screen and gets filled with
        # values that will represent what "type" the row is--
        # e.g. road, river, grass, etc.
        self.rows = np.zeros(c.ROW_COUNT)
        self.generate_array()

        self.loaded = []

    def generate_array(self):
        '''
        generate_array fills the array created in the constructor
        with values that indicate whether that row is a road, river,
        grass, etc.

        param: 
            self
        return: 
            nothing
        '''
        # TODO: This code currently only works if not considering the
        # fact that that the screen moves. Fix that

        # Legend for rows vector
        # -------
        # -1 : River
        #  0 : Grass
        #  1 : Road

        # Make sure the first three rows are always grass at the
        # beginning of the game
        self.rows[0] = 0
        self.rows[1] = 0
        self.rows[2] = 0

        # For each row, excluding the first three which should be
        # grass...
        for i in range(c.ROW_COUNT - 3):

            # Offset the seed a bit depending on the iteration and
            # find the value on the perlin noise wave
            x = self.seed + i * .3
            noise = pnoise1(x)

            # Depending on the noise function's value, set the
            # appropriate value based on the legend
            if (noise > -1 and
                noise < -0.1):

                # -1 : River
                self.rows[i + 3] = -1

            elif (noise > -0.1 and
                noise < 0.1):

                # 0 : Grass
                self.rows[i + 3] = 0

            elif (noise > 0.1 and
                noise < 1):

                # 1 : Road
                self.rows[i + 3] = 1
                
            else:
                print("ERROR GENERATING ARRAY IN WORLD_GEN.PY")
                exit()
    
    def generate_screen(self):

        for i in range(c.ROW_COUNT):

            self.loaded.append(self.generate_row(i))

    def generate_row(self, row):
        '''
        generate_row is a helper function that takes a row index 
        and generates that row by calling a child generate function
        based on what type of row it should be, assigned by the
        WorldGen's "rows" varaiable

        param: 
            self
            row - the current row to be generated
        return:
            a SpriteList object from child function
        '''

        # Based on the legend
        if self.rows[row] == -1:

            return self.generate_cars(row)
        
        elif self.rows[row] == 0:

            return self.generate_grassy(row)
        
        elif self.rows[row] == 1:

            return self.generate_river(row)
          
        else:

            print("PROBLEM IN GENERATION.")
            exit()
    
    def generate_cars(self, row):

        hostiles = arcade.SpriteList()

        # For each tile, just generate a hostile object that kills you
        for i in range(c.COLUMN_COUNT):

            hostiles.append(
                Hostile(c.TILE_SIZE, i, row, arcade.csscolor.RED))
        
        return hostiles

    def generate_grassy(self, row):
        '''
        generate_grassy takes a row and generates it randomly based on
        the "grassy" quality -- surrounded by trees, with randomly placed
        rocks

        param:
            self
            row - a row index to be generated
        return:
            a SpriteList object containing all of the object sprites for
                that row
        '''

        sprites = arcade.SpriteList()

        # Generate a normal curve with a mean of 0 and a st. dev. of 1.1
        # and sample it c.COLUMN_COUNT times, then sort it. This is done
        # to get a "normal" distribution of values so that ones towards the
        # edges can be set to be trees
        grass = np.random.normal(loc = 0, scale = 1.1, size = c.COLUMN_COUNT)
        grass = np.sort(grass)

        # For each cell in the row
        for i in range(c.COLUMN_COUNT):

            # Make it so values samples from the normal curve towards the edges
            # are more likely to be trees (we want a border)
            if (grass[i] < -1 or
                grass[i] > 1):

                sprites.append(
                    Obstacle(c.TILE_SIZE, i, row, arcade.csscolor.DARK_GREEN))

            # Otherwise, make it a random chance to be a rock
            else:

                if random.random() < .3:
                    sprites.append(
                        Obstacle(c.TILE_SIZE, i, row, arcade.csscolor.DARK_GRAY))
        
        return sprites

    def generate_river(self, row):
        '''
        generate_river takes a row and generates it based on
        the "river" quality -- a line of water that kills you

        param:
            self
            row - a row index to be generated
        return:
            a SpriteList object containing all of the object sprites for
                that row
        '''

        hostiles = arcade.SpriteList()

        # For each tile, just generate a hostile object that kills you
        for i in range(c.COLUMN_COUNT):

            hostiles.append(
                Hostile(c.TILE_SIZE, i, row, arcade.csscolor.BLUE))
        
        return hostiles
    
    def get_row(self, row):

        return_list = []

        for x in range(c.COLUMN_COUNT):

            there_was_a_sprite = False

            for sprite in self.loaded[row]:

                if sprite.x == x:

                    there_was_a_sprite = True
                    return_list.append(sprite)

            if not there_was_a_sprite:
                    
                return_list.append(None)

        return return_list
        