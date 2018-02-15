from ScrumblesData import *
from ScrumblesObjects import *
import datetime
username = 'TestUser'
password = 'PASSWORD'


dbLoginInfo = DataBaseLoginInfo()
dbLoginInfo.userID = 'test_user'
dbLoginInfo.password = 'testPassword'
dbLoginInfo.ipaddress = '173.230.136.241'
dbLoginInfo.defaultDB = 'test'


dataConnection = ScrumblesData(dbLoginInfo)
dataConnection.connect()
users = dataConnection.getData(Query.getAllUsersQuery)
sprints = dataConnection.getData(Query.getAllSprintsQuery)
cards = dataConnection.getData(Query.getAllCardsQuery)
comments = dataConnection.getData(Query.getAllCommentsQuery)

result = dataConnection.getData(Query.getUserIdByUsernameAndPassword(username, password))

if result == ():
    userID = 'cannot authenticate user'
else:
    userID = result[0]['UserID']

dataConnection.close()



for user in users:
    print('User ID\t\t', user['UserID'])
    print('Name\t\t', user['UserName'])
    print('Email\t\t', user['UserEmailAddress'])
    print('Password\t', user['UserPassword'])
    print('Role\t\t', user['UserRole'])
    print()
for sprint in sprints:
    print('SprintID\t', sprint['SprintID'])
    print('Name\t\t', sprint['SprintName'])
    print('Start\t\t', str(sprint['StartDate']))
    print('Due\t\t\t', str(sprint['DueDate']))
    print()
for card in cards:
    status = {0:'Unassigned',1:'Assigned',2:'In Progress',3:'Submitted',4:'Approved'}
    assignedUser = 'Not assigned to user'
    assignedSprint = 'Not assigned to Sprint'
    for sprint in sprints:
        if card['SprintID'] == sprint['SprintID']:
            assignedSprint = sprint['SprintName']
    for user in users:
        if card['UserID'] == user['UserID']:
            assignedUser = user['UserName']

    print('Card ID\t\t', card['CardID'])
    print('Type\t\t', card['CardType'])
    print('Priority\t', card['CardPriority'])
    print('Title\t\t', card['CardTitle'])
    print('Description\t', card['CardDescription'])
    print('Created on\t', str(card['CardCreatedDate']))
    print('Due Date\t', str(card['CardDueDate']))
    print('CodeLink\t', card['CardCodeLink'])
    print('SprintID\t', assignedSprint)
    print('UserID\t\t', assignedUser)
    print('Status\t\t', status[card['Status']])
    print()
for comment in comments:
    print('Comment ID\t', comment['CommentID'])
    print('TimeStamp\t',str(comment['CommentTimeStamp']))
    print('Content\t',comment['CommentContent'])
    username = ''
    for user in users:
        if user['UserID'] == comment['UserID']:
            username = user['UserName']
    print('User\t', username)
    cardTitle = ''
    for card in cards:
        if card['CardID'] == comment['CardID']:
            cardTitle = card['CardTitle']
    print('Item\t',cardTitle)
    print()

print(userID)

# Below is a successful test to create an Item
# Follow the procedure below for item creation
# item = Item()
# item.itemType = 'Story'
# item.itemTitle = 'User Clicks View Sprints'
# item.itemDescription = 'User will click a view sprints button or menu item and the application will show the Sprint View'
# itemQuery = Query.createItemQuery(item)
# print(itemQuery)
# try:
#     dataConnection.connect()
#     dataConnection.setData(Query.createItemQuery(item))
#     dataConnection.close()
# except Exception as e:
#     print(str(e))

# testSprint = Sprint()
# testSprint.sprintStartDate = datetime.date(2018,2,13)
# testSprint.sprintDueDate = datetime.date(2018,3,26)
# testSprint.sprintName = 'Sprint 3: Final Release'
# testSprintQuery = Query.createSprintQuery(testSprint)
# print(testSprintQuery)
# dataConnection.connect()
# try:
#     dataConnection.setData(Query.createSprintQuery(testSprint))
# except Exception as e:
#     print(str(e))
# dataConnection.close()

dataConnection.connect()
userQueryResult = dataConnection.getData(Query.getUserByUsername('bfallin'))
itemQueryResult = dataConnection.getData(Query.getCardByCardID(2))
sprintQueryResult = dataConnection.getData(Query.getSprintBySprintID(6))
dataConnection.close()
print(userQueryResult)
print(itemQueryResult)
print(sprintQueryResult)

bfallin = User(userQueryResult[0])
item = Item(itemQueryResult[0])
sprint = Sprint(sprintQueryResult[0])

# dataConnection.connect()
# dataConnection.setData(Query.assignCardToSprintQuery(item,sprint))
# dataConnection.close()

# newComment = Comment()
# newComment.commentContent = 'This item is nearly finished after the latest push'
# newComment.commentUserID = bfallin.userID
# newComment.commentItemID = item.itemID
#
# createCommentQuery = Query.createCommentQuery(newComment)
# print(createCommentQuery)
# dataConnection.connect()
# dataConnection.setData(Query.createCommentQuery(newComment))
# dataConnection.close()

