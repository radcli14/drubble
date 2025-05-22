//
//  ContentView.swift
//  drubble
//
//  Created by Eliott Radcliffe on 5/22/25.
//

import SwiftUI
import SceneKit

struct ContentView: View {
    @StateObject private var gameManager = GameManager()
    
    var body: some View {
        ZStack {
            // 3D Game Scene
            SceneView(
                scene: gameManager.scene,
                pointOfView: gameManager.camera,
                options: [.allowsCameraControl]
            )
            .ignoresSafeArea()
            
            // Game UI Overlay
            VStack {
                // Score and status display
                HStack {
                    Text("Score: \(gameManager.score)")
                        .font(.headline)
                    Spacer()
                    Text(gameManager.gameMode.rawValue)
                        .font(.headline)
                }
                .padding()
                .background(.ultraThinMaterial)
                
                Spacer()
                
                // Game controls based on game mode
                switch gameManager.gameMode {
                case .menu:
                    Button("Start Game") {
                        gameManager.startGame()
                    }
                    .font(.title)
                    .padding()
                    .background(.blue)
                    .foregroundColor(.white)
                    .clipShape(Capsule())
                    
                case .angleSelect:
                    VStack {
                        Text("Set Launch Angle")
                            .font(.headline)
                        Text(String(format: "%.1f°", gameManager.startAngle * 180 / .pi))
                            .font(.title)
                        HStack {
                            Button("←") {
                                gameManager.decreaseAngle()
                            }
                            .padding()
                            Button("Set") {
                                gameManager.setAngle()
                            }
                            .padding()
                            Button("→") {
                                gameManager.increaseAngle()
                            }
                            .padding()
                        }
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                    
                case .speedSelect:
                    VStack {
                        Text("Set Launch Speed")
                            .font(.headline)
                        Text(String(format: "%.1f m/s", gameManager.startSpeed))
                            .font(.title)
                        HStack {
                            Button("←") {
                                gameManager.decreaseSpeed()
                            }
                            .padding()
                            Button("Launch") {
                                gameManager.setSpeed()
                            }
                            .padding()
                            Button("→") {
                                gameManager.increaseSpeed()
                            }
                            .padding()
                        }
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                    
                case .playing:
                    HStack {
                        // Movement controls
                        VStack {
                            Button("Jump") { }
                                .padding()
                                .simultaneousGesture(
                                    DragGesture(minimumDistance: 0)
                                        .onChanged { _ in
                                            gameManager.startJumping()
                                        }
                                        .onEnded { _ in
                                            gameManager.stopJumping()
                                        }
                                )
                            HStack {
                                Button("←") { }
                                    .padding()
                                    .simultaneousGesture(
                                        DragGesture(minimumDistance: 0)
                                            .onChanged { _ in
                                                gameManager.startMovingLeft()
                                            }
                                            .onEnded { _ in
                                                gameManager.stopMoving()
                                            }
                                    )
                                Button("→") { }
                                    .padding()
                                    .simultaneousGesture(
                                        DragGesture(minimumDistance: 0)
                                            .onChanged { _ in
                                                gameManager.startMovingRight()
                                            }
                                            .onEnded { _ in
                                                gameManager.stopMoving()
                                            }
                                    )
                            }
                        }
                        .padding()
                        
                        Spacer()
                        
                        // Stool controls
                        VStack {
                            Button("Extend") { }
                                .padding()
                                .simultaneousGesture(
                                    DragGesture(minimumDistance: 0)
                                        .onChanged { _ in
                                            gameManager.startExtendingStool()
                                        }
                                        .onEnded { _ in
                                            gameManager.stopExtendingStool()
                                        }
                                )
                            HStack {
                                Button("←") { }
                                    .padding()
                                    .simultaneousGesture(
                                        DragGesture(minimumDistance: 0)
                                            .onChanged { _ in
                                                gameManager.startTiltingLeft()
                                            }
                                            .onEnded { _ in
                                                gameManager.stopTilting()
                                            }
                                    )
                                Button("→") { }
                                    .padding()
                                    .simultaneousGesture(
                                        DragGesture(minimumDistance: 0)
                                            .onChanged { _ in
                                                gameManager.startTiltingRight()
                                            }
                                            .onEnded { _ in
                                                gameManager.stopTilting()
                                            }
                                    )
                            }
                        }
                        .padding()
                    }
                    .background(.ultraThinMaterial)
                    
                case .gameOver:
                    VStack {
                        Text("Game Over!")
                            .font(.title)
                        Text("Final Score: \(gameManager.score)")
                            .font(.headline)
                        Button("Play Again") {
                            gameManager.startGame()
                        }
                        .padding()
                        .background(.blue)
                        .foregroundColor(.white)
                        .clipShape(Capsule())
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                }
            }
            .padding()
        }
    }
}

#Preview {
    ContentView()
}
