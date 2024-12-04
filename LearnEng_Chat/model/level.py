from dao.dbConnection import DBConnection

class Level:
    _tableName = "Level"
    _idCol = "LevelID"
    _nameCol = "LevelName"
    _id = None
    _name = None
    _editors = None
    
    def __init__ (self, name, editors=None, id=None):
        self._id = id
        self._name = name
        self._editors = editors  #set

    def setName(self, name):
        self._name = name

    def setEditors(self, editors):
        self._editors = editors

    def getId(self):
        return self._id
    
    def create_levelObj(self, result=None):
        if result is None or result is []:
            return None
        elif (isinstance(result, dict)):
            id = result['LevelID']
            name = result['LevelName']
            levelObj = Level(id=id, name=name)
            return levelObj
        elif (isinstance(result, list)):
            levelObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['LevelID']
                    name = each['LevelName']
                    levelObj = Level(id=id, name=name)
                    levelObjList.append(levelObj)
            return levelObjList
        
        return False

    @classmethod
    def fetch_all(self):
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        levelObjList = self.create_levelObj(self, result)
        return levelObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        levelObj = self.create_levelObj(self, result)
        return levelObj
    
    @classmethod
    def fetch_by_name(self, search_name):
        queryName = f"SELECT * FROM {self._tableName} WHERE {self._nameCol} LIKE '%{search_name}%'"
        result = DBConnection.fetch_all(queryName)

        levelObjList = self.create_levelObj(self, result)
        return levelObjList
    
    # @classmethod
    # def retrieve_level_by_editor(self):
    #     result = DBConnection.fetch_all(f"SELECT * FROM Level WHERE ID = '{self.editor}'")
    #     return result
    
    def __str__(self):
        return f'LevelID: {self._id} \nLevel Name: {self._name} \nLevel Editor: {self._editors}'