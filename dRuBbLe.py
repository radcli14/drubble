# Import required packages
#from IPython import get_ipython
#get_ipython().magic('reset -sf')
exec(open('./drubbleFunc.py').read())
#from drubbleFunc import *

# Obtain Parameters
p = parameters()

# Initial states
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,0,0,0,p.x0,p.y0,p.l0,0,0,0,0,1]
gs = gameState(u0)

# Open display
if engine == 'pygame':
		pygame.init()
		pygame.font.init()
		screen = pygame.display.set_mode(size) #,pygame.FULLSCREEN) 
		pygame.display.set_caption('dRuBbLe')
		icon = pygame.image.load('figs/icon.png')
		pygame.display.set_icon(icon)

# Define the Events
#events = [BallHitStool,BallHitFloor]

# Set the keyboard input and mouse defaults
keyPush        = np.zeros(8)
mousePos       = width/2,height/2 
userControlled = np.array([True, True, True, True]) 
userControlled = np.array([True, False, False, False])

# Initialize stats
stats = gameScore()

# Settings for setting initial trjectory
showedSplash = False
sa           = np.pi/4
startAngle   = sa
ss           = 10
startSpeed   = 2*ss
phase        = 0
msg = ['','',
       'OPTIONS \n    Single Drubble \n\n\n Press space to begin!!!',
       'Use arrow keys to control player, W-A-S-D keys to control stool. Press space to begin!',
       'Press space to select starting angle',
       'Press space to select starting speed','','','']

# Run an infinite loop until gameMode is zero
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
		                phase = 0
		                startSpeed = 10
		                clock.tick(10)
		                continue
		            
		            # Start the ball moving!
		            if gs.gameMode == 5 and event.key == pygame.K_SPACE:
		                gs.gameMode = 6
		                gs.u[2] = vx0
		                gs.u[3] = vy0
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
		        showedSplash = makeSplashScreen(showedSplash)
		    
		    if gs.gameMode>1 and gs.gameMode<7:
		        screen.fill(skyBlue)
		        ## ANGLE AND SPEED SETTINGS
		        if gs.gameMode == 4:
		            startAngle = 0.25*np.pi*(1 + 0.75*np.sin(phase))
		        if gs.gameMode == 5:
		            startSpeed = ss*(1 + 0.75*np.sin(phase))
		        if gs.gameMode == 4 or gs.gameMode == 5:
		            phase += 3*dt
		            vx0 = startSpeed*np.cos(startAngle)
		            vy0 = startSpeed*np.sin(startAngle)
		            gs.u[2] = vx0
		            gs.u[3] = vy0
		         
		        ## SIMULATION
		        gs.simStep()
		        
		        # Update statistics
		        if gs.gameMode==6:
		            stats.update()
		 
		        ## ANIMATION
		        # Get the ranges in meters using the setRanges function
		        xrng, yrng, MeterToPixel, PixelOffset, MeterToRatio, RatioOffset = setRanges(gs.u)
		        
		        # Draw the background
		        makeBackgroundImage()
		        
		        # Draw the ball and player
		        makeGameImage()
		        
		        # Draw the score line
		        makeScoreLine()
		        
		        # Draw meter markers
		        makeMarkers()
		
		        # Show the Message Text
		        showMessage(msg[gs.gameMode])  
		
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
	gs.gameMode = 6
	gs.u[2] = 3
	gs.u[3] = 12
	class Game (Scene):
		def setup(self):
			# Add the game state classes to the scene
			self.gs = gs
			
			# Generate the sky blue background
			self.background_color = '#acf9ee'
			
			# Get ranges for drawing the player and ball
			xrng, yrng, MeterToPixel, PixelOffset, MeterToRatio, RatioOffset = setRanges(gs.u)
			
			# Initialize the background image
			# self.bg0 =
			
			# Initialize the ball image
			self.ball = SpriteNode('emj:Red_Circle')
			dbPix = 2*p.rb*MeterToPixel
			self.ball.size = (dbPix,dbPix)
			self.ball.anchor_point = (0.5, 0.5)
			self.ball.position = (gs.xb*MeterToPixel+PixelOffset, (gs.yb+p.rb)*MeterToPixel)
			self.add_child(self.ball)
			
			# Initialize the player's head
			spPix = 0.7*MeterToPixel
			self.head = SpriteNode('emj:Slice_Of_Pizza')
			self.head.size = (spPix,spPix)
			self.head.anchor_point = (0.5, 0.0)
			self.head.position = (gs.xp*MeterToPixel+PixelOffset, (gs.yp+p.d)*MeterToPixel)
			self.add_child(self.head)
			
		def update(self):
			# Get the gravity vector
			g = gravity()
			#print(np.around(g,2))
			if np.abs(g[1])>0.05:
				keyPush[0] = max(min(10*g[1],1),-1)
			else:
				keyPush[0] = 0
			
			# Run one simulation step
			self.gs.simStep()
			xrng, yrng, m2p, po, m2r, ro = setRanges(self.gs.u)
			
			# update the ball and head sprites
			self.ball.position = (gs.xb*m2p-po+width/2, 
                                 (gs.yb+p.rb)*m2p+height/20)
			self.head.position = (gs.xp*m2p-po+width/2, 
                                 (gs.yp+p.d)*m2p+height/20)
			
			
		def draw(self):
			xrng, yrng, m2p, po, m2r, ro = setRanges(self.gs.u)
			
			# Generate the trajectory
			linePlot(gs.xTraj,gs.yTraj,m2p,po,width,height,gray,1)
			
			# Generate the bottom line
			stroke(black)
			stroke_weight(height/20)
			line(0,height/40,width,height/40)
			
			# Generate a player image
			xv,yv,sx,sy = stickDude(gs)
			linePlot(xv,yv,m2p,po,width,height,darkGreen,0.15*m2p)
			
			# Generate a stool image
			linePlot(sx,sy,m2p,po,width,height,red,0.1*m2p)
						
	if __name__ == '__main__':
		run(Game(), LANDSCAPE, show_fps=True)
