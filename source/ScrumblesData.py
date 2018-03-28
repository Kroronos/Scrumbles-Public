import logging
import MySQLdb
import ScrumblesObjects
import re
import hashlib
import base64
import threading,time
import remoteUpdate

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

def dbWrap(func):
    def wrapper(self,*args):
        self.conn.connect()
        func(self,*args)
        self.conn.close()
    return wrapper


class QueryException(Exception):
    def __init__(self,message):
        super().__init__(message)

class DataBlock:
    users = []
    items = []
    projects = []
    comments = []
    tags = []
    sprints = []
    updaterCallbacks = []


    def __init__(self):
        logging.info('Initializing DataBlock Object')
        self.alive = True
        self.dbLogin = DataBaseLoginInfo('login.txt')
        self.conn = ScrumblesData(self.dbLogin)
        self.listener = remoteUpdate.RemoteUpdate()
        self.lock = threading.Lock()
        self.updateAllObjects()
        self.size = self.getLen()
        self.updaterThread = threading.Thread(target = self.updater, args=())
        self.cv = threading.Condition()

        self.updaterThread.start()

    def __del__(self):
        self.shutdown()
        del self.listener

    def getLen(self):
        rv = len(self.items)
        return rv

    def debugDump(self):
        print('\nDumping Projects')
        debug_ObjectdumpList(self.projects)
        for P in self.projects:
            print('Dumping lists in ', P.projectName)
            print('Dumping assgined Users')
            debug_ObjectdumpList(P.listOfAssignedUsers)
            print('Dumping assinged Sprints')
            debug_ObjectdumpList(P.listOfAssignedSprints)
            print('Dumping assigned Items')
            debug_ObjectdumpList(P.listOfAssignedItems)
        print('\nDumping Sprints')
        debug_ObjectdumpList(self.sprints)
        for S in self.sprints:
            print('Dumping lists in ', S.sprintName)
            print('Dumping assigned Items')
            debug_ObjectdumpList(S.listOfAssignedItems)
            print('Dumping assigned Users')
            debug_ObjectdumpList(S.listOfAssignedUsers)
        print('\nDumping Users')
        debug_ObjectdumpList(self.users)
        for U in self.users:
            print('Dumping lists in ', U.userName)
            print('Dumping assigned items')
            debug_ObjectdumpList(U.listOfAssignedItems)
            print('Dumping comments')
            debug_ObjectdumpList(U.listOfComments)
            print('Dumping in projects')
            debug_ObjectdumpList(U.listOfProjects)
        print('\nDumping Items')
        debug_ObjectdumpList(self.items)
        for I in self.items:
            print('Dumping comments on item',I.itemTitle)
        print('\nDumping Comments')
        debug_ObjectdumpList(self.comments)




    def updateAllObjects(self):
        self.conn.connect()
        self.users.clear()
        self.items.clear()
        self.projects.clear()
        self.comments.clear()
        self.tags.clear()
        self.sprints.clear()
        userTable = self.conn.getData(Query.getAllUsers)
        itemTable = self.conn.getData(Query.getAllCards)
        projectTable = self.conn.getData(Query.getAllProjects)
        commentTable = self.conn.getData(Query.getAllComments)
        sprintTable = self.conn.getData(Query.getAllSprints)
        userToProjectRelationTable = self.conn.getData(Query.getAllUserProject)
        itemToProjectRelationTable = self.conn.getData(Query.getAllProjectItem)
        self.conn.close()
        for comment in commentTable:
            Comment = ScrumblesObjects.Comment(comment)
            self.comments.append(Comment)

        for item in itemTable:
            Item = ScrumblesObjects.Item(item)
            Item.listOfComments = [C for C in self.comments if C.commentItemID == Item.itemID]
            self.items.append(Item)


        for user in userTable:
            User = ScrumblesObjects.User(user)
            User.listOfAssignedItems = [ I for I in self.items if I.itemUserID == User.userID ]
            User.listOfComments = [ C for C in self.comments if C.commentUserID == User.userID ]
            self.users.append(User)

        for sprint in sprintTable:
            Sprint = ScrumblesObjects.Sprint(sprint)
            Sprint.listOfAssignedItems = [I for I in self.items if I.itemSprintID == Sprint.sprintID]
            Sprint.listOfAssignedUsers = [U for U in self.users if U.userID in [I.itemUserID for I in Sprint.listOfAssignedItems]]
            self.sprints.append(Sprint)

        for project in projectTable:
            Project = ScrumblesObjects.Project(project)
            Project.listOfAssignedSprints = [S for S in self.sprints if S.projectID == Project.projectID]
            self.projects.append(Project)



        for user in self.users:
            for dict in userToProjectRelationTable:
                if dict['UserID'] == user.userID:
                    for project in self.projects:
                        if dict['ProjectID'] == project.projectID:
                            user.listOfProjects.append(project)

        for project in self.projects:
            for dict in userToProjectRelationTable:
                if dict['ProjectID'] == project.projectID:
                    for user in self.users:
                        if dict['UserID'] == user.userID:
                            project.listOfAssignedUsers.append(user)

            for dict in itemToProjectRelationTable:
                if dict['ProjectID'] == project.projectID:
                    for item in self.items:
                        if dict['ItemID'] == item.itemID:
                            item.projectID = project.projectID

                            project.listOfAssignedItems.append(item)


        #self.debugDump()
        return True

    def validateData(self):
        return self.getLen() > 0

    @dbWrap
    def addUserToProject(self,project,user):
        logging.info('Adding User %s to project %s' % (user.UserName,project.projectName))
        if user not in project.listOfAssignedUsers:
            self.conn.setData(ProjectQuery.addUser(project,user))
        else:
            print('User already assigned to project')

    @dbWrap
    def removeUserFromProject(self,project,user):
        logging.info('Removing User %s from project %s' %(user.UserName,project.projectName) )
        for item in self.items:
            if item in project.listOfAssignedItems:
                if item.itemUserID == user.userID:
                    item.itemUserID = 0

            self.conn.setData(Query.updateObject(item))

        self.conn.setData(ProjectQuery.removeUser(project,user))


    ##### DUPLICATE CODE TODO Remove below and change callers to addNewScrumblesObject
    @dbWrap
    def addComment(self,comment):
        logging.warning('Depreciated function call: Adding Comment to database: %s' % comment.commentContent)
        self.conn.setData(Query.createObject(comment))


    @dbWrap
    def assignUserToItem(self,user,item):
        logging.info('Assigning User %s to item %s.'%(user.userName,item.itemTitle))
        item.itemUserID = user.userID
        item.itemStatus = 1
        self.conn.setData(Query.updateObject(item))
    @dbWrap
    def addItemToProject(self,project,item):
        logging.info('Adding item %s to project %s.' %(item.itemTitle,project.projectName))
        if item not in project.listOfAssignedItems:
            item.projectID = project.projectID
            self.conn.setData(ProjectQuery.addItem(project,item))
        else:
            print('Item already assigned to project')
    @dbWrap
    def removeItemFromProject(self,project,item):
        logging.info('Removing item %s from project %s.' % (item.itemTitle,project.projectName))
        item.projectID = 0
        self.conn.setData(ProjectQuery.removeItem(project,item))

    @dbWrap
    def addNewScrumblesObject(self,obj):
        logging.info('Adding new object %s to database' % repr(obj))
        self.conn.setData(Query.createObject(obj))

    @dbWrap
    def updateScrumblesObject(self,obj):
        logging.info('Updating object %s to database' % repr(obj))
        self.conn.setData(Query.updateObject(obj))

    @dbWrap
    def deleteScrumblesObject(self,obj):
        logging.info('Deleting object %s from database' % repr(obj))
        self.conn.setData(Query.deleteObject(obj))

    @dbWrap
    def modifiyItemPriority(self,item,priority):
        logging.info('Modifying item %s priority to %s' % (item.itemTitle,item.priorityEquivalents[priority]))
        assert priority in range(1,3)
        item.itemPriority = priority
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def modifyItemStatus(self,item,status):
        logging.info('Modifying item %s status to %s' % (item.itemTitle,item.statusEquivalents[status]))
        assert status in range(0,4)
        item.itemStatus = status
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def modifyItemStatusByString(self,item,status):
        logging.info('Modifying item %s to status %s.' % (item.itemTitle,status))
        item.itemStatus = item.statusEquivalentsReverse[status]
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def assignItemToSprint(self,item,sprint):
        logging.info('Assigning Item %s to Sprint %s.',(item.itemTitle,sprint.sprintName))
        item.itemSprintID = sprint.sprintID
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def removeItemFromSprint(self,item):
        logging.info('Removing Item %s from sprint %d.'%(item.itemTitle,item.itemSprintID))
        item.itemSprintID = 0
        self.conn.setData(Query.updateObject(item))




    def updater(self):
        logging.info('Updater Thread %s started' % threading.get_ident())
        threading.Thread(target=self.listener.start,args=()).start()

        while self.alive:
            time.sleep(2)
            if self.listener.isDBChanged:
                time.sleep(2)
                with self.cv:
                    self.cv.wait_for(self.updateAllObjects)

                    self.executeUpdaterCallbacks()
                    self.listener.isDBChanged = False


    def packCallback(self,callback):
        logging.info('Callback %s packed into DataBlock' % str(callback))
        self.updaterCallbacks.append(callback)

    def executeUpdaterCallbacks(self):
        if len(self.updaterCallbacks) > 0:
            for func in self.updaterCallbacks:
                logging.info('Executing Updater Func %s'% str(func))
                func()

    def shutdown(self):
        logging.info('Shutting down Thread %s'%threading.get_ident())
        self.alive = False
        self.listener.stop()




