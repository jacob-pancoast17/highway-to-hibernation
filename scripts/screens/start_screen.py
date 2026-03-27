''' Module representing the start screen. '''
import arcade
import arcade.gui
from scripts import constants as c
from scripts.game_view import GameView


class StartScreen(arcade.View):
    '''
    StartScreen represents the start screen view
    '''

    def __init__(self):
        '''
        Constructor calls arcade 'View' superclass constructor

        param: self
        return: nothing
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
        title.center_y = c.WINDOW_HEIGHT * 3 / 4
        title.scale = 0.85
        self.sprites.append(title)

        # Load play button
        play_texture = arcade.load_texture("sprites/play_button.png")
        play_texture_hover = arcade.load_texture("sprites/play_button_hover.png")

        play_button = arcade.gui.UITextureButton(
            width = 100,
            texture = play_texture,
            texture_hovered = play_texture_hover
        )

        # Initialize button and define on-click event
        @play_button.event("on_click")
        def on_click_play(event):
            print("Awesome!")
            game_view = GameView()
            self.window.show_view(game_view)

        # Tell the button how to position itself
        anchor = self.uimanager.add(arcade.gui.UIAnchorLayout())

        anchor.add(
            anchor_x = "center_x",
            anchor_y = "center_y",
            child = play_button
        )

    def on_show_view(self):
        '''
        on_show_view defines events that happen when switching
        to the start screen view

        param: self
        return: nothing
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

        param: self
        return: nothing
        '''
        self.uimanager.disable()


    def on_draw(self):
        '''
        on_draw redraws the frame for the start screen

        param: self
        return: nothing
        '''
        # Reset window
        self.clear()

        # Draw UI elements
        self.sprites.draw()
        self.uimanager.draw()
