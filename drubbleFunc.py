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
size      = width, height = 1000, 600
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
# Import the background image combining ESA, Big Chair, River, and USS Barry
bg0 = pygame.image.load('figs/bg0.png')
bg0 = pygame.transform.scale(bg0, (2400, 400))
bg0_rect   = bg0.get_rect()

# Import the splash screen
splash     = pygame.image.load('figs/splash.png')
splash     = pygame.transform.scale(splash, (int(0.84*width), int(0.9*height)))
splashrect = splash.get_rect()
splashrect.left   = int(-0.1*width)
splashrect.bottom = int(0.9*height)

diagram    = pygame.image.load('figs/diagram.png')
diagram    = pygame.transform.scale(diagram,(int(0.3*width),int(0.8*height)))
diagrect   = diagram.get_rect();
diagrect.left   = int(width*0.75)
diagrect.bottom = int(height+4)
diagrect.height = int(height*0.1)

def makeSplashScreen(showedSplash):
    if showedSplash:
        screen.fill(skyBlue)
        screen.blit(splash, splashrect)
        screen.blit(diagram, diagrect)
        font = pygame.font.SysFont(p.MacsFavoriteFont, int(height/12))
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
    return showedSplash

def showMessage(msgText):
    font = pygame.font.SysFont(p.MacsFavoriteFont, int(height/32))
    msgRend = font.render(msgText, True, black)
    screen.blit(msgRend,(0.05*width,0.1*height))
    
def makeBackgroundImage():
    # Draw the ESA, Big Chair, River, and USS Barry
    drawBackgroundImage(bg0,bg0_rect,-0.25,-5,0)

def drawBackgroundImage(image,rect,xpos,ypos,howTall):
    rect.left = width*(-u[0]/120+xpos)
    rect.bottom = height+(u[9]/40-0.9)*MeterToPixel
    screen.blit(image,rect)
    
def makeGameImage():
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    # Get the plotting vectors using stickDude function
    xv,yv,sx,sy = stickDude(u)
        
    # Convert to pixels
    xvp          = np.array(xv)*MeterToPixel-PixelOffset+width/2
    yvp          = height-(np.array(yv)+1)*MeterToPixel
    sxp          = np.array(sx)*MeterToPixel-PixelOffset+width/2
    syp          = height-(np.array(sy)+1)*MeterToPixel
    trajList     = list(zip(np.array(xTraj)*MeterToPixel-PixelOffset+width/2,
                            height-(np.array(yTraj)+1)*MeterToPixel))
    stickList    = list(zip(xvp,yvp))
    stoolList    = list(zip(sxp,syp))
    ballPosition = (int(xb*MeterToPixel-PixelOffset+width/2),
                    int(height-(yb+1)*MeterToPixel) )
    headPosition = (int(xp*MeterToPixel-PixelOffset+width/2), 
                    int(height-(yp+1.75*p.d+1)*MeterToPixel) )
    
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
    linearMass  = True
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

def varStates(obj):
    obj.xb  = obj.u[0]  # Ball distance [m]
    obj.yb  = obj.u[1]  # Ball height [m]
    obj.dxb = obj.u[2]  # Ball horizontal speed [m]
    obj.dyb = obj.u[3]  # Ball vertical speed [m]
    obj.xp  = obj.u[4]  # Player distance [m]
    obj.yp  = obj.u[5]  # Player height [m]
    obj.lp  = obj.u[6]  # Stool extension [m]
    obj.tp  = obj.u[7]  # Stool tilt [rad]
    obj.dxp = obj.u[8]  # Player horizontal speed [m/s]
    obj.dyp = obj.u[9]  # Player vertical speed [m/s]
    obj.dlp = obj.u[10] # Stool extension rate [m/s]
    obj.dtp = obj.u[11] # Stool tilt rate [rad/s]
    return obj

