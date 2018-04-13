import tkinter as tk
from tkinter import ttk
from frames import ScrumblesFrames, listboxEventHandler
import sys
from styling import styling as style



class analyticsView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.initalRun = True

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Analytics")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

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

        self.insideUser = False
        self.userList = ScrumblesFrames.SList(self.userAnalyticsFrame, "USERS")
        self.userAnalyticsContents = tk.Frame(self.userAnalyticsFrame)
        self.userAnalyticsContentsOptions = []
        self.userAnalyticsContentsOptions.append(self.userAnalyticsContents)

        self.userList.listbox.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

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

        self.updateUserFrame()
        self.initalRun = False

    def generateTaskUserPie(self):
        taskUserPie = ScrumblesFrames.SPie(self.userGraphFrame)
        title = "Percentage of Tasks Completed By Users"
        #now we need labels, values
        labels = list()
        values = list()
        for user in self.controller.activeProject.listOfAssignedUsers:
            firstTask = True
            for task in user.listOfAssignedItems:
                if task.projectID == self.controller.activeProject.projectID:
                    if task.itemStatus == 4:
                        if firstTask is True:
                            values.append(1)
                            labels.append(user.userName)
                            firstTask = False
                        else:
                            values[-1] += 1

        taskUserPie.generateGraph(labels, values, title)
        return taskUserPie
    def generateTaskUserHistogram(self):
        taskUserHistogram = ScrumblesFrames.SHistogram(self.userGraphFrame)
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

    def generateUserLabels(self):
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

        userLabels = tk.Frame(self.userAnalyticsContents, relief=tk.SOLID, borderwidth=1)
        MVPLabels = tk.Frame(userLabels)
        MVPTasks = tk.Label(MVPLabels, text=MVPTaskName + " completed " + MVPTaskValue
                                              +" tasks. The most out of anyone in this project so far.")
        MVPPoints = tk.Label(MVPLabels, text=MVPPointsName + " earned " + MVPPointsValue
                                              +" points. The most out of anyone in this project so far.")
        averageLabels = tk.Frame(userLabels)
        averageTasks = tk.Label(averageLabels, text="The average amount of tasks completed in this project is " + averageTasksValue+".")
        averagePoints = tk.Label(averageLabels, text="The average amount of points earneed in this project is " + averagePointsValue+".")

        MVPTasks.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        MVPPoints.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        MVPLabels.pack(side=tk.TOP, fill=tk.X, expand=True)

        averageTasks.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        averagePoints.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        averageLabels.pack(side=tk.TOP, fill=tk.X, expand=True)


        return userLabels

    def listboxEvents(self, event):
        if event.widget is self.userList.listbox:
            self.generateInternalUserFrame(event)

    def generateInternalUserFrame(self, event):
        self.userEvent = event
        userName = event.widget.get(tk.ANCHOR)

        tasksCompleted, tasksAssigned, pointsEarned = self.getUserTaskInfo(userName)
        if tasksAssigned == 0:
            tasksAssigned = 1 #Prevent divide by zero when calculating percentage
        bestSprint, worstSprint, bestSprintPoints, worstSprintPoints = self.analyzeUserSprints(userName)
        internalUserFrame = tk.Frame(self.userAnalyticsFrame)
        # progress bar
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("scrumbles.Horizontal.TProgressbar", troughcolor=style.scrumbles_blue, background=style.scrumbles_orange)

        progressBarStyle = "scrumbles.Horizontal.TProgressbar"

        progressBarFrame = tk.Frame(internalUserFrame)
        userProgressBar = ttk.Progressbar(progressBarFrame, style=progressBarStyle, orient="horizontal", mode="determinate")
        userProgressBarTopping = tk.Frame(progressBarFrame)
        userProgressBarLabel = tk.Label(userProgressBarTopping, text=userName + " has completed " + str(int((tasksCompleted/tasksAssigned)*100)) + "% of the tasks they've been assigned.")
        userClearButton = tk.Button(userProgressBarTopping, text=style.left_arrow, command=lambda:self.clearSelection(self.userList.listbox,1), font=('Helvetica', '13'))
        userClearButton.pack(side=tk.LEFT)
        userProgressBarLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        userProgressBarTopping.pack(side=tk.TOP, fill=tk.X, expand=True)
        userProgressBar.pack(side=tk.TOP, fill=tk.X, expand=True)
        userProgressBar["value"] = tasksCompleted
        userProgressBar["maximum"] = tasksAssigned
        progressBarFrame.pack(side=tk.TOP, fill=tk.X, expand=False)

        statisticsFrame = tk.Frame(internalUserFrame,  relief=tk.SOLID, borderwidth=1)
        performanceFrame = tk.Frame(statisticsFrame,  relief=tk.SOLID, borderwidth=1)
        tasksCompletedLabel = tk.Label(performanceFrame, text="Tasks Completed: " + str(tasksCompleted))
        pointsEarnedLabel = tk.Label(performanceFrame, text="Points Earned: " + str(pointsEarned))
        sprintFrame = tk.Frame(statisticsFrame,  relief=tk.SOLID, borderwidth=1)
        bestSprintLabel = tk.Label(sprintFrame, text="User performed best on sprint " + bestSprint + " earning " + str(bestSprintPoints) + " points.")
        worstSprintLabel = tk.Label(sprintFrame, text="User performed worst on sprint " + worstSprint + " earning " + str(worstSprintPoints) + " points.")

        tasksCompletedLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        pointsEarnedLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        bestSprintLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        worstSprintLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        performanceFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        sprintFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        statisticsFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.userAnalyticsContents.pack_forget()
        if len(self.userAnalyticsContentsOptions) == 1:
            self.userAnalyticsContentsOptions.append(internalUserFrame)
        else:
            self.userAnalyticsContentsOptions[1] = internalUserFrame
        self.userAnalyticsContents = self.userAnalyticsContentsOptions[1]

        self.userAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.insideUser = True

    def getUserTaskInfo(self, userName):
        itemsAssigned = 0
        itemsCompleted = 0
        pointsEarned = 0
        for user in self.controller.activeProject.listOfAssignedUsers:
            if user.userName == userName:
                for item in user.listOfAssignedItems:
                    if item.projectID == self.controller.activeProject.projectID:
                        itemsAssigned +=1
                        if item.itemStatus == 4:
                            itemsCompleted +=1
                            pointsEarned += item.itemPoints
                break #end once we found the user
        return itemsCompleted, itemsAssigned, pointsEarned

    def analyzeUserSprints(self, userName):
        bestSprintPoints = -1
        worstSprintPoints = sys.maxsize
        bestSprintName = ""
        worstSprintName = ""
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            for user in sprint.listOfAssignedUsers:
                if user.userName == userName:
                    localPoints = 0
                    for item in user.listOfAssignedItems:
                        if item.projectID == self.controller.activeProject.projectID:
                            if item.itemStatus == 4:
                                localPoints += item.itemPoints
                        if localPoints < worstSprintPoints:
                            worstSprintPoints = localPoints
                            worstSprintName = sprint.sprintName
                        if localPoints > bestSprintPoints:
                            bestSprintPoints = localPoints
                            bestSprintName = sprint.sprintName
        return bestSprintName, worstSprintName, bestSprintPoints, worstSprintPoints

    def updateUserFrame(self):
        if self.insideUser is True:
            self.generateInternalUserFrame(self.userEvent)

        if self.initalRun is False:
            self.userList.pack_forget()
            self.userLabels.pack_forget()
            self.taskUserPieChart.pack_forget()
            self.taskUserHistogram.pack_forget()
            self.userAnalyticsContents.pack_forget()
            self.userGraphFrame.pack_forget()

        self.userLabels = self.generateUserLabels()

        self.userGraphFrame = tk.Frame(self.userAnalyticsContents)
        self.taskUserHistogram = self.generateTaskUserHistogram()
        self.taskUserPieChart = self.generateTaskUserPie()


        self.userList.pack(side=tk.LEFT, fill=tk.Y)
        self.userLabels.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.taskUserPieChart.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.taskUserHistogram.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.userAnalyticsContents.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.userGraphFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def clearSelection(self, listbox, view):
        if view == 0: #sprint analytics
            self.sprintAnalyticsContents.pack_forget()
            self.sprintAnalyticsContents = self.sprintAnalyticsContentsOptions[0]
        if view == 1: #user analytics
            self.userAnalyticsContents.pack_forget()
            self.userAnalyticsContents = self.userAnalyticsContentsOptions[0]
            self.userAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if view == 2: #task analytics
            self.taskAnalyticsContents.pack_forget()
            self.taskAnalyticsContents = self.taskAnalyticsContentsOptions[0]

        listbox.selection_clear(0, tk.END)
