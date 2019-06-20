#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:18:17 2019

@author: radcli14
"""
# Import the Kivy modules
from math import fmod, floor
from random import randint
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
# from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from kivy.config import Config

# Import drubbleFunc to get the supporting functions and classes
from drubbleFunc import *

# Initialize Game State
gs = GameState(p.u0, engine)

# Initialize stats
stats = GameScore()

try:
    # Initialize drums
    num_loops = 2
    current_loop = 0
    loop = [SoundLoader.load('a/0'+str(k)+'-DC-Base.wav') for k in range(num_loops)]
    for k in range(num_loops):
        loop[k].volume = 0.4

    def sound_stopped(self):
        current_loop = randint(0, num_loops-1)
        loop[current_loop].play()

    for k in range(num_loops):
        try:
            loop[k].bind(on_stop=sound_stopped)
        except:
            print('failed binding to sound_stopped')
    loop[current_loop].play()

    stool_sound = SoundLoader.load('a/GoGo_crank_hit_Stool.wav')
    floor_sound = SoundLoader.load('a/GoGo_guitar_hit_slide_Floor.wav')
except:
    print('failed loading wav')

# Set the sky blue background color
Window.clearcolor = (skyBlue[0], skyBlue[1], skyBlue[2], 1)
print(platform)
if platform in ('linux', 'windows', 'win', 'macosx'):
    """Config.set('graphics', 'width', '1200')
    Config.set('graphics', 'height', '675')
    Config.set('graphics', 'window_state', 'minimized')
    Config.write() """
    width = 1200
    height = 675
    Window.size = (width, height)
else:
    width, height = Window.size

# On the retina screen, Window.size gets doubled, this is the correction factor
screen_scf = Window.size[0] / width

# Set the icon
Window.icon = 'a/icon.png'

# Initialize the players
p1 = playerLines(0, gs, width, height)
p2 = playerLines(1, gs, width, height)


class MyBackground(Widget):
    # Size of the black bar on the bottom of the screen
    bottomLineHeight = NumericProperty(height * screen_scf / 20.0)

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
    xpos = randint(0, 100*num_bg)

    def __init__(self, w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        self.width = w
        self.height = h

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.width = w
        self.height = h

    def update(self, x, y, w, h, m2p):
        # Since we're updating, you probably want it visible
        self.bg_alpha = 1.0

        # xmod is normalized position of the player between 0 and num_bg
        xmod = fmod(x+self.xpos, 100.0 * self.num_bg) / 100.0
        xrem = fmod(xmod, 1)
        xflr = int(floor(xmod))

        # xsel selects which background textures are used TBR
        if xrem <= 0.5:
            xsel = xflr - 1
        else:
            xsel = xflr

        # scf is the scale factor to apply to the background
        scf = (m2p / 70.0)**0.5
        self.img_w = int(round(self.w_orig * scf))
        self.img_h = int(round(self.h_orig * scf))

        # Decide which textures are used
        self.bg_text0 = self.textures[xsel]
        if xsel < (self.num_bg-1):
            self.bg_text1 = self.textures[xsel + 1]
        else:
            self.bg_text1 = self.textures[0]

        # Determine where the edge is located
        if xrem <= 0.5:
            # Player is in the right frame
            edge = int(round(w / 2.0 - xrem * self.img_w))
        else:
            # Player is in the left frame
            edge = int(round(w / 2.0 + (1.0 - xrem) * self.img_w))

        # Position the textures
        overlap = 0.0
        self.bg_left0 = edge - (1 - overlap) * self.img_w
        self.bg_left1 = edge - overlap * self.img_w


def make_markers(self, p):
    # xrng_r is the first and last markers on the screen, xrng_n is the
    # number of markers
    xrng_r = [round(p.xrng[i], -1) for i in range(2)]
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
        fsize = min(24 * screen_scf, int(p.m2p))  # Font size
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
    lbl_height = 0.2 * height * screen_scf

    def __init__(self, w=width, h=height, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        self.width = w
        self.height = h

    def resize(self, w=width, h=height):
        self.width = w
        self.height = h

    def update(self, showSplash):
        if not gs.showedSplash:
            self.k += self.k_increment
            self.splash_fade -= self.k_increment/255.0
        if self.k >= 255:
            gs.showedSplash = True
            self.text_alpha = 1
            
    def clear(self):
        with self.canvas:
            Color(skyBlue[0]*self.k/255.0, skyBlue[1]*self.k/255.0, skyBlue[2]*self.k/255.0, 1)
            Rectangle(pos=(0, 0), size=(self.width, self.height))


class MyFace(Widget):
    sz = NumericProperty(0)
    img_left = NumericProperty(0.0)
    img_bottom = NumericProperty(0.0)
    jersey_left = NumericProperty(0.0)
    jersey_right = NumericProperty(0.0)
    jersey_bottom = NumericProperty(0.0)
    jersey_source = StringProperty(None)
    stool_left = NumericProperty(0.0)
    stool_bottom = NumericProperty(0.0)
    stool_width = NumericProperty(0.0)
    stool_height = NumericProperty(0.0)
    stool_angle = NumericProperty(0.0)
    rotate_center = ListProperty([0, 0])
    image_source = StringProperty(None)
    face_alpha = NumericProperty(0.0)
    stool_color = ListProperty([0, 0, 0])
    line_list = ListProperty([0, 0])
    line_color = ListProperty([0, 0, 0])
    line_width = NumericProperty(1)
    shorts_source0 = StringProperty(None)
    shorts_source1 = StringProperty(None)
    shorts_angle0 = NumericProperty(0.0)
    shorts_angle1 = NumericProperty(0.0)

    def __init__(self, image_source='a/myFace.png', jersey_source='a/MyJersey.png', shorts_source='a/MyShorts.png',
                 stool_color=white, line_color=darkGreen, **kwargs):
        super(MyFace, self).__init__(**kwargs)
        self.image_source = image_source
        self.jersey_source = jersey_source
        self.shorts_source0 = shorts_source
        self.shorts_source1 = shorts_source.replace('.', '1.')
        self.stool_color = stool_color
        self.line_color = line_color

    def update(self, x, y, l, th, m2p, po, w, h, player):
        xp, yp = xy2p(x, y, m2p, po, w, h)
        self.sz = int(m2p*0.7)
        self.img_left = int(xp-self.sz*0.5)
        self.img_bottom = int(yp-0.05*m2p)
        self.jersey_left = int(xp-self.sz*0.3)
        self.jersey_bottom = int(yp-1.0*self.sz)
        self.jersey_right = int(xp+self.sz*0.3)
        self.stool_width = int(0.7*m2p)
        self.stool_height = int(m2p)
        self.stool_left = int(xp - 0.5 * self.stool_width)
        self.stool_bottom = int(yp + (l - 0.9 - 0.5 * p.d) * m2p)
        self.stool_angle = th * 180.0 / pi
        self.rotate_center = [self.img_left + self.sz*0.5, yp - 0.5 * p.d * m2p]
        self.line_width = 0.075*m2p
        self.line_list = player
        self.shorts_angle0 = -atan2(player[4]-player[6], player[5]-player[7]) * 180.0 / pi
        self.shorts_angle1 = -atan2(player[4]-player[2], player[5]-player[3]) * 180.0 / pi
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
    line_width = screen_scf
    if platform in ('linux', 'windows', 'macosx'):
        line_alpha = NumericProperty(0.5)
    else:
        line_alpha = NumericProperty(1.0)

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


def touchStick(loc, stick):
    tCnd = [loc[0] > stick.ts_x[0],
            loc[0] < stick.ts_x[1],
            loc[1] > stick.ts_y[0],
            loc[1] < stick.ts_y[1]]

    # Touched inside the stick
    if all(tCnd):
        x = min(max(p.tsens * (2.0 * (loc[0] - stick.ts_x[0]) / stick.ch_s - 1), -1), 1)
        y = min(max(p.tsens * (2.0 * (loc[1] - stick.ts_y[0]) / stick.ch_s - 1), -1), 1)
        return x, y
        # mag = sqrt(x ** 2 + y ** 2)
        # ang = round(4.0 * atan2(y, x) / pi) * pi / 4
        # return mag * cos(ang), mag * sin(ang)
    else:
        return 0, 0


class Stick(Widget):
    id_code = None
    # Crosshair position (ch_x, ch_y) and size (ch_s)
    ch_x = NumericProperty(0.0)
    ch_y = NumericProperty(0.0)
    ch_s = NumericProperty(0.0)

    # Touch stick locations in pixels, for detecting control input
    ts_x = [0.0, 0.0]
    ts_y = [0.0, 0.0]

    # Control values
    ctrl_x = NumericProperty(0.0)
    ctrl_y = NumericProperty(0.0)

    def __init__(self, norm_size=(0.2, 0.2), norm_pos=(0.0, 0.0),
                 w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(Stick, self).__init__(**kwargs)
        self.size = width * screen_scf, height * screen_scf
        self.norm_size = norm_size
        self.norm_pos = norm_pos
        self.ch_x = norm_pos[0] * w
        self.ch_y = norm_pos[1] * h
        self.ch_s = norm_size[0] * w

        self.ts_x = [norm_pos[0] * w, norm_pos[0] * w + norm_size[0] * w]
        self.ts_y = [norm_pos[1] * w, norm_pos[1] * w + norm_size[1] * w]
        self.ctrl = (0, 0)

    def update_el(self, x, y):
        self.ctrl_x = x
        self.ctrl_y = y
        self.ctrl = (x, y)

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.ch_x = self.norm_pos[0] * w
        self.ch_y = self.norm_pos[1] * h
        self.ch_s = self.norm_size[0] * w

        self.ts_x = [self.norm_pos[0] * w, self.norm_pos[0] * w + self.norm_size[0] * w]
        self.ts_y = [self.norm_pos[1] * w, self.norm_pos[1] * w + self.norm_size[1] * w]



# Create OptionButtons class
class OptionButtons(Widget):
    background_color = ListProperty([1, 1, 1, 0.75])
    background_normal = 'a/button.png'
    text = StringProperty('')
    label_font = StringProperty('a/airstrea.ttf')
    label_font_size = NumericProperty(0.0)
    label_color = ListProperty([0.0, 0.0, 0.0, 1.0])

    def __init__(self, norm_pos=(0.0, 0.0), norm_size=(0.5, 0.1), norm_font_size=0.05,
                 w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(OptionButtons, self).__init__()
        self.pos = (norm_pos[0] * w, norm_pos[1] * h)
        self.size = (norm_size[0] * w, norm_size[1] * h)
        self.text = kwargs['text']
        self.norm_pos = norm_pos
        self.norm_size = norm_size
        self.norm_font_size = norm_font_size
        self.label_font_size = norm_font_size * h
        self.label_color = [kwargs['color'][0], kwargs['color'][1], kwargs['color'][2], 1]

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.size = (self.norm_size[0] * w, self.norm_size[1] * h)
        self.pos = (self.norm_pos[0] * w, self.norm_pos[1] * h)
        self.label_font_size = self.norm_font_size * h

    def detect_touch(self, loc):
        touch_conditions = [loc[0] > self.pos[0],
                            loc[0] < self.pos[0] + self.size[0],
                            loc[1] > self.pos[1],
                            loc[1] < self.pos[1] + self.size[1]]
        return all(touch_conditions)


class ScoreLabel(Widget):
    label_text = StringProperty('')
    label_left = NumericProperty(0.0)
    label_font = StringProperty('a/VeraMono.ttf')
    label_size = NumericProperty(int(0.02 * width * screen_scf))

    def __init__(self, norm_left=0.0, w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(ScoreLabel, self).__init__()
        self.label_text = kwargs['text']
        self.norm_left = norm_left
        self.label_left = norm_left * w
        self.width = width * screen_scf
        self.height = height * screen_scf

    def update(self, label_string):
        self.label_text = label_string

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.label_left = self.norm_left * w
        self.label_size = int(0.02*w)
        self.width = w
        self.height = h


class DrubbleGame(Widget):
    def __init__(self, **kwargs):
        super(DrubbleGame, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.bind(size=self.resize_canvas)
        if platform in ('linux', 'windows', 'macosx'):
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
            self.splash = SplashScreen(w=width*screen_scf, h=height*screen_scf)
            self.add_widget(self.splash)

            # Initialize the background
            self.bg = MyBackground()

            # Initialize the ball
            self.ball = Ball()

            # Initialize the player faces
            self.myFace = MyFace(image_source='a/myFace.png', jersey_source='a/MyJersey.png',
                                 shorts_source='a/MyShorts.png', line_color=green, stool_color=white)
            self.LadyFace = MyFace(image_source='a/LadyFace.png', jersey_source='a/LadyJersey.png',
                                   shorts_source='a/LadyShorts.png', line_color=pink, stool_color=gray)

    def add_game_widgets(self): 
        # Add game widgets
        with self.canvas:

            self.add_widget(self.bg)
            self.add_widget(self.myFace)
            self.add_widget(self.LadyFace)
            self.add_widget(self.ball)

            self.bg.resize(w=self.width, h=self.height)

            # Initialize the sticks
            self.moveStick = Stick(norm_size=(0.2, 0.2), norm_pos=(0.8, 0.05))
            self.tiltStick = Stick(norm_size=(0.2, 0.2), norm_pos=(0.0, 0.05))
            self.add_widget(self.moveStick)
            self.add_widget(self.tiltStick)

            # Initialize the score line
            self.time_label = ScoreLabel(text='Time', norm_left=0.0)
            self.dist_label = ScoreLabel(text='Distance', norm_left=0.2)
            self.high_label = ScoreLabel(text='Height', norm_left=0.4)
            self.boing_label = ScoreLabel(text='Boing!', norm_left=0.6)
            self.score_label = ScoreLabel(text='Score', norm_left=0.8)
            self.add_widget(self.time_label)
            self.add_widget(self.dist_label)
            self.add_widget(self.high_label)
            self.add_widget(self.boing_label)
            self.add_widget(self.score_label)

            self.optionButt = OptionButtons(text='Options', norm_size=(0.18, 0.06),
                                            norm_pos=(0.01, 0.88), norm_font_size=0.05, color=red)
            self.add_widget(self.optionButt)

            self.actionButt = OptionButtons(text=p.actionMSG[3], norm_size=(0.18, 0.06),
                                            norm_pos=(0.81, 0.88),  norm_font_size=0.05, color=red)
            self.add_widget(self.actionButt)

            self.weHaveWidgets = True

            self.resize_canvas()

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
        # Add option screen buttons
        with self.canvas:
            self.singleDrubbleButt = OptionButtons(text='Single dRuBbLe', norm_size=(0.7, 0.2),
                                                   norm_pos=(0.15, 0.7),  norm_font_size=0.15,
                                                   w=self.width, h=self.height, color=red)
            self.doubleDrubbleButt = OptionButtons(text='Double dRuBbLe', norm_size=(0.7, 0.2),
                                                   norm_pos=(0.15, 0.4),  norm_font_size=0.15,
                                                   w=self.width, h=self.height, color=red)

    # Controls
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(self.keyPush, keycode, 1))
        if gs.gameMode == 1 and gs.showedSplash:
            cycleModes(gs, stats, engine)
        elif keycode[1] == 'spacebar':
            cycleModes(gs, stats, engine)
            self.actionButt.text = p.actionMSG[gs.gameMode]
        elif keycode[1] == 'escape':
            gs.gameMode = 1
            self.remove_game_widgets()
            self.canvas.clear()
            with self.canvas:
                Color(skyBlue[0], skyBlue[1], skyBlue[2], 1)
                Rectangle(size=(self.width, self.height))
            self.add_option_buttons()
            cycleModes(gs, stats, engine)
        return True
    
    def _on_keyboard_up(self, keyboard, keycode):
        self.keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(self.keyPush, keycode, 0))
        return True
    
    def on_touch_down(self, touch):
        loc = (touch.x, touch.y)
        if gs.gameMode == 1 and gs.showedSplash:
            cycleModes(gs, stats, engine)
        elif gs.gameMode == 2 and self.singleDrubbleButt.detect_touch(loc):
            p.nPlayer = 1
            cycleModes(gs, stats, engine)
        elif gs.gameMode == 2 and self.doubleDrubbleButt.detect_touch(loc):
            p.nPlayer = 2
            cycleModes(gs, stats, engine)
        elif gs.gameMode > 2:
            # Cycle through modes if touch above the halfway point
            if self.actionButt.detect_touch(loc):
                cycleModes(gs, stats, engine)
                self.actionButt.text = p.actionMSG[gs.gameMode]
                self.actionButt.background_color = (0, 0.5, 1, 0.5)
            if self.optionButt.detect_touch(loc):
                gs.gameMode = 1
                self.remove_game_widgets()
                self.canvas.clear()
                with self.canvas:
                    Color(skyBlue[0], skyBlue[1], skyBlue[2], 1)
                    Rectangle(size=(self.width, self.height))
                self.add_option_buttons()
                cycleModes(gs, stats, engine)
                self.optionButt.background_color = (0, 0.5, 1, 0.5)

            # Detect control inputs
            xy = touchStick(loc, self.moveStick)
            if xy[0] != 0:
                self.moveStick.id_code = touch.id
                self.moveStick.update_el(xy[0], xy[1])
                gs.ctrl[0:2] = xy
            
            xy = touchStick(loc, self.tiltStick)
            if xy[0] != 0:
                self.tiltStick.id_code = touch.id
                self.tiltStick.update_el(xy[0], xy[1])
                gs.ctrl[2:4] = [xy[1], -xy[0]]

    def on_touch_move(self, touch):
        if gs.gameMode > 2 and self.weHaveWidgets:
            # Detect control inputs
            xy = touchStick((touch.x,touch.y), self.moveStick)
            if touch.id == self.moveStick.id_code and xy[0] != 0:
                self.moveStick.update_el(xy[0], xy[1])
                gs.ctrl[0:2] = xy

            xy = touchStick((touch.x,touch.y),self.tiltStick)
            if touch.id == self.tiltStick.id_code and xy[0] != 0:
                self.tiltStick.update_el(xy[0], xy[1])
                gs.ctrl[2:4] = [xy[1], -xy[0]]

    def on_touch_up(self, touch):
        if gs.gameMode > 2 and self.weHaveWidgets:
            if touch.id == self.moveStick.id_code:
                self.moveStick.update_el(0, 0)
                gs.ctrl[0:2] = [0, 0]
                
            if touch.id == self.tiltStick.id_code:
                self.tiltStick.update_el(0, 0)
                gs.ctrl[2:4] = [0, 0]

            self.actionButt.background_color = (1, 1, 1, 0.75)
            self.optionButt.background_color = (1, 1, 1, 0.75)

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
                make_markers(self, p1)

                # Draw the ball
                self.ball.update(gs.xb, gs.yb, p1.m2p, p1.po, self.width, self.height)

    def resize_canvas(self, *args):
        if self.weHaveWidgets:
            self.time_label.resize(w=self.width, h=self.height)
            self.dist_label.resize(w=self.width, h=self.height)
            self.high_label.resize(w=self.width, h=self.height)
            self.boing_label.resize(w=self.width, h=self.height)
            self.score_label.resize(w=self.width, h=self.height)

            self.moveStick.resize(w=self.width, h=self.height)
            self.tiltStick.resize(w=self.width, h=self.height)

            self.bg.resize(self.width, self.height)
            self.bg.bottomLineHeight = self.height/20.0

            self.actionButt.resize(w=self.width, h=self.height)
            self.optionButt.resize(w=self.width, h=self.height)

    # Time step the game
    def update(self, dt):
        #if platform == 'android':
        #    Window.release_all_keyboards()

        if self.weHaveWidgets:
            self.actionButt.text = p.actionMSG[gs.gameMode]

        # Either update the splash, or add the widgets
        if gs.gameMode == 1:
            self.splash.resize(w=self.width, h=self.height)
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

        # Call the simStep method
        ddt = gs.simStep(p, gs, stats)

        # Adjust pitch of the loop that is playing (TBR not working)
        #print(ddt*fs)
        #for k in range(num_loops):
        #    loop[k].pitch = ddt * fs

        if gs.gameMode > 2:
            stats.update(gs)

            # Update score line
            self.time_label.update('Time %9.1f' % gs.t)
            self.dist_label.update('Distance %6.1f' % stats.stoolDist)
            self.high_label.update('Height %7.2f' % stats.maxHeight)
            self.boing_label.update('Boing! %7.0f' % stats.stoolCount)
            self.score_label.update('Score %8.0f' % stats.score)

        # Player drawing settings        
        xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u, self.width)
            
        p1.width = p2.width = self.width
        p1.height = p2.height = self.height
        
        p1.update(gs, self.width)
        p2.update(gs, self.width)
        
        if gs.gameMode > 2:
            xMean = (gs.xb+gs.xp[0])/2.0
            self.bg.update(xMean, gs.yb, self.width, self.height, m2p)
            self.moveStick.update_el(gs.ctrl[0], gs.ctrl[1])
            self.tiltStick.update_el(-gs.ctrl[3], gs.ctrl[2])
            self.myFace.update(gs.xp[0], gs.yp[0] + 1.5*p.d, gs.lp[0], gs.tp[0], m2p, po,
                               self.width, self.height, p1.player)
            if p.nPlayer > 1:
                self.LadyFace.update(gs.xp[1], gs.yp[1] + 1.5 * p.d, gs.lp[1], gs.tp[1], m2p, po,
                                     self.width, self.height, p2.player)
            self.update_canvas()

            # Make the bounce sounds
            if gs.StoolBounce:
                stool_sound.volume = min(0.1, norm([gs.dxb, gs.dyb]) / 50.0)
                stool_sound.play()
            elif gs.FloorBounce:
                floor_sound.volume = norm([gs.dxb, gs.dyb]) / 15.0
                floor_sound.play()


class DrubbleApp(App):
    icon = 'a/icon.png'

    def build(self):
        game = DrubbleGame()
        Clock.schedule_interval(game.update, 1.0/fs)
        return game


if __name__ == '__main__':
    DrubbleApp().run()