# Import required packages
exec(open("./drubbleFunc.py").read())

# Clos figure windows
plt.close('all')

# Obtain Parameters
p = parameters()

# Initial States
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.y0,p.l0,0,0,0,0,0,-1,3.5,3,12]

# Predict position and time where ball hits stool
[xb,yb,tb] = BallPredict(u0)

# Generalized Forces
Q = np.matrix([[p.Qx],[p.Qy],[p.Ql],[p.Qt]])

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

# Initialize the PDF file
with PdfPages('demoDrubble.pdf') as pdf:

    # Plot results
    f1 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='x [m]')
    plt.plot(sol.t,sol.y[0,:])
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='y [m]')
    plt.plot(sol.t,sol.y[1,:])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='l [m]')
    plt.plot(sol.t,sol.y[2,:])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='theta [deg]')
    plt.plot(sol.t,180/np.pi*sol.y[3,:])
    #pdf.savefig()
    
    f2 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='dx/dt [m/s]')
    plt.plot(sol.t,sol.y[4,:])
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='dy/dt [m/s]')
    plt.plot(sol.t,sol.y[5,:])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='dl/dt [m/s]')
    plt.plot(sol.t,sol.y[6,:])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='dtheta/dt [deg]')
    plt.plot(sol.t,sol.y[7,:])
    #pdf.savefig()
    
    # Generate an overlay plot of several frames
    f3 = plt.figure()
    ax = f3.add_subplot(211)
    ax.set_aspect('equal')
    
    for n in range(0,int(2*fs),int(fs/6)): 
    
        # Get the plotting vectors using stickDude function
        xv,yv,rf,lf,sx,sy = stickDude(n)
        
        # Generate plot at time t[n]
        plt.plot(xv,yv)
        plt.plot(rf[0],rf[1],'k>')
        plt.plot(lf[0],lf[1],'k<')
        plt.plot(sol.y[0,n],sol.y[1,n]+p.d*1.6,'go')
        plt.plot(sx,sy,'-r')
        #plt.xlim(sol.y[0,n]+[-5.5,0.5])
        #plt.ylim(sol.y[1,n]+[-2.1,1.9])
        
    ax = f3.add_subplot(212)
    ax.set_aspect('equal')
    
    for n in range(int(2*fs+fs/6),int(2*fs+9*fs/6),int(fs/6)): 
    
        # Get the plotting vectors using stickDude function
        xv,yv,rf,lf,sx,sy = stickDude(n)
        
        # Generate plot at time t[n]
        plt.plot(xv,yv)
        plt.plot(rf[0],rf[1],'k>')
        plt.plot(lf[0],lf[1],'k<')
        plt.plot(sol.y[0,n],sol.y[1,n]+p.d*1.6,'go')
        plt.plot(sx,sy,'-r')
    
    #pdf.savefig()
    
# Generate an animation
fig = plt.figure()    
ax  = fig.add_axes([0,0,1,1])
DPI = fig.get_dpi()
fig.set_size_inches(1334.0/float(DPI),750.0/float(DPI))
LN, RF, LF, HD, GD, ST, BL = initPlots()

ani = animation.FuncAnimation(fig, animate, np.size(t), interval=dt*1000, 
                              init_func=init, blit=True)
#plt.show()    
# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=fs, metadata=dict(artist='Me'), bitrate=1800)
ani.save('demoDrubble.mp4', writer=writer)