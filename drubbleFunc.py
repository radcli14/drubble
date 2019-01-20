# Import modules
# import os
# import time
import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_pdf import PdfPages

# Define the bunch class
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

# Parameters
def parameters():
    g  = 9.81 # Gravitational acceleration [m/s^2]
    
    # Player parameters
    mc = 50    # Mass of player [kg]
    mg = 2     # Mass of stool [kg]
    m  = mc+mg # Total mass
    y0 = 1.5   # Equilibrium position of player CG
    d  = 0.3   # Relative position from player CG to stool rotation axis
    l0 = 1.5   # Equilibrium position of stool
    ax = 1     # Horizontal acceleration [g]
    Qx = ax*m*g;
    fy = 0.8 # vertical frequency
    Ky = m*(fy*2*np.pi)**2
    Qy = Ky*0.3 # Leg strength
    fl = 1.2 # Stool extension frequency
    Kl = mg*(fl*2*np.pi)**2
    Ql = Kl*0.3 # Arm strength
    ft = 0.5 # Stool tilt frequency
    Kt = (mg*l0*l0)*(ft*2*np.pi)**2
    Qt = 0.3*Kt # Tilt strength
    vx = 10 # Horizontal top speed [m/s]
    Cx = Qx/vx
    zy = 0.1 # Vertical damping ratio
    Cy = 2*zy*np.sqrt(Ky*m)
    zl = 0.2 # Stool extension damping ratio
    Cl = 2*zl*np.sqrt(Kl*m)
    zt = 0.05 # Stool tilt damping ratio
    Ct = 2*zl*np.sqrt(Kt*m)
    
    # Stool parameters
    xs = np.array([-0.2 ,  0.2 ,  0.14, 
                    0.16, -0.16,  0.16, 
                    0.18, -0.18,  0.18,  
                    0.2 ,  0.14, -0.14, -0.2])
    ys = np.array([  0 ,  0  ,  0  , 
                   -0.3, -0.3, -0.3, 
                   -0.6, -0.6, -0.6,
                   -0.9,  0  ,   0 ,  -0.9 ])
    
    p = Bunch(g=g,mc=mc,mg=mg,m=m,y0=y0,d=d,l0=l0,ax=ax,Qx=Qx,Qy=Qy,Ql=Ql,
              Qt=Qt,fy=fy,Ky=Ky,fl=fl,Kl=Kl,ft=ft,Kt=Kt,vx=vx,Cx=Cx,zy=zy,
              Cy=Cy,zl=zl,Cl=Cl,zt=zt,Ct=Ct,xs=xs,ys=ys)
    return p 

# Predict
def BallPredict(u):
    x  = u[8]  # Ball horizontal position
    y  = u[9]  # Ball vertical position
    dx = u[10] # Ball horizontal velocity
    dy = u[11] # Ball vertical velocity
    
    # Solve for time that the ball would hit the stool
    tb = -(-dy - np.sqrt(dy**2 + p.g*(y-p.y0-p.d-p.l0) ))/p.g
    
    # Solve for position that the ball would hit the stool
    xb = x+dx*tb
    yb = y+dy*tb-0.5*p.g*tb**2
    
    return xb,yb,tb

# Equation of Motion
def PlayerAndStool(t,u):
    # Resolve the States
    l = u[2]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    th = u[3]
    s = np.sin(th)
    c = np.cos(th)
    dl = u[6]
    dth = u[7]
    q = np.matrix([u[0],u[1],u[2],u[3]])
    dq = np.matrix([u[4],u[5],u[6],u[7]])
    q = q.T
    dq = dq.T

    # Mass Matrix
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
    
    # Coriolis and Centripetal Force Vector
    D = np.matrix([[-2*p.mg*dl*dth*c+p.mg*l*dth*dth*s], 
                   [-2*p.mg*dl*dth*s+p.mg*l*dth*dth*c], 
                   [0],
                   [0]])
    
    # Gravitational Force Vector
    G = np.matrix([[0],
                   [p.m*p.g],
                   [p.mg*p.g*c],
                   [-p.mg*p.g*l*s]])         

    # Fix the time, if supplied as tspan vector
    if np.size(t)>1:
        t = t[0]
        
    # Control horizontal acceleration based on zero effort miss (ZEM)
    # Subtract 1 secoond to get there early    
    ZEM = xb - u[0] - u[4]*np.abs(tb-t-1)
    #print(ZEM)
    Bx = 1.0*ZEM
    if Bx>1:
        Bx = 1
    elif Bx<-1:
        Bx = -1
    
    # Control leg extension based on timing, turn on when impact in <0.25 sec
    By = np.abs(tb-t)<0.25
    
    # Control arm extension based on timing, turn on when impact in <0.25 sec
    Bl = np.abs(tb-t)<0.25
    
    # Control stool angle by pointing at the ball
    B  = np.matrix([[Bx],[0],[0],[0]])
    xdiff = u[8]-u[0]
    ydiff = u[9]-u[1]-p.d
    #wantAngle = np.arctan2(xdiff,ydiff)
    wantAngle = np.arctan(xdiff/ydiff)
    Bth = 5.0*(th - wantAngle)
    if Bth>1:
        Bth = 1
    elif Bth<-1:
        Bth = -1
    
    # Multiply Q and B to get the control forces
    B  = np.matrix([[Bx],[By],[Bl],[Bth]])
    QQ = np.multiply(Q,B)
    
    # Equation of Motion
    RHS = -C*dq-K*q+K*q0-D-G+QQ
    ddq = M.I*RHS
    
    # Output State Derivatives
    du = [u[4],u[5],u[6],u[7],ddq[0,0],
          ddq[1,0],ddq[2,0],ddq[3,0],
          u[10],u[11],0,-p.g]
    return du

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

