import {
  CameraControls,
  Environment,
} from "@react-three/drei";
import { useEffect, useRef, useState } from "react";
import { Character } from "./DisplayCharacter";

export const characters = ["MaleCharacter1", "MaleCharacter2"];

export const ConfigureCharacterControl = ({selectedCharacter}) => {
  const cameraControls = useRef();

  useEffect(() => {
    const controls = cameraControls.current;
    controls.setLookAt(0, 1.5, 5, 0, 1.7, 0);

    controls.minDistance = 5;
    controls.maxDistance = 5;

    controls.minPolarAngle = Math.PI / 2;
    controls.maxPolarAngle = Math.PI / 2;
    controls.minAzimuthAngle = -Math.PI / 4;
    controls.maxAzimuthAngle = Math.PI / 4;

    controls.minAzimuthAngle = 0;
    controls.maxAzimuthAngle = 0;
  }, []);


  const [character, setCharacter] = useState(null);

  useEffect(() => {
    console.log("Selected Character:", character);
    let characterFileName = $("#character-select")
    if (character != characterFileName.val()) {
      characterFileName.val(character).change();
    }
  }, [character]);

  useEffect(() => {
    setCharacter(selectedCharacter)
  }, [selectedCharacter]);

  const selectElement = document.getElementById("character-select");
  useEffect(() => {
    characters.forEach((character) => {
      const option = document.createElement("option");
      option.value = character;
      option.textContent = character;
      selectElement.appendChild(option);
    })
  }, [characters]);

  useEffect(() => {
    $('#character-select').change(function () {
      setCharacter($(this).val())
    });
  })

  return (
    <>
      <CameraControls ref={cameraControls} />
      <Environment preset="sunset" />
      <Character key={character} character={character} />
    </>
  );
};

