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

class BaseList(tk.Frame,tk.Listbox):
    def __init__(self, controller):
        self.fullList = []
        self.controller = controller

    # def get(self,*args,**kwargs):
    #     return self.listbox.get(*args,**kwargs)
    #
    # def curselection(self,*args,**kwargs):
    #     print('debug curselection',self.listbox.curselection(*args,**kwargs))
    #     return self.listbox.curselection(*args,**kwargs)

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

    def importSprintsList(self, sprints):
        self.deleteList()
        listOfnames = []
        for sprints in sprints:
            listOfnames.append(sprints.sprintName)
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
        self.fullList = sorted(self.fullList, key=lambda s: self.processSort(s))
        self.importListSorted(self.fullList)

    def sortReverse(self):
        self.fullList = sorted(self.fullList, key=lambda s: self.processSort(s), reverse=True)
        self.importListSorted(self.fullList)

    def processSort(self, string):
        string = string.lower()
        string = "".join(string.split())
        return string

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
            return item[:len(str)].lower() == str.lower()

        matches = [x for x in self.fullList if fulfillsCondition(x, str)]
        self.showPartialList(matches)


class SComboList(BaseList):
    def __init__(self, controller, title, products):
        BaseList.__init__(self, controller)
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
    def __init__(self, controller, title):
        BaseList.__init__(self, controller)
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self, bg=style.scrumbles_blue, relief=tk.SOLID, borderwidth=1)
        self.searchFrame = tk.Frame(self.titleFrame, relief=tk.SOLID, bg=style.scrumbles_blue)

        self.searchLabel = tk.Label(self.searchFrame, text="Search:", bg=style.scrumbles_blue)
        self.searchEntry = tk.Entry(self.searchFrame)
        self.searchButton = tk.Button(self.searchFrame, text=style.right_enter_arrow, bg=style.scrumbles_blue, command=lambda: self.search(self.searchEntry.get()), relief=tk.FLAT)
        self.undoSearchButton = tk.Button(self.searchFrame, text=style.cancel_button, bg=style.scrumbles_blue, command=lambda: self.clearSearchEntry(), relief=tk.FLAT)

        self.searchEntry.bind('<Return>', lambda event: self.search(self.searchEntry.get()))
        self.undoSearchButton.pack(side = tk.RIGHT)
        self.searchButton.pack(side = tk.RIGHT)
        self.searchEntry.pack(side = tk.RIGHT)
        self.searchLabel.pack(side = tk.RIGHT)


        self.titleLabel = tk.Label(self.titleFrame, text=title, bg=style.scrumbles_blue, relief=tk.FLAT)
        self.sortButton = tk.Button(self.titleFrame, text=style.updown_arrow, bg=style.scrumbles_blue, command=lambda: self.decideSort(), relief=tk.FLAT)

        self.titleLabel.pack(side = tk.LEFT)
        self.sortButton.pack(side = tk.RIGHT)
        self.searchFrame.pack(side = tk.RIGHT)

        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, width = 50, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"
        self.titleFrame.pack(fill=tk.X, expand=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listFrame.pack(fill=tk.BOTH, expand=True)

    def clearSearchEntry(self):
        self.showFullList()
        self.searchEntry.delete(0,tk.END)

class SBacklogListColor(SBacklogList):
    def __init__(self, controller, title):
        SBacklogList.__init__(self, controller, title)

    def sortForward(self):
        super().sortForward()
        self.colorCodeListboxes()

    def sortRevers(self):
        super().sortReverse()
        self.colorCodeListboxes()

    def colorCodeListboxes(self):
        i = 0

        for itemTitle in self.listbox.get(0,tk.END):
            for item in self.controller.controller.activeProject.listOfAssignedItems:
                if itemTitle == item.itemTitle and item.itemSprintID is None:
                    self.listbox.itemconfig(i, {'bg': 'firebrick4'})
                    self.listbox.itemconfig(i, {'fg':'VioletRed1'})
                elif itemTitle == item.itemTitle and item.itemSprintID is not None:
                    self.listbox.itemconfig(i, {'bg':'dark green'})
                    self.listbox.itemconfig(i, {'fg':'lawn green'})
            i += 1


    def importListSorted(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.colorCodeListboxes()

    def clearSearchEntry(self):
        self.showFullList()
        self.searchEntry.delete(0,tk.END)
        self.colorCodeListboxes()


    def search(self, str):
        def fulfillsCondition(item,str):
            return item[:len(str)].lower() == str.lower()

        matches = [x for x in self.fullList if fulfillsCondition(x, str)]

        self.showPartialList(matches)
        self.colorCodeListboxes()


class SList(BaseList):
    def __init__(self, controller, title):
        BaseList.__init__(self, controller)
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
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH,expand=True)
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

    def __init__(self, controller, master):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth=1)
        self.controller = controller
        self.master = master
        self.top = None

        self.itemEditorLabel = tk.Label(self, text = "Item Editor", anchor = 'w').grid(row = 0, column = 0)


        self.itemNameLabel = tk.Label(self, text = "Name: ", anchor = 'w').grid(row = 1, column = 0)
        self.itemNameEntryText = tk.StringVar()
        self.itemNameEntry = tk.Entry(self, textvariable = self.itemNameEntryText).grid(row = 1, column = 1)

        self.itemDescriptionLabel =  tk.Label(self, text = "Description: ", anchor = 'w').grid(row = 2, column = 0)
        self.itemDescriptionEntryText = tk.StringVar()
        self.itemDescriptionEntry = tk.Entry(self, textvariable = self.itemDescriptionEntryText).grid(row = 2, column = 1)


        self.itemPriorityLabel = tk.Label( self, text = "Priority: ", anchor = 'w').grid(row = 3, column = 0)
        self.itemPriorityValue = tk.StringVar()
        self.priorities = ("Low Priority", "Medium Priority", "High Priority")
        self.itemPrioritySelector = ttk.Combobox(self, textvariable = self.itemPriorityValue, values = self.priorities, state = "readonly").grid(row = 3, column = 1)



        self.itemStatusLabel = tk.Label(self, text = "Status: ", anchor = 'w').grid(row = 4)
        self.itemStatusValue = tk.StringVar()
        self.statuses = ("Not started", "In Progress", "Done")
        self.itemStatusSelector = ttk.Combobox(self, textvariable = self.itemStatusValue, values = self.statuses, state = "readonly").grid(row = 4, column = 1)


        self.itemTypeLabel = tk.Label(self, text = "Item Type: ", anchor = 'w').grid(row = 5)
        self.itemTypeValue = tk.StringVar()
        self.itemTypeEntry = tk.Entry(self, textvariable = self.itemTypeValue).grid(row = 5, column = 1)

        self.itemUserLabel = tk.Label(self, text = "User: ", anchor = 'w').grid(row = 6)
        self.itemUserValue = tk.StringVar()

        #generate list of usernames
        self.listOfUsers = []
        for user in self.master.dataBlock.users:
            self.listOfUsers.append(user.userName)

        self.itemUserSelector = ttk.Combobox(self, textvariable = self.itemUserValue, values = self.listOfUsers , state = "readonly").grid(row = 6, column = 1)

        self.submitButton = tk.Button(self, text="Submit Changes", command = self.update_item).grid( column = 2 )

        self.addButton = tk.Button(self, text = "Add Item", command = self.add_item).grid( column = 2 )




    def selectItem(text):
        print("Item Selected")

    def load_items(self, name, description, status, priority, itemType, user):
        #do things
        print("Items Loaded")
        self.itemNameEntryText.set(name)
        self.itemDescriptionEntryText.set(description)
        self.itemStatusValue.set(status)
        self.itemPriorityValue.set(priority)
        self.itemTypeValue.set(itemType)
        self.itemUserValue.set(user)

    def add_item(self):
        self.top = tk.Toplevel()
        self.top.title("New Item")
        self.top.itemAdditionLabel = tk.Label(self.top, text = "New Item Information", anchor = 'w').grid(row = 0, column = 0)


        self.top.itemAdditionNameLabel = tk.Label(self.top, text = "Name: ", anchor = 'w').grid(row = 1, column = 0)
        self.top.itemAdditionNameEntryText = tk.StringVar()
        self.top.itemAdditionNameEntry = tk.Entry(self.top, textvariable = self.top.itemAdditionNameEntryText).grid(row = 1, column = 1)

        self.top.itemAdditionDescriptionLabel =  tk.Label(self.top, text = "Description: ", anchor = 'w').grid(row = 2, column = 0)
        self.top.itemAdditionDescriptionEntryText = tk.StringVar()
        self.top.itemAdditionDescriptionEntry = tk.Entry(self.top, textvariable = self.top.itemAdditionDescriptionEntryText).grid(row = 2, column = 1)


        self.top.itemAdditionPriorityLabel = tk.Label( self.top, text = "Priority: ", anchor = 'w').grid(row = 3, column = 0)
        self.top.itemAdditionPriorityValue = tk.StringVar()
        self.top.itemAdditionPrioritySelector = ttk.Combobox(self.top, textvariable = self.top.itemAdditionPriorityValue, values = self.priorities, state = "readonly").grid(row = 3, column = 1)



        self.top.itemAdditionStatusLabel = tk.Label(self.top, text = "Status: ", anchor = 'w').grid(row = 4)
        self.top.itemAdditionStatusValue = tk.StringVar()
        self.top.itemAdditionStatusSelector = ttk.Combobox(self.top, textvariable = self.top.itemAdditionStatusValue, values = self.statuses, state = "readonly").grid(row = 4, column = 1)

        self.top.itemAdditionTypeLabel = tk.Label(self.top, text = "Item Type: ", anchor = 'w').grid(row = 5, column = 0)
        self.top.itemAdditionTypeText = tk.StringVar()
        self.top.itemAdditionTypeEntry = tk.Entry(self.top, textvariable = self.top.itemAdditionTypeText).grid(row = 5, column = 1)

        self.top.itemAdditionUserLabel = tk.Label(self.top, text = "User: ", anchor = 'w').grid(row = 6)
        self.top.itemAdditionUserValue = tk.StringVar()
        self.top.itemAdditionUserSelector = ttk.Combobox(self.top, textvariable = self.top.itemAdditionUserValue, values = self.listOfUsers , state = "readonly").grid(row = 6, column = 1)


        self.top.submitButton = tk.Button(self.top, text="Submit", command = self.add_item_to_database).grid( column = 2 )

    def add_item_to_database(self):

        itemToAdd = ScrumblesObjects.Item()

        itemToAdd.itemTitle = self.top.itemAdditionNameEntryText.get()
        itemToAdd.itemDescription = self.top.itemAdditionDescriptionEntryText.get()

        #encode priority
        if self.top.itemAdditionPriorityValue.get() == self.priorities[0]:
            itemToAdd.itemPriority = 0
        elif self.top.itemAdditionPriorityValue.get() == self.priorities[1]:
            itemToAdd.itemPriority = 1
        elif self.top.itemAdditionPriorityValue.get() == self.priorities[2]:
            itemToAdd.itemPriority = 2

        #encode status
        if self.top.itemAdditionStatusValue.get() == self.statuses[0]:
            itemToAdd.itemStatus = 0
        elif self.top.itemAdditionStatusValue.get() == self.statuses[1]:
            itemToAdd.itemStatus = 1
        elif self.top.itemAdditionStatusValue.get() == self.statuses[2]:
            itemToAdd.itemStatus = 2

        itemToAdd.itemType = self.top.itemAdditionTypeText.get()

        for user in self.master.dataBlock.users:
            if user.userName == self.top.itemAdditionUserValue.get():
                itemToAdd.itemUserID = user.userID

        self.master.dataBlock.addNewScrumblesObject(itemToAdd)


        self.top.destroy()


    def remove_item(self):
        #do things
        print("Items remove")

    def update_item(self, item):

        item.itemTitle = self.itemNameEntryText.get()
        item.itemDescription = self.itemDescriptionEntryText.get()


        # ScrumblesData.DataBlock.updateScrumblesObject()

        #encode priority
        if self.itemPriorityValue.get() == self.priorities[0]:
            item.itemPriority = 0
        elif self.itemPriorityValue.get() == self.priorities[1]:
            item.itemPriority = 1
        elif self.itemPriorityValue.get() == self.priorities[2]:
            item.itemPriority = 2

        #encode status
        if self.itemStatusValue.get() == self.statuses[0]:
            item.itemStatus = 0
        elif self.itemStatusValue.get() == self.statuses[1]:
            item.itemStatus = 1
        elif self.itemStatusValue.get() == self.statuses[2]:
            item.itemStatus = 2

        item.itemType = self.itemTypeValue.get()

        for user in self.master.dataBlock.users:
            if user.userName == self.itemUserValue.get():
                item.itemUserID = user.userID

        self.master.dataBlock.updateScrumblesObject(item)





