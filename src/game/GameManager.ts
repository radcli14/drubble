import { PhysicsEngine } from '../physics/PhysicsEngine';
import { PhysicsParams } from '../constants/PhysicsParams';
import { GameState, GameMode, GameVariant, GameControls, Vector3 } from '../types/GameTypes';

export class GameManager {
  private state: GameState;
  private startAngle: number = Math.PI / 4;
  private startSpeed: number = 10.0;
  private anglePhase: number = 0;
  private speedPhase: number = 0;

  constructor() {
    this.state = this.getInitialState();
  }

  private getInitialState(): GameState {
    return {
      mode: 'MENU',
      variant: 'CLASSIC',
      time: 0,
      frameCount: 0,
      ball: {
        position: { x: 0, y: PhysicsParams.rb, z: 0 },
        velocity: { x: 0, y: 0, z: 0 },
      },
      player: {
        position: { x: PhysicsParams.x0, y: PhysicsParams.y0, z: 0 },
        stoolExtension: PhysicsParams.l0,
        stoolTilt: 0,
        velocity: { x: 0, y: 0, z: 0 },
        stoolExtensionRate: 0,
        stoolTiltRate: 0,
      },
      score: 0,
      highScore: 0,
      bounceCount: 0,
      maxHeight: 0,
      maxDistance: 0,
      isStuck: false,
      predictedImpact: {
        position: { x: 0, y: 0, z: 0 },
        time: 0,
      },
    };
  }

  public update(controls: GameControls): void {
    this.state.frameCount++;
    this.state.time += PhysicsParams.dt;

    switch (this.state.mode) {
      case 'ANGLE_SELECT':
        this.updateAngleSelect();
        break;
      case 'SPEED_SELECT':
        this.updateSpeedSelect();
        break;
      case 'PLAYING':
        this.updatePlaying(controls);
        break;
      default:
        break;
    }
  }

  private updateAngleSelect(): void {
    this.anglePhase += 3 * PhysicsParams.dt;
    this.startAngle = (Math.PI / 4) * (1 + 0.75 * Math.sin(this.anglePhase));
    this.updateLaunchVelocity();
  }

  private updateSpeedSelect(): void {
    this.speedPhase += 3 * PhysicsParams.dt;
    this.startSpeed = 10.0 * (1.2 + 0.6 * Math.sin(this.speedPhase));
    this.updateLaunchVelocity();
  }

  private updateLaunchVelocity(): void {
    const direction = this.state.variant === 'FRONTON' ? 1 : -1;
    this.state.ball.velocity = {
      x: direction * this.startSpeed * Math.cos(this.startAngle),
      y: this.startSpeed * Math.sin(this.startAngle),
      z: 0,
    };
  }

  private updatePlaying(controls: GameControls): void {
    // Update player physics
    this.updatePlayerPhysics(controls);

    // Update ball physics if not stuck
    if (!this.state.isStuck) {
      const { newBall, collision } = PhysicsEngine.updateBallPhysics(
        this.state.ball,
        this.state.player,
        this.state.variant,
        PhysicsParams.dt
      );

      this.state.ball = newBall;

      // Handle collisions
      if (collision === 'STOOL') {
        this.state.bounceCount++;
        this.updateScore();
      } else if (collision === 'GROUND') {
        if (Math.abs(this.state.ball.velocity.y) < PhysicsParams.dybtol) {
          this.state.isStuck = true;
          this.state.mode = 'GAME_OVER';
        }
      }

      // Update max height and distance
      this.state.maxHeight = Math.max(this.state.maxHeight, this.state.ball.position.y);
      this.state.maxDistance = Math.max(this.state.maxDistance, Math.abs(this.state.ball.position.x));

      // Update predicted impact
      const prediction = PhysicsEngine.predictBallTrajectory(
        this.state.ball,
        this.state.player,
        this.state.variant
      );
      this.state.predictedImpact = {
        position: prediction.impactPosition,
        time: prediction.impactTime,
      };
    }
  }

  private updatePlayerPhysics(controls: GameControls): void {
    // Simple player movement - can be made more complex with physics
    const player = this.state.player;
    
    // Update position based on controls
    player.position.x += controls.horizontal * PhysicsParams.vx * PhysicsParams.dt;
    player.position.y += controls.vertical * 2 * PhysicsParams.dt;
    
    // Update stool
    player.stoolExtension += controls.stoolExtend * 2 * PhysicsParams.dt;
    player.stoolTilt += controls.stoolTilt * 2 * PhysicsParams.dt;

    // Clamp values
    player.position.y = Math.max(PhysicsParams.d, Math.min(player.position.y, 4));
    player.stoolExtension = Math.max(0.5, Math.min(player.stoolExtension, 2.5));
    player.stoolTilt = Math.max(-Math.PI/3, Math.min(player.stoolTilt, Math.PI/3));
  }

  private updateScore(): void {
    this.state.score = Math.floor(
      this.state.maxDistance * 
      this.state.maxHeight * 
      this.state.bounceCount
    );
    this.state.highScore = Math.max(this.state.score, this.state.highScore);
  }

  public getState(): GameState {
    return this.state;
  }

  public setMode(mode: GameMode): void {
    this.state.mode = mode;
    if (mode === 'PLAYING') {
      this.state = this.getInitialState();
      this.state.mode = 'PLAYING';
    }
  }

  public setVariant(variant: GameVariant): void {
    this.state.variant = variant;
    this.state = this.getInitialState();
    this.state.variant = variant;
  }
} 