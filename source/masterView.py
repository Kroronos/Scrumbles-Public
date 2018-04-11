import logging
import tkinter as tk
from tkinter import messagebox
import adminMainView
import SMmainView
import loginView
import developerHomeView
import teamManagerView
import itemManagerView
import platform
import webbrowser
import DataBlock
import Dialogs


class masterView(tk.Tk):
    def __init__(self):

        print('Init masterView')
        tk.Tk.__init__(self)

        self.w_rat, self.h_rat = getGeometryFromFile("geometry.txt")
        self.w_rat /= 1280
        self.h_rat/= 720
        w = 1280*self.w_rat
        h = 720*self.h_rat
        print("Width: " + str(w))
        print("Height: " + str(h))
        ws =self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.title("Scrumbles")
        if platform.system() == "Windows":
            self.iconbitmap("logo.ico")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))


        self.frames = {}







        self.protocol('WM_DELETE_WINDOW', lambda s=self: exitProgram(s))
        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.menuBar = None
        self.hiddenMenu = tk.Menu(self)

        loginFrame = loginView.loginView(self.container, self)
        
        self.add_frame(loginFrame, loginView)


        self.show_frame(loginView)
        self.dataConnection = None





        self.activeUser = None

    def show_frame(self, cont):
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
        if (self.activeUser.userRole == "Admin"):
            fileMenu.add_command(label="Create New Project", command=self.showCreateProjectDialog)
        self.setOpenProjectsMenu(fileMenu)
        self.dataBlock.packCallback(self.updateOpenProjectsMenu)
        fileMenu.add_command(label="Exit", command=lambda:exitProgram(self))

        editMenu = tk.Menu(menuBar, tearoff=0)
        if (self.activeUser.userRole == "Admin"):
            editMenu.add_command(label="Create New User", command=self.showCreateUserDialog)
        if (self.activeUser.userRole == "Admin" or self.activeUser.userRole == "Scrum Master"):
            editMenu.add_command(label="Create New Sprint", command=self.showCreateSprintDialog)
        editMenu.add_command(label="Create New Item", command=self.showCreateItemDialog)

        profileMenu = tk.Menu(menuBar, tearoff=0)
        profileMenu.add_command(label=self.activeUser.userName)
        profileMenu.add_command(label="Log Out", command=lambda: logOut(self))

        viewMenu = tk.Menu(menuBar, tearoff=0)
        if (self.activeUser.userRole == "Admin"):
            viewMenu.add_command(label="Administrator Home", command=lambda: self.show_frame(adminMainView))
        if (self.activeUser.userRole == "Scrum Master"):
            viewMenu.add_command(label="Scrum Master Home", command=lambda: self.show_frame(SMmainView))       
        elif (self.activeUser.userRole == "Developer"):
            viewMenu.add_command(label="Developer Home", command=lambda: self.show_frame(developerHomeView))
        
        viewMenu.add_command(label="Team Manager", command=lambda: self.show_frame(teamManagerView))
        viewMenu.add_command(label="Sprint Manager", command=lambda: self.show_frame(sprintManagerView))
        viewMenu.add_command(label="Projects Backlog", command=lambda: self.show_frame(backlogManagerView))
        viewMenu.add_command(label="Item Manager", command = lambda: self.show_frame(itemManagerView))


        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label = "Scrumbles's API", command = self.openAPI)
        helpMenu.add_command(label = "Scrumbles's Current Status", command = self.openStatus)
        helpMenu.add_command(label = "What's with the colors", command=self.colorHelp)
        helpMenu.add_command(label = 'Refresh Data',command=self.refreshData)

        menuBar.add_cascade(label="File", menu=fileMenu)
        menuBar.add_cascade(label="Create", menu=editMenu)
        menuBar.add_cascade(label="Profile", menu=profileMenu)
        menuBar.add_cascade(label="View", menu=viewMenu)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        self.menuBar = menuBar

    def colorHelp(self):
        Dialogs.AboutDialog(self, master=self).show()

    def raiseMenuBar(self):
        self.configure(menu=self.menuBar)

    def hideMenuBar(self):
        self.configure(menu=self.hiddenMenu)

    def getViews(self):
        views = []
        viewNames = []
        if (self.activeUser.userRole == "Admin"):
            views.append(adminMainView)
            viewNames.append("Admin Home")

        elif (self.activeUser.userRole == "Scrum Master"):
            views.append(SMmainView)
            viewNames.append("Scrum Master Home")  

        views.append(developerHomeView)
        viewNames.append("Developer Home")

        views.append(teamManagerView)
        viewNames.append("Team Manager")


        views.append(itemManagerView)
        viewNames.append("Item Manager")
        return views, viewNames

    def showCreateProjectDialog(self):

        Dialogs.CreateProjectDialog(self, master=self, dataBlock=self.dataBlock).show()
    def showCreateUserDialog(self):
        Dialogs.CreateUserDialog(self, master=self, dataBlock=self.dataBlock).show()


    def showCreateSprintDialog(self):
        Dialogs.CreateSprintDialog(self, master=self, dataBlock=self.dataBlock).show()

    def showCreateItemDialog(self):
        Dialogs.CreateItemDialog(self, master=self, dataBlock=self.dataBlock).show()

    def generateViews(self, loggedInUser):
        self.withdraw()
        self.splash = Dialogs.SplashScreen(self, self)


        self.dataBlock = DataBlock.DataBlock()

        while self.dataBlock.isLoading:
            self.splash.step_progressBar(1)

        self.activeProject = self.dataBlock.projects[0]

        print('Logged in %s'%loggedInUser)

        for user in self.dataBlock.users:
             if loggedInUser == user.userName:
                 loggedInUser = user
        self.activeUser = loggedInUser
        print('%s Loggin in'%loggedInUser.userName)
        self.dataBlock.packCallback(self.repointActiveObjects)


        AdminHomeFrame = adminMainView.adminMainView(self.container, self, loggedInUser)
        ScrumMasterHomeFrame = SMmainView.SMmainView(self.container, self, loggedInUser)
        developerHomeFrame = developerHomeView.developerHomeView(self.container, self, loggedInUser)
        teamManagerFrame = teamManagerView.teamManagerView(self.container, self, loggedInUser)
        itemManagerFrame = itemManagerView.ItemManagerView(self.container, self)

        self.add_frame(AdminHomeFrame, adminMainView)
        self.add_frame(ScrumMasterHomeFrame, SMmainView)
        self.add_frame(developerHomeFrame, developerHomeView)
        self.add_frame(teamManagerFrame, teamManagerView)
        self.add_frame(itemManagerFrame, itemManagerView)

        self.generateMenuBar()
        self.splash.kill()
        self.deiconify()
        if (self.activeUser.userRole == "Admin"):
            self.show_frame(adminMainView)

        elif (self.activeUser.userRole == "Scrum Master"):
            self.show_frame(SMmainView)

        elif (self.activeUser.userRole == "Developer"):
            self.show_frame(developerHomeView)


        self.title("Scrumbles"+" - "+self.activeProject.projectName)
        if platform.system() == "Windows":
            self.iconbitmap("logo.ico")

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
        if(self.activeUser != None and (self.activeUser.userRole == "Scrum Master" or self.activeUser.userRole == "Developer")):
            for text in listOfProjects:
                for project in self.activeUser.listOfProjects:
                    if(project.projectName == text):
                        self.popMenu.add_command(label=project.projectName, command=lambda t=project.projectName: self.setActiveProject(t))
        else:
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

    def refreshData(self):
        self.dataBlock.updateAllObjects()
        self.dataBlock.executeUpdaterCallbacks()

    def __str__(self):
        return 'Scrumbles Master View Controller'

def logOut(controller):
    logging.info('%s logged out'%controller.activeUser.userID)
    #Do Some Stuff Here To Clear States
    loginFrame = loginView.loginView(controller.container, controller)
    controller.add_frame(loginFrame, loginView)
    controller.show_frame(loginView)
    controller.title("Scrumbles")

def exitProgram(mainwindow):
    setGeometryFile(mainwindow)
    try:
        mainwindow.dataBlock.shutdown()
        mainwindow.destroy()
    except:
        pass
    logging.info("Shutting down gracefully")
    exit()

def showGettingStartedText():
    print("Get Started By Adding Creating A Project!")

def getGeometryFromFile(file):
    try:
        geometryFile = open(file,'r')
        w = processFile(geometryFile)
        h = processFile(geometryFile)
        w = int(w)
        h = int(h)
        geometryFile.close()
    except:
        print("EXCEPTION ALERTTTT")
        w = 1280
        h = 720

    return w,h

def processFile(openFile):
    item = openFile.readline()
    item = item.rstrip("\n\r")
    return item

def setGeometryFile(window):
    w = window.winfo_width()
    h = window.winfo_height()
    f = open("geometry.txt", "w+")
    f.write(str(w)+"\n")
    f.write(str(h)+"\n")
    f.close()
