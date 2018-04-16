import tkinter as tk
import webbrowser

import csv
import datetime
from data import ScrumblesData
from data import ScrumblesObjects

from frames.SGraphs import *
from frames.SLists import *

from styling import styling as style
from tkinter import ttk

class commentsField(tk.Frame):
    def __init__(self, controller, master):
        tk.Frame.__init__(self, controller, relief = tk.SOLID, borderwidth = 1)

        self.master = master

        self.titleText = tk.StringVar()
        self.titleText.set("Comments")
        self.commentTitleF = tk.Frame(self, relief = tk.SOLID, borderwidth = 1)
        self.commentTitle = tk.Label(self.commentTitleF, textvariable = self.titleText)
        self.commentField = tk.Frame(self)
        self.comments = []
        self.commentTextElements = []

        self.canvas = tk.Canvas(self.commentField, bd = 1, scrollregion = (0,0,1000,1000), height = 100)
        self.scrollbar = tk.Scrollbar(self.commentField, command = self.canvas.yview, cursor = "hand2")
        self.canvas.config(yscrollcommand = self.scrollbar.set)

        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.canvas.pack(expand = True, fill = tk.BOTH)
        self.internals = tk.Frame(self.canvas)
        self.canvasFrame = self.canvas.create_window(0, 0, window = self.internals, anchor = tk.NW)

        self.newCommentFieldF = tk.Frame(self)
        self.newCommentFieldFI = tk.Frame(self.newCommentFieldF)
        self.newCommentField = tk.Text(self.newCommentFieldFI, height = 5)
        self.newCommentFieldScrollBar = tk.Scrollbar(self.newCommentFieldFI, command = self.newCommentField.yview, cursor = "hand2")
        self.newCommentField['yscrollcommand'] = self.newCommentFieldScrollBar.set
        self.submitButton = tk.Button(self.newCommentFieldF, text = "Submit", command = self.submitComment, cursor = "hand2")
        self.newCommentField.bind('<Control-s>', lambda event: self.submitComment(event))
        self.source = None
        self.searchParams = None

        self.commentTitle.pack(side = tk.TOP, fill = tk.X)
        self.commentTitleF.pack(side = tk.TOP, fill = tk.X)
        self.commentField.pack(side = tk.TOP, fill = tk.BOTH, ipady = 4)

        self.newCommentFieldScrollBar.pack(side = tk.RIGHT, fill = tk.Y)
        self.newCommentField.pack(side = tk.LEFT, fill = tk.X, expand = True)
        self.newCommentFieldFI.pack(side = tk.TOP, fill = tk.BOTH)
        self.submitButton.pack(side = tk.TOP, fill = tk.BOTH)

        self.internals.bind("<Configure>", self.OnFrameConfigure)
        self.canvas.bind('<Configure>', self.FrameWidth)

    def submitComment(self, event = None):
        newComment = ScrumblesObjects.Comment()
        newComment.commentContent = self.newCommentField.get("1.0", tk.END)
        newComment.commentContent = str(newComment.commentContent)
        newComment.commentContent = newComment.commentContent.strip()

        newComment.commentTimeStamp = datetime.datetime.now()
        newComment.commentSignature = self.master.activeUser.userName + " " + datetime.datetime.now().strftime("%I:%M %p, %m/%d/%y")
        newComment.commentUserID = self.master.activeUser.userID
        newComment.commentItemID = self.inspection.itemID

        self.newCommentField.delete("1.0", tk.END)
        if newComment.commentContent: #check for empty string
            self.comments.append(newComment)
            self.renderCommentField(initializedComments = True)
            self.master.dataBlock.addNewScrumblesObject(newComment)

    def updateFromListOfCommentsObject(self, source, searchParams, isUpdate = False):
        self.clearCommentField()

        if source is not None and searchParams is not None:
            if isUpdate is False:
                self.source = source
                self.searchParams = searchParams

                self.clearCommentField()
                self.inspection = None
                for thing in source:
                    if thing.getTitle() == searchParams:
                        self.inspection = thing

            else:
                self.inspection = None

                if type(source[0]) is ScrumblesObjects.Item:
                    for user in self.master.activeProject.listOfAssignedUsers:
                        if user.userName == searchParams:
                            self.inspection = user
                if type(source[0] is ScrumblesObjects.User):
                    for item in self.master.activeProject.listOfAssignedItems:
                        if item.itemTitle == searchParams:
                            self.inspection = item

            if self.inspection is not None:
                self.titleText.set("Comments\n" + self.inspection.getTitle())
                for comment in self.inspection.listOfComments:
                    self.comments.append(comment)

            self.renderCommentField()

    def updateComments(self):
        self.updateFromListOfCommentsObject(self.source, self.searchParams, isUpdate = True)

    def renderCommentField(self, initializedComments = False):
        if initializedComments is True:
            for element in self.commentTextElements:
                element.pack_forget()
            self.commentTextElements.clear()

        self.comments = sorted(self.comments, reverse = True, key = lambda s: s.commentTimeStamp)
        for comment in self.comments:
            commentFrame = tk.Frame(self.internals)
            commentLabel = tk.Label(commentFrame, 
                                    anchor = tk.W, 
                                    text = comment.commentContent,
                                    justify = tk.LEFT, 
                                    wraplength = self.master.w_rat*500,
                                    font = style.comment_font)
            if comment.commentSignature is not None:
                commentSignatureLabel = tk.Label(commentFrame, 
                                                 anchor = tk.W, 
                                                 text = comment.commentSignature,
                                                 justify = tk.LEFT, 
                                                 wraplength = self.master.w_rat*500,
                                                 font = style.comment_signature_font)
            else:
                commentUserName = None
                for user in self.master.dataBlock.users:
                    if user.userID == comment.commentUserID:
                        commentUserName = user.userName
                if commentUserName is not None:
                    if type(self.inspection) is ScrumblesObjects.Item:
                        comment.commentSignature = commentUserName + " " + comment.commentTimeStamp.strftime("%I:%M %p, %m/%d/%y")
                    else:
                        for item in self.inspection.listOfAssignedItems:
                            if item.itemID == comment.commentItemID:
                                itemName = item.itemTitle
                                comment.commentSignature = itemName + "\n" + commentUserName + " " + comment.commentTimeStamp.strftime("%I:%M %p, %m/%d/%y")
                    commentSignatureLabel = tk.Label(commentFrame,
                                                     anchor = tk.W, 
                                                     text = comment.commentSignature,
                                                     justify = tk.LEFT, 
                                                     wraplength = self.master.w_rat*500,
                                                     font = style.comment_signature_font)
            self.commentTextElements.append(commentFrame)
            commentLabel.pack(side = tk.TOP, fill = tk.X)
            commentSignatureLabel.pack(side = tk.TOP, fill = tk.X)
            commentFrame.pack(side = tk.TOP, fill = tk.X, pady=10)

        self.commentField.pack(side = tk.TOP, fill = tk.BOTH, expand=True)

        if type(self.inspection) is ScrumblesObjects.Item:
            self.newCommentFieldF.pack_forget()
            self.newCommentFieldF.pack(side = tk.BOTTOM, fill = tk.X)
        else:
            self.newCommentFieldF.pack_forget()

    def clearCommentField(self):
        self.comments.clear()
        self.newCommentField.delete("1.0", tk.END)
        self.commentField.pack_forget()
        for element in self.commentTextElements:
            element.pack_forget()
        self.commentTextElements.clear()

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvasFrame, width = canvas_width)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

