from data import DataBlock, ScrumblesObjects
from datetime import datetime
import time
import logging

PASS = '\033[92m'
FAIL = '\033[91m'
SLEEP = 8

logging.basicConfig(format='%(levelname)s:  %(asctime)s:  %(message)s', filename='ScrumblesTest.log',level=logging.DEBUG)
logging.info('Application starting')


testRun = {}

db = DataBlock.DataBlock()

Tsprint = ScrumblesObjects.Sprint()
Tsprint.sprintName = 'Test Sprint for deletion'
Tsprint.sprintStartDate = datetime.now()
Tsprint.sprintDueDate = datetime.now()
Tsprint.projectID = 0


TItem = ScrumblesObjects.Item()
TItem.itemTitle = "Test Item to add to Test Sprint"
TItem.itemDescription = 'Test TEST TEST'
TItem.itemPriority = 0
TItem.itemStatus = 0
TItem.itemPoints = 9
TItem.itemType = 'User Story'


print('adding sprint')
try:
    db.addNewScrumblesObject(Tsprint)
    time.sleep(SLEEP)
    testRun['Add Sprint'] = (True,'Pass')
except Exception as e:
    test = 'Failed to add Sprint to DB\n'+str(e)
    testRun['Add Sprint'] = (False, test)



try:
    TSprint = db.sprintMap[Tsprint.sprintID]
    testRun['Add to sprint Map'] = (True, 'Pass')
except KeyError:
    test = 'Failed to add Sprint %i to MAP'%Tsprint.sprintID
    testRun['Add to sprint Map'] = (False, test)


print('adding item')
try:
    db.addNewScrumblesObject(TItem)
    time.sleep(SLEEP)
    testRun['Add Item'] = (True, 'pass')
except Exception as e:
    test = 'Failed to add Item to database\n' + str(e)
    testRun['Add Item'] = (False,test)



try:
    TItem =  db.itemMap[TItem.itemID]
    testRun['Item in Map'] = (True, 'pass')
except KeyError:
    test = 'Failed to add Item %i to itemMap'% TItem.itemID
    testRun['Item in Map'] = (False,test)


if testRun['Add Item'][0]:
    print('assigning item to sprint')
    try:
        db.assignItemToSprint(TItem,Tsprint)
        time.sleep(SLEEP)
        testRun['Assign To Sprint'] = (True,'Pass')
    except Exception as e:
        test = 'Failed to assign item to Sprint\n'+ str(e)
        testRun['Assign to Sprint'] = (False, test)
    

    try:
        assert TItem.itemSprintID == Tsprint.sprintID, 'Item.sprintID did not get to Sprint.sprintID'
    except AssertionError as e:
        test = str(e)
        testRun['Assign To Sprint'] = (False, test)
else:
    testRun['Assign To Sprint'] = (False,'skipped')

print('deleting sprint')
try:
    db.deleteScrumblesObject(Tsprint)
    time.sleep(SLEEP)
    testRun['Delete Sprint'] = (True,'Pass')
except Exception as e:
    test = 'Failed to delete Sprint from database\n'+str(e)
    testRun['Delete Sprint'] = (False,test)


try:
    TSprint = db.sprintMap[Tsprint.sprintID]
    testRun['Remove from  Sprint MAP'] = (False, 'Sprint still in db SprintMap')
except KeyError:
    testRun['Remove from  Sprint MAP'] = (True,'Pass')

try:
    TItem = db.itemMap[TItem.itemID]
    assert TItem.itemSprintID is None, 'SprintID did not remove from item'
    testRun['Remove Sprint From Item'] = (True,'pass')
except AssertionError as e:
    test = str(e)
    testRun['Remove Sprint From Item'] = (False,test)
except KeyError:
    testRun['Remove Sprint From Item'] = (False, 'ItemID not in Map')

print('Deleting Item')
try:
    db.deleteScrumblesObject(TItem)
    time.sleep(SLEEP)
    testRun['Delete Item'] = (True,'pass')
except Exception as e:
    test = 'Failed to delete Item from database\n'+str(e)
    testRun['Delete Item'] = (False,test)


try:
    TItem = db.itemMap[TItem.itemID]
    testRun['Remove Item From MAP'] = (False, 'Item still in db itemMap')
except KeyError:
    test = 'pass'
    testRun['Remove Item From MAP'] = (True, test)


sumPass = 0
sumFail = 0
totalTest = 0

print('\n\n********REPORT*****************\n\n')

for key in testRun:
    totalTest += 1
    if testRun[key][0]:
        sumPass += 1
        print(PASS)
        print('%s :'%key,testRun[key][0])
    else:
        print(FAIL)
        print('%s :\033[91m' % key, testRun[key][0] )
        sumFail += 1
print(PASS)
print('%i out of %i tests pass'%(sumPass,totalTest))
if sumFail > 0:
    print(FAIL)
print('%i our of %i tests failed'%(sumFail,totalTest))

print('\n\n\n')
print('The Following Test Failed')
for key in testRun:
    if testRun[key][0]:
        pass
    else:
        print(PASS)
        print('%s failed because:--------\/'%key)
        print(FAIL)
        print( '%s'%key,testRun[key][1])

try:
    db.shutdown()
except:
    pass