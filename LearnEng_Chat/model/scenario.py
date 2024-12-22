from dao.dbConnection import DBConnection
from model.level import Level

class Scenario: 
    _tableName = "Scenario"
    _idCol = "ScenarioID"
    _nameCol = "ScenarioName"
    _id = None
    _name = None
    _image = None
    _scenarioDesc = None
    _characterDesc = None
    _vocab = None
    _grammar = None
    _situationalChat = None
    _level = None

    def __init__(self, name, image, scenarioDesc, characterDesc, vocab, grammar, situationalChat, level, id=None):
        self._id = id
        self._name = name
        self._image = image              # image path
        self._scenarioDesc = scenarioDesc
        self._characterDesc = characterDesc
        self._vocab = vocab
        self._grammar = grammar
        self._situationalChat = situationalChat
        self._level = level if isinstance(level, Level) else self.getLevel(level)

    def setName(self, name):
        self._name = name
    
    def setImage(self, image):
        self._image = image

    def setScenarioDesc(self, scenarioDesc):
        self._scenarioDesc = scenarioDesc

    def setCharacterDesc(self, characterDesc):
        self._characterDesc = characterDesc

    def setVocab(self, vocab):
        self._vocab = vocab

    def setLevel(self, level):
        self._level = self.getLevel(level)

    def getLevel(self, level=None):
        if level is None:
            return self._level
        
        levelObj = None
        if not isinstance(level, Level):
            levelObj = Level.fetch_by_id(level)
        else:
            levelObj = level
        return levelObj
    
    def create_scenarioObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            id = result['ScenarioID']
            name = result['ScenarioName']
            image = result['ScenarioImage']
            scenarioDesc = result['ScenarioDescription']
            characterDesc = result['CharacterDescription']
            vocab = result['Vocab']
            grammar = result['Grammar']
            situationalChat = result['SituationalChat']
            level = result['LevelID']

            scenarioObj = Scenario(name, image, scenarioDesc, characterDesc, vocab, grammar, situationalChat, level, id)
            return scenarioObj
        
        elif (isinstance(result, list)):
            scenarioObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['ScenarioID']
                    name = each['ScenarioName']
                    image = each['ScenarioImage']
                    scenarioDesc = each['ScenarioDescription']
                    characterDesc = each['CharacterDescription']
                    vocab = each['Vocab']
                    grammar = result['Grammar']
                    situationalChat = result['SituationalChat']
                    level =  each['LevelID']

                    scenarioObj = Scenario(name, image, scenarioDesc, characterDesc, vocab, grammar, situationalChat, level, id)
                    scenarioObjList.append(scenarioObj)
            return scenarioObjList
        
        return False
    
    def create_scenario(self):
        insertQ = f"INSERT INTO {self._tableName} VALUES (NULL, '{self._name}', '{self._image}', '{self._scenarioDesc}', '{self._characterDesc}', '{self._vocab}', '{self._grammar}', '{self._situationalChat}', '{self._level.id}')"
        DBConnection.execute_query(insertQ)

    def update_scenario(self):
        updateQ = f"UPDATE {self._tableName} SET ScenarioName = '{self._name}', ScenarioImage = '{self._image}', ScenarioDescription = '{self._scenarioDesc}', CharacterDescription = '{self._characterDesc}', Vocab = '{self._vocab}', Grammar = '{self._grammar}', SituationalChat = '{self._situationalChat}' WHERE ScenarioID = {self._id};"
        print(updateQ)
        DBConnection.execute_query(updateQ)

    @classmethod
    def fetch_all(self): #return all scenario objects(info)
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        scenarioObjList = self.create_scenarioObj(self, result)
        return scenarioObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        scenarioObj = self.create_scenarioObj(self, result)
        return scenarioObj
    
    @classmethod
    def fetch_by_name(self, search_name):
        queryName = f"SELECT * FROM Level WHERE {self._nameCol} LIKE '%{search_name}%'"
        result = DBConnection.fetch_all(queryName)

        scenarioObjList = self.create_scenarioObj(self, result)
        return scenarioObjList
    
    def __str__(self):
        return f'ScenarioID: {self._id} \nScenario Name: {self._name} \nScenario Image: {self._image} \nScenario Description: {self._scenarioDesc} \nCharacter Description: {self._characterDesc} \nVocab: {self._vocab} \nLevel: {self._level._id}'
    