# import tkinter as Tk
# from tkinter import ttk, messagebox
# import logging
from data import ScrumblesObjects
from frames.GenericDialogs import *

class CreateSprintDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprint = None
        self.oldSprintName = None
        self.month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Nov','Dec']
        self.day = [str(d) for d in range(1,32)]
        self.year = [str(y) for y in range(2018,2100)]
        if not self.isTest:
            self.geometry('%dx%d'%(900*self.master.w_rat, 500*self.master.h_rat))
            self.projects = tuple([P.projectName for P in self.dataBlock.projects])
            self.projectIDmap = {}
            for P in self.dataBlock.projects:
                self.projectIDmap[P.projectID] = P.projectName
        self.title('Create a New Sprint')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):

        monthVar = Tk.StringVar()
        monthVar = 'Jan'

        Tk.Label(self, text="Sprint Name").grid(row=2, column=1, pady=5, sticky='E')
        self.sprintNameEntry = Tk.Entry(self, cursor = "hand2")
        self.sprintNameEntry.grid(row=2, column=2, pady=5)
        self.projectNameVar = Tk.StringVar()

        if not self.isTest:
            Tk.Label(self, text="Project").grid(row=3, column=1, pady=5, sticky='E')
            self.assignSprintToObject = ttk.Combobox(self,textvariable=self.projectNameVar,state='readonly',values=self.projects, cursor = "hand2")
            self.assignSprintToObject.grid(row=3,column=2,pady=5)

        Tk.Label(self, text="Start Date").grid(row=4, column=1, pady=5, sticky='E')
        self.StartMonthCombo = ttk.Combobox(self,textvariable=monthVar,values=self.month,state='readonly',width=5, cursor = "hand2")
        self.StartMonthCombo.grid(row=4,column=2)

        self.StartDayCombo = ttk.Combobox(self,values=self.day,state='readonly',width=3, cursor = "hand2")
        self.StartDayCombo.grid(row=4,column=3)

        self.StartYearCombo = ttk.Combobox(self,values=self.year,state='readonly',width=5, cursor = "hand2")
        self.StartYearCombo.grid(row=4,column=4)

        Tk.Label(self, text="Due Date").grid(row=5, column=1, pady=5, sticky='E')
        self.DueMonthCombo = ttk.Combobox(self, values=self.month, state='readonly',width=5, cursor = "hand2")
        self.DueMonthCombo.grid(row=5, column=2)

        self.DueDayCombo = ttk.Combobox(self, values=self.day, state='readonly',width=3, cursor = "hand2")
        self.DueDayCombo.grid(row=5, column=3)

        self.DueYearCombo = ttk.Combobox(self, values=self.year, state='readonly',width=5, cursor = "hand2")
        self.DueYearCombo.grid(row=5, column=4)

        self.createButton = Tk.Button(self, text="Create Sprint", command=self.ok, cursor = "hand2")
        self.createButton.grid(row=8,column=2,pady=5)

        self.cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor = "hand2")
        self.cancelButton.grid(row=8,column=1,pady=5)

    @staticmethod
    def getStartDate(dateblock):

        if dateblock.month == '' or dateblock.day == '' or dateblock.year == '':
            dateString = 'Jan 1 2100 5:00PM'
        else:
            dateString = dateblock.month+" "+dateblock.day+" "+dateblock.year+" 5:00PM"
        return datetime.datetime.strptime(dateString,'%b %d %Y %I:%M%p')
    @staticmethod
    def getDueDate(dateblock):

        if dateblock.month == '' or dateblock.day == '' or dateblock.year == '':
            dateString = 'Jan 1 2100 5:00PM'
        else:
            dateString = dateblock.month+" "+dateblock.day+" "+dateblock.year+" 5:00PM"
        return datetime.datetime.strptime(dateString,'%b %d %Y %I:%M%p')

    def getDate(self,type):

        class dateblock:
            def __init__(self):
                self.month = None
                self.day = None
                self.year = None

        if type == 'start':
            dateblock.month = self.StartMonthCombo.get()
            dateblock.day = self.StartDayCombo.get()
            dateblock.year = self.StartYearCombo.get()
            date = self.getStartDate(dateblock)
        elif type == 'due':
            dateblock.month = self.DueMonthCombo.get()
            dateblock.day = self.DueDayCombo.get()
            dateblock.year = self.DueYearCombo.get()
            date = self.getDueDate(dateblock)
        else:
            raise Exception("getDate parameter must be 'start' or 'due' ")
        return date

    @tryExcept
    def ok(self):
        if self.sprint is None:
            sprint = ScrumblesObjects.Sprint()
        else:
            sprint = self.sprint


        sprint.sprintName = self.sprintNameEntry.get()
        sprint.sprintStartDate = self.getDate('start')
        sprint.sprintDueDate = self.getDate('due')

        if self.oldSprintName is None or self.oldSprintName != sprint.sprintName:
            self.validateName(sprint.sprintName)

        if not self.isTest:
            projectName = self.assignSprintToObject.get()
            for P in self.dataBlock.projects:
                if P.projectName == projectName:
                    sprint.projectID = P.projectID

        if not self.isTest:
            self.writeData(sprint)

        self.exit()

    def writeData(self,obj):
        try:
            self.dataBlock.addNewScrumblesObject(obj)
        except IntegrityError:
            logging.exception('ID Collision')
            obj.sprintID = ScrumblesObjects.generateRowID()
            self.dataBlock.addNewScrumblesObject(obj)
        else:
            messagebox.showinfo('Info', 'New Sprint Successfully Created')


