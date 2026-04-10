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
        self.seed = random.random() * 1000
        print(self.seed)
        random.seed(self.seed)

        self.rows = []
        self.generate_array()

        self.tex_eng = tex_eng

        self.loaded_indices = []
        self.backgrounds = []
        self.loaded = []
        self.platforms = []
        self.collectibles = []
        self.current_walk_coords = (c.STARTING_X, c.STARTING_Y)

        self.window = window
        self.player = player
        self.speed = None
        self.sprites = None
        self.spawn = [None]

        self.log_moving_left = random.choice([True, False])
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
            x = self.seed + i * .2
            noise = pnoise1(x)

            # Depending on the noise function's value, set the
            # appropriate value based on the legend

            # Gravel if the last row was a river
            if (self.rows[-1][0] == "River_Logs" or
                self.rows[-1][0] == "River_Lilypads"):

                self.rows.append(["Bank"])

            # River (lilypads)
            elif (noise > -1 and noise < -0.5):

                # River with lilypads
                self.rows.append(["River_Lilypads"])

            # River (with logs)
            elif(noise> -0.5 and noise < -0.1):

                # random speed for log velocity
                rand_speed = random.choices([c.LOG_SPEED_SLOW, c.LOG_SPEED_MED, c.LOG_SPEED_FAST],
                                        weights = [1/3, 1/3, 1/3])
                # River with logs
                self.rows.append(["River_Logs", rand_speed[0]])

            # Forest
            elif (noise > -0.1 and noise < 0.1):

                # Forest
                self.rows.append(["Forest"])

            # Wolfs
            elif (noise > 0.1 and
                noise < 1):

                # Pack
                self.rows.append(["Pack"])

            else:
                print("ERROR GENERATING ARRAY IN WORLD_GEN.PY")

        # Make sure the first last rows are always grass at the
        # beginning of the game
        for i in range(c.NUM_ENDING_FOREST_ROWS):

            self.rows.append(['Victory'])
        #TODO create fast_log_rows, med_log_rows, and slow_log_rows here and update in update screen
        

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

            background = self.generate_background(i)
            self.backgrounds.append(background)

            bottom_row = self.generate_row(i)
            self.loaded.append(bottom_row)

            # Randomly pick a velocity to add to list for initial screen generation
    
            middle_row = self.generate_platforms(i)

            self.platforms.append(middle_row)

            top_row = self.generate_collectible(i)
            self.collectibles.append(top_row)

        # append indices for each log row to an array according to its speed for time_engine
        curr_log_rows = self.get_log_rows()
        for i in curr_log_rows:
            if (self.rows[i][1] == c.LOG_SPEED_SLOW):
                self.slow_log_rows.append(i)
            elif (self.rows[i][1] == c.LOG_SPEED_MED):
                self.med_log_rows.append(i)
            elif (self.rows[i][1] == c.LOG_SPEED_FAST):
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
        self.loaded.pop(0)
        self.platforms.pop(0)
        self.collectibles.pop(0)
        self.loaded_indices.pop(0)

        # Generate a new row
        new_background = self.generate_background(new_row_index)
        self.backgrounds.append(new_background)

        new_row = self.generate_row(new_row_index)
        self.loaded.append(new_row)

        new_platform  = self.generate_platforms(new_row_index)
        self.platforms.append(new_platform)


        new_collectible = self.generate_collectible(new_row_index)
        self.collectibles.append(new_collectible)

        self.loaded_indices.append(new_row_index)

        # Move everything else down (iterate over rows - 1 because
        # we have 1 less row)
        for i in range(c.ROW_COUNT - 1):
            self.backgrounds[i].move(change_x = 0,
                                     change_y = -c.TILE_HEIGHT)
            self.loaded[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
            self.platforms[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
            self.collectibles[i].move(change_x = 0,
                                change_y = -c.TILE_HEIGHT)
        self.player.center_y -= c.VELOCITY_MULTIPLIER
        self.player.angle = 180


        # get curr num of log rows and reset speed_log_rows to be empty
        # in order to properly loop thru spawn checks
        curr_log_rows = self.get_log_rows()
        self.slow_log_rows = []
        self.med_log_rows = []
        self.fast_log_rows = []

        for i in curr_log_rows:
            if (self.rows[i][1] == c.LOG_SPEED_SLOW):
                self.slow_log_rows.append(i)
            elif (self.rows[i][1] == c.LOG_SPEED_MED):
                self.med_log_rows.append(i)
            elif (self.rows[i][1] == c.LOG_SPEED_FAST):
                self.fast_log_rows.append(i)
            else:
                print("LOG SPEED APPENDING ERROR")

    def generate_background(self, row):
        '''
        generate_background is a helper function that takes a row index 
        and generates that row of backgrounds by calling a child generate 
        function based on what type of row it should be, assigned by the
        WorldGen's "rows" varaiable

        param: 
            self
            row - the current row to be generated
        returns:
            a SpriteList object from child function
        '''

        if self.rows[row][0] == "Pack":

            return self.generate_grass(row)

        elif self.rows[row][0] == "Forest":

            return self.generate_grass(row)

        # Rivers don't need a background
        elif (self.rows[row][0] == "River_Lilypads" or
              self.rows[row][0] =="River_Logs"):

            return arcade.SpriteList()
        
        elif (self.rows[row][0] == "Bank"):

            return self.generate_bank(row)

        elif self.rows[row][0] == "Victory":

            return self.generate_grass(row)

        else:

            print("PROBLEM IN GENERATION.")
            exit()



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
        if self.rows[row][0] == "Pack":

            return self.generate_wolves(row)

        elif self.rows[row][0] == "Forest":

            return self.generate_forest(row)

        elif (self.rows[row][0] == "River_Lilypads" or
              self.rows[row][0] =="River_Logs"):

            return self.generate_river(row)
        
        elif (self.rows[row][0] == "Bank"):

            return arcade.SpriteList()

        elif self.rows[row][0] == "Victory":

            return self.generate_victory(row)

        else:

            print("PROBLEM IN GENERATION.")
            exit()

    def generate_platforms(self, row):
        '''
        generates platforms
        '''

        # Use self.row[row] to figure out if the row generated was with lilypads or logs

        if self.rows[row][0] == 'River_Lilypads':

            return self.generate_lilypads(row)

        elif self.rows[row][0] == 'River_Logs':

            return self.generate_logs(row, self.log_moving_left)

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
        if self.rows[row][0] == 'Forest':

            return self.generate_honey(row)

        else:

            return arcade.SpriteList()
        
    def generate_grass(self, row):
        '''
        generate_grass takes a row and generates the grass background
        for it

        param:
            self
            row - the row index to be drawn at
        returns:
            a spritelist of grass objects
        '''

        grass = arcade.SpriteList()

        for i in range(c.COLUMN_COUNT):

            grass_texture = random.choices(
                    ['sprites/grass_1.png',
                    'sprites/grass_2.png',
                    'sprites/grass_3.png',
                    'sprites/flowers_1.png',
                    'sprites/flowers_2.png',
                    'sprites/flowers_3.png'],
                    weights = [0.22, 0.22, 0.22,
                               0.11, 0.11, 0.11])[0]
            
            cell = arcade.Sprite(grass_texture)
            
            # Set the cell's center based on grid position
            cell.center_x = c.TILE_WIDTH * i + c.TILE_WIDTH // 2
            cell.center_y = c.TILE_HEIGHT * (row - self.loaded_indices[0]) + c.TILE_HEIGHT // 2

            grass.append(cell)
        
        return grass
    
    def generate_bank(self, row):
        '''
        generate_bank takes a row and generates the bank background
        for it

        param:
            self
            row - the row index to be drawn at
        returns:
            a spritelist of gravel objects
        '''

        bank = arcade.SpriteList()

        for i in range(c.COLUMN_COUNT):            
                
            bank_texture = random.choices(["sprites/bank_1.png",
                                           "sprites/bank_2.png",
                                           "sprites/bank_3.png"],
                                           weights = [
                                               1/3,
                                               1/3,
                                               1/3
                                           ])[0]

            cell = arcade.Sprite(bank_texture)

            # Set the cell's center based on grid position
            cell.center_x = c.TILE_WIDTH * i + c.TILE_WIDTH // 2
            cell.center_y = c.TILE_HEIGHT * (row - self.loaded_indices[0]) + c.TILE_HEIGHT // 2

            bank.append(cell)
        
        return bank


    def generate_wolves(self, row):
        '''
        generate_wolves takes a row and generates it randomly based on
        the "wolves" quality -- moving objects across the screen

        param:
            self
            row - a row index to be generated
        returns:
            a SpriteList object containing all of the object sprites for
                that row
        '''

        walkable = self.drunkards_walk(self.current_walk_coords[0],
                                       self.current_walk_coords[1],
                                       4, c.COLUMN_COUNT - 4)
        walkable = sorted(walkable, key=lambda x: x[1])

        hostiles = arcade.SpriteList()

        # For each tile, just generate a hostile object that kills you

        moving_left = random.choice([True, False])
        # Pick a random speed
        self.speed = random.uniform(c.LOWER_OBSTACLE_SPEED, c.UPPER_OBSTACLE_SPEED)

        if not moving_left:
            hostiles.append(Hostile(self.tex_eng.wolf[0], 0, row - self.loaded_indices[0],
                                    self.tex_eng, self.speed, static=False, left=False))
        else:
            hostiles.append(Hostile(self.tex_eng.wolf[0], 14, row - self.loaded_indices[0],
                                    self.tex_eng, self.speed, static=False, left=True))
            

        self.current_walk_coords = walkable[-1]

        self.current_walk_coords = walkable[-1]

        return hostiles

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

        # For each Wolf in the row
        for wolf in self.loaded[row - self.loaded_indices[0]]:

            # If it's still on screen, keep it
            if not wolf.is_off_screen():
                hostiles.append(wolf)

        index = 0
        while len(hostiles) == 0:

            wolf = self.loaded[row - self.loaded_indices[0]][index]
            if wolf.is_off_screen():
                hostiles.append(wolf)
            else:
                index += 1


        # After cleaning up the current cacrs we have in a row,
        # let's check if we should add a new one!
        spawn = random.choices([True, False], weights=[20, 80])
        if not spawn[0]:
            return

        # First we need to determine  when the last in line
        # arrives (we don't want wolves lapping each other)
        last_arrival = hostiles[-1]

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

        if last_arrival.is_moving_left:
            hostiles.append(Hostile(self.tex_eng.wolf[0], 14, row - self.loaded_indices[0],
                         self.tex_eng, speed = new_speed, static=False, left=True))
        else:
            hostiles.append(Hostile(self.tex_eng.wolf[0], 0, row - self.loaded_indices[0],
                         self.tex_eng, speed = new_speed, static=False, left=False))

        # Replace currently loaded row with the updated one
        self.loaded[row - self.loaded_indices[0]] = hostiles


    def generate_forest(self, row):
        '''
        generate_forest takes a row and generates it randomly based on
        the "Forest" quality -- surrounded by trees, with randomly placed
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
        num_trees_left = random.randint(1,4)
        num_trees_right = random.randint(1,4)

        walkable = self.drunkards_walk(self.current_walk_coords[0],
                                       self.current_walk_coords[1],
                                       num_trees_left,
                                       c.COLUMN_COUNT - num_trees_right)
        walkable = sorted(walkable, key=lambda x: x[1])

        last_rock = None

        # Append trees to the left
        tree_textures_left = self.tex_eng.get_trees(num_trees_left, False)

        for i in range(num_trees_left):

            tree_texture = tree_textures_left[i]

            tree = Obstacle(tree_texture, i, row=row - self.loaded_indices[0])

            tree.center_y = (c.TILE_HEIGHT * (row - self.loaded_indices[0])
                                    + c.TILE_HEIGHT)
            
            sprites.append(tree)

        # Append rocks
        for i in range(c.COLUMN_COUNT - (num_trees_left + num_trees_right)):

            x = i + num_trees_left

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
        tree_textures_right = self.tex_eng.get_trees(num_trees_right, True)

        for i in range(num_trees_right):
            
            x = c.COLUMN_COUNT - num_trees_right + i

            tree_texture = tree_textures_right[i]

            tree = Obstacle(tree_texture, x, row=row - self.loaded_indices[0])

            tree.center_y = (c.TILE_HEIGHT * (row - self.loaded_indices[0])
                                    + c.TILE_HEIGHT)
            
            sprites.append(tree)


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
                Hostile("sprites/water.png", i, row - self.loaded_indices[0], self.tex_eng))

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

        walkable = self.drunkards_walk(self.current_walk_coords[0], row - self.loaded_indices[0],
                                       4, c.COLUMN_COUNT - 4)
        walkable = sorted(walkable, key=lambda x: x[1])

        # Append all except the last one
        for i in range(len(walkable) - 1):

            lilypads.append(Platform('sprites/lilypad.png',
                                            walkable[i][0],
                                            walkable[i][1]))

        for i in range(4, c.COLUMN_COUNT - 4):

            if ((i, row) not in walkable and random.random() < .2):

                lilypad_texture = random.choices(
                    ['sprites/lilypad.png',
                    'sprites/pink frog.png'],
                    weights = [0.9, 0.1])

                for lilypad in lilypads:

                    if lilypad.x is not i:

                        lilypads.append(Platform(lilypad_texture[0], i,
                                                row - self.loaded_indices[0]))

        # Update walk
        self.current_walk_coords = walkable[-1]

        return lilypads

    def generate_logs(self, row, moving_left):
        '''
        generate_logs takes a row and generates a line of water that 
        kills you with logs that move across the screen that you can 
        jump on to cross

        param:
            self
            row
            log_moving_left
        returns:
            a SpriteList object containing all of the log sprites for
                that row
        '''

        walkable = self.drunkards_walk(self.current_walk_coords[0], row, 4, c.COLUMN_COUNT - 4)
        walkable = sorted(walkable, key=lambda x: x[1])

        log_cells = arcade.SpriteList()

        length = random.randint(c.SMALLEST_LOG,c.BIGGEST_LOG)

        for i in range(length):

            if moving_left:

                log_textures = self.tex_eng.get_log(length)

                #speed for this one: self.platforms[(row - self.loaded_indices[0])-1][1]

                log_cells.append(Platform(log_textures[length - 1 - i],
                                    15 - i,
                                    row= row - self.loaded_indices[0],
                                    static = False,
                                    speed= self.rows[row][1],
                                    left=True))

            else:

                log_textures = self.tex_eng.get_log(length)

                log_cells.append(Platform(log_textures[i],
                                    i,
                                    row= row - self.loaded_indices[0],
                                    static = False,
                                    speed= self.rows[row][1],
                                    left=False))

        for log in log_cells:
            print(f"{log} x: {log.x}, y: {log.y}")

        # Update walk
        self.current_walk_coords = walkable[-1]

        # Change log direction for next row
        self.log_moving_left = not moving_left


        return log_cells

    def generate_victory(self, row):
        '''
        generate_victory takes a row and generates it randomly based on
        the "victory" quality -- surrounded by trees, with randomly placed
        rocks (similar to Forest). If the row is the last one in the game,
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
        
        existing_row = self.platforms[row - self.loaded_indices[0]]
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

            if self.rows[i][0] == "Pack":

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

            elif a[0] == 'right' and x < right_bound:

                x += 1

                if (x, y)not in path:

                    path.append((x, y))

            elif a[0] == 'left' and x > left_bound:

                x += -1

                if (x, y)not in path:

                    path.append((x, y))
