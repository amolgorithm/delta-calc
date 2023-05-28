"""DeltaCalc/calculator.py

***The purpose of this project is to create a simple standard calculator application using the tkinter framework***

Copyright (c) 2022- Amol S. All rights reserved.

"""

#imports
from tkinter import * #Using tkinter for this app. Fun fact: Did you know that tkinter means Tk interface?
import tkinter.font as font #font for tkinter text
import math #math will come of importance later on in the program
from functools import partial #as will this
from datetime import datetime #getting current date for logging operations in history
import os


#window dimensions
window_width = 400
window_height = 600


cwd = os.getcwd() + "./" if os.getcwd()[-len("\DeltaCalc"):] == "\DeltaCalc" else os.getcwd() + "./DeltaCalc/"  #current working directory (so that when doing `python DeltaCalc` in terminal, external files are accessible)


#main application related dimensions
textbox_height = 100
default_textbox_content = "0" #default content of result textbox
current_textbox_content = "0" #current content of result textbox
textbox_font_size = 34 #font size of textbox (which will vary based on number of digits in the textbox)
textbox_dynamic_limit = 14
textbox_final_limit = 42 #final limit for number of digits in textbox

button_rows = 8 #button grid rows
button_cols = 4 #button grid columns


previous_settings_file = open(cwd + "settings.txt", "r")

app_color_mode = previous_settings_file.readline().strip()
app_font_family = previous_settings_file.readline()

previous_settings_file.close()


color_modes = {
	"dark": {
		"bg": "#030303",
		"buttonbg1": "#38332d",
		"buttonbg2": "light coral",
		"buttonbg3": "sky blue",
		"buttonabg1": "#28231d",
		"buttonabg2": "crimson",
		"buttonabg3": "dodger blue",
		"textboxbg": "#151922",
		"genfg": "white" #general foreground
		
	},
	"light": {
		"bg": "white",
		"buttonbg1": "#f0f0f0",
		"buttonbg2": "crimson",
		"buttonbg3": "dodger blue",
		"buttonabg1": "light gray",
		"buttonabg2": "light coral",
		"buttonabg3": "sky blue",
		"textboxbg": "white",
		"genfg": "black" #general foreground
	},
	"coffee": {
		"bg": "#1d1711",
		"buttonbg1": "#986f51",
		"buttonbg2": "#8b4325",
		"buttonbg3": "#b8b3b4",
		"buttonabg1": "#5e442b",
		"buttonabg2": "#c27a43",
		"buttonabg3": "#9b9c97",
		"textboxbg": "#3c2d22",
		"genfg": "#f1e8d6" #general foreground
	}
}


root = None # root tkinter window
	

#widgets involved in calculator application
textbox = None
history_button = None
settings_button = None


num1 = 0 #first number of the result
operation_performed = False #boolean that states if operation is performed
operation_to_perform = "+" #operation that will be performed (+, -, *, /, etc.)



#class for calculator calc_buttons
class CalcButton:
	#constructor
	def __init__(self, x, y, width, height, text, font_size, bg, fg, command, actbg):
		#properties and dimensions of a calculator button.
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.font_size = font_size
		self.bg = bg
		self.fg = fg
		self.command = command
		self.actbg = actbg
		self.button = None
		
	#draws the calculator button of a CalcButton object on root window.
	def draw(self):
		global app_font_family
		
		self.button = Button(root, text = self.text, bg = self.bg, fg = self.fg, bd = 0, command = self.command, activebackground = self.actbg, activeforeground = color_modes[app_color_mode]["genfg"])
		self.button.place(x = self.x, y = self.y, width = self.width, height = self.height)
		self.button["font"] = font.Font(family = app_font_family, size = self.font_size)
		
	#destroys (removes) the button widget of a CalcButton object.
	def destroy(self):
		self.button.destroy()




calc_buttons = {} #dictionary of calculator calc_buttons involved in program
calc_button_icons = ["xʸ", "√x", "ⁿ√x", "mod", "sin", "cos", "tan", "log", "sin⁻¹", "cos⁻¹", "tan⁻¹", "10ˣ", "π", "e", "n!", "+", "7", "8", "9", "-", "4", "5", "6", "x", "1", "2", "3", "÷", "⌫", "0", ".", "="] #icons of each calculator button



