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
    private var player: SCNNode  // Root node for the player
    private var playerBody: SCNNode
    private var playerHead: SCNNode
    private var playerArms: [SCNNode]
    private var playerLegs: [SCNNode]
    private var ball: SCNNode
    private var ground: SCNNode
    private var stool: SCNNode
    private var stoolRungs: [SCNNode]
    
    // Physics Parameters
    private let gravity: Float = 9.81
    private let ballRadius: Float = 0.2
    private let stoolRadius: Float = 0.35
    private let playerStartX: Float = 5.0
    private let playerStartY: Float = 1.5
    private let playerHeight: Float = 2.0
    private let limbThickness: Float = 0.1
    
    // Game State
    @Published private(set) var startAngle: Float = .pi / 4
    @Published private(set) var startSpeed: Float = 10.0
    private var isStuck = false
    private var lastUpdateTime: TimeInterval = 0
    
    // Movement State
    private var isMovingLeft = false
    private var isMovingRight = false
    private let moveSpeed: Float = 3.0  // Units per second
    
    override init() {
        // Initialize properties
        scene = SCNScene()
        scene.background.contents = UIColor.clear
        
        // Setup Camera
        camera = SCNNode()
        camera.camera = SCNCamera()
        camera.position = SCNVector3(x: 5, y: 8, z: 15)
        camera.eulerAngles.x = -Float.pi / 6
        camera.look(at: SCNVector3(x: 5, y: 0, z: 0))
        
        // Create Ground
        let groundGeometry = SCNFloor()
        groundGeometry.reflectivity = 0
        let groundMaterial = SCNMaterial()
        groundMaterial.diffuse.contents = UIColor.systemGray.withAlphaComponent(0.3)
        groundMaterial.transparency = 0.7
        groundGeometry.materials = [groundMaterial]
        ground = SCNNode(geometry: groundGeometry)
        
        // Create Player
        player = SCNNode()  // Root node
        player.position = SCNVector3(x: playerStartX, y: 0, z: 0)
        
        // Body
        let bodyGeometry = SCNCylinder(radius: CGFloat(limbThickness), height: CGFloat(playerHeight) * 0.4)
        let bodyMaterial = SCNMaterial()
        bodyMaterial.diffuse.contents = UIColor.systemBlue
        bodyGeometry.materials = [bodyMaterial]
        playerBody = SCNNode(geometry: bodyGeometry)
        playerBody.position = SCNVector3(x: 0, y: playerHeight * 0.5, z: 0)
        
        // Head
        let headGeometry = SCNSphere(radius: CGFloat(limbThickness) * 2)
        headGeometry.materials = [bodyMaterial]
        playerHead = SCNNode(geometry: headGeometry)
        playerHead.position = SCNVector3(x: 0, y: playerHeight * 0.7, z: 0)
        
        // Arms
        playerArms = []
        let armLength: Float = 0.6
        for i in 0...1 {
            let armGeometry = SCNCylinder(radius: CGFloat(limbThickness) * 0.8, height: CGFloat(armLength))
            let arm = SCNNode(geometry: armGeometry)
            arm.position = SCNVector3(x: (i == 0 ? -1 : 1) * limbThickness * 3, 
                                    y: playerHeight * 0.6,
                                    z: 0)
            arm.eulerAngles.z = (i == 0 ? 1 : -1) * Float.pi / 6
            playerArms.append(arm)
        }
        
        // Legs
        playerLegs = []
        let legLength: Float = 0.7
        for i in 0...1 {
            let legGeometry = SCNCylinder(radius: CGFloat(limbThickness), height: CGFloat(legLength))
            let leg = SCNNode(geometry: legGeometry)
            leg.position = SCNVector3(x: (i == 0 ? -1 : 1) * limbThickness * 2,
                                    y: playerHeight * 0.3,
                                    z: 0)
            playerLegs.append(leg)
        }
        
        // Create Stool with rungs
        stool = SCNNode()
        stool.position = SCNVector3(x: playerStartX, y: playerHeight * 0.9, z: 0)
        
        let stoolGeometry = SCNCylinder(radius: CGFloat(stoolRadius), height: 0.1)
        let stoolMaterial = SCNMaterial()
        stoolMaterial.diffuse.contents = UIColor.systemOrange
        stoolGeometry.materials = [stoolMaterial]
        let stoolTop = SCNNode(geometry: stoolGeometry)
        
        // Create rungs
        stoolRungs = []
        let rungCount = 2
        let rungSpacing: Float = 0.2
        for i in 0..<rungCount {
            let rungGeometry = SCNCylinder(radius: CGFloat(limbThickness), height: CGFloat(stoolRadius) * 2)
            rungGeometry.materials = [stoolMaterial]
            let rung = SCNNode(geometry: rungGeometry)
            rung.position = SCNVector3(x: 0, y: -Float(i + 1) * rungSpacing, z: 0)
            rung.eulerAngles.x = Float.pi / 2  // Rotate to be horizontal
            stoolRungs.append(rung)
        }
        
        // Create Ball
        let ballGeometry = SCNSphere(radius: CGFloat(ballRadius))
        let ballMaterial = SCNMaterial()
        ballMaterial.diffuse.contents = UIColor.systemRed
        ballGeometry.materials = [ballMaterial]
        ball = SCNNode(geometry: ballGeometry)
        ball.position = SCNVector3(x: 0, y: ballRadius, z: 0)
        
        // Call super.init() after all properties are initialized
        super.init()
        
        // Setup scene hierarchy
        scene.rootNode.addChildNode(camera)
        scene.rootNode.addChildNode(ground)
        scene.rootNode.addChildNode(player)
        scene.rootNode.addChildNode(ball)
        
        // Add player parts to player node
        player.addChildNode(playerBody)
        player.addChildNode(playerHead)
        playerArms.forEach { player.addChildNode($0) }
        playerLegs.forEach { player.addChildNode($0) }
        
        // Add stool parts
        scene.rootNode.addChildNode(stool)
        stool.addChildNode(stoolTop)
        stoolRungs.forEach { stool.addChildNode($0) }
        
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
        
        ball.physicsBody?.collisionBitMask = 2 | 4
        
        scene.physicsWorld.contactDelegate = self
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
        
        // Handle continuous movement
        if isMovingLeft {
            movePlayerAndStool(deltaX: -moveSpeed / 60)  // 60 fps
        } else if isMovingRight {
            movePlayerAndStool(deltaX: moveSpeed / 60)
        }
        
        // Check if ball is below ground
        if ball.position.y < -2 {
            gameMode = .gameOver
            return
        }
        
        if ball.physicsBody?.velocity.y ?? 0 > 0 {
            isStuck = false
        }
    }
    
    private func movePlayerAndStool(deltaX: Float) {
        let action = SCNAction.moveBy(x: CGFloat(deltaX), y: 0, z: 0, duration: 0)
        player.runAction(action)
        stool.runAction(action)
        
        // Animate legs while moving
        animateLegsForMovement()
    }
    
    private func animateLegsForMovement() {
        let legSwingAngle: Float = Float.pi / 6
        
        // Alternate leg positions
        let timestamp = CACurrentMediaTime()
        let frequency: Double = 2.0  // Steps per second
        let phase = sin(timestamp * .pi * frequency)
        
        playerLegs[0].eulerAngles.x = legSwingAngle * Float(phase)
        playerLegs[1].eulerAngles.x = -legSwingAngle * Float(phase)
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
        isMovingLeft = true
        isMovingRight = false
    }
    
    func moveRight() {
        guard gameMode != .menu && gameMode != .gameOver else { return }
        isMovingRight = true
        isMovingLeft = false
    }
    
    func stopMoving() {
        isMovingLeft = false
        isMovingRight = false
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
