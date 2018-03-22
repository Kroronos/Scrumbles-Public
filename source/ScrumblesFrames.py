import tkinter as tk
import webbrowser
import matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import csv
import tkcalendar
import datetime
import ScrumblesData
import ScrumblesObjects

from styling import styling as style
from tkinter import ttk

class BaseList(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)
        self.fullList = []

    def showPartialList(self, list):
        self.clearList()
        for item in list:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def showFullList(self):
        self.clearList()
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()


    def importList(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()


    def importItemList(self, items):
        self.deleteList()
        listofnames = []
        for item in items:
            listofnames.append(item.itemTitle)
        self.fullList = listofnames
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importProjectList(self, projects):
        self.deleteList()
        listOfnames = []
        for project in projects:
            listOfnames.append(project.projectName)
        self.fullList = listOfnames
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()



    def importListSorted(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)

    def appendList(self, list):
        for item in list:
            self.fullList.append(item)
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def addItem(self, item):
        self.fullList.append(item)
        self.listbox.insert(tk.END, item)
        self.enforceSort()

    def sortForward(self):
        items = self.listbox.get(0, tk.END)
        items = sorted(items)
        self.fullList = sorted(self.fullList)
        self.importListSorted(items)

    def sortReverse(self):
        items = self.listbox.get(0, tk.END)
        items = sorted(items, reverse=True)
        self.fullList = sorted(self.fullList, reverse=True)
        self.importListSorted(items)

    def clearList(self):
        self.listbox.delete(0, tk.END)

    def deleteList(self):
        self.listbox.delete(0, tk.END)
        self.fullList = []

    def deleteSelectedItem(self):

        deleteIndex = self.listbox.get(0, tk.END).index(tk.ANCHOR)
        del self.fullList[deleteIndex]
        self.listbox.delete(tk.ANCHOR)
        self.enforceSorting()

    def decideSort(self):
        if self.typeSort == "none":
           self.typeSort = "forward"
           self.sortButton["text"] = style.up_arrow
           self.sortForward()
        elif self.typeSort == "forward":
            self.typeSort = "reverse"
            self.sortButton["text"] = style.down_arrow
            self.sortReverse()
        else:
            self.typeSort = "forward"
            self.sortButton["text"] = style.up_arrow
            self.sortForward()

    def enforceSort(self):
        if self.typeSort == "none":
            return
        elif self.typeSort == "forward":
            self.sortForward()
        else:
            self.sortReverse()

    def search(self, str):
        def fulfillsCondition(item,str):
            return item[:len(str)] == str

        matches = [x for x in self.fullList if fulfillsCondition(x, str)]
        self.showPartialList(matches)


class SComboList(BaseList):
    def __init__(self, controller, title, products):
        tk.Frame.__init__(self, controller)

        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.box_value)
        self.box['values'] = (products)
        self.box.current(0)
        self.box.pack(fill = tk.X)

        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listFrame.pack(fill=tk.BOTH, expand=True)

class SBacklogList(BaseList):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self, bg=style.scrumbles_blue, relief=tk.SOLID, borderwidth=1)
        self.searchFrame = tk.Frame(self.titleFrame, relief=tk.SOLID, bg=style.scrumbles_blue)

        self.searchLabel = tk.Label(self.searchFrame, text="Search:", bg=style.scrumbles_blue)
        self.searchEntry = tk.Entry(self.searchFrame)
        self.searchButton = tk.Button(self.searchFrame, text=style.right_enter_arrow, bg=style.scrumbles_blue, command=lambda: self.search(self.searchEntry.get()), relief=tk.FLAT)
        self.undoSearchButton = tk.Button(self.searchFrame, text=style.cancel_button, bg=style.scrumbles_blue, command=lambda: self.showFullList(), relief=tk.FLAT)

        self.searchEntry.bind('<Return>', lambda event: self.search(self.searchEntry.get()))
        self.undoSearchButton.pack(side = tk.RIGHT)
        self.searchButton.pack(side = tk.RIGHT)
        self.searchEntry.pack(side = tk.RIGHT)
        self.searchLabel.pack(side = tk.RIGHT)


        self.titleLabel = tk.Label(self.titleFrame, text="Backlog", bg=style.scrumbles_blue, relief=tk.FLAT)
        self.sortButton = tk.Button(self.titleFrame, text=style.updown_arrow, bg=style.scrumbles_blue, command=lambda: self.decideSort(), relief=tk.FLAT)

        self.titleLabel.pack(side = tk.LEFT)
        self.sortButton.pack(side = tk.RIGHT)
        self.searchFrame.pack(side = tk.RIGHT)

        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, width = 80, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"
        self.titleFrame.pack(fill=tk.X, expand=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listFrame.pack(fill=tk.BOTH, expand=True)

class SList(BaseList):
    def __init__(self, controller, title):
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self, bg=style.scrumbles_blue, relief=tk.SOLID, borderwidth=1)
        self.titleLabel = tk.Label(self.titleFrame, text=title, bg=style.scrumbles_blue, relief=tk.FLAT)
        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"

        self.sortButton = tk.Button(self.titleFrame, text=style.updown_arrow, bg=style.scrumbles_blue, command=lambda: self.decideSort(), relief=tk.FLAT)
        self.titleLabel.pack(side=tk.LEFT)
        self.sortButton.pack(side=tk.RIGHT)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.titleFrame.pack(fill=tk.X, expand=False)
        self.listFrame.pack(fill=tk.BOTH, expand=True)


