#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 22:51:49 2019

@author: radcli14
"""
import time
import pygame
pygame.mixer.init()
kick = pygame.mixer.Sound('kick.wav')
snare = pygame.mixer.Sound('snare1.wav')
hat = pygame.mixer.Sound('hat1.wav')
timb = pygame.mixer.Sound('timbaleFlam1.wav')

kick.play()
time.sleep(1)
snare.play()
time.sleep(1)
hat.play()
time.sleep(1)
timb.play()