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
keyPush        = np.zeros(8)

# Initialize stats
stats = gameScore()

# Set the sky blue background color
Window.clearcolor = (skyBlue[0], skyBlue[1], skyBlue[2], 1)
Window.size = (width, height)

# Initialize the players
p1 = playerLines(0)
p2 = playerLines(1)

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
            # Draw Bottom Line
            Color(black[0], black[1], black[2],1)
            Rectangle(pos=(0,0),size=(self.width, self.height/20))
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
                
        # Player drawing settings        
        xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
        p1.width = p2.width = self.width
        p1.height = p2.height = self.height
        
        p1.update(gs)
        p2.update(gs)
        
        self.update_canvas()
    pass

class drubbleApp(App):
    def build(self):
        game = drubbleGame()
        Clock.schedule_interval(game.update, 1.0/fs)
        return game

if __name__ == '__main__':
    drubbleApp().run()