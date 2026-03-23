'''This module loads and manages textures'''
import random
import arcade

import constants as c

class TextureEngine():
    '''
    The TextureEngine manages textures, loads them, and
    draws every frame
    '''

    def __init__(self, world, player):
        '''
        Constructor

        param:
            self
            world - a world engine
            player - a player
        '''

        self.world = world
        self.player = arcade.SpriteList()
        self.player.append(player)

        # Create the grid
        self.grid = self.create_grid()

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
                cell.center_x = (c.MARGIN + c.TILE_WIDTH) * column + c.MARGIN + c.TILE_WIDTH // 2
                cell.center_y = (c.MARGIN + c.TILE_HEIGHT) * row + c.MARGIN + c.TILE_HEIGHT // 2

                # Append to list of all grid sprites to draw
                grid.append(cell)

        return grid

    def draw_all_rows(self):
        '''
        draw_all_rows is a helper function that draws all
        currently loaded rows of the world engine

        param: 
            self
        returns:
            nothing
        '''

        for i in range(len(self.world.loaded)):

            self.world.loaded[i].draw()

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

        for i in range(len(self.world.platforms)):

            self.world.platforms[i].draw()

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
        self.draw_all_rows()
        self.draw_all_platforms()
        self.player.draw()
