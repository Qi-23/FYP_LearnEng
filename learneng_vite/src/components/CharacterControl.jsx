import {
  CameraControls,
  Environment,
  Text,
} from "@react-three/drei";
import { Suspense, useEffect, useRef, useState } from "react";
import { useChat } from "../hooks/useChat";
import { Character } from "./Character";

const Dots = (props) => {
  const { loading } = useChat();
  const [loadingText, setLoadingText] = useState("");
  const response = useRef("");

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setLoadingText((loadingText) => {
          if (loadingText.length > 2) {
            return ".";
          }
          return loadingText + ".";
        });
      }, 800);
      return () => clearInterval(interval);
    } else {
      setLoadingText("");

      $.get('http://127.0.0.1:5000/get_new_response', function (data) {
        if (response.current != data.new_response && data.new_response != '') {
            // console.log(data.new_response);
            response.current = data.new_response;

            $('#chatArea').append('<div class="chat-bubble ' + 'ai' + '">' + response.current + '</div>');
            // Scroll to the bottom of the chat area
            $('#chatArea').scrollTop($('#chatArea')[0].scrollHeight);
        }
        
    });
    }
  }, [loading]);

  if (!loading) return null;
  return (
    <group {...props}>
      <Text fontSize={0.14} anchorX={"left"} anchorY={"bottom"}>
        {loadingText}
        <meshBasicMaterial attach="material" color="black" />
      </Text>
    </group>
  );
};

export const CharacterControl = () => {
  const cameraControls = useRef();

  useEffect(() => {
    const controls = cameraControls.current;
    controls.setLookAt(0, 1.5, 5, 0, 1.7, 0);

    // Restrict camera movement
    controls.minDistance = 5;
    controls.maxDistance = 5; // Fix zoom level

    // Restrict vertical and horizontal rotation (with broader ranges)
    controls.minPolarAngle = Math.PI / 2; // 30 degrees (downward)
    controls.maxPolarAngle = Math.PI / 2; // 90 degrees (upward)

    // Restrict horizontal rotation if needed
    controls.minAzimuthAngle = -Math.PI / 4; // -45 degrees
    controls.maxAzimuthAngle = Math.PI / 4;  // 45 degrees

    controls.minAzimuthAngle = 0; // Limit left/right rotation
    controls.maxAzimuthAngle = 0;
  }, []);

  return (
    <>
      <CameraControls ref={cameraControls} />
      <Environment preset="sunset" />
      {/* Wrapping Dots into Suspense to prevent Blink when Troika/Font is loaded */}
      <Suspense>
        <Dots position-y={1.85} position-x={-0.09} />
      </Suspense>
      <Character />
    </>
  );
};
