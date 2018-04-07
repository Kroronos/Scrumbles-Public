import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
from MySQLdb import IntegrityError
import ScrumblesData
import masterView
import ScrumblesObjects
import DataBlock
import webbrowser
import sys, traceback
import datetime
import logging
from SLists import ColorSchemes
import time

def tryExcept(f):
    def wrapper(self):
        try:
            f(self)

        except IntegrityError as e:
            logging.exception('Invalid Input')
            if 'UserName' in str(e):
                messagebox.showerror('Error', 'Username already in use')
            elif "EmailAddress" in str(e):
                messagebox.showerror('Error', "Email address already in use")
            elif 'SprintName' in str(e):
                messagebox.showerror('Error', 'Sprint Must have unique Name')
            else:
                messagebox.showerror('Error', str(type(e)) + '\n' + str(e))
                self.executeSuccess = False
                self.exit()


        except Exception as e:

            messagebox.showerror('Error', str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack(file=sys.stdout)
            self.executeSuccess = False
            self.exit()
    return wrapper



class GenericDialog(Tk.Toplevel):
    def __init__(self,*args, **kwargs):
        """ Defines A Generic PopUp Dialog
        First Param required to be root window
        master=MasterView
        dataBlock=DataBlock
        """
        print('SUPER arg[0]', args[0])
        print('SUPER kwargs', kwargs )

        self.isTest = False
        self.isTest = kwargs.pop('test', None)
        if self.isTest is not None and self.isTest:
            removeKey = kwargs.pop('dataBlock', None)
            removeKey = kwargs.pop('master', None)
        self.dataBlock = kwargs.pop('dataBlock',None)
        if self.dataBlock is not None:
            assert type(self.dataBlock) is DataBlock.DataBlock, 'Key: dataBlock must be a DataBlock object'
        self.master = kwargs.pop('master', None)
        if self.master is not None:
            assert type(self.master) is masterView.masterView, 'Key: master must be the Scrumbles masterView'

        print('Popped master from kwargs, self.master is:',self.master)

        Tk.Toplevel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.top = self
        self.transient()
        self.grab_set()
        self.executeSuccess = True


    def createWidgets(self):
        pass
    def exit(self):
        self.top.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.executeSuccess

class CreateProjectDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        if not self.isTest:
            self.geometry('%dx%d'%(600*self.master.w_rat, 200*self.master.h_rat))

        self.title('Create a New Project')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):
        Tk.Label(self, text="Project Title").grid(row=2, column=1, pady=5, sticky='E')

        self.projectTitleEntry = Tk.Entry(self, width=27)
        self.projectTitleEntry.grid(row=2, column=2, pady=5, sticky='W')

        self.createButton = Tk.Button(self, text="Create Project", command=self.ok, cursor = "hand2")
        self.createButton.grid(row=8, column=2, pady=5)
        self.cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor = "hand2")
        self.cancelButton.grid(row=8, column=1, pady=5)


    @tryExcept
    def ok(self):
        project = ScrumblesObjects.Project()
        project.projectName = self.projectTitleEntry.get()
        try:
            if not self.isTest:
                self.dataBlock.addNewScrumblesObject(project)
            else:
                print('TESTMODE: self.dataBlock.addNewScrumblesObject(%s)'%repr(project))
        except IntegrityError:
            logging.exception('ID Collision')
            project.projectID = ScrumblesObjects.generateRowID()
            self.dataBlock.addNewScrumblesObject(project)
        else:
            messagebox.showinfo('Info', 'New Item Successfully Created')
            self.exit()

class CreateUserDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if not self.isTest:
            self.geometry('%dx%d'%(600*self.master.w_rat, 500*self.master.h_rat))
        self.title('Create a New User')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):

        Tk.Label(self, text="User Name").grid(row=2, column=1, pady=5, sticky='E')
        self.userNameEntry = Tk.Entry(self)
        self.userNameEntry.grid(row=2,column=2,pady=5)

        Tk.Label(self, text="User Password").grid(row=3, column=1, pady=5, sticky='E')
        self.passwordEntry = Tk.Entry(self,show='*')
        self.passwordEntry.grid(row=3,column=2,pady=5)

        Tk.Label(self, text="Re-enter Password").grid(row=4, column=1, pady=5, sticky='E')
        self.reEnterPasswordEntry = Tk.Entry(self,show='*')
        self.reEnterPasswordEntry.grid(row=4,column=2,pady=5)

        Tk.Label(self, text="User Email Address").grid(row=5, column=1, pady=5, sticky='E')
        self.emailEntry =Tk.Entry(self)
        self.emailEntry.grid(row=5,column=2,pady=5)

        Tk.Label(self, text="User Role").grid(row=6, column=1, pady=5, sticky='E')
        roleVar = Tk.StringVar()
        items = ('Admin', 'Scrum Master', 'Developer')
        self.roleCombobox = ttk.Combobox(self,textvariable=roleVar,state='readonly',values=items)
        self.roleCombobox.grid(row=6, column=2)
        self.roleCombobox.selection_clear()


        self.createButton = Tk.Button(self, text="Create User", command=self.ok, cursor = "hand2")
        self.createButton.grid(row=8,column=2,pady=5)

        self.cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor = "hand2")
        self.cancelButton.grid(row=8,column=1,pady=5)


    @staticmethod
    def validatePasswordMatch(password1, password2):
        if password1 != password2:
            raise Exception('Passwords do not Match')
        return

    @tryExcept
    def ok(self):

        self.validatePasswordMatch(self.passwordEntry.get(),self.reEnterPasswordEntry.get())

        user = ScrumblesObjects.User()
        user.userName = self.userNameEntry.get()
        user.userPassword = self.passwordEntry.get()
        user.userEmailAddress = self.emailEntry.get()
        user.userRole = self.roleCombobox.get()

        try:
            if not self.isTest:
                self.dataBlock.addNewScrumblesObject(user)
        except IntegrityError:
            logging.exception('ID Collision')
            user.userID = ScrumblesObjects.generateRowID()
            self.dataBlock.addNewScrumblesObject(user)
        else:
            messagebox.showinfo('Info', 'New User Successfully Created')
            self.exit()

class CreateSprintDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprint = None
        self.month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Nov','Dec']
        self.day = [str(d) for d in range(1,32)]
        self.year = [str(y) for y in range(2018,2100)]
        if not self.isTest:
            self.geometry('%dx%d'%(900*self.master.w_rat, 500*self.master.h_rat))
            self.projects = tuple([P.projectName for P in self.dataBlock.projects])
            self.projectIDmap = {}
            for P in self.dataBlock.projects:
                self.projectIDmap[P.projectID] = P.projectName
        self.title('Create a New Sprint')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):

        monthVar = Tk.StringVar()
        monthVar = 'Jan'

        Tk.Label(self, text="Sprint Name").grid(row=2, column=1, pady=5, sticky='E')
        self.sprintNameEntry = Tk.Entry(self)
        self.sprintNameEntry.grid(row=2, column=2, pady=5)
        self.projectNameVar = Tk.StringVar()

        if not self.isTest:
            Tk.Label(self, text="Project").grid(row=3, column=1, pady=5, sticky='E')
            self.assignSprintToObject = ttk.Combobox(self,textvariable=self.projectNameVar,state='readonly',values=self.projects)
            self.assignSprintToObject.grid(row=3,column=2,pady=5)

        Tk.Label(self, text="Start Date").grid(row=4, column=1, pady=5, sticky='E')
        self.StartMonthCombo = ttk.Combobox(self,textvariable=monthVar,values=self.month,state='readonly',width=5)
        self.StartMonthCombo.grid(row=4,column=2)

        self.StartDayCombo = ttk.Combobox(self,values=self.day,state='readonly',width=3)
        self.StartDayCombo.grid(row=4,column=3)

        self.StartYearCombo = ttk.Combobox(self,values=self.year,state='readonly',width=5)
        self.StartYearCombo.grid(row=4,column=4)

        Tk.Label(self, text="Due Date").grid(row=5, column=1, pady=5, sticky='E')
        self.DueMonthCombo = ttk.Combobox(self, values=self.month, state='readonly',width=5)
        self.DueMonthCombo.grid(row=5, column=2)

        self.DueDayCombo = ttk.Combobox(self, values=self.day, state='readonly',width=3)
        self.DueDayCombo.grid(row=5, column=3)

        self.DueYearCombo = ttk.Combobox(self, values=self.year, state='readonly',width=5)
        self.DueYearCombo.grid(row=5, column=4)

        self.createButton = Tk.Button(self, text="Create Sprint", command=self.ok, cursor = "hand2")
        self.createButton.grid(row=8,column=2,pady=5)

        self.cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor = "hand2")
        self.cancelButton.grid(row=8,column=1,pady=5)

    @staticmethod
    def getStartDate(dateblock):

        if dateblock.month == '' or dateblock.day == '' or dateblock.year == '':
            dateString = 'Jan 1 2100 5:00PM'
        else:
            dateString = dateblock.month+" "+dateblock.day+" "+dateblock.year+" 5:00PM"
        return datetime.datetime.strptime(dateString,'%b %d %Y %I:%M%p')
    @staticmethod
    def getDueDate(dateblock):

        if dateblock.month == '' or dateblock.day == '' or dateblock.year == '':
            dateString = 'Jan 1 2100 5:00PM'
        else:
            dateString = dateblock.month+" "+dateblock.day+" "+dateblock.year+" 5:00PM"
        return datetime.datetime.strptime(dateString,'%b %d %Y %I:%M%p')

    def getDate(self,type):

        class dateblock:
            def __init__(self):
                self.month = None
                self.day = None
                self.year = None

        if type == 'start':
            dateblock.month = self.StartMonthCombo.get()
            dateblock.day = self.StartDayCombo.get()
            dateblock.year = self.StartYearCombo.get()
            date = self.getStartDate(dateblock)
        elif type == 'due':
            dateblock.month = self.DueMonthCombo.get()
            dateblock.day = self.DueDayCombo.get()
            dateblock.year = self.DueYearCombo.get()
            date = self.getDueDate(dateblock)
        else:
            raise Exception("getDate parameter must be 'start' or 'due' ")
        return date

    @tryExcept
    def ok(self):
        if self.sprint is None:
            sprint = ScrumblesObjects.Sprint()
        else:
            sprint = self.sprint
        sprint.sprintName = self.sprintNameEntry.get()
        sprint.sprintStartDate = self.getDate('start')
        sprint.sprintDueDate = self.getDate('due')
        if not self.isTest:
            projectName = self.assignSprintToObject.get()
            for P in self.dataBlock.projects:
                if P.projectName == projectName:
                    sprint.projectID = P.projectID

        if not self.isTest:
            self.writeData(sprint)

        self.exit()

    def writeData(self,obj):
        try:
            self.dataBlock.addNewScrumblesObject(obj)
        except IntegrityError:
            logging.exception('ID Collision')
            obj.sprintID = ScrumblesObjects.generateRowID()
            self.dataBlock.addNewScrumblesObject(obj)
        else:
            messagebox.showinfo('Info', 'New Sprint Successfully Created')

