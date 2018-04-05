import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
from MySQLdb import IntegrityError
import ScrumblesData
import ScrumblesObjects
import webbrowser
import sys, traceback
import datetime
import logging
import time



class CreateProjectDialog:
    def __init__(self, parent, dataBlock):

        self.dataBlock = dataBlock

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.transient(parent)
        popUPDialog.grab_set()
        popUPDialog.resizable(0, 0)
        popUPDialog.geometry('600x200')

        popUPDialog.title('Create a New Project')

        Tk.Label(popUPDialog, text="Project Title").grid(row=2, column=1, pady=5, sticky='E')


        self.projectTitleEntry = Tk.Entry(popUPDialog, width=27)
        self.projectTitleEntry.grid(row=2, column=2, pady=5, sticky='W')



        createButton = Tk.Button(popUPDialog, text="Create Project", command=self.ok)
        createButton.grid(row=8, column=2, pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=8, column=1, pady=5)

    def ok(self):

        try:

            project = ScrumblesObjects.Project()
            project.projectName = self.projectTitleEntry.get()


            try:
                self.dataBlock.addNewScrumblesObject(project)
            except IntegrityError:
                logging.exception('ID Collision')
                project.projectID = ScrumblesObjects.generateRowID()
                self.dataBlock.addNewScrumblesObject(project)



        except Exception as e:
            messagebox.showerror('Error', str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack(file=sys.stdout)

        else:
            messagebox.showinfo('Info', 'New Item Successfully Created')
            self.exit()


    def exit(self):
        self.top.destroy()


class CreateUserDialog:

    def __init__(self, parent, dataBlock):

        self.dataBlock = dataBlock

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.transient(parent)
        popUPDialog.grab_set()
        popUPDialog.resizable(0, 0)
        popUPDialog.geometry('600x500')
        popUPDialog.title('Create a New User')

        Tk.Label(popUPDialog, text="User Name").grid(row=2,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="User Password").grid(row=3,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Re-enter Password").grid(row=4,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="User Email Address").grid(row=5,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="User Role").grid(row=6,column=1,pady=5,sticky='E')

        self.userNameEntry = Tk.Entry(popUPDialog)
        self.userNameEntry.grid(row=2,column=2,pady=5)

        self.passwordEntry = Tk.Entry(popUPDialog,show='*')
        self.passwordEntry.grid(row=3,column=2,pady=5)
        self.reEnterPasswordEntry = Tk.Entry(popUPDialog,show='*')
        self.reEnterPasswordEntry.grid(row=4,column=2,pady=5)

        self.emailEntry =Tk.Entry(popUPDialog)
        self.emailEntry.grid(row=5,column=2,pady=5)

        roleVar = Tk.StringVar()
        items = ('Admin', 'Scrum Master', 'Developer')
        self.roleCombobox = ttk.Combobox(popUPDialog,textvariable=roleVar,state='readonly',values=items)
        self.roleCombobox.grid(row=6, column=2)
        self.roleCombobox.selection_clear()


        createButton = Tk.Button(popUPDialog, text="Create User", command=self.ok)
        createButton.grid(row=8,column=2,pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=8,column=1,pady=5)

    @staticmethod
    def validatePasswordMatch(password1, password2):
        if password1 != password2:
            raise Exception('Passwords do not Match')
        return

    def ok(self):

        try:
            self.validatePasswordMatch(self.passwordEntry.get(),self.reEnterPasswordEntry.get())

            user = ScrumblesObjects.User()
            user.userName = self.userNameEntry.get()
            user.userPassword = self.passwordEntry.get()
            user.userEmailAddress = self.emailEntry.get()
            user.userRole = self.roleCombobox.get()


            try:
                self.dataBlock.addNewScrumblesObject(user)
            except IntegrityError:
                logging.exception('ID Collision')
                user.userID = ScrumblesObjects.generateRowID()
                self.dataBlock.addNewScrumblesObject(user)


        except IntegrityError as e:
            logging.exception('Invalid Input')
            if 'UserName' in str(e):
                messagebox.showerror('Error', 'Username already in use')
            elif "EmailAddress" in str(e):
                messagebox.showerror('Error', "Email address already in use")
            else:
                messagebox.showerror('Error',str(e))
        except Exception as e:
            messagebox.showerror('Error',str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack(file=sys.stdout)

        else:
            messagebox.showinfo('Info', 'New User Successfully Created')
            self.exit()



    def exit(self):
        self.top.destroy()


class CreateSprintDialog:

    def __init__(self, parent, dataBlock):

        self.month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Nov','Dec']
        self.day = [str(d) for d in range(1,32)]
        self.year = [str(y) for y in range(2018,2100)]

        self.dataBlock = dataBlock

        popUPDialog = self.top = Tk.Toplevel(parent)

        popUPDialog.transient(parent)
        popUPDialog.grab_set()
        popUPDialog.resizable(0, 0)

        popUPDialog.geometry('900x500')
        popUPDialog.title('Create a New Sprint')

        Tk.Label(popUPDialog, text="Sprint Name").grid(row=2,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Project").grid(row=3,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Start Date").grid(row=4,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Due Date").grid(row=5,column=1,pady=5,sticky='E')
        monthVar = Tk.StringVar()
        monthVar = 'Jan'
        self.StartMonthCombo = ttk.Combobox(popUPDialog,textvariable=monthVar,values=self.month,state='readonly',width=5)
        self.StartMonthCombo.grid(row=4,column=2)
        self.StartDayCombo = ttk.Combobox(popUPDialog,values=self.day,state='readonly',width=3)
        self.StartDayCombo.grid(row=4,column=3)
        self.StartYearCombo = ttk.Combobox(popUPDialog,values=self.year,state='readonly',width=5)
        self.StartYearCombo.grid(row=4,column=4)

        self.DueMonthCombo = ttk.Combobox(popUPDialog, values=self.month, state='readonly',width=5)
        self.DueMonthCombo.grid(row=5, column=2)
        self.DueDayCombo = ttk.Combobox(popUPDialog, values=self.day, state='readonly',width=3)
        self.DueDayCombo.grid(row=5, column=3)
        self.DueYearCombo = ttk.Combobox(popUPDialog, values=self.year, state='readonly',width=5)
        self.DueYearCombo.grid(row=5, column=4)


        self.sprintNameEntry = Tk.Entry(popUPDialog)
        self.sprintNameEntry.grid(row=2, column=2, pady=5)
        self.projectNameVar = Tk.StringVar()
        projects = tuple([P.projectName for P in self.dataBlock.projects])
        self.assignSprintToObject = ttk.Combobox(popUPDialog,textvariable=self.projectNameVar,state='readonly',values=projects)
        self.assignSprintToObject.grid(row=3,column=2,pady=5)



        createButton = Tk.Button(popUPDialog, text="Create Sprint", command=self.ok)
        createButton.grid(row=8,column=2,pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=8,column=1,pady=5)


    def getStartDate(self):
        month = self.StartMonthCombo.get()
        day = self.StartDayCombo.get()
        year = self.StartYearCombo.get()

        if month == '' or day == '' or year == '':
            dateString = 'Jan 1 2100 5:00PM'
        else:
            dateString = month+" "+day+" "+year+" 5:00PM"
        return datetime.datetime.strptime(dateString,'%b %d %Y %I:%M%p')

    def getDueDate(self):
        month = self.DueMonthCombo.get()
        day = self.DueDayCombo.get()
        year = self.DueYearCombo.get()
        if month == '' or day == '' or year == '':
            dateString = 'Jan 1 2100 5:00PM'
        else:
            dateString = month+" "+day+" "+year+" 5:00PM"
        return datetime.datetime.strptime(dateString,'%b %d %Y %I:%M%p')

    def ok(self):

        try:

            sprint = ScrumblesObjects.Sprint()
            sprint.sprintName = self.sprintNameEntry.get()
            sprint.sprintStartDate = self.getStartDate()
            sprint.sprintDueDate = self.getDueDate()

            projectName = self.assignSprintToObject.get()
            for P in self.dataBlock.projects:
                if P.projectName == projectName:
                    sprint.projectID = P.projectID


            try:
                self.dataBlock.addNewScrumblesObject(sprint)
            except IntegrityError:
                logging.exception('ID Collision')
                sprint.sprintID = ScrumblesObjects.generateRowID()
                self.dataBlock.addNewScrumblesObject(sprint)

        except IntegrityError as e:
            logging.exception('Invalid Input')
            if 'SprintName' in str(e):
                messagebox.showerror('Error', 'Sprint Must have unique Name')
            else:
                messagebox.showerror('Error', str(type(e)) + '\n' + str(e))
        except Exception as e:
            messagebox.showerror('Error',str(type(e))+'\n'+str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack(file=sys.stdout)

        else:
            messagebox.showinfo('Info', 'New Sprint Successfully Created')
            self.exit()



    def exit(self):
        self.top.destroy()


class CreateItemDialog:

    def __init__(self, parent, dataBlock):
        self.parent = parent
        self.dataBlock = dataBlock
        self.parent = parent

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.transient(parent)
        popUPDialog.grab_set()
        popUPDialog.resizable(0, 0)
        popUPDialog.geometry('600x640')
        popUPDialog.title('Create a New Item')


        Tk.Label(popUPDialog, text="Item Title").grid(row=2,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Item Description").grid(row=3,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Item Type").grid(row=6,column=1,pady=5,sticky='E')


        self.itemTitleEntry = Tk.Entry(popUPDialog,width=27)
        self.itemTitleEntry.grid(row=2,column=2,pady=5,sticky='W')

        self.itemDescriptionEntry = Tk.Text(popUPDialog,height=6,width=20,wrap=Tk.WORD)
        self.itemDescriptionEntry.grid(row=3,column=2,pady=5)




        self.ItemTypeVar = Tk.StringVar()
        self.itemTypes = ('User Story', 'Epic', 'Bug','Chore','Feature')
        self.ItemTypebox = ttk.Combobox(popUPDialog,textvariable=self.ItemTypeVar,state='readonly',values=self.itemTypes)
        self.ItemTypebox.grid(row=6, column=2,sticky='W')
        self.ItemTypebox.current(0)


        self.itemPriorityLabel = Tk.Label(popUPDialog,text='Item Priority').grid(row=7,column=1,sticky='E')
        self.itemPriorities = ( "Low Priority", "Medium Priority", "High Priority")
        self.itemPriorityVar = Tk.StringVar()
        self.itemPriorityCombobox = ttk.Combobox(popUPDialog,textvariable=self.itemPriorityVar,state='readonly')
        self.itemPriorityCombobox['values'] = self.itemPriorities
        self.itemPriorityCombobox.current(0)
        self.itemPriorityCombobox.grid(row=7,column=2,sticky='W')


        self.pointsEntryLabel = Tk.Label(popUPDialog, text="Points").grid(row=8,column=1,sticky='E')
        self.pointsEntry = Tk.Entry(popUPDialog)
        self.pointsEntry.grid(row=8,column=2)

        self.commentTextBoxLabel = Tk.Label(popUPDialog, text='Comment').grid(row=10, column=1, sticky='E')
        self.commentTextBox = Tk.Text(popUPDialog, height=6, width=20, wrap=Tk.WORD)
        self.commentTextBox.grid(row=10, column=2,pady=5)

        createButton = Tk.Button(popUPDialog, text="Create Item", command=self.ok)
        createButton.grid(row=11,column=2,pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=11,column=1,pady=5)


    def ok(self):

        try:


            item = ScrumblesObjects.Item()

            item.itemTitle = self.itemTitleEntry.get()
            item.itemDescription = self.itemDescriptionEntry.get('1.0','end-1c')
            item.itemType = self.ItemTypebox.get()
            item.itemPoints = self.pointsEntry.get()
            item.itemPriority = item.priorityTextToNumberMap[self.itemPriorityCombobox.get()]

            comment = ScrumblesObjects.Comment()
            comment.commentContent = self.commentTextBox.get('1.0','end-1c')
            comment.commentUserID = self.parent.activeUser.userID
            comment.commentItemID = item.itemID


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

            self.dataBlock.addItemToProject(self.parent.activeProject,item)

        except Exception as e:
            logging.exception('Object Creation Error')
            messagebox.showerror('Error',str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack(file=sys.stdout)

        else:
            messagebox.showinfo('Info', 'New Item Successfully Created')
            self.exit()

    def exit(self):
        self.top.destroy()



class EditItemDialog:
    def __init__(self, parent, dataBlock, Item):
        print(type(Item))
        self.parent = parent
        print(Item)
        self.item = Item
        self.dataBlock = dataBlock
        self.ItemTypeVar = Tk.StringVar()
        self.itemUserVar = Tk.StringVar()
        self.sprintVar = Tk.StringVar()
        self.itemPriorityVar = Tk.StringVar

        self.listOfUsers = self.dataBlock.users
        self.listOfSprints = parent.controller.activeProject.listOfAssignedSprints
        self.userMap = {}
        self.sprintMap = {}
        for U in self.dataBlock.users:
            self.userMap[U.userID] = U.userName
        for S in self.dataBlock.sprints:
            self.sprintMap[S.sprintID] = S.sprintName
        userNames = [user.userName for user in self.listOfUsers]
        userNames.append('None')
        sprintNames = [sprint.sprintName for sprint in self.listOfSprints]
        sprintNames.append('None')

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.transient(parent)
        popUPDialog.grab_set()
        popUPDialog.resizable(0, 0)
        popUPDialog.geometry('600x600')
        popUPDialog.title('Edit %s' % Item.itemTitle)

        Tk.Label(popUPDialog, text="Item Title").grid(row=2, column=1, pady=5, sticky='E')
        Tk.Label(popUPDialog, text="Item Description").grid(row=3, column=1, pady=5, sticky='E')
        Tk.Label(popUPDialog, text="Item Type").grid(row=6, column=1, pady=5, sticky='E')
        Tk.Label(popUPDialog, text='Assign To User').grid(row=7,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text='Assign to Sprint').grid(row=8,column=1,pady=5,sticky='E')

        Tk.Label(popUPDialog, text="Set Priority").grid(row=9,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Set link to Code").grid(row=10,column=1,pady=5,sticky='E')

        self.itemTitleEntry = Tk.Entry(popUPDialog, width=27)
        self.itemTitleEntry.insert(0,Item.itemTitle)
        self.itemTitleEntry.grid(row=2, column=2, pady=5, sticky='W')

        self.itemDescriptionEntry = Tk.Text(popUPDialog, height=6, width=20, wrap=Tk.WORD)

        self.itemDescriptionEntry.insert(Tk.END,Item.itemDescription)
        self.itemDescriptionEntry.grid(row=3, column=2, pady=5)


        itemTypes = Item.validItemTypes
        self.ItemTypebox = ttk.Combobox(popUPDialog, textvariable=self.ItemTypeVar, state='readonly', values=Item.validItemTypes)
        self.ItemTypebox.grid(row=6, column=2, sticky='W')
        #self.ItemTypebox.selection_clear()
        if Item.itemType in itemTypes:
           self.ItemTypebox.set(Item.itemType)
        else:
            self.ItemTypebox.current(0)
        users = tuple(userNames)
        sprints = tuple(sprintNames)

        self.usersComboBox = ttk.Combobox(popUPDialog, textvariable=self.itemUserVar, state='readonly',values=users)
        self.usersComboBox.current(0)
        self.usersComboBox.grid(row=7,column=2, sticky='W')
        if self.item.itemUserID is not None and self.item.itemUserID != 0:
            self.usersComboBox.set(self.userMap[self.item.itemUserID])
        else:
            self.usersComboBox.set('None')
        self.sprintsComboBox = ttk.Combobox(popUPDialog, textvariable=self.sprintVar, state='readonly',values=sprints)
        self.sprintsComboBox.current(0)
        self.sprintsComboBox.grid(row=8,column=2, sticky='W')
        if self.item.itemSprintID is not None and self.item.itemSprintID != 0:
            self.sprintsComboBox.set(self.sprintMap[self.item.itemSprintID])
        else:
            self.sprintsComboBox.set('None')
        self.itemCodeLinkEntry = Tk.Entry(popUPDialog, width=27)
        self.itemCodeLinkEntry.grid(row=10, column=2, pady=5, sticky='W')
        if self.item.itemCodeLink is not None:
            self.itemCodeLinkEntry.insert(0,self.item.itemCodeLink)

        self.itemPriorityCombobox = ttk.Combobox(popUPDialog, textvariable=self.itemPriorityVar, state='readonly', width=27)
        self.itemPriorityCombobox['values'] = ( "Low Priority","Medium Priority", "High Priority")
        self.itemPriorityCombobox.current(Item.itemPriority)
        self.itemPriorityCombobox.grid(row=9, column=2, pady=5, sticky='W')



        self.commentTextBoxLabel = Tk.Label(popUPDialog, text='Reason For Change').grid(row=11, column=1, sticky='E')
        self.commentTextBox = Tk.Text(popUPDialog, height=6, width=20, wrap=Tk.WORD)
        self.commentTextBox.grid(row=11, column=2, pady=5,sticky='W')

        createButton = Tk.Button(popUPDialog, text="Update Item", command=self.ok)
        createButton.grid(row=12, column=2, pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=12, column=1, pady=5)

    def ok(self):

        try:


            item = self.item

            item.itemTitle = self.itemTitleEntry.get()
            item.itemDescription = self.itemDescriptionEntry.get('1.0', 'end-1c')
            selectedSprint = None
            selectedUser = None

            comment = ScrumblesObjects.Comment()
            comment.commentContent = self.commentTextBox.get('1.0', 'end-1c')
            comment.commentUserID = self.parent.controller.activeUser.userID
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
                self.dataBlock.assignItemToSprint(item,selectedSprint)
            else:
                item.itemSprintID = None
                item.itemDueDate = None

            item.itemType = self.ItemTypebox.get()
            self.dataBlock.assignUserToItem(selectedUser,item)



            item.itemCodeLink = self.itemCodeLinkEntry.get()
            if self.itemPriorityCombobox.get() == '':
                item.itemPriority = 0
            else:
                self.dataBlock.modifiyItemPriority(item,item.priorityTextToNumberMap[self.itemPriorityCombobox.get()])


            self.dataBlock.updateScrumblesObject(item)



        except Exception as e:
            logging.exception('Object Edit Error')
            messagebox.showerror('Error', str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack(file=sys.stdout)
        else:
            messagebox.showinfo('Info', "Item '%s' Successfully Updated"%item.itemTitle)
            self.exit()


    def exit(self):

        self.top.destroy()

class SplashScreen(Tk.Toplevel):
    def __init__(self,parent):
        Tk.Toplevel.__init__(self,parent,cursor="wait")
        print('Init Splash')

        self.wm_overrideredirect(True)
        self.title('Welcome To Scrumbles')
        w = 1280
        h = 800
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
# root.update()
# #
# # # u = CreateUserDialog(root,dataConnection)
# # # s = CreateSprintDialog(root, dataConnection)
# # # i = CreateItemDialog(root, dataConnection)
# # p = CreateProjectDialog(root, dataConnection)
#

# # u = CreateUserDialog(root,dataConnection)
# # s = CreateSprintDialog(root, dataConnection)
# # i = CreateItemDialog(root, dataConnection)
# # p = CreateProjectDialog(root, dataConnection)
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

