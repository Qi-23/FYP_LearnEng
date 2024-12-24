import { Loader } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { CharacterControl } from "./components/CharacterControl";
import { useChat } from "./hooks/useChat";
import { useEffect, useState } from "react";

function CharacterLoader() {

  const { getResponse, getChatStatus, nextChat } = useChat();
  const [init, setInit] = useState();

  const queryParams = new URLSearchParams(window.location.search);
  const id = queryParams.get("id");

  useEffect(() => {
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
        <CharacterControl />
      </Canvas>
    </>
  );
}

export default CharacterLoader;
