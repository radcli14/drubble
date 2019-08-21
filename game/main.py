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
from kivy.animation import Animation
from kivy.storage.jsonstore import JsonStore
from kivy.core.text.markup import MarkupLabel
from os.path import join
import cProfile

# Import drubbleFunc to get the supporting functions and classes
import sys
sys.path.append("_applibs")
sys.path.append(".")
from drubbleFunc import *

# Initialize Game State
gs = GameState(p.u0, engine)

# Initialize stats
stats = GameScore()

try:
    # Initialize drums
    num_loops = 2
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

    # Load the sounds that play on bounces
    stool_sound = SoundLoader.load('a/GoGo_crank_hit_Stool.wav')
    floor_sound = SoundLoader.load('a/GoGo_guitar_hit_slide_Floor.wav')
except:
    print('failed loading wav')

# Set the sky blue background color
Window.clearcolor = (cyan[0], cyan[1], cyan[2], 1)
print('dRuBbLe game launched from the ', platform, ' platform')
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
    num_bg = 5

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

    # Markers
    yardLine = []
    yardMark = []
    nMarks = 0

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
        while x + self.xpos < 0:
            x += 100.0 * self.num_bg
        xmod = fmod(x+self.xpos, 100.0 * self.num_bg) / 100.0
        xrem = fmod(xmod, 1)
        xflr = int(floor(xmod))

        # xsel selects which background textures are used
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

    def anim_in(self, duration=1):
        anim = Animation(opacity=1, duration=duration)
        anim.start(self)

    def anim_out(self, duration=1):
        anim = Animation(opacity=0, duration=duration)
        anim.start(self)

    def make_markers(self, p):
        with self.canvas:
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

                # Numbers
                strxr = str(xr)  # String form of xr
                fsize = min(24 * screen_scf, int(p.m2p))  # Font size
                xypos = (int(start_x + 5), self.height / 20 - fsize)  # Position of text
                lsize = (len(strxr) * fsize / 2.0, fsize)  # Label size
                if k >= self.nMarks:
                    self.yardLine.append(Line(points=(start_x, start_y, end_x, end_y), width=1.5))
                    self.yardMark.append(Label(font_size=fsize,
                                               size=lsize, pos=xypos,
                                               text=strxr, color=(1, 1, 1, 1),
                                               halign='left', valign='top'))
                    self.add_widget(self.yardMark[k])
                    self.nMarks += 1
                else:
                    self.yardLine[k].points = (start_x, start_y, end_x, end_y)
                    self.yardMark[k].font_size = fsize
                    self.yardMark[k].size = lsize
                    self.yardMark[k].pos = xypos
                    self.yardMark[k].text = strxr

            # Cleanup
            if self.nMarks > xrng_n:
                for k in range(self.nMarks - xrng_n):
                    self.yardMark.pop(xrng_n)
                    self.yardLine[xrng_n].points = (0, 0)
                    self.yardLine.pop(xrng_n)
                    self.nMarks = xrng_n


class SplashScreen(Widget):
    def __init__(self, w=width*screen_scf, h=height*screen_scf, splash_duration=4.0, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        self.width = w
        self.height = h
        self.opacity = 0.0
        anim = Animation(opacity=1.0, duration=splash_duration)
        anim.start(self)
        Clock.schedule_once(self.confirm_showed_splash, splash_duration)

    def confirm_showed_splash(self, dt):
        gs.showedSplash = True

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.width = w
        self.height = h

    def anim_out(self, w=width*screen_scf):
        anim = Animation(x=w/2.0, y=0, size=(0, 0), opacity=0, duration=0.5, t='in_back')
        anim.start(self)


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
    line_width = screen_scf * 1.5
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
        if gs.game_mode < 7:
            self.trajectory = intersperse(x, y)
        else:
            self.trajectory = []

    def clear(self):
        self.ball_alpha = 0.0

    def anim_in(self):
        anim = Animation(opacity=1.0, duration=1)
        anim.start(self)

    def anim_out(self):
        anim = Animation(opacity=0.0, duration=1)
        anim.start(self)


# Returns the center_x, center_y, and diameter of the stick
def get_stick_pos(ch):
    return ch.pos[0]+ch.size[0]/2.0, ch.pos[1]+ch.size[1]/2.0, ch.size[0]


def touchStick(loc, stick):
    tCnd = [loc[0] > stick.pos[0],
            loc[0] < stick.pos[0] + stick.size[0],
            loc[1] > stick.pos[1],
            loc[1] < stick.pos[1] + stick.size[1]]

    # Touched inside the stick
    if all(tCnd):
        x = min(max(p.tsens * (2.0 * (loc[0] - stick.pos[0]) / stick.size[0] - 1), -1), 1)
        y = min(max(p.tsens * (2.0 * (loc[1] - stick.pos[1]) / stick.size[1] - 1), -1), 1)
        return x, y
        # mag = sqrt(x ** 2 + y ** 2)
        # ang = round(4.0 * atan2(y, x) / pi) * pi / 4
        # return mag * cos(ang), mag * sin(ang)
    else:
        return 0, 0


class Stick(Widget):
    id_code = None
    is_on_screen = False

    # Control values
    ctrl = ListProperty([0.0, 0.0])

    def __init__(self, norm_size=(0.2, 0.2), norm_pos=(0.0, 0.0),
                 w=width*screen_scf, h=height*screen_scf, out_position='left', **kwargs):
        super(Stick, self).__init__(**kwargs)
        self.norm_size = norm_size
        self.norm_pos = norm_pos
        self.size = self.norm_size[0] * width * screen_scf, self.norm_size[1] * width * screen_scf
        self.pos = self.norm_pos[0] * width * screen_scf, self.norm_pos[1] * height * screen_scf

        self.ctrl = [0, 0]

        # Start with it off screen
        self.out_position = out_position
        if self.out_position == 'left':
            self.pos[0] = -self.norm_size[0] * w
        else:
            self.pos[0] = w

        # print('Instantiated a stick at pos =', self.pos, 'and size =', self.size)

    def update_el(self, x, y):
        self.ctrl = [x, y]

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        if self.is_on_screen:
            self.pos[0] = self.norm_pos[0] * w
        elif self.out_position == 'left':
            self.pos[0] = -self.norm_size[0] * w
        else:
            self.pos[0] = w
        self.size = self.norm_size[0] * w, self.norm_size[1] * w
        self.pos[1] = self.norm_pos[1] * h
        # print('Resized a stick to size =', self.size, 'and pos =', self.pos)

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=0.25):
        in_x = self.norm_pos[0] * w
        in_y = self.norm_pos[1] * h
        anim = Animation(x=in_x, y=in_y, duration=duration, t='out_back')
        anim.start(self)
        self.is_on_screen = True
        # print('Moved a stick (anim_in) to size =', self.size, 'and pos =', (in_x, in_y))

    def anim_out(self, w=width*screen_scf, h=height*screen_scf):
        if self.out_position == 'left':
            out_x = -self.norm_size[0] * w
        else:
            out_x = w
        out_y = self.norm_pos[1] * h
        anim = Animation(x=out_x, y=out_y, duration=0.25, t='in_back')
        anim.start(self)
        self.is_on_screen = False
        # print('Moved a stick (anim_out) to size =', self.size, 'and pos =', (out_x, out_y))


