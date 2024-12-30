import { Loader } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { CharacterControl } from "./components/CharacterControl";
import { useChat } from "./hooks/useChat";
import { useEffect, useState } from "react";

function CharacterLoader() {

  const { getResponse, getChatStatus, nextChat } = useChat();
  const [scenario, setScenario] = useState(null);
  const [character, setCharacter] = useState(null);
  const [init, setInit] = useState();
  const [backgroundImageSrc, setBackgroundImageSrc] = useState(null);

  const queryParams = new URLSearchParams(window.location.search);
  const id = queryParams.get("id");
  console.log(id);

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

      setScenario(scenarioData.scenario);
      setCharacter(scenarioData.scenario.characterFileName)
      fetchBackgroundImage(scenarioData.scenario.id)
    }
  }

  const fetchBackgroundImage = async (id) => {
    const url = `http://127.0.0.1:5000/scenario/images/${id}`
    try {
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        const image = new Image();
        
        if (data.backgroundImage) {
          image.src = `data:${data.backgroundImageType};base64,${data.backgroundImage}`;
          setBackgroundImageSrc(image.src);
        } 
      }
    } catch (error) {
      console.error('Error fetching background image:', error);
    }
  };

  useEffect(() => {
    getScenario(id);
    getResponse("init", id);
    setInit(true);
  }, []);

  useEffect(() => {
    if (nextChat) {
      getResponse("cont");
    }
  }, [nextChat])

  useEffect(() => {
    const intervalId = setInterval(() => {
      getChatStatus();
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <Loader />
      <Canvas shadows camera={{ position: [0, 0, 1], fov: 6, aspect: window.innerWidth / window.innerHeight }}>
        <CharacterControl character={character} backgroundImage={backgroundImageSrc}/>
      </Canvas>
    </>
  );
}

export default CharacterLoader;
