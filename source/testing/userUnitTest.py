### test creation and deletion of a User object
import ScrumblesObjects
import ScrumblesData

def testUsers(dataConnection):
    testUser = ScrumblesObjects.User()
    testUser.userName = 'UnitTestUser'
    testUser.userPassword = 'NoneOneC0res'
    testUser.userEmailAddress = 'testME@unitester.com'
    testUser.userRole = 'Admin'
    testUserCreationQuery = ScrumblesData.Query.createObject(testUser)
    assert testUserCreationQuery is not None
    dataConnection.connect()
    dataConnection.setData(testUserCreationQuery)
    dataConnection.close()
    testUserSearchQuery = ScrumblesData.UserQuery.getUserByUsername(testUser.userName)
    assert testUserSearchQuery is not None
    dataConnection.connect()
    foundTestuserResult = dataConnection.getData(testUserSearchQuery)
    dataConnection.close()
    foundUser = ScrumblesObjects.User(foundTestuserResult[0])
    assert foundUser.userName == testUser.userName
    dataConnection.connect()
    dataConnection.setData(ScrumblesData.Query.deleteObject(foundUser))
    foundTestuserResult = dataConnection.getData(testUserSearchQuery)
    dataConnection.close()
    assert foundTestuserResult == ()
    print('User Data',testUser.userID, 'successfully created and deleted on remote server')