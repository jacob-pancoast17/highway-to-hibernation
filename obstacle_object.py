''' Module representing obstacle objects in the game. '''
from object import Object

class Obstacle(Object):
    '''
    Constructor creates a obstacle object which "is-an" object

    param: 
        same as object parameters
    returns:
        nothing
    '''
    def __init__ (self, size, x, y, color):
        super().__init__(size, x, y, color)
