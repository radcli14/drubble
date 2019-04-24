# Import modules
import numpy as np

# Determine if you are running from a PC or from iPhone
import platform
ps = platform.system()
pm = platform.machine()
if ps == 'Windows' or ps == 'Linux' or pm == 'x86_64':
    #from pygame import mixer
    #mixer.init(frequency=44100,channels=8)
    engine = 'kivy'
elif ps == 'Darwin':    
    engine = 'ista'
    from scene import *
    import motion
    import ui
    import scene_drawing
    import sound   

# Frame rate
fs = 60

# Window size
if engine == 'kivy':
    size = width, height = 800, 500
elif engine == 'ista':
    width  = max(get_screen_size())
    height = min(get_screen_size())
    
# Color definition    
red       = (1,0,0)
green     = (0,1,0)
blue      = (0,0,1)
darkBlue  = (0,0,128.0/255.0)
white     = (1,1,1)
gray      = (160.0/255.0,160.0/255.0,160.0/255.0)
black     = (0,0,0)
pink      = (1,100.0/255.0,100.0/255.0)
skyBlue   = (135.0/255.0, 206.0/255.0, 235.0/255.0)
darkGreen = (0,120.0/255.0,0)
    
# Convert physical coordinates to pixels
def xy2p(x,y,m2p,po,w,h):
    return np.array(x)*m2p-po+w/2, np.array(y)*m2p+h/20

# Initiate pygame screen and message    
if engine == 'ista':

    def makeSplashScreen(obj):
        if gs.showedSplash:
            obj.background_color = skyBlue
            image(splash,0,0.2*height,0.8*width,0.8*height)
        else:
            k = float(obj.kSplash)/255.0
            obj.background_color = (skyBlue[0]*k,skyBlue[1]*k,skyBlue[2]*k)
            image(splash,0,0.2*height,0.8*width,0.8*height)
            if k>=1:
                gs.showedSplash = True
            
    def linePlot(x,y,m2p,po,w,h,clr,wgt):
        x,y = xy2p(x,y,m2p,po,w,h)
        stroke(clr)
        stroke_weight(wgt)
        for k in range(1,np.size(x)):
            line(x[k-1],y[k-1],x[k],y[k])
    
    def initStick(self,alph,sz,ap,ps):
        Stick = SpriteNode('figs/crossHair.png',parent=self)
        Stick.size = (sz,sz)
        Stick.anchor_point = ap
        Stick.position = ps
        Stick.x = (ps[0]-ap[0]*sz,ps[0]+(1-ap[0])*sz)
        Stick.y = (ps[1]-ap[1]*sz,ps[1]+(1-ap[1])*sz)
        Stick.cntr = ((Stick.x[0]+Stick.x[1])/2,(Stick.y[0]+Stick.y[1])/2)
        Stick.ctrl = (0,0)
        Stick.id = None
        
        Aura = SpriteNode('shp:Circle')
        #Aura = ShapeNode(circle,'white')
        #circle = ui.Path.oval (0, 0, 0.5*sz,0.5*sz)
        Aura.size = (0.5*sz,0.5*sz)
        Aura.position = Stick.cntr
        return Stick, Aura

    def touchStick(loc,stick):
        tCnd = [loc[0] > stick.x[0],
                loc[0] < stick.x[1],
                loc[1] > stick.y[0],
                loc[1] < stick.y[1]]
                    
        # Touched inside the stick
        if all(tCnd):
            x = min(max(p.tsens*(2*(loc[0]-stick.x[0])/stick.size[0] - 1),-1),1)
            y = min(max(p.tsens*(2*(loc[1]-stick.y[0])/stick.size[1] - 1),-1),1)
            
            mag = np.sqrt(x**2+y**2)
            ang = np.around(4*np.arctan2(y,x)/np.pi)*np.pi/4
            
            return (mag*np.cos(ang),mag*np.sin(ang))
        else:
            return (0,0)    
            
     
    def toggleVisibleSprites(self,boule):
        if boule:
            self.moveStick.alpha = 0.5
            self.moveAura.alpha = 0.5
            self.tiltStick.alpha = 0.5
            self.tiltAura.alpha = 0.5
            self.add_child(self.ball)
            self.add_child(self.head)
            if p.nPlayer>1:
                self.add_child(self.head1)
            self.time_label.alpha = 1
            self.dist_label.alpha = 1
            self.high_label.alpha = 1
            self.boing_label.alpha = 1
            self.score_label.alpha = 1
        else:
            self.moveStick.alpha = 0
            self.moveAura.alpha = 0
            self.tiltStick.alpha = 0
            self.tiltAura.alpha = 0
            self.ball.remove_from_parent()
            self.head.remove_from_parent()
            self.head1.remove_from_parent()
            self.time_label.alpha = 0
            self.dist_label.alpha = 0
            self.high_label.alpha = 0
            self.boing_label.alpha = 0
            self.score_label.alpha = 0

