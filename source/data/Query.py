from data import ScrumblesObjects
import hashlib,re
from datetime import datetime


class QueryException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Query:
    getAllUsers = 'SELECT * FROM UserTable'
    getAllSprints = 'SELECT * FROM SprintTable'
    getAllCards = 'SELECT * FROM CardTable'
    getAllComments = 'SELECT * FROM CommentTable'
    getAllProjects = 'SELECT * FROM ProjectsTable'
    getAllUserProject = 'SELECT * FROM ProjectUserTable'
    getAllProjectItem = 'SELECT * FROM ProjectItemTable'
    validItemTypes = ['User Story', 'Epic', 'Bug','Chore','Feature']
    @staticmethod
    def getUserByUsernameAndPassword(username, password):
        hashedPassword = Password(password)
        hashedPassword.encrypt()
        query = 'SELECT * from UserTable WHERE (BINARY UserName=\'%s\') AND (BINARY UserPassword=\'%s\')' % (
            username, str(hashedPassword))
        return query

    @staticmethod
    def assignCardToSprint(item, sprint):
        if item is None or sprint is None:
            raise QueryException('Item or Sprint is None type')
        if item.itemID is None:
            raise QueryException('ItemID is None type')
        if sprint.sprintID is None:
            raise QueryException('SprintID is None type')

        query = ''''UPDATE CardTable SET CardDueDate = ( 
                SELECT DueDate FROM SprintTable WHERE SprintID=%s), 
                SprintID = %s, Status=1 WHERE CardID = %s'''
        return query, (sprint.sprintID, sprint.sprintID, item.itemID)

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
        query = 'INSERT INTO ProjectsTable (ProjectID, ProjectName) VALUES (%s,%s)'
        return query, (project.projectID,project.projectName)

    @staticmethod
    def deleteProject(project):
        assert project is not None
        query = 'DELETE FROM ProjectsTable WHERE ProjectID=%s'
        return query , (project.projectID,)

    @staticmethod
    def updateProject(project):
        assert project is not None
        query = 'UPDATE ProjectsTable SET ProjectName=%s WHERE ProjectID = %s'
        return query, (project.projectName,project.projectID)

    @staticmethod
    def addUser(project, user):
        query = 'INSERT INTO ProjectUserTable (UserID, ProjectID) VALUES (%s,%s)'
        return query , (user.userID,project.projectID)

    @staticmethod
    def removeUser(project, user):
        query = 'DELETE FROM ProjectUserTable WHERE ProjectID=%s AND UserID=%s'
        return query, (project.projectID, user.userID)

    @staticmethod
    def addItem(project, item):
        query = 'INSERT INTO ProjectItemTable (ItemID,ProjectID) VALUES (%s,%s)'
        return query, (item.itemID,project.projectID)

    @staticmethod
    def removeItem(project, item):
        query = '''DELETE FROM ProjectItemTable WHERE ProjectID=%s AND ItemID=%s;
        '''
        return query, (project.projectID,item.itemID)


class SprintQuery(Query):
    @staticmethod
    def createSprint(sprint):
        ObjectValidator.validate(sprint)
        sprintMap = {'SprintName': 'NULL', 'StartDate': 'NULL', 'DueDate': 'NULL', 'ProjectID': 'NULL'}
        sprintMap['SprintID'] = sprint.sprintID
        if sprint.sprintName is not None:
            sprintMap['SprintName'] = sprint.sprintName
        if sprint.sprintStartDate is not None:
            sprintMap['StartDate'] = sprint.sprintStartDate
        if sprint.sprintDueDate is not None:
            sprintMap['DueDate'] = sprint.sprintDueDate
        if sprint.projectID is not None:
            sprintMap['ProjectID'] = sprint.projectID

        query = '''INSERT INTO SprintTable (SprintID, SprintName, StartDate,DueDate,ProjectID) VALUES (
        %s,%s,%s,%s,%s)'''

        return query, (sprintMap['SprintID'], sprintMap['SprintName'], sprintMap['StartDate']
                                              , sprintMap['DueDate'], sprintMap['ProjectID'])

    @staticmethod
    def updateSprint(sprint):
        assert sprint is not None
        assert sprint.sprintID is not None

        query = '''UPDATE SprintTable SET StartDate=%s,DueDate=%s, SprintName=%s WHERE SprintID=%s'''
        return query, ( sprint.sprintStartDate,
                    sprint.sprintDueDate,
                    sprint.sprintName,
                    sprint.sprintID )

    @staticmethod
    def getSprintBySprintID(sprintID):
        assert sprintID is not None
        query = 'SELECT * FROM SprintTable WHERE SprintID=%s'
        return query, (sprintID,)

    @staticmethod
    def deleteSprint(sprint):
        assert sprint is not None
        query = '''DELETE FROM SprintTable WHERE SprintID=%s
                   UPDATE CardTable SET SprintID=%s WHERE SprintID=%s'''
        parameterMap = {1:(sprint.sprintID,),2:(None,sprint.sprintID)}
        return query,parameterMap


