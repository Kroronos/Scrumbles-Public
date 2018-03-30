import ScrumblesObjects
import hashlib
import re

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
            str(project.projectID), project.projectName)
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
    def addUser(project, user):
        query = 'INSERT INTO ProjectUserTable (UserID, ProjectID) VALUES (\'%s\',\'%s\')' % (
            str(user.userID), str(project.projectID)
        )
        return query

    @staticmethod
    def removeUser(project, user):
        query = 'DELETE FROM ProjectUserTable WHERE ProjectID=\'%s\' AND UserID=\'%s\'' % (
            str(project.projectID), str(user.userID)
        )
        return query

    @staticmethod
    def addItem(project, item):
        query = 'INSERT INTO ProjectItemTable (ItemID,ProjectID) VALUES (\'%s\',\'%s\')' % (
            str(item.itemID), str(project.projectID)
        )
        return query

    @staticmethod
    def removeItem(project, item):
        query = 'DELETE FROM ProjectItemTable WHERE ProjectID=\'%s\' AND ItemID=\'%s\'' % (
            str(project.projectID), str(item.itemID)
        )
        return query


class SprintQuery(Query):
    @staticmethod
    def createSprint(sprint):
        ObjectValidator.validate(sprint)
        sprintMap = {'SprintName': 'NULL', 'StartDate': 'NULL', 'DueDate': 'NULL', 'ProjectID': 'NULL'}
        sprintMap['SprintID'] = "'" + str(sprint.sprintID) + "'"
        if sprint.sprintName is not None:
            sprintMap['SprintName'] = "'" + str(sprint.sprintName) + "'"
        if sprint.sprintStartDate is not None:
            sprintMap['StartDate'] = "'" + str(sprint.sprintStartDate) + "'"
        if sprint.sprintDueDate is not None:
            sprintMap['DueDate'] = "'" + str(sprint.sprintDueDate) + "'"
        if sprint.projectID is not None:
            sprintMap['ProjectID'] = "'" + str(sprint.projectID) + "'"

        query = '''INSERT INTO SprintTable (SprintID, SprintName, StartDate,DueDate,ProjectID) VALUES (
        %s,%s,%s,%s,%s)''' % (sprintMap['SprintID'], sprintMap['SprintName'], sprintMap['StartDate']
                                              , sprintMap['DueDate'], sprintMap['ProjectID'])
        print(query)
        return query

    @staticmethod
    def updateSprint(sprint):
        assert sprint is not None
        assert sprint.sprintID is not None

        query = 'UPDATE SprintTable SET StartDate=\'%s\',' \
                'DueDate=\'%s\', SprintName=\'%s\' WHERE SprintID=%i' % (
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
                'CardId,' \
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
        itemDict['Type'] = "'" + item.itemType + "'"
        itemDict['Priority'] = "'" + str(item.itemPriority) + "'"
        itemDict['Title'] = "'" + item.itemTitle + "'"
        itemDict['Descr'] = "'" + item.itemDescription + "'"
        itemDict['DueDate'] = 'NULL'
        if item.itemDueDate is not None:
            itemDict['DueDate'] = "'" + str(item.itemDueDate) + "'"
        itemDict['Sprint'] = "'" + str(item.itemSprintID) + "'"
        itemDict['User'] = "'" + str(item.itemUserID) + "'"
        itemDict['Status'] = "'" + str(item.itemStatus) + "'"
        itemDict['CodeLink'] = 'NULL'
        if item.itemCodeLink is not None:
            itemDict['CodeLink'] = "'" + item.itemCodeLink + "'"
        itemDict['Points'] = "'" + str(item.itemPoints) + "'"

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
                CardPoints=%s WHERE CardID=%s''' % (
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