class commentsField(tk.Frame):


    def go_to_git(self):
        #do things
        print("git opened")
        webbrowser.open("github.com")

    def __init__(self, controller):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth = 1)

        self.commentTitle = tk.Label(self, text = "Comments").pack(side = tk.TOP, fill = tk.X)
        self.commentField = tk.Entry(self).pack(side = tk.TOP, fill = tk.X)
        self.openGit = tk.Button(self, text="Github", command = self.go_to_git).pack(side = tk.TOP, fill = tk.X)

        # self.titleText = tk.StringVar()
        # self.titleText.set("Comments")
        # self.commentTitleF = tk.Frame(self,relief=tk.SOLID, borderwidth=1)
        # self.commentTitle = tk.Label(self.commentTitleF, textvariable=self.titleText)
        # self.commentField = tk.Frame(self)
        # self.comments = []
        # self.commentTextElements = []

        # self.commentTitle.pack(side=tk.TOP, fill=tk.X)
        # self.commentTitleF.pack(side=tk.TOP, fill=tk.X)
        # self.commentField.pack(side=tk.TOP, fill=tk.BOTH)

    def updateFromListOfCommentsObject(self, listOfCommentsObject, objectName):
        self.clearCommentField()
        for comment in listOfCommentsObject.listOfComments:
            self.comments.append(comment)
        self.titleText.set("Comments\n" + objectName)
        self.renderCommentField()

    def renderCommentField(self):
        self.comments = sorted(self.comments, key=lambda s: s.commentTimeStamp)
        for comment in self.comments:
            commentLabel = tk.Label(self.commentField, text=comment.commentContent)
            self.commentTextElements.append(commentLabel)
            commentLabel.pack(side=tk.TOP, fill=tk.X)
        self.commentField.pack(side=tk.TOP, fill=tk.BOTH)

    def clearCommentField(self):
        self.comments.clear()
        self.commentField.pack_forget()
        for element in self.commentTextElements:
            element.pack_forget()
        self.commentTextElements.clear()

