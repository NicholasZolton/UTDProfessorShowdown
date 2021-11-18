import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import Nebula
from ratemyprof_api import RMPHolder
import re
from Grades import Grades

class App(ttk.Frame):
	def __init__(self, parent):
		ttk.Frame.__init__(self)

		# Rows/Column setup
		self.columnconfigure(index=0, weight=1)
		self.rowconfigure(index=0, weight=1)
		self.rowconfigure(index=1, weight=1)

		# Lists
		self.option_menu_list = ['', 'Combined', 'Rating', 'Grades']
		self.setup()

	def setup(self):
		self.menubar()
		self.controls()

	def menubar(self):
		self.menubar = tk.Menu(root)

		# Advanced
		advanced = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label='Advanced', menu=advanced)
		advanced.add_command(label='Placeholder', command=None)
		advanced.add_separator()
		advanced.add_command(label='Update RateMyProfessor')

		# About
		about = tk.Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label='About', menu=about)
		about.add_command(label='GitHub', command=None)
		
		# Draw menu bar
		root.config(menu=self.menubar)
		self.menubar = tk.Menu(root)
	
	def controls(self):
		# Controls frame
		self.controls_frame = ttk.Frame(self, padding=(10, 10))
		self.controls_frame.grid(row=0, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

		# Classcode PlaceholderEntry
		style = ttk.Style(root)
		style.configure("Placeholder.TEntry", foreground="#d5d5d5")
		self.classcode_entry = self.PlaceholderEntry(self.controls_frame, "Search for a class")
		self.classcode_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

		# Classcode Submit button
		self.classcode_submit = ttk.Button(self.controls_frame, text='Search')
		self.classcode_submit.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

		# Classcode Label
		self.classcode_label = ttk.Label(self.controls_frame, text="Class code (ex: 'CS 2305')", font=('calibre', 10, 'normal'))
		self.classcode_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

		# Sort dropdown
		self.optionmenu = ttk.OptionMenu(
			self.controls_frame, self.sort_var, *self.option_menu_list, command=self.test
		)
		self.optionmenu.grid(row=0, column=4, padx=5, pady=5)

	class PlaceholderEntry(ttk.Entry):
		def __init__(self, container, placeholder, *args, **kwargs):
			super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
			self.placeholder = placeholder

			self.insert("0", self.placeholder)
			self.bind("<FocusIn>", self._clear_placeholder)
			self.bind("<FocusOut>", self._add_placeholder)

		def _clear_placeholder(self, e):
			if self["style"] == "Placeholder.TEntry":
				self.delete("0", "end")
				self["style"] = "TEntry"

		def _add_placeholder(self, e):
			if not self.get():
				self.insert("0", self.placeholder)
				self["style"] = "Placeholder.TEntry"


if __name__ == "__main__":
	root = tk.Tk()
	root.title("UTD Professor Compare")

	# Theme setup
	root.tk.call("source", "azure.tcl")
	root.tk.call("set_theme", "light")

	app = App(root)
	app.pack(fill="both", expand=True)

	# Set a minsize for the window, and place it in the middle
	root.update()
	root.minsize(root.winfo_width(), root.winfo_height())
	x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
	y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
	root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

	root.mainloop()