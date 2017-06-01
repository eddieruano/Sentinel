#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 02:07:17
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import os
import time
import VoyagerHCSR04


### Set path ###
TOP_DIR = os.path.dirname(os.path.abspath(__file__))

def main():

    Voyager1 = VoyagerHCSR04("Voyager1", 17, 4)
    Voyager2 = VoyagerHCSR04("Voyager2", 22, 27)
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