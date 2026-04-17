'''This module contains the engine that manages timing and spawns'''
from scripts import constants as c

from scripts.objects.hostile_object import Hostile

class TimeEngine():
    '''
    The TimeEngine class is the engine that manages world time
    and spawning behavior for certain objects including "wolvess"
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

        self.next_fast_log_spawn_check = c.TIME_BETWEEN_FAST_LOG_SPAWNS
        self.next_med_log_spawn_check = c.TIME_BETWEEN_MED_LOG_SPAWNS
        self.next_slow_log_spawn_check = c.TIME_BETWEEN_SLOW_LOG_SPAWNS

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
        self.try_to_move_log(time)

        if self.world_time > self.next_spawn_check:
            self.spawn_hostiles()
        if self.world_time > self.next_fast_log_spawn_check:
            # Check to see if a fast log row exists and append to list to pass into function
            if len(self.world.fast_log_rows) > 0:
                self.spawn_platforms("FAST", self.world.fast_log_rows)
        if self.world_time > self.next_med_log_spawn_check:
            if len(self.world.med_log_rows) > 0:
                self.spawn_platforms("MED", self.world.med_log_rows)
        if self.world_time > self.next_slow_log_spawn_check:
            if len(self.world.slow_log_rows) > 0:
                self.spawn_platforms("SLOW", self.world.slow_log_rows)

    def try_to_move_log(self, delta_time):
        '''
        try_to_move_log takes the elapsed time and tests if
        we can move log objects. If we can, move them

        param:
            self
            delta_time - the time since the last on_update call
        returns:
            nothing
        '''
        # Get the current log rows
        curr_log_rows = self.world.get_log_rows()

        # Try to move each log in each row
        for row in curr_log_rows:

            for log in self.world.platforms[row - self.world.loaded_indices[0]]:

                log.try_move(delta_time, self.world.player)

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
        curr_wolf_rows = self.world.get_wolf_rows()
        # print(f"curr wolf rows: {curr_wolf_rows}")

        # Try to move each wolf in each row
        for row in curr_wolf_rows:

            for wolf in self.world.obstacles[row - self.world.loaded_indices[0]]:

                if isinstance(wolf, Hostile):

                    wolf.run(delta_time)

                    wolf.try_move(delta_time, self.world.player)

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
        curr_wolf_rows = self.world.get_wolf_rows()

        # Then for each row update the board using the world
        # engine
        for row in curr_wolf_rows:

            self.world.update_wolves(row)


    def spawn_platforms(self, row_speed, curr_rows):
        '''
        spawn_platforms tries to spawn platforms in each row 

        param:
            self
        returns:
            nothing
        '''

        # Add TIME_BETWEEN_LOG_SPAWNS to log spawns
        if row_speed == "FAST":
            self.next_fast_log_spawn_check = self.world_time + c.TIME_BETWEEN_FAST_LOG_SPAWNS
        elif row_speed == "MED":
            self.next_med_log_spawn_check = self.world_time + c.TIME_BETWEEN_MED_LOG_SPAWNS
        elif row_speed == "SLOW":
            self.next_slow_log_spawn_check = self.world_time + c.TIME_BETWEEN_SLOW_LOG_SPAWNS
        else:
            print("UNKNOWN SPEED ERROR IN time_engine.py")
            return
        # print(self.next_log_spawn_check)

        # Then for each row passed in, update the board using the world
        # engine
        for row in curr_rows:
            self.world.update_logs(row)
