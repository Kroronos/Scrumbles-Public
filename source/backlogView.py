import tkinter as tk
import tkcalendar
import ScrumblesData
import masterView
import ScrumblesFrames

from tkinter import ttk
class backlogView(tk.Frame):
    def __init__(self, parent, controller,user):
        tk.Frame.__init__(self, parent)
        products = ("PRODUCTS", "PRODUCT A", "PRODUCT B", "PRODUCT C")

        self.usernameLabel = tk.Label(self, text='Welcome to the Projects Backlog View ', font=("Verdana", 12))
        self.usernameLabel.pack()
        self.productList = ScrumblesFrames.SComboList(self, "PRODUCT BACKLOG", products)
        self.backlog = ScrumblesFrames.SBacklogList(self)




        controller.dataConnection.connect()
        self.productListData = ["1","2","3","4","5","6","7",]
        self.backlogData = ["a","b","c","bee","e","f","g",] 
        
        controller.dataConnection.close()

        self.productList.importList(self.productListData)
        self.backlog.importList(self.backlogData)
        self.productList.pack(side=tk.LEFT, fill=tk.Y)
        self.backlog.pack(side=tk.LEFT, fill=tk.Y)