class EditSprintDialog(CreateSprintDialog):
    def __init__(self, *args, **kwargs):
        sprint = kwargs.pop('sprint',None)
        assert type(sprint) == ScrumblesObjects.Sprint, 'keyword sprint must be a ScrumblesObject.Sprint'
        super().__init__(*args, **kwargs)
        self.sprint = sprint
        self.updateWidgets()
        self.title('Modify Sprint')
        self.protocol('WM_DELETE_WINDOW', lambda: self.cancel())
    def updateWidgets(self):
        self.sprintNameEntry.insert(0,self.sprint.sprintName)
        if not self.isTest:
            self.assignSprintToObject.set(self.projectIDmap[self.sprint.projectID])
            self.assignSprintToObject['state'] = 'disabled'
        self.StartDayCombo.set(self.sprint.sprintStartDate.strftime('%d'))
        self.StartMonthCombo.set(self.sprint.sprintStartDate.strftime('%b'))
        self.StartYearCombo.set(self.sprint.sprintStartDate.strftime('%Y'))
        self.DueDayCombo.set(self.sprint.sprintDueDate.strftime('%d'))
        self.DueMonthCombo.set(self.sprint.sprintDueDate.strftime('%b'))
        self.DueYearCombo.set(self.sprint.sprintDueDate.strftime('%Y'))
        self.createButton['text'] = 'Update'
        self.cancelButton['command'] = self.cancel

    def writeData(self,obj):
        self.dataBlock.updateScrumblesObject(obj)
    def cancel(self):
        self.executeSuccess = False
        self.exit()

class CreateItemDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        print('SELF', type(self))
        print('CREATE arg[0]', args[0])
        print('CREATE kwargs', kwargs)
        print("Colling Super Init")
        super().__init__(*args, **kwargs)
        self.item = None
        if not self.isTest:
            print('Super __init__ Complete, self.master=',self.master)
            self.geometry('%dx%d'%(600*self.master.w_rat, 640*self.master.h_rat))
        self.title('Create a New Item')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):

        Tk.Label(self, text="Item Title").grid(row=2, column=1, pady=5, sticky='E')
        self.itemTitleEntry = Tk.Entry(self, width=27)
        self.itemTitleEntry.grid(row=2, column=2, pady=5, sticky='W')

        Tk.Label(self, text="Item Description").grid(row=3, column=1, pady=5, sticky='E')
        self.itemDescriptionEntry = Tk.Text(self, height=6, width=20, wrap=Tk.WORD)
        self.itemDescriptionEntry.grid(row=3, column=2, pady=5)

        Tk.Label(self, text="Item Type").grid(row=6, column=1, pady=5, sticky='E')
        self.ItemTypeVar = Tk.StringVar()
        self.itemTypes = ('User Story', 'Epic', 'Bug','Chore','Feature')
        self.ItemTypebox = ttk.Combobox(self,textvariable=self.ItemTypeVar,state='readonly',values=self.itemTypes)
        self.ItemTypebox.grid(row=6, column=2,sticky='W')
        self.ItemTypebox.current(0)

        self.itemPriorityLabel = Tk.Label(self,text='Item Priority').grid(row=7,column=1,sticky='E')
        self.itemPriorities = ( "Low Priority", "Medium Priority", "High Priority")
        self.itemPriorityVar = Tk.StringVar()
        self.itemPriorityCombobox = ttk.Combobox(self,textvariable=self.itemPriorityVar,state='readonly')
        self.itemPriorityCombobox['values'] = self.itemPriorities
        self.itemPriorityCombobox.current(0)
        self.itemPriorityCombobox.grid(row=7,column=2,sticky='W')

        self.pointsEntryLabel = Tk.Label(self, text="Points").grid(row=8,column=1,sticky='E')
        self.pointsEntry = Tk.Entry(self)
        self.pointsEntry.grid(row=8,column=2)

        self.commentTextBoxLabel = Tk.Label(self, text='Comment').grid(row=10, column=1, sticky='E')
        self.commentTextBox = Tk.Text(self, height=6, width=20, wrap=Tk.WORD)
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
        print('SELF',type(self))
        print('EDIT arg[0]', args[0])
        print('EDIT kwargs', kwargs)
        print('CALLING Create _init_')


        item = kwargs.pop('item',None)
        assert type(item) is ScrumblesObjects.Item
        super().__init__(*args, **kwargs)

        print('Create _init_complete: self.master =', self.master)
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
        #self.pointsEntryLabel.grid_forget()
        self.pointsEntry.grid_forget()
        self.createButton.grid_forget()
        self.cancelButton.grid_forget()


        Tk.Label(self, text='Assign To User').grid(row=7, column=1, pady=5, sticky='E')
        Tk.Label(self, text='Assign to Sprint').grid(row=8, column=1, pady=5, sticky='E')
        Tk.Label(self, text="Set link to Code").grid(row=10, column=1, pady=5, sticky='E')



        self.itemTitleEntry = Tk.Entry(self, width=27)
        self.itemTitleEntry.insert(0, self.item.itemTitle)
        self.itemTitleEntry.grid(row=2, column=2, pady=5, sticky='W')

        self.itemDescriptionEntry = Tk.Text(self, height=6, width=20, wrap=Tk.WORD)

        self.itemDescriptionEntry.insert(Tk.END, self.item.itemDescription)
        self.itemDescriptionEntry.grid(row=3, column=2, pady=5)

        itemTypes = self.item.validItemTypes
        self.ItemTypebox = ttk.Combobox(self, textvariable=self.ItemTypeVar, state='readonly',
                                        values=self.item.validItemTypes)
        self.ItemTypebox.grid(row=6, column=2, sticky='W')


        self.ItemTypebox.set(self.item.itemType)
        if not self.isTest:
            users = tuple(self.userNames)
            sprints = tuple(self.sprintNames)
        else:
            users = ('user1','user2')
            sprints = ('sprint1','sprint2')

        self.usersComboBox = ttk.Combobox(self, textvariable=self.itemUserVar, state='readonly', values=users)
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
            item = self.item
            item.itemTitle = self.itemTitleEntry.get()
            item.itemDescription = self.itemDescriptionEntry.get('1.0', 'end-1c')
            selectedSprint = None
            selectedUser = None

            comment = ScrumblesObjects.Comment()
            comment.commentContent = self.commentTextBox.get('1.0', 'end-1c')
            comment.commentUserID = self.master.activeUser.userID
            comment.commentItemID = item.itemID

            if len(comment.commentContent) > 0:
                try:
                    self.dataBlock.addNewScrumblesObject(comment)
                except IntegrityError:
                    comment.commentID = ScrumblesObjects.generateRowID()
                    self.dataBlock.addNewScrumblesObject(comment)
            else:
                raise Exception('Comment box cannot be blank\nPlease enter a change reason.')

            for sprint in self.listOfSprints:
                if sprint.sprintName == self.sprintsComboBox.get():
                    selectedSprint = sprint
                    if selectedSprint.sprintDueDate is None:
                        raise Exception('Corrupted Sprint Data, contact your database admin')
            for user in self.listOfUsers:
                if user.userName == self.usersComboBox.get():
                    selectedUser = user

            if self.sprintsComboBox.get() != 'None':
                self.dataBlock.removeItemFromSprint(item)
                self.dataBlock.assignItemToSprint(item, selectedSprint)
            else:
                item.itemSprintID = None
                item.itemDueDate = None

            item.itemType = self.ItemTypebox.get()
            self.dataBlock.assignUserToItem(selectedUser, item)

            item.itemCodeLink = self.itemCodeLinkEntry.get()
            if self.itemPriorityCombobox.get() == '':
                item.itemPriority = 0
            else:
                self.dataBlock.modifiyItemPriority(item, item.priorityTextToNumberMap[self.itemPriorityCombobox.get()])

            self.dataBlock.updateScrumblesObject(item)


            messagebox.showinfo('Info', "Item '%s' Successfully Updated" % item.itemTitle)
            self.exit()

    def exit(self):

        self.top.destroy()


