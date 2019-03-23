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
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics import *

# Execute drubbleFunc to get the supporting functions and classes
exec(open('./drubbleFunc.py').read())

# Obtain Parameters
p = parameters()

# Initial states
q0 = np.matrix([[0],[p.y0],[p.l0],[0]])
u0 = [0,p.rb,0,0,p.x0,p.y0,p.l0,0,0,0,0,10,
                 0   ,p.y0,p.l0,0,0,0,0,-10]
nPlayer = 2
gs = gameState(u0)

# Set the keyboard input and mouse defaults
keyPush = np.zeros(8)

# Initialize stats
stats = gameScore()

# Set the sky blue background color
Window.clearcolor = (skyBlue[0], skyBlue[1], skyBlue[2], 1)
Window.size = (width, height)

# Initialize the players
p1 = playerLines(0)
p2 = playerLines(1)

class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        self.xpos = 0
        with self.canvas:
            # Import the background image
            self.bg = Rectangle(source='figs/bg0.png', 
                                pos=(0,0), size=(2400,400))

             # Draw the bottom line
            Color(black[0], black[1], black[2],1)
            self.bl = Rectangle(pos=(0,0),size=(width, height/20))

    def update(self, x, y, w, h):
        self.bg.pos = (w*(-x/60+self.xpos),-y*5+h/20)
        self.bl.size = (w,h/20)

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

    def update_el(self,x,y):
        ch_x, ch_y, ch_s = get_stick_pos(self.ch)
        self.el.pos = (ch_x-ch_s/4.0+ch_s*x/4.0,ch_y-ch_s/4.0+ch_s*y/4.0)

class drubbleGame(Widget):
    def __init__(self,**kwargs):
        super(drubbleGame, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up = self._on_keyboard_up)
        self.nMarks = 0
        self.yardMark = []
        
        # Add score line widgets
        with self.canvas:
            # Initialize the background
            self.bg = MyBackground()
            self.add_widget(self.bg)
            
            # Initialize the sticks
            sz = 0.2*width
            self.moveStick = stick(size=(sz,sz), pos=(0.8*width,0.05*height))
            self.add_widget(self.moveStick)
            self.tiltStick = stick(size=(sz,sz), pos=(0,0.05*height))
            self.add_widget(self.tiltStick)
            
            # Initialize the score line
            self.time_label = Label(font_size=18,pos=(10,420),halign='left',
                                    text='Time = ',color=(0,0,0,1))
            self.add_widget(self.time_label)
            self.dist_label = Label(font_size=18,pos=(160,420),halign='left',
                                    text='Distance = ',color=(0,0,0,1))
            self.add_widget(self.dist_label)
            self.high_label = Label(font_size=18,pos=(310,420),halign='left',
                                    text='Height = ',color=(0,0,0,1))
            self.add_widget(self.high_label)
            self.boing_label = Label(font_size=18,pos=(460,420),halign='left',
                                    text='Boing! = ',color=(0,0,0,1))
            self.add_widget(self.boing_label)
            self.score_label = Label(font_size=18,pos=(610,420),halign='left',
                                    text='Score = ',color=(0,0,0,1))
            self.add_widget(self.score_label)
        
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
    
    # Internal properties of the game widget
    def update_canvas(self,*args):
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
            
            if nPlayer>1:
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

    def update(self,dt):
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
        
        self.bg.update((gs.xb+gs.xp[0])/2.0,gs.yb,self.width,self.height)
        self.moveStick.update_el(gs.ctrl[0],gs.ctrl[1])
        self.tiltStick.update_el(-gs.ctrl[3],gs.ctrl[2])
        
        self.update_canvas()
    pass

class drubbleApp(App):
    def build(self):
        game = drubbleGame()
        Clock.schedule_interval(game.update, 1.0/fs)
        return game

if __name__ == '__main__':
    drubbleApp().run()