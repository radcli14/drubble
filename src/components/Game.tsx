import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Cylinder, Sphere } from '@react-three/drei';
import { GameManager } from '../game/GameManager';
import { GameControls } from '../types/GameTypes';
import { PhysicsParams } from '../constants/PhysicsParams';

// Player character component
const Player = ({ position, stoolExtension, stoolTilt }: any) => {
  // Body parts
  const bodyHeight = 1.5;
  const bodyRadius = 0.1;
  const headRadius = 0.2;
  const armLength = 0.6;
  const legLength = 0.8;

  return (
    <group position={[position.x, position.y, position.z]}>
      {/* Body */}
      <Cylinder
        args={[bodyRadius, bodyRadius, bodyHeight, 8]}
        position={[0, bodyHeight/2, 0]}
      >
        <meshStandardMaterial color="blue" />
      </Cylinder>

      {/* Head */}
      <Sphere
        args={[headRadius, 8, 8]}
        position={[0, bodyHeight + headRadius, 0]}
      >
        <meshStandardMaterial color="pink" />
      </Sphere>

      {/* Arms */}
      <Cylinder
        args={[0.05, 0.05, armLength, 8]}
        position={[-bodyRadius*2, bodyHeight*0.8, 0]}
        rotation={[0, 0, Math.PI/4]}
      >
        <meshStandardMaterial color="blue" />
      </Cylinder>
      <Cylinder
        args={[0.05, 0.05, armLength, 8]}
        position={[bodyRadius*2, bodyHeight*0.8, 0]}
        rotation={[0, 0, -Math.PI/4]}
      >
        <meshStandardMaterial color="blue" />
      </Cylinder>

      {/* Legs */}
      <Cylinder
        args={[0.05, 0.05, legLength, 8]}
        position={[-bodyRadius*1.5, legLength/2, 0]}
      >
        <meshStandardMaterial color="blue" />
      </Cylinder>
      <Cylinder
        args={[0.05, 0.05, legLength, 8]}
        position={[bodyRadius*1.5, legLength/2, 0]}
      >
        <meshStandardMaterial color="blue" />
      </Cylinder>

      {/* Stool */}
      <group rotation={[0, 0, stoolTilt]}>
        <Cylinder
          args={[0.05, 0.05, stoolExtension, 8]}
          position={[0, bodyHeight*0.8, 0]}
          rotation={[0, 0, Math.PI/2]}
        >
          <meshStandardMaterial color="brown" />
        </Cylinder>
        <Cylinder
          args={[PhysicsParams.stoolRadius, PhysicsParams.stoolRadius, 0.1, 16]}
          position={[stoolExtension/2, bodyHeight*0.8, 0]}
          rotation={[Math.PI/2, 0, 0]}
        >
          <meshStandardMaterial color="brown" />
        </Cylinder>
      </group>
    </group>
  );
};

// Ball component
const Ball = ({ position }: any) => (
  <Sphere args={[PhysicsParams.rb, 32, 32]} position={[position.x, position.y, position.z]}>
    <meshStandardMaterial color="red" />
  </Sphere>
);

// Wall component for Fronton mode
const Wall = () => (
  <group position={[PhysicsParams.wallDistance, PhysicsParams.wallHeight/2, 0]}>
    <Cylinder
      args={[0.2, 0.2, PhysicsParams.wallHeight, 8]}
      rotation={[0, 0, 0]}
    >
      <meshStandardMaterial color="gray" />
    </Cylinder>
  </group>
);

// Ground plane
const Ground = () => (
  <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, 0, 0]}>
    <planeGeometry args={[100, 100]} />
    <meshStandardMaterial color="green" />
  </mesh>
);

// Camera controller
const CameraController = ({ target }: any) => {
  const { camera } = useThree();
  
  useFrame(() => {
    // Position camera to keep both player and ball in view
    const cameraDistance = 15;
    const cameraHeight = 8;
    camera.position.x = target.x - cameraDistance * 0.7;
    camera.position.y = cameraHeight;
    camera.position.z = cameraDistance;
    camera.lookAt(target.x, target.y, 0);
  });

  return null;
};

// Main game component
export const Game = () => {
  const gameManager = useRef(new GameManager());
  const [controls, setControls] = useState<GameControls>({
    horizontal: 0,
    vertical: 0,
    stoolExtend: 0,
    stoolTilt: 0,
  });

  // Handle keyboard input
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowLeft':
          setControls(c => ({ ...c, horizontal: -1 }));
          break;
        case 'ArrowRight':
          setControls(c => ({ ...c, horizontal: 1 }));
          break;
        case 'ArrowUp':
          setControls(c => ({ ...c, vertical: 1 }));
          break;
        case 'ArrowDown':
          setControls(c => ({ ...c, vertical: -1 }));
          break;
        case 'w':
          setControls(c => ({ ...c, stoolExtend: 1 }));
          break;
        case 's':
          setControls(c => ({ ...c, stoolExtend: -1 }));
          break;
        case 'a':
          setControls(c => ({ ...c, stoolTilt: -1 }));
          break;
        case 'd':
          setControls(c => ({ ...c, stoolTilt: 1 }));
          break;
        case ' ':
          if (gameManager.current.getState().mode === 'ANGLE_SELECT') {
            gameManager.current.setMode('SPEED_SELECT');
          } else if (gameManager.current.getState().mode === 'SPEED_SELECT') {
            gameManager.current.setMode('PLAYING');
          }
          break;
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowLeft':
        case 'ArrowRight':
          setControls(c => ({ ...c, horizontal: 0 }));
          break;
        case 'ArrowUp':
        case 'ArrowDown':
          setControls(c => ({ ...c, vertical: 0 }));
          break;
        case 'w':
        case 's':
          setControls(c => ({ ...c, stoolExtend: 0 }));
          break;
        case 'a':
        case 'd':
          setControls(c => ({ ...c, stoolTilt: 0 }));
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  // Game loop
  useFrame(() => {
    gameManager.current.update(controls);
  });

  const state = gameManager.current.getState();

  return (
    <Canvas style={{ width: '100%', height: '100%' }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      
      <CameraController target={state.ball.position} />

      <Player
        position={state.player.position}
        stoolExtension={state.player.stoolExtension}
        stoolTilt={state.player.stoolTilt}
      />
      
      <Ball position={state.ball.position} />
      
      {state.variant === 'FRONTON' && <Wall />}
      
      <Ground />
    </Canvas>
  );
}; 