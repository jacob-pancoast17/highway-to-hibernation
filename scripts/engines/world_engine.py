'''This module represents world generation'''
import random
import arcade
from noise import pnoise1
from scripts import constants as c
from scripts.objects.den_object import Den
from scripts.objects.hostile_object import Hostile
from scripts.objects.obstacle_object import Obstacle
from scripts.objects.platform_object import Platform

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
        returns: 
            nothing
        '''
        # Set a random seed for the perlin noise function
        self.seed = random.random() * 1000
        random.seed(self.seed)

        self.rows = []
        self.generate_array()

        self.loaded_indices = []
        self.loaded = []
        self.platforms = []
        self.collectibles = []
        self.current_walk_coords = (c.STARTING_X, c.STARTING_Y)

        self.window = window
        self.player = player
        self.speed = None
        self.sprites = None
        self.spawn = [None]

    def generate_array(self):
        '''
        generate_array fills the array created in the constructor
        with values that indicate whether that row is a road, river,
        grass, etc.

        param: 
            self
        returns: 
            nothing
        '''
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
            if (noise > -1 and noise < -0.5):

                # River with lilypads
                self.rows.append("River_Lilypads")

            elif(noise> -0.5 and noise < -0.1):

                # River with logs
                self.rows.append("River_Logs")

            elif (noise > -0.1 and noise < 0.1):

                # Grassy
                self.rows.append("Grassy")

            elif (noise > 0.1 and
                noise < 1):

                # Road
                self.rows.append("Road")

            else:
                print("ERROR GENERATING ARRAY IN WORLD_GEN.PY")

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

        for i in range(c.ROW_COUNT):
            self.loaded_indices.append(i)

            bottom_row = self.generate_row(i)
            self.loaded.append(bottom_row)

            # Randomly pick a velocity to add to list
            rand_speed = random.choices([c.LOG_SPEED_SLOW, c.LOG_SPEED_MED, c.LOG_SPEED_FAST],
                                        weights = [1/3, 1/3, 1/3])
            #print(rand_speed)

            middle_row = self.generate_platforms(i)
            self.platforms.append([middle_row, rand_speed[0]])

            top_row = self.generate_collectible(i)
            self.collectibles.append(top_row)

    def update_screen(self, new_row_index):
        '''
        update_screen is called whenever a new row needs to be generated, it pushes
        the previously drawn rows down so a new row can be added and is important 
        for our infinite generation

        param:
            self
            new_row_index
        returns:
            nothing
        '''
        # Delete the first row
        self.loaded.pop(0)
        self.platforms.pop(0)
        self.collectibles.pop(0)
        self.loaded_indices.pop(0)

        # Generate a new row
        new_row = self.generate_row(new_row_index)
        self.loaded.append(new_row)

        rand_speed = random.choices([c.LOG_SPEED_SLOW, c.LOG_SPEED_MED, c.LOG_SPEED_FAST],
                                    weights = [1/3, 1/3, 1/3])
        new_platform  = self.generate_platforms(new_row_index)
        self.platforms.append([new_platform, rand_speed[0]])

        new_collectible = self.generate_collectible(new_row_index)
        self.collectibles.append(new_collectible)

        self.loaded_indices.append(new_row_index)

        # Move everything else down (iterate over rows - 1 because
        # we have 1 less row)
        for i in range(c.ROW_COUNT - 1):
            self.loaded[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
            self.platforms[i][0].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
            self.collectibles[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
        self.player.center_y -= c.VELOCITY_MULTIPLIER
        self.player.angle = 180

    def generate_row(self, row):
        '''
        generate_row is a helper function that takes a row index 
        and generates that row by calling a child generate function
        based on what type of row it should be, assigned by the
        WorldGen's "rows" varaiable

        param: 
            self
            row - the current row to be generated
        returns:
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

            return self.generate_logs(row)

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
        returns:
            a SpriteList object from child function
        '''
        if self.rows[row] == 'Grassy':

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
        returns:
            a SpriteList object containing all of the object sprites for
                that row
        '''

        hostiles = arcade.SpriteList()

        # For each tile, just generate a hostile object that kills you

        moving_left = random.choice([True, False])
        # Pick a random speed
        self.speed = random.uniform(c.LOWER_OBSTACLE_SPEED, c.UPPER_OBSTACLE_SPEED)

        if not moving_left:
            hostiles.append(Hostile("sprites/rock1.png", 0, row - self.loaded_indices[0],
                                    self.speed, static=False, left=False))
        else:
            hostiles.append(Hostile("sprites/rock1.png", 14, row - self.loaded_indices[0],
                                    self.speed, static=False, left=True))

        return hostiles

    def update_cars(self, row):
        '''
        update_cars takes a row and updates the cars in that row by trying
        to move them and then trying to spawn new ones if we are at the next
        spawn check

        param:
            self
            row
        returns:
            nothing
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
        if last_arrival.left is False:
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

        if last_arrival.is_moving_left:
            hostiles.append(Hostile("sprites/rock1.png", 14, row - self.loaded_indices[0],
                         speed = new_speed, static=False, left=True))
        else:
            hostiles.append(Hostile("sprites/rock1.png", 0, row - self.loaded_indices[0],
                         speed = new_speed, static=False, left=False))

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
        returns:
            a SpriteList object containing all of the object sprites for
                that row
        '''

        sprites = arcade.SpriteList()

        # Generate a random number of trees
        trees_left = random.randint(1,4)
        trees_right = random.randint(1,4)

        walkable = self.drunkards_walk(self.current_walk_coords[0],
                                       self.current_walk_coords[1],
                                       trees_left,
                                       c.COLUMN_COUNT - trees_right)
        walkable = sorted(walkable, key=lambda x: x[1])

        last_rock = None
        # Append trees to the left
        for i in range(trees_left):

            tree_texture = random.choices(
                    ['sprites/tree1_no_bush.png',
                    'sprites/tree2_no_bush.png',
                    'sprites/tree3_no_bush.png'],
                    weights = [0.33, 0.34, 0.33])

            sprites.append(Obstacle(tree_texture[0], i, row=row - self.loaded_indices[0]))

            sprites[-1].scale = 0.95
            sprites[-1].center_y = (c.TILE_HEIGHT * (row - self.loaded_indices[0])
                                    + c.TILE_HEIGHT * 0.95)

        # Append rocks
        for i in range(c.COLUMN_COUNT - (trees_left + trees_right)):

            x = i + trees_left

            # We should not spawn in a rock
            if row == c.STARTING_Y and x == c.STARTING_X:
                pass

            # Rocks should not spawn on the walk
            elif (x, row) in walkable:
                pass

            # Otherwise, make it a random chance to be a rock
            else:
                chance = random.random()
                if chance < .3:

                    if last_rock is None or last_rock.x != i-1:
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

                        last_rock = Obstacle(rock_texture[0], x, row - self.loaded_indices[0])
                        sprites.append(last_rock)

        # Trees on the right
        for i in range(trees_right):

            x = c.COLUMN_COUNT - trees_right + i

            tree_texture = random.choices(
                    ['sprites/tree1_no_bush.png',
                    'sprites/tree2_no_bush.png',
                    'sprites/tree3_no_bush.png'],
                    weights = [0.33, 0.34, 0.33])
            sprites.append(
                    Obstacle(tree_texture[0], x, row - self.loaded_indices[0]))
            sprites[-1].scale = 0.95
            sprites[-1].center_y = (c.TILE_HEIGHT * (row - self.loaded_indices[0]) +
                                    c.TILE_HEIGHT * 0.95)


        # Update walk
        self.current_walk_coords = walkable[-1]

        return sprites

    def generate_honey(self, row):
        """
        generate_honey takes a row and generates it randomly
        to spawn honey that gives you points if you get it

        param:
            self
            row - a row index to be generated
        returns:
            a SpriteList object containing all of the object sprites for
                that row
        """

        self.sprites = arcade.SpriteList()

        # Will honey spawn in this row?
        if random.random() < .25:

            spawnable_spots = list(range(15))
            #print(row - self.loaded_indices[0])
            cells = self.loaded[row - self.loaded_indices[0]]

            # Remove not spawnable spots
            for cell in cells:

                spawnable_spots.remove(cell.x)

            # Pick a random one and put it there
            x = random.choices(spawnable_spots)

            hunny = Obstacle('sprites/hunny.png',
                                            x[0],
                                            row - self.loaded_indices[0])
            self.sprites.append(hunny)

            return self.sprites

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
        returns:
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

        param:
            self
            row
        returns:
            a SpriteList object containing all of the lilypad sprites for
                that row
        """

        lilypads = arcade.SpriteList()

        walkable = self.drunkards_walk(self.current_walk_coords[0], row, 4, c.COLUMN_COUNT - 4)
        walkable = sorted(walkable, key=lambda x: x[1])

        # Append all except the last one
        for i in range(len(walkable) - 1):

            lilypads.append(Obstacle('sprites/lilypad.png',
                                            walkable[i][0],
                                            walkable[i][1]))
            print("Lilypad on")
            print(walkable[i][0], walkable[i][1])

        for i in range(c.COLUMN_COUNT):

            if ((i, row) not in walkable and
                random.random() < .2):

                lilypads.append(Obstacle('sprites/lilypad.png', i, row - self.loaded_indices[0]))

        # Update walk
        self.current_walk_coords = walkable[-1]

        return lilypads

    def generate_logs(self, row):
        '''
        generate_logs takes a row and generates a line of water that 
        kills you with logs that move across the screen that you can 
        jump on to cross

        param:
            self
            row
        returns:
            a SpriteList object containing all of the log sprites for
                that row
        '''

        log_cells = arcade.SpriteList()
        moving_left = random.choice([True, False])

        length = random.randint(c.SMALLEST_LOG,c.BIGGEST_LOG)

        rand_speed = random.choices([c.LOG_SPEED_SLOW, c.LOG_SPEED_MED, c.LOG_SPEED_FAST],
                                        weights = [1/3, 1/3, 1/3])


        for i in range(length):

            if moving_left:

                log_cells.append(Platform('sprites/water_log.png',
                                    15 - i,
                                    row= row - self.loaded_indices[0],
                                    static = False,
                                    speed= rand_speed[0],
                                    left=True))

            else:

                log_cells.append(Platform('sprites/water_log.png',
                                    i,
                                    row= row - self.loaded_indices[0],
                                    static = False,
                                    speed= rand_speed[0],
                                    left=False))

        for log in log_cells:
            print(f"{log} x: {log.x}, y: {log.y}")
        return log_cells

    def generate_victory(self, row):
        '''
        generate_victory takes a row and generates it randomly based on
        the "victory" quality -- surrounded by trees, with randomly placed
        rocks (similar to grassy). If the row is the last one in the game,
        place the victory cell, the "den"

        param:
            self
            row - a row index to be generated
        returns:
            a SpriteList object containing all of the object sprites for
                that row
        '''

        sprites = arcade.SpriteList()

        # Generate a random number of trees
        trees_left = random.randint(1,4)
        trees_right = random.randint(1,4)


        last_rock = None
        # Append trees to the left
        for i in range(trees_left):

            tree_texture = random.choices(
                    ['sprites/tree1_no_bush.png',
                    'sprites/tree2_no_bush.png',
                    'sprites/tree3_no_bush.png'],
                    weights = [0.33, 0.34, 0.33])

            sprites.append(
                    Obstacle(tree_texture[0], i, row - self.loaded_indices[0]))

            sprites[-1].scale = 0.95
            sprites[-1].center_y = (c.TILE_HEIGHT * (row - self.loaded_indices[0])
                                    + c.TILE_HEIGHT * 0.95)

        for i in range(c.COLUMN_COUNT - trees_left - trees_right):

            x = i + trees_left

            # The victory square should not be a rock
            if row == c.ENDING_Y and x == c.ENDING_X:
                den = Den('sprites/den.png', x, row - self.loaded_indices[0])
                sprites.append(den)

            # Always a clear path to end
            elif x == c.ENDING_X:
                pass

            # Otherwise, make it a random chance to be a rock
            else:
                chance = random.random()
                if chance < .1:

                    if last_rock is None or last_rock.x != i-1:
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

                        last_rock = Obstacle(rock_texture[0], x, row - self.loaded_indices[0])
                        sprites.append(last_rock)

        # Trees on the right
        for i in range(trees_right):

            x = c.COLUMN_COUNT - trees_right + i

            tree_texture = random.choices(
                    ['sprites/tree1_no_bush.png',
                    'sprites/tree2_no_bush.png',
                    'sprites/tree3_no_bush.png'],
                    weights = [0.33, 0.34, 0.33])

            sprites.append(
                    Obstacle(tree_texture[0], x, row - self.loaded_indices[0]))

            sprites[-1].scale = 0.95
            sprites[-1].center_y = (c.TILE_HEIGHT * (row - self.loaded_indices[0])
                                    + c.TILE_HEIGHT * 0.95)

        return sprites

    def update_logs(self, row):
        '''
        update_logs takes a row and updates the logs in that row by trying
        to move them and then trying to spawn new ones if we are at the next
        spawn check

        param:
            self
            row
        returns:
            nothing
        '''
        new_row = arcade.SpriteList()

        existing_row = self.platforms[row - self.loaded_indices[0]][0]
        tmp = existing_row[0]
        moving_left = tmp.is_moving_left

        # For each log in the row
        for moving_cell in existing_row:

            # If it's still on screen, keep it
            if not moving_cell.is_off_screen():
                new_row.append(moving_cell)

        # We want at least one so we can store if the row is a left row or a right row
        if len(new_row) == 0:

            new_row.append(tmp)

        # After cleaning up the current logs we have in a row,
        # let's check if we should add a new one!

        # ensures spawn is assigned a value
        spawn = random.choices([True, False], weights=[50, 50])

        if self.platforms[row - self.loaded_indices[0]][1] == c.LOG_SPEED_SLOW:
            spawn = random.choices([True, False], weights=[65, 35])
            print("WE GOT SLOW!")
        elif self.platforms[row - self.loaded_indices[0]][1] == c.LOG_SPEED_MED:
            spawn = random.choices([True, False], weights=[70, 30])
            print("WE GOT MED")
        elif self.platforms[row - self.loaded_indices[0]][1] == c.LOG_SPEED_FAST:
            spawn = random.choices([True, False], weights=[90, 10])
            #print("WE GOT FAST")

        if not spawn[0]:
            return

        # Randomly choose how many tiles the log is
        log_size = random.randint(c.SMALLEST_LOG, c.BIGGEST_LOG)
        for i in range(log_size):
            if moving_left:
                # if there is a log on screen, copy the velocity for the next log spawned
                new_row.append(
                    Platform("sprites/water_log.png", c.COLUMN_COUNT - 1 + i,
                                row - self.loaded_indices[0],
                                speed = self.platforms[row - self.loaded_indices[0]][1],
                                static=False, left=True))
            else:
                new_row.append(
                    Platform("sprites/water_log.png", 0 - i, row - self.loaded_indices[0],
                             speed = self.platforms[row - self.loaded_indices[0]][1],
                             static=False, left=False))
        # Replace currently loaded row with the updated one
        self.platforms[row - self.loaded_indices[0]][0] = new_row
        # print("SPEED:")
        # print(self.platforms[row - self.loaded_indices[0]][1])

    def get_row(self, row):
        '''
        get_row takes a row and returns a list version of all the sprites
        in that row (NOT a SpriteList) as a pyarcade SpriteList can only
        contain sprites, but we need spaces that contain 'None'-- a blank
        tile

        param:
            self
            row - a row index to convert from a SpriteList to a list 
        returns:
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
        returns:
            the row as a list of sprite objects and Nones
        '''

        return_list = []

        # For every x position in the row
        for x in range(c.COLUMN_COUNT):

            there_was_a_sprite = False

            for sprite in self.platforms[row - self.loaded_indices[0]][0]:

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
        returns:
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
        returns:
            A list of all log row indices
        '''

        logs = []

        for i in self.loaded_indices:

            if self.rows[i] == "River_Logs":

                logs.append(i)

        return logs

    def drunkards_walk(self, x, y, left_bound, right_bound):
        '''
        drunkards_walk returns the tiles in a given row which need to be empty

        param:
            x
            y
        returns:
            a list of coordinates in a row that must be empty
        '''
        path = [(x, y)]

        while True:
            a = random.choices(['up', 'left', 'right'],
                            weights = [1/3, 1/3, 1/3])

            if a[0] == 'up':

                y += 1

                path.append((x, y))
                return path

            elif a[0] == 'right' and x != right_bound:

                x += 1

                if (x, y)not in path:

                    path.append((x, y))

            elif a[0] == 'left' and x != left_bound:

                x += -1

                if (x, y)not in path:

                    path.append((x, y))
