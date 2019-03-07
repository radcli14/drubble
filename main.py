#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:18:17 2019

@author: radcli14
"""
# Import the Kivy modules
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

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
Window.clearcolor = (0.86, 0.9, 1, 1)


class drubbleGame(Widget):
    pass


xv,yv, sx, sy = stickDude(gs,0)
# Get ranges for drawing the player and ball
xrng, yrng, m2p, po, m2r, ro = setRanges(gs.u)
            
class drubbleApp(App):
    def build(self):
        return drubbleGame()


if __name__ == '__main__':
    drubbleApp().run()