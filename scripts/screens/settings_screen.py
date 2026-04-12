''' Module representing the settings screen. '''
import arcade
from scripts import constants as c


class Settings(arcade.View):
    ''' Settings represents the settings view '''
    def __init__(self, previous_view, from_pause=False):
        '''
        Constructor calls arcade 'View' superclass constructor
        
        param:
            self
        returns:
            nothing
        '''
        super().__init__()

        self.previous_view = previous_view

        # if from_pause:
        #     self.came_from_game = True
        # else:
        #     self.came_from_game = False

        # Change this to the one above to be able to edit screen size ^
        self.came_from_game = True

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.num_volume_bars = 10

        # Change these if adding more options
        self.options = ['Volume',
                        'Window',
                        'Resolution',
                        'Debug Mode',
                        'Back']
        self.num_options = len(self.options)
        self.currently_selected = self.options[0]

        self.window_options = ['Windowed',
                               'Borderless Windowed',
                               'Fullscreen']

        self.resolution_options = [450,
                                   675]

        self.size_dependent_constructor()

    def size_dependent_constructor(self):
        '''
        size_dependent_constructor is a constuctor used if the resolution is changed

        param:
            self
        returns:
            nothing
        '''
        self.space_between_options = 50 * c.RESOLUTION_RATIO
        self.space_between_volume_bars = 15 * c.RESOLUTION_RATIO

        self.options_coords = [(c.WINDOW_WIDTH * 5 / 16, c.WINDOW_HEIGHT * 0.70)]
        self.options_coords = self.generate_coords(self.num_options, self.options_coords[0])

    def on_update(self, delta_time):
        '''
        Happens every frame

        param:
            self
            delta_time
        returns:
            nothing
        '''
        self.time_elapsed += delta_time

        if self.time_elapsed > self.next_blink:

            self.next_blink += c.BLINK_RATE

            self.blink()

    def generate_coords(self, num_options, previous_coord):
        '''
        generate_coords is a helper funciton used to generate the coordinates of the game
        "buttons" based on the previous buttons coordinates

        param:
            self
            num_options - number of options in the set of "buttons"
            previous_coord - coordinates of previous "button"
        returns:
            return_list - list of coordinates
        '''

        return_list = [previous_coord]

        for i in range(num_options - 1):

            return_list.append((return_list[-1][0], return_list[-1][1] -
                                self.space_between_options))

        return return_list

    def on_draw(self):
        self.clear()

        self.draw_settings()
        self.draw_volume()
        self.draw_window()
        self.draw_resolution()
        self.draw_debug_mode()
        self.draw_back()

    def on_key_press(self, symbol, modifiers):
        '''
        on_key_press detects when a key is pressed

        param:
            self
            symbol - key pressed
            modifiers - e.g. capslock or numlock
        returns:
            nothing
        '''
        # Move up
        if ((symbol == arcade.key.UP or symbol == arcade.key.W) and
            self.currently_selected != self.options[0]):

            # Get curr index
            curr_index = self.options.index(self.currently_selected)

            if not self.came_from_game or self.currently_selected == 'Back':
                self.currently_selected = self.options[curr_index - 1]
            else:
                self.currently_selected = self.options[curr_index - 3]

        # Move down
        elif ((symbol == arcade.key.DOWN or symbol == arcade.key.S) and
            self.currently_selected != self.options[-1]):

            # Get curr index
            curr_index = self.options.index(self.currently_selected)

            if not self.came_from_game or self.currently_selected != 'Volume':
                self.currently_selected = self.options[curr_index + 1]
            elif self.currently_selected:
                self.currently_selected = self.options[curr_index + 3]

        # Move left or right
        elif (symbol == arcade.key.LEFT or symbol == arcade.key.A):

            # For volume
            if (self.currently_selected == 'Volume' and
                c.VOLUME > c.MIN_VOLUME):

                c.VOLUME -= 1

            # For window
            if self.currently_selected == 'Window':

                index = self.window_options.index(c.WINDOW) - 1

                if index == -1:
                    c.WINDOW = self.window_options[-1]
                else:
                    c.WINDOW = self.window_options[index]

                self.change_window()

            # For resolution
            if self.currently_selected == 'Resolution':

                index = self.resolution_options.index(c.RESOLUTION) - 1

                if index == -1:
                    c.RESOLUTION = self.resolution_options[-1]
                else:
                    c.RESOLUTION = self.resolution_options[index]

                self.change_resolution()

            # For debug
            if self.currently_selected == 'Debug Mode':

                c.DEBUG = not c.DEBUG

        # Move left or right
        elif (symbol == arcade.key.RIGHT or symbol == arcade.key.D):

            # For volume
            if (self.currently_selected == 'Volume' and c.VOLUME < c.MAX_VOLUME):

                c.VOLUME += 1

            # For window
            if self.currently_selected == 'Window':

                index = self.window_options.index(c.WINDOW) + 1

                if index == len(self.window_options):
                    c.WINDOW = self.window_options[0]
                else:
                    c.WINDOW = self.window_options[index]

                self.change_window()

            # For resolution
            if self.currently_selected == 'Resolution':

                index = self.resolution_options.index(c.RESOLUTION) + 1

                if index == len(self.resolution_options):
                    c.RESOLUTION = self.resolution_options[0]
                else:
                    c.RESOLUTION = self.resolution_options[index]

                self.change_resolution()

            # For debug
            if self.currently_selected == 'Debug Mode':

                c.DEBUG = not c.DEBUG

        # Exit to menu
        elif symbol == arcade.key.ESCAPE:

            self.window.show_view(self.previous_view)
            #self.previous_view.initialize()
            # Commented out so the game doesn't break
            # This is what would allow you to change the resolution mid game

        elif symbol == arcade.key.ENTER:

            # For back
            if self.currently_selected == 'Back':

                self.window.show_view(self.previous_view)

    def draw_settings(self):
        '''
        draw_settings is a helper function used to draw the settings text for the setting
        screen

        param:
            self
        returns:
            nothing
        '''
        arcade.draw_text(
            "SETTINGS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.82,
            font_name="Edit Undo BRK",
            font_size=40 * c.RESOLUTION_RATIO,
            anchor_x="center")

    def draw_volume(self):
        '''
        draw_volume is a helper function used to draw the volume text for the setting
        screen

        param:
            self
        returns:
            nothing
        '''
        if (self.blinked and
            self.currently_selected == 'Volume'):

            volume_title = arcade.Text(
                "VOLUME",

                # Would need to be changed to change order
                x=self.options_coords[0][0],
                y=self.options_coords[0][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK)

            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[0][0],
                self.options_coords[0][1],
                volume_title.content_width,
                volume_title.content_height),
                arcade.csscolor.WHITE
            )

            volume_title.draw()

        else:

            volume_title = arcade.Text(
                "VOLUME",

                # Would need to be changed to change order
                x=self.options_coords[0][0],
                y=self.options_coords[0][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

            volume_title.draw()

        for i in range(c.VOLUME):

            arcade.draw_rect_filled(
                arcade.XYWH((self.options_coords[0][0] + (volume_title.content_width / 2) +
                            40 + (self.space_between_volume_bars * i)),
                self.options_coords[0][1],
                10 * c.RESOLUTION_RATIO,
                30 * c.RESOLUTION_RATIO),
                arcade.csscolor.WHITE)

        for i in range(self.num_volume_bars - c.VOLUME):

            x = i + c.VOLUME

            arcade.draw_rect_filled(
                arcade.XYWH((self.options_coords[0][0] + (volume_title.content_width / 2) +
                            40 + (self.space_between_volume_bars * x)),
                self.options_coords[0][1],
                10 * c.RESOLUTION_RATIO,
                30 * c.RESOLUTION_RATIO),
                arcade.csscolor.DIM_GRAY)

        volume_arrow_left = arcade.Text(
                "<",

                # Would need to be changed to change order
                x=self.options_coords[0][0] + (volume_title.content_width / 2) + 40 +
                    (self.space_between_volume_bars * 0) - (20 * c.RESOLUTION_RATIO),
                y=self.options_coords[0][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        volume_arrow_right = arcade.Text(
                ">",

                # Would need to be changed to change order
                x=self.options_coords[0][0] + (volume_title.content_width / 2) + 40 +
                    (self.space_between_volume_bars * 9) + (20 * c.RESOLUTION_RATIO),
                y=self.options_coords[0][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        volume_arrow_left.draw()
        volume_arrow_right.draw()

    def draw_window(self):
        '''
        draw_window is a helper function used to draw the window text for the setting
        screen

        param:
            self
        returns:
            nothing
        '''
        if (self.blinked and
            self.currently_selected == 'Window'):

            window_title = arcade.Text(
                "WINDOW",

                # Would need to be changed to change order of options
                x=self.options_coords[1][0],
                y=self.options_coords[1][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK)

            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[1][0],
                self.options_coords[1][1],
                window_title.content_width,
                window_title.content_height),
                arcade.csscolor.WHITE
            )

        else:

            window_title = arcade.Text(
                "WINDOW",

                # Would need to be changed to change order of options
                x=self.options_coords[1][0],
                y=self.options_coords[1][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

        if self.came_from_game:

            window_title.color = arcade.csscolor.DIM_GRAY

        window_title.draw()

        if c.WINDOW == 'Windowed':
            window_status = arcade.Text(
                    "Windowed",

                    # Would need to be changed to change order
                    x=self.options_coords[1][0] + window_title.content_width * 3/2,
                    y=self.options_coords[1][1],

                    align='right',
                    font_name="Edit Undo BRK",
                    font_size=30 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)

        elif c.WINDOW == 'Fullscreen':
            window_status = arcade.Text(
                    "Fullscreen",

                    # Would need to be changed to change order
                    x=self.options_coords[1][0] + window_title.content_width * 3/2,
                    y=self.options_coords[1][1],

                    align='right',
                    font_name="Edit Undo BRK",
                    font_size=30 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)
        else:
            window_status = arcade.Text(
                    "Borderless\nWindowed",

                    # Would need to be changed to change order
                    x=self.options_coords[1][0] + window_title.content_width * 3/2,
                    y=self.options_coords[1][1],

                    align='center',
                    font_name="Edit Undo BRK",
                    multiline=True,
                    width = 300 * c.RESOLUTION_RATIO,
                    font_size=20 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)

        window_arrow_left = arcade.Text(
                "<",

                # Would need to be changed to change order
                x=self.options_coords[1][0] + (window_title.content_width * 3 / 2) -
                    (110 * c.RESOLUTION_RATIO),
                y=self.options_coords[1][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        window_arrow_right = arcade.Text(
                ">",

                # Would need to be changed to change order
                x=self.options_coords[1][0] + (window_title.content_width * 3 / 2) +
                    (110 * c.RESOLUTION_RATIO),
                y=self.options_coords[1][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        if self.came_from_game:

            window_status.color = arcade.csscolor.DIM_GRAY
            window_arrow_left.color = arcade.csscolor.DIM_GRAY
            window_arrow_right.color = arcade.csscolor.DIM_GRAY

        window_status.draw()

        window_arrow_left.draw()
        window_arrow_right.draw()

    def draw_resolution(self):
        '''
        draw_resolution is a helper function used to draw the resolution text for the setting
        screen

        param:
            self
        returns:
            nothing
        '''
        if (self.blinked and
            self.currently_selected == 'Resolution'):

            resolution_title = arcade.Text(
                "RESOLUTION",

                # Would need to be changed to change order of options
                x=self.options_coords[2][0],
                y=self.options_coords[2][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK)

            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[2][0],
                self.options_coords[2][1],
                resolution_title.content_width,
                resolution_title.content_height),
                arcade.csscolor.WHITE
            )

        else:

            resolution_title = arcade.Text(
                "RESOLUTION",

                # Would need to be changed to change order of options
                x=self.options_coords[2][0],
                y=self.options_coords[2][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

        if self.came_from_game:

            resolution_title.color = arcade.csscolor.DIM_GRAY

        resolution_title.draw()

        resolution_status = None

        if c.RESOLUTION == 450:
            resolution_status = arcade.Text(
                    "450 x 450",

                    # Would need to be changed to change order
                    x=self.options_coords[2][0] + resolution_title.content_width,
                    y=self.options_coords[2][1],

                    align='right',
                    font_name="Edit Undo BRK",
                    font_size=25 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)

        elif c.RESOLUTION == 675:
            resolution_status = arcade.Text(
                    "675 x 675",

                    # Would need to be changed to change order
                    x=self.options_coords[2][0] + resolution_title.content_width,
                    y=self.options_coords[2][1],

                    align='right',
                    font_name="Edit Undo BRK",
                    font_size=25 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)
        # else:
        #     debug_status = arcade.Text(
        #             f"Borderless\nWindowed",

        #             # Would need to be changed to change order
        #             x=self.options_coords[1][0] + window_title.content_width * 3/2,
        #             y=self.options_coords[1][1],

        #             align='center',
        #             font_name="Edit Undo BRK",
        #             multiline=True,
        #             width = 300,
        #             font_size=20,
        #             anchor_x="center",
        #             anchor_y="center",
        #             color = arcade.csscolor.WHITE)

        resolution_arrow_left = arcade.Text(
                "<",

                # Would need to be changed to change order
                x=self.options_coords[2][0] + (resolution_title.content_width) -
                    (90 * c.RESOLUTION_RATIO),
                y=self.options_coords[2][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        resolution_arrow_right = arcade.Text(
                ">",

                # Would need to be changed to change order
                x=self.options_coords[2][0] + (resolution_title.content_width) +
                    (90 * c.RESOLUTION_RATIO),
                y=self.options_coords[2][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        if self.came_from_game:

            resolution_status.color = arcade.csscolor.DIM_GRAY
            resolution_arrow_left.color = arcade.csscolor.DIM_GRAY
            resolution_arrow_right.color = arcade.csscolor.DIM_GRAY

        resolution_status.draw()
        resolution_arrow_left.draw()
        resolution_arrow_right.draw()

    def draw_debug_mode(self):
        '''
        draw_debug_mode is a helper function used to draw the debug text for the setting
        screen

        param:
            self
        returns:
            nothing
        '''
        if (self.blinked and
            self.currently_selected == 'Debug Mode'):

            debug_title = arcade.Text(
                "DEBUG MODE",

                # Would need to be changed to change order of options
                x=self.options_coords[3][0],
                y=self.options_coords[3][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.BLACK)

            arcade.draw_rect_filled(
                arcade.XYWH(self.options_coords[3][0],
                self.options_coords[3][1],
                debug_title.content_width,
                debug_title.content_height),
                arcade.csscolor.WHITE
            )

        else:

            debug_title = arcade.Text(
                "DEBUG MODE",

                # Would need to be changed to change order of options
                x=self.options_coords[3][0],
                y=self.options_coords[3][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO,
                anchor_x="center",
                anchor_y="center",
                color = arcade.csscolor.WHITE)

        debug_title.draw()

        if c.DEBUG:
            debug_status = arcade.Text(
                    "ON",

                    # Would need to be changed to change order
                    x=self.options_coords[3][0] + debug_title.content_width * 7/8,
                    y=self.options_coords[3][1],

                    align='right',
                    font_name="Edit Undo BRK",
                    font_size=30 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)
        else:
            debug_status = arcade.Text(
                    "OFF",

                    # Would need to be changed to change order
                    x=self.options_coords[3][0] + debug_title.content_width * 7/8,
                    y=self.options_coords[3][1],

                    align='right',
                    font_name="Edit Undo BRK",
                    font_size=30 * c.RESOLUTION_RATIO,
                    anchor_x="center",
                    anchor_y="center",
                    color = arcade.csscolor.WHITE)

        debug_arrow_left = arcade.Text(
                "<",

                # Would need to be changed to change order
                x=self.options_coords[3][0] + (debug_title.content_width * 7 / 8) -
                    (50 * c.RESOLUTION_RATIO),
                y=self.options_coords[3][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        debug_arrow_right = arcade.Text(
                ">",

                # Would need to be changed to change order
                x=self.options_coords[3][0] + (debug_title.content_width * 7 / 8) +
                    (50 * c.RESOLUTION_RATIO),
                y=self.options_coords[3][1],

                align='right',
                font_name="Edit Undo BRK",
                font_size=30 * c.RESOLUTION_RATIO / 1.5,
                anchor_x="center",
                anchor_y="center")

        debug_status.draw()
        debug_arrow_left.draw()
        debug_arrow_right.draw()

    def draw_back(self):
        '''
        draw_back is a helper function used to draw the back button from the settings
        screen

        param:
            self
        returns:
            nothing
        '''
        if self.blinked and self.currently_selected == 'Back':

            back_text = arcade.Text(
                "BACK",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.08,
                font_size=30 * c.RESOLUTION_RATIO,
                font_name="Edit Undo BRK",
                anchor_x='center',
                anchor_y='center',
                color = arcade.csscolor.BLACK
            )

            arcade.draw_rect_filled(
                arcade.XYWH(back_text.x,
                back_text.y,
                back_text.content_width + (6 * c.RESOLUTION_RATIO),
                back_text.content_height),
                arcade.csscolor.WHITE)

        else:

            back_text = arcade.Text(
                "BACK",
                x=c.WINDOW_WIDTH / 2,
                y=c.WINDOW_HEIGHT * 0.08,
                font_size=30 * c.RESOLUTION_RATIO,
                font_name="Edit Undo BRK",
                anchor_x='center',
                anchor_y='center'
            )

        back_text.draw()

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

    def change_window(self):
        '''
        Changes the current window size
        
        param:
            self
        return:
            nothing
        '''
        if c.WINDOW == 'Windowed':

            self.window.set_fullscreen(False)

        else:

            self.window.set_fullscreen(True)

    def change_resolution(self):
        '''
        Changes the current resolution
        
        param:
            self
        return:
            nothing
        '''
        if c.RESOLUTION == 450:

            # Change tile sizes
            c.TILE_SIZE = 30

            # Change window size
            c.WINDOW_HEIGHT = c.TILE_SIZE * c.ROW_COUNT
            c.WINDOW_WIDTH = c.TILE_SIZE * c.COLUMN_COUNT

        elif c.RESOLUTION == 675:
            # Change tile sizes
            c.TILE_SIZE = 1.5 * 30

            # Change window size
            c.WINDOW_HEIGHT = c.TILE_SIZE * c.ROW_COUNT
            c.WINDOW_WIDTH = c.TILE_SIZE * c.COLUMN_COUNT

        c.RESOLUTION_RATIO = c.TILE_SIZE / 30

        self.window.set_size(c.WINDOW_WIDTH, c.WINDOW_HEIGHT)
        #self.window.update()
        self.size_dependent_constructor()

    def on_resize(self, width, height):

        super().on_resize(width, height)

        print(f"{height}, {width}")

        #self.camera.position = (-225, -225)
