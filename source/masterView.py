import tkinter as tk
import mainView 
import loginView
import developerHomeView
import Dialogs
import ScrumblesData


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

       # self.add_frame(mainFrame, mainView)
        
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
        fileMenu.add_command(label="Exit", command=lambda:exitProgram(self))

        profileMenu = tk.Menu(menuBar, tearoff=0)
        profileMenu.add_command(label="Log Out", command=lambda: logOut(self))

        viewMenu = tk.Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="Main Menu", command=lambda: self.show_frame(mainView))
        viewMenu.add_command(label="Developer Home View", command=lambda: self.show_frame(developerHomeView))
        viewMenu.add_command(label="Sprint View", command=lambda: self.show_frame(mainView))

        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Getting Started", command=showGettingStartedText)

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Profile", menu=profileMenu)
        menuBar.add_cascade(label="View", menu=viewMenu)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        return menuBar

    def raiseMenuBar(self):
        self.configure(menu=self.menuBar)

    def hideMenuBar(self):
        self.configure(menu=self.hiddenMenu)

    def showCreateUserDialog(self):
        createUserDialog = Dialogs.CreateUserDialog(self, self.dataConnection)
        self.wait_window(createUserDialog.top)

    def showCreateSprintDialog(self):
        createSprintDialog = Dialogs.CreateSprintDialog(self, self.dataConnection)
        self.wait_window(createSprintDialog.top)

    def generateViews(self, loggedInUser):
        mainFrame = mainView.mainView(self.container, self, loggedInUser)
        self.add_frame(mainFrame, mainView)

        developerHomeFrame = developerHomeView.developerHomeView(self.container, self, loggedInUser)
        self.add_frame(developerHomeFrame, developerHomeView)
        self.show_frame(mainView)

    def setDatabaseConnection(self):
        dbLoginInfo = ScrumblesData.DataBaseLoginInfo("login.txt")
        dbLoginInfo.userID = 'test_user'
        dbLoginInfo.password = 'testPassword'
        dbLoginInfo.ipaddress = '173.230.136.241'
        dbLoginInfo.defaultDB = 'test'
        self.dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)


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