# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 14:25:28
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-14 10:01:17

import RPi.GPIO as GPIO
import logging
import subprocess
import time

from subprocess import CalledProcessError
from subprocess import check_output

""" Initialization of Central Logger """
# Top Vars
LogLevel = logging.DEBUG        ## Change this later
LogLocation = "mainLog.txt"
#-------S8Proto
# Create Instance of Logger
Houston = logging.getLogger(__name__)
# Setting Logging Level --Change from Debug later
Houston.setLevel(level=LogLevel)
# Set up Format Protocol --> Type of Msg, Name of Module, Time, PayloadMessage
HouForm = logging.Formatter('%(levelname)s:%(name)s:%(asctime)s:%(message)s')
# Set up File Handler + Add level + add formatter
HouFile = logging.FileHandler(LogLocation)
HouFile.setLevel(LogLevel)
HouFile.setFormatter(HouForm)
# Set up Stream Handler + level + format
HouStream = logging.StreamHandler()
HouStream.setLevel(LogLevel)
HouStream.setFormatter(HouForm)
# Add all handlers to instance of Handler
Houston.addHandler(HouStream)
Houston.addHandler(HouFile)
Houston.info("Logger has been created.")
class Sentinel(object):
    def __init__(self):
        global Houston
        """Create an instance of Sentinel"""
        # CONSTANTS
        self.flagPause = False
        self.flagShut = False
        self.CONST_REDUX = 0.1
        self.CONST_ZONE_FIX = 0.0
        self.PROXCOUNT = 50
        self.CAPCOUNT = 60
        self.CONST_BOUNCE = 800
        self.CONST_RESCOUNT = 60
        self.CONST_PROX_RETRIES = 50
        # Locks/Mutex/Counters
        self.ActiveLock = True
        self.CapLock = False
        self.ProxLock = False
        self.Redux = 0.0
        self.ProxCountdown = self.PROXCOUNT
        self.CapCountdown = self.CAPCOUNT
        self.SpCount = self.CONST_RESCOUNT
        self.CountdownLoopSpeed = 1.0   # seconds
        self.RunningLoopSpeed = 0.05    # seconds
        # Knob Monitors
        self.StateKnob = 1.0
        self.KNOB0 = False
        self.KNOB1 = False
        self.KNOB2 = False
        self.KNOB3 = False
        self.KNOB4 = False
        self.KnobInterrupt = False
        self.StartDetect = False
        # Proximity Monitors
        self.Proximity = 0.0
        self.ProximityRetries = self.CONST_PROX_RETRIES
        self.FlagDisparity = False
        # Capacitive Monitors
        self.TouchRegister = 0
        self.PrimaryGripChannel = 1 << 2
        self.SecondaryGripChannel = 1 << 8
        # Mutex
        self.MutexSpeech = False;
    def queryKnobState(self, desi):
        if (GPIO.input(desi.IN_SPEED0) == False):
            self.StateKnob == 0.0
        elif (GPIO.input(desi.IN_SPEED1) == False):
            self.StateKnob == 1.0
        elif (GPIO.input(desi.IN_SPEED2) == False):
            self.StateKnob == 2.0
        elif (GPIO.input(desi.IN_SPEED3) == False):
            self.StateKnob == 3.0
        elif (GPIO.input(desi.IN_SPEED4) == False):
            self.StateKnob == 4.0
        else:
            # Do Nothing
            Houston.error("No Knob Position was set.")
    def setSpeed(self, speed):
        self.ActualSpeed = speed
        self.Redux = (self.ActualSpeed * self.CONST_REDUX) * 10
    def updateActiveLock(self, intouch):
        self.TouchRegister = intouch.touched()
        # Need to target channels
        if (self.TouchRegister  > 1):
            self.ActiveLock = True
        else:
            self.ActiveLock = False
    def setKnobInterrupt(self):
        self.KnobInterrupt = True
    def checkForInput(self):
        if self.KnobInterrupt == True:
            return True
        else:
            return False
    def checkMutexSpeech(self):
        try:
            if (subprocess.check_output(["pidof","-s", "aplay"]) == 0):
                self.MutexSpeech = False;
            else:
                self.MutexSpeech = True;
            return self.MutexSpeech
        except CalledProcessError:
            self.MutexSpeech = False
            return self.MutexSpeech
    def takeMutexSpeech(self):
        subprocess.call(['killall', 'aplay'])
    def clearMutexSpeech(self):
        while(self.checkMutexSpeech()):
            self.takeMutexSpeech()
        return True
    def waitMutexSpeech(self):
        while(self.checkMutexSpeech()):
            time.sleep(0.001)
        return True
    def inMotion(self, desi):
        if desi.State_Main == "Paused":
            return False
        elif desi.State_Main == "Speed0":
            return False
        elif self.CapLock == True:
            return False
        elif self.ProxLock == True:
            return False
        else:
            return True