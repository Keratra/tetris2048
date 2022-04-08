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
   font_family = "Aharoni"

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self):
      # set the number on the tile
      self.number = 2 if random.randint(0,10) < 8 else 4
      # set the colors of the tile
      self.background_color = Color(238, 228, 218) # background (tile) color
      self.foreground_color = Color(119, 110, 101) # foreground (number) color
      self.box_color = Color(119, 110, 101) # box (boundary) color
      self.font_size = 24
      self.is_connected = False
      self.colors = {
         2: {
            'color': Color(238, 228, 218),
            'font': 24
            },
         4: {
            'color': Color(238, 225, 201),
            'font': 24
            },
         8: {
            'color': Color(243, 178, 122),
            'font': 24
            },
         16: {
            'color': Color(246, 150, 100),
            'font': 24
            },
         32: {
            'color': Color(247, 124, 95),
            'font': 24
            },
         64: {
            'color': Color(247, 95, 59),
            'font': 24
            },
         128: {
            'color': Color(237, 208, 115),
            'font': 20
            },
         256: {
            'color': Color(237, 204, 98),
            'font': 20
            },
         512: {
            'color': Color(237, 201, 80),
            'font': 20
            },
         1024: {
            'color': Color(237, 197, 63),
            'font': 16
            },
         2048: {
            'color': Color(237, 194, 46),
            'font': 16
            }
      }

   # change background color according to the number on the tile
   def update_color(self):

      if self.number in self.colors:
         self.font_size = self.colors[self.number]['font']
         return self.colors[self.number]['color']
      else:
         self.foreground_color = Color(240,240,240)
         self.font_size = 16
         return Color(60, 58, 51)

   # Method for drawing the tile
   def draw(self, position, length = 1.05, is_pred = False, next = False):
      # draw the tile as a filled square
      if is_pred:
         stddraw.setPenColor(Color(42, 69, 99))
      else:
         self.background_color = self.update_color()
         stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      if is_pred:
         stddraw.setPenColor(Color(151, 178, 199))
      else:
         stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      if not next:
         # draw the number on the tile
         stddraw.setPenColor(self.foreground_color)
         stddraw.setFontFamily(Tile.font_family)
         stddraw.setFontSize(self.font_size)
         stddraw.text(position.x, position.y, str(self.number))
      stddraw.setPenRadius()  # reset the pen radius to its default value