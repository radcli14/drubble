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
u0 = [0,p.y0,p.l0,0,0,0,0,0,-4,8,3,12]
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
game_over = False
u = u0
n = 0
stoolCount = 0
floorCount = 0
clock = pygame.time.Clock()
clock.tick()
averageStepTime = 0
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
            # Reset the game
            if event.key == pygame.K_ESCAPE:
                t  = 0
                te = 0
                n  = 0
                u  = u0
                eventCount = 0
                ballMoves = False
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
    xr    = np.around(u[0],-1)
    Ticks = ( ((xr-20)*MeterToPixel-PixelOffset+width/2,height-MeterToPixel) , 
              ((xr-20)*MeterToPixel-PixelOffset+width/2,height)              ,
              ((xr-10)*MeterToPixel-PixelOffset+width/2,height)              , 
              ((xr-10)*MeterToPixel-PixelOffset+width/2,height-MeterToPixel) ,
              (xr*MeterToPixel-PixelOffset+width/2,height-MeterToPixel)      ,
              (xr*MeterToPixel-PixelOffset+width/2,height)                   ,
              ((xr+10)*MeterToPixel-PixelOffset+width/2,height)              ,
              ((xr+10)*MeterToPixel-PixelOffset+width/2,height-MeterToPixel) ,
              ((xr+20)*MeterToPixel-PixelOffset+width/2,height-MeterToPixel) ,
              ((xr+20)*MeterToPixel-PixelOffset+width/2,height) )
    font   = pygame.font.SysFont("comicsansms", int(np.around(0.8*MeterToPixel)))
    yard_m20 = font.render(str(int(xr-20)), True, black)
    yard_m10 = font.render(str(int(xr-10)), True, black)
    yard_0   = font.render(str(int(xr)), True, black)
    yard_p10 = font.render(str(int(xr+10)), True, black)
    yard_p20 = font.render(str(int(xr+20)), True, black)
    
    # Draw the background, ball, head, player, and stool
    screen.fill(skyBlue)
    pygame.draw.circle(screen, pink, ballPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.circle(screen, darkGreen, headPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.lines(screen, pink, False, trajList, 1)
    pygame.draw.lines(screen, darkGreen, False, stickList, 3)
    pygame.draw.lines(screen, red, False, stoolList, 3)
    pygame.draw.lines(screen, black, False, ((0,height-MeterToPixel),(width,height-MeterToPixel)),1)
    pygame.draw.lines(screen, black, False,Ticks)
    screen.blit(yard_m20,((xr-19.7)*MeterToPixel-PixelOffset+width/2, height-MeterToPixel))
    screen.blit(yard_m10,((xr-9.7)*MeterToPixel-PixelOffset+width/2, height-MeterToPixel))
    screen.blit(yard_0,((xr+0.3)*MeterToPixel-PixelOffset+width/2, height-MeterToPixel))
    screen.blit(yard_p10,((xr+10.3)*MeterToPixel-PixelOffset+width/2, height-MeterToPixel))
    screen.blit(yard_p20,((xr+20.3)*MeterToPixel-PixelOffset+width/2, height-MeterToPixel))
    
    #screen.blit(bigChair, bC_rect)
    pygame.display.flip()
    
    # Timing Variables
    #thisStepTime = clock.tick()
    #if n>0:
    #    averageStepTime = (averageStepTime*(n-1) + thisStepTime)/n
    clock.tick(fs)
    
    #input("This is here for debugging ... Press Enter to continue...")
