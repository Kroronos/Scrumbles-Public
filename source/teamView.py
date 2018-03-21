import tkinter as tk
import ScrumblesFrames
import listboxEventHandler

class teamView(tk.Frame):
    def __init__(self, parent, controller, user):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.teamMembers = []

        self.memberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemInspect = ScrumblesFrames.SUserItemInspection(self)

        self.dynamicSources, queryType = self.assignedItemInspect.getSCardDescriptionExport()
        self.descriptionManager = ScrumblesFrames.SCardDescription(self, self.dynamicSources, queryType)

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        self.memberList.listbox.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))
        for source in self.dynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.updateFrame()

        self.memberList.pack(side=tk.LEFT, fill=tk.Y)
        self.assignedItemInspect.pack(side=tk.LEFT, fill=tk.BOTH)
        self.descriptionManager.pack(side=tk.LEFT)

    def updateFrame(self):
        self.teamMembers.clear()

        self.teamMembers = [user.userName for user in self.controller.dataBlock.users]
        print(self.teamMembers)
        self.memberList.importList(self.teamMembers)

    def listboxEvents(self, event):
        if event.widget is self.memberList.listbox:
            self.descriptionManager.resetToStart()
            for user in self.controller.dataBlock.users:
                if user.userName == event.widget.get(tk.ANCHOR):
                    self.assignedItemInspect.update(user.listOfAssignedItems)

        for source in self.dynamicSources:
            if event.widget is source:
                self.descriptionManager.changeDescription(event)

