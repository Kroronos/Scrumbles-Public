import tkinter as tk
import tkcalendar
import ScrumblesData
import masterView
import ScrumblesFrames

from tkinter import ttk
class mainView(tk.Frame):
    def __init__(self, parent, controller,user):
        tk.Frame.__init__(self, parent)

        self.usernameLabel = tk.Label(self, text='Welcome to the Main View ', font=("Verdana", 12))
        self.usernameLabel.pack()
        self.productBacklogList = ScrumblesFrames.SList(self, "PRODUCT BACKLOG")
        self.scrumTeamList = ScrumblesFrames.SList(self, "SCRUM TEAMS")
        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemList = ScrumblesFrames.SList(self, "ASSIGNED ITEMS")
        self.cal = tkcalendar.Calendar(self,font="Arial 14", selectmode='day',cursor="hand1", year=2018, month=2, day=5)

        self.sprintGraph = ScrumblesFrames.SLineGraph(self)
        self.sprintGraph.setAxes("Sprint Day", "Cards Completed")
        self.sprintGraph.displayGraph()


        controller.dataConnection.connect()
        backlog = controller.dataConnection.getData('SELECT * FROM CardTable')
        backlog = [card['CardTitle'] for card in backlog]

        scrumTeams = [] #needs database query

        teamMembers = controller.dataConnection.getData('SELECT UserName FROM UserTable')
        teamMembers = [member['UserName'] for member in teamMembers]

        assignedItem = controller.dataConnection.getData('SELECT * FROM CardTable')
        assignedItem = [card['CardTitle'] for card in assignedItem]
        

        controller.dataConnection.close()

        self.productBacklogList.importList(backlog)
        self.scrumTeamList.importList(scrumTeams)
        self.teamMemberList.importList(teamMembers)
        self.assignedItemList.importList(assignedItem)

        self.productBacklogList.pack(side=tk.LEFT, fill=tk.Y)
        self.assignedItemList.pack(side=tk.RIGHT, fill=tk.Y)
        self.teamMemberList.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrumTeamList.pack(side=tk.RIGHT, fill=tk.Y)
        self.cal.pack(side=tk.TOP, fill=tk.BOTH)
        self.sprintGraph.pack(side=tk.BOTTOM, fill=tk.X)