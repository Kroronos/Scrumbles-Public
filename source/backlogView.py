import tkinter as tk
import tkcalendar
import ScrumblesData
import ScrumblesObjects
import masterView
import ScrumblesFrames
import Dialogs


from tkinter import ttk
class backlogView(tk.Frame):
    def __init__(self, parent, controller,user):
        tk.Frame.__init__(self, parent)
        products = ("PRODUCTS", "PRODUCT A", "PRODUCT B", "PRODUCT C")
        self.controller = controller
        self.usernameLabel = tk.Label(self, text='Welcome to the Projects Backlog View ', font=("Verdana", 12))
        self.usernameLabel.pack()
        self.productList = ScrumblesFrames.SComboList(self, "PRODUCT BACKLOG", products)
        self.backlog = ScrumblesFrames.SBacklogList(self)

        self.contextMenu = tk.Menu()
        self.aqua = parent.tk.call('tk','windowingsystem') == 'aqua'
        self.contextMenu.add_command(label=u'Update Item',command=self.updateItem)



        controller.dataConnection.connect()
        productQueryResult = controller.dataConnection.getData(ScrumblesData.Query.getAllProjects)
        itemListQueryResult = controller.dataConnection.getData(ScrumblesData.Query.getAllCards)
        controller.dataConnection.close()

        listofProducts = []
        for dictionary in productQueryResult:
            listofProducts.append(ScrumblesObjects.Project(dictionary))
        listofItems = []
        for dictionary in itemListQueryResult:
            listofItems.append(ScrumblesObjects.Item(dictionary))
        self.productListData = listofProducts
        self.backlogData = listofItems

        #todo Not sure if it was Projects that was supposed to be displayed under Products...

        #self.productListData = ["1","2","3","4","5","6","7",]
        #self.backlogData = ["a","b","c","bee","e","f","g",]



        self.productList.importProjectList(self.productListData)

        self.backlog.importItemList(self.backlogData)
        self.backlog.listbox.bind('<2>' if self.aqua else '<3>', lambda e: self.context_menu(e,self.contextMenu))
        self.productList.pack(side=tk.LEFT, fill=tk.Y)
        self.backlog.pack(side=tk.LEFT, fill=tk.Y)

        #todo Click on project name to display items in backlog
        #todo click and drag on items in backlog to change priority variable of an item so that sort will be user defined

    def updateItem(self):
        self.controller.dataConnection.connect()
        itemResultQuery = self.controller.dataConnection.getData(ScrumblesData.CardQuery.getCardByCardTitle(self.itemTitle))
        self.controller.close()
        item = ScrumblesObjects.Item(itemResultQuery[0])
        editUserDialog = Dialogs.EditItemDialog(self, self.controller.dataConnection,item)
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