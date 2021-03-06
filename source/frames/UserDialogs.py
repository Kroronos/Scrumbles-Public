# import tkinter as Tk
# from tkinter import ttk, messagebox
# import logging
from data import ScrumblesObjects
from frames.GenericDialogs import *

class CreateUserDialog(GenericDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        if not self.isTest:
            self.geometry('%dx%d'%(300, 200))
        self.title('Create a New User')
        self.createWidgets()

    @tryExcept
    def createWidgets(self):

        Tk.Label(self, text="User Name").grid(row=2, column=1, padx=5, pady=5, sticky='W')
        self.userNameEntry = Tk.Entry(self, width=27, cursor = "hand2")
        self.userNameEntry.grid(row=2, column=2, pady=5, sticky='W')

        Tk.Label(self, text="User Password").grid(row=3, column=1, padx=5, pady=5, sticky='W')
        self.passwordEntry = Tk.Entry(self, width=27, show='*', cursor = "hand2")
        self.passwordEntry.grid(row=3, column=2, pady=5, sticky='W')

        Tk.Label(self, text="Re-enter Password").grid(row=4, column=1, padx=5, pady=5, sticky='W')
        self.reEnterPasswordEntry = Tk.Entry(self, width=27, show='*', cursor = "hand2")
        self.reEnterPasswordEntry.grid(row=4, column=2, pady=5, sticky='W')

        Tk.Label(self, text="User Email Address").grid(row=5, column=1, padx=5, pady=5, sticky='W')
        self.emailEntry =Tk.Entry(self, width=27, cursor = "hand2")
        self.emailEntry.grid(row=5, column=2, pady=5, sticky='W')

        Tk.Label(self, text="User Role").grid(row=6, column=1, padx=5, pady=5, sticky='W')
        roleVar = Tk.StringVar()
        items = ('Admin', 'Scrum Master', 'Developer')
        self.roleCombobox = ttk.Combobox(self, textvariable=roleVar, state='readonly', values=items, width=24, cursor="hand2")
        self.roleCombobox.grid(row=6, column=2, sticky='W')
        self.roleCombobox.selection_clear()

        self.createButton = Tk.Button(self, text="Create User", command=self.ok, cursor="hand2")
        self.createButton.grid(row=8, column=1, columnspan=2, padx=70, pady=10, sticky='W')

        self.cancelButton = Tk.Button(self, text="Cancel", command=self.exit, cursor="hand2")
        self.cancelButton.grid(row=8, column=2, columnspan=2, padx=70, pady=10, sticky='W')


    @staticmethod
    def validatePasswordMatch(password1, password2):
        if password1 != password2:
            raise Exception('Passwords do not Match')
        return

    @tryExcept
    def ok(self):

        self.validatePasswordMatch(self.passwordEntry.get(), self.reEnterPasswordEntry.get())

        user = ScrumblesObjects.User()
        user.userName = self.userNameEntry.get()
        user.userPassword = self.passwordEntry.get()
        user.userEmailAddress = self.emailEntry.get()
        user.userRole = self.roleCombobox.get()
        self.validateName(user.userName)
        try:
            if not self.isTest:
                self.dataBlock.addNewScrumblesObject(user)
        except IntegrityError:
            logging.exception('ID Collision')
            user.userID = ScrumblesObjects.generateRowID()
            self.dataBlock.addNewScrumblesObject(user)
        else:
            messagebox.showinfo('Info', 'New User Successfully Created')
            self.exit()
