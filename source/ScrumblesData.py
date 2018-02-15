import MySQLdb

class DataBaseLoginInfo:
    pass

class Query:
    getAllUsers = 'SELECT * FROM UserTable'
    getAllSprints = 'SELECT * FROM SprintTable'
    getAllCards = 'SELECT * FROM CardTable'
    getAllComments = 'SELECT * FROM CommentTable'

    def getUserIdByUsernameAndPassword(username, password):
        query = 'SELECT UserID from UserTable WHERE (BINARY UserName=\'%s\') AND (BINARY UserPassword=\'%s\')' % (
        username, password)
        return query

    def assignCardToSprint(item,sprint):
        assert item.itemID is not None
        assert sprint.sprintID is not None
        query = 'UPDATE CardTable SET CardDueDate = ( ' \
                'SELECT DueDate FROM SprintTable WHERE SprintID=%i), ' \
                'SprintID = %i, Status=1 WHERE CardID = %i' % (sprint.sprintID,
                                                     sprint.sprintID,
                                                     item.itemID)
        return query

class SprintQuery(Query):
    def createSprint(sprint):
        assert sprint.sprintName is not None
        query = 'INSERT INTO SprintTable (StartDate,DueDate,SprintName) VALUES (\'%s\',\'%s\',\'%s\')' % (
            str(sprint.sprintStartDate), str(sprint.sprintDueDate), sprint.sprintName)
        return query

    def updateSprint(sprint):
        assert sprint is not None
        assert sprint.sprintID is not None

        query = 'UPDATE SprintTable SET StartDate=%s,' \
                'DueDate=\'%s\', SprintName=\'%s\' WHERE SprintID=%i'%(
            sprint.sprintStartDate,
            sprint.sprintDueDate,
            sprint.sprintName,
            sprint.sprintID
        )
        return query

    def getSprintBySprintID(sprintID):
        assert sprintID is not None
        query = 'SELECT * FROM SprintTable WHERE SprintID=%i' % (sprintID)
        return query

class CardQuery(Query):
    def createCard(item):
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

    def updateCard(item):
        assert item is not None
        assert item.itemID is not None
        query = 'UPDATE CardTable SET ' \
                'CardType=\'%s\',' \
                'CardPriority=%i,' \
                'CardTitle=\'%s\',' \
                'CardDescription=\'%s\',' \
                'CardDueDate=\'%s\',' \
                'CardCodeLink=\'%s\',' \
                'SprintID=%i,' \
                'UserID=%i,' \
                'Status=%i WHERE CardID=%i'% (
            item.itemType,
            item.itemPriority,
            item.itemTitle,
            item.itemDescription,
            item.itemDueDate,
            item.itemCodeLink,
            item.itemSprintID,
            item.itemUserID,
            item.itemStatus,
            item.itemID
        )
        return query

    def getCardByCardID(cardID):
        query = 'SELECT * from CardTable WHERE CardID=%i' % (cardID)
        return query

    def getCardsBySprint(sprint):
        assert sprint is not None
        assert sprint.sprintID is not None
        query = 'SELECT * FROM CardTable WHERE SprintID=%i' % (sprint.sprintID)
        return query

class UserQuery(Query):
    def getUserByUsername(username):
        query = 'SELECT * from UserTable WHERE UserName=\'%s\'' % (username)
        return query

    def createUser(user):
        assert user.userName is not None
        assert user.userEmailAddress is not None
        assert user.userPassword is not None
        assert user.userRole is not None

        query = 'INSERT INTO UserTable (userName,UserEmailAddress,UserPassword,UserRole) VALUES (\'%s\',\'%s\',\'%s\',\'%s\')' % (
            user.userName, user.userEmailAddress, user.userPassword, user.userRole)
        return query

    def updateUser(user):
        assert user is not None
        assert user.userID is not None
        query = 'UPDATE UserTable SET ' \
                'UserName=\'%s\',' \
                'UserEmailAddress=\'%s\',' \
                'UserPassword=\'%s\',' \
                'UserRole=\'%s\' WHERE ' \
                'UserID=%i' % (
            user.userName,
            user.userEmailAddress,
            user.userPassword,
            user.userRole,
            user.userID
        )
        return query

class CommentQuery(Query):
    def createComment(comment):
        assert comment is not None
        assert comment.commentContent is not None
        assert comment.commentItemID is not None
        assert comment.commentUserID is not None
        query = 'INSERT INTO CommentTable (CommentTimeStamp,' \
                'CommentContent,' \
                'CardID,' \
                'UserID) VALUES ( NOW(), \'%s\',%i,%i)' % (
                    comment.commentContent,
                    comment.commentItemID,
                    comment.commentUserID
                )
        return query

    def updateComment(comment):
        assert comment is not None
        assert comment.commentID is not None
        query = 'UPDATE CommentTable SET ' \
                'CommentContent=\'%s\' WHERE' \
                'CommentID=%i' % (
            comment.commentContent,
            comment.commentID
        )

    def getCommentsByUser(user):
        assert user is not None
        assert user.userID is not None
        query = 'SELECT * FROM CommentTable WHERE UserID=%i' % (user.userID)
        return query

    def getCommentsByItem(item):
        assert item is not None
        assert item.itemID is not None
        query = 'SELECT * FROM CommentTable WHERE CardID=%i' % (item.itemID)
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




