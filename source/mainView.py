import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ScrumblesFrames, SPopMenu,ScrumblesObjects,Dialogs
import listboxEventHandler
from styling import styling as style
import logging
import tkinter as tk
import Dialogs

class mainViewPopup(SPopMenu.GenericPopupMenu):
    def __init__(self,root,Master):
        super().__init__(root,Master)
        self.isAssignDeleted = False


    def context_menu(self, event, menu):
        self.widget = event.widget
        self.event = event
        index = self.widget.nearest(event.y)
        _, yoffset, _, height = self.widget.bbox(index)
        if event.y > height + yoffset + 5:
            return
        self.selectedObject = self.widget.get(index)

        self.selectedObject = self.findSelectedObject(self.selectedObject)
        try:
            self.root.selectedItem = self.selectedObject
        except:
            pass
        # for i in range(5):
        #     print('index %i = %s'%(i,str(self.index(i))))
        try:
            self.delete(u'Approve Item')
        except Exception as e:
            pass
        if self.root.roleMap[self.root.activeRole] > 0:
            if self.index(0) is None:
                self.usersMenu = tk.Menu(self, tearoff=0)
                self.usersMenuEpic = tk.Menu(self, tearoff=0)
                self.usersMenuSprint = tk.Menu(self, tearoff=0)

                self.add_cascade(label=u'Assign to User', menu=self.usersMenu)

                for name in [U.userName for U in self.master.activeProject.listOfAssignedUsers]:
                    self.usersMenu.add_command(label=name, command=lambda n=name:self.root.assignToUser(n))

                self.listOfSprints = [S for S in self.master.activeProject.listOfAssignedSprints]
                self.add_cascade(label=u'Assign to Sprint', menu=self.usersMenuSprint)

                for name in [S.sprintName for S in self.listOfSprints]:
                    self.usersMenuSprint.add_command(label=name, command=lambda n=name:self.root.assignToSprint(n))


                self.listOfEpics = [I for I in self.master.activeProject.listOfAssignedItems if I.itemType == 'Epic']
                self.add_cascade(label=u'Assign to Epic', menu=self.usersMenuEpic)

                for name in [I.itemTitle for I in self.listOfEpics]:
                    self.usersMenuEpic.add_command(label=name, command=lambda n=name:self.root.assignToEpic(n))


                self.add_command(label=u'Edit Item',
                                           command=self.root.updateItem)
                self.add_command(label=u'Delete Item',
                                           command=self.root.deleteItem)

            if self.selectedObject.itemStatus == 3:
                print (self.index(0))
                self.add_command(label=u'Approve Item', command=self.root.approveItem)

            if self.selectedObject.itemStatus == 3:
                self.add_command(label=u'Reject Item', command=self.root.rejectItem)


        self.widget.selection_clear(0, tk.END)
        self.widget.selection_set(index)
        self.widget.activate(index)
        menu.post(event.x_root, event.y_root)


    def getSelectedObject(self):
        return self.selectedObject




