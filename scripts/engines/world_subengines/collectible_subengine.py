'''This module is the part of the world engine that generates collectibles'''
# Python modules
import arcade
import random

# Constants
from scripts import constants as c

# Objects
from scripts.objects.obstacle_object import Obstacle

def generate_collectible(texture_engine, obstacles, biome, row, curr_bottom):
        '''
        generate_collectible is a helper function that takes a row index 
        and generates the collectibles in that row by calling a child generate function
        based on what type of collectible it should be

        param: 
            texture_engine - where to get textures from
            biome - current biome to generate collectibles based off
            row - the current row to be generated
            curr_bottom - the current bottom of the screen
        returns:
            a SpriteList object from child function
        '''
        if biome == 'Forest':

            return generate_honey(texture_engine, obstacles, row, curr_bottom)

        else:

            return arcade.SpriteList()
        
def generate_honey(texture_engine, obstacles, row, curr_bottom):
    """
    generate_honey takes a row and generates it randomly
    to spawn honey that gives you points if you get it

    param:
        texture_engine - where to get the hunny texture from
        row - a row index to be generated
        curr_bottom - the current bottom of the screen
    returns:
        a SpriteList object containing all of the hunny sprites
    """

    hunny = arcade.SpriteList()

    # Will honey spawn in this row?
    if random.random() < .25:

        spawnable_spots = list(range(c.COLUMN_COUNT))
        cells = obstacles[row - curr_bottom]

        # Remove not spawnable spots
        for cell in cells:

            spawnable_spots.remove(cell.x)

        # Pick a random one and put it there
        x = random.choices(spawnable_spots)

        hun = Obstacle(texture_engine.hunny,
                                        x[0],
                                        row - curr_bottom,
                                        True)
        hunny.append(hun)

        return hunny

    # If no honey spawn, just return a blank list
    else:

        return arcade.SpriteList()