class AboutDialog(GenericDialog):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.apiLink = 'https://github.com/CEN3031-group16/GroupProject/wiki'

        if not self.isTest:
            w = 600*self.master.w_rat
            h = 600*self.master.h_rat
            ws = self.parent.winfo_screenwidth()  # width of the screen
            hs = self.parent.winfo_screenheight()  # height of the screen
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.title('About Scrumbles')
        self.createWidgets()

    def createWidgets(self):
        Tk.Label(self, text="Scrumbles is an application designed to help you manage programming projects and teams efficiently").grid(row=1, pady=5, sticky='E')
        linkLabel = Tk.Label(self, text=self.apiLink,fg='blue',cursor='gumby')
        linkLabel.grid(row=2,pady=5)
        linkLabel.bind('<Button-1>',self.openPage)

        itemList = [ 'Not Assigned To Anything', 'Assigned to Sprint, no User', 'Assigned to User, No Sprint', 'Assigned to User and Sprint', 'In Progress', 'Submitted','Item Is Epic' ,'Complete']
        listBoxWidth=0
        self.itemListBox = Tk.Listbox(self, selectborderwidth=10)
        self.itemListBox.grid(row=3)
        for item in itemList:
            self.itemListBox.insert(Tk.END,item)
            if len(item) > listBoxWidth:
                listBoxWidth = len(item)

        self.itemListBox['width'] = listBoxWidth
        self.itemListBox['activestyle'] = 'dotbox'
        self.itemListBox['height'] = len(itemList)


        self.itemListBox.itemconfig(0, ColorSchemes.incompleteAssignmentColorScheme) # Not Assigned To Anything
        self.itemListBox.itemconfig(1, ColorSchemes.incompleteAssignmentColorScheme) #Assigned to Sprint, no User
        self.itemListBox.itemconfig(2, ColorSchemes.incompleteAssignmentColorScheme) #Assigned to User, No Sprint
        self.itemListBox.itemconfig(3, ColorSchemes.assignedScheme) # Assigned to User and Sprint
        self.itemListBox.itemconfig(4, ColorSchemes.inProgressColorScheme) # In Progress
        self.itemListBox.itemconfig(5, ColorSchemes.submittedColorScheme) # Submitted
        self.itemListBox.itemconfig(6, ColorSchemes.epicItemColorScheme) # Item Is Epic
        self.itemListBox.itemconfig(7, ColorSchemes.completedItemColorScheme) # Completed



        okayButton = Tk.Button(self, text="Okay", command=self.exit, cursor = "hand2")
        okayButton.grid(row=20, pady=5)

    def openPage(self, *args, **kwargs):
        webbrowser.open(self.apiLink)

    def exit(self):
        self.top.destroy()





class codeLinkDialog(GenericDialog):
    def __init__(self,*args,**kwargs):
        self.Item = kwargs.pop('item')

        super().__init__(*args,**kwargs)

        self.protocol('WM_DELETE_WINDOW', lambda: self.cancel())
        if not self.isTest:
            w = 600*self.master.w_rat
            h = 80*self.master.h_rat
            ws = self.parent.winfo_screenwidth()  # width of the screen
            hs = self.parent.winfo_screenheight()  # height of the screen
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            self.geometry('%dx%d+%d+%d'%(w,h,x,y))
        self.createWidgets()
    @tryExcept
    def createWidgets(self):
        self.title('Edit %s' % self.Item.itemTitle)
        self.codeLinkLabel = ttk.Label(self,text='Please enter link to Code')
        self.codeLinkLabel.grid(row=1,column=1)
        self.codeLinkEntry = Tk.Entry(self,width=60)
        self.codeLinkEntry.grid(row=2,column=1,sticky='W')
        if self.Item.itemCodeLink is not None:
            self.codeLinkEntry.insert(0,self.Item.itemCodeLink)
        self.submitButton = Tk.Button(self, text="Update Item", command=self.ok, cursor = "hand2")
        self.submitButton.grid(row=2, column=2, padx=3)
        self.cancelButton = Tk.Button(self,text='Cancel',command=self.cancel, cursor = "hand2")
        self.cancelButton.grid(row=2,column=3,pady=1)
    @tryExcept
    def ok(self):
        self.executeSuccess = True
        self.Item.itemCodeLink = self.codeLinkEntry.get()
        if not self.isTest:
            self.dataBlock.updateScrumblesObject(self.Item)
        self.exit()


    def exit(self):
        self.top.destroy()

    def cancel(self):
        self.executeSuccess = False
        self.exit()





