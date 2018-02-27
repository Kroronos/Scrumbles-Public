
import tkinter as tk

import ScrumblesFrames
import ScrumblesData



class ItemManagerView(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller =  controller

		self.usernameLabel = tk.Label(self, text = "Item Manager", font = ("Verdana", 12))
		self.usernameLabel.pack(side = tk.TOP, fill = tk.X)

		self.itemList = ScrumblesFrames.SList(self, "ITEMS")
		# self.grid(row = 1, column = 0)

		controller.dataConnection.connect()

		self.items = controller.dataConnection.getData('SELECT * FROM CardTable')
		self.items = [card['CardTitle'] for card in self.items]

		controller.dataConnection.close()

		self.itemList.importList(self.items)
		self.itemList.pack(side = tk.LEFT, fill = tk.Y)

		self.commentsTitle = tk.Label(self, text = "Comments", font = ("Verdana",12))
		self.commentsTitle.pack(side = tk.RIGHT, anchor = "n")
		# self.commentsTitle.grid(row = 0, column = 0)
		#self.commentsTitle.pack(side = tk.RIGHT)
		# self.comments = ScrumblesFrames.SList(self,"COMMENTS")
		self.commentsField = tk.Entry(self)
		# self.commentsField.grid(row = 1)
		# self.comments.importList([self.commentsField])
		#self.commentsField.pack(side = tk.RIGHT)

		self.commentsField.pack(side = tk.RIGHT, fill = tk.Y, anchor = "s")

		self.dataTest = tk.Label(self, text="First")
		# self.dataTest.pack(padx = 300, pady = 150, side = tk.LEFT)

		self.dataEntry = tk.Entry(width = 10)

	# def load_items(self):
	# 	#do things
	# 	print("Items Loaded")
    #
	# def add_item(self):
	# 	#do things
	# 	print("Items added")
    #
	# def remove_item(self):
	# 	#do things
	# 	print("Items remove")
    #
	# def update_item(self):
	# 	#do things
	# 	print("Items updated")
    #
	# def go_to_git(self):
	# 	#do things
	# 	print("git opened")