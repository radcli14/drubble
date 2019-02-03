# Import required packages
exec(open("./drubbleFunc.py").read())
pygame.init()

# Window size and color definition
size = width, height = 1000, 600
speed = [2, 2]
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,100,100)
skyBlue = (220, 255, 255)
darkGreen = (0,120,0)

# Obtain Parameters
p = parameters()

# Initial States
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.y0,p.l0,0,0,0,0,0,-4,8,3,12]
te = 0
t  = 0
fs = 30
dt = 1/fs

# Predict position and time where ball hits stool
[xb,yb,tb,Xb,Yb] = BallPredict(u0)

# Open display
screen = pygame.display.set_mode(size)

# Import the Big Chair image
#bigChair = pygame.image.load("bigChair.jpg")
#bC_rect = bigChair.get_rect()

# Define the Events
events = [BallHitStool,BallHitFloor]

# Set the keyboard input and mouse defaults
keyPush        = np.array([0,0,0,0])
mousePos       = width/2,height/2 
userControlled = True 
ballMoves      = False

# Run an infinite loop until stopped
game_over = False
u = u0
n = 0
eventCount = 0
while not game_over:
    ## USER INPUT
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT: 
            #sys.exit()
            game_over = True
            pygame.quit()
        # Detect keyboard input    
        if event.type == pygame.KEYDOWN:
            # Start the ball moving!
            if event.key == pygame.K_SPACE:
                ballMoves = True
                u[10] = u0[10]
                u[11] = u0[11]
            # Left and right control for Bx parameter
            if event.key == pygame.K_LEFT:
                keyPush[0] = -1
            if event.key == pygame.K_RIGHT:
                keyPush[0] = +1
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT):
                keyPush[0] = 0
            
    #print(keyPush)   
    
    ## SIMULATION
    # Time until event 
    timeUntilBounce = tb-t;

    sol, wasEvent, te = simThisStep(t,u,te) 
    eventCount += wasEvent

    if wasEvent:
        # Recalculate ball position the next time it crosses top of stool
        [xb,yb,tb,Xb,Yb] = BallPredict(sol.y[:,-1])
        tb = tb+te
        
    # Add solution into the state vector
    u = sol.y[:,-1].tolist()
    
    # Stop the ball from moving if the player hasn't hit space yet
    if ballMoves:
        t += dt    
        n += 1
    else:
        u[8]  = u0[8]
        u[9]  = u0[9]
        u[10] = 0
        u[11] = 0
    
    ## ANIMATION
    # Get the plotting vectors using stickDude function
    xv,yv,sx,sy = stickDude(u)
    
    # Get the ranges in meters using the setRange function
    xrng, yrng = setRanges(u)
    
    # Convert locations in meters to pixels
    MeterToPixel = width/(xrng[1]-xrng[0])
    PixelOffset  = (xrng[0]+xrng[1])/2*MeterToPixel
    xvp          = np.array(xv)*MeterToPixel-PixelOffset+width/2
    yvp          = height-np.array(yv)*MeterToPixel
    sxp          = np.array(sx)*MeterToPixel-PixelOffset+width/2
    syp          = height-np.array(sy)*MeterToPixel
    trajList     = list(zip(np.array(Xb)*MeterToPixel-PixelOffset+width/2,
                            height-np.array(Yb)*MeterToPixel))
    stickList    = list(zip(xvp,yvp))
    stoolList    = list(zip(sxp,syp))
    ballPosition = (int(u[8]*MeterToPixel-PixelOffset+width/2),
                    int(height-u[9]*MeterToPixel) )
    headPosition = (int(u[0]*MeterToPixel-PixelOffset+width/2), 
                    int(height-(u[1]+1.75*p.d)*MeterToPixel) )
    
    # Draw the background, ball, head, player, and stool
    screen.fill(skyBlue)
    pygame.draw.circle(screen, pink, ballPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.circle(screen, darkGreen, headPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.lines(screen, pink, False, trajList, 1)
    pygame.draw.lines(screen, darkGreen, False, stickList, 3)
    pygame.draw.lines(screen, red, False, stoolList, 3)
    
    #screen.blit(bigChair, bC_rect)
    pygame.display.flip()
    # I want this to work ... pygame.time.Clock.tick(fs/2)
    
    #input("This is here for debugging ... Press Enter to continue...")
