//
//  PhysicsParams.swift
//  drubble
//
//  Created by Eliott Radcliffe on 5/22/25.
//

import Foundation

struct PhysicsParams {
    // Physics constants
    static let gravity: Float = 9.81            // Gravitational acceleration [m/s^2]
    static let corStool: (Float, Float) = (0.70, 0.90)  // Coefficient of restitution when ball hits stool
    static let corGround: (Float, Float) = (0.50, 0.70) // COR when ball hits ground
    static let corWall: (Float, Float) = (0.80, 0.90)   // COR when ball hits wall (for Fronton mode)
    static let ballRadius: Float = 0.2          // Radius of the ball
    
    // Player parameters
    static let playerMass: Float = 50.0    // Mass of player [kg]
    static let stoolMass: Float = 2.0      // Mass of stool [kg]
    static let totalMass: Float = playerMass + stoolMass  // Total mass [kg]
    static let startX: Float = 5.0         // Initial player position [m]
    static let startY: Float = 1.5         // Equilibrium position of player CG [m]
    static let playerHeight: Float = 2.0    // Height of player [m]
    static let stoolOffset: Float = 0.3    // Relative position from player CG to stool rotation axis [m]
    static let stoolLength: Float = 1.5    // Equilibrium position of stool
    static let horizontalAccel: Float = 1.5 // Horizontal acceleration [g]
    static let verticalFreq: Float = 0.8   // vertical frequency [Hz]
    static let stoolExtendFreq: Float = 2.2 // Stool extension frequency
    static let stoolTiltFreq: Float = 1.25 // Stool tilt frequency [Hz]
    static let maxSpeed: Float = 10.0      // Horizontal top speed [m/s]
    
    // Stool parameters
    static let stoolRadii: [Float] = [0.35, 0.30, 0.25]  // Different sizes for difficulty levels
    static let stoolHandPos: Float = -0.6
    
    // Game settings
    static let frameRate: Int = 60
    static let dt: Float = 1.0 / Float(frameRate)
    static let dybtol: Float = 4.0        // Tolerance on last bounce speed before stopping motion
    
    // Fronton wall parameters
    static let wallDistance: Float = 15.0  // Distance to the wall from origin [m]
    static let wallHeight: Float = 10.0    // Height of the wall [m]
    static let wallWidth: Float = 8.0      // Width of the wall [m]
    
    // Initial conditions
    static let initialAngle: Float = .pi / 4
    static let initialSpeed: Float = 10.0
    
    static let maxHorizForce: Float = horizontalAccel * totalMass * gravity  // Max horizontal force [N]
    static let horizControlGain: Float = 1.5     // Control gain on horizontal force
    
    // Spring constants and damping
    static let legStiffness: Float = totalMass * pow(verticalFreq * 2 * .pi, 2)  // Leg stiffness [N/m]
    static let legStrength: Float = legStiffness * 0.3  // Leg strength [N]
    static let armStiffness: Float = stoolMass * pow(stoolExtendFreq * 2 * .pi, 2)  // Arm stiffness [N/m]
    static let armStrength: Float = armStiffness * 0.3  // Arm strength [N]
    static let tiltStiffness: Float = (stoolMass * pow(stoolLength, 2)) * pow(stoolTiltFreq * 2 * .pi, 2)  // Tilt stiffness [N-m/rad]
    static let tiltStrength: Float = tiltStiffness * 0.8  // Tilt strength [N-m]
    static let tiltControlGain: Float = 0.8     // Control gain on tilt
    
    // Damping coefficients
    static let horizDamping: Float = maxHorizForce / maxSpeed  // Horizontal damping [N-s/m]
    static let vertDampingRatio: Float = 0.1    // Vertical damping ratio
    static let vertDamping: Float = 2 * vertDampingRatio * sqrt(legStiffness * totalMass)  // Vertical damping [N-s/m]
    static let armDampingRatio: Float = 0.08    // Arm damping ratio
    static let armDamping: Float = 2 * armDampingRatio * sqrt(armStiffness * totalMass)  // Arm damping [N-s/m]
    static let tiltDampingRatio: Float = 0.09   // Stool tilt damping ratio
    static let tiltDamping: Float = 2 * armDampingRatio * sqrt(tiltStiffness * totalMass)  // Tilt damping [N-m-s/rad]
    
    // State limits to prevent crashing
    static let horizSpeedLimit: (Float, Float) = (-20, 20)
    static let vertPosLimit: (Float, Float) = (-1, 4)
    static let vertSpeedLimit: (Float, Float) = (-20, 20)
    static let stoolLengthLimit: (Float, Float) = (-1, 3)
    static let stoolExtendSpeedLimit: (Float, Float) = (-20, 20)
    static let stoolTiltLimit: (Float, Float) = (-3.14, 3.14)
    static let stoolTiltSpeedLimit: (Float, Float) = (-20, 20)
    
    // Animation parameters
    static let stanceWidth: Float = 0.3
    static let footStepLength: Float = 1.25
    static let footStepRate: Float = 3.0
    static let footRecoveryRate: Float = 12.0
    static let legLength: Float = 0.9 * (startY - stoolOffset)
} 
