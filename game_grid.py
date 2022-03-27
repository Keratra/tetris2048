import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import copy # needed for deep copying

# Class used for modelling the game grid
class GameGrid:
	# Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles landed onto the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      self.display_tetromino = None
      self.prediction_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(205,193,180)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(187,172,161) 
      self.boundary_color = Color(119, 110, 101)

      # use this for the information part of the grid: Color(119, 110, 101)
           
      # thickness values used for the grid lines and the boundaries
      self.line_thickness = 0.008
      self.box_thickness = 1 * self.line_thickness

   def predict(self):
      self.prediction_tetromino = copy.deepcopy(self.current_tetromino)
      while self.prediction_tetromino.can_be_moved("down", self):
         self.prediction_tetromino.move("down", self)
      self.prediction_tetromino.draw(pred = True)

   # Method used for resetting the game environment
   def reset_scene(self):
      self.tile_matrix = np.full((self.grid_height, self.grid_width), None)
      self.current_tetromino = None
      self.display_tetromino = None
      self.game_over = False

   # Method used for displaying the game grid
   def display(self, speed=100):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current/active tetromino if it is not None (the case when the 
      # game grid is updated)
      if self.current_tetromino is not None:
         self.predict()
         self.current_tetromino.draw()
      if self.display_tetromino is not None:
         self.display_tetromino.bottom_left_cell = Point()
         self.display_tetromino.bottom_left_cell.y = 2
         self.display_tetromino.bottom_left_cell.x = self.grid_width + 1
         self.display_tetromino.draw()
      # draw a box around the game grid 
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(speed)
         
   # Method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value            
      
   # Method for drawing the boundaries around the game grid 
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible 
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.6, -0.6
      stddraw.rectangle(pos_x, pos_y, self.grid_width + 0.1, self.grid_height + 0.1)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column 
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have 
      # tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None
      
   # Method used for checking whether the cell with given row and column indexes 
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   def is_row_full(self, row):
      for col in range(self.grid_width):
         if self.tile_matrix[row][col] is None:
            return False
      return True
   #remove if row is full

   def remove_row(self, row):
      for col in range(self.grid_width):
         self.tile_matrix[row][col] = None

   def shift_rows_down(self, row):
      for i in range(row + 1, self.grid_height):
         for col in range(self.grid_width):
            print('col:', col)
            self.tile_matrix[i - 1][col] = self.tile_matrix[i][col]
            self.tile_matrix[i][col] = None

   def remove_full_rows(self):
      for row in range(self.grid_height):
         while self.is_row_full(row):
            self.remove_row(row)
            self.shift_rows_down(row)

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid 
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):            
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      self.remove_full_rows()
      # return the game_over flag
      return self.game_over