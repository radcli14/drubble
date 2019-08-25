# Import the supporting functions and classes
engine = 'ista'
from scene import *
import motion
import ui
import scene_drawing
import sound
import numpy as np
from drubbleFunc import *

# Window size
width = max(get_screen_size())
height = min(get_screen_size())

def makeSplashScreen(obj):
    if gs.showedSplash:
        obj.background_color = skyBlue
        image(splash, 0, 0, width, height)
    else:
        k = float(obj.kSplash) / 255.0
        obj.background_color = (skyBlue[0] * k, skyBlue[1] * k, skyBlue[2] * k)
        image(splash, 0, 0, width, height)
        if k >= 1:
            gs.showedSplash = True


def linePlot(x, y, m2p, po, w, h, clr, wgt):
    x, y = xy2p(x, y, m2p, po, w, h)
    stroke(clr)
    stroke_weight(wgt)
    for k in range(1, np.size(x)):
        line(x[k - 1], y[k - 1], x[k], y[k])


def initStick(self, alph, sz, ap, ps):
    Stick = SpriteNode('a/crossHair.png', parent=self)
    Stick.size = (sz, sz)
    Stick.anchor_point = ap
    Stick.position = ps
    Stick.x = (ps[0] - ap[0] * sz, ps[0] + (1 - ap[0]) * sz)
    Stick.y = (ps[1] - ap[1] * sz, ps[1] + (1 - ap[1]) * sz)
    Stick.cntr = ((Stick.x[0] + Stick.x[1]) / 2, (Stick.y[0] + Stick.y[1]) / 2)
    Stick.ctrl = (0, 0)
    Stick.id = None

    Aura = SpriteNode('shp:Circle')
    # Aura = ShapeNode(circle,'white')
    # circle = ui.Path.oval (0, 0, 0.5*sz,0.5*sz)
    Aura.size = (0.5 * sz, 0.5 * sz)
    Aura.position = Stick.cntr
    return Stick, Aura


def touchStick(loc, stick):
    tCnd = [loc[0] > stick.x[0],
            loc[0] < stick.x[1],
            loc[1] > stick.y[0],
            loc[1] < stick.y[1]]

    # Touched inside the stick
    if all(tCnd):
        x = min(max(p.tsens * (2 * (loc[0] - stick.x[0]) / stick.size[0] - 1), -1), 1)
        y = min(max(p.tsens * (2 * (loc[1] - stick.y[0]) / stick.size[1] - 1), -1), 1)

        #mag = np.sqrt(x ** 2 + y ** 2)
        #ang = np.around(4 * np.arctan2(y, x) / np.pi) * np.pi / 4

        #return (mag * np.cos(ang), mag * np.sin(ang))
        return x, y
    else:
        return (0, 0)


def toggleVisibleSprites(self, boule):
    if boule:
        self.moveStick.alpha = 0.5
        self.moveAura.alpha = 0.5
        self.tiltStick.alpha = 0.5
        self.tiltAura.alpha = 0.5
        self.add_child(self.ball)
        self.add_child(self.head)
        self.add_child(self.stool)
        if p.nPlayer > 1:
            self.add_child(self.head1)
            self.add_child(self.stool1)
        self.time_label.alpha = 1
        self.dist_label.alpha = 1
        self.high_label.alpha = 1
        self.boing_label.alpha = 1
        self.score_label.alpha = 1
        self.actionButt.add()
        self.option_butt.add()
    else:
        self.moveStick.alpha = 0
        self.moveAura.alpha = 0
        self.tiltStick.alpha = 0
        self.tiltAura.alpha = 0
        self.ball.remove_from_parent()
        self.head.remove_from_parent()
        self.head1.remove_from_parent()
        self.stool.remove_from_parent()
        self.stool1.remove_from_parent()
        self.time_label.alpha = 0
        self.dist_label.alpha = 0
        self.high_label.alpha = 0
        self.boing_label.alpha = 0
        self.score_label.alpha = 0
        self.actionButt.rm()
        self.option_butt.rm()

def makeMarkers(xrng, m2p, po):

    xrng_r = np.around(xrng, -1)
    xrng_n = int((xrng_r[1] - xrng_r[0]) / 10.0) + 1
    for k in range(0, xrng_n):
        xr = xrng_r[0] + 10 * k

        [start_x, start_y] = xy2p(xr, 0, m2p, po, width, height)
        [end_x, end_y] = xy2p(xr, -1, m2p, po, width, height)
        stroke(white)
        stroke_weight(1)
        line(start_x, start_y, end_x, end_y)
        fsize = min(24, int(m2p))
        text(str(int(xr)), font_name=p.MacsFavoriteFont, font_size=fsize, x=start_x - 2,
             y=start_y + m2p / 20.0, alignment=1)


