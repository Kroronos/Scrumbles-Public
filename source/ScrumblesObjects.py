
class User:
    userName = None
    userEmailAddress = None
    userID = None
    userRole = None
    listOfAssignedItems = []
    

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

    def assignItemToSprint(self, item):
        item.itemSprintID = self.sprintID
        if item not in listOfAssignedItems:
            listOfAssignedItems.append(item)

    def removeItemFromSprint(self, item):
        if item in listOfAssignedItems:
            item.sprintID = None
            listOfAssignedItems.remove(item)
        else:
            raise Exception('Item does not exist in Sprint')

class Comment:
    commentID = None
    commentTimeStamp = None
    commentContent = None
    commentCardID = None
    commentUserID = None

    
