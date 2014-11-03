##
# user interface
##
from tkinter import *


class Gui():
    def __init__(self):
        self.st = ""

    def get_string(self):
        self.root = Tk()
        self.root.title('Пароль?')
        self.root.geometry("%dx%d+%d+%d" % (250, 50, self.root.winfo_screenwidth()/2, self.root.winfo_screenheight()/2))
        self.entry = Entry(self.root)
        self.entry.pack()
        self.entry.focus_set()
        button = Button(self.root, bg="black", fg="red", text="done", command=self.button_click)
        button.pack()
        self.root.mainloop()
        return self.st

    def button_click(self):
        self.st = self.entry.get()
        self.root.destroy()