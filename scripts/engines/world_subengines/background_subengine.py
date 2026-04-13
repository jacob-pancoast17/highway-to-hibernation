'''This module is the part of the world engine that generates backgrounds'''
import arcade
from scripts import constants as c

def generate_background(texture_engine, biome, row, curr_bottom):
    '''
    generate_background is a helper function that takes a row index 
    and generates that row of backgrounds by calling a child generate 
    function based on what type of row it should be, assigned by the
    WorldGen's "rows" varaiable

    param: 
        texture_engine - where to get textures from
        biome - the current biome to generate a row based off
        row - the current row to be generated
        curr_bottom - the current bottom of the screen
    returns:
        a SpriteList object from child function
    '''

    biome = biome[0]

    if biome == "Hostile":

        return generate_grass(texture_engine, row, curr_bottom)

    elif biome == "Forest":

        return generate_grass(texture_engine, row, curr_bottom)

    # Rivers don't need a background
    elif biome == "River_Lilypads" or biome =="River_Logs":

        return arcade.SpriteList()

    elif biome == "Bank":

        return generate_bank(texture_engine, row, curr_bottom)

    elif biome == "Victory":

        return generate_grass(texture_engine, row, curr_bottom)

    else:

        print("PROBLEM IN GENERATION.")
        exit()

def generate_grass(texture_engine, row, curr_bottom):
    '''
    generate_grass takes a row and generates the grass background
    for it

    param:
        texture_engine - where to get textures from
        row - the row index to be drawn at
        curr_bottom - the current bottom of the screen
    returns:
        a spritelist of grass objects
    '''

    grass = arcade.SpriteList()

    for i in range(c.COLUMN_COUNT):

        grass_texture = texture_engine.get_grass()

        cell = arcade.Sprite(grass_texture)

        # Set the cell's center based on grid position
        cell.center_x = c.TILE_SIZE * i + c.TILE_SIZE // 2
        cell.center_y = c.TILE_SIZE * (row - curr_bottom) + c.TILE_SIZE // 2

        cell.scale = c.RESOLUTION_RATIO

        grass.append(cell)

    return grass

def generate_bank(texture_engine, row, curr_bottom):
    '''
    generate_bank takes a row and generates the bank background
    for it

    param:
        texture_engine - where to get textures from
        row - the row index to be drawn at
        curr_bottom - the current bottom of the screen
    returns:
        a spritelist of bank objects
    '''

    bank = arcade.SpriteList()

    for i in range(c.COLUMN_COUNT):

        bank_texture = texture_engine.get_bank()

        cell = arcade.Sprite(bank_texture)

        # Set the cell's center based on grid position
        cell.center_x = c.TILE_SIZE * i + c.TILE_SIZE // 2
        cell.center_y = c.TILE_SIZE * (row - curr_bottom) + c.TILE_SIZE // 2

        cell.scale = c.RESOLUTION_RATIO

        bank.append(cell)

    return bank
