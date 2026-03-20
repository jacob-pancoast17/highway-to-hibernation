''' Module representing the main game view. '''
import arcade
import constants as c
from hostile_object import Hostile
from obstacle_object import Obstacle
from player import Player
import random
from world_gen import WorldGen
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
        self.world_time = 0
        self.next_move = 0

        self.grid = None

        self.player_sprite = None

        self.world = None
        self.world_time = 0
        self.next_spawn_check = None
        self.next_spawn_check = c.TIME_BETWEEN_SPAWNS
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
        and creates the grid, objects, and the player

        param: self
        return: nothing
        '''

        # Create grid
        self.grid = arcade.SpriteList()

        # Create player object and "list" of players--
        # pyarcade can only drawing using a SpriteList, so
        # player has to be in a SpriteList
        self.player = Player(c.STARTING_Y,
                             c.STARTING_X)
        self.player_sprite = arcade.SpriteList()

        # Use the player class's to_sprite() to add the
        # SPRITE version to the SpriteList (to match types)
        self.player_sprite.append(self.player)

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

        # Create the grid
        for row in range(c.ROW_COUNT):

            for column in range(c.COLUMN_COUNT):

                # Append a new cell
                grass_texture = random.choices(
                    ['sprites/grass_1.png',
                    'sprites/grass_2.png',
                    'sprites/grass_3.png',
                    'sprites/flowers_1.png',
                    'sprites/flowers_2.png',
                    'sprites/flowers_3.png'],
                    weights = [0.22,
                     0.22,
                     0.22,
                     0.11,
                     0.11,
                     0.11]
                )
                sprite = arcade.Sprite(grass_texture[0])

                # Set the cell's center based on grid position
                sprite.center_x = (c.MARGIN + c.TILE_WIDTH) * column + c.MARGIN + c.TILE_WIDTH // 2
                sprite.center_y = (c.MARGIN + c.TILE_HEIGHT) * row + c.MARGIN + c.TILE_HEIGHT // 2

                # Append to list of all grid sprites to draw
                self.grid.append(sprite)

        self.world = WorldGen(self.window, self.player)
        self.world.generate_screen()
        
        # self.curr_loaded = []
        # for i in range(c.ROW_COUNT):
        #     self.curr_loaded.append(self.world.generate_row(i))
        # for i in range(len(self.curr_loaded)):
        #     print(self.world.rows[i])
        #     print(self.curr_loaded[i])

    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()

        # Draw the shapes representing our current grid
        self.grid.draw()

        # Load 1 row (TEMP)
        for i in range(len(self.world.loaded)):
            self.world.loaded[i].draw()
        for i in range(len(self.world.addons)):
            self.world.addons[i].draw()
        
        self.player_sprite.draw() # Draw the player on TOP of the grid
        
        # Load score text
        self.score_text.draw()
        
    def on_update(self, delta_time):
        '''
        Happens every frame
        '''
        self.world_time += delta_time

        curr_hostile_rows = self.world.get_hostile_rows()

        for row in curr_hostile_rows:

            # Try to move cars in each car row
            if self.world.loaded[row][0].static == False:

                for hostile in self.world.loaded[row]:
                    hostile.try_move(delta_time, self.window, self.player)

        # For every time between spawns, try to spawn
        if self.world_time > self.next_spawn_check:
            self.next_spawn_check += c.TIME_BETWEEN_SPAWNS
            for row in curr_hostile_rows:

                if self.world.loaded[row][0].static == False:
                    self.world.update_cars(row)
        # self.world_time += delta_time
        # speed = 0.5

        # if self.world_time >= self.next_move:
        #     self.next_move += speed
        #     for hostile in self.aggressive_hostiles_sprites:
        #         if hostile.try_move(self.window, self.player):
        #             hostile.move()
    

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
            from pause_screen import Pause
            # Pass in the current game state into Pause()
            self.window.show_view(Pause(self))
