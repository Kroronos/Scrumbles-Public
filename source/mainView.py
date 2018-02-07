from tkinter import *

def viewSprintWindow():
    print("View Sprint Called")

def viewBacklogWindow():
    print("View Backlog Called")

def viewUserWindow():
    print("View user called")

mainView = Tk()
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

mainloop()
