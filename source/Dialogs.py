import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
from MySQLdb import IntegrityError
import ScrumblesData
import ScrumblesObjects
import webbrowser
import sys, traceback
class CreateProjectDialog:
    def __init__(self, parent, dbConnector):

        self.dbConnector = dbConnector

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.geometry('300x100')
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

            self.dbConnector.connect()
            try:
                self.dbConnector.setData(ScrumblesData.Query.createObject(project))
            except IntegrityError:
                project.projectID = ScrumblesObjects.generateRowID()
                self.dbConnector.setData(ScrumblesData.Query.createObject(project))
            self.dbConnector.close()


        except Exception as e:
            messagebox.showerror('Error', str(e))

        else:
            messagebox.showinfo('Info', 'New Item Successfully Created')
            self.exit()
        finally:
            if self.dbConnector is not None:
                if self.dbConnector.isConnected():
                    self.dbConnector.close()

    def exit(self):
        if self.dbConnector is not None:
            assert self.dbConnector.isConnected() == False
        self.top.destroy()


class CreateUserDialog:

    def __init__(self, parent, dbConnector):

        self.dbConnector = dbConnector

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.geometry('300x250')
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

            self.dbConnector.connect()
            try:
                self.dbConnector.setData(ScrumblesData.Query.createObject(user))
            except IntegrityError:
                user.userID = ScrumblesObjects.generateRowID()
                self.dbConnector.setData(ScrumblesData.Query.createObject(user))
            self.dbConnector.close()

        except IntegrityError as e:
            if 'UserName' in str(e):
                messagebox.showerror('Error', 'Username already in use')
            elif "EmailAddress" in str(e):
                messagebox.showerror('Error', "Email address already in use")
            else:
                messagebox.showerror('Error',str(e))
        except Exception as e:
            messagebox.showerror('Error',str(e))

        else:
            messagebox.showinfo('Info', 'New User Successfully Created')
            self.exit()
        finally:
            if self.dbConnector is not None:
                if self.dbConnector.isConnected():
                    self.dbConnector.close()


    def exit(self):
        if self.dbConnector is not None:
            assert self.dbConnector.isConnected() == False
        self.top.destroy()


class CreateSprintDialog:

    def __init__(self, parent, dbConnector):

        self.dbConnector = dbConnector

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.geometry('300x250')
        popUPDialog.title('Create a New Sprint')

        Tk.Label(popUPDialog, text="Sprint Name").grid(row=2,column=1,pady=5,sticky='E')


        self.sprintNameEntry = Tk.Entry(popUPDialog)
        self.sprintNameEntry.grid(row=2, column=2, pady=5)



        createButton = Tk.Button(popUPDialog, text="Create Sprint", command=self.ok)
        createButton.grid(row=8,column=2,pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=8,column=1,pady=5)



    def ok(self):

        try:

            sprint = ScrumblesObjects.Sprint()
            sprint.sprintName = self.sprintNameEntry.get()

            self.dbConnector.connect()
            try:
                self.dbConnector.setData(ScrumblesData.Query.createObject(sprint))
            except IntegrityError:
                sprint.sprintID = ScrumblesObjects.generateRowID()
                self.dbConnector.setData(ScrumblesData.Query.createObject(sprint))
            self.dbConnector.close()

        except IntegrityError as e:
            if 'SprintName' in str(e):
                messagebox.showerror('Error', 'Sprint Must have unique Name')
            else:
                messagebox.showerror('Error', str(type(e)) + '\n' + str(e))
        except Exception as e:
            messagebox.showerror('Error',str(type(e))+'\n'+str(e))

        else:
            messagebox.showinfo('Info', 'New Sprint Successfully Created')
            self.exit()
        finally:
            if self.dbConnector is not None:
                if self.dbConnector.isConnected():
                    self.dbConnector.close()


    def exit(self):
        if self.dbConnector is not None:
            assert self.dbConnector.isConnected() == False
        self.top.destroy()


