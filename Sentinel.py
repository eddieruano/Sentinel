# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 14:25:28
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-05 01:08:36

import RPi.GPIO as GPIO
class Sentinel(object):
    def __init__(self):
        """Create an instance of Sentinel"""
        # Locks/Mutex/Counters
        self.ActiveLock = True
        self.Redux = 0.0
        self.ProxCountdown = 50
        self.CapCountdown = 100
        self.CountdownLoopSpeed = 1.0   # seconds
        self.RunningLoopSpeed = 0.05    # seconds
        # Knob Monitors
        self.StateKnob = 0
        self.KNOB0 = False
        self.KNOB1 = False
        self.KNOB2 = False
        self.KNOB3 = False
        self.KNOB4 = False
        self.StateSpeed = 0.0
        # Proximity Monitors
        self.Proximity = 0.0
        self.ProximityRetries = 3
        self.FlagDisparity = False
        self.CONST_REDUX = 0.1
        self.CONST_ZONE_FIX = 0.0
        # Capacitive Monitors
        self.TouchRegister = 0
        self.PrimaryGripChannel = 1 << 2
        self.SecondaryGripChannel = 1 << 8
    def getStateKnob(self, desi):
        self.KNOB0 = GPIO.input(desi.IN_SPEED0)
        self.KNOB1 = GPIO.input(desi.IN_SPEED1)
        self.KNOB2 = GPIO.input(desi.IN_SPEED2)
        self.KNOB3 = GPIO.input(desi.IN_SPEED3)
        self.KNOB4 = GPIO.input(desi.IN_SPEED4)
    def setStateKnob(self):
        if self.KNOB0 == False:
            self.StateKnob = 0
            print("State0")
        elif self.KNOB1 == False:
            self.StateKnob = 1
            print("State1")
        elif self.KNOB2 == False:
            self.StateKnob = 2
            print("State2")
        elif self.KNOB3 == False:
            self.StateKnob = 3
            print("State3")
        elif self.KNOB4 == False:
            self.StateKnob = 4
            print("State4")
        else:
            print("Error in StateKnob")
    def setStateCap(self, intouch):
        self.TouchRegister = intouch
    def setSpeed(self, speed):
        self.StateSpeed = speed
        self.Redux = (self.StateSpeed * 0.5) * 10
    def updateActiveLock(self, intouch):
        self.TouchRegister = intouch.touched()
        # Need to target channels
        print (intouch.touched())
        if self.TouchRegister  > 1:
            self.ActiveLock = True
        else:
            #print ("NO CONTACT")
            self.ActiveLock = False
        