class mainView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'

        self.tabButtons = ScrumblesFrames.STabs(self, controller, user.userRole + " Home")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.activeProject = controller.activeProject

        self.roleMap = {'Developer':0,'Scrum Master':1,'Admin':2}
        self.activeRole = controller.activeUser.userRole
        

        self.fullBacklog = ScrumblesFrames.SBacklogListColor(self,"ALL ITEMS", controller)
        self.sprintList = ScrumblesFrames.SList(self, "SPRINTS")
        self.itemList = ScrumblesFrames.SBacklogListColor(self, "ITEMS",controller)
        self.subItemList = ScrumblesFrames.SBacklogListColor(self, "SUB-ITEMS",controller)

        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'
        self.FBPopMenu= None
        self.sprintPopMenu = None
        self.itemPopMenu= None
        self.subItemPopMenu= None

        self.generatePopupThing()



        self.sprints = []
        self.sprintItems = []
        self.sprintItemSubItems = []

        self.selectedFB = None
        self.selectedSprint = None
        self.selectedItem = None
        self.selectedSubItem = None

        sprintDynamicSources = [self.sprintList.listbox]
        sprintQueryType = ['Sprint']
        self.sprintDescriptionManager = ScrumblesFrames.SCardDescription(self, controller, sprintDynamicSources, sprintQueryType)

        itemDynamicSources = [self.fullBacklog.listbox, self.itemList.listbox, self.subItemList.listbox]
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


        self.fullBacklog.listbox.bind('<2>' if self.aqua else '<3>',
                                        lambda event: (self.generatePopupThing(), self.FBPopMenu.context_menu(event, self.FBPopMenu)))
        self.sprintList.listbox.bind('<2>' if self.aqua else '<3>',
                                        lambda event: (self.generatePopupThing(), self.sprintPopMenu.context_menu(event, self.sprintPopMenu)))
        self.itemList.listbox.bind('<2>' if self.aqua else '<3>',
                                   lambda event: (self.generatePopupThing(), self.itemPopMenu.context_menu(event,self.itemPopMenu)))
        self.subItemList.listbox.bind('<2>' if self.aqua else '<3>',
                                   lambda event: (self.generatePopupThing(), self.subItemPopMenu.context_menu(event, self.subItemPopMen)))

        
        self.fullBacklog.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sprintList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.sprintDescriptionManager.pack(side = tk.TOP, fill = tk.BOTH)
        self.itemList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.subItemList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.itemDescriptionManager.pack(side = tk.RIGHT, fill = tk.BOTH)

        self.updateSprintList()
        self.updateLists()
        self.controller.dataBlock.packCallback(self.updateSprintList)
        self.controller.dataBlock.packCallback(self.updateLists)
    def generatePopupThing(self):

        self.FBPopMenu= mainViewPopup(self,self.controller)
        self.sprintPopMenu = SPopMenu.GenericPopupMenu(self,self.controller)
        if self.roleMap[self.activeRole] > 0:
            self.sprintPopMenu.add_command(label=u'Edit Sprint',
                                           command=self.editSprint)
            self.sprintPopMenu.add_command(label=u'Delete Sprint',
                                           command=self.deleteSprint)


        self.itemPopMenu= mainViewPopup(self,self.controller)
        self.subItemPopMenu= mainViewPopup(self,self.controller)

    def approveItem(self):
        item = None

        try:
            title = self.selectedItem.itemTitle
            for i in self.controller.dataBlock.items:
                if i.itemTitle == title:
                    item = i
            self.controller.dataBlock.modifyItemStatus(item, item.statusTextToNumberMap['Complete'])
            comment = ScrumblesObjects.Comment()
            comment.commentContent = '%s Has Approved Item' % self.controller.activeUser.userName
            comment.commentItemID = item.itemID
            comment.commentUserID = self.controller.activeUser.userID
            self.controller.dataBlock.addNewScrumblesObject(comment)
        except Exception as e:
            logging.exception('Could not assign item to Complete')
            messagebox.showerror('Error',str(e))

        messagebox.showinfo('Success','Item Approved')

    def rejectItem(self):
        item = None


        try:
            title = self.selectedItem.itemTitle
            for i in self.controller.dataBlock.items:
                if i.itemTitle == title:
                    item = i
            self.controller.dataBlock.modifyItemStatus(item, item.statusTextToNumberMap['In Progress'])
            comment = ScrumblesObjects.Comment()
            comment.commentContent = '%s Has Rejected Item' % self.controller.activeUser.userName
            comment.commentItemID = item.itemID
            comment.commentUserID = self.controller.activeUser.userID
            self.controller.dataBlock.addNewScrumblesObject(comment)
        except Exception as e:
            logging.exception('Could not assign item to Complete')
            messagebox.showerror('Error',str(e))

        messagebox.showinfo('Success','Item Rejected')

    def assignToUser(self,username):
        user = None

        if messagebox.askyesno('Assign To User','Do you wish to assign item to user %s?'%username):
            for U in self.controller.dataBlock.users:
                if U.userName == username:
                    user = U

            if user is not None:

                try:
                    title = self.selectedItem.itemTitle
                    for i in self.controller.dataBlock.items:
                        if i.itemTitle == title:
                            item = i

                    assert item is not None
                    self.controller.dataBlock.assignUserToItem(user,item)
                    comment = ScrumblesObjects.Comment()
                    comment.commentContent = '%s Has Assigned User %s to Item' % (self.controller.activeUser.userName, user.userName)
                    comment.commentItemID = item.itemID
                    comment.commentUserID = self.controller.activeUser.userID
                    self.controller.dataBlock.addNewScrumblesObject(comment)
                except Exception as e:
                    messagebox.showerror('Error',str(e))
                    logging.exception('Error assigning user %s to item'%username)
                    return
                messagebox.showinfo('Success','Item Assigned to User %s'%user.userName)


            else:
                messagebox.showerror('Error','User not found in DataBlock')
                logging.error('User %s not found in dataBlock'%username)

    def assignToSprint(self,Insprint):
        sprint = None

        if messagebox.askyesno('Assign To Sprint','Do you wish to assign item to sprint %s?'%Insprint):
            for I in self.controller.activeProject.listOfAssignedSprints:
                if I.sprintName == Insprint:
                    sprint = I
            if sprint is not None:
                try:
                    title = self.selectedItem.itemTitle
                    for i in self.controller.dataBlock.items:
                        if i.itemTitle == title:
                            item = i
                    assert item is not None
                    self.controller.dataBlock.assignItemToSprint(item,sprint)
                    comment = ScrumblesObjects.Comment()
                    comment.commentContent = '%s Has Assigned Item %s to Sprint' % (self.controller.activeUser.userName, item.itemTitle)
                    comment.commentItemID = item.itemID
                    comment.commentUserID = self.controller.activeUser.userID
                    self.controller.dataBlock.addNewScrumblesObject(comment)
                except Exception as e:
                    messagebox.showerror('Error',str(e))
                    logging.exception('Error assigning item %s to sprint'%item.itemTitle)
                    return
                messagebox.showinfo('Success','Item Assigned Item to sprint, %s'%sprint.sprintName)


            else:
                messagebox.showerror('Error','Sprint not found in DataBlock')
                logging.error('Sprint not found in dataBlock')

    def assignToEpic(self,Inepic):
        epic = None

        if messagebox.askyesno('Assign To Epic','Do you wish to assign item to Epic %s?'%Inepic):
            for I in self.controller.activeProject.listOfAssignedItems:
                 if I.itemType == 'Epic':
                    if I.itemTitle == Inepic:
                        epic = I
            if epic is not None:
                try:
                    title = self.selectedItem.itemTitle
                    for i in self.controller.dataBlock.items:
                        if i.itemTitle == title:
                            item = i
                    assert item is not None
                    self.controller.dataBlock.addItemToEpic(item,epic)
                    comment = ScrumblesObjects.Comment()
                    comment.commentContent = '%s Has Assigned Item %s to Epic' % (self.controller.activeUser.userName, item.itemTitle)
                    comment.commentItemID = item.itemID
                    comment.commentUserID = self.controller.activeUser.userID
                    self.controller.dataBlock.addNewScrumblesObject(comment)
                except Exception as e:
                    messagebox.showerror('Error',str(e))
                    logging.exception('Error assigning item %s to epic'%item.itemTitle)
                    return
                messagebox.showinfo('Success','Item Assigned Item to Epic, %s'%epic.itemTitle)


            else:
                messagebox.showerror('Error','Epic not found in DataBlock')
                logging.error('Epic not found in dataBlock')

    def editSprint(self):
        sprint = self.sprintPopMenu.getSelectedObject()
        if Dialogs.EditSprintDialog(self.controller,master=self.controller,
                                 dataBlock=self.controller.dataBlock,
                                 sprint=sprint).show():
            messagebox.showinfo('Success','Sprint Updated Successfully')

    def deleteSprint(self):
        sprint = self.sprintPopMenu.getSelectedObject()
        self.selectedItem = None
        self.selectedSubItem = None
        if Dialogs.DeleteSprintDialog(self.controller,master=self.controller,
                                 dataBlock=self.controller.dataBlock,
                                 sprint=sprint).show():
            self.selectedSprint = None


    def deleteItem(self):
        item = None
        title = self.selectedItem.itemTitle
        for i in self.controller.dataBlock.items:
            if i.itemTitle == title:
                item = i

        if item is None:
            print('Item Title:', title)
            print('backlogData:')
            for i in self.controller.activeProject.listOfAssignedItems:
                print(i.itemTitle)
            raise Exception('Error Loading item from title')
        try:
            if messagebox.askyesno('Warning','Are you sure you want to delete %s\nThis action cannot be reversed'%str(item)):
                self.controller.dataBlock.deleteScrumblesObject(item,self.controller.activeProject)
                messagebox.showinfo('Success', 'Item %s deleted from database'%item.itemTitle)
        except Exception as e:
            logging.exception('Failed to delete item %s'%str(item))
            messagebox.showerror('Error', 'Failed to delete item\n'+str(e))
        self.selectedItem = None
        self.selectedSubItem = None

    def updateItem(self):
        item = None
        title = self.selectedItem.itemTitle
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
    def updateSprintList(self):
        self.sprints = []
        self.fullList = []
        self.sprints = [sprint for sprint in self.controller.activeProject.listOfAssignedSprints]
        self.fullList = [item for item in self.controller.activeProject.listOfAssignedItems]
        self.sprintList.importSprintsList(self.sprints)
        self.fullBacklog.importItemList(self.fullList)
        self.fullBacklog.colorCodeListboxes()
        self.generatePopupThing()

    def updateLists(self):
        self.fullList = []
        self.sprints = []
        self.sprintItems = []
        self.sprintItemSubItems = []

        self.sprintList.clearList()
        self.itemList.clearList()
        self.subItemList.clearList()
        self.fullBacklog.clearList()

        self.fullList = [item for item in self.controller.activeProject.listOfAssignedItems]
        self.sprints = [sprint for sprint in self.controller.activeProject.listOfAssignedSprints]
        self.sprintList.importSprintsList(self.sprints)
        self.fullBacklog.importItemList(self.fullList)
        self.fullBacklog.colorCodeListboxes()
        if (self.selectedSprint != None):
            for sprint in self.controller.activeProject.listOfAssignedSprints:
                if (sprint.sprintName == self.selectedSprint.sprintName):
                    self.selectedSprint = sprint
            self.sprintItems = self.selectedSprint.listOfAssignedItems
            self.itemList.importItemList(self.sprintItems)
            self.itemList.colorCodeListboxes()
            if (self.selectedItem != None):
                for item in self.controller.activeProject.listOfAssignedItems:
                    if (item.itemTitle == self.selectedItem.itemTitle):
                        self.selectedItem = item
                self.sprintItemSubItems = [item for item in self.selectedItem.subItemList]

        self.subItemList.importItemList(self.sprintItemSubItems)
        self.subItemList.colorCodeListboxes()
        self.itemList.colorCodeListboxes()
        self.activeProject = self.controller.activeProject
        del self.itemPopMenu
        self.itemPopMenu = mainViewPopup(self, self.controller)
        self.generatePopupThing()

    def assignedFBEvent(self, event):
        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemTitle == event.widget.get(tk.ANCHOR):
                self.selectedFB = item


    def assignedSprintEvent(self, event):
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == event.widget.get(tk.ANCHOR):
                self.selectedSprint = sprint
                self.sprintItems = sprint.listOfAssignedItems
                self.sprintItemSubItems = sprint.listOfAssignedItems
                self.itemList.importItemList(self.sprintItems)
                self.itemList.colorCodeListboxes()
                self.subItemList.clearList()

    def assignedItemEvent(self, event):
        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemTitle == event.widget.get(tk.ANCHOR):

                print(item.itemTitle)
                self.selectedItem = item
                self.subItemList.clearList()
                self.subItemList.importItemList(item.subItemList)
                self.subItemList.colorCodeListboxes()
    def listboxEvents(self, event):
        
        if event.widget is self.fullBacklog.listbox:
            self.assignedFBEvent
            self.itemDescriptionManager.changeDescription(event)

        if event.widget is self.sprintList.listbox:
            self.assignedSprintEvent(event)
            self.sprintDescriptionManager.changeDescription(event)

        if event.widget is self.itemList.listbox:
            self.assignedItemEvent(event)
            self.itemDescriptionManager.changeDescription(event)

        if event.widget is self.subItemList.listbox:
            self.itemDescriptionManager.changeDescription(event)
        self.generatePopupThing()
    def __str__(self):
        return 'Scrumbles Home View'


    # def getCodeLink(self,item):
    #     isUpdated = [False]  #Had to make this a list because bool and int are immutable
    #     evnt = self.myItemsPopMenu.event
    #     #yes it is bad practice, but getLinkPopUp is a frame that isn't going to have return value,
    #     #so, isUpdated is going to be modified by the popup
    #     #bad juju, I know, but do you have a better idea?
    #     getLinkPopUP = Dialogs.codeLinkDialog(self,self.controller,self.controller.dataBlock,item,evnt,isUpdated)
    #     self.wait_window(getLinkPopUP.top)
    #     return isUpdated


