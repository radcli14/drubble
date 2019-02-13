# Import modules
# import os
import sys
import time
import numpy as np
import scipy.integrate as spi
import scipy.special as scs
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.cbook import get_sample_data
import pygame

# Define the bunch class
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

# Window size and color definition
size = width, height = 1000, 600
red       = (255,0,0)
green     = (0,255,0)
blue      = (0,0,255)
darkBlue  = (0,0,128)
white     = (255,255,255)
black     = (0,0,0)
pink      = (255,100,100)
skyBlue   = (220, 230, 255)
darkGreen = (0,120,0)

## LOAD IMAGES, AND DEFINE FUNCTIONS TO DISPLAY THEM
# Import the Big Chair image
bigChair = pygame.image.load('figs/bigChair.png')
bC_rect  = bigChair.get_rect()

# Import the Entertainment and Sports Arena image
ESA      = pygame.image.load('figs/esa.png')
ESA_rect = ESA.get_rect()

# Import the Anacostia River image
river      = pygame.image.load('figs/river.png')
river_rect = river.get_rect()

# Import the USS Barry image
barry      = pygame.image.load('figs/barry.png')
barry_rect = river.get_rect()

# Import the splash screen
splash     = pygame.image.load('figs/splash.png')
splash     = pygame.transform.scale(splash, (int(0.84*width), int(0.9*height)))
splashrect = splash.get_rect()
splashrect.left   = int(-0.1*width)
splashrect.bottom = int(0.9*height)

diagram    = pygame.image.load('figs/diagram.png')
diagram    = pygame.transform.scale(diagram,(int(0.3*width),int(0.8*height)))
diagrect   = diagram.get_rect();
diagrect.left = int(width*0.75)
diagrect.bottom = int(height+4)
diagrect.height = int(height*0.1)

def showMessage(msgText):
    font = pygame.font.SysFont(p.MacsFavoriteFont, int(height/32))
    msgRend = font.render(msgText, True, black)
    screen.blit(msgRend,(0.05*width,0.1*height))
    
def makeBackgroundImage():
    # Draw the Big Chair
    drawBackgroundImage(bigChair,bC_rect,-5,7,20)
    
    # Draw the Anacostia River
    drawBackgroundImage(river,river_rect,100,10,25)
    
    # Draw the Entertainment and Sports Arena
    drawBackgroundImage(ESA,ESA_rect,40,10,20)
    
    # Draw the USS Barry
    drawBackgroundImage(barry,barry_rect,163,9.5,20)

def drawBackgroundImage(image,rect,xpos,ypos,howTall):
    w,h = rect.size
    defPixNum = MeterToPixel # Default pixel number
    numPixelHeight = howTall*defPixNum
    scf = numPixelHeight/h # Scale Factor
    W = int(scf*w)
    H = int(scf*h)
    imageNow    = pygame.transform.scale(image,(W,H))
    rectNow = rect
    rectNow.center = ((xpos*defPixNum-PixelOffset+width/2)*0.5,height-ypos*defPixNum)
    rectNow.size = (W,H)
    screen.blit(imageNow, rectNow)
    
