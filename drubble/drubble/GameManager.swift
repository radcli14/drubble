//
//  GameManager.swift
//  drubble
//
//  Created by Eliott Radcliffe on 5/22/25.
//

import SwiftUI
import SceneKit

enum GameMode: String {
    case menu = "Menu"
    case angleSelect = "Set Angle"
    case speedSelect = "Set Speed"
    case playing = "Playing"
    case gameOver = "Game Over"
}

class GameManager: NSObject, ObservableObject {
    // MARK: - Published Properties
    @Published var score = 0
    @Published var gameMode: GameMode = .menu
    
    // MARK: - SceneKit Properties
    let scene: SCNScene
    let camera: SCNNode
    
    // Game Objects
    private var player: SCNNode
    private var ball: SCNNode
    private var ground: SCNNode
    private var stool: SCNNode
    
    // Physics Parameters
    private let gravity: Float = 9.81
    private let ballRadius: Float = 0.2
    private let stoolRadius: Float = 0.35
    private let playerStartX: Float = 5.0
    private let playerStartY: Float = 1.5
    
    // Game State
    @Published private(set) var startAngle: Float = .pi / 4
    @Published private(set) var startSpeed: Float = 10.0
    private var isStuck = false
    private var lastUpdateTime: TimeInterval = 0
    
    override init() {
        // Initialize properties
        scene = SCNScene()
        scene.background.contents = UIColor.systemBlue.withAlphaComponent(0.3)
        
        // Setup Camera
        camera = SCNNode()
        camera.camera = SCNCamera()
        camera.position = SCNVector3(x: 0, y: 5, z: 10)
        camera.eulerAngles.x = -Float.pi / 6
        
        // Create Ground
        let groundGeometry = SCNFloor()
        groundGeometry.reflectivity = 0
        let groundMaterial = SCNMaterial()
        groundMaterial.diffuse.contents = UIColor.systemGreen
        groundGeometry.materials = [groundMaterial]
        ground = SCNNode(geometry: groundGeometry)
        
        // Create Player
        let playerGeometry = SCNCylinder(radius: 0.1, height: 1.5)
        let playerMaterial = SCNMaterial()
        playerMaterial.diffuse.contents = UIColor.systemBlue
        playerGeometry.materials = [playerMaterial]
        player = SCNNode(geometry: playerGeometry)
        player.position = SCNVector3(x: playerStartX, y: playerStartY, z: 0)
        
        // Create Stool
        let stoolGeometry = SCNCylinder(radius: CGFloat(stoolRadius), height: 0.1)
        let stoolMaterial = SCNMaterial()
        stoolMaterial.diffuse.contents = UIColor.systemOrange
        stoolGeometry.materials = [stoolMaterial]
        stool = SCNNode(geometry: stoolGeometry)
        stool.position = SCNVector3(x: playerStartX, y: playerStartY - 0.8, z: 0)
        
        // Create Ball
        let ballGeometry = SCNSphere(radius: CGFloat(ballRadius))
        let ballMaterial = SCNMaterial()
        ballMaterial.diffuse.contents = UIColor.systemRed
        ballGeometry.materials = [ballMaterial]
        ball = SCNNode(geometry: ballGeometry)
        ball.position = SCNVector3(x: 0, y: ballRadius, z: 0)
        
        // Call super.init() after all properties are initialized
        super.init()
        
        // Setup scene hierarchy and additional configuration
        scene.rootNode.addChildNode(camera)
        
        // Setup Lighting
        let ambientLight = SCNNode()
        ambientLight.light = SCNLight()
        ambientLight.light?.type = .ambient
        ambientLight.light?.intensity = 100
        scene.rootNode.addChildNode(ambientLight)
        
        let directionalLight = SCNNode()
        directionalLight.light = SCNLight()
        directionalLight.light?.type = .directional
        directionalLight.position = SCNVector3(x: 5, y: 5, z: 0)
        scene.rootNode.addChildNode(directionalLight)
        
        scene.rootNode.addChildNode(ground)
        scene.rootNode.addChildNode(player)
        scene.rootNode.addChildNode(stool)
        scene.rootNode.addChildNode(ball)
        
        // Setup Physics
        scene.physicsWorld.gravity = SCNVector3(x: 0, y: -gravity, z: 0)
        ground.physicsBody = SCNPhysicsBody(type: .static, shape: nil)
        ball.physicsBody = SCNPhysicsBody(type: .dynamic, shape: nil)
        ball.physicsBody?.mass = 1.0
        ball.physicsBody?.restitution = 0.8
        
        // Set up collision detection
        ball.physicsBody?.categoryBitMask = 1
        stool.physicsBody = SCNPhysicsBody(type: .kinematic, shape: nil)
        stool.physicsBody?.categoryBitMask = 2
        ground.physicsBody?.categoryBitMask = 4
        
        ball.physicsBody?.collisionBitMask = 2 | 4  // Collide with stool and ground
        
        // Set up physics contact delegate
        scene.physicsWorld.contactDelegate = self
        
        // Start update loop
        setupUpdateLoop()
    }
    