class Query:
    getAllUsers = 'SELECT * FROM UserTable'
    getAllSprints = 'SELECT * FROM SprintTable'
    getAllCards = 'SELECT * FROM CardTable'
    getAllComments = 'SELECT * FROM CommentTable'
    getAllProjects = 'SELECT * FROM ProjectsTable'
    getAllUserProject = 'SELECT * FROM ProjectUserTable'
    getAllProjectItem = 'SELECT * FROM ProjectItemTable'
    @staticmethod
    def getUserByUsernameAndPassword(username, password):
        hashedPassword = Password(password)
        hashedPassword.encrypt()
        query = 'SELECT * from UserTable WHERE (BINARY UserName=\'%s\') AND (BINARY UserPassword=\'%s\')' % (
        username, str(hashedPassword))
        return query

    @staticmethod
    def assignCardToSprint(item,sprint):
        if item is None or sprint is None:
            raise QueryException('Item or Sprint is None type')
        if item.itemID is None:
            raise QueryException('ItemID is None type')
        if sprint.sprintID is None:
            raise QueryException('SprintID is None type')
        query = 'UPDATE CardTable SET CardDueDate = ( ' \
                'SELECT DueDate FROM SprintTable WHERE SprintID=%i), ' \
                'SprintID = %i, Status=1 WHERE CardID = %i' % (sprint.sprintID,
                                                     sprint.sprintID,
                                                     item.itemID)
        return query

    @staticmethod
    def createObject(obj):
        query = ''
        if type(obj) == ScrumblesObjects.User:
            query = UserQuery.createUser(obj)
        elif type(obj) == ScrumblesObjects.Sprint:
            query = SprintQuery.createSprint(obj)
        elif type(obj) == ScrumblesObjects.Item:
            query = CardQuery.createCard(obj)
        elif type(obj) == ScrumblesObjects.Comment:
            query = CommentQuery.createComment(obj)
        elif type(obj) == ScrumblesObjects.Project:
            query = ProjectQuery.createProject(obj)

        else:
            raise Exception('Invalid Object Type')
        return query

    @staticmethod
    def deleteObject(obj):
        query = ''
        if type(obj) == ScrumblesObjects.User:
            query = UserQuery.deleteUser(obj)
        elif type(obj) == ScrumblesObjects.Comment:
            query = CommentQuery.deleteComment(obj)
        elif type(obj) == ScrumblesObjects.Sprint:
            query = SprintQuery.deleteSprint(obj)
        elif type(obj) == ScrumblesObjects.Item:
            query = CardQuery.deleteCard(obj)
        elif type(obj) == ScrumblesObjects.Project:
            query = ProjectQuery.deleteProject(obj)
        else:
            raise Exception('Invalid Object Type')
        return query

    @staticmethod
    def updateObject(obj):
        query = ''
        if type(obj) == ScrumblesObjects.User:
            query = UserQuery.updateUser(obj)
        elif type(obj) == ScrumblesObjects.Comment:
            query = CommentQuery.updateComment(obj)
        elif type(obj) == ScrumblesObjects.Sprint:
            query = SprintQuery.updateSprint(obj)
        elif type(obj) == ScrumblesObjects.Item:
            query = CardQuery.updateCard(obj)
        elif type(obj) == ScrumblesObjects.Project:
            query = ProjectQuery.updateProject(obj)
        else:
            raise Exception('Invalid Object Type')
        return query

