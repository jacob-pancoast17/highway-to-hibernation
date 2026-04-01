'''This module represents world generation'''
import arcade
import constants as c
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

        # Fill a numpy vector with 15 zeros (this represents
        # each row on the current screen and gets filled with
        # values that will represent what "type" the row is--
        # e.g. road, river, grass, etc.
        self.rows = []
        self.generate_array()

        self.loaded = []
        self.platforms = []

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

        # Make sure the first three rows are always grass at the
        # beginning of the game
        self.rows.append('Grassy')
        self.rows.append('Grassy')
        self.rows.append('Grassy')

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

            bottom_row = self.generate_row(i)
            self.loaded.append(bottom_row)

            # Randomly pick a velocity to add to list
            rand_speed = random.choices([c.LOG_SPEED_SLOW, c.LOG_SPEED_MED, c.LOG_SPEED_FAST], weights = [1/3, 1/3, 1/3])
            #print(rand_speed)

            top_row = self.generate_platforms(i)
            self.platforms.append([top_row, rand_speed[0]])

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
        if self.rows[row] == "Road":

            return self.generate_cars(row)
        
        elif self.rows[row] == "Grassy":

            return self.generate_grassy(row)
        
        elif self.rows[row] == "River_Lilypads" or "River_Logs":

            return self.generate_river(row)
        else:

            print("PROBLEM IN GENERATION.")
            exit()

    def generate_platforms(self, row):

        # Use self.row[row] to figure out if the row generated was with lilypads or logs

        if self.rows[row] == 'River_Lilypads':

            return self.generate_lilypads(row)
        elif self.rows[row] == 'River_Logs':
            logs = self.generate_logs(row)

            return logs
            
        # for grassy
        elif self.rows[row] == "Grassy":

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
    
        return sprites
    
    def generate_honey(self, row):

        # Will honey spawn in this row?
        if random.random() < .25:

            spawnable_spots = []
            honey = arcade.SpriteList()

            # Mark spawnable spots
            for i in range(len(self.get_row(row))):

                cell = self.get_row(row)[i]

                if cell == None:

                    spawnable_spots.append(i)
            
            # Pick a random one and put it there
            x = random.choices(spawnable_spots)

            hunny = Obstacle('sprites/hunny.png',
                                            x[0],
                                            row)
            hunny.scale = .025
            honey.append(hunny)
            
            return honey
        
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
                Hostile("sprites/water.png", i, row))
        
        return river
    
    def generate_lilypads(self, row):

        lilypads = arcade.SpriteList()
        atLeastOne = False

        while atLeastOne == False:
            for i in range(15):

                if random.random() < .2:

                    lilypads.append(Obstacle('sprites/lilypad.png',
                                            i,
                                            row))
                    
            if len(lilypads) > c.MIN_LILYPADS_PER_RIVER:

                atLeastOne = True
                
        return lilypads
    
    def generate_logs(self, row):

        logs = []
        x = 0
        moving_left = random.choice([True, False])

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
                        #TODO somehow get speed index correct
                        log.append(Platform('sprites/rock1_mossy.png',
                                            x + i,
                                            row,
                                            speed= c.LOG_SPEED_SLOW,
                                            static= False,
                                            left= moving_left))
                        print(f"part of log in row {row} at {x+i}")
                    
                    logs.append(log)
                    x += length
            
            else:

                x += 1

        list = arcade.SpriteList()
        
        for log in logs:

            for sprite in log:

                list.append(sprite)
        
        return list
    
    def update_logs(self, row):

        curr_row_of_platforms = arcade.SpriteList()

        # For each log in the row
        for log in self.platforms[row][0]:

            # If it's still on screen, keep it
            if not log.is_off_screen():
                curr_row_of_platforms.append(log)

        index = 0
        while len(curr_row_of_platforms) == 0:
            
            log = self.platforms[row][0][index]
            if log.is_off_screen():
                curr_row_of_platforms.append(log)
            else:
                index += 1

            
        # After cleaning up the current logs we have in a row, 
        # let's check if we should add a new one! 

        # Change spawn rate weights based on current row speed

        if(self.platforms[row][1] == c.LOG_SPEED_SLOW):
            spawn = random.choices([True, False], weights=[70, 30])
            print("WE GOT SLOW!")
        elif(self.platforms[row][-1] == c.LOG_SPEED_MED):
            spawn = random.choices([True, False], weights=[60, 40])
            print("WE GOT MED")
        elif(self.platforms[row][-1] == c.LOG_SPEED_FAST):
            spawn = random.choices([True, False], weights=[50, 50])
            print("WE GOT FAST")
        

        #spawn = random.choices([True, False], weights=[70, 30])
        if not spawn[0]:
            return
        
        # First we need to determine  when the last in line 
        # arrives (we don't want logs lapping each other)
        last_arrival = curr_row_of_platforms[-1]

        # Randomly choose how many tiles the log is
        tile_num = random.randint(c.SMALLEST_LOG, c.BIGGEST_LOG)
        for i in range(tile_num):
            if last_arrival.is_moving_left:
                # if there is a log on screen, copy the velocity for the next log spawned
                curr_row_of_platforms.append(
                    Platform("sprites/rock1_mossy.png", c.COLUMN_COUNT - 1 + i, row, speed = self.platforms[row][1], static=False, left=True))
            else:
                #self.platforms[row][-1].speed need for speed
                curr_row_of_platforms.append(
                    Platform("sprites/rock1_mossy.png", 0 - i, row, speed = self.platforms[row][1], static=False, left=False))

        # Replace currently loaded row with the updated one
        self.platforms[row][0] = curr_row_of_platforms
    
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

            for sprite in self.platforms[row][0]:
                
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

        for i in range(c.ROW_COUNT):

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

            for i in range(len(self.platforms)):

                if self.rows[i] == "River_Logs":

                    logs.append(i)
            
            return logs
