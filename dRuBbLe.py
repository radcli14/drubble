# Execute drubbleFunc to get the supporting functions and classes
exec(open('./drubbleFunc.py').read())

# Obtain Parameters
p = parameters()

# Initial states
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.rb,0,0,p.x0,p.y0,p.l0,0,0,0,0,10,
                 0   ,p.y0,p.l0,0,0,0,0,-10]
nPlayer = 2
gs = gameState(u0)

# Set the keyboard input and mouse defaults
keyPush        = np.zeros(8)
userControlled = np.array([[True, True, True, True ],
                           [False,False,False,False]]) 

# Initialize stats
stats = gameScore()

# Initialize drums
drums = drumBeat()

# Run an infinite loop until gs.gameMode is zero
if engine == 'pygame':
    clock = pygame.time.Clock()
    while gs.gameMode>0:
        ## USER INPUT
        for event in pygame.event.get():
            # Detect the quit event (window close)
            if event.type == pygame.QUIT: 
                gs.gameMode = 0
            
            # Detect keyboard input
            if event.type == pygame.KEYDOWN:
                # Exit the game
                if event.key == pygame.K_ESCAPE:
                    gs.gameMode = 0
                
                # Exit the splash screen
                if gs.gameMode==1 and event.key == pygame.K_SPACE:
                    gs.gameMode = 2
                    clock.tick(10)
                    continue
                
                if gs.gameMode==2 and event.key == pygame.K_SPACE:
                    gs.gameMode = 3
                    clock.tick(10)
                    continue
                
                # Progress through angle and speed selection
                if (gs.gameMode==3 or gs.gameMode==4) and event.key == pygame.K_SPACE:
                    gs.gameMode += 1
                    gs.phase = 0
                    clock.tick(10)
                    continue
                
                # Start the ball moving!
                if gs.gameMode == 5 and event.key == pygame.K_SPACE:
                    gs.gameMode = 6
                    clock.tick(10)
                    continue
                
                # Reset the game
                if gs.gameMode == 6 and event.key == pygame.K_SPACE:
                    stats = gameScore()
                    gs = gameState(u0)
                    gs.gameMode = 2
    
            # Get player control inputs
            keyPush = playerControlInput(event)             
    
        # Show the Splash Sreen
        if gs.gameMode==1:
            makeSplashScreen()
        
        ## ANGLE AND SPEED SETTINGS
        if gs.gameMode>2 and gs.gameMode<6:
            gs.setAngleSpeed()
        
        if gs.gameMode>1 and gs.gameMode<7:
            # Create the sky
            screen.fill(skyBlue)

            ## SIMULATION
            gs.simStep()
            
            # Update statistics
            if gs.gameMode==6:
                stats.update()
     
            ## ANIMATION
            # Get the ranges in meters using the setRanges function
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
            # Draw the background
            makeBackgroundImage()
            
            # Draw the ball and player
            makeGameImage()
            
            # Draw the score line
            makeScoreLine()
            
            # Draw meter markers
            makeMarkers(xrng,m2p,po)
    
            # Show the Message Text
            showMessage(msg[gs.gameMode])  
            
        #if gs.gameMode==6:    
            # Play the drums
            #drums.play()
    
        # Update the display
        pygame.display.flip()
        
        # Timing Variables
        if p.timeRun and gs.n>0:
            thisStepTime = clock.tick()
            stats.averageStepTime = (stats.averageStepTime*(gs.n-1) + thisStepTime)/gs.n
        clock.tick(fs)
    
    # Exit the game   
    pygame.quit()
        
