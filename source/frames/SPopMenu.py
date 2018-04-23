import tkinter as Tk
from tkinter import messagebox
import logging

class GenericPopupMenu(Tk.Menu):
    def __init__(self,root,Master):
        Tk.Menu.__init__(self)
        self.config(tearoff=0)
        self.root = root
        self.dataBlock = Master.dataBlock
        self.master = Master
        self.widget = None
        self.event = None
        try:
            self.selectedObject = root.selectedItem
        except:
            self.selectedObject = None



    def context_menu(self, event, menu):
        self.widget = event.widget
        self.event = event
        index = self.widget.nearest(event.y)
        try:
            _, yoffset, _, height = self.widget.bbox(index)
        except TypeError:
            return
        if event.y > height + yoffset + 5:
            return
        self.selectedObject = self.widget.get(index)
        try:
            self.root.selectedItem = self.selectedObject
        except:
            pass
        self.widget.selection_clear(0, Tk.END)
        self.widget.selection_set(index)
        self.widget.activate(index)
        menu.post(event.x_root, event.y_root)

    def getSelectedObject(self):
        if self.selectedObject is None:
            raise Exception('PopMenu Selected Item is None')
        else:
            obj = self.findSelectedObject(self.selectedObject)
            return obj

    def findSelectedObject(self,name):
        for I in self.dataBlock.items:
            if name == I.itemTitle:
                return I
        for U in self.dataBlock.users:
            if name == U.userName:
                return U
        for P in self.dataBlock.projects:
            if name == P.projectName:
                return P
        for S in self.dataBlock.sprints:
            if name == S.sprintName:
                return S



class BacklogManPopMenu(GenericPopupMenu):
    def __init__(self,root,Master,epicList=None):
        GenericPopupMenu.__init__(self,root,Master)

        self.add_command(label=u'Promote To Epic', command=self.promoteItemToEpic)
        try:
            self.selectedItem = root.selectedItem
        except:
            self.selectedItem = self.selectedObject
        self.hasEpics = False

        if epicList is not None:
            self.hasEpics = True
            self.setEpicsMenu()
        self.listOfEpics = epicList


    def promoteItemToEpic(self):
        item = self.getSelectedObject()

        if item is None:
            raise Exception('Error Loading item from title')

        self.dataBlock.promoteItemToEpic(item)

    def updateEpicsMenu(self):
        if self.hasEpics:
            self.setEpicsMenu()

    def setEpicsMenu(self):

        listOfEpics = [E.itemTitle for E in self.root.listOfEpics]

        try:
            self.delete('Assign To Epic')
        except Exception:
            pass

        self.popMenu = Tk.Menu(self, tearoff=0, cursor = "hand2")
        for text in listOfEpics:
            self.popMenu.add_command(label=text, command=lambda t=text: self.assignItemToEpic(t))

        self.add_cascade(label='Assign To Epic', menu=self.popMenu, underline=0)

    def assignItemToEpic(self, epicName):

        epic = None
        item = self.getSelectedObject()
        for I in self.master.activeProject.listOfAssignedItems:
            if I.itemTitle == epicName:
                epic = I


        try:
            if self.isItemAlreadyInAnEpic(item):
                self.dataBlock.reAssignItemToEpic(item, epic)
                messagebox.showinfo('Success', 'Re-Assigned %s to %s' % (item.itemTitle, epic.itemTitle))
            else:
                self.dataBlock.addItemToEpic(item, epic)

                messagebox.showinfo('Success', 'Assigned %s to %s'%(item.itemTitle,epic.itemTitle))
        except Exception as e:
            logging.exception('Error assigning item: "%s" to Epic: "%s"'%(str(item),str(epic)))
            messagebox.showerror('Error', str(e)+"Error logged to Scrumbles.log")

    def isItemAlreadyInAnEpic(self, item):
        listOfItemsInAnEpic = []
        for I in self.dataBlock.items:
            if I.itemType == 'Epic':

                for subItem in I.subItemList:
                    listOfItemsInAnEpic.append(subItem)
        return item in listOfItemsInAnEpic
