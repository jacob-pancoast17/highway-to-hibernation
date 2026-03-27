'''This module represents world generation'''
import arcade
from scripts import constants as c
from objects.den_object import Den
from objects.hostile_object import Hostile
from noise import pnoise1
import numpy as np
from objects.obstacle_object import Obstacle
import random
from objects.platform_object import Platform

class WorldEngine():
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

        self.rows = []
        self.generate_array()

        self.loaded_indices = []
        self.loaded = []
        self.platforms = []
        self.collectibles = []

        self.window = window
        self.player = player

        # SpriteList for honey the player can collect
        self.hunny_list = arcade.SpriteList()

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

        # Make sure the first rows are always grass at the
        # beginning of the game
        for i in range(c.NUM_START_GRASSY_ROWS):
            self.rows.append('Grassy')

        # For each row... (excluding the first three which
        # should be grass
        for i in range(c.LEVEL_SIZE - c.NUM_START_GRASSY_ROWS - c.NUM_ENDING_GRASSY_ROWS):

            # Offset the seed a bit depending on the iteration and
            # find the value on the perlin noise wave
            x = self.seed + i * .3
            noise = pnoise1(x)

            # Depending on the noise function's value, set the
            # appropriate value based on the legend
            if (noise > -1 and
                noise < -0.5):

                # River with lilypads
                self.rows.append("River_Lilypads")

            elif(noise> -0.5 and 
                 noise < -0.1):
                
                # River with logs
                self.rows.append("River_Logs")
            elif (noise > -0.1 and
                noise < 0.1):

                # Grassy
                self.rows.append("Grassy")

            elif (noise > 0.1 and
                noise < 1):

                # Road
                self.rows.append("Road")
                
            else:
                print("ERROR GENERATING ARRAY IN WORLD_GEN.PY")
                exit()

        # Make sure the first last rows are always grass at the
        # beginning of the game
        for i in range(c.NUM_ENDING_GRASSY_ROWS):
  
            self.rows.append('Victory')
    
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
            self.loaded_indices.append(i)

            bottom_row = self.generate_row(i)
            self.loaded.append(bottom_row)

            middle_row = self.generate_platforms(i)
            self.platforms.append(middle_row)

            top_row = self.generate_collectible(i)
            self.collectibles.append(top_row)
    
    def update_screen(self, new_row_index):
        # Delete the first row
        self.loaded.pop(0)
        self.platforms.pop(0)
        self.collectibles.pop(0)
        self.loaded_indices.pop(0)

        # Generate a new row 
        new_row = self.generate_row(new_row_index)
        new_platform  = self.generate_platforms(new_row_index)
        new_collectible = self.generate_collectible(new_row_index)
        self.loaded_indices.append(new_row_index)

        # Move everything else down (iterate over rows - 1 because 
        # we have 1 less row)
        for i in range(c.ROW_COUNT - 1):
            self.loaded[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
            self.platforms[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
            self.collectibles[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
        self.player.center_y -= c.VELOCITY_MULTIPLIER
        self.player.angle = 180

        # Add the new row
        self.loaded.append(new_row)
        self.platforms.append(new_platform)
        self.collectibles.append(new_collectible)

        print(f"added that to row {new_row_index}")
        print(f"loaded is currently {self.loaded_indices}")
        print(f"the index in self.loaded should be {new_row_index - self.loaded_indices[0]}")

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
        if self.rows[row] == "Road":

            return self.generate_cars(row)
        
        elif self.rows[row] == "Grassy":

            return self.generate_grassy(row)
        
        elif (self.rows[row] == "River_Lilypads" or
              self.rows[row] =="River_Logs"):
            
            return self.generate_river(row)
        
        elif self.rows[row] == "Victory":

            return self.generate_victory(row)

        
        else:

            print("PROBLEM IN GENERATION.")
            exit()

    def generate_platforms(self, row):
        '''
        generates platforms
        '''

        # Use self.row[row] to figure out if the row generated was with lilypads or logs

        if self.rows[row] == 'River_Lilypads':

            return self.generate_lilypads(row)
        elif self.rows[row] == 'River_Logs':
            logs = self.generate_logs(row)

            return logs   
        
        else:

            return arcade.SpriteList()
        
    def generate_collectible(self, row):
        '''
        generate_collectible is a helper function that takes a row index 
        and generates the collectibles in that row by calling a child generate function
        based on what type of collectible it should be

        param: 
            self
            row - the current row to be generated
        return:
            a SpriteList object from child function
        '''
        if self.rows[row] == 0:

            return self.generate_honey(row)

        else: 

            return arcade.SpriteList()

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
                Hostile("sprites/rock1.png", 0, row - self.loaded_indices[0], self.speed, static=False, left=moving_left))
        else:
            hostiles.append(
                Hostile("sprites/rock1.png", 14, row - self.loaded_indices[0], self.speed, static=False, left=moving_left))

        return hostiles

    def update_cars(self, row):
        '''
        update_cars takes a row and updates the cars in that row by trying
        to move them and then trying to spawn new ones if we are at the next
        spawn check
        '''

        hostiles = arcade.SpriteList()

        # For each car in the row
        for car in self.loaded[row - self.loaded_indices[0]]:

            # If it's still on screen, keep it
            if not car.is_off_screen():
                hostiles.append(car)

        index = 0
        while len(hostiles) == 0:
            
            car = self.loaded[row - self.loaded_indices[0]][index]
            if car.is_off_screen():
                hostiles.append(car)
            else:
                index += 1


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
        # Max speed that would place the car arriving at the next available
        min_speed = next_avail_arrival_time / c.COLUMN_COUNT

        # Truncate that so we don't get any turtles
        if min_speed < c.LOWER_OBSTACLE_SPEED:
            min_speed = c.LOWER_OBSTACLE_SPEED

        new_speed = random.uniform(min_speed, c.UPPER_OBSTACLE_SPEED)

        # Truncate THAT so we don't get any speed demons
        if new_speed > c.UPPER_OBSTACLE_SPEED:
            new_speed = c.UPPER_OBSTACLE_SPEED

        arrival = 15 * new_speed
        #print(f"last arrival time in {last_arrival_time}, currently at x = {last_arrival.x}")
        #print(f"next available arrival is
        #  {next_avail_arrival_time} due to speed of {last_arrival.speed}")
        # print(f"adding a new car on row {row} with
        #   speed {new_speed} which will arrive in {arrival}")

        if last_arrival.is_moving_left:
            hostiles.append(
                Hostile("sprites/rock1.png", 14, row - self.loaded_indices[0], speed = new_speed, static=False, left=True))
        else:
            hostiles.append(
                Hostile("sprites/rock1.png", 0, row - self.loaded_indices[0], speed = new_speed, static=False, left=False))

        # Replace currently loaded row with the updated one
        self.loaded[row - self.loaded_indices[0]] = hostiles


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

                # Append a new grass cell
                tree_texture = random.choices(
                    ['sprites/tree1_no_bush.png',
                    'sprites/tree2_no_bush.png',
                    'sprites/tree3_no_bush.png'],
                    weights = [0.33, 0.34, 0.33])

                sprites.append(
                    Obstacle(tree_texture[0], i, row - self.loaded_indices[0]))
                
                sprites[-1].scale = 0.95
                sprites[-1].center_y = c.TILE_HEIGHT * (row - self.loaded_indices[0]) + c.TILE_HEIGHT * 0.95

            # Otherwise, make it a random chance to be a rock
            else:
                chance = random.random()
                if chance < .3:

                    if last_rock == None or last_rock.x != i-1:
                        rock_texture = random.choices(
                            ['sprites/rock1.png',
                            'sprites/rock2.png',
                            'sprites/rock3.png',
                            'sprites/rock1_mossy.png',
                            'sprites/rock2_mossy.png',
                            'sprites/rock3_mossy.png',
                            'sprites/log.png',
                            'sprites/log_mossy.png',
                            'sprites/log_mushrooms.png'],
                            weights = [0.18, 0.18, 0.18, 0.08, 0.08, 0.08, 0.12, 0.06, 0.04])

                        last_rock = Obstacle(rock_texture[0], i, row - self.loaded_indices[0])
                        sprites.append(last_rock)

        return sprites

    def generate_honey(self, row):
        """
        generate_honey takes a row and generates it randomly
        to spawn honey that gives you points if you get it
        """

        # Will honey spawn in this row?
        if random.random() < .25:

            spawnable_spots = []

            # Mark spawnable spots
            for i in range(len(self.get_row(row))):

                cell = self.get_row(row)[i]

                if cell == None:

                    spawnable_spots.append(i)

            # Pick a random one and put it there
            x = random.choices(spawnable_spots)

            hunny = Obstacle('sprites/hunny.png',
                                            x[0],
                                            row - self.loaded_indices[0])

            self.hunny_list.append(hunny)
            
            return self.hunny_list
        
        # If no honey spawn, just return a blank list
        else:

            return arcade.SpriteList()

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
                Hostile("sprites/water.png", i, row - self.loaded_indices[0]))
        
        return river

    def generate_lilypads(self, row):
        """
        generate_lilypads takes a row and generates a lilypad that you
        can walk on to cross the river, with a random chance of spawning in each
        """

        lilypads = arcade.SpriteList()
        at_least_one = False

        while at_least_one == False:
            for i in range(15):

                if random.random() < .2:

                    lilypads.append(Obstacle('sprites/lilypad.png',
                                            i,
                                            row - self.loaded_indices[0]))
                    
            if len(lilypads) > c.MIN_LILYPADS_PER_RIVER:

                at_least_one = True

        return lilypads

    def generate_logs(self, row):
        '''
        generate_logs takes a row and generates a line of water that 
        kills you with logs that move across the screen that you can 
        jump on to cross
        '''

        logs = []
        x = 0

        # For each spot before the end
        while x < 15:

            # Try to spawn a log if  probablility
            if random.random() < 0.25:

                if logs and logs[-1][0].x != x - 1:

                    pass

                else:

                    if x <= 11:
                        length = random.randint(c.SMALLEST_LOG,c.BIGGEST_LOG)
                    else:
                        length = random.randint(c.SMALLEST_LOG, 15 - x)

                    log = arcade.SpriteList()

                    for i in range(length):

                        log.append(Obstacle('sprites/water_log.png',
                                            x + i,
                                            row - self.loaded_indices[0]))
                        #print(f"part of log in row {row} at {x+i}")
                    
                    logs.append(log)
                    x += length

            else:

                x += 1

        list = arcade.SpriteList()

        for log in logs:

            for sprite in log:

                list.append(sprite)

        return list
    
    def generate_victory(self, row):
        '''
        generate_victory takes a row and generates it randomly based on
        the "victory" quality -- surrounded by trees, with randomly placed
        rocks (similar to grassy). If the row is the last one in the game,
        place the victory cell, the "den"

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


        last_rock = None
        # For each cell in the row
        for i in range(c.COLUMN_COUNT):

            # The victory square should not be a rock
            if row == c.ENDING_Y and i == c.ENDING_X:
                den = Den('sprites/bear_2.png', i, row - self.loaded_indices[0])
                sprites.append(den)

            # Always a clear path to end
            elif i == c.ENDING_X:
                pass
            
            # Make it so values samples from the normal curve towards the edges
            # are more likely to be trees (we want a border)
            elif (grass[i] < -1 or
                grass[i] > 1):

                # Append a new grass cell
                tree_texture = random.choices(
                    ['sprites/tree1_no_bush.png',
                    'sprites/tree2_no_bush.png',
                    'sprites/tree3_no_bush.png'],
                    weights = [0.33, 0.34, 0.33])

                sprites.append(
                    Obstacle(tree_texture[0], i, row - self.loaded_indices[0]))
                
                sprites[-1].scale = 0.95
                sprites[-1].center_y = c.TILE_HEIGHT * (row - self.loaded_indices[0]) + c.TILE_HEIGHT * 0.95

            # Otherwise, make it a random chance to be a rock
            else:
                chance = random.random()
                if chance < .1:

                    if last_rock == None or last_rock.x != i-1:
                        rock_texture = random.choices(
                            ['sprites/rock1.png',
                            'sprites/rock2.png',
                            'sprites/rock3.png',
                            'sprites/rock1_mossy.png',
                            'sprites/rock2_mossy.png',
                            'sprites/rock3_mossy.png',
                            'sprites/log.png',
                            'sprites/log_mossy.png',
                            'sprites/log_mushrooms.png'],
                            weights = [0.18, 0.18, 0.18, 0.08, 0.08, 0.08, 0.12, 0.06, 0.04])

                        last_rock = Obstacle(rock_texture[0], i, row - self.loaded_indices[0])
                        sprites.append(last_rock)
    
        return sprites
    
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

            for sprite in self.loaded[row - self.loaded_indices[0]]:
                
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

    def get_platform(self, row):
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

            for sprite in self.platforms[row - self.loaded_indices[0]]:
                
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

    def get_car_rows(self):
        '''
        get_car_rows returns all the indices of current car rows

        param:
            self
        return:
            A list of all car row indices
        '''

        cars = []

        for i in self.loaded_indices:

            if self.rows[i] == "Road":

                cars.append(i)

        return cars

    def get_log_rows(self):
        '''
        get_log_rows returns all the indices of current log rows

        param:
            self
        return:
            A list of all log row indices
        '''

        logs = []

        for i in range(len(self.loaded)):

            if self.rows[i] == "River_Logs":

                logs.append(i)
        
        return logs
    
    def drunkards_walk(x, y):
        '''
        drunkards_walk returns the tiles in a given row which need to be empty

        param:
            x
            y
        returns:
            a list of coordinates in a row that must be empty
        '''
        path = []
        
        while y < 14:
            a = random.choices(['up', 'left', 'right'],
                            weights = [1/3, 1/3, 1/3])
            
            if a[0] == 'up':

                y += 1

                if not((x, y) in path):

                    path.append((x, y))
                    return path
                
            elif a[0] == 'right' and x != 14:

                x += 1

                if not((x, y) in path):

                    path.append((x, y))

            elif a[0] == 'left' and x != 0:

                x += -1

                if not((x, y) in path):

                    path.append((x, y))

