#from tkinter import *
#from masterView import *
#from mainView import *
#from ScrumblesData import *

#comment fake a branch split


import tkinter as tk
from tkinter import messagebox
import masterView
import mainView
import ScrumblesData
import ScrumblesObjects

def authenticateUser(username, password, dbLoginInfo):
    user = None
    dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)
    dataConnection.connect()
    result = dataConnection.getData(ScrumblesData.Query.getUserIdByUsernameAndPassword(username, password))
    dataConnection.close()
    if result == ():
        raise Exception('Invalid USERNAME PASSWORD combo')
    else:
        user = ScrumblesObjects.User(result[0])
    return user


def viewSprintWindow():
    print("View Sprint Called")


def viewBacklogWindow():
    print("View Backlog Called")


def viewUserWindow():
    print("View user called")


class loginView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.inputFrame = tk.Frame(self)
        self.controller = controller

        self.usernameLabel = tk.Label(self.inputFrame, text="Username")
        self.passwordLabel = tk.Label(self.inputFrame, text="Password")
        self.usernameEntry = tk.Entry(self.inputFrame)
        self.passwordEntry = tk.Entry(self.inputFrame, show='*')
        self.loginButton = tk.Button(self.inputFrame, text='Login', command=lambda: self.loginProcess())

        self.usernameLabel.grid(row=3, column=2, sticky=tk.EW)
        self.usernameEntry.grid(row=3, column=3, columnspan=2, sticky=tk.EW)

        self.passwordLabel.grid(row=4, column=2, sticky=tk.EW)
        self.passwordEntry.grid(row=4, column=3, columnspan=2, sticky=tk.EW)
        self.loginButton.grid(row=6, column=3, sticky=tk.EW)


        for x in range(0, 7):
            self.inputFrame.grid_rowconfigure(x, weight=1, pad=5)
            self.inputFrame.grid_columnconfigure(x, weight=1)

        self.title = tk.Label(self, text="Time to Scrumble: Login", font=("Verdana", 12))

        self.title.grid(row=0, column=2, columnspan=1, sticky=tk.NSEW)
        self.inputFrame.grid(row=1, column=2, columnspan=1, sticky=tk.EW)

        for x in range(0, 5):
            self.grid_rowconfigure(x, weight=1)
            self.grid_columnconfigure(x, weight=1)

        self.passwordEntry.bind('<Return>', lambda event: self.loginProcess())
        self.usernameEntry.bind('<Return>', lambda event: self.loginProcess())
        self.loginButton.bind('<Return>', lambda event: self.loginProcess())


    def loginProcess(self):
        loggedInUser = self.loginButtonClicked()
        if (loggedInUser is not None):
            self.controller.setDatabaseConnection()
            self.controller.generateViews(loggedInUser)

    def loginButtonClicked(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        loggedInUser = None
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo()
        dbLoginInfo.userID = 'test_user'
        dbLoginInfo.password = 'testPassword'
        dbLoginInfo.ipaddress = '173.230.136.241'
        dbLoginInfo.defaultDB = 'test'

        try:
           loggedInUser = authenticateUser(username, password, dbLoginInfo)
        except Exception as error:
            messagebox.showerror('Invalid Login', 'Username and Password do not match')
            return loggedInUser

        print('Successful login')
        self.destroy()
        return loggedInUser
