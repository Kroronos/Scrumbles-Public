# import tkinter as Tk
# from tkinter import ttk, messagebox
# import logging
from data import ScrumblesObjects
from frames.GenericDialogs import *


class CreateItemDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = None
        if not self.isTest:
            self.geometry('%dx%d'%(600*self.master.w_rat, 640*self.master.h_rat))
        self.title('Create a New Item')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):

        Tk.Label(self, text="Item Title").grid(row=2, column=1, pady=5, sticky='E')
        self.itemTitleEntry = Tk.Entry(self, width=27, cursor = "hand2")
        self.itemTitleEntry.grid(row=2, column=2, pady=5, sticky='W')

        Tk.Label(self, text="Item Description").grid(row=3, column=1, pady=5, sticky='E')
        self.itemDescriptionEntry = Tk.Text(self, height=6, width=20, wrap=Tk.WORD, cursor = "hand2")
        self.itemDescriptionEntry.grid(row=3, column=2, pady=5)

        Tk.Label(self, text="Item Type").grid(row=6, column=1, pady=5, sticky='E')
        self.ItemTypeVar = Tk.StringVar()
        self.itemTypes = ('User Story', 'Epic', 'Bug','Chore','Feature')
        self.ItemTypebox = ttk.Combobox(self,textvariable=self.ItemTypeVar,state='readonly',values=self.itemTypes, cursor = "hand2")
        self.ItemTypebox.grid(row=6, column=2,sticky='W')
        self.ItemTypebox.current(0)

        self.itemPriorityLabel = Tk.Label(self,text='Item Priority').grid(row=7,column=1,sticky='E')
        self.itemPriorities = ( "Low Priority", "Medium Priority", "High Priority")
        self.itemPriorityVar = Tk.StringVar()
        self.itemPriorityCombobox = ttk.Combobox(self,textvariable=self.itemPriorityVar,state='readonly', cursor = "hand2")
        self.itemPriorityCombobox['values'] = self.itemPriorities
        self.itemPriorityCombobox.current(0)
        self.itemPriorityCombobox.grid(row=7,column=2,sticky='W')

        self.pointsEntryLabel = Tk.Label(self, text="Points").grid(row=8,column=1,sticky='E')
        self.pointsEntry = Tk.Entry(self, cursor = "hand2")
        self.pointsEntry.grid(row=8,column=2)

        self.commentTextBoxLabel = Tk.Label(self, text='Comment').grid(row=10, column=1, sticky='E')
        self.commentTextBox = Tk.Text(self, height=6, width=20, wrap=Tk.WORD, cursor = "hand2")
        self.commentTextBox.grid(row=10, column=2,pady=5)

        self.createButton = Tk.Button(self, text="Create Item", command=self.ok, cursor = "hand2")
        self.createButton.grid(row=11,column=2,pady=5)
        self.cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor = "hand2")
        self.cancelButton.grid(row=11,column=1,pady=5)

    @tryExcept
    def ok(self):
            if self.item is None:
                item = ScrumblesObjects.Item()
            else:
                item = self.item
            item.itemTitle = self.itemTitleEntry.get()
            item.itemDescription = self.itemDescriptionEntry.get('1.0','end-1c')
            item.itemType = self.ItemTypebox.get()
            item.itemPoints = self.pointsEntry.get()
            item.itemPriority = item.priorityTextToNumberMap[self.itemPriorityCombobox.get()]
            self.validateName(item.itemTitle)
            comment = ScrumblesObjects.Comment()
            comment.commentContent = self.commentTextBox.get('1.0','end-1c')
            if not self.isTest:
                comment.commentUserID = self.parent.activeUser.userID
            comment.commentItemID = item.itemID
            if not self.isTest:
                self.writeData(item,comment)

            self.exit()


    def writeData(self,item,comment):
        if not item.itemPoints.isdigit():
            raise Exception('Points must be a number')

        try:
            self.dataBlock.addNewScrumblesObject(item)
        except IntegrityError:
            logging.exception('ID Collision')
            item.itemID = ScrumblesObjects.generateRowID()
            comment.commentItemID = item.itemID
            self.dataBlock.addNewScrumblesObject(item)

        if len(comment.commentContent) > 0:
            try:
                self.dataBlock.addNewScrumblesObject(comment)
            except IntegrityError:
                comment.commentID = ScrumblesObjects.generateRowID()
                self.dataBlock.addNewScrumblesObject(comment)
            else:
                messagebox.showinfo('Info', 'New Item Successfully Created')

        self.dataBlock.addItemToProject(self.parent.activeProject, item)

    def exit(self):
        self.top.destroy()


