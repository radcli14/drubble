# Import required packages
exec(open("./drubbleFunc.py").read())

# Clos figure windows
plt.close('all')

# Obtain Parameters
p = parameters()

# Initial States
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.y0,p.l0,0,0,0,0,0,-4,8,4,12]

# Predict position and time where ball hits stool
[xb,yb,tb] = BallPredict(u0)

# Time vector for test simulation
tspan = [0, 10]
fs = 30
dt = 1/fs
t = np.linspace(tspan[0],tspan[1],fs*(tspan[1]-tspan[0])+1)

# Calculate a single point, to test    
du = PlayerAndStool(tspan,u0)
print(du)

# Define the Events
events = [BallHitStool,BallHitFloor]
#events = [BallHitFloor]

# Run a simulation
sol = spi.solve_ivp(PlayerAndStool,tspan,u0,t_eval=t,events=events)
T = sol.t
Y = sol.y.T
while T[-1]<tspan[1]:
    # Solve up to the instant event occured, and get states at that instant
    if np.size(sol.t_events[0]):
        te = sol.t_events[0][0]
        StoolBounce = True
        FloorBounce = False
    elif np.size(sol.t_events[1]):
        te = sol.t_events[1][0]
        StoolBounce = False
        FloorBounce = True
    print("te = ",te)
    ne    = np.size(T)
    un    = Y[-1].tolist()
    sol   = spi.solve_ivp(PlayerAndStool,[T[-1],te],un)
    ue    = sol.y[:,-1].tolist() 
    
    if StoolBounce:
        ue[9] = ue[9]+0.001
        
        # Reverse direction of the ball
        ue[10] = p.COR*ue[10]
        ue[11] = -p.COR*ue[11]
        
    elif FloorBounce:
        ue[9] = 0.001
    
        # Reverse direction of the ball
        ue[10] = p.COR*ue[10]
        ue[11] = -p.COR*ue[11]
    
    # Recalculate next position
    [xb,yb,tb] = BallPredict(ue)
    tb = tb+te
    
    # Re-initialize from the event states
    tspan_r = [te,tspan[1]]
    sol = spi.solve_ivp(PlayerAndStool,tspan_r,ue,t_eval=t[ne:],events=events)
    
    # Concatenate onto the T,Y arrays
    T = np.concatenate((T,sol.t),axis=0)
    Y = np.concatenate((Y,sol.y.T),axis=0)

# Initialize the PDF file
with PdfPages('demoDrubble.pdf') as pdf:

    # Plot results
    f1 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='x [m]')
    plt.plot(T,Y[:,0])
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='y [m]')
    plt.plot(T,Y[:,1])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='l [m]')
    plt.plot(T,Y[:,2])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='theta [deg]')
    plt.plot(T,np.rad2deg(Y[:,3]))
    #pdf.savefig()
    
    f2 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='dx/dt [m/s]')
    plt.plot(T,Y[:,4])
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='dy/dt [m/s]')
    plt.plot(T,Y[:,5])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='dl/dt [m/s]')
    plt.plot(T,Y[:,6])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='dtheta/dt [deg]')
    plt.plot(T,np.rad2deg(Y[:,7]))
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
        plt.plot(Y[n,0],Y[n,1]+p.d*1.6,'go')
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
        plt.plot(Y[n,0],Y[n,1]+p.d*1.6,'go')
        plt.plot(sx,sy,'-r')
    #pdf.savefig()
    
    f4 = plt.figure()
    plt.plot(Y[:,8],Y[:,9])
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
# Export the movie file
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=fs, metadata=dict(artist='Me'), bitrate=1800)
#ani.save('demoDrubble.mp4', writer=writer)