class ProjectQuery(Query):
    @staticmethod
    def createProject(project):
        ObjectValidator.validate(project)
        query = 'INSERT INTO ProjectsTable (ProjectID, ProjectName) VALUES (\'%s\',\'%s\')' % (
            str(project.projectID),project.projectName)
        return query

    @staticmethod
    def deleteProject(project):
        assert project is not None
        query = 'DELETE FROM ProjectsTable WHERE ProjectID=\'%s\'' % (str(project.projectID))
        return query

    @staticmethod
    def updateProject(project):
        assert project is not None
        query = 'UPDATE ProjectsTable SET ProjectName=\'%s\' WHERE ProjectID = %i' % (project.projectName,
                                                                                      project.projectID)
        return query

    @staticmethod
    def addUser(project,user):
        query = 'INSERT INTO ProjectUserTable (UserID, ProjectID) VALUES (\'%s\',\'%s\')' % (
            str(user.userID),str(project.projectID)
        )
        return query
    @staticmethod
    def removeUser(project,user):
        query = 'DELETE FROM ProjectUserTable WHERE ProjectID=\'%s\' AND UserID=\'%s\'' % (
            str(project.projectID),str(user.userID)
        )
        return query
    @staticmethod
    def addItem(project,item):
        query = 'INSERT INTO ProjectItemTable (ItemID,ProjectID) VALUES (\'%s\',\'%s\')' % (
            str(item.itemID),str(project.projectID)
        )
        return query
    @staticmethod
    def removeItem(project,item):
        query = 'DELETE FROM ProjectItemTable WHERE ProjectID=\'%s\' AND ItemID=\'%s\'' % (
            str(project.projectID),str(item.itemID)
        )
        return query
