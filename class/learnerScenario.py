class LearnerScenario:
    def __init__ (id, chatHistory, historyDateTime, scenario, learner):
        self.id = id
        self.chatHistory = chatHistory
        self.historyDateTime = historyDateTime
        self.scenario = scenario     # scenario obj
        self.learner = learner       # learner obj