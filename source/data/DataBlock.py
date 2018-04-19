from data.ScrumblesData import DataBaseLoginInfo, ScrumblesData, debug_ObjectdumpList
from data.Query import *
from data import RemoteUpdate, ScrumblesObjects
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
    itemMap = {}
    sprintMap = {}
    projectMap = {}
    userMap = {}
    commentMap = {}

    def __init__(self,mode=None,):
        self.dbLogin = DataBaseLoginInfo('login.txt')
        self.conn = ScrumblesData(self.dbLogin)
        self.mode = mode
        self.isLoading = True
        self.firstLoad = True
        if mode is None:
            logging.info('Initializing DataBlock Object')
            self.alive = True

            self.listener = RemoteUpdate.RemoteUpdate()
            self.lock = threading.Lock()
            self.size = self.getLen()
            self.updaterThread = threading.Thread(target = self.updater, name='UpdaterThread')
            self.listenerThread = threading.Thread(target=self.listener.start, name='UpdateListener')
            self.cv = threading.Condition()

            self.listenerThread.start()
            self.updaterThread.start()

    def __del__(self):
        if self.mode != 'test':

            self.shutdown()
            

    def onConnectionLoss(self,func):
        while self.listener.alive:
            time.sleep(1)
            if not self.alive:
                return

        func()


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

    def updater(self):
        logging.info('Updater Thread %s started' % threading.get_ident())
        if self.firstLoad:
            self.updateAllObjects()
            self.firstLoad = False

        while self.alive:
            time.sleep(1)

            if self.listener.isDBChanged:

                time.sleep(2)   # <<--- This is the thread timing tweak.
                # with self.cv:
                #     self.cv.wait_for(self.updateAllObjects)
                self.lock.acquire(timeout=2)
                self.updateAllObjects()
                self.lock.release()
                self.lock.acquire(timeout=2)
                self.executeUpdaterCallbacks()
                self.lock.release()
                self.lock.acquire(timeout=2)
                self.listener.isDBChanged = False
                self.lock.release()

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


                try:
                    func()
                except Exception as e:
                    logging.exception('Function {} failed to update'.format(str(func)))

    def shutdown(self):

        logging.info('Shutting down Thread %s'%threading.get_ident())
        self.alive = False
        if self.mode != 'test':
            self.listener.stop()





    def updateAllObjects(self):
        if self.firstLoad:
            time.sleep(1)
        self.isLoading = True
        funcStartTime = time.clock()

        self.conn.connect()
        self.users.clear()
        self.items.clear()
        self.projects.clear()
        self.comments.clear()
        self.tags.clear()
        self.sprints.clear()
        self.itemMap = {}
        self.sprintMap = {}
        self.commentMap = {}
        self.projectMap = {}
        self.userMap = {}
        #print('getting tables')
        loopStartTime = time.clock()
        userTable = self.conn.getData(Query.getAllUsers)
        itemTable = self.conn.getData(Query.getAllCards)
        projectTable = self.conn.getData(Query.getAllProjects)
        commentTable = self.conn.getData(Query.getAllComments)
        sprintTable = self.conn.getData(Query.getAllSprints)
        userToProjectRelationTable = self.conn.getData(Query.getAllUserProject)
        itemToProjectRelationTable = self.conn.getData(Query.getAllProjectItem)
        itemTimeLineTable = self.conn.getData('SELECT * FROM CardTimeLine')
        epicTable = self.conn.getData('SELECT * FROM EpicTable')

        self.conn.close()

        #print('Tables loaded in %fms' % ((time.clock()-loopStartTime)*1000) )

        loopStartTime = time.clock()
        #print('splicing vectors')

        timeLineMap = self.mapTimeline(itemTimeLineTable)
        epicMap = self.buildEpicMap(epicTable)
        for comment in commentTable:
            Comment = ScrumblesObjects.Comment(comment)
            self.comments.append(Comment)
            self.commentMap[Comment.commentID] = Comment
        #print('Comment List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for item in itemTable:
            Item = ScrumblesObjects.Item(item)
            Item.listOfComments = [C for C in self.comments if C.commentItemID == Item.itemID]
            self.applyItemLine(Item,timeLineMap)
            # try:
            #     Item.itemTimeLine = timeLineMap[Item.itemID]
            # except KeyError:
            #     timeLineMap = self.reloadTimeLineMap()
            if 'AssignedToSPrint' in Item.itemTimeLine:
                Item.itemTimeLine['AssignedToSprint'] = Item.itemTimeLine['AssignedToSPrint']
            #self.populateItemTimeLine(Item,timeLineMap)
            self.itemMap[Item.itemID] = Item
            self.items.append(Item)
        #print('Item List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for I in self.items:
            if I.itemID in epicMap:  #epicMap[subitemID]->EpicID
                self.itemMap[epicMap[I.itemID]].subItemList.append(I) #itemMap[itemID]->Item
        #print('Item subitems spliced in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for user in userTable:
            User = ScrumblesObjects.User(user)
            User.listOfAssignedItems = [ I for I in self.items if I.itemUserID == User.userID ]
            User.listOfComments = [ C for C in self.comments if C.commentUserID == User.userID ]
            self.users.append(User)
            self.userMap[User.userID] = User
        #print('User List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for sprint in sprintTable:
            Sprint = ScrumblesObjects.Sprint(sprint)
            Sprint.listOfAssignedItems = [I for I in self.items if I.itemSprintID == Sprint.sprintID]
            Sprint.listOfAssignedUsers = [U for U in self.users if U.userID in [I.itemUserID for I in Sprint.listOfAssignedItems]]
            self.sprints.append(Sprint)
            self.sprintMap[Sprint.sprintID] = Sprint
        #print('Sprint List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for project in projectTable:
            Project = ScrumblesObjects.Project(project)
            Project.listOfAssignedSprints = [S for S in self.sprints if S.projectID == Project.projectID]
            self.projects.append(Project)
            self.projectMap[Project.projectID] = Project
        #print('Project List Built in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for user in self.users:
            for dict in userToProjectRelationTable:
                if dict['UserID'] == user.userID:
                    for project in self.projects:
                        if dict['ProjectID'] == project.projectID:
                            user.listOfProjects.append(project)
        #print('Users Spliced to Projects in %fms' % ((time.clock() - loopStartTime) * 1000))

        loopStartTime = time.clock()
        for project in self.projects:
            for dict in userToProjectRelationTable:
                if dict['ProjectID'] == project.projectID:
                    for user in self.users:
                        if dict['UserID'] == user.userID:
                            project.listOfAssignedUsers.append(user)
            #print('Projects spliced to users in %fms' % ((time.clock() - loopStartTime) * 1000))

            loopStartTime = time.clock()
            for dict in itemToProjectRelationTable:
                if dict['ProjectID'] == project.projectID:
                    for item in self.items:
                        if dict['ItemID'] == item.itemID:
                            item.projectID = project.projectID

                            project.listOfAssignedItems.append(item)
        #print('Items Spliced to Projects in %fms' % ((time.clock() - loopStartTime) * 1000))

        #self.debugDump()
        #print('Data Loaded in %fs' % (time.clock()-funcStartTime))
        self.isLoading = False
        return True

    def applyItemLine(self, Item, timeLineMap):
        try:
            Item.itemTimeLine = timeLineMap[Item.itemID]
        except KeyError as e:
            time.sleep(1)
            logging.exception('Error applying item TimeLine')

            self.applyItemLine( Item, self.reloadTimeLineMap() )
        return

    @dbWrap
    def reloadTimeLineMap(self):
        itemTimeLineTable = self.conn.getData('SELECT * FROM CardTimeLine')
        timeLineMap = self.mapTimeline(itemTimeLineTable)
        return timeLineMap

    def mapTimeline(self,QResult):
        #QResult is a tuple of dicts
        #I want to map each cardID to a dict
        timeLineMap = {}
        for dict in QResult:
            timeLineMap[dict['CardID']] = dict
        return timeLineMap

    def buildEpicMap(self,epicTable):
        epicMap = {}
        for dict in epicTable:
            epicMap[dict['SubitemID']] = dict['EpicID']
        return epicMap
    def validateData(self):
        return self.getLen() > 0

    @dbWrap
    def addUserToProject(self,project,user):
        logging.info('Adding User %s to project %s' % (user.userName,project.projectName))
        if user not in project.listOfAssignedUsers:
            self.conn.setData(ProjectQuery.addUser(project,user))
        else:
           logging.warning('User already assigned to project')

    @dbWrap
    def removeUserFromProject(self,project,user):
        logging.info('Removing User %s from project %s' %(user.userName,project.projectName) )
        itemList = []
        for item in self.items:
            if item in project.listOfAssignedItems:
                if item.itemUserID == user.userID:
                    itemList.append(item)


        self.conn.setMulti(CardQuery.removeUserFromListOfCards(itemList))
        self.conn.setData(ProjectQuery.removeUser(project,user))



    @dbWrap
    def addComment(self,comment):
        logging.warning('Depreciated function call: Adding Comment to database: %s' % comment.commentContent)
        self.conn.setData(Query.createObject(comment))


    @dbWrap
    def assignUserToItem(self,user,item):
        oldItem = item
        if user is not None:
            logging.info('Assigning User %s to item %s.'%(user.userName,item.itemTitle))
            item.itemUserID = user.userID
            item.itemStatus = item.statusTextToNumberMap['Assigned']
        else:
            logging.info('Assinging None User to item %s.' % item.itemTitle)
            item.itemUserID = None
            item.itemStatus = item.statusTextToNumberMap['Not Assigned']

        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'Assign user to item'
        comment.commentItemID = item.itemID
        comment.commentUserID = 0
        self.conn.setMulti(CardQuery.updateCard(item, oldItem, comment))

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
        if repr(obj) == "<class 'data.ScrumblesObjects.Item'>" or type(obj) == ScrumblesObjects.Item:
            self.conn.setData(TimeLineQuery.newItem(obj))
        logging.info('Adding new object %s to database' % repr(obj))
        self.conn.setData(Query.createObject(obj))

    def printQ(self,Q):
        sql = Q[0].splitlines()
        params = Q[1]
        for index, line in enumerate(sql):
            print('Line:{}\n{}\n{}'.format(index+1,line,params[index+1]))


    @dbWrap
    def updateScrumblesObject(self,obj,oldObj=None,comment=None):
        logging.info('Updating object %s to database' % repr(obj))
        if repr(obj) == "<class 'data.ScrumblesObjects.Item'>" or type(obj) == ScrumblesObjects.Item:
            assert oldObj is not None, 'old object cannot be none'
            assert comment is not None, 'Comment cannot be none'
            Q = CardQuery.updateCard(obj,oldObj,comment)
            self.conn.setMulti(Q)

        else:
            print('Not an Item')
            self.conn.setData(Query.updateObject(obj))

    @dbWrap
    def deleteScrumblesObject(self,obj,project=None):
        logging.info('Deleting object %s from database' % repr(obj))
        if repr(obj) == "<class 'data.ScrumblesObjects.Item'>" or type(obj) == ScrumblesObjects.Item:
            self.conn.setMulti(CardQuery.deleteCard(obj))
        elif repr(obj) == "<class 'data.ScrumblesObjects.Sprint'>" or type(obj) == ScrumblesObjects.Sprint:
            self.conn.setMulti(SprintQuery.deleteSprint(obj))
        else:
            self.conn.setData(Query.deleteObject(obj))

    @dbWrap
    def removeItemFromComments(self,item):
        logging.info('Removing item from comments database')
        self.conn.setData(CommentQuery.deleteItemFromComments(item))


    @dbWrap
    def modifiyItemPriority(self,item,priority):
        logging.info('Modifying item %s priority to %s' % (item.itemTitle,item.priorityNumberToTextMap[priority]))
        assert priority in range(0,3)
        oldItem = item
        item.itemPriority = priority
        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'item priority changed'
        comment.commentItemID = item.itemID
        comment.commentUserID = 0
        self.conn.setMulti(CardQuery.updateCard(item, oldItem, comment))

    @dbWrap
    def modifyItemStatus(self,item,status):
        logging.info('Modifying item %s status to %s' % (item.itemTitle,item.statusNumberToTextMap[status]))
        assert status in range(0,5)
        oldItem = item
        item.itemStatus = item.statusNumberToTextMap[status]
        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'modify item status'
        comment.commentItemID = item.itemID
        comment.commentUserID = 0

        try:
            self.conn.setMulti(CardQuery.updateCard(item, oldItem, comment))
        except Exception as e:
            item.itemStatus = oldItem.itemStaus
            raise e

    @dbWrap
    def modifyItemStatusByString(self,item,status):
        logging.info('Modifying item %s to status %s.' % (item.itemTitle,status))
        oldItem = item
        item.itemStatus = item.statusTextToNumberMap[status]
        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'Modify Item Status'
        comment.commentItemID = item.itemID
        comment.commentUserID = 0
        self.conn.setMulti(CardQuery.updateCard(item, oldItem, comment))

    @dbWrap
    def assignItemToSprint(self,item,sprint):
        logging.info('Assigning Item %s to Sprint %s.'%(item.itemTitle,sprint.sprintName))
        oldItem = item
        item.itemSprintID = sprint.sprintID
        item.itemDueDate = sprint.sprintDueDate
        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'item assigned to sprint'
        comment.commentItemID = item.itemID
        comment.commentUserID = 0
        self.conn.setMulti(CardQuery.updateCard(item,oldItem,comment))


    @dbWrap
    def removeItemFromSprint(self,item):

        logging.info('Removing Item %s from sprint %s.'%(item.itemTitle,str(item.itemSprintID)))
        oldItem = item
        item.itemSprintID = 0
        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'item removed from sprint'
        comment.commentItemID = item.itemID
        comment.commentUserID = 0
        self.conn.setMulti(CardQuery.updateCard(item, oldItem, comment))

    @dbWrap
    def promoteItemToEpic(self,item):
        logging.info('Promoting Item %s to Epic'% item.itemTitle)
        oldItem = item
        comment = ScrumblesObjects.Comment()
        comment.commentContent = 'promoted item to epic'
        comment.commentItemID = item.itemID
        comment.commentUserID = 0
        item.itemType = 'Epic'
        self.conn.setMulti(CardQuery.updateCard(item, oldItem, comment))

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


