#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-06 05:43:20
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
################################## IMPORTS ###################################
import sys
import os.path
import signal
import time
#
import collections
import pyaudio
import wave
from math import floor
# Customs Mods #
import RPi.GPIO as GPIO
import Sentinel as Sentinel
# Local Modules #
################################### PATHS #####################################
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import drivers.VoyagerHCSR04 as VoyagerHCSR04
import DESIConfig as DESIConfig
import drivers.MPR121 as MPR121
import trigger.snowboydetect as snowboydetect
############################ INITIALIZE CLASSES ###############################
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
#TouchSense = MPR121.MPR121()
Sentinel = Sentinel.Sentinel()
################################## PATHS ######################################

def main():
    # Variables
    # 
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    # try:
    #     if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
    #         print("TSense Error")
    #         sys.exit(1)
    # except OSError as e:
    #     print(e)
    #     print("Sensor Error.")
    #     sys.exit(1)
    Sentinel.getStateKnob(DESI)
    Sentinel.setStateKnob()
    #Sentinel.updateActiveLock(TouchSense)
    # Add the triggers
    GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, callback=StartHandler, bouncetime=Sentinel.CONST_BOUNCE)
    GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING, callback=PauseHandler, bouncetime=Sentinel.CONST_BOUNCE)
    try:
        DESI.DESISendResponse("audio/wav_lets_start.wav")
        print("Listening")
        localKnobState = Sentinel.StateKnob
        while True:
            # Update the ActiveLock
            #Sentinel.updateActiveLock(TouchSense)
            # Query the knob states
            Sentinel.getStateKnob(DESI)
            # Set the Knob State according to the recent get
            Sentinel.setStateKnob()
            # Check if the knob changed position
            if (Sentinel.StateKnob != localKnobState):
                localKnobState = Sentinel.StateKnob
                DESI.DESISend(Sentinel.StateKnob * 1.0)
            # Set the Speed if the knob doesn't match up
            if (Sentinel.StateKnob != Sentinel.StateSpeed):
                DESI.DESISend(Sentinel.StateKnob * 1.0)
                Sentinel.StateSpeed = (Sentinel.StateKnob * 1.0)
            # Start Query for Distances
            Sentinel.Proximity = queryDistance()
            # Check to see if the Distance is above the threshold
            if (Sentinel.Proximity > 12.0):
                print("Yellow")
                # Start the coundown here
                Sentinel.ProxCountdown -= 1
                # Here we trigger finally
                if(Sentinel.ProxCountdown == 0):
                    i = 0
                    while i < Sentinel.Redux:
                        DESI.DESISend("SendDown")
                        i += 1
                    # Update the new speed and redux
                    Sentinel.setSpeed(Sentinel.StateSpeed - Sentinel.Redux)
                    # Restart the counter
                    Sentinel.ProxCountdown = Sentinel.PROXCOUNT
            else: # Else, we're back in the green
                Sentinel.ProxCountdown = Sentinel.PROXCOUNT
                Sentinel.setSpeed(Sentinel.StateKnob * 1.0)
            # Here we check for contact
            # if not Sentinel.ActiveLock:
            #     # Start the countdown to regain contact
            #     if Sentinel.CapCountdown == 0 and not Sentinel.ContactLock:
            #         DESI.DESISend("Pause")
            #         Sentinel.ContactLock = True
            #     else:
            #         # Continue to countdown
            #         Sentinel.CapCountdown -= 1
            # else: 
            #     # Any contact will reset the counter because it's sensitive
            #     Sentinel.CapCountdown = Sentinel.CAPCOUNT
            #     Sentinel.ContactLock = False
            #     Sentinel.setSpeed(Sentinel.StateKnob * 1.0)
            time.sleep(Sentinel.RunningLoopSpeed)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Shutdown Mission.")
        #Detector.terminate()
        
### END OF MAIN ###
"""Helper Functions"""
def activateAlexa():
    GPIO.output(DESI.OUT_ALEXA, GPIO.LOW)
    time.sleep(2)
    GPIO.output(DESI.OUT_ALEXA, GPIO.HIGH)
def queryDistance():
    distv1 = Voyager1.get_distance()
    distv2 = Voyager2.get_distance()
    # Sanitize
    distv1 = sanitizeDistance(Voyager1, distv1)
    distv2 = sanitizeDistance(Voyager2, distv2)
    # Subtract 3.5 to get 0
    distv1 = abs(distv1 - 3.5)
    distv2 = abs(distv2 - 3.5)
    if distv1 == -1.0 and distv2 != -1.0:
        print("Check Sensor 1")
        return distv2
    elif distv2 == -1.0 and distv1 != -1.0:
        print("Check Sensor 2")
        return distv1
    else:
        ave = (distv1 + distv2) / 2
    return ave
def sanitizeDistance(voy, inDist):
    tries = 0
    while inDist == -1.0 and tries < Sentinel.ProximityRetries:
        inDist = Voyager1.get_distance()
    return inDist
def StartHandler(channel):
    print("Starting")
    DESI.DESISend("Start")
def PauseHandler(channel):
    if (Sentinel.StateKnob == 0):
        DESI.DESISend("Shutdown")
        time.sleep(30)
        GPIO.cleanup()
        print("Shutdown")
        sys.exit(0)
    else:
        print("pause")
        DESI.DESISend("Pause")
#def signal_handler(signal, frame):
#    global HotwordInterrupt
#    HotwordInterrupt = True
#def interrupt_callback():
#    global HotwordInterrupt
#    return HotwordInterrupt
### MAIN CALL ###
if __name__ == "__main__":
    main()