if engine == 'ista':
    gs.gameMode = 3

    # Initialize the background image
    try:
        bg0 = scene_drawing.load_image_file('figs/bg0.png')
        bg0_sz = (6*height,height)
        bgLoaded = True
    except:
        bgLoaded = False
    
    class Game (Scene):
        def setup(self):
            # Initialize the motion module
            motion.start_updates()
        	
            # Add the game state classes to the scene
            self.touchCycle = False
            
            # Initialize the buttons or sticks
            self.moveStick,self.moveAura = initStick(self,0.1,0.2*width,(1,0),(width,height/20))
            self.tiltStick,self.tiltAura = initStick(self,0.1,0.2*width,(0,0),(0,height/20))
            
            # Generate the sky blue background
            self.background_color = '#acf9ee'
            
            # Initialize the score line
            score_font = ('Futura', 12)
            self.time_label = LabelNode('Time = '+f'{gs.t:.1f}', score_font, parent=self,color=black)
            self.time_label.anchor_point = (0.0, 1.0)
            self.time_label.position = (width*0.02, height - 2)
            self.time_label.z_position = 1
            
            self.dist_label = LabelNode('Distance = '+f'{stats.stoolDist:.1f}', score_font, parent=self,color=black)
            self.dist_label.anchor_point = (0.0, 1.0)
            self.dist_label.position = (width*0.2, height - 2)
            self.dist_label.z_position = 1
            
            self.high_label = LabelNode('Height = '+f'{stats.maxHeight:.1f}', score_font, parent=self,color=black)
            self.high_label.anchor_point = (0.0, 1.0)
            self.high_label.position = (width*0.42, height - 2)
            self.high_label.z_position = 1
            
            self.boing_label = LabelNode('Boing! = '+str(int(stats.stoolCount)), score_font, parent=self,color=black)
            self.boing_label.anchor_point = (0.0, 1.0)
            self.boing_label.position = (width*0.62, height - 2)
            self.boing_label.z_position = 1
            
            self.score_label = LabelNode('Score = '+str(stats.score), score_font, parent=self,color=black)
            self.score_label.anchor_point = (0.0, 1.0)
            self.score_label.position = (width*0.77, height - 2)
            self.score_label.z_position = 1
            
            # Get ranges for drawing the player and ball
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
            # Initialize the ball image
            self.ball = SpriteNode('emj:Red_Circle')
            dbPix = 2*p.rb*m2p
            self.ball.size = (dbPix,dbPix)
            self.ball.anchor_point = (0.5, 0.5)
            self.ball.position = (gs.xb*m2p+po, (gs.yb+p.rb)*m2p)
            self.add_child(self.ball)
            
            # Initialize the player's head
            self.head = SpriteNode('emj:Slice_Of_Pizza')
            spPix = 0.7*m2p
            self.head.size = (spPix,spPix)
            self.head.anchor_point = (0.5, 0.0)
            self.head.position = (gs.xp[0]*m2p+po, (gs.yp[0]+p.d)*m2p)
            self.add_child(self.head)
            
            if nPlayer>0:
                self.head1 = SpriteNode('emj:Corn')
                self.head1.size = (spPix,spPix)
                self.head1.anchor_point = (0.5, 0.0)
                self.head.position = (gs.xp[1]*m2p+po, (gs.yp[1]+p.d)*m2p)
                self.add_child(self.head1)
        
        def update(self):
            # Update if there was a touch
            if self.touchCycle:
                cycleModes(gs,stats)
                self.touchCycle = False
                
            # Get the gravity vector and acceleration
            if gs.ctrlMode == 'motion':
                g = motion.get_gravity()
                gThreshold = 0.05
                slope = 5
                if g[1]>gThreshold:
                    keyPush[0] = min(slope*(g[1]-gThreshold),1)
                elif g[1]<-gThreshold:
                    keyPush[1] = -max(slope*(g[1]+gThreshold),-1)
                else:
                    keyPush[0] = 0
                    keyPush[1] = 0
                
                a = motion.get_user_acceleration()
                aScale=2
                if a[1]>0:
                    keyPush[2] = max(aScale*a[1],1)
                    keyPush[3] = 0
                else:
                    keyPush[2] = 0
                    keyPush[3]=max(-aScale*a[1],1)
            elif gs.ctrlMode == 'vStick':
                keyPush[1] = self.moveStick.ctrl[0]
                keyPush[2] = self.moveStick.ctrl[1]
                keyPush[4] = self.tiltStick.ctrl[1]
                keyPush[7] = self.tiltStick.ctrl[0]
                
            ## ANGLE AND SPEED SETTINGS
            if gs.gameMode>2 and gs.gameMode<6:
                gs.setAngleSpeed()
            
            # Run one simulation step
            gs.simStep()
            if gs.gameMode==6:
                stats.update()
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
            # Update score line
            self.time_label.text  = 'Time = '+f'{gs.t:.1f}'
            self.dist_label.text  = 'Distance = '+f'{stats.stoolDist:.2f}'
            self.high_label.text  = 'Height = '+f'{stats.maxHeight:.2f}'
            self.boing_label.text = 'Boing! = '+str(int(stats.stoolCount))
            self.score_label.text = 'Score = '+str(stats.score)
            
            # update the ball sprites
            dbPix = 2*p.rb*m2p
            self.ball.size = (dbPix,dbPix)
            x,y = xy2p(gs.xb,gs.yb,m2p,po,width,height)
            self.ball.position = (x,y)
            
            # Generate the head sprites
            spPix = 0.7*m2p
            self.head.size = (spPix,spPix)
            x,y = xy2p(gs.xp[0],gs.yp[0]+p.d,m2p,po,width,height)
            self.head.position = (x,y)
            
            if nPlayer>0:
                self.head1.size = (spPix,spPix)
                x,y = xy2p(gs.xp[1],gs.yp[1]+p.d,m2p,po,width,height)
                self.head1.position = (x,y)
                                 
        def draw(self):
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
            # Generate the background
            if bgLoaded:
                drawBackgroundImage(bg0,bg0_sz,-0.25,-10,m2p)
                
            
            # Generate the trajectory
            linePlot(gs.xTraj,gs.yTraj,m2p,po,width,height,white,2)
            
            # Generate the bottom line
            stroke(black)
            stroke_weight(height/20)
            line(0,height/40,width,height/40)
            
            # Generate the markers
            makeMarkers(xrng,m2p,po)
            
            for k in range(nPlayer):
                # Generate a player image
                xv,yv,sx,sy = stickDude(gs,k)
                linePlot(xv,yv,m2p,po,width,height,p.playerColor[k],0.15*m2p)
            
                # Generate a stool image
                linePlot(sx,sy,m2p,po,width,height,p.stoolColor[k],0.1*m2p)
                        
        def touch_began(self, touch):
            # Reset if necessary
            if touch.location[1] > height/2:
                self.touchCycle = True
            
            # Detect control inputs
            xy = touchStick(touch.location,self.moveStick)
            if xy[0] != 0:
            	self.moveStick.ctrl = xy
            	self.moveStick.id = touch.touch_id
            	
            xy = touchStick(touch.location,self.tiltStick)
            if xy[0] != 0:
            	self.tiltStick.ctrl = xy
            	self.tiltStick.id = touch.touch_id	
        
        def touch_moved(self,touch):
            # Detect control inputs
            xy = touchStick(touch.location,self.moveStick)
            if touch.touch_id == self.moveStick.id and xy[0] != 0:
                self.moveStick.ctrl = xy
            
            xy = touchStick(touch.location,self.tiltStick)
            if touch.touch_id == self.tiltStick.id and xy[0] != 0:
                self.tiltStick.ctrl = xy
        
        def touch_ended(self,touch):
            if touch.touch_id == self.moveStick.id:
                self.moveStick.ctrl = (0,0)
        
            if touch.touch_id == self.tiltStick.id:
                self.tiltStick.ctrl = (0,0)
        
        def stop(self):
            motion.stop_updates()
                
    if __name__ == '__main__':
        run(Game(), LANDSCAPE, show_fps=True)
        
        
        
        
