import ScrumblesData
from DataBlock import *
from datetime import datetime
db = DataBlock(mode='test')
maxDate = datetime(9999, 12, 31, 23, 59, 59)
db.conn.connect()

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










#if an item is assigned to a sprint, the item should be
#assigned to the project the sprint is assigned to
# for P in db.projects:
#     for S in P.listOfAssignedSprints:
#         for I in S.listOfAssignedItems:
#
#             db.addItemToProject(P,I)
#         for U in S.listOfAssignedUsers:
#             db.addUserToProject(P,U)


db.conn.close()
db.shutdown()