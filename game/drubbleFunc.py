# Import modules
from math import sin, cos, pi, sqrt, isnan, fmod, atan2, erf
from random import randint
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
import sys
try:
    import numpy as np
    from numpy import array
    USE_NUMPY = True
    print('Successfully imported numpy')
except:
    USE_NUMPY = False
    print('Failed importing numpy')
print('')
print('  USE_NUMPY = ' + str(USE_NUMPY))
print('')

# Frame rate
if 'dRuBbLe' in sys.argv[0]:
    fs = 60
    engine = 'ista'
else:
    fs = 30
    engine = 'kivy'
dt = 1.0/fs

# Color definition
darkBlue = (0, 0, 128.0/255.0)
skyBlue = (135.0/255.0, 226.0/255.0, 255.0/255.0)
cyan = (0.0, 1.0, 1.0)
darkGreen = (0, 120.0/255.0, 0)
olive = [[128.0 / 255.0, 128.0 / 255.0, 0.0, 1.0], [128.0 / 255.0, 128.0 / 255.0, 0.0, 1.0]]

# Android System Colors
red = [[244.0 / 255.0, 67.0 / 255.0, 54.0 / 255.0, 1.0], []]
pink = [[233.0 / 255.0, 30.0 / 255.0, 99.0 / 255.0, 1.0], []]
purple = [[156.0 / 255.0, 39.0 / 255.0, 176.0 / 255.0, 1.0], []]
deep_purple = [[103.0 / 255.0, 58.0 / 255.0, 183.0 / 255.0, 1.0], []]
indigo = [[6.0 / 255.0, 81.0 / 255.0, 181.0 / 255.0, 1.0], []]
blue = [[33.0 / 255.0, 150.0 / 255.0, 243.0 / 255.0, 1.0], []]
light_blue = [[3.0 / 255.0, 169.0 / 255.0, 244.0 / 255.0, 1.0], []]
cyan = [[0.0 / 255.0, 188.0 / 255.0, 212.0 / 255.0, 1.0], []]
teal = [[0.0 / 255.0, 150.0 / 255.0, 136.0 / 255.0, 1.0], []]
green = [[76.0 / 255.0, 175.0 / 255.0, 80.0 / 255.0, 1.0], []]
light_green = [[139.0 / 255.0, 195.0 / 255.0, 74.0 / 255.0, 1.0], []]
lime = [[205.0 / 255.0, 220.0 / 255.0, 57.0 / 255.0, 1.0], []]
yellow = [[255.0 / 255.0, 235.0 / 255.0, 59.0 / 255.0, 1.0], []]
amber = [[255.0 / 255.0, 193.0 / 255.0, 7.0 / 255.0, 1.0], []]
orange = [[255.0 / 255.0, 152.0 / 255.0, 0.0 / 255.0, 1.0], []]
deep_orange = [[255.0 / 255.0, 87.0 / 255.0, 2.0 / 255.0, 1.0], []]
brown = [[121.0 / 255.0, 85.0 / 255.0, 72.0 / 255.0, 1.0], []]
grey = [[158.0 / 255.0, 158.0 / 255.0, 158.0 / 255.0, 1.0], []]
blue_grey = [[96.0 / 255.0, 125.0 / 255.0, 139.0 / 255.0, 1.0], []]

# Apple System Color
blue = [[0.0, 122.0 / 255.0, 1.0, 1.0], [10.0 / 255.0, 132.0 / 255.0, 1.0, 1.0]]
green = [[52.0 / 255.0, 199.0 / 255.0, 89.0 / 255.0, 1.0], [48.0 / 255.0, 209.0 / 255.0, 88.0 / 255.0, 1.0]]
indigo = [[88.0 / 255.0, 86.0 / 255.0, 214.0 / 255.0, 1.0], [94.0 / 255.0, 91.0 / 255.0, 120.0 / 255.0, 1.0]]
orange = [[255.0 / 255.0, 149.0 / 255.0, 0.0 / 255.0, 1.0], [255.0 / 255.0, 159.0 / 255.0, 10.0 / 255.0, 1.0]]
pink = [[255.0 / 255.0, 45.0 / 255.0, 85.0 / 255.0, 1.0], [255.0 / 255.0, 55.0 / 255.0, 95.0 / 255.0, 1.0]]
purple = [[175.0 / 255.0, 82.0 / 255.0, 222.0 / 255.0, 1.0], [191.0 / 255.0, 90.0 / 255.0, 242.0 / 255.0, 1.0]]
red = [[255.0 / 255.0, 59.0 / 255.0, 48.0 / 255.0, 1.0], [255.0 / 255.0, 69.0 / 255.0, 58.0 / 255.0, 1.0]]
teal = [[90.0 / 255.0, 200.0 / 255.0, 250.0 / 255.0, 1.0], [100.0 / 255.0, 110.0 / 255.0, 255.0 / 255.0, 1.0]]
yellow = [[255.0 / 255.0, 204.0 / 255.0, 0.0 / 255.0, 1.0], [255.0 / 255.0, 214.0 / 255.0, 10.0 / 255.0, 1.0]]

# Shades of gray
gray = [[142.0 / 255.0, 142.0 / 255.0, 147.0 / 255.0, 1.0], [142.0 / 255.0, 142.0 / 255.0, 147.0 / 255.0, 1.0]]
gray_2 = [[174.0 / 255.0, 174.0 / 255.0, 178.0 / 255.0, 1.0], [99.0 / 255.0, 99.0 / 255.0, 102.0 / 255.0, 1.0]]
gray_3 = [[199.0 / 255.0, 199.0 / 255.0, 204.0 / 255.0, 1.0], [72.0 / 255.0, 72.0 / 255.0, 74.0 / 255.0, 1.0]]
gray_4 = [[209.0 / 255.0, 209.0 / 255.0, 214.0 / 255.0, 1.0], [58.0 / 255.0, 58.0 / 255.0, 60.0 / 255.0, 1.0]]
gray_5 = [[229.0 / 255.0, 229.0 / 255.0, 234.0 / 255.0, 1.0], [44.0 / 255.0, 44.0 / 255.0, 46.0 / 255.0, 1.0]]
gray_6 = [[242.0 / 255.0, 242.0 / 255.0, 247.0 / 255.0, 1.0], [28.0 / 255.0, 28.0 / 255.0, 30.0 / 255.0, 1.0]]

# Black if darkMode is true, otherwise white
white = (1, 1, 1)
black = (0, 0, 0)
black_white = [[0.0, 0.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0]]


def xy2p(x, y, m2p, po, w, h):
    """
    Convert physical coordinates to pixels
    :param x: Horizontal position [m]
    :param y: Vertical position [m]
    :param m2p: Meter to Pixel conversion factor
    :param po: Number of pixels offset
    :param w: Screen width in pixels
    :param h: Screen height in pixels
    :return: (x in pixels, y in pixels)
    """
    # xp = x * m2p - po + 0.5 * w if type(x) in (int, float) else [xi * m2p - po + 0.5 * w for xi in x]
    # yp = y * m2p + 0.05 * h if type(y) in (int, float) else [yi * m2p + 0.05 * h for yi in y]
    xp = [xi * m2p - po + 0.5 * w for xi in x] if type(x) in (list, tuple) else x * m2p - po + 0.5 * w
    yp = [yi * m2p + 0.05 * h for yi in y] if type(y) in (list, tuple) else y * m2p + 0.05 * h
    return xp, yp


