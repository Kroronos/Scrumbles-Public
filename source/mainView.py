import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ScrumblesFrames, SPopMenu,ScrumblesObjects,Dialogs
import listboxEventHandler
from styling import styling as style
import logging

class mainView(tk.Frame):
    def __init__(self, parent, controller, user):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.aqua = parent.tk.call('tk', 'windowingsystem') == 'aqua'

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Scrum Master Home")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.myItemsPopMenu = SPopMenu.GenericPopupMenu(self, self.controller)
        self.myItemsPopMenu.add_command(label=u'Begin Work', command=self.setItemToInprogress)
        self.myItemsPopMenu.add_command(label=u'Submit For Review', command=self.setItemToSubmitted)

        self.backlogPopMenu = SPopMenu.GenericPopupMenu(self, self.controller)
        self.backlogPopMenu.add_command(label=u'Assign To me', command=self.assignItemToActiveUser)

        self.itemColumnFrame = tk.Frame(self)
        self.userItemList = ScrumblesFrames.SBacklogListColor(self.itemColumnFrame, "MY ITEMS",controller)
        self.userItemList.listbox.bind('<2>' if self.aqua else '<3>',
                                        lambda event: self.myItemsPopMenu.context_menu(event, self.myItemsPopMenu))

        self.productBacklogList = ScrumblesFrames.SBacklogListColor(self.itemColumnFrame,"BACKLOG",controller)

        self.productBacklogList.listbox.bind('<2>' if self.aqua else '<3>',
                                        lambda event: self.backlogPopMenu.context_menu(event, self.backlogPopMenu) )



        self.commentFeed = ScrumblesFrames.commentsField(self, self.controller)

        # progress bar
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("scrumbles.Horizontal.TProgressbar", troughcolor=style.scrumbles_blue, background=style.scrumbles_orange)

        progressBarStyle = "scrumbles.Horizontal.TProgressbar"

        self.progressBar = ttk.Progressbar(self.itemColumnFrame, style=progressBarStyle, orient="horizontal", mode="determinate")

        self.teamMemberList = ScrumblesFrames.SList(self, "TEAM MEMBERS")


        self.backlog = []
        self.teamMembers = []
        self.assignedItems = []
        self.selectedUser = None

        self.controller.dataBlock.packCallback(self.updateLists)
        self.updateLists()

        #Append Any Sources for Dynamic Events to this List
        dynamicSources = [self.productBacklogList.listbox, self.userItemList.listbox]
        queryType = ['Item', 'Item']
        self.descriptionManager = ScrumblesFrames.SCardDescription(self, controller, dynamicSources, queryType)

        # To Prevent Duplicate Tkinter Events
        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        #Bind Sources
        for source in dynamicSources:
            source.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.progressBar.pack(side=tk.TOP, fill=tk.X)
        self.userItemList.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.productBacklogList.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.itemColumnFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.descriptionManager.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.commentFeed.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def updateProgressBar(self):
        self.maxTasks = len(self.assignedItems)
        self.completedTasks = 0
        for item in self.assignedItems:
            if item.itemStatus == 4:
                self.completedTasks += 1
        self.progressBar["value"] = self.completedTasks
        self.progressBar["maximum"] = self.maxTasks

    def updateLists(self):
        self.backlog.clear()
        self.teamMembers.clear()
        self.assignedItems.clear()

        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemStatus == 0:
                self.backlog.append(item)

        self.teamMembers = [user.userName for user in self.controller.activeProject.listOfAssignedUsers]
        for item in self.controller.activeUser.listOfAssignedItems:
            if item.projectID == self.controller.activeProject.projectID:
                self.assignedItems.append(item)

        self.productBacklogList.clearList()
        self.productBacklogList.importItemList(self.backlog)
        self.productBacklogList.colorCodeListboxes()

        self.userItemList.clearList()
        self.userItemList.importItemList(self.assignedItems)
        self.userItemList.colorCodeListboxes()
        self.updateProgressBar()
        self.commentFeed.updateComments()


    def listboxEvents(self, event):
        if event.widget is self.userItemList.listbox:
            self.descriptionManager.changeDescription(event)
            self.commentFeed.updateFromListOfCommentsObject(self.controller.activeProject.listOfAssignedItems,
                                                            event.widget.get(tk.ANCHOR))

        if event.widget is self.productBacklogList.listbox:
            self.descriptionManager.changeDescription(event)
            self.commentFeed.updateFromListOfCommentsObject(self.controller.activeProject.listOfAssignedItems,
                                                            event.widget.get(tk.ANCHOR))

    def setItemToInprogress(self):
        Item = self.myItemsPopMenu.getSelectedItemObject()
        Comment = ScrumblesObjects.Comment()
        Comment.commentItemID = Item.itemID
        Comment.commentUserID = self.controller.activeUser.userID
        Comment.commentContent = 'Set to In Progress by menu action'
        result = messagebox.askyesno('Get to Work','Are you ready to begin work on this item?')
        if result:
            try:
                self.controller.dataBlock.modifyItemStatus(Item, Item.statusTextToNumberMap['In Progress'])
                self.controller.dataBlock.addNewScrumblesObject(Comment)
                messagebox.showinfo('Success','Item Status changed to In-Progress')
            except Exception as e:
                logging.exception('Error Setting Item to In progress')
                messagebox.showerror('Error', str(e))
    def setItemToSubmitted(self):
        Item = self.myItemsPopMenu.getSelectedItemObject()
        Comment = ScrumblesObjects.Comment()
        Comment.commentItemID = Item.itemID
        Comment.commentUserID = self.controller.activeUser.userID
        Comment.commentContent = 'Set to Submitted by menu action'
        updated = Dialogs.codeLinkDialog(self.controller, master=self.controller, dataBlock=self.controller.dataBlock,
                                         item=Item).show()
        if updated:
            try:
                self.controller.dataBlock.modifyItemStatus(Item, Item.statusTextToNumberMap['Submitted'])
                self.controller.dataBlock.addNewScrumblesObject(Comment)
                messagebox.showinfo('Success','Item Submitted to Scrum Master for review')
            except Exception as e:
                logging.exception('Error Assigning Submitting item for review')
                messagebox.showerror('Error', str(e))
    def assignItemToActiveUser(self):
        Item = self.backlogPopMenu.getSelectedItemObject()
        if Item.itemUserID is not None:
            messagebox.showerror('Error','Cannot Assign Item to Self!\nItem already assigned to another user')
            return False
        Comment = ScrumblesObjects.Comment()
        Comment.commentItemID = Item.itemID
        Comment.commentUserID = self.controller.activeUser.userID
        Comment.commentContent = 'Assigned to self by menu action'


        self.assignedItems.append(Item)
        self.userItemList.addItem(Item.itemTitle)
        self.updateProgressBar()
        result = messagebox.askyesno('Assign To Me','Do you want Assign this Item to yourself?')
        if result:
            try:
                self.controller.dataBlock.assignUserToItem(self.controller.activeUser,Item)
                self.controller.dataBlock.addNewScrumblesObject(Comment)
                messagebox.showinfo('Success', 'Item Assigned to %s' % self.controller.activeUser.userName)
            except Exception as e:
                logging.exception('Error Assigning Item to active User')
                messagebox.showerror('Error', str(e))
            return True

    # def getCodeLink(self,item):
    #     isUpdated = [False]  #Had to make this a list because bool and int are immutable
    #     evnt = self.myItemsPopMenu.event
    #     #yes it is bad practice, but getLinkPopUp is a frame that isn't going to have return value,
    #     #so, isUpdated is going to be modified by the popup
    #     #bad juju, I know, but do you have a better idea?
    #     getLinkPopUP = Dialogs.codeLinkDialog(self,self.controller,self.controller.dataBlock,item,evnt,isUpdated)
    #     self.wait_window(getLinkPopUP.top)
    #     return isUpdated