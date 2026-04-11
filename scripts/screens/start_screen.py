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

        self.options = ['Mode', 'Play']
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
        arcade.draw_text(
            "SELECT MODE:",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * .57,
            font_name="Edit Undo BRK",
            font_size=40 * c.RESOLUTION_RATIO,
            anchor_x="center"
        )

         # draw stats window
        arcade.draw_text(
            "<          >",
            x=self.options_coords[0],
            y=self.options_coords[1],
            font_name="Edit Undo BRK",
            font_size=30 * c.RESOLUTION_RATIO,
            anchor_x="center",
            anchor_y="center"
        )


        # draw stats window
        arcade.draw_text(
            "Press L for leaderboard",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 3.4,
            font_name="Edit Undo BRK",
            font_size=18 * c.RESOLUTION_RATIO,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press 'S' for personal stats",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 4.5,
            font_name="Edit Undo BRK",
            font_size=18 * c.RESOLUTION_RATIO,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press 'Q' to Quit",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 6.5,
            font_name="Edit Undo BRK",
            font_size=18 * c.RESOLUTION_RATIO,
            anchor_x="center"
        )

        # draw "buttons"
        self.draw_mode()
        self.draw_play()

    def on_update(self, delta_time):
        '''
        Happens every frame
        '''

        self.time_elapsed += delta_time

        if self.time_elapsed > self.next_blink:

            self.next_blink += c.BLINK_RATE

            self.blink()

    def on_key_press(self, symbol, modifiers):

        # Move up
        if (symbol == arcade.key.LEFT):

            if self.currently_selected_option == 'Mode':

                # Get curr index
                curr_index = self.modes.index(self.currently_selected_mode)

                if curr_index - 1 == -1:
                    
                    curr_index = len(self.modes)
                    self.currently_selected_mode = self.modes[curr_index - 1]

                else:

                    self.currently_selected_mode = self.modes[curr_index - 1]

        # Move down
        elif (symbol == arcade.key.RIGHT):

            if self.currently_selected_option == 'Mode':

                # Get curr index
                curr_index = self.modes.index(self.currently_selected_mode)

                if curr_index + 1 == len(self.modes):

                    curr_index = -1
                    self.currently_selected_mode = self.modes[curr_index + 1]

                else:

                    self.currently_selected_mode = self.modes[curr_index + 1]
        
        elif (symbol == arcade.key.DOWN):

            index = self.options.index(self.currently_selected_option)

            if index != len(self.options) - 1:

                self.currently_selected_option = self.options[index + 1]

        elif (symbol == arcade.key.UP):

            index = self.options.index(self.currently_selected_option)

            if index != 0:

                self.currently_selected_option = self.options[index - 1]

        # Open stats page
        elif symbol == arcade.key.L:
            self.window.show_view(LeaderboardScreen(self))
        elif symbol == arcade.key.S:
            from scripts.screens.stats_screen import StatsScreen
            self.window.show_view(StatsScreen())
        elif symbol == arcade.key.Q:
            self.window.close()
        elif symbol == arcade.key.F:
            self.window.show_view(Settings(self))

        elif symbol == arcade.key.ENTER and self.currently_selected_option == 'Play':
            if self.currently_selected_mode == "Hundred":
                c.LEVEL_SIZE = 100
                c.CURRENT_MODE = 'Hundred'
            elif self.currently_selected_mode == "Fifty":
                c.LEVEL_SIZE = 50
                c.CURRENT_MODE = 'Fifty'
            elif self.currently_selected_mode == "Thirty":
                c.LEVEL_SIZE = 30
                c.CURRENT_MODE = 'Thirty'
            else:
                c.LEVEL_SIZE = 10000
                c.CURRENT_MODE = 'Infinite'
            game_view = GameView()
            self.window.show_view(game_view)

    def draw_mode(self):
        '''
        draw_infinity is a helper function which draws the infinite levels button

        param:
            self
        returns:
            nothing
        '''

        if (self.blinked and self.currently_selected_option == 'Mode'):

            if (self.currently_selected_mode == 'Infinite'):

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
                    "PLAY! ➜]",
                    x=self.options_coords[0],
                    y=self.options_coords[1] - (60 * c.RESOLUTION_RATIO),
                    font_name="Edit Undo BRK",
                    font_size=60 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color=arcade.csscolor.WHITE)
        
        play.draw()

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


