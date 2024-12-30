DROP TABLE Summary;
DROP TABLE LearnerScenario;
DROP TABLE Learner;
DROP TABLE VirtualCharacter;
DROP TABLE Scenario;
DROP TABLE LevelEditor;
DROP TABLE Level;
DROP TABLE Voice;
DROP TABLE Editor;

CREATE TABLE Editor (
  EditorID 	INT AUTO_INCREMENT,
  Username 	VARCHAR(255) UNIQUE NOT NULL,
  Password	VARCHAR(255) NOT NULL,
  Email 	VARCHAR(255) UNIQUE,
  Status 	VARCHAR(255),
  StatusUpdatedDate 	DATE,
  PRIMARY KEY (EditorID)
);

CREATE TABLE Level (
  LevelID 	INT AUTO_INCREMENT,
  LevelName 	VARCHAR(255) UNIQUE NOT NULL,
  PRIMARY KEY (LevelID)
);

CREATE TABLE Scenario (
  ScenarioID  	INT AUTO_INCREMENT,
  ScenarioName  VARCHAR(255) NOT NULL,
  ScenarioImage MEDIUMBLOB,
  ScenarioDescription 	TEXT NOT NULL,
  CharacterDescription 	TEXT NOT NULL,
  Vocab         TEXT NOT NULL,
  Grammar         TEXT NOT NULL,
  SituationalChat         TEXT NOT NULL,
  CharacterName   VARCHAR(255) NOT NULL,
  CharacterFileName   VARCHAR(255) NOT NULL,
  BackgroundImage MEDIUMBLOB,
  LevelID 	INT,
  PRIMARY KEY (ScenarioID),
  FOREIGN KEY (LevelID) REFERENCES Level(LevelID)
);