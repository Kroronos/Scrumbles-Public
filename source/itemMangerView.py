import tkinter as tk
from tkinter import ttk
import ScrumblesFrames


# class dataForm(tk.Frame):
# 	def __init__(self):
# 		self.nameLabel = tk.Label(self, text="Name: ").grid(row=0)
# 		self.descriptionLabel = tk.Label(self, text="Description: ").grid(row=1)

# 		self.weightLabel = tk.Label(self, text = "Weight: ").grid(row = 2)
# 		self.statusLabel = tk.Label(self, text = "Status: ").grid(row = 3)

# 		self.name = tk.Entry(self)
# 		self.description = tk.Entry(self)
# 		self.weight = tk.Entry(self)
# 		self.status = tk.Entry(self)

# 		self.name.grid(row = 0, column = 1)
# 		self.description.grid(row = 1, column = 1)
# 		self.weight.grid(row = 2, column = 1)
# 		self.status.grid(row = 3, column = 1)


class ItemManagerView(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller =  controller

		self.usernameLabel = tk.Label(self, text = "Item Manager", font = ("Verdana", 12))
		self.usernameLabel.pack(side = tk.TOP, fill = tk.X)

		self.tabButtons = ScrumblesFrames.STabs(self, controller, "Item Manager View")
		self.tabButtons.pack(side=tk.TOP, fill=tk.X)

		self.itemList = ScrumblesFrames.SList(self, "ITEMS")
		# self.grid(row = 1, column = 0)


		self.items =[item.itemTitle for item in self.controller.dataBlock.items]



		self.itemList.importList(self.items)
		self.itemList.pack(side = tk.LEFT, fill = tk.Y)

		#self.data = dataForm.__init__(self)
		#self.data.pack(side = tk.LEFT, fill = tk.Y)

		# self.commentsTitle = tk.Label(self, text = "Comments", font = ("Verdana",12))
		# self.commentsTitle.pack(side = tk.RIGHT, fill = tk.Y, padx = 20, pady = 20)
		#self.commentsTitle.grid(row = 0, column = 0)
		#self.commentsTitle.pack(side = tk.RIGHT)
		#self.comments = ScrumblesFrames.SList(self,"COMMENTS")

		self.commentField = ScrumblesFrames.commentsField(self)
		self.commentField.pack(side = tk.RIGHT, fill = tk.Y, padx = 20, pady = 20, ipadx = 5, ipady = 5)

		self.itemEditor = ScrumblesFrames.itemPicker(self)
		self.itemEditor.pack(side = tk.LEFT, fill = tk.BOTH, padx = 20, pady = 20, ipadx = 5, ipady = 5)

		#self.dataTest = tk.Label(self, text="First")
		# self.dataTest.pack(padx = 300, pady = 150, side = tk.LEFT)

		#self.dataEntry = tk.Entry(width = 10)

	