class SLineGraph(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.y = [1,4,2,5,1,4,2,5,1,4]
        self.label = None

        self.figure = Figure(figsize=(4, 4), dpi=100)
        self.graph = self.figure.add_subplot(1,1,1)


    def setTitle(self, title):
        self.label = tk.Label(self, text=title)

    def setAxes(self, xAxis, yAxis):
        self.graph.set_xlabel(xAxis)
        self.graph.set_ylabel(yAxis)
        self.figure.subplots_adjust(left=.15)
        self.figure.subplots_adjust(bottom=.15)

    def importDataFromCSV(self, fileName, delimeter):
        with open(fileName, 'r') as file:
            plots = csv.reader(file, delimeter)
            for row in plots:
                self.x.append(int(row[0]))
                self.y.append(int(row[1]))

    def displayGraph(self):
        self.graph.plot(self.x, self.y)
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.show()
        if self.label is not None:
            self.label.pack(side=tk.TOP, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=1, pady=1)

    def changeBackgroundColor(self, color):
        self.graph.set_facecolor(facecolor=color)

class SCalendar(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)
        now = datetime.datetime.now()
        self.cal = tkcalendar.Calendar(self, font="Arial 14", selectmode='day', year=now.year, month=now.month, day=now.day)
        self.cal.pack(side=tk.TOP, fill=tk.BOTH)

class itemPicker(tk.Frame):

    def __init__(self, controller):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth=1)
       
        self.itemNumberLabel = tk.Label(self, text = "Item Number: ", anchor = 'w').grid(row = 0, column = 0)


        self.itemNameLabel = tk.Label(self, text = "Name: ", anchor = 'w').grid(row = 1, column = 0)
        self.itemNameEntryText = tk.StringVar()
        self.itemNameEntry = tk.Entry(self, textvariable = self.itemNameEntryText).grid(row = 1, column = 1)

        self.itemDescriptionLabel =  tk.Label(self, text = "Description: ", anchor = 'w').grid(row = 2, column = 0)
        self.itemDescriptionEntryText = tk.StringVar()
        self.itemDescriptionEntry = tk.Entry(self, textvariable = self.itemDescriptionEntryText).grid(row = 2, column = 1)


        self.itemPriorityLabel = tk.Label( self, text = "Priority: ", anchor = 'w').grid(row = 3, column = 0)
        self.itemPriorities = ("Low Priority", "Medium Priority", "High Priority")
        self.itemPrioritySelector = ttk.Combobox(self, values = self.itemPriorities).grid(row = 3, column = 1)

        self.itemStatusLabel = tk.Label(self, text = "Status: ", anchor = 'w').grid(row = 4)
        self.statuses = ("Not started", "In Progress", "Done") 
        self.itemStatusSelector = ttk.Combobox(self, values = self.statuses).grid(row = 4, column = 1)
        

        self.submitButton = tk.Button(self, text="Submit Changes", command = self.update_item).grid( row = 5, column = 1 )

    def selectItem(text):
        #l.config(text = "Hello World", width = "50" , )
        print("Item Selected")


    def load_items(self, name, description):
        #do things
        print("Items Loaded")
        self.itemNameEntryText.set(name)
        self.itemDescriptionEntryText.set(description)

    def add_item(self):
        #do things
        print("Items added")
    
    def remove_item(self):
        #do things
        print("Items remove")
    
    def update_item(self):
        #do things
        # self.itemNameEntry.select_clear()
        # self.itemNameEntry.insert(0, "Item Updated")
        # self.itemNameEntry.config(text = "Item Selected")
        print("Items updated")
        # res.configure(text = "Ergebnis: " + str(eval(entry.get())))
        # self.itemNameEntry.configure(text = "changed")
        # self.itemNameEntry.text = "Configure"
        self.itemDescriptionEntryText.set("Updated")

        # self.itemNameEntry.delete(0,END)
        # self.itemNameEntry.insert(0, "new text")


