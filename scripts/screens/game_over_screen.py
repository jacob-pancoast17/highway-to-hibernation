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
        self.submit_message_timer = 0


        self.initialize()

    def initialize(self):
        '''
        initialize is part of the game over screen's constructor, but has a special property.
        initialize only sets logic that is dependent on the size of the screen, which must
        be updated every time the user changes the resolution in settings.

        param:
            self
        returns:
            nothing
        '''
        self.game_over_text = arcade.Text(
            "YOU ARE DEAD",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.72,
            color=c.blood_mwahaha,
            font_size=50 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.score_text = arcade.Text(
            f"SCORE: {self.score}",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.58,
            font_size=30 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.play_again_text = arcade.Text(
            "Click to play again",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.38,
            font_size=20 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.leaderboard_text = arcade.Text(
            "Press 'L' for leaderboard",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.28,
            font_size=20 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.name_label_text = arcade.Text(
            "ENTER YOUR INITIALS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.46,
            font_size=22 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.name_text = arcade.Text(
            "_ _ _",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.38,
            font_size=28 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.submit_text = arcade.Text(
            "Press ENTER to submit",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.30,
            font_size=18 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.main_text = arcade.Text(
            "Press 'M' to go to main menu",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.18,
            font_size=20 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x='center',
            anchor_y='center'
        )

        self.submit_message_text = arcade.Text(
            "",
            x=c.WINDOW_WIDTH / 2,
            y = c.WINDOW_HEIGHT * 0.05,
            font_size = 16 * c.RESOLUTION_RATIO,
            font_name = "Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )





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

        self.game_over_text.draw()
        self.score_text.draw()

        if not self.submitted:
            self.name_label_text.draw()
            self.name_text.draw()
            self.submit_text.draw()
        else:
            self.play_again_text.draw()
            self.leaderboard_text.draw()
            self.main_text.draw()

        self.submit_message_text.draw()


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
            self.submit_message_text.text = self.submit_message
            return

        name = self.player_name.strip()
        if not name:
            name = "BOT"

        success = record_score(name, self.score)

        if success:
            self.submitted = True
            self.submit_message = "Score submitted!"
        else:
            self.submit_message = "Could not submit score."

        self.submit_message_text.text = self.submit_message
        self.submit_message_timer = 4.5

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        '''
        on_mouse_press detects when the mouse is pressed and
        changes the view to the game view again to restart

        param: self
            _x - cursor x pos
            _y - cursor y pos
            _button - button on mouse pressed
            _modifiers - shift, ctrl, numlock, etc.
        '''
        self.window.show_view(self.previous_view.__class__())


    def on_update(self, delta_time):
        if self.submit_message_timer > 0:
            self.submit_message_timer -= delta_time
            if self.submit_message_timer <= 0:
                self.submit_message = ""
                self.submit_message_text.text = ""
                self.submit_message_timer = 0

    def on_key_press(self, symbol, modifiers):
        '''
        on_key_press detects when the E key is pressed
        and closes the game window

        param: self
            symbol - key pressed
            modifiers - e.g. capslock or numlock
        '''
        if not self.submitted:
        
            if symbol == arcade.key.ENTER:
                    self.submit_score()
            elif symbol == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
                self.name_text.text = self.player_name if self.player_name else "_ _ _"
            else:
                if len(self.player_name) < 3 and 97 <= symbol <= 122:
                    self.player_name += chr(symbol).upper()
                    self.name_text.text = " ".join(self.player_name)
                elif len(self.player_name) < 3 and 65 <= symbol <= 90:
                    self.player_name += chr(symbol)
                    self.name_text.text = " ".join(self.player_name)

        else:
            if symbol == arcade.key.M:
                from scripts.screens.start_screen import StartScreen
                self.window.show_view(StartScreen())
            elif symbol == arcade.key.L:
                self.window.show_view(LeaderboardScreen(self))
