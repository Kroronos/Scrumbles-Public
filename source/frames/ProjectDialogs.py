# import tkinter as Tk
# from tkinter import ttk, messagebox
# import logging
from data import ScrumblesObjects
from frames.GenericDialogs import *


class CreateProjectDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        if not self.isTest:
            self.geometry('%dx%d'%(230*self.master.w_rat, 50*self.master.h_rat))

        self.title('Create a New Project')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):
        Tk.Label(self, text="Project Title").grid(row=2, column=1, pady=5, sticky='W')

        self.projectTitleEntry = Tk.Entry(self, width=43)
        self.projectTitleEntry.grid(row=2, column=2, columnspan = 2, pady=5, sticky='W')

        self.createButton = Tk.Button(self, text="Create Project", command=self.ok, cursor="hand2")
        self.createButton.grid(row=8, column=2, columnspan=2, padx=20, pady=5, sticky='W')
        self.cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor="hand2")
        self.cancelButton.grid(row=8, column=3, columnspan=2, padx=20, pady=5, sticky='W')


    @tryExcept
    def ok(self):
        project = ScrumblesObjects.Project()
        project.projectName = self.projectTitleEntry.get()
        self.validateName(project.projectName)
        try:
            if not self.isTest:
                self.dataBlock.addNewScrumblesObject(project)
            else:
                print('TESTMODE: self.dataBlock.addNewScrumblesObject(%s)'%repr(project))
        except IntegrityError:
            logging.exception('ID Collision')
            project.projectID = ScrumblesObjects.generateRowID()
            self.dataBlock.addNewScrumblesObject(project)
        else:
            messagebox.showinfo('Info', 'New Item Successfully Created')
            self.exit()
