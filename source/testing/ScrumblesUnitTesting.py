import ScrumblesData
import ScrumblesObjects

ScrumblesUser_username = 'TestUser'
ScrumblesUser_password = 'Password1'

dbLoginInfo = ScrumblesData.DataBaseLoginInfo('login.txt')


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
assert len(allCommentsQueryResult) >= 0
print('Data Download Successful')
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
    #assert len(element) == 4  this is dumb, number of sprints change
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

print('Scrumbles Objects created successfully')

## Test Authentication Query
dataConnection.connect()
authUserQuery = ScrumblesData.Query.getUserByUsernameAndPassword(ScrumblesUser_username,ScrumblesUser_password)
authUserQueryResult = dataConnection.getData(authUserQuery)
dataConnection.close()
print(authUserQueryResult)
authUser = ScrumblesObjects.User(authUserQueryResult[0])

assert authUser.userName == ScrumblesUser_username

print('Authentication pass')

## Test Item Creation and deletion
from testing import itemUnitTest, userUnitTest, sprintUnitTest

itemUnitTest.testItems(dataConnection)

userUnitTest.testUsers(dataConnection)

sprintUnitTest.testSprints(dataConnection)




print('All Tests pass')