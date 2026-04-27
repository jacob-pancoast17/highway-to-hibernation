'''This module loads and manages textures'''
import random
import arcade

from scripts import constants as c

class TextureEngine():
    '''
    The TextureEngine manages textures, loads them, and draws every frame
    '''

    def __init__(self):
        '''
        Constructor

        param:
            self
        returns:
            nothing
        '''

        ### SPRITES

        ## BEAR

        # list of the current sprites for each bear skin
        # list order: walk sprite, death1, death2
        bear_sprite_set = []

        if c.SKIN == "Polar":
            bear_sprite_set = ["sprites/polar_bear.png", "sprites/polar_bear_death1.png",
                               "sprites/polar_bear_death2_sheet.png"]
        elif c.SKIN == "Black" :
            bear_sprite_set = ["sprites/black_bear.png", "sprites/black_bear_death1.png",
                               "sprites/black_bear_death2_sheet.png"]
        elif c.SKIN == "Pooh" :
            bear_sprite_set = ["sprites/pooh_bear.png", "sprites/pooh_bear_death1.png",
                               "sprites/pooh_bear_death2_sheet.png"]
        else:
            # Grizzly is default
            bear_sprite_set = ["sprites/bear_rev2.png", "sprites/bear_death1.png",
                               "sprites/bear_death2_sheet.png"]

        self.bear = bear_sprite_set[0]
        # player
        self.player = None
        # world
        self.world = None
        # Deaths
        drowning_sheet = arcade.load_spritesheet(bear_sprite_set[2])
        self.drowning = drowning_sheet.get_texture_grid(size = (30, 30), columns=9, count=9)

        self.mauled = arcade.load_texture(bear_sprite_set[1])

        wolf_sheet = arcade.load_spritesheet("sprites/wolf_sheet.png")
        self.wolf = drowning_sheet.get_texture_grid(size = (30, 30), columns=9, count=9)

        wolf_sheet = arcade.load_spritesheet("sprites/wolf_sheet.png")
        self.wolf = drowning_sheet.get_texture_grid(size = (30, 30), columns=9, count=9)

        ## HUNNY
        self.hunny = 'sprites/hunny.png'

        ## BACKGROUNDS

        # Grass
        self.grass1 = 'sprites/grass_1.png'
        self.grass2 = 'sprites/grass_2.png'
        self.grass3 = 'sprites/grass_3.png'
        self.flowers1 = 'sprites/flowers_1.png'
        self.flowers2 = 'sprites/flowers_2.png'
        self.flowers3 = 'sprites/flowers_3.png'

        # Bank
        self.bank1 = 'sprites/bank_1.png'
        self.bank2 = 'sprites/bank_2.png'
        self.bank3 = 'sprites/bank_3.png'

        ## OBSTACLES
        # Trees
        self.tree1 = "sprites/tree1.png"
        self.tree2 = "sprites/tree2.png"
        self.tree3 = "sprites/tree3.png"

        self.tree1_left_end = "sprites/tree1_left_end.png"
        self.tree2_left_end = "sprites/tree2_left_end.png"
        self.tree3_left_end = "sprites/tree3_left_end.png"

        self.tree1_right_end = "sprites/tree1_right_end.png"
        self.tree2_right_end = "sprites/tree2_right_end.png"
        self.tree3_right_end = "sprites/tree3_right_end.png"

        self.tree1_no_bush = "sprites/tree1_no_bush.png"
        self.tree2_no_bush = "sprites/tree2_no_bush.png"
        self.tree3_no_bush = "sprites/tree3_no_bush.png"

        # Logs
        self.logs = ["sprites/water_log_left_end.png",
                     "sprites/water_log_connector.png",
                     "sprites/water_log_right_end.png"]

        # Wolf
        wolf_sheet = arcade.load_spritesheet("sprites/wolf_sheet.png")
        self.wolf = wolf_sheet.get_texture_grid(size = (30, 30), columns=11, count=11)

        # Bees
        hive_sheet = arcade.load_spritesheet("sprites/beehive.png")
        self.hive = hive_sheet.get_texture_grid(size = (30, 30), columns=17, count=17)

        bees_sheet = arcade.load_spritesheet("sprites/bees.png")
        self.swarm = bees_sheet.get_texture_grid(size = (30, 30), columns=6, count=6)

    def add_player(self, player):
        '''
        add_player is a helper function with initializes the player sprite and adds
        it to the game
        
        param:
            self
            player - a player
        returns:
            nothing
        '''
        self.player = arcade.SpriteList()
        self.player.append(player)

    def add_world(self, world):
        '''
        add_world is a helper function with initializes the world and adds it to the game
        
        param:
            self
            world - a world
        returns:
            nothing
        '''
        self.world = world

    def create_grid(self):
        '''
        create_grid creates the grid of grass sprites

        param:
            self
        returns:
            a list of sprites corresponding to the grid cells
        '''
        grid = arcade.SpriteList()

        for row in range(c.ROW_COUNT):

            for column in range(c.COLUMN_COUNT):

                # Append a new grass cell
                grass_texture = random.choices(
                    ['sprites/grass_1.png',
                    'sprites/grass_2.png',
                    'sprites/grass_3.png',
                    'sprites/flowers_1.png',
                    'sprites/flowers_2.png',
                    'sprites/flowers_3.png'],
                    weights = [0.22, 0.22, 0.22,
                               0.11, 0.11, 0.11])

                cell = arcade.Sprite(grass_texture[0])

                # Set the cell's center based on grid position
                cell.center_x = c.TILE_SIZE * column + c.TILE_SIZE // 2
                cell.center_y = c.TILE_SIZE * row + c.TILE_SIZE // 2

                # Append to list of all grid sprites to draw
                grid.append(cell)

        return grid

    def get_grass(self):
        '''
        get_grass returns a random grass texture

        param:
            self
        returns:
            a random grass texture
        '''
        grass_texture = random.choices(
                    [self.grass1,
                     self.grass2,
                     self.grass3,
                     self.flowers1,
                     self.flowers2,
                     self.flowers3],
                    weights = [0.22, 0.22, 0.22,
                               0.11, 0.11, 0.11])[0]

        return grass_texture

    def get_bank(self):
        '''
        get_bank returns a random banks texture

        param:
            self
        returns:
            a random banks texture
        '''
        bank_texture = random.choices(
            [self.bank1,
             self.bank2,
             self.bank3],
             weights = [1/3, 1/3, 1/3])[0]

        return bank_texture

    def get_trees(self, num_trees, right):
        '''
        get_trees is a helper function which takes a number of trees and randomly picks
        their textures and ensures that bushes don't get cut off
        
        param:
            self
            num_trees - number of trees on the edges of a row
            right - boolean of whether or not the trees are on the right side of 
                the screen
        returns:
            trees - list of the textures
        '''
        trees = []

        bush_start_chance = 0.5
        end_bush_chance = 0.3

        if not right:
            in_bush = random.choice([True, False])
        else:
            in_bush = False

        # For each tree
        for i in range(num_trees):

            # If there is currently no bush
            if not in_bush:

                # Attempt to start bushes
                if (random.random() < bush_start_chance or not
                    (right is False and i == num_trees - 1)):

                    # Bushes right end
                    tree_right_end = random.choices([self.tree1_right_end,
                                         self.tree2_right_end,
                                         self.tree3_right_end],
                                         weights = [1/3, 1/3, 1/3])[0]
                    trees.append(tree_right_end)

                    in_bush = True

                # Otherwise, append a tree with no bush
                else:

                    tree_no_bush = random.choices([self.tree1_no_bush,
                                       self.tree2_no_bush,
                                       self.tree3_no_bush],
                                       weights = [1/3, 1/3, 1/3])[0]
                    trees.append(tree_no_bush)

            # Otherwise
            else:

                # See if we should end the bush
                if (random.random() < end_bush_chance or
                    (right is False and i == num_trees - 1)):

                    # Bushes left end
                    tree_left_end = random.choices([self.tree1_left_end,
                                    self.tree2_left_end,
                                    self.tree3_left_end],
                                    weights = [1/3, 1/3, 1/3])[0]
                    trees.append(tree_left_end)

                    in_bush = False

                # Otherwise, continue bushes
                else:

                    tree = random.choices([self.tree1,
                               self.tree2,
                               self.tree3],
                               weights = [1/3, 1/3, 1/3])[0]
                    trees.append(tree)

        return trees

    def get_log(self, length):
        '''
        get_log is a helper function which takes a length of the log picks the correct
        textures so each tile is correctly connected
        
        param:
            self
            length - length of the log
        returns:
            logs - list of the textures
        '''
        logs = []

        # For each cell
        for i in range(length):

            if i == 0:

                logs.append(self.logs[0])

            elif i == length - 1:

                logs.append(self.logs[2])

            else:

                logs.append(self.logs[1])

        return logs

    def draw_all_backgrounds(self):
        '''
        draw_all_backgrounds is a helper function that draws all
        currently background rows of the world engine

        param:
            self
        returns:
            nothing
        '''
        for index in reversed(self.world.loaded_indices):

            self.world.backgrounds[index - self.world.loaded_indices[0]].draw()

    def draw_all_obstacle(self):
        '''
        draw_all_rows is a helper function that draws all
        currently loaded rows of the world engine

        param:
            self
        returns:
            nothing
        '''
        for index in reversed(self.world.loaded_indices):

            if (self.world.rows[index][0] == 'Forest' or
                self.world.rows[index][0] == 'Road' or
                self.world.rows[index][0] == 'Bank' or
                self.world.rows[index][0] == 'Victory' or
                self.world.rows[index][0] == 'Hostile'):

                self.world.obstacles[index - self.world.loaded_indices[0]].draw()

    def draw_all_rivers(self):
        '''
        draw_all_rows is a helper function that draws all
        currently loaded rows of the world engine

        param:
            self
        returns:
            nothing
        '''
        for index in reversed(self.world.loaded_indices):

            if (self.world.rows[index][0] == 'River_Lilypads' or
                self.world.rows[index][0] == 'River_Logs'):

                self.world.obstacles[index - self.world.loaded_indices[0]].draw()

    def draw_all_platforms(self):
        '''
        draw_all_platforms is a helper function that
        draws all currently loaded rows of platforms 
        in the world engine

        param:
            self
        returns:
            nothing
        '''
        for row in reversed(self.world.platforms):

            # For logs
            if isinstance(row, list):

                row[0].draw()

            # For lilypads
            else:

                row.draw()

    def draw_all_collectibles(self):
        '''
        draw_all_collectibles is a helper function that
        draws all currently loaded rows of collectibles 
        in the world engine

        param:
            self
        returns:
            nothing
        '''
        for collectibles in reversed(self.world.collectibles):

            collectibles.draw()

    def draw_all_sprites(self):
        '''
        draw_all_sprites draws the currently loaded
        world

        param:
            self
        returns:
            nothing
        '''

        self.draw_all_backgrounds()
        self.draw_all_rivers()
        self.draw_all_platforms()
        self.player.draw()
        self.draw_all_collectibles()
        self.draw_all_obstacle()