# Create OptionButtons class
class OptionButtons(Widget):
    background_color = ListProperty([1, 1, 1, 0.75])
    background_normal = 'a/button.png'
    text = StringProperty('')
    label_font = StringProperty('a/airstrea.ttf')
    label_font_size = NumericProperty(0.0)
    label_color = ListProperty([0.0, 0.0, 0.0, 1.0])
    out_position = StringProperty('')
    is_on_screen = False

    def __init__(self, norm_pos=(0.0, 0.0), norm_size=(0.5, 0.1), norm_font_size=0.05,
                 w=width*screen_scf, h=height*screen_scf, out_position='top', **kwargs):
        super(OptionButtons, self).__init__()
        self.pos = [norm_pos[0] * w, norm_pos[1] * h]
        self.size = [norm_size[0] * w, norm_size[1] * h]
        self.text = kwargs['text']
        self.norm_pos = norm_pos
        self.norm_size = norm_size
        self.norm_font_size = norm_font_size
        self.label_font_size = norm_font_size * h
        self.label_color = [kwargs['color'][0], kwargs['color'][1], kwargs['color'][2], 1]
        self.out_position = out_position

        # Initialize with the button positioned outside
        if self.out_position == 'top':
            self.pos[1] = h
        elif self.out_position == 'bottom':
            self.pos[1] = -self.size[1]
        elif self.out_position == 'left':
            self.pos[0] = -self.size[0]
        elif self.out_position == 'right':
            self.pos[0] = w

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.size = [self.norm_size[0] * w, self.norm_size[1] * h]
        if self.is_on_screen:
            self.pos = [self.norm_pos[0] * w, self.norm_pos[1] * h]
        elif self.out_position == 'top':
            self.pos = [self.norm_pos[0] * w, h]
        elif self.out_position == 'bottom':
            self.pos = [self.norm_pos[0] * w, -self.size[1]]
        elif self.out_position == 'left':
            self.pos = [-self.size[0],  self.norm_pos[1] * h]
        elif self.out_position == 'right':
            self.pos = [w, self.norm_pos[1] * h]

        self.label_font_size = self.norm_font_size * h

    def detect_touch(self, loc):
        touch_conditions = [loc[0] > self.pos[0],
                            loc[0] < self.pos[0] + self.size[0],
                            loc[1] > self.pos[1],
                            loc[1] < self.pos[1] + self.size[1]]
        return all(touch_conditions)

    def background_touched(self, dt=0):
        self.background_color = (0, 0, 1, 0.5)

    def background_untouched(self, dt=0):
        self.background_color = (1, 1, 1, 0.75)

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=0.5):
        anim = Animation(x=self.norm_pos[0]*w, y=self.norm_pos[1]*h, duration=duration, t='out_back')
        anim.start(self)
        self.is_on_screen = True

    def anim_out(self, w=width*screen_scf, h=height*screen_scf, duration=0.5):
        out_x = self.pos[0]
        out_y = self.pos[1]
        if self.out_position == 'left':
            out_x = -self.width
        elif self.out_position == 'right':
            out_x = w
        if self.out_position == 'bottom':
            out_y = -self.size[1]
        elif self.out_position == 'top':
            out_y = h
        anim = Animation(x=out_x, y=out_y, duration=duration, t='in_back')
        anim.start(self)
        self.is_on_screen = False

    def anim_out_then_in(self, w=width*screen_scf, h=height*screen_scf, duration=10):
        out_x = self.pos[0]
        out_y = self.pos[1]
        if self.out_position == 'left':
            out_x = -self.width
        elif self.out_position == 'right':
            out_x = w
        if self.out_position == 'bottom':
            out_y = -self.size[1]
        elif self.out_position == 'top':
            out_y = h
        anim_out = Animation(x=out_x, y=out_y, duration=0.5, t='in_back')
        anim_pause = Animation(x=out_x, y=out_y, duration=(duration-1), t='in_back')
        anim_in = Animation(x=self.norm_pos[0]*w, y=self.norm_pos[1]*h, duration=0.5, t='out_back')
        anim = anim_out + anim_pause + anim_in
        anim.start(self)
        self.is_on_screen = True


