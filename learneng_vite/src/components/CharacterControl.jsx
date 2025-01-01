import { Suspense, useEffect, useRef, useState } from "react";
import { CameraControls, Environment, Text, useTexture } from "@react-three/drei";
import * as THREE from "three";
import { Character } from "./Character";
import { useThree } from "@react-three/fiber";
import { useChat } from "../hooks/useChat";

export const CharacterControl = ({ character, backgroundImage }) => {
  const cameraControls = useRef();
  const [backgroundTexture, setBackgroundTexture] = useState(null);
  const [isTextureLoaded, setIsTextureLoaded] = useState(false);

  const { camera, viewport } = useThree();
  const { width: viewportWidth, height: viewportHeight } = viewport;

  const { loading } = useChat();
  const [loadingText, setLoadingText] = useState("");
  const response = useRef("");

  useEffect(() => {
    if (backgroundImage && typeof backgroundImage === "string") {
      if (backgroundImage.startsWith("data:image/")) {
        const texture = new THREE.TextureLoader().load(backgroundImage);
        setBackgroundTexture(texture);
        setIsTextureLoaded(true);
      } else {
        console.error("Invalid base64 image format.");
        setIsTextureLoaded(false);
      }
    } else {
      console.error("backgroundImage is not a valid string.");
      setIsTextureLoaded(false);
    }
  }, [backgroundImage]);

  useEffect(() => {
    const controls = cameraControls.current;
    controls.setLookAt(0, 1.5, 5, 0, 1.7, 0);
  }, []);

  const fov = camera.fov * (Math.PI / 180);
  const aspect = viewportWidth / viewportHeight;
  const distance = 5;
  const imageHeight = 2 * Math.tan(fov / 2) * distance;
  const imageWidth = imageHeight * aspect;
  const scaleFactor = 1.5;
  const scaledImageHeight = imageHeight * scaleFactor;
  const scaledImageWidth = imageWidth * scaleFactor;
  const cameraDirection = new THREE.Vector3();
  camera.getWorldDirection(cameraDirection);
  const imagePosition = new THREE.Vector3();
  imagePosition.copy(camera.position).add(cameraDirection.multiplyScalar(-distance));

  imagePosition.y = 1.7;
  imagePosition.z = -0.5;

  const Dots = (props) => {
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

  return (
    <>
      <CameraControls ref={cameraControls} />
      <Environment preset="sunset" />

      {isTextureLoaded && backgroundTexture && (
        <Suspense fallback={<mesh><boxGeometry /><meshBasicMaterial color="gray" /></mesh>}>
          <Dots position-y={1.85} position-x={-0.09} />
          <mesh position={imagePosition.toArray()}>
            <planeGeometry args={[scaledImageWidth, scaledImageHeight]} />
            <meshStandardMaterial map={backgroundTexture} side={THREE.DoubleSide} />
          </mesh>
        </Suspense>
      )}
      {character && (
        <Character key={character} character={character} />
      )}
    </>
  );
};
