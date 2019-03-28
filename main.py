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
#from kivy.properties import NumericProperty, ReferenceListProperty, OptionProperty
from kivy.core.window import Window
#from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import *
#from kivy.config import Config

# Execute drubbleFunc to get the supporting functions and classes
exec(open('./drubbleFunc.py').read())

# Obtain Parameters
p = parameters()

# Initial states
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.rb,0,0,p.x0,p.y0,p.l0,0,0,0,0,10,
                 0   ,p.y0,p.l0,0,0,0,0,-10]
gs = gameState(u0)

# Set the keyboard input and mouse defaults
keyPush = np.zeros(8)

# Initialize stats
stats = gameScore()

# Set the sky blue background color
Window.clearcolor = (skyBlue[0], skyBlue[1], skyBlue[2], 1)
Window.size = (width, height)
#width, height = Window.size
#leftAlign = OptionProperty('left')

# Set the icon (neither are working...)
#Config.window_icon = 'figs/icon.png'
Window.icon = 'figs/icon.png'

# Initialize the players
p1 = playerLines(0)
p2 = playerLines(1)

class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        self.xpos = 0
        self.sz_orig = self.w_orig,self.h_orig = (2400,400)
        with self.canvas:
            # Import the background image
            self.bg = Rectangle(source='figs/bg0.png', 
                                pos=(0,0), size=self.sz_orig)

             # Draw the bottom line
            Color(black[0], black[1], black[2],1)
            self.bl = Rectangle(pos=(0,0),size=(width, height/20))

    def update(self, x, y, w, h, m2p): 
        scf = (m2p/70)**0.5
        posInBG = x/100*scf*(self.w_orig-self.xpos) # Position in the Background
        self.bg.size = (int(self.w_orig*scf),int(self.h_orig*scf))
        self.bg.pos = (w/2.0-posInBG,0)
        self.bl.size = (w,h/20)

class splashScreen(Widget):
    def __init__(self, **kwargs):
        super(splashScreen, self).__init__(**kwargs) 
        self.k = 0
            
    def update(self,showSplash):  
        if not gs.showedSplash:
            self.k += 2
            self.canvas.clear()
            with self.canvas:
                Color(skyBlue[0]*self.k/255,skyBlue[1]*self.k/255,skyBlue[2]*self.k/255,1)
                Rectangle(pos=(0,0),size=(width,height))
                if showSplash:
                    Rectangle(source='figs/splash.png',pos=(0,0.2*height), 
                              size=(0.8*width,0.8*height))
                    if self.k >= 255:
                        Label(font_size=48,pos=(0,0),size=(width,0.2*height),
                              color=(darkGreen[0],darkGreen[1],darkGreen[2],1),
                              halign='center',text='Press Space to Begin!')
        if self.k >= 255:
            gs.showedSplash = True    
            
    def clear(self):
        with self.canvas:
            Color(skyBlue[0]*self.k/255,skyBlue[1]*self.k/255,skyBlue[2]*self.k/255,1)
            Rectangle(pos=(0,0),size=(width,height))            

# Returns the center_x, center_y, and diameter of the stick
def get_stick_pos(ch):
    return ch.pos[0]+ch.size[0]/2.0, ch.pos[1]+ch.size[1]/2.0, ch.size[0] 

class stick(Widget):
    def __init__(self,**kwargs):
        super(stick, self).__init__(**kwargs)
        with self.canvas:
            self.ch = Rectangle(source='figs/crossHair.png',**kwargs)    
            ch_x, ch_y, ch_s = get_stick_pos(self.ch)
            self.el = Ellipse(pos=(ch_x-ch_s/4.0,ch_y-ch_s/4.0),
                              size=(ch_s/2.0,ch_s/2.0))
        
        self.ts_x = (ch_x-ch_s/2.0,ch_x+ch_s/2.0)
        self.ts_y = (ch_y-ch_s/2.0,ch_y+ch_s/2.0)
        self.cntr = (ch_x,ch_y)
        self.ctrl = (0,0)

    def update_el(self,x,y):
        ch_x, ch_y, ch_s = get_stick_pos(self.ch)
        self.el.pos = (ch_x-ch_s/4.0+ch_s*x/4.0,ch_y-ch_s/4.0+ch_s*y/4.0)
        self.ctrl = (x,y)