class ScoreLabel(Widget):
    label_text = StringProperty('')
    label_font = StringProperty('a/VeraMono.ttf')
    label_size = NumericProperty(int(0.02 * width * screen_scf))
    is_on_screen = False

    def __init__(self, norm_left=0.0, w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(ScoreLabel, self).__init__()
        self.label_text = kwargs['text']
        self.norm_left = norm_left
        self.size = [0.2 * w, 0.02 * width * screen_scf + 4]
        self.pos = [self.norm_left * w, h]

    def update(self, label_string):
        self.label_text = label_string

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.label_size = int(0.02*w)
        self.size = [0.2 * w, 0.02 * w + 4]
        if self.is_on_screen:
            self.pos = [self.norm_left * w, h - self.label_size - 4]
        else:
            self.pos = [self.norm_left * w, h]

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=0.1):
        in_x = self.norm_left * w
        in_y = h - self.label_size - 4
        anim = Animation(x=in_x, y=in_y, duration=duration)
        anim.start(self)
        self.is_on_screen = True

    def anim_out(self, w=width*screen_scf, h=height*screen_scf, duration=0.1):
        out_x = self.norm_left * w
        out_y = h
        anim = Animation(x=out_x, y=out_y, duration=duration, t='in_elastic')
        anim.start(self)
        self.is_on_screen = False


