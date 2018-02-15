
class User:
    userName = None
    userEmailAddress = None
    userID = None
    userRole = None
    listOfAssignedItemID = []

    #Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self, queryResultDict=None):
        if queryResultDict is None:
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

    # Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self,queryResultDict=None):
        if queryResultDict is None:
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

    def addComment(self, comment):
        self.listOfComments.append(comment)


class Sprint:
    sprintID = None
    sprintStartDate = None
    sprintDueDate = None
    sprintName = None
    listOfAssignedItems = []

    # Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self,queryResultDict=None):
        if queryResultDict is None:
            return
        assert 'SprintName' in queryResultDict
        self.sprintID = queryResultDict['SprintID']
        self.sprintStartDate = queryResultDict['StartDate']
        self.sprintDueDate = queryResultDict['DueDate']
        self.sprintName = queryResultDict['SprintName']

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
    commentCardID = None
    commentUserID = None

    # Note: ScrumblesData.getData() returns a LIST of DICTS
    # This initializer accepts a DICT not a List
    def __init__(self, queryResultDict=None):
        if queryResultDict is None:
            return
        assert 'CommentContent' in queryResultDict
        self.commentID = queryResultDict['CommentID']
        self.commentTimeStamp = queryResultDict['CommentTimeStamp']
        self.commentContent = queryResultDict['CommentContent']
        self.commentCardID = queryResultDict['CardID']
        self.commentUserID = queryResultDict['UserID']
