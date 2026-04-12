''' Module representing the start screen. '''
import arcade
import arcade.gui
from scripts import constants as c
from scripts.game_view import GameView
from scripts.screens.leaderboard_screen import LeaderboardScreen
from scripts.screens.stats_screen import StatsScreen
from scripts.screens.settings_screen import Settings


class StartScreen(arcade.View):
    '''
    StartScreen represents the start screen view
    '''

    def __init__(self):
        '''
        Constructor calls arcade 'View' superclass constructor

        param:
            self
        returns:
            nothing
        '''
        super().__init__()

        # Enable GUI manager
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        self.currently_selected_option = None
        self.currently_selected_mode = None

        self.blinked = None

        self.initialize()

    def initialize(self):
        '''
        initialize is part of the start screen's constructor, but has a special property.
        initialize only sets logic that is dependent on the size of the screen, which must
        be updated every time the user changes the resolution in settings.

        param:
            self
        returns:
            nothing
        '''

        # Load title
        self.sprites = arcade.SpriteList()
        title = arcade.Sprite("sprites/title.png")
        title.center_x = c.WINDOW_WIDTH / 2
        title.center_y = c.WINDOW_HEIGHT * .8
        title.scale = 0.85 * c.RESOLUTION_RATIO
        self.sprites.append(title)

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.options = ['Mode',
                        'Play',
                        'Stats',
                        'Settings',
                        'Leaderboard', 
                        'Quit']
        self.modes = ['Thirty', 'Fifty', 'Hundred', 'Infinite']

        self.num_options = len(self.modes)
        self.currently_selected_option = self.options[0]
        self.currently_selected_mode = c.CURRENT_MODE
        self.options_coords = [c.WINDOW_WIDTH / 2, c.WINDOW_HEIGHT * 0.50]

        self.stats_text = arcade.Text(
            "Press 'S' for stats",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 8,
            font_size = 17 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )

    def on_show_view(self):
        '''
        on_show_view defines events that happen when switching to the start screen view

        param:
            self
        returns:
            nothing
        '''
        # Set background color
        # self.window.background_color == c.start_screen_background

        # Reset view
        self.window.default_camera.use()
        self.uimanager.enable()

    def on_hide_view(self):
        '''
        on_hide_view defines events that happen when switching
        away from the start screen

        param:
            self
        returns:
            nothing
        '''
        self.uimanager.disable()

    def on_draw(self):
        '''
        on_draw redraws the frame for the start screen

        param:
            self
        returns:
            nothing
        '''
        # Reset window
        self.clear()

        # Draw UI elements
        self.sprites.draw()
        self.uimanager.draw()

        # draw stats window
        select = arcade.Text(
            "SELECT MODE:",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * .57,
            font_name="Edit Undo BRK",
            font_size=40 * c.RESOLUTION_RATIO,
            anchor_x="center"
        )

        select.draw()

        # draw "buttons"
        self.draw_mode()
        self.draw_play()
        self.draw_stats()
        self.draw_leaderboard()
        self.draw_settings()
        self.draw_quit()

    def on_update(self, delta_time):
        '''
        Happens every frame

        param:
            self
            delta_time - time passed since last on_update
        return:
            nothing
        '''

        self.time_elapsed += delta_time

        if self.time_elapsed > self.next_blink:

            self.next_blink += c.BLINK_RATE

            self.blink()

    def on_key_press(self, symbol, modifiers):
        '''
        defines key presses

        param:
            self
            symbol - the key
            modifiers - any modifiers (e.g. capslock)
        return:
            nothing
        '''

        # Move up
        if (symbol == arcade.key.LEFT or symbol == arcade.key.A):

            if self.currently_selected_option == 'Mode':

                # Get curr index
                curr_index = self.modes.index(self.currently_selected_mode)

                if curr_index - 1 == -1:

                    curr_index = len(self.modes)
                    self.currently_selected_mode = self.modes[curr_index - 1]

                else:

                    self.currently_selected_mode = self.modes[curr_index - 1]

            elif self.currently_selected_option == 'Settings':

                self.currently_selected_option = 'Stats'

            elif self.currently_selected_option == 'Quit':

                self.currently_selected_option = 'Leaderboard'

        # Move down
        elif (symbol == arcade.key.RIGHT or symbol == arcade.key.D):

            if self.currently_selected_option == 'Mode':

                # Get curr index
                curr_index = self.modes.index(self.currently_selected_mode)

                if curr_index + 1 == len(self.modes):

                    curr_index = -1
                    self.currently_selected_mode = self.modes[curr_index + 1]

                else:

                    self.currently_selected_mode = self.modes[curr_index + 1]

            elif self.currently_selected_option == 'Stats':

                self.currently_selected_option = 'Settings'

            elif self.currently_selected_option == 'Leaderboard':

                self.currently_selected_option = 'Quit'

        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:

            if self.currently_selected_option == 'Mode':

                self.currently_selected_option = 'Play'

            elif self.currently_selected_option == 'Play':

                self.currently_selected_option = 'Stats'

            elif self.currently_selected_option == 'Stats':

                self.currently_selected_option = 'Leaderboard'

            elif self.currently_selected_option == 'Settings':

                self.currently_selected_option = 'Quit'

        elif (symbol == arcade.key.UP or symbol == arcade.key.W):

            if self.currently_selected_option == 'Play':

                self.currently_selected_option = 'Mode'

            elif self.currently_selected_option  == 'Stats':

                self.currently_selected_option = 'Play'

            elif self.currently_selected_option  == 'Settings':

                self.currently_selected_option = 'Play'

            elif self.currently_selected_option == 'Leaderboard':

                self.currently_selected_option = 'Stats'

            elif self.currently_selected_option == 'Quit':

                self.currently_selected_option = 'Settings'

        elif symbol == arcade.key.ENTER:

            if self.currently_selected_option == 'Play':

                c.CURRENT_OPTION = 'Play'

                if self.currently_selected_mode == "Hundred":
                    c.LEVEL_SIZE = 100
                    c.ENDING_X = 7
                    c.ENDING_Y = 99
                    c.CURRENT_MODE = 'Hundred'

                elif self.currently_selected_mode == "Fifty":
                    c.LEVEL_SIZE = 50
                    c.ENDING_X = 7
                    c.ENDING_Y = 49
                    c.CURRENT_MODE = 'Fifty'

                elif self.currently_selected_mode == "Thirty":
                    c.LEVEL_SIZE = 30
                    c.ENDING_X = 7
                    c.ENDING_Y = 29
                    c.CURRENT_MODE = 'Thirty'

                else:
                    c.LEVEL_SIZE = 10000
                    c.ENDING_X = 7
                    c.ENDING_Y = 9999
                    c.CURRENT_MODE = 'Infinite'

                game_view = GameView()
                self.window.show_view(game_view)

            elif self.currently_selected_option == 'Stats':

                c.CURRENT_OPTION = 'Stats'
                self.window.show_view(StatsScreen(self))

            elif self.currently_selected_option == 'Leaderboard':

                c.CURRENT_OPTION = 'Leaderboard'
                self.window.show_view(LeaderboardScreen(self))

            elif self.currently_selected_option == 'Settings':

                c.CURRENT_OPTION = 'Settings'
                self.window.show_view(Settings(self))

            elif self.currently_selected_option == 'Quit':

                self.window.close()

    def draw_mode(self):
        '''
        draw_mode draws the mode slider

        param:
            self
        returns:
            nothing
        '''

        if (self.blinked and self.currently_selected_option == 'Mode'):

            if self.currently_selected_mode == 'Infinite':

                mode_blink = arcade.Text(
                    "INFINITE",
                    x=self.options_coords[0],
                    y=self.options_coords[1],
                    font_name="Edit Undo BRK",
                    font_size=30 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.BLACK)

                arcade.draw_rect_filled(
                    arcade.XYWH(self.options_coords[0],
                    self.options_coords[1],
                    mode_blink.content_width + (6 * c.RESOLUTION_RATIO),
                    mode_blink.content_height),
                    arcade.csscolor.WHITE
                )

            elif self.currently_selected_mode == 'Hundred':

                mode_blink = arcade.Text(
                "HUNDRED",
                # Would need to be changed to change order
                x=self.options_coords[0],
                y=self.options_coords[1],
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.BLACK)

                arcade.draw_rect_filled(
                    arcade.XYWH(self.options_coords[0],
                    self.options_coords[1],
                    mode_blink.content_width + (6 * c.RESOLUTION_RATIO),
                    mode_blink.content_height),
                    arcade.csscolor.WHITE
                )

            elif self.currently_selected_mode == 'Fifty':

                mode_blink = arcade.Text(
                "FIFTY",
                # Would need to be changed to change order
                x=self.options_coords[0],
                y=self.options_coords[1],
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.BLACK)

                arcade.draw_rect_filled(
                    arcade.XYWH(self.options_coords[0],
                    self.options_coords[1],
                    mode_blink.content_width + (6 * c.RESOLUTION_RATIO),
                    mode_blink.content_height),
                    arcade.csscolor.WHITE)

            else:

                mode_blink = arcade.Text(
                "THIRTY",
                # Would need to be changed to change order
                x=self.options_coords[0],
                y=self.options_coords[1],
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.BLACK)

            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[0],
                self.options_coords[1],
                mode_blink.content_width + (6 * c.RESOLUTION_RATIO),
                mode_blink.content_height),
                arcade.csscolor.WHITE
            )

            mode_blink.draw()

        else:

            if self.currently_selected_mode == 'Infinite':

                mode = arcade.Text(
                    "INFINITE",
                    x=self.options_coords[0],
                    y=self.options_coords[1],
                    font_name="Edit Undo BRK",
                    font_size=30 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)

            elif self.currently_selected_mode == 'Hundred':

                mode = arcade.Text(
                "HUNDRED",
                # Would need to be changed to change order
                x=self.options_coords[0],
                y=self.options_coords[1],
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

            elif self.currently_selected_mode == 'Fifty':

                mode = arcade.Text(
                "FIFTY",
                x=self.options_coords[0],
                y=self.options_coords[1],
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

            else:

                mode = arcade.Text(
                "THIRTY",
                x=self.options_coords[0],
                y=self.options_coords[1],
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.WHITE)

            mode.draw()

    def draw_play(self):
        '''
        draw_play draws the play button

        param:
            self
        returns:
            nothing
        '''

        if self.blinked and self.currently_selected_option == 'Play':

            play = arcade.Text(
            "PLAY!",
            # Would need to be changed to change order
            x=self.options_coords[0],
            y=self.options_coords[1] - (60 * c.RESOLUTION_RATIO),
            font_name="Edit Undo BRK",
            font_size=60 * c.RESOLUTION_RATIO,
            anchor_x="center",
            anchor_y="center",
            color=arcade.csscolor.BLACK)

            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[0],
                self.options_coords[1] - (60 * c.RESOLUTION_RATIO),
                play.content_width + (6 * c.RESOLUTION_RATIO),
                play.content_height),
                arcade.csscolor.WHITE
            )

        else:

            play = arcade.Text(
                    "PLAY!",
                    x=self.options_coords[0],
                    y=self.options_coords[1] - (60 * c.RESOLUTION_RATIO),
                    font_name="Edit Undo BRK",
                    font_size=60 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color=arcade.csscolor.WHITE)

        play.draw()

    def draw_stats(self):
        '''
        draw_stats draws the stats button

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected_option == 'Stats':
            stats = arcade.Text(
                "Stats",
                x=c.WINDOW_WIDTH / 4,
                y=self.options_coords[1] - (135 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK
            )
            arcade.draw_rect_filled(
                arcade.XYWH(stats.x,
                stats.y,
                stats.content_width + (6 * c.RESOLUTION_RATIO),
                stats.content_height),
                arcade.csscolor.WHITE
            )

        else:
            stats = arcade.Text(
                "Stats",
                x=c.WINDOW_WIDTH / 4,
                y=self.options_coords[1] - (135 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center"
            )

        stats.draw()

    def draw_leaderboard(self):
        '''
        draw_leaderboard draws the leaderboard button

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected_option == 'Leaderboard':

            leaderboard = arcade.Text(
                "Leaderboard",
                x=c.WINDOW_WIDTH / 4,
                y=self.options_coords[1] - (180 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK
            )
            arcade.draw_rect_filled(
                arcade.XYWH(leaderboard.x,
                leaderboard.y,
                leaderboard.content_width + (6 * c.RESOLUTION_RATIO),
                leaderboard.content_height),
                arcade.csscolor.WHITE
            )

        else:
            leaderboard = arcade.Text(
                "Leaderboard",
                x=c.WINDOW_WIDTH / 4,
                y=self.options_coords[1] - (180 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center"
            )

        leaderboard.draw()

    def draw_settings(self):
        '''
        draw_settings draws the settings button

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected_option == 'Settings':

            settings = arcade.Text(
                "Settings",
                x=c.WINDOW_WIDTH * 3 / 4,
                y=self.options_coords[1] - (135 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK
            )
            arcade.draw_rect_filled(
                arcade.XYWH(settings.x,
                settings.y,
                settings.content_width + (6 * c.RESOLUTION_RATIO),
                settings.content_height),
                arcade.csscolor.WHITE
            )

        else:
            settings = arcade.Text(
                "Settings",
                x=c.WINDOW_WIDTH * 3 / 4,
                y=self.options_coords[1] - (135 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center"
            )

        settings.draw()

    def draw_quit(self):
        '''
        draw_quit draws the quit button

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected_option == 'Quit':

            quit_text = arcade.Text(
                "Quit",
                x=c.WINDOW_WIDTH * 3 / 4,
                y=self.options_coords[1] - (180 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK
            )
            arcade.draw_rect_filled(
                arcade.XYWH(quit_text.x,
                quit_text.y,
                quit_text.content_width + (6 * c.RESOLUTION_RATIO),
                quit_text.content_height),
                arcade.csscolor.WHITE
            )

        else:
            quit_text = arcade.Text(
                "Quit",
                x=c.WINDOW_WIDTH * 3 / 4,
                y=self.options_coords[1] - (180 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size= 24 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center"
            )

        quit_text.draw()

    def blink(self):
        '''
        blink takes the variable blinked and changes it on or off depending on what the
        current value is

        param:
            self
        returns:
            nothing
        '''

        if self.blinked is False:

            self.blinked = True

        else:
            self.blinked = False
