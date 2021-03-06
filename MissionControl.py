#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-14 11:17:19
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
################################## IMPORTS ###################################
import logging
import os.path
import signal
import sys
import time
# 
from math import floor
# Customs Mods #
import RPi.GPIO as GPIO
import Sentinel as Sentinel
# Local Modules #
################################### PATHS #####################################
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import DESIConfig as DESIConfig
import drivers.MPR121 as MPR121
import drivers.VoyagerHCSR04 as VoyagerHCSR04
#import trigger.snowboydetect as snowboydetect
############################ INITIALIZE CLASSES ###############################
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()
Sentinel = Sentinel.Sentinel()
################################# LOGGER ######################################
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
def main():
    global Houston
    # Variables/Flags
    flagRailWarning = False
    flagSelectorWarning = False
    flagProximityWarning = False
    flagRedux = False
    flagStartSet = False
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    Houston.info("Checking Cap Sensor SDA")
    try:
        if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
            Houston.error("TSense Error")
            sys.exit(1)
    except OSError as e:
        Houston.error(e)
        Houston.critical("Sensor Error.")
        sys.exit(1)

    Houston.info("Getting Knob State") 
    # Update the Knob state in Sentinel 
    Sentinel.queryKnobState(DESI)    
    Houston.info(Sentinel.StateKnob)   
    # Update the Active Lock checks for Contact
    Houston.info("Checking Active Lock.")
    Sentinel.updateActiveLock(TouchSense)
    Houston.info(Sentinel.ActiveLock)
    # Single Start Trigger
    Houston.info("Adding Start Trigger")
    GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, callback=StartHandler, bouncetime=Sentinel.CONST_BOUNCE)
    try:
        #Wait for the Start Command
        Houston.info("Waiting for Start Command.")
        while not Sentinel.StartDetect:
            Sentinel.queryKnobState(DESI)
        #Wait until the correct Knob State Happens
        Houston.info("Waiting For Knob Zero Position")
        while Sentinel.StateKnob != 0.0:
            # if the counter reaches zero issue warning
            if (Sentinel.SpCount == 0):
                DESI.DESISendResponse("audio/wav_sp_sel.wav")
                Sentinel.SpCount = Sentinel.CONST_RESCOUNT
            else:
                # decrement counter
                time.sleep(0.1)
                Sentinel.SpCount-=1
            # we verify here
            Sentinel.queryKnobState(DESI)
        Houston.info("Knob in Zero, Now initializing Treadmill")
        # in correct setting so we wait for speech mutex
        Sentinel.waitMutexSpeech()
        DESI.DESISendResponse("audio/wav_okay_megan.wav")
        Houston.info("Waiting 1 Second.")
        time.sleep(1)
        Houston.info("Let's Start is being Played.")
        Sentinel.waitMutexSpeech()
        DESI.DESISendResponse("audio/wav_lets_start.wav")
        Houston.info("Enabling Pause/Stop Button")
        GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING, callback=PauseHandler, bouncetime=Sentinel.CONST_BOUNCE)
        flagStartSet = True
        """MAIN WORKOUT LOOP BEGINS"""
        while True:
            if Sentinel.flagShut == True:
                continue
            localKnobState = Sentinel.StateKnob
            # Update the ActiveLock
            Sentinel.updateActiveLock(TouchSense)
            # Query the knob states
            Sentinel.getStateKnob(DESI)
            # Set the Knob State according to the recent get
            Sentinel.setStateKnob()
            speed = getSpeed()
            if (Sentinel.StateKnob == 0.0) and (flagStartSet == False):
                GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, callback=StartHandler, bouncetime=Sentinel.CONST_BOUNCE)
                flagStartSet = True
            elif(flagStartSet == True):
                GPIO.remove_event_detect(DESI.IN_START)
                flagStartSet = False
                
            # Check if the knob changed position
            if (Sentinel.StateKnob != localKnobState):
                localKnobState = Sentinel.StateKnob
                speed = getSpeed()
                if Sentinel.flagPause == False:
                    DESI.DESISend(speed)
                print("State Indifff")
                print(speed)
            if (Sentinel.CapLock == True):
                continue
            if (Sentinel.ProxLock == True):
                continue
            # Set the Speed if the knob doesn't match up
            #if (Sentinel.StateKnob != Sentinel.ActualSpeed):
            #    DESI.DESISend(Sentinel.StateKnob * 1.0)
            #    Sentinel.ActualSpeed = (speed)
            # Here we check for contact
            """ CAPACITANCE CHECKS """
            # Check for an issue warning
            flagRailWarning = checkRailWarning(flagRailWarning)
            # if we aren't touching
            if not Sentinel.ActiveLock and Sentinel.flagPause == False:
                print("NO CONTACT")
                # If we reach zero on the counter and not in pause
                if ((Sentinel.CapCountdown == 0) and (Sentinel.CapLock == False)):
                    # save current workout state
                    saved_state = Sentinel.StateKnob
                    Sentinel.waitMutexSpeech()
                    DESI.DESISendResponse(DESI.RespondPaused)   #pause
                    DESI.DESISend("Pause")
                    Sentinel.flagPause = True
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
            Sentinel.Proximity = queryDistance()
            #print (Sentinel.Proximity)
            if Sentinel.Proximity > 12.0 and Sentinel.flagPause == False:
                flagProximityWarning = True
                # If we reach zero on the counter and not in pause
                if ((Sentinel.ProxCountdown == 0) and (Sentinel.ProxLock == False)):
                    Sentinel.ProximityRetries += 1
                    # reduce speed
                    i = 0.0
                    while i < Sentinel.Redux:
                        #print("Reducing By: " + i)
                        DESI.DESISend("SendDown")
                        i += 1.0
                        flagRedux = True
                        Sentinel.ActualSpeed = Sentinel.ActualSpeed - 0.1
                    # Enable the CapLock
                    if (Sentinel.ProximityRetries > Sentinel.CONST_PROX_RETRIES):
                        Sentinel.ProxLock = True
                        DESI.DESISend("Pause")
                        Sentinel.flagPause = True
                        Sentinel.waitMutexSpeech()
                        DESI.DESISendResponse(DESI.RespondPause)
                        print("ProxLocked.")
                    # Runs forever until CapLock disabled
                else:
                    # Else we are not making contact but not end of count
                    Sentinel.ProxCountdown -= 1
            else:  # we are making contact
                    Sentinel.ProxCountdown = Sentinel.PROXCOUNT
                    flagProximityWarning = False
                    sp = getSpeed()
                    if flagRedux:
                        DESI.DESISend(sp)
                        flagRedux = False
            """"""""""""" END PROXIMITY CHECKS """""""""""""""""""""
            #print(Sentinel.ActualSpeed)
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
    if (Sentinel.StateKnob == 0.0) and DESI.State_Main == "Pause":
        DESI.DESISend("Shutdown")
        Sentinel.flagShut = True
        GPIO.cleanup()
        print("Shutdown")
        return
    else:
        print("Starting")
        Sentinel.StartDetect = True
        DESI.DESISend("Start")

