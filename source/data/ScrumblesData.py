import MySQLdb, logging
from data import ScrumblesObjects
import base64
import time

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
        maxRows = 0
        how = 1
        assert self.dbConnection is not None
        self.dbConnection.query(query)
        try:
            queryResult = self.dbConnection.store_result()
            returnVal = queryResult.fetch_row(maxRows, how)
        except AttributeError as e:
            logging.exception('Query {} failed to execute, attempting again in 2 seconds'.format(query))
            time.sleep(2)
            try:
                queryResult = self.dbConnection.store_result()
                returnVal = queryResult.fetch_row(maxRows, how)
            except AttributeError as e:
                logging.exception('Query failed to execute second time, giving up')
                return
        return returnVal

    def setMulti(self,query):
        sql = query[0]
        i = 0
        params = query[1]
        try:
            for line in sql.splitlines():

                i += 1
                cursor = self.dbConnection.cursor()
                try:
                    cursor.execute(line,params[i])
                except Exception as e:
                    logging.exception('failed to execute query')
                    raise(e)
                cursor.close()
            self.dbConnection.commit()
        except Exception:
            logging.exception('Multi Line SQL did not commit')
            self.dbConnection.rollback()

    def setData(self, query):
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