class SCardDescription(tk.Frame):
    def __init__(self, controller, master, sources, datatype):
        tk.Frame.__init__(self, controller)
        self.master = master
        self.controller = controller
        self.dataBlock = master.dataBlock
        self.config(relief = tk.SUNKEN, borderwidth = 5)
        self.dataTypeText = datatype[0]

        self.canvas = tk.Canvas(self, bd = 1, scrollregion = (0, 0, 1000, 1000), height = 100)
        self.scrollbar = tk.Scrollbar(self, command = self.canvas.yview, cursor = "hand2")
        self.canvas.config(yscrollcommand = self.scrollbar.set)

        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.canvas.pack(expand = True, fill = tk.BOTH)

        self.internals = tk.Frame(self.canvas)
        self.canvasFrame = self.canvas.create_window(0, 0, window = self.internals, anchor = tk.NW)
        self.titleText = tk.StringVar()
        self.titleText.set(self.dataTypeText + " Description")
        self.title = tk.Label(self.internals,
                              textvariable = self.titleText,
                              font = (style.header_family, style.header_size, style.header_weight))
        self.title.pack(fill = tk.BOTH)
        self.internals.bind("<Configure>", self.OnFrameConfigure)
        self.canvas.bind('<Configure>', self.FrameWidth)
        # Reference datatype with widget code as key, allowing data calls from ScrumblesFrames
        self.datatype = dict((source, table) for source, table in zip(sources, datatype))

        self.cardDescriptions = {}
        self.cardDescriptions['Start'] = self.cardDescriptionStartFrame(self.internals, self.dataTypeText)
        self.cardDescriptions['Item'] = self.cardDescriptionItemFrame(self.internals)
        self.cardDescriptions['User'] = self.cardDescriptionUserFrame(self.internals)
        self.cardDescriptions['Sprint'] = self.cardDescriptionSprintFrame(self.internals)

        self.cardDescriptions['Active'] = self.cardDescriptions['Start']
        self.cardDescriptions['Active'].pack(side = tk.TOP, expand = True, fill = tk.BOTH)

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvasFrame, width = canvas_width)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    class cardDescriptionStartFrame(tk.Frame):
        def __init__(self, controller, dataTypeText):
            tk.Frame.__init__(self, controller)
            tk.helpMeLabel = tk.Label(self, text = "Click on any " + dataTypeText.lower() + " to obtain information about it!")
            tk.helpMeLabel.pack()

    class cardDescriptionItemFrame(tk.Frame):
        def __init__(self, controller):
            tk.Frame.__init__(self, controller)

            self.itemTypeF = tk.Frame(self)
            self.itemTypeT = tk.Label(self.itemTypeF, text = "Type: ")
            self.itemType = tk.Label(self.itemTypeF, text = "")

            self.itemPriorityF = tk.Frame(self)
            self.itemPriorityT = tk.Label(self.itemPriorityF, text = "Priority: ")
            self.itemPriority = tk.Label(self.itemPriorityF, text = "")

            self.itemDueDateF = tk.Frame(self)
            self.itemDueDateT = tk.Label(self.itemDueDateF, text = "Due Date: ")
            self.itemDueDate = tk.Label(self.itemDueDateF, text = "")

            self.itemStatusF = tk.Frame(self)
            self.itemStatusT = tk.Label(self.itemStatusF, text = "Status: ")
            self.itemStatus = tk.Label(self.itemStatusF, text = "")

            self.itemUserF = tk.Frame(self)
            self.itemUserT = tk.Label(self.itemUserF, text = "Assigned Users: ")
            self.itemUser = tk.Label(self.itemUserF, text = "")

            self.itemSprintF = tk.Frame(self)
            self.itemSprintT = tk.Label(self.itemSprintF, text = "Assigned Sprint:")
            self.itemSprint = tk.Label(self.itemSprintF, text = "")

            self.itemDescriptionF = tk.Frame(self)
            self.itemDescriptionT = tk.Label(self.itemDescriptionF, text = "Description: ")
            self.itemDescription = tk.Label(self.itemDescriptionF, text = "")

            self.itemCodeLinkF = tk.Frame(self)
            self.itemCodeLinkT = tk.Label(self.itemCodeLinkF, text = 'Link to Code: ')
            self.itemCodeLink = tk.Label(self.itemCodeLinkF, text = "")

            self.itemTypeT.pack(side = tk.LEFT, fill = tk.X)
            self.itemType.pack(side = tk.LEFT, fill = tk.X)
            self.itemPriorityT.pack(side = tk.LEFT, fill = tk.X)
            self.itemPriority.pack(side = tk.LEFT, fill = tk.X)
            self.itemDueDateT.pack(side = tk.LEFT, fill = tk.X)
            self.itemDueDate.pack(side = tk.LEFT, fill = tk.X)
            self.itemStatusT.pack(side = tk.LEFT, fill = tk.X)
            self.itemStatus.pack(side = tk.LEFT, fill = tk.X)
            self.itemUserT.pack(side = tk.LEFT, fill = tk.X)
            self.itemUser.pack(side = tk.LEFT, fill = tk.X)
            self.itemSprintT.pack(side = tk.LEFT, fill = tk.X)
            self.itemSprint.pack(side = tk.LEFT, fill = tk.X)
            self.itemDescriptionT.pack(side = tk.LEFT, fill = tk.X)
            self.itemDescription.pack(side = tk.LEFT, fill = tk.X)
            self.itemCodeLinkT.pack(side = tk.LEFT, fill = tk.X)
            self.itemCodeLink.pack(side = tk.LEFT, fill = tk.X)

            self.itemTypeF.pack(side = tk.TOP, fill = tk.X)
            self.itemPriorityF.pack(side = tk.TOP, fill = tk.X)
            self.itemDueDateF.pack(side = tk.TOP, fill = tk.X)
            self.itemStatusF.pack(side = tk.TOP, fill = tk.X)
            self.itemUserF.pack(side = tk.TOP, fill = tk.X)
            self.itemSprintF.pack(side = tk.TOP, fill = tk.X)
            self.itemDescriptionF.pack(side = tk.TOP, fill = tk.X)
            self.itemCodeLinkF.pack(side = tk.TOP, fill = tk.X)

        def repack(self):
            self.itemTypeT.pack_forget()
            self.itemType.pack_forget()
            self.itemPriorityT.pack_forget()
            self.itemPriority.pack_forget()
            self.itemDueDateT.pack_forget()
            self.itemDueDate.pack_forget()
            self.itemStatusT.pack_forget()
            self.itemStatus.pack_forget()
            self.itemDescriptionT.pack_forget()
            self.itemDescription.pack_forget()
            self.itemUserT.pack_forget()
            self.itemUser.pack_forget()
            self.itemSprintT.pack_forget()
            self.itemSprint.pack_forget()
            self.itemCodeLink.pack_forget()
            self.itemCodeLinkT.pack_forget()

            self.itemTypeF.pack_forget()
            self.itemPriorityF.pack_forget()
            self.itemDueDateF.pack_forget()
            self.itemStatusF.pack_forget()
            self.itemDescriptionF.pack_forget()
            self.itemUserF.pack_forget()
            self.itemSprintF.pack_forget()
            self.itemCodeLinkF.pack_forget()

            self.itemTypeT.pack(side = tk.LEFT, fill = tk.X)
            self.itemType.pack(side = tk.LEFT, fill = tk.X)
            self.itemPriorityT.pack(side = tk.LEFT, fill = tk.X)
            self.itemPriority.pack(side = tk.LEFT, fill = tk.X)
            self.itemDueDateT.pack(side = tk.LEFT, fill = tk.X)
            self.itemDueDate.pack(side = tk.LEFT, fill = tk.X)
            self.itemStatusT.pack(side = tk.LEFT, fill = tk.X)
            self.itemStatus.pack(side = tk.LEFT, fill = tk.X)
            self.itemUserT.pack(side = tk.LEFT, fill = tk.X)
            self.itemUser.pack(side = tk.LEFT, fill = tk.X)
            self.itemSprintT.pack(side = tk.LEFT, fill = tk.X)
            self.itemSprint.pack(side = tk.LEFT, fill = tk.X)
            self.itemDescriptionT.pack(side = tk.LEFT, fill = tk.X)
            self.itemDescription.pack(side = tk.LEFT, fill = tk.X)
            self.itemCodeLinkT.pack(side = tk.LEFT, fill = tk.X)
            self.itemCodeLink.pack(side = tk.LEFT, fill = tk.X)

            self.itemTypeF.pack(side = tk.TOP, fill = tk.X)
            self.itemPriorityF.pack(side = tk.TOP, fill = tk.X)
            self.itemDueDateF.pack(side = tk.TOP, fill = tk.X)
            self.itemStatusF.pack(side = tk.TOP, fill = tk.X)
            self.itemUserF.pack(side = tk.TOP, fill = tk.X)
            self.itemSprintF.pack(side = tk.TOP, fill = tk.X)
            self.itemDescriptionF.pack(side = tk.TOP, fill = tk.X)
            self.itemCodeLinkF.pack(side = tk.TOP, fill = tk.X)

    class cardDescriptionUserFrame(tk.Frame):
        def __init__(self, controller):
            tk.Frame.__init__(self, controller)

            self.userRoleF = tk.Frame(self)
            self.userRoleT = tk.Label(self.userRoleF, text = "Role: ")
            self.userRole = tk.Label(self.userRoleF, text = "")

            self.userEmailF = tk.Frame(self)
            self.userEmailT = tk.Label(self.userEmailF, text = "Email: ")
            self.userEmail = tk.Label(self.userEmailF, text = "")

            self.userRoleT.pack(side = tk.LEFT)
            self.userRole.pack(side = tk.LEFT)
            self.userEmailT.pack(side = tk.LEFT)
            self.userEmail.pack(side = tk.LEFT)

            self.userRoleF.pack(side = tk.TOP)
            self.userEmailF.pack(side = tk.TOP)

        def repack(self):
            self.userRoleT.pack_forget()
            self.userRole.pack_forget()
            self.userEmailT.pack_forget()
            self.userEmail.pack_forget()

            self.userRoleF.pack_forget()
            self.userEmailF.pack_forget()

            self.userRoleT.pack(side = tk.LEFT)
            self.userRole.pack(side = tk.LEFT)
            self.userEmailT.pack(side = tk.LEFT)
            self.userEmail.pack(side = tk.LEFT)

            self.userRoleF.pack(side = tk.TOP)
            self.userEmailF.pack(side = tk.TOP)

    class cardDescriptionSprintFrame(tk.Frame):
        def __init__(self, controller):
            tk.Frame.__init__(self, controller)
            self.sprintStartF = tk.Frame(self)
            self.sprintStartT = tk.Label(self.sprintStartF, text = "Start Date: ")
            self.sprintStart = tk.Label(self.sprintStartF, text = "")

            self.sprintDueF = tk.Frame(self)
            self.sprintDueT = tk.Label(self.sprintDueF, text = "Due Date: ")
            self.sprintDue = tk.Label(self.sprintDueF, text = "")

            # progress bar
            s = ttk.Style()
            s.theme_use('clam')
            s.configure("scrumbles.Horizontal.TProgressbar",
                        troughcolor = 'gray',
                        background = style.scrumbles_green_fg)

            progressBarStyle = "scrumbles.Horizontal.TProgressbar"

            self.sprintProgressBar = ttk.Progressbar(self,
                                                     style = progressBarStyle,
                                                     length = 200,
                                                     orient = "horizontal",
                                                     mode = "determinate")

            self.sprintStartT.pack(side = tk.LEFT)
            self.sprintStart.pack(side = tk.LEFT)
            self.sprintDueT.pack(side = tk.LEFT)
            self.sprintDue.pack(side = tk.LEFT)

            self.sprintStartF.pack(side = tk.TOP)
            self.sprintDueF.pack(side = tk.TOP)
            self.sprintProgressBar.pack(side = tk.TOP)

        def repack(self):
            self.sprintStartT.pack_forget()
            self.sprintStart.pack_forget()
            self.sprintDueT.pack_forget()
            self.sprintDue.pack_forget()

            self.sprintStartF.pack_forget()
            self.sprintDueF.pack_forget()
            self.sprintProgressBar.pack_forget()

            self.sprintStartT.pack(side = tk.LEFT)
            self.sprintStart.pack(side = tk.LEFT)
            self.sprintDueT.pack(side = tk.LEFT)
            self.sprintDue.pack(side = tk.LEFT)

            self.sprintStartF.pack(side = tk.TOP)
            self.sprintDueF.pack(side = tk.TOP)
            self.sprintProgressBar.pack(side = tk.TOP)

    def repack(self):
        self.title.pack(fill = tk.X)
        self.cardDescriptions['Active'].pack(side = tk.TOP, expand = True, fill = tk.BOTH)
        self.canvas.pack_forget()
        self.canvas.pack(side = tk.TOP, expand = True, fill = tk.BOTH)

    def changeDescription(self, event):
        widget = event.widget
        self.eventSetTitle(widget)
        self.generateAdditionalFields(widget)
        self.repack()

    def setTitle(self, title):
        self.titleText.set(title)

    def eventSetTitle(self, widget):
        selection = widget.get(tk.ANCHOR)
        self.setTitle(selection)

    def generateAdditionalFields(self, widget):
        match = None

        if self.datatype[widget] == 'User':
            for user in self.dataBlock.users:
                if user.userName == widget.get(tk.ANCHOR):
                    match = user
            #If ListBox Select Isn't Properly Handled
            if match is None:
                self.resetToStart()
            else:
                self.generateUserFields(match)

        if self.datatype[widget] == 'Item':
            for item in self.dataBlock.items:
                if item.itemTitle == widget.get(tk.ANCHOR):
                    match = item
            # If ListBox Select Isn't Properly Handled
            if match is None:
                self.resetToStart()
            else:
                self.generateItemFields(match)

        if self.datatype[widget] == 'Sprint':
            for sprint in self.dataBlock.sprints:
                if sprint.sprintName == widget.get(tk.ANCHOR):
                    match = sprint
            if match is None:
                self.resetToStart()
            else:
                self.generateSprintFields(match)

    def generateUserFields(self, selectedUser):
        self.cardDescriptions["User"].userRole.configure(text = selectedUser.userRole,
                                                         justify = tk.LEFT,
                                                         wraplength = self.master.w_rat*300)
        self.cardDescriptions["User"].userEmail.configure(text = selectedUser.userEmailAddress,
                                                          justify = tk.LEFT,
                                                          wraplength = self.master.w_rat*300)
        self.cardDescriptions["User"].repack()
        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions["User"]

    def generateItemFields(self, selectedItem):
        self.cardDescriptions["Item"].itemType.configure(text = selectedItem.itemType,
                                                         justify = tk.LEFT,
                                                         wraplength = self.master.w_rat*300)
        if selectedItem.itemPriority is not None:
            self.cardDescriptions["Item"].itemPriority.configure(text = selectedItem.getPriorityString(),
                                                                 justify = tk.LEFT,
                                                                 wraplength = self.master.w_rat*300)
        else:
            self.cardDescriptions["Item"].itemPriority.configure(text = selectedItem.itemPriority,
                                                                 justify = tk.LEFT,
                                                                 wraplength = self.master.w_rat*300)
        if selectedItem.itemDueDate is not None:
            self.cardDescriptions["Item"].itemDueDate.configure(text = selectedItem.getFormattedDueDate(),
                                                                justify = tk.LEFT,
                                                                wraplength = self.master.w_rat*300)
        else:
            self.cardDescriptions["Item"].itemDueDate.configure(text = selectedItem.itemDueDate,
                                                                justify = tk.LEFT,
                                                                wraplength = self.master.w_rat*300)

        self.cardDescriptions["Item"].itemStatus.configure(text = selectedItem.getStatus(),
                                                           justify = tk.LEFT,
                                                           wraplength = self.master.w_rat*300)
        self.cardDescriptions["Item"].itemDescription.configure(text = selectedItem.itemDescription,
                                                                justify = tk.LEFT,
                                                                wraplength = self.master.w_rat*300)

        if selectedItem.itemCodeLink is not None and selectedItem.itemCodeLink != '':
            self.cardDescriptions["Item"].itemCodeLink.configure(text = selectedItem.itemCodeLink,
                                                                 justify = tk.LEFT,
                                                                 wraplength = self.master.w_rat*300,
                                                                 fg = 'blue',
                                                                 underline = 1,
                                                                 cursor = 'gumby')
            self.cardDescriptions["Item"].itemCodeLink.bind('<Button-1>', lambda event: self.open(event))
        else:
            self.cardDescriptions["Item"].itemCodeLink.configure(text = u'None Set',
                                                                 justify = tk.LEFT,
                                                                 wraplength = self.master.w_rat*300,
                                                                 fg = 'red',
                                                                 underline = -1,
                                                                 cursor = 'X_cursor')
            
            self.cardDescriptions['Item'].itemCodeLink.unbind('<Button 1>')

        sprintName = ""
        for sprint in self.master.dataBlock.sprints:
            if sprint.sprintID == selectedItem.itemSprintID:
                sprintName = sprint.sprintName
        self.cardDescriptions["Item"].itemSprint.configure(text = sprintName,
                                                           justify = tk.LEFT,
                                                           wraplength = self.master.w_rat*300)

        userName = ""
        for user in self.master.dataBlock.users:
            if user.userID == selectedItem.itemUserID:
                userName = user.userName
        self.cardDescriptions["Item"].itemUser.configure(text = userName,
                                                         justify = tk.LEFT,
                                                         wraplength = self.master.w_rat*300)
        self.cardDescriptions["Item"].repack()

        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions["Item"]

    def generateSprintFields(self, selectedSprint):
        self.cardDescriptions["Sprint"].sprintStart.configure(text = selectedSprint.getFormattedStartDate(),
                                                              justify = tk.LEFT,
                                                              wraplength = self.master.w_rat*300)
        self.cardDescriptions["Sprint"].sprintDue.configure(text = selectedSprint.getFormattedDueDate(),
                                                            justify = tk.LEFT,
                                                            wraplength = self.master.w_rat*300)
        self.completedTasks = 0
        for item in selectedSprint.listOfAssignedItems:
            if item.itemStatus == 4:
                self.completedTasks += 1
        self.cardDescriptions["Sprint"].sprintProgressBar["value"] = self.completedTasks
        self.cardDescriptions["Sprint"].sprintProgressBar["maximum"] = len(selectedSprint.listOfAssignedItems)

        self.cardDescriptions["Sprint"].repack()

        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions["Sprint"]

    def resetToStart(self):
        self.titleText.set("Item Description")
        self.cardDescriptions["Active"].pack_forget()
        self.cardDescriptions["Active"] = self.cardDescriptions['Start']
        self.cardDescriptions['Active'].pack(side = tk.TOP)

    def open(self, event):
        link = event.widget.cget('text')

        webbrowser.open(link)