class gameState:
    # Initiate the state variables as a list, and as individual variables
    def __init__(self,u0):
        self.t  = 0
        self.n  = 0
        self.te = 0
        
        self.u  = u0[:]
        self.ue = u0[:]
        self.xI,self.yI,self.tI,self.xTraj,self.yTraj = BallPredict(u0)
        self = varStates(self)
       
    # Execute a simulation step of duration dt    
    def simStep(self):
        # Increment timing variables
        self.t += dt   
        self.n += 1
        
        # Initial assumption, there was no event
        StoolBounce = False
        FloorBounce = False
        
        # Prevent event detection if there was already one within 0.1 seconds, 
        # or if the ball is far from the stool or ground
        L = BallHitStool(self.t,self.u)       # Distance to stool
        vBall = np.array((self.dxb,self.dyb)) # Velocity
        sBall = np.sqrt(vBall@vBall)          # Speed
        
        # Integrate using Euler method
        sol = Bunch(y=np.zeros((12,p.nEulerSteps+1)),status=False)
        sol.y[:,0] = self.u
        for k in range(1,p.nEulerSteps+1):
            dydt = PlayerAndStool(t,sol.y[:,k-1])
            sol.y[:,k] = sol.y[:,k-1] + np.array(dydt)*dt/p.nEulerSteps
            if (self.t-self.te)>0.1 and (L<2*sBall*dt or self.yb<2*self.dyb*dt):
                if BallHitStool(self.t,sol.y[:,k])<0:
                    StoolBounce = True
                if BallHitFloor(self.t,sol.y[:,k])<0:   
                    FloorBounce = True
                if StoolBounce or FloorBounce:
                    self.te = self.t+k*dt
                    self.ue = sol.y[:,k].tolist()
                    tBreak = k*dt
                    break 
        
        # If an event occured, increment the counter, otherwise continue
        if StoolBounce or FloorBounce:        
            # Change ball states depending on if it was a stool or floor bounce
            if StoolBounce:
                self.ue[1] = self.ue[1]+0.001
                
                # Obtain the bounce velocity
                vBounce,vRecoil = BallBounce(self.te,self.ue)
                self.ue[2] = vBounce[0]
                self.ue[3] = vBounce[1]
                
                # Add  the recoil to the player states
                self.ue[8]  = self.ue[8]  + vRecoil[0]
                self.ue[9]  = self.ue[9]  + vRecoil[1]
                self.ue[10] = self.ue[10] + vRecoil[2]
                self.ue[11] = self.ue[11] + vRecoil[3]
                
            elif FloorBounce:
                self.ue[1] = 0.001
            
                # Reverse direction of the ball
                self.ue[2] = +p.COR*self.ue[2]
                self.ue[3] = -p.COR*self.ue[3]       
         
            # Re-initialize from the event states
            sol = spi.solve_ivp(PlayerAndStool,[0,dt-tBreak],self.ue)
            
            # Predict the future trajectory of the ball
            self.xI,self.yI,self.tI,self.xTraj,self.yTraj = BallPredict(self.u)
            self.tI = self.tI+self.te
        
        # Update states
        self.u = sol.y[:,-1].tolist()
        
        # Stop the ball from moving if the player hasn't hit space yet
        if gameMode<6:
            self.u[0] = u0[0]
            self.u[1] = u0[1]
            self.u[2] = 0
            self.u[3] = 0   
            
        # Named states    
        self   = varStates(self)

def unpackStates(u):
    # xp, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    xb  = u[0]  # Ball distance [m]
    yb  = u[1]  # Ball height [m]
    dxb = u[2]  # Ball horizontal speed [m]
    dyb = u[3]  # Ball vertical speed [m]
    xp  = u[4]  # Player distance [m]
    yp  = u[5]  # Player height [m]
    lp  = u[6]  # Stool extension [m]
    tp  = u[7]  # Stool tilt [rad]
    dxp = u[8]  # Player horizontal speed [m/s]
    dyp = u[9]  # Player vertical speed [m/s]
    dlp = u[10] # Stool extension rate [m/s]
    dtp = u[11] # Stool tilt rate [rad/s]
    return xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp

def resetStats():
    stats = Bunch(t=0,n=0,stoolCount=0,stoolDist=0,maxHeight=0,floorCount=0,
                  score=0,averageStepTime=0)
    return stats

