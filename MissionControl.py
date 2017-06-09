#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-08 23:24:41
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
#import trigger.snowboydetect as snowboydetect
############################ INITIALIZE CLASSES ###############################
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()
Sentinel = Sentinel.Sentinel()
################################## PATHS ######################################

def main():
    # Variables/Flags
    flagRailWarning = False
    flagSelectorWarning = False
    flagProximityWarning = False
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    try:
        if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
            print("TSense Error")
            sys.exit(1)
    except OSError as e:
        print(e)
        print("Sensor Error.")
        sys.exit(1)
    Sentinel.getStateKnob(DESI)
    Sentinel.setStateKnob()
    time.sleep(1)
    Sentinel.getStateKnob(DESI)
    Sentinel.setStateKnob()
    Sentinel.updateActiveLock(TouchSense)
    # Single Start Trigger
    GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, callback=StartHandler, bouncetime=Sentinel.CONST_BOUNCE)
    try:
        print("Listening")
        #Wait for the Start Command
        while not Sentinel.StartDetect:
            print("Off")
        #Wait until the correct Knob State Happens
        while Sentinel.StateKnob != 0:
            # if the counter reaches zero issue warning
            if (Sentinel.SpCount == 0):
                
                DESI.DESISendResponse("audio/wav_sp_sel.wav")
                Sentinel.SpCount = Sentinel.CONST_RESCOUNT
            else:
                # decrement counter
                time.sleep(0.1)
                Sentinel.SpCount-=1
            # we verify here
            Sentinel.getStateKnob(DESI)
            Sentinel.setStateKnob()
        # in correct setting so we wait for speech mutex
        Sentinel.waitMutexSpeech()
        DESI.DESISendResponse("audio/wav_okay_megan.wav")
        # issue start
        Sentinel.waitMutexSpeech()
        DESI.DESISendResponse("audio/wav_lets_start.wav")
        # officially add pause event
        GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING, callback=PauseHandler, bouncetime=Sentinel.CONST_BOUNCE)
        while True:
            # Update the ActiveLock
            Sentinel.updateActiveLock(TouchSense)
            # Query the knob states
            Sentinel.getStateKnob(DESI)
            # Set the Knob State according to the recent get
            Sentinel.setStateKnob()
            speed = getSpeed()
            if (Sentinel.capLock == True):
                continue
            # Check if the knob changed position
            if ((Sentinel.StateKnob * 1.0) != localKnobState):
                localKnobState = Sentinel.StateKnob
                DESI.DESISend(speed)
                print("in")
            # Set the Speed if the knob doesn't match up
            if ((Sentinel.StateKnob * 1.0) != Sentinel.StateSpeed):
                DESI.DESISend(Sentinel.StateKnob * 1.0)
                Sentinel.StateSpeed = (speed)
            # Here we check for contact
            """ CAPACITANCE CHECKS """
            # Check for an issue warning
            flagRailWarning = checkRailWarning(flagRailWarning)
            # if we aren't touching
            if not Sentinel.ActiveLock:
                # If we reach zero on the counter and not in pause
                if ((Sentinel.CapCountdown == 0) and (Sentinel.CapLock == False)):
                    # save current workout state
                    saved_state = Sentinel.StateKnob
                    DESI.DESISendResponse(DESI.RespondPaused)   #pause
                    DESI.DESISend("Pause")
                    print(DESI.State_Main)
                    # Enable the CapLock
                    Sentinel.CapLock = True
                    print("CapLocked.")
                    # Runs forever until CapLock disabled
                else:
                    # Else we are not making contact but not end of count
                    Sentinel.CapCountdown -= 1
            else:  # we are making contact
                    Sentinel.CapCountdown = Sentinel.CAPCOUNT
                    flagRailWarning = False
            
            """ START PROXIMITY CHECKS """
            #Start Query for Distances
            # Sentinel.Proximity = queryDistance()
            # if (Sentinel.Proximity > 12.0):
            #     #if (flagProximityWarning == False):
            #     #    DESI.DESISendResponse(DESI.RespondProx)
            #     #    flagProximityWarning = True
            #     print("Yellow")
            #     # Start the coundown here
            #     Sentinel.ProxCountdown -= 1

            #     # Here we trigger finally
            #     if(Sentinel.ProxCountdown == 0):
            #         i = 0
            #         while i < Sentinel.Redux:
            #             DESI.DESISend("SendDown")
            #             i += 1
            #         # Update the new speed and redux
            #         Sentinel.setSpeed(Sentinel.StateSpeed - Sentinel.Redux)
            #         # Restart the counter
            #         Sentinel.ProxCountdown = Sentinel.PROXCOUNT
            #         Sentinel.ProxLock = True

            # else: # Else, we're back in the green
            #     if Sentinel.ProxLock == True:

            #         DESI.DESISend()
            #     Sentinel.ProxCountdown = Sentinel.PROXCOUNT
            #     Sentinel.setSpeed(Sentinel.StateKnob * 1.0)
            """"""""""""" END PROXIMITY CHECKS """""""""""""""""""""
            time.sleep(Sentinel.RunningLoopSpeed)
    except KeyboardInterrupt:
        GPIO.cleanup()
        DESI.DESICleanup()
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
    if (Sentinel.StateKnob == 0) and DESI.State_Main == "Pause":
        DESI.DESISend("Shutdown")
        time.sleep(30)
        GPIO.cleanup()
        print("Shutdown")
        sys.exit(0)
    else:
        print("Starting")
        Sentinel.StartDetect = True
        DESI.DESISend("Start")
def getSpeed():
    if Sentinel.StateKnob == 0:
        return "Send00"
    elif Sentinel.StateKnob == 1:
        return "Send01"
    elif Sentinel.StateKnob == 2:
        return "Send02"
    elif Sentinel.StateKnob == 3:
        return "Send03"
    elif Sentinel.StateKnob == 4:
        return "Send04"
    else:
        return "Send00"
def PauseHandler(channel):
    print("pause")
    DESI.DESISend("Pause")
    if Sentinel.CapLock == True:
        Sentinel.CapLock = False
    elif Sentinel.ProxLock == True:
        Sentinel.ProxLock = False
def checkRailWarning(flag):
    if ((Sentinel.ActiveLock == False) and (flag == False)):
        if (Sentinel.CapCountdown == (Sentinel.CAPCOUNT / 2)):
            DESI.DESISendResponse(DESI.RespondRails)
        return True
    return False

#def signal_handler(signal, frame):
#    global HotwordInterrupt
#    HotwordInterrupt = True
#def interrupt_callback():
#    global HotwordInterrupt
#    return HotwordInterrupt
### MAIN CALL ###
if __name__ == "__main__":
    main()