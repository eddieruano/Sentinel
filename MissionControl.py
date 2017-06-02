#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-02 01:03:26
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import sys
import os.path
import signal
import time
import curses
import logging
# Customs Mods #
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
# Local Modules #
### Set path ###
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import drivers.VoyagerHCSR04 as VoyagerHCSR04
import drivers.HUD as HUD
import drivers.DESIConfig as DESIConfig

### Configure Logger ###
logging.basicConfig()
logger = logging.getLogger("Houston")
logger.setLevel(logging.INFO)
### Global Variables ###
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()
HUD = HUD.HUD()

def main():
    # Variables
    proxError = 0.0
    distv1 = 0.0
    distv2 = 0.0
    slack = 0.0
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
        logger.info("TouchSense Failure.")
                                  # Initialize comms with MPR121 using default I2C bus of device, and # default I2C address (0x5A). 
        sys.exit(1)

    try:
        while True:
            # Query for the proximity of Megan #
            distv1 = Voyager1.get_distance()
            distv2 = Voyager2.get_distance()
            distAverage = distv1 + distv2 / 2

            proxError = distv1 - distv2

            state = checkState(distAverage)

            if state != "Green":
                if state == "Red":
                    DESI.send("Pause")

                slack = 30 - distAverage
                redux = ((distAverage - 10) / 2) * 10
                redux = int(redux)

            renderDisplay(self, STATE, SPEED, distv1, distv2, CONTACT_M, CONTACT_L, CONTACT_R, CONTACT_T, "Active"):
            time.sleep(0.5)
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