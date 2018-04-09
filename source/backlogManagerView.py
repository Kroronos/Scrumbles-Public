import tkinter as tk
import ScrumblesFrames, SPopMenu, Dialogs, listboxEventHandler


class backlogManagerView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        userRoleMap = controller.activeUser.userRoleMap
        self.activeRole = userRoleMap[self.controller.activeUser.userRole]

        self.selectedItem = None
        self.selectedSprint = None

        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'


        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Backlog Manager")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.projectNameLabelText = tk.StringVar
        self.projectNameLabelText = ' %s Project Backlog View ' % self.controller.activeProject.projectName
        self.projectNameLabel = tk.Label(self, text=self.projectNameLabelText, font=("Verdana", 12))
        self.projectNameLabel.pack()

        self.sprintList = ScrumblesFrames.SBacklogList(self, "SPRINTS")
        self.backlog = ScrumblesFrames.SBacklogList(self, "SPRINT BACKLOG")
        self.fullBacklog = ScrumblesFrames.SBacklogListColor(self,"ALL ITEMS")
        self.fullBacklog.importItemList(self.controller.activeProject.listOfAssignedItems)
        self.fullBacklog.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if self.activeRole > 0:
            self.listOfEpics = [I for I in self.controller.activeProject.listOfAssignedItems if I.itemType == 'Epic']
            self.fullBacklog.listbox.bind('<2>' if self.aqua else '<3>',
                                            lambda event: self.popMenu.context_menu(event, self.popMenu))

            self.popMenu = SPopMenu.BacklogManPopMenu(self,self.controller,self.listOfEpics)
            self.popMenu.add_command(label=u'Update Item', command=self.updateItem)


        self.sprintList = ScrumblesFrames.SBacklogList(self, "SPRINTS")
        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.sprintList.importSprintsList(self.sprintListData)
        self.sprintList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sprintBacklog = ScrumblesFrames.SBacklogList(self, "SPRINT BACKLOG")
        self.sprintBacklog.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if self.activeRole > 0:
            self.sprintBacklog.listbox.bind('<2>' if self.aqua else '<3>',lambda event: self.popMenu.context_menu(event, self.popMenu))


        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.controller.dataBlock.packCallback(self.updateBacklogViewData)
        self.updateBacklogViewData()



        #Append Any Sources for Dynamic Events to this List
        dynamicSources = [self.sprintList.listbox, self.fullBacklog.listbox]#ADD ITEMS HERE

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)
        self.fullBacklog.colorCodeListboxes()



        #Bind Sources
        for source in dynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))


    def updateItem(self):
        item = None
        title = self.selectedItem
        for i in self.controller.dataBlock.items:
            if i.itemTitle == title:
               item = i

        if item is None:
            print('Item Title:',title)
            print('backlogData:')
            for i in self.controller.activeProject.listOfAssignedItems:
                print(i.itemTitle)
            raise Exception('Error Loading item from title')

        Dialogs.EditItemDialog(self.controller, master=self.controller, dataBlock=self.controller.dataBlock ,item=item).show()

    def updateBacklogViewData(self):
        print('Calling updateBacklogViewData')
        self.listOfEpics = []
        self.projectNameLabelText = ' %s Project Backlog View ' % self.controller.activeProject.projectName
        self.projectNameLabel['text'] = self.projectNameLabelText

        self.sprintList.clearList()

        self.sprintBacklog.clearList()

        self.fullBacklog.clearList()

        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.sprintList.importSprintsList(self.sprintListData)

        self.fullBacklog.importItemList(self.controller.activeProject.listOfAssignedItems)
        self.fullBacklog.colorCodeListboxes()
        if self.activeRole > 0:
            self.listOfEpics = [ I for I in self.controller.activeProject.listOfAssignedItems if I.itemType == 'Epic']
            self.popMenu.updateEpicsMenu()



    def assignedSprintSelectedEvent(self, event):
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == event.widget.get(tk.ANCHOR):
                self.selectedSprint = sprint
                self.assignedItems = sprint.listOfAssignedItems
                self.sprintBacklog.importItemList(self.assignedItems)
                self.sprintBacklog.colorCodeListboxes()




    def listboxEvents(self, event):
        if event.widget is self.sprintList.listbox:
            self.assignedSprintSelectedEvent(event)


    def __str__(self):
        return 'Scrumbles Backlog Manger View'