class SprintQuery(Query):
    @staticmethod
    def createSprint(sprint):
        ObjectValidator.validate(sprint)
        sprintMap = { 'SprintName': 'NULL','StartDate':'NULL','DueDate':'NULL', 'ProjectID':'NULL'}
        sprintMap['SprintID'] = "'"+str(sprint.sprintID)+"'"
        if sprint.sprintName is not None:
            sprintMap['SprintName'] = "'"+str(sprint.sprintName)+"'"
        if sprint.sprintStartDate is not None:
            sprintMap['StartDate'] = "'"+str(sprint.sprintStartDate)+"'"
        if sprint.sprintDueDate is not None:
            sprintMap['DueDate'] = "'"+str(sprint.sprintDueDate)+"'"
        if sprint.projectID is not None:
            sprintMap['ProjectID'] = "'"+str(sprint.projectID)+"'"

        query = '''INSERT INTO SprintTable (SprintID, SprintName, StartDate,DueDate,ProjectID) VALUES (
        %s,%s,%s,%s,%s)''' % (sprintMap['SprintID'],sprintMap['SprintName'],sprintMap['StartDate']
                              ,sprintMap['DueDate'],sprintMap['ProjectID'])
        print(query)
        return query

    @staticmethod
    def updateSprint(sprint):
        assert sprint is not None
        assert sprint.sprintID is not None

        query = 'UPDATE SprintTable SET StartDate=\'%s\',' \
                'DueDate=\'%s\', SprintName=\'%s\' WHERE SprintID=%i'%(
            sprint.sprintStartDate,
            sprint.sprintDueDate,
            sprint.sprintName,
            sprint.sprintID
        )
        return query

    @staticmethod
    def getSprintBySprintID(sprintID):
        assert sprintID is not None
        query = 'SELECT * FROM SprintTable WHERE SprintID=%i' % (sprintID)
        return query

    @staticmethod
    def deleteSprint(sprint):
        assert sprint is not None
        query = 'DELETE FROM SprintTable WHERE SprintID=%i' % (sprint.sprintID)
        return query

