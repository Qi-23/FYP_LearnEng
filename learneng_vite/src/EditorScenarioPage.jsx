import React, { useEffect, useState } from "react";
import ConfigureCharacterLoader from "./ConfigureCharacterLoader"

function EditorScenarioPage() {
  const [scenario, setScenario] = useState(null);
  const [currentLevel, setCurrentLevel] = useState(null);
  const [currentLevelString, setCurrentLevelString] = useState(null);
  const [selectedCharacter, setSelectedCharacter] = useState(null);

  const queryParams = new URLSearchParams(window.location.search);
  const id = queryParams.get("id");
  const levelValue = queryParams.get("levelValue");
  const levelString = queryParams.get("level");

  const getScenario = async (id) => {
    if (id) {
      const loadScenario = await fetch("/api/ScenarioConfig", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: id })
      });
      const scenarioData = await loadScenario.json();

      if (scenario !== scenarioData.scenario) {
        setScenario(scenarioData.scenario);
        setSelectedCharacter(scenarioData.scenario.characterFileName)
        $("#btn-submit_form").removeAttr("disabled").removeClass("btn-outline-secondary").addClass("btn-primary");
      }
      if (currentLevel != scenarioData.level) {
        setCurrentLevel(scenarioData.level)
      }
            
      const insertImage = async () => {
        const url = `http://127.0.0.1:5000/scenario/images/${id}`;
        try {
          const response = await fetch(url);
          if (response.ok) {
            const data = await response.json();
            const image = new Image();
            if (data.scenarioImage) {
              image.src = `data:${data.scenarioImageType};base64,${data.scenarioImage}`;
              selectedImage.attr("src", image.src);
            } else {
              selectedImage.attr("src", "background/null.png");
            }
      
            if (data.backgroundImage) {
              image.src = `data:${data.backgroundImageType};base64,${data.backgroundImage}`;
              backgroundImage.attr("src", image.src);
              console.log(image.src)
            } else {
              backgroundImage.attr("src", "background/null.png");
            }
          } else {
            console.log("Image fetch failed");
            selectedImage.attr("src", "background/null.png");
            backgroundImage.attr("src", "background/null.png");
          }
        } catch (error) {
          console.error("Error fetching image:", error);
          selectedImage.attr("src", "background/null.png");
          backgroundImage.attr("src", "background/null.png");
        }
      };
      
      insertImage();
    }
  }

  useEffect(() => {
    if (id) {
      getScenario(id);
      $(".end-field").each(function () {
        $(this).removeClass("justify-content-center").addClass("justify-content-between");
      })
      $(".delete-btn").each(function () {
        $(this).removeClass("d-none");
        $(this).on("click", function (e) {
          e.preventDefault();
          if (confirm("Are you sure you want to delete this scenario?")) {
            $.ajax({
              url: `http://127.0.0.1:5000/scenario/delete_scenario`,
              type: "POST",
              data: JSON.stringify({ id: id }),
              contentType: "application/json",
              success: function (response) {
                console.log(response);
                window.location.href = "/editor_scenario_page.html";
              },
              error: function (error) {
                console.log(error);
              }
            });
          }
        });
      })

    } else if (levelValue) {
      setCurrentLevel(levelValue)
      setCurrentLevelString(levelString)
      setSelectedCharacter('MaleCharacter1')
      $("#btn-submit_form").removeAttr("disabled").removeClass("btn-outline-secondary").addClass("btn-primary");
    }
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

      scenarioID.val(scenario.id)
      levelInput.val(scenario.level)
      displayLevel.text(scenario.levelString)

      scenarioName.val(scenario.name)
      scenarioDescription.val(scenario.scenarioDesc)
      characterDescription.val(scenario.characterDesc)
      vocab.val(scenario.vocab)
      grammar.val(scenario.grammar)
      situationalChat.val(scenario.situationalChat)

      hiddenCharacter.val(scenario.characterFileName)


    } else {
      // scenarioImage.attr("src", "page_photo/placeholder.png")
      // scenarioName.val("scenario_xx")
      // scenarioDescription.val("Create a hotel scenario which allow user to book a room")
      // characterDescription.val("The ai character will act as a front desk officer in the hotel")

      // scenarioImage.attr("src", "page_photo/placeholder.png")

      levelInput.val(currentLevel)
      displayLevel.text(currentLevelString)

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
      <ConfigureCharacterLoader selectedCharacter={selectedCharacter} />
    </div>
  );
};

export default EditorScenarioPage;
