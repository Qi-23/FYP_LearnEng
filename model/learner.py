from dao.dbConnection import DBConnection
from model.level import Level

class Learner:
    _tableName = "Learner"
    _idCol = "LearnerID"
    _usernameCol = "Username"
    _id = None
    _profilePicture = None
    _username = None
    _password = None
    _level = None

    def __init__ (self, profilePicture, username, password, level, id=None):
        self._id = id
        self._profilePicture = profilePicture
        self._username = username
        self._password = password
        self._level = level if isinstance(level, Level) else self.getLevel(level)

    def getLevel(self, level=None):
        if level is None:
            return self._level
        
        levelObj = None
        if not isinstance(level, Level):
            levelObj = Level.fetch_by_id(level)
        else:
            levelObj = level
        return levelObj
    
    def create_learnerObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            id = result['LearnerID']
            profilePicture = result['ProfilePicture']
            username = result['Username']
            password = result['Password']
            level = result['LevelID']

            learnerObj = Learner(profilePicture, username, password, level, id)
            return learnerObj
        
        elif (isinstance(result, list)):
            learnerObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['LearnerID']
                    profilePicture = each['ProfilePicture']
                    username = each['Username']
                    password = each['Password']
                    level = each['LevelID']

                    learnerObj = Learner(profilePicture, username, password, level, id)
                    learnerObjList.append(learnerObj)
            return learnerObjList
        
        return False

    @classmethod
    def fetch_all(self):
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        learnerObjList = self.create_learnerObj(self, result)
        return learnerObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        learnerObj = self.create_learnerObj(self, result)
        return learnerObj
    
    @classmethod
    def fetch_by_username(self, search_username):
        queryUsername = f"SELECT * FROM Level WHERE {self._usernameCol} = '{search_username}'"
        result = DBConnection.fetch_all(queryUsername)

        learnerObjList = self.create_learnerObj(self, result)
        return learnerObjList
    
    def __str__(self):
        return f'Learner ID: {self._id} \nUsername Name: {self._username} \nLearner Password: {self._password} \nLearner Level ID: {self._level._id}'
    