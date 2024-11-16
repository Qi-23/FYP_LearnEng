from dao.dbConnection import DBConnection
from model.editor import Editor

class Voice:
    _tableName = "Voice"
    _idCol = "VoiceID"
    _nameCol = "VoiceName"
    _id = None
    _name = None
    _gender = None
    _filePath = None
    _editor = None

    def __init__ (self, name, gender, filePath, editor=None, id=None):
        self._id = id
        self._name = name
        self._gender = gender        # f/m
        self._filePath = filePath
        self._editor = editor if isinstance(editor, Editor) else self.getEditor(editor)

    def getEditor(self, editor=None):
        if editor is None:
            return self._editor
        
        editorObj = None
        if not isinstance(editor, Editor):
            editorObj = Editor.fetch_by_id(editor)
        else:
            editorObj = editor
        return editorObj
    
    def create_voiceObj(self, result=None):
        if result is None or result is []:
            return None

        if (isinstance(result, dict)):
            id = result['VoiceID']
            name = result['VoiceName']
            gender = result['VoiceGender']
            file = result['VoiceFile']
            editor = result['EditorID']

            voiceObj = Voice(name, gender, file, editor, id)
            return voiceObj
        
        elif (isinstance(result, list)):
            voiceObjList = []
            for each in result:
                if (isinstance(each, dict)):
                    id = each['VoiceID']
                    name = each['VoiceName']
                    gender = each['VoiceGender']
                    file = each['VoiceFile']
                    editor = each['EditorID']

                    voiceObj = Voice(name, gender, file, editor, id)
                    voiceObjList.append(voiceObj)
            return voiceObjList
        
        return False
    
    @classmethod
    def fetch_all(self):
        queryAll = f"SELECT * FROM {self._tableName}"
        result = DBConnection.fetch_all(queryAll)
        voiceObjList = self.create_voiceObj(self, result)
        return voiceObjList
    
    @classmethod
    def fetch_by_id(self, search_id):
        queryId = f"SELECT * FROM {self._tableName} WHERE {self._idCol} = {search_id}"
        result = DBConnection.fetch_one(queryId)

        voiceObj = self.create_voiceObj(self, result)
        return voiceObj
    
    @classmethod
    def fetch_by_name(self, search_name):
        queryName = f"SELECT * FROM Level WHERE {self._nameCol} LIKE '%{search_name}%'"
        result = DBConnection.fetch_all(queryName)

        voiceObjList = self.create_voiceObj(self, result)
        return voiceObjList
    
    def __str__(self):
        return f"Voice Id: {self._id} \nVoice Name: {self._name} \nGender: {self._gender} \nFile: {self._filePath} \nEditor: {self._editor._id}"