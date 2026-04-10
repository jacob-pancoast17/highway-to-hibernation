''' Module representing the start screen. '''
import arcade
import arcade.gui
from scripts import constants as c
from scripts.game_view import GameView
from scripts.screens.stats_screen import StatsScreen


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

        # Load title
        self.sprites = arcade.SpriteList()
        #title_texture = arcade.load_texture()
        title = arcade.Sprite("sprites/title.png")
        title.center_x = c.WINDOW_WIDTH / 2
        title.center_y = c.WINDOW_HEIGHT * .8
        title.scale = 0.85
        self.sprites.append(title)

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.options = ['Infinite', 'Hundred', 'Fifty', 'Thirty']
        self.space_between_options = 50

        self.num_options = len(self.options)
        self.currently_selected = self.options[0]
        self.options_coords = [(c.WINDOW_WIDTH / 2, c.WINDOW_HEIGHT * 0.57)]
        self.options_coords = self.generate_coords(self.num_options, self.options_coords[0])

        self.stats_text = arcade.Text(
            "Press 'S' for stats",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 8,
            font_size = 17,
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
        self.stats_text.draw()

        # draw "buttons"
        self.draw_infinity()
        self.draw_hundred()
        self.draw_fifty()
        self.draw_thirty()

    def on_update(self, delta_time):
        '''
        Happens every frame
        '''

        self.time_elapsed += delta_time

        if self.time_elapsed > self.next_blink:

            self.next_blink += c.BLINK_RATE

            self.blink()

    def generate_coords(self, num_options, previous_coord):

        return_list = [previous_coord]

        for i in range(num_options - 1):

            return_list.append((return_list[-1][0], return_list[-1][1] - self.space_between_options))

        return return_list

    def on_key_press(self, symbol, modifiers):

        # Move up
        if (symbol == arcade.key.UP and
            self.currently_selected != self.options[0]):

            # Get curr index
            curr_index = self.options.index(self.currently_selected)

            self.currently_selected = self.options[curr_index - 1]

        # Move down
        elif (symbol == arcade.key.DOWN and
            self.currently_selected != self.options[-1]):

            # Get curr index
            curr_index = self.options.index(self.currently_selected)

            self.currently_selected = self.options[curr_index + 1]
        
        # Open stats page
        elif symbol == arcade.key.S:
            self.window.show_view(StatsScreen(self))
        
        elif symbol == arcade.key.ENTER:
            if self.currently_selected == "Hundred":
                c.LEVEL_SIZE = 100
            elif self.currently_selected == "Fifty":
                c.LEVEL_SIZE = 50
            elif self.currently_selected == "Thirty":
                c.LEVEL_SIZE = 30
            else:
                c.LEVEL_SIZE = 10000
            game_view = GameView()
            self.window.show_view(game_view)

    
    def draw_infinity(self):

        if (self.blinked and self.currently_selected == 'Infinite'):

            infinite = arcade.Text(
                "INFINITE",
                x=self.options_coords[0][0],
                y=self.options_coords[0][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK)

            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[0][0],
                self.options_coords[0][1],
                infinite.content_width + 6,
                infinite.content_height),
                arcade.csscolor.WHITE
            )

        else:
            infinite = arcade.Text(
                "INFINITE",
                x=self.options_coords[0][0],
                y=self.options_coords[0][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

        infinite.draw()

    def draw_hundred(self):
        
        if (self.blinked and self.currently_selected == 'Hundred'):
            hundred = arcade.Text(
                "HUNDRED",
                # Would need to be changed to change order
                x=self.options_coords[1][0],
                y=self.options_coords[1][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.BLACK)
            
            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[1][0],
                self.options_coords[1][1],
                hundred.content_width + 6,
                hundred.content_height),
                arcade.csscolor.WHITE
            )

        else:
            hundred = arcade.Text(
                "HUNDRED",
                # Would need to be changed to change order
                x=self.options_coords[1][0],
                y=self.options_coords[1][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

        hundred.draw()

    def draw_fifty(self):
        if (self.blinked and self.currently_selected == 'Fifty'):
            fifty = arcade.Text(
                "FIFTY",
                # Would need to be changed to change order
                x=self.options_coords[2][0],
                y=self.options_coords[2][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.BLACK)
            
            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[2][0],
                self.options_coords[2][1],
                fifty.content_width + 6,
                fifty.content_height),
                arcade.csscolor.WHITE)

        else:
            fifty = arcade.Text(
                "FIFTY",
                x=self.options_coords[2][0],
                y=self.options_coords[2][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

        fifty.draw()
        
    def draw_thirty(self):

        if (self.blinked and self.currently_selected == 'Thirty'):
            thirty = arcade.Text(
                "THIRTY",
                # Would need to be changed to change order
                x=self.options_coords[3][0],
                y=self.options_coords[3][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.BLACK)
            
            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[3][0],
                self.options_coords[3][1],
                thirty.content_width + 6,
                thirty.content_height),
                arcade.csscolor.WHITE
            )

        else:
            thirty = arcade.Text(
                "THIRTY",
                x=self.options_coords[3][0],
                y=self.options_coords[3][1],
                font_name="Edit Undo BRK",
                font_size=30,
                anchor_x="center",
                anchor_y="center",
                color=arcade.csscolor.WHITE)

        thirty.draw()

    def blink(self):

        if self.blinked is False:

            self.blinked = True

        else:
            self.blinked = False
