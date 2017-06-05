# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 14:25:28
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-04 21:36:22

import RPi.GPIO as GPIO
class Sentinel(object):
    def __init__(self):
        """Create an instance of Sentinel"""
        # Initialize Everything
        self.KNOB0 = False
        self.KNOB1 = False
        self.KNOB2 = False
        self.KNOB3 = False
        self.KNOB4 = False
        self.KNOB5 = False
        self.Proximity = 0.0
        self.ProximityRetries = 3
        self.FlagDisparity = False
        self.CONST_REDUX = 0.1
        self.CONST_ZONE_FIX = 0.0
    def getState(self, desi):
        self.KNOB0 = GPIO.input(GPIO.IN_SPEED0)
        self.KNOB1 = GPIO.input(GPIO.IN_SPEED1)
        self.KNOB2 = GPIO.input(GPIO.IN_SPEED2)
        self.KNOB3 = GPIO.input(GPIO.IN_SPEED3)
        self.KNOB4 = GPIO.input(GPIO.IN_SPEED4)
        self.KNOB5 = GPIO.input(GPIO.IN_SPEED5)

