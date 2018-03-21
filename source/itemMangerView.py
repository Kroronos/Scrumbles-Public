import tkinter as tk
from tkinter import ttk
import ScrumblesFrames


class ItemManagerView(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller =  controller

		self.usernameLabel = tk.Label(self, text = "Item Manager", font = ("Verdana", 12))
		self.usernameLabel.pack(side = tk.TOP, fill = tk.X)

		self.itemList = ScrumblesFrames.SList(self, "ITEMS")
		self.itemList.listbox.bind('<<ListboxSelect>>', lambda event: self.dynamicEventHandler(event))

		# self.grid(row = 1, column = 0)


		self.items =[item.itemTitle for item in self.controller.dataBlock.items]



		self.itemList.importList(self.items)
		self.itemList.pack(side = tk.LEFT, fill = tk.Y)



		self.commentField = ScrumblesFrames.commentsField(self)
		self.commentField.pack(side = tk.RIGHT, fill = tk.Y, padx = 20, pady = 20, ipadx = 5, ipady = 5)

		self.itemEditor = ScrumblesFrames.itemPicker(self)
		self.itemEditor.pack(side = tk.LEFT, fill = tk.BOTH, padx = 20, pady = 20, ipadx = 5, ipady = 5)

	def dynamicEventHandler(self, event):
		self.itemEditor.load_items()
		index = self.itemList.listbox.curselection()
		print(self.itemList.listbox.get(index[0]))
		print(self.itemList.listbox.get(index))

        # def selection(self, val):
        #  sender = val.Listbox1
        #  index = listbox1.curselection()
        #  value = Listbox1.get(index[0])
        #  if index == 1 or index == 4:
        #      seltext = software
        #  elif index == 2 or index == 5:
        #      seltext = hardware
        #  elif index == 3:
        #      seltext = mobile
        #  elif index == 6:
        #      seltext = wireless
        #  elif index == 7:
        #      seltext = AD
        #  elif index == 8:
        #      seltext = printer
        # if event.widget is self.teamMemberList.listbox:
        #     self.getItemsAssignedToUser(event)
        #     self.descriptionManager.changeDescription(event)

        # if event.widget is self.productBacklogList.listbox:
        #     self.descriptionManager.changeDescription(event)

        # if event.widget is self.assignedItemList.listbox:
        #     self.descriptionManager.changeDescription(event)
		print("item Selected")

		#self.dataTest = tk.Label(self, text="First")
		# self.dataTest.pack(padx = 300, pady = 150, side = tk.LEFT)

		#self.dataEntry = tk.Entry(width = 10)

	

        # #Append Any Sources for Dynamic Events to this List
        # dynamicSources = [self.productBacklogList.fx, self.teamMemberList.listbox, self.assignedItemList.listbox]
        # queryType = ['Item', 'User', 'Item']
        # self.descriptionManager = ScrumblesFrames.SCardDescription(self, dynamicSources, queryType)
        # #Bind Sources
        # for source in dynamicSources:
            
		


   