# Parameters
class Parameters:
    # Game parameters
    g = 9.81            # Gravitational acceleration [m/s^2]
    COR_s = 0.70, 0.90  # Coefficient of restitution (COR) when ball hits stool
    COR_g = 0.50, 0.70  # COR when ball hits ground
    COR_n = 0.80, 1.00  # COR when ball hits net
    rb = 0.2            # Radius of the ball

    # Player parameters
    mc = 50.0    # Mass of player [kg]
    mg = 2.0     # Mass of stool [kg]
    m = mc+mg    # Total mass [kg]
    x0 = 5.0     # Initial player position [m]
    y0 = 1.5     # Equilibrium position of player CG [m]
    d = 0.3      # Relative position from player CG to stool rotation axis [m]
    l0 = 1.5     # Equilibrium position of stool
    ax = 1.5     # Horizontal acceleration [g]
    Qx = ax*m*g  # Max horizontal force [N]
    Gx = 1.5     # Control gain on Qx
    fy = 0.8     # vertical frequency [Hz]
    Ky = m * (fy*2*pi)**2  # Leg stiffness [N/m]
    Qy = Ky*0.3  # Leg strength [N], to be updated
    fl = 2.2     # Stool extension frequency
    Kl = mg * (fl*2*pi)**2  # Arm stiffness [N/m]
    Ql = Kl*0.3  # Arm strength [N]
    ft = 1.25     # Stool tilt frequency [Hz]
    Kt = (mg*l0*l0) * (ft*2*pi)**2  # Tilt stiffness [N-m/rad]
    Qt = 0.8*Kt  # Tilt strength [N-m]
    Gt = 0.8     # Control gain on Qt
    vx = 10.0    # Horizontal top speed [m/s]
    Cx = Qx/vx   # Horizontal damping [N-s/m]
    zy = 0.1     # Vertical damping ratio
    Cy = 2 * zy * sqrt(Ky*m)  # Vertical damping [N-s/m]
    zl = 0.08    # Arm damping ratio
    Cl = 2 * zl * sqrt(Kl*m)  # Arm damping [N-s/m]
    zt = 0.09    # Stool tilt damping ratio
    Ct = 2.0 * zl * sqrt(Kt*m)  # Tilt damping [N-m-s/rad]

    # Initial states
    q0 = [0.0, y0, l0, 0.0]
    u0 = [0.0, rb, 0.0, 0.0, x0, y0, l0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0, y0, l0, 0.0, 0.0, 0.0, 0.0, -10.0]

    # Game play settings
    demo_mode = False
    userControlled = [[True for _ in range(4)], [False for _ in range(4)]]
    num_player = 1

    # Stool parameters
    stool_radius = 0.35, 0.3, 0.25
    stool_hand_pos = -0.6

    if USE_NUMPY:
        # q0 in numpy array form
        q0_array = np.array([[q0[0]], [q0[1]], [q0[2]], [q0[3]]])

        # Mass matrix
        M = np.array([[m, 0, 0, -mg * l0],
                      [0, m, mg, 0],
                      [0, mg, mg, 0],
                      [-mg * l0, 0, 0, mg * l0**2]])
        invM = np.linalg.inv(M)

        # Damping Matrix
        C = np.diag([Cx, Cy, Cl, Ct])

        # Stiffness Matrix
        K = np.diag([0.0, Ky, Kl, Kt])

    # Touch Stick Sensitivity
    tsens = 1.2
    
    # Tolerance on last bounce speed before stopping motion
    dybtol = 4.0
    
    # start_angle (sa) and start_speed (ss) initially
    sa = pi / 4
    ss = 10.0
    
    # Parameter settings I'm using to try to improve running speed
    linearMass = False
    num_euler_steps = 1
    timeRun = False
    gc = False
    profile_mode = False
    
    # Font settings
    MacsFavoriteFont = 'Optima'  # Papyrus' 'jokerman' 'poorrichard' 'rockwell' 'comicsansms'
    
    # Player visual settings (name, line_color, stool_color, ball_color, face_size, down_shift)
    player_data = [('bro', green[0], gray[0], green[0], 0.7, 0.05),
                   ('gal', orange[0], gray_6[0], yellow[0], 0.8, 0.1),
                   ('max', gray[0], red[0], red[0], 0.7, 0.1),
                   ('woof', indigo[0], orange[0], orange[0], 0.8, 0.1),
                   ('hal', black_white[0], orange[0], gray_3[0], 1.1, 0.25),
                   ('goran', gray_6[0][:3] + [0.5], blue[0], red[0], 1, 0),
                   ('bear', yellow[0], pink[0], purple[0], 0.7, 0.1),
                   ('pigy', red[0], purple[0], pink[0], 0.8, 0.1),
                   ('guado', pink[0], teal[0], blue[0], 0.6, 0.0),
                   ('chiq', orange[0], green[0], purple[0], 1.0, 0.1)]
    players = {}
    for n, data in enumerate(player_data):
        name, line_color, stool_color, ball_color, face_size, down_shift = data
        players[n] = players[name] = {
            'face_texture': Image(source='a/'+name+'_face.png').texture,
            'jersey_texture': Image(source='a/'+name+'_jersey.png').texture,
            'shorts_texture0': Image(source='a/'+name+'_shorts.png').texture,
            'shorts_texture1': Image(source='a/'+name+'_shorts1.png').texture,
            'line_color': line_color, 'stool_color': stool_color, 'ball_color': ball_color,
            'face_size': face_size, 'down_shift': down_shift
        }

    # This is the text used in the upper right button
    actionMSG = '', '', '', 'Begin', 'Set Angle', 'Set Speed', 'High Scores', 'Restart'

    # Put in limits for the states to prevent crashing
    dxp_lim = -20, 20
    yp_lim = -1, 4
    dyp_lim = -20, 20
    lp_lim = -1, 3
    dlp_lim = -20, 20
    tp_lim = -3.14, 3.14
    dtp_lim = -20, 20

    # Parameters used in creating the stick dude
    stance_width = 0.3
    foot_step_length = 1.25
    foot_step_rate = 3.0
    foot_recovery_rate = 12.0
    leg_length = 0.9 * (y0 - d)

    # Number of points to include in the future trajectory predictions (ball_predict() function)
    num_future_points = 7

    # Time increment between future trajectory points
    future_increment = 0.1

    # Sound effects and music settings
    fx_is_on = True
    music_is_on = True

    # Difficulty levels (note, p.stool_radius is a vector, which is indexed by p.difficult_level)
    difficult_text = ['Easy', 'Hard', 'Silly']
    difficult_speed_scale = 0.85, 1.0, 1.2
    difficult_level = 0

    # VolleyDrubble Mode Settings
    volley_mode = False
    net_height = 5.0  # [m]
    net_width = 1.0   # [m]
    serving_player = 0
    serving_angle = 60
    serving_speed = 10
    back_line = 25.0
    winning_score = 5


p = Parameters()
dp = dir(p)
for k, pval in enumerate(dp):
    print()


# Initialize sounds
try:
    # Initialize drums
    num_loops = 3
    loop = [SoundLoader.load('a/0'+str(k)+'-DC-Base.wav') for k in range(num_loops)]
    for k in range(num_loops):
        loop[k].volume = 0.4

    def sound_stopped(self):
        # Randomize which loop to play, but prevent repeats of the intro
        if self.id_number == 0:
            current_loop = randint(1, num_loops-1)
        else:
            current_loop = randint(0, num_loops-1)

        # Restart playing a new drum loop
        loop[current_loop].play()

    for k in range(num_loops):
        loop[k].bind(on_stop=sound_stopped)
        loop[k].id_number = k

    # Start the intro loop playing
    loop[0].play()

    # Load the sounds that play on events
    stool_sound = SoundLoader.load('a/GoGo_crank_hit_Stool.wav')
    floor_sound = SoundLoader.load('a/GoGo_guitar_hit_slide_Floor.wav')
    floor_sound.pitch = 0.92
    stuck_sound = SoundLoader.load('a/GoGo_flam_drm_fill.wav')
    stuck_sound.volume = 0.7
    button_sound = SoundLoader.load('a/GoGo_flam_woo.wav')
    button_sound.volume = 0.5
    start_loop = SoundLoader.load('a/GoGo_hitta_conga_loop.wav')
    start_loop.volume = 0.4
    start_loop.pitch = 1.54

    SOUND_LOADED = True
except:
    print('failed loading wav')
    SOUND_LOADED = False


def varStates(obj):
    obj.xb = obj.u[0]         # Ball distance [m]
    obj.yb = obj.u[1]         # Ball height [m]
    obj.dxb = obj.u[2]        # Ball horizontal speed [m]
    obj.dyb = obj.u[3]        # Ball vertical speed [m]
    obj.xp = obj.u[4:13:8]    # Player distance [m]
    obj.yp = obj.u[5:14:8]    # Player height [m]
    obj.lp = obj.u[6:15:8]    # Stool extension [m]
    obj.tp = obj.u[7:16:8]    # Stool tilt [rad]
    obj.dxp = obj.u[8:17:8]   # Player horizontal speed [m/s]
    obj.dyp = obj.u[9:18:8]   # Player vertical speed [m/s]
    obj.dlp = obj.u[10:19:8]  # Stool extension rate [m/s]
    obj.dtp = obj.u[11:20:8]  # Stool tilt rate [rad/s]
    return obj


def unpackStates(u):
    # xp, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    xb = u[0]         # Ball distance [m]
    yb = u[1]         # Ball height [m]
    dxb = u[2]        # Ball horizontal speed [m]
    dyb = u[3]        # Ball vertical speed [m]
    xp = u[4:13:8]    # Player distance [m]
    yp = u[5:14:8]    # Player height [m]
    lp = u[6:15:8]    # Stool extension [m]
    tp = u[7:16:8]    # Stool tilt [rad]
    dxp = u[8:17:8]   # Player horizontal speed [m/s]
    dyp = u[9:18:8]   # Player vertical speed [m/s]
    dlp = u[10:19:8]  # Stool extension rate [m/s]
    dtp = u[11:20:8]  # Stool tilt rate [rad/s]
    return xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp


def linspace(start, stop, n):
    if n == 1:
        return stop
    h = (stop - start) / (n - 1)
    v = [start + h * i for i in range(n)]
    return v


