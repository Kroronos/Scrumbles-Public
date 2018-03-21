import tkinter as tk
import ScrumblesFrames
import listboxEventHandler

class teamView(tk.Frame):
    def __init__(self, parent, controller, user):
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.teamMembers = []

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Team View")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.memberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")
        self.assignedItemInspect = ScrumblesFrames.SUserItemInspection(self, controller)

        self.dynamicSources, queryType = self.assignedItemInspect.getSCardDescriptionExport()
        self.descriptionManager = ScrumblesFrames.SCardDescription(self, controller, self.dynamicSources, queryType)
        self.recentComments = ScrumblesFrames.commentsField(self)

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        self.memberList.listbox.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))
        for source in self.dynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.updateFrame()

        self.memberList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.assignedItemInspect.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.descriptionManager.pack(side=tk.LEFT, expand=True)
        self.recentComments.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def updateFrame(self):
        self.teamMembers.clear()
        self.teamMembers = [user.userName for user in self.controller.dataBlock.users]
        self.memberList.importList(self.teamMembers)

    def listboxEvents(self, event):
        if event.widget is self.memberList.listbox:
            self.descriptionManager.resetToStart()
            for user in self.controller.dataBlock.users:
                if user.userName == event.widget.get(tk.ANCHOR):
                    self.assignedItemInspect.update(user)
                    self.recentComments.updateFromListOfCommentsObject(user, user.userName)

        for source in self.dynamicSources:
            if event.widget is source:
                self.descriptionManager.changeDescription(event)
                for item in self.controller.dataBlock.items:
                    if item.itemTitle == event.widget.get(tk.ANCHOR):
                        self.recentComments.updateFromListOfCommentsObject(item, item.itemTitle)

