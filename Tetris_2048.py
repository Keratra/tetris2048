import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes
from scenes import *
from playsound import playsound

# Group: Heavenly Celestials
# ->    Kerem Kaya
# -> Mehmet Talha Bozan
# ->    Pelin Mişe

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
   # create the canvas for the game
   grid_h, grid_w, grid = create_canvas(the_grid_height=20, the_grid_width=10, info_grid_width=4)
   
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   first_tetromino_shape = generate_next_tetromino_type()
   current_tetromino = create_tetromino(first_tetromino_shape)
   grid.current_tetromino = current_tetromino
   # create and show the next tetromino as a display
   next_tetromino_shape = generate_next_tetromino_type()
   next_tetromino_display = create_tetromino(next_tetromino_shape)
   grid.display_tetromino = next_tetromino_display

   # if the game doesn't start, then please remove this line
   # this is because there is a possiblity that the line below only works on Windows
   # play music in the background
   #playsound('music.mp3', False)

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   is_game_scene, game_speed = display_game_menu(grid_h, grid_w)
   do_reset = False
   # clear the queue of the pressed keys for a smoother interaction
   stddraw.clearKeysTyped()
   # the main game loop (keyboard interaction for moving the tetromino) 
   while True:
      if is_game_scene:
         # check user interactions via the keyboard
         if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
            key_typed = "left"  if key_typed == "a" else key_typed
            key_typed = "right" if key_typed == "d" else key_typed
            key_typed = "down"  if key_typed == "s" else key_typed
            key_typed = "up"    if key_typed == "w" else key_typed
            # end the game by pressing "ESC" button
            if key_typed == "escape":
               is_game_scene = False
            # if the left arrow key has been pressed
            elif key_typed == "left":
               # move the active tetromino left by one
               current_tetromino.move(key_typed, grid) 
            # if the right arrow key has been pressed
            elif key_typed == "right":
               # move the active tetromino right by one
               current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
               # move the active tetromino down by one 
               # (soft drop: causes the tetromino to fall down faster)
               current_tetromino.move(key_typed, grid)
            elif key_typed == "space":
               # causes the tetromino to drop down as far as it can
               current_tetromino.hard_drop(grid)
            elif key_typed == "up":
               current_tetromino.rotate_clockwise(grid)
            elif key_typed == "left ctrl" :
               current_tetromino.rotate_counter_clockwise(grid)
            elif key_typed == "p":
               do_reset = display_pause_menu(grid_h,grid_w)
            # clear the queue of the pressed keys for a smoother interaction
            stddraw.clearKeysTyped()

         if do_reset:
            grid.reset_scene() # remove the existing tetrominos in grid
            first_tetromino_shape = generate_next_tetromino_type()
            current_tetromino = create_tetromino(first_tetromino_shape)
            grid.current_tetromino = current_tetromino
            # create and show the next tetromino as a display
            next_tetromino_shape = generate_next_tetromino_type()
            next_tetromino_display = create_tetromino(next_tetromino_shape)
            grid.display_tetromino = next_tetromino_display
            is_game_scene, game_speed = display_game_menu(grid_h, grid_w)
            # clear the queue of the pressed keys for an actual restart
            stddraw.clearKeysTyped()
            do_reset = False
         else:
            # move the active tetromino down by one at each iteration (auto fall)
            success = current_tetromino.move("down", grid)

            # place the active tetromino on the grid when it cannot go down anymore
            if not success:
               # get the tile matrix of the tetromino without empty rows and columns
               # and the position of the bottom left cell in this matrix
               tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
               # update the game grid by locking the tiles of the landed tetromino
               game_over = grid.update_grid(tiles, pos)
               
               # end the main game loop if the game is over
               if game_over:
                  is_game_scene = False
               # create the next tetromino to enter the game grid
               # by using the create_tetromino function defined below
               current_tetromino = create_tetromino(next_tetromino_shape)
               grid.current_tetromino = current_tetromino
               # generate the next next tetromino. :D 
               next_tetromino_shape = generate_next_tetromino_type()
               next_tetromino_display = create_tetromino(next_tetromino_shape)
               grid.display_tetromino = next_tetromino_display
            # display the game grid and the current tetromino
            grid.display(game_speed)
            #display_next_tetromino(grid_h, grid_w, grid, next_tetromino_shape)
      else: # game over scene
         grid.reset_scene() # remove the existing tetrominos in grid
         first_tetromino_shape = generate_next_tetromino_type()
         current_tetromino = create_tetromino(first_tetromino_shape)
         grid.current_tetromino = current_tetromino
         # create and show the next tetromino as a display
         next_tetromino_shape = generate_next_tetromino_type()
         next_tetromino_display = create_tetromino(next_tetromino_shape)
         grid.display_tetromino = next_tetromino_display
         is_game_scene = display_game_over(grid_h, grid_w)
         
         is_game_scene, game_speed = display_game_menu(grid_h, grid_w)
         # clear the queue of the pressed keys for an actual restart
         stddraw.clearKeysTyped()

# Function for generating the rando  m shape for the next tetromino
def generate_next_tetromino_type():
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ 'I', 'O', 'Z', 'J', 'T', 'L', 'S' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   return random_type

# Function for creating a tetromino to enter the game grid from the given type
def create_tetromino(tetromino_type):
   # create and return the tetromino
   tetromino = Tetromino(tetromino_type)
   return tetromino

# Function for creating the canvas for the game
def create_canvas(the_grid_height, the_grid_width, info_grid_width):
   # set the dimensions of the game grid
   info_grid_w = info_grid_width
   grid_h, grid_w = the_grid_height, the_grid_width + info_grid_w
   # set the size of the drawing canvas
   canvas_h, canvas_w = 45 * grid_h, 45 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h) 
   # set the scale of the coordinate system
   stddraw.setXscale(-1.5, grid_w + 0.5)
   stddraw.setYscale(-1.5, grid_h + 0.5)
   # set the dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w - info_grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w - info_grid_w)
   return grid_h, grid_w, grid

# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   start()