def zeros(ztup):
    if type(ztup) in (list, tuple):
        z = [0 for _ in range(ztup[1])]
        Z = [z for _ in range(ztup[0])]
        return Z
    else:
        z = [0 for _ in range(ztup)]
        return z


# Predict motion of the ball
def ball_predict(gs, active_player):
    if gs.dyb == 0 or gs.game_mode <= 2:
        # Ball is not moving, impact time is zero
        tI = 0
    elif gs.game_mode > 2 and (gs.dyb > 0) and (gs.yb < gs.yp[active_player] + p.d + gs.lp[active_player]):
        # Ball is in play, moving upward and below the stool
        # Solve for time and height at apogee
        ta = gs.dyb / p.g
        ya = 0.5 * p.g * ta ** 2

        # Solve for time the ball would hit the ground
        tI = ta + sqrt(2.0 * ya / p.g)
    elif gs.game_mode > 2 and gs.yb > 3.2:
        # Ball is in play, above the stool
        # Solve for time that the ball would hit the stool
        tI = -(-gs.dyb - sqrt(gs.dyb ** 2 + 2.0 * p.g * (gs.yb - 3.2))) / p.g
    else:
        tI = 0

    if isnan(tI):
        tI = 0

    # Solve for position that the ball would hit the stool
    xI = gs.xb + gs.dxb * tI
    yI = gs.yb + gs.dyb * tI - 0.5 * p.g * tI ** 2

    # Solve for time that the ball would hit the ground
    tG = -(-gs.dyb - sqrt(gs.dyb ** 2 + 2.0 * p.g * (gs.yb-p.rb))) / p.g

    # Solve at 0.15 second increments or until ball hits ground
    time_offset = dt + p.future_increment - fmod(gs.t / p.future_increment, 1.0) * p.future_increment
    T = zeros(p.num_future_points)
    for n in range(p.num_future_points):
        t = time_offset + p.future_increment * n
        T[n] = t if t < tG else tG

    traj = {'t': zeros(p.num_future_points), 'x': zeros(p.num_future_points), 'y': zeros(p.num_future_points)}
    n = -1
    for t in T:
        n += 1
        traj['t'][n] = gs.t + T[n]
        traj['x'][n] = gs.xb + gs.dxb * t
        traj['y'][n] = gs.yb + gs.dyb * t - 0.5 * p.g * t ** 2

    # Time until event
    time_until_bounce = tI
    tI = time_until_bounce + gs.t

    # Output variables
    # xI = Ball distance at impact [m]
    # yI = Ball height at impact [m]
    # tI = Time at impact [s]
    # traj = Ball trajectory ['t' in seconds, 'x' in m, 'y' in m]
    return xI, yI, tI, traj, time_until_bounce


