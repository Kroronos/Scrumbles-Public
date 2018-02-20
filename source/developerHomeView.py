import tkinter as tk
import ScrumblesFrames
import ScrumblesData
import masterView


class developerHomeView(tk.Frame):
    def __init__(self, parent, controller, user):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.usernameLabel = tk.Label(self, text='Welcome to the Developer Home View ',font=("Verdana", 12))
        self.usernameLabel.pack()

        self.sprintGraph = ScrumblesFrames.SLineGraph(self)
        self.sprintGraph.setAxes("Sprint Day", "Cards Completed")
        self.sprintGraph.displayGraph()

        self.productBacklogList = ScrumblesFrames.SList(self, "PRODUCT BACKLOG")
        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemList = ScrumblesFrames.SList(self, "ASSIGNED ITEMS")

        controller.dataConnection.connect()
        self.backlog = controller.dataConnection.getData('SELECT * FROM CardTable')
        self.backlog = [card['CardTitle'] for card in self.backlog]


        self.teamMembers = controller.dataConnection.getData('SELECT UserName FROM UserTable')
        self.teamMembers = [member['UserName'] for member in self.teamMembers]

        self.assignedItem = controller.dataConnection.getData('SELECT * FROM CardTable')
        self.assignedItem = [card['CardTitle'] for card in self.assignedItem]
        controller.dataConnection.close()

        self.productBacklogList.importList(self.backlog)
        self.teamMemberList.importList(self.teamMembers)
        self.assignedItemList.importList(self.assignedItem)



        self.productBacklogList.importList(self.backlog)
        self.teamMemberList.importList(self.teamMembers)
        self.assignedItemList.importList(self.assignedItem)

        def updateLists():
            self.after(30000,updateLists)
            controller.dataConnection.connect()
            backlogCheck = controller.dataConnection.getData('SELECT * FROM CardTable')
            backlogCheck = [card['CardTitle'] for card in backlogCheck]

            teamMembersCheck = controller.dataConnection.getData('SELECT UserName FROM UserTable')
            teamMembersCheck = [member['UserName'] for member in teamMembersCheck]

            assignedItemCheck = controller.dataConnection.getData('SELECT * FROM CardTable')
            assignedItemCheck = [card['CardTitle'] for card in assignedItemCheck]
            
            controller.dataConnection.close()

            if (set(self.backlog) != set(backlogCheck)):
                self.backlog=backlogCheck
                self.productBacklogList.importList(self.backlog)

            if (set(self.teamMembers) != set(teamMembersCheck)):
                self.teamMembers=teamMembersCheck
                self.teamMemberList.importList(self.teamMembers)

            if (set(self.assignedItem) != set(assignedItemCheck)):
                self.assignedItem=assignedItemCheck
                self.assignedItemList.importList(self.assignedItem)

        updateLists()

        self.productBacklogList.pack(side=tk.LEFT, fill=tk.Y)
        self.assignedItemList.pack(side=tk.RIGHT, fill=tk.Y)
        self.teamMemberList.pack(side=tk.RIGHT, fill=tk.Y)
        self.sprintGraph.pack(side=tk.BOTTOM, fill=tk.X)