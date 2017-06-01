#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 08:43:51
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import os
import time
import RPi.GPIO as GPIO
import VoyagerHCSR04
import MPR121
import DESIConfig

### Set path ###
TOP_DIR = os.path.dirname(os.path.abspath(__file__))

### Global Variables ###
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()

def main():
    
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    # Initialize TouchSense Capacitive Sensor Array
    # Initialize communication with MPR121 using default I2C bus of device, and
    # default I2C address (0x5A).  
    if not TouchSense.begin():
        print('Error initializing MPR121.  Check your wiring!')
        sys.exit(1)

    """Starts Main Workout Loop"""
    ActiveFlag = True
    try:
        while ActiveFlag:
            distv1 = Voyager1.get_distance()
            print ("Measured Distance = %.1f cm" % distv1)
            time.sleep(1)
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Shutdown Mission.")
        GPIO.cleanup()

### MAIN CALL ###
if __name__ == "__main__":
    main()