class SCardDescription(tk.Frame):
    def __init__(self, controller, master, sources, datatype):
        tk.Frame.__init__(self, controller)
        self.master = master
        self.controller = controller
        self.dataBlock = master.dataBlock
        self.config(relief=tk.SUNKEN, borderwidth=5)

        self.canvas = tk.Canvas(self, bd=1, scrollregion=(0,0,1000,1000), height=100)
        self.scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.internals = tk.Frame(self.canvas)
        self.canvasFrame = self.canvas.create_window(0,0,window=self.internals, anchor=tk.NW)
        self.titleText = tk.StringVar()
        self.titleText.set("Item Description")
        self.title = tk.Label(self.internals, textvariable=self.titleText,
                              font=(style.header_family, style.header_size, style.header_weight))
        self.title.pack(fill=tk.BOTH)
        self.internals.bind("<Configure>", self.OnFrameConfigure)
        self.canvas.bind('<Configure>', self.FrameWidth)
        # Reference datatype with widget code as key, allowing data calls from ScrumblesFrames
        self.datatype = dict((source, table) for source, table in zip(sources, datatype))

        self.cardDescriptions = {}
        self.cardDescriptions['Start'] = self.cardDescriptionStartFrame(self.internals)
        self.cardDescriptions['Item'] = self.cardDescriptionItemFrame(self.internals)
        self.cardDescriptions['User'] = self.cardDescriptionUserFrame(self.internals)
        self.cardDescriptions['Active'] = self.cardDescriptions['Start']
        self.cardDescriptions['Active'].pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvasFrame, width= canvas_width)
    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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

            self.itemUserF = tk.Frame(self)
            self.itemUserT = tk.Label(self.itemUserF, text="Assigned Users: ")
            self.itemUser = tk.Label(self.itemUserF, text="")

            self.itemSprintF = tk.Frame(self)
            self.itemSprintT = tk.Label(self.itemSprintF, text="Assigned Sprint:")
            self.itemSprint = tk.Label(self.itemSprintF, text="")

            self.itemDescriptionF = tk.Frame(self)
            self.itemDescriptionT = tk.Label(self.itemDescriptionF, text="Description: ")
            self.itemDescription = tk.Label(self.itemDescriptionF, text="")

            self.itemTypeT.pack(side=tk.LEFT, fill=tk.X)
            self.itemType.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriorityT.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriority.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDateT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDate.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatusT.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatus.pack(side=tk.LEFT, fill=tk.X)
            self.itemUserT.pack(side=tk.LEFT, fill=tk.X)
            self.itemUser.pack(side=tk.LEFT, fill=tk.X)
            self.itemSprintT.pack(side=tk.LEFT, fill=tk.X)
            self.itemSprint.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescriptionT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescription.pack(side=tk.LEFT, fill=tk.X)

            self.itemTypeF.pack(side=tk.TOP, fill=tk.X)
            self.itemPriorityF.pack(side=tk.TOP, fill=tk.X)
            self.itemDueDateF.pack(side=tk.TOP, fill=tk.X)
            self.itemStatusF.pack(side=tk.TOP, fill=tk.X)
            self.itemUserF.pack(side=tk.TOP, fill=tk.X)
            self.itemSprintF.pack(side=tk.TOP, fill=tk.X)
            self.itemDescriptionF.pack(side=tk.TOP, fill=tk.X)

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
            self.itemUserT.pack_forget()
            self.itemUser.pack_forget()
            self.itemSprintT.pack_forget()
            self.itemSprint.pack_forget()

            self.itemTypeF.pack_forget()
            self.itemPriorityF.pack_forget()
            self.itemDueDateF.pack_forget()
            self.itemStatusF.pack_forget()
            self.itemDescriptionF.pack_forget()
            self.itemUserF.pack_forget()
            self.itemSprintF.pack_forget()

            self.itemTypeT.pack(side=tk.LEFT, fill=tk.X)
            self.itemType.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriorityT.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriority.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDateT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDate.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatusT.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatus.pack(side=tk.LEFT, fill=tk.X)
            self.itemUserT.pack(side=tk.LEFT, fill=tk.X)
            self.itemUser.pack(side=tk.LEFT, fill=tk.X)
            self.itemSprintT.pack(side=tk.LEFT, fill=tk.X)
            self.itemSprint.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescriptionT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescription.pack(side=tk.LEFT, fill=tk.X)

            self.itemTypeF.pack(side=tk.TOP, fill=tk.X)
            self.itemPriorityF.pack(side=tk.TOP, fill=tk.X)
            self.itemDueDateF.pack(side=tk.TOP, fill=tk.X)
            self.itemStatusF.pack(side=tk.TOP, fill=tk.X)
            self.itemUserF.pack(side=tk.TOP, fill=tk.X)
            self.itemSprintF.pack(side=tk.TOP, fill=tk.X)
            self.itemDescriptionF.pack(side=tk.TOP, fill=tk.X)

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
        self.title.pack(fill=tk.X)
        self.cardDescriptions['Active'].pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.canvas.pack_forget()
        self.canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)


    def changeDescription(self, event):
        widget = event.widget
        self.eventSetTitle(widget)
        self.generateAdditionalFields(widget)
        self.repack()

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
            #If ListBox Select Isn't Properly Handled
            if match is None:
                self.resetToStart()
            else:
                self.generateUserFields(match)

        if self.datatype[widget] == 'Item':
            for item in self.dataBlock.items:
                if item.itemTitle == widget.get(tk.ANCHOR):
                    match = item
            # If ListBox Select Isn't Properly Handled
            if match is None:
                self.resetToStart()
            else:
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
        if selectedItem.itemPriority is not None and selectedItem.itemPriority != 0:
            self.cardDescriptions["Item"].itemPriority.configure(text=selectedItem.getPriority(), justify=tk.LEFT, wraplength=300)
        else:
            self.cardDescriptions["Item"].itemPriority.configure(text=selectedItem.itemPriority, justify=tk.LEFT, wraplength=300)
        if selectedItem.itemDueDate is not None:
            self.cardDescriptions["Item"].itemDueDate.configure(text=selectedItem.getFormattedDueDate(), justify=tk.LEFT, wraplength=300)
        else:
            self.cardDescriptions["Item"].itemDueDate.configure(text=selectedItem.itemDueDate, justify=tk.LEFT, wraplength=300)
        self.cardDescriptions["Item"].itemStatus.configure(text=selectedItem.getStatus(), justify=tk.LEFT, wraplength=300)
        self.cardDescriptions["Item"].itemDescription.configure(text=selectedItem.itemDescription, justify=tk.LEFT, wraplength=300)
        sprintName = ""
        for sprint in self.master.dataBlock.sprints:
            if sprint.sprintID == selectedItem.itemSprintID:
                sprintName = sprint.sprintName
        self.cardDescriptions["Item"].itemSprint.configure(text=sprintName, justify=tk.LEFT, wraplength=300)
        userName = ""
        for user in self.master.dataBlock.users:
            if user.userID == selectedItem.itemUserID:
                userName = user.userName
        self.cardDescriptions["Item"].itemUser.configure(text=userName, justify=tk.LEFT, wraplength=300)

        self.cardDescriptions["Item"].repack()

        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions["Item"]

    def resetToStart(self):
        self.titleText.set("Item Description")
        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions['Start']
        self.cardDescriptions['Active'].pack(side=tk.TOP)

