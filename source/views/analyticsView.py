import tkinter as tk
from tkinter import ttk
from frames import ScrumblesFrames, listboxEventHandler
import sys
from styling import styling as style

from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import collections


class analyticsView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.initialRun = True

        self.tabButtons = ScrumblesFrames.STabs(self, controller, "Analytics")
        self.tabButtons.pack(side=tk.TOP, fill=tk.X)

        self.eventHandler = listboxEventHandler.listboxEventHandler()
        self.eventHandler.setEventToHandle(self.listboxEvents)

        self.selectionNotebook = ttk.Notebook(self)

        self.sprintAnalyticsFrame = tk.Frame(self)

        self.userAnalyticsFrame = tk.Frame(self)

        self.taskAnalyticsFrame = tk.Frame(self)

        self.insideSprint = False
        self.velocityWanted = True
        self.sprintList = ScrumblesFrames.SList(self.sprintAnalyticsFrame, "SPRINTS")
        self.sprintAnalyticsContents = tk.Frame(self.sprintAnalyticsFrame)
        self.sprintAnalyticsContentsOptions = []
        self.sprintAnalyticsContentsOptions.append(self.sprintAnalyticsContents)
        self.sprintList.listbox.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.insideUser = False
        self.userList = ScrumblesFrames.SList(self.userAnalyticsFrame, "USERS")
        self.userAnalyticsContents = tk.Frame(self.userAnalyticsFrame)
        self.userAnalyticsContentsOptions = []
        self.userAnalyticsContentsOptions.append(self.userAnalyticsContents)
        self.userList.listbox.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

        self.insideTask = False
        self.taskList = ScrumblesFrames.SList(self.taskAnalyticsFrame, "TASKS")
        self.taskAnalyticsContents = tk.Frame(self.taskAnalyticsFrame)
        self.taskAnalyticsContentsOptions = []
        self.taskAnalyticsContentsOptions.append(self.taskAnalyticsContents)

        self.taskList.listbox.bind('<<ListboxSelect>>', lambda event: self.eventHandler.handle(event))

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
        plt.close('all')
        self.teamMembers = []
        self.teamMembers = [user.userName for user in self.controller.activeProject.listOfAssignedUsers]
        self.userList.importList(self.teamMembers)

        self.sprintListing = []
        self.sprintListing = [sprint.sprintName for sprint in self.controller.activeProject.listOfAssignedSprints]
        self.sprintList.importList(self.sprintListing)

        self.taskListing = []
        self.taskListing = [item.itemTitle for item in self.controller.activeProject.listOfAssignedItems]
        self.taskList.importList(self.taskListing)

        self.updateSprintFrame()
        self.updateUserFrame()
        self.updateTaskFrame()
        self.initialRun = False

    def listboxEvents(self, event):
        if event.widget is self.sprintList.listbox:
            self.generateInternalSprintFrame(event)
        if event.widget is self.userList.listbox:
            self.generateInternalUserFrame(event)
        if event.widget is self.taskList.listbox:
            self.generateInternalTaskFrame(event)

    def updateUserFrame(self):
        if self.initialRun is False:
            self.userList.pack_forget()
            self.userLabels.pack_forget()
            self.taskUserPieChart.pack_forget()
            self.taskUserHistogram.pack_forget()
            if len(self.userAnalyticsContentsOptions) == 2:
                self.userAnalyticsContentsOptions[0].pack_forget()
                self.userAnalyticsContentsOptions[1].pack_forget()
            self.userAnalyticsContents.pack_forget()
            self.userGraphFrame.pack_forget()

        self.userLabels = self.generateUserLabels()

        self.userGraphFrame = tk.Frame(self.userAnalyticsContentsOptions[0])
        self.taskUserHistogram = self.generateTaskUserHistogram()
        self.taskUserPieChart = self.generateTaskUserPie()

        if self.insideUser is False:
            self.userAnalyticsContents = self.userAnalyticsContentsOptions[0]

        self.userList.pack(side=tk.LEFT, fill=tk.Y)
        self.userGraphFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.userLabels.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.taskUserPieChart.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.taskUserHistogram.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.userAnalyticsContents.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        if self.insideUser is True:
            self.generateInternalUserFrame(userEventName=self.userEventName)

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
        if len(labels) == 0:
            labels.append("Completed By Active Users")
            labels.append("Completed By Former Users")
            values.append(0)
            values.append(0)
        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemStatus == 4:
                values[0] += 1
        if values[0] == 0:
            labels[0] = "Complete"
            labels[1] = "Incomplete"
            values[1] = 1
        taskUserPie.generateGraph(labels, values, title)
        return taskUserPie


    def generateTaskUserHistogram(self):
        taskUserHistogram = ScrumblesFrames.SHistogram(self.userGraphFrame)
        tasksStateByUsers = []


        #get tasks State per user
        bins = 0
        for user in self.controller.activeProject.listOfAssignedUsers:
            count = 0
            for item in user.listOfAssignedItems:
                if item.itemStatus == 4:
                    if item.projectID == self.controller.activeProject.projectID:
                        count = count + 1
            if count > bins:
                bins = count
            tasksStateByUsers.append(count)

        taskUserHistogram.generateGraph(bins+1, tasksStateByUsers, "Tasks Complete","Number of Users")
        return taskUserHistogram

    def generateUserLabels(self):
        MVPTaskName = ""
        MVPPointsName = ""
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
        averagePointsValue = str("%.2f"%averagePointsValue)
        averageTasksValue = str("%.2f"%averageTasksValue)

        if MVPTaskName == "":
            MVPTaskName = "No one"
            MVPPointsName = "No one"
            MVPTaskValue = "any"
            MVPPointsValue = "any"
        userLabels = tk.Frame(self.userAnalyticsContentsOptions[0], relief=tk.SOLID, borderwidth=1)

        MVPLabels = tk.Frame(userLabels)
        MVPTasks = tk.Label(MVPLabels, text=MVPTaskName + " completed " + MVPTaskValue
                                              +" tasks. The most out of anyone in this project so far.")
        MVPPoints = tk.Label(MVPLabels, text=MVPPointsName + " earned " + MVPPointsValue
                                              +" points. The most out of anyone in this project so far.")
        averageLabels = tk.Frame(userLabels)
        averageTasks = tk.Label(averageLabels, text="The average amount of tasks completed in this project is " + averageTasksValue+".")
        averagePoints = tk.Label(averageLabels, text="The average amount of points earned in this project is " + averagePointsValue+".")


        MVPTasks.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        MVPPoints.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        MVPLabels.pack(side=tk.TOP, fill=tk.X, expand=True)

        averageTasks.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        averagePoints.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        averageLabels.pack(side=tk.TOP, fill=tk.X, expand=True)


        return userLabels

    def generateInternalUserFrame(self, event=None, userEventName=None):
        if event is not None:
            userName = event.widget.get(tk.ANCHOR)
            self.userEventName = userName
        if userEventName is not None:
            userName = userEventName

        tasksCompleted, tasksAssigned, pointsEarned, matchFound = self.getUserTaskInfo(userName)

        if matchFound is False:
            self.clearSelection(self.userList.listbox, 1)
            return
          
        if tasksAssigned == 0:
            tasksAssigned = 1 #Prevent divide by zero when calculating percentage
        bestSprint, worstSprint, bestSprintPoints, worstSprintPoints = self.analyzeUserSprints(userName)
        internalUserFrame = tk.Frame(self.userAnalyticsFrame)
        # progress bar
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("scrumbles.Horizontal.TProgressbar", troughcolor = 'gray', background = style.scrumbles_green_fg)

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
        if tasksCompleted == 0:
            bestSprintLabel = tk.Label(sprintFrame, text="User hasn't completed any task in any sprint, so they have no best sprint.")
            worstSprintLabel = tk.Label(sprintFrame, text="User hasn't completed any task in any sprint, so they have no worst sprint.")
        else:
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
        matchFound = False
        for user in self.controller.activeProject.listOfAssignedUsers:
            if user.userName == userName:
                for item in user.listOfAssignedItems:
                    if item.projectID == self.controller.activeProject.projectID:
                        itemsAssigned +=1
                        if item.itemStatus == 4:
                            itemsCompleted +=1
                            pointsEarned += item.itemPoints
                matchFound = True
                break #end once we found the user
        return itemsCompleted, itemsAssigned, pointsEarned, matchFound

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
      
    def updateSprintFrame(self):
        if self.initialRun is False:
            self.sprintAnalyticsContentsOptions[0].pack_forget()
            if len(self.sprintAnalyticsContentsOptions) == 2:
                self.sprintAnalyticsContentsOptions[1].pack_forget()
            self.sprintAnalyticsContents.pack_forget()
            self.sprintList.pack_forget()

            self.sprintAnalyticsContentsOptions[0] = tk.Frame(self.sprintAnalyticsFrame)

        self.generateSprintProgressBar()

        self.generateSprintGraphs()

        if self.insideSprint is False:
            self.sprintAnalyticsContents = self.sprintAnalyticsContentsOptions[0]

        self.sprintList.pack(side=tk.LEFT, fill=tk.Y)
        self.sprintAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        if self.insideSprint is True:
            self.generateInternalSprintFrame(sprintEventName=self.sprintEventName)

    def generateSprintProgressBar(self):
        progressBarStyle = "scrumbles.Horizontal.TProgressbar"
        maxValue = len(self.controller.activeProject.listOfAssignedSprints)
        currValue = maxValue
        sprintProgressBarFrame = tk.Frame(self.sprintAnalyticsContentsOptions[0])
        sprintProgressBar = ttk.Progressbar(sprintProgressBarFrame, style=progressBarStyle, orient="horizontal", mode="determinate")
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            for item in sprint.listOfAssignedItems:
                if item.itemStatus != 4:
                    currValue -= 1
                    break
        sprintProgressBar["value"] = currValue
        sprintProgressBar["maximum"] = maxValue

        sprintProgressBarLabel = tk.Label(sprintProgressBarFrame, text=str(currValue)+" Sprints have been fully completed out of " + str(maxValue) + " .")

        sprintProgressBarLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        sprintProgressBar.pack(side=tk.TOP, fill=tk.X, expand=True)
        sprintProgressBarFrame.pack(side=tk.TOP, fill=tk.X)

    def generateSprintGraphs(self):
        self.sprintGraphFrame = tk.Frame(self.sprintAnalyticsContentsOptions[0])
        sprintNames, sprintTaskValues, sprintPointValues = self.analyzeSprints()
        self.generateSprintTaskBarGraph(sprintNames, sprintTaskValues)
        self.generateSprintPointBarGraph(sprintNames, sprintPointValues)
        self.sprintGraphFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def analyzeSprints(self):
        sprintNames = list()
        sprintTasks = list()
        sprintPoints = list()
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            firstRun = True
            sprintNames.append(sprint.sprintName)
            for item in sprint.listOfAssignedItems:
                if firstRun is True:
                    if item.itemStatus == 4:
                        sprintTasks.append(1)
                        sprintPoints.append(item.itemPoints)
                    else:
                        sprintTasks.append(0)
                        sprintPoints.append(0)
                    firstRun = False
                else:
                    if item.itemStatus == 4:
                        sprintTasks[-1] += 1
                        sprintPoints[-1] += item.itemPoints
        return sprintNames, sprintTasks, sprintPoints

    def generateSprintTaskBarGraph(self, sprintNames, sprintTaskValues):
        sprintBarGraph = ScrumblesFrames.SBar(self.sprintGraphFrame)
        tickValue = int((max(sprintTaskValues)-min(sprintTaskValues))/10)
        if tickValue <= 0:
            tickValue = 1
        sprintBarGraph.generateGraph(sprintNames, sprintTaskValues, "Sprints", "Tasks Completed", tickValue=tickValue)
        sprintBarGraph.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def generateSprintPointBarGraph(self, sprintNames, sprintPointValues):
        sprintBarGraph = ScrumblesFrames.SBar(self.sprintGraphFrame)
        tickValue = int((max(sprintPointValues)-min(sprintPointValues))/10)
        if tickValue <= 0:
            tickValue = 1
        sprintBarGraph.generateGraph(sprintNames, sprintPointValues, "Sprints", "Points Earned", isOrange=True, tickValue=tickValue)
        sprintBarGraph.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def generateInternalSprintFrame(self, event=None, sprintEventName=None, velocityWanted=True):
        if event is not None:
            sprintName = event.widget.get(tk.ANCHOR)
            self.sprintEventName = sprintName
        if sprintEventName is not None:
            sprintName = sprintEventName


        internalSprintFrame = tk.Frame(self.sprintAnalyticsFrame)
        # progress bar
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("scrumbles.Horizontal.TProgressbar", troughcolor='gray', background=style.scrumbles_green_fg)

        tasksAssigned = 0
        tasksCompleted = 0

        matchFound = False
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == sprintName:
                for item in sprint.listOfAssignedItems:
                    tasksAssigned +=1
                    if item.itemStatus == 4:
                        tasksCompleted += 1
                matchFound = True
                break  #escape once sprint has been found

        if matchFound is False:
            self.clearSelection(self.sprintList.listbox, 0)
            return

        if tasksAssigned == 0:
            tasksAssigned += 1
        progressBarStyle = "scrumbles.Horizontal.TProgressbar"

        progressBarFrame = tk.Frame(internalSprintFrame)
        sprintProgressBar = ttk.Progressbar(progressBarFrame, style=progressBarStyle, orient="horizontal", mode="determinate")
        sprintProgressBarTopping = tk.Frame(progressBarFrame)
        sprintProgressBarLabel = tk.Label(sprintProgressBarTopping, text=sprintName + " has completed " + str(int((tasksCompleted/tasksAssigned)*100)) + "% of the tasks assigned to it.")
        sprintClearButton = tk.Button(sprintProgressBarTopping, text=style.left_arrow, command=lambda:self.clearSelection(self.sprintList.listbox,0), font=('Helvetica', '13'))

        selectorFrame = tk.Frame(internalSprintFrame)
        selectorTopFrame = tk.Frame(selectorFrame)
        velocityButton = tk.Button(selectorTopFrame, text="Velocity", command=lambda: self.changeSprintGraph(True))
        tasksButton = tk.Button(selectorTopFrame, text="Completed Tasks", command=lambda: self.changeSprintGraph(False))
        if velocityWanted is True:
            velocityButton.config(bg= style.scrumbles_offwhite)
            tasksButton.config(bg = style.scrumbles_grey)
        else:
            velocityButton.config(bg=style.scrumbles_grey)
            tasksButton.config(bg=style.scrumbles_offwhite)

        sprintClearButton.pack(side=tk.LEFT)
        sprintProgressBarLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        sprintProgressBarTopping.pack(side=tk.TOP, fill=tk.X, expand=True)
        sprintProgressBar.pack(side=tk.TOP, fill=tk.X, expand=True)
        sprintProgressBar["value"] = tasksCompleted
        sprintProgressBar["maximum"] = tasksAssigned
        progressBarFrame.pack(side=tk.TOP, fill=tk.X, expand=False)

        velocityButton.pack(side=tk.LEFT)
        tasksButton.pack(side=tk.LEFT)
        selectorTopFrame.pack(side=tk.TOP, fill=tk.X)
        selectorFrame.pack(side=tk.TOP, fill=tk.X)

        statisticsFrame = tk.Frame(internalSprintFrame,  relief=tk.SOLID, borderwidth=1)
        if velocityWanted is True:
            self.generateInternalVelocityLineGraph(statisticsFrame, sprintName)
        else:
            self.generateInternalSprintLineGraph(statisticsFrame, sprintName)
        statisticsFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sprintAnalyticsContents.pack_forget()
        if len(self.sprintAnalyticsContentsOptions) == 1:
            self.sprintAnalyticsContentsOptions.append(internalSprintFrame)
        else:
            self.sprintAnalyticsContentsOptions[1] = internalSprintFrame
        self.sprintAnalyticsContents = self.sprintAnalyticsContentsOptions[1]

        self.sprintAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.insideSprint = True
    
    def generateInternalVelocityLineGraph(self,controller, sprintName):
        CompletedItemDatePair = {}
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == sprintName:
                CompletedItemDatePair.update({sprint.sprintStartDate: 0})
                for item in sprint.listOfAssignedItems:
                    if item.itemStatus == 4:
                        if item.itemTimeLine["Completed"] != datetime(9999, 12, 31, 23, 59, 59):
                            alreadyInDict = False
                            alreadyKeyed = None
                            for key in CompletedItemDatePair.keys():
                                if key.strftime("%y%m%d") == item.itemTimeLine["Completed"].strftime("%y%m%d"):
                                    alreadyInDict = True
                                    alreadyKeyed = key
                                    break

                            if alreadyInDict is True:
                                CompletedItemDatePair[alreadyKeyed] += item.itemPoints
                            else:
                                CompletedItemDatePair.update({item.itemTimeLine["Completed"]: item.itemPoints})

                isCurrentMatch = False
                for key in CompletedItemDatePair.keys():
                    if datetime.now().strftime("%y%m%d") == key.strftime("%y%m%d"):
                        isCurrentMatch = True


                if isCurrentMatch is False:
                    CompletedItemDatePair.update({datetime.now(): 0})
                break
        labels = list()
        xvalues = list()
        for date in CompletedItemDatePair.keys():
            labels.append(date.strftime("%m/%d/%y"))
            xvalues.append(int(date.strftime("%y%m%d"))) #so that our x's are actually chronological
        yvalues = list(CompletedItemDatePair.values())

        newLabels = list()
        labelsPositions = list()
        lastStoredValue = 0

        xvalues, yvalues, labels = (list(t) for t in zip(*sorted(zip(xvalues, yvalues, labels)))) #sort for proper behavior
        for i in range(0, len(xvalues)): #this fixes overlapping labels on x axis
            if i == 0:
                lastStoredValue = xvalues[i]
                labelsPositions.append(xvalues[i])
                newLabels.append(labels[i])
            else:
                if xvalues[i]-lastStoredValue >= int((xvalues[0] - xvalues[-1])/5): #about a month off
                    if xvalues[i]-lastStoredValue > 5: #5 day min
                        lastStoredValue = xvalues[i]
                        labelsPositions.append(xvalues[i])
                        newLabels.append(labels[i])

        internalSprintPointsGraph = ScrumblesFrames.SLine(controller)
        internalSprintPointsGraph.generateGraph(xvalues, yvalues, labelsPositions, newLabels,
                                                "Date of Completion","Points Earned",
                                                yticks=int(max(yvalues)/10))
        internalSprintPointsGraph.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def generateInternalSprintLineGraph(self, controller, sprintName):
        CompletedItemDatePair = {}
        for sprint in self.controller.activeProject.listOfAssignedSprints:
            if sprint.sprintName == sprintName:
                CompletedItemDatePair.update({sprint.sprintStartDate: 0})
                for item in sprint.listOfAssignedItems:
                    if item.itemStatus == 4:
                        if item.itemTimeLine["Completed"] != datetime(9999, 12, 31, 23, 59, 59):
                            alreadyInDict = False
                            alreadyKeyed = None
                            for key in CompletedItemDatePair.keys():
                                if key.strftime("%y%m%d") == item.itemTimeLine["Completed"].strftime("%y%m%d"):
                                    alreadyInDict = True
                                    alreadyKeyed = key
                                    break

                            if alreadyInDict is True:
                                CompletedItemDatePair[alreadyKeyed] += 1
                            else:
                                CompletedItemDatePair.update({item.itemTimeLine["Completed"]: 1})

                isCurrentMatch = False
                for key in CompletedItemDatePair.keys():
                    if datetime.now().strftime("%y%m%d") == key.strftime("%y%m%d"):
                        isCurrentMatch = True


                if isCurrentMatch is False:
                    CompletedItemDatePair.update({datetime.now(): 0})
                break
        labels = list()
        xvalues = list()
        for date in CompletedItemDatePair.keys():
            labels.append(date.strftime("%m/%d/%y"))
            xvalues.append(int(date.strftime("%y%m%d"))) #so that our x's are actually chronological
        yvalues = list(CompletedItemDatePair.values())

        newLabels = list()
        labelsPositions = list()
        lastStoredValue = 0

        xvalues, yvalues, labels = (list(t) for t in zip(*sorted(zip(xvalues, yvalues, labels)))) #sort for proper behavior
        for i in range(0, len(xvalues)): #this fixes overlapping labels on x axis
            if i == 0:
                lastStoredValue = xvalues[i]
                labelsPositions.append(xvalues[i])
                newLabels.append(labels[i])
            else:
                if xvalues[i]-lastStoredValue >= int((xvalues[0] - xvalues[-1])/5): #about a month off
                    if xvalues[i]-lastStoredValue > 5: #5 day min
                        lastStoredValue = xvalues[i]
                        labelsPositions.append(xvalues[i])
                        newLabels.append(labels[i])

        internalSprintLineGraph = ScrumblesFrames.SLine(controller)
        internalSprintLineGraph.generateGraph(xvalues, yvalues, labelsPositions, newLabels, "Date of Completion","Completed Tasks")
        internalSprintLineGraph.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def updateTaskFrame(self):
        if self.initialRun is False:
            self.taskAnalyticsContentsOptions[0].pack_forget()
            if len(self.taskAnalyticsContentsOptions) == 2:
                self.taskAnalyticsContentsOptions[1].pack_forget()
            self.taskAnalyticsContents.pack_forget()
            self.taskAnalyticsContentsTop.pack_forget()
            self.taskList.pack_forget()

            self.taskAnalyticsContentsOptions[0] = tk.Frame(self.taskAnalyticsFrame)

        self.taskAnalyticsContentsTop = tk.Frame(self.taskAnalyticsContentsOptions[0])
        self.generateTaskGraphs()
        self.generateAverageCreationToStateLabels()

        self.taskAnalyticsContentsTop.pack(side=tk.TOP, fill=tk.X, expand=True)

        if self.insideTask is False:
            self.taskAnalyticsContents = self.taskAnalyticsContentsOptions[0]

        self.taskList.pack(side=tk.LEFT, fill=tk.Y)
        self.taskAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        if self.insideTask is True:
            self.generateInternalTaskFrame(taskEventName=self.taskEventName)

    def generateAverageCreationToStateLabels(self):
        totalCreationCompletion = timedelta(0)
        totalCreationCompletionTasks = 0
        totalCreationSubmission = timedelta(0)
        totalCreationSubmissionTasks = 0
        totalCreationProgress = timedelta(0)
        totalCreationProgressTasks = 0
        totalCreationUserAssignment = timedelta(0)
        totalCreationUserAssignmentTasks = 0
        totalNumberOfPoints = 0
        numberOfItems = 0
        maxDate = datetime(9999, 12, 31, 23, 59, 59)
        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemTimeLine["Completed"] != maxDate:
                totalCreationCompletion = totalCreationCompletion + (item.itemTimeLine["Completed"] - item.itemCreationDate)
                totalCreationCompletionTasks +=1
            if item.itemTimeLine["Submitted"] != maxDate:
                totalCreationSubmission = totalCreationSubmission + (item.itemTimeLine["Submitted"] - item.itemCreationDate)
                totalCreationSubmissionTasks += 1
            if item.itemTimeLine["WorkStarted"] != maxDate:
                totalCreationProgress = totalCreationProgress + (item.itemTimeLine["WorkStarted"] - item.itemCreationDate)
                totalCreationProgressTasks += 1
            if item.itemTimeLine["AssignedToUser"] != maxDate:
                totalCreationUserAssignment = totalCreationUserAssignment + (item.itemTimeLine["AssignedToUser"] - item.itemCreationDate)
                totalCreationUserAssignmentTasks +=1
            totalNumberOfPoints += item.itemPoints
            numberOfItems += 1

        if totalCreationSubmissionTasks == 0:
            totalCreationSubmissionTasks += 1
        if totalCreationCompletionTasks == 0:
            totalCreationCompletionTasks += 1
        if totalCreationUserAssignmentTasks == 0:
            totalCreationUserAssignmentTasks +=1
        if totalCreationProgressTasks == 0:
            totalCreationProgressTasks += 1

        averageCreationCompletion = totalCreationCompletion/totalCreationCompletionTasks
        averageCreationSubmission = totalCreationSubmission/totalCreationSubmissionTasks
        averageCreationProgress = totalCreationProgress/totalCreationProgressTasks
        averageCreationUserAssignment = totalCreationUserAssignment/totalCreationUserAssignmentTasks
        averageNumberOfPoints = totalNumberOfPoints/numberOfItems

        averageCreationCompletionWeeks = int(averageCreationCompletion.days/7)
        averageCreationSubmissionWeeks = int(averageCreationSubmission.days/7)
        averageCreationProgressWeeks = int(averageCreationProgress.days/7)
        averageCreationUserAssignmentWeeks = int(averageCreationUserAssignment.days/7)

        averageCreationCompletionDays = averageCreationCompletion.days - averageCreationCompletionWeeks*7
        averageCreationSubmissionDays = averageCreationSubmission.days - averageCreationSubmissionWeeks*7
        averageCreationProgressDays = averageCreationProgress.days - averageCreationProgressWeeks*7
        averageCreationUserAssignmentDays  = averageCreationUserAssignment.days - averageCreationUserAssignmentWeeks*7

        if averageCreationCompletionWeeks == 0:
            averageCreationCompletionString = "The average time for tasks to be completed after creation is "\
                                              + str(averageCreationCompletionDays) + " " \
                                              + self.dayOrDays(averageCreationCompletionDays) + "."
        elif averageCreationCompletionDays == 0 and averageCreationCompletionWeeks != 1:
            averageCreationCompletionString = "The average time for tasks to be completed after creation is "\
                                              + str(averageCreationCompletionWeeks) + " " \
                                              + self.weekOrWeeks(averageCreationCompletionWeeks) + "."
        else:
            averageCreationCompletionString = "The average time for tasks to be completed after creation is " \
                                              + str(averageCreationCompletionWeeks) + " " \
                                              + self.weekOrWeeks(averageCreationCompletionWeeks) + " and " \
                                              + str(averageCreationCompletionDays) + " "\
                                              + self.dayOrDays(averageCreationCompletionDays) + "."
        if averageCreationSubmissionWeeks == 0:
            averageCreationSubmissionString = "The average time for tasks to be submitted after creation is "\
                                              + str(averageCreationSubmissionDays) + " " \
                                              + self.dayOrDays(averageCreationSubmissionDays) + "."
        elif averageCreationSubmissionDays == 0:
            averageCreationSubmissionString = "The average time for tasks to be submitted after creation is "\
                                              + str(averageCreationSubmissionWeeks) + " "\
                                              + self.weekOrWeeks(averageCreationSubmissionWeeks) + "."
        else:
            averageCreationSubmissionString = "The average time for tasks to be submitted after creation is " \
                                              + str(averageCreationSubmissionWeeks) + " " \
                                              + self.weekOrWeeks(averageCreationSubmissionWeeks) + " and " \
                                              + str(averageCreationSubmissionDays) + " " \
                                              + self.dayOrDays(averageCreationSubmissionDays) + "."

        if averageCreationProgressWeeks == 0:
            averageCreationProgressString = "The average time for work to begin on tasks is "\
                                              + str(averageCreationProgressDays) + " " \
                                            + self.dayOrDays(averageCreationProgressDays) + "."
        elif averageCreationProgressDays == 0:
            averageCreationProgressString = "The average time for work to begin on tasks is "\
                                              + str(averageCreationProgressWeeks) + " "\
                                            + self.weekOrWeeks(averageCreationProgressWeeks) + "."
        else:
            averageCreationProgressString = "The average time for work to begin on tasks is "\
                                              + str(averageCreationProgressWeeks) + " " \
                                            + self.weekOrWeeks(averageCreationProgressWeeks) + " and " \
                                              + str(averageCreationProgressDays) + " " + \
                                            self.dayOrDays(averageCreationProgressDays) + "."

        if averageCreationUserAssignmentWeeks == 0:
            averageCreationUserAssignmentString = "The average time for tasks to be assigned to users is "\
                                              + str(averageCreationUserAssignmentDays) + " " \
                                                  + self.dayOrDays(averageCreationUserAssignmentDays) + "."
        elif averageCreationUserAssignmentDays == 0:
            averageCreationUserAssignmentString = "The average time for tasks to be assigned to users is "\
                                              + str(averageCreationUserAssignmentWeeks) + " " \
                                                  + self.weekOrWeeks(averageCreationUserAssignmentWeeks) + "."
        else:
            averageCreationUserAssignmentString = "The average time for tasks to be assigned to users is " \
                                              + str(averageCreationUserAssignmentWeeks) + " " \
                                                  + self.weekOrWeeks(averageCreationUserAssignmentWeeks) + " and " \
                                              + str(averageCreationUserAssignmentDays) + " " \
                                                  + self.dayOrDays(averageCreationUserAssignmentDays) + "."
        labelFrame = tk.Frame(self.taskAnalyticsContentsTop, highlightthickness=1)
        creationCompletionLabel = tk.Label(labelFrame,
                                           text=averageCreationCompletionString)
        creationSubmissionLabel = tk.Label(labelFrame,
                                           text=averageCreationSubmissionString)
        creationProgressLabel = tk.Label(labelFrame,
                                           text=averageCreationProgressString)
        creationUserAssignmentLabel = tk.Label(labelFrame,
                                           text=averageCreationUserAssignmentString)
        numberOfPointsLabel = tk.Label(labelFrame,
                                       text="The average number of points assigned to each task is "
                                            + str("%.2f"%averageNumberOfPoints) + ".")

        creationCompletionLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        creationSubmissionLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        creationProgressLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        creationUserAssignmentLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        numberOfPointsLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        labelFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def generateTaskGraphs(self):
        self.taskStatePieFrame = tk.Frame(self.taskAnalyticsContentsTop)
        self.generateTaskStatePieChart()
        self.taskStatePieFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.taskPointDistributionFrame = tk.Frame(self.taskAnalyticsContentsOptions[0], highlightthickness=1)
        self.generatePointDistributionGraph()
        self.taskPointDistributionFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def generatePointDistributionGraph(self):
        pointsDistribution = list()
        bins = 0
        for item in self.controller.activeProject.listOfAssignedItems:
            bins+=1
            pointsDistribution.append(item.itemPoints)

        pointDistributionHistogram = ScrumblesFrames.SHistogram(self.taskPointDistributionFrame)
        pointDistributionHistogram.generateGraph(max(pointsDistribution), pointsDistribution, "Point Value", "Number Of Tasks", max(pointsDistribution)/(max(pointsDistribution)/10))
        pointDistributionHistogram.pack(side=tk.TOP, fill=tk.X, expand=True)
        
    def generateTaskStatePieChart(self):
        taskStatePie = ScrumblesFrames.SPie(self.taskStatePieFrame)
        title = "State Of Project Tasks"
        #now we need labels, values
        labels = ["Not Assigned", "Assigned", "In Progress", "Submitted", "Completed"]
        values = [0, 0, 0, 0, 0]

        for item in self.controller.activeProject.listOfAssignedItems:
            values[item.itemStatus] += 1

        #check for 0%s
        for index, value in enumerate(values):
            if value == 0:
                del values[index]
                del labels[index]
        for index, value in enumerate(values):
            if value == 0:
                labels[index] = "Other"
        taskStatePie.generateGraph(labels, values, title)
        taskStatePie.pack(side=tk.TOP, fill=tk.BOTH)

    def generateInternalTaskFrame(self, event=None, taskEventName=None):
        if event is not None:
            taskName = event.widget.get(tk.ANCHOR)
            self.taskEventName = taskName
        if taskEventName is not None:
            taskName = taskEventName


        internalTaskFrame = tk.Frame(self.taskAnalyticsFrame)
        
        creationCompletion = timedelta(0)
        creationSubmission = timedelta(0)
        creationProgress = timedelta(0)
        creationUserAssignment = timedelta(0)
        numberOfPoints = 0

        maxDate = datetime(9999, 12, 31, 23, 59, 59)
        trueItem = None
        matchFound = False
        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemTitle == taskName:
                if item.itemTimeLine["Completed"] != maxDate:
                    creationCompletion = (item.itemTimeLine["Completed"] - item.itemCreationDate)
                if item.itemTimeLine["Submitted"] != maxDate:
                    creationSubmission = (item.itemTimeLine["Submitted"] - item.itemCreationDate)
                if item.itemTimeLine["WorkStarted"] != maxDate:
                    creationProgress = (item.itemTimeLine["WorkStarted"] - item.itemCreationDate)
                if item.itemTimeLine["AssignedToUser"] != maxDate:
                    creationUserAssignment = (item.itemTimeLine["AssignedToUser"] - item.itemCreationDate)

                numberOfPoints += item.itemPoints
                matchFound = True
                trueItem = item
                break

        if matchFound is False:
            self.clearSelection(self.taskList.listbox, 2)
            return

        taskInternalTopFrame = tk.Frame(internalTaskFrame)
        taskClearButton = tk.Button(taskInternalTopFrame, text=style.left_arrow, command=lambda:self.clearSelection(self.taskList.listbox, 2), font=('Helvetica', '13'))
        taskNameLabel = tk.Label(taskInternalTopFrame, text=taskName, font=style.comment_font, relief="solid", borderwidth=.5)

        taskClearButton.pack(side=tk.LEFT)
        taskNameLabel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        taskInternalTopFrame.pack(side=tk.TOP, fill=tk.X)

        creationCompletionWeeks = int(creationCompletion.days/7)
        creationSubmissionWeeks = int(creationSubmission.days/7)
        creationProgressWeeks = int(creationProgress.days/7)
        creationUserAssignmentWeeks = int(creationUserAssignment.days/7)

        creationCompletionDays = creationCompletion.days - creationCompletionWeeks*7
        creationSubmissionDays = creationSubmission.days - creationSubmissionWeeks*7
        creationProgressDays = creationProgress.days - creationProgressWeeks*7
        creationUserAssignmentDays = creationUserAssignment.days - creationUserAssignmentWeeks*7

        if creationCompletionWeeks == 0:
            creationCompletionString = "This task was completed in  "\
                                              + str(creationCompletionDays) + " " \
                                              + self.dayOrDays(creationCompletionDays) + "."
        elif creationCompletionDays == 0 and creationCompletionWeeks != 1:
            creationCompletionString = "This task was completed in "\
                                              + str(creationCompletionWeeks) + " " \
                                              + self.weekOrWeeks(creationCompletionWeeks) + "."
        else:
            creationCompletionString = "This task was completed in " \
                                              + str(creationCompletionWeeks) + " " \
                                              + self.weekOrWeeks(creationCompletionWeeks) + " and " \
                                              + str(creationCompletionDays) + " "\
                                              + self.dayOrDays(creationCompletionDays) + "."
        if creationSubmissionWeeks == 0:
            creationSubmissionString = "This task was submitted in "\
                                              + str(creationSubmissionDays) + " " \
                                              + self.dayOrDays(creationSubmissionDays) + "."
        elif creationSubmissionDays == 0:
            creationSubmissionString = "This task was submitted in "\
                                              + str(creationSubmissionWeeks) + " "\
                                              + self.weekOrWeeks(creationSubmissionWeeks) + "."
        else:
            creationSubmissionString = "This task was submitted in " \
                                              + str(creationSubmissionWeeks) + " " \
                                              + self.weekOrWeeks(creationSubmissionWeeks) + " and " \
                                              + str(creationSubmissionDays) + " " \
                                              + self.dayOrDays(creationSubmissionDays) + "."

        if creationProgressWeeks == 0:
            creationProgressString = "Work began on this task in "\
                                              + str(creationProgressDays) + " " \
                                            + self.dayOrDays(creationProgressDays) + "."
        elif creationProgressDays == 0:
            creationProgressString = "Work began on this task in "\
                                              + str(creationProgressWeeks) + " "\
                                            + self.weekOrWeeks(creationProgressWeeks) + "."
        else:
            creationProgressString = "Work began on this task in "\
                                              + str(creationProgressWeeks) + " " \
                                            + self.weekOrWeeks(creationProgressWeeks) + " and " \
                                              + str(creationProgressDays) + " " + \
                                            self.dayOrDays(creationProgressDays) + "."

        if creationUserAssignmentWeeks == 0:
            creationUserAssignmentString = "This task was assigned to a user in "\
                                              + str(creationUserAssignmentDays) + " " \
                                                  + self.dayOrDays(creationUserAssignmentDays) + "."
        elif creationUserAssignmentDays == 0:
            creationUserAssignmentString = "This task was assigned to a user in "\
                                              + str(creationUserAssignmentWeeks) + " " \
                                                  + self.weekOrWeeks(creationUserAssignmentWeeks) + "."
        else:
            creationUserAssignmentString = "This task was assigned to a user in " \
                                              + str(creationUserAssignmentWeeks) + " " \
                                                  + self.weekOrWeeks(creationUserAssignmentWeeks) + " and " \
                                              + str(creationUserAssignmentDays) + " " \
                                                  + self.dayOrDays(creationUserAssignmentDays) + "."

        labelFrame = tk.Frame(internalTaskFrame, highlightthickness=1)
        creationCompletionLabel = tk.Label(labelFrame,
                                           text=creationCompletionString)
        creationSubmissionLabel = tk.Label(labelFrame,
                                           text=creationSubmissionString)
        creationProgressLabel = tk.Label(labelFrame,
                                           text=creationProgressString)
        creationUserAssignmentLabel = tk.Label(labelFrame,
                                           text=creationUserAssignmentString)
        numberOfPointsLabel = tk.Label(labelFrame,
                                       text="The number of points assigned to this task is "
                                            + str("%.2f"%numberOfPoints) + ".")

        statisticsFrame = tk.Frame(internalTaskFrame,  relief=tk.SOLID, borderwidth=1)
        self.generateTaskGanttChart(statisticsFrame, taskName)
        statisticsFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if trueItem.itemStatus == 4:
            creationCompletionLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        if trueItem.itemStatus >= 3:
            creationSubmissionLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        if trueItem.itemStatus >= 2:
            creationProgressLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        if trueItem.itemStatus >= 1:
            creationUserAssignmentLabel.pack(side=tk.TOP, fill=tk.X, expand=True)
        if trueItem.itemStatus == 0:
            lazyLabel = tk.Label(labelFrame, text="No progress on this item has been made since creation")
            lazyLabel.pack(side=tk.TOP, fill=tk.X, expand=True)

        numberOfPointsLabel.pack(side=tk.TOP, fill=tk.X, expand=True)

        labelFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.taskAnalyticsContents.pack_forget()
        if len(self.taskAnalyticsContentsOptions) == 1:
            self.taskAnalyticsContentsOptions.append(internalTaskFrame)
        else:
            self.taskAnalyticsContentsOptions[1] = internalTaskFrame
        self.taskAnalyticsContents = self.taskAnalyticsContentsOptions[1]

        self.taskAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.insideTask = True

    def generateTaskGanttChart(self,controller, taskName):
        pointNames = list()
        pointPoints = list()
        beginningPoints = list()
        endingPoints = list()
        statusLabels = list()
        inspectedItem = None
        for item in self.controller.activeProject.listOfAssignedItems:
            if item.itemTitle == taskName:
                inspectedItem = item

        if inspectedItem.itemStatus >= 1:
            beginningPoints.append(int(inspectedItem.itemCreationDate.strftime("%y%m%d")))
            pointNames.append(inspectedItem.itemCreationDate.strftime("%m/%d/%y"))
            pointPoints.append(int(inspectedItem.itemCreationDate.strftime("%y%m%d")))
            endingPoints.append(int(inspectedItem.itemTimeLine["AssignedToUser"].strftime("%y%m%d")))
            pointNames.append(inspectedItem.itemTimeLine["AssignedToUser"].strftime("%m/%d/%y"))
            pointPoints.append(int(inspectedItem.itemTimeLine["AssignedToUser"].strftime("%y%m%d"))
                               + pointPoints[-1])
            statusLabels.append("Assignment")
        if inspectedItem.itemStatus >= 2:
            beginningPoints.append(int(inspectedItem.itemTimeLine["AssignedToUser"].strftime("%y%m%d"))
                                   + pointPoints[-2])
            endingPoints.append(int(inspectedItem.itemTimeLine["WorkStarted"].strftime("%y%m%d")))
            pointNames.append(inspectedItem.itemTimeLine["WorkStarted"].strftime("%m/%d/%y"))
            pointPoints.append(int(inspectedItem.itemTimeLine["WorkStarted"].strftime("%y%m%d"))
                               + pointPoints[-1])
            statusLabels.append("Waiting To Be Started")
        if inspectedItem.itemStatus >= 3:
            beginningPoints.append(int(inspectedItem.itemTimeLine["WorkStarted"].strftime("%y%m%d"))
                                   + pointPoints[-2])
            endingPoints.append(int(inspectedItem.itemTimeLine["Submitted"].strftime("%y%m%d")))
            pointNames.append(inspectedItem.itemTimeLine["Submitted"].strftime("%m/%d/%y"))
            pointPoints.append(int(inspectedItem.itemTimeLine["Submitted"].strftime("%y%m%d"))
                               + pointPoints[-1])
            statusLabels.append("Work")
        if inspectedItem.itemStatus == 4:
            beginningPoints.append(int(inspectedItem.itemTimeLine["Submitted"].strftime("%y%m%d"))
                                   + pointPoints[-2])
            endingPoints.append(int(inspectedItem.itemTimeLine["Completed"].strftime("%y%m%d")))
            pointNames.append(inspectedItem.itemTimeLine["Completed"].strftime("%m/%d/%y"))
            pointPoints.append(int(inspectedItem.itemTimeLine["Completed"].strftime("%y%m%d"))
                               + pointPoints[-1])
            statusLabels.append("Submission")

        #remove duplicates
        prevPoint = 0
        if len(pointPoints) != 0:
            for index, point in enumerate(pointPoints):
                if prevPoint == 0:
                    prevPoint = point
                else:
                    if point == prevPoint:
                        del pointNames[index]
                        del pointPoints[index]

        #remove times too close together
        oldPoint = None
        if len(pointPoints) != 0:
            for index, point in enumerate(pointPoints):
                if oldPoint is None:
                    oldPoint = point
                    continue
                if len(pointPoints) > 2:

                    if int(point - oldPoint) > int((pointPoints[-1]-pointPoints[0])/5): #quarter of difference between start and endpoint
                        oldPoint = point
                    else:
                        del pointNames[index]
                        del pointPoints[index]

        taskGanttChart = ScrumblesFrames.SGantt(controller)
        taskGanttChart.generateGraph(beginningPoints, endingPoints, statusLabels, pointPoints, pointNames,
                                         "Status of Task", "Dates")
        taskGanttChart.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def clearSelection(self, listbox, view):
        if view == 0: #sprint analytics
            self.sprintAnalyticsContentsOptions[1].pack_forget()
            self.sprintAnalyticsContents = self.sprintAnalyticsContentsOptions[0]
            self.sprintAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.insideSprint = False

        if view == 1: #user analytics
            self.userAnalyticsContentsOptions[1].pack_forget()
            self.userAnalyticsContents = self.userAnalyticsContentsOptions[0]
            self.userAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.insideUser = False

        if view == 2: #task analytics
            self.taskAnalyticsContentsOptions[1].pack_forget()
            self.taskAnalyticsContents = self.taskAnalyticsContentsOptions[0]
            self.taskAnalyticsContents.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.insideTask = False

        listbox.selection_clear(0, tk.END)

    def changeSprintGraph(self, isVelocity):
        self.generateInternalSprintFrame(sprintEventName=self.sprintEventName,velocityWanted=isVelocity)

    #utlity function for week/day strings
    def weekOrWeeks(self, weekNumber):
        if weekNumber != 1:
            return "weeks"
        else:
            return "week"

    def dayOrDays(self, dayNumber):
        if dayNumber != 1:
            return "days"
        else:
            return "day"

