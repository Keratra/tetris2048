import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
import random

# Class used for modeling numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 24

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self):
      # set the number on the tile
      self.number = 2 if random.randint(0,10) < 8 else 4
      # set the colors of the tile
      self.background_color = Color(238, 228, 218) # background (tile) color
      self.foreground_color = Color(119, 110, 101) # foreground (number) color
      self.box_color = Color(187,172,161) # box (boundary) color

   # Method for drawing the tile
   def draw(self, position, length = 1, is_pred = False):
      if is_pred:
         # draw the tile as a filled square
         stddraw.setPenColor(Color(42, 69, 99))
         stddraw.filledSquare(position.x, position.y, length / 2)
         # draw the bounding box around the tile as a square
         stddraw.setPenColor(Color(151, 178, 199))
         stddraw.setPenRadius(Tile.boundary_thickness)
         stddraw.square(position.x, position.y, length / 2)
         stddraw.setPenRadius()  # reset the pen radius to its default value
         # draw the number on the tile
         stddraw.setPenColor(self.foreground_color)
         stddraw.setFontFamily(Tile.font_family)
         stddraw.setFontSize(Tile.font_size)
         stddraw.text(position.x, position.y, str(self.number))
         return
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))