# Set the keyboard input and mouse defaults
keyPush = np.zeros(8)

# Initialize gamestate
gs = GameState(p.u0, engine)

# Initialize stats
stats = GameScore()

# Initialize drums
drums = DrumBeat()
drum_player = [sound.Player(drums.loop[k]) for k in range(drums.nloops)]

class MyBackground:
    # Size of the black bar on the bottom of the screen
    bottomLineHeight = height / 20.0

    # Set size of the background, before updates
    sz_orig = w_orig, h_orig = (2400.0, 400.0)

    # Number of background images
    num_bg = 3

    # Import the background images
    bg = []
    for n in range(num_bg):
        name = 'a/bg' + str(n) + '.png'
        bg.append(scene_drawing.load_image_file(name))

    # Randomize the start location in the background
    xpos = np.random.rand() * 100.0 * num_bg

    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)

        self.width = width
        self.height = height

    def update(self, x, y, w, h, m2p): 
        # xmod is normalized position of the player between 0 and num_bg
        xmod = np.mod(x+self.xpos, 100.0*self.num_bg)/100.0
        xrem = np.mod(xmod, 1)
        xflr = int(np.floor(xmod))

        # xsel selects which background textures are used TBR
        if xrem <= 0.5:
            xsel = xflr - 1
        else:
            xsel = xflr

        # scf is the scale factor to apply to the background
        scf = (m2p / 70.0) ** 0.5
        img_w = int(np.around(self.w_orig * scf))
        img_h = int(np.around(self.h_orig * scf))

        # Decide which textures are used
        idx_left = xsel
        if xsel < (self.num_bg - 1):
            idx_right = xsel + 1
        else:
            idx_right = 0

        # Determine where the edge is located
        if xrem <= 0.5:
            # Player is in the right frame
            edge = int(np.around(w / 2.0 - xrem * img_w))
        else:
            # Player is in the left frame
            edge = int(np.around(w / 2.0 + (1.0 - xrem) * img_w))

        # Position the textures
        overlap = 0.0
        bg_left0 = edge - (1 - overlap) * img_w
        bg_left1 = edge - overlap * img_w

        # Draw the textures
        scene_drawing.image(self.bg[idx_left], bg_left0, self.bottomLineHeight, img_w, img_h)
        scene_drawing.image(self.bg[idx_right], bg_left1, self.bottomLineHeight, img_w, img_h)


# Create OptionButtons class
class OptionButtons:
    def __init__(self, anchor_point=(0.5, 0.5), rm_pos=(0, 1.1*height), **kwargs):
        # Get the keyword arguments
        text = kwargs['text']
        font = kwargs['font']
        self.pos = kwargs['position']
        self.rm_pos = rm_pos
        self.sz = kwargs['size']
        ap = anchor_point
        
        # Set the boundaries
        self.left = self.pos[0] - self.sz[0] * ap[0]
        self.right = self.pos[0] + self.sz[0] * (1-ap[0])
        self.bottom = self.pos[1] - self.sz[1] * ap[1]
        self.top = self.pos[1] + self.sz[1] * (1-ap[1])
        
        # Set up the background image
        self.img = SpriteNode('a/button.png')
        self.img.position = (self.rm_pos[0], self.rm_pos[1])
        self.img.size = self.sz
        self.img.alpha = 0.5
        self.img.anchor_point = (0, 0)
        
        # Set up the text
        self.butt = LabelNode(text=text, font=font, color=red)
        self.butt.position = (self.rm_pos[0] + self.sz[0]/2, self.rm_pos[1] + self.sz[1]/2)
        self.butt.anchor_point = (0.5, 0.5)
        
    def text(self, str):
        self.butt.text = str
        
    def detect_touch(self, loc):
        tCnd = [loc[0] > self.left,
                loc[0] < self.right,
                loc[1] > self.bottom,
                loc[1] < self.top]
        return all(tCnd)
        
    def add(self, t=0.5):
        move_action = Action.move_to(self.left, self.bottom, t, TIMING_SINODIAL)
        self.img.run_action(move_action)
        move_action = Action.move_to(self.left + self.sz[0]/2, self.bottom + self.sz[1]/2, t, TIMING_SINODIAL)
        self.butt.run_action(move_action)
        
    def rm(self, t=0.5):
        move_action = Action.move_to(self.rm_pos[0], self.rm_pos[1], t, TIMING_SINODIAL)
        self.img.run_action(move_action)
        move_action = Action.move_to(self.rm_pos[0] + self.sz[0]/2, self.rm_pos[1] + self.sz[1]/2, t, TIMING_SINODIAL)
        self.butt.run_action(move_action)

