''' Module representing the main game view. '''
import arcade
from scripts import constants as c
from scripts.objects.player import Player
from scripts.screens.pause_screen import Pause
from scripts.screens.game_over_screen import GameOver
from scripts.engines.texture_engine import TextureEngine
from scripts.engines.time_engine import TimeEngine
from scripts.engines.world_engine import WorldEngine
from scripts.stats_manager import record_score

#from pause_screen import Pause

class GameView(arcade.View):
    '''GameView represents a window object'''

    def __init__(self):
        '''
        Constructor

        param:
            self
        returns:
            nothing
        '''
        super().__init__()

        self.background_color = c.background

        # Timing
        self.next_move = 0
        self.time_stopped = False
        self.death_timer = 0

        self.player_sprite = None

        self.world = None
        self.player = None
        self.controls_removed = False

        # A variable to store our gui camera object
        self.gui_camera = None

        # This variable will store the text for score that we will draw to the screen.
        self.score_text = None

        self.current_bottom_of_screen = None
        self.current_top_of_screen = None

        self.farthest_y = None

        self.walk_playback = None
        self.hunny_pickup = None
        self.achieve_game_over = None

        self.setup()


    def setup(self):
        '''
        setup is run whenever the window is initially created,
        and creates the player, world engine, texture engine,
        and time engine.

        param:
            self
        returns:
            nothing
        '''
        self.texture_engine = TextureEngine()

        self.player = Player(c.STARTING_Y, c.STARTING_X, self.texture_engine)

        self.texture_engine.add_player(self.player)

        self.world = WorldEngine(self.window, self.player, self.texture_engine)
        self.world.generate_screen()

        self.texture_engine.add_world(self.world)

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

        self.current_bottom_of_screen = 0
        self.current_top_of_screen = c.ROW_COUNT - 1

        # Music
        c.MAIN_THEME = arcade.play_sound(c.ADVENTURE_MUSIC)
        c.MAIN_THEME.loop = True
        c.MAIN_THEME.volume = 0.4

    def on_draw(self):
        '''
        Render the screen every frame
        '''
        self.clear()

        self.texture_engine.draw_all_sprites()

        # Load score text
        self.score_text.draw()

    def on_update(self, delta_time):
        '''
        Happens every frame
        '''

        c.MAIN_THEME.play()

        if not self.time_stopped:

            self.time_engine.pass_time(delta_time)

        if self.player.dead:

            self.time_stopped = True
            self.controls_removed = True
            self.player.angle = 180
            self.death_timer += delta_time
            self.play_death_animation(delta_time)

            if self.death_timer > c.DEATH_ANIMATION_LENGTH:

                self.window.show_view(GameOver(self.player.score, self))
                self.achieve_game_over = arcade.play_sound(c.GAME_OVER_JINGLE)

            return

        # checks for collision between player and collectibles

        for hunny in self.world.collectibles:

            hit = arcade.check_for_collision_with_list(
                self.player, hunny)

            if hit:

                self.world.collectibles[self.world.collectibles.index(hunny)] = arcade.SpriteList()
                self.player.score += 300
                self.hunny_pickup = arcade.play_sound(c.HUNNY_SFX)

            self.score_text.text = f"Score: {self.player.score}"

    def on_key_press(self, symbol, modifiers):
        '''
        on_key_press detects when a key is pressed

        param: self
           symbol - key pressed
           modifiers - e.g. capslock or numlock
        '''

        # If the player presses a key, update the speed if able to move
        if ((symbol == arcade.key.UP or
            symbol == arcade.key.DOWN or
            symbol == arcade.key.LEFT or
            symbol == arcade.key.RIGHT) and
            not self.controls_removed):

            # Test if player is going to collide with something
            did_move = self.player.try_move(symbol, self.world, self.window)

            if did_move:
                # print("made it!")
                # play movement sfx
                self.walk_playback = arcade.play_sound(c.WALK_SFX)

                if self.player.y > self.farthest_y:
                    self.farthest_y = self.player.y
                    self.player.score += 100
                    self.score_text.text = f"Score: {self.player.score}"

                print(self.current_bottom_of_screen)
                if (self.player.y > self.current_bottom_of_screen + (c.DIST_UNTIL_STAY_PUT - 1) and
                    self.current_top_of_screen != c.LEVEL_SIZE - 1 and symbol == arcade.key.UP):
                    self.move_screen_up()

            print(f"[{self.player.x}, {self.player.y}]")

        elif symbol == arcade.key.ESCAPE:
            # Pass in the current game state into Pause()
            self.window.show_view(Pause(self))
            c.MAIN_THEME.pause()
        elif symbol == arcade.key.X:
            self.player.dead = True
            self.player.death = "Mauled"
            self.death_sound = arcade.play_sound(c.DEATH_SFX)

    def move_screen_up(self):
        '''
        move_screen_up 
        '''

        self.world.update_screen(self.current_top_of_screen + 1)

        self.current_bottom_of_screen += 1
        self.current_top_of_screen += 1

    def play_death_animation(self, delta_time):
        '''
        play_death_aninmation runs the death animation when the player dies

        param:
            self
            delta_time
        returns:
            nothing
        '''

        arcade.stop_sound(c.MAIN_THEME)
        self.player.die(delta_time)
