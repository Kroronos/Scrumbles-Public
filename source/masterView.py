import logging
import tkinter as tk
from tkinter import messagebox
import mainView
import loginView
import developerHomeView
import teamManagerView
import sprintManagerView
import backlogManagerView
import itemManagerView
import platform

import time

import webbrowser


import DataBlock
import Dialogs
import ScrumblesData


class masterView(tk.Tk):
    def __init__(self):

        print('Init masterView')
        tk.Tk.__init__(self)
        self.withdraw()
        w = 1280
        h = 720
        ws =self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.title("Scrumbles")
        # self.geometry("1280x720")
        if platform.system() == "Windows":
            self.iconbitmap("logo.ico")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.splash = Dialogs.SplashScreen(self)

        self.frames = {}
        print('Init DataBlock')
        self.dataBlock = DataBlock.DataBlock()

        while self.dataBlock.isLoading:
             self.splash.step_progressBar(1)


        self.splash.kill()

        self.dataBlock.packCallback(self.repointActiveObjects)
        self.protocol('WM_DELETE_WINDOW', lambda s=self: exitProgram(s))
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.menuBar = self.generateMenuBar()
        self.hiddenMenu = tk.Menu(self)

        loginFrame = loginView.loginView(self.container, self)
        #mainFrame = mainView.mainView(self.container, self)

       # self.add_frame(mainFrame, mainView)
        
        self.add_frame(loginFrame, loginView)





        self.deiconify()
        self.show_frame(loginView)
        self.dataConnection = None
        self.activeProject = self.dataBlock.projects[0]


        self.activeUser = None




    def show_frame(self, cont):
        #print("Dictionary issue")
        frame = self.frames[cont]
        print("Switching Views")
        frame.tkraise()

        if(cont!=loginView):
            self.raiseMenuBar()
        else:
            self.hideMenuBar()

    def add_frame(self, addedFrame, addedFrameClass):
        logging.info('Packing Frame %s'% str(addedFrame))
        self.frames[addedFrameClass] = addedFrame
        addedFrame.grid(row=0, column=0, sticky="nsew")

    def generateMenuBar(self):
        menuBar = tk.Menu(self)

        fileMenu = tk.Menu(menuBar, tearoff=0)
        self.fileMenu = fileMenu
        fileMenu.add_command(label="Create New Project", command=self.showCreateProjectDialog)
        self.setOpenProjectsMenu(fileMenu)
        self.dataBlock.packCallback(self.updateOpenProjectsMenu)
        fileMenu.add_command(label="Exit", command=lambda:exitProgram(self))

        editMenu = tk.Menu(menuBar, tearoff=0)
        editMenu.add_command(label="Create New User", command=self.showCreateUserDialog)
        editMenu.add_command(label="Create New Sprint", command=self.showCreateSprintDialog)
        editMenu.add_command(label="Create New Item", command=self.showCreateItemDialog)

        profileMenu = tk.Menu(menuBar, tearoff=0)
        profileMenu.add_command(label="Log Out", command=lambda: logOut(self))

        viewMenu = tk.Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="Main", command=lambda: self.show_frame(mainView))
        viewMenu.add_command(label="Developer Home", command=lambda: self.show_frame(developerHomeView))
        viewMenu.add_command(label="Team Manager", command=lambda: self.show_frame(teamManagerView))
        viewMenu.add_command(label="Sprint Manager", command=lambda: self.show_frame(sprintManagerView))
        viewMenu.add_command(label="Projects Backlog", command=lambda: self.show_frame(backlogManagerView))
        viewMenu.add_command(label="Item Manager", command = lambda: self.show_frame(itemManagerView))


        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label = "Scrumbles's API", command = self.openAPI)
        helpMenu.add_command(label = "Scrumbles's Current Status", command = self.openStatus)

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Edit", menu=editMenu)
        menuBar.add_cascade(label="Profile", menu=profileMenu)
        menuBar.add_cascade(label="View", menu=viewMenu)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        return menuBar

    def raiseMenuBar(self):
        self.configure(menu=self.menuBar)

    def hideMenuBar(self):
        self.configure(menu=self.hiddenMenu)

    def getViews(self):
        views = []
        viewNames = []
        views.append(mainView)
        viewNames.append("Main")

        views.append(developerHomeView)
        viewNames.append("Developer Home")

        views.append(teamManagerView)
        viewNames.append("Team Manager")

        views.append(sprintManagerView)
        viewNames.append("Sprint Manager")

        views.append(backlogManagerView)
        viewNames.append("Backlog Manager")

        views.append(itemManagerView)
        viewNames.append("Item Manager")
        return views, viewNames

    def showCreateProjectDialog(self):
        if self.activeUser.userRole == "Admin":
            createProjectDialog = Dialogs.CreateProjectDialog(self,self.dataBlock)
            self.wait_window(createProjectDialog.top)
        else:
            messagebox.showerror('Access Denied', 'Must Be An Administrator')


    def showCreateUserDialog(self):
        if self.activeUser.userRole == "Admin":
            createUserDialog = Dialogs.CreateUserDialog(self, self.dataBlock)
            self.wait_window(createUserDialog.top)
        else:
            messagebox.showerror('Access Denied', 'Must Be An Administrator')

    def showCreateSprintDialog(self):
        if self.activeUser.userRole == "Admin" or self.activeUser.userRole == "Scrum Master":
            createSprintDialog = Dialogs.CreateSprintDialog(self, self.dataBlock)
            self.wait_window(createSprintDialog.top)
        else:
            messagebox.showerror('Access Denied', 'Must Be An Administrator')

    def showCreateItemDialog(self):
        createItemDialog = Dialogs.CreateItemDialog(self,self.dataBlock)
        self.wait_window(createItemDialog.top)

    def generateViews(self, loggedInUser):
        self.activeUser = loggedInUser
        mainFrame = mainView.mainView(self.container, self, loggedInUser)
        developerHomeFrame = developerHomeView.developerHomeView(self.container, self, loggedInUser)
        teamManagerFrame = teamManagerView.teamManagerView(self.container, self, loggedInUser)
        sprintManagerFrame = sprintManagerView.sprintManagerView(self.container, self)
        backlogManagerFrame = backlogManagerView.backlogManagerView(self.container, self, loggedInUser)
        itemManagerFrame = itemManagerView.ItemManagerView(self.container, self)

        self.add_frame(mainFrame, mainView)
        self.add_frame(developerHomeFrame, developerHomeView)
        self.add_frame(teamManagerFrame, teamManagerView)
        self.add_frame(sprintManagerFrame, sprintManagerView)
        self.add_frame(backlogManagerFrame, backlogManagerView)
        self.add_frame(itemManagerFrame, itemManagerView)
        
        self.show_frame(mainView)
        self.title("Scrumbles"+" - "+self.activeProject.projectName)
        self.iconbitmap("logo.ico")

    def setDatabaseConnection(self):
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        self.dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)

   
    def openAPI(self):
        webbrowser.open_new_tab('https://github.com/CEN3031-group16/GroupProject/wiki/Scrumbles-API-Documentation')

    def openStatus(self):
        webbrowser.open_new_tab('https://github.com/CEN3031-group16/GroupProject/wiki/Current-Status')

    def updateOpenProjectsMenu(self):
        self.setOpenProjectsMenu(self.fileMenu)

    def setOpenProjectsMenu(self,menu):
        listOfProjects = [P.projectName for P in self.dataBlock.projects]
        try:
            menu.delete('Open Project')
        except Exception:
            logging.exception('Failed to delete menu')

        self.popMenu = tk.Menu(menu,tearoff=0)
        for text in listOfProjects:
            self.popMenu.add_command(label=text, command=lambda t=text: self.setActiveProject(t))

        menu.insert_cascade(index=1, label='Open Project', menu=self.popMenu, underline=0)

    def setActiveProject(self,projectName):
        for P in self.dataBlock.projects:
            if P.projectName == projectName:
                self.activeProject = P
        self.title("Scrumbles"+" - "+self.activeProject.projectName)
        logging.info('Active Project set to %s' % self.activeProject.projectName)
        self.dataBlock.executeUpdaterCallbacks()

    def repointActiveObjects(self):
        for P in self.dataBlock.projects:
            if P.projectName == self.activeProject.projectName:
                self.activeProject = P
        for U in self.dataBlock.users:
            if U.userName == self.activeUser.userName:
                self.activeUser = U

def logOut(controller):
    logging.info('%s logged out'%controller.activeUser.userID)
    #Do Some Stuff Here To Clear States
    loginFrame = loginView.loginView(controller.container, controller)
    controller.add_frame(loginFrame, loginView)
    controller.show_frame(loginView)
    controller.title("Scrumbles")

def exitProgram(mainwindow):
    mainwindow.dataBlock.shutdown()
    mainwindow.destroy()
    logging.info("Shutting down gracefully")
    exit()

def showGettingStartedText():
    print("Get Started By Adding Creating A Project!")
