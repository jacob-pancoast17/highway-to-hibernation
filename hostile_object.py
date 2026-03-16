''' Module representing hostile objects - both passive and aggressive. '''
import arcade
import constants as c
from game_over_screen import GameOver
from object import Object

class Hostile(Object):
    '''
    Constructor creates a hostile object which "is-an" object

    param: 
        same as object parameters
    returns:
        nothing
    '''
    # pylint throws an error here but im going to keep it for now i dont break anything
    def __init__(self, size, x, y, color):
        super().__init__(size, x, y, color)


    '''
    Try move to test if the hostile collides with the player.
    If it does, return true to end the game. If not, return false to move the hostile.

    param:
        self: the hostile object
        window: the current game view window, used to end the game if there is a collision
        player: the player object, used to test for collision
    returns:
        true if there is a collision, false if not
    '''
    def try_move(self, window, player):
        if self.obj.center_y < 0:
            temp = self.obj.center_y
            self.obj.center_y = c.WINDOW_HEIGHT - (c.TILE_HEIGHT / 2) - 5
            hit = arcade.check_for_collision(self.to_sprite(), player)
            self.obj.center_y = temp
            if hit:
                window.show_view(GameOver())
                return True
        else:
            self.obj.center_y -= c.VELOCITY_MULTIPLIER
            hit = arcade.check_for_collision(self.to_sprite(), player)
            self.obj.center_y += c.VELOCITY_MULTIPLIER
            if hit:
                window.show_view(GameOver())
                return True
        return False


    '''
    Move the hostile down the screen. If it goes off the screen, move it back to the top.
    '''
    def move(self):
        if self.obj.center_y < 0:
            self.obj.center_y = c.WINDOW_HEIGHT - (c.TILE_HEIGHT / 2) - 5
        else:
            self.obj.center_y -= c.VELOCITY_MULTIPLIER
