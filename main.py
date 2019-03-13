#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:18:17 2019

@author: radcli14
"""
# Import the Kivy modules
from kivy.app import App
from kivy.uix.widget import Widget
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

class playerLines():
    def __init__(self,gs,pnum):
        # Get the player stick figure
        xv, yv, sx, sy = stickDude(gs,pnum)
        
        # Get ranges for drawing the player and ball
        xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
        
        # Convert to pixels
        x,y = xy2p(xv,yv,m2p,po,width,height)
        xs,ys = xy2p(sx,sy,m2p,po,width,height)
        
        # Convert to format used for Kivy line
        self.m2p = m2p
        self.player = intersperse(x,y)
        self.stool  = intersperse(xs,ys)
        
    def update(self,gs):
        # Get the player stick figure
        xv, yv, sx, sy = stickDude(gs,0)
        
        # Get ranges for drawing the player and ball
        xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
        
        # Convert to pixels
        x,y = xy2p(xv,yv,m2p,po,width,height)
        xs,ys = xy2p(sx,sy,m2p,po,width,height)
        
        # Convert to format used for Kivy line
        self.m2p = m2p
        self.player = intersperse(x,y)
        self.stool  = intersperse(xs,ys)

p1 = playerLines(gs,0)

class drubbleGame(Widget):
    def __init__(self,**kwargs):
        super(drubbleGame, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
    n = 0
       
    # Internal properties of the game widget
    def update_canvas(self,*args):
        self.canvas.clear()
        with self.canvas:
            # Draw Bottom Line
            Color(0,0,0,1)
            Rectangle(pos=(0,0),size=(self.width, self.height/20))
            
            # Draw Player One
            Color(darkGreen[0], darkGreen[1], darkGreen[2], 1)
            Line(points=p1.player,width=0.075*p1.m2p)
            Color(white[0], white[1], white[2], 1)
            Line(points=p1.stool,width=0.05*p1.m2p)
            #Ellipse(pos=self.pos,size=self.size)
    
    def update(self,dt):
        gs.simStep()
        p1.update(gs)
        
        self.update_canvas()
    pass

class drubbleApp(App):
    def build(self):
        game = drubbleGame()
        Clock.schedule_interval(game.update, 1.0/fs)
        return game

if __name__ == '__main__':
    drubbleApp().run()