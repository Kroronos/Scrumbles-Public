### test creation and deletion of a Sprint object
import datetime
from data import ScrumblesData, ScrumblesObjects


def testSprints(dataConnection):
    getAllSprintsQuery = ScrumblesData.Query.getAllSprints
    testSprint = ScrumblesObjects.Sprint()
    testSprint.sprintName = 'UniqueSprintName'
    testSprint.sprintStartDate = datetime.date(2018,1,31)
    testSprint.sprintDueDate = datetime.date(2018,2,27)

    testSprintCreationQuery = ScrumblesData.Query.createObject(testSprint)
    assert testSprintCreationQuery is not None
    dataConnection.connect()
    allSprintsQueryResult = dataConnection.getData(getAllSprintsQuery)
    dataConnection.setData(testSprintCreationQuery)
    allNewSprintsQueryResult = dataConnection.getData(getAllSprintsQuery)
    dataConnection.close()

    assert len(allNewSprintsQueryResult) != len(allSprintsQueryResult)

    testSprintSearchQuery = ScrumblesData.SprintQuery.getSprintBySprintID(testSprint.sprintID)
    assert testSprintSearchQuery is not None
    dataConnection.connect()
    foundTestSprintResult = dataConnection.getData(testSprintSearchQuery)
    dataConnection.close()
    foundSprint = ScrumblesObjects.Sprint(foundTestSprintResult[0])
    assert foundSprint.sprintName == testSprint.sprintName
    dataConnection.connect()
    dataConnection.setData(ScrumblesData.Query.deleteObject(foundSprint))
    foundTestSprintResult = dataConnection.getData(testSprintSearchQuery)
    dataConnection.close()
    assert foundTestSprintResult == ()
    print('Sprint',testSprint.sprintID,' Data successfully created and deleted on remote server')