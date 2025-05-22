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
    private let limbThickness: Float = 0.1
    
    // Game State
    @Published private(set) var startAngle: Float = .pi / 4
    @Published private(set) var startSpeed: Float = 10.0
    private var isStuck = false
    private var lastUpdateTime: TimeInterval = 0
    
    // Player State
    private var playerVelocity = SCNVector3(x: 0, y: 0, z: 0)
    private var stoolLength: Float = PhysicsParams.stoolLength
    private var stoolLengthVelocity: Float = 0
    private var stoolTilt: Float = 0
    private var stoolTiltVelocity: Float = 0
    
    // Movement State
    private var isMovingLeft = false
    private var isMovingRight = false
    private var isJumping = false
    private var isExtendingStool = false
    private var isTiltingLeft = false
    private var isTiltingRight = false
    private let moveSpeed: Float = 3.0  // Units per second
    
    // Forces
    private var horizontalForce: Float = 0
    private var verticalForce: Float = 0
    private var stoolExtendForce: Float = 0
    private var stoolTiltTorque: Float = 0
    
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
        let bodyGeometry = SCNCylinder(radius: CGFloat(limbThickness), height: CGFloat(PhysicsParams.playerHeight) * 0.4)
        let bodyMaterial = SCNMaterial()
        bodyMaterial.diffuse.contents = UIColor.systemBlue
        bodyGeometry.materials = [bodyMaterial]
        playerBody = SCNNode(geometry: bodyGeometry)
        playerBody.position = SCNVector3(x: 0, y: PhysicsParams.playerHeight * 0.5, z: 0)
        
        // Head
        let headGeometry = SCNSphere(radius: CGFloat(limbThickness) * 2)
        headGeometry.materials = [bodyMaterial]
        playerHead = SCNNode(geometry: headGeometry)
        playerHead.position = SCNVector3(x: 0, y: PhysicsParams.playerHeight * 0.7, z: 0)
        
        // Arms
        playerArms = []
        let armLength: Float = 0.6
        for i in 0...1 {
            let armGeometry = SCNCylinder(radius: CGFloat(limbThickness) * 0.8, height: CGFloat(armLength))
            let arm = SCNNode(geometry: armGeometry)
            arm.position = SCNVector3(x: (i == 0 ? -1 : 1) * limbThickness * 3, 
                                    y: PhysicsParams.playerHeight * 0.6,
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
                                    y: PhysicsParams.playerHeight * 0.3,
                                    z: 0)
            playerLegs.append(leg)
        }
        
        // Create Stool with rungs
        stool = SCNNode()
        stool.position = SCNVector3(x: playerStartX, y: PhysicsParams.playerHeight * 0.9, z: 0)
        
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
        scene.physicsWorld.gravity = SCNVector3(x: 0, y: -PhysicsParams.gravity, z: 0)
        
        // Ground physics
        ground.physicsBody = SCNPhysicsBody(type: .static, shape: nil)
        ground.physicsBody?.restitution = CGFloat(PhysicsParams.corGround.1)
        ground.physicsBody?.friction = 0.5
        
        // Ball physics
        let ballShape = SCNPhysicsShape(geometry: ballGeometry, options: nil)
        ball.physicsBody = SCNPhysicsBody(type: .dynamic, shape: ballShape)
        ball.physicsBody?.mass = 1.0
        ball.physicsBody?.restitution = CGFloat(PhysicsParams.corStool.1)
        ball.physicsBody?.angularDamping = 0.5
        ball.physicsBody?.friction = 0.3
        
        // Player physics - using kinematic body to manually control physics
        let playerShape = SCNPhysicsShape(node: player, options: [.keepAsCompound: true])
        player.physicsBody = SCNPhysicsBody(type: .kinematic, shape: playerShape)
        
        // Stool physics
        let stoolShape = SCNPhysicsShape(node: stool, options: [.keepAsCompound: true])
        stool.physicsBody = SCNPhysicsBody(type: .kinematic, shape: stoolShape)
        stool.physicsBody?.restitution = CGFloat(PhysicsParams.corStool.1)
        
        // Set up collision detection
        ball.physicsBody?.categoryBitMask = 1
        stool.physicsBody?.categoryBitMask = 2
        ground.physicsBody?.categoryBitMask = 4
        player.physicsBody?.categoryBitMask = 8
        
        ball.physicsBody?.collisionBitMask = 2 | 4 | 8
        stool.physicsBody?.collisionBitMask = 1
        ground.physicsBody?.collisionBitMask = 1
        player.physicsBody?.collisionBitMask = 1
        
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
        
        let currentTime = CACurrentMediaTime()
        let dt = Float(currentTime - lastUpdateTime)
        lastUpdateTime = currentTime
        
        // Calculate forces based on controls
        updateForces()
        
        // Update player position and velocity using physics equations
        let playerPos = player.position
        let stoolPos = stool.position
        
        // Horizontal motion with damping
        let horizontalAccel = (horizontalForce - PhysicsParams.horizDamping * playerVelocity.x) / PhysicsParams.totalMass
        playerVelocity.x += horizontalAccel * dt
        playerVelocity.x = clamp(playerVelocity.x, min: PhysicsParams.horizSpeedLimit.0, max: PhysicsParams.horizSpeedLimit.1)
        
        // Vertical motion with spring force and damping
        let verticalSpringForce = -PhysicsParams.legStiffness * (playerPos.y - PhysicsParams.startY)
        let verticalDampingForce = -PhysicsParams.vertDamping * playerVelocity.y
        let verticalAccel = (verticalForce + verticalSpringForce + verticalDampingForce) / PhysicsParams.totalMass - PhysicsParams.gravity
        playerVelocity.y += verticalAccel * dt
        playerVelocity.y = clamp(playerVelocity.y, min: PhysicsParams.vertSpeedLimit.0, max: PhysicsParams.vertSpeedLimit.1)
        
        // Stool extension with spring force and damping
        let stoolSpringForce = -PhysicsParams.armStiffness * (stoolLength - PhysicsParams.stoolLength)
        let stoolDampingForce = -PhysicsParams.armDamping * stoolLengthVelocity
        let stoolExtendAccel = (stoolExtendForce + stoolSpringForce + stoolDampingForce) / PhysicsParams.stoolMass
        stoolLengthVelocity += stoolExtendAccel * dt
        stoolLengthVelocity = clamp(stoolLengthVelocity, min: PhysicsParams.stoolExtendSpeedLimit.0, max: PhysicsParams.stoolExtendSpeedLimit.1)
        
        // Stool tilt with spring torque and damping
        let tiltSpringTorque = -PhysicsParams.tiltStiffness * stoolTilt
        let tiltDampingTorque = -PhysicsParams.tiltDamping * stoolTiltVelocity
        let tiltAccel = (stoolTiltTorque + tiltSpringTorque + tiltDampingTorque) / (PhysicsParams.stoolMass * pow(stoolLength, 2))
        stoolTiltVelocity += tiltAccel * dt
        stoolTiltVelocity = clamp(stoolTiltVelocity, min: PhysicsParams.stoolTiltSpeedLimit.0, max: PhysicsParams.stoolTiltSpeedLimit.1)
        
        // Update positions
        let newX = playerPos.x + playerVelocity.x * dt
        let newY = clamp(playerPos.y + playerVelocity.y * dt, min: PhysicsParams.vertPosLimit.0, max: PhysicsParams.vertPosLimit.1)
        player.position = SCNVector3(x: newX, y: newY, z: playerPos.z)
        
        stoolLength = clamp(stoolLength + stoolLengthVelocity * dt, min: PhysicsParams.stoolLengthLimit.0, max: PhysicsParams.stoolLengthLimit.1)
        stoolTilt = clamp(stoolTilt + stoolTiltVelocity * dt, min: PhysicsParams.stoolTiltLimit.0, max: PhysicsParams.stoolTiltLimit.1)
        
        // Update stool position and rotation
        stool.position = SCNVector3(x: newX, y: newY + PhysicsParams.playerHeight * 0.9, z: stoolPos.z)
        stool.eulerAngles.z = stoolTilt
        
        // Update leg animation based on movement
        updateLegAnimation(dt: dt)
    }
    
    private func updateForces() {
        // Reset forces
        horizontalForce = 0
        verticalForce = 0
        stoolExtendForce = 0
        stoolTiltTorque = 0
        
        // Apply horizontal force based on movement
        if isMovingLeft {
            horizontalForce = -PhysicsParams.maxHorizForce
        } else if isMovingRight {
            horizontalForce = PhysicsParams.maxHorizForce
        }
        
        // Apply vertical force for jumping
        if isJumping {
            verticalForce = PhysicsParams.legStrength
        }
        
        // Apply stool extension force
        if isExtendingStool {
            stoolExtendForce = PhysicsParams.armStrength
        }
        
        // Apply stool tilt torque
        if isTiltingLeft {
            stoolTiltTorque = -PhysicsParams.tiltStrength
        } else if isTiltingRight {
            stoolTiltTorque = PhysicsParams.tiltStrength
        }
    }
    
    private func updateLegAnimation(dt: Float) {
        guard abs(playerVelocity.x) > 0.1 else {
            // Reset legs to neutral position when not moving
            playerLegs.enumerated().forEach { i, leg in
                leg.position.x = (i == 0 ? -1 : 1) * limbThickness * 2
                leg.eulerAngles.z = 0
            }
            return
        }
        
        // Animate legs based on movement
        let cycleTime = 1.0 / PhysicsParams.footStepRate
        let t = Float(CACurrentMediaTime()).truncatingRemainder(dividingBy: Float(cycleTime))
        let phase = t / Float(cycleTime) * 2 * .pi
        
        playerLegs.enumerated().forEach { i, leg in
            let offset = i == 0 ? 0 : .pi  // Legs move opposite to each other
            let angle = sin(Double(phase) + offset) * 0.5  // Max angle of leg swing
            leg.eulerAngles.z = Float(angle)
            
            // Move leg position slightly to simulate stepping
            let baseX = (i == 0 ? -1 : 1) * limbThickness * 2
            let stepOffset = cos(phase + Float(offset)) * PhysicsParams.footStepLength * 0.1
            leg.position.x = baseX + stepOffset
        }
    }
    
    private func clamp<T: Comparable>(_ value: T, min: T, max: T) -> T {
        return Swift.min(Swift.max(value, min), max)
    }
    
    // MARK: - Game Control Methods
    func startGame() {
        score = 0
        gameMode = .angleSelect
        resetPositions()
    }
    
    func resetPositions() {
        // Reset player and stool positions
        player.position = SCNVector3(x: playerStartX, y: playerStartY, z: 0)
        stool.position = SCNVector3(x: playerStartX, y: playerStartY + PhysicsParams.playerHeight * 0.9, z: 0)
        ball.position = SCNVector3(x: 0, y: ballRadius, z: 0)
        
        // Reset velocities and forces
        playerVelocity = SCNVector3Zero
        stoolLength = PhysicsParams.stoolLength
        stoolLengthVelocity = 0
        stoolTilt = 0
        stoolTiltVelocity = 0
        
        // Reset ball physics
        ball.physicsBody?.velocity = SCNVector3Zero
        ball.physicsBody?.angularVelocity = SCNVector4Zero
        
        isStuck = false
    }
    
    func setAngle() {
        gameMode = .speedSelect
    }
    
    func setSpeed() {
        gameMode = .playing
        
        // Apply initial velocity to the ball
        let vx = startSpeed * cos(startAngle)
        let vy = startSpeed * sin(startAngle)
        ball.physicsBody?.velocity = SCNVector3(x: vx, y: vy, z: 0)
    }
    
    func increaseAngle() {
        startAngle = min(startAngle + 0.1, .pi / 2)
    }
    
    func decreaseAngle() {
        startAngle = max(startAngle - 0.1, 0)
    }
    
    func increaseSpeed() {
        startSpeed = min(startSpeed + 0.5, 20.0)  // Maximum speed of 20 m/s
    }
    
    func decreaseSpeed() {
        startSpeed = max(startSpeed - 0.5, 5.0)  // Minimum speed of 5 m/s
    }
    
    // MARK: - Control Methods
    func startMovingLeft() {
        isMovingLeft = true
        isMovingRight = false
    }
    
    func startMovingRight() {
        isMovingRight = true
        isMovingLeft = false
    }
    
    func stopMoving() {
        isMovingLeft = false
        isMovingRight = false
    }
    
    func startJumping() {
        isJumping = true
    }
    
    func stopJumping() {
        isJumping = false
    }
    
    func startExtendingStool() {
        isExtendingStool = true
    }
    
    func stopExtendingStool() {
        isExtendingStool = false
    }
    
    func startTiltingLeft() {
        isTiltingLeft = true
        isTiltingRight = false
    }
    
    func startTiltingRight() {
        isTiltingRight = true
        isTiltingLeft = false
    }
    
    func stopTilting() {
        isTiltingLeft = false
        isTiltingRight = false
    }
}

