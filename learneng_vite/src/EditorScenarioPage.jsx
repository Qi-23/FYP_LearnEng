import React, { useEffect, useState } from "react";

function EditorScenarioPage() {
  const [scenario, setScenario] = useState(null);

  const getScenario = async () => {
    const loadScenario = await fetch("/api/ScenarioConfig", { method: 'GET' });
    const scenarioData = await loadScenario.json();
    if (scenario !== scenarioData.scenario) {
      setScenario(scenarioData.scenario);
    }
  }

  useEffect(() => {
    getScenario();
  }, []);

  let displayLevel = $("#displayLevel")
  
  let scenarioID = $("#scenarioID")
  let level = $("#level")
  let selectedImage = $("#selectedImage")
  let scenarioName = $("#scenarioName")
  let scenarioDescription = $("#scenarioDescription")
  let characterDescription = $("#characterDescription")
  let vocab = $("#vocab")

  useEffect(() => {
    if (scenario) {
      console.log(scenario)
      selectedImage.attr("src", "page_photo/" + scenario.image)
      
      
      scenarioID.val(scenario.id)
      level.val(scenario.level)
      displayLevel.text("Level " + scenario.level)

      scenarioName.val(scenario.name)
      scenarioDescription.val(scenario.scenarioDes)
      characterDescription.val(scenario.characterDesc)
      vocab.val(scenario.vocab)
    } else {
      // scenarioImage.attr("src", "page_photo/placeholder.png")
      // scenarioName.val("scenario_xx")
      // scenarioDescription.val("Create a hotel scenario which allow user to book a room")
      // characterDescription.val("The ai character will act as a front desk officer in the hotel")
      
      // scenarioImage.attr("src", "page_photo/placeholder.png")
      scenarioName.val()
      scenarioDescription.val()
      characterDescription.val()
      vocab.val()
    }
  }, [scenario]);

  return (
    <div></div>
  );
};

export default EditorScenarioPage;
