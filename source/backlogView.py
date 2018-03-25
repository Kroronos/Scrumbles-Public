import tkinter as tk

import ScrumblesData
import ScrumblesObjects

import ScrumblesFrames
import Dialogs
import listboxEventHandler

import threading

#from tkinter import ttk

class backlogView(tk.Frame):
    def __init__(self, parent, controller,user):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.projectNameLabelText = tk.StringVar
        self.projectNameLabelText = ' %s Project Backlog View ' % self.controller.activeProject.projectName
        self.projectNameLabel = tk.Label(self, text=self.projectNameLabelText, font=("Verdana", 12))
        self.projectNameLabel.pack()
        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Backlog View")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)
        self.sprintList = ScrumblesFrames.SBacklogList(self, "SPRINTS")
        self.backlog = ScrumblesFrames.SBacklogList(self, "SPRINT BACKLOG")
        self.fullBacklog = ScrumblesFrames.SBacklogListColor(self,"ALL ITEMS")
        self.fullBacklog.importItemList(self.controller.activeProject.listOfAssignedItems)
        self.fullBacklog.pack(side=tk.LEFT, fill=tk.Y)


        self.sprintList = ScrumblesFrames.SBacklogList(self, "SPRINTS")
        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.sprintList.importSprintsList(self.sprintListData)
        self.sprintList.pack(side=tk.LEFT, fill=tk.Y)

        self.sprintBacklog = ScrumblesFrames.SBacklogList(self, "SPRINT BACKLOG")
        self.sprintBacklog.pack(side=tk.LEFT, fill=tk.Y)
        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'
        self.sprintBacklog.listbox.bind('<2>' if self.aqua else '<3>',lambda event: self.context_menu(event, self.contextMenu))




        self.contextMenu = tk.Menu()


        self.contextMenu.add_command(label=u'Update Item',command=self.updateItem)



        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.controller.dataBlock.packCallback(self.updateBacklogViewData)


        self.selectedSprint = None



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

    def updateItem(self):
        item = None
        title = self.itemTitle
        for i in self.controller.activeProject.listOfAssignedItems:
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
         self.itemTitle = widget.get(index)
         #print('do something')
         menu.post(event.x_root, event.y_root)





    def updateBacklogViewData(self):
        self.projectNameLabelText = ' %s Project Backlog View ' % self.controller.activeProject.projectName
        self.projectNameLabel['text'] = self.projectNameLabelText
        self.sprintList.clearList()
        self.sprintBacklog.clearList()
        self.fullBacklog.clearList()
        self.sprintListData = self.controller.activeProject.listOfAssignedSprints
        self.sprintList.importSprintsList(self.sprintListData)
        self.fullBacklog.importItemList(self.controller.activeProject.listOfAssignedItems)
        self.fullBacklog.colorCodeListboxes()



    def assignedSprintSelectedEvent(self, event):
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == event.widget.get(tk.ANCHOR):
                self.selectedSprint = sprint
                self.assignedItems = sprint.listOfAssignedItems
                self.sprintBacklog.importItemList(self.assignedItems)




    def listboxEvents(self, event):
        if event.widget is self.sprintList.listbox:
            self.assignedSprintSelectedEvent(event)



        #######################################################################
        ###Five freaking hours of troublshooting... I am a F@$%ing moron
        # right here.. Python PASSES OBJECTS AROUND BY REFERENCE
        #self.productListData.clear()  # <--- This clears dataBlock.projects GLOBALLY
        #self.backlogData.clear()      # <--- This clears dataBlock.items GLOBALLY
        #####################################################################

        ############### Below is completely Stupid,  these need to repack the frames
        # NEED CODE BELOW TO REPACK FRAMES NOT this
        #self.productListData = DB.projects # <-- this does nothing, this is the same as a = a
        #self.backlogData = DB.items #<-- this does nothing, this is the same as a = a
        #############################################################################
        #  This is why sleep deprivation and programming do not mix well
        ##############################################################################

