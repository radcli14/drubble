# Import required packages
exec(open("./drubbleFunc.py").read())
pygame.init()
pygame.font.init()

# Window size and color definition
size = width, height = 1200, 600
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
u0 = [5,p.y0,p.l0,0,0,0,0,0,0,0,3,16]
te = 0
t  = 0
fs = 30
dt = 1/fs

# Predict position and time where ball hits stool
[xb,yb,tb,Xb,Yb] = BallPredict(u0)

# Open display
screen = pygame.display.set_mode(size)
pygame.display.set_caption('dRuBbLe')

# Import the Big Chair image
#bigChair = pygame.image.load("bigChair.jpg")
#bC_rect = bigChair.get_rect()

# Define the Events
events = [BallHitStool,BallHitFloor]

# Set the keyboard input and mouse defaults
keyPush        = np.zeros(8)
mousePos       = width/2,height/2 
userControlled = np.array([True, True, True, True]) 
ballMoves      = False

# Run an infinite loop until stopped
gameQuit = False
u = u0
n = 0
stoolCount = 0
stoolDist  = 0
maxHeight  = 0
floorCount = 0
clock = pygame.time.Clock()
averageStepTime = 0
while not gameQuit:
    ## USER INPUT
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT: 
            #sys.exit()
            gameQuit = True
        # Detect keyboard input    
        if event.type == pygame.KEYDOWN:
            # Start the ball moving!
            if event.key == pygame.K_SPACE:
                ballMoves = True
                u[10] = u0[10]
                u[11] = u0[11]
            # Reset the game
            if event.key == pygame.K_ESCAPE:
                t  = 0
                te = 0
                n  = 0
                u  = u0
                stoolCount = 0
                stoolDist  = 0
                maxHeight  = 0
                floorCount = 0
                averageStepTime = 0
                ballMoves  = False
                [xb,yb,tb,Xb,Yb] = BallPredict(u)
            # Left and right control for Bx parameter
            if event.key == pygame.K_LEFT:
                keyPush[0] = 1
            if event.key == pygame.K_RIGHT:
                keyPush[1] = 1
            # Up and down control for By parameter
            if event.key == pygame.K_UP:
                keyPush[2] = 1
            if event.key == pygame.K_DOWN:
                keyPush[3] = 1
            # W and S control for Bl parameter    
            if event.key == pygame.K_w:
                keyPush[4] = 1
            if event.key == pygame.K_s:
                keyPush[5] = 1    
            # A and D control for Bth parameter
            if event.key == pygame.K_a:
                keyPush[6] = 1
            if event.key == pygame.K_d:
                keyPush[7] = 1    
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keyPush[0] = 0
            if event.key == pygame.K_RIGHT:
                keyPush[1] = 0
            # Up and down control for By parameter
            if event.key == pygame.K_UP:
                keyPush[2] = 0
            if event.key == pygame.K_DOWN:
                keyPush[3] = 0
            # W and S control for Bl parameter    
            if event.key == pygame.K_w:
                keyPush[4] = 0
            if event.key == pygame.K_s:
                keyPush[5] = 0    
            # A and D control for Bth parameter
            if event.key == pygame.K_a:
                keyPush[6] = 0
            if event.key == pygame.K_d:
                keyPush[7] = 0             

    ## SIMULATION
    # Time until event 
    timeUntilBounce = tb-t;

    sol, StoolBounce, FloorBounce, te = simThisStep(t,u,te) 
    stoolCount += StoolBounce
    floorCount += FloorBounce

    if StoolBounce or FloorBounce:
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
    
    # Stats
    if StoolBounce and stoolDist<u[0]:
        stoolDist = u[0]
    if maxHeight<u[9]:
        maxHeight = u[9]   
    
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
    dist = font.render('Distance = '+f'{stoolDist:.1f}', True, white)
    screen.blit(dist,(0.23*width,0))
    high = font.render('Height = '+f'{maxHeight:.2f}', True, white)
    screen.blit(high,(0.45*width,0))
    boing = font.render('Boing! = '+str(int(stoolCount)), True, white)
    screen.blit(boing,(0.65*width,0))
    score = font.render('Score = '+str(int(stoolDist*maxHeight*stoolCount)),
                        True,white)
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
pygame.quit()