def getSpeed():
    if Sentinel.StateKnob == 0.0:
        Sentinel.setSpeed(0.0)
        return "Send00"
    elif Sentinel.StateKnob == 1.0:
        Sentinel.setSpeed(2.0)
        return "Send01"
    elif Sentinel.StateKnob == 2.0:
        Sentinel.setSpeed(2.5)
        return "Send02"
    elif Sentinel.StateKnob == 3.0:
        Sentinel.setSpeed(3.0)
        return "Send03"
    elif Sentinel.StateKnob == 4.0:
        Sentinel.setSpeed(3.5)
        return "Send04"
    else:
        return "Send00"
def PauseHandler(channel):
    print("pause")
    DESI.DESISend("Pause")
    Sentinel.flagPause = not Sentinel.flagPause
    if Sentinel.CapLock == True:
        Sentinel.CapLock = False
    elif Sentinel.ProxLock == True:
        Sentinel.ProxLock = False
        Sentinel.ProximityRetries = 0
def checkRailWarning(flag):
    if ((Sentinel.ActiveLock == False) and (flag == False)):
        if (Sentinel.CapCountdown == (Sentinel.CAPCOUNT / 2)):
            DESI.DESISendResponse(DESI.RespondRails)
        return True
    return False
### MAIN CALL ###
if __name__ == "__main__":
    main()