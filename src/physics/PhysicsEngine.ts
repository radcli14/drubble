import { PhysicsParams } from '../constants/PhysicsParams';
import { Vector3, BallState, PlayerState, GameVariant } from '../types/GameTypes';

export class PhysicsEngine {
  private static readonly MAX_PREDICTION_POINTS = 10;
  private static readonly PREDICTION_TIME_STEP = 0.1;

  static predictBallTrajectory(
    ball: BallState,
    player: PlayerState,
    variant: GameVariant
  ): { positions: Vector3[]; impactTime: number; impactPosition: Vector3 } {
    const positions: Vector3[] = [];
    let currentPos = { ...ball.position };
    let currentVel = { ...ball.velocity };
    let dt = this.PREDICTION_TIME_STEP;
    let impactTime = 0;
    let impactPosition = { ...currentPos };
    let hasImpact = false;

    for (let i = 0; i < this.MAX_PREDICTION_POINTS && !hasImpact; i++) {
      // Update position
      currentPos = {
        x: currentPos.x + currentVel.x * dt,
        y: currentPos.y + currentVel.y * dt - 0.5 * PhysicsParams.g * dt * dt,
        z: currentPos.z + currentVel.z * dt,
      };

      // Update velocity
      currentVel = {
        x: currentVel.x,
        y: currentVel.y - PhysicsParams.g * dt,
        z: currentVel.z,
      };

      positions.push({ ...currentPos });

      // Check for collisions
      const stoolCollision = this.checkStoolCollision(currentPos, player);
      const groundCollision = this.checkGroundCollision(currentPos);
      const wallCollision = variant === 'FRONTON' ? 
        this.checkWallCollision(currentPos) : false;

      if (stoolCollision || groundCollision || wallCollision) {
        hasImpact = true;
        impactTime = (i + 1) * dt;
        impactPosition = { ...currentPos };
      }
    }

    return {
      positions,
      impactTime,
      impactPosition,
    };
  }

  static updateBallPhysics(
    ball: BallState,
    player: PlayerState,
    variant: GameVariant,
    dt: number
  ): { newBall: BallState; collision: 'NONE' | 'STOOL' | 'GROUND' | 'WALL' } {
    const newPosition = {
      x: ball.position.x + ball.velocity.x * dt,
      y: ball.position.y + ball.velocity.y * dt - 0.5 * PhysicsParams.g * dt * dt,
      z: ball.position.z + ball.velocity.z * dt,
    };

    const newVelocity = {
      x: ball.velocity.x,
      y: ball.velocity.y - PhysicsParams.g * dt,
      z: ball.velocity.z,
    };

    // Check collisions
    if (this.checkStoolCollision(newPosition, player)) {
      const bounceVel = this.calculateStoolBounce(ball, player);
      return {
        newBall: {
          position: newPosition,
          velocity: bounceVel,
        },
        collision: 'STOOL',
      };
    }

    if (this.checkGroundCollision(newPosition)) {
      const bounceVel = this.calculateGroundBounce(ball);
      return {
        newBall: {
          position: { ...newPosition, y: PhysicsParams.rb },
          velocity: bounceVel,
        },
        collision: 'GROUND',
      };
    }

    if (variant === 'FRONTON' && this.checkWallCollision(newPosition)) {
      const bounceVel = this.calculateWallBounce(ball);
      return {
        newBall: {
          position: newPosition,
          velocity: bounceVel,
        },
        collision: 'WALL',
      };
    }

    return {
      newBall: {
        position: newPosition,
        velocity: newVelocity,
      },
      collision: 'NONE',
    };
  }

  private static checkStoolCollision(position: Vector3, player: PlayerState): boolean {
    // Simplified stool collision check - can be made more accurate
    const stoolPos = {
      x: player.position.x,
      y: player.position.y + PhysicsParams.d + player.stoolExtension * Math.cos(player.stoolTilt),
      z: player.position.z,
    };

    const dx = position.x - stoolPos.x;
    const dy = position.y - stoolPos.y;
    const dz = position.z - stoolPos.z;
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);

    return distance < (PhysicsParams.stoolRadius + PhysicsParams.rb);
  }

  private static checkGroundCollision(position: Vector3): boolean {
    return position.y <= PhysicsParams.rb;
  }

  private static checkWallCollision(position: Vector3): boolean {
    return position.x >= PhysicsParams.wallDistance - PhysicsParams.rb;
  }

  private static calculateStoolBounce(ball: BallState, player: PlayerState): Vector3 {
    const [CORx, CORy] = PhysicsParams.COR_s;
    return {
      x: -ball.velocity.x * CORx,
      y: -ball.velocity.y * CORy,
      z: ball.velocity.z,
    };
  }

  private static calculateGroundBounce(ball: BallState): Vector3 {
    const [CORx, CORy] = PhysicsParams.COR_g;
    return {
      x: ball.velocity.x * CORx,
      y: -ball.velocity.y * CORy,
      z: ball.velocity.z,
    };
  }

  private static calculateWallBounce(ball: BallState): Vector3 {
    const [CORx, CORy] = PhysicsParams.COR_w;
    return {
      x: -ball.velocity.x * CORx,
      y: ball.velocity.y,
      z: ball.velocity.z,
    };
  }
} 