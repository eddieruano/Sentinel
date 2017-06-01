#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 10:25:15
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import sys
import os.path
import signal
import time
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import tresources.VoyagerHCSR04
import tresources.DESIConfig
import snowboydecoder

### Set path ###
### Global Variables ###
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()
### Begin Voice Detection Config ###
HotwordInterrupt = False
TriggerWord = DESI.pmdl
Detector = snowboydecoder.HotwordDetector(TriggerWord, sensitivity=0.5)

def main():
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    # Initialize TouchSense Capacitive Sensor Array
    # Initialize comms with MPR121 using default I2C bus of device, and
    # default I2C address (0x5A).  
    if not TouchSense.begin():
        print('Error initializing MPR121')
        sys.exit(1)
    # Voice Detection
    signal.signal(signal.SIGINT, signal_handler)
    detector.start(detected_callback=snowboydecoder.play_audio_file,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)
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
        Detector.terminate()
        GPIO.cleanup()
    ### END OF MAIN ###
"""Helper Functions"""
def activateAlexa():
    GPIO.output(DESI.OUT_ALEXA, GPIO.LOW)
    time.sleep(2)
    GPIO.output(DESI.OUT_ALEXA, GPIO.HIGH)
def signal_handler(signal, frame):
    global HotwordInterrupt
    HotwordInterrupt = True
def interrupt_callback():
    global HotwordInterrupt
    return HotwordInterrupt
### MAIN CALL ###
if __name__ == "__main__":
    main()