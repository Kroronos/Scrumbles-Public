import MySQLdb

class DataBaseLoginInfo:
    pass

class Query:
    getAllUsersQuery = 'SELECT * FROM UserTable'
    getAllSprintsQuery = 'SELECT * FROM SprintTable'
    getAllCardsQuery = 'SELECT * FROM CardTable'
    getAllCommentsQuery = 'SELECT * FROM CommentTable'
    def getSprintBySprintID(sprintID):
        assert sprintID is not None
        query = 'SELECT * FROM SprintTable WHERE SprintID=%i'%(sprintID)
        return query

    def getCommentsByUser(user):
        assert user is not None
        assert user.userID is not None
        query = 'SELECT * FROM CommentTable WHERE UserID=%i'%(user.userID)
        return query

    def getCommentsByItem(item):
        assert item is not None
        assert item.itemID is not None
        query = 'SELECT * FROM CommentTable WHERE CardID=%i'%(item.itemID)
        return query

    def getUserByUsername(username):
        query = 'SELECT * from UserTable WHERE UserName=\'%s\'' % (username)
        return query

    def getCardByCardID(cardID):
        query = 'SELECT * from CardTable WHERE CardID=%i'%(cardID)
        return query

    def getItemBySprint(sprint):
        assert sprint is not None
        assert sprint.sprintID is not None
        query = 'SELECT * FROM CardTable WHERE SprintID=%i'%(sprint.sprintID)
        return query

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

    def createItemQuery(item):
        assert item is not None
        assert item.itemType is not None
        assert item.itemTitle is not None
        assert item.itemDescription is not None
        query = 'INSERT INTO CardTable (' \
                'CardType,' \
                'CardPriority,' \
                'CardTitle,' \
                'CardDescription,' \
                'CardCreatedDate,' \
                'Status) VALUES (' \
                '\'%s\',0,\'%s\',\'%s\',' \
                'NOW(),0)' % (
            item.itemType,
            item.itemTitle,
            item.itemDescription
        )
        return query

    def createCommentQuery(comment):
        assert comment is not None
        assert comment.commentContent is not None
        assert comment.commentItemID is not None
        assert comment.commentUserID is not None
        query = 'INSERT INTO CommentTable (CommentTimeStamp,' \
                'CommentContent,' \
                'CardID,' \
                'UserID) VALUES ( NOW(), \'%s\',%i,%i)'%(
            comment.commentContent,
            comment.commentItemID,
            comment.commentUserID
        )
        return query


    def assignCardToSprintQuery(item,sprint):
        assert item.itemID is not None
        assert sprint.sprintID is not None
        query = 'UPDATE CardTable SET CardDueDate = ( ' \
                'SELECT DueDate FROM SprintTable WHERE SprintID=%i), ' \
                'SprintID = %i, Status=1 WHERE CardID = %i' % (sprint.sprintID,
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




