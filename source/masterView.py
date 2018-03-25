import tkinter as tk

import mainView 
import loginView
import backlogView
import developerHomeView
import itemManagerView
import teamView

import Dialogs
import ScrumblesData



class masterView(tk.Tk):
    def __init__(self):
        self.frames = {}
        self.dataBlock = ScrumblesData.DataBlock()
        tk.Tk.__init__(self)
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

        self.show_frame(loginView)
        self.dataConnection = None
        self.activeProject = None
        self.title("Scrumbles")
        self.geometry("1000x600")

        #self.iconbitmap("logo.ico")

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
        viewMenu.add_command(label="Main Menu", command=lambda: self.show_frame(mainView))
        viewMenu.add_command(label="Developer Home View", command=lambda: self.show_frame(developerHomeView))
        viewMenu.add_command(label="Team View", command=lambda: self.show_frame(teamView))
        viewMenu.add_command(label="Sprint View", command=lambda: self.show_frame(mainView))
        viewMenu.add_command(label="Projects Backlog View", command=lambda: self.show_frame(backlogView))
        viewMenu.add_command(label = "Item Manager View", command = lambda: self.show_frame(itemManagerView))

        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="About", command=self.openAboutDialog)

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
        viewNames.append("Main View")

        views.append(developerHomeView)
        viewNames.append("Developer Home View")

        views.append(teamView)
        viewNames.append("Team View")

        views.append(backlogView)
        viewNames.append("Backlog View")

        views.append(itemManagerView)
        viewNames.append("Item Manager View")
        return views, viewNames

    def showCreateProjectDialog(self):
        createProjectDialog = Dialogs.CreateProjectDialog(self,self.dataBlock)
        self.wait_window(createProjectDialog.top)

    def showCreateUserDialog(self):
        createUserDialog = Dialogs.CreateUserDialog(self, self.dataBlock)
        self.wait_window(createUserDialog.top)

    def showCreateSprintDialog(self):
        createSprintDialog = Dialogs.CreateSprintDialog(self, self.dataBlock)
        self.wait_window(createSprintDialog.top)

    def showCreateItemDialog(self):
        createItemDialog = Dialogs.CreateItemDialog(self,self.dataBlock)
        self.wait_window(createItemDialog.top)

    def generateViews(self, loggedInUser):
        self.activeUser = loggedInUser
        mainFrame = mainView.mainView(self.container, self, loggedInUser)
        developerHomeFrame = developerHomeView.developerHomeView(self.container, self, loggedInUser)
        backlogViewFrame = backlogView.backlogView(self.container, self, loggedInUser)
        itemManagerFrame = itemManagerView.ItemManagerView(self.container, self)
        teamViewFrame = teamView.teamView(self.container, self, loggedInUser)

        self.add_frame(mainFrame, mainView)
        self.add_frame(developerHomeFrame, developerHomeView)
        self.add_frame(backlogViewFrame, backlogView)
        self.add_frame(itemManagerFrame, itemManagerView)
        self.add_frame(teamViewFrame, teamView)
        
        self.show_frame(mainView)

    def setDatabaseConnection(self):
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        self.dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)

    def openAboutDialog(self):
        helpBox = Dialogs.AboutDialog(self)

        self.wait_window(helpBox.top)

    def updateOpenProjectsMenu(self):
        self.setOpenProjectsMenu(self.fileMenu)

    def setOpenProjectsMenu(self,menu):
        listOfProjects = [P.projectName for P in self.dataBlock.projects]
        try:
            menu.delete('Open Project')
        except Exception:
            pass
        self.popMenu = tk.Menu(menu,tearoff=0)
        for text in listOfProjects:
            self.popMenu.add_command(label=text,command = lambda t=text:self.setActiveProject(t))

        menu.add_cascade(label='Open Project',menu=self.popMenu,underline=0)

    def setActiveProject(self,projectName):
        for P in self.dataBlock.projects:
            if P.projectName == projectName:
                self.activeProject = P

        print('Active Project set to', self.activeProject.projectName)

def logOut(controller):
    print("Log Me Out Scotty")
    #Do Some Stuff Here To Clear States
    loginFrame = loginView.loginView(controller.container, controller)
    controller.add_frame(loginFrame, loginView)
    controller.show_frame(loginView)

def exitProgram(mainwindow):
    mainwindow.dataBlock.shutdown()
    mainwindow.destroy()
    print("Exiting Program")
    exit()

def showGettingStartedText():
    print("Get Started By Adding Creating A Project!")