def stickDude(n):
    # States at time t[n]
    x = sol.y[0,n]
    y = sol.y[1,n]
    l = sol.y[2,n]
    th = sol.y[3,n]
    s = np.sin(th)
    c = np.cos(th)
    v = sol.y[4,n]

    # Right Foot [rf] Left Foot [lf] Positions
    rf = [x+0.25+(v/p.vx)*np.sin(1.5*x+3*np.pi/2), 
          0.2*(v/p.vx)*(1+np.sin(1.5*x+3*np.pi/2))]
    lf = [x-0.25+(v/p.vx)*np.cos(1.5*x), 
          0.2*(v/p.vx)*(1+np.cos(1.5*x))]
    
    # Waist Position
    w = [x,y-p.d]
    
    # Right Knee [rk] Left Knee [lk] Positions
    rk = ThirdPoint(w,rf,p.y0-p.d,2*((sol.y[4,n]>-2)-0.5))
    lk = ThirdPoint(w,lf,p.y0-p.d,2*((sol.y[4,n]>2)-0.5))
    
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
    
    return xv,yv,rf,lf,sx,sy

def initPlots():
    LN, = plt.plot([], [], '-g', animated=True) # Stick figure
    RF, = plt.plot([], [], '<k', animated=True) # Right foot
    LF, = plt.plot([], [], '>k', animated=True) # Left foot
    HD, = plt.plot([], [], 'go', animated=True) # Head
    GD, = plt.plot([], [], '-b', animated=True) # Ground
    ST, = plt.plot([], [], '-r', animated=True) # Stool
    BL, = plt.plot([], [], 'mo', animated=True) # Ball
    return LN, RF, LF, HD, GD, ST, BL,

def init():
    ax.set_xlim(-1,11)
    ax.set_ylim(-1,5)
    #ax.set_aspect('equal')
    return LN, RF, LF, HD, GD, ST, BL,

def animate(n):
    # Get the plotting vectors using stickDude function
    xv,yv,rf,lf,sx,sy = stickDude(n)

    # Get state variables
    x  = sol.y[0,n]
    y  = sol.y[1,n]
    l  = sol.y[2,n]
    th = sol.y[3,n]

    # Update the plot
    LN.set_data(xv, yv)
    RF.set_data(rf[0],rf[1])
    LF.set_data(lf[0],lf[1])
    HD.set_data(x,y+p.d*1.6)
    GD.set_data([x-100, x+100],[0,0])
    ST.set_data(sx,sy)
    BL.set_data(sol.y[8,n],sol.y[9,n])
    
    # Update Axis Limits
    maxy  = 1.25*np.max([sol.y[9,n],y+p.d+l*np.cos(th)])
    diffx = 1.25*np.abs(x-sol.y[8,n])
    midx  = (x+sol.y[8,n])/2
    if diffx>2*(maxy+1):
        xrng = midx-0.5*diffx, midx+0.5*diffx
        yrng = -1, 0.5*(diffx-0.5)
    else:
        xrng = midx-maxy-0.5, midx+maxy+0.5
        yrng = -1, maxy
    ax.set_xlim(xrng)
    ax.set_ylim(yrng)
    
    return LN, RF, LF, HD, GD, ST, BL,