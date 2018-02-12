from ScrumblesData import *
from masterView import *
from tkinter import *

class mainView(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)

