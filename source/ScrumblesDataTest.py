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
    print('Card ID\t\t', card['CardID'])
    print('Type\t\t', card['CardType'])
    print('Priority\t', card['CardPriority'])
    print('Title\t\t', card['CardTitle'])
    print('Description\t', card['CardDescription'])
    print('Created on\t', str(card['CardCreatedDate']))
    print('Due Date\t', str(card['CardDueDate']))
    print('CodeLink\t', card['CardCodeLink'])
    print('SprintID\t', card['SprintID'])
    print('UserID\t\t', card['UserID'])
    print('Status\t\t', card['Status'])
    print()
for comment in comments:
    print(comment)

print(userID)

# The following test case passed
# bfallin = User()
# bfallin.userName = 'bfallin'
# bfallin.userEmailAddress = 'fallinbryan@ufl.edu'
# bfallin.userRole = 'Scrum Master'
# bfallin.userPassword = 'ITrustNo1'
# createBfallinQuery = Query.createUserQuery(bfallin)
# print(createBfallinQuery)
#
# dataConnection.connect()
# try:
#     dataConnection.setData(Query.createUserQuery(bfallin))
# except Exception as e:
#     print(str(e))
# dataConnection.close()

testSprint = Sprint()
testSprint.sprintStartDate = datetime.date(2018,2,12)
testSprint.sprintDueDate = datetime.date(2018,2,25)
testSprint.sprintName = 'Sprint 1: Make me Pretty'
testSprintQuery = Query.createSprintQuery(testSprint)
print(testSprintQuery)
# dataConnection.connect()
# try:
#     dataConnection.setData(Query.createSprintQuery(testSprint))
# except Exception as e:
#     print(str(e))
# dataConnection.close()
