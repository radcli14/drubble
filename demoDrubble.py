# Import required packages
# import os
# import time
import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import drubbleFunc
runfile('drubbleFunc.py')

# Parameters
g  = 9.81 # Gravitational acceleration [m/s^2]
mc = 50 # Mass of player [kg]
mg = 2  # Mass of stool [kg]
m  = mc+mg # Total mass
y0 = 1.5  # Equilibrium position of player CG
d  = 0.3 # Relative position from player CG to stool rotation axis
l0 = 1  # Equilibrium position of stool
ax = 1  # Horizontal acceleration [g]
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

# Initial States
q0 = np.matrix([[0],[y0],[l0],[0]])
#u0 = np.matrix([[0],[y0],[l0],[0],[0],[0],[0],[0]])
u0 = [0,y0,l0,0,0,0,0,0]

# Generalized Forces
Q = np.matrix([[Qx],[0],[0],[0]])

# Time vector for test simulation
tspan = [0, 10]
fs = 30
dt = 1/fs
t = np.linspace(tspan[0],tspan[1],fs*(tspan[1]-tspan[0])+1)

# Calculate a single point, to test    
du = PlayerAndStool(tspan,u0)
print(du)

# Run a simulation
sol = spi.solve_ivp(PlayerAndStool,tspan,u0,t_eval=t)

# Plot results
plt.figure()
plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='x [m]')
plt.plot(sol.t,sol.y[0,:])
plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='y [m]')
plt.plot(sol.t,sol.y[1,:])
plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='l [m]')
plt.plot(sol.t,sol.y[2,:])
plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='\theta [deg]')
plt.plot(sol.t,180/np.pi*sol.y[3,:])

plt.figure()
plt.subplot(2,2,1)
plt.plot(sol.t,sol.y[4,:])
plt.subplot(2,2,2)
plt.plot(sol.t,sol.y[5,:])
plt.subplot(2,2,3)
plt.plot(sol.t,sol.y[6,:])
plt.subplot(2,2,4)
plt.plot(sol.t,sol.y[7,:])


#ani = animation.FuncAnimation(fig, animate, range(0,np.size(t), interval=dt, init_func=init)

#plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')

for n in range(0,30,2): 
    #range(0,np.size(t)):
    
    # Get the plotting vectors using plotDude function
    xv,yv,rf,lf = stickDude(n)
    
    # Generate plot at time t[n]
    plt.plot(xv,yv)
    plt.plot(rf[0],rf[1],'k>')
    plt.plot(lf[0],lf[1],'k<')
    plt.xlim([x-4.5,x+0.5])
    plt.ylim([y-2.1,y+1.9])
         