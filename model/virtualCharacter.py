from dao.dbConnection import DBConnection
from model.voice import Voice
from model.scenario import Scenario

class VirtualCharacter:
    _tableName = "VirtualCharacter"
    _idCol = "CharacterID"
    _nameCol = "CharacterName"
    _id = None
    _name = None
    _roleDesc = None
    _lookDesc = None
    _characteristicDesc = None
    _referenceImage = None
    _voice = None
    _scenario = None

    def __init__ (self, name, role=None, look=None, characteristics=None, referenceImage=None, voice=None, scenario=None, id=None):
        self._id = id
        self._name = name
        self._roleDesc = role
        self._lookDesc = look
        self._characteristicsDesc = characteristics
        self._referenceImage = referenceImage    #image path
        self._voice = voice if isinstance(voice, Voice) else self.getLevel(self, voice)                    #voice object
        self._scenario = scenario if isinstance(scenario, Scenario) else self.getScenario(self, scenario)

    def getVoice(self, voice=None):
        if voice is None:
            return self._voice
        
        voiceObj = None
        if not isinstance(voice, Voice):
            voiceObj = Voice.fetch_by_id(voice)
        else:
            voiceObj = voice
        return voiceObj
    
    def getScenario(self, scenario=None):
        if scenario is None:
            return self._scenario
        
        scenarioObj = None
        if not isinstance(scenario, Scenario):
            scenarioObj = Scenario.fetch_by_id(scenario)
        else:
            scenarioObj = scenario
        return scenarioObj
    
    def create_virtualCharacterObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            id = result['CharacterID']
            name = result['CharacterName']
            role = result['CharacterRole']
            look = result['CharacterLook']
            characteristics = result['Characteristics']
            image = result['ReferenceImage']
            voice = self.getVoice(self, result['VoiceID'])
            scenario = self.getScenario(self, result['ScenarioID'])

            virtualCharacterObj = VirtualCharacter(name, role, look, characteristics, image, voice, scenario, id)
            return virtualCharacterObj
        
        elif (isinstance(result, list)):
            virtualCharacterObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['CharacterID']
                    name = each['CharacterName']
                    role = each['CharacterRole']
                    look = each['CharacterLook']
                    characteristics = each['Characteristics']
                    image = each['ReferenceImage']
                    voice = self.getVoice(self, each['VoiceID'])
                    scenario = self.getScenario(self, each['ScenarioID'])

                    virtualCharacterObj = VirtualCharacter(name, role, look, characteristics, image, voice, scenario, id)
                    virtualCharacterObjList.append(virtualCharacterObj)
            return virtualCharacterObjList
        
        return False
    
    @classmethod
    def fetch_all(self):
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        virtualCharacterObjList = self.create_virtualCharacterObj(self, result)
        return virtualCharacterObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        virtualCharacterObj = self.create_virtualCharacterObj(self, result)
        return virtualCharacterObj
    
    @classmethod
    def fetch_by_name(self, search_name):
        queryName = f"SELECT * FROM Level WHERE {self._nameCol} LIKE '%{search_name}%'"
        result = DBConnection.fetch_all(queryName)

        virtualCharacterObjList = self.create_virtualCharacterObj(self, result)
        return virtualCharacterObjList
    
    def __str__(self):
        return (f"Character Id: {self._id} \nCharacter Name: {self._name} \nCharacter Role: {self._roleDesc}" +
        f"\nCharacter Look: {self._lookDesc} \nCharacteristics: {self._characteristicDesc} \nReference Image: {self._referenceImage}" + 
        f"\nVoice Id: {self._voice._id} \nScenario Id: {self._scenario._id}")