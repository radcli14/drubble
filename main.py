#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:18:17 2019

@author: radcli14
"""

from kivy.app import App
from kivy.uix.widget import Widget


class drubbleGame(Widget):
    pass


class drubbleApp(App):
    def build(self):
        return drubbleGame()


if __name__ == '__main__':
    drubbleApp().run()