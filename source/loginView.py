import tkinter as tk
from tkinter import messagebox
from Query import Query
import masterView
import logging
import ScrumblesData



def authenticateUser(username, password, dbLoginInfo):
    user = None
    dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)
    dataConnection.connect()
    result = dataConnection.getData(Query.getUserByUsernameAndPassword(username, password))
    dataConnection.close()
    if result == ():
        logging.warning('Login Failed for %s' % username)
        raise Exception('Invalid USERNAME PASSWORD combo')
    else:
        user = username
        logging.info('%s Successfully logged in' % username)
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
        controller.protocol('WM_DELETE_WINDOW', lambda s=controller: masterView.exitProgram(s))
        self.inputFrame = tk.Frame(self)
        self.controller = controller

        self.usernameLabel = tk.Label(self.inputFrame, text="Username")
        self.passwordLabel = tk.Label(self.inputFrame, text="Password")
        self.usernameEntry = tk.Entry(self.inputFrame)
        self.passwordEntry = tk.Entry(self.inputFrame, show='*')
        self.loginButton = tk.Button(self.inputFrame, text='Login', command=lambda: self.loginProcess())
        self.loginButtonBypassAdmin = tk.Button(self.inputFrame, text='Bypass as AdminUser', command=lambda: self.loginProcessBypassAdmin())
        self.loginButtonBypassSM = tk.Button(self.inputFrame, text='Bypass as ScrumMaster', command=lambda: self.loginProcessBypassSM())
        self.loginButtonBypassDev = tk.Button(self.inputFrame, text='Bypass as DevUser', command=lambda: self.loginProcessBypassDev())

        self.usernameLabel.grid(row=3, column=2, sticky=tk.EW)
        self.usernameEntry.grid(row=3, column=3, columnspan=2, sticky=tk.EW)

        self.passwordLabel.grid(row=4, column=2, sticky=tk.EW)
        self.passwordEntry.grid(row=4, column=3, columnspan=2, sticky=tk.EW)
        self.loginButton.grid(row=6, column=3, sticky=tk.EW)
        self.loginButtonBypassAdmin.grid(row=7, column=3, sticky=tk.EW)
        self.loginButtonBypassSM.grid(row=8, column=3, sticky=tk.EW)
        self.loginButtonBypassDev.grid(row=9, column=3, sticky=tk.EW)



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

            self.controller.generateViews(loggedInUser)

    def loginButtonClicked(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        loggedInUserName = None

        try:
            loggedInUserName = authenticateUser(username, password, dbLoginInfo)

        except Exception as error:
            logging.warning('Failed Login user %s'% username)
            messagebox.showerror('Invalid Login', 'Username and Password do not match')
            return loggedInUserName

        print('Successful login')
        self.destroy()
        return loggedInUserName



        ############################################

    def loginProcessBypassAdmin(self):
        loggedInUser = self.loginButtonClickedBypassAdmin()
        if (loggedInUser is not None):
            print('loginProcessBypassAdmin')

            self.controller.generateViews(loggedInUser)


    def loginButtonClickedBypassAdmin(self):
        username = "AdminUser"#self.usernameEntry.get()
        password = "Password1"#self.passwordEntry.get()

        loggedInUserName = None
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        try:
           loggedInUserName = authenticateUser(username, password, dbLoginInfo)

        except Exception as error:
            logging.warning('Failed login %s' % username )
            messagebox.showerror('Invalid Login', 'Username and Password do not match')
            return loggedInUserName

        print('Successful login')
        self.destroy()
        return loggedInUserName
        ##################################################
    def loginProcessBypassSM(self):
        loggedInUser = self.loginButtonClickedBypassSM()
        if (loggedInUser is not None):
            #self.controller.setDatabaseConnection()
            self.controller.generateViews(loggedInUser)


    def loginButtonClickedBypassSM(self):
        username = "ScrumMaster"#self.usernameEntry.get()
        password = "Password1"#self.passwordEntry.get()

        loggedInUserName = None
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        try:
           loggedInUserName = authenticateUser(username, password, dbLoginInfo)

        except Exception as error:
            logging.warning('Failed login %s' % username )
            messagebox.showerror('Invalid Login', 'Username and Password do not match')
            return loggedInUserName

        print('Successful login')
        self.destroy()
        return loggedInUserName
        ##################################################
    def loginProcessBypassDev(self):
        loggedInUser = self.loginButtonClickedBypassDev()
        if (loggedInUser is not None):

            self.controller.generateViews(loggedInUser)


    def loginButtonClickedBypassDev(self):
        username = "DevUser"#self.usernameEntry.get()
        password = "Password1"#self.passwordEntry.get()

        loggedInUserName = None
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        try:
           loggedInUserName = authenticateUser(username, password, dbLoginInfo)

        except Exception as error:
            logging.warning('Failed login %s' % username )
            messagebox.showerror('Invalid Login', 'Username and Password do not match')
            return loggedInUserName

        print('Successful login')
        self.destroy()
        return loggedInUserName
        ##################################################