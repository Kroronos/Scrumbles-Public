from tkinter import *
from mainView import *
from loginView import *

class masterView(Tk):
    def __init__(self):
        self.frames = {}

        Tk.__init__(self)
        self.container = Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.menuBar = self.generateMenuBar()
        self.hiddenMenu = Menu(self)

        loginFrame = loginView(self.container, self)

        self.add_frame(loginFrame, loginView)

        self.show_frame(loginView)

        self.title("Scrumbles")
        self.geometry("800x600")
        self.iconbitmap("logo.ico")


    def show_frame(self, cont):
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
        menuBar = Menu(self)

        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Exit", command=exitProgram)

        profileMenu = Menu(menuBar, tearoff=0)
        profileMenu.add_command(label="Log Out", command=lambda: logOut(self))

        viewMenu = Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="Main Menu", command=lambda: self.show_frame(mainView))
        viewMenu.add_command(label="Sprint View", command=lambda: self.show_frame(mainView))

        helpMenu = Menu(menuBar, tearoff=0)
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

def logOut(controller):
    print("Log Me Out Scotty")
    #Do Some Stuff Here To Clear States
    loginFrame = loginView(controller.container, controller)
    controller.add_frame(loginFrame, loginView)
    controller.show_frame(loginView)

def exitProgram():
    print("Exiting Program")
    exit()

def showGettingStartedText():
    print("Get Started By Adding Creating A Project!")