if engine == 'kivy':
    def touchStick(loc,stick):
        tCnd = [loc[0] > stick.ts_x[0],
                loc[0] < stick.ts_x[1],
                loc[1] > stick.ts_y[0],
                loc[1] < stick.ts_y[1]]
                    
        # Touched inside the stick
        if all(tCnd):
            x = min(max(p.tsens*(2.0*(loc[0]-stick.ts_x[0])/stick.size[0] - 1),-1),1)
            y = min(max(p.tsens*(2.0*(loc[1]-stick.ts_y[0])/stick.size[1] - 1),-1),1)
            
            mag = np.sqrt(x**2+y**2)
            ang = np.around(4.0*np.arctan2(y,x)/np.pi)*np.pi/4
            
            return (mag*np.cos(ang),mag*np.sin(ang))
        else:
            return (0,0)    
    
dt = 1.0/fs

if engine == 'ista':        
    def makeMarkers(xrng,m2p,po):
                
        xrng_r = np.around(xrng,-1)
        xrng_n = int((xrng_r[1]-xrng_r[0])/10.0)+1
        for k in range(0,xrng_n):
            xr = xrng_r[0]+10*k
            
            [start_x,start_y] = xy2p(xr, 0,m2p,po,width,height) 
            [end_x,end_y]     = xy2p(xr,-1,m2p,po,width,height) 
            stroke(white)
            stroke_weight(1)
            line(start_x,start_y,end_x,end_y)
            fsize = min(24,int(m2p))
            text(str(int(xr)),font_name=p.MacsFavoriteFont,font_size=fsize,x=start_x-2,y=start_y+m2p/20.0,alignment=1)
            
if engine == 'kivy':
    def makeMarkers(self,p):
        
        # xrng_r is the first and last markers on the screen, xrng_n is the 
        # number of markers
        xrng_r = np.around(p.xrng,-1)
        xrng_n = int((xrng_r[1]-xrng_r[0])/10.0)+1

        for k in range(self.nMarks):
            self.yardMark[k].text = ''
        
        for k in range(xrng_n):
            # Current yardage
            xr = int(xrng_r[0]+10*k)
            
            # Lines
            [start_x,start_y] = xy2p(xr, 0,p.m2p,p.po,self.width,self.height) 
            [end_x,end_y]     = xy2p(xr,-1,p.m2p,p.po,self.width,self.height)     
            Color(white[0],white[1],white[2],1)
            Line(points=(start_x,start_y,end_x,end_y),width=1.5)
            
            # Numbers
            strxr = str(xr)                               # String form of xr
            fsize = min(24,int(p.m2p))                    # Font size
            xypos = (int(start_x+5),self.height/20-fsize) # Position of text 
            lsize = (len(strxr)*fsize/2.0,fsize)          # Label size
            if k >= self.nMarks:
                self.yardMark.append(Label(font_size=fsize,
                                           size=lsize,pos=xypos,
                                           text=strxr,color=(1,1,1,1),
                                           halign='left',valign='top'))
                self.add_widget(self.yardMark[k])
                self.nMarks += 1
            else:
                self.yardMark[k].font_size = fsize
                self.yardMark[k].size = lsize
                self.yardMark[k].pos  = xypos
                self.yardMark[k].text = strxr

# Parameters
class Parameters:
    # Game parameters
    g   = 9.81 # Gravitational acceleration [m/s^2]
    COR = 0.8  # Coefficient of restitution
    rb  = 0.2  # Radius of the ball
       
    # Player parameters
    mc = 50.0    # Mass of player [kg]
    mg = 2.0     # Mass of stool [kg]
    m  = mc+mg   # Total mass [kg]
    x0 = 5.0     # Initial player position [m]
    y0 = 1.5     # Equilibrium position of player CG [m]
    d  = 0.3     # Relative position from player CG to stool rotation axis [m]
    l0 = 1.5     # Equilibrium position of stool
    ax = 1.0     # Horizontal acceleration [g]
    Qx = ax*m*g  # Max horizontal force [N]
    Gx = 1.5     # Control gain on Qx
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
    vx = 10.0    # Horizontal top speed [m/s]
    Cx = Qx/vx   # Horizontal damping [N-s/m]
    zy = 0.1     # Vertical damping ratio
    Cy = 2*zy*np.sqrt(Ky*m) # Vertical damping [N-s/m]
    zl = 0.2     # Arm damping ratio
    Cl = 2*zl*np.sqrt(Kl*m) # Arm damping [N-s/m]
    zt = 0.05    # Stool tilt damping ratio
    Ct = 2.0*zl*np.sqrt(Kt*m) # Tilt damping [N-m-s/rad]

    # Initial states
    q0 = np.matrix([[0.0], [y0], [l0], [0.0]])
    u0 = [0.0, rb, 0.0, 0.0, x0 , y0 , l0 ,   0.0, 0.0, 0.0, 0.0, 10.0,
          0.0, y0, l0 , 0.0, 0.0, 0.0, 0.0, -10.0]

    # Gameplay settings
    userControlled = np.array([[True, True, True, True ],
                               [False,False,False,False]]) 
    nPlayer = 1

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
    
    # Damping Matrix     
    C = np.diag([Cx,Cy,Cl,Ct])
    
    # Stiffness Matrix
    K = np.diag([0.0,Ky,Kl,Kt])
    
    # Touch Stick Sensitivity
    tsens = 1.5
    
    # Tolerance on last bounce speed before stopping motion
    dybtol = 2.0
    
    # startAngle (sa) and startSpeed (ss) initially
    sa = np.pi/4
    ss = 10.0
    
    # Parameter settings I'm using to try to improve running speed
    invM = M.I
    linearMass  = False
    nEulerSteps = 4
    timeRun     = False
    
    # Font settings
    MacsFavoriteFont = 'Papyrus' # 'jokerman' 'poorrichard' 'rockwell' 'comicsansms'
    
    # Color settings
    playerColor = (darkGreen,red)
    stoolColor  = (white,black)


