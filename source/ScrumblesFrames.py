import tkinter as tk


import matplotlib
matplotlib.use("TKAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import csv
import tkcalendar
import datetime

from styling import styling as style
from tkinter import ttk

class BaseList(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)
        self.fullList = []

    def showPartialList(self, list):
        self.clearList()
        for item in list:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def showFullList(self):
        self.clearList()
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()


    def importList(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()


    def importItemList(self, items):
        self.deleteList()
        listofnames = []
        for item in items:
            listofnames.append(item.itemTitle)
        self.fullList = listofnames
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importProjectList(self, projects):
        self.deleteList()
        listOfnames = []
        for project in projects:
            listOfnames.append(project.projectName)
        self.fullList = listOfnames
        for item in self.fullList:
            self.listbox.insert(tk.END, item)
        self.enforceSort()



    def importListSorted(self, list):
        self.deleteList()
        self.fullList = list
        for item in self.fullList:
            self.listbox.insert(tk.END, item)

    def appendList(self, list):
        for item in list:
            self.fullList.append(item)
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def addItem(self, item):
        self.fullList.append(item)
        self.listbox.insert(tk.END, item)
        self.enforceSort()

    def sortForward(self):
        items = self.listbox.get(0, tk.END)
        items = sorted(items)
        self.fullList = sorted(self.fullList)
        self.importListSorted(items)

    def sortReverse(self):
        items = self.listbox.get(0, tk.END)
        items = sorted(items, reverse=True)
        self.fullList = sorted(self.fullList, reverse=True)
        self.importListSorted(items)

    def clearList(self):
        self.listbox.delete(0, tk.END)

    def deleteList(self):
        self.listbox.delete(0, tk.END)
        self.fullList = []

    def deleteSelectedItem(self):

        deleteIndex = self.listbox.get(0, tk.END).index(tk.ANCHOR)
        del self.fullList[deleteIndex]
        self.listbox.delete(tk.ANCHOR)
        self.enforceSorting()

    def decideSort(self):
        if self.typeSort == "none":
           self.typeSort = "forward"
           self.sortButton["text"] = style.up_arrow
           self.sortForward()
        elif self.typeSort == "forward":
            self.typeSort = "reverse"
            self.sortButton["text"] = style.down_arrow
            self.sortReverse()
        else:
            self.typeSort = "forward"
            self.sortButton["text"] = style.up_arrow
            self.sortForward()

    def enforceSort(self):
        if self.typeSort == "none":
            return
        elif self.typeSort == "forward":
            self.sortForward()
        else:
            self.sortReverse()

    def search(self, str):
        def fulfillsCondition(item,str):
            return item[:len(str)] == str
        
        matches = [x for x in self.fullList if fulfillsCondition(x, str)]
        self.showPartialList(matches)
        


class SComboList(BaseList):
    def __init__(self, controller, title, products):
        tk.Frame.__init__(self, controller)

        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self, textvariable=self.box_value)
        self.box['values'] = (products)
        self.box.current(0)
        self.box.pack(fill = tk.X)

        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listFrame.pack(fill=tk.BOTH, expand=True)

class SBacklogList(BaseList):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self, bg=style.scrumbles_blue, relief=tk.SOLID, borderwidth=1)
        self.searchFrame = tk.Frame(self.titleFrame, relief=tk.SOLID, bg=style.scrumbles_blue)

        self.searchLabel = tk.Label(self.searchFrame, text="Search:", bg=style.scrumbles_blue)
        self.searchEntry = tk.Entry(self.searchFrame)
        self.searchButton = tk.Button(self.searchFrame, text=style.right_enter_arrow, bg=style.scrumbles_blue, command=lambda: self.search(self.searchEntry.get()), relief=tk.FLAT)
        self.undoSearchButton = tk.Button(self.searchFrame, text=style.cancel_button, bg=style.scrumbles_blue, command=lambda: self.showFullList(), relief=tk.FLAT)

        self.searchEntry.bind('<Return>', lambda event: self.search(self.searchEntry.get()))
        self.undoSearchButton.pack(side = tk.RIGHT)
        self.searchButton.pack(side = tk.RIGHT)
        self.searchEntry.pack(side = tk.RIGHT)
        self.searchLabel.pack(side = tk.RIGHT)
       

        self.titleLabel = tk.Label(self.titleFrame, text="Backlog", bg=style.scrumbles_blue, relief=tk.FLAT)
        self.sortButton = tk.Button(self.titleFrame, text=style.updown_arrow, bg=style.scrumbles_blue, command=lambda: self.decideSort(), relief=tk.FLAT)
    
        self.titleLabel.pack(side = tk.LEFT)
        self.sortButton.pack(side = tk.RIGHT)
        self.searchFrame.pack(side = tk.RIGHT)
    
        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, width = 80, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"
        self.titleFrame.pack(fill=tk.X, expand=False)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listFrame.pack(fill=tk.BOTH, expand=True)

