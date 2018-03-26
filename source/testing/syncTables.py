import ScrumblesData
import time

print('Initializing DataBlock')
db = ScrumblesData.DataBlock()
db.lockDown()

db.conn.connect()
print('Clearing Data From ProjectItemTable')
db.conn.setData('DELETE FROM ProjectItemTable')
print('Clearing Data From projectUserTable')
db.conn.setData('DELETE FROM ProjectUserTable')
db.conn.close()

print('Data deleted from Tables')

#if an item is assigned to a sprint, the item should be
#assigned to the project the sprint is assigned to
print('Re-applying Vectors')
for P in db.projects:
    for S in P.listOfAssignedSprints:
        print('Reticulating Items in Projects')
        for I in S.listOfAssignedItems:
            time.sleep(2)
            print('\tAdding Item',I.itemTitle,'to project',P.projectName)
            db.addItemToProject(P,I)
        print('Reticulating Users in Projects')
        for U in S.listOfAssignedUsers:
            print('\tAdding User', U.userName, 'to project', P.projectName)
            time.sleep(2)
            db.addUserToProject(P,U)
print('Shutting down gracefully')
db.unlock()
db.shutdown()