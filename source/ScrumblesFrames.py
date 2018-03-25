import tkinter as tk

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
        tk.Frame.__init__(self, controller)
        self.fullList = []

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
    def __init__(self, controller):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth=1)

        self.itemNumberLabel = tk.Label(self, text = "Item Number: ", justify = tk.LEFT).grid(row = 0)


        self.itemNameLabel = tk.Label(self, text = "Name: ", justify = tk.LEFT).grid(row = 1)
        self.itemNameEntry = tk.Entry(self).grid(row = 1, column = 1)

        self.itemDescriptionLabel =  tk.Label(self, text = "Description: ", justify = tk.LEFT).grid(row = 2)
        self.itemDescriptionEntry = tk.Entry(self).grid(row = 2, column = 1)


        self.itemWeightLabel = tk.Label( self, text = "Weight: ", justify = tk.LEFT, anchor = tk.W).grid(row = 3)
        #self.itemWeightSelector =
        # self.
        #self.itemWeightScroller = tk.Scrollbar

        self.itemStatusLabel = tk.Label(self, text = "Status: ", justify = tk.LEFT).grid(row = 4)
        self.itemStatusFrame = tk.Frame(self)
        #self.item


    def selectItem(self,text):
        self.itemNumberLabel.text = text

class commentsField(tk.Frame):
    def __init__(self,controller):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth=1)

        self.titleText = tk.StringVar()
        self.titleText.set("Comments")
        self.commentTitleF = tk.Frame(self,relief=tk.SOLID, borderwidth=1)
        self.commentTitle = tk.Label(self.commentTitleF, textvariable=self.titleText)
        self.commentField = tk.Frame(self)
        self.comments = []
        self.commentTextElements = []

        self.commentTitle.pack(side=tk.TOP, fill=tk.X)
        self.commentTitleF.pack(side=tk.TOP, fill=tk.X)
        self.commentField.pack(side=tk.TOP, fill=tk.BOTH)

    def updateFromListOfCommentsObject(self, listOfCommentsObject, objectName):
        self.clearCommentField()
        for comment in listOfCommentsObject.listOfComments:
            self.comments.append(comment)
        self.titleText.set("Comments from " + objectName)
        self.renderCommentField()

    def renderCommentField(self):
        self.comments = sorted(self.comments, key=lambda s: s.commentTimeStamp)
        for comment in self.comments:
            commentLabel = tk.Label(self.commentField, comment.commentContent)
            self.commentTextElements.append(commentLabel)
            commentLabel.pack(side=tk.top, fill=tk.X)
        self.commentField.pack(side=tk.TOP, fill=tk.BOTH)

    def clearCommentField(self):
        self.comments.clear()
        self.commentField.pack_forget()
        self.commentTextElements.clear()


class SCardDescription(tk.Frame):
    def __init__(self, controller, master, sources, datatype):
        tk.Frame.__init__(self, controller)
        self.master = master
        self.controller = controller
        self.dataBlock = master.dataBlock
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
        self.cardDescriptions['Active'].pack(side=tk.TOP)

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

            self.itemTypeT.pack(side=tk.LEFT, fill=tk.X)
            self.itemType.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriorityT.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriority.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDateT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDate.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatusT.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatus.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescriptionT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescription.pack(side=tk.LEFT, fill=tk.X)

            self.itemTypeF.pack(side=tk.TOP, fill=tk.X)
            self.itemPriorityF.pack(side=tk.TOP, fill=tk.X)
            self.itemDueDateF.pack(side=tk.TOP, fill=tk.X)
            self.itemStatusF.pack(side=tk.TOP, fill=tk.X)
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

            self.itemTypeF.pack_forget()
            self.itemPriorityF.pack_forget()
            self.itemDueDateF.pack_forget()
            self.itemStatusF.pack_forget()
            self.itemDescriptionF.pack_forget()

            self.itemTypeT.pack(side=tk.LEFT, fill=tk.X)
            self.itemType.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriorityT.pack(side=tk.LEFT, fill=tk.X)
            self.itemPriority.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDateT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDueDate.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatusT.pack(side=tk.LEFT, fill=tk.X)
            self.itemStatus.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescriptionT.pack(side=tk.LEFT, fill=tk.X)
            self.itemDescription.pack(side=tk.LEFT, fill=tk.X)

            self.itemTypeF.pack(side=tk.TOP, fill=tk.X)
            self.itemPriorityF.pack(side=tk.TOP, fill=tk.X)
            self.itemDueDateF.pack(side=tk.TOP, fill=tk.X)
            self.itemStatusF.pack(side=tk.TOP, fill=tk.X)
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
        self.cardDescriptions['Active'].pack(side=tk.TOP, fill=tk.BOTH)


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


