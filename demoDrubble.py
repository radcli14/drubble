# Import required packages
exec(open("./drubbleFunc.py").read())

# Clos figure windows
plt.close('all')

# Obtain Parameters
p = parameters()

# Initial States
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.y0,p.l0,0,0,0,0,0,-4,8,3,12]

# Predict position and time where ball hits stool
[xb,yb,tb] = BallPredict(u0)

# Time vector for test simulation
tspan = [0, 20]
fs = 30
dt = 1/fs
t = np.linspace(tspan[0],tspan[1],fs*(tspan[1]-tspan[0])+1)

# Output data matrix
N = np.size(t)
Y = np.zeros((N,12))
Y[0,:] = u0

# Calculate a single point, to test    
# du = PlayerAndStool(tspan,u0)
# print(du)

# Define the Events
events = [BallHitStool,BallHitFloor]
#events = [BallHitFloor]

# Run a simulation demo
eventCount = 0
te = 0
n = 0

start_time = time.time()
while t[n]<tspan[1]:
    try:
        u = Y[n,:].tolist()
        if (t[n]-te)>0.1:
            sol = spi.solve_ivp(PlayerAndStool,[t[n],t[n+1]],u, 
                                max_step=0.005,events=events)
        else:
            sol = spi.solve_ivp(PlayerAndStool,[t[n],t[n+1]],u, 
                                max_step=0.005)    
        
        if sol.status:
            eventCount = eventCount+1
        else:
            n = n+1
            Y[n,:] = sol.y[:,-1]
            continue
        
        # Solve up to the instant event occured, and get states at that instant
        if np.size(sol.t_events[0]):
            te = sol.t_events[0][0]
            StoolBounce = True
            FloorBounce = False
        elif np.size(sol.t_events[1]):
            te = sol.t_events[1][0]
            StoolBounce = False
            FloorBounce = True
        print("te = ",te,' sec, StoolBounce = ',
              StoolBounce,', FloorBounce = ',FloorBounce)
        ue = sol.y[:,-1].tolist()
        # sol = spi.solve_ivp(PlayerAndStool,[t[n],te],un)
        # ue  = sol.y[:,-1].tolist() 
        
        if StoolBounce:
            ue[9] = ue[9]+0.001
            
            # Obtain the bounce velocity
            print("stool!")
            vBounce = BallBounce(te,ue)
            print("vBounce=",vBounce)
            ue[10] = vBounce[0]
            ue[11] = vBounce[1]
            #print(ue)
        elif FloorBounce:
            ue[9] = 0.001
        
            # Reverse direction of the ball
            ue[10] = p.COR*ue[10]
            ue[11] = -p.COR*ue[11]
        
        # Recalculate next position
        [xb,yb,tb] = BallPredict(ue)
        tb = tb+te
 
        # Re-initialize from the event states
        sol = spi.solve_ivp(PlayerAndStool,[te,t[n+1]],ue)
        
        # Iterate n, and add the current result into the data matrix
        n = n+1
        Y[n,:] = sol.y[:,-1]
        
    except:
        print("There was an exception in the simulation loop")
        break
print("--- Simulation ran in %s seconds ---" % (time.time() - start_time))

# Initialize the PDF file
with PdfPages('demoDrubble.pdf') as pdf:

    # Plot results
    f1 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='x [m]')
    plt.plot(t,Y[:,0])
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='y [m]')
    plt.plot(t,Y[:,1])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='l [m]')
    plt.plot(t,Y[:,2])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='theta [deg]')
    plt.plot(t,np.rad2deg(Y[:,3]))
    #pdf.savefig()
    
    f2 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='dx/dt [m/s]')
    plt.plot(t,Y[:,4])
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='dy/dt [m/s]')
    plt.plot(t,Y[:,5])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='dl/dt [m/s]')
    plt.plot(t,Y[:,6])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='dtheta/dt [deg]')
    plt.plot(t,np.rad2deg(Y[:,7]))
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
        try:
            # Get the plotting vectors using stickDude function
            xv,yv,rf,lf,sx,sy = stickDude(n)
            
            # Generate plot at time t[n]
            plt.plot(xv,yv)
            plt.plot(rf[0],rf[1],'k>')
            plt.plot(lf[0],lf[1],'k<')
            plt.plot(Y[n,0],Y[n,1]+p.d*1.6,'go')
            plt.plot(sx,sy,'-r')
        except:
            print("There was an exception generating the plot")
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
Writer = animation.writers['ffmpeg']
writer = Writer(fps=fs, metadata=dict(artist='Me'), bitrate=1800)
ani.save('demoDrubble.mp4', writer=writer)