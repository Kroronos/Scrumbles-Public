import ScrumblesData


db = ScrumblesData.DataBlock()
db.conn.connect()

db.conn.setData('DELETE FROM ProjectItemTable')
db.conn.setData('DELETE FROM ProjectUserTable')

db.conn.close()


#if an item is assigned to a sprint, the item should be
#assigned to the project the sprint is assigned to
for P in db.projects:
    for S in P.listOfAssignedSprints:
        for I in S.listOfAssignedItems:

            db.addItemToProject(P,I)
        for U in S.listOfAssignedUsers:
            db.addUserToProject(P,U)

db.shutdown()