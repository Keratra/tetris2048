import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes

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
   button_main_blc_x, button_main_blc_y = img_center_x - button_w / 2, 4
   # coordinates of the bottom left corner of the game difficulty buttons
   button_easy_blc_x, button_easy_blc_y     = img_center_x - button_w / 4 - 3, 2
   button_normal_blc_x, button_normal_blc_y = img_center_x - button_w / 4, 4
   button_hard_blc_x, button_hard_blc_y     = img_center_x - button_w / 4 + 3, 6
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_main_blc_x, button_main_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Aharoni")
   stddraw.setFontSize(40)
   stddraw.setPenColor(text_color)
   text_to_display = "Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   game_speed = 250
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
         if mouse_x >= button_main_blc_x and mouse_x <= button_main_blc_x + button_w:
            if mouse_y >= button_main_blc_y and mouse_y <= button_main_blc_y + button_h:
               # clear the background canvas to background_color
               stddraw.clear(background_color)
               # get the directory in which this python code file is placed
               current_dir = os.path.dirname(os.path.realpath(__file__))
               # path of the image file
               img_file = current_dir + "/images/howtoplay-controls-v2.png"
               # image is represented using the Picture class
               image_to_display = Picture(img_file)
               # display the image
               stddraw.picture(image_to_display, img_center_x, img_center_y + 2)
               # difficulty buttons
               stddraw.setPenColor(button_color)
               stddraw.filledRectangle(button_easy_blc_x - 0.5, button_easy_blc_y + 0.5, button_w / 2, button_h)
               stddraw.filledRectangle(button_normal_blc_x,     button_normal_blc_y,     button_w / 2, button_h)
               stddraw.filledRectangle(button_hard_blc_x + 0.5, button_hard_blc_y - 0.5, button_w / 2, button_h)
               stddraw.setFontSize(36)
               stddraw.setPenColor(text_color)
               stddraw.text(img_center_x - 3.5, 3.5, "Easy")
               stddraw.text(img_center_x,         5, "Normal")
               stddraw.text(img_center_x + 3.5, 6.5, "Hard")
               stddraw.show(50)
               while True:
                  stddraw.show(50)
                  # check if the mouse has been left-clicked on the button
                  if stddraw.mousePressed():
                     # get the x and y coordinates of the location at which the mouse has 
                     # most recently been left-clicked  
                     mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                     # check if these coordinates are inside the button
                     if mouse_x >= button_easy_blc_x and mouse_x <= button_easy_blc_x + button_w / 2:
                        if mouse_y >= button_easy_blc_y and mouse_y <= button_easy_blc_y + button_h:
                           # start the game with the difficulty level "easy"
                           game_speed = 300
                           break
                     if mouse_x >= button_normal_blc_x and mouse_x <= button_normal_blc_x + button_w / 2:
                        if mouse_y >= button_normal_blc_y and mouse_y <= button_normal_blc_y + button_h:
                           # start the game with the difficulty level "normal"
                           game_speed = 250
                           break
                     if mouse_x >= button_hard_blc_x and mouse_x <= button_hard_blc_x + button_w / 2:
                        if mouse_y >= button_hard_blc_y and mouse_y <= button_hard_blc_y + button_h:
                           # start the game with the difficulty level "hard"
                           game_speed = 150
                           break
               break # break the loop to end the method and start the game
   return True, game_speed

# Function for displaying a simple menu after the game is over
def display_game_over(grid_height, grid_width, current_score):
   # colors used for the menu
   background_color = Color(238, 228, 218)
   button_color = Color(119, 110, 101)
   text_color = Color(238, 228, 218)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # dimensions of the start game button
   button_w, button_h = grid_width - 8, 2
   # coordinates of the bottom left corner of the start game button 
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 6
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Aharoni")
   stddraw.setFontSize(40)
   stddraw.setPenColor(text_color)
   text_to_display = "Restart"
   stddraw.text(img_center_x, 7, text_to_display)
   text_to_show = "Game Over"
   stddraw.setPenColor(button_color)
   stddraw.setFontSize(72)
   stddraw.text(img_center_x, grid_height*3//4 - 1, text_to_show)
   stddraw.setFontSize(24)
   
   # check if highscore.txt exists, if not create it
   if not os.path.exists("highscore.txt"):
      with open("highscore.txt", "w") as f:
         f.write("0")
   # read the highscore from the file
   with open("highscore.txt", "r") as f:
      highscore = int(f.read())

   # check if the current score is greater than the highscore
   if current_score > highscore:
      with open("highscore.txt", "w") as f:
            # update the highscore
            highscore = current_score
            # write the new highscore to the file
            f.write(str(highscore))
   stddraw.setFontSize(36)
   stddraw.text(img_center_x, grid_height*3//4 - 3.5, "Score: " + str(current_score))
   stddraw.text(img_center_x, grid_height*3//4 - 4.5, "High Score: " + str(highscore))
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
               do_restart = True
               break # break the loop to end the method and start the game
   return True

# Function for pause screen
def display_pause_menu(grid_height, grid_width):
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
   # dimensions of the start game button
   button_w, button_h = grid_width - 8, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   button_res_blc_x, button_res_blc_y = img_center_x - button_w / 2, 1
   # display the start game button as a filled rectangle

   stddraw.setFontSize(144)
   stddraw.text(img_center_x, img_center_y, "Paused")

   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   stddraw.filledRectangle(button_res_blc_x, button_res_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Aharoni")
   stddraw.setFontSize(40)
   stddraw.setPenColor(text_color)
   text_to_display = "Resume"
   stddraw.text(img_center_x, 5, text_to_display)
   stddraw.text(img_center_x, 2, "Restart")

   do_reset = False

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
               do_reset = False
               break # break the loop to end the method and start the game
         if mouse_x >= button_res_blc_x and mouse_x <= button_res_blc_x + button_w:
            if mouse_y >= button_res_blc_y and mouse_y <= button_res_blc_y + button_h:
               do_reset = True
               break # break the loop to end the method and start the game
   return do_reset
