export type Vector3 = {
  x: number;
  y: number;
  z: number;
};

export type PlayerState = {
  position: Vector3;
  stoolExtension: number;
  stoolTilt: number;
  velocity: Vector3;
  stoolExtensionRate: number;
  stoolTiltRate: number;
};

export type BallState = {
  position: Vector3;
  velocity: Vector3;
};

export type GameMode = 
  | 'MENU'
  | 'OPTIONS'
  | 'ANGLE_SELECT'
  | 'SPEED_SELECT'
  | 'PLAYING'
  | 'GAME_OVER'
  | 'HIGH_SCORES';

export type GameVariant = 'CLASSIC' | 'FRONTON';

export type GameState = {
  mode: GameMode;
  variant: GameVariant;
  time: number;
  frameCount: number;
  ball: BallState;
  player: PlayerState;
  score: number;
  highScore: number;
  bounceCount: number;
  maxHeight: number;
  maxDistance: number;
  isStuck: boolean;
  predictedImpact: {
    position: Vector3;
    time: number;
  };
};

export type GameControls = {
  horizontal: number;  // -1 to 1
  vertical: number;    // -1 to 1
  stoolExtend: number; // -1 to 1
  stoolTilt: number;   // -1 to 1
}; 