
class User:
    userName = None
    userEmailAddress = None
    userID = None
    userRole = None

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

    def assignToUser(self,user):
        self.itemUserID = user.userID

    def assignToSprint(self,sprint):
        self.itemSprintID = sprint.sprintID
        self.itemDueDate = sprint.sprintDueDate

    def modifyStatus(self, status):
        self.itemStatus = status

    def modifyPriority(self, priority):
        self.itemPriority = priority

class Sprint:
    sprintID = None
    sprintStartDate = None
    sprintDueDate = None
    sprintName = None

class Comment:
    commentID = None
    commentTimeStamp = None
    commentContent = None
    commentCardID = None
    commentUserID = None

    
