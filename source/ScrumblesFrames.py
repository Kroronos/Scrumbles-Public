import tkinter as tk

class SList(tk.Frame):
    def __init__(self, controller, title):
        tk.Frame.__init__(self, controller)

        self.titleFrame = tk.Frame(self, bg="light steel blue", relief=tk.SOLID, borderwidth=1)
        self.titleLabel = tk.Label(self.titleFrame, text=title, bg="light steel blue", relief=tk.FLAT)
        self.listFrame = tk.Frame(self)
        self.listScrollbar = tk.Scrollbar(self.listFrame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(self.listFrame, selectmode=tk.BROWSE, yscrollcommand=self.listScrollbar.set)
        self.listScrollbar.config(command=self.listbox.yview)

        #define symbols, should ideally be done in styling file
        self.typeSort = "none"
        self.updown = u'\u2B0D'
        self.up = u'\u2B06'
        self.down = u'\u2B07'

        self.sortButton = tk.Button(self.titleFrame, text=self.updown, bg="light steel blue", command=lambda: self.decideSort(), relief=tk.FLAT)
        self.titleLabel.pack(side=tk.LEFT)
        self.sortButton.pack(side=tk.RIGHT)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.titleFrame.pack(fill=tk.X, expand=False)
        self.listFrame.pack(fill=tk.BOTH, expand=True)

    def importList(self, list):
        self.clearList()
        for item in list:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def importListSorted(self, list):
        self.clearList()
        for item in list:
            self.listbox.insert(tk.END, item)

    def appendList(self, list):
        for item in list:
            self.listbox.insert(tk.END, item)
        self.enforceSort()

    def addItem(self, item):
        self.listbox.insert(tk.END, item)
        self.enforceSort()

    def sortForward(self):
        items = self.listbox.get(0, tk.END)
        print(len(items))
        items = sorted(items)
        self.importListSorted(items)

    def sortReverse(self):
        items = self.listbox.get(0, tk.END)
        items = sorted(items, reverse=True)
        self.importListSorted(items)

    def clearList(self):
        self.listbox.delete(0, tk.END)

    def deleteSelectedItem(self):
        self.listbox.delete(tk.ANCHOR)
        self.enforceSorting()

    def decideSort(self):
        if self.typeSort == "none":
           self.typeSort = "forward"
           self.sortButton["text"] = self.up
           self.sortForward()
        elif self.typeSort == "forward":
            self.typeSort = "reverse"
            self.sortButton["text"] = self.down
            self.sortReverse()
        else:
            self.typeSort = "forward"
            self.sortButton["text"] = self.up
            self.sortForward()

    def enforceSort(self):
        if self.typeSort == "none":
            return
        elif self.typeSort == "forward":
            self.sortForward()
        else:
            self.sortReverse()