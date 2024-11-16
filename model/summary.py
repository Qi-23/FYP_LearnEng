from dao.dbConnection import DBConnection
from model.learnerScenario import LearnerScenario

class Summary:
    _tableName = "Summary"
    _idCol = "SummaryID"
    _SummarizedContent = None
    _qnaHistory = None
    _learnerScenario = None

    def __init__ (self, summarizedContent, learnerScenario, qnaHistory=None, id=None):
        self._id = id
        self._summarizedContent = summarizedContent
        self._qnaHistory = qnaHistory
        self._learnerScenario = learnerScenario if isinstance(learnerScenario, LearnerScenario) else self.getLearnerScenario(learnerScenario)
    
    def getLearnerScenario(self, learnerScenario=None):
        if learnerScenario is None:
            return self._learnerScenario
        
        learnerScenarioObj = None
        if not isinstance(learnerScenario, LearnerScenario):
            learnerScenarioObj = LearnerScenario.fetch_by_id(learnerScenario)
        else:
            learnerScenarioObj = learnerScenario
        return learnerScenarioObj

    def create_summaryObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            id = result['SummaryID']
            summarizedContent = result['SummarizedContent']
            qnaHistory = result['QnaHistory']
            learnerScenario = result['LearnerScenarioID']
            
            summaryObj = Summary(summarizedContent, learnerScenario, qnaHistory, id)
            return summaryObj
        
        elif (isinstance(result, list)):
            summaryObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['SummaryID']
                    summarizedContent = each['SummarizedContent']
                    qnaHistory = each['QnaHistory']
                    learnerScenario = each['LearnerScenarioID']
                    
                    summaryObj = Summary(summarizedContent, learnerScenario, qnaHistory, id)
                    summaryObjList.append(summaryObj)
            return summaryObjList
        
        return False
    
    @classmethod
    def fetch_all(self):
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        summaryObjList = self.create_summaryObj(self, result)
        return summaryObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        summaryObj = self.create_summaryObj(self, result)
        return summaryObj
    
    def __str__(self):
        return f"Summary Id: {self._id} \nSummarized Content: {self._summarizedContent} \nLearner Scenario ID: {self._learnerScenario._id}"