class GameState:
    floor_bounce = False
    stool_bounce = False
    net_bounce = False
    volley_game_is_active = False
    active_player = 0
    screen_width = 0
    screen_height = 0
    u = zeros(20)

    # Initiate the state variables as a list, and as individual variables
    def __init__(self, u0=p.u0, engine='kivy'):
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
        self.game_mode = 1
        self.showedSplash = False

        # Determine the control method, and initialize ctrl variable
        if engine == 'kivy':
            self.ctrlMode = 'keys'
            self.ctrl_func = 0
        elif engine == 'ista':
            #self.ctrlMode = 'motion'
            #self.ctrl_func = 1
            self.ctrlMode = 'vStick'
            self.ctrl_func = 2
        self.ctrl = [0.0, 0.0, 0.0, 0.0]
        self.keyPush = [0, 0, 0, 0, 0, 0, 0, 0]
        
        # Timing
        self.t = 0
        self.n = 0
        self.te = 0
        
        # State variables
        self.xb = self.u[0] = u0[0]  # Ball distance [m]
        self.yb = self.u[1] = u0[1]  # Ball height [m]
        self.dxb = self.u[2] = u0[2]  # Ball horizontal speed [m]
        self.dyb = self.u[3] = u0[3]  # Ball vertical speed [m]
        self.xp = self.u[4:13:8] = u0[4:13:8]  # Player distance [m]
        self.yp = self.u[5:14:8] = u0[5:14:8]  # Player height [m]
        self.lp = self.u[6:15:8] = u0[6:15:8]  # Stool extension [m]
        self.tp = self.u[7:16:8] = u0[7:16:8]  # Stool tilt [rad]
        self.dxp = self.u[8:17:8] = u0[8:17:8]  # Player horizontal speed [m/s]
        self.dyp = self.u[9:18:8] = u0[9:18:8]  # Player vertical speed [m/s]
        self.dlp = self.u[10:19:8] = u0[10:19:8]  # Stool extension rate [m/s]
        self.dtp = self.u[11:20:8] = u0[11:20:8]  # Stool tilt rate [rad/s]

        # Foot positions for drawing the stick figure [x, y, phase]
        self.foot_position = [[[self.xp[0] - p.stance_width, 0.0, 0.0], [self.xp[0] + p.stance_width, 0.0, 0.5 * pi]],
                              [[self.xp[1] - p.stance_width, 0.0, 0.0], [self.xp[1] + p.stance_width, 0.0, 0.5 * pi]]]

        # Event states
        self.ue = u0[:]
        self.xI, self.yI, self.tI, self.traj, self.timeUntilBounce = ball_predict(self, 0)
        self.stool_count = 0

        # Angle and Speed Conditions
        self.start_angle = p.sa
        self.start_speed = p.ss
        self.phase = 0
        
        # Stuck condition
        self.Stuck = False

        # Initiate Volley Drubble
        if p.volley_mode:
            self.volley_game_is_active = True

        # Plotting ranges and sticks
        self.xr = 0.0, 1.0
        self.yr = 0.0, 1.0
        self.m2p = 1.0
        self.po = 0.0
        # self.player_x = [[], []]
        # self.player_y = [[], []]
        self.player = [[], []]
         
    # Get control input from external source
    def set_control(self, keyPush=[0, 0, 0, 0, 0, 0, 0, 0],
                   moveStick=(0, 0), tiltStick=(0, 0),
                   g=(0, 0, 0), a=(0, 0, 0)):

        if self.ctrl_func == 0:
            # Key press control
            self.ctrl = [keyPush[1]-keyPush[0], keyPush[2]-keyPush[3], keyPush[4]-keyPush[5], keyPush[6]-keyPush[7]]
            
        elif self.ctrl_func == 1:
            # Motion control scale factors
            g_threshold = 0.05
            slope = 5.0
            a_scale = 2.0

            # Run left/right
            if g[1] > g_threshold:
                self.ctrl[0] = -min(slope*(g[1]-g_threshold), 1)
            elif g[1] < -g_threshold:
                self.ctrl[0] = -max(slope*(g[1]+g_threshold), -1)
            else:
                self.ctrl[0]
                
            # Push up/down    
            if a[1]>0:
                self.ctrl[1] = min(a_scale*a[1], 1)
            else:
                self.ctrl[1] = max(a_scale*a[1], -1)
                    
        elif self.ctrl_func == 2:
            # Virtual stick control
            self.ctrl = [moveStick[0], moveStick[1], tiltStick[1], -tiltStick[0]]
        
    # Execute a simulation step of duration dt    
    def sim_step(self):
        # Increment n 
        self.n += 1

        # Active player
        self.active_player = int(self.xb > 0) if p.volley_mode else self.stool_count % p.num_player

        # Initial assumption, there was no event
        self.stool_bounce = False
        self.floor_bounce = False
        self.net_bounce = False
        
        # Prevent event detection if there was already one within 0.1 seconds, 
        # or if the ball is far from the stool or ground
        # L = ball_hit_stool(self.t, self.u, self.active_player)  # Distance to stool
        v_ball = (self.dxb, self.dyb)                           # Velocity
        s_ball = norm(v_ball)                                   # Speed

        # Set the timing
        time_condition = (self.yb - self.yp[self.active_player] - self.lp[self.active_player] * cos(self.tp[self.active_player]) - p.d) / s_ball if s_ball > 0.0 else -1.0
        near_condition = abs(self.xb - self.xp[self.active_player]) < 1.0
        net_condition = p.volley_mode and abs(self.xb) - p.net_width < 1.0 and self.yb - p.net_height - p.net_width < 1.0
        if gs.n > 1 and ((0.0 < time_condition < 0.5 and near_condition) or net_condition):
            # Slow speed
            ddt = dt / 1.5 * p.difficult_speed_scale[p.difficult_level]
            num_step = 4 * p.num_euler_steps
        else:
            # Regular speed
            ddt = dt * p.difficult_speed_scale[p.difficult_level]
            num_step = p.num_euler_steps

        # Integrate using Euler method
        # Initialize state variables
        if USE_NUMPY:
            U = np.zeros((num_step+1, 20))
            U[0, :] = self.u
        else:
            U = zeros((num_step+1, 20))
            U[0] = self.u

        for k in range(1, num_step+1):
            # Increment time
            self.t += ddt / num_step
            
            # Calculate the derivatives of states w.r.t. time
            dudt = player_and_stool(self.t, U[k-1])

            # Calculate the states at the next step
            if USE_NUMPY:
                U[k] = U[k-1] + np.array(dudt) * ddt / num_step
            else:
                U[k] = [U[k-1][i] + dudt[i] * ddt / num_step for i in range(20)]

            # Check for events
            if (self.t - self.te) > 0.1 and not self.Stuck:
                if ball_hit_stool(self.t, U[k], self.active_player) < 0.0:
                    self.stool_bounce = True
                elif (U[k][1] - p.rb) < 0.0:
                    self.floor_bounce = True
                if p.volley_mode and ball_hit_net(self.t, U[k]) < 0.0:
                    self.net_bounce = True
                if self.stool_bounce or self.floor_bounce or self.net_bounce:
                    self.te = self.t
                    self.ue = U[k]
                    tBreak = k * ddt / num_step
                    break 
        
        # If an event occurred, update the states, otherwise continue
        if self.stool_bounce or self.floor_bounce or self.net_bounce:
            # Change ball states depending on if it was a stool or floor bounce
            if self.stool_bounce:
                self.stool_count += 1

                # Play the sound
                if SOUND_LOADED and p.fx_is_on:
                    stool_sound.volume = max(0.02, min(norm([self.dxb, self.dyb]) / 130.0, 0.8))
                    stool_sound.play()

                # Obtain the bounce velocity
                v_bounce, v_recoil = ball_bounce_stool(self, self.active_player)
                self.ue[2] = v_bounce[0]
                self.ue[3] = v_bounce[1]
                
                # Add  the recoil to the player
                self.ue[8 + self.active_player * 8] = self.ue[8 + self.active_player * 8] + v_recoil[0]
                self.ue[9 + self.active_player * 8] = self.ue[9] + v_recoil[1]
                self.ue[10 + self.active_player * 8] = self.ue[10] + v_recoil[2]
                self.ue[11 + self.active_player * 8] = self.ue[11] + v_recoil[3]
                
            elif self.floor_bounce:
                # Play the sound
                if SOUND_LOADED and p.fx_is_on:
                    floor_sound.volume = min(norm([self.dxb, self.dyb]) / 13.0, 1.0)
                    floor_sound.play()

                # Reverse direction of the ball
                self.ue[2] = +p.COR_g[0] * self.ue[2]
                self.ue[3] = -p.COR_g[1] * self.ue[3]

            elif self.net_bounce:
                # Play the sound
                if SOUND_LOADED and p.fx_is_on:
                    floor_sound.volume = min(norm([self.dxb, self.dyb]) / 13.0, 1.0)
                    floor_sound.play()

                # Obtain the bounce velocity
                v_bounce = ball_bounce_net(self)
                self.ue[2] = v_bounce[0]
                self.ue[3] = v_bounce[1]

            # Re-initialize from the event states
            self.t += ddt - tBreak
            dudt = player_and_stool(self.t, self.ue)
            self.u = [self.ue[i] + dudt[i] * (ddt-tBreak) for i in range(20)]

            # The speed of the ball dropped too much, it is now stuck
            if self.floor_bounce and p.volley_mode or sqrt(self.u[2]**2 + self.u[3]**2) < p.dybtol and self.u[1] < 1:
                # Play the sound
                if SOUND_LOADED and p.fx_is_on:
                    stuck_sound.play()

                # Switch the stuck flag
                self.Stuck = True

                # If playing volley drubble, increment the score and restart the game
                if self.volley_game_is_active:
                    self.volley_game_is_active = False
                    if p.volley_mode and self.xb > 0:
                        p.serving_player = 0
                        stats.volley_score[0] += 1
                        print('Player 1 wins point, score is ', stats.volley_score)
                    elif p.volley_mode and self.xb < 0:
                        p.serving_player = 1
                        stats.volley_score[1] += 1
                        print('Player 2 wins point, score is ', stats.volley_score)
                        p.serving_angle, p.serving_speed = randint(55, 78), randint(12, 17)
                        print('  -- New serving angle = ', p.serving_angle, ' deg')
                        print('  -- New serving speed = ', p.serving_speed, ' m/s')

        else:   
            # Update states
            self.u = U[-1]

        # Ensure that the states did not go out of limits, prevent crashing
        self.u[1] = max(self.u[1], p.rb)
        self.u[5] = min(max(self.u[5], p.yp_lim[0]), p.yp_lim[1])
        self.u[6] = min(max(self.u[6], p.lp_lim[0]), p.lp_lim[1])
        self.u[7] = min(max(self.u[7], p.tp_lim[0]), p.tp_lim[1])
        self.u[8] = min(max(self.u[8], p.dxp_lim[0]), p.dxp_lim[1])
        self.u[9] = min(max(self.u[9], p.dyp_lim[0]), p.dyp_lim[1])
        self.u[10] = min(max(self.u[10], p.dlp_lim[0]), p.dlp_lim[1])
        self.u[11] = min(max(self.u[11], p.dtp_lim[0]), p.dtp_lim[1])
        if p.num_player > 1:
            self.u[13] = min(max(self.u[13], p.yp_lim[0]), p.yp_lim[1])
            self.u[14] = min(max(self.u[14], p.lp_lim[0]), p.lp_lim[1])
            self.u[15] = min(max(self.u[15], p.tp_lim[0]), p.tp_lim[1])
            self.u[16] = min(max(self.u[16], p.dxp_lim[0]), p.dxp_lim[1])
            self.u[17] = min(max(self.u[17], p.dyp_lim[0]), p.dyp_lim[1])
            self.u[18] = min(max(self.u[18], p.dlp_lim[0]), p.dlp_lim[1])
            self.u[19] = min(max(self.u[19], p.dtp_lim[0]), p.dtp_lim[1])
        if p.volley_mode:
            if self.u[4] > -0.5 * p.net_width:
                self.u[4] = -0.501 * p.net_width
                self.u[8] = 0.0
            if self.u[12] < 0.5 * p.net_width:
                self.u[12] = 0.501 * p.net_width
                self.u[16] = 0.0
            if self.u[0] <= -p.back_line or self.u[0] >= p.back_line:
                self.u[0] = -p.back_line + 0.001 if self.u[0] < 0 else p.back_line - 0.001
                self.u[2] = - self.u[2] * p.COR_n[0]

        # If stuck, keep it rolling
        if self.Stuck:
            self.u[1] = p.rb
            self.u[2] = (1 - 0.01 * ddt) * self.u[2]
            self.u[3] = 0

        # Predict the future trajectory of the ball
        if 3 < gs.game_mode < 6 or (gs.game_mode == 6 and self.traj['t'][0] - dt < gs.t):
            self.xI, self.yI, self.tI, self.traj, self.timeUntilBounce = ball_predict(self, self.active_player)

        # Stop the ball from moving if it hasn't been launched yet
        if self.game_mode < 6:
            self.t = 0
            self.n = 0
            self.u[0] = p.u0[0]
            self.u[1] = p.u0[1]

        # Named states
        self.xb = self.u[0]  # Ball distance [m]
        self.yb = self.u[1]  # Ball height [m]
        self.dxb = self.u[2]  # Ball horizontal speed [m]
        self.dyb = self.u[3]  # Ball vertical speed [m]
        self.xp = self.u[4:13:8]  # Player distance [m]
        self.yp = self.u[5:14:8]  # Player height [m]
        self.lp = self.u[6:15:8]  # Stool extension [m]
        self.tp = self.u[7:16:8]  # Stool tilt [rad]
        self.dxp = self.u[8:17:8]  # Player horizontal speed [m/s]
        self.dyp = self.u[9:18:8]  # Player vertical speed [m/s]
        self.dlp = self.u[10:19:8]  # Stool extension rate [m/s]
        self.dtp = self.u[11:20:8]  # Stool tilt rate [rad/s]

        # Plotting ranges
        self.xr, self.yr, self.m2p, self.po = set_ranges(self.u, self.screen_width)

        # Stick figures
        for k in range(p.num_player):
            self.stick_dude(k)

    def set_angle_and_speed(self):
        if self.game_mode == 4:
            self.start_angle = 0.25 * pi * (1 + 0.75*sin(self.phase))
        if self.game_mode == 5:
            self.start_speed = p.ss * (1.2 + 0.6*sin(self.phase))
        if self.game_mode == 4 or self.game_mode == 5:
            self.phase += 3 * dt * p.difficult_speed_scale[p.difficult_level]
            start_direction = 1.0 if not p.volley_mode or (p.volley_mode and p.serving_player == 0) else -1.0
            self.u[2] = start_direction * self.start_speed * cos(self.start_angle)
            self.u[3] = self.start_speed * sin(self.start_angle)

    # Solve for the vertices that make up the stick man and stool
    def stick_dude(self, k):
        # Sine and cosine of the tilt angle
        s = sin(self.tp[k])
        c = cos(self.tp[k])

        # Right Foot [rf] Left Foot [lf] Positions
        rf = self.foot_position[k][0]
        lf = self.foot_position[k][1]
        vn = self.dxp[k] / p.vx

        ddt = dt * p.difficult_speed_scale[p.difficult_level]

        rf[2] += p.foot_step_rate * ddt * pi if rf[2] < pi else - pi
        if 0.0 < rf[2] > pi / 2.0:
            desired_foot_position = self.xp[k] + p.foot_step_length * vn - p.stance_width
            rf[0] += p.foot_recovery_rate * ddt * (desired_foot_position - rf[0])
            rf[1] = abs(vn * sin(rf[2]))

        lf[2] += p.foot_step_rate * ddt * pi if lf[2] < pi else - pi
        if 0.0 < lf[2] > pi / 2.0:
            desired_foot_position = self.xp[k] + p.foot_step_length * vn + p.stance_width
            lf[0] += p.foot_recovery_rate * ddt * (desired_foot_position - lf[0])
            lf[1] = abs(vn * sin(lf[2]))

        # Waist Position
        w = self.xp[k], self.yp[k] - p.d

        # Right Knee [rk] Left Knee [lk] Positions
        rk = third_point(w, rf, p.leg_length, -1)
        lk = third_point(w, lf, p.leg_length, 1)

        # Shoulder Position
        sh = self.xp[k], self.yp[k] + p.d
        shl = self.xp[k] - 0.18, self.yp[k] + p.d + 0.05
        shr = self.xp[k] + 0.18, self.yp[k] + p.d + 0.05

        # Right Hand [rh] Left Hand [lh] Position
        r = p.stool_radius[p.difficult_level]
        rh = (self.xp[k] - r * c - (self.lp[k] + p.stool_hand_pos) * s,
              self.yp[k] + p.d - r * s + (self.lp[k] + p.stool_hand_pos) * c)
        lh = (self.xp[k] + r * c - (self.lp[k] + p.stool_hand_pos) * s,
              self.yp[k] + p.d + r * s + (self.lp[k] + p.stool_hand_pos) * c)

        # Right Elbow [re] Left Elbow [le] Position
        re = third_point(shl, rh, 1, 1)
        le = third_point(shr, lh, 1, -1)

        # Stick man vectors in physical units
        xv = rf[0], rk[0], w[0], lk[0], lf[0], lk[0], w[0], sh[0], shl[0], re[0], rh[0], re[0], shl[0], shr[0], le[0], lh[0]
        yv = rf[1], rk[1], w[1], lk[1], lf[1], lk[1], w[1], sh[1], shl[1], re[1], rh[1], re[1], shl[1], shr[1], le[1], lh[1]

        # Plotting vectors
        px, py = xy2p(xv, yv, self.m2p, self.po, self.screen_width, self.screen_height)
        self.player[k] = intersperse(px, py)


