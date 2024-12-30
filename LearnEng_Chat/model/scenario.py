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
    _characterFileName = None
    _backgroundImage = None
    _level = None

    def __init__(self, name, scenarioDesc, characterDesc, vocab, characterFileName, grammar, situationalChat, level, id=None, image=None, backgroundImage=None):
        self._id = id
        self._name = name
        self._image = image              # image path
        self._scenarioDesc = scenarioDesc
        self._characterDesc = characterDesc
        self._vocab = vocab
        self._grammar = grammar
        self._situationalChat = situationalChat
        self._characterFileName = characterFileName
        self._backgroundImage = backgroundImage
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
    
    def to_dict(self):
        return {
            "id": self._id,
            "name": self._name,
            "scenarioDesc": self._scenarioDesc,
            "characterDesc": self._characterDesc,
            "vocab": self._vocab,
            "grammar": self._grammar,
            "situationalChat": self._situationalChat,
            "characterFileName": self._characterFileName,
            "level": self._level._id,
            "levelString": self._level._name
        }
    
    def create_object(self, each):
        id = each['ScenarioID']
        name = each['ScenarioName']
        image = each['ScenarioImage']
        scenarioDesc = each['ScenarioDescription']
        characterDesc = each['CharacterDescription']
        vocab = each['Vocab']
        grammar = each['Grammar']
        situationalChat = each['SituationalChat']
        characterFileName = each['CharacterFileName']
        backgroundImage = each['BackgroundImage']
        level = each['LevelID']

        scenarioObj = Scenario(name, scenarioDesc, characterDesc, vocab, characterFileName, grammar, situationalChat, level, id, image, backgroundImage)
        return scenarioObj
    
    def create_scenarioObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            scenarioObj = self.create_object(self, result)
            return scenarioObj
        
        elif (isinstance(result, list)):
            scenarioObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    scenarioObj = self.create_object(self, each)
                    scenarioObjList.append(scenarioObj)
            return scenarioObjList
        
        return False
    
    def create_scenario(self):
        insertQ = """
        INSERT INTO Scenario (ScenarioName, ScenarioImage, ScenarioDescription, CharacterDescription, Vocab, Grammar, SituationalChat, CharacterFileName, BackgroundImage, LevelID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        print(insertQ, (self._name, 'image', self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, 'backgroundImage', self._level._id))
        DBConnection.execute_query(insertQ, (self._name, self._image, self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, self._backgroundImage, self._level._id))

    def update_scenario(self):
        if (not self._image and not self._backgroundImage):
            self.update_scenario_without_images()
        elif (not self._image):
            self.update_scenario_without_scenarioImage()
        elif (not self._backgroundImage):
            self.update_scenario_without_backgroundImage()
        else:
            self.update_scenario_with_images()

    def update_scenario_with_images(self):
        updateQ = """
        UPDATE Scenario
        SET ScenarioName = %s, ScenarioImage = %s, ScenarioDescription = %s, CharacterDescription = %s, Vocab = %s, Grammar = %s, SituationalChat = %s, CharacterFileName = %s, BackgroundImage = %s
        WHERE ScenarioID = %s
        """
        print(updateQ, (self._name, 'image', self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, "backgroundImage", self._id))
        DBConnection.execute_query(updateQ, (self._name, self._image, self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, self._backgroundImage, self._id))
        
    def update_scenario_without_images(self):
        updateQ = """
        UPDATE Scenario
        SET ScenarioName = %s, ScenarioDescription = %s, CharacterDescription = %s, Vocab = %s, Grammar = %s, SituationalChat = %s, CharacterFileName = %s
        WHERE ScenarioID = %s
        """
        print(updateQ, (self._name, self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, self._id))
        DBConnection.execute_query(updateQ, (self._name, self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, self._id))
        
    def update_scenario_without_scenarioImage(self):
        updateQ = """
        UPDATE Scenario
        SET ScenarioName = %s, ScenarioDescription = %s, CharacterDescription = %s, Vocab = %s, Grammar = %s, SituationalChat = %s, CharacterFileName = %s, BackgroundImage = %s
        WHERE ScenarioID = %s
        """
        print(updateQ, (self._name, self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, "backgroundImage", self._id))
        DBConnection.execute_query(updateQ, (self._name, self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, self._backgroundImage, self._id))
        
    def update_scenario_without_backgroundImage(self):
        updateQ = """
        UPDATE Scenario
        SET ScenarioName = %s, ScenarioImage = %s, ScenarioDescription = %s, CharacterDescription = %s, Vocab = %s, Grammar = %s, SituationalChat = %s, CharacterFileName = %s
        WHERE ScenarioID = %s
        """
        print(updateQ, (self._name, 'image', self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, self._id))
        DBConnection.execute_query(updateQ, (self._name, self._image, self._scenarioDesc, self._characterDesc, self._vocab, self._grammar, self._situationalChat, self._characterFileName, self._id))
        
    @classmethod
    def delete_by_id(self, search_id):
        deleteQ = f"DELETE FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.execute_query(deleteQ)

        scenarioObj = self.create_scenarioObj(self, result)
        return scenarioObj
    
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
        return f'ScenarioID: {self._id} \nScenario Name: {self._name} \nScenario Image: {self._image} \nScenario Description: {self._scenarioDesc} \nCharacter Description: {self._characterDesc} \nVocab: {self._vocab} \nLevel: {self._level._id} \nbackgroundImage: {self._backgroundImage}'
    
