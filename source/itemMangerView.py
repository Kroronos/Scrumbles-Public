from tkinter import *
import tkinter as tk
from tkinter import ttk
import ScrumblesFrames
import ScrumblesData

root = Tk()

class ItemManagerView(ttk.Frame):
	def __init__(self, parent, controller):#, parent, controller):
		self.controller = controller
		tk.Frame.__init__(self, parent)

		self.usernameLabel = tk.Label(self, text = "Item Manager", font = ("Verdana", 12))
		self.usernameLabel.pack()

		self.itemList = ScrumblesFrames.SList(self, "ITEMS")

		controller.dataConnection.connect()
		self.items = controller.dataConnection.getData('SELECT * FROM ItemTable')
		self.items = [item['ItemTitle'] for item in self.itemList]

		controller.dataConnection.close()

		self.itemList.importList(self.items)

		self.itemList.pack(side = tk.LEFT, fill = tk.Y)
		

		self.commentBox = Entry(self)

		self.commentBox.pack(side = tk.RIGHT, fill = tk.Y )
	def load_items():
		#do things
		print("Items Loaded")

	def add_item():
		#do things
		print("Items added")

	def remove_item():
		#do things
		print("Items remove")

	def update_item():
		#do things
		print("Items updated")

	def go_to_git():
		#do things
		print("git opened")