gs = GameState()


class GameScore:
    # Set the high score file path and name
    high_score_file = 'score.json'
    store = None

    # Initialize the volleyball game scores
    all_volley_score = [[], [], []]
    streak = [0, 0, 0]
    volley_record = [[0, 0], [0, 0], [0, 0]]

    # Initialize all scores as empty arrays
    all_stool_dist = [[[], []], [[], []], [[], []]]
    all_height = [[[], []], [[], []], [[], []]]
    all_stool_count = [[[], []], [[], []], [[], []]]
    all_score = [[[], []], [[], []], [[], []]]

    # Initialize high scores as zero
    high_stool_dist = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    high_height = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    high_stool_count = [[0, 0], [0, 0], [0, 0]]
    high_score = [[0, 0], [0, 0], [0, 0]]

    # Initiate statistics as zeros
    def __init__(self):
        # Timing
        self.t = 0
        self.n = 0
        # self.average_step_time = 0

        # Scores for the current game
        if p.volley_mode:
            self.volley_score = [0, 0]
        else:
            self.stool_count = 0
            self.stool_dist = 0
            self.max_height = 0
            self.floor_count = 0
            self.score = 0
        
    # Update statistics for the current game state    
    def update(self):
        self.t = gs.t
        self.n = gs.n
        if p.volley_mode:
            # Update the volleyball game score
            if gs.xb < 0:
                self.volley_score[0] += 1
            else:
                self.volley_score[1] += 1
        else:
            if gs.stool_bounce and self.stool_dist < gs.xb:
                self.stool_dist = gs.xb
            if self.max_height < gs.yb and self.stool_count > 0:
                self.max_height = gs.yb
            self.stool_count += gs.stool_bounce
            self.floor_count += gs.floor_bounce
            self.score = int(self.stool_dist * self.max_height * self.stool_count)

    # Initialize high scores from the user_data_dir
    def init_high(self, high_score_file='score.json'):
        # Initialize the JsonStore
        self.high_score_file = high_score_file
        print('Attempting to initialize high scores at ' + self.high_score_file)
        self.store = JsonStore(high_score_file)

        # Import high scores, or set to zero
        try:
            # Load from JsonStore
            p.difficult_level = self.store.get('difficult_level')['value']
            self.all_volley_score = self.store.get('all_volley_score')['value']
            self.volley_record = self.store.get('volley_record')['value']
            self.streak = self.store.get('streak')['value']
            self.all_stool_dist = self.store.get('all_stool_dist')['value']
            self.all_height = self.store.get('all_height')['value']
            self.all_stool_count = self.store.get('all_stool_count')['value']
            self.all_score = self.store.get('all_score')['value']
            self.high_stool_dist = self.store.get('high_stool_dist')['value']
            self.high_height = self.store.get('high_height')['value']
            self.high_stool_count = self.store.get('high_stool_count')['value']
            self.high_score = self.store.get('high_score')['value']
            print('  Successfully imported high scores')
        except:
            print('  Failed importing high scores, creating store')

    # Update high scores
    def update_high(self):
        # Indices for the high scores
        j = p.difficult_level
        k = p.num_player - 1

        if p.volley_mode:
            # Append to the complete database
            self.all_volley_score[j].append(self.volley_score)

            # Increment the all time record and winning/losing streak
            if self.volley_score[0] > self.volley_score[1]:
                # Player won
                self.volley_record[j][0] += 1
                self.streak[j] = self.streak[j] + 1 if self.streak[j] > 0 else 1
            elif self.volley_score[0] < self.volley_score[1]:
                # Opponent won
                self.volley_record[j][1] += 1
                self.streak[j] = self.streak[j] - 1 if self.streak[j] < 0 else -1
        else:
            # Append to the complete database
            self.all_stool_dist[j][k].append(self.stool_dist)
            self.all_height[j][k].append(self.max_height)
            self.all_stool_count[j][k].append(self.stool_count)
            self.all_score[j][k].append(self.score)

            # Determine if this is a new high in any category
            self.high_stool_dist[j][k] = max(self.high_stool_dist[j][k], self.stool_dist)
            self.high_height[j][k] = max(self.high_height[j][k], self.max_height)
            self.high_stool_count[j][k] = max(self.high_stool_count[j][k], self.stool_count)
            self.high_score[j][k] = max(self.high_score[j][k], self.score)

        # Write to file
        try:
            self.store.put('difficult_level', value=p.difficult_level)
            self.store.put('all_volley_score', value=self.all_volley_score)
            self.store.put('volley_record', value=self.volley_record)
            self.store.put('streak', value=self.streak)
            self.store.put('all_stool_dist', value=self.all_stool_dist)
            self.store.put('all_height', value=self.all_height)
            self.store.put('all_stool_count', value=self.all_stool_count)
            self.store.put('all_score', value=self.all_score)
            self.store.put('high_stool_dist', value=self.high_stool_dist)
            self.store.put('high_height', value=self.high_height)
            self.store.put('high_stool_count', value=self.high_stool_count)
            self.store.put('high_score', value=self.high_score)
        except:
            print('failed exporting high scores to ', self.high_score_file)


stats = GameScore()


# Determine from the stats what percentile the current game is, return string forms
def return_percentile(all_stats, this_stat):
    if len(all_stats) == 0 and this_stat > 0:
        # First run, so must be a new high
        return 'New High!'
    elif len(all_stats) == 0 and this_stat == 0:
        # First run, but didn't do anything
        return ' '
    else:
        percent = 100 * len([i for i in all_stats if i > this_stat]) / len(all_stats)
        if percent > 50.0:
            percent = 100 - percent
            percent_str = 'Bottom %0.0f%%' % percent
        else:
            percent_str = 'Top %0.0f%%' % percent
        return percent_str