class SplashScreen(Tk.Toplevel):
    def __init__(self,parent, master):
        Tk.Toplevel.__init__(self,parent,cursor="watch")
        print('Init Splash')

        self.wm_overrideredirect(True)
        self.title('Welcome To Scrumbles')
        w = 1280*master.w_rat
        h = 800*master.h_rat
        ws = parent.winfo_screenwidth()  # width of the screen
        hs = parent.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.waitLabel = Tk.Label(self,text='Please wait while Scrumbles Loads')
        self.waitLabel.pack()
        self.isAlive = True

        self.pbarList = []
        for i in range(30):
            pbar = None
            pbar= ttk.Progressbar(self,length=1000,maximum=10*(i),mode='indeterminate')
            pbar.pack()
            #pbar.start(10)
            self.pbarList.append(pbar)


        self.update()
        #self.start_progressBar()
    def kill(self):
        print('destroying Splash')
        self.isAlive = False
        self.destroy()

    def step_progressBar(self,interval):
        for pbar in self.pbarList:
            pbar.step(interval)
            self.update()




## THE FOLLWING CODE WILL ALLOW STANDALONE EXECUTION OF DIALOGS INDEPENDENT OF SCRUMBLES APP

##  UNCOMMENT ONLY FOR TESTING.
##  KEEP CODE BLOCK COMMENTED OUT FOR PRODUCTION TESTING
# dbLoginInfo = ScrumblesData.DataBaseLoginInfo('login.txt')
# #
# dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)

# root = Tk.Tk()
# Tk.Button(root, text="Hello!").pack()
# # root.update()
# # #
# # # # u = CreateUserDialog(root,dataConnection)
# # # # s = CreateSprintDialog(root, dataConnection)
# # # # i = CreateItemDialog(root, dataConnection)
# # # p = CreateProjectDialog(root, dataConnection)
# #
# # # u = CreateUserDialog(root,dataConnection)
# # # s = CreateSprintDialog(root, dataConnection)
# # # i = CreateItemDialog(root, dataConnection)
# # # p = CreateProjectDialog(root, dataConnection)
# h = AboutDialog(root)
# root.wait_window(h.top)

# items = []
# dataConnection.connect()
# for dic in dataConnection.getData(ScrumblesData.Query.getAllCards):
#     items.append(ScrumblesObjects.Item(dic))
# dataConnection.close()
# edit = EditItemDialog(root, dataConnection, items[0])
#
# root.wait_window(edit.top)



# root.wait_window(p.top)
if __name__ == '__main__':
    TSprint = ScrumblesObjects.Sprint()
    TSprint.sprintName = 'Test Sprint'
    TSprint.sprintStartDate = datetime.datetime.strptime('Jan 1 2100 5:00PM','%b %d %Y %I:%M%p')
    TSprint.sprintDueDate = TSprint.sprintStartDate
    TSprint.projectID = 0
    TItem = ScrumblesObjects.Item()
    TItem.itemTitle = 'TestItem'
    TItem.itemDescription = 'description'
    TItem.itemType = 'Epic'
    TItem.itemPriority = 0

    root = Tk.Tk()

    # assert CreateProjectDialog(root, test=True).show(),'create project failed'
    # assert CreateUserDialog(root, test=True).show(), 'create user failed'
    # assert CreateSprintDialog(root, test=True).show(), 'create Sprint failed'
    # assert EditSprintDialog(root, test=True, sprint=TSprint).show(), 'edit Sprint failed'
    # assert CreateItemDialog(root, test=True).show(),'create item failed'
    # assert EditItemDialog(root, test=True, item=TItem ).show(), 'edit item failed'
    # assert AboutDialog(root,test=True).show(), 'Help Dialog Failed'
    assert codeLinkDialog(root, test=True, item=TItem).show()
    assert not codeLinkDialog(root, test=True, item=TItem).show()
