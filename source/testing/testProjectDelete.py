from data import DataBlock
from data import ScrumblesObjects
from datetime import datetime
import time

report = {}
functionList = []
maxDate = datetime(9999, 12, 31, 23, 59, 59)
db = DataBlock.DataBlock(mode='test')

TProject = ScrumblesObjects.Project()
TProject.projectName = 'TProject'

TSprint_one = ScrumblesObjects.Sprint()
TSprint_one.sprintName = 'TestSprint_1'
TSprint_one.projectID = TProject.projectID
TSprint_one.sprintStartDate = datetime.now()
TSprint_one.sprintDueDate = maxDate

TSprint_two = ScrumblesObjects.Sprint()
TSprint_two.sprintName = 'TestSprint_2'
TSprint_two.projectID = TProject.projectID
TSprint_two.sprintStartDate = datetime.now()
TSprint_two.sprintDueDate = maxDate
Sprints = [TSprint_one,TSprint_two]

def test(func):
    def wrapper(*args, **kwargs):
        start = time.clock()
        try:
            func(*args, **kwargs)
            executeTime = (time.clock() - start) * 1000
            report[func.__name__] = 'Executed in {0:.2f}ms Pass'.format(executeTime)
        except Exception as e:
            executeTime = (time.clock() - start)*1000
            report[func.__name__] = 'Executed in {0:.2f}ms Fail:\n'.format(executeTime)+ str(e)

    return wrapper


@test
def testCreateProject(project):
    try:
        db.addNewScrumblesObject(project)
    except Exception as e:
        raise(e)
    db.updateAllObjects()
    project = db.projectMap[project.projectID]
    db.updateAllObjects()

@test
def testCreateSprints(sprints):
    for S in sprints:
        try:
            db.addNewScrumblesObject(S)
        except Exception as e:
            raise (e)

    db.updateAllObjects()

    for S in sprints:
        S = db.sprintMap[S.sprintID]

@test
def testAssignSprintsToProject(sprints,project):
    for S in sprints:
        S.projectID = project.projectID
        try:
            db.updateScrumblesObject(S)
        except Exception as e:
            raise e
    db.updateAllObjects()
    for S in sprints:
        assert db.sprintMap[S.sprintID].projectID == project.projectID


@test
def testDeleteProject(project):
    db.deleteScrumblesObject(project)
    db.updateAllObjects()
    for S in db.sprints:
        assert S.projectID != project.projectID

    assert project.projectID not in db.projectMap
    assert project not in db.projects



@test
def testDeleteSprints(sprints):
    for S in sprints:
        db.deleteScrumblesObject(S)

    db.updateAllObjects()

    for S in sprints:
        assert S not in db.sprints
        assert S.sprintID not in db.sprintMap

functionList.append(lambda p=TProject: testCreateProject(p))
functionList.append(lambda s=Sprints: testCreateSprints(s))
functionList.append(lambda s=Sprints, p=TProject: testAssignSprintsToProject(s,p))
functionList.append(lambda p=TProject: testDeleteProject(p))
functionList.append(lambda s=Sprints:testDeleteSprints(s))

for f in functionList:
    f()


finalStatus = 'PASS'
for r in report:
    print('{} : {}'.format(r,report[r]))
    if 'fail' in report[r]:
        finalStatus = 'FAIL'

print('MODULE UNIT TESTING STATUS: {}'.format(finalStatus))