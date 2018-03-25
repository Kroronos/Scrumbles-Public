import tkinter as tk

import ScrumblesData
import ScrumblesObjects

import ScrumblesFrames
import Dialogs

import threading

#from tkinter import ttk

class backlogManagerView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Backlog Manager")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        products = ("PRODUCTS", "PRODUCT A", "PRODUCT B", "PRODUCT C")
        self.productList = ScrumblesFrames.SComboList(self, "PRODUCT BACKLOG", products)
        self.backlog = ScrumblesFrames.SBacklogList(self)

        self.contextMenu = tk.Menu()
        self.aqua = parent.tk.call('tk','windowingsystem') == 'aqua'
        self.contextMenu.add_command(label=u'Update Item',command=self.updateItem)




        self.productListData = self.controller.dataBlock.projects
        self.backlogData = self.controller.dataBlock.items
        self.controller.dataBlock.packCallback(self.updateBacklogViewData)




        #todo Not sure if it was Projects that was supposed to be displayed under Products...

        #self.productListData = ["1","2","3","4","5","6","7",]
        #self.backlogData = ["a","b","c","bee","e","f","g",]



        self.productList.importProjectList(self.productListData)

        self.backlog.importItemList(self.backlogData)
        self.backlog.listbox.bind('<2>' if self.aqua else '<3>', lambda event: self.context_menu(event,self.contextMenu))
        self.productList.pack(side=tk.LEFT, fill=tk.Y)
        self.backlog.pack(side=tk.LEFT, fill=tk.Y)

        #todo Click on project name to display items in backlog
        #todo click and drag on items in backlog to change priority variable of an item so that sort will be user defined

    def updateItem(self):
        item = None
        title = self.itemTitle
        for i in self.backlogData:
            if i.itemTitle == title:
               item = i

        if item is None:
            print('Item Title:',title)
            print('backlogData:')
            for i in self.backlogData:
                print(i.itemTitle)
            raise Exception('Error Loading item from title')



        editUserDialog = Dialogs.EditItemDialog(self, self.controller.dataBlock ,item)
        self.wait_window(editUserDialog.top)



    def context_menu(self,event,menu):
         widget = event.widget
         index = widget.nearest(event.y)
         _, yoffset, _, height = widget.bbox(index)
         if event.y > height + yoffset + 5:
             return
         self.itemTitle = widget.get(index)
         #print('do something')
         menu.post(event.x_root, event.y_root)




    def updateBacklogViewData(self):
        self.productList.clearList()
        self.backlog.clearList()
        self.productList.importProjectList(self.productListData)
        self.backlog.importItemList(self.backlogData)


        #######################################################################
        ###Five freaking hours of troublshooting... I am a F@$%ing moron
        # right here.. Python PASSES OBJECTS AROUND BY REFERENCE
        #self.productListData.clear()  # <--- This clears dataBlock.projects GLOBALLY
        #self.backlogData.clear()      # <--- This clears dataBlock.items GLOBALLY
        #####################################################################

        ############### Below is completely Stupid,  these need to repack the frames
        # NEED CODE BELOW TO REPACK FRAMES NOT this
        #self.productListData = DB.projects # <-- this does nothing, this is the same as a = a
        #self.backlogData = DB.items #<-- this does nothing, this is the same as a = a
        #############################################################################
        #  This is why sleep deprivation and programming do not mix well
        ##############################################################################

