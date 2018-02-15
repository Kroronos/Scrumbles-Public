import ScrumblesData
import ScrumblesObjects
import datetime

ScrumblesUser_username = 'TestUser'
ScrumblesUser_password = 'PASSWORD'

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
testItemCreationQuery = ScrumblesData.Query.createObject(testItem)
assert testItemCreationQuery is not None
dataConnection.connect()
dataConnection.setData(testItemCreationQuery)

testItemSearchQuery = ScrumblesData.CardQuery.getCardByCardTitle(testItem.itemTitle)
testItemSearchResult = dataConnection.getData(testItemSearchQuery)
retrievedItem = ScrumblesObjects.Item(testItemSearchResult[0])

dataConnection.close()

assert retrievedItem.itemDescription == testItem.itemDescription

dataConnection.connect()
dataConnection.setData(ScrumblesData.Query.deleteObject(retrievedItem))
itemAfterDeletionQueryResult = dataConnection.getData(ScrumblesData.CardQuery.getCardByCardID(retrievedItem.itemID))
dataConnection.close()
assert itemAfterDeletionQueryResult == ()


print('All Tests pass')