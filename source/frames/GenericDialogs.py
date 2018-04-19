import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
from MySQLdb import IntegrityError
from views import masterView
import webbrowser
from data import DataBlock
import sys, traceback
import logging
from frames.SLists import ColorSchemes
from data import ScrumblesObjects



def tryExcept(f):
    def wrapper(self):
        try:

            f(self)

        except IntegrityError as e:
            logging.exception('Invalid Input')
            if 'UserName' in str(e):
                messagebox.showerror('Error', 'Username already in use')
            elif "EmailAddress" in str(e):
                messagebox.showerror('Error', "Email address already in use")
            elif 'SprintName' in str(e):
                messagebox.showerror('Error', 'Sprint Must have unique Name')
            else:
                messagebox.showerror('Error', str(type(e)) + '\n' + str(e))
                self.executeSuccess = False
                self.exit()


        except Exception as e:

            messagebox.showerror('Error', str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack(file=sys.stdout)
            self.executeSuccess = False
            self.exit()
    return wrapper

class GenericDialog(Tk.Toplevel):
    def __init__(self,*args, **kwargs):
        """ Defines A Generic PopUp Dialog
        First Param required to be root window
        master=MasterView
        dataBlock=DataBlock
        """

        self.isTest = False
        self.isTest = kwargs.pop('test', None)
        if self.isTest is not None and self.isTest:
            removeKey = kwargs.pop('dataBlock', None)
            removeKey = kwargs.pop('master', None)
        self.dataBlock = kwargs.pop('dataBlock',None)
        if self.dataBlock is not None:
            assert type(self.dataBlock) is DataBlock.DataBlock, 'Key: dataBlock must be a DataBlock object'
        self.master = kwargs.pop('master', None)
        if self.master is not None:
            assert type(self.master) is masterView.masterView, 'Key: master must be the Scrumbles masterView'

        Tk.Toplevel.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.top = self
        self.transient()
        self.grab_set()
        self.executeSuccess = True


    def createWidgets(self):
        pass
    def exit(self):
        self.top.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.executeSuccess

    def validateName(self,objName):
        isGood = True
        for title in [I.itemTitle for I in self.dataBlock.items]:
            if objName == title:
                isGood = False
        for name in [U.userName for U in self.dataBlock.users]:
            if objName == name:
                isGood = False
        for name in [P.projectName for P in self.dataBlock.projects]:
            if objName == name:
                isGood = False
        for name in [S.sprintName for S in self.dataBlock.sprints]:
            if objName == name:
                isGood = False
        if not isGood:
            raise Exception('Object Name Must Be Unique')


class AboutDialog(GenericDialog):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.apiLink = 'https://github.com/CEN3031-group16/GroupProject/wiki'

        if not self.isTest:
            w = 600*self.master.w_rat
            h = 600*self.master.h_rat
            ws = self.parent.winfo_screenwidth()  # width of the screen
            hs = self.parent.winfo_screenheight()  # height of the screen
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.title('About Scrumbles')
        self.createWidgets()

    def createWidgets(self):
        Tk.Label(self, text="Scrumbles is an application designed to help you manage programming projects and teams efficiently").grid(row=1, pady=5, sticky='E')
        linkLabel = Tk.Label(self, text=self.apiLink,fg='blue',cursor='gumby')
        linkLabel.grid(row=2,pady=5)
        linkLabel.bind('<Button-1>',self.openPage)

        itemList = [ 'Not Assigned To Anything', 'Assigned to Sprint, no User', 'Assigned to User, No Sprint', 'Assigned to User and Sprint', 'In Progress', 'Submitted','Item Is Epic' ,'Complete']
        listBoxWidth=0
        self.itemListBox = Tk.Listbox(self, selectborderwidth=10)
        self.itemListBox.grid(row=3)
        for item in itemList:
            self.itemListBox.insert(Tk.END,item)
            if len(item) > listBoxWidth:
                listBoxWidth = len(item)

        self.itemListBox['width'] = listBoxWidth
        self.itemListBox['activestyle'] = 'dotbox'
        self.itemListBox['height'] = len(itemList)


        self.itemListBox.itemconfig(0, ColorSchemes.incompleteAssignmentColorScheme) # Not Assigned To Anything
        self.itemListBox.itemconfig(1, ColorSchemes.incompleteAssignmentColorScheme) #Assigned to Sprint, no User
        self.itemListBox.itemconfig(2, ColorSchemes.incompleteAssignmentColorScheme) #Assigned to User, No Sprint
        self.itemListBox.itemconfig(3, ColorSchemes.assignedScheme) # Assigned to User and Sprint
        self.itemListBox.itemconfig(4, ColorSchemes.inProgressColorScheme) # In Progress
        self.itemListBox.itemconfig(5, ColorSchemes.submittedColorScheme) # Submitted
        self.itemListBox.itemconfig(6, ColorSchemes.epicItemColorScheme) # Item Is Epic
        self.itemListBox.itemconfig(7, ColorSchemes.completedItemColorScheme) # Completed



        okayButton = Tk.Button(self, text="Okay", command=self.exit, cursor = "hand2")
        okayButton.grid(row=20, pady=5)

    def openPage(self, *args, **kwargs):
        webbrowser.open(self.apiLink)

    def exit(self):
        self.top.destroy()


class codeLinkDialog(GenericDialog):
    def __init__(self,*args,**kwargs):
        self.Item = kwargs.pop('item')

        super().__init__(*args,**kwargs)

        self.protocol('WM_DELETE_WINDOW', lambda: self.cancel())
        if not self.isTest:
            # w = 600*self.master.w_rat
            # h = 80*self.master.h_rat
            # ws = self.parent.winfo_screenwidth()  # width of the screen
            # hs = self.parent.winfo_screenheight()  # height of the screen
            # x = (ws / 2) - (w / 2)
            # y = (hs / 2) - (h / 2)
            # self.geometry('%dx%d+%d+%d'%(w,h,x,y))
            pass
        self.createWidgets()
    @tryExcept
    def createWidgets(self):
        self.title('Edit %s' % self.Item.itemTitle)
        self.codeLinkLabel = ttk.Label(self,text='Please enter link to Code')
        self.codeLinkLabel.grid(row=1,column=1)
        self.codeLinkEntry = Tk.Entry(self,width=60)
        self.codeLinkEntry.grid(row=2,column=1,sticky='W')
        if self.Item.itemCodeLink is not None:
            self.codeLinkEntry.insert(0,self.Item.itemCodeLink)
        self.submitButton = Tk.Button(self, text="Update Item", command=self.ok, cursor = "hand2")
        self.submitButton.grid(row=2, column=2, padx=3)
        self.cancelButton = Tk.Button(self,text='Cancel',command=self.cancel, cursor = "hand2")
        self.cancelButton.grid(row=2,column=3,pady=1)
    @tryExcept
    def ok(self):
        self.executeSuccess = True
        oldItem = self.Item
        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'modify code link'
        comment.commentItemID = self.Item.itemID
        comment.commentUserID = 0

        self.Item.itemCodeLink = self.codeLinkEntry.get()
        if not self.isTest:
            self.dataBlock.updateScrumblesObject(self.Item, oldItem, comment)

        self.exit()

    def exit(self):
        self.top.destroy()

    def cancel(self):
        self.executeSuccess = False
        self.exit()
