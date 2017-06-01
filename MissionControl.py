#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 07:06:32
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import os
import time
import RPi.GPIO as GPIO
import VoyagerHCSR04


### Set path ###
TOP_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    Trig_V1 = 4
    Echo_V1 = 17
    Trig_V2 = 27
    Echo_V2 = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Trig_V1, GPIO.OUT)
    GPIO.setup(Echo_V1, GPIO.IN)
    GPIO.setup(Trig_V2, GPIO.OUT)
    GPIO.setup(Echo_V2, GPIO.IN)

    Voyager1 = VoyagerHCSR04.Voyager("Voyager1", Trig_V1, Echo_V1)
    Voyager2 = VoyagerHCSR04.Voyager("Voyager2", Trig_V2, Echo_V2)
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