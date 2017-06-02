#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-02 12:38:05
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import sys
import os.path
import signal
import time
# Customs Mods #
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
# Local Modules #
### Set path ###
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import drivers.VoyagerHCSR04 as VoyagerHCSR04
import drivers.DESIConfig as DESIConfig
### Global Variables ###
DESI = DESIConfig.DESI()
#Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
#Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
#TouchSense = MPR121.MPR121()

def main():
    # Variables
    proxError = 0.0
    distv1 = 0.0
    distv2 = 0.0
    slack = 0.0
    contact = False
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    #DESI.initProximity(Voyager1, Voyager2)
    #if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
    #    print("TSense")
    #    sys.exit(1)
    try:
        DESI.DESIListen()
        while True:

            # Query for the proximity of Megan #
            #distv1 = Voyager1.get_distance()
            #time.sleep(0.3)
            #distv2 = Voyager2.get_distance()
            #distAverage = (distv1 + distv2) / 2
            #proxError = distv1 - distv2
            #contact = checkContact()
            #state = checkState(distAverage)
            #if state == "Red":
            #    print("Red!")
            #    past_state = state
            #    DESI.send("Pause")
            #    time.sleep(5)
            #    DESI.send(past_state)
            #elif state == "Yellow":
            #    DESI.send("Down")
            #    time.sleep(0.4)
            #    DESI.send("Down")
            #    time.sleep(0.4)
            #    DESI.send("Down")
            #else:
            #    print("Green!")
            #    slack = 30 - distAverage
            #    redux = ((distAverage - 10) / 2) * 10
            #    redux = int(redux)
#
#           time.sleep(1)
    # Catch Ctrl+C
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
#def signal_handler(signal, frame):
#    global HotwordInterrupt
#    HotwordInterrupt = True
#def interrupt_callback():
#    global HotwordInterrupt
#    return HotwordInterrupt
### MAIN CALL ###
if __name__ == "__main__":
    main()