class EditItemDialog(CreateItemDialog):

    def __init__(self, *args, **kwargs):
        item = kwargs.pop('item',None)
        assert type(item) is ScrumblesObjects.Item
        super().__init__(*args, **kwargs)

        self.item = item
        assert type(item) is ScrumblesObjects.Item
        if not self.isTest:
            self.listOfSprints = self.master.activeProject.listOfAssignedSprints
            self.listOfUsers = self.dataBlock.users
            self.userMap = {}
            self.sprintMap = {}
            for U in self.dataBlock.users:
                self.userMap[U.userID] = U.userName
            for S in self.dataBlock.sprints:
                self.sprintMap[S.sprintID] = S.sprintName
            self.userNames = [user.userName for user in self.listOfUsers]
            self.userNames.append('None')
            self.sprintNames = [sprint.sprintName for sprint in self.listOfSprints]
            self.sprintNames.append('None')

        self.ItemTypeVar = Tk.StringVar()
        self.itemUserVar = Tk.StringVar()
        self.sprintVar = Tk.StringVar()
        self.itemPriorityVar = Tk.StringVar
        if not self.isTest:
            self.geometry('%dx%d' % (600 * self.master.w_rat, 600 * self.master.h_rat))
        self.title('Edit %s' % self.item.itemTitle)
        self.updateWidgets()
    def updateWidgets(self):

        self.commentTextBox.grid_forget()
        self.pointsEntry.grid_forget()
        self.createButton.grid_forget()
        self.cancelButton.grid_forget()


        Tk.Label(self, text='Assign To User').grid(row=7, column=1, pady=5, sticky='E')
        Tk.Label(self, text='Assign to Sprint').grid(row=8, column=1, pady=5, sticky='E')
        Tk.Label(self, text="Set link to Code").grid(row=10, column=1, pady=5, sticky='E')



        self.itemTitleEntry = Tk.Entry(self, width=27, cursor = "hand2")
        self.itemTitleEntry.insert(0, self.item.itemTitle)
        self.itemTitleEntry.grid(row=2, column=2, pady=5, sticky='W')

        self.itemDescriptionEntry = Tk.Text(self, height=6, width=20, wrap=Tk.WORD, cursor = "hand2")

        self.itemDescriptionEntry.insert(Tk.END, self.item.itemDescription)
        self.itemDescriptionEntry.grid(row=3, column=2, pady=5)

        itemTypes = self.item.validItemTypes
        self.ItemTypebox = ttk.Combobox(self, textvariable=self.ItemTypeVar, state='readonly',
                                        values=self.item.validItemTypes, cursor = "hand2")
        self.ItemTypebox.grid(row=6, column=2, sticky='W')


        self.ItemTypebox.set(self.item.itemType)
        if not self.isTest:
            users = tuple(self.userNames)
            sprints = tuple(self.sprintNames)
        else:
            users = ('user1','user2')
            sprints = ('sprint1','sprint2')

        self.usersComboBox = ttk.Combobox(self, textvariable=self.itemUserVar, state='readonly', values=users, cursor = "hand2")
        self.usersComboBox.current(0)
        self.usersComboBox.grid(row=7, column=2, sticky='W')
        if self.item.itemUserID is not None and self.item.itemUserID != 0:
            self.usersComboBox.set(self.userMap[self.item.itemUserID])
        else:
            self.usersComboBox.set('None')
        self.sprintsComboBox = ttk.Combobox(self, textvariable=self.sprintVar, state='readonly', values=sprints)
        self.sprintsComboBox.current(0)
        self.sprintsComboBox.grid(row=8, column=2, sticky='W')
        if self.item.itemSprintID is not None and self.item.itemSprintID != 0:
            self.sprintsComboBox.set(self.sprintMap[self.item.itemSprintID])
        else:
            self.sprintsComboBox.set('None')
        self.itemCodeLinkEntry = Tk.Entry(self, width=27)
        self.itemCodeLinkEntry.grid(row=10, column=2, pady=5, sticky='W')
        if self.item.itemCodeLink is not None:
            self.itemCodeLinkEntry.insert(0, self.item.itemCodeLink)

        Tk.Label(self, text='Item Priority').grid(row=9, column=1, sticky='E')
        self.itemPriorityCombobox = ttk.Combobox(self, textvariable=self.itemPriorityVar, state='readonly',
                                                 width=27)
        self.itemPriorityCombobox['values'] = ("Low Priority", "Medium Priority", "High Priority")
        self.itemPriorityCombobox.current(self.item.itemPriority)
        self.itemPriorityCombobox.grid(row=9, column=2, pady=5, sticky='W')

        self.commentTextBoxLabel = Tk.Label(self, text='Reason For Change').grid(row=11, column=1, sticky='E')
        self.commentTextBox = Tk.Text(self, height=6, width=20, wrap=Tk.WORD)
        self.commentTextBox.grid(row=11, column=2, pady=5, sticky='W')

        createButton = Tk.Button(self, text="Update Item", command=self.ok, cursor = "hand2")
        createButton.grid(row=12, column=2, pady=5)
        cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor = "hand2")
        cancelButton.grid(row=12, column=1, pady=5)

    @tryExcept
    def ok(self):
            item = ScrumblesObjects.Item
            oldItem = self.item
            item.itemID = oldItem.itemID
            item.itemTitle = self.itemTitleEntry.get()
            item.itemDescription = self.itemDescriptionEntry.get('1.0', 'end-1c')
            selectedSprint = None
            selectedUser = None
            if item.itemTitle != oldItem.itemTitle:
                self.validateName(item.itemTitle)
            comment = ScrumblesObjects.Comment()
            comment.commentContent = self.commentTextBox.get('1.0', 'end-1c')
            comment.commentUserID = self.master.activeUser.userID
            comment.commentItemID = item.itemID

            if len(comment.commentContent) <= 0:
                raise Exception('Comment box cannot be blank\nPlease enter a change reason.')
                #todo add comment as parameter to updateObject
                # try:
                #     self.dataBlock.addNewScrumblesObject(comment)
                # except IntegrityError:
                #     comment.commentID = ScrumblesObjects.generateRowID()
                #     self.dataBlock.addNewScrumblesObject(comment)
            # else:
            #     raise Exception('Comment box cannot be blank\nPlease enter a change reason.')

            for sprint in self.listOfSprints:
                if sprint.sprintName == self.sprintsComboBox.get():
                    selectedSprint = sprint
                    if selectedSprint.sprintDueDate is None:
                        raise Exception('Corrupted Sprint Data, contact your database admin')

            for user in self.listOfUsers:
                if user.userName == self.usersComboBox.get():
                    selectedUser = user

            if self.sprintsComboBox.get() != 'None':
                item.itemSprintID = selectedSprint.sprintID
            else:
                item.itemSprintID = None
                item.itemDueDate = None

            #todo add logic below to query, compare old item to new item
            # if self.sprintsComboBox.get() != 'None':
            #     self.dataBlock.removeItemFromSprint(item)
            #     self.dataBlock.assignItemToSprint(item, selectedSprint)
            # else:
            #     item.itemSprintID = None
            #     item.itemDueDate = None

            item.itemType = self.ItemTypebox.get()

            #todo add login to query
            #self.dataBlock.assignUserToItem(selectedUser, item)

            item.itemUserID = selectedUser.userID

            item.itemCodeLink = self.itemCodeLinkEntry.get()
            item.itemPriority = item.priorityTextToNumberMap[self.itemPriorityCombobox.get()]

            #todo add logic to query
            # if self.itemPriorityCombobox.get() == '':
            #     item.itemPriority = 0
            # else:
            #     self.dataBlock.modifiyItemPriority(item, item.priorityTextToNumberMap[self.itemPriorityCombobox.get()])

            #todo add logic to query
            # if oldItemType == 'Epic' and item.itemType != 'Epic':
            #     self.dataBlock.deleteEpic(item)
            # self.dataBlock.updateScrumblesObject(item)


            messagebox.showinfo('Info', "Item '%s' Successfully Updated" % item.itemTitle)
            self.exit()

    def exit(self):

        self.top.destroy()