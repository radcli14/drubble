# Import required packages
from IPython import get_ipython
get_ipython().magic('reset -sf')
exec(open("./drubbleFunc.py").read())
pygame.init()
pygame.font.init()

# Obtain Parameters
p = parameters()

# Initial states
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
#vx0 = 3  # Initial ball horizontal velocity [m/s]
#vy0 = 16 # Initial ball vertical velocity [m/s]
u0 = [p.x0,p.y0,p.l0,0.5,0,0,0,0,0,0,0,0]
u  = u0

# Set timing
fs = 30
dt = 1/fs
te = 0
t  = 0
n  = 0

# Predict position and time where ball hits stool
[xb,yb,tb,Xb,Yb] = BallPredict(u0)

# Open display
screen = pygame.display.set_mode(size)
pygame.display.set_caption('dRuBbLe')

# Define the Events
events = [BallHitStool,BallHitFloor]

# Set the keyboard input and mouse defaults
keyPush        = np.zeros(8)
mousePos       = width/2,height/2 
userControlled = np.array([True, True, True, True]) 
#userControlled = np.array([False, False, False, False])

# Initialize stats
stats = resetStats()

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
startAngle   = np.pi/4
startSpeed   = 10
phase        = 0
msg = ['','','',
       'Use arrow keys to control player, W-A-S-D keys to control stool. Press space to begin!',
       'Press space to select starting angle',
       'Press space to select starting speed','','','']

# Run an infinite loop until gameMode is zero
clock = pygame.time.Clock()
while gameMode>0:
    ## USER INPUT
    for event in pygame.event.get():
        # Detect the quit event (window close)
        if event.type == pygame.QUIT: 
            gameMode = 0
        
        # Detect keyboard input
        if event.type == pygame.KEYDOWN:
            # Exit the splash screen
            if gameMode == 1 and event.key == pygame.K_SPACE:
                gameMode = 3
                clock.tick(10)
                continue
            
            # Progress through angle and speed selection
            ismem = np.in1d(gameMode,[3,4])
            if ismem[0] and event.key == pygame.K_SPACE:
                gameMode += 1
                phase = 0
                startSpeed = 10
                clock.tick(10)
                continue
            
            # Start the ball moving!
            if gameMode == 5 and event.key == pygame.K_SPACE:
                gameMode = 6
                u[10] = vx0
                u[11] = vy0
                clock.tick(10)
                continue
            
            # Reset the game
            if gameMode == 6 and event.key == pygame.K_ESCAPE:
                t  = 0
                n  = 0
                te = 0
                u  = u0
                stats = resetStats()
                gameMode = 3
                [xb,yb,tb,Xb,Yb] = BallPredict(u)
                
        # Get player control inputs
        keyPush = playerControlInput(event)             

    # Show the Splash Sreen
    if gameMode==1:
        showedSplash = makeSplashScreen(showedSplash)
    
    if gameMode==2 or gameMode==3 or gameMode==4 or gameMode==5 or gameMode==6:
        screen.fill(skyBlue)
        ## ANGLE AND SPEED SETTINGS
        if gameMode == 4:
            startAngle = 0.25*np.pi*(1 + np.sin(phase))
        if gameMode == 5:
            startSpeed = 10*(1 + np.sin(phase))
        if gameMode == 4 or gameMode == 5:
            phase += 0.05
            vx0 = startSpeed*np.cos(startAngle)
            vy0 = startSpeed*np.sin(startAngle)
            u[10] = vx0
            u[11] = vy0
            [xb,yb,tb,Xb,Yb] = BallPredict(u)
            tb = tb+te
         
        ## SIMULATION
        sol, StoolBounce, FloorBounce, te = simThisStep(t,u,te) 
    
        if StoolBounce or FloorBounce:
            # Recalculate ball position the next time it crosses top of stool
            [xb,yb,tb,Xb,Yb] = BallPredict(sol.y[:,-1])
            tb = tb+te
         
        # Add solution into the state vector
        u = sol.y[:,-1].tolist()
    
        # Stop the ball from moving if the player hasn't hit space yet
        if gameMode==3 or gameMode==4 or gameMode==5:
            u[8]  = u0[8]
            u[9]  = u0[9]
            u[10] = 0
            u[11] = 0   
        if gameMode==6:
            # Time increment
            t += dt    
            n += 1
            
            # Stats
            if StoolBounce and stats.stoolDist<u[0]:
                stats.stoolDist = u[0]
            if stats.maxHeight<u[9]:
                stats.maxHeight = u[9]   
            stats.stoolCount += StoolBounce
            stats.floorCount += FloorBounce
            stats.score = int(stats.stoolDist*stats.maxHeight*stats.stoolCount)
        
        ## ANIMATION
        # Get the ranges in meters using the setRanges function
        xrng, yrng, MeterToPixel, PixelOffset = setRanges(u)
        
        # Draw the background
        # makeBackgroundImage()
        
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
    if p.timeRun and n>0:
        thisStepTime = clock.tick()
        stats.averageStepTime = (stats.averageStepTime*(n-1) + thisStepTime)/n
    clock.tick(fs)

# Exit the game after game_over   
pygame.quit()