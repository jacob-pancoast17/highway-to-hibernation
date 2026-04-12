''' Module representing the pause screen. '''
import arcade
from scripts import constants as c
from scripts.screens.settings_screen import Settings
from scripts.screens.leaderboard_screen import LeaderboardScreen

class Pause(arcade.View):
    '''
    Constructor calls arcade 'View' superclass constructor

    param:
        self
    returns:
        nothing
    '''
    def __init__(self, game_view):

        super().__init__()

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.title_coords = [c.WINDOW_WIDTH / 2, c.WINDOW_HEIGHT * 3 / 4]

        self.options = ['Reset', 'Leaderboard', 'Settings', 'Main Menu']
        self.currently_selected = self.options[0]
        
        self.game_view = game_view
        self.initialize()

    def initialize(self):
        '''
        initialize is part of the pause screen's constructor, but has a special property.
        initialize only sets logic that is dependent on the size of the screen, which must
        be updated every time the user changes the resolution in settings.

        param:
            self
        returns:
            nothing
        '''
        self.pause_spr = arcade.Sprite(
            path_or_texture= "sprites/pause_graphic.png",
            scale = 1.25 * c.RESOLUTION_RATIO,
            center_x = c.WINDOW_WIDTH / 2,
            center_y = c.WINDOW_HEIGHT / 2,
            angle = 180.0
        )
        self.sprites = arcade.SpriteList()
        self.sprites.append(self.pause_spr)

        self.pause_text = arcade.Text(
            "PAUSE",
            x = self.title_coords[0],
            y = self.title_coords[1],
            font_size = 50 * c.RESOLUTION_RATIO,
            font_name="Edit Undo BRK",
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.continue_text = arcade.Text(
            "Press 'ESC' to continue",
            x = c.WINDOW_WIDTH / 2,
            y = 0 + 60 * c.RESOLUTION_RATIO,
            font_size = 18,
            font_name="Edit Undo BRK",
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
        # Reset view
        self.window.default_camera.use()


    def on_draw(self):
        '''
        on_draw redraws the pause screen

        param:
            self
        returns:
            nothing
        '''
        self.clear()
        self.sprites.draw()

        pause = arcade.Text(
            "PAUSE",
            font_name="Edit Undo BRK",
            x = self.title_coords[0],
            y = self.title_coords[1],
            font_size = 50,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        pause.draw()

        self.draw_reset()
        self.draw_leaderboard()
        self.draw_main_menu()
        self.draw_settings()

        self.continue_text.draw()

    def on_key_press(self, symbol, modifiers):

        index = self.options.index(self.currently_selected)

        if symbol == arcade.key.ESCAPE:

            self.window.show_view(self.game_view)
            self.game_view.initialize()

        if symbol == arcade.key.ENTER:

            if self.currently_selected == 'Main Menu':

                from scripts.screens.start_screen import StartScreen
                self.window.show_view(StartScreen())
            
            elif self.currently_selected == 'Reset':
                
                self.window.show_view(self.game_view.__class__())
            
            elif self.currently_selected == 'Leaderboard':

                self.window.show_view(LeaderboardScreen(self))

            elif self.currently_selected == 'Settings':

                self.window.show_view(Settings(self, True))

        elif symbol == arcade.key.UP and index != 0:
    
            self.currently_selected = self.options[index - 1]
        
        elif symbol == arcade.key.DOWN and index != len(self.options) - 1:
        
            self.currently_selected = self.options[index + 1]

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

    def draw_reset(self):
        '''
        draw_reset draws the reset button

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected == 'Reset':

            reset = arcade.Text(
                "Reset",
                x=self.title_coords[0],
                y=self.title_coords[1] - (60 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK
            )
            arcade.draw_rect_filled(
                arcade.XYWH(reset.x,
                reset.y,
                reset.content_width + (6 * c.RESOLUTION_RATIO),
                reset.content_height),
                arcade.csscolor.WHITE
            )

        else:
            reset = arcade.Text(
                "Reset",
                x=self.title_coords[0],
                y=self.title_coords[1] - (60 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center"
            )

        reset.draw()

    def draw_leaderboard(self):
        '''
        draw_leaderboard draws the leaderboard button

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected == 'Leaderboard':
            leaderboard = arcade.Text(
                "leaderboard",
                x=self.title_coords[0],
                y=self.title_coords[1] - (100 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
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
                "leaderboard",
                x=self.title_coords[0],
                y=self.title_coords[1] - (100 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
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
        if self.blinked and self.currently_selected == 'Settings':

            settings = arcade.Text(
                "Settings",
                x=self.title_coords[0],
                y=self.title_coords[1] - (140 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
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
                x=self.title_coords[0],
                y=self.title_coords[1] - (140 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center"
            )

        settings.draw()

    def draw_main_menu(self):
        '''
        draw_main_menu draws the main menu button

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected == 'Main Menu':

            main_menu = arcade.Text(
                "Main Menu",
                x=self.title_coords[0],
                y=self.title_coords[1] - (180 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK
            )
            arcade.draw_rect_filled(
                arcade.XYWH(main_menu.x,
                main_menu.y,
                main_menu.content_width + (6 * c.RESOLUTION_RATIO),
                main_menu.content_height),
                arcade.csscolor.WHITE
            )

        else:
            main_menu = arcade.Text(
                "Main Menu",
                x=self.title_coords[0],
                y=self.title_coords[1] - (180 * c.RESOLUTION_RATIO),
                font_name="Edit Undo BRK",
                font_size = 30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center"
            )

        main_menu.draw()

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