if engine == 'ista':
    
    class Game (Scene):
        def setup(self):

            # Initialize the motion module
            motion.start_updates()

            # Add the game state classes to the scene
            self.touchCycle = False
            
            # Initialize the counter for the splash screen
            self.kSplash = 0
            self.splash = SpriteNode('a/splash.png')
            self.splash.size = (width, height)
            self.splash.anchor_point = (0.0, 0.0)
            self.splash.position = (0, 0)
            self.add_child(self.splash)
            self.splash.alpha = 0
            fade_action = Action.fade_to(1, 2)
            self.splash.run_action(fade_action)
            
            # Generate the sky blue background and images
            self.background_color = skyBlue
            self.bg = MyBackground() 
            
            # Initialize the buttons or sticks
            self.moveStick,self.moveAura = initStick(self,0.1,0.2*width,(1,0),(width,height/20))
            self.tiltStick,self.tiltAura = initStick(self,0.1,0.2*width,(0,0),(0,height/20))
            self.add_child(self.moveAura)
            self.add_child(self.tiltAura)
            
            # Initialize the score line
            score_font = ('Menlo', 11)
            self.time_label = LabelNode('Time', score_font, parent=self,color=white)
            self.time_label.anchor_point = (0.0, 1.0)
            self.time_label.position = (width*0.01, height - 2)
            self.time_label.z_position = 1
            
            self.dist_label = LabelNode('Distance', score_font, parent=self, color=white)
            self.dist_label.anchor_point = (0.0, 1.0)
            self.dist_label.position = (width*0.21, height - 2)
            self.dist_label.z_position = 1
            
            self.high_label = LabelNode('Height', score_font, parent=self,color=white)
            self.high_label.anchor_point = (0.0, 1.0)
            self.high_label.position = (width*0.42, height - 2)
            self.high_label.z_position = 1
            
            self.boing_label = LabelNode('Boing!', score_font, parent=self,color=white)
            self.boing_label.anchor_point = (0.0, 1.0)
            self.boing_label.position = (width*0.62, height - 2)
            self.boing_label.z_position = 1
            
            self.score_label = LabelNode('Score', score_font, parent=self,color=white)
            self.score_label.anchor_point = (0.0, 1.0)
            self.score_label.position = (width*0.82, height - 2)
            self.score_label.z_position = 1
            
            # Get ranges for drawing the player and ball
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u, width)
            
            # Initialize the ball image
            self.ball = SpriteNode('a/ball.png')
            dbPix = 2*p.rb*m2p
            self.ball.size = (dbPix, dbPix)
            self.ball.anchor_point = (0.5, 0.5)
            self.ball.position = (gs.xb*m2p+po, (gs.yb+p.rb)*m2p)
            
            # Initialize the player's head
            self.head = SpriteNode('a/myFace.png')
            spPix = 0.7*m2p
            self.head.size = (spPix, spPix)
            self.head.anchor_point = (0.5, 0.0)
            self.head.position = (gs.xp[0]*m2p+po, (gs.yp[0]+p.d)*m2p)
            
            self.head1 = SpriteNode('a/LadyFace.png')
            self.head1.size = (spPix, spPix)
            self.head1.anchor_point = (0.5, 0.0)
            self.head.position = (gs.xp[1]*m2p+po, (gs.yp[1]+p.d)*m2p)

            # Initialize Stools
            self.stool = SpriteNode('a/stool.png')
            self.stool.size = (0.7*m2p, m2p)
            self.stool.position = (gs.xp[0]*m2p+po, (gs.yp[0]+p.d)*m2p)
            self.stool.anchor_point = (0.5, 1.0)
            
            self.stool1 = SpriteNode('a/stool.png', color=gray)
            self.stool1.size = (0.7*m2p, m2p)
            self.stool1.position = (gs.xp[1]*m2p+po, (gs.yp[1]+p.d)*m2p)
            self.stool1.anchor_point = (0.5, 1.0)

            # Initialize Buttons
            self.actionButt = OptionButtons(text='Begin', font=(p.MacsFavoriteFont, 20), position=(0.99*width, 0.92*height), size=(0.18 * width, 0.04 * width), anchor_point=(1,1))
            
            self.option_butt = OptionButtons(text='Options', font=(p.MacsFavoriteFont, 20), position=(0.01*width,0.92*height), size=(0.18 * width, 0.04 * width), anchor_point=(0,1))
            
            self.add_child(self.actionButt.butt)
            self.add_child(self.actionButt.img)
            self.add_child(self.option_butt.butt)
            self.add_child(self.option_butt.img)
            self.actionButt.text('Begin')
            
            self.singleButt = OptionButtons(text='Single Drubble', font=(p.MacsFavoriteFont,36), size=(0.8*width,0.2*height),  position=(0.5*width, 0.75*height),  rm_pos=(-1.5*width, 0.75*height))
            self.doubleButt = OptionButtons(text='Double Drubble', font=(p.MacsFavoriteFont,36), size=(0.8*width,0.2*height), position=(0.5*width, 0.5*height), rm_pos=(1.5*width, 0.5*height))
            
            self.add_child(self.singleButt.butt)
            self.add_child(self.singleButt.img)
            self.add_child(self.doubleButt.butt)
            self.add_child(self.doubleButt.img)
            
            toggleVisibleSprites(self, False)

            # Start the drums
            self.current_drum = 0
            drum_player[self.current_drum].play()
            
        def update(self):
            # Update if there was a touch
            if self.touchCycle:
                cycleModes(gs, stats, engine)
                if gs.game_mode == 2:
                    self.singleButt.add()
                    self.doubleButt.add()
                    
                if gs.game_mode == 3:
                    self.singleButt.rm()
                    self.doubleButt.rm()
                    toggleVisibleSprites(self,True)
                    
                    
                if gs.game_mode == 4:
                    self.actionButt.text('Set Angle')
                    
                if gs.game_mode == 5:
                    self.actionButt.text('Set Speed')
                    
                if gs.game_mode == 6:
                    self.actionButt.text('Restart')
                    
                self.touchCycle = False
                
            # Get control inputs
            if gs.ctrlMode == 'motion':
                gs.setControl(g=motion.get_gravity(), a=motion.get_user_acceleration())    
            elif gs.ctrlMode == 'vStick' and gs.game_mode>1:
                gs.setControl(moveStick=self.moveStick.ctrl,
                              tiltStick=self.tiltStick.ctrl)
                
                # Move auras
                xy = self.moveStick.ctrl
                c = self.moveStick.cntr
                s = self.moveStick.size[0]/3
                self.moveAura.position = (c[0]+xy[0]*s,c[1]+xy[1]*s)
                xy = self.tiltStick.ctrl
                c = self.tiltStick.cntr
                self.tiltAura.position = (c[0]+xy[0]*s,c[1]+xy[1]*s)
                
            ## ANGLE AND SPEED SETTINGS
            if gs.game_mode>2 and gs.game_mode<6:
                gs.setAngleSpeed()
            
            # Run one simulation step
            gs.simStep(p, gs, stats)
            if gs.game_mode == 6:
                stats.update(gs)
            xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u, width)
            if gs.StoolBounce:
                sound.play_effect('digital:PhaseJump3')
            if gs.FloorBounce and not gs.Stuck:
                sound.play_effect('game:Error')
                
            # Play the drum beat
            if drum_player[self.current_drum].current_time > 0.985 * drum_player[self.current_drum].duration:
                next_drum = 1
                if next_drum == self.current_drum:
                    drum_player[self.current_drum].current_time = 0.0
                else:
                    self.current_drum = next_drum
                    drum_player[self.current_drum].play()
            #drums.play_ista()
            
            # Update score line
            self.time_label.text = 'Time - %10.1f' % gs.t
            self.dist_label.text = 'Distance - %6.1f' % stats.stoolDist
            self.high_label.text = 'Height - %8.2f' % stats.maxHeight
            self.boing_label.text = 'Boing! - %6.0f' % stats.stoolCount
            self.score_label.text = 'Score - %9.0f' % stats.score
            
            # update the ball sprites
            dbPix = 2*p.rb*m2p
            self.ball.size = (dbPix, dbPix)
            x,y = xy2p(gs.xb, gs.yb, m2p, po, width, height)
            self.ball.position = (x, y)
            
            # Update the head and stool sprites
            spPix = 0.7*m2p
            self.head.size = (spPix, spPix)
            x,y = xy2p(gs.xp[0], gs.yp[0]+p.d, m2p, po, width, height)
            self.head.position = (x, y)
            
            self.stool.size = (0.7*m2p, m2p)
            x,y = xy2p(gs.xp[0] - gs.lp[0] * np.sin(gs.tp[0]), gs.yp[0]+p.d + gs.lp[0] * np.cos(gs.tp[0]), m2p, po, width, height)
            self.stool.position = (x, y)
            self.stool.rotation = gs.tp[0]
            
            if p.nPlayer > 1:
                self.head1.size = (spPix,spPix)
                x,y = xy2p(gs.xp[1], gs.yp[1]+p.d, m2p, po, width, height)
                self.head1.position = (x,y)
                
                self.stool1.size = (0.7*m2p, m2p)
                x,y = xy2p(gs.xp[1] - gs.lp[1] * np.sin(gs.tp[1]), gs.yp[1]+p.d + gs.lp[1] * np.cos(gs.tp[1]), m2p, po, width, height)
                self.stool1.position = (x, y)
                self.stool1.rotation = gs.tp[1]
            
        def draw(self):
            # Show the splash screen
            if gs.game_mode == 1:
                #makeSplashScreen(self)
                if not gs.showedSplash:
                    self.kSplash += 2
            else:
                xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u, width)
            
                # Generate the background
                if gs.game_mode>2:
                    # Update the background
                    xMean = (gs.xb+gs.xp[0])/2.0
                    self.bg.update(xMean,gs.yb,width,height,m2p)
            
                if gs.game_mode>2:
                    # Generate the bottom line
                    stroke(black)
                    stroke_weight(height/20)
                    line(0,height/40,width,height/40)
            
                    # Generate the markers
                    makeMarkers(xrng,m2p,po)
            
                    # Generate the trajectory
                    linePlot(gs.xTraj,gs.yTraj,m2p,po,width,height,white,1)
                    
                    for k in range(p.nPlayer):
                        # Generate a player image
                        xv,yv,sx,sy = stickDude(gs,k)
                        linePlot(xv,yv,m2p,po,width,height,p.playerColor[k],0.15*m2p)
            
                        # Generate a stool image
                        #linePlot(sx,sy,m2p,po,width,height,p.stoolColor[k],0.1*m2p)
                        
        def touch_began(self, touch):
            # Reset if necessary
            if gs.game_mode == 1 and self.kSplash >= 255:
                self.touchCycle = True
                move_action = Action.move_to(0, -height, 0.5, TIMING_SINODIAL)
                self.splash.run_action(move_action)
            
            if gs.game_mode == 2:
                b1 = self.singleButt.detect_touch(touch.location)
                b2 = self.doubleButt.detect_touch(touch.location)
                if b1 or b2:
                    self.touchCycle = True
                    p.nPlayer = b1 + 2*b2
                    self.singleButt.rm()
                    self.doubleButt.rm()
            
            if gs.game_mode > 2 and self.actionButt.detect_touch(touch.location):
                self.touchCycle = True
            
            if gs.game_mode > 2 and self.option_butt.detect_touch(touch.location):
                gs.game_mode = 1
                toggleVisibleSprites(self,False)
                self.touchCycle = True
                
            # Detect control inputs
            xy = touchStick(touch.location,self.moveStick)
            if xy[0] != 0:
            	self.moveStick.ctrl = xy
            	self.moveStick.id = touch.touch_id
            	self.moveAura.alpha = 1
            	
            xy = touchStick(touch.location,self.tiltStick)
            if xy[0] != 0:
            	self.tiltStick.ctrl = xy
            	self.tiltStick.id = touch.touch_id	
            	self.tiltAura.alpha = 1
        
        def touch_moved(self,touch):
            # Detect control inputs
            xy = touchStick(touch.location,self.moveStick)
            if touch.touch_id == self.moveStick.id and xy[0] != 0:
                self.moveStick.ctrl = xy
            
            xy = touchStick(touch.location,self.tiltStick)
            if touch.touch_id == self.tiltStick.id and xy[0] != 0:
                self.tiltStick.ctrl = xy
                
        
        def touch_ended(self,touch):
            if touch.touch_id == self.moveStick.id:
                self.moveStick.ctrl = (0,0)
                self.moveAura.alpha = 0.5
        
            if touch.touch_id == self.tiltStick.id:
                self.tiltStick.ctrl = (0,0)
                self.tiltAura.alpha = 0.5
                
        def stop(self):
            motion.stop_updates()
                
    if __name__ == '__main__':
        run(Game(), LANDSCAPE, frame_interval=60.0/fs,show_fps=False)
        
        
        
        
