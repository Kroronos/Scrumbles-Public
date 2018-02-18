import tkinter as tk
import ScrumblesFrames
import ScrumblesData
import masterView


class developerHomeView(tk.Frame):
    def __init__(self, parent, controller, user):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.usernameLabel = tk.Label(self, text='Welcome to the Developer Home View ')
        self.usernameLabel.pack()

        self.productBacklogList = ScrumblesFrames.SList(self, "PRODUCT BACKLOG")
        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemList = ScrumblesFrames.SList(self, "ASSIGNED ITEMS")

        controller.dataConnection.connect()
        backlog = ScrumblesData.ScrumblesData.getData(controller.dataConnection, 'SELECT * FROM CardTable')
        backlog = [card['CardTitle'] for card in backlog]


        teamMembers = ScrumblesData.ScrumblesData.getData(controller.dataConnection, 'SELECT UserName FROM UserTable')
        teamMembers = [member['UserName'] for member in teamMembers]

        assignedItem = ScrumblesData.ScrumblesData.getData(controller.dataConnection, 'SELECT * FROM CardTable')
        assignedItem = [card['CardTitle'] for card in assignedItem]
        controller.dataConnection.close()

        self.productBacklogList.importList(backlog)
        self.teamMemberList.importList(teamMembers)
        self.assignedItemList.importList(assignedItem)

        self.productBacklogList.pack(side=tk.LEFT, fill=tk.Y)
        self.assignedItemList.pack(side=tk.RIGHT, fill=tk.Y)
        self.teamMemberList.pack(side=tk.RIGHT, fill=tk.Y)