'''This module loads and manages textures'''
import random
import arcade

from scripts import constants as c

class TextureEngine():
    '''
    The TextureEngine manages textures, loads them, and
    draws every frame
    '''

    def __init__(self):
        '''
        Constructor

        param:
            self
            world - a world engine
            player - a player
        '''
        
        ## SPRITES
        # Bear
        self.bear = "sprites/bear_rev2.png"
        # Deaths
        drowning_sheet = arcade.load_spritesheet("sprites/bear_death2_sheet.png")
        self.drowning = drowning_sheet.get_texture_grid(size = (30, 30), columns=9, count=9)

        self.mauled = arcade.load_texture("sprites/bear_death1.png")

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

        # Create the grid
        self.grid = self.create_grid()

    def add_player(self, player):

        self.player = arcade.SpriteList()
        self.player.append(player)

    def add_world(self, world):

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
                cell.center_x = c.TILE_WIDTH * column + c.TILE_WIDTH // 2
                cell.center_y = c.TILE_HEIGHT * row + c.TILE_HEIGHT // 2

                # Append to list of all grid sprites to draw
                grid.append(cell)

        return grid
    
    def get_trees(self, num_trees, right):

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
                    (right == False and i == num_trees - 1)):

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
                    (right == False and i == num_trees - 1)):
                    
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

    def draw_all_grassy_and_cars(self):
        '''
        draw_all_rows is a helper function that draws all
        currently loaded rows of the world engine

        param: 
            self
        returns:
            nothing
        '''
        for index in reversed(self.world.loaded_indices):

            if (self.world.rows[index] == 'Grassy' or
                self.world.rows[index] == 'Road' or
                self.world.rows[index] == 'Victory'):

                self.world.loaded[index - self.world.loaded_indices[0]].draw()

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

            if (self.world.rows[index] == 'River_Lilypads' or
                self.world.rows[index] == 'River_Logs'):

                self.world.loaded[index - self.world.loaded_indices[0]].draw()

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

        self.grid.draw()
        self.draw_all_rivers()
        self.draw_all_platforms()
        self.player.draw()
        self.draw_all_collectibles()
        self.draw_all_grassy_and_cars()
