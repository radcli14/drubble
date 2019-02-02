# Import required packages
exec(open("./drubbleFunc.py").read())

# Export Figures and Animations
eboule = False

# Close figure windows
plt.close('all')

# Set Screen Size
size = width, height = 1000, 600

# Obtain Parameters
p = parameters()

# Initial States
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.y0,p.l0,0,0,0,0,0,-4,8,3,12]

# Predict position and time where ball hits stool
[xb,yb,tb,Xb,Yb] = BallPredict(u0)

# Time vector for test simulation
tspan = [0, 50]
fs = 30
dt = 1/fs
t  = np.linspace(tspan[0],tspan[1],fs*(tspan[1]-tspan[0])+1)

# Output data matrices
N         = np.size(t)
Y         = np.zeros((N,12))
Y[0,:]    = u0
XB        = np.zeros((N,20))
YB        = np.zeros((N,20))
WantAngle = np.zeros((N,1))
ZZEM      = np.zeros((N,1))

# Define the Events
events = [BallHitStool,BallHitFloor]

# Run a simulation demo
eventCount = 0
te = 0
n  = 0

start_time = time.time()
while t[n]<tspan[1]:
    # Ball trajectory prediction
    XB[n,:] = Xb
    YB[n,:] = Yb
    
    # Time until event 
    timeUntilBounce = tb-t[n];
    
    # Get the control logic variables for plotting after we're done
    Q, Bx, By, Bl, Bth, ZEM, wantAngle, xdiff, ydiff = ControlLogic(t[n],Y[n,:].tolist())
    WantAngle[n] = wantAngle
    ZZEM[n] = ZEM
    
    sol, wasEvent, te = simThisStep(t[n],Y[n,:].tolist(),te) 
    eventCount += wasEvent

    # Iterate n, and add the current result into the data matrix
    n += 1
    Y[n,:] = sol.y[:,-1]

    if wasEvent:
        # Recalculate ball position the next time it crosses top of stool
        [xb,yb,tb,Xb,Yb] = BallPredict(Y[n,:])
        tb = tb+te
print("--- Simulation ran in %s seconds ---" % (time.time() - start_time))

# Initialize the PDF file
with PdfPages('demoDrubble.pdf') as pdf:

    # Plot results
    f1 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='x [m]')
    plt.plot(t,Y[:,0])
    plt.plot(t,ZZEM)
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='y [m]')
    plt.plot(t,Y[:,1])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='l [m]')
    plt.plot(t,Y[:,2])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='theta [deg]')
    plt.plot(t,np.rad2deg(Y[:,3]))
    plt.plot(t,np.rad2deg(WantAngle))
    plt.tight_layout()
    if eboule:
        pdf.savefig()
    
    f2 = plt.figure()
    plt.subplot(2,2,1,xlabel='Time [sec]',ylabel='dx/dt [m/s]')
    plt.plot(t,Y[:,4])
    plt.subplot(2,2,2,xlabel='Time [sec]',ylabel='dy/dt [m/s]')
    plt.plot(t,Y[:,5])
    plt.subplot(2,2,3,xlabel='Time [sec]',ylabel='dl/dt [m/s]')
    plt.plot(t,Y[:,6])
    plt.subplot(2,2,4,xlabel='Time [sec]',ylabel='dtheta/dt [deg]')
    plt.plot(t,np.rad2deg(Y[:,7]))
    plt.tight_layout()
    if eboule:
        pdf.savefig()
    
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
    plt.tight_layout()    
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
    plt.tight_layout()        
    if eboule:
        pdf.savefig()
    
    f4 = plt.figure()
    plt.plot(Y[:,8],Y[:,9])
    plt.xlabel('Distance [m]')
    plt.ylabel('Height [m]')
    plt.tight_layout()
    if eboule:
        pdf.savefig()
    
# Generate an animation
fig = plt.figure()    
ax  = fig.add_axes([0,0,1,1])
DPI = fig.get_dpi()
fig.set_size_inches(width/float(DPI),height/float(DPI))
LN, RF, LF, HD, GD, ST, BL, BA = initPlots()

ani = animation.FuncAnimation(fig, animate, np.size(t), interval=dt*1000, 
                              init_func=init, blit=True)

# Export the movie file
if eboule:
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=fs, metadata=dict(artist='Me'), bitrate=1800)
    ani.save('demoDrubble.mp4', writer=writer)