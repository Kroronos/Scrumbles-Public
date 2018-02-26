import ScrumblesData 
import ScrumblesObjects

def printItemDetails(item):
    print(item.itemID)
    print(item.itemType)
    print(item.itemTitle)
    print(item.itemDescription)
    print(item.itemCreationDate)
    print(item.itemDueDate)
    print(item.itemCodeLink)
    print(item.itemSprintID)
    print(item.itemUserID)
    print(item.itemStatus)


login_info = ScrumblesData.DataBaseLoginInfo()
login_info.userID = 'test_user'
login_info.password = 'testPassword'
login_info.ipaddress = '173.230.136.241'
login_info.defaultDB = 'test'

dataConnection = ScrumblesData.ScrumblesData(login_info)
dataConnection.connect()
itemTable = dataConnection.getData(ScrumblesData.Query.getAllCards)
dataConnection.close()

listOfAllItems = []
for row in itemTable:
    item = ScrumblesObjects.Item(row)
    listOfAllItems.append(item)

for item in listOfAllItems:
    printItemDetails(item)
