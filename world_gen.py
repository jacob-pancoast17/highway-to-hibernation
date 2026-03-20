'''This module represents world generation'''
import arcade
import constants as c
from hostile_object import Hostile
from noise import pnoise1
import numpy as np
from obstacle_object import Obstacle
import random

class WorldGen():
    '''
    The WorldGen class is the engine that generates
    the world pseudo-randomly
    '''
    
    def __init__(self, window, player):
        '''
        Constructor
        Sets a random seed for the perlin noise function and
        calls the helper generate_array function

        param: 
            self
        return: 
            nothing
        '''
        # Set a random seed for the perlin noise function
        self.seed = random.random() * 1000
        #self.seed = 0.1 * 1000

        # Fill a numpy vector with 15 zeros (this represents
        # each row on the current screen and gets filled with
        # values that will represent what "type" the row is--
        # e.g. road, river, grass, etc.
        self.rows = np.zeros(c.ROW_COUNT)
        self.generate_array()

        self.loaded = []

        self.window = window
        self.player = player

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

        # For each row... (excluding the first three which 
        # should be grass
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
        '''
        generate_screen generates a row for every row that should
        appear on screen

        param:
            self
        return
            nothing
        '''

        #TODO: Right now only works not considering a moving screen

        for i in range(c.ROW_COUNT):

            row = self.generate_row(i)
            print(row)
            self.loaded.append(row)

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
        '''
        generate_cars takes a row and generates it randomly based on
        the "cars" quality -- moving objects across the screen

        param:
            self
            row - a row index to be generated
        return:
            a SpriteList object containing all of the object sprites for
                that row
        '''

        hostiles = arcade.SpriteList()

        # For each tile, just generate a hostile object that kills you

        moving_left = random.choice([True, False])
        # Pick a random speed
        self.speed = random.uniform(c.LOWER_OBSTACLE_SPEED, c.UPPER_OBSTACLE_SPEED)

        if not moving_left:
            hostiles.append(
                Hostile("sprites/rock1.png", 0, row, self.speed, static=False, left=moving_left))
        else:
            hostiles.append(
                Hostile("sprites/rock1.png", 14, row, self.speed, static=False, left=moving_left))

        return hostiles
    
    def update_cars(self, row):

        hostiles = arcade.SpriteList()

        # For each car in the row
        for car in self.loaded[row]:

            # If it's still on screen, keep it
            if not car.is_off_screen():
                hostiles.append(car)

        index = 0
        while len(hostiles) == 0:
            
            car = self.loaded[row][index]
            if car.is_off_screen():
                hostiles.append(car)
            else:
                index += 1

        #print(f"row {row}: how many cars? {len(hostiles)}")
            
        # After cleaning up the current cacrs we have in a row, 
        # let's check if we should add a new one! 
        spawn = random.choices([True, False], weights=[20, 80])
        if not spawn[0]:
            return
        
        # First we need to determine  when the last in line 
        # arrives (we don't want cars lapping each other)
        last_arrival = hostiles[-1]

        # Arrival time if going right
        if last_arrival.left == False:
            last_arrival_time = (c.COLUMN_COUNT - last_arrival.x) * last_arrival.speed
        # vs left
        else:
            last_arrival_time = last_arrival.x * last_arrival.speed

        # Now that we know when the next one arrives, let's
        # pick a speed that won't cause this new car to lap
        # the last arriving of the previous cars
        next_avail_arrival_time = last_arrival_time + last_arrival.speed
        # Max speed that would place the car arriving at the next availablee
        min_speed = next_avail_arrival_time / c.COLUMN_COUNT

        # Truncate that so we don't get any speed demons
        if min_speed < 0.2:
            min_speed = 1.0

        new_speed = random.uniform(min_speed, c.UPPER_OBSTACLE_SPEED)
        arrival = 15 * new_speed
        #print(f"last arrival time in {last_arrival_time}, currently at x = {last_arrival.x}")
        #print(f"next available arrival is {next_avail_arrival_time} due to speed of {last_arrival.speed}")
        #print(f"adding a new car on row {row} with speed {new_speed} which will arrive in {arrival}")

        if last_arrival.is_moving_left:
            hostiles.append(
                Hostile("sprites/rock1.png", 14, row, speed = new_speed, static=False, left=True))
        else:
            hostiles.append(
                Hostile("sprites/rock1.png", 0, row, speed = new_speed, static=False, left=False))

        # Replace currently loaded row with the updated one
        self.loaded[row] = hostiles


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

        # TODO: HONEY
        #honey = random.choices([True, False], weights=[20, 80])

        last_rock = None
        # For each cell in the row
        for i in range(c.COLUMN_COUNT):

            # We should not spawn in a rock
            if row == c.STARTING_Y and i == c.STARTING_X:
                pass
            
            # Make it so values samples from the normal curve towards the edges
            # are more likely to be trees (we want a border)
            elif (grass[i] < -1 or
                grass[i] > 1):

                sprites.append(
                    Obstacle('sprites/log_mushrooms.png', i, row))

            # Otherwise, make it a random chance to be a rock
            else:
                chance = random.random()
                if chance < .3:

                    if last_rock == None or last_rock.x != i-1:
                        last_rock = Obstacle('sprites/rock2.png', i, row)
                        sprites.append(last_rock)

                #elif chance < .4 and honey:
                #    last_rock = Obstacle(c.TILE_SIZE, i, row, arcade.csscolor.GOLD)
                    
    
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

        river = arcade.SpriteList()

        # Generate the whole river as hostile objects
        for i in range(c.COLUMN_COUNT):

            river.append(
                Hostile("sprites/water.png", i, row))
            
        # Call appropriate helper function to define specific types
        #type = random.choices(['Lilypads', 'Logs'])
        if type[0] == 'Lilypads':
            #river = self.generate_lilypads(river)
            pass
        else:
            pass
            #generate_logs(river)
        
        return river
    
    def generate_lilypads(self, river):
        print("generating lilypads!")
        for water_tile in river:
            if random.random() < .2:
                water_tile = arcade.SpriteSolidColor(c.TILE_WIDTH,
                                                     c.TILE_HEIGHT,
                                                     color=arcade.color.GREEN_YELLOW,
                                                     center_x=water_tile.center_x,
                                                     center_y=water_tile.center_y)
    
    def get_row(self, row):
        '''
        get_row takes a row and returns a list version of all the sprites
        in that row (NOT a SpriteList) as a pyarcade SpriteList can only
        contain sprites, but we need spaces that contain 'None'-- a blank
        tile

        param:
            self
            row - a row index to convert from a SpriteList to a list 
        return:
            the row as a list of sprite objects and Nones
        '''

        return_list = []

        # For every x position in the row
        for x in range(c.COLUMN_COUNT):

            there_was_a_sprite = False

            for sprite in self.loaded[row]:
                
                # For each sprite in the current row, check
                # if it's x coord matches the current x
                if sprite.x == x:

                    # if it does, append the sprite
                    there_was_a_sprite = True
                    return_list.append(sprite)

            # If not, append a "None"
            if not there_was_a_sprite:
                    
                return_list.append(None)

        # This creates a list of the form
        # [Obstacle, None, None, None, Obstacle] for example
        return return_list
        
    def get_hostile_rows(self):
        '''
        get_hostile_rows returns all the hostile row indices

        param:
            self
        return:
            A list of all hostiles row indices
        '''

        hostiles = []

        for i in range(len(self.loaded)):

            if self.rows[i] == 1 or self.rows[i] == -1:

                hostiles.append(i)
        
        return hostiles