class CardQuery(Query):
    @staticmethod
    def createCard(item):
        ObjectValidator.validate(item)
        query = '''INSERT INTO CardTable ( 
                CardId, 
                CardType,
                CardPriority, 
                CardTitle, 
                CardDescription,
                CardCreatedDate, 
                CardPoints,
                Status) VALUES (
                %s,%s,%s,%s,%s,
                NOW(),%s,0) '''

        return query , (
                    item.itemID,
                    item.itemType,
                    item.itemPriority,
                    item.itemTitle,
                    item.itemDescription,
                    item.itemPoints
                )

    @staticmethod
    def updateCard(item,oldItem,comment):
        maxDate = datetime(9999, 12, 31, 23, 59, 59)
        sql = ''
        params = {}
        assert item is not None
        assert item.itemID is not None
        assert item.itemType in Query.validItemTypes
        assert item.itemPriority in range(0, 3)

        sql += 'UPDATE CardTable SET  CardType=%s, CardPriority=%s, CardTitle=%s,CardDescription=%s, CardDueDate=%s,CardCodeLink=%s, SprintID=%s, UserID=%s, Status=%s, CardPoints=%s  WHERE CardID=%s\n'
        params[1] = (item.itemType,item.itemPriority,item.itemTitle,item.itemDescription,item.itemDueDate,item.itemCodeLink,item.itemSprintID,item.itemUserID,item.itemStatus,item.itemPoints,item.itemID)
        sql += 'INSERT INTO CommentTable (CommentID, CommentTimeStamp,CommentContent,CardID,UserID) VALUES ( %s,NOW(), %s,%s,%s)\n'
        params[2] = (comment.commentID,comment.commentContent,comment.commentItemID,comment.commentUserID)

        nextParam = 3

        if oldItem.itemSprintID == item.itemSprintID:
            pass

        elif oldItem.itemSprintID is None and item.itemSprintID is not None:
            sql +='UPDATE CardTimeLine SET AssignedToSprint=NOW() WHERE CardID=%s\n'
            params[nextParam] = (item.itemID,)
            nextParam += 1

        elif oldItem.itemSprintID is not None and item.itemSprintID is None:
            sql +='UPDATE CardTimeLine SET AssignedToSprint=%s WHERE CardID=%s\n'
            params[nextParam] = (maxDate,item.itemID)
            nextParam += 1

        elif oldItem.itemSprintID != item.itemSprintID:
            sql +='UPDATE CardTimeLine SET AssignedToSprint=NOW() WHERE CardID=%s\n'
            params[nextParam] = (item.itemID,)
            nextParam += 1

        if oldItem.itemUserID == item.itemUserID:
            pass

        elif oldItem.itemUserID is None and item.itemUserID is not None:
            sql +='UPDATE CardTimeLine SET  AssignedToUser=NOW() WHERE CardID=%s\n'
            params[nextParam] = (item.itemID,)
            nextParam += 1

        elif oldItem.itemUserID is not None and item.itemUserID is None:
            sql += 'UPDATE CardTimeLine SET  AssignedToUser=%s WHERE CardID=%s\n'
            params[nextParam] = (maxDate, item.itemID)
            nextParam += 1

        elif oldItem.itemUserID != item.itemUserID:
            sql += 'UPDATE CardTimeLine SET  AssignedToUser=NOW() WHERE CardID=%s\n'
            params[nextParam] = (item.itemID,)
            nextParam += 1

        if oldItem.itemType == item.itemType:
            pass

        elif oldItem.itemType == 'Epic' and item.itemType != 'Epic':
            sql += 'DELETE FROM EpicTable WHERE EpicID=%s\n'
            params[nextParam] = (item.itemID,)
            nextParam += 1
            pass

        elif oldItem.itemType != 'Epic' and item.itemType == 'Epic':
            pass



        return sql,params


    @staticmethod
    def removeUserFromListOfCards(itemList):
        sql = ''
        params = {}
        for i, item in enumerate(itemList):
            sql+= 'UPDATE CardTable SET UserID=%s WHERE CardID=%s\n'
            params[i+1] = (None,item.itemID)

        return sql,params




    @staticmethod
    def deleteCard(item):
        assert item is not None
        ID = item.itemID
        query = '''DELETE FROM CardTable WHERE CardID=%s;
        DELETE FROM EpicTable WHERE SubitemID=%s;
        DELETE FROM EpicTable WHERE EpicID=%s;
        DELETE FROM CardTimeLine WHERE CardID=%s;
        DELETE FROM CommentTable WHERE CardID=%s;
        DELETE FROM ProjectItemTable WHERE ItemID=%s'''
        parameterMap = {1: (ID,), 2:(ID,), 3:(ID,), 4:(ID,),5:(ID,),6:(ID,)}
        return query,parameterMap
    @staticmethod
    def getEpicSubitems(item):
        assert item is not None
        query = 'Select SubitemID From EpicTable WHERE EpicID=%s' % (item.itemID)
        return query
    @staticmethod
    def removeItemFromEpic(item):
        assert item is not None
        query = 'DELETE FROM EpicTable WHERE SubitemID=%s'
        return query, (item.itemID,)
    @staticmethod
    def deleteEpic(item):
        assert item is not None
        query = 'DELETE FROM EpicTable WHERE EpicID=%s'
        return query,(item.itemID,)
    @staticmethod
    def assignItemToEpic(item,epic):
        assert item is not None
        assert epic.itemType == 'Epic'
        query = 'INSERT INTO EpicTable (EpicID,SubitemID) VALUES (%s,%s)'
        return query,(epic.itemID,item.itemID)

