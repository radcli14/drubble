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
} 
