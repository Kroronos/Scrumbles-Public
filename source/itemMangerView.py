
import tkinter as tk

import ScrumblesFrames
import ScrumblesData



class ItemManagerView(tk.Frame):
    def __init__(self, parent, controller):#, parent, controller):
        tk.Frame.__init__(self, parent)
        self.usernameLabel = tk.Label(self, text = "Item Manager", font = ("Verdana", 12))
        self.usernameLabel.pack()

        self.itemList = ScrumblesFrames.SList(self, "ITEMS")

        #controller.dataConnection.connect()
        #self.items = controller.dataConnection.getData('SELECT * FROM ItemTable')
        #self.items = [item['ItemTitle'] for item in self.itemList]

        #controller.dataConnection.close()

        #self.itemList.importList(self.items)

        self.itemList.pack(side = tk.LEFT, fill = tk.Y)


        #self.commentBox = Entry(self)

        #self.commentBox.pack(side = tk.RIGHT, fill = tk.Y )
        #def load_items(self):
        #do things
        #print("Items Loaded")

        #def add_item(self):
        #do things
        #print("Items added")

        #def remove_item(self):
        #do things
        #print("Items remove")

        #def update_item(self):
        #do things
        #print("Items updated")

        #def go_to_git(self):
        #do things
        #print("git opened")
        #