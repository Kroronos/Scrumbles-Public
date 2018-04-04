import tkinter as Tk
from tkinter import messagebox

class GenericPopupMenu(Tk.Menu):
    def __init__(self,root,Master):
        Tk.Menu.__init__(self)
        self.config(tearoff=0)
        self.root = root
        self.dataBlock = Master.dataBlock
        self.master = Master
        self.widget = None
        try:
            self.selectedItem = root.selectedItem
        except:
            self.selectedItem = None

    def context_menu(self, event, menu):
        self.widget = event.widget
        index = self.widget.nearest(event.y)
        _, yoffset, _, height = self.widget.bbox(index)
        if event.y > height + yoffset + 5:
            return
        self.selectedItem = self.widget.get(index)
        try:
            self.root.selectedItem = self.selectedItem
        except:
            pass
        self.widget.selection_clear(0, Tk.END)
        self.widget.selection_set(index)
        menu.post(event.x_root, event.y_root)



class DevHomePopMenu(GenericPopupMenu):
    def __init__(self,root,Master,epicList=None):
        GenericPopupMenu.__init__(self,root,Master)

        self.add_command(label=u'Promote To Epic', command=self.promoteItemToEpic)
        try:
            self.selectedItem = root.selectedItem
        except:
            self.selectedItem = None
        self.hasEpics = False

        if epicList is not None:
            self.hasEpics = True
            self.setEpicsMenu()
        self.listOfEpics = epicList


    def promoteItemToEpic(self):
        item = None
        title = self.selectedItem
        for i in self.dataBlock.items:
            if i.itemTitle == title:
                item = i

        if item is None:
            print('Item Title:', title)
            print('backlogData:')
            for i in self.root.activeProject.listOfAssignedItems:
                print(i.itemTitle)
            raise Exception('Error Loading item from title')

        self.dataBlock.promoteItemToEpic(item)

    def updateEpicsMenu(self):
        if self.hasEpics:
            self.setEpicsMenu()

    def setEpicsMenu(self):

        listOfEpics = [E.itemTitle for E in self.root.listOfEpics]
        print(listOfEpics)
        try:
            self.delete('Assign To Epic')
        except Exception:
            pass

        self.popMenu = Tk.Menu(self, tearoff=0)
        for text in listOfEpics:
            self.popMenu.add_command(label=text, command=lambda t=text: self.assignItemToEpic(t))

        self.add_cascade(label='Assign To Epic', menu=self.popMenu, underline=0)

    def assignItemToEpic(self, epicName):

        epic = None
        item = None
        for I in self.master.activeProject.listOfAssignedItems:
            if I.itemTitle == epicName:
                epic = I
            if I.itemTitle == self.selectedItem:
                item = I

        try:
            if self.isItemAlreadyInAnEpic(item):
                self.dataBlock.reAssignItemToEpic(item, epic)
            else:
                self.dataBlock.addItemToEpic(item, epic)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def isItemAlreadyInAnEpic(self, item):
        listOfItemsInAnEpic = []
        for I in self.dataBlock.items:
            if I.itemType == 'Epic':
                for subItem in I.subItemList:
                    listOfItemsInAnEpic.append(subItem)
        return item in listOfItemsInAnEpic