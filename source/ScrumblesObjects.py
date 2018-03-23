import hashlib, random, threading, os

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
    listOfAssignedItems = []
    listOfComments = []
    listOfProjects = []

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
    listOfComments = []
    projectID = 0
    statusEquivalents = {1 : "Low Priority", 2 : "Medium Priority", 3 : "High Priority"}

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



    def assignToUser(self, user):
        self.itemUserID = user.userID

    def modifyStatus(self, status):
        self.itemStatus = status

    def modifyPriority(self, priority):
        self.itemPriority = priority

    def getPriority(self):
        return self.statusEquivalents[self.itemPriority]


class Sprint:
    sprintID = None
    sprintStartDate = None
    sprintDueDate = None
    sprintName = None
    projectID = None
    listOfAssignedItems = []
    listOfAssignedUsers = []

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


#todo move assignments to dataBlock
    def assignItemToSprint(self, item):
        item.itemSprintID = self.sprintID
        if item not in self.listOfAssignedItems:
            self.listOfAssignedItems.append(item)

    def removeItemFromSprint(self, item):
        if item in self.listOfAssignedItems:
            item.sprintID = None
            self.listOfAssignedItems.remove(item)
        else:
            raise Exception('Item does not exist in Sprint')

class Comment:
    commentID = None
    commentTimeStamp = None
    commentContent = None
    commentItemID = None
    commentUserID = None
    #todo listOfTags = []

    # Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self, queryResultDict=None):
        if queryResultDict is None:
            self.commentID =  generateRowID()
            return
        assert 'CommentContent' in queryResultDict
        self.commentID = queryResultDict['CommentID']
        self.commentTimeStamp = queryResultDict['CommentTimeStamp']
        self.commentContent = queryResultDict['CommentContent']
        self.commentItemID = queryResultDict['CardID']
        self.commentUserID = queryResultDict['UserID']


class Project:
    projectID = None
    projectName = None
    listOfAssignedSprints = []
    listOfAssignedUsers = []
    listOfAssignedItems = []
    def __init__(self, queryResultDict=None):
        if queryResultDict is None:
            self.projectID = generateRowID()
            return
        assert 'ProjectName' in queryResultDict
        self.projectID = queryResultDict['ProjectID']
        self.projectName = queryResultDict['ProjectName']

#todo class Tag: