#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-05 00:32:04
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
################################## IMPORTS ###################################
import sys
import os.path
import signal
import time
from math import floor
# Customs Mods #
import RPi.GPIO as GPIO
import Sentinel as Sentinel
# Local Modules #
################################### PATHS #####################################
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import drivers.VoyagerHCSR04 as VoyagerHCSR04
import drivers.DESIConfig as DESIConfig
import drivers.MPR121 as MPR121
############################ INITIALIZE CLASSES ###############################
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()
Sentinel = Sentinel.Sentinel()
################################## PATHS ######################################

def main():
    # Variables
    lastZone = -1.0
    subZone = 0.0
    redFlag = False
    saveSpeed = DESI.State_Speed
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
        print("TSense")
        sys.exit(1)

    Sentinel.getStateKnob(DESI)
    Sentinel.setStateKnob()
    Sentinel.updateActiveLock(TouchSense)
    # Add the triggers
    GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED0, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED1, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED2, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED3, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED4, GPIO.FALLING)
    try:
        print("Listening")
        
        while True:
            Sentinel.updateActiveLock(TouchSense)
            if(Sentinel.ActiveLock):
                if(GPIO.event_detected(DESI.IN_START)):
                    print("start")
                    DESI.DESISend("Start")
                elif(GPIO.event_detected(DESI.IN_PAUSE)):
                    print("pause")
                    DESI.DESISend("Pause")
                elif(GPIO.event_detected(DESI.IN_SPEED0)):
                    print("0")
                    DESI.DESISend("Send00")
                elif(GPIO.event_detected(DESI.IN_SPEED1)):
                    print("1")
                    DESI.DESISend("Send01")
                elif(GPIO.event_detected(DESI.IN_SPEED2)):
                    print("2")
                    DESI.DESISend("Send02")
                elif(GPIO.event_detected(DESI.IN_SPEED3)):
                    print("3")
                    DESI.DESISend("Send03")
                elif(GPIO.event_detected(DESI.IN_SPEED4)):
                    print("4")
                    DESI.DESISend("Send04")
                else:
                    pass

                Sentinel.Proximity = queryDistance()
                if (Sentinel.Proximity > 12.0):
                    print("Yellow")
                time.sleep(Sentinel.RunningLoopSpeed)
            else:
                #print(Sentinel.TouchRegister)
                time.sleep(Sentinel.RunningLoopSpeed)
                print("Countdown Started")
                Sentinel.Countdown -= 1
                if(Sentinel.Countdown == 0):
                    DESI.DESISend("Pause")
                    Sentinel.Countdown = 100
                else:
                    pass
                #time.sleep(Sentinel.CountdownLoopSpeed)
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
#def signal_handler(signal, frame):
#    global HotwordInterrupt
#    HotwordInterrupt = True
#def interrupt_callback():
#    global HotwordInterrupt
#    return HotwordInterrupt
### MAIN CALL ###
if __name__ == "__main__":
    main()