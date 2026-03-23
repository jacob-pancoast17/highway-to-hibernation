''' Module representing the main game view. '''
import arcade
import constants as c
from objects.player import Player
from engines.texture_engine import TextureEngine
from engines.time_engine import TimeEngine
from engines.world_engine import WorldEngine
#from pause_screen import Pause

class GameView(arcade.View):
    '''GameView represents a window object'''

    def __init__(self):
        '''
        Constructor

        param: self
        return: nothing
        '''
        super().__init__()

        self.background_color = c.background

        # Timing
        self.next_move = 0

        self.player_sprite = None

        self.world = None
        self.player = None

        # A variable to store our gui camera object
        self.gui_camera = None

        # This variable will store our score as an integer.
        self.score = 0

        # This variable will store the text for score that we will draw to the screen.
        self.score_text = None

        self.setup()


    def setup(self):
        '''
        setup is run whenever the window is initially created,
        and creates the player, world engine, texture engine,
        and time engine.

        param: self
        return: nothing
        '''

        self.player = Player(c.STARTING_Y, c.STARTING_X)

        self.world = WorldEngine(self.window, self.player)
        self.world.generate_screen()

        self.texture_engine = TextureEngine(self.world, self.player)

        self.time_engine = TimeEngine(self.world, self.window)


        # Initialize our gui camera, initial settings are the same as our world camera.
        self.gui_camera = arcade.Camera2D()

        # Reset our score to 0
        self.score = 0

        # Farthest y value that the player reaches (used for score)
        self.farthest_y = 0

        # Initialize our arcade.Text object for score
        self.score_text = arcade.Text(
            f"Score: {self.score}", 
            x=5, 
            y=5,
            font_name="Edit Undo BRK",
            font_size=25,
            bold= True)

    def on_draw(self):
        """
        Render the screen every frame
        """
        self.clear()

        self.texture_engine.draw_all_sprites()
        
        # Load score text
        self.score_text.draw()
        
    def on_update(self, delta_time):
        '''
        Happens every frame
        '''

        self.time_engine.pass_time(delta_time)
        

    def on_key_press(self, key, modifiers):
        '''
        on_key_press detects when a key is pressed

        param: self
           symbol - key pressed
           modifiers - e.g. capslock or numlock
        '''

        # If the player presses a key, update the speed if able to move
        if (key == arcade.key.UP or
            key == arcade.key.DOWN or
            key == arcade.key.LEFT or
            key == arcade.key.RIGHT):

            # Test if player is going to collide with something
            did_move = self.player.try_move(key, self.world, self.window)
            if(did_move):
                #print("made it!")
                if(self.player.y > self.farthest_y):
                    self.farthest_y = self.player.y 
                    self.score += 100
                    #TODO delete print statement
                    print("SCORE:")
                    print(self.score)
                    self.score_text.text = f"Score: {self.score}"
            print(f"[{self.player.x}, {self.player.y}]")

        elif (key == arcade.key.ESCAPE):
            from screens.pause_screen import Pause
            # Pass in the current game state into Pause()
            self.window.show_view(Pause(self))
