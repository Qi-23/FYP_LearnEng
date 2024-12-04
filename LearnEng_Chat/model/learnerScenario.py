from dao.dbConnection import DBConnection
from model.scenario import Scenario
from model.learner import Learner

class LearnerScenario:
    _tableName = "LearnerScenario"
    _idCol = "LearnerScenarioID"
    _id = None
    _chatHistory = None
    _historyDateTime = None
    _scenario = None
    _learner = None

    def __init__ (self, chatHistory, historyDateTime, scenario, learner, id=None):
        self._id = id
        self._chatHistory = chatHistory
        self._historyDateTime = historyDateTime
        self._scenario = scenario if isinstance(scenario, Scenario) else self.getScenario(scenario)
        self._learner = learner if isinstance(learner, Learner) else self.getLearner(scenario)

    def getScenario(self, scenario=None):
        if scenario is None:
            return self._scenario
        
        scenarioObj = None
        if not isinstance(scenario, Scenario):
            scenarioObj = Scenario.fetch_by_id(scenario)
        else:
            scenarioObj = scenario
        return scenarioObj

    def getLearner(self, learner=None):
        if learner is None:
            return self._learner
        
        learnerObj = None
        if not isinstance(learner, Learner):
            learnerObj = Learner.fetch_by_id(learner)
        else:
            learnerObj = learner
        return learnerObj
    
    def create_learnerScenarioObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            id = result['LearnerScenarioID']
            chatHistory = result['ChatHistory']
            historyDateTime = result['HistoryDateTime']
            scenario = result['ScenarioID']
            learner = result['LearnerID']

            learnerScenarioObj = LearnerScenario(chatHistory, historyDateTime, scenario, learner, id)
            return learnerScenarioObj
        
        elif (isinstance(result, list)):
            learnerScenarioObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['LearnerScenarioID']
                    chatHistory = each['ChatHistory']
                    historyDateTime = each['HistoryDateTime']
                    scenario = each['ScenarioID']
                    learner = each['LearnerID']

                    learnerScenarioObj = LearnerScenario(chatHistory, historyDateTime, scenario, learner, id)
                    learnerScenarioObjList.append(learnerScenarioObj)
            return learnerScenarioObjList
        
        return False
    
    @classmethod
    def fetch_all(self):
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        learnerScenarioObjList = self.create_learnerScenarioObj(self, result)
        return learnerScenarioObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        learnerScenarioObj = self.create_learnerScenarioObj(self, result)
        return learnerScenarioObj
    
    def __str__(self):
        return f"Learner Scenario Id: {self._id} \nHistory Date Time: {self._historyDateTime} \nScenario ID: {self._scenario._id} \nLearner ID: {self._learner._id}"