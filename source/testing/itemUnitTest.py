from data import ScrumblesData
from frames import ScrumblesObjects


def testItems(dataConnection):
    testItem = ScrumblesObjects.Item()
    testItem.itemType = 'UNIT_TEST_2'
    testItem.itemTitle = 'UNIT_TEST_2'
    testItem.itemDescription = 'UNIT TESTING ITEM CREATION, previous test failed to delete'
    testItemCreationQuery = ScrumblesData.Query.createObject(testItem)
    assert testItemCreationQuery is not None
    dataConnection.connect()

    dataConnection.setData(testItemCreationQuery)

    testItemSearchQuery = ScrumblesData.CardQuery.getCardByCardID(testItem.itemID)
    testItemSearchResult = dataConnection.getData(testItemSearchQuery)
    retrievedItem = ScrumblesObjects.Item(testItemSearchResult[0])

    dataConnection.close()

    assert retrievedItem.itemDescription == testItem.itemDescription

    dataConnection.connect()
    dataConnection.setData(ScrumblesData.Query.deleteObject(retrievedItem))
    itemAfterDeletionQueryResult = dataConnection.getData(ScrumblesData.CardQuery.getCardByCardID(retrievedItem.itemID))
    dataConnection.close()
    assert itemAfterDeletionQueryResult == ()
    print('Item',testItem.itemID,' Data successfully created and deleted on remote server')