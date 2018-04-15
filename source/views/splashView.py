import tkinter as tk
from tkinter import ttk

class splashView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, cursor = "watch")
        self.controller = controller
        print('Init Splash')

        self.waitLabel = tk.Label(self, text = 'Please wait while Scrumbles Loads')
        self.waitLabel.pack()
        self.isAlive = True

        self.pbarList = []
        for i in range(30):
            pbar = None
            pbar = ttk.Progressbar(self, length=1000, maximum=10 * i, mode='indeterminate')
            pbar.pack()
            self.pbarList.append(pbar)

        self.update

    def stepProgressBar(self, interval):
        for pbar in self.pbarList:
            pbar.step(interval)
            self.update_idletasks()
