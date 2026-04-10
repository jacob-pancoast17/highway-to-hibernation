'''This module is the part of the world engine that generates obstacles'''
# Python modules
import arcade
import random

# Constants
from scripts import constants as c

# Path algorithm
from scripts.engines.world_subengines.drunkards_walk import drunkards_walk

# Objects
from scripts.objects.den_object import Den
from scripts.objects.hostile_object import Hostile
from scripts.objects.obstacle_object import Obstacle

def generate_obstacles(texture_engine, current_walk_coords, biome, row, curr_bottom):
    '''
    generate_obstacles is a helper function that takes a row index 
    and generates that row by calling a child generate function
    based on what type of row it should be, assigned by the
    WorldGen's "rows" varaiable

    param: 
        texture_engine - where to get textures from
        current_walk_coords - current coordinates of the possible path
        biome - the current biome to generate a row based off
        row - the current row to be generated
        curr_bottom - the current bottom of the screen
    returns:
        a SpriteList object from child function and the new walkable path
    '''
    if biome == "Pack":

        return generate_wolves(texture_engine, current_walk_coords, row, curr_bottom)

    elif biome == "Forest":

        return generate_forest(texture_engine, current_walk_coords, row, curr_bottom)

    elif (biome == "River_Lilypads" or
            biome =="River_Logs"):

        return generate_river(texture_engine, current_walk_coords, row, curr_bottom)
    
    elif (biome == "Bank"):

        return [arcade.SpriteList(), current_walk_coords]

    elif biome == "Victory":

        return generate_victory(texture_engine, current_walk_coords, row, curr_bottom)

    else:

        print("PROBLEM IN GENERATION DUE TO A BIOME MISMATCH IN obstacle_subengine.py")
        exit()

def generate_wolves(texture_engine, curr_walk_coords, row, curr_bottom):
        '''
        generate_wolves takes a row and generates it randomly based on
        the "wolves" quality -- moving objects across the screen

        param:
            texture_engine - where to get textures from
            curr_walk_coords - current coords of the walkable path
            row - the row index to be drawn at
            curr_bottom - the current bottom of the screen
        returns:`
            a spritelist of obstacles and the new walkable_path
        '''

        walkable = drunkards_walk(curr_walk_coords[0],
                                  curr_walk_coords[1],
                                  4, c.COLUMN_COUNT - 4)
        walkable = sorted(walkable, key=lambda x: x[1])

        hostiles = arcade.SpriteList()

        # For each tile, just generate a hostile object that kills you

        moving_left = random.choice([True, False])
        # Pick a random speed
        speed = random.uniform(c.LOWER_OBSTACLE_SPEED, c.UPPER_OBSTACLE_SPEED)

        if not moving_left:
            hostiles.append(Hostile(texture_engine.wolf[0], 0, row - curr_bottom,
                                    texture_engine, speed, static=False, left=False))
        else:
            hostiles.append(Hostile(texture_engine.wolf[0], 14, row - curr_bottom,
                                    texture_engine, speed, static=False, left=True))
            

        current_walk_coords = walkable[-1]

        return [hostiles, current_walk_coords]

