from object import Object

class HostileObject(Object):
    '''
    Constructor creates a hostile object which "is-an" object

    param: 
        same as object parameters
    returns:
        nothing
    '''
    def __init__(self, size, x, y, color):
        super().__init__(size, x, y, color)
