import tkinter as tk
import mainView 
import loginView
import backlogView
import developerHomeView
import Dialogs
import ScrumblesData
import itemMangerView
import sprintManagerView

class masterView(tk.Tk):
    def __init__(self):
        self.frames = {}

        tk.Tk.__init__(self)
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.menuBar = self.generateMenuBar()
        self.hiddenMenu = tk.Menu(self)

        loginFrame = loginView.loginView(self.container, self)
        #mainFrame = mainView.mainView(self.container, self)

        #self.add_frame(mainFrame, mainView)
        
        self.add_frame(loginFrame, loginView)

        self.show_frame(loginView)
        self.dataConnection = None
        self.title("Scrumbles")
        self.geometry("1000x600")
        self.iconbitmap("logo.ico")


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
        fileMenu.add_command(label="Create New User", command=self.showCreateUserDialog)
        fileMenu.add_command(label="Create New Sprint", command=self.showCreateSprintDialog)
        fileMenu.add_command(label="Create New Item", command=self.showCreateItemDialog)
        fileMenu.add_command(label="Create New Project", command=self.showCreateProjectDialog)
        fileMenu.add_command(label="Exit", command=lambda:exitProgram(self))


        profileMenu = tk.Menu(menuBar, tearoff=0)
        profileMenu.add_command(label="Log Out", command=lambda: logOut(self))

        viewMenu = tk.Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="Main Menu", command=lambda: self.show_frame(mainView))
        viewMenu.add_command(label="Developer Home View", command=lambda: self.show_frame(developerHomeView))
        viewMenu.add_command(label="Sprint Manager View", command=lambda: self.show_frame(sprintManagerView))
        viewMenu.add_command(label="Projects Backlog View", command=lambda: self.show_frame(backlogView))
        viewMenu.add_command(label="Item Manager View", command = lambda: self.show_frame(itemMangerView))

        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="About", command=self.openAboutDialog)

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Profile", menu=profileMenu)
        menuBar.add_cascade(label="View", menu=viewMenu)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        return menuBar

    def raiseMenuBar(self):
        self.configure(menu=self.menuBar)

    def hideMenuBar(self):
        self.configure(menu=self.hiddenMenu)

    def showCreateProjectDialog(self):
        createProjectDialog = Dialogs.CreateProjectDialog(self,self.dataConnection)
        self.wait_window(createProjectDialog.top)

    def showCreateUserDialog(self):
        createUserDialog = Dialogs.CreateUserDialog(self, self.dataConnection)
        self.wait_window(createUserDialog.top)

    def showCreateSprintDialog(self):
        createSprintDialog = Dialogs.CreateSprintDialog(self, self.dataConnection)
        self.wait_window(createSprintDialog.top)

    def showCreateItemDialog(self):
        createItemDialog = Dialogs.CreateItemDialog(self,self.dataConnection)
        self.wait_window(createItemDialog.top)

    def generateViews(self, loggedInUser):
        mainFrame = mainView.mainView(self.container, self, loggedInUser)
        developerHomeFrame = developerHomeView.developerHomeView(self.container, self, loggedInUser)
        backlogViewFrame = backlogView.backlogView(self.container, self, loggedInUser)
        itemMangerFrame = itemMangerView.ItemManagerView(self.container, self)
        sprintManagerFrame = sprintManagerView.sprintManagerView(self.container, self)

        self.add_frame(mainFrame, mainView)
        self.add_frame(developerHomeFrame, developerHomeView)
        self.add_frame(backlogViewFrame, backlogView)
        self.add_frame(itemMangerFrame,itemMangerView)
        self.add_frame(sprintManagerFrame, sprintManagerView)
        
        self.show_frame(mainView)

    def setDatabaseConnection(self):
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        self.dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)

    def openAboutDialog(self):
        helpBox = Dialogs.AboutDialog(self)
        self.wait_window(helpBox.top)


def logOut(controller):
    print("Log Me Out Scotty")
    #Do Some Stuff Here To Clear States
    loginFrame = loginView.loginView(controller.container, controller)
    controller.add_frame(loginFrame, loginView)
    controller.show_frame(loginView)

def exitProgram(mainwindow):
    mainwindow.destroy()
    print("Exiting Program")
    exit()

def showGettingStartedText():
    print("Get Started By Adding Creating A Project!")

