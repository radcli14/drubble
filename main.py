#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:18:17 2019

@author: radcli14
"""
# Import the Kivy modules
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.core.audio import SoundLoader

# Execute drubbleFunc to get the supporting functions and classes
# engine = 'kivy'
from drubbleFunc import *

# Set the keyboard input and mouse defaults
keyPush = np.zeros(8)

# Initialize stats
stats = GameScore()

# Initialize drums
#drums = DrumBeat()
#def drums_callback(dt):
#    drums.play_kivy()

# Set the sky blue background color
Window.clearcolor = (skyBlue[0], skyBlue[1], skyBlue[2], 1)
#Window.size = (width, height)
width, height = Window.size

# Set the icon (neither are working...)
#Config.window_icon = 'a/icon.png'
Window.icon = 'a/icon.png'

# Initialize the players
p1 = playerLines(0)
p2 = playerLines(1)

# This is the text used in the upper right button
actionMSG = ['', '', '', '    Begin', 'Set Angle', 'Set Speed', '  Restart']


class MyBackground(Widget):
    # Size of the black bar on the bottom of the screen
    bottomLineHeight = NumericProperty(height/20.0)

    # Set size of the background, before updates
    sz_orig = w_orig, h_orig = (2400.0, 400.0)
    img_w = NumericProperty(w_orig)
    img_h = NumericProperty(h_orig)

    # Number of background images
    num_bg = 3

    # Create the properties for the left edges of the bg images
    bg_left0 = NumericProperty(0.0)
    bg_left1 = NumericProperty(0.0)

    # Create the textures
    textures = []
    for n in range(num_bg):
        textures.append(Image(source='a/bg'+str(n)+'.png').texture)
    bg_text0 = ObjectProperty(None)
    bg_text1 = ObjectProperty(None)
    bg_alpha = NumericProperty(0.0)

    # Randomize the start location in the backgroun
    xpos = np.random.rand() * 100.0 * num_bg

    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        self.width = width
        self.height = height

    def update(self, x, y, w, h, m2p):
        # Since we're updating, you probably want it visible
        self.bg_alpha = 1.0

        # xmod is normalized position of the player between 0 and num_bg
        xmod = np.mod(x+self.xpos, 100.0 * self.num_bg)/100.0
        xrem = np.mod(xmod, 1)
        xflr = int(np.floor(xmod))

        # xsel selects which background textures are used TBR
        if xrem <= 0.5:
            xsel = xflr-1
        else:
            xsel = xflr

        # scf is the scale factor to apply to the background
        scf = (m2p/70.0)**0.5
        self.img_w = int(np.around(self.w_orig*scf))
        self.img_h = int(np.around(self.h_orig*scf))

        # Decide which textures are used
        self.bg_text0 = self.textures[xsel]
        if xsel < (self.num_bg-1):
            self.bg_text1 = self.textures[xsel+1]
        else:
            self.bg_text1 = self.textures[0]

        # Determine where the edge is located
        if xrem <= 0.5:
            # Player is in the right frame
            edge = int(np.around(w/2.0-xrem*self.img_w))
        else:
            # Player is in the left frame
            edge = int(np.around(w/2.0+(1.0-xrem)*self.img_w))

        # Position the textures
        overlap = 0.0
        self.bg_left0 = edge-(1-overlap)*self.img_w
        self.bg_left1 = edge-overlap*self.img_w


def makeMarkers(self, p):
    # xrng_r is the first and last markers on the screen, xrng_n is the
    # number of markers
    xrng_r = np.around(p.xrng, -1)
    xrng_n = int((xrng_r[1] - xrng_r[0]) / 10.0) + 1

    for k in range(self.nMarks):
        self.yardMark[k].text = ''

    for k in range(xrng_n):
        # Current yardage
        xr = int(xrng_r[0] + 10 * k)

        # Lines
        [start_x, start_y] = xy2p(xr, 0, p.m2p, p.po, self.width, self.height)
        [end_x, end_y] = xy2p(xr, -1, p.m2p, p.po, self.width, self.height)
        Color(white[0], white[1], white[2], 1)
        Line(points=(start_x, start_y, end_x, end_y), width=1.5)

        # Numbers
        strxr = str(xr)  # String form of xr
        fsize = min(24, int(p.m2p))  # Font size
        xypos = (int(start_x + 5), self.height / 20 - fsize)  # Position of text
        lsize = (len(strxr) * fsize / 2.0, fsize)  # Label size
        if k >= self.nMarks:
            self.yardMark.append(Label(font_size=fsize,
                                       size=lsize, pos=xypos,
                                       text=strxr, color=(1, 1, 1, 1),
                                       halign='left', valign='top'))
            self.add_widget(self.yardMark[k])
            self.nMarks += 1
        else:
            self.yardMark[k].font_size = fsize
            self.yardMark[k].size = lsize
            self.yardMark[k].pos = xypos
            self.yardMark[k].text = strxr


class SplashScreen(Widget):
    k = 0.0
    k_increment = 5.0
    splash_fade = NumericProperty(1)
    text_alpha = NumericProperty(0)
    lbl_height = 0.2*height

    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        self.width = width
        self.height = height

    def update(self,showSplash):  
        if not gs.showedSplash:
            self.k += self.k_increment
            self.splash_fade -= self.k_increment/255.0
        if self.k >= 255:
            gs.showedSplash = True
            self.text_alpha = 1
            
    def clear(self):
        with self.canvas:
            Color(skyBlue[0]*self.k/255.0, skyBlue[1]*self.k/255.0, skyBlue[2]*self.k/255.0, 1)
            Rectangle(pos=(0, 0), size=(width, height))


class MyFace(Widget):
    img_left = NumericProperty(0.0)
    img_bottom = NumericProperty(0.0)
    sz = NumericProperty(0)
    image_source = StringProperty(None)
    face_alpha = NumericProperty(0.0)

    def __init__(self, image_source='a/myFace.png', **kwargs):
        super(MyFace, self).__init__(**kwargs)
        self.image_source = image_source
            
    def update(self, x, y, m2p, po, w, h):
        xp, yp = xy2p(x, y, m2p, po, w, h)
        self.sz = int(m2p*0.7)
        self.img_left = int(xp-self.sz*0.5)
        self.img_bottom = int(yp)
        self.face_alpha = 1.0

    def clear(self):
        self.face_alpha = 0.0


class Ball(Widget):
    img_left = NumericProperty(0.0)
    img_bottom = NumericProperty(0.0)
    sz = NumericProperty(0)
    image_source = StringProperty(None)
    ball_alpha = NumericProperty(0.0)
    trajectory = ListProperty([])

    def __init__(self, image_source='a/ball.png', **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.image_source = image_source

    def update(self, xb, yb, m2p, po, w, h):
        x, y = xy2p(xb, yb, m2p, po, w, h)
        self.sz = int(2.0 * p1.m2p * p.rb)
        self.img_left = int(x - p1.m2p * p.rb)
        self.img_bottom = int(y - p1.m2p * p.rb)
        self.ball_alpha = 1.0
        x, y = xy2p(gs.xTraj, gs.yTraj, m2p, po, w, h)
        self.trajectory = intersperse(x, y)

    def clear(self):
        self.ball_alpha = 0.0


# Returns the center_x, center_y, and diameter of the stick
def get_stick_pos(ch):
    return ch.pos[0]+ch.size[0]/2.0, ch.pos[1]+ch.size[1]/2.0, ch.size[0] 


class stick(Widget):
    #ch_x = NumericProperty(0.0)
    #ch_y = NumericProperty(0.0)
    #ch_s = NumericProperty(0.0)
    #ctrl_x = NumericProperty(0.0)
    #ctrl_y = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(stick, self).__init__(**kwargs)

        #size = kwargs['size']
        #pos = kwargs['pos']
        #print(size)
        #print(pos)
        #ch_x = NumericProperty(pos[0])
        #ch_y = NumericProperty(pos[1])
        #ch_s = NumericProperty(size[0])

        #self.ts_x = (pos[0]-size[0]/2.0, pos[0]+size[0]/2.0)
        #self.ts_y = (pos[1]-size[1]/2.0, pos[1]+size[1]/2.0)
        #self.center = pos

        with self.canvas:
            self.ch = Image(source='a/crossHair.png', **kwargs)
            ch_x, ch_y, ch_s = get_stick_pos(self.ch)
            Color(1, 1, 1, 0.5)
            self.el = Ellipse(pos=(ch_x-ch_s/4.0, ch_y-ch_s/4.0),
                              size=(ch_s/2.0, ch_s/2.0))

        self.ts_x = (ch_x-ch_s/2.0, ch_x+ch_s/2.0)
        self.ts_y = (ch_y-ch_s/2.0, ch_y+ch_s/2.0)
        self.cntr = (ch_x, ch_y)
        self.ctrl = (0, 0)

    def update_el(self, x, y):
        #self.ctrl_x = x
        #self.ctrl_y = y

        ch_x, ch_y, ch_s = get_stick_pos(self.ch)
        self.el.pos = (ch_x-ch_s/4.0+ch_s*x/4.0, ch_y-ch_s/4.0+ch_s*y/4.0)
        self.ctrl = (x, y)


# Create OptionButtons class
class OptionButtons(Label):
    def resize(self, size, pos):
        self.butt.size = size
        self.butt.pos = pos

    def detect_touch(self, loc):
        tCnd = [loc[0] > self.pos[0],
                loc[0] < self.pos[0] + self.size[0],
                loc[1] > self.pos[1],
                loc[1] < self.pos[1] + self.size[1]]
        return all(tCnd)


class ScoreLabel(Widget):
    label_text = StringProperty('')
    label_left = NumericProperty(0.0)
    label_font = StringProperty('a/VeraMono.ttf')
    label_size = NumericProperty(int(0.015*width))

    def __init__(self, **kwargs):
        super(ScoreLabel, self).__init__()
        self.label_text = kwargs['text']
        self.label_left = kwargs['left']
        self.width = width
        self.height = height

    def update(self, label_string):
        self.label_text = label_string

    def resize(self, w, h):
        self.label_left = self.label_left * w / self.width
        self.label_size = int(0.015*w)
        self.width = w
        self.height = h


class DrubbleGame(Widget):
    def __init__(self, **kwargs):
        super(DrubbleGame, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.bind(size=self.resize_canvas)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        #Window.bind(on_joy_hat=self.on_joy_hat)
        #Window.bind(on_joy_ball=self.on_joy_ball)
        Window.bind(on_joy_axis=self.on_joy_axis)
        #Window.bind(on_joy_button_up=self.on_joy_button_up)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        self.nMarks = 0
        self.yardMark = []
        self.weHaveWidgets = False
        self.weHaveButtons = False
        with self.canvas:
            # Splash screen, init right away
            self.splash = SplashScreen()
            self.add_widget(self.splash)

            # Initialize the background
            self.bg = MyBackground()

            # Initialize the ball
            self.ball = Ball()

            # Initialize the player faces
            self.myFace = MyFace(image_source='a/myFace.png')
            self.LadyFace = MyFace(image_source='a/LadyFace.png')

    def add_game_widgets(self): 
        # Add game widgets
        with self.canvas:

            self.add_widget(self.bg)
            self.add_widget(self.myFace)
            self.add_widget(self.LadyFace)
            self.add_widget(self.ball)

            # Initialize the sticks
            sz = 0.2*width
            self.moveStick = stick(size=(sz, sz), pos=(0.8*width, 0.05*height))
            self.tiltStick = stick(size=(sz, sz), pos=(0, 0.05*height))
            self.add_widget(self.moveStick)
            self.add_widget(self.tiltStick)

            # Initialize the score line
            self.time_label = ScoreLabel(text='Time', left=0.0*self.width)
            self.dist_label = ScoreLabel(text='Distance', left=0.2*self.width)
            self.high_label = ScoreLabel(text='Height', left=0.4*self.width)
            self.boing_label = ScoreLabel(text='Boing!', left=0.6*self.width)
            self.score_label = ScoreLabel(text='Score', left=0.81*self.width)
            self.add_widget(self.time_label)
            self.add_widget(self.dist_label)
            self.add_widget(self.high_label)
            self.add_widget(self.boing_label)
            self.add_widget(self.score_label)

            self.optionButt = OptionButtons(text='Options',
                                            size=(0.2 * self.width, 24),
                                            pos=(0.0 * self.width, self.height-50),
                                            font_size=24)
            self.add_widget(self.optionButt)

            self.actionButt = OptionButtons(text=actionMSG[3],
                                            size=(0.2 * self.width, 24),
                                            pos=(0.8 * self.width, self.height-50),
                                            font_size=24)
            self.add_widget(self.actionButt)

            self.weHaveWidgets = True

    def remove_game_widgets(self):
        self.remove_widget(self.bg)
        self.remove_widget(self.moveStick)
        self.remove_widget(self.tiltStick)
        self.remove_widget(self.myFace)
        self.remove_widget(self.LadyFace)
        self.myFace.clear()
        self.LadyFace.clear()
        self.remove_widget(self.time_label)
        self.remove_widget(self.dist_label)
        self.remove_widget(self.high_label)
        self.remove_widget(self.boing_label)
        self.remove_widget(self.score_label)

    def add_option_buttons(self):
        w, h = (self.width, self.height)
        # Add option screen buttons
        with self.canvas:
            self.singleDrubbleButt = OptionButtons(text='Single Drubble',
                                                   size=(0.8*w, 0.2*h),
                                                   pos=(0.1*w, 0.7*h),
                                                   font_size=0.1*h)
            self.doubleDrubbleButt = OptionButtons(text='Double Drubble',
                                                   size=(0.8*w, 0.2*h),
                                                   pos=(0.1*w, 0.4*h),
                                                   font_size=0.1*h)
            self.tripleDrubbleButt = OptionButtons(text='Triple Drubble',
                                                   size=(0.8*w, 0.2*h),
                                                   pos=(0.1*w, 0.1*h),
                                                   font_size=0.1*h)

    # Controls
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(keyPush, keycode, 1))
        if gs.gameMode == 1 and gs.showedSplash:
            cycleModes(gs, stats)
        elif keycode[1] == 'spacebar':
            cycleModes(gs, stats)
            self.actionButt.text = actionMSG[gs.gameMode]
        elif keycode[1] == 'escape':
            gs.gameMode = 1
            self.remove_game_widgets()
            self.canvas.clear()
            with self.canvas:
                Color(skyBlue[0], skyBlue[1], skyBlue[2], 1)
                Rectangle(size=(self.width, self.height))
            self.add_option_buttons()
            cycleModes(gs, stats)
        return True
    
    def _on_keyboard_up(self, keyboard, keycode):
        keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(keyPush, keycode, 0))
        return True
    
    def on_touch_down(self, touch):
        loc = (touch.x, touch.y)
        if gs.gameMode == 1 and gs.showedSplash:
            cycleModes(gs, stats)
        elif gs.gameMode == 2 and self.singleDrubbleButt.detect_touch(loc):
            p.nPlayer = 1
            cycleModes(gs, stats)
        elif gs.gameMode == 2 and self.doubleDrubbleButt.detect_touch(loc):
            p.nPlayer = 2
            cycleModes(gs, stats)
        elif gs.gameMode > 2:
            # Cycle through modes if touch above the halfway point
            if self.actionButt.detect_touch(loc):
                cycleModes(gs, stats)
                self.actionButt.text = actionMSG[gs.gameMode]
            if self.optionButt.detect_touch(loc):
                gs.gameMode = 1
                self.remove_game_widgets()
                self.canvas.clear()
                with self.canvas:
                    Color(skyBlue[0], skyBlue[1], skyBlue[2], 1)
                    Rectangle(size=(self.width, self.height))
                self.add_option_buttons()
                cycleModes(gs, stats)

            # Detect control inputs
            xy = touchStick(loc, self.moveStick)
            if xy[0] != 0:
                self.moveStick.id = touch.id
                self.moveStick.update_el(xy[0], xy[1])
                gs.ctrl[0:2] = xy
            
            xy = touchStick(loc, self.tiltStick)
            if xy[0] != 0:
                self.tiltStick.id = touch.id    
                self.tiltStick.update_el(xy[0], xy[1])
                gs.ctrl[2:4] = [xy[1], -xy[0]]

    def on_touch_move(self, touch):
        if gs.gameMode > 2 and self.weHaveWidgets:
            # Detect control inputs
            xy = touchStick((touch.x,touch.y), self.moveStick)
            if touch.id == self.moveStick.id and xy[0] != 0:
                self.moveStick.update_el(xy[0], xy[1])
                gs.ctrl[0:2] = xy

            xy = touchStick((touch.x,touch.y),self.tiltStick)
            if touch.id == self.tiltStick.id and xy[0] != 0:
                self.tiltStick.update_el(xy[0], xy[1])
                gs.ctrl[2:4] = [xy[1], -xy[0]]

    def on_touch_up(self, touch):
        if gs.gameMode > 2 and self.weHaveWidgets:
            if touch.id == self.moveStick.id:
                self.moveStick.update_el(0, 0)
                gs.ctrl[0:2] = [0, 0]
                
            if touch.id == self.tiltStick.id:
                self.tiltStick.update_el(0, 0)
                gs.ctrl[2:4] = [0, 0]

    def on_joy_axis(self, win, stickid, axisid, value):
        print('me')
        print(win)

    def on_joy_button_down(self, win, stickid, buttonid):
        print('butt')

    # Drawing commands
    def update_canvas(self,*args):
        if self.weHaveWidgets:
            self.canvas.clear()
            with self.canvas:
                # Draw Bottom Line
                makeMarkers(self,p1)
                
                # Draw Player One
                Color(darkGreen[0], darkGreen[1], darkGreen[2], 1)
                Line(points=p1.player, width=0.075*p1.m2p)
                Color(white[0], white[1], white[2], 1)
                Line(points=p1.stool, width=0.05*p1.m2p)
                
                if p.nPlayer>1:
                    # Draw Player Two
                    Color(red[0], red[1], red[2], 1)
                    Line(points=p2.player,width=0.075*p2.m2p)
                    Color(black[0], black[1], black[2], 1)
                    Line(points=p2.stool, width=0.05*p2.m2p)
            
                # Draw the ball
                self.ball.update(gs.xb, gs.yb, p1.m2p, p1.po, self.width, self.height)

    def resize_canvas(self, *args):
        if self.weHaveWidgets:
            self.time_label.resize(self.width, self.height)
            self.dist_label.resize(self.width, self.height)
            self.high_label.resize(self.width, self.height)
            self.boing_label.resize(self.width, self.height)
            self.score_label.resize(self.width, self.height)
            
            sz = self.moveStick.ch.size[0]
            self.moveStick.ch.pos = (self.width-sz, 0.05*self.height)
            self.tiltStick.ch.pos = (0, 0.05*self.height)

            self.bg.size = self.bg.width, self.bg.height = (self.width, self.height)
            self.bg.bottomLineHeight = self.bg.height/20.0

            self.actionButt.pos = (0.8 * self.width, self.height-50)
            self.optionButt.pos = (0.0 * self.width, self.height-50)

    # Time step the game
    def update(self, dt):
        # Either update the splash, or add the widgets
        if gs.gameMode == 1:
            self.splash.update(True)
        elif gs.gameMode == 2 and not self.weHaveButtons:
            self.add_option_buttons()
            self.splash.clear()
            self.remove_widget(self.splash)
            self.weHaveButtons = True
        elif gs.gameMode > 2 and not self.weHaveWidgets:
            self.add_game_widgets()            

        # ANGLE AND SPEED SETTINGS
        if 2 < gs.gameMode < 6:
            gs.setAngleSpeed()
        
        gs.simStep(p, stats)
        if gs.gameMode > 2:
            stats.update()

            # Update score line
            self.time_label.update('Time - %11.1f' % gs.t)
            self.dist_label.update('Distance - %7.1f' % stats.stoolDist)
            self.high_label.update('Height - %9.2f' % stats.maxHeight)
            self.boing_label.update('Boing! - %9.0f' % stats.stoolCount)
            self.score_label.update('Score - %10.0f' % stats.score)

        # Player drawing settings        
        xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
        p1.width = p2.width = self.width
        p1.height = p2.height = self.height
        
        p1.update(gs)
        p2.update(gs)
        
        if gs.gameMode > 2:
            xMean = (gs.xb+gs.xp[0])/2.0
            self.bg.update(xMean, gs.yb, self.width, self.height, m2p)
            self.moveStick.update_el(gs.ctrl[0], gs.ctrl[1])
            self.tiltStick.update_el(-gs.ctrl[3], gs.ctrl[2])
            self.myFace.update(gs.xp[0], gs.yp[0]+1.5*p.d, m2p, po,
                               self.width, self.height)
            if p.nPlayer > 1:
                self.LadyFace.update(gs.xp[1], gs.yp[1] + 1.5 * p.d, m2p, po,
                                     self.width, self.height)
            self.update_canvas()


class DrubbleApp(App):
    icon = 'a/icon.png'

    def build(self):
        game = DrubbleGame()
        Clock.schedule_interval(game.update, 1.0/fs)
        # Clock.schedule_interval(drums_callback, 1.0/7.0)
        return game


if __name__ == '__main__':
    DrubbleApp().run()