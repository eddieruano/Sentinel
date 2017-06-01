# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 07:23:39
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 08:33:43

import RPi.GPIO as GPIO

class DESI(object):
    """Representation of a DESI Entity"""
    # Control Box Pins
    IN_START    = 9
    IN_PAUSE    = 10
    IN_SPEED0   = 11
    IN_SPEED1   = 5
    IN_SPEED2   = 6
    IN_SPEED3   = 13
    IN_SPEED4   = 19
    # Proximity Sensor Pins
    PROX1_TRIG  = 4
    PROX1_ECHO  = 17
    PROX2_TRIG  = 27
    PROX2_ECHO  = 22
    # Relay Pins
    OUT_START   = 14
    OUT_OFF     = 15
    OUT_PAUSE   = 18
    OUT_ENTER   = 23
    OUT_0       = 24
    OUT_1       = 25
    OUT_2       = 8
    OUT_3       = 7
    OUT_4       = 12
    OUT_5       = 16
    OUT_DOWN    = 21
    OUT_ALEXA   = 20
    # States of DESI
    State_Main  = "Idle"
    State_Knob  = "Speed0"
    State_Touch = "Negative"
    # Constructor
    def __init__(self):
        """Create an instance of DESI"""
        # Nothing to do here since there is very little state in the class.
        pass
    def initDESI(self):
        # Set up GPIO stuff
        GPIO.setmode(GPIO.BCM)
        self.initControlBox()
        self.initRelays()
    def initControlBox(self):
        GPIO.setup(self.IN_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Start & Pause Set.")
        GPIO.setup(self.IN_SPEED0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print("Buttons Complete.")
    def initProximity(self, sensorV1, sensorV2):
        # Set up the correct In/Out Scheme for send/receive
        GPIO.setup(sensorV1.trigger_pin, GPIO.OUT)
        GPIO.setup(sensorV1.echo_pin, GPIO.IN)
        GPIO.setup(sensorV2.trigger_pin, GPIO.OUT)
        GPIO.setup(sensorV2.echo_pin, GPIO.IN)
        print("Proximity Sensors Set.")
    def initRelays(self):
        # Set up the correct In/Out Scheme for send/receive
        GPIO.setup(self.OUT_START, GPIO.OUT)
        GPIO.setup(self.OUT_OFF, GPIO.OUT)
        GPIO.setup(self.OUT_PAUSE, GPIO.OUT)
        GPIO.setup(self.OUT_ENTER, GPIO.OUT)
        GPIO.setup(self.OUT_0, GPIO.OUT)
        GPIO.setup(self.OUT_1, GPIO.OUT)
        GPIO.setup(self.OUT_2, GPIO.OUT)
        GPIO.setup(self.OUT_3, GPIO.OUT)
        GPIO.setup(self.OUT_4, GPIO.OUT)
        GPIO.setup(self.OUT_5, GPIO.OUT)
        GPIO.setup(self.OUT_DOWN, GPIO.OUT)
        GPIO.setup(self.OUT_ALEXA, GPIO.OUT)
        GPIO.output(self.OUT_START, GPIO.HIGH)
        GPIO.output(self.OUT_OFF, GPIO.HIGH)
        GPIO.output(self.OUT_PAUSE, GPIO.HIGH)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        GPIO.output(self.OUT_0, GPIO.HIGH)
        GPIO.output(self.OUT_1, GPIO.HIGH)
        GPIO.output(self.OUT_2, GPIO.HIGH)
        GPIO.output(self.OUT_3, GPIO.HIGH)
        GPIO.output(self.OUT_4, GPIO.HIGH)
        GPIO.output(self.OUT_5, GPIO.HIGH)
        GPIO.output(self.OUT_DOWN, GPIO.HIGH)
        GPIO.output(self.OUT_ALEXA, GPIO.HIGH)
        print("Proximity Sensors Set.")
