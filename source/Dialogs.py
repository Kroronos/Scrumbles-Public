import tkinter as Tk
from tkinter import ttk
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
        Tk.Label(popUPDialog, text="User Email Address").grid(row=4,column=1,pady=5,sticky='E')
        Tk.Label(popUPDialog, text="User Role").grid(row=5,column=1,pady=5,sticky='E')

        self.userNameEntry = Tk.Entry(popUPDialog)
        self.userNameEntry.grid(row=2,column=2,pady=5)

        self.passwordEntry = Tk.Entry(popUPDialog)
        self.passwordEntry.grid(row=3,column=2,pady=5)

        self.emailEntry =Tk.Entry(popUPDialog)
        self.emailEntry.grid(row=4,column=2,pady=5)

        roleVar = Tk.StringVar()
        items = ('Admin', 'Scrum Master', 'Developer')
        self.roleCombobox = ttk.Combobox(popUPDialog,textvariable=roleVar,state='readonly',values=items)
        self.roleCombobox.grid(row=5, column=2)
        self.roleCombobox.selection_clear()


        createButton = Tk.Button(popUPDialog, text="Create User", command=self.ok)
        createButton.grid(row=8,column=2,pady=5)
        cancelButton = Tk.Button(popUPDialog, text="Cancel", command=self.exit)
        cancelButton.grid(row=8,column=1,pady=5)

    def ok(self):

        print ("User Name", self.userNameEntry.get())
        print ("Password", self.passwordEntry.get())
        print ("Email", self.emailEntry.get())
        print ("Role", self.roleCombobox.get())

        user = ScrumblesObjects.User()
        user.userName = self.userNameEntry.get()
        user.userPassword = self.passwordEntry.get()
        user.userEmailAddress = self.emailEntry.get()
        user.userRole = self.roleCombobox.get()

        self.dbConnector.connect()
        self.dbConnector.setData(ScrumblesData.Query.createObject(user))
        self.dbConnector.close()


        self.exit()

    def exit(self):
        self.top.destroy()

# dbLoginInfo = ScrumblesData.DataBaseLoginInfo()
# dbLoginInfo.userID = 'test_user'
# dbLoginInfo.password = 'testPassword'
# dbLoginInfo.ipaddress = '173.230.136.241'
# dbLoginInfo.defaultDB = 'test'
# dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)
#
#
# root = Tk.Tk()
# Tk.Button(root, text="Hello!").pack()
# root.update()
#
# d = CreateUserDialog(root,dataConnection)
#
# root.wait_window(d.top)