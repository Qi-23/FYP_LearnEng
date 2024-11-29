import { Canvas } from "@react-three/fiber"
import { Experience } from "@/components/Experience";

export default function character() {
  return (
    <main className="h-screen min-h-screen">
    <Canvas shadows camera={{ position: [0, 0, 8], fov: 10 }}>
      <Experience />
    </Canvas>
    </main>
  );
}