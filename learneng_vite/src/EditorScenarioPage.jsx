import React, { useEffect, useState } from "react";
import ConfigureCharacterLoader from "./ConfigureCharacterLoader"

function EditorScenarioPage() {
  const [scenario, setScenario] = useState(null);
  const [currentLevel, setCurrentLevel] = useState(null);
  const [selectedCharacter, setSelectedCharacter] = useState(null);

  const getScenario = async () => {
    const loadScenario = await fetch("/api/ScenarioConfig", { method: 'GET' });
    const scenarioData = await loadScenario.json();
    
    if (scenario !== scenarioData.scenario) {
      setScenario(scenarioData.scenario);
      setSelectedCharacter(scenarioData.scenario.characterFileName)
    } 
    if (currentLevel != scenarioData.level) {
      setCurrentLevel(scenarioData.level)
    }
  }

  useEffect(() => {
    getScenario();
  }, []);

  let displayLevel = $("#displayLevel")
  
  let scenarioID = $("#scenarioID")
  let levelInput = $("#level")
  let selectedImage = $("#selectedImage")
  let scenarioName = $("#scenarioName")
  let scenarioDescription = $("#scenarioDescription")
  let characterDescription = $("#characterDescription")
  let vocab = $("#vocab")
  let grammar = $("#grammar")
  let situationalChat = $("#situationalChat")
  let backgroundImage = $("#selectedBackgroundImage")
  let hiddenCharacter = $("#hiddenCharacter")

  useEffect(() => {
    if (scenario) {
      console.log(scenario)
      selectedImage.attr("src", "page_photo/" + scenario.image)
      
      scenarioID.val(scenario.id)
      levelInput.val(scenario.level)
      displayLevel.text("Level " + scenario.level)

      scenarioName.val(scenario.name)
      scenarioDescription.val(scenario.scenarioDesc)
      characterDescription.val(scenario.characterDesc)
      vocab.val(scenario.vocab)
      grammar.val(scenario.grammar)
      situationalChat.val(scenario.situationalChat)

      hiddenCharacter.val(scenario.characterFileName)

      if (scenario.backgroundImage == null || scenario.backgroundImage == "null") {
        backgroundImage.attr("src", "background/null.png")
      } else {
        backgroundImage.attr("src", "background/" + scenario.backgroundImage)
      }
      
    } else {
      // scenarioImage.attr("src", "page_photo/placeholder.png")
      // scenarioName.val("scenario_xx")
      // scenarioDescription.val("Create a hotel scenario which allow user to book a room")
      // characterDescription.val("The ai character will act as a front desk officer in the hotel")
      
      // scenarioImage.attr("src", "page_photo/placeholder.png")

      levelInput.val(currentLevel)
      displayLevel.text("Level " + currentLevel)

      scenarioName.val()
      scenarioDescription.val()
      characterDescription.val()
      vocab.val()
      grammar.val()
      situationalChat.val()
      hiddenCharacter.val()
    }
  }, [currentLevel, scenario]);

  return (
    <div style={{ height: '100%' }}>
      <ConfigureCharacterLoader selectedCharacter={selectedCharacter}/>
    </div>
  );
};

export default EditorScenarioPage;