def generate_forest(texture_engine, curr_walk_coords, row, curr_bottom):
    '''
    generate_forest takes a row and generates it randomly based on
    the "Forest" quality -- surrounded by trees, with randomly placed
    rocks

    param:
        texture_engine - where to get textures from
        curr_walk_coords - current coords of the walkable path
        row - the row index to be drawn at
        curr_bottom - the current bottom of the screen
    returns:
        a spritelist of obstacles and the new walkable path coords
    '''

    sprites = arcade.SpriteList()

    # Generate a random number of trees
    num_trees_left = random.randint(1,4)
    num_trees_right = random.randint(1,4)

    walkable = drunkards_walk(curr_walk_coords[0],
                              curr_walk_coords[1],
                              num_trees_left,
                              c.COLUMN_COUNT - num_trees_right)
    
    walkable = sorted(walkable, key=lambda x: x[1])

    last_rock = None

    # Append trees to the left
    tree_textures_left = texture_engine.get_trees(num_trees_left, False)

    for i in range(num_trees_left):

        tree_texture = tree_textures_left[i]

        tree = Obstacle(tree_texture, i, row=row - curr_bottom)

        tree.center_y = (c.TILE_SIZE * (row - curr_bottom)
                                + c.TILE_SIZE)
        
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

                    last_rock = Obstacle(rock_texture[0], x, row - curr_bottom)
                    sprites.append(last_rock)

    # Trees on the right
    tree_textures_right = texture_engine.get_trees(num_trees_right, True)

    for i in range(num_trees_right):
        
        x = c.COLUMN_COUNT - num_trees_right + i

        tree_texture = tree_textures_right[i]

        tree = Obstacle(tree_texture, x, row=row - curr_bottom)

        tree.center_y = (c.TILE_SIZE * (row - curr_bottom)
                                + c.TILE_SIZE)
        
        sprites.append(tree)


    # Update walk
    current_walk_coords = walkable[-1]

    return [sprites, current_walk_coords]

def generate_river(texture_engine, curr_walk_coords, row, curr_bottom):
    '''
    generate_river takes a row and generates it randomly based on
    the "River" quality -- hostile water cells

    param:
        texture_engine - where to get textures from
        curr_walk_coords - current coords of the walkable path
        row - the row index to be drawn at
        curr_bottom - the current bottom of the screen
    returns:
        a spritelist of obstacles and the new walkable path coords
    '''

    river = arcade.SpriteList()

    # Generate the whole river as hostile objects
    for i in range(c.COLUMN_COUNT):

        river.append(
            Hostile("sprites/water.png", i, row - curr_bottom, texture_engine))

    return [river, curr_walk_coords]

def generate_victory(texture_engine, curr_walk_coords, row, curr_bottom):
    '''
    generate_victory takes a row and generates it randomly based on
    the "Victory" quality -- similar to Forest

    param:
        texture_engine - where to get textures from
        curr_walk_coords - current coords of the walkable path
        row - the row index to be drawn at
        curr_bottom - the current bottom of the screen
    returns:
        a spritelist of obstacles and the new walkable path coords
    '''


    sprites = arcade.SpriteList()

    # Generate a random number of trees
    num_trees_left = random.randint(1,4)
    num_trees_right = random.randint(1,4)


    last_rock = None

    # Append trees to the left
    tree_textures_left = texture_engine.get_trees(num_trees_left, False)

    for i in range(num_trees_left):

        tree_texture = tree_textures_left[i]

        sprites.append(
                Obstacle(tree_texture, i, row - curr_bottom))

        sprites[-1].scale = 0.95
        sprites[-1].center_y = (c.TILE_SIZE * (row - curr_bottom)
                                + c.TILE_SIZE * 0.95)

    for i in range(c.COLUMN_COUNT - num_trees_left - num_trees_right):

        x = i + num_trees_left

        # The victory square should not be a rock
        if row == c.ENDING_Y and x == c.ENDING_X:
            den = Den('sprites/den.png', x, row - curr_bottom)
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

                    last_rock = Obstacle(rock_texture[0], x, row - curr_bottom)
                    sprites.append(last_rock)

    # Trees on the right
    tree_textures_right = texture_engine.get_trees(num_trees_right, True)

    for i in range(num_trees_right):

        x = c.COLUMN_COUNT - num_trees_right + i

        tree_texture = tree_textures_right[i]

        sprites.append(
                Obstacle(tree_texture, x, row - curr_bottom))

        sprites[-1].scale = 0.95
        sprites[-1].center_y = (c.TILE_SIZE * (row - curr_bottom)
                                + c.TILE_SIZE * 0.95)

    return [sprites, curr_walk_coords]
