# Execute drubbleFunc to get the supporting functions and classes
exec(open('./drubbleFunc.py').read())

# Set the keyboard input and mouse defaults
keyPush = np.zeros(8)

# Initialize stats
stats = GameScore()

# Initialize drums
drums = DrumBeat()

class MyBackground:
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        # Randomize the start location in the background
        self.xpos = np.random.rand()*200.0
        # Set size of the background, before updates
        self.sz_orig = self.w_orig,self.h_orig = (2400.0,400.0)
        
        # Add widgets to the canvas
        self.bg = []
        self.num_bg = 2  # Number of background images

        # Import the background images
        for n in range(self.num_bg):
            name = 'figs/bg'+str(n)+'.png'
            self.bg.append(scene_drawing.load_image_file(name))

    def update(self, x, y, w, h, m2p): 
        # xmod is normalized position of the player between 0 and num_bg
        xmod = np.mod(x+self.xpos,200)/100.0
        
        # scf is the scale factor to apply to the background
        scf = (m2p/70.0)**0.5

        # Position in the Background
        posInBG = w/2.0-xmod*scf*self.w_orig
        newWidth = self.w_orig*scf
        newHeight = self.h_orig*scf

        lowerBound = int(h/20.0-5)
        #self.ground.size = (w, lowerBound+h/6.0*scf)
        if xmod>=0 and xmod<0.5:
            scene_drawing.image(self.bg[0],posInBG,lowerBound,newWidth,newHeight)
            scene_drawing.image(self.bg[1],posInBG-newWidth,lowerBound,newWidth,newHeight)
        elif xmod>=0.5 and xmod<1.5:
            scene_drawing.image(self.bg[0],posInBG,lowerBound,newWidth,newHeight)
            scene_drawing.image(self.bg[1],posInBG+newWidth,lowerBound,newWidth,newHeight)
        elif xmod>=1.5 and xmod<=2.0:
            scene_drawing.image(self.bg[0],posInBG+self.num_bg*newWidth,lowerBound,newWidth,newHeight)
            scene_drawing.image(self.bg[1],posInBG+newWidth,lowerBound,newWidth,newHeight)
        
# Create OptionButtons class
class OptionButtons:
    def __init__(self,*args,**kwargs):
        self.butt = LabelNode(*args,**kwargs)
        self.left = self.butt.position[0]-self.butt.size[0]*self.butt.anchor_point[0]
        self.right = self.butt.position[0]+self.butt.size[0]*(1-self.butt.anchor_point[0])
        self.bottom = self.butt.position[1]-self.butt.size[1]*self.butt.anchor_point[1]
        self.top = self.butt.position[1]+self.butt.size[1]*(1-self.butt.anchor_point[1])
        
    def text(self,str):
        self.butt.text = str
        self.left = self.butt.position[0]-self.butt.size[0]*self.butt.anchor_point[0]
        self.right = self.butt.position[0]+self.butt.size[0]*(1-self.butt.anchor_point[0])
        self.bottom = self.butt.position[1]-self.butt.size[1]*self.butt.anchor_point[1]
        self.top = self.butt.position[1]+self.butt.size[1]*(1-self.butt.anchor_point[1])
        
    def detect_touch(self,loc):
        tCnd = [loc[0] > self.left,
                loc[0] < self.right,
                loc[1] > self.bottom,
                loc[1] < self.top]
        return all(tCnd)
        
    def rm(self):
        self.butt.remove_from_parent()

