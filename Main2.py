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
		self.sort_var = tk.StringVar(value=self.option_menu_list[1])
		self.table = []

		# vars
		self.professorname_var = tk.StringVar()
		self.classnum_var = tk.StringVar()
		self.class2_var = tk.StringVar()
		self.className = tk.StringVar()
		self.sort_var = tk.StringVar(value=self.option_menu_list[1])

		self.treeview_data = [
			("", 1, "Parent", ("Item 1", "Value 1")),
			(1, 2, "Child", ("Subitem 1.1", "Value 1.1")),
			(1, 3, "Child", ("Subitem 1.2", "Value 1.2")),
			(1, 4, "Child", ("Subitem 1.3", "Value 1.3")),
			(1, 5, "Child", ("Subitem 1.4", "Value 1.4")),
			("", 6, "Parent", ("Item 2", "Value 2")),
			(6, 7, "Child", ("Subitem 2.1", "Value 2.1")),
			(6, 8, "Sub-parent", ("Subitem 2.2", "Value 2.2")),
			(8, 9, "Child", ("Subitem 2.2.1", "Value 2.2.1")),
			(8, 10, "Child", ("Subitem 2.2.2", "Value 2.2.2")),
			(8, 11, "Child", ("Subitem 2.2.3", "Value 2.2.3")),
			(6, 12, "Child", ("Subitem 2.3", "Value 2.3")),
			(6, 13, "Child", ("Subitem 2.4", "Value 2.4")),
			("", 14, "Parent", ("Item 3", "Value 3")),
			(14, 15, "Child", ("Subitem 3.1", "Value 3.1")),
			(14, 16, "Child", ("Subitem 3.2", "Value 3.2")),
			(14, 17, "Child", ("Subitem 3.3", "Value 3.3")),
			(14, 18, "Child", ("Subitem 3.4", "Value 3.4")),
			("", 19, "Parent", ("Item 4", "Value 4")),
			(19, 20, "Child", ("Subitem 4.1", "Value 4.1")),
			(19, 21, "Sub-parent", ("Subitem 4.2", "Value 4.2")),
			(21, 22, "Child", ("Subitem 4.2.1", "Value 4.2.1")),
			(21, 23, "Child", ("Subitem 4.2.2", "Value 4.2.2")),
			(21, 24, "Child", ("Subitem 4.2.3", "Value 4.2.3")),
			(19, 25, "Child", ("Subitem 4.3", "Value 4.3")),
		]

		self.setup()

	def setup(self):
		self.menubar()
		self.controls()
		self.treeview()

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
		style.configure("Placeholder.TEntry", foreground="#808080")
		self.classcode_entry = self.PlaceholderEntry(self.controls_frame, "Search for a class", textvariable=self.classnum_var)
		self.classcode_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

		# Classcode Submit button
		self.classcode_submit = ttk.Button(self.controls_frame, text='Search', command=self.submit)
		self.classcode_submit.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

		# Classcode Label
		self.classcode_label = ttk.Label(self.controls_frame, text="Class code (ex: 'CS 2305')", font=('calibre', 10, 'normal'))
		self.classcode_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

		# Sort dropdown
		self.optionmenu = ttk.OptionMenu(self.controls_frame, self.sort_var, *self.option_menu_list, command=self.test)
		self.optionmenu.grid(row=0, column=4, padx=5, pady=5)

		# Filter PlaceholderEntry
		self.filter_entry = self.PlaceholderEntry(self.controls_frame, "Filter by professors")
		self.filter_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

		# Filter Label
		self.filter_label = ttk.Label(self.controls_frame, text="Filter names (ex: 'Chin, Ntafos, Feng')", font=('calibre', 10, 'normal'))
		self.filter_label.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky="w")
		
		# bindings
		self.classcode_entry.bind("<Tab>", self.focusText2)
		self.filter_entry.bind("<Return>", self.submitBind)
		self.classcode_entry.bind("<Return>", self.submitBind)

	def treeview(self):
		# Treeview frame
		self.view_frame = ttk.Frame(self, padding=(10, 0))
		self.view_frame.grid(row=1, column=0, padx=(10, 10), pady=(0, 20), sticky="nsew")

		# Scrollbar
		self.scrollbar = ttk.Scrollbar(self.view_frame)
		self.scrollbar.pack(side="right", fill="y")

		# Treeview
		self.treeview = ttk.Treeview(self.view_frame,
			selectmode="browse",
			yscrollcommand=self.scrollbar.set,
			columns=(1, 2, 3),
			height=15,
		)
		self.treeview.pack(expand=True, fill="both")
		self.scrollbar.config(command=self.treeview.yview)
		
		# Treeview columns
		self.treeview.column("#0", anchor="w", width=50)
		self.treeview.column(1, anchor="w", width=10)
		self.treeview.column(2, anchor="w", width=10)
		self.treeview.column(3, anchor="w", width=10)

		# Treeview headings
		self.treeview.heading("#0", text="Professor", anchor="center")
		self.treeview.heading(1, text="Combined", anchor="center")
		self.treeview.heading(2, text="Rating", anchor="center")
		self.treeview.heading(3, text="Grades", anchor="center")

		# Insert treeview data
		for item in self.treeview_data:
			self.treeview.insert(
				parent=item[0], index="end", iid=item[1], text=item[2], values=item[3]
			)

	def submitBind(self, test):
		self.submit()

	def focusText2(self, test):
		self.filter_entry.focus()
		return "break"

	def test(self, value):
		self.sort()

	def submit(self):
		# getting name
		self.filterList = re.findall(r'[a-zA-Z]+', self.class2_var.get())
		self.filterList = [each_string.upper() for each_string in self.filterList]
		classnum = self.classnum_var.get()
		matchForPrefix = re.search(r'[a-zA-Z]+', classnum)
		self.pref = classnum[matchForPrefix.start():matchForPrefix.end()]
		matchForClass = re.search(r'[0-9]+', classnum)
		self.num = int(classnum[matchForClass.start():matchForClass.end()])
		self.className.set(Nebula.getCourseNameWithNumber(str(self.pref), self.num))
		# creating list
		self.g1 = Grades(str(self.pref), str(self.num))
		self.sort()

	def sort(self):
		self.table.clear()
		self.text_area.configure(state='normal')
		self.text_area.delete('1.0', tk.END)
		courseName = str(Nebula.getCourseNameWithNumber(str(self.pref), self.num))

		self.text_area.insert(tk.INSERT, courseName + '\n')

		if courseName.find('No results') == -1:
			self.text_area.insert(tk.INSERT, "Professor\t\t\t\tComb.\tRating\tGrades\n\n")

		# if self.sort_var.get() != 'Combined':
		#	 self.text_area.insert(tk.INSERT, "\tClasses") # add classes counter if not default sort
		# self.text_area.insert(tk.INSERT, "\n\n")

		sorted = 0

		if self.sort_var.get() == 'Combined':
			sorted = self.g1.sortedProfsByTrueRating
		elif self.sort_var.get() == 'Grades':
			sorted = self.g1.sortedProfsByMedian
		else:
			sorted = self.g1.sortedProfsByRMP

		for i in sorted:
			valid = True
			if len(self.filterList) > 0:
				found = False
				for j in self.filterList:
					if i.rmpName.upper().find(j) != -1:
						found = True
				if not found:
					valid = False
			if valid:
				tempRating = i.rmpRating
				if tempRating == -1:
					tempRating = 2.5
				if i.trueRating > 75 and i.getMedian() > 80 and tempRating > 2.5:
					self.text_area.insert(tk.INSERT, i.rmpName + "\t\t\t\t", 'good')
				elif (i.trueRating > 75 or i.getMedian() > 80 or tempRating > 2.5) and (not tempRating <= 1 and not i.getMedian() < 70):
					self.text_area.insert(tk.INSERT, i.rmpName + "\t\t\t\t", 'medium')
				else:
					self.text_area.insert(tk.INSERT, i.rmpName + "\t\t\t\t", 'bad')

				if i.trueRating <= 75:
					self.text_area.insert(tk.INSERT, str(round(i.trueRating, 2)) + "\t", 'bad')
				else:
					self.text_area.insert(tk.INSERT, str(round(i.trueRating, 2)) + "\t", 'good')

				add = ""
				if i.rmpRating != -1:
					if i.rmpRating <= 2.5:
						self.text_area.insert(tk.INSERT, str(i.rmpRating), 'bad')
					else:
						self.text_area.insert(tk.INSERT, str(i.rmpRating), 'good')
				else:
					self.text_area.insert(tk.INSERT, "N/A")

				self.text_area.insert(tk.INSERT, '\t')

				if i.getMedian() <= 80:
					self.text_area.insert(tk.INSERT, str(i.getMedian()), 'bad')
				else:
					self.text_area.insert(tk.INSERT, str(i.getMedian()), 'good')

				self.text_area.insert(tk.INSERT, '\n')

		self.text_area.configure(state='disabled')

	def updateRMP(self):
		RMPHolder.x.createprofessorlist()

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