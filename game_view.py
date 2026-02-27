import arcade
import constants as c
import game_over_screen as GameOver
from object import Object

'''
GameView represents a window object
'''
class GameView(arcade.View):
    '''
    Constructor

    param: arcade window
    return: nothing
    '''
    def __init__(self):
        super().__init__()

        self.background_color = c.background
        self.shape_list = None
        self.object_list = None

        self.curr_player_pos = [0, 7]
        self.grid = []
        for row in range(c.ROW_COUNT):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(c.COLUMN_COUNT):
                if(row == 0 and column == 7):
                    self.grid[row].append(1)
                else:
                    self.grid[row].append(0)  # Append a cell


        # Set the window's background color
        self.background_color = arcade.color.BLACK
        # Create shapes from the grid
        self.recreate_grid()

    def recreate_grid(self):
        """
        Create the shapes for our current grid.


        We look at the values in each cell.
        If the cell contains 0 we create a white shape.
        If the cell contains 1 we create a green shape.
        """
        self.shape_list = arcade.shape_list.ShapeElementList()
        for row in range(c.ROW_COUNT):
            for column in range(c.COLUMN_COUNT):
                if self.grid[row][column] == 0:
                    color = arcade.color.WHITE
                else:
                    color = arcade.color.GREEN


                x = (c.MARGIN + c.WIDTH) * column + c.MARGIN + c.WIDTH // 2
                y = (c.MARGIN + c.HEIGHT) * row + c.MARGIN + c.HEIGHT // 2


                current_rect = arcade.shape_list.create_rectangle_filled(
                    x, y, c.WIDTH, c.HEIGHT, color,
                )
                self.shape_list.append(current_rect)


    def on_draw(self):
        """
        Render the screen.
        """
        # We should always start by clearing the window pixels
        self.clear()


        # Draw the shapes representing our current grid
        self.shape_list.draw()

    '''
    on_key_press detects when a key is pressed

    param: self
           symbol - key pressed
           modifiers - e.g. capslock or numlock
    '''

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # If the player presses a key, update the speed
        if key == arcade.key.UP:
            #print("Up!")
            if(self.curr_player_pos[0] < len(self.grid) - 1):
                self.grid[self.curr_player_pos[0]][self.curr_player_pos[1]] = 0
                self.curr_player_pos[0] = self.curr_player_pos[0] + 1
                print(self.curr_player_pos)
        elif key == arcade.key.DOWN:
            #print("Down!")
            if(self.curr_player_pos[0] > 0):
                self.grid[self.curr_player_pos[0]][self.curr_player_pos[1]] = 0
                self.curr_player_pos[0] = self.curr_player_pos[0] - 1
                print(self.curr_player_pos)
        elif key == arcade.key.LEFT:
            #print("Left!")
            if(self.curr_player_pos[1] > 0):
                self.grid[self.curr_player_pos[0]][self.curr_player_pos[1]] = 0
                self.curr_player_pos[1] = self.curr_player_pos[1] - 1
                print(self.curr_player_pos)
        elif key == arcade.key.RIGHT:
            #print("Right!")
            if(self.curr_player_pos[1] < len(self.grid[0]) - 1):
                self.grid[self.curr_player_pos[0]][self.curr_player_pos[1]] = 0
                self.curr_player_pos[1] = self.curr_player_pos[1] + 1
                print(self.curr_player_pos)
        elif key == arcade.key.ESCAPE:
            game_over = GameOver.GameOver()
            self.window.show_view(game_over)
        self.grid[self.curr_player_pos[0]][self.curr_player_pos[1]] = 1
        self.recreate_grid()

    '''
    run_window sets up the window and runs it

    param: self
    return: nothing
    '''
    def run_window(self):
        #self.setup()
        arcade.run()