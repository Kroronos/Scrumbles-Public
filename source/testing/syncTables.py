import ScrumblesData
import time

# print('Initializing DataBlock')
# db = ScrumblesData.DataBlock()
# db.lockDown()

# db.conn.connect()
# print('Clearing Data From ProjectItemTable')
# db.conn.setData('DELETE FROM ProjectItemTable')
# print('Clearing Data From projectUserTable')
# db.conn.setData('DELETE FROM ProjectUserTable')
# db.conn.close()

# from DataBlock import *
# from datetime import datetime
# db = DataBlock(mode='test')
# maxDate = datetime(9999, 12, 31, 23, 59, 59)
# db.conn.connect()

# db.conn.setData('DELETE FROM ProjectItemTable')
# db.conn.setData('DELETE FROM ProjectUserTable')




# timelineResult = db.conn.getData('SELECT * FROM CardTimeLine')
# template = timelineResult[0]
# cardIDs = [ card['CardID'] for card in timelineResult ]

# for stamp in timelineResult:
#     id = stamp['CardID']
#     db.conn.setData( ('UPDATE CardTimeLine SET Created=(SELECT CardCreatedDate FROM CardTable WHERE CardID=%s) WHERE CardID=%s' , (id ,id) ) )
#     for name in stamp:
#         if stamp[name] is None:
#             update = 'UPDATE CardTimeLine SET %s' % name
#             db.conn.setData( ( update + '=%s WHERE CardID=%s' ,('9999-12-31 23:59:59',id ) ) )










# print('Data deleted from Tables')

# #if an item is assigned to a sprint, the item should be
# #assigned to the project the sprint is assigned to

# print('Re-applying Vectors')
# for P in db.projects:
    # for S in P.listOfAssignedSprints:
        # print('Reticulating Items in Projects')
        # for I in S.listOfAssignedItems:
            # time.sleep(2)
            # print('\tAdding Item',I.itemTitle,'to project',P.projectName)
            # db.addItemToProject(P,I)
        # print('Reticulating Users in Projects')
        # for U in S.listOfAssignedUsers:
            # print('\tAdding User', U.userName, 'to project', P.projectName)
            # time.sleep(2)
            # db.addUserToProject(P,U)
# print('Shutting down gracefully')
# db.unlock()

# for P in db.projects:
#     for S in P.listOfAssignedSprints:
#         for I in S.listOfAssignedItems:
#
#             db.addItemToProject(P,I)
#         for U in S.listOfAssignedUsers:
#             db.addUserToProject(P,U)


# db.conn.close()

# db.shutdown()