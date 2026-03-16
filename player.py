''' Module representing the player and movement'''
import arcade
import constants as c



class Player():
    '''Player class: holds all information about the player, including position and sprite'''
    def __init__(self, row, column):
        # For now just makes cubes
        # Right now this also ignores the angle parameter

        self.obj = arcade.Sprite(
            path_or_texture= "sprites/bear.png",
            scale = 1.25,
            center_x = (c.MARGIN + c.TILE_WIDTH) * row + c.MARGIN + c.TILE_WIDTH // 2,
            center_y = (c.MARGIN + c.TILE_HEIGHT) * column + c.MARGIN + c.TILE_HEIGHT // 2,
            angle = 180.0
        )

        self.curr_x = row
        self.curr_y = column

    def get_curr_x(self):
        '''Returns the player's current x position in the grid'''
        return self.curr_x

    def get_curr_y(self):
        '''Returns the player's current y position in the grid'''
        return self.curr_y

    def try_move(self, key, object_type, objects_sprite_list):
        ''' Checks if player can move in the direction of the key pressed 
            without going out of bounds or colliding with an obstacle or hostile. 
            Returns true if the move is valid, false otherwise.'''
        if key == arcade.key.UP:
            if self.curr_y >= c.ROW_COUNT - 1:
                return False


            elif (object_type == 'Obstacle' or
                  object_type == 'Hostile'):
                self.obj.center_y += c.VELOCITY_MULTIPLIER
                hit_list = arcade.check_for_collision_with_list(
                    self.obj,
                    objects_sprite_list
                )
                self.obj.center_y -= c.VELOCITY_MULTIPLIER
                if hit_list:
                    return False

            print("Good to go!")

            return True

        elif key == arcade.key.DOWN:
            if self.curr_y <= 0:
                return False

            elif (object_type == 'Obstacle' or
                  object_type == 'Hostile'):
                self.obj.center_y -= c.VELOCITY_MULTIPLIER
                hit_list = arcade.check_for_collision_with_list(
                    self.obj,
                    objects_sprite_list
                )
                self.obj.center_y += c.VELOCITY_MULTIPLIER
                if hit_list:
                    return False
            print("Good to go!")

            return True

        elif key == arcade.key.LEFT:
            if self.curr_x <= 0:
                return False

            elif (object_type == 'Obstacle' or
                  object_type == 'Hostile'):
                self.obj.center_x -= c.VELOCITY_MULTIPLIER
                hit_list = arcade.check_for_collision_with_list(
                    self.obj,
                    objects_sprite_list
                )
                self.obj.center_x += c.VELOCITY_MULTIPLIER
                if hit_list:
                    return False
            print("Good to go!")

            return True
        elif key == arcade.key.RIGHT:
            if self.curr_x >= c.COLUMN_COUNT - 1:
                return False
            elif (object_type == 'Obstacle' or
                  object_type == 'Hostile'):
                self.obj.center_x += c.VELOCITY_MULTIPLIER
                hit_list = arcade.check_for_collision_with_list(
                    self.obj,
                    objects_sprite_list
                )
                self.obj.center_x -= c.VELOCITY_MULTIPLIER
                if hit_list:
                    return False
            print("Good to go!")
            return True
    def move(self, key):
        '''Moves the player in the direction of the key pressed, if the move is valid.'''
        if (key == arcade.key.UP and
            self.curr_y < c.ROW_COUNT - 1):
            #print("UP")
            self.obj.center_y += c.VELOCITY_MULTIPLIER
            self.curr_y += 1
            self.obj.change_angle = 180
            self.obj.angle = self.obj.change_angle

        elif (key == arcade.key.DOWN and
              self.curr_y > 0):
            #print("DOWN")
            self.obj.center_y -= c.VELOCITY_MULTIPLIER
            self.curr_y -= 1
            self.obj.change_angle = 0
            self.obj.angle = self.obj.change_angle

        elif (key == arcade.key.LEFT and
              self.curr_x > 0):
            #print("LEFT")
            self.obj.center_x -= c.VELOCITY_MULTIPLIER
            self.curr_x -= 1
            self.obj.change_angle = 90
            self.obj.angle = self.obj.change_angle

        elif (key == arcade.key.RIGHT and
              self.curr_x < c.COLUMN_COUNT - 1):
            #print("RIGHT")
            self.obj.center_x += c.VELOCITY_MULTIPLIER
            self.curr_x += 1
            self.obj.change_angle = 270
            self.obj.angle = self.obj.change_angle

        print(f"[{self.curr_x}, {self.curr_y}]")

    def to_sprite(self):
        ''' Returns the player as a sprite to be drawn '''
        return self.obj
