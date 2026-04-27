'''This module represents world generation'''
# Python Modules
import random
import arcade
from noise import pnoise1

# Constants
from scripts import constants as c

# Subengines
from scripts.engines.world_subengines.background_subengine import generate_background
from scripts.engines.world_subengines.collectible_subengine import generate_collectible
from scripts.engines.world_subengines.obstacle_subengine import generate_obstacles
from scripts.engines.world_subengines.platform_subengine import generate_platforms

# Objects
from scripts.objects.hostile_object import Hostile
from scripts.objects.obstacle_object import Obstacle
from scripts.objects.platform_object import Platform

class WorldEngine():
    '''
    The WorldGen class is the engine that generates
    the world pseudo-randomly
    '''

    def __init__(self, window, player, tex_eng):
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
        self.seed = round(random.random() * 10000000)
        self.noise_seed = self.seed / 1000000
        random.seed(self.seed)

        self.rows = []
        self.generate_array()

        self.tex_eng = tex_eng

        self.loaded_indices = []
        self.backgrounds = []
        self.obstacles = []
        self.platforms = []
        self.collectibles = []
        self.current_walk_coords = (c.STARTING_X, c.STARTING_Y)

        self.window = window
        self.player = player
        self.speed = None
        self.sprites = None
        self.spawn = [None]

        self.last_move_left = None
        self.fast_log_rows = []
        self.med_log_rows = []
        self.slow_log_rows = []

    def generate_array(self):
        '''
        generate_array fills the array created in the constructor
        with array values that indicate whether that row is a road, river,
        grass, etc, as well as other info each row may need, such as log speed.

        param: 
            self
        returns: 
            nothing
        '''
        # Make sure the first rows are always grass at the
        # beginning of the game
        for i in range(c.NUM_START_FOREST_ROWS):
            self.rows.append(['Forest'])

        # For each row... (excluding the first three which
        # should be grass
        for i in range(c.LEVEL_SIZE - c.NUM_START_FOREST_ROWS - c.NUM_ENDING_FOREST_ROWS):

            # Offset the seed a bit depending on the iteration and
            # find the value on the perlin noise wave
            x = self.noise_seed + i * .2
            noise = pnoise1(x)

            # Depending on the noise function's value, set the
            # appropriate value based on the legend

            # Gravel if the last row was a river
            if (self.rows[-1][0] == "River_Logs" or
                self.rows[-1][0] == "River_Lilypads"):

                self.rows.append(["Bank"])

            # River (lilypads)
            elif (noise >= -1 and noise <= -0.5):

                # River with lilypads
                self.rows.append(["River_Lilypads"])

            # River (with logs)
            elif(noise > -0.5 and noise <= -0.1):

                # random speed for log velocity
                rand_speed = random.choices([c.LOG_SPEED_SLOW, c.LOG_SPEED_MED, c.LOG_SPEED_FAST],
                                        weights = [1/3, 1/3, 1/3])[0]
                # River with logs
                self.rows.append(["River_Logs", rand_speed])

            # Forest
            elif (noise > -0.1 and noise <= 0.1):

                # Forest
                self.rows.append(["Forest"])

            # Wolfs
            elif (noise > 0.1 and noise <= 1):

                type = random.choice(['Wolf', 'Bees'])

                # Hostile
                self.rows.append(["Hostile", type])

            else:
                print("ERROR GENERATING ARRAY IN WORLD_GEN.PY DUE TO A" +
                       f"NOISE LEVEL OF {noise} NOT MATCHING ANY BIOME")

        # Make sure the first last rows are always grass at the
        # beginning of the game
        for i in range(c.NUM_ENDING_FOREST_ROWS):

            self.rows.append(['Victory'])

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

            background = generate_background(self.tex_eng, # Texture engine
                                             self.rows[i], # Biome
                                             i, # Current row
                                             self.loaded_indices[0]) # Current bottom row
            self.backgrounds.append(background)

            obstacle_info = generate_obstacles(self.tex_eng, # Texture engine
                                               self.current_walk_coords, # Current walk coords
                                               self.rows[i], # Biome
                                               i, # Current row
                                               self.loaded_indices[0]) # Current bottom row
            self.obstacles.append(obstacle_info[0])
            self.current_walk_coords = obstacle_info[1]

            # Randomly pick a velocity to add to list for initial screen generation

            platform_info = generate_platforms(self.tex_eng, # Texture engine
                                               self.platforms, # Current platforms
                                               self.current_walk_coords, # Current walk coords
                                               self.rows[i], # Biome
                                               i, # Current row
                                               self.loaded_indices[0]) # Current bottom row
            self.platforms.append(platform_info[0])
            self.current_walk_coords = platform_info[1]
            self.last_move_left = platform_info[2]

            collectible = generate_collectible(self.tex_eng, # Texture engine
                                            self.obstacles, # Current obstacles
                                            self.rows[i], # Current walk coords
                                            i, # Current row
                                            self.loaded_indices[0]) # Current bottom row
            self.collectibles.append(collectible)

        # append indices for each log row to an array according to its speed for time_engine
        curr_log_rows = self.get_log_rows()

        for i in curr_log_rows:
            if self.rows[i][1] == c.LOG_SPEED_SLOW:
                self.slow_log_rows.append(i)
            elif self.rows[i][1] == c.LOG_SPEED_MED:
                self.med_log_rows.append(i)
            elif self.rows[i][1] == c.LOG_SPEED_FAST:
                self.fast_log_rows.append(i)
            else:
                print("LOG SPEED APPENDING ERROR")
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
        self.backgrounds.pop(0)
        self.obstacles.pop(0)
        self.platforms.pop(0)
        self.collectibles.pop(0)
        self.loaded_indices.pop(0)

        # Generate a new row
        new_background = generate_background(self.tex_eng, # Texture engine
                                             self.rows[new_row_index], # Biome of new row index
                                             new_row_index, # New row index
                                             self.loaded_indices[0]) # Bottom row
        self.backgrounds.append(new_background)

        new_obstacle_info = generate_obstacles(self.tex_eng, # Texture engine
                                               self.current_walk_coords, # Current walk coords
                                               self.rows[new_row_index], # Biome
                                               new_row_index, # New row index
                                               self.loaded_indices[0]) # Bottom row
        self.obstacles.append(new_obstacle_info[0])
        self.current_walk_coords = new_obstacle_info[1]

        platform_info = generate_platforms(self.tex_eng, # Texture engine
                                               self.platforms, # Current platforms
                                               self.current_walk_coords, # Current walk coords
                                               self.rows[new_row_index], # Biome
                                               new_row_index, # Current row
                                               self.loaded_indices[0]) # Current bottom row

        if self.rows[new_row_index][0] == 'River_Logs':
            self.platforms.append(arcade.SpriteList())
            self.current_walk_coords = self.current_walk_coords
        else:
            self.platforms.append(platform_info[0])
            self.current_walk_coords = platform_info[1]

        new_collectible = generate_collectible(self.tex_eng, # Texture engine
                                                self.obstacles, # Current platforms
                                                self.rows[new_row_index], # Biome
                                                new_row_index, # New row index
                                                self.loaded_indices[0]) # Bottom row
        self.collectibles.append(new_collectible)

        self.loaded_indices.append(new_row_index)

        # Move everything else down (iterate over rows - 1 because
        # we have 1 less row)
        for i in range(c.ROW_COUNT - 1):
            self.backgrounds[i].move(change_x = 0,
                                     change_y = -c.TILE_SIZE)
            self.obstacles[i].move(change_x = 0,
                                change_y = -c.TILE_SIZE)
            self.platforms[i].move(change_x = 0,
                                change_y = -c.TILE_SIZE)
            self.collectibles[i].move(change_x = 0,
                                change_y = -c.TILE_SIZE)
        self.player.center_y -= c.VELOCITY_MULTIPLIER * c.RESOLUTION_RATIO
        self.player.angle = 180


        # get curr num of log rows and reset speed_log_rows to be empty
        # in order to properly loop thru spawn checks
        curr_log_rows = self.get_log_rows()
        self.slow_log_rows = []
        self.med_log_rows = []
        self.fast_log_rows = []

        for i in curr_log_rows:
            if self.rows[i][1] == c.LOG_SPEED_SLOW:
                self.slow_log_rows.append(i)
            elif self.rows[i][1] == c.LOG_SPEED_MED:
                self.med_log_rows.append(i)
            elif self.rows[i][1] == c.LOG_SPEED_FAST:
                self.fast_log_rows.append(i)
            else:
                print("LOG SPEED APPENDING ERROR")

        if self.rows[i][0] == 'River_Logs':

            for cell in self.platforms[-1]:

                print("generated with log")

    def update_wolves(self, row):
        '''
        update_wolves takes a row and updates the wolves in that row by trying
        to move them and then trying to spawn new ones if we are at the next
        spawn check

        param:
            self
            row
        returns:
            nothing
        '''

        hostiles = arcade.SpriteList()

        # Add the tree and hive first
        for wolf in self.obstacles[row - self.loaded_indices[0]]:

            if isinstance(wolf, Obstacle):

                hostiles.append(wolf)

        # For each Wolf in the row
        for wolf in self.obstacles[row - self.loaded_indices[0]]:

            # If it's still on screen, keep it
            if isinstance(wolf, Hostile) and not wolf.is_off_screen():
                hostiles.append(wolf)

        index = -1
        while len(hostiles) < 1:

            wolf = self.obstacles[row - self.loaded_indices[0]][index]

            if wolf.is_off_screen():
                hostiles.append(wolf)
                index -= 1


        # After cleaning up the current cacrs we have in a row,
        # let's check if we should add a new one!
        spawn = random.choices([True, False], weights=[20, 80])
        if not spawn[0]:
            return

        # First we need to determine  when the last in line
        # arrives (we don't want wolves lapping each other)
        index = -1

        while not isinstance(self.obstacles[row - self.loaded_indices[0]][index], Hostile):
            index -=1

        last_arrival = self.obstacles[row - self.loaded_indices[0]][index]

        # Arrival time if going right
        if last_arrival.left is False:
            last_arrival_time = (c.COLUMN_COUNT - last_arrival.x) * last_arrival.speed
        # vs left
        else:
            last_arrival_time = last_arrival.x * last_arrival.speed

        # Now that we know when the next one arrives, let's
        # pick a speed that won't cause this new wolf to lap
        # the last arriving of the previous wolves
        next_avail_arrival_time = last_arrival_time + last_arrival.speed
        # Max speed that would place the wolf arriving at the next available
        min_speed = next_avail_arrival_time / c.COLUMN_COUNT

        # Truncate that so we don't get any turtles
        if min_speed < c.LOWER_OBSTACLE_SPEED:
            min_speed = c.LOWER_OBSTACLE_SPEED

        new_speed = random.uniform(min_speed, c.UPPER_OBSTACLE_SPEED)

        # Truncate THAT so we don't get any speed demons
        if new_speed > c.UPPER_OBSTACLE_SPEED:
            new_speed = c.UPPER_OBSTACLE_SPEED

        type = self.rows[row][1]

        # Pick the texture
        if type == 'Wolf':

            hostile_texture = self.tex_eng.wolf[0]

        else:

            hostile_texture = self.tex_eng.swarm[0]

        if last_arrival.is_moving_left:

            wolf = Hostile(hostile_texture, 14, row - self.loaded_indices[0],
                         self.tex_eng, speed = new_speed, static=False, left=True)

        else:

            wolf = Hostile(hostile_texture, 0, row - self.loaded_indices[0],
                         self.tex_eng, speed = new_speed, static=False, left=False)

        wolf.scale = c.RESOLUTION_RATIO
        hostiles.append(wolf)

        # Replace currently loaded row with the updated one
        self.obstacles[row - self.loaded_indices[0]] = hostiles

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

        existing_row = self.platforms[row - self.loaded_indices[0]]
        if len(existing_row) > 0:
            tmp = existing_row[0]
            moving_left = tmp.is_moving_left
            self.last_move_left = moving_left
        else:
            moving_left = not self.last_move_left

        # For each log in the row
        for moving_cell in existing_row:

            # If it's still on screen, keep it
            if not moving_cell.is_off_screen():
                new_row.append(moving_cell)

        # After cleaning up the current logs we have in a row,
        # let's check if we should add a new one!

        # ensures spawn is assigned a value
        spawn = random.choices([True, False], weights=[50, 50])

        if self.rows[row][1] == c.LOG_SPEED_SLOW:
            spawn = random.choices([True, False], weights=[100, 0])
            # print("WE GOT SLOW!")
        elif self.rows[row][1] == c.LOG_SPEED_MED:
            spawn = random.choices([True, False], weights=[100, 0])
            # print("WE GOT MED!")
        elif self.rows[row][1] == c.LOG_SPEED_FAST:
            spawn = random.choices([True, False], weights=[100, 0])
            # print("WE GOT FAST!")

        if not spawn[0]:
            return

        # Randomly choose how many tiles the log is
        log_size = random.randint(c.SMALLEST_LOG, c.BIGGEST_LOG)

        for i in range(log_size):
            if moving_left:
                log_textures = self.tex_eng.get_log(log_size)
                # if there is a log on screen, copy the velocity for the next log spawned
                new_row.append(
                    Platform(log_textures[i], c.COLUMN_COUNT - 1 + i,
                                row - self.loaded_indices[0],
                                speed = self.rows[row][1],
                                static=False, left=True))
            else:
                log_textures = self.tex_eng.get_log(log_size)
                log_textures = list(reversed(log_textures))
                new_row.append(
                    Platform(log_textures[i], 0 - i, row - self.loaded_indices[0],
                             speed = self.rows[row][1],
                             static=False, left=False))

        # Replace currently loaded row with the updated one
        self.platforms[row - self.loaded_indices[0]] = new_row

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

            for sprite in self.obstacles[row - self.loaded_indices[0]]:

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

    def get_wolf_rows(self):
        '''
        get_wolf_rows returns all the indices of current wolf rows

        param:
            self
        returns:
            A list of all wolf row indices
        '''

        wolves = []

        for i in self.loaded_indices:

            if self.rows[i][0] == "Hostile":

                wolves.append(i)

        return wolves

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

            if self.rows[i][0] == "River_Logs":

                logs.append(i)

        return logs

    def update_resolution(self):
        '''
        Updates the current resolution
        
        param:
            self
        return:
            nothing
        '''
        ## FOR BACKGROUNDS
        for row in self.backgrounds:

            for cell in row:

                if cell is None:

                    pass

                else:

                    # Set the cell's center based on grid position
                    cell.center_x = c.TILE_SIZE * row.index(cell) + c.TILE_SIZE // 2
                    cell.center_y = (c.TILE_SIZE * self.backgrounds.index(row)
                                    + c.TILE_SIZE // 2)

                    cell.scale = c.RESOLUTION_RATIO

        ## FOR OBSTACLES
        for row in self.obstacles:

            for cell in row:

                if cell is None:

                    pass

                else:

                    # For trees specifically
                    if (isinstance(cell, Obstacle) and
                        cell.texture in [self.tex_eng.tree1, self.tex_eng.tree2, self.tex_eng.tree3,
                                        self.tex_eng.tree1_left_end, self.tex_eng.tree2_left_end,
                                        self.tex_eng.tree3_left_end, self.tex_eng.tree1_right_end,
                                        self.tex_eng.tree2_right_end, self.tex_eng.tree3_right_end,
                                        self.tex_eng.tree1_no_bush, self.tex_eng.tree2_no_bush,
                                        self.tex_eng.tree3_no_bush]):

                        cell.update_resolution(cell.x, cell.y, False)

                    elif isinstance(cell, Obstacle):

                        cell.update_resolution(cell.x, cell.y, True)

                    else:

                        cell.update_resolution(cell.x, cell.y)

        ## FOR PLATFORMS

        for row in self.platforms:

            for cell in row:

                cell.update_resolution(cell.x, cell.y)

        ## FOR COLLECTIBLES

        for row in self.collectibles:

            for cell in row:

                cell.update_resolution(cell.x, cell.y, True)
