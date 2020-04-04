#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:18:17 2019

@author: radcli14

Errors

Possible fix for the XCode error "Command PhaseScriptExecution failed with a nonzero exit code"
HareshGediya commented on May 24
Just had the same problem.
I did it by remove file in Pods -> Targets Support Files -> Pods-AppName -> Pods-AppName-frameworks.sh.
And install pod again using pod install.

DSPerson commented on Jun 14
Xcode -> File -> Workspace Setting... -> cut Build System to Legacy Build System. Have Fun

:-1: Undefined symbol: _OBJC_CLASS_$_WKWebView
Go to your Project, click on General, scroll down to Linked Frameworks and Libraries, and add WebKit.framework as Optional. See here: Xcode 6 + iOS 8 SDK but deploy on iOS 7 (UIWebKit & WKWebKit)

-- When validating for app store on 7 October 2019
Invalid Bundle Structure - The binary file 'drubble.app/lib/python3.7/site-packages/numpy/core/lib/libnpymath.a' is not permitted. Your app can’t contain standalone executables or libraries, other than a valid CFBundleExecutable of supported bundles. Refer to the Bundle Programming Guide at https://developer.apple.com/go/?id=bundle-structure for information on the iOS app bundle structure.

ITMS-90683: Missing Purpose String in Info.plist
-- in XCode, click on drubble-info.plist, add entry for "Privacy - Camera Usage Description"

Google AdMob IDs

iOS
AdMob App ID: ca-app-pub-4007502882739240~9117326010
Banner Ad ID: ca-app-pub-4007502882739240/5795838735
iPhone 6/7/8 (4.7 Inch): 750 x 1334 (16 x 9)
iPhone 6/7/8 Plus (5.5 Inch): 1242 x 2208 (16 x 9)
iPhone X (5.8-Inch): 1125 x 2436 (19.5 x 9)

