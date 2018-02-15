import tkinter as tk
import ScrumblesData
import masterView

class mainView(tk.Frame):
    def __init__(self, parent, controller,user):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.usernameLabel = tk.Label(self, text='Welcome to Scrumbles ' + user.userName)
        self.usernameLabel.pack()