// MARK: - Physics Contact Delegate
extension GameManager: SCNPhysicsContactDelegate {
    func physicsWorld(_ world: SCNPhysicsWorld, didBegin contact: SCNPhysicsContact) {
        let nodeA = contact.nodeA
        let nodeB = contact.nodeB
        
        // Ball-Stool collision
        if (nodeA == ball && nodeB == stool) || (nodeA == stool && nodeB == ball) {
            handleBallStoolCollision(contact: contact)
        }
        
        // Ball-Ground collision
        if (nodeA == ball && nodeB == ground) || (nodeA == ground && nodeB == ball) {
            handleBallGroundCollision(contact: contact)
        }
    }
    
    private func handleBallStoolCollision(contact: SCNPhysicsContact) {
        guard !isStuck else { return }
        
        let ball = contact.nodeA == self.ball ? contact.nodeA : contact.nodeB
        let stool = contact.nodeA == self.stool ? contact.nodeA : contact.nodeB
        
        // Get velocities
        let ballVelocity = ball.physicsBody?.velocity ?? SCNVector3Zero
        let stoolVelocity = SCNVector3(x: playerVelocity.x, y: playerVelocity.y, z: 0)
        
        // Calculate relative velocity
        let relativeVelocity = SCNVector3(
            x: ballVelocity.x - stoolVelocity.x,
            y: ballVelocity.y - stoolVelocity.y,
            z: ballVelocity.z - stoolVelocity.z
        )
        
        // Calculate normal vector at contact point
        let contactNormal = contact.contactNormal
        
        // Calculate reflection vector with coefficient of restitution
        let cor = PhysicsParams.corStool
        let dotProduct = dot(relativeVelocity, contactNormal)
        let reflectionVelocity = SCNVector3(
            x: relativeVelocity.x - (1 + cor.0) * contactNormal.x * dotProduct,
            y: relativeVelocity.y - (1 + cor.1) * contactNormal.y * dotProduct,
            z: relativeVelocity.z - (1 + cor.0) * contactNormal.z * dotProduct
        )
        
        // Add back stool velocity to get final ball velocity
        let finalVelocity = SCNVector3(
            x: reflectionVelocity.x + stoolVelocity.x,
            y: reflectionVelocity.y + stoolVelocity.y,
            z: reflectionVelocity.z + stoolVelocity.z
        )
        
        // Apply the new velocity to the ball
        ball.physicsBody?.velocity = finalVelocity
        
        // Apply recoil to player and stool
        let recoilForce = Float(0.1)  // Adjust this value for desired recoil effect
        playerVelocity.x += -contactNormal.x * recoilForce
        playerVelocity.y += -contactNormal.y * recoilForce
        stoolTiltVelocity += Float(dot(SCNVector3(x: -contactNormal.z, y: contactNormal.x, z: 0), 
                                     SCNVector3(x: 1, y: 0, z: 0))) * recoilForce
        
        // Increment score
        score += 1
    }
    
    private func handleBallGroundCollision(contact: SCNPhysicsContact) {
        let ball = contact.nodeA == self.ball ? contact.nodeA : contact.nodeB
        let ballVelocity = ball.physicsBody?.velocity ?? SCNVector3Zero
        
        // Apply ground coefficient of restitution
        let cor = PhysicsParams.corGround
        ball.physicsBody?.velocity = SCNVector3(
            x: ballVelocity.x * cor.0,
            y: -ballVelocity.y * cor.1,
            z: ballVelocity.z * cor.0
        )
        
        // Check for game over
        if abs(ballVelocity.y) < PhysicsParams.dybtol {
            isStuck = true
            gameMode = .gameOver
        }
    }
    
    private func dot(_ a: SCNVector3, _ b: SCNVector3) -> Float {
        return a.x * b.x + a.y * b.y + a.z * b.z
    }
}
