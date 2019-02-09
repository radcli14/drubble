# Import required packages
from IPython import get_ipython
get_ipython().magic('reset -sf')
exec(open("./drubbleFunc.py").read())
pygame.init()
pygame.font.init()

# Window size and color definition
size = width, height = 1000, 600
red       = (255,0,0,1)
green     = (0,255,0,1)
blue      = (0,0,255,1)
darkBlue  = (0,0,128,1)
white     = (255,255,255,1)
black     = (0,0,0,1)
pink      = (255,100,100,1)
skyBlue   = (150, 255, 255, 0.3)
darkGreen = (0,120,0,1)

# Obtain Parameters
p = parameters()

# Initial states
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
vx0 = 3  # Initial ball horizontal velocity [m/s]
vy0 = 16 # Initial ball vertical velocity [m/s]
u0 = [p.x0,p.y0,p.l0,0.5,0,0,0,0,0,0,vx0,vy0]
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
salpha = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
pygame.display.set_caption('dRuBbLe')

# Import the Big Chair image
bigChair = pygame.image.load("bigChair.jpg")
bC_rect = bigChair.get_rect()

# Import the splash screen
splash     = pygame.image.load('splash.png')
splash     = pygame.transform.scale(splash, (int(0.84*width), int(0.9*height)))
splashrect = splash.get_rect()
splashrect.left   = int(-0.1*width)
splashrect.bottom = int(0.9*height)

diagram    = pygame.image.load('diagram.png')
diagram    = pygame.transform.scale(diagram,(int(0.3*width),int(0.9*height)))
diagrect   = diagram.get_rect();
diagrect.left = int(width*0.75)
diagrect.bottom = int(height+4)
diagrect.height = int(height*0.1)

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
            # Start the ball moving!
            if gameMode == 1 and event.key == pygame.K_SPACE:
                gameMode = 3
                clock.tick(10)
                continue
            if gameMode == 3 and event.key == pygame.K_SPACE:
                gameMode = 6
                u[10] = vx0
                u[11] = vy0
                
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
        if showedSplash:
            screen.fill(skyBlue)
            screen.blit(splash, splashrect)
            screen.blit(diagram, diagrect)
            font = pygame.font.SysFont("comicsansms", int(height/12))
            spc  = font.render('Press Space To Begin!', True, darkGreen)
            screen.blit(spc,(0.22*width,int(0.88*height)))
        else:
            for splashNess in range(0,240,4):
                screen.fill((splashNess,splashNess,splashNess))
                screen.blit(splash, splashrect)
                screen.blit(diagram, diagrect)
                pygame.display.flip()
                clock.tick(30)
            showedSplash = True
        
    if gameMode==2 or gameMode==3 or gameMode==4 or gameMode==5 or gameMode==6:
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
        # Get the plotting vectors using stickDude function
        xv,yv,sx,sy = stickDude(u)
        
        # Get the ranges in meters using the setRange function
        xrng, yrng = setRanges(u)
        
        # Convert locations in meters to pixels
        MeterToPixel = width/(xrng[1]-xrng[0])
        PixelOffset  = (xrng[0]+xrng[1])/2*MeterToPixel
        xvp          = np.array(xv)*MeterToPixel-PixelOffset+width/2
        yvp          = height-(np.array(yv)+1)*MeterToPixel
        sxp          = np.array(sx)*MeterToPixel-PixelOffset+width/2
        syp          = height-(np.array(sy)+1)*MeterToPixel
        trajList     = list(zip(np.array(Xb)*MeterToPixel-PixelOffset+width/2,
                                height-(np.array(Yb)+1)*MeterToPixel))
        stickList    = list(zip(xvp,yvp))
        stoolList    = list(zip(sxp,syp))
        ballPosition = (int(u[8]*MeterToPixel-PixelOffset+width/2),
                        int(height-(u[9]+1)*MeterToPixel) )
        headPosition = (int(u[0]*MeterToPixel-PixelOffset+width/2), 
                        int(height-(u[1]+1.75*p.d+1)*MeterToPixel) )
        
        # Draw the background, ball, head, player,  stool, floor
        screen.fill(white)
        bigChairNow    = pygame.transform.scale(bigChair,
                          (int(0.03*width*MeterToPixel),
                           int(0.04*height*MeterToPixel)))
        bC_rect.left   = -15*MeterToPixel-PixelOffset+width/2
        bC_rect.bottom = height-0.7*MeterToPixel
        bC_rect.height = 0.04*height*MeterToPixel
        screen.blit(bigChairNow, bC_rect)
        screen.fill(skyBlue)
        pygame.draw.circle(screen, pink, ballPosition, int(p.rb*MeterToPixel), 0)
        pygame.draw.circle(screen, darkGreen, headPosition, int(p.rb*MeterToPixel), 0)
        pygame.draw.lines(screen, pink, False, trajList, 1)
        pygame.draw.lines(screen, darkGreen, False, stickList, 
                          int(np.ceil(0.15*MeterToPixel)))
        pygame.draw.lines(screen, red, False, stoolList, 
                          int(np.ceil(0.1*MeterToPixel)))
        pygame.draw.line(screen, black, (0,height-0.5*MeterToPixel),
                         (width,height-0.5*MeterToPixel),int(MeterToPixel))
        
        # Draw the score line
        pygame.draw.line(screen, black, (0,height/30), 
                         (width,height/30),int(height/15))
        font = pygame.font.SysFont("comicsansms", int(height/24))
        time = font.render('Time = '+f'{t:.1f}', True, white)
        screen.blit(time,(0.05*width,0))
        dist = font.render('Distance = '+f'{stats.stoolDist:.1f}', True, white)
        screen.blit(dist,(0.23*width,0))
        high = font.render('Height = '+f'{stats.maxHeight:.2f}', True, white)
        screen.blit(high,(0.45*width,0))
        boing = font.render('Boing! = '+str(int(stats.stoolCount)), True, white)
        screen.blit(boing,(0.65*width,0))
        score = font.render('Score = '+str(stats.score),True,white)
        screen.blit(score,(0.8*width,0))
        
        # Draw meter markers
        font   = pygame.font.SysFont("comicsansms", int(np.around(0.8*MeterToPixel)))
        xrng_r = np.around(xrng,-1)
        xrng_n = int((xrng_r[1]-xrng_r[0])/10)+1
        for k in range(0,xrng_n):
            xr = xrng_r[0]+10*k
            start_pos = [xr*MeterToPixel-PixelOffset+width/2,height-MeterToPixel]
            end_pos   = [xr*MeterToPixel-PixelOffset+width/2,height]
            pygame.draw.line(screen, white, start_pos, end_pos)
            meter = font.render(str(int(xr)), True, white)
            start_pos[0]=start_pos[0]+0.2*MeterToPixel
            start_pos[1]=start_pos[1]-0.1*MeterToPixel
            screen.blit(meter,start_pos)

    #screen.blit(bigChair, bC_rect)
    pygame.display.flip()
    
    # Timing Variables
    if p.timeRun and n>0:
        thisStepTime = clock.tick()
        averageStepTime = (averageStepTime*(n-1) + thisStepTime)/n
    clock.tick(fs)
    
    #input("This is here for debugging ... Press Enter to continue...")

# Exit the game after game_over
#sys.exit()    
pygame.quit()