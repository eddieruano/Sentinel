# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 07:23:39
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-02 12:31:32

import RPi.GPIO as GPIO
import logger
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
    PROX1_TRIG  = 17
    PROX1_ECHO  = 4
    PROX2_TRIG  = 22
    PROX2_ECHO  = 27
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
        GPIO.setwarnings(False) #check
        self.initControlBox()
        self.initRelays()
    def initControlBox(self):
        GPIO.setup(self.IN_START, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_PAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IN_SPEED4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print ("Buttons Complete.")
    def initProximity(self, sensorV1, sensorV2):
        # Set up the correct In/Out Scheme for send/receive
        GPIO.setup(sensorV1.trigger_pin, GPIO.OUT)
        GPIO.setup(sensorV1.echo_pin, GPIO.IN)
        GPIO.setup(sensorV2.trigger_pin, GPIO.OUT)
        GPIO.setup(sensorV2.echo_pin, GPIO.IN)
        print ("Proximity Sensor Set.")
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
        print ("Relay Array Set.")
    def DESIListen(self):
        GPIO.add_event_detect(self.IN_START, GPIO.FALLING, performStart, bounceTime)
        GPIO.add_event_detect(self.IN_PAUSE, GPIO.FALLING, performPause, bounceTime)
        GPIO.add_event_detect(self.IN_SPEED0, GPIO.FALLING, perform00, bounceTime)
        GPIO.add_event_detect(self.IN_SPEED1, GPIO.FALLING, perform01, bounceTime)
        GPIO.add_event_detect(self.IN_SPEED2, GPIO.FALLING, perform02, bounceTime)
        GPIO.add_event_detect(self.IN_SPEED3, GPIO.FALLING, perform03, bounceTime)
        GPIO.add_event_detect(self.IN_SPEED4, GPIO.FALLING, perform04, bounceTime)
        print("Listening.")
    def DESISend(self, command):
        if command == "Start":
            self.performStart()
            print("SendStart")
        elif command == "Pause":
            self.performPause()
            print("SendPause")
        elif command == "Off":
            self.performOff()
            print("Off")
        elif command == "Enter":
            self.performEnter()
            print("Enter")
        elif command == "00":
            self.perform00()
            print("Send00")
        elif command == "01":
            self.perform01()
            print("Send01")
        elif command == "02":
            self.perform02()
            print("Send02")
        elif command == "03":
            self.perform03()
            print("Send03")
        elif command == "04":
            self.perform04()
            print("Send04")
        elif command == "05":
            self.perform05()
            print("Send04")
        else:
            print("Error")
            print(command)
    def DESIUpdateState(self, state):
        pass
    def performShutdown():
        print("Shutting Down")
        GPIO.output(self.OUT_PAUSE, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(self.OUT_PAUSE, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(self.OUT_ENTER, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(self.OUT_ENTER, GPIO.HIGH)
        time.sleep(0.2)
        self.State_Main = "Shutdown"
    def performPause(self):
        if self.State_Main != "Pause"
            GPIO.output(self.OUT_PAUSE, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_PAUSE, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.HIGH)
            time.sleep(0.2)
            self.State_Main = "Pause"
        else:
            print("Shutting Down")
            self.performShutdown()
    def performStart(self):
        if self.State_Main == "Idle"
            GPIO.output(self.OUT_0, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_0, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.HIGH)
            time.sleep(0.2)
            self.State_Main = "Speed0"
        else:
            print("Already Started")
    def perform00(self):
        if self.State_Main == "Speed1" or self.State_Main == "Idle"
            GPIO.output(self.OUT_0, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_0, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.HIGH)
            time.sleep(0.2)
            self.State_Main = "Speed0"
        else:
            print("Nope")
    def perform01(self):
        if self.State_Main == "Speed0" or self.State_Main == "Speed2":
            GPIO.output(self.OUT_0, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_0, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.HIGH)
            time.sleep(0.2)
            self.State_Main = "Speed1"
        else:
            print("Nope")
    def perform02(self):
        if self.State_Main == "Speed1" or self.State_Main == "Speed3":
            GPIO.output(self.OUT_0, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_0, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.HIGH)
            time.sleep(0.2)
            self.State_Main = "Speed2"
        else:
            print("Nope")
    def perform03(self):
        if self.State_Main == "Speed4" or self.State_Main == "Speed2":
            GPIO.output(self.OUT_0, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_0, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.HIGH)
            time.sleep(0.2)
            self.State_Main = "Speed3"
        else:
            print("Nope")
    def perform04(self):
        if self.State_Main == "Speed3"
            GPIO.output(self.OUT_0, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_0, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.OUT_ENTER, GPIO.HIGH)
            time.sleep(0.2)
            self.State_Main = "Speed4"
        else:
            print("Nope")

