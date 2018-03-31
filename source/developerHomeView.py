import tkinter as tk
import ScrumblesFrames
import listboxEventHandler


class developerHomeView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Developer Home")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.itemColumnFrame = tk.Frame(self)
        self.userItemList = ScrumblesFrames.SList(self.itemColumnFrame, "MY ITEMS")
        self.productBacklogList = ScrumblesFrames.SBacklogListColor(self.itemColumnFrame,"BACKLOG")
        self.commentFeed = ScrumblesFrames.commentsField(self, self.controller)


        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")

        self.backlog = []
        self.teamMembers = []
        self.assignedItems = []
        self.selectedUser = None

        self.controller.dataBlock.packCallback(self.updateLists)
        self.updateLists()

        #Append Any Sources for Dynamic Events to this List
        dynamicSources = [self.productBacklogList.listbox, self.userItemList.listbox]
        queryType = ['Item', 'Item']
        self.descriptionManager = ScrumblesFrames.SCardDescription(self, controller, dynamicSources, queryType)

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        #Bind Sources
        for source in dynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.userItemList.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.productBacklogList.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.itemColumnFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.descriptionManager.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.commentFeed.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def updateLists(self):
        self.backlog.clear()
        self.teamMembers.clear()

        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemStatus == 0:
                self.backlog.append(item)

        self.teamMembers = [user.userName for user in self.controller.activeProject.listOfAssignedUsers]
        self.assignedItems = self.controller.activeUser.listOfAssignedItems

        self.productBacklogList.importItemList(self.backlog)
        self.userItemList.importItemList(self.assignedItems)

        self.commentFeed.updateComments()


    def listboxEvents(self, event):
        if event.widget is self.userItemList.listbox:
            self.descriptionManager.changeDescription(event)
            self.commentFeed.updateFromListOfCommentsObject(self.controller.activeProject.listOfAssignedItems,
                                                            event.widget.get(tk.ANCHOR))

        if event.widget is self.productBacklogList.listbox:
            self.descriptionManager.changeDescription(event)
            self.commentFeed.updateFromListOfCommentsObject(self.controller.activeProject.listOfAssignedItems,
                                                            event.widget.get(tk.ANCHOR))