def makeGameImage():
    # Get the plotting vectors using stickDude function
    xv,yv,sx,sy = stickDude(u)
        
    # Convert to pixels
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
    
    # Draw circles and lines
    pygame.draw.circle(screen, pink, ballPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.circle(screen, darkGreen, headPosition, int(p.rb*MeterToPixel), 0)
    pygame.draw.lines(screen, pink, False, trajList, 1)
    pygame.draw.lines(screen, darkGreen, False, stickList, 
                      int(np.ceil(0.15*MeterToPixel)))
    pygame.draw.lines(screen, red, False, stoolList, 
                      int(np.ceil(0.1*MeterToPixel)))
    pygame.draw.line(screen, black, (0,height-0.5*MeterToPixel),
                     (width,height-0.5*MeterToPixel),int(MeterToPixel))

def makeScoreLine():
    #pygame.draw.line(screen, black, (0,height/30), 
    #                 (width,height/30),int(height/15))
    font = pygame.font.SysFont(p.MacsFavoriteFont, int(height/24))
    time = font.render('Time = '+f'{t:.1f}', True, black)
    screen.blit(time,(0.05*width,0))
    dist = font.render('Distance = '+f'{stats.stoolDist:.1f}', True, black)
    screen.blit(dist,(0.23*width,0))
    high = font.render('Height = '+f'{stats.maxHeight:.2f}', True, black)
    screen.blit(high,(0.45*width,0))
    boing = font.render('Boing! = '+str(int(stats.stoolCount)), True, black)
    screen.blit(boing,(0.65*width,0))
    score = font.render('Score = '+str(stats.score),True,black)
    screen.blit(score,(0.8*width,0))

def makeMarkers():
    font   = pygame.font.SysFont(p.MacsFavoriteFont,
                                 int(np.around(0.8*MeterToPixel)))
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

# Parameters
def parameters():
    # Game parameters
    g   = 9.81 # Gravitational acceleration [m/s^2]
    COR = 0.8  # Coefficient of restitution
    rb  = 0.2  # Radius of the ball
       
    # Player parameters
    mc = 50      # Mass of player [kg]
    mg = 2       # Mass of stool [kg]
    m  = mc+mg   # Total mass [kg]
    x0 = 5       # Initial player position [m]
    y0 = 1.5     # Equilibrium position of player CG [m]
    d  = 0.3     # Relative position from player CG to stool rotation axis [m]
    l0 = 1.5     # Equilibrium position of stool
    ax = 1       # Horizontal acceleration [g]
    Qx = ax*m*g; # Max horizontal force [N]
    Gx = 2.0;    # Control gain on Qx 
    fy = 0.8     # vertical frequency [Hz]
    Ky = m*(fy*2*np.pi)**2 # Leg stiffness [N/m]
    Qy = Ky*0.3  # Leg strength [N], to be updated
    fl = 2.2     # Stool extension frequency
    Kl = mg*(fl*2*np.pi)**2 # Arm stiffness [N/m]
    Ql = Kl*0.3  # Arm strength [N]
    ft = 1.5     # Stool tilt frequency [Hz]
    Kt = (mg*l0*l0)*(ft*2*np.pi)**2 # Tilt stiffnes [N-m/rad]
    Qt = 0.6*Kt  # Tilt strength [N-m]
    Gt = 0.8     # Control gain on Qt
    vx = 10      # Horizontal top speed [m/s]
    Cx = Qx/vx   # Horizontal damping [N-s/m]
    zy = 0.1     # Vertical damping ratio
    Cy = 2*zy*np.sqrt(Ky*m) # Vertical damping [N-s/m]
    zl = 0.2     # Arm damping ratio
    Cl = 2*zl*np.sqrt(Kl*m) # Arm damping [N-s/m]
    zt = 0.05    # Stool tilt damping ratio
    Ct = 2*zl*np.sqrt(Kt*m) # Tilt damping [N-m-s/rad]

    # Stool parameters
    xs = np.array([-0.25,  0.25,  0.14, 
                    0.16, -0.16,  0.16, 
                    0.18, -0.18,  0.18,  
                    0.2 ,  0.14, -0.14, -0.2])
    ys = np.array([  0  ,  0   ,  0   , 
                   -0.3 , -0.3 , -0.3 , 
                   -0.6 , -0.6 , -0.6 ,
                   -0.9 ,  0   ,   0  , -0.9 ])
    
    M = np.matrix([[  m    , 0  , 0  , -mg*l0  ],
                   [  0    , m  , mg ,    0    ],
                   [  0    , mg , mg ,    0    ],
                   [-mg*l0 , 0  , 0  , mg*l0**2]])
    
    # Parameter settings I'm using to try to improve running speed
    invM = M.I
    linearMass  = False
    odeMethod   = 'RK23' 
    odeIsEuler  = True
    nEulerSteps = 4
    timeRun     = False
    
    # Font settings
    MacsFavoriteFont = 'comicsansms' # 'jokerman' 'poorrichard' 'rockwell' 'comicsansms'
    
    p = Bunch(g=g,mc=mc,mg=mg,m=m,x0=x0,y0=y0,d=d,l0=l0,ax=ax,Qx=Qx,Gx=Gx,
              Qy=Qy,Ql=Ql,Qt=Qt,fy=fy,Ky=Ky,fl=fl,Kl=Kl,ft=ft,Kt=Kt,vx=vx,
              Cx=Cx,zy=zy,Cy=Cy,zl=zl,Cl=Cl,zt=zt,Ct=Ct,xs=xs,ys=ys,COR=COR,
              rb=rb,M=M,invM=invM,linearMass=linearMass,odeMethod=odeMethod,
              odeIsEuler=odeIsEuler,nEulerSteps=nEulerSteps,timeRun=timeRun,
              MacsFavoriteFont=MacsFavoriteFont)
    return p 

def resetStats():
    stats = Bunch(t=0,n=0,stoolCount=0,stoolDist=0,maxHeight=0,floorCount=0,
                  score=0,averageStepTime=0)
    return stats

# Predict
def BallPredict(u):
    x  = u[8]  # Ball horizontal position
    y  = u[9]  # Ball vertical position
    dx = u[10] # Ball horizontal velocity
    dy = u[11] # Ball vertical velocity
    
    if (dy>0) & (y<p.y0+p.d+p.l0):
        # Solve for time and height at apogee
        ta = dy/p.g
        ya = 0.5*p.g*ta**2

        # Solve for time the ball would hit the stool
        tb = ta + np.sqrt(2*ya/p.g)
    else:
        # Solve for time that the ball would hit the stool
        tb = -(-dy - np.sqrt(dy**2+2*p.g*(y-p.y0-p.d-p.l0)))/p.g
        
    if np.isnan(tb):
        tb = 0

    # Solve for position that the ball would hit the stool
    xb = x+dx*tb
    yb = y+dy*tb-0.5*p.g*tb**2
    
    # Solve for the arc
    Tb = np.linspace(0,tb,20)
    Xb = x+dx*Tb
    Yb = y+dy*Tb-0.5*p.g*Tb**2
    return xb,yb,tb,Xb,Yb

# Equation of Motion
def PlayerAndStool(t,u):
    # Resolve the States
    l   = u[2]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    th  = u[3]
    s   = np.sin(th)
    c   = np.cos(th)
    dl  = u[6]
    dth = u[7]
    q   = np.matrix([u[0],u[1],u[2],u[3]])
    dq  = np.matrix([u[4],u[5],u[6],u[7]])
    q   = q.T
    dq  = dq.T

    # Mass Matrix
    if not p.linearMass:     
        M = np.matrix([[   p.m   ,    0    ,-p.mg*s,-p.mg*l*c],
                       [    0    ,   p.m   , p.mg*c,-p.mg*l*s],
                       [-p.mg*s  ,  p.mg*c , p.mg  ,   0     ],
                       [-p.mg*l*c,-p.mg*l*s,   0   , p.mg*l*l]])

    # Damping Matrix     
    C = np.diag([p.Cx,p.Cy,p.Cl,p.Ct])
    
    # Stiffness Matrix
    K = np.diag([0 ,p.Ky,p.Kl,p.Kt])
    
    # Frequency Check
    # V,D = np.linalg.eig(M.I*K)
    # print("omega^2 = ",V)
    # print("freq    = ",np.sqrt(V)/2/np.pi)
    # print("phi     = \n",D)
    
    # Centripetal [0,1] and Coriolis [3] Force Vector
    D = np.matrix([[-p.mg*dl*dth*c+p.mg*l*dth*dth*s], 
                   [-p.mg*dl*dth*s+p.mg*l*dth*dth*c], 
                   [0],
                   [2*p.mg*dth]])
    
    # Gravitational Force Vector
    G = np.matrix([[0],
                   [p.m*p.g],
                   [p.mg*p.g*c],
                   [-p.mg*p.g*l*s]])         

    # Fix the time, if supplied as tspan vector
    if np.size(t)>1:
        t = t[0]       
    
    # Control inputs form the generalized forces
    Q, Bx, By, Bl, Bth, ZEM, wantAngle, xdiff, ydiff = ControlLogic(t,u)
    
    # Equation of Motion
    RHS = -C*dq-K*q+K*q0-D-G+Q
    if p.linearMass:
        ddq = p.invM*RHS
    else:
        ddq = M.I*RHS
    
    # Output State Derivatives
    du = [u[4],u[5],u[6],u[7],ddq[0,0], # Player velocities
          ddq[1,0],ddq[2,0],ddq[3,0],   # Player accelerations
          u[10],u[11],0,-p.g]           # Ball velocities and accelerations
    return du

def playerControlInput(event):
    if event.type == pygame.KEYDOWN:
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
    return keyPush

def ControlLogic(t,u):
    # Time until event 
    timeUntilBounce = tb-t;
    
    # Control horizontal acceleration based on zero effort miss (ZEM)
    # Subtract 1 secoond to get there early, and subtract 0.1 m to keep the
    # ball moving forward 
    ZEM = (xb-0.05) - u[0] - u[4]*np.abs(timeUntilBounce-1)
    if userControlled[0]:
        if keyPush[0] +keyPush[1] == 0:
            Bx = -scs.erf(u[4])
        else:
            Bx = keyPush[1]-keyPush[0]
    else:
        Bx = p.Gx*ZEM
        if Bx>1:
            Bx = 1
        elif (Bx<-1) or (timeUntilBounce<0.2) & (timeUntilBounce>0):
            Bx = -1
    
    # Control leg extension based on timing, turn on when impact in <0.2 sec
    if userControlled[1]:
        By = keyPush[2]-keyPush[3]
    else:
        if (timeUntilBounce<0.6) and (timeUntilBounce>0.4):
            By = -1
        elif np.abs(timeUntilBounce)<0.2:       
            By = 1
        else:
            By = 0
    
    # Control arm extension based on timing, turn on when impact in <0.2 sec
    if userControlled[2]:
        Bl = keyPush[4]-keyPush[5]
    else:
        Bl = np.abs(timeUntilBounce)<0.2
    
    # Control stool angle by pointing at the ball
    xdiff = u[8]-u[0]
    ydiff = u[9]-u[1]-p.d
    wantAngle = np.arctan2(-xdiff,ydiff)
    if userControlled[3]:
        Bth = keyPush[6]-keyPush[7]
    else:
        Bth = p.Qt*(wantAngle-u[3])
        if Bth>1:
            Bth = 1
        elif Bth<-1 or ((tb-t)<0.2) & ((tb-t)>0):
            Bth = -1
        
    Q = np.matrix([[Bx*p.Qx],[By*p.Qy],[Bl*p.Ql],[Bth*p.Qt]])    
    
    return Q, Bx, By, Bl, Bth, ZEM, wantAngle, xdiff, ydiff    

def BallHitFloor(t,u):
    return u[9]-p.rb
BallHitFloor.terminal = True

def BallHitStool(t,u):
    # Get the stool locations using stickDude function
    xv,yv,sx,sy = stickDude(u)
    
    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = np.array([sx[1]-sx[0],sy[1]-sy[0]])
    
    # Calculate z that minimizes the distance
    z  = ( (u[8]-sx[0])*r1[0] + (u[9]-sy[0])*r1[1] )/( r1@r1 )
    
    # Find the closest point of impact on the stool
    if z<0:
        ri = np.array([sx[0],sy[0]])
    elif z>1:
        ri = np.array([sx[1],sy[1]])
    else:
        ri = np.array([sx[0]+z*r1[0],sy[0]+z*r1[1]])

    # Vector from the closest point of impact to the center of the ball    
    r2 = np.array([u[8]-ri[0],u[9]-ri[1]])

    # Calculate the distance to the outer radius of the ball t
    #L  = np.sign(r2[1])*np.sqrt(r2@r2)-p.rb
    L = np.sqrt(r2@r2)-p.rb
    
    return L 
BallHitStool.terminal = True 

def BallBounce(t,u):
    # Get the stool locations using stickDude function
    xv,yv,sx,sy = stickDude(u)
    
    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = np.array([sx[1]-sx[0],sy[1]-sy[0]])
    
    # Calculate z that minimizes the distance
    z  = ( (u[8]-sx[0])*r1[0] + (u[9]-sy[0])*r1[1] )/( r1@r1 )
    
    # Find the closest point of impact on the stool
    if z<0:
        ri = np.array([sx[0],sy[0]])
    elif z>1:
        ri = np.array([sx[1],sy[1]])
    else:
        ri = np.array([sx[0]+z*r1[0],sy[0]+z*r1[1]])
    
    # Velocity at the impact point 
    print("ri=",ri)
    vi = np.array([u[4]-u[2]*np.sin(u[3])-(ri[1]-u[1])*u[7],
                   u[5]+u[2]*np.cos(u[3])+(ri[0]-u[0])*u[7]])
    print("vi=",vi)
    
    # Velocity of the ball relative to impact point
    vbrel = np.array([u[10],u[11]])-vi
    
    # Vector from the closest point of impact to the center of the ball    
    r2 = np.array([u[8]-ri[0],u[9]-ri[1]])
    u2 = r2/np.sqrt(r2@r2)
    print("r2=",r2)
    print("u2=",u2)
    
    # Delta ball velocity
    print("vb=",[u[10],u[11]])
    print("vbrel=",vbrel)
    delta_vb = 2*p.COR*(u2@vbrel)
    
    # Velocity after bounce
    vBounce = -u2*delta_vb + np.array([u[10],u[11]])
    
    # Obtain the player recoil states
    BounceImpulse = -p.mg*vBounce
    c = np.cos(u[3])
    s = np.sin(u[3])
    l = u[2]
    dRdq = np.matrix([[ 1  , 0  ],
                      [ 0  , 1  ],
                      [-s  , c  ],
                      [-c*l,-s*l] ])
    Qi = dRdq@BounceImpulse
    vRecoil = p.invM@np.transpose(Qi)

    return vBounce, vRecoil

def bhDebug(T,Y):
    N = np.size(T)
    Ls = np.zeros(N)
    Lf = np.zeros(N)
    for n in range(N):
        Ls[n] = BallHitStool(T[n],Y[n,:])
        Lf[n] = BallHitFloor(T[n],Y[n,:])
    plt.figure()
    plt.plot(T,Ls,'-bo')  
    plt.plot(T,Lf,'-rx')    
    plt.grid('on')

def simThisStep(t,u,te):
    # Initial assumption, there was no event
    StoolBounce = False
    FloorBounce = False
    
    # Prevent event detection if there was already one within 0.1 seconds, 
    # or if the ball is far from the stool or ground
    L = BallHitStool(t,u)
    vball = np.array((u[10],u[11]))
    
    if p.odeIsEuler:
        # Integrate using Euler method
        sol = Bunch(y=np.zeros((12,p.nEulerSteps)),status=False)
        sol.y[:,0] = u
        for k in range(1,p.nEulerSteps):
            dydt = PlayerAndStool(t,sol.y[:,k-1])
            sol.y[:,k] = sol.y[:,k-1] + np.array(dydt)*dt/p.nEulerSteps
            if (t-te)>0.1 and (L<2*np.sqrt(vball@vball)*dt or u[9]<2*(-vball[1]*dt)):
                if BallHitStool(t,sol.y[:,k])<0:
                    StoolBounce = True
                    EventString = 'Awesome Stool Bounce!'
                if BallHitFloor(t,sol.y[:,k])<0:   
                    FloorBounce = True
                    EventString = 'Boring Floor Bounce :('
                if StoolBounce or FloorBounce:
                    te = t+k*dt
                    ue = sol.y[:,k]
                    break        
    else:
        if (t-te)>0.1 and (L<2*np.sqrt(vball@vball)*dt or u[9]<2*(-vball[1]*dt)):
            sol = spi.solve_ivp(PlayerAndStool,[0,dt],u,method=p.odeMethod, 
                                max_step=dt/4,first_step=dt/4,min_step=dt/8,
                                events=events)
        else:
            sol = spi.solve_ivp(PlayerAndStool,[0,dt],u,method=p.odeMethod,
                                first_step=dt,min_step=dt/4)    
            if sol.status:
                # Determine if the was stool or floor
                # and get states at time of event
                ue = sol.y[:,-1].tolist()
                if np.size(sol.t_events[0]):
                    te = sol.t_events[0][0]+t
                    StoolBounce = True
                    EventString = 'Awesome Stool Bounce!'
                elif np.size(sol.t_events[1]):
                    te = sol.t_events[1][0]+t
                    FloorBounce = True
                    EventString = 'Boring Floor Bounce :('
                    
    # If an event occured, increment the counter, otherwise continue
    if StoolBounce or FloorBounce:        
        # Print the time and type of event    
        print("te = ",te,' sec, ',EventString)

        # Change ball states depending on if it was a stool or floor bounce
        if StoolBounce:
            ue[9] = ue[9]+0.001
            
            # Obtain the bounce velocity
            vBounce,vRecoil = BallBounce(te,ue)
            print("vBounce=",vBounce)
            ue[10] = vBounce[0]
            ue[11] = vBounce[1]
            
            # Add  the recoil to the player states
            ue[4] = ue[4] + vRecoil[0]
            ue[5] = ue[5] + vRecoil[1]
            ue[6] = ue[6] + vRecoil[2]
            ue[7] = ue[7] + vRecoil[3]
            
        elif FloorBounce:
            ue[9] = 0.001
        
            # Reverse direction of the ball
            ue[10] = +p.COR*ue[10]
            ue[11] = -p.COR*ue[11]       
     
        # Re-initialize from the event states
        sol = spi.solve_ivp(PlayerAndStool,[0,dt],ue)
    else:
        wasEvent = False
    
    return sol, StoolBounce, FloorBounce, te  


def ThirdPoint(P0,P1,L,SGN):

    Psub = [P0[0]-P1[0],P0[1]-P1[1]]
    Padd = [P0[0]+P1[0],P0[1]+P1[1]]
    P2 = [Padd[0]/2, Padd[1]/2]
    d = np.linalg.norm(Psub) # Distance between point P0,P1

    if d > L:
        P3 = P2
    else:
        a  = (d**2)/2/d # Distance to mid-Point
        h  = np.sqrt( (L**2)/4 - a**2 )
        x3 = P2[0] + h*SGN*Psub[1]/d
        y3 = P2[1] - h*SGN*Psub[0]/d
        P3 = [x3,y3]
    return P3

def stickDude(inp):
    # Get the state variables
    if np.size(inp)<2:
        # States at time t[n]
        x  = Y[n,0] # sol.y[0,n]
        y  = Y[n,1] # sol.y[1,n]
        l  = Y[n,2] # sol.y[2,n]
        th = Y[n,3] # sol.y[3,n]
        v  = Y[n,4] # sol.y[4,n]
    else:
        x  = inp[0]
        y  = inp[1]
        l  = inp[2]
        th = inp[3]
        v  = inp[4]
        
    s = np.sin(th)
    c = np.cos(th)
        
    # Right Foot [rf] Left Foot [lf] Positions
    rf = [x-0.25+(v/p.vx)*np.sin(1.5*x+3*np.pi/2), 
          0.2*(v/p.vx)*(1+np.sin(1.5*x+3*np.pi/2))]
    lf = [x+0.25+(v/p.vx)*np.cos(1.5*x), 
          0.2*(v/p.vx)*(1+np.cos(1.5*x))]
    
    # Waist Position
    w = [x,y-p.d]
    
    # Right Knee [rk] Left Knee [lk] Positions
    rk = ThirdPoint(w,rf,p.y0-p.d,-1) #*((v>-2)-0.5))
    lk = ThirdPoint(w,lf,p.y0-p.d,1) #2*((v>2)-0.5))
    
    # Shoulder Position
    sh = [x,y+p.d]
    
    # Stool Position
    sx = x+p.xs*c-(l+p.ys)*s
    sy = y+p.d+(l+p.ys)*c+p.xs*s
    
    # Right Hand [rh] Left Hand [lh] Position 
    rh = [sx[7], sy[7]] # [x-0.5*l*sp,y+p.d+0.5*l*cp]
    lh = [sx[6], sy[6]] # [x-0.5*l*sm,y+p.d+0.5*l*cm]
    
    # Right Elbow [re] Left Elbow [le] Position
    re = ThirdPoint(sh,rh,1,1)
    le = ThirdPoint(sh,lh,1,-1)
    
    # Plotting vectors
    xv = [rf[0],rk[0],w[0],lk[0],lf[0],lk[0],w[0],sh[0],re[0],rh[0],re[0],sh[0],le[0],lh[0]]
    yv = [rf[1],rk[1],w[1],lk[1],lf[1],lk[1],w[1],sh[1],re[1],rh[1],re[1],sh[1],le[1],lh[1]]
    
    return xv,yv,sx,sy

def initPlots():
    LN, = plt.plot([], [], '-g', animated=True) # Stick figure
    HD, = plt.plot([], [], 'go', animated=True) # Head
    GD, = plt.plot([], [],'-bx', animated=True) # Ground
    ST, = plt.plot([], [], '-r', animated=True) # Stool
    BL, = plt.plot([], [], 'mo', animated=True) # Ball
    BA, = plt.plot([], [], ':k', animated=True) # Ball (arc)
    return LN, HD, GD, ST, BL, BA,

def init():
    ax.set_xlim(-1,11)
    ax.set_ylim(-1,5)
    
    #ax.set_aspect('equal')
    return LN, HD, GD, ST, BL, BA,

def setRanges(u):
    maxy  = 1.25*np.max([u[9],u[1]+p.d+u[2]*np.cos(u[3]),12])
    diffx = 1.25*np.abs(u[0]-u[8])
    midx  = (u[0]+u[8])/2
    if diffx>2*(maxy+1):
        xrng = midx-0.5*diffx, midx+0.5*diffx
        yrng = -1, 0.5*(diffx-0.5)
    else:
        xrng = midx-maxy-0.5, midx+maxy+0.5
        yrng = -1, maxy
        
    MeterToPixel = width/(xrng[1]-xrng[0])
    PixelOffset  = (xrng[0]+xrng[1])/2*MeterToPixel
    return xrng, yrng, MeterToPixel, PixelOffset
        
def animate(n):
    # Get the plotting vectors using stickDude function
    xv,yv,sx,sy = stickDude(Y[n,:])

    # Get state variables
    x  = Y[n,0] # sol.y[0,n]
    y  = Y[n,1] # sol.y[1,n]
    l  = Y[n,2] # sol.y[2,n]
    th = Y[n,3] # sol.y[3,n]

    # Update the plot
    LN.set_data(xv, yv)
    HD.set_data(x,y+p.d*1.6)
    GD.set_data(np.round(x+np.linspace(-40,40,81)),0)
    ST.set_data(sx,sy)
    BL.set_data(Y[n,8],Y[n,9])
    BA.set_data(XB[n,:],YB[n,:])
    
    # Update Axis Limits
    xrng, yrng = setRanges(Y[n,:])
    ax.set_xlim(xrng)
    ax.set_ylim(yrng)
    
    return LN, HD, GD, ST, BL, BA,