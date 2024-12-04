import { Loader } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Leva } from "leva";
import { Experience } from "./components/Experience";
import { useChat } from "./hooks/useChat";
import { useEffect, useState } from "react";
// import { UI } from "./components/UI";

function App() {

  const { getResponse, loading, message, getChatStatus, allowNextChat, nextChat } = useChat();
  const [init, setInit] = useState();

  useEffect(() => {
    getResponse("init");
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
      <Leva hidden/>
      {/* <UI/> */}
      <Canvas shadows camera={{ position: [0, 0, 1], fov: 6}}>
        <Experience />
      </Canvas>
    </>
  );
}

export default App;
