@staticmethod
def deleteObject(obj):
    query = ''
    if repr(obj) == "<class 'data.ScrumblesObjects.User'>":
        query = UserQuery.deleteUser(obj)
    elif repr(obj) == "<class 'data.ScrumblesObjects.Comment'>":
        query = CommentQuery.deleteComment(obj)
    elif repr(obj) == "<class 'data.ScrumblesObjects.Sprint'>":
        query = SprintQuery.deleteSprint(obj)
    elif type(obj) == ScrumblesObjects.Item:
        query = CardQuery.deleteCard(obj)
    elif repr(obj) == "<class 'data.ScrumblesObjects.Project'>":
        query = ProjectQuery.deleteProject(obj)
    else:
        raise Exception('Invalid Object Type')
    return query


@staticmethod
def updateObject(obj):
    query = ''
    if repr(obj) == "<class 'data.ScrumblesObjects.User'>":
        query = UserQuery.updateUser(obj)
    elif repr(obj) == "<class 'data.ScrumblesObjects.Comment'>":
        query = CommentQuery.updateComment(obj)
    elif repr(obj) == "<class 'data.ScrumblesObjects.Sprint'>":
        query = SprintQuery.updateSprint(obj)
    elif type(obj) == ScrumblesObjects.Item:
        query = CardQuery.updateCard(obj)
    elif repr(obj) == "<class 'data.ScrumblesObjects.Project'>":
        query = ProjectQuery.updateProject(obj)
    else:
        raise Exception('Invalid Object Type')
    return query
