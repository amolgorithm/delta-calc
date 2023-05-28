from tkinter import * #Using tkinter for this app. Fun fact: Did you know that tkinter means Tk interface?
import tkinter.font as font #font for tkinter text


"""DeltaCalc/calculator.py

Copyright (c) 2022- Amol S. All rights reserved.

"""
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
