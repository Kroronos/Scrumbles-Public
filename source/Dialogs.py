import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
from MySQLdb import IntegrityError
import ScrumblesData
import ScrumblesObjects

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

    def validatePasswordMatch(self,password1,password2):
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

## THE FOLLWING CODE WILL ALLOW STANDALONE EXECUTION OF DIALOGS INDEPENDENT OF SCRUMBLES APP
##  UNCOMMENT ONLY FOR TESTING.
##  KEEP CODE BLOCK COMMENTED OUT FOR PRODUCTION TESTING
dbLoginInfo = ScrumblesData.DataBaseLoginInfo()
dbLoginInfo.userID = 'test_user'
dbLoginInfo.password = 'testPassword'
dbLoginInfo.ipaddress = '173.230.136.241'
dbLoginInfo.defaultDB = 'test'
dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)


root = Tk.Tk()
Tk.Button(root, text="Hello!").pack()
root.update()

#d = CreateUserDialog(root,dataConnection)
d = CreateSprintDialog(root, dataConnection)

root.wait_window(d.top)