import { Loader } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { ConfigureCharacterControl } from "./components/ConfigureCharacterControl";
import { useEffect, useState } from "react";

export const characters = ["MaleCharacter1", "MaleCharacter2"];

function ConfigureCharacterLoader({selectedCharacter}) {

  return (
    <>
      <Loader />
      <Canvas shadows camera={{ position: [0, 0, 1], fov: 6 }}>
        <ConfigureCharacterControl selectedCharacter={selectedCharacter}/>
      </Canvas>
    </>
  );
}

export default ConfigureCharacterLoader;
