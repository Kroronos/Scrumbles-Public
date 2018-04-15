import logging
import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import messagebox
from views import splashView, developerHomeView, mainView, teamManagerView, loginView, analyticsView

import platform
import webbrowser
from data import DataBlock
from frames import Dialogs
from tkinter import messagebox
import time
import threading

class masterView(tk.Tk):
    def __init__(self):

        print('Init masterView')
        tk.Tk.__init__(self)

        self.w_rat, self.h_rat = getGeometryFromFile("geometry.txt")
        self.w_rat /= 1280
        self.h_rat /= 720
        w = 1280*self.w_rat
        h = 720*self.h_rat
        print("Width: " + str(w))
        print("Height: " + str(h))
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.title("Scrumbles")
        if platform.system() == "Windows":
            self.iconbitmap("logo.ico")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

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
            
            self.bind('<Control-m>', self.showMainView)
            self.bind('<Control-h>', self.showHomeView)
            self.bind('<Control-t>', self.showTeamView)
            self.bind('<Control-a>', self.showAnalyticsView)

            self.bind('<Control-r>', self.refreshData)

        except Exception as inst:
            print("User is not logged in")

        self.bind('<Control-q>', self.windowQuit)
        self.bind('<Control-w>', self.windowMin)



  
    def show_frame(self, cont):
        frame = self.frames[cont]
        print("Switching Views")
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

        if (self.activeUser.userRole == "Admin"):
            fileMenu.add_command(label="Create New Project            Ctrl+p", command=self.showCreateProjectDialog)
        self.setOpenProjectsMenu(fileMenu)
        self.dataBlock.packCallback(self.updateOpenProjectsMenu)
        fileMenu.add_command(label="Exit                                      Ctrl+q", command=lambda:exitProgram(self))

        editMenu = tk.Menu(menuBar, tearoff=0)
        if (self.activeUser.userRole == "Admin"):
            editMenu.add_command(label="Create New User                  Ctrl+u", underline= 11, command=self.showCreateUserDialog)
        if (self.activeUser.userRole == "Admin" or self.activeUser.userRole == "Scrum Master"):
            editMenu.add_command(label="Create New Sprint                Ctrl+s", underline=11, command=self.showCreateSprintDialog)
        editMenu.add_command(label="Create New Item                  Ctrl+i",  underline=11,command=self.showCreateItemDialog)

        profileMenu = tk.Menu(menuBar, tearoff=0)
        profileMenu.add_command(label=self.activeUser.userName)
        profileMenu.add_command(label="Log Out", command=lambda: logOut(self))

        viewMenu = tk.Menu(menuBar, tearoff=0, cursor = "hand2")
        if (self.activeUser.userRole == "Admin"):
            viewMenu.add_command(label="Administrator Main     Ctrl+m", underline=0, command=lambda: self.show_frame(mainView))
        
        if (self.activeUser.userRole == "Scrum Master"):
            viewMenu.add_command(label="Scrum Master Main     Ctrl+m", underline=0, command=lambda: self.show_frame(mainView))
        
        elif (self.activeUser.userRole == "Developer"):
            viewMenu.add_command(label="Developer Main           Ctrl+m", underline=0, command=lambda: self.show_frame(mainView))



        viewMenu.add_command(label="Developer Home         Ctrl+h", underline=11, command=lambda: self.show_frame(developerHomeView))
        viewMenu.add_command(label="Team Manager             Ctrl+t", underline=0, command=lambda: self.show_frame(teamManagerView))
        viewMenu.add_command(label="Analytics View              Ctrl+a", underline=0, command = lambda: self.show_frame(analyticsView))


        helpMenu = tk.Menu(menuBar, tearoff=0, cursor = "hand2")
        helpMenu.add_command(label = "User Guide", command = self.openUserGuide)
        helpMenu.add_command(label = "Scrumbles's API", command = self.openAPI)
        helpMenu.add_command(label = "Scrumbles's Current Status", command = self.openStatus)
        helpMenu.add_command(label = "What's With The Colors", command=self.colorHelp)
        helpMenu.add_command(label = 'Refresh Data                Ctrl+r', command=self.refreshData)

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Edit", menu=editMenu)
        menuBar.add_cascade(label="Profile", menu=profileMenu)
        menuBar.add_cascade(label="View", menu=viewMenu)
        menuBar.add_cascade(label="Help", menu=helpMenu)


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
            views.append(mainView)
            viewNames.append("Admin Main")

        elif self.activeUser.userRole == "Scrum Master":
            views.append(mainView)
            viewNames.append("Scrum Master Main")

        elif self.activeUser.userRole == "Developer":
            views.append(mainView)
            viewNames.append("Developer Main")

        views.append(developerHomeView)
        viewNames.append("Developer Home")

        views.append(teamManagerView)
        viewNames.append("Team Manager")

        views.append(analyticsView)
        viewNames.append("Analytics")

        return views, viewNames


    def showCreateProjectDialog(self,event):

        Dialogs.CreateProjectDialog(self, master=self, dataBlock=self.dataBlock).show()
   
    def showCreateUserDialog(self,event):
        Dialogs.CreateUserDialog(self, master=self, dataBlock=self.dataBlock).show()


    def showCreateSprintDialog(self,event):
        Dialogs.CreateSprintDialog(self, master=self, dataBlock=self.dataBlock).show()

    def showCreateItemDialog(self,event):
        Dialogs.CreateItemDialog(self, master=self, dataBlock=self.dataBlock).show()



    def windowMin(self, event):
        minimize(self)

    def windowQuit(self, event):
        exitProgram(self)

    def showMainView(self, event):
        self.show_frame(mainView)

    def showHomeView(self, event):
        self.show_frame(developerHomeView)

    def showTeamView(self, event):
        self.show_frame(teamManagerView)

    def showAnalyticsView(self, event):
        self.show_frame(analyticsView)

    def generateViews(self, loggedInUser):

        self.dataBlock = DataBlock.DataBlock()

        if self.dataBlock.isLoading is True:
            self.show_frame(splashView)

        while self.dataBlock.isLoading:
            self.splashFrame.stepProgressBar(1)

        self.activeProject = self.dataBlock.projects[0]

        #todo
        threading.Thread(target = self.dataBlock.onConnectionLoss, args = (self.connectionLossHandler,)).start()

        print('Logged in %s' % loggedInUser)

        for user in self.dataBlock.users:
            if loggedInUser == user.userName:
                loggedInUser = user

        self.activeUser = loggedInUser
        print('%s Loggin in' % loggedInUser.userName)

        if not self.activeUser.listOfProjects:
            messagebox.showinfo('No Assigned Projects', 'You are not currently assigned to any projects '
                                                        '\nPlease contact an administrator or team leader')
            logOut(self)
            return

        self.dataBlock.packCallback(self.repointActiveObjects)

        homeFrame = mainView.mainView(self.container, self, loggedInUser)
        developerHomeFrame = developerHomeView.developerHomeView(self.container, self, loggedInUser)
        teamManagerFrame = teamManagerView.teamManagerView(self.container, self, loggedInUser)
        analyticsFrame = analyticsView.analyticsView(self.container, self)

        self.add_frame(homeFrame, mainView)
        self.add_frame(developerHomeFrame, developerHomeView)
        self.add_frame(teamManagerFrame, teamManagerView)
        self.add_frame(analyticsFrame, analyticsView)

        self.generateMenuBar()

        if self.activeUser.userRole == "Admin":
            self.show_frame(mainView)

        elif self.activeUser.userRole == "Scrum Master":
            self.show_frame(mainView)

        elif self.activeUser.userRole == "Developer":
            self.show_frame(developerHomeView)

        self.title("Scrumbles" + " - " + self.activeProject.projectName)
        if platform.system() == "Windows":
            self.iconbitmap("logo.ico")

    def openUserGuide(self):
        webbrowser.open_new_tab('https://github.com/CEN3031-group16/GroupProject/wiki/User-Guide')


    def connectionLossHandler(self):
        messagebox.showerror('Loss of Connection','Network Connection Lost, Logging Out of App')
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

        menu.insert_cascade(index=1, label='Open Project', menu=self.popMenu)

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

    def refreshData(self, event):
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

def showGettingStartedText():
    print("Get Started By Adding Creating A Project!")

def getGeometryFromFile(file):
    try:
        geometryFile = open(file, 'r')
        w = processFile(geometryFile)
        h = processFile(geometryFile)
        w = int(w)
        h = int(h)
        geometryFile.close()
    except:
        print("EXCEPTION ALERT")
        w = 1280
        h = 720

    return w, h

def processFile(openFile):
    item = openFile.readline()
    item = item.rstrip("\n\r")
    return item

def setGeometryFile(window):
    w = window.winfo_width()
    h = window.winfo_height()
    f = open("geometry.txt", "w+")
    f.write(str(w) + "\n")
    f.write(str(h) + "\n")
    f.close()