def setup_root_tkwindow(_root):
	global root
	
	root = _root



def settings_window():
	global color_modes
	
	font_families = ['Arial', 'Arial Narrow', 'Century', 'Courier', 'Harrington', 'High Tower Text', 'Microsoft Sans Serif', 'Microsoft Yi Baiti', 'Modern', 'MS Serif', 'Roman', 'Script', 'Segoe Script', 'Segoe UI Light', 'Segoe UI Semibold', 'Segoe UI Symbol', 'Segoe UI', 'Small Fonts', 'System', 'Tahoma', 'Terminal', 'Times New Roman', 'Vivaldi', 'Wingdings']
	
	
	settings_win = Tk()
	settings_win.title("DeltaCalc Settings")
	settings_win.geometry("{0}x{1}".format(window_width, window_height))
	settings_win.configure(bg = color_modes[app_color_mode]["bg"])
	settings_win.iconphoto(False, PhotoImage(file = cwd + "./logos/settings_logo.png", master = settings_win))
	settings_win.resizable(False, False)

	
	darkbutton = None
	lightbutton = None
	coffeebutton = None
	color_mode_label = None
	
	color_mode_label = Label(settings_win, text = "Color Mode:", bg = color_modes[app_color_mode]["bg"], fg = color_modes[app_color_mode]["genfg"], bd = 0, relief=RAISED)
	color_mode_label.place(x = window_width/2 - 40, y = 40)
	
	darkbutton = Button(settings_win, text = "Dark", bg = color_modes["dark"]["buttonbg1"], fg = color_modes["dark"]["genfg"], bd = 0, command = lambda: change_color_mode("dark"), activebackground = color_modes["dark"]["genfg"], activeforeground = color_modes["dark"]["buttonbg1"])
	darkbutton.place(x = 1, y = 60, width = window_width/3 - 2, height = 20)
	
	lightbutton = Button(settings_win, text = "Light", bg = color_modes["light"]["buttonbg1"], fg = color_modes["light"]["genfg"], bd = 0, command = lambda: change_color_mode("light"), activebackground = color_modes["light"]["genfg"], activeforeground = color_modes["light"]["buttonbg1"])
	lightbutton.place(x = window_width/3 + 2, y = 60, width = window_width/3 - 2, height = 20)
	
	coffeebutton = Button(settings_win, text = "Coffee", bg = color_modes["coffee"]["buttonbg1"], fg = color_modes["coffee"]["genfg"], bd = 0, command = lambda: change_color_mode("coffee"), activebackground = color_modes["coffee"]["genfg"], activeforeground = color_modes["coffee"]["buttonbg1"])
	coffeebutton.place(x = window_width/1.5 + 2, y = 60, width = window_width/3 - 2, height = 20)
	

	def change_font_family(given_font: str):
		global app_font_family
		
		
		settings_file_readable = open(cwd + "./settings.txt", "r")
		settings_file_colormode_text = settings_file_readable.readline()
		settings_file_readable.close()
		
		settings_file_editable = open(cwd + "./settings.txt", "w")
		
		settings_file_editable.write(settings_file_colormode_text + given_font)
		settings_file_editable.close()
		
		app_font_family = given_font
		
		destroy_widgets()
		
		setup_calc_buttons()
		draw_calc_buttons()
		draw_textbox(current_textbox_content)
		
		
	
	fontbuttons = []
	font_family_label = None
	
	font_button_y = window_height - 276
	font_button_x = 0
	i = 0
	
	
	font_family_label = Label(settings_win, text = "Font Family:", bg = color_modes[app_color_mode]["bg"], fg = color_modes[app_color_mode]["genfg"], bd = 0, relief=RAISED)
	font_family_label.place(x = window_width/2 - 40, y = font_button_y - 20)
	
	
	for fnt in font_families:
		button_command = partial(change_font_family, fnt)
		
		if i == (len(font_families) // 2):
			font_button_x = window_width/2
			font_button_y = window_height - 276
		
		fontbuttons.append(Button(settings_win, text = fnt, bg = color_modes[app_color_mode]["buttonbg1"], fg = color_modes[app_color_mode]["genfg"], bd = 0, command = button_command, activebackground = color_modes[app_color_mode]["genfg"], activeforeground = color_modes[app_color_mode]["buttonbg1"]))
		fontbuttons[i].place(x = font_button_x, y = font_button_y, width = window_width/2 - 3, height = 20)
		
		font_button_y += 23
		i += 1
		
	
	
	def change_color_mode(given_color: str):
		global app_color_mode, root
		nonlocal fontbuttons, darkbutton, lightbutton, coffeebutton, color_mode_label, font_family_label
		
		if given_color != app_color_mode:
			
			settings_file_readable = open(cwd + "./settings.txt", "r")
			
			settings_file_readable.readline()
			
			settings_file_colormode_text = settings_file_readable.readline()
			settings_file_readable.close()
			
			settings_file_editable = open(cwd + "./settings.txt", "w")
			
			settings_file_editable.write(given_color + "\n" + settings_file_colormode_text)
			settings_file_editable.close()
			
			root.withdraw()
			settings_win.withdraw()
			
			app_color_mode = given_color
			
			destroy_widgets()
			
			root["bg"] = color_modes[app_color_mode]["bg"]
			
			setup_calc_buttons()
			draw_calc_buttons()
			draw_textbox(current_textbox_content)
			
			settings_win["bg"] = color_modes[app_color_mode]["bg"]
			
			if darkbutton != None and lightbutton != None and coffeebutton != None and color_mode_label != None:
				darkbutton.destroy()
				lightbutton.destroy()
				color_mode_label.destroy()
				
			if fontbuttons:
				for i in range(0, len(fontbuttons)):
					fontbuttons[i].destroy()
					
				fontbuttons.clear()
			
			
			color_mode_label = Label(settings_win, text="Color Mode:", bg = color_modes[app_color_mode]["bg"], fg = color_modes[app_color_mode]["genfg"], bd = 0, relief=RAISED)
			color_mode_label.place(x = window_width/2 - 40, y = 40)
	
			darkbutton = Button(settings_win, text = "Dark", bg = color_modes["dark"]["buttonbg1"], fg = color_modes["dark"]["genfg"], bd = 0, command = lambda: change_color_mode("dark"), activebackground = color_modes["dark"]["genfg"], activeforeground = color_modes["dark"]["buttonbg1"])
			darkbutton.place(x = 1, y = 60, width = window_width/3 - 2, height = 20)
			
			lightbutton = Button(settings_win, text = "Light", bg = color_modes["light"]["buttonbg1"], fg = color_modes["light"]["genfg"], bd = 0, command = lambda: change_color_mode("light"), activebackground = color_modes["light"]["genfg"], activeforeground = color_modes["light"]["buttonbg1"])
			lightbutton.place(x = window_width/3 + 2, y = 60, width = window_width/3 - 2, height = 20)
			
			coffeebutton = Button(settings_win, text = "Coffee", bg = color_modes["coffee"]["buttonbg1"], fg = color_modes["coffee"]["genfg"], bd = 0, command = lambda: change_color_mode("coffee"), activebackground = color_modes["coffee"]["genfg"], activeforeground = color_modes["coffee"]["buttonbg1"])
			coffeebutton.place(x = window_width/1.5 + 2, y = 60, width = window_width/3 - 2, height = 20)
			
			
			font_button_y = window_height - 276
			font_button_x = 0
			i = 0
			
			font_family_label = Label(settings_win, text = "Font Family:", bg = color_modes[app_color_mode]["bg"], fg = color_modes[app_color_mode]["genfg"], bd = 0, relief=RAISED)
			font_family_label.place(x = window_width/2 - 40, y = font_button_y - 20)
			
			for fnt in font_families:
				button_command = partial(change_font_family, fnt)
				
				if i == (len(font_families) // 2):
					font_button_x = window_width/2
					font_button_y = window_height - 276
				
				fontbuttons.append(Button(settings_win, text = fnt, bg = color_modes[app_color_mode]["buttonbg1"], fg = color_modes[app_color_mode]["genfg"], bd = 0, command = button_command, activebackground = color_modes[app_color_mode]["genfg"], activeforeground = color_modes[app_color_mode]["buttonbg1"]))
				fontbuttons[i].place(x = font_button_x, y = font_button_y, width = window_width/2 - 3, height = 20)
				
				font_button_y += 23
				i += 1
				
				
			root.after(0, root.deiconify)
			settings_win.after(0, settings_win.deiconify)

		
	settings_win.mainloop()
	


#creates a new window for the history of operations done by the calculator.
#This data is stored in a csv file
def history_window():
	
	#creates new window
	history_win = Tk()
	history_win.title("History of operations")
	history_win.geometry("{0}x{1}".format(window_width, window_height))
	history_win.configure(bg = color_modes[app_color_mode]["bg"])
	history_win.iconphoto(False, PhotoImage(file = cwd + "./logos/history_logo.png", master = history_win))
	history_win.resizable(False, True)
	
	#opens the file that stores the history of operations data
	history_file_readable = open(cwd + "./history.txt", "r", encoding = "utf-8")
	
	#The 3 lines below flip the sequence of the data, so that the recent is at the top
	hfr_list = history_file_readable.read().split("\n")
	hfr_list.reverse()
	history_file_readable_reverse_order = "\n".join(hfr_list)
	
	#draws the history file's contents as text on the screen
	operations_history_text = Text(history_win, bg = color_modes[app_color_mode]["bg"], fg = color_modes[app_color_mode]["genfg"], font=("Arial 15"))
	operations_history_text.insert(END, history_file_readable_reverse_order)
	operations_history_text.place(x = 0, y = 0, width = window_width, height = window_height)
	
	history_win.mainloop()




#returns the result after an operation between two numbers, given the operation (+, -, *, /, etc.), or a function, given a number (sin, cos, tan)
def operation(oper: str, num1, num2):
	result = 0 #sets result to 0
	
	if oper == "+": #if oper is + case
		result = num1 + num2
		
	elif oper == "-": #if oper is - case
		result = num1 - num2
	
	elif oper == "x": #if oper is * case
		result = num1 * num2
		
	elif oper == "÷": #if oper is / case
		result = num1 / num2
		
	elif oper == "mod": #if oper is % case
		result = num1 % num2
	
	elif oper == "**": #if oper is ** case
		result = num1 ** num2
	
	elif oper == "√x": #if oper is sqrt case
		result = math.sqrt(num1)
		
	elif oper == "ⁿ√x": #if oper is nth root case
		result = abs(num1) ** (1 / num2)
		
		if num2 % 2 == 1 and num1 < 0:
			result = -result
			
	elif oper == "n!": #if oper is factorial case
		result = 1
		
		for i in range(1, num1 + 1):
			result *= i
			
	elif oper == "sin": #if oper is sin case
		result = math.sin(num1)
		
	elif oper == "cos": #if oper is cos case
		result = math.cos(num1)
		
	elif oper == "tan": #if oper is tan case
		result = math.tan(num1)
		
	elif oper == "log": #if oper is log case
		result = math.log(num1)
		
	elif oper == "sin⁻¹": #if oper is asin case
		result = math.asin(num1)
		
	elif oper == "cos⁻¹": #if oper is acos case
		result = math.acos(num1)
		
	elif oper == "tan⁻¹": #if oper is atan case
		result = math.atan(num1)
		
	elif oper == "10ˣ": #if oper is 10 ** x case
		result = 10 ** num1
		
	 
	#this if statment is saying if result is in integer, remove the .0 that follows
	if math.ceil(result) == result: # math.ceil(ABC.DFE) equals ABC.DFE only when .DFE equals .000, which means that it is an integer
		result = int(result)
		
	return result    #returning the result



#adds or sets given num to the textbox content
def add_number_to_textbox(num: str): #num is the digit or '.' in string form
	global current_textbox_content, default_textbox_content  #accessing two needed global variables
	
	if num == "π":
		draw_textbox(str(math.pi))
		current_textbox_content = str(math.pi)
	elif num == "e":
		draw_textbox(str(math.e))
		current_textbox_content = str(math.e)
	elif num == "." and ("." not in current_textbox_content): #if num equals '.' and the current textbox content doesn't already contain it, '.' is appended to current textbox content
		draw_textbox(current_textbox_content + num)
		current_textbox_content += num
	elif num == "-" and ("-" not in current_textbox_content) and (current_textbox_content == default_textbox_content): #if num equals '-' and the current textbox content doesn't already contain it, '-' is appended to current textbox content
		draw_textbox(num)
		current_textbox_content = num
	elif num.isnumeric(): #else if num is numeric, it is a digit,
		if current_textbox_content == default_textbox_content: #if the current textbox content equals 0, the current textbox content becomes num, because you cannot have something like 08
			draw_textbox(num)
			current_textbox_content = num
		else: # else, num is appened to the current textbox content
			draw_textbox(current_textbox_content + num)
			current_textbox_content += num



def perform_operation(index: int):
	global current_textbox_content, default_textbox_content, num1, operation_to_perform, operation_performed
	
	if not operation_performed and (calc_button_icons[index] != "=" and calc_button_icons[index] != "⌫"):
		if "." in current_textbox_content:
			num1 = float(current_textbox_content)
		else:
			num1 = int(current_textbox_content)
			
		current_textbox_content = default_textbox_content
		operation_to_perform = calc_button_icons[index]
		
		if calc_button_icons[index] == "√x":
			current_textbox_content = str(operation("√x", num1, 0))
			
			history_file_appendable = open(cwd + "./history.txt", "a", encoding = "utf-8")
			history_file_appendable.write("Sqrtof " + str(num1) + " = " + str(operation(operation_to_perform, num1, 0)) + "  " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
			history_file_appendable.close()
			
			operation_performed = False
			operation_to_perform = "+"
			num1 = 0
			draw_textbox(current_textbox_content)
			
		elif calc_button_icons[index] == "sin" or calc_button_icons[index] == "cos" or calc_button_icons[index] == "tan" or calc_button_icons[index] == "log" or calc_button_icons[index] == "sin⁻¹" or calc_button_icons[index] == "cos⁻¹" or calc_button_icons[index] == "tan⁻¹" or calc_button_icons[index] == "10ˣ":
			current_textbox_content = str(operation(calc_button_icons[index], num1, 0))
			
			history_file_appendable = open(cwd + "./history.txt", "a", encoding = "utf-8")
			history_file_appendable.write("{}(".format(operation_to_perform) + str(num1) + ") = " + str(operation(operation_to_perform, num1, 0)) + "  " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
			history_file_appendable.close()
			
			operation_performed = False
			operation_to_perform = "+"
			num1 = 0
			draw_textbox(current_textbox_content)
			
		elif calc_button_icons[index] == "n!":
			current_textbox_content = str(operation("n!", num1, 0))
			
			history_file_appendable = open(cwd + "./history.txt", "a", encoding = "utf-8")
			history_file_appendable.write(str(num1) + "! = " + str(operation(operation_to_perform, num1, 0)) + "  " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
			history_file_appendable.close()
			
			operation_performed = False
			operation_to_perform = "+"
			num1 = 0
			draw_textbox(current_textbox_content)
		
		elif calc_button_icons[index] == "xʸ":
			operation_to_perform = "**"
			
		
	elif calc_button_icons[index] == "=":
		textbox_number_form = 0 
		
		if "." in current_textbox_content:
			textbox_number_form = float(current_textbox_content)
		else:
			textbox_number_form = int(current_textbox_content)
		
		current_textbox_content = str(operation(operation_to_perform, num1, textbox_number_form))
		
		history_file_appendable = open(cwd + "./history.txt", "a", encoding = "utf-8")
		history_file_appendable.write(str(num1) + " " + operation_to_perform + " " + str(textbox_number_form) + " = " + str(operation(operation_to_perform, num1, textbox_number_form)) + "  " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
		history_file_appendable.close()
		
		
		
		operation_performed = False
		operation_to_perform = "+"
		num1 = 0
		draw_textbox(current_textbox_content)
		
	elif calc_button_icons[index] == "⌫":
		current_textbox_content = current_textbox_content[:-1]
		
		if len(current_textbox_content) < 1:
			current_textbox_content = default_textbox_content
		
		draw_textbox(current_textbox_content)



#sets up the buttons in the calculator application
def setup_calc_buttons():
	global calc_buttons, calc_button_icons
	
	button_bg = ""
	button_fg = ""
	button_actbg = ""
	
	button_command = None
	
	
	for i in range(0, len(calc_button_icons)):
		if i == len(calc_button_icons)-1:
			button_bg = color_modes[app_color_mode]["buttonbg3"]
			button_fg = color_modes[app_color_mode]["genfg"]
			button_actbg = color_modes[app_color_mode]["buttonabg3"]
			
		elif i == len(calc_button_icons)-4:
			button_bg = color_modes[app_color_mode]["buttonbg2"]
			button_fg = color_modes[app_color_mode]["genfg"]
			button_actbg = color_modes[app_color_mode]["buttonabg2"]
		
		else:
			button_bg = color_modes[app_color_mode]["buttonbg1"]
			button_fg = color_modes[app_color_mode]["genfg"]
			button_actbg = color_modes[app_color_mode]["buttonabg1"]
			
		if calc_button_icons[i].isnumeric() or calc_button_icons[i] == "." or calc_button_icons[i] == "π" or calc_button_icons[i] == "e" or (calc_button_icons[i] == "-" and current_textbox_content == default_textbox_content):
			button_command = partial(add_number_to_textbox, calc_button_icons[i])
		else:
			button_command = partial(perform_operation, i)
			
		calc_buttons[calc_button_icons[i]] = CalcButton(2 + (i % button_cols) * (window_width/button_cols), textbox_height + (i // 4) * ((window_height - textbox_height) / button_rows), window_width/button_cols - 3, (window_height - textbox_height) / button_rows - 3, calc_button_icons[i], 25, button_bg, button_fg, button_command, button_actbg)
			

#draws the buttons in the calculator application
def draw_calc_buttons():
	global calc_buttons, calc_button_icons
	
	for j in range(0, len(calc_button_icons)):
		calc_buttons[calc_button_icons[j]].draw()


#draws the result textbox
def draw_textbox(txt: str):
	global textbox, history_button, settings_button, textbox_font_size, textbox_dynamic_limit, app_font_family
	
	if len(txt) % textbox_dynamic_limit == 0:
		textbox_font_size = int(textbox_font_size / 2)
		textbox_dynamic_limit *= 2
		
	if (len(txt) >= textbox_final_limit):
		txt = "ERR! Too long!"
		textbox_font_size = 34
	
	textbox = Entry(root, bg = color_modes[app_color_mode]["textboxbg"], fg = color_modes[app_color_mode]["genfg"], justify = RIGHT, bd = 0)
	textbox["font"] = font.Font(family = app_font_family, size = textbox_font_size)
	textbox.insert(END, txt)
	textbox.place(x = 0, y = 0, width = window_width, height = textbox_height)

	#History Button	
	history_button = Button(root, text = "Hist", bg = color_modes[app_color_mode]["buttonbg1"], fg = color_modes[app_color_mode]["genfg"], bd = 0, command = history_window)
	history_button.place(x = 0, y = 0, width = 40, height = 40)
	history_button["font"] = font.Font(family = app_font_family, size = 10)
	
	#Settings Button	
	settings_button = Button(root, text = "Set", bg = color_modes[app_color_mode]["buttonbg1"], fg = color_modes[app_color_mode]["genfg"], bd = 0, command = settings_window)
	settings_button.place(x = 42, y = 0, width = 40, height = 40)
	settings_button["font"] = font.Font(family = app_font_family, size = 10)



#destroys the widgets in the root window
def destroy_widgets():
	textbox.destroy()
	history_button.destroy()
	settings_button.destroy()
	
	for b in calc_buttons:
		calc_buttons[b].destroy()
		
	calc_buttons.clear()
	
	
