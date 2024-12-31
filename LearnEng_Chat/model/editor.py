from dao.dbConnection import DBConnection
import logging

class Editor: 
    _tableName = "Editor"
    _idCol = "EditorID"
    _usernameCol = "Username"
    _id = None
    _username = None
    _password = None
    _email = None

    def __init__ (self, username, password, email, id=None) :
        self._id = id
        self._username = username
        self._password = password
        self._email = email

    def create_editorObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            id = result['EditorID']
            username = result['Username']
            password = result['Password']
            email = result['Email']

            editorObj = Editor(username, password, email, id)
            return editorObj
        
        elif (isinstance(result, list)):
            editorObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['EditorID']
                    username = each['Username']
                    password = each['Password']
                    email = each['Email']

                    editorObj = Editor(username, password, email, id)
                    editorObjList.append(editorObj)
            return editorObjList
        
        return False

    @classmethod
    def fetch_all(self):
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        editorObjList = self.create_editorObj(self, result)
        return editorObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        editorObj = self.create_editorObj(self, result)
        return editorObj
    
    @classmethod
    def fetch_by_username(self, search_username):
        queryUsername = f"SELECT * FROM {self._tableName} WHERE {self._usernameCol} = '{search_username}'"
        logging.info(queryUsername)
        result = DBConnection.fetch_one(queryUsername)

        editorObj = self.create_editorObj(self, result)
        return editorObj
    
    @classmethod
    def check_authentication(cls, username, password):
        editor = cls.fetch_by_username(username)
        if not editor:
            return False
        if editor._password == password:
            return True
        else :
            return False
    
    def __str__(self):
        return f"Id: {self._id} \nUsername: {self._username} \nPassword: {self._password} \nEmail: {self._email}"