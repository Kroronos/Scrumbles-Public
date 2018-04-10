import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ScrumblesFrames, SPopMenu,ScrumblesObjects,Dialogs
import listboxEventHandler
from styling import styling as style
import logging
import tkinter as tk
import Dialogs

class SMmainViewPopup(SPopMenu.GenericPopupMenu):
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
        # for i in range(5):
        #     print('index %i = %s'%(i,str(self.index(i))))
        try:
            self.delete(u'Approve Item')
        except Exception as e:
            pass
        if self.root.roleMap[self.root.activeRole] > 0:
            if self.index(0) is None:
                self.usersMenu = tk.Menu(self, tearoff=0)
                self.add_cascade(label=u'Assign to User', menu=self.usersMenu)
                for name in [U.userName for U in self.master.activeProject.listOfAssignedUsers]:
                    self.usersMenu.add_command(label=name, command=lambda n=name:self.root.assignToUser(n))

            if self.selectedObject.itemStatus == 3:
               if self.index(1) is None or self.index(1)==0:
                   self.add_command(label=u'Approve Item', command=self.root.approveItem)




        try:
            self.root.selectedItem = self.selectedObject
        except:
            pass
        self.widget.selection_clear(0, tk.END)
        self.widget.selection_set(index)
        self.widget.activate(index)
        menu.post(event.x_root, event.y_root)


    def getSelectedObject(self):
        return self.selectedObject




class SMmainView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'

        self.tabButtons = ScrumblesFrames.STabs(self, controller, user.userRole + " Home")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.activeProject = controller.activeProject
        self.sprintPopMenu = SPopMenu.GenericPopupMenu(self,self.controller)
        self.roleMap = {'Developer':0,'Scrum Master':1,'Admin':2}
        self.activeRole = controller.activeUser.userRole
        if self.roleMap[self.activeRole] > 0:
            self.sprintPopMenu.add_command(label=u'Edit Sprint',
                                           command=self.editSprint)
            self.sprintPopMenu.add_command(label=u'Delete Sprint',
                                           command=self.deleteSprint)

        self.itemPopMenu= SMmainViewPopup(self,self.controller)
        self.subItemPopMenu= SMmainViewPopup(self,self.controller)


        self.sprintList = ScrumblesFrames.SList(self, "SPRINTS")
        self.itemList = ScrumblesFrames.SBacklogListColor(self, "ITEMS",controller)
        self.subItemList = ScrumblesFrames.SBacklogListColor(self, "SUB-ITEMS",controller)

        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'

        self.sprintList.listbox.bind('<2>' if self.aqua else '<3>',
                                        lambda event: self.sprintPopMenu.context_menu(event, self.sprintPopMenu))
        self.itemList.listbox.bind('<2>' if self.aqua else '<3>',
                                   lambda event: self.itemPopMenu.context_menu(event,self.itemPopMenu))
        self.subItemList.listbox.bind('<2>' if self.aqua else '<3>',
                                   lambda event: self.subItemPopMenu.context_menu(event, self.subItemPopMenu))


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

    def approveItem(self):

        try:
            item = self.itemPopMenu.getSelectedObject()
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

    def assignToUser(self,username):
        user = None

        if messagebox.askyesno('Assign To User','Do you wish to assign item to user %s'%username):
            for U in self.controller.dataBlock.users:
                if U.userName == username:
                    user = U
            if user is not None:
                try:
                    item = self.itemPopMenu.getSelectedObject()
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
    def editSprint(self):
        sprint = self.sprintPopMenu.getSelectedObject()
        if Dialogs.EditSprintDialog(self.controller,master=self.controller,
                                 dataBlock=self.controller.dataBlock,
                                 sprint=sprint).show():
            messagebox.showinfo('Success','Sprint Updated Successfully')

    def deleteSprint(self):
        sprint = self.sprintPopMenu.getSelectedObject()
        self.selectedItem = None
        if Dialogs.DeleteSprintDialog(self.controller,master=self.controller,
                                 dataBlock=self.controller.dataBlock,
                                 sprint=sprint).show():
            self.selectedItem = None


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
        if (self.selectedItem != None):
            self.sprintItemSubItems = [item for item in self.selectedItem.subItemList]

        self.sprintList.importSprintsList(self.sprints)
        self.itemList.importItemList(self.sprintItems)
        self.itemList.colorCodeListboxes()
        self.subItemList.importItemList(self.sprintItemSubItems)
        self.subItemList.colorCodeListboxes()
        self.itemList.colorCodeListboxes()
        self.activeProject = self.controller.activeProject
        del self.itemPopMenu
        self.itemPopMenu = SMmainViewPopup(self, self.controller)

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
        if event.widget is self.sprintList.listbox:
            self.assignedSprintEvent(event)
            self.sprintDescriptionManager.changeDescription(event)

        if event.widget is self.itemList.listbox:
            self.assignedItemEvent(event)
            self.itemDescriptionManager.changeDescription(event)

        if event.widget is self.subItemList.listbox:
            self.itemDescriptionManager.changeDescription(event)
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


