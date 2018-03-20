import tkinter as tk

import ScrumblesFrames
import ScrumblesData

class sprintManagerView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.usernameLabel = tk.Label(self, text = "Sprint Manager", font = ("Verdana", 12))
        self.usernameLabel.pack()

        self.itemList = ScrumblesFrames.SList(self, "SPRINTS")

        self.itemList.pack(side = tk.LEFT, fill = tk.Y)