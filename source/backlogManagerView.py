import tkinter as tk
from tkinter import messagebox
import ScrumblesData
import ScrumblesObjects

import ScrumblesFrames
import Dialogs
import listboxEventHandler
import time
import threading

#from tkinter import ttk

class backlogManagerView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selectedItem = None
        self.selectedSprint = None
        self.listOfEpics = []
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
        self.fullBacklog.pack(side=tk.LEFT, fill=tk.Y)
        self.fullBacklog.listbox.bind('<2>' if self.aqua else '<3>',
                                        lambda event: self.context_menu(event, self.contextMenu))


        self.sprintList = ScrumblesFrames.SBacklogList(self, "SPRINTS")
        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.sprintList.importSprintsList(self.sprintListData)
        self.sprintList.pack(side=tk.LEFT, fill=tk.Y)

        self.sprintBacklog = ScrumblesFrames.SBacklogList(self, "SPRINT BACKLOG")
        self.sprintBacklog.pack(side=tk.LEFT, fill=tk.Y)

        self.sprintBacklog.listbox.bind('<2>' if self.aqua else '<3>',lambda event: self.context_menu(event, self.contextMenu))




        self.contextMenu = tk.Menu(tearoff=0)

        self.contextMenu.add_command(label=u'Update Item',command=self.updateItem)
        self.contextMenu.add_command(label=u'Promote To Epic',command=self.promoteItemToEpic)
        self.setEpicsMenu(self.contextMenu)


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

        #todo Click on project name to display items in sprintBacklog
        #todo click and drag on items in sprintBacklog to change priority variable of an item so that sort will be user defined

    def colorizeBackLogList(self):
        for index in range(len(self.controller.activeProject.listOfAssignedItems)):
            for S in self.controller.activeProject.listOfAssignedSprints:
                if self.controller.activeProject.listOfAssignedItems[index] in S.listOfAssignedItems:
                    self.fullBacklog.listbox.itemconfig(index,{'bg': 'firebrick'})
                    self.fullBacklog.listbox.itemconfig(index,{'fg': 'red'})
                else:
                    self.fullBacklog.listbox.itemconfig(index,{'bg' : 'dark green'})
                    self.fullBacklog.listbox.itemconfig(index,{'fg' : 'lawn green'})


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



        editUserDialog = Dialogs.EditItemDialog(self, self.controller.dataBlock ,item)
        self.wait_window(editUserDialog.top)



    def context_menu(self,event,menu):
         widget = event.widget
         index = widget.nearest(event.y)
         _, yoffset, _, height = widget.bbox(index)
         if event.y > height + yoffset + 5:
             return
         self.selectedItem = widget.get(index)
         #print('do something')
         menu.post(event.x_root, event.y_root)





    def updateBacklogViewData(self):
        print('Calling updateBacklogViewData')

        self.projectNameLabelText = ' %s Project Backlog View ' % self.controller.activeProject.projectName
        self.projectNameLabel['text'] = self.projectNameLabelText
        self.sprintList.clearList()
        self.sprintBacklog.clearList()
        self.fullBacklog.clearList()
        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.sprintList.importSprintsList(self.sprintListData)
        self.fullBacklog.importItemList(self.controller.activeProject.listOfAssignedItems)
        self.fullBacklog.colorCodeListboxes()
        self.listOfEpics = [ I for I in self.controller.activeProject.listOfAssignedItems if I.itemType == 'Epic']
        self.updateEpicsMenu()



    def assignedSprintSelectedEvent(self, event):
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == event.widget.get(tk.ANCHOR):
                self.selectedSprint = sprint
                self.assignedItems = sprint.listOfAssignedItems
                self.sprintBacklog.importItemList(self.assignedItems)




    def listboxEvents(self, event):
        if event.widget is self.sprintList.listbox:
            self.assignedSprintSelectedEvent(event)

    def promoteItemToEpic(self):
        item = None
        title = self.selectedItem
        for i in self.controller.dataBlock.items:
            if i.itemTitle == title:
                item = i

        if item is None:
            print('Item Title:', title)
            print('backlogData:')
            for i in self.controller.activeProject.listOfAssignedItems:
                print(i.itemTitle)
            raise Exception('Error Loading item from title')

        self.controller.dataBlock.promoteItemToEpic(item)

    def updateEpicsMenu(self):
        self.setEpicsMenu(self.contextMenu)

    def setEpicsMenu(self,menu):

        listOfEpics = [E.itemTitle for E in self.listOfEpics]
        print(listOfEpics)
        try:
            menu.delete('Assign To Epic')
        except Exception:
           pass

        self.popMenu = tk.Menu(menu,tearoff=0)
        for text in listOfEpics:
            self.popMenu.add_command(label=text,command = lambda t=text:self.assignItemToEpic(t))

        menu.add_cascade(label='Assign To Epic',menu=self.popMenu,underline=0)

    def assignItemToEpic(self,epicName):

        epic = None
        item = None
        for I in self.controller.activeProject.listOfAssignedItems:
            if I.itemTitle == epicName:
                epic = I
            if I.itemTitle == self.selectedItem:
                item = I

        try:
            if self.isItemAlreadyInAnEpic(item):
                self.controller.dataBlock.reAssignItemToEpic(item,epic)
            else:
                self.controller.dataBlock.addItemToEpic(item, epic)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def isItemAlreadyInAnEpic(self,item):
        listOfItemsInAnEpic = []
        for I in self.controller.dataBlock.items:
            if I.itemType == 'Epic':
                for subItem in I.subItemList:
                    listOfItemsInAnEpic.append(subItem)
        return item in listOfItemsInAnEpic
