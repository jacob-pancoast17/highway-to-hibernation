import arcade

class Object():
    '''
    Constructor

    param:
        size, the box's length and width
        x, x position on the window
        y, y position on the window
        color, arcade.csscolor color type
        angle, the angle of the box
    returns:
        nothing
    '''
    def __init__(self, size, x, y, color):
        # For now just makes cubes
        # Right now this also ignores the angle parameter
        square = arcade.SpriteSolidColor(
            width = size,
            height = size,
            center_x = x,
            center_y = y,
            color = color,
            angle = 0
        )