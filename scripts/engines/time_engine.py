'''This module contains the engine that manages timing and spawns'''
import constants as c

class TimeEngine():
    '''
    The TimeEngine class is the engine that manages world time
    and spawning behavior for certain objects including "cars"
    and logs
    '''

    def __init__(self, world, window):
        '''
        Constructor
        Takes a world engine and a window and creates the time
        engine

        param:
            self
            world - a world engine
            window - a game window
        returns:
            nothing
        '''

        self.world_time = 0
        self.world = world
        self.window = window

        # Set the first spawn check
        self.next_spawn_check = c.TIME_BETWEEN_SPAWNS

    def pass_time(self, time):
        '''
        pass_time takes the elapsed time since the last on_update call
        in the game window and adds it to the elapsed time, then checks
        if certain movable objects should spawn

        param:
            self
            time - the elapsed time since the last on_update call
        returns:
            nothing
        '''

        self.world_time += time

        # Try to move hostile objects and attempt to spawn
        # new ones if we are at the next check
        self.try_to_move_hostiles(time)

        if self.world_time > self.next_spawn_check:

            self.spawn_hostiles()

    def try_to_move_hostiles(self, delta_time):
        '''
        try_to_move_hostiles takes the elapsed time and tests if
        we can move hostile objects. If we can, move them

        param:
            self
            delta_time - the time since the last on_update call
        returns:
            nothing
        '''

        # Get the current hostile rows
        curr_car_rows = self.world.get_car_rows()

        # Try to move each car in each row
        for row in curr_car_rows:

            for car in self.world.loaded[row]:

                car.try_move(delta_time, self.window, self.world.player)

    def spawn_hostiles(self):
        '''
        spawn_hostiles tries to spawn hostiles in each row 

        param:
            self
        returns:
            nothing
        '''

        self.next_spawn_check += c.TIME_BETWEEN_SPAWNS

        # Get the current hostile rows
        curr_car_rows = self.world.get_car_rows()

        # Then for each row update the board using the world
        # engine
        for row in curr_car_rows:

            self.world.update_cars(row)
