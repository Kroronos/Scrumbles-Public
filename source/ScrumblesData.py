import MySQLdb

class DataBaseLoginInfo:
    pass

class Query:
    getAllUsersQuery = 'SELECT * FROM UserTable'
    getAllSprintsQuery = 'SELECT * FROM SprintTable'
    getAllCardsQuery = 'SELECT * FROM CardTable'
    getAllCommentsQuery = 'SELECT * FROM CommentTable'

class ScrumblesData:
    def __init__(self, dbLoginInfo):
        self.ipaddress = dbLoginInfo.ipaddress
        self.userID = dbLoginInfo.userID
        self.password = dbLoginInfo.password
        self.defaultDB = dbLoginInfo.defaultDB
    
    def connect(self):
        self.dbConnection = MySQLdb.connect(self.ipaddress,self.userID,self.password,self.defaultDB)
		
    def getData(self,query):
        self.dbConnection.query(query)
        queryResult = self.dbConnection.store_result()
        maxRows = 0
        how = 1
        return queryResult.fetch_row(maxRows,how)
		
    def setData(self,query):
        self.dbConnection.query(query)
        self.commit()
	
    def close(self):
        self.dbConnection.close()




