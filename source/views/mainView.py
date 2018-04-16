from tkinter import messagebox
from frames import SPopMenu, Dialogs, ScrumblesFrames, listboxEventHandler
from data import ScrumblesObjects
import logging
import tkinter as tk


class mainViewPopup(SPopMenu.GenericPopupMenu):
    def __init__(self,root, Master, isSubItem):
        super().__init__(root, Master)
        self.isAssignDeleted = False
        self.isSubItem = isSubItem

    def context_menu(self, event, menu):
        self.widget = event.widget
        self.event = event
        index = self.widget.nearest(event.y)
        _, yOffSet, _, height = self.widget.bbox(index)
        if event.y > height + yOffSet + 5:
            return
        self.selectedObject = self.widget.get(index)

        self.selectedObject = self.findSelectedObject(self.selectedObject)
        try:
            self.root.selectedItem = self.selectedObject
        except:
            pass
        try:
            self.delete(u'Approve Item')
        except Exception as e:
            pass
        if self.root.roleMap[self.root.activeRole] > 0:
            if self.index(0) is None:
                self.usersMenu = tk.Menu(self, tearoff = 0)
                self.usersMenuEpic = tk.Menu(self, tearoff = 0)
                self.usersMenuSprint = tk.Menu(self, tearoff = 0)

                self.add_cascade(label = u'Assign to User', menu = self.usersMenu)

                for name in [U.userName for U in self.master.activeProject.listOfAssignedUsers]:
                    self.usersMenu.add_command(label = name, command = lambda n = name: self.root.assignToUser(n))

                self.listOfSprints = [S for S in self.master.activeProject.listOfAssignedSprints]
                self.add_cascade(label = u'Assign to Sprint', menu = self.usersMenuSprint)

                for name in [S.sprintName for S in self.listOfSprints]:
                    self.usersMenuSprint.add_command(label = name, command = lambda n = name: self.root.assignToSprint(n))

                self.listOfEpics = [I for I in self.master.activeProject.listOfAssignedItems if I.itemType == 'Epic']
                self.add_cascade(label = u'Assign to Epic', menu = self.usersMenuEpic)

                for name in [I.itemTitle for I in self.listOfEpics]:
                    self.usersMenuEpic.add_command(label = name, command = lambda n = name: self.root.assignToEpic(n))

                self.add_command(label = u'Edit Item', command = self.root.updateItem)
                self.add_command(label = u'Delete Item', command = self.root.deleteItem)
                if self.isSubItem:
                    self.add_command(label = u'Remove Subitem', command = self.root.removeFromEpic)
                    
            if self.selectedObject.itemStatus == 3:
                self.add_command(label = u'Approve Item', command = self.root.approveItem)

            if self.selectedObject.itemStatus == 3:
                self.add_command(label = u'Reject Item', command = self.root.rejectItem)

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

        self.tabButtons = ScrumblesFrames.STabs(self, controller, user.userRole + " Main")
        self.tabButtons.pack(side = tk.TOP, fill = tk.X)

        self.activeProject = controller.activeProject

        self.roleMap = {'Developer': 0, 'Scrum Master': 1, 'Admin': 2}
        self.activeRole = controller.activeUser.userRole

        self.fullBacklogList = ScrumblesFrames.SBacklogListColor(self, "ALL ITEMS", controller)
        self.sprintList = ScrumblesFrames.SList(self, "SPRINTS")
        self.itemList = ScrumblesFrames.SBacklogListColor(self, "ITEMS", controller, canAdd=False)
        self.subItemList = ScrumblesFrames.SBacklogListColor(self, "SUB-ITEMS", controller, canAdd=False)

        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'
        self.FBPopMenu = None
        self.sprintPopMenu = None
        self.itemPopMenu = None
        self.subItemPopMenu = None

        self.generatePopupThing()

        self.sprints = []
        self.sprintItems = []
        self.sprintItemSubItems = []
        self.fullList = []

        self.selectedFullBacklogItem = None
        self.selectedSprint = None
        self.selectedItem = None
        self.selectedSubItem = None

        sprintDynamicSources = [self.sprintList.listbox]
        sprintQueryType = ['Sprint']
        self.sprintDescriptionManager = ScrumblesFrames.SCardDescription(self, controller, sprintDynamicSources, sprintQueryType)

        itemDynamicSources = [self.fullBacklogList.listbox,
                              self.itemList.listbox,
                              self.subItemList.listbox]
        itemQueryType = ['Item', 'Item', 'Item']
        self.itemDescriptionManager = ScrumblesFrames.SCardDescription(self, controller, itemDynamicSources, itemQueryType)

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        #Bind Sources
        for source in itemDynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))
        for source in sprintDynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.fullBacklogList.listbox.bind('<2>' if self.aqua else '<3>',
                                          lambda event: (self.generatePopupThing(),
                                                     self.FBPopMenu.context_menu(event,
                                                     self.FBPopMenu)))
        self.sprintList.listbox.bind('<2>' if self.aqua else '<3>',
                                     lambda event: (self.generatePopupThing(),
                                                    self.sprintPopMenu.context_menu(event,
                                                    self.sprintPopMenu)))
        self.itemList.listbox.bind('<2>' if self.aqua else '<3>',
                                   lambda event: (self.generatePopupThing(),
                                                  self.itemPopMenu.context_menu(event,
                                                  self.itemPopMenu)))
        self.subItemList.listbox.bind('<2>' if self.aqua else '<3>',
                                      lambda event: (self.generatePopupThing(),
                                                     self.subItemPopMenu.context_menu(event,
                                                     self.subItemPopMenu)))

        self.fullBacklogList.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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
        self.FBPopMenu = mainViewPopup(self, self.controller, False)
        self.sprintPopMenu = SPopMenu.GenericPopupMenu(self, self.controller)
        if self.roleMap[self.activeRole] > 0:
            self.sprintPopMenu.add_command(label=u'Edit Sprint',
                                           command=self.editSprint)
            self.sprintPopMenu.add_command(label=u'Delete Sprint',
                                           command=self.deleteSprint)

        self.itemPopMenu = mainViewPopup(self, self.controller, False)
        self.subItemPopMenu = mainViewPopup(self, self.controller, True)

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

    def removeFromEpic(self):
        item = None

        try:
            title = self.selectedItem.itemTitle
            for i in self.controller.dataBlock.items:
                if i.itemTitle == title:
                    item = i
            self.controller.dataBlock.removeItemFromEpic(item)
            comment = ScrumblesObjects.Comment()
            comment.commentContent = '%s Has Removed Item from epic' % self.controller.activeUser.userName
            comment.commentItemID = item.itemID
            comment.commentUserID = self.controller.activeUser.userID
            self.controller.dataBlock.addNewScrumblesObject(comment)

        except Exception as e:
            logging.exception('Could not remove item from epic')
            messagebox.showerror('Error', str(e))

        messagebox.showinfo('Success', 'Item Removed')

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
            messagebox.showerror('Error', str(e))

        messagebox.showinfo('Success', 'Item Rejected')

    def assignToUser(self, username):
        user = None

        if messagebox.askyesno('Assign To User', 'Do you wish to assign item to user %s?' % username):
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
                    self.controller.dataBlock.assignUserToItem(user, item)
                    comment = ScrumblesObjects.Comment()
                    comment.commentContent = '%s Has Assigned User %s to Item' % (self.controller.activeUser.userName, user.userName)
                    comment.commentItemID = item.itemID
                    comment.commentUserID = self.controller.activeUser.userID
                    self.controller.dataBlock.addNewScrumblesObject(comment)
                except Exception as e:
                    messagebox.showerror('Error', str(e))
                    logging.exception('Error assigning user %s to item'%username)
                    return
                messagebox.showinfo('Success', 'Item Assigned to User %s'%user.userName)

            else:
                messagebox.showerror('Error', 'User not found in DataBlock')
                logging.error('User %s not found in dataBlock'%username)

    def assignToSprint(self, inSprint):
        sprint = None

        if messagebox.askyesno('Assign To Sprint', 'Do you wish to assign item to sprint %s?' % inSprint):
            for i in self.controller.activeProject.listOfAssignedSprints:
                if i.sprintName == inSprint:
                    sprint = i
            if sprint is not None:
                try:
                    title = self.selectedItem.itemTitle
                    for j in self.controller.dataBlock.items:
                        if j.itemTitle == title:
                            item = j
                    assert item is not None
                    self.controller.dataBlock.assignItemToSprint(item, sprint)
                    comment = ScrumblesObjects.Comment()
                    comment.commentContent = '%s Has Assigned Item %s to Sprint' % (self.controller.activeUser.userName, item.itemTitle)
                    comment.commentItemID = item.itemID
                    comment.commentUserID = self.controller.activeUser.userID
                    self.controller.dataBlock.addNewScrumblesObject(comment)
                except Exception as e:
                    messagebox.showerror('Error', str(e))
                    logging.exception('Error assigning item %s to sprint' % item.itemTitle)
                    return
                messagebox.showinfo('Success', 'Item Assigned Item to sprint, %s' % sprint.sprintName)

            else:
                messagebox.showerror('Error', 'Sprint not found in DataBlock')
                logging.error('Sprint not found in dataBlock')

    def assignToEpic(self, inEpic):
        epic = None

        if messagebox.askyesno('Assign To Epic', 'Do you wish to assign item to Epic %s?' % inEpic):
            for i in self.controller.activeProject.listOfAssignedItems:
                if i.itemType == 'Epic':
                    if i.itemTitle == inEpic:
                        epic = i
            if epic is not None:
                try:
                    title = self.selectedItem.itemTitle
                    for j in self.controller.dataBlock.items:
                        if j.itemTitle == title:
                            item = j
                    assert item is not None
                    self.controller.dataBlock.addItemToEpic(item, epic)
                    comment = ScrumblesObjects.Comment()
                    comment.commentContent = '%s Has Assigned Item %s to Epic' % (self.controller.activeUser.userName, item.itemTitle)
                    comment.commentItemID = item.itemID
                    comment.commentUserID = self.controller.activeUser.userID
                    self.controller.dataBlock.addNewScrumblesObject(comment)
                except Exception as e:
                    messagebox.showerror('Error', str(e))
                    logging.exception('Error assigning item %s to epic' % item.itemTitle)
                    return
                messagebox.showinfo('Success', 'Item Assigned Item to Epic, %s' % epic.itemTitle)


            else:
                messagebox.showerror('Error', 'Epic not found in DataBlock')
                logging.error('Epic not found in dataBlock')

    def editSprint(self):
        sprint = self.sprintPopMenu.getSelectedObject()
        if Dialogs.EditSprintDialog(self.controller,
                                    master=self.controller,
                                    dataBlock=self.controller.dataBlock,
                                    sprint=sprint).show():
            messagebox.showinfo('Success', 'Sprint Updated Successfully')

    def deleteSprint(self):
        sprint = self.sprintPopMenu.getSelectedObject()
        self.selectedItem = None
        self.selectedSubItem = None
        if Dialogs.DeleteSprintDialog(self.controller,
                                      master=self.controller,
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
            raise Exception('Error Loading item from title')
        try:
            if messagebox.askyesno('Warning', 'Are you sure you want to delete %s\nThis action cannot be reversed' % str(item)):
                self.controller.dataBlock.deleteScrumblesObject(item,self.controller.activeProject)
                messagebox.showinfo('Success', 'Item %s deleted from database' % item.itemTitle)
        except Exception as e:
            logging.exception('Failed to delete item %s' % str(item))
            messagebox.showerror('Error', 'Failed to delete item\n' + str(e))
        self.selectedItem = None
        self.selectedSubItem = None

    def updateItem(self):
        item = None
        title = self.selectedItem.itemTitle
        for i in self.controller.dataBlock.items:
            if i.itemTitle == title:
                item = i

        if item is None:
            raise Exception('Error Loading item from title')

        Dialogs.EditItemDialog(self.controller,
                               master=self.controller,
                               dataBlock=self.controller.dataBlock,
                               item=item).show()

    def updateSprintList(self):
        self.sprints = []
        self.fullList = []
        self.sprints = [sprint for sprint in self.controller.activeProject.listOfAssignedSprints]
        self.fullList = [item for item in self.controller.activeProject.listOfAssignedItems]
        self.sprintList.importSprintsList(self.sprints)
        self.fullBacklogList.importItemList(self.fullList)
        self.fullBacklogList.colorCodeListboxes()
        self.generatePopupThing()

    def updateLists(self):
        self.fullList = []
        self.sprints = []
        self.sprintItems = []
        self.sprintItemSubItems = []

        self.sprintList.clearList()
        self.itemList.clearList()
        self.subItemList.clearList()
        self.fullBacklogList.clearList()

        self.fullList = [item for item in self.controller.activeProject.listOfAssignedItems]
        self.sprints = [sprint for sprint in self.controller.activeProject.listOfAssignedSprints]
        self.sprintList.importSprintsList(self.sprints)
        self.fullBacklogList.importItemList(self.fullList)
        try:
            self.fullBacklogList.colorCodeListboxes()
        except Exception as e:
            logging.exception('Error coloring list boxes', str(e))

        if self.selectedSprint is not None:
            for sprint in self.controller.activeProject.listOfAssignedSprints:
                if sprint.sprintName == self.selectedSprint.sprintName:
                    self.selectedSprint = sprint

            self.sprintItems = self.selectedSprint.listOfAssignedItems
            self.itemList.importItemList(self.sprintItems)
            self.itemList.colorCodeListboxes()

            if self.selectedItem is not None:
                for item in self.controller.activeProject.listOfAssignedItems:
                    if item.itemTitle == self.selectedItem.itemTitle:
                        self.selectedItem = item
                self.sprintItemSubItems = [item for item in self.selectedItem.subItemList]

        self.subItemList.importItemList(self.sprintItemSubItems)
        self.subItemList.colorCodeListboxes()
        self.itemList.colorCodeListboxes()
        self.activeProject = self.controller.activeProject
        del self.itemPopMenu
        self.itemPopMenu = mainViewPopup(self, self.controller, False)
        self.generatePopupThing()

    def assignedFullBacklogEvent(self, event):
        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemTitle == event.widget.get(tk.ANCHOR):
                self.selectedFullBacklogItem = item
                self.selectedItem = item
                if self.selectedItem.itemSprintID is not None:
                    try:
                        self.selectedSprint = self.controller.dataBlock.sprintMap[self.selectedFullBacklogItem.itemSprintID]
                    except KeyError:
                        pass

                    self.sprintItems = self.selectedSprint.listOfAssignedItems
                    self.itemList.importItemList(self.sprintItems)
                    self.itemList.colorCodeListboxes()

                if self.selectedItem.subItemList is not None:
                    self.sprintItemSubItems = self.selectedItem.subItemList
                    self.subItemList.clearList()
                    self.subItemList.importItemList(item.subItemList)
                    self.subItemList.colorCodeListboxes()

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
                self.selectedItem = item
                self.subItemList.clearList()
                self.subItemList.importItemList(item.subItemList)
                self.subItemList.colorCodeListboxes()

    def listboxEvents(self, event):
        if event.widget is self.fullBacklogList.listbox:
            self.assignedFullBacklogEvent(event)
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
