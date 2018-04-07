import tkinter as tk
import SPopMenu
import ScrumblesFrames
import listboxEventHandler
import Dialogs
from tkinter import messagebox
import ScrumblesData

class sprintManagerView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.sprintPopMenu = SPopMenu.GenericPopupMenu(self,self.controller)
        roleMap = {'Developer':0,'Scrum Master':1,'Admin':2}
        activeRole = controller.activeUser.userRole
        if roleMap[activeRole] > 0:
            self.sprintPopMenu.add_command(label=u'Edit Sprint',
                                           command=self.editSprint)

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Sprint Manager")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.sprintList = ScrumblesFrames.SList(self, "SPRINTS")
        self.itemList = ScrumblesFrames.SBacklogListColor(self, "ITEMS",controller)
        self.subItemList = ScrumblesFrames.SBacklogListColor(self, "SUB-ITEMS",controller)

        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'

        self.sprintList.listbox.bind('<2>' if self.aqua else '<3>',
                                        lambda event: self.sprintPopMenu.context_menu(event, self.sprintPopMenu))

        self.sprints = []
        self.sprintItems = []
        self.sprintItemSubItems = []
        self.selectedSprint = None
        self.selectedItem = None
        self.selectedSubItem = None

        sprintDynamicSources = [self.sprintList.listbox]
        sprintQueryType = ['Sprint']
        self.sprintDescriptionManager = ScrumblesFrames.SCardDescription(self, controller, sprintDynamicSources, sprintQueryType)

        itemDynamicSources = [self.itemList.listbox, self.subItemList.listbox]
        itemQueryType = ['Item', 'Item']
        self.itemDescriptionManager = ScrumblesFrames.SCardDescription(self, controller, itemDynamicSources, itemQueryType)

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        #Bind Sources
        for source in itemDynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))
        for source in sprintDynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.sprintList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.sprintDescriptionManager.pack(side = tk.TOP, fill = tk.BOTH)
        self.itemList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.subItemList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.itemDescriptionManager.pack(side = tk.RIGHT, fill = tk.BOTH)

        self.updateSprintList()
        self.controller.dataBlock.packCallback(self.updateSprintList)
        self.controller.dataBlock.packCallback(self.updateLists)

    def editSprint(self):
        sprint = self.sprintPopMenu.getSelectedObject()
        if Dialogs.EditSprintDialog(self.controller,master=self.controller,
                                 dataBlock=self.controller.dataBlock,
                                 sprint=sprint).show():
            messagebox.showinfo('Success','Sprint Updated Successfully')
    def updateSprintList(self):
        self.sprints = []
        self.sprints = [sprint for sprint in self.controller.activeProject.listOfAssignedSprints]
        self.sprintList.importSprintsList(self.sprints)

    def updateLists(self):
        self.sprints = []
        self.sprintItems = []
        self.sprintItemSubItems = []

        self.sprintList.clearList()
        self.itemList.clearList()
        self.subItemList.clearList()

        self.sprints = [sprint for sprint in self.controller.activeProject.listOfAssignedSprints]
        self.sprintItems = [item for item in self.controller.activeProject.listOfAssignedItems]
        self.sprintItemSubItems = [item for item in self.controller.activeProject.listOfAssignedItems]

        self.sprintList.importSprintsList(self.sprints)
        self.itemList.importItemList(self.sprintItems)
        self.itemList.colorCodeListboxes()
        self.subItemList.importItemList(self.sprintItemSubItems)
        self.itemList.colorCodeListboxes()

    def assignedSprintEvent(self, event):
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == event.widget.get(tk.ANCHOR):
                self.selectedSprint = sprint
                self.sprintItems = sprint.listOfAssignedItems
                self.sprintItemSubItems = sprint.listOfAssignedItems
                self.itemList.importItemList(self.sprintItems)
                self.itemList.colorCodeListboxes()
                self.subItemList.importItemList(self.sprintItemSubItems)
                self.subItemList.colorCodeListboxes()

    def listboxEvents(self, event):
        if event.widget is self.sprintList.listbox:
            self.assignedSprintEvent(event)
            self.sprintDescriptionManager.changeDescription(event)

        if event.widget is self.itemList.listbox:
            self.itemDescriptionManager.changeDescription(event)

        if event.widget is self.subItemList.listbox:
            self.itemDescriptionManager.changeDescription(event)