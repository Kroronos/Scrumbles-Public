import tkinter as tk
from data import DataBlock

root = tk.Tk()

userListBox = tk.Listbox(root)
sprintListBox = tk.Listbox(root)
itemListBox = tk.Listbox(root)
projectListBox = tk.Listbox(root)
commentListBox = tk.Listbox(root)

userNames = []
itemNames = []
sprintNames = []
projectNames = []
comments = []


def updateUserList():
    print('update User List')
    userNames.clear()
    userListBox.delete(0,tk.END)
    for user in dataBlock.users:
        userNames.append(user.userName)
    for user in userNames:
        userListBox.insert(tk.END, user)

def updateItemList():
    print('update Item List')
    itemNames.clear()
    itemListBox.delete(0,tk.END)
    for item in dataBlock.items:
        itemNames.append(item.itemTitle)
    for Item in itemNames:
        itemListBox.insert(tk.END, Item)




dataBlock = DataBlock.DataBlock()
dataBlock.packCallback(updateUserList)
dataBlock.packCallback(updateItemList)








updateUserList()
updateItemList()

userListBox.pack()
itemListBox.pack()

root.mainloop()

dataBlock.shutdown()
dataBlock.listener.stop()








