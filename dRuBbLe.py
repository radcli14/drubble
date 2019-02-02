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

# Run an infinite loop until stopped
game_over = False
u = u0
n = 0
eventCount = 0
while not game_over:
    ## USER INPUT
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT: 
            #sys.exit()
            game_over = True
            pygame.quit()

    ## SIMULATION
    # Time until event 
    timeUntilBounce = tb-t;

    sol, wasEvent, te = simThisStep(t,u,te) 
    eventCount += wasEvent

    if wasEvent:
        # Recalculate ball position the next time it crosses top of stool
        [xb,yb,tb,Xb,Yb] = BallPredict(sol.y[:,-1])
        tb = tb+te
        
    t += dt    
    n += 1
    u = sol.y[:,-1].tolist()
    
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
    #bC_rect = bC_rect.move(speed)
    #if bC_rect.left < 0 or bC_rect.right > width:
    #    speed[0] = -speed[0]
    #if bC_rect.top < 0 or bC_rect.bottom > height:
    #    speed[1] = -speed[1]

    screen.fill(skyBlue)
    pygame.draw.circle(screen, pink, ballPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.circle(screen, darkGreen, headPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.lines(screen, pink, False, trajList, 1)
    pygame.draw.lines(screen, darkGreen, False, stickList, 3)
    pygame.draw.lines(screen, red, False, stoolList, 3)
    
    #screen.blit(bigChair, bC_rect)
    pygame.display.flip()