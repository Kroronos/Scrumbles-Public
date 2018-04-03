import hashlib, random, threading, os
from datetime import datetime

#Thread local storage
thread_local = threading.local()


#Row ID Range; with highest bit always set
ID_RANGE = (2**62,2**63)

def generateRowID():

    try:
        thread_local_random = thread_local.random
    except AttributeError:
        thread_local_random = _init_thread_local_random()

    return thread_local_random.randrange(*ID_RANGE)

def _init_thread_local_random():
    rng = random.SystemRandom()
    hash_object = hashlib.sha1(hex(os.getpid()).encode())
    hash_object.update(hex(rng.randrange(*ID_RANGE)).encode())
    seed = int(hash_object.hexdigest(), 16)

    thread_local.random = random.Random(seed)

    return thread_local.random

class User:
    userName = None
    userEmailAddress = None
    userID = None
    userRole = None


    #Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self, queryResultDict=None):
        if queryResultDict is None:
            self.userID = generateRowID()
            return
        assert 'UserName' in queryResultDict

        self.userName = queryResultDict['UserName']
        self.userEmailAddress = queryResultDict['UserEmailAddress']
        self.userPassword = queryResultDict['UserPassword']
        self.userRole = queryResultDict['UserRole']
        self.userID = queryResultDict['UserID']
        self.listOfAssignedItems = []
        self.listOfComments = []
        self.listOfProjects = []

    def getTitle(self):
        return self.userName

class Item:
    itemID = None
    itemType = None
    itemPriority = None
    itemTitle = None
    itemDescription = None
    itemCreationDate = None
    itemDueDate = None
    itemCodeLink = None
    itemSprintID = None
    itemUserID = None
    itemStatus = None
    itemTimeLine = None

    priorityNumberToTextMap = {0: "Low Priority", 1: "Medium Priority", 2: "High Priority"}
    priorityTextToNumberMap = {"Low Priority":0, "Medium Priority":1, "High Priority":2}
    statusNumberToTextMap = {0 : 'Not Assigned', 1: 'Assigned', 2: 'In Progress', 3: 'Submitted', 4: 'Complete'}
    statusTextToNumberMap = {'Not Assigned': 0, 'Assigned': 1, 'In Progress': 2, 'Submitted': 3, 'Complete': 4}
    validItemTypes = ('User Story', 'Epic', 'Bug', 'Chore', 'Feature')
    # Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self,queryResultDict=None):
        if queryResultDict is None:
            self.itemID = generateRowID()
            return
        assert 'CardType' in queryResultDict
        self.itemID = queryResultDict['CardID']
        self.itemType = queryResultDict['CardType']
        self.itemPriority = queryResultDict['CardPriority']
        self.itemTitle = queryResultDict['CardTitle']
        self.itemDescription = queryResultDict['CardDescription']
        self.itemCreationDate = queryResultDict['CardCreatedDate']
        self.itemDueDate = queryResultDict['CardDueDate']
        self.itemCodeLink = queryResultDict['CardCodeLink']
        self.itemSprintID = queryResultDict['SprintID']
        self.itemUserID = queryResultDict['UserID']
        self.itemStatus = queryResultDict['Status']
        self.itemPoints = queryResultDict['CardPoints']
        #todo find every reference to the two lines below and refactor using the static dictionaries defined above
        self.listOfStatuses = self.statusNumberToTextMap
        self.listOfPriorities = self.priorityNumberToTextMap

        #DataBlock will update timeline with values from the database
        maxDate = datetime(9999, 12, 31, 23, 59, 59)
        self.itemTimeLine = {'AssignedToSprint':maxDate , 'AssignedToUser':maxDate, 'WorkStarted':maxDate,'Submitted':maxDate,'Completed':maxDate}
        self.listOfComments = []
        self.subItemList = []
        self.projectID = 0

    def getPriority(self):
        return self.itemPriority

    def getPriorityString(self):
        return Item.priorityNumberToTextMap[self.itemPriority]

    def getEnglishPriority(self):
        if self.itemPriority in range(0,3):
            return self.listOfPriorities[self.itemPriority]
        else:
            raise Exception("Invalid Priority Value")
    def getEnglishStatus(self):
        if self.itemStatus in range(0,5):
            return self.listOfStatuses[self.itemStatus]
        else:
           raise Exception("Invalid Status Value")
    def getDescription(self):
        return self.itemDescription

    def getTitle(self):
        return self.itemTitle

    def getStatus(self):
        return Item.statusNumberToTextMap[self.itemStatus]

    def getType(self):
        return self.itemType

    def getFormattedDueDate(self):
        return self.itemDueDate.strftime("%I:%M %p, %m/%d/%y")

    def getFormattedCreationDate(self):
        return self.itemCreationDate.strftime("%I:%M %p, %m/%d/%y")


class Sprint:
    sprintID = None
    sprintStartDate = None
    sprintDueDate = None
    sprintName = None
    projectID = None

    def getFormattedDueDate(self):
        return self.sprintDueDate.strftime("%I:%M %p, %m/%d/%y")

    def getFormattedStartDate(self):
        return self.sprintStartDate.strftime("%I:%M %p, %m/%d/%y")


    # Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self,queryResultDict=None):
        if queryResultDict is None:
            self.sprintID = generateRowID()
            return
        assert 'SprintName' in queryResultDict
        self.sprintID = queryResultDict['SprintID']
        self.sprintStartDate = queryResultDict['StartDate']
        self.sprintDueDate = queryResultDict['DueDate']
        self.sprintName = queryResultDict['SprintName']
        self.projectID = queryResultDict['ProjectID']
        self.listOfAssignedItems = []
        self.listOfAssignedUsers = []

class Comment:

    #todo listOfTags = []

    # Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self, queryResultDict=None):
        if queryResultDict is None:
            self.commentID = generateRowID()
            return
        assert 'CommentContent' in queryResultDict
        self.commentID = queryResultDict['CommentID']
        self.commentTimeStamp = queryResultDict['CommentTimeStamp']
        self.commentContent = queryResultDict['CommentContent']
        self.commentItemID = queryResultDict['CardID']
        self.commentUserID = queryResultDict['UserID']
        self.commentSignature = None


class Project:
    projectID = None
    projectName = None

    def __init__(self, queryResultDict=None):
        if queryResultDict is None:
            self.projectID = generateRowID()
            return
        assert 'ProjectName' in queryResultDict
        self.projectID = queryResultDict['ProjectID']
        self.projectName = queryResultDict['ProjectName']
        self.listOfAssignedSprints = []
        self.listOfAssignedUsers = []
        self.listOfAssignedItems = []

#todo implement class tag: