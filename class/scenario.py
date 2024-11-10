class Scenario: 
    def __init__(id, name, picture, scenarioDescription, characterDescription):
        self.id = id
        self.name = name
        self.picture = picture
        self.scenarioDescription = scenarioDescription
        self.characterDescription = characterDescription

    def read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")

    def retrieve() : 
        print('hello')