class SList(BaseList):
    def __init__(self, controller, title):
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self, bg=style.scrumbles_blue, relief=tk.SOLID, borderwidth=1)
        self.titleLabel = tk.Label(self.titleFrame, text=title, bg=style.scrumbles_blue, relief=tk.FLAT)
        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        self.typeSort = "none"

        self.sortButton = tk.Button(self.titleFrame, text=style.updown_arrow, bg=style.scrumbles_blue, command=lambda: self.decideSort(), relief=tk.FLAT)
        self.titleLabel.pack(side=tk.LEFT)
        self.sortButton.pack(side=tk.RIGHT)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.titleFrame.pack(fill=tk.X, expand=False)
        self.listFrame.pack(fill=tk.BOTH, expand=True)


class SLineGraph(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)

        self.x = [1,2,3,4,5,6,7,8,9,10]
        self.y = [1,4,2,5,1,4,2,5,1,4]
        self.label = None

        self.figure = Figure(figsize=(4, 4), dpi=100)
        self.graph = self.figure.add_subplot(1,1,1)


    def setTitle(self, title):
        self.label = tk.Label(self, text=title)

    def setAxes(self, xAxis, yAxis):
        self.graph.set_xlabel(xAxis)
        self.graph.set_ylabel(yAxis)
        self.figure.subplots_adjust(left=.15)
        self.figure.subplots_adjust(bottom=.15)

    def importDataFromCSV(self, fileName, delimeter):
        with open(fileName, 'r') as file:
            plots = csv.reader(file, delimeter)
            for row in plots:
                self.x.append(int(row[0]))
                self.y.append(int(row[1]))

    def displayGraph(self):
        self.graph.plot(self.x, self.y)
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.show()
        if self.label is not None:
            self.label.pack(side=tk.TOP, fill=tk.X)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=1, pady=1)

    def changeBackgroundColor(self, color):
        self.graph.set_facecolor(facecolor=color)

class SCalendar(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller)
        now = datetime.datetime.now()
        self.cal = tkcalendar.Calendar(self, font="Arial 14", selectmode='day', year=now.year, month=now.month, day=now.day)
        self.cal.pack(side=tk.TOP, fill=tk.BOTH)

class itemPicker(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth=1)
       
        self.itemNumberLabel = tk.Label(self, text = "Item Number: ", justify = tk.LEFT).grid(row = 0)


        self.itemNameLabel = tk.Label(self, text = "Name: ", justify = tk.LEFT).grid(row = 1)
        self.itemNameEntry = tk.Entry(self).grid(row = 1, column = 1)

        self.itemDescriptionLabel =  tk.Label(self, text = "Description: ", justify = tk.LEFT).grid(row = 2)
        self.itemDescriptionEntry = tk.Entry(self).grid(row = 2, column = 1)


        self.itemWeightLabel = tk.Label( self, text = "Weight: ", justify = tk.LEFT, anchor = tk.W).grid(row = 3)
        #self.itemWeightSelector =
        # self.
        #self.itemWeightScroller = tk.Scrollbar 

        self.itemStatusLabel = tk.Label(self, text = "Status: ", justify = tk.LEFT).grid(row = 4)
        self.itemStatusFrame = tk.Frame(self)
        #self.item

    
    def selectItem(text):
        self.itemNumberLabel.text = text

class commentsField(tk.Frame):
    def __init__(self,controller):
        tk.Frame.__init__(self, controller, relief=tk.SOLID, borderwidth = 1)

        # self.commentTitle = tk.Label(self, text = "Comments")
        # self.commentTitle.pack(side = tk.TOP)

        # self.commentField = tk.Entry(self, width = 150)
        # self.commentField.pack(side = tk.BOTTOM, fill = tk.Y)

        self.commentTitle = tk.Label(self, text = "Comments").grid(row = 0)
        
        # self.commentField = Tk.Text(
        self.commentField = tk.Entry(self).grid(row = 1, rowspan = 20)


