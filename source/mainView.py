import tkinter as tk
import tkcalendar
import ScrumblesData
import masterView

from tkinter import ttk
class mainView(tk.Frame):
    def __init__(self, parent, controller,user):
        tk.Frame.__init__(self, parent)




        self.ProductBacklogFrame = tk.Frame(self)
        self.CalendarFrame = tk.Frame(self)
        self.ScrumTeamFrame = tk.Frame(self)
        self.TeamMemberFrame = tk.Frame(self)
        self.AssignmentsFrame = tk.Frame(self)

        self.controller = controller

        self.Lb1 = tk.Listbox(self.ProductBacklogFrame)
        self.button1 = ttk.Button(self.ProductBacklogFrame,text='Click!')

        self.Lb2 = tk.Listbox(self.ScrumTeamFrame)
        self.button2 = ttk.Button(self.ScrumTeamFrame,text='Click!')
        
        self.Lb3 = tk.Listbox(self.TeamMemberFrame)
        self.button3 = ttk.Button(self.TeamMemberFrame,text='Click!')

        self.Lb4 = tk.Listbox(self.AssignmentsFrame)
        self.button4 = ttk.Button(self.AssignmentsFrame,text='Click!')
        
        self.ProductBacklogFrame.grid_rowconfigure(0, weight=1)
        self.ProductBacklogFrame.grid_rowconfigure(1, weight=1)
        self.ProductBacklogFrame.grid_columnconfigure(1, weight=1)

        self.CalendarFrame.grid_rowconfigure(0, weight=1)
        self.CalendarFrame.grid_rowconfigure(1, weight=1)
        self.CalendarFrame.grid_columnconfigure(1, weight=1)

        self.ScrumTeamFrame.grid_rowconfigure(0, weight=1)
        self.ScrumTeamFrame.grid_rowconfigure(1, weight=1)
        self.ScrumTeamFrame.grid_columnconfigure(1, weight=1)

        self.TeamMemberFrame.grid_rowconfigure(0, weight=1)
        self.TeamMemberFrame.grid_rowconfigure(1, weight=1)
        self.TeamMemberFrame.grid_columnconfigure(1, weight=1)

        self.AssignmentsFrame.grid_rowconfigure(0, weight=1)
        self.AssignmentsFrame.grid_rowconfigure(1, weight=1)
        self.AssignmentsFrame.grid_columnconfigure(1, weight=1)

        cal = tkcalendar.Calendar(self.CalendarFrame,font="Arial 14", selectmode='day',cursor="hand1", year=2018, month=2, day=5)
        cal.pack()

        self.Lb1.grid(row=0,column=0,rowspan=2,sticky=tk.NSEW)
        self.button1.grid(row=1,column=0, sticky=tk.S+tk.E+tk.W)

        self.Lb2.grid(row=0,column=0,rowspan=2,sticky=tk.NSEW)
        self.button2.grid(row=1,column=0, sticky=tk.S+tk.E+tk.W)
        
        self.Lb3.grid(row=0,column=0,rowspan=2,sticky=tk.NSEW)
        self.button3.grid(row=1,column=0, sticky=tk.S+tk.E+tk.W)

        self.Lb4.grid(row=0,column=0,rowspan=2,sticky=tk.NSEW)
        self.button4.grid(row=1,column=0, sticky=tk.S+tk.E+tk.W)
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        for x in range(0,4):
            self.grid_columnconfigure(x,weight=1)


        self.ProductBacklogFrame.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)#tk.W+tk.N+tk.S)
        self.CalendarFrame.grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)#tk.W+tk.N+tk.S)
        self.ScrumTeamFrame.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW)#tk.E+tk.N+tk.S)
        self.TeamMemberFrame.grid(row=0, column=3, rowspan=2, sticky=tk.NSEW)#tk.E+tk.N+tk.S)
        self.AssignmentsFrame.grid(row=0, column=4, rowspan=2, sticky=tk.NSEW)#tk.E+tk.N+tk.S)


