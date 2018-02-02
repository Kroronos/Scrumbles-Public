from ScrumblesData import *


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
dataConnection.close()

for user in users:
    print(user)
for sprint in sprints:
    print(sprint)
for card in cards:
    print(card)
for comment in comments:
    print(comment)
