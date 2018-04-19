import logging
import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import messagebox
from views import splashView, loginView, adminMainView, scrumMasterMainView, developerHomeView, backlogView, analyticsView

import platform
import webbrowser
from data import DataBlock
from frames import Dialogs
from tkinter import messagebox
import time
import threading

class masterView(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.w_rat, self.h_rat, full = getGeometryFromFile("geometry.txt")
        self.w_rat /= 1280
        self.h_rat /= 720
        w = 1280*self.w_rat
        h = 720*self.h_rat

        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.title("Scrumbles")
        if platform.system() == "Windows":
            self.iconbitmap("logo.ico")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        if full == 1:
            self.state('zoomed')
        self.frames = {}

        self.protocol('WM_DELETE_WINDOW', lambda s = self: exitProgram(s))
        self.container = tk.Frame(self)

        self.container.pack(side = "top", fill = "both", expand = True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.menuBar = None
        self.hiddenMenu = tk.Menu(self)

        loginFrame = loginView.loginView(self.container, self)
        self.add_frame(loginFrame, loginView)

        self.splashFrame = splashView.splashView(self.container, self)
        self.add_frame(self.splashFrame, splashView)

        self.show_frame(loginView)

        self.dataConnection = None
        self.activeUser = None

        try:
            self.bind('<Control-u>', self.showCreateUserDialog)
            self.bind('<Control-i>', self.showCreateItemDialog)
            self.bind('<Control-s>', self.showCreateSprintDialog)
            self.bind('<Control-p>', self.showCreateProjectDialog)

            self.bind('<Control-h>', self.showDeveloperHomeView)
            self.bind('<Control-b>', self.showBacklogView)
            self.bind('<Control-a>', self.showAnalyticsView)

            self.bind('<Control-r>', self.refreshData)

            self.bind('<Control-m>', self.showMainView)
        

        except Exception as e:
            logging.exception("User is not logged in")

        self.bind('<F1>', self.openUserGuide)

        self.bind('<Control-q>', self.windowQuit)
        self.bind('<Control-w>', self.windowMin)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        if cont != (loginView or splashView):
            self.raiseMenuBar()
        else:
            self.hideMenuBar()

    def add_frame(self, addedFrame, addedFrameClass):
        logging.info('Packing Frame %s' % str(addedFrame))
        self.frames[addedFrameClass] = addedFrame
        addedFrame.grid(row = 0, column = 0, sticky = "nsew")

    def generateMenuBar(self):
        menuBar = tk.Menu(self, cursor = "hand2")

        fileMenu = tk.Menu(menuBar, tearoff = 0, cursor = "hand2")
        self.fileMenu = fileMenu

        if self.activeUser.userRole == "Admin":
            fileMenu.add_command(label = "Create New Project", command = self.showCreateProjectDialog, accelerator = "CTRL+P")
        self.setOpenProjectsMenu(fileMenu)
        self.dataBlock.packCallback(self.updateOpenProjectsMenu)
        fileMenu.add_command(label = "Exit", command = lambda: exitProgram(self), accelerator = "CTRL+U")

        editMenu = tk.Menu(menuBar, tearoff = 0)
        if self.activeUser.userRole == "Admin":
            editMenu.add_command(label = "Create New User", underline = 11, command = self.showCreateUserDialog, accelerator = "CTRL+U")

        if self.activeUser.userRole == "Admin" or self.activeUser.userRole == "Scrum Master":
            editMenu.add_command(label = "Create New Sprint", underline = 11, command = self.showCreateSprintDialog, accelerator = "CTRL+S")
        editMenu.add_command(label = "Create New Item",  underline = 11, command = self.showCreateItemDialog, accelerator = "CTRL+I")

        profileMenu = tk.Menu(menuBar, tearoff=0)
        profileMenu.add_command(label = self.activeUser.userName)
        profileMenu.add_command(label = "Log Out", command = lambda: logOut(self))

        viewMenu = tk.Menu(menuBar, tearoff = 0, cursor = "hand2")
        if self.activeUser.userRole == "Admin":
            viewMenu.add_command(label = "Administrator Main", underline = 0, command = lambda: self.show_frame(adminMainView), accelerator = "CTRL+M")
        
        elif self.activeUser.userRole == "Scrum Master":
            viewMenu.add_command(label = "Scrum Master Main", underline = 0, command = lambda: self.show_frame(scrumMasterMainView), accelerator = "CTRL+M")

        viewMenu.add_command(label = "Developer Main", underline = 0, command = lambda: self.show_frame(developerHomeView), accelerator = "CTRL+H")
        viewMenu.add_command(label = "Backlog", underline = 0, command = lambda: self.show_frame(backlogView), accelerator = "CTRL+B")
        viewMenu.add_command(label = "Analytics View", underline = 0, command = lambda: self.show_frame(analyticsView), accelerator = "CTRL+A")

        helpMenu = tk.Menu(menuBar, tearoff = 0, cursor = "hand2")
        helpMenu.add_command(label = "User Guide", command = self.openUserGuide)
        helpMenu.add_command(label = "Scrumbles's API", command = self.openAPI)
        helpMenu.add_command(label = "Scrumbles's Current Status", command = self.openStatus)
        helpMenu.add_command(label = "What's With The Colors", command = self.colorHelp)
        helpMenu.add_command(label = 'Refresh Data', command = self.refreshData, accelerator = "CTRL+R")

        menuBar.add_cascade(label = "File", menu = fileMenu)
        menuBar.add_cascade(label = "Edit", menu = editMenu)
        menuBar.add_cascade(label = "Profile", menu = profileMenu)
        menuBar.add_cascade(label = "View", menu = viewMenu)
        menuBar.add_cascade(label = "Help", menu = helpMenu)

        self.menuBar = menuBar
        self.menuBar.config(cursor = "hand2")

    def colorHelp(self):
        Dialogs.AboutDialog(self, master = self).show()

    def raiseMenuBar(self):
        self.configure(menu = self.menuBar)

    def hideMenuBar(self):
        self.configure(menu = self.hiddenMenu)

    def getViews(self):
        views = []
        viewNames = []

        if self.activeUser.userRole == "Admin":
            views.append(adminMainView)
            viewNames.append("Admin Main")

        elif self.activeUser.userRole == "Scrum Master":
            views.append(scrumMasterMainView)
            viewNames.append("Scrum Master Main")

        views.append(developerHomeView)
        viewNames.append("Developer Home")

        views.append(backlogView)
        viewNames.append("Backlog")

        views.append(analyticsView)
        viewNames.append("Analytics")

        return views, viewNames

    def showCreateProjectDialog(self, event = None):
        Dialogs.CreateProjectDialog(self, master = self, dataBlock = self.dataBlock).show()
   
    def showCreateUserDialog(self, even = None):
        Dialogs.CreateUserDialog(self, master = self, dataBlock = self.dataBlock).show()

    def showCreateSprintDialog(self, event = None):
        Dialogs.CreateSprintDialog(self, master = self, dataBlock = self.dataBlock).show()

    def showCreateItemDialog(self, event = None):
        Dialogs.CreateItemDialog(self, master = self, dataBlock = self.dataBlock).show()

    def windowMin(self, event = None):
        minimize(self)

    def windowQuit(self, event = None):
        exitProgram(self)

    def showSplashView(self, event = None):
        self.show_frame(splashView)

    def showMainView(self, event = None):
        if self.activeUser.userRole == "Admin":
            self.show_frame(adminMainView)
        elif self.activeUser.userRole == "Scrum Master":
            self.show_frame(scrumMasterMainView)

    def showDeveloperHomeView(self, event = None):
        self.show_frame(developerHomeView)

    def showBacklogView(self, event = None):
        self.show_frame(backlogView)

    def showAnalyticsView(self, event = None):
        self.show_frame(analyticsView)

    def generateViews(self, loggedInUser):
        self.dataBlock = DataBlock.DataBlock()

        if self.dataBlock.isLoading is True:
            self.showSplashView()

        while self.dataBlock.isLoading:
            self.splashFrame.stepProgressBar(1)

        #todo
        threading.Thread(target = self.dataBlock.onConnectionLoss, args = (self.connectionLossHandler,)).start()

        self.activeProject = getProjectFromFile("project.txt", self.dataBlock)
        for user in self.dataBlock.users:
            if loggedInUser == user.userName:
                loggedInUser = user

        self.activeUser = loggedInUser

        if not self.activeUser.listOfProjects:
            messagebox.showinfo('No Assigned Projects', 'You are not currently assigned to any projects '
                                                        '\nPlease contact an administrator or team leader')
            logOut(self)
            return

        self.dataBlock.packCallback(self.repointActiveObjects)

        if self.activeUser.userRole == "Admin":
            adminMainFrame = adminMainView.adminMainView(self.container, self, loggedInUser)
        elif self.activeUser.userRole == "Scrum Master":
            scrumMasterMainFrame = scrumMasterMainView.scrumMasterMainView(self.container, self, loggedInUser)
        developerHomeFrame = developerHomeView.developerHomeView(self.container, self, loggedInUser)
        backlogFrame = backlogView.backlogView(self.container, self, loggedInUser)
        analyticsFrame = analyticsView.analyticsView(self.container, self)

        if self.activeUser.userRole == "Admin":
            self.add_frame(adminMainFrame, adminMainView)
        elif self.activeUser.userRole == "Scrum Master":
            self.add_frame(scrumMasterMainFrame, scrumMasterMainView)
        self.add_frame(developerHomeFrame, developerHomeView)
        self.add_frame(backlogFrame, backlogView)
        self.add_frame(analyticsFrame, analyticsView)

        self.generateMenuBar()

        self.showMainView()

        if self.activeUser.userRole == "Developer":
            self.showDeveloperHomeView()

        self.title("Scrumbles" + " - " + self.activeProject.projectName)
        if platform.system() == "Windows":
            self.iconbitmap("logo.ico")

    def openUserGuide(self, event = None):
        webbrowser.open_new_tab('https://github.com/CEN3031-group16/GroupProject/wiki/User-Guide')

    def connectionLossHandler(self):
        messagebox.showerror('Loss of Connection', 'Network Connection Lost, Logging Out of App')
        logOut(self)

    def openAPI(self):
        webbrowser.open_new_tab('https://github.com/CEN3031-group16/GroupProject/wiki/Scrumbles-API-Documentation')

    def openStatus(self):
        webbrowser.open_new_tab('https://github.com/CEN3031-group16/GroupProject/wiki/Current-Status')

    def updateOpenProjectsMenu(self):
        self.setOpenProjectsMenu(self.fileMenu)

    def setOpenProjectsMenu(self, menu):
        listOfProjects = [P.projectName for P in self.dataBlock.projects]

        try:
            menu.delete('Open Project')
        except Exception:
            logging.exception('Failed to delete menu')

        self.popMenu = tk.Menu(menu, tearoff = 0)
        if self.activeUser is None and (self.activeUser.userRole == "Scrum Master" or
                                        self.activeUser.userRole == "Developer"):
            for text in listOfProjects:
                for project in self.activeUser.listOfProjects:
                    if project.projectName == text:
                        self.popMenu.add_command(label = project.projectName,
                                                 command = lambda t = project.projectName: self.setActiveProject(t))
        else:
            for text in listOfProjects:
                self.popMenu.add_command(label = text, command = lambda t = text: self.setActiveProject(t))

        menu.insert_cascade(index = 1,
                            label = 'Open Project',
                            menu = self.popMenu)

    def setActiveProject(self, projectName):
        for P in self.dataBlock.projects:
            if P.projectName == projectName:
                self.activeProject = P
        self.title("Scrumbles" + " - " + self.activeProject.projectName)
        logging.info('Active Project set to %s' % self.activeProject.projectName)
        self.dataBlock.executeUpdaterCallbacks()

    def repointActiveObjects(self):
        for P in self.dataBlock.projects:
            if P.projectName == self.activeProject.projectName:
                self.activeProject = P
        for U in self.dataBlock.users:
            if U.userName == self.activeUser.userName:
                self.activeUser = U

    def refreshData(self, event = None):
        self.dataBlock.updateAllObjects()
        self.dataBlock.executeUpdaterCallbacks()

    def __str__(self):
        return 'Scrumbles Master View Controller'

def logOut(controller):
    logging.info('%s logged out' % controller.activeUser.userID)
    controller.dataBlock.shutdown()
    messagebox.showinfo('Logout', 'Shutting Down Active Threads')
    time.sleep(3)
    del controller.dataBlock
    #Do Some Stuff Here To Clear States
    loginFrame = loginView.loginView(controller.container, controller)
    controller.add_frame(loginFrame, loginView)
    controller.show_frame(loginView)
    controller.title("Scrumbles")

def exitProgram(mainWindow):
    try:
        setProjectFile(mainWindow.activeProject)
    except:
        pass
    setGeometryFile(mainWindow)
    plt.close('all')
    try:
        mainWindow.dataBlock.shutdown()
    except:
        logging.exception('Shutdown Failure')
    try:

        del mainWindow.dataBlock

        mainWindow.destroy()
    except:
        logging.exception('Shutdown Failure')
    finally:
        exit()
    logging.info("Shutting down gracefully")
    exit()

def minimize(mainwindow):
    mainwindow.iconify()

def getGeometryFromFile(file):
    try:
        geometryFile = open(file, 'r')
        w = processFile(geometryFile)
        h = processFile(geometryFile)
        full = processFile(geometryFile)
        w = int(w)
        h = int(h)
        full = int(full)
        geometryFile.close()
    except:
        w = 1280
        h = 720
        full = 0

    return w, h, full

def getProjectFromFile(file, dataBlock):
    print("Entered")
    try:
        projectFile = open(file, 'r')
        projectID = processFile(projectFile)
        projectID = int(projectID)
        projectFile.close()
    except:
        return dataBlock.projects[0]

    for project in dataBlock.projects:
        if project.projectID == projectID:
            return project

    return dataBlock.projects[0]

def processFile(openFile):
    item = openFile.readline()
    item = item.rstrip("\n\r")
    return item

def setGeometryFile(window):
    window.update()
    w = window.winfo_width()
    h = window.winfo_height()
    full = window.wm_state()
    if full == "zoomed":
        full = 1
    else:
        full = 0
    f = open("geometry.txt", "w+")
    f.write(str(w) + "\n")
    f.write(str(h) + "\n")
    f.write(str(full)+"\n")
    f.close()

def setProjectFile(activeProject):
    f = open("project.txt", "w+")
    f.write(str(activeProject.projectID) + "\n")
    f.close()
