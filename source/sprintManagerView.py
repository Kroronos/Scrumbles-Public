import tkinter as tk

import ScrumblesFrames
import ScrumblesData

class sprintManagerView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Sprint Manager")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.itemList = ScrumblesFrames.SList(self, "SPRINTS")

        self.itemList.pack(side = tk.LEFT, fill = tk.Y)