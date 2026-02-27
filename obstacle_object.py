from object import Object

class ObstacleObject(Object):
    '''
    Constructor creates a obstacle object which "is-an" object

    param: 
        same as object parameters
    returns:
        nothing
    '''
    def __init__ (self, size, x, y, color):
        super().__init__(size, x, y, color)
    