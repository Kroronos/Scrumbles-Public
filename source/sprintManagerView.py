import tkinter as tk

import ScrumblesFrames
import listboxEventHandler
import ScrumblesData

class sprintManagerView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Sprint Manager")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.sprintList = ScrumblesFrames.SList(self, "SPRINTS")
        self.itemList = ScrumblesFrames.SList(self, "ITEMS")
        self.subItemList = ScrumblesFrames.SList(self, "SUB-ITEMS")

        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'

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

    def updateSprintList(self):
        self.sprints.clear()
        self.sprints = [sprint for sprint in self.controller.dataBlock.sprints]
        self.sprintList.importSprintsList(self.sprints)

    def updateLists(self):
        self.sprints.clear()
        self.sprintItems.clear()
        self.sprintItemSubItems.clear()

        self.sprints = [sprint for sprint in self.controller.dataBlock.sprints]
        self.sprintItems = [item for item in self.controller.dataBlock.items]
        self.sprintItemSubItems = [item for item in self.controller.dataBlock.items]

        self.sprintList.importSprintsList(self.sprints)
        self.itemList.importItemList(self.sprintItems)
        self.subItemList.importItemList(self.sprintItemSubItems)

    def assignedSprintEvent(self, event):
        for sprint in self.controller.dataBlock.sprints:
            if sprint.sprintName == event.widget.get(tk.ANCHOR):
                self.selectedSprint = sprint
                self.sprintItems = sprint.listOfAssignedItems
                self.sprintItemSubItems = sprint.listOfAssignedItems
                self.itemList.importItemList(self.sprintItems)
                self.subItemList.importItemList(self.sprintItemSubItems)

    def listboxEvents(self, event):
        if event.widget is self.sprintList.listbox:
            self.assignedSprintEvent(event)
            self.sprintDescriptionManager.changeDescription(event)

        if event.widget is self.itemList.listbox:
            self.itemDescriptionManager.changeDescription(event)

        if event.widget is self.subItemList.listbox:
            self.itemDescriptionManager.changeDescription(event)