class SUserItemInspection(tk.Frame):

    def __init__(self, controller, master):
        tk.Frame.__init__(self, controller)
        self.master = master
        self.controller = controller
        self.dataBlock = self.master.dataBlock

        self.textBox = tk.Frame(self)

        self.nameTag = tk.Frame(self.textBox, relief = tk.SOLID, borderwidth = 1)
        self.nameLabel = tk.Label(self.nameTag, text ="Name")
        self.nameString = tk.StringVar()
        self.nameText = tk.Label(self.nameTag, textvariable = self.nameString, cursor ="hand2")

        self.roleTag = tk.Frame(self.textBox, relief = tk.SOLID, borderwidth = 1)
        self.roleLabel = tk.Label(self.roleTag, text ="Role")
        self.roleString = tk.StringVar()
        self.roleText = tk.Label(self.roleTag, textvariable = self.roleString, cursor ="hand2")

        self.itemBox = tk.Frame(self)
        self.assignedItemsList = SList(self.itemBox, "Assigned Items")
        self.inProgressItemsList = SList(self.itemBox, "In Progress Items")
        self.submittedItemsList = SList(self.itemBox, "Submitted Items")
        self.completedItemsList = SList(self.itemBox, "Completed Items")

        self.nameLabel.pack(fill = tk.X)
        self.nameText.pack(fill = tk.X)
        self.roleLabel.pack(fill = tk.X)
        self.roleText.pack(fill = tk.X)

        self.nameTag.pack(side = tk.LEFT, fill = tk.X, expand = 1)
        self.roleTag.pack(side = tk.LEFT, fill = tk.X, expand = 1)

        self.assignedItemsList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.inProgressItemsList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.submittedItemsList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.completedItemsList.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        self.textBox.pack(side = tk.TOP, fill = tk.X)
        self.itemBox.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

    def update(self, user):
        self.nameString.set(user.userName)
        self.roleString.set(user.userRole)
        self.updateItems(user.listOfAssignedItems)

    def updateItems(self, items):
        assignedItems = []
        inProgressItems = []
        submittedItems = []
        completedItems = []
        for item in items:
            if item.projectID == self.master.activeProject.projectID:
                if item.itemStatus == 1:
                    assignedItems.append(item)
                if item.itemStatus == 2:
                    inProgressItems.append(item)
                if item.itemStatus == 3:
                    submittedItems.append(item)
                if item.itemStatus == 4:
                    completedItems.append(item)

        self.updateAssignedItems(assignedItems)
        self.updateInProgressItems(inProgressItems)
        self.updateSubmittedItems(submittedItems)
        self.updateCompletedItems(completedItems)

    def updateAssignedItems(self, assignedItems):
        self.assignedItemsList.importItemList(assignedItems)

    def updateInProgressItems(self, inProgressItems):
        self.inProgressItemsList.importItemList(inProgressItems)

    def updateSubmittedItems(self, submittedItems):
        self.submittedItemsList.importItemList(submittedItems)

    def updateCompletedItems(self, completedItems):
        self.completedItemsList.importItemList(completedItems)

    def getSCardDescriptionExport(self):
        return [self.assignedItemsList.listbox, 
                self.inProgressItemsList.listbox, 
                self.submittedItemsList.listbox, 
                self.completedItemsList.listbox], \
               ['Item', 'Item', 'Item', 'Item']