class CardQuery(Query):
    @staticmethod
    def createCard(item):
        ObjectValidator.validate(item)
        query = 'INSERT INTO CardTable (' \
                'CardId,'\
                'CardType,' \
                'CardPriority,' \
                'CardTitle,' \
                'CardDescription,' \
                'CardCreatedDate,' \
                'CardPoints,' \
                'Status) VALUES (' \
                '\'%s\',\'%s\',0,\'%s\',\'%s\',' \
                'NOW(),\'%s\',0)' % (
            str(item.itemID),
            item.itemType,
            item.itemTitle,
            item.itemDescription,
            str(item.itemPoints)
        )
        print(query)
        return query

    @staticmethod
    def updateCard(item):
        assert item is not None
        assert item.itemID is not None
        itemDict = {}
        itemDict['Type'] = "'"+item.itemType+"'"
        itemDict['Priority'] = "'"+str(item.itemPriority)+"'"
        itemDict['Title'] = "'"+item.itemTitle+"'"
        itemDict['Descr'] = "'"+item.itemDescription+"'"
        itemDict['DueDate'] = 'NULL'
        if item.itemDueDate is not None:
            itemDict['DueDate'] = "'"+str(item.itemDueDate)+"'"
        itemDict['Sprint'] = "'"+str(item.itemSprintID)+"'"
        itemDict['User'] = "'"+str(item.itemUserID)+"'"
        itemDict['Status'] = "'"+str(item.itemStatus)+"'"
        itemDict['CodeLink'] = 'NULL'
        if item.itemCodeLink is not None:
            itemDict['CodeLink'] = "'"+item.itemCodeLink+"'"
        itemDict['Points'] = "'"+str(item.itemPoints)+"'"

        query = '''UPDATE CardTable SET
                CardType=%s,
                CardPriority=%s,
                CardTitle=%s,
                CardDescription=%s,
                CardDueDate=%s,
                CardCodeLink=%s,
                SprintID=%s,
                UserID=%s,
                Status=%s,
                CardPoints=%s WHERE CardID=%s'''% (
            itemDict['Type'],
            itemDict['Priority'],
            itemDict['Title'],
            itemDict['Descr'],
            itemDict['DueDate'],
            itemDict['CodeLink'],
            itemDict['Sprint'],
            itemDict['User'],
            itemDict['Status'],
            itemDict['Points'],
            item.itemID
        )
        print(query)
        return query

    @staticmethod
    def getCardByCardID(cardID):
        query = 'SELECT * from CardTable WHERE CardID=%i' % (cardID)
        return query

    @staticmethod
    def getCardByCardTitle(cardTitle):
        query = 'SELECT * FROM CardTable WHERE CardTitle=\'%s\'' % (cardTitle)
        return query

    @staticmethod
    def getCardsBySprint(sprint):
        assert sprint is not None
        assert sprint.sprintID is not None
        query = 'SELECT * FROM CardTable WHERE SprintID=%i' % (sprint.sprintID)
        return query

    @staticmethod
    def deleteCard(item):
        assert item is not None
        query = 'DELETE FROM CardTable WHERE CardID=%i' % (item.itemID)
        return query

class UserQuery(Query):
    @staticmethod
    def getUserByUsername(username):
        query = 'SELECT * from UserTable WHERE UserName=\'%s\'' % (username)
        return query

    @staticmethod
    def createUser(user):
        ObjectValidator.validate(user)
        password = Password(user.userPassword)
        password.encrypt()
        query = 'INSERT INTO UserTable (UserID, userName,UserEmailAddress,UserPassword,UserRole) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (
            str(user.userID), user.userName, user.userEmailAddress, str(password), user.userRole)
        return query

    @staticmethod
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

    @staticmethod
    def deleteUser(user):
        assert user is not None
        query = 'DELETE FROM UserTable WHERE UserID=%i' % (user.userID)
        return query

