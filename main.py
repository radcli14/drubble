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
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        keyPush = ctrl2keyPush(gs)
        gs.setControl(keyPush=kvUpdateKey(keyPush,keycode,1))
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
            makeMarkers(p1,self.width,self.height)
            
            # Draw Player One
            Color(darkGreen[0], darkGreen[1], darkGreen[2], 1)
            Line(points=p1.player,width=0.075*p1.m2p)
            Color(white[0], white[1], white[2], 1)
            Line(points=p1.stool,width=0.05*p1.m2p)
            
            if nPlayer>1:
                Color(red[0], red[1], red[2], 1)
                Line(points=p2.player,width=0.075*p2.m2p)
                Color(black[0], black[1], black[2], 1)
                Line(points=p2.stool,width=0.05*p2.m2p)
            #Ellipse(pos=self.pos,size=self.size)
            
        #makeMarkerText(p1,width,height)
        
    def update(self,dt):
        gs.simStep()
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