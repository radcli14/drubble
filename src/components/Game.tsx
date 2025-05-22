import React, { useState, useEffect } from 'react';
import { View, Platform } from 'react-native';
import { Canvas, useFrame } from '@react-three/fiber/native';
import { Cylinder, Sphere, OrthographicCamera } from '@react-three/drei/native';
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
        <meshBasicMaterial color="blue" />
      </Cylinder>

      {/* Head */}
      <Sphere
        args={[headRadius, 8, 8]}
        position={[0, bodyHeight + headRadius, 0]}
      >
        <meshBasicMaterial color="pink" />
      </Sphere>

      {/* Arms */}
      <Cylinder
        args={[0.05, 0.05, armLength, 8]}
        position={[-bodyRadius*2, bodyHeight*0.8, 0]}
        rotation={[0, 0, Math.PI/4]}
      >
        <meshBasicMaterial color="blue" />
      </Cylinder>
      <Cylinder
        args={[0.05, 0.05, armLength, 8]}
        position={[bodyRadius*2, bodyHeight*0.8, 0]}
        rotation={[0, 0, -Math.PI/4]}
      >
        <meshBasicMaterial color="blue" />
      </Cylinder>

      {/* Legs */}
      <Cylinder
        args={[0.05, 0.05, legLength, 8]}
        position={[-bodyRadius*1.5, legLength/2, 0]}
      >
        <meshBasicMaterial color="blue" />
      </Cylinder>
      <Cylinder
        args={[0.05, 0.05, legLength, 8]}
        position={[bodyRadius*1.5, legLength/2, 0]}
      >
        <meshBasicMaterial color="blue" />
      </Cylinder>

      {/* Stool */}
      <group position={[0, stoolExtension, 0]} rotation={[0, 0, stoolTilt]}>
        <Cylinder
          args={[0.2, 0.2, 0.05, 8]}
          position={[0, 0, 0]}
        >
          <meshBasicMaterial color="brown" />
        </Cylinder>
      </group>
    </group>
  );
};

// Ball component
const Ball = ({ position }: any) => (
  <Sphere args={[PhysicsParams.rb, 32, 32]} position={[position.x, position.y, position.z]}>
    <meshBasicMaterial color="red" />
  </Sphere>
);

// Wall component for Fronton mode
const Wall = () => (
  <group position={[PhysicsParams.wallDistance, PhysicsParams.wallHeight/2, 0]}>
    <Cylinder
      args={[0.2, 0.2, PhysicsParams.wallHeight, 8]}
      rotation={[0, 0, 0]}
    >
      <meshBasicMaterial color="gray" />
    </Cylinder>
  </group>
);

// Ground plane
const Ground = () => (
  <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, 0, 0]}>
    <planeGeometry args={[100, 100]} />
    <meshBasicMaterial color="green" />
  </mesh>
);

// Scene component that handles the 3D rendering
const Scene = ({ gameManager, controls }: { gameManager: GameManager, controls: GameControls }) => {
  const state = gameManager.getState();

  // Update game state every frame
  useFrame(() => {
    gameManager.update(controls);
  });

  return (
    <>
      <OrthographicCamera
        makeDefault
        position={[0, 5, 10]}
        zoom={50}
        near={0.1}
        far={1000}
      />
      
      <color attach="background" args={["#87CEEB"]} /> {/* Sky blue background */}
      
      <Player
        position={state.player.position}
        stoolExtension={state.player.stoolExtension}
        stoolTilt={state.player.stoolTilt}
      />
      
      <Ball position={state.ball.position} />
      
      {state.variant === 'FRONTON' && <Wall />}
      
      <Ground />
    </>
  );
};

// Main game component
export const Game = () => {
  const [gameManager] = useState(() => new GameManager());
  const [controls, setControls] = useState<GameControls>({
    horizontal: 0,
    vertical: 0,
    stoolExtend: 0,
    stoolTilt: 0,
  });

  // Handle keyboard input
  useEffect(() => {
    if (Platform.OS === 'web') {
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
            if (gameManager.getState().mode === 'ANGLE_SELECT') {
              gameManager.setMode('SPEED_SELECT');
            } else if (gameManager.getState().mode === 'SPEED_SELECT') {
              gameManager.setMode('PLAYING');
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
    }
  }, [gameManager]);

  return (
    <View style={{ flex: 1 }}>
      <Canvas gl={{ alpha: false }}>
        <Scene gameManager={gameManager} controls={controls} />
      </Canvas>
    </View>
  );
}; 