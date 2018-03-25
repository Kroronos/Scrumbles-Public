import tkinter as tk
import ScrumblesFrames
import listboxEventHandler


class developerHomeView(tk.Frame):
    def __init__(self, parent, controller, user):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.firstCall = True

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Developer Home View")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.cal = ScrumblesFrames.SCalendar(self)

        self.sprintGraph = ScrumblesFrames.SLineGraph(self)
        self.sprintGraph.setAxes("Sprint Day", "Cards Completed")
        self.sprintGraph.displayGraph()

        self.productBacklogList = ScrumblesFrames.SList(self, "PRODUCT BACKLOG")
        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemList = ScrumblesFrames.SList(self, "ASSIGNED ITEMS")

        self.backlog = []
        self.teamMembers = []
        self.assignedItems = []
        self.selectedUser = None

        self.controller.dataBlock.packCallback(self.updateLists)
        self.updateLists()

        #Append Any Sources for Dynamic Events to this List
        dynamicSources = [self.productBacklogList.listbox, self.teamMemberList.listbox, self.assignedItemList.listbox]
        queryType = ['Item', 'User', 'Item']
        self.descriptionManager = ScrumblesFrames.SCardDescription(self, controller, dynamicSources, queryType)

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        #Bind Sources
        for source in dynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.productBacklogList.pack(side=tk.LEFT, fill=tk.Y)
        self.assignedItemList.pack(side=tk.RIGHT, fill=tk.Y)
        self.teamMemberList.pack(side=tk.RIGHT, fill=tk.Y)
        #self.descriptionManager.pack_propagate(0)
        #self.descriptionManager.config(height=100, width=100)
        self.descriptionManager.pack(side=tk.TOP, fill=tk.BOTH, expand=True, ipadx=10, ipady=10)
        self.cal.pack(side=tk.TOP, fill=tk.BOTH)
        self.sprintGraph.pack(side=tk.BOTTOM, fill=tk.X)

    def assignedItemEvent(self, event):
        for user in self.controller.dataBlock.users:
            if user.userName == event.widget.get(tk.ANCHOR):
                self.selectedUser = user
                self.assignedItems = user.listOfAssignedItems
                self.assignedItemList.importItemList(self.assignedItems)


    def updateLists(self):
        self.backlog.clear()
        self.teamMembers.clear()

        self.backlog = [item.itemTitle for item in self.controller.dataBlock.items]
        self.teamMembers = [user.userName for user in self.controller.dataBlock.users]
        if self.selectedUser is not None:
            self.assignedItems = self.selectedUser.listOfAssignedItems
        self.productBacklogList.importList(self.backlog)
        self.teamMemberList.importList(self.teamMembers)
        self.assignedItemList.importItemList(self.assignedItems)

    def listboxEvents(self, event):
        if event.widget is self.teamMemberList.listbox:
            self.assignedItemEvent(event)
            self.descriptionManager.changeDescription(event)

        if event.widget is self.productBacklogList.listbox:
            self.descriptionManager.changeDescription(event)

        if event.widget is self.assignedItemList.listbox:
            self.descriptionManager.changeDescription(event)


