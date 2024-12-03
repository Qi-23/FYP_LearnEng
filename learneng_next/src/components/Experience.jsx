import { CameraControls, Environment, Gltf, OrbitControls } from "@react-three/drei";
import { Character } from "./Character";

export const Experience = () => {
    return (
        <>
            {/* <OrbitControls /> */}
            <Character position={[0, -3.3, 0]} scale={2} />
            <Environment preset="sunset" />
        </>
    );
};