class drubbleGame(Widget):
    def __init__(self,**kwargs):
        super(drubbleGame, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.bind(size=self.resize_canvas)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up = self._on_keyboard_up)
        self.nMarks = 0
        self.yardMark = []
        self.weHaveWidgets = False
        self.weHaveButtons = False
        with self.canvas:
            self.splash = splashScreen()
            self.add_widget(self.splash)
        
    def add_game_widgets(self): 
        # Add game widgets
        with self.canvas:
            # Initialize the background
            self.bg = MyBackground()
            self.add_widget(self.bg)
            
            # Initialize the sticks
            sz = 0.2*self.width
            self.moveStick = stick(size=(sz,sz), pos=(0.8*width,0.05*height))
            self.add_widget(self.moveStick)
            self.tiltStick = stick(size=(sz,sz), pos=(0,0.05*height))
            self.add_widget(self.tiltStick)
            
            # Initialize the score line
            self.time_label = Label(font_size=18,halign='left',
                                    pos=(0.0*self.width,self.height-20),
                                    size=(0.2*self.width,18),
                                    text='Time = 0.0',color=(0,0,0,1))
            self.add_widget(self.time_label)
            self.dist_label = Label(font_size=18,halign='left',
                                    pos=(0.2*self.width,self.height-20),
                                    size=(0.2*self.width,18),
                                    text='Distance = 0.00',color=(0,0,0,1))
            self.add_widget(self.dist_label)
            self.high_label = Label(font_size=18,halign='left',
                                    pos=(0.4*self.width,self.height-20),
                                    size=(0.2*self.width,18),
                                    text='Height = 0.00',color=(0,0,0,1))
            self.add_widget(self.high_label)
            self.boing_label = Label(font_size=18,halign='left',
                                    pos=(0.6*self.width,self.height-20),
                                    size=(0.2*self.width,18),
                                    text='Boing! = 0',color=(0,0,0,1))
            self.add_widget(self.boing_label)
            self.score_label = Label(font_size=18,halign='left',
                                    pos=(0.8*self.width,self.height-20),
                                    size=(0.2*self.width,18),
                                    text='Score = 0',color=(0,0,0,1))
            self.add_widget(self.score_label)
            dir(self.score_label)

    def add_option_buttons(self):
        w,h = (self.width,self.height)
        # Add option screen buttons
        with self.canvas:
            self.singleDrubbleButt = Button(text='Single Drubble',
                                            size=(0.8*w,0.2*h),
                                            pos=(0.1*w,0.7*h),
                                            font_size=0.1*h)
            self.doubleDrubbleButt = Button(text='Double Drubble',
                                            size=(0.8*w,0.2*h),
                                            pos=(0.1*w,0.4*h),
                                            font_size=0.1*h)
            self.tripleDrubbleButt = Button(text='Triple Drubble',
                                            size=(0.8*w,0.2*h),
                                            pos=(0.1*w,0.1*h),
                                            font_size=0.1*h)
    ## Controls
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(keyPush,keycode,1))
        if keycode[1] == 'spacebar':
            cycleModes(gs,stats)
        return True
    
    def _on_keyboard_up(self, keyboard, keycode):
        keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(keyPush,keycode,0))
        return True
    
    def on_touch_down(self, touch):
        if gs.gameMode==2 and touch.y>self.height*0.67:
            p.nPlayer=1
            print('nPlayer=',str(p.nPlayer))
            cycleModes(gs,stats)
        elif gs.gameMode==2 and touch.y>self.height*0.33:
            p.nPlayer=2
            print('p.nPlayer=',str(p.nPlayer))
            cycleModes(gs,stats)
        elif gs.gameMode>2:
            # Cycle through modes if touch above the halfway point
            if touch.y > self.height/2:
                cycleModes(gs,stats)

            # Detect control inputs
            xy = touchStick((touch.x,touch.y),self.moveStick)
            if xy[0] != 0:
                self.moveStick.id = touch.id
                self.moveStick.update_el(xy[0],xy[1])
                gs.ctrl[0:2] = xy
            
            xy = touchStick((touch.x,touch.y),self.tiltStick)
            if xy[0] != 0:
                self.tiltStick.id = touch.id    
                self.tiltStick.update_el(xy[0],xy[1])
                gs.ctrl[2:4] = [xy[1],-xy[0]]

    def on_touch_move(self,touch):
        if gs.gameMode>2 and self.weHaveWidgets: 
            # Detect control inputs
            xy = touchStick((touch.x,touch.y),self.moveStick)
            if touch.id == self.moveStick.id and xy[0] != 0:
                self.moveStick.update_el(xy[0],xy[1])
                gs.ctrl[0:2] = xy

            xy = touchStick((touch.x,touch.y),self.tiltStick)
            if touch.id == self.tiltStick.id and xy[0] != 0:
                self.tiltStick.update_el(xy[0],xy[1])
                gs.ctrl[2:4] = [xy[1],-xy[0]]

    def on_touch_up(self,touch):
        if gs.gameMode>2 and self.weHaveWidgets:
            if touch.id == self.moveStick.id:
                self.moveStick.update_el(0,0)
                gs.ctrl[0:2] = [0,0]
                
            if touch.id == self.tiltStick.id:
                self.tiltStick.update_el(0,0)
                gs.ctrl[2:4] = [0,0]

    #3 Drawing commands
    def update_canvas(self,*args):
        if self.weHaveWidgets:
            self.canvas.clear()
            with self.canvas:                       
                # Draw the tracer line
                Color(white[0], white[1], white[2], 1)
                x,y = xy2p(gs.xTraj,gs.yTraj,p1.m2p,p1.po,self.width,self.height)
                Line(points=intersperse(x,y),width=1.5)
                
                # Draw Bottom Line
                makeMarkers(self,p1)
                
                # Draw Player One
                Color(darkGreen[0], darkGreen[1], darkGreen[2], 1)
                Line(points=p1.player,width=0.075*p1.m2p)
                Color(white[0], white[1], white[2], 1)
                Line(points=p1.stool,width=0.05*p1.m2p)
                
                if p.nPlayer>1:
                    # Draw Player Two
                    Color(red[0], red[1], red[2], 1)
                    Line(points=p2.player,width=0.075*p2.m2p)
                    Color(black[0], black[1], black[2], 1)
                    Line(points=p2.stool,width=0.05*p2.m2p)
            
                # Draw the ball
                Color(pink[0], pink[1], pink[2], 1)
                x,y = xy2p(gs.xb,gs.yb,p1.m2p,p1.po,self.width,self.height)
                Ellipse(pos=(x-p1.m2p*p.rb,y-p1.m2p*p.rb),
                        size=(2.0*p1.m2p*p.rb,2.0*p1.m2p*p.rb))
                
    def resize_canvas(self,*args):
        if self.weHaveWidgets:
            self.time_label.pos=(0.0*self.width,self.height-20)
            self.dist_label.pos=(0.2*self.width,self.height-20)
            self.high_label.pos=(0.4*self.width,self.height-20)
            self.boing_label.pos=(0.6*self.width,self.height-20)
            self.score_label.pos=(0.8*self.width,self.height-20)
            
            sz = self.moveStick.ch.size[0]
            self.moveStick.ch.pos = (self.width-sz,0.05*self.height)       
            self.tiltStick.ch.pos = (0,0.05*self.height)

    ## Time step the game
    def update(self,dt):
        # Either update the splash, or add the widgets
        if gs.gameMode == 1:
            self.splash.update(True)
        elif gs.gameMode == 2 and not self.weHaveButtons:
            self.add_option_buttons()
            self.splash.clear()
            self.remove_widget(self.splash)
            self.weHaveButtons = True
        elif gs.gameMode>2 and not self.weHaveWidgets:
            self.add_game_widgets()            
            self.weHaveWidgets = True            
            print('nPlayer=',str(p.nPlayer))   
            
        ## ANGLE AND SPEED SETTINGS
        if gs.gameMode>2 and gs.gameMode<6:
            gs.setAngleSpeed()
        
        gs.simStep()
        if gs.gameMode==6:
            stats.update()

            # Update score line
            self.time_label.text  = 'Time = '+f'{gs.t:.1f}'
            self.dist_label.text  = 'Distance = '+f'{stats.stoolDist:.2f}'
            self.high_label.text  = 'Height = '+f'{stats.maxHeight:.2f}'
            self.boing_label.text = 'Boing! = '+str(int(stats.stoolCount))
            self.score_label.text = 'Score = '+str(stats.score)    
            
        # Player drawing settings        
        xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
        p1.width = p2.width = self.width
        p1.height = p2.height = self.height
        
        p1.update(gs)
        p2.update(gs)
        
        if gs.gameMode>2:
            xMean = (gs.xb+gs.xp[0])/2.0
            self.bg.update(xMean,gs.yb,self.width,self.height,m2p)
            self.moveStick.update_el(gs.ctrl[0],gs.ctrl[1])
            self.tiltStick.update_el(-gs.ctrl[3],gs.ctrl[2])
            
            self.update_canvas()

class drubbleApp(App):
    icon = 'figs/icon.png'
    def build(self):
        game = drubbleGame()
        Clock.schedule_interval(game.update, 1.0/fs)
        return game

if __name__ == '__main__':
    drubbleApp().run()