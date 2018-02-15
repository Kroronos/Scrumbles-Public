import MySQLdb

class DataBaseLoginInfo:
    pass

class Query:
    getAllUsersQuery = 'SELECT * FROM UserTable'
    getAllSprintsQuery = 'SELECT * FROM SprintTable'
    getAllCardsQuery = 'SELECT * FROM CardTable'
    getAllCommentsQuery = 'SELECT * FROM CommentTable'

    def getUserIdByUsernameAndPassword(username, password):
        query ='SELECT UserID from UserTable WHERE (BINARY UserName=\'%s\') AND (BINARY UserPassword=\'%s\')'%(username,password)
        return query
    def createUserQuery(user):
        assert user.userName is not None
        assert user.userEmailAddress is not None
        assert user.userPassword is not None
        assert user.userRole is not None

        query = 'INSERT INTO UserTable (userName,UserEmailAddress,UserPassword,UserRole) VALUES (\'%s\',\'%s\',\'%s\',\'%s\')' % (
            user.userName, user.userEmailAddress, user.userPassword, user.userRole)
        return query

    def createSprintQuery(sprint):
        assert sprint.sprintStartDate is not None
        assert sprint.sprintDueDate is not None
        assert sprint.sprintName is not None
        query = 'INSERT INTO SprintTable (StartDate,DueDate,SprintName) VALUES (\'%s\',\'%s\',\'%s\')' % (
            str(sprint.sprintStartDate),str(sprint.sprintDueDate),sprint.sprintName)
        return query

    def assignItemToSprintQuery(item,sprint):
        assert item.itemID is not None
        assert sprint.sprintID is not None
        query = 'UPDATE CardTable SET CardDueDate = ( ' \
                'SELECT DueDate FROM SprintTable WHERE SprintID=%i), ' \
                'SprintID = %i where CardID = %i' % (sprint.sprintID,
                                                     sprint.sprintID,
                                                     item.itemID)
        return query

class ScrumblesData:
    def __init__(self, dbLoginInfo):
        self.ipaddress = dbLoginInfo.ipaddress
        self.userID = dbLoginInfo.userID
        self.password = dbLoginInfo.password
        self.defaultDB = dbLoginInfo.defaultDB
        self.dbConnection = None
    def connect(self):
        self.dbConnection = MySQLdb.connect(self.ipaddress,self.userID,self.password,self.defaultDB)
		
    def getData(self,query):
        assert self.dbConnection is not None
        self.dbConnection.query(query)
        queryResult = self.dbConnection.store_result()
        maxRows = 0
        how = 1
        return queryResult.fetch_row(maxRows,how)
		
    def setData(self,query):
        assert self.dbConnection is not None
        self.dbConnection.query(query)
        self.dbConnection.commit()
	
    def close(self):
        assert self.dbConnection is not None
        self.dbConnection.close()