class EditSprintDialog(CreateSprintDialog):
    def __init__(self, *args, **kwargs):
        sprint = kwargs.pop('sprint',None)
        assert type(sprint) == ScrumblesObjects.Sprint, 'keyword sprint must be a ScrumblesObject.Sprint'
        super().__init__(*args, **kwargs)
        self.sprint = sprint
        self.updateWidgets()
        self.title('Modify Sprint')
        self.protocol('WM_DELETE_WINDOW', lambda: self.cancel())
    def updateWidgets(self):
        self.sprintNameEntry.insert(0,self.sprint.sprintName)
        if not self.isTest:
            self.assignSprintToObject.set(self.projectIDmap[self.sprint.projectID])
            self.assignSprintToObject['state'] = 'disabled'
        self.StartDayCombo.set(self.sprint.sprintStartDate.strftime('%d'))
        self.StartMonthCombo.set(self.sprint.sprintStartDate.strftime('%b'))
        self.StartYearCombo.set(self.sprint.sprintStartDate.strftime('%Y'))
        self.DueDayCombo.set(self.sprint.sprintDueDate.strftime('%d'))
        self.DueMonthCombo.set(self.sprint.sprintDueDate.strftime('%b'))
        self.DueYearCombo.set(self.sprint.sprintDueDate.strftime('%Y'))
        self.createButton['text'] = 'Update'
        self.cancelButton['command'] = self.cancel

    def writeData(self,obj):
        self.dataBlock.updateScrumblesObject(obj)
    def cancel(self):
        self.executeSuccess = False
        self.exit()


class DeleteSprintDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        sprint = kwargs.pop('sprint',None)
        assert type(sprint) == ScrumblesObjects.Sprint, 'keyword sprint must be a ScrumblesObject.Sprint'
        super().__init__(*args, **kwargs)
        self.sprint = sprint
        self.title('Delete Sprint')
        self.createWidgets()
        self.protocol('WM_DELETE_WINDOW', lambda: self.cancel())



    @tryExcept
    def ok(self):
        try:
            if not self.isTest:
                self.dataBlock.deleteScrumblesObject(self.sprint)
                self.exit()
            else:
                print('TESTMODE: self.dataBlock.deleteScrumblesObject(%s)'%repr(self.sprint))
        except IntegrityError:
            logging.exception('ID Collision')

        else:
            messagebox.showinfo('Info', 'Sprint Successfully Deleted')



    def cancel(self):
        self.executeSuccess = False
        self.exit()

    def createWidgets(self):
        Tk.Label(self, text="Delete "+ self.sprint.sprintName + "?").grid(row=2, column=1, pady=5, sticky='E')


        self.deleteButton = Tk.Button(self, text="Delete", command=self.ok)
        self.deleteButton.grid(row=8,column=2,pady=5)

        self.cancelButton = Tk.Button(self, text="Cancel", command=self.cancel)
        self.cancelButton.grid(row=8,column=1,pady=5)