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


        #Percent of Sprints Done - Progress Task
        #Tasks Completed Per Sprint - Bar Graph
        #Weighed Tasks Completed Per Sprint (Points) - Bar Graph
            #For Sprint
                #Number of Completed Items vs Date - Line Graph
                #Percent Assigned Completed - Progress Bar

            #Per User
                #Tasks Completed
                #Points Earned
                #Best Sprint
                #Worst Sprint
        self.userList = ScrumblesFrames.SList(self.userAnalyticsFrame, "USERS")
        self.averageMVPLabels = self.generateMVPLabels()
        self.taskUserHistogram = self.generateTaskUserHistogram()
        self.userList.pack(side=tk.LEFT, fill=tk.Y)
        self.averageMVPLabels.pack()
        self.taskUserHistogram.pack()

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
        self.updateFrame()
        self.controller.dataBlock.packCallback(self.updateFrame)

    def updateFrame(self):
        self.teamMembers = []
        self.teamMembers = [user.userName for user in self.controller.activeProject.listOfAssignedUsers]
        self.userList.importList(self.teamMembers)

    def generateTaskUserHistogram(self):
        taskUserHistogram = ScrumblesFrames.SHistogram(self.userAnalyticsFrame)
        tasksCompletedByUsers = []


        #get tasks completed per user
        bins = 0
        for user in self.controller.activeProject.listOfAssignedUsers:
            count = 0
            for item in user.listOfAssignedItems:
                if item.itemStatus == 4:
                    if item.projectID == self.controller.activeProject.projectID:
                        count = count + 1
            if count > bins:
                bins = count
            tasksCompletedByUsers.append(count)

        print(bins)
        for i in range(0, len(tasksCompletedByUsers)):
            if tasksCompletedByUsers[i] != 0:
                tasksCompletedByUsers[i] += 1
        taskUserHistogram.generateGraph(bins+1, tasksCompletedByUsers, "Tasks Completed","Number of Users")
        return taskUserHistogram

    def generateMVPLabels(self):
        MVPTaskName =  None
        MVPPointsName = None
        MVPTaskValue = 0
        MVPPointsValue = 0
        averageTasksValue = 0
        averagePointsValue = 0
        numOfUsers = len(self.controller.activeProject.listOfAssignedUsers)

        for user in self.controller.activeProject.listOfAssignedUsers:
            localPointsValue = 0
            localTasksValue = 0
            for item in user.listOfAssignedItems:
                if item.itemStatus == 4:
                    if item.projectID == self.controller.activeProject.projectID:
                        localPointsValue = item.itemPoints + localPointsValue
                        localTasksValue = localTasksValue + 1
                        averagePointsValue = item.itemPoints + averagePointsValue
                        averageTasksValue = averageTasksValue + 1
            if localPointsValue > MVPPointsValue:
                MVPPointsValue = localPointsValue
                MVPPointsName = user.userName

            if localTasksValue > MVPTaskValue:
                MVPTaskValue = localTasksValue
                MVPTaskName = user.userName

        averageTasksValue = averageTasksValue/numOfUsers
        averagePointsValue = averagePointsValue/numOfUsers

        #convert to strings for concatination
        MVPTaskValue = str(MVPTaskValue)
        MVPPointsValue = str(MVPPointsValue)
        averagePointsValue = str(averagePointsValue)
        averageTasksValue = str(averageTasksValue)

        MVPLabels = tk.Frame(self.userAnalyticsFrame)
        MVPTasks = tk.Label(MVPLabels, text=MVPTaskName + " completed " + MVPTaskValue
                                              +" tasks. The most out of anyone in this project so far.")
        MVPPoints = tk.Label(MVPLabels, text=MVPPointsName + " earned " + MVPPointsValue
                                              +" points. The most out of anyone in this project so far.")
        averageTasks = tk.Label(MVPLabels, text="The average amount of tasks completed in this project is " + averageTasksValue)
        averagePoints = tk.Label(MVPLabels, text="The average amount of points earneed in this project is " + averagePointsValue)

        MVPTasks.pack(side=tk.TOP, fill=tk.X)
        averageTasks.pack(side=tk.TOP, fill=tk.X)
        MVPPoints.pack(side=tk.TOP, fill=tk.X)
        averagePoints.pack(side=tk.TOP, fill=tk.X)

        return MVPLabels