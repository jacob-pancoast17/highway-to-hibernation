''' Module representing the game over screen. '''
import arcade
from scripts import constants as c
from scripts.stats_manager import record_score
from scripts.screens.leaderboard_screen import LeaderboardScreen


class GameOver(arcade.View):
    ''' GameOver represents the game over view '''

    def __init__(self, score, previous_view):
        '''
        Constructor calls arcade 'View' superclass constructor
        
        param:
            self
        returns:
            nothing
        '''
        super().__init__()
        self.score = score
        self.previous_view = previous_view
        self.player_name = ""
        self.submitted = False
        self.submit_message = ""

    def on_show_view(self):
        '''
        on_show_view defines events that happen when switching to the game over screen
        
        param:
            self
        returns:
            nothing
        '''
        # Set background color
        self.window.background_color = c.game_over_background

        # Reset view
        self.window.default_camera.use()

    def on_draw(self):
        '''
        on_draw redraws the game over screen

        param:
            self
        returns:
            nothing
        '''
        # reset window
        self.clear()

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "YOU ARE DEAD",
            font_name="Edit Undo BRK",
            color= c.blood_mwahaha,
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 3 / 4,
            font_size = 50,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        arcade.draw_text(
            f"SCORE: {self.score}",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 5 / 8,
            font_size = 30,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        arcade.draw_text(
            "Enter your name:",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 0.54,
            font_size = 22,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        arcade.draw_text(
            self.player_name if self.player_name else "_",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 0.48,
            font_size = 24,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "Press ENTER to submit score",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT / 2,
            font_size = 20,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        #TODO: Change to text objects, same in start_screen
        arcade.draw_text(
            "Click to play again",
            font_name="Edit Undo BRK",
            x = c.WINDOW_WIDTH / 2,
            y = (c.WINDOW_HEIGHT / 2)-30,
            font_size = 20,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        arcade.draw_text(
            "Press 'L' for leaderboard",
            font_name="Edit Undo BRK",
            x=c.WINDOW_WIDTH / 2,
            y=(c.WINDOW_HEIGHT / 2) - 60,
            font_size=20,
            anchor_x='center',
            anchor_y='center'
        )

        arcade.draw_text(
            "Press 'Q' to quit",
            font_name="Edit Undo BRK",
            x=c.WINDOW_WIDTH / 2,
            y=(c.WINDOW_HEIGHT / 2) - 90,
            font_size=20,
            anchor_x='center',
            anchor_y='center'
        )

        if self.submit_message:
            arcade.draw_text(
                self.submit_message,
                font_name="Edit Undo BRK",
                x=c.WINDOW_WIDTH / 2,
                y=(c.WINDOW_HEIGHT / 2) - 130,
                font_size=18,
                anchor_x='center',
                anchor_y='center'
            )

    def submit_score(self):
        '''
        submit_score uploads the player's score to firebase
        
        param:
            self
        returns:
            nothing
        '''
        if self.submitted:
            self.submit_message = "Score already submitted!"
            return

        name = self.player_name.strip()
        if not name:
            name = "Player"

        success = record_score(name, self.score)

        if success:
            self.submitted = True
            self.submit_message = "Score submitted!"
        else:
            self.submit_message = "Could not submit score."

    # on_mouse_press detects when the mouse is pressed and
    # changes the view to the game view again to restart

    # param: self
     #      _x - cursor x pos
     #      _y - cursor y pos
     #     _button - button on mouse pressed
     #     _modifiers - shift, ctrl, numlock, etc.
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(self.previous_view.__class__())


    # on_key_press detects when the E key is pressed
    # and closes the game window

    # param: self
     #      symbol - key pressed
     #      modifiers - e.g. capslock or numlock

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            self.window.close()
        elif symbol == arcade.key.L:
            self.window.show_view(LeaderboardScreen(self))
        elif symbol == arcade.key.ENTER:
            self.submit_score()
        elif symbol == arcade.key.BACKSPACE:
            self.player_name = self.player_name[:-1]
        elif symbol == arcade.key.SPACE:
            if len(self.player_name) < 12:
                self.player_name += " "
        else:
            if len(self.player_name) < 12 and 32 <= symbol <= 126:
                self.player_name += chr(symbol)