class STabs(tk.Frame):
    def __init__(self, controller, master, viewName):
        tk.Frame.__init__(self, controller)
        self.master = master
        self.controller = controller
        self.viewName = viewName
        self.buttonList = []
        self.generateButtons()

    class viewButton(tk.Button):
        def __init__(self, controller, viewName, view, event):
            if viewName == controller.viewName:
                tk.Button.__init__(self, 
                                   controller, 
                                   text = str(viewName), 
                                   command = lambda: event(view), 
                                   bg = style.scrumbles_offwhite, 
                                   relief = tk.SOLID, 
                                   borderwidth = 1, 
                                   cursor = "hand2")
            else:
                tk.Button.__init__(self, 
                                   controller, 
                                   text = str(viewName), 
                                   command = lambda: event(view), 
                                   bg = style.scrumbles_grey, 
                                   relief = tk.SOLID, 
                                   borderwidth = 1, 
                                   cursor = "hand2")

    def generateButtons(self):
        self.buttonList.clear()
        views, viewNames = self.master.getViews()
        
        for view, viewName in zip(views, viewNames):
            if viewName == "Team Manager" and self.master.activeUser.userRole != "Admin":
                continue
            else:
                viewButton = self.viewButton(self, viewName, view, self.tabEvent)
                self.buttonList.append(viewButton)
                viewButton.pack(side = tk.LEFT)

    def tabEvent(self, selectedView):
        self.master.show_frame(selectedView)
