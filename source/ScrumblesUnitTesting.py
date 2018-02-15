import ScrumblesData
import ScrumblesObjects
import datetime

ScrumblesUser_username = 'TestUser'
ScrumblesUser_password = 'PASSWORD'

def deleteUserQuery(user):
    assert user is not None
    query = 'DELETE FROM UserTable WHERE UserID=%i' % (user.userID)
    return query

def deleteCommentQuery(comment):
    assert comment is not None
    query = 'DELETE FROM CommentTable WHERE CommentID=%i' % (comment.commentID)
    return query

def deleteSprintQuery(sprint):
    assert sprint is not None
    query = 'DELETE FROM SprintTable WHERE SprintID=%i' % (sprint.sprintID)
    return query

def deleteCardQuery(item):
    assert item is not None
    query = 'DELETE FROM CardTable WHERE CardID=%i' % (item.itemID)
    return query

def deleteObjectQuery(obj):
    query = ''
    if type(obj) == ScrumblesObjects.User:
        query = deleteUserQuery(obj)
    elif type(obj) == ScrumblesObjects.Comment:
        query = deleteCommentQuery(obj)
    elif type(obj) == ScrumblesObjects.Sprint:
        query = deleteSprintQuery(obj)
    elif type(obj) == ScrumblesObjects.Item:
        query = deleteCardQuery(obj)
    else:
        raise Exception('Invalid Object Type')
    return query

dbLoginInfo = ScrumblesData.DataBaseLoginInfo()
dbLoginInfo.userID = 'test_user'
dbLoginInfo.password = 'testPassword'
dbLoginInfo.ipaddress = '173.230.136.241'
dbLoginInfo.defaultDB = 'test'

dataConnection = ScrumblesData.ScrumblesData(dbLoginInfo)
dataConnection.connect()

getAllUsersQuery = ScrumblesData.Query.getAllUsers
getAllSprintsQuery = ScrumblesData.Query.getAllSprints
getAllItemsQuery = ScrumblesData.Query.getAllCards
getAllCommentsQuery = ScrumblesData.Query.getAllComments


## Test retrieval of Remote SQL Data
allUsersQueryResult = dataConnection.getData(getAllUsersQuery)
allSprintsQueryResult = dataConnection.getData(getAllSprintsQuery)
allItemsQueryResult = dataConnection.getData(getAllItemsQuery)
allCommentsQueryResult = dataConnection.getData(getAllCommentsQuery)

dataConnection.close()

assert len(allUsersQueryResult) > 0
assert len(allSprintsQueryResult) > 0
assert len(allItemsQueryResult) > 0
assert len(allCommentsQueryResult) > 0

listOfUsers = []
listOfSprints = []
listOfItems = []
listOfComments = []

## Test construction of Objects from Query Results
for element in allUsersQueryResult:
    assert len(element) == 5
    assert 'UserID' in element
    assert 'UserName' in element
    assert 'UserEmailAddress' in element
    assert 'UserPassword' in element
    assert 'UserRole' in element
    user = ScrumblesObjects.User(element)
    assert user.userID == element['UserID']
    assert user.userName == element['UserName']
    assert user.userEmailAddress == element['UserEmailAddress']
    assert user.userPassword == element['UserPassword']
    assert user.userRole == element['UserRole']
    listOfUsers.append(user)
assert len(listOfUsers) == len(allUsersQueryResult)

for element in allSprintsQueryResult:
    assert len(element) == 4
    assert 'SprintID' in element
    assert 'StartDate' in element
    assert 'DueDate' in element
    assert 'SprintName' in element
    sprint = ScrumblesObjects.Sprint(element)
    assert sprint.sprintID == element['SprintID']
    assert sprint.sprintStartDate == element['StartDate']
    assert sprint.sprintDueDate == element['DueDate']
    assert sprint.sprintName == element['SprintName']
    listOfSprints.append(sprint)
assert len(listOfSprints) == len(allSprintsQueryResult)

for element in allItemsQueryResult:
    assert len(element) == 11
    assert 'CardID' in element
    assert 'CardType' in element
    assert 'CardPriority' in element
    assert 'CardTitle' in element
    assert 'CardDescription' in element
    assert 'CardCreatedDate' in element
    assert 'CardDueDate' in element
    assert 'CardCodeLink' in element
    assert 'SprintID' in element
    assert 'UserID' in element
    assert 'Status' in element
    item = ScrumblesObjects.Item(element)
    assert item.itemID == element['CardID']
    assert item.itemType == element['CardType']
    assert item.itemPriority == element['CardPriority']
    assert item.itemTitle == element['CardTitle']
    assert item.itemDescription == element['CardDescription']
    assert item.itemCreationDate == element['CardCreatedDate']
    assert item.itemDueDate == element['CardDueDate']
    assert item.itemCodeLink == element['CardCodeLink']
    assert item.itemSprintID == element['SprintID']
    assert item.itemUserID == element['UserID']
    assert item.itemStatus == element['Status']
    listOfItems.append(item)
assert len(listOfItems) == len(allItemsQueryResult)

for element in allCommentsQueryResult:
    assert len(element) == 5
    assert 'CommentID' in element
    assert 'CommentTimeStamp' in element
    assert 'CommentContent' in element
    assert 'CardID' in element
    assert 'UserID' in element
    comment = ScrumblesObjects.Comment(element)
    assert comment.commentID == element['CommentID']
    assert comment.commentTimeStamp == element['CommentTimeStamp']
    assert comment.commentContent == element['CommentContent']
    assert comment.commentItemID == element['CardID']
    assert comment.commentUserID == element['UserID']
    listOfComments.append(comment)
assert len(listOfComments) == len(allCommentsQueryResult)

## Test Authentication Query
dataConnection.connect()
authUserQuery = ScrumblesData.Query.getUserIdByUsernameAndPassword(ScrumblesUser_username,ScrumblesUser_password)
authUserQueryResult = dataConnection.getData(authUserQuery)
authUser = ScrumblesObjects.User(authUserQueryResult[0])
dataConnection.close()
assert authUser.userName == ScrumblesUser_username


## Test Item Creation
testItem = ScrumblesObjects.Item()
testItem.itemType = 'UNIT_TEST_2'
testItem.itemTitle = 'UNIT_TEST_2'
testItem.itemDescription = 'UNIT TESTING ITEM CREATION, previous test failed to delete'
testItemCreationQuery = ScrumblesData.CardQuery.createCard(testItem)

dataConnection.connect()
dataConnection.setData(testItemCreationQuery)

testItemSearchQuery = ScrumblesData.CardQuery.getCardByCardTitle(testItem.itemTitle)
testItemSearchResult = dataConnection.getData(testItemSearchQuery)
retrievedItem = ScrumblesObjects.Item(testItemSearchResult[0])

dataConnection.close()

assert retrievedItem.itemDescription == testItem.itemDescription

dataConnection.connect()
dataConnection.setData(deleteObjectQuery(retrievedItem))
itemAfterDeletionQueryResult = dataConnection.getData(ScrumblesData.CardQuery.getCardByCardID(retrievedItem.itemID))
dataConnection.close()
assert itemAfterDeletionQueryResult == ()


print('All Tests pass')