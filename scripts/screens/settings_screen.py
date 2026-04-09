import arcade
from scripts import constants as c


class Settings(arcade.View):
    def __init__(self, previous_view):

        super().__init__()

        self.previous_view = previous_view

        self.time_elapsed = 0
        self.next_blink = c.BLINK_RATE
        self.blinked = False

        self.num_volume_bars = 10 

        # Change these if adding more options
        self.options = ['Volume',
                        'Window',
                        'Resolution',
                        'Debug Mode']
        self.num_options = len(self.options)
        self.currently_selected = self.options[0]

        self.window_options = ['Windowed',
                               'Borderless Windowed',
                               'Fullscreen']
        
        self.resolution_options = [450,
                                   900]
        
        self.size_dependent_constructor()

    def size_dependent_constructor(self):

        print('constructing')

        self.space_between_options = 50 * c.RESOLUTION_RATIO
        self.space_between_volume_bars = 15 * c.RESOLUTION_RATIO

        self.options_coords = [(c.WINDOW_WIDTH * 5 / 16, c.WINDOW_HEIGHT * 0.70)]
        self.options_coords = self.generate_coords(self.num_options, self.options_coords[0])

    def on_show_view(self):
        self.window.default_camera.use()

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

    def on_draw(self):
        self.clear()

        self.draw_settings()
        self.draw_volume()
        self.draw_window()
        self.draw_resolution()
        self.draw_debug_mode()
        
        self.draw_escape()      

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
        
        # Move left or right
        elif (symbol == arcade.key.LEFT):

            # For volume
            if (self.currently_selected == 'Volume' and
                c.VOLUME > c.MIN_VOLUME):

                c.VOLUME -= 1

            # For window
            if (self.currently_selected == 'Window'):

                index = self.window_options.index(c.WINDOW) - 1

                if index == -1:
                    c.WINDOW = self.window_options[-1]
                else:
                    c.WINDOW = self.window_options[index]
                
                self.change_window()

            # For resolution
            if (self.currently_selected == 'Resolution'):

                index = self.resolution_options.index(c.RESOLUTION) - 1

                if index == -1:
                    c.RESOLUTION = self.resolution_options[-1]
                else:
                    c.RESOLUTION = self.resolution_options[index]
            
                self.change_resolution()

            # For debug
            if (self.currently_selected == 'Debug Mode'):

                c.DEBUG = not c.DEBUG

        # Move left or right
        elif (symbol == arcade.key.RIGHT):

            # For volume
            if (self.currently_selected == 'Volume' and
                c.VOLUME < c.MAX_VOLUME):

                c.VOLUME += 1

            # For window
            if (self.currently_selected == 'Window'):

                index = self.window_options.index(c.WINDOW) + 1

                if index == len(self.window_options):
                    c.WINDOW = self.window_options[0]
                else:
                    c.WINDOW = self.window_options[index]

                self.change_window()

            # For resolution
            if (self.currently_selected == 'Resolution'):

                index = self.resolution_options.index(c.RESOLUTION) + 1

                if index == len(self.resolution_options):
                    c.RESOLUTION = self.resolution_options[0]
                else:
                    c.RESOLUTION = self.resolution_options[index]

                self.change_resolution()

            # For debug
            if (self.currently_selected == 'Debug Mode'):

                c.DEBUG = not c.DEBUG

        # Exit to menu
        elif symbol == arcade.key.ESCAPE:
            
            self.window.show_view(self.previous_view)

    def draw_settings(self):

        print(f"font size: {40 * c.RESOLUTION_RATIO}")

        arcade.draw_text(
            "SETTINGS",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.82,
            font_name="Edit Undo BRK",
            font_size=40 * c.RESOLUTION_RATIO,
            anchor_x="center")
    
    def draw_volume(self):

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
                    arcade.XYWH((self.options_coords[0][0] + (volume_title.content_width / 2) + 40 + (self.space_between_volume_bars * i)),
                    self.options_coords[0][1],
                    10 * c.RESOLUTION_RATIO,
                    30 * c.RESOLUTION_RATIO),
                    arcade.csscolor.WHITE
                )
        
        for i in range(self.num_volume_bars - c.VOLUME):

            x = i + c.VOLUME

            arcade.draw_rect_filled(
                    arcade.XYWH((self.options_coords[0][0] + (volume_title.content_width / 2) + 40 + (self.space_between_volume_bars * x)),
                    self.options_coords[0][1],
                    10 * c.RESOLUTION_RATIO,
                    30 * c.RESOLUTION_RATIO),
                    arcade.csscolor.DIM_GRAY
                )
            
    def draw_window(self):

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
        
        window_title.draw()

        if c.WINDOW == 'Windowed':
            debug_status = arcade.Text(
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
            debug_status = arcade.Text(
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
            debug_status = arcade.Text(
                    f"Borderless\nWindowed",

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

        debug_status.draw()
            
    def draw_resolution(self):

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
        
        resolution_title.draw()

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
            
        elif c.RESOLUTION == 900:
            resolution_status = arcade.Text(
                    "900 x 900",

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

        resolution_status.draw()
    
    def draw_debug_mode(self):

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

        debug_status.draw()

    def draw_escape(self):

        arcade.draw_text(
            "Press ESC to go back",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT * 0.08,
            font_name="Edit Undo BRK",
            font_size=16 * c.RESOLUTION_RATIO,
            anchor_x="center"
        )

    def blink(self):

        if self.blinked == False:

            self.blinked = True

        else:
            self.blinked = False

    def change_window(self):

        if c.WINDOW == 'Windowed':

            self.window.set_fullscreen(False)
            self.window.style = arcade.Window.WINDOW_STYLE_DEFAULT

        elif c.WINDOW == 'Borderless Window':

            self.window.set_fullscreen(False)
            self.window.style = arcade.Window.WINDOW_STYLE_BORDERLESS

        else:

            self.window.set_fullscreen(True)
            self.window.style = arcade.Window.WINDOW_STYLE_DEFAULT

        #self.window.update()
    
    def change_resolution(self):

        if c.RESOLUTION == 450:

            c.WINDOW_HEIGHT = c.TILE_SIZE * c.ROW_COUNT
            c.WINDOW_WIDTH = c.TILE_SIZE * c.COLUMN_COUNT

        elif c.RESOLUTION == 900:

            c.WINDOW_HEIGHT = 2 * c.TILE_SIZE * c.ROW_COUNT
            c.WINDOW_WIDTH = 2 * c.TILE_SIZE * c.COLUMN_COUNT

        c.RESOLUTION_RATIO = c.RESOLUTION / 450

        self.window.set_size(c.WINDOW_WIDTH, c.WINDOW_HEIGHT)
        #self.window.update()
        self.size_dependent_constructor()
