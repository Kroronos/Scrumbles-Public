import tkinter as tk
from tkinter import ttk

class splashView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, cursor = "watch")
        self.controller = controller


        self.waitLabel = tk.Label(self, text = 'Please wait while Scrumbles Loads')
        self.waitLabel.pack()
        self.isAlive = True

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("green.Horizontal.TProgressbar",
                    troughcolor = 'white',
                    background = 'lime green')

        self.pbarList = []
        for i in range(30):
            pbar = None
            pbar = ttk.Progressbar(self,
                                   style = "green.Horizontal.TProgressbar",
                                   length = 1000,
                                   maximum = 10 * (i+1),
                                   mode = 'indeterminate')
            pbar.pack()
            self.pbarList.append(pbar)

        self.update

    def stepProgressBar(self, interval):
        for pbar in self.pbarList:
            pbar.step(interval)
            self.update_idletasks()
