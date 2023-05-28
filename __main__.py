"""DeltaCalc/__main__.py

***The purpose of this project is to create a simple standard calculator application using the tkinter framework***

Copyright (c) 2022- Amol S. All rights reserved.

"""


#imports
from tkinter import * #Using tkinter for this app. Fun fact: Did you know that tkinter means Tk interface?
import calculator  #personal module
import os



#window dimensions
window_width = calculator.window_width
window_height = calculator.window_height


cwd = os.getcwd() + "./" if os.getcwd()[-len("\DeltaCalc"):] == "\DeltaCalc" else os.getcwd() + "./DeltaCalc/"  #current working directory (so that when doing `python DeltaCalc` in terminal, external files are accessible)


root = Tk() # root tkinter window

root.withdraw() #hiding window to hide glitch that comes when preloading

root.title("DeltaCalc") #title of app
root.geometry("{0}x{1}".format(window_width, window_height)) #setting the window dimensions
root.resizable(False, False) #disabling user's window resizing ability
root.iconphoto(False, PhotoImage(file = cwd + "./logos/deltacalc_logo.png")) #setting the icon/logo of my project
root.configure(bg = calculator.color_modes[calculator.app_color_mode]["bg"]) #background color

root.after(0, root.deiconify) #unhiding window instantly


	
if __name__ == "__main__":
	calculator.setup_root_tkwindow(root)
	calculator.setup_calc_buttons()
	calculator.draw_calc_buttons()
	calculator.draw_textbox(calculator.default_textbox_content)
	
	root.mainloop()