class SUserItemInspection(tk.Frame):

    def __init__(self, controller, master):
        tk.Frame.__init__(self, controller)
        self.master = master
        self.controller = controller
        self.dataBlock = self.master.dataBlock

        self.textbox = tk.Frame(self)

        self.nametag = tk.Frame(self.textbox, relief=tk.SOLID, borderwidth=1)
        self.nameLabel = tk.Label(self.nametag, text="Name")
        self.nameString = tk.StringVar()
        self.nameText = tk.Label(self.nametag, textvariable=self.nameString)

        self.roletag = tk.Frame(self.textbox, relief=tk.SOLID, borderwidth=1)
        self.roleLabel = tk.Label(self.roletag, text="Role")
        self.roleString = tk.StringVar()
        self.roleText = tk.Label(self.roletag, textvariable=self.roleString)

        self.itembox = tk.Frame(self)
        self.inProgressItemsList = SList(self.itembox, "In Progress Items")
        self.submittedItemsList = SList(self.itembox, "Submitted Items")
        self.completedItemsList = SList(self.itembox, "Completed Items")

        self.nameLabel.pack(fill=tk.X)
        self.nameText.pack(fill=tk.X)
        self.roleLabel.pack(fill=tk.X)
        self.roleText.pack(fill=tk.X)

        self.nametag.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.roletag.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.inProgressItemsList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.submittedItemsList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.completedItemsList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.textbox.pack(side=tk.TOP, fill=tk.X)
        self.itembox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




    def update(self, user):
        self.nameString.set(user.userName)
        self.roleString.set(user.userRole)
        self.updateItems(user.listOfAssignedItems)

    def updateItems(self, assignedItems):
        inProgressItems = []
        submittedItems = []
        completedItems = []
        for item in assignedItems:
            if item.itemStatus == 1:
                inProgressItems.append(item)
            if item.itemStatus == 2:
                submittedItems.append(item)
            if item.itemStatus == 3:
                completedItems.append(item)
        self.updateInProgessItems(inProgressItems)
        self.updateSubmittedItems(submittedItems)
        self.updateCompletedItems(completedItems)

    def updateInProgessItems(self, inProgressItems):
        self.inProgressItemsList.importItemList(inProgressItems)

    def updateSubmittedItems(self, submittedItems):
        self.submittedItemsList.importItemList(submittedItems)

    def updateCompletedItems(self, completedItems):
        self.completedItemsList.importItemList(completedItems)

    def getSCardDescriptionExport(self):
        return [self.inProgressItemsList.listbox, self.submittedItemsList.listbox, self.completedItemsList.listbox], ['Item', 'Item', 'Item']

class STabs(tk.Frame):
    def __init__(self, controller, master, viewName):
        tk.Frame.__init__(self, controller)
        self.master = master
        self.controller = controller
        self.viewName = viewName
        self.buttonList = []
        self.generateButtons()

    class viewButton(tk.Button):
        def __init__(self, controller, viewName, view, event):
            if viewName == controller.viewName:
                tk.Button.__init__(self, controller, text=str(viewName), command=lambda: event(view), bg=style.scrumbles_offwhite, relief=tk.SOLID, borderwidth=1)
            else:
                tk.Button.__init__(self, controller, text=str(viewName), command=lambda: event(view), bg=style.scrumbles_grey, relief=tk.SOLID, borderwidth=1)

    def generateButtons(self):
        self.buttonList.clear()
        views, viewNames = self.master.getViews()
        for view, viewName in zip(views, viewNames):
            viewButton = self.viewButton(self, viewName, view, self.tabEvent)
            self.buttonList.append(viewButton)
            viewButton.pack(side=tk.LEFT)

    def tabEvent(self, selectedView):
        self.master.show_frame(selectedView)


