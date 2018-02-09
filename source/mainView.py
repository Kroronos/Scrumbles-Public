from ScrumblesData import *
from tkinter import *


def authenticateUser(username,password,dbLoginInfo):
    userID = None
    dataConnection = ScrumblesData(dbLoginInfo)
    dataConnection.connect()
    result = dataConnection.getData(Query.getUserIdByUsernameAndPassword(username,password))
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
    def __init__(self, master):
        super().__init__(master)

        self.usernameLabel = Label(self, text="Username")
        self.passwordLabel = Label(self, text="Password")
        self.usernameEntry = Entry(self)
        self.passwordEntry = Entry(self,show='*')

        self.usernameLabel.grid(row=0,sticky=E)
        self.passwordLabel.grid(row=1,sticky=E)
        self.usernameEntry.grid(row=0,column=1)
        self.passwordEntry.grid(row=1,column=1)

        self.loginButton = Button(self, text='Login', command=self.loginButtonClicked)
        self.loginButton.grid(columnspan=2)

        self.pack()
        
    def loginButtonClicked(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        dbLoginInfo = DataBaseLoginInfo()
        dbLoginInfo.userID = 'test_user'
        dbLoginInfo.password = 'testPassword'
        dbLoginInfo.ipaddress = '173.230.136.241'
        dbLoginInfo.defaultDB = 'test'
        try:
            authenticateUser(username,password,dbLoginInfo)
        except Exception as error:
            print(repr(error))
            return False

        print('Successful login')
        self.master.destroy()
        return True
        

mainView = Tk()
authenticateView = Toplevel()
loginDiaglog = LoginDialog(authenticateView)

mainView.title("Scrumbles says: Hello World!")
mainView.geometry('800x600')
mainView.iconbitmap('logo.ico')



mainViewMenu = Menu(mainView)  #Create a menu 
mainView.config(menu=mainViewMenu) #attach menu to root

windowMenu = Menu(mainViewMenu)  #Create a menu item attached to mainViewMenu
mainViewMenu.add_cascade(label="Window", menu=windowMenu)

windowMenu.add_command(label="Sprint View",command=viewSprintWindow)
windowMenu.add_command(label="Backlog View", command=viewBacklogWindow)
windowMenu.add_command(label="User Manger View", command=viewUserWindow)

mainView.mainloop()