def cycle_modes(gs, stats, engine):
    # Exit splash screen
    if gs.game_mode == 1:
        gs.game_mode += 1
        return

    # Exit options screen
    if gs.game_mode == 2:
        # Reset game
        stats.__init__()
        if p.volley_mode:
            p.u0[0] = - (p.back_line - 1) if p.serving_player == 0 else p.back_line - 1
            p.u0[4] = - p.back_line / 2.0
            p.u0[12] = p.back_line / 2.0
        else:
            p.u0[0] = 0.0
            p.u0[4] = 5.0
            p.u0[12] = 0.0
        gs.__init__(p.u0, engine)
        gs.game_mode = 3
        return

    # Progress through angle and speed selection
    if gs.game_mode == 3 or gs.game_mode == 4:
        gs.game_mode += 1
        gs.phase = 0
        return

    # Start the ball moving!
    if gs.game_mode == 5:
        gs.game_mode = 6
        return

    # Show the high scores
    if gs.game_mode == 6:
        if p.volley_mode and stats.volley_score[0] < p.winning_score and stats.volley_score[1] < p.winning_score:
            p.u0[0] = - (p.back_line - 1) if p.serving_player == 0 else p.back_line - 1
            p.u0[4] = - p.back_line / 2.0
            p.u0[12] = p.back_line / 2.0
            gs.__init__(p.u0, engine)
            gs.game_mode = 3
        else:
            gs.game_mode = 7
        return

    # Reset the game
    if gs.game_mode == 7 and p.volley_mode:
        p.u0[0] = - (p.back_line - 1) if p.serving_player == 0 else p.back_line - 1
        p.u0[4] = - p.back_line / 2.0
        p.u0[12] = p.back_line / 2.0
        stats.__init__()
        gs.__init__(p.u0, engine)
        gs.game_mode = 3
    else:
        stats.__init__()
        gs.__init__(p.u0, engine)
        gs.game_mode = 3
        return


# Equation of Motion
def player_and_stool(t, u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    # Initialize output
    du = zeros(20)
    du[0:4] = [dxb, dyb, 0, -p.g]  # Ball velocities and accelerations
    
    # Loop over players
    for k in range(p.num_player):
        # Sines and cosines of the stool angle
        s = sin(tp[k])
        c = cos(tp[k])
        
        # Mass Matrix
        if USE_NUMPY:
            # Create player state vectors
            q = np.array([[xp[k]], [yp[k]], [lp[k]], [tp[k]]])
            dq = np.array([[dxp[k]], [dyp[k]], [dlp[k]], [dtp[k]]])

            if not p.linearMass:
                M = np.array([[p.m,                   0,          -p.mg * s, -p.mg * lp[k] * c],
                              [0,                    p.m,          p.mg * c, -p.mg * lp[k] * s],
                              [-p.mg * s,          p.mg * c,       p.mg,            0],
                              [-p.mg * lp[k]*c, -p.mg * lp[k] * s,   0,       p.mg * lp[k]**2]])

            # Centripetal [0,1] and Coriolis [3] Force Vector
            D = np.array([[- 2.0 * p.mg * dlp[k] * dtp[k] * c + p.mg * lp[k] * s * dtp[k]**2],
                          [- 2.0 * p.mg * dlp[k] * dtp[k] * s - p.mg * lp[k] * c * dtp[k]**2],
                          [- p.mg * lp[k] * dtp[k]**2],
                          [2.0 * p.mg * lp[k] * dlp[k] * dtp[k]]])

            # Gravitational Force Vector
            G = np.array([[0.0],
                          [p.m * p.g],
                          [p.mg * p.g * c],
                          [-p.mg * p.g * lp[k] * s]])

            # Fix the time, if supplied as tspan vector
            if np.size(t) > 1:
                t = t[0]
        
        # Control inputs form the generalized forces
        Qx, Qy, Ql, Qth = control_logic(u, k)

        # Equilibrium stool angle
        Teq = atan2(xp[k] - xb,yb - p.d - yp[k]), atan2(xp[k] - gs.xI, gs.yI - p.d - yp[k])
        w = (1.0 + 2.0 * erf(0.2 * abs(xp[k]-gs.xI))) / 3.0
        teq = min(max(w * Teq[0] + (1.0 - w) * Teq[1], -0.5), 0.5)

        # Equation of Motion
        if USE_NUMPY:
            Q = np.array([[Qx], [Qy], [Ql], [Qth]])
            p.q0_array[3] = teq
            rhs = - p.C.dot(dq) - p.K.dot(q) + p.K.dot(p.q0_array) - D - G + Q
            if p.linearMass:
                ddq = p.invM.dot(rhs)
            else:
                ddq = np.linalg.inv(M).dot(rhs)
        else:

            # Equations of motion, created in the Jupyter notebook eom.ipynb
            ddq = [None, None, None, None]
            ddq[0] = (-p.Cl*dlp[k]*lp[k]*s - p.Ct*dtp[k]*c - p.Cx*dxp[k]*lp[k] + p.Kl*p.l0*lp[k]*s - p.Kl*lp[k]**2*s
                      - p.Kt*tp[k]*c + Ql*lp[k]*s + Qth*c + Qx*lp[k]) / (p.mc*lp[k])
            ddq[1] = (-(p.Ct*dtp[k] + p.Kt*tp[k] - Qth + 2.0*dlp[k]*dtp[k]*p.mg*lp[k] - p.g*p.mg*lp[k]*s)*s
                      + (p.Cl*dlp[k] - p.Kl*p.l0 + p.Kl*lp[k] - Ql - dtp[k]**2*p.mg*lp[k] + p.g*p.mg*c)*lp[k]*c
                      - (p.Cy*dyp[k] - p.Ky*p.y0 + p.Ky*yp[k] - Qy - 2.0*dlp[k]*dtp[k]*p.mg*s - dtp[k]**2*p.mg*lp[k]*c
                         + p.g*p.mc + p.g*p.mg)*lp[k])/(p.mc*lp[k])
            ddq[2] = -p.Cl*dlp[k]/p.mg - p.Cl*dlp[k]/p.mc - p.Cx*dxp[k]*s/p.mc + p.Cy*dyp[k]*c/p.mc + p.Kl*p.l0/p.mg + p.Kl*p.l0/p.mc - p.Kl*lp[k]/p.mg - p.Kl*lp[k]/p.mc - p.Ky*p.y0*c/p.mc + p.Ky*yp[k]*c/p.mc + Ql/p.mg + Ql/p.mc + Qx*s/p.mc - Qy*c/p.mc + dtp[k]**2*lp[k]
            ddq[3] = (-p.Ct*dtp[k]*p.mc - p.Ct*dtp[k]*p.mg - p.Cx*dxp[k]*p.mg*lp[k]*c - p.Cy*dyp[k]*p.mg*lp[k]*s - p.Kt*p.mc*(tp[k]-teq) - p.Kt*p.mg*(tp[k]-teq) + p.Ky*p.mg*p.y0*lp[k]*s - p.Ky*p.mg*lp[k]*yp[k]*s + Qth*p.mc + Qth*p.mg + Qx*p.mg*lp[k]*c + Qy*p.mg*lp[k]*s - 2.0*dlp[k]*dtp[k]*p.mc*p.mg*lp[k])/(p.mc*p.mg*lp[k]**2)

        # Output state derivatives (Player velocities and accelerations)
        i1 = k * 8 + 4
        i2 = k * 8 + 12
        if USE_NUMPY:
            du[i1:i2] = [dxp[k], dyp[k], dlp[k], dtp[k], ddq[0, 0], ddq[1, 0], ddq[2, 0], ddq[3, 0]]
        else:
            du[i1:i2] = [dxp[k], dyp[k], dlp[k], dtp[k], ddq[0], ddq[1], ddq[2], ddq[3]]
    
    return du


def ctrl2keyPush(gs):
    keyPush = gs.keyPush
    if gs.ctrl[0] < 0:
        keyPush[0] = -gs.ctrl[0]
    elif gs.ctrl[0] > 0:
        keyPush[1] = gs.ctrl[0]
    if gs.ctrl[1] > 0:
        keyPush[2] = gs.ctrl[1]
    elif gs.ctrl[1] < 0:
        keyPush[3] = -gs.ctrl[1]    
    if gs.ctrl[2] > 0:
        keyPush[4] = gs.ctrl[2]
    elif gs.ctrl[2] < 0:
        keyPush[5] = -gs.ctrl[2]
    if gs.ctrl[3] > 0:
        keyPush[6] = gs.ctrl[3]
    elif gs.ctrl[3] < 0:
        keyPush[7] = -gs.ctrl[3]  
    return keyPush


def kvUpdateKey(keyPush, keycode, val):
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


def control_logic(u, k):
    # Initialize the list of generalized forces
    Q = [0.0, 0.0, 0.0, 0.0]

    # If the ball is stuck, then stop making the computer move
    if gs.Stuck:
        return Q

    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)
    
    # Run to the projected intercept point (pip). If the computer
    # Is the active player, this will be at gs.xI, otherwise will be at
    # gs.xI + 10
    if p.volley_mode:
        player_run_ahead = 10.0 if gs.xI < 0 and k is 1 else 0.0
    else:
        player_run_ahead = 0.0 if k == gs.active_player else 10.0
    diff_distance =  (2.0 * k - 1) * 0.4 if p.volley_mode else -0.25
    pip = gs.xI + player_run_ahead + diff_distance
    if p.userControlled[k][0]:
        Q[0] = p.Qx * (1.5 * gs.ctrl[0] - 0.5 * erf(dxp[k]))
    else:
        if gs.timeUntilBounce > 0:
            if pip - xp[k] > 3:
                Q[0] = p.Qx
            elif pip - xp[k] < -3:
                Q[0] = - p.Qx
            else:
                Q[0] = p.Qx * min(max(p.Gx * (pip - xp[k]) - 0.4 * dxp[k], -1), 1)
        else:
            Q[0] = p.Qx * min(max(p.Gx * (xb - xp[k] + player_run_ahead), -1), 1)
    
    # Control leg extension based on timing, turn on when impact in <0.2 sec
    if p.userControlled[k][1]:
        Q[1] = p.Qy * gs.ctrl[1]
    else:
        if (gs.timeUntilBounce < 0.6) and (gs.timeUntilBounce > 0.4):
            Q[1] = - p.Qy
        elif abs(gs.timeUntilBounce) < 0.2:
            Q[1] = p.Qy

    # Control arm extension based on timing, turn on when impact in <0.2 sec
    if p.userControlled[k][2]:
        Q[2] = p.Ql * gs.ctrl[2]
    else:
        Q[2] = p.Ql * (abs(gs.timeUntilBounce) < 0.2)
    
    # Control stool angle by pointing at the ball
    dx = xb - xp[k]  # Ball distance - player distance
    dy = yb - yp[k] - p.d
    want_angle = atan2(-dx, dy)
    if p.userControlled[k][3]:
        Q[3] = p.Qt * gs.ctrl[3]
    else:
        Q[3] = p.Qt * p.Gt * (want_angle-tp[k])
        if Q[3] > p.Qt:
            Q[3] = p.Qt
        elif Q[3] < -p.Qt or (0 < gs.timeUntilBounce < 0.017):
            Q[3] = - p.Qt

    if USE_NUMPY:
        return np.array(Q)
    else:
        return Q


