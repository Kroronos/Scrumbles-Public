import MySQLdb, logging
import ScrumblesObjects
import base64


class DataBaseLoginInfo:
    def __init__(self,file):
        loginFile = open(file, 'r')
        self.userID = self.getFromFile(loginFile)
        self.password = self.getFromFile(loginFile)
        self.ipaddress = self.getFromFile(loginFile)
        self.defaultDB = self.getFromFile(loginFile)
        loginFile.close()
    def getFromFile(self, openFile):
        item = openFile.readline()
        item = item.rstrip("\n\r")
        item = base64.standard_b64decode(item)
        item = item.decode('utf8')
        return item

def debug_ObjectdumpList(L):
    if len(L) == 0:
        print('-----> ** Empty List ** <-----')

    elif type(L[0]) == ScrumblesObjects.Item:
        for I in L:
            print('\t',I.itemTitle)
    elif type(L[0]) == ScrumblesObjects.User:
        for U in L:
            print('\t',U.userName)
    elif type(L[0]) == ScrumblesObjects.Sprint:
        for S in L:
            print('\t',S.sprintName)
    elif type(L[0]) == ScrumblesObjects.Project:
        for P in L:
            print('\t',P.projectName)
    elif type(L[0]) == ScrumblesObjects.Comment:
        for C in L:
            print('\t',C.commentUserID)

class ScrumblesData:
    def __init__(self, dbLoginInfo):
        self.ipaddress = dbLoginInfo.ipaddress
        self.userID = dbLoginInfo.userID
        self.password = dbLoginInfo.password
        self.defaultDB = dbLoginInfo.defaultDB
        self.dbConnection = None
        self.cursor = None
        # This connect and close will check if the network is good
        # an excpetion will be thrown if unable to connect to server
        self.connect()
        self.close()

    def connect(self):
        self.dbConnection = MySQLdb.connect(self.ipaddress, self.userID, self.password, self.defaultDB)
        self.cursor = self.dbConnection.cursor()
    def getData(self, query):
        assert self.dbConnection is not None
        self.dbConnection.query(query)
        queryResult = self.dbConnection.store_result()
        maxRows = 0
        how = 1
        return queryResult.fetch_row(maxRows, how)

    def setData(self, query):
        print(query)
        assert self.dbConnection is not None
        try:
            if type(query) is not tuple:
                self.cursor.execute(query)
                self.dbConnection.commit()
            else:

                self.cursor.execute(query[0],query[1])
                self.dbConnection.commit()
        except:
            logging.exception('Query did not execute')
            self.dbConnection.rollback()


    def close(self):
        assert self.dbConnection is not None
        self.cursor = None
        self.dbConnection.close()

    def isConnected(self):
        return self.dbConnection.open == 1






