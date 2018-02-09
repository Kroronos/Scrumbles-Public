from ScrumblesData import *
from tkinter import *


def authenticateUser(username, password, dbLoginInfo):
    userID = None
    dataConnection = ScrumblesData(dbLoginInfo)
    dataConnection.connect()
    result = dataConnection.getData(Query.getUserIdByUsernameAndPassword(username, password))
    dataConnection.close()
    if result == ():
        raise Exception('Invalid USERNAME PASSWORD combo')
    else:
        userId = result[0]['UserID']
    return userId


def viewSprintWindow():
    print("View Sprint Called")


def viewBacklogWindow():
    print("View Backlog Called")


def viewUserWindow():
    print("View user called")


class LoginDialog(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.usernameLabel = Label(self, text="Username")
        self.passwordLabel = Label(self, text="Password")
        self.usernameEntry = Entry(self)
        self.passwordEntry = Entry(self, show='*')

        self.usernameLabel.grid(row=0, sticky=E)
        self.passwordLabel.grid(row=1, sticky=E)
        self.usernameEntry.grid(row=0, column=1)
        self.passwordEntry.grid(row=1, column=1)

        self.loginButton = Button(self, text='Login', command= lambda: self.loginProcess())
        self.loginButton.grid(columnspan=2)

        self.pack()

    def loginProcess(self):
        validation = self.loginButtonClicked()
        if(validation):
            mainFrame = mainView(self.controller.container, self.controller)
            self.controller.add_frame(mainFrame, mainView)
            self.controller.show_frame(mainView)

    def loginButtonClicked(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        dbLoginInfo = DataBaseLoginInfo()

        try:
            authenticateUser(username, password, dbLoginInfo)
        except Exception as error:
            print(repr(error))
            return False

        dbLoginInfo.userID = 'test_user'
        dbLoginInfo.password = 'testPassword'
        dbLoginInfo.ipaddress = '173.230.136.241'
        dbLoginInfo.defaultDB = 'test'


        print('Successful login')
        self.destroy()
        return True


class masterView(Tk):
    def __init__(self):
        self.frames = {}

        Tk.__init__(self)
        self.container = Frame(self)

        self.container.pack(side = "top", fill = "both", expand = True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)


        loginFrame = LoginDialog(self.container, self)

        self.add_frame(loginFrame, LoginDialog)

        self.show_frame(LoginDialog)

        self.title("Scrumbles")
        self.geometry("800x600")
        self.iconbitmap("logo.ico")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def add_frame(self, addedFrame, addedFrameClass):
        self.frames[addedFrameClass] = addedFrame
        addedFrame.grid(row = 0, column = 0, sticky = "nsew")


class mainView(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text = "Time to Scrumble: Main View", font = ("Verdana", 12))
        label.grid(row = 0, column = 0, sticky = "nsew")

app = masterView()
app.mainloop()