p = Parameters()

class DrumBeat:
    def __init__(self):
        self.n        = 0
        self.bpm      = 105.0 # Beats per minute
        self.npb      = np.around(fs*60.0/4.0/self.bpm) # frames per beat
        self.nps      = 16.0*self.npb # frames per sequence
        #self.sequence = [[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
        #                 [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
        #                 [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
        #                 [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0]]
        self.sequence = [[1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0],
                         [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
                         [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                         [0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0]]
        if engine == 'ista':
            self.drum = ['dc/01_kick.wav',
                         'dc/04_snare2.wav',
                         'dc/06_openHat6.wav',
                         'dc/09_hiConga2.wav']
        elif engine == 'kivy':
            self.drum = []
            #self.drum.append(mixer.Sound(file='dc/kick.ogg'))
            #self.drum.append(mixer.Sound(file='dc/snare2.ogg'))
            #self.drum.append(mixer.Sound(file='dc/openHat6.ogg'))
            #self.drum.append(mixer.Sound(file='dc/hiConga1.ogg'))
            self.drum.append(SoundLoader.load('dc/kick.ogg'))
            self.drum.append(SoundLoader.load('dc/snare2.ogg'))
            self.drum.append(SoundLoader.load('dc/openHat6.ogg'))
            self.drum.append(SoundLoader.load('dc/hiConga1.ogg'))

        self.m = 4
        self.randFactor = 1.0
       
    def play_ista(self):    
        whichSequence   = np.floor(self.n/self.nps)
        whereInSequence = self.n-whichSequence*self.nps
        beat = whereInSequence/self.npb
        numDrums = max(1,gs.gameMode-2)
        if not np.mod(beat,1):
            b = int(beat)
            for k in range(numDrums):
                if self.sequence[k][b] or np.random.uniform()>self.randFactor:
                    sound.play_effect(self.drum[k])
        self.n+=1
                    
    def play_kivy(self):
        for k in range(self.m):
            if self.sequence[k][self.n] or np.random.uniform()>self.randFactor:
                self.drum[k].play() 
                
        self.n += 1
        if self.n>=16: 
            self.n = 0            
    
def varStates(obj):
    obj.xb  = obj.u[0]  # Ball distance [m]
    obj.yb  = obj.u[1]  # Ball height [m]
    obj.dxb = obj.u[2]  # Ball horizontal speed [m]
    obj.dyb = obj.u[3]  # Ball vertical speed [m]
    obj.xp  = obj.u[4:13:8]  # Player distance [m]
    obj.yp  = obj.u[5:14:8]  # Player height [m]
    obj.lp  = obj.u[6:15:8]  # Stool extension [m]
    obj.tp  = obj.u[7:16:8]  # Stool tilt [rad]
    obj.dxp = obj.u[8:17:8]  # Player horizontal speed [m/s]
    obj.dyp = obj.u[9:18:8]  # Player vertical speed [m/s]
    obj.dlp = obj.u[10:19:8] # Stool extension rate [m/s]
    obj.dtp = obj.u[11:20:8] # Stool tilt rate [rad/s]
    return obj

def unpackStates(u):
    # xp, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    xb  = u[0]  # Ball distance [m]
    yb  = u[1]  # Ball height [m]
    dxb = u[2]  # Ball horizontal speed [m]
    dyb = u[3]  # Ball vertical speed [m]
    xp  = u[4:13:8]  # Player distance [m]
    yp  = u[5:14:8]  # Player height [m]
    lp  = u[6:15:8]  # Stool extension [m]
    tp  = u[7:16:8]  # Stool tilt [rad]
    dxp = u[8:17:8]  # Player horizontal speed [m/s]
    dyp = u[9:18:8]  # Player vertical speed [m/s]
    dlp = u[10:19:8] # Stool extension rate [m/s]
    dtp = u[11:20:8] # Stool tilt rate [rad/s]
    return xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp


# Predict motion of the ball
def BallPredict(gs):
    if gs.dyb == 0 or gs.gameMode <= 2:
        # Ball is not moving, impact time is zero
        tI = 0
    elif gs.gameMode > 2 and (gs.dyb > 0) and (gs.yb < gs.yp[0] + p.d + gs.lp[0]):
        # Ball is in play, moving upward and below the stool
        # Solve for time and height at apogee
        ta = gs.dyb / p.g
        ya = 0.5 * p.g * ta ** 2

        # Solve for time the ball would hit the ground
        tI = ta + np.sqrt(2.0 * ya / p.g)
    else:
        # Ball is in play, above the stool
        # Solve for time that the ball would hit the stool
        tI = -(-gs.dyb - np.sqrt(gs.dyb ** 2 + 2.0 * p.g * (gs.yb - gs.yp[0] - p.d - gs.lp[0]))) / p.g

    if np.isnan(tI):
        tI = 0

    # Solve for position that the ball would hit the stool
    xI = gs.xb + gs.dxb * tI
    yI = gs.yb + gs.dyb * tI - 0.5 * p.g * tI ** 2

    # Solve for time that the ball would hit the ground
    tG = -(-gs.dyb - np.sqrt(gs.dyb ** 2 + 2.0 * p.g * gs.yb)) / p.g

    # Solve for the arc for the next 1.2 seconds, or until ball hits ground
    T = np.linspace(0, min(1.2, tG), 20)
    xTraj = gs.xb + gs.dxb * T
    yTraj = gs.yb + gs.dyb * T - 0.5 * p.g * T ** 2

    # Time until event
    timeUntilBounce = tI;
    tI = timeUntilBounce + gs.t

    # Output variables
    # xI = Ball distance at impact [m]
    # yI = Ball height at impact [m]
    # tI = Time at impact [s]
    # xTraj = Ball trajectory distances [m]
    # yTraj = Ball trajectory heights [m]
    return xI, yI, tI, xTraj, yTraj, timeUntilBounce

class GameState:
    # Initiate the state variables as a list, and as individual variables
    def __init__(self,u0):
        # Define Game Mode
        # 0 = Quit
        # 1 = Splash screen
        # 2 = Options screen
        # 3 = In game, pre-angle set
        # 4 = In game, angle set
        # 5 = In game, distance set
        # 6 = In game
        # 7 = Game over, resume option
        # 8 = Game over, high scores
        self.gameMode = 1
        self.showedSplash = False
        
        # Determine the control method, and initialize ctrl variable
        if engine == 'kivy':
            self.ctrlMode = 'keys'
            self.ctrlFunc = 0
        elif engine == 'ista':
            #self.ctrlMode = 'motion'
            #self.ctrlFunc = 1
            self.ctrlMode = 'vStick'
            self.ctrlFunc = 2
        self.ctrl = [0,0,0,0]
        
        # Timing
        self.t  = 0
        self.n  = 0
        self.te = 0
        
        # State variables
        self.u  = u0[:]
        self = varStates(self)
       
        # Event states
        self.ue = u0[:]
        self.xI,self.yI,self.tI,self.xTraj,self.yTraj,self.timeUntilBounce = BallPredict(self)
        
        # Angle and Speed Conditions
        self.startAngle = p.sa
        self.startSpeed = p.ss
        self.phase      = 0
        
        # Stuck condition
        self.Stuck = False
         
    # Get control input from external source
    def setControl(self,keyPush=np.zeros(8),
                   moveStick=[0,0],tiltStick=[0,0],
                   g=[0,0,0],a=[0,0,0]):
        
        if self.ctrlFunc == 0:
            # Key press control
            self.ctrl = [keyPush[1]-keyPush[0],keyPush[2]-keyPush[3],
                         keyPush[4]-keyPush[5],keyPush[6]-keyPush[7]]
            
        elif self.ctrlFunc == 1:
            # Motion control scale factors
            gThreshold = 0.05
            slope = 5.0
            aScale = 2.0

            # Run left/right
            if g[1]>gThreshold:
                self.ctrl[0] = -min(slope*(g[1]-gThreshold),1)
            elif g[1]<-gThreshold:
                self.ctrl[0] = -max(slope*(g[1]+gThreshold),-1)
            else:
                self.ctrl[0]
                
            # Push up/down    
            if a[1]>0:
                self.ctrl[1] = min(aScale*a[1],1)
            else:
                self.ctrl[1] = max(aScale*a[1],-1)
                    
        elif self.ctrlFunc == 2:
            # Virtual stick control
            self.ctrl = [moveStick[0],moveStick[1],tiltStick[1],-tiltStick[0]]
        
    # Execute a simulation step of duration dt    
    def simStep(self):
        # Increment n 
        self.n += 1
        
        # Active player
        pAct = np.mod(stats.stoolCount,p.nPlayer)
        
        # Initial assumption, there was no event
        self.StoolBounce = False
        self.FloorBounce = False
        
        # Prevent event detection if there was already one within 0.1 seconds, 
        # or if the ball is far from the stool or ground
        L = BallHitStool(self.t,self.u,pAct)       # Distance to stool
        vBall = np.array((self.dxb,self.dyb)) # Velocity
        sBall = np.linalg.norm(vBall)         # Speed
        
        ## Integrate using Euler method
        # Initialize state variables
        U = np.zeros((20,p.nEulerSteps+1))
        U[:,0] = self.u
        for k in range(1,p.nEulerSteps+1):
            # Increment time
            self.t += dt/p.nEulerSteps
            
            # Calculate the derivatives of states w.r.t. time
            dudt = PlayerAndStool(self.t,U[:,k-1])
            
            # Calculate the states at the next step
            U[:,k] = U[:,k-1] + np.array(dudt)*dt/p.nEulerSteps
            
            # Check for events
            if (self.t-self.te)>0.1: 
                if BallHitStool(self.t,U[:,k],pAct)<0.0:
                    self.StoolBounce = True
                if BallHitFloor(self.t,U[:,k])<0.0:
                    self.FloorBounce = True
                if self.StoolBounce or self.FloorBounce:
                    self.te = self.t
                    self.ue = U[:,k] 
                    tBreak = k*dt/p.nEulerSteps
                    break 
        
        # If an event occured, increment the counter, otherwise continue
        if self.StoolBounce or self.FloorBounce:        
            # Change ball states depending on if it was a stool or floor bounce
            if self.StoolBounce:
                # Obtain the bounce velocity
                vBounce,vRecoil = BallBounce(self,np.mod(stats.stoolCount,p.nPlayer))
                self.ue[2] = vBounce[0]
                self.ue[3] = vBounce[1]
                
                # Add  the recoil to the player 
                self.ue[8+pAct*8]  = self.ue[8+pAct*8]  + vRecoil[0,0]
                self.ue[9+pAct*8]  = self.ue[9]  + vRecoil[0,1]
                self.ue[10+pAct*8] = self.ue[10] + vRecoil[0,2]
                self.ue[11+pAct*8] = self.ue[11] + vRecoil[0,3]
                
            elif self.FloorBounce:
                # Reverse direction of the ball
                self.ue[2] = +p.COR*self.ue[2]
                self.ue[3] = -p.COR*self.ue[3]     
                
         
            # Re-initialize from the event states
            self.t += dt-tBreak
            dudt = PlayerAndStool(self.t,self.ue)
            self.u = self.ue + np.array(dudt)*(dt-tBreak)
            
            # Stuck
            if np.sqrt(self.u[2]**2+self.u[3]**2)<p.dybtol and self.u[1]<1:
                self.Stuck = True
        else:   
            # Update states
            self.u = U[:,-1]  
        
        if self.Stuck:
            self.u[1] = p.rb
            self.u[2] = 0.9999*self.u[2]
            self.u[3] = 0
        
        # Generate the new ball trajectory prediction line
        if self.StoolBounce or self.FloorBounce or self.gameMode<7:    
            # Predict the future trajectory of the ball
            self.xI,self.yI,self.tI,self.xTraj,self.yTraj,self.timeUntilBounce = BallPredict(self)

        # Stop the ball from moving if the player hasn't hit space yet
        if self.gameMode<6:
            self.t = 0
            self.n = 0
            self.u[0] = p.u0[0]
            self.u[1] = p.u0[1]
        # Named states    
        self   = varStates(self)

    def setAngleSpeed(self):
        if self.gameMode == 4:
            self.startAngle = 0.25*np.pi*(1 + 0.75*np.sin(self.phase))
        if self.gameMode == 5:
            self.startSpeed = p.ss*(1 + 0.75*np.sin(self.phase))
        if self.gameMode == 4 or self.gameMode == 5:
            self.phase += 3*dt
            self.u[2] = self.startSpeed*np.cos(self.startAngle)
            self.u[3] = self.startSpeed*np.sin(self.startAngle)


gs = GameState(p.u0)

def cycleModes(gs,stats):
    # Exit splash screen
    if gs.gameMode == 1:
        gs.gameMode += 1
        return
    
    # Exit options screen 
    if gs.gameMode == 2:
        # Reset game
        stats.__init__()
        gs.__init__(p.u0)
        gs.gameMode = 3
        return
        
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
        gs.__init__(p.u0)
        gs.gameMode = 3
        return

class GameScore:
    # Initiate statistics as zeros
    def __init__(self):
        self.t = 0
        self.n = 0
        self.stoolCount = 0
        self.stoolDist  = 0
        self.maxHeight  = 0
        self.floorCount = 0
        self.score      = 0
        self.averageStepTime = 0
        
    # Update statistics for the current game state    
    def update(self):
        self.t = gs.t
        self.n = gs.n
        if gs.StoolBounce and self.stoolDist<gs.xb:
            self.stoolDist = gs.xb
        if self.maxHeight<gs.yb and self.stoolCount>0:
            self.maxHeight = gs.yb   
        self.stoolCount += gs.StoolBounce
        self.floorCount += gs.FloorBounce
        self.score = int(self.stoolDist*self.maxHeight*self.stoolCount)

# Equation of Motion
def PlayerAndStool(t,u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    # Initialize output
    du = np.zeros(20)
    du[0:4] = [dxb,dyb,0,-p.g] # Ball velocities and accelerations
    
    # Loop over players
    for k in range(p.nPlayer):
        # Create player state vectors
        q  = np.matrix([[xp[k]],[yp[k]],[lp[k]],[tp[k]]])
        dq = np.matrix([[dxp[k]],[dyp[k]],[dlp[k]],[dtp[k]]])
    
        # Sines and cosines of the stool angle
        s = np.sin(tp[k])
        c = np.cos(tp[k])
        
        # Mass Matrix
        if not p.linearMass:     
            M = np.matrix([[   p.m       ,    0        ,-p.mg*s,-p.mg*lp[k]*c ],
                           [    0        ,   p.m       , p.mg*c,-p.mg*lp[k]*s ],
                           [-p.mg*s      ,  p.mg*c     , p.mg  ,   0          ],
                           [-p.mg*lp[k]*c,-p.mg*lp[k]*s,   0   , p.mg*lp[k]**2]])
        
        # Centripetal [0,1] and Coriolis [3] Force Vector
        D = np.matrix([[-p.mg*dlp[k]*dtp[k]*c + p.mg*lp[k]*dtp[k]*dtp[k]*s], 
                       [-p.mg*dlp[k]*dtp[k]*s +p.mg*lp[k]*dtp[k]*dtp[k]*c], 
                       [0.0],
                       [2.0*p.mg*dtp[k]]])
        
        # Gravitational Force Vector
        G = np.matrix([[ 0.0          ],
                       [ p.m*p.g      ],
                       [ p.mg*p.g*c   ],
                       [-p.mg*p.g*lp[k]*s]])         
    
        # Fix the time, if supplied as tspan vector
        if np.size(t)>1:
            t = t[0]       
        
        # Control inputs form the generalized forces
        Q, Bx, By, Bl, Bth, ZEM, wantAngle, xdiff, ydiff = ControlLogic(t,u,k)
        
        # Equation of Motion
        RHS = -p.C*dq-p.K*q+p.K*p.q0-D-G+Q
        if p.linearMass:
            ddq = p.invM*RHS
        else:
            ddq = M.I*RHS
        
        # Output State Derivatives
        i1 = k*8+4
        i2 = k*8+12
        du[i1:i2] = [dxp[k],dyp[k],dlp[k],dtp[k],ddq[0,0],ddq[1,0],ddq[2,0],ddq[3,0]] # Player velocities and accelerations
    
    return du.tolist()

def ctrl2keyPush(gs):
    keyPush = np.zeros(8)
    if gs.ctrl[0]<0:
        keyPush[0] = -gs.ctrl[0]
    elif gs.ctrl[0]>0:
        keyPush[1] = gs.ctrl[0]
    if gs.ctrl[1]>0:
        keyPush[2] = gs.ctrl[1]
    elif gs.ctrl[1]<0:
        keyPush[3] = -gs.ctrl[1]    
    if gs.ctrl[2]>0:
        keyPush[4] = gs.ctrl[2]
    elif gs.ctrl[2]<0:
        keyPush[5] = -gs.ctrl[2]
    if gs.ctrl[3]>0:
        keyPush[6] = gs.ctrl[3]
    elif gs.ctrl[3]<0:
        keyPush[7] = -gs.ctrl[3]  
    return keyPush

def kvUpdateKey(keyPush,keycode,val):
    if keycode[1] == 'w':
        keyPush[4] = val
    elif keycode[1] == 's':
        keyPush[5] = val
    elif keycode[1] == 'a':
        keyPush[6] = val
    elif keycode[1] == 'd':
        keyPush[7] = val
    elif keycode[1] == 'up':
        keyPush[2] = val
    elif keycode[1] == 'down':
        keyPush[3] = val
    elif keycode[1] == 'left':
        keyPush[0] = val
    elif keycode[1] == 'right':
        keyPush[1] = val
    return keyPush

def ControlLogic(t,u,k):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    # Control horizontal acceleration based on zero effort miss (ZEM)
    # Subtract 1 secoond to get there early, and subtract 0.01 m to keep the
    # ball moving forward 
    ZEM = (gs.xI+10.0*(p.nPlayer-1-np.mod(stats.stoolCount,2))-0.1) - xp[k] - dxp[k]*np.abs(gs.timeUntilBounce-1)
    if p.userControlled[k,0]:
        if gs.ctrl[0] == 0:
            try:
                Bx = -scs.erf(dxp[k])
            except:
                Bx = -np.sign(dxp[k])
        else:
            Bx = gs.ctrl[0]
    else:
        Bx = p.Gx*ZEM
        if Bx>1.0:
            Bx = 1.0
        elif (Bx<-1) or (gs.timeUntilBounce<0 and gs.timeUntilBounce>0):
            Bx = -1.0
    
    # Control leg extension based on timing, turn on when impact in <0.2 sec
    if p.userControlled[k,1]:
        By = gs.ctrl[1]
    else:
        if (gs.timeUntilBounce<0.6) and (gs.timeUntilBounce>0.4):
            By = -1.0
        elif np.abs(gs.timeUntilBounce)<0.2:       
            By = 1.0
        else:
            By = 0.0
    
    # Control arm extension based on timing, turn on when impact in <0.2 sec
    if p.userControlled[k,2]:
        Bl = gs.ctrl[2]
    else:
        Bl = np.abs(gs.timeUntilBounce)<0.2
    
    # Control stool angle by pointing at the ball
    xdiff = xb-xp[k] # Ball distance - player distance
    ydiff = yb-yp[k]-p.d
    wantAngle = np.arctan2(-xdiff,ydiff)
    if p.userControlled[k,3]:
        Bth = gs.ctrl[3]
    else:
        Bth = p.Gt*(wantAngle-tp[k])
        if Bth>1.0:
            Bth = 1.0
        elif Bth<-1 or (gs.timeUntilBounce<0.017) and (gs.timeUntilBounce>0):
            Bth = -1.0
        
    Q = np.matrix([[Bx*p.Qx],[By*p.Qy],[Bl*p.Ql],[Bth*p.Qt]])    
    
    return Q, Bx, By, Bl, Bth, ZEM, wantAngle, xdiff, ydiff    

def BallHitFloor(t,u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u) 
    return yb-p.rb
BallHitFloor.terminal = True

def BallHitStool(t,u,k):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
        
    # Get the stool locations using stickDude function
    xv,yv,sx,sy = stickDude(u,k)
    
    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = np.array([sx[1]-sx[0],sy[1]-sy[0]])
    
    # Calculate z that minimizes the distance
    z  = ( (xb-sx[0])*r1[0] + (yb-sy[0])*r1[1] )/(r1.dot(r1))
    
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
    L = np.sqrt(r2.dot(r2))-p.rb
    
    return L 
BallHitStool.terminal = True 

def BallBounce(gs,k):
    # Get the stool locations using stickDude function
    xv,yv,sx,sy = stickDude(gs.u,k)
    
    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = np.array([sx[1]-sx[0],sy[1]-sy[0]])
    
    # Calculate z that minimizes the distance
    z  = ( (gs.xb-sx[0])*r1[0] + (gs.yb-sy[0])*r1[1] )/(r1.dot(r1))
    
    # Find the closest point of impact on the stool
    if z<0:
        ri = np.array([sx[0],sy[0]])
    elif z>1:
        ri = np.array([sx[1],sy[1]])
    else:
        ri = np.array([sx[0]+z*r1[0],sy[0]+z*r1[1]])
    
    # Velocity of the stool at the impact point 
    vi = np.array([gs.dxp-gs.lp[k]*np.sin(gs.tp[k])-(ri[1]-gs.yp[k])*gs.dtp[k],
                   gs.dyp[k]+gs.lp[k]*np.cos(gs.tp[k])+(ri[0]-gs.xp[k])*gs.dtp[k]])
    
    # Velocity of the ball relative to impact point
    vbrel = np.array([gs.dxb,gs.dyb])-vi
    
    # Vector from the closest point of impact to the center of the ball    
    r2 = np.array([gs.xb-ri[0],gs.yb-ri[1]])
    u2 = r2/np.sqrt(r2.dot(r2))

    # Delta ball velocity
    delta_vb = 2.0*p.COR*u2.dot(vbrel)
    
    # Velocity after bounce
    vBounce = -u2*delta_vb + np.array([gs.dxb,gs.dyb])
    
    # Obtain the player recoil states
    BounceImpulse = -p.mg*vBounce
    c = np.cos(gs.tp[k])
    s = np.sin(gs.tp[k])
    dRdq = np.array([[ 1.0    , 0.0 ],
                     [ 0.0    , 1.0 ],
                     [-s      , c   ],
                     [-c*gs.lp[k],-s*gs.lp[k]]])
    Qi = dRdq.dot(BounceImpulse)
    vRecoil = np.dot(p.invM,Qi)
    return vBounce, vRecoil

# Solves for the location of the knee or elbow based upon the two other 
# end-points of the triangle 
def ThirdPoint(P0,P1,L,SGN):

    Psub = [P0[0]-P1[0],P0[1]-P1[1]]
    Padd = [P0[0]+P1[0],P0[1]+P1[1]]
    P2 = [Padd[0]/2.0, Padd[1]/2.0]
    d = np.linalg.norm(Psub) # Distance between point P0,P1

    if d > L:
        P3 = P2
    else:
        a  = (d**2)/2.0/d # Distance to mid-Point
        h  = np.sqrt( (L**2)/4.0 - a**2 )
        x3 = P2[0] + h*SGN*Psub[1]/d
        y3 = P2[1] - h*SGN*Psub[0]/d
        P3 = [x3,y3]
    return P3

# Solve for the vertices that make up the stick man and stool
def stickDude(inp,k):
    k8=k*8
    # Get the state variables
    if type(inp)==int:
        # States at time t[n]
        x  = Y[n,4+k8] 
        y  = Y[n,5+k8] 
        l  = Y[n,6+k8] 
        th = Y[n,7+k8] 
        v  = Y[n,8+k8] 
    elif type(inp)==list or type(inp)==np.ndarray:
          # States from u 
        x  = inp[4+k8]
        y  = inp[5+k8]
        l  = inp[6+k8]
        th = inp[7+k8]
        v  = inp[8+k8]
    elif type(inp)==GameState:
        # States from gs
        x  = inp.xp[k]
        y  = inp.yp[k]
        l  = inp.lp[k]
        th = inp.tp[k]
        v  = inp.dxp[k]
    else:
        # Wasn't able to identify type, tying states from gs
        x  = inp.xp[k]
        y  = inp.yp[k]
        l  = inp.lp[k]
        th = inp.tp[k]
        v  = inp.dxp[k]
    #print('stickDude x=%f' % x)
    s = np.sin(th)
    c = np.cos(th)
        
    # Right Foot [rf] Left Foot [lf] Positions
    rf = [x-0.25+(v/p.vx)*np.sin(1.5*x+3.0*np.pi/2.0),
          0.2*(v/p.vx)*(1+np.sin(1.5*x+3.0*np.pi/2.0))]
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
    rh = [sx[7], sy[7]] 
    lh = [sx[6], sy[6]] 
    
    # Right Elbow [re] Left Elbow [le] Position
    re = ThirdPoint(sh,rh,1,1)
    le = ThirdPoint(sh,lh,1,-1)
    
    # Plotting vectors
    xv = [rf[0],rk[0],w[0],lk[0],lf[0],lk[0],w[0],sh[0],re[0],rh[0],re[0],sh[0],le[0],lh[0]]
    yv = [rf[1],rk[1],w[1],lk[1],lf[1],lk[1],w[1],sh[1],re[1],rh[1],re[1],sh[1],le[1],lh[1]]
    
    return xv,yv,sx,sy

# Solve for the x and y ranges to include in the plot, scale factors to 
# convert from meters to pixels, and pixel offset to the center line
# Ratio refers to normalized positions in the window on the scale [0 0 1 1]
def setRanges(u):
    maxy  = 1.25*np.max([u[1],u[5]+p.d+u[6]*np.cos(u[7]),3.0])
    diffx = 1.25*np.abs(u[0]-u[4])
    midx  = (u[0]+u[4])/2.0
    if diffx>2*(maxy+1):
        xrng = midx-0.5*diffx, midx+0.5*diffx
        yrng = -1.0, 0.5*(diffx-0.5)
    else:
        xrng = midx-maxy-0.5, midx+maxy+0.5
        yrng = -1.0, maxy

    MeterToPixel = width/(xrng[1]-xrng[0])
    MeterToRatio = 1.0/(xrng[1]-xrng[0])
    PixelOffset  = (xrng[0]+xrng[1])/2.0*MeterToPixel
    RatioOffset  = (xrng[0]+xrng[1])/2.0*MeterToRatio
    return xrng, yrng, MeterToPixel, PixelOffset, MeterToRatio, RatioOffset
 
def intersperse(list1,list2):    
    result = [None]*(len(list1)+len(list2))
    result[::2] = list1
    result[1::2] = list2    
    return result

class playerLines():
    def __init__(self,pnum):
        self.pnum = pnum
        self.width = width
        self.height = height
        self.update(gs)
        
    def update(self,gs):
        # Get the player stick figure
        self.xv, self.yv, self.sx, self.sy = stickDude(gs,self.pnum)
        
        # Get ranges for drawing the player and ball
        self.xrng, self.yrng, self.m2p, self.po, m2r, ro = setRanges(gs.u)
        
        # Convert to pixels
        self.player_x,self.player_y = xy2p(self.xv,self.yv,self.m2p,self.po,
                                           self.width,self.height)
        self.stool_x,self.stool_y = xy2p(self.sx,self.sy,self.m2p,self.po,
                                         self.width,self.height)
        
        # Convert to format used for Kivy line
        self.player = intersperse(self.player_x,self.player_y)
        self.stool  = intersperse(self.stool_x,self.stool_y)


# Below this line are the functions I created when I started demoDrubble,
# these are basically obsolete, eventually will be deleted
defObsoleteDemoFuncs = False
if defObsoleteDemoFuncs:

    # Define the bunch class
    class Bunch:
        def __init__(self, **kwds):
            self.__dict__.update(kwds)

    ### CHECK WHETHER THESE OR NEEDED FOR ISTA, PROBABLY SWITCH TO THE NEW BACKGROUND CLASS
    def makeBackgroundImage():
        # Draw the ESA, Big Chair, River, and USS Barry
        drawBackgroundImage(bg0, bg0_rect, -0.25, -5, m2p)


    def drawBackgroundImage(img, rect, xpos, ypos, m2p):
        left = width * (-(gs.xb + gs.xp[0]) / 120.0 + xpos)
        bottom = -gs.yb * 5.0 + ypos + height / 20.0
        image(bg0, left, bottom, rect[0], rect[1])

    def showMessage(msgText):
        font = pygame.font.SysFont(p.MacsFavoriteFont, int(height / 32))
        if type(msgText) == str:
            msgRend = font.render(msgText, True, black)
            screen.blit(msgRend, (0.05 * width, 0.1 * height))
        elif type(msgText) == list:
            for n in range(np.size(msgText)):
                msgRend = font.render(msgText[n], True, black)
                screen.blit(msgRend, (0.05 * width, 0.1 * height + n * 36))


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

    # Used for debuggin the output of the "Ball Hit" functions, but unused now
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
        xrng, yrng, m2p, po, m2r, ro = setRanges(Y[n,:])
        ax.set_xlim(xrng)
        ax.set_ylim(yrng)
        
        return LN, HD, GD, ST, BL, BA,