# Predict
def BallPredict(u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    if (dyb>0) and (yb<p.y0+p.d+p.l0): 
        # Solve for time and height at apogee
        ta = dyb/p.g
        ya = 0.5*p.g*ta**2

        # Solve for time the ball would hit the stool
        tI = ta + np.sqrt(2*ya/p.g)
    else:
        # Solve for time that the ball would hit the stool
        tI = -(-dyb - np.sqrt(dyb**2+2*p.g*(yb-p.y0-p.d-p.l0)))/p.g
        
    if np.isnan(tI):
        tI = 0

    # Solve for position that the ball would hit the stool
    xI = xb+dxb*tI
    yI = yb+dyb*tI-0.5*p.g*tI**2
    
    # Solve for the arc
    T     = np.linspace(0,tI+1,40)
    xTraj = xb+dxb*T
    yTraj = yb+dyb*T-0.5*p.g*T**2
    
    # Output variables
    # xI = Ball distance at impact [m]
    # yI = Ball height at impact [m]
    # tI = Time at impact [s]
    # xTraj = Ball trajectory distances [m]
    # yTraj = Ball trajectory heights [m]
    return xI,yI,tI,xTraj,yTraj

# Equation of Motion
def PlayerAndStool(t,u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    # Create player state vectors
    q   = np.matrix([[xp],[yp],[lp],[tp]])
    dq  = np.matrix([[dxp],[dyp],[dlp],[dtp]])

    # Sines and cosines of the stool angle
    s   = np.sin(tp)
    c   = np.cos(tp)
    
    # Mass Matrix
    if not p.linearMass:     
        M = np.matrix([[   p.m    ,    0     ,-p.mg*s,-p.mg*lp*c ],
                       [    0     ,   p.m    , p.mg*c,-p.mg*lp*s ],
                       [-p.mg*s   ,  p.mg*c  , p.mg  ,   0       ],
                       [-p.mg*lp*c,-p.mg*lp*s,   0   , p.mg*lp**2]])

    # Damping Matrix     
    C = np.diag([p.Cx,p.Cy,p.Cl,p.Ct])
    
    # Stiffness Matrix
    K = np.diag([0 ,p.Ky,p.Kl,p.Kt])
    
    # Centripetal [0,1] and Coriolis [3] Force Vector
    D = np.matrix([[-p.mg*dlp*dtp*c+p.mg*lp*dtp*dtp*s], 
                   [-p.mg*dlp*dtp*s+p.mg*lp*dtp*dtp*c], 
                   [0],
                   [2*p.mg*dtp]])
    
    # Gravitational Force Vector
    G = np.matrix([[ 0            ],
                   [ p.m*p.g      ],
                   [ p.mg*p.g*c   ],
                   [-p.mg*p.g*lp*s]])         

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
    du = [dxb,dyb,                             # Ball velocities
          0,-p.g,                              # Ball accelerations
          dxp,dyp,dlp,dtp,                     # Player velocities
          ddq[0,0],ddq[1,0],ddq[2,0],ddq[3,0]] # Player accelerations
          
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
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    # Time until event 
    timeUntilBounce = tI-t;
    
    # Control horizontal acceleration based on zero effort miss (ZEM)
    # Subtract 1 secoond to get there early, and subtract 0.05 m to keep the
    # ball moving forward 
    ZEM = (xI-0.05) - xp - dxp*np.abs(timeUntilBounce-1)
    if userControlled[0]:
        if keyPush[0] +keyPush[1] == 0:
            Bx = -scs.erf(dxp)
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
    xdiff = xb-xp # Ball distance - player distance
    ydiff = yb-yp-p.d
    wantAngle = np.arctan2(-xdiff,ydiff)
    if userControlled[3]:
        Bth = keyPush[6]-keyPush[7]
    else:
        Bth = p.Qt*(wantAngle-tp)
        if Bth>1:
            Bth = 1
        elif Bth<-1 or ((tI-t)<0.2) & ((tI-t)>0):
            Bth = -1
        
    Q = np.matrix([[Bx*p.Qx],[By*p.Qy],[Bl*p.Ql],[Bth*p.Qt]])    
    
    return Q, Bx, By, Bl, Bth, ZEM, wantAngle, xdiff, ydiff    

def BallHitFloor(t,u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u) 
    return yb-p.rb
BallHitFloor.terminal = True

def BallHitStool(t,u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
        
    # Get the stool locations using stickDude function
    xv,yv,sx,sy = stickDude(u)
    
    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = np.array([sx[1]-sx[0],sy[1]-sy[0]])
    
    # Calculate z that minimizes the distance
    z  = ( (xb-sx[0])*r1[0] + (yb-sy[0])*r1[1] )/( r1@r1 )
    
    # Find the closest point of impact on the stool
    if z<0:
        ri = np.array([sx[0],sy[0]])
    elif z>1:
        ri = np.array([sx[1],sy[1]])
    else:
        ri = np.array([sx[0]+z*r1[0],sy[0]+z*r1[1]])

    # Vector from the closest point of impact to the center of the ball    
    r2 = np.array([xb-ri[0],yb-ri[1]])

    # Calculate the distance to the outer radius of the ball t
    L = np.sqrt(r2@r2)-p.rb
    
    return L 
BallHitStool.terminal = True 

def BallBounce(t,u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
        
    # Get the stool locations using stickDude function
    xv,yv,sx,sy = stickDude(u)
    
    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = np.array([sx[1]-sx[0],sy[1]-sy[0]])
    
    # Calculate z that minimizes the distance
    z  = ( (xb-sx[0])*r1[0] + (yb-sy[0])*r1[1] )/( r1@r1 )
    
    # Find the closest point of impact on the stool
    if z<0:
        ri = np.array([sx[0],sy[0]])
    elif z>1:
        ri = np.array([sx[1],sy[1]])
    else:
        ri = np.array([sx[0]+z*r1[0],sy[0]+z*r1[1]])
    
    # Velocity of the stool at the impact point 
    vi = np.array([dxp-lp*np.sin(tp)-(ri[1]-yp)*dtp,
                   dyp+lp*np.cos(tp)+(ri[0]-xp)*dtp])
    
    # Velocity of the ball relative to impact point
    vbrel = np.array([dxb,dyb])-vi
    
    # Vector from the closest point of impact to the center of the ball    
    r2 = np.array([xb-ri[0],yb-ri[1]])
    u2 = r2/np.sqrt(r2@r2)

    # Delta ball velocity
    delta_vb = 2*p.COR*(u2@vbrel)
    
    # Velocity after bounce
    vBounce = -u2*delta_vb + np.array([dxb,dyb])
    
    # Obtain the player recoil states
    BounceImpulse = -p.mg*vBounce
    c = np.cos(tp)
    s = np.sin(tp)
    dRdq = np.matrix([[ 1   , 0   ],
                      [ 0   , 1   ],
                      [-s   , c   ],
                      [-c*lp,-s*lp]])
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
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
        
    # Initial assumption, there was no event
    StoolBounce = False
    FloorBounce = False
    
    # Prevent event detection if there was already one within 0.1 seconds, 
    # or if the ball is far from the stool or ground
    L = BallHitStool(t,u)
    vball = np.array((dxb,dyb))
    
    if p.odeIsEuler:
        # Integrate using Euler method
        sol = Bunch(y=np.zeros((12,p.nEulerSteps+1)),status=False)
        sol.y[:,0] = u
        for k in range(1,p.nEulerSteps+1):
            dydt = PlayerAndStool(t,sol.y[:,k-1])
            sol.y[:,k] = sol.y[:,k-1] + np.array(dydt)*dt/p.nEulerSteps
            if (t-te)>0.1 and (L<2*np.sqrt(vball@vball)*dt or yb<2*dyb*dt):
                if BallHitStool(t,sol.y[:,k])<0:
                    StoolBounce = True
                if BallHitFloor(t,sol.y[:,k])<0:   
                    FloorBounce = True
                if StoolBounce or FloorBounce:
                    te = t+k*dt
                    ue = sol.y[:,k]
                    break        
    else:
        if (t-te)>0.1 and (L<2*np.sqrt(vball@vball)*dt or yb<2*dyb*dt):
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
                elif np.size(sol.t_events[1]):
                    te = sol.t_events[1][0]+t
                    FloorBounce = True
                    
    # If an event occured, increment the counter, otherwise continue
    if StoolBounce or FloorBounce:        
        # Change ball states depending on if it was a stool or floor bounce
        if StoolBounce:
            ue[1] = ue[1]+0.001
            
            # Obtain the bounce velocity
            vBounce,vRecoil = BallBounce(te,ue)
            ue[2] = vBounce[0]
            ue[3] = vBounce[1]
            
            # Add  the recoil to the player states
            ue[8]  = ue[8]  + vRecoil[0]
            ue[9]  = ue[9]  + vRecoil[1]
            ue[10] = ue[10] + vRecoil[2]
            ue[11] = ue[11] + vRecoil[3]
            
        elif FloorBounce:
            ue[1] = 0.001
        
            # Reverse direction of the ball
            ue[2] = +p.COR*ue[2]
            ue[3] = -p.COR*ue[3]       
     
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
        x  = Y[n,4] # sol.y[0,n]
        y  = Y[n,5] # sol.y[1,n]
        l  = Y[n,6] # sol.y[2,n]
        th = Y[n,7] # sol.y[3,n]
        v  = Y[n,8] # sol.y[4,n]
    else:
        x  = inp[4]
        y  = inp[5]
        l  = inp[6]
        th = inp[7]
        v  = inp[8]
        
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
    maxy  = 1.25*np.max([u[1],u[5]+p.d+u[6]*np.cos(u[7]),12])
    diffx = 1.25*np.abs(u[0]-u[4])
    midx  = (u[0]+u[4])/2
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
    x  = Y[n,4] # sol.y[0,n]
    y  = Y[n,5] # sol.y[1,n]
    l  = Y[n,6] # sol.y[2,n]
    th = Y[n,7] # sol.y[3,n]

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