class commentsField(tk.Frame):
    
    def go_to_git(self):
        #do things
        print("git opened")
        webbrowser.open("github.com")



    def __init__(self, controller):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth = 1)

        # self.commentTitle = tk.Label(self, text = "Comments")
        # self.commentTitle.pack(side = tk.TOP)

        # self.commentField = tk.Entry(self, width = 150)
        # self.commentField.pack(side = tk.BOTTOM, fill = tk.Y)

        self.commentTitle = tk.Label(self, text = "Comments").grid(row = 0)

        self.commentField = tk.Entry(self).grid(row = 1)
        self.openGit = tk.Button(self, text="Github", command = self.go_to_git).grid( row = 2 )


class SCardDescription(tk.Frame):
    def __init__(self, controller, sources, datatype):
        tk.Frame.__init__(self, controller)
        self.controller = controller
        self.dataBlock = controller.controller.dataBlock
        self.config(relief=tk.SUNKEN, borderwidth=5)

        self.titleText = tk.StringVar()
        self.titleText.set("Item Description")
        self.title = tk.Label(self, textvariable=self.titleText,
                              font=(style.header_family, style.header_size, style.header_weight))
        self.title.pack(fill=tk.BOTH)

        # Reference datatype with widget code as key, allowing data calls from ScrumblesFrames
        self.datatype = dict((source, table) for source, table in zip(sources, datatype))

        self.cardDescriptions = {}
        self.cardDescriptions['Start'] = self.cardDescriptionStartFrame(self)
        self.cardDescriptions['Item'] = self.cardDescriptionItemFrame(self)
        self.cardDescriptions['User'] = self.cardDescriptionUserFrame(self)
        self.cardDescriptions['Active'] = self.cardDescriptions['Start']
        self.cardDescriptions['Active'].pack(side=tk.BOTTOM)

        self.descriptionLock = False
        self.oldWidget = None

    class cardDescriptionStartFrame(tk.Frame):
        def __init__(self, controller):
            tk.Frame.__init__(self, controller)
            tk.helpMeLabel = tk.Label(self, text="Click on a card to obtain information about it!")
            tk.helpMeLabel.pack()

    class cardDescriptionItemFrame(tk.Frame):
        def __init__(self, controller):
            tk.Frame.__init__(self, controller)

            self.itemTypeF = tk.Frame(self)
            self.itemTypeT = tk.Label(self.itemTypeF, text="Type: ")
            self.itemType = tk.Label(self.itemTypeF, text="")

            self.itemPriorityF = tk.Frame(self)
            self.itemPriorityT = tk.Label(self.itemPriorityF, text="Priority: ")
            self.itemPriority = tk.Label(self.itemPriorityF, text="")

            self.itemDueDateF = tk.Frame(self)
            self.itemDueDateT = tk.Label(self.itemDueDateF , text="Due Date: ")
            self.itemDueDate = tk.Label(self.itemDueDateF , text="")

            self.itemStatusF = tk.Frame(self)
            self.itemStatusT = tk.Label(self.itemStatusF, text="Status: ")
            self.itemStatus = tk.Label(self.itemStatusF, text="")

            self.itemDescriptionF = tk.Frame(self)
            self.itemDescriptionT = tk.Label(self.itemDescriptionF, text="Description: ")
            self.itemDescription = tk.Label(self.itemDescriptionF, text="")

            self.itemTypeT.pack(side=tk.LEFT)
            self.itemType.pack(side=tk.LEFT)
            self.itemPriorityT.pack(side=tk.LEFT)
            self.itemPriority.pack(side=tk.LEFT)
            self.itemDueDateT.pack(side=tk.LEFT)
            self.itemDueDate.pack(side=tk.LEFT)
            self.itemStatusT.pack(side=tk.LEFT)
            self.itemStatus.pack(side=tk.LEFT)
            self.itemDescriptionT.pack(side=tk.LEFT)
            self.itemDescription.pack(side=tk.LEFT)

            self.itemTypeF.pack(side=tk.TOP)
            self.itemPriorityF.pack(side=tk.TOP)
            self.itemDueDateF.pack(side=tk.TOP)
            self.itemStatusF.pack(side=tk.TOP)
            self.itemDescriptionF.pack(side=tk.TOP)

        def repack(self):
            self.itemTypeT.pack_forget()
            self.itemType.pack_forget()
            self.itemPriorityT.pack_forget()
            self.itemPriority.pack_forget()
            self.itemDueDateT.pack_forget()
            self.itemDueDate.pack_forget()
            self.itemStatusT.pack_forget()
            self.itemStatus.pack_forget()
            self.itemDescriptionT.pack_forget()
            self.itemDescription.pack_forget()

            self.itemTypeF.pack_forget()
            self.itemPriorityF.pack_forget()
            self.itemDueDateF.pack_forget()
            self.itemStatusF.pack_forget()
            self.itemDescriptionF.pack_forget()

            self.itemTypeT.pack(side=tk.LEFT)
            self.itemType.pack(side=tk.LEFT)
            self.itemPriorityT.pack(side=tk.LEFT)
            self.itemPriority.pack(side=tk.LEFT)
            self.itemDueDateT.pack(side=tk.LEFT)
            self.itemDueDate.pack(side=tk.LEFT)
            self.itemStatusT.pack(side=tk.LEFT)
            self.itemStatus.pack(side=tk.LEFT)
            self.itemDescriptionT.pack(side=tk.LEFT)
            self.itemDescription.pack(side=tk.LEFT)

            self.itemTypeF.pack(side=tk.TOP)
            self.itemPriorityF.pack(side=tk.TOP)
            self.itemDueDateF.pack(side=tk.TOP)
            self.itemStatusF.pack(side=tk.TOP)
            self.itemDescriptionF.pack(side=tk.TOP)

    class cardDescriptionUserFrame(tk.Frame):
        def __init__(self, controller):
            tk.Frame.__init__(self, controller)


            self.userRoleF = tk.Frame(self)
            self.userRoleT = tk.Label(self.userRoleF, text="Role: ")
            self.userRole = tk.Label(self.userRoleF, text="")

            self.userEmailF = tk.Frame(self)
            self.userEmailT = tk.Label(self.userEmailF, text="Email: ")
            self.userEmail = tk.Label(self.userEmailF, text="")


            self.userRoleT.pack(side=tk.LEFT)
            self.userRole.pack(side=tk.LEFT)
            self.userEmailT.pack(side=tk.LEFT)
            self.userEmail.pack(side=tk.LEFT)

            self.userRoleF.pack(side=tk.TOP)
            self.userEmailF.pack(side=tk.TOP)

        def repack(self):
            self.userRoleT.pack_forget()
            self.userRole.pack_forget()
            self.userEmailT.pack_forget()
            self.userEmail.pack_forget()

            self.userRoleF.pack_forget()
            self.userEmailF.pack_forget()

            self.userRoleT.pack(side=tk.LEFT)
            self.userRole.pack(side=tk.LEFT)
            self.userEmailT.pack(side=tk.LEFT)
            self.userEmail.pack(side=tk.LEFT)

            self.userRoleF.pack(side=tk.TOP)
            self.userEmailF.pack(side=tk.TOP)


    def repack(self):
        self.title.pack(fill=tk.BOTH)
        self.cardDescriptions['Active'].pack(side=tk.BOTTOM, fill=tk.BOTH)


    def changeDescription(self, event):
        widget = event.widget

        widgetChanged = False

        if self.oldWidget is None:
            self.oldWidget = widget

        if self.oldWidget != widget and self.descriptionLock == False:
            self.oldWidget = widget
            widgetChanged = True

        if self.descriptionLock is False:
            self.eventSetTitle(widget)
            self.generateAdditionalFields(widget)
            self.repack()

        if self.descriptionLock is True:
            self.descriptionLock = False

        if widgetChanged:
            self.descriptionLock = True


    def setTitle(self, title):
        self.titleText.set(title)


    def eventSetTitle(self, widget):
        selection = widget.get(tk.ANCHOR)
        self.setTitle(selection)


    def generateAdditionalFields(self, widget):
        match = None

        if self.datatype[widget] == 'User':
            for user in self.dataBlock.users:
                if user.userName == widget.get(tk.ANCHOR):
                    match = user

            self.generateUserFields(match)

        if self.datatype[widget] == 'Item':
            for item in self.dataBlock.items:
                if item.itemTitle == widget.get(tk.ANCHOR):
                    match = item

            self.generateItemFields(match)

    def generateUserFields(self, selectedUser):
        self.cardDescriptions["User"].userRole.configure(text=selectedUser.userRole, justify=tk.LEFT, wraplength=300)
        self.cardDescriptions["User"].userEmail.configure(text=selectedUser.userEmailAddress, justify=tk.LEFT,
                                                          wraplength=300)

        self.cardDescriptions["User"].repack()

        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions["User"]

    def generateItemFields(self, selectedItem):
        self.cardDescriptions["Item"].itemType.configure(text=selectedItem.itemType, justify=tk.LEFT, wraplength=300)
        self.cardDescriptions["Item"].itemPriority.configure(text=selectedItem.itemPriority, justify=tk.LEFT, wraplength=300)
        self.cardDescriptions["Item"].itemDescription.configure(text=selectedItem.itemDueDate, justify=tk.LEFT, wraplength=300)
        self.cardDescriptions["Item"].itemDescription.configure(text=selectedItem.itemStatus, justify=tk.LEFT, wraplength=300)
        self.cardDescriptions["Item"].itemDescription.configure(text=selectedItem.itemDescription, justify=tk.LEFT, wraplength=300)

        self.cardDescriptions["Item"].repack()

        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions["Item"]