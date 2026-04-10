''' Module representing the start screen. '''
import arcade
import arcade.gui
from scripts import constants as c
from scripts.game_view import GameView
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
        title.center_y = c.WINDOW_HEIGHT * 3 / 4
        title.scale = 0.85 * c.RESOLUTION_RATIO
        self.sprites.append(title)

        # Load play button
        play_texture = arcade.load_texture("sprites/play_button.png")
        play_texture_hover = arcade.load_texture("sprites/play_button_hover.png")

        play_button = arcade.gui.UITextureButton(
            width = play_texture.width * c.RESOLUTION_RATIO,
            height = play_texture.height * c.RESOLUTION_RATIO,
            texture = play_texture,
            texture_hovered = play_texture_hover
        )
        play_button.center_x = c.WINDOW_WIDTH / 2
        play_button.center_y = c.WINDOW_HEIGHT / 2
        print(f"width: {play_button.width} height: {play_button.height}")

        # Initialize button and define on-click event
        @play_button.event("on_click")
        def on_click_play(event):
            game_view = GameView()
            self.window.show_view(game_view)

        # Tell the button how to position itself
        self.uimanager.clear()
        self.uimanager.add(play_button)

        self.stats_text = arcade.Text(
            "Press 'S' for stats",
            x=c.WINDOW_WIDTH / 2,
            y=c.WINDOW_HEIGHT / 5,
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
        self.stats_text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.S:
            self.window.show_view(StatsScreen(self))

        elif symbol == arcade.key.F:
            self.window.show_view(Settings(self))

