import tkinter as tk
from frames import ScrumblesFrames, listboxEventHandler


class adminMainView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selectedUser = None
        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Main")
        self.tabButtons.pack(side = tk.TOP, fill = tk.X)

        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'

        self.teamMembers = []
        self.allUsers = []

        self.userListsF = tk.Frame(self)
        self.userList = ScrumblesFrames.SList(self.userListsF, "USERS")
        self.memberList = ScrumblesFrames.SList(self.userListsF, "TEAM MEMBERS")

        self.dynamicF = tk.Frame(self)
        self.assignedItemInspect = ScrumblesFrames.SUserItemInspection(self, controller)

        self.dynamicSources, queryType = self.assignedItemInspect.getSCardDescriptionExport()
        self.descriptionManager = ScrumblesFrames.SCardDescription(self.dynamicF, controller, self.dynamicSources, queryType)
        self.recentComments = ScrumblesFrames.commentsField(self.dynamicF, self.controller)

        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        self.memberList.listbox.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))
        for source in self.dynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.inspectedItem = None
        self.memberList.listbox.bind('<2>' if self.aqua else '<3>', lambda event: self.memberPopup(event))
        self.userList.listbox.bind('<2>' if self.aqua else '<3>', lambda event: self.memberPopup(event))

        self.controller.dataBlock.packCallback(self.updateFrame)
        self.updateFrame()

        self.memberList.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.userList.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.userListsF.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        self.assignedItemInspect.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        self.dynamicF.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.descriptionManager.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.recentComments.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

    def updateFrame(self):
        self.teamMembers.clear()
        self.allUsers.clear()

        self.allUsers = [user.userName for user in self.controller.dataBlock.users]
        self.teamMembers = [user.userName for user in self.controller.activeProject.listOfAssignedUsers]
        self.userList.importList(self.allUsers)
        self.memberList.importList(self.teamMembers)
        self.descriptionManager.resetToStart()
        self.assignedItemInspect.update(self.selectedUser)
        self.recentComments.updateComments(self.selectedUser)

    def generateMemberMenus(self, widget):
        self.memberPopupMenu = tk.Menu(self, tearoff = 0)
        self.generateAddToProjectMenus()
        self.generateRemoveFromProjectMenus(widget)

    def generateAddToProjectMenus(self):
        projectOptions = tk.Menu(self.memberPopupMenu, 
                                 tearoff = 0, 
                                 cursor = "hand2")
        
        for project in self.controller.dataBlock.projects:
            if project not in self.inspectedItem.listOfProjects:
                projectOptions.add_command(label = project.projectName, 
                                           command = lambda project = project: 
                                           self.controller.dataBlock.addUserToProject(project, self.inspectedItem))

        self.memberPopupMenu.add_cascade(label = "Assign User To Project", menu = projectOptions)

    def generateRemoveFromProjectMenus(self, widget):
        assignedProjects = tk.Menu(self.memberPopupMenu, 
                                   tearoff = 0, 
                                   cursor = "hand2")
        
        if not self.inspectedItem.listOfProjects:
            assignedProjects.add_command(label = "[Empty]", 
                                         state = "disabled")
        if widget is self.userList.listbox:
            for project in self.inspectedItem.listOfProjects:
                assignedProjects.add_command(label = project.projectName,
                                             command = lambda project = project:
                                             self.controller.dataBlock.removeUserFromProject(project, self.inspectedItem))
        else:
            project = self.controller.activeProject
            assignedProjects.add_command(label=project.projectName,
                                         command=lambda project=project:
                                         self.controller.dataBlock.removeUserFromProject(project, self.inspectedItem))

        self.memberPopupMenu.add_cascade(label = "Remove User From Project",
                                         menu = assignedProjects)

    def listboxEvents(self, event):
        if event.widget is self.memberList.listbox:
            self.descriptionManager.resetToStart()
            self.recentComments.updateFromListOfCommentsObject(self.controller.activeProject.listOfAssignedUsers,
                                                               event.widget.get(tk.ANCHOR))

            for user in self.controller.dataBlock.users:
                if user.userName == event.widget.get(tk.ANCHOR):
                    self.assignedItemInspect.update(user)
                    self.selectedUser = user

        for source in self.dynamicSources:
            if event.widget is source:
                self.descriptionManager.changeDescription(event)
                self.recentComments.updateFromListOfCommentsObject(self.controller.activeProject.listOfAssignedItems,
                                                                   event.widget.get(tk.ANCHOR))

    def memberPopup(self, event):
        if self.controller.activeUser.userRole == "Developer":
            return
        
        widget = event.widget
        index = widget.nearest(event.y)
        try:
            _, yoffset, _, height = widget.bbox(index)
        except ValueError:
            return
        if event.y > height + yoffset + 5:
            return
        
        self.inspectedItem = widget.get(index)
        widget.selection_clear(0, tk.END)
        widget.selection_set(index)
        widget.activate(index)
        for user in self.controller.dataBlock.users:
            if user.userName == self.inspectedItem:
                self.inspectedItem = user
                
        self.generateMemberMenus(widget)
        self.memberPopupMenu.post(event.x_root, event.y_root)
