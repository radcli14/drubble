# Import required packages
exec(open("./drubbleFunc.py").read())
pygame.init()

# Window size and color definition
size = width, height = 1000, 600
speed = [2, 2]
cyan = 0, 255, 255

# Initial States
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u  = [0,p.y0,p.l0,0,0,0,0,0,-4,8,3,12]
te = 0
t  = 0
fs = 30
dt = 1/fs

# Open display
screen = pygame.display.set_mode(size)

# Import the Big Chair image
bigChair = pygame.image.load("bigChair.jpg")
bC_rect = bigChair.get_rect()

# Run an infinite loop until stopped
while 1:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT: sys.exit()

# Prevent event detection if there was already one within 0.1 seconds
    if (t-te)>0.1:
        sol = spi.solve_ivp(PlayerAndStool,[0,dt],u,events=events)
    else:
        sol = spi.solve_ivp(PlayerAndStool,[0,dt],u)   


    bC_rect = bC_rect.move(speed)
    if bC_rect.left < 0 or bC_rect.right > width:
        speed[0] = -speed[0]
    if bC_rect.top < 0 or bC_rect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(cyan)
    screen.blit(bigChair, bC_rect)
    pygame.display.flip()