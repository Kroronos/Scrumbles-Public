import tkinter as tk
from tkinter import ttk
import ScrumblesFrames


class analyticsView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Analytics")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.selectionNotebook = ttk.Notebook(self)

        self.sprintAnalyticsFrame = tk.Frame(self)
        self.userAnalyticsFrame = tk.Frame(self)
        self.taskAnalyticsFrame = tk.Frame(self)

        #Percent of Sprints Done
        #Tasks Completed Per Sprint
        #Weighed Tasks Completed Per Sprint (Points)
            #For Sprint
                #Number of Completed Items vs Date
                #Percent Assigned Completed

        #User With Most Tasks Completed
        #User With Most Points Earned
        #Average Tasks Completed Per User
        #Average Points Earned Per User
        #Chart Showing Tasks Completed By Users (What Percent Fall In What Quartile)'
            #Per User
                #Tasks Completed
                #Points Earned
                #Best Sprint
                #Worst Sprint

        #For Tasks
            #Average Time From Creation to Completion
            #Average Time From Creation to Submission
            #Average Time From Creation to Progress
            #Average Time From Creation to Assignent
            #Average Number of Points
            #Graph Point Distribution
                #Per Task
                    #TFCC
                    #TFCS
                    #TFCP
                    #TFCA
                    #Number of Points




        #removes the stupid lines around selections in notebooks
        style = ttk.Style()
        style.layout("Tab",
                     [('Notebook.tab', {'sticky': 'nswe', 'children':
                         [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                         # [('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                             [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                                # })],
                                                })],
                                        })]
                     )

        self.selectionNotebook.add(self.sprintAnalyticsFrame, text="Sprints")
        self.selectionNotebook.add(self.userAnalyticsFrame, text="Users")
        self.selectionNotebook.add(self.taskAnalyticsFrame, text="Tasks")

        self.selectionNotebook.enable_traversal() #Allows tabbing through ctrl+tab if notebook tabs are selected
        self.selectionNotebook.pack(fill=tk.BOTH, expand=True)

