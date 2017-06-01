#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 08:15:30
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import os
import time
import RPi.GPIO as GPIO
import VoyagerHCSR04
import DESIConfig as DESI

### Set path ###
TOP_DIR = os.path.dirname(os.path.abspath(__file__))

### Global Variables ###
DESI = DESI.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", Trig_V1, Echo_V1)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", Trig_V2, Echo_V2)


def main():
    # Sets the Pin Numbering Scheme to same as Cobbler
    
    
    # Initialize DESI States
    DESI.initDESI()
    try:
        while True:
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