class CreateItemDialog:

    def __init__(self, parent, dbConnector):

        self.dbConnector = dbConnector

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.geometry('300x250')
        popUPDialog.title('Create a New Item')


        Tk.Label(popUPDialog, text="Item Title").grid(row=2,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Item Description").grid(row=3,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="Item Type").grid(row=6,column=1,pady=5,sticky='E')


        self.itemTitleEntry = Tk.Entry(popUPDialog,width=27)
        self.itemTitleEntry.grid(row=2,column=2,pady=5,sticky='W')

        self.itemDescriptionEntry = Tk.Text(popUPDialog,height=6,width=20,wrap=Tk.WORD)
        self.itemDescriptionEntry.grid(row=3,column=2,pady=5)




        ItemTypeVar = Tk.StringVar()
        items = ('User Story', 'Epic', 'Bug','Chore','Feature')
        self.ItemTypebox = ttk.Combobox(popUPDialog,textvariable=ItemTypeVar,state='readonly',values=items)
        self.ItemTypebox.grid(row=6, column=2,sticky='W')
        self.ItemTypebox.selection_clear()


        createButton = Tk.Button(popUPDialog, text="Create Item", command=self.ok)
        createButton.grid(row=8,column=2,pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=8,column=1,pady=5)


    def ok(self):

        try:


            item = ScrumblesObjects.Item()

            item.itemTitle = self.itemTitleEntry.get()
            item.itemDescription = self.itemDescriptionEntry.get('1.0','end-1c')
            item.itemType = self.ItemTypebox.get()

            self.dbConnector.connect()
            try:
                self.dbConnector.setData(ScrumblesData.Query.createObject(item))
            except IntegrityError:
                item.itemID = ScrumblesObjects.generateRowID()
                self.dbConnector.setData(ScrumblesData.Query.createObject(item))
            self.dbConnector.close()


        except Exception as e:
            messagebox.showerror('Error',str(e))

        else:
            messagebox.showinfo('Info', 'New Item Successfully Created')
            self.exit()
        finally:
            if self.dbConnector is not None:
                if self.dbConnector.isConnected():
                    self.dbConnector.close()


    def exit(self):
        if self.dbConnector is not None:
            assert self.dbConnector.isConnected() == False
        self.top.destroy()



class AboutDialog:
    def __init__(self, parent):
        self.apiLink = 'https://github.com/CEN3031-group16/GroupProject/wiki'

        popUPDialog = self.top = Tk.Toplevel(parent)
        popUPDialog.geometry('550x200')
        popUPDialog.title('About Scrumbles')

        Tk.Label(popUPDialog, text="Scrumbles is an application designed to help you manage programming projects and teams efficiently").grid(row=1, pady=5, sticky='E')
        linkLabel = Tk.Label(popUPDialog, text=self.apiLink,fg='blue')
        linkLabel.grid(row=2,pady=5)
        linkLabel.bind('<Button-1>',self.openPage)

        okayButton = Tk.Button(popUPDialog, text="Okay", command=self.exit)
        okayButton.grid(row=3, pady=5)

    def openPage(self, *args, **kwargs):
        webbrowser.open(self.apiLink)

    def exit(self):
        self.top.destroy()


#todo get dataBlock from caller
class EditItemDialog:
    def __init__(self, parent, dataBlock, Item):
        self.item = Item
        self.dataBlock = dataBlock
        ItemTypeVar = Tk.StringVar()
        itemUserVar = Tk.StringVar()
        sprintVar = Tk.StringVar()

        self.listOfUsers = self.dataBlock.users
        self.listOfSprints = self.dataBlock.sprints
        userNames = [user.userName for user in self.listOfUsers]
        sprintNames = [sprint.sprintName for sprint in self.listOfSprints]

        popUPDialog = self.top = Tk.Toplevel(parent)
        #popUPDialog.geometry('300x250')
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


        items = ('User Story', 'Epic', 'Bug', 'Chore', 'Feature')
        self.ItemTypebox = ttk.Combobox(popUPDialog, textvariable=ItemTypeVar, state='readonly', values=items)
        self.ItemTypebox.grid(row=6, column=2, sticky='W')
        #self.ItemTypebox.selection_clear()
        self.ItemTypebox.current(items.index(Item.itemType))

        users = tuple(userNames)
        sprints = tuple(sprintNames)
        self.usersComboBox = ttk.Combobox(popUPDialog, textvariable=itemUserVar, state='readonly',values=users)
        self.usersComboBox.current(0)
        self.usersComboBox.grid(row=7,column=2, sticky='W')

        self.sprintsComboBox = ttk.Combobox(popUPDialog, textvariable=sprintVar, state='readonly',values=sprints)
        self.sprintsComboBox.current(0)
        self.sprintsComboBox.grid(row=8,column=2, sticky='W')


        self.itemCodeLinkEntry = Tk.Entry(popUPDialog, width=27)
        self.itemCodeLinkEntry.grid(row=10, column=2, pady=5, sticky='W')
        self.itemPriorityEntry = Tk.Entry(popUPDialog, width=27)
        self.itemPriorityEntry.grid(row=9, column=2, pady=5, sticky='W')

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
            userID = 0


            for sprint in self.listOfSprints:
                if sprint.sprintName == self.sprintsComboBox.get():
                    selectedSprint = sprint
            for user in self.listOfUsers:
                if user.userName == self.usersComboBox.get():
                    userID = user.userID

            if self.sprintsComboBox.get() != '':
                item.itemSprintID = selectedSprint.sprintID
                item.itemDueDate = selectedSprint.sprintDueDate

            item.itemType = self.ItemTypebox.get()

            item.itemUserID = userID


            item.itemCodeLink = self.itemCodeLinkEntry.get()
            if self.itemPriorityEntry.get() == '':
                item.itemPriority = 0
            else:
                item.itemPriority = int(self.itemPriorityEntry.get())



            self.dataBlock.updateScrumblesObject(item)




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

