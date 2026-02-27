import arcade
import constants as c
import game_view as GameView

'''
StartScreen represents the start screen view
'''
class StartScreen(arcade.View):
    '''
    Constructor calls arcade 'View' superclass constructor

    param: self
    return: nothing
    '''
    def __init__(self):
        super().__init__()

    '''
    on_show_view defines events that happen when switching
    to the start screen view

    param: self
    return: nothing
    '''
    def on_show_view(self):
        # Set background color
        self.window.background_color == c.start_screen_background

        # Reset view
        self.window.default_camera.use()

    '''
    on_draw redraws the frame for the start screen

    param: self
    return: nothing
    '''
    def on_draw(self):
        # Reset window
        self.clear()

        #TODO: Change to text objects, apparently draw is very inefficient
        arcade.draw_text("Highway to Hibernation", 
                         x = c.WIDTH / 2, 
                         y = c.HEIGHT * 3 / 4,
                         font_size = 50,
                         anchor_x = "center",
                         anchor_y = "center")
        
        arcade.draw_text("Click to begin",
                         x = c.WIDTH / 2,
                         y = c.HEIGHT / 2,
                         font_size = 20,
                         anchor_x = "center",
                         anchor_y = "center")
        
    '''
    on_mouse_press detects when the mouse is pressed and
    changes the view to the game view

    param: self
           _x - cursor x pos
           _y - cursor y pos
           _button - button on mouse pressed
           _modifiers - shift, ctrl, numlock, etc.
    '''
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView.GameView()
        self.window.show_view(game_view)
        game_view.run_window()
