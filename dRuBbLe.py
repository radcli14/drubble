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

# Set the keyboard input and mouse defaults
keyPush        = np.zeros(8)
mousePos       = width/2,height/2 
userControlled = np.array([True, True, True, True]) 
userControlled = np.array([True, False, False, False])

# Initialize stats
stats = gameScore()

# Settings for setting initial trjectory
showedSplash = False

msg = ['','',
       ['OPTIONS','    Single Drubble','','','','Press space to begin!!!'],
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
            showedSplash = makeSplashScreen(showedSplash)
        
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
    gs.gameMode = 3
    
    def cycleModes(gs,stats):
        # Progress through angle and speed selection
        if (gs.gameMode==3 or gs.gameMode==4): 
            gs.gameMode += 1
            gs.phase = 0
            return
            
        # Start the ball moving!
        if gs.gameMode == 5:
            gs.gameMode = 6
            return
            
        # Reset the game
        if gs.gameMode == 6:
            stats.__init__()
            gs.__init__(u0)
            gs.gameMode = 3
            return

    class Game (Scene):
        def setup(self):
            # Add the game state classes to the scene
            self.touchCycle = False
            
            # Generate the sky blue background
            self.background_color = '#acf9ee'
            
            # Get ranges for drawing the player and ball
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
            # Initialize the background image
            # self.bg0 =
            
            # Initialize the ball image
            self.ball = SpriteNode('emj:Red_Circle')
            dbPix = 2*p.rb*m2p
            self.ball.size = (dbPix,dbPix)
            self.ball.anchor_point = (0.5, 0.5)
            self.ball.position = (gs.xb*m2p+po, (gs.yb+p.rb)*m2p)
            self.add_child(self.ball)
            
            # Initialize the player's head
            spPix = 0.7*m2p
            self.head = SpriteNode('emj:Slice_Of_Pizza')
            self.head.size = (spPix,spPix)
            self.head.anchor_point = (0.5, 0.0)
            self.head.position = (gs.xp*m2p+po, (gs.yp+p.d)*m2p)
            self.add_child(self.head)
        
        def update(self):
            # Update if there was a touch
            if self.touchCycle:
                cycleModes(gs,stats)
                self.touchCycle = False
                
            # Get the gravity vector
            g = gravity()
            gThreshold = 0.05
            slope = 5
            if g[1]>gThreshold:
                keyPush[0] = min(slope*(g[1]-gThreshold),1)
            elif g[1]<-gThreshold:
                keyPush[1] = -max(slope*(g[1]+gThreshold),-1)
            else:
                keyPush[0] = 0
                keyPush[1] = 0
            
            ## ANGLE AND SPEED SETTINGS
            if gs.gameMode>2 and gs.gameMode<6:
                gs.setAngleSpeed()
            
            # Run one simulation step
            gs.simStep()
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
            # update the ball and head sprites
            self.ball.position = (gs.xb*m2p-po+width/2, 
                                 (gs.yb+p.rb)*m2p+height/20)
            self.head.position = (gs.xp*m2p-po+width/2, 
                                 (gs.yp+p.d)*m2p+height/20)
                                 
            #self.gs = gs
            #print(gs.gameMode)
            
        def draw(self):
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
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
                        
        def touch_began(self, touch):
            self.touchCycle = True
            #self.cycleModes()
            
       
                
    if __name__ == '__main__':
        run(Game(), LANDSCAPE, show_fps=True)