class HighScoreLabel(Widget):
    # Initiate the widget properties
    label_text = StringProperty('')
    label_font = StringProperty('a/Airstream.ttf')
    this_run = StringProperty('')
    best_run = StringProperty('')
    is_high = StringProperty('')
    font_size = NumericProperty(0)
    label_color = ListProperty([1, 0, 0, 1])
    outline_width = NumericProperty(2 * screen_scf)
    outline_color = ListProperty([1, 1, 1])
    ratio_from_top = 0.77
    is_on_screen = False

    def __init__(self, outside_position='top', vertical_position=0,
                 label_text='', this_run='This Run', best_run='Best',
                 w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(HighScoreLabel, self).__init__()
        # Outside position is a string, determining where the button goes when off-screen
        self.outside_position = outside_position

        # Vertical position is an integer, goes from top [0] to bottom [4] when on-screen
        self.vertical_position= vertical_position

        # Label text is the left column [distance, height, boing, or score]
        self.label_text = label_text

        # Left position of the widget when on-screen
        self.label_left = 0.08 * w

        # Current scores and the saved best score
        self.this_run = this_run
        self.best_run = best_run

        # Sizing
        self.width = 0.9 * w
        self.height = 0.1 * h
        self.font_size = 0.09 * h

        # Start with the widget off-screen
        if self.is_on_screen:
            self.pos = [self.label_left, (self.ratio_from_top - 0.1 * self.vertical_position) * h]
        else:
            if self.outside_position == 'left':
                self.pos[0] = -self.width
            elif self.outside_position == 'right':
                self.pos[0] = w
            if self.outside_position == 'bottom':
                self.pos[1] = -self.size[1]
            elif self.outside_position == 'top':
                self.pos[1] = h

    def anim_in(self, h=height*screen_scf, duration=1):
        in_x = self.label_left
        in_y = (self.ratio_from_top - 0.1 * self.vertical_position) * h
        anim = Animation(x=in_x, y=in_y, duration=duration, t='out_elastic')
        anim.start(self)
        print(self.label_text, ' ', self.this_run, ' ', self.best_run, ' ', self.is_high)

    def anim_out(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        out_x = self.pos[0]
        out_y = self.pos[1]
        if self.outside_position == 'left':
            out_x = -self.width
        elif self.outside_position == 'right':
            out_x = w
        if self.outside_position == 'bottom':
            out_y = -self.size[1]
        elif self.outside_position == 'top':
            out_y = h
        anim = Animation(x=out_x, y=out_y, duration=duration, t='in_elastic')
        anim.start(self)

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.label_left = 0.08 * w
        self.width = 0.9 * w
        self.height = 0.1 * h
        self.font_size = 0.09 * h

        if self.is_on_screen:
            self.pos = [self.label_left, (self.ratio_from_top - 0.1 * self.vertical_position) * h]
        else:
            if self.outside_position == 'left':
                self.pos[0] = -self.width
            elif self.outside_position == 'right':
                self.pos[0] = w
            if self.outside_position == 'bottom':
                self.pos[1] = -self.size[1]
            elif self.outside_position == 'top':
                self.pos[1] = h


class RotatingRing(Image):
    angle = NumericProperty(0.0)
    center = ListProperty((0.0, 0.0))

    def start_rotation(self):
        anim = Animation(angle=360, duration=3.14)
        anim += Animation(angle=360, duration=3.14)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class Tutorial(Widget):
    n = 0
    msg = ['Welcome to dRuBbLe!!!\nTap to Begin',
           'Touch the stick on the\nlower left to move the stool',
           'Touch the stick on the\nlower right to move the player',
           'Use the action button in\nthe upper right to start the game',
           'Tap once to set the launch angle',
           'Tap again to set the speed\nand launch the ball',
           'Try to bounce the ball\noff the top of your stool',
           'Bounce as far and as high as possible',
           'Good Luck!!!',
           '']
    is_paused = False

    # Text label properties
    label_text = StringProperty('')
    label_font_size = NumericProperty(0.0)
    label_pos = ListProperty([0.5 * Window.width, 0.6 * Window.height])
    label_size = ListProperty([0.0, 0.0])
    label_outline_width = 3.0 * screen_scf
    label_opacity = NumericProperty(0.0)

    # Rotating ring properties
    ring_pos = ListProperty([0.0, 0.0])
    ring_size = ListProperty([0.0, 0.0])
    ring_angle = NumericProperty(0.0)
    ring_center = ListProperty((0.0, 0.0))
    ring_opacity = NumericProperty(0.0)

    def __init__(self, w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(Tutorial, self).__init__()
        self.n = 0
        self.width = w
        self.height = h
        self.pos = (0, 0)

        # Text Label Properties
        self.label_text = ''
        self.label_font_size = 0.0
        self.label_pos = [0.5 * w, 0.6 * h]
        self.label_size = [0.0, 0.0]
        self.label_opacity = 0.0

        # Create the ring widget
        self.ring_pos = [0.0, 0.0]
        self.ring_size = [0.0, 0.0]
        self.ring_center = [0.0, 0.0]
        self.ring_opacity = 0.0

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

    def change_message(self, dt):
        self.label_text = self.msg[self.n]

    def set_pause_false(self, dt):
        self.is_paused = False

    def pause(self, dt):
        self.is_paused = True
        Clock.schedule_once(self.set_pause_false, dt)

    def new_ring_position(self, ring_size=(0, 0), ring_pos=(0, 0), in_duration=0.0, out_duration=0.0):
        anim_ring_out = Animation(ring_opacity=0.0, duration=out_duration)
        anim_ring_pos = Animation(ring_size=ring_size, ring_pos=ring_pos, ring_angle=0.0,
                                  ring_center=(ring_pos[0]+0.5*ring_size[0], ring_pos[1]+0.5*ring_size[1]),
                                  ring_opacity=0.0, duration=0)
        anim_ring_in = Animation(ring_opacity=1.0, ring_angle=360, duration=in_duration)
        anim_ring_rotate = Animation(ring_angle=1080, duration=2*in_duration)
        anim = anim_ring_out + anim_ring_pos + anim_ring_in + anim_ring_rotate
        anim.start(self)

    def clear_ring(self, out_duration=1.0):
        anim_ring_out = Animation(ring_opacity=0.0, duration=out_duration)
        anim_ring_out.start(self)

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        # Determine the width and height scale factors
        if self.width > 0:
            width_scale = w / self.width
            height_scale = h / self.height
        else:
            width_scale = 1.0
            height_scale = 1.0

        # Resize the entire widget
        self.width = w
        self.height = h

        # Resize the label
        self.label_font_size = 0.12 * h
        self.label_pos = [0.2 * w, 0.6 * h]
        self.label_size = [0.6 * w, 0.3 * h]

        # Resize the ring
        self.ring_size = (self.ring_size[0] * width_scale, self.ring_size[1] * height_scale)
        self.ring_pos = (self.ring_pos[0] * width_scale, self.ring_pos[1] * height_scale)
        self.ring_center = (self.ring_pos[0] + 0.5 * self.ring_size[0], self.ring_pos[1] + 0.5 * self.ring_size[1])

    def check_touches(self, app_object):
        if self.is_paused:
            return

        was_touched = False
        w = self.width
        h = self.height

        if self.n == 0:
            was_touched = True
            app_object.tiltStick.anim_in(w=self.width, h=self.height, duration=1)
            self.new_ring_position(ring_size=(0.36*w, 0.36*w), ring_pos=(-0.08*w, -0.08*w+0.05*h),
                                   in_duration=3.0, out_duration=0.0)
        elif self.n == 1 and abs(gs.ctrl[2]) + abs(gs.ctrl[3]) != 0.0:
            was_touched = True
            app_object.moveStick.anim_in(w=self.width, h=self.height, duration=1)
            self.new_ring_position(ring_size=(0.36*w, 0.36*w), ring_pos=(0.72*w, -0.08*w+0.05*h),
                                   in_duration=2.0, out_duration=3.0)
        elif self.n == 2 and abs(gs.ctrl[1]) + abs(gs.ctrl[2]) != 0.0:
            was_touched = True
            app_object.actionButt.anim_in(w=self.width, h=self.height)
            self.new_ring_position(ring_size=(0.36*w, 0.36*w), ring_pos=(0.72*w, 0.59*h),
                                   in_duration=2.0, out_duration=3.0)
        elif self.n == 3 and gs.game_mode >= 4:
            was_touched = True
        elif self.n == 4 and gs.game_mode >= 5:
            was_touched = True
        elif self.n == 5 and gs.game_mode >= 6:
            was_touched = True
        elif self.n == 6:
            was_touched = True
            self.clear_ring(out_duration=1.0)
            app_object.optionButt.anim_in(w=self.width, h=self.height)
        elif self. n == 7:
            was_touched = True
        elif self.n == 8:
            was_touched = True

        # Switch to the next message if there was a touch
        next_pause_duration = 3.0 if self.n < 6 else 5.0
        if was_touched:
            self.pause(next_pause_duration)
            self.n += 1
            Clock.schedule_once(self.change_message, 2)
            self.switch(w=app_object.width, h=app_object.height, duration=4.0)

        # Remove widgets if reached end of tutorial
        if self.n >= self.msg.__len__():
            self.anim_out()
            app_object.tutorial_mode = False
        return

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        anim = Animation(label_size=(0.6*w, 0.3*h), label_pos=(0.2*w, 0.6*h), label_opacity=1.0,
                         label_font_size=0.12*h, duration=duration, t='out_elastic')
        anim.start(self)

    def anim_out(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        anim = Animation(label_size=(0.6*w, 0.3*h), label_pos=(0.2*w, 0.6*h), label_opacity=0.0,
                         ring_size=(0, 0), ring_opacity=0.0,
                         label_font_size=0.07*self.height, duration=0.33*duration, t='out_elastic')
        anim.start(self)

    def switch(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        anim_out = Animation(label_size=(0, 0), label_pos=(0.5*w, 0.5*h), label_opacity=0.0, label_font_size=0.0,
                             duration=0.25*duration, t='in_elastic')
        anim_pause = Animation(duration=0.5*duration)
        anim_in = Animation(label_size=(0.6*w, 0.3*h), label_pos=(0.2*w, 0.6*h), label_opacity=1.0,
                            label_font_size=0.12*self.height, duration=0.25*duration, t='out_elastic')
        anim = anim_out + anim_pause + anim_in
        anim.start(self)


class DrubbleGame(Widget):
    tutorial_mode = False

    def __init__(self, **kwargs):
        super(DrubbleGame, self).__init__(**kwargs)
        self.bind(size=self.resize_canvas)
        if platform in ('linux', 'windows', 'win', 'macosx'):
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self._keyboard.bind(on_key_up=self._on_keyboard_up)
        #Window.bind(on_joy_hat=self.on_joy_hat)
        #Window.bind(on_joy_ball=self.on_joy_ball)
        Window.bind(on_joy_axis=self.on_joy_axis)
        #Window.bind(on_joy_button_up=self.on_joy_button_up)
        Window.bind(on_joy_button_down=self.on_joy_button_down)
        self.nMarks = 0
        self.weHaveWidgets = False
        self.weHaveButtons = False
        self.needToResize = True
        with self.canvas:
            # Splash screen, init right away
            self.splash = SplashScreen(w=width*screen_scf, h=height*screen_scf)
            self.add_widget(self.splash)

            # Initialize the background
            self.bg = MyBackground()
            #self.add_widget(self.bg)

            # Initialize the tutorial
            self.tutorial = Tutorial()
            #self.add_widget(self.tutorial)

            # Initialize the ball
            self.ball = Ball()
            #self.add_widget(self.ball)

            # Initialize the sticks
            self.moveStick = Stick(norm_size=(0.2, 0.2), norm_pos=(0.8, 0.05), out_position='right')
            self.tiltStick = Stick(norm_size=(0.2, 0.2), norm_pos=(0.0, 0.05), out_position='left')
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

            # Initialize the player faces
            self.myFace = MyFace(image_source='a/myFace2.png', jersey_source='a/MyJersey.png',
                                 shorts_source='a/MyShorts.png', line_color=green, stool_color=white)
            self.LadyFace = MyFace(image_source='a/LadyFace.png', jersey_source='a/LadyJersey.png',
                                   shorts_source='a/LadyShorts.png', line_color=olive, stool_color=gray)

            # Initialize the high score labels
            self.high_score_header = HighScoreLabel()
            self.high_dist_label = HighScoreLabel(outside_position='left', vertical_position=1,
                                                  label_text='Distance', this_run='%0.1f' % stats.stool_dist,
                                                  best_run='%0.1f' % stats.high_stool_dist[p.nPlayer-1])
            self.high_height_label = HighScoreLabel(outside_position='right', vertical_position=2,
                                                    label_text='Height', this_run='%0.2f' % stats.max_height,
                                                    best_run='%0.2f' % stats.high_height[p.nPlayer-1])
            self.high_boing_label = HighScoreLabel(outside_position='left', vertical_position=3,
                                                   label_text='Boing!', this_run='%0.0f' % stats.stool_count,
                                                   best_run='%0.0f' % stats.high_stool_count[p.nPlayer-1])
            self.high_score_label = HighScoreLabel(outside_position='right', vertical_position=4,
                                                   label_text='Score', this_run='%0.0f' % stats.score,
                                                   best_run='%0.0f' % stats.high_score[p.nPlayer-1])
            self.add_widget(self.high_score_header)
            self.add_widget(self.high_dist_label)
            self.add_widget(self.high_height_label)
            self.add_widget(self.high_boing_label)
            self.add_widget(self.high_score_label)

            # Initialize the option and action buttons
            self.singleDrubbleButt = OptionButtons(text='Single dRuBbLe', norm_size=(0.5, 0.2), out_position='left',
                                                   norm_pos=(0.1, 0.7),  norm_font_size=0.14,  color=red)
            self.doubleDrubbleButt = OptionButtons(text='Double dRuBbLe', norm_size=(0.8, 0.2), out_position='right',
                                                   norm_pos=(0.1, 0.4),  norm_font_size=0.14,  color=red)
            self.tutorial_butt = OptionButtons(text='How2', norm_size=(0.25, 0.2), out_position='left',
                                               norm_pos=(0.65, 0.7),  norm_font_size=0.14,  color=red)
            self.optionButt = OptionButtons(text='Options', norm_size=(0.18, 0.06), out_position='left',
                                            norm_pos=(0.01, 0.88), norm_font_size=0.055, color=red)
            self.actionButt = OptionButtons(text=p.actionMSG[3], norm_size=(0.18, 0.06), out_position='right',
                                            norm_pos=(0.81, 0.88),  norm_font_size=0.055, color=red)
            self.add_widget(self.optionButt)
            self.add_widget(self.actionButt)

    def remove_splash(self, dt):
        self.remove_widget(self.splash)

    def add_game_widgets(self, dt):
        print('Adding game widgets')
        # Background
        self.add_widget(self.bg)
        self.bg.anim_in()

        # Ball
        self.add_widget(self.ball)
        self.ball.anim_in()

        # Players
        self.add_widget(self.myFace)
        self.add_widget(self.LadyFace)

        if self.tutorial_mode:
            self.add_widget(self.tutorial)
        else:
            # Option and action buttons
            self.optionButt.anim_in(w=self.width, h=self.height)
            self.actionButt.anim_in(w=self.width, h=self.height)

            # Sticks
            self.moveStick.anim_in(w=self.width, h=self.height)
            self.tiltStick.anim_in(w=self.width, h=self.height)

        # Score labels
        self.time_label.anim_in(w=self.width, h=self.height, duration=0.1)
        self.dist_label.anim_in(w=self.width, h=self.height, duration=0.2)
        self.high_label.anim_in(w=self.width, h=self.height, duration=0.3)
        self.boing_label.anim_in(w=self.width, h=self.height, duration=0.4)
        self.score_label.anim_in(w=self.width, h=self.height, duration=0.5)

        self.weHaveWidgets = True
        self.resize_canvas()
        print('  --> Done!')

    def remove_game_widgets(self):
        self.bg.anim_out()
        self.ball.anim_out()
        self.moveStick.anim_out(w=self.width, h=self.height)
        self.tiltStick.anim_out(w=self.width, h=self.height)
        self.myFace.clear()
        self.LadyFace.clear()
        self.time_label.anim_out(w=self.width, h=self.height, duration=0.15)
        self.dist_label.anim_out(w=self.width, h=self.height, duration=0.30)
        self.high_label.anim_out(w=self.width, h=self.height, duration=0.45)
        self.boing_label.anim_out(w=self.width, h=self.height, duration=0.60)
        self.score_label.anim_out(w=self.width, h=self.height, duration=0.75)

        self.optionButt.anim_out(w=self.width, h=self.height)
        self.actionButt.anim_out(w=self.width, h=self.height)

        Clock.schedule_once(self.remove_game_widgets_callback, 1.0)
        self.weHaveWidgets = False

    def remove_game_widgets_callback(self, dt):
        # Create the callback so that there is a delay to allow the
        # animations to complete before removing the widgets.
        self.remove_widget(self.bg)
        self.remove_widget(self.ball)
        self.remove_widget(self.myFace)
        self.remove_widget(self.LadyFace)

    def add_option_buttons(self, dt):
        # Add option screen buttons
        self.add_widget(self.singleDrubbleButt)
        self.add_widget(self.doubleDrubbleButt)
        self.add_widget(self.tutorial_butt)
        self.singleDrubbleButt.anim_in(w=self.width, h=self.height)
        self.doubleDrubbleButt.anim_in(w=self.width, h=self.height)
        self.tutorial_butt.anim_in(w=self.width, h=self.height)

    def remove_option_buttons(self):
        # Add option screen buttons
        self.singleDrubbleButt.anim_out(w=self.width, h=self.height)
        self.doubleDrubbleButt.anim_out(w=self.width, h=self.height)
        self.tutorial_butt.anim_out(w=self.width, h=self.height)
        self.remove_widget(self.singleDrubbleButt)
        self.remove_widget(self.doubleDrubbleButt)
        self.remove_widget(self.tutorial_butt)

    def add_high_scores(self):
        # Update the strings for the current scores
        self.high_dist_label.this_run = '%0.1f' % stats.stool_dist
        self.high_height_label.this_run = '%0.2f' % stats.max_height
        self.high_boing_label.this_run = '%0.0f' % stats.stool_count
        self.high_score_label.this_run = '%0.0f' % stats.score

        # Calculate percentiles
        pct_dist_str = return_percentile(stats.all_stool_dist[p.nPlayer-1], stats.stool_dist)
        pct_height_str = return_percentile(stats.all_height[p.nPlayer - 1], stats.max_height)
        pct_boing_str = return_percentile(stats.all_stool_count[p.nPlayer - 1], stats.stool_count)
        pct_score_str = return_percentile(stats.all_score[p.nPlayer - 1], stats.score)

        # Include either a percentile, or new high string
        hstr = 'New High!'
        self.high_dist_label.is_high = hstr if stats.stool_dist > stats.high_stool_dist[p.nPlayer-1] else pct_dist_str
        self.high_height_label.is_high = hstr if stats.max_height > stats.high_height[p.nPlayer-1] else pct_height_str
        self.high_boing_label.is_high = hstr if stats.stool_count>stats.high_stool_count[p.nPlayer-1] else pct_boing_str
        self.high_score_label.is_high = hstr if stats.score > stats.high_score[p.nPlayer-1] else pct_score_str

        # Update the strings for the high scores
        self.high_dist_label.best_run = '%0.1f' % stats.high_stool_dist[p.nPlayer-1]
        self.high_height_label.best_run = '%0.2f' % stats.high_height[p.nPlayer-1]
        self.high_boing_label.best_run = '%0.0f' % stats.high_stool_count[p.nPlayer-1]
        self.high_score_label.best_run = '%0.0f' % stats.high_score[p.nPlayer-1]

        # Bring the high scores onto the screen
        self.high_score_header.anim_in(h=self.height, duration=1)
        self.high_dist_label.anim_in(h=self.height, duration=1)
        self.high_height_label.anim_in(h=self.height, duration=1)
        self.high_boing_label.anim_in(h=self.height, duration=1)
        self.high_score_label.anim_in(h=self.height, duration=1)

        # Update the high scores
        stats.update_high()

    def remove_high_scores(self, duration=1):
        # Take the high scores off the screen
        self.high_score_header.anim_out(w=self.width, h=self.height, duration=duration)
        self.high_dist_label.anim_out(w=self.width, h=self.height, duration=duration)
        self.high_height_label.anim_out(w=self.width, h=self.height, duration=duration)
        self.high_boing_label.anim_out(w=self.width, h=self.height, duration=duration)
        self.high_score_label.anim_out(w=self.width, h=self.height, duration=duration)

    # Controls
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(self.keyPush, keycode, 1))
        if gs.game_mode == 1 and gs.showedSplash:
            cycle_modes(gs, stats, engine)
        elif gs.game_mode == 2 and keycode[1] == 'spacebar':
            self.single_drubble_button_press()
        elif gs.game_mode > 2 and keycode[1] == 'spacebar':
            self.action_button_press()
        elif gs.game_mode > 2 and keycode[1] == 'escape':
            self.option_button_press()
        return True
    
    def _on_keyboard_up(self, keyboard, keycode):
        self.keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(self.keyPush, keycode, 0))
        return True
    
    def on_touch_down(self, touch):
        loc = (touch.x, touch.y)
        if gs.game_mode == 1 and gs.showedSplash:
            cycle_modes(gs, stats, engine)
        elif gs.game_mode == 2 and self.singleDrubbleButt.detect_touch(loc):
            self.single_drubble_button_press()
        elif gs.game_mode == 2 and self.doubleDrubbleButt.detect_touch(loc):
            self.double_drubble_button_press()
        elif gs.game_mode == 2 and self.tutorial_butt.detect_touch(loc):
            self.tutorial_button_press()
        elif gs.game_mode > 2:
            # Cycle through modes if touched the action or option_butt
            if self.actionButt.detect_touch(loc) and not self.tutorial.is_paused:
                self.action_button_press()
            if self.optionButt.detect_touch(loc):
                self.option_button_press()

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

        if self.tutorial_mode:
            self.tutorial.check_touches(self)

    def on_touch_move(self, touch):
        if gs.game_mode > 2 and self.weHaveWidgets:
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
        if gs.game_mode > 2 and self.weHaveWidgets:
            if touch.id == self.moveStick.id_code:
                self.moveStick.update_el(0, 0)
                gs.ctrl[0:2] = [0, 0]
                
            if touch.id == self.tiltStick.id_code:
                self.tiltStick.update_el(0, 0)
                gs.ctrl[2:4] = [0, 0]

    def on_joy_axis(self, win, stickid, axisid, value):
        if axisid == 0:
            # Stool tilt
            gs.ctrl[3] = -value / 32768
        elif axisid == 1:
            # Stool up/down
            gs.ctrl[2] = value / 32768
        elif axisid == 2:
            # Left/right movement
            gs.ctrl[0] = value / 32768
        elif axisid == 3:
            # Up/down movement
            gs.ctrl[1] = value / 32768

    def on_joy_button_down(self, win, stickid, buttonid):
        if gs.game_mode == 1:
            cycle_modes(gs, stats, engine)
        elif gs.game_mode == 2:
            if buttonid in (0, 6):
                # A button
                self.single_drubble_button_press()
            elif buttonid in (1, 7):
                # B button
                self.double_drubble_button_press()
        elif gs.game_mode > 2:
            if buttonid in (1, 6):
                # Left trigger
                self.option_button_press()
            elif buttonid in (0, 7):
                # Right trigger
                self.action_button_press()

    # What to do when the single drubble button is pressed
    def single_drubble_button_press(self):
        # Specify that this will be the one player version, and start game
        p.nPlayer = 1
        cycle_modes(gs, stats, engine)

        # Add the in-game widgets
        Clock.schedule_once(self.add_game_widgets, 1.0)
        self.remove_option_buttons()

        # Turn the button blue momentarily
        self.singleDrubbleButt.background_touched()
        Clock.schedule_once(self.singleDrubbleButt.background_untouched, 0.1)

    # What to do when the double drubble button is pressed
    def double_drubble_button_press(self):
        # Specify this will be the two player version, and start game
        p.nPlayer = 2
        cycle_modes(gs, stats, engine)

        # Add the in-game widgets
        Clock.schedule_once(self.add_game_widgets, 1.0)
        self.remove_option_buttons()

        # Turn the button blue momentarily
        self.doubleDrubbleButt.background_touched()
        Clock.schedule_once(self.doubleDrubbleButt.background_untouched, 0.1)

    # What to do when option button is pressed
    def option_button_press(self):
        # Return to the option screen, removing the in-game widgets
        gs.game_mode = 1
        self.remove_game_widgets()
        self.remove_high_scores()
        Clock.schedule_once(self.add_option_buttons, 1.0)

        # Reset game states and scores
        cycle_modes(gs, stats, engine)

        # Turn the button blue momentarily
        self.optionButt.background_touched()
        Clock.schedule_once(self.optionButt.background_untouched, 0.1)

    # What to do when action button is pressed
    def action_button_press(self):
        # Progress through the speed/angle setting, game, then high score
        cycle_modes(gs, stats, engine)

        # Update the button text and color
        self.actionButt.text = p.actionMSG[gs.game_mode]
        self.actionButt.background_color = (0, 0.5, 1, 0.5)

        # If on completion of the game, add the high scores
        # If on restart of game, remove the high scores
        # Also move the sticks and option buttons out of the way
        if gs.game_mode == 7:
            self.add_high_scores()
            self.bg.anim_out()
            self.moveStick.anim_out(w=self.width, h=self.height)
            self.tiltStick.anim_out(w=self.width, h=self.height)
            self.optionButt.anim_out_then_in(w=self.width, h=self.height)
            self.actionButt.anim_out_then_in(w=self.width, h=self.height)
        elif gs.game_mode == 3:
            self.remove_high_scores()
            self.bg.anim_in()
            self.moveStick.anim_in(w=self.width, h=self.height)
            self.tiltStick.anim_in(w=self.width, h=self.height)

        # Turn the button blue momentarily
        self.actionButt.background_touched()
        Clock.schedule_once(self.actionButt.background_untouched, 0.1)

    # What to do when the tutorial button is pressed
    def tutorial_button_press(self):
        # Specify that this will be the one player version, and start game
        p.nPlayer = 1
        cycle_modes(gs, stats, engine)

        # Turn on tutorial mode
        self.tutorial_mode = True
        self.tutorial.__init__(w=self.width, h=self.height)
        self.tutorial.label_text = self.tutorial.msg[0]
        self.tutorial.anim_in(w=self.width, h=self.height, duration=1.0)
        self.tutorial.pause(2)

        # Add selected widgets
        self.remove_option_buttons()
        Clock.schedule_once(self.add_game_widgets, 1.0)

        # Turn the button blue momentarily
        self.tutorial_butt.background_touched()
        Clock.schedule_once(self.tutorial_butt.background_untouched, 0.1)

    def resize_canvas(self, *args):
        # Splash screen
        if not gs.showedSplash:
            self.splash.resize(w=self.width, h=self.height)

        # High score labels
        self.high_score_header.resize(w=self.width, h=self.height)
        self.high_dist_label.resize(w=self.width, h=self.height)
        self.high_height_label.resize(w=self.width, h=self.height)
        self.high_boing_label.resize(w=self.width, h=self.height)
        self.high_score_label.resize(w=self.width, h=self.height)

        # Score labels
        self.time_label.resize(w=self.width, h=self.height)
        self.dist_label.resize(w=self.width, h=self.height)
        self.high_label.resize(w=self.width, h=self.height)
        self.boing_label.resize(w=self.width, h=self.height)
        self.score_label.resize(w=self.width, h=self.height)

        # Sticks
        self.moveStick.resize(w=self.width, h=self.height)
        self.tiltStick.resize(w=self.width, h=self.height)

        # Background image
        self.bg.resize(self.width, self.height)
        self.bg.bottomLineHeight = self.height/20.0

        # Buttons
        self.singleDrubbleButt.resize(w=self.width, h=self.height)
        self.doubleDrubbleButt.resize(w=self.width, h=self.height)
        self.tutorial_butt.resize(w=self.width, h=self.height)
        self.actionButt.resize(w=self.width, h=self.height)
        self.optionButt.resize(w=self.width, h=self.height)

        # Tutorial
        self.tutorial.resize(w=self.width, h=self.height)

    # Time step the game
    def update(self, dt):
        if self.needToResize:
            self.resize_canvas()
            self.needToResize = False

        if self.weHaveWidgets:
            self.actionButt.text = p.actionMSG[gs.game_mode]

        # Either update the splash, or add the widgets
        if gs.game_mode == 2 and not self.weHaveButtons:
            self.splash.anim_out(w=self.width)
            Clock.schedule_once(self.remove_splash, 1.0)
            Clock.schedule_once(self.add_option_buttons, 1.0)
            self.weHaveButtons = True
        #elif gs.game_mode > 2 and not self.weHaveWidgets:
        #    Clock.schedule_once(self.add_game_widgets, 1.0)

        # Angle and speed settings
        if 2 < gs.game_mode < 6:
            gs.setAngleSpeed()

        # Call the simStep method
        ddt = gs.sim_step(p, gs, stats)

        # Adjust pitch of the loop that is playing (TBR not working)
        #print(ddt*fs)
        #for k in range(num_loops):
        #    loop[k].pitch = ddt * fs

        if gs.game_mode > 2:
            stats.update(gs)

            # Update score line
            self.time_label.update('Time %9.1f' % gs.t)
            self.dist_label.update('Distance %6.1f' % stats.stool_dist)
            self.high_label.update('Height %7.2f' % stats.max_height)
            self.boing_label.update('Boing! %7.0f' % stats.stool_count)
            self.score_label.update('Score %8.0f' % stats.score)

        # Player drawing settings        
        xrng, yrng, m2p, po = set_ranges(gs.u, self.width)
            
        p1.width = p2.width = self.width
        p1.height = p2.height = self.height
        
        p1.update(gs, self.width)
        p2.update(gs, self.width)
        
        if gs.game_mode > 2:
            xMean = (gs.xb+gs.xp[0])/2.0
            self.bg.update(xMean, gs.yb, self.width, self.height, m2p)
            self.bg.make_markers(p1)
            self.moveStick.update_el(gs.ctrl[0], gs.ctrl[1])
            self.tiltStick.update_el(-gs.ctrl[3], gs.ctrl[2])
            self.myFace.update(gs.xp[0], gs.yp[0] + 1.5*p.d, gs.lp[0], gs.tp[0], m2p, po,
                               self.width, self.height, p1.player)

            # Update the ball
            self.ball.update(gs.xb, gs.yb, p1.m2p, p1.po, self.width, self.height)

            if p.nPlayer > 1:
                self.LadyFace.update(gs.xp[1], gs.yp[1] + 1.5 * p.d, gs.lp[1], gs.tp[1], m2p, po,
                                     self.width, self.height, p2.player)

            # Make the bounce sounds
            if gs.StoolBounce:
                stool_sound.volume = min(0.1, norm([gs.dxb, gs.dyb]) / 50.0)
                stool_sound.play()
            elif gs.FloorBounce:
                floor_sound.volume = norm([gs.dxb, gs.dyb]) / 15.0
                floor_sound.play()


class DrubbleApp(App):
    icon = 'a/icon.png'

    '''
    def on_start(self):
        self.profile = cProfile.Profile()
        self.profile.enable()

    def on_stop(self):
        self.profile.disable()
        self.profile.dump_stats('drubble.profile')
    '''

    def build(self):
        game = DrubbleGame()
        data_dir = getattr(self, 'user_data_dir')
        stats.init_high(join(data_dir, 'scores.json'))
        Clock.schedule_interval(game.update, 1.0/fs)
        return game


if __name__ == '__main__':
    DrubbleApp().run()