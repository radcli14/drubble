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

# Set timing
fs = 60
dt = 1/fs

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
#userControlled = np.array([True, True, True, True]) 
userControlled = np.array([False, False, False, False])

# Initialize stats
stats = gameScore()

# Define Game Mode
# 0 = Quit
# 1 = Splash screen
# 2 = Options screen (TBD)
# 3 = In game, pre-angle set
# 4 = In game, angle set
# 5 = In game, distance set
# 6 = In game
# 7 = Game over, resume option
# 8 = Game over, high scores
gameMode = 1
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
		while gameMode>0:
		    ## USER INPUT
		    for event in pygame.event.get():
		        # Detect the quit event (window close)
		        if event.type == pygame.QUIT: 
		            gameMode = 0
		        
		        # Detect keyboard input
		        if event.type == pygame.KEYDOWN:
		            # Exit the game
		            if event.key == pygame.K_ESCAPE:
		                gameMode = 0
		            
		            # Exit the splash screen
		            if gameMode==1 and event.key == pygame.K_SPACE:
		                gameMode = 2
		                clock.tick(10)
		                continue
		            
		            if gameMode==2 and event.key == pygame.K_SPACE:
		                gameMode = 3
		                clock.tick(10)
		                continue
		            
		            # Progress through angle and speed selection
		            if (gameMode==3 or gameMode==4) and event.key == pygame.K_SPACE:
		                gameMode += 1
		                phase = 0
		                startSpeed = 10
		                clock.tick(10)
		                continue
		            
		            # Start the ball moving!
		            if gameMode == 5 and event.key == pygame.K_SPACE:
		                gameMode = 6
		                gs.u[2] = vx0
		                gs.u[3] = vy0
		                clock.tick(10)
		                continue
		            
		            # Reset the game
		            if gameMode == 6 and event.key == pygame.K_SPACE:
		                stats = gameScore()
		                gs = gameState(u0)
		                gameMode = 2
		
		        # Get player control inputs
		        keyPush = playerControlInput(event)             
		
		    # Show the Splash Sreen
		    if gameMode==1:
		        showedSplash = makeSplashScreen(showedSplash)
		    
		    if gameMode>1 and gameMode<7:
		        screen.fill(skyBlue)
		        ## ANGLE AND SPEED SETTINGS
		        if gameMode == 4:
		            startAngle = 0.25*np.pi*(1 + np.sin(phase))
		        if gameMode == 5:
		            startSpeed = ss*(1 + np.cos(phase))
		        if gameMode == 4 or gameMode == 5:
		            phase += 0.05
		            vx0 = startSpeed*np.cos(startAngle)
		            vy0 = startSpeed*np.sin(startAngle)
		            gs.u[2] = vx0
		            gs.u[3] = vy0
		         
		        ## SIMULATION
		        gs.simStep()
		        
		        # Update statistics
		        if gameMode==6:
		            stats.update()
		 
		        ## ANIMATION
		        # Get the ranges in meters using the setRanges function
		        xrng, yrng, MeterToPixel, PixelOffset = setRanges(gs.u)
		        
		        # Draw the background
		        makeBackgroundImage()
		        
		        # Draw the ball and player
		        makeGameImage()
		        
		        # Draw the score line
		        makeScoreLine()
		        
		        # Draw meter markers
		        makeMarkers()
		
		        # Show the Message Text
		        showMessage(msg[gameMode])  
		
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
	darkGreen = (0,120/255,0)
	width, height = (736,414)
	gameMode = 6
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
			# Run one simulation step
			self.gs.simStep()
			xrng, yrng, MeterToPixel, PixelOffset, MeterToRatio, RatioOffset = setRanges(self.gs.u)
			
			# update the ball and head sprites
			self.ball.position = (gs.xb*MeterToPixel-PixelOffset+width/2, (gs.yb+p.rb)*MeterToPixel)
			self.head.position = (gs.xp*MeterToPixel-PixelOffset+width/2, (gs.yp+p.d)*MeterToPixel)
			
			
		def draw(self):
			xrng, yrng, MeterToPixel, PixelOffset, MeterToRatio, RatioOffset = setRanges(self.gs.u)
			
			# Generate a player image
			xv,yv,sx,sy = stickDude(gs)
			x=np.array(xv)*MeterToPixel-PixelOffset+width/2
			y=np.array(yv)*MeterToPixel
			stroke(darkGreen)
			fill(darkGreen)
			stroke_weight(3)
			for k in range(1,np.size(xv)):
				line(x[k-1],y[k-1],x[k],y[k])
			
			# Generate a stool image
			x=np.array(sx)*MeterToPixel-PixelOffset+width/2
			y=np.array(sy)*MeterToPixel
			stroke(red)
			fill(red)
			stroke_weight(3)
			for k in range(1,np.size(sx)):
				line(x[k-1],y[k-1],x[k],y[k])
						
	if __name__ == '__main__':
		run(Game(), LANDSCAPE, show_fps=True)
