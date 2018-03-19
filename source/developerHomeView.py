import tkinter as tk
import ScrumblesFrames



class developerHomeView(tk.Frame):
    def __init__(self, parent, controller, user):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.firstCall = True
        self.usernameLabel = tk.Label(self, text='Welcome to the Developer Home View ',font=("Verdana", 12))
        self.usernameLabel.pack()

        self.cal = ScrumblesFrames.SCalendar(self)

        self.sprintGraph = ScrumblesFrames.SLineGraph(self)
        self.sprintGraph.setAxes("Sprint Day", "Cards Completed")
        self.sprintGraph.displayGraph()

        self.productBacklogList = ScrumblesFrames.SList(self, "PRODUCT BACKLOG")
        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemList = ScrumblesFrames.SList(self, "ASSIGNED ITEMS")
        #todo Fix this *BLEEPING* Binding -_-
        self.assignedItemList.listbox.bind('<<ListboxSelect>>', lambda event: self.getItemsAssignedToUser(event))
        #self.assignedItemList.bind('<<ListboxSelect>>', lambda event: self.getItemsAssignedToUser(event)) doesn't work
        self.backlog = []
        self.teamMembers = []
        self.assignedItems = []
        self.controller.dataBlock.packCallback(self.updateLists)
        self.updateLists()

        self.productBacklogList.pack(side=tk.LEFT, fill=tk.Y)
        self.assignedItemList.pack(side=tk.RIGHT, fill=tk.Y)
        self.teamMemberList.pack(side=tk.RIGHT, fill=tk.Y)
        self.cal.pack(side=tk.TOP, fill=tk.BOTH)
        self.sprintGraph.pack(side=tk.BOTTOM, fill=tk.X)

    def getItemsAssignedToUser(self,event=None,userName=None):
        userIndex = 0
        if event is not None:
            print(event)
            widget = event.widget
            index = widget.nearest(event.y)
            userName = widget.get(index)
        for index in range(len(self.controller.dataBlock.users)):
            if userName == self.controller.dataBlock.users[index].userName:
                userIndex = index
            else:
                userIndex = 0


        userID = self.controller.dataBlock.users[userIndex].userID
        self.assignedItems.clear()
        for item in self.controller.dataBlock.items:
            if item.itemUserID == userID:
                self.assignedItems.append(item.itemTitle)


    def updateLists(self):

        selectedUserName = self.controller.dataBlock.users[0].userName


        self.backlog.clear()
        self.teamMembers.clear()
        self.assignedItems.clear()
        self.backlog = [item.itemTitle for item in self.controller.dataBlock.items]
        self.teamMembers = [user.userName for user in self.controller.dataBlock.users]

        self.getItemsAssignedToUser(None,selectedUserName)
        self.productBacklogList.importList(self.backlog)
        self.teamMemberList.importList(self.teamMembers)
        self.assignedItemList.importList(self.assignedItems)