def ball_hit_floor(t, u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u) 
    return yb - p.rb


def ball_hit_stool(t, u, k):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)

    # Calculate the stool locations
    s = sin(tp[k])
    c = cos(tp[k])
    r = p.stool_radius[p.difficult_level]
    sx = xp[k] - r * c - lp[k] * s, xp[k] + r * c - lp[k] * s
    sy = yp[k] + p.d - r * s + lp[k] * c, yp[k] + p.d + r * s + lp[k] * c

    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = sx[1] - sx[0], sy[1] - sy[0]
    
    # Calculate z that minimizes the distance
    z = ((xb - sx[0]) * r1[0] + (yb - sy[0]) * r1[1]) / (r1[0]**2 + r1[1]**2)
    
    # Find the closest point of impact on the stool
    if z < 0:
        ri = sx[0], sy[0]
    elif z > 1:
        ri = sx[1], sy[1]
    else:
        ri = sx[0] + z * r1[0], sy[0] + z * r1[1]

    # Vector from the closest point of impact to the center of the ball    
    r2 = xb - ri[0], yb - ri[1]

    # Calculate the distance to the outer radius of the ball t
    return norm(r2) - p.rb


def ball_bounce_stool(gs, k):
    # Calculate sines and cosines of the tilt angle
    c = cos(gs.tp[k])
    s = sin(gs.tp[k])

    # Calculate the stool locations
    r = p.stool_radius[p.difficult_level]
    sx = gs.xp[k] - r * c - gs.lp[k] * s, gs.xp[k] + r * c - gs.lp[k] * s
    sy = gs.yp[k] + p.d - r * s + gs.lp[k] * c, gs.yp[k] + p.d + r * s + gs.lp[k] * c

    # Vectors from the left edge of the stool to the right, and to the ball
    r1 = sx[1] - sx[0], sy[1] - sy[0]

    # Calculate z that minimizes the distance
    z = ((gs.xb - sx[0]) * r1[0] + (gs.yb - sy[0]) * r1[1]) / (r1[0] ** 2 + r1[1] ** 2)

    # Find the closest point of impact on the stool
    if z < 0:
        ri = sx[0], sy[0]
    elif z > 1:
        ri = sx[1], sy[1]
    else:
        ri = sx[0] + z * r1[0], sy[0] + z * r1[1]

    # Velocity of the stool at the impact point 
    vi = (gs.dxp[k] - gs.lp[k] * s - (ri[1] - gs.yp[k]) * gs.dtp[k],
          gs.dyp[k] + gs.lp[k] * c + (ri[0] - gs.xp[k]) * gs.dtp[k])

    # Velocity and speed of the ball relative to impact point
    vbrel = gs.dxb - vi[0], gs.dyb - vi[1]

    # Vector from the closest point of impact to the center of the ball    
    r2 = gs.xb - ri[0], gs.yb - ri[1]
    nr2 = norm(r2)
    u2 = r2[0] / nr2, r2[1] / nr2

    # Relative velocity of the ball projected into the vector u2
    vbrel_proj = vbrel[0] * u2[0], vbrel[1] * u2[1]

    # Relative speed of the ball, projected into the vector u2
    srel = norm(vbrel_proj)

    # Delta ball velocity
    delta_vb = 2.0 * p.COR_s[0] * u2[0] * srel, 2.0 * p.COR_s[1] * u2[1] * srel

    if USE_NUMPY:
        # Velocity after bounce
        v_bounce = np.array(delta_vb) + np.array([gs.dxb, gs.dyb])

        # Obtain the generalized impulse
        bounce_impulse = -p.mg * v_bounce
        dRdq = np.array([[1.0, 0.0],
                         [0.0, 1.0],
                         [-s, c],
                         [-c * gs.lp[k], -s * gs.lp[k]]])
        Qi = dRdq.dot(bounce_impulse)

        # Obtain the player recoil states
        v_recoil = p.invM.dot(Qi)
    else:
        # Velocity after bounce
        v_bounce = delta_vb[0] + gs.dxb, delta_vb[1] + gs.dyb

        # Obtain the generalized impulse
        bounce_impulse = -p.mg * v_bounce[0], -p.mg * v_bounce[1]
        Q = (bounce_impulse[0], bounce_impulse[1],
             -s * bounce_impulse[0] + c * bounce_impulse[1],
             -c * gs.lp[k] * bounce_impulse[0] - s * gs.lp[k] * bounce_impulse[1])

        # Obtain the player recoil states
        v_recoil = (Q[2] * s / p.mc + Q[3] * c / (p.mc * gs.lp[k]) + Q[0] / p.mc,
                    - Q[2] * c / p.mc + Q[3] * s / (p.mc * gs.lp[k]) + Q[1] / p.mc,
                    Q[2] * (1.0 / p.mg + 1.0 / p.mc) + Q[0] * s / p.mc - Q[1] * c / p.mc,
                    Q[3] * (p.mc + p.mg) / (p.mc * p.mg * gs.lp[k] ** 2)
                    + Q[0] * c / (p.mc * gs.lp[k]) + Q[1] * s / (p.mc * gs.lp[k]))

    return v_bounce, v_recoil


def ball_hit_net(t, u):
    # Unpack the state variables
    xb, yb, dxb, dyb, xp, yp, lp, tp, dxp, dyp, dlp, dtp = unpackStates(u)

    # Calculate the distance from the ball to the edge of the net
    if yb >= p.net_height:
        return norm([xb, yb - p.net_height]) - 0.5 * p.net_width - p.rb
    elif xb <= 0:
        return - xb - 0.5 * p.net_width - p.rb
    else:
        return xb - 0.5 * p.net_width - p.rb


def ball_bounce_net(gs):
    # Calculate the unit vector from the net to the ball
    if gs.yb >= p.net_height:
        r = [gs.xb, gs.yb - p.net_height]
    else:
        r = [gs.xb, 0]
    nr = norm(r)    
    u = [r[0] / nr, r[1] / nr]    
    
    # Calculate the ball speed projected onto the unit vector
    s = norm([gs.dxb * u[0], gs.dyb * u[1]])
    
    # Return the ball velocity after recoil
    return gs.dxb + 2.0 * s * u[0] * p.COR_n[0], gs.dyb + 2.0 * s * u[1] * p.COR_n[1]


# Make the events terminal
ball_hit_floor.terminal = True
ball_hit_stool.terminal = True
ball_hit_net.terminal = True        


def norm(V):
    variance = 0
    for v in V:
        variance += v**2
    return sqrt(variance)


