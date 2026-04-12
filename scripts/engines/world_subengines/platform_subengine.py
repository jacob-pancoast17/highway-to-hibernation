'''This module is the part of the world engine that generates platforms'''
# Python modules
import random
import arcade

# Constants
from scripts import constants as c

# Path algorithm
from scripts.engines.world_subengines.drunkards_walk import drunkards_walk

# Objects
from scripts.objects.platform_object import Platform

def generate_platforms(texture_engine, platforms, current_walk_coords, biome_info,
                       row, curr_bottom):
    '''
    generate_platform is a helper function that takes a row index 
    and generates platforms based on the biome

    param: 
        texture_engine - where to get textures from
        current_walk_coords - current coordinates of the possible path
        biome - the current biome to generate a row based off
        row - the current row to be generated
        curr_bottom - the current bottom of the screen
    returns:
        a SpriteList object from child function and the new walkable path
    '''

    biome = biome_info[0]


    if biome == 'River_Lilypads':

        return generate_lilypads(texture_engine, current_walk_coords, row, curr_bottom)

    elif biome == 'River_Logs':

        return generate_logs(texture_engine, platforms, current_walk_coords, row,
                             curr_bottom, biome_info[1])

    else:

        return [arcade.SpriteList(), current_walk_coords]

def generate_lilypads(texture_engine, curr_walk_coords, row, curr_bottom):
    """
    generate_lilypads takes a row and lilypads you can use to walk across
    the river. Some are randomly placed, other are placed on the walkable
    path

    param:
        texture_engine - where to get textures from
        curr_walk_coords - current coords of the walkable path
        row - the row index to be drawn at
        curr_bottom - the current bottom of the screen
    returns:
        a spritelist of obstacles and the new walkable path coords
    """

    lilypads = arcade.SpriteList()

    walkable = drunkards_walk(curr_walk_coords[0], row - curr_bottom,
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
                'sprites/lilypad-with-frog.png'],
                weights = [0.9, 0.1])

            for lilypad in lilypads:

                if lilypad.x is not i:

                    lilypads.append(Platform(lilypad_texture[0], i,
                                            row - curr_bottom))

    # Update walk
    current_walk_coords = walkable[-1]

    return [lilypads, current_walk_coords]

def generate_logs(texture_engine, platforms, curr_walk_coords, row, curr_bottom, speed):
    '''
    generate_logs takes a row and generates logs that move across the
    screen

    param:
        texture_engine - where to get textures from
        curr_walk_coords - current coords of the walkable path
        row - the row index to be drawn at
        curr_bottom - the current bottom of the screen
        speed - the row speed
    returns:
        a spritelist of obstacles and the new walkable path coords
    '''

    walkable = drunkards_walk(curr_walk_coords[0], row, 4, c.COLUMN_COUNT - 4)
    walkable = sorted(walkable, key=lambda x: x[1])

    log_cells = arcade.SpriteList()
    moving_left = random.choice([True, False])

    length = random.randint(c.SMALLEST_LOG, c.BIGGEST_LOG)

    for i in range(length):

        if moving_left:

            log_textures = texture_engine.get_log(length)

            log_cells.append(Platform(log_textures[length - 1 - i],
                                15 - i,
                                row = row - curr_bottom,
                                static = False,
                                speed = speed,
                                left = True))

        else:

            log_textures = texture_engine.get_log(length)

            log_cells.append(Platform(log_textures[i],
                                i,
                                row = row - curr_bottom,
                                static = False,
                                speed = speed,
                                left = False))

    # Update walk
    current_walk_coords = walkable[-1]

    return [log_cells, current_walk_coords]
