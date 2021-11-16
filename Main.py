import time
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

        self.g1 = Grades('cs', '2305')

        # lists
        self.option_menu_list = ['', 'Combined', 'Rating', 'Grades']
        self.table = []

        # vars
        self.professorname_var = tk.StringVar()
        self.classnum_var = tk.StringVar()
        self.class2_var = tk.StringVar()
        self.className = tk.StringVar()
        self.sort_var = tk.StringVar(value=self.option_menu_list[1])

        self.setup()

    def setup(self):
        # menu bar
        self.menubar = tk.Menu(root)
        # advanced
        advanced = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Advanced', menu=advanced)
        advanced.add_command(label='Placeholder', command=None)
        advanced.add_separator()
        advanced.add_command(label='Update RateMyProfessor', command=self.updateRMP)
        # about
        about = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='About', menu=about)
        about.add_command(label='GitHub', command=None)
        # draw menu bar
        root.config(menu=self.menubar)
        self.menubar = tk.Menu(root)

        # entry frame
        self.menu_frame = ttk.Frame(self, padding=(10, 10))
        self.menu_frame.grid(
            row=0, column=0, padx=(10, 10), pady=(0, 10)
        )

        # entry label
        self.classcode_label = ttk.Label(
            self.menu_frame, text='Class code (ex: \'CS 2305\')', font=('calibre', 10, 'normal')
        )
        self.classcode_label.grid(row=0, column=2, padx=0, pady=5)

        # entry field
        self.classcode_entry = ttk.Entry(
            self.menu_frame, textvariable=self.classnum_var, font=('calibre', 10, 'normal')
        )
        self.classcode_entry.grid(row=0, column=0, padx=0, pady=5)

        # submit button
        self.sub_btn = ttk.Button(
            self.menu_frame, text='Search', command=self.submit
        )
        self.sub_btn.grid(row=0, column=1, padx=0, pady=5)

        # sort label
        self.sort_label = ttk.Label(
            self.menu_frame, text='Sort', font=('calibre', 10, 'normal')
        )
        self.sort_label.grid(row=0, column=3, padx=5, pady=5)

        # sort dropdown
        self.optionmenu = ttk.OptionMenu(
            self.menu_frame, self.sort_var, *self.option_menu_list, command=self.test
        )
        self.optionmenu.grid(row=0, column=4, padx=5, pady=5)

        # entry label 2
        self.class2_label = ttk.Label(
            self.menu_frame, text='Filter names (ex: \'Chin, Ntafos, Willson\')', font=('calibre', 10, 'normal')
        )
        self.class2_label.grid(row=1, column=2, padx=5, pady=5)

        # entry field 2
        self.class2_entry = ttk.Entry(
            self.menu_frame, textvariable=self.class2_var, font=('calibre', 10, 'normal')
        )
        self.class2_entry.grid(row=1, column=0, padx=5, pady=5)

        # bindings
        self.classcode_entry.bind("<Tab>", self.focusText2)
        self.class2_entry.bind("<Return>", self.submitBind)
        self.classcode_entry.bind("<Return>", self.submitBind)

        # class name label
        # self.classNameLabel = ttk.Label(
        #     self.menu_frame,
        #     text=self.className.get(),
        #     justify="center",
        #     font=("-size", 12, "-weight", "normal"),
        # )
        # self.classNameLabel.grid(row=2, column=0, pady=0, columnspan=4)

        # entry frame
        self.content_frame = ttk.Frame(self, padding=(10, 10))
        self.content_frame.grid(
            row=1, column=0, padx=(10, 10), pady=(0, 0)
        )

        # text box
        self.text_area = tk.scrolledtext.ScrolledText(self.content_frame,
                                                      width=65,
                                                      height=17,
                                                      font=("Calibri",
                                                            12))
        self.text_area.grid(row=0, column=0, pady=0, padx=10)
        self.text_area.configure(state='disabled')

        # setup colors for the text area
        # https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/
        self.text_area.tag_configure('good', foreground='green')
        self.text_area.tag_configure('bad', foreground='red')
        self.text_area.tag_configure('medium', foreground='orange2')

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

    def submitBind(self, test):
        self.submit()

    def focusText2(self, test):
        self.class2_entry.focus()
        return "break"

    def test(self, value):
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
        #     self.text_area.insert(tk.INSERT, "\tClasses") # add classes counter if not default sort
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


if __name__ == "__main__":
    # set up root
    root = tk.Tk()
    app = App(root)
    app.pack(fill="both", expand=True)
    root.title('UTD Professor Showdown')

    # set theme up
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")

    # setting the windows size
    root.geometry("700x500")
    root.mainloop()