class CommentQuery(Query):
    @staticmethod
    def createComment(comment):

        query = 'INSERT INTO CommentTable (CommentID, CommentTimeStamp,' \
                'CommentContent,' \
                'CardID,' \
                'UserID) VALUES ( \'%s\',NOW(), \'%s\',%i,%i)' % (
                    str(comment.commentID),
                    comment.commentContent,
                    comment.commentItemID,
                    comment.commentUserID
                )
        return query

    @staticmethod
    def updateComment(comment):
        assert comment is not None
        assert comment.commentID is not None
        query = 'UPDATE CommentTable SET ' \
                'CommentContent=\'%s\' WHERE' \
                'CommentID=%i' % (
            comment.commentContent,
            comment.commentID
        )
        return query

    @staticmethod
    def getCommentsByUser(user):
        assert user is not None
        assert user.userID is not None
        query = 'SELECT * FROM CommentTable WHERE UserID=%i' % (user.userID)
        return query

    @staticmethod
    def getCommentsByItem(item):
        assert item is not None
        assert item.itemID is not None
        query = 'SELECT * FROM CommentTable WHERE CardID=%i' % (item.itemID)
        return query

    @staticmethod
    def deleteComment(comment):
        assert comment is not None
        query = 'DELETE FROM CommentTable WHERE CommentID=%i' % (comment.commentID)
        return query

class ScrumblesData:
    def __init__(self, dbLoginInfo):
        self.ipaddress = dbLoginInfo.ipaddress
        self.userID = dbLoginInfo.userID
        self.password = dbLoginInfo.password
        self.defaultDB = dbLoginInfo.defaultDB
        self.dbConnection = None
        #This connect and close will check if the network is good
        #an excpetion will be thrown if unable to connect to server
        self.connect()
        self.close()
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

    def isConnected(self):
        return self.dbConnection.open == 1

class Password:
    password = None

    def __init__(self,password):
        self.password = password
    def __str__(self):
        return self.password

    def doesPasswordMeetComplexityRequirement(self):
        #must be 8 digits, 1 uppercase, 1 lowercase, and 1 digit
        if self.password == '':
            raise Exception('Password must not be blank')
        isLong = len(self.password) >= 8
        isNotAllLowercase = self.password.lower() != self.password
        isNotAllUppercase = self.password.upper() != self.password
        hasANumber = False
        for char in self.password:
            if char.isdigit():
                hasANumber = True

        goodPassword = isLong and isNotAllLowercase and isNotAllUppercase and hasANumber
        if not goodPassword:
            raise Exception('Password must be 8 digits long and contain at least 1 upper case, 1 lowercase and 1 number')


    def encrypt(self):
        self.password = self.password.encode('utf-8')
        self.password = hashlib.sha256(self.password).hexdigest()
        
    __repr__ = __str__

class ObjectValidator:
    @staticmethod
    def validate(obj):
        if type(obj) == ScrumblesObjects.User:
            ObjectValidator.validateUser(obj)
        elif type(obj) == ScrumblesObjects.Item:
            ObjectValidator.validateCard(obj)
        elif type(obj) == ScrumblesObjects.Sprint:
            ObjectValidator.validateSprint(obj)
        elif type(obj) == ScrumblesObjects.Comment:
            ObjectValidator.validateComment(obj)
        elif type(obj) == ScrumblesObjects.Project:
            ObjectValidator.validateProject(obj)
        else:
            raise Exception('Invalid Object')

    @staticmethod
    def validateProject(project):
        if len(project.projectName) < 1:
            raise Exception('Project Name too short')
        return

    @staticmethod
    def validateUser(user):

        if len(user.userName) < 5:
            raise Exception('User Name too Short')
        if ' ' in user.userName:
            raise Exception('User Name must not contain spaces')

        validEmail  = '^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'
        if re.search(validEmail,user.userEmailAddress) is None:
            raise Exception('Invalid Email address')

        password = Password(user.userPassword)
        password.doesPasswordMeetComplexityRequirement()

        userRoles = ('Admin', 'Scrum Master', 'Developer')
        if user.userRole not in userRoles:
            raise Exception('Invalid User Role')

    @staticmethod
    def validateCard(item):
        assert item is not None
        assert item.itemType is not None
        assert item.itemTitle is not None
        assert item.itemDescription is not None
        if item.itemType == '':
            raise Exception('Item Type cannot be Blank')
        if item.itemTitle == '':
            raise Exception('Item Title cannot be Blank')
        if item.itemDescription == '':
            raise Exception('Item Description cannot be Blank')

    @staticmethod
    def validateSprint(sprint):
        assert sprint.sprintName is not None
        if sprint.sprintName == '':
            raise Exception('Sprint Name cannot be blank')

    @staticmethod
    def validateComment(comment):
        assert comment is not None
        assert comment.commentContent is not None
        assert comment.commentItemID is not None
        assert comment.commentUserID is not None
