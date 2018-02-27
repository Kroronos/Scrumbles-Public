import tkinter as tk
import tkcalendar
import ScrumblesData
import ScrumblesObjects
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
        self.productList.pack(side=tk.LEFT, fill=tk.Y)
        self.backlog.pack(side=tk.LEFT, fill=tk.Y)

        #todo Click on project name to display items in backlog
        #todo click and drag on items in backlog to change priority variable of an item so that sort will be user defined