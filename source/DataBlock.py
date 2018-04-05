from ScrumblesData import DataBaseLoginInfo, ScrumblesData, debug_ObjectdumpList
from Query import *
import ScrumblesObjects, remoteUpdate
import logging, threading, time

def dbWrap(func):
    def wrapper(self,*args):
        self.conn.connect()
        func(self,*args)
        self.conn.close()
    return wrapper

class DataBlock:
    users = []
    items = []
    projects = []
    comments = []
    tags = []
    sprints = []
    updaterCallbacks = []


    def __init__(self,mode=None,):
        self.dbLogin = DataBaseLoginInfo('login.txt')
        self.conn = ScrumblesData(self.dbLogin)
        self.mode = mode
        self.isLoading = True
        self.firstLoad = True
        if mode is None:
            logging.info('Initializing DataBlock Object')
            self.alive = True

            self.listener = remoteUpdate.RemoteUpdate()
            self.lock = threading.Lock()
            #self.updateAllObjects()
            self.size = self.getLen()
            self.updaterThread = threading.Thread(target = self.updater, args=())
            self.cv = threading.Condition()

            self.updaterThread.start()

    def __del__(self):
        if self.mode != 'test':
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
            print('Dumping subitems in item')
            debug_ObjectdumpList(I.subItemList)
        print('\nDumping Comments')
        debug_ObjectdumpList(self.comments)




    def updateAllObjects(self):
        self.isLoading = True
        funcStartTime = time.clock()
        print('connecting')
        self.conn.connect()
        self.users.clear()
        self.items.clear()
        self.projects.clear()
        self.comments.clear()
        self.tags.clear()
        self.sprints.clear()
        print('getting tables')
        loopStartTime = time.clock()
        userTable = self.conn.getData(Query.getAllUsers)
        itemTable = self.conn.getData(Query.getAllCards)
        projectTable = self.conn.getData(Query.getAllProjects)
        commentTable = self.conn.getData(Query.getAllComments)
        sprintTable = self.conn.getData(Query.getAllSprints)
        userToProjectRelationTable = self.conn.getData(Query.getAllUserProject)
        itemToProjectRelationTable = self.conn.getData(Query.getAllProjectItem)
        self.conn.close()

        print('Tables loaded in %fms' % ((time.clock()-loopStartTime)*1000) )

        loopStartTime = time.clock()
        print('splicing vectors')
        for comment in commentTable:
            Comment = ScrumblesObjects.Comment(comment)
            self.comments.append(Comment)
        print('Comment List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for item in itemTable:
            Item = ScrumblesObjects.Item(item)
            Item.listOfComments = [C for C in self.comments if C.commentItemID == Item.itemID]
            self.populateItemTimeLine(Item)
            self.items.append(Item)
        print('Item List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for I in self.items:
            if I.itemType == 'Epic':
                self.populateSubItems(I)
        print('Item subitems spliced in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for user in userTable:
            User = ScrumblesObjects.User(user)
            User.listOfAssignedItems = [ I for I in self.items if I.itemUserID == User.userID ]
            User.listOfComments = [ C for C in self.comments if C.commentUserID == User.userID ]
            self.users.append(User)
        print('User List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for sprint in sprintTable:
            Sprint = ScrumblesObjects.Sprint(sprint)
            Sprint.listOfAssignedItems = [I for I in self.items if I.itemSprintID == Sprint.sprintID]
            Sprint.listOfAssignedUsers = [U for U in self.users if U.userID in [I.itemUserID for I in Sprint.listOfAssignedItems]]
            self.sprints.append(Sprint)
        print('Sprint List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for project in projectTable:
            Project = ScrumblesObjects.Project(project)
            Project.listOfAssignedSprints = [S for S in self.sprints if S.projectID == Project.projectID]
            self.projects.append(Project)
        print('Project List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for user in self.users:
            for dict in userToProjectRelationTable:
                if dict['UserID'] == user.userID:
                    for project in self.projects:
                        if dict['ProjectID'] == project.projectID:
                            user.listOfProjects.append(project)
        print('Users Spliced to Projects in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for project in self.projects:
            for dict in userToProjectRelationTable:
                if dict['ProjectID'] == project.projectID:
                    for user in self.users:
                        if dict['UserID'] == user.userID:
                            project.listOfAssignedUsers.append(user)
            print('Projects spliced to users in %fms' % ((time.clock() - loopStartTime) * 1000))

            loopStartTime = time.clock()
            for dict in itemToProjectRelationTable:
                if dict['ProjectID'] == project.projectID:
                    for item in self.items:
                        if dict['ItemID'] == item.itemID:
                            item.projectID = project.projectID

                            project.listOfAssignedItems.append(item)
        print('Items Spliced to Projects in %fms' % ((time.clock() - loopStartTime) * 1000))

        #self.debugDump()
        print('Data Loaded in %fs' % (time.clock()-funcStartTime))
        self.isLoading = False
        return True

    def validateData(self):
        return self.getLen() > 0

    @dbWrap
    def addUserToProject(self,project,user):
        logging.info('Adding User %s to project %s' % (user.UserName,project.projectName))
        if user not in project.listOfAssignedUsers:
            self.conn.setData(ProjectQuery.addUser(project,user))
        else:
           logging.warning('User already assigned to project')

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
        if user is not None:
            logging.info('Assigning User %s to item %s.'%(user.userName,item.itemTitle))
            item.itemUserID = user.userID
            item.itemStatus = item.statusTextToNumberMap['Assigned']
        else:
            logging.info('Assinging None User to item %s.' % item.itemTitle)
            item.itemUserID = None
            item.itemStatus = item.statusTextToNumberMap['Not Assigned']

        self.conn.setData(Query.updateObject(item))
        self.conn.setData(TimeLineQuery.timeStampItem(item))

    @dbWrap
    def addItemToProject(self,project,item):
        logging.info('Adding item %s to project %s.' %(item.itemTitle,project.projectName))
        if item not in project.listOfAssignedItems:
            item.projectID = project.projectID
            self.conn.setData(ProjectQuery.addItem(project,item))
        else:
           logging.warning('Item already assigned to project')
    @dbWrap
    def removeItemFromProject(self,project,item):
        logging.info('Removing item %s from project %s.' % (item.itemTitle,project.projectName))
        item.projectID = 0
        self.conn.setData(ProjectQuery.removeItem(project,item))

    @dbWrap
    def addNewScrumblesObject(self,obj):
        if type(obj) == ScrumblesObjects.Item:
            self.conn.setData(TimeLineQuery.newItem(obj))
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
        logging.info('Modifying item %s priority to %s' % (item.itemTitle,item.priorityNumberToTextMap[priority]))
        assert priority in range(0,3)
        item.itemPriority = priority
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def modifyItemStatus(self,item,status):
        logging.info('Modifying item %s status to %s' % (item.itemTitle,item.statusNumberToTextMap[status]))
        assert status in range(0,5)
        oldStatus = item.itemStatus
        item.itemStatus = status
        try:
            self.conn.setData(TimeLineQuery.timeStampItem(item))
            self.conn.setData(Query.updateObject(item))
        except Exception as e:
            item.itemStatus = oldStatus
            raise e

    @dbWrap
    def modifyItemStatusByString(self,item,status):
        logging.info('Modifying item %s to status %s.' % (item.itemTitle,status))
        item.itemStatus = item.statusTextToNumberMap[status]
        self.conn.setData(TimeLineQuery.timeStampItem(item))
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def assignItemToSprint(self,item,sprint):
        logging.info('Assigning Item %s to Sprint %s.'%(item.itemTitle,sprint.sprintName))
        item.itemSprintID = sprint.sprintID
        item.itemDescription = sprint.sprintDueDate
        self.conn.setData(Query.updateObject(item))
        self.conn.setData(TimeLineQuery.stampItemToSprint(item))

    @dbWrap
    def removeItemFromSprint(self,item):

        logging.info('Removing Item %s from sprint %s.'%(item.itemTitle,str(item.itemSprintID)))
        item.itemSprintID = 0
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def promoteItemToEpic(self,item):
        logging.info('Promoting Item %s to Epic'% item.itemTitle)
        item.itemType = 'Epic'
        self.conn.setData(Query.updateObject(item))

    @dbWrap
    def addItemToEpic(self,item,epic):
        if item.itemType == 'Epic':
            raise Exception('Cannot Assign Epic to Epic')
        if epic.itemType != 'Epic':
            raise Exception('Item not an Epic')
        if epic.itemTitle == item.itemTitle:
            raise Exception('Epic cannot be Self Assigned')
        logging.info('Adding item %s to Epic %s' % (item.itemTitle, epic.itemTitle))
        self.conn.setData(CardQuery.assignItemToEpic(item,epic))


    def reAssignItemToEpic(self,item,epic):
        self.removeItemFromEpic(item)
        self.addItemToEpic(item,epic)

    @dbWrap
    def removeItemFromEpic(self,item):
        logging.info('Removing item %s from Epic' % item.itemTitle)
        self.conn.setData(CardQuery.removeItemFromEpic(item))

    @dbWrap
    def deleteEpic(self,item):
        assert item.itemType == 'Epic'
        logging.info('Deleting Epic %s and removing bindings' % item.itemTitle)
        self.conn.setData(CardQuery.deleteEpic(item))

    @dbWrap
    def populateSubItems(self,item):
        queryResult = self.conn.getData(CardQuery.getEpicSubitems(item))
        for dict in queryResult:
           for I in self.items:
               if dict['SubitemID'] == str(I.itemID):
                   item.subItemList.append(I)

    @dbWrap
    def populateItemTimeLine(self,item):
        queryReslt = self.conn.getData(TimeLineQuery.getItemTimeLine(item))
        if queryReslt != ():
            item.itemTimeLine = queryReslt[0]
            #This is a workaround from a funky bug between MySQL and MySQL db
            #although the Column name in the db is AssignedToSprint
            #it is coming back as AssignedToSPrint
            item.itemTimeLine['AssignedToSprint'] = item.itemTimeLine['AssignedToSPrint']

    def updater(self):
        logging.info('Updater Thread %s started' % threading.get_ident())
        threading.Thread(target=self.listener.start,args=()).start()
        if self.firstLoad:
            self.updateAllObjects()
            self.firstLoad = False

        while self.alive:
            time.sleep(1)
            if self.listener.isDBChanged:
                time.sleep(1)
                with self.cv:
                    self.cv.wait_for(self.updateAllObjects)

                    self.executeUpdaterCallbacks()
                    self.listener.isDBChanged = False


    def turnOffListener(self):
        self.alive = False
    def turnOnListener(self):
        self.alive = True

    def packCallback(self,callback):
        logging.info('Packing Callback %s' % str(callback))
        self.updaterCallbacks.append(callback)

    def executeUpdaterCallbacks(self):
        if len(self.updaterCallbacks) > 0:
            for func in self.updaterCallbacks:
                logging.info('Thread %s Executing Updater Func %s' % ( threading.get_ident(), str(func) ) )
                func()

    def shutdown(self):
        logging.info('Shutting down Thread %s'%threading.get_ident())
        self.alive = False
        if self.mode != 'test':
            self.listener.stop()