# Solves for the location of the knee or elbow based upon the two other 
# end-points of the triangle 
def third_point(P0, P1, L, SGN):
    # Subtract then add the two points
    Psub = [P0[0]-P1[0], P0[1]-P1[1]]
    Padd = [P0[0]+P1[0], P0[1]+P1[1]]

    # Calculate the midpoint between the two
    P2 = [Padd[0]/2.0, Padd[1]/2.0]

    # Distance between point P0, P1
    d = norm(Psub)

    if d > L:
        # P0 and P1 are too far apart to form a knee, use the midpoint
        P3 = P2
    else:
        a = (d**2)/2.0/d  # Distance to mid-Point
        h = sqrt((L**2)/4.0 - a**2)
        x3 = P2[0] + h*SGN*Psub[1]/d
        y3 = P2[1] - h*SGN*Psub[0]/d
        P3 = [x3, y3]
    return P3


# Solve for the x and y ranges to include in the plot, scale factors to 
# convert from meters to pixels, and pixel offset to the center line
# Ratio refers to normalized positions in the window on the scale [0 0 1 1]
def set_ranges(u, w):
    # Ranges are determined by the maximum height of the stool, and differential between ball and player
    max_y = 1.1 * max([u[1], u[5] + p.d + u[6] * cos(u[7]), 3.0])
    diff_x = abs(u[0] - u[4])

    # Left and right edges are defined as the midpoint between ball and stool,
    # plus or minus the maximum height and half the differential distance.
    mid_x = (u[0] + u[4]) / 2.0
    x_rng = mid_x - max_y - 0.5 * diff_x, mid_x + max_y + 0.5 * diff_x

    # Bottom and top edges are defined as -1 meter and the max height
    # plus half the differential distance
    y_rng = -1.0, max_y + 0.5 * (diff_x - 0.5)

    # Meter to pixel conversion is the screen width divided by differential
    # distance. Pixel offset is the mean of the ranges, scaled to pixels.
    meter_to_pixel = w / (x_rng[1] - x_rng[0])
    pixel_offset = (x_rng[0] + x_rng[1]) / 2.0 * meter_to_pixel
    return x_rng, y_rng, meter_to_pixel, pixel_offset


def intersperse(list1, list2):
    result = [None] * (len(list1) + len(list2))
    result[::2] = list1
    result[1::2] = list2
    return result


# Below this line are the functions I created when I started demoDrubble,
# these are basically obsolete, eventually will be deleted
defObsoleteDemoFuncs = False
if defObsoleteDemoFuncs:

    # Solve for the vertices that make up the stick man and stool
    def stick_dude(inp, k):
        k8 = k * 8
        # Get the state variables
        try:
            # States from u
            x = inp[4 + k8]
            y = inp[5 + k8]
            l = inp[6 + k8]
            th = inp[7 + k8]
            v = inp[8 + k8]
        except:
            # States from gs
            x = inp.xp[k]
            y = inp.yp[k]
            l = inp.lp[k]
            th = inp.tp[k]
            v = inp.dxp[k]

        s = sin(th)
        c = cos(th)

        # Right Foot [rf] Left Foot [lf] Positions
        vn = v / p.vx
        rf = x - 0.25 + vn * sin(1.5 * x + 3.0 * pi / 2.0), 0.2 * vn * (1.0 + sin(1.5 * x + 3.0 * pi / 2.0))
        lf = x + 0.25 + vn * cos(1.5 * x), 0.2 * vn * (1.0 + cos(1.5 * x))

        # Waist Position
        w = (x, y - p.d)

        # Right Knee [rk] Left Knee [lk] Positions
        rk = third_point(w, rf, p.y0 - p.d, -1)
        lk = third_point(w, lf, p.y0 - p.d, 1)

        # Shoulder Position
        sh = x, y + p.d
        shl = x - 0.18, y + p.d + 0.05
        shr = x + 0.18, y + p.d + 0.05

        # Right Hand [rh] Left Hand [lh] Position
        r = p.stool_radius[p.difficult_level]
        rh = x - r * c - (l + p.stool_hand_pos) * s, y + p.d - r * s + (l + p.stool_hand_pos) * c
        lh = x + r * c - (l + p.stool_hand_pos) * s, y + p.d + r * s + (l + p.stool_hand_pos) * c

        # Right Elbow [re] Left Elbow [le] Position
        re = third_point(shl, rh, 1, 1)
        le = third_point(shr, lh, 1, -1)

        # Plotting vectors
        xv = rf[0], rk[0], w[0], lk[0], lf[0], lk[0], w[0], sh[0], shl[0], re[0], rh[0], re[0], shl[0], shr[0], le[0], \
             lh[0]
        yv = rf[1], rk[1], w[1], lk[1], lf[1], lk[1], w[1], sh[1], shl[1], re[1], rh[1], re[1], shl[1], shr[1], le[1], \
             lh[1]

        return xv, yv


    class DrumBeat:
        def __init__(self):
            self.n = 0
            self.bpm = 105.0  # Beats per minute
            self.npb = round(fs * 60.0 / 4.0 / self.bpm)  # frames per beat
            self.nps = 16.0 * self.npb  # frames per sequence
            # self.sequence = [[1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
            #                 [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
            #                 [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],
            #                 [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0]]
            # self.sequence = [[1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0],
            #                 [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
            #                 [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
            #                [0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0]]
            try:
                self.drum = ['a/01_kick.wav',
                             'a/04_snare2.wav',
                             'a/06_openHat6.wav',
                             'a/09_hiConga2.wav']
                self.loop = ['a/00-DC-Base.mp3', 'a/01-DC-Base.mp3']
            except:
                self.drum = []
                self.loop = []
                self.drum.append(SoundLoader.load('a/01_kick.wav'))
                self.drum.append(SoundLoader.load('a/04_snare2.wav'))
                self.drum.append(SoundLoader.load('a/06_openHat6.wav'))
                self.drum.append(SoundLoader.load('a/09_hiConga2.wav'))
                self.loop.append(SoundLoader.load('a/00-DC-Base.mp3'))
                self.loop.append(SoundLoader.load('a/01-DC-Base.mp3'))
                self.loop[0].play()

            self.m = 4
            self.randFactor = 1.0
            self.nloops = 2

        def play_ista(self):
            whichSequence = np.floor(self.n / self.nps)
            whereInSequence = self.n - whichSequence * self.nps
            beat = whereInSequence / self.npb
            numDrums = max(1, gs.game_mode - 2)
            if not np.mod(beat, 1):
                b = int(beat)
                for k in range(numDrums):
                    if self.sequence[k][b] or np.random.uniform() > self.randFactor:
                        sound.play_effect(self.drum[k])
            self.n += 1

        def play_kivy(self):
            for k in range(self.m):
                if self.sequence[k][self.n] or np.random.uniform() > self.randFactor:
                    self.drum[k].play()

            self.n += 1
            if self.n >= 16:
                self.n = 0

        def check_kivy(self):
            pass

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
            Ls[n] = ball_hit_stool(T[n],Y[n,:])
            Lf[n] = ball_hit_floor(T[n],Y[n,:])
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
        # Get the plotting vectors using stick_dude function
        xv, yv, sx, sy = stick_dude(Y[n,:])
    
        # Get state variables
        x = Y[n, 4]  # sol.y[0,n]
        y = Y[n, 5]  # sol.y[1,n]
        l = Y[n, 6]  # sol.y[2,n]
        th = Y[n, 7]  # sol.y[3,n]
    
        # Update the plot
        LN.set_data(xv, yv)
        HD.set_data(x,y+p.d*1.6)
        GD.set_data(np.round(x+np.linspace(-40,40,81)),0)
        ST.set_data(sx,sy)
        BL.set_data(Y[n,8],Y[n,9])
        BA.set_data(XB[n,:],YB[n,:])
        
        # Update Axis Limits
        xrng, yrng, m2p, po = set_ranges(Y[n,:])
        ax.set_xlim(xrng)
        ax.set_ylim(yrng)
        
        return LN, HD, GD, ST, BL, BA,


    class playerLines():
        def __init__(self, pnum, gs, w, h):
            self.pnum = pnum
            self.width = w
            self.height = h
            self.update(gs, w)
            self.sv = []
            self.yv = []
            self.xrng = []
            self.yrng = []
            self.m2p = []
            self.po = []

        def update(self, gs, w):
            # Get the player stick figure
            self.xv, self.yv = stick_dude(gs, self.pnum)

            # Get ranges for drawing the player and ball
            self.xrng, self.yrng, self.m2p, self.po = set_ranges(gs.u, w)

            # Convert to pixels
            self.player_x, self.player_y = xy2p(self.xv, self.yv, self.m2p, self.po,
                                                self.width, self.height)
            # self.stool_x, self.stool_y = xy2p(self.sx, self.sy, self.m2p, self.po,
            #                                 self.width, self.height)

            # Convert to format used for Kivy line
            self.player = intersperse(self.player_x, self.player_y)
            # self.stool = intersperse(self.stool_x, self.stool_y)