class UserQuery(Query):

    @staticmethod
    def createUser(user):
        ObjectValidator.validate(user)
        password = Password(user.userPassword)
        password.encrypt()
        query = 'INSERT INTO UserTable (UserID, userName,UserEmailAddress,UserPassword,UserRole) VALUES (%s,%s,%s,%s,%s)'
        return query,(user.userID, user.userName, user.userEmailAddress, password, user.userRole)

    @staticmethod
    def updateUser(user):
        assert user is not None
        assert user.userID is not None
        query = '''UPDATE UserTable SET  
                UserName=%s,
                UserEmailAddress=%s,
                UserPassword=%s,
                UserRole=%s  WHERE 
                UserID=%s'''
        return query, ( user.userName, user.userEmailAddress,user.userPassword,user.userRole,user.userID )

    @staticmethod
    def deleteUser(user):
        assert user is not None
        query = 'DELETE FROM UserTable WHERE UserID=%s'
        return query , (user.userID,)


class CommentQuery(Query):
    @staticmethod
    def createComment(comment):
        query = '''INSERT INTO CommentTable (CommentID, CommentTimeStamp,
                CommentContent,
                CardID,
                UserID) VALUES ( %s,NOW(), %s,%s,%s)'''
        return query, (
                    comment.commentID,
                    comment.commentContent,
                    comment.commentItemID,
                    comment.commentUserID
                )

    @staticmethod
    def updateComment(comment):
        assert comment is not None
        assert comment.commentID is not None
        query = '''UPDATE CommentTable SET CommentContent=%s WHERE CommentID=%s'''
        return query,(comment.commentContent, comment.commentID)

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
        query = 'DELETE FROM CommentTable WHERE CommentID=%s'
        return query, (comment.commentID,)
    @staticmethod
    def deleteItemFromComments(item):
        assert type(item) is ScrumblesObjects.Item
        query = 'DELETE FROM CommentTable WHERE CardID = %s'
        return query, (item.itemID)

class TimeLineQuery(Query):
    statusMap = {0: 'AssignedToUser', 1: 'AssignedToUser', 2: 'WorkStarted', 3: 'Submitted', 4: 'Completed'}
    #statusEquivalentsReverse = {'Not Assigned': 0, 'Assigned': 1, 'In Progress': 2, 'Submitted': 3, 'Complete': 4}

    @staticmethod
    def newItem(item):
        query = 'INSERT INTO CardTimeLine (CardID,Created) VALUES (%s,NOW())'
        return query, (item.itemID,)

    @staticmethod
    def timeStampItem(item):
        maxDate = datetime(9999, 12, 31, 23, 59, 59)
        if item.itemTimeLine['AssignedToSprint'] == maxDate and item.itemTimeLine['AssignedToUser'] == maxDate:
            if item.itemStatus > 1:
                raise Exception('Invalid Operation: Item must be assigned to sprint and user before changing status to %s'%item.statusNumberToTextMap[item.itemStatus])
            else:
                query = 'INSERT INTO CardTimeLine (CardID, AssignedToUser) VALUES (%s,NOW())'
                rtnTuple = (item.itemID,)
        else:
            q = 'UPDAte CardTimeLine SET %s' % TimeLineQuery.statusMap[item.itemStatus]
            if item.itemStatus > 0:
                query = q+'=NOW() WHERE CardID=%s'
                rtnTuple = (item.itemID,)

            else:
                query = q+'=%s WHERE CardID=%s'
                rtnTuple = (maxDate, item.itemID)
        return query,   rtnTuple

    @staticmethod
    def stampItemToSprint(item):
        query = 'UPDATE CardTimeLine SET AssignedToSprint=NOW() WHERE CardID=%s'
        return query, (item.itemID,)

    @staticmethod
    def getItemTimeLine(item):
        query = 'SELECT AssignedToSPrint, AssignedToUser, WorkStarted, Submitted, Completed, Created FROM CardTimeLine WHERE CardID=%i' %item.itemID
        return query


class Password:
    password = None

    def __init__(self, password):
        self.password = password

    def __str__(self):
        return self.password

    def doesPasswordMeetComplexityRequirement(self):
        # must be 8 digits, 1 uppercase, 1 lowercase, and 1 digit
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
            raise Exception(
                'Password must be 8 digits long and contain at least 1 upper case, 1 lowercase and 1 number')

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

        validEmail = '^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'
        if re.search(validEmail, user.userEmailAddress) is None:
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
        assert item.itemType in Query.validItemTypes
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
