import tkinter as tk
import ScrumblesData
import masterView


class developerHomeView(tk.Frame):
    def __init__(self, parent, controller,user):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.usernameLabel = tk.Label(self, text='Welcome to the Developer Home View ')
        self.usernameLabel.pack()