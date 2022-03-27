""" from tkinter import E """
import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():
   # set the dimensions of the game grid
   info_grid_w = 4
   grid_h, grid_w = 20, 12 + info_grid_w
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
   # create the first tetromino to enter the game grid 
   # by using the create_tetromino function defined below
   first_tetromino_shape = generate_next_tetromino_type(grid_h, grid_w)
   current_tetromino = create_tetromino(grid_h, grid_w, first_tetromino_shape)
   grid.current_tetromino = current_tetromino
   # create and show the next tetromino as a display
   next_tetromino_shape = generate_next_tetromino_type(grid_h, grid_w)
   next_tetromino_display = create_tetromino(grid_h, grid_w, next_tetromino_shape)
   grid.display_tetromino = next_tetromino_display

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   is_game_scene = display_game_menu(grid_h, grid_w)
   game_speed = 250

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
            
            #print("Key:", key_typed)

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
            elif key_typed == "tab":
               game_speed = 250
            elif key_typed == "left shift":
               game_speed = 120
            # clear the queue of the pressed keys for a smoother interaction
            stddraw.clearKeysTyped()

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
            current_tetromino = create_tetromino(grid_h, grid_w, next_tetromino_shape)
            grid.current_tetromino = current_tetromino
            # generate the next next tetromino. :D 
            next_tetromino_shape = generate_next_tetromino_type(grid_h, grid_w)
            next_tetromino_display = create_tetromino(grid_h, grid_w, next_tetromino_shape)
            grid.display_tetromino = next_tetromino_display
         # display the game grid and the current tetromino
         grid.display(game_speed)
      else: # game over scene
         grid.reset_scene() # remove the existing tetrominos in grid
         first_tetromino_shape = generate_next_tetromino_type(grid_h, grid_w)
         current_tetromino = create_tetromino(grid_h, grid_w, first_tetromino_shape)
         grid.current_tetromino = current_tetromino
         # create and show the next tetromino as a display
         next_tetromino_shape = generate_next_tetromino_type(grid_h, grid_w)
         next_tetromino_display = create_tetromino(grid_h, grid_w, next_tetromino_shape)
         grid.display_tetromino = next_tetromino_display
         is_game_scene = display_game_over(grid_h, grid_w)
         # clear the queue of the pressed keys for an actual restart
         stddraw.clearKeysTyped()

   

# Function for generating the random shape for the next tetromino
def generate_next_tetromino_type(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   #[ 'I', 'O', 'Z', 'J', 'T', 'L', 'S' ]
   tetromino_types = [ 'I', 'O', 'Z', 'J', 'T', 'L', 'S' ]
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   return random_type

# Function for creating a tetromino to enter the game grid from the given type
def create_tetromino(grid_height, grid_width, tetromino_type):
   # create and return the tetromino
   tetromino = Tetromino(tetromino_type)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(238, 228, 218)
   button_color = Color(119, 110, 101)
   text_color = Color(238, 228, 218)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 8, 2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has 
         # most recently been left-clicked  
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
               break # break the loop to end the method and start the game
   return True

# Function for displaying a simple menu after the game is over
def display_game_over(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(238, 228, 218)
   button_color = Color(119, 110, 101)
   text_color = Color(238, 228, 218)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 8, 2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Restart"
   stddraw.text(img_center_x, 5, text_to_display)
   text_to_show = "GAME OVER"
   stddraw.setPenColor(button_color)
   stddraw.setFontSize(72)
   stddraw.text(img_center_x, 8, text_to_show)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has 
         # most recently been left-clicked  
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h: 
               break # break the loop to end the method and start the game
   return True

# start() function is specified as the entry point (main function) from which 
# the program starts execution
if __name__== '__main__':
   start()