Android
AdMob App ID: ca-app-pub-4007502882739240~4287725061
Banner Ad ID: ca-app-pub-4007502882739240/2325289594
Interstitial Ad ID: ca-app-pub-4007502882739240/3261013033
"""
# Import modules
from math import fmod, floor
from random import randint, random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ListProperty, ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import *
from kivy.utils import platform
from kivy.animation import Animation
# import kivymd as kmd
from os.path import join
import gc as gc
import tracemalloc

# Import drubbleFunc to get the supporting functions and classes
import sys
sys.path.append("_applibs")
sys.path.append(".")
from drubbleFunc import *

if p.profile_mode:
    import cProfile as cProfile
    tracemalloc.start()

# Import Ads
if platform == 'android':
    from kivmob import KivMob, TestIds
    USE_TEST_IDS = False
elif platform == 'ios':
    from pyobjus import autoclass

# Dark mode toggle, for future implementation
isDark = 0

# Set the sky blue background color
Window.clearcolor = teal[isDark]

# Set window size based on platform, if on a desktop then use the iPhone 8 resolution, 16 x 9
print('dRuBbLe game launched from the ' + platform + ' platform')
if platform in ('linux', 'windows', 'win', 'macosx'):
    # iPhone 8 Resolution
    width = 1334
    height = 750

    # iPad Resolution
    width = 1044
    height = 800
    Window.size = (width, height)
else:
    width, height = Window.size

Window.left = 50
# On the retina screen, Window.size gets doubled, this is the correction factor
screen_scf = Window.size[0] / width

# Set the icon
Window.icon = 'a/icon.png'


class Yard(Widget):
    text = StringProperty('')
    font_scale = NumericProperty(0.05)

    def __init__(self, size=(100, 100), pos=(0, 0), text='', **kwargs):
        super(Yard, self).__init__(**kwargs)
        self.size = size
        self.pos = pos
        self.text = text


class MyBackground(Widget):
    # Size of the black bar on the bottom of the screen
    bottom_line_height = NumericProperty(height * screen_scf / 20.0)

    # Set size of the background, before updates
    sz_orig = w_orig, h_orig = (2400.0, 400.0)
    img_w = NumericProperty(w_orig)
    img_h = NumericProperty(h_orig)

    # Number of background images
    num_bg = 6

    # Create the properties for the left edges of the bg images
    bg_left0 = NumericProperty(0.0)
    bg_left1 = NumericProperty(0.0)

    # Create the textures
    textures = [Image(source='a/bg'+str(n)+'.png').texture for n in range(num_bg)]
    bg_text0 = ObjectProperty(None)
    bg_text1 = ObjectProperty(None)

    # Markers
    yard = []
    nMarks = 0

    # Randomize the start location in the backgroun
    xpos = randint(0, 100.0 * num_bg)

    def __init__(self, w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        self.width = w
        self.height = h
        self.opacity = 0.0

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.width = w
        self.height = h

    def update(self, x, y, w, h):
        # xmod is normalized position of the player between 0 and num_bg
        while x + self.xpos < 0:
            x += 100.0 * self.num_bg
        xmod = fmod(x + self.xpos, 100.0 * self.num_bg) / 100.0
        xrem = fmod(xmod, 1)
        xflr = int(floor(xmod))

        # xsel selects which background textures are used
        if xrem <= 0.5:
            xsel = xflr - 1
        else:
            xsel = xflr

        # scf is the scale factor to apply to the background
        scf = (gs.m2p / 70.0)**0.5
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

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        self.width = w
        self.height = h
        Animation.cancel_all(self)
        anim = Animation(opacity=1, duration=duration)
        anim.start(self)

    def anim_out(self, duration=1):
        Animation.cancel_all(self)
        anim = Animation(opacity=0, duration=duration)
        anim.start(self)

    def make_markers(self):
        with self.canvas:
            # xrng_r is the first and last markers on the screen, xrng_n is the number of markers
            pm = -10, 10  # plus minus, prevents flickering of markers on the edges
            xrng_r = [round(gs.xr[i] + pm[i], -1) for i in range(2)]
            xrng_n = int(0.1 * (xrng_r[1] - xrng_r[0])) + 1

            for k in range(max(xrng_n, self.nMarks)):
                # Current yardage
                xr = int(xrng_r[0] + 10 * k)
                mid_x = xr * gs.m2p - gs.po + 0.5 * self.width

                if k >= self.nMarks:
                    # Create a yard mark, and add it to the background object
                    self.yard.append(Yard(pos=(int(mid_x-5.0*gs.m2p), 0), text=str(xr),
                                          size=(int(10.0*gs.m2p), self.bottom_line_height)))
                    self.add_widget(self.yard[k])
                    self.nMarks += 1
                else:
                    # Update an existing yard mark
                    self.yard[k].x = int(mid_x - 5.0 * gs.m2p)
                    self.yard[k].width = int(10.0 * gs.m2p)
                    self.yard[k].text = str(xr)

            # Cleanup
            if self.nMarks > xrng_n:
                for k in range(self.nMarks - xrng_n):
                    self.yard[xrng_n].opacity = 0.0
                    self.remove_widget(self.yard[xrng_n])
                    self.yard.pop(xrng_n)
                    self.nMarks = xrng_n


class SplashScreen(Widget):
    splash_texture = Image(source='a/splash.png').texture

    def __init__(self, w=width*screen_scf, h=height*screen_scf, splash_duration=4.0, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        self.height = h
        self.width = self.height * 2.17
        self.pos = - 0.5 * (self.width - w), 0.0
        self.opacity = 0.0
        anim = Animation(opacity=1.0, duration=splash_duration)
        anim.start(self)
        Clock.schedule_once(self.confirm_showed_splash, splash_duration)

    def confirm_showed_splash(self, dt):
        gs.showedSplash = True

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.height = h
        self.width = self.height * 2.17
        self.pos = - 0.5 * (self.width - w), 0.0

    def anim_out(self, w=width*screen_scf):
        anim = Animation(x=w/2.0, y=0, size=(0, 0), opacity=0, duration=0.5, t='in_back')
        anim.start(self)


class MyFace(Widget):
    face_scale = 0.0
    down_shift = 0.0
    face_size = NumericProperty(0.7)
    sz = NumericProperty(0)
    img_left = NumericProperty(0.0)
    img_bottom = NumericProperty(0.0)
    jersey_left = NumericProperty(0.0)
    jersey_right = NumericProperty(0.0)
    jersey_bottom = NumericProperty(0.0)
    jersey_texture = ObjectProperty(None)
    stool_left = NumericProperty(0.0)
    stool_bottom = NumericProperty(0.0)
    stool_width = NumericProperty(0.0)
    stool_height = NumericProperty(0.0)
    stool_angle = NumericProperty(0.0)
    rotate_center = ListProperty([0, 0])
    face_texture = ObjectProperty(None)
    stool_color = ListProperty([1, 1, 1, 1])
    line_list = ListProperty([0, 0])
    line_color = ListProperty([0, 0, 0])
    line_width = NumericProperty(1)
    shorts_texture0 = ObjectProperty(None)
    shorts_texture1 = ObjectProperty(None)
    shorts_angle0 = NumericProperty(0.0)
    shorts_angle1 = NumericProperty(0.0)
    stool_texture = ObjectProperty(Image(source='a/stool.png').texture)

    def __init__(self, **kwargs):
        super(MyFace, self).__init__()
        self.face_scale = kwargs['face_size']
        self.down_shift = kwargs['down_shift']
        self.face_texture = kwargs['face_texture']
        self.jersey_texture = kwargs['jersey_texture']
        self.shorts_texture0 = kwargs['shorts_texture0']
        self.shorts_texture1 = kwargs['shorts_texture1']
        self.stool_color = kwargs['stool_color']
        self.line_color = kwargs['line_color']
        self.opacity = 0.0

    def update(self, x, y, l, th, m2p, po, w, h, player):
        xp, yp = xy2p(x, y, m2p, po, w, h)
        self.sz = int(m2p * 0.7)
        self.face_size = float(self.face_scale * m2p)
        self.img_left = int(xp - self.face_size * 0.5)
        self.img_bottom = int(yp - self.down_shift * self.face_size)
        self.jersey_left = int(xp - self.sz * 0.3)
        self.jersey_bottom = int(yp - 1.0 * self.sz)
        self.jersey_right = int(xp + self.sz * 0.3)
        self.stool_width = int(2.8 * p.stool_radius[p.difficult_level] * m2p)
        self.stool_height = int(m2p)
        self.stool_left = int(xp - 0.5 * self.stool_width)
        self.stool_bottom = int(yp + (l - 0.9 - 0.5 * p.d) * m2p)
        self.stool_angle = float(th * 180.0 / pi)
        self.rotate_center = self.img_left + self.sz * 0.5, yp - 0.5 * p.d * m2p
        self.line_width = float(0.075 * m2p + 0.001)
        self.line_list = player
        self.shorts_angle0 = -atan2(player[4] - player[6], player[5] - player[7]) * 180.0 / pi
        self.shorts_angle1 = -atan2(player[4] - player[2], player[5] - player[3]) * 180.0 / pi

    def anim_in(self, w=Window.width, h=Window.height, duration=1.0):
        self.width = w
        self.height = h
        Animation.cancel_all(self)
        anim = Animation(opacity=1.0, duration=duration)
        anim.start(self)

    def anim_out(self, duration=1.0):
        Animation.cancel_all(self)
        anim = Animation(opacity=0.0, duration=duration)
        anim.start(self)

    def clear(self):
        self.opacity = 0.0


class VolleyNet(Widget):
    font_name = StringProperty('a/VeraMono.ttf')
    score = StringProperty('0 - 0')
    zero = NumericProperty(Window.width / 2.0)
    score_width = NumericProperty(Window.width / 10.0)
    score_height = NumericProperty(Window.height / 10.0)
    score_bottom = NumericProperty(0.9 * Window.height)
    back_line_pos = ListProperty([[0.0, 0.0], [0.0, 0.0]])
    back_line_size = ListProperty([[0.0, 0.0], [0.0, 0.0]])

    net_rect = Image(source='a/net_rect.png').texture
    net_circle = Image(source='a/net_circ.png').texture

    def __init__(self):
        super(VolleyNet, self).__init__()
        self.opacity = 0.0

    def update(self, m2p, po, w=Window.width, h=Window.height):
        x = - po + w / 2
        self.pos = (float(x - 0.5 * p.net_width * m2p), 0.05 * h)
        d = float(m2p * p.back_line)
        self.back_line_pos = [[0.0, 0.05 * h], [x + d, 0.05 * h]]
        self.back_line_size = [[x - d, 0.95 * h], [w - x - d, 0.95 * h]]
        self.size = (float(p.net_width * m2p), float((p.net_height + 0.5 * p.net_width) * m2p))
        self.score = str(stats.volley_score[0]) + ' - ' + str(stats.volley_score[1])

    def anim_in(self, duration=1.0):
        Animation.cancel_all(self)
        anim = Animation(opacity=1.0, duration=duration)
        anim.start(self)

    def anim_out(self, duration=1.0):
        Animation.cancel_all(self)
        anim = Animation(opacity=0.0, duration=duration)
        anim.start(self)

    def resize(self, w=Window.width, h=Window.height):
        self.zero = w / 2.0
        self.score_width = w / 10.0
        self.score_height = h / 10.0
        self.score_bottom = 0.9 * h


class ImpactBall(Widget):
    color = ListProperty([1.0, 1.0, 1.0, 1.0])
    angle = NumericProperty(0.0)
    star_texture = ObjectProperty(Image(source='a/bano.png').texture)
    star_scale = NumericProperty(2.0)
    texture = ObjectProperty(Image(source='a/cg_black_on_white.png').texture)

    def __init__(self, color=pink[isDark]):
        super(ImpactBall, self).__init__()
        self.color = color
        self.start_rotation()

    def start_rotation(self):
        anim = Animation(angle=360, duration=1.57)
        anim += Animation(angle=360, duration=1.57)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0


class Ball(Widget):
    img_left = NumericProperty(0.0)
    img_bottom = NumericProperty(0.0)
    sz = NumericProperty(1.0)
    random_add = [[random()-0.5 for _ in range(2)] for _ in range(p.num_future_points)]
    random_scale = NumericProperty(0.0)
    impact_x = NumericProperty(0.0)
    impact_y = NumericProperty(0.0)
    past_x = zeros(32)
    past_y = zeros(32)
    past_points = ListProperty(zeros(64))
    ball_texture = Image(source='a/ball.png').texture

    def __init__(self, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.opacity = 0.0
        self.future = []

        with self.canvas:
            Color(rgba=(red[isDark][0], red[isDark][1], red[isDark][2], 0.8))
            self.future = [Ellipse(size=(0, 0)) for _ in range(p.num_future_points)]
            self.impact = ImpactBall(color=(pink[isDark]))
            Color(rgba=(1, 1, 1, 1))
            self.now = Ellipse(size=(self.sz, self.sz), texture=self.ball_texture, pos=self.pos)

    def update(self, xb, yb, m2p, po, w, h, pause_flag):
        # Update the past position of the ball
        if not pause_flag:
            self.past_x = [xb] + self.past_x[:-1]
            self.past_y = [yb] + self.past_y[:-1]
        x, y = xy2p(self.past_x, self.past_y, m2p, po, w, h)
        self.past_points = intersperse(x, y)

        # Generate the current position of the ball
        x, y = xy2p(xb, yb, m2p, po, w, h)
        self.sz = int(2.0 * m2p * p.rb)
        self.img_left = int(x - m2p * p.rb)
        self.img_bottom = int(y - m2p * p.rb)
        self.now.pos = (self.img_left, self.img_bottom)
        self.now.size = (self.sz, self.sz)

        # Generate the impact position of the ball
        c = 0.15
        self.impact_x = float((1 - c) * self.impact_x + c * (gs.xI - p.rb))
        self.impact_y = float((1 - c) * self.impact_y + c * (gs.yI - p.rb))
        self.impact.color[3] = erf(gs.yI - 2.7)
        x, y = xy2p(self.impact_x, self.impact_y, m2p, po, w, h)
        self.impact.pos = int(x), int(y)
        self.impact.size = self.sz, self.sz
        self.impact.star_scale = float(1.0 + 3.0 * gs.timeUntilBounce)

        # Generate the future positions of the ball
        X, Y = xy2p(gs.traj['x'], gs.traj['y'], m2p, po, w, h)
        nf = float(p.num_future_points)
        for n in range(X.__len__()):
            sz = 0.5 * self.sz * (1.0 - n / nf)
            self.future[n].pos = (X[n] - 0.5 * sz + self.random_add[n][0] * self.random_scale * m2p,
                                  Y[n] - 0.5 * sz + self.random_add[n][1] * self.random_scale * m2p)
            self.future[n].size = (sz, sz)

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=1.0):
        self.width = w
        self.height = h
        self.random_add = [[random() - 0.5 for _ in range(2)] for _ in range(p.num_future_points)]
        self.random_scale = 0.0
        Animation.cancel_all(self)
        anim = Animation(opacity=1.0, duration=duration)
        anim.start(self)

    def anim_out(self):
        Animation.cancel_all(self)
        anim = Animation(opacity=0.0, duration=1)
        anim.start(self)


class BallCannon(Widget):
    texture = Image(source='a/ball_cannon.png').texture
    angle = NumericProperty(p.sa)
    color = ListProperty([1.0, 1.0, 1.0, 0.0])

    def __init__(self, **kwargs):
        super(BallCannon, self).__init__(**kwargs)
        self.opacity = 0.0

    def update(self, xb, yb, angle, speed, m2p, po, w=Window.width, h=Window.height):
        x, y = xy2p(xb, yb, m2p, po, w, h)

        self.size = float(6.0 * p.rb * m2p), float(3.0 * p.rb * m2p)
        self.pos = float(x - 1.5 * p.rb * m2p), float(y - 1.5 * p.rb * m2p)
        self.angle = 180.0 / pi * angle
        self.color[1] = float(1.0 - 0.384 * (speed - 10.0) / 10.0)
        self.color[2] = float(1.0 - 0.406 * (speed - 10.0) / 10.0)

    def anim_in(self, duration=1.0):
        Animation.cancel_all(self)
        anim = Animation(opacity=1.0, color=[1.0, 1.0, 1.0, 1.0], duration=duration)
        anim.start(self)

    def anim_out(self, duration=1.0):
        Animation.cancel_all(self)
        anim = Animation(opacity=0.0, color=[1.0, 1.0, 1.0, 0.0], duration=duration)
        anim.start(self)


# Returns the center_x, center_y, and diameter of the stick
def get_stick_pos(ch):
    return ch.pos[0]+ch.size[0]/2.0, ch.pos[1]+ch.size[1]/2.0, ch.size[0]


def touch_stick(loc, stick):
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
        self.size = int(self.norm_size[0] * w), int(self.norm_size[1] * h)
        self.pos = int(self.norm_pos[0] * w), int(self.norm_pos[1] * h)

        self.ctrl = [0, 0]

        # Start with it off screen
        self.out_position = out_position
        if self.out_position == 'left':
            self.pos[0] = -int(self.norm_size[0] * w)
        else:
            self.pos[0] = int(w)

        print('Instantiated a stick at pos = ' + str(self.pos) + ' and size = ' + str(self.size))

    def update_el(self, x, y):
        self.ctrl = [x, y]

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        if self.is_on_screen:
            self.pos[0] = int(self.norm_pos[0] * w)
        elif self.out_position == 'left':
            self.pos[0] = -int(self.norm_size[0] * w)
        else:
            self.pos[0] = w
        self.size = int(self.norm_size[0] * w), int(self.norm_size[1] * h)
        self.pos[1] = int(self.norm_pos[1] * h)
        print('Resized a stick to size = ' + str(self.size) + ' and pos = ' + str(self.pos))

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=0.25):
        in_x = int(self.norm_pos[0] * w)
        in_y = int(self.norm_pos[1] * h)
        Animation.cancel_all(self)
        anim = Animation(x=in_x, y=in_y, duration=duration, t='out_back')
        anim.start(self)
        self.is_on_screen = True
        print('Moved a stick (anim_in) to size = ' + str(self.size) + ' and pos = ' + str([in_x, in_y]))

    def anim_out(self, w=width*screen_scf, h=height*screen_scf):
        if self.out_position == 'left':
            out_x = -int(self.norm_size[0] * w)
        else:
            out_x = int(w)
        out_y = int(self.norm_pos[1] * h)
        Animation.cancel_all(self)
        anim = Animation(x=out_x, y=out_y, duration=0.25, t='in_back')
        anim.start(self)
        self.is_on_screen = False
        print('Moved a stick (anim_out) to size = ' + str(self.size) + ' and pos = ' + str([out_x, out_y]))


# Create OptionButtons class
class OptionButtons(Button):
    def_button_color = (1, 1, 1, 0.9)
    touched_button_color = (1, 1, 1, 0.6)
    button_color = ListProperty(def_button_color)
    shadow_color = ListProperty(blue[isDark])

    label_text = StringProperty('')
    label_font = StringProperty('a/airstrea.ttf')
    label_font_size = NumericProperty(0.0)
    label_color = ListProperty(red[isDark])
    out_position = StringProperty('')
    corner_radius = NumericProperty(0.015 * Window.width)
    shadow_width = NumericProperty(0.003 * Window.width)
    is_on_screen = False
    is_blinking = False
    is_high_score = False

    def __init__(self, label_text='', norm_pos=(0.0, 0.0), norm_size=(0.5, 0.1), norm_font_size=0.05,
                 w=Window.width, h=Window.height, out_position='top', color=red[isDark], **kwargs):
        super(OptionButtons, self).__init__()
        # Eliminate default backgrounds
        self.background_color = 1, 1, 1, 0
        self.background_normal = ''
        self.background_disabled_down = ''
        self.background_disabled_normal = ''
        self.background_down = ''

        # Position and size of the buttons
        self.norm_pos = norm_pos
        self.norm_size = norm_size
        self.pos = [norm_pos[0] * w, norm_pos[1] * h]
        self.size = [norm_size[0] * w, norm_size[1] * h]

        # Label properties
        self.label_text = label_text
        self.norm_font_size = norm_font_size
        self.label_font_size = norm_font_size * h
        self.label_color = color

        # Initialize with the button positioned outside
        self.out_position = out_position
        if self.out_position == 'top':
            self.pos[1] = h
        elif self.out_position == 'bottom':
            self.pos[1] = - self.size[1] - 2.0 * self.shadow_width
        elif self.out_position == 'left':
            self.pos[0] = - self.size[0] - 2.0 * self.shadow_width
        elif self.out_position == 'right':
            self.pos[0] = w

        # Set up visual properties of the rounded rectangles
        self.corner_radius = 0.015 * w
        self.shadow_width = 0.003 * w

    def resize(self, w=Window.width, h=Window.height):
        if self.is_high_score:
            self.size = [0.5 * self.norm_size[0] * w, 0.5 * self.norm_size[1] * h]
            self.label_font_size = 0.5 * self.norm_font_size * h
        else:
            self.size = [self.norm_size[0] * w, self.norm_size[1] * h]
            self.label_font_size = self.norm_font_size * h
        if self.is_on_screen and not self.is_high_score:
            self.pos = [self.norm_pos[0] * w, self.norm_pos[1] * h]
        elif self.is_on_screen and self.is_high_score:
            self.pos = (0.2 * w + 0.6 * self.norm_pos[0] * w, 0.8 * h)
        elif self.out_position == 'top':
            self.pos = [self.norm_pos[0] * w, h]
        elif self.out_position == 'bottom':
            self.pos = [self.norm_pos[0] * w, - self.size[1] - self.shadow_width]
        elif self.out_position == 'left':
            self.pos = [- self.size[0] - self.shadow_width, self.norm_pos[1] * h]
        elif self.out_position == 'right':
            self.pos = [w, self.norm_pos[1] * h]

        self.corner_radius = 0.015 * w
        self.shadow_width = 0.003 * w

    def detect_touch(self, loc):
        touch_conditions = [loc[0] > self.pos[0],
                            loc[0] < self.pos[0] + self.size[0],
                            loc[1] > self.pos[1],
                            loc[1] < self.pos[1] + self.size[1]]
        return all(touch_conditions)

    def background_touched(self, dt=0):
        anim = Animation(shadow_width=0.0, button_color=self.touched_button_color, duration=0.1) + \
               Animation(shadow_width=0.003 * Window.width, button_color=self.def_button_color, duration=0.1)
        anim.start(self)
        if SOUND_LOADED and p.fx_is_on:
            button_sound.play()

    def anim_in(self, w=Window.width, h=Window.height, duration=0.5):
        Animation.cancel_all(self)
        anim = Animation(x=self.norm_pos[0]*w, y=self.norm_pos[1]*h, size=(self.norm_size[0]*w, self.norm_size[1]*h),
                         duration=duration, t='out_back')
        anim.start(self)
        self.is_high_score = False
        self.is_on_screen = True

    def anim_in_to_high_score(self, w=Window.width, h=Window.height, duration=0.5):
        Animation.cancel_all(self)
        anim = Animation(x=0.2*w+0.6*self.norm_pos[0]*w, y=0.82*h,
                         size=(0.6*self.norm_size[0]*w, 0.5*self.norm_size[1]*h),
                         label_font_size=0.6*self.norm_font_size*h, duration=duration, t='out_back')
        anim.start(self)
        self.is_high_score = True
        self.is_on_screen = True

    def anim_out(self, w=Window.width, h=Window.height, duration=0.5):
        out_x = self.pos[0]
        out_y = self.pos[1]
        if self.out_position == 'left':
            out_x = - self.norm_size[0] * w - 2.0 * self.shadow_width
        elif self.out_position == 'right':
            out_x = w
        if self.out_position == 'bottom':
            out_y = - self.norm_size[1] * h - 2.0 * self.shadow_width
        elif self.out_position == 'top':
            out_y = h
        Animation.cancel_all(self)
        anim = Animation(x=out_x, y=out_y, size=(self.norm_size[0]*w, self.norm_size[1]*h),
                         label_font_size=self.norm_font_size*h, duration=duration, t='in_back')
        anim.start(self)
        self.is_high_score = False
        self.is_on_screen = False

    def anim_out_then_in(self, w=Window.width, h=Window.height, duration=10):
        out_x = self.pos[0]
        out_y = self.pos[1]
        if self.out_position == 'left':
            out_x = - self.norm_size[0] * w - 2.0 * self.shadow_width
        elif self.out_position == 'right':
            out_x = w
        if self.out_position == 'bottom':
            out_y = - self.norm_size[1] * h - 2.0 * self.shadow_width
        elif self.out_position == 'top':
            out_y = h
        Animation.cancel_all(self)
        anim_out = Animation(x=out_x, y=out_y, duration=0.5, t='in_back')
        anim_pause = Animation(x=out_x, y=out_y, duration=(duration-1), t='in_back')
        anim_in = Animation(x=self.norm_pos[0]*w, y=self.norm_pos[1]*h, duration=0.5, t='out_back')
        anim = anim_out + anim_pause + anim_in
        anim.start(self)
        self.is_on_screen = True

    def blink(self, duration=1):
        anim_red = Animation(button_color=(red[isDark][0], red[isDark][1], red[isDark][2], 0.4), duration=duration)
        anim_mid = Animation(button_color=self.def_button_color, duration=duration)
        anim_blue = Animation(button_color=(blue[isDark][0], blue[isDark][1], blue[isDark][2],  0.6), duration=duration)
        anim_def = Animation(button_color=self.def_button_color, duration=duration)
        anim = anim_red + anim_mid + anim_blue + anim_def
        anim.repeat = True
        anim.start(self)
        self.is_blinking = True
        print('  Blinking button')


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
        Animation.cancel_all(self)
        anim = Animation(x=in_x, y=in_y, duration=duration)
        anim.start(self)
        self.is_on_screen = True

    def anim_out(self, w=width*screen_scf, h=height*screen_scf, duration=0.1):
        out_x = self.norm_left * w
        out_y = h
        Animation.cancel_all(self)
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
    font_size_ratio = 0.0
    font_size = NumericProperty(0)
    label_color = ListProperty(red[isDark])
    outline_width = NumericProperty(2 * screen_scf)
    outline_color = ListProperty(gray_6[0][0:3])
    ratio_from_top = 0.68
    is_on_screen = False

    def __init__(self, outside_position='top', vertical_position=0, label_color=red[isDark], font_size_ratio=0.04,
                 label_text='Category', this_run='This Run', best_run='Best', is_high='Rank',
                 w=width*screen_scf, h=height*screen_scf, **kwargs):
        super(HighScoreLabel, self).__init__()
        # Outside position is a string, determining where the button goes when off-screen
        self.outside_position = outside_position

        # Vertical position is an integer, goes from top [0] to bottom [4] when on-screen
        self.vertical_position = vertical_position

        # Label text is the left column [distance, height, boing, or score]
        self.label_text = label_text

        # Left position of the widget when on-screen
        self.label_left = 0.01 * w

        # Current scores and the saved best score
        self.label_text = label_text
        self.this_run = this_run
        self.best_run = best_run
        self.is_high = is_high

        # Sizing
        self.width = 0.98 * w
        self.height = 0.1 * h
        self.font_size_ratio = font_size_ratio
        self.font_size = self.font_size_ratio * w
        self.label_color = label_color

        # Start with the widget off-screen
        if self.is_on_screen:
            self.pos = [self.label_left, (self.ratio_from_top - 0.12 * self.vertical_position) * h]
        else:
            if self.outside_position == 'left':
                self.pos[0] = -self.width
            elif self.outside_position == 'right':
                self.pos[0] = w
            if self.outside_position == 'bottom':
                self.pos[1] = -self.size[1] - self.font_size
            elif self.outside_position == 'top':
                self.pos[1] = h + self.font_size

    def anim_in(self, h=height*screen_scf, duration=1):
        in_x = self.label_left
        in_y = (self.ratio_from_top - 0.12 * self.vertical_position) * h
        Animation.cancel_all(self)
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
            out_y = - self.size[1] - self.font_size
        elif self.outside_position == 'top':
            out_y = h + self.font_size
        Animation.cancel_all(self)
        anim = Animation(x=out_x, y=out_y, duration=duration, t='in_elastic')
        anim.start(self)

    def resize(self, w=width*screen_scf, h=height*screen_scf):
        self.label_left = 0.01 * w
        self.width = 0.98 * w
        self.height = 0.1 * h
        self.font_size = self.font_size_ratio * w

        if self.is_on_screen:
            self.pos = [self.label_left, (self.ratio_from_top - 0.12 * self.vertical_position) * h]
        else:
            if self.outside_position == 'left':
                self.pos[0] = - self.width
            elif self.outside_position == 'right':
                self.pos[0] = w
            if self.outside_position == 'bottom':
                self.pos[1] = - self.size[1] - self.font_size
            elif self.outside_position == 'top':
                self.pos[1] = h + self.font_size


class RotatingRing(Image):
    angle = NumericProperty(0.0)
    center = ListProperty((0.0, 0.0))

    def __init__(self):
        super(RotatingRing, self).__init__()
        self.source = 'a/tutorial_ring.png'
        self.size = [0.0, 0.0]
        self.opacity = 1.0

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
    msg = ['Welcome to dRuBbLe!!!\nLets learn how 2 play',
           'Touch the stick\non the left to\nmove the stool',
           'Touch the stick\non the right to\nmove the player',
           'Use the action\nbutton to start\nthe game',
           'Tap once to set\nthe launch angle',
           'Tap again to set\nthe speed and\nlaunch the ball',
           'Run under the\nspinning ball',
           'Try to bounce\nthe ball off the\ntop of your stool',
           'Bounce as far\nand as high\nas possible',
           'Good Luck!!!',
           '']
    is_paused = False
    ball_is_paused = False
    ball_wait = False
    dyb_before = 0
    pause_state = gs.u

    # Text label properties
    label_text = StringProperty('')
    label_font_size = NumericProperty(0.0)
    label_pos = ListProperty([0.5 * Window.width, 0.4 * Window.height])
    label_size = ListProperty([0.0, 0.0])
    label_color = ListProperty(blue[isDark])
    label_outline_color = ListProperty(gray_6[isDark])
    label_outline_width = 3.0 * screen_scf
    label_opacity = NumericProperty(0.0)
    label_font_name = StringProperty('a/Airstream.ttf')

    def __init__(self, w=Window.width, h=Window.height, **kwargs):
        super(Tutorial, self).__init__()
        self.n = 0
        self.width = w
        self.height = h
        self.pos = (0, 0)
        self.opacity = 0.0

        # Text Label Properties
        self.label_text = ''
        self.label_font_size = 0.0
        self.label_pos = [0.5 * w, 0.4 * h]
        self.label_size = [0.0, 0.0]
        self.label_opacity = 0.0

        # Create the ring widget
        with self.canvas:
            self.ring = RotatingRing()
            self.add_widget(self.ring)
            self.ring.start_rotation()

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

    def change_message(self, dt):
        print('Tutorial Change Message to : \n' + self.msg[self.n] + '\n')
        self.label_text = self.msg[self.n]

    def set_pause_false(self, dt):
        self.is_paused = False

    def set_wait_false(self, dt):
        self.ball_wait = False

    def pause(self, dt):
        self.is_paused = True
        Clock.schedule_once(self.set_pause_false, dt)

    def new_ring_position(self, ring_size=(0, 0), ring_pos=(0, 0), in_duration=0.0, out_duration=0.0):
        anim_ring_out = Animation(opacity=0.0, duration=out_duration)
        anim_ring_pos = Animation(size=ring_size, pos=ring_pos,
                                  center=(ring_pos[0]+0.5*ring_size[0], ring_pos[1]+0.5*ring_size[1]),
                                  opacity=0.0, duration=0)
        anim_ring_in = Animation(opacity=1.0, duration=in_duration)
        anim = anim_ring_out + anim_ring_pos + anim_ring_in
        anim.start(self.ring)

    def clear_ring(self, out_duration=1.0):
        anim_ring_out = Animation(opacity=0.0, duration=out_duration)
        anim_ring_out.start(self.ring)

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
        self.label_pos = [0.2 * w, 0.4 * h]
        self.label_size = [0.6 * w, 0.3 * h]

        # Resize the ring
        self.ring.size = (self.ring.size[0] * width_scale, self.ring.size[1] * height_scale)
        self.ring.pos = (self.ring.pos[0] * width_scale, self.ring.pos[1] * height_scale)
        self.ring.center = (self.ring.pos[0] + 0.5 * self.ring.size[0], self.ring.pos[1] + 0.5 * self.ring.size[1])

    def update(self, app_object):
        if self.is_paused:
            return

        self.dyb_before = gs.dyb
        was_touched = False
        in_range = abs(gs.xp[0] - gs.xI) < p.rb
        w = self.width
        h = self.height

        if self.n == 0:
            # Welcome
            was_touched = True
            app_object.tilt_stick.anim_in(w=self.width, h=self.height, duration=1)
            ring_size = (1.5 * app_object.tilt_stick.size[0], 1.5 * app_object.tilt_stick.size[1])
            ring_pos = (app_object.tilt_stick.norm_pos[0] * w - 0.167 * ring_size[0],
                        app_object.tilt_stick.norm_pos[1] * h - 0.167 * ring_size[1])
            print('Surrounded the move stick with a rotating ring_size = ', ring_size, '  ring_pos = ', ring_pos)
            self.new_ring_position(ring_size=ring_size, ring_pos=ring_pos, in_duration=2.0, out_duration=0.0)
        elif self.n == 1 and norm(gs.ctrl[2:4]) > 0.3:
            # Touch left
            was_touched = True
            app_object.move_stick.anim_in(w=self.width, h=self.height, duration=1)
            ring_size = (1.5 * app_object.move_stick.size[0], 1.5 * app_object.move_stick.size[1])
            ring_pos = (app_object.move_stick.norm_pos[0] * w - 0.167 * ring_size[0],
                        app_object.move_stick.norm_pos[1] * h - 0.167 * ring_size[1])
            print('Surrounded the tilt stick with a rotating ring_size = ', ring_size, '  ring_pos = ', ring_pos)
            self.new_ring_position(ring_size=ring_size, ring_pos=ring_pos, in_duration=2.0, out_duration=2.0)
        elif self.n == 2 and norm(gs.ctrl[:1]) > 0.3:
            # Touch right
            was_touched = True
            app_object.action_butt.anim_in(w=self.width, h=self.height)
            ring_size = (1.5 * app_object.action_butt.size[0], 1.5 * app_object.action_butt.size[0])
            butt_center_y = app_object.action_butt.norm_pos[1] * h + 0.5 * app_object.action_butt.size[1]
            ring_pos = (app_object.action_butt.norm_pos[0] * w - 0.167 * ring_size[0],
                        butt_center_y - 0.5 * ring_size[1])
            print('Surrounded the action button with a rotating ring_size = ', ring_size, '  ring_pos = ', ring_pos)
            self.new_ring_position(ring_size=ring_size, ring_pos=ring_pos, in_duration=2.0, out_duration=2.0)
        elif self.n == 3 and gs.game_mode >= 4:
            # Touch action
            was_touched = True
        elif self.n == 4 and gs.game_mode >= 5:
            # Touch angle
            was_touched = True
        elif self.n == 5 and gs.game_mode >= 6:
            # Touch speed
            was_touched = True
            self.clear_ring(out_duration=1.0)
        elif self.n in (6, 7, 8) and in_range:
            # (6) Run to ball, (7) Try to bounce, (8) Bounce as far
            was_touched = True
            self.ball_is_paused = False
            self.ball_wait = True
            # Clock.schedule_once(self.set_wait_false, 0.9)
        elif self.n == 9 and in_range:
            # Good luck
            was_touched = True
            self.ball_is_paused = False
            if not app_object.option_butt.is_on_screen:
                app_object.option_butt.anim_in(w=self.width, h=self.height)

        # Switch to the next message if there was a touch
        next_pause_duration = 3.0 if self.n < 8 else 5.0
        if was_touched:
            self.pause(next_pause_duration)
            self.n += 1
            Clock.schedule_once(self.change_message, 2)
            self.switch(w=app_object.width, h=app_object.height, duration=next_pause_duration)

        # Remove widgets if reached end of tutorial
        if self.n >= len(self.msg):
            self.clear_ring()
            self.anim_out()
            Clock.schedule_once(app_object.remove_tutorial_callback, 1.0)
            app_object.tutorial_mode = False
        return

    def anim_in(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        Animation.cancel_all(self)
        anim = Animation(label_size=(0.6*w, 0.3*h), label_pos=(0.2*w, 0.4*h), opacity=1.0, label_opacity=1.0,
                         label_font_size=0.05*w, duration=duration, t='out_elastic')
        anim.start(self)

    def anim_out(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        Animation.cancel_all(self)
        anim = Animation(label_size=(0.6*w, 0.3*h), label_pos=(0.2*w, 0.4*h), opacity=0.0, label_opacity=0.0,
                         label_font_size=0.0*w, duration=0.33*duration, t='out_elastic')
        anim.start(self)

    def switch(self, w=width*screen_scf, h=height*screen_scf, duration=1):
        Animation.cancel_all(self)
        anim_out = Animation(label_size=(0, 0), label_pos=(0.5*w, 0.5*h), label_opacity=0.0,
                             label_font_size=0.0, duration=0.25*duration, t='in_elastic')
        anim_pause = Animation(duration=0.5*duration)
        anim_in = Animation(label_size=(0.6*w, 0.3*h), label_pos=(0.2*w, 0.4*h), label_opacity=1.0,
                            label_font_size=0.05*w, duration=0.25*duration, t='out_elastic')
        anim = anim_out + anim_pause + anim_in
        anim.start(self)


class DrubbleGame(Widget):
    tutorial_mode = False
    adSwitchSuccessful = False
    volley_score_on_screen = False

    def __init__(self, **kwargs):
        super(DrubbleGame, self).__init__(**kwargs)
        self.bind(size=self.resize_canvas)
        if platform in ('linux', 'windows', 'win', 'macosx'):
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self._keyboard.bind(on_key_up=self._on_keyboard_up)
        # Window.bind(on_joy_hat=self.on_joy_hat)
        # Window.bind(on_joy_ball=self.on_joy_ball)
        Window.bind(on_joy_axis=self.on_joy_axis)
        # Window.bind(on_joy_button_up=self.on_joy_button_up)
        Window.bind(on_joy_button_down=self.on_joy_button_down)

        with self.canvas:
            # Splash screen, init right away
            self.splash = SplashScreen(w=width*screen_scf, h=height*screen_scf)
            self.add_widget(self.splash)

            # Initialize the background
            self.bg = MyBackground()

            # Initialize the tutorial
            self.tutorial = Tutorial()

            # Initialize the volleyball net
            self.net = VolleyNet()

            # Initialize the ball
            self.ball = Ball()
            self.ball_cannon = BallCannon()

            # Initialize the sticks
            self.move_stick = Stick(norm_size=(0.3, 0.5), norm_pos=(0.69, 0.34), out_position='right')
            self.tilt_stick = Stick(norm_size=(0.3, 0.5), norm_pos=(0.01, 0.34), out_position='left')

            # Initialize the score line
            self.time_label = ScoreLabel(text='Time', norm_left=0.0)
            self.dist_label = ScoreLabel(text='Distance', norm_left=0.2)
            self.high_label = ScoreLabel(text='Height', norm_left=0.4)
            self.boing_label = ScoreLabel(text='Boing!', norm_left=0.6)
            self.score_label = ScoreLabel(text='Score', norm_left=0.8)

            # Initialize the player faces
            self.rand_player = randint(1, len(p.player_data)-1)
            self.rand_player = 1  # for debugging
            self.player_dicts = [p.players[0], p.players[self.rand_player]]
            self.player = [MyFace(**p.players[0]), MyFace(**p.players[self.rand_player])]

            # Initialize the high score labels
            j = p.difficult_level
            k = p.num_player - 1
            self.high_score_header = HighScoreLabel(label_color=blue[isDark], font_size_ratio=0.05)
            self.high_dist_label = HighScoreLabel(outside_position='left', vertical_position=1,
                                                  label_text='Distance', this_run='%0.1f' % stats.stool_dist,
                                                  best_run='%0.1f' % stats.high_stool_dist[j][k])
            self.high_height_label = HighScoreLabel(outside_position='right', vertical_position=2,
                                                    label_text='Height', this_run='%0.2f' % stats.max_height,
                                                    best_run='%0.2f' % stats.high_height[j][k])
            self.high_boing_label = HighScoreLabel(outside_position='left', vertical_position=3,
                                                   label_text='Boing!', this_run='%0.0f' % stats.stool_count,
                                                   best_run='%0.0f' % stats.high_stool_count[j][k])
            self.high_score_label = HighScoreLabel(outside_position='right', vertical_position=4,
                                                   label_text='Score', this_run='%0.0f' % stats.score,
                                                   best_run='%0.0f' % stats.high_score[j][k])

            self.volley_win_label = Label(color=blue[isDark], outline_color=(white[0], white[1], white[2]),
                                          outline_width=0.0, halign='center', valign='center')
            self.volley_record_label = Label(color=red[isDark], outline_color=(white[0], white[1], white[2]),
                                             outline_width=0.0, halign='center', valign='center')

            # Initialize the option and action buttons
            self.single_drubble_butt = OptionButtons(label_text='Single dRuBbLe', norm_size=(0.55, 0.2),
                                                     out_position='left', norm_pos=(0.05, 0.7), norm_font_size=0.12)
            self.double_drubble_butt = OptionButtons(label_text='Double dRuBbLe', norm_size=(0.55, 0.2),
                                                     out_position='right', norm_pos=(0.05, 0.4), norm_font_size=0.12)
            self.volley_drubble_butt = OptionButtons(label_text='Volley dRuBbLe', norm_size=(0.55, 0.2),
                                                     out_position='left', norm_pos=(0.05, 0.1), norm_font_size=0.12)
            self.tutorial_butt = OptionButtons(label_text='How 2\nPlay', norm_size=(0.3, 0.2), out_position='left',
                                               norm_pos=(0.65, 0.7),  norm_font_size=0.08)
            difficult_text = 'Difficulty\n-- ' + p.difficult_text[p.difficult_level] + ' --'
            self.difficult_butt = OptionButtons(label_text=difficult_text, norm_size=(0.3, 0.2), out_position='right',
                                                norm_pos=(0.65, 0.4), norm_font_size=0.08)
            self.fx_butt = OptionButtons(label_text='FX\nOn', norm_size=(0.14, 0.2), norm_pos=(0.65, 0.1),
                                         out_position='left', norm_font_size=0.08)
            self.music_butt = OptionButtons(label_text='Music\nOn', norm_size=(0.14, 0.2), norm_pos=(0.81, 0.1),
                                            out_position='left', norm_font_size=0.08)
            self.option_butt = OptionButtons(label_text='Options', norm_size=(0.19, 0.09), out_position='left',
                                             norm_pos=(0.01, 0.85), norm_font_size=0.06)
            self.action_butt = OptionButtons(label_text=p.actionMSG[3], norm_size=(0.19, 0.09), out_position='right',
                                             norm_pos=(0.8, 0.85), norm_font_size=0.06)

            # Create the button bindings
            # self.fx_butt.bind(on_press=self.fx_button_press)

            # Initialize  ads
            if platform == 'android':
                if USE_TEST_IDS:
                    self.ads = KivMob(TestIds.APP)
                    self.ads.new_interstitial(TestIds.INTERSTITIAL)
                    self.ads.new_banner(TestIds.BANNER, top_pos=False)
                else:
                    self.ads = KivMob('ca-app-pub-4007502882739240~4287725061')
                    self.ads.new_interstitial('ca-app-pub-4007502882739240/3261013033')
                    self.ads.new_banner('ca-app-pub-4007502882739240/2325289594', top_pos=False)
                self.ads.request_banner()
            elif platform == 'ios' and not self.adSwitchSuccessful:
                try:
                    self.banner_ad = autoclass('adSwitch').alloc().init()
                    self.adSwitchSuccessful = True
                    print('loaded adSwitch')
                except:
                    print('adSwitch did not load')

    def remove_splash(self, dt):
        self.remove_widget(self.splash)

    def add_game_widgets(self, dt):
        print('Adding game widgets')
        # Background
        self.add_widget(self.bg)
        self.bg.anim_in(w=self.width, h=self.height, duration=0.25)

        # Volleyball net
        if p.volley_mode:
            self.add_widget(self.net)
            self.net.anim_in(duration=0.35)

        # Ball
        self.add_widget(self.ball)
        self.ball.anim_in(w=self.width, h=self.height, duration=0.5)
        if p.num_player is 1 or p.volley_mode:
            self.ball.impact.color = pink[isDark]
        else:
            self.ball.impact.color = self.player[gs.active_player].line_color
        self.add_widget(self.ball_cannon)
        self.ball_cannon.anim_in(duration=0.5)

        # Players
        self.add_widget(self.player[0])
        self.add_widget(self.player[1])
        self.player[0].anim_in(w=self.width, h=self.height, duration=0.75)
        if p.num_player > 1:
            self.player[1].anim_in(w=self.width, h=self.height, duration=0.75)

        # Sticks and buttons
        self.add_widget(self.move_stick)
        self.add_widget(self.tilt_stick)
        self.add_widget(self.option_butt)
        self.add_widget(self.action_butt)

        if self.tutorial_mode:
            self.add_widget(self.tutorial)
            self.tutorial.anim_in(w=self.width, h=self.height, duration=1.0)
        else:
            # Option and action buttons
            self.option_butt.anim_in(w=self.width, h=self.height, duration=1.5)
            self.action_butt.anim_in(w=self.width, h=self.height, duration=1.5)

            # Sticks
            self.move_stick.anim_in(w=self.width, h=self.height, duration=1.25)
            self.tilt_stick.anim_in(w=self.width, h=self.height, duration=1.25)

        # Score labels
        if not p.volley_mode:
            self.add_widget(self.time_label)
            self.add_widget(self.dist_label)
            self.add_widget(self.high_label)
            self.add_widget(self.boing_label)
            self.add_widget(self.score_label)
            self.time_label.anim_in(w=self.width, h=self.height, duration=0.1)
            self.dist_label.anim_in(w=self.width, h=self.height, duration=0.2)
            self.high_label.anim_in(w=self.width, h=self.height, duration=0.3)
            self.boing_label.anim_in(w=self.width, h=self.height, duration=0.4)
            self.score_label.anim_in(w=self.width, h=self.height, duration=0.5)

        self.resize_canvas()
        print('  --> Done!')

    def remove_game_widgets(self):
        print('Removing game widgets')
        self.bg.anim_out()
        # Volleyball net
        if p.volley_mode:
            self.net.anim_out(duration=0.2)
        self.ball.anim_out()
        self.ball_cannon.anim_out()
        self.move_stick.anim_out(w=self.width, h=self.height)
        self.tilt_stick.anim_out(w=self.width, h=self.height)
        self.player[0].anim_out()
        self.player[1].anim_out()
        if not p.volley_mode:
            self.time_label.anim_out(w=self.width, h=self.height, duration=0.15)
            self.dist_label.anim_out(w=self.width, h=self.height, duration=0.30)
            self.high_label.anim_out(w=self.width, h=self.height, duration=0.45)
            self.boing_label.anim_out(w=self.width, h=self.height, duration=0.60)
            self.score_label.anim_out(w=self.width, h=self.height, duration=0.75)

        self.option_butt.anim_out(w=self.width, h=self.height)
        self.action_butt.anim_out(w=self.width, h=self.height)

        Clock.schedule_once(self.remove_game_widgets_callback, 1.0)

    def remove_game_widgets_callback(self, dt):
        # Create the callback so that there is a delay to allow the
        # animations to complete before removing the widgets.
        self.remove_widget(self.bg)
        self.remove_widget(self.ball)
        self.remove_widget(self.ball_cannon)
        # Volleyball net
        if p.volley_mode:
            self.remove_widget(self.net)
            p.volley_mode = False

        self.remove_widget(self.player[0])
        self.remove_widget(self.player[1])
        self.remove_widget(self.move_stick)
        self.remove_widget(self.tilt_stick)
        self.remove_widget(self.option_butt)
        self.remove_widget(self.action_butt)
        if not p.volley_mode:
            self.remove_widget(self.time_label)
            self.remove_widget(self.dist_label)
            self.remove_widget(self.high_label)
            self.remove_widget(self.boing_label)
            self.remove_widget(self.score_label)
        print('  --> Done!')

    def add_option_buttons(self, dt):
        print('Adding option buttons')
        # Add option screen buttons
        self.add_widget(self.single_drubble_butt)
        self.add_widget(self.double_drubble_butt)
        self.add_widget(self.volley_drubble_butt)
        self.add_widget(self.tutorial_butt)
        self.add_widget(self.difficult_butt)
        self.add_widget(self.fx_butt)
        self.add_widget(self.music_butt)
        self.single_drubble_butt.anim_in(w=self.width, h=self.height)
        self.double_drubble_butt.anim_in(w=self.width, h=self.height)
        self.volley_drubble_butt.anim_in(w=self.width, h=self.height)
        self.tutorial_butt.anim_in(w=self.width, h=self.height)
        self.difficult_butt.anim_in(w=self.width, h=self.height)
        self.fx_butt.anim_in(w=self.width, h=self.height)
        self.music_butt.anim_in(w=self.width, h=self.height)
        print('  --> Done!')

    def remove_option_buttons(self):
        print('Removing option buttons')
        # Add option screen buttons
        self.single_drubble_butt.anim_out(w=self.width, h=self.height)
        self.double_drubble_butt.anim_out(w=self.width, h=self.height)
        self.volley_drubble_butt.anim_out(w=self.width, h=self.height)
        self.tutorial_butt.anim_out(w=self.width, h=self.height)
        self.difficult_butt.anim_out(w=self.width, h=self.height)
        self.fx_butt.anim_out(w=self.width, h=self.height)
        self.music_butt.anim_out(w=self.width, h=self.height)
        Clock.schedule_once(self.remove_option_buttons_callback, 1.0)

    def remove_option_buttons_callback(self, dt):
        self.remove_widget(self.single_drubble_butt)
        self.remove_widget(self.double_drubble_butt)
        self.remove_widget(self.volley_drubble_butt)
        self.remove_widget(self.tutorial_butt)
        self.remove_widget(self.difficult_butt)
        self.remove_widget(self.fx_butt)
        self.remove_widget(self.music_butt)
        print('  --> Done!')

    def add_high_scores(self):
        print('Adding High Scores')
        # Indices for the high scores
        j = p.difficult_level
        k = p.num_player - 1

        # Bring the difficulty widget on screen
        self.add_widget(self.difficult_butt)
        self.difficult_butt.anim_in_to_high_score(w=self.width, h=self.height, duration=0.5)

        if p.volley_mode:
            # Bring the volley drubble widget on screen
            self.add_widget(self.volley_drubble_butt)
            self.volley_drubble_butt.anim_in_to_high_score(w=self.width, h=self.height, duration=0.5)

            # Update the high scores
            stats.update_high()

            # Write a win or lose message dependent on whether the player or opponent score is higher
            if stats.volley_score[0] > stats.volley_score[1]:
                win_msg = 'You win  ' + str(stats.volley_score[0]) + ' - ' + str(stats.volley_score[1])
                record_msg = 'Winning streak is  ' + str(stats.streak[j])
            elif stats.volley_score[1] > stats.volley_score[0]:
                win_msg = 'You lose  ' + str(stats.volley_score[1]) + ' - ' + str(stats.volley_score[0])
                record_msg = 'Losing streak is ' + str(-stats.streak[j])
            record = stats.volley_record[j]
            record_msg += '\nAll time record is  ' + str(record[0]) + ' - ' + str(record[1])
            print(win_msg)
            print(record_msg)

            # Update the parameters of the text that displays
            self.volley_win_label.text = win_msg
            self.volley_win_label.pos = 0.5 * self.width, 0.5 * self.height
            self.volley_win_label.size = 0.0, 0.0
            self.volley_win_label.font_size = 0
            self.volley_record_label.text = record_msg
            self.volley_record_label.pos = 0.5 * self.width, 0.5 * self.height
            self.volley_record_label.size = 0.0, 0.0
            self.volley_record_label.font_size = 0

            # Add the widget, and animate it onto the screen
            self.add_widget(self.volley_win_label)
            anim = Animation(pos=(0.2*self.width, 0.55*self.height), size=(0.6*self.width, 0.2*self.height),
                             font_size=0.13*self.height, duration=0.5, outline_width=0.005*self.height, t='out_back')
            anim.start(self.volley_win_label)
            self.add_widget(self.volley_record_label)
            anim = Animation(pos=(0.2 * self.width, 0.3 * self.height), size=(0.6 * self.width, 0.3 * self.height),
                             font_size=0.1 * self.height, duration=0.5, outline_width=0.005*self.height, t='out_back')
            anim.start(self.volley_record_label)

            self.volley_score_on_screen = True
        else:
            # Update the strings for the current scores
            self.high_dist_label.this_run = '%0.1f' % stats.stool_dist
            self.high_height_label.this_run = '%0.2f' % stats.max_height
            self.high_boing_label.this_run = '%0.0f' % stats.stool_count
            self.high_score_label.this_run = '%0.0f' % stats.score

            # Calculate percentiles
            pct_dist_str = return_percentile(stats.all_stool_dist[j][k], stats.stool_dist)
            pct_height_str = return_percentile(stats.all_height[j][k], stats.max_height)
            pct_boing_str = return_percentile(stats.all_stool_count[j][k], stats.stool_count)
            pct_score_str = return_percentile(stats.all_score[j][k], stats.score)

            # Include either a percentile, or new high string
            hstr = 'New High!'
            self.high_dist_label.is_high = hstr if stats.stool_dist > stats.high_stool_dist[j][k] else pct_dist_str
            self.high_height_label.is_high = hstr if stats.max_height > stats.high_height[j][k] else pct_height_str
            self.high_boing_label.is_high = hstr if stats.stool_count>stats.high_stool_count[j][k] else pct_boing_str
            self.high_score_label.is_high = hstr if stats.score > stats.high_score[j][k] else pct_score_str

            # Update the strings for the high scores
            self.high_dist_label.best_run = '%0.1f' % stats.high_stool_dist[j][k]
            self.high_height_label.best_run = '%0.2f' % stats.high_height[j][k]
            self.high_boing_label.best_run = '%0.0f' % stats.high_stool_count[j][k]
            self.high_score_label.best_run = '%0.0f' % stats.high_score[j][k]

            # Bring the high scores onto the screen
            if p.num_player == 1:
                self.add_widget(self.single_drubble_butt)
                self.single_drubble_butt.anim_in_to_high_score(w=self.width, h=self.height, duration=0.5)
            elif p.num_player == 2:
                self.add_widget(self.double_drubble_butt)
                self.double_drubble_butt.anim_in_to_high_score(w=self.width, h=self.height, duration=0.5)
            self.add_widget(self.high_score_header)
            self.add_widget(self.high_dist_label)
            self.add_widget(self.high_height_label)
            self.add_widget(self.high_boing_label)
            self.add_widget(self.high_score_label)
            self.high_score_header.anim_in(h=self.height, duration=1.0)
            self.high_dist_label.anim_in(h=self.height, duration=1.5)
            self.high_height_label.anim_in(h=self.height, duration=2.0)
            self.high_boing_label.anim_in(h=self.height, duration=2.5)
            self.high_score_label.anim_in(h=self.height, duration=3.0)

            # Update the high scores
            stats.update_high()

        # Add a banner ad
        if platform == 'ios':
            self.show_banner()
        elif platform == 'android':
            self.ads.show_banner()

        print('  --> Done!')

    def remove_high_scores(self, duration=1):
        print('Removing High Scores')

        # Remove the difficulty button
        self.difficult_butt.anim_out(w=self.width, h=self.height, duration=duration)

        if self.volley_score_on_screen:
            anim = Animation(x=0.5*self.width, size=(0, 0), font_size=0, outline_width=0, t='in_back', duration=0.5)
            anim.start(self.volley_win_label)
            anim.start(self.volley_record_label)
            self.volley_drubble_butt.anim_out(w=self.width, h=self.height, duration=duration)
        else:
            # Take the high scores off the screen
            if p.num_player == 1:
                self.single_drubble_butt.anim_out(w=self.width, h=self.height, duration=duration)
            elif p.num_player == 2:
                self.double_drubble_butt.anim_out(w=self.width, h=self.height, duration=duration)
            self.high_score_header.anim_out(w=self.width, h=self.height, duration=duration)
            self.high_dist_label.anim_out(w=self.width, h=self.height, duration=duration)
            self.high_height_label.anim_out(w=self.width, h=self.height, duration=duration)
            self.high_boing_label.anim_out(w=self.width, h=self.height, duration=duration)
            self.high_score_label.anim_out(w=self.width, h=self.height, duration=duration)

        Clock.schedule_once(self.remove_high_scores_callback, 1.0)

        # Remove the banner ad
        if platform == 'ios' and self.adSwitchSuccessful:
            self.hide_banner()
        elif platform == 'android':
            self.ads.hide_banner()
            self.ads.request_banner()

    def remove_high_scores_callback(self, dt):
        self.remove_widget(self.difficult_butt)
        if self.volley_score_on_screen:
            print('Removing volley score widget')
            self.volley_win_label.text = ''
            self.remove_widget(self.volley_win_label)
            self.volley_record_label.text = ''
            self.remove_widget(self.volley_record_label)
            self.remove_widget(self.volley_drubble_butt)
            self.volley_score_on_screen = False
        else:
            if p.num_player == 1:
                self.remove_widget(self.single_drubble_butt)
            elif p.num_player == 2:
                self.remove_widget(self.double_drubble_butt)
            self.remove_widget(self.high_score_header)
            self.remove_widget(self.high_dist_label)
            self.remove_widget(self.high_height_label)
            self.remove_widget(self.high_boing_label)
            self.remove_widget(self.high_score_label)
        print('  --> Done!')

    # Controls
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.keyPush = ctrl2keyPush(gs)
        gs.set_control(keyPush=kvUpdateKey(self.keyPush, keycode, 1))
        if gs.game_mode == 1 and gs.showedSplash:
            cycle_modes(gs, stats, engine)
            self.splash.anim_out(w=self.width)
            Clock.schedule_once(self.remove_splash, 1.0)
            Clock.schedule_once(self.add_option_buttons, 1.0)
        elif gs.game_mode == 2 and keycode[1] == 'spacebar':
            self.single_drubble_button_press()
        elif gs.game_mode > 2 and keycode[1] == 'spacebar':
            self.action_button_press()
        elif gs.game_mode > 2 and keycode[1] == 'escape':
            self.option_button_press()
        return True
    
    def _on_keyboard_up(self, keyboard, keycode):
        self.keyPush = ctrl2keyPush(gs)
        gs.set_control(keyPush=kvUpdateKey(self.keyPush, keycode, 0))
        return True
    
    def on_touch_down(self, touch):
        loc = (touch.x, touch.y)
        if gs.game_mode == 1 and gs.showedSplash:
            cycle_modes(gs, stats, engine)
            self.splash.anim_out(w=self.width)
            Clock.schedule_once(self.remove_splash, 1.0)
            Clock.schedule_once(self.add_option_buttons, 1.0)
        elif gs.game_mode == 2 and self.single_drubble_butt.detect_touch(loc):
            self.single_drubble_button_press()
        elif gs.game_mode == 2 and self.double_drubble_butt.detect_touch(loc):
            self.double_drubble_button_press()
        elif gs.game_mode == 2 and self.volley_drubble_butt.detect_touch(loc):
            self.volley_drubble_button_press()
        elif gs.game_mode == 2 and self.tutorial_butt.detect_touch(loc):
            self.tutorial_button_press()
        elif gs.game_mode == 2 and self.difficult_butt.detect_touch(loc):
            self.difficult_button_press()
        elif gs.game_mode == 2 and self.fx_butt.detect_touch(loc):
            self.fx_button_press()
        elif gs.game_mode == 2 and self.music_butt.detect_touch(loc):
            self.music_button_press()
        elif gs.game_mode > 2:
            # Cycle through modes if touched the action or option_butt
            if self.action_butt.detect_touch(loc) and not self.tutorial.is_paused:
                self.action_button_press()
            if self.option_butt.detect_touch(loc):
                self.option_button_press()

            # Detect control inputs
            xy = touch_stick(loc, self.move_stick)
            if xy[0] != 0:
                self.move_stick.id_code = touch.id
                self.move_stick.update_el(xy[0], xy[1])
                gs.ctrl[0:2] = xy
            
            xy = touch_stick(loc, self.tilt_stick)
            if xy[0] != 0:
                self.tilt_stick.id_code = touch.id
                self.tilt_stick.update_el(xy[0], xy[1])
                gs.ctrl[2:4] = [xy[1], -xy[0]]

    def on_touch_move(self, touch):
        if gs.game_mode > 2:
            # Detect control inputs
            xy = touch_stick((touch.x, touch.y), self.move_stick)
            if touch.id == self.move_stick.id_code and xy[0] != 0:
                self.move_stick.update_el(xy[0], xy[1])
                gs.ctrl[0:2] = xy

            xy = touch_stick((touch.x, touch.y),self.tilt_stick)
            if touch.id == self.tilt_stick.id_code and xy[0] != 0:
                self.tilt_stick.update_el(xy[0], xy[1])
                gs.ctrl[2:4] = [xy[1], -xy[0]]

    def on_touch_up(self, touch):
        if gs.game_mode > 2:
            if touch.id == self.move_stick.id_code:
                self.move_stick.update_el(0, 0)
                gs.ctrl[0:2] = [0, 0]
                
            if touch.id == self.tilt_stick.id_code:
                self.tilt_stick.update_el(0, 0)
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
        p.num_player = 1
        cycle_modes(gs, stats, engine)

        # Add the in-game widgets
        Clock.schedule_once(self.add_game_widgets, 1.0)
        self.remove_option_buttons()

        # Turn the button blue momentarily
        self.single_drubble_butt.background_touched()

    # What to do when the double drubble button is pressed
    def double_drubble_button_press(self):
        # Specify this will be the two player version, and start game
        p.num_player = 2
        cycle_modes(gs, stats, engine)

        # Add the in-game widgets
        Clock.schedule_once(self.add_game_widgets, 1.0)
        self.remove_option_buttons()

        # Turn the button blue momentarily
        self.double_drubble_butt.background_touched()

    # What to do when the volley drubble button is pressed
    def volley_drubble_button_press(self):
        # Specify this will be the two player version, and start game
        p.num_player = 2
        p.volley_mode = True
        cycle_modes(gs, stats, engine)

        # Add the in-game widgets
        Clock.schedule_once(self.add_game_widgets, 1.0)
        self.remove_option_buttons()

        # Turn the button blue momentarily
        self.volley_drubble_butt.background_touched()

    # What to do when option button is pressed
    def option_button_press(self):
        # Return to the option screen, removing the in-game widgets
        gs.game_mode = 1
        self.remove_game_widgets()
        self.remove_high_scores()
        Clock.schedule_once(self.add_option_buttons, 1.0)

        # Reset game states and scores
        cycle_modes(gs, stats, engine)
        self.action_butt.label_text = p.actionMSG[3]

        # Turn the button blue momentarily
        self.option_butt.background_touched()

        if self.tutorial_mode:
            print('Removing the tutorial')
            self.tutorial.anim_out(w=self.width, h=self.height, duration=1.0)
            Clock.schedule_once(self.remove_tutorial_callback, 1.0)
            self.tutorial_mode = False

    # What to do when action button is pressed
    def action_button_press(self):
        print('Action button, p.volley_mode=', p.volley_mode, ', gs.game_mode=', gs.game_mode)
        # Progress through the speed/angle setting, game, then high score
        if p.volley_mode and gs.game_mode == 6 and not gs.Stuck:
            return
        else:
            cycle_modes(gs, stats, engine)
            print('  cycle_modes, gs.game_mode=', gs.game_mode)

        # Start or stop playing the angle and speed setting sound
        if gs.game_mode == 4 and SOUND_LOADED and p.fx_is_on:
            start_loop.play()
            start_loop.loop = True
        elif gs.game_mode == 6 and SOUND_LOADED and p.fx_is_on:
            start_loop.stop()

        # If its blinking, stop it
        if self.action_butt.is_blinking:
            Animation.cancel_all(self.action_butt)
            self.action_butt.is_blinking = False

        # Update the button text and color
        if p.volley_mode and gs.game_mode == 6:
            self.action_butt.label_text = ''
        else:
            self.action_butt.label_text = p.actionMSG[gs.game_mode]

        # If on completion of the game, add the high scores
        # If on restart of game, remove the high scores
        # Also move the sticks and option buttons out of the way
        if gs.game_mode == 7:
            print('  Animating out, w=', self.width, ' h=', self.height)
            if p.volley_mode:
                self.net.anim_out()

            self.add_high_scores()

            self.bg.anim_out()
            self.move_stick.anim_out(w=self.width, h=self.height)
            self.tilt_stick.anim_out(w=self.width, h=self.height)
            self.ball.anim_out()
            self.player[0].anim_out()
            if p.num_player > 1:
                self.player[1].anim_out()
            # self.option_butt.anim_out_then_in(w=self.width, h=self.height)
            # self.action_butt.anim_out_then_in(w=self.width, h=self.height)
        elif gs.game_mode == 3:
            print('  Animating in, w=', self.width, ' h=', self.height)
            self.remove_high_scores()
            self.bg.anim_in(w=self.width, h=self.height)
            self.move_stick.anim_in(w=self.width, h=self.height)
            self.tilt_stick.anim_in(w=self.width, h=self.height)
            self.ball.anim_in(w=self.width, h=self.height)
            self.player[0].anim_in(w=self.width, h=self.height)
            if p.num_player > 1:
                self.player[1].anim_in(w=self.width, h=self.height)
            if p.volley_mode:
                self.net.anim_in()

        # Turn the button blue momentarily
        self.action_butt.background_touched()

    # What to do when the tutorial button is pressed
    def tutorial_button_press(self):
        # Specify that this will be the one player version, and start game
        p.num_player = 1
        cycle_modes(gs, stats, engine)

        # Turn on tutorial mode
        self.tutorial_mode = True
        self.tutorial.__init__(w=self.width, h=self.height)
        self.tutorial.label_text = self.tutorial.msg[0]
        self.tutorial.anim_in(w=self.width, h=self.height, duration=1.0)
        self.tutorial.pause(2)

        # Add selected widgets
        self.remove_option_buttons()
        Clock.schedule_once(self.add_game_widgets, 0.25)

        # Turn the button blue momentarily
        self.tutorial_butt.background_touched()

    def difficult_button_press(self):
        # Increment the difficulty level
        if p.difficult_level < 2:
            p.difficult_level += 1
        else:
            p.difficult_level = 0

        # Channge the button text
        self.difficult_butt.label_text = 'Difficulty\n-- ' + p.difficult_text[p.difficult_level] + ' --'

        # Turn the button blue momentarily
        self.difficult_butt.background_touched()

    def fx_button_press(self):
        if p.fx_is_on:
            p.fx_is_on = False
            self.fx_butt.label_text = 'FX\nOff'
        else:
            p.fx_is_on = True
            self.fx_butt.label_text = 'FX\nOn'

        # Turn the button blue momentarily
        self.fx_butt.background_touched()

    def music_button_press(self):
        if p.music_is_on:
            p.music_is_on = False
            anim = Animation(volume=0.0, duration=1.0)
            for k in range(num_loops):
                anim.start(loop[k])
            self.music_butt.label_text = 'Music\nOff'
        else:
            p.music_is_on = True
            anim = Animation(volume=0.4, duration=1.0)
            for k in range(num_loops):
                anim.start(loop[k])
            self.music_butt.label_text = 'Music\nOn'

        # Turn the button blue momentarily
        self.music_butt.background_touched()

    def remove_tutorial_callback(self, dt):
        self.tutorial.label_text = ''
        self.remove_widget(self.tutorial)
        print('  --> Done!')

    def resize_canvas(self, *args):
        # GameState object
        gs.screen_width = self.width
        gs.screen_height = self.height

        # Splash screen
        if gs.game_mode == 1:
            self.splash.resize(w=self.width, h=self.height)

        # High score labels
        self.high_score_header.resize(w=self.width, h=self.height)
        self.high_dist_label.resize(w=self.width, h=self.height)
        self.high_height_label.resize(w=self.width, h=self.height)
        self.high_boing_label.resize(w=self.width, h=self.height)
        self.high_score_label.resize(w=self.width, h=self.height)
        self.volley_win_label.pos = (0.2 * self.width, 0.3 * self.height)
        self.volley_win_label.size = (0.6 * self.width, 0.5 * self.height)
        self.volley_win_label.font_size = 0.13 * self.height
        self.volley_win_label.outline_width = 0.01 * self.height

        # Score labels
        self.time_label.resize(w=self.width, h=self.height)
        self.dist_label.resize(w=self.width, h=self.height)
        self.high_label.resize(w=self.width, h=self.height)
        self.boing_label.resize(w=self.width, h=self.height)
        self.score_label.resize(w=self.width, h=self.height)

        # Sticks
        self.move_stick.resize(w=self.width, h=self.height)
        self.tilt_stick.resize(w=self.width, h=self.height)

        # Background image
        self.bg.resize(self.width, self.height)
        self.bg.bottom_line_height = self.height / 20.0

        # Buttons
        self.single_drubble_butt.resize(w=self.width, h=self.height)
        self.double_drubble_butt.resize(w=self.width, h=self.height)
        self.volley_drubble_butt.resize(w=self.width, h=self.height)
        self.tutorial_butt.resize(w=self.width, h=self.height)
        self.difficult_butt.resize(w=self.width, h=self.height)
        self.action_butt.resize(w=self.width, h=self.height)
        self.option_butt.resize(w=self.width, h=self.height)
        self.fx_butt.resize(w=self.width, h=self.height)
        self.music_butt.resize(w=self.width, h=self.height)

        # Tutorial
        self.tutorial.resize(w=self.width, h=self.height)

        # Volley
        self.net.resize(w=self.width, h=self.height)

    def show_banner(self):
        # Show ads
        if self.adSwitchSuccessful:
            self.banner_ad.show_ads()

    def hide_banner(self):
        if self.adSwitchSuccessful:
            # Hide ads
            self.banner_ad.hide_ads()

    # Time step the game
    def update(self, dt):
        if gs.game_mode < 3:
            # Make sure the AdMob banner is not automatically created at the start
            if self.adSwitchSuccessful:
                self.banner_ad.hide_ads()

            # There is no updating required for the splash and update screen, so exit the method
            return

        # Memory debugging and garbage collection
        if p.gc and gs.n > 0 and not gs.n % 100:
            gc.collect()
        if p.profile_mode and gs.n > 0 and not gs.n % 100:
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')

            print("[ Top 20 ]")
            for stat in top_stats[:20]:
                print(stat)

        # If running in demo mode, use computer control algorithm
        if p.demo_mode and gs.n > 0:
            Q = control_logic(gs.u, 0)
            sc = p.Qx, p.Qy, p.Ql, p.Qt
            gs.ctrl = [Q[k] / sc[k] for k in range(4)]

        # Call the sim_step method
        if gs.game_mode < 7:
            gs.sim_step()

        # Do tutorial stuff
        if self.tutorial_mode:
            # The ball will be paused above the player to allow them to get under the stool. The .ball_wait property
            # in the tutorial makes sure this pause only happens once per bounce. To determine whether to permit the
            # pause, this determines whether the sign of the trajectory has changed.
            sign_change = (self.tutorial.dyb_before * gs.dyb) < 0

            # The tutorial method tests several conditions to determine whether to advance
            self.tutorial.update(self)

            # Make the ball stationary while paused
            if self.tutorial.ball_is_paused:
                gs.xb, gs.yb, gs.dxb, gs.dyb = gs.u[:4] = self.tutorial.pause_state[:4]
            # Detect if ball bounce is impacting soon, in which case, pause it
            elif self.tutorial.n in (6, 7, 8) and gs.dyb <= -0.5 * norm(gs.u[2:4]) and not self.tutorial.ball_wait:
                self.tutorial.ball_is_paused = True
                self.tutorial.pause_state = gs.u[:4]
            # If a sign change occured, then permit flipping the .ball_wait property to False
            elif self.tutorial.ball_wait and sign_change:
                self.tutorial.ball_wait = False

        # Angle and speed settings
        if gs.game_mode < 6:
            gs.set_angle_and_speed()
            if gs.game_mode is 5 and SOUND_LOADED:
                start_loop.volume = 0.5 * gs.start_speed / p.ss

        if p.volley_mode:
            # Update the net
            self.net.update(gs.m2p, gs.po, w=self.width, h=self.height)

            # Automatically cycle based on randomized start conditions for the serving computer
            if gs.game_mode == 3 and p.serving_player == 1:
                self.action_button_press()
            elif gs.game_mode == 4 and p.serving_player == 1 and 180.0 / pi * gs.start_angle >= p.serving_angle:
                self.action_button_press()
            elif gs.game_mode == 5 and p.serving_player == 1 and gs.start_speed >= p.serving_speed:
                self.action_button_press()

            # Bring the action button back if the ball is stuck
            if gs.Stuck and self.action_butt.label_text is '':
                if stats.volley_score[0] >= p.winning_score or stats.volley_score[1] >= p.winning_score:
                    self.action_butt.label_text = 'Results'
                else:
                    self.action_butt.label_text = 'Restart'
        else:
            stats.update()

            # Update score line
            self.time_label.update('Time %9.1f' % gs.t)
            self.dist_label.update('Distance %6.1f' % stats.stool_dist)
            self.high_label.update('Height %7.2f' % stats.max_height)
            self.boing_label.update('Boing! %7.0f' % stats.stool_count)
            self.score_label.update('Score %8.0f' % stats.score)

        x_mean = 0.5 * (gs.xb + gs.xp[0])
        self.bg.update(x_mean, gs.yb, self.width, self.height)
        self.bg.make_markers()
        self.move_stick.update_el(gs.ctrl[0], gs.ctrl[1])
        self.tilt_stick.update_el(-gs.ctrl[3], gs.ctrl[2])

        # Start blinking the action button if the ball is stuck, and make the ball "explode"
        if gs.game_mode == 6 and gs.Stuck and not self.action_butt.is_blinking:
            self.action_butt.blink(duration=0.5)
            animation = Animation(random_scale=4.0, opacity=0.0, duration=3.0)
            animation.start(self.ball)

        # Update the ball
        self.ball.update(gs.xb, gs.yb, gs.m2p, gs.po, self.width, self.height, self.tutorial.ball_is_paused)
        if not p.volley_mode:
            self.ball_cannon.update(0.0, p.rb, gs.start_angle, gs.start_speed, gs.m2p, gs.po, self.width, self.height)
        elif p.serving_player is 0:
            self.ball_cannon.update(-p.back_line+1, p.rb, gs.start_angle, gs.start_speed, gs.m2p, gs.po)
        elif p.serving_player is 1:
            self.ball_cannon.update(p.back_line-1, p.rb, pi-gs.start_angle, gs.start_speed, gs.m2p, gs.po)

        if gs.stool_bounce and p.num_player > 1 and not p.volley_mode:
            self.ball.impact.color = self.player_dicts[1 - gs.active_player % 2]['ball_color']

        # Update the player(s)
        self.player[0].update(gs.xp[0], gs.yp[0] + 1.5*p.d, gs.lp[0], gs.tp[0], gs.m2p, gs.po,
                           self.width, self.height, gs.player[0])
        if p.num_player > 1:
            self.player[1].update(gs.xp[1], gs.yp[1] + 1.5 * p.d, gs.lp[1], gs.tp[1], gs.m2p, gs.po,
                                 self.width, self.height, gs.player[1])


class DrubbleApp(App):
    icon = 'a/icon.png'

    def on_start(self):
        if p.profile_mode:
            self.profile = cProfile.Profile()
            self.profile.enable()

    def on_stop(self):
        if p.profile_mode:
            self.profile.disable()
            self.profile.dump_stats('drubble.profile')

    def build(self):
        data_dir = getattr(self, 'user_data_dir')
        stats.init_high(join(data_dir, 'scores.json'))
        game = DrubbleGame()
        Clock.schedule_interval(game.update, 1.0/fs)
        return game


if __name__ == '__main__':
    DrubbleApp().run()