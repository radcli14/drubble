# Import modules
# import os
# import time
import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
    fl = 1.2 # Stool extension frequency
    Kl = mg*(fl*2*np.pi)**2
    ft = 0.5 # Stool tilt frequency
    Kt = (mg*l0*l0)*(ft*2*np.pi)**2
    vx = 10 # Horizontal top speed [m/s]
    Cx = Qx/vx
    zy = 0.1 # Vertical damping ratio
    Cy = 2*zy*np.sqrt(Ky*m)
    zl = 0.2 # Stool extension damping ratio
    Cl = 2*zl*np.sqrt(Kl*m)
    zt = 0.05 # Stool tilt damping ratio
    Ct = 2*zl*np.sqrt(Kt*m)
    
    # Stool parameters
    xs = np.array([-0.2, 0.2, 0.14, 
                    0.16, -0.16, 0.16, 
                    0.18, -0.18, 0.18,  
                    0.2, 0.15, -0.15, -0.2])
    ys = np.array([  0 ,  0  ,  0  , 
                   -0.3, -0.3, -0.3, 
                   -0.6, -0.6, -0.6,
                   -0.9,  0  ,   0  ,  -0.9 ])
    
    #p = {'g':g,'mc':mc,'mg':mg,'m':m,'y0':y0,'d':d,'l0':l0,'ax':ax,'Qx':Qx,
    #     'fy':fy,'Ky':Ky,'fl':fl,'Kl':Kl,'ft':ft,'Kt':Kt,'vx':vx,'Cx':Cx,
    #     'zy':zy,'Cy':Cy,'zl':zl,'Cl':Cl,'zt':zt,'Ct':Ct}
    p = Bunch(g=g,mc=mc,mg=mg,m=m,y0=y0,d=d,l0=l0,ax=ax,Qx=Qx,fy=fy,Ky=Ky,
              fl=fl,Kl=Kl,ft=ft,Kt=Kt,vx=vx,Cx=Cx,zy=zy,Cy=Cy,zl=zl,Cl=Cl,
              zt=zt,Ct=Ct,xs=xs,ys=ys)
    return p 

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

    # Equation of Motion
    RHS = -C*dq-K*q+K*q0-D-G+Q
    ddq = M.I*RHS
    
    # Output State Derivatives
    du = [u[4],u[5],u[6],u[7],ddq[0,0],ddq[1,0],ddq[2,0],ddq[3,0]]
    return du

def stickDude(n):
    # States at time t[n]
    x = sol.y[0,n]
    y = sol.y[1,n]
    l = sol.y[2,n]
    th = sol.y[3,n]
    s = np.sin(th)
    sp = np.sin(th+0.25)
    sm = np.sin(th-0.25)
    c = np.cos(th)
    cp = np.cos(th+0.25)
    cm = np.cos(th-0.25)
    v = sol.y[4,n]

    # Right Foot [rf] Left Foot [lf] Positions
    rf = [x+0.15+(v/p.vx)*np.sin(1.5*x+3*np.pi/2), 
          0.2*(v/p.vx)*(1+np.sin(1.5*x+3*np.pi/2))]
    lf = [x-0.15+(v/p.vx)*np.cos(1.5*x), 
          0.2*(v/p.vx)*(1+np.cos(1.5*x))]
    
    # Right Knee [rk] Left Knee [lk] Positions
    
    # Waist Position
    w = [x,y-p.d]
    
    # Shoulder Position
    sh = [x,y+p.d]
    
    # Stool Position
    sx = x+p.xs*c-(l+p.ys)*s
    sy = y+p.d+(l+p.ys)*c+p.xs*s
    
    # Right Hand [rh] Left Hand [lh] Position 
    rh = [sx[7], sy[7]] # [x-0.5*l*sp,y+p.d+0.5*l*cp]
    lh = [sx[6], sy[6]] # [x-0.5*l*sm,y+p.d+0.5*l*cm]
    
    # Plotting vectors
    xv = [rf[0],w[0],lf[0],w[0],sh[0],rh[0],sh[0],lh[0],sh[0]]
    yv = [rf[1],w[1],lf[1],w[1],sh[1],rh[1],sh[1],lh[1],sh[1]]
    
    return xv,yv,rf,lf,sx,sy

def initPlots():
    LN, = plt.plot([], [], '-g', animated=True) # Stick figure
    RF, = plt.plot([], [], '<k', animated=True) # Right foot
    LF, = plt.plot([], [], '>k', animated=True) # Left foot
    HD, = plt.plot([], [], 'go', animated=True) # Head
    GD, = plt.plot([], [], '-b', animated=True) # Ground
    ST, = plt.plot([], [], '-r', animated=True) # Stool
    return LN, RF, LF, HD, GD, ST,

def init():
    ax.set_xlim(-1,11)
    ax.set_ylim(-1,5)
    ax.set_aspect('equal')
    return LN, RF, LF, HD, GD, ST,

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
    
    # Update Axis Limits
    #ax.set_xlim(xv[1]-4.5, xv[1]+0.5)
    #ax.set_ylim(yv[1]-1.2, yv[1]+2.8)
    
    return LN, RF, LF, HD, GD, ST,