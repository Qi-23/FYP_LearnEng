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

CREATE TABLE Voice (
  VoiceID 	INT AUTO_INCREMENT,
  VoiceName 	VARCHAR(255) UNIQUE NOT NULL,
  VoiceGender 	CHAR NOT NULL,
  VoiceFile 	VARCHAR(255) NOT NULL,
  EditorID 	INT,
  PRIMARY KEY (VoiceId),
  FOREIGN KEY (EditorID) REFERENCES Editor(EditorID)
);

CREATE TABLE Level (
  LevelID 	INT AUTO_INCREMENT,
  LevelName 	VARCHAR(255) UNIQUE NOT NULL,
  PRIMARY KEY (LevelID)
);

CREATE TABLE LevelEditor (
  LevelID 	INT,
  EditorID 	INT,
  PRIMARY KEY (LevelID, EditorID),
  FOREIGN KEY (LevelID) REFERENCES Level(LevelID),
  FOREIGN KEY (EditorID) REFERENCES Editor(EditorID)
);

CREATE TABLE Scenario (
  ScenarioID  	INT AUTO_INCREMENT,
  ScenarioName  VARCHAR(255) NOT NULL,
  ScenarioImage TEXT NOT NULL,
  ScenarioDescription 	TEXT NOT NULL,
  CharacterDescription 	TEXT NOT NULL,
  Vocab         TEXT NOT NULL,
  LevelID 	INT,
  PRIMARY KEY (ScenarioID),
  FOREIGN KEY (LevelID) REFERENCES Level(LevelID)
);

CREATE TABLE VirtualCharacter (
  CharacterID 	INT AUTO_INCREMENT,
  CharacterName 	VARCHAR(255) NOT NULL,
  CharacterRole 	VARCHAR(255) NOT NULL,
  CharacterLook 	TEXT,
  Characteristics 	TEXT,
  ReferenceImage 	VARCHAR(255),
  VoiceID 	INT,
  ScenarioID 	INT NOT NULL,
  PRIMARY KEY (CharacterID),
  FOREIGN KEY (VoiceID) REFERENCES Voice(VoiceID),
  FOREIGN KEY (ScenarioID) REFERENCES Scenario(ScenarioID)
);

CREATE TABLE Learner (
  LearnerID 	INT AUTO_INCREMENT,
  ProfilePicture 	VARCHAR(255) NOT NULL,
  Username 	VARCHAR(255) UNIQUE NOT NULL,
  Password 	VARCHAR(255) NOT NULL,
  LevelID 	INT,
  PRIMARY KEY (LearnerID),
  FOREIGN KEY (LevelID) REFERENCES Level(LevelID)
);

CREATE TABLE LearnerScenario (
  LearnerScenarioID 	INT AUTO_INCREMENT,
  ChatHistory 	LONGTEXT NOT NULL,
  HistoryDateTime DATETIME NOT NULL,
  ScenarioID 	INT,
  LearnerID 	INT,
  PRIMARY KEY (LearnerScenarioID),
  FOREIGN KEY (ScenarioID) REFERENCES Scenario(ScenarioID),
  FOREIGN KEY (LearnerID) REFERENCES Learner(LearnerID)
);

CREATE TABLE Summary (
  SummaryID 	INT AUTO_INCREMENT,
  SummarizedContent MEDIUMTEXT NOT NULL,
  QnaHistory 	MEDIUMTEXT,
  LearnerScenarioID 	INT,
  Primary Key (SummaryID)
);