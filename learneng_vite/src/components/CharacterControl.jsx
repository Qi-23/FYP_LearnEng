import { Suspense, useEffect, useRef, useState } from "react";
import { CameraControls, Environment, useTexture } from "@react-three/drei";
import * as THREE from "three";
import { Character } from "./Character"; // Assuming you have your Character component
import { useThree } from "@react-three/fiber";

export const CharacterControl = () => {
  const cameraControls = useRef();
  const backgroundTexture = useTexture("/page_photo/hotelFrontDesk.png"); // Path to your image
  const [isTextureLoaded, setIsTextureLoaded] = useState(false); // State to track if the texture is loaded

  const { camera, viewport } = useThree(); // Getting the camera and viewport from the scene
  const { width: viewportWidth, height: viewportHeight } = viewport;

  // Check if the texture is loaded
  useEffect(() => {
    if (backgroundTexture) {
      setIsTextureLoaded(true); // Update state once texture is loaded
    }
  }, [backgroundTexture]);

  // Set up camera controls
  useEffect(() => {
    const controls = cameraControls.current;
    controls.setLookAt(0, 1.5, 5, 0, 1.7, 0);
  }, []);

  // Camera FOV (field of view) and aspect ratio
  const fov = camera.fov * (Math.PI / 180); // Convert FOV from degrees to radians
  const aspect = viewportWidth / viewportHeight;

  // Calculate the distance to the background image (based on FOV)
  const distance = 5; // Set this distance based on your scene requirements

  // Calculate the background image height and width based on the camera's FOV
  const imageHeight = 2 * Math.tan(fov / 2) * distance; // Height of the image based on FOV and distance
  const imageWidth = imageHeight * aspect; // Width based on the aspect ratio

  // Scaling factor to increase image size (e.g., 1.2 will increase size by 20%)
  const scaleFactor = 1.5; // Increase size by 20%

  // Apply the scaling factor to the image dimensions
  const scaledImageHeight = imageHeight * scaleFactor;
  const scaledImageWidth = imageWidth * scaleFactor;

  // Get the camera's forward direction (where the camera is looking)
  const cameraDirection = new THREE.Vector3();
  camera.getWorldDirection(cameraDirection);

  // Position the background in front of the camera, adjusted for its direction
  const imagePosition = new THREE.Vector3();
  imagePosition.copy(camera.position).add(cameraDirection.multiplyScalar(-distance));

  imagePosition.y = 1.7; 
  imagePosition.z = -0.5; 

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

      {/* Wait for texture to load before rendering the background */}
      {isTextureLoaded && (
        <Suspense fallback={<mesh><boxGeometry /><meshBasicMaterial color="gray" /></mesh>}>
          <mesh position={imagePosition.toArray()}>
            <planeGeometry args={[scaledImageWidth, scaledImageHeight]} />
            <meshStandardMaterial map={backgroundTexture} side={THREE.DoubleSide} />
          </mesh>
        </Suspense>
      )}

      <Character />
    </>
  );
};