    private func setupUpdateLoop() {
        scene.isPaused = false
        let updateLoop = SCNAction.customAction(duration: 1.0/60.0) { [weak self] (_, _) in
            self?.update()
        }
        let forever = SCNAction.repeatForever(updateLoop)
        scene.rootNode.runAction(forever)
    }
    
    private func update() {
        guard gameMode == .playing else { return }
        
        // Check if ball is below ground (game over condition)
        if ball.position.y < -2 {
            gameMode = .gameOver
            return
        }
        
        // Update score based on successful bounces
        if ball.physicsBody?.velocity.y ?? 0 > 0 {
            isStuck = false
        }
    }
    
    // MARK: - Game Control Methods
    func startGame() {
        gameMode = .angleSelect
        resetBall()
        score = 0
    }
    
    func setAngle() {
        guard gameMode == .angleSelect else { return }
        gameMode = .speedSelect
    }
    
    func setSpeed() {
        guard gameMode == .speedSelect else { return }
        gameMode = .playing
        
        // Launch the ball
        let angle = startAngle
        let speed = startSpeed
        let velocity = SCNVector3(
            x: speed * cos(angle),
            y: speed * sin(angle),
            z: 0
        )
        ball.physicsBody?.velocity = velocity
    }
    
    func resetBall() {
        ball.position = SCNVector3(x: 0, y: ballRadius, z: 0)
        ball.physicsBody?.velocity = SCNVector3Zero
        isStuck = false
    }
    
    // MARK: - Player Control Methods
    func moveLeft() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        let action = SCNAction.moveBy(x: -0.5, y: 0, z: 0, duration: 0.1)
        player.runAction(action)
        stool.runAction(action)
    }
    
    func moveRight() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        let action = SCNAction.moveBy(x: 0.5, y: 0, z: 0, duration: 0.1)
        player.runAction(action)
        stool.runAction(action)
    }
    
    func moveUp() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        let action = SCNAction.moveBy(x: 0, y: 0.5, z: 0, duration: 0.1)
        player.runAction(action)
        stool.runAction(action)
    }
    
    func moveDown() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        let action = SCNAction.moveBy(x: 0, y: -0.5, z: 0, duration: 0.1)
        player.runAction(action)
        stool.runAction(action)
    }
    
    func extendStool() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        
        let currentY = stool.position.y
        let maxExtension = playerStartY - 0.4  // Maximum extension limit
        
        if currentY < maxExtension {
            let action = SCNAction.moveBy(x: 0, y: 0.1, z: 0, duration: 0.1)
            stool.runAction(action)
        }
    }
    
    func retractStool() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        
        let currentY = stool.position.y
        let minExtension = playerStartY - 1.2  // Minimum extension limit
        
        if currentY > minExtension {
            let action = SCNAction.moveBy(x: 0, y: -0.1, z: 0, duration: 0.1)
            stool.runAction(action)
        }
    }
    
    func tiltLeft() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        
        let currentRotation = stool.eulerAngles.z
        let maxTilt = Float.pi / 4  // 45 degrees maximum tilt
        
        if currentRotation < maxTilt {
            let action = SCNAction.rotateBy(x: 0, y: 0, z: 0.1, duration: 0.1)
            stool.runAction(action)
        }
    }
    
    func tiltRight() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        
        let currentRotation = stool.eulerAngles.z
        let minTilt = -Float.pi / 4  // -45 degrees maximum tilt
        
        if currentRotation > minTilt {
            let action = SCNAction.rotateBy(x: 0, y: 0, z: -0.1, duration: 0.1)
            stool.runAction(action)
        }
    }
    
    // MARK: - Angle and Speed Control
    func increaseAngle() {
        guard gameMode == .angleSelect else { return }
        startAngle = min(startAngle + 0.1, .pi / 2)  // Max 90 degrees
    }
    
    func decreaseAngle() {
        guard gameMode == .angleSelect else { return }
        startAngle = max(startAngle - 0.1, 0)  // Min 0 degrees
    }
    
    func increaseSpeed() {
        guard gameMode == .speedSelect else { return }
        startSpeed = min(startSpeed + 0.5, PhysicsParams.maxSpeed)
    }
    
    func decreaseSpeed() {
        guard gameMode == .speedSelect else { return }
        startSpeed = max(startSpeed - 0.5, 5.0)  // Minimum speed of 5 m/s
    }
}

// MARK: - Physics Contact Delegate
extension GameManager: SCNPhysicsContactDelegate {
    func physicsWorld(_ world: SCNPhysicsWorld, didBegin contact: SCNPhysicsContact) {
        let nodeA = contact.nodeA
        let nodeB = contact.nodeB
        
        // Handle ball-stool collision
        if (nodeA == ball && nodeB == stool) || (nodeA == stool && nodeB == ball) {
            if !isStuck {
                score += 1
                isStuck = true
            }
        }
        
        // Handle ball-ground collision
        if (nodeA == ball && nodeB == ground) || (nodeA == ground && nodeB == ball) {
            if ball.physicsBody?.velocity.y ?? 0 < PhysicsParams.dybtol {
                gameMode = .gameOver
            }
        }
    }
}