if engine == 'ista':
    # Initialize the splash screen
    splash = scene_drawing.load_image_file('figs/splash.png')
    
    class Game (Scene):
        def setup(self):
            # Initialize the motion module
            motion.start_updates()
        	
            # Add the game state classes to the scene
            self.touchCycle = False
            
            # Initialize the counter for the splash screen
            self.kSplash = 0
            
            # Generate the sky blue background and images
            self.background_color = skyBlue
            self.bg = MyBackground()
            
            # Initialize the buttons or sticks
            self.moveStick,self.moveAura = initStick(self,0.1,0.2*width,(1,0),(width,height/20))
            self.tiltStick,self.tiltAura = initStick(self,0.1,0.2*width,(0,0),(0,height/20))
            self.add_child(self.moveAura)
            self.add_child(self.tiltAura)
            
            # Initialize the score line
            score_font = (p.MacsFavoriteFont, 12)
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
            
            # Initialize the player's head
            self.head = SpriteNode('figs/myFace.png')
            spPix = 0.7*m2p
            self.head.size = (spPix,spPix)
            self.head.anchor_point = (0.5, 0.0)
            self.head.position = (gs.xp[0]*m2p+po, (gs.yp[0]+p.d)*m2p)
            
            self.head1 = SpriteNode('emj:Corn')
            self.head1.size = (spPix,spPix)
            self.head1.anchor_point = (0.5, 0.0)
            self.head.position = (gs.xp[1]*m2p+po, (gs.yp[1]+p.d)*m2p)
            
            self.actionButt = OptionButtons(text='Begin',font=(p.MacsFavoriteFont,24),position=(0.95*width,0.95*height),anchor_point=(1,1))
            
            self.optionButt = OptionButtons(text='Options',font=(p.MacsFavoriteFont,24),position=(0.05*width,0.95*height),anchor_point=(0,1))
            
            toggleVisibleSprites(self,False)
            
        def update(self):
            # Update if there was a touch
            if self.touchCycle:
                cycleModes(gs,stats)
                if gs.gameMode == 2:
                    self.singleButt = OptionButtons(text='Single Drubble',font=(p.MacsFavoriteFont,36),size=(0.8*width,0.2*height),position=(0.5*width,0.75*height))
                    self.doubleButt = OptionButtons(text='Double Drubble',font=(p.MacsFavoriteFont,36),size=(0.8*width,0.2*height),position=(0.5*width,0.5*height))
                    self.add_child(self.singleButt.butt)
                    self.add_child(self.doubleButt.butt)
                    
                if gs.gameMode == 3:
                    toggleVisibleSprites(self,True)
                    self.add_child(self.actionButt.butt)
                    self.add_child(self.optionButt.butt)
                    self.actionButt.text('Begin')
                    
                if gs.gameMode == 4:
                    self.actionButt.text('Set Angle')
                    
                if gs.gameMode == 5:
                    self.actionButt.text('Set Speed')
                    
                if gs.gameMode == 6:
                    self.actionButt.text('Restart')
                    
                self.touchCycle = False
                
            # Get control inputs
            if gs.ctrlMode == 'motion':
                gs.setControl(g=motion.get_gravity(),
                              a=motion.get_user_acceleration())    
            elif gs.ctrlMode == 'vStick' and gs.gameMode>1:
                gs.setControl(moveStick=self.moveStick.ctrl,
                              tiltStick=self.tiltStick.ctrl)
                
                # Move auras
                xy = self.moveStick.ctrl
                c = self.moveStick.cntr
                s = self.moveStick.size[0]/3
                self.moveAura.position = (c[0]+xy[0]*s,c[1]+xy[1]*s)
                xy = self.tiltStick.ctrl
                c = self.tiltStick.cntr
                self.tiltAura.position = (c[0]+xy[0]*s,c[1]+xy[1]*s)
                
            ## ANGLE AND SPEED SETTINGS
            if gs.gameMode>2 and gs.gameMode<6:
                gs.setAngleSpeed()
            
            # Run one simulation step
            gs.simStep()
            if gs.gameMode==6:
                stats.update()
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            if gs.StoolBounce:
                sound.play_effect('digital:PhaseJump3')
            if gs.FloorBounce and not gs.Stuck:
                sound.play_effect('game:Error')
                
            # Play the drum beat
            drums.play_ista()
            
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
            
            if p.nPlayer>1:
                self.head1.size = (spPix,spPix)
                x,y = xy2p(gs.xp[1],gs.yp[1]+p.d,m2p,po,width,height)
                self.head1.position = (x,y)
            
        def draw(self):
            # Show the splash screen
            if gs.gameMode == 1:
                makeSplashScreen(self)
                if not gs.showedSplash:
                    self.kSplash += 2
            else:
                xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
                # Generate the background
                if gs.gameMode>2:
                    # Update the background
                    xMean = (gs.xb+gs.xp[0])/2.0
                    self.bg.update(xMean,gs.yb,width,height,m2p)
            
                if gs.gameMode>2:
                    # Generate the bottom line
                    stroke(black)
                    stroke_weight(height/20)
                    line(0,height/40,width,height/40)
            
                    # Generate the markers
                    makeMarkers(xrng,m2p,po)
            
                    # Generate the trajectory
                    linePlot(gs.xTraj,gs.yTraj,m2p,po,width,height,white,2)
                    
                    for k in range(p.nPlayer):
                        # Generate a player image
                        xv,yv,sx,sy = stickDude(gs,k)
                        linePlot(xv,yv,m2p,po,width,height,p.playerColor[k],0.15*m2p)
            
                        # Generate a stool image
                        linePlot(sx,sy,m2p,po,width,height,p.stoolColor[k],0.1*m2p)
                        
        def touch_began(self, touch):
            # Reset if necessary
            if gs.gameMode == 1 and self.kSplash >= 255: 
                self.touchCycle = True
            
            if gs.gameMode == 2:
                b1 = self.singleButt.detect_touch(touch.location)
                b2 = self.doubleButt.detect_touch(touch.location)
                if b1 or b2:
                    self.touchCycle = True
                    p.nPlayer = b1 + 2*b2
                    self.singleButt.rm()
                    self.doubleButt.rm()
            
            if gs.gameMode > 2 and self.actionButt.detect_touch(touch.location):
                self.touchCycle = True
            
            if gs.gameMode > 2 and self.optionButt.detect_touch(touch.location):
                gs.gameMode = 1
                toggleVisibleSprites(self,False)
                self.touchCycle = True
                
            # Detect control inputs
            xy = touchStick(touch.location,self.moveStick)
            if xy[0] != 0:
            	self.moveStick.ctrl = xy
            	self.moveStick.id = touch.touch_id
            	self.moveAura.alpha = 1
            	
            xy = touchStick(touch.location,self.tiltStick)
            if xy[0] != 0:
            	self.tiltStick.ctrl = xy
            	self.tiltStick.id = touch.touch_id	
            	self.tiltAura.alpha = 1
        
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
                self.moveAura.alpha = 0.5
        
            if touch.touch_id == self.tiltStick.id:
                self.tiltStick.ctrl = (0,0)
                self.tiltAura.alpha = 0.5
                
        def stop(self):
            motion.stop_updates()
                
    if __name__ == '__main__':
        run(Game(), LANDSCAPE, show_fps=False)
        
        
        
        
