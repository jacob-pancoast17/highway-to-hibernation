'''This module defines the drunkard's walk algorithm used in world generation to solve
the possible path problem'''

import random

def drunkards_walk(x, y, left_bound, right_bound):
    '''
    drunkards_walk returns the tiles in a given row which need to be empty

    param:
        x - x to start the walk on
        y - y to start the walk on
    returns:
        a list of coordinates in a row that must be empty
    '''
    path = [(x, y)]

    while True:
        a = random.choices(['up', 'left', 'right'],
                        weights = [1/3, 1/3, 1/3])

        if a[0] == 'up':

            y += 1

            path.append((x, y))
            return path

        elif a[0] == 'right' and x < right_bound:

            x += 1

            if (x, y)not in path:

                path.append((x, y))

        elif a[0] == 'left' and x > left_bound:

            x += -1

            if (x, y)not in path:

                path.append((x, y))
