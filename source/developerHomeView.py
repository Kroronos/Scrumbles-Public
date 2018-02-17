import tkinter as tk
import ScrumblesFrames
import ScrumblesData
import masterView


class developerHomeView(tk.Frame):
    def __init__(self, parent, controller,user):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.usernameLabel = tk.Label(self, text='Welcome to the Developer Home View ')
        self.usernameLabel.pack()

        self.productBacklogList = ScrumblesFrames.SList(self, "PRODUCT BACKLOG")
        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemList = ScrumblesFrames.SList(self, "ASSIGNED ITEMS")

        backlog = ["GUI", "Styling File", "Hashing", "Encrypted Database", "Global Macros"]
        teamMember = ["Anthony", "Kathy", "Liu", "Dave", "Josh", "Kayla"]
        assignedItem = ["Processing", "Statistics", "UML Diagram", "Use Cases", "Refactor", "User Stories"]

        self.productBacklogList.importList(backlog)
        self.teamMemberList.importList(teamMember)
        self.assignedItemList.importList(assignedItem)

        self.productBacklogList.pack(side=tk.LEFT, fill=tk.Y)
        self.assignedItemList.pack(side=tk.RIGHT, fill=tk.Y)
        self.teamMemberList.pack(side=tk.RIGHT, fill=tk.Y)